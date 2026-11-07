"""R64.3 (M112): food consumption of a city population, from the nutrition record.

Reads research/economy/data/nutrient_needs.json (version 2), nutrient_profiles.json and satiety_index.json, and a case
file (city inputs and goods available per person per day). Solves, per person of the city (adult equivalent):

  stage 1 (fed):      maximise z = energy eaten / energy need, z <= 1
  stage 2 (adequacy): maximise the mean adequacy ratio MAR = mean_i min(1, intake_i / target_i), z held at stage 1
  stage 3 (quality):  minimise energy taken from lower-quality goods, z and MAR held (people draw on the better stocks)

subject to: availability per good, ceilings per nutrient, the protein ceiling, the fat limit and the user's ceilings
per good (milk 3 L, fat 250 g per good, fruit at most one watermelon). The specification is
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
COD_PARTS = {'cod': 36, 'liver (lingcod)': 5, 'roe': 4}         # Torry Advisory Note 17, % of whole ungutted cod
COD_LIVER_OIL_VIT_A = 30000.0                                   # ug RAE per 100 g, USDA 173577 (record 2d)


def composition(profiles):
    """Per good: nutrients per gram, from the first (as-eaten) form; the whole cod for BONUS_FISH."""
    out = {}
    for g, forms in profiles['goods'].items():
        if not g.startswith('BONUS_'):
            continue
        if g == 'BONUS_FISH':
            parts = {f['form']: f for f in forms}
            tot = float(sum(COD_PARTS.values()))
            row = {}
            for k in profiles['units']:
                row[k] = sum((parts[p].get(k) or 0.0) * w for p, w in COD_PARTS.items()) / tot
            liver = parts['liver (lingcod)']
            row['vit_a_rae'] += COD_LIVER_OIL_VIT_A * liver['fat'] / 100.0 * COD_PARTS['liver (lingcod)'] / tot
            base = {k: v for k, v in row.items()}
        else:
            base = {k: (forms[0].get(k) or 0.0) for k in profiles['units']}
        if forms[0].get('iodine') is None and profiles['mext'].get(g):   # SR Legacy holds no iodine: MEXT (record 2d)
            iod = profiles['mext'][g][0].get('iodine')
            base['iodine'] = iod if iod is not None else 0.0
        per_g = {k: v / 100.0 for k, v in base.items()}
        niacin = per_g['niacin'] * (1 / 3.0 if g in CEREALS else 1.0)
        per_g['niacin_ne'] = niacin + per_g['tryptophan'] * 1000.0 / 60.0
        out[g] = per_g
    return out


def quality(c, target, E):
    """MAR of a diet of this good alone at the energy need (ceilings ignored): the good's nutritional quality."""
    if c['kcal'] <= 0:
        return 0.0
    grams = E / c['kcal']
    return sum(min(1.0, c[i] * grams / t) for i, t in target.items()) / len(target)


def solve(case):
    needs, profiles, sat = load('nutrient_needs.json'), load('nutrient_profiles.json'), load('satiety_index.json')
    ms, W = case['male_share'], case['body_weight_kg']
    comp = composition(profiles)
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
    animal = any(g in ANIMAL for g in goods)
    fe_abs = num(needs['absorption']['iron_fraction']['value']['mixed_diet' if animal else 'vegetarian'], ms)

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
    keys = list(target)
    n, m = len(goods), len(keys)
    # variables: x_g (n), z (1), v_i (m)
    avail = [case['available_g'][g] for g in goods]
    caps = []
    for g in goods:
        cap = avail[goods.index(g)]
        if comp[g]['fat'] > 0:
            cap = min(cap, 250.0 / comp[g]['fat'])                 # user: 250 g fat from one good (M93)
        if g == 'BONUS_DAIRY':
            cap = min(cap, 3000.0)                                   # user: about 3 L milk a day (M88)
        caps.append(cap)
    bounds = [(0, c) for c in caps] + [(0, 1)] + [(0, 1)] * m
    A, b = [], []

    def row(coef_x, coef_z=0.0, coef_v=None):
        r = list(coef_x) + [coef_z] + (coef_v or [0.0] * m)
        return r
    A.append(row([comp[g]['kcal'] for g in goods]))                  # energy eaten <= E (surplus stays in store)
    b.append(E)
    A.append(row([-comp[g]['kcal'] for g in goods], E))              # z * E <= energy eaten
    b.append(0.0)
    A.append(row([comp[g]['protein'] for g in goods]))               # liver's urea capacity (Bilsborough and Mann)
    b.append(protein_limit)
    fruit = [i for i, g in enumerate(goods) if g in FRUIT]
    if fruit:
        A.append(row([1.0 if i in fruit else 0.0 for i in range(n)]))  # user: fruit at most one watermelon (M86)
        b.append(4518.0)
    if not case.get('lactase_persistent', True) and 'BONUS_DAIRY' in goods:
        lac = num(needs['gut_limits']['lactose_g']['value']['tolerated_by_intolerant'], ms)
        A.append(row([comp[g]['sugars'] if g == 'BONUS_DAIRY' else 0.0 for g in goods]))
        b.append(lac)
    # nutrient ceilings, the protein ceiling and the fat sweating onset are harms: reported, not constraints (M101)
    for j, k in enumerate(keys):                                      # v_k * target_k <= intake_k
        v = [0.0] * m
        v[j] = target[k]
        A.append(row([-comp[g][k] for g in goods], 0.0, v))
        b.append(0.0)
    nv = n + 1 + m
    c1 = [0.0] * nv
    c1[n] = -1.0
    r1 = linprog(c1, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    if r1.status != 0:
        raise SystemExit('stage 1 failed: ' + r1.message)
    z = r1.x[n]
    A2, b2 = A + [[-1.0 if i == n else 0.0 for i in range(nv)]], b + [-(z - TOL)]
    c2 = [0.0] * nv
    for j in range(m):
        c2[n + 1 + j] = -1.0 / m
    r2 = linprog(c2, A_ub=A2, b_ub=b2, bounds=bounds, method='highs')
    mar = -r2.fun
    q = {g: quality(comp[g], target, E) for g in goods}
    A3 = A2 + [[0.0] * (n + 1) + [-1.0 / m] * m]
    b3 = b2 + [-(mar - TOL)]
    c3 = [(1.0 - q[g]) * comp[g]['kcal'] for g in goods] + [0.0] * (1 + m)
    r3 = linprog(c3, A_ub=A3, b_ub=b3, bounds=bounds, method='highs')
    x = {g: r3.x[i] for i, g in enumerate(goods)}
    P = float(sum(comp[g]['protein'] * x[g] for g in goods))
    K = float(sum(comp[g]['kcal'] * x[g] for g in goods))
    F = float(sum(comp[g]['fat'] * x[g] for g in goods))
    harms = {'protein_g': round(P, 1), 'protein_limit_g': round(protein_limit, 1),
             'protein_above_ceiling_g_per_kg': bool(P > protein_ceiling + TOL),
             'protein_energy_share': round(4 * P / max(TOL, K), 3),
             'protein_energy_share_harm': bool(4 * P / max(TOL, K) > nut['protein']['ceiling']['energy_share_harm']),
             'fat_g': round(F, 1),
             'fat_in_sweating_range': bool(F >= needs['gut_limits']['fat_g']['value']['sweating_from'][0])}
    out = report(case, needs, comp, sat, goods, x, E, ree, pal, z, mar, q, target, minimum, ceiling, fe_abs, ms, W)
    out['harms'] = harms
    out['binding_limits'] = {'protein_at_urea_capacity': bool(harms['protein_g'] >= protein_limit - 1e-3),
                             'goods_exhausted': [g for g in goods if x[g] >= case['available_g'][g] - 1e-3]}
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
    phytate = sum(x[g] * (1 - comp[g]['water']) * (phy['unrefined_cereals_legumes'] if g in CEREALS else
                                                   phy['roots_tubers'] if g == 'BONUS_POTATO' else 0.0) / 100.0
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
    satm = sat['map']
    sat_e = sum(sat['holt'][satm[g]] / 100.0 * comp[g]['kcal'] * x[g] for g in goods if g in satm)
    sat_cov = sum(comp[g]['kcal'] * x[g] for g in goods if g in satm)
    wellbeing = sorted(({'good': g, 'grams': round(x[g], 1), 'hyper_palatable': bool(hyperpalatable(comp[g])),
                         'kcal_per_g': round(comp[g]['kcal'], 2),
                         'satiety_index': sat['holt'][satm[g]] if g in satm else None}
                        for g in goods if x[g] > TOL), key=lambda r: (not r['hyper_palatable'], r['kcal_per_g']))
    return {
        'case': case.get('name'), 'ree_kcal': round(ree, 1), 'pal_used': pal, 'pal_asked': case['pal'],
        'energy_need_kcal': round(E, 1), 'fed_z': round(z, 4), 'mar': round(mar, 4),
        'eaten_g': {g: round(float(x[g]), 1) for g in goods}, 'left_in_store_g': {g: round(case['available_g'][g] - x[g], 1) for g in goods},
        'quality': {g: round(q[g], 3) for g in goods}, 'nutrients': rows,
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
        print('==', r['case'], '| E', r['energy_need_kcal'], 'kcal | fed', r['fed_z'], '| MAR', r['mar'])
        print('   eaten g:', r['eaten_g'])
        print('   below minimum:', [n['nutrient'] for n in r['nutrients'] if n['below_minimum']] or 'none',
              '| above ceiling:', [n['nutrient'] for n in r['nutrients'] if n['above_ceiling']] or 'none')
        print('   harms:', r['harms'], '| binding:', r['binding_limits'])
        print('   water ml:', r['water_ml'], '| zinc absorbed', r['zinc_absorbed_mg'], '/ min', r['zinc_absorbed_minimum_mg'])


if __name__ == '__main__':
    main()
