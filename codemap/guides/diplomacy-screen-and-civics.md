# How the diplomacy screen works, and who chooses the civics

Source: GitLab branch `Graphics-Paging-Fix-Test` at `1d9a473`; line numbers refer to it. Calls inside the DLL
come from the code map (`query.py`, `impact.py`). Calls from the exe cannot be seen in the source: where
the exe is involved, this says only which DLL functions the exe can call (exported, or virtual in
`CvPlayer`) and what they do. The order in which the exe calls them is inferred from what they return, and
marked as such.

## Part 1. The diplomacy screen

### 1.1 Who draws what

The diplomacy screen has three owners:

| part | owner | where |
|---|---|---|
| The window: leader animation, the two trade columns, the comment list, the buttons | the exe | not in the source |
| The player's reply options under each AI comment | Python | `Assets/Python/CvDiplomacy.py` (751 lines) |
| Everything the screen shows or decides about the game | the DLL | exported functions below |

**Python's part.** `CvDiplomacy.determineResponses` (CvDiplomacy.py:29) maps each AI comment to the user
comments offered. For example:
- `AI_DIPLOCOMMENT_OFFER_DEAL` offers accept, renegotiate or reject (lines 75–84);
- `AI_DIPLOCOMMENT_TRADING` offers propose, demand, ask, gift and "what would make this deal work" (lines
  154–228).

The mod's file differs from the BTS file (`Python (2)/CvDiplomacy.py`) by one RevolutionDCM option, "do not
bother us" / "resume talks" (lines 307–315). Python makes no game decision on this screen.

**The DLL's part.** All functions below are exported (`map/functions.tsv`, column `exported`) or pure
virtual in `CvPlayer` (CvPlayer.h:1203–1232), so the exe reaches the `CvPlayerAI` versions through the
vtable.

| step | DLL function | what it does |
|---|---|---|
| Can we talk? | `CvPlayer::canContact` | contact, war-weariness and "refuses to talk" rules |
| Fill each column | `CvPlayer::buildTradeTable` (CvPlayer.cpp:23774–23974) | one `TradeData` per item the player could ever trade with the other: gold, gold per turn, maps, vassal, open borders, pacts, techs, resources, cities, peace/war/embargo, civics, religion; each tested with `canTradeItem` |
| Grey out or mark items | `CvPlayer::updateTradeList` (24181–24273), `canTradeItem` (5413–5725), `getTradeDenial` (5729–5803) | which items are offerable now; the red "We don't want to…" reasons are `DenialTypes` |
| Label items | `getHeadingTradeString` (23977–24020), `getItemTradeString` (24024–24178) | text and icon of each heading and item |
| Limits of the gold boxes | `CvPlayerAI::AI_maxGoldTrade` (CvPlayerAI.cpp:9724–9754), `AI_maxGoldPerTurnTrade` (9758–9778) | how much gold or gold per turn the player can put in |
| AI answers a proposal | `CvPlayerAI::AI_considerOffer` (8989–9128, virtual) | accept or refuse |
| "What would make this work?" | `CvPlayerAI::AI_counterPropose` (9131–9720, virtual) | adds items to either side until the AI accepts |
| Deal made | `CvGame::implementDeal` (CvGame.cpp:3487–3501) → `CvDeal::addTrades` → `CvDeal::startTrade` (CvDeal.cpp:696–1094) | items move; annual items start |
| Replies to AI requests | `CvPlayer::handleDiploEvent` (CvPlayer.cpp:5137–5349) | 23 `DIPLOEVENT_*` cases: accept a demand, join a war, convert, change civics … |
| Help text | `CvGameTextMgr::getTradeString`, `getDealString`, `getAttitudeString`, `setTechTradeHelp`, `setBonusTradeHelp` | tooltips |

**AI-initiated contact.** `CvPlayerAI::AI_doDiplo` (CvPlayerAI.cpp:17345–19308) builds a
`CvDiploParameters` with a comment and the two offer lists, and hands it to the exe with
`gDLL->beginDiplomacy` (52 places in CvPlayerAI.cpp). Between AIs, the same function implements deals
directly with `implementDeal`.

**Reading (call order):** for each player, the exe calls `buildTradeTable` once when the screen opens, then
`updateTradeList` after each change. When the human presses "propose" it calls `AI_considerOffer`.
- *Rests on:* the arguments: `updateTradeList` takes both current offers.
- *Would contradict it:* a trace of the exe. **Open**; it does not change anything below.

### 1.2 The items are fixed by the exe

`TradeableItems` (CvEnums.h:1951–1986) has 16 values, from `TRADE_GOLD` to `TRADE_RELIGION`. Two counts
exist only when the DLL is compiled (`#ifdef _USRDLL`): `NUM_BASIC_ITEMS` and `NUM_TRADEABLE_HEADINGS`. The
exe was compiled without them.

**Reading:** the exe walks the headings with its own fixed count, 16. A 17th item would not get a heading in
the trade window.
- *Rests on:* the `#ifdef`. The exe's header has no count, so its loop bound is a number compiled into the
  exe.
- *Would contradict it:* a test build adding `TRADE_LOAN` at the end and seeing a heading appear.
- **Open** until that test. This decides route B of the debt plan (`loans-and-bonds.md`, section 4).

### 1.3 How the AI values a proposal (at 1d9a473)

For a new deal, `AI_considerOffer` compares two values:
- **what it receives:** `AI_dealVal(ePlayer, theirList)`;
- **what it gives:** `AI_tradeGiveVal(ePlayer, ourList)`. This is the recipient's value of each item, except
  that a resource counts as the AI's own loss, gold at the AI's own gold percent, and gold per turn at
  `AI_goldPerTurnCostVal`.

Attitude, war and "we fear you" rules come before this comparison. The counter-proposal adds items, then
checks the whole package with `AI_isMutuallyBeneficialDeal` when it contains a resource, gold or gold per
turn. Details and the switch problem are in `test-branch-1d9a473.md`, part 2b.

**What the AI does not see:**
- **Time.** Gold per turn is valued as `PEACE_TREATY_LENGTH` turns of payments (`AI_goldPerTurnTradeVal`,
  CvPlayerAI.cpp:9782–9787). `PEACE_TREATY_LENGTH` is 10 (GlobalDefines.xml:761) and is not scaled by game
  speed. `CvDeal::doTurn` spreads each deal's value over the same 10 turns for attitude (CvDeal.cpp:305, 319).
- **Commitment.** Either side can cancel an annual deal once `turnsToCancel` reaches 0 (CvDeal.cpp:1299–1301:
  `initialTurn + PEACE_TREATY_LENGTH − gameTurn`). `CvDeal::verify` (335–383) ends deals whose resource is
  gone. War ends all deals between the teams (CvTeam.cpp:1443–1450). An AI re-tests its own deals each turn
  with `AI_considerOffer(…, -1)` (CvPlayerAI.cpp:17425, 17446) and cancels them when they fail.
- **Credit.** A promise to pay later carries no risk and no price, because no promise outlives a war or a
  cancellation.

### 1.4 What could be improved, and on what evidence

These are readings. Each would be a change judged by the seeded experiment of `method/docs/framework.md`
(section 7) and would need a registered prediction (CLAUDE.md, rule 10).

1. **Restore the switch contract.** Put the 1d9a473 valuation under a new bit of `AI_DIPLOMACY_FLAGS`, so the
   old AI can serve as the baseline in the same DLL.
2. **Positive net for AI–AI deals.**
   - *Rests on:* `CvDeal::doTurn` (CvDeal.cpp:298–331) turns every non-peace deal's value into
     `AI_changePeacetimeTradeValue`, which raises attitude. A deal of net value 0 still earns attitude.
   - *Change:* require a net value above 0 between AIs.
3. **Annual items valued over the term actually expected.**
   - *Rests on:* the deal is cancellable after `PEACE_TREATY_LENGTH`, so the expected life of an annual item
     depends on the partner's attitude and war risk. The AI uses a constant instead.
   - *Change:* use the expected life, from the attitude and war-plan data the AI already keeps
     (`AI_getAttitudeVal`, CvPlayerAI.cpp:7387–7518).
4. **Commitments that survive.** A term on a deal (no cancellation before maturity) is the prerequisite for
   loans. It is the first step of the debt plan.

## Part 2. Who chooses the civics

### 2.1 What the code does

`CvPlayerAI::AI_doCivics` (CvPlayerAI.cpp:17135–17221), once per turn for an AI player:

1. It returns while the civic timer runs, or while `canRevolution` is false.
2. It scores every civic the player can adopt with `AI_civicValue`, once each, and keeps the best per civic
   option.
   - The eight civic options are Leadership, Administration, Taxation, Economy, Employment, Education,
     Religion and Military (`XML/GameInfo/CIV4CivicOptionInfos.xml`).
3. It sums the current package and the best package.
4. It switches when `AICivicPolicy::shouldSwitch` (AICivicPolicy.h:63–78) holds:
   `(best − current) × horizon > current × anarchyTurns + current × horizon × threshold / 100`.
   - The horizon is `2 × range(AI_CIVIC_CHANGE_DELAY, 6, 500)`. `AI_CIVIC_CHANGE_DELAY` is 12
     (GlobalDefinesAlt.xml:845–846), so the horizon is 24 turns.
   - The threshold is `AI_CIVIC_SWITCH_THRESHOLD_PERCENT`, 5 (line 849–850), plus 13 during anarchy outside
     a golden age.
5. After a revolution, the civic timer is set from `MIN_REVOLUTION_TURNS` (5, GlobalDefines.xml:768–769) and
   `AI_CIVIC_CHANGE_DELAY`.

`AI_civicValue(eCivic)` (13303–14107, about 800 lines) is a method of the player. Everything it reads belongs
to the whole empire:
- the empire's cities and yields;
- its war plans (`AI_getWarPlan`);
- its trade routes and foreign connections;
- state religion and religion counts;
- the number of military units;
- victory strategies.

Money enters in three places:
- **Upkeep:** `−getSingleCivicUpkeep(eCivic, true) × 80 / 100` (offset 139 in the function). Upkeep is
  computed from total population and the civic's upkeep type (CvPlayer.cpp:14177–14257).
- **"Upgrade anywhere":** doubled when `getGold() + 10 × calculateBaseNetGold()` exceeds
  `50 + 100 × era` (offset 266–268).
- **Unlock values:** gold above `AI_goldTarget` (offset 750).

The leader's personality enters once: the leader's favourite civic (`CvLeaderHeadInfo::getFavoriteCivic`)
gets ×5/4 plus 6 per city plus 20 (offset 776–786).

**Not read:** the civics' Revolution stability fields (`getRevIdxLocal`, `getRevIdxNational`, … in
CvInfos.h:1688–1696). Only the Revolution Python reads them (`Python/Revolution/RevCivicsUtils.py:73` and
following).

### 2.2 The answer

**Civics are chosen from the perspective of the whole civilization:** one `CvPlayerAI` object, one treasury
(`CvPlayer::m_iGold`), one score per civic.
- There is no government actor separate from the civ.
- There is no budget of a government: no account that civic upkeep is paid from, and no account that limits
  what a regime can spend.
- The Leadership option (despotism, monarchy, republic …) is valued by the same function, on the same
  empire-wide figures, as every other option.
- The leader's personality appears only as the favourite-civic bonus and through `MaxWarRand` in the war
  plan check (offset 129).

**Reading:** this is a state-as-unitary-actor model. The civics are policies the state picks for its own
benefit, not the choices of a ruling group with its own interests.
- *Rests on:* 2.1. Nothing in the scoring asks who benefits inside the empire. The Revolution component
  models internal discontent, but the AI ignores its civic fields when choosing.
- *Would contradict it:* a code path where civic choice reads a per-group or per-faction quantity. None is
  in `AI_civicValue`, and the graph shows no caller of `getRevIdx*` in the DLL's AI.

**Reading:** each civic is scored independently, against the current civics.
- *Rests on:* step 2 above, one `AI_civicValue` call per civic. Interactions are therefore valued against the
  current package. `AI_civicValue` does replace the current civic of the option when projecting yields
  (offset 374–378), but does not replace other options' civics.
- *Would contradict it:* a package-level score. There is none.

**What a "government with its own budget" would take** (only if the user wants it; not part of this plan):
- a per-player ruling-group account in `CvPlayer`;
- civic upkeep and some incomes routed to it;
- `AI_civicValue` given a term for the group's account.

The debt plan below keeps a single treasury. Debt is owed by the civilization.
