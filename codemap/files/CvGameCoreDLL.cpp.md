# CvGameCoreDLL.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **15** `operator new(unsigned int)`
  - calls: CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvDLLUtilityIFaceBase::newMem [CvDLLUtilityIFaceBase.h]
  - called by (610): CLinkList<CvWString>::insertAtEnd, CLinkList<IDInfo>::Read, CLinkList<IDInfo>::insertAtBeginning, CLinkList<IDInfo>::insertAtEnd, CLinkList<IDInfo>::insertBefore, CLinkList<MissionData>::Read, CLinkList<MissionData>::insertAtEnd, CLinkList<OrderData>::Read, CLinkList<OrderData>::insertAtBeginning, CLinkList<OrderData>::insertAtEnd, CLinkList<TechTypes>::Read, CLinkList<TechTypes>::insertAtEnd …
- **24** `operator delete(void*)`
  - calls: CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvDLLUtilityIFaceBase::delMem [CvDLLUtilityIFaceBase.h]
  - called by (838): CLLNode<CvWString>::`scalar deleting dtor', CLLNode<IDInfo>::`scalar deleting dtor', CLLNode<MissionData>::`scalar deleting dtor', CLLNode<OrderData>::`scalar deleting dtor', CLLNode<TechTypes>::`scalar deleting dtor', CLLNode<TradeData>::`scalar deleting dtor', CLLNode<XYCoords>::`scalar deleting dtor', CLLNode<int>::`scalar deleting dtor', CLinkList<CvWString>::`scalar deleting dtor', CLinkList<CvWString>::insertAtEnd, CLinkList<IDInfo>::Read, CLinkList<IDInfo>::`scalar deleting dtor' …
- **36** `operator new[](unsigned int)`
  - calls: CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvDLLUtilityIFaceBase::newMemArray [CvDLLUtilityIFaceBase.h]
  - called by (153): CvArea::CvArea, CvArea::reset, CvArtInfoTerrain::CvArtInfoTerrain(), CvBonusInfo::read(FDataStreamBase*), CvBuildingInfo::read(FDataStreamBase*), CvCity::CvCity, CvCity::reset, CvCity::updateTradeRoutes, CvCityAI::AI_reset, CvCityAI::CvCityAI, CvCivicInfo::read(FDataStreamBase*), CvCivilizationInfo::copyNonDefaults …
- **43** `operator delete[](void*)`
  - calls: CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvDLLUtilityIFaceBase::delMemArray [CvDLLUtilityIFaceBase.h]
  - called by (245): CvActionInfo::`vector deleting dtor', CvAnimationCategoryInfo::`vector deleting dtor', CvAnimationPathInfo::`vector deleting dtor', CvArea::CvArea, CvArea::uninit, CvArea::~CvArea, CvArtFileMgr::`vector deleting dtor', CvArtInfoAsset::`vector deleting dtor', CvArtInfoBonus::`vector deleting dtor', CvArtInfoBuilding::`vector deleting dtor', CvArtInfoCivilization::`vector deleting dtor', CvArtInfoFeature::`vector deleting dtor' …
- **55** `operator new(unsigned int, char*, int)`
  - calls: CvDLLUtilityIFaceBase::newMem [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
- **60** `operator new[](unsigned int, char*, int)`
  - calls: CvDLLUtilityIFaceBase::newMem [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
- **65** `operator delete(void*, char*, int)`
  - calls: CvDLLUtilityIFaceBase::delMem [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
- **70** `operator delete[](void*, char*, int)`
  - calls: CvDLLUtilityIFaceBase::delMem [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
- **76** `reallocMem(void*, unsigned int, char const*, int)`
  - calls: CvDLLUtilityIFaceBase::reallocMem [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
- **81** `memSize(void*)`
  - calls: CvDLLUtilityIFaceBase::memSize [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
- **92** `_DllMain@12`
  - calls: CvGlobals::setDLLIFace [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
- **138** `startProfilingDLL()`
  - calls: CvGlobals::isDLLProfilerEnabled [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::ProfilerBegin [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (1): CvPlayer::setTurnActive
- **149** `stopProfilingDLL()`
  - calls: CvGlobals::isDLLProfilerEnabled [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvDLLUtilityIFaceBase::ProfilerEnd [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (1): CvGame::doTurn
