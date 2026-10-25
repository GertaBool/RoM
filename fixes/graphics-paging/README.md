# Graphics paging (patch `graphics-paging.patch`)

The patch applies to GitLab `main` `c42be8b`. The design is G1 in `research/graphics/README.md`,
section 5; the user build and its test steps are in `builds/graphics-paging/`.

## Code

| Where | What |
|---|---|
| `CvGame::updateGraphicsPaging`, `CvGame::pageGraphics` | Each update reads `getLookAtPlot()`. When the camera has moved two plots, or every 500 ms, a pass over the map: inside the window, plots, units and cities are paged in; outside the window and its margin, they are paged out. The window scales with `CvGameInterface.getCameraZoom` when `GRAPHICS_PAGING_ZOOM` is set; if that call fails once, it is not asked again. World Builder and `GRAPHICS_PAGING` 0 page everything back in. |
| `CvUnit::pageGraphics`, `CvCity::pageGraphics` | Out: `RemoveUnitFromBattle` (units), `removeEntity`, `destroyEntity`, then a new bare entity (as the constructor makes it). In: `setup`, and for cities `setInfoDirty`, `setLayoutDirty`, `updateVisibility`. Never paged out: the active player's units and cities, and units fighting, attacking, dying or in combat focus. `setupGraphical` leaves a new unit or city bare when it is outside the window. |
| `CvPlot::pageGraphics` | Out: the feature and route symbols and the plot builder are destroyed. In: `updateFeatureSymbol(true)`, `updateRouteSymbol(true)`, `setLayoutDirty(true)`. While out, `updateFeatureSymbol`, `updateRouteSymbol`, `setLayoutDirty` and `updatePlotBuilder` make nothing. Rivers, flags and the terrain stay. |
| `CvDLLEntity` | Flag `m_bGraphicsPagedOut` (not saved). While it is set, the visual wrappers (`setVisible`, animations, moves, `NotifyEntity`, siege tower, `IsSelected`) do nothing. |
| `addEntityMission` (`CvGameCoreUtils`) | Replaces the 29 direct `AddMission` calls. A paged-out unit in a mission is paged in when the mission's plot is visible to the active team; otherwise the mission (a visual only) is skipped. |
| `CvUnit::isCombatVisible`, `CvUnit::setXY` | A battle that will be shown pages both units in. A unit about to be shown moving, or moving into the window, is paged in at the plot it leaves. |
| Direct entity calls | `updateEnemyGlow` (`CvUnit`, `CvGame`, `CvPlayer`), `updateGraphicEra`, `showPromotionGlow`, `updatePromotionLayers`: skipped for paged-out units. |
| `CvCity::isInfoDirty`, `isLayoutDirty` | False while the city is paged out, so the executable does not rebuild its billboard or layout. |
| `GlobalDefinesAlt.xml` | The `GRAPHICS_PAGING*` defines. |
| `Assets/Python/EntryPoints/CvGameInterface.py` | New in the mod: the Beyond the Sword file unchanged, plus `getCameraZoom()`. |

## Differences from the registered description (P7, P8)

The register's change text was written before the build:
- **Battles.** It said battles of paged-out units are not animated. As built, a battle that would
  be shown pages both units in first, so it is animated as before.
- **Window.** It said the window is sized for the farthest zoom. As built, that is its widest
  size, and it shrinks with the camera zoom when `GRAPHICS_PAGING_ZOOM` is 1.

The harness has no Python, so it did not exercise the zoom scaling; whether it showed any battle is not counted.

## Validation

- Build: MSVC 2003, release, 0 errors and 0 warnings; harness build of the same source likewise.
- Clang gate (`clang-gate.log`): no new diagnostics in the eight changed `.cpp` files.
- `apply.py --check` on a clean `c42be8b` checkout passes (`manifest.json`).
- Harness (`toolchain/harness/README.md`, Graphics):
  - Setup: the 460 AD autosave, graphics set up after loading, a camera sweeping the map one
    plot per update, 3 turns per run, 30 seeded runs per arm for P7 and for P8.
  - Every run completed, in both arms.
  - In all 60 seed pairs, the game state after 3 turns and the telemetry (timings aside) are
    identical with paging on and off.
  - The visual calls that reach an entity not set up are the same in both arms.
  - Per-run values: `harness-runs.json`, made by `tools/paging_summary.py`.
- Ledger:
  - P7 (`completed`, a >= b): corroborated, p nan, A 0.500.
  - P8 (`turn_seconds`, a <= b): corroborated, p 0.9651, A 0.497.
- Not tested: the game itself (the memory saved, the window against the screen, the zoom scale).
