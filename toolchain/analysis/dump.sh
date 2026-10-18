#!/bin/bash
# Dump one save with the full state (HARNESS_HISTORY_DIAG) and no turns played.
# usage: dump.sh <save dir> <out dir> <human player> [harness DLL] [turns, default 0]
#   <save dir>: harness.exe, <name>.init, <name>.game and the game folders (see seeds.sh).
#   The out dir is a hard-linked copy with its own logs/ and, if given, its own DLL.
# Writes <out dir>/run.jsonl.state0.json (and, after the turns played, run.jsonl.state1.json; every seat, the human's
# included, played by the AI), and probe.json: the human seat's counterfactual civics and the AIs' tech values. Needs WINEPREFIX (toolchain env.sh).
set -e
SAVE=$(cd "$1" && pwd); OUT=$2; HUMAN=$3; DLL=$4; TURNS=${5:-0}
NAME=$(basename "$(ls "$SAVE"/*.init | head -1)" .init)
rm -rf "$OUT"; mkdir -p "$(dirname "$OUT")"; cp -al "$SAVE" "$OUT"
rm -f "$OUT"/run.jsonl* "$OUT"/run.log "$OUT"/oracle.jsonl; rm -rf "$OUT/logs"; mkdir "$OUT/logs"
if [ -n "$DLL" ]; then rm -f "$OUT/CvGameCoreDLL.dll"; cp "$DLL" "$OUT/CvGameCoreDLL.dll"; fi
cd "$OUT" && HARNESS_HISTORY_DIAG=1 HARNESS_HUMAN=$HUMAN HARNESS_PROBE=probe.json timeout $((1800 + 300 * TURNS)) wine harness.exe save "$NAME.init" "$NAME.game" $TURNS run.jsonl 5 20000 < /dev/null > run.log 2>&1
ls -la "$OUT/run.jsonl.state0.json"
