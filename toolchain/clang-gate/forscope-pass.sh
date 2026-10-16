#!/bin/bash
# usage: forscope-pass.sh <mirror-dir> -- emulate MSVC 7.1 legacy for-scope (two rounds)
HERE=$(dirname "$(readlink -f "$0")")
m=$1; tmp=$(mktemp -d)
for round in 1 2; do
  (cd "$m" && grep -l "for *( *int" *.cpp | xargs -P 8 -I{} sh -c "CASEDIR=$m '$HERE/check.sh' $m {} > $tmp/{}.log 2>&1 || true")
  python3 "$HERE/forscope.py" "$m" $tmp/*.log
  rm -f $tmp/*.log
done
rm -rf $tmp
