"""PR.F8.T4: the tile formula and the population model in Python, checked against England and Wales about 1300.

A computed check (CLAUDE.md rule 9). The C++ steps (PR.F7, FD.F2, FD.F3) are compared with these numbers.
Inputs, each with its source (tile_output.md, open_questions.md sections 3-4, 7):
  arable 10.7 million acres, 60 % under grain              Campbell, as cited (tile_output.md)
  wheat 0.385 t/ha net of seed                              Pretty 1990, Winchester manors
  people about 4.75 million (4.5-5)                         England about 1300 (population_model.md)
  working share 40 %, of whom 80 % in farming               D23 estimate; Allen/Clark farm shares about 1300
  3 ha per worker at the Agriculture stage                  Columella's labour days (proposals.json production)
  grain up to 80 % of a worker's calories                   Food in Medieval England (Oxford)
  satiety per kg of wheat as stored                         research/economy/data/nutrition.json via food_values_edits.values
  s = 2,600 satiety units a day, r = 1 % a year             open_questions.md section 7
usage: check_england1300.py      (exit status 1 if a check fails)"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'connector'))
from food_values_edits import values, DATA   # the same numbers the XML gets

ACRE_HA = 0.404686
ARABLE_HA = 10.7e6 * ACRE_HA
GRAIN_SHARE = 0.60
NET_T_HA = 0.385
PEOPLE = 4.75e6
WORK, FARM = 0.40, 0.80
HA_PER_WORKER = 3.0
GRAIN_KCAL_SHARE = 0.80
S_PER_DAY = 2600
R_PER_MILLE = 10

fails = []
def check(name, value, lo, hi, unit=''):
    ok = lo <= value <= hi
    print('%-46s %12.3f %-10s [%g, %g] %s' % (name, value, unit, lo, hi, 'ok' if ok else 'FAIL'))
    if not ok: fails.append(name)

d = json.load(open(DATA)); v = values(d)
wheat = d['goods']['BONUS_WHEAT']

# 1. the tile formula, England-wide: area worked = min(usable arable, workers x ha per worker)
workers = PEOPLE * WORK * FARM
worked = min(ARABLE_HA, workers * HA_PER_WORKER)
check('ha per farm worker (arable / workers)', ARABLE_HA / workers, 2.7, 3.4, 'ha')
check('labour-limited area / arable', workers * HA_PER_WORKER / ARABLE_HA, 0.9, 1.1)
grain_t = worked * GRAIN_SHARE * NET_T_HA
check('net grain, million t', grain_t / 1e6, 0.95, 1.05, 'Mt')

# 2. calories and satiety per head a day
kcal_raw = grain_t * 1000 * wheat['kcal'] * 10 / PEOPLE / 365
check('grain kcal per head a day, as harvested', kcal_raw, 1850, 2000, 'kcal')
kcal_milled = kcal_raw * wheat['edible']
print('%-46s %12.0f kcal  (at %.0f %% extraction)' % ('grain kcal per head a day, after milling', kcal_milled, 100 * wheat['edible']))
total_kcal = kcal_raw / GRAIN_KCAL_SHARE
check('total kcal per head a day (grain 80 %)', total_kcal, 2300, 2500, 'kcal')

# satiety: grain at its factor (milling loss included), the rest of the diet at an animal-food factor
grain_sat = grain_t * 1000 * v['BONUS_WHEAT']['satiety_per_kg'] / PEOPLE / 365
other_kcal = total_kcal - kcal_raw
f_animal = (v['BONUS_COW']['factor'] + v['BONUS_DAIRY']['factor'] + v['BONUS_FISH']['factor']) / 3
sat_total = grain_sat + other_kcal * f_animal
print('%-46s %12.0f        (grain %.0f + other %.0f kcal x %.2f)' % ('satiety per head a day', sat_total, grain_sat, other_kcal, f_animal))

# 3. the population model: K = F / s, logistic years in integers (the C++ step: N += N r (K-N) / (K 1000))
F_day = sat_total * PEOPLE
K = int(F_day / S_PER_DAY)
check('N / K at s = %d' % S_PER_DAY, PEOPLE / K, 0.85, 1.15)
N = 1000
for year in range(1, 2001):
    N = N + N * R_PER_MILLE * (K - N) // (K * 1000)        # Python ints are unbounded; in C++ this is __int64
    if year in (200, 600, 1000, 2000):
        print('%-46s %12d  (K %d)' % ('people after %d years from 1,000 at r = 1 %%' % year, N, K))
check('people after 2,000 years / K', N / K, 0.95, 1.0)

print('FAILED: ' + ', '.join(fails) if fails else 'all checks pass')
sys.exit(1 if fails else 0)
