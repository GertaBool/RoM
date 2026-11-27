# Review of the GitLab passes 2 to 8

What the four commits called "pass 2" to "pass 8" on GitLab `main` changed, what the code map and the
checks show about them, and what reading every changed hunk found. Written by hand at GitLab `main`
`ede81881b7de`, against the commit before pass 2, `c08a472`.

Sections 1 to 4 describe. Section 5 holds the readings. Section 6 lists what stays open. Section 7 follows
the passes into the agenda planner, the city governors and the military operations.

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

114 of the 220 "calls through a function pointer" in `map/unresolved.tsv` were switch statements compiled
as jump tables (`jmp DWORD PTR $LN…[reg*4]`). `extract_asm.py` now skips them; 106 remain.

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

## 7. Agenda planner, city governors and military operations

### 7.1 How they were traced

- The map's callees of `CvPlayerAI::AI_updateAgenda`, `CvCityAI::AI_updateLocalGovernor`,
  `AI_buildGovernorChooseProduction`, `CvPlayerAI::AI_updateMilitaryOperations`, `CvUnitAI::AI_operationMove`
  and `AI_reinforceOperation`, three calls deep, crossed with the functions the passes changed.
- Then by hand: what the six read, what fills those fields, and what reads `m_iGovernorType`, the agenda and
  the war plans.
- None of the six functions changed. Their inputs did.
- **Scope:** pass 2, the only one in the shipped DLL, touches none of the code below. Its one hunk on these
  paths, `AI_cityThreat`, only changes how a power ratio is computed. Everything in this section acts only
  with a DLL built from `ede81881b7de`. The XML defaults that switch it on are `AI_CUNNING_FLAGS` 1023
  (bits 128 and 256) and `AI_ECONOMY_FLAGS` 15 (bit 4).

### 7.2 City governors

| ID | Where | Fact |
|---|---|---|
| GV1 | `CvCityAI::AI_chooseProduction`, `CvCityAI.cpp:1048` | `bSpecGov` is true for every governor above `GOVERNOR_STEWARD`. In `AICityGovernorPolicy.h` that is all eight of them, Agriculturalist to Colonial. Those cities lose the production, gold, research, maintenance and espionage foci from `iEconomyFlags`. Only happiness, health and their governor's case remain. `iEconomyFlags` drives the economy-building calls at `CvCityAI.cpp:1498, 2541, 3282, 3291`. What remains: Agriculturalist: food, health, happiness. Harbourmaster: sea, food, gold. Merchant and Colonial: gold, maintenance. Industrialist: production. Scholar: research, specialists. Curator: culture, happiness. Castellan: defence, experience, production. Each also keeps happiness and health. Before the passes, every case added to the full set. |
| GV2 | `CvCityAI::AI_isDanger`, `CvCityAI.cpp:6828` | With bit 128 set, a city is in danger when visible land units that can attack stand within two plots, and their total `currCombatStr` is at least 80 % of the city's own plot strength. Those units must belong to a non-barbarian player that is not at war with the owner, not a vassal or master, and not Friendly. Before, only `AI_getAnyPlotDanger`, which covers enemies at war, counted. `MIN_CITY_RANGE` is 1 (`GlobalDefines.xml:226`): a foreign city two plots away lies inside the scan. |
| GV3 | `AI_updateLocalGovernor` with `AICityGovernorPolicy` | `context.danger` comes from `AI_isDanger`. With danger, the Castellan is eligible, with a utility of 80 + 2 × production + culture pressure. The Steward's utility is 40 + food + production + commerce. Example: a city with 12 food, 8 production and 10 commerce scores 96 for the Castellan and 70 for the Steward. `prosperity` subtracts 20 for danger. Every turn of danger between reviews adds a disruption turn. A review held while danger is on gives negative performance, which replaces the incumbent and resets its reputation. |
| GV4 | `CvCityAI::AI_specialistValue`, `CvCityAI.cpp:540` | Scholar and Agriculturalist cities value Great People points at 10. The default is 4, and Great People emphasis gives 20. |

### 7.3 Agenda planner

| ID | Where | Fact |
|---|---|---|
| AG1 | `CvTeamAI::AI_doWar`, anti-hegemon branch (`CvTeamAI.cpp`, before the log line "starting ANTI-HEGEMON") | The branch is the last `else if` after the random total, limited and dogpile war rolls. So it runs on every turn those rolls fail, with no random gate and no `AI_noWarAttitudeProb` test. Only Friendly blocks it. `isHegemonThreat` counts the team itself among the met teams. With three met teams, the leader holds at least a third of the power and of the score, so the leader always passes the 33 % and 32 % tests. Coalition power adds the reachable power of every met team Cautious or worse toward the target, whether or not that team plans war. |
| AG2 | `AI_doWar`, `WARPLAN_PREPARING_LIMITED` handling | With cunning bit 1 set and no strike force ready, the plan is dropped after `20 × iAbandonTimeModifier / 100` turns. On the next turn the anti-hegemon branch can set it again, since `getAnyWarPlanCount(true)` is 0 once more. |
| AG3 | `AI_updateAgenda`, `CvPlayerAI.cpp:4622` | A war plan adds 350 to Survive, 850 to Conquest and 250 to Power Spike, and takes 300 from Expand Land. `AI_isFinancialTrouble` lowers its safe percentage by 12 under any war plan. |
| AG4 | `CvPlayerAI::AI_isFinancialTrouble`, `CvPlayerAI.cpp:4201` | The commerce sent to culture and espionage now counts as income. An empire with those sliders up is in financial trouble less often. That trouble is worth 900 to Recover, and costs 700 to Expand Land and 300 to Conquest. |
| AG5 | `CvTeamAI::AI_getEnemyPowerPercent` | Only widened to 64 bits and capped. The result is the same unless the old one overflowed. |

### 7.4 Military operations

| ID | Where | Fact |
|---|---|---|
| OP1 | `CvPlayerAI::AI_getTotalFloatingDefenders` | `UNITAI_COLLATERAL` and `UNITAI_DEFENSE_AIR` are no longer counted. The list `AI_chooseLeastRepresentedUnit` fills that count from (`CvCityAI.cpp:2004`) still holds `UNITAI_COLLATERAL` at weight 100, and is used at lines 2008 and 3111. Collateral units built to meet the quota no longer reduce the shortfall. Collateral is also a role that operations request (`aiDesiredRoles[UNITAI_COLLATERAL]`). |
| OP2 | `CvCityAI::AI_neededDefenders`, `CvCityAI.cpp:6632` | The same staged-unit scan as GV2 adds 1 to 6 defenders per city, from `stagedGarrisonDeficit`, in peacetime. |
| OP3 | `CvTeamAI::AI_calculateAreaAIType`, `CvTeamAI.cpp:621` | After a recent attack, an area is now set to MASSING instead of DEFENSIVE when own power is at least 65 % of enemy power and the war-success ratio is at least −50. |
| OP4 | The operation functions | `AI_updateMilitaryOperations`, `AI_operationMove` and `AI_reinforceOperation` are unchanged. An operation starts only from an `UNITAI_ATTACK_CITY` group, against a city of a team at war. The general's personality reads `AI_getAgendaBudget(AI_BUDGET_EXPANSION)`. |
| OP5 | `CvUnitAI::AI_Abombard`, reached from `AI_operationMove` through `AI_anyAttack` | Its random skip is removed, but the function acts only when `DCM_ARCHER_BOMBARD` is on. Its default is 0 (`GlobalDefinesAlt.xml:75`) and False (`Config/RevDCM.xml:65`). No effect by default. |
| OP6 | `CvPlayerAI::AI_doTurnUnitsPost`, tactical upgrades (bit 512) | Units scoring 1000 or more skip the upgrade budget. A unit in a city under `AI_getAnyPlotDanger` gets 1000. So does a unit with no danger, if it has the experience bonus, a capped unit class and at least 44 experience points. |

### 7.5 Readings

**4. Under a DLL built from `main`, specialised governors stop building the economy.**
- *Facts:* GV1. Eight of nine governor types drop the production, gold, research and maintenance foci from
  the main economy-building calls.
- *Would contradict it:* other building calls without `iEconomyFlags` (for example the
  `AI_buildGovernorChooseProduction` set at `CvCityAI.cpp:12770`, which serves human governors) filling those
  buildings in AI cities. In play, AI cities with non-Steward governors keeping pace in markets, libraries and
  forges.

**5. Peaceful neighbours turn border cities into Castellan cities and make governors churn.**
- *Facts:* GV2, GV3. Units in transit under Open Borders, border garrisons and cities two plots away all count.
  The test needs 80 % of the city's own plot strength, and a frontier city often holds one or two defenders.
- *Would contradict it:* governor logs in peacetime showing few Castellan appointments and few replacements on
  negative performance.

**6. The agenda planner spends much more of the game under a war plan, so it leans to Conquest and Survive.**
- *Facts:* AG1 to AG3. There is no random gate or attitude test, a three-team leader always qualifies, and an
  abandoned plan is re-set at once.
- *Would contradict it:* `AI_doWar` logs showing the anti-hegemon line rarely. Or agenda histories with the
  same share of Conquest and Survive turns as at `c08a472`.

**7. Fewer and later operations, because units stay home.**
- *Facts:* OP1, OP2 hold more units as defenders. OP4: operations need attack-city groups, and these
  changes do not make any. OP3 pulls the other way after an attack.
- *Would contradict it:* the number of operations created per war, and their group sizes, matching
  `c08a472` in seeded runs.

### 7.6 Open

- How often each condition holds in play: the Castellan share, governor replacements, turns under a war plan,
  operations per war. This needs the harness build of `ede81881b7de` from section 6, and logs at
  `gTeamLogLevel` and `gCityLogLevel` of 2 or more.
- Whether GV4's value for Agriculturalists is intended. The commit gives no reason.
