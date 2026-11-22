# Debt: loans and bonds between civilizations and with an open market

A plan, not an implementation. Nothing is built until the design is approved. Every code change it
describes is gated by a registered prediction (CLAUDE.md, rules 9–10).

Written from the source at `1d9a473` (branch `Graphics-Paging-Fix-Test`), the commit the map was built from.
Line numbers refer to it. This plan replaces the earlier version of this guide, which was written at
`2a8b9a83`. Two facts found since change its recommendation for loans between players:
- gold-per-turn deals create money when the payer is broke (section 1, fact 3);
- a loan cannot be told apart from a purchase inside an ordinary deal.

## 0. Summary

**Instruments.** Two:
- a **loan**, repaid in equal payments each turn;
- a **bond**, paying a coupon each turn and the principal at maturity.

**Counterparties.** Either can be agreed between two civilizations, or with the **open market**: a
counterparty held in `CvGame` that is no player. The market quotes a price per borrower from its credit,
the term, the kind and the collateral.

**Where the code goes:**
- Contracts live in `CvGame`.
- Payments are made explicitly once per player turn, so a broke borrower pays less, and that shortfall is
  recorded. It is not created from nothing.
- Each player keeps a cached turn total, so the gold hot path never loops over contracts.

**How players act:**
- Civilizations agree loans through a loan screen whose actions travel as `ModNetMessage`s handled in C++.
- Putting loans into the exe's trade window is tried first as a one-day prototype (route B, section 6).
- AIs borrow and lend through four functions built on `AI_goldPerTurnCostVal`.

**Phases:**

| phase | what | gated on |
|---|---|---|
| 0 | route B prototype | the game |
| 1 | the market, for humans only | |
| 2 | loans between civilizations | |
| 3 | AI borrowing | |
| 4 | AI lending | |
| 5 | bond resale, collateral seizure | |

Phases 1–5 are each gated by a prediction.

## 1. What exists today (facts)

1. **No debt.** No contract, interest or credit concept exists in the DLL, the Python or the XML.
2. **Gold per turn.** `TRADE_GOLD_PER_TURN` moves gold each turn through `changeGoldPerTurnByPlayer`
   (CvDeal.cpp:803–805) into `m_iGoldPerTurn`. `CvPlayer::calculateBaseNetGold` (CvPlayer.cpp:8342–8350) adds
   it to the gold commerce and subtracts inflated costs.
3. **Broke payers still "pay".** `CvPlayer::doGold` (15287–15354) applies `calculateGoldRate`. If gold falls
   below 0, it sets gold to 0, starts a strike and disbands units. The receiver's gold rate includes the
   full payment regardless.
   - **Reading:** a bankrupt payer's gold per turn is created from nothing on the receiver's side.
   - *Would contradict it:* a check elsewhere that ends or scales a deal when its payer is broke.
     `CvDeal::verify` (CvDeal.cpp:335–383) checks only resources and peace, and `CvGame::doDeals`
     (CvGame.cpp:6952–6962) calls only `verify` and `doTurn`.
4. **Deals are short promises.**
   - Either side may cancel after `PEACE_TREATY_LENGTH` = 10 turns (GlobalDefines.xml:761; CvDeal.cpp:1299–1301).
     That length is the same at every game speed.
   - War ends every deal between the two teams (CvTeam.cpp:1443–1450).
   - An AI re-tests its deals each turn and cancels the ones it no longer accepts (CvPlayerAI.cpp:17425, 17446).
5. **The AI counts payments it owes.** `AI_isFinancialTrouble` (CvPlayerAI.cpp:4112–4167) adds
   `max(0, −getGoldPerTurn())` to expenses and calls the AI troubled when less than 40% of net commerce is
   funded. The threshold is lowered by war plans, by avoiding science and by repeat research.
6. **The AI has a payer-cost curve.** `AI_goldPerTurnCostVal` (9789–9810, new in 1d9a473) values a payment at
   between 1 and 2 times its trade value, by the share not covered by
   `max(0, goldRate) + (gold − goldTarget)/10`.
7. **Gold limits for trades** are `AI_maxGoldTrade` and `AI_maxGoldPerTurnTrade` (9724–9778). Both are
   exported, and the exe uses them for the gold boxes.
8. **Saves are versioned by a flag per class:**

   | class | flag | where | how the read checks it |
   |---|---|---|---|
   | `CvPlayer` | 1 | CvPlayer.cpp:19022 | `if (uiFlag > 0)` at read offset 502 |
   | `CvGame` | 1 | CvGame.cpp:9416 | `if (uiFlag < 1)` at read offsets 9 and 56 |
   | `CvDeal` | 0 | CvDeal.cpp:664 | no check |

9. **Network messages.**
   - `CvNetModNetMessage::Execute` (CvMessageData.cpp:524–526) passes five integers to Python's
     `onModNetMessage` and does nothing else.
   - Ids used by the mod's Python: 100 and 101 (Revolution.py:156–157), 410 and 411
     (RoMEventManager.py:140–141), 500 and 501 (CvStrategyOverlay.py:94–95), 5088 (RoMEventManager.py:142),
     5656 (AIAutoPlay.py:61).
10. **Inflation** (`calculateInflationRate`, CvPlayer.cpp:8258–8307) rises quadratically with turns. It
    multiplies costs, not gold held or owed.
11. **Game length differs by speed** (total `iTurnsPerIncrement` in CIV4GameSpeedInfo.xml):

    | speed | turns |
    |---|---|
    | Blitz | 215 |
    | Quick | 352 |
    | Normal | 700 |
    | Epic | 1050 |
    | Marathon | 1470 |
    | Snail | 3000 |

    None of the speed percent fields equals these ratios. For Marathon, `iResearchPercent` is 600,
    `iVictoryDelayPercent` 300 and `iGrowthPercent` 200, while turns are 1470/700 = 210% of Normal.
12. **The exe's `TradeableItems` has no count** (CvEnums.h:1951–1986). See `diplomacy-screen-and-civics.md`,
    section 1.2.

## 2. The instruments

| term | loan | bond |
|---|---|---|
| principal `P` | paid to the borrower at signing | paid to the issuer at signing |
| payments | equal each turn (annuity): `A = P·r / (1 − (1+r)^−T)` | coupon `P·r` each turn |
| principal back | inside the payments | `P` at maturity |
| term `T` | turns, scaled by game length (section 3.3) | same |
| rate `r` | per turn, fixed at signing, or floating on the market base rate | same |
| early repayment | allowed, outstanding principal plus a penalty in turns of interest | issuer may call it, if callable |
| resale | no | phase 5: the holder may sell it to the market at the market's price |

**Conditions** a contract can carry, chosen from a fixed list so the AI can value them:
- **Collateral:**
  - none;
  - a resource: on default it becomes an annual gift to the lender for `T` turns;
  - a city: on default it goes to a civilization lender. The market takes no cities; it takes the city's
    gold output for `T` turns instead.
- **Purpose terms:**
  - *war bond:* a higher limit while at war and a higher rate;
  - *development loan:* a lower rate, available only below the average score.
- **Covenant:**
  - *no war on the lender:* breaking it is default;
  - *no new debt above a ratio:* breaking it raises the rate by a step.

All arithmetic is in integers: amounts in gold, rates in basis points per turn (1/10,000). The annuity is
computed by a 64-bit integer loop over `T` turns. Floating-point values would differ between machines'
compilers and settings and desynchronise a network game.

## 3. Pricing and credit

### 3.1 The market base rate

- `CvGame::m_iMarketBaseRateBp` is updated once per game turn.
- It moves towards a target, at most one step per turn.
- The target is a real rate (a define) plus the expected inflation per turn: the difference of
  `calculateInflationRate` between this turn and the next, averaged over alive players.
- **Market supply:** the market lends from a pool, `m_iMarketCapital`.
  - It grows by a define percent of the world's total gold commerce each turn, and by repayments and
    coupons.
  - It shrinks by loans out and by defaults.
  - A pool below a share of its target raises the rate. A scarce market is dear.

**Reading:** a nominal rate that includes inflation keeps debt from becoming free late in the game, when
inflation runs high.
- *Rests on:* fact 10. Owed gold is not inflated, so a fixed nominal rate below inflation is a subsidy to
  borrowers.
- *Would contradict it:* the inflation per turn being negligible next to any rate. That can be computed from
  the formula for each speed and era, without simulating (rule 9).

### 3.2 A borrower's credit

`CvPlayer::getCreditScore()` is computed in integers from the player's own figures and cached once per turn:

| input | how | source |
|---|---|---|
| debt service ratio | payments owed per turn ÷ gross gold + research commerce | the per-player cache (section 4) and `getCommerceRate` |
| financial trouble | the AI test of fact 5, applied to any player | `AI_isFinancialTrouble`; its logic moved to `CvPlayer`, or reproduced |
| default history | defaults in the last `N` turns, decaying | new `m_iDefaultTurns` |
| size | cities and population | `getNumCities`, `getTotalPopulation` |
| war | at war, losing cities | `GET_TEAM().getAtWarCount`, war memory |

- **Spread** = `f(score)`, a short table in a new defines file.
- **Limit:** new borrowing is refused when debt service after the loan would exceed a define percent of
  gross commerce.

A civilization lender quotes its own price (section 7); the score is information it uses.

### 3.3 Game speed

- Terms and rates are stated for Normal speed in the defines.
- At load, the DLL computes `L` = total turns of the game speed × 100 / total turns of Normal, from
  `GameTurnInfos`: 210 for Marathon.
- A term is `T × L / 100`.
- A per-turn rate is the rate such that compounding over `L/100` turns equals one Normal turn.
  - Computed once at load, in integers, by bisection.
  - At the rates in question, `r × 100 / L` is close enough. The bisection removes the question.
- **Reading:** `L` is the right clock because a loan's cost should be the same share of a game at every
  speed. The percent fields measure other things (research, growth). This is a design choice. *What would
  contradict it:* an economy whose gold commerce per turn does not scale like `1/L`. That can be checked from
  the logs of seeded runs at two speeds.

## 4. Data model

```cpp
// CvDebt.h (new): one contract
struct CvDebtContract
{
	int iID;
	DebtKinds eKind;               // DEBT_LOAN, DEBT_BOND
	PlayerTypes eBorrower;
	PlayerTypes eLender;           // NO_PLAYER = the market
	int iPrincipal;                // at signing
	int iOutstanding;              // principal still owed
	int iRateBp;                   // per turn, basis points
	bool bFloating;                // follows m_iMarketBaseRateBp + spread
	int iPayment;                  // per turn: annuity (loan) or coupon (bond)
	int iSignTurn, iMaturityTurn;
	int iArrears;                  // unpaid gold carried forward
	int iMissedTurns;
	DebtCollateral eCollateral; int iCollateralData;   // resource or city id
	int iConditions;               // bit flags: war bond, no-war covenant, ...
	void read(FDataStreamBase*); void write(FDataStreamBase*);
};
```

**`CvGame`:**
- `FFreeListTrashArray<CvDebtContract> m_debts`, as deals use;
- `m_iMarketBaseRateBp`, `m_iMarketCapital`;
- the pending offers of section 6.

**`CvPlayer`** caches, updated when a contract is signed, paid, defaulted or ended, never recomputed on the
hot path:
- `m_iDebtDuePerTurn` (owed);
- `m_iDebtIncomePerTurn` (owed to it);
- `m_iDebtOutstanding`;
- `m_iDebtReceivable`: received last turn, credited this turn; see 5.2.

**Saves:**
- `CvGame::write` and `read`: flag 1 → 2. Market and contracts are read when the flag is at least 2.
- `CvPlayer::write` and `read`: flag 1 → 2. The caches are read when the flag is at least 2.
  - The caches are saved rather than rebuilt at load, because the exe decides the order in which `CvGame`
    and the players are read, and the source does not show it.
- `CvPlayerAI` gets the default memory of section 7.3, behind its own flag.
- Old saves load with no debt.

## 5. Turn processing

### 5.1 The hot path stays a constant

`calculateBaseNetGold` gains one term: `− m_iDebtDuePerTurn + m_iDebtIncomePerTurn`. Effects:
- the slider, the top bar, `AI_isFinancialTrouble` and `AI_goldTarget` see the debt;
- debt is not counted inside `calculateInflatedCosts`, so payments are nominal (fact 10);
- the comment in `calculatePreInflatedCosts` (CvPlayer.cpp:8236) warns that this path is called tens of
  thousands of times per turn; one member read keeps it constant.

`AI_isFinancialTrouble` reads `getGoldPerTurn()`, not `calculateBaseNetGold`. It gets
`m_iDebtDuePerTurn − m_iDebtIncomePerTurn` added to its expenses explicitly.

### 5.2 Payment without creating money

1. **Borrower,** in `CvPlayer::doGold`, after `changeGold(iGoldChange)`:
   - if gold is below 0, the debt part of the shortfall is unpaid: `unpaid = min(−gold, m_iDebtDuePerTurn)`;
   - the unpaid amount is spread over the borrower's contracts, oldest first, as arrears;
   - gold is raised by `unpaid` before the existing strike logic runs. The debt took no gold the borrower
     did not have; the strike still follows from other costs.
2. **Lender:** what each contract actually paid is added to its lender's `m_iDebtReceivable`, or to the
   market's capital.
3. **The lender's next `doGold`** credits `m_iDebtReceivable` and then clears it.
   - The lag of one turn is the price of not depending on the order in which players take their turns.
   - The `+m_iDebtIncomePerTurn` term in 5.1 is the expected income for the slider. The credit is the real
     one.
4. **Bullet repayment** of a bond at maturity is a lump in `CvGame::doDebt`. If the issuer's gold falls
   short:
   - the market refinances it at a penalty rate, when the issuer's limit allows;
   - otherwise it is arrears.

The same fix should be offered for ordinary gold-per-turn deals (fact 3). That would be a separate change
with its own prediction.

### 5.3 Once per game turn

`CvGame::doTurn` (CvGame.cpp:6804–6948) calls a new `CvGame::doDebt` after `doDeals`:
- update the base rate and the market pool;
- for each contract:
  - move a floating rate;
  - reduce the outstanding principal by the principal part of what was paid;
  - mature or end the contract;
  - apply default rules (5.4).
- refresh the player caches of changed contracts.

### 5.4 Default

- **Arrears:** each turn they accrue at the contract rate plus a penalty.
- **Default:** after `DEBT_GRACE_TURNS` turns with arrears (scaled by `L`), or at once on breaking a
  covenant. Then:
  - **collateral:** a resource becomes an annual gift through `CvGame::implementDeal` (the existing path); a
    city goes through `CvPlayer::acquireCity` to a civilization lender, or its gold output to the market;
  - **memory:** the lender gets a "defaulted on us" memory (7.3); the market sets `m_iDefaultTurns`;
  - **exclusion:** the market refuses new debt for a define number of turns;
  - **write-off:** the outstanding principal and arrears are written off; the contract ends.
- **War between borrower and lender:**
  - payments stop, and the contract is frozen;
  - at peace it resumes, with the frozen turns added to the term;
  - if the borrower declared the war, it is a default.
- **Vassals:** a new master does not take on its vassal's debts. Debt survives `CvTeam::setVassal`
  (CvTeam.cpp:4814–5122) unchanged.
- **Death:** if a player dies (`CvPlayer::setAlive`, CvPlayer.cpp:11816–11905), its debts are written off and
  the contracts it held as lender are cancelled.
- **Chance:** none. Default is a rule, not a roll. If a roll is ever added, it must use
  `CvGame::getSorenRandNum` (CvGame.cpp:8897–8899) so that every machine draws the same number.

## 6. How players make contracts

### 6.1 With the market

The market is no player, so there is no diplomacy.
- A **Debt** screen (6.4) shows the market's live quote for each kind, term and condition. The quote comes
  from `CvGame::getMarketQuote(ePlayer, kind, term, conditions, &rate, &limit)`, a const function.
- Buttons send a `ModNetMessage` in a reserved id range, **7000–7099**, which no Python module uses (fact 9):

  | id | action | data |
  |---|---|---|
  | 7000 | borrow | kind, amount, term index, conditions |
  | 7001 | buy a market bond (lend to the market) | kind, amount, term index |
  | 7002 | repay early | contract id |
  | 7003 | sell a bond to the market (phase 5) | contract id |
  | 7010–7012 | offer / accept / refuse a loan between civilizations | below |

- `CvNetModNetMessage::Execute` handles 7000–7099 in C++ and passes every other id to Python as today. The
  rules run in the DLL on every machine, from the same synced state, so the screens never change state
  themselves.
- The market re-checks the quote when the message arrives: the state may have moved since the click.

### 6.2 Between civilizations

There are three routes.

**Route A: an ordinary deal of gold for gold per turn.** Rejected:
- the payments would create money when the borrower is broke (fact 3);
- the deal could be cancelled after 10 turns (fact 4);
- nothing tells a loan from a purchase of a resource for a lump sum.

**Route B: a new trade item `TRADE_LOAN` in the exe's trade window.** Its data is an index into a pending
loan offer held by `CvGame`, which carries the terms.
- The DLL side is feasible: `buildTradeTable`, `getHeadingTradeString`, `getItemTradeString`, `canTradeItem`,
  `getTradeDenial` and `CvDeal::startTrade` all switch on the item type.
- What cannot be seen is whether the exe shows a 17th heading (section 1.2 of the diplomacy guide).
- **Phase 0 tests it.** Add `TRADE_LOAN` at the end of the enum, return a heading string for it, and look at
  the trade window in the game. One day's work; it needs the game. If the heading appears, route B is used
  for the trade window, with route C's back end.

**Route C: a loan screen of the mod** (the fallback, and the back end in any case):
- *Offer:* the Debt screen's "Offer a loan" tab, or a button on the foreign advisor, picks a civilization
  and terms, and sends 7010. `CvGame` stores the pending offer: proposer, the other side, terms, and the turn
  it expires.
- *An AI answers* in the same message's execution, on every machine, through
  `CvPlayerAI::AI_considerLoan` (7.2), and the result is shown.
- *A human answers* through a popup (a `CvPopupInfo` of `BUTTONPOPUP_PYTHON`) that sends 7011 or 7012.
- *An AI offers a human a loan* from `AI_doDiplo` (section 7). The offer reaches the human as the same popup.
  It cannot use the diplomacy window, which can only show the existing items.
- *Between AIs,* `AI_doDiplo` signs directly. No message is needed: the AI turn runs on every machine.

### 6.3 What a signed loan does

`CvGame::signDebt(contract)`:
- moves the principal with `changeGold` (exported; signature unchanged);
- adds the contract;
- updates both caches;
- posts a Python event (`CvEventReporter`, a new `debtSigned` event), so mods and the event log can react.

### 6.4 Interface

- **Finance advisor** (`Python/Screens/BugFinanceAdvisor.py`, chosen in
  `Python/EntryPoints/CvScreensInterface.py`):
  - a "Debt payments" row among the expenses and an "Interest received" row among the incomes;
  - a button that opens the Debt screen.
- **Debt screen:** a new screen with an id in `Python/Screens/CvScreenEnums.py`, entries in
  `CvScreensInterface.py`, and buttons with `WIDGET_GENERAL`. Three tabs:
  - contracts held and owed;
  - market quotes;
  - offer a loan.
- **Tooltips:** `WIDGET_HELP_FINANCE_DEBT` goes at the end of `WidgetTypes`, never in the middle, because the
  exe uses the numbers. It gets a case in `CvDLLWidgetData::parseHelp` (CvDLLWidgetData.cpp:53–653) and a
  `CvGameTextMgr::buildFinanceDebtString`.
- **Text:** new `TXT_KEY_DEBT_*` entries in the mod's `XML/Text`. Text needs no prediction (`method/config.json`,
  `text_only`).
- **Python access:**
  - `CyGame`: `getNumDebts`, `getDebt(i)` returning a small `CyDebt` wrapper (getters only), `getMarketQuote`,
    `getMarketBaseRate`;
  - `CyPlayer`: `getDebtDuePerTurn`, `getDebtIncomePerTurn`, `getDebtOutstanding`, `getCreditScore`;
  - bound in `CyGameInterface.cpp` and `CyPlayerInterface*.cpp`.
  - Nothing that changes state is bound for Python.

## 7. The AI

All decisions are integer functions of synced state. Each is a pure helper in a new header,
`AIDebtPolicy.h`, beside the existing `AI*Policy.h` headers, so it can be compiled and checked natively
without the game.

### 7.1 Borrowing from the market (phase 3)

`CvPlayerAI::AI_doDebt`, called from `AI_doTurnPost` (CvPlayerAI.cpp:543–577) before `AI_doCommerce`
(16646–17127). It borrows when one of three conditions holds:

1. **To avoid a strike.**
   - Condition: `calculateGoldRate() + getGold() < 0` next turn, with no slider setting that covers it.
   - It borrows the smallest loan that covers the gap for `T` turns, if the payment passes
     `AI_goldPerTurnCostVal(payment) ≤ value of avoiding the strike`. The value of avoiding the strike is the
     upkeep gold of the units the strike would disband: `disbandUnit` takes `strikeTurns/2` units
     (CvPlayer.cpp:15287–15354).
2. **War chest.**
   - Condition: a war plan is prepared (`AI_getWarPlan`) and production is short of the plan.
   - It borrows a war bond if the gold, spent on hurrying or upgrading, yields more than its cost over the
     term.
3. **Not otherwise.** No borrowing to fund research by default. A define enables it later, for an
   experiment.

The repayment test reuses fact 6: a payment is affordable when `AI_goldPerTurnCostVal(payment)` stays at
most a define multiple of its trade value. At that bound the payment is covered by income.

### 7.2 Lending (phase 4)

`AI_considerLoan(eBorrower, terms)` and the offers in `AI_doDiplo`.

- **Lends only gold it can spare:** `getGold() − AI_goldTarget()` (4199–4294).
- **Value of a loan** = present value of the payments × the chance they continue − principal.
  - *Present value:* at the AI's own hurdle rate, the market base rate plus a define.
  - *Chance they continue:* falls with war risk, read from the AI's own war plan against the borrower, its
    attitude (`AI_getAttitudeVal`, 7387–7518), the borrower's credit score, and whether they share a war
    enemy.
- **Accepts** when the value is above 0 and the borrower is not a target of the lender's war plans.
- **Never lends to a team it plans war on.**
  - **Reading:** this follows Thucydides' Corcyra debate (`smith-machiavelli-and-the-game.md`): lending
    strengthens a future enemy.
  - *Would contradict it:* runs where lending to rivals raises the lender's cities taken.

### 7.3 Attitude and memory

- A new `m_aiDefaultedOnUs[MAX_PLAYERS]` in `CvPlayerAI`, decaying, saved behind its flag. It enters
  `AI_getAttitudeVal` as a negative term with its own text line.
- A loan currently being paid enters as a small positive term, like the peacetime trade value.
- No new `MemoryTypes` value: the enum is shared with the exe, and its use there cannot be seen.

### 7.4 Valuation inside trades (only if route B works)

`AI_dealVal` and `AI_tradeGiveVal` get a `TRADE_LOAN` case:
- for the lender, the value of 7.2;
- for the borrower, principal − `AI_goldPerTurnCostVal(payment)` summed over the term with discounting.

The mutual-benefit check of 1d9a473 then applies unchanged.

## 8. How it is judged

**Computed, not simulated (rule 9).** Tables written from the formulas through `method/figlib.py`:
- annuity payments by term and rate;
- the speed factor `L` per speed;
- the market rate path under the inflation formula, per speed;
- the largest affordable payment from `AI_goldPerTurnCostVal`.

**Experiments.** The registered essential variables are `completed`, `turn_seconds`, `taken` and `lost`
(`method/mission/variables.json`). Each phase's prediction is made on one of them before its runs:

| phase | prediction |
|---|---|
| 1 (market, human only) | `completed` no regression, `turn_seconds` no worse; AI-only runs unchanged by construction |
| 3 (AI borrowing) | `completed` no regression; `turn_seconds` no worse; a stated direction on `taken` and `lost` (the AI defends better if it avoids strikes) |
| 4 (AI lending) | the same, against phase 3 |

- Each with at least 5 seeded runs (`HARNESS_RESEED`), Welch's test on ranks, against the best existing
  version and fixed opponents.
- An economic variable (strike turns, defaults per game) would make these sharper. Adding one is a method
  change (a `Method:` trailer) and needs the user's approval. Until then, such counts are reported as
  descriptions, not as results.

**Correctness checks:**
- `AIDebtPolicy.h` compiled natively: annuity sums to principal plus interest; no overflow at the largest
  terms; monotone spreads.
- A save from the current build loads with no debt.
- A save with debt reloads to the same caches.
- **Network sync:** the network game with two machines is open. Without it, every new action goes through
  7000–7099 and every rule reads synced state only. The graph check of `test-branch-1d9a473.md` (part 2a) is
  repeated for every new member: no reader outside the debt code, no state written from the interface.

## 9. Phases

| phase | content | needs |
|---|---|---|
| 0 | `TRADE_LOAN` heading prototype; read what the exe shows | the game |
| 1 | `CvDebtContract`, market, pricing, payment, default, saves, Debt screen, finance rows; market only, humans only | prediction on `completed` and `turn_seconds` |
| 2 | loans between civilizations by route C (and B if phase 0 succeeded); human ↔ AI and human ↔ human | as above |
| 3 | AI borrowing (7.1) | prediction on `taken` and `lost` |
| 4 | AI lending and AI ↔ AI loans (7.2–7.3) | as above |
| 5 | bond resale to the market; collateral seizure of cities; covenants | as above |

## 10. Risks

| risk | where | guard |
|---|---|---|
| A broke borrower's payments create money | fact 3 | 5.2 |
| The AI borrows into strikes | 7.1 | test 1 needs the strike to be avoided; debt counted in `AI_isFinancialTrouble` (5.1) |
| Network desync | any state changed from a screen | 6.1; integer math only (section 2) |
| Old saves fail to load | read flags | section 4 |
| The exe misreads a new enum value | `TradeableItems`, `WidgetTypes` | values appended at the end only; phase 0 |
| Human exploit: borrow from an AI, then declare war | 5.4 | declaring war on the lender is default; memory 7.3; market exclusion |
| Debt becomes free late in the game | fact 10 | 3.1 |
| Speed distortions | fact 11 | 3.3 |
| Turn time | 5.1, 5.3 | constant hot path; one pass over contracts per game turn |
| Revolution component misses debt | `Revolution.py:1849–1858` repeats the AI's funded-percent test from `getGoldPerTurn()` and `calculateInflatedCosts()`, with a threshold of 75% (lowered by wars), as a stability factor. Debt kept outside `getGoldPerTurn` would not reach it | add `getDebtDuePerTurn() − getDebtIncomePerTurn()` to `iNetExpenses` there in phase 1; other gold reads in Revolution (`RevUtils.py:967`, `Revolution.py:473, 2076–2132`, buy-off costs at 2974, 3028) see the gold held, which a loan raises: **open** whether that lets a ruler borrow out of a revolt |
