# Graphics paging: the crash while zooming fast

[`../graphics-paging-zoom.patch`](../graphics-paging-zoom.patch) applies to GitLab `main` `3bec049` (tree
`c3dc2a44` after it) and serves P20, under hypothesis H11 (`method/mission/register.json`).

## The crash

The user's game crashed at turn 108 while they zoomed in and out fast to test paging: 20 civilizations on
an edited huge Europe map, under Proton. Facts from the session's `GraphicsPaging.log` and
`PythonDbg.log`:
- **Before:** 105 passes set up 2,282 plots, 21 units and 7 cities again. The most in one pass was 238
  plots, 2 units and 1 city, at turn 107.
- **The last pass:** the window grew from 60 x 43 to 60 x 65 plots in 0.3 s. One pass then set up 918
  plots, 6 units and 2 cities again in a single update, four times the previous most.
- **Tile art:** each of those plots also had its tile art rebuilt. `CvPlot::pageGraphics(true)` called
  `updateFeatureSymbol(true)`, which calls `RebuildTileArt` first. Paging never removes tile art.
- **After:** no further pass is logged. Python logged about 4 s more without an error (the two clocks
  lined up at the turn 107/108 change, within about a second).
- **Not obtained:** a crash address. Which code failed is not known.

## The change

| Part | Change |
|---|---|
| Tile art | `CvPlot::pageGraphics(true)` gives the plot its feature symbol again through the new `CvPlot::updateFeatureSymbolEntity`, the part of `updateFeatureSymbol` after `RebuildTileArt`. A feature that changes while the plot is paged out still rebuilds the tile art, as before. |
| Spread | `CvGame::pageGraphics(false)` sets up at most `GRAPHICS_PAGING_MAX_IN` (100) plots, units and cities again. The rest of the window waits, and `CvGame::updateGraphicsPaging` goes on at the next update, before reading the camera again. Page-outs are not limited. |
| Log | A pass that stopped at the limit is logged as "pass, more next update". |

`GRAPHICS_PAGING_MAX_IN` 0 removes the limit. The tile-art change has no switch. Nothing new is saved.

**What it costs on screen:** while a large set-up is spread out, part of the newly shown area lacks its
units' models, flags and feature symbols. The game updates many times a second, so 918 plots take about
ten updates.

## Validation

- **Build:** MSVC 2003 release `59db478feb3c`, all 103 source files compiled, 0 errors and 0 warnings.
- **Clang gate:** 0 new diagnostics on `CvGame.cpp` and `CvPlot.cpp` ([clang-gate.log](clang-gate.log)).
- **Patch:** `apply.py` on a clean `3bec049` gives tree `c3dc2a44` ([manifest.json](manifest.json)).
- **Harness pilot** (one seed per arm, 20 turns, zooming: not evidence):
  - `main` set up 352 plots in one pass;
  - this build set up at most 100 per pass and finished in the following passes.
- **P20 evidence:** pending.
- **In game:** not yet tested.
