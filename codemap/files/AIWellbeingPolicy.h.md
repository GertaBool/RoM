# AIWellbeingPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **7** `AIWellbeingPolicy::clamp(int, int, int)`
  - called by (4): AIWellbeingPolicy::happinessMarginal, AIWellbeingPolicy::happinessPotential, AIWellbeingPolicy::healthMarginal, AIWellbeingPolicy::healthPotential
- **12** `AIWellbeingPolicy::happinessPotential(int)`
  - calls: AIWellbeingPolicy::clamp
  - called by (1): AIWellbeingPolicy::happinessMarginal
- **21** `AIWellbeingPolicy::healthPotential(int)`
  - calls: AIWellbeingPolicy::clamp
  - called by (1): AIWellbeingPolicy::healthMarginal
- **30** `AIWellbeingPolicy::happinessMarginal(int, int)`
  - calls: AIWellbeingPolicy::happinessPotential, AIWellbeingPolicy::clamp
  - called by (1): CvPlayerAI::AI_getHappinessWeight
- **36** `AIWellbeingPolicy::healthMarginal(int, int)`
  - calls: AIWellbeingPolicy::healthPotential, AIWellbeingPolicy::clamp
  - called by (1): CvPlayerAI::AI_getHealthWeight
