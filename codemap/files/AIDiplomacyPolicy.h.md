# AIDiplomacyPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **12** `AIDiplomacyPolicy::goldForValueGap(int, int, bool)`
  - called by (3): CvPlayerAI::AI_counterPropose, CvPlayerAI::AI_doDiplo, CvPlayerAI::AI_doPeace
- **29** `AIDiplomacyPolicy::valueFromGold(int, int)`
  - called by (3): CvPlayerAI::AI_counterPropose, CvPlayerAI::AI_doDiplo, CvPlayerAI::AI_doPeace
- **43** `AIDiplomacyPolicy::scaleByRatio(int, int, int)`
  - called by (4): CvPlayerAI::AI_considerOffer, CvPlayerAI::AI_getStrategyHash, CvTeamAI::AI_endWarVal, CvTeamAI::AI_surrenderTrade
- **51** `AIDiplomacyPolicy::saturatingAdd(int, int)`
  - called by (2): CvPlayerAI::AI_counterPropose, CvPlayerAI::AI_doPeace
