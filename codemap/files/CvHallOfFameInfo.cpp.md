# CvHallOfFameInfo.cpp

Group: interface, text and messages. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **5** `CvHallOfFameInfo::CvHallOfFameInfo()`
- **9** `CvHallOfFameInfo::~CvHallOfFameInfo()` (virtual)
- **17** `CvHallOfFameInfo::loadReplays()`
  - calls: CvDLLUtilityIFaceBase::loadReplays [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
  - called by (1): CyHallOfFameInfo::loadReplays
- **22** `CvHallOfFameInfo::getNumGames()`
  - called by (1): CyHallOfFameInfo::getNumGames
- **27** `CvHallOfFameInfo::getReplayInfo(int)`
  - called by (1): CyHallOfFameInfo::getReplayInfo
