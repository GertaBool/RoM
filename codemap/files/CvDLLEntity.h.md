# CvDLLEntity.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **31** `CvDLLEntity::getEntity()` (exported)
  - called by (5): CvDLLEntity::PlayAnimation, CvDLLEntity::StopAnimation, CvDLLEntity::removeEntity, CvDLLEntity::setVisible, CvDLLEntity::setup
- **32** `CvDLLEntity::getEntity() const` (exported)
  - called by (1): CvDLLEntity::IsSelected
- **33** `CvDLLEntity::getUnitEntity()` (exported)
  - called by (16): CvDLLEntity::ExecuteMove, CvDLLEntity::GetSiegeTower, CvDLLEntity::MoveTo, CvDLLEntity::NotifyEntity, CvDLLEntity::QueueMove, CvDLLEntity::SetPosition, CvDLLEntity::SetSiegeTower, CvGame::updateUnitEnemyGlow, CvPlayer::doWarnings, CvPlayer::setCurrentEra, CvUnit::NotifyEntity, CvUnit::pageGraphics …
- **34** `CvDLLEntity::getCityEntity()` (exported)
- **35** `CvDLLEntity::getUnitEntity() const` (exported)
- **36** `CvDLLEntity::getCityEntity() const` (exported)
- **38** `CvDLLEntity::setEntity(CvEntity*)` (exported)
- **60** `CvDLLEntity::isGraphicsPagedOut() const` (exported)
  - called by (10): CvGame::pageGraphics, CvGame::updateUnitEnemyGlow, CvPlayer::doWarnings, CvPlayer::setCurrentEra, CvPlot::canPageGraphicsOut, CvUnit::NotifyEntity, CvUnit::setHasPromotion, CvUnit::setPromotionReady, CvUnit::setXY, addEntityMission
- **·** `CombatDetails::CombatDetails(CombatDetails const&)` (exported; written by the compiler)
- **·** `CvDLLEntity::CvDLLEntity(CvDLLEntity const&)` (exported; written by the compiler)
- **·** `CombatDetails::operator=(CombatDetails const&)` (exported; written by the compiler)
- **·** `CvDLLEntity::operator=(CvDLLEntity const&)` (exported; written by the compiler)
- **·** `CvDLLEntity::`vector deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: CvDLLEntity::~CvDLLEntity [CvDLLEntity.cpp], operator delete(void*) [CvGameCoreDLL.cpp], operator delete[](void*) [CvGameCoreDLL.cpp]
  - takes the address of: CvDLLEntity::~CvDLLEntity [CvDLLEntity.cpp]
- **·** `CvTalkingHeadMessage::`default ctor closure'()` (exported; written by the compiler)
  - calls: CvTalkingHeadMessage::CvTalkingHeadMessage [CvTalkingHeadMessage.cpp]
- **·** `CvDLLEntity::`scalar deleting dtor'(unsigned int)` (virtual; written by the compiler)
  - calls: CvDLLEntity::~CvDLLEntity [CvDLLEntity.cpp], operator delete(void*) [CvGameCoreDLL.cpp]
