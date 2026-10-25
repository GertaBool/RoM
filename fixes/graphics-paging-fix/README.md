# Graphics paging fix: plot builders kept, a switch per part

[`../graphics-paging-fix.patch`](../graphics-paging-fix.patch) applies to GitLab `main` `a459d0d8`
(tree `04ac18c6`) and gives tree `b605bb93`. GitLab branch `claude/graphics-paging-fix` (`9b3afb3b`)
holds the same tree. It serves P11, under hypothesis H6 (`method/mission/register.json`).

## The fault

The user reported a freeze at the first city founded with `main` `a459d0d8`. These are the facts
from the logs the user sent:
- `PythonDbg.log` ends after `PY:City Built Event: London` and `Timer - scores took 5 ms`.
- `LSystem.log` ends after the city and plot L-system tables and two `no generic art` warnings.
- `PythonErr.log` shows one `TypeError: getCameraZoom() takes no arguments (1 given)`.

These are the facts from the code (GitLab `c42be8b`, `CvPlot.cpp`):
- `PlotBuilderIFace()->destroy` is called only in `CvPlot::uninit`.
- Feature, route and yield symbols and flags are destroyed and remade in vanilla update
  functions.
- Unit and city entities are destroyed in `kill`.

Paging's `CvPlot::pageGraphics(false)` destroyed the plot builder mid-game.

Reading (H6): the executable does not expect a plot builder to go away during a game. It shares
its L-system with city layouts, and the first city layout comes at the first city. H6 is
contradicted if the game still freezes at the first city with `GRAPHICS_PAGING_PLOT_BUILDERS` 0, or
does not freeze with it 1.

## The change

- `GRAPHICS_PAGING_UNITS`, `_CITIES`, `_PLOTS` (feature and route symbols) and `_PLOT_BUILDERS`
  switch each part. All are 1 except plot builders, which are 0. `GRAPHICS_PAGING_SYMBOLS` stays.
- `CvGame::pageGraphics` pages out only the parts that are on; paging in always runs.
- A plot keeps three bits saying what its page-out removed (`m_bPagedPlots`, `m_bPagedBuilder`,
  `m_bPagedSymbols`). Its update guards and its page-in act only on those.
- `CvGameInterface.getCameraZoom(argsList=None)`.

## Harness

The headless harness gained two settings for this fix (`toolchain/harness/main.cpp`,
`HarnessHooks.cpp`):
- `HARNESS_GRAPHICS=1` now also sets up graphics in WorldBuilder scenario runs.
- `HARNESS_ACTIVE=<player>` gives an all-AI game an active player.

Without an active player, the vanilla display branch of `CvPlot::calculateYield` indexes
`m_aiRevealedOwner` with `NO_TEAM`. The harness then crashed in `CvPlot::updateSymbols` from
`setOwner` when the first cities were founded, with or without paging. The real game always has an
active player, so that crash was the harness's, not the user's freeze.

## Validation

- **Build:** MSVC 2003 release, 0 errors and 0 warnings.
- **Clang gate:** 0 new diagnostics on the four changed `.cpp` files ([clang-gate.log](clang-gate.log)).
- **Harness evidence for P11:** pending.
- **In game:** not yet tested.
