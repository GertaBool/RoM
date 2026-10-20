# AIProductionChainPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **7** `AIProductionChainPolicy::parallelTechReadinessPercent(int)`
  - called by (1): `anonymous namespace'::AI_buildingTechReadinessPercent
- **16** `AIProductionChainPolicy::readinessPercent(int, bool, bool, bool)`
  - called by (1): `anonymous namespace'::AI_unitReadinessPercent
- **26** `AIProductionChainPolicy::downstreamBuildingValue(int, int, bool)`
  - called by (1): CvPlayerAI::AI_techBuildingValue
