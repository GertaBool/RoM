# CyArea.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **18** `CyArea::getArea()`
  - called by (20): CyCity::AI_countBestBuilds, CyMap::updateMinOriginalStartDist, CyPlayer::AI_totalAreaUnitAIs, CyPlayer::AI_totalWaterAreaUnitAIs, CyPlayer::AI_unitValue, CyPlayer::countNumCoastalCitiesByArea, CyPlayer::countPotentialForeignTradeCities, CyPlayer::countReligionSpreadUnits, CyPlayer::countUnimprovedBonuses, CyPlot::isAdjacentToArea, CyPlot::isPotentialCityWorkForArea, CySelectionGroup::canEnterArea …
- **19** `CyArea::isNone()` (Python: isNone)
  - called by (1): CyAreaPythonInterface
