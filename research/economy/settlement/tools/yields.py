#!/usr/bin/env python3
"""How much buildings, civics, specialists and trade routes add to what the plots give, measured in the games.
For each player and turn: the observed production (sum of CvCity::getYieldRate(YIELD_PRODUCTION)) and commerce
(gold + research + culture + espionage rates), against the production and commerce of the plots its rebuilt cities
work. Also: the trade-route profit each rebuilt city would earn to its best domestic partner
(CvCity::getBaseTradeProfit on a Standard world), and the rebuilt cities' food under the starting civic's food
modifier (Oral Law).
usage: yields.py <settlement dir>"""
import collections, importlib.util, json, os, sys
import numpy as np

ROOT = sys.argv[1]
sys.argv = ['model.py', ROOT]
spec = importlib.util.spec_from_file_location('model', os.path.join(ROOT, 'tools', 'model.py'))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
BC = json.load(open(os.path.join(ROOT, 'data', 'bc.json')))
games = [g for g in M.G if g['completed']]
TURNS = 150
WORLD_PCT, POP_PCT, PROFIT_PCT = 50, 50, 20  # CIV4WorldInfo Standard iTradeProfitPercent; THEIR_POPULATION_TRADE_PERCENT; TRADE_PROFIT_PERCENT
oral = next(c for c in BC['civics'] if c['type'] == 'CIVIC_ORAL_LAW')['yield_mod']
rp = [[] for _ in range(TURNS)]; rc = [[] for _ in range(TURNS)]
tot = np.zeros((TURNS, 4))  # plot production, observed production, plot commerce, observed commerce (summed over games)
profit = collections.Counter(); food = collections.Counter()
for g in games:
    hist = M.cities_by_turn(g)
    for t in range(TURNS):
        cities = hist[t]
        if not cities: continue
        late = t >= M.CHAIN_TURN
        M.TG, M.CITY_TG, M.RANK = M.LATE if late else M.EARLY
        imp = M.improved_late if late else M.improved_early
        sz = M.sizes(g, t, cities, 'age'); pl = M.owned_plots(cities)
        per = collections.defaultdict(lambda: np.zeros(3))
        for p, (o, f0) in cities.items():
            tiles = M.city_tiles(p, sz[p], pl.get(p))
            y = np.maximum(imp[p], [3, 2, 1]) + (imp[tiles].sum(axis=0) if tiles else 0)
            per[o] += y
            food['cityturns'] += 1
            food['short_plain'] += int(y[0] < 3 * sz[p])
            food['short_oral'] += int(int(y[0]) * (100 + oral[0]) // 100 < 3 * sz[p])
            if t in (49, 99, 149):
                best = 0
                for q, (o2, f2) in cities.items():
                    if q != p and o2 == o:
                        d = max(abs(int(M.XY[p][0]) - int(M.XY[q][0])), abs(int(M.XY[p][1]) - int(M.XY[q][1])))
                        best = max(best, min(sz[q] * POP_PCT, d * WORLD_PCT) * PROFIT_PCT // 100)
                profit[(t, 'routes')] += 1; profit[(t, 'floor')] += int(best <= 100); profit[(t, 'sum')] += max(100, best)
        for o, y in per.items():
            rows = g['players'].get(str(o))
            if not rows or t >= len(rows): continue
            row = rows[t]
            prod_obs, com_obs = row[4], row[6] + row[7] + row[8] + row[9]
            tot[t] += [y[1], prod_obs, y[2], com_obs]
            if y[1] > 0: rp[t].append(prod_obs / y[1])
            if y[2] > 0: rc[t].append(com_obs / y[2])
q = lambda a, pc: [round(float(np.percentile(x, pc)), 3) if x else None for x in a]
out = dict(prod_ratio=dict(p25=q(rp, 25), p50=q(rp, 50), p75=q(rp, 75)), com_ratio=dict(p25=q(rc, 25), p50=q(rc, 50), p75=q(rc, 75)),
           totals=tot.tolist(), food=dict(food), oral=oral,
           profit={str(t): dict(routes=profit[(t, 'routes')], at_floor=profit[(t, 'floor')], mean=round(profit[(t, 'sum')] / max(1, profit[(t, 'routes')]) / 100, 3))
                   for t in (49, 99, 149)})
json.dump(out, open(os.path.join(ROOT, 'data', 'yields.json'), 'w'))
print(json.dumps({k: out[k] for k in ('food', 'profit')}), 'prod ratio median t50/100/150', out['prod_ratio']['p50'][49], out['prod_ratio']['p50'][99],
      out['prod_ratio']['p50'][149], 'com', out['com_ratio']['p50'][49], out['com_ratio']['p50'][99], out['com_ratio']['p50'][149])
