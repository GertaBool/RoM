# Debt: loans and bonds between civilizations and with the open market

[`../debt.patch`](../debt.patch) applies to GitLab `Graphics-Paging-Fix-Test` at `8587217` ("Selection fix").
The local commit is `af47b07`, tree `2d9f7500`; the DLL source folder's tree is `08540323`.
It implements the plan in [`codemap/guides/loans-and-bonds.md`](../../codemap/guides/loans-and-bonds.md). The
prediction it serves is P14 (`method/mission/register.json`): runs reach their result line no less often with
debt than without. The build is in [`builds/debt`](../../builds/debt/).

## What it does

### Contracts

There are two kinds of contract:
- a **loan**, repaid in equal payments each turn;
- a **bond**, which pays a coupon each turn and the principal at maturity.

Either kind is made with the **market** (a counterparty held in `CvGame`, not a player) or between two
**civilizations**.

Terms come in four lengths: `DEBT_TERM_0`–`3`, 10/20/30/50 turns at Normal speed. They scale with the game
speed's length in turns (Marathon 1470 turns, Normal 700: 210 %).

The market offers five products:

| product | condition |
|---|---|
| loan | none |
| floating-rate loan | the rate follows the base rate |
| bond | none |
| war bond | only at war; higher limit and rate |
| development loan | only below the average score; lower rate |

Civilizations can also lend to the market by buying its bonds, and sell claims they hold to the market.

Between civilizations a loan can carry a resource or a city as collateral.

### Prices and limits

Every rate is an integer in parts per million per turn. It is made of:
- the market base rate, which moves an eighth of the way to its target each turn. The target is a real
  rate plus the rise of the average price level from the game's own inflation formula, adjusted for how
  scarce the market's capital is;
- a credit spread from the borrower's score (0–100);
- a premium per term step;
- the condition's premium or discount.

The market lends while all payments stay within `DEBT_MAX_SERVICE_PERCENT` (25 %) of gross gold and research
commerce, and while the principal stays within `DEBT_PRINCIPAL_CAP_TURNS` turns of that commerce. It never
lends more than its capital.

### Payments

Each turn the borrower pays only what it has (in `CvPlayer::doGold`). The unpaid part becomes **arrears**,
which carry a penalty rate. Lenders receive what was actually paid, at their next `doGold`. A broke borrower
therefore creates no gold for its lender, unlike the game's ordinary gold-per-turn deals.

### Default

After `DEBT_GRACE_TURNS` (5) turns in a row with arrears, the debt is in **default**:
- the collateral goes to the lender;
- the market lends the defaulter nothing for `DEBT_DEFAULT_EXCLUSION_TURNS`;
- a civilization lender remembers the default (attitude, fading over `DEBT_DEFAULT_MEMORY_TURNS`);
- the claim is written off.

A borrower that declares war on its lender defaults. A war between the two parties freezes the contract and
moves its maturity on.

### The AI

The AI (`CvPlayerAI::AI_doDebt`, after `AI_doDiplo`) does four things:
- borrows to avoid a strike;
- takes a war chest when at war or preparing one (a war bond at war);
- repays its dearest debt early when well above its gold target;
- lends spare gold: to the civilization it likes best that is short of gold, or to the market.

It answers human offers with `AI_considerLoan`. Its value of a loan is the present value of the payments
times the chance they continue (from attitude, credit, collateral and war), minus the principal. It never
lends to a team it plans war on, and never borrows from one.

Debt counts in `AI_isFinancialTrouble`, in `AI_goldTarget` (three turns of payments) and in Revolution's
financial-stability test (`Revolution.py`).

### The interface

- **Debt screen:** `Python/Screens/CvDebtScreen.py`, opened from a button on the Finance Advisor. It shows
  contracts held and owed, the market's quotes, and offers to and from other civilizations.
- **Finance Advisor:** two rows, debts owed to you and debt payments.

Every action is a `ModNetMessage` with an id in 7000–7099, handled in C++ (`CvNetModNetMessage::Execute`).
The screen never changes the game itself, so network games stay in step.

### Saves

| class | save flag | what is added |
|---|---|---|
| `CvGame` | 2 | contracts, offers, market |
| `CvPlayer` | 2 | caches |
| `CvPlayerAI` | 7 | memory of defaults |

Older saves load with no debt. `DEBT_ENABLE 0` switches the whole mechanic off.

## Files

| file | content |
|---|---|
| `AIDebtPolicy.h` | the arithmetic, game-free: annuity (with the game's rounding of interest), present value, speed conversion of rates, credit score and spread, borrowing limit, a lender's value of a loan |
| `CvDebt.h`, `CvDebt.cpp` | contracts and offers; the rules, in `CvGame`, `CvPlayer` and `CvPlayerAI` methods; network messages; logging |
| `CvGame.h/.cpp` | members, reset, `doDebt` after `doDeals`, save flag 2 |
| `CvPlayer.h/.cpp` | caches, `calculateBaseNetGold` (one member read), `doGold`, save flag 2 |
| `CvPlayerAI.h/.cpp` | `AI_doDebt` call, attitude term, financial trouble, gold target, save flag 7 |
| `CvTeam.cpp` | `declareWar` calls `onDebtWarDeclared` |
| `CvMessageData.cpp` | ids 7000–7099 handled in C++ |
| `CyGame*`, `CyPlayer*` | getters for Python, nothing that changes state |
| `GlobalDefinesAlt.xml` | 27 `DEBT_*` defines, each commented |
| `XML/Text/Debt_CIV4GameText.xml` | 72 text keys, English in all five language tags |
| Python | the Debt screen, Finance Advisor rows and button, screen enum and entry point, Revolution's financial test |

## Checks

### Build

`toolchain/build_dll.sh`, `CLEAN=1`, Visual C++ Toolkit 2003 under Wine, release target: 0 errors, 0 warnings.

| property | value |
|---|---|
| size | 6,217,728 bytes |
| SHA-256 | `ff172b2e…7015a87` |
| exports | 2,452 names, the same count as `8587217` |

### Python

All five changed Python files compile under Python 2.4.4 (`compile()`, run under Wine).

### Arithmetic

[`tests/test_debt_policy.cpp`](tests/test_debt_policy.cpp), `g++ -std=c++98 -Wall -Wextra`: all checks pass.
- **Loans:** 245 combinations of principal, rate and term. Each loan is repaid exactly within its term, with
  interest rounded as the game rounds it. The first version of the annuity left a remainder at maturity in
  most of them; this test found that.
- **Speed conversion:** compounds to the same growth.
- **Spreads and scores:** spreads fall as scores rise.
- **Limits:** the payment of the limit fits, and one more gold does not.
- **Present values:** checked as well.

### Headless runs

The harness (`toolchain/harness`), 300 turns at Normal speed, Noble, was run on a generated scenario
([`harness/make_scenario.py`](harness/make_scenario.py)):
- one 52×34 continent;
- six AI civilizations with two cities each, the first era's techs and 300 gold;
- everyone in contact;
- Revolution, BarbarianCiv and Tech Diffusion off.

Arm a is the debt build and arm b is `8587217`. Each arm has five runs on the seeds `ledger.py seeds P14`
gives. The seed is passed as the scenario's random seed: in scenario mode the harness does not read
`HARNESS_RESEED`, which only reseeds a loaded save. A first set of runs used it, and every run of an arm
came out identical; those runs were discarded.

Two edits to a local copy of the harness, outside `toolchain/`:
- [`harness/HarnessState-test-branch.patch`](harness/HarnessState-test-branch.patch) stubs three diagnostics
  that call AI functions this branch does not have (`AI_balanceHegemon`, `AI_balanceNoWarProb`,
  `AI_stagedForecast`);
- the harness's base XML files from AdvCiv were taken from the original game's XML instead.

Each run directory under [`runs/`](runs/) keeps `run.log`, `run.jsonl` and `debt.log` (the debt lines of the
BBAI log).

| arm | seed | result | civs alive at 300 | contracts | borrowed | of which war bonds | market bonds bought | payment shortfalls | defaults | early repayments |
|---|---|---|---|---|---|---|---|---|---|---|
| a | 1276710784 | turn 300 | 5 | 63 | 14 | 8 | 49 | 5 | 1 | 2 |
| a | 1758601584 | turn 300 | 6 | 56 | 17 | 12 | 39 | 0 | 0 | 4 |
| a | 1870926109 | turn 300 | 4 | 78 | 22 | 15 | 56 | 11 | 1 | 4 |
| a | 854728325 | turn 300 | 4 | 48 | 12 | 10 | 36 | 2 | 0 | 2 |
| a | 908745140 | turn 300 | 6 | 71 | 22 | 18 | 49 | 3 | 0 | 9 |
| b | 1233860452 | turn 300 | 5 | – | – | – | – | – | – | – |
| b | 196739820 | turn 300 | 6 | – | – | – | – | – | – | – |
| b | 42380683 | turn 300 | 4 | – | – | – | – | – | – | – |
| b | 568643073 | turn 300 | 6 | – | – | – | – | – | – | – |
| b | 91720609 | turn 300 | 6 | – | – | – | – | – | – | – |

All ten runs reached their result line. The evidence of P14 is recorded in
`method/mission/evidence/P14/a.tsv` and `b.tsv`.

**Both defaults** (seeds 1276710784 and 1870926109):
- player 3 borrowed 20 gold from the market for 10 turns to avoid a strike;
- it then paid nothing for five turns (owed 3, 6, 9, 12, 15);
- its debt grew to 28 with the penalty, and it defaulted.

**No loan between civilizations was made in these runs.** The AI offers one only to a civilization it is
at least pleased with that is short of gold. Human offers are untested (no human in the harness).

## Readings

- **The mechanic runs without breaking the game in these runs:**
  - all runs completed;
  - payments, arrears, defaults, early repayment and the market's turn ran;
  - nothing in the runs points to lost or created gold.

  *What would contradict it:* a run that stops, or a player whose gold moves without a matching contract
  record. Gold flows were not audited turn by turn: **open**.
- **Borrowing to avoid a strike helps only when the deficit is temporary.** Both defaults were such loans
  that delayed insolvency by one turn.
  - *Rests on:* the two default traces above.
  - *Would contradict it:* such loans being repaid in other runs. None of the strike loans in these runs
    was followed to its end in this README.
  - *A change to consider:* borrow only when the player could cover the payment at a full gold slider.

## Open

- **The exe's trade window** (route B, phase 0): untested; needs the game.
- **In the game:**
  - the Debt screen and the Finance Advisor rows;
  - human offers and answers;
  - network games;
  - old saves loading.

  The harness has no Python, no interface and no network.
- **Python events** for debt (signed, default) are not posted.
- **Translations:** the texts are English in every language.
- **Unchecked edge cases:**
  - a vassal that joins its master's war against its own lender defaults like any declarer;
  - `handleDebtMessage` trusts the player number in the message, as the mod's Python messages do.
