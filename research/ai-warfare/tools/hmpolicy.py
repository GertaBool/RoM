#!/usr/bin/env python3
"""The human model's policy (toolchain/harness/HarnessHuman.cpp), derived from the logged games.

usage: hmpolicy.py <policy out> <registry.fig.json> <records.json> <game.duckdb> ...

Every element is a rule applied to the human's records in the games given, pooled:
  TECH    the techs the human got after turn 0 (X lines, by any route), ordered by the mean over
          the games of their normalised rank (rank of the acquisition turn / techs got)
  CIVIC   per civic option, the civics the human adopted (CIVICS commands, A lines: a civic not
          held before), in tiers by position: tier k holds the k-th civic adopted in each game.
          A tier came late in a game if its civic there was adopted more than one turn after the
          human got its TechPrereq (or after the first CIVICS command, for a tech held from the
          start), or never though the tech of one of its civics was held two turns before the
          game's last turn; a tier that came late in a game is marked '*': the model then keeps the
          civic held from the previous tier (for the first tier: the civic held) while the AI's own
          civic value rates it at least as high, so that value chooses between waiting and switching.
          Within a tier of several civics the AI's value picks one, which is then kept
  BUILD   building classes (kind "building" in BuildingInfo: no wonders) the human completed (N
          lines) in at least a third of its cities with a completion in one game, ordered by the
          mean over the games of the median position in each city's order of completions
  PARAM   the war, trade and production parameters, each with its rule in the registry table
"""
import collections, json, math, os, statistics, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

OUT, REG, RECS, DBS = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
R = json.load(open(RECS))
reg = Registry(REG, [RECS] + DBS, R)
games = [os.path.basename(d).split('.')[0] for d in DBS]
cons = {g: duckdb.connect(d, read_only=True) for g, d in zip(games, DBS)}
gl = ', '.join(games)


def q(g, sql, *a):
    return cons[g].execute(sql, list(a)).fetchall()


H = {g: q(g, 'select player, team, civ from wl_P where human=1')[0] for g in games}
LAST = {g: q(g, 'select max(turn) from wl_T')[0][0] for g in games}
TECHT = {g: dict(q(g, 'select tech, min(turn) from wl_X where player=? group by 1', H[g][0])) for g in games}

# --- research order ---
norm = collections.defaultdict(list)
for g in games:
    got = sorted((t, x) for x, t in TECHT[g].items() if t > 0)
    for i, (t, x) in enumerate(got):
        norm[x].append((i + 1) / len(got))
techs = sorted(norm, key=lambda x: (statistics.mean(norm[x]), x))
rows = [[x, *[TECHT[g].get(x, '') for g in games], round(1000 * statistics.mean(norm[x]))] for x in techs]
reg.result_table('hm_tech_order', ['tech', *[f'{g}_turn' for g in games], 'mean_normalised_rank'], rows, 'turn', 'human',
                 'acquisition turns', f'X lines of the human in {gl} (first turn per tech, turn 0 left out: held from the start); '
                 'mean_normalised_rank: per mille, the mean over the games holding the tech of its rank among the techs got / their number',
                 techs, n=len(techs), xml='TechInfo', xml_vals=techs)

# --- civic tiers ---
CI = R['CivicInfo']
opt_of = {k.removeprefix('CIVIC_'): v['CivicOptionType'].removeprefix('CIVICOPTION_') for k, v in CI.items()}
prereq = {k.removeprefix('CIVIC_'): (v.get('TechPrereq') or 'NONE').removeprefix('TECH_') for k, v in CI.items()}
seqs = {}         # game -> option -> [(civic, turn)]
init0 = {}        # game -> option -> the civilization's initial civic
first_cmd = {}
for g in games:
    init = {opt_of[c.removeprefix('CIVIC_')]: c.removeprefix('CIVIC_') for c in R['CivilizationInfo'][H[g][2]]['InitialCivics']}
    held = dict(init); init0[g] = dict(init)
    s = collections.defaultdict(list)
    cmds = q(g, "select turn, arg_max(a1, seq) from wl_A where player=? and kind='CIVICS' group by 1 order by 1", H[g][0])
    first_cmd[g] = cmds[0][0] if cmds else 0
    for t, l in cmds:
        for c in [x.removeprefix('CIVIC_') for x in l.split(',') if x]:
            o = opt_of[c]
            if held.get(o) != c:
                s[o].append((c, t)); held[o] = c
    seqs[g] = s


def techturn(g, c):
    tech = prereq[c]
    return 0 if tech == 'NONE' else TECHT[g].get(tech)


def late_games(o, k, tier):
    """The games where the k-th civic of option o came late: adopted more than one turn after its
    tech (by the first CIVICS command for a tech held from the start), or never though the tech of a
    civic of the tier was held two turns before the game's last turn."""
    out = []
    for g in games:
        if len(seqs[g][o]) > k:
            c, at = seqs[g][o][k]
            tt = techturn(g, c)
            if at > max(tt + 1, first_cmd[g] if tt == 0 else 0): out.append(g)
        elif any(techturn(g, c) is not None and techturn(g, c) <= LAST[g] - 2 for c in tier):
            out.append(g)
    return out


civrows, policy_civics = [], []
options = sorted({o for g in games for o in seqs[g]}, key=lambda o: R['CivicOptionInfo']['CIVICOPTION_' + o]['_index'])
for o in options:
    n = max(len(seqs[g][o]) for g in games)
    tiers = []
    for k in range(n):
        tier = sorted({seqs[g][o][k][0] for g in games if len(seqs[g][o]) > k})
        late = late_games(o, k, tier)
        prev = tiers[-1][1] if tiers else sorted({init0[g][o] for g in games if o in init0[g]})
        merged = (prev if late else []) + [c for c in tier if not late or c not in prev]
        tiers.append((merged, tier, late))
        civrows.append([f'{o} {k + 1}', ' '.join(tier), ' '.join(late) or '-', ' | '.join(merged),
                        *['; '.join(f'{c} {t}' for c, t in seqs[g][o][k:k + 1]) or '-' for g in games]])
    policy_civics.append(f'CIVIC CIVICOPTION_{o} ' + ' '.join(('*' if late else '') + '|'.join('CIVIC_' + c for c in t) for _, t, late in tiers))
civ_all = sorted({c for g in games for o in seqs[g] for c, _ in seqs[g][o]})
reg.result_table('hm_civic_tiers', ['option_tier', 'adopted', 'late_in', 'candidates', *[f'{g}_adopted' for g in games]], civrows,
                 'turn', 'human', 'whole game', f'CIVICS commands of the human in {gl} (A lines; a civic not held before; the start: the '
                 'civilization\'s InitialCivics), the TechPrereq of each civic and the human\'s X lines; late_in: the games where the tier\'s civic '
                 'was adopted more than one turn after its tech, or never though a tech of the tier was held two turns before the last turn; '
                 'candidates: the tier and, when it came late in a game, the previous tier (for the first: the InitialCivics), which '
                 'the model keeps while the AI values it at least as high', [r[0] for r in civrows], n=sum(len(v) for g in games for v in seqs[g].values()),
                 xml='CivicInfo', xml_vals=civ_all)

# --- building template ---
BI = {k.removeprefix('BUILDING_'): v for k, v in R['BuildingInfo'].items()}
kind = {}
for g in games:
    kind.update(dict(q(g, 'select building, kind from building_info')))
ranks = collections.defaultdict(dict)   # building -> game -> (cities, median rank)
share = {}
for g in games:
    n = q(g, 'select building, x, y from wl_N where player=? order by seq', H[g][0])
    pos, k = collections.defaultdict(list), collections.Counter()
    for b, x, y in n:
        k[(x, y)] += 1; pos[b].append(k[(x, y)])
    ncity = len(k)
    share[g] = ncity
    for b, p in pos.items():
        ranks[b][g] = (len(p), statistics.median(p))
tpl = [b for b in ranks if kind.get(b) == 'building' and any(c * 3 >= share[g] for g, (c, _) in ranks[b].items())]
tpl.sort(key=lambda b: (statistics.mean(m for _, m in ranks[b].values()), b))
cls = {b: BI[b]['BuildingClass'] for b in tpl}
seen, tplc = set(), []
for b in tpl:
    if cls[b] not in seen: seen.add(cls[b]); tplc.append(b)
trows = [[b, cls[b].removeprefix('BUILDINGCLASS_'), *[f'{ranks[b][g][0]} / {share[g]}' if g in ranks[b] else '-' for g in games],
          *[ranks[b][g][1] if g in ranks[b] else '' for g in games]] for b in tplc]
reg.result_table('hm_template', ['building', 'class', *[f'{g}_cities' for g in games], *[f'{g}_median_position' for g in games]], trows,
                 'rank', 'human', 'whole game', f'N lines of the human in {gl}: buildings (BuildingInfo kind "building") completed in at least '
                 'a third of the human\'s cities with a completion in one game ("cities": completing cities / cities with a completion), by '
                 'the mean of their median positions in each city\'s order of completions; one row per class (the first building of a class)',
                 tplc, n=len(tplc), xml='BuildingInfo', xml_vals=tplc)

# --- parameters ---
wars = []   # game, declaration turn, target team, ratio, peace turn, captures, last capture
for g in games:
    pl, team, _ = H[g]
    tp = dict((t, p) for p, t in q(g, 'select player, team from wl_P'))
    for t, tgt in q(g, 'select turn, target from wl_W where team=? order by seq', team):
        mp = q(g, 'select power from wl_M where player=? and turn=?', pl, t - 1)
        mt = q(g, 'select power from wl_M where player=? and turn=?', tp.get(tgt), t - 1)
        pq = q(g, 'select min(turn) from wl_Q where team=? and target=? and turn>=?', team, tgt, t)[0][0]
        caps = [r[0] for r in q(g, 'select turn from wl_K where new_owner=? and old_owner=? and turn>=? and turn<=? order by turn',
                                 pl, tp.get(tgt), t, pq if pq is not None else LAST[g])]
        wars.append(dict(g=g, t=t, target=tgt, ratio=mp[0][0] / mt[0][0] if mp and mt and mt[0][0] else None, peace=pq,
                         caps=len(caps), last=caps[-1] if caps else None))
ended = [w for w in wars if w['peace'] is not None]
first = {g: min(w['t'] for w in wars if w['g'] == g) for g in games}
ratios = sorted(w['ratio'] for w in wars if w['ratio'])
sales = []
for g in games:
    pl = H[g][0]
    d = q(g, '''select seq, turn, list(item) filter (where (side=1 and first=?) or (side=2 and second=?)) given,
                list(item) filter (where not ((side=1 and first=?) or (side=2 and second=?))) got,
                sum(data) filter (where item=0 and not ((side=1 and first=?) or (side=2 and second=?))) gold
                from deal_items where first=? or second=? group by 1, 2''', *([pl] * 8))
    sales += [(g, t, gold) for _, t, given, got, gold in d if given and 9 in given and got and 0 in got and 8 not in given]
sale_turns = {g: sorted(t for gg, t, _ in sales if gg == g) for g in games}
gaps = [b - a for g in games for a, b in zip(sale_turns[g], sale_turns[g][1:])]
units = sum(q(g, 'select count(*) from wl_U where player=?', H[g][0])[0][0] for g in games)
blds = sum(q(g, 'select count(*) from wl_N where player=?', H[g][0])[0][0] for g in games)
peace_gaps = sorted(b['t'] - a['peace'] for a, b in zip(ended, ended[1:]) if a['g'] == b['g'] and b['t'] >= a['peace'])
P = collections.OrderedDict()
P['war_min_turn'] = (min(first.values()) - 10, f'the first declaration of each game ({", ".join(f"{g} {first[g]}" for g in games)}), the earlier less 10 turns for the build-up and the march')
r30 = []
for w in wars:
    g = w['g']; pl, team, _ = H[g]
    tpl = dict((t_, p_) for p_, t_ in q(g, 'select player, team from wl_P'))[w['target']]
    a = q(g, 'select power from wl_M where player=? and turn=?', pl, w['t'] - 30); b = q(g, 'select power from wl_M where player=? and turn=?', tpl, w['t'] - 30)
    if a and b and b[0][0]: r30.append(a[0][0] / b[0][0])
r30.sort()
P['prep_ratio_pct'] = (int(100 * r30[1]) // 10 * 10, f'the second-lowest power ratio of the human to its target thirty turns before the declaration (M lines) over {len(r30)} wars, rounded down to tens: the preparation begins against a team the seat matches this far')
P['decl_ratio_pct'] = (int(100 * ratios[0]) // 10 * 10, f'the lowest power ratio (M lines, the turn before) of the {len(ratios)} declarations, rounded down to tens: every declaration was at least this (most were at twice the power or more, hm_wars)')
p10 = {g: q(g, 'select quantile_cont(odds, 0.1), count(*) from wl_C where att=?', H[g][0])[0] for g in games}
P['attack_min_odds'] = (int(min(v for v, _ in p10.values())) // 10 * 10, 'the lower of the games\' 10th percentiles of the odds (per mille) of the human\'s attacks (C lines; ' + ', '.join(f'{g}: {round(v)} of {n} attacks' for g, (v, n) in p10.items()) + '), rounded down to tens; the seat attacks whenever its odds reach this')
# the war model (study/war.md, section 10): the first city taken in each war and the cities taken after it
def ycity(g, player, t):
    out = {}
    for x, y, d, fo in q(g, 'select x, y, defenders, "foreign" from wl_Y where player=? and turn=? order by seq', player, t):
        out.setdefault((x, y), (d, fo))
    return out


margins, first_d, next_d, siege = [], [], [], []
for w in wars:
    g = w['g']; pl, team, _ = H[g]
    tpl = dict((t_, p_) for p_, t_ in q(g, 'select player, team from wl_P'))[w['target']]
    end = w['peace'] if w['peace'] is not None else LAST[g]
    caps = q(g, 'select turn, x, y from wl_K where old_owner=? and new_owner=? and turn between ? and ? order by seq', tpl, pl, w['t'], end)
    tc, hc = ycity(g, tpl, w['t']), set(ycity(g, pl, w['t']))
    own = set(hc)
    for k, (t_, x, y) in enumerate(caps):
        d = min(max(abs(x - a), abs(y - b)) for a, b in own) if own else None
        if k == 0 and (x, y) in tc:
            first_d.append(d)
            if tc[(x, y)][0] <= 2: margins.append(tc[(x, y)][1] - tc[(x, y)][0])
        elif k > 0 and d is not None: next_d.append(d)
        own.add((x, y))
    for (x, y), (dfn, fo) in tc.items():
        od = [o for (o,) in q(g, 'select odds from wl_C where att=? and def=? and x=? and y=? and turn between ? and ?', pl, tpl, x, y, w['t'], end)]
        if any(o < 500 for o in od): siege.append((dfn, min(od)))
stage = []
for w in wars:
    g = w['g']; pl, team, _ = H[g]
    tpl = dict((t_, p_) for p_, t_ in q(g, 'select player, team from wl_P'))[w['target']]
    end = w['peace'] if w['peace'] is not None else LAST[g]
    fc = q(g, 'select x, y from wl_K where old_owner=? and new_owner=? and turn between ? and ? order by seq limit 1', tpl, pl, w['t'], end)
    if not fc: continue
    cx, cy = fc[0]
    ds = []
    for u, x, y, tx, ty in q(g, "select a1, a2, a3, a6, a7 from wl_A where player=? and turn=? and kind='MISSION' and a5='MISSION_MOVE_TO'", pl, w['t']):
        ui = q(g, 'select default_ai, domain from unit_info where unit=?', u)
        if ui and ui[0][1] == 'LAND' and ui[0][0] not in ('WORKER', 'SETTLE', 'EXPLORE', 'MERCHANT') and max(abs(int(tx) - cx), abs(int(ty) - cy)) <= 1:
            ds.append(max(abs(int(x) - cx), abs(int(y) - cy)))
    if ds: stage.append(statistics.median(ds))
P['stage_distance'] = (round(statistics.median(stage)), f'the median over {len(stage)} wars of the median distance, on the declaration day, from the first city taken to the plots from which the human\'s fighting land units were ordered onto it or next to it (A lines MISSION_MOVE_TO): the strike group gathers this far from the objective and closes in on the declaration')
P['war_gap_turns'] = (min(peace_gaps), f'the shortest time from a peace to the next declaration of the same game ({len(peace_gaps)} gaps)')
P['strike_margin'] = (round(statistics.median(margins)), f'the median, over the {len(margins)} wars whose first city taken had at most two defenders (raids), of the land units of other players within two plots of it (Y lines, the declaration turn) less its defenders; the strike group is the defenders plus this')
P['target_max_distance'] = (max(first_d), f'the farthest, from the human\'s cities (Y lines, the declaration turn), of the first cities taken in the {len(first_d)} wars')
P['next_target_max_distance'] = (max(next_d), f'the farthest of the {len(next_d)} later cities taken in a war from the human\'s cities and those taken before in the same war')
if siege:
    P['siege_defenders'] = (min(d for d, _ in siege), f'the fewest defenders (Y lines, the declaration turn) of a city the human attacked at odds under 500 ({len(siege)} cities); there the strike group may attack at siege_min_odds')
    P['siege_min_odds'] = (min(o for _, o in siege) // 10 * 10, 'the lowest odds (per mille, C lines) of the human\'s attacks on those cities, rounded down to tens')
else:
    P['siege_defenders'] = (999, 'no attack of the human at odds under 500 in these games: the siege rule is off')
    P['siege_min_odds'] = (P['attack_min_odds'][0], 'as attack_min_odds: the siege rule is off')
ob_first = {g: q(g, 'select min(turn) from deal_items where item=5 and (first=? or second=?)', H[g][0], H[g][0])[0][0] for g in games}
P['ob_min_turn'] = (min(ob_first.values()), 'the first open-borders deal of the human (deal items TRADE_OPEN_BORDERS: ' + ', '.join(f'{g} {t}' for g, t in ob_first.items()) + '), the earlier; from then on the seat offers open borders to every AI met')
P['ob_every'] = (10, 'not measured: an AI that refused is asked again after this many turns')
P['home_keep'] = (1, 'not measured: a city keeps at least this many defenders when its units join a strike group (the human\'s cities held one or two; study/war.md, section 7)')
P['stage_max_turns'] = (10, 'the approach table covers the ten days before a declaration (study/war.md, section 4): units farther than this many turns from the staging plot are not called')
ob_first = {g: q(g, 'select min(turn) from deal_items where item=5 and (first=? or second=?)', H[g][0], H[g][0])[0][0] for g in games}
P['ob_min_turn'] = (min(ob_first.values()), 'the first open-borders deal of the human (deal items TRADE_OPEN_BORDERS: ' + ', '.join(f'{g} {t}' for g, t in ob_first.items()) + '), the earlier; from then on the seat offers open borders to every AI met')
P['ob_every'] = (10, 'not measured: an AI that refused is asked again after this many turns')
P['home_keep'] = (1, 'not measured: a city keeps at least this many defenders when its units join a strike group (the human\'s cities held one or two; study/war.md, section 7)')
P['stage_max_turns'] = (10, 'the approach table covers the ten days before a declaration (study/war.md, section 4): units farther than this many turns from the staging plot are not called')
P['prep_max_turns'] = (30, 'not in the data (every human preparation ended in a declaration): a preparation is given up after this')
stall = [w['peace'] - w['last'] for w in ended if w['last'] is not None]
P['war_stall_turns'] = (math.ceil(statistics.median(stall)), f'the median, rounded up, of turns from the last capture to peace over the {len(stall)} ended wars with a capture')
lens = [w['peace'] - w['t'] for w in ended]
P['war_max_turns'] = (max(lens), f'the longest of the {len(lens)} ended wars (declaration to peace)')
P['trade_min_turn'] = (min(t for _, t, _ in sales), f'the first sale of a tech for gold ({len(sales)} sales: D items, tech given, gold received, no peace treaty)')
P['trade_every'] = (round(statistics.mean(gaps)), f'the mean of the {len(gaps)} gaps between sales of the same game, rounded')
P['trade_min_gold'] = (min(gold for _, _, gold in sales), 'the smallest gold received for a tech')
P['ai_every'] = (round((units + blds) / units), f'one choice in this many is the AI\'s: the human\'s completions ({blds} buildings, N lines; {units} units, U lines) over its unit completions, rounded')
FIGHT = ('COUNTER', 'ATTACK', 'ATTACK_CITY', 'CITY_DEFENSE', 'ASSAULT_SEA', 'ATTACK_SEA')
built = lambda g, lo, hi: sum(1 for (u,) in q(g, 'select unit from wl_U where player=? and turn between ? and ?', H[g][0], lo, hi)
                              if (q(g, 'select default_ai from unit_info where unit=?', u) or [('',)])[0][0] in FIGHT)
pre_u = sum(built(w['g'], w['t'] - 30, w['t'] - 1) for w in wars); base_u = sum(built(w['g'], w['t'] - 60, w['t'] - 31) for w in wars)
P['ai_every_war'] = (max(1, round(P['ai_every'][0] * base_u / max(1, pre_u))), f'ai_every scaled by the fighting units the human built in the thirty turns before its declarations against the thirty before those (U lines, DefaultUnitAI: {pre_u} against {base_u}), rounded, at least one: during a preparation or war the AI builds the seat\'s units that much more often')
P['settler_min_pop'] = (3, 'not measured: a city builds a settler only from this size')
P['max_cities'] = (99, 'no limit')
prow = [[k, v, why] for k, (v, why) in P.items()]
reg.result_table('hm_params', ['parameter', 'value', 'rule'], prow, 'turns', 'human', 'whole game',
                 f'W, Q, K, M, A, C and Y lines and deal items of the human in {gl}; turns except: decl_ratio_pct (per cent), trade_min_gold '
                 '(gold), ai_every (choices), strike_margin and home_keep (units), target_max_distance, '
                 'next_target_max_distance and stage_distance (plots), siege_defenders (units), attack_min_odds and siege_min_odds (per mille)', list(P), n=len(wars))
wrows = [[f'{w["g"]} {w["t"]}', w['target'], round(w['ratio'], 2) if w['ratio'] else '', w['peace'] if w['peace'] is not None else '-',
          w['caps'], w['last'] if w['last'] is not None else '-'] for w in wars]
reg.result_table('hm_wars', ['declaration', 'target_team', 'power_ratio', 'peace_turn', 'cities_taken', 'last_capture_turn'], wrows, 'turn',
                 'human', 'each declaration', f'W lines of the human team in {gl}, the power of both (M lines, the turn before), the first Q line of '
                 'the pair from then on, and the K lines of cities taken from the target in between', [r[0] for r in wrows], n=len(wars))

with open(OUT, 'w') as f:
    f.write(f'# hmpolicy.py from {gl}\n')
    for x in techs: f.write(f'TECH TECH_{x}\n')
    for c in policy_civics: f.write(c + '\n')
    for b in tplc: f.write(f'BUILD {cls[b]}\n')
    for k, (v, _) in P.items(): f.write(f'PARAM {k} {v}\n')
reg.save()
print(open(OUT).read(), file=sys.stderr)
