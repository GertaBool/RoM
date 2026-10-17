#!/usr/bin/env python3
"""Turn one logged game into a fixed set of tables (the same for every game).

usage: gamedata.py <WarLog.log> <out dir> --human N --records records.json
                   [--state state0.json] [--bbai BBAI.log] [--cuts 50,100,...]

Inputs:
  WarLog.log    the game's war log (WAR_LOG = 1); timestamps and CRLF are stripped
  records.json  xmlread.py output, for unit roles and XML costs
  state0.json   optional: the save loaded and dumped by the headless harness
                (cities, every city tile, units, civics, civic and building scores)
  BBAI.log      optional: AI decision log from turns replayed from the save

Outputs in <out dir>, one CSV per table, plus summary.md with the main figures:
  economy.csv      M lines: per turn and player
  techs.csv        X lines: turn each player got each tech
  spending.csv     U and N lines priced at the costs the game itself reported
                   (Y line "needed"), else XML cost x the observed speed factor
  buildings.csv    N lines
  wars.csv         W, Q, K, Z lines
  battles.csv      C lines joined with their R result
  cities_war.csv   Y lines
  human_orders.csv / human_builds.csv / human_civics.csv / human_research.csv /
  human_commands.csv   the human's A lines, by kind
  great_people.csv V lines
  tiles.csv        (with --state) every city tile: owner, group, worked, yields
  cities.csv       (with --state) every city: pop, yields, buildings, order
  civic_scores.csv (with --state) each AI's own score for every civic
  ai_choices.csv   (with --bbai) production choices by branch of AI_chooseProduction
Nothing here infers; summary.md states figures only.
"""
import argparse, collections, csv, json, os, re, statistics as st

ap = argparse.ArgumentParser()
ap.add_argument('log'); ap.add_argument('out')
ap.add_argument('--human', type=int, required=True)
ap.add_argument('--records', required=True)
ap.add_argument('--state'); ap.add_argument('--bbai')
ap.add_argument('--cuts', default='50,100,150,200,250')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
H = str(a.human)
R = json.load(open(a.records)); UI = R['UnitInfo']; BI = R['BuildingInfo']; BC = R['BuildingClassInfo']

L = []
for raw in open(a.log, encoding='latin-1'):
    raw = raw.rstrip('\r\n')
    raw = re.sub(r'^\[[^\]]*\] ', '', raw)
    if raw: L.append(raw.split('\t'))
by = collections.defaultdict(list)
for l in L: by[l[0]].append(l)
players = {l[1]: dict(team=l[2], civ=l[3][13:], leader=l[4][7:], human=l[5]) for l in by['P']}
ais = [p for p in players if p not in (H, '50')]
# The log usually ends mid-turn: the last full turn is the last one on which every player
# has an M line, or, in logs without M lines, the turn before the last T line.
m_count = collections.Counter(int(l[1]) for l in by['M'])
if m_count:
    last_turn = max(t for t in m_count if m_count[t] >= m_count.get(t - 1, 0))
else:
    last_turn = max((int(l[1]) for l in by['T']), default=1) - 1
cuts = [int(c) for c in a.cuts.split(',') if int(c) < last_turn] + [last_turn]

def write(name, header, rows):
    with open(os.path.join(a.out, name), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def who(p): return 'human' if p == H else ('barbarian' if p == '50' else 'ai')

# ---- economy (M) ----
MF = ['cities', 'pop', 'land', 'food', 'hammers', 'commerce', 'research', 'gold_rate', 'gold', 'military', 'power', 'score',
      'research_slider', 'golden_age_turns']
eco = {}
for l in by['M']:
    v = [int(x) for x in l[3:]] + [None] * (len(MF) - len(l[3:]))
    eco[(int(l[1]), l[2])] = v[:len(MF)]
write('economy.csv', ['turn', 'player', 'who'] + MF, [[t, p, who(p)] + v for (t, p), v in sorted(eco.items())])

# ---- techs (X) ----
write('techs.csv', ['turn', 'player', 'who', 'tech'], [[l[1], l[2], who(l[2]), l[3]] for l in by['X']])

# ---- costs observed in Y lines ----
obs = collections.defaultdict(list)
for l in by['Y']:
    if l[7] != '-': obs[(l[7], l[2] == H)].append(int(l[9]))
ru, rb = [], []
for (o, hum), v in obs.items():
    base = int(((UI.get(o) or BI.get(o)) or {}).get('iCost') or 0)
    if base > 0: (ru if o.startswith('UNIT_') else rb).append(st.median(v) / base)
fu = st.median(ru) if ru else 1.0; fb = st.median(rb) if rb else 1.0
def cost(kind, name, hum):
    o = ('UNIT_' if kind == 'U' else 'BUILDING_') + name
    v = obs.get((o, hum)) or obs.get((o, not hum))
    if v: return st.median(v), 'observed'
    base = int(((UI.get(o) if kind == 'U' else BI.get(o)) or {}).get('iCost') or 0)
    return base * (fu if kind == 'U' else fb), 'xml'
def ucat(n):
    r = UI.get('UNIT_' + n, {}); ai = r.get('DefaultUnitAI', '')
    if ai == 'UNITAI_SETTLE': return 'settlers'
    if ai == 'UNITAI_WORKER': return 'workers'
    if ai == 'UNITAI_WORKER_SEA': return 'workboats'
    if r.get('Domain') == 'DOMAIN_SEA': return 'navy'
    return 'land military' if int(r.get('iCombat') or 0) > 0 else 'other units'
sp_rows = []
for l in by['U'] + by['N']:
    if l[2] == '50': continue
    c, src = cost(l[0], l[3], l[2] == H)
    sp_rows.append([l[1], l[2], who(l[2]), 'unit' if l[0] == 'U' else 'building', l[3],
                    ucat(l[3]) if l[0] == 'U' else 'buildings', round(c), src])
write('spending.csv', ['turn', 'player', 'who', 'kind', 'item', 'category', 'hammers', 'cost_source'], sp_rows)

# ---- buildings, wars, battles, cities in war, great people ----
def world(b):
    c = BC.get(BI.get('BUILDING_' + b, {}).get('BuildingClass', ''), {})
    return str(c.get('iMaxGlobalInstances', '-1')) == '1'
write('buildings.csv', ['turn', 'player', 'who', 'building', 'x', 'y', 'world_wonder'],
      [[l[1], l[2], who(l[2]), l[3], l[4], l[5], int(world(l[3]))] for l in by['N']])
write('wars.csv', ['kind', 'turn', 'a', 'b', 'x', 'y', 'pop'],
      [[{'W': 'war', 'Q': 'peace', 'K': 'captured', 'Z': 'razed'}[l[0]], l[1], l[2], l[3]] + (l[4:7] if l[0] in 'KZ' else ['', '', ''])
       for l in L if l[0] in 'WQKZ'])
res = {}
for l in by['R']: res.setdefault((l[1], l[2], l[3], l[5], l[6]), []).append(l)
bat = []
for l in by['C']:
    rr = res.get((l[1], l[2], l[3], l[6], l[7])) or []
    won = 'attacker' if rr else ('defender' if res.get((l[1], l[6], l[7], l[2], l[3])) else 'withdrew/unknown')
    bat.append([l[1], l[2], who(l[2]), l[3], l[4], l[5], l[6], who(l[6]), l[7], l[8], l[9], l[10], l[11], l[12], l[13],
                l[14], l[15], int(l[16]) / 10, l[17], won])
write('battles.csv', ['turn', 'att', 'att_who', 'att_unit', 'att_hp', 'att_xp', 'def', 'def_who', 'def_unit', 'def_hp', 'def_xp',
                      'x', 'y', 'terrain', 'feature', 'hills', 'city_def', 'win_pct', 'units_on_plot', 'result'], bat)
write('cities_war.csv', ['turn', 'owner', 'who', 'x', 'y', 'pop', 'hammers', 'order', 'stored', 'needed', 'defenders',
                         'best_defender', 'defence_pct', 'danger', 'foreign_units'], [[l[1], l[2], who(l[2])] + l[3:] for l in by['Y']])
write('great_people.csv', ['turn', 'player', 'who', 'unit', 'x', 'y', 'action'], [[l[1], l[2], who(l[2])] + l[3:] for l in by['V']])

# ---- the human's commands ----
A = [l for l in by['A'] if l[2] == H]
write('human_commands.csv', ['turn', 'kind', 'fields'], [[l[1], l[3], '|'.join(l[4:])] for l in A])
write('human_orders.csv', ['turn', 'x', 'y', 'item'], [[l[1], l[4], l[5], l[7]] for l in A if l[3] == 'ORDER'])
write('human_builds.csv', ['turn', 'x', 'y', 'build'], [[l[1], l[5], l[6], l[9]] for l in A if l[3] == 'MISSION' and l[8] == 'MISSION_BUILD'])
write('human_research.csv', ['turn', 'chosen'], [[l[1], l[4]] for l in A if l[3] == 'RESEARCH'])
civ_rows, prev = [], None
for l in A:
    if l[3] != 'CIVICS': continue
    cur = [c for c in l[4].split(',') if c]
    for c in cur:
        if prev is None or c not in prev: civ_rows.append([l[1], c])
    prev = cur
write('human_civics.csv', ['turn', 'adopted'], civ_rows)

# ---- state dump ----
summ_state = []
if a.state:
    d = json.load(open(a.state))
    cap = {(int(l[4]), int(l[5])) for l in by['K'] if l[3] == H}
    trows, crows, cvrows = [], [], []
    for p in d['players']:
        pid = str(p['id'])
        for c in p['cities']:
            grp = 'ai' if pid != H else ('human_captured' if (c['x'], c['y']) in cap else 'human_founded')
            crows.append([pid, grp, c['x'], c['y'], c['pop'], c['food'], c['prod'], c['commerce'], c['spec'], c['order'], len(c['buildings'])])
            for t in c.get('tiles', []):
                trows.append([pid, grp, c['x'], c['y']] + t)
        for cv in p.get('civicValues', []):
            if pid != H: cvrows.append([pid, cv[0], cv[1], cv[2], int(cv[0] in p['civics'])])
    write('cities.csv', ['player', 'group', 'x', 'y', 'pop', 'food_surplus', 'hammers', 'commerce', 'specialists', 'order', 'buildings'], crows)
    write('tiles.csv', ['player', 'group', 'city_x', 'city_y', 'worked', 'terrain', 'feature', 'improvement', 'hills', 'river', 'bonus',
                        'food', 'hammers', 'commerce'], trows)
    write('civic_scores.csv', ['player', 'civic', 'option', 'score', 'in_force'], cvrows)
    for grp in ('human_founded', 'human_captured', 'ai'):
        T = [r for r in trows if r[1] == grp]; W = [r for r in T if r[4] == 1]
        cs = [r for r in crows if r[1] == grp]
        if not cs: continue
        pop = sum(r[4] for r in cs); th = sum(r[12] for r in W); tc = sum(r[13] for r in W)
        summ_state.append((grp, len(cs), pop, sum(r[6] for r in cs) / max(1, pop), sum(r[7] for r in cs) / max(1, pop),
                           sum(r[6] for r in cs) / max(1, th), sum(r[7] for r in cs) / max(1, tc),
                           sum(1 for r in T if r[7] != '-') / max(1, len(T)), sum(1 for r in T if r[6] == 'FOREST') / max(1, len(T))))

# ---- AI decision log ----
if a.bbai:
    cnt = collections.Counter(m.group(1).strip() for m in re.finditer(r'City \S+ uses (.+?)(?: with .*)?$', open(a.bbai, errors='replace').read(), re.M))
    write('ai_choices.csv', ['branch', 'choices'], cnt.most_common())

# ---- summary.md: figures only ----
def ai_mean(t, i):
    v = [eco[(t, p)][i] for p in ais if (t, p) in eco and eco[(t, p)][0]]
    return st.mean(v) if v else float('nan')
out = [f'# Game data summary (human = player {H}, {players.get(H, {}).get("civ", "?")})', '',
       f'Generated by `tools/gamedata.py` from the war log' + (', the save dump' if a.state else '') + (', the AI decision log' if a.bbai else '') + '.',
       'Tables are in this folder; every figure below can be recomputed from them.', '']
# Mission metric at the last full turn: K cities the human took, L cities it lost,
# R human techs / best AI techs, S human score / best AI score (needs M lines).
ntech = collections.Counter(l[2] for l in by['X'] if int(l[1]) <= last_turn)
best_t = max((ntech[p] for p in ais), default=0)
K = sum(1 for l in by['K'] if l[3] == H and int(l[1]) <= last_turn)
Lost = sum(1 for l in by['K'] if l[2] == H and int(l[1]) <= last_turn)
sc = {p: eco[(last_turn, p)][11] for p in players if (last_turn, p) in eco}
best_s = max((sc[p] for p in ais if p in sc), default=0)
out += [f'## Mission metric at turn {last_turn} (the last full turn)', '', '| K taken | L lost | R techs | S score |', '|---|---|---|---|',
        f'| {K} | {Lost} | {ntech[H]}/{best_t} = {ntech[H] / max(1, best_t):.2f} | ' +
        (f'{sc[H]}/{best_s} = {sc[H] / max(1, best_s):.2f}' if H in sc else 'not logged') + ' |', '',
        '## Economy per citizen (M lines)', '', '| Turn | Human hammers | AI mean | Human commerce | AI mean | Human research | AI mean |', '|---|---|---|---|---|---|---|']
for t in cuts:
    h = eco.get((t, H))
    if not h: continue
    pc = lambda v, i: v[i] / max(1, v[1])
    av = [eco[(t, p)] for p in ais if (t, p) in eco and eco[(t, p)][1]]
    out.append(f'| {t} | {pc(h,4):.2f} | {st.mean(pc(v,4) for v in av):.2f} | {pc(h,5):.2f} | {st.mean(pc(v,5) for v in av):.2f} | {pc(h,6):.2f} | {st.mean(pc(v,6) for v in av):.2f} |')
out += ['', '## Techs (X lines)', '', '| Turn | Human | AI mean | AI max |', '|---|---|---|---|']
for t in cuts:
    n = collections.Counter(l[2] for l in by['X'] if int(l[1]) <= t)
    av = [n[p] for p in ais]
    out.append(f'| {t} | {n[H]} | {st.mean(av):.1f} | {max(av)} |')
out += ['', '## Production spending (U and N lines, game-reported costs)', '', '| To turn | Who | ' + ' | '.join(['buildings', 'land military', 'settlers', 'workers', 'navy', 'workboats']) + ' |', '|---|---|---|---|---|---|---|---|']
for t in cuts:
    for wh in ('human', 'ai'):
        c = collections.Counter();
        for r in sp_rows:
            if int(r[0]) <= t and r[2] == wh: c[r[5]] += r[6]
        tot = sum(c.values()) or 1
        out.append(f'| {t} | {wh} | ' + ' | '.join(f'{100*c[k]/tot:.0f} %' for k in ['buildings', 'land military', 'settlers', 'workers', 'navy', 'workboats']) + ' |')
out += ['', f'Cost factor observed: units ×{fu:.2f}, buildings ×{fb:.2f} of the XML cost.', '']
hb = [l for l in by['N'] if l[2] == H]
out += ['## Wars and battles', '']
for r in [r for r in [[l[0], l[1], l[2], l[3]] for l in L if l[0] in 'WQ'] if H in (r[2], r[3])]:
    out.append(f'- {"War" if r[0] == "W" else "Peace"} on turn {r[1]}: player {r[2]} – player {r[3]}')
hum_b = [b for b in bat if H in (b[1], b[6])]
if hum_b:
    out.append(f'- Battles involving the human: {len(hum_b)}; human attacks at win chances {min(b[17] for b in hum_b if b[1] == H):.0f}–{max(b[17] for b in hum_b if b[1] == H):.0f} %' if any(b[1] == H for b in hum_b) else '')
caps = [l for l in by['K'] if l[3] == H]
out.append(f'- Cities captured by the human: {len(caps)}')
nonsiege = [b for b in bat if b[2] == 'ai' and b[7] != 'barbarian' and b[17] < 5 and not any(s in b[3] for s in ('CATAPULT', 'RAM', 'BALLISTA', 'TREBUCHET'))]
out.append(f'- AI non-siege attacks under 5 %: {len(nonsiege)} of {sum(1 for b in bat if b[2] == "ai")}')
out += ['', '## Great people (V lines)', '', f'- Born: human {sum(1 for l in by["V"] if l[2] == H and l[6] == "BORN")}, AIs {sum(1 for l in by["V"] if l[2] != H and l[6] == "BORN")}',
        f'- Golden-age turns (M lines): human {sum(1 for (t, p), v in eco.items() if p == H and v[13])}, AIs {sum(1 for (t, p), v in eco.items() if p != H and v[13])}', '']
if summ_state:
    out += ['## Cities at the save (state dump)', '', '| Group | Cities | Pop | Hammers per citizen | Commerce per citizen | Hammers ÷ tile hammers | Commerce ÷ tile commerce | Land improved | Land forest |', '|---|---|---|---|---|---|---|---|---|']
    for g in summ_state:
        out.append(f'| {g[0]} | {g[1]} | {g[2]} | {g[3]:.2f} | {g[4]:.2f} | {g[5]:.2f} | {g[6]:.2f} | {g[7]:.0%} | {g[8]:.0%} |')
    out.append('')
if a.bbai:
    out += ['## AI production choices in the replayed turns (BBAI log)', '', '| Branch of AI_chooseProduction | Choices |', '|---|---|']
    out += [f'| {k} | {v} |' for k, v in cnt.most_common(15)] + ['']
open(os.path.join(a.out, 'summary.md'), 'w').write('\n'.join(x for x in out if x is not None) + '\n')
print('wrote', len(os.listdir(a.out)), 'files to', a.out)
