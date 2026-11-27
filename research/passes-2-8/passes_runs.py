#!/usr/bin/env python3
"""The figures of the P18 and P19 harness runs: c08a472 (before pass 2) against ede81881b7de (GitLab main).

usage: passes_runs.py <registry.fig.json> <runs root>
  runs root: <root>/P18/{a,b}/s<seed> and <root>/P19/{a,b}/s<seed>, each with run.jsonl and run.log
  (toolchain/harness telemetry). P18 arm a and P19 arm b are c08a472; P18 arm b and P19 arm a are main
  (method/mission/register.json). Figures pool the 20 runs of each commit, except the test of P18,
  which uses P18's own runs as the ledger does.
Reads only: telemetry fields agenda, trouble, plans, ops and gov of every AI player on every turn record,
the ms of every turn record, and the RESULT line of run.log. Writes the registry (method/figlib.py).
"""
import glob, json, os, statistics, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'method'))
from figlib import Registry
from stats import rank_welch

GOV = ['Steward', 'Agriculturalist', 'Harbourmaster', 'Merchant', 'Industrialist', 'Scholar', 'Curator', 'Castellan',
       'Colonial']
AGENDA = ['Survive', 'Recover', 'Expand land', 'Expand maritime', 'Consolidate', 'Power spike', 'Conquest', 'Science',
          'Culture']
COMMITS = {'c08a472': [('P18', 'a'), ('P19', 'b')], 'main': [('P18', 'b'), ('P19', 'a')]}
WHO = 'every AI player of the Mediterranean scenario (10 players, all AI)'
TURN = 'turns 1 to 350, Marathon'


def turn_records(d):
    return [json.loads(l) for l in open(os.path.join(d, 'run.jsonl')) if l.startswith('{"t"')]


def main():
    out, root = sys.argv[1], sys.argv[2]
    dirs = {c: sorted(d for p, a in arms for d in glob.glob(os.path.join(root, p, a, 's*'))) for c, arms in COMMITS.items()}
    inputs = [os.path.join(d, f) for ds in dirs.values() for d in ds for f in ('run.jsonl', 'run.log')]
    R = Registry(out, inputs)
    src = 'toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py'
    S = {}
    for c, ds in dirs.items():
        s = dict(runs=len(ds), done=0, pt=0, plans=0, ops=0, trouble=0, gov=[0] * 10, agenda=[0] * 9, secs=[])
        for d in ds:
            s['done'] += int('RESULT' in open(os.path.join(d, 'run.log'), errors='replace').read())
            recs = turn_records(d)
            s['secs'].append(sum(r.get('ms', 0) for r in recs) / 1000.0)
            for r in recs:
                for p in r.get('p', []):
                    if 'gov' not in p: continue
                    s['pt'] += 1
                    s['plans'] += int(p['plans'] > 0)
                    s['ops'] += p['ops']
                    s['trouble'] += p['trouble']
                    s['gov'] = [x + y for x, y in zip(s['gov'], p['gov'])]
                    if 0 <= p['agenda'] < 9: s['agenda'][p['agenda']] += 1
        S[c] = s
    cs = list(COMMITS)
    for c in cs:
        R.fig(f'runs_{c}', S[c]['runs'], 'runs', WHO, TURN, src)
        R.fig(f'done_{c}', S[c]['done'], 'runs', WHO, 'turn 350', src + ': runs whose run.log has the RESULT line')
        R.fig(f'pt_{c}', S[c]['pt'], 'turns', WHO, TURN, src + ': player-turn records with the new fields')
        R.fig(f'secs_median_{c}', round(statistics.median(S[c]['secs']), 1), 'seconds', 'the harness run',
              TURN, src + ': sum of the turn records\' ms, median over the runs')
    pct = lambda x, n: round(1000.0 * x / n, 1) if n else 0
    R.result_table('state', ['measure'] + cs,
                   [['player-turns under a war plan'] + [pct(S[c]['plans'], S[c]['pt']) for c in cs],
                    ['player-turns in financial trouble'] + [pct(S[c]['trouble'], S[c]['pt']) for c in cs],
                    ['active operations, summed over player-turns'] + [pct(S[c]['ops'], S[c]['pt']) for c in cs]],
                   'per mille', WHO, TURN, src + ': per mille of player-turns (operations: per thousand player-turns)',
                   over=['player-turns under a war plan', 'player-turns in financial trouble',
                         'active operations, summed over player-turns'],
                   n=sum(S[c]['pt'] for c in cs))
    R.result_table('agenda', ['agenda'] + cs,
                   [[AGENDA[i]] + [pct(S[c]['agenda'][i], sum(S[c]['agenda'])) for c in cs] for i in range(9)],
                   'per mille', WHO, TURN, src + ': per mille of player-turns with an agenda', over=AGENDA,
                   n=sum(sum(S[c]['agenda']) for c in cs))
    R.result_table('governor', ['governor'] + cs,
                   [[GOV[i]] + [pct(S[c]['gov'][i], sum(S[c]['gov'][:9])) for c in cs] for i in range(9)],
                   'per mille', 'every AI city with a governor', TURN, src + ': per mille of city-turns with a governor',
                   over=GOV, n=sum(sum(S[c]['gov'][:9]) for c in cs))
    p18a = [sum(r.get('ms', 0) for r in turn_records(d)) / 1000.0 for d in sorted(glob.glob(os.path.join(root, 'P18', 'a', 's*')))]
    p18b = [sum(r.get('ms', 0) for r in turn_records(d)) / 1000.0 for d in sorted(glob.glob(os.path.join(root, 'P18', 'b', 's*')))]
    t, df, p, A = rank_welch(p18a, p18b)
    R.fig('p18_p', round(p, 4), 'share', 'the harness run', TURN,
          'method/stats.py rank_welch on P18 arm a (c08a472) against arm b (main), seconds per run', n=len(p18a) + len(p18b))
    R.fig('p18_A', round(A, 2), 'share', 'the harness run', TURN,
          'Vargha-Delaney A of P18 arm a over arm b (probability that a run of c08a472 takes longer)', n=len(p18a) + len(p18b))
    R.save()


if __name__ == '__main__':
    main()
