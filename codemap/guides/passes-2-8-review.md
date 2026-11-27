# Review of the GitLab passes 2 to 8

What the four commits called "pass 2" to "pass 8" on GitLab `main` changed, what the code map and the
checks show about them, and what reading every changed hunk found. Written by hand at GitLab `main`
`ede81881b7de`, against the commit before pass 2, `c08a472`.

Sections 1 to 4 describe. Section 5 holds the readings. Section 6 lists what stays open. Section 7 follows
the passes into the agenda planner, the city governors and the military operations, through shared state.

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

This section replaces an earlier version written before the state map existed. That version traced the
three systems by calls only. It missed the coupling through shared state, and how far `AI_isDanger`'s
consumers reach.

### 7.1 How they were traced

1. **Shared state.** `tool/state.py` lists every class member (3318), and every function that reads or
   writes each one, directly or through an accessor (`map/state.tsv`). `tool/subsystems.py` groups the AI
   classes' members by the functions that write them (`subsystems.md`). Without being told, that grouping
   puts the three systems in groups of their own:
   - agenda: group 5, 11 members, from `m_iAIAgenda` to `m_kAIStrategicContext`;
   - operations: groups 14 and 74, `m_aiMilitaryOperations`, `m_aiGeneralCareers` and the delivery cache;
   - governors: group 31, the seven `m_iGovernor…` members;
   - war plans: groups 4 and 30, `m_aeWarPlan` and `m_aiWarPlanStateCounter`.
2. **Consumers of every change.** `tool/impact.py` lists, for each of the 106 functions the four commits
   changed, every caller, every member it writes and every reader of that member
   (`reviews/impact-c08a472-ede8188.tsv`, 29390 links, none left out).
3. **Reading.**
   - Every call site was read for: `AI_isDanger` (11 in cities, 13 in units), `AI_isFinancialTrouble` (40 sites
     in 33 functions), `AI_neededDefenders` and `AI_isDefended`, and `AI_getTotalFloatingDefenders`.
   - Also read: the operation functions (`AI_updateMilitaryOperations`, `AI_reinforceOperation`,
     `AI_getOperationReinforcementGroup`), `AI_updateAgenda`, and the governor policy.
   - The other changed functions were classified from their hunks (section 7.6).
4. **Scope.** The shipped DLL holds pass 2 only, and pass 2 changes none of the behaviour below. Its one hunk
   on these paths, `AI_cityThreat`, only changes how a power ratio is computed. Everything here acts only with
   a DLL built from `ede81881b7de`, where the XML defaults switch it on: `AI_CUNNING_FLAGS` 1023 (bits 128, 256,
   512) and `AI_ECONOMY_FLAGS` 15 (bit 4).

### 7.2 How the three systems are coupled (from the state map)

| From | To | Through |
|---|---|---|
| governors | agenda | `AI_updateAgenda` reads every city's `AI_getGovernorType`, reputation and completed terms, and adds `AIFeedbackPolicy::agendaDelta`, at most ±120 per agenda. |
| operations | agenda | `AI_updateAgenda` reads finished operations' doctrine evidence (`m_aiGeneralCareers`). |
| war plans | agenda | `AI_getStrategicContext` sets `hasWarPlan` (`m_kAIStrategicContext`). |
| agenda | production | `AI_chooseProduction` adds `(AI_getAgendaBudget(AI_BUDGET_MILITARY) − 200) / 20` to the unit-build chance. |
| agenda | operations | A new operation's general personality reads `AI_getAgendaBudget(AI_BUDGET_EXPANSION)`. |
| governors | production | Castellan +10 to the unit-build chance, Agriculturalist and Scholar −5 (`CvCityAI.cpp:923`). Building foci (GV1). |
| governors | citizens and workers | `AI_yieldValue`'s governor multipliers reach `AI_plotValue` (tiles worked), `AI_updateBestBuild` (improvements chosen) and `AI_updateWorkersNeededHere`. |
| danger | all three | `AI_isDanger` feeds the governor context, production, drafting, hurrying, garrisons and transports (7.3). |

### 7.3 `AI_isDanger`: what peacetime "danger" now does

**Fact (`CvCityAI.cpp:6828`).** With bit 128 set, a city is in danger when visible land units that can attack
stand within two plots, and their total `currCombatStr` is at least 80 % of the city's own plot strength.
Those units must belong to a non-barbarian player that is not at war with the owner, not a vassal or master,
and not Friendly. `MIN_CITY_RANGE` is 1 (`GlobalDefines.xml:226`), so a foreign city two plots away is inside
the scan. Human-owned cities are unaffected (`!isHuman()`).

Every consumer, and what danger does there:

| Site | Effect of danger |
|---|---|
| `AI_updateLocalGovernor` (11421, 11468) | Disruption turn. Castellan becomes eligible. −20 prosperity at review (GV2, GV3). |
| `AI_chooseProduction` (746; used at 43 places in the function) | Stops workers, settlers, sea workers, wonders and most economy buildings. Builds a minimum of 4 attack units plus the defender shortfall (1827). Raises the odds of defensive units (2034). Builds experience buildings (3266). Raises the settling threshold by half (2149). |
| `AI_buildGovernorChooseProduction` (12660) | None: it serves human cities' governors, and the new scan skips human owners. |
| `AI_bestUnit` (3546) | Settler value ×8 instead of ×20, worker ×2 instead of ×7, explorer ×6 instead of ×15, sea worker ×3 instead of ×10. |
| `AI_neededDefenders` (6601, 6620) | +1 defender, and +1 more in a city taken in the last 10 turns. |
| `AI_doDraft` (8881) | When not defended, the draft skips the financial-trouble check (8884) and the population check (8891). |
| `AI_goldHurryScore` (8989), `AI_doHurry` (9030, 9159) | A combat unit's hurry value is 50 instead of 4 in peace. Defence buildings count as essential within 3 turns. The turtle gold thresholds are lower. |
| `AI_guardCity` | A unit with `bLeave` may not leave the city. |
| `AI_assaultSeaMove` (`CvUnitAI.cpp:7358`) | A loaded transport in a city in danger unloads all its cargo and skips its turn: an invasion force waiting in port disembarks. |
| `AI_pickup` (20855, 20933, 20984) | Attack-city units in a city in danger are not picked up. Transports do not go to such cities. |
| `AI_defendPlot` (23595) | Every unit asked whether to defend its plot in an own city in danger answers yes. |
| `AI_guardCityAirlift`, `AI_offensiveAirlift`, `AI_assaultSeaReinforce` | Such cities are preferred as airlift and reinforcement destinations. |
| `AI_airOffenseBaseValue`, `AI_airBombDefenses`, `AI_RbombardNaval`, `AI_defenseAirMove` | Value ×2 or ×3. For foreign cities, from their owner's side. |

### 7.4 Findings by system

**City governors**

| ID | Fact |
|---|---|
| GV1 | `bSpecGov` (`CvCityAI.cpp:1048`) is true for all eight governors above the Steward. They drop the production, gold, research, maintenance and espionage foci from `iEconomyFlags`, which the economy-building calls at lines 1498, 2541, 3282 and 3291 use. They keep happiness, health and their own case. Agriculturalist: food. Harbourmaster: sea, food, gold. Merchant and Colonial: gold, maintenance. Industrialist: production. Scholar: research, specialists. Curator: culture. Castellan: defence, experience, production. |
| GV2 | Danger (7.3) makes the Castellan eligible, with a utility of 80 + 2 × production + culture pressure. The Steward's is 40 + food + production + commerce. With 12 food, 8 production and 10 commerce, that is 96 against 70. |
| GV3 | Danger subtracts 20 from prosperity. A review held while danger is on gives negative performance, and the incumbent is replaced with its reputation reset. Every turn of danger between reviews is a disruption turn. |
| GV4 | Scholar and Agriculturalist cities value Great People points at 10 (`CvCityAI.cpp:540`). The default is 4. |
| GV5 | Governors feed the agenda (7.2). Computed from `AIFeedbackPolicy`, if every city has a Castellan: new governors (0 terms, reputation 0) add 11 to Survive, 11 to Conquest and 9 to Power Spike. Veterans (5 terms, reputation 100) add 68, 68 and 56. Stewards add between −2 and +4. |

**Agenda planner**

| ID | Fact |
|---|---|
| AG1 | The anti-hegemon branch of `AI_doWar` is the last `else if` after the three random war rolls. It runs on every turn they fail, with no random gate and no `AI_noWarAttitudeProb` test. Only Friendly blocks it. |
| AG2 | `isHegemonThreat` counts the team itself among the met teams. With three, the leader holds at least a third of power and of score, so it always passes the 33 % and 32 % tests. Coalition power adds every met team Cautious or worse toward the target, whether or not it plans war. |
| AG3 | A `PREPARING_LIMITED` plan with no strike force ready is dropped after `20 × iAbandonTimeModifier / 100` turns. On the next turn `getAnyWarPlanCount(true)` is 0, and the branch can set it again. |
| AG4 | A war plan adds 350 to Survive, 850 to Conquest and 250 to Power Spike, and takes 300 from Expand Land. `AI_isFinancialTrouble` lowers its safe percentage by 12 under any war plan. |
| AG5 | `AI_isFinancialTrouble` counts commerce sent to culture and espionage as income, so it is true less often with those sliders up. All 40 call sites use it the same way: trouble means cut costs or hold back. They include unit disbanding (`AI_doMilitary`, `CvPlayerAI.cpp:17139`), espionage spending (17586, so a high espionage slider no longer counts against itself), settlers, hurrying, drafting, trades, Recover (+900) and the finance gate on war (`AI_doWar`, `CvTeamAI.cpp:5166`, which AG1 checks). |
| AG6 | GV5 and AG4 add up: Castellan cities and war plans both push Survive and Conquest. |

**Military operations**

| ID | Fact |
|---|---|
| OP1 | `AI_getTotalFloatingDefenders` stopped counting `UNITAI_COLLATERAL` and `UNITAI_DEFENSE_AIR`. The list `AI_chooseLeastRepresentedUnit` fills that count from (`CvCityAI.cpp:2004`, used at 2008 and 3111) still holds `UNITAI_COLLATERAL`. Collateral units built to meet the quota no longer reduce the shortfall. |
| OP2 | `AI_neededDefenders` adds 1 to 6 defenders per city from the peacetime scan. Through `AI_isDefended`, that reaches `AI_guardCity`, `AI_guardCityAirlift`, `AI_chokeDefend`, `AI_pickup`, `AI_doDraft`, `AI_doHurry` and `AI_chooseProduction`: units stay as garrisons. |
| OP3 | 7.3: transports with an invasion force unload in a port in danger, attack-city units there are not picked up, and garrisons do not leave. |
| OP4 | `AI_promote` (bit 512): a land unit of level 2 or more, in enemy territory during a war and with less than 20 damage, keeps a ready promotion until it has the experience for the next level as well (`isPromotionReady` means experience ≥ `calculateExperience(getLevel())`). Units on campaign fight one promotion short. |
| OP5 | `AI_calculateAreaAIType`: after a recent attack, MASSING instead of DEFENSIVE at 65 % of enemy area power or more. Area AI type has 48 readers (`query.py state m_aeAreaAIType`). In `AI_doWar`'s total-war switch, MASSING leaves `bAreaValid` as it was, where DEFENSIVE set it to false. |
| OP6 | `AI_reserveMove` (bit 512): a lone reserve unit that can build routes builds one on an own plot without danger. |
| OP7 | Tactical upgrades in `AI_doTurnUnitsPost` (bit 512): a unit scoring 1000 or more skips the upgrade budget. That is a unit in a city under `AI_getAnyPlotDanger`, or one with the experience bonus, a capped unit class and at least 44 experience points. |
| OP8 | The operation functions themselves are unchanged. An operation starts only from an `UNITAI_ATTACK_CITY` group, against a city of a team at war. `AI_Abombard`'s change acts only with `DCM_ARCHER_BOMBARD` on, which is off by default (`GlobalDefinesAlt.xml:75`, `Config/RevDCM.xml:65`). |

**Found by this trace, present before the passes**

| ID | Fact |
|---|---|
| PRE1 | Operations ask for roles that are never delivered. A Logistician's operation sets `aiDesiredRoles[UNITAI_RESERVE] = 2`. A Colonizer's sets `UNITAI_CITY_DEFENSE` 2 and `UNITAI_WORKER` 1. But `AI_getOperationReinforcementGroup` returns nothing for a unit outside `isOperationFieldRole` (attack-city, attack, counter, collateral, pillage), and only the moves of those five roles call `AI_reinforceOperation`. The same code is at `c08a472`. |

### 7.5 Readings

**4. Under a DLL built from `main`, specialised governors stop building the economy.**
- *Facts:* GV1.
- *Would contradict it:* AI cities with non-Steward governors keeping pace in markets, libraries and forges in
  play. Those buildings coming from calls that do not use `iEconomyFlags`.

**5. Peaceful neighbours make AI cities behave as if besieged.**
- *Facts:* 7.3, GV2, GV3, OP2, OP3. One condition, units of a non-Friendly neighbour near a lightly held city,
  touches production, governors, drafting, hurrying, garrisons and invasion transports at once.
- *Would contradict it:* logs in peacetime showing `AI_isDanger` rarely true without a war.

**6. The agenda planner leans to Conquest and Survive, from two directions.**
- *Facts:* AG1 to AG4, plus GV5 through Castellan cities. AG5 adds less financial caution.
- *Would contradict it:* agenda histories with the same share of Conquest and Survive turns as at `c08a472`.
  Or the anti-hegemon log line appearing rarely.

**7. Fewer and weaker operations, at the moment the agenda asks for war.**
- *Facts:* OP1 to OP4 keep units home, unload invasions and withhold promotions, while 6 raises the military
  budget. OP5 pulls the other way after an attack.
- *Would contradict it:* the number of operations per war and their group sizes matching `c08a472` in seeded
  runs.

### 7.6 The other changed functions

Of the 106 changed functions, these change no result except in overflow, by their hunks: the 64-bit power
ratios in `CvTeamAI` (`AI_getEnemyPowerPercent`, `AI_endWarVal`, `AI_startWarVal`, `AI_minorKeepWarVal`,
`AI_getBarbarianCivWarVal`, `AI_surrenderTrade`, `AI_declareWarTradeVal`), `AI_cityThreat`,
`AI_getConquestVictoryStage`, and the `AIDiplomacyPolicy` helpers.

Graphics paging and reveal (`CvGame::pageGraphics`, `updateGraphicsPaging`, `processDeferredReveals`,
`CvCity::pageGraphics`, `CvUnit::pageGraphics`, `CvPlot::refreshRevealedRouteOnly`, `isRevealedRouteDirty`,
`CvGame::reset`) and the pass 8 work-rate functions were checked in section 4.4.

The remaining behaviour changes were listed in 4.2 and are traced in `reviews/impact-c08a472-ede8188.tsv`:
civic, technology, building, corporation, trade and diplomacy valuation, founding, nukes and bombard.
Their consumers were not read one by one: listed, not read.

### 7.7 Open

- How often each condition holds in play: `AI_isDanger` in peacetime, the Castellan share, governor
  replacements, turns under a war plan, operations per war and their size. This needs the harness build of
  `ede81881b7de` from section 6, and logs at `gTeamLogLevel` and `gCityLogLevel` of 2 or more.
- The 48 readers of area AI type under OP5, read one by one.
- Whether GV4's value for Agriculturalists is intended. The commit gives no reason.
