# AICityGovernorPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **40** `AICityGovernorPolicy::clamp(int, int, int)`
  - called by (4): AICityGovernorPolicy::performance, AICityGovernorPolicy::prosperity, AICityGovernorPolicy::termLength, AICityGovernorPolicy::utility
- **45** `AICityGovernorPolicy::eligible(int, const Context &)`
  - called by (2): AICityGovernorPolicy::utility, CvCityAI::AI_updateLocalGovernor
- **73** `AICityGovernorPolicy::utility(int, const Context &)`
  - calls: AICityGovernorPolicy::eligible, AICityGovernorPolicy::clamp
  - called by (1): AICityGovernorPolicy::choose
- **100** `AICityGovernorPolicy::choose(const Context &, int)`
  - calls: AICityGovernorPolicy::utility
  - called by (1): CvCityAI::AI_updateLocalGovernor
- **127** `AICityGovernorPolicy::prosperity(const Context &)`
  - calls: AICityGovernorPolicy::clamp
  - called by (1): CvCityAI::AI_updateLocalGovernor
- **134** `AICityGovernorPolicy::termLength(const Context &)`
  - calls: AICityGovernorPolicy::clamp
  - called by (1): CvCityAI::AI_updateLocalGovernor
- **145** `AICityGovernorPolicy::performance(int, int, int, int)`
  - calls: AICityGovernorPolicy::clamp
  - called by (1): CvCityAI::AI_updateLocalGovernor
