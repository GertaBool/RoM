# AIBuildingLinePolicy.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **12** `AIBuildingLinePolicy::clamp(int, int, int)`
  - called by (10): AIBuildingLinePolicy::corporationNetValue100, AIBuildingLinePolicy::crusadeWonderValue, AIBuildingLinePolicy::djenneWonderValue, AIBuildingLinePolicy::goldenAgeBuildingValue, AIBuildingLinePolicy::himejiWonderValue, AIBuildingLinePolicy::militaryWonderBonusValue, AIBuildingLinePolicy::naniteDefuserValue, AIBuildingLinePolicy::prereqChainCredit, AIBuildingLinePolicy::scaledCivicHorizon, AIBuildingLinePolicy::worldBankValue
- **21** `AIBuildingLinePolicy::netUpgradeValue(int, int)`
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **34** `AIBuildingLinePolicy::prereqChainCredit(int, int, int, bool)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **49** `AIBuildingLinePolicy::obsolescenceFactorPercent(int, int, bool)`
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **61** `AIBuildingLinePolicy::goldenAgeBuildingValue(bool, int, int, int)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **79** `AIBuildingLinePolicy::militaryWonderBonusValue(int, int, int, int, bool)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **96** `AIBuildingLinePolicy::worldBankValue(int, int, int)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **104** `AIBuildingLinePolicy::crusadeWonderValue(int, bool, int)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **110** `AIBuildingLinePolicy::djenneWonderValue(int, int, bool)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **116** `AIBuildingLinePolicy::himejiWonderValue(int, bool, int)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **122** `AIBuildingLinePolicy::naniteDefuserValue(int, int)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvCityAI::AI_buildingValueThreshold
- **132** `AIBuildingLinePolicy::scaledCivicHorizon(int, int)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvPlayerAI::AI_doCivics
- **142** `AIBuildingLinePolicy::corporationNetValue100(int, int, int, int)`
  - calls: AIBuildingLinePolicy::clamp
  - called by (1): CvPlayerAI::AI_corporationValue
