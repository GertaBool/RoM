# CvDLLPlotBuilderIFaceBase.h

Group: engine interface. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **17** `CvDLLPlotBuilderIFaceBase::init(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updatePlotBuilder
- **18** `CvDLLPlotBuilderIFaceBase::create(…)` (virtual; pure virtual, provided by the exe)
  - called by (1): CvPlot::updatePlotBuilder
- **21** `CvDLLPlotBuilderIFaceBase::destroy(…)` (virtual; declared, not defined in the source)
  - called by (1): CvPlot::uninit
