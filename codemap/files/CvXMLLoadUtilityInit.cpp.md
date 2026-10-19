# CvXMLLoadUtilityInit.cpp

Group: game data and XML loading. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **20** `CvXMLLoadUtility::InitStringList(CvString **, int, CvString)`
  - calls: CvString::CvString() [CvString.h], CvString::operator=(const CvString &) [CvString.h]
  - takes the address of: CvString::operator=(const CvString &) [CvString.h]
  - called by (2): CvXMLLoadUtility::SetVariableListTagPair(CvString **, const TCHAR *, CvString *, int, CvString), CvXMLLoadUtility::SetVariableListTagPair(CvString **, const TCHAR *, int, int, CvString)
- **48** `CvXMLLoadUtility::Init2DFloatList(float ***, int, int)`
- **83** `CvXMLLoadUtility::Init2DIntList(int ***, int, int)`
  - called by (3): CvBuildingInfo::read(CvXMLLoadUtility *), CvCivicInfo::read(CvXMLLoadUtility *), CvImprovementInfo::read(CvXMLLoadUtility *)
- **118** `CvXMLLoadUtility::InitPointerFloatList(float ***, int)`
- **147** `CvXMLLoadUtility::InitPointerIntList(int ***, int)`
- **176** `CvXMLLoadUtility::Init2DDirectionTypesList(DirectionTypes ***, int, int)`
- **211** `CvXMLLoadUtility::InitImprovementBonusList(CvImprovementBonusInfo **, int)`
  - calls: CvImprovementBonusInfo::CvImprovementBonusInfo [CvInfos.cpp]
  - called by (2): CvImprovementInfo::read(CvXMLLoadUtility *), CvXMLLoadUtility::SetImprovementBonuses
- **251** `CvXMLLoadUtility::InitBuildingDefaults(int **)`
  - calls: CvGlobals::getNumBuildingClassInfos [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getBuildingClassInfo(BuildingClassTypes) [CvGlobals.cpp], CvBuildingClassInfo::getDefaultBuildingIndex [CvInfos.cpp]
  - called by (1): CvCivilizationInfo::read(CvXMLLoadUtility *)
- **280** `CvXMLLoadUtility::InitUnitDefaults(int **)`
  - calls: CvGlobals::getNumUnitClassInfos [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getUnitClassInfo(UnitClassTypes) [CvGlobals.cpp], CvUnitClassInfo::getDefaultUnitIndex [CvInfos.cpp]
  - called by (1): CvCivilizationInfo::read(CvXMLLoadUtility *)
- **309** `CvXMLLoadUtility::CleanUpGlobalVariables()` (exported)
  - calls: CvGlobals::deleteInfoArrays [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
