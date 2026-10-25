# Graphics paging: the window is what the camera shows

**Status: built and tested headless, not yet in the game.** This DLL is GitLab `main` `d929b57` plus
merge request !59 (build `526bbebe2dc9`, branch `claude/paging-coherence` `cadd95b3`). It has two parts:
- **The crash fix** (`fixes/graphics-paging-coherence.patch`): a plot keeps its graphics while anything
  on it keeps its own, and roads always stay.
- **The window** (`fixes/graphics-paging-camera.patch`): the paging window is computed from the camera.

## How the window is computed

What the screen shows follows from the camera:
- **The camera:** its eye and target, from `CyCamera().GetCurrentPosition()` and `GetLookAt()`.
- **The field of view:** `FIELD_OF_VIEW` (42° in `GlobalDefines.xml`). The executable takes it from the
  DLL (`CvGlobals::getFIELD_OF_VIEW`).
- **The screen's aspect ratio:** from its resolution.

The DLL casts rays from the eye through the corners and edge midpoints of the view onto the map's
ground plane. A plot is 180 world units (`PLOT_SIZE`). The extent of those hits west, east, north and
south of the look-at plot, plus one plot, is the window. Paging out starts `GRAPHICS_PAGING_MARGIN`
(4) plots beyond it.

Some example windows on a 1920×1080 screen:

| Camera distance, pitch | West | East | North | South |
|---|---|---|---|---|
| 700, 28° (closest) | 11 | 11 | 13 | 3 |
| 2200, 45° | 15 | 15 | 12 | 6 |
| 6000, 28° | 83 | 83 | up to 100 | 17 |

The last row reaches far past the old fixed window (40 each side, 40 north, 16 south). The window
the DLL computes matches an independent calculation in every case tested.

## How the window follows the camera

- When the screen shows more (zooming out, tilting, turning), the window grows at once.
- When it shows less, the window shrinks only after 5 seconds (`GRAPHICS_PAGING_SHRINK_MS`), so zooming
  in and out does not rebuild graphics.
- In globe view nothing is paged in or out.
- If the camera cannot be read, the old fixed window (`GRAPHICS_PAGING_RANGE_*`) is used.
  `GRAPHICS_PAGING_CAMERA` 0 also selects it.

## Install

Copy into `Mods/Rise of Mankind/`:

| File here | Goes to |
|---|---|
| `CvGameCoreDLL.dll` | `Assets/CvGameCoreDLL.dll` |
| `GlobalDefinesAlt.xml` | `Assets/XML/GlobalDefinesAlt.xml` |
| `CvGameInterface.py` | `Assets/Python/EntryPoints/CvGameInterface.py` |

Saves move freely between this DLL and the earlier ones.
