# CvDLLFlagEntityIFaceBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **33** `CvDLLFlagEntityIFaceBase::create(PlayerTypes)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **35** `CvDLLFlagEntityIFaceBase::getPlayer(CvFlagEntity *)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **36** `CvDLLFlagEntityIFaceBase::getPlot(CvFlagEntity *)` (virtual; pure virtual, provided by the exe)
- **37** `CvDLLFlagEntityIFaceBase::setPlot(CvFlagEntity *, CvPlot *, bool)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **38** `CvDLLFlagEntityIFaceBase::updateUnitInfo(CvFlagEntity *, const CvPlot *, bool)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateFlagSymbol
- **39** `CvDLLFlagEntityIFaceBase::updateGraphicEra(CvFlagEntity *)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updateGraphicEra
- **40** `CvDLLFlagEntityIFaceBase::setVisible(CvFlagEntity *, bool)` (virtual)
  - calls: CvDLLEntityIFaceBase::setVisible [CvDLLEntityIFaceBase.h], CvDLLUtilityIFaceBase::getEntityIFace [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h], CvGlobals::getInstance [CvGlobals.h]
- **41** `CvDLLFlagEntityIFaceBase::destroy(CvFlagEntity *&, bool)` (virtual; pure virtual, provided by the exe)
  - called by (2): CvPlot::uninit, CvPlot::updateFlagSymbol
