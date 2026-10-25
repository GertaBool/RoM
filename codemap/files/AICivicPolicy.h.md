# AICivicPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **15** `AICivicPolicy::recurringUnitCostPerTurn(int, int, int, int, int, int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **32** `AICivicPolicy::scaleCostPercent(int, int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **42** `AICivicPolicy::freeExperienceValuePerTurn(int, int, int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **54** `AICivicPolicy::applyPenalty(int, int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **65** `AICivicPolicy::shouldSwitch(__int64, __int64, int, int, int)`
  - called by (1): CvPlayerAI::AI_doCivics
