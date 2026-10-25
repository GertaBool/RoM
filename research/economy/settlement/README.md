# Settlement Economy: a quantitative design study

[settlement-economy.pdf](settlement-economy.pdf) measures how a goods economy, in which settlements make, use, store
and trade quantities of goods, would behave in Rise of Mankind, and what each implementation choice in the codebase
changes. It rebuilds the settlements of the 30 baseline harness games of P18 (build 504830a0dee0, GitLab main 3bec049,
Mediterranean Standard, 150 turns) from their telemetry, checks them against the games, and runs a deterministic,
integer-only model of the proposed rules on them under eleven variants. It also measures what buildings, civics,
specialists and trade routes add to the land's yields, and what the goods pass and the AI's valuation cost per turn.

It is a design study, not a change: nothing in the mod is altered, and no prediction is registered for it.
Companion to [Land, not tokens](../land-and-industry.pdf).

| File | What it is |
|---|---|
| `tools/games.py` | Settlements, populations, production and commerce rates, and deals of harness games, from their telemetry |
| `tools/bc.py` | What every building and civic does to food, production, commerce, growth and trade (XML records) |
| `tools/model.py` | The reference model: plot goods, needs, recipes, integer rationing, stores, spoilage, governors; eleven variants |
| `tools/calibrate.py` | The rebuilt cities' food against the populations the games fed, in three stages |
| `tools/analysis.py` | Per-turn needs met, shortfalls by city size, the floating-point check, land capacity per citizen |
| `tools/yields.py` | Observed production and commerce against the rebuilt plots; trade-route profits; food under Oral Law |
| `tools/calibrate_needs.py` | Need levels per citizen solved from design targets (share of citizens supplied) by bisection over the 30 games; writes `data/needs_derived.json` |
| `tools/bench.c` | Cost of the goods pass and of the AI's marginal values, in C |
| `tools/sfigures.py`, `tools/sbuild.py` | Figures and the PDF; every quoted number is read from `data/` |
| `tools/run_all.sh` | The whole study in order |
