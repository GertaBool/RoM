# CvDLLPythonIFaceBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **22** `CvDLLPythonIFaceBase::isInitialized()` (virtual; pure virtual, provided by the exe)
  - called by (1): CvDllPythonEvents::preEvent
- **24** `CvDLLPythonIFaceBase::getMapScriptModule()` (virtual; pure virtual, provided by the exe)
  - called by (22): CvGame::assignStartingPlots, CvGame::normalizeStartingPlots, CvGame::pythonIsBonusIgnoreLatitudes, CvMap::init, CvMap::reset, CvMapGenerator::addBonuses, CvMapGenerator::addFeatures, CvMapGenerator::addGoodies, CvMapGenerator::addLakes, CvMapGenerator::addRivers, CvMapGenerator::afterGeneration, CvMapGenerator::canPlaceBonusAt …
- **32** `CvDLLPythonIFaceBase::MakeFunctionArgs(void **, int)` (virtual; pure virtual, provided by the exe)
  - called by (1): CyArgsList::makeFunctionArgs
- **34** `CvDLLPythonIFaceBase::moduleExists(const char *, bool)` (virtual; pure virtual, provided by the exe)
- **35** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *)` (virtual; pure virtual, provided by the exe)
  - called by (40): CvDLLButtonPopup::OnOkClicked, CvDLLButtonPopup::launchPythonScreen, CvDLLWidgetData::doForeignAdvisor, CvDLLWidgetData::doPediaBack, CvDLLWidgetData::doPediaBonusJump, CvDLLWidgetData::doPediaBuildJump, CvDLLWidgetData::doPediaBuildingJump, CvDLLWidgetData::doPediaCivicJump, CvDLLWidgetData::doPediaCivilizationJump, CvDLLWidgetData::doPediaConstructJump, CvDLLWidgetData::doPediaCorporationJump, CvDLLWidgetData::doPediaDescription …
- **36** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, long *)` (virtual; pure virtual, provided by the exe)
  - called by (88): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool), CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCity::getConscriptUnit …
- **37** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, CvString *)` (virtual; pure virtual, provided by the exe)
- **38** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, CvWString *)` (virtual; pure virtual, provided by the exe)
  - called by (2): CvDLLWidgetData::parseFlagHelp, CvGameTextMgr::setEventHelp
- **39** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, std::vector<byte> *)` (virtual; pure virtual, provided by the exe)
- **40** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, std::vector<int> *)` (virtual; pure virtual, provided by the exe)
  - called by (4): CvGame::getNewHighlightPlot, CvMap::reset, CvMapGenerator::generatePlotTypes, CvMapGenerator::generateTerrain
- **41** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, int *, int *)` (virtual; pure virtual, provided by the exe)
- **42** `CvDLLPythonIFaceBase::callFunction(const char *, const char *, void *, std::vector<float> *)` (virtual; pure virtual, provided by the exe)
- **43** `CvDLLPythonIFaceBase::callPythonFunction(const char *, const char *, int, long *)` (virtual; pure virtual, provided by the exe)
- **45** `CvDLLPythonIFaceBase::pythonUsingDefaultImpl()` (virtual; pure virtual, provided by the exe)
  - called by (18): CvGame::assignStartingPlots, CvGame::normalizeStartingPlots, CvGame::pythonIsBonusIgnoreLatitudes, CvMap::reset, CvMapGenerator::addBonuses, CvMapGenerator::addFeatures, CvMapGenerator::addGoodies, CvMapGenerator::addLakes, CvMapGenerator::addRivers, CvMapGenerator::canPlaceBonusAt, CvMapGenerator::canPlaceGoodyAt, CvMapGenerator::doRiver …
- **48** `CvDLLPythonIFaceBase::makePythonObject(T *)`
  - called by (82): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool), CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCityAI::AI_chooseProduction …
- **65** `CvDLLPythonIFaceBase::setSeqFromArray(const T *, int, PyObject *)`
- **97** `CvDLLPythonIFaceBase::putSeqInArray(PyObject *, T **)`
  - called by (5): CyCity::setWallOverridePoints, CyMapGenerator::setPlotTypes, CyMessageControl::sendUpdateCivics, CyPlayer::getCivicAnarchyLength, CyPlayer::getCivicUpkeep
- **122** `CvDLLPythonIFaceBase::putFloatSeqInArray(PyObject *, T **)`
- **147** `CvDLLPythonIFaceBase::putStringSeqInArray(PyObject *, T **)`
