# CvPlot.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **250** `CvPlot::getX_INLINE() const`
  - called by (329): CvCity::applyEvent, CvCity::init, CvCity::kill, CvCity::popOrder, CvCity::setRallyPlot, CvCityAI::AI_bestPlotBuild, CvDLLButtonPopup::launchEventPopup, CvDLLWidgetData::parseActionHelp, CvGame::createAnimals, CvGame::createBarbarianCities, CvGame::createBarbarianUnits, CvGame::doGlobalWarming …
- **257** `CvPlot::getY_INLINE() const`
  - called by (329): CvCity::applyEvent, CvCity::init, CvCity::kill, CvCity::popOrder, CvCity::setRallyPlot, CvCityAI::AI_bestPlotBuild, CvDLLButtonPopup::launchEventPopup, CvDLLWidgetData::parseActionHelp, CvGame::createAnimals, CvGame::createBarbarianCities, CvGame::createBarbarianUnits, CvGame::doGlobalWarming …
- **345** `CvPlot::getOwnerINLINE() const`
  - called by (133): CvCity::alterWorkingPlot, CvCity::applyEvent, CvCity::canApplyEvent, CvCity::cultureStrength, CvCityAI::AI_calculateCulturePressure, CvCityAI::AI_countNumBonuses, CvCityAI::AI_countNumImprovableBonuses, CvCityAI::AI_stealPlots, CvDLLButtonPopup::launchDeclareWarMovePopup, CvDLLButtonPopup::launchDoEspionagePopup, CvDLLButtonPopup::launchDoEspionageTargetPopup, CvDLLWidgetData::parseActionHelp …
- **505** `CvPlot::getPlotBuilder()` (exported)
