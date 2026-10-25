# Graphics paging, fixed: the freeze at the first city

**Status: built and tested headless, not yet in the game.** This DLL is GitLab `main` `a459d0d8`
(graphics paging with G2, G3, G4, merged as !57) plus one change, `fixes/graphics-paging-fix.patch`
(build `d88a69fdae2c`, GitLab branch `claude/graphics-paging-fix`).

## What went wrong

The game froze when you founded London, your first city. `PythonDbg.log` ends after
`City Built Event: London` and the score update, and `LSystem.log` had just laid out the city.

Paging destroys several kinds of graphics far from the camera. Vanilla Beyond the Sword destroys and
remakes all of them during normal play except one: the plot builder, which draws a plot's bonus and
improvement art. Vanilla destroys plot builders only when the game ends (`CvPlot::uninit`). Plot
builders use the same layout system as cities (`CIV4PlotLSystem.xml` and `CIV4CityLSystem.xml` in
`LSystem.log`). Paging had destroyed far-away plot builders at the start, and London was the first
city to be laid out.

That is the reading, not a proof: the harness has no executable, so it cannot run the layout
system. Your game decides.

A second, smaller fault: `CvGameInterface.getCameraZoom` took no argument, and the game passes one.
It failed once (`PythonErr.log`), and the window then stayed at its widest size.

## What this build changes

- Plot builders are no longer paged out (`GRAPHICS_PAGING_PLOT_BUILDERS` 0). Bonus and improvement
  art far from the camera stays.
- Each part of paging has its own switch, so a fault can be narrowed down without a new DLL.
- `getCameraZoom` takes the argument, so the window follows the zoom again.

## Install

Back up the three files first, then copy:

| File here | Goes to (in `Mods/Rise of Mankind/`) |
|---|---|
| `CvGameCoreDLL.dll` | `Assets/CvGameCoreDLL.dll` |
| `GlobalDefinesAlt.xml` | `Assets/XML/GlobalDefinesAlt.xml` |
| `CvGameInterface.py` | `Assets/Python/EntryPoints/CvGameInterface.py` |

## What to check

1. Start a new game and found your first city. Play on a few turns.
2. If it still freezes, set these to 0 one at a time in `GlobalDefinesAlt.xml`, restart, and
   found a city again. Tell me which one stops the freeze:
   - `GRAPHICS_PAGING_SYMBOLS`: yield symbols and unit flags far away;
   - `GRAPHICS_PAGING_PLOTS`: feature and route art far away;
   - `GRAPHICS_PAGING_CITIES`: other players' cities far away;
   - `GRAPHICS_PAGING_UNITS`: other players' units far away.

   `GRAPHICS_PAGING` 0 turns all of paging off.
3. If something looks wrong, set `GRAPHICS_PAGING_LOG` to 1 (with `LoggingEnabled = 1` in
   `CivilizationIV.ini`) and send `Logs/GraphicsPaging.log` with `PythonErr.log`.

Saves move freely between this DLL and the earlier ones: nothing new is saved.
