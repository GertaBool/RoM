#!/bin/bash
# usage: forscope-pass.sh <mirror-dir> -- apply legacy for-scope emulation (two rounds)
m=$1; tmp=$(mktemp -d)
for round in 1 2; do
  (cd "$m" && grep -l "for *( *int" *.cpp | xargs -P 8 -I{} sh -c "CASEDIR=$m /home/user/src/shim/check.sh $m {} > $tmp/{}.log 2>&1 || true")
  python3 /home/user/src/shim/forscope.py "$m" $tmp/*.log
  rm -f $tmp/*.log
done
rm -rf $tmp
