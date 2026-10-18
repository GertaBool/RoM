#!/bin/bash
# Rebuild every derived table and figure of the study, in dependency order, then render and check.
# usage: rebuild.sh [data dir = ~/.cache/rom-ana/data]
#   data dir: records.json, CvEnums.h, and per game gameN/{WarLog.log, human, [state0.json, probe.json, t1.json, t10.json]}
#   (t1/t10: the state after a harness continuation of 1 and 10 turns from the save, dump.sh with turns)
#   (state0.json from toolchain/analysis/dump.sh). Databases go to ~/.cache/rom-ana/db.
set -e
D=${1:-$HOME/.cache/rom-ana/data}; DB=$HOME/.cache/rom-ana/db; mkdir -p "$DB"
R=$(cd "$(dirname "$0")/../.." && pwd)/research/ai-warfare; T=$R/tools; PY=$HOME/.cache/rom-ana/bin/python
games=$(cd "$D" && ls -d game* | sort)
for g in $games; do
  st=(); [ -e "$D/$g/state0.json" ] && st=(--state "$D/$g/state0.json")
  [ -e "$D/$g/probe.json" ] && st+=(--probe "$D/$g/probe.json")
  for l in t1 t10; do [ -e "$D/$g/$l.json" ] && st+=(--later "$l=$D/$g/$l.json"); done
  $PY "$T/extract.py" "$D/$g/WarLog.log" "$DB/$g.duckdb" "${st[@]}" --records "$D/records.json" --enums "$D/CvEnums.h" --manifest "$R/games/$g/extract.json"
  $PY "$T/cases.py" "$DB/$g.duckdb" "$(cat "$D/$g/human")" "$R/games/$g" "$R/games/$g/cases.fig.json"
done
with_state=$(for g in $games; do [ -e "$D/$g/state0.json" ] && echo $g; done)
for c in slider_turn slider_dir upgrade_turn; do $PY "$T/models.py" $c "$R/study/$c.fig.json" "$R/games" $with_state; done
$PY "$T/models.py" order_unit "$R/study/order_unit.fig.json" "$R/games" $games
$PY "$T/production.py" "$R/study/production.fig.json" $(for g in $with_state; do echo "$DB/$g.duckdb:$(cat "$D/$g/human")"; done)
$PY "$T/sqlfig.py" "$R/study/queries.json" "$R/study/data.fig.json" $(for g in $with_state; do echo "$g=$DB/$g.duckdb"; done)
$PY "$T/sqlfig.py" "$R/study/queries_win.json" "$R/study/win.fig.json" records="$D/records.json" $(for g in $games; do echo "$g=$DB/$g.duckdb"; done)
$PY "$T/sqlfig.py" "$R/study/queries_ops.json" "$R/study/ops.fig.json" records="$D/records.json" $(for g in $games; do echo "$g=$DB/$g.duckdb"; done)
$PY "$T/sqlfig.py" "$R/study/queries_style.json" "$R/study/style.fig.json" records="$D/records.json" $(for g in $games; do echo "$g=$DB/$g.duckdb"; done)
$PY "$T/phases.py" "$R/study/phases.fig.json" $(for g in $games; do echo "$DB/$g.duckdb"; done)
$PY "$T/strategy.py" "$R/study/targets.fig.json" $(for g in $with_state; do echo "$DB/$g.duckdb"; done)
$PY "$T/tileyield.py" "$R/study/yields.fig.json" "$D/records.json" $(for g in $with_state; do echo "$DB/$g.duckdb"; done)
$PY "$T/growth.py" "$R/study/growth.fig.json" "$D/records.json" $(for g in $with_state; do echo "$DB/$g.duckdb"; done)
python3 "$T/check_all.py" --render
