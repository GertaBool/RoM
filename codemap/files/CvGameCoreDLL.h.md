# CvGameCoreDLL.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **44** `NiColorA::NiColorA(float, float, float, float)`
  - called by (7): CvCity::getBarBackgroundColor, CvCity::getCityBillboardSizeIconColors, CvColorInfo::read, CvPlayer::getCultureLayerColors, CvPlayer::getReligionLayerColors, CvPlayer::getTradeLayerColors, CvPlayer::getUnitLayerColors
- **45** `NiColorA::NiColorA()`
  - called by (2): CvCity::getCityBillboardSizeIconColors, CvColorInfo::CvColorInfo()
- **51** `NiPoint2::NiPoint2()`
  - called by (2): CvPlotIndicatorData::CvPlotIndicatorData(), CvUnitEntry::CvUnitEntry
- **52** `NiPoint2::NiPoint2(float, float)`
  - called by (4): CvPlayer::getResourceLayerColors, CvUnit::attackForDamage, CvUnit::updateCombat, CvUnit::updateStackCombat
- **59** `NiPoint3::NiPoint3()`
  - called by (4): CvDllPythonEvents::reportKbdEvent, CvDllPythonEvents::reportMouseEvent, CvGlobals::CvGlobals, CvPlot::getPoint
- **60** `NiPoint3::NiPoint3(float, float, float)`
  - called by (15): CvDLLButtonPopup::launchAlarmPopup, CvDLLButtonPopup::launchDisbandCityPopup, CvDLLButtonPopup::launchEventPopup, CvDLLButtonPopup::launchProductionPopup, CvDLLButtonPopup::launchRazeCityPopup, CvGame::regenerateMap, CvGlobals::init, CvPlayer::setTurnActive, CvSelectionGroup::continueMission, CvUnit::attackForDamage, CvUnit::found, CvUnit::promote …
- **87** `NiPoint3::Length() const`
  - called by (1): NiPoint3::Unitize
- **90** `NiPoint3::Unitize()`
  - calls: NiPoint3::Length
  - called by (3): CvUnit::attackForDamage, CvUnit::updateCombat, CvUnit::updateStackCombat
- **·** `CvPlotIndicatorData::~CvPlotIndicatorData()` (exported; written by the compiler)
  - calls: CvString::~CvString [CvString.h], CvWString::~CvWString [CvString.h]
  - called by (2): CvPlayer::getResourceLayerColors, CvPlayer::getUnitLayerColors
- **·** `CvColorInfo::`vector deleting dtor'(unsigned int)` (virtual; overrides CvInfoBase::`vector deleting dtor'; written by the compiler)
  - calls: operator delete(void*) [CvGameCoreDLL.cpp], operator delete[](void*) [CvGameCoreDLL.cpp], CvColorInfo::~CvColorInfo [CvInfos.cpp]
  - takes the address of: CvColorInfo::~CvColorInfo [CvInfos.cpp]
- **·** `CvUnitFormationInfo::`vector deleting dtor'(unsigned int)` (virtual; overrides CvInfoBase::`vector deleting dtor'; written by the compiler)
  - calls: operator delete(void*) [CvGameCoreDLL.cpp], operator delete[](void*) [CvGameCoreDLL.cpp], CvUnitFormationInfo::~CvUnitFormationInfo [CvInfos.cpp]
  - takes the address of: CvUnitFormationInfo::~CvUnitFormationInfo [CvInfos.cpp]
