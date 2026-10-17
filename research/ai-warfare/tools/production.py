#!/usr/bin/env python3
"""Units against buildings completed in the capital and elsewhere, human against AI.

usage: production.py <registry.fig.json> <game.duckdb>:<human id> ...
       (run with ~/.cache/rom-ana/bin/python; databases with a save dump)

Completions: U lines (units) and N lines (buildings) of every player, by the city they came from.
Capital: the city holding BUILDING_PALACE in the save dump, so a capital moved during the game
is counted at its last place. Shares are of the completions in that group of cities.
"""
import os, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

REG, specs = sys.argv[1], sys.argv[2:]
reg = Registry(REG, [s.split(':')[0] for s in specs])
for spec in specs:
    db, h = spec.split(':'); h = int(h); g = os.path.basename(db).split('.')[0]
    con = duckdb.connect(db, read_only=True)
    rows = con.execute(f"""
      with cap as (select player, x, y from city_buildings where building = 'BUILDING_PALACE'),
           c as (select player, x, y, 'unit' k from wl_U union all select player, x, y, 'building' from wl_N),
           j as (select c.player, c.k, case when cap.x is not null then 'capital' else 'other' end place
                 from c left join cap on cap.player = c.player and cap.x = c.x and cap.y = c.y
                 where c.player in (select player from cap))
      select case when player = {h} then 'human' else 'ai' end who, place,
             sum(case when k = 'unit' then 1 else 0 end) units, count(*) n
      from j group by 1, 2 order by 1 desc, 2""").fetchall()
    t = con.execute('select min(turn), max(turn) from wl_U').fetchone()
    for who, place, units, n in rows:
        reg.fig(f'{g}_{who}_{place}_unit_share', round(units / n, 3), 'share', who, f'{t[0]}-{t[1]}',
                'wl_U and wl_N completions; capital = BUILDING_PALACE at the save', n=n)
        reg.fig(f'{g}_{who}_{place}_n', n, 'units built', who, f'{t[0]}-{t[1]}', 'wl_U plus wl_N rows (completions)')
    print(g, rows, file=sys.stderr)
reg.save()
