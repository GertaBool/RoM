#!/usr/bin/env python3
"""City assaults from harness telemetry: what the attacking stacks were made of, how
they were used, and which of them took the city.

usage: assault-analysis.py run.jsonl [run.jsonl ...]
Needs a harness DLL with the assault records (`{"as":...}`, build_dll.sh hooks in
updateCombat, bombard and rangeStrike). One record is one attacking team against one
city in one turn; a city counts as taken when the same turn's record shows it captured
by that team.
"""
import json, sys, statistics as st
from collections import Counter

ROLES = {'SIEGE': 'siege', 'ARCHER': 'archer', 'MOUNTED': 'mounted', 'MELEE': 'melee',
         'GUN': 'gunpowder', 'ARMOR': 'armour', 'RECON': 'recon'}


def assaults_of(path):
    hdr, out = None, []
    for line in open(path):
        if not line.startswith('{'):
            continue
        r = json.loads(line)
        if r.get('hdr'):
            hdr = r
            continue
        if 'p' not in r:
            continue
        team = {p['id']: p['team'] for p in hdr['players']}
        captured = set()
        for e in r.get('ev', []):
            if 'capture' in e:
                captured.add((team.get(e['by'], e['by']), e['capture']))
        civ = set(team.values())
        for e in r.get('ev', []):
            if 'as' in e and e['n'] > 0 and e['as'][0] in civ:
                a = dict(e)
                a['t'] = r['t']
                a['taken'] = (e['as'][0], e['as'][2]) in captured
                out.append(a)
    return out


def features(a):
    units = max(1, a['units'])
    st_ = a.get('st', {})
    dmax, d0, d1 = a['def']
    hp = a['hp'][0] / a['hp'][1] if a['hp'][1] else 100
    return {
        'units': a['units'],
        'siege share': 100.0 * st_.get('SIEGE', 0) / units,
        'archer share': 100.0 * st_.get('ARCHER', 0) / units,
        'collateral units': a['cu'],
        'walls bombarded': a['bomb'][0] > 0,
        'ranged strikes': a['bomb'][3] > 0,
        'collateral first': a['col1'] == 1,
        'walls left %': 100.0 * d1 / dmax if dmax > 0 else 0.0,
        'defender health %': hp,
        'defenders': a['defs'],
    }


def pct(n, d):
    return 100.0 * n / d if d else float('nan')


def row(label, xs):
    if not xs:
        return
    n = sum(a['n'] for a in xs)
    w = sum(a['w'] for a in xs)
    taken = sum(a['taken'] for a in xs)
    print('  %-44s assaults %5d  took the city %5.1f%%  battles won %3.0f%%  units lost per city taken %5.1f'
          % (label, len(xs), pct(taken, len(xs)), pct(w, n), (n - w) / max(1, taken)))


def main(paths):
    xs = []
    for p in paths:
        xs += assaults_of(p)
    if not xs:
        print('no assaults')
        return
    print('assault turns (team against city, with at least one attack): %d; cities taken in them: %d'
          % (len(xs), sum(a['taken'] for a in xs)))
    comp = Counter()
    for a in xs:
        for k, v in a.get('st', {}).items():
            comp[k] += v
    tot = sum(comp.values())
    print('stack composition over all assaults: ' + ', '.join('%s %.0f%%' % (k, 100.0 * v / tot) for k, v in comp.most_common(8)))
    f = [features(a) for a in xs]
    print('median stack %d units; walls bombarded first in %.0f%%; ranged strikes in %.0f%%; collateral first in %.0f%%;'
          ' assaults with no siege or collateral unit %.0f%%' % (
              st.median(x['units'] for x in f), pct(sum(x['walls bombarded'] for x in f), len(f)),
              pct(sum(x['ranged strikes'] for x in f), len(f)), pct(sum(x['collateral first'] for x in f), len(f)),
              pct(sum(1 for a in xs if a.get('st', {}).get('SIEGE', 0) == 0 and a['cu'] == 0), len(f))))
    print('attackers by unit AI: ' + ', '.join('%s %d' % kv for kv in sum((Counter(a.get('ua', {})) for a in xs), Counter()).most_common(6)))
    print('\n# What took cities')
    pairs = list(zip(xs, f))
    row('all', xs)
    row('walls at most a quarter of full at the first attack', [a for a, x in pairs if x['walls left %'] <= 25])
    row('walls above half at the first attack', [a for a, x in pairs if x['walls left %'] > 50])
    row('walls bombarded this turn', [a for a, x in pairs if x['walls bombarded']])
    row('ranged strikes this turn', [a for a, x in pairs if x['ranged strikes']])
    row('collateral attack first', [a for a, x in pairs if x['collateral first']])
    row('no collateral attack', [a for a, x in pairs if a['col'] == 0])
    row('defenders at 60% health or less when hit', [a for a, x in pairs if x['defender health %'] <= 60])
    row('defenders above 90% health when hit', [a for a, x in pairs if x['defender health %'] > 90])
    row('stack has siege', [a for a, x in pairs if x['siege share'] > 0])
    row('stack has no siege and no collateral unit', [a for a, x in pairs if x['siege share'] == 0 and a['cu'] == 0])
    row('stack has archers', [a for a, x in pairs if x['archer share'] > 0])
    for lo, hi in ((1, 1), (2, 5), (6, 15), (16, 999)):
        row('stack of %d-%d units' % (lo, hi), [a for a, x in pairs if lo <= x['units'] <= hi])
    for lo, hi in ((1, 2), (3, 4), (5, 99)):
        row('%d-%d defenders' % (lo, hi), [a for a, x in pairs if lo <= x['defenders'] <= hi])
    row('attacker had a class bonus in most attacks', [a for a in xs if 2 * a['bon'] > a['n']])
    print('\n# Composition and use at the same stack size (took the city %, assaults)')
    tests = (('siege in stack', lambda a, x: x['siege share'] > 0),
             ('collateral unit in stack', lambda a, x: a['cu'] > 0),
             ('archers in stack', lambda a, x: x['archer share'] > 0),
             ('walls at most 1/4', lambda a, x: x['walls left %'] <= 25),
             ('ranged strikes', lambda a, x: x['ranged strikes']),
             ('collateral first', lambda a, x: x['collateral first']))
    sizes = ((1, 3), (4, 9), (10, 999))
    print('  %-26s' % '' + ''.join('%22s' % ('%d-%d units' % s if s[1] < 999 else '%d+ units' % s[0]) for s in sizes))
    for label, test in tests:
        cells = []
        for lo, hi in sizes:
            yes = [a for a, x in pairs if lo <= x['units'] <= hi and test(a, x)]
            no = [a for a, x in pairs if lo <= x['units'] <= hi and not test(a, x)]
            c = lambda g: '%3.0f%% (%3d)' % (pct(sum(a['taken'] for a in g), len(g)), len(g)) if g else '   -      '
            cells.append('%11s|%10s' % (c(yes), c(no)))
        print('  %-26s' % (label + ' yes|no') + ''.join('%22s' % c for c in cells))


if __name__ == '__main__':
    main(sys.argv[1:])
