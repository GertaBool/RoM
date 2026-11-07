"""R50 (M97): worked trace of the food model (food_model_spec.md version 2) from input data to every intermediate value.

Part 1: for beef, potatoes and apples, each term of E13 (satisfaction), E14 (nutrient density), E15 (well-being),
E16 (the two keys) and E12 (fullness). Part 2: for the rich city (E), E3-E8 and E11, then the allocation under
version 1 (one pass on V = s + nu + beta) and version 2 (pass 1 on N until fed, pass 2 on beta), good by good.
usage: food_model_trace.py
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('fm', os.path.join(HERE, 'food_model.py'))
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)
NEED = fm.NEED['needs']


def goods_part():
    for g in ['BONUS_COW', 'BONUS_POTATO', 'BONUS_APPLE']:
        v, m, d = fm.good(g), fm.micro(g), fm.NUT['goods'][g]
        kc = v['kcal']
        p = 4 * v['protein'] / kc
        q = d['diaas'] if d.get('diaas') is not None else (1.0 if g in fm.ANIMAL else 0.44)
        print('\n%s: per 100 g kcal %s, protein %s g, fat %s g; DIAAS %s' % (g[6:].title(), kc, v['protein'], v['fat'], q))
        print('  E13  s = (1 + 2 x %.3f x %.2f) / (1 + 2 x 0.146 x 0.44) = %.3f' % (p, min(q, 1), fm.satisfaction(g)))
        sh = [min(1, (v['protein'] / kc) / (NEED['protein']['value'] / 2600))]
        terms = ['protein %.2f' % sh[0]]
        for k in fm.NUTRIENTS:
            x = min(1, (m[k] / m['kcal']) / (NEED[k]['value'] / 2600))
            sh.append(x)
            terms.append('%s %.2f' % (k, x))
        print('  E14  terms: ' + ', '.join(terms))
        print('       nu = %.3f / 13 = %.3f' % (sum(sh), fm.nutrition(g)))
        sug = 4 * fm.SUGARS.get(g, 0) / kc
        fat = min(1, 9 * v['fat'] / kc)
        alc = 7 * fm.ALCOHOL_G.get(g, 0) / kc
        carb = max(0, 1 - fat - p - alc)
        water = m['water'] / m['kcal']
        print('  E15  beta = %.3f + 2 x %.3f x %.3f + %.3f + min(1, %.3f / 3) - 0.5 x %.3f = %.3f'
              % (sug, fat, carb, alc, water, fat, fm.wellbeing(g)))
        print('  E16  N = s + nu = %.3f;  beta = %.3f;   E12  sigma = %.3f' % (fm.nutrition_key(g), fm.wellbeing(g), fm.satiety(g)))


def city_part():
    name, n, work, stocks = [c for c in fm.CITIES if c[0].startswith('E.')][0]
    avail = {g: fm.grams_per_day(t, n) for g, t in stocks.items()}
    pal = sum(s * fm.PAL[k] for k, s in work.items())
    lpk, mgl = fm.BREW['BONUS_TEA']
    caf = min(avail['BONUS_TEA'], 600 / (lpk * mgl / 1000)) * lpk * mgl / 1000
    c = caf / 600
    e_need = fm.BMR * pal + 150 * c
    e_max = fm.BMR * 2.4 + 150 * c
    print('\n%s' % name)
    print('  E3  PAL_w = %s = %.3f' % (' + '.join('%.1f x %.2f' % (s, fm.PAL[k]) for k, s in work.items()), pal))
    print('  E4  caffeine %.0f mg -> c = %.3f' % (caf, c))
    print('  E5  E_need = 1,536 x %.3f + 150 x %.3f = %.0f kcal' % (pal, c, e_need))
    print('  E6  E_max = 1,536 x 2.40 + 150 x %.3f = %.0f kcal' % (c, e_max))
    print('  E7  F_cap = 1.36 x E_max = %.0f;  fed at 1.36 x E_need = %.0f;  E8  P_max = %.0f g'
          % (1.36 * e_max, 1.36 * e_need, 0.35 * e_max / 4))
    foods = [g for g in avail if g not in fm.BREW and g != 'BONUS_SALT']
    per = {}
    cap = {}
    for g in foods:
        v = fm.good(g)
        per[g] = dict(kc=v['kcal'] * v['edible'] / 100, pr=v['protein'] * v['edible'] / 100,
                      ft=v['fat'] * v['edible'] / 100, ed=v['edible'])
        cc = avail[g]
        if per[g]['ft'] > 0:
            cc = min(cc, 250 / per[g]['ft'])
        if g == 'BONUS_DAIRY':
            cc = min(cc, 3000)
        cap[g] = cc
    print('  E11 caps g: ' + ', '.join('%s %d' % (g[6:].title(), cap[g]) for g in foods))

    def run(passes):
        q = {g: 0.0 for g in foods}
        e = sat = p = fr = 0.0
        log = []
        for keys, stop in passes:
            while e < e_max - 1e-9 and sat < stop - 1e-9:
                best, bm = None, 0
                for g in foods:
                    k = keys[g]
                    if k <= 0:
                        continue
                    dq = 10 / per[g]['kc']
                    if q[g] + dq > cap[g] + 1e-9 or p + dq * per[g]['pr'] > 0.35 * e_max / 4:
                        continue
                    if g in fm.FRUIT and fr + dq * per[g]['ed'] > 4518:
                        continue
                    mv = k / (1 + q[g] / fm.SERVING_G[g])
                    if mv > bm:
                        best, bm = g, mv
                if best is None:
                    break
                dq = 10 / per[best]['kc']
                q[best] += dq
                e += 10
                sat += 10 * fm.satiety(best)
                p += dq * per[best]['pr']
                if best in fm.FRUIT:
                    fr += dq * per[best]['ed']
            log.append((round(e), round(sat)))
        return q, log

    V = {g: fm.satisfaction(g) + fm.nutrition(g) + fm.wellbeing(g) for g in foods}
    N = {g: fm.nutrition_key(g) for g in foods}
    B = {g: fm.wellbeing(g) for g in foods}
    q1, l1 = run([(V, 1.36 * e_max)])
    q2, l2 = run([(N, 1.36 * e_need), (B, 1.36 * e_max)])
    print('  version 1 (one pass on V): ends at E %d kcal, F %d' % l1[0])
    print('  version 2: pass 1 ends at E %d kcal, F %d (fed); pass 2 ends at E %d kcal, F %d' % (l2[0] + l2[1]))
    print('\n| Good | V (v1) | N (v2) | beta (v2) | sigma | serving g | eaten v1 g | eaten v2 g | kcal v1 | kcal v2 |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for g in foods:
        print('| %s | %.2f | %.2f | %.2f | %.2f | %s | %d | %d | %d | %d |' % (g[6:].title(), V[g], N[g], B[g], fm.satiety(g),
              fm.SERVING_G[g], q1[g], q2[g], q1[g] * per[g]['kc'], q2[g] * per[g]['kc']))
    print('| total | | | | | | | | %d | %d |' % (sum(q1[g] * per[g]['kc'] for g in foods), sum(q2[g] * per[g]['kc'] for g in foods)))


if __name__ == '__main__':
    goods_part()
    city_part()
