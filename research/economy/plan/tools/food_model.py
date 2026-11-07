"""R64.3 (M112): food consumption of a city population, from the nutrition record.

Reads research/economy/data/nutrient_needs.json (version 2), nutrient_profiles.json and satiety_index.json, and a case
file (city inputs and goods available per person per day). Solves, per person of the city (adult equivalent):

  stage 1 (basal):    energy of basal function, up to 1.2 x REE (the lowest daily expenditure; M114)
  stage 2 (fed):      maximise z = energy eaten / energy need (M93: being fed is the baseline);
                      labour capacity = (energy / REE - 1.2) / (PAL - 1.2)
  stage 3 (minima):   maximise the mean coverage of the nutrient minima; deficient = below a minimum (M114)
  stage 4 (adequacy): maximise the mean adequacy ratio MAR = mean_i min(1, intake_i / target_i)
  stage 5 (quality):  minimise energy taken from lower-quality goods (people draw on the better stocks)
each stage holds the optimum of the stages before it

subject to: availability per good, energy eaten <= need, the user's ceilings per good (milk 3 L, fat 250 g per good,
fruit at most one watermelon) and lactose where it applies. Protein is energy like any other (excess is turned into
glucose) up to the liver's daily urea capacity, spread over three meals; the nutrient ceilings, the protein ceiling
and fat are harms, reported (M101, M114). The specification is
research/economy/food_model.md; every equation there maps to a line here.

usage: food_model.py <case.json> [--json out.json]
"""
import json
import os
import sys

from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data')
TOL = 1e-6


def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as fh:
        return json.load(fh)


def num(v, male_share):
    """A level value as one number: sex values weighted by the male share; a range [lo, hi] as its midpoint."""
    if isinstance(v, dict):
        if 'male' in v:
            return male_share * num(v['male'], male_share) + (1 - male_share) * num(v['female'], male_share)
        raise ValueError(v)
    if isinstance(v, list):
        return (v[0] + v[1]) / 2.0
    return v


CEREALS = {'BONUS_WHEAT', 'BONUS_RICE', 'BONUS_CORN'}           # niacin about 1/3 available (Carpenter 1983)
ANIMAL = {'BONUS_COW', 'BONUS_PIG', 'BONUS_SHEEP', 'BONUS_DEER', 'BONUS_HORSE', 'BONUS_FISH', 'BONUS_CLAM',
          'BONUS_CRAB', 'BONUS_SHRIMP', 'BONUS_WHALE', 'BONUS_DAIRY'}
FRUIT = {'BONUS_APPLE', 'BONUS_BANANA', 'BONUS_LEMON'}
DRINK_HI = {'BONUS_DAIRY': 'milk_full_fat', 'BONUS_ALCOHOL': 'lager', 'BONUS_TEA': 'tea'}


def composition(profiles, whole):
    """Per good: nutrients per gram, from the first (as-eaten) form; the whole cod for BONUS_FISH."""
    out = {}
    for g, forms in profiles['goods'].items():
        if not g.startswith('BONUS_'):
            continue
        if g == 'BONUS_FISH':
            parts = {f['form']: f for f in forms}
            cod = whole['cod_as_eaten']['value']
            COD_PARTS = cod['parts_pct_of_round_weight']
            tot = float(sum(COD_PARTS.values()))
            row = {}
            for k in profiles['units']:
                row[k] = sum((parts[p].get(k) or 0.0) * w for p, w in COD_PARTS.items()) / tot
            liver = parts['liver (lingcod)']
            row['vit_a_rae'] += cod['liver_oil_vit_a_ug_per_100g'] * liver['fat'] / 100.0 * COD_PARTS['liver (lingcod)'] / tot
            base = {k: v for k, v in row.items()}
        else:
            base = {k: (forms[0].get(k) or 0.0) for k in profiles['units']}
        out[g] = finish(g, base, forms[0], profiles)
        for f in forms[1:]:                                          # other forms, chosen in a case as 'GOOD:form'
            out[g + ':' + f['form']] = finish(g, {k: (f.get(k) or 0.0) for k in profiles['units']}, f, profiles, False)
        for f in profiles['mext'].get(g, []):                        # MEXT forms, chosen as 'GOOD:mext:form' (R68)
            b3 = {k: (f.get(k) or 0.0) for k in profiles['units']}
            pg = finish(g, b3, dict(f, iodine=f.get('iodine') if f.get('iodine') is not None else 0.0), profiles, False)
            pg['niacin_ne'] = (f.get('niacin_ne') or 0.0) / 100.0      # MEXT gives niacin equivalents directly
            out[g + ':mext:' + f['form']] = pg
        if g == 'BONUS_FISH':                                        # whole herring by season (fat only changes)
            h = [f for f in forms if f['form'] == 'herring'][0]
            for season, fat in whole['herring_whole_fat_pct']['value'].items():
                b2 = {k: (h.get(k) or 0.0) for k in profiles['units']}
                b2['fat'] = fat
                b2['kcal'] = 4 * b2['protein'] + 9 * fat + 4 * b2['carbohydrate']
                out[g + ':herring whole, ' + season] = finish(g, b2, h, profiles, False)
    return out


def finish(g, base, form, profiles, default=True):
    if default and form.get('iodine') is None and profiles['mext'].get(g):   # SR Legacy holds no iodine: MEXT of the
        # same good's default form (record 2d); other forms keep 0 where no iodine record exists
        iod = profiles['mext'][g][0].get('iodine')
        base['iodine'] = iod if iod is not None else 0.0
    per_g = {k: v / 100.0 for k, v in base.items()}
    niacin = per_g['niacin'] * (1 / 3.0 if g in CEREALS else 1.0)
    per_g['niacin_ne'] = niacin + per_g['tryptophan'] * 1000.0 / 60.0
    return per_g


def quality(c, target, E):
    """MAR of a diet of this good alone at the energy need (ceilings ignored): the good's nutritional quality."""
    if c['kcal'] <= 0:
        return 0.0
    grams = E / c['kcal']
    return sum(min(1.0, c[i] * grams / t) for i, t in target.items()) / len(target)


def solve(case):
    needs, profiles, sat = load('nutrient_needs.json'), load('nutrient_profiles.json'), load('satiety_index.json')
    ms, W = case['male_share'], case['body_weight_kg']
    comp = composition(profiles, needs['whole_animal'])
    goods = [g for g in case['available_g'] if case['available_g'][g] > 0]
    for g in goods:
        if g not in comp:
            raise SystemExit('no composition record for ' + g)
    en = needs['energy']
    ree = en['ree_kcal']['value']['per_kg'] * W + en['ree_kcal']['value']['constant']
    pal_ceiling = en['pal_limits']['value']['alimentary_ceiling']
    pal = min(case['pal'], pal_ceiling)
    E = pal * ree
    nut = needs['nutrients']
    protein_target = num(nut['protein']['optimum']['value'], ms) * W
    hot = case.get('hot_shift_share', 0.0)
    sweat_na = num(nut['sodium']['sweat_per_hot_shift']['value'], ms) * hot
    animal = any(g.split(':')[0] in ANIMAL for g in goods)
    fe_abs = num(needs['absorption']['iron_fraction']['value']['mixed_diet' if animal else 'vegetarian'], ms)
    tea = any(g.split(':')[0] == 'BONUS_TEA' for g in goods) and case.get('tea_with_meals', True)
    if tea:                                                          # tea with meals: iron absorbed -64 % (record 2c)
        fe_abs *= 1.0 + needs['absorption']['iron_inhibitors']['value']['tea']

    def scaled(k, lvl):
        e = nut[k][lvl]
        v = e['value']
        if v is None:
            return None
        v = num(v, ms)
        basis = e.get('basis_' + lvl, nut[k]['basis'])
        if basis == 'per_kg':
            v *= W
        elif basis == 'per_1000_kcal':
            v *= E / 1000.0
        elif basis == 'per_g_protein':
            v *= protein_target
        elif basis == 'absorbed':
            v /= fe_abs if k == 'iron' else 1.0
        return v

    target, minimum, ceiling = {}, {}, {}
    for k in nut:
        if k == 'protein':
            target[k], minimum[k] = protein_target, scaled(k, 'minimum')
            continue
        if k == 'iron':      # optimum is already dietary (absorbed need / 0.15); minimum is absorbed losses
            target[k] = num(nut[k]['optimum']['value'], ms)
            minimum[k] = num(nut[k]['minimum']['value'], ms) / fe_abs
        elif k == 'zinc':    # optimum is dietary; the absorbed minimum is checked after with Miller's equation
            target[k] = num(nut[k]['optimum']['value'], ms)
            minimum[k] = None
        else:
            t = scaled(k, 'optimum')
            target[k] = t if t is not None else num(nut[k]['recommended']['value'], ms)
            minimum[k] = scaled(k, 'minimum')
        c = nut[k]['ceiling']['value']
        if c is not None:
            ceiling[k] = num(c, ms) * (W if nut[k]['ceiling'].get('basis_ceiling') == 'per_kg' else 1.0)
    target['sodium'] += sweat_na
    minimum['sodium'] += sweat_na
    ceiling['sodium'] += sweat_na
    protein_ceiling = num(nut['protein']['ceiling']['value'], ms) * W
    protein_limit = num(nut['protein']['intake_limit']['value'], ms) * W
    floor = en['pal_limits']['value']['lowest'] * ree        # energy of basal function: the lowest daily expenditure
    keys = list(target)
    mkeys = [k for k in keys if minimum.get(k) is not None]
    n, m, mm = len(goods), len(keys), len(mkeys)
    # variables: x_g (n) | u_k for the minima and energy floor (mm + 1) | z (1) | v_k for the targets (m)
    iu, iz, iv = n, n + mm + 1, n + mm + 2
    nv = n + mm + 2 + m
    caps = []
    for g in goods:
        cap = case['available_g'][g]
        if comp[g]['fat'] > 0:
            cap = min(cap, 250.0 / comp[g]['fat'])                 # user: 250 g fat from one good (M93)
        if g == 'BONUS_DAIRY':
            cap = min(cap, 3000.0)                                   # user: about 3 L milk a day (M88)
        caps.append(cap)
    bounds = [(0, c) for c in caps] + [(0, 1)] * (mm + 1) + [(0, 1)] + [(0, 1)] * m
    A, b = [], []

    def row(**coef):
        r = [0.0] * nv
        for i, v in coef.items():
            r[int(i[1:])] = v
        return r

    def xrow(vals, extra=None):
        r = list(vals) + [0.0] * (nv - n)
        for i, v in (extra or {}).items():
            r[i] = v
        return r
    kcal = [comp[g]['kcal'] for g in goods]
    A.append(xrow(kcal)); b.append(E)                                 # energy eaten <= need (surplus stays in store)
    # protein is energy (excess is turned into glucose), up to what the liver can turn into urea in a day, spread over the
    # day's three meals (Bilsborough and Mann 2006: 285-365 g a day for 80 kg); beyond it no more protein can be used (M114)
    A.append(xrow([comp[g]['protein'] for g in goods])); b.append(protein_limit)
    fruit = [i for i, g in enumerate(goods) if g.split(':')[0] in FRUIT]
    if fruit:
        A.append(xrow([1.0 if i in fruit else 0.0 for i in range(n)])); b.append(4518.0)   # user: one watermelon (M86)
    # lactose limit (Wilt 2010) only for people neither lactase persistent nor of a dairy culture, and only on fresh
    # milk: fermented dairy with live cultures is digested in the gut (Kolars 1984); M113
    if not case.get('lactase_persistent', True) and not case.get('dairy_culture', False) and 'BONUS_DAIRY' in goods:
        lac = num(needs['gut_limits']['lactose_g']['value']['tolerated_by_intolerant'], ms)
        A.append(xrow([comp[g]['sugars'] if g == 'BONUS_DAIRY' else 0.0 for g in goods])); b.append(lac)
    # harms (nutrient ceilings, protein above 2.5 g/kg or 35 % of energy, fat sweating) are reported, never constraints (M101)
    for j, k in enumerate(mkeys):                                     # u_k * minimum_k <= intake_k
        A.append(xrow([-comp[g][k] for g in goods], {iu + j: minimum[k]})); b.append(0.0)
    A.append(xrow([-c for c in kcal], {iu + mm: floor})); b.append(0.0)  # u_E * floor <= energy eaten
    A.append(xrow([-c for c in kcal], {iz: E})); b.append(0.0)         # z * E <= energy eaten
    for j, k in enumerate(keys):                                      # v_k * target_k <= intake_k
        A.append(xrow([-comp[g][k] for g in goods], {iv + j: target[k]})); b.append(0.0)

    def lp(c, A_, b_):
        r = linprog(c, A_ub=A_, b_ub=b_, bounds=bounds, method='highs')
        if r.status != 0:
            raise SystemExit('LP failed: ' + r.message)
        return r
    # stage 1: basal function -- energy up to 1.2 x REE (M114)
    c1 = [0.0] * nv; c1[iu + mm] = -1.0
    uE = -lp(c1, A, b).fun
    A.append(list(c1)); b.append(-(uE - TOL))
    # stage 2: being fed -- energy for labour up to the need (M93: satiety being met is the baseline)
    c2 = [0.0] * nv; c2[iz] = -1.0
    z = -lp(c2, A, b).fun
    A.append(list(c2)); b.append(-(z - TOL))
    # stage 3: the nutrient minima, mean coverage (M114: the body's functions)
    c3m = [0.0] * nv
    for j in range(mm):
        c3m[iu + j] = -1.0 / mm
    Sm = -lp(c3m, A, b).fun
    A.append(list(c3m)); b.append(-(Sm - TOL))
    S = (Sm * mm + uE) / (mm + 1)
    # stage 4: nutrition, the mean adequacy ratio against the targets
    c3 = [0.0] * nv
    for j in range(m):
        c3[iv + j] = -1.0 / m
    mar = -lp(c3, A, b).fun
    A.append(list(c3)); b.append(-(mar - TOL))
    # stage 5: the better stocks first
    q = {g: quality(comp[g], target, E) for g in goods}
    c4 = [(1.0 - q[g]) * comp[g]['kcal'] for g in goods] + [0.0] * (nv - n)
    r4 = lp(c4, A, b)
    x = {g: float(r4.x[i]) for i, g in enumerate(goods)}
    K = float(sum(comp[g]['kcal'] * x[g] for g in goods))
    P = float(sum(comp[g]['protein'] * x[g] for g in goods))
    F = float(sum(comp[g]['fat'] * x[g] for g in goods))
    pal_reached = K / ree
    low = en['pal_limits']['value']['lowest']
    labour = max(0.0, min(1.0, (pal_reached - low) / (case['pal'] - low))) if case['pal'] > low else 1.0
    out = report(case, needs, comp, sat, goods, x, E, ree, pal, z, mar, q, target, minimum, ceiling, fe_abs, ms, W)
    meal = P / 3.0
    gut = nut['protein'].get('gut_absorption_g_per_h', {}).get('value', [1.3, 10.0])
    out['function'] = {'basal_energy_kcal': round(floor, 1), 'minima_coverage': round(S, 4),
                       'starving': bool(K < floor - TOL),
                       'deficient': [k for k in mkeys if sum(comp[g][k] * x[g] for g in goods) < minimum[k] - TOL],
                       'pal_reached': round(pal_reached, 3), 'labour_capacity': round(labour, 3)}
    out['harms'] = {'protein_g': round(P, 1), 'protein_per_meal_g': round(meal, 1),
                    'protein_meal_absorption_h': [round(meal / gut[1], 1), round(meal / gut[0], 1)],
                    'protein_above_urea_capacity': bool(P > protein_limit + TOL), 'urea_capacity_g': round(protein_limit, 1),
                    'protein_above_ceiling_g_per_kg': bool(P > protein_ceiling + TOL),
                    'protein_energy_share': round(4 * P / max(TOL, K), 3),
                    'fat_g': round(F, 1),
                    'fat_in_sweating_range': bool(F >= needs['gut_limits']['fat_g']['value']['sweating_from'][0])}
    out['goods_exhausted'] = [g for g in goods if x[g] >= case['available_g'][g] - 1e-3]
    return out


def miller_zinc(zinc_mg, phytate_mg, calcium_mg, protein_g, p):
    """Absorbed zinc (mg/d), Miller et al. 2013 eq. 2; inputs converted to mmol/d."""
    tdz, tdp, tdc = zinc_mg / 65.38, phytate_mg / 660.04, calcium_mg / 40.078
    zz = tdz * (1 + p['B_Pr'] * protein_g)
    xx = p['K_T'] * (1 + tdp * (1 - p['B_Ca'] * tdc) / p['K_P'])
    s = xx + p['A_MAX'] + zz
    return 0.5 * (s - (s * s - 4 * p['A_MAX'] * zz) ** 0.5) * 65.38


def hyperpalatable(c):
    kcal = c['kcal']
    if kcal <= 0:
        return False
    fat_e, sug_e, carb_e = c['fat'] * 9 / kcal, c['sugars'] * 4 / kcal, c['carbohydrate'] * 4 / kcal
    na_pct = c['sodium'] / 1000.0 * 100.0   # mg per g -> % by weight
    return (fat_e > 0.25 and na_pct >= 0.30) or (fat_e > 0.20 and sug_e > 0.20) or (carb_e > 0.40 and na_pct >= 0.20)


def report(case, needs, comp, sat, goods, x, E, ree, pal, z, mar, q, target, minimum, ceiling, fe_abs, ms, W):
    intake = {k: sum(comp[g][k] * x[g] for g in goods) for k in list(target) + ['kcal', 'water', 'fat', 'alcohol',
                                                                               'carbohydrate', 'sugars', 'fiber']}
    wt = needs['water']['turnover_ml']['value']
    water_turnover = (wt['pal'] * pal + wt['body_weight_kg'] * W + wt['sex_male'] * ms + wt['humidity_pct'] * case['humidity_pct']
                      + wt['athlete'] * case.get('athlete', 0) + wt['hdi_group'] * case['hdi_group']
                      + wt['altitude_m'] * case['altitude_m'] + wt['age_sq'] * case['age'] ** 2 + wt['age'] * case['age']
                      + wt['temp_sq'] * case['temp_c'] ** 2 + wt['temp_c'] * case['temp_c'] + wt['constant'])
    hi = needs['water']['hydration_index']['value']
    drink_hydration = sum(hi[DRINK_HI[g]] * x[g] for g in goods if g in DRINK_HI)    # 1 g of drink ~ 1 ml
    food_water = sum(comp[g]['water'] * x[g] for g in goods if g not in DRINK_HI)
    metabolic = needs['water']['metabolic_water_ml']['value']
    water_drawn = max(0.0, water_turnover - food_water - metabolic - drink_hydration)
    p = needs['absorption']['zinc_equation']['value']
    phy = needs['absorption']['phytate_mg_per_100g_dry']['value']
    phytate = sum(x[g] * (1 - comp[g]['water']) * (phy['unrefined_cereals_legumes'] if g.split(':')[0] in CEREALS else
                                                   phy['roots_tubers'] if g.split(':')[0] == 'BONUS_POTATO' else 0.0) / 100.0
                  for g in goods)
    zinc_abs = miller_zinc(intake['zinc'], phytate, intake['calcium'], intake['protein'], p)
    zmin = num(needs['nutrients']['zinc']['minimum']['value'], ms)
    alcohol_week = intake['alcohol'] * 7
    rows = []
    for k in target:
        rows.append({'nutrient': k, 'intake': round(intake[k], 3), 'target': round(target[k], 3),
                     'adequacy': round(min(1.0, intake[k] / target[k]), 3) if target[k] else None,
                     'minimum': None if minimum.get(k) is None else round(minimum[k], 3),
                     'below_minimum': bool(minimum.get(k) is not None and intake[k] < minimum[k] - TOL),
                     'ceiling': None if k not in ceiling else round(ceiling[k], 3),
                     'above_ceiling': bool(k in ceiling and intake[k] > ceiling[k] + TOL)})
    contrib = {k: {g: round(float(comp[g][k] * x[g]), 3) for g in goods if comp[g][k] * x[g] > 0} for k in target}
    satm = sat['map']
    sat_e = sum(sat['holt'][satm[g]] / 100.0 * comp[g]['kcal'] * x[g] for g in goods if g in satm)
    sat_cov = sum(comp[g]['kcal'] * x[g] for g in goods if g in satm)
    wellbeing = sorted(({'good': g, 'grams': round(x[g], 1), 'hyper_palatable': bool(hyperpalatable(comp[g])),
                         'kcal_per_g': round(comp[g]['kcal'], 2),
                         'satiety_index': sat['holt'][satm[g]] if g in satm else None}
                        for g in goods if x[g] > TOL), key=lambda r: (not r['hyper_palatable'], r['kcal_per_g']))
    return {
        'case': case.get('name'), 'ree_kcal': round(ree, 1), 'pal_used': pal, 'pal_asked': case['pal'],
        'energy_need_kcal': round(E, 1), 'energy_share_of_need': round(z, 4), 'mar': round(mar, 4),
        'eaten_g': {g: round(float(x[g]), 1) for g in goods}, 'left_in_store_g': {g: round(case['available_g'][g] - x[g], 1) for g in goods},
        'quality': {g: round(q[g], 3) for g in goods}, 'nutrients': rows, 'contributions': contrib,
        'zinc_absorbed_mg': round(zinc_abs, 2), 'zinc_absorbed_minimum_mg': round(zmin, 2),
        'iron_absorption_fraction': fe_abs,
        'water_ml': {'turnover': round(water_turnover), 'from_food': round(food_water), 'metabolic': metabolic,
                     'from_drinks': round(drink_hydration), 'water_to_draw': round(water_drawn)},
        'alcohol_g_per_week': round(alcohol_week, 1),
        'fullness_index_mean_where_measured': round(sat_e / sat_cov, 3) if sat_cov else None,
        'energy_share_with_measured_satiety': round(sat_cov / intake['kcal'], 3) if intake['kcal'] else None,
        'wellbeing_list': wellbeing,
    }


def main():
    args = sys.argv[1:]
    with open(args[0], encoding='utf-8') as fh:
        cases = json.load(fh)
    out = [solve(c) for c in cases['cases']]
    if '--json' in args:
        with open(args[args.index('--json') + 1], 'w', encoding='utf-8') as fh:
            json.dump(out, fh, indent=1, ensure_ascii=False)
            fh.write('\n')
    for r in out:
        f = r['function']
        print('==', r['case'], '| E need', r['energy_need_kcal'], '| minima', f['minima_coverage'], '| starving', f['starving'],
              '| deficient', f['deficient'] or 'none', '| labour', f['labour_capacity'], '(PAL', f['pal_reached'], ') | MAR', r['mar'])
        print('   eaten g:', r['eaten_g'])
        print('   above ceiling:', [n['nutrient'] for n in r['nutrients'] if n['above_ceiling']] or 'none')
        print('   harms:', r['harms'], '| exhausted:', r['goods_exhausted'])
        print('   water ml:', r['water_ml'], '| zinc absorbed', r['zinc_absorbed_mg'], '/ min', r['zinc_absorbed_minimum_mg'])


if __name__ == '__main__':
    main()
