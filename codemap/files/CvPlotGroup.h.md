# CvPlotGroup.h

Group: game objects. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **34** `CvPlotGroup::getOwnerINLINE() const`
  - called by (7): CvPlotGroup::addPlot, CvPlotGroup::changeNumBonuses(BonusTypes, int), CvPlotGroup::changeNumBonuses(std::vector<int, std::allocator<int>> const&), CvPlotGroup::deletePlotsNode, CvPlotGroup::getOwner, CvPlotGroup::recalculatePlots, CvPlotGroup::removePlot
