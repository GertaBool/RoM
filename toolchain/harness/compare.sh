#!/bin/bash
# Run every scenario against each harness DLL build and summarize.
# usage: [MODE=plain] compare.sh <turns> <mod checkout> <name>=<build dir> ...
# Each build gets a game folder $WORK/root-<name> with run-*.log and bbai-*.log.
turns=$1; mod=$2; shift 2
source "$(dirname "$0")/env.sh"
for spec in "$@"; do
  name=${spec%%=*}; dir=${spec#*=}
  root=$WORK/root-$name
  "$H/mkroot.sh" "$root" "$dir" "$mod"
  for sc in islands mid far; do
    (cd "$root" && timeout 1800 wine harness.exe $sc $turns $MODE > run-$sc.log 2>&1; cp logs/BBAI.log bbai-$sc.log 2>/dev/null)
    res=$(grep RESULT "$root/run-$sc.log" || echo "RESULT missing (crash?)")
    first=$(grep -m1 "founds new city.* at" "$root/bbai-$sc.log" | grep -v "at 10, 7" | sed 's/.*founds new city //')
    stall=$(grep -c "MISSING_ESCORT_OR_CAPACITY" "$root/bbai-$sc.log")
    printf "%-6s %-8s %s | missing-escort waits: %s | %s\n" "$name" "$sc" "$res" "$stall" "${first:-no overseas city}"
  done
done
