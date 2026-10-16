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
# realpath -s: absolute without resolving symlinks; setup_toolchain.sh links vctk to a
# folder whose name contains spaces, which the GNUmakefile cannot pass to cl.
winpath() { echo "Z:$(realpath -s "$1")"; }
# Incremental: an existing build tree is kept and only changed files are copied, so
# make recompiles just those .cpp files. .depend is empty (no header dependencies),
# so a changed header removes every object and the build is complete again.
# CLEAN=1 forces a build from nothing.
[ "${CLEAN:-0}" = 1 ] && rm -rf "$out"
mkdir -p "$out"
header_changed=0
for f in "$src"/*.cpp "$src"/*.h "$src"/*.inl "$src"/GNUmakefile "$src"/gensourcelist; do
  t="$out/$(basename "$f")"
  if ! cmp -s "$f" "$t"; then
    cp -p "$f" "$t"
    case "$f" in *.h|*.inl|*GNUmakefile) header_changed=1;; esac
  fi
done
[ "$header_changed" = 1 ] && rm -rf "$out/release"
[ -e "$out/Boost-1.32.0" ] || ln -s "$BTS_SDK_DIR/Boost-1.32.0" "$out/Boost-1.32.0"
[ -e "$out/Python24" ] || ln -s "$BTS_SDK_DIR/Python24" "$out/Python24"
cd "$out"
sh ./gensourcelist
: > .depend; touch .depend
export WINEARCH=win32 WINEDEBUG=-all
make -j"$jobs" TARGET=release WINE=wine \
  VCTOOLKIT="$(winpath "$VCTOOLKIT_DIR")" PSDK="$(winpath "$PSDK_DIR")" \
  BOOST=./Boost-1.32.0 PYTHON=./Python24 OUTDIR=./out release/CvGameCoreDLL.dll
