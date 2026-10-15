#!/usr/bin/env python3
"""Summarise what AI units do over a game (harness telemetry with HARNESS_UNIT_ACTIVITY=1).

usage: unit-activity.py <CvEnums.h> <run.jsonl> [turn step]
Per game phase (turn windows), for each unit AI type summed over all players:
units, share in a city, asleep/fortified, moved since the previous record,
unmoved 10+ and 50+ turns, in a group of 2+. Also units per city.
"""
import json, re, sys

enums = open(sys.argv[1], encoding='latin-1').read()
body = enums[enums.index('NO_UNITAI = -1'):enums.index('NUM_UNITAI_TYPES')]
names = {}
i = -2
for x in re.sub(r'//[^\n]*', '', body).split(','):
    x = x.strip()
    if not x or x.startswith('#'):
        continue
    i = int(x.split('=')[1]) if '=' in x else i + 1
    names[i] = x.split('=')[0].strip().replace('UNITAI_', '')

recs = [json.loads(l) for l in open(sys.argv[2]) if l.startswith('{') and '"ua"' in l]
step = int(sys.argv[3]) if len(sys.argv) > 3 else 100
phases = {}
for r in recs:
    ph = (r['t'] - 1) // step
    cities = sum(p['cities'] for p in r['p'])
    d = phases.setdefault(ph, {'n': 0, 'cities': 0, 'ai': {}})
    d['n'] += 1
    d['cities'] += cities
    for pid, rows in r['ua'].items():
        for row in rows:
            a = d['ai'].setdefault(row[0], [0] * 7)
            for k in range(7):
                a[k] += row[k + 1]
for ph in sorted(phases):
    d = phases[ph]
    tot = sum(a[0] for a in d['ai'].values())
    print('== turns %d-%d (%d records): %.0f units, %.1f per city' % (ph * step + 1, (ph + 1) * step, d['n'], tot / d['n'], tot / max(1, d['cities'])))
    print('   %-16s %7s %6s %7s %6s %6s %6s %6s' % ('unit AI', 'units', 'city%', 'sleep%', 'moved%', '10t+%', '50t+%', 'grp%'))
    for ai, a in sorted(d['ai'].items(), key=lambda kv: -kv[1][0]):
        if a[0] / d['n'] < 2:
            continue
        pct = lambda k: 100.0 * a[k] / a[0]
        print('   %-16s %7.0f %6.0f %7.0f %6.0f %6.0f %6.0f %6.0f' % (names.get(ai, str(ai))[:16], a[0] / d['n'], pct(1), pct(2), pct(3), pct(4), pct(5), pct(6)))
