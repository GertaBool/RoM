# CyPlot.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **20** `CyPlot::getPlot()`
  - called by (108): CyCity::atPlot, CyCity::canWork, CyCity::getCityPlotIndex, CyCity::isWorkingPlot, CyGame::cyclePlotUnits, CyGame::selectionListMove, CyMap::calculatePathDistance, CyMap::findWater, CyMapGenerator::doRiver, CyPlayer::canBuild, CyPlayer::canDoEspionageMission, CyPlayer::canReceiveGoody …
- **21** `CyPlot::setPlot(CvPlot *)`
  - called by (4): CyMap::sPlot, CyMap::sPlotByIndex, cysPlotCardinalDirection, cysPlotXY
- **22** `CyPlot::isNone()` (Python: isNone)
  - called by (2): CyPlayer::startingPlotWithinRange, CyPlotPythonInterface1
