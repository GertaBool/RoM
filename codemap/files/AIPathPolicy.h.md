# AIPathPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **8** `AIPathPolicy::scaleRatio(const int, const int, const int)`
  - called by (1): AIPathPolicy::threatAdjustedCost
- **34** `AIPathPolicy::threatAdjustedCost(const int, const int, const bool, const bool)`
  - calls: AIPathPolicy::scaleRatio
  - called by (1): pathCost
