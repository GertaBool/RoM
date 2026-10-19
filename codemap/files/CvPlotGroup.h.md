# CvPlotGroup.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **33** `CvPlotGroup::getOwnerINLINE()`
  - called by (6): CvPlotGroup::addPlot, CvPlotGroup::changeNumBonuses, CvPlotGroup::deletePlotsNode, CvPlotGroup::getOwner, CvPlotGroup::recalculatePlots, CvPlotGroup::removePlot
