"""R44 (M91): the food model on the game's goods, one city-year at a time (third version).

  stocks (tonnes)  ->  grams per head a day  ->  what is eaten: one allocation with diminishing returns over three
  motives (satiety, nutrition, well-being), within the body's ceilings  ->  energy, nutrients, water  ->  x, coverage,
  hydration, activity, work  ->  tonnes used, left, spoiled.

Data, read from files: nutrition.json (energy, protein, fat, edible share, keeping form, hydration index),
nutrient_profiles.json (USDA SR Legacy and MEXT: nutrients, water), nutrient_needs.json (EFSA 2017; Japanese DRI 2025
for sodium), satiety_fit.json (Holt 1995 fit, satiety_fit.py). Literature values are named where they are set;
estimates are marked ESTIMATE.
usage: food_model.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data')
NUT = json.load(open(os.path.join(DATA, 'nutrition.json'), encoding='utf-8'))
PROF = json.load(open(os.path.join(DATA, 'nutrient_profiles.json'), encoding='utf-8'))
NEED = json.load(open(os.path.join(DATA, 'nutrient_needs.json'), encoding='utf-8'))
SFIT = json.load(open(os.path.join(DATA, 'satiety_fit.json'), encoding='utf-8'))

# ---- need (FAO/WHO/UNU 2004; EFSA weights; Dulloo 1989) ----
BMR = ((15.057 * 68.1 + 692.2) + (14.818 * 58.5 + 486.6)) / 2
PAL = {'vigorous': 2.25, 'active': 1.76, 'sedentary': 1.53}
PAL_MIN, PAL_MAX = 1.40, 2.40
CAFFEINE_KCAL_MAX, CAFFEINE_MG_MAX = 150, 600
BREW = {'BONUS_TEA': (43.0, 200.0), 'BONUS_COFFEE': (15.0, 600.0)}   # MEXT: litres per kg, mg caffeine per litre
WATER_NEED_ML = 2250       # EFSA 2010 adequate intake of total water: men 2.5 L, women 2.0 L (water from food included)

# ---- the body's ceilings ----
PROTEIN_MAX_SHARE = 0.35   # Bilsborough and Mann 2006
FAT_PER_GOOD_G = 250       # M93 (was 100, M88): heuristic for the usual maximum of one good
MILK_MAX_G = 3000          # the user (M86, M88, M91): milk's own ceiling, one part of a person's water
FRUIT_MAX_G = 4518         # one whole watermelon (USDA SR Legacy portion), all fruit together (M86)
SALT_MAX_G = 10            # ESTIMATE
LEMON_MAX_G = 116          # ESTIMATE (M92: no one eats kilograms of lemons): two lemons a day (USDA NLEA serving 58 g)
# fullness (M92): people eat until they feel full, counted in satiety units (white-bread kcal). The capacity is the
# energy ceiling at the mean satiety of Holt's 38 foods (136): a person eating average foods is full at PAL 2.40.
HOLT_MEAN = 1.36           # mean of the 38 SI values in Holt et al. 1995 (as reproduced on Wikipedia)
SAT_EXP = 1.0              # fullness per kcal = satiety ** SAT_EXP (1.0 = Holt's index as measured; option B uses 0.5)

# ---- servings: the step of diminishing returns (USDA SR Legacy household portions) ----
SERVING_G = {'BONUS_WHEAT': 64, 'BONUS_RICE': 158, 'BONUS_CORN': 234, 'BONUS_POTATO': 300, 'BONUS_COW': 85,
             'BONUS_PIG': 113, 'BONUS_SHEEP': 85, 'BONUS_DEER': 85, 'BONUS_HORSE': 85, 'BONUS_FISH': 85,
             'BONUS_CLAM': 85, 'BONUS_CRAB': 85, 'BONUS_SHRIMP': 85, 'BONUS_WHALE': 85, 'BONUS_DAIRY': 244,
             'BONUS_BANANA': 126, 'BONUS_LEMON': 58, 'BONUS_APPLE': 242, 'BONUS_OLIVES': 42, 'BONUS_SUGAR': 4.2,
             'BONUS_WINE': 147, 'BONUS_ALCOHOL': 356, 'BONUS_SALT': 5}
# wheat 2 slices of bread; rice 1 cup cooked; maize 1 cup porridge; potato 1 large; meat and fish 3 oz; milk 1 cup;
# banana, lemon, apple NLEA serving; olives 5 tbsp (ESTIMATE); sugar 1 tsp; wine 5 fl oz; beer 1 can

PROFILE_FORM = {
    'BONUS_WHEAT': 'grain', 'BONUS_RICE': 'brown', 'BONUS_CORN': 'grain', 'BONUS_POTATO': 'boiled',
    'BONUS_COW': 'meat', 'BONUS_PIG': 'meat', 'BONUS_SHEEP': 'meat', 'BONUS_DEER': 'meat', 'BONUS_HORSE': 'meat',
    'BONUS_FISH': 'cod', 'BONUS_CLAM': 'raw', 'BONUS_CRAB': 'raw', 'BONUS_SHRIMP': 'raw', 'BONUS_WHALE': 'meat',
    'BONUS_DAIRY': 'milk', 'BONUS_BANANA': 'raw', 'BONUS_LEMON': 'raw', 'BONUS_APPLE': 'raw', 'BONUS_OLIVES': 'olives',
    'BONUS_SUGAR': 'brown', 'BONUS_WINE': 'wine', 'BONUS_ALCOHOL': 'beer', 'BONUS_TEA': 'green, brewed',
    'BONUS_SALT': 'table salt',
}
MEXT_FORM = {'BONUS_WHEAT': 'soft flour', 'BONUS_RICE': 'polished', 'BONUS_CORN': 'grain', 'BONUS_POTATO': 'raw',
             'BONUS_COW': 'shoulder', 'BONUS_PIG': 'loin', 'BONUS_FISH': 'cod', 'BONUS_CLAM': 'asari clam',
             'BONUS_WHALE': 'red meat', 'BONUS_DAIRY': 'milk', 'BONUS_LEMON': 'whole fruit', 'BONUS_APPLE': 'with skin',
             'BONUS_BANANA': 'raw', 'BONUS_WINE': 'red wine', 'BONUS_TEA': 'sencha infusion', 'BONUS_SALT': 'salt',
             'BONUS_SUGAR': 'white sugar'}
DRINKS = {'BONUS_DAIRY', 'BONUS_WINE', 'BONUS_ALCOHOL', 'BONUS_TEA', 'BONUS_COFFEE'}
FRUIT = {'BONUS_BANANA', 'BONUS_LEMON', 'BONUS_APPLE'}
ANIMAL = set(NUT['animal_goods'])
NUTRIENTS = ['vit_c', 'vit_a_rae', 'thiamin', 'niacin', 'folate_dfe', 'b12', 'iron', 'zinc', 'calcium', 'iodine',
             'potassium', 'sodium']
SPOIL = {k: v['value'] for k, v in NUT['spoilage_per_year_percent'].items()}

# ---- the Fish good as the whole animal eaten (M91): a catch of fatty and lean fish, with liver ----
# shares are ESTIMATES to source (catch composition; cod liver about 5 % of body weight). Composition USDA SR Legacy:
# herring, Pacific, raw (173669); cod, Atlantic, raw (171955); lingcod liver (169810, 42 g fat), its vitamin A scaled
# from cod liver oil (173577: 30,000 ug RAE per 100 g) by the liver's fat share.
WHOLE_FISH = {'herring': (0.50, dict(kcal=195, protein=16.39, fat=13.88, vit_a_rae=32)),
              'cod flesh': (0.45, dict(kcal=82, protein=17.81, fat=0.67, vit_a_rae=12)),
              'liver': (0.05, dict(kcal=424, protein=5.6, fat=42.0, vit_a_rae=30000 * 0.42))}
WF = {k: sum(s * c.get(k, 0) for s, c in WHOLE_FISH.values()) for k in ('kcal', 'protein', 'fat', 'vit_a_rae')}


def good(g):
    """energy, protein, fat per 100 g as stored, eaten share; the Fish good as the whole animal"""
    v = dict(NUT['goods'][g])
    if g == 'BONUS_FISH':
        v.update(kcal=WF['kcal'], protein=WF['protein'], fat=WF['fat'], edible=0.85)   # ESTIMATE: 15 % bones, fins
    return v


def micro(g):
    f = PROFILE_FORM.get(g)
    if not f:
        return None
    u = next(x for x in PROF['goods'][g] if x['form'] == f)
    r = {k: (u.get(k) or 0.0) for k in NUTRIENTS + ['kcal', 'water']}
    m = next((x for x in PROF.get('mext', {}).get(g, []) if x['form'] == MEXT_FORM.get(g)), None)
    r['iodine'] = (m['iodine'] or 0.0) if m else 0.0
    if g == 'BONUS_TEA' and m:
        r['vit_c'] = m['vit_c'] or 0.0
    if g == 'BONUS_FISH':
        r['vit_a_rae'] = WF['vit_a_rae']
    return r


# ---- the three motives, per kcal ----
SUGARS = {'BONUS_WHEAT': 4.34, 'BONUS_DAIRY': 5.05, 'BONUS_BANANA': 12.23, 'BONUS_LEMON': 2.5, 'BONUS_APPLE': 10.39,
          'BONUS_SUGAR': 99.8, 'BONUS_WINE': 0.62, 'BONUS_POTATO': 0.89, 'BONUS_CORN': 0.27, 'BONUS_RICE': 0.05}
ALCOHOL_G = {'BONUS_WINE': 10.6, 'BONUS_ALCOHOL': 3.9}            # USDA SR Legacy, g per 100 g (sugars likewise)
LIQUID_SATIETY = 0.5        # ESTIMATE: liquid energy satiates less (Almiron-Roig et al. 2003, PMID 14649371)
HOLT = {'BONUS_POTATO': 323, 'BONUS_COW': 176, 'BONUS_RICE': 138, 'BONUS_APPLE': 197, 'BONUS_BANANA': 118,
        'BONUS_WHEAT': 157, 'BONUS_LEMON': 202}     # wheat as wholemeal bread; lemon as Holt's oranges


def satiety(g):
    """Holt where measured (white bread = 1.00), the fitted formula otherwise; drinks reduced"""
    s = HOLT.get(g, SFIT['goods'].get(g, 100)) / 100.0
    return s * (LIQUID_SATIETY if g in DRINKS else 1.0)


def nutrition(g):
    """nutrient density per 100 kcal, as the Nutrient Rich Foods index: shares of daily need capped at 1, averaged"""
    v, m = good(g), micro(g)
    if not v['kcal']:
        return 0.0
    sh = [min(1.0, v['protein'] * 100.0 / v['kcal'] / NEED['needs']['protein']['value'])]
    if m is not None and m['kcal']:
        sh += [min(1.0, m[k] * 100.0 / m['kcal'] / NEED['needs'][k]['value']) for k in NUTRIENTS]
    return sum(sh) / len(sh)


def wellbeing(g):
    """well-being per kcal (ESTIMATE weights on sourced effects):
       reward    sugar's share of energy; fat together with carbohydrate (supra-additive reward, DiFeliceantonio et al.
                 2018, PMID 29909968; a fat-sugar milkshake released striatal dopamine, PMID 37375579); alcohol's share
                 of energy (striatal dopamine release at low doses, meta-analysis PMID 39729041)
       lightness water per kcal (fresh, light foods), less fat (a high-fat meal raised sleepiness and fatigue 2-3 h
                 later, Wells et al. 1997, PMID 9145937)"""
    v, m = good(g), micro(g)
    if not v['kcal']:
        return 0.0
    kc = v['kcal']
    sugar = 4 * SUGARS.get(g, 0.0) / kc
    fat = min(1.0, 9 * v['fat'] / kc)
    alcohol = 7 * ALCOHOL_G.get(g, 0.0) / kc
    carb = max(0.0, 1 - fat - 4 * v['protein'] / kc - alcohol)
    water = (m['water'] / m['kcal']) if (m and m['kcal']) else 0.0
    light = min(1.0, water / 3.0) - 0.5 * fat
    return sugar + 2.0 * fat * carb + alcohol + light


def value(g):
    """M93: fullness is the limit, so the eating order weighs what a good delivers per unit of fullness: energy (1 per
    kcal), nutrients and well-being, divided by its satiety. Staples fill; the best foods deliver the calories."""
    return (1.0 + nutrition(g) + wellbeing(g)) / satiety(g)


def grams_per_day(t, n):
    return t * 1e6 / (n * 365.0)


def city_year(people, work, stocks, step_kcal=10.0):
    avail = {g: grams_per_day(t, people) for g, t in stocks.items() if g in NUT['goods']}
    q = {g: 0.0 for g in avail}
    caf = 0.0
    for g, (lpk, mgl) in BREW.items():                  # tea and coffee carry no energy; drunk up to 600 mg caffeine
        if g in avail:
            q[g] = min(avail[g], max(0.0, CAFFEINE_MG_MAX - caf) / (lpk * mgl / 1000.0))
            caf += q[g] * lpk * mgl / 1000.0
    c_caf = min(1.0, caf / CAFFEINE_MG_MAX)
    pal_work = sum(s * PAL[k] for k, s in work.items())
    e_need = BMR * pal_work + CAFFEINE_KCAL_MAX * c_caf
    e_max = BMR * PAL_MAX + CAFFEINE_KCAL_MAX * c_caf
    if 'BONUS_SALT' in avail:
        q['BONUS_SALT'] = min(avail['BONUS_SALT'], SALT_MAX_G)
    foods = [g for g in avail if g not in BREW and g != 'BONUS_SALT' and good(g)['kcal']]
    per = {}
    for g in foods:
        v = good(g)
        per[g] = dict(kc=v['kcal'] * v['edible'] / 100.0, pr=v['protein'] * v['edible'] / 100.0,
                      ft=v['fat'] * v['edible'] / 100.0, ed=v['edible'])
    cap = {}
    for g in foods:
        c = avail[g]
        if per[g]['ft'] > 0:
            c = min(c, FAT_PER_GOOD_G / per[g]['ft'])
        if g == 'BONUS_DAIRY':
            c = min(c, MILK_MAX_G)
        if g == 'BONUS_LEMON':
            c = min(c, LEMON_MAX_G)
        cap[g] = c
    vals = {g: value(g) for g in foods}
    s_cap = (HOLT_MEAN ** SAT_EXP) * e_max
    sat = 0.0
    e, p, fruit = 0.0, 0.0, 0.0
    p_max = PROTEIN_MAX_SHARE * e_max / 4.0
    # one allocation: each step of 10 kcal goes to the good whose next serving is worth most per unit of fullness:
    # value / (1 + q / serving)
    while e < e_max - 1e-9 and sat < s_cap - 1e-9:
        best, bm = None, 0.0
        for g in foods:
            dq = step_kcal / per[g]['kc']
            if q[g] + dq > cap[g] + 1e-9 or p + dq * per[g]['pr'] > p_max:
                continue
            if g in FRUIT and fruit + dq * per[g]['ed'] > FRUIT_MAX_G:
                continue
            mv = vals[g] / (1.0 + q[g] / SERVING_G[g])
            if mv > bm:
                best, bm = g, mv
        if best is None:
            break
        dq = step_kcal / per[best]['kc']
        q[best] += dq
        e += step_kcal
        sat += step_kcal * satiety(best) ** SAT_EXP
        p += dq * per[best]['pr']
        if best in FRUIT:
            fruit += dq * per[best]['ed']
    intake = {k: 0.0 for k in NUTRIENTS}
    food_water, drink_water, animal_p = 0.0, 0.0, 0.0
    for g, x in q.items():
        v, m = good(g), micro(g)
        if g in BREW:
            drink_water += x * BREW[g][0]
            eaten_100g = x * BREW[g][0] / 100.0
        else:
            eaten_100g = x * (1.0 if g == 'BONUS_SALT' else v['edible']) / 100.0
            if g in DRINKS:
                drink_water += x * v['edible'] * (v.get('hydration') or 1.0)
            elif m is not None:
                food_water += eaten_100g * m['water']
        if m is not None:
            for k in NUTRIENTS:
                intake[k] += eaten_100g * m[k]
        if g in ANIMAL:
            animal_p += x * v['protein'] * v['edible'] / 100.0
    a_fe = 0.10 + 0.08 * (animal_p / p if p else 0)
    cov = {k: intake[k] * (a_fe / 0.16 if k == 'iron' else 1.0) / NEED['needs'][k]['value'] for k in NUTRIENTS}
    plain_water = max(0.0, WATER_NEED_ML - food_water - drink_water)
    pal_act = max(PAL_MIN, min(PAL_MAX, e / BMR))
    workf = max(0.0, min(1.2, (pal_act - PAL_MIN) / (pal_work - PAL_MIN)))
    used = {g: q.get(g, 0) * people * 365 / 1e6 for g in stocks}
    left = {g: stocks[g] - used[g] for g in stocks}
    spoiled = {g: left[g] * SPOIL[NUT['goods'][g]['form']] / 100 for g in left if g in NUT['goods']}
    s_need = HOLT_MEAN * e_need                  # fed (M93): satiety met at the need, eating average foods
    return dict(fed=sat / s_need, sat=sat, s_cap=s_cap, e_need=e_need, e_max=e_max, e_in=e, x=e / e_need, prot=p, prot_share=4 * p / e if e else 0,
                food_water=food_water, drink_water=drink_water, plain_water=plain_water, caf=caf, pal_act=pal_act,
                work=workf, q=q, cov=cov, a_fe=a_fe, used=used, left=left, spoiled=spoiled)


CITIES = [
    ('A. Market town, 20,000; 70 % vigorous, 20 % active, 10 % sedentary', 20000,
     {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_WHEAT': 7000, 'BONUS_DAIRY': 4000, 'BONUS_PIG': 600, 'BONUS_APPLE': 1500, 'BONUS_ALCOHOL': 3000, 'BONUS_SALT': 60}),
    ('B. Coastal city, 200,000; 50 % vigorous, 30 % active, 20 % sedentary', 200000,
     {'vigorous': 0.5, 'active': 0.3, 'sedentary': 0.2},
     {'BONUS_RICE': 75000, 'BONUS_FISH': 35000, 'BONUS_TEA': 600, 'BONUS_BANANA': 15000, 'BONUS_SALT': 500}),
    ('C. Industrial city, 1,000,000; 40 % vigorous, 30 % active, 30 % sedentary', 1000000,
     {'vigorous': 0.4, 'active': 0.3, 'sedentary': 0.3},
     {'BONUS_WHEAT': 220000, 'BONUS_POTATO': 600000, 'BONUS_SUGAR': 30000, 'BONUS_DAIRY': 250000, 'BONUS_COW': 40000,
      'BONUS_COFFEE': 3000, 'BONUS_SALT': 3000}),
    ('E. Rich city, 100,000, everything in surplus; 20 % vigorous, 40 % active, 40 % sedentary', 100000,
     {'vigorous': 0.2, 'active': 0.4, 'sedentary': 0.4},
     {'BONUS_COW': 20000, 'BONUS_DAIRY': 150000, 'BONUS_POTATO': 60000, 'BONUS_WHEAT': 40000, 'BONUS_APPLE': 20000,
      'BONUS_SUGAR': 8000, 'BONUS_WINE': 15000, 'BONUS_TEA': 400, 'BONUS_SALT': 500}),
    ('F. Fishing village, 5,000, fish (whole animal) and crab in plenty; 70 % vigorous', 5000,
     {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_FISH': 6000, 'BONUS_CRAB': 2000, 'BONUS_SALT': 15}),
    ('G. Potato labourers, 10,000, potatoes and milk in plenty; 80 % vigorous', 10000,
     {'vigorous': 0.8, 'active': 0.1, 'sedentary': 0.1}, {'BONUS_POTATO': 30000, 'BONUS_DAIRY': 6000, 'BONUS_SALT': 30}),
    ('H. Lemon groves, 5,000, lemons, wheat and fish', 5000,
     {'vigorous': 0.6, 'active': 0.3, 'sedentary': 0.1}, {'BONUS_LEMON': 6000, 'BONUS_WHEAT': 1500, 'BONUS_FISH': 600, 'BONUS_SALT': 15}),
    ('D. Besieged town, 20,000, grain and salt pork only', 20000,
     {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_WHEAT': 3000, 'BONUS_PIG': 400, 'BONUS_SALT': 60}),
]
SHORT = {'vit_c': 'C', 'vit_a_rae': 'A', 'thiamin': 'B1', 'niacin': 'B3', 'folate_dfe': 'fol', 'b12': 'B12',
         'iron': 'Fe', 'zinc': 'Zn', 'calcium': 'Ca', 'iodine': 'I', 'potassium': 'K', 'sodium': 'Na'}


def main():
    print('BMR %.0f kcal; whole fish per 100 g as stored: %.0f kcal, %.1f g protein, %.1f g fat, %.0f ug vitamin A'
          % (BMR, WF['kcal'], WF['protein'], WF['fat'], WF['vit_a_rae']))
    print('\n| Good | Satiety | Nutrition | Well-being | Value per fullness unit | Serving g |')
    print('|---|---|---|---|---|---|')
    gs = [g for g in NUT['goods'] if NUT['goods'][g]['kcal']]
    for g in sorted(gs, key=lambda g: -value(g)):
        print('| %s | %.2f | %.2f | %.2f | %.2f | %s |' % (g[6:].title(), satiety(g), nutrition(g), wellbeing(g),
                                                          value(g), SERVING_G[g]))
    for name, n, work, stocks in CITIES:
        r = city_year(n, work, stocks)
        print('\n#### %s' % name)
        print('| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |')
        print('|---|---|---|---|---|---|')
        for g in stocks:
            print('| %s | %s | %.0f | %.0f | %s | %s |' % (g[6:].title(), format(stocks[g], ','), grams_per_day(stocks[g], n),
                  r['q'].get(g, 0), format(round(r['left'][g]), ','), format(round(r['spoiled'].get(g, 0)), ',')))
        print('\n| Fed (fullness / need) | Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x (energy) | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |')
        print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        print('| %.2f | %d / %d | %d | %d | %d | %.2f | %d (%d %%) | %d | %d | %d | %d | %.2f | %.2f |' % (
            r['fed'], r['sat'], r['s_cap'], r['e_need'], r['e_max'], r['e_in'], r['x'], r['prot'], round(100 * r['prot_share']), r['food_water'],
            r['drink_water'], r['plain_water'], r['caf'], r['pal_act'], r['work']))
        print('\n| ' + ' | '.join(SHORT[k] for k in NUTRIENTS) + ' |')
        print('|' + '---|' * len(NUTRIENTS))
        print('| ' + ' | '.join('%.2f' % r['cov'][k] for k in NUTRIENTS) + ' |')


if __name__ == '__main__':
    main()
