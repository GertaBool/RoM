#!/usr/bin/env python3
"""Paired comparison of two campaign sets (same maps, speeds and seeds).

usage: dipl_compare.py SET_A_DIR SET_B_DIR [OUT.json]
Each set dir holds <map>-<SPEED>-<seed>/run.jsonl. Prints per-run metrics side
by side and the mean paired difference with a sign count.
"""
import collections
import json
import os
import statistics as st
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
_spec = importlib.util.spec_from_file_location("dipl_analyze", os.path.join(os.path.dirname(os.path.abspath(__file__)), "dipl-analyze.py"))
_mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
analyse, ITEM = _mod.analyse, _mod.ITEM

TRADE_KINDS = {
    'tech swap': lambda a, b: a == {'TECH'} and b == {'TECH'},
    'tech for gold': lambda a, b: (a == {'TECH'} and b == {'GOLD'}) or (a == {'GOLD'} and b == {'TECH'}),
    'resource swap': lambda a, b: a == {'RES'} and b == {'RES'},
    'resource for gold/turn': lambda a, b: (a == {'RES'} and b == {'GPT'}) or (a == {'GPT'} and b == {'RES'}),
    'gift': lambda a, b: not a or not b,
    'peace': lambda a, b: 'PEACE' in a | b or 'PEACE_TREATY' in a | b,
    'open borders': lambda a, b: a == {'OB'} and b == {'OB'},
    'defensive pact': lambda a, b: 'DP' in a | b,
    'vassal/capitulation': lambda a, b: 'VASSAL' in a | b or 'SURRENDER' in a | b,
    'war hire': lambda a, b: 'WAR' in a | b,
    'maps': lambda a, b: a == {'MAPS'} or b == {'MAPS'},
}


def kinds(item_lists):
    return set(ITEM[i[0]] if 0 <= i[0] < len(ITEM) else str(i[0]) for i in item_lists)


def metrics(run_dir):
    r = analyse(run_dir)
    rows = [json.loads(l) for l in open(os.path.join(run_dir, 'run.jsonl'))]
    turns = [x for x in rows[1:] if 'p' in x]
    span = max(1, r['last'] - r['first'])
    m = collections.OrderedDict()
    m['turns'] = r['last']
    trades = collections.Counter()
    for t in turns:
        for e in t.get('ev', []):
            if 'trade' in e:
                a, b = kinds(e['ai']), kinds(e['bi'])
                for name, test in TRADE_KINDS.items():
                    if test(a, b):
                        trades[name] += 1
                        break
                else:
                    trades['other'] += 1
    total_trades = sum(trades.values())
    m['trades/100t'] = round(100.0 * total_trades / span, 1)
    for name in list(TRADE_KINDS) + ['other']:
        m['  ' + name] = round(100.0 * trades[name] / span, 2)
    wars = r['wars']
    m['wars/100t'] = round(100.0 * len(wars) / span, 2)
    ended = [w for w in wars if w['end'] is not None]
    m['war length (median)'] = st.median([w['end'] - w['start'] for w in ended]) if ended else None
    m['power ratio at declaration (median)'] = st.median([w['power_ratio'] for w in wars]) if wars else None
    caps = [sum(int(v) for k, v in w['captures'].items() if int(k) == w['attacker']) for w in wars]
    m['cities taken by attacker per war'] = round(st.mean(caps), 2) if caps else None
    m['wars won by attacker (took a city)'] = round(sum(1 for c in caps if c > 0) / len(caps), 2) if caps else None
    # wars declared on the score leader of the declaration turn
    by_turn = {x['t']: x for x in turns}
    on_leader = 0
    for w in wars:
        x = by_turn.get(w['start'])
        if x is None:
            continue
        team_score = collections.Counter()
        team_of = {p['id']: p['team'] for p in rows[0]['players']}
        for p in x['p']:
            team_score[team_of.get(p['id'], p['id'])] += p['score']
        leader_team = team_score.most_common(1)[0][0]
        on_leader += w['defender'] == leader_team
    m['share of wars declared on the score leader'] = round(on_leader / len(wars), 2) if wars else None
    last = turns[-1]
    scores = sorted((p['score'] for p in last['p']), reverse=True)
    m['top score share at end'] = round(scores[0] / max(1, sum(scores)), 2)
    m['players alive at end'] = len(last['p'])
    t, met, ob, dp, vas, war = r['prevalence'][-1] if r['prevalence'] else (0, 0, 0, 0, 0, 0)
    m['vassal pairs at end'] = vas
    m['open borders pairs at end'] = ob
    m['defensive pacts at end'] = dp
    m['mean techs at end'] = round(st.mean(p['techs'] for p in last['p']), 1)
    m['total cities at end'] = sum(p['cities'] for p in last['p'])
    m['player-turns in financial trouble %'] = round(100.0 * sum(p['trouble'] for x in turns for p in x['p']) / max(1, sum(len(x['p']) for x in turns)), 1)
    m['victory'] = '%s@%d' % (last['victory'], last['t']) if last['state'] == 2 else '-'
    return m


def main():
    set_a, set_b = sys.argv[1], sys.argv[2]
    runs = sorted(set(os.listdir(set_a)) & set(os.listdir(set_b)))
    res = {}
    for run in runs:
        try:
            res[run] = (metrics(os.path.join(set_a, run)), metrics(os.path.join(set_b, run)))
        except Exception as e:  # incomplete runs are listed, not fatal
            print('skip', run, e)
    if len(sys.argv) > 3:
        json.dump(res, open(sys.argv[3], 'w'), indent=1)
    names = [os.path.basename(set_a.rstrip('/')), os.path.basename(set_b.rstrip('/'))]
    keys = list(next(iter(res.values()))[0].keys()) if res else []
    for run, (a, b) in res.items():
        print('== %s (%s vs %s)' % (run, names[0], names[1]))
        for k in keys:
            print('  %-42s %10s %10s' % (k, a[k], b[k]))
    print('== paired over %d runs: mean of %s, mean of %s, mean difference, runs with %s higher / lower' % (len(res), names[0], names[1], names[1]))
    for k in keys:
        pairs = [(a[k], b[k]) for a, b in res.values() if isinstance(a[k], (int, float)) and isinstance(b[k], (int, float))]
        if not pairs:
            continue
        ma, mb = st.mean(p[0] for p in pairs), st.mean(p[1] for p in pairs)
        up = sum(1 for p in pairs if p[1] > p[0]); down = sum(1 for p in pairs if p[1] < p[0])
        print('  %-42s %10.2f %10.2f %+9.2f   %d/%d' % (k, ma, mb, mb - ma, up, down))


if __name__ == '__main__':
    main()
