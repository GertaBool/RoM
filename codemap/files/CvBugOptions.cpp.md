# CvBugOptions.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **22** `logMsg(char const*, ...)`
  - calls: CvDLLUtilityIFaceBase::logMsg [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (1): setIsBug
- **30** `isBug()`
  - called by (3): CvDLLWidgetData::parseFlagHelp, getBugOptionBOOL, getBugOptionINT
- **35** `setIsBug(bool)`
  - calls: logMsg
  - called by (1): CvGlobals::setIsBug
- **42** `getDefineBOOL(char const*, bool)`
  - calls: CvGlobals::getDefinesVarSystem [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], FVariableSystem::GetValue(char const*, int&) const [FVariableSystem.inl]
  - called by (1): getBugOptionBOOL
- **55** `getDefineINT(char const*, int)`
  - calls: CvGlobals::getDefinesVarSystem [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], FVariableSystem::GetValue(char const*, int&) const [FVariableSystem.inl]
  - called by (1): getBugOptionINT
- **69** `getBugOptionBOOL(char const*, bool, char const*)`
  - calls: isBug, CyArgsList::CyArgsList [CyArgsList.h], CyArgsList::add(char const*) [CyArgsList.cpp], CyArgsList::add(int) [CyArgsList.cpp], CvDLLPythonIFaceBase::callFunction [CvDLLPythonIFaceBase.h], CvDLLUtilityIFaceBase::getPythonIFace [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CyArgsList::makeFunctionArgs [CyArgsList.cpp], CvString::CvString() [CvString.h], getDefineBOOL, CvString::~CvString [CvString.h]
  - called by (32): CvDLLButtonPopup::launchProductionPopup, CvDLLWidgetData::doTrain, CvDLLWidgetData::parseChangeSpecialistHelp, CvDLLWidgetData::parseConscriptHelp, CvDLLWidgetData::parseHappinessHelp, CvDLLWidgetData::parseHealthHelp, CvDLLWidgetData::parseHelp, CvDLLWidgetData::parseHurryHelp, CvDLLWidgetData::parseMaintenanceHelp, CvGame::selectionListMove, CvGameTextMgr::buildCityBillboardCityNameString, CvGameTextMgr::buildCityBillboardIconString …
- **99** `getBugOptionINT(char const*, int, char const*)`
  - calls: isBug, CyArgsList::CyArgsList [CyArgsList.h], CyArgsList::add(char const*) [CyArgsList.cpp], CyArgsList::add(int) [CyArgsList.cpp], CvDLLPythonIFaceBase::callFunction [CvDLLPythonIFaceBase.h], CvDLLUtilityIFaceBase::getPythonIFace [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CyArgsList::makeFunctionArgs [CyArgsList.cpp], CvString::CvString() [CvString.h], getDefineINT, CvString::~CvString [CvString.h]
  - called by (3): CvGameTextMgr::setBuildingHelpActual, CvGameTextMgr::setCombatPlotHelp, CvGameTextMgr::setUnitHelp(CvWStringBuffer&, UnitTypes, bool, bool, bool, CvCity*)
