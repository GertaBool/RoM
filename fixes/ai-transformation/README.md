# 5-pass RoM AI transformation (Passes 3–7 over pass 2 `f0d5629`)

[`../ai-transformation.patch`](../ai-transformation.patch) applies cleanly on top of pass 2
([`../ai-and-paging-pass2.patch`](../ai-and-paging-pass2.patch) over `c08a472`, commit `f0d5629`).
It serves prediction `P17` (`method/mission/register.json`, hypothesis `H12`).

## Applying on Windows (CRLF)

Because RoM's C++ files use CRLF line endings, preserve CR bytes when applying with `git am`:

```sh
git am --keep-cr ai-transformation.patch
```

(Or apply directly to the working tree with `git apply ai-transformation.patch`.)

## Feature switches (`BBAI_AI_Variables_GlobalDefines.xml`)

Rule and logic bug fixes (Pass 3) apply unconditionally. Behavioral upgrades (Passes 4–7) are
explicitly gated behind two bitmasks so every subsystem can be toggled or A/B tested independently:

| Define | Default | Bit | Controls |
|---|---:|---:|---|
| `AI_ECONOMY_FLAGS` | `15` | `1` | `AI_ECONOMY_BUILDING_LINES`: net-delta building upgrades, per-city `BuildingClassNeededs` lookahead, obsolescence decay, Golden Age / military / Python-scripted Wonders |
| `AI_ECONOMY_FLAGS` | `15` | `2` | `AI_ECONOMY_CIVIC_COEVAL`: `Peasantry` Cottage & `Coastal` co-evaluation, `RevIdx` civic stability, `zCivics` unlock credit, `GameSpeed`-scaled civic horizon |
| `AI_ECONOMY_FLAGS` | `15` | `4` | `AI_ECONOMY_TECH_AND_CORP`: buildable-building bonus unlocks, inflation-scaled corporation net profit, multi-pair surplus luxury swaps, `FirstFreeUnitClass`/`TechCityTrade`/`DisableTechs` tech valuation, depth-5/6 research |
| `AI_ECONOMY_FLAGS` | `15` | `8` | `AI_ECONOMY_GOVERNOR_SPEC`: City Governor specialization, 50% `Process` parity, negative-food Slave starvation guard, `Financial`/`Agricultural` extra-yield thresholds |
| `AI_CUNNING_FLAGS` | `1023` | `128` | `AI_CUNNING_STAGED_THREAT`: peacetime border & offshore staged-army garrison deterrence, proactive Open Borders revocation on lethal staging |
| `AI_CUNNING_FLAGS` | `1023` | `256` | `AI_CUNNING_COALITION`: prospective anti-hegemon balance-of-power coalitions, Victory-Level-3 prevention, defensive counterstroke posture, deterministic `AI_doPeace` demands |
| `AI_CUNNING_FLAGS` | `1023` | `512` | `AI_CUNNING_TACTICAL_MASTERY`: priority-ranked unit upgrades, 65% hero odds floor, non-stall siege bombard, wartime promotion banking, transport cargo promotions, combat engineer road building |

## What it changes

### Pass 3 — Unconditional rule/logic bug fixes & AI parity
- **Colonist / Pioneer / Roman Colonist AI & MP parity (`CvUnit.cpp`, `RoMEventManager.py`, `CvPlayerAI.cpp`)**:
  - Moved the Colonist (Pop 3 + preset buildings), Pioneer (Pop 4 + preset buildings), and Roman Colonist (Pop 3 + preset buildings) founding packages into deterministic C++ inside `CvUnit::found()` (respecting `canConstruct` and guarded by `ROM_MULTIPLAYER_FIX <= 0`).
  - Removed the broken UI-dependent `CyInterface().getHeadSelectedUnit()` / `sendModNetMessage` block from `RoMEventManager.py::onCityBuilt` (which silently failed for all AIs and caused MP OOS).
  - Updated `CvPlayerAI::AI_unitValue` (`UNITAI_SETTLE`) to value Colonist (+650), Roman Colonist (+650), and Pioneer (+1200) above ordinary Settlers.
- **Diplomacy, economy & floating defense (`CvPlayerAI.cpp`, `CvPlayer.cpp`)**:
  - Fixed `AI_bonusTrade` so `BONUSCLASS_LUXURY`, `BONUSCLASS_GENERAL` (Wine, Dye, Spices, Cotton, Olives), and happy/health bonuses referenced in building `PrereqOrBonuses` are no longer misclassified as strategic military monopolies.
  - Counted slider-diverted Culture and Espionage commerce in `AI_isFinancialTrouble`.
  - Excluded `UNITAI_COLLATERAL` and `UNITAI_DEFENSE_AIR` from `AI_getTotalFloatingDefenders`.
  - Fixed `CvPlayer::setUpgradeAnywhere(bool)` ignoring `false` and `CvPlayer::processCivics` recomputing across active traits and civics on `iChange < 0`.
- **City, assault, team & unit bugs (`CvCityAI.cpp`, `CvSelectionGroupAI.cpp`, `CvTeamAI.cpp`, `CvUnitAI.cpp`)**:
  - Fixed `AI_assaultForecast` capture check (`!isNoCapture() && combatLimit() >= maxHitPoints()` across `pAttacker` and remaining attackers in `aOrder`, fixing 1-move final attackers returning 0% capture).
  - Converted `AI_specialistValue` GPP calculation to 64-bit; fixed `FreeBonus` scaling (`iNumFreeBonuses == -1` zeroing out 1-city civs and 20× extra-copy spam); added `getBonusYieldModifier` to `iPass == 0` focused passes (`FOOD`/`PRODUCTION`/`GOLD`); hoisted dead `isProductionProject()` check out of `eProductionBuilding != NO_BUILDING`.
  - Fixed `AI_makePeaceTrade` (`eTeam` -> `ePeaceTeam`), `AI_getTechMonopolyValue` war-plan check, and remaining 32-bit power overflows in `AI_doWar`.
  - Fixed `AI_settleMove` escort drop, `AI_workerMove` inverted Needed/Have inequality & 80% fort preemption, `AI_betterPlotBuild` `iPlotGroupId == -1` 4× road dead-code bug, `AI_escortSeaMove` argument, `AI_doInquisition` return value, `AI_nuke`/`AI_nukeRange` targeting & negative-penalty clamping, and DCM bombard (`AI_RbombardPlot`/`Unit`/`City`/`Naval`, `AI_Abombard`, `AI_FEngage`) null guards, flag checks, and random skips.

### Pass 4 — Economic & building-line mastery (`AIBuildingLinePolicy.h`, `AI_ECONOMY_FLAGS`)
- Added pure C++03 header `AIBuildingLinePolicy.h` and `isAIEconomy(int)` helper (`CvGameCoreUtils.h`/`.cpp`).
- **Net-delta building upgrades & prerequisite chains (`CvCityAI.cpp`)**: Scores RoM's 29 `RoMEventManager.py` building replacement lines by net incremental delta (with `s_bInLineEval` recursion guard), credits same-city `BuildingClassNeededs` prerequisites (e.g., Settlement -> Town -> City -> Metropolitan Essentials), applies `ObsoleteTech` era depreciation, and values Golden Age triggers/modifiers, unit-upgrade discounts, Great General rate modifiers, and Python-scripted Wonders (`World Bank`, `Crusade`, `Djenne`, `Himeji Castle`, `Nanite Defuser`).
- **Civics, corporations & luxury swaps (`CvPlayerAI.cpp`, `CvCityAI.cpp`)**: Added `iRevIdxLocal`/`National`/`Distance` stability scoring, potential-plot civic co-evaluation (`Peasantry` Cottages, `Coastal` seafood, `iImprovementUpgradeRateModifier` scaling), `zCivics` unlock credit, `GameSpeed`-scaled civic horizon, buildable-building `BonusHappiness`/`Health`/`YieldModifier` credit in `AI_bonusUnlockVal`, inflation-scaled maintenance subtraction in `AI_corporationValue`, and multi-pair surplus luxury swap fallback in `AI_doDiplo`.

### Pass 5 — Strategic defense & coalition diplomacy (`AIStrategicDefensePolicy.h`, `AI_CUNNING_FLAGS`)
- Added pure C++03 header `AIStrategicDefensePolicy.h` and bits `128`, `256`, `512` to `AI_CUNNING_FLAGS` (default `1023`).
- Wired peacetime border & offshore staged-army deterrence into `developBeforeReinforcing`, `AI_neededDefenders`, and `AI_isDanger` (`CvCityAI.cpp`), plus proactive Open Borders revocation on lethal border staging (`CvPlayerAI.cpp`).
- Wired prospective anti-hegemon balance-of-power coalitions, Victory-Level-3 prevention, and `defensiveCounterstrokeAllowed` posture into `CvTeamAI.cpp`, and made `AI_doPeace` tech/city demands deterministic (`CvPlayerAI.cpp`).

### Pass 6 — City specialization & tech lookahead (`CvCityAI.cpp`, `CvPlayerAI.cpp`)
- Activated `iEconomyFlags` City Governor specialization, 50% `Process` hammer-to-commerce parity, negative-food `SPECIALIST_SLAVES` starvation guard, and `getExtraYieldThreshold` (`Financial` 4C, `Agricultural` 5F) in `AI_bestPlotBuild`.
- Added `FirstFreeUnitClass`, `iHappiness`, `TechCityTrade` bonus unlocks, and civ-unique `DisableTechs` scoring in `AI_techValue`, and extended `AI_chooseResearch` lookahead depth to `6` (Ancient/Classical) and `5` (later eras).

### Pass 7 — Tactical combat & execution mastery (`CvSelectionGroup.cpp`, `CvPlayerAI.cpp`, `CvUnitAI.cpp`)
- Added priority-ranked unit upgrade pre-pass in `AI_doTurnUnitsPost` (threatened city defenders -> frontline/war-zone combat units -> high-XP veterans & national-limit heroes before FIFO).
- Added 65% combat odds floor for `iMaxPlayerInstances == 1` combat heroes and non-stall city bombardment before `finishMoves()` in `CvSelectionGroup.cpp`.
- Added wartime single-promotion banking for +50% field heal (`AI_promote`), `getCargoChange()` (`PROMOTION_TRANSPORT1/2/3`) valuation (`AI_promotionValue`), and idle Combat Engineer route-building fallback (`AI_reserveMove`).

## Save compatibility

Zero changes to any `::read` or `::write` serialization method. Save format and DLL export table
(`2,452` exports) are 100% compatible with `c08a472` and pass 2 (`f0d5629`). Empirically verified by
saving a `6,606,272`-byte Turn-250 snapshot from the transformed DLL and loading & advancing it in
both the transformed DLL (Turns 250–300, `RESULT save turn 300 state 0`) and the unmodified
baseline DLL (Turns 250–252, `RESULT save turn 252 state 0`).

## Checks

### Release DLL build
`CLEAN=1 toolchain/build_dll.sh` (Visual C++ Toolkit 2003 under Wine, release target):
**0 errors, 0 warnings**.

| property | value |
|---|---|
| size | `6,189,056` bytes |
| SHA-256 | `94a9c198bbb88357e01dde9448af4c021b76f890e98c0910dd335dec79df7d2b` |
| exports | `2,452` names (identical to `c08a472` and `f0d5629`) |

### Static analysis (`clang-gate`)
`toolchain/clang-gate/diffcheck.sh` across all 9 modified `.cpp` files against `f0d5629`:
**0 new errors, 0 new warnings**.

### Native C++98 unit tests
[`tests/test_ai_transformation.cpp`](tests/test_ai_transformation.cpp) compiled with
`g++ -Wall -Wextra -Werror -std=c++98 -I<rom>/Assets/CvGameCoreDLL`: **ALL PASSED** (covers
`AIBuildingLinePolicy.h` and `AIStrategicDefensePolicy.h`: net-delta upgrades, per-city prereq
credit, obsolescence decay, Golden Age & military wonders, Python-scripted wonders, GameSpeed
civic horizon, inflation-adjusted corporation net profit, staged garrison deficit, proactive Open
Borders revocation, 64-bit anti-hegemon & coalition power gates, and defensive counterstroke
posture).

### Headless harness 300-turn A/B soak (`p15.scn`, seed `1570079469`, Noble, Normal speed)
Paired run on `p15.scn` (`GAMESPEED_NORMAL`, `HANDICAP_NOBLE`, seed `1570079469`, 6 AI civs;
transformed DLL run 0->250 with `HARNESS_SNAPSHOT=250` and resumed 250->300 to test both full
completion and binary save/load):

| Turn-300 metric | Pass-2 baseline (`f0d5629`) | Transformed (`Passes 3–7`) | Change |
|---|---:|---:|---:|
| Alive civs (out of 6) | `6` | `4` | 2 civs conquered |
| Max techs (leader) | `90` | `108` | **+18 techs** |
| Top-3 civs' techs (mean) | `90, 84, 77` (`83.7`) | `108, 104, 99` (`103.7`) | **+20.0 techs/civ** |
| Total score | `4,616` | `5,800` | **+25.6%** |
| Total population | `314` | `520` | **+65.6%** |
| Total research rate | `1,224` | `2,780` | **+127.1%** |
| Total production | `3,122` | `5,311` | **+70.1%** |
| Total buildings | `912` | `1,183` | **+29.7%** |
| Total military power | `18,073` | `23,804` | **+31.7%** |
| Top empire power | `7,207` | `13,845` | **+92.1%** |
| Late-game turn time (T250–297 mean) | `8,430 ms` | `5,514 ms` | **-34.6% faster** |

### Open checks
- **Full seeded harness battery (`P17`)**: `method/mission/evidence/P17/` is open (`n >= 5`
  paired seeded runs).
- **In-game Civ4 executable verification**: live human game testing (Colonist/Pioneer/Roman
  Colonist founding in SP/MP, luxury trading, peacetime border deterrence & Open Borders
  revocation, and late-game combat).
