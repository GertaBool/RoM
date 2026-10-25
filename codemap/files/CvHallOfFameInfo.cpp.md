# CvHallOfFameInfo.cpp

Group: interface, text and messages. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **6** `CvHallOfFameInfo::CvHallOfFameInfo()`
  - called by (1): CyHallOfFameInfo::CyHallOfFameInfo
- **10** `CvHallOfFameInfo::~CvHallOfFameInfo()` (virtual)
  - called by (1): CvHallOfFameInfo::`scalar deleting dtor'
- **18** `CvHallOfFameInfo::loadReplays()`
  - calls: CvDLLUtilityIFaceBase::loadReplays [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (1): CyHallOfFameInfo::loadReplays
- **23** `CvHallOfFameInfo::getNumGames() const`
  - called by (1): CyHallOfFameInfo::getNumGames
- **28** `CvHallOfFameInfo::getReplayInfo(int)`
  - called by (1): CyHallOfFameInfo::getReplayInfo
- **·** `CvHallOfFameInfo::`scalar deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: operator delete(void*) [CvGameCoreDLL.cpp], CvHallOfFameInfo::~CvHallOfFameInfo
