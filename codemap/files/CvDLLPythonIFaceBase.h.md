# CvDLLPythonIFaceBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **22** `CvDLLPythonIFaceBase::isInitialized(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvDllPythonEvents::preEvent
- **24** `CvDLLPythonIFaceBase::getMapScriptModule(…)` (virtual; pure virtual, provided by the exe)
  - called by (22): CvGame::assignStartingPlots, CvGame::normalizeStartingPlots, CvGame::pythonIsBonusIgnoreLatitudes, CvMap::init, CvMap::reset, CvMapGenerator::addBonuses, CvMapGenerator::addFeatures, CvMapGenerator::addGoodies, CvMapGenerator::addLakes, CvMapGenerator::addRivers, CvMapGenerator::afterGeneration, CvMapGenerator::canPlaceBonusAt …
- **32** `CvDLLPythonIFaceBase::MakeFunctionArgs(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CyArgsList::makeFunctionArgs
- **35** `CvDLLPythonIFaceBase::callFunction(…)` (virtual; pure virtual, provided by the exe)
  - called by (134): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const, CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCity::getConscriptUnit …
- **45** `CvDLLPythonIFaceBase::pythonUsingDefaultImpl(…)` (virtual; pure virtual, provided by the exe)
  - called by (18): CvGame::assignStartingPlots, CvGame::normalizeStartingPlots, CvGame::pythonIsBonusIgnoreLatitudes, CvMap::reset, CvMapGenerator::addBonuses, CvMapGenerator::addFeatures, CvMapGenerator::addGoodies, CvMapGenerator::addLakes, CvMapGenerator::addRivers, CvMapGenerator::canPlaceBonusAt, CvMapGenerator::canPlaceGoodyAt, CvMapGenerator::doRiver …
- **50** `CvDLLPythonIFaceBase::makePythonObject<struct EventTriggeredData const>(EventTriggeredData const*)`
  - called by (3): CvPlayer::canDoEvent, CvPlayer::checkExpireEvent, CvPlayer::setTriggerFired
- **50** `CvDLLPythonIFaceBase::makePythonObject<struct CombatDetails>(CombatDetails*)`
  - called by (1): CvUnit::resolveCombat
- **50** `CvDLLPythonIFaceBase::makePythonObject<struct EventTriggeredData>(EventTriggeredData*)`
  - called by (3): CvGameTextMgr::setEventHelp, CvPlayer::applyEvent, CvPlayer::initTriggeredData
- **50** `CvDLLPythonIFaceBase::makePythonObject<class CyCity>(CyCity*)`
  - called by (38): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const, CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCityAI::AI_chooseProduction …
- **50** `CvDLLPythonIFaceBase::makePythonObject<class CyPlot>(CyPlot*)`
  - called by (20): CvDllPythonEvents::reportGoodyReceived, CvDllPythonEvents::reportGotoPlotSet, CvDllPythonEvents::reportNukeExplosion, CvDllPythonEvents::reportPlotFeatureRemoved, CvDllPythonEvents::reportPlotPicked, CvDllPythonEvents::reportPlotRevealed, CvDllPythonEvents::reportUnitGifted, CvDllPythonEvents::reportUnitMove, CvDllPythonEvents::reportUnitSetXY, CvGame::canHandleAction, CvGame::getPlotHighlightColor, CvGame::selectionListMove …
- **50** `CvDLLPythonIFaceBase::makePythonObject<class CySelectionGroup>(CySelectionGroup*)`
  - called by (2): CvSelectionGroup::groupAttack, CvSelectionGroup::groupStackAttack
- **50** `CvDLLPythonIFaceBase::makePythonObject<class CyUnit>(CyUnit*)`
  - called by (27): CvDllPythonEvents::reportCombatLogCollateral, CvDllPythonEvents::reportCombatLogFlanking, CvDllPythonEvents::reportCombatResult, CvDllPythonEvents::reportCombatRetreat, CvDllPythonEvents::reportCombatWithdrawal, CvDllPythonEvents::reportGoodyReceived, CvDllPythonEvents::reportGreatPersonBorn, CvDllPythonEvents::reportNukeExplosion, CvDllPythonEvents::reportUnitBuildImprovement, CvDllPythonEvents::reportUnitBuilt, CvDllPythonEvents::reportUnitCaptured, CvDllPythonEvents::reportUnitCreated …
- **99** `CvDLLPythonIFaceBase::putSeqInArray<int>(_object*, int**)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
  - called by (4): CyMapGenerator::setPlotTypes, CyMessageControl::sendUpdateCivics, CyPlayer::getCivicAnarchyLength, CyPlayer::getCivicUpkeep
- **99** `CvDLLPythonIFaceBase::putSeqInArray<float>(_object*, float**)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
  - called by (1): CyCity::setWallOverridePoints
