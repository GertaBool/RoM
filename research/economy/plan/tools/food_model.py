"""The food model, version 4 (M101): first principles, few variables, exact solution.

SPECIFICATION: research/economy/food_model_spec.md (version 4) is the authority. This file is the reference
implementation: it solves the three-stage lexicographic program (stage 1 nutrition adequacy, stage 2 well-being,
stage 3 even use of supply) exactly as linear programs (scipy.optimize.linprog, HiGHS), and reports the outcomes and
the scarcity values (shadow prices of the stocks). Equation numbers refer to the specification.
usage: food_model.py
"""
import json
import math
import os

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', '..', 'data')
NUT = json.load(open(os.path.join(DATA, 'nutrition.json'), encoding='utf-8'))
PROF = json.load(open(os.path.join(DATA, 'nutrient_profiles.json'), encoding='utf-8'))
NEED = json.load(open(os.path.join(DATA, 'nutrient_needs.json'), encoding='utf-8'))
SFIT = json.load(open(os.path.join(DATA, 'satiety_fit.json'), encoding='utf-8'))

# ---------------- scalars (specification section 3b) ----------------
B = ((15.057 * 68.1 + 692.2) + (14.818 * 58.5 + 486.6)) / 2      # basal rate, kcal/(p d); FAO 2004, EFSA weights
LAMBDA = {'vigorous': 2.25, 'active': 1.76, 'sedentary': 1.53}    # FAO 2004 Table 5.1
L_MIN, L_MAX = 1.40, 2.40                                         # FAO 2004 Table 5.3
KAPPA, GAMMA = 150.0, 600.0                                       # caffeine: kcal at mg (Dulloo 1989)
SIGMA_BAR = 1.36                                                  # mean Holt index / 100 (Holt 1995)
P_ABS = 3.6 * 63.3                                                # protein ceiling g/(p d): liver capacity (Bilsborough and Mann 2006) x EFSA mean weight
Q_FRUIT = 4518.0                                                  # all fruit g/(p d): one watermelon (USDA portion)
W_NEED = 2250.0                                                   # total water ml/(p d) (EFSA 2010)
M_E = 100.0                                                       # the unit of diminishing returns: 100 kcal of a good
SEGMENTS = [0.5, 1, 2, 3, 5, 8, 12, 20, 30]                       # breakpoints (units of 100 kcal) of ln(1+n), stage 2

# ---------------- sets (section 2) ----------------
DRINKS = {'BONUS_DAIRY', 'BONUS_WINE', 'BONUS_ALCOHOL', 'BONUS_TEA', 'BONUS_COFFEE'}
BREWED = {'BONUS_TEA': (43.0, 200.0), 'BONUS_COFFEE': (15.0, 600.0)}  # litres per kg, mg caffeine per litre (MEXT)
FRUIT = {'BONUS_BANANA', 'BONUS_LEMON', 'BONUS_APPLE'}
STAPLES = {'BONUS_WHEAT', 'BONUS_RICE', 'BONUS_CORN', 'BONUS_POTATO', 'BONUS_SALT'}
WELLBEING = set(NUT['goods']) - STAPLES - set(['BONUS_TEA', 'BONUS_COFFEE'])
#   W: every food good except the plain staples and salt; tea and coffee are well-being goods taken in stage 0
#   (caffeine); tobacco joins W when it has data
HARMFUL = {'BONUS_WINE': 10.6, 'BONUS_ALCOHOL': 3.9}              # alcohol g per 100 g (USDA SR Legacy); tobacco to add
ANIMAL = set(NUT['animal_goods'])
MICRO = ['vit_c', 'vit_a_rae', 'thiamin', 'niacin', 'folate_dfe', 'b12', 'iron', 'zinc', 'calcium', 'iodine',
         'potassium', 'sodium']
ADEQ = ['fullness', 'energy', 'protein'] + MICRO                  # the 15 components of adequacy

# ---------------- per-good data (section 3a) ----------------
CEIL_SPECIFIC = {'BONUS_DAIRY': 3000.0, 'BONUS_LEMON': 116.0}     # the user (M86); estimate (M92)
FAT_PER_GOOD = 250.0                                              # the user (M93)
HOLT = {'BONUS_POTATO': 323, 'BONUS_COW': 176, 'BONUS_RICE': 138, 'BONUS_APPLE': 197, 'BONUS_BANANA': 118,
        'BONUS_WHEAT': 157, 'BONUS_LEMON': 202}
DRINK_FULLNESS = 0.5                                              # estimate (liquid calories satiate less, PMID 14649371)
PROFILE_FORM = {'BONUS_WHEAT': 'grain', 'BONUS_RICE': 'brown', 'BONUS_CORN': 'grain', 'BONUS_POTATO': 'boiled',
                'BONUS_COW': 'meat', 'BONUS_PIG': 'meat', 'BONUS_SHEEP': 'meat', 'BONUS_DEER': 'meat',
                'BONUS_HORSE': 'meat', 'BONUS_FISH': 'cod', 'BONUS_CLAM': 'raw', 'BONUS_CRAB': 'raw',
                'BONUS_SHRIMP': 'raw', 'BONUS_WHALE': 'meat', 'BONUS_DAIRY': 'milk', 'BONUS_BANANA': 'raw',
                'BONUS_LEMON': 'raw', 'BONUS_APPLE': 'raw', 'BONUS_OLIVES': 'olives', 'BONUS_SUGAR': 'brown',
                'BONUS_WINE': 'wine', 'BONUS_ALCOHOL': 'beer', 'BONUS_TEA': 'green, brewed', 'BONUS_SALT': 'table salt'}
MEXT_FORM = {'BONUS_WHEAT': 'soft flour', 'BONUS_RICE': 'polished', 'BONUS_CORN': 'grain', 'BONUS_POTATO': 'raw',
             'BONUS_COW': 'shoulder', 'BONUS_PIG': 'loin', 'BONUS_FISH': 'cod', 'BONUS_CLAM': 'asari clam',
             'BONUS_WHALE': 'red meat', 'BONUS_DAIRY': 'milk', 'BONUS_LEMON': 'whole fruit', 'BONUS_APPLE': 'with skin',
             'BONUS_BANANA': 'raw', 'BONUS_WINE': 'red wine', 'BONUS_TEA': 'sencha infusion', 'BONUS_SALT': 'salt',
             'BONUS_SUGAR': 'white sugar'}
WHOLE_FISH = [(0.50, dict(kcal=195, protein=16.39, fat=13.88, vit_a_rae=32)),
              (0.45, dict(kcal=82, protein=17.81, fat=0.67, vit_a_rae=12)),
              (0.05, dict(kcal=424, protein=5.6, fat=42.0, vit_a_rae=30000 * 0.42))]
WF = {k: sum(s * c.get(k, 0) for s, c in WHOLE_FISH) for k in ('kcal', 'protein', 'fat', 'vit_a_rae')}
WHOLE_ANIMAL = {'BONUS_COW': [('meat', 0.97), ('liver', 0.03)], 'BONUS_PIG': [('meat', 0.97), ('liver', 0.03)]}
# bioavailability b_gi: iron absorbed 18 % from animal, 10 % from plant foods, against EFSA's assumed 16 %
# (FAO/WHO 2004; Hurrell and Egli 2010); maize niacin one third available (Carpenter 1983)
B_IRON_ANIMAL, B_IRON_PLANT, B_NIACIN_MAIZE = 0.18 / 0.16, 0.10 / 0.16, 1 / 3
SPOIL = {k: v['value'] for k, v in NUT['spoilage_per_year_percent'].items()}


def good(g):
    v = dict(NUT['goods'][g])
    if g == 'BONUS_FISH':
        v.update(kcal=WF['kcal'], protein=WF['protein'], fat=WF['fat'], edible=0.85)
    return v


def micro(g):
    f = PROFILE_FORM.get(g)
    if not f:
        return None
    if g in WHOLE_ANIMAL:
        parts = [(next(x for x in PROF['goods'][g] if x['form'] == pf), sh) for pf, sh in WHOLE_ANIMAL[g]]
        r = {k: sum((u.get(k) or 0.0) * sh for u, sh in parts) for k in MICRO + ['kcal', 'water']}
    else:
        u = next(x for x in PROF['goods'][g] if x['form'] == f)
        r = {k: (u.get(k) or 0.0) for k in MICRO + ['kcal', 'water']}
    m = next((x for x in PROF.get('mext', {}).get(g, []) if x['form'] == MEXT_FORM.get(g)), None)
    r['iodine'] = (m['iodine'] or 0.0) if m else 0.0
    if g == 'BONUS_TEA' and m:
        r['vit_c'] = m['vit_c'] or 0.0
    if g == 'BONUS_FISH':
        r['vit_a_rae'] = WF['vit_a_rae']
    return r


def sigma(g):
    s = HOLT.get(g, SFIT['goods'].get(g, 100)) / 100.0
    return s * (DRINK_FULLNESS if g in DRINKS else 1.0)


def bio(g, i):
    if i == 'iron':
        return B_IRON_ANIMAL if g in ANIMAL else B_IRON_PLANT
    if i == 'niacin' and g == 'BONUS_CORN':
        return B_NIACIN_MAIZE
    return 1.0


def row(g):
    """per gram as stored: energy, protein, digestible protein, fat, fullness, nutrients (bioavailable), water"""
    v, m = good(g), micro(g)
    ed = v['edible'] if g != 'BONUS_SALT' else 1.0
    dq = v['diaas'] if v.get('diaas') is not None else (1.0 if g in ANIMAL else 0.44)
    r = dict(e=v['kcal'] * ed / 100.0, p=v['protein'] * ed / 100.0, pd=v['protein'] * ed / 100.0 * min(dq, 1.0),
             f=v['fat'] * ed / 100.0, ed=ed)
    r['F'] = sigma(g) * r['e'] if r['e'] else 0.0
    r['n'] = {i: (ed / 100.0) * bio(g, i) * (m[i] if m else 0.0) for i in MICRO}
    r['water'] = (ed / 100.0) * (m['water'] if m else 0.0)
    return r


def R_e(g):
    v = good(g)
    return v['kcal'] * (v['edible'] if g != 'BONUS_SALT' else 1.0) / 100.0


def solve(people, work, stocks):
    avail = {g: t * 1e6 / (365.0 * people) for g, t in stocks.items()}           # (1)
    q0, caf = {}, 0.0                                                             # stage 0: brewed drinks (2)
    for g, (lpk, mgl) in BREWED.items():
        if g in avail:
            q0[g] = min(avail[g], max(0.0, GAMMA - caf) / (lpk * mgl / 1000.0))
            caf += q0[g] * lpk * mgl / 1000.0
    c = min(1.0, caf / GAMMA)
    lam_w = sum(s * LAMBDA[k] for k, s in work.items())                           # (3)
    e_need = B * lam_w + KAPPA * c                                                 # (4)
    e_max = B * L_MAX + KAPPA * c                                                  # (5)
    f_fed, f_max = SIGMA_BAR * e_need, SIGMA_BAR * e_max                           # (6)
    need = {'fullness': f_fed, 'energy': e_need, 'protein': NEED['needs']['protein']['value']}
    need.update({i: NEED['needs'][i]['value'] for i in MICRO})
    const = {i: 0.0 for i in ADEQ}                                                 # nutrients of the brewed drinks
    for g, x in q0.items():
        m = micro(g)
        if m:
            for i in MICRO:
                const[i] += x * BREWED[g][0] / 100.0 * m[i]
    goods = [g for g in avail if g not in BREWED]
    R = {g: row(g) for g in goods}
    ub = {}
    for g in goods:                                                                # (7)
        u = avail[g]
        if R[g]['f'] > 0:
            u = min(u, FAT_PER_GOOD / R[g]['f'])
        if g in CEIL_SPECIFIC:
            u = min(u, CEIL_SPECIFIC[g])
        ub[g] = u
    nG, nI = len(goods), len(ADEQ)
    W = [g for g in goods if g in WELLBEING and R_e(g) > 0]
    nS = len(SEGMENTS)
    nV = nG + nI + len(W) * nS
    iq = {g: k for k, g in enumerate(goods)}
    iy = {i: nG + k for k, i in enumerate(ADEQ)}
    isg = {(g, k): nG + nI + w * nS + k for w, g in enumerate(W) for k in range(nS)}

    def coef(g, i):
        if i == 'fullness':
            return R[g]['F']
        if i == 'energy':
            return R[g]['e']
        if i == 'protein':
            return R[g]['pd']
        return R[g]['n'][i]

    A_ub, b_ub = [], []
    for i in ADEQ:                                                                 # y_i <= c_i(q)
        a = np.zeros(nV)
        a[iy[i]] = 1.0
        for g in goods:
            a[iq[g]] = -coef(g, i) / need[i]
        A_ub.append(a)
        b_ub.append(const[i] / need[i])
    for vec, cap in ((lambda g: R[g]['F'], f_max), (lambda g: R[g]['e'], e_max), (lambda g: R[g]['p'], P_ABS),
                     (lambda g: R[g]['ed'] if g in FRUIT else 0.0, Q_FRUIT)):     # (8)-(11)
        a = np.zeros(nV)
        for g in goods:
            a[iq[g]] = vec(g)
        A_ub.append(a)
        b_ub.append(cap)
    A_eq, b_eq = [], []
    for g in W:                                                                    # units of 100 kcal = sum of segments
        a = np.zeros(nV)
        a[iq[g]] = R[g]['e'] / M_E
        for k in range(nS):
            a[isg[(g, k)]] = -1.0
        A_eq.append(a)
        b_eq.append(0.0)
    bounds = [(0, ub[g]) for g in goods] + [(0, 1)] * nI
    for g in W:
        prev = 0.0
        for k, bp in enumerate(SEGMENTS):
            bounds.append((0, (bp - prev) if k < nS - 1 else None))
            prev = bp
    slopes, prev = [], 0.0
    for bp in SEGMENTS:
        slopes.append((math.log(1 + bp) - math.log(1 + prev)) / (bp - prev))
        prev = bp
    A_ub, b_ub = np.array(A_ub), np.array(b_ub)
    A_eq = np.array(A_eq) if A_eq else None
    b_eq = np.array(b_eq) if b_eq else None

    def lp(cvec, extra=None, extra_b=None):
        Au, bu = A_ub, b_ub
        if extra is not None:
            Au, bu = np.vstack([A_ub] + extra), np.concatenate([b_ub, extra_b])
        r = linprog(cvec, A_ub=Au, b_ub=bu, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        assert r.status == 0, r.message
        return r

    c1 = np.zeros(nV)                                                              # stage 1 (12)
    for i in ADEQ:
        c1[iy[i]] = -1.0 / nI
    r1 = lp(c1)
    a_star = -r1.fun
    c2 = np.zeros(nV)                                                              # stage 2 (13)
    for g in W:
        for k in range(nS):
            c2[isg[(g, k)]] = -slopes[k]
    keepA = [c1.reshape(1, -1)]
    r2 = lp(c2, keepA, np.array([-a_star + 1e-7]))
    psi_star = -r2.fun
    c3 = np.zeros(nV)                                                              # stage 3 (14)
    for g in goods:
        c3[iq[g]] = 1.0 / avail[g] if avail[g] > 0 else 0.0
    r3 = lp(c3, keepA + [c2.reshape(1, -1)], np.array([-a_star + 1e-7, -psi_star + 1e-7]))
    q = {g: r3.x[iq[g]] for g in goods}
    q.update(q0)
    sv1 = {g: max(0.0, -r1.upper.marginals[iq[g]]) if ub[g] == avail[g] else 0.0 for g in goods}
    sv2 = {g: max(0.0, -r2.upper.marginals[iq[g]]) if ub[g] == avail[g] else 0.0 for g in goods}
    E = sum(R[g]['e'] * q[g] for g in goods)                                       # outcomes (15)-(22)
    F = sum(R[g]['F'] * q[g] for g in goods)
    P = sum(R[g]['p'] * q[g] for g in goods)
    cov = {i: (sum(coef(g, i) * q[g] for g in goods) + const[i]) / need[i] for i in ADEQ}
    A = sum(min(1.0, cov[i]) for i in ADEQ) / nI
    psi = sum(math.log(1 + R[g]['e'] * q[g] / M_E) for g in W)
    alcohol = sum(q[g] * good(g)['edible'] * HARMFUL[g] / 100.0 for g in HARMFUL if g in q)
    w_food = sum(R[g]['water'] * q[g] for g in goods if g not in DRINKS)
    w_drink = sum(q[g] * R[g]['ed'] * (good(g).get('hydration') or 1.0) for g in goods if g in DRINKS)
    w_drink += sum(q0[g] * BREWED[g][0] for g in q0)
    w_plain = max(0.0, W_NEED - w_food - w_drink)
    work = min(1.0, E / e_need)                                                     # (20)
    used = {g: q.get(g, 0.0) * 365 * people / 1e6 for g in stocks}
    left = {g: stocks[g] - used[g] for g in stocks}
    spoiled = {g: left[g] * SPOIL[NUT['goods'][g]['form']] / 100.0 for g in stocks}
    return dict(avail=avail, ub=ub, q=q, e_need=e_need, e_max=e_max, f_fed=f_fed, f_max=f_max, caf=caf, lam_w=lam_w,
                A_star=a_star, psi_star=psi_star, E=E, F=F, P=P, x=E / e_need, fed=F / f_fed, cov=cov, A=A, psi=psi,
                alcohol=alcohol, w_food=w_food, w_drink=w_drink, w_plain=w_plain, work=work, used=used, left=left,
                spoiled=spoiled, sv1=sv1, sv2=sv2, R=R)


CITIES = [
    ('A. Market town, 20,000', 20000, {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_WHEAT': 7000, 'BONUS_DAIRY': 4000, 'BONUS_PIG': 600, 'BONUS_APPLE': 1500, 'BONUS_ALCOHOL': 3000, 'BONUS_SALT': 60}),
    ('B. Coastal city, 200,000', 200000, {'vigorous': 0.5, 'active': 0.3, 'sedentary': 0.2},
     {'BONUS_RICE': 75000, 'BONUS_FISH': 35000, 'BONUS_TEA': 600, 'BONUS_BANANA': 15000, 'BONUS_SALT': 500}),
    ('C. Industrial city, 1,000,000', 1000000, {'vigorous': 0.4, 'active': 0.3, 'sedentary': 0.3},
     {'BONUS_WHEAT': 220000, 'BONUS_POTATO': 600000, 'BONUS_SUGAR': 30000, 'BONUS_DAIRY': 250000, 'BONUS_COW': 40000,
      'BONUS_COFFEE': 3000, 'BONUS_SALT': 3000}),
    ('E. Rich city, 100,000', 100000, {'vigorous': 0.2, 'active': 0.4, 'sedentary': 0.4},
     {'BONUS_COW': 20000, 'BONUS_DAIRY': 150000, 'BONUS_POTATO': 60000, 'BONUS_WHEAT': 40000, 'BONUS_APPLE': 20000,
      'BONUS_SUGAR': 8000, 'BONUS_WINE': 15000, 'BONUS_TEA': 400, 'BONUS_SALT': 500}),
    ('F. Fishing village, 5,000', 5000, {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_FISH': 6000, 'BONUS_CRAB': 2000, 'BONUS_SALT': 15}),
    ('G. Potato labourers, 10,000', 10000, {'vigorous': 0.8, 'active': 0.1, 'sedentary': 0.1},
     {'BONUS_POTATO': 30000, 'BONUS_DAIRY': 6000, 'BONUS_SALT': 30}),
    ('D. Besieged town, 20,000', 20000, {'vigorous': 0.7, 'active': 0.2, 'sedentary': 0.1},
     {'BONUS_WHEAT': 3000, 'BONUS_PIG': 400, 'BONUS_SALT': 60}),
]
SHORT = {'fullness': 'F', 'energy': 'E', 'protein': 'prot', 'vit_c': 'C', 'vit_a_rae': 'A', 'thiamin': 'B1',
         'niacin': 'B3', 'folate_dfe': 'fol', 'b12': 'B12', 'iron': 'Fe', 'zinc': 'Zn', 'calcium': 'Ca', 'iodine': 'I',
         'potassium': 'K', 'sodium': 'Na'}


def main():
    print('| City | A* | Psi* | fed | x | protein g | alcohol g | plain water ml | work | eaten g/(p d) |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    res = {}
    for name, n, work, stocks in CITIES:
        r = solve(n, work, stocks)
        res[name] = r
        eaten = ', '.join('%s %d' % (g[6:].lower(), v) for g, v in r['q'].items() if v >= 0.5)
        print('| %s | %.3f | %.2f | %.2f | %.2f | %d | %.1f | %d | %.2f | %s |' % (name, r['A_star'], r['psi_star'], r['fed'],
              r['x'], r['P'], r['alcohol'], r['w_plain'], r['work'], eaten))
    print('\n| City | ' + ' | '.join(SHORT[i] for i in ADEQ) + ' |')
    print('|---|' + '---|' * len(ADEQ))
    for name, r in res.items():
        print('| %s | ' % name + ' | '.join('%.2f' % min(9.99, r['cov'][i]) for i in ADEQ) + ' |')
    print('\n| City | scarce goods: shadow value in stage 1 (adequacy per kg) / stage 2 (well-being per kg) |')
    print('|---|---|')
    for name, r in res.items():
        s = ', '.join('%s %.4f / %.4f' % (g[6:].lower(), 1000 * r['sv1'][g], 1000 * r['sv2'][g])
                      for g in r['sv1'] if r['sv1'][g] > 1e-12 or r['sv2'][g] > 1e-12)
        print('| %s | %s |' % (name, s or 'none'))


if __name__ == '__main__':
    main()
