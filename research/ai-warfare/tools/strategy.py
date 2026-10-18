#!/usr/bin/env python3
"""Which rule picks the AI the human declares war on: maximum-likelihood strategy classification.

usage: strategy.py <registry.fig.json> <game.duckdb> ...   (databases with M lines and a save dump)

Method (Bröder, in Gigerenzer, Hertwig and Pachur, Heuristics, chapter 17; Bröder and Schiffer
2003): every candidate strategy names, for each decision, the option(s) it would choose. A user of
the strategy is assumed to follow it except for errors at a constant rate e, an error picking any
other option with equal chance. With ties, the strategy's choice is any of its m tied options with
equal chance. The likelihood of the observed choices is then
  L(e) = prod over decisions of ((1 - e) / m if the choice is among the m, else e / (k - m)),
k the number of options, maximised at e = errors / n. Guessing (every option with chance 1/k)
has no parameter. Strategies are compared by log L and by BIC = -2 log L + q ln n, q = 1 for a
strategy and 0 for guessing.

A decision is every W line in which the human declares (log order, so a second declaration of
the same turn sees the first). Options: every AI player with an M line on the turn before, not
then at war with the human, holding a city, and not unmet by the human at the save (diplo; a player
gone by the save has no row and is kept, whether met or not). Cues, from the turn before: power and cities (M lines), and the grid distance between
the nearest pair of cities of the human and of the option on that turn (city owners over time
from the save's cities and the K and Z lines on each plot; map wrap ignored). Strategies:
  weakest            the least power
  nearest            the least distance (distance decay: Snook, Taylor and Bennell, Heuristics,
                     chapter 29, p. 593)
  nearest_then_weak  take-the-best with distance first: the nearest; ties by the least power
  weak_of_near_half  the least power among the options at or under the median distance
  most_cities        the most cities
  weakest_ratio      the least power per city
  engaged            at war with a team other than the human's (W lines of the pair before the declaration,
                     no Q line between; wars before a log's first W line are not seen): the test the
                     literature suggested (Jomini, The Art of War, Article XL; study/war.md, section 9)
  nearest_then_engaged, engaged_then_nearest   take-the-best with both cues, in either order
Tables: <game>_war_targets (each decision, the target's rank on each cue), war_target_strategies
(per game and pooled).
"""
import math, os, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry


def city_owner_intervals(con):
    cp = {(x, y): (p, f) for p, x, y, f in con.execute('select player, x, y, founded from cities').fetchall()}
    ev = con.execute("select x, y, turn, old_owner, k from (select x, y, turn, old_owner, 'K' k from wl_K "
                     "union all select x, y, turn, old_owner, 'Z' from wl_Z) order by x, y, turn, k").fetchall()
    by = {}
    for x, y, t, o, k in ev: by.setdefault((x, y), []).append((t, o))
    iv = []
    for xy in set(cp) | set(by):
        prev = cp[xy][1] if xy in cp else 0
        for t, o in by.get(xy, []):
            iv.append((xy, prev, t, o)); prev = t
        if xy in cp: iv.append((xy, prev, 10 ** 6, cp[xy][0]))
    return iv


def decisions(con):
    h = con.execute('select player from wl_P where human=1').fetchone()[0]
    rows = con.execute('select other, met from diplo where player=?', [h]).fetchall()
    known = {o for o, _ in rows}; unmet = {o for o, m in rows if not m}   # players gone by the save have no row
    W = con.execute('select seq, turn, team, target from wl_W order by seq').fetchall()
    Q = con.execute('select seq, turn, team, target from wl_Q order by seq').fetchall()
    iv = city_owner_intervals(con)
    out = []
    for seq, t, team, target in W:
        if team != h: continue
        at_war = set()
        for s2, t2, a, b in W:
            if s2 >= seq or h not in (a, b): continue
            o = b if a == h else a
            if not any(q[0] > s2 and q[0] < seq and {q[2], q[3]} == {a, b} for q in Q): at_war.add(o)
        m = {p: (pw, c) for p, pw, c in con.execute('select player, power, cities from wl_M where turn=?', [t - 1]).fetchall()}
        cities = {}
        for (x, y), t0, t1, o in iv:
            if t0 <= t < t1: cities.setdefault(o, []).append((x, y))
        engaged = set()   # at war with a team other than the human's: a W line of the pair before, no Q line between
        for s2, t2, a, b in W:
            if s2 >= seq or h in (a, b): continue
            if not any(q[0] > s2 and q[0] < seq and {q[2], q[3]} == {a, b} for q in Q): engaged |= {a, b}
        opts = []
        for p, (pw, c) in m.items():
            if p == h or p in at_war or p in unmet or p not in cities: continue
            d = min(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a in cities.get(h, []) for b in cities[p]) if cities.get(h) else None
            opts.append(dict(p=p, power=pw, cities=c, dist=d, engaged=0 if p in engaged else 1))
        out.append(dict(seq=seq, turn=t, target=target, opts=opts))
    return out


def picks(name, opts):
    if name == 'weakest': key = lambda o: o['power']
    elif name == 'nearest': key = lambda o: o['dist']
    elif name == 'nearest_then_weak': key = lambda o: (o['dist'], o['power'])
    elif name == 'most_cities': key = lambda o: -o['cities']
    elif name == 'weakest_ratio': key = lambda o: o['power'] / max(1, o['cities'])
    elif name == 'engaged': key = lambda o: o['engaged']
    elif name == 'nearest_then_engaged': key = lambda o: (o['dist'], o['engaged'])
    elif name == 'engaged_then_nearest': key = lambda o: (o['engaged'], o['dist'])
    elif name == 'weak_of_near_half':
        ds = sorted(o['dist'] for o in opts); med = ds[(len(ds) - 1) // 2]
        near = [o for o in opts if o['dist'] <= med]
        best = min(o['power'] for o in near)
        return {o['p'] for o in near if o['power'] == best}
    best = min(key(o) for o in opts)
    return {o['p'] for o in opts if key(o) == best}


STRATS = ['weakest', 'nearest', 'nearest_then_weak', 'weak_of_near_half', 'most_cities', 'weakest_ratio', 'engaged',
          'nearest_then_engaged', 'engaged_then_nearest']


def score(ds):
    rows = []
    n = len(ds)
    g = sum(-math.log(len(d['opts'])) for d in ds)
    for s in STRATS:
        hits = 0.0; cases = []
        for d in ds:
            P = picks(s, d['opts']); m = len(P); k = len(d['opts'])
            hit = d['target'] in P; hits += (1 / m) if hit else 0
            cases.append((hit, m, k))
        e = sum(1 for c in cases if not c[0]) / n
        ll = 0.0
        for hit, m, k in cases:
            if hit: ll += math.log((1 - e) / m) if e < 1 else -math.inf
            else: ll += math.log(e / (k - m)) if k > m else -math.inf
        rows.append([s, sum(1 for c in cases if c[0]), n, round(e, 3), round(ll, 2), round(-2 * ll + math.log(n), 2)])
    rows.append(['guessing', '', n, '', round(g, 2), round(-2 * g, 2)])
    return rows


REG, DBS = sys.argv[1], sys.argv[2:]
reg = Registry(REG, DBS)
pooled = []
head = ['strategy', 'choices_matched', 'decisions', 'error_rate', 'log_likelihood', 'bic']
for db in DBS:
    gname = os.path.basename(db).split('.')[0]
    con = duckdb.connect(db, read_only=True)
    ds = decisions(con)
    bad = [d for d in ds if d['target'] not in {o['p'] for o in d['opts']}]
    if bad: raise SystemExit(f'{gname}: target not among the options at turns {[d["turn"] for d in bad]}')
    rows = []
    for d in ds:
        o = d['opts']; t = next(x for x in o if x['p'] == d['target'])
        rank = lambda key: 1 + sum(1 for x in o if key(x) < key(t))
        rows.append([d['turn'], d['target'], len(o), rank(lambda x: x['power']), rank(lambda x: x['dist']),
                     rank(lambda x: -x['cities']), t['power'], min(x['power'] for x in o), t['dist'], min(x['dist'] for x in o)])
    reg.result_table(f'{gname}_war_targets', ['turn', 'target', 'options', 'power_rank', 'distance_rank', 'cities_rank',
                     'target_power', 'least_power', 'target_distance', 'least_distance'], rows, 'rank', 'human',
                     'each declaration of the human (cues from the turn before)',
                     f'strategy.py: W lines of {gname}; options: AIs with an M line the turn before, holding a city, not at war with the human, not unmet at the save; '
                     'rank 1 = the least power, the least distance, the most cities', [r[0] for r in rows], n=len(rows))
    reg.result_table(f'{gname}_war_target_strategies', head, score(ds), 'category', 'human', 'each declaration of the human',
                     f'strategy.py: maximum-likelihood classification over the declarations of {gname}', STRATS + ['guessing'], n=len(ds))
    pooled += ds
reg.result_table('war_target_strategies_pooled', head, score(pooled), 'category', 'human', 'each declaration of the human',
                 'strategy.py: maximum-likelihood classification over the declarations of every game given', STRATS + ['guessing'], n=len(pooled))
reg.save()
for r in score(pooled): print(r, file=sys.stderr)
