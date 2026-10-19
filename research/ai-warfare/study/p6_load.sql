-- Loads the P6 harness runs into DuckDB (study/queries_p6.json): replace CAMP with the campaign directory
-- (CAMP/<arm>/s<seed>/run.jsonl and run.log), SEAT with the human-model seat; run with
-- duckdb.connect(<p6.duckdb>).execute(<this text>). One row per run.
create or replace table lines as
  select regexp_extract(filename, '/([ab])/s([0-9]+)/run.jsonl$', 1) arm, cast(regexp_extract(filename, '/([ab])/s([0-9]+)/run.jsonl$', 2) as bigint) seed, json j
  from read_json_objects('CAMP/*/s*/run.jsonl', format='newline_delimited', filename=true)
  where json_extract(json, '$.t') is not null;
create or replace table ev as
  select arm, seed, cast(json_extract(j, '$.t') as int) turn, unnest(from_json(json_extract(j, '$.ev'), '["JSON"]')) e from lines;
create or replace table runs as
  select r.arm, r.seed,
    (select count(*) from ev where ev.arm=r.arm and ev.seed=r.seed and json_extract(e, '$.capture') is not null and cast(json_extract(e, '$.by') as int)=SEAT) as taken,
    (select count(*) from ev where ev.arm=r.arm and ev.seed=r.seed and json_extract(e, '$.capture') is not null and cast(json_extract(e, '$.from') as int)=SEAT) as lost,
    (select count(*) from ev where ev.arm=r.arm and ev.seed=r.seed and json_extract(e, '$.war') is not null and cast(json_extract(e, '$.war[1]') as int)=SEAT) as wars_on_seat,
    (select count(*) from ev where ev.arm=r.arm and ev.seed=r.seed and json_extract(e, '$.war') is not null and cast(json_extract(e, '$.war[0]') as int)=SEAT) as wars_by_seat,
    (select count(*) from ev where ev.arm=r.arm and ev.seed=r.seed and json_extract(e, '$.war') is not null and cast(json_extract(e, '$.war[0]') as int)<>SEAT and cast(json_extract(e, '$.war[1]') as int)<>SEAT) as ai_ai_wars,
    (select max(cast(json_extract(j, '$.t') as int)) from lines l where l.arm=r.arm and l.seed=r.seed) as last_turn,
    (select sum(cast(json_extract(j, '$.ms') as bigint)) from lines l where l.arm=r.arm and l.seed=r.seed) / 1000.0 as run_seconds
  from (select distinct arm, seed from lines) r;
create or replace table pw as
  select arm, seed, t as turn, cast(json_extract(x, '$.id') as int) as id, cast(json_extract(x, '$.power') as int) as power,
    cast(json_extract(x, '$.cities') as int) as cities
  from (select arm, seed, cast(json_extract(j, '$.t') as int) as t, unnest(from_json(json_extract(j, '$.p'), '["JSON"]')) as x from lines);
create or replace table turns as
  select arm, seed, turn, sum(power) as total_power, max(power) as top_power, arg_max(id, power) as top_id,
    max(case when id=SEAT then power end) as seat_power
  from pw where cities>0 group by arm, seed, turn;
create or replace table wars as
  select arm, seed, turn, cast(json_extract(e, '$.war[0]') as int) as by_team, cast(json_extract(e, '$.war[1]') as int) as on_team,
    cast(json_extract(e, '$.pow[0]') as int) as by_power, cast(json_extract(e, '$.pow[1]') as int) as on_power,
    cast(json_extract(e, '$.plan') as int) as plan
  from ev where json_extract(e, '$.war') is not null;
drop table pw;
drop table lines;
