#!/usr/bin/env python3
"""The human's decisions across logged games, from each game's generated tables.

usage: decisions.py <records.json> <games dir> game1:0 game2:2 game3:12 game4:3 > figures.md

Questions (each table names its source; a game without the source is left out):
  A  attack odds: what win chances the human attacks at, against the AI
  B  city assaults: the order of attacks on one city in one turn
  C  wars: declarer, power ratio the turn before, length, captures, peace after the last capture
  D  war targets: the target's rank among the AI neighbours by power, distance and cities
  E  unit tier at declaration: the human's strongest recent land unit against the target's best
     defender at the war's start
  F  upgrades and gold around declarations
  G  civics: turns from the prerequisite tech to adoption; civics adopted per switch
  H  research: how many AIs knew each tech the human chose, at the choice
  I  expansion: founding turns, distances to the capital and to the nearest own city
  J  first order in each new city
  K  promotions chosen, and when
  L  cities the human captured: nearer to the human's cities than to the owner's own other cities?
  M  city spacing: steps from each founded city to its owner's nearest earlier city, human against AI
  N  tech deals (game 4): AIs knowing each tech the human gave, sold or received, at the deal
Figures only.
"""
import collections, csv, json, os, statistics as st, sys

R = json.load(open(sys.argv[1]))
UI = R['UnitInfo']; CI = R['CivicInfo']
GD = sys.argv[2]
GAMES = [(g.split(':')[0], g.split(':')[1]) for g in sys.argv[3:]]
SIEGE = ('CATAPULT', 'RAM', 'BALLISTA', 'TREBUCHET', 'BALLISTA_ROME', 'ONAGER')


def rd(g, f):
    p = os.path.join(GD, g, f + '.csv')
    return list(csv.DictReader(open(p, newline=''))) if os.path.exists(p) else None


def steps(a, b): return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def q(v, f): return sorted(v)[min(len(v) - 1, int(f * len(v)))] if v else float('nan')


def combat(u): return int((UI.get('UNIT_' + u) or {}).get('iCombat') or 0)


def table(head, rows):
    print('| ' + ' | '.join(head) + ' |'); print('|' + '---|' * len(head))
    for r in rows: print('| ' + ' | '.join(str(x) for x in r) + ' |')
    print()


D = {}
for g, h in GAMES:
    d = {k: rd(g, k) for k in ('battles', 'wars', 'economy', 'techs', 'human_civics', 'human_research', 'human_commands',
                               'human_orders', 'cities', 'cities_war', 'spending')}
    d['h'] = h
    d['E'] = {(int(r['turn']), r['player']): r for r in d['economy']} if d['economy'] else {}
    d['X'] = collections.defaultdict(dict)
    for r in d['techs']: d['X'][r['player']].setdefault(r['tech'], int(r['turn']))
    D[g] = d

# ---- A attack odds ----
print('## A. Attack odds (battles.csv, win chance per mille / 10)\n')
rows = []
for g, d in D.items():
    h = d['h']
    for who, sel in (('human', lambda b: b['att'] == h), ('AI on human', lambda b: b['def'] == h and b['att_who'] == 'ai'),
                     ('AI on AI', lambda b: b['att_who'] == 'ai' and b['def_who'] == 'ai')):
        bs = [b for b in d['battles'] if sel(b)]
        for cls, f in (('all', lambda b: True), ('non-siege', lambda b: not any(s in b['att_unit'] for s in SIEGE))):
            v = [float(b['win_pct']) for b in bs if f(b)]
            if not v: continue
            won = sum(1 for b in bs if f(b) and b['result'] == 'attacker')
            rows.append([g, who, cls, len(v), f'{min(v):.0f}', f'{q(v, .1):.0f}', f'{st.median(v):.0f}',
                         f'{100 * sum(x >= 90 for x in v) / len(v):.0f} %', f'{100 * sum(x < 50 for x in v) / len(v):.0f} %',
                         f'{100 * won / len(v):.0f} %'])
table(['Game', 'Attacker', 'Units', 'Attacks', 'Min', '10th pct', 'Median', '≥ 90 %', '< 50 %', 'Won'], rows)

# ---- B city assaults ----
print('## B. City assaults by the human: attacks on one city plot in one turn, 3 or more (battles.csv, in log order)\n')
rows = []
for g, d in D.items():
    grp = collections.OrderedDict()
    for b in d['battles']:
        if b['att'] == d['h'] and b['city_def'] not in ('-1', ''):
            grp.setdefault((b['turn'], b['x'], b['y']), []).append(b)
    gs = [v for v in grp.values() if len(v) >= 3]
    if not gs: continue
    first_low = sum(1 for v in gs if float(v[0]['win_pct']) <= min(float(b['win_pct']) for b in v))
    first_siege = sum(1 for v in gs if any(s in v[0]['att_unit'] for s in SIEGE))
    rising = sum(1 for v in gs if all(float(v[i]['win_pct']) <= float(v[i + 1]['win_pct']) + 1e-9 for i in range(len(v) - 1)))
    rows.append([g, len(gs), st.median(len(v) for v in gs), first_low, first_siege, rising,
                 f"{st.median(float(v[0]['win_pct']) for v in gs):.0f}", f"{st.median(float(v[-1]['win_pct']) for v in gs):.0f}"])
table(['Game', 'Assaults', 'Median attacks', 'First attack has the lowest odds', 'First attacker is siege',
       'Odds never fall along the sequence', 'Median odds, first', 'Median odds, last'], rows)

# ---- C wars ----
print('## C. Wars declared by the human (wars.csv; power from economy.csv where logged)\n')
rows = []; ai_ratio = collections.defaultdict(list)
for g, d in D.items():
    h, W, E = d['h'], d['wars'], d['E']
    for w in W:
        if w['kind'] != 'war': continue
        t, a, b = int(w['turn']), w['a'], w['b']
        ea, eb = E.get((t - 1, a)), E.get((t - 1, b))
        ratio = f"{int(eb['power']) / max(1, int(ea['power'])):.2f}" if ea and eb else '-'
        if a != h and b != h:
            if ea and eb: ai_ratio[g].append(int(eb['power']) / max(1, int(ea['power'])))
            continue
        if a != h: continue
        pe = [int(x['turn']) for x in W if x['kind'] == 'peace' and {x['a'], x['b']} == {a, b} and int(x['turn']) >= t]
        end = min(pe) if pe else None
        caps = [int(x['turn']) for x in W if x['kind'] == 'captured' and x['a'] == b and x['b'] == h and t <= int(x['turn']) <= (end or 10 ** 6)]
        rows.append([g, t, b, ratio, (end - t) if end else 'open', len(caps), (min(caps) - t) if caps else '-',
                     (end - max(caps)) if (end and caps) else '-'])
table(['Game', 'Declared', 'Target', 'Target power ÷ human power (turn before)', 'Turns to peace', 'Cities taken',
       'Turns to first capture', 'Turns from last capture to peace'], rows)
rows = [[g, len(v), f'{min(v):.2f}', f'{st.median(v):.2f}', f'{max(v):.2f}'] for g, v in ai_ratio.items()]
print('AI declarations on AIs, for comparison: target power ÷ declarer power the turn before.\n')
table(['Game', 'Declarations', 'Min', 'Median', 'Max'], rows)


# ---- D targets ----
def cities_at(d, t):
    """Cities standing at turn t with their owner: save cities founded by then, owners rolled back
    through later K lines; razed cities from Z lines before their razing."""
    K = sorted((int(x['turn']), (int(x['x']), int(x['y'])), x['a'], x['b']) for x in d['wars'] if x['kind'] == 'captured')
    out = {}
    for c in d['cities'] or []:
        xy, f = (int(c['x']), int(c['y'])), int(c['founded'])
        if f > t: continue
        own = c['player']
        later = [k for k in K if k[1] == xy and k[0] > t and k[0] >= f]
        if later: own = later[0][2]
        out[xy] = own
    for z in d['wars']:
        if z['kind'] == 'razed' and int(z['turn']) > t:
            xy = (int(z['x']), int(z['y']))
            if xy not in out: out[xy] = z['a']
    return out


print('## D. War targets (games with a save dump): rank of the target among AI neighbours\n')
print('Neighbours: AIs with a city within 8 steps of a human city the turn before the declaration (cities reconstructed '
      'from the save and the K/Z lines; cities razed by AIs or founded and lost unseen are missing). Rank 1 = weakest '
      'power, nearest, fewest cities.\n')
rows = []
for g, d in D.items():
    if not d['cities'] or not d['E']: continue
    h = d['h']
    for w in d['wars']:
        if w['kind'] != 'war' or w['a'] != h: continue
        t, b = int(w['turn']), w['b']
        cs = cities_at(d, t - 1)
        hc = [xy for xy, o in cs.items() if o == h]
        nb = collections.defaultdict(lambda: 99); ncity = collections.Counter()
        for xy, o in cs.items():
            if o == h: continue
            ncity[o] += 1
            nb[o] = min(nb[o], min((steps(xy, y) for y in hc), default=99))
        cand = [o for o in nb if nb[o] <= 8 and (t - 1, o) in d['E']]
        if b not in cand: rows.append([g, t, b, len(cand), 'not a neighbour', '', '', '']); continue
        pw = lambda o: int(d['E'][(t - 1, o)]['power'])
        rk = lambda key: 1 + sum(1 for o in cand if key(o) < key(b))
        rows.append([g, t, b, len(cand), rk(pw), rk(lambda o: nb[o]), rk(lambda o: ncity[o]),
                     ', '.join(f'{o}:{pw(o)}/{nb[o]}' for o in sorted(cand, key=pw))])
table(['Game', 'Declared', 'Target', 'Neighbours', 'Power rank', 'Distance rank', 'Cities rank',
       'Neighbours by power (player:power/steps)'], rows)

# ---- E unit tier ----
print('## E. Land unit the human built most in the 30 turns before the declaration, against the target\'s best '
      'defender in its first Y line of the war (spending.csv, cities_war.csv; strength = iCombat)\n')
rows = []
for g, d in D.items():
    if not d['cities_war']: continue
    h = d['h']
    for w in d['wars']:
        if w['kind'] != 'war' or w['a'] != h: continue
        t, b = int(w['turn']), w['b']
        built = [s['item'] for s in d['spending'] if s['player'] == h and s['kind'] == 'unit' and t - 30 <= int(s['turn']) <= t
                 and s['category'] == 'land military']
        best = collections.Counter(built).most_common(1)[0][0] if built else None
        ys = [y for y in d['cities_war'] if y['owner'] == b and int(y['turn']) >= t]
        y0 = min((int(y['turn']) for y in ys), default=None)
        defs = collections.Counter(y['best_defender'] for y in ys if int(y['turn']) == y0)
        bd = max(defs, key=combat, default=None)
        rows.append([g, t, b, f'{best} ({combat(best)})' if best else '-', f'{bd} ({combat(bd)})' if bd else '-',
                     ', '.join(f'{k} {v}' for k, v in defs.most_common(4))])
table(['Game', 'Declared', 'Target', 'Human unit (strength)', 'Target best defender (strength)', 'Best defenders over its cities'], rows)

# ---- F upgrades and gold ----
print('## F. Upgrades and gold around the human\'s declarations (human_commands.csv, economy.csv)\n')
rows = []
for g, d in D.items():
    h = d['h']
    up = collections.Counter(int(c['turn']) for c in d['human_commands'] if 'COMMAND_UPGRADE' in c['fields'])
    decl = [int(w['turn']) for w in d['wars'] if w['kind'] == 'war' and w['a'] == h]
    if not up: continue
    near = sum(v for t, v in up.items() if any(-5 <= t - x <= 5 for x in decl))
    span = max(int(r['turn']) for r in d['techs'])
    window = len({t for x in decl for t in range(x - 5, x + 6) if 0 <= t <= span})
    gold = []
    for x in decl:
        e = d['E'].get((x - 1, h))
        prev = [int(d['E'][(t, h)]['gold']) for t in range(x - 31, x - 1) if (t, h) in d['E']]
        if e and prev: gold.append(f"{x}: {e['gold']} (median of 30 turns before {st.median(prev):.0f})")
    rows.append([g, sum(up.values()), near, f'{100 * window / max(1, span):.0f} %', '; '.join(gold) or '-'])
table(['Game', 'Upgrades', 'Within 5 turns of a declaration', 'Share of turns within 5 of a declaration',
       'Gold the turn before each declaration'], rows)

# ---- G civics ----
print('## G. Civics: turns from the prerequisite tech (CivicInfo TechPrereq) to adoption, and civics per switch\n')
rows = []
for g, d in D.items():
    h = d['h']; lags = []; per = collections.Counter(int(c['turn']) for c in d['human_civics'])
    first = min(per)
    for c in d['human_civics']:
        t = int(c['turn'])
        if t == first: continue
        tp = (CI.get(c['adopted']) or {}).get('TechPrereq')
        kt = d['X'][h].get(tp[5:]) if tp and tp != 'NONE' else None
        lags.append((c['adopted'][6:], t - kt if kt is not None else None))
    known = [l for _, l in lags if l is not None]
    rows.append([g, len(lags), sum(1 for l in known if l <= 1), f'{st.median(known):.0f}' if known else '-',
                 ', '.join(f'{n} {l}' for n, l in lags), ', '.join(f'{t}:{n}' for t, n in sorted(per.items()) if t != first)])
table(['Game', 'Adoptions', 'Within 1 turn of the tech', 'Median lag', 'Civic and lag', 'Turn: civics adopted'], rows)

# ---- H research ----
print('## H. Research: AIs that knew each tech the human chose, at the choice (human_research.csv, techs.csv)\n')
rows = []
for g, d in D.items():
    h = d['h']; ais = [p for p in d['X'] if p not in (h, '50')]
    v = []
    for r in d['human_research']:
        tech = r['chosen'][5:]
        if not tech: continue
        t = int(r['turn'])
        if d['X'][h].get(tech, -1) < t and tech in d['X'][h] and d['X'][h][tech] <= t: continue
        v.append((tech, sum(1 for p in ais if d['X'][p].get(tech, 10 ** 6) <= t)))
    zero = sum(1 for _, n in v if n == 0)
    first = sum(1 for tech, n in v if tech in d['X'][h] and all(d['X'][p].get(tech, 10 ** 6) > d['X'][h][tech] for p in ais))
    rows.append([g, len(v), zero, first, ', '.join(f'{t} {n}' for t, n in v)])
table(['Game', 'Choices', 'No AI knew it', 'Human first in the world', 'Tech and AIs knowing it'], rows)

# ---- I expansion ----
print('## I. Cities the human founded (cities.csv, save cities with group human_founded)\n')
rows = []
for g, d in D.items():
    if not d['cities']: continue
    h = d['h']
    fc = sorted((int(c['founded']), (int(c['x']), int(c['y']))) for c in d['cities'] if c['group'] == 'human_founded')
    cap = fc[0][1]
    for i, (t, xy) in enumerate(fc[1:], 1):
        rows.append([g, t, f'{xy[0]},{xy[1]}', steps(xy, cap), min(steps(xy, y) for _, y in fc[:i]), t - fc[i - 1][0]])
table(['Game', 'Founded', 'Plot', 'Steps to the capital', 'Steps to the nearest earlier own city', 'Turns since the previous'], rows)

# ---- J first order ----
print('## J. First order in each city after the capital (human_orders.csv)\n')
rows = []
for g, d in D.items():
    seen, first = set(), collections.Counter()
    cap = (d['human_orders'][0]['x'], d['human_orders'][0]['y'])
    for o in d['human_orders']:
        xy = (o['x'], o['y'])
        if xy in seen: continue
        seen.add(xy)
        if xy != cap: first[o['item'].split('_', 1)[1]] += 1
    rows.append([g, sum(first.values()), ', '.join(f'{k} {v}' for k, v in first.most_common())])
table(['Game', 'Cities', 'First order'], rows)

# ---- K promotions ----
print('## K. Promotions chosen (human_commands.csv; games whose log names them)\n')
rows = []
for g, d in D.items():
    pr = collections.Counter()
    for c in d['human_commands']:
        f = c['fields'].split('|')
        if len(f) > 5 and f[4] == 'COMMAND_PROMOTION' and f[5].startswith('PROMOTION_'):
            pr[f[5][10:].rstrip('0123456789')] += 1
    if pr: rows.append([g, sum(pr.values()), ', '.join(f'{k} {v}' for k, v in pr.most_common(10))])
table(['Game', 'Promotions', 'By line'], rows)
rows = []
for g, d in D.items():
    am = sorted(int(c['turn']) for c in d['human_commands'] if 'PROMOTION_AMPHIBIOUS' in c['fields'])
    if am: rows.append([g, len(am), am[0], am[-1], ', '.join(f'{t}' for t in am)])
if rows:
    print('Amphibious promotions by turn:\n'); table(['Game', 'Promotions', 'First', 'Last', 'Turns'], rows)

# ---- L captured cities ----
print('## L. Cities the human captured: steps to the nearest human city and to the owner\'s nearest other city, '
      'the turn before the capture (reconstructed as in D)\n')
rows = []
for g, d in D.items():
    if not d['cities']: continue
    h = d['h']
    for k in d['wars']:
        if k['kind'] != 'captured' or k['b'] != h: continue
        t, xy, o = int(k['turn']), (int(k['x']), int(k['y'])), k['a']
        cs = cities_at(d, t - 1); cs[xy] = o
        dh = min((steps(xy, y) for y, w in cs.items() if w == h), default=99)
        do = min((steps(xy, y) for y, w in cs.items() if w == o and y != xy), default=99)
        rows.append([g, t, f'{xy[0]},{xy[1]}', o, k['pop'], dh, do if do < 99 else 'none', 'yes' if dh < do else 'no'])
table(['Game', 'Captured', 'Plot', 'Owner', 'Pop', 'Steps to a human city', 'Steps to an own city', 'Nearer the human'], rows)

# ---- M spacing ----
print('## M. City spacing: steps from each city to the nearest earlier city of the same owner (save cities never '
      'captured; AI cities founded after turn 50)\n')
rows = []
for g, d in D.items():
    if not d['cities']: continue
    h = d['h']
    capt = {(int(k['x']), int(k['y'])) for k in d['wars'] if k['kind'] == 'captured'}
    by = collections.defaultdict(list)
    for c in d['cities']:
        xy = (int(c['x']), int(c['y']))
        if xy in capt and c['group'] != 'human_founded': continue
        by[c['player']].append((int(c['founded']), xy))
    for who, sel in (('human', lambda p: p == h), ('AI', lambda p: p != h)):
        v = []
        for p, cs in by.items():
            if not sel(p): continue
            cs.sort()
            for i, (t, xy) in enumerate(cs):
                if i == 0 or (who == 'AI' and t <= 50): continue
                v.append(min(steps(xy, y) for _, y in cs[:i]))
        if v: rows.append([g, who, len(v), min(v), f'{st.median(v):.0f}', max(v), f'{100 * sum(x <= 3 for x in v) / len(v):.0f} %'])
table(['Game', 'Owner', 'Cities', 'Min', 'Median', 'Max', '≤ 3 steps'], rows)

# ---- N deals ----
print('## N. Tech deals with the human: AIs that knew the tech at the deal (deals.csv, techs.csv)\n')
rows = []
for g, d in D.items():
    dl = rd(g, 'deals')
    if not dl: continue
    h = d['h']; ais = [p for p in d['X'] if p not in (h, '50')]
    for r in dl:
        if r['item'] != 'tech': continue
        t = int(r['turn']); tech = r['value']
        kind = 'received' if r['taker'] == h else 'given'
        pay = [x for x in dl if x['turn'] == r['turn'] and x['giver'] == r['taker'] and x['taker'] == r['giver']]
        rows.append([g, t, kind, r['giver'] if kind == 'received' else r['taker'], tech,
                     sum(1 for p in ais if d['X'][p].get(tech, 10 ** 6) < t), ', '.join(f"{x['item']} {x['value']}" for x in pay) or '-'])
table(['Game', 'Turn', 'Human', 'Other side', 'Tech', 'AIs knowing it before', 'In return'], rows)
