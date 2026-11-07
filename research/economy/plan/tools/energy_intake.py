"""R40.3 (M86): the energy and intake model, computed for test cases.

Per person and day (one abstracted adult, M84):
  BMR      = mean of FAO/WHO/UNU 2004 (18-30 y) men 15.057 W + 692.2 at 68.1 kg and women 14.818 W + 486.6 at
             58.5 kg (EFSA 2017 reference weights)
  PAL_work = sum over kinds of work of share x PAL (FAO 2004 Table 5.1: sedentary 1.53, active 1.76, vigorous 2.25)
  E_need   = BMR x PAL_work + caffeine (Dulloo 1989: up to 150 kcal a day at 6 x 100 mg)
  E_max    = BMR x 2.40 + caffeine (FAO 2004 Table 5.3: PAL above 2.40 is hard to keep up)
Intake: the city's available goods (g per head a day) are eaten in proportion, scaled by one factor t (0..1) found by
bisection, until the first limit binds:
  energy   sum kcal <= E_max
  protein  sum protein x 4 <= 35 % of E_max (danger level, Bilsborough and Mann 2006); 25 % reported as comfortable
  fat      per good: fat from one good <= FAT_PER_GOOD g (estimate from M86: 3 L milk ~ 98 g, a pound of 80/20 beef ~ 91 g)
  per good milk <= 3,000 g (M86)
  mass     sum wet weight of food <= MASS_MAX g (estimate from M86: a whole watermelon, fruit as watermelon)
Outcome:
  x        = E_in / E_need (food sufficiency for the population model)
  PAL_act  = clamp(E_in / BMR, 1.40, 2.40) (FAO 2004 Table 5.3 range); activity follows intake (M85)
  work     = physical work output factor = clamp((PAL_act - 1.40) / (PAL_work - 1.40), 0, 1 + WORK_BONUS_MAX)
  surplus  = available - eaten, to storage (D27 C), trade or animals
usage: energy_intake.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PROF = json.load(open(os.path.join(HERE, '..', '..', 'data', 'nutrient_profiles.json'), encoding='utf-8'))

BMR = ((15.057 * 68.1 + 692.2) + (14.818 * 58.5 + 486.6)) / 2      # 1,535 kcal
PAL = {'vigorous': 2.25, 'active': 1.76, 'sedentary': 1.53}
PAL_MIN, PAL_MAX = 1.40, 2.40
CAFFEINE_KCAL = 150
PROTEIN_MAX_SHARE = 0.35
FAT_PER_GOOD = 100          # estimate (M86 examples)
MILK_MAX = 3000             # M86
MASS_MAX = 6000             # estimate: a whole watermelon (M86, fruit as watermelon)
WORK_BONUS_MAX = 0.20       # estimate: extra physical output from eating above need, Fogel's energy for work

FOODS = {  # name: (good, form)
    'wheat bread': ('BONUS_WHEAT', 'grain'), 'pasta': ('REF_PASTA', 'cooked'), 'potato': ('BONUS_POTATO', 'boiled'),
    'milk': ('BONUS_DAIRY', 'milk'), 'cheese': ('BONUS_DAIRY', 'cheese'), 'butter': ('BONUS_DAIRY', 'butter'),
    'beef': ('REF_GROUND_BEEF', '80/20 raw'), 'deer': ('BONUS_DEER', 'meat'), 'cod': ('BONUS_FISH', 'cod'),
    'watermelon': ('REF_WATERMELON', 'raw'), 'apple': ('BONUS_APPLE', 'raw'), 'sugar': ('REF_SUGAR', 'granulated'),
    'cabbage': ('REF_CABBAGE', 'raw'), 'beer': ('BONUS_ALCOHOL', 'beer'),
}
DRINKS = {'milk', 'beer'}   # count against drink, not food mass


def row(name):
    g, f = FOODS[name]
    r = next(x for x in PROF['goods'][g] if x['form'] == f)
    return {k: (r[k] or 0.0) for k in ('kcal', 'protein', 'fat', 'water')}


def eat(avail, work, caffeine=0.0):
    e_need = BMR * sum(s * PAL[k] for k, s in work.items()) + CAFFEINE_KCAL * caffeine
    e_max = BMR * PAL_MAX + CAFFEINE_KCAL * caffeine
    caps = {}
    for n, a in avail.items():
        r = row(n)
        c = a
        if r['fat'] > 0:
            c = min(c, FAT_PER_GOOD * 100.0 / r['fat'])
        if n == 'milk':
            c = min(c, MILK_MAX)
        caps[n] = c

    def at(t):
        q = {n: min(t * avail[n], caps[n]) for n in avail}
        e = sum(q[n] * row(n)['kcal'] / 100 for n in q)
        p = sum(q[n] * row(n)['protein'] / 100 for n in q)
        m = sum(q[n] for n in q if n not in DRINKS)
        return q, e, p, m

    def ok(t):
        q, e, p, m = at(t)
        return e <= e_max and p * 4 <= PROTEIN_MAX_SHARE * e_max and m <= MASS_MAX

    lo, hi = 0.0, 1.0
    if ok(1.0):
        lo = 1.0
    else:
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    q, e, p, m = at(lo)
    binding = []
    if lo < 1.0:
        q2, e2, p2, m2 = at(min(1.0, lo + 1e-4))
        if e2 > e_max: binding.append('energy')
        if p2 * 4 > PROTEIN_MAX_SHARE * e_max: binding.append('protein')
        if m2 > MASS_MAX: binding.append('mass')
    binding += ['%s (%s)' % ('fat' if n != 'milk' or caps[n] < MILK_MAX else 'milk cap', n)
                for n in q if q[n] >= caps[n] - 1e-6 and caps[n] < avail[n]]
    x = e / e_need
    pal_act = max(PAL_MIN, min(PAL_MAX, e / BMR))
    pal_work = (e_need - CAFFEINE_KCAL * caffeine) / BMR
    workf = max(0.0, min(1 + WORK_BONUS_MAX, (pal_act - PAL_MIN) / (pal_work - PAL_MIN)))
    return dict(e_need=e_need, e_in=e, x=x, protein_share=p * 4 / e if e else 0, mass=m, pal_act=pal_act, work=workf,
                eaten=q, surplus={n: avail[n] - q[n] for n in avail}, binding=binding or ['none: ate what was there'])


CASES = [
    ('labourers, bread, milk, beef, cabbage, ample', {'wheat bread': 900, 'milk': 1000, 'beef': 200, 'cabbage': 300}, {'vigorous': 1.0}, 0),
    ('labourers, bread and beer only, scarce', {'wheat bread': 600, 'beer': 1500}, {'vigorous': 1.0}, 0),
    ('clerks, same ample food as the labourers', {'wheat bread': 900, 'milk': 1000, 'beef': 200, 'cabbage': 300}, {'sedentary': 1.0}, 0),
    ('clerks with coffee (6 cups)', {'wheat bread': 500, 'milk': 500, 'beef': 150, 'cabbage': 300}, {'sedentary': 1.0}, 1.0),
    ('potato labourers (boiled potatoes, milk)', {'potato': 5000, 'milk': 1500}, {'vigorous': 1.0}, 0),
    ('fruit only, abundant (fruit as watermelon)', {'watermelon': 12000}, {'active': 1.0}, 0),
    ('apples only, abundant (fruit as watermelon)', {'apple': 12000}, {'active': 1.0}, 0),
    ('lean game only, abundant (deer)', {'deer': 4000}, {'vigorous': 1.0}, 0),
    ('cheese only, abundant', {'cheese': 2000}, {'active': 1.0}, 0),
    ('beef 80/20 only, abundant', {'beef': 3000}, {'active': 1.0}, 0),
    ('pasta only, abundant', {'pasta': 6000}, {'active': 1.0}, 0),
    ('sugar added to a scarce bread diet', {'wheat bread': 500, 'sugar': 400}, {'active': 1.0}, 0),
    ('mixed city: half farm, quarter shop, quarter desk', {'wheat bread': 800, 'milk': 800, 'beef': 150, 'potato': 600, 'apple': 300}, {'vigorous': 0.5, 'active': 0.25, 'sedentary': 0.25}, 0),
]


def main():
    print('BMR (abstracted adult) %.0f kcal; PAL range %.2f-%.2f' % (BMR, PAL_MIN, PAL_MAX))
    print('| Case | Need kcal | Eaten kcal | x | Protein % of energy | Food mass g | PAL actual | Work factor | Binding limit | Left over (g) |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for name, avail, work, caf in CASES:
        r = eat(avail, work, caf)
        left = ', '.join('%s %d' % (n, v) for n, v in r['surplus'].items() if v >= 1) or '-'
        print('| %s | %d | %d | %.2f | %d | %d | %.2f | %.2f | %s | %s |' % (
            name, r['e_need'], r['e_in'], r['x'], round(100 * r['protein_share']), r['mass'], r['pal_act'], r['work'],
            '; '.join(r['binding']), left))


if __name__ == '__main__':
    main()
