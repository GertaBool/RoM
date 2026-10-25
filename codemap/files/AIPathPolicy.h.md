# AIPathPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **9** `AIPathPolicy::scaleRatio(int, int, int)`
  - called by (1): AIPathPolicy::threatAdjustedCost
- **36** `AIPathPolicy::threatAdjustedCost(int, int, bool, bool)`
  - calls: AIPathPolicy::scaleRatio
  - called by (1): pathCost
