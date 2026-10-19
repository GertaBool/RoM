# CvPlayerAI.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **64** `AIOperationData::AIOperationData()`
  - called by (2): CvPlayerAI::AI_updateMilitaryOperations, CvPlayerAI::read
- **90** `AIGeneralCareer::AIGeneralCareer()`
  - called by (3): CvPlayerAI::AI_recordGeneralLoss, CvPlayerAI::AI_rememberGeneral, CvPlayerAI::read
- **90** `AIGeneralCareer::operator=(const AIGeneralCareer &)`
  - called by (1): CvPlayerAI::AI_rememberGeneral
- **99** `AIOperationDeliveryCache::AIOperationDeliveryCache()`
  - called by (1): CvPlayerAI::AI_getOperationRoleTarget
- **128** `CvPlayerAI::getPlayer(PlayerTypes)` (static)
  - called by (1038): CvArea::changeBuildingBadHealth, CvArea::changeBuildingGoodHealth, CvArea::changeBuildingHappiness, CvArea::changeFreeSpecialist, CvArea::changeYieldRateModifier, CvArea::countHasCorporation, CvArea::countHasReligion, CvCity::applyEvent, CvCity::badHealth, CvCity::calculateColonyMaintenanceTimes100, CvCity::calculateCorporationMaintenanceTimes100(CorporationTypes), CvCity::calculateDistanceMaintenanceTimes100 …
- **357** `CvPlayerAI::AI_enemyTargetMissionAIs(TeamTypes, MissionAITypes *, int, CvSelectionGroup *)` (declared, not defined in the source)
- **500** `CvPlayerAI::AI_getTotalCityThreat()` (declared, not defined in the source)
- **501** `CvPlayerAI::AI_getTotalFloatingDefenseNeeded()` (declared, not defined in the source)
