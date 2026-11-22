# CvGame.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **520** `CvGame::AI_init(…)` (virtual; pure virtual)
  - called by (1): CvGame::init
- **521** `CvGame::AI_reset(…)` (virtual; pure virtual)
  - called by (1): CvGame::reset
- **522** `CvGame::AI_makeAssignWorkDirty(…)` (virtual; pure virtual)
  - called by (2): CvGame::setHeadquarters, CvGame::setHolyCity
- **523** `CvGame::AI_updateAssignWork(…)` (virtual; pure virtual)
  - called by (1): CvGame::update
- **524** `CvGame::AI_combatValue(…)` (virtual; pure virtual)
