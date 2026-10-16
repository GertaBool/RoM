#!/bin/bash
# usage: check.sh <mirror-dir> <file.cpp> [extra clang args]
# Whole-translation-unit semantic check of one DLL source file with clang in MSVC
# compatibility mode, against the BTS SDK's Boost 1.32 and Python 2.4 headers.
# Environment: BTS_SDK_DIR (CvGameCoreDLL folder of the BTS SDK), CASEDIR (mirror dir).
HERE=$(dirname "$(readlink -f "$0")")
: "${BTS_SDK_DIR:?set BTS_SDK_DIR to the BTS SDK CvGameCoreDLL folder}"
dir=$1; shift; f=$1; shift
cd "$dir" && clang++ -fsyntax-only -std=gnu++98 -fms-extensions -fms-compatibility -fdelayed-template-parsing \
  -Wno-everything -ferror-limit=0 -Wno-error=non-pod-varargs -Wno-error=invalid-token-paste \
  -I"$HERE" -I"${CASEDIR:-$dir}" -isystem "$BTS_SDK_DIR/Boost-1.32.0/include" -isystem "$BTS_SDK_DIR/Python24/include" \
  -DWIN32 -D_WINDOWS -D_USRDLL -DCVGAMECOREDLL_EXPORTS -DNDEBUG -DFINAL_RELEASE "$@" "$f"
