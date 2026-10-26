#!/bin/bash
# batch.sh <P> <root a> <root b> [jobs]: the 5 seeds of prediction P (ledger.py seeds) on both arms, run in
# parallel with xargs (not GNU parallel: the harness aborts under it), then collected into
# method/mission/evidence/<P>/<arm>.tsv with ledger.py collect (seat 0).
set -e
source "$(dirname "$0")/env.sh"
P=$1; ra=$2; rb=$3; jobs=${4:-3}
seeds=$(python3 "$REPO/method/ledger.py" seeds "$P" 5)
for s in $seeds; do echo "$ra $S/exp/$P/a/s$s $s"; echo "$rb $S/exp/$P/b/s$s $s"; done |
  xargs -P "$jobs" -L 1 "$(dirname "$0")/run.sh"
for arm in a b; do
  python3 "$REPO/method/ledger.py" collect "$P" $arm 0 $(for s in $seeds; do echo "$S/exp/$P/$arm/s$s"; done)
done
cat "$REPO/method/mission/evidence/$P/"*.tsv
