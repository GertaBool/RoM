#!/bin/bash
# Build a harness variant of CvGameCoreDLL: the given source tree plus
# HarnessHooks.cpp (extra exports only), optionally with BBAI logging on.
# usage: build_dll.sh <Assets/CvGameCoreDLL> <build dir> [log|profile|logprofile]
#   profile: PROFILE_FUNC scopes report to the harness profiler (slower, for relative costs)
set -e
src=$1; out=$2; log=$3
source "$(dirname "$0")/env.sh"
tmp=$(mktemp -d "$WORK/dllsrc.XXXX")
cp "$src"/*.cpp "$src"/*.h "$src"/*.inl "$src"/GNUmakefile "$src"/gensourcelist "$tmp"/
cp "$H"/Harness*.cpp "$tmp"/
# Harness-only instrumentation of the copy: CvDeal::addTrades reports every
# agreed trade to the telemetry (HH_noteTrade). The source tree is not touched.
python3 - "$tmp/CvDeal.cpp" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p, 'rb').read().decode('latin-1')
anchor = '\tTeamTypes eFirstTeam = GET_PLAYER(getFirstPlayer()).getTeam();'
start = s.index('void CvDeal::addTrades(')
i = s.index(anchor, start)
s = s[:i] + '\tHH_noteTrade(getFirstPlayer(), getSecondPlayer(), pFirstList, pSecondList);\r\n' + s[i:]
decl = 'void HH_noteTrade(PlayerTypes eFirst, PlayerTypes eSecond, const CLinkList<TradeData>* pFirst, const CLinkList<TradeData>* pSecond);\r\n'
s = s[:start] + decl + s[start:]
open(p, 'wb').write(s.encode('latin-1'))
PYEOF
case "$log" in
  log) export CFLAGS="/DLOG_AI" ;;
  profile) export CFLAGS="/DFP_PROFILE_ENABLE" ;;
  logprofile) export CFLAGS="/DLOG_AI /DFP_PROFILE_ENABLE" ;;
esac
# Diagnostics that need the settlement delivery regions (patch 0012 and later).
if grep -q AI_canDeliverSettler "$src/CvPlayerAI.h"; then export CFLAGS="${CFLAGS:-} /DHARNESS_SETTLE_REACH"; fi
"$H/../build_dll.sh" "$tmp" "$out" 8
rm -rf "$tmp"
ls -la "$out/release/CvGameCoreDLL.dll"
