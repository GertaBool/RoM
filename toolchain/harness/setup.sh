#!/bin/bash
# Generate the engine stubs and the base-game XML, and build the inert
# python24.dll and boost_python DLL replacements.
# usage: setup.sh <mod Assets/CvGameCoreDLL> <AdvCiv Assets/XML> <any built CvGameCoreDLL.dll>
#                 [<original game Assets/XML> <BTS Assets/XML>]
#   The DLL only supplies the list of Boost.Python imports to provide. With the
#   game's two XML folders, their files replace the generated ones.
# needs: python3, objdump, llvm-undname, lld-link
set -e
src=$1; advciv=$2; refdll=$3; basexml=$4; btsxml=$5
source "$(dirname "$0")/env.sh"
python3 "$H/gen_stubs.py" "$BTS_SDK_DIR" "$WORK/engine_stubs.h"
rm -rf "$WORK/btsxml"
python3 "$H/gen_bts_xml.py" "$src" "$advciv" "$WORK/btsxml"
[ -n "$btsxml" ] && python3 "$H/overlay_game_xml.py" "$WORK/btsxml" "$basexml" "$btsxml"
objdump -p "$refdll" | awk '/DLL Name: boost/{f=1;next} /DLL Name/{f=0} f' | awk '{print $NF}' | grep '^?' > "$WORK/bp_imports.txt"
python3 "$H/bpstub/gen_bpstub.py" "$WORK/bp_imports.txt" "$WORK/bpstub.c" "$WORK/boost_python.def"
mkdir -p "$WORK/out" "$WORK/obj"
cd "$WORK/obj"
wine "$CL" /nologo /O2 /MD /LD "$(winpath "$H/pystub/python24.c")" /Fe..\\out\\python24.dll /link /NOLOGO 2>&1 | grep -iE "error|warning" || true
wine "$CL" /nologo /O2 /MD /c "$(winpath "$WORK/bpstub.c")" /Fobpstub.obj 2>&1 | grep -iE "error|warning" || true
# MSVC 7.1's linker truncates exported names at '@'; lld-link keeps decorated names intact.
lld-link /nologo /dll /machine:x86 /def:"$WORK/boost_python.def" bpstub.obj /out:../out/boost_python-vc71-mt-1_32.dll \
  /nodefaultlib "$VCTOOLKIT_DIR/lib/msvcrt.lib" "$VCTOOLKIT_DIR/lib/oldnames.lib" "$VCTOOLKIT_DIR/lib/kernel32.lib"
ls -la "$WORK/out"/*.dll
