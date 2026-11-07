"""R44.9 (M91): a satiety formula fitted to Holt et al. 1995, applied to the game's food goods as eaten.

Holt SH et al., "A satiety index of common foods", Eur J Clin Nutr 1995 (PMID 7498104): 240 kcal servings of 38 foods,
white bread = 100. The abstract: SI rises with serving weight (r 0.66), water (0.64), fibre (0.46) and protein (0.37)
and falls with fat (-0.43). SI values as the Wikipedia "Satiety value" table reproduces them.

Model (per 240 kcal serving of the food as eaten, composition from USDA SR Legacy):
  ln(SI / 100) = a + b ln(W / W_bread) + c (protein share of energy) + d (fibre g per 100 kcal) + e (fat share of energy)
fitted by least squares on the Holt foods that have a clear USDA match. It prints the fit, each food's fitted value
and leave-one-out error, and the value for each game food good in its usual eaten form.
usage: satiety_fit.py <sr_legacy_csv_folder>
"""
import csv
import json
import math
import os
import sys

import numpy as np

HOLT = {  # Holt food: (SI, USDA fdc id of the eaten form)
    'white bread': (100, '174924'), 'potatoes (boiled)': (323, '170440'), 'fish (as cooked cod)': (225, '171956'),
    'beef steak': (176, '168633'), 'eggs (poached)': (150, '172186'), 'cheese (cheddar)': (146, '173414'),
    'white rice': (138, '168878'), 'brown rice': (132, '169704'), 'white pasta': (119, '169737'),
    'oranges': (202, '169097'), 'apples': (197, '171688'), 'bananas': (118, '173944'), 'grapes': (162, '174683'),
    'popcorn': (154, '167959'), 'peanuts': (84, '173806'), 'jellybeans': (118, '167991'), 'ice cream': (96, '167575'),
    'yogurt (low fat fruit)': (88, '173456'), 'croissant': (47, '174987'), 'cake': (65, '172704'),
    'doughnuts': (68, '172758'), 'cookies': (120, '172716'), 'crackers': (127, '174982'), 'potato chips': (91, '169677'),
    'lentils': (133, '172421'), 'baked beans': (168, '175182'), 'porridge': (209, '171675'),
    'wholemeal bread': (157, '172688'), 'grain bread (rye)': (154, '172684'),
}
GOODS = {  # game good: USDA fdc id of its usual eaten form
    'BONUS_WHEAT': ('172688', 'whole-wheat bread'), 'BONUS_RICE': ('168878', 'white rice, cooked'),
    'BONUS_CORN': ('171675', 'porridge stands in for maize porridge (oats)'), 'BONUS_POTATO': ('170440', 'boiled potatoes'),
    'BONUS_COW': ('168633', 'beef steak, broiled'), 'BONUS_PIG': ('167818', 'pork loin, raw'),
    'BONUS_SHEEP': ('172545', 'lamb, raw'), 'BONUS_DEER': ('173855', 'deer, raw'), 'BONUS_HORSE': ('175086', 'horse, raw'),
    'BONUS_FISH': ('175116', 'herring, raw'), 'BONUS_CLAM': ('174214', 'clam, raw'), 'BONUS_CRAB': ('174204', 'crab, raw'),
    'BONUS_SHRIMP': ('174210', 'shrimp, raw'), 'BONUS_WHALE': ('169797', 'beluga meat, raw'),
    'BONUS_DAIRY': ('172217', 'whole milk'), 'BONUS_BANANA': ('173944', 'banana'), 'BONUS_LEMON': ('167746', 'lemon'),
    'BONUS_APPLE': ('171688', 'apple'), 'BONUS_OLIVES': ('169094', 'ripe olives'), 'BONUS_SUGAR': ('169655', 'sugar'),
    'BONUS_WINE': ('173190', 'red wine'), 'BONUS_ALCOHOL': ('168746', 'beer'), 'REF_CHEESE': ('173414', 'cheddar'),
    'REF_BUTTER': ('173410', 'butter'),
}
NUT_IDS = {'1008': 'kcal', '1003': 'protein', '1004': 'fat', '1079': 'fibre', '1051': 'water'}


def load(folder, ids):
    val = {}
    for r in csv.DictReader(open(os.path.join(folder, 'food_nutrient.csv'), encoding='utf-8')):
        if r['fdc_id'] in ids and r['nutrient_id'] in NUT_IDS:
            val.setdefault(r['fdc_id'], {})[NUT_IDS[r['nutrient_id']]] = float(r['amount'])
    return val


def features(c, w_bread):
    kcal = c['kcal']
    w = 24000.0 / kcal                           # grams per 240 kcal
    return [1.0, math.log(w / w_bread), 4 * c.get('protein', 0) / kcal, 100 * c.get('fibre', 0) / kcal,
            9 * c.get('fat', 0) / kcal]


def main(folder):
    ids = {v[1] for v in HOLT.values()} | {v[0] for v in GOODS.values()}
    comp = load(folder, ids)
    w_bread = 24000.0 / comp['174924']['kcal']
    names = list(HOLT)
    X = np.array([features(comp[HOLT[n][1]], w_bread) for n in names])
    y = np.array([math.log(HOLT[n][0] / 100.0) for n in names])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    ss = ((y - pred) ** 2).sum()
    r2 = 1 - ss / ((y - y.mean()) ** 2).sum()
    print('fit on %d Holt foods: ln(SI/100) = %.3f + %.3f ln(W/W_bread) + %.3f protein share + %.3f fibre/100 kcal + %.3f fat share; R2 = %.2f'
          % (len(names), *beta, r2))
    print('| Holt food | SI measured | SI fitted | Leave-one-out | g per 240 kcal |')
    print('|---|---|---|---|---|')
    errs = []
    for i, n in enumerate(names):
        m = np.ones(len(names), bool)
        m[i] = False
        b, *_ = np.linalg.lstsq(X[m], y[m], rcond=None)
        loo = 100 * math.exp(X[i] @ b)
        errs.append(abs(math.log(loo / HOLT[n][0])))
        print('| %s | %d | %d | %d | %d |' % (n, HOLT[n][0], round(100 * math.exp(pred[i])), round(loo),
                                             round(24000.0 / comp[HOLT[n][1]]['kcal'])))
    print('median leave-one-out error: %d %%' % round(100 * (math.exp(sorted(errs)[len(errs) // 2]) - 1)))
    print('\n| Game good | Eaten form (USDA) | SI fitted | Holt measured |')
    print('|---|---|---|---|')
    measured = {'BONUS_POTATO': 323, 'BONUS_COW': 176, 'BONUS_RICE': 138, 'BONUS_APPLE': 197, 'BONUS_BANANA': 118,
                'BONUS_WHEAT': 157, 'REF_CHEESE': 146}
    out = {}
    for g, (fid, form) in GOODS.items():
        c = comp[fid]
        if not c.get('kcal'):
            continue
        si = 100 * math.exp(np.array(features(c, w_bread)) @ beta)
        out[g] = round(si)
        print('| %s | %s | %d | %s |' % (g.split('_', 1)[1].title(), form, round(si), measured.get(g, '-')))
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'satiety_fit.json')
    json.dump({'about': 'Satiety index (white bread 100) fitted to Holt 1995 by satiety_fit.py (R44.9); coefficients '
                        'for ln(SI/100) on [1, ln(W/W_bread), protein share, fibre per 100 kcal, fat share]',
               'coefficients': [round(float(b), 4) for b in beta], 'r2': round(float(r2), 3), 'goods': out},
              open(path, 'w'), indent=1)
    print('\nwrote', path)


if __name__ == '__main__':
    main(sys.argv[1])
