#!/usr/bin/env python3
"""Phases of the human's game: an exact segmentation of its per-turn activity.

usage: phases.py <registry.fig.json> <game.duckdb> ...   (run with ~/.cache/rom-ana/bin/python)

Per turn of the human (turn 0 to the last T line), from the war log:
  build      build and route orders (A lines MISSION_BUILD, MISSION_ROUTE_TO)
  move       move orders (MISSION_MOVE_TO)
  train      city orders for units (ORDER, order type 0)
  construct  city orders for buildings (ORDER, order type 1)
  found      cities founded (MISSION_FOUND)
  attack     battles the human started (C lines with the human attacking)
  war        1 while a war of the human is open (a W line not yet ended by a Q line of the pair)
Each series is transformed by log(1 + x) and standardised (a constant series is left out). A
partition of the turns into segments of at least MIN_LEN turns is scored by the summed squared
deviation of every series from its segment mean, plus BETA per segment; the minimum is found
exactly by dynamic programming over segment ends (the best partition of turns 0..t ends in a
segment s..t whose prefix 0..s-1 is itself best partitioned; by induction over t). BETA is the
parsimony coefficient (framework.md, section 6): p * ln(n) for p series over n turns. The
partition is also computed at half and at twice BETA, so a boundary that moves with BETA is seen.
Tables: <game>_phases (each segment with the mean of every raw series per turn and the cities the
human held at its end) and <game>_phase_beta (the boundaries at each BETA).
"""
import math, os, sys

import duckdb
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

MIN_LEN = 10
SERIES = ['build', 'move', 'train', 'construct', 'found', 'attack', 'war']


def series(con):
    h = con.execute('select player from wl_P where human=1').fetchone()[0]
    last = con.execute('select max(turn) from wl_T').fetchone()[0]
    n = last + 1
    X = {k: np.zeros(n) for k in SERIES}
    q = lambda sql: con.execute(sql, [h]).fetchall()
    for t, k in q("select turn, a5 from wl_A where player=? and a5 in ('MISSION_BUILD', 'MISSION_ROUTE_TO', 'MISSION_MOVE_TO', 'MISSION_FOUND')"):
        if t < n: X['found' if k == 'MISSION_FOUND' else 'move' if k == 'MISSION_MOVE_TO' else 'build'][t] += 1
    for t, o in q("select turn, a3 from wl_A where player=? and kind='ORDER' and a3 in ('0', '1')"):
        if t < n: X['train' if o == '0' else 'construct'][t] += 1
    for (t,) in q('select turn from wl_C where att=?'):
        if t < n: X['attack'][t] += 1
    for t0, t1 in con.execute('''select w.turn, coalesce((select min(q.turn) from wl_Q q where q.seq > w.seq and
            ((q.team=w.team and q.target=w.target) or (q.team=w.target and q.target=w.team))), ?) from wl_W w
            where w.team=? or w.target=?''', [last, h, h]).fetchall():
        X['war'][t0:t1 + 1] = 1
    cities = np.zeros(n)
    ev = q("""select turn, 1 from wl_A where player=? and kind='MISSION' and a5='MISSION_FOUND'
              union all select turn, 1 from wl_K where new_owner=$1 union all select turn, -1 from wl_K where old_owner=$1
              union all select turn, -1 from wl_Z where new_owner=$1""".replace('$1', str(h)))
    for t, d in ev:
        if t < n: cities[t:] += d
    return h, n, X, cities


def partition(Z, beta):
    """Exact optimal partitioning: segments [s, t), each of length >= MIN_LEN."""
    n = Z.shape[0]
    c1 = np.vstack([np.zeros(Z.shape[1]), np.cumsum(Z, 0)])
    c2 = np.vstack([np.zeros(Z.shape[1]), np.cumsum(Z * Z, 0)])
    cost = lambda s, t: float(((c2[t] - c2[s]) - (c1[t] - c1[s]) ** 2 / (t - s)).sum())
    F = [0.0] + [math.inf] * n
    back = [0] * (n + 1)
    for t in range(MIN_LEN, n + 1):
        for s in [0] + list(range(MIN_LEN, t - MIN_LEN + 1)):
            if F[s] == math.inf: continue
            v = F[s] + cost(s, t) + beta
            if v < F[t] - 1e-12: F[t], back[t] = v, s
    cuts, t = [], n
    while t > 0:
        cuts.append((back[t], t)); t = back[t]
    return cuts[::-1]


REG, DBS = sys.argv[1], sys.argv[2:]
reg = Registry(REG, DBS)
for db in DBS:
    g = os.path.basename(db).split('.')[0]
    con = duckdb.connect(db, read_only=True)
    h, n, X, cities = series(con)
    used = [k for k in SERIES if X[k].std() > 0]
    Z = np.column_stack([(np.log1p(X[k]) - np.log1p(X[k]).mean()) / np.log1p(X[k]).std() for k in used])
    beta = len(used) * math.log(n)
    segs = partition(Z, beta)
    rows = []
    for i, (s, t) in enumerate(segs):
        rows.append([i + 1, f'{s}-{t - 1}', t - s] + [round(float(X[k][s:t].mean()), 2) for k in SERIES] + [int(cities[t - 1])])
    reg.result_table(f'{g}_phases', ['phase', 'turns', 'length'] + [f'{k}_per_turn' if k != 'war' else 'war_share' for k in SERIES]
                     + ['cities_at_end'], rows, 'orders', 'human', f'turns 0-{n - 1}',
                     f'phases.py: exact optimal partition (segments of at least {MIN_LEN} turns, penalty p ln n per segment, p = {len(used)} series: '
                     f'{", ".join(used)}) of the war log of {g}; means of the raw series per turn', [r[0] for r in rows], n=n)
    stab = []
    for m in (0.5, 1, 2):
        stab.append([m, ' '.join(str(s) for s, _ in partition(Z, beta * m)[1:]) or '-'])
    reg.result_table(f'{g}_phase_beta', ['penalty_factor', 'phase_starts'], stab, 'turn', 'human', f'turns 0-{n - 1}',
                     'phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled', [r[0] for r in stab], n=n)
    print(g, 'beta', round(beta, 1), [(s, t - 1) for s, t in segs], file=sys.stderr)
reg.save()
