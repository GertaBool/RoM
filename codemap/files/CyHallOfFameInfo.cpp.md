# CyHallOfFameInfo.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **6** `CyHallOfFameInfo::CyHallOfFameInfo()`
  - calls: CvHallOfFameInfo::CvHallOfFameInfo [CvHallOfFameInfo.cpp]
- **11** `CyHallOfFameInfo::loadReplays()` (Python: loadReplays)
  - calls: CvHallOfFameInfo::loadReplays [CvHallOfFameInfo.cpp]
  - called by (1): CyHallOfFameInterface
- **16** `CyHallOfFameInfo::getNumGames() const` (Python: getNumGames)
  - calls: CvHallOfFameInfo::getNumGames [CvHallOfFameInfo.cpp]
  - called by (1): CyHallOfFameInterface
- **21** `CyHallOfFameInfo::getReplayInfo(int)` (Python: getReplayInfo)
  - calls: operator new(unsigned int) [CvGameCoreDLL.cpp], CvHallOfFameInfo::getReplayInfo [CvHallOfFameInfo.cpp], CyReplayInfo::CyReplayInfo(CvReplayInfo*) [CyReplayInfo.cpp], operator delete(void*) [CvGameCoreDLL.cpp]
  - called by (1): CyHallOfFameInterface
