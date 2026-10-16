# Open Borders coupling map (Rise of Mankind, BBAI DLL + Python + XML)

Scope: everything that reads, writes, displays or reasons about Open Borders (OB)
in `Assets/` of GitLab `main` 93ae873 (with patch 0013). Read-only analysis, nothing modified.

Path conventions: `DLL/` = `Assets/CvGameCoreDLL/`, `Py/` = `Assets/Python/`,
`XML/` = `Assets/XML/`. Line numbers are from the current tree.

Category tags used throughout (planned split):

- [T] trade rights (trade routes, foreign trade commerce, resource connection)
- [C] civilian access (workers, settlers, missionaries, executives, great people, explorers, ...)
- [M] military access (combat units, warships, air basing)
- [-] not actually coupled to OB (listed because the task named it)
- [?] ambiguous, see section 4

## 0. Key findings in brief

1. OB is one bool per team pair (`CvTeam::m_abOpenBorders`), always set symmetrically by
   a "dual" deal item. Direct DLL readers of `isOpenBorders`: about 25 call sites; most
   behaviour flows through four derived predicates: `CvUnit::canEnterTerritory`,
   `CvPlot::isFriendlyCity`, `CvTeam::isFriendlyTerritory` (vassal case) and
   `CvTeam::isFreeTrade` (trade routes).
2. Resource trading and the trade network (plot groups, road connection through
   foreign land) are NOT gated by OB today (`CvPlot::isTradeNetwork*`,
   `CvPlayer::canTradeNetworkWith`). Gating resources behind "trade rights" would be new
   behaviour, not a split of existing behaviour.
3. Many "civilian" units already ignore borders: spies, great spy, great merchant,
   caravans, merchant ships, caravel-type explorers, submarines have `bRivalTerritory`;
   spies are also `bInvisible`. Missionaries, executives, prophets, workers, settlers,
   scouts/explorers, great generals and work boats do need OB.
4. Declaring war kills the OB deal before `setAtWar`, so `verifyUnitValidPlot` teleports
   every unit that was inside via OB out of the territory before the war starts
   (DLL/CvTeam.cpp:1440-1460). Units "already inside" can never be used for a surprise attack.
5. The flag direction convention is inconsistent between callers (giver vs holder); this is
   invisible while OB is symmetric but becomes a real bug if any agreement is made one-way.
6. The trade screen lives in the EXE; it reads item ranges from the DLL
   (`GC.getNumBasicItems()/getNumTradeableHeadings()`, DllExport) and mirrors items for
   which `CvDeal::isDual` (DllExport) is true. Enum placement and dual-ness are therefore
   the main integration risks.

---------------------------------------------------------------------------------------

## 1. Storage and lifecycle

### 1.1 Data and accessors

| What | Where |
|---|---|
| `bool* m_abOpenBorders` (per team, size MAX_TEAMS) | DLL/CvTeam.h:500; alloc DLL/CvTeam.cpp:60; free :113 |
| reset own row / other teams' column | DLL/CvTeam.cpp:261, :287 (only when not constructor call and id valid) |
| `isOpenBorders(eIndex)` | DLL/CvTeam.h:293, DLL/CvTeam.cpp:4646-4651 |
| `setOpenBorders(eIndex, b)` (not exposed to Python) | DLL/CvTeam.h:294, DLL/CvTeam.cpp:4654-4691 |
| `isFreeTrade(eIndex)` = !war && met && (OB or game FreeTrade vote) | DLL/CvTeam.cpp:4630-4643 |
| `signOpenBorders(eTeam)` (builds dual OB deal between leaders) | DLL/CvTeam.cpp:2244-2268 |
| tech gate `m_iOpenBordersTradingCount`, `isOpenBordersTrading()` | DLL/CvTeam.h:208-210, :471; DLL/CvTeam.cpp:4012-4028; incremented in `processTech` DLL/CvTeam.cpp:6824-6827 |
| AI counter `m_aiOpenBordersCounter` | DLL/CvTeamAI.h:173-175, :228; DLL/CvTeamAI.cpp:61, 82, 118, 134, 3701-3721 |
| pure virtual counter hooks on CvTeam | DLL/CvTeam.h:429-430 |

`setOpenBorders` side effects (DLL/CvTeam.cpp:4662-4689), in order:
1. remembers old `isFreeTrade`;
2. writes the flag;
3. `AI_setOpenBordersCounter(eIndex, 0)` (attitude counter reset on both sign and cancel);
4. `GC.getMapINLINE().verifyUnitValidPlot()` - full-map scan; bumps units that may no
   longer stand where they are (DLL/CvPlot.cpp:805-895, test at :835);
5. Score dirty bit for the active team;
6. if free-trade status changed: `updateTradeRoutes()` for every player of THIS team only
   (the other team updates when its own flag flips).

### 1.2 How a deal creates OB

- Trade item `TRADE_OPEN_BORDERS` (DLL/CvEnums.h:1960). `CvDeal::isAnnual` (DLL/CvDeal.cpp:1307),
  `isDual` (:1322), `hasData` false (:1339). `isDual`/`isAnnual`/`hasData` are DllExport
  (DLL/CvDeal.h:63-65): the EXE trade screen mirrors dual items onto both sides.
- Availability: `CvPlayer::canTradeItem` case at DLL/CvPlayer.cpp:5658-5672: different teams,
  not at war, not already OB, and either team has `isOpenBordersTrading()` (tech flag
  `bOpenBordersTrading`, only TECH_TRADE in XML/Technologies/CIV4TechInfos.xml:3988).
  `CvPlayer::canTradeWith` also lists the tech (DLL/CvPlayer.cpp:5378).
- Denial: `CvPlayer::getTradeDenial` -> `CvTeamAI::AI_openBordersTrade` (DLL/CvPlayer.cpp:5785-5786,
  DLL/CvTeamAI.cpp:3408-3460).
- Trade table / strings: `buildTradeTable` DLL/CvPlayer.cpp:23779-23783,
  `getItemTradeString` :24031-24032, `CvGameTextMgr::getTradeString` DLL/CvGameTextMgr.cpp:15455-15456,
  `CvDLLWidgetData::parseTradeItem` DLL/CvDLLWidgetData.cpp:4725-4726.
- Execution: `CvGame::implementDeal` (DLL/CvGame.cpp:2618-2633) -> `CvDeal::addTrades`
  (DLL/CvDeal.cpp:118-293) -> `startTrade` case DLL/CvDeal.cpp:1015-1036:
  - item with `m_iData == 0` (as offered from the UI/AI): calls
    `startTeamTrade(TRADE_OPEN_BORDERS, fromTeam, toTeam, bDual=true)` (DLL/CvDeal.cpp:1192-1224),
    which implements one sub-deal per (fromPlayer, toPlayer) pair containing `OB(m_iData=1)`
    on both sides, and THEN sets the team flag `GET_TEAM(from).setOpenBorders(to, true)`.
    The `m_iData==0` item is NOT saved in the outer deal (bSave stays false).
  - item with `m_iData == 1` (team sub-deal): only `bSave = true`, flag already set.
  - The second (mirrored) OB item of the outer deal creates no extra sub-deal because
    `canTradeItem` now fails (flag already set on one side) and the empty deal is killed;
    it only sets the reverse flag. Correctness depends on this ordering.
- Consequence: an "OB + 10 gpt" offer becomes two independent deals (gpt in the outer deal,
  OB in the team sub-deal). See defect 6.4.

### 1.3 How OB ends

- `CvDeal::kill(bKillTeam)` (DLL/CvDeal.cpp:77-116) calls `endTrade` for both lists
  (:106, :111). `endTrade` OB case DLL/CvDeal.cpp:1142-1167:
  `setOpenBorders(to, false)`, then `endTeamTrade` kills every sibling OB sub-deal between the
  two teams (DLL/CvDeal.cpp:1226-1272, uses `kill(false)`), then gives every player of the
  receiving team `MEMORY_CANCELLED_OPEN_BORDERS` (+1) against every player of the giving team.
  Since kill() runs both lists, BOTH teams always receive the memory.
- Cancelable after `PEACE_TREATY_LENGTH` turns (`turnsToCancel`, DLL/CvDeal.cpp:1274-1296).
- AI cancellation loop in `CvPlayerAI::AI_doDiplo` (DLL/CvPlayerAI.cpp:16995-17122): deals older
  than 2*PEACE_TREATY_LENGTH; vs AI: cancel if any of our items now has a denial
  (`getTradeDenial`, :17010/:17031); vs human: cancel if `AI_considerOffer(..., -1)` fails
  (:17001/:17022). See defect 6.3.
- War: `CvTeam::declareWar` kills ALL deals between the two teams (DLL/CvTeam.cpp:1440-1447)
  before `setAtWar` (:1459-1460); final `verifyUnitValidPlot` at :1537.
- Permanent alliance: `CvTeam::addTeam` kills OB/DP/peace/vassal deals between the merging
  teams (DLL/CvTeam.cpp:556-591), then copies OB flags with third teams directly (no deals) via
  `setOpenBorders` both ways (DLL/CvTeam.cpp:650-670); `shareCounters` takes the max OB counter
  (DLL/CvTeam.cpp:929-932).
- Vassal/master: no automatic OB. `AI_openBordersTrade` never denies to our master
  (DLL/CvTeamAI.cpp:3422-3425). `CvTeam::setVassal` (DLL/CvTeam.cpp:4809ff.) only kills DP and
  peace-treaty deals with third parties (:4900-4925); `freeVassal` kills only vassal deals
  (DLL/CvTeam.cpp:5153-5203). Master always treats vassal land as friendly; vassal treats
  master land as friendly only WITH OB (`isFriendlyTerritory`, DLL/CvTeam.cpp:7029-7051, OB at :7046).
- Team reset/elimination: `CvTeam::reset` clears both directions (DLL/CvTeam.cpp:261, 287).

### 1.4 Votes

- `VOTE_OPEN_BORDERS` (Apostolic Palace source, XML/GameInfo/CIV4VoteInfo.xml:512; flag
  `CvVoteInfo::isOpenBorders`, DLL/CvInfos.cpp:20386, 20464, 20522, 20561; Python
  DLL/CyInfoInterface3.cpp:193).
  - validity: `CvGame::isValidVoteSelection` DLL/CvGame.cpp:4277-4302 (invalid if all full members
    already have OB with each other);
  - proposer check: `CvPlayer::canDoResolution` DLL/CvPlayer.cpp:23115-23131;
  - defiance: `CvPlayer::canDefyResolution` DLL/CvPlayer.cpp:23240-23254;
  - effect: `CvGame::processVote` DLL/CvGame.cpp:7786-7804 -> `CvTeam::signOpenBorders` for every
    pair of voting members;
  - text: `CvGame::addVoteSelection` DLL/CvGame.cpp:9313-9317 (`TXT_KEY_POPUP_ELECTION_OPEN_BORDERS`);
  - AI vote: `CvPlayerAI::AI_diploVote` DLL/CvPlayerAI.cpp:8322-8352 (yes if friendly to secretary or
    no team denies `AI_openBordersTrade`).
- `VOTE_FREE_TRADE` (UN, XML/GameInfo/CIV4VoteInfo.xml:101): `CvGame::changeFreeTradeCount`
  (DLL/CvGame.cpp:3827-3843) makes `isFreeTrade` true for everyone -> trade-route half of OB.
  AI evaluation counts cities of OB partners (DLL/CvPlayerAI.cpp:8272-8312, OB at :8296).

### 1.5 Save / load

| Data | Write | Read | Notes |
|---|---|---|---|
| `m_iOpenBordersTradingCount` | DLL/CvTeam.cpp:7452 | :7343 | uiFlag=0, no versioning yet (:7329/:7438) |
| `m_abOpenBorders[MAX_TEAMS]` | DLL/CvTeam.cpp:7484 | :7375 | between PermanentWarPeace and DefensivePact |
| `m_aiOpenBordersCounter` | DLL/CvTeamAI.cpp:4034 | :4011 | uiFlag=0 |
| deals (TradeData with numeric `m_eItemType`) | DLL/CvDeal.cpp:661-673 | :676-690 | uiFlag=0; item type stored as int -> enum renumbering breaks old saves |
| contact timers `[MAX_PLAYERS][NUM_CONTACT_TYPES]` | DLL/CvPlayerAI.cpp:19052 | :18847 | array size from enum; CvPlayerAI already versioned (uiFlag=6 at :18989, checks at :18773-18941) |
| memory `[MAX_PLAYERS][NUM_MEMORY_TYPES]` | DLL/CvPlayerAI.cpp:19056 | :18851 | same |
| diplomacy parameters offer lists | DLL/CvDiploParameters.cpp:250-271 | :221-246 | TradeData numeric too |
| info cache (tech flag, leaderhead OB fields) | DLL/CvInfos.cpp:1835, 19483-19506 | :1752, 19323-19346 | XML cache stream, rebuilt from XML |

Precedent for versioned reads: DLL/CvCityAI.cpp:13474 (`if (uiFlag >= 1)`), DLL/CvGame.cpp:8283/8330,
DLL/CvPlayerAI.cpp:18773-18941.

### 1.6 Python exposure (DLL side)

- `CyTeam`: `signOpenBorders`, `getOpenBordersTradingCount`, `isOpenBordersTrading`,
  `changeOpenBordersTradingCount`, `isFreeTrade`, `isOpenBorders`
  (DLL/CyTeam.cpp:86-90, 415-430, 690-693; DLL/CyTeamInterface.cpp:35, 116-118, 172-173).
- `CyPlayer.canHaveTradeRoutesWith` (DLL/CyPlayerInterface2.cpp:73), `canTradeItem`,
  `canTradeNetworkWith` (DLL/CyPlayerInterface1.cpp:132-134), `AI_get/changeMemoryCount`.
- `CyUnit/CySelectionGroup.canEnterTerritory/canEnterArea(eTeam, ..., bIgnoreRightOfPassage)`
  (DLL/CyUnitInterface1.cpp:36-37, DLL/CySelectionGroupInterface.cpp:39-40), `CyPlot.isFriendlyCity`
  (DLL/CyPlotInterface1.cpp:93).
- Info: `CvTechInfo.isOpenBordersTrading` (DLL/CyInfoInterface1.cpp:80); leaderhead
  `getOpenBordersAttitudeDivisor/ChangeLimit/RefuseAttitudeThreshold`
  (DLL/CyInfoInterface3.cpp:114-115, 137); `CvVoteInfo.isOpenBorders/isFreeTrade` (:188, :193).
- Enums: `WIDGET_HELP_OPEN_BORDERS`, `OPEN_BORDERS_CHAR`, `TRADE_OPEN_BORDERS`,
  `CONTACT_OPEN_BORDERS`, `MEMORY_CANCELLED_OPEN_BORDERS`
  (DLL/CyEnumsInterface.cpp:370, 753, 1432, 1500, 1536). The whole TradeableItems export is
  DLL/CyEnumsInterface.cpp:1424-1447 (includes NUM_BASIC_ITEMS / NUM_TRADEABLE_HEADINGS).

### 1.7 UI and text

DLL:
- Tech help "enables open borders": `buildOpenBordersString` DLL/CvGameTextMgr.cpp:14306-14316,
  called from `setTechTradeHelp` :8503; widget `WIDGET_HELP_OPEN_BORDERS`
  (DLL/CvDLLWidgetData.cpp:364-365, 942, 5391-5394).
- Attitude line "open borders +N": `getAttitudeString` DLL/CvGameTextMgr.cpp:15256-15260.
- Leader relation hover: `parseLeaderLineHelp` DLL/CvGameTextMgr.cpp:16536-16539.
- Trade route hover "cannot trade: closed borders": `buildTradeString`
  DLL/CvGameTextMgr.cpp:19288, 19309-19336 (uses `canHaveTradeRoutesWith` and `isFreeTrade`).
- Raze/gift popup: DLL/CvDLLButtonPopup.cpp:1419-1422 (and the same test in
  `CvPlayer::acquireCity` DLL/CvPlayer.cpp:2889-2894).
- "Declare war to enter?" popup hint `TXT_KEY_POPUP_ENTER_WITH_OPEN_BORDERS`:
  DLL/CvDLLButtonPopup.cpp:1700-1703.
- Icon `[ICON_OPENBORDERS]` -> `OPEN_BORDERS_CHAR` (DLL/CvDllTranslator.cpp:33,
  DLL/CvEnums.h:999). FontSymbols are bound to the game font atlas; new icons are not free.
- Rebase help uses `isFriendlyCity` (DLL/CvGameTextMgr.cpp:19563).

Python:
- Scoreboard OB icon: Py/Screens/CvMainInterface.py:5382-5386, Py/Screens/CvMainInterface-PLE.py:4819-4823,
  BUG column 'B' Py/BUG/Scoreboard.py:74-79, 113, 273-274.
- Foreign advisor relation lines + legend: Py/Screens/CvForeignAdvisor.py:511, 694, 740.
- Exotic foreign advisor trade column: Py/Screens/CvExoticForeignAdvisor.py:689 (`canHaveTradeRoutesWith`).
- Tech tree OB icon: Py/Screens/CvTechChooser.py:652-654, 1372 (art `INTERFACE_TECH_OPENBORDERS`,
  XML/Art/CIV4ArtDefines_Interface.xml:602).
- BUG trade utilities: Py/BUG/TradeUtil.py:162-174 (`canSignOpenBorders`), :520, :676;
  Py/BUG/DealUtil.py:60, 99-130 (isAnnual/isDual/hasData mirrors of CvDeal), :292;
  Py/BUG/AttitudeUtil.py:46 (parses `TXT_KEY_MISC_ATTITUDE_OPEN_BORDERS`);
  Py/Contrib/MoreCiv4lerts.py:77, 112-113, 374-380, 462-467 + option Py/BUG/Tabs/BugAlertsOptionsTab.py:47;
  font symbol map Py/CvUtil.py:595.
- Py/CvDiplomacy.py has no OB-specific code (the trade screen is in the EXE).
- All Python uses symbolic `TradeableItems.*` names; no numeric trade-item constants found.

XML:
- Text keys used (`TXT_KEY_TRADE_OPEN_BORDERS[_STRING]`, `TXT_KEY_MISC_OPEN_BORDERS`,
  `TXT_KEY_MISC_ATTITUDE_OPEN_BORDERS`, `TXT_KEY_MISC_ENABLES_OPEN_BORDERS`,
  `TXT_KEY_POPUP_ENTER_WITH_OPEN_BORDERS`, `TXT_KEY_POPUP_ELECTION_OPEN_BORDERS`,
  `TXT_KEY_VOTE_OPEN_BORDERS`, `TXT_KEY_MEMORY_CANCELLED_OPEN_BORDERS`) mostly come from the base
  BtS text, not this tree; mod-local: `TXT_KEY_BUG_CANNOT_TRADE_CLOSED_BORDERS`
  (XML/Text/BULL_CIV4GameText.xml:1082), `TXT_KEY_MORECIV4LERTS_OPEN_BORDERS`
  (XML/Text/MoreCiv4lerts_CIV4GameText.xml:219).
- Leaderheads: `iOpenBordersAttitudeDivisor`, `iOpenBordersAttitudeChangeLimit`,
  `OpenBordersRefuseAttitudeThreshold`, `ContactRand/ContactDelay CONTACT_OPEN_BORDERS`,
  `MemoryDecay MEMORY_CANCELLED_OPEN_BORDERS` (e.g. XML/Civilizations/CIV4LeaderHeadInfos.xml:63-64, 86,
  278-279, 301, 359, 417, 503; 59 leaders). No `MemoryAttitudePercent` for the cancel memory: it
  only feeds `DENIAL_RECENT_CANCEL`. Copies in every module schema/leaderhead file under
  `Assets/Modules/Custom Leaderheads/*` and `Assets/Unloaded Modules/Realistic Diplomacy`.
- `CONTACT_OPEN_BORDERS` in XML/GlobalTypes.xml:78 (loaded positionally against NUM_CONTACT_TYPES,
  DLL/CvXMLLoadUtilitySet.cpp:537-538); `MEMORY_CANCELLED_OPEN_BORDERS` XML/BasicInfos/CIV4MemoryInfos.xml:114.
- Schemas: XML/Technologies/CIV4TechnologiesSchema.xml, XML/Civilizations/CIV4CivilizationsSchema.xml,
  XML/GameInfo/CIV4GameInfoSchema.xml (+ per-module copies).
- Relevant defines (XML/GlobalDefines.xml): NEUTRAL_HEAL_RATE 10 (:449), FRIENDLY_HEAL_RATE 15 (:453),
  ESPIONAGE_SPY_INTERCEPT_MOD -75 (:1490), ESPIONAGE_SPY_NO_INTRUDE_INTERCEPT_MOD -90 (:1494),
  IGNORE_PLOT_GROUP_FOR_TRADE_ROUTES 0 (:1614), USE_SPIES_NO_ENTER_BORDERS 0 (:1658);
  XML/TechDiffusion_GlobalDefines.xml TECH_DIFFUSION_ENABLE 1.

---------------------------------------------------------------------------------------

## 2. Every effect of Open Borders

### 2.1 Unit entry and movement

- `CvUnit::canEnterTerritory(eTeam, bIgnoreRightOfPassage)` DLL/CvUnit.cpp:2462-2503. Allowed if:
  friendly territory (:2464; own, our vassal, or our master WITH OB), unowned, at war,
  `bRivalTerritory` unit, `bInvisible` unit, `bHiddenNationality` unit, or
  (!bIgnoreRightOfPassage && `GET_TEAM(unitTeam).isOpenBorders(eTeam)`) (:2496). [C]/[M] by unit
- `canEnterArea` adds the barbarian border-obstacle rule (DLL/CvUnit.cpp:2506-2526).
- `canMoveInto` DLL/CvUnit.cpp:2591-2950: `canEnterArea` at :2629 (also gates feature/terrain
  impassable checks), humans re-evaluated on the revealed owner (:2894-2897); without entry right
  a human needs `bDeclareWar`, the AI needs `AI_isSneakAttackReady && AI_isDeclareWar` (:2899-2932).
  `canMoveThrough` = `canMoveInto(.., false, false, true)` (:2959-2962). [C]/[M]
- Units in the wrong place are expelled by `CvPlot::verifyUnitValidPlot` (DLL/CvPlot.cpp:835) ->
  `jumpToNearestValidPlot` (DLL/CvUnit.cpp:3147-3227, entry test :3172). Triggered on every OB flip
  (DLL/CvTeam.cpp:4670), on war (:1537) and elsewhere (DLL/CvPlayer.cpp:2823, 22665,
  DLL/CvArea.cpp:739, DLL/CvPlot.cpp:443/5044/5741). [C]/[M]
- Human "declare war to move" detection: `getDeclareWarMove` DLL/CvUnit.cpp:2529-2567 uses
  `canEnterArea` and, for ships, `canCargoEnterArea(.., false)` (DLL/CvUnit.cpp:10198-10215: every cargo
  unit must have the right). [C]/[M]; a transport may be civilian while its cargo is military.
- Units that bypass OB completely (XML/Units/CIV4UnitInfos.xml): `bRivalTerritory`: UNIT_SPY,
  UNIT_NANITE_SPY, UNIT_GREAT_SPY, UNIT_MERCHANT (great merchant), UNIT_TRADE_CARAVAN,
  UNIT_TRADE_MERCHANT_MAN, UNIT_FREIGHT, UNIT_ENTERTAINER, UNIT_CRUSADER, UNIT_TREASURE,
  caravel-class explorers (CARAVEL, CHINA_JUNK, PORTUGAL_CARRACK, FLUYT, SLOOP, OOSTINDIEVAARDER,
  BRIGANTINE), all submarines; `bHiddenNationality`: GUERRILLA, PRIVATEER, SR71 and the UN module
  units; module spies (Special Agent, 007, Agent). Units that DO need OB include workers, settlers,
  work boats, scouts/explorers (combat 1/3, bOnlyDefensive, UNITCOMBAT_RECON), missionaries,
  executives, prophets, great generals, all regular military.

### 2.2 Ports, air bases, cargo, paradrop (via `CvPlot::isFriendlyCity`)

`isFriendlyCity` DLL/CvPlot.cpp:3563-3603 is true for a foreign city if the unit's combat-owner
team has OB with the city team (:3591) or the city is our vassal. Used by:
- ships entering coastal land cities (DLL/CvUnit.cpp:2681) [M] (work boats/transports: [C]?);
- air units landing/basing (DLL/CvUnit.cpp:2693), `shouldLoadOnMove` (:3587), `canUnload` air
  capacity (:3696), air fallback in `jumpToNearestValidPlot` (:3176) [M];
- paradrop must start in a friendly city (DLL/CvUnit.cpp:4580) [M];
- `CvSelectionGroup::isAmphibPlot` (DLL/CvSelectionGroup.cpp:5040), AI naval targeting
  (DLL/CvSelectionGroup.cpp:2186-2209), AI (DLL/CvUnitAI.cpp:23760) [M];
- rebase help text (DLL/CvGameTextMgr.cpp:19563) [M].
- Airlift is NOT OB: source and target must be own team or vassal (DLL/CvUnit.cpp:4061-4131). [-]

### 2.3 Path finding and MOVE_* flags

- No MOVE_* flag (DLL/CvDefines.h:10-25) mentions OB. `MOVE_SAFE_TERRITORY` = own territory only,
  `MOVE_NO_ENEMY_TERRITORY` = not at war; OB enters the unit path finder only through
  `canMoveOrAttackInto` in `pathDestValid` (DLL/CvGameCoreUtils.cpp:1696, 1716) and
  `canMoveThrough` in the pathValid helper (DLL/CvGameCoreUtils.cpp:~2007-2115). [C]/[M] by unit
- Team step finder `teamStepValid` (DLL/CvGameCoreUtils.cpp:2339-2405): plot passable if unowned,
  target team, friendly territory, war plan, or `isOpenBorders(plotTeam)` (:2396). Used by
  `CvPlot::isHasPathToEnemyCity / isHasPathToPlayerCity / calculatePathDistanceToPlot`
  (DLL/CvPlot.cpp:2965, 3044, 3087) -> city production assault decision
  (DLL/CvCityAI.cpp:2588), BarbarianCiv victim choice (DLL/CvTeam.cpp:3413), inquisitor targeting
  (DLL/CvPlayerAI.cpp:25140-25245), debug text (DLL/CvGameTextMgr.cpp:4387-4399). [?] team-level
- `CvSelectionGroup::groupDeclareWar` uses `canEnterArea(.., bIgnoreRightOfPassage=true)`
  (DLL/CvSelectionGroup.cpp:4312): an AI stack stepping into a sneak-attack target declares war even
  if OB would let it in. [M] (should ignore all three rights)
- Path reuse (DLL/CvSelectionGroup.cpp:47-90, DLL/AIPathReuse.h) keys on group, mission epoch,
  turn and moves; OB/war changes do not invalidate it (see 6.9).

### 2.4 Trade routes and foreign commerce

- `CvTeam::isFreeTrade` (DLL/CvTeam.cpp:4630-4643) -> `CvPlayer::canHaveTradeRoutesWith`
  (DLL/CvPlayer.cpp:23402-23435; even vassal/master need it) -> `CvCity::updateTradeRoutes`
  (DLL/CvCity.cpp:12576; partner city must also share our plot group, :12583). [T]
- `setOpenBorders` refreshes trade routes when free-trade status flips (DLL/CvTeam.cpp:4677-4688). [T]
- AI: `countPotentialForeignTradeCities[Connected]` (DLL/CvPlayer.cpp:4963-5030) used in strategic
  context (DLL/CvPlayerAI.cpp:4441), tech value of water trade (:5471), civic value (:12987). [T]
- `CvPlayerAI::AI_stopTradingTradeVal` doubles the embargo price if the asking player has OB with
  the target (DLL/CvPlayerAI.cpp:10383). [T]
- Free Trade vote evaluation counts OB partners' cities (DLL/CvPlayerAI.cpp:8296). [T]
- UI: `buildTradeString` (DLL/CvGameTextMgr.cpp:19309-19336), exotic advisor (Py/Screens/CvExoticForeignAdvisor.py:689). [T]
- Event: Tea event requires some `canHaveTradeRoutesWith` partner
  (Py/EntryPoints/CvRandomEventInterface.py:2396). [T]

### 2.5 Resource trade and the trade network [-] (not coupled today)

- `TRADE_RESOURCES` requires only `canTradeNetworkWith` (capital connected, DLL/CvPlayer.cpp:5455,
  5805-5820); `CvDeal::verify` cancels resource deals on disconnection, not on OB
  (DLL/CvDeal.cpp:334-383).
- Plot groups: `CvPlot::isTradeNetwork` / `isTradeNetworkConnected` (DLL/CvPlot.cpp:3879-3990) depend on
  war, blockade, revealed, routes/rivers/terrain-trade; the only borders-related piece is
  `isCity(true, eTeam)` for "acts as city" improvements, which uses `isFriendlyTerritory`
  (DLL/CvPlot.cpp:3552; OB matters only vassal->master).
- Passive religion spread uses `isConnectedTo` (plot groups), not OB (DLL/CvCity.cpp:13862).

### 2.6 Religion and corporation spread

- Missionaries/prophets: `CvUnit::canSpread` requires `canEnterArea` (DLL/CvUnit.cpp:6236). [C]
- Executives: `canSpreadCorporation` (DLL/CvUnit.cpp:6365). [C] (corporations are commerce, but the
  gate is unit entry)
- AI targeting: `AI_spreadReligion` (DLL/CvUnitAI.cpp:12841), `AI_spreadCorporation` (:13073) use
  `canEnterTerritory`; `AI_missionaryValue` (DLL/CvPlayerAI.cpp:12187) and `AI_executiveValue`
  (:12358) count only civs that have OB with us; `AI_getStrategyHash` missionary strategy
  (:21311). [C]

### 2.7 Espionage

- Spy entry: spies are `bRivalTerritory` + `bInvisible`; `USE_SPIES_NO_ENTER_BORDERS` (0) path
  (DLL/CvUnit.cpp:2616-2623, `canSpiesEnterBorders` DLL/CvPlayer.cpp:23590) is about passive missions,
  not OB. [-]
- Interception each turn: intruding spy in OB territory uses ESPIONAGE_SPY_NO_INTRUDE_INTERCEPT_MOD
  (-90) instead of -75 (DLL/CvUnit.cpp:744-757, OB at :749). [C]?
- Bribe unit mission requires friendly territory or OB with the target (DLL/CvPlayer.cpp:23494). [?]
  (the bribed unit is usually military, so [M] is the natural reading)

### 2.8 Culture, borders, war weariness

- `CvPlot::countFriendlyCulture` (DLL/CvPlot.cpp:10245-10262, OB at :10255) adds culture of teams that
  have OB with the fighter; used by `CvTeam::changeWarWeariness(.., kPlot, ..)`
  (DLL/CvTeam.cpp:4325-4353) for every combat/capture weariness event (DLL/CvUnit.cpp:1573-1634,
  10583-10584, 10713, 15957-15958). Fighting on an OB partner's soil counts as home soil. [M]
- Improvement defence bonus only in friendly territory (DLL/CvPlot.cpp:2743; OB matters only for
  vassal in master land). [M]
- No effect on culture spread or border growth. [-]

### 2.9 Great people, missionaries, settlers, workers

- Entry-gated (2.1): workers (incl. road building in foreign land, which `CvPlot::canBuild` allows,
  DLL/CvPlot.cpp:2271ff.), settlers (paths only; cannot found inside foreign borders anyway),
  missionaries, executives, great prophet, great general, scouts/explorers. [C] (general: [M]?)
- Great merchant trade mission (`canTrade` DLL/CvUnit.cpp:6852) is entry-gated in code but
  UNIT_MERCHANT is `bRivalTerritory`, so effectively ungated. [-]
- Other GP actions (great work, join, hurry, construct, discover, golden age) are own-city/
  own-team only. [-]
- Unit gifting requires standing in the recipient's territory (DLL/CvUnit.cpp:3359-3424), i.e.
  needs the entry right of the gifted unit. [C]/[M] by unit

### 2.10 Healing

- `healRate` (DLL/CvUnit.cpp:3919-4023): city heal + city building heal applies in ANY city the unit
  stands in (foreign OB city included); friendly vs neutral extra heal uses `isFriendlyTerritory`
  (:3938, :3951). OB therefore matters (a) indirectly by allowing presence and (b) directly only
  for a vassal in its master's land (FRIENDLY 15 vs NEUTRAL 10). [M] (presence: by unit)

### 2.11 Upgrades, airlift, unit supply

- Upgrade: own territory only unless `isUpgradeAnywhere` (DLL/CvUnit.cpp:8037-8060). [-]
- Airlift: own/vassal (2.2). [-]
- Outside-unit counting in `setVassal` (DLL/CvTeam.cpp:4825-4862) is vassal-based, not OB. [-]

### 2.12 AI attitude and memory

- `AI_doCounter` +1 per turn while OB (DLL/CvTeamAI.cpp:4426-4429); reset on any flip
  (DLL/CvTeam.cpp:4668).
- `AI_getOpenBordersAttitude` = counter / iOpenBordersAttitudeDivisor, clamped to
  +-ChangeLimit, zero at war (DLL/CvPlayerAI.cpp:7868-7881); summed in `AI_getAttitudeVal`
  (:7465); shown in `getAttitudeString` (DLL/CvGameTextMgr.cpp:15256). Default leaders: /25, limit 2.
- `MEMORY_CANCELLED_OPEN_BORDERS` (DLL/CvDeal.cpp:1148-1166) -> `DENIAL_RECENT_CANCEL`
  (DLL/CvTeamAI.cpp:3432); decays with iMemoryRand 10; no attitude weight.
- Close-borders attitude (DLL/CvPlayerAI.cpp:7722-7758) is about shared/stolen plots and land
  targets, NOT OB. [-]
- OB value also flows into peacetime trade value (`CvDeal::addTrades` :205/:218, `doTurn`
  :304/:318), hence `AI_getTradeAttitude` (DLL/CvPlayerAI.cpp:7994-7998); symmetric OB mostly
  cancels out there.

### 2.13 Diplomacy valuation and denial

- Value: `AI_openBordersTradeVal` = our cities + their cities (DLL/CvTeamAI.cpp:3402-3405);
  `AI_dealVal` (DLL/CvPlayerAI.cpp:8874-8876). Symmetric, so OB-for-OB always balances.
- Denial `AI_openBordersTrade` (DLL/CvTeamAI.cpp:3408-3460): human never denies; vassal of eTeam or
  shared war -> no denial; recent cancel memory; worst enemy; attitude <= any member's
  `OpenBordersRefuseAttitudeThreshold`. Nothing about war plans, power, or units.
- Tech value of `bOpenBordersTrading` (DLL/CvPlayerAI.cpp:5367-5385; extra for minors under
  START_AS_MINORS).

### 2.14 Tech diffusion

- DLL TECH_DIFFUSION: known-tech exponent +1.5 per team with OB (or our vassal)
  (DLL/CvPlayer.cpp:8367 in `calculateResearchModifier`). [T]? (knowledge travels with trade)
- Python Revolution TechDiffusion: OB partner = 3 diffusion power (Py/Revolution/Gameready/TechDiffusion.py:186). [T]?

### 2.15 City liberation gift

- Gift option after conquest only if the liberation player is same team, has OB with us, or is
  our vassal (DLL/CvPlayer.cpp:2889-2894, DLL/CvDLLButtonPopup.cpp:1419-1422). [?]

### 2.16 Victory conditions, events

- No victory condition reads OB. [-]
- Events: Tea (2.4); event-triggered war declarations kill OB like any war
  (DLL/CvPlayer.cpp:20750). No event grants or reads OB directly. [-]

### 2.17 Minor civs / Revolution (Python)

- START_AS_MINORS: a minor becomes a full civ when it gains `bOpenBordersTrading`
  (Py/Revolution/Gameready/StartAsMinors.py:109, 134; Py/Revolution/Gameready/BarbarianCiv.py:1778). Tech gate.
- Revolution signs OB on peaceful reincarnation / join (Py/Revolution/Gameready/Revolution.py:5416,
  5634, 5869). [?] (probably all three)
- Rebel spawn/retreat plots may lie in OB territory of the spawning player
  (Py/Revolution/RevUtils.py:211, 263; default `bOpenBordersPlots=True` used by
  Py/Revolution/Gameready/Revolution.py:830-834, 6541, 6544, 6665, 6668). [M]

### 2.18 Complete list of Python readers of OB state

`isOpenBorders`: CvMainInterface.py:5382, CvMainInterface-PLE.py:4819, CvForeignAdvisor.py:694, 740,
RevUtils.py:263, TechDiffusion.py:186, BUG/TradeUtil.py:172.
`isOpenBordersTrading` (tech gate): BUG/TradeUtil.py:174, StartAsMinors.py:109, 134 (tech info),
BarbarianCiv.py:1778, CvTechChooser.py:652 (tech info).
`signOpenBorders`: Revolution.py:5416, 5634, 5869.
`TRADE_OPEN_BORDERS`: MoreCiv4lerts.py:465, BUG/TradeUtil.py:520, 676, BUG/DealUtil.py:60, 104, 113,
124, 292, BUG/Scoreboard.py:75, 274.
`canHaveTradeRoutesWith`: CvRandomEventInterface.py:2396, CvExoticForeignAdvisor.py:689.

---------------------------------------------------------------------------------------

## 3. AI behaviour that depends on OB

- Movement/exploration/settling/working: no explicit OB logic; everything goes through
  `canMoveInto` in the path finder (2.3). Explorers (UNITAI_EXPLORE), settler escorts, worker
  `AI_improve*`, missionaries and executives only plan through/into civs whose land they may enter.
  Note explorers have combat 3/bOnlyDefensive; a naive "combat > 0 => military" classifier would
  move them into military access.
- Missionary/executive economics: 2.6 (`AI_missionaryValue`, `AI_executiveValue`,
  `AI_getStrategyHash`).
- War planning:
  - `teamStepValid` treats OB land as passable when deciding whether enemies are reachable by land
    (assault ship production decision DLL/CvCityAI.cpp:2588; BarbCiv victim DLL/CvTeam.cpp:3413).
  - Attack stacks path into a sneak-attack target and declare war on entry
    (`AI_isDeclareWar` DLL/CvSelectionGroupAI.cpp:671; `groupPathTo` -> `groupDeclareWar`
    DLL/CvSelectionGroup.cpp:4688, 4312). OB is ignored for that test.
  - Units already inside the target's land via OB are teleported out when war is declared
    (deal kill before setAtWar, DLL/CvTeam.cpp:1440-1460 + :4670). `jumpToNearestValidPlot` uses
    `setXY`, which splits the group; `groupDeclareWar` then reports "bumped" (unit count changed).
  - The AI happily signs/keeps OB with a team it plans to attack: neither `AI_openBordersTrade`
    nor the proposal code checks `AI_getWarPlan` (DLL/CvTeamAI.cpp:3408-3460, DLL/CvPlayerAI.cpp:18054-18100).
  - Vassal naval reinforcement goes to the master's offensive areas only with OB
    (`AI_assaultSeaReinforce` DLL/CvUnitAI.cpp:17908).
- Proposals (`AI_doDiplo` DLL/CvPlayerAI.cpp:18054-18100): only the team leader; contact timer
  `CONTACT_OPEN_BORDERS`; 1/ContactRand chance; both sides must pass `canTradeItem(.., bTestDenial)`;
  humans get a diplo popup, AIs get an immediate deal.
- Cancellation (`AI_doDiplo` DLL/CvPlayerAI.cpp:16995-17122): see 1.3 and 6.3.
- Attitude: `AI_getOpenBordersAttitude` (+1 per 25 turns, max +2 for default leaders).
- Votes: `AI_diploVote` for OB vote and Free Trade vote (1.4).
- Tech research: TECH_TRADE valued +500/+400 for OB trading (DLL/CvPlayerAI.cpp:5367-5385).
- Close-borders attitude is unrelated (2.12).

---------------------------------------------------------------------------------------

## 4. Effect -> proposed agreement

| # | Effect (site) | Agreement | Ambiguity / reasoning |
|---|---|---|---|
| 1 | Land/sea unit entry `canEnterTerritory` (CvUnit.cpp:2496) and everything built on it (canMoveInto, path finder, verifyUnitValidPlot, getDeclareWarMove, canCargoEnterArea, gifting) | C or M by unit | Needs a unit classifier. Edge cases: explorers/scouts (combat>0, bOnlyDefensive, recon), transports (combat, bOnlyDefensive, carry military cargo), great general (combat 0 but military), work boats, caravans (already rival territory). Proposal: military = canAttack() && !isOnlyDefensive(), or DOMAIN_AIR, or great-general type; everything else civilian; optional XML override tag. |
| 2 | Foreign port / air base `isFriendlyCity` (CvPlot.cpp:3591) | M (C for civilian ships) | Team-level today but called with a unit; switch to the same unit-based right as #1. Air basing and paradrop are clearly M. |
| 3 | Vassal in master land = friendly (`isFriendlyTerritory` CvTeam.cpp:7046) -> entry, heal rate, fort defence, teamStepValid, bribe | M | Team-level predicate; healing and improvement defence are combat concerns. Entry for civilian vassal units should then be handled by #1, not by this predicate. |
| 4 | Trade routes `isFreeTrade` (CvTeam.cpp:4642) and its users (2.4) | T | Clear. |
| 5 | Resource trading / trade network | (T) | Not coupled today; gating it is new behaviour (needs canTradeItem, CvDeal::verify, AI changes). Plot-group connectivity through foreign roads should stay ungated or domestic connections break. |
| 6 | Missionary/executive/prophet spread (CvUnit.cpp:6236, 6365) and AI valuation (CvPlayerAI.cpp:12187, 12358, 21311; CvUnitAI.cpp:12841, 13073) | C | Executives could be argued T (corporations), but the gate is physical presence of a unit. |
| 7 | Spy interception modifier (CvUnit.cpp:749) | C | Spies do not need OB to enter; this is only "less suspicious with a visitor treaty". Could also be dropped. |
| 8 | Spy bribe-unit legality (CvPlayer.cpp:23494) | M | The bribed unit must be allowed to stand there; usually a military unit. Better: test the right matching the bribed unit type. |
| 9 | War-weariness culture ratio (CvPlot.cpp:10255) | M | "Fighting on allied soil". |
| 10 | teamStepValid (CvGameCoreUtils.cpp:2396) | M | Used for military reachability; inquisitor targeting (CvPlayerAI.cpp:25140ff.) is civilian - give that caller C or make the finder take the right as data. |
| 11 | groupDeclareWar ignore-ROP (CvSelectionGroup.cpp:4312) | M (ignore all) | Keep "ignore every right". |
| 12 | Vassal sea reinforcement (CvUnitAI.cpp:17908) | M | |
| 13 | OB attitude counter and attitude (CvTeamAI.cpp:4426, CvPlayerAI.cpp:7868) | all / ? | Either one counter for "any agreement" or three counters with separate leaderhead weights. Simplest: count turns with at least T, or weight T=1, C=1, M=2. |
| 14 | MEMORY_CANCELLED_OPEN_BORDERS + DENIAL_RECENT_CANCEL | all / ? | Shared memory is simplest; per-agreement memory needs new MemoryTypes (save + XML impact). |
| 15 | Tech diffusion (CvPlayer.cpp:8367, TechDiffusion.py:186) | T | Could be "any agreement"; trade is the historical carrier. |
| 16 | City liberation gift (CvPlayer.cpp:2893, CvDLLButtonPopup.cpp:1422) | ? | Pure diplomatic friendliness test; suggest "any agreement" (or T). |
| 17 | OB vote (AP) | ? | Probably signs all three (closest to current meaning) or only T+C; decide and mirror in canDoResolution/canDefyResolution/isValidVoteSelection/AI_diploVote. |
| 18 | Free Trade vote (UN) | T | Already only the trade half. |
| 19 | Embargo price doubling (CvPlayerAI.cpp:10383) | T | |
| 20 | Scoreboard / advisor / leader-line / BUG icons | each | One symbol today (OPEN_BORDERS_CHAR); need three markers or text. |
| 21 | Tech gate bOpenBordersTrading (TECH_TRADE), minor->full civ conversion | all or per agreement | Keep one flag gating all three initially; per-agreement tech flags are optional XML schema work. |
| 22 | Revolution `signOpenBorders` calls | all | Keep `signOpenBorders` as "sign all three". |
| 23 | Rebel spawn plots in OB land (RevUtils.py:263) | M | Rebels are combat units. |
| 24 | Healing in a foreign OB city | by unit (presence) | No direct OB test except #3. |
| 25 | Airlift, upgrades, resource trades, passive religion spread, culture | - | Not coupled. |

---------------------------------------------------------------------------------------

## 5. Implementation sketch

### 5.1 Decisions to take first

1. Symmetric or one-way? Current code is symmetric everywhere and the EXE mirrors any item with
   `CvDeal::isDual()==true`. Making the three agreements dual keeps every existing direction
   assumption valid (recommended for a first version). One-way agreements ("I grant you military
   access for gold") require fixing the direction convention at every call site (6.8).
2. Bundle or replace? Options: (a) keep TRADE_OPEN_BORDERS as a bundle item that sets all three
   rights and add three granular items; (b) repurpose TRADE_OPEN_BORDERS as one of the three and add
   two. (b) is less code; (a) is friendlier to Python/Revolution/votes. Overlapping items in (a)
   need clear cancellation rules (cancel bundle = clear only rights not backed by another deal).
3. Should trade rights gate resource trades (2.5)? If yes it is a new rule with AI impact.

### 5.2 Data

- Replace `bool* m_abOpenBorders` with `int* m_aiAccessRights` (bitmask per other team):
  `ACCESS_TRADE=1, ACCESS_CIVILIAN=2, ACCESS_MILITARY=4` (new enum in CvEnums.h, exposed to Python).
- API: `bool hasAccessRight(TeamTypes eOther, AccessRightTypes e) const`,
  `void setAccessRight(TeamTypes eOther, AccessRightTypes e, bool b)`, `int getAccessRights(eOther)`.
  Keep `isOpenBorders(eOther)` as a compatibility wrapper (recommend: "all three set") so Python
  and untouched UI keep working; add `CyTeam.hasAccessRight`.
- `setAccessRight` must replicate the side effects of `setOpenBorders` selectively:
  counter handling; `verifyUnitValidPlot` only when C or M changes (also skip when turning ON -
  the current code scans the whole map even when rights are granted); `updateTradeRoutes` only when
  T changes (`isFreeTrade` must read the T bit); score dirty bit; bump the path-reuse epoch
  (`CvSelectionGroup::noteMissionTargetsChanged`) when C/M change.
- Unit-level helper: `bool CvUnit::isMilitaryAccessUnit() const` (+ optional XML override) and
  `bool CvTeam::canUnitEnter(const CvUnit&, TeamTypes eHost)`.
- `CvTeamAI`: either keep one counter (turns with any right) or three counters (save impact).

### 5.3 TradeableItems placement

Facts from the tree:
- Enum DLL/CvEnums.h:1951-1986: basic items 0..8 (TRADE_OPEN_BORDERS=5), `NUM_BASIC_ITEMS`=9,
  `TRADE_TECHNOLOGIES`=9 ... `TRADE_RELIGION`=16, `NUM_TRADEABLE_HEADINGS`=17.
- In the EXE build (`#else` branch) the counters are not enum values: CvGlobals.h:1592-1594 map
  `NUM_BASIC_ITEMS/NUM_TRADEABLE_HEADINGS/NUM_TRADEABLE_ITEMS` to DllExport getters
  (DLL/CvGlobals.h:1017-1019, DLL/CvGlobals.cpp:4189-4191). So the EXE asks the DLL where basic items
  end and headings begin; the trade table content comes from DllExport `buildTradeTable`,
  `getHeadingTradeString`, `getItemTradeString`, `updateTradeList`, `canTradeItem`,
  `getTradeDenial` (DLL/CvPlayer.h:236-237, 1163-1166) and `CvDeal::isDual/isAnnual/hasData/...`
  (DLL/CvDeal.h:63-71). Whether the EXE also hard-codes values such as TRADE_TECHNOLOGIES=9 cannot be
  verified from source.
- Python only uses symbolic names (no numeric TRADE_* found), so Python is order-insensitive.

Options:
- A. Insert the new items in the basic range (after TRADE_PEACE_TREATY, before NUM_BASIC_ITEMS).
  Natural UI (single entries next to Open Borders), but shifts TRADE_TECHNOLOGIES..TRADE_RELIGION;
  requires remapping item types in old saves (CvDeal and CvDiploParameters lists) and carries the
  unverifiable risk that the EXE hard-codes a heading value.
- B. Append after TRADE_RELIGION (before NUM_TRADEABLE_HEADINGS). No renumbering, old saves keep
  valid item numbers, no EXE constant risk; but `buildTradeTable` (DLL/CvPlayer.cpp:23816) and the EXE
  treat these values as headings, so each needs a `getHeadingTradeString` text and appears as a
  collapsible heading with one child item. Lower risk; recommended unless option A is tested
  in-game first.
- With option (b) of 5.1, TRADE_OPEN_BORDERS keeps value 5 for one of the agreements and only two
  items are added.

Also update: `CvDeal::isAnnual/isDual/hasData` (DLL/CvDeal.cpp:1299-1343), `startTrade/endTrade`
cases (:1015, :1142), `CvTeam::addTeam` deal-kill lists (DLL/CvTeam.cpp:562, 577),
`canTradeItem`/`getTradeDenial`/`buildTradeTable`/`getItemTradeString` (CvPlayer.cpp:5658, 5785,
23779, 24031), `AI_dealVal` (CvPlayerAI.cpp:8874), `parseTradeItem` (CvDLLWidgetData.cpp:4725),
`getTradeString` (CvGameTextMgr.cpp:15455), `CyEnumsInterface.cpp:1424-1447`, BUG mirrors
(Py/BUG/DealUtil.py:99-130, Py/BUG/TradeUtil.py:514-524, 674-682, Py/BUG/Scoreboard.py:74-79).

### 5.4 Save compatibility

- CvTeam: write `uiFlag=1`; on read, `if (uiFlag < 1)` read the old `bool[MAX_TEAMS]` and convert
  true -> all three bits; else read the int mask (same stream position, DLL/CvTeam.cpp:7375/7484).
- CvTeamAI counters: if split into three, version the read (DLL/CvTeamAI.cpp:4011).
- CvDeal: write `uiFlag=1`. For old saves: (i) option A needs remapping of item types >= 9; (ii) old
  OB sub-deals (item TRADE_OPEN_BORDERS, iData=1) must be converted so that every granted right is
  backed by a deal item (append the new items to both lists), otherwise rights set by the
  conversion in CvTeam can never be cancelled.
- CvDiploParameters (pending diplomacy) can be dropped/remapped the same way.
- Avoid new ContactTypes/MemoryTypes in the first version: they change `NUM_CONTACT_TYPES` /
  `NUM_MEMORY_TYPES` array sizes in CvPlayerAI saves (DLL/CvPlayerAI.cpp:18847-18851, 19052-19056),
  must match XML/GlobalTypes.xml and CIV4MemoryInfos.xml, and every leaderhead (59 + module copies)
  would need ContactRand/ContactDelay/MemoryDecay entries. Reuse CONTACT_OPEN_BORDERS and
  MEMORY_CANCELLED_OPEN_BORDERS for all three; if added later, bump CvPlayerAI uiFlag to 7.

### 5.5 Deal UI

- Dual items are mirrored automatically by the EXE (isDual). One-way items would show only on the
  offering side.
- Text keys: three item names, three "_STRING" variants, heading texts if option B, attitude line,
  tech-help line, election text, scoreboard legend, BUG "closed borders" reason.
- Icons: no new FontSymbols without font art; use text markers or reuse OPEN_BORDERS_CHAR /
  TRADE_CHAR (DLL/CvEnums.h:991-1000).

### 5.6 AI valuation (replace the symmetric city-count value)

- Trade rights: value = expected foreign trade route gain (use
  `countPotentialForeignTradeCitiesConnected`, trade route yield); both sides gain, so mostly
  balanced; deny only for worst enemy / embargo memory.
- Civilian access: value for the receiver from `AI_missionaryValue`/`AI_executiveValue` external
  parts and settler reach; cost for the host when the receiver has more religions/corporations to
  push (state religion conflict, `isNoNonStateReligionSpread`).
- Military access: host cost high; deny when the receiver is a land target with power advantage,
  when we have a war plan against them, or attitude below a stricter threshold (reuse
  `DefensivePactRefuseAttitudeThreshold` or OB threshold + 1 level). Value to the receiver when it
  shares a war with the host or has war plans against third parties reachable through the host.
- Proposals in `AI_doDiplo`: try T first, then C, M only with shared war/vassal/friendly.
- Cancellation: per-item denial keeps working; consider adding war-plan checks so the AI cancels
  military access before attacking (otherwise its own units get bounced, 6.1).
- Votes: decide what the OB vote signs and evaluate each right's denial in `AI_diploVote`.

### 5.7 Minimal call-site switch list (DLL)

| Site | New predicate |
|---|---|
| CvTeam::isFreeTrade CvTeam.cpp:4642 | T |
| CvUnit::canEnterTerritory CvUnit.cpp:2496 | C or M by unit (host team grants to unit team) |
| CvPlot::isFriendlyCity CvPlot.cpp:3591 | same unit-based test |
| CvTeam::isFriendlyTerritory CvTeam.cpp:7046 | M |
| CvUnit::doTurn spy CvUnit.cpp:749 | C |
| CvPlayer::canSpyBribeUnit CvPlayer.cpp:23494 | M (or by bribed unit) |
| teamStepValid CvGameCoreUtils.cpp:2396 | M (inquisitor caller: C) |
| CvPlot::countFriendlyCulture CvPlot.cpp:10255 | M |
| CvUnitAI::AI_assaultSeaReinforce CvUnitAI.cpp:17908 | M |
| CvPlayerAI::AI_missionaryValue :12187, AI_executiveValue :12358, AI_getStrategyHash :21311 | C |
| CvPlayerAI::AI_stopTradingTradeVal :10383, AI_diploVote free trade :8296 | T |
| CvPlayer::calculateResearchModifier CvPlayer.cpp:8367 | T (or any) |
| CvPlayer::acquireCity :2893, CvDLLButtonPopup.cpp:1422 | any |
| CvGame::isValidVoteSelection :4290, CvPlayer::canDefyResolution :23249, canDoResolution :23121, AI_diploVote :8345, processVote :7798 | per vote decision |
| CvGameTextMgr parseLeaderLineHelp :16536, buildTradeString :19323 | display per right |
| CvTeam::addTeam propagation CvTeam.cpp:658-666 | copy the mask |
| CvTeamAI::AI_doCounter :4426 | per counter decision |

Python: CvMainInterface.py:5382, CvMainInterface-PLE.py:4819, CvForeignAdvisor.py:694/740 (+ legend
:511), RevUtils.py:263 (M), TechDiffusion.py:186 (T), BUG TradeUtil/DealUtil/Scoreboard/MoreCiv4lerts.

### 5.8 Size and risk estimate

- DLL: ~25 direct readers, ~20 switch/case sites for the new items, new storage/serialization,
  three valuation/denial functions, proposal logic, unit classifier: roughly 700-1000 lines touched
  in ~20 files.
- Python: ~150-250 lines (UI, BUG utilities, Revolution).
- XML: 10-20 text keys; optional tech flags/leaderhead fields (avoid in v1: 59 leaders + module
  schema copies).
- Risk: medium-high. Main risks: (1) EXE trade-screen behaviour with new items (only testable
  in-game); (2) save conversion of existing OB deals; (3) unit classification edge cases
  (explorers, transports with military cargo, great generals); (4) AI balance (military access
  denial, units bounced at war); (5) direction semantics if any agreement becomes one-way.
  Keeping all three dual and appending items after TRADE_RELIGION is the lowest-risk path.

---------------------------------------------------------------------------------------

## 6. Defects and inconsistencies found

6.1 [verified, behaviour inherited from BtS] Declaring war teleports OB guests before war starts.
`CvTeam::declareWar` kills all deals first (DLL/CvTeam.cpp:1440-1447); `endTrade` ->
`setOpenBorders(false)` -> `verifyUnitValidPlot` (DLL/CvTeam.cpp:4670) runs while `isAtWar` is still
false (set at :1459-1460), so `canEnterTerritory` fails and both sides' units inside the other's land
are moved by `jumpToNearestValidPlot` (DLL/CvPlot.cpp:835). Failure: an AI attack stack that walked in
under OB and then calls `groupDeclareWar` (DLL/CvSelectionGroup.cpp:4312) is scattered (groups
split by setXY) and the move aborts; garrisons in an ally's cities are expelled. Probably intended,
but the AI does not plan for it (keeps OB with its targets, section 3).

6.2 [verified code path, not runtime-tested] Forming a permanent alliance also expels units.
`CvTeam::addTeam` kills the OB deals between the merging teams (DLL/CvTeam.cpp:556-591) before the
players are merged, so the same `verifyUnitValidPlot` pass moves each partner's units out of the
other's territory (e.g. units defending the partner's cities), and both sides get
MEMORY_CANCELLED_OPEN_BORDERS against their future teammates.

6.3 [verified] The AI never cancels OB with a human for attitude reasons, but does with AIs.
For humans the cancel loop uses `AI_considerOffer(.., iChange=-1)` (DLL/CvPlayerAI.cpp:17001, 17022),
which skips the denial check (`if (iChange > -1)`, :8939) and compares values that are identical for
OB-for-OB (`AI_openBordersTradeVal` symmetric, DLL/CvTeamAI.cpp:3402-3405; `iChange < 0` branch :9056).
For AI partners it cancels as soon as `AI_openBordersTrade` denies (attitude, worst enemy;
DLL/CvPlayerAI.cpp:17010, 17031). Same asymmetry applies to defensive pacts.

6.4 [verified, exploitability uncertain] Payment and agreement are separate deals. A deal
"OB <-> OB + N gpt" saves only the gpt in the outer deal; OB lives in the team sub-deal
(DLL/CvDeal.cpp:1015-1036 bSave only for iData!=0; :1192-1224). Cancelling the OB sub-deal does not
end the gpt deal and vice versa. The split will multiply this (three agreements, each in its own
sub-deal); consider linking payments or valuing them as one package.

6.5 [verified, low impact] MEMORY_CANCELLED_OPEN_BORDERS is always given to both teams.
`kill()` runs `endTrade` for both lists (DLL/CvDeal.cpp:106, 111); each OB end adds memory to the
receiving side (DLL/CvDeal.cpp:1148-1166). The party that did not cancel (or the victim of a war
declaration, or alliance partners in 6.2) gets the same `DENIAL_RECENT_CANCEL` (DLL/CvTeamAI.cpp:3432)
as the canceller. With multi-player teams the cascade in `endTeamTrade` adds one memory per player
pair, prolonging the refusal.

6.6 [verified, low impact] OB value is counted although it is annual. `AI_dealVal` adds
`AI_openBordersTradeVal` regardless of `bIgnoreAnnual` (DLL/CvPlayerAI.cpp:8874-8876; resources, gpt,
vassal are gated). At signing both the outer deal and the team sub-deal call `addTrades`, so the
value enters peacetime trade value twice (DLL/CvDeal.cpp:205, 218), then again every turn in
`CvDeal::doTurn` (:304, :318). Mostly cancels in `AI_getTradeAttitude` because OB is symmetric.

6.7 [verified] The OB vote can pass but leave pairs unsigned. `processVote` calls
`signOpenBorders` for every voting pair (DLL/CvGame.cpp:7786-7804); that silently does nothing unless
`canTradeItem` holds, i.e. one of the two teams has the OB trading tech and they are not at war
(DLL/CvTeam.cpp:2255-2257, DLL/CvPlayer.cpp:5658-5672). `canDoResolution` only checks pairs with the
proposer (DLL/CvPlayer.cpp:23115-23131). Example: A (has TECH_TRADE) proposes, B and C lack it: B-C stay
closed. Also: validity uses `isFullMember` (DLL/CvGame.cpp:4282, 4288) while signing uses
`isVotingMember` (:7791, :7796), and the validity loop's `break` only leaves the inner loop
(:4293, harmless).

6.8 [verified, latent] Inconsistent direction convention. Deals set `GET_TEAM(giver).setOpenBorders(
receiver)` (DLL/CvDeal.cpp:1019, 1143), i.e. the flag means "granted by this team". Readers that
match: `countFriendlyCulture` (DLL/CvPlot.cpp:10255), `AI_missionaryValue/AI_executiveValue`
(DLL/CvPlayerAI.cpp:12187, 12358), main interface (`their.isOpenBorders(us)`). Readers that assume
"held by this team": `canEnterTerritory` (DLL/CvUnit.cpp:2496), `isFriendlyCity` (DLL/CvPlot.cpp:3591),
`isFriendlyTerritory` (DLL/CvTeam.cpp:7046), spy intercept (DLL/CvUnit.cpp:749), bribe
(DLL/CvPlayer.cpp:23494), `teamStepValid` (DLL/CvGameCoreUtils.cpp:2396), strategy hash
(DLL/CvPlayerAI.cpp:21311), vassal reinforce (DLL/CvUnitAI.cpp:17908), RevUtils.py:263. Harmless while
symmetric; any one-way agreement inverts half of these.

6.9 [uncertain] Rights changes do not invalidate AI path reuse. The reuse key
(DLL/CvSelectionGroup.cpp:52-66) ignores OB/war state; if OB flips between two `generatePath(..,
bReuse=true)` calls for the same group with unchanged moves in one turn, the continued A* tree may be
stale. Window is narrow today; with three independently flipping rights add an epoch bump.

6.10 [uncertain] Ending vassalage does not re-verify unit positions. `CvTeam::setVassal`
(DLL/CvTeam.cpp:4809ff.) never calls `verifyUnitValidPlot`, so a master's units in a released vassal's
land without OB stay until the next global verify (any OB change or war anywhere). Not observed
in-game.

6.11 [verified, cosmetic] `CvPlayer::canDefyResolution` compares `(PlayerTypes)iTeam != getTeam()`
(DLL/CvPlayer.cpp:23245) and `processVote` loops teams with `MAX_CIV_PLAYERS` (DLL/CvGame.cpp:7788,
7793). Numerically correct (MAX_CIV_TEAMS == MAX_CIV_PLAYERS, DLL/CvDefines.h:55) but type-confused.

6.12 [verified, cosmetic] `setOpenBorders` scans the whole map with `verifyUnitValidPlot` even when
OB is granted (DLL/CvTeam.cpp:4670), and a war declaration with OB triggers it three times
(two deal directions + :1537). Performance only.

6.13 [verified, UI] Trade-route hover can give a misleading reason: "network not connected" is based
on capital connection (`canTradeNetworkWith`, DLL/CvGameTextMgr.cpp:19318-19321) while routes need a
per-city plot-group match (DLL/CvCity.cpp:12583).
