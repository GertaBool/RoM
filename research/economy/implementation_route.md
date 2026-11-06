# Open questions and the implementation route (R27, M73)

D31 (water and hydration) is decided (M73). This file lists what is still open (part 1) and the route to build the
food, drink, water and population work in XML, C++ and Python with the tools this project has (part 2). The
function lists come from the code map (`codemap/tool/query.py`). Its source is GitLab main `e694caf`, which
predates the economy branch; part 2 starts by rebuilding it.

## 1. Still open

### 1a. Decisions waiting on you

| Decision | State | Where the proposal is |
|---|---|---|
| D30 population model | open; the compact Malthusian model with the tile formula and sourced `r`, `s`, `s_min` is proposed | `open_questions.md` section 7, `population_formula.md` |
| D24 what a map declares | open; the block schema with three layers is proposed | `open_questions.md` section 9 |
| D21 entertainment media | open; services over the trade network are proposed | `open_questions.md` section 10 |
| D27 keeping | decided; the spoilage table per form and Salt as preserver are proposed for its open item | `open_questions.md` section 5 |
| D28 Flour and fine cloth | decided; "no Flour, fine cloth a Drapers luxury" is proposed for its open item | `open_questions.md` section 6 |
| D29 guilds, five items | decided; proposals for once-per-game by secret technique, the luxuries, three grades, the political role and 5-person workshops | `open_questions.md` section 8 |

### 1b. Values that are still estimates (to replace with sources, or to accept as estimates)

- **People:** the working share (40 %); food per head after the transition (3,300 and 3,800); `r` after the
  transition (0.5 %); migration `m` (2 %).
- **Land:** usable land per plot type; ha per worker for crops other than wheat; the rotation's nitrogen effect.
- **Animals:** milk per cow, live weights and head per hectare before Biology; the medieval figures were not found.
  A lead: the 13th-century *Hosebondrie*.
- **Sea and plantations:** fish per fisher (a lead: the 1861 Gloucester schooner landings and crews); labour per
  hectare for sugar and bananas.
- **Keeping:** the spoilage rates of cheese, cured and dried forms; salt per tonne of fish or meat.
- **Water:** the supply per source (Groundwater Well 500, Aqueduct 50,000 m³ a day), the wells limit (5,000
  people), the health per shortfall and per quality, and the Bath House's water use.
- **Drinks and satiety:** the hydration index of juices; milk drunk by pastoral peoples per day; potatoes' bulk
  satiety, which the formula does not capture.

### 1c. Checks that wait on you in the game

- The LQ.F9.T5 and T6 icons.
- PR.F6: a map script's and a scenario's scale read back with `CyMap().getPlotAreaKm2()`, and a WorldBuilder save
  that keeps the BeginEconomy block.
- A test game with `builds/settlement-economy`.
- The UI mock-up (R9.1).
- The Glass button texture.
- LQ.F10.T2 is blocked (Wikimedia Commons answered HTTP 429).

### 1d. One technical question the code map raises

- `CvPlayer::getRealPopulation()` and `CyCity` and `CyPlayer` return `long`, which is 32 bits in this compiler.
- On an Earth map with a real population model, a player's or the world's people exceed 2³¹ (about 2.1 billion).
- **Proposal:** keep people in `__int64` inside the DLL (rule F). Give Python a value in thousands, or a second
  accessor, and keep the old `long` accessors for the existing screens.

## 2. The route

### Tools used at each step

| Tool | Use |
|---|---|
| `codemap/tool/query.py` (find, callers, callees, path, rank) and `codemap/files/*.md` | locate every function a change touches and every caller of it, before writing |
| `codemap/tool/build.sh` | rebuild the map from the branch (Visual C++ Toolkit 2003 under Wine) |
| `toolchain/setup_toolchain.sh` and the MSVC toolchain | build the DLL into `builds/settlement-economy` with provenance and patch |
| `research/economy/plan/tools/connector/*_edits.py` | generate GitLab commits for the connector (`mcp__gitlab__add_commit`); batches under 15 MiB; unique anchors |
| `research/economy/plan/tools/xml_fields.py` | dump the records before and after each XML change |
| `toolchain/harness` (`batch.sh`, `run.sh`, HarnessScenario) | seeded runs: 5 per arm for safety, 30 for play claims |
| `method/ledger.py`, `method/mission/register.json` | register each prediction before its evidence; `Serves:` trailers |
| `method/check_all.py`, `check_plan.py` | before every commit; tasks with `done_when` (rule A) |

### Step 0. Groundwork (Python tools, no game change)

1. **Rebuild the code map** from `claude/settlement-economy` (d2a8f756). It then covers `CvPlayer::doGoods`, the goods
   accounts (GW.F3) and `CvMap::m_iPlotAreaKm2`. Every later step queries it.
2. **Write the source table `research/economy/data/nutrition.json`:** per good, the FAO kcal, protein and fat; DIAAS;
   the as-eaten factor; the hydration index; the spoilage per form. Each value carries its source.
3. **Write the generator `tools/connector/food_values_edits.py`.** It computes `iSatietyPerTonne`,
   `iProteinPerTonne` and `iHydrationPercent` from the table (`open_questions.md` sections 4 and 4b) and writes the
   connector edits for the XML. This follows the PR.F6.T3 generator pattern.
4. **Write a deterministic check `tools/check_england1300.py`** (rule 9: computed, not simulated). It runs the tile
   formula and population model in Python with the decided values and asserts the England 1300 figures: about
   1,926 kcal a day from grain, 3 ha per farm worker, and `N` near `K`. The C++ is checked against it later.
5. **Plan the work.** Add the features FG.F4 (population model, once D30 is decided), CN.F4 (water and drinks,
   D31) and PR.F7 (usable land and the tile formula), each task with its `done_when`. Register predictions
   P58 and onward.

### Step 1. Schema and catalogue (XML and C++ readers; no behaviour change)

- **XML schema:** add the new fields to `CIV4BuildingsSchema.xml`, the terrain schema (bonuses and improvements)
  and `GlobalDefines.xml`. Values go into `CIV4BonusInfos.xml`, `CIV4BuildingInfos.xml` and
  `CIV4ImprovementInfos.xml`, through the generator.

| Record | New fields |
|---|---|
| BonusInfo | `iSatietyPerTonne`, `iProteinPerTonne`, `iHydrationPercent`, spoilage per form |
| BuildingInfo | `iWaterSupply`, `iWaterUse`, `iWaterQualityChange` |
| ImprovementInfo | `iWaterSupply`, `bLivestockWater` |
| GlobalDefines | `WATER_DRINK_PER_HEAD_ML`, `WATER_LEVEL_BASIC`, `WATER_LEVEL_INTERMEDIATE`, `WATER_LEVEL_OPTIMAL` |

- **C++ readers (`CvInfos.cpp`/`.h`):**
  - `CvBonusInfo::read(CvXMLLoadUtility*)` (line 17100) and its cache pair `read`/`write(FDataStreamBase*)`
    (16988);
  - `CvBuildingInfo::read` (11038, 10486);
  - `CvImprovementInfo::read` (16237, 16060);
  - each class's `copyNonDefaults`, because the modules merge records;
  - getters;
  - Python exposure in `CyInfoInterface*.cpp`.
- **Evidence:** a safety prediction. Five seeds per arm must give identical games, because nothing reads the
  fields yet.

### Step 2. Production (PR.F1, PR.F7; C++)

- **The produce step of `CvPlayer::doGoods`** (GW.F5, on the branch) computes each worked plot's goods with the tile
  formula. It uses:
  - the plot area (`CvMap::getPlotAreaKm2`);
  - the usable land per plot type (a lookup from terrain and feature);
  - the yield and ha per worker per tech stage;
  - workers from the city's people.
- **The engine's yields** (`CvPlot::calculateYield`) stay as they are, so the AI and the screens keep their inputs.
- **Evidence:** a prediction on the goods quantities, checked against `check_england1300.py` on one deterministic
  run; plus safety.

### Step 3. Food by satiety, and drinks (FG, CN.F4; C++)

- **The consume step of `doGoods`:** each person eats satiety (`s` a day) and drinks 1.8 L × the hydration index.
  Drinks go first, then water.
- **The stores** count satiety. Spoilage by form is the store step (SD.F2).
- **Integers (rule F):** all sums in `__int64`.

### Step 4. The population model (FG.F4; C++ and Python), once D30 is decided

- **`CvCity`:** a new `__int64 m_llPeople`, saved behind a new uiFlag in `CvCity::read`/`write` (14108, 14373).
- **`CvCity::doGrowth`** (13449; called only from `CvCity::doTurn`):
  - replaced by the logistic year loop toward `K = F / s`, with the death term from health;
  - the city size follows from people through the inverse of the present curve, via `setPopulation`.
- **The translation layer:** `growthThreshold()` (5411) and `foodDifference()` (5381) keep their signatures and
  return values in food units derived from the people model.
  - **Their callers keep working unchanged** (code map):
    - `CvCityAI::AI_yieldValue`, `AI_juggleCitizens`, `AI_chooseProduction`, `AI_bestUnitAI`, `AI_chooseUnit`,
      `AI_buildingValueThreshold`;
    - `CvDLLWidgetData::parsePopulationHelp`;
    - `CvGameTextMgr::setCityBarHelp` and `buildCityBillboardCityNameString`;
    - the food bar (`getFoodBarPercentages`, `getFoodTurnsLeft`);
    - `CvPlayer::doAdvancedStartAction`.
  - **Python callers:**
    - `CvMainInterface.updateCityScreen` (growthThreshold 14 calls, foodDifference, getFoodTurnsLeft);
    - `Revolution.updateLocalRevIndices` (foodDifference);
    - `RevolutionWatchAdvisor` and `CvCustomizableDomesticAdvisor` (calculateGrowth, calculateFood);
    - `SettlementTrainingProfiler`.
- **`CvCity::getRealPopulation()`** (6090) returns the people. Its callers are `CvPlayer::getRealPopulation`,
  `CyCity::getRealPopulation` (used by `CvInfoScreen.drawTextChart`) and `CvDLLWidgetData::parseCityNameHelp`.
  Overflow is handled as in 1d.
- **Evidence:**
  - the deterministic check against `check_england1300.py`;
  - a play prediction (30 seeds) that AI cities still grow, against fixed opponents;
  - safety.

### Step 5. Water supply and health (CN.F4; C++ and Python)

- **`CvCity`:** `m_iWaterSupply` and `m_iWaterQuality`, and `updateWaterSupply()` beside `updateFreshWaterHealth()`
  (6810). It is called wherever buildings, improvements or the city's plots change.
  - The code map shows `updateFreshWaterHealth` called only from `CvCity::init` at the first level. Rebuild the map
    and list every path into the building and plot changes (`query.py callers CvCity::processBuilding 2`) before
    choosing the update points.
- **Health:** a water term in `CvCity::goodHealth()` (5251) and `badHealth()` (5304). Their callers include the
  AI (`AI_yieldValue`, `AI_updateLocalGovernor`, `AI_bestPlotBuild`, `AI_getTargetSize`, `AI_chooseProduction`,
  ...) and the help texts `CvGameTextMgr::setGoodHealthHelp` and `setBadHealthHelp`. So the AI and the help text
  see water with no AI change.
- **Python:** one line in `CvMainInterface.updateCityScreen` (supply, need, level, quality); the sector overview
  (D26).
- **Evidence:** a computed check of the access levels on one deterministic run; safety.

### Step 6. Spoilage by form, needs, guilds, map data, media

These follow in the plan's component order (SD, CN, IN, LD, TR, AI). Each is located with the code map before it is
written.

### The commit and evidence cycle for every step

1. Write the task's `done_when` and register the prediction (ledger) before any evidence exists.
2. Query the code map for every function touched and every caller.
3. Write the edit generator under `tools/connector/` and commit to GitLab through the connector, one concern per
   commit (rule D).
4. Build the DLL with the toolchain into `builds/settlement-economy`, with provenance and `source.patch`
   (`Serves:` trailer).
5. Run the harness (5 seeds per arm for safety; 30 for play claims); then the computed checks.
6. Record the result in the register, mark the task done with `check_plan.py`, and update the plan's current block.

### What I can and cannot do from here

- **Can:** the code map (query, and rebuild with the Wine toolchain as earlier builds did); GitLab commits through
  the connector; DLL builds; harness runs; all Python tools and checks.
- **Cannot:** see the game's screen. The UI lines, icons and WorldBuilder round-trips wait on your in-game checks
  (1c).
