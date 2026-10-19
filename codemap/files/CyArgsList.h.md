# CyArgsList.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **16** `CyArgsList::CyArgsList()` (exported)
  - called by (191): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool), CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCity::getConscriptUnit …
- **18** `CyArgsList::add(uint)` (exported)
  - calls: CyArgsList::add(int) [CyArgsList.cpp]
- **28** `CyArgsList::size()` (exported)
- **29** `CyArgsList::push_back(void *)` (exported)
  - called by (9): CyArgsList::add(const byte *, int), CyArgsList::add(const char *), CyArgsList::add(const char *, int), CyArgsList::add(const float *, int), CyArgsList::add(const int *, int), CyArgsList::add(const wchar *), CyArgsList::add(float), CyArgsList::add(int), CyArgsList::add(void *)
- **30** `CyArgsList::clear()` (exported)
