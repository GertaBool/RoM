# AIFeedbackPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **11** `AIFeedbackPolicy::Signal::Signal(const Signal &)`
  - called by (1): AIFeedbackPolicy::governorRecommendation
- **14** `AIFeedbackPolicy::Signal::Signal()`
  - called by (2): AIFeedbackPolicy::governorRecommendation, CvPlayerAI::AI_updateAgenda
- **17** `AIFeedbackPolicy::clamp(int, int, int)`
  - called by (5): AIFeedbackPolicy::agendaDelta, AIFeedbackPolicy::chooseGeneralPersonality, AIFeedbackPolicy::doctrineConfidence, AIFeedbackPolicy::doctrineEvidence, AIFeedbackPolicy::governorRecommendation
- **22** `AIFeedbackPolicy::governorRecommendation(int, int, int)`
  - calls: AIFeedbackPolicy::Signal::Signal(), AIFeedbackPolicy::Signal::Signal(const Signal &), AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateAgenda
- **47** `AIFeedbackPolicy::agendaDelta(const int (&)[5], const Signal &)`
  - calls: AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateAgenda
- **58** `AIFeedbackPolicy::doctrineEvidence(int, int)`
  - calls: AIFeedbackPolicy::clamp
- **63** `AIFeedbackPolicy::doctrineConfidence(int, int, int)`
  - calls: AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateAgenda
- **73** `AIFeedbackPolicy::chooseGeneralPersonality(int, int, int, int, int, int)`
  - calls: AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateMilitaryOperations
