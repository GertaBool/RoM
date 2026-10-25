#!/usr/bin/env python3
"""Settlements and deals of harness games, from their telemetry (run.jsonl): each player's cities, population,
buildings and production per turn; every city founded, captured or razed with its plot; every resource deal.

usage: games.py <out.json> <run dir>...
"""
import json, os, sys

out, dirs = sys.argv[1], sys.argv[2:]
games = []
for d in sorted(dirs):
    seed = int(os.path.basename(d.rstrip('/'))[1:])
    T = [json.loads(l) for l in open(os.path.join(d, 'run.jsonl')) if l.startswith('{"t"')]
    players = {}
    events, deals, ends = [], [], {}
    for row in T:
        t = row['t']
        for p in row['p']:
            players.setdefault(p['id'], []).append([t, p.get('cities', 0), p.get('pop', 0), p.get('bld', 0), p.get('prod', 0), p.get('gold', 0),
                                                     p.get('gr', 0), p.get('rr', 0), p.get('cr', 0), p.get('er', 0)])
        for e in row.get('ev') or []:
            if 'found' in e: events.append(dict(t=t, kind='found', plot=e['found'], owner=e['by']))
            elif 'capture' in e: events.append(dict(t=t, kind='capture', plot=e['capture'], owner=e['by'], pop=e.get('pop')))
            elif 'razed' in e: events.append(dict(t=t, kind='razed', plot=e['razed']))
            elif 'deal' in e: deals.append(dict(t=t, id=e['deal'], a=e['a'], b=e['b'], ai=e['ai'], bi=e['bi']))
            elif 'trade' in e: deals.append(dict(t=t, id=None, a=e['trade'][0], b=e['trade'][1], ai=e['ai'], bi=e['bi']))
            elif 'dealEnd' in e: ends[e['dealEnd']] = t
    for x in deals:
        x['end'] = ends.get(x['id']) if x['id'] is not None else None
    completed = any(l.startswith('RESULT scenario turn 150') for l in open(os.path.join(d, 'run.log')))
    games.append(dict(seed=seed, turns=len(T), completed=completed, players=players, events=events, deals=deals))
json.dump(dict(source=dirs[0].rsplit('/', 2)[0], games=games), open(out, 'w'))
print(len(games), 'games;', sum(len(g['events']) for g in games), 'city events;', sum(len(g['deals']) for g in games), 'deals')
