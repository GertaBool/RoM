#!/bin/bash
# usage: build.sh <CvGameCoreDLL-source-dir> <build-dir> [jobs]
# Builds CvGameCoreDLL.dll with VC++ Toolkit 2003 + Platform SDK 2003 under Wine,
# using the repository's own GNUmakefile (release target).
set -e
src=$1; out=$2; jobs=${3:-8}
SDKB=/home/user/src/sdk/beyond-the-sword-sdk-develop/CvGameCoreDLL
rm -rf "$out"; mkdir -p "$out"
cp "$src"/*.cpp "$src"/*.h "$src"/*.inl "$src"/GNUmakefile "$src"/gensourcelist "$out"/
ln -s $SDKB/Boost-1.32.0 "$out"/Boost-1.32.0
ln -s $SDKB/Python24 "$out"/Python24
cd "$out"
sh ./gensourcelist
: > .depend; touch .depend
export WINEPREFIX=/home/user/src/msvc/wine32 WINEARCH=win32 WINEDEBUG=-all
make -j"$jobs" TARGET=release WINE=wine \
  VCTOOLKIT=Z:/home/user/src/msvc/vctk PSDK=Z:/home/user/src/msvc/psdk2003 \
  BOOST=./Boost-1.32.0 PYTHON=./Python24 OUTDIR=./out release/CvGameCoreDLL.dll
