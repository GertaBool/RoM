#!/bin/bash
# usage: runscn.sh <set name> <build dir> <map tag> <speed> <seed> [turns]
# WORK: harness work dir with b-* builds and scn/ (converted WorldBuilder scenarios); MOD: the mod checkout; HARNESS: toolchain/harness
S=${WORK:?set WORK}; MOD=${MOD:?set MOD}; HARNESS=${HARNESS:-$(cd "$(dirname "$0")/../../../toolchain/harness" && pwd)}
set_name=$1; build=$2; tag=$3; speed=$4; seed=$5; turns=$6
case $tag in
  med) scn="Mediterranean, Standard.scn" ;;
  earth12) scn="Earth 12 preset civs, Standard.scn" ;;
  earth18) scn="Earth 18 preset civs, Huge.scn" ;;
esac
case $speed in
  GAMESPEED_EPIC) : ${turns:=300}; detail=10 ;;
  GAMESPEED_MARATHON) : ${turns:=590}; detail=20 ;;
esac
source "$HARNESS/env.sh"
root=$S/$set_name/$tag-${speed#GAMESPEED_}-$seed
mkdir -p "$root"
"$HARNESS/mkroot.sh" "$root" "$build" "$MOD" >/dev/null
cp "$S/scn/$scn" "$root/map.scn"
cd "$root" && timeout 20000 wine harness.exe scenario map.scn $speed HANDICAP_NOBLE $seed $turns run.jsonl $detail > run.log 2>&1
echo "$set_name $tag $speed $seed rc=$? $(grep RESULT run.log) $(date -u +%H:%M)"
