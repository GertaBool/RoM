# CvMap.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **25** `coordRange(int, int, bool)`
  - called by (1): CvMap::plotINLINE
- **60** `CvMapInitData::CvMapInitData(int, int, int, int, bool, bool)`
  - called by (3): CvMap::CvMap, CvMap::read, CvMap::rebuild
- **126** `CvMap::isPlotINLINE(int, int) const`
  - calls: CvMap::getGridWidthINLINE, CvMap::getGridHeightINLINE
  - called by (3): CvMap::isPlot, CvMap::plotINLINE, CyMap::isPlot
- **133** `CvMap::numPlotsINLINE() const`
  - calls: CvMap::getGridWidthINLINE, CvMap::getGridHeightINLINE
  - called by (116): CvArea::calculateTotalBestNatureYield, CvArea::countCoastalLand, CvDeal::startTrade, CvGame::assignStartingPlots, CvGame::circumnavigationAvailable, CvGame::createBarbarianCities, CvGame::doGlobalWarming, CvGame::doTurn, CvGame::drawBattleEffects, CvGame::foundBarbarianCity, CvGame::initScoreCalculation, CvGame::normalizeAddRiver …
- **140** `CvMap::plotNumINLINE(int, int) const`
  - calls: CvMap::getGridWidthINLINE
  - called by (13): CvGame::deferRevealedGraphics, CvMap::plotINLINE, CvMap::plotNum, CvMap::plotSorenINLINE, CvPlayer::getReligionLayerColors, CvPlayerAI::AI_canDeliverSettler, CvPlayerAI::AI_isPlotCitySite, CvPlayerAI::AI_isSettleSiteDeliverable, CvPlayerAI::AI_plotTargetMissionAIs(CvPlot*, MissionAITypes*, int, int&, CvSelectionGroup*, int) const, CvPlayerAI::AI_updateSettleReach, CvUnitAI::AI_pirateBlockade, CyMap::plotNum …
- **162** `CvMap::getGridWidthINLINE() const`
  - called by (32): CvGame::graphicsWindowFromCamera, CvGame::pageGraphics, CvMap::getGridWidth, CvMap::getWidthCoords, CvMap::init, CvMap::isPlotINLINE, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::numPlotsINLINE, CvMap::plotByIndexINLINE, CvMap::plotINLINE, CvMap::plotNumINLINE …
- **169** `CvMap::getGridHeightINLINE() const`
  - called by (29): CvGame::graphicsWindowFromCamera, CvGame::pageGraphics, CvMap::getGridHeight, CvMap::getHeightCoords, CvMap::init, CvMap::isPlotINLINE, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::numPlotsINLINE, CvMap::plotByIndexINLINE, CvMap::plotINLINE, CvMap::plotYToPointY …
- **188** `CvMap::isWrapXINLINE() const`
  - called by (18): CvGame::circumnavigationAvailable, CvGame::pageGraphics, CvMap::getMapFractalFlags, CvMap::isWrapX, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::plotINLINE, CvMap::setup, CvPlot::calculatePathDistanceToPlot, CvPlot::getLatitudeMinutes, CvPlot::getLongitudeMinutes, CvPlot::isHasPathToEnemyCity …
- **195** `CvMap::isWrapYINLINE() const`
  - called by (18): CvGame::circumnavigationAvailable, CvGame::pageGraphics, CvMap::getMapFractalFlags, CvMap::isWrapY, CvMap::maxPlotDistance, CvMap::maxStepDistance, CvMap::plotINLINE, CvMap::setup, CvPlot::calculatePathDistanceToPlot, CvPlot::getLatitudeMinutes, CvPlot::getLongitudeMinutes, CvPlot::isHasPathToEnemyCity …
- **202** `CvMap::isWrapINLINE() const`
  - called by (1): CvMap::isWrap
- **222** `CvMap::plotByIndexINLINE(int) const`
  - calls: CvMap::getGridWidthINLINE, CvMap::getGridHeightINLINE
  - called by (109): CvArea::calculateTotalBestNatureYield, CvArea::countCoastalLand, CvDLLButtonPopup::launchMainMenuPopup, CvDeal::startTrade, CvGame::assignStartingPlots, CvGame::createBarbarianCities, CvGame::doGlobalWarming, CvGame::doTurn, CvGame::drawBattleEffects, CvGame::foundBarbarianCity, CvGame::initScoreCalculation, CvGame::normalizeAddRiver …
- **229** `CvMap::plotINLINE(int, int) const`
  - calls: CvMap::getGridWidthINLINE, CvMap::isWrapXINLINE, coordRange, CvMap::getGridHeightINLINE, CvMap::isWrapYINLINE, CvMap::isPlotINLINE, CvMap::plotNumINLINE
  - called by (62): CvCity::doTask, CvCity::init, CvDLLButtonPopup::launchDeclareWarMovePopup, CvDLLWidgetData::doGotoTurnEvent, CvGame::applyFlyoutMenu, CvGame::pageGraphics, CvGameTextMgr::setPlotListHelp, CvMap::findCity, CvMap::plot, CvMap::pointToPlot, CvMapGenerator::canPlaceBonusAt, CvMapGenerator::canPlaceGoodyAt …
- **239** `CvMap::plotSorenINLINE(int, int) const`
  - calls: CvMap::plotNumINLINE
  - called by (35): CvCity::getRallyPlot, CvCity::plot, CvMap::combinePlotGroups, CvMap::init, CvMap::syncRandPlot, CvPlayer::getStartingPlot, CvPlayerAI::AI_advancedStartDoRoute, CvPlot::calculateImprovementYieldChange, CvPlot::getInlandCorner, CvPlotGroup::changeNumBonuses, CvPlotGroup::recalculatePlots, CvPlotGroup::removePlot …
- **·** `CvMap::`vector deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: operator delete(void*) \[CvGameCoreDLL.cpp\], operator delete\[\](void*) \[CvGameCoreDLL.cpp\], CvMap::~CvMap \[CvMap.cpp\]
  - takes the address of: CvMap::~CvMap \[CvMap.cpp\]
