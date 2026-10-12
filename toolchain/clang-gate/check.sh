#!/bin/bash
# usage: check.sh <dll-dir> <file.cpp> [extra clang args]
SDK=/home/user/src/sdk/beyond-the-sword-sdk-develop/CvGameCoreDLL
dir=$1; shift; f=$1; shift
cd "$dir" && clang++ -fsyntax-only -std=gnu++98 -fms-extensions -fms-compatibility -fdelayed-template-parsing -Wno-everything -ferror-limit=0 -Wno-error=non-pod-varargs -Wno-error=invalid-token-paste \
  -I/home/user/src/shim -I${CASEDIR:-/home/user/src/case-upstream} -isystem $SDK/Boost-1.32.0/include -isystem $SDK/Python24/include \
  -DWIN32 -D_WINDOWS -D_USRDLL -DCVGAMECOREDLL_EXPORTS -DNDEBUG -DFINAL_RELEASE \
  -D_MOD_SENTRY -D_MOD_FRACTRADE -D_MOD_GOVWORKERS "$@" "$f"
