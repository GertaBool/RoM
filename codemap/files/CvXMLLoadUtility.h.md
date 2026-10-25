# CvXMLLoadUtility.h

Group: game data and XML loading. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **77** `CvXMLLoadUtility::RegisterProgressCB(void (__cdecl*)(int, int, char const*))` (exported)
- **160** `CvXMLLoadUtility::GetXML()`
  - called by (45): CvAdvisorInfo::read, CvAnimationPathInfo::read, CvArtInfoFeature::read, CvArtInfoUnit::read, CvBonusInfo::read(CvXMLLoadUtility*), CvBuildingInfo::read(CvXMLLoadUtility*), CvCivicInfo::read(CvXMLLoadUtility*), CvCivilizationInfo::read(CvXMLLoadUtility*), CvCorporationInfo::read, CvDiplomacyInfo::copyNonDefaults, CvDiplomacyInfo::read(CvXMLLoadUtility*), CvDiplomacyResponse::read(CvXMLLoadUtility*) …
- **362** `CvXMLLoadUtility::SetGlobalDefine<char const>(char const*, char const*&)`
  - calls: CvGlobals::getDefinesVarSystem [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], FVariableSystem::GetValue(char const*, char const*&) const [FVariableSystem.inl]
  - called by (1): CvXMLLoadUtility::SetPostGlobalsGlobalDefines
- **440** `CvXMLLoadUtility::InitList<int>(int**, int, int)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
  - called by (28): CvBonusInfo::read(CvXMLLoadUtility*), CvBuildingInfo::read(CvXMLLoadUtility*), CvCivicInfo::read(CvXMLLoadUtility*), CvCivilizationInfo::read(CvXMLLoadUtility*), CvCorporationInfo::read, CvEmphasizeInfo::read, CvFeatureInfo::read, CvImprovementInfo::read(CvXMLLoadUtility*), CvProcessInfo::read, CvReligionInfo::read, CvRouteInfo::read, CvSpecialistInfo::read …
- **440** `CvXMLLoadUtility::InitList<float>(float**, int, float)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
  - called by (1): CvXMLLoadUtility::SetVariableListTagPair(float**, char const*, int, int, float)
- **440** `CvXMLLoadUtility::InitList<bool>(bool**, int, bool)`
  - calls: operator new[](unsigned int) [CvGameCoreDLL.cpp]
  - called by (6): CvBuildingInfo::read(CvXMLLoadUtility*), CvTechInfo::read(CvXMLLoadUtility*), CvXMLLoadUtility::SetCommerce<bool>, CvXMLLoadUtility::SetFeatureStruct, CvXMLLoadUtility::SetVariableListTagPair(bool**, char const*, CvString*, int, bool), CvXMLLoadUtility::SetVariableListTagPair(bool**, char const*, int, int, bool)
- **450** `CvXMLLoadUtility::SetCommerce<int>(int**)`
  - calls: CvXMLLoadUtility::SkipToNextVal [CvXMLLoadUtility.cpp], CvDLLUtilityIFaceBase::getXMLIFace [CvDLLUtilityIFaceBase.h], CvDLLXmlIFaceBase::GetNumChildren [CvDLLXMLIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvXMLLoadUtility::InitList<int>, CvXMLLoadUtility::GetChildXmlVal(int*, int) [CvXMLLoadUtilityGet.cpp], CvXMLLoadUtility::GetNextXmlVal(int*, int) [CvXMLLoadUtilityGet.cpp], CvDLLXmlIFaceBase::SetToParent [CvDLLXMLIFaceBase.h]
  - called by (9): CvBuildingInfo::read(CvXMLLoadUtility*), CvCivicInfo::read(CvXMLLoadUtility*), CvCorporationInfo::read, CvEmphasizeInfo::read, CvProcessInfo::read, CvReligionInfo::read, CvSpecialistInfo::read, CvTraitInfo::read, CvVoteSourceInfo::read
- **450** `CvXMLLoadUtility::SetCommerce<bool>(bool**)`
  - calls: CvXMLLoadUtility::SkipToNextVal [CvXMLLoadUtility.cpp], CvDLLUtilityIFaceBase::getXMLIFace [CvDLLUtilityIFaceBase.h], CvDLLXmlIFaceBase::GetNumChildren [CvDLLXMLIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvXMLLoadUtility::InitList<bool>, CvXMLLoadUtility::GetChildXmlVal(bool*, bool) [CvXMLLoadUtilityGet.cpp], CvXMLLoadUtility::GetNextXmlVal(bool*, bool) [CvXMLLoadUtilityGet.cpp], CvDLLXmlIFaceBase::SetToParent [CvDLLXMLIFaceBase.h]
  - called by (2): CvBuildingInfo::read(CvXMLLoadUtility*), CvTechInfo::read(CvXMLLoadUtility*)
