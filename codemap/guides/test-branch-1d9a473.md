# The test branch at 1d9a473: the codebase and the newest update

Branch `Graphics-Paging-Fix-Test` on GitLab, head `1d9a473` (2026-11-22, "Memory fixes; Also trade in the
diplomacy screen reworked"), with its parent `69955ed` ("Memory fixes"). The code map in `codemap/map` was
rebuilt from this commit. The DLL built at this commit by the release configuration (MSVC 2003, under Wine)
compiled with 0 errors and 0 warnings; the file is 6,168,576 bytes.

Every statement below comes from one of three sources:
- the map tables, read with `codemap/tool/query.py` and `codemap/tool/impact.py`;
- the source at `1d9a473`, cited as `file:line`;
- `git diff cdda5b6 1d9a473`.

Each part describes first. Readings are marked **Reading**: each names the facts it rests on and what would
contradict it.

## 1. The codebase as the map sees it

**Size** (`codemap/skeleton.md`, generated from `map/`):
- 176 source files with functions, and 13,351 compiled functions.
- 150,598 direct calls, 17,646 virtual calls, and 4,325 places that take a function's address.
- 333 classes; 3,676 member variables (`map/fields.tsv`).
- 3,892 functions bound for Python, 183 places where C++ calls Python, and 81 events posted to Python.
- 278 Python modules.
- XML elements in `map/xml_tags.tsv` (mod, BTS and Civ4 layers): 8,788 rows.

**Where control comes from.** `query.py rank` lists the functions that every call path from outside the DLL
must pass through, and how many functions each one dominates. The largest are:

| function | dominates | where |
|---|---|---|
| `CvGame::update` | 375 | CvGame.cpp:2175 |
| `CvGame::updateMoves` → `CvPlayerAI::AI_unitUpdate` → `CvSelectionGroupAI::AI_update` → `CvUnitAI::AI_update` | 280 / 278 / 269 / 250 | CvGame.cpp:8106 … CvUnitAI.cpp:195 |
| `CvXMLLoadUtility::LoadPreMenuGlobals` | 334 | CvXMLLoadUtilitySet.cpp:768 |
| `CvPlayer::setTurnActive` → `CvPlayer::doTurn` | 164 / 131 | CvPlayer.cpp:12160, 3918 |
| `CvXMLLoadUtility::LoadPostMenuGlobals` | 150 | CvXMLLoadUtilitySet.cpp:949 |
| `CvDLLWidgetData::parseHelp` | 137 | CvDLLWidgetData.cpp:53 |
| `CvGame::doTurn` | 72 | CvGame.cpp:6804 |
| `CvPlayerAI::write` / `CvPlayerAI::read` | 51 / 48 | CvPlayerAI.cpp:19572, 19316 |

The DLL has four main entry trunks:
- the per-frame update, which mostly moves units;
- the per-turn update of each player and city;
- XML loading;
- the interface's help text.

Diplomacy has no trunk of its own:
- `CvPlayerAI::AI_doDiplo` (CvPlayerAI.cpp:17345–19308, about 1,960 lines) is reached from `AI_doTurnPost`.
- The trade screen's calls arrive from the exe, through exported functions and the `CvPlayer` vtable
  (part 3 of `diplomacy-screen-and-civics.md`).

## 2. What the update changed

The diff covers eight files:
- `CvCity.cpp`, `CvGame.cpp`, `CvGame.h`, `CvPlayerAI.cpp`, `CvPlayerAI.h`, `CvPlot.cpp`, `CvUnit.cpp`
  and `GlobalDefinesAlt.xml`;
- 495 lines added and 68 removed.

The full trace is `codemap/impact/Graphics-Paging-Fix-Test_cdda5b6..1d9a473.md`. The trace from the last merge
to `main` is `codemap/impact/Graphics-Paging-Fix-Test_71de0ab..1d9a473.md`. The change has two unrelated
parts.

### 2a. Graphics memory control

**What it does:**
- **New: `CvGame::updateGraphicsMemoryPressure`** (CvGame.cpp:2416–2506).
  - It reads the process's free virtual address space through `GlobalMemoryStatusEx`, at most once per
    250 ms unless forced.
  - It sets `m_iGraphicsMemoryPressure`: 0 is normal, 1 is conserve, 2 is critical.
  - Thresholds: conserve is `max(GRAPHICS_PAGING_MEMORY_CONSERVE_MB, total/8)`, critical is
    `max(..._CRITICAL_MB, total/16)`, recovery is `max(..._RECOVER_MB, total/4)`.
  - Leaving state 1 needs `GRAPHICS_PAGING_MEMORY_RECOVER_SAMPLES` ordinary samples in a row above the
    recovery mark.
  - A failed query sets the state to 0.
- **`CvGame::pageGraphics`:**
  - Under state 1, page-ins per pass are capped at `GRAPHICS_PAGING_MEMORY_CONSERVE_MAX_IN`.
  - Under state 2, only selected units and cities are paged in, at most `GRAPHICS_PAGING_CRITICAL_SELECTED_IN`.
  - The state is sampled again after every 8 page-ins (CvGame.cpp:2980–2995).
- **`CvGame::endBulkReveal`** processes the queue of revealed plots only under state 0 (CvGame.cpp:2336–2340).
- **Active player's units and cities can now be paged out:**
  - Before, `CvUnit::canPageGraphicsOut` and `CvCity::canPageGraphicsOut` always kept the active player's
    graphics.
  - Now they may page them out, gated by `GRAPHICS_PAGING_ACTIVE_UNITS` (1) and `GRAPHICS_PAGING_ACTIVE_CITIES`
    (0).
  - Kept regardless: the selected unit, the unit at the move target, and the head-selected city
    (CvUnit.cpp:464–480, CvCity.cpp:764–779).

**New defines** (`GlobalDefinesAlt.xml`):

| define | value |
|---|---|
| `MEMORY_CONTROL` | 1 |
| `CONSERVE_MB` | 512 |
| `CRITICAL_MB` | 256 |
| `RECOVER_MB` | 768 |
| `RECOVER_SAMPLES` | 20 |
| `CONSERVE_MAX_IN` | 8 |
| `CRITICAL_SELECTED_IN` | 4 |
| `PRESSURE_RANGE_X` | 12 |
| `PRESSURE_RANGE_NORTH` | 12 |
| `PRESSURE_RANGE_SOUTH` | 8 |
| `ACTIVE_UNITS` | 1 |
| `ACTIVE_CITIES` | 0 |

All have the prefix `GRAPHICS_PAGING_`.

**Changed defines:**

| define | before | after |
|---|---|---|
| `GRAPHICS_PAGING_MARGIN` | 4 | 8 |
| `GRAPHICS_PAGING_MAX_IN` | 100 | 64 |
| `GRAPHICS_PAGING_MAX_OUT` | 100 | 64 |
| `GRAPHICS_PAGING_REVEAL_MAX` | 50 | 25 |

**Can it desynchronise a network game?** The pressure value differs from machine to machine, so the
question is whether it reaches state that every machine must hold equally. The graph answers it in three
steps:

1. **Readers of the pressure** (`map/field_access.tsv`):
   - `updateGraphicsMemoryPressure` itself;
   - `pageGraphics` (six reads);
   - `endBulkReveal` (one read);
   - `updateGraphicsPaging`, through `pageGraphics`.
2. **What those readers write, and what they call:**
   - `pageGraphics` writes `m_bGraphicsPaging`, `m_bPagingPending` and `m_bPagingPendingOut`. It calls
     `CvPlot::pageGraphics`, `CvUnit::pageGraphics`, `CvCity::pageGraphics`, the interface's selection
     getters and the log.
   - `endBulkReveal` writes `m_eBulkRevealTeam` and `m_iBulkRevealDepth`. Both are set before the pressure
     is read; the read only decides whether `processDeferredReveals` runs. It calls
     `CvMap::updateMinimapColor`, the interface's dirty bits and `processDeferredReveals`.
   - `processDeferredReveals` writes only `m_aiDeferredRevealPlots`.
   - The three per-object `pageGraphics` functions write:
     - `CvPlot::m_bGraphicsPagedOut`, `m_bPagedBuilder`, `m_bPagedPlots`, `m_bPagedSymbols` and `m_bPlotLayoutDirty`;
     - `CvDLLEntity::m_bGraphicsPagedOut`.
     - Their callees to depth 3 are symbol, entity and visibility updates. None is a random-number call or an
       AI function.
3. **Whether any of that is game state:**
   - None of the members above is written in `CvGame::write` or `CvPlot::write`.
   - Readers of `m_bGraphicsPagedOut` outside the paging code: `CvPlayer::setCurrentEra` (CvPlayer.cpp:12685),
     `CvPlayer::doWarnings` (18232), `CvUnit::setXY` (CvUnit.cpp:10591, 10601), `setPromotionReady` (12021)
     and `setHasPromotion` (12830).
   - Each of those reads guards only an entity call (`updateGraphicEra`, `updateEnemyGlow`,
     `showPromotionGlow`, `updatePromotionLayers`) or a page-in.

**Reading:** the memory control is presentation-only and does not risk an out-of-sync error.
- *Rests on:* step 3; no random-number call on the reach; nothing written that is saved.
- *Would contradict it:* a reader of one of the written members that the map does not see. Calls from the
  exe are invisible to the map; it sees the DLL's own code only. A sync log comparison from a network game
  with two machines of different free memory would settle it. That test has not been run here: **open**.

**Reading:** `GRAPHICS_PAGING_ACTIVE_UNITS = 1` makes the active player's idle, offscreen units lose their
entities.
- *Rests on:* `CvUnit::canPageGraphicsOut` (CvUnit.cpp:464–480).
- *Would contradict it:* `bPageActiveUnits` (CvGame.cpp:3024, true when the define is above 0) not being used to page out the active player's units.
- *Consequence:* a player who jumps the camera to a far unit through a list (the military advisor, the unit
  cycle) gets that unit's entity after the next paging pass, not at once. Whether this is visible in play is
  **open**: it needs the game.

### 2b. Trade valuation in diplomacy

**What it does.** Four new functions in `CvPlayerAI`:
- **`AI_tradeGiveVal`** (CvPlayerAI.cpp:8914–8944) values what a player gives.
  - It starts from the recipient's `AI_dealVal`.
  - For a resource it uses the giver's own loss (`AI_bonusTradeVal(…, -1)`) instead of the recipient's gain.
  - For gold it uses the giver's gold percent instead of the recipient's.
  - For gold per turn it uses `AI_goldPerTurnCostVal` instead of the recipient's `AI_goldPerTurnTradeVal`.
- **`AI_dealNetVal`** (8946–8952) is what a player receives minus `AI_tradeGiveVal` of what it gives.
- **`AI_isMutuallyBeneficialDeal`** (8954–8961) requires both sides' net value to be at least 0. The other
  side's net is computed by the other player's own `CvPlayerAI` object, including when that player is human.
- **`AI_goldPerTurnCostVal`** (9789–9810) is the payer's cost of a gold-per-turn payment.
  - It starts from the ordinary trade value.
  - A sustainable payment is `max(0, goldRate) + (gold − goldTarget)/PEACE_TREATY_LENGTH`.
  - The share of the payment above that adds up to the same amount again, so the cost is at most twice the
    ordinary one.

Callers (`query.py callers`):

| function | called by |
|---|---|
| `AI_tradeGiveVal` | `AI_considerOffer`, `AI_dealNetVal` |
| `AI_isMutuallyBeneficialDeal` | `AI_counterPropose` |
| `AI_goldPerTurnCostVal` | `AI_doDiplo`, `AI_tradeGiveVal` |

`AI_considerOffer` is also reached from `CvDLLButtonPopup::OnOkClicked` and from the exe through the vtable.
`impact.py func CvPlayerAI::AI_tradeGiveVal` reaches 66 C++ functions, 53 Python functions, and 19
exported functions.

Changed behaviour:
1. **`AI_considerOffer`** (9066–9070): for a new deal (`iChange > -1`), what the AI gives is valued by
   `AI_tradeGiveVal`. Before, it was the recipient's value, raised to at least the AI's own resource loss
   under switch 2. Cancelling an existing deal (`iChange = -1`) keeps the old valuation.
2. **`AI_counterPropose`:**
   - The gold the AI asks for is now valued at the human's gold percent, not its own (9544–9550, 9640–9648).
   - After the counter-offer is built, a deal that contains a resource, gold or gold per turn is accepted
     only if `AI_isMutuallyBeneficialDeal` holds for the whole package (9682–9719).
3. **`AI_doDiplo`:**
   - Gold the AI offers for a tech is valued at the recipient's gold percent.
   - A resource swap needs each side's net value to be at least 0. This replaces "each side gains at least
     two thirds of the other's gain" between AIs, and "receive ≥ give" towards humans.
   - A resource bought for gold per turn is priced at the midpoint between the seller's loss and the
     largest payment that leaves the buyer a gain, found by binary search over `AI_goldPerTurnCostVal`
     (18968–19010).

**The switch contract is broken.** `CvGameCoreUtils.h:415–426` and the comment on `AI_DIPLOMACY_FLAGS` in
`BBAI_AI_Variables_GlobalDefines.xml` (value 15) say that 0 restores the old AI. Three changes above ignore
the switches:
- `AI_considerOffer` removed the `isAIDiplomacy(AI_DIPLOMACY_RESOURCE_VALUE)` test, and the new valuation
  applies always.
- In the resource swap of `AI_doDiplo`, the old `!isAIDiplomacy(AI_DIPLOMACY_OFFERS) || …` condition is gone.
- The final check of `AI_counterPropose` and the gold-percent changes test no switch.

So with `AI_DIPLOMACY_FLAGS = 0` the AI is no longer the old AI.

**Reading:** this matters for judging the update. The method compares a variant against the best existing
version in seeded runs (`method/docs/framework.md`, section 7). The flag was the way to run the old version
from the same DLL.
- *Rests on:* the two comments and the removed tests above.
- *Would contradict it:* another build of `cdda5b6` kept for the comparison. None is in `builds/`.
- *Fix:* gate the four changes behind a new bit, `AI_DIPLOMACY_NET_VALUE = 16`, and set the default to 31.
  This keeps 0 and 15 meaning what they meant.

**Reading:** the direction is right, and Smith would recognise it.
- *Rests on:* a trade is now judged by what each side gives up as well as what it gains. Under the old rule
  an AI refused to give a spare resource when the human valued it highly (`max(iOurValue, iOurLoss)`), even
  though giving it cost the AI little.
- *Would contradict it:* seeded runs showing AIs trading away resources they then miss (unhappiness or
  unhealthiness rising after a trade), or gold-per-turn deals that push payers into strikes. Neither has been
  measured. The update has no registered prediction and no experiment, so by rule 9 its effect is an
  **open** question, not a result.

**Two details to check:**
- **Net value of 0 is accepted** (`>= 0` in all three places). A swap where neither side gains passes.
  Harmless, but it lets the AI make zero-value deals that still count towards `AI_changePeacetimeTradeValue`
  in `CvDeal::doTurn` (CvDeal.cpp:298–331), which raises attitude. **Reading:** `> 0` for AI–AI deals would
  stop attitude from being bought with empty trades. *Would contradict it:* such deals never arising, because
  every real swap has a nonzero net.
- **The human side of the final check is the AI's estimate.** `GET_PLAYER(ePlayer).AI_dealNetVal` runs the
  AI's valuation on the human's empire, so the AI may refuse a counter-offer that it judges bad for the
  human. This is new: before, the AI only asked whether the deal was good for itself. **Reading:** it can
  block a deal the human would want, for example when the human values a resource for a plan the AI does
  not model. *Would contradict it:* the check never failing for humans in practice. That needs the game.

### 2c. Other changes

The plot symbol functions `refreshRevealedGraphics`, `updateFeatureSymbolEntity`, `updateRouteSymbol` and
`updatePlotBuilder` gained guards for paged-out plots. `CvGame::reset` initialises the new members
(CvGame.cpp:537–542).

## 3. What the map could not settle

- **Exe calls into the DLL.** The map sees the exported functions, but not which ones the exe calls when, or
  in which order. That affects the out-of-sync question above and the trade screen.
- **Effects in play.** Turn time, memory, AI trade outcomes: all need the game and the seeded harness.
