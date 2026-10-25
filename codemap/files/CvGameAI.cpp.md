# CvGameAI.cpp

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **13** `CvGameAI::CvGameAI()`
  - calls: CvGame::CvGame [CvGame.cpp], CvGameAI::AI_reset, CvGame::~CvGame [CvGame.cpp]
  - called by (1): CvGlobals::init
- **19** `CvGameAI::~CvGameAI()` (virtual)
  - calls: CvGameAI::AI_uninit, CvGame::~CvGame [CvGame.cpp]
  - called by (1): CvGameAI::`scalar deleting dtor'
- **25** `CvGameAI::AI_init()` (virtual; overrides CvGame::AI_init)
  - calls: CvGameAI::AI_reset
- **34** `CvGameAI::AI_uninit()`
  - called by (2): CvGameAI::AI_reset, CvGameAI::~CvGameAI
- **39** `CvGameAI::AI_reset()` (virtual; overrides CvGame::AI_reset)
  - calls: CvGameAI::AI_uninit
  - called by (2): CvGameAI::AI_init, CvGameAI::CvGameAI
- **47** `CvGameAI::AI_makeAssignWorkDirty()` (virtual; overrides CvGame::AI_makeAssignWorkDirty)
  - calls: CvPlayer::isAlive [CvPlayer.cpp], CvPlayerAI::getPlayer [CvPlayerAI.h], CvPlayerAI::AI_makeAssignWorkDirty [CvPlayerAI.cpp]
  - called by (9): CvCity::init, CvCity::kill, CvPlayer::changeHasCorporationCount, CvPlayer::changeHasReligionCount, CvPlayer::changeStateReligionCount, CvPlayer::setCivics, CvPlayer::setLastStateReligion, CvTeam::declareWar, CvTeam::makePeace
- **61** `CvGameAI::AI_updateAssignWork()` (virtual; overrides CvGame::AI_updateAssignWork)
  - calls: CvPlayerAI::getPlayer [CvPlayerAI.h], CvPlayer::isAlive [CvPlayer.cpp], CvPlayer::getTeam [CvPlayer.cpp], CvTeam::isHuman [CvTeam.cpp], CvTeamAI::getTeam [CvTeamAI.h], CvPlayer::AI_updateAssignWork [CvPlayer.h] ⇢ CvPlayerAI::AI_updateAssignWork
- **76** `CvGameAI::AI_combatValue(UnitTypes)` (virtual; overrides CvGame::AI_combatValue)
  - calls: CvGlobals::getUnitInfo(UnitTypes) [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvUnitInfo::getDomainType [CvInfos.cpp], CvUnitInfo::getAirCombat [CvInfos.cpp], CvUnitInfo::getCombat [CvInfos.cpp], CvGlobals::getDefineINT(char const*) const [CvGlobals.cpp], CvUnitInfo::getFirstStrikes [CvInfos.cpp], CvUnitInfo::getChanceFirstStrikes [CvInfos.cpp], CvGame::getBestLandUnitCombat [CvGame.cpp]
  - called by (6): CvCityAI::AI_doDraft, CvCityAI::AI_doHurry, CvPlayerAI::AI_civicValue, CvPlayerAI::AI_techUnitValue, CvPlayerAI::AI_unitValue, CvUnit::gift
- **100** `CvGameAI::AI_turnsPercent(int, int)`
  - called by (2): CvCityAI::AI_bestBuildingThreshold, CvCityAI::AI_bestProject
- **113** `CvGameAI::read(FDataStreamBase*)` (virtual; overrides CvGame::read)
  - calls: CvGame::read [CvGame.cpp], FDataStreamBase::Read [FDataStreamBase.h]
- **124** `CvGameAI::write(FDataStreamBase*)` (virtual; overrides CvGame::write)
  - calls: CvGame::write [CvGame.cpp], FDataStreamBase::Write [FDataStreamBase.h]
- **·** `CvGameAI::`scalar deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: CvGameAI::~CvGameAI, operator delete(void*) [CvGameCoreDLL.cpp]
