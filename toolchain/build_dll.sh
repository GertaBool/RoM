#!/bin/bash
# Build CvGameCoreDLL.dll with Visual C++ Toolkit 2003 + Platform SDK 2003 under Wine,
# using the repository's own GNUmakefile (release target, no _MOD_* switches, like
# the shipped DLL).
#
# usage: build_dll.sh <Assets/CvGameCoreDLL source dir> <build dir> [jobs]
# environment (Linux paths):
#   VCTOOLKIT_DIR  folder containing bin/cl.exe, include/, lib/ (incl. msvcprt.lib)
#   PSDK_DIR       Platform SDK folder with Include/ and Lib/ (lower-case aliases added by setup)
#   BTS_SDK_DIR    BTS SDK CvGameCoreDLL folder with Boost-1.32.0/ and Python24/
#   WINEPREFIX     32-bit prefix (WINEARCH=win32)
set -e
src=$1; out=$2; jobs=${3:-8}
: "${VCTOOLKIT_DIR:?}" "${PSDK_DIR:?}" "${BTS_SDK_DIR:?}" "${WINEPREFIX:?}"
winpath() { echo "Z:$(readlink -f "$1")"; }
rm -rf "$out"; mkdir -p "$out"
cp "$src"/*.cpp "$src"/*.h "$src"/*.inl "$src"/GNUmakefile "$src"/gensourcelist "$out"/
ln -s "$BTS_SDK_DIR/Boost-1.32.0" "$out/Boost-1.32.0"
ln -s "$BTS_SDK_DIR/Python24" "$out/Python24"
cd "$out"
sh ./gensourcelist
: > .depend; touch .depend
export WINEARCH=win32 WINEDEBUG=-all
make -j"$jobs" TARGET=release WINE=wine \
  VCTOOLKIT="$(winpath "$VCTOOLKIT_DIR")" PSDK="$(winpath "$PSDK_DIR")" \
  BOOST=./Boost-1.32.0 PYTHON=./Python24 OUTDIR=./out release/CvGameCoreDLL.dll
