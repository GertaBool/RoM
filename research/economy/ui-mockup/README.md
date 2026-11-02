# UI mock-up (R9, M52)

A mock-up of what the planned in-game screens would show, published as a Design canvas:
https://claude.ai/artifact/JjCX63Da4ix16sN4oCX1mD (private to the owner). This folder holds its source files.

Four artboards, each from the plan's features and the statement, not from code (none of these screens exists yet):
- `Main.dc.html`: the city screen's goods panel (UI.F1), with the food store (FG.F1), needs per category (CN.F1)
  and the accounts GW.F3 keeps (stock, produced, received, sent, consumed, spoiled).
- `Pedia.dc.html`: the Civilopedia page of Dairy (UI.F2): unit, category, need, how it keeps, sources, uses.
- `PlotHelp.dc.html`: plot help over the map (LD.F6): each land quality with a band word and ore depth.
- `Contract.dc.html`: a supply contract on the diplomacy screen (TR.F1, TR.F2, D7), the statement's example package.

From the records: units and categories (GitLab 4bea4e0e), needs and roles (proposals.json), building names.
Made up: every quantity. Open and shown one possible way: how goods with different units add up within one need
(CN.F1.T3); grouping the panel by category.
