#!/bin/bash
# usage: mirror.sh <dll-src-dir> <out-dir> -- copy DLL source, apply semantics-preserving portability edits
set -e
HERE=$(dirname "$(readlink -f "$0")")
src=$1; out=$2
rm -rf "$out"; mkdir -p "$out"
cp "$src"/*.cpp "$src"/*.h "$src"/*.inl "$out"/ 2>/dev/null || true
# MSVC accepts pasting a type name with '*'/'&'; standard preprocessors do not.
sed -i 's/##\*/ */g; s/##&/ \&/g' "$out"/CvArtFileMgr.h
python3 "$HERE/mkcase.py" "$out" "$out"
