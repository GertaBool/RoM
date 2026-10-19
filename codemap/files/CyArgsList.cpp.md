# CyArgsList.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **10** `CyArgsList::add(int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (151): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool), CvCity::doPlotCulture, CvCity::getConscriptUnit, CvCity::getProductionNeeded(BuildingTypes), CvCity::getTriggerValue, CvCity::init, CvDLLButtonPopup::OnFocus, CvDLLButtonPopup::OnOkClicked, CvDLLButtonPopup::launchChooseTechPopup …
- **15** `CyArgsList::add(float)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (1): CvDllPythonEvents::reportUpdate
- **21** `CyArgsList::add(void *)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (83): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool), CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCityAI::AI_chooseProduction …
- **27** `CyArgsList::add(const char *)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (85): CvDllPythonEvents::preSave, CvDllPythonEvents::reportBeginGameTurn, CvDllPythonEvents::reportBeginPlayerTurn, CvDllPythonEvents::reportBuildingBuilt, CvDllPythonEvents::reportChangeWar, CvDllPythonEvents::reportChat, CvDllPythonEvents::reportCityAcquired, CvDllPythonEvents::reportCityAcquiredAndKept, CvDllPythonEvents::reportCityBuildingBuilding, CvDllPythonEvents::reportCityBuildingProcess, CvDllPythonEvents::reportCityBuildingProject, CvDllPythonEvents::reportCityBuildingUnit …
- **33** `CyArgsList::add(const wchar *)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (5): CvDLLButtonPopup::OnFocus, CvDLLButtonPopup::OnOkClicked, CvDllPythonEvents::reportChat, CvNetAddReminder::Execute, CvPlayer::sendReminder
- **42** `CyArgsList::add(const char *, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
- **48** `CyArgsList::add(const float *, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
- **63** `CyArgsList::add(const byte *, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
- **78** `CyArgsList::add(const int *, int)` (exported)
  - calls: CyArgsList::push_back [CyArgsList.h]
  - called by (3): CvDllPythonEvents::reportMouseEvent, CvDllPythonEvents::reportPlayerRevolution, CvDllPythonEvents::reportSelectionGroupPushMission
- **92** `CyArgsList::makeFunctionArgs()` (exported)
  - calls: CvDLLPythonIFaceBase::MakeFunctionArgs [CvDLLPythonIFaceBase.h], CvDLLUtilityIFaceBase::getPythonIFace [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
  - called by (110): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool), CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCity::getConscriptUnit …
