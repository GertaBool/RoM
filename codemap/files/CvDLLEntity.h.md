# CvDLLEntity.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **31** `CvDLLEntity::getEntity()` (exported)
  - called by (5): CvDLLEntity::PlayAnimation, CvDLLEntity::StopAnimation, CvDLLEntity::removeEntity, CvDLLEntity::setVisible, CvDLLEntity::setup
- **32** `CvDLLEntity::getEntity()` (exported)
  - called by (1): CvDLLEntity::IsSelected
- **33** `CvDLLEntity::getUnitEntity()` (exported)
  - called by (15): CvDLLEntity::ExecuteMove, CvDLLEntity::GetSiegeTower, CvDLLEntity::MoveTo, CvDLLEntity::NotifyEntity, CvDLLEntity::QueueMove, CvDLLEntity::SetPosition, CvDLLEntity::SetSiegeTower, CvGame::updateUnitEnemyGlow, CvPlayer::doWarnings, CvPlayer::setCurrentEra, CvUnit::NotifyEntity, CvUnit::planBattle …
- **34** `CvDLLEntity::getCityEntity()` (exported)
- **35** `CvDLLEntity::getUnitEntity()` (exported)
- **36** `CvDLLEntity::getCityEntity()` (exported)
- **38** `CvDLLEntity::setEntity(CvEntity *)` (exported)
