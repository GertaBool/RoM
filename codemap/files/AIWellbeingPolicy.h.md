# AIWellbeingPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **6** `AIWellbeingPolicy::clamp(const int, const int, const int)`
  - called by (4): AIWellbeingPolicy::happinessMarginal, AIWellbeingPolicy::happinessPotential, AIWellbeingPolicy::healthMarginal, AIWellbeingPolicy::healthPotential
- **11** `AIWellbeingPolicy::happinessPotential(const int)`
  - calls: AIWellbeingPolicy::clamp
  - called by (1): AIWellbeingPolicy::happinessMarginal
- **20** `AIWellbeingPolicy::healthPotential(const int)`
  - calls: AIWellbeingPolicy::clamp
  - called by (1): AIWellbeingPolicy::healthMarginal
- **29** `AIWellbeingPolicy::happinessMarginal(const int, const int)`
  - calls: AIWellbeingPolicy::clamp, AIWellbeingPolicy::happinessPotential
  - called by (1): CvPlayerAI::AI_getHappinessWeight
- **35** `AIWellbeingPolicy::healthMarginal(const int, const int)`
  - calls: AIWellbeingPolicy::clamp, AIWellbeingPolicy::healthPotential
  - called by (1): CvPlayerAI::AI_getHealthWeight
