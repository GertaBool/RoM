#!/usr/bin/env python3
"""Compare two harness snapshots (.game + .game.idx) part by part.
usage: snapdiff.py A.game B.game"""
import sys
def parts(path):
    data = open(path, 'rb').read()
    out, start = [], 0
    for line in open(path + '.idx'):
        name, end = line.split()
        out.append((name, data[start:int(end)]))
        start = int(end)
    return out
a, b = parts(sys.argv[1]), parts(sys.argv[2])
for (na, da), (nb, db) in zip(a, b):
    if da == db:
        continue
    first = next((i for i in range(min(len(da), len(db))) if da[i] != db[i]), min(len(da), len(db)))
    ndiff = sum(1 for x, y in zip(da, db) if x != y)
    print('%-9s size %d vs %d, first difference at +%d, %d differing bytes (same offsets)' % (na, len(da), len(db), first, ndiff))
