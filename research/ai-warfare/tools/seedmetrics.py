#!/usr/bin/env python3
"""One value per seeded run, from the oracle records of toolchain/analysis/seeds.sh.

usage: seedmetrics.py <seeds dir> <metric> [--exclude-player N] > values.txt   (input for exper.py)

Metrics, summed over the players counted (all but --exclude-player, normally the human seat,
which the harness hands to the AI) and over the turns played:
  kills_available  expected kills an expert could make before each player's moves (before.kills)
  kills_made       kills made in those moves (after.kills)
  kill_share       kills_made / kills_available
  exposed_value    value an expert enemy could destroy after the moves (after.lossV)
  city_fall        sum of next-turn capture chances of the player's cities (after.cityFall)
Seeds are read in numeric order; a seed whose run.log has fewer turn lines than the others is
reported on stderr and left out.
"""
import json, os, re, sys

D, metric = sys.argv[1], sys.argv[2]
ex = int(sys.argv[sys.argv.index('--exclude-player') + 1]) if '--exclude-player' in sys.argv else None
runs = sorted((int(m.group(1)), os.path.join(D, d)) for d in os.listdir(D) if (m := re.fullmatch(r's(\d+)', d)))
turns = {s: sum(1 for l in open(os.path.join(p, 'run.log'), errors='replace') if l.startswith('turn ')) for s, p in runs}
full = max(turns.values())
for s, p in runs:
    if turns[s] < full:
        print(f'seed {s}: {turns[s]} of {full} turn lines, left out', file=sys.stderr); continue
    av = made = exp = fall = 0.0
    for l in open(os.path.join(p, 'oracle.jsonl')):
        r = json.loads(l)
        if r.get('p') == ex: continue
        if r['o'] == 'before': av += r.get('kills', 0)
        elif r['o'] == 'after':
            made += r.get('kills', 0); exp += r.get('lossV', 0); fall += r.get('cityFall', 0)
    v = {'kills_available': av, 'kills_made': made, 'kill_share': made / av if av else float('nan'),
         'exposed_value': exp, 'city_fall': fall}[metric]
    print(f'{v:.6g}')
