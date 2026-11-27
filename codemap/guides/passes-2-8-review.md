# Review of the GitLab passes 2 to 8

What the four commits called "pass 2" to "pass 8" on GitLab `main` changed, what the code map and the
checks show about them, and what reading every changed hunk found. Written by hand at GitLab `main`
`ede81881b7de`, against the commit before pass 2, `c08a472`.

Sections 1 to 4 describe. Section 5 holds the readings. Section 6 lists what stays open.

## 1. The commits

| Commit | Date | Message | Size |
|---|---|---|---|
| `08893b2` | 2026-11-23 | Pass 2: post-merge AI strength, overflow and graphics paging fixes | 13 files, +640 / -248 |
| `df09f82` | 2026-11-23 | "Patched critical bugs": a new `Assets/CvGameCoreDLL.dll`, build scripts; no source line | 7 files, +1 / -1 |
| `bf17674` | 2026-11-23 | Passes 3 to 7: "5-pass RoM AI transformation" | 14 files, +1491 / -145 |
| `d5fa0d1` | 2026-11-24 | Pass 8: upgrade rate, work rate, inquisition conditions, RevCivicsUtils, Guilds XML, civic values | 8 files, +255 / -133 |

## 2. How they were checked

1. **Two code maps**, of `c08a472` and of `ede81881b7de`, built with `codemap/tool/build.sh` and compared
   function by function and call by call.
2. **The checks** of `codemap/tool/check_links.py` (defines, types, text keys, XML references, Python
   links) on both trees, and the define names the new code reads.
3. **Every changed hunk read**, about 4900 diff lines in 180 hunks. The callers, reach and loading rules
   came from the map and the source.
4. **Builds:** the current source and pass 2 were built with the real compiler, and the shipped DLL was
   compared with them.

Not done: harness runs. The harness compiles against the staging-defence and balance patches. They apply
to `c08a472`, but not to `ede81881b7de`, whose passes rewrote the same functions. So the passes are
judged by reading and by the map, not by play.

## 3. What the map and the checks show

| Measure | `c08a472` | `ede81881b7de` |
|---|---|---|
| Units compiled, errors, warnings | 105, 0, 0 | 105, 0, 0 |
| Functions defined | 13371 | 13405 (35 added, 1 changed signature) |
| Distinct calls | 76013 | 76360 (389 added, 42 removed) |
| Python modules that failed to parse | 0 | 0 |
| Define names read by the new code and missing from the XML | | 0 of 6 |

- The 35 added functions are the policy helpers (`AIBuildingLinePolicy`, `AIStrategicDefensePolicy`, the
  new `AICivicPolicy` and `AIDiplomacyPolicy` functions), `CvPlayerAI::AI_resourceReservationVal`,
  `AI_tradeReservationVal`, `CvPlot::refreshRevealedRouteOnly`, `isRevealedRouteDirty` and
  `isAIEconomy`.
- `EventTriggeredData`'s compiler-written copy functions also appear. Their source files are unchanged:
  this is a difference in what the compiler writes out of line.

## 4. Findings

### 4.1 Errors

| ID | Where | Fact | Effect | Status |
|---|---|---|---|---|
| R1 | `Assets/CvGameCoreDLL.dll` in the repository | The shipped DLL was last replaced by `df09f82`, before passes 3 to 8, and has not changed since. It contains none of the strings that only passes 3 to 8 add (`AI_ECONOMY_FLAGS`, `BUILDINGCLASS_TOWN_ESSENTIALS`, `UNITCLASS_ROMAN_COLONIST`, `CIVIC_PEASANTRY`, `BUILDING_WORLD_BANK`); a build of `ede81881b7de` contains each. Passes 3 to 7 also removed the Python that applied the Colonist, Pioneer and Roman Colonist founding packages (`RoMEventManager.onCityBuilt`, line 460) and moved it into `CvUnit::found` (`CvUnit.cpp:6266`). | A game run from `main` as shipped has none of the C++ changes of passes 3 to 8, and no founding packages at all: the Python is gone and the shipped DLL lacks the C++. The XML of passes 3 to 8 (`AI_CUNNING_FLAGS` 1023, `AI_ECONOMY_FLAGS` 15) asks for behaviour that DLL does not have. | confirmed |
| R2 | `CvCityAI::AI_buildingValueThreshold`, upgrade-pair table (`CvCityAI.cpp:6062`) | The table that subtracts the value of a building an upgrade deletes holds 44 pairs. The upgrade lines `RoMEventManager.py` applies hold 81 (read by `toolchain/harness/gen_rom_tables.py`). None of the 44 is wrong. The 37 missing pairs include the whole power-plant line (Hydro, Nuclear and Fusion plants each replace the Coal, Oil and Japanese Shale plants), the National Shield, and every skip-tier replacement (a Commercial Center also removes a Fair or a Market). Where the Python removes several lower tiers, the C++ subtracts only the most valuable one. | For those buildings the AI values the upgrade without the building it destroys. | confirmed |
| R3 | `CvPlayerAI::AI_corporationValue` (`CvPlayerAI.cpp:13209`) | The gross value is a weight times `YieldProduced` (hundredths per resource: 75 is 0.75 food) times the resource count, then times 3. So one food per turn counts as 30000. `calculateCorporationMaintenanceTimes100` is in hundredths of gold, so two gold per turn counts as 200. `corporationNetValue100` subtracts the second from the first. | The "net-profit maintenance check" weighs gold paid about 100 times less than gold produced, and rarely changes a decision. | confirmed (ineffective, not harmful) |

### 4.2 Changes of behaviour the commit messages call fixes, or do not state

| Where | Fact |
|---|---|
| `AI_CUNNING_FLAGS` (`BBAI_AI_Variables_GlobalDefines.xml:61`) | Default raised from 127 to 1023. This switches on staged-army deterrence and Open Borders cancellation (128), anti-hegemon coalitions and deterministic peace offers (256), and tactical changes (512) for every game. |
| `CvUnitAI::AI_nuke` and others (`CvUnitAI.cpp:12298, 12406, 18769, 22539`) | Nuclear targets now include players the AI is Annoyed with, not only Furious. The message calls it a targeting fix. |
| `CvCityAI::AI_chooseProduction` (`CvCityAI.cpp:1048`) | With `AI_ECONOMY_FLAGS` 4 (on by default), a city with a specialised governor drops the production, gold, research and maintenance building focus, and keeps only what its governor's case adds back. A Scholar city values buildings by research, specialists, happiness and health only. Every governor has a case. |
| `AI_RbombardPlot`, `AI_RbombardUnit`, `AI_RbombardCity` | The early return while `DCM_NAVAL_BOMBARD` is set is removed. |
| `AI_Abombard`, `AI_FEngage`, `AI_RbombardNaval` | The 50 % random skip and the random value factor are removed, so these run every turn and choose deterministically. |
| `AI_doPeace` | With 256 on, peace offers pick the cheapest technology and the most fitting city instead of a random one. |
| `AI_maxGoldPerTurnTrade` (pass 2) | A human or teammate may now promise more gold per turn than its income: the income plus its treasury over `PEACE_TREATY_LENGTH`. |
| Synchronised random numbers | Several AI draws are removed or added. The sequence changes, but the same way on every machine: no desync. |

### 4.3 Turn time: work added in hot paths (open)

- `AI_buildingValueThreshold`: for every building evaluated, a loop over all building classes. For each
  class that needs this one, a recursive evaluation of the downstream building, one level deep, guarded
  by a static flag.
- A 5x5 scan of every unit around the city, added to `AI_isDanger`, `AI_neededDefenders` and
  `AI_chooseProduction`. `AI_isDanger` is called often.
- `AI_doDiplo`: a 5x5 scan around every own city, for every Open Borders deal, every turn. A swap search
  over every pair of resources, with `canTradeItem` on each.

None of this was measured. Section 6 says how.

### 4.4 Checked and found correct

| Where | What was checked |
|---|---|
| `CvGame::pageGraphics` (pass 2) | The centre-out ring visits each ring's cells once and keeps to the window. Every budget break ends its loops. The page-out cursor resumes. `m_bPagingPendingOut` is set from `bMoreOut` at the end (line 3282). |
| `AI_considerOffer` called for AI-to-AI gold-per-turn cancellation | It is `const`. Both deal orientations pass the right lists. |
| `CvPlayer::hasStateReligionHolyCity`, `hasStateReligionShrine` | `=` became `==`: correct. |
| `AI_RbombardNaval`, `AI_Abombard`, `AI_FEngage`, `AI_RbombardUnit` | The loop nesting and the null guards are correct. |
| 64-bit power conversions in `CvTeamAI` and `CvPlayerAI` | The same ratios, saturated to `int`. |
| `CvPlayer::setUpgradeAnywhere`, `processCivics` | Clearing the flag re-checks every trait and every other active civic. Only `init` and `processCivics` set it, and it is saved. |
| `CvUnit::found` founding packages | The same buildings, coastal additions, `canConstruct(..., false, true, false)` test and populations as the removed Python handler (messages 410, 411, 5088). `ROM_MULTIPLAYER_FIX` is 0. |
| `AI_assaultForecast` capture | A winning attacker advances into an emptied plot regardless of its moves (`canAdvance`). |
| `CvSelectionGroup::groupAttack` bombard | The bombard pushed inside a mission completes at once. `continueMission` re-reads the queue head, and `AI_update` falls through to the hold step on the next try. |
| `CvTeamAI::AI_makePeaceTrade` | The land ratio now uses the peace team: a correct fix. |
| `CvPlot::doImprovementUpgrade`, `getUpgradeTimeLeft` (pass 8) | The lattice step averages the fractional rate exactly, and the turns left match it. `isOwned()` removes a `GET_PLAYER(NO_PLAYER)` read for improvements that upgrade outside borders. |
| `getWorkRate`, `workRate` (pass 8) | `NO_UNIT` is skipped. The rate floor is 10 % and at least 1. |
| `setInquisitionConditions` (pass 8) | `NO_CIVIC` is skipped, and a disallowing civic now clears the flag. |
| Guilds civic `iRevIdxDistanceModifier` (pass 8) | `CvCivicInfo::read` reads that tag; the base civics use it 68 times. |
| `RevCivicsUtils.py` (pass 8) | `initCivicsList` declares `global civicsList`, and every new caller initialises the list first. |
| `AI_corporationValue` with no city | It falls back to the capital. |
| `AI_yieldValue` process conversion | `aiYields` is a local copy. |
| `AI_tradeReservationVal` | It keeps `AI_tradeGiveVal`'s structure. Only resources, gold and gold per turn are revalued. |

### 4.5 An error in the map, found here

108 of the 220 "calls through a function pointer" in `map/unresolved.tsv` were switch statements compiled
as jump tables (`jmp DWORD PTR $LN…[reg*4]`). `extract_asm.py` now skips them.

## 5. Readings

**1. Anyone playing `main` from the repository plays without passes 3 to 8 and without founding
packages.**
- *Facts:* R1. `git log -- Assets/CvGameCoreDLL.dll` lists `df09f82` as the last change. The strings of
  passes 3 to 8 are absent from that DLL.
- *Would contradict it:* players installing a DLL built from `ede81881b7de` instead of the shipped one.

**2. The building-line valuation was written from memory of the upgrade lines, not from them.**
- *Facts:* R2. The table holds the first tier of each line and misses every line that skips tiers or
  has several predecessors. The Python's lists are machine-readable (`gen_rom_tables.py` reads them).
- *Would contradict it:* the 37 missing pairs being removed from the Python on purpose. They are present
  at `ede81881b7de`.

**3. The passes make the AI spend more time per turn.**
- *Facts:* 4.3.
- *Would contradict it:* turn times within noise of `c08a472` in the harness (section 6).

## 6. Open

- **Turn time and stability of passes 3 to 8 in play.** These need a harness build of `ede81881b7de`:
  either the staging and balance patches rebased onto it, or the harness's diagnostics that read those
  patches' members made optional. Then seeded runs against `c08a472`, comparing `turn_seconds` and
  `completed`.
- **Whether the shipped DLL is exactly pass 2.** A build of `08893b2` is 4096 bytes larger than the
  shipped DLL. It may come from other build settings. It is not passes 3 to 8 in any case.
