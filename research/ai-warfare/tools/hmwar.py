"""The human's war decisions, each with the state the human saw (study/model.md).

usage: hmwar.py <out dir> <registry.fig.json> <game.duckdb>:<player> [...]
       hmwar.py --selftest
       (run with ~/.cache/rom-ana/bin/python; databases from extract.py, from logs written by the
       war-log snapshot DLL: lines I L J O. A game without I lines for the player is skipped.)

The state of a decision is what the player had and saw as its turn began: the I header of that
turn start (new_turn = 1) and the L, J and O lines after it. The decision is what the player did
before its next I line. Cases, one row per decision, go to <out dir>/<game>/cases_<class>.csv
(label y and binary cues, read by models.py) and war_<class>.csv (the same cases with the
continuous cues kept). Classes:

  declare   each turn start at which the player has met a team it is not at war with that holds a
            city in a J line (a candidate). y = 1 if the player's team declares war (W line) before
            the next turn start. Cues: best capture chance within 3 and within 1 plot over the
            candidates (capture3, capture1, per mille), its units within 3 plots of that city,
            already at war with someone, open borders with that city's team, that team at war
            with a third team (W and Q lines so far).
  target    each declaration: the options are the candidate teams of that turn start, the choice
            the declared-on team. A declaration on a team with no J city is counted as out of
            reach and left out of the comparison.
  assault   each turn start at war, for each enemy city with a unit of the player within 1 plot:
            y = 1 if the player attacks that city's plot before the next turn start. Cues:
            capture1, its defence %, defence fallen since the last turn start (bombarded), a
            siege unit of the player within 1 plot.
  peace     each turn start, for each team at war with the player: y = 1 if peace is made (Q
            line) before the next turn start. Cues: a city of that team within reach at an even
            chance (capture3 >= 500), a city of it taken since the war began (K lines).

Models fitted here, each leaving one game out in turn (Gigerenzer, Hertwig and Pachur,
Heuristics, chapter 1: few free parameters, judged on data not used to fit them):
  satisficing  y = 1 when the cue is at least the aspiration level q (Simon 1955, in Heuristics,
               chapter 1); q is the observed cue value that maximises hits on the training games.
  hazard       a discrete-time hazard: the chance of y = 1 at a case is logistic in the cue
               (a + b cue), fitted by maximum likelihood (Newton's method).
  base rate    the training games' share of y = 1 at every case.
Scored on the held-out game by hits (satisficing) and by log score (hazard, base rate).
Target choice: maximum-likelihood strategy classification (Broeder; Heuristics, chapter 17; the
formula of strategy.py), strategies: highest capture3, most units near, satisficing (the
candidate with the most units near among those at capture3 >= q, q fitted on the declare cases
of the other games), and guessing.
Figures written: per game the cases and declarations, and every fit, to the registry.
"""
import collections, csv, math, os, sys

EVEN = 500  # per mille: an even chance, the fixed boundary of the binary capture cues


def turn_starts(con, player):
    """[(seq, turn, end seq)] of the player's new-turn starts; end is its next I line (any kind)."""
    rows = con.execute('select seq, turn, new_turn from wl_I where player = ? order by seq', [player]).fetchall()
    out = []
    for i, (seq, turn, new) in enumerate(rows):
        if not new: continue
        end = rows[i + 1][0] if i + 1 < len(rows) else 10 ** 15
        out.append((seq, turn, end))
    return out


def teams(con):
    return dict(con.execute('select player, team from wl_P').fetchall())


def wars_between(con):
    """[(seq, team, target, is_war)] in log order, both directions implied."""
    w = con.execute("select seq, team, target, 1 from wl_W union all select seq, team, target, 0 from wl_Q order by 1").fetchall()
    return w


def war_state(events, upto):
    """Pairs of teams at war after the events before seq upto (W and Q lines only)."""
    at = set()
    for seq, a, b, war in events:
        if seq >= upto: break
        pair = frozenset((a, b))
        if war: at.add(pair)
        else: at.discard(pair)
    return at


def build(con, player, siege_units):
    """The case rows of every class for one game."""
    T = teams(con)
    me = T[player]
    events = wars_between(con)
    starts = turn_starts(con, player)
    cases = collections.defaultdict(list)
    declared_out_of_reach = 0
    prev_def = {}
    for seq, turn, end in starts:
        O = {r[0]: r[1:] for r in con.execute('select team, war, open_borders from wl_O where player = ? and seq > ? and seq < ?',
                                              [player, seq, end]).fetchall()}
        J = con.execute('select owner, x, y, def_mod, near1, near3, capture1, capture3, seq from wl_J where player = ? and seq > ? '
                        'and seq < ? order by seq', [player, seq, end]).fetchall()
        mine = con.execute('select unit, x, y from wl_L where viewer = ? and owner = ? and seq > ? and seq < ?',
                           [player, player, seq, end]).fetchall()
        decl = con.execute('select seq, target from wl_W where team = ? and seq > ? and seq < ? order by seq', [me, seq, end]).fetchall()
        peace = {t for (t,) in con.execute('select target from wl_Q where team = ? and seq > ? and seq < ? union '
                                           'select team from wl_Q where target = ? and seq > ? and seq < ?',
                                           [me, seq, end, me, seq, end]).fetchall()}
        attacked = {(x, y) for x, y in con.execute('select x, y from wl_C where att = ? and seq > ? and seq < ?',
                                                   [player, seq, end]).fetchall()}
        at = war_state(events, seq)
        at_war_any = any(v[0] for v in O.values())
        # candidates: met (an O line), not at war, holding a city in a J line
        cand = collections.defaultdict(list)
        for owner, x, y, dm, n1, n3, c1, c3, jseq in J:
            t = T.get(owner)
            if t in O and not O[t][0]:
                cand[t].append((c3, c1, n3, x, y))
        if cand:
            best_t, best = max(((t, max(v)) for t, v in cand.items()), key=lambda tv: (tv[1][0], tv[1][2]))
            c3, c1, n3 = best[0], max(c[1] for c in cand[best_t]), best[2]
            engaged = any(best_t in p and me not in p for p in at)
            row = dict(seq=seq, turn=turn, y=int(bool(decl)), capture3=c3, capture1=c1, near3=n3, at_war=int(at_war_any),
                       open_borders=int(bool(O[best_t][1])), engaged=int(engaged), candidates=len(cand))
            cases['declare'].append(row)
        for dseq, target in decl:
            if target not in cand:
                declared_out_of_reach += 1
                continue
            opts = {t: dict(capture3=max(c[0] for c in v), near3=max(c[2] for c in v)) for t, v in cand.items()}
            cases['target'].append(dict(seq=dseq, turn=turn, choice=target, options=opts))
        # assault and peace: enemies per O
        enemies = {t for t, v in O.items() if v[0]}
        for owner, x, y, dm, n1, n3, c1, c3, jseq in J:
            t = T.get(owner)
            if t in enemies and n1 > 0:
                fell = int((x, y) in prev_def and dm < prev_def[(x, y)])
                siege = int(any(u in siege_units and abs(ux - x) <= 1 and abs(uy - y) <= 1 for u, ux, uy in mine))
                cases['assault'].append(dict(seq=seq, turn=turn, y=int((x, y) in attacked), capture1=c1, def_mod=dm,
                                             def_fell=fell, siege_near=siege, cap1_even=int(c1 >= EVEN)))
        prev_def = {(x, y): dm for owner, x, y, dm, n1, n3, c1, c3, jseq in J}
        for t in sorted(enemies):
            reach = int(any(T.get(o) == t and c3 >= EVEN for o, x, y, dm, n1, n3, c1, c3, jseq in J))
            began = max([s for s, a, b, w in events if w and frozenset((a, b)) == frozenset((me, t)) and s < seq] or [0])
            took = con.execute('select count(*) from wl_K k join wl_P p on p.player = k.old_owner where k.new_owner = ? and p.team = ? '
                               'and k.seq > ? and k.seq < ?', [player, t, began, seq]).fetchone()[0]
            cases['peace'].append(dict(seq=seq, turn=turn, y=int(t in peace), reach_even=reach, took_city=int(took > 0)))
    for r in cases['declare']:
        r['cap3_even'] = int(r['capture3'] >= EVEN)
        r['cap1_even'] = int(r['capture1'] >= EVEN)
    return cases, declared_out_of_reach, len(starts)


BINARY = {'declare': ['cap3_even', 'cap1_even', 'at_war', 'open_borders', 'engaged'],
          'assault': ['cap1_even', 'def_fell', 'siege_near'],
          'peace': ['reach_even', 'took_city']}
CONT = {'declare': 'capture3', 'assault': 'capture1'}


def write_cases(outdir, game, cases):
    d = os.path.join(outdir, game)
    os.makedirs(d, exist_ok=True)
    for cls, cues in BINARY.items():
        rows = cases.get(cls, [])
        with open(os.path.join(d, f'cases_{cls}.csv'), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['seq', 'turn', 'y'] + cues)
            for r in rows: w.writerow([r['seq'], r['turn'], r['y']] + [r[c] for c in cues])
        if rows:
            keys = [k for k in rows[0] if k != 'options']
            with open(os.path.join(d, f'war_{cls}.csv'), 'w', newline='') as f:
                w = csv.DictWriter(f, keys)
                w.writeheader()
                for r in rows: w.writerow({k: r[k] for k in keys})


def fit_aspiration(xs, ys):
    """q among the observed values (and above all of them) maximising hits of 'y = 1 iff x >= q'."""
    best = (-1, None)
    for q in sorted(set(xs)) + [max(xs) + 1 if xs else 1]:
        hits = sum((x >= q) == bool(y) for x, y in zip(xs, ys))
        if hits > best[0]: best = (hits, q)
    return best[1]


def fit_logit(xs, ys, iters=50):
    """(a, b) of P(y = 1) = 1 / (1 + exp(-(a + b x))), x in per mille / 1000, by Newton's method;
    None when the cases do not separate (all y equal)."""
    if len(set(ys)) < 2: return None
    a, b = 0.0, 0.0
    X = [x / 1000.0 for x in xs]
    for _ in range(iters):
        ga = gb = haa = hab = hbb = 0.0
        for x, y in zip(X, ys):
            p = 1 / (1 + math.exp(-max(-30, min(30, a + b * x))))
            ga += y - p; gb += (y - p) * x
            w = p * (1 - p); haa += w; hab += w * x; hbb += w * x * x
        det = haa * hbb - hab * hab
        if det <= 1e-12: break
        a += (hbb * ga - hab * gb) / det; b += (haa * gb - hab * ga) / det
    return a, b


def log_score(p, y):
    p = min(1 - 1e-6, max(1e-6, p))
    return math.log(p if y else 1 - p)


def loo(by_game, cls):
    """Leave one game out for the satisficing rule, the hazard and the base rate on CONT[cls]."""
    key = CONT[cls]
    res = []
    for g in by_game:
        tr = [r for h, rows in by_game.items() if h != g for r in rows]
        te = by_game[g]
        if not tr or not te: continue
        xs, ys = [r[key] for r in tr], [r['y'] for r in tr]
        q = fit_aspiration(xs, ys)
        hits = sum((r[key] >= q) == bool(r['y']) for r in te)
        base = sum(ys) / len(ys)
        ab = fit_logit(xs, ys)
        ls_h = sum(log_score(1 / (1 + math.exp(-(ab[0] + ab[1] * r[key] / 1000.0))), r['y']) for r in te) if ab else None
        ls_b = sum(log_score(base, r['y']) for r in te)
        res.append(dict(game=g, n=len(te), q=q, hits=hits, log_hazard=ls_h, log_base=ls_b))
    return res


def classify_targets(decisions):
    """Broeder's likelihood (strategy.py): log L and errors of each strategy over all decisions, one
    error rate per strategy; each decision carries the aspiration level q fitted without its game."""
    def pick(opts, rule, q):
        if rule == 'highest capture3':
            m = max(o['capture3'] for o in opts.values()); return {t for t, o in opts.items() if o['capture3'] == m}
        if rule == 'most units near':
            m = max(o['near3'] for o in opts.values()); return {t for t, o in opts.items() if o['near3'] == m}
        if rule == 'satisficing':
            ok = {t: o for t, o in opts.items() if o['capture3'] >= q} or opts
            m = max(o['near3'] for o in ok.values()); return {t for t, o in ok.items() if o['near3'] == m}
    out = {}
    for rule in ('highest capture3', 'most units near', 'satisficing'):
        errs = 0; terms = []
        for d in decisions:
            s = pick(d['options'], rule, d['q'])
            k, m = len(d['options']), len(s)
            hit = d['choice'] in s
            errs += not hit
            terms.append((hit, k, m))
        n = len(terms)
        e = errs / n if n else 0
        ll = 0.0
        for hit, k, m in terms:
            if hit: ll += math.log(max(1e-9, (1 - e) / m))
            else: ll += math.log(max(1e-9, e / (k - m))) if k > m else math.log(1e-9)
        out[rule] = dict(n=n, errors=errs, logL=ll)
    out['guessing'] = dict(n=len(decisions), errors=None, logL=sum(-math.log(len(d['options'])) for d in decisions))
    return out


def siege_types(records):
    U = records['UnitInfo']; U = U if isinstance(U, list) else list(U.values())
    return {u['Type'][5:] for u in U if u.get('Combat') == 'UNITCOMBAT_SIEGE'}


def main():
    import duckdb, json
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import figlib
    outdir, regpath, specs = sys.argv[1], sys.argv[2], sys.argv[3:]
    recp = os.path.expanduser('~/.cache/rom-ana/data/records.json')
    records = json.load(open(recp))
    siege = siege_types(records)
    games = {}
    for spec in specs:
        path, player = spec.rsplit(':', 1)
        game = os.path.splitext(os.path.basename(path))[0]
        con = duckdb.connect(path, read_only=True)
        if con.execute('select count(*) from wl_I where player = ?', [int(player)]).fetchone()[0] == 0:
            print(f'{game}: no I lines for player {player}; skipped', file=sys.stderr)
            continue
        cases, out_of_reach, n_starts = build(con, int(player), siege)
        write_cases(outdir, game, cases)
        games[game] = (cases, out_of_reach, n_starts, path)
    if not games:
        raise SystemExit('no game with snapshot lines')
    reg = figlib.Registry(regpath, [g[3] for g in games.values()] + [recp])
    who = 'human'
    for g, (cases, oor, ns, _) in games.items():
        reg.fig(f'{g}_turn_starts', ns, 'turns', who, 'all logged turns', 'hmwar.py, I lines with new_turn = 1')
        for cls in ('declare', 'assault', 'peace', 'target'):
            reg.fig(f'{g}_{cls}_cases', len(cases[cls]), 'turns' if cls != 'target' else 'lines', who, 'all logged turns',
                    f'hmwar.py, class {cls}')
        reg.fig(f'{g}_declared_out_of_reach', oor, 'lines', who, 'all logged turns', 'hmwar.py, W lines on a team without a J city')
    for cls in ('declare', 'assault'):
        by = {g: v[0][cls] for g, v in games.items()}
        rows = loo(by, cls)
        if rows:
            src = f'hmwar.py, leave one game out on {CONT[cls]}'
            over = [r['game'] for r in rows]
            reg.result_table(f'{cls}_loo_hits', ['held-out game', 'cases', 'satisficing hits'],
                             [[r['game'], r['n'], r['hits']] for r in rows], 'turns', who, 'all logged turns', src, over)
            reg.result_table(f'{cls}_loo_q', ['held-out game', 'aspiration q fitted on the other games'],
                             [[r['game'], r['q']] for r in rows], 'per mille', who, 'all logged turns', src, over)
            reg.result_table(f'{cls}_loo_score', ['held-out game', 'hazard', 'base rate'],
                             [[r['game'], 'n/a' if r['log_hazard'] is None else round(r['log_hazard'], 2), round(r['log_base'], 2)]
                              for r in rows], 'log score', who, 'all logged turns', src, over)
    allq = {}
    for g in games:
        tr = [r for h, v in games.items() if h != g for r in v[0]['declare']]
        allq[g] = fit_aspiration([r['capture3'] for r in tr], [r['y'] for r in tr]) if tr else EVEN
    decisions = [dict(d, q=allq[g]) for g, v in games.items() for d in v[0]['target']]
    if decisions:
        res = classify_targets(decisions)
        order = ['highest capture3', 'most units near', 'satisficing', 'guessing']
        reg.result_table('target_strategies', ['strategy', 'declarations', 'errors', 'log L'],
                         [[k, res[k]['n'], '-' if res[k]['errors'] is None else res[k]['errors'], round(res[k]['logL'], 2)] for k in order],
                         'lines', who, 'declaration turns', 'hmwar.py, Broeder strategy classification', order)
    reg.save()
    print(f'{len(games)} games; registry {regpath}', file=sys.stderr)


def selftest():
    """A synthetic game: the cases and labels of every class are checked against hand counts."""
    import duckdb
    con = duckdb.connect()
    con.execute('create table wl_P (seq bigint, player bigint, team bigint, civ varchar, leader varchar, human bigint)')
    con.execute("insert into wl_P values (1,0,0,'a','a',1),(2,1,1,'b','b',0),(3,2,2,'c','c',0)")
    con.execute('create table wl_I (seq bigint, turn bigint, player bigint, new_turn bigint, own_units bigint, cities bigint, defenders bigint, teams bigint)')
    con.execute('create table wl_O (seq bigint, turn bigint, player bigint, team bigint, war bigint, open_borders bigint, def_pact bigint, vassal bigint, plan_theirs bigint, plan_ours bigint, weariness bigint)')
    con.execute('create table wl_J (seq bigint, turn bigint, player bigint, owner bigint, x bigint, y bigint, pop bigint, def_mod bigint, visible bigint, war bigint, defenders bigint, near1 bigint, near3 bigint, on_ships bigint, capture1 bigint, losses1 bigint, capture3 bigint, losses3 bigint)')
    con.execute('create table wl_L (seq bigint, turn bigint, viewer bigint, owner bigint, id bigint, unit varchar, x bigint, y bigint)')
    con.execute('create table wl_W (seq bigint, turn bigint, team bigint, target bigint, warplan bigint)')
    con.execute('create table wl_Q (seq bigint, turn bigint, team bigint, target bigint, warplan bigint)')
    con.execute('create table wl_C (seq bigint, turn bigint, att bigint, x bigint, y bigint)')
    con.execute('create table wl_K (seq bigint, turn bigint, old_owner bigint, new_owner bigint, x bigint, y bigint, pop bigint)')
    # turn 10: at peace with 1 and 2; city of 1 at capture3 300, of 2 at 700; no declaration
    con.execute('insert into wl_I values (100,10,0,1,2,2,0,2)')
    con.execute('insert into wl_O values (101,10,0,1,0,1,0,0,-1,-1,0),(102,10,0,2,0,0,0,0,-1,-1,0)')
    con.execute('insert into wl_J values (103,10,0,1,5,5,3,20,1,0,2,0,2,0,0,0,300,100),(104,10,0,2,9,9,3,20,1,0,1,0,4,0,0,0,700,50)')
    con.execute("insert into wl_L values (105,10,0,0,1,'CATAPULT',8,8)")
    # turn 11: same, declares on team 2
    con.execute('insert into wl_I values (200,11,0,1,2,2,0,2)')
    con.execute('insert into wl_O values (201,11,0,1,0,1,0,0,-1,-1,0),(202,11,0,2,0,0,0,0,-1,-1,0)')
    con.execute('insert into wl_J values (203,11,0,1,5,5,3,20,1,0,2,0,2,0,0,0,300,100),(204,11,0,2,9,9,3,20,1,0,1,3,5,0,800,40,800,40)')
    con.execute('insert into wl_W values (210,11,0,2,-1)')
    # turn 12: at war with 2; units adjacent, defence fell 20 -> 0, catapult adjacent; attacks; peace with 2
    con.execute('insert into wl_I values (300,12,0,1,2,2,0,2)')
    con.execute('insert into wl_O values (301,12,0,1,0,1,0,0,-1,-1,0),(302,12,0,2,1,0,0,0,-1,-1,0)')
    con.execute('insert into wl_J values (303,12,0,2,9,9,3,0,1,1,1,3,5,0,900,30,900,30),(306,12,0,1,5,5,3,20,1,0,2,0,2,0,0,0,300,100)')
    con.execute("insert into wl_L values (304,12,0,0,1,'CATAPULT',8,8)")
    con.execute('insert into wl_C values (310,12,0,9,9)')
    con.execute('insert into wl_Q values (320,12,0,2,-1)')
    cases, oor, ns = build(con, 0, {'CATAPULT'})
    d = cases['declare']
    assert ns == 3 and len(d) == 3, (ns, len(d))  # turn 12: still at peace with team 1 (a candidate)
    assert [r['y'] for r in d] == [0, 1, 0] and d[0]['capture3'] == 700 and d[1]['capture1'] == 800, d
    assert d[0]['open_borders'] == 0 and d[2]['at_war'] == 1 and d[2]['capture3'] == 300, d
    t = cases['target']
    assert len(t) == 1 and t[0]['choice'] == 2 and set(t[0]['options']) == {1, 2} and oor == 0, t
    a = cases['assault']
    assert len(a) == 1 and a[0]['y'] == 1 and a[0]['def_fell'] == 1 and a[0]['siege_near'] == 1 and a[0]['cap1_even'] == 1, a
    p = cases['peace']
    assert len(p) == 1 and p[0]['y'] == 1 and p[0]['reach_even'] == 1 and p[0]['took_city'] == 0, p
    assert fit_aspiration([300, 700, 800], [0, 0, 1]) == 800
    r = classify_targets([dict(x, q=750) for x in t])
    assert r['highest capture3']['errors'] == 0 and r['satisficing']['errors'] == 0, r
    print('hmwar selftest: ok')


if __name__ == '__main__':
    selftest() if sys.argv[1:] == ['--selftest'] else main()
