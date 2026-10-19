# CyCity.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **24** `CyCity::getCity()`
  - called by (22): CyCity::calculateTradeProfit, CyCity::isConnectedTo, CyGame::cityPushOrder, CyGame::setHeadquarters, CyGame::setHolyCity, CyGameTextMgr::getBuildingHelp, CyGameTextMgr::getCorporationHelpCity, CyGameTextMgr::getProjectHelp, CyGameTextMgr::getReligionHelpCity, CyGameTextMgr::getUnitHelp, CyMap::findCity, CyPlayer::acquireCity …
- **25** `CyCity::isNone()` (Python: isNone)
  - called by (1): CyCityPythonInterface1
