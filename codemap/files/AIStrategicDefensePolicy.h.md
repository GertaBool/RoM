# AIStrategicDefensePolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **13** `AIStrategicDefensePolicy::clamp(int, int, int)`
  - called by (2): AIStrategicDefensePolicy::coalitionCanMatchTarget, AIStrategicDefensePolicy::stagedGarrisonDeficit
- **20** `AIStrategicDefensePolicy::stagedGarrisonDeficit(int, int, int)`
  - calls: AIStrategicDefensePolicy::clamp
  - called by (1): CvCityAI::AI_neededDefenders
- **37** `AIStrategicDefensePolicy::shouldCancelOpenBordersForStaging(int, int, bool, bool, bool)`
  - called by (1): CvPlayerAI::AI_doDiplo
- **49** `AIStrategicDefensePolicy::isHegemonThreat(__int64, __int64, __int64, __int64, int, bool)`
  - called by (1): CvTeamAI::AI_doWar
- **60** `AIStrategicDefensePolicy::coalitionCanMatchTarget(__int64, __int64, int)`
  - calls: AIStrategicDefensePolicy::clamp
  - called by (1): CvTeamAI::AI_doWar
- **70** `AIStrategicDefensePolicy::defensiveCounterstrokeAllowed(int, int, int)`
  - called by (1): CvTeamAI::AI_calculateAreaAIType
