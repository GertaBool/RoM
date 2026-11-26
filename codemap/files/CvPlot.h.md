# CvPlot.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **63** `CvPlot::isGraphicsPagedOut() const`
  - called by (1): CvGame::pageGraphics
- **71** `CvPlot::isRevealedGraphicsDirty() const`
  - called by (2): CvGame::deferRevealedGraphics, CvGame::processDeferredReveals
- **72** `CvPlot::isRevealedRouteDirty() const`
  - called by (1): CvGame::processDeferredReveals
- **73** `CvPlot::setRevealedGraphicsDirty(bool)`
  - called by (1): CvGame::deferRevealedGraphics
- **263** `CvPlot::getX_INLINE() const`
  - called by (335): CvCity::applyEvent, CvCity::init, CvCity::kill, CvCity::popOrder, CvCity::setRallyPlot, CvCityAI::AI_bestPlotBuild, CvDLLButtonPopup::launchEventPopup, CvDLLWidgetData::parseActionHelp, CvGame::createAnimals, CvGame::createBarbarianCities, CvGame::createBarbarianUnits, CvGame::deferRevealedGraphics …
- **270** `CvPlot::getY_INLINE() const`
  - called by (335): CvCity::applyEvent, CvCity::init, CvCity::kill, CvCity::popOrder, CvCity::setRallyPlot, CvCityAI::AI_bestPlotBuild, CvDLLButtonPopup::launchEventPopup, CvDLLWidgetData::parseActionHelp, CvGame::createAnimals, CvGame::createBarbarianCities, CvGame::createBarbarianUnits, CvGame::deferRevealedGraphics …
- **358** `CvPlot::getOwnerINLINE() const`
  - called by (135): CvCity::alterWorkingPlot, CvCity::applyEvent, CvCity::canApplyEvent, CvCity::cultureStrength, CvCityAI::AI_calculateCulturePressure, CvCityAI::AI_countNumBonuses, CvCityAI::AI_countNumImprovableBonuses, CvCityAI::AI_stealPlots, CvDLLButtonPopup::launchDeclareWarMovePopup, CvDLLButtonPopup::launchDoEspionagePopup, CvDLLButtonPopup::launchDoEspionageTargetPopup, CvDLLWidgetData::parseActionHelp …
- **519** `CvPlot::getPlotBuilder()` (exported)
