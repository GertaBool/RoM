#!/usr/bin/env python3
"""Declared SQL queries over extract.py databases, as figure tables (tools/figlib.py).

usage: sqlfig.py <spec.json> <registry.fig.json> [records=<records.json>] <name>=<game.duckdb> ...
       run with ~/.cache/rom-ana/bin/python

The spec is a list of queries: {"id", "db" (a name given on the command line, or "*" for every
one, or for those listed in "dbs": the id is then prefixed with the name), "sql", "unit", "who", "turn", "source",
and "xml": [record type, column or list of columns] when columns list game types: their records are then stored and docs.py
requires their effects (needs records=)}. Each result
becomes one table figure; its rows are exactly what the query returns, so a GROUP BY lists every
category present; its ORDER BY must be total (ties broken by every column shown), and queries run
on one thread, so the same database gives the same rows in the same order. Values are printed as returned (floats rounded to 3 places). A query that
returns no rows is an error, so an empty result is never shown as a finding.
"""
import json, os, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry, FigureError

SPEC, REG = sys.argv[1], sys.argv[2]
dbs = dict(a.split('=', 1) for a in sys.argv[3:])
rec = dbs.pop('records', None)
spec = json.load(open(SPEC))
reg = Registry(REG, [SPEC] + list(dbs.values()) + ([rec] if rec else []), json.load(open(rec)) if rec else None)
cons = {k: duckdb.connect(v, read_only=True) for k, v in dbs.items()}
for c in cons.values(): c.execute('set threads = 1')   # tie order must not depend on thread scheduling
fmt = lambda v: round(v, 3) if isinstance(v, float) else ('' if v is None else v)
for q in spec:
    names = [n for n in dbs if n in q['dbs']] if q.get('dbs') else list(dbs)
    for name in (names if q['db'] == '*' else [q['db']]):
        r = cons[name].execute(q['sql'])
        head = [d[0] for d in r.description]
        rows = [[fmt(v) for v in row] for row in r.fetchall()]
        if not rows: raise FigureError(f"{q['id']} ({name}): no rows")
        fid = f"{name}_{q['id']}" if q['db'] == '*' else q['id']
        xt, xc = q.get('xml', (None, None))
        reg.result_table(fid, head, rows, q['unit'], q['who'], q['turn'], f"{q['source']} [{name}]", [r[0] for r in rows],
                         n=sum(1 for _ in rows), xml=xt, xml_vals=[r[head.index(c)] for r in rows for c in ([xc] if isinstance(xc, str) else xc)] if xt else None)
        print(f'{fid}: {len(rows)} rows', file=sys.stderr)
reg.save()
