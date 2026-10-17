#!/usr/bin/env python3
"""Decision cases of the human, each with the cues known before it (study/plan.md, section 3).

usage: cases.py <game.duckdb> <human id> <out dir> <registry.fig.json>
       (run with ~/.cache/rom-ana/bin/python; the database comes from extract.py)

A decision's information set is every log line before it (seq < the decision's seq), restricted
to what the human sees: its own M lines (written at the end of its turn, so they include that
turn's effects), its own techs (X), declarations and peace involving anyone (W, Q, announced),
cities it captured (K) and its own commands. Other players' private lines are not used.

Classes (one CSV each in <out dir>, cases_<class>.csv; label y and binary cues):
  slider_turn   every turn the human ended: y = 1 if it clicked the research slider that turn
  slider_dir    turns with a net research change: y = 1 if the net change was toward gold
  upgrade_turn  every turn the human ended: y = 1 if it upgraded a unit that turn
  order_unit    every city order: y = 1 if the order is a unit (order type 0, TRAIN); no economy cue,
                so games without M lines (the first log version) have these cases too
The moment of a turn case is its first deciding command, or the human's TURN line if none.
Slider moves forced by CvPlayer::verifyGoldCommercePercent are not commands and are not cases.
"""
import bisect, collections, csv, os, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

DB, H, OUT, REG = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
con = duckdb.connect(DB, read_only=True)
q = lambda s: con.execute(s).fetchall()

teams = dict(q('select player, team from wl_P'))
if any(teams[p] != p for p in teams):
    raise SystemExit('teams differ from players: map W/Q teams to players before using this tool')
A = q(f'select seq, turn, kind, a1, a2, a3, a4, a5 from wl_A where player={H} order by seq')
M = q(f'select seq, turn, gold, gold_rate, slider from wl_M where player={H} order by seq')
WQ = q('select seq, turn, team, target, 1 from wl_W union all select seq, turn, team, target, 0 from wl_Q order by 1')
K = q(f'select seq, turn, x, y from wl_K where new_owner={H} order by seq')
X = q(f'select seq, turn from wl_X where player={H} order by seq')
Mseq = [m[0] for m in M]
Mturn = {m[1]: m for m in M}


def m_prev(s):
    i = bisect.bisect_left(Mseq, s) - 1
    return M[i] if i >= 0 else None


def war_state(s):
    w = set()
    for e in WQ:
        if e[0] >= s: break
        if H in (e[2], e[3]):
            o = e[3] if e[2] == H else e[2]
            (w.add if e[4] else w.discard)(o)
    return w


def recent(events, s, t, k, pred=lambda e: True):
    return int(any(e[0] < s and e[1] >= t - k and pred(e) for e in events))


# MISSION fields: a1 unit, a2 x, a3 y, a4 group size, a5 mission
moves = q(f"select seq, turn, a2, a3 from wl_A where player={H} and kind='MISSION' and a5='MISSION_FOUND' order by seq")
found = [(t, int(x), int(y)) for _, t, x, y in moves]
capital = found[0][1:] if found else None

turn_seq = {}
for a in A:
    if a[2] == 'TURN': turn_seq.setdefault(a[1], a[0])
clicks = collections.defaultdict(list); upg = collections.defaultdict(list)
for a in A:
    if a[2] == 'PERCENT' and a[3] == '1': clicks[a[1]].append((a[0], int(a[4])))
    if a[2] == 'COMMAND' and a[7] == 'COMMAND_UPGRADE': upg[a[1]].append(a[0])

rows = collections.defaultdict(list)
CUES = {
    'slider_turn': ['gold_rate_neg', 'at_war', 'declared_3', 'peace_3', 'captured_3'],
    'slider_dir': ['gold_rate_neg', 'at_war', 'declared_3', 'slider_high'],
    'upgrade_turn': ['declared_1', 'at_war', 'gold_rate_pos', 'gold_doubled_10', 'tech_3'],
    'order_unit': ['at_war', 'declared_3', 'capital', 'captured_city', 'young_city'],
}
for t, ts in sorted(turn_seq.items()):
    for cls, events in (('slider_turn', clicks), ('upgrade_turn', upg)):
        s = (events[t][0][0] if cls == 'slider_turn' else events[t][0]) if events.get(t) else ts
        mp = m_prev(s)
        if mp is None: continue
        w = war_state(s)
        decl = lambda k: recent(WQ, s, t, k, lambda e: e[4] == 1 and e[2] == H)
        if cls == 'slider_turn':
            c = dict(gold_rate_neg=int(mp[3] < 0), at_war=int(bool(w)), declared_3=decl(3),
                     peace_3=recent(WQ, s, t, 3, lambda e: e[4] == 0 and H in (e[2], e[3])), captured_3=recent(K, s, t, 3))
            rows[cls].append(dict(seq=s, turn=t, y=int(bool(clicks.get(t))), **c))
            net = sum(v for _, v in clicks.get(t, []))
            if net:
                rows['slider_dir'].append(dict(seq=s, turn=t, y=int(net < 0), gold_rate_neg=c['gold_rate_neg'],
                                               at_war=c['at_war'], declared_3=c['declared_3'], slider_high=int(mp[4] >= 70)))
        else:
            back = Mturn.get(mp[1] - 10)
            rows[cls].append(dict(seq=s, turn=t, y=int(bool(upg.get(t))), declared_1=decl(1), at_war=int(bool(w)),
                                  gold_rate_pos=int(mp[3] >= 0), gold_doubled_10=int(back is not None and mp[2] >= 2 * max(1, back[2])),
                                  tech_3=recent(X, s, t, 3)))
for a in A:
    if a[2] != 'ORDER': continue
    s, t, x, y = a[0], a[1], int(a[3]), int(a[4])
    cap = [k for k in K if k[0] < s and (k[2], k[3]) == (x, y)]
    fd = [f for f in found if (f[1], f[2]) == (x, y) and f[0] <= t]
    born = max([k[1] for k in cap] + [f[0] for f in fd]) if (cap or fd) else None
    rows['order_unit'].append(dict(seq=s, turn=t, y=int(a[5] == '0'), at_war=int(bool(war_state(s))),
                                   declared_3=recent(WQ, s, t, 3, lambda e: e[4] == 1 and e[2] == H),
                                   capital=int(capital == (x, y)), captured_city=int(bool(cap)),
                                   young_city=int(born is not None and t - born <= 20)))

os.makedirs(OUT, exist_ok=True)
paths = []
for cls, cues in CUES.items():
    p = os.path.join(OUT, f'cases_{cls}.csv'); paths.append(p)
    with open(p, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['seq', 'turn', 'y'] + cues)
        for r in rows[cls]: w.writerow([r['seq'], r['turn'], r['y']] + [r[c] for c in cues])
reg = Registry(REG, [DB] + paths)
who = f'human (player {H})'
for cls in CUES:
    R = rows[cls]
    if not R: continue
    span = f"{min(r['turn'] for r in R)}-{max(r['turn'] for r in R)}"
    reg.fig(f'{cls}_n', len(R), 'turns' if cls.endswith('turn') or cls == 'slider_dir' else 'orders', who, span, f'cases_{cls}.csv')
    reg.fig(f'{cls}_pos', sum(r['y'] for r in R), 'turns' if cls.endswith('turn') or cls == 'slider_dir' else 'orders', who, span,
            f'cases_{cls}.csv, y = 1')
# Source checks the cases rest on (study/plan.md, section 2)
after = q(f"""select count(*), count(distinct a.turn) from wl_A a join wl_M m on m.player={H} and m.turn=a.turn
           where a.player={H} and a.kind not in ('TURN','AUTOMOVES') and a.seq > m.seq""")[0]
reg.fig('cmds_after_own_M', after[0], 'orders', who, 'all turns', 'wl_A rows after the human\'s own wl_M row of the same turn')
sl = q(f"""with m as (select turn, slider from wl_M where player={H}),
            c as (select turn, sum(cast(a2 as int)) ch from wl_A where player={H} and kind='PERCENT' and a1='1' group by turn),
            j as (select m.turn, m.slider - lag(m.slider) over (order by m.turn) d, coalesce(c.ch, 0) ch from m left join c using (turn))
            select count(*), coalesce(sum(case when d = ch then 1 else 0 end), 0), coalesce(sum(case when d <> ch and ch = 0 then 1 else 0 end), 0)
            from j where d is not null""")[0]
if sl[0]:
    reg.fig('slider_turns_compared', sl[0], 'turns', who, 'all turns', 'wl_M slider change against wl_A PERCENT clicks, research')
    reg.fig('slider_consistent', sl[1], 'turns', who, 'all turns', 'turns where the slider change equals the clicks')
    reg.fig('slider_moved_no_click', sl[2], 'turns', who, 'all turns', 'slider changed with no click: CvPlayer::verifyGoldCommercePercent')
n_orders = q(f"select count(*) from wl_A where player={H} and kind='ORDER'")[0][0]
if n_orders != len(rows['order_unit']): raise SystemExit(f'order cases {len(rows["order_unit"])} != ORDER lines {n_orders}')
reg.fig('capital', f'{capital[0]},{capital[1]}' if capital else '-', 'category', who, found[0][0] if found else '-',
        'first MISSION_FOUND of the human')
reg.save()
print({c: (len(rows[c]), sum(r['y'] for r in rows[c])) for c in CUES}, file=sys.stderr)
