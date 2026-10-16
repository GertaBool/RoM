# How the game runs: rendering, interface, time and memory

What the game executable does, what the DLL and the mod's Python ask of it, and where
turn time and memory go. Measured in the headless harness with the real DLL (patch
0016) and checked against the source. The executable itself was not run: it is the
2005 Gamebryo engine on DirectX 9, 32-bit, and its code is encrypted by copy protection.

Detailed maps (each claim marked as verified in code, measured, or inferred about
the executable):

- [render-ui-map.md](render-ui-map.md): what the DLL asks the renderer and interface to
  do, the interface's dirty bits and the Python that redraws the HUD, and the art load
  from XML.
- [ai-hotloops-map.md](ai-hotloops-map.md): where the AI's turn time goes, bounded and
  pruned path searches, other hot spots, and 14 behaviour faults.
- [memory-map.md](memory-map.md): memory per object, sparse arrays, the save stream and
  proposals.
- `profile-t400-incl.txt` and `profile-t400-self.txt`: the turn-400 profile behind
  them.

## Who does what

| Part | Work |
|---|---|
| Executable | Rendering, animation, sound, the UI toolkit, the path finder's A* loop, file and network handling, hosting Python |
| DLL (C++) | Rules and AI; tells the executable which units, plots, cities and interface parts changed |
| Python | Draws the HUD and screens (the main interface alone is 6,500 lines), answers rule callbacks, handles events |

## Rendering and interface

The harness now counts every call the DLL makes into the executable's interfaces
(`HARNESS_PY_COUNTS=1`). Per late-game turn: 2,500 unit-entity notifications, 2,200
enemy-glow updates and 500 animated moves. Interface dirty bits are set up to 57 times
each (the espionage advisor's), 40 times for the plot list and 26 for the scoreboard.

These counts are a lower bound. The harness reports graphics as not initialised, so
the DLL skips yield symbols, flags and some move animations.

The largest costs we can reduce:

| What | Cost | Change |
|---|---|---|
| Scoreboard redraw (BUG Advanced Scoreboard) | 40-60k Python-to-DLL calls per redraw at 40 players; requested 2 times per player per turn, plus each score change | Redraw only for the active player, cache the "will declare war" checks per turn, one pass over met players instead of four nested 50x50 loops |
| Plot list | Every unit birth or death redraws the Python plot list whenever the human has nothing selected: `pPlot == getSelectionPlot()` holds for NULL == NULL (verified, CvUnit.cpp:10423 and four more sites) | `pPlot != NULL` at five sites; a 100-unit stack costs about 44k calls per redraw |
| Hover help over a stack of more than 15 units | Allocates 423 x 51 arrays of 244 ints, about 21 MB, and zeroes them on every hover (verified, `CvGameTextMgr::setPlotListHelp`) | Count only the unit types present; frees 21 MB of the executable's 4 GB |
| `CvGame::updateScore` | Calls Python `calculateScore` players x players times (verified) | Once per player; identical ranks |
| Yield symbols | Rebuilt on every plot when yields change, visible or not | Rebuild when revealed |
| City and unit models | Up to about 106 building models in a size-40 city; settlers draw 7 figures (stock BTS: 4) | `GAME_CITY_SIZE_EXP_MODIFIER` and unit group sizes in XML; visual only |

Patch 0017 makes the plot list, hover help and `updateScore` changes, along with
tech-first `canBuild` and the route-build scan in `getBestRoute`
([fixes](../../fixes/README.md#settler-without-cities-interface-redraws-and-turn-time)).

## Turn time

Profile of three turns from the turn-400 Marathon snapshot (342 cities, about 1,800
units), 20.5 s in all:

- **Path searches: 55 % inclusive** (29,654 searches). The DLL's callbacks `pathValid`,
  `pathCost` and `pathAdd` take 7.7 s of it. Most of the remaining 3.4 s is the
  harness's own A*, which scans its open list linearly. The game's A* lives in the
  executable and its speed is unknown, so the callback time is the reliable measure.
- **`CvCity::canTrain`:** 1.06 million calls.
- **`CvPlayer::canBuild`:** 3.8 million calls, mostly from `getBestRoute`. `canBuild`
  tests the plot before the far cheaper tech check (verified).

Prototypes measured on the same three turns:

| Change | Saving | Same game? |
|---|---|---|
| `AI_guardCity` searches only as far as the caller's turn limit | `AI_guardCity` 3.87 s to 1.27 s; turns 20.5 s to 18.4 s | No: a turn bound can find a different path. A cost bound gives the same decisions ([section 2.4](ai-hotloops-map.md#24-an-exact-bound-prune-by-cost-on-the-parent-side)) |
| `getBestRoute` scans only the 9 route builds, best first | 0.27 s | Yes, identical telemetry |

The map's ranked list estimates that applying every change with identical decisions
takes the three turns from 20.5 s to about 13 to 15 s. The largest items:
- cost-bounded searches in `AI_guardCity`;
- tech-first `canBuild`;
- branch and bound in `AI_pickTargetCity` and `AI_nextCityToImprove`;
- an upgrade-tree memo for `canTrain`.

## Memory

- **The DLL's game state is small.** About 13 MB in the measured late game
  (114 cities, 1,521 units) and about 20 MB estimated for 342 cities.
- **"Memory allocation failure" crashes come from the executable's 4 GB of art and
  textures**, plus fixed blocks like the 21 MB hover array above.
- **Sparse arrays dominate:**
  - Cities: 78 % of each city's 23 KB is 11 arrays sized by building, unit or
    promotion count, 0-3 % of them non-zero.
  - Player slots: all 51 slots allocate every array, although 39 are unused in a
    12-player game.
  - Units: each stores its promotions as 244 booleans with about 3 set.
- **Save:** 10.3 MB uncompressed, 0.53 MB after compression; almost all zeros.
- **Open item:** a continuous run grows about 80 KB per turn more than its live state.
  The cause is not yet traced, in the DLL or the harness.

The map's proposals (sparse city records, bitsets, lazy player slots, history as
vectors) halve the state. That matters less than the art budget for the 4 GB limit.
