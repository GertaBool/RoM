#!/usr/bin/env python3
"""The human's wars, one by one: build-up, staging, target choice, assaults and peace.

usage: warstudy.py <registry.fig.json> <records.json> <game.duckdb> ...   (games with Y lines)

A war is a W line of the human's team; it ends with the first Q line of the same pair, or is open at
the game's last turn. Day d of a war is its declaration turn + d. Sources per table:
  wars          W, Q, M (power the turn before), K (cities taken), C (attacks), R (losses: loser), deal items
                on the peace turn (gold, gold per turn, techs and cities either way)
  buildup       U lines (units built, by UnitInfo DefaultUnitAI) and A lines COMMAND_UPGRADE and COMMAND_PROMOTION
                of the human in the 30 turns before the declaration, against the 30 turns before those
  upgrades      the unit types those upgrades went to, per war
  staging       on the declaration turn: Y lines of the target's cities ("foreign": land units of other players within
                two plots, before the human's moves); A lines MISSION_MOVE_TO of the human (units: group sizes), those of
                land units ordered from a water plot (COAST or OCEAN in the save's plots), naval moves and GROUP commands
                from ten turns before to the declaration
  targets       Y lines of the target's cities on the declaration turn (the first line of each city that turn): size,
                defenders, best defender, defence modifier, foreign units within two plots; distance (grid, map wrap
                ignored) to the nearest city of the human (its Y lines on the declaration turn and the cities it took
                since); the day the city fell to the human in that war
  choice        each city the human took: the cities the target held that turn (Y lines) are the options; each cue
                names its best options; maximum-likelihood classification (Bröder, in Heuristics, chapter 17): the
                chosen city is a best option with probability 1 - e (shared among the best), any other with e (shared
                among the rest); e fitted on a grid; against guessing (each option 1/m)
  days          per war and day: attacks (C lines by the human), their odds (per mille), attacks by siege units
                (DefaultUnitAI ATTACK_CITY) and by ships, units lost, bombards (B lines), cities taken
  assaults      per city taken: the human's attacks on that plot from the declaration to the capture, in order
  peace         ended wars: days from the last capture to the peace, and the deal of the peace turn
  home          the human's cities on the declaration turn (Y lines) and the attacks on its units and cities during the
                war (C lines with the human defending), cities it lost (K lines)
"""
import collections, json, math, os, statistics, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

REG, RECS, DBS = sys.argv[1], sys.argv[2], sys.argv[3:]
R = json.load(open(RECS))
reg = Registry(REG, [RECS] + DBS, R)
ROLES = ['COUNTER', 'ATTACK', 'ATTACK_CITY', 'CITY_DEFENSE', 'ASSAULT_SEA', 'ATTACK_SEA']
med = lambda v: round(statistics.median(v), 1) if v else ''
T_all = collections.defaultdict(list)   # table -> rows over games
O_all = collections.defaultdict(list)
units_named = collections.defaultdict(set)
choice_cases = []

for db in DBS:
    g = os.path.basename(db).split('.')[0]
    con = duckdb.connect(db, read_only=True)
    q = lambda s, *a: con.execute(s, list(a)).fetchall()
    hp, team = q('select player, team from wl_P where human=1')[0]
    tp = {t: p for p, t in q('select player, team from wl_P')}
    last = q('select max(turn) from wl_T')[0][0]
    water = {(x, y) for x, y in q("select x, y from plots where terrain in ('COAST', 'OCEAN')")}
    ui = {u: (ai, dom) for u, ai, dom in q('select unit, default_ai, domain from unit_info')}
    ui_all = ui
    role = lambda u: ui.get(u, ('?', '?'))[0]
    dom = lambda u: ui.get(u, ('?', '?'))[1]

    def ycities(player, t):
        out = {}
        for x, y, pop, d, bd, dm, fo in q('select x, y, pop, defenders, best_defender, def_mod, "foreign" from wl_Y where player=? and turn=? order by seq', player, t):
            out.setdefault((x, y), (pop, d, bd, dm, fo))
        return out

    for T, tgt in q('select turn, target from wl_W where team=? order by seq', team):
        P = tp[tgt]
        wid = f'{g} {T}'
        pq = q('select min(turn) from wl_Q where team=? and target=? and turn>=?', team, tgt, T)[0][0]
        end = pq if pq is not None else last
        # --- overview
        mp = q('select power from wl_M where player=? and turn=?', hp, T - 1)
        mt = q('select power from wl_M where player=? and turn=?', P, T - 1)
        caps = q('select turn, x, y, pop from wl_K where old_owner=? and new_owner=? and turn between ? and ? order by seq', P, hp, T, end)
        tcity = ycities(P, T)
        attacks = q('select seq, turn, att_unit, odds, x, y, def_unit from wl_C where att=? and def=? and turn between ? and ? order by seq', hp, P, T, end)
        lost = q('select count(*) from wl_R where loser=? and winner=? and turn between ? and ?', hp, P, T, end)[0][0]
        killed = q('select count(*) from wl_R where loser=? and winner=? and turn between ? and ?', P, hp, T, end)[0][0]
        T_all['wars'].append([wid, P, round(mp[0][0] / mt[0][0], 2) if mp and mt and mt[0][0] else '', len(tcity), len(caps),
                              caps[0][0] - T if caps else '-', len(attacks), killed, lost, pq - T if pq is not None else 'open'])
        O_all['wars'].append(wid)
        # --- was the target already at war with another team? (W and Q lines of every other pair)
        others = q('select team, target, turn from wl_W where team<>? and target<>? and turn<?', team, team, T)
        atwar = set()
        for a, b, t0 in others:
            t1 = q('select min(turn) from wl_Q where ((team=? and target=?) or (team=? and target=?)) and turn>=?', a, b, b, a, t0)[0][0]
            if t1 is None or t1 >= T: atwar |= {a, b}
        alive = {t for (t,) in q('select distinct p.team from wl_M m join wl_P p on p.player=m.player where m.turn=? and m.cities>0', T - 1)} - {team}
        T_all['engaged'].append([wid, 'yes' if tgt in atwar else 'no', len(atwar & alive), len(alive), round(len(atwar & alive) / len(alive), 2) if alive else ''])
        O_all['engaged'].append(wid)
        # --- build-up
        for lo, hi, lab in ((T - 30, T - 1, 'the 30 turns before'), (T - 60, T - 31, 'the 30 turns before those')):
            built = collections.Counter(role(u) for (u,) in q('select unit from wl_U where player=? and turn between ? and ?', hp, lo, hi))
            upg = q("select a6 from wl_A where player=? and kind='COMMAND' and a5='COMMAND_UPGRADE' and turn between ? and ?", hp, lo, hi)
            prom = q("select count(*) from wl_A where player=? and kind='COMMAND' and a5='COMMAND_PROMOTION' and turn between ? and ?", hp, lo, hi)[0][0]
            T_all['buildup'].append([f'{wid}, {lab}', *[built.get(r, 0) for r in ROLES], sum(v for k, v in built.items() if k not in ROLES),
                                     len(upg), prom])
            O_all['buildup'].append(f'{wid}, {lab}')
            if lab == 'the 30 turns before':
                for (u,) in upg:
                    T_all['upgrades_rows'].append(dict(war=wid, to=u.removeprefix('UNIT_')))
        # --- staging on the declaration turn
        moves = q("select a1, a2, a3, a4, a6, a7 from wl_A where player=? and kind='MISSION' and a5='MISSION_MOVE_TO' and turn=?", hp, T)
        pre = q("select turn, a1, a2, a3, a4 from wl_A where player=? and kind='MISSION' and a5='MISSION_MOVE_TO' and turn between ? and ?", hp, T - 10, T)
        land_sea = sum(1 for _, u, x, y, n in pre if dom(u) == 'LAND' and (int(x), int(y)) in water)
        naval = sum(1 for _, u, x, y, n in pre if dom(u) == 'SEA')
        groups = q("select count(*) from wl_A where player=? and kind='GROUP' and turn between ? and ?", hp, T - 10, T)[0][0]
        first_cap = (caps[0][1], caps[0][2]) if caps else None
        T_all['staging'].append([wid, sum(1 for v in tcity.values() if v[4] > 0), tcity[first_cap][4] if first_cap in tcity else '-',
                                 len(moves), sum(int(n or 1) for *_, n, _, _ in moves), land_sea, naval, groups])
        O_all['staging'].append(wid)
        # --- the approach: moves of fighting land units over the ten days before, toward the cities taken
        taken = [(c[1], c[2]) for c in caps]
        if taken:
            for d in range(-10, 1):
                mv = q("select a1, a2, a3, a4, a6, a7 from wl_A where player=? and kind='MISSION' and a5='MISSION_MOVE_TO' and turn=?", hp, T + d)
                fight = [m for m in mv if dom(m[0]) == 'LAND' and ui.get(m[0], ('', ''))[0] not in ('WORKER', 'SETTLE', 'EXPLORE', 'MERCHANT', '?')]
                dist = lambda x, y: min(max(abs(int(x) - a), abs(int(y) - b)) for a, b in taken)
                near = [m for m in fight if dist(m[4], m[5]) <= 2]
                T_all['approach'].append([f'{wid} day {d}', len(fight), sum(int(m[3] or 1) for m in fight), len(near), sum(int(m[3] or 1) for m in near),
                                          med([dist(m[1], m[2]) for m in fight]), med([dist(m[4], m[5]) for m in fight])])
                O_all['approach'].append(f'{wid} day {d}')
        # --- the target's cities
        hc = set(ycities(hp, T))
        capd = {}
        for t, x, y, pop in caps: capd.setdefault((x, y), t - T)
        for (x, y), (pop, d, bd, dm, fo) in sorted(tcity.items(), key=lambda kv: (kv[1][1], kv[0])):
            dist = min((max(abs(x - a), abs(y - b)) for a, b in hc), default='')
            T_all['targets'].append([f'{wid} {x},{y}', pop, d, bd, dm, fo, dist, capd.get((x, y), '-')])
            O_all['targets'].append(f'{wid} {x},{y}')
            units_named['targets'].add(bd)
        # --- choice cases: each city taken, among the target's cities that turn
        owned = set(hc)
        for t, x, y, pop in caps:
            opts = ycities(P, t)
            if (x, y) in opts and len(opts) > 1:
                cue = {}
                for k, v in opts.items():
                    dist = min((max(abs(k[0] - a), abs(k[1] - b)) for a, b in owned), default=99)
                    cue[k] = dict(defenders=v[1], defence=v[3], distance=dist, near=-v[4], small=v[0], large=-v[0])
                choice_cases.append((f'{wid} {x},{y}', (x, y), cue))
            owned.add((x, y))
        # --- days
        bomb = collections.Counter(t for (t,) in q('select turn from wl_B where player=? and turn between ? and ?', hp, T, end))
        for d in range(0, min(end, last) - T + 1):
            t = T + d
            at = [a for a in attacks if a[1] == t]
            capt = [c for c in caps if c[0] == t]
            lo = q('select count(*) from wl_R where loser=? and winner=? and turn=?', hp, P, t)[0][0]
            if not at and not capt and d > 0: continue
            od = [a[3] for a in at]
            T_all['days'].append([f'{wid} day {d}', len(at), med(od), min(od) if od else '', sum(1 for a in at if role(a[2]) == 'ATTACK_CITY'),
                                  sum(1 for a in at if dom(a[2]) == 'SEA'), bomb.get(t, 0), lo, len(capt)])
            O_all['days'].append(f'{wid} day {d}')
        # --- assaults
        for t, x, y, pop in caps:
            seq = [a for a in attacks if (a[4], a[5]) == (x, y) and a[1] <= t]
            T_all['assaults'].append([f'{wid} {x},{y}', t - T, tcity.get((x, y), ('', '', '', '', ''))[1], len(seq),
                                      ' '.join(f'{a[2]}:{a[3]}' for a in seq) or '(walked in)', sum(1 for a in seq if a[3] < 500)])
            O_all['assaults'].append(f'{wid} {x},{y}')
            for a in seq: units_named['assaults'].add(a[2])
        # --- peace
        if pq is not None:
            items = q('select side, first, item, data from deal_items where turn=? and ((first=? and second=?) or (first=? and second=?))', pq, hp, P, P, hp)
            got = lambda it: sum(d for s, f, i, d in items if i == it and ((s == 1 and f == P) or (s == 2 and f == hp)))
            cnt = lambda it, frm: sum(1 for s, f, i, d in items if i == it and ((s == 1 and f == frm) or (s == 2 and f != frm)))
            lastcap = caps[-1][0] if caps else None
            T_all['peace'].append([wid, pq - T, pq - lastcap if lastcap is not None else '-', got(0), got(1), cnt(9, P), cnt(9, hp), cnt(11, P)])
            O_all['peace'].append(wid)
        # --- home
        hcity = ycities(hp, T)
        defs = [v[1] for v in hcity.values()]
        hit = q('select count(*) from wl_C where def=? and att=? and turn between ? and ?', hp, P, T, end)[0][0]
        hlost = q('select count(*) from wl_K where old_owner=? and turn between ? and ?', hp, T, end)[0][0]
        T_all['home'].append([wid, len(hcity), med(defs), sum(1 for d in defs if d <= 1), hit, hlost])
        O_all['home'].append(wid)

src = 'warstudy.py on the war logs of ' + ', '.join(os.path.basename(d).split('.')[0] for d in DBS)
reg.result_table('war_overview', ['war', 'target_player', 'power_ratio', 'target_cities', 'cities_taken', 'first_capture_day', 'attacks',
                                  'enemy_units_killed', 'units_lost', 'peace_day'], T_all['wars'], 'cities', 'human', 'each war',
                 src + ': W lines of the human team (war: game and declaration turn), the power of both the turn before (M lines), the '
                 'target\'s cities on the declaration turn (Y lines), cities taken (K), attacks (C), units killed and lost (R), the peace (Q); '
                 'days count from the declaration', O_all['wars'], n=len(O_all['wars']))
reg.result_table('war_buildup', ['war_window', *[r.lower() for r in ROLES], 'other_units', 'upgrades', 'promotions'], T_all['buildup'],
                 'units built', 'human', 'the 60 turns before each declaration', src + ': U lines by DefaultUnitAI (UnitInfo) and A lines '
                 'COMMAND_UPGRADE and COMMAND_PROMOTION, in the 30 turns before the declaration and the 30 before those; upgrades and '
                 'promotions are commands', O_all['buildup'], n=len(T_all['buildup']))
ups = T_all['upgrades_rows']
reg.census_table('war_upgrades', ups, 'to', 'orders', 'human', 'the 30 turns before each declaration', src + ': A lines '
                 'COMMAND_UPGRADE, the unit type upgraded to', group='war', xml='UnitInfo', label='upgraded_to')
reg.result_table('war_staging', ['war', 'target_cities_with_foreign_units_near', 'foreign_units_near_first_taken', 'moves_on_declaration',
                                 'units_moved', 'land_moves_from_sea_10_turns', 'naval_moves_10_turns', 'group_commands_10_turns'],
                 T_all['staging'], 'orders', 'human', 'the declaration turn and the ten before', src + ': Y lines of the target\'s cities on '
                 'the declaration turn ("foreign": other players\' land units within two plots, before the human moves); A lines of the human: '
                 'MISSION_MOVE_TO on the declaration turn (units: their group sizes), those from ten turns before to the declaration by land '
                 'units standing on water (COAST, OCEAN) and by ships, and GROUP commands', O_all['staging'], n=len(O_all['staging']))
reg.result_table('war_approach', ['war_day', 'fighting_moves', 'units_in_them', 'moves_ending_near', 'units_ending_near', 'median_distance_from',
                                   'median_distance_to'], T_all['approach'], 'orders', 'human', 'the ten days before each declaration that took a '
                 'city, and the declaration', src + ': A lines MISSION_MOVE_TO of the human\'s land units other than workers, settlers, '
                 'explorers and merchants (DefaultUnitAI); units: group sizes; near: the target plot within two plots of a city the human '
                 'took in that war; distances in grid plots from the unit\'s plot and from its target plot to the nearest such city',
                 O_all['approach'], n=len(O_all['approach']))
eng = T_all['engaged']
reg.result_table('war_engaged', ['war', 'target_at_war_elsewhere', 'other_teams_at_war', 'other_teams', 'share_at_war'], eng, 'cities', 'every team',
                 'each declaration turn', src + ': a team is at war with another when a W line of the pair precedes the declaration and no Q '
                 'line of the pair ends it before; wars before the first W line of the log are not seen; other teams: teams other than the '
                 'human\'s with a city in M lines the turn before; share_at_war: the chance that a team picked at random among them was at '
                 'war, the expected count of targets at war being the sum of these shares', O_all['engaged'], n=len(eng))
reg.fig('targets_at_war_elsewhere', sum(1 for r in eng if r[1] == 'yes'), 'cities', 'the human\'s targets', 'each declaration turn',
        'war_engaged: wars whose target was at war with another team (counted per war)', n=len(eng))
reg.fig('targets_at_war_expected', round(sum(r[4] for r in eng if r[4] != ''), 1), 'cities', 'the human\'s targets', 'each declaration turn',
        'war_engaged: sum over wars of share_at_war, the count expected if targets were picked without regard to their wars', n=len(eng))
dist = [1.0]                                        # Poisson-binomial: P(k targets at war) from the shares
for r in eng:
    pr = r[4] if r[4] != '' else 0
    dist = [a * (1 - pr) + (dist[i - 1] * pr if i else 0) for i, a in enumerate(dist + [0.0])]
k_obs = sum(1 for r in eng if r[1] == 'yes')
reg.fig('targets_at_war_p', round(sum(dist[k_obs:]), 4), 'share', 'the human\'s targets', 'each declaration turn',
        'war_engaged: the chance of at least as many targets at war elsewhere if each war\'s target were a random other team '
        '(Poisson-binomial over the wars\' shares, computed exactly)', n=len(eng))
ships = sorted({u for u, (ai, d) in ui_all.items() if d == 'SEA' and u in ('GALLEY', 'QUINQUEREME')})
reg.result_table('war_ships', ['ship'], [[u] for u in ships], 'xml', 'human', 'whole game', 'the ships named in section 9 (UnitInfo records)',
                 ships, n=len(ships), xml='UnitInfo', xml_vals=ships)
reg.fig('wars_counted', len(eng), 'cities', 'human', 'each declaration', 'W lines of the human team in the games given', n=len(eng))
reg.result_table('war_targets', ['war_city', 'pop', 'defenders', 'best_defender', 'defence_pct', 'foreign_units_near', 'distance', 'day_taken'],
                 T_all['targets'], 'cities', 'the human\'s targets', 'each declaration turn', src + ': the first Y line of each city of the '
                 'target on the declaration turn; distance: grid plots to the nearest city of the human that turn (its Y lines); day_taken: '
                 'days after the declaration that the human took it in this war (K lines)', O_all['targets'], n=len(O_all['targets']),
                 xml='UnitInfo', xml_vals=sorted(units_named['targets']))
# choice classification
CUES = [(('defenders',), 'fewest defenders'), (('defence',), 'lowest defence modifier'), (('distance',), 'nearest to the human\'s cities'),
        (('near',), 'most foreign units within two plots'), (('small',), 'smallest'), (('large',), 'largest'),
        (('distance', 'defenders'), 'nearest, then fewest defenders'), (('distance', 'defence'), 'nearest, then lowest defence'),
        (('near', 'defenders'), 'most units near, then fewest defenders'), (('defenders', 'distance'), 'fewest defenders, then nearest'),
        (('distance', 'near'), 'nearest, then most units near')]
val = lambda v, keys: tuple(v[k] for k in keys)


def lnL(cases, key, e):
    s = 0.0
    for _, chosen, cue in cases:
        m = len(cue)
        best_v = min(val(v, key) for v in cue.values())
        best = [k for k, v in cue.items() if val(v, key) == best_v]
        if chosen in best: s += math.log((1 - e) / len(best))
        else: s += math.log(e / (m - len(best))) if m > len(best) else math.log(1e-12)
    return s


crow = []
n = len(choice_cases)
guess = sum(math.log(1 / len(c[2])) for c in choice_cases)
for key, name in CUES:
    hits = sum(1 for _, ch, cue in choice_cases if val(cue[ch], key) == min(val(v, key) for v in cue.values()))
    best = max(((lnL(choice_cases, key, e / 100), e / 100) for e in range(1, 100)), key=lambda z: z[0]) if n else (0, 0)
    crow.append([name, n, hits, round(best[1], 2), round(best[0], 2), round(guess, 2), round(best[0] - guess, 2)])
reg.result_table('war_choice', ['cue', 'cities_taken', 'chosen_was_best', 'error_rate', 'ln_likelihood', 'ln_likelihood_guessing', 'gain_over_guessing'],
                 crow, 'cities', 'human', 'each city taken', src + ': each city the human took (K lines) with more than one city of the target '
                 'that turn (Y lines); options: those cities; a cue\'s best options: its least value (defenders, defence modifier, distance to '
                 'the human\'s cities including those taken before in the war, size) or most foreign units near; a pair of cues: the '
                 'second decides among the first\'s best (take-the-best, Gigerenzer, Heuristics, chapter 14); maximum-likelihood '
                 'classification with one error rate per cue (Bröder, in Heuristics, chapter 17), e on a grid of hundredths; guessing: each '
                 'option 1/m; chosen_was_best counts ties as hits', [c[1] for c in CUES], n=n)
reg.result_table('war_days', ['war_day', 'attacks', 'median_odds', 'lowest_odds', 'siege_unit_attacks', 'ship_attacks', 'bombards', 'units_lost',
                              'cities_taken'], T_all['days'], 'battles', 'human', 'each day with an attack or capture, and the declaration',
                 src + ': C lines with the human attacking the target (odds per mille; siege units: DefaultUnitAI ATTACK_CITY; ships: SEA '
                 'domain), B lines of the human, R lines with the human losing, K lines', O_all['days'], n=len(O_all['days']))
reg.result_table('war_assaults', ['war_city', 'day_taken', 'defenders_at_declaration', 'attacks', 'attacks_in_order_unit_odds', 'attacks_under_500'],
                 T_all['assaults'], 'battles', 'human', 'each city taken', src + ': for each city the human took, its attacks on that plot '
                 'from the declaration to the capture turn (C lines, in order: unit and odds per mille); defenders: Y lines on the '
                 'declaration turn', O_all['assaults'], n=len(O_all['assaults']), xml='UnitInfo', xml_vals=sorted(units_named['assaults']))
reg.result_table('war_peace', ['war', 'peace_day', 'days_after_last_capture', 'gold_received', 'gold_per_turn_received', 'techs_received',
                               'techs_given', 'cities_received'], T_all['peace'], 'turns', 'human', 'each peace', src + ': Q lines and the deal '
                 'items of the peace turn between the two (TRADE_GOLD, TRADE_GOLD_PER_TURN, TRADE_TECHNOLOGIES, TRADE_CITIES; given by '
                 'side); gold in gold, techs and cities counted', O_all['peace'], n=len(O_all['peace']))
reg.result_table('war_home', ['war', 'human_cities', 'median_defenders', 'cities_with_one_defender_or_none', 'attacks_on_human', 'cities_lost'],
                 T_all['home'], 'cities', 'human', 'each war', src + ': the human\'s Y lines on the declaration turn; C lines with the human '
                 'defending against the target and K lines of cities it lost, during the war', O_all['home'], n=len(O_all['home']))
reg.save()
for k in ('war_choice',):
    for r in reg.figs[k]['rows']: print(r, file=sys.stderr)
