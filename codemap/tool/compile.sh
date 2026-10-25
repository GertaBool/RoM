#!/bin/bash
# Compile every .cpp of the DLL source with the real compiler (Visual C++ Toolkit 2003 under Wine) and keep,
# per file, the object (.obj) and the assembly listing with source lines (.asm, from /FAs), and the type
# records of every class in one probe object (codemap_types.obj). These are what the code map is read from; nothing is linked or run.
# usage: compile.sh <Assets/CvGameCoreDLL dir> <work dir> [jobs]
# Flags: those of the source's GNUmakefile release target, with the release defines (NDEBUG,
# FINAL_RELEASE) but /Od /Ob0 instead of /O2: no optimisation and no inlining, so every call written in
# the source stays a call in the listing.
# Environment: VCTOOLKIT_DIR PSDK_DIR BTS_SDK_DIR WINEPREFIX (toolchain/README.md).
set -eu
src=$(cd "$1" && pwd); w=$2; jobs=${3:-4}
: "${VCTOOLKIT_DIR:?}" "${PSDK_DIR:?}" "${BTS_SDK_DIR:?}" "${WINEPREFIX:?}"
export WINEARCH=win32 WINEDEBUG=-all
mkdir -p "$w/b" "$w/out"
cp "$src"/*.cpp "$src"/*.h "$src"/*.inl "$w/b/"
printf '#define WAR_LOG_BUILD "%s"\r\n' codemap > "$w/b/WarLogBuild.h"
ln -sfn "$BTS_SDK_DIR/Boost-1.32.0" "$w/b/Boost-1.32.0"
ln -sfn "$BTS_SDK_DIR/Python24" "$w/b/Python24"
wp() { echo "Z:$(realpath -s "$1")"; }
vc=$(wp "$VCTOOLKIT_DIR"); ps=$(wp "$PSDK_DIR")
cl="$VCTOOLKIT_DIR/bin/cl.exe"
flags="/MD /nologo /GR /Gy /W3 /EHsc /Gd /Gm- /DWIN32 /D_WINDOWS /D_USRDLL /DCVGAMECOREDLL_EXPORTS /c
 /Fp../out/CvGameCoreDLL.pch /I$vc/include /I$ps/Include /I$ps/Include/mfc /IBoost-1.32.0/include
 /IPython24/include /Od /Ob0 /DNDEBUG /DFINAL_RELEASE /FAs /Fa../out/"
cd "$w/b"
# Under Wine, cl can hang after an error: each compile has a time limit.
# shellcheck disable=SC2086
timeout 1800 wine "$cl" _precompile.cpp $flags /YcCvGameCoreDLL.h /Fo../out/_precompile.obj > ../out/_precompile.log 2>&1 \
  || { cat ../out/_precompile.log; exit 1; }
# The type records (classes, bases, virtual methods and their slots) come from one probe unit that includes
# every header, built as a precompiled header with /Z7: MSVC writes the types of everything a precompiled
# header defines, used or not. (Units do not get /Z7: the Boost.Python ones exceed its limit, C1067.)
{ printf '#include "CvGameCoreDLL.h"\r\n'; for h in *.h; do printf '#include "%s"\r\n' "$h"; done; printf '#pragma hdrstop\r\n'; } \
  > _codemap_types.cpp
probe_flags=$(echo "$flags" | sed 's|/Fp[^ ]*||')   # its own precompiled header file
# shellcheck disable=SC2086
timeout 1800 wine "$cl" _codemap_types.cpp $probe_flags /Z7 /Yc /Fp../out/codemap_types.pch \
  /Fo../out/codemap_types.obj > ../out/codemap_types.log 2>&1 || { cat ../out/codemap_types.log; exit 1; }
for f in *.cpp; do case "$f" in _precompile.cpp|_codemap_types.cpp) ;; *) echo "$f";; esac; done | sort | xargs -P "$jobs" -I{} sh -c \
  "timeout 1800 wine '$cl' {} $(echo $flags) /YuCvGameCoreDLL.h /Fo../out/\$(basename {} .cpp).obj > ../out/\$(basename {} .cpp).log 2>&1 \
   || echo 'FAILED {}'"
# a unit that did not compile leaves no listing: say so, and fail
missing=0
for f in *.cpp; do [ "$f" = _codemap_types.cpp ] || [ -s "../out/${f%.cpp}.asm" ] || { echo "no listing for $f"; missing=1; }; done
exit $missing
