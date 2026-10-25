# Graphics paging: the crash on moving a unit, fixed

**Status: built and tested headless, not yet in the game.** This DLL is GitLab `main` `d929b57`
plus `fixes/graphics-paging-coherence.patch` (build `dd2152452c46`, GitLab branch
`claude/paging-coherence`).

## What went wrong

Paging handled a plot and the units on it separately. A plot outside the window around the camera
lost its flag, yield symbols and road graphic, even when a unit or city on it kept its own
graphics. Your own units and cities always keep theirs.

The unchanged game never shows a unit without its flag, or a road you can see without its graphic.
The executable reads both itself (`updateFlagSymbol`, `getFlagSymbol`, `getRouteSymbol`,
`isRoute`). Moving such a unit made it use a flag that was not there.

The headless harness now does what the executable does near the camera: it updates the flags and
counts these states. Each run below is 100 turns from turn 0 of your Huge Mediterranean map.

| Build | Camera | Live units without a flag | Roads without a graphic | Units on screen without a flag |
|---|---|---|---|---|
| Before paging (`c42be8b`) | following your units | 0 | 0 | 0 |
| Before paging (`c42be8b`) | sweeping the map | 0 | 0 | 0 |
| `main` `d929b57` | following your units | 27 | 58 | 4 |
| `main` `d929b57` | sweeping the map | 62 | 75 | 0 |
| This build | following your units | 0 | 0 | 0 |
| This build | sweeping the map | 0 | 0 | 0 |

The game plays the same, turn by turn, in all three builds.

## What this build changes

- **A plot keeps its graphics** while any unit or city on it keeps its own, or a move you make
  ends there.
- **Page-in follows units and cities.** A unit or city that gets its graphics back, or moves,
  brings its plot's graphics first.
- **Flags are rebuilt on demand.** When the executable asks for a flag on a plot that needs one,
  the plot's graphics come back on the spot.
- **Roads are never removed.**
- **The zoom no longer shrinks the window** (`GRAPHICS_PAGING_ZOOM` 0). How the camera's zoom
  value relates to what the screen shows is not known, and the widest-zoom window holds the
  screen at any zoom.

## Install

Copy into `Mods/Rise of Mankind/`:

| File here | Goes to |
|---|---|
| `CvGameCoreDLL.dll` | `Assets/CvGameCoreDLL.dll` |
| `GlobalDefinesAlt.xml` | `Assets/XML/GlobalDefinesAlt.xml` |
| `CvGameInterface.py` | `Assets/Python/EntryPoints/CvGameInterface.py` |

Saves move freely between this DLL and the earlier ones.
