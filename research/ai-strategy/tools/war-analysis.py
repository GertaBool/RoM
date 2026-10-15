#!/usr/bin/env python3
"""Wars and battles from harness telemetry, measured against strategic principles.

usage: war-analysis.py run.jsonl [run.jsonl ...]
Needs a harness DLL built with the war hooks (build_dll.sh: HH_noteChangeWar,
HH_noteCombatStart/Result). Reconstructs every war from declaration to peace or
the end of the game, with the declarer's preparation, the battles both ways,
the cities that changed hands and how the war ended.
"""
import json, sys, statistics as st

PLANS = {-1: 'none', 0: 'attacked recently', 1: 'attacked', 2: 'preparing limited', 3: 'preparing total',
         4: 'limited', 5: 'total', 6: 'dogpile'}


def load(path):
    hdr, recs = None, []
    for line in open(path):
        if not line.startswith('{'):
            continue
        r = json.loads(line)
        if r.get('hdr'):
            hdr = r
        elif 'p' in r:
            recs.append(r)
    return hdr, recs


def wars_of(path):
    hdr, recs = load(path)
    team = {p['id']: p['team'] for p in hdr['players']}
    alive_rel = {}
    wars, open_wars = [], {}
    last_t = recs[-1]['t']
    prev = None
    for r in recs:
        t = r['t']
        teams = r.get('teams', [])
        score = {team.get(p['id'], p['id']): p['score'] for p in r['p']}
        leader = max(score, key=score.get) if score else None
        at_war = set()
        rel = r.get('rel', [])
        for a in range(len(rel)):
            for b in range(len(rel)):
                if a != b and rel[a][b][0] & 2:
                    at_war.add((teams[a], teams[b]))
        for e in r.get('ev', []):
            if 'war' in e:
                d, x = e['war']
                key = frozenset((d, x))
                if key in open_wars:
                    continue
                pa, pb = e.get('pow', [0, 1])
                near = e.get('near', [0, 0])
                w = {'game': path, 'start': e['t'], 'end': None, 'd': d, 'x': x, 'plan': e.get('plan', -1),
                     'ratio': pa / max(1, pb), 'near': near[0] / max(1, near[1]), 'nearUnits': near[0],
                     'others': e.get('others', 0), 'vassal': e.get('vassal', 0),
                     'dOther': sum(1 for (a, b) in (prev or set()) if a == d and b != x),
                     'onLeader': x == leader, 'dLeader': d == leader,
                     'caps': [], 'lost': [], 'razed': 0, 'cb': {'d': [0] * 10, 'x': [0] * 10}}
                open_wars[key] = w
                wars.append(w)
            elif 'peace' in e:
                key = frozenset(e['peace'])
                w = open_wars.pop(key, None)
                if w:
                    w['end'] = e['t']
            elif 'capture' in e:
                by, frm = team.get(e['by'], e['by']), team.get(e['from'], e['from'])
                w = open_wars.get(frozenset((by, frm)))
                if w:
                    (w['caps'] if by == w['d'] else w['lost']).append((t, e.get('prevPop', 0), e.get('wonders', 0)))
            elif 'razed' in e:
                owner = team.get(e['owner'], e['owner'])
                for key, w in open_wars.items():
                    if owner in key:
                        w['razed'] += 1
                        break
            elif 'cb' in e:
                a, b = e['cb'][0], e['cb'][1]
                w = open_wars.get(frozenset((a, b)))
                if w:
                    side = 'd' if a == w['d'] else 'x'
                    for k in range(min(10, len(e['cb']) - 2)):
                        w['cb'][side][k] += e['cb'][2 + k]
        prev = at_war
    for w in wars:
        w['len'] = (w['end'] if w['end'] is not None else last_t) - w['start']
        w['ongoing'] = w['end'] is None
    return wars, last_t


def pct(n, d):
    return 100.0 * n / d if d else float('nan')


def main(paths):
    allw, turns = [], 0
    for p in paths:
        w, t = wars_of(p)
        allw += w
        turns += t
    main_w = [w for w in allw if not w['vassal']]
    n = len(main_w)
    print('games %d, turns %d, wars declared %d (%.1f per 100 game turns), joined as vassal %d'
          % (len(paths), turns, n, 100.0 * n / max(1, turns), len(allw) - n))
    if not n:
        return
    med = lambda xs: st.median(xs) if xs else float('nan')
    print('\n# Decision to fight')
    print('  war plan at declaration:', {PLANS[k]: sum(1 for w in main_w if w['plan'] == k) for k in sorted({w['plan'] for w in main_w})})
    print('  power ratio declarer/target: median %.2f; below 1.0 in %.0f%%; above 2.0 in %.0f%%'
          % (med([w['ratio'] for w in main_w]), pct(sum(w['ratio'] < 1 for w in main_w), n), pct(sum(w['ratio'] > 2 for w in main_w), n)))
    print('  target already at war with others: %.0f%%; declarer already at war elsewhere: %.0f%%'
          % (pct(sum(w['others'] > 0 for w in main_w), n), pct(sum(w['dOther'] > 0 for w in main_w), n)))
    print('  wars on the score leader: %.0f%%; wars by the score leader: %.0f%%'
          % (pct(sum(w['onLeader'] for w in main_w), n), pct(sum(w['dLeader'] for w in main_w), n)))
    print('\n# Preparation and concentration')
    print('  declarer land units within 2 plots of the target at declaration: median %.0f%% (%d units); none in %.0f%%'
          % (100 * med([w['near'] for w in main_w]), med([w['nearUnits'] for w in main_w]), pct(sum(w['nearUnits'] == 0 for w in main_w), n)))
    print('\n# Conduct and outcome')
    first = [w['caps'][0][0] - w['start'] for w in main_w if w['caps']]
    print('  wars with at least one city taken by the declarer: %.0f%%; turns to the first capture: median %s'
          % (pct(sum(1 for w in main_w if w['caps']), n), med(first)))
    print('  cities taken per war: declarer %.2f, target %.2f; razed during wars (either side) %.2f per war'
          % (st.mean(len(w['caps']) for w in main_w), st.mean(len(w['lost']) for w in main_w), st.mean(w['razed'] for w in main_w)))
    ended = [w for w in main_w if not w['ongoing']]
    print('  length (ended wars): median %s turns; ended wars with no city taken by either side: %.0f%%; ongoing at the end %d'
          % (med([w['len'] for w in ended]), pct(sum(1 for w in ended if not w['caps'] and not w['lost']), len(ended)), n - len(ended)))
    stale = [w for w in main_w if w['len'] >= 50 and not w['caps'] and not w['lost']]
    print('  stalemates (50+ turns, no city changed hands): %d of %d' % (len(stale), n))
    print('\n# Battles')
    for side, label in (('d', 'declarer attacking'), ('x', 'target attacking')):
        v = [sum(w['cb'][side][k] for w in main_w) for k in range(10)]
        if not v[0]:
            continue
        print('  %s: %d attacks, won %.0f%%, mean predicted odds %.0f%%, lone attackers %.0f%%, mean group %.1f, on cities %.0f%% (won %.0f%%), collateral units %.0f%%'
              % (label, v[0], pct(v[1], v[0]), v[2] / 10.0 / v[0], pct(v[3], v[0]), v[4] / v[0], pct(v[5], v[0]), pct(v[6], v[5]), pct(v[7], v[0])))
        if v[0]:
            b = [sum(w['cb'][side][k] for w in main_w) for k in (8, 9)]
            print('    with a class bonus over the defender %.0f%%; defender already damaged %.0f%%' % (pct(b[0], v[0]), pct(b[1], v[0])))
    dl = sum((w['cb']['d'][0] - w['cb']['d'][1]) + w['cb']['x'][1] for w in main_w)
    xl = sum(w['cb']['d'][1] + (w['cb']['x'][0] - w['cb']['x'][1]) for w in main_w)
    print('  units lost in battle: declarers %d, targets %d (exchange ratio %.2f)' % (dl, xl, xl / max(1, dl)))
    print('\n# What predicts success (declarer took a city; net cities; exchange ratio)')
    def row(label, ws):
        if not ws:
            return
        dl = sum((w['cb']['d'][0] - w['cb']['d'][1]) + w['cb']['x'][1] for w in ws)
        xl = sum(w['cb']['d'][1] + (w['cb']['x'][0] - w['cb']['x'][1]) for w in ws)
        print('  %-34s wars %3d  took a city %3.0f%%  net cities %+.2f  exchange %.2f' % (
            label, len(ws), pct(sum(1 for w in ws if w['caps']), len(ws)),
            st.mean(len(w['caps']) - len(w['lost']) for w in ws), xl / max(1, dl)))
    for lo, hi in ((0, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 99)):
        row('power ratio %.1f-%.1f' % (lo, hi), [w for w in main_w if lo <= w['ratio'] < hi])
    row('massed: 50%+ of army near target', [w for w in main_w if w['near'] >= 0.5])
    row('partly: 1-49% near', [w for w in main_w if 0 < w['near'] < 0.5])
    row('nothing near', [w for w in main_w if w['nearUnits'] == 0])
    for k in sorted({w['plan'] for w in main_w}):
        row('plan ' + PLANS[k], [w for w in main_w if w['plan'] == k])
    row('target already at war', [w for w in main_w if w['others'] > 0])
    row('target at peace with others', [w for w in main_w if w['others'] == 0])
    row('declarer on two fronts', [w for w in main_w if w['dOther'] > 0])
    lone = [w for w in main_w if w['cb']['d'][0] >= 10]
    if lone:
        lo = [w for w in lone if w['cb']['d'][3] / w['cb']['d'][0] >= 0.5]
        hi = [w for w in lone if w['cb']['d'][3] / w['cb']['d'][0] < 0.5]
        row('mostly lone attackers (10+ attacks)', lo)
        row('mostly stacks (10+ attacks)', hi)
    print('\n# Wars (start, declarer->target, plan, power ratio, near, caps/lost, length)')
    for w in sorted(main_w, key=lambda w: (w['game'], w['start']))[:200]:
        print('  %s t%d %d->%d %s ratio %.2f near %d%% caps %d lost %d len %d%s' % (
            w['game'].split('/')[-2], w['start'], w['d'], w['x'], PLANS[w['plan']], w['ratio'], 100 * w['near'],
            len(w['caps']), len(w['lost']), w['len'], ' ongoing' if w['ongoing'] else ''))


if __name__ == '__main__':
    main(sys.argv[1:])
