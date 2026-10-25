# Graphics paging: unit, city and plot graphics only near the camera

**Status: tested headless, not yet in the game.** This DLL is GitLab `main` `c42be8b` plus one
change: graphics paging (`fixes/graphics-paging.patch`, build `72dcbedc28f7`). Its DLL source,
`GlobalDefinesAlt.xml` and Python are those of `2a8b9a83`, the build of your Mediterranean game,
plus this change.

## What it changes

Your 460 AD game ended at 490 AD with the executable's memory allocation failure. The executable
builds a model for every unit and city and the trees, roads and improvements of every plot, on
screen or not (`research/graphics/README.md`, R-C). With paging on:

- Graphics are kept only in a window around the plot the camera looks at. Units and cities
  outside it keep an empty entity; plots outside it drop their feature (trees), route and
  improvement graphics.
- When the camera comes near again, they are rebuilt. The window is larger than the screen, so
  this happens off screen.
- Your own units and cities always keep their graphics, wherever they are, as do units fighting
  or dying.
- An AI unit outside the window that you would see move or fight gets its graphics first.
- Nothing is saved and the game plays the same. Saves move freely between this DLL and the old one.

The window follows the camera zoom: zoomed in, it is smaller.

## Install

Back up the three files first, then copy:

| File here | Goes to (in `Mods/Rise of Mankind/`) |
|---|---|
| `CvGameCoreDLL.dll` | `Assets/CvGameCoreDLL.dll` |
| `GlobalDefinesAlt.xml` | `Assets/XML/GlobalDefinesAlt.xml` (main's file plus the defines below) |
| `CvGameInterface.py` | `Assets/Python/EntryPoints/CvGameInterface.py` (new: the Beyond the Sword file plus one function, `getCameraZoom`) |

## What to check in the game

1. **The screen.** Load the 460 AD autosave, zoom all the way out and pan around. Look for units,
   cities, trees or roads that are missing near the screen edges or pop in on screen. If you
   see any, raise `GRAPHICS_PAGING_RANGE_X`, `_NORTH` and `_SOUTH` (or set `GRAPHICS_PAGING_ZOOM`
   to 0 first, to rule out the zoom scaling) and tell me which edge it was.
2. **Memory.** In Task Manager, open *Details*, find `Civ4BeyondSword.exe` and add the
   *Commit size* column. Note it a minute after loading the 460 AD autosave, and again after
   ten turns. Do it once with `GRAPHICS_PAGING` 1 and once with 0 (restart the game after
   changing the XML).
3. **Play past 490 AD** with paging on.
4. If something looks wrong, set `GRAPHICS_PAGING_LOG` to 1 (with `LoggingEnabled = 1` in
   `CivilizationIV.ini`) and send `Logs/GraphicsPaging.log`. It records the camera zoom the DLL
   reads and how many units, cities and plots each pass paged.

## Switches in `GlobalDefinesAlt.xml`

| Define | Default | Meaning |
|---|---|---|
| `GRAPHICS_PAGING` | 1 | 0: graphics everywhere, as before |
| `GRAPHICS_PAGING_RANGE_X` | 40 | Plots east and west of the look-at plot, at the widest zoom |
| `GRAPHICS_PAGING_RANGE_NORTH` | 40 | Plots north (the far side of the screen), at the widest zoom |
| `GRAPHICS_PAGING_RANGE_SOUTH` | 16 | Plots south, at the widest zoom |
| `GRAPHICS_PAGING_MARGIN` | 4 | Plots beyond the window that keep whatever they have, so a camera moving back and forth does not rebuild |
| `GRAPHICS_PAGING_STEP` | 2 | Plots the camera moves before the window follows at once |
| `GRAPHICS_PAGING_INTERVAL_MS` | 500 | Milliseconds between passes while the camera stands still |
| `GRAPHICS_PAGING_ZOOM` | 1 | 1: the window shrinks as you zoom in; 0: always the widest size |
| `GRAPHICS_PAGING_ZOOM_SAFETY_PERCENT` | 150 | At zoom z (0 to 1), the window is z times this percent of the widest, at most 100 % |
| `GRAPHICS_PAGING_ZOOM_MIN_PERCENT` | 35 | The window never shrinks below this percent of the widest |
| `GRAPHICS_PAGING_LOG` | 0 | 1: log each pass to `Logs/GraphicsPaging.log` |

## What is known, and what is open

Measured in the headless harness, from the 460 AD autosave, 3 turns per run, 30 seeded runs with
paging on and 30 off for each of the two predictions:
- **All 120 runs completed.** In every seed pair the game state after three turns is identical
  with paging on and off.
- **No new calls on empty entities.** Visual calls reaching an entity that was not set up are
  equal in both arms, so paging adds none.
- **Fewer entities set up.** Units and cities with graphics at turns 357 to 359: 1,813, 1,780 and
  1,190 on average with paging, against 2,689, 2,736 and 2,782 without.
- **Not slower.** P7 (runs complete) and P8 (turn time no worse) are both corroborated:
  turn-time p 0.97, A 0.50.

The harness has no camera zoom, so its window was always the widest; at normal zoom, more is
paged out.

*Open:*
- **Memory saved.** How much memory this saves in the executable: the harness counts entities,
  not bytes. Your Task Manager reading answers it.
- **Window size.** Whether the defaults cover the screen at the widest zoom. They are estimated,
  not measured, from the camera defines (distance 7000, field of view 42 to 48 degrees). At a
  45-degree pitch the far corners of the screen may lie beyond 40 plots, so the far edge at the
  widest zoom is the first place to look.
- **Zoom scale.** Whether `CyCamera().GetZoom()` runs from 0 to 1 in proportion to the camera
  distance, as the scaling assumes. The log shows the values.
- **Empty entities.** Whether an empty entity costs the executable much. If it does, paging
  saves less than the counts above suggest.
