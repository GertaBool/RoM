# Graphics paging: the camera read through CvScreensInterface

**Status: built and tested headless, not yet in the game.** This DLL is GitLab `main` `4ec8ebc` plus
[`fixes/graphics-paging-interface.patch`](../../fixes/graphics-paging-interface.patch) (build
`504830a0dee0`). Paging itself is unchanged from
[`builds/graphics-paging-camera`](../graphics-paging-camera/README.md).

## What changes

- **The DLL** asks `CvScreensInterface.getCameraView` for the camera, not `CvGameInterface.getCameraView`.
- **The mod's Python** gets `getCameraView` in `Assets/Python/EntryPoints/CvScreensInterface.py`.
- **The mod's `Assets/Python/EntryPoints/CvGameInterface.py` goes.** It came with graphics paging in
  merge request !57 and was described as the Beyond the Sword file unchanged. It is not that file:
  - it lacks 22 functions that Firaxis's own DLL calls, among them `getUnitCostMod`,
    `getBuildingCostMod`, `getUpgradePriceOverride`, `getExperienceNeeded`, `doPillageGold` and
    `doCityCaptureGold`;
  - it hands every call to the plain `CvGameUtils`, not to BUG's dispatcher, which is how RoM's
    `RoMGameUtils` rules are reached (`Assets/Config/RoMSettings.xml`).

  Without the file, the game's own `CvGameInterface.py` answers again.

## Install

In `Mods/Rise of Mankind/`:

| Step | File |
|---|---|
| Copy `CvGameCoreDLL.dll` to | `Assets/CvGameCoreDLL.dll` |
| Copy `CvScreensInterface.py` to | `Assets/Python/EntryPoints/CvScreensInterface.py` |
| Copy `GlobalDefinesAlt.xml` to | `Assets/XML/GlobalDefinesAlt.xml` (the same file as the camera build's) |
| **Delete** | `Assets/Python/EntryPoints/CvGameInterface.py` |

Copying files over an installed mod does not delete anything, so the last step has to be done by hand.
With the new Python and an older paging DLL, the camera cannot be read and the fixed window
(`GRAPHICS_PAGING_RANGE_*`) is used.

Saves move freely between this DLL and the earlier ones.

## What to look for in the game

- RoM's missionary cost (75 % under a state religion civic), the civic and Djenne building
  discounts, and Personal Replicators halving upgrade prices. With the file removed they should
  apply again.
- `Logs/PythonErr.log` should hold no `getCameraView` errors. With `GRAPHICS_PAGING_LOG` 1,
  `Logs/GraphicsPaging.log` should say "camera", not "defines".
