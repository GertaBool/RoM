"""R71 (M119): writes research/economy/data/user_inputs_template.csv, every figure and nuanced entry the food model
needs from the user, generated from the data files so that current values and sources are copied, not typed.

Columns: id, section, item, unit, needed_for, current_value, current_source, nuance, your_value, your_source.
The user fills your_value and your_source; the model reads the filled file back (a later task).
usage: python3 research/economy/plan/tools/user_inputs_template.py   (from the repository root)
"""
import csv
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
DATA = os.path.join(ROOT, 'data')


def load(n):
    with open(os.path.join(DATA, n), encoding='utf-8') as fh:
        return json.load(fh)


prof, needs, sat, nutr = load('nutrient_profiles.json'), load('nutrient_needs.json'), load('satiety_index.json'), load('nutrition.json')
rows = []


def add(section, item, unit, needed_for, current='', source='', nuance=''):
    rows.append({'id': 'U%03d' % (len(rows) + 1), 'section': section, 'item': item, 'unit': unit, 'needed_for': needed_for,
                 'current_value': current, 'current_source': source, 'nuance': nuance, 'your_value': '', 'your_source': ''})


# 1. satiety index for every game good and form the model can eat
forms = []
for g, fl in prof['goods'].items():
    if g.startswith('BONUS_'):
        forms += [g] + ['%s:%s' % (g, f['form']) for f in fl[1:]]
for g, fl in prof['mext'].items():
    forms += ['%s:mext:%s' % (g, f['form']) for f in fl]
forms += ['BONUS_FISH:herring whole, %s' % s for s in needs['whole_animal']['herring_whole_fat_pct']['value']]
for g in forms:
    m = sat['map'].get(g)
    add('satiety', 'satiety index of ' + g, 'white bread = 100, per 240 kcal', 'satiety as the gauge of being fed (M92, M93)',
        sat['holt'][m] if m else '', 'Holt 1995 (%s)' % m if m else '', 'Holt measured 38 foods; a value here is per 240 kcal over 2 h')
add('satiety', 'fullness level that counts as fed', 'mean satiety index of the day\'s energy, or another measure you name',
    'stage 2: being fed by satiety instead of energy', '', '', 'how fullness and the energy need combine: e.g. fed when both are met, or fullness first')
add('satiety', 'satiety of drinks', 'factor on the satiety of the same energy as food', 'milk, beer, wine, tea in the being-fed measure',
    '', '', 'the record: liquid calories satiate less, compensation incomplete (PMID 14649371, 36771409); no factor given')

# 2. dessert step
add('dessert', 'goods that count as dessert or well-being goods', 'list of goods', '"steak and potatoes, then dessert" (M88)', '', '', 'fruit, sugar, wine, beer, tea, olives?')
add('dessert', 'energy allowed beyond the need for dessert', 'kcal per person per day, or % of the need', 'dessert intake after nutrition is met',
    '0', 'model: energy capped at the need', 'or: dessert replaces lower-quality staple energy within the need')
add('dessert', 'order within dessert', 'rule', 'which dessert good first', '', '', 'by reward (hyper-palatable), lightness, health, repetition (M91, M102)')

# 3. rich city
for item, unit, nu in [('milk to cheese', 'kg milk per kg cheese', 'by cheese type: fresh, hard'), ('milk to butter', 'kg milk per kg butter', ''),
                       ('grain to bread', 'kg bread per kg grain', 'extraction and water added'), ('share of surplus milk turned into dairy products', '%', 'by city size or market building'),
                       ('trigger of the rich city', 'building, tier or wealth', 'Commercial Center, Commodity Market, Fair (M88)'),
                       ('sugar intake of a rich city', 'g per person per day', 'today or 1900s Britain (M91)')]:
    add('rich city', item, unit, 'rich city (M91)', '', '', nu)

# 4. game effects
for item, unit, nu in [('labour capacity to production', 'function', 'e.g. hammers or tile output x labour capacity'),
                       ('deficiency to health', 'function', 'unhealthy faces per nutrient below its minimum, or by severity'),
                       ('harms to health', 'function', 'nutrient ceilings, protein above 2.5 g/kg, alcohol, contaminants'),
                       ('nutrition (MAR) to growth or fertility', 'function', 'M75: good food raises fertility'),
                       ('nutrition to commerce, science, culture', 'function', 'M75'),
                       ('high-protein foods to unit strength', '% strength', 'M57: not siege, vehicles, robots, machines'),
                       ('starving to population', 'function', 'energy below 1.2 x REE: deaths or decline per turn'),
                       ('iodine to research or culture', 'function', 'M118: cognition')]:
    add('game effects', item, unit, 'food effects in the game (M57, M75)', '', '', nu)

# 5. animal shares
for part in ['meat', 'blubber', 'liver', 'other organs eaten']:
    add('whale', 'whale %s share' % part, '% of live or carcass weight (say which)', 'whale as eaten (M83, M85)', '', '',
        'species; MEXT holds red meat (11110), skin with blubber honkawa (11112), belly unesu (11111)')
for part in ['meat (lean)', 'liver', 'heart', 'kidneys', 'fat eaten (lard, back fat)']:
    add('pig', 'pig %s share' % part, '% of live weight', 'pig as eaten (M84, M94)', '', '', 'record: pig liver 1.5 % of slaughter by-products, base not stated')
add('cow', 'confirm cow shares meat 41.4, liver 1.12, heart 0.37, kidneys 0.18', '% of live weight', 'cow as eaten',
    '41.4 / 1.12 / 0.37 / 0.18', needs['whole_animal']['cow_as_eaten']['source'][:120], 'organ shares from a source whose base (live or carcass) is not stated')
for animal in ['sheep', 'deer', 'horse']:
    add(animal, '%s as eaten: meat and organ shares' % animal, '% of live weight', 'whole animal (M84, M94)', '', '', 'now muscle only')

# 6. ceilings per good (user)
uc = needs['user_ceilings_g']['value']
add('ceilings', 'lemons per day', 'g per person per day', 'M92', '', '', 'whole fruit or juice')
add('ceilings', 'meat per good per day', 'g', 'M85', uc['meat_per_good'], 'user M85 (a pound of ground beef)', 'applies to every meat good? to the whole animal or muscle only?')
add('ceilings', 'cheese per day', 'g', 'M85', uc['cheese'], 'user M85', '')
add('ceilings', 'milk per day', 'g', 'M88', uc['milk'], 'user M88', '')
add('ceilings', 'fat from one good per day', 'g', 'M93', uc['fat_per_good'], 'user M93', '')
add('ceilings', 'fruit per day, all fruit', 'g', 'M86', uc['fruit_total'], 'user M86 (one watermelon, USDA portion)', '')
for g in ['BONUS_SUGAR', 'BONUS_OLIVES', 'BONUS_WINE (wine)', 'BONUS_ALCOHOL (beer)', 'BONUS_SALT', 'BONUS_TEA', 'BONUS_COFFEE', 'BONUS_CLAM', 'BONUS_WHALE']:
    add('ceilings', 'ceiling of ' + g, 'g per person per day', 'what a person can physically take (P6)', '', '', '')

# 7. forms eaten by culture
for g, fl in prof['goods'].items():
    if g.startswith('BONUS_') and len(fl) + len(prof['mext'].get(g, [])) > 1:
        options = ', '.join([f['form'] for f in fl] + ['mext:' + f['form'] for f in prof['mext'].get(g, [])])
        add('forms', 'form of %s eaten by default' % g, 'form name', 'composition of the good', fl[0]['form'] if g not in ('BONUS_FISH', 'BONUS_COW') else 'whole animal as eaten',
            'first form in nutrient_profiles.json', 'options: ' + options + '; by culture, era or region?')
add('forms', 'fish catch by coast or region', 'shares of forms', 'BONUS_FISH by terrain and culture', '', '', 'North Atlantic: cod, herring, mackerel; rivers and paddies: small fish eaten whole; ...')
add('forms', 'year-round fat of whole herring', '% fat', 'herring as eaten', '', 'record: 7.9 (May) to 19.5 (August); Canadian means 9.8 and 11.2 (June-October)', '')
add('forms', 'are fish bones eaten (dried, fermented, small fish)', 'yes/no by form', 'calcium of fishing peoples', '', '', 'MEXT dried whole sardine maruboshi 570 mg calcium per 100 g')

# 8. culture and person variables
for item, unit, cur, src, nu in [('PAL by work: farmer', 'ratio', 2.41, 'Harris 2025 (Rwandan farmers)', ''),
                                 ('PAL by work: fisher', 'ratio', '', '', ''), ('PAL by work: craftsman, town dweller', 'ratio', '', '', ''),
                                 ('PAL by work: soldier, miner, labourer', 'ratio', '', '', 'record: miners lose 10-12 L water a day'),
                                 ('body weight by era or people', 'kg', 70, 'case input (Haskell 2011 reference man)', ''),
                                 ('share of children, and their adult equivalent', '% and factor', '', '', 'the record has adult levels only'),
                                 ('lactase persistence by culture', 'yes/no', '', '', 'dairy cultures (M113)'),
                                 ('tea type by culture (black or green)', 'type', '', '', 'only black tea and coffee inhibit iron in the model'),
                                 ('tea timing by culture', 'with meals / after', 'with_meal', 'case default', ''),
                                 ('maize treated with alkali by culture', 'yes/no', 'no', 'case default', 'nixtamalisation'),
                                 ('pork cooked through by culture or era', 'yes/no', '', '', 'parasite risk (M118)')]:
    add('people', item, unit, 'case variables', cur, src, nu)

# 9. spoilage marked as estimates
for k, v in nutr['spoilage_per_year_percent'].items():
    if 'estimate' in v['basis']:
        add('spoilage', 'spoilage per year, keep class ' + k, '% per year', 'keeping of what is left (M57; D2, D5)', v['value'], v['basis'], 'estimate in nutrition.json, needs a source')
add('spoilage', 'keep class of each good', 'class', 'keeping', '', 'nutrition.json goods.form', 'salt is in class "dried" whose basis names stockfish and dried fruit')

# 10. benefits above the optimum (R70)
for k in needs['nutrients']:
    add('athletes', 'athletes\' or heavy labourers\' optimum of ' + k, needs['nutrients'][k]['unit'], 'benefits towards athletes\' levels (M118)',
        needs['nutrients'][k].get('athletes', {}).get('value', '') or '', needs['nutrients'][k].get('athletes', {}).get('source', ''), 'only protein has a value in the record')
add('athletes', 'iodine study showing cognitive gains above sufficiency', 'citation', 'M118', '', '', 'trials read stop at 145-172 ug/L')

# 11. contaminants and parasites (R70)
for c, goods in [('mercury', 'fish by form'), ('cadmium', 'shellfish, offal'), ('inorganic arsenic', 'rice brown and polished, shellfish')]:
    add('contaminants', '%s concentration in %s' % (c, goods), 'mg per kg', 'harms of one-sided diets (M118)', '', '', 'primary surveys not yet read')
    add('contaminants', 'tolerable weekly intake of %s' % c, 'ug per kg body weight per week', 'harms of one-sided diets', '', '', '')
add('contaminants', 'parasite risk of undercooked pork', 'cases per kg eaten, or a rule', 'M118', '', 'record: Trichinella 0.1-2.1 %, T. solium 13.8-22 % of pigs', '')

with open(os.path.join(DATA, 'user_inputs_template.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print('wrote', len(rows), 'rows')
