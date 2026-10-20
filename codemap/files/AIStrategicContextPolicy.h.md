# AIStrategicContextPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **11** `AIStrategicContextPolicy::clamp(int, int, int)`
  - called by (1): AIStrategicContextPolicy::usefulForeignTradeCities
- **54** `AIStrategicContextPolicy::Snapshot::Snapshot()`
  - called by (6): CvPlayerAI::AI_doTurnPre, CvPlayerAI::AI_getStrategicContext, CvPlayerAI::AI_reset, CvPlayerAI::AI_updateAgenda, CvPlayerAI::CvPlayerAI, CvPlayerAI::read
- **58** `AIStrategicContextPolicy::isCurrent(AIStrategicContextPolicy::Snapshot const&, int, int)`
  - called by (1): CvPlayerAI::AI_getStrategicContext
- **65** `AIStrategicContextPolicy::saturatingAdd(int, int)`
  - called by (1): CvPlayerAI::AI_getStrategicContext
- **74** `AIStrategicContextPolicy::goldRunway(int, int)`
  - called by (1): CvPlayerAI::AI_getStrategicContext
- **86** `AIStrategicContextPolicy::usefulForeignTradeCities(int, int)`
  - calls: AIStrategicContextPolicy::clamp
  - called by (1): CvPlayerAI::AI_getStrategicContext
