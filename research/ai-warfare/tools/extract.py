#!/usr/bin/env python3
"""Every field of one game's sources into one DuckDB database, with a conservation check.

usage: extract.py <WarLog.log> <out.duckdb> [--state state0.json] [--oracle oracle.jsonl] [--manifest extract.json]

War log: one table per line type, with `seq` (the line's position in the log, so "known before
a decision" is `seq <` the decision's seq), columns named after the format strings in the DLL
(CvGameCoreUtils.cpp, warLog*), all fields kept. A lines keep kind and all fields (a1..a12);
D lines are also exploded into deal_items (side 1 = first player gives, 2 = second gives).
Save dump (HARNESS_HISTORY_DIAG): players, econ, costs, hist (long: player, series, turn, k,
value), units (every unit), cities, tiles (with their city-plot order), civic_values, created,
replay, progress. Oracle (HARNESS_ORACLE, turns played after the save): one table per record kind
(oracle_after, oracle_before, oracle_atk), scalar fields as columns, lists kept as JSON text.

Running check (framework.md, section 3): the rows of each war-log table equal the lines of its
type, and their sum equals the non-empty lines read; each dump table equals its source count.
The manifest records these counts and the input hashes. Run with ~/.cache/rom-ana/bin/python.
"""
import argparse, collections, csv, hashlib, json, os, re, sys, tempfile

import duckdb

# field names after the line type, from the DLL's format strings
WL = {
    'H': 'turn speed handicap width height',
    'P': 'player team civ leader human',
    'T': 'turn year',
    'W': 'turn team target warplan', 'Q': 'turn team target warplan',
    'C': 'turn att att_unit att_hp att_xp def def_unit def_hp def_xp x y terrain feature hills city_def odds plot_units',
    'R': 'turn winner winner_unit winner_hp loser loser_unit',
    'S': 'turn att att_unit def def_unit damage x y',
    'B': 'turn player unit x y def_before def_after',
    'K': 'turn old_owner new_owner x y pop', 'Z': 'turn old_owner new_owner x y pop',
    'G': 'turn player x y military head_ai mission_ai target_x target_y units',
    'U': 'turn player unit x y',
    'N': 'turn player building x y',
    'Y': 'turn player x y pop hammers orders stored needed defenders best_defender def_mod danger foreign',
    'M': 'turn player cities pop land food hammers commerce research gold_rate gold military power score slider golden',
    'V': 'turn player unit x y action',
    'X': 'turn player tech',
    'D': 'turn first second items_first items_second',
    'E': 'turn sender receiver event data1 data2',
}
A_MAX = 12


def num(v):
    try: return int(v)
    except ValueError: return v


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('log'); ap.add_argument('db')
    ap.add_argument('--state'); ap.add_argument('--manifest'); ap.add_argument('--oracle')
    a = ap.parse_args()
    rows = collections.defaultdict(list)
    seen = collections.Counter(); other = 0; total = 0
    for raw in open(a.log, encoding='latin-1'):
        line = re.sub(r'^\[[^\]]*\]\s*', '', raw.rstrip('\r\n'))
        if not line.strip(): continue
        total += 1
        f = line.split('\t')
        t = f[0]
        seen[t] += 1
        if t == 'A':
            rows['A'].append([total, num(f[1]), num(f[2]), f[3]] + (f[4:] + [None] * A_MAX)[:A_MAX])
        elif t in WL:
            n = len(WL[t].split())
            vals = [num(x) for x in f[1:]]
            if t == 'D' and len(vals) == n - 1: vals.append('')
            if len(vals) != n: raise SystemExit(f'{t}: {len(vals)} fields, expected {n}: {line[:120]}')
            rows[t].append([total] + vals)
        else:
            other += 1
    if os.path.exists(a.db): os.remove(a.db)
    con = duckdb.connect(a.db)
    counts = {}

    def table(name, cols, data):
        con.execute(f'create table {name} ({", ".join(f"\"{c}\" {typ}" for c, typ in cols)})')
        if data:  # bulk load through a temporary CSV: one COPY instead of a statement per row
            with tempfile.NamedTemporaryFile('w', suffix='.csv', newline='', delete=False) as tf:
                w = csv.writer(tf)
                for r in data: w.writerow(['\\N' if v is None else v for v in r])
            con.execute(f"copy {name} from '{tf.name}' (format csv, header false, nullstr '\\N')")
            os.remove(tf.name)
        counts[name] = con.execute(f'select count(*) from {name}').fetchone()[0]

    # text fields of the format strings (%s); every other field is %d. An empty table gets these
    # types too, so queries that compare numbers work on games without that line type.
    TEXT = set('speed handicap civ leader att_unit def_unit terrain feature winner_unit loser_unit unit building '
               'orders best_defender head_ai units action tech items_first items_second'.split())

    def cols_of(data, names):
        out = []
        for i, c in enumerate(names):
            vs = [r[i] for r in data if r[i] is not None and r[i] != '']
            num_ok = all(isinstance(v, int) for v in vs) and c not in TEXT
            out.append((c, 'BIGINT' if num_ok else 'VARCHAR'))
        return out

    for t, spec in WL.items():
        names = ['seq'] + spec.split()
        data = [[None if v == '' else v for v in r] if t != 'D' else r for r in rows[t]]
        data = [[v if (isinstance(v, int) or v is None) else str(v) for v in r] for r in data]
        cl = cols_of(data, names)
        data = [[(str(v) if typ == 'VARCHAR' and v is not None else v) for v, (_, typ) in zip(r, cl)] for r in data]
        table('wl_' + t, cl, data)
    acols = [('seq', 'BIGINT'), ('turn', 'BIGINT'), ('player', 'BIGINT'), ('kind', 'VARCHAR')] + [(f'a{i + 1}', 'VARCHAR') for i in range(A_MAX)]
    table('wl_A', acols, [r[:4] + [None if v is None else str(v) for v in r[4:]] for r in rows['A']])
    di = []
    for r in rows['D']:
        for side, items in ((1, r[4]), (2, r[5])):
            for it in str(items).split(','):
                if ':' in it:
                    k, v = it.split(':'); di.append([r[0], r[1], r[2], r[3], side, int(k), int(v)])
    table('deal_items', [('seq', 'BIGINT'), ('turn', 'BIGINT'), ('first', 'BIGINT'), ('second', 'BIGINT'), ('side', 'BIGINT'),
                         ('item', 'BIGINT'), ('data', 'BIGINT')], di)
    errs = [f'wl_{t}: {counts["wl_" + t]} rows, {seen[t]} lines' for t in list(WL) + ['A'] if counts['wl_' + t] != seen[t]]
    if sum(counts['wl_' + t] for t in list(WL) + ['A']) + other != total: errs.append('war-log rows do not sum to the lines read')
    src = {'log_lines': total, 'log_unknown_type': other, 'log_types': dict(seen)}

    if a.state:
        d = json.load(open(a.state))
        P = d['players']
        table('players', [('player', 'BIGINT'), ('leader', 'VARCHAR'), ('human', 'BIGINT'), ('gold', 'BIGINT'),
                          ('gold_rate', 'BIGINT'), ('research_rate', 'BIGINT'), ('culture_rate', 'BIGINT'),
                          ('research', 'VARCHAR'), ('era', 'BIGINT'), ('vic', 'BIGINT'), ('agenda', 'BIGINT')],
              [[p['id'], p['leader'], int(bool(p['human'])), p['gold'], p['goldRate'], p['researchRate'], p['cultureRate'],
                str(p['research']), p['era'], p['vic'], p['agenda']] for p in P])
        ek = [k for k, v in P[0]['econ'].items() if not isinstance(v, list)]
        table('econ', [('player', 'BIGINT')] + [(k, 'BIGINT') for k in ek], [[p['id']] + [p['econ'][k] for k in ek] for p in P])
        table('econ_pct', [('player', 'BIGINT'), ('kind', 'VARCHAR'), ('commerce', 'BIGINT'), ('value', 'BIGINT')],
              [[p['id'], kind, i, v] for p in P for kind in ('pct', 'flex') for i, v in enumerate(p['econ'][kind])])
        ck = list(P[0]['costs'])
        table('costs', [('player', 'BIGINT')] + [(k, 'BIGINT') for k in ck], [[p['id']] + [p['costs'][k] for k in ck] for p in P])
        vec = lambda x: x if isinstance(x, list) else [x]
        h = [[p['id'], s, t, k, v] for p in P for s, ser in p['hist'].items() for t, x in enumerate(ser) for k, v in enumerate(vec(x))]
        table('hist', [('player', 'BIGINT'), ('series', 'VARCHAR'), ('turn', 'BIGINT'), ('k', 'BIGINT'), ('value', 'BIGINT')], h)
        ucols = 'unit ai xp level can_fight x y area age group_size mission_ai plot_owner cargo'.split()
        table('units', [('player', 'BIGINT')] + [(c, 'VARCHAR' if c in ('unit', 'ai') else 'BIGINT') for c in ucols],
              [[p['id']] + u for p in P for u in p['unitList']])
        table('cities', [('player', 'BIGINT'), ('x', 'BIGINT'), ('y', 'BIGINT'), ('pop', 'BIGINT'), ('founded', 'BIGINT'),
                         ('food', 'BIGINT'), ('prod', 'BIGINT'), ('commerce', 'BIGINT'), ('culture', 'BIGINT'),
                         ('happy', 'BIGINT'), ('unhappy', 'BIGINT'), ('good', 'BIGINT'), ('bad', 'BIGINT'), ('spec', 'BIGINT'),
                         ('improved', 'BIGINT'), ('radius', 'BIGINT'), ('order', 'VARCHAR'), ('order_turns', 'BIGINT'),
                         ('buildings', 'BIGINT')],
              [[p['id'], c['x'], c['y'], c['pop'], c['founded'], c['food'], c['prod'], c['commerce'], c.get('culture'),
                c.get('happy'), c.get('unhappy'), c.get('good'), c.get('bad'), c['spec'], c['improved'], c['radius'],
                str(c['order']), c.get('orderTurns'), len(c['buildings'])] for p in P for c in p['cities']])
        table('city_buildings', [('player', 'BIGINT'), ('x', 'BIGINT'), ('y', 'BIGINT'), ('building', 'VARCHAR')],
              [[p['id'], c['x'], c['y'], str(b)] for p in P for c in p['cities'] for b in c['buildings']])
        tcols = 'worked terrain feature improvement hills river bonus food hammers commerce'.split()
        table('tiles', [('player', 'BIGINT'), ('city_x', 'BIGINT'), ('city_y', 'BIGINT'), ('seq', 'BIGINT')] +
              [(c, 'VARCHAR' if c in ('terrain', 'feature', 'improvement', 'bonus') else 'BIGINT') for c in tcols],
              [[p['id'], c['x'], c['y'], i] + t for p in P for c in p['cities'] for i, t in enumerate(c.get('tiles', []))])
        table('civic_values', [('player', 'BIGINT'), ('civic', 'VARCHAR'), ('option', 'VARCHAR'), ('score', 'BIGINT')],
              [[p['id']] + list(cv[:3]) for p in P for cv in p.get('civicValues', [])])
        table('civics', [('player', 'BIGINT'), ('civic', 'VARCHAR')], [[p['id'], c] for p in P for c in p['civics']])
        table('techs', [('player', 'BIGINT'), ('tech', 'VARCHAR')], [[p['id'], str(t)] for p in P for t in p['techs']])
        table('created', [('unit', 'VARCHAR'), ('n', 'BIGINT')], [[k, v] for k, v in d.get('created', {}).items()])
        table('replay', [('turn', 'BIGINT'), ('player', 'BIGINT'), ('type', 'BIGINT'), ('text', 'VARCHAR')],
              [list(r[:3]) + [str(r[3])] for r in d.get('replay', [])])
        want = {'players': len(P), 'units': sum(len(p['unitList']) for p in P), 'cities': sum(len(p['cities']) for p in P),
                'tiles': sum(len(c.get('tiles', [])) for p in P for c in p['cities']), 'replay': len(d.get('replay', [])),
                'hist': sum(len(vec(x)) for p in P for ser in p['hist'].values() for x in ser)}
        errs += [f'{k}: {counts[k]} rows, {v} in the dump' for k, v in want.items() if counts[k] != v]
        src['state_turn'] = d['turn']
    if a.oracle:
        recs = collections.defaultdict(list)
        for l in open(a.oracle):
            if l.strip(): r = json.loads(l); recs[r['o']].append(r)
        for kind, rs in recs.items():
            keys = sorted({k for r in rs for k in r if k != 'o'})
            typ = {k: ('DOUBLE' if all(isinstance(r.get(k), (int, float)) or r.get(k) is None for r in rs) else 'VARCHAR') for k in keys}
            table('oracle_' + kind, [(k, typ[k]) for k in keys],
                  [[(json.dumps(r.get(k)) if typ[k] == 'VARCHAR' and r.get(k) is not None else r.get(k)) for k in keys] for r in rs])
            if counts['oracle_' + kind] != len(rs): errs.append(f'oracle_{kind}: {counts["oracle_" + kind]} rows, {len(rs)} records')
        src['oracle_records'] = {k: len(v) for k, v in recs.items()}
    con.close()
    man = {'inputs': {os.path.basename(p): sha(p) for p in (a.log, a.state, a.oracle) if p},
           'source': src, 'tables': counts, 'errors': errs}
    if a.manifest: json.dump(man, open(a.manifest, 'w'), indent=1, sort_keys=True)
    print(f'{len(counts)} tables, {sum(counts.values())} rows; {total} log lines; errors: {len(errs)}', file=sys.stderr)
    for e in errs: print(e, file=sys.stderr)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
