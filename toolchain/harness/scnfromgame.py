#!/usr/bin/env python3
"""The turn-0 scenario of a logged game: the map's own scenario (wbs2scn.py output of the
world-builder save the game started from) with the game's setup as the save records it.

usage: scnfromgame.py <map.scn> <state0.json> <out.scn>
  state0.json: a save dump (dump.sh) with its "setup" block.

From the save: the game options, the victories, and each seat's handicap (the human's
difficulty is its seat's handicap). Everything else (plots, starting plots, units, gold) is
the map's turn-0 state.

Checks, before writing (any failure stops):
  - the map's width and height equal the save's;
  - the seats (id, team, civilization, leader) equal the save's;
  - every plot's plot type, terrain and river edges equal the save's; these do not change in play.
Reported, not checked: plots whose feature or bonus differs (chopped forests, cities on
features, new resources), and the save's start plots against the map's.
"""
import json
import sys


def main(scn, state, out):
    d = json.load(open(state))
    s = d['setup']
    plots = {(p[0], p[1]): p for p in d['plots']}
    lines = open(scn).read().splitlines()
    errors, feat, bonus = [], 0, 0
    seats = {x[0]: x for x in s['seats']}
    seen = set()
    res = []
    for ln in lines:
        a = ln.split(' ')
        k = a[0]
        if k in ('OPTION', 'VICTORY'):
            continue                      # replaced by the save's below
        if k == 'MAP':
            if (int(a[1]), int(a[2])) != (s['w'], s['h']):
                errors.append('map size %s x %s, save %d x %d' % (a[1], a[2], s['w'], s['h']))
            res.append(ln)
            res += ['OPTION ' + o for o in s['options']] + ['VICTORY ' + v for v in s['victories']]
            continue
        if k == 'PLAYER':
            i = int(a[1]); seen.add(i)
            st = seats.get(i)
            if st is None or [int(a[2]), a[3], a[4]] != [st[1], st[2], st[3]]:
                errors.append('seat %d: map %s, save %s' % (i, a[1:5], st))
            else:
                if (int(a[6]), int(a[7])) != (st[5], st[6]):
                    print('seat %d: start plot map %s,%s, save %d,%d' % (i, a[6], a[7], st[5], st[6]), file=sys.stderr)
                a[5] = st[4]
            res.append(' '.join(a))
            continue
        if k == 'PLOT':
            x, y = int(a[1]), int(a[2])
            p = plots.get((x, y))
            px = s['plotx'][y * s['w'] + x]
            if p is None:
                errors.append('plot %d,%d not in save' % (x, y))
            else:
                if int(a[3]) != p[3] or a[4] != 'TERRAIN_' + p[2]:
                    errors.append('plot %d,%d: map %s %s, save %d %s' % (x, y, a[3], a[4], p[3], p[2]))
                if [int(a[10]), int(a[11])] != px[:2]:
                    errors.append('plot %d,%d rivers: map %s %s, save %s' % (x, y, a[10], a[11], px[:2]))
                feat += (a[5] != ('FEATURE_' + p[4] if p[4] != '-' else '-'))
                bonus += (a[7] != ('BONUS_' + p[5] if p[5] != '-' else '-'))
        res.append(ln)
    for i in seats:
        if i not in seen:
            errors.append('seat %d in save, not on the map' % i)
    print('plots %d; feature differs on %d, bonus on %d' % (len(plots), feat, bonus), file=sys.stderr)
    if errors:
        print('\n'.join(errors[:20]), file=sys.stderr)
        sys.exit('%d mismatches: not written' % len(errors))
    open(out, 'w').write('\n'.join(res) + '\n')


if __name__ == '__main__':
    main(*sys.argv[1:4])
