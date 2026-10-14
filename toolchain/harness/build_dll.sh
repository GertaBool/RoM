#!/bin/bash
# Build a harness variant of CvGameCoreDLL: the given source tree plus
# the Harness*.cpp files (exports, telemetry, mirrors of the mod's Python),
# optionally with BBAI logging on.
# usage: build_dll.sh <Assets/CvGameCoreDLL> <build dir> [log|profile|logprofile]
#   profile: PROFILE_FUNC scopes report to the harness profiler (slower, for relative costs)
set -e
src=$1; out=$2; log=$3
source "$(dirname "$0")/env.sh"
tmp=$(mktemp -d "$WORK/dllsrc.XXXX")
cp "$src"/*.cpp "$src"/*.h "$src"/*.inl "$src"/GNUmakefile "$src"/gensourcelist "$tmp"/
cp "$H"/Harness*.cpp "$H"/Harness*.h "$tmp"/
# RoM's Python building rules, mirrored in HarnessRoM.cpp; tables from the mod's Python.
python3 "$H/gen_rom_tables.py" "$src/../Python" "$tmp/HarnessRoMTables.h"
# Harness-only instrumentation of the copy (the source tree is not touched):
# CvDeal::addTrades reports every agreed trade to the telemetry (HH_noteTrade);
# the building-built and begin-player-turn events run the Python mirrors;
# HarnessPeek may read the AI's caches.
python3 - "$tmp" <<'PYEOF'
import sys
d = sys.argv[1]

def insert(name, function, anchor, call, decl, after=False):
    p = d + '/' + name
    s = open(p, 'rb').read().decode('latin-1')
    start = s.index(function)
    i = s.index(anchor, start) + (len(anchor) if after else 0)
    s = s[:i] + call + '\r\n' + s[i:]
    s = s[:start] + decl + '\r\n' + s[start:]
    open(p, 'wb').write(s.encode('latin-1'))

insert('CvDeal.cpp', 'void CvDeal::addTrades(', '\tTeamTypes eFirstTeam = GET_PLAYER(getFirstPlayer()).getTeam();',
       '\tHH_noteTrade(getFirstPlayer(), getSecondPlayer(), pFirstList, pSecondList);',
       'void HH_noteTrade(PlayerTypes eFirst, PlayerTypes eSecond, const CLinkList<TradeData>* pFirst, const CLinkList<TradeData>* pSecond);')
insert('CvEventReporter.cpp', 'void CvEventReporter::buildingBuilt(', '{\r\n',
       '\tHH_buildingBuilt(pCity, eBuilding);', 'void HH_buildingBuilt(CvCity* pCity, BuildingTypes eBuilding);', after=True)
insert('CvEventReporter.cpp', 'void CvEventReporter::beginPlayerTurn(', '{\r\n',
       '\tHH_beginPlayerTurn(iGameTurn, ePlayer);', 'void HH_beginPlayerTurn(int iGameTurn, PlayerTypes ePlayer);', after=True)
# HarnessPeek (HarnessPeek.h) reads and restores the AI's caches.
for name, anchor in (('CvPlayerAI.h', 'class CvPlayerAI : public CvPlayer\r\n{\r\n'),
                     ('CvCityAI.h', 'class CvCityAI : public CvCity\r\n{\r\n'),
                     ('CvCity.h', 'class CvCity : public CvDLLEntity\r\n{\r\n')):
    p = d + '/' + name
    s = open(p, 'rb').read().decode('latin-1')
    i = s.index(anchor) + len(anchor)
    s = s[:i] + '\tfriend struct HarnessPeek;\r\n' + s[i:]
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
