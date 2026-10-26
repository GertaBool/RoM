#!/bin/bash
# run.sh <root name> <out dir> <seed>: one 150-turn GAMESPEED_NORMAL, HANDICAP_NOBLE game of
# PrivateMaps/Mediterranean, Standard (all AI) in a throwaway copy of the game folder; keeps run.log, run.jsonl.
source "$(dirname "$0")/env.sh"
root=$1; out=$2; seed=$3
tmp=$S/exp/roots/$(basename "$(dirname "$out")")-$(basename "$out")-$$; rm -rf "$tmp" "$out"; mkdir -p "$tmp" "$out"
cp -a "$S/hw/$root/." "$tmp/"; rm -rf "$tmp/logs"; mkdir "$tmp/logs"
cp "$S/hw/medstd.scn" "$tmp/"
cd "$tmp"
timeout 3000 wine harness.exe scenario medstd.scn GAMESPEED_NORMAL HANDICAP_NOBLE "$seed" 150 run.jsonl 10 > run.log 2>&1
echo "exit $?" >> run.log
mv run.log run.jsonl "$out/"
cd / && rm -rf "$tmp"
