# FFreeListArrayBase.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **35** `FFreeListArrayBase::~FFreeListArrayBase<T>()` (virtual)
- **36** `FFreeListArrayBase::init(int)` (virtual; pure virtual, provided by the exe)
- **37** `FFreeListArrayBase::uninit()` (virtual; pure virtual, provided by the exe)
- **38** `FFreeListArrayBase::getAt(int)` (virtual; pure virtual, provided by the exe)
  - called by (3): FFreeListArrayBase::nextIter, FFreeListArrayBase::operator[], FFreeListArrayBase::prevIter
- **54** `FFreeListArrayBase::getIndexAfterLast()`
  - called by (4): CvGame::getIndexAfterLastDeal, CvMap::getIndexAfterLastArea, FFreeListArrayBase::endIter, FFreeListArrayBase::nextIter
- **57** `FFreeListArrayBase::getCount()`
  - called by (7): CvGame::getNumDeals, CvMap::getNumAreas, CvPlayer::getNumCities, CvPlayer::getNumEventsTriggered, CvPlayer::getNumPlotGroups, CvPlayer::getNumSelectionGroups, CvPlayer::getNumUnits
- **59** `FFreeListArrayBase::removeAll()` (virtual; pure virtual, provided by the exe)
- **66** `FFreeListArrayBase::growArray()` (virtual; pure virtual, provided by the exe)
- **69** `FFreeListArrayBase::FFreeListArrayBase<T>()`
- **83** `FFreeListArrayBase::operator[](int)`
  - calls: FFreeListArrayBase::getAt
- **94** `FFreeListArrayBase::beginIter(int *)`
  - calls: FFreeListArrayBase::nextIter
  - called by (8): CvGame::doVoteResults, CvGame::firstDeal, CvMap::firstArea, CvPlayer::firstCity, CvPlayer::firstEventTriggered, CvPlayer::firstPlotGroup, CvPlayer::firstSelectionGroup, CvPlayer::firstUnit
- **102** `FFreeListArrayBase::nextIter(int *)`
  - calls: FFreeListArrayBase::getIndexAfterLast, FFreeListArrayBase::getAt
  - called by (9): CvGame::doVoteResults, CvGame::nextDeal, CvMap::nextArea, CvPlayer::nextCity, CvPlayer::nextEventTriggered, CvPlayer::nextPlotGroup, CvPlayer::nextSelectionGroup, CvPlayer::nextUnit, FFreeListArrayBase::beginIter
- **118** `FFreeListArrayBase::endIter(int *)`
  - calls: FFreeListArrayBase::getIndexAfterLast, FFreeListArrayBase::prevIter
  - called by (7): CvGame::firstDeal, CvMap::firstArea, CvPlayer::firstCity, CvPlayer::firstEventTriggered, CvPlayer::firstPlotGroup, CvPlayer::firstSelectionGroup, CvPlayer::firstUnit
- **126** `FFreeListArrayBase::prevIter(int *)`
  - calls: FFreeListArrayBase::getAt
  - called by (8): CvGame::nextDeal, CvMap::nextArea, CvPlayer::nextCity, CvPlayer::nextEventTriggered, CvPlayer::nextPlotGroup, CvPlayer::nextSelectionGroup, CvPlayer::nextUnit, FFreeListArrayBase::endIter
