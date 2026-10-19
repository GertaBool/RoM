# AIProductionChainPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **6** `AIProductionChainPolicy::parallelTechReadinessPercent(const int)`
  - called by (1): AI_buildingTechReadinessPercent
- **14** `AIProductionChainPolicy::readinessPercent(const int, const bool, const bool, const bool)`
  - called by (1): AI_unitReadinessPercent
- **24** `AIProductionChainPolicy::downstreamBuildingValue(const int, const int, const bool)`
  - called by (1): CvPlayerAI::AI_techBuildingValue
