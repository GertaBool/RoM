# Graphics paging: the zoom fix

**Status: built, harness evidence pending, not yet tested in the game.** This DLL is GitLab `main` `3bec049`
plus [`fixes/graphics-paging-zoom.patch`](../../fixes/graphics-paging-zoom.patch) (build `59db478feb3c`).

## What changes

- **No tile-art rebuild on page-in.** A plot that comes back near the camera gets its feature symbol, yield
  symbols and flags again, without the terrain's tile art being rebuilt. Paging never removes tile art.
- **At most 100 set-ups per update.** One update sets up at most `GRAPHICS_PAGING_MAX_IN` plots, units and
  cities again; a zoom that uncovers more is finished over the next updates.

## Install

In `Mods/Rise of Mankind/`:

| Step | File |
|---|---|
| Copy `CvGameCoreDLL.dll` to | `Assets/CvGameCoreDLL.dll` |
| Copy `GlobalDefinesAlt.xml` to | `Assets/XML/GlobalDefinesAlt.xml` |

This DLL does not hold the diplomacy change (`builds/diplomacy-values`); both apply to `main` and can be
merged one after the other. Saves move freely between this DLL and the earlier ones.

## What to look for in the game

- Zoom in and out fast, as before the crash. With `GRAPHICS_PAGING_LOG` 1, `Logs/GraphicsPaging.log` shows
  "pass, more next update" lines when a zoom uncovers more than 100 plots, units and cities.
- At the edges of a fresh zoom-out, units, flags and forests may appear a fraction of a second late.
- If it still crashes: `Logs/GraphicsPaging.log`, and Proton's log with `PROTON_LOG=1 %command%` in the
  game's launch options (`~/steam-8800.log`, the "Unhandled exception" lines name the module and address).
