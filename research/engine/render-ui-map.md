# RoM render / UI cost map (DLL -> engine, dirty bits, Python HUD, XML art)

Sources read (read-only):
- DLL: /home/user/src/rom-upstream/Assets/CvGameCoreDLL (paths below are relative to it unless prefixed)
- Python: /home/user/src/rom-upstream/Assets/Python (prefix `Py/`)
- XML: /home/user/src/rom-upstream/Assets/XML and Assets/Modules (MLF-resolved: 281 module XML files load)
- SDK interface headers: /home/user/src/sdk/beyond-the-sword-sdk-develop/CvGameCoreDLL/CvDLL*IFaceBase.h
  (the DLL's copies are byte-identical to the SDK ones)
- Harness (only to interpret the measured counts): /home/user/RoM/toolchain/harness/{engine.cpp,gen_stubs.py,main.cpp}

Tags used throughout:
- [V] verified in DLL/Python/XML source.
- [I] inference about what the closed executable does (not verifiable here).
- [M] measured by the coordinator's harness (5 AI turns, turn-400 Marathon Mediterranean snapshot,
  342 cities, ~1,800 units, all AI, active player = player 0).

Key constants [V]: MAX_CIV_PLAYERS = 50, MAX_PLAYERS = MAX_TEAMS = 51 (CvDefines.h:47-57);
NUM_CITY_PLOTS = 21 (CvDefines.h:76); PLOT_VISIBILITY_RANGE = 1; MAX_YIELD_STACK = 5;
culture radius up to 6 (7 culture levels, CvCity::doPlotCulture loop over (2r+1)^2);
loaded info counts: 423 units, 312 unit classes, 428 buildings, 413 building classes, 244 promotions,
83 leaderheads, 54 improvements.

-----------------------------------------------------------------------------------------------------

## 0. How to read the harness numbers [V from harness source]

- The harness never calls `CvGlobals::setGraphicsInitialized`, so `GC.IsGraphicsInitialized()` is false.
  Every DLL path behind that gate is skipped in the harness (18 sites in CvPlot.cpp alone: updateSymbols,
  updateFeatureSymbol, updateRouteSymbol, updateRiverSymbol, updateFlagSymbol, updateFog, updateCenterUnit,
  updateMinimapColor, setLayoutDirty, plus CvUnit::setXY QueueMove/SetPosition at CvUnit.cpp:10848).
  => Harness counts for plot symbols, flags, fog, plot builders and unit QueueMove/SetPosition are a strict
  lower bound (mostly zero). Counts for ungated calls (Entity::NotifyEntity, updateEnemyGlow, ExecuteMove,
  isCitySelected, getSelectionPlot, setDirty) are representative.
- `g_engineCallCounts` (engine.cpp:16) is never reset; main.cpp:205-213 prints total/turns. Load-time calls
  (plot/unit/city construction and XML load) are therefore included in the "per turn" figures.
- Stubs return NULL/false/0: getSelectionPlot() == NULL, isCitySelected() == false, IsSelected() == false,
  python callFunction returns lResult = 0 (so calculateScore returns 0 for everyone).

### 0.1 Measured engine calls [M] and their sources [V]

| Call (per turn) | Source in DLL | Notes |
|---|---|---|
| Route::destroy 1,126; River::destroy 1,126; Feature::destroy 1,126; FlagEntity::destroy 2,252 | CvPlot::uninit, CvPlot.cpp:125 (feature), :130 (route), :131 (river), :132-133 (two flags: m_pFlagSymbol, m_pFlagSymbolOffset) | The exact 1:1:1:2 ratio matches only CvPlot::uninit. uninit runs from the CvPlot ctor (reset(0,0,true) CvPlot.cpp:84 -> :185), from CvPlot::read (reset() :8997 -> uninit) and from ~CvPlot (:90). With graphics off, the other destroy sites (updateFeatureSymbol :7937/:7943, updateRouteSymbol :7997/:8003, updateRiverSymbol :8055/:8062, updateFlagSymbol :8170/:8174) are unreachable. So 5,630 total = numPlots x (uninit calls per plot during load/teardown). This is load-time, not per-turn rendering. |
| Entity::IsSelected 3,103 | CvUnit::setXY :10911, setMoves :11107, setDamage :11057, setExperience :11146, setLevel :11201, setCombatUnit :12175, setHasPromotion :12713, CvSelectionGroup::IsSelected loop :4081, startMission/continueMission :1392/:2025/:2552/:2602 | Cheap exe query; all ungated. |
| Entity::NotifyEntity 2,502 | CvUnit::setDamage :11052 (MISSION_DAMAGE, every heal/damage), CvSelectionGroup::setActivityType :5329 (MISSION_IDLE for every unit of a group whose activity changes), CvUnit::setFacingDirection :11830, combat :1561-1562/:15945-15946, build :7576, many one-off missions | Not gated by visibility to the active player. |
| Entity::updateEnemyGlow 2,188 | CvPlayer::doWarnings :18210 (loops ALL own units of EVERY player each turn; called from CvPlayer::setTurnActive :12341 for AI too) + CvUnit::setXY :10925 (every step of every unit) | ~1,800 units + ~400 steps matches. Not gated. |
| Entity::ExecuteMove 514 | CvSelectionGroup::groupMove :4618/:4631 (every unit of a moving group at end of move), combat :1535/:3093/:15918 | Not gated by visibility. QueueMove/SetPosition (CvUnit.cpp:10856/:10860) are 0 in harness only because of the graphics gate; in game every setXY calls one of them. |
| Utility::getAudioTagIndex 510 | XML load (CvInfos.cpp:13101, :23921-23925, :25281, CvXMLLoadUtilitySet.cpp:3394) | Load-time only. |
| Entity::createUnitEntity 244, createCityEntity 23, destroyEntity 14 | CvUnit ctor CvUnit.cpp:61, CvCity ctor CvCity.cpp:102 | Mostly object construction at load plus units built/killed. |
| Interface::addMessage 116 | many | Messages to AI players are formatted in the DLL (gDLL->getText) even though only the active player sees them [I]. |
| Entity::updatePromotionLayers 61, showPromotionGlow 41 | CvUnit::setHasPromotion :12720 (once per promotion changed), setPromotionReady :11914 | Per event; fine. |
| Interface::isCitySelected 10,084 | see 0.2 | |
| Interface::getSelectionPlot 6,771 | see 0.2 | |

### 0.2 Why ~17,000 isCitySelected/getSelectionPlot calls per AI turn [V]

isCitySelected (CvCity::isCitySelected, CvCity.cpp:1345 -> interface). Call sites NOT gated by owner:
- CvCity::updateCommerce(eIndex) :9787 - on every commerce change of any city; reached from setBaseYieldRate
  (:9262, which fires on each changeBaseYieldRate from setWorkingPlot), changeSpecialistPopulation :6077,
  updateBuildingCommerce :10072, updateReligionCommerce :10233, CvPlayer::updateCommerce loops (CvPlayer.cpp:4294/4306)...
  NUM_COMMERCE_TYPES = 4, so one yield change can produce up to 4 calls.
- CvCity::setWorkingPlot :11898 (every worker reassignment by AI_assignWorkingPlots), setSpecialistCount :11455,
  setFreeSpecialistCount :11675, setForceSpecialistCount :11618, pushOrder :12830, popOrder :13199/:13265,
  setRallyPlot :5915, setName :10919, kill :955.
- CvPlot::updateShowCitySymbols CvPlot.cpp:4805: loops 21 plots and calls isCitySelected for each city found;
  called from CvPlot::updateWorkingCity :6024 (every working-city change, i.e. culture/owner churn) and
  CvCity::updateSelectedCity :1392. Not graphics-gated, so it runs in the harness too.
- Gated (short-circuit on active player first): setPopulation :6014, hurry :3915, setCitizensAutomated :8646,
  setProductionAutomated :8666, setBuilding/Project/UnitProduction :11155/:11251/:11306,
  CvCityAI::AI_assignWorkingPlots :392, AI_setEmphasize :6644; setBaseYieldRate :9268 is gated by active team.
- 10,084 / 342 cities = ~29 per city per turn: consistent with AI worker reassignment + commerce churn.

getSelectionPlot. Sites (all ungated, each compares a plot to the selection plot to set PlotListButtons):
- CvUnit::setMoves :11114 (every unit at doTurn and every move step), setDamage :11062 (healing),
  setXY :10684 and :10864 (two per step), joinGroup :10423, setCombatUnit :12180;
  CvSelectionGroup::setActivityType :5342; CvGame::updateSelectionList (CvGameInterface.cpp:541, exe-driven).
- 6,771 / 1,800 units = ~3.8 per unit per turn.

Cost [I]: each is a virtual call into the exe that walks a short list (selected cities / selection list);
17k calls x ~20-100 ns is < 2 ms per turn. Not worth optimising by itself. What matters is what they
trigger (dirty bits, below), and one real bug:

BUG [V]: `pPlot == getSelectionPlot()` is true when both are NULL. pPlot is NULL in
- CvUnit::joinGroup :10423 when called from CvUnit::kill (setXY(INVALID) at CvUnit.cpp:673, then joinGroup(NULL) at :675),
- CvUnit::joinGroup from CvUnit::setXY :10530-10532 during CvUnit::init (unit not yet on a plot),
- CvSelectionGroup::setActivityType :5342 for an empty group (plot() returns NULL, CvSelectionGroup.cpp:4177-4190),
- CvUnit::setMoves/setDamage on an off-map unit.
In the game the selection plot is NULL whenever the human has nothing selected (typical while AI turns run),
so every unit birth and death anywhere in the world sets PlotListButtons_DIRTY_BIT and forces a full Python
plot-list redraw (section 2/3). This explains the harness's 40 PlotListButtons sets per turn.
Fix: add `pPlot != NULL &&` to those five comparisons. Zero behaviour change for real selections.

-----------------------------------------------------------------------------------------------------

## 1. DLL -> renderer: interfaces, call sites, triggers

### 1.1 Interface inventory [V]

| Interface | Call sites | Methods used |
|---|---|---|
| Engine (CvDLLEngineIFaceBase) | 100 | SetDirty 22 (GlobeTexture, GlobePartialTexture, MinimapTexture, CultureBorders), addColoredPlot 13, fillAreaBorderPlot 6, clearAreaBorderPlots 4, RebuildPlot 2, RebuildAllPlots 2, RebuildTileArt 1, RebuildRiverPlotTile 1, MarkPlotTextureAsDirty 1, MarkBridgesDirty 1, ForceTreeOffsets 1, Lighten/Darken/BlackenVisibility 5, TriggerEffect 3, Add/RemoveGreatWall 2, updateFoundingBorder 1 |
| Entity | 67 | (via CvDLLEntity wrapper) createUnit/CityEntity, setup, setVisible, MoveTo, QueueMove, ExecuteMove, SetPosition, NotifyEntity, AddMission (~35 sites, combat/air/bombard), RemoveUnitFromBattle, updateEnemyGlow, updatePromotionLayers, showPromotionGlow, updateGraphicEra, updatePosition, setupFloodPlains |
| PlotBuilder | 3 | create/init (CvPlot::updatePlotBuilder :9504-9516), destroy (uninit) |
| Symbol (yield symbols) | 10 | createSymbol/init/setTypeYield/setAlpha/setScale/updatePosition/Hide/destroy (CvPlot.cpp:629-746, 8524-8560) |
| Feature | 13 | createFeature/init/getFeature/Hide/IsHidden/destroy + dummy-model helpers |
| Route | 8 | createRoute/init/getRoute/destroy/updateGraphicEra |
| River | 5 | createRiver/init/destroy |
| FlagEntity | 20 | create/setPlot/updateUnitInfo/getPlayer/destroy/updateGraphicEra |
| Interface | 1,150 | setDirty 237 sites, addMessage, selection queries, setMinimapColor, lookAt, playGeneralSound |

Exe-polled DllExports that pull graphics state from the DLL [V exported, I polled]:
CvMap::updateFlagSymbols (CvMap.cpp:342, loops all plots, rebuilds flags where isFlagDirty), CvMap::updateCenterUnit,
CvPlot::isLayoutDirty / getVisibleImprovementState / getVisibleBonusState / shouldUsePlotBuilder / getCenterUnit,
CvCity::isLayoutDirty + getVisibleBuildings (CvCity.h:1009 comment: "called whenever CvCity::setLayoutDirty() is called"),
CvCity::getVisibleEffects, CvGame::updateColoredPlots / updateBlockadedPlots / getPlotUnit / getPlotUnits /
getGlobeLayers, CvPlayer::getGlobeLayerColors, CvGameTextMgr::setPlotListHelp / setPlotHelp (mouse-over help).

### 1.2 Per-event map

Unit move, one step (CvUnit::setXY CvUnit.cpp:10488-10930) [V]:
- old/new plot: changeAdjacentSight -/+ ((2*visRange+1)^2 plots) -> CvPlot::changeVisibilityCount :7032.
  For plots whose visibility flips for the ACTIVE team only: updateFog (1 engine call), updateMinimapColor,
  updateCenterUnit; first reveal -> setRevealed :7543 -> updateSymbols + updateFog + updateVisibility
  (layout dirty, symbol/feature/route visibility) + MinimapSection/GlobeLayer dirty.
- removeUnit/addUnit with bUpdate (CvPlot.cpp:8432-8500) -> updateCenterUnit on both plots (gated by
  isActiveVisible; inside: getSelectedUnit O(n) with one exe IsSelected per unit, then up to 5 getBestDefender
  passes O(n) each, CvPlot.cpp:763-807) + setFlagDirty.
- QueueMove (if visible to a watching human) else SetPosition: one entity call, always (CvUnit.cpp:10848-10861).
- updateEnemyGlow: always (CvUnit.cpp:10925).
- Selection-plot compares (2), PlotListButtons dirty if equal; ColoredPlots dirty if the unit is selected.
- CvSelectionGroup::groupMove: ExecuteMove for every unit at end of move (CvSelectionGroup.cpp:4618/4631).
Complexity: O(sight^2) visibility updates + O(n_plot) center-unit work per unit per step on plots the active team
sees. Moving a stack of n units through visible plots costs O(n^2) defender evaluations per step
(n=100: ~2 x 100 x 100 x up to 6 passes = 10^4-10^5 isBetterDefenderThan calls). Hidden plots: O(1).

Combat [V]: AddMission (battle definition), RemoveUnitFromBattle, ExecuteMove(0.5,true), NotifyEntity(DAMAGE) x2,
setDamage -> NotifyEntity + PlotListButtons/InfoPane dirty, lookAt only if isCombatVisible (CvUnit.cpp:14215:
only when a human attacker/defender lacks QUICK_ATTACK/QUICK_DEFENSE). Battle effects (Afforess):
CvGame::drawBattleEffects CvGame.cpp:10039 loops ALL plots and calls TriggerEffect for each isBattle plot; Python calls
it every 23rd updateScreen (Py/Screens/CvMainInterface.py:1256-1261), i.e. about every 5.75 s [I: 250 ms period].

Yield symbols [V]: CvPlot::updateSymbols :695 deletes all symbols of the plot, recomputes 3 yields via
calculateYield(display), creates maxYield/5+1 symbol layers, then setAlpha/setScale/updatePosition/Hide each.
NOT gated by revealed/visible/owner: runs for every plot in the world. Triggers:
- CvPlot::updateYield :6471 when any yield changes (-> updateSymbols :6515). updateYield callers include
  CvCity::updateYield (21 plots) <- CvPlayer::updateYield (all cities) <- CvTeam::updateYield (all members),
  CvPlayer::changeGoldenAgeTurns :9898, updateExtraYieldThreshold :13089, changeImprovementYieldChange :14384,
  CvTeam::changeImprovementYieldChange :6595, CvTeam::processTech :6945 (every plot with a bonus revealed by the tech,
  map-wide scan), setForceRevealedBonus :7249 (map scan), CvArea::changeNumTiles :378 (CvMap::updateYield = all plots),
  CvCity::changeSeaPlotYield/changeRiverPlotYield :8974/:8997 (21 plots), setPopulation :5993.
- CvPlot::setOwner :4845 -> updateYield (may updateSymbols) AND an unconditional updateSymbols at :5100 (double rebuild).
- setRevealed/setRevealedImprovementType/setRevealedRouteType for the active team (:7587, :7741, :7790).
- CvCity::setRevealed (CvCity.cpp:10816): 21 plots for the active team.
- Map-wide: CvGame::toggleDebugMode :4521, setActivePlayer :4731 (hotseat), CvMap::setupGraphical (load).
Complexity: per yield-change event, plots touched x (3 calculateYield + 2-4 symbol create/destroy + ~6 setters).
A tech/civic/golden-age that changes yields rebuilds 21 x cities plots (late game: 21 x 40 cities = 840 plots per
player event), including plots no human can see. updateSymbolDisplay on worked-plot change is gated by
active team (CvCity.cpp:11892).

Culture spread / border change [V]: CvCity::doPlotCulture loops (2r+1)^2 plots (r <= 6: 169) every turn per city
calling changeCulture; only owner changes do graphics work. CvPlot::setOwner :4845 per flipped plot:
updateRevealedOwner for all 51 teams (setRevealedOwner :7273 -> for active team: updateMinimapColor,
GlobeLayer dirty, engine CultureBorders_DIRTY_BIT), updateWorkingCity (-> updateYield, updateFog,
updateShowCitySymbols over 21 plots), changeAdjacentSight -/+ (9 plots x 2), updateIrrigated, updateYield,
updatePlotGroup, danger-cache invalidation over (2*DANGER_RANGE+1)^2, updateSymbols.
Per flipped plot: O(21 + 51 + 9) plot/team updates + plot-group work; engine border rebuild is requested
via CultureBorders_DIRTY_BIT [I: the engine rebuilds border geometry for the whole map or large sections
per dirty frame]. CvCity::acquireCity/revolt is the heavy version.

Improvement built/pillaged/upgraded [V] CvPlot::setImprovementType :5661: setRevealedImprovementType for every
team that sees it (active team -> updateSymbols + setLayoutDirty), updateIrrigated, updateYield (symbols),
21-plot feature-happiness update, CitizenButtons_DIRTY_BIT UNCONDITIONALLY (:5771) for every improvement change
anywhere (hamlet->village->town growth included). setLayoutDirty for the plot itself only in debug mode;
the visible change arrives through setRevealedImprovementType for the active team.

Route built [V] setRouteType :5782: setRevealedRouteType for each team that sees it (active team ->
updateSymbols + updateRouteSymbol(true, true) = rebuild of route entity on the plot and 8 neighbours),
updateYield, updatePlotGroup.

Feature change (chop, forest growth, global warming) [V] setFeatureType :5440: updateYield, updateFeatureSymbol
(always calls RebuildTileArt CvPlot.cpp:7931, then destroy/create feature entity) - NOT visibility gated;
updateRiverSymbolArt for flood plains; 21-plot city health/happiness.

Terrain/plot type change [V]: setPlotType :5363 -> RebuildPlot(heights+textures) + feature/route/river symbol
updates on 9 plots; setTerrainType :5418 -> RebuildPlot(textures). Callers: CvGame::doGlobalWarming
CvGame.cpp:6186-6230 (late-game, several per turn), terraform events CvGame.cpp:1263-2009. Not visibility gated.

City growth [V] CvCity::setPopulation: setLayoutDirty(true) + setInfoDirty (CvCity.cpp:6009-6010) -> exe calls
getVisibleBuildings [I]: O(428 buildings) + sort, returns up to 10 + 2*floor(pop^1.05) building models
(GAME_CITY_SIZE_EXP_MODIFIER 1.05). processBuilding :4548 also sets layout dirty (every building gained/lost).

Era change [V] CvPlayer::setCurrentEra :12640: loops ALL plots calling updateGraphicEra (route + flag entity
per plot), setLayoutDirty on plots with revealed improvements owned by that player, setLayoutDirty all its
cities, updateGraphicEra on every unit; fires for every player (AI too). Rare (players x eras per game).

Owner change of a city [V]: CvPlot::setOwner (city branch) -> acquireCity -> entity destroy/create, all of the
above for the 21-plot radius plus culture recompute.

Active-player switch / debug toggle [V] (CvGame.cpp:4515-4545, 4720-4751): updateFog + updateVisibility +
updateSymbols + updateMinimapColor for EVERY plot, updateUnitEnemyGlow for every unit, ~10 dirty bits.

Colored plots [V] CvGame::updateColoredPlots (CvGameInterface.cpp:18-500), called by the exe when
ColoredPlots_DIRTY_BIT is set [I]. Always calls Python `updateColoredPlots` first (:50). Then, depending
on selection: city screen (21 plots), settler/founder with GRAPHICOPTION_CITY_RADIUS: loop over ALL plots
(:207-226); DCM bombard ranges; air range; worker recommendations (2 x AI_bestCityBuild);
9x9 canFound + AI_isPlotCitySite (:396-440); blockading unit selected: every active-team unit x
(2*SHIP_BLOCKADE_RANGE+1)^2 x calculatePathDistance (:449-490). ColoredPlots dirty is set by every step of a
selected unit (CvUnit.cpp:10919), setFacingDirection :11822, setWorkingPlot :11902, updateWorkingCity
CvPlot.cpp:6032 (active player, city-radius option on).

### 1.3 Visibility gating summary [V]

Gated to the active team/player: updateFog, updateCenterUnit (isActiveVisible), setRevealed* side effects,
updateMinimapColor on unit moves (isActiveVisible), updateSymbolDisplay on worked plots, CultureBorders/GlobeLayer
dirty from setRevealedOwner, most GameData/Score/Research/Percent dirty bits, combat camera (isCombatVisible),
AI mission timers (only if isVisibleToWatchingHuman, CvSelectionGroup.cpp:2525-2529).

Not gated (work done for invisible/AI-only events): updateSymbols/updateYield (all plots), updateFeatureSymbol +
RebuildTileArt, RebuildPlot (global warming), setCurrentEra map loop, CvPlayer::doWarnings updateEnemyGlow for
all units of all players, setXY QueueMove/SetPosition + updateEnemyGlow, groupMove ExecuteMove,
NotifyEntity(IDLE/DAMAGE), CitizenButtons from setImprovementType, Espionage_Advisor from AI espionage weights,
updateCommerce/setWorkingPlot isCitySelected queries, PlotListButtons NULL==NULL case.

### 1.4 Expensive rebuild hot spots (ranked by likely frequency x cost)

1. updateSymbols per yield change, ungated, 21 x cities plots per player-wide event; plus double rebuild in setOwner.
2. Plot hover help (CvGameTextMgr::setPlotListHelp :1374, DllExport, called from getPlotHelp :19492/:19517 and
   from CvPlayer::getUnitLayerColors :24449 for every globe-view unit indicator). When the plot shows more than
   iMaxNumUnits = 15 units it (re)zeroes arrays sized GC.getNumUnitInfos() * MAX_PLAYERS = 423 x 51 = 21,573
   entries, each with an int[244] promotion array (CvGameTextMgr.cpp:1778 limit, reset loop :1811-1830): ~5.3 M int writes per call and
   a one-time 21 MB heap allocation (m_apbPromotion, CvGameTextMgr.h:290) inside a 4 GB address space; then a
   final 21,573-entry scan (:1889). Triggered by hovering a big stack [I: on every new mouse-over plot] and by the
   globe-view unit layer for each indicator plot.
3. updateCenterUnit O(n) x up to 6 passes on every add/remove on visible plots: O(n^2) per visible stack move.
4. updateColoredPlots for blockading/settler selections (map-wide loops, path distance).
5. CvGame::updateScore (CvGame.cpp:2232): O(P^2) Python `calculateScore` callbacks (CvPlayer.cpp:4582) per
   score update: A(A+1)/2 calls for A alive players (A=40: 820) each time score is dirty, at most once per
   CvGame::update tick. Sets Score_DIRTY_BIT when ranks/scores change (CvGame.cpp:4981/5042/5064).
6. CvPlayer::doWarnings: updateEnemyGlow for every unit of every player each turn (CvPlayer.cpp:18210).
7. setCurrentEra whole-map loop; global-warming RebuildPlot.

### 1.5 Engine dirty bits [V]
EngineDirtyBits (CvEnums.h:336): GlobeTexture, GlobePartialTexture, MinimapTexture, CultureBorders.
CultureBorders set at CvPlot.cpp:7299 (setRevealedOwner, active team), :5072 (debug), CvPlayer.cpp:1693/3618
(civ/name change), CvGame.cpp:4533/4750. GlobePartialTexture once per game turn (CvGame.cpp:6053).

-----------------------------------------------------------------------------------------------------

## 2. Interface dirty bits (CvEnums.h:348-385)

Python consumer: Py/Screens/CvMainInterface.py `redraw()` :1405-1488 (called by the exe when dirty bits are set
[I]) checks PercentButtons, Flag, MiscButtons, InfoPane, PlotListButtons, SelectionButtons, ResearchButtons,
CitizenButtons, GameData, Help, CityScreen, Score (or checkFlashUpdate), GlobeInfo. Advisors check their own bit in
`update(fDelta)` only while open. Bits not read by Python are consumed by the exe [I].
CvMainInterface-PLE.py is not imported anywhere (dead file).

Measured sets per turn [M] in parentheses. "sites" = number of setDirty(true) call sites in the DLL [V].

| Bit | sites | Main setters (hot in bold) | Gate | Consumer and redraw cost |
|---|---|---|---|---|
| SelectionCamera | 2 | CvPlayer::setTurnActive :12351, CvUnit::kill :619 | partly | exe |
| Fog | 0 | - | | exe |
| GlobeLayer | 10 | setRevealed :7592, setRevealedOwner :7297, setBonusType :5650, setXY of selected settler :10915, setHasTech :6551 | active | exe -> getGlobeLayerColors (unit layer: O(alive players x (plots+units)) + setPlotListHelp per indicator, see 1.4-2) |
| GlobeInfo | 2 | changeCiv, setIsMinorCiv | | Python updateGlobeviewButtons :5922 (small) |
| Waypoints | 4 | doTurnUnits (active), mission queue changes (active+selected) | yes | exe |
| PercentButtons | 5 | setActivePlayer, changeCommerceFlexibleCount, makeHasMet | mostly | Python updatePercentButtons :1491, O(4) |
| MiscButtons | 6 | setGold :9822, anarchy, revolution/conversion timers, setHasTech | active | Python updateMiscButtons :1604 |
| PlotListButtons (40) | 10 | **CvUnit::setMoves :11116, setDamage :11064, setXY :10688/:10868, joinGroup :10425, setCombatUnit :12182, CvSelectionGroup::setActivityType :5344**, promote :7694, CvCity::push/popOrder :12835/:13270 | selection-plot compare (NULL==NULL bug, 0.2) | Python updatePlotListButtons :1937. Default draw method VAN (Config/Plot List Enhancements.xml Draw_Method default 1). Fixed cost per redraw: hide 7 widgets x 350 buttons (35 per row at 1920 px x MAX_PLOT_LIST_ROWS 10) = 2,450 calls (:2042-2054) + 2 x 244 promotion moveToFront (:2084-2093) + addUnitGraphicGFC 3D unit model re-add (:2010, :2033). Per displayed own unit: ~20 widget/DLL calls + MonkeyTools.checkAnyUpgrade (Py/Contrib/MonkeyTools.py:87-110) = 423 canUpgrade calls. 50-unit stack: ~22k Python->DLL calls; 100-unit: ~44k. |
| SelectionButtons (2.6) | 19 | setGold :9823 (active), setActivityType :5345, mission queue (active+selected), setHasTech :6549, doTurnUnits :4128 (active), popOrder/pushOrder (selected city), setPromotionReady/setHasPromotion (selected) | mostly | Python updateSelectionButtons :2386. City selected: 312 unit classes x canTrain x2 + 2 x 413 building classes x canConstruct x2 (Python cannotConstruct callback CvCity.cpp:2505-2517 for those passing C++ checks, USE_CANNOT_CONSTRUCT_CALLBACK=1) + projects/processes. Unit selected: getActionsToShow + canHandleAction per action. |
| CitizenButtons (24) | 4 | **CvPlot::setImprovementType :5771 (ungated, any improvement change in the world)**, setSpecialistCount :11457 (selected), AI_assignWorkingPlots :394 (active+selected) | no | Python updateCitizenButtons_hide :2775 + one of 3 variants (specialists x counts); small but pointless when no city screen is up. |
| ResearchButtons | 6 | push/popResearch, setHasTech, clearResearchQueue (active) | yes | Python updateResearchButtons :2728: 2 x 308 techs (only shown when no research) |
| Event | 0 | - | | exe |
| Center | 1 | setWinner | | exe |
| GameData (1) | 30 | setGold :9824, changeCommerceRate :13243, unit/gold-per-unit changes (active), CvUnit::init :237 (active), setGameTurn :3479, setResearchProgress :5604 (active) | active | Python updateGameDataStrings :3216: GP bar (loops own cities), GG bar, updateResourceStrings (:3423; runs ~140 hide calls even when the RoM resource bar option is off - default False) |
| Score (26) | 25 | **CvPlayer::setTurnActive :12436 (ungated, twice per player per turn)**, CvGame::setRankPlayer :4981 / setPlayerScore :5042 / setRankTeam :5064 (ungated), changeStateReligionCount :11307, setLastStateReligion :12731 (ungated), research push/pop (active), declareWar/makePeace/makeHasMet/openBorders/pact (active involved), AI_changeMemoryCount (active) | partly | Python updateScoreStrings :5148 (see 3.3): O(MAX_CIV_TEAMS x MAX_CIV_PLAYERS) = 2,500-iteration nested loops run 4 times (pre-count :5216, main :5244, checkScrollingScoreboard :6477 twice: via updateScrollingScoreboard :6473 and BUG/Scoreboard.py:387, which also constructs a fresh CvMainInterface + PLE object each draw and overwrites the global g_mainInterface) + per shown player ~60 DLL calls + isWHEOOH (O(P) canTradeItem/getTradeDenial(TRADE_WAR) -> CvTeamAI::AI_declareWarTrade, itself O(P)) + isWorstEnemy (O(P) team-name compares) + Scoreboard.draw 25 parts x P. Estimated 40-60k Python->DLL calls per redraw at P=40. |
| TurnTimer (1) | 1 | setGameTurn | | exe |
| Help | 3 | setForceSpecialistCount (selected), change Unit/BuildingClassMaking (active) | | Python updateHelpStrings :5867 |
| MinimapSection | 7 | setRevealed :7591 (active), setActivePlayer, setName... | active | exe |
| SelectionSound | 1 | changeCiv | | exe |
| Cursor | 1 | setGameState | | exe |
| CityInfo (9) | 16 | **CvPlayer::doTurn :4046 (ungated, once per player per turn -> 9 = player count in the snapshot)**, CvArea::changeCleanPowerCount :710 / changeYieldRateModifier :817 (ungated), state religion modifiers, declareWar/makePeace (active involved) | partly | exe (city billboards) [I] |
| UnitInfo (9) | 9 | **CvPlayer::doTurnUnits :4131 (ungated, once per player per turn)**, promote (selected), setBestLandUnit | partly | exe (unit flags/info bars) [I] |
| Popup | 2 | revolution, setResearchingTech | | exe |
| CityScreen | 12 | setBaseYieldRate :9270, updateCommerce :9790, setWorkingPlot :11901, setPopulation, setName, production setters, push/popOrder (all selected-city gated), setCommercePercent (active) | selected | Python updateCityScreen :3583 (1,206 lines): O(428 buildings) scan + per built building (~100-200 late) ~15 DLL calls + 2 table cells; religions/corporations/bonuses loops; sets Domestic_Advisor dirty. |
| InfoPane | 23 | setMoves/setDamage/setExperience/setLevel/setName/setHasPromotion of the selected unit, mission queue (active+selected), city yields/commerce/working plot (selected city) | selected | Python updateInfoPaneStrings :4789: 3 x 244 promotion-widget hides always (:4816-4823); selected stack of S units: S x 244 isHasPromotion (:4952-4960, BUG Stack Promotions default on) + 423 countEntities (:4985) + S-step movement scan. S=100: ~25k calls per redraw, and a moving selected stack sets it every step. |
| Flag | 7 | setCurrentEra :12670, setActivePlayer, changeCiv/setName/setCivName | | Python updateFlag :2377 (trivial); exe flags |
| HighlightPlot | 2 | changeLeader/changeCiv | | exe |
| ColoredPlots | 7 | setXY of selected unit :10919, setFacingDirection :11822, setWorkingPlot :11902, updateWorkingCity CvPlot.cpp:6032, setRallyPlot, regenerateMap, changeCiv | selected/active | exe -> CvGame::updateColoredPlots (1.2) + Python callback |
| BlockadedPlots | 2 | CvUnit::updatePlunder :5631, setActivePlayer | | exe -> CvGame::updateBlockadedPlots: all plots (CvGameInterface.cpp:503) |
| Financial_Screen | 1 | setCommercePercent (active) | | Py/Screens/BugFinanceAdvisor.py:457 (only when open) |
| Foreign_Screen (1.8) | 6 | addDeal :7976 (ungated), changeLeader/Civ, setName, setIsMinorCiv | no | Py/Screens/CvForeignAdvisor.py:825 drawContents (only when open) |
| Soundtrack | 4 | era/civ changes | | exe |
| Domestic_Advisor | 0 (DLL) | set by Python after CityScreen redraw | | advisors when open |
| Espionage_Advisor (57) | 3 | **CvPlayer::setEspionageSpendingWeightAgainstTeam :16700 (from CvPlayerAI::AI_doCommerce :16352/:16362/:16505/:16635 for every AI player and target team)**, CvTeam::setCounterespionageTurnsLeftAgainstTeam :7117 / setCounterespionageModAgainstTeam :7145 (from CvTeam::doTurn :1128/:1133 for every team) | no | Py/Screens/CvEspionageAdvisor.py:1206 update(): refreshActiveTab only while the advisor is open. 57/turn = ~6 per player: AI re-weights espionage targets every turn. Wasted unless the screen is open during AI turns; then it re-renders the tab up to once per frame. Gate on getID()==active player / eIndex or getID()==active team. |
| Advanced_Start | 6 | doAdvancedStartAction | | exe/WB |

-----------------------------------------------------------------------------------------------------

## 3. Per-frame and per-input Python

### 3.1 Entry points [V code, I frequency]
- `CvScreensInterface.forceScreenUpdate(MAIN_INTERFACE)` -> CvMainInterface.updateScreen :1241. Firaxis comment
  ":1240 Will update the screen (every 250 MS)" and NJAGC decrements its timer by 250 per call (:1372) [I: ~4 Hz].
  Per call: BugOptions.write() (iterates INI files, writes dirty ones; Py/BUG/BugOptions.py:160), every 23rd call
  gc.getGame().drawBattleEffects() (DLL loop over all plots), screen.initMinimap(...) every call (:1271),
  ~15 CyInterface queries for the end-turn text, updateEndTurnButton, NJAGC clock text, PLE.checkInfoPane.
  O(1) except drawBattleEffects (O(numPlots) C++ every ~5.75 s). Cheap.
- `forceScreenRedraw(MAIN_INTERFACE)` -> redraw :1405 [I: called by the exe on frames where interface dirty bits
  are set]. setFieldofView (no-op unless changed) + ~14 isDirty calls + checkFlashUpdate, then the handlers in
  section 2. All real cost is in the handlers.
- `update(argsList)` per frame for open screens (CvScreensInterface.py:934): main interface update() is empty
  (:6397); advisors poll their dirty bit.
- `handleInput` (:6262) only on widget events (hover on/off, click); dictionary dispatch; cheap.
  Hover on plot-list buttons -> PLE info pane (PLE.showUnitInfoPane :1846) builds text per hover.
- Python events per tick: genericEvent("gameUpdate") from CvGame::update CvGame.cpp:2157 (not gated by
  USE_ON_UPDATE_CALLBACK) -> BugEventManager -> BugUtil.doDeferredCalls (Config/BUG Core.xml:97): O(1) when queue empty.
  mouseEvent/kbdEvent do an engine pickPlot raycast each (CvDllPythonEvents.cpp:42-60).
- DLL mouse-over help (not Python): CvGameTextMgr::getPlotHelp -> setPlotListHelp (1.4-2): the worst per-mouse-move cost
  on big stacks (~5 M writes per hovered stack > 15 units).
- Per AI unit move Python events (not UI, listed for completeness): unitMove and plotRevealed are not gated
  (CvDllPythonEvents.cpp reportUnitMove/reportPlotRevealed); unitSetXY is gated off (USE_ON_UNIT_SET_XY_CALLBACK 0).

### 3.2 Late-game n estimates and per-redraw cost (estimates [I] assume ~1-3 us per Python->DLL call in Python 2.4)

| Redraw | Work | n = 50-100 unit stack, 20-40 players | Est. time |
|---|---|---|---|
| PlotListButtons (VAN) | 2,450 hides + 488 moveToFront + per own unit (20 + 423 canUpgrade) | 22k-44k calls | 30-130 ms |
| InfoPane, selected stack | 732 hides + S x 244 + 423 | 13k-25k calls | 15-75 ms |
| Score (AlignIcons default) | 4 x 2,500-iteration loops + P x (60 + WHEOOH O(P) + WorstEnemy O(P)) + draw | 40k-60k calls (P=40); ~10k (P=9) | 50-180 ms (P=40) |
| SelectionButtons (city) | 312 x 2 canTrain + 826 x 2 canConstruct (+ Python callback each passing) | ~2.5k calls + 100-300 Python callbacks | 10-40 ms |
| CityScreen | 428 scan + ~150 built x 17 | ~3k calls | 5-15 ms |

Frequency during AI turns: Score fires 2 x P times per turn from setTurnActive alone (80 at P=40) plus every
tick in which any score or rank changed; PlotListButtons fires for every unit created/killed while nothing is
selected (NULL==NULL) and for every change on the selected plot. A per-turn total of several seconds of
UI-thread Python for a 40-player game is plausible [I]; measure before trusting.

### 3.3 Other O(n) notes [V]
- updateScoreStrings hide loop: 51 x (2 + 25 parts) = 1,377 hides per redraw (:5158-5166).
- Scoreboard.draw: BugUtil.Timer("scores") already instruments it (Py/BUG/Scoreboard.py:367) - usable for measurement.
- getPlotUnit (CvGameInterface.cpp:617) is O(n) per index; Python uses cacheInterfacePlotUnits once per redraw (:2119), good.
- PLE/BUG draw methods (PLE.py, BugUnitPlot.py) are off by default; same per-unit helpers (_displayUnitPlotList_*).

-----------------------------------------------------------------------------------------------------

## 4. Graphics load from XML

### 4.1 Unit models [V] (base XML/Units/CIV4UnitInfos.xml + 16 loaded module UnitInfos; module merge keeps the
larger iGroupSize, CvInfos.cpp:6793-6818)
- 423 unit types. iGroupSize distribution: 1:232, 2:35, 3:133, 4:4, 5:8, 6:1, 7:8, 8:2.
  Mean 1.97 models per unit type (unweighted), median 1. Land units mean 2.28 (317 types); sea 1.06; air 1.00.
  Sum of iRequired equals iGroupSize except for 21 types. Mesh groups per unit: 1 for 404 types, up to 7.
- By combat class: melee 3.29, gun 3.31, archer 3.0, mounted 2.76, siege 2.06, worker 2.12, settler class 7.0,
  animals 6.67; tracked/air/ships ~1.
- Largest: UNIT_CENTURIO 8, UNIT_CYBORG 8, UNIT_SETTLER/COLONIST/PIONEER/ROMAN_COLONIST 7 (stock BTS settler = 4),
  WARDOG/GUARDDOG/AUTOMATONS/HYPASPIST2 7. Late-game common units: Infantry 3, Rifleman 3, Machine Gun 3,
  Artillery 2, Worker 2, Mechanized Infantry 1, Modern Armor 1.
- iMeleeWaveSize: 1:226, 2:40, 3:144, 7:4. iRangedWaveSize: 0:161, 1:185, 3:55, 5:3 (number of models
  animating in a combat wave).
- Stock BTS for comparison: 123 types, mean 1.98.
- [I] Civ4 draws one representative ("center") unit per plot when idle (DllExport CvPlot::getCenterUnit,
  flag shows the stack); all units of a moving/fighting group animate. So per-frame model count ~ sum over
  occupied visible plots of iGroupSize(center unit) + moving units x iGroupSize.

### 4.2 Art defines [V] (XML/Art + loaded modules)
| Kind | Defined | Distinct NIF | Referenced | Stock BTS defined |
|---|---|---|---|---|
| UnitArtInfo | 884 | 824 (399 KFM) | 834 (437 by UnitInfos, 413 by 8 UnitArtStyles), 50 unreferenced | 224 |
| BuildingArtInfo | 417 | 320 | 391 | 160 |
| LeaderheadArtInfo | 83 | 83 (+83 NoShaderNIF) | 83 | 53 |
| ImprovementArtInfo | 55 | 45 | - | 25 |
Unit art: all 884 have ShadowDef, 168 have TrailDefinition, 340 bActAsRanged; mean fScale 0.46.
Building art: 83 with bAnimated=1.
Unit art styles (8 RoM vs 5 stock) multiply distinct unit models: the same unit class loads a different
NIF per civ style, so a 40-civ game can keep several hundred unit NIFs resident [I].

### 4.3 City and plot art multipliers [V]
- City buildings drawn: CvCity::getVisibleBuildings: 10 + 2*floor(pop^1.05) models (GAME_CITY_SIZE_METHOD
  METHOD_EXPONENTIAL, GAME_CITY_SIZE_EXP_MODIFIER 1.05, max 70% unique, GlobalDefines.xml; same as stock).
  pop 20 -> 56, pop 30 -> 80, pop 40 -> 106, pop 50 -> 130 models per city. RoM cities grow larger than stock,
  so this is a primary draw-call multiplier: 40 visible size-40 cities ~ 4,000 building models [I].
  Lever: lower GAME_CITY_SIZE_EXP_MODIFIER (e.g. 0.9 -> pop 40: 10+2*27 = 64) - purely visual.
- Yield symbols: MAX_YIELD_STACK 5 -> layers = maxYield/5 + 1 per plot; symbol objects exist for every plot
  (created ungated), shown only with yield display / city screen.
- Improvement art: 55 defines; plot builders created per plot with improvement/bonus (CvPlot::updatePlotBuilder).
- Routes/rivers/features: one entity each per plot; features in tile-art mode go through RebuildTileArt.

### 4.4 Stock graphic options that reduce load (XML_BTSsubfolder/GameInfo/CIV4GraphicOptionInfos.xml; RoM has no
override) [V names, I effects]
- GRAPHICOPTION_SINGLE_UNIT_GRAPHICS (default 0): one model instead of iGroupSize (mean 1.97 -> 1; settlers 7 -> 1);
  needs restart (Py/EntryPoints/CvOptionsScreenCallbackInterface.py:105).
- GRAPHICOPTION_EFFECTS_DISABLED, FROZEN_ANIMATIONS, NO_COMBAT_ZOOM (DLL honours it, CvUnit.cpp:1447),
  NO_ENEMY_GLOW (skips glow rendering; the DLL still calls updateEnemyGlow), LOWRES_TEXTURES, HIRES_TERRAIN off,
  NO_MOVIES, GLOBE_VIEW_BUILDINGS_DISABLED (default 1), CITY_RADIUS off (avoids the all-plot loop in
  updateColoredPlots :207 and updateWorkingCity ColoredPlots dirty).
- Player options (not graphic options): QUICK_MOVES / QUICK_ATTACK / QUICK_DEFENSE and turning off
  SHOW_ENEMY_MOVES / SHOW_FRIENDLY_MOVES (CvSelectionGroup::showMoves :483 -> mission timers and camera lookAt
  for visible AI moves, :2525-2540) shorten AI-turn wall time.

-----------------------------------------------------------------------------------------------------

## 5. Ranked cost drivers we can reduce (DLL / Python / XML)

1. Scoreboard redraw (Python + DLL). Change: (a) in CvPlayer::setTurnActive (CvPlayer.cpp:12436) set Score dirty
   only if isGameMultiPlayer() or this is the active player; (b) Python: throttle updateScoreStrings during AI turns
   (leave the bit set and redraw at most every ~0.5-1 s while not the active player's turn); (c) replace the
   4 nested 50x50 team/player loops with one pass over alive, met players grouped by team; (d) Scoreboard.py:387 -
   pass the existing main interface instead of constructing CvMainInterface (also fixes g_mainInterface overwrite);
   (e) cache isWHEOOH / isWorstEnemy per game turn, or ship WHEOOH default False in Config/Advanced Scoreboard.xml.
   Impact: high for 20-40 players (est. 50-180 ms x 80+ redraws per AI turn). Risk: low (display only).
   Measure: BugUtil.Timer("scores") log; harness Score dirty count per turn (26 -> ~8 at 9 players);
   A/B AI-turn wall time with scores hidden.
2. Plot-list redraw (Python + DLL). Change: (a) DLL guard `pPlot != NULL &&` at CvUnit.cpp:10423, :11062, :11114,
   :12180 and CvSelectionGroup.cpp:5342 (kills the NULL==NULL redraw on every unit birth/death);
   (b) MonkeyTools.checkAnyUpgrade: replace the 423-iteration canUpgrade loop by one DLL call (pUnit.hasUpgrade(False)
   plus the canMove/territory test, or a new CyUnit::canUpgradeAny) and cache per unit per turn;
   (c) hide only the buttons shown last time instead of all 350 x 7; drop the 2 x 244 moveToFront loops or
   restrict them to promotions actually shown. Impact: high for big stacks (est. 30-130 ms per redraw, many
   redraws per turn). Risk: low. Measure: harness PlotListButtons count (40/turn -> near 0 with no selection);
   time updatePlotListButtons with BugUtil.Timer on a 100-unit stack.
3. Plot hover help arrays (DLL, CvGameTextMgr::setPlotListHelp :1778-1900). Change: aggregate only the
   (unitType, owner) keys present on the plot (small map/vector, promotion counts only for those keys) instead
   of 423 x 51 x 244 zeroing; frees ~21 MB permanently. Impact: high per hover over stacks > 15 units and for the
   globe-view unit layer; also memory headroom under 4 GB. Risk: low (text only; keep output identical).
   Measure: PROFILE_FUNC already present (FProfiler); time the call in the harness on a plot with 100 units;
   compare process private bytes.
4. InfoPane for selected stacks (Python). Change: build stack promotion counts with one DLL helper or only over
   promotions any selected unit can have; skip the 732 hides when nothing was shown; replace 423 countEntities
   with one pass over the selection list. Impact: medium-high while moving big selected stacks. Risk: low.
   Measure: BugUtil.Timer around updateInfoPaneStrings.
5. Ungated yield-symbol rebuilds (DLL). Change: in CvPlot::updateSymbols return early (and mark a
   m_bSymbolsDirty flag) when the plot is not revealed by the active team; rebuild on reveal (setRevealed
   already calls updateSymbols) and in setupGraphical; remove the duplicate updateSymbols at the end of setOwner
   (CvPlot.cpp:5100) when updateYield already rebuilt. Impact: medium (tech/civic/golden-age and border churn
   across the world). Risk: medium (active-player switch and debug mode must force a full refresh; hotseat).
   Measure: count Symbol::createSymbol/destroy in the harness after enabling graphics init in the stub;
   compare before/after.
6. CvGame::updateScore O(P^2) Python callbacks (DLL). Change: call calculateScore once per player, then
   select by the same rule (>= keeps the highest index on ties) - identical ranks. Impact: medium
   (820 -> 40 Python calls per score update at 40 players; also fewer Score dirties). Risk: low.
   Measure: harness callback count for calculateScore (HARNESS_PY_COUNTS=1).
7. Wasted dirty bits for AI (DLL). Change: gate Espionage_Advisor sets (CvPlayer.cpp:16700, CvTeam.cpp:7117/:7145)
   to the active player/team; gate CitizenButtons in setImprovementType (CvPlot.cpp:5771) to
   isCityScreenUp/selected working city or active owner; CityInfo/UnitInfo in doTurn/doTurnUnits
   (CvPlayer.cpp:4046/:4131) to the active player (verify billboards still refresh for foreign cities at turn end).
   Impact: low-medium (fewer redraws/exe refreshes). Risk: low (CityInfo: medium). Measure: harness dirty counts
   (Espionage_Advisor 57 -> ~1, CitizenButtons 24 -> ~0).
8. Per-unit entity calls for AI (DLL). Change: CvPlayer::doWarnings updateEnemyGlow loop only for the active
   player (or only units whose glow state can change: units in or next to active-team territory); skip
   NotifyEntity(MISSION_IDLE)/(DAMAGE) and ExecuteMove for units not visible to the active team
   (isVisible(activeTeam) on the unit's plot). Impact: medium on frame time during AI turns [I: depends on exe
   culling]. Risk: medium (entities that later become visible must have the right state/animation; test reveal
   and combat cases). Measure: harness updateEnemyGlow 2,188 -> ~400, NotifyEntity 2,502 -> visible share.
9. City building models (XML). Change: GAME_CITY_SIZE_EXP_MODIFIER 1.05 -> 0.9-0.95 (GlobalDefines.xml).
   Impact: medium-high draw calls in late game with many big visible cities. Risk: none for gameplay (visual).
   Measure: FPS / frame time on a late save zoomed over a core region; DX9 draw-call counter (e.g. PIX/
   apitrace on a test machine).
10. Unit models (XML). Change: cut settler-class iGroupSize 7 -> 3-4 (stock 4), animals 5-7 -> 3, any 7-8
    groups -> 4; optional "light" module that sets late-era land units to 1-2. Impact: medium (moving AI
    stacks and settlers on screen); also mention SINGLE_UNIT_GRAPHICS to users. Risk: none for gameplay.
    Measure: frame time during visible AI moves; VRAM/private bytes after a long session.
11. updateCenterUnit O(n^2) per visible stack move (DLL). Change: defer center-unit recomputation to
    CvMap::updateFlagSymbols (already iterates flag-dirty plots once per frame [I]) by marking a per-plot
    "center dirty" in add/removeUnit, or skip the update for intermediate units of a group move and do it once
    per plot after groupMove. Impact: medium for big visible stacks. Risk: medium (getCenterUnit is DllExport
    and read by the exe; must be valid when read). Measure: PROFILE("CvPlot::updateCenterUnit") counts/time.
12. ColoredPlots for blockading/settler selections (DLL). Change: cache blockade range plots per turn;
    replace the all-plot CITY_RADIUS loop by iterating the player's cities x 21. Impact: low-medium (only when
    such a unit is selected, per step). Risk: low. Measure: PROFILE_FUNC in updateColoredPlots.
13. Minor: updateGameDataStrings calls updateResourceStrings even with the bar off (~140 hides);
    setCurrentEra whole-map updateGraphicEra for every AI era change; drawBattleEffects map scan every 23rd
    updateScreen (could iterate a list of battle plots). Low impact, low risk.

Not worth changing: the ~17k isCitySelected/getSelectionPlot queries per turn (sub-ms) and load-time
destroy/audio-tag calls seen in the harness.

Harness suggestions to make these measurable: reset g_engineCallCounts after scenario load; optionally call
GC.setGraphicsInitialized(true) in a mode where the stubbed create() functions return dummy non-NULL objects,
so updateSymbols/updateFlagSymbol/updateCenterUnit paths get counted; add per-call-site counters for
setDirty (file:line) to attribute dirty bits.
