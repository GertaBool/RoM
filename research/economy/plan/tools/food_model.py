"""R41.2 (M87): the food model on the game's goods, one city-year at a time.

It joins the pieces decided so far into one calculation on the food and drink goods of the settlement-economy branch
(research/economy/data/nutrition.json, the values the generator writes into CIV4BonusInfos):
  stocks (tonnes, as stored)  ->  grams per head a day  ->  what is eaten (appetite and limits)
  ->  energy, satiety, protein, nutrients, drink  ->  x, coverage, activity, work  ->  tonnes used, left, spoiled.

Data, all read from files:
  nutrition.json            kcal, protein, fat per 100 g as bought; edible share; keeping form; hydration index;
                            satiety factor (protein share x DIAAS, fitted to Holt 1995) as in food_values_edits.py
  nutrient_profiles.json    vitamins, minerals and water per 100 g edible (USDA SR Legacy; MEXT for iodine and tea)
  nutrient_needs.json       daily needs (EFSA 2017; Japanese DRI 2025 for sodium)
  FAO/WHO/UNU 2004          BMR equations, PAL by lifestyle, PAL range 1.40-2.40
Estimates are named ESTIMATE where they are set; each is a parameter to source or to decide.
usage: food_model.py
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data')
NUT = json.load(open(os.path.join(DATA, 'nutrition.json'), encoding='utf-8'))
PROF = json.load(open(os.path.join(DATA, 'nutrient_profiles.json'), encoding='utf-8'))
NEED = json.load(open(os.path.join(DATA, 'nutrient_needs.json'), encoding='utf-8'))
_spec = importlib.util.spec_from_file_location('fve', os.path.join(HERE, 'connector', 'food_values_edits.py'))
_fve = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fve)
SAT = _fve.values(NUT)                      # per good: satiety_per_kg (satiety units per kg as stored)

# ---- need (FAO/WHO/UNU 2004; EFSA reference weights; Dulloo 1989) ----
BMR = ((15.057 * 68.1 + 692.2) + (14.818 * 58.5 + 486.6)) / 2
PAL = {'vigorous': 2.25, 'active': 1.76, 'sedentary': 1.53}
PAL_MIN, PAL_MAX = 1.40, 2.40
CAFFEINE_KCAL_MAX = 150                     # 6 x 100 mg a day
CAFFEINE_MG_PER_CUP = 100
CAFFEINE_G_PER_KG = {'BONUS_TEA': 25, 'BONUS_COFFEE': 12}     # ESTIMATE (to source): caffeine in leaf and bean
TEA_LITRES_PER_KG = 43                      # ESTIMATE (to verify): MEXT infusion 10 g leaf in 430 ml
CUP_ML = 150                                # ESTIMATE

# ---- appetite and limits ----
HEADROOM = 0.15                             # ESTIMATE, appetite option B (round_m86.md 3d), not yet decided
PROTEIN_MAX_SHARE = 0.35                    # Bilsborough and Mann 2006
FAT_PER_GOOD_G = 100                        # ESTIMATE from the user's milk and beef examples (M86)
MILK_MAX_G = 3000                           # the user's estimate (M86)
FOOD_MASS_MAX_G = 6000                      # ESTIMATE: a whole watermelon, fruit as watermelon (M86)
DRINK_MAX_ML = 3500                         # ESTIMATE: total drinks a day
SALT_MAX_G = 10                             # ESTIMATE: salt eaten a day at most
DRINK_NEED_ML = 1800                        # FD.drink (M71)

# ---- game good -> USDA/MEXT form for micronutrients (nutrient_profiles.json) ----
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


def micro(good):
    """nutrients per 100 g as eaten of the good (None when the good has no profile)"""
    f = PROFILE_FORM.get(good)
    if not f:
        return None
    u = next(x for x in PROF['goods'][good] if x['form'] == f)
    r = {k: (u.get(k) or 0.0) for k in NUTRIENTS + ['kcal', 'water']}
    m = next((x for x in PROF.get('mext', {}).get(good, []) if x['form'] == MEXT_FORM.get(good)), None)
    r['iodine'] = (m['iodine'] or 0.0) if m else 0.0
    if good == 'BONUS_TEA' and m:
        r['vit_c'] = m['vit_c'] or 0.0
    return r


def grams_per_day(tonnes, people):
    return tonnes * 1e6 / (people * 365.0)


def city_year(people, work, stocks):
    """people; work = {kind: share}; stocks = {good: tonnes available this year, as stored}"""
    # 1. what is there, per head a day (stored grams; tea and coffee as infusion and caffeine)
    avail = {g: grams_per_day(t, people) for g, t in stocks.items() if g in NUT['goods']}
    caf_mg = sum(grams_per_day(stocks.get(g, 0), people) * CAFFEINE_G_PER_KG[g] for g in CAFFEINE_G_PER_KG)
    caf_supply = min(1.0, caf_mg / (6 * CAFFEINE_MG_PER_CUP))
    # 2. need
    pal_work = sum(s * PAL[k] for k, s in work.items())
    e_need = BMR * pal_work + CAFFEINE_KCAL_MAX * caf_supply
    e_max = BMR * PAL_MAX + CAFFEINE_KCAL_MAX * caf_supply
    appetite = e_need * (1 + HEADROOM)                         # in satiety units (bread-equivalent kcal)

    def per_g(g):
        v = NUT['goods'][g]
        ed = v['edible']
        return dict(kcal=v['kcal'] * ed / 100, prot=v['protein'] * ed / 100, fat=v['fat'] * ed / 100,
                    sat=SAT[g]['satiety_per_kg'] / 1000.0, mass=ed)

    caps = {}
    for g, a in avail.items():
        p = per_g(g)
        c = a
        if p['fat'] > 0:
            c = min(c, FAT_PER_GOOD_G / p['fat'])
        if g == 'BONUS_DAIRY':
            c = min(c, MILK_MAX_G)
        if g == 'BONUS_SALT':
            c = min(c, SALT_MAX_G)
        if g == 'BONUS_TEA':
            c = min(c, DRINK_MAX_ML / (TEA_LITRES_PER_KG))   # g leaf for at most the drink cap
        caps[g] = c

    def at(t):
        q = {g: min(t * avail[g], caps[g]) for g in avail}
        tot = dict(kcal=0.0, prot=0.0, sat=0.0, mass=0.0, drink=0.0)
        for g, x in q.items():
            p = per_g(g)
            tot['kcal'] += x * p['kcal']
            tot['prot'] += x * p['prot']
            tot['sat'] += x * p['sat']
            if g == 'BONUS_TEA':
                tot['drink'] += x * TEA_LITRES_PER_KG
            elif g in DRINKS:
                tot['drink'] += x * p['mass']
            else:
                tot['mass'] += x * p['mass']
        return q, tot

    def ok(t):
        q, s = at(t)
        return (s['sat'] <= appetite and s['kcal'] <= e_max and s['prot'] * 4 <= PROTEIN_MAX_SHARE * e_max
                and s['mass'] <= FOOD_MASS_MAX_G and s['drink'] <= DRINK_MAX_ML)

    lo, hi = 0.0, 1.0
    if ok(1.0):
        lo = 1.0
    else:
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    q, s = at(lo)
    binding = 'none: all eaten'
    if lo < 1.0:
        q2, s2 = at(min(1.0, lo + 1e-4))
        for name, over in (('appetite', s2['sat'] > appetite), ('energy', s2['kcal'] > e_max),
                           ('protein', s2['prot'] * 4 > PROTEIN_MAX_SHARE * e_max),
                           ('food mass', s2['mass'] > FOOD_MASS_MAX_G), ('drink', s2['drink'] > DRINK_MAX_ML)):
            if over:
                binding = name
                break
    # 3. nutrients: USDA/MEXT values per 100 g of the eaten form, applied to the grams eaten (energy from nutrition.json)
    intake = {k: 0.0 for k in NUTRIENTS}
    fruit_water = 0.0
    animal_prot = 0.0
    for g, x in q.items():
        m = micro(g)
        if m is None:
            continue
        p = per_g(g)
        if g == 'BONUS_TEA':
            eaten_100g = x * TEA_LITRES_PER_KG / 100.0           # infusion grams / 100
        else:
            eaten_100g = x * (1.0 if g == 'BONUS_SALT' else p['mass']) / 100.0   # grams eaten / 100 (salt: edible 0 means no energy, but it is eaten)
        for k in NUTRIENTS:
            intake[k] += eaten_100g * m[k]
        if g in FRUIT:
            fruit_water += eaten_100g * m['water']
        if g in ANIMAL:
            animal_prot += x * p['prot']
    a_fe = 0.10 + 0.08 * (animal_prot / s['prot'] if s['prot'] else 0)   # FAO 10 % to 18 % (straight line ESTIMATE)
    cov = {}
    for k in NUTRIENTS:
        need = NEED['needs'][k]['value']
        v = intake[k] * (a_fe / 0.16 if k == 'iron' else 1.0)
        cov[k] = v / need
    drink = s['drink'] + fruit_water
    # 4. outcome
    x_suff = s['kcal'] / e_need
    pal_act = max(PAL_MIN, min(PAL_MAX, s['kcal'] / BMR))
    workf = max(0.0, min(1.2, (pal_act - PAL_MIN) / (pal_work - PAL_MIN)))
    # 5. goods used, left and spoiled (tonnes a year)
    used = {g: q[g] * people * 365 / 1e6 for g in q}
    left = {g: stocks[g] - used.get(g, 0) for g in stocks}
    spoiled = {g: left[g] * SPOIL[NUT['goods'][g]['form']] / 100 for g in left if g in NUT['goods']}
    return dict(e_need=e_need, appetite=appetite, e_in=s['kcal'], sat=s['sat'], x=x_suff, prot=s['prot'],
                prot_share=s['prot'] * 4 / s['kcal'] if s['kcal'] else 0, mass=s['mass'], drink=drink,
                pal_act=pal_act, work=workf, binding=binding, q=q, cov=cov, a_fe=a_fe, caf=caf_supply,
                used=used, left=left, spoiled=spoiled)


CITIES = [
    ('A. Market town, 20,000; 70 % vigorous, 20 % active, 10 % sedentary',
     20000, {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_WHEAT': 7000, 'BONUS_DAIRY': 4000, 'BONUS_PIG': 600, 'BONUS_APPLE': 1500, 'BONUS_ALCOHOL': 3000,
      'BONUS_SALT': 60}),
    ('B. Coastal city, 200,000; 50 % vigorous, 30 % active, 20 % sedentary',
     200000, {'vigorous': 0.5, 'active': 0.3, 'sedentary': 0.2},
     {'BONUS_RICE': 75000, 'BONUS_FISH': 35000, 'BONUS_TEA': 600, 'BONUS_BANANA': 15000, 'BONUS_SALT': 500}),
    ('C. Industrial city, 1,000,000; 40 % vigorous, 30 % active, 30 % sedentary',
     1000000, {'vigorous': 0.4, 'active': 0.3, 'sedentary': 0.3},
     {'BONUS_WHEAT': 220000, 'BONUS_POTATO': 600000, 'BONUS_SUGAR': 30000, 'BONUS_DAIRY': 250000, 'BONUS_COW': 40000,
      'BONUS_COFFEE': 3000, 'BONUS_SALT': 3000}),
    ('D. Besieged town, 20,000, grain and salt pork only',
     20000, {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_WHEAT': 3000, 'BONUS_PIG': 400, 'BONUS_SALT': 60}),
]

SHORT = {'vit_c': 'C', 'vit_a_rae': 'A', 'thiamin': 'B1', 'niacin': 'B3', 'folate_dfe': 'fol', 'b12': 'B12',
         'iron': 'Fe', 'zinc': 'Zn', 'calcium': 'Ca', 'iodine': 'I', 'potassium': 'K', 'sodium': 'Na'}


def main():
    print('BMR %.0f kcal a day (abstracted adult)' % BMR)
    for name, people, work, stocks in CITIES:
        r = city_year(people, work, stocks)
        print('\n### %s' % name)
        print('| Good | Stock t | Per head g/day | Eaten g/day | Used t | Left t | Spoiled t |')
        print('|---|---|---|---|---|---|---|')
        for g in stocks:
            a = grams_per_day(stocks[g], people)
            print('| %s | %s | %.0f | %.0f | %s | %s | %s |' % (g[6:].title(), format(stocks[g], ','), a, r['q'].get(g, 0),
                  format(round(r['used'].get(g, 0)), ','), format(round(r['left'][g]), ','),
                  format(round(r['spoiled'].get(g, 0)), ',')))
        print('\n| Need kcal | Appetite (satiety units) | Eaten kcal | Satiety eaten | x | Protein g (share) | Food mass g | Drink ml | Caffeine supply | PAL actual | Work | Binding |')
        print('|---|---|---|---|---|---|---|---|---|---|---|---|')
        print('| %d | %d | %d | %d | %.2f | %d (%d %%) | %d | %d | %.2f | %.2f | %.2f | %s |' % (
            r['e_need'], r['appetite'], r['e_in'], r['sat'], r['x'], r['prot'], round(100 * r['prot_share']),
            r['mass'], r['drink'], r['caf'], r['pal_act'], r['work'], r['binding']))
        print('\nCoverage (1.00 = need met; iron after absorption %.0f %%):' % (100 * r['a_fe']))
        print('| ' + ' | '.join(SHORT[k] for k in NUTRIENTS) + ' |')
        print('|' + '---|' * len(NUTRIENTS))
        print('| ' + ' | '.join('%.2f' % r['cov'][k] for k in NUTRIENTS) + ' |')


if __name__ == '__main__':
    main()
