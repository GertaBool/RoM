#!/usr/bin/env python3
"""Need levels derived from design targets instead of guessed: for each need, the level per citizen (by city size:
1-3, 4-8, 9 and more) at which the share of citizens fully supplied meets its target in the 30 games, under the
recommended rules (staple shared in the network, stores, spoilage, goods-aware governor). Bisection on one scale
factor per need, all needs together, in parallel over the games. Writes data/needs_derived.json.
usage: calibrate_needs.py <settlement dir>"""
import collections, importlib.util, json, multiprocessing as mp, os, sys
import numpy as np

ROOT = sys.argv[1]
TARGET = {'variety': 0.80, 'clothing': 0.80, 'fuel': 0.80, 'luxury': 0.50}  # design intents: everyday goods for most, comforts for half
SIZE_SHAPE = (1.0, 1.4, 2.0)  # a town's citizens want 1.4 times a village's, a city's twice (design intent)
START = {'variety': 35, 'clothing': 15, 'fuel': 20, 'luxury': 6}  # hundredths per citizen for a village: the starting point
ITER = 9


def load():
    sys.argv = ['model.py', ROOT]
    spec = importlib.util.spec_from_file_location('model', os.path.join(ROOT, 'tools', 'model.py'))
    M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
    return M


M = None


def work(args):
    global M
    if M is None: M = load()
    gi, levels = args
    M.NEEDS[:] = [(cat, goods, per if cat not in levels else tuple(int(round(levels[cat] * k)) for k in SIZE_SHAPE))
                  for cat, goods, per in M.NEEDS_BASE]
    M.NEEDS[4] = ('tools', ['tools'], (0, 0, 0))  # tools are an input to production in the vision, not a consumer need
    V = dict(rule='age', staple='goods', dist='network', store=True, spoil=True, units=100, tiers='size', governor='aware')
    r = M.run(M.GAMES[gi], V)
    m = r['m']
    return {k: m.get(k, 0) for k in m}


if __name__ == '__main__':
    M = load()
    n_games = len(M.GAMES)
    lo = {k: 0.0 for k in TARGET}; hi = {k: 4.0 * START[k] for k in TARGET}
    lev = dict(START); hist = []
    with mp.Pool(4) as pool:
        for it in range(ITER):
            res = pool.map(work, [(gi, lev) for gi in range(n_games)])
            tot = collections.Counter()
            for r in res: tot.update(r)
            met = {k: 1 - tot['shortpop_' + k] / tot['popturns'] for k in TARGET}
            staple_short = tot['shortpop_staple'] / tot['popturns']
            hist.append(dict(levels={k: round(v, 2) for k, v in lev.items()}, met={k: round(v, 4) for k, v in met.items()}, staple_short=round(staple_short, 4)))
            print(it, hist[-1], flush=True)
            for k in TARGET:  # more supplied than the target: raise the level; fewer: lower it
                if met[k] > TARGET[k]: lo[k] = lev[k]
                else: hi[k] = lev[k]
                lev[k] = (lo[k] + hi[k]) / 2
    best = min(hist, key=lambda h: sum(abs(h['met'][k] - TARGET[k]) for k in TARGET))
    json.dump(dict(target=TARGET, size_shape=SIZE_SHAPE, start=START, history=hist, chosen=best), open(os.path.join(ROOT, 'data', 'needs_derived.json'), 'w'), indent=1)
    print('chosen', best)
