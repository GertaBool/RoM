# CvDLLFAStarIFaceBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **21** `CvDLLFAStarIFaceBase::create(…)` (virtual; pure virtual, provided by the exe)
  - called by (5): CvPlot::calculatePathDistanceToPlot, CvPlot::isHasPathToEnemyCity, CvPlot::isHasPathToPlayerCity, CvPlot::updateIrrigated, CvSelectionGroup::initSecondaryPathFinder
- **22** `CvDLLFAStarIFaceBase::destroy(…)` (virtual; pure virtual, provided by the exe)
  - called by (5): CvPlot::calculatePathDistanceToPlot, CvPlot::isHasPathToEnemyCity, CvPlot::isHasPathToPlayerCity, CvPlot::updateIrrigated, CvSelectionGroup::releaseSecondaryPathFinder
- **23** `CvDLLFAStarIFaceBase::GeneratePath(…)` (virtual; pure virtual, provided by the exe)
  - called by (13): CvCityAI::AI_updateRouteToCity, CvGame::startFlyoutMenu, CvMap::calculateAreas, CvMap::calculatePathDistance, CvPlayer::countUnimprovedBonuses, CvPlayerAI::AI_advancedStartDoRoute, CvPlot::calculatePathDistanceToPlot, CvPlot::isHasPathToEnemyCity, CvPlot::isHasPathToPlayerCity, CvPlot::updateIrrigated, CvPlotGroup::recalculatePlots, CvUnitAI::AI_solveBlockageProblem …
- **24** `CvDLLFAStarIFaceBase::Initialize(…)` (virtual; pure virtual, provided by the exe)
  - called by (6): CvMap::setup, CvPlot::calculatePathDistanceToPlot, CvPlot::isHasPathToEnemyCity, CvPlot::isHasPathToPlayerCity, CvPlot::updateIrrigated, CvSelectionGroup::initSecondaryPathFinder
- **25** `CvDLLFAStarIFaceBase::SetData(…)` (virtual; pure virtual, provided by the exe)
  - called by (6): CvGame::startFlyoutMenu, CvPlot::calculatePathDistanceToPlot, CvPlot::isHasPathToEnemyCity, CvPlot::isHasPathToPlayerCity, CvPlotGroup::recalculatePlots, `anonymous namespace'::generatePathOn
- **26** `CvDLLFAStarIFaceBase::GetLastNode(…)` (virtual; pure virtual, provided by the exe)
  - called by (7): CvGame::startFlyoutMenu, CvMap::calculatePathDistance, CvPlayerAI::AI_advancedStartDoRoute, CvPlot::calculatePathDistanceToPlot, CvSelectionGroup::getPathLastNode, CvUnitAI::AI_solveBlockageProblem, `anonymous namespace'::generatePathOn
- **28** `CvDLLFAStarIFaceBase::IsPathDest(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): pathCost
- **29** `CvDLLFAStarIFaceBase::GetStartX(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): stepDestValid
- **30** `CvDLLFAStarIFaceBase::GetStartY(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): stepDestValid
- **33** `CvDLLFAStarIFaceBase::GetInfo(…)` (virtual; pure virtual, provided by the exe)
  - called by (8): borderValid, joinArea, pathAdd, pathCost, pathDestValid, pathValid, plotGroupValid, routeValid
- **34** `CvDLLFAStarIFaceBase::ForceReset(…)` (virtual; pure virtual, provided by the exe)
  - called by (7): CvCityAI::AI_updateRouteToCity, CvMap::resetPathDistance, CvPlayer::countUnimprovedBonuses, CvPlayer::doTurnUnits, CvPlayerAI::AI_advancedStartDoRoute, CvSelectionGroup::resetPath, CvUnit::setMoves
