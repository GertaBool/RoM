# CyArgsList.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **16** `CyArgsList::CyArgsList()` (exported)
  - called by (191): CvCity::canConstruct, CvCity::canCreate, CvCity::canMaintain, CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const, CvCity::doCulture, CvCity::doGreatPeople, CvCity::doGrowth, CvCity::doMeltdown, CvCity::doPlotCulture, CvCity::doProduction, CvCity::doReligion, CvCity::getConscriptUnit …
- **18** `CyArgsList::add(unsigned int)` (exported)
  - calls: CyArgsList::add(int) [CyArgsList.cpp]
- **28** `CyArgsList::size() const` (exported)
- **29** `CyArgsList::push_back(void*)` (exported)
  - called by (9): CyArgsList::add(char const*), CyArgsList::add(char const*, int), CyArgsList::add(float const*, int), CyArgsList::add(float), CyArgsList::add(int const*, int), CyArgsList::add(int), CyArgsList::add(unsigned char const*, int), CyArgsList::add(unsigned short const*), CyArgsList::add(void*)
- **30** `CyArgsList::clear()` (exported)
- **·** `CvPopupInfo::`default ctor closure'()` (exported; written by the compiler)
  - calls: CvPopupInfo::CvPopupInfo [CvPopupInfo.cpp]
