# AISettlementPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **14** `AISettlementPolicy::Candidate::Candidate(int, int)`
  - called by (1): CvPlayerAI::AI_updateFoundValues
- **15** `AISettlementPolicy::Candidate::operator<(const Candidate &)`
- **21** `AISettlementPolicy::scaleRatio(const int, const int, const int)`
  - called by (2): AISettlementPolicy::deliveryValue, AISettlementPolicy::portfolioValue
- **35** `AISettlementPolicy::portfolioSize(const int, const int)`
  - called by (1): CvPlayerAI::AI_updateFoundValues
- **42** `AISettlementPolicy::portfolioValue(const int, const int, const int)`
  - calls: AISettlementPolicy::scaleRatio
  - called by (1): CvPlayerAI::AI_updateCitySites
- **54** `AISettlementPolicy::deliveryValue(const int, const int, const int)`
  - calls: AISettlementPolicy::scaleRatio
  - called by (2): CvUnitAI::AI_found, CvUnitAI::AI_settlerSeaTransport
- **68** `AISettlementPolicy::warFoundThresholdPercent(const bool, const int, const int)`
  - called by (1): CvPlayerAI::AI_getMinFoundValue
