# Adding loans and a bond market

Where loans between players and a bond market would go in the code, and what to watch. A plan, not an
implementation. Written by hand from the source at commit `2a8b9a83eb5b`, the commit the map was built
from; line numbers refer to it. Nothing like debt exists in the mod today.

The work falls in three places:
- the DLL: where the money is stored, moved each turn and saved, and the AI's decisions;
- the Python screens: what the player sees;
- one network message, so that what a player does on a screen happens on every machine of a network game.

## 1. Where the money moves (DLL)

Every turn's gold passes through one function: `CvPlayer::calculateBaseNetGold` (CvPlayer.cpp:8342). It
adds gold commerce and gold-per-turn deals and subtracts the inflated costs. Loan payments added there
reach everything else on their own:
- the turn's payment through `calculateGoldRate` (8491), applied by `doGold` (15284);
- the top bar's gold rate in `Python/Screens/CvMainInterface.py` (3313) and its tooltip `setGoldStr`
  (CvGameTextMgr.cpp:271);
- the research slider.

Three things to watch:
- **Speed.** The comment in `calculatePreInflatedCosts` (8236) says the AI calls this path tens of
  thousands of times per turn. Keep the turn's loan total in a member variable, updated when a loan changes;
  never loop over loans there.
- **Inflation.** Inside `calculateInflatedCosts` (8311) loan payments would inflate; beside it, debt stays
  in nominal gold. That is a design choice.
- **Missing a payment.** `doGold` already handles running out of gold: gold is set to 0, a strike starts
  and units are disbanded. Missed payments and default belong there.

Taking a loan pays the principal through `changeGold` (9846). It is exported to the exe: keep its
signature.

## 2. State and saves

- **Each player's loans** go in `CvPlayer`, reset in `CvPlayer::reset`. Write them at the end of
  `CvPlayer::write` (19012) and raise its version flag from 1 to 2; in `CvPlayer::read` (18457) read the new
  fields only when the flag is at least 2, so older saves still load.
- **The market** (interest rate, bonds outstanding) goes in `CvGame`, versioned the same way in
  `CvGame::read` and `CvGame::write` (8285, 8529). Update it once per game turn in `CvGame::doTurn`
  (CvGame.cpp:5921), after `doDeals`.
- **Rates and limits** are global defines. `XML/GlobalDefinesAlt.xml` works as it is; a new defines file
  needs its own `ReadGlobalDefines` line in `CvXMLLoadUtility::SetGlobalDefines`
  (CvXMLLoadUtilitySet.cpp:208–238).

## 3. Loans between players

**Route A: build on existing deals (recommended).** A loan is a lump of gold to the borrower
(`TRADE_GOLD`) and gold per turn back to the lender (`TRADE_GOLD_PER_TURN`). That works end to end today:
the exe's diplomacy screen, the AI's valuation (`CvPlayerAI::AI_dealVal` 8823, `AI_considerOffer`), saves and
network games. `CvDeal::startTrade` moves the per-turn gold into each side's `m_iGoldPerTurn`, which
`calculateBaseNetGold` adds in.

What is missing is a term. Either side can cancel a deal after `PEACE_TREATY_LENGTH` turns
(`CvDeal::turnsToCancel`, CvDeal.cpp:1294), so a borrower could stop paying. Add a term to `CvDeal`, refuse
cancelling in `isCancelable` (1275) until the loan is repaid, and end the deal at maturity in
`CvDeal::doTurn` (297).

**Route B: a new trade item `TRADE_LOAN`.** The exe's diplomacy screen asks the DLL for its items through
exported functions: `CvPlayer::buildTradeTable`, `getHeadingTradeString`, `getItemTradeString`,
`canTradeItem`, `getTradeDenial`. But the exe was compiled with a version of `TradeableItems` that has no
count of headings, and how the exe walks them cannot be seen in the source. This route needs testing
against the exe. If taken, the new value goes at the end of the enum.

## 4. The bond market

A market has no other player, so it does not go through diplomacy: issuing bonds is borrowing from the
market, buying bonds is lending to it. Both are actions on a screen, and a screen must never change the
game state directly, or a network game goes out of sync.

The existing path is `CyMessageControl().sendModNetMessage` (five integers). It arrives in
`CvNetModNetMessage::Execute` (CvMessageData.cpp:524), which today only passes it to Python's
`onModNetMessage` (`Python/RoMEventManager.py`, 151). Handle a reserved range of message ids in C++ inside
`Execute`, so all loan logic stays in the DLL. If default involves chance, use the synchronised random
number generator.

## 5. The AI

- **Borrowing and lending:** in `CvPlayerAI::AI_doTurnPost` (543) or `AI_doCommerce` (16250), where the
  sliders are set. Borrow when `AI_isFinancialTrouble` (4112) is true; lend when gold is above
  `AI_goldTarget` (4199).
- **Offering loans** to other players: `AI_doDiplo` (16949).
- **Counting debt.** `AI_isFinancialTrouble` is called from many places. If it does not count loan
  payments, the AI borrows its way into strikes.
- **Judging it.** AI changes are judged by the seeded experiment of `method/docs/framework.md` (section 7),
  and each code commit names a registered prediction (CLAUDE.md, rules 9 and 10).

## 6. UI

- **Python access.** Screens see only what is exposed: getters on `CyPlayer` (CyPlayer.cpp and the
  `.def` lines in CyPlayerInterface1.cpp and CyPlayerInterface2.cpp) and on `CyGame` (CyGameInterface.cpp).
- **Finance advisor.** The mod uses `Python/Screens/BugFinanceAdvisor.py`, chosen in
  `Python/EntryPoints/CvScreensInterface.py` (116–126).
  - Add a "Debt payments" row among the expense rows in `drawContents` (394–422: unit cost, maintenance,
    civics, inflation) and an "Interest received" row by the income from other civilizations (380).
  - With the BUG option off, the base game's `CvFinanceAdvisor.py` is used; changing it means copying it
    into the mod.
- **Tooltips.** Each finance row has a `WIDGET_HELP_FINANCE_*` widget, handled in
  `CvDLLWidgetData::parseHelp` (441–491), with its text built in `CvGameTextMgr::buildFinance*String`
  (15645–15821). Add `WIDGET_HELP_FINANCE_DEBT` at the end of `WidgetTypes` (RoM already adds its widget
  types there; never in the middle, the exe uses the numbers), a case in `parseHelp` and a
  `buildFinanceDebtString`.
- **Market screen.** A new Python screen: an id in `Python/Screens/CvScreenEnums.py`, a show function and
  an input-handler entry in `CvScreensInterface.py`, and buttons with `WIDGET_GENERAL` whose input handler
  sends the network message of section 4. Open it from a button on the finance advisor.
- **Text.** New `TXT_KEY` entries in the mod's `XML/Text`.
- **Events** for Python mods (loan taken, default), if wanted: through `CvEventReporter` and
  `CvDllPythonEvents`.

## A quick mock-up

The Python hooks `doGold` and `getExtraCost` exist but are off (`XML/PythonCallbackDefines.xml`). A
mock-up can use them. `getExtraCost` sits on the hot path of section 1 and was switched off for turn time,
so it is good for a mock-up only.
