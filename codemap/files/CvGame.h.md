# CvGame.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **514** `CvGame::AI_init(…)` (virtual; pure virtual)
  - called by (1): CvGame::init
- **515** `CvGame::AI_reset(…)` (virtual; pure virtual)
  - called by (1): CvGame::reset
- **516** `CvGame::AI_makeAssignWorkDirty(…)` (virtual; pure virtual)
  - called by (2): CvGame::setHeadquarters, CvGame::setHolyCity
- **517** `CvGame::AI_updateAssignWork(…)` (virtual; pure virtual)
  - called by (1): CvGame::update
- **518** `CvGame::AI_combatValue(…)` (virtual; pure virtual)
