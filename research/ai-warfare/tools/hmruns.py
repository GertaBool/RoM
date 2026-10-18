#!/usr/bin/env python3
"""The human-model experiment: one row per run, outcomes per arm, tests, and fidelity to the human.

usage: hmruns.py extract <campaign dir> <runs.json> <map>=<seat> ...
       hmruns.py report <registry.fig.json> <records.json> <runs.json> <map>=<game.duckdb>:<seat>:<turn> ...
  campaign dir: one directory per run, <map>-<arm>-s<seed>, holding run.jsonl (harness telemetry, one
  record per turn) and done.txt; <map>-<arm>-s<seed>.hm.log beside it for model arms (HarnessHuman.cpp).
  extract reduces each run to the measures below at the turns in TURNS and the model's decision
  turns (hm.log); runs.json is that derived table (no telemetry). report computes the registry from it.
  <turn>: the human's last full turn in that game, where the runs are set against the human.

Per run, for the seat (from the telemetry records):
  score_rank   the seat's place by score among the players alive at turn 300 (1 = first)
  cities, pop, land, techs, power, score   at turn 300
  taken        cities the seat captured from other players (capture events), turns 1-300
  lost         cities other players captured from the seat
  wars_begun   war declarations by the seat's team (war events)
Runs that did not reach turn 300 are counted and left out.
Tests: each model or ablation arm against the control arm of the same map, Welch's t-test on
ranks (exper.py), two-tailed; P(A>B): the probability that a run of the arm beats a control run
(higher value; for score_rank and lost, lower).
Fidelity: the same measures at the human's last full turn, the runs' medians against the human's
own figures from the war log (M lines: cities, pop, score and its rank; X lines: techs; K lines:
cities taken and lost; W lines: declarations), and the turns of the human's civic adoptions and
first war against the model's (hm.log).
"""
import collections, glob, json, math, os, re, statistics, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry
from exper import rank_welch

END = 300
TURNS = [100, 150, 200, 250, 265, 284, 300]


def read_run(path, seat):
    recs = [json.loads(l) for l in open(os.path.join(path, 'run.jsonl'))]
    hdr, turns = recs[0], recs[1:]
    team = next(p['team'] for p in hdr['players'] if p['id'] == seat)
    by_t = {r['t']: r for r in turns}
    taken, lost, wars = collections.Counter(), collections.Counter(), collections.Counter()
    for r in turns:
        for e in r.get('ev', []):
            if 'capture' in e:
                if e['by'] == seat: taken[r['t']] += 1
                if e['from'] == seat: lost[r['t']] += 1
            if 'war' in e and e['war'][0] == team: wars[r['t']] += 1
    return by_t, taken, lost, wars


def at(by_t, taken, lost, wars, seat, t):
    r = by_t.get(t)
    if r is None: return None
    p = {x['id']: x for x in r['p']}
    me = p.get(seat)
    if me is None or me.get('cities', 0) == 0 and t > 10:
        return dict(score_rank=len(p), cities=0, pop=0, land=0, techs=0, power=0, score=0,
                    taken=sum(v for k, v in taken.items() if k <= t), lost=sum(v for k, v in lost.items() if k <= t),
                    wars_begun=sum(v for k, v in wars.items() if k <= t))
    alive = [x for x in p.values() if x.get('cities', 0) > 0]
    rank = 1 + sum(1 for x in alive if x['score'] > me['score'])
    return dict(score_rank=rank, cities=me['cities'], pop=me['pop'], land=me['land'], techs=me['techs'], power=me['power'],
                score=me['score'], taken=sum(v for k, v in taken.items() if k <= t), lost=sum(v for k, v in lost.items() if k <= t),
                wars_begun=sum(v for k, v in wars.items() if k <= t))


# hm.log lines of the war and attack rules (HarnessHuman.cpp), counted per run
WAR_STEPS = [('preparations', ' prepare against '), ('declared_by_rule', ' declare on '), ('wars_entered', ' at war with '),
             ('given_up', 'no declaration in time'), ('peace_made', 'peace made'), ('attacks', ' attack '),
             ('into_empty_city', 'empty city')]
METRICS = ['score_rank', 'cities', 'pop', 'land', 'techs', 'power', 'score', 'taken', 'lost', 'wars_begun']
LOWER_BETTER = {'score_rank', 'lost'}


def extract(camp, out, seats):
    res = []
    for d in sorted(glob.glob(os.path.join(camp, '*-s*'))):
        m = re.fullmatch(r'(.+?)-(.+)-s(\d+)', os.path.basename(d))
        if not os.path.isdir(d) or not m or m.group(1) not in seats or not os.path.exists(os.path.join(d, 'run.jsonl')): continue
        seat = seats[m.group(1)]
        data = read_run(d, seat)
        run = dict(map=m.group(1), arm=m.group(2), seed=int(m.group(3)), last_turn=max(data[0]),
                   at={t: at(*data, seat, t) for t in TURNS if t in data[0]})
        lg = d + '.hm.log'
        if os.path.exists(lg):
            seen, fw, slider = {}, None, []
            steps = collections.Counter()
            for line in open(lg):
                f = line.split()
                for k, pat in WAR_STEPS:
                    if pat in line: steps[k] += 1
                if len(f) > 1 and f[1] == 'civics':
                    for c in f[2:]: seen.setdefault(c.removeprefix('CIVIC_'), int(f[0]))
                if len(f) > 2 and f[1] == 'at' and f[2] == 'war' and fw is None: fw = int(f[0])
            run['civics'] = seen
            run['first_war'] = fw
            run['war_steps'] = dict(steps)
        res.append(run)
    json.dump(res, open(out, 'w'), indent=0)
    print(f'{len(res)} runs', file=sys.stderr)


if sys.argv[1] == 'extract':
    extract(sys.argv[2], sys.argv[3], {a.split('=')[0]: int(a.split('=')[1]) for a in sys.argv[4:]})
    sys.exit(0)
REG, RECS, RUNS = sys.argv[2], sys.argv[3], sys.argv[4]
MAPS = {}
for a in sys.argv[5:]:
    m, rest = a.split('=', 1)
    db, seat, turn = rest.rsplit(':', 2)
    MAPS[m] = (db, int(seat), int(turn))
R = json.load(open(RECS))
runs = collections.defaultdict(list)      # (map, arm) -> [(seed, metrics at END, metrics at human turn, run)]
short = collections.Counter()
for r in json.load(open(RUNS)):
    if r['map'] not in MAPS: continue
    end = r['at'].get(str(END))
    if end is None: short[(r['map'], r['arm'])] += 1; continue
    runs[(r['map'], r['arm'])].append((r['seed'], end, r['at'].get(str(MAPS[r['map']][2])), r))

reg = Registry(REG, [RECS, RUNS] + [v[0] for v in MAPS.values()], R)
arms = sorted({a for _, a in runs}, key=lambda a: (a != 'control', a != 'model', a))
maps = sorted(MAPS)
med = lambda v: round(statistics.median(v), 1) if v else ''
srows = []
for mp in maps:
    db, seat, hturn = MAPS[mp]
    con = duckdb.connect(db, read_only=True)
    sp, hc, w, h = con.execute('select speed, handicap, width, height from wl_H').fetchone()
    civ, leader = con.execute('select civ, leader from wl_P where human=1').fetchone()
    npl = con.execute("select count(*) from wl_P where civ <> 'CIVILIZATION_BARBARIAN'").fetchone()[0]
    srows.append([mp, os.path.basename(db).split('.')[0], seat, civ.removeprefix('CIVILIZATION_'), leader.removeprefix('LEADER_'), sp.removeprefix('GAMESPEED_'),
                  hc.removeprefix('HANDICAP_'), f'{w} x {h}', npl, hturn, END, sum(len(v) for (m, _), v in runs.items() if m == mp)])
reg.result_table('hm_setup', ['map', 'game', 'seat', 'civilization', 'leader', 'speed', 'game_handicap', 'plots', 'players', 'human_last_turn',
                              'turns_played', 'runs'], srows, 'turns', 'every player', 'turn 0', 'H and P lines of the game\'s war log (speed, '
                 'the game\'s handicap, map size, the seats; players: civilizations, the barbarians left out); human_last_turn: its last '
                 'full turn; turns_played: each run from turn 0; runs: runs reaching it, all arms', maps, n=len(maps))
reg.fig('end_turn', END, 'turn', 'every player', f'turn {END}', 'the last turn of every run')
reg.fig('min_runs', 30, 'runs', 'every arm', 'whole campaign', 'runs required per arm and map (CLAUDE.md rule 9; framework.md section 7)')
rows, over = [], []
for mp in maps:
    for arm in arms:
        rs = runs.get((mp, arm))
        if not rs: continue
        over.append(f'{mp} {arm}')
        rows.append([f'{mp} {arm}', len(rs), short[(mp, arm)]] + [med([r[1][k] for r in rs]) for k in METRICS])
reg.result_table('hm_outcomes', ['map_arm', 'runs', 'runs_short', *METRICS], rows, 'cities', 'model seat', f'turn {END}',
                 f'harness telemetry (run.jsonl) of each run in the campaign: medians over runs of the seat at turn {END}; '
                 'score_rank: place by score among players with a city (rank); cities, pop, land, techs, power, score as the telemetry; '
                 'taken, lost: capture events turns 1-300; wars_begun: war events declared by the seat\'s team; runs_short: runs that '
                 f'stopped before turn {END}, left out', over, n=sum(len(v) for v in runs.values()))
trows, tover = [], []
for mp in maps:
    ctl = runs.get((mp, 'control'))
    if not ctl: continue
    for arm in arms:
        if arm == 'control' or (mp, arm) not in runs: continue
        rs = runs[(mp, arm)]
        for k in METRICS:
            a, b = [r[1][k] for r in rs], [r[1][k] for r in ctl]
            t = df = p = None; A = 0.5
            if len(set(a + b)) >= 2 and min(len(a), len(b)) >= 2:
                t, df, p, A = rank_welch(a, b)
                if math.isnan(t): t = df = p = None
            if k in LOWER_BETTER: A = 1 - A
            tover.append(f'{mp} {arm} {k}')
            trows.append([f'{mp} {arm} {k}', len(a), len(b), med(a), med(b), round(t, 2) if t is not None else '',
                          round(df, 1) if df is not None else '', f'{p:.3g}' if p is not None else '', round(A, 3),
                          'anecdote' if min(len(a), len(b)) < 30 else 'result'])
for mp in maps:
    for arm in arms:
        rs = runs.get((mp, arm))
        if not rs: continue
        for k in ('score_rank', 'cities', 'pop', 'techs', 'taken'):
            reg.fig(f'med_{mp}_{arm.replace("-", "_").replace("+", "_")}_{k}', med([r[1][k] for r in rs]), {'score_rank': 'rank', 'pop': 'citizens', 'techs': 'techs'}.get(k, 'cities'),
                    'model seat', f'turn {END}', f'median over the {len(rs)} runs of arm {arm} on map {mp} (hm_outcomes)', n=len(rs))
for r in trows:
    key = r[0].replace(' ', '_').replace('-', '_').replace('+', '_')
    reg.fig(f'p_{key}', r[7] or '-', 'share', 'model seat', f'turn {END}', 'two-tailed p of the rank Welch test (hm_tests)', n=r[1] + r[2])
    reg.fig(f'A_{key}', r[8], 'share', 'model seat', f'turn {END}', 'chance that an arm run is better than a control run (hm_tests)', n=r[1] + r[2])
reg.result_table('hm_tests', ['arm_metric', 'n_arm', 'n_control', 'median_arm', 'median_control', 't', 'dof', 'p', 'p_arm_better', 'status'],
                 trows, 'cities', 'model seat', f'turn {END}', 'exper.rank_welch: Welch\'s t-test on pooled ranks, arm against the control '
                 'of the same map; p_arm_better: Vargha-Delaney A, the chance that a run of the arm is better than a control run (lower is better '
                 'for score_rank and lost); status: "anecdote" when either side has fewer than 30 runs (CLAUDE.md rule 9); units per metric as '
                 'in hm_outcomes', tover, n=sum(len(v) for v in runs.values()))

# fidelity at the human's last full turn
frows, fover = [], []
for mp in maps:
    db, seat, hturn = MAPS[mp]
    con = duckdb.connect(db, read_only=True)
    hp = con.execute('select player from wl_P where human=1').fetchone()[0]
    m = con.execute('select cities, pop, score from wl_M where player=? and turn=?', [hp, hturn]).fetchone()
    srank = 1 + con.execute('select count(*) from wl_M where turn=? and score>? and cities>0', [hturn, m[2]]).fetchone()[0]
    techs = con.execute('select count(distinct tech) from wl_X where player=? and turn<=?', [hp, hturn]).fetchone()[0]
    taken = con.execute('select count(*) from wl_K where new_owner=? and turn<=?', [hp, hturn]).fetchone()[0]
    lost = con.execute('select count(*) from wl_K where old_owner=? and turn<=?', [hp, hturn]).fetchone()[0]
    team = con.execute('select team from wl_P where human=1').fetchone()[0]
    wars = con.execute('select count(*) from wl_W where team=? and turn<=?', [team, hturn]).fetchone()[0]
    human = dict(score_rank=srank, cities=m[0], pop=m[1], techs=techs, score=m[2], taken=taken, lost=lost, wars_begun=wars)
    for arm in arms:
        rs = [r for r in runs.get((mp, arm), []) if r[2] is not None]
        if not rs: continue
        for k in ['score_rank', 'cities', 'pop', 'techs', 'taken', 'lost', 'wars_begun']:
            v = [r[2][k] for r in rs]
            fover.append(f'{mp} {arm} {k}')
            frows.append([f'{mp} {arm} {k}', len(v), human[k], med(v), min(v), max(v),
                          sum(1 for x in v if (x <= human[k] if k in LOWER_BETTER else x >= human[k]))])
reg.result_table('hm_fidelity', ['map_arm_metric', 'runs', 'human', 'runs_median', 'runs_min', 'runs_max', 'runs_at_or_beyond_human'], frows,
                 'cities', 'model seat and human', 'the human\'s last full turn', 'the runs at the human\'s last full turn of the game (telemetry) '
                 'against the human\'s war log at that turn (M lines: cities, pop, score; rank by score among players with a city; X lines: techs '
                 'held; K lines: cities taken and lost; W lines: declarations by its team); runs_at_or_beyond_human: runs as good as the human '
                 'or better (lower for score_rank and lost); techs in the telemetry and X lines count the same TechInfo records', fover,
                 n=sum(len(v) for v in runs.values()))

# the course of the game: medians of the runs at fixed turns against the human's war log
jrows, jover = [], []
for mp in maps:
    db, seat, hturn = MAPS[mp]
    con = duckdb.connect(db, read_only=True)
    hp = con.execute('select player from wl_P where human=1').fetchone()[0]
    for t in [x for x in TURNS if x <= hturn and x not in (265, 284)]:
        m = con.execute('select cities, pop, score from wl_M where player=? and turn=?', [hp, t]).fetchone()
        rk = 1 + con.execute('select count(*) from wl_M where turn=? and score>? and cities>0', [t, m[2]]).fetchone()[0]
        te = con.execute('select count(distinct tech) from wl_X where player=? and turn<=?', [hp, t]).fetchone()[0]
        jover.append(f'{mp} {t} human'); jrows.append([f'{mp} {t} human', 1, rk, m[0], m[1], te])
        for arm in arms:
            v = [r[3]['at'].get(str(t)) for r in runs.get((mp, arm), [])]
            v = [x for x in v if x]
            if not v: continue
            jover.append(f'{mp} {t} {arm}')
            jrows.append([f'{mp} {t} {arm}', len(v), med([x['score_rank'] for x in v]), med([x['cities'] for x in v]), med([x['pop'] for x in v]),
                          med([x['techs'] for x in v])])
reg.result_table('hm_trajectory', ['map_turn_side', 'runs', 'score_rank', 'cities', 'pop', 'techs'], jrows, 'cities', 'model seat and human',
                 'turns 100, 150, 200 and 250', 'human: its M lines at the turn (cities, pop, score; rank among players with a city) and X lines '
                 '(techs held); arms: medians over runs of the seat in the telemetry at the turn; pop in citizens, techs in techs, score_rank a rank',
                 jover, n=len(jrows))

# the war rules step by step (hm.log), against the human's own wars and attacks
hrows, hover = [], []
for mp in maps:
    db, seat, hturn = MAPS[mp]
    con = duckdb.connect(db, read_only=True)
    hp, team = con.execute('select player, team from wl_P where human=1').fetchone()
    human = dict(declared_by_rule=con.execute('select count(*) from wl_W where team=?', [team]).fetchone()[0],
                 peace_made=con.execute('select count(*) from wl_Q where team=?', [team]).fetchone()[0],
                 attacks=con.execute('select count(*) from wl_C where att=?', [hp]).fetchone()[0])
    for arm in arms:
        rl = [r[3] for r in runs.get((mp, arm), []) if 'war_steps' in r[3]]
        if not rl: continue
        for k, _ in WAR_STEPS:
            v = [r['war_steps'].get(k, 0) for r in rl]
            hover.append(f'{mp} {arm} {k}')
            hrows.append([f'{mp} {arm} {k}', len(v), human.get(k, '-'), med(v), min(v), max(v), sum(v)])
reg.result_table('hm_war_steps', ['map_arm_step', 'runs', 'human', 'runs_median', 'runs_min', 'runs_max', 'runs_total'], hrows, 'turns',
                 'model seat and human', 'whole game', 'per run, the hm.log lines of each step of the war and attack rules (preparations '
                 'begun, declarations by the rule, wars entered whoever declared, preparations given up, peace made by the rule, attacks '
                 'and walks into empty cities by the attack rule); the human: its declarations (W lines), peace made (Q lines of its team) '
                 'and attacks (C lines) over its whole game; every column counts events', hover, n=len(hrows))

# decision timing (hm.log) against the human: civic adoptions and the first war
CI = {k.removeprefix('CIVIC_'): v['CivicOptionType'] for k, v in R['CivicInfo'].items()}
drows, dover = [], []
for mp in maps:
    db, seat, hturn = MAPS[mp]
    con = duckdb.connect(db, read_only=True)
    hp, team = con.execute('select player, team from wl_P where human=1').fetchone()
    hciv = {}
    held = None
    for t, l in con.execute("select turn, arg_max(a1, seq) from wl_A where player=? and kind='CIVICS' group by 1 order by 1", [hp]).fetchall():
        for c in [x.removeprefix('CIVIC_') for x in l.split(',') if x]:
            hciv.setdefault(c, t)
    hwar = con.execute('select min(turn) from wl_W where team=?', [team]).fetchone()[0]
    for arm in arms:
        rl = [r[3] for r in runs.get((mp, arm), []) if 'civics' in r[3]]
        if not rl: continue
        logs = rl
        adopt = collections.defaultdict(list)
        first_war = [r.get('first_war') for r in rl]
        for r in rl:
            for c, t in r['civics'].items(): adopt[c].append(t)
        for c in sorted(hciv, key=lambda c: (hciv[c], c)):
            if hciv[c] <= 2: continue
            v = adopt.get(c, [])
            dover.append(f'{mp} {arm} {c}')
            drows.append([f'{mp} {arm} {c}', hciv[c], len(v), len(logs), med(v), min(v) if v else '', max(v) if v else ''])
        fw = [x for x in first_war if x is not None]
        dover.append(f'{mp} {arm} first war')
        drows.append([f'{mp} {arm} first war', hwar, len(fw), len(logs), med(fw), min(fw) if fw else '', max(fw) if fw else ''])
civs = sorted({r[0].split()[-1] for r in drows if not r[0].endswith('first war')})
reg.result_table('hm_timing', ['map_arm_decision', 'human_turn', 'runs_with_it', 'runs', 'runs_median_turn', 'runs_min', 'runs_max'], drows,
                 'turn', 'model seat and human', 'whole game', 'the turn of each civic the human adopted after turn 2 (CIVICS commands, A '
                 'lines; first command naming it) and of its first declaration (W lines), against the model runs\' hm.log: the first '
                 '"civics" line naming the civic, the first "at war" line', dover, n=len(dover), xml='CivicInfo', xml_vals=civs)
reg.save()
for k in ('hm_outcomes',):
    for r in reg.figs[k]['rows']: print(r, file=sys.stderr)
