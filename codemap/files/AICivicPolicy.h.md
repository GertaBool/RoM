# AICivicPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **12** `AICivicPolicy::recurringUnitCostPerTurn(const int, const int, const int, const int, const int, const int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **31** `AICivicPolicy::scaleCostPercent(const int, const int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **40** `AICivicPolicy::freeExperienceValuePerTurn(const int, const int, const int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **53** `AICivicPolicy::applyPenalty(const int, const int)`
  - called by (1): CvPlayerAI::AI_civicValue
- **63** `AICivicPolicy::shouldSwitch(const long long, const long long, const int, const int, const int)`
  - called by (1): CvPlayerAI::AI_doCivics
