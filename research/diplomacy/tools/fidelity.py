#!/usr/bin/env python3
"""Totals over all players every N turns for one or more run.jsonl files.
usage: fidelity.py N label=path [label=path ...]"""
import json, sys
step = int(sys.argv[1])
runs = [a.split('=', 1) for a in sys.argv[2:]]
data = {}
for label, path in runs:
    rows = {}
    for line in open(path):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if 't' in r and 'p' in r:
            rows[r['t']] = r
    data[label] = rows
print('%-6s %-5s %6s %6s %6s %6s %6s %8s %7s %6s %7s' % ('run', 'turn', 'cities', 'pop', 'pop/c', 'bld/c', 'units', 'gold', 'beakers', 'techs', 'ms'))
last = max(max(r) for r in data.values())
for t in range(0, last + 1, step):
    for label, rows in data.items():
        r = rows.get(t)
        if r is None:
            continue
        P = r['p']
        c = sum(p['cities'] for p in P) or 1
        pop = sum(p['pop'] for p in P)
        bld = sum(p.get('bld', 0) for p in P)
        print('%-6s %-5d %6d %6d %6.1f %6s %6d %8d %7d %6.1f %7d' % (
            label, t, c, pop, pop / c, ('%.1f' % (bld / c)) if bld else '-', sum(p['units'] for p in P),
            sum(p['gold'] for p in P), sum(p['rr'] for p in P), sum(p['techs'] for p in P) / len(P), r.get('ms', 0)))
