# Impact of 71de0abe5dc8..cdda5b65d3da

Commits:

- cdda5b6 2026-11-21 Map trading fix 2
- 9627e50 2026-11-21 Map trade fix, GPT fix also
- 9b85482 2026-11-20 Update 3 files

```
 Assets/CvGameCoreDLL/CvCity.cpp     |  26 +++-
 Assets/CvGameCoreDLL/CvDeal.cpp     |   6 +-
 Assets/CvGameCoreDLL/CvGame.cpp     | 251 ++++++++++++++++++++++++++++++++----
 Assets/CvGameCoreDLL/CvGame.h       |  12 +-
 Assets/CvGameCoreDLL/CvPlayerAI.cpp |  55 ++++----
 Assets/CvGameCoreDLL/CvPlot.cpp     |  90 ++++++++++++-
 Assets/CvGameCoreDLL/CvPlot.h       |   8 ++
 Assets/XML/GlobalDefinesAlt.xml     |  12 +-
 8 files changed, 393 insertions(+), 67 deletions(-)
```
_Members, XML fills and defines at cdda5b65d3da: the map's clang tables (exact)._

## C++ functions

- changed: 13; added: 8; removed: 0
  - changed CvCity::setRevealed  (CvCity.cpp:10862-10905)
  - changed CvDeal::startTrade  (CvDeal.cpp:695-1094)
  - changed CvGame::reset  (CvGame.cpp:482-726)
  - changed CvGame::updateGraphicsPaging  (CvGame.cpp:2406-2558)
  - changed CvGame::pageGraphics  (CvGame.cpp:2696-2896)
  - changed CvPlayerAI::AI_counterPropose  (CvPlayerAI.cpp:9090-9641)
  - changed CvPlayerAI::AI_goldPerTurnTradeVal  (CvPlayerAI.cpp:9702-9708)
  - changed CvPlayerAI::AI_doDiplo  (CvPlayerAI.cpp:17242-19180)
  - changed CvPlot::reset  (CvPlot.cpp:179-266)
  - changed CvPlot::setupGraphical  (CvPlot.cpp:272-294)
  - changed CvPlot::setRevealed  (CvPlot.cpp:7700-7822)
  - changed CvPlot::setRevealedImprovementType  (CvPlot.cpp:7888-7916)
  - changed CvPlot::setRevealedRouteType  (CvPlot.cpp:7940-7982)
  - added CvGame::beginBulkReveal  (CvGame.cpp:2295-2306)
  - added CvGame::endBulkReveal  (CvGame.cpp:2308-2334)
  - added CvGame::deferRevealedGraphics  (CvGame.cpp:2336-2351)
  - added CvGame::processDeferredReveals  (CvGame.cpp:2353-2404)
  - added CvPlot::deferRevealedGraphics  (CvPlot.cpp:296-299)
  - added CvPlot::refreshRevealedGraphics  (CvPlot.cpp:305-337)
  - added CvPlot::isRevealedGraphicsDirty  (CvPlot.h:68-68)
  - added CvPlot::setRevealedGraphicsDirty  (CvPlot.h:69-69)

## Member declarations

- added CvGame::m_aiDeferredRevealPlots std::vector<int>
- added CvGame::m_bPagingPendingOut bool
- added CvGame::m_eBulkRevealTeam TeamTypes
- added CvGame::m_iBulkRevealDepth int
- added CvPlot::m_bRevealedGraphicsDirty bool
- added CvPlot::m_bRevealedRouteDirty bool

## Members written on changed lines, or declared new

CvGame::m_aiDeferredRevealPlots, CvGame::m_bPagingPending, CvGame::m_bPagingPendingOut, CvGame::m_eBulkRevealTeam, CvGame::m_iBulkRevealDepth, CvPlot::m_bRevealedGraphicsDirty, CvPlot::m_bRevealedRouteDirty

## Defines read on changed lines

GRAPHICS_PAGING_LOG, GRAPHICS_PAGING_MAX_OUT, GRAPHICS_PAGING_REVEAL_MAX, PEACE_TREATY_LENGTH

## XML

- GlobalDefinesAlt.xml: tags on changed lines: none; defines: GRAPHICS_PAGING_MAX_OUT, GRAPHICS_PAGING_REVEAL_MAX

## Reach

| | start | reached | per level |
|---|---|---|---|
| member variables | 7 | 0 |  |
| C++ functions | 21 | 841 | 1: 37, 2: 71, 3: 104, 4: 124, 5: 129, 6: 99, 7: 203, 8: 46, 9: 17, 10: 8, 11: 3 |
| Python functions | 0 | 316 | 2: 6, 3: 28, 4: 50, 5: 31, 6: 77, 7: 56, 8: 28, 9: 23, 10: 10, 11: 3, 12: 4 |
| defines | 4 | 0 |  |

- C++ functions the exe calls (exported): 101: CvCity::cheat, CvDLLButtonPopup::OnOkClicked, CvDLLButtonPopup::launchButtonPopup, CvDLLWidgetData::executeAction, CvDLLWidgetData::isLink, CvDLLWidgetData::parseHelp, CvDeal::isCancelable, CvDeal::kill, CvDeal::turnsToCancel, CvEventReporter::gameStart, CvEventReporter::kbdEvent, CvEventReporter::reportModNetMessage ...
- C++ functions bound for Python: 143
- Python event handlers: 35: AIAutoPlay.onBeginGameTurn (BeginGameTurn), AIAutoPlay.onGameStart (GameStart), AIAutoPlay.onKbdEvent (kbdEvent), AIAutoPlay.onModNetMessage (ModNetMessage), AIAutoPlay.onVictory (victory), BarbarianCiv.onBeginGameTurn (BeginGameTurn), BarbarianCiv.onCityAcquired (cityAcquired), BarbarianCiv.onEndPlayerTurn (EndPlayerTurn), ChangePlayer.onKbdEvent (kbdEvent), CvEnhancedTechConquestEventManager.onCityAcquired (cityAcquired), CvEventManager.onCityRazed (cityRazed), CvEventManager.onKbdEvent (kbdEvent)
- C++ files: CvUnitAI.cpp 165, CvUnit.cpp 80, CvPlayer.cpp 75, CvGame.cpp 65, CvCity.cpp 39, CvPlot.cpp 39, CvTeam.cpp 37, CyPlayer.cpp 37, CvPlayerAI.cpp 33, CvSelectionGroup.cpp 21, CyCity.cpp 19, CvMessageData.cpp 19, CyTeam.cpp 18, CyUnit.cpp 18, CvDLLWidgetData.cpp 17, CvDllPythonEvents.cpp 17, CvEventReporter.cpp 17, CyPlot.cpp 15, CvMap.cpp 13, CvGameTextMgr.cpp 13, CvCityAI.cpp 13, CvDeal.cpp 10, CvMapGenerator.cpp 10, CyMapGenerator.cpp 10, CyMap.cpp 7
- Python modules: EntryPoints/CvRandomEventInterface.py 60, base/Screens/CvWorldBuilderScreen.py 23, EntryPoints/CvScreensInterface.py 19, Revolution/Gameready/Revolution.py 17, Contrib/MoreCiv4lerts.py 15, Revolution/Gameready/AIAutoPlay.py 14, Revolution/RevEvents.py 11, Revolution/Gameready/BarbarianCiv.py 11, PyHelpers.py 7, Revolution/RevUtils.py 7, Screens/PLE.py 7, base/pyWB/CvWBDesc.py 6, RoMEventManager.py 6, Screens/CvForeignAdvisor.py 6, base/CvEventManager.py 6, Screens/CvMainInterface.py 6, base/CvDebugTools.py 5, Screens/CvExoticForeignAdvisor.py 5, ModTools/ModTools.py 5, base/CvPerfTest.py 5, CvMapGeneratorUtil.py 5, Contrib/RevDCMReligionControl.py 5, Screens/CvPediaMain.py 5, BUG/DealUtil.py 4, Revolution/Development/ChangePlayer.py 4

## Member variables (7)

- CvGame::m_aiDeferredRevealPlots (CvGame.h:688): std::vector<int>
- CvGame::m_bPagingPending (CvGame.h:684): bool
- CvGame::m_bPagingPendingOut (CvGame.h:685): bool
- CvGame::m_eBulkRevealTeam (CvGame.h:687): TeamTypes
- CvGame::m_iBulkRevealDepth (CvGame.h:686): int
- CvPlot::m_bRevealedGraphicsDirty (CvPlot.h:611): bool
- CvPlot::m_bRevealedRouteDirty (CvPlot.h:612): bool

## XML tags and defines

- define GRAPHICS_PAGING_LOG: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MAX_OUT: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_REVEAL_MAX: GlobalDefinesAlt.xml [mod]
- define PEACE_TREATY_LENGTH: GlobalDefines.xml [mod]

## C++ functions, level by level


### level 0 (21)

- CvCity::setRevealed  (CvCity.cpp:10863)
- CvDeal::startTrade  (CvDeal.cpp:696)
- CvGame::beginBulkReveal  (CvGame.cpp:2296)
- CvGame::deferRevealedGraphics  (CvGame.cpp:2337)
- CvGame::endBulkReveal  (CvGame.cpp:2309)
- CvGame::pageGraphics  (CvGame.cpp:2697)
- CvGame::processDeferredReveals  (CvGame.cpp:2354)
- CvGame::reset  (CvGame.cpp:483)
- CvGame::updateGraphicsPaging  (CvGame.cpp:2407)
- CvPlayerAI::AI_counterPropose  (CvPlayerAI.cpp:9091)
- CvPlayerAI::AI_doDiplo  (CvPlayerAI.cpp:17243)
- CvPlayerAI::AI_goldPerTurnTradeVal  (CvPlayerAI.cpp:9703)
- CvPlot::deferRevealedGraphics  (CvPlot.cpp:297)
- CvPlot::isRevealedGraphicsDirty  (CvPlot.h:68)
- CvPlot::refreshRevealedGraphics  (CvPlot.cpp:306)
- CvPlot::reset  (CvPlot.cpp:180)
- CvPlot::setRevealed  (CvPlot.cpp:7701)
- CvPlot::setRevealedGraphicsDirty  (CvPlot.h:69)
- CvPlot::setRevealedImprovementType  (CvPlot.cpp:7889)
- CvPlot::setRevealedRouteType  (CvPlot.cpp:7941)
- CvPlot::setupGraphical  (CvPlot.cpp:273)

### level 1 (37)

- CvCity::init  (CvCity.cpp:157)  <- call CvCity::setRevealed
- CvDLLWidgetData::parseTradeItem  (CvDLLWidgetData.cpp:4631)  <- define PEACE_TREATY_LENGTH
- CvDeal::addTrades  (CvDeal.cpp:119)  <- call CvDeal::startTrade
- CvDeal::doTurn  (CvDeal.cpp:298)  <- define PEACE_TREATY_LENGTH
- CvDeal::turnsToCancel  (CvDeal.cpp:1299)  <- define PEACE_TREATY_LENGTH
- CvGame::CvGame  (CvGame.cpp:50)  <- call CvGame::reset
- CvGame::init  (CvGame.cpp:108)  <- call CvGame::reset
- CvGame::read  (CvGame.cpp:8971)  <- call CvGame::reset
- CvGame::update  (CvGame.cpp:2171)  <- call CvGame::updateGraphicsPaging
- CvGameTextMgr::getTradeString  (CvGameTextMgr.cpp:15442)  <- define PEACE_TREATY_LENGTH
- CvGameTextMgr::getTurnTimerText  (CvGameTextMgr.cpp:19628)  <- define PEACE_TREATY_LENGTH
- CvMap::setRevealedPlots  (CvMap.cpp:291)  <- call CvPlot::setRevealed
- CvMap::setupGraphical  (CvMap.cpp:263)  <- call CvPlot::setupGraphical
- CvPlayer::acquireCity  (CvPlayer.cpp:2337)  <- call CvPlot::setRevealed
- CvPlayer::assimilatePlayer  (CvPlayer.cpp:22593)  <- call CvPlot::setRevealed
- CvPlayer::doAdvancedStartAction  (CvPlayer.cpp:16735)  <- call CvPlot::setRevealed
- CvPlayer::getItemTradeString  (CvPlayer.cpp:24024)  <- define PEACE_TREATY_LENGTH
- CvPlayer::initFreeUnits  (CvPlayer.cpp:1848)  <- call CvPlot::setRevealed
- CvPlayer::receiveGoody  (CvPlayer.cpp:6344)  <- call CvPlot::setRevealed
- CvPlayer::splitEmpire  (CvPlayer.cpp:22369)  <- call CvPlot::setRevealed
- CvPlayerAI::AI_bonusTradeVal  (CvPlayerAI.cpp:10120)  <- define PEACE_TREATY_LENGTH
- CvPlayerAI::AI_dealVal  (CvPlayerAI.cpp:8823)  <- call CvPlayerAI::AI_goldPerTurnTradeVal
- CvPlayerAI::AI_doAdvancedStart  (CvPlayerAI.cpp:23991)  <- call CvPlot::setRevealed
- CvPlayerAI::AI_doTurnPost  (CvPlayerAI.cpp:543)  <- call CvPlayerAI::AI_doDiplo
- CvPlayerAI::AI_eventValue  (CvPlayerAI.cpp:19602)  <- define PEACE_TREATY_LENGTH
- CvPlayerAI::AI_maxGoldPerTurnTrade  (CvPlayerAI.cpp:9679)  <- define PEACE_TREATY_LENGTH
- CvPlot::CvPlot  (CvPlot.cpp:44)  <- call CvPlot::reset
- CvPlot::changeStolenVisibilityCount  (CvPlot.cpp:7286)  <- call CvPlot::setRevealed
- CvPlot::changeVisibilityCount  (CvPlot.cpp:7189)  <- call CvPlot::setRevealed
- CvPlot::init  (CvPlot.cpp:108)  <- call CvPlot::reset
- CvPlot::read  (CvPlot.cpp:9204)  <- call CvPlot::reset
- CvPlot::setImprovementType  (CvPlot.cpp:5818)  <- call CvPlot::setRevealedImprovementType
- CvPlot::setRouteType  (CvPlot.cpp:5939)  <- call CvPlot::setRevealedRouteType
- CvTeam::addTeam  (CvTeam.cpp:520)  <- call CvPlot::setRevealed
- CvTeam::resetPlotAndCityData  (CvTeam.cpp:433)  <- call CvCity::setRevealed
- CyCity::setRevealed  (CyCity.cpp:2236)  <- call CvCity::setRevealed
- CyPlot::setRevealed  (CyPlot.cpp:967)  <- call CvPlot::setRevealed

### level 2 (71)

- CvCity::applyEvent  (CvCity.cpp:15236)  <- call CvPlot::setImprovementType
- CvCity::doTask  (CvCity.cpp:1504)  <- call CvPlayer::acquireCity
- CvCity::kill  (CvCity.cpp:1005)  <- call CvPlot::setImprovementType
- CvCity::liberate  (CvCity.cpp:15930)  <- call CvPlayer::acquireCity
- CvDLLWidgetData::parseHelp  (CvDLLWidgetData.cpp:53)  <- call CvDLLWidgetData::parseTradeItem
- CvDeal::isCancelable  (CvDeal.cpp:1280)  <- call CvDeal::turnsToCancel
- CvGame::doDeals  (CvGame.cpp:6754)  <- call CvDeal::doTurn
- CvGame::doGlobalWarming  (CvGame.cpp:6768)  <- call CvPlot::setImprovementType
- CvGame::implementDeal  (CvGame.cpp:3289)  <- call CvDeal::addTrades
- CvGame::initFreeState  (CvGame.cpp:786)  <- call CvMap::setRevealedPlots
- CvGame::initFreeUnits  (CvGame.cpp:846)  <- call CvPlayer::initFreeUnits
- CvGame::processVote  (CvGame.cpp:8467)  <- call CvPlayer::acquireCity
- CvGame::regenerateMap  (CvGame.cpp:348)  <- call CvMap::setupGraphical
- CvGameAI::CvGameAI  (CvGameAI.cpp:13)  <- call CvGame::CvGame
- CvGameAI::read  (CvGameAI.cpp:113)  <- call CvGame::read
- CvGameTextMgr::getDealString  (CvGameTextMgr.cpp:15071)  <- call CvGameTextMgr::getTradeString
- CvMap::init  (CvMap.cpp:65)  <- call CvPlot::init
- CvMap::read  (CvMap.cpp:1300)  <- call CvPlot::CvPlot
- CvMapGenerator::addGoodies  (CvMapGenerator.cpp:888)  <- call CvPlot::setImprovementType
- CvNetAdvancedStartAction::Execute  (CvMessageData.cpp:484)  <- call CvPlayer::doAdvancedStartAction
- CvNetEmpireSplit::Execute  (CvMessageData.cpp:588)  <- call CvPlayer::splitEmpire
- CvPlayer::applyEvent  (CvPlayer.cpp:20656)  <- call CvPlot::setImprovementType
- CvPlayer::doEspionageMission  (CvPlayer.cpp:16109)  <- call CvPlayer::acquireCity
- CvPlayer::doGoody  (CvPlayer.cpp:6546)  <- call CvPlayer::receiveGoody
- CvPlayer::doTurn  (CvPlayer.cpp:3918)  <- call CvPlayerAI::AI_doTurnPost
- CvPlayer::initCity  (CvPlayer.cpp:2320)  <- call CvCity::init
- CvPlayer::initInGame  (CvPlayer.cpp:445)  <- call CvTeam::resetPlotAndCityData
- CvPlayer::setTurnActive  (CvPlayer.cpp:12160)  <- call CvPlayerAI::AI_doAdvancedStart
- CvPlayerAI::AI_advancedStartDoRoute  (CvPlayerAI.cpp:23752)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartPlaceCity  (CvPlayerAI.cpp:23638)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartPlaceExploreUnits  (CvPlayerAI.cpp:23529)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartRevealRadius  (CvPlayerAI.cpp:23613)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartRouteTerritory  (CvPlayerAI.cpp:23788)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_chooseEvent  (CvPlayerAI.cpp:20145)  <- call CvPlayerAI::AI_eventValue
- CvPlayerAI::AI_considerOffer  (CvPlayerAI.cpp:8937)  <- call CvPlayerAI::AI_dealVal
- CvPlayerAI::AI_doSplit  (CvPlayerAI.cpp:20180)  <- call CvPlayer::splitEmpire
- CvPlayerAI::AI_stopTradingTradeVal  (CvPlayerAI.cpp:10641)  <- call CvPlayerAI::AI_dealVal
- CvPlot::applyEvent  (CvPlot.cpp:10212)  <- call CvPlot::setImprovementType
- CvPlot::changeAdjacentSight  (CvPlot.cpp:1854)  <- call CvPlot::changeVisibilityCount
- CvPlot::changeBuildProgress  (CvPlot.cpp:7998)  <- call CvPlot::setImprovementType
- CvPlot::doImprovementUpgrade  (CvPlot.cpp:693)  <- call CvPlot::setImprovementType
- CvPlot::erase  (CvPlot.cpp:449)  <- call CvPlot::setImprovementType
- CvPlot::nukeExplosion  (CvPlot.cpp:1058)  <- call CvPlot::setImprovementType
- CvPlot::removeGoody  (CvPlot.cpp:3697)  <- call CvPlot::setImprovementType
- CvPlot::setFeatureType  (CvPlot.cpp:5597)  <- call CvPlot::setImprovementType
- CvPlot::setOwner  (CvPlot.cpp:5002)  <- call CvPlayer::acquireCity
- CvPlot::updateCityRoute  (CvPlot.cpp:5986)  <- call CvPlot::setRouteType
- CvTeam::setHasTech  (CvTeam.cpp:5947)  <- call CvMap::setRevealedPlots
- CvTeam::setStolenVisibilityTimer  (CvTeam.cpp:4270)  <- call CvPlot::changeStolenVisibilityCount
- CvUnit::airBomb  (CvUnit.cpp:4895)  <- call CvPlot::setImprovementType
- ... 21 more

### level 3 (104)

- CvCity::doMeltdown  (CvCity.cpp:14052)  <- call CvPlot::nukeExplosion
- CvDLLButtonPopup::OnOkClicked  (CvDLLButtonPopup.cpp:75)  <- call CvPlayerAI::AI_considerOffer
- CvDLLWidgetData::doDealKill  (CvDLLWidgetData.cpp:5969)  <- call CvDeal::isCancelable
- CvDLLWidgetData::isLink  (CvDLLWidgetData.cpp:1072)  <- call CvDeal::isCancelable
- CvDLLWidgetData::parseKillDealHelp  (CvDLLWidgetData.cpp:5906)  <- call CvDeal::isCancelable
- CvDeal::startTeamTrade  (CvDeal.cpp:1198)  <- call CvGame::implementDeal
- CvDeal::verify  (CvDeal.cpp:336)  <- call CvDeal::isCancelable
- CvGame::addPlayer  (CvGame.cpp:9533)  <- call CvPlayer::initInGame
- CvGame::cheatSpaceship  (CvGameInterface.cpp:2561)  <- call CvTeam::setHasTech
- CvGame::doTurn  (CvGame.cpp:6606)  <- call CvPlayer::setTurnActive
- CvGame::initDiplomacy  (CvGame.cpp:730)  <- call CvGame::implementDeal
- CvGame::nextActivePlayer  (CvGameInterface.cpp:2691)  <- call CvPlayer::setTurnActive
- CvGame::normalizeAddExtras  (CvGame.cpp:1748)  <- call CvPlot::setFeatureType
- CvGame::normalizeAddGoodTerrain  (CvGame.cpp:1643)  <- call CvPlot::setFeatureType
- CvGame::normalizeAddRiver  (CvGame.cpp:1206)  <- call CvPlot::setFeatureType
- CvGame::normalizeRemoveBadFeatures  (CvGame.cpp:1370)  <- call CvPlot::setFeatureType
- CvGame::setInitialItems  (CvGame.cpp:293)  <- call CvGame::initFreeState
- CvGame::setVoteOutcome  (CvGame.cpp:6019)  <- call CvGame::processVote
- CvGameTextMgr::getDealString  (CvGameTextMgr.cpp:15060)  <- call CvGameTextMgr::getDealString
- CvGlobals::init  (CvGlobals.cpp:384)  <- call CvGameAI::CvGameAI
- CvMap::erasePlots  (CvMap.cpp:280)  <- call CvPlot::erase
- CvMap::rebuild  (CvMap.cpp:1378)  <- call CvMap::init
- CvMapGenerator::addFeatures  (CvMapGenerator.cpp:644)  <- call CvPlot::setFeatureType
- CvMapGenerator::addGameElements  (CvMapGenerator.cpp:240)  <- call CvMapGenerator::addGoodies
- CvMapGenerator::eraseFeatures  (CvMapGenerator.cpp:957)  <- call CvPlot::setFeatureType
- CvMapGenerator::eraseGoodies  (CvMapGenerator.cpp:979)  <- call CvPlot::removeGoody
- CvNetDoTask::Execute  (CvMessageData.cpp:283)  <- call CvCity::doTask
- CvNetEventTriggered::Execute  (CvMessageData.cpp:685)  <- call CvPlayer::applyEvent
- CvNetResearch::Execute  (CvMessageData.cpp:376)  <- call CvTeam::setHasTech
- CvPlayer::cheat  (CvPlayer.cpp:24740)  <- call CvTeam::setHasTech
- CvPlayer::disband  (CvPlayer.cpp:6222)  <- call CvCity::kill
- CvPlayer::doEvents  (CvPlayer.cpp:21539)  <- call CvPlayer::applyEvent
- CvPlayer::forcePeace  (CvPlayer.cpp:23601)  <- call CvGame::implementDeal
- CvPlayer::found  (CvPlayer.cpp:6737)  <- call CvPlayer::initCity
- CvPlayer::isTradingWithTeam  (CvPlayer.cpp:5899)  <- call CvDeal::isCancelable
- CvPlayer::killCities  (CvPlayer.cpp:2951)  <- call CvCity::kill
- CvPlayer::read  (CvPlayer.cpp:18464)  <- call ReadStreamableFFreeListTrashArray<class CvSelectionGroupAI>
- CvPlayer::setAlive  (CvPlayer.cpp:11816)  <- call CvPlayer::setTurnActive
- CvPlayer::setAutoMoves  (CvPlayer.cpp:12481)  <- call CvPlayer::setTurnActive
- CvPlayer::setNewPlayerAlive  (CvPlayer.cpp:11916)  <- call CvPlayer::setTurnActive
- CvPlayer::stopTradingWithTeam  (CvPlayer.cpp:5963)  <- call CvDeal::isCancelable
- CvPlayer::trigger  (CvPlayer.cpp:21805)  <- call CvPlayer::applyEvent
- CvPlayerAI::AI_chooseFreeTech  (CvPlayerAI.cpp:7103)  <- call CvTeam::setHasTech
- CvPlayerAI::AI_conquerCity  (CvPlayerAI.cpp:1744)  <- call CvCity::doTask
- CvPlayerAI::AI_doPeace  (CvPlayerAI.cpp:862)  <- call CvGame::implementDeal
- CvPlayerAI::AI_doTurnUnitsPost  (CvPlayerAI.cpp:625)  <- call CvPlayerAI::AI_doSplit
- CvPlot::doCulture  (CvPlot.cpp:8946)  <- call CvPlot::setOwner
- CvPlot::doFeature  (CvPlot.cpp:8788)  <- call CvPlot::setFeatureType
- CvPlot::doImprovement  (CvPlot.cpp:630)  <- call CvPlot::doImprovementUpgrade
- CvPlot::setPlotType  (CvPlot.cpp:5292)  <- call CvPlot::erase
- ... 54 more

(levels above 3: 629 more)

## Python functions, level by level


### level 2 (6)

- canTriggerHolyMountainRevealed  (EntryPoints/CvRandomEventInterface.py:218)  <- py>cpp CyPlot::setRevealed
- Revolution.processRevolution  (Revolution/Gameready/Revolution.py:5015)  <- py>cpp CyPlot::setRevealed
- Revolution.spawnRevolutionaries  (Revolution/Gameready/Revolution.py:6243)  <- py>cpp CyPlot::setRevealed
- CvWorldBuilderScreen.RevealCurrentPlot  (base/Screens/CvWorldBuilderScreen.py:2314)  <- py>cpp (name match) CyCity::setRevealed
- CvWorldBuilderScreen.revealAll  (base/Screens/CvWorldBuilderScreen.py:2304)  <- py>cpp CyPlot::setRevealed
- CvWBDesc.applyInitialItems  (base/pyWB/CvWBDesc.py:1617)  <- py>cpp CyPlot::setRevealed

### level 3 (28)

- Deal.turnsToCancel  (BUG/DealUtil.py:202)  <- py>cpp (name match) CyDeal::turnsToCancel
- GoldPerTurnTrade.onBeginActivePlayerTurn  (Contrib/Civ4lerts.py:780)  <- py>cpp (only target) CyPlayer::AI_maxGoldPerTurnTrade
- applyEarthquake1  (EntryPoints/CvRandomEventInterface.py:6860)  <- py>cpp (only target) CyPlot::setImprovementType
- applyVolcano1  (EntryPoints/CvRandomEventInterface.py:790)  <- py>cpp (only target) CyPlot::setImprovementType
- doAntelope2  (EntryPoints/CvRandomEventInterface.py:1206)  <- py>cpp CyPlot::setImprovementType
- doImpactCrater2  (EntryPoints/CvRandomEventInterface.py:1782)  <- py>cpp CyPlot::setImprovementType
- doSpicy2  (EntryPoints/CvRandomEventInterface.py:410)  <- py>cpp CyPlot::setImprovementType
- doWiningMonks2  (EntryPoints/CvRandomEventInterface.py:1295)  <- py>cpp CyPlot::setImprovementType
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
- RoMEventManager.onCityLost  (RoMEventManager.py:508)  <- py>cpp (only target) CyPlot::setImprovementType
- CvExoticForeignAdvisor.drawActive  (Screens/CvExoticForeignAdvisor.py:380)  <- py>cpp CyDeal::turnsToCancel
- CvExoticForeignAdvisor.drawResourceDeals  (Screens/CvExoticForeignAdvisor.py:1145)  <- py>cpp CyPlayer::AI_maxGoldPerTurnTrade
- CvForeignAdvisor.drawPossibleDeals  (Screens/CvForeignAdvisor.py:269)  <- py>cpp CyPlayer::AI_maxGoldPerTurnTrade
- CvDebugTools.allImprovements  (base/CvDebugTools.py:267)  <- py>cpp CyPlot::setImprovementType
- CvWorldBuilderScreen.eraseAll  (base/Screens/CvWorldBuilderScreen.py:2448)  <- py>cpp (only target) CyPlot::setImprovementType
- CvWorldBuilderScreen.placeObject  (base/Screens/CvWorldBuilderScreen.py:714)  <- py>cpp (only target) CyPlot::setImprovementType
- CvWorldBuilderScreen.removeObject  (base/Screens/CvWorldBuilderScreen.py:931)  <- py>cpp (only target) CyPlot::setImprovementType
- CvWorldBuilderScreen.setMultipleReveal  (base/Screens/CvWorldBuilderScreen.py:1909)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.RevealCurrentPlot
- CvPlotDesc.apply  (base/pyWB/CvWBDesc.py:1118)  <- py>cpp CyPlot::setImprovementType

(levels above 3: 282 more)

## Reach per start node

| start | reached | C++ | Python | members |
|---|---|---|---|---|
| PEACE_TREATY_LENGTH | 1135 | 825 | 310 | 0 |
| CvGame::m_aiDeferredRevealPlots | 1036 | 778 | 258 | 0 |
| CvPlot::m_bRevealedGraphicsDirty | 1031 | 773 | 258 | 0 |
| CvGame::m_iBulkRevealDepth | 1030 | 772 | 258 | 0 |
| CvPlot::isRevealedGraphicsDirty | 1029 | 771 | 258 | 0 |
| CvGame::m_eBulkRevealTeam | 1027 | 769 | 258 | 0 |
| CvPlot::setRevealedGraphicsDirty | 1026 | 768 | 258 | 0 |
| CvGame::deferRevealedGraphics | 1025 | 767 | 258 | 0 |
| CvPlot::deferRevealedGraphics | 1024 | 766 | 258 | 0 |
| CvPlot::setRevealedRouteType | 1020 | 762 | 258 | 0 |
| CvCity::setRevealed | 1018 | 760 | 258 | 0 |
| CvPlot::setRevealedImprovementType | 1017 | 759 | 258 | 0 |
| CvPlot::setRevealed | 1016 | 758 | 258 | 0 |
| CvPlayerAI::AI_goldPerTurnTradeVal | 1009 | 757 | 252 | 0 |
| GRAPHICS_PAGING_LOG | 1008 | 756 | 252 | 0 |
| CvPlot::m_bRevealedRouteDirty | 1008 | 756 | 252 | 0 |
| GRAPHICS_PAGING_REVEAL_MAX | 1007 | 755 | 252 | 0 |
| CvPlot::refreshRevealedGraphics | 1007 | 755 | 252 | 0 |
| CvGame::processDeferredReveals | 1006 | 754 | 252 | 0 |
| CvGame::endBulkReveal | 1004 | 752 | 252 | 0 |
| CvGame::beginBulkReveal | 1004 | 752 | 252 | 0 |
| CvDeal::startTrade | 1003 | 751 | 252 | 0 |
| CvPlayerAI::AI_doDiplo | 113 | 60 | 53 | 0 |
| CvPlot::reset | 16 | 13 | 3 | 0 |
| CvGame::reset | 11 | 11 | 0 | 0 |
| CvPlot::setupGraphical | 8 | 6 | 2 | 0 |
| GRAPHICS_PAGING_MAX_OUT | 3 | 3 | 0 | 0 |
| CvGame::pageGraphics | 2 | 2 | 0 | 0 |
| CvGame::m_bPagingPendingOut | 2 | 2 | 0 | 0 |
| CvGame::m_bPagingPending | 2 | 2 | 0 | 0 |
| CvGame::updateGraphicsPaging | 1 | 1 | 0 | 0 |
| CvPlayerAI::AI_counterPropose | 0 | 0 | 0 | 0 |
