# AIDiplomacyPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **13** `AIDiplomacyPolicy::goldForValueGap(int, int, bool)`
  - called by (3): CvPlayerAI::AI_counterPropose, CvPlayerAI::AI_doDiplo, CvPlayerAI::AI_doPeace
- **30** `AIDiplomacyPolicy::valueFromGold(int, int)`
  - called by (8): AIDiplomacyPolicy::goldPerTurnCostVal, CvPlayerAI::AI_counterPropose, CvPlayerAI::AI_dealVal, CvPlayerAI::AI_doDiplo, CvPlayerAI::AI_doPeace, CvPlayerAI::AI_goldPerTurnTradeVal, CvPlayerAI::AI_tradeGiveVal, CvPlayerAI::AI_tradeReservationVal
- **44** `AIDiplomacyPolicy::scaleByRatio(int, int, int)`
  - called by (3): CvPlayerAI::AI_considerOffer, CvPlayerAI::AI_getStrategyHash, CvTeamAI::AI_endWarVal
- **52** `AIDiplomacyPolicy::saturatingAdd(int, int)`
  - called by (4): CvPlayerAI::AI_counterPropose, CvPlayerAI::AI_dealVal, CvPlayerAI::AI_doDiplo, CvPlayerAI::AI_doPeace
- **62** `AIDiplomacyPolicy::goldPerTurnCostVal(int, int, int, int, int, int)`
  - calls: AIDiplomacyPolicy::valueFromGold
  - called by (2): AIDiplomacyPolicy::maxAffordableGoldPerTurn, CvPlayerAI::AI_goldPerTurnCostVal
- **83** `AIDiplomacyPolicy::maxAffordableGoldPerTurn(int, int, int, int, int, int, int, bool)`
  - calls: AIDiplomacyPolicy::goldPerTurnCostVal
  - called by (2): CvPlayerAI::AI_counterPropose, CvPlayerAI::AI_doDiplo
- **109** `AIDiplomacyPolicy::scaleByRatio64(__int64, __int64, __int64)`
  - called by (6): CvTeamAI::AI_declareWarTradeVal, CvTeamAI::AI_endWarVal, CvTeamAI::AI_getBarbarianCivWarVal, CvTeamAI::AI_minorKeepWarVal, CvTeamAI::AI_startWarVal, CvTeamAI::AI_surrenderTrade
- **117** `AIDiplomacyPolicy::powerRatioPercent(int, int)`
  - called by (2): CvCityAI::AI_cityThreat, CvPlayerAI::AI_conquerCity
- **126** `AIDiplomacyPolicy::isWeightedGreater(__int64, __int64, __int64, __int64)`
  - called by (4): CvPlayerAI::AI_conquerCity, CvPlayerAI::AI_considerOffer, CvPlayerAI::AI_getConquestVictoryStage, CvTeamAI::AI_surrenderTrade
- **134** `AIDiplomacyPolicy::resourceReservationVal(int, int, int)`
  - called by (1): CvPlayerAI::AI_resourceReservationVal
