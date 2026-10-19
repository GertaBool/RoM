# CvGameCoreDLL.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **14** `operator new(size_t)`
  - calls: CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::newMem(size_t, const char *, int) [CvDLLUtilityIFaceBase.h]
- **23** `operator delete(void *)`
  - calls: CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::delMem(void *, const char *, int) [CvDLLUtilityIFaceBase.h]
- **35** `operator new[](size_t)`
  - calls: CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::newMemArray [CvDLLUtilityIFaceBase.h]
- **42** `operator delete[](void *)`
  - calls: CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::delMemArray [CvDLLUtilityIFaceBase.h]
- **54** `operator new(size_t, char *, int)`
  - calls: CvDLLUtilityIFaceBase::newMem(size_t, const char *, int) [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **59** `operator new[](size_t, char *, int)`
  - calls: CvDLLUtilityIFaceBase::newMem(size_t, const char *, int) [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **64** `operator delete(void *, char *, int)`
  - calls: CvDLLUtilityIFaceBase::delMem(void *, const char *, int) [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **69** `operator delete[](void *, char *, int)`
  - calls: CvDLLUtilityIFaceBase::delMem(void *, const char *, int) [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **75** `reallocMem(void *, unsigned int, const char *, int)`
  - calls: CvDLLUtilityIFaceBase::reallocMem [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **80** `memSize(void *)`
  - calls: CvDLLUtilityIFaceBase::memSize [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **89** `DllMain(HANDLE, DWORD, LPVOID)`
  - calls: CvGlobals::setDLLIFace [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
- **137** `startProfilingDLL()`
  - calls: CvGlobals::isDLLProfilerEnabled [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::ProfilerBegin [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (1): CvPlayer::setTurnActive
- **148** `stopProfilingDLL()`
  - calls: CvGlobals::isDLLProfilerEnabled [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::ProfilerEnd [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (1): CvGame::doTurn
