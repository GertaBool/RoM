# AIResearchPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **9** `AIResearchPolicy::saturatingAdd(int, int)`
  - called by (1): CvPlayerAI::AI_bestTech
- **24** `AIResearchPolicy::completionScore(int, int, int, int)`
  - called by (1): CvPlayerAI::AI_bestTech
