# CvBugOptions.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **21** `logMsg(const char *, ...)`
  - calls: CvDLLUtilityIFaceBase::logMsg [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
  - called by (1): setIsBug
- **29** `isBug()`
  - called by (3): CvDLLWidgetData::parseFlagHelp, getBugOptionBOOL, getBugOptionINT
- **34** `setIsBug(bool)`
  - calls: logMsg
  - called by (1): CvGlobals::setIsBug
- **41** `getDefineBOOL(const char *, bool)`
  - calls: CvGlobals::getDefinesVarSystem [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], FVariableSystem::GetValue(const char *, int &) [FVariableSystem.inl]
  - called by (1): getBugOptionBOOL
- **54** `getDefineINT(const char *, int)`
  - calls: CvGlobals::getDefinesVarSystem [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], FVariableSystem::GetValue(const char *, int &) [FVariableSystem.inl]
  - called by (1): getBugOptionINT
- **68** `getBugOptionBOOL(const char *, bool, const char *)`
  - calls: isBug, CyArgsList::CyArgsList [CyArgsList.h], CyArgsList::add(const char *) [CyArgsList.cpp], CyArgsList::add(int) [CyArgsList.cpp], CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, long *) [CvDLLPythonIFaceBase.h], CvDLLUtilityIFaceBase::getPythonIFace [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CyArgsList::makeFunctionArgs [CyArgsList.cpp], CvString::CvString() [CvString.h], getDefineBOOL
  - called by (32): CvDLLButtonPopup::launchProductionPopup, CvDLLWidgetData::doTrain, CvDLLWidgetData::parseChangeSpecialistHelp, CvDLLWidgetData::parseConscriptHelp, CvDLLWidgetData::parseHappinessHelp, CvDLLWidgetData::parseHealthHelp, CvDLLWidgetData::parseHelp, CvDLLWidgetData::parseHurryHelp, CvDLLWidgetData::parseMaintenanceHelp, CvGame::selectionListMove, CvGameTextMgr::buildCityBillboardCityNameString, CvGameTextMgr::buildCityBillboardIconString …
- **98** `getBugOptionINT(const char *, int, const char *)`
  - calls: isBug, CyArgsList::CyArgsList [CyArgsList.h], CyArgsList::add(const char *) [CyArgsList.cpp], CyArgsList::add(int) [CyArgsList.cpp], CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, long *) [CvDLLPythonIFaceBase.h], CvDLLUtilityIFaceBase::getPythonIFace [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CyArgsList::makeFunctionArgs [CyArgsList.cpp], CvString::CvString() [CvString.h], getDefineINT
  - called by (3): CvGameTextMgr::setBuildingHelpActual, CvGameTextMgr::setCombatPlotHelp, CvGameTextMgr::setUnitHelp(CvWStringBuffer &, UnitTypes, bool, bool, bool, CvCity *)
