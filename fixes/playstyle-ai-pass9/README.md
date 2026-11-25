# Playstyle-aligned tactical & economic AI fixes (Pass 9 over Pass 8 `546d223`)

[`../playstyle-ai-pass9.patch`](../playstyle-ai-pass9.patch) applies cleanly on top of
Pass 8 ([`../civic-engine-and-ai-pass8.patch`](../civic-engine-and-ai-pass8.patch), commit `546d223`).
It serves prediction `P19` (`method/mission/register.json`, hypothesis `H14`).

## Applying on Windows (CRLF)

Because RoM's C++ files use CRLF line endings, preserve CR bytes when applying with `git am`:

```sh
git am --keep-cr playstyle-ai-pass9.patch
```

(Or apply directly to the working tree with `git apply playstyle-ai-pass9.patch`.)

## What it fixes

All decision math lives in header-only, engine-independent C++98 [`AIPlaystylePolicy.h`](../playstyle-ai-pass9.patch)
and is integrated across `CvCityAI.cpp`, `CvPlayerAI.cpp`, `CvUnitAI.cpp`, and `CvSelectionGroup.cpp`.

### 1. Build ladder, `0`-route trade projection & `Walls` (`CvCityAI.cpp`)
- **Projected trade-route base (`AI_buildingValueThreshold`)**: Because RoM sets `INITIAL_TRADE_ROUTES = 0`, `getTradeYield()` was `0` in newly founded/conquered cities, zeroing `TradeRouteModifier` and `ForeignTradeRouteModifier` on `Port`, `Harbor`, `River Port`, `Lighthouse`, `Jewellery`, and `Market`. `AIPlaystylePolicy::projectedTradeYield()` now projects both the building's own added trade-route slots and a discounted near-term slot (`65%` of one route) for pure modifier buildings in `0`-route cities.
- **Border-pop buildings ahead of `PROCESS_CULTURE` (`AI_chooseProduction`)**: Evaluates `AI_chooseBuilding(BUILDINGFOCUS_CULTURE, 25)` *before* `AI_chooseProcess(COMMERCE_CULTURE)` so new/captured cities finish permanent `Monument` / `50H` `Walls` instead of stalling on Culture process.
- **Dual-purpose `Walls` (`+1 Culture`, `+30% Defense`, `50H`)**: Credits dual Culture+Defense synergy in `getCultureLevel() <= 1` cities and removes the `3 * pop` random gate on `BUILDINGFOCUS_DEFENSE` for unfortified frontier/recently-acquired cities.
- **Peacetime core infrastructure priority (`AI_chooseProduction`)**: In peaceful, safe, non-military-specialized cities (after all defender, floating-defender, worker, settler, naval, and spy quotas have already run), evaluates `AI_chooseBuilding()` ahead of the unfocused random peacetime unit roll.

### 2. Tile development, Great People EV math, Tech-for-Gold & Food Corporations (`CvCityAI.cpp`, `CvPlayerAI.cpp`, `CvUnitAI.cpp`)
- **Camp-spam root cause fix (`CvCityAI::AI_bestPlotBuild`)**: Replaced the minimum-`iTime` resource-connector override (which forced `400`-time `BUILD_CAMP` across 21 Camp-eligible resources over `500`-time `Plantation`/`Olive Farm`/`Apple Farm` and tied `Pasture`) with net weighted plot-yield ranking (using the city's exact `iFoodPriority`, `iProductionPriority`, `iCommercePriority`, breaking ties by shorter `iTime`).
- **Full Golden Age valuation (`CvPlayerAI::AI_calculateGoldenAgeValue`)**: Models average city yield/commerce multipliers, **zero-anarchy pending civic swap savings** (`getCivicAnarchyLength` × empire output × `120%` for RevolutionDCM anarchy avoidance), and `+100%` empire GP birth rate via `AIPlaystylePolicy::goldenAgeTotalValue()`.
- **Unified Great Person marginal EV math (`CvUnitAI::AI_scientistMove`, `AI_engineerMove`, `AI_generalMove`)**:
  - Great Scientists compare real marginal single-city `Academy` NPV (`AIPlaystylePolicy::academyConstructNpv`) against per-unit Golden Age value and Bulb value (while preserving Corporation HQ founding priority), stopping large empires from building low-ROI Academies or settling scientists ahead of Golden Ages/Bulbs.
  - Great Engineers discount wonder hurrying via `AIPlaystylePolicy::engineerWonderHurryDiscountPct()` when `HURRY_GOLD` + treasury can finish the wonder or it finishes in `<= 4` turns, preserving GEs for Golden Ages, `Iron Works`/`Pont du Gard`/Corp HQs, or contested wonders.
  - Non-operational Great Generals prioritize `AI_construct(2)` / `AI_construct(4)` (`Military Academy`, `Courier System`, `Secret Army Base`) ahead of routine specialist settling.
- **Affordable tangential tech-for-gold sales (`CvPlayerAI::AI_doDiplo`)**: Replaced max-`AI_techTradeVal` single-tech selection (which aborted whenever a buyer lacked cash for the priciest tech) with `AIPlaystylePolicy::tangentialTechSaleScore()`, preferring affordable non-military/non-wonder techs while refusing military unlocks to border threats, higher-rank rivals, or war targets.
- **Food Corporation weighting (`CvPlayerAI::AI_corporationValue`)**: Scales `YIELD_FOOD` weight (`90–170` vs `100` Production) via `AIPlaystylePolicy::foodCorporationYieldWeight()` based on city happy/health headroom.

### 3. Land XML `iAirRange` combat, Collateral Cavalry ordering, Unit ROI & Coastal Defense (`CvPlayerAI.cpp`, `CvCityAI.cpp`, `CvUnitAI.cpp`, `CvSelectionGroup.cpp`)
- **Land XML ranged & trait valuation (`CvPlayerAI::AI_unitValue`)**: Scores all 46 land `iAirRange >= 1` units via `AIPlaystylePolicy::landRangedUnitValueBonus()` (`Archer`, `Longbowman` `airLim=90`, `Crossbowman`, `Horse Archer` `airLim=75, collat=25`, `Catapult`, `Artillery` `airRng=2`), plus `isEnemyRoute()` and `isAlwaysHeal()` free promotions (Roman legions), hills/feature chokepoint defense specialists, and unique Warlord/Centurion squad-leader units.
- **Group-wide true-`airRange` ranged targeting (`CvUnitAI::AI_rangeAttack`)**: Replaced head-unit-only `canRangeStrike()` and broken melee `AI_attackOdds()` targeting with stack-wide `scoreGroupRangeStrikePlot()` -> `AIPlaystylePolicy::rangeTargetScore()`, summing actual capped primary damage (`airCombatLimit() - damage`) plus collateral splash over true group `airRange()` (returning `0` on already-capped targets).
- **Combined-arms 3-phase execution (`CvSelectionGroup::groupAttack`, `CvUnitAI::AI_attackCityMove`, `AI_collateralMove`, `AI_update`)**:
  - **Phase 1 (Zero-Risk Ranged Volleys)**: Fires every ready land `canRangeStrikeAt()` unit in an attacking stack inside `CvSelectionGroup::groupAttack()`, before bombardment/assault forecasting in `AI_attackCityMove()`, before dead DCM calls in `AI_collateralMove()`, and defensively from owned cities and defensive/fortified-chokepoint positions in `AI_update()` (guarding non-defensive unit AIs on terrain behind `getFortifyTurns() > 0` so marching siege stacks do not stall).
  - **Phase 2 (Collateral Cavalry / Siege Priority)**: `LFBgetBetterAttacker()` adds `AIPlaystylePolicy::collateralAttackPriorityBonus()` so collateral cavalry (`Horse Archer`, `Light Cavalry`, `Chariot`) and siege strike before melee finishers against multi-unit healthy stacks.
  - **Circumstantial 2-Move Skirmish (`RANGED_ATTACKS_USE_MOVES = 0`)**: Independent 2-move ranged units (never in mixed stacks, never abandoning cities/Settlers/Workers) can step 1 tile into safe firing range and shoot (`trySkirmishStepAndShoot`) and step back 1 tile after firing only to a strictly safer plot (`trySkirmishRetreatAfterShot`).
- **Unit turn-time ROI & Coastal Defense (`CvCityAI::AI_bestUnitAI`, `AI_neededDefenders`)**: Applies `AIPlaystylePolicy::unitTurnTimeDivisor()` (steepening above 5 turns, and applied under Slavery whip too) so slow expensive units concentrate in fast hammer cities; scales coastal city garrisons via `AIPlaystylePolicy::coastalNavalThreatDefenders()` when hostile/war-planning navies share `waterArea()`.

### 4. Espionage/RevDCM slider floors, Spy AI, Luxury Bundles & Upgrade Reserves (`CvPlayerAI.cpp`)
- **Solvent Espionage & Era 1+ RevDCM Research floors (`AI_doCommerce`)**: Enforces `AIPlaystylePolicy::espionageFloorPercent()` (`5–10%` aligned to slider increments once Espionage is active in Era 1+, not zeroed vs Pleased/Friendly rivals and not stripped for `HURRY_GOLD`), and enforces an Era 1+ RevolutionDCM `>= 50%` research floor via `revDcmResearchFloorPercent()` (only shifting from `COMMERCE_GOLD` so Culture/Espionage are never disturbed).
- **Proactive Spy AI (`AI_bestPlotEspionage`)**: Triggers Counter-Espionage when a rival holds `>= 125%` of our accumulated EPs (`>= 100` EP) and wires up `Switch Civic` (`getSwitchCivicCostFactor() > 0`) for hostile/war targets or civs blocking our state-religion spread when we own its Holy City.
- **Luxury reservation & Mixed `Resource + GPT` imports (`AI_resourceReservationVal`, `AI_doDiplo`)**: Extends the `50%` surplus-sharing floor to XML building yield-multiplier luxuries (`Coffee`, `Tea`, `Gold`, `Silver`, etc.) and adds mixed `Spare Resource + GPT` import offers when a pure 1-for-1 swap has a value gap.
- **Urgent upgrade reserve before `AI_doGoldHurry()`**: Reserves frontline obsolete-unit upgrade cash (`AIPlaystylePolicy::urgentUpgradeReserve()`) in `AI_doGoldHurry()` before spending treasury ahead of `AI_doTurnUnitsPost()`.

## Save compatibility

Zero changes to any `::read` or `::write` serialization method and zero public header ABI changes.
Save format and DLL export table (`2,452` exports) are 100% compatible with `c08a472`, `f0d5629`,
`0fabccd`, and `546d223`.

## Checks

### Release DLL build
`toolchain/build_dll.sh` (Visual C++ Toolkit 2003 under Wine, release target):
**0 errors, 0 warnings**.

| property | value |
|---|---|
| size | `6,205,440` bytes |
| SHA-256 | `f97f98b154beaffb0c8b1cc43c5d947e4197d0cf7cfd7ed64cd40071abc80913` |
| exports | `2,452` names (identical to `c08a472`, `f0d5629`, `0fabccd`, and `546d223`) |

### Static analysis (`clang-gate`)
`toolchain/clang-gate/diffcheck.sh` across all 4 modified `.cpp` files (`CvCityAI.cpp`, `CvPlayerAI.cpp`,
`CvUnitAI.cpp`, `CvSelectionGroup.cpp`) against `546d223`:
**0 new errors, 0 new warnings** (`baseline: 1 errors/0 warnings; patched: 1 errors/0 warnings; new: 0`).

### Native C++98 unit tests & patch round-trip
- [`tests/test_playstyle_pass9.cpp`](tests/test_playstyle_pass9.cpp) compiled with
  `g++ -Wall -Wextra -Werror -std=c++98 -I<rom>/Assets/CvGameCoreDLL`: **ALL PASSED** (covering all
  13 functions in `AIPlaystylePolicy.h` including 0-route projections, Golden Age anarchy-skip &
  Academy NPV crossovers, Engineer gold-hurry discounts, tangential tech sales, ranged damage target
  scoring, collateral cavalry attack priority, safe 2-move skirmish guards, turn-time ROI,
  Espionage/RevDCM floors, urgent upgrade reserves, and coastal naval threats).
- `git am --keep-cr playstyle-ai-pass9.patch` over `546d223`: byte-for-byte identical across
  `Assets/CvGameCoreDLL`.

### Open checks
- **Full seeded harness battery (`P19`)**: `method/mission/evidence/P19/` is open (`n >= 5` paired seeded runs).
- **In-game Civ4 executable verification**: live tactical ranged-volley + collateral cavalry + skirmish behavior, Camp-to-Pasture/Plantation tile development, and Espionage/RevDCM slider stability.
