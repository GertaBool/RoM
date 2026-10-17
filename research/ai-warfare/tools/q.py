#!/usr/bin/env python3
"""Exact SQL over one game's tables (DuckDB), printed compactly.

usage: q.py <game dir> "<sql>" [--limit 40]

Every CSV in the folder is a view named after its file (tiles, wars, battles, ...). The human's
commands are also split into a view `cmd`: turn, kind, unit, x, y, size, what, data (field 0-5 of
the A line's fields; `what` is the mission or command name). Output is the result and its row
count. For exploration only: figures that go into a document are produced through figlib.
"""
import os, sys

import duckdb

G, sql = sys.argv[1], sys.argv[2]
lim = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else 40
con = duckdb.connect()
for f in sorted(os.listdir(G)):
    if f.endswith('.csv'):
        con.execute(f"create view {f[:-4]} as select * from read_csv_auto('{os.path.join(G, f)}', all_varchar=false)")
if os.path.exists(os.path.join(G, 'human_commands.csv')):
    con.execute("""create view cmd as select turn, kind,
        split_part(fields, '|', 1) as unit, try_cast(split_part(fields, '|', 2) as int) as x,
        try_cast(split_part(fields, '|', 3) as int) as y, split_part(fields, '|', 4) as size,
        split_part(fields, '|', 5) as what, split_part(fields, '|', 6) as data from human_commands""")
r = con.execute(sql)
cols = [d[0] for d in r.description]
rows = r.fetchall()
print(' | '.join(cols))
for row in rows[:lim]: print(' | '.join('' if v is None else str(v) for v in row))
print(f'({len(rows)} rows{"" if len(rows) <= lim else f", {lim} shown"})')
