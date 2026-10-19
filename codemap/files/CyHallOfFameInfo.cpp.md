# CyHallOfFameInfo.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **5** `CyHallOfFameInfo::CyHallOfFameInfo()`
- **10** `CyHallOfFameInfo::loadReplays()` (Python: loadReplays)
  - calls: CvHallOfFameInfo::loadReplays [CvHallOfFameInfo.cpp]
  - called by (1): CyHallOfFameInterface
- **15** `CyHallOfFameInfo::getNumGames()` (Python: getNumGames)
  - calls: CvHallOfFameInfo::getNumGames [CvHallOfFameInfo.cpp]
  - called by (1): CyHallOfFameInterface
- **20** `CyHallOfFameInfo::getReplayInfo(int)` (Python: getReplayInfo)
  - calls: CvHallOfFameInfo::getReplayInfo [CvHallOfFameInfo.cpp], CyReplayInfo::CyReplayInfo(CvReplayInfo *) [CyReplayInfo.cpp]
  - called by (1): CyHallOfFameInterface
