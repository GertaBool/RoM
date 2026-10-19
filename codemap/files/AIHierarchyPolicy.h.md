# AIHierarchyPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **37** `AIHierarchyPolicy::Intent::Intent()`
  - called by (1): AIHierarchyPolicy::derive
- **37** `AIHierarchyPolicy::Intent::Intent(const Intent &)`
  - called by (1): AIHierarchyPolicy::derive
- **46** `AIHierarchyPolicy::clamp(int, int, int)`
  - called by (6): AIHierarchyPolicy::derive, AIHierarchyPolicy::operationDeliveryHorizon, AIHierarchyPolicy::operationRoleTarget, AIHierarchyPolicy::operationTargetValue, AIHierarchyPolicy::routeAdjustedValue, AIHierarchyPolicy::transportCapacityDivisor
- **51** `AIHierarchyPolicy::derive(const Context &)`
  - calls: AIHierarchyPolicy::Intent::Intent(), AIHierarchyPolicy::clamp, AIHierarchyPolicy::Intent::Intent(const Intent &)
  - called by (1): CvPlayerAI::AI_updateAgenda
- **80** `AIHierarchyPolicy::transportCapacityDivisor(int)`
  - calls: AIHierarchyPolicy::clamp
  - called by (1): CvCityAI::AI_chooseProduction
- **87** `AIHierarchyPolicy::routeAdjustedValue(int, int, int, int)`
  - calls: AIHierarchyPolicy::clamp
- **101** `AIHierarchyPolicy::scaleRatio(int, int, int)`
  - called by (1): AIHierarchyPolicy::operationTargetValue
- **113** `AIHierarchyPolicy::operationTargetValue(int, int, int, int)`
  - calls: AIHierarchyPolicy::clamp, AIHierarchyPolicy::scaleRatio
  - called by (1): CvPlayerAI::AI_findOperationTargetCity
- **125** `AIHierarchyPolicy::operationDeliveryHorizon(int)`
  - calls: AIHierarchyPolicy::clamp
  - called by (2): CvPlayerAI::AI_getOperationReinforcementGroup, CvPlayerAI::AI_getOperationRoleTarget
- **133** `AIHierarchyPolicy::operationRoleTarget(int, int, int, bool, int, int)`
  - calls: AIHierarchyPolicy::clamp
  - called by (1): CvPlayerAI::AI_getOperationRoleTarget
