"""R76.2-R76.4 (M126): sorts every row of the user's inputs file into EXACT or QUESTION, and writes the questions.

Input: <stem>.cells.csv from ods_extract.py (the lossless record) and data/user_inputs_template.csv (what was sent).
A row is EXACT only when all of these hold: its value cell is a number (float or percentage), its unit is the one sent
(or the user's own edit of it, which then defines the unit), it carries no note of the user's, and no question is
written for it below. Every other row is a QUESTION: free text that needs structure, a reading the user did not
state, a contradiction, or a value whose meaning depends on a choice made in translation. Edits the user made to the
template's columns (item, unit, needed_for, nuance) are listed for every row; they are the user's definitions.
Nothing is translated here; answers are applied by a later step, only as given.

Outputs (next to <out stem>): .questions.csv (one line per question, with empty answer columns) and .rows.csv (every
row: status, the parsed value and unit for EXACT rows, the edits).
usage: user_inputs_questions.py <stem>.cells.csv <out stem>
"""
import csv
import json
import os
import sys
from decimal import Decimal

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')

# Questions from reading every row (R75 audit, M126). Each: the question, and the options when they are known.
Q = {
 'U091': ('A bare good in your dessert list (e.g. BONUS_APPLE, BONUS_TEA): does it mean every form of that good, or only its default form (U146, U152)?',
          'every form | the default form only | other'),
 'U093': ('"Sugar first, Fruit second. Wine:wine and Alcohol third, Tea and Olives fourth": which goods are "Fruit"? Are grapes and raisins (BONUS_WINE, BONUS_WINE:raisins), dried apple and lemon juice fruit here? Does olive oil count with olives, and red wine (MEXT) with wine?',
          ''),
 'U094': ('10 kg of milk per kg of cheese: for every cheese, or for one kind (fresh or hard)? Which buildings or techniques make cheese (M122: an artisanal or industrial process)?', ''),
 'U095': ('20 kg of milk per kg of butter: which buildings or techniques make butter?', ''),
 'U096': ('"0.60kg" for grain to bread: is it 0.6 kg of bread from 1 kg of grain (the unit as sent), or 0.6 kg of grain per kg of bread? Which buildings or techniques bake bread?',
          '0.6 kg bread per kg grain | 0.6 kg grain per kg bread | other'),
 'U097': ('70 % of surplus milk turned into dairy products: how is it split between cheese and butter (and other products)? What counts as surplus: milk left after people drink their fill?', ''),
 'U098': ('You describe the rich city as a simulation case, not a triggered state. Are BUILDINGCLASS_METROPOLITAN_ESSENTIALS, population above 10, River Port and above and Market and above the definition of that case (all four together)?',
          'yes, all four together | other'),
 'U099': ('50 g of sugar per person per day (OECD-FAO): does it apply to every city or only to the rich-city case? Is it an amount people eat when sugar is available, or a ceiling? (Your sugar ceiling U127 is 300 g.)', ''),
 'U101': ('"By severity": which severity scale: below the minimum versus below the optimum (the four levels per nutrient), or the depth of the shortfall (e.g. intake as a share of the minimum)?', ''),
 'U102': ('Harms to health include tobacco, poisoning, pesticides and environmental pollutants. The record has no data on these yet: should they be researched now, or recorded for the game-effects stage?',
          'research now | record for the game-effects stage | other'),
 'U103': ('Strength: "logarithmic relationship to protein consumption and health": how does health enter (a factor on strength, a second term)? Fertility: by how much do excess energy and nutrients, animal foods, desserts and clams raise fertility, and which harmful substances lower it?', ''),
 'U104': ('Excess energy and nutrition boost commerce: by how much (e.g. % commerce per unit of excess), and what counts as excess (above the optimum, above the need)?', ''),
 'U105': ('Strength: 30 % at 50 g protein, 80 % at 1.6 g per kg body weight. Is 200 % reached exactly at the liver limit, and is that limit your fixed 288 g or the urea capacity that scales with body weight (4.06 g/kg: 284 g at 70 kg)? Which logarithm between the points (straight in ln(protein) through the three points)?', ''),
 'U106': ('Starving to population: "decline per turn or a negative growth rate; possible mass die-off": which one, and what triggers a mass die-off (how long or how deep the starving)?', ''),
 'U107': ('IQ from iodine: at which iodine intake does IQ reach the floor of 70? Is 115 reached at 1 mg? What shape between the points (straight in log10 of iodine)? "Every point above and below 100 has an exponentially larger effect on output": which function (e.g. output x e^(k (IQ-100)), and k)?', ''),
 'U108': ('Whale shares 30 / 40 / 2 / 12 %: of live weight or carcass weight? Which organs are the "other organs eaten" (12 %)?', ''),
 'U117': ('Cow 60 % meat, 20 % fat, 2.5 % organs: which organs, and in what split (liver, heart, kidneys, others)? The old split 1.12 : 0.37 : 0.18 came from the shares you replaced.', ''),
 'U118': ('Sheep 2.5 % organs: which organs and in what split?', ''),
 'U119': ('Deer 3 % organs: which organs and in what split?', ''),
 'U120': ('Horse 2.5 % organs: which organs and in what split?', ''),
 'U121': ('"Lemon cider: 1L (equivalent to 30g)": what is lemon cider (fermented lemon juice, a lemon drink with water and sugar)? Does 1 L of it hold the lemon of 30 g of fruit, so that the 30 g ceiling holds for lemons in any form?', ''),
 'U122': ('Meat: median 150 g, upper end 400 g, maximum 1 kg, all livestock and deer together. Which one is the ceiling on what a person eats (the maximum, 1 kg)? Is the median a typical intake to use somewhere? Does "meat" mean the whole animal as eaten (with fat and organs) or lean meat only? You added "an Indian wrote this" to my note: what should I take from it?', ''),
 'U135': ('Whale 800 g: of the whole whale as eaten (meat, blubber, organs) or of meat only? Clams 800 g (U134): raw, without shell?', ''),
 'U136': ('Bread: whole-wheat or white flour, and which extraction? "Ideally fermented": leavened bread (yeast or sourdough)?', ''),
 'U138': ('Maize "Grain", also made into flour and bread: which record: cooked whole grain (e.g. boiled or polenta), flour, or cornbread?', ''),
 'U145': ('Milk as the default form: raw or pasteurised? (U163: raw milk is digestible by everyone.)', 'raw | pasteurised | depends on the era or culture'),
 'U147': ('Lemon "juice", "Cider in particular": which composition record: lemon juice (USDA 167747), or a lemon cider record (none held yet)?', ''),
 'U152': ('Tea "depends on the culture, brewed", herbal teas grouped (mountain tea, thyme, sage): is one record for brewed herbal tea (USDA 173232, herbs other than chamomile) acceptable for the group, or should each culture have its own?', ''),
 'U154': ('Fish categories to composition records: freshwater fish, small pelagic, large pelagic, demersal, salmonids, other marine fish. Which species stands for each (my choices were pond smelt eaten whole, whole herring, bluefin tuna, cod as eaten, wild salmon, Atlantic mackerel)?', ''),
 'U156': ('"Only small fish (cooked or fermented)": which of the six categories are small fish eaten with bones (freshwater, small pelagic)?', ''),
 'U157': ('The four work classes (manual labour 2.0, sedentary 1.5, soldier 2.5, slaves in quarries or mines 3.0): how does a city\'s population divide between them (worked tiles, specialists, units)?', ''),
 'U161': ('Body weight "depends on food composition, can range from 50kg to 120kg": by which rule (e.g. with protein or energy intake), and at what weight before any food effect?', ''),
 'U163': ('Lactase persistence by culture: which game civilizations belong to which group?', ''),
 'U168': ('Spoilage classes: which goods are "cured, salted, fermented" (cheese, cured meat, salted fish: goods of the game?), which "dried" (tea, coffee, sugar, salt, dried fruit), which "root and grains", and is everything else "others" (90 %)?', ''),
 'U169': ('In the nuance of the dried class you wrote "estimate for dried fruit": is 10 % an estimate for dried fruit only, with tea leaves and coffee beans in the same class?', ''),
 'U170': ('Canned 2 % a year: the plan has no canned good (the Cannery lengthens shelf life). Keep 2 % as what the Cannery brings goods to, or drop it?', 'Cannery brings goods to 2 % | drop | other'),
 'U171': ('Root and grains 50 % a year: also for grain in a granary (the earlier figure was 5 % in traditional storage, FAO)?', ''),
 'U173': ('Protein 300 g for a 140 kg wrestler: for other body weights, scale by weight (300/140 g per kg), or 300 g for everyone?', 'scale by body weight | 300 g for everyone | other'),
 'U191': ('Mercury 0.01 to 0.20 mg per kg in fish: which fish at the low end and which at the high end (e.g. small pelagic low, large pelagic high)?', ''),
 'U194': ('Cadmium 5: the item says "tolerable daily intake" but the unit says "per week". Which?', 'per day | per week'),
 'U196': ('Inorganic arsenic 0.06: the item says "tolerable daily intake" but the unit says "per week". Which?', 'per day | per week'),
}
# Rows the user answered elsewhere, or marked: kept as given, no question.
ANSWERED = {'U089': 'M122: bread-equivalent fullness', 'U090': 'M123: multiply the drink indices by 0.8',
            'U100': 'the user: needs to be discussed (a discussion, not a question here)',
            'U162': 'not relevant', 'U164': 'not relevant', 'U165': 'not relevant', 'U166': 'not relevant', 'U167': 'not relevant',
            'U190': 'not relevant', 'U197': 'not relevant'}
# Rows whose note gives a source or names the unit: the number is exact, the note is kept verbatim.
NOTE_OK = {'U108': 'source', 'U109': 'source', 'U110': 'source', 'U111': 'source', 'U129': 'unit: 2000 g = 2 L of wine',
           'U131': 'context of the ceiling', 'U132': 'unit: brewed tea, litres', 'U133': 'unit: brewed coffee, litres',
           'U168': 'the user: spoilage rate', 'U173': 'the person the value is for'}
# Rows whose text is complete as it stands (a list or a statement to keep verbatim).
VERBATIM = {'U092': '100 % of the need (percentage cell)', 'U137': 'Polished', 'U139': 'Boiled', 'U140': 'whole animal as eaten',
            'U141': 'whole animal as eaten', 'U142': 'whole animal as eaten', 'U143': 'raw', 'U144': 'whole animal as eaten',
            'U146': 'raw', 'U148': 'raw', 'U149': 'oil', 'U150': 'brown', 'U151': 'grapes', 'U153': 'table salt',
            'U195': 'brown 0.15, white 0.10, shellfish 0.01 mg per kg', 'U192': '0.3 ug per kg body weight per day (item: daily)',
            'U191': None}


def main():
    cells = list(csv.DictReader(open(sys.argv[1], encoding='utf-8')))
    out = sys.argv[2]
    rows = {}
    head = {int(c['col']): c['shown'] for c in cells if c['row'] == '1'}
    for c in cells:
        r = int(c['row'])
        if r == 1:
            continue
        rows.setdefault(r, {})[head[int(c['col'])]] = c
    tmpl = {t['id']: t for t in csv.DictReader(open(os.path.join(DATA, 'user_inputs_template.csv'), encoding='utf-8'))}
    qs, allrows = [], []
    for r in sorted(rows):
        c = rows[r]
        g = lambda k: c[k]['shown'] if k in c else ''
        i = g('id')
        t = tmpl[i]
        edits = ['%s: %r -> %r' % (k, t.get(k, ''), g(k)) for k in ('section', 'item', 'unit', 'needed_for', 'nuance') if (t.get(k) or '') != g(k)]
        v = c.get('your_value')
        num = v is not None and v['type'] in ('float', 'percentage')
        item = g('item')
        question, options = None, ''
        if i in Q:
            question, options = Q[i]
        elif item.startswith('satiety index of ') and ':' not in item[17:] and not item[17:].startswith('REF_') \
                and not g('your_value').startswith('(not relevant)'):
            good = item[17:]
            prof = json.load(open(os.path.join(DATA, 'nutrient_profiles.json'), encoding='utf-8'))
            first = prof['goods'][good][0]
            question = ('Your satiety index %s for %s (a row without a form): which form is it for? In the sheet sent, the row stood for '
                        'the good\'s first form in the composition file, %s (USDA %s), but the sheet did not say so.%s' % (
                            g('your_value'), good, first['form'], first['fdc_id'],
                            (' The value then shown, %s, was %s.' % (t['current_value'], t['current_source'])) if t['current_value'] else ''))
            options = 'the first USDA form | your default form (forms section) | the good in general | other'
        if g('your_value').startswith('(not relevant)'):
            ANSWERED.setdefault(i, 'not relevant (the user); for potato the boiled form, 180 (M123)')
        status = 'QUESTION' if question else ('ANSWERED' if i in ANSWERED else ('EXACT' if num and (not g('your_nuance') or i in NOTE_OK) else
                 ('VERBATIM' if i in VERBATIM or (not num and g('your_value') and not g('your_nuance')) else 'QUESTION')))
        if status == 'QUESTION' and not question:
            question = 'The value %r with your note %r: how should it be read?' % (g('your_value'), g('your_nuance'))
        parsed = ''
        if status == 'EXACT':
            d = Decimal(v['value'])
            x = d * 100 if v['type'] == 'percentage' else d
            x = format(x, 'f'); x = x.rstrip('0').rstrip('.') if '.' in x else x
            u = g('unit')
            parsed = x + (' %' if v['type'] == 'percentage' and not u.startswith('%') else '') + ' ' + u
            if i in NOTE_OK:
                parsed += ' [note kept: %s]' % NOTE_OK[i]
        allrows.append({'id': i, 'status': status, 'item': item, 'unit': g('unit'), 'your_value': g('your_value'), 'your_nuance': g('your_nuance'),
                        'parsed': parsed, 'answered_by': ANSWERED.get(i, ''), 'template_edits': ' | '.join(edits)})
        if question:
            qs.append({'q': 'Q%03d' % (len(qs) + 1), 'id': i, 'item': item, 'your_value': g('your_value'), 'your_nuance': g('your_nuance'),
                       'question': question, 'options': options, 'answer': '', 'answer_note': ''})
    for name, data in (('.rows.csv', allrows), ('.questions.csv', qs)):
        with open(out + name, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader()
            w.writerows(data)
    n = {}
    for a in allrows:
        n[a['status']] = n.get(a['status'], 0) + 1
    print(n, '|', len(qs), 'questions')


if __name__ == '__main__':
    main()
