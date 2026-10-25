# CvDLLFlagEntityIFaceBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **33** `CvDLLFlagEntityIFaceBase::create(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **35** `CvDLLFlagEntityIFaceBase::getPlayer(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **37** `CvDLLFlagEntityIFaceBase::setPlot(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **38** `CvDLLFlagEntityIFaceBase::updateUnitInfo(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **39** `CvDLLFlagEntityIFaceBase::updateGraphicEra(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateGraphicEra
- **41** `CvDLLFlagEntityIFaceBase::destroy(…)` (virtual; pure virtual, provided by the exe)
  - called by (2): CvPlot::uninit, CvPlot::updateFlagSymbol
