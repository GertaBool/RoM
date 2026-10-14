#!/usr/bin/env python3
"""Diplomacy statistics from harness scenario telemetry (run.jsonl files).

usage: dipl_analyze.py OUT.json RUN_DIR [RUN_DIR ...]
Each RUN_DIR holds run.jsonl (header line, then one line per turn).
Prints a text report and writes per-run metrics plus pooled tables to OUT.json.
"""
import json, sys, os, collections, statistics as st

ITEM = ['GOLD', 'GPT', 'MAPS', 'VASSAL', 'SURRENDER', 'OB', 'DP', 'PA', 'PEACE_TREATY',
        'TECH', 'RES', 'CITY', 'PEACE', 'WAR', 'EMBARGO', 'CIVIC', 'RELIGION']
WARPLAN = {-1: 'none', 0: 'attacked_recent', 1: 'attacked', 2: 'prep_limited', 3: 'prep_total',
           4: 'limited', 5: 'total', 6: 'dogpile'}
ATTC = ['closeBorders', 'war', 'peace', 'sameReligion', 'diffReligion', 'bonusTrade', 'openBorders',
        'defPact', 'rivalDefPact', 'rivalVassal', 'shareWar', 'favCivic', 'trade', 'rivalTrade', 'colony',
        'firstImpression', 'teamSize', 'betterRank', 'worseRank', 'lowRank', 'lostWar']


def side(items):
    return '+'.join(sorted(ITEM[i[0]] if 0 <= i[0] < len(ITEM) else str(i[0]) for i in items)) or '-'


def analyse(run_dir):
    rows = [json.loads(l) for l in open(os.path.join(run_dir, 'run.jsonl'))]
    hdr, turns = rows[0], [r for r in rows[1:] if 'p' in r]
    players = {p['id']: p for p in hdr['players']}
    # players can appear during the game (RoM spawns civilizations); they are
    # counted as their own team under the name P<id>
    team_of = collections.defaultdict(lambda: -1, {p['id']: p['team'] for p in hdr['players']})
    leader = {p['id']: p['leader'][7:] for p in hdr['players']}
    for r in turns:
        for p in r['p']:
            if p['id'] not in leader:
                leader[p['id']] = 'P%d' % p['id']
                team_of[p['id']] = r['teams'][-1] if p['id'] not in team_of else team_of[p['id']]
    members = collections.defaultdict(list)
    for pid, t in team_of.items():
        members[t].append(pid)
    out = dict(run=os.path.basename(run_dir), speed=hdr['speed'], players=len(players),
               turns=len(turns), first=turns[0]['t'], last=turns[-1]['t'])

    trades = collections.Counter()
    trade_items = collections.Counter()
    wars = []          # declarations
    open_wars = {}     # (a,b) team pair sorted -> war record
    captures = collections.Counter()
    prevalence = []    # per sampled turn: fractions of met pairs with OB, DP, vassal, war
    per_leader = collections.defaultdict(lambda: collections.Counter())
    attc_sum = collections.defaultdict(list)
    prev_rel = None
    prev_teams = None
    elim = []
    for r in turns:
        t = r['t']
        pl = {p['id']: p for p in r['p']}
        team_power = collections.Counter()
        for p in r['p']:
            team_power[team_of[p['id']]] += p['power']
        teams = r['teams']
        rel = r['rel']
        idx = {tm: i for i, tm in enumerate(teams)}
        # events
        for e in r.get('ev', []):
            if 'trade' in e:
                a, b = e['trade']
                sig = ' <-> '.join(sorted([side(e['ai']), side(e['bi'])]))
                trades[sig] += 1
                for it in e['ai'] + e['bi']:
                    trade_items[ITEM[it[0]] if 0 <= it[0] < len(ITEM) else str(it[0])] += 1
                per_leader[leader.get(a, a)]['trades'] += 1
                per_leader[leader.get(b, b)]['trades'] += 1
            elif 'capture' in e:
                frm, by = e['from'], e['by']
                captures[(frm, by)] += 1
                per_leader[leader.get(by, by)]['captured'] += 1
                per_leader[leader.get(frm, frm)]['lost'] += 1
                key = tuple(sorted((team_of.get(frm, -1), team_of.get(by, -1))))
                if key in open_wars:
                    open_wars[key]['captures'][team_of.get(by, -1)] += 1
            elif 'eliminated' in e:
                elim.append((t, e['eliminated']))
                per_leader[leader.get(e['eliminated'], e['eliminated'])]['eliminated'] += 1
        # relations
        if prev_rel is not None:
            pidx = {tm: i for i, tm in enumerate(prev_teams)}
            for ta in teams:
                for tb in teams:
                    if ta >= tb:
                        continue
                    now = rel[idx[ta]][idx[tb]][0] & 2
                    was = (ta in pidx and tb in pidx and prev_rel[pidx[ta]][pidx[tb]][0] & 2)
                    key = (ta, tb)
                    if now and not was:
                        wpa, wpb = rel[idx[ta]][idx[tb]][1], rel[idx[tb]][idx[ta]][1]
                        if wpa in (4, 5, 6) and wpb not in (4, 5, 6):
                            att, dfn, plan = ta, tb, wpa
                        elif wpb in (4, 5, 6) and wpa not in (4, 5, 6):
                            att, dfn, plan = tb, ta, wpb
                        else:
                            att, dfn, plan = ta, tb, max(wpa, wpb)
                        # declarer's attitude toward the target (first members)
                        ap, dp = members[att][0], members[dfn][0]
                        alive_ids = [p['id'] for p in r['p']]
                        attv = None
                        if ap in pl and dp in alive_ids:
                            v = pl[ap]['att'][alive_ids.index(dp)]
                            attv = v
                        w = dict(start=t, attacker=att, defender=dfn, plan=WARPLAN.get(plan, plan),
                                 power_ratio=round(team_power[att] / max(1, team_power[dfn]), 2),
                                 attitude=attv, captures=collections.Counter(), end=None,
                                 attacker_leader=leader.get(ap), defender_leader=leader.get(dp))
                        wars.append(w)
                        open_wars[key] = w
                        per_leader[leader.get(ap)]['declared'] += 1
                        per_leader[leader.get(dp)]['attacked'] += 1
                    elif was and not now and key in open_wars:
                        w = open_wars.pop(key)
                        w['end'] = t
                        w['success'] = (prev_rel[pidx[w['attacker']]][pidx[w['defender']]][2],
                                        prev_rel[pidx[w['defender']]][pidx[w['attacker']]][2])
        # prevalence every 10 turns
        if t % 10 == 0:
            met = ob = dp = vas = war = 0
            for i, ta in enumerate(teams):
                for j, tb in enumerate(teams):
                    if i >= j:
                        continue
                    bits = rel[i][j][0] | rel[j][i][0]
                    if bits & 1:
                        met += 1
                        ob += bool(bits & 4); dp += bool(bits & 8); vas += bool(bits & 16); war += bool(bits & 2)
            prevalence.append((t, met, ob, dp, vas, war))
        # attitude components on detail turns
        for p in r['p']:
            if 'attc' in p:
                for other, comp in p['attc'].items():
                    for k, v in enumerate(comp[:len(ATTC)]):
                        if v:
                            attc_sum[ATTC[k]].append(v)
        prev_rel, prev_teams = rel, teams
    for w in open_wars.values():
        w['end'] = None
    last = turns[-1]
    ranking = sorted(last['p'], key=lambda p: -p['score'])
    for rank, p in enumerate(ranking):
        per_leader[leader[p['id']]]['rank'] = rank + 1
        per_leader[leader[p['id']]]['cities_end'] = p['cities']
        per_leader[leader[p['id']]]['techs_end'] = p['techs']
    for w in wars:
        w['captures'] = dict((str(k), v) for k, v in w['captures'].items())
    out.update(trades=dict(trades), trade_items=dict(trade_items), wars=wars, eliminated=elim,
               prevalence=prevalence, per_leader={k: dict(v) for k, v in per_leader.items()},
               attc={k: (len(v), round(st.mean(v), 2)) for k, v in attc_sum.items()},
               turn_ms_last=last.get('ms'))
    return out


def main():
    outp, runs = sys.argv[1], sys.argv[2:]
    res = []
    for d in runs:
        try:
            res.append(analyse(d))
        except Exception as e:  # incomplete runs are reported, not fatal
            print('skip', d, e)
    json.dump(res, open(outp, 'w'), indent=1, default=str)
    for r in res:
        span = r['last'] - r['first']
        print('== %s (%s, %d players, turns %d-%d, last turn %s ms)' % (r['run'], r['speed'][10:], r['players'], r['first'], r['last'], r['turn_ms_last']))
        print('  trades %d: %s' % (sum(r['trades'].values()), ', '.join('%s x%d' % kv for kv in sorted(r['trades'].items(), key=lambda x: -x[1])[:8])))
        ws = r['wars']
        if ws:
            ended = [w for w in ws if w['end'] is not None]
            print('  wars declared %d (%.1f per 100 turns); ended %d; median duration %s; power ratio at declaration median %.2f (min %.2f, max %.2f)' % (
                len(ws), 100.0 * len(ws) / max(1, span), len(ended),
                st.median([w['end'] - w['start'] for w in ended]) if ended else '-',
                st.median([w['power_ratio'] for w in ws]), min(w['power_ratio'] for w in ws), max(w['power_ratio'] for w in ws)))
            att = [w['attitude'] for w in ws if w['attitude'] is not None]
            if att:
                print('  declarer attitude toward target at declaration: median %s, range %s..%s' % (st.median(att), min(att), max(att)))
            caps = sum(sum(w['captures'].values()) for w in ws)
            print('  cities captured during these wars: %d; eliminations %d' % (caps, len(r['eliminated'])))
        else:
            print('  no wars')
        if r['prevalence']:
            t, met, ob, dp, vas, war = r['prevalence'][-1]
            print('  at turn %d: met pairs %d, open borders %d, defensive pacts %d, vassals %d, at war %d' % (t, met, ob, dp, vas, war))


if __name__ == '__main__':
    main()
