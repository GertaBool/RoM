# AIHierarchyPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **47** `AIHierarchyPolicy::clamp(int, int, int)`
  - called by (5): AIHierarchyPolicy::derive, AIHierarchyPolicy::operationDeliveryHorizon, AIHierarchyPolicy::operationRoleTarget, AIHierarchyPolicy::operationTargetValue, AIHierarchyPolicy::transportCapacityDivisor
- **52** `AIHierarchyPolicy::derive(AIHierarchyPolicy::Context const&)`
  - calls: AIHierarchyPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateAgenda
- **81** `AIHierarchyPolicy::transportCapacityDivisor(int)`
  - calls: AIHierarchyPolicy::clamp
  - called by (1): CvCityAI::AI_chooseProduction
- **102** `AIHierarchyPolicy::scaleRatio(int, int, int)`
  - called by (1): AIHierarchyPolicy::operationTargetValue
- **115** `AIHierarchyPolicy::operationTargetValue(int, int, int, int)`
  - calls: AIHierarchyPolicy::clamp, AIHierarchyPolicy::scaleRatio
  - called by (1): CvPlayerAI::AI_findOperationTargetCity
- **126** `AIHierarchyPolicy::operationDeliveryHorizon(int)`
  - calls: AIHierarchyPolicy::clamp
  - called by (2): CvPlayerAI::AI_getOperationReinforcementGroup, CvPlayerAI::AI_getOperationRoleTarget
- **135** `AIHierarchyPolicy::operationRoleTarget(int, int, int, bool, int, int)`
  - calls: AIHierarchyPolicy::clamp
  - called by (1): CvPlayerAI::AI_getOperationRoleTarget
