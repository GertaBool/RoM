# CvXMLLoadUtilityModTools.cpp

Group: game data and XML loading. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **36** `CvXMLLoadUtilityModTools::StringArrayExtend(CvString**, int*, CvString**, int, CvString) const`
  - calls: CvString::operator=(CvString const&) [CvString.h], operator new[](unsigned int) [CvGameCoreDLL.cpp], CvString::`vector deleting dtor' [CvInfos.cpp], operator delete[](void*) [CvGameCoreDLL.cpp], CvString::~CvString [CvString.h]
  - takes the address of: CvString::CvString() [CvString.h], CvString::~CvString [CvString.h]
  - called by (4): CvCivilizationInfo::copyNonDefaults, CvDiplomacyResponse::UpdateDiplomacies, CvQuestInfo::copyNonDefaults, CvUnitInfo::copyNonDefaults
- **112** `CvXMLLoadUtilityModTools::isDuplicate(int, int*, int) const`
  - called by (2): CvEventTriggerInfo::copyNonDefaults, CvHandicapInfo::copyNonDefaults
- **124** `CvXMLLoadUtilityModTools::isDuplicate(int, CvWString*, CvWString) const`
  - calls: CvWString::~CvWString [CvString.h]
  - called by (1): CvEventTriggerInfo::copyNonDefaults
- **139** `CvXMLLoadUtilityModTools::setLocationName(CvString*, char const*)`
  - calls: CvString::CvString(char const*) [CvString.h], CvString::CvString(CvString const&) [CvString.h], CvString::operator=(std::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) [CvString.h], operator new(unsigned int) [CvGameCoreDLL.cpp], CvXMLLoadUtility::CvXMLLoadUtility [CvXMLLoadUtility.cpp], CvString::operator char const * [CvString.h], CvXMLLoadUtilityModTools::isExcludedFile, CvXMLLoadUtilityModTools::isModularArt, CvDLLUtilityIFaceBase::getModName [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvString::operator=(char const*) [CvString.h], CvXMLLoadUtilityModTools::writeThm, CvXMLLoadUtilityModTools::isCommaFile, CvString::operator=(CvString const&) [CvString.h], CvXMLLoadUtility::`scalar deleting dtor' [CvInitCore.cpp], operator delete(void*) [CvGameCoreDLL.cpp], CvString::~CvString [CvString.h]
  - called by (17): CvArtInfoAsset::read, CvArtInfoBonus::read, CvArtInfoFeature::read, CvArtInfoImprovement::read, CvArtInfoLeaderhead::read, CvArtInfoTerrain::read, CvArtInfoUnit::read, CvAssetInfoBase::read, CvAttachableInfo::read, CvCameraInfo::read, CvEffectInfo::read, CvInfoBase::read(CvXMLLoadUtility*) …
- **255** `CvXMLLoadUtilityModTools::isExcludedFile(char const*)`
  - calls: CvString::CvString(char const*) [CvString.h], CvString::operator[] [CvString.h], CvString::~CvString [CvString.h]
  - called by (1): CvXMLLoadUtilityModTools::setLocationName
- **287** `CvXMLLoadUtilityModTools::isCommaFile(CvString*, char const*)`
  - calls: CvString::CvString() [CvString.h], CvString::CvString(char const*) [CvString.h], CvString::operator=(CvString const&) [CvString.h], CvString::GetLength [CvString.h], CvString::operator[] [CvString.h], CvString::operator=(std::basic_string<char, std::char_traits<char>, std::allocator<char>> const&) [CvString.h], CvXMLLoadUtilityModTools::GetProgramDir, CvDLLUtilityIFaceBase::getModName [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvString::operator char const * [CvString.h], CvString::operator=(char const*) [CvString.h], CvString::~CvString [CvString.h]
  - called by (1): CvXMLLoadUtilityModTools::setLocationName
- **480** `CvXMLLoadUtilityModTools::isModularArt(char const*)`
  - calls: CvXMLLoadUtilityModTools::GetProgramDir, CvString::~CvString [CvString.h], CvString::operator=(char const*) [CvString.h], CvString::CvString() [CvString.h], CvString::CvString(char const*) [CvString.h], CvDLLUtilityIFaceBase::getModName [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h], CvString::operator=(CvString const&) [CvString.h]
  - called by (2): CvXMLLoadUtility::LoadModLoadControlInfo<class CvModLoadControlInfo>, CvXMLLoadUtilityModTools::setLocationName
- **636** `CvXMLLoadUtilityModTools::GetProgramDir()`
  - calls: CvString::CvString(char const*) [CvString.h], CvString::operator char const * [CvString.h], CvString::CvString(CvString const&) [CvString.h], CvString::~CvString [CvString.h]
  - called by (4): CvXMLLoadUtilityModTools::isCommaFile, CvXMLLoadUtilityModTools::isModularArt, CvXMLLoadUtilitySetMod::loadModControlArray, CvXMLLoadUtilitySetMod::setModLoadControlDirArray
- **654** `CvXMLLoadUtilityModTools::deleteFileName(char const*, char)`
  - calls: CvString::CvString(char const*) [CvString.h], CvString::CvString(CvString const&) [CvString.h], CvString::~CvString [CvString.h]
  - called by (97): CvXMLLoadUtility::LoadDiplomacyInfo, CvXMLLoadUtility::LoadGlobalClassInfo<class CvAdvisorInfo>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvAnimationCategoryInfo>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvAnimationPathInfo>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoBonus>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoBuilding>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoCivilization>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoFeature>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoImprovement>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoInterface>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoLeaderhead>, CvXMLLoadUtility::LoadGlobalClassInfo<class CvArtInfoMisc> …
- **670** `CvXMLLoadUtilityModTools::writeThm(char const*)`
  - calls: CvString::CvString(char const*) [CvString.h], CvString::operator char const * [CvString.h], CvString::~CvString [CvString.h]
  - called by (1): CvXMLLoadUtilityModTools::setLocationName
