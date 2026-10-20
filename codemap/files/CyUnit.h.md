# CyUnit.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **23** `CyUnit::getUnit()`
  - called by (33): CyCity::addProductionExperience, CyCity::isBombardable, CyGameTextMgr::getSpecificUnitHelp, CyPlayer::canReceiveGoody, CyPlayer::doEspionageMission, CyPlayer::doGoody, CyPlayer::receiveGoody, CyPlot::getBestDefender, CyPlot::getNumVisibleEnemyDefenders, CyPlot::getNumVisiblePotentialEnemyDefenders, CyPlot::isEnemyCity, CyPlot::isFriendlyCity …
- **25** `CyUnit::isNone()` (Python: isNone)
  - called by (1): CyUnitPythonInterface1
