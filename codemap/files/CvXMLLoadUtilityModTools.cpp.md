# CvXMLLoadUtilityModTools.cpp

Group: game data and XML loading. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **33** `CvXMLLoadUtilityModTools::StringArrayExtend(CvString **, int *, CvString **, int, CvString)`
  - calls: CvString::CvString(const char *) [CvString.h], CvString::operator=(const CvString &) [CvString.h], CvString::CvString() [CvString.h]
  - takes the address of: CvString::operator=(const CvString &) [CvString.h]
  - called by (4): CvCivilizationInfo::copyNonDefaults, CvDiplomacyResponse::UpdateDiplomacies, CvQuestInfo::copyNonDefaults, CvUnitInfo::copyNonDefaults
- **111** `CvXMLLoadUtilityModTools::isDuplicate(int, int *, int)`
  - called by (2): CvEventTriggerInfo::copyNonDefaults, CvHandicapInfo::copyNonDefaults
- **123** `CvXMLLoadUtilityModTools::isDuplicate(int, CvWString *, CvWString)`
  - called by (1): CvEventTriggerInfo::copyNonDefaults
- **138** `CvXMLLoadUtilityModTools::setLocationName(CvString *, const char *)`
  - calls: CvString::CvString(const char *) [CvString.h], CvString::CvString(const CvString &) [CvString.h], CvString::operator=(const std::string &) [CvString.h], CvXMLLoadUtility::CvXMLLoadUtility [CvXMLLoadUtility.cpp], CvString::operator const char * [CvString.h], CvXMLLoadUtilityModTools::isExcludedFile, CvXMLLoadUtilityModTools::isModularArt, CvDLLUtilityIFaceBase::getModName [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvString::operator=(const char *) [CvString.h], CvXMLLoadUtilityModTools::writeThm, CvXMLLoadUtilityModTools::isCommaFile, CvString::operator=(const CvString &) [CvString.h]
  - takes the address of: CvString::operator=(const std::string &) [CvString.h], CvString::operator=(const char *) [CvString.h], CvString::operator=(const CvString &) [CvString.h]
  - called by (17): CvArtInfoAsset::read, CvArtInfoBonus::read, CvArtInfoFeature::read, CvArtInfoImprovement::read, CvArtInfoLeaderhead::read, CvArtInfoTerrain::read, CvArtInfoUnit::read, CvAssetInfoBase::read, CvAttachableInfo::read, CvCameraInfo::read, CvEffectInfo::read, CvInfoBase::read(CvXMLLoadUtility *) …
- **254** `CvXMLLoadUtilityModTools::isExcludedFile(const char *)`
  - calls: CvString::CvString(const char *) [CvString.h], CvString::operator[](int) [CvString.h]
  - takes the address of: CvString::operator[](int) [CvString.h]
  - called by (1): CvXMLLoadUtilityModTools::setLocationName
- **286** `CvXMLLoadUtilityModTools::isCommaFile(CvString *, const char *)`
  - calls: CvString::CvString() [CvString.h], CvString::CvString(const char *) [CvString.h], CvString::operator=(const CvString &) [CvString.h], CvString::GetLength [CvString.h], CvString::operator[](int) [CvString.h], CvString::operator=(const std::string &) [CvString.h], CvXMLLoadUtilityModTools::GetProgramDir, CvDLLUtilityIFaceBase::getModName [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvString::operator const char * [CvString.h], CvString::operator=(const char *) [CvString.h]
  - takes the address of: CvString::operator=(const CvString &) [CvString.h], CvString::operator[](int) [CvString.h], CvString::operator=(const std::string &) [CvString.h], CvString::operator=(const char *) [CvString.h]
  - called by (1): CvXMLLoadUtilityModTools::setLocationName
- **479** `CvXMLLoadUtilityModTools::isModularArt(const char *)`
  - calls: CvXMLLoadUtilityModTools::GetProgramDir, CvString::operator=(const char *) [CvString.h], CvString::CvString() [CvString.h], CvString::CvString(const char *) [CvString.h], CvDLLUtilityIFaceBase::getModName [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h], CvString::operator=(const CvString &) [CvString.h]
  - takes the address of: CvString::operator=(const char *) [CvString.h], CvString::operator=(const CvString &) [CvString.h]
  - called by (2): CvXMLLoadUtility::LoadModLoadControlInfo, CvXMLLoadUtilityModTools::setLocationName
- **635** `CvXMLLoadUtilityModTools::GetProgramDir()`
  - calls: CvString::CvString(const char *) [CvString.h], CvString::operator const char * [CvString.h], CvString::CvString(const CvString &) [CvString.h]
  - called by (4): CvXMLLoadUtilityModTools::isCommaFile, CvXMLLoadUtilityModTools::isModularArt, CvXMLLoadUtilitySetMod::loadModControlArray, CvXMLLoadUtilitySetMod::setModLoadControlDirArray
- **653** `CvXMLLoadUtilityModTools::deleteFileName(const char *, const char)`
  - calls: CvString::CvString(const char *) [CvString.h], CvString::CvString(const CvString &) [CvString.h]
  - called by (3): CvXMLLoadUtility::LoadDiplomacyInfo, CvXMLLoadUtility::LoadGlobalClassInfo, CvXMLLoadUtility::LoadGlobalClassInfoModular
- **669** `CvXMLLoadUtilityModTools::writeThm(const char *)`
  - calls: CvString::CvString(const char *) [CvString.h], CvString::operator const char * [CvString.h]
  - called by (1): CvXMLLoadUtilityModTools::setLocationName
