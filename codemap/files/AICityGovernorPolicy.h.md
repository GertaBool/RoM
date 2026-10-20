# AICityGovernorPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **41** `AICityGovernorPolicy::clamp(int, int, int)`
  - called by (4): AICityGovernorPolicy::performance, AICityGovernorPolicy::prosperity, AICityGovernorPolicy::termLength, AICityGovernorPolicy::utility
- **46** `AICityGovernorPolicy::eligible(int, AICityGovernorPolicy::Context const&)`
  - called by (2): AICityGovernorPolicy::utility, CvCityAI::AI_updateLocalGovernor
- **74** `AICityGovernorPolicy::utility(int, AICityGovernorPolicy::Context const&)`
  - calls: AICityGovernorPolicy::eligible, AICityGovernorPolicy::clamp
  - called by (1): AICityGovernorPolicy::choose
- **101** `AICityGovernorPolicy::choose(AICityGovernorPolicy::Context const&, int)`
  - calls: AICityGovernorPolicy::utility
  - called by (1): CvCityAI::AI_updateLocalGovernor
- **128** `AICityGovernorPolicy::prosperity(AICityGovernorPolicy::Context const&)`
  - calls: AICityGovernorPolicy::clamp
  - called by (1): CvCityAI::AI_updateLocalGovernor
- **135** `AICityGovernorPolicy::termLength(AICityGovernorPolicy::Context const&)`
  - calls: AICityGovernorPolicy::clamp
  - called by (1): CvCityAI::AI_updateLocalGovernor
- **146** `AICityGovernorPolicy::performance(int, int, int, int)`
  - calls: AICityGovernorPolicy::clamp
  - called by (1): CvCityAI::AI_updateLocalGovernor
