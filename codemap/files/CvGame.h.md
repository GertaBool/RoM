# CvGame.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **504** `CvGame::AI_init()` (exported; virtual; pure virtual)
  - called by (1): CvGame::init
- **505** `CvGame::AI_reset()` (exported; virtual; pure virtual)
  - called by (1): CvGame::reset
- **506** `CvGame::AI_makeAssignWorkDirty()` (exported; virtual; pure virtual)
  - called by (2): CvGame::setHeadquarters, CvGame::setHolyCity
- **507** `CvGame::AI_updateAssignWork()` (exported; virtual; pure virtual)
  - called by (1): CvGame::update
- **508** `CvGame::AI_combatValue(UnitTypes)` (exported; virtual; pure virtual)
