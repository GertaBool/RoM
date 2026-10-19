# CvMap.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **24** `coordRange(int, int, bool)`
  - called by (1): CvMap::plotINLINE
- **58** `CvMapInitData::CvMapInitData(int, int, int, int, bool, bool)`
  - called by (3): CvMap::CvMap, CvMap::read, CvMap::rebuild
- **125** `CvMap::isPlotINLINE(int, int)`
  - calls: CvMap::getGridWidthINLINE, CvMap::getGridHeightINLINE
  - called by (3): CvMap::isPlot, CvMap::plotINLINE, CyMap::isPlot
- **132** `CvMap::numPlotsINLINE()`
  - calls: CvMap::getGridWidthINLINE, CvMap::getGridHeightINLINE
  - called by (114): CvArea::calculateTotalBestNatureYield, CvArea::countCoastalLand, CvDeal::startTrade, CvGame::assignStartingPlots, CvGame::circumnavigationAvailable, CvGame::createBarbarianCities, CvGame::doGlobalWarming, CvGame::doTurn, CvGame::drawBattleEffects, CvGame::foundBarbarianCity, CvGame::initScoreCalculation, CvGame::normalizeAddRiver …
- **139** `CvMap::plotNumINLINE(int, int)`
  - calls: CvMap::getGridWidthINLINE
  - called by (12): CvMap::plotINLINE, CvMap::plotNum, CvMap::plotSorenINLINE, CvPlayer::getReligionLayerColors, CvPlayerAI::AI_canDeliverSettler, CvPlayerAI::AI_isPlotCitySite, CvPlayerAI::AI_isSettleSiteDeliverable, CvPlayerAI::AI_plotTargetMissionAIs(CvPlot *, MissionAITypes *, int, int &, CvSelectionGroup *, int), CvPlayerAI::AI_updateSettleReach, CvUnitAI::AI_pirateBlockade, CyMap::plotNum, MissionTargetMap::plotIndex
- **161** `CvMap::getGridWidthINLINE()`
  - called by (30): CvMap::getGridWidth, CvMap::getWidthCoords, CvMap::init, CvMap::isPlotINLINE, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::numPlotsINLINE, CvMap::plotByIndexINLINE, CvMap::plotINLINE, CvMap::plotNumINLINE, CvMap::plotX, CvMap::plotXToPointX …
- **168** `CvMap::getGridHeightINLINE()`
  - called by (27): CvMap::getGridHeight, CvMap::getHeightCoords, CvMap::init, CvMap::isPlotINLINE, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::numPlotsINLINE, CvMap::plotByIndexINLINE, CvMap::plotINLINE, CvMap::plotYToPointY, CvMap::pointYToPlotY, CvMap::setup …
- **187** `CvMap::isWrapXINLINE()`
  - called by (17): CvGame::circumnavigationAvailable, CvMap::getMapFractalFlags, CvMap::isWrapX, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::plotINLINE, CvMap::setup, CvPlot::calculatePathDistanceToPlot, CvPlot::getLatitudeMinutes, CvPlot::getLongitudeMinutes, CvPlot::isHasPathToEnemyCity, CvPlot::isHasPathToPlayerCity …
- **194** `CvMap::isWrapYINLINE()`
  - called by (17): CvGame::circumnavigationAvailable, CvMap::getMapFractalFlags, CvMap::isWrapY, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::plotINLINE, CvMap::setup, CvPlot::calculatePathDistanceToPlot, CvPlot::getLatitudeMinutes, CvPlot::getLongitudeMinutes, CvPlot::isHasPathToEnemyCity, CvPlot::isHasPathToPlayerCity …
- **201** `CvMap::isWrapINLINE()`
  - called by (1): CvMap::isWrap
- **221** `CvMap::plotByIndexINLINE(int)`
  - calls: CvMap::getGridWidthINLINE, CvMap::getGridHeightINLINE
  - called by (107): CvArea::calculateTotalBestNatureYield, CvArea::countCoastalLand, CvDLLButtonPopup::launchMainMenuPopup, CvDeal::startTrade, CvGame::assignStartingPlots, CvGame::createBarbarianCities, CvGame::doGlobalWarming, CvGame::doTurn, CvGame::drawBattleEffects, CvGame::foundBarbarianCity, CvGame::initScoreCalculation, CvGame::normalizeAddRiver …
- **228** `CvMap::plotINLINE(int, int)`
  - calls: coordRange, CvMap::getGridWidthINLINE, CvMap::isWrapXINLINE, CvMap::getGridHeightINLINE, CvMap::isWrapYINLINE, CvMap::isPlotINLINE, CvMap::plotNumINLINE
  - called by (61): CvCity::doTask, CvCity::init, CvDLLButtonPopup::launchDeclareWarMovePopup, CvDLLWidgetData::doGotoTurnEvent, CvGame::applyFlyoutMenu, CvGameTextMgr::setPlotListHelp, CvMap::findCity, CvMap::plot, CvMap::pointToPlot, CvMapGenerator::canPlaceBonusAt, CvMapGenerator::canPlaceGoodyAt, CvPlayer::applyEvent …
- **238** `CvMap::plotSorenINLINE(int, int)`
  - calls: CvMap::plotNumINLINE
  - called by (35): CvCity::getRallyPlot, CvCity::plot, CvMap::combinePlotGroups, CvMap::init, CvMap::syncRandPlot, CvPlayer::getStartingPlot, CvPlayerAI::AI_advancedStartDoRoute, CvPlot::calculateImprovementYieldChange, CvPlot::getInlandCorner, CvPlotGroup::changeNumBonuses, CvPlotGroup::recalculatePlots, CvPlotGroup::removePlot …
