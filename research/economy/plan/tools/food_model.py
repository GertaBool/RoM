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
CAFFEINE_KCAL_MAX = 150                     # Dulloo 1989: 6 x 100 mg a day
CAFFEINE_MG_MAX = 600
# brewing (MEXT 8th edition, remarks of the infusion records): litres of drink per kg and caffeine per litre
#   sencha 10 g / 430 ml, caffeine 0.02 g per 100 g; coffee 10 g / 150 ml, caffeine 0.06 g per 100 g
BREW = {'BONUS_TEA': (43.0, 200.0), 'BONUS_COFFEE': (15.0, 600.0)}

# ---- physiological ceilings (M85, M86, M88) ----
PROTEIN_MAX_SHARE = 0.35                    # Bilsborough and Mann 2006 (danger above 35 % of energy)
FAT_PER_GOOD_G = 100                        # accepted (M88)
MILK_MAX_G = 3000                           # the user (M86, M88)
FRUIT_MAX_G = 4518                          # one whole watermelon (USDA SR Legacy portion, fdc 167765), all fruit together (M86, M88)
SALT_MAX_G = 10                             # ESTIMATE
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


# Holt et al. 1995 satiety index (white bread 100), measured values as the Wikipedia "Satiety value" table reproduces
# them (PMID 7498104); goods without a measured food keep the protein-factor formula of food_values_edits.py. Holt's
# abstract: water (r 0.64), fibre (0.46) and protein (0.37) raise satiety, fat lowers it (-0.43).
SI_MEASURED = {'BONUS_POTATO': 323, 'BONUS_FISH': 225, 'BONUS_COW': 176, 'BONUS_RICE': 138, 'BONUS_WHEAT': 100,
               'BONUS_APPLE': 197, 'BONUS_LEMON': 202, 'BONUS_BANANA': 118}   # lemon: Holt's oranges (citrus)


def satiety_factor(g):
    return SI_MEASURED[g] / 100.0 if g in SI_MEASURED else SAT[g]['factor']


def quality(g):
    """eating order (M88: the best goods first by nutrition, health and satiety): satiety factor x (1 + nutrient
    density). Nutrient density as in the Nutrient Rich Foods index (Drewnowski and Fulgoni 2011, PMID 21272703):
    per 100 kcal, each nutrient as a share of its daily need, capped at 1, averaged over the 12 nutrients and protein."""
    v = NUT['goods'][g]
    if not v['kcal']:
        return 0.0
    m = micro(g)
    shares = []
    if m is not None and m['kcal']:
        for k in NUTRIENTS:
            shares.append(min(1.0, m[k] * 100.0 / m['kcal'] / NEED['needs'][k]['value']))
    shares.append(min(1.0, v['protein'] * 100.0 / v['kcal'] / NEED['needs']['protein']['value']))
    nd = sum(shares) / len(shares)
    return satiety_factor(g) * (1 + nd)


def grams_per_day(tonnes, people):
    return tonnes * 1e6 / (people * 365.0)


def city_year(people, work, stocks):
    """people; work = {kind: share}; stocks = {good: tonnes available this year, as stored}"""
    avail = {g: grams_per_day(t, people) for g, t in stocks.items() if g in NUT['goods']}
    # 1. caffeine drinks first: as much as is there, up to 600 mg
    caf_mg, drink_ml, q = 0.0, 0.0, {}
    for g, (l_per_kg, mg_per_l) in BREW.items():
        if g in avail:
            gram = min(avail[g], max(0.0, CAFFEINE_MG_MAX - caf_mg) / (l_per_kg * mg_per_l / 1000.0))
            q[g] = gram
            caf_mg += gram * l_per_kg * mg_per_l / 1000.0
            drink_ml += gram * l_per_kg
    c_caf = min(1.0, caf_mg / CAFFEINE_MG_MAX)
    # 2. need and the energy ceiling (appetite = what the body can turn over: PAL 2.40)
    pal_work = sum(s * PAL[k] for k, s in work.items())
    e_need = BMR * pal_work + CAFFEINE_KCAL_MAX * c_caf
    e_max = BMR * PAL_MAX + CAFFEINE_KCAL_MAX * c_caf
    # 3. eat in order of quality, each good up to its ceiling and the room left
    e_room, p_room, fruit_room = e_max, PROTEIN_MAX_SHARE * e_max / 4.0, FRUIT_MAX_G
    order = sorted([g for g in avail if g not in BREW], key=lambda g: -quality(g))
    binding = {}
    for g in order:
        v = NUT['goods'][g]
        ed = v['edible']
        kc, pr, ft = v['kcal'] * ed / 100.0, v['protein'] * ed / 100.0, v['fat'] * ed / 100.0
        lim = {'stock': avail[g]}
        if ft > 0:
            lim['fat 100 g'] = FAT_PER_GOOD_G / ft
        if g == 'BONUS_DAIRY':
            lim['milk 3 L'] = MILK_MAX_G
        if g in FRUIT:
            lim['fruit (one watermelon)'] = fruit_room / ed
        if g == 'BONUS_SALT':
            lim['salt'] = SALT_MAX_G
        if kc > 0:
            lim['energy ceiling'] = e_room / kc
        if pr > 0:
            lim['protein ceiling'] = p_room / pr
        why = min(lim, key=lim.get)
        x = max(0.0, lim[why])
        q[g] = x
        binding[g] = why
        e_room -= x * kc
        p_room -= x * pr
        if g in FRUIT:
            fruit_room -= x * ed
    # 4. totals
    e_in = sum(q[g] * NUT['goods'][g]['kcal'] * NUT['goods'][g]['edible'] / 100.0 for g in q)
    prot = sum(q[g] * NUT['goods'][g]['protein'] * NUT['goods'][g]['edible'] / 100.0 for g in q)
    sat = sum(q[g] * SAT[g]['satiety_per_kg'] / 1000.0 for g in q)
    intake = {k: 0.0 for k in NUTRIENTS}
    fruit_water, animal_prot = 0.0, 0.0
    for g, x in q.items():
        m = micro(g)
        ed = NUT['goods'][g]['edible']
        if g in DRINKS and g not in BREW:
            drink_ml += x * ed
        if m is None:
            continue
        if g == 'BONUS_TEA':
            eaten_100g = x * BREW[g][0] / 100.0
        else:
            eaten_100g = x * (1.0 if g == 'BONUS_SALT' else ed) / 100.0
        for k in NUTRIENTS:
            intake[k] += eaten_100g * m[k]
        if g in FRUIT:
            fruit_water += eaten_100g * m['water']
        if g in ANIMAL:
            animal_prot += x * NUT['goods'][g]['protein'] * ed / 100.0
    a_fe = 0.10 + 0.08 * (animal_prot / prot if prot else 0)
    cov = {k: intake[k] * (a_fe / 0.16 if k == 'iron' else 1.0) / NEED['needs'][k]['value'] for k in NUTRIENTS}
    drink = drink_ml + fruit_water
    x_suff = e_in / e_need
    pal_act = max(PAL_MIN, min(PAL_MAX, e_in / BMR))
    workf = max(0.0, min(1.2, (pal_act - PAL_MIN) / (pal_work - PAL_MIN)))
    used = {g: q.get(g, 0) * people * 365 / 1e6 for g in stocks}
    left = {g: stocks[g] - used[g] for g in stocks}
    spoiled = {g: left[g] * SPOIL[NUT['goods'][g]['form']] / 100 for g in left if g in NUT['goods']}
    return dict(e_need=e_need, e_max=e_max, e_in=e_in, sat=sat, x=x_suff, prot=prot,
                prot_share=prot * 4 / e_in if e_in else 0, drink=drink, water_from_supply=max(0, DRINK_NEED_ML - drink),
                pal_act=pal_act, work=workf, q=q, order=order, binding=binding, cov=cov, a_fe=a_fe, caf=caf_mg,
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
    ('E. Rich city, 100,000, everything in surplus; 20 % vigorous, 40 % active, 40 % sedentary',
     100000, {'vigorous': 0.2, 'active': 0.4, 'sedentary': 0.4},
     {'BONUS_COW': 20000, 'BONUS_DAIRY': 150000, 'BONUS_POTATO': 60000, 'BONUS_WHEAT': 40000, 'BONUS_APPLE': 20000,
      'BONUS_SUGAR': 8000, 'BONUS_WINE': 15000, 'BONUS_SALT': 500}),
    ('F. Fishing village, 5,000, seafood only in plenty; 70 % vigorous',
     5000, {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_FISH': 6000, 'BONUS_CRAB': 2000, 'BONUS_SALT': 15}),
    ('D. Besieged town, 20,000, grain and salt pork only',
     20000, {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_WHEAT': 3000, 'BONUS_PIG': 400, 'BONUS_SALT': 60}),
]

SHORT = {'vit_c': 'C', 'vit_a_rae': 'A', 'thiamin': 'B1', 'niacin': 'B3', 'folate_dfe': 'fol', 'b12': 'B12',
         'iron': 'Fe', 'zinc': 'Zn', 'calcium': 'Ca', 'iodine': 'I', 'potassium': 'K', 'sodium': 'Na'}


def main():
    print('BMR %.0f kcal a day (abstracted adult)' % BMR)
    print('\nEating order (quality = satiety factor x (1 + nutrient density per 100 kcal)):')
    print('| Rank | Good | Satiety (Holt where measured) | Quality |')
    print('|---|---|---|---|')
    rank = sorted([g for g in NUT['goods'] if NUT['goods'][g]['kcal']], key=lambda g: -quality(g))
    for i, g in enumerate(rank, 1):
        print('| %d | %s | %.2f%s | %.2f |' % (i, g[6:].title(), satiety_factor(g), ' (Holt)' if g in SI_MEASURED else '', quality(g)))
    for name, people, work, stocks in CITIES:
        r = city_year(people, work, stocks)
        print('\n### %s' % name)
        print('| Good (in eating order) | Stock t | Per head g/day | Eaten g/day | Stopped by | Used t | Left t | Spoiled t |')
        print('|---|---|---|---|---|---|---|---|')
        for g in [g for g in BREW if g in stocks] + r['order']:
            a = grams_per_day(stocks[g], people)
            print('| %s | %s | %.0f | %.0f | %s | %s | %s | %s |' % (g[6:].title(), format(stocks[g], ','), a, r['q'].get(g, 0),
                  r['binding'].get(g, 'caffeine 600 mg' if g in BREW and r['q'][g] < a - 1e-6 else 'stock'),
                  format(round(r['used'][g]), ','), format(round(r['left'][g]), ','), format(round(r['spoiled'].get(g, 0)), ',')))
        print('\n| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Drink ml (from goods) | From water supply ml | Caffeine mg | PAL actual | Work |')
        print('|---|---|---|---|---|---|---|---|---|---|')
        print('| %d | %d | %d | %.2f | %d (%d %%) | %d | %d | %d | %.2f | %.2f |' % (
            r['e_need'], r['e_max'], r['e_in'], r['x'], r['prot'], round(100 * r['prot_share']), r['drink'],
            r['water_from_supply'], r['caf'], r['pal_act'], r['work']))
        print('\nCoverage (1.00 = need met; iron after absorption %.0f %%):' % (100 * r['a_fe']))
        print('| ' + ' | '.join(SHORT[k] for k in NUTRIENTS) + ' |')
        print('|' + '---|' * len(NUTRIENTS))
        print('| ' + ' | '.join('%.2f' % r['cov'][k] for k in NUTRIENTS) + ' |')


if __name__ == '__main__':
    main()
