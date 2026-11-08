"""R64.3 (M112): food consumption of a city population, from the nutrition record.

Reads research/economy/data/nutrient_needs.json (version 2), nutrient_profiles.json and satiety_index.json, and a case
file (city inputs and goods available per person per day). Solves, per person of the city (adult equivalent):

  stage 1 (basal):    energy of basal function, up to 1.2 x REE (the lowest daily expenditure; M114)
  stage 2 (fullness): maximise fullness / 3,000 (user U089): fullness = sum of satiety index / 100 x kcal, drinks x 0.8
  stage 3 (energy):   maximise z = energy eaten / energy need; labour capacity = (energy / REE - 1.2) / (PAL - 1.2)
  stage 4 (minima):   maximise the mean coverage of the nutrient minima; deficient = below a minimum (M114)
  stage 5 (adequacy): maximise the mean adequacy ratio MAR = mean_i min(1, intake_i / target_i)
  stage 6 (athletes): maximise the mean of min(1, intake_i / athletes' optimum_i) (M118; user U173-U189)
  stage 7 (quality):  minimise energy taken from lower-quality goods (people draw on the better stocks)
  stage 8 (dessert):  dessert goods left in store, beyond the need up to 1.0 x need, in the user's order (U091-U093)
each LP stage holds the optimum of the stages before it

subject to: availability per good, energy eaten <= need (stages 1-7), the user's ceilings (data/user_inputs.json, M120:
per good, fat 250 g per good, meat 1 kg in all, fruit one watermelon), and lactose only for pasteurised milk by the
culture's lactase-persistent share. Protein is energy like any other up to the liver's daily urea capacity, spread over
three meals; nutrient ceilings, the protein ceiling, fat and contaminants are harms, reported (M101, M114). Outputs also
give strength and IQ from the user's anchors. The specification is research/economy/food_model.md.

usage: food_model.py <case.json> [--json out.json] [--md report.md]
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
MEAT = {'BONUS_COW', 'BONUS_PIG', 'BONUS_SHEEP', 'BONUS_DEER', 'BONUS_HORSE'}
DRINK_HI = {'BONUS_DAIRY': 'milk_full_fat', 'BONUS_ALCOHOL': 'lager', 'BONUS_TEA': 'tea'}


SRC, DEFAULT, PARTS = {}, {}, {}      # composite recipes, default keys and part shares, filled by composition()


def composition(profiles, whole, user):
    """Per gram of each good and form. Keys: 'GOOD:form' (USDA), 'GOOD:mext:form' (MEXT), composites
    ('GOOD:whole', 'BONUS_FISH:region:<region>', 'BONUS_FISH:herring whole, <season>'), and 'GOOD' = the user's default form."""
    out, organs = {}, {}
    for g, forms in profiles['goods'].items():
        if not g.startswith('BONUS_'):
            continue
        for i, f in enumerate(forms):
            out[g + ':' + f['form']] = finish(g, {k: (f.get(k) or 0.0) for k in profiles['units']}, f, profiles, i == 0)
        for f in profiles['mext'].get(g, []):                        # MEXT forms (niacin equivalents as MEXT gives them)
            pg = finish(g, {k: (f.get(k) or 0.0) for k in profiles['units']}, dict(f, iodine=f.get('iodine') or 0.0), profiles, False)
            pg['niacin_ne'] = (f.get('niacin_ne') or 0.0) / 100.0
            out[g + ':mext:' + f['form']] = pg

    def mix(parts, organ_parts=(), name=None):
        tot = float(sum(parts.values()))
        if name:
            PARTS[name] = {p: w / tot for p, w in parts.items()}
            SRC[name] = ' + '.join('%s %.1f %%' % (p, 100 * w / tot) for p, w in parts.items())
        row = {k: sum(out[p][k] * w for p, w in parts.items()) / tot for k in out[next(iter(parts))]}
        return row, sum(w for p, w in parts.items() if p in organ_parts) / tot
    # cod as eaten (Torry shares; vitamin A of the liver from cod liver oil x the liver's fat)
    cod = whole['cod_as_eaten']['value']
    cp = {'BONUS_FISH:' + k: v for k, v in cod['parts_pct_of_round_weight'].items()}
    row, _ = mix(cp, name='BONUS_FISH:whole')
    SRC['BONUS_FISH:whole'] = 'cod as eaten (Torry shares): ' + SRC['BONUS_FISH:whole'] + '; liver vitamin A from cod liver oil; iodine MEXT cod'
    row['vit_a_rae'] += cod['liver_oil_vit_a_ug_per_100g'] / 100.0 * out['BONUS_FISH:liver (lingcod)']['fat'] * cp['BONUS_FISH:liver (lingcod)'] / sum(cp.values())
    row['iodine'] = out['BONUS_FISH:cod']['iodine'] if out['BONUS_FISH:cod']['iodine'] else profiles['mext']['BONUS_FISH'][0]['iodine'] / 100.0
    out['BONUS_FISH:whole'] = row
    # herring eaten whole: year-round fat (user U155) and the seasonal values (record)
    h = out['BONUS_FISH:herring']
    for label, fat in [('year-round', user['herring_year_round_fat'] * 100)] + list(whole['herring_whole_fat_pct']['value'].items()):
        r2 = dict(h)
        r2['fat'] = fat / 100.0
        r2['kcal'] = 4 * h['protein'] + 9 * fat / 100.0 + 4 * h['carbohydrate']
        out['BONUS_FISH:herring whole, ' + label] = r2
        SRC['BONUS_FISH:herring whole, ' + label] = 'herring (USDA %s) with whole-fish fat %.1f %% (%s), kcal by Atwater 4/9/4' % (
            [f for f in profiles['goods']['BONUS_FISH'] if f['form'] == 'herring'][0]['fdc_id'], fat,
            'user U155' if label == 'year-round' else 'record, Faroese herring')
    # fish catch by region (user U154): category -> record
    CAT = {'Freshwater fish': 'BONUS_FISH:mext:pond smelt, whole', 'Small pelagic': 'BONUS_FISH:herring whole, year-round',
           'Large pelagic': 'BONUS_FISH:tuna (bluefin)', 'Demersal': 'BONUS_FISH:whole', 'Salmonids': 'BONUS_FISH:salmon (Atlantic, wild)',
           'Other marine fish': 'BONUS_FISH:Atlantic mackerel'}
    for region, shares in user['fish_catch_by_region']['shares'].items():
        out['BONUS_FISH:region:' + region], _ = mix({CAT[c]: w for c, w in shares.items() if w > 0}, name='BONUS_FISH:region:' + region)
        SRC['BONUS_FISH:region:' + region] = 'catch of %s (user U154): ' % region + SRC['BONUS_FISH:region:' + region]
    # land animals and whale as eaten (user U112-U120; organs in the ratio of the cow's liver:heart:kidneys)
    org = whole['cow_as_eaten']['value']['parts_pct_of_live_weight']
    ratio = {'liver': org['liver'], 'heart': org['heart'], 'kidneys': org['kidneys']}
    rt = sum(ratio.values())
    NEAR = {'BONUS_COW': ('BONUS_COW:lean', 'BONUS_COW:fat (suet)', 'BONUS_COW'), 'BONUS_SHEEP': ('BONUS_SHEEP:lean', 'BONUS_COW:fat (suet)', 'BONUS_SHEEP'),
            'BONUS_DEER': ('BONUS_DEER:meat', 'BONUS_COW:fat (suet)', 'BONUS_SHEEP'), 'BONUS_HORSE': ('BONUS_HORSE:meat', 'BONUS_COW:fat (suet)', 'BONUS_COW')}
    for g, key in [('BONUS_COW', 'cow'), ('BONUS_SHEEP', 'sheep'), ('BONUS_DEER', 'deer'), ('BONUS_HORSE', 'horse')]:
        sh = user[key + '_shares']
        lean, fat, og = NEAR[g]
        parts = {lean: sh['lean'], fat: sh['fat']}
        for o, w in ratio.items():
            parts[og + ':' + o] = parts.get(og + ':' + o, 0) + sh['organs'] * w / rt
        out[g + ':whole'], organs[g + ':whole'] = mix(parts, [og + ':' + o for o in ratio], name=g + ':whole')
    sh = user['pig_shares']
    out['BONUS_PIG:whole'], organs['BONUS_PIG:whole'] = mix({'BONUS_PIG:lean': sh['lean'], 'BONUS_PIG:fat (backfat)': sh['fat'], 'BONUS_PIG:liver': sh['liver'],
                                                             'BONUS_PIG:heart': sh['heart'], 'BONUS_PIG:kidneys': sh['kidneys']},
                                                            ['BONUS_PIG:liver', 'BONUS_PIG:heart', 'BONUS_PIG:kidneys'], name='BONUS_PIG:whole')
    sh = user['whale_shares']
    out['BONUS_WHALE:whole'], organs['BONUS_WHALE:whole'] = mix({'BONUS_WHALE:meat': sh['meat'], 'BONUS_WHALE:blubber (bowhead)': sh['blubber'],
                                                                 'BONUS_WHALE:liver': sh['liver'] + sh['other_organs']}, ['BONUS_WHALE:liver'],
                                                                name='BONUS_WHALE:whole')
    SRC['BONUS_WHALE:whole'] += ' (other organs: liver record, the nearest held)'
    # the default form of each good (user U136-U153)
    for g in profiles['goods']:
        if not g.startswith('BONUS_'):
            continue
        f = user['default_form'].get(g, {}).get('form')
        key = g + ':' + f if f else g + ':' + profiles['goods'][g][0]['form']
        if f == 'polished' and key not in out:
            key = g + ':mext:polished'
        if key not in out:
            raise SystemExit('default form %s of %s has no composition record' % (f, g))
        out[g] = out[key]
        DEFAULT[g] = key
        if key in organs:
            organs[g] = organs[key]
    return out, organs


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


def solve(case, extra_kcal=0.0):
    needs, profiles, sat, user = load('nutrient_needs.json'), load('nutrient_profiles.json'), load('satiety_index.json'), load('user_inputs.json')
    ms, W = case['male_share'], case['body_weight_kg']
    comp, organs = composition(profiles, needs['whole_animal'], user)
    goods = [g for g in case['available_g'] if case['available_g'][g] > 0]
    for g in goods:
        if g not in comp:
            raise SystemExit('no composition record for ' + g)
    en = needs['energy']
    ree = en['ree_kcal']['value']['per_kg'] * W + en['ree_kcal']['value']['constant']
    pal_asked = user['pal_by_work'][case['work']] if 'work' in case else case['pal']
    pal = min(pal_asked, en['pal_limits']['value']['alimentary_ceiling'])
    E = pal * ree + extra_kcal                                       # caffeine raises expenditure (Dulloo 1989; M85)
    nut = needs['nutrients']
    protein_target = num(nut['protein']['optimum']['value'], ms) * W
    sweat_na = num(nut['sodium']['sweat_per_hot_shift']['value'], ms) * case.get('hot_shift_share', 0.0)
    animal = any(g.split(':')[0] in ANIMAL for g in goods)
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
    # athletes' and heavy labourers' optima (user U173-U189): adequacy may rise towards them (M118)
    ath = {}
    for k in target:
        a_ = user['athletes_optimum'].get(k)
        if a_:
            v = a_['value'] * (W / 140.0 if k == 'protein' else 1.0)    # protein given for a 140 kg wrestler
            ath[k] = max(v, target[k])
    protein_ceiling = num(nut['protein']['ceiling']['value'], ms) * W
    protein_limit = num(nut['protein']['intake_limit']['value'], ms) * W
    floor = en['pal_limits']['value']['lowest'] * ree        # energy of basal function: the lowest daily expenditure
    # satiety per good (user U001-U088): the default key takes the value of its chosen form, else of the good
    SI = user['satiety_index']

    def si(g):
        # the form's own index, else the good's (U001-U088); a composite without its own index: the energy-weighted
        # index of its parts (satiety is per 240 kcal, so parts weigh by the energy they bring)
        r = resolved(g, user)
        for k in (r, g):
            if SI.get(k) is not None:
                return SI[k]
        if r in PARTS:
            pk = {p: w * comp[p]['kcal'] for p, w in PARTS[r].items()}
            vals = {p: si(p) for p in pk}
            if all(v is not None for v in vals.values()):
                return sum(vals[p] * pk[p] for p in pk) / sum(pk.values())
        return SI.get(g.split(':')[0])
    dfac = user['drink_satiety_factor']['value']
    sat_per_g = {g: (si(g) or 0.0) / 100.0 * comp[g]['kcal'] * (dfac if is_drink(resolved(g, user)) else 1.0) for g in goods}
    fed = user['fed_fullness']['value']
    keys = list(target)
    akeys = list(ath)
    mkeys = [k for k in keys if minimum.get(k) is not None]
    n, m, mm, ma = len(goods), len(keys), len(mkeys), len(akeys)
    # variables: x_g (n) | u_k minima + basal energy (mm + 1) | zF fullness (1) | z energy (1) | v_k targets (m) | w_k athletes (ma)
    iu, iF, iz, iv, iw = n, n + mm + 1, n + mm + 2, n + mm + 3, n + mm + 3 + m
    nv = iw + ma
    ceil = user['ceilings_g']

    def cap_of(g, avail):
        r = resolved(g, user)
        base = g.split(':')[0]
        cap = avail
        if comp[g]['fat'] > 0:
            cap = min(cap, ceil['fat_per_good'] / comp[g]['fat'])    # user: 250 g fat from one good (M93, U125)
        if r in ceil and isinstance(ceil[r], float):
            cap = min(cap, ceil[r])                                   # the form's own ceiling (U121: lemon 30 g, juice 1 L)
        elif base in ceil and isinstance(ceil[base], float) and not (base == 'BONUS_LEMON' and 'juice' in r):
            cap = min(cap, ceil[base])                                # user's ceiling of the good (U127-U135)
        if r in ('BONUS_DAIRY:milk', 'BONUS_DAIRY:mext:milk'):
            cap = min(cap, ceil['milk'])                              # user: 3 L milk (U124)
        if r in ('BONUS_DAIRY:cheese', 'BONUS_DAIRY:mext:processed cheese'):
            cap = min(cap, ceil['cheese'])                            # user: 1 kg cheese (U123)
        return cap
    bounds = [(0, cap_of(g, case['available_g'][g])) for g in goods] + [(0, 1)] * (nv - n)
    A, b = [], []

    def xrow(vals, extra=None):
        r = list(vals) + [0.0] * (nv - n)
        for i, v in (extra or {}).items():
            r[i] = v
        return r
    kcal = [comp[g]['kcal'] for g in goods]
    A.append(xrow(kcal)); b.append(E)                                 # energy eaten <= need; dessert comes after (U092)
    A.append(xrow([comp[g]['protein'] for g in goods])); b.append(protein_limit)   # urea capacity, a daily rate (M114)
    meat = [1.0 if g.split(':')[0] in MEAT else 0.0 for g in goods]
    if any(meat):
        A.append(xrow(meat)); b.append(ceil['meat_total']['max'])       # all meat together (U122: maximum 1 kg)
    fruit = [1.0 if is_fruit(resolved(g, user)) else 0.0 for g in goods]
    if any(fruit):
        A.append(xrow(fruit)); b.append(ceil['fruit_total'])           # one watermelon (U126)
    milk_keys = [g for g in goods if resolved(g, user) in ('BONUS_DAIRY:milk', 'BONUS_DAIRY:mext:milk')]
    lactose_rule = 'none: raw milk is universally digestible (U163)'
    if case.get('milk_pasteurized', False) and milk_keys:
        # pasteurised milk (U163; M113: cultures, cheese and butter are not limited): persistent people drink up to the milk
        # ceiling, the others keep to 12-15 g lactose; the city mean is weighted by the culture's persistent share
        share = user['lactase_persistence']['shares'][case['culture']]
        lac = num(needs['gut_limits']['lactose_g']['value']['tolerated_by_intolerant'], ms)
        lim = share * ceil['milk'] + (1 - share) * lac / comp[milk_keys[0]]['sugars']
        A.append(xrow([1.0 if g in milk_keys else 0.0 for g in goods])); b.append(lim)
        lactose_rule = 'pasteurised milk at most %.0f g (persistent share %.2f x %.0f g + rest x %.1f g lactose)' % (lim, share, ceil['milk'], lac)
    for j, k in enumerate(mkeys):
        A.append(xrow([-comp[g][k] for g in goods], {iu + j: minimum[k]})); b.append(0.0)
    A.append(xrow([-c for c in kcal], {iu + mm: floor})); b.append(0.0)
    A.append(xrow([-sat_per_g[g] for g in goods], {iF: fed})); b.append(0.0)   # zF * fed fullness <= fullness eaten
    A.append(xrow([-c for c in kcal], {iz: E})); b.append(0.0)
    for j, k in enumerate(keys):
        A.append(xrow([-comp[g][k] for g in goods], {iv + j: target[k]})); b.append(0.0)
    for j, k in enumerate(akeys):
        A.append(xrow([-comp[g][k] for g in goods], {iw + j: ath[k]})); b.append(0.0)

    def lp(c):
        r = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        if r.status != 0:
            raise SystemExit('LP failed: ' + r.message)
        return r

    def stage(idx, weights=None):
        c = [0.0] * nv
        for j, i in enumerate(idx):
            c[i] = -(weights[j] if weights else 1.0 / len(idx))
        v = -lp(c).fun
        A.append(list(c)); b.append(-(v - TOL))
        return v
    uE = stage([iu + mm])                                             # 1 basal function (M114)
    zF = stage([iF])                                                  # 2 fullness: fed by satiety (M92, M93; U089)
    z = stage([iz])                                                   # 3 energy for labour
    Sm = stage([iu + j for j in range(mm)])                           # 4 nutrient minima (M114)
    S = (Sm * mm + uE) / (mm + 1)
    mar = stage([iv + j for j in range(m)])                           # 5 adequacy against the optima
    ab = stage([iw + j for j in range(ma)]) if ma else 0.0           # 6 towards athletes' optima (M118, U173-U189)
    q = {g: quality(comp[g], target, E) for g in goods}
    q_of = q.get
    r6 = lp([(1.0 - q[g]) * comp[g]['kcal'] for g in goods] + [0.0] * (nv - n))   # 7 the better stocks first
    x = {g: float(r6.x[i]) for i, g in enumerate(goods)}
    # 8 dessert (M88; U091-U093): beyond the need, up to the share of the need, in the user's order
    dess = [g for g in goods if g in user['dessert']['goods']]
    y = {g: 0.0 for g in goods}
    room = user['dessert']['energy_beyond_need_share'] * E
    for group in user['dessert']['order']:
        gl = [g for g in dess if (g in group.get('goods', []) or g.split(':')[0] in group.get('bases', [])) and g not in group.get('except', [])]
        for g in sorted(gl, key=lambda h: -q_of(h)):
            if room <= TOL or comp[g]['kcal'] <= 0:
                continue
            free = cap_of(g, case['available_g'][g]) - x[g]
            if is_fruit(resolved(g, user)):
                free = min(free, ceil['fruit_total'] - sum(x[h] + y[h] for h in goods if is_fruit(resolved(h, user))))
            if g.split(':')[0] in MEAT:
                free = min(free, ceil['meat_total']['max'] - sum(x[h] + y[h] for h in goods if h.split(':')[0] in MEAT))
            take = max(0.0, min(free, room / comp[g]['kcal']))
            y[g] += take
            room -= take * comp[g]['kcal']
    xt = {g: x[g] + y[g] for g in goods}
    K = float(sum(comp[g]['kcal'] * x[g] for g in goods))
    KT = float(sum(comp[g]['kcal'] * xt[g] for g in goods))
    P = float(sum(comp[g]['protein'] * xt[g] for g in goods))
    F = float(sum(comp[g]['fat'] * xt[g] for g in goods))
    pal_reached = min(K, E) / ree
    low = en['pal_limits']['value']['lowest']
    labour = max(0.0, min(1.0, (pal_reached - low) / (pal_asked - low))) if pal_asked > low else 1.0
    out = report(case, needs, comp, sat, goods, xt, E, ree, pal, z, mar, q, target, minimum, ceiling, fe_abs, ms, W)
    out['pal_asked'] = pal_asked
    for w_ in out['wellbeing_list']:
        w_['satiety_index'] = None if si(w_['good']) is None else round(si(w_['good']), 1)                        # the user's index (U001-U088)
    out['eaten_main_g'] = {g: round(x[g], 1) for g in goods}
    out['dessert_g'] = {g: round(y[g], 1) for g in goods if y[g] > 0.05}
    out['energy_main_kcal'] = round(K, 1)
    out['energy_total_kcal'] = round(KT, 1)
    out['fullness'] = {'value': round(sum(sat_per_g[g] * x[g] for g in goods), 1), 'fed_level': fed, 'coverage': round(zF, 4),
                       'goods_without_satiety_index': [g for g in goods if si(g) is None]}
    out['athletes_coverage'] = round(ab, 4)
    out['athletes_targets'] = {k: round(v, 1) for k, v in ath.items()}
    out['lactose_rule'] = lactose_rule
    out['caps_g'] = {g: round(bounds[i][1], 1) for i, g in enumerate(goods)}
    meal = P / 3.0
    gut = nut['protein'].get('gut_absorption_g_per_h', {}).get('value', [1.3, 10.0])
    out['function'] = {'basal_energy_kcal': round(floor, 1), 'minima_coverage': round(S, 4),
                       'starving': bool(K < floor - TOL),
                       'deficient': [k for k in mkeys if sum(comp[g][k] * xt[g] for g in goods) < minimum[k] * (1 - 1e-4)],
                       'pal_reached': round(pal_reached, 3), 'labour_capacity': round(labour, 3)}
    out['harms'] = {'protein_g': round(P, 1), 'protein_per_meal_g': round(meal, 1),
                    'protein_meal_absorption_h': [round(meal / gut[1], 1), round(meal / gut[0], 1)],
                    'protein_above_urea_capacity': bool(P > protein_limit * (1 + 1e-4)), 'urea_capacity_g': round(protein_limit, 1),
                    'protein_above_ceiling_g_per_kg': bool(P > protein_ceiling * (1 + 1e-4)),
                    'protein_energy_share': round(4 * P / max(TOL, KT), 3),
                    'fat_g': round(F, 1),
                    'fat_in_sweating_range': bool(F >= needs['gut_limits']['fat_g']['value']['sweating_from'][0])}
    out['goods_exhausted'] = [g for g in goods if xt[g] >= case['available_g'][g] - 1e-3]
    cafd = needs['caffeine_mg_per_100g']['value']
    out['caffeine_mg'] = round(sum(cafd.get(g, 0.0) / 100.0 * xt[g] for g in goods), 1)
    out['caffeine_extra_kcal'] = round(extra_kcal, 1)
    out['iron'] = {'absorption_fraction': round(fe_abs, 4), 'inhibitor': 'none applied (tea type and timing not relevant, M120)'}
    caf = needs['absorption']['calcium_fraction_by_good']['value']
    known = {g: xt[g] * comp[g]['calcium'] for g in goods if g in caf and xt[g] > TOL}
    out['calcium_absorbed'] = {'mg_from_goods_with_a_measured_fraction': round(sum(caf[g] * v for g, v in known.items()), 1),
                               'goods_measured': sorted(known),
                               'goods_without_measured_fraction': sorted(g for g in goods if g not in caf and xt[g] * comp[g]['calcium'] > 1)}
    b12m = num(needs['absorption']['b12_absorbed']['value']['per_meal_saturation_ug'], ms)
    out['b12_absorbed_ceiling_three_meals_ug'] = round(3 * b12m, 2)
    out['alcohol_with_fat'] = bool(any(comp[g]['alcohol'] > 0 and xt[g] > TOL for g in goods) and F > 0)
    eaten_kcal = {g: comp[g]['kcal'] * xt[g] for g in goods}
    big = max(eaten_kcal.values()) / KT if KT else 0.0
    out['wellbeing'] = {'goods_over_5pct_energy': sum(1 for v in eaten_kcal.values() if KT and v / KT >= 0.05),
                        'largest_good_energy_share': round(big, 3),
                        'nutrients_below_minimum': len(out['function']['deficient']),
                        'harm_flags': [nn['nutrient'] for nn in out['nutrients'] if nn['above_ceiling']]}
    # strength (user U105) and IQ from iodine (user U107): the user's anchors, interpolated in ln / log10
    import math
    sa = user['strength_anchors']
    pts = [(sa['protein_g_30pct'], 30.0), (sa['protein_per_kg_80pct'] * W, 80.0), (protein_limit, float(sa['cap_pct']))]
    out['strength_pct'] = round(interp_log(P, pts, math.log, cap=float(sa['cap_pct'])), 1)
    ia = user['iq_from_iodine_anchors']
    iod = sum(comp[g]['iodine'] * xt[g] for g in goods)
    ipts = [(15.0, float(ia['floor_iq']))] + [(float(u), float(q_)) for u, q_ in ia['points_ug_iq']]
    out['iq'] = round(interp_log(max(iod, 1e-9), ipts, math.log10, floor=float(ia['floor_iq']) if iod <= 5000 else 0.0), 1)
    out['iodine_ug'] = round(iod, 1)
    # contaminants (user U191-U196), per kg body weight
    ct = user['contaminants']
    fish_kg = sum(xt[g] for g in goods if g.split(':')[0] == 'BONUS_FISH') / 1000.0
    hg = [fish_kg * v * 1000.0 / W for v in ct['mercury_fish_mg_per_kg']]                  # ug per kg bw per day
    shell_kg = sum(xt[g] for g in goods if g.split(':')[0] in ('BONUS_CLAM', 'BONUS_CRAB', 'BONUS_SHRIMP')) / 1000.0
    offal_kg = sum(xt[g] * organs.get(g, 1.0 if any(o in g for o in (':liver', ':heart', ':kidneys')) else 0.0) for g in goods) / 1000.0
    cd = (shell_kg + offal_kg) * ct['cadmium_shellfish_offal_mg_per_kg'] * 1000.0 * 7 / W    # ug per kg bw per week
    rice_b = sum(xt[g] for g in goods if g in ('BONUS_RICE:brown',)) / 1000.0
    rice_p = sum(xt[g] for g in goods if g.split(':')[0] == 'BONUS_RICE' and g != 'BONUS_RICE:brown') / 1000.0
    asi = ct['arsenic_inorganic_mg_per_kg']
    ar = (rice_b * asi['rice brown'] + rice_p * asi['rice polished'] + shell_kg * asi['shellfish']) * 1000.0 * 7 / W
    out['contaminants'] = {'mercury_ug_per_kg_bw_day': [round(v, 3) for v in hg], 'mercury_tolerable': ct['mercury_tolerable_ug_per_kg_bw_day'],
                           'cadmium_ug_per_kg_bw_week': round(cd, 3), 'cadmium_tolerable': ct['cadmium_tolerable_ug_per_kg_bw_week'],
                           'arsenic_ug_per_kg_bw_week': round(ar, 3), 'arsenic_tolerable': ct['arsenic_inorganic_tolerable_ug_per_kg_bw_week']}
    # keeping: the user's spoilage classes (U168-U172) by the good's keep class in nutrition.json
    nutr = load('nutrition.json')
    CLS = {'grain_granary': 'roots and grains', 'grain_open': 'roots and grains', 'root': 'roots and grains', 'kept': 'cured, salted, fermented',
           'dried': 'dried', 'canned': 'canned', 'fresh': 'others'}
    sp = user['spoilage_per_year']
    out['keeping'] = {}
    for g in goods:
        kc = nutr['goods'].get(g.split(':')[0], {}).get('form')
        out['keeping'][g] = {'left_g_per_day': round(case['available_g'][g] - xt[g], 1), 'keep_class': kc,
                             'user_class': CLS.get(kc), 'spoilage_per_year_pct': round(100 * sp[CLS[kc]], 1) if kc in CLS else None}
    return out


def resolved(g, user):
    """The form a key stands for: a bare good is the user's default form (U136-U153)."""
    if ':' in g:
        return g
    f = user['default_form'].get(g, {}).get('form')
    return g + ':' + f if f else g


def is_drink(r):
    """Drinks for the satiety factor (U090): milk, beer, wine, tea, coffee, lemon juice."""
    base = r.split(':')[0]
    return (base in ('BONUS_ALCOHOL', 'BONUS_TEA', 'BONUS_COFFEE') and 'leaves' not in r and 'powder' not in r) or \
        r in ('BONUS_DAIRY:milk', 'BONUS_DAIRY:mext:milk', 'BONUS_WINE:wine', 'BONUS_WINE:mext:red wine', 'BONUS_LEMON:juice')


def is_fruit(r):
    """Fruit for the one-watermelon ceiling (U126): banana, lemon, apple, grapes and raisins; not juice or wine."""
    base = r.split(':')[0]
    if base == 'BONUS_WINE':
        return 'wine' not in r
    return base in FRUIT and 'juice' not in r


def interp_log(xv, pts, f, cap=None, floor=None):
    """Piecewise linear in f(x) through the anchor points; outside them the end segment continues, then cap and floor."""
    pts = sorted(pts)
    if xv <= pts[0][0]:
        (x0, y0), (x1, y1) = pts[0], pts[1]
    elif xv >= pts[-1][0]:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
    else:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            if x0 <= xv <= x1:
                break
    yv = y0 + (y1 - y0) * (f(xv) - f(x0)) / (f(x1) - f(x0)) if x1 != x0 else y0
    if xv >= pts[-1][0] and cap is not None:
        yv = min(yv, cap)
    if cap is not None:
        yv = min(yv, cap)
    if floor is not None:
        yv = max(yv, floor)
    return max(yv, 0.0)


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
                     'below_minimum': bool(minimum.get(k) is not None and intake[k] < minimum[k] * (1 - 1e-4)),   # LP tolerance
                     'ceiling': None if k not in ceiling else round(ceiling[k], 3),
                     'above_ceiling': bool(k in ceiling and intake[k] > ceiling[k] * (1 + 1e-4))})
    contrib = {k: {g: round(float(comp[g][k] * x[g]), 3) for g in goods if comp[g][k] * x[g] > 0} for k in target}
    wellbeing = sorted(({'good': g, 'grams': round(x[g], 1), 'hyper_palatable': bool(hyperpalatable(comp[g])),
                         'kcal_per_g': round(comp[g]['kcal'], 2), 'satiety_index': None}
                        for g in goods if x[g] > TOL), key=lambda r: (not r['hyper_palatable'], r['kcal_per_g']))
    return {
        'case': case.get('name'), 'ree_kcal': round(ree, 1), 'pal_used': pal,
        'energy_need_kcal': round(E, 1), 'energy_share_of_need': round(z, 4), 'mar': round(mar, 4),
        'eaten_g': {g: round(float(x[g]), 1) for g in goods}, 'left_in_store_g': {g: round(case['available_g'][g] - x[g], 1) for g in goods},
        'quality': {g: round(q[g], 3) for g in goods}, 'nutrients': rows, 'contributions': contrib,
        'zinc_absorbed_mg': round(zinc_abs, 2), 'zinc_absorbed_minimum_mg': round(zmin, 2),
        'iron_absorption_fraction': fe_abs,
        'water_ml': {'turnover': round(water_turnover), 'from_food': round(food_water), 'metabolic': metabolic,
                     'from_drinks': round(drink_hydration), 'water_to_draw': round(water_drawn)},
        'alcohol_g_per_week': round(alcohol_week, 1),
        'wellbeing_list': wellbeing,
    }


UNITS = {'protein': 'g', 'sodium': 'mg', 'potassium': 'mg', 'calcium': 'mg', 'magnesium': 'mg', 'iron': 'mg', 'zinc': 'mg',
         'iodine': 'µg', 'selenium': 'µg', 'vit_a_rae': 'µg RAE', 'thiamin': 'mg', 'riboflavin': 'mg', 'niacin_ne': 'mg NE',
         'vit_b6': 'mg', 'folate_dfe': 'µg DFE', 'b12': 'µg', 'vit_c': 'mg'}


def record_of(g, profiles):
    """Where a good's composition comes from, for the report."""
    pre = ''
    if g in DEFAULT:
        pre, g = 'default form %s: ' % DEFAULT[g], DEFAULT[g]
    if g in SRC:
        return pre + SRC[g]
    base, _, form = g.partition(':')
    if form.startswith('mext:'):
        f = [x for x in profiles['mext'][base] if x['form'] == form[5:]][0]
        return pre + 'MEXT %s (%s)' % (f['mext_no'], form[5:])
    forms = profiles['goods'][base]
    f = [x for x in forms if x['form'] == form][0] if form else forms[0]
    return pre + 'USDA %d (%s)' % (f['fdc_id'], f['usda'])


def markdown(cases, results, comp, profiles):
    """The case report, written from the tool's own output (R69): inputs first, then results."""
    L = ['# Food model: case report', '', 'Written by `plan/tools/food_model.py --md`; every number below comes from the run, nothing is typed by hand.', '']
    for c, r in zip(cases, results):
        L += ['## ' + c['name'], '', '### Inputs', '',
              '| Variable | Value |', '|---|---|',
              '| body weight | %s kg |' % c['body_weight_kg'], '| share of men | %s |' % c['male_share'], '| age | %s years |' % c['age'],
              '| work class | %s |' % c.get('work', '—'), '| activity level asked (PAL) | %s (%s) |' % (r['pal_asked'], 'user U157-U160' if 'work' in c else 'case'),
              '| air temperature | %s °C |' % c['temp_c'],
              '| relative humidity | %s %% |' % c['humidity_pct'], '| altitude | %s m |' % c['altitude_m'],
              '| development group (Yamada HDI) | %s |' % c['hdi_group'], '| share of days with a hot work shift | %s |' % c.get('hot_shift_share', 0),
              '| culture (lactase persistence, user U163) | %s |' % c.get('culture', '—'), '| milk pasteurised | %s |' % c.get('milk_pasteurized', False),
              '| lactose rule | %s |' % r['lactose_rule'], '',
              '| Good available | Composition record | g per person per day (cap from user ceilings) | kcal / protein g / fat g per 100 g |', '|---|---|---|---|']
        for g, a in c['available_g'].items():
            k = comp[g]
            L.append('| %s | %s | %s (cap %s) | %.0f / %.1f / %.1f |' % (g, record_of(g, profiles), a, r['caps_g'][g], 100 * k['kcal'], 100 * k['protein'], 100 * k['fat']))
        f = r['function']
        L += ['', '### Results', '',
              '| Measure | Value |', '|---|---|',
              '| resting expenditure | %s kcal |' % r['ree_kcal'],
              '| energy need (PAL x REE + caffeine) | %s kcal (caffeine %s mg, +%s kcal) |' % (r['energy_need_kcal'], r['caffeine_mg'], r['caffeine_extra_kcal']),
              '| energy of basal function (1.2 x REE) | %s kcal |' % f['basal_energy_kcal'],
              '| starving | %s |' % ('yes' if f['starving'] else 'no'),
              '| fullness eaten / fed level (user U089, U090) | %s / %s (coverage %s); no satiety index: %s |' % (
                  r['fullness']['value'], r['fullness']['fed_level'], r['fullness']['coverage'], ', '.join(r['fullness']['goods_without_satiety_index']) or 'none'),
              '| energy eaten: main / with dessert | %s / %s kcal |' % (r['energy_main_kcal'], r['energy_total_kcal']),
              '| labour capacity (PAL reached) | %s (%s) |' % (f['labour_capacity'], f['pal_reached']),
              '| nutrient minima covered (mean) | %s |' % f['minima_coverage'],
              '| deficient (below minimum) | %s |' % (', '.join(f['deficient']) or 'none'),
              '| mean adequacy ratio | %s |' % r['mar'],
              '| coverage of athletes\' optima (user U173-U189) | %s |' % r['athletes_coverage'],
              '| strength (user U105 anchors) | %s %% |' % r['strength_pct'],
              '| iodine / IQ (user U107 anchors) | %s µg / %s |' % (r['iodine_ug'], r['iq']),
              '| mercury (fish, low-high) / tolerable | %s / %s µg per kg bw a day |' % (r['contaminants']['mercury_ug_per_kg_bw_day'], r['contaminants']['mercury_tolerable']),
              '| cadmium (shellfish, offal) / tolerable | %s / %s µg per kg bw a week |' % (r['contaminants']['cadmium_ug_per_kg_bw_week'], r['contaminants']['cadmium_tolerable']),
              '| inorganic arsenic (rice, shellfish) / tolerable | %s / %s µg per kg bw a week |' % (r['contaminants']['arsenic_ug_per_kg_bw_week'], r['contaminants']['arsenic_tolerable']),
              '| iron absorbed fraction | %s (%s) |' % (r['iron']['absorption_fraction'], r['iron']['inhibitor']),
              '| calcium absorbed, goods with a measured fraction | %s mg (%s); no measured fraction: %s |' % (
                  r['calcium_absorbed']['mg_from_goods_with_a_measured_fraction'], ', '.join(r['calcium_absorbed']['goods_measured']) or 'none',
                  ', '.join(r['calcium_absorbed']['goods_without_measured_fraction']) or 'none'),
              '| zinc absorbed (Miller) / minimum | %s / %s mg |' % (r['zinc_absorbed_mg'], r['zinc_absorbed_minimum_mg']),
              '| B12 absorbed at most (3 meals x per-meal saturation) | %s µg |' % r['b12_absorbed_ceiling_three_meals_ug'],
              '| protein, per meal, absorption hours at 10 and 1.3 g/h | %s g, %s g, %s h |' % (r['harms']['protein_g'], r['harms']['protein_per_meal_g'], r['harms']['protein_meal_absorption_h']),
              '| urea capacity | %s g |' % r['harms']['urea_capacity_g'],
              '| fat | %s g (sweating range: %s) |' % (r['harms']['fat_g'], r['harms']['fat_in_sweating_range']),
              '| alcohol | %s g a week (with fat: %s) |' % (r['alcohol_g_per_week'], r['alcohol_with_fat']),
              '| water: turnover / from food / metabolic / from drinks / to draw | %s / %s / %s / %s / %s ml |' % tuple(r['water_ml'][k] for k in ['turnover', 'from_food', 'metabolic', 'from_drinks', 'water_to_draw']),
              '| repetition: goods over 5 %% of energy / largest share | %s / %s |' % (r['wellbeing']['goods_over_5pct_energy'], r['wellbeing']['largest_good_energy_share']),
              '', '| Good | Eaten g (main + dessert) | Left g | Quality | Keep class -> user class (spoilage % a year, user U168-U172) |', '|---|---|---|---|---|']
        for g in c['available_g']:
            kp = r['keeping'][g]
            L.append('| %s | %s (%s + %s) | %s | %s | %s -> %s (%s) |' % (g, r['eaten_g'][g], r['eaten_main_g'][g], r['dessert_g'].get(g, 0), kp['left_g_per_day'],
                                                                   r['quality'][g], kp['keep_class'], kp['user_class'], kp['spoilage_per_year_pct']))
        L += ['', '| Nutrient | Intake | Target | Athletes | Minimum | Ceiling | Where it comes from (share of intake) |', '|---|---|---|---|---|---|---|']
        for n in r['nutrients']:
            cc = r['contributions'][n['nutrient']]
            tot = sum(cc.values()) or 1.0
            src = ', '.join('%s %d %%' % (g, round(100 * v / tot)) for g, v in sorted(cc.items(), key=lambda t: -t[1]) if v / tot >= 0.05)
            L.append('| %s (%s) | %s%s | %s | %s | %s | %s%s | %s |' % (n['nutrient'], UNITS[n['nutrient']], n['intake'], ' **below minimum**' if n['below_minimum'] else '',
                                                           n['target'], r['athletes_targets'].get(n['nutrient'], '—'), '—' if n['minimum'] is None else n['minimum'],
                                                           '—' if n['ceiling'] is None else n['ceiling'], ' **above**' if n['above_ceiling'] else '', src or '—'))
        L += ['', '| Well-being list (separate from nutrition) | g | hyper-palatable | kcal per g | satiety index |', '|---|---|---|---|---|']
        for w in r['wellbeing_list']:
            L.append('| %s | %s | %s | %s | %s |' % (w['good'], w['grams'], w['hyper_palatable'], w['kcal_per_g'], w['satiety_index'] if w['satiety_index'] is not None else 'not measured'))
        L.append('')
    return '\n'.join(L) + '\n'


def run(case):
    """Solve; caffeine raises expenditure, so iterate until the caffeine eaten and the energy need agree."""
    extra, r = 0.0, None
    for _ in range(10):
        r = solve(case, extra)
        new = 150.0 * min(r['caffeine_mg'], 600.0) / 600.0           # Dulloo 1989: +150 kcal at 600 mg
        if abs(new - extra) < 0.5:
            break
        extra = new
    return r


def main():
    args = sys.argv[1:]
    with open(args[0], encoding='utf-8') as fh:
        cases = json.load(fh)
    out = [run(c) for c in cases['cases']]
    if '--md' in args:
        prof = load('nutrient_profiles.json')
        comp, _ = composition(prof, load('nutrient_needs.json')['whole_animal'], load('user_inputs.json'))
        with open(args[args.index('--md') + 1], 'w', encoding='utf-8') as fh:
            fh.write(markdown(cases['cases'], out, comp, prof))
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
