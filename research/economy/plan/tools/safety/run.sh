#!/bin/bash
# run.sh <root name> <out dir> <seed>: one 150-turn GAMESPEED_NORMAL, HANDICAP_NOBLE game of
# PrivateMaps/Mediterranean, Standard (all AI; or the game folder's map.scn) in a throwaway copy of the game folder; keeps run.log, run.jsonl.
source "$(dirname "$0")/env.sh"
root=$1; out=$2; seed=$3
tmp=$S/exp/roots/$(basename "$(dirname "$out")")-$(basename "$out")-$$; rm -rf "$tmp" "$out"; mkdir -p "$tmp" "$out"
cp -a "$S/hw/$root/." "$tmp/"; rm -rf "$tmp/logs"; mkdir "$tmp/logs"
# the scenario: the game folder's own map.scn when it has one (an arm that differs by scenario), else medstd.scn
if [ -f "$S/hw/$root/map.scn" ]; then cp "$S/hw/$root/map.scn" "$tmp/medstd.scn"; else cp "$S/hw/medstd.scn" "$tmp/"; fi
cd "$tmp"
timeout 3000 wine harness.exe scenario medstd.scn GAMESPEED_NORMAL HANDICAP_NOBLE "$seed" 150 run.jsonl 10 > run.log 2>&1
echo "exit $?" >> run.log
mv run.log run.jsonl "$out/"
cd / && rm -rf "$tmp"
