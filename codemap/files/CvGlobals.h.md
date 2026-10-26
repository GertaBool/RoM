# CvGlobals.h

Group: game data and XML loading. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **176** `CvGlobals::getMapINLINE()`
  - called by (306): CvArea::calculateTotalBestNatureYield, CvArea::changeBorderObstacleCount, CvArea::changeNumTiles, CvArea::countCoastalLand, CvCity::calculateColonyMaintenanceTimes100, CvCity::calculateCorporationMaintenanceTimes100(CorporationTypes) const, CvCity::calculateDistanceMaintenanceTimes100, CvCity::calculateNumCitiesMaintenanceTimes100, CvCity::doReligion, CvCity::doTask, CvCity::getBaseTradeProfit, CvCity::getCorporationCommerceByCorporation …
- **177** `CvGlobals::getGameINLINE()`
  - called by (802): CvArea::changeCleanPowerCount, CvArea::changeYieldRateModifier, CvCity::applyEvent, CvCity::calculateColonyMaintenanceTimes100, CvCity::canBeSelected, CvCity::canConstruct, CvCity::canPageGraphicsOut, CvCity::changeBonusBadHealth, CvCity::changeBonusGoodHealth, CvCity::changeBonusYieldRateModifier, CvCity::changeBuildingBadHealth, CvCity::changeBuildingGoodHealth …
- **937** `CvGlobals::getDLLIFace()`
  - called by (1346): CvAdvisorInfo::read, CvAnimationPathInfo::read, CvArea::changeCleanPowerCount, CvArea::changeYieldRateModifier, CvArtInfoFeature::read, CvArtInfoUnit::read, CvBonusInfo::read(CvXMLLoadUtility*), CvBuildingInfo::read(CvXMLLoadUtility*), CvCity::applyEvent, CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain …
- **1571** `CvGlobals::getInstance()` (exported; static)
  - called by (3103): AI_isSacrificeWorth, CvActionInfo::getAutomateType, CvActionInfo::getCommandData, CvActionInfo::getCommandType, CvActionInfo::getHotkeyInfo, CvActionInfo::getMissionType, CvActionInfo::isConfirmCommand, CvActionInfo::isVisible, CvAdvisorInfo::read, CvAnimationPathInfo::read, CvArea::calculateTotalBestNatureYield, CvArea::changeBorderObstacleCount …
- **·** `CvGlobals::`vector deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: operator delete(void*) [CvGameCoreDLL.cpp], operator delete[](void*) [CvGameCoreDLL.cpp], CvGlobals::~CvGlobals [CvGlobals.cpp]
  - takes the address of: CvGlobals::~CvGlobals [CvGlobals.cpp]
- **·** `CvRandom::`vector deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: operator delete(void*) [CvGameCoreDLL.cpp], operator delete[](void*) [CvGameCoreDLL.cpp], CvRandom::~CvRandom [CvRandom.cpp]
  - takes the address of: CvRandom::~CvRandom [CvRandom.cpp]
