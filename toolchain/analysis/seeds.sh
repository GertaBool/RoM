#!/bin/bash
# Seeded continuations of one save, in parallel (framework.md, section 7).
# usage: seeds.sh <save dir> <out dir> <turns> <first seed> <last seed> [jobs=4]
#   <save dir> holds harness.exe, CvGameCoreDLL.dll, <name>.init, <name>.game and the game folders.
# Each seed runs in <out dir>/s<seed>, a hard-linked copy (no extra disk for the inputs), with
# HARNESS_RESEED=<seed>, HARNESS_ORACLE=oracle.jsonl and HARNESS_HISTORY_DIAG=1; extra HARNESS_*
# variables in the environment are passed through. Needs WINEPREFIX (toolchain env.sh).
set -e
SAVE=$(cd "$1" && pwd); OUT=$2; TURNS=$3; A=$4; B=$5; J=${6:-4}
NAME=$(basename "$(ls "$SAVE"/*.init | head -1)" .init)
mkdir -p "$OUT"
run() {
  d="$OUT/s$1"; rm -rf "$d"; cp -al "$SAVE" "$d"; rm -f "$d"/run.jsonl* "$d"/run.log "$d"/oracle.jsonl
  rm -rf "$d/logs"; mkdir "$d/logs"   # the harness writes its logs here: never into the linked template
  cd "$d" && HARNESS_RESEED=$1 HARNESS_ORACLE=oracle.jsonl HARNESS_HISTORY_DIAG=1 \
    timeout 3600 wine harness.exe save "$NAME.init" "$NAME.game" "$TURNS" run.jsonl 5 20000 < /dev/null > run.log 2>&1
  echo "seed $1: $(grep -c '^turn ' run.log) turn lines, $(wc -l < oracle.jsonl) oracle records"
}
export -f run; export OUT TURNS SAVE NAME
# xargs, not GNU parallel: Wine aborts (free(): invalid pointer) in the environment parallel sets up.
seq "$A" "$B" | xargs -P "$J" -I{} bash -c 'run {}'
