# Graphics memory and time in a large Rise of Mankind game

The user's Mediterranean game crashed at 490 AD with the executable's memory allocation failure.
This analysis asks what grows with such a game on the graphics side, and what can shrink it
without lowering the picture. Every figure below comes from a file in [data/](data/), made by a
script in [tools/](tools/); the save and the logs themselves are not published.

## 1. Questions and sources

| Question | Source |
|---|---|
| What ended the session? | `app.log` (the executable's log) |
| How large is the game? | The autosave of 460 AD, loaded in the headless harness with the DLL built from GitLab `2a8b9a83` (`harness.exe save`, `HARNESS_HISTORY_DIAG=1`) |
| How much memory does the DLL itself use while the game is played? | The same harness, 30 turns from the save, process memory sampled every 5 s |
| Which textures does the mod ship, in which formats? | The mod's three FPK packs and its loose files, read by [tools/textures.py](tools/textures.py) |
| Which of them does this game use? | The save's unit and building types, followed through the mod's art definitions to the NIF models and the textures named in them ([tools/active.py](tools/active.py)) |
| How many models stand on the map? | The save's units and each unit's `iGroupSize` ([tools/instances.py](tools/instances.py)) |
| How much of that would a view window hold? | The same, counted inside the busiest window of a given size ([tools/window.py](tools/window.py)) |
| How often are city billboards rebuilt? | RoM's debug log `CvGameTextMgr_buildCityBillboardString.log` ([tools/billboards.py](tools/billboards.py)) |

Not available here, and marked *open* where it matters: the executable's own memory use by
category (no profiler on the user's machine), the base game's art (213 models the game uses come
from it), and the features and improvements on the map's plots (the harness does not dump them).

## 2. Setup

- Map 107 x 87 plots, Marathon, Noble; turn 356 (460 AD) in the autosave
  ([data/instances-ad460.txt](data/instances-ad460.txt), [data/windows-ad460.txt](data/windows-ad460.txt)).
- 21 civilizations alive; the human is Henry VIII of England.
- 300 cities and 2,359 units at turn 356; 55 unit types, 84 building types, 1,959 buildings
  ([data/active-ad460.json](data/active-ad460.json)).
- Executable: `Civ4BeyondSword.exe` of 2009-05-14, large-address-aware, so 4 GB of address space on 64-bit Windows.

## 3. Description

### The session (logs, 460 to 490 AD)

- The game was loaded at 16:08:38; the executable logged `ERR: Memory allocation failure - exiting
  program.` at 8602 s of its clock, about 17:27, with an unreadable reason string (repeating bytes
  `fe 0b b0 b5`, the pattern of the dialog on screen).
- City billboards: 206,087 rebuilds in 4,711 s, of 309 cities. 200,577 of them fall in 396 seconds
  with 100 or more rebuilds; at most 798 in one second. 100,885 rebuilds repeat the same city within
  0.2 s of its previous one ([data/billboards-session.json](data/billboards-session.json)).
- The billboard debug logging wrote 373,505 lines in the session.
- The scoreboard (BUG, Python) took a mean of 220 ms per update, 743 updates, 163 s in all (`PythonDbg.log`).

### The DLL without graphics (harness, turns 356 to 386)

- Resident memory 97.1 MB after loading, 110.9 MB at turn 386, at most 111.5 MB.
- Mean turn 20.8 s, longest 30.5 s ([data/harness-ad460-30turns.json](data/harness-ad460-30turns.json)).

### Textures the mod ships

- 7,404 textures once loose files replace packed members of the same path, 440 MB if all were loaded
  ([data/textures-summary.txt](data/textures-summary.txt)).
- By format: DXT3 217.1 MB, DXT1 66.1 MB, uncompressed 32-bit DDS 50.5 MB, DXT5 48.3 MB, 32-bit TGA 46.2 MB.
- 746 uncompressed textures, 108.7 MB. 889 groups of identical files under different paths, 64.0 MB of extra copies.
- The two GameFont sheets are 32-bit TGA, 5.6 MB and 4.8 MB.

### Textures this game uses (turn 356)

- 472 models for the 55 unit types (every era and art-style variant) and 84 building types; 213 of
  them are base-game models, not in the mod.
- The mod textures those models name: 981 files, 25.0 MB; 53 uncompressed, 4.4 MB; 4.9 MB of
  identical copies ([data/active-ad460.json](data/active-ad460.json)).

### Models on the map (turn 356)

- 6,386 unit models from 2,359 units; for example 1,005 Axemen (335 units x 3), 675 Light
  Swordsmen (225 x 3), 651 War Dogs (93 x 7), 644 Workers (322 x 2) ([data/instances-ad460.txt](data/instances-ad460.txt)).

| View window (plots) | Share of the map's plots | Unit models inside, busiest placement | Cities inside, busiest placement |
|---|---|---|---|
| 24 x 16 | 4 % | 1,093 of 6,386 (17 %) | 27 of 300 (9 %) |
| 32 x 22 | 8 % | 1,547 (24 %) | 41 (14 %) |
| 48 x 32 | 17 % | 2,336 (37 %) | 84 (28 %) |

([data/windows-ad460.txt](data/windows-ad460.txt))

## 4. Readings

**R-A. The DLL's own data is not what fills the 4 GB.** At turn 356 to 386 the DLL with the
harness holds about 111 MB, and grows 13.8 MB in 30 turns. Facts: section 3, harness. Contradicted
if the real game's DLL heap were much larger than the harness's, which would show as the
executable's private bytes falling sharply when the same save is loaded with graphics off.

**R-B. Texture formats are not the lever in this game.** The mod textures the game's units and
buildings use are at most 25.0 MB, and their uncompressed part 4.4 MB; converting every one of them
to DXT would save a few MB of 4,096. The 108.7 MB of uncompressed textures in the whole mod are mostly
custom leaderheads and interface screens, loaded only when shown. Facts: section 3, textures.
Contradicted if the executable keeps textures of every leaderhead met in memory; that would
show as memory rising with each diplomacy screen opened.

**R-C. What grows with this game is the number of things drawn: models on the map, city layouts
and plot graphics.** Every unit and city gets its entity when it is constructed, whether on screen or
not (`createUnitEntity` in the `CvUnit` constructor, `CvUnit.cpp:61`; `createCityEntity` in the `CvCity`
constructor, `CvCity.cpp:102`), and `CvMap::setupGraphical` sets up the feature, route, river and flag
graphics of every plot of the map (`CvMap.cpp:270-273`, `CvPlot.cpp:266`). Here that is 6,386 unit
models, 300 city layouts and 9,309 plots. Facts: sections 2 and 3, and the code cited. *Open:* the bytes per model and per plot are
the executable's and are not measured; the share of the 4 GB they take is inferred from the fact
that nothing else in the game scales with its size.

**R-D. A view window holds a small part of it.** Even a 48 x 32 window placed where the most units
stand holds 37 % of the unit models, 28 % of the cities and 17 % of the plots. Facts: section 3,
models. Contradicted if the human's camera ranged over most of the map within a few seconds.

**R-E. Billboards are rebuilt in bursts, mostly repeats.** 97 % of the rebuilds fall in 396 burst
seconds, and half of all rebuilds are a city rebuilt again within 0.2 s. The DLL only sets a flag
(`CvCity::setInfoDirty`); the executable rebuilds a city's billboard whenever it finds the flag
set, so a city set dirty again between frames is rebuilt again. 29 setters in `CvCity.cpp` set it.
*Open:* which of them fire repeatedly in the bursts.

## 5. Changes, by expected effect

None of these is built yet. Each changes the DLL, so each needs the user's approval of its design
and a prediction in `method/mission/register.json` before it is built (CLAUDE.md rules 9 and 10).

### G1. Graphics paging around the camera (space; large)

Keep graphics only for the plots near where the camera looks; destroy them elsewhere and recreate
them when the camera comes back. What is on screen does not change.

- **Where the camera is:** `gDLL->getInterfaceIFace()->getLookAtPlot()`, read in `CvGame::update`
  when it has moved three or more plots since the last check.
- **Window:** plots within a range of the look-at plot (define `GRAPHICS_PAGING_RANGE`, 0 = off,
  the current behaviour), with a margin of a few plots before paging out again so a camera moving
  back and forth does not rebuild.
- **Page out a plot:** destroy its feature, route, river, improvement and flag symbols (the calls
  `CvPlot::uninit` already makes, `CvPlot.cpp:125-133`); remove and destroy each unit's entity (as
  `CvUnit::uninit`, `CvUnit.cpp:72-75`) and the city's (as `CvCity::uninit`, `CvCity.cpp:116-117`).
- **Page in:** `CvPlot::setupGraphical` with the route symbol; each unit's entity as
  `CvUnit::reloadEntity` makes it (`CvUnit.cpp:82-94`, already used on upgrades); the city's entity and
  layout (`createCityEntity`, `setupGraphical`, `setLayoutDirty`).
- **Guards:** the DLL addresses a unit's or city's entity in 67 places (29 `AddMission`, 8
  `RemoveUnitFromBattle`, 4 `updatePosition` and others). Each skips the visual when the entity is
  paged out; a unit that moves into the window gets its entity first. Selected units and units in
  combat are never paged out.
- **Not saved:** graphics only, so saves and multiplayer sync are unchanged.
- **Expected:** the map-scaled part of graphics memory falls to what the window holds; for this game
  at most 37 % of the unit models, 28 % of the cities and 17 % of the plots at a 48 x 32 window.
- **Risks:** an engine call on a unit without an entity crashes (guards above, and the switch);
  recreating a city's layout costs time when the camera arrives (the margin limits how often).
- **Verification:** headless, the game must play identically with paging on and off (same
  telemetry), and every paged-out entity call must be skipped; in the game, the user's process
  memory at the 460 AD save with paging on and off, and play past 490 AD.

### G2. Billboard rebuilds only when shown values change (time)

- **Measure first:** a harness build that counts, per city and frame, each change of the info flag
  from clear to set, and which setter set it, over a few turns of the 460 AD save.
- **Change:** in the setters that fire repeatedly, set the flag only when a value the billboard shows
  changes (name, population, food and production bars, production icon, religion and corporation
  icons, defence).
- **Expected:** fewer of the 206,087 rebuilds per session; the size is unknown until measured.

### G3. Remove RoM's leftover billboard debug logging (time)

- `CvGameTextMgr::buildCityBillboardIconString` (`CvGameTextMgr.cpp:17570-17606`) writes two or three
  log lines per rebuild: 373,505 lines in this session. It writes only with logging on, and the war
  log needs logging on. Removing the three `logMsg` calls changes nothing on screen.

### Not pursued

- **Texture recompression and deduplication:** at most a few MB in this game (R-B).
- **Smaller formations or single-unit graphics:** they lower the picture.

## 6. Open

- The executable's memory by category at the crash; the user can read it with a memory tool at the
  460 AD save.
- Plot features and improvements on the map (a harness dump of them would count trees and buildings per plot).
- What makes the scoreboard take 220 ms per update.
- The 213 base-game models' sizes.
