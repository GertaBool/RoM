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

- C++ functions the exe calls (exported): 101: CvCity::cheat, CvDLLButtonPopup::OnOkClicked, CvDLLButtonPopup::launchButtonPopup, CvDLLWidgetData::executeAction, CvDLLWidgetData::isLink, CvDLLWidgetData::parseHelp, CvDeal::isCancelable, CvDeal::kill, CvDeal::turnsToCancel, CvEventReporter::gameStart, CvEventReporter::kbdEvent, CvEventReporter::reportModNetMessage, CvGame::CvGame, CvGame::cheatSpaceship, CvGame::implementDeal, CvGame::init, CvGame::initDiplomacy, CvGame::initFreeState, CvGame::initFreeUnits, CvGame::nextActivePlayer, CvGame::normalizeStartingPlots, CvGame::read, CvGame::regenerateMap, CvGame::reset, CvGame::reviveActivePlayer, CvGame::revivePlayer, CvGame::setAIAutoPlay, CvGame::setInitialItems, CvGame::setVoteChosen, CvGame::update, CvGame::updateCitySight, CvGameTextMgr::getActiveDealsString, CvGameTextMgr::getBonusDataForWB, CvGameTextMgr::getDealString, CvGameTextMgr::getTechDataForWB, CvGameTextMgr::getTradeString, CvGameTextMgr::getTurnTimerText, CvGameTextMgr::parseLeaderHeadHelp, CvGameTextMgr::setBonusHelp, CvGameTextMgr::setBonusTradeHelp, CvGameTextMgr::setTechHelp, CvGameTextMgr::setTechTradeHelp, CvGlobals::init, CvMap::erasePlots, CvMap::init, CvMap::read, CvMap::setupGraphical, CvMapGenerator::addFeatures, CvMapGenerator::addGameElements, CvMapGenerator::addGoodies, CvMapGenerator::eraseFeatures, CvMapGenerator::eraseGoodies, CvMapGenerator::generateRandomMap, CvNetAdvancedStartAction::Execute, CvNetAutoMission::Execute, CvNetAutoMoves::Execute, CvNetChangeVassal::Execute, CvNetChangeWar::Execute, CvNetChooseElection::Execute, CvNetConvert::Execute, CvNetDoCommand::Execute, CvNetDoTask::Execute, CvNetEmpireSplit::Execute, CvNetEventTriggered::Execute, CvNetFoundReligion::Execute, CvNetModNetMessage::Execute, CvNetPopOrder::Execute, CvNetPushMission::Execute, CvNetPushOrder::Execute, CvNetResearch::Execute, CvNetTurnComplete::Execute, CvNetUpdateCivics::Execute, CvPlayer::applyEvent, CvPlayer::buildTradeTable, CvPlayer::canTradeItem, CvPlayer::cheat, CvPlayer::convert, CvPlayer::doAdvancedStartAction, CvPlayer::foundReligion, CvPlayer::getGlobeLayerColors, CvPlayer::getItemTradeString, CvPlayer::handleDiploEvent, CvPlayer::init, CvPlayer::revolution, CvPlayer::setAutoMoves, CvPlayer::setEndTurn, CvPlayer::setLoyalMember, CvPlayer::setTurnActive, CvPlayer::splitEmpire, CvPlayerAI::AI_maxGoldPerTurnTrade, CvPlot::erase, CvPlot::setFeatureType, CvPlot::setImprovementType, CvPlot::setRevealed, CvPlot::setRouteType, CvSelectionGroup::autoMission, CvSelectionGroup::pushMission, CvTeam::declareWar, CvTeam::init, CvTeam::makePeace, DLLPublishToPython
- C++ functions bound for Python: 143: CyCity::addProductionExperience, CyCity::changeCulture, CyCity::changeCultureTimes100, CyCity::changeOccupationTimer, CyCity::clearOrderQueue, CyCity::conscript, CyCity::createGreatPeople, CyCity::doTask, CyCity::kill, CyCity::liberate, CyCity::popOrder, CyCity::pushOrder, CyCity::setCulture, CyCity::setCultureTimes100, CyCity::setHasCorporation, CyCity::setNumRealBuilding, CyCity::setOccupationTimer, CyCity::setProductionAutomated, CyCity::setRevealed, CyDeal::getCannotCancelReason, CyDeal::isCancelable, CyDeal::kill, CyDeal::turnsToCancel, CyGame::addPlayer, CyGame::clearHeadquarters, CyGame::regenerateMap, CyGame::reviveActivePlayer, CyGame::setAIAutoPlay, CyGame::setHeadquarters, CyGame::setWinner, CyGameTextMgr::getActiveDealsString, CyGameTextMgr::getBonusHelp, CyGameTextMgr::getDealString, CyGameTextMgr::getTechHelp, CyGameTextMgr::getTradeString, CyMap::erasePlots, CyMap::rebuild, CyMap::recalculateAreas, CyMap::regenerateGameElements, CyMap::setAllPlotTypes, CyMap::setRevealedPlots, CyMap::verifyUnitValidPlot, CyMapGenerator::addFeatures, CyMapGenerator::addGameElements, CyMapGenerator::addGoodies, CyMapGenerator::addLakes, CyMapGenerator::eraseFeatures, CyMapGenerator::eraseGoodies, CyMapGenerator::generatePlotTypes, CyMapGenerator::generateRandomMap, CyMapGenerator::generateTerrain, CyMapGenerator::setPlotTypes, CyPlayer::AI_maxGoldPerTurnTrade, CyPlayer::acquireCity, CyPlayer::assimilatePlayer, CyPlayer::canStopTradingWithTeam, CyPlayer::canTradeItem, CyPlayer::changeCiv, CyPlayer::changeCombatExperience, CyPlayer::convert, CyPlayer::createGreatPeople, CyPlayer::disband, CyPlayer::disbandUnit, CyPlayer::doEspionageMission, CyPlayer::doGoody, CyPlayer::findNewCapital, CyPlayer::forcePeace, CyPlayer::found, CyPlayer::foundCorporation, CyPlayer::foundReligion, CyPlayer::initCity, CyPlayer::initTriggeredData, CyPlayer::initUnit, CyPlayer::killAllDeals, CyPlayer::killCities, CyPlayer::killUnits, CyPlayer::raze, CyPlayer::receiveGoody, CyPlayer::removeBuildingClass, CyPlayer::revolution, CyPlayer::setAlive, CyPlayer::setCivics, CyPlayer::setCombatExperience, CyPlayer::setLastStateReligion, CyPlayer::setLoyalMember, CyPlayer::setNewPlayerAlive, CyPlayer::splitEmpire, CyPlayer::stopTradingWithTeam, CyPlayer::trigger, CyPlot::changeBuildProgress, CyPlot::changeCulture, CyPlot::changeVisibilityCount, CyPlot::erase, CyPlot::nukeExplosion, CyPlot::removeGoody, CyPlot::setCulture, CyPlot::setFeatureType, CyPlot::setImprovementType, CyPlot::setOwner, CyPlot::setOwnerNoUnitCheck, CyPlot::setPlotType, CyPlot::setRevealed, CyPlot::setRouteType, CyPlot::setTerrainType, CySelectionGroup::popMission, CySelectionGroup::pushMission, CySelectionGroup::pushMoveToMission, CyTeam::addTeam, CyTeam::assignVassal, CyTeam::changeEspionagePointsAgainstTeam, CyTeam::changeExtraWaterSeeFromCount, CyTeam::changeProjectCount, CyTeam::changeResearchProgress, CyTeam::changeTechShareCount, CyTeam::declareWar, CyTeam::freeVassal, CyTeam::makePeace, CyTeam::meet, CyTeam::setEspionagePointsAgainstTeam, CyTeam::setHasTech, CyTeam::setIsMinorCiv, CyTeam::setResearchProgress, CyTeam::setVassal, CyTeam::signDefensivePact, CyTeam::signOpenBorders, CyUnit::attackForDamage, CyUnit::changeDamage, CyUnit::changeExperience, CyUnit::convert, CyUnit::doCommand, CyUnit::gift, CyUnit::giveExperience, CyUnit::jumpToNearestValidPlot, CyUnit::kill, CyUnit::lead, CyUnit::promote, CyUnit::rangeStrike, CyUnit::rotateFacingDirectionClockwise, CyUnit::rotateFacingDirectionCounterClockwise, CyUnit::setDamage, CyUnit::setHasPromotion, CyUnit::setReconPlot, CyUnit::setXY
- Python event handlers: 35: AIAutoPlay.onBeginGameTurn (BeginGameTurn), AIAutoPlay.onGameStart (GameStart), AIAutoPlay.onKbdEvent (kbdEvent), AIAutoPlay.onModNetMessage (ModNetMessage), AIAutoPlay.onVictory (victory), BarbarianCiv.onBeginGameTurn (BeginGameTurn), BarbarianCiv.onCityAcquired (cityAcquired), BarbarianCiv.onEndPlayerTurn (EndPlayerTurn), ChangePlayer.onKbdEvent (kbdEvent), CvEnhancedTechConquestEventManager.onCityAcquired (cityAcquired), CvEventManager.onCityRazed (cityRazed), CvEventManager.onKbdEvent (kbdEvent), MoreCiv4lertsEvent.OnCityAcquired (cityAcquired), MoreCiv4lertsEvent.OnCityBuilt (cityBuilt), MoreCiv4lertsEvent.OnCityLost (cityLost), MoreCiv4lertsEvent.OnCityRazed (cityRazed), Revolution.onBeginPlayerTurn (BeginPlayerTurn), Revolution.onEndPlayerTurn (EndPlayerTurn), Revolution.onModNetMessage (ModNetMessage), RevolutionInit.onGameStart (GameStart), RoMEventManager.onBeginPlayerTurn (BeginPlayerTurn), RoMEventManager.onBuildingBuilt (buildingBuilt), RoMEventManager.onCityLost (cityLost), RoMEventManager.onModNetMessage (ModNetMessage), RoMEventManager.onProjectBuilt (projectBuilt), TechDiffusion.onBeginGameTurn (BeginGameTurn), Tester.onBeginPlayerTurn (BeginPlayerTurn), onBeginPlayerTurn (BeginPlayerTurn), onChangeWar (changeWar), onCityAcquired (cityAcquired), onEndGameTurn (EndGameTurn), onEndPlayerTurn (EndPlayerTurn), onSetPlayerAlive (setPlayerAlive), onSetPlayerAlive (setPlayerAlive), onTechAcquired (techAcquired)
- C++ files: CvUnitAI.cpp 165, CvUnit.cpp 80, CvPlayer.cpp 75, CvGame.cpp 65, CvCity.cpp 39, CvPlot.cpp 39, CvTeam.cpp 37, CyPlayer.cpp 37, CvPlayerAI.cpp 33, CvSelectionGroup.cpp 21, CyCity.cpp 19, CvMessageData.cpp 19, CyTeam.cpp 18, CyUnit.cpp 18, CvDLLWidgetData.cpp 17, CvDllPythonEvents.cpp 17, CvEventReporter.cpp 17, CyPlot.cpp 15, CvMap.cpp 13, CvGameTextMgr.cpp 13, CvCityAI.cpp 13, CvDeal.cpp 10, CvMapGenerator.cpp 10, CyMapGenerator.cpp 10, CyMap.cpp 7, CyGame.cpp 7, CvSelectionGroupAI.cpp 6, CyGameTextMgr.cpp 5, CyDeal.cpp 4, CvTeamAI.cpp 4, CvDLLButtonPopup.cpp 3, CySelectionGroup.cpp 3, CvPlot.h 2, CvGameAI.cpp 2, FFreeListTrashArray.h 2, CvGameInterface.cpp 2, CyCityInterface1.cpp 1, CyPlotInterface1.cpp 1, CvDLLPython.cpp 1, CvGlobals.cpp 1, CyMapInterface.cpp 1, CyPlayerInterface2.cpp 1, CyPlayerInterface1.cpp 1, CyTeamInterface.cpp 1, CyGameInterface.cpp 1, CyGameTextMgrInterface.cpp 1, CyUnitInterface1.cpp 1, CyMapGeneratorInterface.cpp 1, CvArea.cpp 1, CySelectionGroupInterface.cpp 1, CvGameCoreUtils.cpp 1
- Python modules: EntryPoints/CvRandomEventInterface.py 60, base/Screens/CvWorldBuilderScreen.py 23, EntryPoints/CvScreensInterface.py 19, Revolution/Gameready/Revolution.py 17, Contrib/MoreCiv4lerts.py 15, Revolution/Gameready/AIAutoPlay.py 14, Revolution/RevEvents.py 11, Revolution/Gameready/BarbarianCiv.py 11, PyHelpers.py 7, Revolution/RevUtils.py 7, Screens/PLE.py 7, base/pyWB/CvWBDesc.py 6, RoMEventManager.py 6, Screens/CvForeignAdvisor.py 6, base/CvEventManager.py 6, Screens/CvMainInterface.py 6, base/CvDebugTools.py 5, Screens/CvExoticForeignAdvisor.py 5, ModTools/ModTools.py 5, base/CvPerfTest.py 5, CvMapGeneratorUtil.py 5, Contrib/RevDCMReligionControl.py 5, Screens/CvPediaMain.py 5, BUG/DealUtil.py 4, Revolution/Development/ChangePlayer.py 4, BUG/PlayerUtil.py 4, EntryPoints/CvWBInterface.py 3, base/Screens/CvWorldBuilderDiplomacyScreen.py 3, Revolution/Gameready/StartAsMinors.py 3, CvUtil.py 3, Revolution/RevolutionInit.py 3, Screens/CvBUGMilitaryAdvisor.py 3, Contrib/MapFinder.py 2, Revolution/Gameready/TechDiffusion.py 2, Revolution/Development/Tester.py 2, BUG/TradeUtil.py 2, Contrib/FavoriteCivicDetector.py 2, Contrib/Sevopedia/SevoPediaBonus.py 2, base/Screens/CvPediaBonus.py 2, Contrib/Sevopedia/SevoPediaTech.py 2, base/Screens/CvPediaTech.py 2, Contrib/Civ4lerts.py 1, ModTools/ModToolsUtils.py 1, base/EntryPoints/CvGameInterface.py 1, AbandonCityEventManager.py 1, BUG/Scoreboard.py 1, EnhancedTechConquestUtils/EnhancedTechConquest.py 1, EnhancedTechConquestUtils/CvEnhancedTechConquestEventManager.py 1, Contrib/MonkeyTools.py 1, base/pyWB/CvWBPopups.py 1, Contrib/TechWindow.py 1, Contrib/TechWindowWide.py 1, base/Screens/CvTechSplashScreen.py 1

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
- CvUnit::airBomb1  (CvUnit.cpp:14533)  <- call CvPlot::setImprovementType
- CvUnit::bombardRanged  (CvUnit.cpp:15531)  <- call CvPlot::setImprovementType
- CvUnit::pillage  (CvUnit.cpp:5400)  <- call CvPlot::setImprovementType
- CvUnit::sabotage  (CvUnit.cpp:5803)  <- call CvPlot::setImprovementType
- CvUnit::setXY  (CvUnit.cpp:10566)  <- call CvPlayer::acquireCity
- CyCityPythonInterface1  (CyCityInterface1.cpp:15)  <- call CyCity::setRevealed
- CyDeal::turnsToCancel  (CyDeal.cpp:125)  <- call CvDeal::turnsToCancel
- CyGameTextMgr::getTradeString  (CyGameTextMgr.cpp:198)  <- call CvGameTextMgr::getTradeString
- CyMap::setRevealedPlots  (CyMap.cpp:34)  <- call CvMap::setRevealedPlots
- CyPlayer::AI_maxGoldPerTurnTrade  (CyPlayer.cpp:2473)  <- call CvPlayerAI::AI_maxGoldPerTurnTrade
- CyPlayer::acquireCity  (CyPlayer.cpp:153)  <- call CvPlayer::acquireCity
- CyPlayer::assimilatePlayer  (CyPlayer.cpp:2518)  <- call CvPlayer::assimilatePlayer
- CyPlayer::receiveGoody  (CyPlayer.cpp:496)  <- call CvPlayer::receiveGoody
- CyPlayer::splitEmpire  (CyPlayer.cpp:2483)  <- call CvPlayer::splitEmpire
- CyPlot::changeVisibilityCount  (CyPlot.cpp:936)  <- call CvPlot::changeVisibilityCount
- CyPlot::setImprovementType  (CyPlot.cpp:776)  <- call CvPlot::setImprovementType
- CyPlot::setRouteType  (CyPlot.cpp:787)  <- call CvPlot::setRouteType
- CyPlotPythonInterface1  (CyPlotInterface1.cpp:15)  <- call CyPlot::setRevealed
- CyTeam::addTeam  (CyTeam.cpp:48)  <- call CvTeam::addTeam
- ReadStreamableFFreeListTrashArray<class CvArea>  (FFreeListTrashArray.h:485)  <- call CvGame::read
- ReadStreamableFFreeListTrashArray<class CvSelectionGroupAI>  (FFreeListTrashArray.h:485)  <- call CvGame::read

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
- CvPlot::updateCulture  (CvPlot.cpp:713)  <- call CvPlot::setOwner
- CvPlot::updateSight  (CvPlot.cpp:2092)  <- call CvPlot::changeAdjacentSight
- CvSelectionGroup::groupAttack  (CvSelectionGroup.cpp:4392)  <- call CvUnit::bombardRanged
- CvSelectionGroup::groupStackAttack  (CvSelectionGroup.cpp:6368)  <- call CvUnit::bombardRanged
- CvSelectionGroup::setRemoteTransportUnit  (CvSelectionGroup.cpp:5064)  <- call CvUnit::setXY
- CvSelectionGroup::startMission  (CvSelectionGroup.cpp:1372)  <- call CvUnit::airBomb1
- CvTeam::assignVassal  (CvTeam.cpp:5125)  <- call CvGame::implementDeal
- CvTeam::changeStolenVisibilityTimer  (CvTeam.cpp:4302)  <- call CvTeam::setStolenVisibilityTimer
- CvTeam::processTech  (CvTeam.cpp:6792)  <- call CvPlot::updateCityRoute
- CvTeam::setResearchProgress  (CvTeam.cpp:5595)  <- call CvTeam::setHasTech
- CvTeam::setTurnActive  (CvTeam.cpp:7295)  <- call CvPlayer::setTurnActive
- CvTeam::shareCounters  (CvTeam.cpp:897)  <- call CvTeam::setStolenVisibilityTimer
- CvTeam::shareItems  (CvTeam.cpp:820)  <- call CvTeam::setHasTech
- CvTeam::signDefensivePact  (CvTeam.cpp:2276)  <- call CvGame::implementDeal
- CvTeam::signOpenBorders  (CvTeam.cpp:2249)  <- call CvGame::implementDeal
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
- CyCity::kill  (CyCity.cpp:24)  <- call CvCity::kill
- CyCity::liberate  (CyCity.cpp:2814)  <- call CvCity::liberate
- CyDeal::getCannotCancelReason  (CyDeal.cpp:115)  <- call CvDeal::isCancelable
- CyDeal::isCancelable  (CyDeal.cpp:100)  <- call CvDeal::isCancelable
- CyGame::regenerateMap  (CyGame.cpp:1285)  <- call CvGame::regenerateMap
- CyGamePythonInterface  (CyGameInterface.cpp:13)  <- call CyDeal::turnsToCancel
- CyGameTextMgrInterface  (CyGameTextMgrInterface.cpp:9)  <- call CyGameTextMgr::getTradeString
- CyMapGenerator::addGoodies  (CyMapGenerator.cpp:87)  <- call CvMapGenerator::addGoodies
- CyMapPythonInterface  (CyMapInterface.cpp:17)  <- call CyMap::setRevealedPlots
- CyPlayer::doEspionageMission  (CyPlayer.cpp:1031)  <- call CvPlayer::doEspionageMission
- CyPlayer::doGoody  (CyPlayer.cpp:502)  <- call CvPlayer::doGoody
- CyPlayer::initCity  (CyPlayer.cpp:148)  <- call CvPlayer::initCity
- CyPlayerPythonInterface1  (CyPlayerInterface1.cpp:17)  <- call CyPlayer::acquireCity
- CyPlayerPythonInterface2  (CyPlayerInterface2.cpp:17)  <- call CyPlayer::splitEmpire
- CyPlot::changeBuildProgress  (CyPlot.cpp:988)  <- call CvPlot::changeBuildProgress
- CyPlot::erase  (CyPlot.cpp:23)  <- call CvPlot::erase
- CyPlot::nukeExplosion  (CyPlot.cpp:39)  <- call CvPlot::nukeExplosion
- CyPlot::removeGoody  (CyPlot.cpp:309)  <- call CvPlot::removeGoody
- CyPlot::setFeatureType  (CyPlot.cpp:673)  <- call CvPlot::setFeatureType
- CyPlot::setOwner  (CyPlot.cpp:615)  <- call CvPlot::setOwner
- CyPlot::setOwnerNoUnitCheck  (CyPlot.cpp:621)  <- call CvPlot::setOwner
- CyTeam::setHasTech  (CyTeam.cpp:873)  <- call CvTeam::setHasTech
- CyTeamPythonInterface  (CyTeamInterface.cpp:10)  <- call CyTeam::addTeam
- CyUnit::setXY  (CyUnit.cpp:1192)  <- call CvUnit::setXY
- DLLPublishToPython  (CvDLLPython.cpp:50)  <- call CyCityPythonInterface1

### level 4 (124)

- CvCity::doTurn  (CvCity.cpp:1208)  <- call CvCity::doMeltdown
- CvCity::popOrder  (CvCity.cpp:12926)  <- call CvUnit::jumpToNearestValidPlot
- CvCity::setEspionageVisibility  (CvCity.cpp:10918)  <- call CvPlot::updateSight
- CvCity::setNumRealBuildingTimed  (CvCity.cpp:12064)  <- call CvPlayerAI::AI_chooseFreeTech
- CvDLLWidgetData::executeAction  (CvDLLWidgetData.cpp:657)  <- call CvDLLWidgetData::doDealKill
- CvDeal::kill  (CvDeal.cpp:78)  <- call CvGameTextMgr::getDealString
- CvDllPythonEvents::reportCityLost  (CvDllPythonEvents.cpp:534)  <- event RoMEventManager.py RoMEventManager.onCityLost
- CvGame::clearSecretaryGeneral  (CvGame.cpp:3617)  <- call CvGame::setVoteOutcome
- CvGame::createBarbarianCities  (CvGame.cpp:7285)  <- call CvPlayer::found
- CvGame::createBarbarianUnits  (CvGame.cpp:7523)  <- call CvUnit::kill
- CvGame::doVoteResults  (CvGame.cpp:10191)  <- call CvGame::setVoteOutcome
- CvGame::foundBarbarianCity  (CvGame.cpp:10632)  <- call CvPlayer::found
- CvGame::normalizeAddLakes  (CvGame.cpp:1298)  <- call CvPlot::setPlotType
- CvGame::normalizeRemovePeaks  (CvGame.cpp:1260)  <- call CvPlot::setPlotType
- CvGame::normalizeStartingPlots  (CvGame.cpp:2048)  <- call CvGame::normalizeAddRiver
- CvGame::replaceCorporation  (CvGame.cpp:3851)  <- call CvUnit::kill
- CvGame::setAIAutoPlay  (CvGame.cpp:4717)  <- call CvPlayer::setAutoMoves
- CvGame::updateMoves  (CvGame.cpp:7908)  <- call CvPlayer::setAutoMoves
- CvGame::verifyDeals  (CvGame.cpp:3307)  <- call CvDeal::verify
- CvGameTextMgr::getActiveDealsString  (CvGameTextMgr.cpp:16556)  <- call CvGameTextMgr::getDealString
- CvMap::setAllPlotTypes  (CvMap.cpp:306)  <- call CvPlot::setPlotType
- CvMap::updateSight  (CvMap.cpp:418)  <- call CvPlot::updateSight
- CvMapGenerator::addLakes  (CvMapGenerator.cpp:262)  <- call CvPlot::setPlotType
- CvMapGenerator::setPlotTypes  (CvMapGenerator.cpp:1078)  <- call CvPlot::setPlotType
- CvNetAutoMoves::Execute  (CvMessageData.cpp:125)  <- call CvPlayer::setAutoMoves
- CvPlayer::canStopTradingWithTeam  (CvPlayer.cpp:5937)  <- call CvPlayer::isTradingWithTeam
- CvPlayer::disbandUnit  (CvPlayer.cpp:3124)  <- call CvUnit::kill
- CvPlayer::doTurnUnits  (CvPlayer.cpp:4068)  <- call CvPlayerAI::AI_doTurnUnitsPost
- CvPlayer::handleDiploEvent  (CvPlayer.cpp:5137)  <- call CvPlayer::forcePeace
- CvPlayer::init  (CvPlayer.cpp:191)  <- call CvPlayer::setAlive
- CvPlayer::initTriggeredData  (CvPlayer.cpp:19815)  <- call CvPlayer::trigger
- CvPlayer::initUnit  (CvPlayer.cpp:3107)  <- call CvUnit::init
- CvPlayer::killGoldenAgeUnits  (CvPlayer.cpp:9580)  <- call CvUnit::kill
- CvPlayer::killUnits  (CvPlayer.cpp:3282)  <- call CvUnit::kill
- CvPlayer::raze  (CvPlayer.cpp:6151)  <- call CvPlayer::disband
- CvPlayer::setEndTurn  (CvPlayer.cpp:12511)  <- call CvPlayer::setAutoMoves
- CvPlayer::updateCitySight  (CvPlayer.cpp:4358)  <- call CvPlot::updateSight
- CvPlayer::verifyAlive  (CvPlayer.cpp:12013)  <- call CvPlayer::setAlive
- CvPlayerAI::AI_disbandUnit  (CvPlayerAI.cpp:20329)  <- call CvUnit::kill
- CvPlayerAI::read  (CvPlayerAI.cpp:19188)  <- call CvPlayer::read
- CvPlot::changeCultureRangeCities  (CvPlot.cpp:8513)  <- call CvPlot::updateCulture
- CvPlot::doTurn  (CvPlot.cpp:577)  <- call CvPlot::doCulture
- CvPlot::setCulture  (CvPlot.cpp:6783)  <- call CvPlot::updateCulture
- CvPlot::setTerrainType  (CvPlot.cpp:5542)  <- call CvPlot::setPlotType
- CvPlot::updateSeeFromSight  (CvPlot.cpp:2177)  <- call CvPlot::updateSight
- CvPlot::verifyUnitValidPlot  (CvPlot.cpp:962)  <- call CvUnit::jumpToNearestValidPlot
- CvSelectionGroup::activateHeadMission  (CvSelectionGroup.cpp:6327)  <- call CvSelectionGroup::startMission
- CvSelectionGroup::autoMission  (CvSelectionGroup.cpp:718)  <- call CvSelectionGroup::startMission
- CvSelectionGroup::continueMission  (CvSelectionGroup.cpp:2043)  <- call CvSelectionGroup::setRemoteTransportUnit
- CvSelectionGroup::groupBuild  (CvSelectionGroup.cpp:4863)  <- call CvUnit::build
- CvSelectionGroup::groupMove  (CvSelectionGroup.cpp:4697)  <- call CvUnit::move
- CvSelectionGroupAI::AI_update  (CvSelectionGroupAI.cpp:184)  <- call CvSelectionGroup::groupAttack
- CvTeam::changeResearchProgress  (CvTeam.cpp:5627)  <- call CvTeam::setResearchProgress
- CvTeam::doTurn  (CvTeam.cpp:1050)  <- call CvTeam::changeStolenVisibilityTimer
- CvTeam::setVassal  (CvTeam.cpp:4814)  <- call CvPlot::updateCulture
- CvTeam::updateTechShare  (CvTeam.cpp:6682)  <- call CvTeam::updateTechShare
- CvTeam::verifySpyUnitsValidPlot  (CvTeam.cpp:7162)  <- call CvUnit::jumpToNearestValidPlot
- CvTeamAI::AI_doWar  (CvTeamAI.cpp:4754)  <- call CvPlayerAI::AI_doPeace
- CvUnit::airBomb2  (CvUnit.cpp:14684)  <- call CvUnit::kill
- CvUnit::airBomb3  (CvUnit.cpp:14887)  <- call CvUnit::kill
- CvUnit::airBomb4  (CvUnit.cpp:15128)  <- call CvUnit::kill
- CvUnit::airBomb5  (CvUnit.cpp:15315)  <- call CvUnit::kill
- CvUnit::airStrike  (CvUnit.cpp:13455)  <- call CvUnit::setReconPlot
- CvUnit::applyEvent  (CvUnit.cpp:14174)  <- call CvUnit::kill
- CvUnit::attackForDamage  (CvUnit.cpp:3053)  <- call CvUnit::setFacingDirection
- CvUnit::construct  (CvUnit.cpp:6681)  <- call CvUnit::kill
- CvUnit::convert  (CvUnit.cpp:513)  <- call CvUnit::jumpToNearestValidPlot
- CvUnit::destroy  (CvUnit.cpp:5996)  <- call CvUnit::kill
- CvUnit::discover  (CvUnit.cpp:6760)  <- call CvUnit::kill
- CvUnit::doDelayedDeath  (CvUnit.cpp:12044)  <- call CvUnit::kill
- CvUnit::doTurn  (CvUnit.cpp:798)  <- call CvUnit::testSpyIntercepted
- CvUnit::flankingStrikeCombat  (CvUnit.cpp:13272)  <- call CvUnit::kill
- CvUnit::found  (CvUnit.cpp:6229)  <- call CvPlayer::found
- CvUnit::goldenAge  (CvUnit.cpp:7595)  <- call CvUnit::kill
- CvUnit::greatWork  (CvUnit.cpp:7006)  <- call CvUnit::kill
- CvUnit::hurry  (CvUnit.cpp:6857)  <- call CvUnit::kill
- CvUnit::infiltrate  (CvUnit.cpp:7093)  <- call CvUnit::kill
- CvUnit::join  (CvUnit.cpp:6605)  <- call CvUnit::kill
- CvUnit::lead  (CvUnit.cpp:7783)  <- call CvUnit::kill
- CvUnit::nuke  (CvUnit.cpp:4336)  <- call CvUnit::kill
- CvUnit::performInquisition  (CvUnit.cpp:17101)  <- call CvUnit::kill
- CvUnit::recon  (CvUnit.cpp:4605)  <- call CvUnit::setReconPlot
- CvUnit::rotateFacingDirectionClockwise  (CvUnit.cpp:11932)  <- call CvUnit::setFacingDirection
- CvUnit::rotateFacingDirectionCounterClockwise  (CvUnit.cpp:11939)  <- call CvUnit::setFacingDirection
- CvUnit::scrap  (CvUnit.cpp:3417)  <- call CvUnit::kill
- CvUnit::setDamage  (CvUnit.cpp:11136)  <- call CvUnit::kill
- CvUnit::setHasPromotion  (CvUnit.cpp:12725)  <- call CvUnit::changeExtraVisibilityRange
- CvUnit::spread  (CvUnit.cpp:6354)  <- call CvUnit::kill
- CvUnit::spreadCorporation  (CvUnit.cpp:6519)  <- call CvUnit::kill
- CvUnit::stealPlans  (CvUnit.cpp:6153)  <- call CvUnit::kill
- CvUnit::trade  (CvUnit.cpp:6944)  <- call CvUnit::kill
- CvUnit::updateAirCombat  (CvUnit.cpp:1078)  <- call CvUnit::kill
- CvUnit::updateAirStrike  (CvUnit.cpp:871)  <- call CvUnit::kill
- CvUnit::updateCombat  (CvUnit.cpp:1395)  <- call CvUnit::kill
- CvUnit::updateStackCombat  (CvUnit.cpp:15838)  <- call CvUnit::kill
- CvUnit::verifyStackValid  (CvUnit.cpp:14303)  <- call CvUnit::jumpToNearestValidPlot
- CvUnitAI::AI_espionageSpy  (CvUnitAI.cpp:23164)  <- call CvUnit::espionage
- CvUnitAI::AI_revoltCitySpy  (CvUnitAI.cpp:22910)  <- call CvUnit::espionage
- CyGame::addPlayer  (CyGame.cpp:1166)  <- call CvGame::addPlayer
- CyGameTextMgr::getDealString  (CyGameTextMgr.cpp:257)  <- call CvGameTextMgr::getDealString
- CyMap::erasePlots  (CyMap.cpp:28)  <- call CvMap::erasePlots
- CyMap::rebuild  (CyMap.cpp:289)  <- call CvMap::rebuild
- CyMap::regenerateGameElements  (CyMap.cpp:297)  <- call CvMapGenerator::addGameElements
- CyMapGenerator::addFeatures  (CyMapGenerator.cpp:63)  <- call CvMapGenerator::addFeatures
- CyMapGenerator::addGameElements  (CyMapGenerator.cpp:39)  <- call CvMapGenerator::addGameElements
- CyMapGenerator::eraseFeatures  (CyMapGenerator.cpp:99)  <- call CvMapGenerator::eraseFeatures
- CyMapGenerator::eraseGoodies  (CyMapGenerator.cpp:111)  <- call CvMapGenerator::eraseGoodies
- CyMapGeneratorPythonInterface  (CyMapGeneratorInterface.cpp:12)  <- call CyMapGenerator::addGoodies
- CyPlayer::disband  (CyPlayer.cpp:485)  <- call CvPlayer::disband
- CyPlayer::forcePeace  (CyPlayer.cpp:2536)  <- call CvPlayer::forcePeace
- CyPlayer::found  (CyPlayer.cpp:513)  <- call CvPlayer::found
- CyPlayer::killCities  (CyPlayer.cpp:159)  <- call CvPlayer::killCities
- CyPlayer::setAlive  (CyPlayer.cpp:1651)  <- call CvPlayer::setAlive
- CyPlayer::setNewPlayerAlive  (CyPlayer.cpp:1658)  <- call CvPlayer::setNewPlayerAlive
- CyPlayer::stopTradingWithTeam  (CyPlayer.cpp:446)  <- call CvPlayer::stopTradingWithTeam
- CyPlot::setPlotType  (CyPlot.cpp:651)  <- call CvPlot::setPlotType
- CyTeam::assignVassal  (CyTeam.cpp:714)  <- call CvTeam::assignVassal
- CyTeam::setResearchProgress  (CyTeam.cpp:833)  <- call CvTeam::setResearchProgress
- CyTeam::signDefensivePact  (CyTeam.cpp:93)  <- call CvTeam::signDefensivePact
- CyTeam::signOpenBorders  (CyTeam.cpp:87)  <- call CvTeam::signOpenBorders
- CyUnit::jumpToNearestValidPlot  (CyUnit.cpp:113)  <- call CvUnit::jumpToNearestValidPlot
- CyUnit::kill  (CyUnit.cpp:35)  <- call CvUnit::kill
- CyUnit::setReconPlot  (CyUnit.cpp:1223)  <- call CvUnit::setReconPlot
- CyUnitPythonInterface1  (CyUnitInterface1.cpp:18)  <- call CyUnit::setXY

### level 5 (129)

- CvCity::addProductionExperience  (CvCity.cpp:2957)  <- call CvUnit::setHasPromotion
- CvCity::cheat  (CvCity.cpp:16201)  <- call CvCity::popOrder
- CvCity::clearOrderQueue  (CvCity.cpp:12738)  <- call CvCity::popOrder
- CvCity::doCheckProduction  (CvCity.cpp:13628)  <- call CvCity::popOrder
- CvCity::doProduction  (CvCity.cpp:13767)  <- call CvCity::popOrder
- CvCity::emergencyConscript  (CvCity.cpp:16258)  <- call CvPlayer::initUnit
- CvCity::initConscriptedUnit  (CvCity.cpp:4188)  <- call CvPlayer::initUnit
- CvCity::pushOrder  (CvCity.cpp:12752)  <- call CvCity::popOrder
- CvCity::setCultureLevel  (CvCity.cpp:8853)  <- call CvPlot::changeCultureRangeCities
- CvCity::setHasCorporation  (CvCity.cpp:12481)  <- call CvGame::replaceCorporation
- CvCity::setHeadquarters  (CvCity.cpp:4763)  <- call CvPlayer::initUnit
- CvCity::setNumRealBuilding  (CvCity.cpp:12058)  <- call CvCity::setNumRealBuildingTimed
- CvCity::updateEspionageVisibility  (CvCity.cpp:10933)  <- call CvCity::setEspionageVisibility
- CvDLLButtonPopup::launchRazeCityPopup  (CvDLLButtonPopup.cpp:1400)  <- call CvPlayer::raze
- CvDLLWidgetData::parseContactCivHelp  (CvDLLWidgetData.cpp:3484)  <- call CvGameTextMgr::getActiveDealsString
- CvDLLWidgetData::parseTradeRoutes  (CvDLLWidgetData.cpp:6057)  <- call CvGameTextMgr::getActiveDealsString
- CvDeal::endTeamTrade  (CvDeal.cpp:1232)  <- call CvDeal::kill
- CvDeal::endTrade  (CvDeal.cpp:1098)  <- call CvTeam::setVassal
- CvDllPythonEvents::reportBuildingBuilt  (CvDllPythonEvents.cpp:1058)  <- event RoMEventManager.py RoMEventManager.onBuildingBuilt
- CvDllPythonEvents::reportEndGameTurn  (CvDllPythonEvents.cpp:167)  <- event Revolution/RevEvents.py onEndGameTurn
- CvDllPythonEvents::reportEndPlayerTurn  (CvDllPythonEvents.cpp:208)  <- event Revolution/Gameready/Revolution.py Revolution.onEndPlayerTurn
- CvDllPythonEvents::reportModNetMessage  (CvDllPythonEvents.cpp:75)  <- event Revolution/Gameready/Revolution.py Revolution.onModNetMessage
- CvDllPythonEvents::reportProjectBuilt  (CvDllPythonEvents.cpp:1076)  <- event RoMEventManager.py RoMEventManager.onProjectBuilt
- CvEventReporter::cityLost  (CvEventReporter.cpp:229)  <- call CvDllPythonEvents::reportCityLost
- CvGame::changeAIAutoPlay  (CvGame.cpp:4767)  <- call CvGame::setAIAutoPlay
- CvGame::createAnimals  (CvGame.cpp:7790)  <- call CvPlayer::initUnit
- CvGame::doDiploVote  (CvGame.cpp:7277)  <- call CvGame::doVoteResults
- CvGame::isValidVoteSelection  (CvGame.cpp:4915)  <- call CvPlayer::canStopTradingWithTeam
- CvGame::normalizeRemoveBadTerrain  (CvGame.cpp:1447)  <- call CvPlot::setTerrainType
- CvGame::reviveActivePlayer  (CvGame.cpp:4100)  <- call CvPlayer::initUnit
- CvGame::revivePlayer  (CvGame.cpp:4077)  <- call CvPlayer::initUnit
- CvGame::testAlive  (CvGame.cpp:8024)  <- call CvPlayer::verifyAlive
- CvGame::updateCitySight  (CvGame.cpp:3022)  <- call CvPlayer::updateCitySight
- CvGame::updateSecretaryGeneral  (CvGame.cpp:3640)  <- call CvGame::clearSecretaryGeneral
- CvGame::updateTurnTimer  (CvGame.cpp:7994)  <- call CvPlayer::setEndTurn
- CvGameTextMgr::parseLeaderHeadHelp  (CvGameTextMgr.cpp:16428)  <- call CvGameTextMgr::getActiveDealsString
- CvGameTextMgr::parseLeaderHeadRelationsHelp  (CvGameTextMgr.cpp:16470)  <- call CvGameTextMgr::getActiveDealsString
- CvMap::doTurn  (CvMap.cpp:330)  <- call CvPlot::doTurn
- CvMap::verifyUnitValidPlot  (CvMap.cpp:527)  <- call CvPlot::verifyUnitValidPlot
- CvMapGenerator::generatePlotTypes  (CvMapGenerator.cpp:1022)  <- call CvMapGenerator::setPlotTypes
- CvMapGenerator::generateTerrain  (CvMapGenerator.cpp:1051)  <- call CvPlot::setTerrainType
- CvNetAutoMission::Execute  (CvMessageData.cpp:821)  <- call CvSelectionGroup::autoMission
- CvNetChangeVassal::Execute  (CvMessageData.cpp:975)  <- call CvTeam::setVassal
- CvNetPopOrder::Execute  (CvMessageData.cpp:238)  <- call CvCity::popOrder
- CvNetTurnComplete::Execute  (CvMessageData.cpp:153)  <- call CvPlayer::setEndTurn
- CvPlayer::addFreeUnit  (CvPlayer.cpp:2004)  <- call CvPlayer::initUnit
- CvPlayer::canDoResolution  (CvPlayer.cpp:23131)  <- call CvPlayer::canStopTradingWithTeam
- CvPlayer::canTradeItem  (CvPlayer.cpp:5413)  <- call CvPlayer::canStopTradingWithTeam
- CvPlayer::createGreatPeople  (CvPlayer.cpp:19505)  <- call CvPlayer::initUnit
- CvPlayer::doGold  (CvPlayer.cpp:15287)  <- call CvPlayer::disbandUnit
- CvPlayer::doResearch  (CvPlayer.cpp:15358)  <- call CvTeam::changeResearchProgress
- CvPlayer::foundReligion  (CvPlayer.cpp:9205)  <- call CvPlayer::initUnit
- CvPlayer::killAllDeals  (CvPlayer.cpp:5997)  <- call CvDeal::kill
- CvPlayer::resetPlotAndCityData  (CvPlayer.cpp:704)  <- call CvPlot::setCulture
- CvPlayer::trigger  (CvPlayer.cpp:21800)  <- call CvPlayer::initTriggeredData
- CvPlayer::verifyUnitStacksValid  (CvPlayer.cpp:23706)  <- call CvUnit::verifyStackValid
- CvPlayerAI::AI_beginDiplomacy  (CvPlayerAI.cpp:17177)  <- call CvPlayer::handleDiploEvent
- CvPlayerAI::AI_diploVote  (CvPlayerAI.cpp:8037)  <- call CvPlayer::canStopTradingWithTeam
- CvPlayerAI::AI_doMilitary  (CvPlayerAI.cpp:16492)  <- call CvPlayerAI::AI_disbandUnit
- CvPlayerAI::AI_unitUpdate  (CvPlayerAI.cpp:1572)  <- call CvSelectionGroupAI::AI_update
- CvPlayerAI::AI_updateMilitaryOperations  (CvPlayerAI.cpp:15963)  <- call CvPlayer::initUnit
- CvPlot::changeCulture  (CvPlot.cpp:6821)  <- call CvPlot::setCulture
- CvSelectionGroup::deleteMissionQueueNode  (CvSelectionGroup.cpp:6161)  <- call CvSelectionGroup::activateHeadMission
- CvSelectionGroup::doDelayedDeath  (CvSelectionGroup.cpp:582)  <- call CvUnit::doDelayedDeath
- CvSelectionGroup::doTurn  (CvSelectionGroup.cpp:298)  <- call CvUnit::doTurn
- CvSelectionGroup::groupPathTo  (CvSelectionGroup.cpp:4751)  <- call CvSelectionGroup::groupMove
- CvSelectionGroup::groupRoadTo  (CvSelectionGroup.cpp:4839)  <- call CvSelectionGroup::groupBuild
- CvSelectionGroup::insertAtEndMissionQueue  (CvSelectionGroup.cpp:6139)  <- call CvSelectionGroup::activateHeadMission
- CvSelectionGroup::updateMission  (CvSelectionGroup.cpp:774)  <- call CvSelectionGroup::continueMission
- CvSelectionGroup::updateTimers  (CvSelectionGroup.cpp:525)  <- call CvUnit::updateAirCombat
- CvTeam::cancelDefensivePacts  (CvTeam.cpp:6990)  <- call CvDeal::kill
- CvTeam::changeAliveCount  (CvTeam.cpp:3777)  <- call CvTeam::setVassal
- CvTeam::changeExtraWaterSeeFromCount  (CvTeam.cpp:3946)  <- call CvMap::updateSight
- CvTeam::changeResearchProgressPercent  (CvTeam.cpp:5632)  <- call CvTeam::changeResearchProgress
- CvTeam::changeTechShareCount  (CvTeam.cpp:4376)  <- call CvTeam::updateTechShare
- CvTeam::declareWar  (CvTeam.cpp:1410)  <- call CvDeal::kill
- CvTeam::freeVassal  (CvTeam.cpp:5158)  <- call CvDeal::kill
- CvTeam::makeHasMet  (CvTeam.cpp:4469)  <- call CvTeam::updateTechShare
- CvTeam::setEspionagePointsAgainstTeam  (CvTeam.cpp:7066)  <- call CvTeam::verifySpyUnitsValidPlot
- CvTeamAI::AI_doTurnPost  (CvTeamAI.cpp:188)  <- call CvTeamAI::AI_doWar
- CvUnit::attack  (CvUnit.cpp:3034)  <- call CvUnit::updateCombat
- CvUnit::changeDamage  (CvUnit.cpp:11173)  <- call CvUnit::setDamage
- CvUnit::collateralCombat  (CvUnit.cpp:13134)  <- call CvUnit::setDamage
- CvUnit::doActiveDefense  (CvUnit.cpp:16322)  <- call CvUnit::setDamage
- CvUnit::doCommand  (CvUnit.cpp:2414)  <- call CvUnit::scrap
- CvUnit::fightInterceptor  (CvUnit.cpp:3044)  <- call CvUnit::updateAirCombat
- CvUnit::gift  (CvUnit.cpp:3496)  <- call CvPlayer::initUnit
- CvUnit::influencePlots  (CvUnit.cpp:16873)  <- call CvPlot::setCulture
- CvUnit::promote  (CvUnit.cpp:7731)  <- call CvUnit::setHasPromotion
- CvUnit::rangeStrike  (CvUnit.cpp:13591)  <- call CvUnit::setDamage
- CvUnit::resolveCombat  (CvUnit.cpp:1247)  <- call CvUnit::setDamage
- CvUnit::upgrade  (CvUnit.cpp:8360)  <- call CvPlayer::initUnit
- CvUnitAI::AI_barbAttackSeaMove  (CvUnitAI.cpp:5966)  <- call CvUnit::scrap
- CvUnitAI::AI_carrierSeaTransport  (CvUnitAI.cpp:18795)  <- call CvSelectionGroupAI::AI_update
- CvUnitAI::AI_doInquisition  (CvUnitAI.cpp:14097)  <- call CvUnit::performInquisition
- CvUnitAI::AI_escortSeaMove  (CvUnitAI.cpp:6687)  <- call CvUnit::scrap
- CvUnitAI::AI_exploreMove  (CvUnitAI.cpp:4611)  <- call CvUnit::scrap
- CvUnitAI::AI_exploreSeaMove  (CvUnitAI.cpp:6922)  <- call CvUnit::scrap
- CvUnitAI::AI_settleMove  (CvUnitAI.cpp:1389)  <- call CvUnit::scrap
- CvUnitAI::AI_settlerSeaMove  (CvUnitAI.cpp:7855)  <- call CvUnit::scrap
- CvUnitAI::AI_spyMove  (CvUnitAI.cpp:5568)  <- call CvUnitAI::AI_revoltCitySpy
- CvUnitAI::AI_upgrade  (CvUnitAI.cpp:617)  <- call CvUnit::doDelayedDeath
- CvUnitAI::AI_workerMove  (CvUnitAI.cpp:1547)  <- call CvUnit::scrap
- CvUnitAI::AI_workerSeaMove  (CvUnitAI.cpp:5850)  <- call CvUnit::scrap
- CyCity::popOrder  (CyCity.cpp:2662)  <- call CvCity::popOrder
- CyDeal::kill  (CyDeal.cpp:91)  <- call CvDeal::kill
- CyGame::setAIAutoPlay  (CyGame.cpp:570)  <- call CvGame::setAIAutoPlay
- CyGameTextMgr::getActiveDealsString  (CyGameTextMgr.cpp:250)  <- call CvGameTextMgr::getActiveDealsString
- CyMap::setAllPlotTypes  (CyMap.cpp:40)  <- call CvMap::setAllPlotTypes
- CyMapGenerator::addLakes  (CyMapGenerator.cpp:45)  <- call CvMapGenerator::addLakes
- CyMapGenerator::setPlotTypes  (CyMapGenerator.cpp:141)  <- call CvMapGenerator::setPlotTypes
- CyPlayer::canStopTradingWithTeam  (CyPlayer.cpp:441)  <- call CvPlayer::canStopTradingWithTeam
- CyPlayer::disbandUnit  (CyPlayer.cpp:175)  <- call CvPlayer::disbandUnit
- CyPlayer::initTriggeredData  (CyPlayer.cpp:2279)  <- call CvPlayer::initTriggeredData
- CyPlayer::initUnit  (CyPlayer.cpp:170)  <- call CvPlayer::initUnit
- CyPlayer::killUnits  (CyPlayer.cpp:180)  <- call CvPlayer::killUnits
- CyPlayer::raze  (CyPlayer.cpp:479)  <- call CvPlayer::raze
- CyPlot::setCulture  (CyPlot.cpp:894)  <- call CvPlot::setCulture
- CyPlot::setTerrainType  (CyPlot.cpp:662)  <- call CvPlot::setTerrainType
- CyTeam::changeResearchProgress  (CyTeam.cpp:839)  <- call CvTeam::changeResearchProgress
- CyTeam::setVassal  (CyTeam.cpp:706)  <- call CvTeam::setVassal
- CyUnit::attackForDamage  (CyUnit.cpp:1759)  <- call CvUnit::attackForDamage
- CyUnit::convert  (CyUnit.cpp:29)  <- call CvUnit::convert
- CyUnit::lead  (CyUnit.cpp:459)  <- call CvUnit::lead
- CyUnit::rotateFacingDirectionClockwise  (CyUnit.cpp:1316)  <- call CvUnit::rotateFacingDirectionClockwise
- CyUnit::rotateFacingDirectionCounterClockwise  (CyUnit.cpp:1322)  <- call CvUnit::rotateFacingDirectionCounterClockwise
- CyUnit::setDamage  (CyUnit.cpp:1239)  <- call CvUnit::setDamage
- CyUnit::setHasPromotion  (CyUnit.cpp:1726)  <- call CvUnit::setHasPromotion
- `anonymous namespace'::setOperationalGeneralBadge  (CvPlayerAI.cpp:15602)  <- call CvUnit::setHasPromotion

### level 6 (99)

- CvArea::changeBorderObstacleCount  (CvArea.cpp:731)  <- call CvMap::verifyUnitValidPlot
- CvCity::conscript  (CvCity.cpp:4233)  <- call CvCity::initConscriptedUnit
- CvCity::createGreatPeople  (CvCity.cpp:1498)  <- call CvPlayer::createGreatPeople
- CvCity::doPlotCulture  (CvCity.cpp:13550)  <- call CvPlot::changeCulture
- CvCity::processBuilding  (CvCity.cpp:4407)  <- call CvCity::setHeadquarters
- CvCity::setProductionAutomated  (CvCity.cpp:8719)  <- call CvCity::clearOrderQueue
- CvCity::updateCultureLevel  (CvCity.cpp:8987)  <- call CvCity::setCultureLevel
- CvCityAI::AI_buildGovernorChooseProduction  (CvCityAI.cpp:12171)  <- call CvCity::clearOrderQueue
- CvCityAI::AI_chooseBuilding  (CvCityAI.cpp:9712)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseProcess  (CvCityAI.cpp:9752)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseProduction  (CvCityAI.cpp:706)  <- call CvCity::clearOrderQueue
- CvCityAI::AI_chooseProject  (CvCityAI.cpp:9736)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseUnit  (CvCityAI.cpp:9406)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseUnit  (CvCityAI.cpp:9457)  <- call CvCity::pushOrder
- CvCityAI::AI_trainInquisitor  (CvCityAI.cpp:13542)  <- call CvCity::pushOrder
- CvDLLButtonPopup::launchButtonPopup  (CvDLLButtonPopup.cpp:855)  <- call CvDLLButtonPopup::launchRazeCityPopup
- CvDLLWidgetData::parseLeaderheadHelp  (CvDLLWidgetData.cpp:6025)  <- call CvGameTextMgr::parseLeaderHeadHelp
- CvDLLWidgetData::parseLeaderheadRelationsHelp  (CvDLLWidgetData.cpp:6036)  <- call CvGameTextMgr::parseLeaderHeadRelationsHelp
- CvEventReporter::buildingBuilt  (CvEventReporter.cpp:382)  <- call CvDllPythonEvents::reportBuildingBuilt
- CvEventReporter::endGameTurn  (CvEventReporter.cpp:100)  <- call CvDllPythonEvents::reportEndGameTurn
- CvEventReporter::endPlayerTurn  (CvEventReporter.cpp:123)  <- call CvDllPythonEvents::reportEndPlayerTurn
- CvEventReporter::projectBuilt  (CvEventReporter.cpp:389)  <- call CvDllPythonEvents::reportProjectBuilt
- CvEventReporter::reportModNetMessage  (CvEventReporter.cpp:64)  <- call CvDllPythonEvents::reportModNetMessage
- CvGame::addVoteSelection  (CvGame.cpp:9990)  <- call CvGame::isValidVoteSelection
- CvGame::addVoteTriggered  (CvGame.cpp:10152)  <- call CvPlayerAI::AI_diploVote
- CvGame::canDoResolution  (CvGame.cpp:4872)  <- call CvPlayer::canDoResolution
- CvGame::doHolyCity  (CvGame.cpp:7015)  <- call CvPlayer::foundReligion
- CvGame::setHeadquarters  (CvGame.cpp:6407)  <- call CvCity::setHasCorporation
- CvGame::updateWar  (CvGame.cpp:7875)  <- call CvTeam::declareWar
- CvGameTextMgr::setBonusTradeHelp  (CvGameTextMgr.cpp:13296)  <- call CvPlayer::canTradeItem
- CvGameTextMgr::setTechTradeHelp  (CvGameTextMgr.cpp:8365)  <- call CvPlayer::canTradeItem
- CvMapGenerator::generateRandomMap  (CvMapGenerator.cpp:999)  <- call CvMapGenerator::generatePlotTypes
- CvNetChangeWar::Execute  (CvMessageData.cpp:1080)  <- call CvTeam::declareWar
- CvNetDoCommand::Execute  (CvMessageData.cpp:863)  <- call CvUnit::doCommand
- CvNetFoundReligion::Execute  (CvMessageData.cpp:620)  <- call CvPlayer::foundReligion
- CvNetPushOrder::Execute  (CvMessageData.cpp:185)  <- call CvCity::pushOrder
- CvPlayer::addFreeUnitAI  (CvPlayer.cpp:1945)  <- call CvPlayer::addFreeUnit
- CvPlayer::buildTradeTable  (CvPlayer.cpp:23774)  <- call CvPlayer::canTradeItem
- CvPlayer::findNewCapital  (CvPlayer.cpp:6012)  <- call CvCity::setNumRealBuilding
- CvPlayer::foundCorporation  (CvPlayer.cpp:9362)  <- call CvCity::setHeadquarters
- CvPlayer::removeBuildingClass  (CvPlayer.cpp:7705)  <- call CvCity::setNumRealBuilding
- CvPlayer::setCivics  (CvPlayer.cpp:14261)  <- call CvGame::updateSecretaryGeneral
- CvPlayer::setLastStateReligion  (CvPlayer.cpp:12729)  <- call CvGame::updateSecretaryGeneral
- CvPlayer::setLoyalMember  (CvPlayer.cpp:14155)  <- call CvGame::updateSecretaryGeneral
- CvPlayer::setTeam  (CvPlayer.cpp:12861)  <- call CvTeam::changeAliveCount
- CvPlayer::updateTimers  (CvPlayer.cpp:4434)  <- call CvSelectionGroup::updateTimers
- CvPlayerAI::AI_doTurnPre  (CvPlayerAI.cpp:430)  <- call CvPlayerAI::AI_doMilitary
- CvSelectionGroup::groupDeclareWar  (CvSelectionGroup.cpp:4301)  <- call CvTeam::declareWar
- CvSelectionGroup::popMission  (CvSelectionGroup.cpp:703)  <- call CvSelectionGroup::deleteMissionQueueNode
- CvSelectionGroup::pushMission  (CvSelectionGroup.cpp:651)  <- call CvSelectionGroup::doDelayedDeath
- CvTeam::changeEspionagePointsAgainstTeam  (CvTeam.cpp:7080)  <- call CvTeam::setEspionagePointsAgainstTeam
- CvTeam::changeProjectCount  (CvTeam.cpp:5330)  <- call CvTeam::changeTechShareCount
- CvTeam::init  (CvTeam.cpp:130)  <- call CvTeam::declareWar
- CvTeam::makePeace  (CvTeam.cpp:1909)  <- call CvMap::verifyUnitValidPlot
- CvTeam::meet  (CvTeam.cpp:2220)  <- call CvTeam::makeHasMet
- CvTeam::setIsMinorCiv  (CvTeam.cpp:3369)  <- call CvTeam::declareWar
- CvTeam::setOpenBorders  (CvTeam.cpp:4659)  <- call CvMap::verifyUnitValidPlot
- CvTeamAI::AI_chooseElection  (CvTeamAI.cpp:1173)  <- call CvPlayerAI::AI_diploVote
- CvUnit::archerBombard  (CvUnit.cpp:16447)  <- call CvUnit::changeDamage
- CvUnit::doHeal  (CvUnit.cpp:4124)  <- call CvUnit::changeDamage
- CvUnit::doOpportunityFire  (CvUnit.cpp:16259)  <- call CvUnit::changeDamage
- CvUnit::doPillageInfluence  (CvUnit.cpp:16986)  <- call CvPlot::changeCulture
- CvUnit::doVictoryInfluence  (CvUnit.cpp:16736)  <- call CvUnit::influencePlots
- CvUnit::interceptTest  (CvUnit.cpp:13377)  <- call CvUnit::fightInterceptor
- CvUnit::resolveAirCombat  (CvUnit.cpp:943)  <- call CvUnit::changeDamage
- CvUnitAI::AI_assaultSeaMove  (CvUnitAI.cpp:7104)  <- call CvUnitAI::AI_barbAttackSeaMove
- CvUnitAI::AI_carrierSeaMove  (CvUnitAI.cpp:8421)  <- call CvUnitAI::AI_carrierSeaTransport
- CvUnitAI::AI_handleSettlerTransport  (CvUnitAI.cpp:7819)  <- call CvUnitAI::AI_settlerSeaMove
- CvUnitAI::AI_missileCarrierSeaMove  (CvUnitAI.cpp:8544)  <- call CvUnitAI::AI_carrierSeaTransport
- CvUnitAI::AI_missionaryMove  (CvUnitAI.cpp:4763)  <- call CvUnitAI::AI_doInquisition
- CvUnitAI::AI_poach  (CvUnitAI.cpp:24236)  <- call CvTeam::declareWar
- CvUnitAI::AI_promote  (CvUnitAI.cpp:695)  <- call CvUnit::promote
- CvUnitAI::AI_switchHurry  (CvUnitAI.cpp:13917)  <- call CvCity::pushOrder
- CvUnitAI::AI_update  (CvUnitAI.cpp:195)  <- call CvUnitAI::AI_spyMove
- CyCity::addProductionExperience  (CyCity.cpp:397)  <- call CvCity::addProductionExperience
- CyCity::clearOrderQueue  (CyCity.cpp:2650)  <- call CvCity::clearOrderQueue
- CyCity::pushOrder  (CyCity.cpp:2656)  <- call CvCity::pushOrder
- CyCity::setHasCorporation  (CyCity.cpp:2629)  <- call CvCity::setHasCorporation
- CyCity::setNumRealBuilding  (CyCity.cpp:2602)  <- call CvCity::setNumRealBuilding
- CyGame::reviveActivePlayer  (CyGame.cpp:293)  <- call CvGame::reviveActivePlayer
- CyMap::verifyUnitValidPlot  (CyMap.cpp:51)  <- call CvMap::verifyUnitValidPlot
- CyMapGenerator::generatePlotTypes  (CyMapGenerator.cpp:123)  <- call CvMapGenerator::generatePlotTypes
- CyMapGenerator::generateTerrain  (CyMapGenerator.cpp:129)  <- call CvMapGenerator::generateTerrain
- CyPlayer::canTradeItem  (CyPlayer.cpp:406)  <- call CvPlayer::canTradeItem
- CyPlayer::createGreatPeople  (CyPlayer.cpp:1127)  <- call CvPlayer::createGreatPeople
- CyPlayer::foundReligion  (CyPlayer.cpp:813)  <- call CvPlayer::foundReligion
- CyPlayer::killAllDeals  (CyPlayer.cpp:452)  <- call CvPlayer::killAllDeals
- CyPlayer::trigger  (CyPlayer.cpp:2252)  <- call CvPlayer::trigger
- CyPlot::changeCulture  (CyPlot.cpp:900)  <- call CvPlot::changeCulture
- CyTeam::changeExtraWaterSeeFromCount  (CyTeam.cpp:362)  <- call CvTeam::changeExtraWaterSeeFromCount
- CyTeam::changeTechShareCount  (CyTeam.cpp:631)  <- call CvTeam::changeTechShareCount
- CyTeam::declareWar  (CyTeam.cpp:64)  <- call CvTeam::declareWar
- CyTeam::freeVassal  (CyTeam.cpp:722)  <- call CvTeam::freeVassal
- CyTeam::setEspionagePointsAgainstTeam  (CyTeam.cpp:927)  <- call CvTeam::setEspionagePointsAgainstTeam
- CyUnit::changeDamage  (CyUnit.cpp:1245)  <- call CvUnit::changeDamage
- CyUnit::doCommand  (CyUnit.cpp:67)  <- call CvUnit::doCommand
- CyUnit::gift  (CyUnit.cpp:138)  <- call CvUnit::gift
- CyUnit::promote  (CyUnit.cpp:479)  <- call CvUnit::promote
- CyUnit::rangeStrike  (CyUnit.cpp:1767)  <- call CvUnit::rangeStrike

### level 7 (203)

- CvCity::doGreatPeople  (CvCity.cpp:13978)  <- call CvCity::createGreatPeople
- CvCity::setCultureTimes100  (CvCity.cpp:10745)  <- call CvCity::doPlotCulture
- CvCity::setNumFreeBuilding  (CvCity.cpp:12271)  <- call CvCity::processBuilding
- CvCity::setOccupationTimer  (CvCity.cpp:8504)  <- call CvCity::updateCultureLevel
- CvCityAI::AI_chooseDefender  (CvCityAI.cpp:9488)  <- call CvCityAI::AI_chooseUnit
- CvCityAI::AI_chooseLeastRepresentedUnit  (CvCityAI.cpp:9514)  <- call CvCityAI::AI_chooseUnit
- CvCityAI::AI_doDraft  (CvCityAI.cpp:8436)  <- call CvCity::conscript
- CvCityAI::AI_doPanic  (CvCityAI.cpp:12033)  <- call CvCityAI::AI_chooseUnit
- CvDLLWidgetData::parseBonusTradeHelp  (CvDLLWidgetData.cpp:5639)  <- call CvGameTextMgr::setBonusTradeHelp
- CvDLLWidgetData::parseTechTradeEntryHelp  (CvDLLWidgetData.cpp:5282)  <- call CvGameTextMgr::setTechTradeHelp
- CvDllPythonEvents::reportBeginGameTurn  (CvDllPythonEvents.cpp:156)  <- event Revolution/Gameready/TechDiffusion.py TechDiffusion.onBeginGameTurn
- CvDllPythonEvents::reportBeginPlayerTurn  (CvDllPythonEvents.cpp:196)  <- event RoMEventManager.py RoMEventManager.onBeginPlayerTurn
- CvDllPythonEvents::reportCityAcquired  (CvDllPythonEvents.cpp:499)  <- event Revolution/Gameready/BarbarianCiv.py BarbarianCiv.onCityAcquired
- CvDllPythonEvents::reportCityRazed  (CvDllPythonEvents.cpp:483)  <- event base/CvEventManager.py CvEventManager.onCityRazed
- CvDllPythonEvents::reportKbdEvent  (CvDllPythonEvents.cpp:30)  <- event base/CvEventManager.py CvEventManager.onKbdEvent
- CvDllPythonEvents::reportSetPlayerAlive  (CvDllPythonEvents.cpp:1273)  <- event Revolution/Gameready/StartAsMinors.py onSetPlayerAlive
- CvDllPythonEvents::reportVictory  (CvDllPythonEvents.cpp:1247)  <- event Revolution/Gameready/AIAutoPlay.py AIAutoPlay.onVictory
- CvGame::addVoteTriggered  (CvGame.cpp:10142)  <- call CvGame::addVoteTriggered
- CvGame::doHeadquarters  (CvGame.cpp:7147)  <- call CvPlayer::foundCorporation
- CvGame::doVoteSelection  (CvGame.cpp:10413)  <- call CvTeam::meet
- CvGame::updateTimers  (CvGame.cpp:7980)  <- call CvPlayer::updateTimers
- CvGameTextMgr::setBonusHelp  (CvGameTextMgr.cpp:13291)  <- call CvGameTextMgr::setBonusTradeHelp
- CvGameTextMgr::setTechHelp  (CvGameTextMgr.cpp:8359)  <- call CvGameTextMgr::setTechTradeHelp
- CvNetModNetMessage::Execute  (CvMessageData.cpp:524)  <- call CvEventReporter::reportModNetMessage
- CvNetPushMission::Execute  (CvMessageData.cpp:769)  <- call CvSelectionGroup::pushMission
- CvPlayer::convert  (CvPlayer.cpp:9086)  <- call CvPlayer::setLastStateReligion
- CvPlayer::doEspionagePoints  (CvPlayer.cpp:15421)  <- call CvTeam::changeEspionagePointsAgainstTeam
- CvPlayer::processBuilding  (CvPlayer.cpp:7739)  <- call CvArea::changeBorderObstacleCount
- CvPlayer::resetCivTypeEffects  (CvPlayer.cpp:1479)  <- call CvPlayer::setCivics
- CvPlayer::revolution  (CvPlayer.cpp:8924)  <- call CvPlayer::setCivics
- CvPlayer::setCombatExperience  (CvPlayer.cpp:11673)  <- call CvCity::createGreatPeople
- CvPlayer::setDefiedResolution  (CvPlayer.cpp:23353)  <- call CvPlayer::setLoyalMember
- CvPlayer::setEndorsedResolution  (CvPlayer.cpp:23379)  <- call CvPlayer::setLoyalMember
- CvPlayer::verifyCivics  (CvPlayer.cpp:4138)  <- call CvPlayer::setCivics
- CvPlot::processArea  (CvPlot.cpp:9053)  <- call CvArea::changeBorderObstacleCount
- CvSelectionGroup::groupAmphibMove  (CvSelectionGroup.cpp:5173)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separate  (CvSelectionGroupAI.cpp:64)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateAI  (CvSelectionGroupAI.cpp:111)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateEmptyTransports  (CvSelectionGroupAI.cpp:157)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateImpassable  (CvSelectionGroupAI.cpp:134)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateNonAI  (CvSelectionGroupAI.cpp:89)  <- call CvSelectionGroup::pushMission
- CvTeam::changeObsoleteBuildingCount  (CvTeam.cpp:5542)  <- call CvCity::processBuilding
- CvTeam::resetVictoryProgress  (CvTeam.cpp:5852)  <- call CvTeam::changeProjectCount
- CvTeamAI::AI_reviewWars  (CvTeamAI.cpp:4132)  <- call CvTeam::makePeace
- CvUnit::bombard  (CvUnit.cpp:5290)  <- call CvSelectionGroup::groupDeclareWar
- CvUnit::fighterEngage  (CvUnit.cpp:16623)  <- call CvUnit::interceptTest
- CvUnitAI::AI_Abombard  (CvUnitAI.cpp:25113)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_FEngage  (CvUnitAI.cpp:25179)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_ICBMMove  (CvUnitAI.cpp:5759)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_RbombardCity  (CvUnitAI.cpp:24924)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_RbombardNaval  (CvUnitAI.cpp:25029)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_RbombardPlot  (CvUnitAI.cpp:24752)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_RbombardUnit  (CvUnitAI.cpp:24834)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_airBombDefenses  (CvUnitAI.cpp:22187)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_airBombPlots  (CvUnitAI.cpp:22098)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_airCarrier  (CvUnitAI.cpp:21647)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_airDefensiveCity  (CvUnitAI.cpp:21529)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_airOffensiveCity  (CvUnitAI.cpp:21113)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_airStrike  (CvUnitAI.cpp:21785)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_animalMove  (CvUnitAI.cpp:1362)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_anyAttack  (CvUnitAI.cpp:15950)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_artistCultureVictoryMove  (CvUnitAI.cpp:24089)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_artistMove  (CvUnitAI.cpp:4953)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_assaultSeaReinforce  (CvUnitAI.cpp:17625)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_assaultSeaTransport  (CvUnitAI.cpp:17256)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_attackAirMove  (CvUnitAI.cpp:8643)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_attackCityLemmingMove  (CvUnitAI.cpp:3472)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_attackCityMove  (CvUnitAI.cpp:2800)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_attackMove  (CvUnitAI.cpp:2145)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_attackSeaMove  (CvUnitAI.cpp:6194)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_barbAttackMove  (CvUnitAI.cpp:1930)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_blockade  (CvUnitAI.cpp:16192)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_bombardCity  (CvUnitAI.cpp:15760)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_bonusOffenseSpy  (CvUnitAI.cpp:23106)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_carrierAirMove  (CvUnitAI.cpp:9289)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_choke  (CvUnitAI.cpp:24351)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_cityAttack  (CvUnitAI.cpp:15873)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_cityAutomated  (CvUnitAI.cpp:9571)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_cityDefenseExtraMove  (CvUnitAI.cpp:4491)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_cityDefenseMove  (CvUnitAI.cpp:4255)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_cityOffenseSpy  (CvUnitAI.cpp:23046)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_collateralMove  (CvUnitAI.cpp:3516)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_connectPlot  (CvUnitAI.cpp:18995)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_construct  (CvUnitAI.cpp:13806)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_counterMove  (CvUnitAI.cpp:4068)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_defend  (CvUnitAI.cpp:14602)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_defendBaseAirStrike  (CvUnitAI.cpp:22004)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_defenseAirMove  (CvUnitAI.cpp:8987)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_defensiveAirStrike  (CvUnitAI.cpp:21901)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_discover  (CvUnitAI.cpp:13468)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_engineerMove  (CvUnitAI.cpp:5453)  <- call CvUnitAI::AI_switchHurry
- CvUnitAI::AI_explore  (CvUnitAI.cpp:15008)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_exploreAir  (CvUnitAI.cpp:22280)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_exploreAir2  (CvUnitAI.cpp:22364)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_exploreAirMove  (CvUnitAI.cpp:22425)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_exploreRange  (CvUnitAI.cpp:15153)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_follow  (CvUnitAI.cpp:556)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_followBombard  (CvUnitAI.cpp:23406)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_fortTerritory  (CvUnitAI.cpp:19593)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_found  (CvUnitAI.cpp:17090)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_foundRange  (CvUnitAI.cpp:17179)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_generalMove  (CvUnitAI.cpp:5180)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_goToTargetBarbCity  (CvUnitAI.cpp:15545)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_goToTargetCity  (CvUnitAI.cpp:15452)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_goldenAge  (CvUnitAI.cpp:12767)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_goody  (CvUnitAI.cpp:14936)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_greatWork  (CvUnitAI.cpp:14138)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_group  (CvUnitAI.cpp:10591)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_groupMergeRange  (CvUnitAI.cpp:10747)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardBonus  (CvUnitAI.cpp:11778)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardCity  (CvUnitAI.cpp:11459)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardCityAirlift  (CvUnitAI.cpp:11710)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardCityBestDefender  (CvUnitAI.cpp:11338)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardCityMinDefender  (CvUnitAI.cpp:11361)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardCitySite  (CvUnitAI.cpp:12025)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardFort  (CvUnitAI.cpp:11934)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_guardSpy  (CvUnitAI.cpp:12080)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_heal  (CvUnitAI.cpp:12534)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_hide  (CvUnitAI.cpp:14800)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_hurry  (CvUnitAI.cpp:13984)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_improveBonus  (CvUnitAI.cpp:19709)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_improveCity  (CvUnitAI.cpp:19086)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_improveLocalPlot  (CvUnitAI.cpp:19140)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_improvePlot  (CvUnitAI.cpp:19964)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_infiltrate  (CvUnitAI.cpp:22710)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_irrigateTerritory  (CvUnitAI.cpp:19455)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_join  (CvUnitAI.cpp:13697)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_lead  (CvUnitAI.cpp:13522)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_leaveAttack  (CvUnitAI.cpp:16098)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_load  (CvUnitAI.cpp:11105)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_loadForSettlement  (CvUnitAI.cpp:11079)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_merchantMove  (CvUnitAI.cpp:5363)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_missileAirMove  (CvUnitAI.cpp:9374)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_missileLoad  (CvUnitAI.cpp:21729)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_missionarySeaMove  (CvUnitAI.cpp:8203)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_moveIntoCity  (CvUnitAI.cpp:24020)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_moveToInquisitionTarget  (CvUnitAI.cpp:14105)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_moveToStagingCity  (CvUnitAI.cpp:23197)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_networkAutomated  (CvUnitAI.cpp:9487)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_nextCityToImprove  (CvUnitAI.cpp:19286)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_nextCityToImproveAirlift  (CvUnitAI.cpp:19395)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_nuke  (CvUnitAI.cpp:22452)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_nukeRange  (CvUnitAI.cpp:22503)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_offensiveAirlift  (CvUnitAI.cpp:14228)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_operationMove  (CvUnitAI.cpp:2103)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_paradrop  (CvUnitAI.cpp:14323)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_paratrooperMove  (CvUnitAI.cpp:2657)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_patrol  (CvUnitAI.cpp:14526)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pickup  (CvUnitAI.cpp:20742)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pickupStranded  (CvUnitAI.cpp:20982)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pillage  (CvUnitAI.cpp:16836)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pillageAroundCity  (CvUnitAI.cpp:15662)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pillageMove  (CvUnitAI.cpp:3730)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pillageRange  (CvUnitAI.cpp:16979)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pirateBlockade  (CvUnitAI.cpp:16326)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_pirateSeaMove  (CvUnitAI.cpp:6096)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_prophetMove  (CvUnitAI.cpp:4847)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_protect  (CvUnitAI.cpp:14451)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_rangeAttack  (CvUnitAI.cpp:16047)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_reconSpy  (CvUnitAI.cpp:22800)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_reinforceOperation  (CvUnitAI.cpp:2125)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_reserveMove  (CvUnitAI.cpp:3877)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_reserveSeaMove  (CvUnitAI.cpp:6472)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_retreatToCity  (CvUnitAI.cpp:20519)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_routeCity  (CvUnitAI.cpp:20251)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_routeTerritory  (CvUnitAI.cpp:20311)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_safety  (CvUnitAI.cpp:14684)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_scientistMove  (CvUnitAI.cpp:5064)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_seaBombardRange  (CvUnitAI.cpp:16586)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_settlerSeaFerry  (CvUnitAI.cpp:18379)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_settlerSeaTransport  (CvUnitAI.cpp:18133)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_shadow  (CvUnitAI.cpp:10481)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_solveBlockageProblem  (CvUnitAI.cpp:24446)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_specialSeaTransportMissionary  (CvUnitAI.cpp:18449)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_specialSeaTransportSpy  (CvUnitAI.cpp:18673)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_spreadCorporation  (CvUnitAI.cpp:13062)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_spreadCorporationAirlift  (CvUnitAI.cpp:13367)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_spreadReligion  (CvUnitAI.cpp:12780)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_spreadReligionAirlift  (CvUnitAI.cpp:13238)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_spySeaMove  (CvUnitAI.cpp:8308)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_stackAttackCity  (CvUnitAI.cpp:23920)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_trade  (CvUnitAI.cpp:22634)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_travelToUpgradeCity  (CvUnitAI.cpp:20407)  <- call CvSelectionGroup::pushMission
- CyCity::conscript  (CyCity.cpp:581)  <- call CvCity::conscript
- CyCity::createGreatPeople  (CyCity.cpp:210)  <- call CvCity::createGreatPeople
- CyCity::setProductionAutomated  (CyCity.cpp:1845)  <- call CvCity::setProductionAutomated
- CyGame::clearHeadquarters  (CyGame.cpp:974)  <- call CvGame::setHeadquarters
- CyGame::setHeadquarters  (CyGame.cpp:968)  <- call CvGame::setHeadquarters
- CyMapGenerator::generateRandomMap  (CyMapGenerator.cpp:117)  <- call CvMapGenerator::generateRandomMap
- CyPlayer::findNewCapital  (CyPlayer.cpp:463)  <- call CvPlayer::findNewCapital
- CyPlayer::foundCorporation  (CyPlayer.cpp:834)  <- call CvPlayer::foundCorporation
- CyPlayer::removeBuildingClass  (CyPlayer.cpp:574)  <- call CvPlayer::removeBuildingClass
- CyPlayer::setCivics  (CyPlayer.cpp:2068)  <- call CvPlayer::setCivics
- CyPlayer::setLastStateReligion  (CyPlayer.cpp:1727)  <- call CvPlayer::setLastStateReligion
- CyPlayer::setLoyalMember  (CyPlayer.cpp:1872)  <- call CvPlayer::setLoyalMember
- CySelectionGroup::popMission  (CySelectionGroup.cpp:38)  <- call CvSelectionGroup::popMission
- CySelectionGroup::pushMission  (CySelectionGroup.cpp:26)  <- call CvSelectionGroup::pushMission
- CySelectionGroup::pushMoveToMission  (CySelectionGroup.cpp:32)  <- call CvSelectionGroup::pushMission
- CyTeam::changeEspionagePointsAgainstTeam  (CyTeam.cpp:933)  <- call CvTeam::changeEspionagePointsAgainstTeam
- CyTeam::changeProjectCount  (CyTeam.cpp:787)  <- call CvTeam::changeProjectCount
- CyTeam::makePeace  (CyTeam.cpp:70)  <- call CvTeam::makePeace
- CyTeam::meet  (CyTeam.cpp:81)  <- call CvTeam::meet
- CyTeam::setIsMinorCiv  (CyTeam.cpp:266)  <- call CvTeam::setIsMinorCiv

### level 8 (46)

- CvCity::changeCulture  (CvCity.cpp:10765)  <- call CvCity::setCultureTimes100
- CvCity::changeCultureTimes100  (CvCity.cpp:10770)  <- call CvCity::setCultureTimes100
- CvCity::changeOccupationTimer  (CvCity.cpp:8531)  <- call CvCity::setOccupationTimer
- CvCity::setCulture  (CvCity.cpp:10740)  <- call CvCity::setCultureTimes100
- CvCityAI::AI_doTurn  (CvCityAI.cpp:186)  <- call CvCityAI::AI_doDraft
- CvDLLWidgetData::parseBonusHelp  (CvDLLWidgetData.cpp:5630)  <- call CvGameTextMgr::setBonusHelp
- CvDLLWidgetData::parseResearchHelp  (CvDLLWidgetData.cpp:3433)  <- call CvGameTextMgr::setTechHelp
- CvDLLWidgetData::parseTechEntryHelp  (CvDLLWidgetData.cpp:5273)  <- call CvGameTextMgr::setTechHelp
- CvDLLWidgetData::parseTechTreeHelp  (CvDLLWidgetData.cpp:3458)  <- call CvGameTextMgr::setTechHelp
- CvDLLWidgetData::parseTechTreePrereq  (CvDLLWidgetData.cpp:5301)  <- call CvGameTextMgr::setTechHelp
- CvDllPythonEvents::reportGameStart  (CvDllPythonEvents.cpp:124)  <- event Revolution/Gameready/AIAutoPlay.py AIAutoPlay.onGameStart
- CvDllPythonEvents::reportTechAcquired  (CvDllPythonEvents.cpp:1094)  <- event Revolution/Gameready/StartAsMinors.py onTechAcquired
- CvEventReporter::beginGameTurn  (CvEventReporter.cpp:94)  <- call CvDllPythonEvents::reportBeginGameTurn
- CvEventReporter::beginPlayerTurn  (CvEventReporter.cpp:118)  <- call CvDllPythonEvents::reportBeginPlayerTurn
- CvEventReporter::cityAcquired  (CvEventReporter.cpp:218)  <- call CvDllPythonEvents::reportCityAcquired
- CvEventReporter::cityRazed  (CvEventReporter.cpp:211)  <- call CvDllPythonEvents::reportCityRazed
- CvEventReporter::kbdEvent  (CvEventReporter.cpp:34)  <- call CvDllPythonEvents::reportKbdEvent
- CvEventReporter::setPlayerAlive  (CvEventReporter.cpp:452)  <- call CvDllPythonEvents::reportSetPlayerAlive
- CvEventReporter::victory  (CvEventReporter.cpp:479)  <- call CvDllPythonEvents::reportVictory
- CvGame::setVoteChosen  (CvGame.cpp:6267)  <- call CvGame::addVoteTriggered
- CvGame::testVictory  (CvGame.cpp:8359)  <- call CvTeam::resetVictoryProgress
- CvGame::verifyCivics  (CvGame.cpp:7966)  <- call CvPlayer::verifyCivics
- CvGameTextMgr::getBonusDataForWB  (CvGameTextMgr.cpp:20107)  <- call CvGameTextMgr::setBonusHelp
- CvGameTextMgr::getTechDataForWB  (CvGameTextMgr.cpp:20085)  <- call CvGameTextMgr::setTechHelp
- CvNetConvert::Execute  (CvMessageData.cpp:556)  <- call CvPlayer::convert
- CvNetUpdateCivics::Execute  (CvMessageData.cpp:336)  <- call CvPlayer::revolution
- CvPlayer::changeCiv  (CvPlayer.cpp:1573)  <- call CvPlayer::resetCivTypeEffects
- CvPlayer::changeCombatExperience  (CvPlayer.cpp:11726)  <- call CvPlayer::setCombatExperience
- CvPlayer::changeFreeBuildingCount  (CvPlayer.cpp:13596)  <- call CvCity::setNumFreeBuilding
- CvPlayer::getResourceLayerColors  (CvPlayer.cpp:24549)  <- call CvGameTextMgr::setBonusHelp
- CvPlayerAI::AI_doCivics  (CvPlayerAI.cpp:17033)  <- call CvPlayer::revolution
- CvPlayerAI::AI_doReligion  (CvPlayerAI.cpp:17126)  <- call CvPlayer::convert
- CvPlot::setArea  (CvPlot.cpp:4400)  <- call CvPlot::processArea
- CvUnitAI::AI_afterAttack  (CvUnitAI.cpp:12673)  <- call CvUnitAI::AI_guardCity
- CvUnitAI::AI_chokeDefend  (CvUnitAI.cpp:12496)  <- call CvUnitAI::AI_anyAttack
- CvUnitAI::AI_connectBonus  (CvUnitAI.cpp:20166)  <- call CvUnitAI::AI_connectPlot
- CvUnitAI::AI_connectCity  (CvUnitAI.cpp:20208)  <- call CvUnitAI::AI_connectPlot
- CvUnitAI::AI_loadForCoastalAttack  (CvUnitAI.cpp:10856)  <- call CvUnitAI::AI_load
- CyCity::setCultureTimes100  (CyCity.cpp:2185)  <- call CvCity::setCultureTimes100
- CyCity::setOccupationTimer  (CyCity.cpp:1762)  <- call CvCity::setOccupationTimer
- CyGameTextMgr::getBonusHelp  (CyGameTextMgr.cpp:121)  <- call CvGameTextMgr::setBonusHelp
- CyGameTextMgr::getTechHelp  (CyGameTextMgr.cpp:76)  <- call CvGameTextMgr::setTechHelp
- CyPlayer::convert  (CyPlayer.cpp:775)  <- call CvPlayer::convert
- CyPlayer::revolution  (CyPlayer.cpp:749)  <- call CvPlayer::revolution
- CyPlayer::setCombatExperience  (CyPlayer.cpp:2092)  <- call CvPlayer::setCombatExperience
- CySelectionGroupInterface  (CySelectionGroupInterface.cpp:15)  <- call CySelectionGroup::pushMission

### level 9 (17)

- CvCity::doCulture  (CvCity.cpp:13523)  <- call CvCity::changeCultureTimes100
- CvEventReporter::gameStart  (CvEventReporter.cpp:84)  <- call CvDllPythonEvents::reportGameStart
- CvEventReporter::techAcquired  (CvEventReporter.cpp:394)  <- call CvDllPythonEvents::reportTechAcquired
- CvGame::changeForceCivicCount  (CvGame.cpp:5974)  <- call CvGame::verifyCivics
- CvGame::setWinner  (CvGame.cpp:5529)  <- call CvEventReporter::victory
- CvMap::calculateAreas  (CvMap.cpp:1397)  <- call CvPlot::setArea
- CvMap::recalculateAreas  (CvMap.cpp:1203)  <- call CvPlot::setArea
- CvNetChooseElection::Execute  (CvMessageData.cpp:1014)  <- call CvGame::setVoteChosen
- CvPlayer::getGlobeLayerColors  (CvPlayer.cpp:24307)  <- call CvPlayer::getResourceLayerColors
- CvUnit::changeExperience  (CvUnit.cpp:11251)  <- call CvPlayer::changeCombatExperience
- CyCity::changeCulture  (CyCity.cpp:2191)  <- call CvCity::changeCulture
- CyCity::changeCultureTimes100  (CyCity.cpp:2197)  <- call CvCity::changeCultureTimes100
- CyCity::changeOccupationTimer  (CyCity.cpp:1768)  <- call CvCity::changeOccupationTimer
- CyCity::setCulture  (CyCity.cpp:2179)  <- call CvCity::setCulture
- CyPlayer::changeCiv  (CyPlayer.cpp:40)  <- call CvPlayer::changeCiv
- CyPlayer::changeCombatExperience  (CyPlayer.cpp:2083)  <- call CvPlayer::changeCombatExperience
- joinArea  (CvGameCoreUtils.cpp:2564)  <- call CvPlot::setArea

### level 10 (8)

- CvDllPythonEvents::reportChangeWar  (CvDllPythonEvents.cpp:1234)  <- event Revolution/RevEvents.py onChangeWar
- CvDllPythonEvents::reportCityBuilt  (CvDllPythonEvents.cpp:468)  <- event Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.OnCityBuilt
- CvMap::setup  (CvMap.cpp:245)  <- call joinArea
- CvUnit::awardSpyExperience  (CvUnit.cpp:7177)  <- call CvUnit::changeExperience
- CvUnit::giveExperience  (CvUnit.cpp:7891)  <- call CvUnit::changeExperience
- CyGame::setWinner  (CyGame.cpp:713)  <- call CvGame::setWinner
- CyMap::recalculateAreas  (CyMap.cpp:270)  <- call CvMap::recalculateAreas
- CyUnit::changeExperience  (CyUnit.cpp:1285)  <- call CvUnit::changeExperience

### level 11 (3)

- CvEventReporter::changeWar  (CvEventReporter.cpp:447)  <- call CvDllPythonEvents::reportChangeWar
- CvEventReporter::cityBuilt  (CvEventReporter.cpp:204)  <- call CvDllPythonEvents::reportCityBuilt
- CyUnit::giveExperience  (CyUnit.cpp:469)  <- call CvUnit::giveExperience

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

### level 4 (50)

- AbandonCityEventManager.__eventAbandonCityDestroyBuildingApply  (AbandonCityEventManager.py:221)  <- py>cpp CyCity::kill
- Deal.getCannotCancelReason  (BUG/DealUtil.py:197)  <- py>cpp (name match) CyDeal::getCannotCancelReason
- Deal.isCancelable  (BUG/DealUtil.py:190)  <- py>cpp (name match) CyDeal::isCancelable
- Deal.kill  (BUG/DealUtil.py:208)  <- py>cpp (name match) CyCity::kill
- finderRegenerate  (Contrib/MapFinder.py:248)  <- py>cpp CyGame::regenerateMap
- regenerateForReal  (Contrib/MapFinder.py:67)  <- py>cpp CyGame::regenerateMap
- FeatureGenerator.addFeaturesAtPlot  (CvMapGeneratorUtil.py:1219)  <- py>cpp CyPlot::setFeatureType
- FeatureGenerator.addForestsAtPlot  (CvMapGeneratorUtil.py:1257)  <- py>cpp CyPlot::setFeatureType
- FeatureGenerator.addIceAtPlot  (CvMapGeneratorUtil.py:1238)  <- py>cpp CyPlot::setFeatureType
- FeatureGenerator.addJunglesAtPlot  (CvMapGeneratorUtil.py:1251)  <- py>cpp CyPlot::setFeatureType
- applyClassicLiteratureDone2  (EntryPoints/CvRandomEventInterface.py:2571)  <- py>cpp CyTeam::setHasTech
- applySilverRain3  (EntryPoints/CvRandomEventInterface.py:7162)  <- py>cpp CyPlot::nukeExplosion
- applyTsunami1  (EntryPoints/CvRandomEventInterface.py:698)  <- py>cpp CyCity::kill
- doNuclearProtest1  (EntryPoints/CvRandomEventInterface.py:4035)  <- py>cpp (name match) CyCity::kill
- advanceEra  (ModTools/ModTools.py:110)  <- py>cpp CyTeam::setHasTech
- clearMap  (ModTools/ModTools.py:12)  <- py>cpp CyPlayer::initCity
- showUnits  (ModTools/ModTools.py:25)  <- py>cpp CyPlot::erase
- showUnitsTerrain  (ModTools/ModTools.py:58)  <- py>cpp CyPlot::erase
- clearMap  (ModTools/ModToolsUtils.py:10)  <- py>cpp CyPlayer::initCity
- PyPlayer.initCity  (PyHelpers.py:336)  <- py>cpp CyPlayer::initCity
- PyPlayer.setHasTech  (PyHelpers.py:141)  <- py>cpp CyTeam::setHasTech
- BarbarianCiv.createMinorCiv  (Revolution/Gameready/BarbarianCiv.py:972)  <- py>cpp (only target) CyPlot::setOwner
- BarbarianCiv.giveTechs  (Revolution/Gameready/BarbarianCiv.py:402)  <- py>cpp CyTeam::setHasTech
- BarbarianCiv.settleMinorCiv  (Revolution/Gameready/BarbarianCiv.py:1326)  <- py>cpp (only target) CyPlot::setOwner
- BarbarianCiv.setupFormerBarbCity  (Revolution/Gameready/BarbarianCiv.py:827)  <- py>cpp (name match) CyCity::kill
- Revolution.onEndPlayerTurn  (Revolution/Gameready/Revolution.py:585)  <- py>py Revolution/Gameready/Revolution.py Revolution.launchRevolution
- Revolution.onModNetMessage  (Revolution/Gameready/Revolution.py:7005)  <- py>py Revolution/Gameready/Revolution.py Revolution.revolutionNetworkPopupHandler
- Revolution.pickRevolutionStyle  (Revolution/Gameready/Revolution.py:2400)  <- py>py Revolution/Gameready/Revolution.py Revolution.makeRevolutionDecision
- onEndGameTurn  (Revolution/RevEvents.py:119)  <- py>py Revolution/RevEvents.py checkForAssimilation
- removeFloatingRebellions  (Revolution/RevEvents.py:851)  <- py>cpp (name match) CyCity::kill
- clearOutCity  (Revolution/RevUtils.py:397)  <- py>cpp (name match) CyUnit::setXY
- giveTechs  (Revolution/RevUtils.py:822)  <- py>cpp CyTeam::setHasTech
- moveEnemyUnits  (Revolution/RevUtils.py:309)  <- py>cpp (name match) CyUnit::setXY
- moveEnemyUnits2  (Revolution/RevUtils.py:357)  <- py>cpp (name match) CyUnit::setXY
- RoMEventManager.onBuildingBuilt  (RoMEventManager.py:324)  <- py>cpp (name match) CyCity::kill
- RoMEventManager.onProjectBuilt  (RoMEventManager.py:390)  <- py>cpp CyPlot::setFeatureType
- CvForeignAdvisor.drawContents  (Screens/CvForeignAdvisor.py:165)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawPossibleDeals
- PLE.tempMove  (Screens/PLE.py:1283)  <- py>cpp (name match) CyUnit::setXY
- CvDebugTools.applyTechCheat  (base/CvDebugTools.py:206)  <- py>cpp (name match) CyTeam::setHasTech
- CvFillMap.fillPlot  (base/CvPerfTest.py:52)  <- py>cpp CyPlayer::initCity
- doGoody  (base/EntryPoints/CvGameInterface.py:216)  <- py>cpp (name match) CyPlayer::doGoody
- CvWorldBuilderScreen.handleTechCB  (base/Screens/CvWorldBuilderScreen.py:544)  <- py>cpp CyTeam::setHasTech
- CvWorldBuilderScreen.handleWorldBuilderTechByEraPullDownCB  (base/Screens/CvWorldBuilderScreen.py:497)  <- py>cpp CyTeam::setHasTech
- CvWorldBuilderScreen.leftMouseDown  (base/Screens/CvWorldBuilderScreen.py:255)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setMultipleReveal
- CvWorldBuilderScreen.mouseOverPlot  (base/Screens/CvWorldBuilderScreen.py:213)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setMultipleReveal
- CvWorldBuilderScreen.placeMultipleObjects  (base/Screens/CvWorldBuilderScreen.py:1828)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.placeObject
- CvWorldBuilderScreen.removeMultipleObjects  (base/Screens/CvWorldBuilderScreen.py:1866)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.removeObject
- CvWorldBuilderScreen.rightMouseDown  (base/Screens/CvWorldBuilderScreen.py:285)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setMultipleReveal
- CvWorldBuilderScreen.setCurrentNormalPlayerIndex  (base/Screens/CvWorldBuilderScreen.py:1622)  <- py>cpp CyTeam::setHasTech
- CvCityDesc.apply  (base/pyWB/CvWBDesc.py:858)  <- py>cpp (name match) CyPlayer::initCity

### level 5 (31)

- Scoreboard.addPlayer  (BUG/Scoreboard.py:207)  <- py>cpp (name match) CyGame::addPlayer
- FeatureGenerator.addFeatures  (CvMapGeneratorUtil.py:1209)  <- py>py CvMapGeneratorUtil.py FeatureGenerator.addFeaturesAtPlot
- Carnation2Callback  (EntryPoints/CvRandomEventInterface.py:4601)  <- py>cpp CyPlayer::forcePeace
- doCarnation2  (EntryPoints/CvRandomEventInterface.py:4570)  <- py>cpp CyPlayer::forcePeace
- doHeroicGesture2  (EntryPoints/CvRandomEventInterface.py:1616)  <- py>cpp CyPlayer::forcePeace
- heroicGesture2Callback  (EntryPoints/CvRandomEventInterface.py:1642)  <- py>cpp CyPlayer::forcePeace
- WorldBuilderHandleTechCB  (EntryPoints/CvScreensInterface.py:659)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleTechCB
- WorldBuilderOnNormalPlayerBrushSelected  (EntryPoints/CvScreensInterface.py:696)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setCurrentNormalPlayerIndex
- leftMouseDown  (EntryPoints/CvScreensInterface.py:891)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.leftMouseDown
- mouseOverPlot  (EntryPoints/CvScreensInterface.py:911)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.mouseOverPlot
- rightMouseDown  (EntryPoints/CvScreensInterface.py:901)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.rightMouseDown
- AIAutoPlay.doNewHuman  (Revolution/Gameready/AIAutoPlay.py:202)  <- py>cpp CyPlayer::setNewPlayerAlive
- BarbarianCiv.checkBarbCities  (Revolution/Gameready/BarbarianCiv.py:878)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.createMinorCiv
- BarbarianCiv.checkMinorCivs  (Revolution/Gameready/BarbarianCiv.py:1224)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.settleMinorCiv
- forceBarbCityToMinor  (Revolution/Gameready/BarbarianCiv.py:2049)  <- py>py (only target) Revolution/Gameready/BarbarianCiv.py BarbarianCiv.createMinorCiv
- Revolution.checkForRevolution  (Revolution/Gameready/Revolution.py:2137)  <- py>py Revolution/Gameready/Revolution.py Revolution.pickRevolutionStyle
- Revolution.chooseRevolutionCiv  (Revolution/Gameready/Revolution.py:3787)  <- py>cpp CyGame::addPlayer
- TechDiffusion.diffuseTech  (Revolution/Gameready/TechDiffusion.py:103)  <- py>cpp CyTeam::setResearchProgress
- CvForeignAdvisor.drawActive  (Screens/CvForeignAdvisor.py:215)  <- py>cpp CyGameTextMgr::getDealString
- CvForeignAdvisor.handleInput  (Screens/CvForeignAdvisor.py:804)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawContents
- CvForeignAdvisor.interfaceScreen  (Screens/CvForeignAdvisor.py:115)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawContents
- CvForeignAdvisor.update  (Screens/CvForeignAdvisor.py:825)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawContents
- PLE.selectGroup  (Screens/PLE.py:1297)  <- py>py Screens/PLE.py PLE.tempMove
- CvDebugTools.applyUnitPicker  (base/CvDebugTools.py:152)  <- py>py PyHelpers.py PyPlayer.initCity
- CvEventManager.__eventAwardTechsAndGoldApply  (base/CvEventManager.py:999)  <- py>py base/CvDebugTools.py CvDebugTools.applyTechCheat
- CvFillMap.emptyMap  (base/CvPerfTest.py:24)  <- py>cpp CyPlayer::killCities
- CvFillMap.fillMap  (base/CvPerfTest.py:30)  <- py>py base/CvPerfTest.py CvFillMap.fillPlot
- CvWorldBuilderDiplomacyScreen.handleVassalPullDownCB  (base/Screens/CvWorldBuilderDiplomacyScreen.py:351)  <- py>cpp CyTeam::assignVassal
- CvWorldBuilderScreen.handleInput  (base/Screens/CvWorldBuilderScreen.py:192)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleWorldBuilderTechByEraPullDownCB
- CvPlotDesc.preApply  (base/pyWB/CvWBDesc.py:1109)  <- py>cpp CyPlot::setPlotType
- CvWBDesc.applyMap  (base/pyWB/CvWBDesc.py:1559)  <- py>cpp CyMap::rebuild

### level 6 (77)

- PickReligionPopup.launchPopup  (Contrib/RevDCMReligionControl.py:194)  <- py>cpp CyGame::setAIAutoPlay
- spawnUnit  (CvUtil.py:351)  <- py>cpp (name match) CyPlayer::initUnit
- EnhancedTechConquest.onCityAcquired  (EnhancedTechConquestUtils/EnhancedTechConquest.py:79)  <- py>cpp CyTeam::changeResearchProgress
- applyBlackbeard1  (EntryPoints/CvRandomEventInterface.py:5138)  <- py>cpp CyPlayer::initUnit
- applyChampion  (EntryPoints/CvRandomEventInterface.py:1014)  <- py>cpp CyUnit::setHasPromotion
- applyCityRuinsTreasure1  (EntryPoints/CvRandomEventInterface.py:7301)  <- py>cpp CyPlayer::initUnit
- applyCrusadeDone1  (EntryPoints/CvRandomEventInterface.py:2961)  <- py>cpp CyPlayer::initUnit
- applyGreedDone1  (EntryPoints/CvRandomEventInterface.py:3358)  <- py>cpp CyPlayer::initUnit
- applyHenryMorgan1  (EntryPoints/CvRandomEventInterface.py:5583)  <- py>cpp CyPlayer::initUnit
- applyHorseWhisperingDone1  (EntryPoints/CvRandomEventInterface.py:2448)  <- py>cpp CyPlayer::initUnit
- applyIllyrianPirates1  (EntryPoints/CvRandomEventInterface.py:6066)  <- py>cpp CyPlayer::initUnit
- applyMahdiArmy1  (EntryPoints/CvRandomEventInterface.py:6163)  <- py>cpp CyPlayer::initUnit
- applyMalaccanPirates1  (EntryPoints/CvRandomEventInterface.py:5428)  <- py>cpp CyPlayer::initUnit
- applyMercenariesAncient1  (EntryPoints/CvRandomEventInterface.py:6436)  <- py>cpp CyPlayer::initUnit
- applyMercenariesAncient2  (EntryPoints/CvRandomEventInterface.py:6478)  <- py>cpp CyPlayer::initUnit
- applyMercenariesClassical1  (EntryPoints/CvRandomEventInterface.py:6593)  <- py>cpp CyPlayer::initUnit
- applyMercenariesClassical2  (EntryPoints/CvRandomEventInterface.py:6635)  <- py>cpp CyPlayer::initUnit
- applyMercenariesMedieval1  (EntryPoints/CvRandomEventInterface.py:6750)  <- py>cpp CyPlayer::initUnit
- applyMercenariesMedieval2  (EntryPoints/CvRandomEventInterface.py:6793)  <- py>cpp CyPlayer::initUnit
- applyPartisans1  (EntryPoints/CvRandomEventInterface.py:3162)  <- py>cpp CyPlayer::initUnit
- applyPartisans2  (EntryPoints/CvRandomEventInterface.py:3208)  <- py>cpp CyPlayer::initUnit
- applyPiratesoftheNeutralZones1  (EntryPoints/CvRandomEventInterface.py:5283)  <- py>cpp CyPlayer::initUnit
- applyRubicon2  (EntryPoints/CvRandomEventInterface.py:4359)  <- py>cpp CyUnit::setHasPromotion
- applySilverRain1  (EntryPoints/CvRandomEventInterface.py:7115)  <- py>cpp CyPlayer::initUnit
- applyStedeBonnet1  (EntryPoints/CvRandomEventInterface.py:5756)  <- py>cpp CyPlayer::initUnit
- applyTheBuccaneers1  (EntryPoints/CvRandomEventInterface.py:4996)  <- py>cpp CyPlayer::initUnit
- applyTheCorsairs1  (EntryPoints/CvRandomEventInterface.py:5909)  <- py>cpp CyPlayer::initUnit
- applyTheGoths1  (EntryPoints/CvRandomEventInterface.py:2099)  <- py>cpp CyPlayer::initUnit
- applyTheHuns1  (EntryPoints/CvRandomEventInterface.py:1877)  <- py>cpp CyPlayer::initUnit
- applyThePhilistines1  (EntryPoints/CvRandomEventInterface.py:2210)  <- py>cpp CyPlayer::initUnit
- applyTheTaliban1  (EntryPoints/CvRandomEventInterface.py:6255)  <- py>cpp CyPlayer::initUnit
- applyTheVandals1  (EntryPoints/CvRandomEventInterface.py:1988)  <- py>cpp CyPlayer::initUnit
- applyTheVedicAryans1  (EntryPoints/CvRandomEventInterface.py:2321)  <- py>cpp CyPlayer::initUnit
- doAssassinDiscovered3  (EntryPoints/CvRandomEventInterface.py:6914)  <- py>cpp CyPlayer::initUnit
- doSpyDiscovered3  (EntryPoints/CvRandomEventInterface.py:4001)  <- py>cpp CyPlayer::initUnit
- handleWorldBuilderDiplomacyVassalPullDownCB  (EntryPoints/CvScreensInterface.py:861)  <- py>py base/Screens/CvWorldBuilderDiplomacyScreen.py CvWorldBuilderDiplomacyScreen.handleVassalPullDownCB
- applyMapDesc  (EntryPoints/CvWBInterface.py:265)  <- py>py base/pyWB/CvWBDesc.py CvWBDesc.applyMap
- showUnitClass  (ModTools/ModTools.py:90)  <- py>cpp CyPlayer::initUnit
- PyCity.initUnit  (PyHelpers.py:620)  <- py>cpp CyPlayer::initUnit
- PyPlayer.initUnit  (PyHelpers.py:284)  <- py>cpp CyPlayer::initUnit
- updateGraphics  (Revolution/Development/ChangePlayer.py:170)  <- py>cpp CyGame::setAIAutoPlay
- Tester.waitingForHandler  (Revolution/Development/Tester.py:300)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.abdicate  (Revolution/Gameready/AIAutoPlay.py:581)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.disableMultiCheck  (Revolution/Gameready/AIAutoPlay.py:529)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.doCheckMultiplayerUpdate  (Revolution/Gameready/AIAutoPlay.py:387)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.onGameLoad  (Revolution/Gameready/AIAutoPlay.py:158)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.onKbdEvent  (Revolution/Gameready/AIAutoPlay.py:342)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.onModNetMessage  (Revolution/Gameready/AIAutoPlay.py:561)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.doNewHuman
- AIAutoPlay.onVictory  (Revolution/Gameready/AIAutoPlay.py:177)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.pickHumanHandler  (Revolution/Gameready/AIAutoPlay.py:227)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.doNewHuman
- BarbarianCiv.getScenario  (Revolution/Gameready/BarbarianCiv.py:209)  <- py>cpp CyGame::setAIAutoPlay
- BarbarianCiv.onBeginGameTurn  (Revolution/Gameready/BarbarianCiv.py:144)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.checkBarbCities
- BarbarianCiv.onCityAcquired  (Revolution/Gameready/BarbarianCiv.py:2017)  <- py>cpp CyPlayer::initUnit
- BarbarianCiv.onEndPlayerTurn  (Revolution/Gameready/BarbarianCiv.py:159)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.checkMinorCivs
- Revolution.doRevReinforcement  (Revolution/Gameready/Revolution.py:659)  <- py>cpp (name match) CyPlayer::initUnit
- Revolution.prepareRevolution  (Revolution/Gameready/Revolution.py:6137)  <- py>cpp (only target) CyUnit::setDamage
- Revolution.updatePlayerRevolution  (Revolution/Gameready/Revolution.py:1048)  <- py>py Revolution/Gameready/Revolution.py Revolution.checkForRevolution
- onSetPlayerAlive  (Revolution/Gameready/StartAsMinors.py:97)  <- py>cpp CyPlayer::initUnit
- TechDiffusion.onBeginGameTurn  (Revolution/Gameready/TechDiffusion.py:77)  <- py>py Revolution/Gameready/TechDiffusion.py TechDiffusion.diffuseTech
- checkRebelBonuses  (Revolution/RevEvents.py:451)  <- py>cpp CyPlayer::initUnit
- onSetPlayerAlive  (Revolution/RevEvents.py:196)  <- py>cpp CyGame::setAIAutoPlay
- giveCityCulture  (Revolution/RevUtils.py:903)  <- py>cpp (name match) CyPlot::setCulture
- giveRebelUnitFreePromotion  (Revolution/RevUtils.py:651)  <- py>cpp (only target) CyUnit::setHasPromotion
- RoMEventManager.onBeginPlayerTurn  (RoMEventManager.py:281)  <- py>cpp CyPlayer::initUnit
- CvMainInterface.updateScoreStrings  (Screens/CvMainInterface.py:5148)  <- py>py BUG/Scoreboard.py Scoreboard.addPlayer
- PLE.getPlotListButtonName  (Screens/PLE.py:815)  <- py>py Screens/PLE.py PLE.selectGroup
- CvDebugTools.putOneOfEveryUnit  (base/CvDebugTools.py:275)  <- py>cpp CyPlayer::initUnit
- CvEventManager.__eventPlaceObjectApply  (base/CvEventManager.py:990)  <- py>py base/CvDebugTools.py CvDebugTools.applyUnitPicker
- CvEventManager.onCityRazed  (base/CvEventManager.py:825)  <- py>cpp CyPlayer::initTriggeredData
- CvEventManager.onKbdEvent  (base/CvEventManager.py:218)  <- py>cpp CyUnit::setDamage
- emptyMap  (base/CvPerfTest.py:11)  <- py>py base/CvPerfTest.py CvFillMap.emptyMap
- fillMap  (base/CvPerfTest.py:7)  <- py>py base/CvPerfTest.py CvFillMap.fillMap
- CvWorldBuilderScreen.handleCityEditCultureCB  (base/Screens/CvWorldBuilderScreen.py:446)  <- py>cpp (name match) CyPlot::setCulture
- CvWorldBuilderScreen.handlePromotionCB  (base/Screens/CvWorldBuilderScreen.py:518)  <- py>cpp (only target) CyUnit::setHasPromotion
- CvWorldBuilderScreen.setAllPlots  (base/Screens/CvWorldBuilderScreen.py:414)  <- py>cpp CyMap::setAllPlotTypes
- CvWorldBuilderScreen.setEditButtonClicked  (base/Screens/CvWorldBuilderScreen.py:1650)  <- py>cpp (only target) CyUnit::setHasPromotion
- CvUnitDesc.apply  (base/pyWB/CvWBDesc.py:673)  <- py>cpp (name match) CyPlayer::initUnit

### level 7 (56)

- getPossibleEmbargos  (BUG/PlayerUtil.py:365)  <- py>cpp (only target) CyPlayer::canTradeItem
- getPossibleWars  (BUG/PlayerUtil.py:409)  <- py>cpp (only target) CyPlayer::canTradeItem
- isGivingFavoriteCivicDenial  (BUG/PlayerUtil.py:469)  <- py>cpp (only target) CyPlayer::canTradeItem
- isWHEOOH  (BUG/PlayerUtil.py:441)  <- py>cpp (only target) CyPlayer::canTradeItem
- getTradeableBonuses  (BUG/TradeUtil.py:328)  <- py>cpp (only target) CyPlayer::canTradeItem
- printStatus  (BUG/TradeUtil.py:715)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getDefensivePactTrades  (Contrib/MoreCiv4lerts.py:474)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getMapTrades  (Contrib/MoreCiv4lerts.py:450)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getOpenBordersTrades  (Contrib/MoreCiv4lerts.py:462)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getPeaceTrades  (Contrib/MoreCiv4lerts.py:522)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getPermanentAllianceTrades  (Contrib/MoreCiv4lerts.py:486)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getSurrenderTrades  (Contrib/MoreCiv4lerts.py:510)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getTechTrades  (Contrib/MoreCiv4lerts.py:428)  <- py>cpp (only target) CyPlayer::canTradeItem
- MoreCiv4lertsEvent.getVassalTrades  (Contrib/MoreCiv4lerts.py:498)  <- py>cpp (only target) CyPlayer::canTradeItem
- PickReligionPopup.__eventPickReligionApply  (Contrib/RevDCMReligionControl.py:225)  <- py>cpp CyPlayer::foundReligion
- PickReligionPopup.__eventPickReligionBegin  (Contrib/RevDCMReligionControl.py:189)  <- py>py Contrib/RevDCMReligionControl.py PickReligionPopup.launchPopup
- ReligionControl.doHolyCity  (Contrib/RevDCMReligionControl.py:28)  <- py>cpp CyPlayer::foundReligion
- CvAddBuilding  (CvUtil.py:114)  <- py>cpp (only target) CyCity::setNumRealBuilding
- CvEnhancedTechConquestEventManager.onCityAcquired  (EnhancedTechConquestUtils/CvEnhancedTechConquestEventManager.py:23)  <- py>py EnhancedTechConquestUtils/EnhancedTechConquest.py EnhancedTechConquest.onCityAcquired
- applyBlessedSea2  (EntryPoints/CvRandomEventInterface.py:82)  <- py>cpp (only target) CyCity::setNumRealBuilding
- applyCrusadeDone2  (EntryPoints/CvRandomEventInterface.py:2995)  <- py>cpp CyCity::setNumRealBuilding
- applyEarthDay2  (EntryPoints/CvRandomEventInterface.py:1507)  <- py>cpp CyPlayer::canTradeItem
- applyHurricane1  (EntryPoints/CvRandomEventInterface.py:618)  <- py>cpp CyCity::setNumRealBuilding
- applyLooters3  (EntryPoints/CvRandomEventInterface.py:507)  <- py>cpp CyCity::setNumRealBuilding
- applyTsunami2  (EntryPoints/CvRandomEventInterface.py:707)  <- py>cpp CyCity::setNumRealBuilding
- canApplyEarthDay2  (EntryPoints/CvRandomEventInterface.py:1485)  <- py>cpp CyPlayer::canTradeItem
- doWeddingFeud3  (EntryPoints/CvRandomEventInterface.py:325)  <- py>cpp CyTeam::declareWar
- weddingFeud3Callback  (EntryPoints/CvRandomEventInterface.py:357)  <- py>cpp CyTeam::declareWar
- WorldBuilderHandleCityEditCultureCB  (EntryPoints/CvScreensInterface.py:620)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleCityEditCultureCB
- WorldBuilderHandlePromotionCB  (EntryPoints/CvScreensInterface.py:653)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handlePromotionCB
- WorldBuilderOnWBEditBrushSelected  (EntryPoints/CvScreensInterface.py:711)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setEditButtonClicked
- PyCity.setNumRealBuildingIdx  (PyHelpers.py:694)  <- py>cpp CyCity::setNumRealBuilding
- ChangePlayer.onKbdEvent  (Revolution/Development/ChangePlayer.py:60)  <- py>py Revolution/Development/ChangePlayer.py updateGraphics
- updateGraphicsHandler  (Revolution/Development/ChangePlayer.py:165)  <- py>py Revolution/Development/ChangePlayer.py updateGraphics
- Tester.onBeginPlayerTurn  (Revolution/Development/Tester.py:214)  <- py>cpp CyTeam::declareWar
- AIAutoPlay.abdicateMultiCheck  (Revolution/Gameready/AIAutoPlay.py:537)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.abdicate
- AIAutoPlay.abdicateMultiCheckNoMessage  (Revolution/Gameready/AIAutoPlay.py:550)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.abdicate
- AIAutoPlay.onBeginGameTurn  (Revolution/Gameready/AIAutoPlay.py:408)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.doCheckMultiplayerUpdate
- AIAutoPlay.onGameStart  (Revolution/Gameready/AIAutoPlay.py:155)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.onGameLoad
- Revolution.checkForRevReinforcement  (Revolution/Gameready/Revolution.py:641)  <- py>py Revolution/Gameready/Revolution.py Revolution.doRevReinforcement
- init  (Revolution/Gameready/StartAsMinors.py:39)  <- py>py Revolution/Gameready/StartAsMinors.py onSetPlayerAlive
- onTechAcquired  (Revolution/Gameready/StartAsMinors.py:127)  <- py>cpp CyMap::verifyUnitValidPlot
- onCityAcquired  (Revolution/RevEvents.py:433)  <- py>py Revolution/RevEvents.py checkRebelBonuses
- updateRevolutionIndices  (Revolution/RevEvents.py:601)  <- py>cpp CyCity::setNumRealBuilding
- RoMEventManager.addCityBuildings  (RoMEventManager.py:238)  <- py>cpp CyCity::setNumRealBuilding
- CvExoticForeignAdvisor.drawTechDeals  (Screens/CvExoticForeignAdvisor.py:1336)  <- py>cpp CyPlayer::canTradeItem
- CvMainInterface._setScrollingScoreboard  (Screens/CvMainInterface.py:6438)  <- py>py Screens/CvMainInterface.py CvMainInterface.updateScoreStrings
- CvMainInterface.changeScoreboardDisplay  (Screens/CvMainInterface.py:6250)  <- py>py Screens/CvMainInterface.py CvMainInterface.updateScoreStrings
- CvMainInterface.redraw  (Screens/CvMainInterface.py:1405)  <- py>py Screens/CvMainInterface.py CvMainInterface.updateScoreStrings
- PLE.doPromotion  (Screens/PLE.py:1653)  <- py>cpp (only target) CyUnit::promote
- PLE.doUpgrade  (Screens/PLE.py:1706)  <- py>cpp (only target) CyUnit::doCommand
- CvDebugTools.allUnits  (base/CvDebugTools.py:256)  <- py>py base/CvDebugTools.py CvDebugTools.putOneOfEveryUnit
- CvWorldBuilderDiplomacyScreen.handleAtWarPullDownCB  (base/Screens/CvWorldBuilderDiplomacyScreen.py:368)  <- py>cpp CyTeam::declareWar
- CvWorldBuilderScreen.handleAllPlotsCB  (base/Screens/CvWorldBuilderScreen.py:363)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setAllPlots
- CvWorldBuilderScreen.handleEditCityBuildingCB  (base/Screens/CvWorldBuilderScreen.py:552)  <- py>cpp (only target) CyCity::setNumRealBuilding
- CvWorldBuilderScreen.setEditCorporationSelected  (base/Screens/CvWorldBuilderScreen.py:1684)  <- py>cpp (only target) CyCity::setHasCorporation

### level 8 (28)

- doUpdate  (Contrib/FavoriteCivicDetector.py:63)  <- py>py BUG/PlayerUtil.py isGivingFavoriteCivicDenial
- ReInitInterceptorMision.doReInit  (Contrib/MonkeyTools.py:41)  <- py>cpp (only target) CySelectionGroup::pushMission
- MoreCiv4lertsEvent.CheckForAlerts  (Contrib/MoreCiv4lerts.py:183)  <- py>py Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.getTechTrades
- MoreCiv4lertsEvent.getBonusTrades  (Contrib/MoreCiv4lerts.py:443)  <- py>py BUG/TradeUtil.py getTradeableBonuses
- AdjustBuilding  (CvUtil.py:379)  <- py>py PyHelpers.py PyCity.setNumRealBuildingIdx
- applyGeneralsPutsch3  (EntryPoints/CvRandomEventInterface.py:4470)  <- py>cpp CyPlayer::setCivics
- applyRubicon3  (EntryPoints/CvRandomEventInterface.py:4378)  <- py>cpp CyPlayer::setCivics
- doGreatMediator2  (EntryPoints/CvRandomEventInterface.py:1686)  <- py>cpp CyTeam::makePeace
- greatMediator2Callback  (EntryPoints/CvRandomEventInterface.py:1712)  <- py>cpp CyTeam::makePeace
- WorldBuilderHandleAllPlotsCB  (EntryPoints/CvScreensInterface.py:605)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleAllPlotsCB
- WorldBuilderHandleEditCityBuildingCB  (EntryPoints/CvScreensInterface.py:665)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleEditCityBuildingCB
- WorldBuilderOnAllPlotsBrushSelected  (EntryPoints/CvScreensInterface.py:741)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleAllPlotsCB
- WorldBuilderOnWBEditCorporationSelected  (EntryPoints/CvScreensInterface.py:729)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setEditCorporationSelected
- forceScreenRedraw  (EntryPoints/CvScreensInterface.py:972)  <- py>py Screens/CvMainInterface.py CvMainInterface.redraw
- handleWorldBuilderDiplomacyAtWarPullDownCB  (EntryPoints/CvScreensInterface.py:864)  <- py>py base/Screens/CvWorldBuilderDiplomacyScreen.py CvWorldBuilderDiplomacyScreen.handleAtWarPullDownCB
- AIAutoPlay.AIChooserHandler  (Revolution/Gameready/AIAutoPlay.py:478)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.abdicateMultiCheck
- Revolution.controlLostNetworkHandler  (Revolution/Gameready/Revolution.py:5932)  <- py>py (only target) Revolution/Gameready/AIAutoPlay.py AIAutoPlay.abdicateMultiCheckNoMessage
- Revolution.onBeginPlayerTurn  (Revolution/Gameready/Revolution.py:555)  <- py>py Revolution/Gameready/Revolution.py Revolution.checkForRevReinforcement
- RevolutionInit.onGameLoad  (Revolution/RevolutionInit.py:98)  <- py>py Revolution/Gameready/StartAsMinors.py init
- RoMEventManager.onModNetMessage  (RoMEventManager.py:151)  <- py>py RoMEventManager.py RoMEventManager.addCityBuildings
- CvMilitaryAdvisor.showSituationReport  (Screens/CvBUGMilitaryAdvisor.py:257)  <- py>py BUG/PlayerUtil.py getPossibleEmbargos
- CvMainInterface.handleInput  (Screens/CvMainInterface.py:6262)  <- py>py Screens/CvMainInterface.py CvMainInterface.changeScoreboardDisplay
- CvMainInterface.setScrollingScoreboard  (Screens/CvMainInterface.py:6432)  <- py>py Screens/CvMainInterface.py CvMainInterface._setScrollingScoreboard
- PLE.unitPromotion  (Screens/PLE.py:766)  <- py>py Screens/PLE.py PLE.doPromotion
- PLE.unitUpgrade  (Screens/PLE.py:837)  <- py>py Screens/PLE.py PLE.doUpgrade
- CvEventManager.__eventWBAllPlotsPopupApply  (base/CvEventManager.py:1033)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleAllPlotsCB
- CvWorldBuilderDiplomacyScreen.handleAIWeightResetAll  (base/Screens/CvWorldBuilderDiplomacyScreen.py:380)  <- py>cpp CyTeam::makePeace
- CvWorldBuilderScreen.setEditHeadquartersSelected  (base/Screens/CvWorldBuilderScreen.py:1694)  <- py>cpp CyGame::setHeadquarters

### level 9 (23)

- FavoriteCivicDetector.onBeginActivePlayerTurn  (Contrib/FavoriteCivicDetector.py:300)  <- py>py Contrib/FavoriteCivicDetector.py doUpdate
- MoreCiv4lertsEvent.OnCityAcquired  (Contrib/MoreCiv4lerts.py:142)  <- py>py Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.CheckForAlerts
- MoreCiv4lertsEvent.OnCityBuilt  (Contrib/MoreCiv4lerts.py:149)  <- py>py Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.CheckForAlerts
- MoreCiv4lertsEvent.OnCityLost  (Contrib/MoreCiv4lerts.py:176)  <- py>py Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.CheckForAlerts
- MoreCiv4lertsEvent.OnCityRazed  (Contrib/MoreCiv4lerts.py:170)  <- py>py Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.CheckForAlerts
- MoreCiv4lertsEvent.onBeginActivePlayerTurn  (Contrib/MoreCiv4lerts.py:136)  <- py>py Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.CheckForAlerts
- SevoPediaBonus.placeSpecial  (Contrib/Sevopedia/SevoPediaBonus.py:153)  <- py>cpp CyGameTextMgr::getBonusHelp
- SevoPediaTech.placeSpecial  (Contrib/Sevopedia/SevoPediaTech.py:209)  <- py>cpp CyGameTextMgr::getTechHelp
- CvTechSplashScreen.interfaceScreen  (Contrib/TechWindow.py:111)  <- py>cpp CyGameTextMgr::getTechHelp
- CvTechSplashScreen.interfaceScreen  (Contrib/TechWindowWide.py:116)  <- py>cpp CyGameTextMgr::getTechHelp
- WorldBuilderOnWBEditHeadquartersSelected  (EntryPoints/CvScreensInterface.py:735)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setEditHeadquartersSelected
- handleWorldBuilderDiplomacyAIWeightResetAllCB  (EntryPoints/CvScreensInterface.py:870)  <- py>py base/Screens/CvWorldBuilderDiplomacyScreen.py CvWorldBuilderDiplomacyScreen.handleAIWeightResetAll
- doSmallRevolts  (Revolution/RevEvents.py:1173)  <- py>cpp (only target) CyCity::setOccupationTimer
- onChangeWar  (Revolution/RevEvents.py:302)  <- py>cpp (only target) CyCity::setOccupationTimer
- RevolutionInit.__init__  (Revolution/RevolutionInit.py:47)  <- py>py Revolution/RevolutionInit.py RevolutionInit.onGameLoad
- RevolutionInit.onGameStart  (Revolution/RevolutionInit.py:92)  <- py>py Revolution/RevolutionInit.py RevolutionInit.onGameLoad
- CvMilitaryAdvisor.handleInput  (Screens/CvBUGMilitaryAdvisor.py:1178)  <- py>py Screens/CvBUGMilitaryAdvisor.py CvMilitaryAdvisor.showSituationReport
- CvMilitaryAdvisor.interfaceScreen  (Screens/CvBUGMilitaryAdvisor.py:179)  <- py>py Screens/CvBUGMilitaryAdvisor.py CvMilitaryAdvisor.showSituationReport
- CvExoticForeignAdvisor.drawInfoImproved  (Screens/CvExoticForeignAdvisor.py:525)  <- py>py Contrib/FavoriteCivicDetector.py doUpdate
- CvPediaBonus.placeSpecial  (base/Screens/CvPediaBonus.py:190)  <- py>cpp CyGameTextMgr::getBonusHelp
- CvPediaTech.placeSpecial  (base/Screens/CvPediaTech.py:240)  <- py>cpp CyGameTextMgr::getTechHelp
- CvTechSplashScreen.interfaceScreen  (base/Screens/CvTechSplashScreen.py:92)  <- py>cpp CyGameTextMgr::getTechHelp
- CvWBPopups.applyEditCity  (base/pyWB/CvWBPopups.py:104)  <- py>py CvUtil.py AdjustBuilding

### level 10 (10)

- SevoPediaBonus.interfaceScreen  (Contrib/Sevopedia/SevoPediaBonus.py:85)  <- py>py Contrib/Sevopedia/SevoPediaBonus.py SevoPediaBonus.placeSpecial
- SevoPediaTech.interfaceScreen  (Contrib/Sevopedia/SevoPediaTech.py:82)  <- py>py Contrib/Sevopedia/SevoPediaTech.py SevoPediaTech.placeSpecial
- PyCity.changeCulture  (PyHelpers.py:595)  <- py>cpp CyCity::changeCulture
- PyCity.setCulture  (PyHelpers.py:598)  <- py>cpp CyCity::setCulture
- onEndPlayerTurn  (Revolution/RevEvents.py:166)  <- py>py Revolution/RevEvents.py doSmallRevolts
- changeCiv  (Revolution/RevUtils.py:1107)  <- py>cpp CyPlayer::changeCiv
- CvExoticForeignAdvisor.drawInfo  (Screens/CvExoticForeignAdvisor.py:456)  <- py>py Screens/CvExoticForeignAdvisor.py CvExoticForeignAdvisor.drawInfoImproved
- CvEventManager.__eventEditCityApply  (base/CvEventManager.py:981)  <- py>py base/pyWB/CvWBPopups.py CvWBPopups.applyEditCity
- CvPediaBonus.interfaceScreen  (base/Screens/CvPediaBonus.py:79)  <- py>py base/Screens/CvPediaBonus.py CvPediaBonus.placeSpecial
- CvPediaTech.interfaceScreen  (base/Screens/CvPediaTech.py:67)  <- py>py base/Screens/CvPediaTech.py CvPediaTech.placeSpecial

### level 11 (3)

- onBeginPlayerTurn  (Contrib/RevDCMReligionControl.py:87)  <- py>cpp CyGame::setWinner
- changeCivHandler  (Revolution/Development/ChangePlayer.py:133)  <- py>py Revolution/RevUtils.py changeCiv
- CvPediaMain.pediaJump  (Screens/CvPediaMain.py:900)  <- py>py base/Screens/CvPediaBonus.py CvPediaBonus.interfaceScreen

### level 12 (4)

- CvPediaMain.back  (Screens/CvPediaMain.py:948)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump
- CvPediaMain.forward  (Screens/CvPediaMain.py:955)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump
- CvPediaMain.link  (Screens/CvPediaMain.py:974)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump
- CvPediaMain.pediaShow  (Screens/CvPediaMain.py:961)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump

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
