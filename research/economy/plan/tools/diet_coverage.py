"""R37.12 (M83): how much of each daily need a diet covers.

Reads research/economy/data/nutrient_profiles.json (USDA SR Legacy, with MEXT values for iodine and tea) and
research/economy/data/nutrient_needs.json (EFSA 2017 and the Japanese DRI 2025), and prints, for each diet, the share
of each need it covers (1.00 = the need met). A value marked >= (≥) leaves out foods with no value in the
file for that nutrient. Iodine comes from MEXT, because SR Legacy holds no iodine for these
foods. The diets in DIETS are constructed examples to show the arithmetic, not historical records.

usage: diet_coverage.py [--md]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data')
NUTR = ['protein', 'vit_c', 'vit_a_rae', 'thiamin', 'niacin', 'folate_dfe', 'b12', 'iron', 'zinc', 'calcium',
        'iodine', 'potassium', 'sodium']
SHORT = {'protein': 'prot', 'vit_c': 'C', 'vit_a_rae': 'A', 'thiamin': 'B1', 'niacin': 'B3', 'folate_dfe': 'fol',
         'b12': 'B12', 'iron': 'Fe', 'zinc': 'Zn', 'calcium': 'Ca', 'iodine': 'I', 'potassium': 'K', 'sodium': 'Na'}

# (good, USDA form, MEXT form for iodine or None); the MEXT form also replaces vitamin C where USDA has none (tea)
FOODS = {
    'wheat': ('BONUS_WHEAT', 'grain', 'soft flour'), 'rice_polished': ('BONUS_RICE', 'polished', 'polished'),
    'rice_brown': ('BONUS_RICE', 'brown', 'polished'), 'corn': ('BONUS_CORN', 'grain', 'grain'),
    'potato': ('BONUS_POTATO', 'raw', 'raw'), 'potato_boiled': ('BONUS_POTATO', 'boiled', 'raw'),
    'beef': ('BONUS_COW', 'meat', 'shoulder'), 'pork': ('BONUS_PIG', 'meat', 'loin'),
    'cod': ('BONUS_FISH', 'cod', 'cod'), 'herring': ('BONUS_FISH', 'herring', 'sardine'),
    'milk': ('BONUS_DAIRY', 'milk', 'milk'), 'butter': ('BONUS_DAIRY', 'butter', None),
    'banana': ('BONUS_BANANA', 'raw', 'raw'), 'apple': ('BONUS_APPLE', 'raw', 'with skin'),
    'beer': ('BONUS_ALCOHOL', 'beer', None), 'salt': ('BONUS_SALT', 'table salt', 'salt'),
    'egg': ('REF_EGG', 'raw', 'raw'), 'cabbage': ('REF_CABBAGE', 'raw', 'raw'), 'lentils': ('REF_LENTILS', 'raw', None),
    'barley': ('REF_BARLEY', 'hulled', None),
    'sencha': ('BONUS_TEA', 'green, brewed', 'sencha infusion'),
}
TEA_FROM_MEXT = {'sencha'}

DIETS = {  # grams a day
    'wheat only': {'wheat': None}, 'polished rice only': {'rice_polished': None}, 'brown rice only': {'rice_brown': None},
    'maize only': {'corn': None}, 'potato only': {'potato_boiled': None}, 'beef only': {'beef': None},
    'milk only': {'milk': None}, 'cod only': {'cod': None},
    'sailor: grain, salt pork, beer': {'wheat': 500, 'pork': 300, 'beer': 1000, 'salt': 10},
    'grain farmer': {'wheat': 650, 'cabbage': 200, 'milk': 300, 'beer': 500, 'salt': 5},
    'herder': {'milk': 2000, 'beef': 300, 'barley': 150},
    'coastal: rice, fish, green tea': {'rice_brown': 450, 'cod': 400, 'potato_boiled': 300, 'cabbage': 200, 'sencha': 600, 'salt': 5},
    'varied': {'wheat': 350, 'potato_boiled': 300, 'beef': 100, 'milk': 300, 'egg': 50, 'cabbage': 150, 'apple': 200,
               'herring': 100, 'lentils': 60, 'butter': 20, 'salt': 3},
}


def load():
    prof = json.load(open(os.path.join(DATA, 'nutrient_profiles.json'), encoding='utf-8'))
    needs = json.load(open(os.path.join(DATA, 'nutrient_needs.json'), encoding='utf-8'))
    return prof, needs


def food_row(prof, name):
    good, uform, mform = FOODS[name]
    u = next(f for f in prof['goods'][good] if f['form'] == uform)
    row = {k: u.get(k) for k in NUTR + ['kcal']}
    m = next((f for f in prof.get('mext', {}).get(good, []) if f['form'] == mform), None) if mform else None
    row['iodine'] = m['iodine'] if m else None
    if name in TEA_FROM_MEXT and m:
        row['vit_c'] = m['vit_c']
    return row


def coverage(prof, needs, diet):
    kcal_ref = needs['reference']['energy_kcal']
    items = dict(diet)
    if len(items) == 1 and list(items.values())[0] is None:     # single food eaten to the energy need
        name = list(items)[0]
        items[name] = 100.0 * kcal_ref / food_row(prof, name)['kcal']
    tot = {k: 0.0 for k in NUTR + ['kcal']}
    unknown = set()
    for name, g in items.items():
        r = food_row(prof, name)
        for k in tot:
            if r[k] is None:
                unknown.add(k)
            else:
                tot[k] += r[k] * g / 100.0
    cov = {k: tot[k] / needs['needs'][k]['value'] for k in NUTR}
    return items, tot['kcal'], cov, unknown


def main(md):
    prof, needs = load()
    hdr = ['diet', 'kcal'] + [SHORT[k] for k in NUTR]
    if md:
        print('| ' + ' | '.join(hdr) + ' |')
        print('|' + '---|' * len(hdr))
    else:
        print('%-34s %6s ' % tuple(hdr[:2]) + ' '.join('%5s' % h for h in hdr[2:]))
    for name, diet in DIETS.items():
        items, kcal, cov, unk = coverage(prof, needs, diet)
        cells = [(('>=%.2f' if md is False else '≥%.2f') % cov[k] if k in unk else '%.2f' % cov[k]) for k in NUTR]
        if md:
            print('| %s | %d | %s |' % (name, kcal, ' | '.join(cells)))
        else:
            print('%-34s %6d ' % (name, kcal) + ' '.join('%5s' % c for c in cells))
    if not md:
        for name, diet in DIETS.items():
            items = coverage(prof, needs, diet)[0]
            print('  %s: %s' % (name, ', '.join('%s %d g' % (k, v) for k, v in items.items())))


if __name__ == '__main__':
    main('--md' in sys.argv)
