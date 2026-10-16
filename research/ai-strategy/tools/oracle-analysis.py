#!/usr/bin/env python3
"""Decision quality of the war AI from the harness's expert oracle (HARNESS_ORACLE).

usage: oracle-analysis.py [--table] <arm dir> [<arm dir> ...]
Each arm dir holds one directory per game with oracle.jsonl (and done.txt when the
game finished). Prints, per arm, measures that do not depend on how well the
opponent plays: what an expert enemy could destroy after each of the AI's turns,
what the AI left undone with its own units, how it chose attackers, and how it
conducted sieges.
"""
import json, os, sys, statistics as st
from collections import defaultdict


def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith('{'):
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    pass
    return rows


def pct(a, b):
    return 100.0 * a / b if b else float('nan')


def arm_stats(arm):
    s = defaultdict(float)
    sieges = []          # per (game, player, city) episode
    games = 0
    for g in sorted(os.listdir(arm)):
        p = os.path.join(arm, g, 'oracle.jsonl')
        if not os.path.exists(os.path.join(arm, g, 'done.txt')) or not os.path.exists(p):
            continue
        games += 1
        rows = load(p)
        episodes = {}    # (player, x, y) -> episode dict, open while the stack stays
        last_turn = {}
        for r in rows:
            o = r.get('o')
            if o == 'after':
                s['war_turns'] += 1
                s['exposed_plots'] += r['exposed']
                s['exposed_units'] += r['units']
                s['loss_units'] += r['lossU']
                s['loss_value'] += r['lossV']
                s['cost_value'] += r['costV']
                s['punish'] += r['punish']
                s['punish_open'] += r['punishOpen']
                s['city_fall'] += r['cityFall']
                s['cities_exposed'] += r['cities']
                s['kill_value'] += r['killV']
                s['lost_value'] += r['lostV']
                if r['punish'] > 0:
                    s['turns_punishable'] += 1
                for e in r['siege']:
                    x, y, owner, d, dmax, nd, na, nsiege, bomb, pnow, lnow, pzero, lzero = e
                    key = (g, r['p'], x, y)
                    ep = episodes.get(key)
                    if ep is None or last_turn.get(key, -9) < r['t'] - 1:
                        ep = {'start': r['t'], 'turns': 0, 'def0': d, 'dmax': dmax, 'bomb_turns': 0,
                              'pnow': [], 'pzero': [], 'defs': [], 'bombrate': [], 'na': []}
                        episodes[key] = ep
                        sieges.append(ep)
                    ep['turns'] += 1
                    ep['defs'].append(d)
                    ep['pnow'].append(pnow)
                    ep['pzero'].append(pzero)
                    ep['bombrate'].append(bomb)
                    ep['na'].append(na)
                    last_turn[key] = r['t']
            elif o == 'before':
                s['before_turns'] += 1
                s['gain'] += r['gain']
                s['gain_kills'] += r['kills']
                if r['gain'] > 0:
                    s['turns_with_chance'] += 1
            elif o == 'atk':
                s['attacks'] += 1
                if 'my' in r:
                    s['val_n'] += 1
                    s['val_abs'] += abs(r['my'] - r['odds'])
                    s['val_close'] += abs(r['my'] - r['odds']) <= 20
                lone = r['group'] == 1
                bad = r['odds'] < 500 and not r['col']
                s['attacks_bad'] += bad
                s['attacks_lone'] += lone
                if r['best'] >= 0 and r['best'] > r['odds'] + 100 and not r['col']:
                    s['attacks_better_alt'] += 1
                if not r['col'] and r['odds'] < 500 and r['best'] >= 500:
                    s['attacks_clear_mistake'] += 1
                if r['city']:
                    s['city_attacks'] += 1
                    if r['def'] > 0 and r['bombLeft'] > 0:
                        s['city_attacks_unbombarded'] += 1
                    if r['def'] > 0:
                        s['city_attacks_def'] += 1
                    if bad:
                        s['city_attacks_bad'] += 1
                if not r['col'] and r['colLeft'] > 0 and r['nd'] >= 2:
                    s['attacks_collateral_unused'] += 1
    return games, s, sieges


def main(arms):
    for arm in arms:
        games, s, sieges = arm_stats(arm)
        name = arm.rstrip('/').split('/')[-1]
        wt = s['war_turns']
        print('== %s: %d games, %d player-turns at war' % (name, games, wt))
        if not wt:
            continue
        print('  An expert enemy, after each of the AI\'s turns at war:')
        print('    could destroy %.1f units (%.0f production) per turn, at a cost of %.0f;' % (
            s['loss_units'] / wt, s['loss_value'] / wt, s['cost_value'] / wt))
        print('    net gain for the expert %.0f per turn, %.0f%% of it against units in the open;' % (
            s['punish'] / wt, pct(s['punish_open'], s['punish'])))
        print('    %.0f%% of the AI\'s war turns leave something an expert would profitably attack;' % pct(s['turns_punishable'], wt))
        print('    of the units within its reach, it could kill %.0f%%; chance a reachable AI city falls: %.1f%%.' % (
            pct(s['loss_units'], s['exposed_units']), pct(s['city_fall'], s['cities_exposed'])))
        bt = s['before_turns']
        if bt:
            print('  With the AI\'s own units, at the start of its turns at war:')
            print('    an expert could destroy %.0f production per turn (%.1f units); the AI destroyed %.0f and lost %.0f in its attacks.' % (
                s['gain'] / bt, s['gain_kills'] / bt, s['kill_value'] / wt, s['lost_value'] / wt))
            print('    share of that opportunity realised: %.0f%%.' % pct(s['kill_value'], s['gain']))
        if s['val_n']:
            print('  Oracle check: its odds differ from the DLL\'s getCombatOdds by %.1f points on average (per mille); within 2 %% in %.0f%% of %d attacks.' % (
                s['val_abs'] / s['val_n'], pct(s['val_close'], s['val_n']), s['val_n']))
        a = s['attacks']
        if a:
            print('  Attacks: %d (%.1f per turn at war)' % (a, a / wt))
            print('    below 50%% odds by a unit without collateral damage: %.0f%%;' % pct(s['attacks_bad'], a))
            print('    another unit on the same plot had 10+ points better odds: %.0f%%;' % pct(s['attacks_better_alt'], a))
            print('    a collateral unit was left unused against 2+ defenders: %.0f%%;' % pct(s['attacks_collateral_unused'], a))
            ca = s['city_attacks']
            if ca:
                print('    on cities: %d; with defences up %.0f%%, of them while a unit there could still bombard %.0f%%; below 50%% odds %.0f%%.' % (
                    ca, pct(s['city_attacks_def'], ca), pct(s['city_attacks_unbombarded'], s['city_attacks_def']), pct(s['city_attacks_bad'], ca)))
        if sieges:
            n = len(sieges)
            long_ = [e for e in sieges if e['turns'] >= 3]
            print('  Sieges (2+ units next to an enemy city): %d episodes, median %d turns' % (n, st.median(e['turns'] for e in sieges)))
            with_bomb = [e for e in sieges if max(e['bombrate']) > 0]
            print('    with a bombard-capable unit: %.0f%%; defences at the first turn median %d%% of %d%%' % (
                pct(len(with_bomb), n), st.median(e['def0'] for e in sieges), st.median(e['dmax'] for e in sieges)))
            zeroed = [e for e in with_bomb if min(e['defs']) == 0 and e['def0'] > 0]
            print('    defences brought to zero during the episode (when they started above zero): %.0f%%' % pct(len(zeroed), len([e for e in with_bomb if e['def0'] > 0])))
            gainz = [e['pzero'][0] - e['pnow'][0] for e in sieges if e['def0'] > 0]
            if gainz:
                print('    capture chance next turn at the first siege turn: %.0f%% as the defences stand, %.0f%% with them at zero' % (
                    100 * st.mean(e['pnow'][0] for e in sieges if e['def0'] > 0), 100 * st.mean(e['pzero'][0] for e in sieges if e['def0'] > 0)))
            hopeless = [e for e in sieges if max(e['pzero']) < 0.1]
            print('    episodes where even with zero defences the stack had under 10%% capture chance on every turn: %.0f%%' % pct(len(hopeless), n))
            if long_:
                print('    episodes of 3+ turns: %d' % len(long_))




def table(arms):
    """One column per arm: the decision-quality measures side by side."""
    rows = [
        ('player-turns at war', lambda s, e: s['war_turns']),
        ('expert could destroy per AI war turn (production)', lambda s, e: s['loss_value'] / s['war_turns']),
        ('expert net gain per AI war turn', lambda s, e: s['punish'] / s['war_turns']),
        ('  of it against units in the open %', lambda s, e: pct(s['punish_open'], s['punish'])),
        ('war turns leaving a profitable target %', lambda s, e: pct(s['turns_punishable'], s['war_turns'])),
        ('reachable AI city taken next turn by an expert %', lambda s, e: pct(s['city_fall'], s['cities_exposed'])),
        ('expert opportunity with own units per turn', lambda s, e: s['gain'] / max(1, s['before_turns'])),
        ('  realised by the AI %', lambda s, e: pct(s['kill_value'], s['gain'])),
        ('AI loss in its own attacks per war turn', lambda s, e: s['lost_value'] / s['war_turns']),
        ('attacks below 50 % by non-collateral units %', lambda s, e: pct(s['attacks_bad'], s['attacks'])),
        ('attacks with a 10+ points better unit on the plot %', lambda s, e: pct(s['attacks_better_alt'], s['attacks'])),
        ('  of which below 50 % while that unit had 50 %+ %', lambda s, e: pct(s['attacks_clear_mistake'], s['attacks'])),
        ('city attacks into standing defences %', lambda s, e: pct(s['city_attacks_def'], s['city_attacks'])),
        ('  of them while a unit could still bombard %', lambda s, e: pct(s['city_attacks_unbombarded'], s['city_attacks_def'])),
        ('city attacks below 50 % %', lambda s, e: pct(s['city_attacks_bad'], s['city_attacks'])),
        ('siege episodes bringing defences to zero %', lambda s, e: pct(len([x for x in e if max(x['bombrate']) > 0 and min(x['defs']) == 0 and x['def0'] > 0]),
                                                                      len([x for x in e if max(x['bombrate']) > 0 and x['def0'] > 0]))),
    ]
    stats = [(a.rstrip('/').split('/')[-1],) + arm_stats(a) for a in arms]
    print('%-55s' % '' + ''.join('%10s' % n[:10] for n, g, s, e in stats))
    print('%-55s' % 'games' + ''.join('%10d' % g for n, g, s, e in stats))
    for label, f in rows:
        vals = []
        for n, g, s, e in stats:
            try:
                vals.append('%10.1f' % f(s, e))
            except (ZeroDivisionError, ValueError):
                vals.append('%10s' % '-')
        print('%-55s' % label + ''.join(vals))


if __name__ == '__main__':
    if sys.argv[1:2] == ['--table']:
        table(sys.argv[2:])
    else:
        main(sys.argv[1:])
