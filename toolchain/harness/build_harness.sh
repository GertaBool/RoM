#!/bin/bash
# Build harness.exe against a harness DLL build (headers + import library).
# usage: build_harness.sh <build dir from build_dll.sh>
set -e
B=$1
source "$(dirname "$0")/env.sh"
mkdir -p "$WORK/obj/inc"
cd "$WORK/obj"
# The DLL's headers declare everything dllexport; seen from the harness the
# same declarations must be dllimport, or inline exported members would drag
# in the vtables of non-exported classes.
cp "$B"/*.h "$B"/*.inl inc/
sed -i 's|^#define DllExport   __declspec( dllexport )|#define DllExport   __declspec( dllimport )|' inc/CvGameCoreDLL.h
grep -q "dllimport" inc/CvGameCoreDLL.h
INC="/I$(winpath inc) /I$(winpath "$BTS_SDK_DIR/Boost-1.32.0/include") /I$(winpath "$BTS_SDK_DIR/Python24/include") /I$(winpath "$H") /I$(winpath "$WORK")"
FLAGS="/nologo /MD /GR /EHsc /O2 /DWIN32 /D_WINDOWS /D_USRDLL /DNDEBUG /DFINAL_RELEASE /W3 /wd4100"
for f in engine xmldom main; do
  wine "$CL" $FLAGS $INC /c "$(winpath "$H/$f.cpp")" /Fo$f.obj 2>&1 | grep -E "error|warning C4(700|715|172|6)" || true
done
wine "$LINK" /NOLOGO /SUBSYSTEM:CONSOLE /LARGEADDRESSAWARE engine.obj xmldom.obj main.obj \
  "$(winpath "$B/release/CvGameCoreDLL.lib")" \
  /LIBPATH:"$(winpath "$BTS_SDK_DIR/Boost-1.32.0/libs")" /LIBPATH:"$(winpath "$BTS_SDK_DIR/Python24/libs")" \
  boost_python-vc71-mt-1_32.lib python24.lib user32.lib msvcprt.lib msvcrt.lib /OUT:harness.exe 2>&1 | grep -v "^$" || true
ls -la harness.exe
