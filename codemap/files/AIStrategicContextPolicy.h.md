# AIStrategicContextPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **10** `AIStrategicContextPolicy::clamp(int, int, int)`
  - called by (1): AIStrategicContextPolicy::usefulForeignTradeCities
- **18** `AIStrategicContextPolicy::Snapshot::operator=(const Snapshot &)`
  - called by (5): CvPlayerAI::AI_doTurnPre, CvPlayerAI::AI_getStrategicContext, CvPlayerAI::AI_reset, CvPlayerAI::AI_updateAgenda, CvPlayerAI::read
- **48** `AIStrategicContextPolicy::Snapshot::Snapshot()`
  - called by (5): CvPlayerAI::AI_doTurnPre, CvPlayerAI::AI_getStrategicContext, CvPlayerAI::AI_reset, CvPlayerAI::AI_updateAgenda, CvPlayerAI::read
- **57** `AIStrategicContextPolicy::isCurrent(const Snapshot &, int, int)`
  - called by (1): CvPlayerAI::AI_getStrategicContext
- **64** `AIStrategicContextPolicy::saturatingAdd(int, int)`
  - called by (1): CvPlayerAI::AI_getStrategicContext
- **73** `AIStrategicContextPolicy::goldRunway(int, int)`
  - called by (1): CvPlayerAI::AI_getStrategicContext
- **85** `AIStrategicContextPolicy::usefulForeignTradeCities(int, int)`
  - calls: AIStrategicContextPolicy::clamp
  - called by (1): CvPlayerAI::AI_getStrategicContext
