# CvTeamAI.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **20** `CvTeamAI::getTeam(TeamTypes)` (static)
  - called by (526): AI_buildingTechReadinessPercent, AI_hasBuildingTechs, CvArea::changeCleanPowerCount, CvCity::calculateNumCitiesMaintenanceTimes100, CvCity::canWork, CvCity::getAdditionalBaseCommerceRateByBuildingImpl, CvCity::getAdditionalBaseGreatPeopleRateByBuilding, CvCity::getAdditionalBaseYieldRateByBuilding, CvCity::getAdditionalCommerceRateModifierByBuildingImpl, CvCity::getAdditionalGreatPeopleRateModifierByBuilding, CvCity::getAdditionalYieldRateModifierByBuilding, CvCity::getLiberationPlayer …
