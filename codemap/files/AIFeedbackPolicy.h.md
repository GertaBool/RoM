# AIFeedbackPolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **14** `AIFeedbackPolicy::Signal::Signal()`
  - called by (2): AIFeedbackPolicy::governorRecommendation, CvPlayerAI::AI_updateAgenda
- **18** `AIFeedbackPolicy::clamp(int, int, int)`
  - called by (4): AIFeedbackPolicy::agendaDelta, AIFeedbackPolicy::chooseGeneralPersonality, AIFeedbackPolicy::doctrineConfidence, AIFeedbackPolicy::governorRecommendation
- **23** `AIFeedbackPolicy::governorRecommendation(int, int, int)`
  - calls: AIFeedbackPolicy::Signal::Signal, AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateAgenda
- **48** `AIFeedbackPolicy::agendaDelta(int const (&)[5], AIFeedbackPolicy::Signal const&)`
  - calls: AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateAgenda
- **64** `AIFeedbackPolicy::doctrineConfidence(int, int, int)`
  - calls: AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateAgenda
- **75** `AIFeedbackPolicy::chooseGeneralPersonality(int, int, int, int, int, int)`
  - calls: AIFeedbackPolicy::clamp
  - called by (1): CvPlayerAI::AI_updateMilitaryOperations
