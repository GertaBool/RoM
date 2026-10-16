#!/usr/bin/env python3
"""Compare arms of a harness experiment: wars, battles, assaults and game outcomes.

usage: ab-compare.py ARM_DIR [ARM_DIR ...]
Each ARM_DIR holds one folder per game with a run.jsonl (as written by the harness
in scenario mode). Prints one column per arm. Needs war-analysis.py and
assault-analysis.py next to this file.
"""
import importlib.util, json, os, sys, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), os.path.join(HERE, name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


wa = load('war-analysis')
aa = load('assault-analysis')


def pct(n, d):
    return 100.0 * n / d if d else float('nan')


def game_stats(path):
    hdr, recs = wa.load(path)
    civ_teams = {p['team'] for p in hdr['players']}
    team = {p['id']: p['team'] for p in hdr['players']}
    caps = elim = 0
    for r in recs:
        for e in r.get('ev', []):
            if 'capture' in e and team.get(e['from']) in civ_teams and team.get(e['by']) in civ_teams:
                caps += 1
            if 'eliminated' in e:
                elim += 1
    last = recs[-1]
    scores = sorted((p['score'] for p in last['p']), reverse=True)
    share = 100.0 * scores[0] / max(1, sum(scores))
    ms = [r.get('ms', 0) for r in recs[-50:]]
    cities = sorted((p.get('cities', 0) for p in last['p']), reverse=True)
    return {'caps': caps, 'elim': elim, 'share': share, 'ms': st.mean(ms) if ms else 0, 'turns': last['t'],
            'top_cities': cities[0] if cities else 0, 'civ_teams': civ_teams}


def arm_metrics(arm_dir):
    paths = sorted(os.path.join(arm_dir, g, 'run.jsonl') for g in os.listdir(arm_dir)
                   if os.path.exists(os.path.join(arm_dir, g, 'done.txt')))
    wars, assaults, games = [], [], []
    for p in paths:
        w, _ = wa.wars_of(p)
        wars += [x for x in w if not x['vassal']]
        g = game_stats(p)
        games.append(g)
        assaults += [a for a in aa.assaults_of(p) if a['as'][0] in g['civ_teams']]
    m = {'games': len(paths)}
    n = len(wars)
    m['wars per game'] = n / max(1, len(paths))
    m['declared below power ratio 1.0 %'] = pct(sum(w['ratio'] < 1 for w in wars), n)
    m['declared with nothing near %'] = pct(sum(w['nearUnits'] == 0 for w in wars), n)
    m['army near target at declaration, median %'] = 100 * st.median([w['near'] for w in wars]) if wars else float('nan')
    m['dogpiles %'] = pct(sum(w['plan'] == 6 for w in wars), n)
    m['wars that take a city %'] = pct(sum(1 for w in wars if w['caps']), n)
    m['net cities per war'] = st.mean(len(w['caps']) - len(w['lost']) for w in wars) if wars else float('nan')
    first = [w['caps'][0][0] - w['start'] for w in wars if w['caps']]
    m['turns to first capture, median'] = st.median(first) if first else float('nan')
    ended = [w for w in wars if not w['ongoing']]
    m['ended wars: median length'] = st.median([w['len'] for w in ended]) if ended else float('nan')
    m['ended wars with no city changing hands %'] = pct(sum(1 for w in ended if not w['caps'] and not w['lost']), len(ended))
    m['stalemates (50+ turns, no city) per game'] = sum(1 for w in wars if w['len'] >= 50 and not w['caps'] and not w['lost']) / max(1, len(paths))
    v = [sum(w['cb']['d'][k] for w in wars) for k in range(8)]
    m['declarer battles won %'] = pct(v[1], v[0])
    m['declarer lone attacks %'] = pct(v[3], v[0])
    dl = sum((w['cb']['d'][0] - w['cb']['d'][1]) + w['cb']['x'][1] for w in wars)
    xl = sum(w['cb']['d'][1] + (w['cb']['x'][0] - w['cb']['x'][1]) for w in wars)
    m['exchange ratio (target losses per declarer loss)'] = xl / max(1, dl)
    na = len(assaults)
    m['assault turns per game'] = na / max(1, len(paths))
    m['assaults that take the city %'] = pct(sum(a['taken'] for a in assaults), na)
    m['units lost per city taken in assaults'] = sum(a['n'] - a['w'] for a in assaults) / max(1, sum(a['taken'] for a in assaults))
    m['assaults with walls bombarded that turn %'] = pct(sum(a['bomb'][0] > 0 for a in assaults), na)
    m['assaults with walls at most 1/4 %'] = pct(sum(1 for a in assaults if a['def'][0] > 0 and 4 * a['def'][2] <= a['def'][0]), na)
    m['assaults with ranged strikes %'] = pct(sum(a['bomb'][3] > 0 for a in assaults), na)
    m['assaults opened by collateral %'] = pct(sum(a['col1'] for a in assaults), na)
    m['assaults with siege or collateral in stack %'] = pct(sum(1 for a in assaults if a.get('st', {}).get('SIEGE', 0) or a['cu']), na)
    m['median assault stack'] = st.median([a['units'] for a in assaults]) if assaults else float('nan')
    m['cities captured between civs per game'] = st.mean(g['caps'] for g in games)
    m['civs eliminated per game'] = st.mean(g['elim'] for g in games)
    m['leader score share at the end %'] = st.mean(g['share'] for g in games)
    m['turn time, last 50 turns (ms)'] = st.mean(g['ms'] for g in games)
    return m


def main(dirs):
    cols = [(os.path.basename(d.rstrip('/')), arm_metrics(d)) for d in dirs]
    keys = list(cols[0][1].keys())
    w = max(len(k) for k in keys)
    print(' ' * w + ''.join('%10s' % c for c, _ in cols))
    for k in keys:
        cells = []
        for _, m in cols:
            x = m[k]
            cells.append('%10s' % (('%d' % x) if isinstance(x, int) else ('%.2f' % x if abs(x) < 10 else '%.1f' % x)))
        print(k.ljust(w) + ''.join(cells))


if __name__ == '__main__':
    main(sys.argv[1:])
