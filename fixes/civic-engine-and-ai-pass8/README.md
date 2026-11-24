# Civic engine, Python/XML, and AI semantic bug fixes (Pass 8 over `0fabccd`)

[`../civic-engine-and-ai-pass8.patch`](../civic-engine-and-ai-pass8.patch) applies cleanly on top of
Passes 3–7 ([`../ai-transformation.patch`](../ai-transformation.patch), commit `0fabccd`).
It serves prediction `P18` (`method/mission/register.json`, hypothesis `H13`).

## Applying on Windows (CRLF)

Because RoM's C++ and XML files use CRLF line endings, preserve CR bytes when applying with `git am`:

```sh
git am --keep-cr civic-engine-and-ai-pass8.patch
```

(Or apply directly to the working tree with `git apply civic-engine-and-ai-pass8.patch`.)

## What it fixes (objective bugs only — zero speculative tuning)

### 1. Engine crash, stall & arithmetic bugs (`AICivicPolicy.h`, `CvPlot.cpp`, `CvUnit.cpp`, `CvPlayer.cpp`)
- **Fractional `iImprovementUpgradeRateModifier` truncation (`AICivicPolicy.h`, `CvPlot.cpp`)**:
  - Previously, `CvPlayer::getImprovementUpgradeRate()` computed integer `(1 * std::max(0, 100 + mod)) / 100`, silently truncating **12 of 13** upgrade-rate civics (`Barter +10%`, `Colonial +10%`, `Double-Entry +10%`, `Precious Metals +15%`, `Coinage +20%`, `Protectionism +20%`, `Assembly +25%`, `Digital +25%`, `National Socialism +30%`, `Regulated +30%`, `Peasantry +50%`, `Guilds +50%`) to `0%` real speedup unless stacked to `>= +100%`.
  - Replaced with exploit-free **plot-progress lattice snapping** (`AICivicPolicy::improvementUpgradeStep()` and exact O(1) `improvementUpgradeTurnsLeft()`): for all `r = 100 + mod >= 100`, advances each plot strictly along its own worked-turn lattice `p_k = floor(k * r / 100)` via `k(p) = floor((100 * (p + 1) - 1) / r)`. Eliminates both turn-parity micro-exploits and UI hover flicker while preserving exact `short m_iUpgradeProgress` save-format compatibility and snapping mid-upgrade/legacy off-lattice values conservatively. Falls back cleanly to turn-keyed Bresenham for hypothetical modded negative modifiers (`0 < r < 100`).
  - Added an `isOwned()` guard in `CvPlot::doImprovementUpgrade()` to prevent `GET_PLAYER(NO_PLAYER)` on `bOutsideBorders` upgrades (`IMPROVEMENT_MINE -> IMPROVEMENT_SHAFT_MINE`).
- **Live `NO_UNIT` out-of-bounds read & worker-speed zero-stall (`CvPlayer.cpp`, `CvUnit.cpp`, `AICivicPolicy.h`)**:
  - Guarded `const UnitTypes eUnit = (UnitTypes)kCiv.getCivilizationUnits(iI); if (eUnit == NO_UNIT) continue;` in `CvPlayer::getWorkRate(BuildTypes)` (fixes live out-of-bounds `GC.getUnitInfo((UnitTypes)-1)` reads across 173 `<UnitType>NONE</UnitType>` entries in `CIV4CivilizationInfos.xml`).
  - Floored stacked negative worker-speed modifiers at `10%` (and at least `1` work unit when base rate `> 0`) via `AICivicPolicy::scaledWorkRate()` in `CvUnit::workRate()` and `CvPlayer::getWorkRate()`, preventing permanent `0` progress/turn worker freeze.
- **`CvPlayer::setInquisitionConditions()` guard & reset (`CvPlayer.cpp`)**:
  - Guarded `NO_CIVIC` before `GC.getCivicInfo(eCivic)` and explicitly cleared `m_bInquisitionConditions = false` before returning on `isDisallowInquisitions()`.

### 2. Python & modular XML fixes (`RevCivicsUtils.py`, `Guilds_CIV4CivicInfos.xml`, `Guilds_CIV4GameInfoSchema.xml`)
- **`RevCivicsUtils.py` first-match shadowing**:
  - Replaced first-match return loops in `getReligiousFreedom`, `getDemocracyLevel`, `getLaborFreedom`, and `getEnvironmentalProtection` with `_getPrimaryCivicMetric()`, selecting the civic category with the largest count of non-zero civics for that metric (preventing `Priesthood` in `Leadership` from shadowing the entire `Religion` category and `Planned Allocation` in `Taxation` from shadowing `Employment`), and ensured `initCivicsList()` runs inside all four `getBest*` helpers.
- **`Guilds` unread XML tag (`Guilds_CIV4CivicInfos.xml`, `Guilds_CIV4GameInfoSchema.xml`)**:
  - Added optional `iRevIdxDistanceModifier` to `Guilds_CIV4GameInfoSchema.xml` and changed `<fRevIdxDistanceMod>0.05</fRevIdxDistanceMod>` to `<iRevIdxDistanceModifier>5</iRevIdxDistanceModifier>` so `CvCivicInfo::read()` actually loads it.

### 3. Objective `CvPlayerAI` code-vs-engine bug fixes (`CvPlayerAI.cpp`)
- **World/Team Wonders & unbuildable buildings scored per-city (`AI_civicValue`)**: Replaced `!isNationalWonderClass()` with `!isLimitedWonderClass()` and required civ/tech/religion availability for unbuilt regular buildings before adding `(iTempValue * getNumCities()) / 2`, eliminating phantom per-city wonder happiness (`Senate`, `Forum Romanum`, `Pyramids`, `Stonehenge`, `Oracle`, etc.) and non-Hellenic `Hellenic Monastery` inflation.
- **Cross-slot state-religion evaluation & `Occult` full-religion count (`AI_civicValue`, `AI_RevCalcCivicRelEffect`)**:
  - Evaluated a candidate civic's own state-religion modifiers (`Priesthood`'s `+25%` building production, `NoNonStateReligionSpread`, and `RevIdx` religion mods) whenever either the civic itself or another active civic slot enables state religion.
  - Counted all city religions (not `total - highest`) for `getNonStateReligionHappiness()` when a civic forces `No State Religion` (`Occult`), matching `CvCity::getReligionHappiness()`.
- **`GAMEOPTION_NO_REVOLUTION` guard (`AI_RevCalcCivicRelEffect`)**: Returned `0` immediately when `GAMEOPTION_NO_REVOLUTION` is active.
- **Fractional `_MOD_FRACTRADE` profit & 0-route trade civic floor (`AI_civicValue`)**: Accumulated `calculateTradeProfitTimes100(pPartner)` before dividing by `100` (matching `CvCity::updateTradeRoutes`), and used a conservative `1` base profit estimate when `iActiveTradeRoutes == 0` so `iTradeRoutes` (`+1/+2` TR) is not zeroed out under `INITIAL_TRADE_ROUTES = 0`.
- **`FavoriteCivic` negative-score sign flip (`AI_civicValue`)**: Guarded `iValue *= 5; iValue /= 4;` behind `if (iValue > 0)` so negative civic scores are not amplified further negative.
- **Dead anarchy threshold branch (`AI_doCivics`)**: Removed the unreachable `if (getAnarchyTurns() > 0 && !isGoldenAge())` block (already guarded by `canRevolution(NULL)`).
- **`Militia` `isMilitaryFoodProduction` distortion (`AI_civicValue`)**: Summed only positive `foodDifference(false)` and scored proportionally (`bWarPlan ? iTempValue / 2 : iTempValue / 10`), removing the bogus `-Food/4` peace penalty and `3x` war blowup.

## Save compatibility

Zero changes to any `::read` or `::write` serialization method. Save format and DLL export table
(`2,452` exports) are 100% compatible with `c08a472`, `f0d5629`, and `0fabccd`.

## Checks

### Release DLL build
`CLEAN=1 toolchain/build_dll.sh` (Visual C++ Toolkit 2003 under Wine, release target):
**0 errors, 0 warnings**.

| property | value |
|---|---|
| size | `6,189,056` bytes |
| SHA-256 | `66df47e30cd509a447132ba16464cd8d26d67e381258e1b547452d1e829ed129` |
| exports | `2,452` names (identical to `c08a472`, `f0d5629`, and `0fabccd`) |

### Static analysis (`clang-gate`)
`toolchain/clang-gate/diffcheck.sh` across all 4 modified `.cpp` files (`CvPlot.cpp`, `CvPlayer.cpp`,
`CvUnit.cpp`, `CvPlayerAI.cpp`) against `0fabccd`:
**0 new errors, 0 new warnings** (`baseline: 12 errors/68 warnings; patched: 12 errors/68 warnings; new: 0`).

### Native C++98, Python & XML unit tests
- [`tests/test_civic_pass8.cpp`](tests/test_civic_pass8.cpp) compiled with
  `g++ -Wall -Wextra -Werror -std=c++98 -I<rom>/Assets/CvGameCoreDLL`: **ALL PASSED** (exhaustive
  lattice simulation across `0%..+250%` step `5%` × 10 upgrade targets × all starting progress values
  `p0 in [0, T-1]` verifying 0 mismatches, 0 monotonicity errors, zero turn-parity exploit, zero UI
  flicker, negative-modifier fallback, and `scaledWorkRate` 10% floor).
- Python syntax & real-XML `RevCivicsUtils` primary-category tests (`Priesthood` + `Folklore`/`Fanaticism`,
  `Planned Allocation` + `Qualified Labor`, `Patrician` + `Pastoral`, `Imperium` + `No Taxes`,
  `Assembly` + `No Taxes`) and `Guilds` XML/schema parse check: **ALL PASSED**.

### Open checks
- **Full seeded harness battery (`P18`)**: `method/mission/evidence/P18/` is open (`n >= 5` paired seeded runs).
- **In-game Civ4 executable verification**: live UI tooltip & fractional cottage/mine/latifundium upgrade verification, `Guilds` XML load, and RevolutionDCM civic demand checks.
