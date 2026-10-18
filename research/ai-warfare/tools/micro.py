#!/usr/bin/env python3
"""The human's micro-decisions in one game, from its generated tables, the scenario and the save dump.

usage: micro.py <game dir> <human id> <scenario.CivBeyondSwordWBSave> <state0.json> <records.json> > micro.md

Sections (figures only):
  1 attention: commands per turn and by kind; what the human automates
  2 city orders: queueing flags, unit share per city, first orders in captured cities
  3 workers: improvements by the plot's starting terrain; routes; human against AI worked tiles
  4 slider: research-slider changes with gold and war state
  5 combat: attacker health and experience, preparation before captures (bombard, ranged attacks)
  6 promotions by unit type
  7 garrisons at the save: units per city, human against AI, by distance to a foreign city
  8 requests from AIs: answer against the requester's distance and power
  9 great people: what each was used for
"""
import collections, csv, json, os, statistics as st, sys

G, H, WBS, DUMP = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
NOTRADE = {k[5:] for k, v in json.load(open(sys.argv[5]))['TechInfo'].items() if v.get('bTrade') is False}
rd = lambda f: list(csv.DictReader(open(os.path.join(G, f + '.csv'), newline='')))
C = rd('human_commands'); E = {(int(r['turn']), r['player']): r for r in rd('economy')}
W = rd('wars'); B = rd('battles'); BL = rd('buildings'); SP = rd('spending'); GP = rd('great_people')
DP = rd('diplomacy'); TI = rd('tiles'); CI = rd('cities')
d = json.load(open(DUMP))
steps = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def table(head, rows):
    print('| ' + ' | '.join(head) + ' |'); print('|' + '---|' * len(head))
    for r in rows: print('| ' + ' | '.join(str(x) for x in r) + ' |')
    print()


def F(c): return c['fields'].split('|')


last = max(int(r['turn']) for r in rd('techs'))
war_turns = set()
for w in W:
    if w['kind'] == 'war' and H in (w['a'], w['b']):
        o = w['b'] if w['a'] == H else w['a']
        pe = [int(x['turn']) for x in W if x['kind'] == 'peace' and {x['a'], x['b']} == {H, o} and int(x['turn']) >= int(w['turn'])]
        war_turns.update(range(int(w['turn']), (min(pe) if pe else last) + 1))

# ---- scenario plots ----
plots, cur = {}, None
for raw in open(WBS, encoding='latin-1'):
    s = raw.strip()
    if s == 'BeginPlot': cur = {}
    elif s == 'EndPlot':
        if cur and 'xy' in cur: plots[cur['xy']] = cur
        cur = None
    elif cur is not None:
        if s.startswith('x=') and ',y=' in s:
            x, y = s.split(','); cur['xy'] = (int(x[2:]), int(y[2:]))
        elif '=' in s:
            k, v = s.split('=', 1); cur.setdefault(k, v.split(',')[0])


def land(xy):
    p = plots.get(xy, {})
    t = p.get('TerrainType', '?')[8:]; pt = p.get('PlotType', '')
    hill = {'0': 'peak', '1': 'hill'}.get(pt, '')
    feat = p.get('FeatureType', '')[8:]
    riv = 'river' if any(k in p for k in ('isNOfRiver', 'isWOfRiver')) else ''
    bon = p.get('BonusType', '')[6:]
    return t, hill, feat, riv, bon

# ---- 1 attention ----
print('## 1. Attention\n')
per = collections.Counter(int(c['turn']) for c in C if c['kind'] not in ('TURN', 'AUTOMOVES'))
rows = []
for a in range(0, last + 1, 25):
    ts = range(a, min(a + 25, last + 1))
    v = [per[t] for t in ts]
    rows.append([f'{a}–{ts[-1]}', sum(v), f'{st.mean(v):.1f}', max(v), sum(1 for t in ts if t in war_turns)])
table(['Turns', 'Commands', 'Per turn', 'Most in one turn', 'Turns at war'], rows)
top = per.most_common(8)
print('Turns with the most commands: ' + ', '.join(f'{t} ({n}{", at war" if t in war_turns else ""})' for t, n in top) + '\n')
auto = collections.Counter(F(c)[0] for c in C if c['kind'] == 'COMMAND' and F(c)[4] == 'COMMAND_AUTOMATE')
amis = collections.Counter(F(c)[0] for c in C if c['kind'] == 'AUTOMISSION')
print('Automated (COMMAND_AUTOMATE): ' + ', '.join(f'{k} {v}' for k, v in auto.most_common()) +
      '. Repeated missions (AUTOMISSION): ' + ', '.join(f'{k} {v}' for k, v in amis.most_common()) + '.\n')
mis = collections.Counter(F(c)[4] for c in C if c['kind'] == 'MISSION')
print('Missions: ' + ', '.join(f'{k[8:]} {v}' for k, v in mis.most_common()) + '.\n')

# ---- 2 city orders ----
print('## 2. City orders\n')
O = [(int(c['turn']), F(c)) for c in C if c['kind'] == 'ORDER']
flags = collections.Counter(f[4] for _, f in O)
print('Order flags (Alt, Shift, Ctrl): ' + ', '.join(f'{k} {v}' for k, v in flags.most_common()) + f' of {len(O)} orders.\n')
caps = {(int(w['x']), int(w['y'])): int(w['turn']) for w in W if w['kind'] == 'captured' and w['b'] == H}
first_cap = collections.Counter()
for xy, t in caps.items():
    o = [f[3] for tt, f in O if (int(f[0]), int(f[1])) == xy and tt >= t]
    if o: first_cap[o[0].split('_', 1)[1]] += 1
print('First order in each captured city: ' + ', '.join(f'{k} {v}' for k, v in first_cap.most_common()) + '.\n')
units = collections.Counter(); allo = collections.Counter()
for t, f in O:
    xy = (int(f[0]), int(f[1])); allo[xy] += 1
    if f[3].startswith('UNIT_'): units[xy] += 1
rows = sorted(([f'{x},{y}', allo[(x, y)], units[(x, y)], f'{100 * units[(x, y)] / allo[(x, y)]:.0f} %'] for (x, y) in allo if allo[(x, y)] >= 8),
              key=lambda r: -int(r[2]))
table(['City', 'Orders', 'Unit orders', 'Unit share'], rows[:12])
mil = collections.Counter()
for s in SP:
    if s['player'] == H and s['kind'] == 'unit' and s['category'] in ('land military', 'navy') and int(s['turn']) >= 250: mil[s['item']] += 1
# Specialisation, human against AI: share of each city's production hammers spent on military units
# (spending.csv, U and N lines with plots), cities with at least 300 hammers logged.
rows = []
for who in ('human', 'ai'):
    hm = collections.defaultdict(lambda: [0, 0])
    for s_ in SP:
        if s_['who'] != who or not s_.get('x'): continue
        k = (s_['player'], s_['x'], s_['y'])
        hm[k][1] += int(s_['hammers'])
        if s_['category'] in ('land military', 'navy'): hm[k][0] += int(s_['hammers'])
    v = [m / t for m, t in hm.values() if t >= 300]
    if v: rows.append([who, len(v), f'{100 * st.median(v):.0f} %', f'{100 * sum(x >= .6 for x in v) / len(v):.0f} %',
                       f'{100 * sum(x <= .15 for x in v) / len(v):.0f} %', f'{100 * st.pstdev(v):.0f}'])
table(['Owner', 'Cities', 'Median military share of hammers', 'Cities ≥ 60 % military', 'Cities ≤ 15 % military', 'Spread (sd, points)'], rows)

# ---- 3 workers ----
print('## 3. Workers\n')
WB = [(int(c['turn']), (int(F(c)[1]), int(F(c)[2])), F(c)[5][6:]) for c in C if c['kind'] == 'MISSION' and F(c)[4] == 'MISSION_BUILD']
bt = collections.defaultdict(collections.Counter)
for t, xy, b in WB:
    tr, hill, feat, riv, bon = land(xy)
    key = ' '.join(x for x in (hill or tr, feat, riv, 'bonus' if bon else '') if x)
    bt[b][key] += 1
rows = [[b, sum(v.values()), ', '.join(f'{k} {n}' for k, n in v.most_common(5))] for b, v in sorted(bt.items(), key=lambda kv: -sum(kv[1].values()))]
table(['Build', 'Count', 'Starting plot (terrain, feature, river, resource)'], rows)
seq = [b for _, _, b in WB]
print('(Starting plot: the scenario\'s terrain before any chopping.)\n')
print('First 20 worker builds in order: ' + ', '.join(seq[:20]) + '.\n')
rt = sum(1 for c in C if c['kind'] == 'MISSION' and F(c)[4] == 'MISSION_ROUTE_TO')
print(f'Route-to missions (a road built along a path): {rt}.\n')
# worked tiles at the save: improvement on worked land tiles, human founded, captured and AI
rows = []
for grp in ('human_founded', 'human_captured', 'ai'):
    T = [r for r in TI if r['group'] == grp and r['worked'] == '1' and r['terrain'] not in ('COAST', 'OCEAN', 'LAKE')]
    if not T: continue
    c = collections.Counter(r['improvement'] for r in T)
    rows.append([grp, len(T), f"{100 * (len(T) - c['-']) / len(T):.0f} %"] + [f"{100 * c[k] / len(T):.0f} %" for k in
                 ('MINE', 'FARM', 'COTTAGE', 'HAMLET', 'VILLAGE', 'WINERY')] +
                [f"{st.mean(int(r['food']) + int(r['hammers']) + int(r['commerce']) for r in T):.2f}"])
table(['Group', 'Worked land tiles', 'Improved', 'Mine', 'Farm', 'Cottage', 'Hamlet', 'Village', 'Winery', 'Yield per tile'], rows)

# ---- 4 slider ----
print('## 4. Research slider (PERCENT commands; commerce 1 = research)\n')
PC = [(int(c['turn']), F(c)) for c in C if c['kind'] == 'PERCENT']
byt = collections.defaultdict(int)
for t, f in PC:
    if f[0] == '1': byt[t] += int(f[1])
rows = []
for t in sorted(byt):
    e = E.get((t, H)); e0 = E.get((t - 1, H))
    rows.append([t, f'{byt[t]:+d}', e0['research_slider'] if e0 else '-', e['research_slider'] if e else '-',
                 e0['gold'] if e0 else '-', e0['gold_rate'] if e0 else '-', 'war' if t in war_turns else ''])
table(['Turn', 'Change', 'Slider before', 'Slider after', 'Gold before', 'Gold per turn before', 'At war'], rows)

# ---- 5 combat ----
print('## 5. Combat\n')
HA = [b for b in B if b['att'] == H]
hp = collections.Counter('full' if b['att_hp'] == '100' else ('≥ 75' if int(b['att_hp']) >= 75 else '< 75') for b in HA)
print(f"Human attacker health: {', '.join(f'{k} {v}' for k, v in hp.most_common())} of {len(HA)}.\n")
ax = [int(b['att_xp']) for b in HA]; dx = [int(b['def_xp']) for b in HA]
print(f'Experience in human attacks: attacker median {st.median(ax)}, defender median {st.median(dx)}; '
      f'attacker above defender in {sum(a > b for a, b in zip(ax, dx))} of {len(HA)}.\n')
AA = [b for b in B if b['att_who'] == 'ai' and b['def_who'] == 'ai']
if AA:
    hp2 = sum(1 for b in AA if b['att_hp'] == '100')
    print(f'AI-on-AI attacks at full health: {hp2} of {len(AA)}; attacker experience median '
          f"{st.median(int(b['att_xp']) for b in AA)}, defender {st.median(int(b['def_xp']) for b in AA)}.\n")
prep = []
for xy, t in sorted(caps.items(), key=lambda kv: kv[1]):
    near = lambda c: steps((int(F(c)[5]), int(F(c)[6])), xy) <= 0 if F(c)[5].lstrip('-').isdigit() else False
    bom = [int(c['turn']) for c in C if c['kind'] == 'MISSION' and F(c)[4] in ('MISSION_BOMBARD', 'MISSION_RANGE_ATTACK')
           and F(c)[5].lstrip('-').isdigit() and steps((int(F(c)[5]), int(F(c)[6])), xy) <= 0 and t - 10 <= int(c['turn']) <= t]
    bomb_unit = collections.Counter(F(c)[0] for c in C if c['kind'] == 'MISSION' and F(c)[4] in ('MISSION_BOMBARD', 'MISSION_RANGE_ATTACK')
                                    and F(c)[5].lstrip('-').isdigit() and steps((int(F(c)[5]), int(F(c)[6])), xy) <= 0 and t - 10 <= int(c['turn']) <= t)
    att = [b for b in HA if (int(b['x']), int(b['y'])) == xy and int(b['turn']) == t]
    prep.append([t, f'{xy[0]},{xy[1]}', len(att), ', '.join(f'{k} {v}' for k, v in bomb_unit.items()) or '-',
                 f"{min(float(b['win_pct']) for b in att):.0f}–{max(float(b['win_pct']) for b in att):.0f}" if att else '-',
                 ', '.join(sorted({b['att_unit'] for b in att})) or '-'])
table(['Captured', 'City', 'Attacks that turn', 'Bombard or ranged attacks on it in the 10 turns before', 'Odds', 'Attackers'], prep)

# ---- 6 promotions ----
print('## 6. Promotions by unit type (COMMAND_PROMOTION)\n')
pu = collections.defaultdict(collections.Counter)
for c in C:
    f = F(c)
    if c['kind'] == 'COMMAND' and f[4] == 'COMMAND_PROMOTION': pu[f[0]][f[5][10:]] += 1
rows = [[u, sum(v.values()), ', '.join(f'{k} {n}' for k, n in v.most_common(7))] for u, v in sorted(pu.items(), key=lambda kv: -sum(kv[1].values()))]
table(['Unit', 'Promotions', 'Most chosen'], rows[:12])

# ---- 7 garrisons ----
print(f"## 7. Garrisons at the save (turn {d['turn']}): land military units on city plots\n")
owner = {(c['x'], c['y']): p['id'] for p in d['players'] for c in p['cities']}
rows = []
for who in ('human', 'ai'):
    v_front, v_back = [], []
    for p in d['players']:
        if (p['id'] == int(H)) != (who == 'human') or p['id'] == 50: continue
        here = collections.Counter((u[5], u[6]) for u in p['unitList'] if u[1] in ('city defense', 'attack', 'counter', 'city counter', 'reserve', 'collateral', 'attack city', 'city special', 'paradrop', 'pillage'))
        for c in p['cities']:
            xy = (c['x'], c['y'])
            dmin = min((steps(xy, o) for o, w in owner.items() if w != p['id']), default=99)
            (v_front if dmin <= 4 else v_back).append(here[xy])
    for lab, v in (('within 4 of a foreign city', v_front), ('farther', v_back)):
        if v: rows.append([who, lab, len(v), f'{st.mean(v):.1f}', st.median(v), sum(1 for x in v if x <= 1)])
table(['Owner', 'Cities', 'Count', 'Mean units', 'Median', 'Cities with 0–1'], rows)
roles = collections.Counter(u[1] for u in next(p for p in d['players'] if p['id'] == int(H))['unitList'])
print('Human units by role at the save: ' + ', '.join(f'{k} {v}' for k, v in roles.most_common()) + '.\n')

# ---- 8 requests ----
print('## 8. Requests from AIs and the answer (diplomacy.csv), with the requester\'s distance and power\n')
hc = lambda t: [(int(c['x']), int(c['y'])) for c in CI if c['player'] == H and int(c['founded']) <= t]
rows = []
for r in DP:
    if r['event'] not in ('give_help', 'refused_help', 'no_join_war', 'no_stop_trading', 'accept_demand', 'rejected_demand'): continue
    t, p = int(r['turn']), r['from']
    pc = [(int(c['x']), int(c['y'])) for c in CI if c['player'] == p]
    dist = min((steps(a, b) for a in pc for b in hc(t)), default='-')
    e, eh = E.get((t, p)), E.get((t, H))
    rows.append([t, p, r['event'], dist, f"{int(e['power']) / max(1, int(eh['power'])):.2f}" if e and eh else '-'])
table(['Turn', 'AI', 'Answer', 'Steps from its cities (at the save) to the human\'s', 'Its power ÷ human power'], rows)

# ---- 9 great people ----
print('## 9. Great people of the human (great_people.csv, MISSION lines)\n')
gp = [g for g in GP if g['player'] == H]
table(['Turn', 'Unit', 'Plot', 'Action'], [[g['turn'], g['unit'], f"{g['x']},{g['y']}", g['action']] for g in gp])

# ---- 10 assault order ----
print('## 10. Order of attacks within one assault (3+ attacks on one city plot in one turn)\n')
grp = collections.OrderedDict()
for b in HA:
    if b['city_def'] not in ('-1', ''): grp.setdefault((b['turn'], b['x'], b['y']), []).append(b)
rows = []
for (t, x, y), v in grp.items():
    if len(v) < 3: continue
    xp = [int(b['att_xp']) for b in v]; hp_ = [int(b['att_hp']) for b in v]
    rows.append([t, f'{x},{y}', len(v), ' → '.join(f"{b['att_unit'][:8]} {b['att_xp']}xp {b['att_hp']}hp {float(b['win_pct']):.0f}%" for b in v),
                 'yes' if xp[0] == max(xp) else 'no', sum(1 for b in v if b['result'] == 'attacker')])
table(['Turn', 'City', 'Attacks', 'Sequence (unit, experience, health, odds)', 'First has the most experience', 'Won'], rows)

# ---- 11 stack sizes ----
print('## 11. Size of the groups the human moves (MISSION_MOVE_TO, military units)\n')
rows = []
for lab, sel in (('at war', lambda t: t in war_turns), ('at peace', lambda t: t not in war_turns)):
    v = [int(F(c)[3]) for c in C if c['kind'] == 'MISSION' and F(c)[4] == 'MISSION_MOVE_TO' and F(c)[0] not in ('WORKER', 'SETTLER', 'ROMAN_COLONIST', 'WORKBOAT')
         and F(c)[3].isdigit() and sel(int(c['turn']))]
    if v: rows.append([lab, len(v), st.median(v), max(v), f'{100 * sum(x == 1 for x in v) / len(v):.0f} %', f'{100 * sum(x >= 4 for x in v) / len(v):.0f} %'])
table(['When', 'Moves', 'Median group', 'Largest', 'Single units', 'Groups of 4+'], rows)

# ---- 12 roads before wars ----
print('## 12. Route builds (TRACK, ROAD, PAVED, ROUTE_TO) within 4 steps of the next target\'s cities, in the 30 turns '
      'before each declaration, against the 30 turns before that\n')
RB = [(int(c['turn']), (int(F(c)[1]), int(F(c)[2]))) for c in C if c['kind'] == 'MISSION' and
      (F(c)[4] == 'MISSION_ROUTE_TO' or (F(c)[4] == 'MISSION_BUILD' and F(c)[5][6:] in ('TRACK', 'ROAD', 'PAVED')))]
own0 = {}
for c in CI: own0[(int(c['x']), int(c['y']))] = c['player']
rows = []
for w in W:
    if w['kind'] != 'war' or w['a'] != H: continue
    t, b = int(w['turn']), w['b']
    tc = [xy for xy in caps if any(k['a'] == b and (int(k['x']), int(k['y'])) == xy for k in W if k['kind'] == 'captured')]
    tc += [xy for xy, o in own0.items() if o == b]
    if not tc: continue
    near = lambda xy: min(steps(xy, y) for y in tc) <= 4
    a1 = [r for r in RB if t - 30 <= r[0] < t]; a0 = [r for r in RB if t - 60 <= r[0] < t - 30]
    rows.append([t, b, len(a1), sum(near(xy) for _, xy in a1), len(a0), sum(near(xy) for _, xy in a0)])
table(['Declared', 'Target', 'Route builds, 30 turns before', 'of them near the target', 'Route builds, 30 turns earlier', 'of them near the target'], rows)

# ---- 13 the requests themselves ----
# What each request was (CvPlayerAI::AI_doDiplo): join war = a random one of the requester's war
# enemies the human has met; stop trading = the requester's worst enemy; ask for help = a random
# tech the human can give it. Rebuilt from the W/Q lines (wars at the turn) and techs.csv.
print('## 13. The requests: what was asked, rebuilt from the state of that turn\n')
X = collections.defaultdict(dict)
for r in rd('techs'): X[r['player']].setdefault(r['tech'], int(r['turn']))
DL = rd('deals') if os.path.exists(os.path.join(G, 'deals.csv')) else []
def enemies(p, t):
    st_ = {}
    for w in W:
        if w['kind'] not in ('war', 'peace') or int(w['turn']) > t or p not in (w['a'], w['b']): continue
        o = w['b'] if w['a'] == p else w['a']
        st_[o] = w['kind'] == 'war'
    return sorted(o for o, v in st_.items() if v)
alive = lambda p, t: (t, p) in E
hcs = lambda t: [(int(c['x']), int(c['y'])) for c in CI if c['player'] == H and int(c['founded']) <= t]
pcs = lambda p: [(int(c['x']), int(c['y'])) for c in CI if c['player'] == p]
def dist(p, t):
    v = [steps(a, b) for a in pcs(p) for b in hcs(t)]
    return min(v) if v else '-'
def traded(o, t):
    return sum(1 for x in DL if {x['giver'], x['taker']} == {H, o} and t - 40 <= int(x['turn']) <= t and x['item'] in ('resource', 'open_borders', 'tech', 'gold'))
rows = []
for r in DP:
    t, p, ev = int(r['turn']), r['from'], r['event']
    if ev in ('no_join_war', 'join_war'):
        en = [o for o in enemies(p, t) if o != H]
        e_h = E.get((t, H))
        desc = '; '.join(f"{o}: {dist(o, t)} steps, power ×{int(E[(t, o)]['power']) / max(1, int(e_h['power'])):.2f} of human, "
                         f"{traded(o, t)} deal items in 40 turns, at war with human: {'yes' if o in enemies(H, t) else 'no'}"
                         for o in en if (t, o) in E and e_h)
        ep, eo = E.get((t, p)), None
        rows.append([t, p, ev, f"{len(en)} possible target(s): {desc or '-'}"])
    elif ev in ('no_stop_trading', 'stop_trading'):
        en = [o for o in enemies(p, t) if o != H]
        rows.append([t, p, ev, f"requester at war with {', '.join(en) or 'nobody'}; human deal items in 40 turns with them: "
                     + (', '.join(f'{o}: {traded(o, t)}' for o in en) or '-')])
    elif ev in ('give_help', 'refused_help'):
        ais = [q for q in X if q not in (H, '50')]
        cand = [k for k, tt in X[H].items() if tt < t and X[p].get(k, 10 ** 6) >= t and k not in NOTRADE]
        common = [k for k in cand if sum(1 for q in ais if X[q].get(k, 10 ** 6) < t) >= 5]
        given = [x['value'] for x in DL if int(x['turn']) == t and x['giver'] == H and x['taker'] == p and x['item'] == 'tech']
        rows.append([t, p, ev, f"{len(cand)} techs it could ask for, {len(common)} known by 5+ AIs"
                     + (f"; given: {', '.join(given)}" if given else '')])
table(['Turn', 'AI', 'Answer', 'What was asked (rebuilt)'], rows)
