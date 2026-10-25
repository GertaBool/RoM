#!/usr/bin/env python3
"""The reconstruction's food check in three stages, over all games: the share of city-turns whose worked plots
cannot feed the observed population (FOOD_CONSUMPTION_PER_POPULATION per citizen).
usage: calibrate.py <settlement dir>"""
import collections, importlib.util, json, os, sys
ROOT = sys.argv[1]; sys.argv = ['model.py', ROOT]
spec = importlib.util.spec_from_file_location('model', os.path.join(ROOT, 'tools', 'model.py'))
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
games = [g for g in M.G if g['completed']]
base_v = dict(rule='age', staple='separate', dist='local', store=False, spoil=False, units=100, tiers='era')
out = {}
for stage, extra in [(1, dict(cal=1)), (2, dict(cal=2)), (3, {}), ('3_equal', dict(rule='equal'))]:
    tot = collections.Counter()
    for g in games: tot.update(M.run(g, dict(base_v, **extra))['m'])
    out[str(stage)] = dict(short=tot['food_deficit_local'], cityturns=tot['cityturns'], share=round(tot['food_deficit_local'] / tot['cityturns'], 4))
    print(stage, out[str(stage)], flush=True)
json.dump(out, open(os.path.join(ROOT, 'data', 'calibration.json'), 'w'), indent=1)
