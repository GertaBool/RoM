# RoM DLL: AI Diplomacy and Trade Code Map

Source: GitLab `main` 93ae873 (merge of !38, the same tree as the tested commit 7f72bd4, i.e. with patch 0013), `Assets/CvGameCoreDLL`.
Paths without a directory are relative to that folder. XML paths are relative to `Assets/XML`.
All line numbers were re-checked against the current tree. Patch 0013 only touches
`CvPlayerAI.cpp` from line 13040 on (AI_civicValue, AI_disbandUnit). None of the code below changed.

Conventions used in this report:
- "giver" is the player who hands an item over. "receiver" is the player who gets it.
- `AI_dealVal(eOther, list)` returns the value **to the calling player** of **receiving** `list` from `eOther`.
- "value points" (vp) is the unit used by AI_dealVal.

---------------------------------------------------------------------------------------------------

## 0. Summary of the most important facts

1. In any trade involving an AI, the trade screen will not mix annual and one-shot items. Annual items are
   resources, gold per turn (GPT), open borders, defensive pact, permanent alliance and vassal items.
   One-shot items are gold, tech, maps and cities. A city also has to be the only item in the deal unless
   it is part of ending a war. This one rule in `CvPlayer::updateTradeList` (CvPlayer.cpp:24220-24244)
   blocks "lump-sum gold or tech for a resource" and "pay for a liberation". Because AI_counterPropose
   skips items marked hidden, the rule binds the AI's counter-proposals as well.
2. When the AI proposes a deal to another AI, the partner is never asked to evaluate it. AI_doDiplo and
   AI_doPeace check the partner's denials and then call `implementDeal` directly. The partner's
   `AI_considerOffer` is only used when a human makes the offer.
3. The AI only ever starts these deal shapes:
   - tech for tech, gold or nothing
   - resource for resource
   - map for map
   - OB for OB, DP for DP, PA for PA
   - peace plus tech, gold or a city
   - tech plus gold to hire a war
   - free liberation gifts of cities
   - vassal offers
   - tribute demands made to humans

   It never proposes GPT for a resource, lump-sum gold for a resource, a tech for a resource, or selling a
   tech for gold.
4. Several valuations ignore game speed: PEACE_TREATY_LENGTH=10, at-war counters, the 20-turn cadence of
   city offers, and per-turn memory decay. Other valuations grow with the turn count instead: has-met
   counters, elapsed turns and game turn. In RoM a game runs at anything from 40% to 700% research speed.
5. There are verified defects (section 6). The main ones:
   - Several products of team power overflow 32-bit ints in mid to late game RoM.
   - Peace deals price gold 1:1 while AI_dealVal prices it at 2-3 vp per gold.
   - When the AI proposes a resource swap to a human, it values the resource it receives with the wrong
     sign, so it undervalues it about 5x.
   - The second tech chosen for a war-hire deal is picked with the wrong comparison variable.
   - Two attitude thresholds are read from the human's leader instead of the AI's own.
   - The attitude cache is not invalidated when memories change or gifts are received.

---------------------------------------------------------------------------------------------------

## 1. Deal machinery

### 1.1 Types

| Item | Where | Notes |
|---|---|---|
| `TradeableItems` | CvEnums.h:1951-1985 | Gold, GPT, maps, vassal, surrender, OB, DP, PA and peace treaty are "basic items". They come before `NUM_BASIC_ITEMS`, which is only defined under `_USRDLL`. From `TRADE_TECHNOLOGIES` on the items are "headings" with sub-items: tech, resources, cities, peace (broker), war, embargo, civic, religion. |
| `TradeData` | CvStructs.h:69-75 | `{TradeableItems m_eItemType; int m_iData; bool m_bOffering; bool m_bHidden;}`. It is DllExport and shared with the EXE. CLinkList writes it as raw `sizeof(T)` bytes (LinkedList.h:386-396), so its layout must stay fixed. |
| `DenialTypes` | CvEnums.h:1289-1321 | DENIAL_NEVER, TOO_MUCH, MYSTERY, JOKING, ATTITUDE, ATTITUDE_THEM, TECH_WHORE, TECH_MONOPOLY, POWER_*, TOO_MANY_WARS, NO_GAIN, NOT_ALLIED, RECENT_CANCEL, WORST_ENEMY, TOO_FAR, VASSAL, WAR/PEACE_NOT_POSSIBLE_* |
| `ContactTypes` | CvEnums.h:2041-2059 | 14 types. Names come from `GlobalTypes.xml` ContactTypes (CvXMLLoadUtilitySet.cpp:537). |
| `MemoryTypes` | CvEnums.h:2061-2107 | 34 types, including RoM's `MEMORY_INQUISITION`. They are listed in `BasicInfos/CIV4MemoryInfos.xml`. |
| `setTradeItem()` | CvGameCoreUtils.h:281 | DllExport helper. |

### 1.2 Per-item behaviour

Column key:
- "A/D/H" means `CvDeal::isAnnual` / `isDual` / `hasData` (CvDeal.cpp:1299-1343).
- "Saved" means `startTrade` returned true, so the node stays in the CvDeal.

| Item | m_iData | A/D/H | startTrade (CvDeal.cpp) | Saved | endTrade | Denial function | AI valuer |
|---|---|---|---|---|---|---|---|
| GOLD | amount | -/-/H | 779-800 moves gold and calls `AI_changeGoldTradedTo` | no | assert | none | `m_iData*AI_goldTradeValuePercent/100` (CvPlayerAI.cpp:8851) |
| GOLD_PER_TURN | amount | A/-/H | 802-820 calls changeGoldPerTurnByPlayer for both sides | yes | reverses it | none | `AI_goldPerTurnTradeVal` (9675) |
| MAPS | - | -/-/- | 822-856 reveals plots and updates plot groups | no | assert | `CvTeamAI::AI_mapTrade` (CvTeamAI.cpp:1977) | `AI_mapTradeVal` (CvTeamAI.cpp:1930) |
| VASSAL / SURRENDER | 0 = lead, 1 = team copy | A/-/- | 858-890 calls `startTeamTrade` and `setVassal` | copy only | `setVassal(false)` + `endTeamTrade` | `AI_vassalTrade` 2034 / `AI_surrenderTrade` 2098 | `AI_vassalTradeVal`/`AI_surrenderTradeVal` both **return 0** (2026, 2090-2094) |
| OPEN_BORDERS | 0 = lead, 1 = copy | A/D/- | 1015-1037 calls `startTeamTrade` and `setOpenBorders` | copy only | 1142-1168 clears OB and adds `MEMORY_CANCELLED_OPEN_BORDERS` | `AI_openBordersTrade` 3408 | `AI_openBordersTradeVal` 3402 = cities(us) + cities(them) |
| DEFENSIVE_PACT | same | A/D/- | 1039-1061 | copy only | 1170-1176 | `AI_defensivePactTrade` 3468 | `AI_defensivePactTradeVal` 3462 = 3*(sum of cities) |
| PERMANENT_ALLIANCE | - | A/D/- | 1063 does nothing; `addTrades` calls `addTeam` (282-292) | no | assert | `AI_permanentAllianceTrade` 3512 | **no case in AI_dealVal**, so it is worth 0 |
| PEACE_TREATY | - | -/D/- | 1066-1081 `setForcePeace` | yes | 1182-1184 | none (always NO_DENIAL) | not itemised. `AI_endWarVal` is added to the whole list when at war (CvPlayerAI.cpp:8823-8826) |
| TECHNOLOGIES | tech | -/-/H | 706-739 `setHasTech` + `setNoTradeTech(true)`, plus MEMORY_TRADED_TECH_TO_US and MEMORY_RECEIVED_TECH_FROM_ANY | no | assert | `CvTeamAI::AI_techTrade` 1728 | `CvTeamAI::AI_techTradeVal` 1675 |
| RESOURCES | bonus | A/-/H | 741-757 export/import | yes | 1102-1105 | `CvPlayerAI::AI_bonusTrade` 10116 | `AI_bonusTradeVal` 10093 |
| CITIES | city id (giver) | -/-/H | 759-777 `doTask(TASK_GIFT)`, which liberates if the receiver is the liberation player (CvCity.cpp:1457-1466) | no | assert | `AI_cityTrade` 10280 | `AI_cityTradeVal` 10232 |
| PEACE (broker) | team | -/-/H | 892-906 `makePeace` | no | assert | `CvTeamAI::AI_makePeaceTrade` 3101 | `AI_makePeaceTradeVal` 3041 |
| WAR | team | -/-/H | 908-933 `declareWar`, plus MEMORY_HIRED_WAR_ALLY | no | assert | `AI_declareWarTrade` 3278 | `AI_declareWarTradeVal` 3143 |
| EMBARGO | team | -/-/H | 935-960 `stopTradingWithTeam`, plus MEMORY_HIRED_TRADE_EMBARGO | no | assert | `AI_stopTradingTrade` 10433 | `AI_stopTradingTradeVal` 10336 |
| CIVIC | civic | -/-/H | 962-992 `revolution`, civic timer >= 10 | no | assert | `AI_civicTrade` 10531 | `AI_civicTradeVal` 10496 |
| RELIGION | religion | -/-/H | 994-1013 `convert`, religion timer >= 10 | no | assert | `AI_religionTrade` 10616 | `AI_religionTradeVal` 10581 |

How team-level items propagate (`m_iData` convention): the deal's lead item carries `m_iData == 0`. `startTeamTrade`
(CvDeal.cpp:1192-1224) then creates one extra deal per pair of team members, each carrying `m_iData = 1`, and those
copies are the ones that are saved. `endTeamTrade` (1226-1272) kills the sibling deals. `assignVassal` (CvTeam.cpp:5120)
uses the same convention. Any new team-level item (for example split borders) has to follow it, or `m_iData` has to
be repurposed, for example as a subtype plus a flag bit.

### 1.3 Deal lifecycle

1. `CvGame::implementDeal(eWho, eOther, pOur, pTheir, bForce)` (CvGame.cpp:2618) calls `addDeal`, `init` and
   `addTrades(pOur, pTheir, !bForce)`. If both saved lists are empty afterwards, the deal is killed at once,
   because one-shot items leave no record.
2. `CvDeal::addTrades` (CvDeal.cpp:118-293):
   - It rechecks `canTradeItem` (validity only, with no denial check) for every item when `bCheckAllowed` is set.
   - If the two sides are at war, it frees the capitulating side's vassals and calls `makePeace`. Any deal
     between warring parties therefore implies peace.
   - Otherwise it credits `AI_changePeacetimeTradeValue` (both sides gave something) or
     `AI_changePeacetimeGrantValue` (one side gave nothing). The value credited is
     `AI_dealVal(..., bIgnoreAnnual=true)`, so annual items count 0 at this point.
   - It then calls `startTrade` for each item.
3. `CvDeal::doTurn` (296-330): for non-peace deals it credits `AI_dealVal(saved items)/PEACE_TREATY_LENGTH`
   each turn as trade or grant value. `CvGame::doDeals` (CvGame.cpp:6057) runs `verifyDeals` and then `doTurn`.
4. `CvDeal::verify` (334-383):
   - It kills resource deals whose bonus has run out, has gone obsolete, or is no longer connected.
   - It kills peace deals once they become cancelable, that is after 10 turns.
   - It never checks whether a GPT payer can still afford the payments.
5. `isCancelable` / `turnsToCancel` (1274-1296): the deal is locked for `PEACE_TREATY_LENGTH` (10) turns from
   `m_iInitialGameTurn`, regardless of game speed. Vassal deals are never cancelable by the master
   (`isUncancelableVassalDeal` 431-508).
6. `kill` (77-115) calls `endTrade` for every saved node, then `deleteDeal`.
7. `CvTeam::declareWar` (CvTeam.cpp:1406, deal-kill loop at 1440-1448) kills **all** deals between the two
   teams, OB included.
8. Saving: `CvDeal::write/read` (661-689) writes `uiFlag=0`, ID, start turn, both players and both lists as raw
   TradeData. `CvGame` streams `m_deals` (CvGame.cpp:8409/8637).

### 1.4 canTradeItem / getTradeDenial (CvPlayer.cpp)

`canTradeItem` is at 5411. With `bTestDenial` it returns `validity && getTradeDenial()==NO_DENIAL` (5418-5421).
Validity rules for each item:
- **TECH** (5425): the tech is tradeable, we have it and it is not `NoTradeTech` (5430), they lack it, either team
  has tech trading, and they `canResearch(tech, bTrade=true)`.
- **RESOURCES** (5452): our trade network connects to them, the bonus is not obsolete for either side, and
  `getNumTradeableBonuses > (bCanTradeAll ? 0 : 1)` (5459). An AI therefore always keeps its last copy unless the
  receiver is a teammate or its master.
- **CITIES** (5471): if the receiver is the city's liberation player, the trade is valid immediately (5475).
  That path skips the vassal, capital and max-city-elimination checks. Otherwise the receiver must be able to
  receive cities, `getMaxCityElimination()==0`, the giver must not be a vassal, the receiver must not be the
  giver's vassal, and the city must not be the capital.
- **GOLD** (5500): gold trading is available and `getGold() >= m_iData`. **GPT** (5510): only the gold-trading tech
  is required. There is no limit on the amount.
- **VASSAL/SURRENDER** (5527): human-to-AI is gated by `BBAI_HUMAN_AS_VASSAL_OPTION` (5534). Surrender requires war
  (or `m_iData==1`). Vassal requires peace.
- **PEACE / WAR / EMBARGO** (5559/5575/5594): only a **non-human** giver can trade these. A human can therefore
  hire an AI, but an AI can never hire a human through a deal.
- **CIVIC / RELIGION** (5607/5634): non-human givers only, unless both players are on the same team.
- **OB** (5658): not at war and no OB yet. **DP** (5674): neither side is a vassal, neither is at war with anyone,
  and `canSignDefensivePact`. **PA** (5699): one-member teams only. **PEACE_TREATY** (5718): always valid.

`getTradeDenial` (5727-5802) only dispatches, to the denial functions listed in the table in 1.2.
Gold, GPT and peace treaty never return a denial.

### 1.5 Trade-screen hooks (DllExport, called by the EXE)

- `buildTradeTable` (CvPlayer.cpp:23746): builds the list of tradeable items. Basic items go in directly. For
  headings it loops `NUM_BASIC_ITEMS..NUM_TRADEABLE_HEADINGS`.
- `getHeadingTradeString` (23949) and `getItemTradeString` (23996): the display strings. A liberation city is
  shown as "(Liberate)" (24077).
- `updateTradeList` (24153-24252) sets `m_bHidden`:
  - It hides the peace treaty and surrender when the sides are not at war, and hides techs under no-tech-trading.
  - It handles hiding between vassal items and end-war items.
  - **The mixing rule** (24220-24244) applies whenever either side is an AI:
    - If the first offered item is not an end-war item, or the sides are not at war, then every inventory item
      whose `isAnnual()` differs from the first item's is hidden.
    - Every city is hidden unless the first item is itself a city. If the first item is a city, everything else
      is hidden.

### 1.6 Who evaluates what

- **Human proposes to AI:** the EXE calls `AI_considerOffer(human, theirList, ourList)` (virtual, CvPlayer.h:1206).
  "What would make this work?" calls `AI_counterPropose` (CvPlayer.h:1207).
- **AI proposes to human:** a `CvDiploParameters` dialog is opened through `AI_beginDiplomacy` (CvPlayerAI.cpp:16859)
  and the human decides. Python `CvDiplomacy.py:66-125` maps each comment to the user's response options.
- **AI proposes to AI:** the proposer calls `canTradeItem(.., true)` on both sides and then `implementDeal`. The
  partner's `AI_considerOffer` is never called. The only exception is surrender: `AI_acceptSurrender` is checked in
  AI_doPeace at line 960. See D14.
- **Vassal tribute:**
  - A human master demands from an AI vassal: popup, then `AI_considerOffer` (CvDLLButtonPopup.cpp:652-685).
  - An AI master takes from an AI vassal: `implementDeal` with no consent at all (CvPlayerAI.cpp:17271-17312).
- **Virtual layout constraint:** `AI_dealVal`, `AI_considerOffer`, `AI_counterPropose`, `AI_maxGoldTrade` and
  `AI_maxGoldPerTurnTrade` are pure virtuals in `CvPlayer` (CvPlayer.h:1205-1242) and the EXE calls them through the
  vtable. Do not reorder them or change their signatures.

---------------------------------------------------------------------------------------------------

## 2. AI valuation

### 2.1 AI_dealVal (CvPlayerAI.cpp:8813-8899)

```
value = (atWar ? GET_TEAM(us).AI_endWarVal(them) : 0) + sum over items of item value
```
- `bIgnoreAnnual` skips RESOURCES, GPT, SURRENDER and VASSAL. It is used at deal start (CvDeal.cpp:205/218).
- `iChange` is passed to `AI_bonusTradeVal`:
  - +1: gaining a copy (the default)
  - -1: valuing a copy we already hold. AI_doDiplo uses this when it re-checks existing deals.
- There is no case for PERMANENT_ALLIANCE or PEACE_TREATY.
- The default argument differs between declarations: `CvPlayer.h:1205` uses `iExtra=0`, `CvPlayerAI.h:294` uses
  `iExtra=1`. See D19.

### 2.2 Per-item valuers

| Valuer | Location | Formula (summary) | Speed scaling |
|---|---|---|---|
| `AI_techTradeVal(tech, eTeam)` | CvTeamAI.cpp:1675-1725 | `1.5*(cost-progress) + 0.5*cost*(share of met teams lacking it)`, times `AITradeModifier`, rounded down to a multiple of 10 | Yes, through the research cost |
| `AI_bonusTradeVal(b, ePlayer, iChange)` | CvPlayerAI.cpp:10093-10113 | `AI_bonusVal(b,iChange)*(min(cities)+3)*30/100*(AITradeModifier+100)/100`, halved for a non-capitulated vassal, **times PEACE_TREATY_LENGTH (10)** | No |
| `AI_bonusVal(b, iChange)` | 9684-9701 | `base+corp` for the 0-to-1 or 1-to-0 case, otherwise `base/5 + corp` (marginal copy) | - |
| `AI_goldTradeValuePercent()` | 22366-22374 | 200, or 300 when `AI_isFinancialTrouble` | No |
| `AI_goldPerTurnTradeVal(gpt)` | 9675-9682 | `gpt*10*goldPercent/100` (10 turns) | No |
| `AI_cityTradeVal(city)` | 10232-10277 | `300 + 50*pop + 200*cultureLevel + 4*(50*pop + elapsedTurns + 100)*ownerCulture%`, plus `10*bonusVal` for each bonus in the fat cross, times 1.5 if the receiver never owned it. Buildings, wonders and production are ignored. | Grows with elapsed turns (10246) |
| `AI_mapTradeVal(eTeam)` | CvTeamAI.cpp:1930-1974 | (unrevealed land*5 + water)/10, halved for a vassal | No |
| `AI_openBordersTradeVal` | CvTeamAI.cpp:3402-3405 | cities(us) + cities(them) | Trivially small |
| `AI_defensivePactTradeVal` | 3462-3465 | 3*(cities(us) + cities(them)) | Trivially small |
| `AI_endWarVal(eTeam)` | CvTeamAI.cpp:1361-1530 | `(100 + 3*cities(both) + pop(both) + 20*theirWarSuccess) * (theirPow+10)/(ourPow+theirPow+10)`, then modifiers for dagger, land ratio, finance, victory strategy, TOTAL (x2) and DOGPILE (x1.5) war plans, and attacker ratio | No (see D5 for overflow) |
| `AI_makePeaceTradeVal` | 3041-3098 | `(50+gameTurn+8*cities)*(attitude modifier)*40/(atWarCounter+10)` | Grows with the turn number |
| `AI_declareWarTradeVal` | 3143-3275 | cities, pop, attitude, power, nukes, DP allies of the target, and `*(60+140*turn/estimateEndTurn)%` | Partly |
| `AI_stopTradingTradeVal` | CvPlayerAI.cpp:10336-10430 | `50+turn/2+5*cities`, attitude, x2 with OB, x3 with DP, plus the value of the giver's existing deals (see D7) | Partly |
| `AI_civicTradeVal` / `AI_religionTradeVal` | 10496 / 10581 | 2 or 3 times the combined population, plus the receiver's civic or religion value gap | No |
| `AI_vassalTradeVal` / `AI_surrenderTradeVal` | CvTeamAI.cpp:2026/2090 | **0** | - |

The valuation model is "our cost equals their gain". The value of anything the AI gives away is computed by
**the receiver's** valuer. The AI's own loss is never priced, apart from the denials:
- tech monopoly in `AI_techTrade`, which uses `AI_getTechMonopolyValue`
- keeping the last copy of a resource
- `DENIAL_NEVER` for cities

It also never prices the relative gain to a rival.

### 2.3 AI_considerOffer (CvPlayerAI.cpp:8927-9062)

Steps in order:
1. If both sides contain gold or GPT, reject (8934).
2. If `iChange > -1`, any denial on our items means reject (8939-8948). The deal-cancellation check calls it with
   `iChange = -1` and skips this step.
3. Same team: accept.
4. Vassal and surrender offers. TRADE_VASSAL requires `AI_declareWarTrade(.., false)==NO_DENIAL` against each of
   their enemies. TRADE_SURRENDER requires `AI_acceptSurrender`.
5. If this is not a vassal trade and the AI gives nothing, accept (8993-8999). The AI accepts any gift.
6. `iOurValue = them.AI_dealVal(us, ourList)` and `iTheirValue = AI_dealVal(them, theirList)` (9004-9005).
7. **Gift / demand branch** (9007-9054): we give something, they give nothing.
   - We are their vassal and the list is tribute: if attitude is at or below `VassalRefuseAttitudeThreshold`, we
     are at peace with everyone and the master has no DP, scale iOurValue by the power ratio (D5 site 9015).
     Otherwise accept.
   - Otherwise reject if attitude is below PLEASED and we have more than 4/3 of their power, or if they hold
     `MEMORY_MADE_DEMAND_RECENT`.
   - `threshold = 2*(hasMetCounter+50)`, times 3 if we are their land target, times
     `(theirPow+100)/(ourPow+100)` (D5 site 9048), minus the grant value they already received from us.
     Accept if `iOurValue < threshold`.
8. If `iChange < 0` (re-evaluating an existing deal): accept if `iTheirValue*110 >= iOurValue*100` (9058).
9. Otherwise accept if `iTheirValue >= iOurValue` (9061). There is no margin, and attitude has no effect on price;
   it only enters through denials.

### 2.4 AI_counterPropose (9065-9614)

- **Case 1: the human offers too little.** The AI adds items, in this order:
  1. at war, the human city with the best `AI_targetCityValue`
  2. gold, only if one gold amount covers the whole gap (9196)
  3. techs and resources (only resources the human has more than one of and that no corporation needs), even if
     this overshoots
  4. maps
  5. gold up to the human's maximum (9290)
  6. GPT, using a linear search (9309)
  7. any remaining resources
- **Case 2: the AI is getting more than it gives.** The AI adds its own items, never overshooting:
  1. at war, surrender (valued at 0, 9370) or a peace treaty, then a city
  2. gold, rounded down
  3. techs and resources
  4. maps
  5. gold, then GPT
- The gold conversions use `AIDiplomacyPolicy::goldForValueGap/valueFromGold/saturatingAdd` (AIDiplomacyPolicy.h),
  which are 64-bit-safe RoM helpers.
- Every inventory loop skips nodes marked `m_bHidden`, so the `updateTradeList` mixing rule also limits counter
  offers.

### 2.5 Gold limits

- `AI_maxGoldTrade` (9617-9648):
  - Human or teammate: all of its gold.
  - AI: `pop * (hasMet+10) * MaxGoldTradePercent/100 - goldTradedTo`, then capped by the RoM deficit reserve
    (`AIDecisionPolicy::goldAfterDeficitReserve`, 12 runway turns scaled by research%), by gold on hand, and
    rounded down to a multiple of 10. `AI_goldTradedTo` only ever grows.
- `AI_maxGoldPerTurnTrade` (9651-9672):
  - Human: `goldRate + gold/10`, then capped at `goldRate` (the gold term is dead, see D9).
  - AI: `pop*MaxGPTPercent/100 + min(0, existing GPT to this partner)`, capped at `goldRate`.
- XML values: `iMaxGoldTradePercent` is 5-20 (29 leaders at 5, 21 at 10). `iMaxGoldPerTurnTradePercent` is 10 for
  56 of 60 leaders (Civilizations/CIV4LeaderHeadInfos.xml).

### 2.6 What AI_doDiplo proposes (CvPlayerAI.cpp:16920-18712)

- Entry is `AI_doTurnPost` (561). There is a Python veto hook, `AI_doDiplo` (16964). BUG sets the default to False
  (Python/BUG/BugGameUtils.py:205).
- It runs two passes: AI partners first, then humans (16977).

| Section | Lines | Partner | Shape (AI gives / AI receives) | Value check | Contact timer |
|---|---|---|---|---|---|
| Re-check existing deals | 16985-17118 | all | cancels the deal | Human deals: `AI_considerOffer(-1)` (17008/17029). AI deals: denial of our items only (17014/17035). | none |
| Gift to teammate or vassal | 17124-17190 | same team or our vassal | resource / - | `their bonusVal(+1) > our bonusVal(-1)` | none |
| Tech gift to vassal | 17192-17262 | our vassal | tech / - | vassal's tech score below 90% of ours (17203) | none |
| Tribute from vassal | 17271-17312 | our vassal | - / resource | none. An AI vassal is never asked. | none |
| Liberation gift | 17317-17388 | anyone at peace, attitude CAUTIOUS or better | city / - | we must not have taken it from them; they own at least half of its plots; turn cadence `(acquired+4)%20` (17325) | none |
| Permanent alliance, else vassal offer | 17391-17505 | leader only | PA <-> PA, or vassal / - | none; vassal offers check that the master would fight our wars | human only |
| Religion, civic, join war, stop trading | 17507-17688 | humans | diplo comment, no deal | random roll | human only |
| Give help | 17690-17755 | weak human | tech / - | attitude above `NoGiveHelp` **of the human's leader** (D3) | yes |
| Ask for help | 17757-17825 | human with more than half our assets | - / tech | random roll (see D11) | yes |
| Demand tribute | 17827-18045 | human, power check | - / gold, map, tech or resource | attitude at or below `DemandTribute` **of the human's leader** (D3) | yes |
| Open borders | 18050-18100 | anyone, leader only | OB <-> OB | denials only | human only |
| Defensive pact | 18102-18150 | anyone, leader only | DP <-> DP | denials only | human only |
| Tech trade | 18152-18334 | anyone | random tech (or nothing) plus gold / random tech plus gold | AI-AI: each side must be within 2/3 of the other (18277). To a human: only if `ourValue >= theirValue`. | human only |
| Resource trade | 18337-18446 | anyone | spare resource / spare resource | AI-AI: **none**. To a human: `our bonusTradeVal(-1) >= their bonusTradeVal(+1)` (18403, D1). | human only |
| Map trade | 18448-18500 | anyone | map <-> map | AI-AI: none. To a human: `ourVal >= theirVal`. | human only |
| Hire war | 18502-18705 | AI with no wars | up to 2 techs plus gold / TRADE_WAR | `theirValue > 0.75*ourValue` (18668) | none |

Notes:
- **Contact timers** are only advanced in the human branches. Between AIs, the only rate limit on trades is the
  per-turn `getSorenRandNum(ContactRand)` roll. Typical ContactRand values are 5 for tech and bonus, 20 for OB and
  maps, and 80 for DP and PA (Civilizations/CIV4LeaderHeadInfos.xml).
- **Item selection** is random: the code takes the maximum of `1+rand(10000)` over all valid techs or resources.
  It does not pick by value, except in war hiring, which weights by research left.
- **Gold balancing** in tech and war-hire deals uses raw 32-bit arithmetic (18238, 18260, 18639, 18654) rather
  than the AIDiplomacyPolicy helpers.

### 2.7 AI_doPeace (CvPlayerAI.cpp:859-1213)

- It is called from `CvTeamAI::AI_doWar` (CvTeamAI.cpp:4722).
- It needs `canContact && AI_isWillingToTalk` on our side only (898), war lasting more than 10 turns (910, unscaled),
  and the contact timer.
- It first offers **surrender** when `canTradeItem(SURRENDER, true)` passes. For an AI partner it also requires
  `AI_acceptSurrender` (960).
- Otherwise it rolls `rand(ContactRand[PEACE])` (20 for 58 of 60 leaders) and builds a peace treaty:
  - Compute `iOurValue = our endWarVal` and `iTheirValue = their endWarVal`.
  - **If they want peace more**, ask for a random tech of theirs, then gold `min(gap, theirMax)` priced **1:1**
    (1018-1027, D4), then the city of theirs with our highest culture share.
  - **If we want peace more**, give a tech worth no more than the gap, gold 1:1 (1085-1094), and a city worth no
    more than the gap.
- Acceptance (1125): a human gets the offer only if `ourValue >= theirValue`. For an AI partner each side must be
  above 3/5 of the other.

### 2.8 Which deal shapes exist and which are generated

The "Allowed by UI vs AI" column reflects the `updateTradeList` rule.

| Shape | Allowed by UI vs AI | AI_counterPropose can build it | AI_doDiplo/AI_doPeace build it |
|---|---|---|---|
| tech <-> tech (+gold) | yes | yes | yes (AI-AI and to humans) |
| tech -> gold (AI buys a tech) | yes | yes | yes (when it has no tech to give) |
| gold -> tech (AI **sells** a tech) | yes | yes | **never**. The block only runs when there is a tech to receive (18208). |
| resource <-> resource | yes | yes | yes (AI-AI with no value check; to humans rarely, D1) |
| GPT <-> resource | yes (both annual) | yes | **never**. No `setTradeItem(TRADE_GOLD_PER_TURN)` exists anywhere in CvPlayerAI.cpp. |
| lump-sum gold <-> resource | **no** (annual and one-shot mixed) | no | never |
| tech <-> resource | **no** | no | never |
| maps <-> gold or tech | yes | yes | never; only map <-> map and tribute demands |
| OB/DP <-> anything except the same item | OB+DP yes; OB+gold no | no (it never adds OB or DP) | never |
| city <-> anything in peacetime | **no** (city must be alone) | no | never; only liberation gifts and peace or war deals |
| liberation request plus payment | **no** | no | never |
| brokered peace (TRADE_PEACE) | humans can ask the AI | no | never |
| embargo, civic or religion as deal items | humans can ask the AI | no | never; only free demands of humans through diplo comments |
| hiring a human for war | not possible (`canTradeItem` WAR requires a non-human giver) | - | only the CONTACT_JOIN_WAR comment, which carries no payment |

---------------------------------------------------------------------------------------------------

## 3. City trades and liberation

- **Liberation target:** `CvCity::getLiberationPlayer(bConquest)` (CvCity.cpp:15906-2015). It returns NO_PLAYER for
  a capital. It returns the owner's colony (`getParent()==owner`) if one exists in the same area; otherwise the
  split-empire player if the owner can split the area. Otherwise it picks the best of
  `max(100, culture)/capitalDistance`, where:
  - distance counts double across areas
  - the original owner gets x1.5 on conquest
  - teammates and vassals get bonuses

  It returns NO_PLAYER if the best candidate is the owner, or if that candidate can see enemy units in the city's
  radius.
- **Execution:** `CvCity::liberate` (15845-15903) calls `acquireCity(this,false,true,true)` and then:
  - **`MEMORY_LIBERATED_CITIES` is added to the receiver's memory of the liberator** (15876). This memory never
    decays and is worth +150% attitude per city for 58 of 60 leaders.
  - Vassal power bookkeeping.
  - Half of the old owner's culture is transferred.
  - Free defenders for a vassal colony.
- **Ways a city can be liberated:**
  - `TASK_GIFT` liberates automatically when the receiver is the liberation player (CvCity.cpp:1457-1461).
  - Human paths: the city screen's `TASK_LIBERATE` (CvDLLWidgetData.cpp:1153), the free-colony popup
    (CvDLLButtonPopup.cpp:2504-2570, not offered during war, 740), and the gift option in the raze popup after a
    conquest (CvPlayer.cpp:2886-2908, which needs OB with the liberation player or the same team or a vassal).
- **AI's own liberation behaviour:**
  - `AI_conquerCity` (1733) never liberates.
  - `AI_doSplit` (19712, called from AI_doTurnUnitsPost 851) splits off areas whose total `AI_cityValue` is
    negative.
  - The AI_doDiplo city section (17317-17388) offers a city **as a pure gift**. The AI-to-AI version is
    implemented without asking the receiver. `AI_cityTrade` returns `DENIAL_NEVER` for non-liberation cities in
    peacetime (10324), so in practice only liberation cities qualify.
- **Validity bypass:** `canTradeItem` has a liberation fast path (CvPlayer.cpp:5475). `AI_cityTrade` returns
  NO_DENIAL for the liberation player (10286). `AI_cityTrade` also lets an AI receiver refuse a distant
  zero-culture city, or any such city while it is in financial trouble (10291-10309).
- **A human asks the AI to liberate a city to them:**
  - The denial check passes.
  - In `AI_considerOffer` the AI gives the city and receives nothing, so the **gift/demand branch** runs (9007-9054).
  - The value is `human.AI_cityTradeVal(city)`, usually 1000-3000 vp, against a threshold of about
    `2*(hasMet+50)*powerRatio`. The request is therefore normally refused unless the two have known each other for
    a long time or the human is much stronger.
  - The human **cannot add a payment**, because `updateTradeList` hides every other item when a city is in the deal
    (CvPlayer.cpp:24234-24237).
  - `AI_counterPropose` cannot ask for anything either, because all its inventory nodes are hidden.
- **The AI asking for a liberation:** this never happens, to humans or to AIs. The AI only requests cities in war
  contexts: AI_doPeace (1033-1054) and AI_counterPropose case 1 (9115-9155). In peace deals it offers cities
  (1100-1122) whose value is no more than the gap.
- **City valuation gaps:** `AI_cityTradeVal` ignores buildings, wonders, specialists and strategic location. The
  giving AI's loss is never computed. The liberator's attitude gain is not priced into the trade.

---------------------------------------------------------------------------------------------------

## 4. Attitude and memory

### 4.1 AI_getAttitudeVal (CvPlayerAI.cpp:7379-7511)

The attitude value is the sum of:
- `LeaderHead.BaseAttitude`
- `Handicap(other).AttitudeChange`
- AI-to-AI only: `4 - |peaceWeight difference|` and `min(warmongerRespect)`
- a team-size penalty
- rank difference (`Worse/BetterRankDifferenceAttitudeChange`)
- +1 when both players are in the bottom half of the ranks
- `LostWarAttitudeChange`
- **CloseBorders** (cached, 7722), **War** (7761), **Peace** (7783), **SameReligion** (7797),
  **DifferentReligion** (7824), **BonusTrade** (7851), **OpenBorders** (7868), **DefensivePact** (7885),
  **RivalDefensivePact** (7907), **RivalVassal** (7925), **ShareWar** (7943), **FavoriteCivic** (7968)
- **Trade**: `(grant + max(0, ourTrade - theirTrade)) / ((hasMet+1)*5)`, clamped to 0..4 (7994)
- **RivalTrade**, from trades with our worst enemy (8001)
- the sum over all memories of `count*MemoryAttitudePercent/100` (8008)
- **Colony** (8013)
- `AttitudeExtra`
- RevDCM rebel adjustment (-5 or -3)

The result is clamped to -100..100. Mapping (7345): >=10 FRIENDLY, >=3 PLEASED, <=-10 FURIOUS, <=-3 ANNOYED,
otherwise CAUTIOUS.

**Cache:** `m_aiAttitudeCache` (7409/7505) is invalidated in `AI_doTurnPre` (448) and by
`AI_changePeacetimeTradeValue` (14898). It is **not** invalidated by `AI_changeMemoryCount` (15109) or
`AI_changePeacetimeGrantValue` (14955). See D6.

### 4.2 Counters and memory decay

- `CvPlayerAI::AI_doCounter` (15148-15250) handles the religion, civic and bonus-trade counters and the contact
  timers (decremented by 1 per turn). Each memory type with a count above 0 loses 1 with probability
  `1/MemoryDecayRand` per turn.
- `CvTeamAI::AI_doCounter` (CvTeamAI.cpp:4400-4450) handles the at-war, at-peace, has-met, OB, DP and share-war
  counters. `setOpenBorders` resets the OB counter (CvTeam.cpp:4668).
- Counts below are the number of leaders out of 60 (CIV4LeaderHeadInfos.xml).
  - Memories that never decay (no MemoryDecay entry): DECLARED_WAR (-300% for 58), DECLARED_WAR_ON_FRIEND,
    HIRED_WAR_ALLY (-200% for 56), NUKED_*, RAZED_*, SPY_CAUGHT, STOPPED_TRADING, HIRED_TRADE_EMBARGO,
    MADE_DEMAND (capped at 10 in handleDiploEvent), LIBERATED_CITIES (+150% for 58).
  - Memories that do decay: CANCELLED_OPEN_BORDERS (rand 10, which drives DENIAL_RECENT_CANCEL),
    MADE_DEMAND_RECENT (20), RECEIVED_TECH_FROM_ANY (20, which drives DENIAL_TECH_WHORE),
    TRADED_TECH_TO_US (100), GIVE_HELP (200).
  - All decay rates are per turn and do not scale with game speed.
- Diplo events (`CvPlayer::handleDiploEvent`, CvPlayer.cpp:5136-5342) record memories:
  - accepting help or a demand also calls `forcePeace`, giving a 10-turn treaty (5173, 5182)
  - a rejected demand can trigger a sneak war plan (5190-5193)

### 4.3 How attitude gates trades

| Item | Gate | XML threshold (distribution over 60 leaders) |
|---|---|---|
| Tech | `AI_techTrade` (CvTeamAI.cpp:1728). Checks worst enemy, `TechRefuseAttitudeThreshold` (each team member), tech whore (below FRIENDLY), monopoly, then MYSTERY or VICTORY for wonders and projects. | ANNOYED 37, FURIOUS 15, CAUTIOUS 4, NONE 4 |
| Resource | `AI_bonusTrade` (10116). Checks worst enemy, corporation input, then Strategic, Happiness or Health thresholds. | Strategic: CAUTIOUS 38, ANNOYED 19, PLEASED 2. Happy: ANNOYED 28, FURIOUS 26 |
| Map | `AI_mapTrade` 1977: `MapRefuseAttitudeThreshold` | - |
| OB | `AI_openBordersTrade` 3408. Shared war means yes. Then recent cancel, worst enemy, `OpenBordersRefuse...`. | ANNOYED 41, FURIOUS 14 |
| DP | `AI_defensivePactTrade` 3468. Only two civs left means no. Then worst enemy, `DefensivePactRefuse...`. | PLEASED 50, CAUTIOUS 9 |
| PA | `AI_permanentAllianceTrade` 3512. Combined power above 50% means POWER denial. DP plus share-war counter below 40 means NOT_ALLIED. Then threshold. | PLEASED 55 |
| Vassal | `AI_surrenderTrade` 2098. Power ratios, victory threat, then `VassalRefuse...` adjusted by an attitude modifier. | PLEASED 37, CAUTIOUS 13 |
| War, embargo | `DeclareWar(Them)Refuse...` and `StopTrading(Them)Refuse...` | - |
| Civic, religion | `AdoptCivicRefuse...` and `ConvertReligionRefuse...` | - |
| Gift branch | below PLEASED and we are more than 4/3 stronger means refuse (9025-9030) | - |
| Proposal cadence | AI_doDiplo: city offers need CAUTIOUS or better (17319). Help and tribute thresholds read the human's leader (D3). | NoGiveHelp CAUTIOUS 58; DemandTribute CAUTIOUS 58 |

`NONE` means NO_ATTITUDE (-1), so that leader never refuses. Thresholds are read in CvInfos.h:4270-4287.
Willingness to talk (`AI_isWillingToTalk` 7223-7273): at war the AI refuses until the war has lasted
`RefuseToTalkWarThreshold` turns (x2 for a chosen war, shorter if it is losing badly). AI vassals never talk while
at war. At peace the AI refuses after `MEMORY_STOPPED_TRADING_RECENT`.

---------------------------------------------------------------------------------------------------

## 5. War and peace decisions that touch diplomacy

- **Entry:** `CvTeamAI::AI_doTurnPost` (167-190) calls `AI_updateWorstEnemy` and then `AI_doWar` (4495). There is a
  Python veto hook `AI_doWar` (4525). Vassals do nothing (4516).
- **War-plan state machine** (4534-4715):
  - ATTACKED_RECENT becomes ATTACKED after 9 or 3 turns.
  - PREPARING_LIMITED becomes LIMITED after `5*timeMod` turns.
  - PREPARING_TOTAL becomes TOTAL when the area is offensive and power is below 140% (or below 110% when areas
    are not shared), or a victory countdown is running. It is abandoned after `20*abandonMod` turns.
  - LIMITED, DOGPILE and TOTAL plans are abandoned when they have no active missions.
  - The time modifiers scale with `TrainPercent`; power ratios come from `AI_maxWarNearbyPowerRatio` and related
    functions.
- **Peace for each team member:** `AI_doPeace` (4718-4725, see 2.7).
- **Unilateral AI-to-AI peace** (4746-4851), reached through `rand(AI_makePeaceRand)`:
  - In a chosen war longer than `max(10, 14*VictoryDelay%)` turns: if the war is idle and neither side has target
    missions, a 1/8 roll triggers `makePeace` (4799).
  - In a long draw (30 or 40 turns times VictoryDelay%): if the end-war values are within 2x of each other,
    `makePeace` (4822).
  - If we planned a dogpile but are fighting alone: `makePeace` (4840).
  - All of these call `CvTeam::makePeace` directly. There is no deal, so there is also **no forced peace treaty**.
- **Starting wars** (4857-5196): only when there are no war plans or `enemyPower < 45%`.
  - Finance and dagger flags feed into `AI_getWarRands/Thresholds`.
  - `AI_noWarAttitudeProb(attitude)` is the attitude veto (4347).
  - Targets are picked by `AI_startWarVal` (1212), filtered by power ratio, land target and adjacency, and set as
    PREPARING_TOTAL, PREPARING_LIMITED or DOGPILE.
  - The actual declaration happens elsewhere: `CvSelectionGroup::groupDeclareWar` (CvSelectionGroup.cpp:4300) for
    units, plus event, vote and diplo-event paths.
- **Peace acceptance:**
  - For human proposals, `AI_considerOffer` adds `AI_endWarVal` to both sides (8822). The gift branch is skipped at
    war because the end-war value is never 0 (`iTheirValue != 0`).
  - A brokered peace (a human asks an AI to make peace with a third party) goes through `AI_makePeaceTrade`
    (3101-3140). It is denied if the third party is human (CONTACT_THEM) or a vassal, if
    `endWarVal(us) > 2*endWarVal(them)`, or by the land-ratio rule (3133, D12).
- **Tribute demands:** see the AI_doDiplo demand section (17827-18045).
  - The AI must be able to declare war, must not already have chosen war on the target (BBAI fix), and must have
    more power than the target's defensive power.
  - Each of gold, map, tech or resource gets its own `ContactRand` roll.
  - Accepting a demand forces a 10-turn peace. Rejecting can lead to `AI_demandRebukedSneak` (a war plan) or
    `AI_demandRebukedWar`.
- **Hiring war partners:** AI_doDiplo hire-war section (18502-18705) together with `AI_declareWarTrade` (3278). The
  hired AI refuses if it is already at war with anyone (BBAI, 3319-3322) or has any war plan (3390-3393).
- **Vassal and capitulation:** `AI_surrenderTrade` (2098-2437) and `AI_acceptSurrender` (2616). `CvDeal::addTrades`
  frees the capitulator's own vassals and copies war success (160-196).

---------------------------------------------------------------------------------------------------

## 6. Verified defects and suspicious logic

Severity: H = changes decisions often, M = sometimes, L = rare or cosmetic.
Status is "verified" unless the entry says otherwise.

**D1 (M). The AI undervalues a resource it receives when proposing a swap to a human.**
CvPlayerAI.cpp:18403 compares `AI_bonusTradeVal(eBestReceiveBonus, iI, -1)` with the human's
`AI_bonusTradeVal(eBestGiveBonus, getID(), +1)`. The AI always has 0 copies of the bonus it would receive, because
`AI_bonusTrade` denies trades for owned bonuses (10146-10149). With `iChange=-1` and a count of 0, `AI_bonusVal`
(9684-9701) takes the marginal branch, `base/5`. The AI therefore proposes a 1:1 swap to a human only when a fifth of
its own value beats the human's full value, so it almost never makes these offers. The argument should be +1.

**D2 (L). The second tech in a war-hire deal is picked with the wrong comparison.**
CvPlayerAI.cpp:18619-18622 tests `if (iValue > iBestValue)` but stores the result in `iBestValue2`/`eBestGiveTech2`.
`iBestValue` is the maximum from the first loop and is never updated here. So the second tech is the *last* tech
whose fresh random roll beats the first loop's maximum. It is not the best one, and often no tech is chosen at all.

**D3 (L). Help and tribute thresholds read the target's leader.**
CvPlayerAI.cpp:17695 (`NoGiveHelpAttitudeThreshold`) and 17859 (`DemandTributeAttitudeThreshold`) use
`GC.getLeaderHeadInfo(GET_PLAYER(iI).getPersonalityType())`. That is the human's leader, not the AI's. The effect is
small today because 58 of 60 leaders share the value CAUTIOUS. Any XML retuning of these fields will apply to the
wrong side.

**D4 (M). Peace deals price gold at 1 vp per gold.**
AI_doPeace adds and compares gold as `iOurValue += iGold` with `iGold = min(gap, max)` (CvPlayerAI.cpp:1018-1027,
1085-1094). Everywhere else gold is worth `AI_goldTradeValuePercent()` = 200-300 vp per 100 gold
(22366; AI_dealVal 8851). As a result:
- the AI asks for 2-3x too much gold when it is the side that wants peace less
- it overpays by 2-3x when it is the side that wants peace more

**D5 (H in late game). Signed 32-bit overflow in products of power.**
In RoM a single unit can have `iPower` up to 2100 (Units/CIV4UnitInfos.xml), so team power reaches 10^5-10^6.
Overflowing sites:
- `AI_endWarVal`: `iValue *= iTheirPower + 10` (CvTeamAI.cpp:1381), `iValue *= 9*iTheirPower` (1415),
  `iValue *= 7*(5*iTheirPower)` (1437/1446/1455)
- `AI_surrenderTrade`: `2*iMasterPower*iTheirSuccess` (2229), `2*iAveragePower*kLoopTeam.getPower(true)` (2265,
  which overflows once both powers exceed about 33k), `iAveragePower*(ourPow+masterPow)` (2272)
- `AI_considerOffer`: `iOurValue *= ourPow+10` (CvPlayerAI.cpp:9015), `iThreshold *= theirPow+100` (9048)

Concrete failures:
- `iAveragePower` turns negative, so `5*iVassalPower > 4*iAveragePower` is always true and the AI always returns
  DENIAL_POWER_US. It never capitulates or volunteers as a vassal.
- `AI_endWarVal` becomes garbage, possibly negative. It feeds AI_doPeace, AI_doWar peace decisions,
  AI_makePeaceTrade and every at-war AI_dealVal.

The RoM helper `AIDiplomacyPolicy` only fixed the gold conversions in AI_counterPropose.
How soon this happens depends on actual power values (verified arithmetic; the in-game magnitude was not measured).

**D6 (M). The attitude cache goes stale after gifts and memory changes.**
`AI_changeMemoryCount` (CvPlayerAI.cpp:15109-15122) and `AI_changePeacetimeGrantValue` (14955-15006) do not call
`AI_invalidateAttitudeCache`. `AI_changePeacetimeTradeValue` does (14898-14899). Example: a human gifts a tech
(grant value, MEMORY_TRADED_TECH_TO_US, MEMORY_GIVE_HELP) and then immediately asks for something in the same turn.
Denials and the gift branch still see the old attitude until the AI's next `AI_doTurnPre` (448). This also hides the
effect of MEMORY_LIBERATED_CITIES, demand memories and similar changes within a turn.

**D7 (M). An embargo is priced from all of the target's deals.**
`AI_stopTradingTradeVal` (CvPlayerAI.cpp:10392-10413) adds the value of every cancelable deal of ePlayer's team. It
never checks that the counterparty is `eTradeTeam`. An embargo against a minor partner is therefore priced as if the
target would lose all of its trade. It also passes `isCancelable(getID())` with the asker's ID instead of the
deal's party.

**D8 (L, text only). Wrong team in the vassal revolt help text.**
In `CvDeal::isUncancelableVassalDeal`, second loop (CvDeal.cpp:497), the vassal is the second player but the call
passes `GET_PLAYER(getFirstPlayer()).getTeam()` as the vassal, which is the master's own team
(`setVassalRevoltHelp(buf, eMaster, eVassal)`, CvGameTextMgr.h:155). The help text is therefore built for the wrong
pair. Line 494 also repeats a redundant `if (pszReason)`.

**D9 (L, dead code). The gold term in a human's GPT limit has no effect.**
`AI_maxGoldPerTurnTrade`, human branch (CvPlayerAI.cpp:9659): `goldRate + gold/PEACE_TREATY_LENGTH` is immediately
capped at `goldRate` (9671). A human with a large treasury and a gold rate of 0 or less can never be asked for any
GPT.

**D10 (M, multiplayer). Out-of-sync risk on the "do not bother" path.**
`AI_beginDiplomacy` (16859-16915) is RevDCM's "do not bother" auto-reject. For DEMAND_TRIBUTE it calls
`AI_demandRebukedWar` (16904), which uses `GC.getASyncRand()` (7307). The comment there says it is only meant for the
machine showing the diplomacy screen. Here it runs inside synchronous AI_doDiplo, and on a true result it calls
`handleDiploEvent(DIPLOEVENT_DEMAND_WAR)` directly, which declares war. Different machines can roll differently,
which leads to a war on only some clients (OOS). This was verified by reading the code; it has not been reproduced.

**D11 (L). The ask-for-help roll can be made against 0.**
CvPlayerAI.cpp:17768-17776 computes `iRand = ContactRand*max(1, techPerc-60)/30` with no `max(1, ...)` (compare the
tech-trade block at 18176). For leaders with ContactRand below 30, or 30-59 with `techPerc <= 61`, the result is 0 or
1, and `getSorenRandNum(0 or 1)` always returns 0 (CvRandom.cpp:70). The request then fires every time the 50-turn
timer allows, and a debug build asserts on `get(0)`.

**D12 (L-M, suspicious). The land-ratio check for brokered peace compares against the wrong team.**
`AI_makePeaceTrade` (CvTeamAI.cpp:3133-3137) computes the land ratio against `eTeam`, the team asking us to make
peace, instead of `ePeaceTeam`, the enemy. Any small civ that asks a large civ to make peace with someone gets
DENIAL_VICTORY, however the war is going. The intent was probably "we are crushing ePeaceTeam" (not confirmed).

**D13 (M). Time constants ignore game speed.**
Game speeds range from Blitz (40% research) to Snail (700%) (GameInfo/CIV4GameSpeedInfo.xml). Fixed in turns:
- `PEACE_TREATY_LENGTH=10` (GlobalDefines.xml:757), which sets treaty length and the cancel lock
  (CvDeal.cpp:1295), and the valuation horizon for resources and GPT (CvPlayerAI.cpp:9677, 10112)
- the 20-turn re-evaluation of existing deals (16993)
- the at-war wait of more than 10 turns in AI_doPeace (910)
- the `%20` city-offer cadence (17325)
- memory decay and contact delays (per-turn XML values)

Meanwhile tech values scale with research cost (CvTeamAI.cpp:1684). Other terms grow with the number of turns
played: has-met counters (9039, 9631, 7997, 8004), elapsed turns (10246) and game turn (CvTeamAI.cpp:3051,
CvPlayerAI.cpp:10349). On Snail, resources and GPT are worth about 1/7 as much relative to techs as on Normal. Gift
thresholds and gold limits are also several times looser than on Normal.

**D14 (H for balance). AI-to-AI deals skip the partner's own evaluation.**
Every AI_doDiplo and AI_doPeace path to an AI partner calls `implementDeal` after denial checks only, with these
value checks at most:
- tech: 2/3 window (18277)
- resources: none (18403)
- maps, OB, DP, PA: none
- peace: 3/5 window (1125)
- war hire: 3/4 (18668)
- vassal tribute: none at all (17271-17312)

Humans get `AI_considerOffer` (full value comparison and the vassal-tribute refusal rule, 9009-9026). The AI partner
can therefore be made to accept a deal it values at 60% of what it gives. This affects AI-AI tech parity and the
inter-AI balance of power in general.

**D15 (M). Peace between AIs can be forced without the partner's willingness.**
AI_doPeace checks only `AI_isWillingToTalk` for the proposer (898). AI_doWar peace (CvTeamAI.cpp:4799, 4822, 4840)
calls `makePeace` with no willingness check, and in the idle case without the partner's end-war value. A partner
that "refuses to talk" can still be pulled into peace.

**D16 (M). Deals are re-checked differently for humans and AIs.**
CvPlayerAI.cpp:16985-17118:
- deals with humans are re-valued (10% tolerance) but denials are not checked
- deals with AIs are checked only for denials of the AI's own items, never for value

An AI never cancels a lopsided AI deal. If a deal with a human only fails on a denial (for example worst enemy or an
attitude drop), it survives.

**D17 (suspicious; status not certain). Tech brokering is always disabled.**
`CvDeal::startTrade` sets `setNoTradeTech(tech, true)` on every traded tech without any condition (CvDeal.cpp:708).
`canTradeItem` refuses `isNoTradeTech` techs (CvPlayer.cpp:5430). The flag is only cleared by team merging
(CvTeam.cpp:1016-1019, `shareCounters`). As a result a team can never re-trade a tech it received by trade, whatever
GAMEOPTION_NO_TECH_BROKERING is set to. The option only changes `canResearch(bTrade)` (CvPlayer.cpp:8618, 8642) and
the Afforess check in `AI_techTrade` (CvTeamAI.cpp:1750-1778). This may be intentional in RoM.

**D18 (L, dead or missing values).**
- `AI_dealVal` has no case for PERMANENT_ALLIANCE.
- `AI_vassalTradeVal` and `AI_surrenderTradeVal` return 0 (CvTeamAI.cpp:2026-2095), so the AI_counterPropose
  surrender line (CvPlayerAI.cpp:9370) adds 0.
- The OB and DP values are trivially small (3404, 3464), so whatever is attached to OB or DP decides the deal.

**D19 (L). Default arguments disagree.**
`CvPlayer::AI_dealVal` declares `iExtra=0` (CvPlayer.h:1205) and `CvPlayerAI::AI_dealVal` declares `iExtra=1`
(CvPlayerAI.h:294). Default arguments bind statically, so a call through `CvPlayer&` (the EXE, `Cy` wrappers) gets
the full value of a bonus, while a call through `GET_PLAYER` (CvPlayerAI&) gets the "+1" value.

**D20 (L). Raw 32-bit gold arithmetic in AI_doDiplo and AI_dealVal.**
CvPlayerAI.cpp:18238, 18260, 18639, 18654 and 8851 still use unprotected `x*100/percent` and `gold*percent`.
Overflow needs a gap above about 21M vp or more than 10M gold, which is unlikely given RoM's highest base tech cost
of 53000 x 7. These sites are also inconsistent with the AIDiplomacyPolicy rounding rules.

**D21 (L, latent).** `CvCity::liberate` dereferences `pCity` in the vassal free-defender loop (CvCity.cpp:15895-15901)
outside the `pCity != NULL` check. This is safe as long as `acquireCity(..., bTrade=true)` always leaves a city.

---------------------------------------------------------------------------------------------------

## 7. Extension points

### 7.1 Lump-sum trades (gold or tech for a resource, tech for GPT, selling a tech for gold)

1. **Unblock the shapes.** Relax the annual/one-shot rule in `CvPlayer::updateTradeList` (CvPlayer.cpp:24220-24244).
   - This one change opens both the human UI and `AI_counterPropose`, which respects `m_bHidden`.
   - No EXE change is needed, because the rule lives in the DLL.
   - Keep it switchable, for example through a GlobalDefine.
2. **Valuation horizon.** `AI_goldPerTurnTradeVal` (9675) and `AI_bonusTradeVal` (10112) both price exactly 10
   turns. For lump sums against annual items, use a horizon that reflects the expected life of the deal and the
   game speed. Options are a new `DIPLO_ANNUAL_HORIZON` scaled by `GameSpeedInfo.ResearchPercent`, or the actual
   cancel lock. Use the same horizon in `CvDeal::doTurn` (296-330) and in the cancel lock.
3. **Keep the paid part of the deal.** One-shot items are not saved: `startTrade` returns false for GOLD and TECH
   (CvDeal.cpp:706-800).
   - After 20 turns, AI_doDiplo re-checks deals with humans via `AI_considerOffer(-1)` (17008/17029). It then sees
     only the annual side, takes the gift branch and cancels, so the human loses what they paid.
   - For AI-AI deals only denials are checked, so a lopsided remainder survives indefinitely.
   - Add per-deal fields such as `m_aiPrepaidValue[2]` and `m_iLockTurns`, or save the one-shot nodes with a flag.
     If you save the nodes, `endTrade` (1092-1190) must stop asserting on GOLD and TECH, and `kill`'s message string
     has to change.
   - Make `turnsToCancel` (1293) honour the prepaid lock, and make the re-check at 16985-17118 count the prepaid
     value.
4. **Acceptance.** `AI_considerOffer` (8927): add a risk premium when the AI pays a lump sum for an annual item,
   because the partner can cancel after the lock, and a discount when the AI receives the lump sum. Gold limits come
   from `AI_maxGoldTrade` (9617).
5. **Proposals.** Add AI_doDiplo generators, preferably chosen by value rather than `rand(10000)`:
   - buy a resource for gold or a tech
   - sell a tech for gold (a new branch next to 18152-18334, which currently requires a tech to receive)
   - offer GPT for a resource
   - for AI partners, call `GET_PLAYER(iI).AI_considerOffer(getID(), ourList, theirList)` before
     `implementDeal`; this also fixes D14

   Each new generator may need its own `ContactTypes` entry (see 7.4 for the save impact).
6. **Python.** BUG's `DealUtil.py:98-127` duplicates `isAnnual/isDual/hasData`, and `TradeUtil.py:515-531` has the
   formatters. Neither needs changes for mixing alone. They do if you add items.

### 7.2 AI offers attached to liberation requests, both directions

1. **UI and counter-offers.** At CvPlayer.cpp:24234, stop hiding other items when the first or current city item has
   `getLiberationPlayer(false) == receiver`. Do the same for the reverse case. `AI_counterPropose` case 1 then works
   unchanged: the AI asks the human for gold, techs or resources in return for liberating.
2. **The AI being asked.** The AI_considerOffer gift branch (9007-9054) applies to an unpaid request. A paid request
   uses the normal `iTheirValue >= iOurValue` rule.
   - Add the giver's own loss with something like `AI_cityLossVal(pCity)` (city value, wonders, strategic value) to
     `iOurValue`, because today only the receiver's gain is counted (2.2).
   - Optionally credit the attitude gain. For an AI receiver that is MEMORY_LIBERATED_CITIES at +150% (CvCity.cpp:15876).
3. **The AI asking.** Add a generator in AI_doDiplo, next to the liberation gift block at 17317-17388.
   - For each foreign city where `getLiberationPlayer(false) == getID()`, build theirList={city} and ourList, sized
     by `AI_cityTradeVal` plus the giver's loss. ourList can hold gold up to `AI_maxGoldTrade`, techs, or OB.
   - A human gets a new diplo comment, an AI partner gets `AI_considerOffer`.
   - Needs:
     - a new `AI_DIPLOCOMMENT_*` in `GameInfo/CIV4DiplomacyInfos.xml` with text in `Text/RoM_GameText_DiplomacyText.xml`
     - a branch in `Python/CvDiplomacy.py` (copy OFFER_DEAL at 74-83: accept, renegotiate, reject)
     - a `CONTACT_*` type (GlobalTypes.xml ContactTypes plus LeaderHead ContactRands/ContactDelays)
4. **Validity** is already in place: `canTradeItem` liberation fast path (CvPlayer.cpp:5475) and `AI_cityTrade`
   (10286). Check that `CvDeal::startTrade` CITIES then `TASK_GIFT` then `liberate()` still runs when gold or techs
   are bundled in. The order of nodes in `addTrades` does not matter for that.

### 7.3 Splitting Open Borders into trade rights, civilian access and military access

**Data.**
- Today OB is `CvTeam::m_abOpenBorders` (CvTeam.cpp:60/261/287), with `isOpenBorders` at 4646, `setOpenBorders` at
  4654-4690 and save/load at 7375/7484.
- Add three bool arrays or one bitmask int array. Keep `isOpenBorders()` as "all three" for compatibility, or
  replace its 34 call sites.
- Gating counter: `m_iOpenBordersTradingCount` comes from TechInfo `bOpenBordersTrading`. For separate techs, add
  new counters and new TechInfo XML fields (CvInfos plus schema).

**Call-site classification of `isOpenBorders`.**

Military access:
- `CvUnit::canEnterTerritory` (CvUnit.cpp:2496). Split it by unit type here, for example on `canFight()` or a
  combat check.
- `CvPlot::isFriendlyCity` (CvPlot.cpp:3591): healing, stacking, air basing.
- `teamStepValid` (CvGameCoreUtils.cpp:2396): AI path search.
- `CvUnitAI::AI_assaultSeaReinforce` (17908).
- War weariness through `CvPlot::countFriendlyCulture` (CvPlot.cpp:10255, CvTeam.cpp:4327).
- Spy handling: `CvUnit::doTurn` intercept (CvUnit.cpp:749), `canSpyBribeUnit` (CvPlayer.cpp:23494).

Civilian access:
- `canEnterTerritory` for non-combat units: missionaries, executives, great people, workers.
- `AI_missionaryValue` (CvPlayerAI.cpp:12187), `AI_executiveValue` (12358), `AI_getStrategyHash` (21318).

Trade rights:
- `CvTeam::isFreeTrade` (4630-4643), which drives trade routes: `canHaveTradeRoutesWith` (CvPlayer.cpp:23416) and
  `countPotentialForeignTradeCities` (4977/5016).
- The trade-route refresh inside `setOpenBorders` (4677-4688).
- Tech diffusion: `calculateResearchModifier` (8367) and Python `Revolution/Gameready/TechDiffusion.py:186`.
- BUG `TradeUtil.py:172`.

Diplomacy and other uses:
- liberation-gift eligibility (CvPlayer.cpp:2893, CvDLLButtonPopup.cpp:1422)
- votes (CvGame.cpp:4277-4290, 7786-7798, 9313; CvPlayer.cpp:23115, 23240-23249; AI_diploVote 8296/8322)
- `AI_stopTradingTradeVal` (10383)
- `CvTeam::addTeam` (658-663)
- `isFriendlyTerritory` (7046)
- `CvTeamAI::AI_doCounter` OB counter (4426)
- text (CvGameTextMgr.cpp:16536)
- UI: `CvMainInterface.py:5382`, `CvForeignAdvisor.py:694/740`, `MoreCiv4lerts.py:465`

**Trade items.**
- **Append** new items after `TRADE_RELIGION` (CvEnums.h:1979). Do not insert before `NUM_BASIC_ITEMS`: that
  shifts `TRADE_TECHNOLOGIES..` values, breaks saves (raw TradeData) and breaks the EXE's view of the enum, which
  sits outside the `_USRDLL` guard.
- Appended items become headings. One option is a "Borders" heading whose `m_iData` is the subtype. Then
  `hasData` must be true, and the startTeamTrade `m_iData==0/1` lead flag needs a different encoding, for example a
  high bit.
- Update:
  - `CvDeal::isAnnual/isDual/hasData` (1299-1343, DllExport, used by the EXE)
  - `startTrade/endTrade/startTeamTrade/endTeamTrade`
  - `canTradeItem`, `getTradeDenial`, `buildTradeTable`, `getHeadingTradeString`, `getItemTradeString`,
    `updateTradeList`
  - `CyEnumsInterface.cpp:1425-1447`
- An alternative that avoids headings: keep `TRADE_OPEN_BORDERS` as "full" and add only the partial items.
- Prior art: Afforess's A New Dawn and C2C (RoM successors) added items after TRADE_RELIGION, including a "rite of
  passage"/limited-borders item. This comes from outside this tree and was not checked here.

**AI.**
- Replace `AI_openBordersTradeVal` (CvTeamAI.cpp:3402) with separate valuers:
  - trade rights: trade-route commerce and diffusion
  - civilian access: missionary and executive value, espionage
  - military access: the value of staging against a shared enemy, minus the threat from a stronger land-target
    neighbour
- Give each type its own denial (`AI_openBordersTrade` 3408). For example, military access should require PLEASED or
  better, never be granted to a team with a war plan against us, and be refused to land-target neighbours above a
  power ratio.
- Add separate AI_doDiplo generators (OB block 18050-18100), and allow asymmetric deals such as military access
  for gold.
- Memory: MEMORY_CANCELLED_OPEN_BORDERS per type (endTrade 1149-1167) or a shared one.
- Attitude: OB counter (`m_aiOpenBordersCounter`) and the LeaderHead `OpenBordersAttitude*` fields.
- XML thresholds: new `*RefuseAttitudeThreshold` fields in `CvLeaderHeadInfo` (CvInfos.h:4283, read in CvInfos.cpp),
  the schema, and `Civilizations/CIV4LeaderHeadInfos.xml`.

**Python and UI.**
- Expose new `CyTeam` getters (CyTeamInterface.cpp:173) and new enum values.
- BUG `DealUtil.py:60, 98-127`, `TradeUtil.py:520` (add formatters), the advisors, the main interface OB icon,
  and `Revolution.py:5416/5634` (`signOpenBorders`).
- Votes: `CIV4VoteInfo bOpenBorders` should map to "all three", or gain new flags.

### 7.4 Save-format checklist

| Stream | Location | Current flag | Impact |
|---|---|---|---|
| CvDeal | CvDeal.cpp:661-689 | writes 0 and ignores it on read | Bump it and add fields (prepaid value, lock) under `if (uiFlag >= 1)`. |
| TradeData nodes | LinkedList.h:367-396 | raw `sizeof(TradeData)` (12 bytes) | Never change the struct layout. Only append new enum values. |
| CvGame deals | CvGame.cpp:8409/8637 | - | No change needed. |
| CvTeam | CvTeam.cpp:7324-7432 / 7434 | `uiFlag` is read but not used in the visible block | New per-team arrays must be versioned. On load, migrate `m_abOpenBorders` into all three. |
| CvTeamAI | CvTeamAI.cpp:4000-4045 | 0 | OB counters per type. |
| CvPlayerAI | CvPlayerAI.cpp:18720 / 18976 (writes `uiFlag=6`, 18989) | 6 | `m_aaiContactTimer` (18847/19052) and `m_aaiMemoryCount` (18851/19056) are written as `NUM_CONTACT_TYPES`/`NUM_MEMORY_TYPES` arrays. Adding a contact or memory type means reading the old length when `uiFlag < 7`. |
| XML enum tables | `GlobalTypes.xml` ContactTypes, `BasicInfos/CIV4MemoryInfos.xml`, LeaderHead ContactRands, Delays, MemoryDecays, MemoryAttitudePercents | - | Must match `NUM_*` exactly (CvGlobals.cpp:1924/2784 asserts). |

### 7.5 Python and EXE exposure (current state)

- **Enum:** `TradeableItems` is fully exported (CyEnumsInterface.cpp:1425-1447), including `NUM_BASIC_ITEMS` and
  `NUM_TRADEABLE_ITEMS`.
- **CyDeal** (CyGameInterface.cpp:349-366): getters, kill, and BUG's `isCancelable/getCannotCancelReason/turnsToCancel`.
- **CyPlayer:**
  - `canTradeItem` and `getTradeDenial` (CyPlayerInterface1.cpp:132-133)
  - `AI_getAttitude`, `AI_getMemoryCount`, `AI_getAttitudeExtra` (CyPlayerInterface2.cpp:27-37)
  - `AI_maxGoldTrade/PerTurnTrade` (58-59)
- **CyTeam:** `isOpenBorders`, `isOpenBordersTrading`, `signOpenBorders`, `signDefensivePact` (CyTeamInterface.cpp:35-36, 117, 173).
- **Python callbacks:** `AI_doDiplo` and `AI_doWar` (veto hooks) and `AI_doDiplo`'s arguments. There are no
  callbacks for valuation or for considerOffer.
- **Python users of TradeableItems:** BUG DealUtil/TradeUtil/PlayerUtil/DiplomacyUtil, MoreCiv4lerts (builds probe
  TradeData for OB, DP, PA, vassal, surrender, peace, tech, maps), CvExoticForeignAdvisor and CvForeignAdvisor
  (resource, tech and GPT tables), CvRandomEventInterface (TRADE_CIVIC). All of them refer to items by name, so
  appending new values is safe for them.
- **EXE-facing DLL functions:** the trade-screen hooks in 1.5, the `CvDeal` statics, `AI_considerOffer`,
  `AI_counterPropose`, `AI_dealVal`, `AI_maxGold*` (virtual), `canTradeItem`, `getTradeDenial`, `setTradeItem`,
  `CvGame::implementDeal`, `CvDeal::kill`, and `isVassalTributeDeal`.
