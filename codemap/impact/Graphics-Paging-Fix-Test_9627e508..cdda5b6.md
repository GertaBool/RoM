# Impact of 9627e508fedc..cdda5b65d3da

Commits:

- cdda5b6 2026-11-21 Map trading fix 2

```
 Assets/CvGameCoreDLL/CvGame.cpp | 37 ++++++++++++++++++++++++---------
 Assets/CvGameCoreDLL/CvGame.h   |  3 ++-
 Assets/CvGameCoreDLL/CvPlot.cpp | 45 +++++++++++++++++++++++++++++++----------
 Assets/CvGameCoreDLL/CvPlot.h   |  3 ++-
 Assets/XML/GlobalDefinesAlt.xml |  5 +++++
 5 files changed, 71 insertions(+), 22 deletions(-)
```
_Members, XML fills and defines at cdda5b65d3da: the map's clang tables (exact)._

## C++ functions

- changed: 6; added: 0; removed: 0
  - changed CvGame::endBulkReveal  (CvGame.cpp:2308-2334)
  - changed CvGame::processDeferredReveals  (CvGame.cpp:2353-2404)
  - changed CvGame::updateGraphicsPaging  (CvGame.cpp:2406-2558)
  - changed CvPlot::refreshRevealedGraphics  (CvPlot.cpp:305-337)
  - changed CvPlot::setRevealed  (CvPlot.cpp:7700-7822)
  - changed CvPlot::setRevealedRouteType  (CvPlot.cpp:7940-7982)

## Member declarations

- none changed

## Members written on changed lines, or declared new

CvPlot::m_bRevealedRouteDirty

## Defines read on changed lines

GRAPHICS_PAGING_REVEAL_MAX

## XML

- GlobalDefinesAlt.xml: tags on changed lines: none; defines: GRAPHICS_PAGING_REVEAL_MAX

## Reach

| | start | reached | per level |
|---|---|---|---|
| member variables | 1 | 0 |  |
| C++ functions | 6 | 761 | 1: 16, 2: 38, 3: 62, 4: 114, 5: 127, 6: 102, 7: 223, 8: 44, 9: 18, 10: 8, 11: 4, 12: 3, 13: 1, 14: 1 |
| Python functions | 0 | 258 | 2: 6, 3: 15, 4: 31, 5: 25, 6: 82, 7: 53, 8: 31, 9: 8, 10: 5, 11: 2 |
| defines | 1 | 0 |  |

- C++ functions the exe calls (exported): 72: CvCity::cheat, CvDLLButtonPopup::OnOkClicked, CvDLLButtonPopup::launchButtonPopup, CvDeal::kill, CvEventReporter::gameStart, CvEventReporter::kbdEvent, CvEventReporter::reportModNetMessage, CvGame::cheatSpaceship, CvGame::implementDeal, CvGame::initDiplomacy, CvGame::initFreeState, CvGame::initFreeUnits ...
- C++ functions bound for Python: 131
- Python event handlers: 31: AIAutoPlay.onBeginGameTurn (BeginGameTurn), AIAutoPlay.onGameStart (GameStart), AIAutoPlay.onKbdEvent (kbdEvent), AIAutoPlay.onModNetMessage (ModNetMessage), AIAutoPlay.onVictory (victory), BarbarianCiv.onBeginGameTurn (BeginGameTurn), BarbarianCiv.onCityAcquired (cityAcquired), BarbarianCiv.onEndPlayerTurn (EndPlayerTurn), ChangePlayer.onKbdEvent (kbdEvent), CvEnhancedTechConquestEventManager.onCityAcquired (cityAcquired), CvEventManager.onCityRazed (cityRazed), CvEventManager.onKbdEvent (kbdEvent)
- C++ files: CvUnitAI.cpp 165, CvUnit.cpp 80, CvPlayer.cpp 67, CvGame.cpp 52, CvCity.cpp 38, CvTeam.cpp 37, CyPlayer.cpp 34, CvPlot.cpp 32, CvPlayerAI.cpp 23, CvSelectionGroup.cpp 21, CvMessageData.cpp 18, CyTeam.cpp 18, CyCity.cpp 18, CyUnit.cpp 18, CvDllPythonEvents.cpp 16, CvEventReporter.cpp 16, CyPlot.cpp 15, CvCityAI.cpp 13, CvMap.cpp 12, CvMapGenerator.cpp 10, CyMapGenerator.cpp 10, CvDeal.cpp 7, CyMap.cpp 7, CyGame.cpp 7, CvSelectionGroupAI.cpp 6
- Python modules: EntryPoints/CvRandomEventInterface.py 59, base/Screens/CvWorldBuilderScreen.py 23, EntryPoints/CvScreensInterface.py 19, Revolution/Gameready/Revolution.py 17, Revolution/Gameready/AIAutoPlay.py 14, Revolution/RevEvents.py 11, Revolution/Gameready/BarbarianCiv.py 11, PyHelpers.py 7, Revolution/RevUtils.py 7, Screens/PLE.py 7, base/pyWB/CvWBDesc.py 6, base/CvEventManager.py 6, RoMEventManager.py 6, Screens/CvMainInterface.py 6, ModTools/ModTools.py 5, base/CvDebugTools.py 5, base/CvPerfTest.py 5, Contrib/RevDCMReligionControl.py 5, CvMapGeneratorUtil.py 5, Revolution/Development/ChangePlayer.py 4, EntryPoints/CvWBInterface.py 3, base/Screens/CvWorldBuilderDiplomacyScreen.py 3, Revolution/Gameready/StartAsMinors.py 3, CvUtil.py 3, Revolution/RevolutionInit.py 3

## Member variables (1)

- CvPlot::m_bRevealedRouteDirty (CvPlot.h:612): bool

## XML tags and defines

- define GRAPHICS_PAGING_REVEAL_MAX: GlobalDefinesAlt.xml [mod]

## C++ functions, level by level


### level 0 (6)

- CvGame::endBulkReveal  (CvGame.cpp:2309)
- CvGame::processDeferredReveals  (CvGame.cpp:2354)
- CvGame::updateGraphicsPaging  (CvGame.cpp:2407)
- CvPlot::refreshRevealedGraphics  (CvPlot.cpp:306)
- CvPlot::setRevealed  (CvPlot.cpp:7701)
- CvPlot::setRevealedRouteType  (CvPlot.cpp:7941)

### level 1 (16)

- CvDeal::startTrade  (CvDeal.cpp:696)  <- call CvGame::endBulkReveal
- CvGame::update  (CvGame.cpp:2171)  <- call CvGame::updateGraphicsPaging
- CvMap::setRevealedPlots  (CvMap.cpp:291)  <- call CvPlot::setRevealed
- CvPlayer::acquireCity  (CvPlayer.cpp:2337)  <- call CvPlot::setRevealed
- CvPlayer::assimilatePlayer  (CvPlayer.cpp:22593)  <- call CvPlot::setRevealed
- CvPlayer::doAdvancedStartAction  (CvPlayer.cpp:16735)  <- call CvPlot::setRevealed
- CvPlayer::initFreeUnits  (CvPlayer.cpp:1848)  <- call CvPlot::setRevealed
- CvPlayer::receiveGoody  (CvPlayer.cpp:6344)  <- call CvPlot::setRevealed
- CvPlayer::splitEmpire  (CvPlayer.cpp:22369)  <- call CvPlot::setRevealed
- CvPlayerAI::AI_doAdvancedStart  (CvPlayerAI.cpp:23991)  <- call CvPlot::setRevealed
- CvPlot::changeStolenVisibilityCount  (CvPlot.cpp:7286)  <- call CvPlot::setRevealed
- CvPlot::changeVisibilityCount  (CvPlot.cpp:7189)  <- call CvPlot::setRevealed
- CvPlot::setRouteType  (CvPlot.cpp:5939)  <- call CvPlot::setRevealedRouteType
- CvTeam::addTeam  (CvTeam.cpp:520)  <- call CvPlot::setRevealed
- CvTeam::resetPlotAndCityData  (CvTeam.cpp:433)  <- call CvPlot::setRevealed
- CyPlot::setRevealed  (CyPlot.cpp:967)  <- call CvPlot::setRevealed

### level 2 (38)

- CvCity::doTask  (CvCity.cpp:1504)  <- call CvPlayer::acquireCity
- CvCity::liberate  (CvCity.cpp:15930)  <- call CvPlayer::acquireCity
- CvDeal::addTrades  (CvDeal.cpp:119)  <- call CvDeal::startTrade
- CvGame::initFreeState  (CvGame.cpp:786)  <- call CvMap::setRevealedPlots
- CvGame::initFreeUnits  (CvGame.cpp:846)  <- call CvPlayer::initFreeUnits
- CvGame::processVote  (CvGame.cpp:8467)  <- call CvPlayer::acquireCity
- CvGame::regenerateMap  (CvGame.cpp:348)  <- call CvMap::setRevealedPlots
- CvNetAdvancedStartAction::Execute  (CvMessageData.cpp:484)  <- call CvPlayer::doAdvancedStartAction
- CvNetEmpireSplit::Execute  (CvMessageData.cpp:588)  <- call CvPlayer::splitEmpire
- CvPlayer::doEspionageMission  (CvPlayer.cpp:16109)  <- call CvPlayer::acquireCity
- CvPlayer::doGoody  (CvPlayer.cpp:6546)  <- call CvPlayer::receiveGoody
- CvPlayer::initInGame  (CvPlayer.cpp:445)  <- call CvTeam::resetPlotAndCityData
- CvPlayer::setTurnActive  (CvPlayer.cpp:12160)  <- call CvPlayerAI::AI_doAdvancedStart
- CvPlayerAI::AI_advancedStartDoRoute  (CvPlayerAI.cpp:23752)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartPlaceCity  (CvPlayerAI.cpp:23638)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartPlaceExploreUnits  (CvPlayerAI.cpp:23529)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartRevealRadius  (CvPlayerAI.cpp:23613)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartRouteTerritory  (CvPlayerAI.cpp:23788)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_doSplit  (CvPlayerAI.cpp:20180)  <- call CvPlayer::splitEmpire
- CvPlot::applyEvent  (CvPlot.cpp:10212)  <- call CvPlot::setRouteType
- CvPlot::changeAdjacentSight  (CvPlot.cpp:1854)  <- call CvPlot::changeVisibilityCount
- CvPlot::changeBuildProgress  (CvPlot.cpp:7998)  <- call CvPlot::setRouteType
- CvPlot::erase  (CvPlot.cpp:449)  <- call CvPlot::setRouteType
- CvPlot::setOwner  (CvPlot.cpp:5002)  <- call CvPlayer::acquireCity
- CvPlot::updateCityRoute  (CvPlot.cpp:5986)  <- call CvPlot::setRouteType
- CvTeam::setHasTech  (CvTeam.cpp:5947)  <- call CvMap::setRevealedPlots
- CvTeam::setStolenVisibilityTimer  (CvTeam.cpp:4270)  <- call CvPlot::changeStolenVisibilityCount
- CvUnit::pillage  (CvUnit.cpp:5400)  <- call CvPlot::setRouteType
- CvUnit::setXY  (CvUnit.cpp:10566)  <- call CvPlayer::acquireCity
- CyMap::setRevealedPlots  (CyMap.cpp:34)  <- call CvMap::setRevealedPlots
- CyPlayer::acquireCity  (CyPlayer.cpp:153)  <- call CvPlayer::acquireCity
- CyPlayer::assimilatePlayer  (CyPlayer.cpp:2518)  <- call CvPlayer::assimilatePlayer
- CyPlayer::receiveGoody  (CyPlayer.cpp:496)  <- call CvPlayer::receiveGoody
- CyPlayer::splitEmpire  (CyPlayer.cpp:2483)  <- call CvPlayer::splitEmpire
- CyPlot::changeVisibilityCount  (CyPlot.cpp:936)  <- call CvPlot::changeVisibilityCount
- CyPlot::setRouteType  (CyPlot.cpp:787)  <- call CvPlot::setRouteType
- CyPlotPythonInterface1  (CyPlotInterface1.cpp:15)  <- call CyPlot::setRevealed
- CyTeam::addTeam  (CyTeam.cpp:48)  <- call CvTeam::addTeam

### level 3 (62)

- CvCity::init  (CvCity.cpp:157)  <- call CvPlot::setOwner
- CvCity::kill  (CvCity.cpp:1005)  <- call CvPlot::changeAdjacentSight
- CvDLLButtonPopup::OnOkClicked  (CvDLLButtonPopup.cpp:75)  <- call CvGame::regenerateMap
- CvGame::addPlayer  (CvGame.cpp:9533)  <- call CvPlayer::initInGame
- CvGame::cheatSpaceship  (CvGameInterface.cpp:2561)  <- call CvTeam::setHasTech
- CvGame::doTurn  (CvGame.cpp:6606)  <- call CvPlayer::setTurnActive
- CvGame::implementDeal  (CvGame.cpp:3289)  <- call CvDeal::addTrades
- CvGame::nextActivePlayer  (CvGameInterface.cpp:2691)  <- call CvPlayer::setTurnActive
- CvGame::setInitialItems  (CvGame.cpp:293)  <- call CvGame::initFreeState
- CvGame::setVoteOutcome  (CvGame.cpp:6019)  <- call CvGame::processVote
- CvMap::erasePlots  (CvMap.cpp:280)  <- call CvPlot::erase
- CvNetDoTask::Execute  (CvMessageData.cpp:283)  <- call CvCity::doTask
- CvNetResearch::Execute  (CvMessageData.cpp:376)  <- call CvTeam::setHasTech
- CvPlayer::applyEvent  (CvPlayer.cpp:20656)  <- call CvPlot::applyEvent
- CvPlayer::cheat  (CvPlayer.cpp:24740)  <- call CvTeam::setHasTech
- CvPlayer::setAlive  (CvPlayer.cpp:11816)  <- call CvPlayer::setTurnActive
- CvPlayer::setAutoMoves  (CvPlayer.cpp:12481)  <- call CvPlayer::setTurnActive
- CvPlayer::setNewPlayerAlive  (CvPlayer.cpp:11916)  <- call CvPlayer::setTurnActive
- CvPlayerAI::AI_chooseFreeTech  (CvPlayerAI.cpp:7103)  <- call CvTeam::setHasTech
- CvPlayerAI::AI_conquerCity  (CvPlayerAI.cpp:1744)  <- call CvCity::doTask
- CvPlayerAI::AI_doTurnUnitsPost  (CvPlayerAI.cpp:625)  <- call CvPlayerAI::AI_doSplit
- CvPlot::doCulture  (CvPlot.cpp:8946)  <- call CvPlot::setOwner
- CvPlot::setPlotType  (CvPlot.cpp:5292)  <- call CvPlot::erase
- CvPlot::updateCulture  (CvPlot.cpp:713)  <- call CvPlot::setOwner
- CvPlot::updateSight  (CvPlot.cpp:2092)  <- call CvPlot::changeAdjacentSight
- CvSelectionGroup::setRemoteTransportUnit  (CvSelectionGroup.cpp:5064)  <- call CvUnit::setXY
- CvSelectionGroup::startMission  (CvSelectionGroup.cpp:1372)  <- call CvUnit::pillage
- CvTeam::changeStolenVisibilityTimer  (CvTeam.cpp:4302)  <- call CvTeam::setStolenVisibilityTimer
- CvTeam::processTech  (CvTeam.cpp:6792)  <- call CvPlot::updateCityRoute
- CvTeam::setResearchProgress  (CvTeam.cpp:5595)  <- call CvTeam::setHasTech
- CvTeam::setTurnActive  (CvTeam.cpp:7295)  <- call CvPlayer::setTurnActive
- CvTeam::shareCounters  (CvTeam.cpp:897)  <- call CvTeam::setStolenVisibilityTimer
- CvTeam::shareItems  (CvTeam.cpp:820)  <- call CvTeam::setHasTech
- CvTeam::updateTechShare  (CvTeam.cpp:6634)  <- call CvTeam::setHasTech
- CvUnit::airlift  (CvUnit.cpp:4203)  <- call CvUnit::setXY
- CvUnit::build  (CvUnit.cpp:7641)  <- call CvPlot::changeBuildProgress
- CvUnit::changeExtraVisibilityRange  (CvUnit.cpp:11540)  <- call CvPlot::changeAdjacentSight
- CvUnit::espionage  (CvUnit.cpp:7332)  <- call CvPlayer::doEspionageMission
- CvUnit::init  (CvUnit.cpp:100)  <- call CvUnit::setXY
- CvUnit::jumpToNearestValidPlot  (CvUnit.cpp:3216)  <- call CvUnit::setXY
- CvUnit::kill  (CvUnit.cpp:582)  <- call CvUnit::setXY
- CvUnit::move  (CvUnit.cpp:3173)  <- call CvUnit::setXY
- CvUnit::paradrop  (CvUnit.cpp:4704)  <- call CvUnit::setXY
- CvUnit::setFacingDirection  (CvUnit.cpp:11905)  <- call CvPlot::changeAdjacentSight
- CvUnit::setReconPlot  (CvUnit.cpp:11086)  <- call CvPlot::changeAdjacentSight
- CvUnit::testSpyIntercepted  (CvUnit.cpp:7400)  <- call CvUnit::setXY
- CyCity::doTask  (CyCity.cpp:216)  <- call CvCity::doTask
- CyCity::liberate  (CyCity.cpp:2814)  <- call CvCity::liberate
- CyGame::regenerateMap  (CyGame.cpp:1285)  <- call CvGame::regenerateMap
- CyMapPythonInterface  (CyMapInterface.cpp:17)  <- call CyMap::setRevealedPlots
- ... 12 more

(levels above 3: 645 more)

## Python functions, level by level


### level 2 (6)

- canTriggerHolyMountainRevealed  (EntryPoints/CvRandomEventInterface.py:218)  <- py>cpp CyPlot::setRevealed
- Revolution.processRevolution  (Revolution/Gameready/Revolution.py:5015)  <- py>cpp CyPlot::setRevealed
- Revolution.spawnRevolutionaries  (Revolution/Gameready/Revolution.py:6243)  <- py>cpp CyPlot::setRevealed
- CvWorldBuilderScreen.RevealCurrentPlot  (base/Screens/CvWorldBuilderScreen.py:2314)  <- py>cpp (name match) CyPlot::setRevealed
- CvWorldBuilderScreen.revealAll  (base/Screens/CvWorldBuilderScreen.py:2304)  <- py>cpp CyPlot::setRevealed
- CvWBDesc.applyInitialItems  (base/pyWB/CvWBDesc.py:1617)  <- py>cpp CyPlot::setRevealed

### level 3 (15)

- WorldBuilderRevealAllCB  (EntryPoints/CvScreensInterface.py:578)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.revealAll
- WorldBuilderUnRevealAllCB  (EntryPoints/CvScreensInterface.py:581)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.revealAll
- applyInitialItems  (EntryPoints/CvWBInterface.py:269)  <- py>py base/pyWB/CvWBDesc.py CvWBDesc.applyInitialItems
- readAndApplyDesc  (EntryPoints/CvWBInterface.py:232)  <- py>py base/pyWB/CvWBDesc.py CvWBDesc.applyInitialItems
- Revolution.joinHumanHandler  (Revolution/Gameready/Revolution.py:6018)  <- py>py Revolution/Gameready/Revolution.py Revolution.processRevolution
- Revolution.launchRevolution  (Revolution/Gameready/Revolution.py:6189)  <- py>py Revolution/Gameready/Revolution.py Revolution.spawnRevolutionaries
- Revolution.makeRevolutionDecision  (Revolution/Gameready/Revolution.py:4192)  <- py>py Revolution/Gameready/Revolution.py Revolution.processRevolution
- Revolution.revolutionNetworkPopupHandler  (Revolution/Gameready/Revolution.py:4906)  <- py>py Revolution/Gameready/Revolution.py Revolution.processRevolution
- assimilateHandler  (Revolution/RevEvents.py:1150)  <- py>cpp CyPlayer::assimilatePlayer
- checkForAssimilation  (Revolution/RevEvents.py:891)  <- py>cpp (only target) CyPlayer::assimilatePlayer
- CvWorldBuilderScreen.eraseAll  (base/Screens/CvWorldBuilderScreen.py:2448)  <- py>cpp (only target) CyPlot::setRouteType
- CvWorldBuilderScreen.placeObject  (base/Screens/CvWorldBuilderScreen.py:714)  <- py>cpp (only target) CyPlot::setRouteType
- CvWorldBuilderScreen.removeObject  (base/Screens/CvWorldBuilderScreen.py:931)  <- py>cpp (only target) CyPlot::setRouteType
- CvWorldBuilderScreen.setMultipleReveal  (base/Screens/CvWorldBuilderScreen.py:1909)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.RevealCurrentPlot
- CvPlotDesc.apply  (base/pyWB/CvWBDesc.py:1118)  <- py>cpp CyPlot::setRouteType

(levels above 3: 237 more)

## Reach per start node

| start | reached | C++ | Python | members |
|---|---|---|---|---|
| CvPlot::setRevealedRouteType | 1020 | 762 | 258 | 0 |
| CvPlot::setRevealed | 1016 | 758 | 258 | 0 |
| CvPlot::m_bRevealedRouteDirty | 1008 | 756 | 252 | 0 |
| GRAPHICS_PAGING_REVEAL_MAX | 1007 | 755 | 252 | 0 |
| CvPlot::refreshRevealedGraphics | 1007 | 755 | 252 | 0 |
| CvGame::processDeferredReveals | 1006 | 754 | 252 | 0 |
| CvGame::endBulkReveal | 1004 | 752 | 252 | 0 |
| CvGame::updateGraphicsPaging | 1 | 1 | 0 | 0 |
