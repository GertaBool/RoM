#!/bin/sh
# The whole study in order. $1: the mod checkout (GitLab main 3bec049); $2...: the harness run folders (s<seed>).
set -e
cd "$(dirname "$0")/.."
MOD=$1; shift
python3 ../tools/extract.py "$MOD" "$MOD/PrivateMaps/Mediterranean, Standard.CivBeyondSwordWBSave" data/map && mv data/map/facts.json data/facts_medstd.json && rmdir data/map
python3 tools/bc.py "$MOD" .
python3 tools/games.py data/games.json "$@"
python3 tools/model.py .
python3 tools/calibrate.py .
python3 tools/analysis.py .
python3 tools/yields.py .
python3 tools/calibrate_needs.py . > data/calibrate_needs.log
gcc -O2 -o /tmp/settlement-bench tools/bench.c && /tmp/settlement-bench > data/bench.csv
python3 tools/sfigures.py .
python3 tools/sbuild.py .
cd .. && python3 vision/tools/vision.py .
