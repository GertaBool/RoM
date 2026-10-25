# Graphics paging: the window from the camera

[`../graphics-paging-camera.patch`](../graphics-paging-camera.patch) is GitLab commit `cadd95b3` (branch
`claude/paging-coherence`, merge request !59). It applies after
[`graphics-paging-coherence.patch`](../graphics-paging-coherence.patch), gives tree `bd6f6235`, and serves
P13 under hypothesis H8.

## Facts

- **The executable's camera settings come from the DLL.** It reads them through exported `CvGlobals`
  getters: `getFIELD_OF_VIEW`, `getCAMERA_MIN_DISTANCE`, `getCAMERA_UPPER_PITCH`,
  `getCAMERA_LOWER_PITCH` and `getPLOT_SIZE`.
- **Values in `GlobalDefines.xml`:**
  - `FIELD_OF_VIEW` is 42 and `PLOT_SIZE` is 180;
  - `CAMERA_MIN_DISTANCE` is 700 and `CAMERA_START_DISTANCE` is 2200;
  - `CAMERA_LOWER_PITCH` is -28 and `CAMERA_UPPER_PITCH` is -90.
- **The camera's greatest distance depends on the map.** It is at least `CAMERA_SMALLEST_MAX_DISTANCE`
  (7000), scaled by `CAMERA_MAX_DISTANCE_FADER` in `CIV4DetailManager.xml`.
- **The globe view takes over between 6000 and 6400 units.** The `DF_SKY` and `DF_GLOBE_TERRAIN`
  faders in `CIV4DetailManager.xml` switch over in that range.
- **Python can read the camera and the screen.** The executable's Python API has
  `CyCamera.GetCurrentPosition` and `GetLookAt`, and `CyEngine.isGlobeviewUp`. RoM's own screens
  read the resolution with `CyGInterfaceScreen.getXResolution` and `getYResolution`.
- **World units map linearly to plots.** `CvMap::plotXToPointX` is `x * width / gridWidth - width / 2 + PLOT_SIZE / 2`.
  Here `width` is the landscape's size, and the ground is the plane z = 0.

## The change

- **Reading the camera:** `CvGameInterface.getCameraView` reads the eye, the target, the resolution and
  the globe view. It uses index calls returning a long, the form the DLL already uses.
- **The footprint:** `CvGame::graphicsWindowFromCamera` builds the view's forward, right and up vectors.
  It casts rays through the 4 corners, the 4 edge midpoints and the centre onto z = 0, using
  `tan(FIELD_OF_VIEW / 2)` vertically and that times the aspect ratio horizontally.
  - A ray at or above the horizon reaches past the map.
  - Each side of the window is the footprint's extent from the look-at plot's centre in plots, plus one.
  - The camera is rejected, and the defines window used instead, when:
    - the eye is not above its target;
    - the eye is closer than half of `CAMERA_MIN_DISTANCE`;
    - the centre ray lands more than 3 plots from the look-at plot.
- **How the window changes:** `CvGame::updateGraphicsPaging` keeps west, east, north and south
  separately.
  - A side that grows applies at once.
  - A smaller window applies after `GRAPHICS_PAGING_SHRINK_MS`.
  - In globe view nothing changes.
- **Removed:** `GRAPHICS_PAGING_ZOOM`, `_ZOOM_SAFETY_PERCENT`, `_ZOOM_MIN_PERCENT` and `getCameraZoom`.

## Validation

- **Build:** MSVC 2003 release `526bbebe2dc9`, 0 errors and 0 warnings.
- **Clang gate:** 0 new diagnostics ([clang-gate.log](clang-gate.log)).
- **The geometry:** with harness cameras (`HARNESS_CAMERA_VIEW`), the windows the DLL logs equal an
  independent ray-plane computation in all four cases. The one exception is the north side at 6000
  units and 28°, which the DLL clamps to the map's 73 rows; the geometry gives 100.

| Distance, pitch, turn, screen | West | East | North | South |
|---|---|---|---|---|
| 2200, 45°, 0°, 1920×1080 | 15 | 15 | 12 | 6 |
| 700, 28°, 0°, 1920×1080 | 11 | 11 | 13 | 3 |
| 6000, 80°, 30°, 2560×1080 | 32 | 37 | 30 | 26 |
| 6000, 28°, 0°, 1920×1080 | 83 | 83 | 73 | 17 |

- **P13 evidence:** pending.
- **In game:** not yet tested.
