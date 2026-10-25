#!/usr/bin/env python3
"""Per-turn series, shortfalls by city size, the floating-point check and the reconstruction checks, for the
variants the figures show. Imports tools/model.py so the rules are the same.

usage: analysis.py <settlement dir>
"""
import collections, importlib.util, json, os, sys
import numpy as np

ROOT = sys.argv[1]
sys.argv = ['model.py', ROOT]
spec = importlib.util.spec_from_file_location('model', os.path.join(ROOT, 'tools', 'model.py'))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
games = [g for g in M.G if g['completed']]
base_v = dict(rule='age', staple='separate', dist='local', store=False, spoil=False, units=100, tiers='era')
SHOW = {'today_food': dict(base_v), 'goods_local': dict(base_v, staple='goods'),
        'goods_network': dict(base_v, staple='goods', dist='network', floatcheck=True),
        'network_store_spoil': dict(base_v, staple='goods', dist='network', store=True, spoil=True),
        'aware_network_store_spoil': dict(base_v, staple='goods', dist='network', store=True, spoil=True, governor='aware')}
out = {}
for name, V in SHOW.items():
    ser = None; bys = np.zeros((4, 2), np.int64); fl = collections.Counter()
    for g in games:
        r = M.run(g, V)
        s = r['series'][:150]
        ser = s.copy() if ser is None else ser + s
        bys += r['bysize']; fl.update(r['fl'])
    share = (ser[:, :, 0] / np.maximum(ser[:, :, 1], 1)).round(4).tolist()
    out[name] = dict(share=share, pop=ser[:, 0, 1].tolist(), bysize=bys.tolist(), float=dict(fl))
    print(name, dict(fl), flush=True)

# the games themselves: cities and population per player and turn, and city sizes by era under each split rule
cities = np.zeros((len(games), 150)); popn = np.zeros((len(games), 150))
for gi, g in enumerate(games):
    for pid, rows in g['players'].items():
        for t, row in enumerate(rows[:150]):
            cities[gi, t] += row[1]; popn[gi, t] += row[2]
sizes = {'age': collections.Counter(), 'equal': collections.Counter()}
for g in games[:10]:
    hist = M.cities_by_turn(g)
    for t in (49, 99, 149):
        if not hist[t]: continue
        for rule in sizes:
            for p, n in M.sizes(g, t, hist[t], rule).items():
                sizes[rule][(t, min(n, 20))] += 1
out['games'] = dict(cities=cities.mean(axis=0).round(2).tolist(), pop=popn.mean(axis=0).round(2).tolist(),
                    cities_p10=np.percentile(cities, 10, axis=0).tolist(), cities_p90=np.percentile(cities, 90, axis=0).tolist(),
                    sizes={r: [[t, n, c] for (t, n), c in sorted(v.items())] for r, v in sizes.items()})
# reconstruction check over all games: rebuilt city counts against the telemetry's
agree = tot = 0
for g in games:
    hist = M.cities_by_turn(g)
    for t in range(g['turns']):
        c = collections.Counter(o for o, f in hist[t].values())
        for pid, rows in g['players'].items():
            if t < len(rows): tot += 1; agree += (c.get(int(pid), 0) == rows[t][1])
out['reconstruction'] = dict(agree=agree, total=tot)
# carrying capacity: what all the plots a realm's cities own could give per citizen, if every one were worked
cap = {t: np.zeros(M.NG) for t in (49, 99, 149)}; popc = {t: 0 for t in cap}
for g in games:
    hist = M.cities_by_turn(g)
    for t in cap:
        if not hist[t]: continue
        M.TG, M.CITY_TG, M.RANK = M.LATE if t >= M.CHAIN_TURN else M.EARLY
        sz = M.sizes(g, t, hist[t], 'age'); pl = M.owned_plots(hist[t])
        for p in hist[t]:
            cap[t] += M.CITY_TG[p] + (M.TG[pl[p][0]].sum(axis=0) if p in pl and pl[p][0] else 0)
            popc[t] += sz[p]
out['capacity_per_citizen'] = {str(t): {M.GOODS[i]: round(float(cap[t][i]) / max(1, popc[t]) / 100, 3) for i in range(M.NG)} for t in cap}
out['needs'] = [(n[0], n[1], n[2]) for n in M.NEEDS]
json.dump(out, open(os.path.join(ROOT, 'data', 'series.json'), 'w'))
print('reconstruction', agree, tot)
