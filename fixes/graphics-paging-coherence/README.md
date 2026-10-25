# Graphics paging coherence: a plot keeps its graphics while anything on it keeps its own

[`../graphics-paging-coherence.patch`](../graphics-paging-coherence.patch) is GitLab commit
`006b7840` (branch `claude/paging-coherence`) on `main` `d929b57`. It gives tree `add8bed3` and
serves P12, under hypothesis H7.

## The fault

With `main` `d929b57`, the user's game crashed when the first unit was moved.

Facts from the code: `CvGame::pageGraphics` paged a plot and the units on it independently. A
plot outside the window lost its yield symbols, flags (`GRAPHICS_PAGING_SYMBOLS`), feature and
route symbols (`GRAPHICS_PAGING_PLOTS`). This happened whether or not a unit or city on it kept
its entity, and the active player's always do.

Facts from the executable (the DLL functions it binds by name): it calls
- `CvPlot::updateFlagSymbol`, `getFlagSymbol` and `getCenterUnit`;
- `CvPlot::getRouteSymbol`, `isRoute` and `shouldDisplayBridge`;
- `CvMap::updateFlagSymbols` and `updateCenterUnit`.

## The check

The harness now holds tokens for every symbol, feature, route, flag and plot builder (`engine.cpp`).
`HH_graphicsCheck` (`HarnessHooks.cpp`) calls `CvMap::updateFlagSymbols`, as the executable does,
and then counts states the unchanged DLL never shows:
- a center unit with its graphics but no flag;
- a revealed route without its symbol;
- on screen: a unit or city without graphics, a feature without its symbol, or a center unit
  without a flag.

Results, 100 turns from turn 0 of the Huge Mediterranean map (`HARNESS_ACTIVE=0`, a check every
update):

| Build | Camera | Flagless live units | Routes without symbol | On-screen units without flag |
|---|---|---|---|---|
| `c42be8b` (before paging) | follow / sweep | 0 / 0 | 0 / 0 | 0 / 0 |
| `d929b57` | follow / sweep | 27 / 62 | 58 / 75 | 4 / 0 |
| this patch | follow / sweep | 0 / 0 | 0 / 0 | 0 / 0 |

The telemetry, apart from timings, is identical across the three builds in both camera modes.

## The change

- **`CvPlot::canPageGraphicsOut`:** false while a unit or city on the plot keeps its graphics, or
  while the single-move goto plot is this one. `pageGraphics(false)` checks it.
- **`CvGame::pageGraphics`:** pages a plot in before its units and city, and out after them.
- **Plots come back with what stands on them:** `CvUnit::setupGraphical`, `CvUnit::pageGraphics(true)`,
  `CvCity::setupGraphical` and `CvCity::pageGraphics(true)` bring their plot back first, and
  `CvUnit::setXY` does so for the plot moved to.
- **`CvPlot::updateFlagSymbol`:** brings a paged-out plot back when it may not stay paged out.
- **Routes:** never paged. `GRAPHICS_PAGING_PLOTS` pages feature symbols only.
- **`GRAPHICS_PAGING_ZOOM`:** 0 by default.

## Validation

- **Build:** MSVC 2003 release `dd2152452c46`, 0 errors and 0 warnings.
- **Clang gate:** 0 new diagnostics ([clang-gate.log](clang-gate.log)).
- **P12 evidence:** pending.
- **In game:** not yet tested.
