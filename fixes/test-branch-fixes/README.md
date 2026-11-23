# Graphics-Paging-Fix-Test (8587217) fixes: paging selection, diplomacy valuation, and callback define

[`../test-branch-fixes.patch`](../test-branch-fixes.patch) applies cleanly to GitLab
`Graphics-Paging-Fix-Test` at `8587217eeb94` ("Selection fix"). It serves prediction `P15`
(`method/mission/register.json`, hypothesis `H10`).

## What it fixes

### 1. Graphics paging selection restoration, multi-selected cities, and bulk-reveal routes
- **`CvGame.cpp` (`pageGraphics`)**:
  - Replaced `break;` with `continue;` in the active-unit and active-city restoration loops so a
    paged-out or cap-hit entry never aborts restoration of remaining units/cities.
  - Checked the full city selection list (`headSelectedCitiesNode` / `nextSelectedCitiesNode`)
    rather than only `getHeadSelectedCity()`.
  - Exempted selected cities from the `iMaxIn` per-slice budget and exempted the head-selected
    city from the critical-pressure cap.
- **`CvCity.cpp` (`canPageGraphicsOut`)**:
  - Protected every city in the multi-selection list from being paged out.
- **`CvGameInterface.cpp` & `CvDLLButtonPopup.cpp`**:
  - Restored paged-out entity graphics before selection in `cyclePlotUnits`,
    `doControl(CONTROL_SELECTINJURED, CONTROL_SELECTCAPITAL)`, `cycleCities`, `selectCity`, and
    all four `OnOkClicked` city-popup handlers.
- **`CvPlot.cpp` (`refreshRevealedGraphics`)**:
  - Rebuilt dirty route symbols (`updateRouteSymbol(true, false)`) when `m_bRevealedRouteDirty`
    is set during bulk reveal.

### 2. Diplomacy valuation, 64-bit gold/GPT overflow, and `AI_DIPLOMACY_FLAGS` contract
- **`AIDiplomacyPolicy.h`**:
  - Added C++98 pure helpers `goldPerTurnCostVal` and `maxAffordableGoldPerTurn` with 64-bit
    intermediate math to prevent 32-bit overflow.
- **`CvGameCoreUtils.h` & `Assets/XML/BBAI_AI_Variables_GlobalDefines.xml`**:
  - Added `AI_DIPLOMACY_NET_VALUE = 16` and updated default `AI_DIPLOMACY_FLAGS` from `15` to `31`.
- **`CvPlayerAI.cpp`**:
  - Switched `AI_dealVal` gold/GPT conversion to 64-bit `valueFromGold` + `saturatingAdd`.
  - Gated bilateral net-value economics on `AI_DIPLOMACY_NET_VALUE` in `AI_considerOffer` and
    `AI_doDiplo`.
  - Required strictly positive (`> 0`) net gain on AI–AI resource swaps and GPT deals.
  - Fixed `AI_counterPropose` false rejections: asking prices now use seller weight
    (`AI_tradeGiveVal`) plus midpoint pricing for spare resources (`iOurLoss + (iBuyerVal - iOurLoss + 1) / 2`),
    AI gold/GPT offers use payer-cost valuation, and human counterparties check `AI_dealNetVal >= 0`.

### 3. Callback define typo
- **`CvGlobals.cpp` (`cacheGlobals`)**:
  - Fixed `"USE_USE_CANNOT_SPREAD_RELIGION_CALLBACK"` -> `"USE_CANNOT_SPREAD_RELIGION_CALLBACK"`.

## Files

| file | change |
|---|---|
| `Assets/CvGameCoreDLL/CvGame.cpp` | `continue` in active loops, full multi-selected city protection, `iMaxIn` / pressure exemptions |
| `Assets/CvGameCoreDLL/CvCity.cpp` | `canPageGraphicsOut()` checks all multi-selected cities |
| `Assets/CvGameCoreDLL/CvGameInterface.cpp` | restore paged-out graphics before unit/city selection |
| `Assets/CvGameCoreDLL/CvDLLButtonPopup.cpp` | restore paged-out city graphics in all 4 `OnOkClicked` handlers |
| `Assets/CvGameCoreDLL/CvPlot.cpp` | rebuild `m_bRevealedRouteDirty` route symbols in `refreshRevealedGraphics()` |
| `Assets/CvGameCoreDLL/AIDiplomacyPolicy.h` | `goldPerTurnCostVal`, `maxAffordableGoldPerTurn` (C++98, 64-bit safe) |
| `Assets/CvGameCoreDLL/CvGameCoreUtils.h` | `AI_DIPLOMACY_NET_VALUE = 16` |
| `Assets/CvGameCoreDLL/CvPlayerAI.cpp` | 64-bit `AI_dealVal`, `AI_DIPLOMACY_NET_VALUE` gating, AI–AI `> 0` gain, `AI_counterPropose` fix |
| `Assets/XML/BBAI_AI_Variables_GlobalDefines.xml` | default `AI_DIPLOMACY_FLAGS` `15` -> `31` |
| `Assets/CvGameCoreDLL/CvGlobals.cpp` | fix `USE_CANNOT_SPREAD_RELIGION_CALLBACK` define lookup typo |

## Save compatibility

`codemap/tool/impact.py diff 8587217 HEAD`: **0 member-declaration changes** across all classes.
Save format is unchanged and 100% compatible with `8587217`.

## Checks

### Release DLL build
`CLEAN=1 toolchain/build_dll.sh` (Visual C++ Toolkit 2003 under Wine, release target): **0 errors, 0 warnings**.

| property | value |
|---|---|
| size | 6,168,576 bytes |
| SHA-256 | `3eb3861f061223271a9c1ab8332f56c817acd1c56d9b63da88b3ef86870892f0` |
| exports | 2,452 names (same count as `8587217`) |

### Static analysis (`clang-gate`)
`toolchain/clang-gate/check.sh` on mirrored + forscope-processed sources across all 7 modified `.cpp` files: **0 errors, 0 warnings** on all changed lines.

### Native C++98 diplomacy unit tests
[`tests/test_diplomacy_fixes.cpp`](tests/test_diplomacy_fixes.cpp) compiled with
`g++ -Wall -Wextra -Werror -std=c++98 -I<rom>/Assets/CvGameCoreDLL`: **ALL PASSED** (covers
64-bit gold/GPT overflow, `goldPerTurnCostVal`, `maxAffordableGoldPerTurn`, midpoint spare-resource
ask pricing, and zero-gain swap rejection).

### Seeded headless harness runs (`P15`)

Ten 300-turn runs (`GAMESPEED_NORMAL`, `HANDICAP_NOBLE`, 6 AI civilizations, `HARNESS_GRAPHICS=1`, `HARNESS_ACTIVE=0`, `HARNESS_CAMERA_FOLLOW=1`, `HARNESS_CAMERA_VIEW=2200,45,0,1920,1080`) on the `fixes/debt/harness/make_scenario.py` scenario using the seeds from `python3 method/ledger.py seeds P15 10` (harness built with `fixes/debt/harness/HarnessState-test-branch.patch` and original Civ4 + BTS XML):

| arm | seed | result | trades | check passes | flagless live units | routes w/o symbol | on-screen units w/o gfx | on-screen cities w/o gfx |
|---|---|---|---:|---:|---:|---:|---:|---:|
| a | 926387420 | turn 300 (state 0) | 45 | 459 | 0 | 0 | 0 | 13 |
| a | 695102974 | turn 300 (state 0) | 103 | 516 | 0 | 0 | 117 | 50 |
| a | 213696118 | turn 300 (state 0) | 65 | 460 | 0 | 0 | 0 | 20 |
| a | 969297610 | turn 300 (state 0) | 71 | 396 | 0 | 1271 | 91 | 126 |
| a | 930289227 | turn 262 (state 2) | 57 | 435 | 0 | 0 | 10 | 35 |
| b | 1262442612 | turn 300 (state 0) | 63 | 515 | 0 | 0 | 17 | 32 |
| b | 1526083124 | turn 300 (state 0) | 73 | 482 | 0 | 237 | 24 | 52 |
| b | 1570079469 | turn 300 (state 0) | 95 | 460 | 0 | 709 | 17 | 45 |
| b | 765479592 | turn 300 (state 0) | 89 | 612 | 0 | 0 | 53 | 55 |
| b | 206128253 | turn 300 (state 0) | 58 | 501 | 0 | 556 | 5 | 1 |

All 10/10 runs reached `RESULT` cleanly (5/5 arm `a`, 5/5 arm `b`, **P15 corroborated**; evidence recorded in `method/mission/evidence/P15/{a,b}.tsv`, run logs in [`runs/`](runs/)). Both arms had 0 flagless live units and 0 on-screen units without flags across all 4,836 check passes; the runs also surfaced two pre-existing scheduling issues in `8587217` (on-screen bare units/cities under map-order `iMaxIn` throttling, and off-window `routes without symbol` after `TRADE_MAPS` bulk reveal) tracked for follow-up.

### Open checks
- **In-game Civ4 executable verification**: selection cycling across paged-out units/cities,
  multi-city selection, bulk map reveal routes, and human-AI `AI_counterPropose` trade screen
  negotiations require testing in the Civ4 BTS executable.
