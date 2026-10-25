# Graphics paging: the camera read through CvScreensInterface

[`../graphics-paging-interface.patch`](../graphics-paging-interface.patch) applies to GitLab `main`
`4ec8ebc` (tree `4985d7da` after it) and serves P15, under hypothesis H9
(`method/mission/register.json`). P14 was the same change; it was withdrawn before any evidence,
because its paths left out the harness, which had to change to build against `main` at all.

## The fault

Facts from the code:
- **!57 added `Assets/Python/EntryPoints/CvGameInterface.py` to the mod** (commit `ccbc1b5`, "the
  Beyond the Sword file unchanged, plus `getCameraZoom()`"), so that the DLL could read the camera
  through `PYGameModule`. !58 and !60 kept it and added `getCameraView`.
- **The file defines 49 functions** besides the camera's. Its `gameUtils()` returns
  `CvGameUtils.CvGameUtils()`, and it never imports `CvGameInterfaceFile`.
- **Firaxis's DLL source calls 22 `CvGameInterface` functions that the file lacks.** The source is the
  BTS SDK in the GitLab repository (`beyond-the-sword-sdk-develop-functional.tar.gz`), and its
  `PYGameModule` is `"CvGameInterface"`. The 22 are `canBuild`, `canDeclareWar`, `canFoundCitiesOnWater`,
  `canPickPlot`, `canRazeCity`, `cannotFoundCity`, `cannotSpreadReligion`, `citiesDestroyFeatures`,
  `doCityCaptureGold`, `doCombat`, `doHeadquarters`, `doPillageGold`, `doReviveActivePlayer`,
  `getBuildingCostMod`, `getCityFoundValue`, `getConscriptUnitType`, `getExperienceNeeded`,
  `getExtraCost`, `getUnitCostMod`, `getUpgradePriceOverride`, `isVictory` and `unitCannotMoveInto`.
- **The mod ships BUG's `CvGameInterfaceFile.py`**, "Overrides the use of CvGameUtils with BUG's modular
  game utils dispatcher". `Assets/Config/RoMSettings.xml` registers `RoMGameUtils` with that dispatcher.
  It holds RoM's rules for `cannotConstruct`, `cannotDoCivic`, `getUnitCostMod`, `getBuildingCostMod`,
  `getUpgradePriceOverride`, `doPillageGold` and `doCityCaptureGold`.
- **`PythonCallbackDefines.xml` (main) switches five callbacks on:** unit cost, building cost, upgrade
  price, cannot construct and cannot do civic. `calculateExperience` calls `getExperienceNeeded` with no
  switch.
- **The headless harness never ran the file.** It answers every Python call in C++ (`engine.cpp`,
  `pythonDefault`), so P7 to P13 could not see it. `builds/graphics-paging*/provenance.json` record
  `tested_in_game: false`.
- **The code map's base-game Python has the same 49 functions** as the mod's file of `ccbc1b5`, at the
  same lines (`codemap/entry_points.md` lists the 22 as "not found").

Reading (H9): the mod's file shadows the game's `CvGameInterface.py`. Since !57, RoM's Python rules
above have not run in the game. `cannotConstruct` and `cannotDoCivic` went to the plain game utils.
The other five were not found. What the executable does when the DLL calls a function the module
lacks is *open*. H9 is contradicted if the installed Beyond the Sword
`Assets/Python/EntryPoints/CvGameInterface.py` is the same file, or if a game on `main` `4ec8ebc` applies
RoM's missionary cost.

## The change

- `CvGame::graphicsWindowFromCamera` calls `getCameraView` in `PYScreensModule`
  (`CvScreensInterface`), a module the DLL already calls 43 times.
- `getCameraView` moves unchanged to the mod's `Assets/Python/EntryPoints/CvScreensInterface.py`.
  That module already has `from CvScreenEnums import *`, so it names `MAIN_INTERFACE` directly.
- The mod's `Assets/Python/EntryPoints/CvGameInterface.py` is deleted.
- `Docs/GRAPHICS_PAGING.md` describes the file and the change.

With the new Python and the DLL of `4ec8ebc`, the camera cannot be read and the fixed window is used.
With the new DLL and the old Python, `CvScreensInterface` has no `getCameraView`, and the fixed
window is used as well. Each half is safe alone.

## Harness

The harness in this repository did not build against GitLab `main`. `HarnessState.cpp` called
`AI_balanceHegemon`, `AI_balanceNoWarProb` and `AI_stagedForecast`, which exist only on unmerged
branches. The notes of P11 to P13 do not say how their harness was built.

`toolchain/harness/build_dll.sh` now defines `HARNESS_BALANCE` and `HARNESS_STAGED_FORECAST` when the
source declares those functions. This follows `HARNESS_SETTLE_REACH`. It built with 0 errors against
`main` `4ec8ebc` (neither flag) and against `claude/staging-defence` plus `balance.patch` (both flags).

## Validation

- **Toolchain:** the Visual C++ Toolkit 2003 installer and the Platform SDK image match the sha256 of
  `builds/0009/provenance.json`.
  - `toolchain/setup_toolchain.sh` stops after unpacking the toolkit: under `set -e`, its alias
    loop ends with a failed test when a file name is already lower case. Its last three steps were
    run by hand.
  - Rebuilt from `4ec8ebc`, the DLL differs from `builds/graphics-paging-camera` only in its two link
    timestamps (6 bytes).
- **Build:** MSVC 2003 release `504830a0dee0`, 0 errors and 0 warnings.
- **Clang gate:** 0 new diagnostics on `CvGame.cpp` ([clang-gate.log](clang-gate.log)).
- **Patch:** `apply.py --check` and apply on a clean `4ec8ebc` checkout give tree `4985d7da`
  ([manifest.json](manifest.json)).
- **GitLab:** branch `claude/paging-interface` (`8fd92c6a`, three connector commits) holds tree
  `4985d7da`, the tested tree. Merge request !62.
  - The connector wrote the new Python lines with LF. The third commit makes them CRLF, as the rest
    of the file is.
- **P15 evidence:** 30 seeded runs per arm.
  - Setup: 20 turns from turn 0 of `PrivateMaps/Mediterranean, Huge.CivBeyondSwordWBSave` (9 players),
    `HARNESS_GRAPHICS=1`, `HARNESS_ACTIVE=0`, `HARNESS_CAMERA_FOLLOW=1`, `HARNESS_CHECK_EVERY=1`,
    `HARNESS_CAMERA_VIEW=2200,45,0,1920,1080`.
  - Arms: a is build `504830a0dee0`, b is `526bbebe2dc9` (`main` `4ec8ebc`).
  - Map: P15 names this map. The P11 to P13 notes report 16 capitals on turn 1, which fits
    `Democragphica, Huge Mediterranean` (17 players) better. Which map they used is *open*.
  - Completion: all 60 runs completed (ledger: corroborated, p nan, A 0.500).
  - Game state: the telemetry, timings aside, is identical in all 30 seed pairs.
  - Graphics lines: the turn-20 `graphics turn` line matches in only 4 pairs, because paging is timed
    by `GetTickCount`. Three repeats of arm b with one seed gave 6, 6 and 7 entities set up, against
    13 in its evidence run.
  - Executable checks (cumulative over every update):
    - arm a: no flagless live unit, route without symbol, or on-screen unit, city or feature without
      graphics;
    - arm b: no flagless live unit and no route without symbol; one check pass in one run (seed
      2074952722, before turn 15) found one on-screen unit without graphics or flag.

    The DLL logic of the two arms is the same: the harness answers `getCameraView` whatever the module.
    This one case is therefore a property of camera paging in both builds, not of this change. A
    reading: the camera had just moved to another unit, and the paging pass runs at most every
    100 ms (`updateGraphicsPaging`), while the harness plays many updates in that time.
- **In game:** not yet tested.
