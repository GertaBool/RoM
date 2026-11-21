# CvPlayerAI.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **129** `CvPlayerAI::getPlayer(PlayerTypes)` (static)
  - called by (1040): CvArea::changeBuildingBadHealth, CvArea::changeBuildingGoodHealth, CvArea::changeBuildingHappiness, CvArea::changeFreeSpecialist, CvArea::changeYieldRateModifier, CvArea::countHasCorporation, CvArea::countHasReligion, CvCity::applyEvent, CvCity::badHealth, CvCity::calculateColonyMaintenanceTimes100, CvCity::calculateCorporationMaintenanceTimes100(CorporationTypes) const, CvCity::calculateDistanceMaintenanceTimes100 …
