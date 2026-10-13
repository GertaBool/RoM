#!/bin/bash
# Build a harness variant of CvGameCoreDLL: the given source tree plus
# HarnessHooks.cpp (extra exports only), optionally with BBAI logging on.
# usage: build_dll.sh <Assets/CvGameCoreDLL> <build dir> [log]
set -e
src=$1; out=$2; log=$3
source "$(dirname "$0")/env.sh"
tmp=$(mktemp -d "$WORK/dllsrc.XXXX")
cp "$src"/*.cpp "$src"/*.h "$src"/*.inl "$src"/GNUmakefile "$src"/gensourcelist "$tmp"/
cp "$H/HarnessHooks.cpp" "$tmp"/
if [ "$log" = log ]; then export CFLAGS="/DLOG_AI"; fi
"$H/../build_dll.sh" "$tmp" "$out" 8
rm -rf "$tmp"
ls -la "$out/release/CvGameCoreDLL.dll"
