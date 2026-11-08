"""SUPERSEDED (R76, M126): it read only two columns and added readings the user did not write (user_inputs_audit_m125.md). Do not use; the values are translated only from the user's answers to data/user_inputs_m120.questions.ods.

R72 (M120): read the user's edited inputs (data/user_inputs_m120.csv, exported from user_inputs_m120.ods by ods_read.py)
and write data/user_inputs.json, the structured values the food model reads. Each row is parsed by its id; a row whose
text does not match the expected shape stops the run, so nothing is guessed. The user's text is kept verbatim beside
each parsed value.

usage: python3 research/economy/plan/tools/user_inputs_apply.py   (from the repository root)
"""
import csv
import json
import os
import re

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')
rows = {r['id']: r for r in csv.DictReader(open(os.path.join(DATA, 'user_inputs_m120.csv'), encoding='utf-8'))}


def val(i):
    return (rows[i].get('your_value') or '').strip()


def note(i):
    return (rows[i].get('your_nuance') or '').strip()


def number(i):
    t = val(i).replace(',', '')
    m = re.fullmatch(r'(-?[0-9.]+)\s*(%|kg|g|L)?', t)
    if not m:
        raise SystemExit('row %s: no number in %r' % (i, val(i)))
    return float(m.group(1)) / (100.0 if m.group(2) == '%' else 1.0)


def pcts(i, n):
    v = [float(x) / 100.0 for x in re.findall(r'([0-9.]+)\s*%', val(i))]
    if len(v) != n:
        raise SystemExit('row %s: expected %d percentages in %r' % (i, n, val(i)))
    return v


out = {'about': 'Values the user gave in user_inputs_m120.ods (M120), parsed by plan/tools/user_inputs_apply.py; "text" is the user\'s own wording.',
       'satiety_index': {}, 'not_relevant': []}

# satiety (U001-U088): item 'satiety index of KEY'
for i, r in rows.items():
    if r['section'] == 'satiety' and r['item'].startswith('satiety index of '):
        key = r['item'][len('satiety index of '):]
        t = val(i)
        if t.startswith('(not relevant)'):
            out['satiety_index'][key] = None
        elif t:
            out['satiety_index'][key] = float(t)
out['fed_fullness'] = {'value': number('U089'), 'unit': 'satiety-weighted kcal: sum of (satiety index / 100) x kcal', 'text': val('U089'),
                       'reading': 'fullness of 3,000 kcal of white bread counts as fed'}
out['drink_satiety_factor'] = {'value': number('U090'), 'text': val('U090')}

# dessert (U091-U093)
out['dessert'] = {'goods': [g.strip(' ,') for g in re.split(r'(?=BONUS_)', val('U091')) if g.strip(' ,')], 'text_goods': val('U091'),
                  'energy_beyond_need_share': number('U092'), 'text_energy': val('U092'),
                  'order': [{'bases': ['BONUS_SUGAR']},
                            {'bases': ['BONUS_BANANA', 'BONUS_LEMON', 'BONUS_APPLE', 'BONUS_WINE'], 'except': ['BONUS_WINE:wine', 'BONUS_WINE:mext:red wine']},
                            {'goods': ['BONUS_WINE:wine', 'BONUS_WINE:mext:red wine'], 'bases': ['BONUS_ALCOHOL']},
                            {'bases': ['BONUS_TEA', 'BONUS_OLIVES']}],
                  'text_order': val('U093'),
                  'order_reading': 'sugar (all forms); then fruit: banana, lemon, apple and the grape forms of BONUS_WINE (grapes, raisins); then wine and beer; then tea and olives (all forms)'}

# rich city (U094-U099)
out['rich_city'] = {'milk_kg_per_kg_cheese': number('U094'), 'milk_kg_per_kg_butter': number('U095'), 'bread_kg_per_kg_grain': number('U096'),
                    'surplus_milk_to_dairy_share': number('U097'), 'trigger': val('U098'), 'trigger_note': note('U098'),
                    'sugar_g_per_day': float(re.match(r'([0-9.]+)', val('U099')).group(1)), 'sugar_source': note('U099')}

# game effects (U100-U107): design inputs, kept verbatim
out['game_effects'] = {rows[i]['item']: {'text': val(i), 'note': note(i)} for i in ['U100', 'U101', 'U102', 'U103', 'U104', 'U105', 'U106', 'U107']}
out['strength_anchors'] = {'protein_g_30pct': 50.0, 'protein_per_kg_80pct': 1.6, 'protein_cap_g_200pct': 'liver limit (urea capacity), user: roughly 288 g', 'cap_pct': 200,
                           'text': val('U105'), 'shape': 'logarithmic (user); the tool interpolates linearly in ln(protein) between the anchors'}
out['iq_from_iodine_anchors'] = {'points_ug_iq': [[150, 100], [1000, 115], [5000, 115], [5000000, 0]], 'floor_iq': 70, 'below_150_to': 70,
                                 'text': val('U107'), 'note': note('U107'),
                                 'shape': 'the tool interpolates linearly in log10(iodine) between the anchors; below 150 ug it falls towards 70 at 15 ug (one tenth), a reading of "possibly two standard deviations less"'}

# animal shares (U108-U120)
out['whale_shares'] = {'meat': number('U108'), 'blubber': number('U109'), 'liver': number('U110'), 'other_organs': number('U111'),
                       'source': note('U108'), 'base': 'not stated (live or carcass)'}
out['pig_shares'] = {'lean': number('U112'), 'liver': number('U113'), 'heart': number('U114'), 'kidneys': number('U115'), 'fat': number('U116')}
for i, a in [('U117', 'cow'), ('U118', 'sheep'), ('U119', 'deer'), ('U120', 'horse')]:
    m, f, o = pcts(i, 3)
    out[a + '_shares'] = {'lean': m, 'fat': f, 'organs': o, 'text': val(i)}

# ceilings (U121-U135)
out['ceilings_g'] = {'BONUS_LEMON': 30.0, 'BONUS_LEMON:juice': 1000.0, 'text_lemon': val('U121'),
                     'meat_total': {'median': 150.0, 'upper': 400.0, 'max': 1000.0, 'text': val('U122'), 'note': note('U122')},
                     'cheese': number('U123'), 'milk': number('U124'), 'fat_per_good': number('U125'), 'fruit_total': number('U126'),
                     'BONUS_SUGAR': number('U127'), 'BONUS_OLIVES': number('U128'), 'BONUS_WINE:wine': number('U129'), 'BONUS_ALCOHOL': number('U130'),
                     'BONUS_SALT': number('U131'), 'BONUS_TEA': number('U132'), 'BONUS_COFFEE': number('U133'), 'BONUS_CLAM': number('U134'), 'BONUS_WHALE': number('U135'),
                     'salt_note': note('U131')}

# default forms (U136-U153)
FORM = {'U136': ('BONUS_WHEAT', 'bread'), 'U137': ('BONUS_RICE', 'polished'), 'U138': ('BONUS_CORN', 'grain'), 'U139': ('BONUS_POTATO', 'boiled'),
        'U140': ('BONUS_COW', 'whole'), 'U141': ('BONUS_PIG', 'whole'), 'U142': ('BONUS_FISH', 'whole'), 'U143': ('BONUS_CLAM', 'raw'),
        'U144': ('BONUS_WHALE', 'whole'), 'U145': ('BONUS_DAIRY', 'milk'), 'U146': ('BONUS_BANANA', 'raw'), 'U147': ('BONUS_LEMON', 'juice'),
        'U148': ('BONUS_APPLE', 'raw'), 'U149': ('BONUS_OLIVES', 'oil'), 'U150': ('BONUS_SUGAR', 'brown'), 'U151': ('BONUS_WINE', 'grapes'),
        'U152': ('BONUS_TEA', 'herbal, brewed'), 'U153': ('BONUS_SALT', 'table salt')}
out['default_form'] = {}
for i, (g, f) in FORM.items():
    out['default_form'][g] = {'form': f, 'text': val(i), 'note': note(i)}

# fish catch by region (U154)
t = val('U154')
regions = ['Asia', 'Europe', 'Africa', 'Latin America', 'N. America', 'Oceania']
cats = ['Freshwater fish', 'Small pelagic', 'Large pelagic', 'Demersal', 'Salmonids', 'Other marine fish']
catch = {r: {} for r in regions}
for c in cats:
    m = re.search(re.escape(c) + r'((?:\s+[0-9.]+%){6})', t)
    if not m:
        raise SystemExit('U154: no row for ' + c)
    for r, v in zip(regions, re.findall(r'([0-9.]+)%', m.group(1))):
        catch[r][c] = float(v) / 100.0
for r in regions:
    if abs(sum(catch[r].values()) - 1.0) > 0.011:
        raise SystemExit('U154: %s shares sum to %.3f' % (r, sum(catch[r].values())))
out['fish_catch_by_region'] = {'shares': catch, 'text': t}
out['herring_year_round_fat'] = number('U155')
out['fish_bones_eaten'] = val('U156')

# people (U157-U167)
out['pal_by_work'] = {'manual labour': number('U157'), 'sedentary': number('U158'), 'soldier': number('U159'), 'slaves in quarries or mines': number('U160')}
out['body_weight'] = {'text': val('U161')}
lp = {}
for line in val('U163').splitlines():
    m = re.match(r'\s*(.+?):\s*([0-9.]+)%', line)
    if m:
        lp[m.group(1)] = float(m.group(2)) / 100.0
out['lactase_persistence'] = {'shares': lp, 'note': note('U163')}
for i in ['U162', 'U164', 'U165', 'U166', 'U167', 'U197']:
    if val(i).lower().startswith('not relevant'):
        out['not_relevant'].append(rows[i]['item'])

# spoilage (U168-U172)
out['spoilage_per_year'] = {'cured, salted, fermented': number('U168'), 'dried': number('U169'), 'canned': number('U170'),
                            'roots and grains': number('U171'), 'others': number('U172'),
                            'notes': {rows[i]['item']: note(i) for i in ['U168', 'U169', 'U170', 'U171', 'U172'] if note(i)}}

# athletes (U173-U189)
KEY = {'protein': ('protein', 'g'), 'sodium': ('sodium', 'g'), 'potassium': ('potassium', 'mg'), 'calcium': ('calcium', 'mg'), 'magnesium': ('magnesium', 'mg'),
       'iron': ('iron', 'mg'), 'zinc': ('zinc', 'mg'), 'iodine': ('iodine', 'mcg'), 'selenium': ('selenium', 'mcg'), 'vitamin A': ('vit_a_rae', 'mcg'),
       'thiamin': ('thiamin', 'mg'), 'riboflavin': ('riboflavin', 'mg'), 'niacin_ne': ('niacin_ne', 'mg NE'), 'vit_b6': ('vit_b6', 'mg'),
       'folate_dfe': ('folate_dfe', 'mcg'), 'b12': ('b12', 'mcg'), 'vit_c': ('vit_c', 'mg')}
out['athletes_optimum'] = {}
for i, r in rows.items():
    if r['section'] == 'athletes' and r['item'].startswith("athletes' or heavy labourers' optimum of "):
        name = r['item'].split(' optimum of ')[1]
        k, unit = KEY[name]
        v = number(i)
        if k == 'sodium':
            v *= 1000.0                                   # g -> mg, the model's unit
        out['athletes_optimum'][k] = {'value': v, 'unit_given': r['unit'], 'note': note(i)}
out['iodine_above_sufficiency_study'] = val('U190')

# contaminants (U191-U196)
lo, hi = [float(x) for x in re.findall(r'[0-9.]+', val('U191'))]
ars = dict((k.strip().lower(), float(v)) for k, v in re.findall(r'(\w+):\s*([0-9.]+)', val('U195')))
out['contaminants'] = {'mercury_fish_mg_per_kg': [lo, hi], 'mercury_tolerable_ug_per_kg_bw_day': number('U192'),
                       'cadmium_shellfish_offal_mg_per_kg': number('U193'), 'cadmium_tolerable_ug_per_kg_bw_week': number('U194'),
                       'arsenic_inorganic_mg_per_kg': {'rice brown': ars['brown'], 'rice polished': ars['white'], 'shellfish': ars['shellfish']},
                       'arsenic_inorganic_tolerable_ug_per_kg_bw_week': number('U196'),
                       'units_as_given': {rows[i]['item']: rows[i]['unit'] for i in ['U192', 'U194', 'U196']}}

json.dump(out, open(os.path.join(DATA, 'user_inputs.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
open(os.path.join(DATA, 'user_inputs.json'), 'a').write('\n')
print('wrote user_inputs.json:', len(out['satiety_index']), 'satiety values,', len(out['athletes_optimum']), 'athletes optima,', len(out['not_relevant']), 'not relevant')
