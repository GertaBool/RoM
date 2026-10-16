#!/bin/bash
# usage: memsample.sh <root> : every 15 s, append "epoch turn VmSize_kB VmRSS_kB VmData_kB" for the harness.exe running in <root>
root=$(readlink -f "$1")
out="$root/mem.tsv"
sleep 20
while :; do
  pid=""
  for p in $(pgrep -f 'harness.exe'); do
    [ "$(readlink /proc/$p/cwd 2>/dev/null)" = "$root" ] && grep -q '^Name:.*harness' /proc/$p/status 2>/dev/null && pid=$p && break
  done
  [ -z "$pid" ] && break
  t=$(tail -n 1 "$root/run.jsonl" 2>/dev/null | cut -c1-16 | grep -o '"t":[0-9]*' | cut -d: -f2)
  awk -v e="$(date +%s)" -v t="$t" '/^VmSize/{s=$2} /^VmRSS/{r=$2} /^VmData/{d=$2} END{print e, t, s, r, d}' /proc/$pid/status >> "$out"
  sleep 15
done
