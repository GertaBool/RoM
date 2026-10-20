# CvXMLLoadUtilityInit.cpp

Group: game data and XML loading. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **21** `CvXMLLoadUtility::InitStringList(CvString**, int, CvString)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp], CvString::operator=(CvString const&) [CvString.h], operator delete[](void*) [CvGameCoreDLL.cpp], CvString::~CvString [CvString.h]
  - takes the address of: CvString::CvString() [CvString.h], CvString::~CvString [CvString.h]
  - called by (2): CvXMLLoadUtility::SetVariableListTagPair(CvString**, char const*, CvString*, int, CvString), CvXMLLoadUtility::SetVariableListTagPair(CvString**, char const*, int, int, CvString)
- **49** `CvXMLLoadUtility::Init2DFloatList(float***, int, int)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
- **84** `CvXMLLoadUtility::Init2DIntList(int***, int, int)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
  - called by (3): CvBuildingInfo::read(CvXMLLoadUtility*), CvCivicInfo::read(CvXMLLoadUtility*), CvImprovementInfo::read(CvXMLLoadUtility*)
- **119** `CvXMLLoadUtility::InitPointerFloatList(float***, int)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
- **148** `CvXMLLoadUtility::InitPointerIntList(int***, int)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
- **177** `CvXMLLoadUtility::Init2DDirectionTypesList(DirectionTypes***, int, int)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
- **212** `CvXMLLoadUtility::InitImprovementBonusList(CvImprovementBonusInfo**, int)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp], operator delete[](void*) [CvGameCoreDLL.cpp]
  - takes the address of: CvImprovementBonusInfo::CvImprovementBonusInfo() [CvInfos.cpp], CvImprovementBonusInfo::~CvImprovementBonusInfo [CvInfos.cpp]
  - called by (2): CvImprovementInfo::read(CvXMLLoadUtility*), CvXMLLoadUtility::SetImprovementBonuses
- **252** `CvXMLLoadUtility::InitBuildingDefaults(int**)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp], CvGlobals::getNumBuildingClassInfos [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getBuildingClassInfo(BuildingClassTypes) [CvGlobals.cpp], CvBuildingClassInfo::getDefaultBuildingIndex [CvInfos.cpp]
  - called by (1): CvCivilizationInfo::read(CvXMLLoadUtility*)
- **281** `CvXMLLoadUtility::InitUnitDefaults(int**)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp], CvGlobals::getNumUnitClassInfos [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getUnitClassInfo(UnitClassTypes) [CvGlobals.cpp], CvUnitClassInfo::getDefaultUnitIndex [CvInfos.cpp]
  - called by (1): CvCivilizationInfo::read(CvXMLLoadUtility*)
- **310** `CvXMLLoadUtility::CleanUpGlobalVariables()` (exported)
  - calls: CvGlobals::deleteInfoArrays [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
