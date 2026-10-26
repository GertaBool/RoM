# CyArgsList.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **11** `CyArgsList::add(int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (152): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const, CvCity::doPlotCulture, CvCity::getConscriptUnit, CvCity::getProductionNeeded(BuildingTypes) const, CvCity::getTriggerValue, CvCity::init, CvDLLButtonPopup::OnFocus, CvDLLButtonPopup::OnOkClicked, CvDLLButtonPopup::launchChooseTechPopup …
- **16** `CyArgsList::add(float)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (1): CvDllPythonEvents::reportUpdate
- **22** `CyArgsList::add(void*)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (83): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const, CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCityAI::AI_chooseProduction …
- **28** `CyArgsList::add(char const*)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (85): CvDllPythonEvents::preSave, CvDllPythonEvents::reportBeginGameTurn, CvDllPythonEvents::reportBeginPlayerTurn, CvDllPythonEvents::reportBuildingBuilt, CvDllPythonEvents::reportChangeWar, CvDllPythonEvents::reportChat, CvDllPythonEvents::reportCityAcquired, CvDllPythonEvents::reportCityAcquiredAndKept, CvDllPythonEvents::reportCityBuildingBuilding, CvDllPythonEvents::reportCityBuildingProcess, CvDllPythonEvents::reportCityBuildingProject, CvDllPythonEvents::reportCityBuildingUnit …
- **34** `CyArgsList::add(unsigned short const*)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (5): CvDLLButtonPopup::OnFocus, CvDLLButtonPopup::OnOkClicked, CvDllPythonEvents::reportChat, CvNetAddReminder::Execute, CvPlayer::sendReminder
- **43** `CyArgsList::add(char const*, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
- **49** `CyArgsList::add(float const*, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
- **64** `CyArgsList::add(unsigned char const*, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
- **79** `CyArgsList::add(int const*, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (3): CvDllPythonEvents::reportMouseEvent, CvDllPythonEvents::reportPlayerRevolution, CvDllPythonEvents::reportSelectionGroupPushMission
- **93** `CyArgsList::makeFunctionArgs()` (exported)
  - calls: CvDLLPythonIFaceBase::MakeFunctionArgs [CvDLLPythonIFaceBase.h], CvDLLUtilityIFaceBase::getPythonIFace [CvDLLUtilityIFaceBase.h], CvGlobals::getInstance [CvGlobals.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (111): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const, CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCity::getConscriptUnit …
