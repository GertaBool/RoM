# CvXMLLoadUtility.h

Group: game data and XML loading. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **59** `CvXMLLoadUtility::SetGlobals()` (exported; declared, not defined in the source)
- **71** `CvXMLLoadUtility::SetHelpText()` (exported; declared, not defined in the source)
- **77** `CvXMLLoadUtility::RegisterProgressCB(ProgressCB)` (exported)
- **160** `CvXMLLoadUtility::GetXML()`
  - called by (45): CvAdvisorInfo::read, CvAnimationPathInfo::read, CvArtInfoFeature::read, CvArtInfoUnit::read, CvBonusInfo::read(CvXMLLoadUtility *), CvBuildingInfo::read(CvXMLLoadUtility *), CvCivicInfo::read(CvXMLLoadUtility *), CvCivilizationInfo::read(CvXMLLoadUtility *), CvCorporationInfo::read, CvDiplomacyInfo::copyNonDefaults, CvDiplomacyInfo::read(CvXMLLoadUtility *), CvDiplomacyResponse::read(CvXMLLoadUtility *) …
- **360** `CvXMLLoadUtility::SetGlobalDefine(const char *, T *&)`
  - calls: CvGlobals::getDefinesVarSystem [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
  - called by (1): CvXMLLoadUtility::SetPostGlobalsGlobalDefines
- **438** `CvXMLLoadUtility::InitList(T **, int, T)`
  - called by (30): CvBonusInfo::read(CvXMLLoadUtility *), CvBuildingInfo::read(CvXMLLoadUtility *), CvCivicInfo::read(CvXMLLoadUtility *), CvCivilizationInfo::read(CvXMLLoadUtility *), CvCorporationInfo::read, CvEmphasizeInfo::read, CvFeatureInfo::read, CvImprovementInfo::read(CvXMLLoadUtility *), CvProcessInfo::read, CvReligionInfo::read, CvRouteInfo::read, CvSpecialistInfo::read …
- **448** `CvXMLLoadUtility::SetCommerce(T **)`
  - calls: CvXMLLoadUtility::SkipToNextVal [CvXMLLoadUtility.cpp], CvDLLUtilityIFaceBase::getXMLIFace [CvDLLUtilityIFaceBase.h], CvDLLXmlIFaceBase::GetNumChildren [CvDLLXMLIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvDLLXmlIFaceBase::SetToParent [CvDLLXMLIFaceBase.h]
  - called by (10): CvBuildingInfo::read(CvXMLLoadUtility *), CvCivicInfo::read(CvXMLLoadUtility *), CvCorporationInfo::read, CvEmphasizeInfo::read, CvProcessInfo::read, CvReligionInfo::read, CvSpecialistInfo::read, CvTechInfo::read(CvXMLLoadUtility *), CvTraitInfo::read, CvVoteSourceInfo::read
