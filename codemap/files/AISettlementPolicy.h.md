# AISettlementPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **14** `AISettlementPolicy::Candidate::Candidate(int, int)`
  - called by (1): CvPlayerAI::AI_updateFoundValues
- **16** `AISettlementPolicy::Candidate::operator<(struct AISettlementPolicy::Candidate const &) const`
- **22** `AISettlementPolicy::scaleRatio(int, int, int)`
  - called by (2): AISettlementPolicy::deliveryValue, AISettlementPolicy::portfolioValue
- **36** `AISettlementPolicy::portfolioSize(int, int)`
  - called by (1): CvPlayerAI::AI_updateFoundValues
- **44** `AISettlementPolicy::portfolioValue(int, int, int)`
  - calls: AISettlementPolicy::scaleRatio
  - called by (1): CvPlayerAI::AI_updateCitySites
- **56** `AISettlementPolicy::deliveryValue(int, int, int)`
  - calls: AISettlementPolicy::scaleRatio
  - called by (2): CvUnitAI::AI_found, CvUnitAI::AI_settlerSeaTransport
- **70** `AISettlementPolicy::warFoundThresholdPercent(bool, int, int)`
  - called by (1): CvPlayerAI::AI_getMinFoundValue
