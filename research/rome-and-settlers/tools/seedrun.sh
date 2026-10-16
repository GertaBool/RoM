#!/bin/bash
# One reseeded continuation of a save in the headless harness.
# usage: seedrun.sh <build name> <seed> <turns>
# environment: S (work folder holding hwork2/b-<build>, masinissa/m410.init and .game,
# vers/env.sh) and MOD (mod checkout with Assets/).
: "${S:?}" "${MOD:?}"
v=$1; seed=$2; turns=$3
source $S/vers/env.sh
root=$S/hwork2/seeds/$v-$seed
mkdir -p $root
"$(dirname "$0")/../../../toolchain/harness/mkroot.sh" $root $S/hwork2/b-$v "$MOD" >/dev/null
cp $S/masinissa/m410.init $S/masinissa/m410.game $root/
cd $root && HARNESS_RESEED=$seed HARNESS_HISTORY_DIAG=1 timeout 3000 wine harness.exe save m410.init m410.game $turns m410-h.jsonl 5 20000 > run-h.log 2>&1
echo "$v $seed rc=$? $(grep RESULT run-h.log)"
