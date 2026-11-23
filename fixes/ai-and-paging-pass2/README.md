# Post-merge AI strength, overflow, and graphics paging fixes (pass 2 over `c08a472`)

[`../ai-and-paging-pass2.patch`](../ai-and-paging-pass2.patch) applies cleanly to GitLab
`main` at `c08a472` (after the merge of `fix/paging-diplomacy-8587217`). It serves prediction
`P16` (`method/mission/register.json`, hypothesis `H11`).

## Applying on Windows (CRLF)

Because RoM's C++ files use CRLF line endings, preserve CR bytes when applying with `git am`:

```sh
git am --keep-cr ai-and-paging-pass2.patch
```

(Or apply directly to the working tree with `git apply ai-and-paging-pass2.patch`.)

## What it fixes

### 1. Diplomacy & resource valuation (Designs A1, 2A, 4C, 5A, G1)
- **`AIDiplomacyPolicy.h`**: Added C++98 64-bit helpers `scaleByRatio64`, `powerRatioPercent`,
  `isWeightedGreater`, and `resourceReservationVal`.
- **`CvPlayerAI.h` / `CvPlayerAI.cpp`**:
  - **Design A1 (closes 1-GPT spare-resource exploit & creation/cancellation mismatch):**
    Added `AI_resourceReservationVal` and `AI_tradeReservationVal` applying a unified
    surplus-sharing bargaining floor (`40%` at deal creation, `50%` for strategic military
    resources to non-friendly/non-vassal buyers, `50%` midpoint ask in `AI_counterPropose`,
    and `30%` at 20-turn renewal with `iChange = +1` regain valuation, `AI_goldPerTurnCostVal`,
    and 64-bit 10% hysteresis). Extended AI–AI standing deal review so financially strained AIs
    cancel unsustainable outgoing `TRADE_GOLD_PER_TURN` deals.
  - **Design 2A:** Scoped `AI_maxGoldPerTurnTrade`'s `calculateGoldRate()` clamp to the AI
    `else` branch so humans running deficit research can offer GPT normally.
  - **Design 4C:** Required positive `AI_mapTradeVal` on at least one side and applied
    `CONTACT_TRADE_MAP` cooldown to AI–AI map swaps, eliminating consecutive-turn zero-value
    map-trade spam.
  - **Design 5A:** Added `AI_corporationBonusVal == 0` guard and midpoint spare-resource offer
    weight on `pOurInventory` `TRADE_RESOURCES` in `AI_counterPropose`, and replaced the last
    32-bit gold gap math in `AI_doDiplo` tech trades with `AIDiplomacyPolicy::goldForValueGap`.
  - **Design G1:** Added imminent growth-cap happiness and health headroom (`50%` at surplus `0`,
    `25%` at surplus `+1`) in `AI_bonusCityValue`.

### 2. Late-game power overflows, economy, civics, bombard, Revolution AI & state religion (Designs B1, C1, D1, E2, F1, 6A)
- **Design B1 (`CvTeamAI.cpp`, `CvPlayerAI.cpp`, `CvCityAI.cpp`):** Converted 10+ 32-bit
  team/player power multiplications and comparisons to 64-bit across `AI_getEnemyPowerPercent`,
  `AI_declareWarTradeVal`, `AI_surrenderTrade`, `AI_endWarVal`, `AI_startWarVal`,
  `AI_minorKeepWarVal`, `AI_getBarbarianCivWarVal`, `AI_conquerCity`,
  `AI_doVictoryStrategies`, and `AI_cityThreat`.
- **Design C1 (`CvPlayerAI.cpp` `AI_doCommerce`):** Stopped raising `COMMERCE_RESEARCH` once
  `COMMERCE_GOLD` hits `0%` so it no longer erases the AI's anti-unhappiness `COMMERCE_CULTURE`
  slider; added a solvency guard on the `0% -> 10%` research bump; replaced `new[]` +
  `SAFE_DELETE` heap UB with stack arrays `aiTarget[MAX_CIV_TEAMS]` / `aiWeight[MAX_CIV_TEAMS]`.
- **Design D1 (`CvPlayerAI.cpp` `AI_civicValue`):** Fixed Inquisition civic typo
  (`iValue /= 5;` -> `iValue += iNonstateReligionCount * 4;`).
- **Design E2 (`CvUnitAI.cpp`):** Moved `if (pBestPlot != NULL)` outside the `iDX` loop in
  `AI_RbombardNaval`, removed the zero-multiplying `getSorenRandNum(20)` / `getSorenRandNum(5)`
  factors for deterministic focus fire, and guarded `pDefender != NULL` in `AI_Abombard`.
- **Design F1 (`CvCityAI.cpp` `AI_buildingValueThreshold`):** Added Revolution-index-scaled
  scoring for `getRevIdxLocal()`, `getRevIdxNational()`, and `getRevIdxDistanceModifier()`
  guarded by `!GC.getGameINLINE().isOption(GAMEOPTION_NO_REVOLUTION)`.
- **Design 6A (`CvPlayer.cpp`):** Fixed `=` assignment typos (`eStateReligion == NO_RELIGION`)
  in `hasStateReligionHolyCity()` and `hasStateReligionShrine()`.

### 3. Graphics paging priority, critical shrink, route reveal drain & entity sync (Designs 3A, 4A, 7B)
- **Design 3A (`CvGame.h`, `CvGame.cpp`):**
  - Replaced south-to-north plot scanning in `CvGame::pageGraphics(false)` with center-out
    Chebyshev rings around `(m_iPagingX, m_iPagingY)` for page-in and a non-serialized
    round-robin cursor `m_iPagingOutCursor` for budgeted page-out.
  - Checked live camera movement and critical pressure before the `m_bPagingPending` and
    100 ms throttle early-returns in `CvGame::updateGraphicsPaging()`.
  - Bypassed `GRAPHICS_PAGING_SHRINK_MS` under critical memory pressure (`m_iGraphicsMemoryPressure == 2`)
    so emergency eviction fires immediately.
- **Design 4A (`CvPlot.h`, `CvPlot.cpp`, `CvGame.cpp`):** Added `CvPlot::refreshRevealedRouteOnly()`
  and drained off-window `m_bRevealedRouteDirty` plots within the remaining
  `GRAPHICS_PAGING_REVEAL_MAX` budget in `CvGame::processDeferredReveals` whenever visible
  camera paging is idle.
- **Design 7B (`CvCity.cpp`, `CvUnit.cpp`):** Aligned `CvCity::pageGraphics(true)` to clear
  `m_bGraphicsPagedOut = false` after `CvDLLEntity::setup()` (matching `CvUnit::pageGraphics(true)`),
  and reconciled unit position and plot flag (`SetPosition(plot()); plot()->setFlagDirty(true);`)
  immediately after setup in `CvUnit::pageGraphics(true)`.

## Save compatibility

Zero changes to any `::read` or `::write` method; `m_iPagingOutCursor` is transient graphics
state matching the rest of `CvGame`'s non-saved paging fields. Save format and DLL export table
are 100% compatible with `c08a472`.

## Checks

### Release DLL build
`CLEAN=1 toolchain/build_dll.sh` (Visual C++ Toolkit 2003 under Wine, release target):
**0 errors, 0 warnings**.

| property | value |
|---|---|
| size | `6,172,672` bytes |
| SHA-256 | `af49620d7c6419351c268abe6b4eebe9c52ff37e856abcda1645835142c26f38` |
| exports | `2,452` names (identical to `c08a472`) |

### Static analysis (`clang-gate`)
`toolchain/clang-gate/check.sh` on mirrored + forscope-processed sources across all 9 modified
`.cpp` files: **0 errors, 0 warnings** on all changed lines.

### Native C++98 unit tests
[`tests/test_ai_diplomacy_pass2.cpp`](tests/test_ai_diplomacy_pass2.cpp) compiled with
`g++ -Wall -Wextra -Werror -std=c++98 -I<rom>/Assets/CvGameCoreDLL`: **ALL PASSED** (covers
1-GPT exploit rejection, 40%/50%/30% reservation floor & hysteresis consistency, pillaged-supply
cancellation, and 64-bit power arithmetic up to `700,000,000`).

### Headless harness A/B smoke check (`p15.scn`, seed `1570079469`, 300 turns, graphics paging on)
With `HARNESS_GRAPHICS=1 HARNESS_ACTIVE=0 HARNESS_CAMERA_FOLLOW=1`, the patched DLL completed
all 300 turns cleanly (`RESULT scenario turn 300 state 0`):
- on-screen bare units: dropped from `17` (`c08a472`) to **`0`**;
- on-screen bare cities: dropped from `45` (`c08a472`) to **`0`**;
- missing route symbols: converged to **`0` new** within 2 turns of the turn-260 map trade
  (transient cumulative `88` vs. persistent `709` across 9+ turns on `c08a472`);
- entity churn: `entities created` dropped from `13,826` to **`2,808`** (`setup` calls
  `11,387` -> **`2,793`**);
- AI–AI map trades: dropped from `8` (including consecutive-turn repeats) to **`2`**.

### Open checks
- **Full seeded harness battery (`P16`)**: `method/mission/evidence/P16/` is open (`n >= 5`
  paired seeded runs).
- **In-game Civ4 executable verification**: live human trade-screen tests (1-GPT rejection,
  human GPT under deficit research) and camera panning/OOM stress testing in `Civ4BeyondSword.exe`.
