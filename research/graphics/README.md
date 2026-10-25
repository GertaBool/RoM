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
| What does the DLL ask the renderer and interface to do each turn, with graphics set up? | The harness with `HARNESS_GRAPHICS=1` and `HARNESS_PY_COUNTS=1`, 3 turns from the 460 AD autosave, paging off and on, and without graphics; a 0-turn run gives the calls made while setting up ([tools/harness_counts.py](tools/harness_counts.py) `engine`) |
| Which code sets a city's billboard or layout dirty, and how often would the executable rebuild them? | No source: a diagnostic harness build ([tools/harness-callers.patch](tools/harness-callers.patch), then [tools/harness-billboard.patch](tools/harness-billboard.patch)). It records the caller of every clean-to-dirty change. After each update it plays the executable: it builds every dirty city's billboard with the DLL's text functions, times them, and clears the flag. Callers are named from the DLL's map file ([tools/addr2sym.py](tools/addr2sym.py)) |
| What do the DLL calls of one BUG scoreboard redraw cost? | The same build: the DLL calls `CvMainInterface.updateScoreStrings` makes for the active player (with `PlayerUtil`, `AttitudeUtil`, `DiplomacyUtil`), timed in parts, 5 repetitions at turn 359 |

The diagnostic builds are not shipped and change no game logic; the harness without graphics and
with them plays the same game. Not available here, and marked *open* where it matters: the executable's own memory use by
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

### Engine calls, with graphics set up (harness, turns 356 to 359)

From [data/engine-calls-ad460.tsv](data/engine-calls-ad460.tsv); the calls made while setting up are
counted apart.
- **Setup:** 7,868 plot yield symbols, 2,302 river symbols, 1,248 plot builders (bonuses and
  improvements), 1,083 route symbols and 2 feature symbols. The trees of this map are tile art,
  not feature symbols.
- **Three turns, paging off:**
  - `isCitySelected` asked 244,427 times;
  - `GameData_DIRTY_BIT` set 67,143 times;
  - `getSelectionPlot` asked 44,613 times;
  - `setMinimapColor` 19,392 times;
  - 1,678 yield symbols created and 1,616 destroyed;
  - fog changes 2,920 lightened and 2,532 darkened plots;
  - `Score_DIRTY_BIT` set 239 times.
- **Paging:** paging on changes none of these counts, apart from the plot builders and routes
  it pages.
- **Callers** ([tools/harness-callers.patch](tools/harness-callers.patch), 2 turns):
  - 48,302 of the `GameData_DIRTY_BIT` sets come from `CvCity::updateCommerce`, through
    `CvPlayer::changeCommerceRate`, only for the active player's cities;
  - 141,943 of the `isCitySelected` calls come from `CvCity::updateCommerce`, for every player's
    cities.

### Billboards and layouts (harness, turns 356 to 359)

From [data/billboard-ad460.json](data/billboard-ad460.json):
- **Rebuilds:** 2,440 billboard rebuilds in 241 updates. 77 updates rebuilt at least one; the
  most in one update was 300, every city at the first update after setting up.
- **Text cost:** building the billboard text of all 2,440 took the DLL 0.043 s.
- **Setters**, clean-to-dirty changes:
  - `CvCity::changeDefenseDamage` 713;
  - `CvCity::processBonus` 693;
  - `CvPlot::changeVisibilityCount` 629;
  - `CvCity::setBaseYieldRate` 49;
  - `CvCity::changeBonusYieldRateModifier` 48.
- **Visibility setter:** `changeVisibilityCount` set a city dirty 2,356 times. 2,095 of these were
  for teams other than the active one, and 552 of those found the billboard clean.
- **Layouts:** 513 rebuilds; setters `CvCity::setupGraphical` 308, `CvCity::processBuilding` 121,
  `CvCity::setPopulation` 84.
- **Scoreboard:** one redraw with 20 rows asks 330 war-trade denials. Its DLL calls take 13.4 ms
  for the "too many wars" check (`PlayerUtil.isWHEOOH`) and 0.1 ms for the rest.

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

**R-F. The DLL's own side of drawing costs little; the executable's does.** With graphics set up
the harness plays turns as fast as without them (the P8 runs). The text of 2,440 billboards costs
the DLL 0.043 s. What the DLL decides is how much the executable must build and keep: entities,
symbols, flags, plot builders, billboards and layouts. Facts: section 3, engine calls and
billboards. Contradicted if a DLL profile of the real game showed graphics calls among its top costs.

**R-G. A quarter of the billboard rebuilds are for nothing the player sees.** The billboard shows
the city as the active team sees it. Yet `changeVisibilityCount` marks it dirty when any team
starts or stops seeing the city. Those other teams account for 552 of the 2,132 rebuilds after
setup (26 %). Facts: section 3, billboards; `CvPlot.cpp`, `changeVisibilityCount`. *Open:* the
session log's rebuild rate (44 a second on average, 798 at most) is many times the harness's
(about 710 a turn). So the executable rebuilds for reasons of its own as well (for example, cities
coming on screen), and those are not counted here.

**R-H. The scoreboard's time is mostly Python, and its DLL part is mostly the WHEOOH check.** The
session measured 220 ms per redraw. Its DLL calls take about 14 ms, 13.4 of them for asking each
AI, about each other team, whether it would declare war on request. The other 200 ms or so are
Python: the loops over players and cities, and each call into the DLL they make, with Python's
call cost. *Open:* the split inside Python, which needs a Python profile in the game.

**R-I. Yield symbols and unit flags scale with the map and are not paged yet.**
- **Yield symbols:** 7,868 exist from the start, one stack per plot with a yield. They stay
  hidden unless yields or the city screen are shown.
- **Flags:** the executable builds one per plot where the active team sees a unit
  (`CvMap::updateFlagSymbols`, called by the executable).

Facts: section 3, engine calls; `CvPlot::updateSymbols`, `CvPlot::updateFlagSymbol`. *Open:* their
bytes in the executable.

## 5. Changes, by expected effect

Each changes the DLL or the mod's Python, so each needs the user's approval of its design and a
prediction in `method/mission/register.json` before it is built (CLAUDE.md rules 9 and 10). G1 is
built (`fixes/graphics-paging/README.md`, `builds/graphics-paging/`); G2 to G5 are not. They are
ordered by expected effect on the crash first (memory), then on time.

### G1. Graphics paging around the camera (space; large)

**Built** as `fixes/graphics-paging.patch`, with predictions P7 and P8. Both are corroborated in
the harness, and the game state is identical with paging on and off. The design below is the one
approved. Two things differ in the build: battles that will be shown page their units in, and the
window scales with the camera zoom. The memory saved in the executable is open until the user
measures it. *Correction:* the trees of this map are tile art, not feature symbols (2 feature
symbols at setup, section 3), so paging leaves trees as they are. On plots it acts on routes and
plot builders.

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

### G4. Page plot yield symbols and unit flags too (space; extends G1)

- **Change:** on page-out, `CvPlot::pageGraphics` also deletes the plot's yield symbols
  (`deleteAllSymbols`) and its two unit flags (`m_pFlagSymbol`, `m_pFlagSymbolOffset`, as
  `CvPlot::uninit` does).
  - While the plot is paged out, `updateSymbols` and `updateFlagSymbol` make nothing.
  - On page-in it calls `updateSymbols` and `setFlagDirty(true)`, so the executable's
    `CvMap::updateFlagSymbols` builds the flags again.
  - Under the same switch as G1.
- **Expected:** of the 7,868 yield symbols and the one flag per plot with a seen unit, only those
  in the window remain (R-I). The bytes are *open*.
- **Risks:**
  - a symbol or flag missing on screen if the window is too small (the same check as G1);
  - the yield display (`isShowYields`) shows only the window, which is all the screen shows.
- **Verification:** as G1: the same game with paging on and off. Visual calls on deleted symbols
  are counted as zero in the harness. In the game: the yield display and the unit flags at the
  window's edge.

### G2. Billboards dirty only for what the active team sees (time; measured)

- **Change:** in `CvPlot::changeVisibilityCount`, set the plot's city dirty only when `eTeam` is
  the active team. In `CvGame::setActivePlayer`, set every city dirty once, so a hotseat switch
  still shows the new team's view.
- **Expected:** up to 552 of the 2,132 rebuilds after setup in the harness (26 %, R-G). Each
  rebuild skipped spares the executable's billboard work, which is not measured here. The
  executable's own rebuilds (R-G, *open*) are not touched.
- **Risks:** a billboard that should show another team's change. The billboard shows nothing of
  another team's view, so none is known.
- **Verification:** the harness counts above, before and after; the same game state; in the game,
  billboards after a city comes into and out of sight.
- **Considered, not proposed yet:** an `isInfoDirty` that compares the billboard's content with
  the last one built before reporting dirty. It would cover every setter, but the executable also
  reads values the DLL does not hand over in strings (the bars' fill), so a stale bar is a risk
  that cannot be checked here.

### G3. Remove RoM's leftover billboard debug logging (time)

- `CvGameTextMgr::buildCityBillboardIconString` (`CvGameTextMgr.cpp:17570-17606`) formats two or
  three debug lines per rebuild even with logging off. With logging on, which the war log needs,
  it writes them: 373,505 lines in this session. Removing the three `Format` and `logMsg` pairs
  changes nothing on screen.

### G5. The scoreboard's "too many wars" check once a turn (time; Python)

- **Change:** in the mod's `PlayerUtil.isWHEOOH`, keep each answer until the turn or a war or
  peace changes it, instead of asking the AI again on every redraw.
- **Expected:** most of the 13.4 ms of DLL calls per redraw (R-H), and the Python loop around them.
  The rest of the 220 ms is *open* until a Python profile in the game shows it.
- **No-code check the user can make now:** turn off the scoreboard's WHEOOH icon in the BUG
  options (Advanced Scoreboard, `WHEOOH`). Then compare the scoreboard's time per update in
  `PythonDbg.log` with the session's 220 ms. The difference is what G5 can save at most.
- **Risks:** a stale icon within a turn; the AI's answer depends on war plans that change between
  turns, so the cache is cleared each turn and on every war or peace.

### Not pursued

- **Texture recompression and deduplication:** at most a few MB in this game (R-B).
- **Smaller formations or single-unit graphics:** they lower the picture.
- **`GameData_DIRTY_BIT` set 67,143 times in three turns:** the flag is read once per frame, so the
  repeated sets cost nothing beyond the first.
- **The 244,427 `isCitySelected` calls:** each is a cheap query in the executable. Guarding them by
  the city's owner, as most other callers already do, would save little.
- **The setup of every plot's graphics at load** (`CvMap::setupGraphical`): before the first update
  the camera's place is unknown, so a paging-aware setup has no window to use; the first pass trims
  it within half a second.

## 6. Open

- The executable's memory by category at the crash; the user can read it with a memory tool at the
  460 AD save.
- Improvements and bonuses on the map: 1,248 plot builders at setup (section 3), not counted by type.
- What makes the scoreboard take 220 ms per update beyond its 14 ms of DLL calls (a Python profile in the game).
- Why the session rebuilt billboards in bursts of up to 798 a second while the DLL's setters ask for about 710 a turn in the harness (R-G).
- The bytes the executable spends per unit model, city layout, plot builder, yield symbol and flag.
- The 213 base-game models' sizes.
