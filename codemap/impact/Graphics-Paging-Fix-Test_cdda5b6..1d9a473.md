# Impact of cdda5b65d3da..1d9a473e5d53

Commits:

- 1d9a473 2026-11-22 Memory fixes; Also trade in the diplomacy screen reworked
- 69955ed 2026-11-22 Memory fixes

```
 Assets/CvGameCoreDLL/CvCity.cpp     |  17 ++-
 Assets/CvGameCoreDLL/CvGame.cpp     | 242 ++++++++++++++++++++++++++++++++----
 Assets/CvGameCoreDLL/CvGame.h       |   5 +
 Assets/CvGameCoreDLL/CvPlayerAI.cpp | 198 +++++++++++++++++++++++------
 Assets/CvGameCoreDLL/CvPlayerAI.h   |   5 +
 Assets/CvGameCoreDLL/CvPlot.cpp     |  16 ++-
 Assets/CvGameCoreDLL/CvUnit.cpp     |  14 ++-
 Assets/XML/GlobalDefinesAlt.xml     |  66 +++++++++-
 8 files changed, 495 insertions(+), 68 deletions(-)
```
_Members, XML fills and defines at 1d9a473e5d53: the map's clang tables (exact)._

## C++ functions

- changed: 13; added: 5; removed: 0
  - changed CvCity::canPageGraphicsOut  (CvCity.cpp:764-779)
  - changed CvGame::reset  (CvGame.cpp:482-730)
  - changed CvGame::endBulkReveal  (CvGame.cpp:2312-2342)
  - changed CvGame::updateGraphicsPaging  (CvGame.cpp:2508-2679)
  - changed CvGame::pageGraphics  (CvGame.cpp:2817-3094)
  - changed CvPlayerAI::AI_considerOffer  (CvPlayerAI.cpp:8989-9128)
  - changed CvPlayerAI::AI_counterPropose  (CvPlayerAI.cpp:9131-9720)
  - changed CvPlayerAI::AI_doDiplo  (CvPlayerAI.cpp:17344-19308)
  - changed CvPlot::refreshRevealedGraphics  (CvPlot.cpp:305-339)
  - changed CvPlot::updateFeatureSymbolEntity  (CvPlot.cpp:8122-8165)
  - changed CvPlot::updateRouteSymbol  (CvPlot.cpp:8175-8227)
  - changed CvPlot::updatePlotBuilder  (CvPlot.cpp:9728-9746)
  - changed CvUnit::canPageGraphicsOut  (CvUnit.cpp:464-480)
  - added CvGame::updateGraphicsMemoryPressure  (CvGame.cpp:2416-2506)
  - added CvPlayerAI::AI_tradeGiveVal  (CvPlayerAI.cpp:8914-8944)
  - added CvPlayerAI::AI_dealNetVal  (CvPlayerAI.cpp:8946-8952)
  - added CvPlayerAI::AI_isMutuallyBeneficialDeal  (CvPlayerAI.cpp:8954-8961)
  - added CvPlayerAI::AI_goldPerTurnCostVal  (CvPlayerAI.cpp:9789-9810)

## Member declarations

- added CvGame::m_dwGraphicsMemorySampleTime DWORD
- added CvGame::m_iGraphicsMemoryAvailMB int
- added CvGame::m_iGraphicsMemoryPressure int
- added CvGame::m_iGraphicsMemoryRecoverySamples int

## Members written on changed lines, or declared new

CvGame::m_bPagingPending, CvGame::m_dwGraphicsMemorySampleTime, CvGame::m_iGraphicsMemoryAvailMB, CvGame::m_iGraphicsMemoryPressure, CvGame::m_iGraphicsMemoryRecoverySamples

## Defines read on changed lines

GRAPHICS_PAGING_ACTIVE_CITIES, GRAPHICS_PAGING_ACTIVE_UNITS, GRAPHICS_PAGING_CRITICAL_SELECTED_IN, GRAPHICS_PAGING_LOG, GRAPHICS_PAGING_MAX_IN, GRAPHICS_PAGING_MEMORY_CONSERVE_MAX_IN, GRAPHICS_PAGING_MEMORY_CONSERVE_MB, GRAPHICS_PAGING_MEMORY_CONTROL, GRAPHICS_PAGING_MEMORY_CRITICAL_MB, GRAPHICS_PAGING_MEMORY_RECOVER_MB, GRAPHICS_PAGING_MEMORY_RECOVER_SAMPLES, GRAPHICS_PAGING_PRESSURE_RANGE_NORTH, GRAPHICS_PAGING_PRESSURE_RANGE_SOUTH, GRAPHICS_PAGING_PRESSURE_RANGE_X, PEACE_TREATY_LENGTH

## XML

- GlobalDefinesAlt.xml: tags on changed lines: none; defines: GRAPHICS_PAGING_ACTIVE_CITIES, GRAPHICS_PAGING_ACTIVE_UNITS, GRAPHICS_PAGING_CRITICAL_SELECTED_IN, GRAPHICS_PAGING_MARGIN, GRAPHICS_PAGING_MAX_IN, GRAPHICS_PAGING_MAX_OUT, GRAPHICS_PAGING_MEMORY_CONSERVE_MAX_IN, GRAPHICS_PAGING_MEMORY_CONSERVE_MB, GRAPHICS_PAGING_MEMORY_CONTROL, GRAPHICS_PAGING_MEMORY_CRITICAL_MB, GRAPHICS_PAGING_MEMORY_RECOVER_MB, GRAPHICS_PAGING_MEMORY_RECOVER_SAMPLES, GRAPHICS_PAGING_PRESSURE_RANGE_NORTH, GRAPHICS_PAGING_PRESSURE_RANGE_SOUTH, GRAPHICS_PAGING_PRESSURE_RANGE_X, GRAPHICS_PAGING_REVEAL_MAX, GRAPHICS_PAGING_SYMBOLS

## Reach

| | start | reached | per level |
|---|---|---|---|
| member variables | 5 | 0 |  |
| C++ functions | 18 | 971 | 1: 30, 2: 61, 3: 139, 4: 178, 5: 144, 6: 108, 7: 219, 8: 45, 9: 21, 10: 16, 11: 8, 12: 1, 13: 1 |
| Python functions | 0 | 335 | 3: 10, 4: 41, 5: 96, 6: 45, 7: 61, 8: 36, 9: 26, 10: 9, 11: 3, 12: 8 |
| defines | 19 | 0 |  |

- C++ functions the exe calls (exported): 120: CvCity::cheat, CvDLLButtonPopup::OnOkClicked, CvDLLButtonPopup::launchButtonPopup, CvDLLWidgetData::executeAction, CvDLLWidgetData::isLink, CvDLLWidgetData::parseHelp, CvDeal::isCancelable, CvDeal::kill, CvDeal::turnsToCancel, CvEventReporter::gameStart, CvEventReporter::kbdEvent, CvEventReporter::reportModNetMessage, CvGame::CvGame, CvGame::cheatSpaceship, CvGame::implementDeal, CvGame::init, CvGame::initDiplomacy, CvGame::initFreeState, CvGame::initFreeUnits, CvGame::nextActivePlayer, CvGame::normalizeStartingPlots, CvGame::read, CvGame::regenerateMap, CvGame::reset, CvGame::reviveActivePlayer, CvGame::revivePlayer, CvGame::setAIAutoPlay, CvGame::setActivePlayer, CvGame::setFinalInitialized, CvGame::setInitialItems, CvGame::setVoteChosen, CvGame::toggleDebugMode, CvGame::update, CvGame::updateCitySight, CvGameTextMgr::getActiveDealsString, CvGameTextMgr::getBonusDataForWB, CvGameTextMgr::getDealString, CvGameTextMgr::getTechDataForWB, CvGameTextMgr::getTradeString, CvGameTextMgr::getTurnTimerText, CvGameTextMgr::parseLeaderHeadHelp, CvGameTextMgr::setBonusHelp, CvGameTextMgr::setBonusTradeHelp, CvGameTextMgr::setTechHelp, CvGameTextMgr::setTechTradeHelp, CvGlobals::init, CvMap::erasePlots, CvMap::init, CvMap::read, CvMap::setupGraphical, CvMap::updateFlagSymbols, CvMap::updateVisibility, CvMapGenerator::addBonuses, CvMapGenerator::addFeatures, CvMapGenerator::addGameElements, CvMapGenerator::addGoodies, CvMapGenerator::addRivers, CvMapGenerator::eraseBonuses, CvMapGenerator::eraseFeatures, CvMapGenerator::eraseGoodies, CvMapGenerator::eraseRivers, CvMapGenerator::generateRandomMap, CvNetAdvancedStartAction::Execute, CvNetAutoMission::Execute, CvNetAutoMoves::Execute, CvNetChangeVassal::Execute, CvNetChangeWar::Execute, CvNetChooseElection::Execute, CvNetConvert::Execute, CvNetDoCommand::Execute, CvNetDoTask::Execute, CvNetEmpireSplit::Execute, CvNetEventTriggered::Execute, CvNetFoundReligion::Execute, CvNetJoinGroup::Execute, CvNetModNetMessage::Execute, CvNetPopOrder::Execute, CvNetPushMission::Execute, CvNetPushOrder::Execute, CvNetResearch::Execute, CvNetTurnComplete::Execute, CvNetUpdateCivics::Execute, CvPlayer::applyEvent, CvPlayer::buildTradeTable, CvPlayer::canTradeItem, CvPlayer::cheat, CvPlayer::convert, CvPlayer::doAdvancedStartAction, CvPlayer::foundReligion, CvPlayer::getGlobeLayerColors, CvPlayer::getItemTradeString, CvPlayer::handleDiploEvent, CvPlayer::init, CvPlayer::revolution, CvPlayer::setAutoMoves, CvPlayer::setEndTurn, CvPlayer::setLoyalMember, CvPlayer::setTurnActive, CvPlayer::setupGraphical, CvPlayer::splitEmpire, CvPlayerAI::AI_maxGoldPerTurnTrade, CvPlot::erase, CvPlot::setFeatureType, CvPlot::setImprovementType, CvPlot::setLayoutDirty, CvPlot::setNOfRiver, CvPlot::setRevealed, CvPlot::setRouteType, CvPlot::setWOfRiver, CvPlot::updateFlagSymbol, CvSelectionGroup::autoMission, CvSelectionGroup::clearUnits, CvSelectionGroup::deleteUnitNode, CvSelectionGroup::pushMission, CvTeam::declareWar, CvTeam::init, CvTeam::makePeace, CvUnit::cheat, CvUnit::joinGroup, DLLPublishToPython
- C++ functions bound for Python: 170: CyCity::addProductionExperience, CyCity::alterSpecialistCount, CyCity::alterWorkingPlot, CyCity::changeCulture, CyCity::changeCultureTimes100, CyCity::changeOccupationTimer, CyCity::clearOrderQueue, CyCity::clearWorkingOverride, CyCity::conscript, CyCity::createGreatPeople, CyCity::doTask, CyCity::kill, CyCity::liberate, CyCity::popOrder, CyCity::pushOrder, CyCity::setCitizensAutomated, CyCity::setCulture, CyCity::setCultureTimes100, CyCity::setHasCorporation, CyCity::setNumRealBuilding, CyCity::setOccupationTimer, CyCity::setProductionAutomated, CyDeal::getCannotCancelReason, CyDeal::isCancelable, CyDeal::kill, CyDeal::turnsToCancel, CyGame::addPlayer, CyGame::changeHumanPlayer, CyGame::clearHeadquarters, CyGame::regenerateMap, CyGame::reviveActivePlayer, CyGame::setAIAutoPlay, CyGame::setActivePlayer, CyGame::setHeadquarters, CyGame::setWinner, CyGame::toggleDebugMode, CyGameTextMgr::getActiveDealsString, CyGameTextMgr::getBonusHelp, CyGameTextMgr::getDealString, CyGameTextMgr::getTechHelp, CyGameTextMgr::getTradeString, CyMap::erasePlots, CyMap::rebuild, CyMap::recalculateAreas, CyMap::regenerateGameElements, CyMap::setAllPlotTypes, CyMap::setRevealedPlots, CyMap::updateVisibility, CyMap::verifyUnitValidPlot, CyMapGenerator::addBonuses, CyMapGenerator::addFeatures, CyMapGenerator::addGameElements, CyMapGenerator::addGoodies, CyMapGenerator::addLakes, CyMapGenerator::addNonUniqueBonusType, CyMapGenerator::addRivers, CyMapGenerator::addUniqueBonusType, CyMapGenerator::doRiver, CyMapGenerator::eraseBonuses, CyMapGenerator::eraseFeatures, CyMapGenerator::eraseGoodies, CyMapGenerator::eraseRivers, CyMapGenerator::generatePlotTypes, CyMapGenerator::generateRandomMap, CyMapGenerator::generateTerrain, CyMapGenerator::setPlotTypes, CyPlayer::AI_maxGoldPerTurnTrade, CyPlayer::acquireCity, CyPlayer::assimilatePlayer, CyPlayer::canStopTradingWithTeam, CyPlayer::canTradeItem, CyPlayer::changeCiv, CyPlayer::changeCombatExperience, CyPlayer::convert, CyPlayer::createGreatPeople, CyPlayer::disband, CyPlayer::disbandUnit, CyPlayer::doEspionageMission, CyPlayer::doGoody, CyPlayer::findNewCapital, CyPlayer::forcePeace, CyPlayer::found, CyPlayer::foundCorporation, CyPlayer::foundReligion, CyPlayer::initCity, CyPlayer::initTriggeredData, CyPlayer::initUnit, CyPlayer::killAllDeals, CyPlayer::killCities, CyPlayer::killUnits, CyPlayer::raze, CyPlayer::receiveGoody, CyPlayer::removeBuildingClass, CyPlayer::revolution, CyPlayer::setAlive, CyPlayer::setCivics, CyPlayer::setCombatExperience, CyPlayer::setCurrentEra, CyPlayer::setLastStateReligion, CyPlayer::setLoyalMember, CyPlayer::setNewPlayerAlive, CyPlayer::splitEmpire, CyPlayer::stopTradingWithTeam, CyPlayer::trigger, CyPlot::changeBuildProgress, CyPlot::changeCulture, CyPlot::changeVisibilityCount, CyPlot::erase, CyPlot::nukeExplosion, CyPlot::removeGoody, CyPlot::setBonusType, CyPlot::setCulture, CyPlot::setFeatureType, CyPlot::setImprovementType, CyPlot::setNOfRiver, CyPlot::setOwner, CyPlot::setOwnerNoUnitCheck, CyPlot::setPlotType, CyPlot::setRevealed, CyPlot::setRouteType, CyPlot::setTerrainType, CyPlot::setWOfRiver, CyPlot::updateVisibility, CySelectionGroup::clearMissionQueue, CySelectionGroup::popMission, CySelectionGroup::pushMission, CySelectionGroup::pushMoveToMission, CySelectionGroup::setActivityType, CySelectionGroup::setAutomateType, CyTeam::addTeam, CyTeam::assignVassal, CyTeam::changeEspionagePointsAgainstTeam, CyTeam::changeExtraWaterSeeFromCount, CyTeam::changeIrrigationCount, CyTeam::changeProjectCount, CyTeam::changeResearchProgress, CyTeam::changeTechShareCount, CyTeam::declareWar, CyTeam::freeVassal, CyTeam::makePeace, CyTeam::meet, CyTeam::setEspionagePointsAgainstTeam, CyTeam::setHasTech, CyTeam::setIsMinorCiv, CyTeam::setResearchProgress, CyTeam::setVassal, CyTeam::signDefensivePact, CyTeam::signOpenBorders, CyUnit::attackForDamage, CyUnit::changeDamage, CyUnit::changeExperience, CyUnit::convert, CyUnit::doCommand, CyUnit::gift, CyUnit::giveExperience, CyUnit::jumpToNearestValidPlot, CyUnit::kill, CyUnit::lead, CyUnit::promote, CyUnit::rangeStrike, CyUnit::rotateFacingDirectionClockwise, CyUnit::rotateFacingDirectionCounterClockwise, CyUnit::setDamage, CyUnit::setHasPromotion, CyUnit::setLeaderUnitType, CyUnit::setPromotionReady, CyUnit::setReconPlot, CyUnit::setTransportUnit, CyUnit::setUnitAIType, CyUnit::setXY
- Python event handlers: 36: AIAutoPlay.onBeginGameTurn (BeginGameTurn), AIAutoPlay.onEndPlayerTurn (EndPlayerTurn), AIAutoPlay.onGameStart (GameStart), AIAutoPlay.onKbdEvent (kbdEvent), AIAutoPlay.onModNetMessage (ModNetMessage), AIAutoPlay.onVictory (victory), BarbarianCiv.onBeginGameTurn (BeginGameTurn), BarbarianCiv.onCityAcquired (cityAcquired), BarbarianCiv.onEndPlayerTurn (EndPlayerTurn), ChangePlayer.onKbdEvent (kbdEvent), CvEnhancedTechConquestEventManager.onCityAcquired (cityAcquired), CvEventManager.onCityRazed (cityRazed), CvEventManager.onKbdEvent (kbdEvent), MoreCiv4lertsEvent.OnCityAcquired (cityAcquired), MoreCiv4lertsEvent.OnCityBuilt (cityBuilt), MoreCiv4lertsEvent.OnCityLost (cityLost), MoreCiv4lertsEvent.OnCityRazed (cityRazed), Revolution.onBeginPlayerTurn (BeginPlayerTurn), Revolution.onEndPlayerTurn (EndPlayerTurn), Revolution.onModNetMessage (ModNetMessage), RevolutionInit.onGameStart (GameStart), RoMEventManager.onBeginPlayerTurn (BeginPlayerTurn), RoMEventManager.onBuildingBuilt (buildingBuilt), RoMEventManager.onCityLost (cityLost), RoMEventManager.onModNetMessage (ModNetMessage), RoMEventManager.onProjectBuilt (projectBuilt), TechDiffusion.onBeginGameTurn (BeginGameTurn), Tester.onBeginPlayerTurn (BeginPlayerTurn), onBeginPlayerTurn (BeginPlayerTurn), onChangeWar (changeWar), onCityAcquired (cityAcquired), onEndGameTurn (EndGameTurn), onEndPlayerTurn (EndPlayerTurn), onSetPlayerAlive (setPlayerAlive), onSetPlayerAlive (setPlayerAlive), onTechAcquired (techAcquired)
- C++ files: CvUnitAI.cpp 169, CvUnit.cpp 97, CvPlayer.cpp 78, CvGame.cpp 69, CvPlot.cpp 51, CvCity.cpp 50, CvPlayerAI.cpp 42, CvTeam.cpp 39, CyPlayer.cpp 38, CvSelectionGroup.cpp 33, CvCityAI.cpp 23, CyUnit.cpp 22, CyCity.cpp 22, CvMessageData.cpp 20, CyPlot.cpp 19, CyTeam.cpp 19, CvMapGenerator.cpp 18, CvDLLWidgetData.cpp 17, CvMap.cpp 17, CyMapGenerator.cpp 17, CvDllPythonEvents.cpp 17, CvEventReporter.cpp 17, CvGameTextMgr.cpp 13, CvDeal.cpp 10, CyGame.cpp 10, CyMap.cpp 8, CvSelectionGroupAI.cpp 7, CySelectionGroup.cpp 6, CyGameTextMgr.cpp 5, CyDeal.cpp 4, CvTeamAI.cpp 4, CvDLLButtonPopup.cpp 3, CvGameAI.cpp 3, CvGameCoreUtils.cpp 3, FFreeListTrashArray.h 2, CvGameInterface.cpp 2, CvArea.cpp 2, CvGlobals.cpp 1, CyPlotInterface1.cpp 1, CyGameInterface.cpp 1, CyGameTextMgrInterface.cpp 1, CyPlayerInterface2.cpp 1, CyUnitInterface1.cpp 1, CyMapInterface.cpp 1, CyMapGeneratorInterface.cpp 1, CvDLLPython.cpp 1, CyPlayerInterface1.cpp 1, CyCityInterface1.cpp 1, CyTeamInterface.cpp 1, CySelectionGroupInterface.cpp 1
- Python modules: EntryPoints/CvRandomEventInterface.py 61, base/Screens/CvWorldBuilderScreen.py 32, EntryPoints/CvScreensInterface.py 20, Revolution/Gameready/Revolution.py 17, Revolution/Gameready/AIAutoPlay.py 15, Contrib/MoreCiv4lerts.py 15, Revolution/Gameready/BarbarianCiv.py 12, Revolution/RevEvents.py 11, Revolution/RevUtils.py 9, Screens/PLE.py 7, PyHelpers.py 7, base/pyWB/CvWBDesc.py 6, Screens/CvForeignAdvisor.py 6, CvMapGeneratorUtil.py 6, RoMEventManager.py 6, base/CvDebugTools.py 6, base/CvEventManager.py 6, Screens/CvMainInterface.py 6, Screens/CvExoticForeignAdvisor.py 5, ModTools/ModTools.py 5, base/CvPerfTest.py 5, Revolution/Development/ChangePlayer.py 5, Contrib/RevDCMReligionControl.py 5, Screens/CvPediaMain.py 5, BUG/DealUtil.py 4, BUG/PlayerUtil.py 4, EntryPoints/CvWBInterface.py 3, Revolution/Gameready/StartAsMinors.py 3, CvUtil.py 3, base/Screens/CvWorldBuilderDiplomacyScreen.py 3, Revolution/RevolutionInit.py 3, Screens/CvBUGMilitaryAdvisor.py 3, Contrib/MapFinder.py 2, Revolution/Gameready/TechDiffusion.py 2, Revolution/Development/Tester.py 2, BUG/TradeUtil.py 2, Contrib/FavoriteCivicDetector.py 2, Contrib/Sevopedia/SevoPediaBonus.py 2, base/Screens/CvPediaBonus.py 2, Contrib/Sevopedia/SevoPediaTech.py 2, base/Screens/CvPediaTech.py 2, Contrib/Civ4lerts.py 1, ModTools/ModToolsUtils.py 1, AbandonCityEventManager.py 1, base/CvCameraControls.py 1, BUG/Scoreboard.py 1, base/EntryPoints/CvGameInterface.py 1, EnhancedTechConquestUtils/EnhancedTechConquest.py 1, Contrib/MonkeyTools.py 1, EnhancedTechConquestUtils/CvEnhancedTechConquestEventManager.py 1, base/pyWB/CvWBPopups.py 1, Contrib/TechWindow.py 1, Contrib/TechWindowWide.py 1, base/Screens/CvTechSplashScreen.py 1

## Member variables (5)

- CvGame::m_bPagingPending (CvGame.h:685): bool
- CvGame::m_dwGraphicsMemorySampleTime (CvGame.h:690): DWORD
- CvGame::m_iGraphicsMemoryAvailMB (CvGame.h:688): int
- CvGame::m_iGraphicsMemoryPressure (CvGame.h:687): int
- CvGame::m_iGraphicsMemoryRecoverySamples (CvGame.h:689): int

## XML tags and defines

- define GRAPHICS_PAGING_ACTIVE_CITIES: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_ACTIVE_UNITS: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_CRITICAL_SELECTED_IN: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_LOG: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MARGIN: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MAX_IN: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MAX_OUT: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MEMORY_CONSERVE_MAX_IN: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MEMORY_CONSERVE_MB: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MEMORY_CONTROL: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MEMORY_CRITICAL_MB: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MEMORY_RECOVER_MB: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_MEMORY_RECOVER_SAMPLES: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_PRESSURE_RANGE_NORTH: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_PRESSURE_RANGE_SOUTH: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_PRESSURE_RANGE_X: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_REVEAL_MAX: GlobalDefinesAlt.xml [mod]
- define GRAPHICS_PAGING_SYMBOLS: GlobalDefinesAlt.xml [mod]
- define PEACE_TREATY_LENGTH: GlobalDefines.xml [mod]

## C++ functions, level by level


### level 0 (18)

- CvCity::canPageGraphicsOut  (CvCity.cpp:765)
- CvGame::endBulkReveal  (CvGame.cpp:2313)
- CvGame::pageGraphics  (CvGame.cpp:2818)
- CvGame::reset  (CvGame.cpp:483)
- CvGame::updateGraphicsMemoryPressure  (CvGame.cpp:2417)
- CvGame::updateGraphicsPaging  (CvGame.cpp:2509)
- CvPlayerAI::AI_considerOffer  (CvPlayerAI.cpp:8990)
- CvPlayerAI::AI_counterPropose  (CvPlayerAI.cpp:9132)
- CvPlayerAI::AI_dealNetVal  (CvPlayerAI.cpp:8947)
- CvPlayerAI::AI_doDiplo  (CvPlayerAI.cpp:17345)
- CvPlayerAI::AI_goldPerTurnCostVal  (CvPlayerAI.cpp:9790)
- CvPlayerAI::AI_isMutuallyBeneficialDeal  (CvPlayerAI.cpp:8955)
- CvPlayerAI::AI_tradeGiveVal  (CvPlayerAI.cpp:8915)
- CvPlot::refreshRevealedGraphics  (CvPlot.cpp:306)
- CvPlot::updateFeatureSymbolEntity  (CvPlot.cpp:8123)
- CvPlot::updatePlotBuilder  (CvPlot.cpp:9729)
- CvPlot::updateRouteSymbol  (CvPlot.cpp:8176)
- CvUnit::canPageGraphicsOut  (CvUnit.cpp:465)

### level 1 (30)

- CvCity::pageGraphics  (CvCity.cpp:784)  <- call CvCity::canPageGraphicsOut
- CvCity::setWorkingPlot  (CvCity.cpp:11944)  <- call CvPlot::updatePlotBuilder
- CvCity::setupGraphical  (CvCity.cpp:738)  <- call CvCity::canPageGraphicsOut
- CvDLLButtonPopup::OnOkClicked  (CvDLLButtonPopup.cpp:75)  <- call CvPlayerAI::AI_considerOffer
- CvDLLWidgetData::parseTradeItem  (CvDLLWidgetData.cpp:4631)  <- define PEACE_TREATY_LENGTH
- CvDeal::doTurn  (CvDeal.cpp:298)  <- define PEACE_TREATY_LENGTH
- CvDeal::startTrade  (CvDeal.cpp:696)  <- call CvGame::endBulkReveal
- CvDeal::turnsToCancel  (CvDeal.cpp:1299)  <- define PEACE_TREATY_LENGTH
- CvGame::CvGame  (CvGame.cpp:50)  <- call CvGame::reset
- CvGame::init  (CvGame.cpp:108)  <- call CvGame::reset
- CvGame::processDeferredReveals  (CvGame.cpp:2362)  <- call CvPlot::refreshRevealedGraphics
- CvGame::read  (CvGame.cpp:9169)  <- call CvGame::reset
- CvGame::update  (CvGame.cpp:2175)  <- call CvGame::updateGraphicsPaging
- CvGameTextMgr::getTradeString  (CvGameTextMgr.cpp:15442)  <- define PEACE_TREATY_LENGTH
- CvGameTextMgr::getTurnTimerText  (CvGameTextMgr.cpp:19628)  <- define PEACE_TREATY_LENGTH
- CvPlayer::getItemTradeString  (CvPlayer.cpp:24024)  <- define PEACE_TREATY_LENGTH
- CvPlayerAI::AI_bonusTradeVal  (CvPlayerAI.cpp:10222)  <- define PEACE_TREATY_LENGTH
- CvPlayerAI::AI_doTurnPost  (CvPlayerAI.cpp:543)  <- call CvPlayerAI::AI_doDiplo
- CvPlayerAI::AI_eventValue  (CvPlayerAI.cpp:19730)  <- define PEACE_TREATY_LENGTH
- CvPlayerAI::AI_goldPerTurnTradeVal  (CvPlayerAI.cpp:9782)  <- define PEACE_TREATY_LENGTH
- CvPlayerAI::AI_maxGoldPerTurnTrade  (CvPlayerAI.cpp:9758)  <- define PEACE_TREATY_LENGTH
- CvPlot::pageGraphics  (CvPlot.cpp:349)  <- call CvPlot::updateFeatureSymbolEntity
- CvPlot::setLayoutDirty  (CvPlot.cpp:9708)  <- call CvPlot::updatePlotBuilder
- CvPlot::setPlotType  (CvPlot.cpp:5294)  <- call CvPlot::updateRouteSymbol
- CvPlot::setRevealedRouteType  (CvPlot.cpp:7943)  <- call CvPlot::updateRouteSymbol
- CvPlot::setRouteType  (CvPlot.cpp:5941)  <- call CvPlot::updateRouteSymbol
- CvPlot::updateFeatureSymbol  (CvPlot.cpp:8109)  <- call CvPlot::updateFeatureSymbolEntity
- CvPlot::updateVisibility  (CvPlot.cpp:765)  <- call CvPlot::updateRouteSymbol
- CvUnit::pageGraphics  (CvUnit.cpp:484)  <- call CvUnit::canPageGraphicsOut
- CvUnit::setupGraphical  (CvUnit.cpp:435)  <- call CvUnit::canPageGraphicsOut

### level 2 (61)

- CvCity::alterWorkingPlot  (CvCity.cpp:12012)  <- call CvCity::setWorkingPlot
- CvCity::init  (CvCity.cpp:157)  <- call CvCity::setupGraphical
- CvCity::setWorkingPlot  (CvCity.cpp:12006)  <- call CvCity::setWorkingPlot
- CvCity::verifyWorkingPlot  (CvCity.cpp:1699)  <- call CvCity::setWorkingPlot
- CvCityAI::AI_addBestCitizen  (CvCityAI.cpp:9768)  <- call CvCity::setWorkingPlot
- CvCityAI::AI_assignWorkingPlots  (CvCityAI.cpp:245)  <- call CvCity::setWorkingPlot
- CvCityAI::AI_juggleCitizens  (CvCityAI.cpp:10041)  <- call CvCity::setWorkingPlot
- CvCityAI::AI_removeWorstCitizen  (CvCityAI.cpp:9917)  <- call CvCity::setWorkingPlot
- CvCityAI::AI_updateWorkersNeededHere  (CvCityAI.cpp:13224)  <- call CvCity::setWorkingPlot
- CvDLLWidgetData::parseHelp  (CvDLLWidgetData.cpp:53)  <- call CvDLLWidgetData::parseTradeItem
- CvDeal::addTrades  (CvDeal.cpp:119)  <- call CvDeal::startTrade
- CvDeal::isCancelable  (CvDeal.cpp:1280)  <- call CvDeal::turnsToCancel
- CvGame::doDeals  (CvGame.cpp:6952)  <- call CvDeal::doTurn
- CvGame::normalizeAddExtras  (CvGame.cpp:1752)  <- call CvPlot::setPlotType
- CvGame::normalizeAddLakes  (CvGame.cpp:1302)  <- call CvPlot::setPlotType
- CvGame::normalizeRemovePeaks  (CvGame.cpp:1264)  <- call CvPlot::setPlotType
- CvGameAI::CvGameAI  (CvGameAI.cpp:13)  <- call CvGame::CvGame
- CvGameAI::read  (CvGameAI.cpp:113)  <- call CvGame::read
- CvGameTextMgr::getDealString  (CvGameTextMgr.cpp:15071)  <- call CvGameTextMgr::getTradeString
- CvMap::setAllPlotTypes  (CvMap.cpp:306)  <- call CvPlot::setPlotType
- CvMap::updateVisibility  (CvMap.cpp:374)  <- call CvPlot::updateVisibility
- CvMapGenerator::addLakes  (CvMapGenerator.cpp:262)  <- call CvPlot::setPlotType
- CvMapGenerator::setPlotTypes  (CvMapGenerator.cpp:1078)  <- call CvPlot::setPlotType
- CvPlayer::doAdvancedStartAction  (CvPlayer.cpp:16735)  <- call CvPlot::setRouteType
- CvPlayer::doEspionageMission  (CvPlayer.cpp:16109)  <- call CvPlot::setRouteType
- CvPlayer::doTurn  (CvPlayer.cpp:3918)  <- call CvPlayerAI::AI_doTurnPost
- CvPlayer::setCurrentEra  (CvPlayer.cpp:12644)  <- call CvPlot::setLayoutDirty
- CvPlayer::setupGraphical  (CvPlayer.cpp:1815)  <- call CvCity::setupGraphical
- CvPlayerAI::AI_chooseEvent  (CvPlayerAI.cpp:20273)  <- call CvPlayerAI::AI_eventValue
- CvPlayerAI::AI_dealVal  (CvPlayerAI.cpp:8823)  <- call CvPlayerAI::AI_bonusTradeVal
- CvPlot::applyEvent  (CvPlot.cpp:10226)  <- call CvPlot::setRouteType
- CvPlot::changeBuildProgress  (CvPlot.cpp:8000)  <- call CvPlot::setRouteType
- CvPlot::erase  (CvPlot.cpp:451)  <- call CvPlot::setRouteType
- CvPlot::setBonusType  (CvPlot.cpp:5769)  <- call CvPlot::setLayoutDirty
- CvPlot::setFeatureType  (CvPlot.cpp:5599)  <- call CvPlot::updateFeatureSymbol
- CvPlot::setImprovementType  (CvPlot.cpp:5820)  <- call CvPlot::setLayoutDirty
- CvPlot::setIrrigated  (CvPlot.cpp:4785)  <- call CvPlot::setLayoutDirty
- CvPlot::setRevealed  (CvPlot.cpp:7703)  <- call CvPlot::updateVisibility
- CvPlot::setRevealedImprovementType  (CvPlot.cpp:7891)  <- call CvPlot::setLayoutDirty
- CvPlot::setTerrainType  (CvPlot.cpp:5544)  <- call CvPlot::setPlotType
- CvPlot::setupGraphical  (CvPlot.cpp:273)  <- call CvPlot::updateFeatureSymbol
- CvPlot::updateCityRoute  (CvPlot.cpp:5988)  <- call CvPlot::setRouteType
- CvPlot::updateFlagSymbol  (CvPlot.cpp:8342)  <- call CvPlot::pageGraphics
- CvPlot::updateRiverSymbol  (CvPlot.cpp:8243)  <- call CvPlot::setLayoutDirty
- CvTeam::processTech  (CvTeam.cpp:6792)  <- call CvPlot::setLayoutDirty
- CvTeam::resetPlotAndCityData  (CvTeam.cpp:433)  <- call CvPlot::setRevealedRouteType
- CvTeam::setForceRevealedBonus  (CvTeam.cpp:7197)  <- call CvPlot::setLayoutDirty
- CvUnit::init  (CvUnit.cpp:100)  <- call CvUnit::setupGraphical
- CvUnit::isCombatVisible  (CvUnit.cpp:14330)  <- call CvUnit::pageGraphics
- CvUnit::pillage  (CvUnit.cpp:5410)  <- call CvPlot::setRouteType
- CvUnit::reloadEntity  (CvUnit.cpp:83)  <- call CvUnit::setupGraphical
- CvUnit::setXY  (CvUnit.cpp:10576)  <- call CvPlot::pageGraphics
- CyDeal::turnsToCancel  (CyDeal.cpp:125)  <- call CvDeal::turnsToCancel
- CyGameTextMgr::getTradeString  (CyGameTextMgr.cpp:198)  <- call CvGameTextMgr::getTradeString
- CyPlayer::AI_maxGoldPerTurnTrade  (CyPlayer.cpp:2473)  <- call CvPlayerAI::AI_maxGoldPerTurnTrade
- CyPlot::setPlotType  (CyPlot.cpp:651)  <- call CvPlot::setPlotType
- CyPlot::setRouteType  (CyPlot.cpp:787)  <- call CvPlot::setRouteType
- CyPlot::updateVisibility  (CyPlot.cpp:70)  <- call CvPlot::updateVisibility
- ReadStreamableFFreeListTrashArray<class CvArea>  (FFreeListTrashArray.h:485)  <- call CvGame::read
- ReadStreamableFFreeListTrashArray<class CvSelectionGroupAI>  (FFreeListTrashArray.h:485)  <- call CvGame::read
- addEntityMission  (CvGameCoreUtils.cpp:219)  <- call CvUnit::pageGraphics

### level 3 (139)

- CvCity::alterSpecialistCount  (CvCity.cpp:11567)  <- call CvCityAI::AI_addBestCitizen
- CvCity::applyEvent  (CvCity.cpp:15249)  <- call CvPlot::setImprovementType
- CvCity::doTask  (CvCity.cpp:1517)  <- call CvCity::alterWorkingPlot
- CvCity::kill  (CvCity.cpp:1018)  <- call CvPlot::setFeatureType
- CvCity::popOrder  (CvCity.cpp:12939)  <- call CvCityAI::AI_assignWorkingPlots
- CvCity::setCitizensAutomated  (CvCity.cpp:8698)  <- call CvCityAI::AI_assignWorkingPlots
- CvCity::verifyWorkingPlots  (CvCity.cpp:1723)  <- call CvCity::verifyWorkingPlot
- CvCityAI::AI_buildGovernorChooseProduction  (CvCityAI.cpp:12171)  <- call CvCityAI::AI_assignWorkingPlots
- CvCityAI::AI_chooseProduction  (CvCityAI.cpp:706)  <- call CvCityAI::AI_assignWorkingPlots
- CvCityAI::AI_doTurn  (CvCityAI.cpp:186)  <- call CvCityAI::AI_updateWorkersNeededHere
- CvCityAI::AI_init  (CvCityAI.cpp:82)  <- call CvCityAI::AI_updateWorkersNeededHere
- CvCityAI::AI_setEmphasize  (CvCityAI.cpp:6606)  <- call CvCityAI::AI_assignWorkingPlots
- CvCityAI::AI_updateAssignWork  (CvCityAI.cpp:400)  <- call CvCityAI::AI_assignWorkingPlots
- CvDLLWidgetData::doDealKill  (CvDLLWidgetData.cpp:5969)  <- call CvDeal::isCancelable
- CvDLLWidgetData::isLink  (CvDLLWidgetData.cpp:1072)  <- call CvDeal::isCancelable
- CvDLLWidgetData::parseKillDealHelp  (CvDLLWidgetData.cpp:5906)  <- call CvDeal::isCancelable
- CvDeal::verify  (CvDeal.cpp:336)  <- call CvDeal::isCancelable
- CvGame::doGlobalWarming  (CvGame.cpp:6966)  <- call CvPlot::setFeatureType
- CvGame::doTurn  (CvGame.cpp:6804)  <- call CvGame::doDeals
- CvGame::implementDeal  (CvGame.cpp:3487)  <- call CvDeal::addTrades
- CvGame::normalizeAddFoodBonuses  (CvGame.cpp:1537)  <- call CvPlot::setBonusType
- CvGame::normalizeAddGoodTerrain  (CvGame.cpp:1647)  <- call CvPlot::setFeatureType
- CvGame::normalizeAddRiver  (CvGame.cpp:1210)  <- call CvPlot::setFeatureType
- CvGame::normalizeRemoveBadFeatures  (CvGame.cpp:1374)  <- call CvPlot::setFeatureType
- CvGame::normalizeRemoveBadTerrain  (CvGame.cpp:1451)  <- call CvPlot::setTerrainType
- CvGame::normalizeStartingPlots  (CvGame.cpp:2052)  <- call CvGame::normalizeRemovePeaks
- CvGame::setActivePlayer  (CvGame.cpp:5561)  <- call CvMap::updateVisibility
- CvGame::toggleDebugMode  (CvGame.cpp:5384)  <- call CvMap::updateVisibility
- CvGameTextMgr::getDealString  (CvGameTextMgr.cpp:15060)  <- call CvGameTextMgr::getDealString
- CvGlobals::init  (CvGlobals.cpp:384)  <- call CvGameAI::CvGameAI
- CvMap::erasePlots  (CvMap.cpp:280)  <- call CvPlot::erase
- CvMap::read  (CvMap.cpp:1300)  <- call ReadStreamableFFreeListTrashArray<class CvArea>
- CvMap::setRevealedPlots  (CvMap.cpp:291)  <- call CvPlot::setRevealed
- CvMap::setupGraphical  (CvMap.cpp:263)  <- call CvPlot::setupGraphical
- CvMap::updateFlagSymbols  (CvMap.cpp:343)  <- call CvPlot::updateFlagSymbol
- CvMapGenerator::addFeatures  (CvMapGenerator.cpp:644)  <- call CvPlot::setFeatureType
- CvMapGenerator::addGameElements  (CvMapGenerator.cpp:240)  <- call CvMapGenerator::addLakes
- CvMapGenerator::addGoodies  (CvMapGenerator.cpp:888)  <- call CvPlot::setImprovementType
- CvMapGenerator::addNonUniqueBonusType  (CvMapGenerator.cpp:828)  <- call CvPlot::setBonusType
- CvMapGenerator::addUniqueBonusType  (CvMapGenerator.cpp:712)  <- call CvPlot::setBonusType
- CvMapGenerator::eraseBonuses  (CvMapGenerator.cpp:968)  <- call CvPlot::setBonusType
- CvMapGenerator::eraseFeatures  (CvMapGenerator.cpp:957)  <- call CvPlot::setFeatureType
- CvMapGenerator::generatePlotTypes  (CvMapGenerator.cpp:1022)  <- call CvMapGenerator::setPlotTypes
- CvMapGenerator::generateTerrain  (CvMapGenerator.cpp:1051)  <- call CvPlot::setTerrainType
- CvNetAdvancedStartAction::Execute  (CvMessageData.cpp:484)  <- call CvPlayer::doAdvancedStartAction
- CvPlayer::acquireCity  (CvPlayer.cpp:2337)  <- call CvPlot::setRevealed
- CvPlayer::applyEvent  (CvPlayer.cpp:20656)  <- call CvPlot::applyEvent
- CvPlayer::assimilatePlayer  (CvPlayer.cpp:22593)  <- call CvPlot::setRevealed
- CvPlayer::changeCiv  (CvPlayer.cpp:1573)  <- call CvPlayer::setupGraphical
- CvPlayer::init  (CvPlayer.cpp:191)  <- call CvPlayer::setupGraphical
- CvPlayer::initCity  (CvPlayer.cpp:2320)  <- call CvCity::init
- CvPlayer::initFreeUnits  (CvPlayer.cpp:1848)  <- call CvPlot::setRevealed
- CvPlayer::initInGame  (CvPlayer.cpp:445)  <- call CvPlayer::setupGraphical
- CvPlayer::initUnit  (CvPlayer.cpp:3107)  <- call CvUnit::init
- CvPlayer::isTradingWithTeam  (CvPlayer.cpp:5899)  <- call CvDeal::isCancelable
- CvPlayer::read  (CvPlayer.cpp:18464)  <- call ReadStreamableFFreeListTrashArray<class CvSelectionGroupAI>
- CvPlayer::receiveGoody  (CvPlayer.cpp:6344)  <- call CvPlot::setRevealed
- CvPlayer::setTurnActive  (CvPlayer.cpp:12160)  <- call CvPlayer::doTurn
- CvPlayer::splitEmpire  (CvPlayer.cpp:22369)  <- call CvPlot::setRevealed
- CvPlayer::stopTradingWithTeam  (CvPlayer.cpp:5963)  <- call CvDeal::isCancelable
- CvPlayer::trigger  (CvPlayer.cpp:21805)  <- call CvPlayerAI::AI_chooseEvent
- CvPlayerAI::AI_advancedStartDoRoute  (CvPlayerAI.cpp:23880)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartPlaceCity  (CvPlayerAI.cpp:23766)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartPlaceExploreUnits  (CvPlayerAI.cpp:23657)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartRevealRadius  (CvPlayerAI.cpp:23741)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_advancedStartRouteTerritory  (CvPlayerAI.cpp:23916)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_assignWorkingPlots  (CvPlayerAI.cpp:1701)  <- call CvCityAI::AI_assignWorkingPlots
- CvPlayerAI::AI_doAdvancedStart  (CvPlayerAI.cpp:24119)  <- call CvPlayer::doAdvancedStartAction
- CvPlayerAI::AI_stopTradingTradeVal  (CvPlayerAI.cpp:10743)  <- call CvDeal::isCancelable
- CvPlot::changeStolenVisibilityCount  (CvPlot.cpp:7288)  <- call CvPlot::setRevealed
- CvPlot::changeVisibilityCount  (CvPlot.cpp:7191)  <- call CvPlot::setRevealed
- CvPlot::doFeature  (CvPlot.cpp:8798)  <- call CvPlot::setFeatureType
- CvPlot::doImprovement  (CvPlot.cpp:632)  <- call CvPlot::setBonusType
- CvPlot::doImprovementUpgrade  (CvPlot.cpp:695)  <- call CvPlot::setImprovementType
- CvPlot::nukeExplosion  (CvPlot.cpp:1060)  <- call CvPlot::setFeatureType
- CvPlot::removeGoody  (CvPlot.cpp:3699)  <- call CvPlot::setImprovementType
- CvPlot::setNOfRiver  (CvPlot.cpp:4611)  <- call CvPlot::updateRiverSymbol
- CvPlot::setWOfRiver  (CvPlot.cpp:4658)  <- call CvPlot::updateRiverSymbol
- CvPlot::updateIrrigated  (CvPlot.cpp:4811)  <- call CvPlot::setIrrigated
- CvPlot::updateWorkingCity  (CvPlot.cpp:6101)  <- call CvCity::setWorkingPlot
- CvSelectionGroup::setRemoteTransportUnit  (CvSelectionGroup.cpp:5064)  <- call CvUnit::setXY
- CvSelectionGroup::startMission  (CvSelectionGroup.cpp:1372)  <- call CvUnit::pillage
- CvTeam::addTeam  (CvTeam.cpp:520)  <- call CvPlot::setRevealed
- CvTeam::setHasTech  (CvTeam.cpp:5947)  <- call CvPlayer::setCurrentEra
- CvTeam::shareItems  (CvTeam.cpp:820)  <- call CvTeam::setForceRevealedBonus
- CvUnit::airBomb  (CvUnit.cpp:4905)  <- call CvPlot::setImprovementType
- CvUnit::airBomb1  (CvUnit.cpp:14543)  <- call CvPlot::setImprovementType
- CvUnit::airBomb2  (CvUnit.cpp:14694)  <- call addEntityMission
- CvUnit::airBomb3  (CvUnit.cpp:14897)  <- call addEntityMission
- CvUnit::airBomb4  (CvUnit.cpp:15138)  <- call addEntityMission
- CvUnit::airBomb5  (CvUnit.cpp:15325)  <- call addEntityMission
- CvUnit::airCircle  (CvUnit.cpp:3932)  <- call addEntityMission
- CvUnit::airlift  (CvUnit.cpp:4213)  <- call CvUnit::setXY
- CvUnit::archerBombard  (CvUnit.cpp:16457)  <- call addEntityMission
- CvUnit::attackForDamage  (CvUnit.cpp:3063)  <- call addEntityMission
- CvUnit::bombard  (CvUnit.cpp:5300)  <- call addEntityMission
- CvUnit::bombardRanged  (CvUnit.cpp:15541)  <- call CvPlot::setImprovementType
- CvUnit::build  (CvUnit.cpp:7651)  <- call CvPlot::changeBuildProgress
- CvUnit::doActiveDefense  (CvUnit.cpp:16332)  <- call addEntityMission
- CvUnit::doOpportunityFire  (CvUnit.cpp:16269)  <- call addEntityMission
- CvUnit::espionage  (CvUnit.cpp:7342)  <- call CvUnit::setXY
- CvUnit::fighterEngage  (CvUnit.cpp:16633)  <- call addEntityMission
- CvUnit::jumpToNearestValidPlot  (CvUnit.cpp:3226)  <- call CvUnit::setXY
- CvUnit::kill  (CvUnit.cpp:592)  <- call CvUnit::setXY
- CvUnit::move  (CvUnit.cpp:3183)  <- call CvUnit::setXY
- CvUnit::nuke  (CvUnit.cpp:4346)  <- call addEntityMission
- CvUnit::paradrop  (CvUnit.cpp:4714)  <- call CvUnit::setXY
- CvUnit::promote  (CvUnit.cpp:7741)  <- call CvUnit::reloadEntity
- CvUnit::rangeStrike  (CvUnit.cpp:13601)  <- call addEntityMission
- CvUnit::recon  (CvUnit.cpp:4615)  <- call addEntityMission
- CvUnit::sabotage  (CvUnit.cpp:5813)  <- call CvPlot::setImprovementType
- CvUnit::setLeaderUnitType  (CvUnit.cpp:12221)  <- call CvUnit::reloadEntity
- CvUnit::testSpyIntercepted  (CvUnit.cpp:7410)  <- call CvUnit::setXY
- CvUnit::updateAirCombat  (CvUnit.cpp:1088)  <- call addEntityMission
- CvUnit::updateAirStrike  (CvUnit.cpp:881)  <- call addEntityMission
- CvUnit::updateCombat  (CvUnit.cpp:1405)  <- call addEntityMission
- CvUnit::updateStackCombat  (CvUnit.cpp:15848)  <- call addEntityMission
- CyCity::alterWorkingPlot  (CyCity.cpp:2591)  <- call CvCity::alterWorkingPlot
- CyDeal::getCannotCancelReason  (CyDeal.cpp:115)  <- call CvDeal::isCancelable
- CyDeal::isCancelable  (CyDeal.cpp:100)  <- call CvDeal::isCancelable
- CyGamePythonInterface  (CyGameInterface.cpp:13)  <- call CyDeal::turnsToCancel
- CyGameTextMgrInterface  (CyGameTextMgrInterface.cpp:9)  <- call CyGameTextMgr::getTradeString
- CyMap::setAllPlotTypes  (CyMap.cpp:40)  <- call CvMap::setAllPlotTypes
- CyMap::updateVisibility  (CyMap.cpp:59)  <- call CvMap::updateVisibility
- CyMapGenerator::addLakes  (CyMapGenerator.cpp:45)  <- call CvMapGenerator::addLakes
- CyMapGenerator::setPlotTypes  (CyMapGenerator.cpp:141)  <- call CvMapGenerator::setPlotTypes
- CyPlayer::doEspionageMission  (CyPlayer.cpp:1031)  <- call CvPlayer::doEspionageMission
- CyPlayer::setCurrentEra  (CyPlayer.cpp:1716)  <- call CvPlayer::setCurrentEra
- CyPlayerPythonInterface2  (CyPlayerInterface2.cpp:17)  <- call CyPlayer::AI_maxGoldPerTurnTrade
- CyPlot::changeBuildProgress  (CyPlot.cpp:988)  <- call CvPlot::changeBuildProgress
- CyPlot::erase  (CyPlot.cpp:23)  <- call CvPlot::erase
- CyPlot::setBonusType  (CyPlot.cpp:765)  <- call CvPlot::setBonusType
- CyPlot::setFeatureType  (CyPlot.cpp:673)  <- call CvPlot::setFeatureType
- CyPlot::setImprovementType  (CyPlot.cpp:776)  <- call CvPlot::setImprovementType
- CyPlot::setRevealed  (CyPlot.cpp:967)  <- call CvPlot::setRevealed
- CyPlot::setTerrainType  (CyPlot.cpp:662)  <- call CvPlot::setTerrainType
- CyPlotPythonInterface1  (CyPlotInterface1.cpp:15)  <- call CyPlot::setPlotType
- CyUnit::setXY  (CyUnit.cpp:1192)  <- call CvUnit::setXY
- changeIrrigated  (CvGameCoreUtils.cpp:1642)  <- call CvPlot::setIrrigated

### level 4 (178)

- CvCity::cheat  (CvCity.cpp:16214)  <- call CvCity::popOrder
- CvCity::clearOrderQueue  (CvCity.cpp:12751)  <- call CvCity::popOrder
- CvCity::doCheckProduction  (CvCity.cpp:13641)  <- call CvCity::popOrder
- CvCity::doMeltdown  (CvCity.cpp:14065)  <- call CvPlot::nukeExplosion
- CvCity::doProduction  (CvCity.cpp:13780)  <- call CvCityAI::AI_chooseProduction
- CvCity::doTurn  (CvCity.cpp:1221)  <- call CvCityAI::AI_doTurn
- CvCity::emergencyConscript  (CvCity.cpp:16271)  <- call CvPlayer::initUnit
- CvCity::initConscriptedUnit  (CvCity.cpp:4201)  <- call CvPlayer::initUnit
- CvCity::liberate  (CvCity.cpp:15943)  <- call CvPlayer::acquireCity
- CvCity::pushOrder  (CvCity.cpp:12765)  <- call CvCity::popOrder
- CvCity::setHeadquarters  (CvCity.cpp:4776)  <- call CvPlayer::initUnit
- CvCity::setNumRealBuildingTimed  (CvCity.cpp:12077)  <- call CvCityAI::AI_updateAssignWork
- CvCity::setProductionAutomated  (CvCity.cpp:8732)  <- call CvCityAI::AI_chooseProduction
- CvCityAI::AI_doEmphasize  (CvCityAI.cpp:9279)  <- call CvCityAI::AI_setEmphasize
- CvDLLWidgetData::executeAction  (CvDLLWidgetData.cpp:657)  <- call CvDLLWidgetData::doDealKill
- CvDeal::kill  (CvDeal.cpp:78)  <- call CvGameTextMgr::getDealString
- CvDeal::startTeamTrade  (CvDeal.cpp:1198)  <- call CvGame::implementDeal
- CvGame::addPlayer  (CvGame.cpp:9731)  <- call CvPlayer::initInGame
- CvGame::changeHumanPlayer  (CvGame.cpp:9807)  <- call CvGame::setActivePlayer
- CvGame::cheatSpaceship  (CvGameInterface.cpp:2561)  <- call CvTeam::setHasTech
- CvGame::createAnimals  (CvGame.cpp:7988)  <- call CvPlayer::initUnit
- CvGame::createBarbarianUnits  (CvGame.cpp:7721)  <- call CvUnit::kill
- CvGame::initDiplomacy  (CvGame.cpp:734)  <- call CvGame::implementDeal
- CvGame::initFreeState  (CvGame.cpp:790)  <- call CvMap::setRevealedPlots
- CvGame::initFreeUnits  (CvGame.cpp:850)  <- call CvPlayer::initFreeUnits
- CvGame::nextActivePlayer  (CvGameInterface.cpp:2691)  <- call CvPlayer::setTurnActive
- CvGame::processVote  (CvGame.cpp:8665)  <- call CvPlayer::acquireCity
- CvGame::regenerateMap  (CvGame.cpp:348)  <- call CvMap::setupGraphical
- CvGame::replaceCorporation  (CvGame.cpp:4049)  <- call CvUnit::kill
- CvGame::reviveActivePlayer  (CvGame.cpp:4298)  <- call CvPlayer::initUnit
- CvGame::revivePlayer  (CvGame.cpp:4275)  <- call CvPlayer::initUnit
- CvGame::setInitialItems  (CvGame.cpp:293)  <- call CvGame::normalizeStartingPlots
- CvGame::verifyDeals  (CvGame.cpp:3505)  <- call CvDeal::verify
- CvGameTextMgr::getActiveDealsString  (CvGameTextMgr.cpp:16556)  <- call CvGameTextMgr::getDealString
- CvMap::updateIrrigated  (CvMap.cpp:429)  <- call CvPlot::updateIrrigated
- CvMap::updateWorkingCity  (CvMap.cpp:451)  <- call CvPlot::updateWorkingCity
- CvMapGenerator::addBonuses  (CvMapGenerator.cpp:674)  <- call CvMapGenerator::addUniqueBonusType
- CvMapGenerator::doRiver  (CvMapGenerator.cpp:373)  <- call CvPlot::setNOfRiver
- CvMapGenerator::eraseGoodies  (CvMapGenerator.cpp:979)  <- call CvPlot::removeGoody
- CvMapGenerator::eraseRivers  (CvMapGenerator.cpp:939)  <- call CvPlot::setNOfRiver
- CvMapGenerator::generateRandomMap  (CvMapGenerator.cpp:999)  <- call CvMapGenerator::generatePlotTypes
- CvNetDoTask::Execute  (CvMessageData.cpp:283)  <- call CvCity::doTask
- CvNetEmpireSplit::Execute  (CvMessageData.cpp:588)  <- call CvPlayer::splitEmpire
- CvNetEventTriggered::Execute  (CvMessageData.cpp:685)  <- call CvPlayer::applyEvent
- CvNetPopOrder::Execute  (CvMessageData.cpp:238)  <- call CvCity::popOrder
- CvNetResearch::Execute  (CvMessageData.cpp:376)  <- call CvTeam::setHasTech
- CvPlayer::addFreeUnit  (CvPlayer.cpp:2004)  <- call CvPlayer::initUnit
- CvPlayer::canStopTradingWithTeam  (CvPlayer.cpp:5937)  <- call CvPlayer::isTradingWithTeam
- CvPlayer::cheat  (CvPlayer.cpp:24740)  <- call CvTeam::setHasTech
- CvPlayer::createGreatPeople  (CvPlayer.cpp:19505)  <- call CvPlayer::initUnit
- CvPlayer::disband  (CvPlayer.cpp:6222)  <- call CvCity::kill
- CvPlayer::disbandUnit  (CvPlayer.cpp:3124)  <- call CvUnit::kill
- CvPlayer::doEvents  (CvPlayer.cpp:21539)  <- call CvPlayer::applyEvent
- CvPlayer::doGoody  (CvPlayer.cpp:6546)  <- call CvPlayer::receiveGoody
- CvPlayer::forcePeace  (CvPlayer.cpp:23601)  <- call CvGame::implementDeal
- CvPlayer::found  (CvPlayer.cpp:6737)  <- call CvPlayer::initCity
- CvPlayer::foundReligion  (CvPlayer.cpp:9205)  <- call CvPlayer::initUnit
- CvPlayer::handleDiploEvent  (CvPlayer.cpp:5137)  <- call CvPlayer::stopTradingWithTeam
- CvPlayer::initTriggeredData  (CvPlayer.cpp:19815)  <- call CvPlayer::trigger
- CvPlayer::killCities  (CvPlayer.cpp:2951)  <- call CvCity::kill
- CvPlayer::killGoldenAgeUnits  (CvPlayer.cpp:9580)  <- call CvUnit::kill
- CvPlayer::killUnits  (CvPlayer.cpp:3282)  <- call CvUnit::kill
- CvPlayer::setAlive  (CvPlayer.cpp:11816)  <- call CvPlayer::setTurnActive
- CvPlayer::setAutoMoves  (CvPlayer.cpp:12481)  <- call CvPlayer::setTurnActive
- CvPlayer::setNewPlayerAlive  (CvPlayer.cpp:11916)  <- call CvPlayer::setTurnActive
- CvPlayerAI::AI_chooseFreeTech  (CvPlayerAI.cpp:7103)  <- call CvTeam::setHasTech
- CvPlayerAI::AI_conquerCity  (CvPlayerAI.cpp:1744)  <- call CvCity::doTask
- CvPlayerAI::AI_disbandUnit  (CvPlayerAI.cpp:20457)  <- call CvUnit::kill
- CvPlayerAI::AI_doCommerce  (CvPlayerAI.cpp:16646)  <- call CvPlayerAI::AI_assignWorkingPlots
- CvPlayerAI::AI_doPeace  (CvPlayerAI.cpp:862)  <- call CvGame::implementDeal
- CvPlayerAI::AI_doSplit  (CvPlayerAI.cpp:20308)  <- call CvPlayer::splitEmpire
- CvPlayerAI::AI_doTurnUnitsPost  (CvPlayerAI.cpp:625)  <- call CvUnit::kill
- CvPlayerAI::AI_updateAssignWork  (CvPlayerAI.cpp:1713)  <- call CvCityAI::AI_updateAssignWork
- CvPlayerAI::AI_updateMilitaryOperations  (CvPlayerAI.cpp:16065)  <- call CvPlayer::initUnit
- CvPlayerAI::read  (CvPlayerAI.cpp:19316)  <- call CvPlayer::read
- CvPlot::changeAdjacentSight  (CvPlot.cpp:1856)  <- call CvPlot::changeVisibilityCount
- CvPlot::doCulture  (CvPlot.cpp:8956)  <- call CvUnit::kill
- CvPlot::doTurn  (CvPlot.cpp:579)  <- call CvPlot::doFeature
- CvPlot::setArea  (CvPlot.cpp:4402)  <- call CvPlot::updateIrrigated
- CvPlot::setOwner  (CvPlot.cpp:5004)  <- call CvUnit::kill
- CvPlot::setPlotCity  (CvPlot.cpp:6014)  <- call CvPlot::updateIrrigated
- CvPlot::setWorkingCityOverride  (CvPlot.cpp:6205)  <- call CvPlot::updateWorkingCity
- CvPlot::verifyUnitValidPlot  (CvPlot.cpp:964)  <- call CvUnit::jumpToNearestValidPlot
- CvSelectionGroup::activateHeadMission  (CvSelectionGroup.cpp:6327)  <- call CvSelectionGroup::startMission
- CvSelectionGroup::airCircle  (CvSelectionGroup.cpp:4106)  <- call CvUnit::airCircle
- CvSelectionGroup::autoMission  (CvSelectionGroup.cpp:718)  <- call CvSelectionGroup::startMission
- CvSelectionGroup::continueMission  (CvSelectionGroup.cpp:2043)  <- call CvSelectionGroup::setRemoteTransportUnit
- CvSelectionGroup::groupAttack  (CvSelectionGroup.cpp:4392)  <- call CvUnit::bombardRanged
- CvSelectionGroup::groupBuild  (CvSelectionGroup.cpp:4863)  <- call CvUnit::build
- CvSelectionGroup::groupMove  (CvSelectionGroup.cpp:4697)  <- call CvUnit::move
- CvSelectionGroup::groupStackAttack  (CvSelectionGroup.cpp:6368)  <- call CvUnit::bombardRanged
- CvSelectionGroup::updateTimers  (CvSelectionGroup.cpp:525)  <- call CvUnit::updateAirCombat
- CvTeam::assignVassal  (CvTeam.cpp:5125)  <- call CvGame::implementDeal
- CvTeam::setResearchProgress  (CvTeam.cpp:5595)  <- call CvTeam::setHasTech
- CvTeam::setStolenVisibilityTimer  (CvTeam.cpp:4270)  <- call CvPlot::changeStolenVisibilityCount
- CvTeam::setTurnActive  (CvTeam.cpp:7295)  <- call CvPlayer::setTurnActive
- CvTeam::signDefensivePact  (CvTeam.cpp:2276)  <- call CvGame::implementDeal
- CvTeam::signOpenBorders  (CvTeam.cpp:2249)  <- call CvGame::implementDeal
- CvTeam::updateTechShare  (CvTeam.cpp:6634)  <- call CvTeam::setHasTech
- CvTeam::verifySpyUnitsValidPlot  (CvTeam.cpp:7162)  <- call CvUnit::jumpToNearestValidPlot
- CvUnit::applyEvent  (CvUnit.cpp:14184)  <- call CvUnit::kill
- CvUnit::attack  (CvUnit.cpp:3044)  <- call CvUnit::updateCombat
- CvUnit::construct  (CvUnit.cpp:6691)  <- call CvUnit::kill
- CvUnit::convert  (CvUnit.cpp:523)  <- call CvUnit::jumpToNearestValidPlot
- CvUnit::destroy  (CvUnit.cpp:6006)  <- call CvUnit::kill
- CvUnit::discover  (CvUnit.cpp:6770)  <- call CvUnit::kill
- CvUnit::doCommand  (CvUnit.cpp:2424)  <- call CvUnit::promote
- CvUnit::doDelayedDeath  (CvUnit.cpp:12054)  <- call CvUnit::kill
- CvUnit::doTurn  (CvUnit.cpp:808)  <- call CvUnit::testSpyIntercepted
- CvUnit::fightInterceptor  (CvUnit.cpp:3054)  <- call CvUnit::updateAirCombat
- CvUnit::flankingStrikeCombat  (CvUnit.cpp:13282)  <- call CvUnit::kill
- CvUnit::found  (CvUnit.cpp:6239)  <- call CvUnit::kill
- CvUnit::gift  (CvUnit.cpp:3506)  <- call CvPlayer::initUnit
- CvUnit::goldenAge  (CvUnit.cpp:7605)  <- call CvUnit::kill
- CvUnit::greatWork  (CvUnit.cpp:7016)  <- call CvUnit::kill
- CvUnit::hurry  (CvUnit.cpp:6867)  <- call CvUnit::kill
- CvUnit::infiltrate  (CvUnit.cpp:7103)  <- call CvUnit::kill
- CvUnit::join  (CvUnit.cpp:6615)  <- call CvUnit::kill
- CvUnit::lead  (CvUnit.cpp:7793)  <- call CvUnit::kill
- CvUnit::performInquisition  (CvUnit.cpp:17111)  <- call CvUnit::kill
- CvUnit::scrap  (CvUnit.cpp:3427)  <- call CvUnit::kill
- CvUnit::setDamage  (CvUnit.cpp:11146)  <- call CvUnit::kill
- CvUnit::spread  (CvUnit.cpp:6364)  <- call CvUnit::kill
- CvUnit::spreadCorporation  (CvUnit.cpp:6529)  <- call CvUnit::kill
- CvUnit::stealPlans  (CvUnit.cpp:6163)  <- call CvUnit::kill
- CvUnit::trade  (CvUnit.cpp:6954)  <- call CvUnit::kill
- CvUnit::upgrade  (CvUnit.cpp:8370)  <- call CvPlayer::initUnit
- CvUnit::verifyStackValid  (CvUnit.cpp:14313)  <- call CvUnit::jumpToNearestValidPlot
- CvUnitAI::AI_espionageSpy  (CvUnitAI.cpp:23164)  <- call CvUnit::espionage
- CvUnitAI::AI_promote  (CvUnitAI.cpp:695)  <- call CvUnit::promote
- CvUnitAI::AI_revoltCitySpy  (CvUnitAI.cpp:22910)  <- call CvUnit::espionage
- CyCity::alterSpecialistCount  (CyCity.cpp:2458)  <- call CvCity::alterSpecialistCount
- CyCity::doTask  (CyCity.cpp:216)  <- call CvCity::doTask
- CyCity::kill  (CyCity.cpp:24)  <- call CvCity::kill
- CyCity::popOrder  (CyCity.cpp:2662)  <- call CvCity::popOrder
- CyCity::setCitizensAutomated  (CyCity.cpp:1834)  <- call CvCity::setCitizensAutomated
- CyCityPythonInterface1  (CyCityInterface1.cpp:15)  <- call CyCity::alterWorkingPlot
- CyGame::setActivePlayer  (CyGame.cpp:677)  <- call CvGame::setActivePlayer
- CyGame::toggleDebugMode  (CyGame.cpp:617)  <- call CvGame::toggleDebugMode
- CyGameTextMgr::getDealString  (CyGameTextMgr.cpp:257)  <- call CvGameTextMgr::getDealString
- CyMap::erasePlots  (CyMap.cpp:28)  <- call CvMap::erasePlots
- CyMap::regenerateGameElements  (CyMap.cpp:297)  <- call CvMapGenerator::eraseFeatures
- CyMap::setRevealedPlots  (CyMap.cpp:34)  <- call CvMap::setRevealedPlots
- CyMapGenerator::addFeatures  (CyMapGenerator.cpp:63)  <- call CvMapGenerator::addFeatures
- CyMapGenerator::addGameElements  (CyMapGenerator.cpp:39)  <- call CvMapGenerator::addGameElements
- CyMapGenerator::addGoodies  (CyMapGenerator.cpp:87)  <- call CvMapGenerator::addGoodies
- CyMapGenerator::addNonUniqueBonusType  (CyMapGenerator.cpp:81)  <- call CvMapGenerator::addNonUniqueBonusType
- CyMapGenerator::addUniqueBonusType  (CyMapGenerator.cpp:75)  <- call CvMapGenerator::addUniqueBonusType
- CyMapGenerator::eraseBonuses  (CyMapGenerator.cpp:105)  <- call CvMapGenerator::eraseBonuses
- CyMapGenerator::eraseFeatures  (CyMapGenerator.cpp:99)  <- call CvMapGenerator::eraseFeatures
- CyMapGenerator::generatePlotTypes  (CyMapGenerator.cpp:123)  <- call CvMapGenerator::generatePlotTypes
- CyMapGenerator::generateTerrain  (CyMapGenerator.cpp:129)  <- call CvMapGenerator::generateTerrain
- CyMapGeneratorPythonInterface  (CyMapGeneratorInterface.cpp:12)  <- call CyMapGenerator::setPlotTypes
- CyMapPythonInterface  (CyMapInterface.cpp:17)  <- call CyMap::setAllPlotTypes
- CyPlayer::acquireCity  (CyPlayer.cpp:153)  <- call CvPlayer::acquireCity
- CyPlayer::assimilatePlayer  (CyPlayer.cpp:2518)  <- call CvPlayer::assimilatePlayer
- CyPlayer::changeCiv  (CyPlayer.cpp:40)  <- call CvPlayer::changeCiv
- CyPlayer::initCity  (CyPlayer.cpp:148)  <- call CvPlayer::initCity
- CyPlayer::initUnit  (CyPlayer.cpp:170)  <- call CvPlayer::initUnit
- CyPlayer::receiveGoody  (CyPlayer.cpp:496)  <- call CvPlayer::receiveGoody
- CyPlayer::splitEmpire  (CyPlayer.cpp:2483)  <- call CvPlayer::splitEmpire
- CyPlayer::stopTradingWithTeam  (CyPlayer.cpp:446)  <- call CvPlayer::stopTradingWithTeam
- CyPlayerPythonInterface1  (CyPlayerInterface1.cpp:17)  <- call CyPlayer::doEspionageMission
- CyPlot::changeVisibilityCount  (CyPlot.cpp:936)  <- call CvPlot::changeVisibilityCount
- CyPlot::nukeExplosion  (CyPlot.cpp:39)  <- call CvPlot::nukeExplosion
- CyPlot::removeGoody  (CyPlot.cpp:309)  <- call CvPlot::removeGoody
- CyPlot::setNOfRiver  (CyPlot.cpp:551)  <- call CvPlot::setNOfRiver
- CyPlot::setWOfRiver  (CyPlot.cpp:564)  <- call CvPlot::setWOfRiver
- CyTeam::addTeam  (CyTeam.cpp:48)  <- call CvTeam::addTeam
- CyTeam::setHasTech  (CyTeam.cpp:873)  <- call CvTeam::setHasTech
- CyUnit::attackForDamage  (CyUnit.cpp:1759)  <- call CvUnit::attackForDamage
- CyUnit::jumpToNearestValidPlot  (CyUnit.cpp:113)  <- call CvUnit::jumpToNearestValidPlot
- CyUnit::kill  (CyUnit.cpp:35)  <- call CvUnit::kill
- CyUnit::promote  (CyUnit.cpp:479)  <- call CvUnit::promote
- CyUnit::rangeStrike  (CyUnit.cpp:1767)  <- call CvUnit::rangeStrike
- CyUnit::setLeaderUnitType  (CyUnit.cpp:1607)  <- call CvUnit::setLeaderUnitType
- CyUnitPythonInterface1  (CyUnitInterface1.cpp:18)  <- call CyUnit::setXY
- DLLPublishToPython  (CvDLLPython.cpp:50)  <- call CyPlotPythonInterface1

### level 5 (144)

- CvArea::changeNumTiles  (CvArea.cpp:365)  <- call CvMap::updateIrrigated
- CvCity::clearWorkingOverride  (CvCity.cpp:1734)  <- call CvPlot::setWorkingCityOverride
- CvCity::conscript  (CvCity.cpp:4246)  <- call CvCity::initConscriptedUnit
- CvCity::createGreatPeople  (CvCity.cpp:1511)  <- call CvPlayer::createGreatPeople
- CvCity::processBuilding  (CvCity.cpp:4420)  <- call CvCity::setHeadquarters
- CvCity::setGameTurnFounded  (CvCity.cpp:6001)  <- call CvMap::updateWorkingCity
- CvCity::setHasCorporation  (CvCity.cpp:12494)  <- call CvGame::replaceCorporation
- CvCity::setNumRealBuilding  (CvCity.cpp:12071)  <- call CvCity::setNumRealBuildingTimed
- CvCityAI::AI_chooseBuilding  (CvCityAI.cpp:9712)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseProcess  (CvCityAI.cpp:9752)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseProject  (CvCityAI.cpp:9736)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseUnit  (CvCityAI.cpp:9406)  <- call CvCity::pushOrder
- CvCityAI::AI_chooseUnit  (CvCityAI.cpp:9457)  <- call CvCity::pushOrder
- CvCityAI::AI_stealPlots  (CvCityAI.cpp:12613)  <- call CvPlot::setWorkingCityOverride
- CvCityAI::AI_trainInquisitor  (CvCityAI.cpp:13542)  <- call CvCity::pushOrder
- CvDLLWidgetData::parseContactCivHelp  (CvDLLWidgetData.cpp:3484)  <- call CvGameTextMgr::getActiveDealsString
- CvDLLWidgetData::parseTradeRoutes  (CvDLLWidgetData.cpp:6057)  <- call CvGameTextMgr::getActiveDealsString
- CvDeal::endTeamTrade  (CvDeal.cpp:1232)  <- call CvDeal::kill
- CvDllPythonEvents::reportCityLost  (CvDllPythonEvents.cpp:534)  <- event RoMEventManager.py RoMEventManager.onCityLost
- CvDllPythonEvents::reportProjectBuilt  (CvDllPythonEvents.cpp:1076)  <- event RoMEventManager.py RoMEventManager.onProjectBuilt
- CvGame::createBarbarianCities  (CvGame.cpp:7483)  <- call CvPlayer::found
- CvGame::doHolyCity  (CvGame.cpp:7213)  <- call CvPlayer::foundReligion
- CvGame::foundBarbarianCity  (CvGame.cpp:10830)  <- call CvPlayer::found
- CvGame::isValidVoteSelection  (CvGame.cpp:5113)  <- call CvPlayer::canStopTradingWithTeam
- CvGame::setAIAutoPlay  (CvGame.cpp:4915)  <- call CvPlayer::setAutoMoves
- CvGame::setFinalInitialized  (CvGame.cpp:5476)  <- call CvMap::updateIrrigated
- CvGame::setVoteOutcome  (CvGame.cpp:6217)  <- call CvGame::processVote
- CvGame::updateMoves  (CvGame.cpp:8106)  <- call CvPlayer::setAutoMoves
- CvGameAI::AI_updateAssignWork  (CvGameAI.cpp:61)  <- call CvPlayerAI::AI_updateAssignWork
- CvGameTextMgr::parseLeaderHeadHelp  (CvGameTextMgr.cpp:16428)  <- call CvGameTextMgr::getActiveDealsString
- CvGameTextMgr::parseLeaderHeadRelationsHelp  (CvGameTextMgr.cpp:16470)  <- call CvGameTextMgr::getActiveDealsString
- CvMap::calculateAreas  (CvMap.cpp:1397)  <- call CvPlot::setArea
- CvMap::doTurn  (CvMap.cpp:330)  <- call CvPlot::doTurn
- CvMap::recalculateAreas  (CvMap.cpp:1203)  <- call CvPlot::setArea
- CvMap::verifyUnitValidPlot  (CvMap.cpp:527)  <- call CvPlot::verifyUnitValidPlot
- CvMapGenerator::addRiver  (CvMapGenerator.cpp:536)  <- call CvMapGenerator::doRiver
- CvMapGenerator::addRivers  (CvMapGenerator.cpp:300)  <- call CvMapGenerator::doRiver
- CvNetAutoMission::Execute  (CvMessageData.cpp:821)  <- call CvSelectionGroup::autoMission
- CvNetAutoMoves::Execute  (CvMessageData.cpp:125)  <- call CvPlayer::setAutoMoves
- CvNetDoCommand::Execute  (CvMessageData.cpp:863)  <- call CvUnit::doCommand
- CvNetFoundReligion::Execute  (CvMessageData.cpp:620)  <- call CvPlayer::foundReligion
- CvNetPushOrder::Execute  (CvMessageData.cpp:185)  <- call CvCity::pushOrder
- CvPlayer::addFreeUnitAI  (CvPlayer.cpp:1945)  <- call CvPlayer::addFreeUnit
- CvPlayer::canDoResolution  (CvPlayer.cpp:23131)  <- call CvPlayer::canStopTradingWithTeam
- CvPlayer::canTradeItem  (CvPlayer.cpp:5413)  <- call CvPlayer::canStopTradingWithTeam
- CvPlayer::changeGoldPerTurnByPlayer  (CvPlayer.cpp:13436)  <- call CvPlayerAI::AI_doCommerce
- CvPlayer::doGold  (CvPlayer.cpp:15287)  <- call CvPlayer::disbandUnit
- CvPlayer::doTurnUnits  (CvPlayer.cpp:4068)  <- call CvPlayerAI::AI_doTurnUnitsPost
- CvPlayer::foundCorporation  (CvPlayer.cpp:9362)  <- call CvCity::setHeadquarters
- CvPlayer::killAllDeals  (CvPlayer.cpp:5997)  <- call CvDeal::kill
- CvPlayer::raze  (CvPlayer.cpp:6151)  <- call CvPlayer::disband
- CvPlayer::setEndTurn  (CvPlayer.cpp:12511)  <- call CvPlayer::setAutoMoves
- CvPlayer::trigger  (CvPlayer.cpp:21800)  <- call CvPlayer::initTriggeredData
- CvPlayer::updateTimers  (CvPlayer.cpp:4434)  <- call CvSelectionGroup::updateTimers
- CvPlayer::verifyAlive  (CvPlayer.cpp:12013)  <- call CvPlayer::setAlive
- CvPlayer::verifyUnitStacksValid  (CvPlayer.cpp:23706)  <- call CvUnit::verifyStackValid
- CvPlayerAI::AI_beginDiplomacy  (CvPlayerAI.cpp:17279)  <- call CvPlayer::handleDiploEvent
- CvPlayerAI::AI_diploVote  (CvPlayerAI.cpp:8037)  <- call CvPlayer::canStopTradingWithTeam
- CvPlayerAI::AI_doMilitary  (CvPlayerAI.cpp:16594)  <- call CvPlayerAI::AI_disbandUnit
- CvPlayerAI::AI_doTurnPre  (CvPlayerAI.cpp:430)  <- call CvPlayerAI::AI_doCommerce
- CvPlot::updateCulture  (CvPlot.cpp:715)  <- call CvPlot::setOwner
- CvPlot::updateSight  (CvPlot.cpp:2094)  <- call CvPlot::changeAdjacentSight
- CvSelectionGroup::deleteMissionQueueNode  (CvSelectionGroup.cpp:6161)  <- call CvSelectionGroup::activateHeadMission
- CvSelectionGroup::doDelayedDeath  (CvSelectionGroup.cpp:582)  <- call CvUnit::doDelayedDeath
- CvSelectionGroup::doTurn  (CvSelectionGroup.cpp:298)  <- call CvUnit::doTurn
- CvSelectionGroup::groupPathTo  (CvSelectionGroup.cpp:4751)  <- call CvSelectionGroup::groupMove
- CvSelectionGroup::groupRoadTo  (CvSelectionGroup.cpp:4839)  <- call CvSelectionGroup::groupBuild
- CvSelectionGroup::insertAtEndMissionQueue  (CvSelectionGroup.cpp:6139)  <- call CvSelectionGroup::activateHeadMission
- CvSelectionGroup::setActivityType  (CvSelectionGroup.cpp:5393)  <- call CvSelectionGroup::airCircle
- CvSelectionGroup::updateMission  (CvSelectionGroup.cpp:774)  <- call CvSelectionGroup::continueMission
- CvSelectionGroupAI::AI_update  (CvSelectionGroupAI.cpp:184)  <- call CvSelectionGroup::groupAttack
- CvTeam::cancelDefensivePacts  (CvTeam.cpp:6990)  <- call CvDeal::kill
- CvTeam::changeIrrigationCount  (CvTeam.cpp:4142)  <- call CvMap::updateIrrigated
- CvTeam::changeResearchProgress  (CvTeam.cpp:5627)  <- call CvTeam::setResearchProgress
- CvTeam::changeStolenVisibilityTimer  (CvTeam.cpp:4302)  <- call CvTeam::setStolenVisibilityTimer
- CvTeam::declareWar  (CvTeam.cpp:1410)  <- call CvDeal::kill
- CvTeam::freeVassal  (CvTeam.cpp:5158)  <- call CvDeal::kill
- CvTeam::setEspionagePointsAgainstTeam  (CvTeam.cpp:7066)  <- call CvTeam::verifySpyUnitsValidPlot
- CvTeam::setVassal  (CvTeam.cpp:4814)  <- call CvDeal::kill
- CvTeam::shareCounters  (CvTeam.cpp:897)  <- call CvTeam::setStolenVisibilityTimer
- CvTeam::updateTechShare  (CvTeam.cpp:6682)  <- call CvTeam::updateTechShare
- CvTeamAI::AI_doWar  (CvTeamAI.cpp:4754)  <- call CvPlayerAI::AI_doPeace
- CvUnit::airStrike  (CvUnit.cpp:13465)  <- call CvUnit::setDamage
- CvUnit::changeDamage  (CvUnit.cpp:11183)  <- call CvUnit::setDamage
- CvUnit::changeExtraVisibilityRange  (CvUnit.cpp:11550)  <- call CvPlot::changeAdjacentSight
- CvUnit::collateralCombat  (CvUnit.cpp:13144)  <- call CvUnit::setDamage
- CvUnit::doVictoryInfluence  (CvUnit.cpp:16746)  <- call CvCity::emergencyConscript
- CvUnit::interceptTest  (CvUnit.cpp:13387)  <- call CvUnit::fightInterceptor
- CvUnit::resolveCombat  (CvUnit.cpp:1257)  <- call CvUnit::setDamage
- CvUnit::setFacingDirection  (CvUnit.cpp:11915)  <- call CvPlot::changeAdjacentSight
- CvUnit::setReconPlot  (CvUnit.cpp:11096)  <- call CvPlot::changeAdjacentSight
- CvUnitAI::AI_barbAttackSeaMove  (CvUnitAI.cpp:5966)  <- call CvUnit::scrap
- CvUnitAI::AI_doInquisition  (CvUnitAI.cpp:14097)  <- call CvUnit::performInquisition
- CvUnitAI::AI_escortSeaMove  (CvUnitAI.cpp:6687)  <- call CvUnit::scrap
- CvUnitAI::AI_exploreMove  (CvUnitAI.cpp:4611)  <- call CvUnit::scrap
- CvUnitAI::AI_exploreSeaMove  (CvUnitAI.cpp:6922)  <- call CvUnit::scrap
- CvUnitAI::AI_settleMove  (CvUnitAI.cpp:1389)  <- call CvUnit::scrap
- CvUnitAI::AI_settlerSeaMove  (CvUnitAI.cpp:7855)  <- call CvUnit::scrap
- CvUnitAI::AI_spyMove  (CvUnitAI.cpp:5568)  <- call CvUnitAI::AI_revoltCitySpy
- CvUnitAI::AI_switchHurry  (CvUnitAI.cpp:13917)  <- call CvCity::pushOrder
- CvUnitAI::AI_upgrade  (CvUnitAI.cpp:617)  <- call CvUnit::doDelayedDeath
- CvUnitAI::AI_workerMove  (CvUnitAI.cpp:1547)  <- call CvUnit::scrap
- CvUnitAI::AI_workerSeaMove  (CvUnitAI.cpp:5850)  <- call CvUnit::scrap
- CyCity::clearOrderQueue  (CyCity.cpp:2650)  <- call CvCity::clearOrderQueue
- CyCity::liberate  (CyCity.cpp:2814)  <- call CvCity::liberate
- CyCity::pushOrder  (CyCity.cpp:2656)  <- call CvCity::pushOrder
- CyCity::setProductionAutomated  (CyCity.cpp:1845)  <- call CvCity::setProductionAutomated
- CyDeal::kill  (CyDeal.cpp:91)  <- call CvDeal::kill
- CyGame::addPlayer  (CyGame.cpp:1166)  <- call CvGame::addPlayer
- CyGame::changeHumanPlayer  (CyGame.cpp:1174)  <- call CvGame::changeHumanPlayer
- CyGame::regenerateMap  (CyGame.cpp:1285)  <- call CvGame::regenerateMap
- CyGame::reviveActivePlayer  (CyGame.cpp:293)  <- call CvGame::reviveActivePlayer
- CyGameTextMgr::getActiveDealsString  (CyGameTextMgr.cpp:250)  <- call CvGameTextMgr::getActiveDealsString
- CyMapGenerator::addBonuses  (CyMapGenerator.cpp:69)  <- call CvMapGenerator::addBonuses
- CyMapGenerator::doRiver  (CyMapGenerator.cpp:57)  <- call CvMapGenerator::doRiver
- CyMapGenerator::eraseGoodies  (CyMapGenerator.cpp:111)  <- call CvMapGenerator::eraseGoodies
- CyMapGenerator::eraseRivers  (CyMapGenerator.cpp:93)  <- call CvMapGenerator::eraseRivers
- CyMapGenerator::generateRandomMap  (CyMapGenerator.cpp:117)  <- call CvMapGenerator::generateRandomMap
- CyPlayer::canStopTradingWithTeam  (CyPlayer.cpp:441)  <- call CvPlayer::canStopTradingWithTeam
- CyPlayer::createGreatPeople  (CyPlayer.cpp:1127)  <- call CvPlayer::createGreatPeople
- CyPlayer::disband  (CyPlayer.cpp:485)  <- call CvPlayer::disband
- CyPlayer::disbandUnit  (CyPlayer.cpp:175)  <- call CvPlayer::disbandUnit
- CyPlayer::doGoody  (CyPlayer.cpp:502)  <- call CvPlayer::doGoody
- CyPlayer::forcePeace  (CyPlayer.cpp:2536)  <- call CvPlayer::forcePeace
- CyPlayer::found  (CyPlayer.cpp:513)  <- call CvPlayer::found
- CyPlayer::foundReligion  (CyPlayer.cpp:813)  <- call CvPlayer::foundReligion
- CyPlayer::initTriggeredData  (CyPlayer.cpp:2279)  <- call CvPlayer::initTriggeredData
- CyPlayer::killCities  (CyPlayer.cpp:159)  <- call CvPlayer::killCities
- CyPlayer::killUnits  (CyPlayer.cpp:180)  <- call CvPlayer::killUnits
- CyPlayer::setAlive  (CyPlayer.cpp:1651)  <- call CvPlayer::setAlive
- CyPlayer::setNewPlayerAlive  (CyPlayer.cpp:1658)  <- call CvPlayer::setNewPlayerAlive
- CyPlot::setOwner  (CyPlot.cpp:615)  <- call CvPlot::setOwner
- CyPlot::setOwnerNoUnitCheck  (CyPlot.cpp:621)  <- call CvPlot::setOwner
- CyTeam::assignVassal  (CyTeam.cpp:714)  <- call CvTeam::assignVassal
- CyTeam::setResearchProgress  (CyTeam.cpp:833)  <- call CvTeam::setResearchProgress
- CyTeam::signDefensivePact  (CyTeam.cpp:93)  <- call CvTeam::signDefensivePact
- CyTeam::signOpenBorders  (CyTeam.cpp:87)  <- call CvTeam::signOpenBorders
- CyTeamPythonInterface  (CyTeamInterface.cpp:10)  <- call CyTeam::addTeam
- CyUnit::convert  (CyUnit.cpp:29)  <- call CvUnit::convert
- CyUnit::doCommand  (CyUnit.cpp:67)  <- call CvUnit::doCommand
- CyUnit::gift  (CyUnit.cpp:138)  <- call CvUnit::gift
- CyUnit::lead  (CyUnit.cpp:459)  <- call CvUnit::lead
- CyUnit::setDamage  (CyUnit.cpp:1239)  <- call CvUnit::setDamage
- joinArea  (CvGameCoreUtils.cpp:2564)  <- call CvPlot::setArea

### level 6 (108)

- CvArea::changeBorderObstacleCount  (CvArea.cpp:731)  <- call CvMap::verifyUnitValidPlot
- CvCity::doGreatPeople  (CvCity.cpp:13991)  <- call CvCity::createGreatPeople
- CvCity::setEspionageVisibility  (CvCity.cpp:10931)  <- call CvPlot::updateSight
- CvCity::setNumFreeBuilding  (CvCity.cpp:12284)  <- call CvCity::processBuilding
- CvCityAI::AI_chooseDefender  (CvCityAI.cpp:9488)  <- call CvCityAI::AI_chooseUnit
- CvCityAI::AI_chooseLeastRepresentedUnit  (CvCityAI.cpp:9514)  <- call CvCityAI::AI_chooseUnit
- CvCityAI::AI_doDraft  (CvCityAI.cpp:8436)  <- call CvCity::conscript
- CvCityAI::AI_doPanic  (CvCityAI.cpp:12033)  <- call CvCityAI::AI_chooseUnit
- CvDLLButtonPopup::launchRazeCityPopup  (CvDLLButtonPopup.cpp:1400)  <- call CvPlayer::raze
- CvDLLWidgetData::parseLeaderheadHelp  (CvDLLWidgetData.cpp:6025)  <- call CvGameTextMgr::parseLeaderHeadHelp
- CvDLLWidgetData::parseLeaderheadRelationsHelp  (CvDLLWidgetData.cpp:6036)  <- call CvGameTextMgr::parseLeaderHeadRelationsHelp
- CvDeal::endTrade  (CvDeal.cpp:1098)  <- call CvPlayer::changeGoldPerTurnByPlayer
- CvDllPythonEvents::reportBeginPlayerTurn  (CvDllPythonEvents.cpp:196)  <- event RoMEventManager.py RoMEventManager.onBeginPlayerTurn
- CvDllPythonEvents::reportBuildingBuilt  (CvDllPythonEvents.cpp:1058)  <- event RoMEventManager.py RoMEventManager.onBuildingBuilt
- CvDllPythonEvents::reportCityAcquired  (CvDllPythonEvents.cpp:499)  <- event Revolution/Gameready/BarbarianCiv.py BarbarianCiv.onCityAcquired
- CvDllPythonEvents::reportSetPlayerAlive  (CvDllPythonEvents.cpp:1273)  <- event Revolution/Gameready/StartAsMinors.py onSetPlayerAlive
- CvEventReporter::cityLost  (CvEventReporter.cpp:229)  <- call CvDllPythonEvents::reportCityLost
- CvEventReporter::projectBuilt  (CvEventReporter.cpp:389)  <- call CvDllPythonEvents::reportProjectBuilt
- CvGame::addVoteSelection  (CvGame.cpp:10188)  <- call CvGame::isValidVoteSelection
- CvGame::addVoteTriggered  (CvGame.cpp:10350)  <- call CvPlayerAI::AI_diploVote
- CvGame::canDoResolution  (CvGame.cpp:5070)  <- call CvPlayer::canDoResolution
- CvGame::changeAIAutoPlay  (CvGame.cpp:4965)  <- call CvGame::setAIAutoPlay
- CvGame::clearSecretaryGeneral  (CvGame.cpp:3815)  <- call CvGame::setVoteOutcome
- CvGame::doHeadquarters  (CvGame.cpp:7345)  <- call CvPlayer::foundCorporation
- CvGame::doVoteResults  (CvGame.cpp:10389)  <- call CvGame::setVoteOutcome
- CvGame::setHeadquarters  (CvGame.cpp:6605)  <- call CvCity::setHasCorporation
- CvGame::testAlive  (CvGame.cpp:8222)  <- call CvPlayer::verifyAlive
- CvGame::updateTimers  (CvGame.cpp:8178)  <- call CvPlayer::updateTimers
- CvGame::updateTurnTimer  (CvGame.cpp:8192)  <- call CvPlayer::setEndTurn
- CvGame::updateWar  (CvGame.cpp:8073)  <- call CvTeam::declareWar
- CvGameTextMgr::setBonusTradeHelp  (CvGameTextMgr.cpp:13296)  <- call CvPlayer::canTradeItem
- CvGameTextMgr::setTechTradeHelp  (CvGameTextMgr.cpp:8365)  <- call CvPlayer::canTradeItem
- CvMap::init  (CvMap.cpp:65)  <- call CvMap::calculateAreas
- CvMap::setup  (CvMap.cpp:245)  <- call joinArea
- CvMap::updateSight  (CvMap.cpp:418)  <- call CvPlot::updateSight
- CvNetChangeVassal::Execute  (CvMessageData.cpp:975)  <- call CvTeam::setVassal
- CvNetChangeWar::Execute  (CvMessageData.cpp:1080)  <- call CvTeam::declareWar
- CvNetTurnComplete::Execute  (CvMessageData.cpp:153)  <- call CvPlayer::setEndTurn
- CvPlayer::buildTradeTable  (CvPlayer.cpp:23774)  <- call CvPlayer::canTradeItem
- CvPlayer::doResearch  (CvPlayer.cpp:15358)  <- call CvTeam::changeResearchProgress
- CvPlayer::findNewCapital  (CvPlayer.cpp:6012)  <- call CvCity::setNumRealBuilding
- CvPlayer::removeBuildingClass  (CvPlayer.cpp:7705)  <- call CvCity::setNumRealBuilding
- CvPlayer::setCombatExperience  (CvPlayer.cpp:11673)  <- call CvCity::createGreatPeople
- CvPlayer::updateCitySight  (CvPlayer.cpp:4358)  <- call CvPlot::updateSight
- CvPlayerAI::AI_unitUpdate  (CvPlayerAI.cpp:1572)  <- call CvSelectionGroupAI::AI_update
- CvPlayerAI::AI_wakePlotTargetMissionAIs  (CvPlayerAI.cpp:13226)  <- call CvSelectionGroup::setActivityType
- CvPlot::changeCultureRangeCities  (CvPlot.cpp:8523)  <- call CvPlot::updateCulture
- CvPlot::processArea  (CvPlot.cpp:9063)  <- call CvArea::changeNumTiles
- CvPlot::setCulture  (CvPlot.cpp:6785)  <- call CvPlot::updateCulture
- CvPlot::updateSeeFromSight  (CvPlot.cpp:2179)  <- call CvPlot::updateSight
- CvSelectionGroup::deactivateHeadMission  (CvSelectionGroup.cpp:6341)  <- call CvSelectionGroup::setActivityType
- CvSelectionGroup::deleteUnitNode  (CvSelectionGroup.cpp:5721)  <- call CvSelectionGroup::setActivityType
- CvSelectionGroup::groupDeclareWar  (CvSelectionGroup.cpp:4301)  <- call CvTeam::declareWar
- CvSelectionGroup::popMission  (CvSelectionGroup.cpp:703)  <- call CvSelectionGroup::deleteMissionQueueNode
- CvSelectionGroup::pushMission  (CvSelectionGroup.cpp:651)  <- call CvSelectionGroup::doDelayedDeath
- CvSelectionGroup::setAutomateType  (CvSelectionGroup.cpp:5476)  <- call CvSelectionGroup::setActivityType
- CvTeam::changeAliveCount  (CvTeam.cpp:3777)  <- call CvTeam::setVassal
- CvTeam::changeEspionagePointsAgainstTeam  (CvTeam.cpp:7080)  <- call CvTeam::setEspionagePointsAgainstTeam
- CvTeam::changeObsoleteBuildingCount  (CvTeam.cpp:5542)  <- call CvCity::processBuilding
- CvTeam::changeResearchProgressPercent  (CvTeam.cpp:5632)  <- call CvTeam::changeResearchProgress
- CvTeam::changeTechShareCount  (CvTeam.cpp:4376)  <- call CvTeam::updateTechShare
- CvTeam::doTurn  (CvTeam.cpp:1050)  <- call CvTeam::changeStolenVisibilityTimer
- CvTeam::init  (CvTeam.cpp:130)  <- call CvTeam::declareWar
- CvTeam::makeHasMet  (CvTeam.cpp:4469)  <- call CvTeam::updateTechShare
- CvTeam::makePeace  (CvTeam.cpp:1909)  <- call CvMap::verifyUnitValidPlot
- CvTeam::setIsMinorCiv  (CvTeam.cpp:3369)  <- call CvTeam::declareWar
- CvTeam::setOpenBorders  (CvTeam.cpp:4659)  <- call CvMap::verifyUnitValidPlot
- CvTeamAI::AI_chooseElection  (CvTeamAI.cpp:1173)  <- call CvPlayerAI::AI_diploVote
- CvTeamAI::AI_doTurnPost  (CvTeamAI.cpp:188)  <- call CvTeamAI::AI_doWar
- CvUnit::doHeal  (CvUnit.cpp:4134)  <- call CvUnit::changeDamage
- CvUnit::joinGroup  (CvUnit.cpp:10424)  <- call CvSelectionGroup::setActivityType
- CvUnit::resolveAirCombat  (CvUnit.cpp:953)  <- call CvUnit::changeDamage
- CvUnit::rotateFacingDirectionClockwise  (CvUnit.cpp:11942)  <- call CvUnit::setFacingDirection
- CvUnit::rotateFacingDirectionCounterClockwise  (CvUnit.cpp:11949)  <- call CvUnit::setFacingDirection
- CvUnit::setHasPromotion  (CvUnit.cpp:12735)  <- call CvUnit::changeExtraVisibilityRange
- CvUnit::setPromotionReady  (CvUnit.cpp:12009)  <- call CvSelectionGroup::setActivityType
- CvUnit::setTransportUnit  (CvUnit.cpp:12322)  <- call CvSelectionGroup::setActivityType
- CvUnit::unloadAll  (CvUnit.cpp:3822)  <- call CvSelectionGroup::setActivityType
- CvUnitAI::AI_assaultSeaMove  (CvUnitAI.cpp:7104)  <- call CvUnitAI::AI_barbAttackSeaMove
- CvUnitAI::AI_carrierSeaTransport  (CvUnitAI.cpp:18795)  <- call CvSelectionGroupAI::AI_update
- CvUnitAI::AI_engineerMove  (CvUnitAI.cpp:5453)  <- call CvUnitAI::AI_switchHurry
- CvUnitAI::AI_handleSettlerTransport  (CvUnitAI.cpp:7819)  <- call CvUnitAI::AI_settlerSeaMove
- CvUnitAI::AI_missionaryMove  (CvUnitAI.cpp:4763)  <- call CvUnitAI::AI_doInquisition
- CvUnitAI::AI_poach  (CvUnitAI.cpp:24236)  <- call CvTeam::declareWar
- CvUnitAI::AI_update  (CvUnitAI.cpp:195)  <- call CvUnitAI::AI_settleMove
- CyCity::clearWorkingOverride  (CyCity.cpp:243)  <- call CvCity::clearWorkingOverride
- CyCity::conscript  (CyCity.cpp:581)  <- call CvCity::conscript
- CyCity::createGreatPeople  (CyCity.cpp:210)  <- call CvCity::createGreatPeople
- CyCity::setHasCorporation  (CyCity.cpp:2629)  <- call CvCity::setHasCorporation
- CyCity::setNumRealBuilding  (CyCity.cpp:2602)  <- call CvCity::setNumRealBuilding
- CyGame::setAIAutoPlay  (CyGame.cpp:570)  <- call CvGame::setAIAutoPlay
- CyMap::recalculateAreas  (CyMap.cpp:270)  <- call CvMap::recalculateAreas
- CyMap::verifyUnitValidPlot  (CyMap.cpp:51)  <- call CvMap::verifyUnitValidPlot
- CyMapGenerator::addRivers  (CyMapGenerator.cpp:51)  <- call CvMapGenerator::addRivers
- CyPlayer::canTradeItem  (CyPlayer.cpp:406)  <- call CvPlayer::canTradeItem
- CyPlayer::foundCorporation  (CyPlayer.cpp:834)  <- call CvPlayer::foundCorporation
- CyPlayer::killAllDeals  (CyPlayer.cpp:452)  <- call CvPlayer::killAllDeals
- CyPlayer::raze  (CyPlayer.cpp:479)  <- call CvPlayer::raze
- CyPlayer::trigger  (CyPlayer.cpp:2252)  <- call CvPlayer::trigger
- CySelectionGroup::setActivityType  (CySelectionGroup.cpp:241)  <- call CvSelectionGroup::setActivityType
- CyTeam::changeIrrigationCount  (CyTeam.cpp:506)  <- call CvTeam::changeIrrigationCount
- CyTeam::changeResearchProgress  (CyTeam.cpp:839)  <- call CvTeam::changeResearchProgress
- CyTeam::declareWar  (CyTeam.cpp:64)  <- call CvTeam::declareWar
- CyTeam::freeVassal  (CyTeam.cpp:722)  <- call CvTeam::freeVassal
- CyTeam::setEspionagePointsAgainstTeam  (CyTeam.cpp:927)  <- call CvTeam::setEspionagePointsAgainstTeam
- CyTeam::setVassal  (CyTeam.cpp:706)  <- call CvTeam::setVassal
- CyUnit::changeDamage  (CyUnit.cpp:1245)  <- call CvUnit::changeDamage
- CyUnit::setReconPlot  (CyUnit.cpp:1223)  <- call CvUnit::setReconPlot

### level 7 (219)

- CvCity::addProductionExperience  (CvCity.cpp:2970)  <- call CvUnit::setHasPromotion
- CvCity::setCultureLevel  (CvCity.cpp:8866)  <- call CvPlot::changeCultureRangeCities
- CvCity::updateEspionageVisibility  (CvCity.cpp:10946)  <- call CvCity::setEspionageVisibility
- CvDLLButtonPopup::launchButtonPopup  (CvDLLButtonPopup.cpp:855)  <- call CvDLLButtonPopup::launchRazeCityPopup
- CvDLLWidgetData::parseBonusTradeHelp  (CvDLLWidgetData.cpp:5639)  <- call CvGameTextMgr::setBonusTradeHelp
- CvDLLWidgetData::parseTechTradeEntryHelp  (CvDLLWidgetData.cpp:5282)  <- call CvGameTextMgr::setTechTradeHelp
- CvDllPythonEvents::reportCityRazed  (CvDllPythonEvents.cpp:483)  <- event base/CvEventManager.py CvEventManager.onCityRazed
- CvDllPythonEvents::reportEndGameTurn  (CvDllPythonEvents.cpp:167)  <- event Revolution/RevEvents.py onEndGameTurn
- CvDllPythonEvents::reportEndPlayerTurn  (CvDllPythonEvents.cpp:208)  <- event Revolution/Gameready/Revolution.py Revolution.onEndPlayerTurn
- CvDllPythonEvents::reportKbdEvent  (CvDllPythonEvents.cpp:30)  <- event base/CvEventManager.py CvEventManager.onKbdEvent
- CvDllPythonEvents::reportModNetMessage  (CvDllPythonEvents.cpp:75)  <- event Revolution/Gameready/Revolution.py Revolution.onModNetMessage
- CvEventReporter::beginPlayerTurn  (CvEventReporter.cpp:118)  <- call CvDllPythonEvents::reportBeginPlayerTurn
- CvEventReporter::buildingBuilt  (CvEventReporter.cpp:382)  <- call CvDllPythonEvents::reportBuildingBuilt
- CvEventReporter::cityAcquired  (CvEventReporter.cpp:218)  <- call CvDllPythonEvents::reportCityAcquired
- CvEventReporter::setPlayerAlive  (CvEventReporter.cpp:452)  <- call CvDllPythonEvents::reportSetPlayerAlive
- CvGame::addVoteTriggered  (CvGame.cpp:10340)  <- call CvGame::addVoteTriggered
- CvGame::doDiploVote  (CvGame.cpp:7475)  <- call CvGame::doVoteResults
- CvGame::doVoteSelection  (CvGame.cpp:10611)  <- call CvGame::addVoteSelection
- CvGame::updateCitySight  (CvGame.cpp:3220)  <- call CvPlayer::updateCitySight
- CvGame::updateSecretaryGeneral  (CvGame.cpp:3838)  <- call CvGame::clearSecretaryGeneral
- CvGameTextMgr::setBonusHelp  (CvGameTextMgr.cpp:13291)  <- call CvGameTextMgr::setBonusTradeHelp
- CvGameTextMgr::setTechHelp  (CvGameTextMgr.cpp:8359)  <- call CvGameTextMgr::setTechTradeHelp
- CvMap::rebuild  (CvMap.cpp:1378)  <- call CvMap::init
- CvNetJoinGroup::Execute  (CvMessageData.cpp:721)  <- call CvUnit::joinGroup
- CvNetPushMission::Execute  (CvMessageData.cpp:769)  <- call CvSelectionGroup::pushMission
- CvPlayer::changeCombatExperience  (CvPlayer.cpp:11726)  <- call CvPlayer::setCombatExperience
- CvPlayer::changeFreeBuildingCount  (CvPlayer.cpp:13596)  <- call CvCity::setNumFreeBuilding
- CvPlayer::doEspionagePoints  (CvPlayer.cpp:15421)  <- call CvTeam::changeEspionagePointsAgainstTeam
- CvPlayer::processBuilding  (CvPlayer.cpp:7739)  <- call CvArea::changeBorderObstacleCount
- CvPlayer::resetPlotAndCityData  (CvPlayer.cpp:704)  <- call CvPlot::setCulture
- CvPlayer::setTeam  (CvPlayer.cpp:12861)  <- call CvTeam::changeAliveCount
- CvPlot::changeCulture  (CvPlot.cpp:6823)  <- call CvPlot::setCulture
- CvSelectionGroup::clearMissionQueue  (CvSelectionGroup.cpp:6099)  <- call CvSelectionGroup::deactivateHeadMission
- CvSelectionGroup::clearUnits  (CvSelectionGroup.cpp:5625)  <- call CvSelectionGroup::deleteUnitNode
- CvSelectionGroup::groupAmphibMove  (CvSelectionGroup.cpp:5173)  <- call CvSelectionGroup::pushMission
- CvSelectionGroup::mergeIntoGroup  (CvSelectionGroup.cpp:5761)  <- call CvUnit::joinGroup
- CvSelectionGroup::removeUnit  (CvSelectionGroup.cpp:5700)  <- call CvSelectionGroup::deleteUnitNode
- CvSelectionGroup::setTransportUnit  (CvSelectionGroup.cpp:4982)  <- call CvUnit::setTransportUnit
- CvSelectionGroup::splitGroup  (CvSelectionGroup.cpp:5811)  <- call CvUnit::joinGroup
- CvSelectionGroup::unloadAll  (CvSelectionGroup.cpp:3968)  <- call CvUnit::unloadAll
- CvSelectionGroupAI::AI_ejectBestDefender  (CvSelectionGroupAI.cpp:897)  <- call CvUnit::joinGroup
- CvSelectionGroupAI::AI_separate  (CvSelectionGroupAI.cpp:64)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateAI  (CvSelectionGroupAI.cpp:111)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateEmptyTransports  (CvSelectionGroupAI.cpp:157)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateImpassable  (CvSelectionGroupAI.cpp:134)  <- call CvSelectionGroup::pushMission
- CvSelectionGroupAI::AI_separateNonAI  (CvSelectionGroupAI.cpp:89)  <- call CvSelectionGroup::pushMission
- CvTeam::changeExtraWaterSeeFromCount  (CvTeam.cpp:3946)  <- call CvMap::updateSight
- CvTeam::changeProjectCount  (CvTeam.cpp:5330)  <- call CvTeam::changeTechShareCount
- CvTeam::meet  (CvTeam.cpp:2220)  <- call CvTeam::makeHasMet
- CvTeamAI::AI_reviewWars  (CvTeamAI.cpp:4132)  <- call CvTeam::makePeace
- CvUnit::automate  (CvUnit.cpp:3405)  <- call CvSelectionGroup::setAutomateType
- CvUnit::cheat  (CvUnit.cpp:14412)  <- call CvUnit::setPromotionReady
- CvUnit::influencePlots  (CvUnit.cpp:16883)  <- call CvPlot::setCulture
- CvUnit::load  (CvUnit.cpp:3718)  <- call CvUnit::setTransportUnit
- CvUnit::loadUnit  (CvUnit.cpp:3628)  <- call CvUnit::setTransportUnit
- CvUnit::testPromotionReady  (CvUnit.cpp:12035)  <- call CvUnit::setPromotionReady
- CvUnit::unload  (CvUnit.cpp:3800)  <- call CvUnit::setTransportUnit
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
- CvUnitAI::AI_carrierSeaMove  (CvUnitAI.cpp:8421)  <- call CvSelectionGroup::pushMission
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
- CvUnitAI::AI_missileCarrierSeaMove  (CvUnitAI.cpp:8544)  <- call CvSelectionGroup::pushMission
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
- CvUnitAI::AI_recruitSettlerEscort  (CvUnitAI.cpp:11029)  <- call CvUnit::joinGroup
- CvUnitAI::AI_reinforceOperation  (CvUnitAI.cpp:2125)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_reserveMove  (CvUnitAI.cpp:3877)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_reserveSeaMove  (CvUnitAI.cpp:6472)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_retreatToCity  (CvUnitAI.cpp:20519)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_routeCity  (CvUnitAI.cpp:20251)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_routeTerritory  (CvUnitAI.cpp:20311)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_safety  (CvUnitAI.cpp:14684)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_scientistMove  (CvUnitAI.cpp:5064)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_seaBombardRange  (CvUnitAI.cpp:16586)  <- call CvSelectionGroup::pushMission
- CvUnitAI::AI_separateSettlerTransports  (CvUnitAI.cpp:7790)  <- call CvUnit::joinGroup
- CvUnitAI::AI_setUnitAIType  (CvUnitAI.cpp:1246)  <- call CvUnit::joinGroup
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
- CyGame::clearHeadquarters  (CyGame.cpp:974)  <- call CvGame::setHeadquarters
- CyGame::setHeadquarters  (CyGame.cpp:968)  <- call CvGame::setHeadquarters
- CyPlayer::findNewCapital  (CyPlayer.cpp:463)  <- call CvPlayer::findNewCapital
- CyPlayer::removeBuildingClass  (CyPlayer.cpp:574)  <- call CvPlayer::removeBuildingClass
- CyPlayer::setCombatExperience  (CyPlayer.cpp:2092)  <- call CvPlayer::setCombatExperience
- CyPlot::setCulture  (CyPlot.cpp:894)  <- call CvPlot::setCulture
- CySelectionGroup::popMission  (CySelectionGroup.cpp:38)  <- call CvSelectionGroup::popMission
- CySelectionGroup::pushMission  (CySelectionGroup.cpp:26)  <- call CvSelectionGroup::pushMission
- CySelectionGroup::pushMoveToMission  (CySelectionGroup.cpp:32)  <- call CvSelectionGroup::pushMission
- CySelectionGroup::setAutomateType  (CySelectionGroup.cpp:257)  <- call CvSelectionGroup::setAutomateType
- CySelectionGroupInterface  (CySelectionGroupInterface.cpp:15)  <- call CySelectionGroup::setActivityType
- CyTeam::changeEspionagePointsAgainstTeam  (CyTeam.cpp:933)  <- call CvTeam::changeEspionagePointsAgainstTeam
- CyTeam::changeTechShareCount  (CyTeam.cpp:631)  <- call CvTeam::changeTechShareCount
- CyTeam::makePeace  (CyTeam.cpp:70)  <- call CvTeam::makePeace
- CyTeam::setIsMinorCiv  (CyTeam.cpp:266)  <- call CvTeam::setIsMinorCiv
- CyUnit::rotateFacingDirectionClockwise  (CyUnit.cpp:1316)  <- call CvUnit::rotateFacingDirectionClockwise
- CyUnit::rotateFacingDirectionCounterClockwise  (CyUnit.cpp:1322)  <- call CvUnit::rotateFacingDirectionCounterClockwise
- CyUnit::setHasPromotion  (CyUnit.cpp:1726)  <- call CvUnit::setHasPromotion
- CyUnit::setPromotionReady  (CyUnit.cpp:1566)  <- call CvUnit::setPromotionReady
- CyUnit::setTransportUnit  (CyUnit.cpp:1623)  <- call CvUnit::setTransportUnit
- `anonymous namespace'::setOperationalGeneralBadge  (CvPlayerAI.cpp:15704)  <- call CvUnit::setHasPromotion

### level 8 (45)

- CvCity::doPlotCulture  (CvCity.cpp:13563)  <- call CvPlot::changeCulture
- CvCity::updateCultureLevel  (CvCity.cpp:9000)  <- call CvCity::setCultureLevel
- CvDLLWidgetData::parseBonusHelp  (CvDLLWidgetData.cpp:5630)  <- call CvGameTextMgr::setBonusHelp
- CvDLLWidgetData::parseResearchHelp  (CvDLLWidgetData.cpp:3433)  <- call CvGameTextMgr::setTechHelp
- CvDLLWidgetData::parseTechEntryHelp  (CvDLLWidgetData.cpp:5273)  <- call CvGameTextMgr::setTechHelp
- CvDLLWidgetData::parseTechTreeHelp  (CvDLLWidgetData.cpp:3458)  <- call CvGameTextMgr::setTechHelp
- CvDLLWidgetData::parseTechTreePrereq  (CvDLLWidgetData.cpp:5301)  <- call CvGameTextMgr::setTechHelp
- CvDllPythonEvents::reportBeginGameTurn  (CvDllPythonEvents.cpp:156)  <- event Revolution/Gameready/TechDiffusion.py TechDiffusion.onBeginGameTurn
- CvDllPythonEvents::reportTechAcquired  (CvDllPythonEvents.cpp:1094)  <- event Revolution/Gameready/StartAsMinors.py onTechAcquired
- CvDllPythonEvents::reportVictory  (CvDllPythonEvents.cpp:1247)  <- event Revolution/Gameready/AIAutoPlay.py AIAutoPlay.onVictory
- CvEventReporter::cityRazed  (CvEventReporter.cpp:211)  <- call CvDllPythonEvents::reportCityRazed
- CvEventReporter::endGameTurn  (CvEventReporter.cpp:100)  <- call CvDllPythonEvents::reportEndGameTurn
- CvEventReporter::endPlayerTurn  (CvEventReporter.cpp:123)  <- call CvDllPythonEvents::reportEndPlayerTurn
- CvEventReporter::kbdEvent  (CvEventReporter.cpp:34)  <- call CvDllPythonEvents::reportKbdEvent
- CvEventReporter::reportModNetMessage  (CvEventReporter.cpp:64)  <- call CvDllPythonEvents::reportModNetMessage
- CvGame::setVoteChosen  (CvGame.cpp:6465)  <- call CvGame::addVoteTriggered
- CvGameTextMgr::getBonusDataForWB  (CvGameTextMgr.cpp:20107)  <- call CvGameTextMgr::setBonusHelp
- CvGameTextMgr::getTechDataForWB  (CvGameTextMgr.cpp:20085)  <- call CvGameTextMgr::setTechHelp
- CvPlayer::getResourceLayerColors  (CvPlayer.cpp:24549)  <- call CvGameTextMgr::setBonusHelp
- CvPlayer::setCivics  (CvPlayer.cpp:14261)  <- call CvGame::updateSecretaryGeneral
- CvPlayer::setLastStateReligion  (CvPlayer.cpp:12729)  <- call CvGame::updateSecretaryGeneral
- CvPlayer::setLoyalMember  (CvPlayer.cpp:14155)  <- call CvGame::updateSecretaryGeneral
- CvPlayerAI::AI_convertUnitAITypesForCrush  (CvPlayerAI.cpp:23165)  <- call CvUnitAI::AI_setUnitAIType
- CvTeam::resetVictoryProgress  (CvTeam.cpp:5852)  <- call CvTeam::changeProjectCount
- CvUnit::awardSpyExperience  (CvUnit.cpp:7187)  <- call CvUnit::testPromotionReady
- CvUnit::changeExperience  (CvUnit.cpp:11261)  <- call CvPlayer::changeCombatExperience
- CvUnit::doPillageInfluence  (CvUnit.cpp:16996)  <- call CvPlot::changeCulture
- CvUnit::giveExperience  (CvUnit.cpp:7901)  <- call CvUnit::testPromotionReady
- CvUnitAI::AI_afterAttack  (CvUnitAI.cpp:12673)  <- call CvUnitAI::AI_guardCity
- CvUnitAI::AI_chokeDefend  (CvUnitAI.cpp:12496)  <- call CvUnitAI::AI_anyAttack
- CvUnitAI::AI_clearSettlerSeaLoads  (CvUnitAI.cpp:18117)  <- call CvSelectionGroup::clearMissionQueue
- CvUnitAI::AI_connectBonus  (CvUnitAI.cpp:20166)  <- call CvUnitAI::AI_connectPlot
- CvUnitAI::AI_connectCity  (CvUnitAI.cpp:20208)  <- call CvUnitAI::AI_connectPlot
- CvUnitAI::AI_loadForCoastalAttack  (CvUnitAI.cpp:10856)  <- call CvUnitAI::AI_load
- CyCity::addProductionExperience  (CyCity.cpp:397)  <- call CvCity::addProductionExperience
- CyGameTextMgr::getBonusHelp  (CyGameTextMgr.cpp:121)  <- call CvGameTextMgr::setBonusHelp
- CyGameTextMgr::getTechHelp  (CyGameTextMgr.cpp:76)  <- call CvGameTextMgr::setTechHelp
- CyMap::rebuild  (CyMap.cpp:289)  <- call CvMap::rebuild
- CyPlayer::changeCombatExperience  (CyPlayer.cpp:2083)  <- call CvPlayer::changeCombatExperience
- CyPlot::changeCulture  (CyPlot.cpp:900)  <- call CvPlot::changeCulture
- CySelectionGroup::clearMissionQueue  (CySelectionGroup.cpp:289)  <- call CvSelectionGroup::clearMissionQueue
- CyTeam::changeExtraWaterSeeFromCount  (CyTeam.cpp:362)  <- call CvTeam::changeExtraWaterSeeFromCount
- CyTeam::changeProjectCount  (CyTeam.cpp:787)  <- call CvTeam::changeProjectCount
- CyTeam::meet  (CyTeam.cpp:81)  <- call CvTeam::meet
- CyUnit::setUnitAIType  (CyUnit.cpp:1737)  <- call CvUnitAI::AI_setUnitAIType

### level 9 (21)

- CvCity::setCultureTimes100  (CvCity.cpp:10758)  <- call CvCity::doPlotCulture
- CvCity::setOccupationTimer  (CvCity.cpp:8517)  <- call CvCity::updateCultureLevel
- CvDllPythonEvents::reportGameStart  (CvDllPythonEvents.cpp:124)  <- event Revolution/Gameready/AIAutoPlay.py AIAutoPlay.onGameStart
- CvEventReporter::beginGameTurn  (CvEventReporter.cpp:94)  <- call CvDllPythonEvents::reportBeginGameTurn
- CvEventReporter::techAcquired  (CvEventReporter.cpp:394)  <- call CvDllPythonEvents::reportTechAcquired
- CvEventReporter::victory  (CvEventReporter.cpp:479)  <- call CvDllPythonEvents::reportVictory
- CvGame::testVictory  (CvGame.cpp:8557)  <- call CvTeam::resetVictoryProgress
- CvNetChooseElection::Execute  (CvMessageData.cpp:1014)  <- call CvGame::setVoteChosen
- CvNetModNetMessage::Execute  (CvMessageData.cpp:524)  <- call CvEventReporter::reportModNetMessage
- CvPlayer::convert  (CvPlayer.cpp:9086)  <- call CvPlayer::setLastStateReligion
- CvPlayer::getGlobeLayerColors  (CvPlayer.cpp:24307)  <- call CvPlayer::getResourceLayerColors
- CvPlayer::resetCivTypeEffects  (CvPlayer.cpp:1479)  <- call CvPlayer::setCivics
- CvPlayer::revolution  (CvPlayer.cpp:8924)  <- call CvPlayer::setCivics
- CvPlayer::setDefiedResolution  (CvPlayer.cpp:23353)  <- call CvPlayer::setLoyalMember
- CvPlayer::setEndorsedResolution  (CvPlayer.cpp:23379)  <- call CvPlayer::setLoyalMember
- CvPlayer::verifyCivics  (CvPlayer.cpp:4138)  <- call CvPlayer::setCivics
- CyPlayer::setCivics  (CyPlayer.cpp:2068)  <- call CvPlayer::setCivics
- CyPlayer::setLastStateReligion  (CyPlayer.cpp:1727)  <- call CvPlayer::setLastStateReligion
- CyPlayer::setLoyalMember  (CyPlayer.cpp:1872)  <- call CvPlayer::setLoyalMember
- CyUnit::changeExperience  (CyUnit.cpp:1285)  <- call CvUnit::changeExperience
- CyUnit::giveExperience  (CyUnit.cpp:469)  <- call CvUnit::giveExperience

### level 10 (16)

- CvCity::changeCulture  (CvCity.cpp:10778)  <- call CvCity::setCultureTimes100
- CvCity::changeCultureTimes100  (CvCity.cpp:10783)  <- call CvCity::setCultureTimes100
- CvCity::changeOccupationTimer  (CvCity.cpp:8544)  <- call CvCity::setOccupationTimer
- CvCity::setCulture  (CvCity.cpp:10753)  <- call CvCity::setCultureTimes100
- CvDllPythonEvents::reportCityBuilt  (CvDllPythonEvents.cpp:468)  <- event Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.OnCityBuilt
- CvEventReporter::gameStart  (CvEventReporter.cpp:84)  <- call CvDllPythonEvents::reportGameStart
- CvGame::setWinner  (CvGame.cpp:5727)  <- call CvEventReporter::victory
- CvGame::verifyCivics  (CvGame.cpp:8164)  <- call CvPlayer::verifyCivics
- CvNetConvert::Execute  (CvMessageData.cpp:556)  <- call CvPlayer::convert
- CvNetUpdateCivics::Execute  (CvMessageData.cpp:336)  <- call CvPlayer::revolution
- CvPlayerAI::AI_doCivics  (CvPlayerAI.cpp:17135)  <- call CvPlayer::revolution
- CvPlayerAI::AI_doReligion  (CvPlayerAI.cpp:17228)  <- call CvPlayer::convert
- CyCity::setCultureTimes100  (CyCity.cpp:2185)  <- call CvCity::setCultureTimes100
- CyCity::setOccupationTimer  (CyCity.cpp:1762)  <- call CvCity::setOccupationTimer
- CyPlayer::convert  (CyPlayer.cpp:775)  <- call CvPlayer::convert
- CyPlayer::revolution  (CyPlayer.cpp:749)  <- call CvPlayer::revolution

### level 11 (8)

- CvCity::doCulture  (CvCity.cpp:13536)  <- call CvCity::changeCultureTimes100
- CvEventReporter::cityBuilt  (CvEventReporter.cpp:204)  <- call CvDllPythonEvents::reportCityBuilt
- CvGame::changeForceCivicCount  (CvGame.cpp:6172)  <- call CvGame::verifyCivics
- CyCity::changeCulture  (CyCity.cpp:2191)  <- call CvCity::changeCulture
- CyCity::changeCultureTimes100  (CyCity.cpp:2197)  <- call CvCity::changeCultureTimes100
- CyCity::changeOccupationTimer  (CyCity.cpp:1768)  <- call CvCity::changeOccupationTimer
- CyCity::setCulture  (CyCity.cpp:2179)  <- call CvCity::setCulture
- CyGame::setWinner  (CyGame.cpp:713)  <- call CvGame::setWinner

### level 12 (1)

- CvDllPythonEvents::reportChangeWar  (CvDllPythonEvents.cpp:1234)  <- event Revolution/RevEvents.py onChangeWar

### level 13 (1)

- CvEventReporter::changeWar  (CvEventReporter.cpp:447)  <- call CvDllPythonEvents::reportChangeWar

## Python functions, level by level


### level 3 (10)

- Deal.turnsToCancel  (BUG/DealUtil.py:202)  <- py>cpp (name match) CyDeal::turnsToCancel
- GoldPerTurnTrade.onBeginActivePlayerTurn  (Contrib/Civ4lerts.py:780)  <- py>cpp (only target) CyPlayer::AI_maxGoldPerTurnTrade
- CvExoticForeignAdvisor.drawActive  (Screens/CvExoticForeignAdvisor.py:380)  <- py>cpp CyDeal::turnsToCancel
- CvExoticForeignAdvisor.drawResourceDeals  (Screens/CvExoticForeignAdvisor.py:1145)  <- py>cpp CyPlayer::AI_maxGoldPerTurnTrade
- CvForeignAdvisor.drawPossibleDeals  (Screens/CvForeignAdvisor.py:269)  <- py>cpp CyPlayer::AI_maxGoldPerTurnTrade
- CvWorldBuilderScreen.eraseAll  (base/Screens/CvWorldBuilderScreen.py:2448)  <- py>cpp (only target) CyPlot::setRouteType
- CvWorldBuilderScreen.placeObject  (base/Screens/CvWorldBuilderScreen.py:714)  <- py>cpp (only target) CyPlot::setPlotType
- CvWorldBuilderScreen.removeObject  (base/Screens/CvWorldBuilderScreen.py:931)  <- py>cpp (only target) CyPlot::setRouteType
- CvPlotDesc.apply  (base/pyWB/CvWBDesc.py:1118)  <- py>cpp CyPlot::setRouteType
- CvPlotDesc.preApply  (base/pyWB/CvWBDesc.py:1109)  <- py>cpp CyPlot::setPlotType

### level 4 (41)

- Deal.getCannotCancelReason  (BUG/DealUtil.py:197)  <- py>cpp (name match) CyDeal::getCannotCancelReason
- Deal.isCancelable  (BUG/DealUtil.py:190)  <- py>cpp (name match) CyDeal::isCancelable
- BonusBalancer.normalizeAddExtras  (CvMapGeneratorUtil.py:1384)  <- py>cpp CyPlot::setBonusType
- FeatureGenerator.addFeaturesAtPlot  (CvMapGeneratorUtil.py:1219)  <- py>cpp CyPlot::setFeatureType
- FeatureGenerator.addForestsAtPlot  (CvMapGeneratorUtil.py:1257)  <- py>cpp CyPlot::setFeatureType
- FeatureGenerator.addIceAtPlot  (CvMapGeneratorUtil.py:1238)  <- py>cpp CyPlot::setFeatureType
- FeatureGenerator.addJunglesAtPlot  (CvMapGeneratorUtil.py:1251)  <- py>cpp CyPlot::setFeatureType
- applyEarthquake1  (EntryPoints/CvRandomEventInterface.py:6860)  <- py>cpp (only target) CyPlot::setImprovementType
- applyMasterBlacksmithDone1  (EntryPoints/CvRandomEventInterface.py:2723)  <- py>cpp CyPlot::setBonusType
- applyVolcano1  (EntryPoints/CvRandomEventInterface.py:790)  <- py>cpp (only target) CyPlot::setImprovementType
- canTriggerHolyMountainRevealed  (EntryPoints/CvRandomEventInterface.py:218)  <- py>cpp CyPlot::setRevealed
- doAntelope2  (EntryPoints/CvRandomEventInterface.py:1206)  <- py>cpp CyPlot::setImprovementType
- doImpactCrater2  (EntryPoints/CvRandomEventInterface.py:1782)  <- py>cpp CyPlot::setImprovementType
- doSpicy2  (EntryPoints/CvRandomEventInterface.py:410)  <- py>cpp CyPlot::setImprovementType
- doWiningMonks2  (EntryPoints/CvRandomEventInterface.py:1295)  <- py>cpp CyPlot::setImprovementType
- clearMap  (ModTools/ModTools.py:12)  <- py>cpp CyPlot::setTerrainType
- showUnitClass  (ModTools/ModTools.py:90)  <- py>cpp CyPlot::setTerrainType
- showUnits  (ModTools/ModTools.py:25)  <- py>cpp CyPlot::setTerrainType
- showUnitsTerrain  (ModTools/ModTools.py:58)  <- py>cpp CyPlot::setTerrainType
- clearMap  (ModTools/ModToolsUtils.py:10)  <- py>cpp CyPlot::setTerrainType
- Revolution.processRevolution  (Revolution/Gameready/Revolution.py:5015)  <- py>cpp CyPlot::setRevealed
- Revolution.spawnRevolutionaries  (Revolution/Gameready/Revolution.py:6243)  <- py>cpp CyPlot::setRevealed
- clearOutCity  (Revolution/RevUtils.py:397)  <- py>cpp (name match) CyUnit::setXY
- moveEnemyUnits  (Revolution/RevUtils.py:309)  <- py>cpp (name match) CyUnit::setXY
- moveEnemyUnits2  (Revolution/RevUtils.py:357)  <- py>cpp (name match) CyUnit::setXY
- RoMEventManager.onCityLost  (RoMEventManager.py:508)  <- py>cpp (only target) CyPlot::setImprovementType
- RoMEventManager.onProjectBuilt  (RoMEventManager.py:390)  <- py>cpp CyPlot::setFeatureType
- CvForeignAdvisor.drawContents  (Screens/CvForeignAdvisor.py:165)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawPossibleDeals
- PLE.tempMove  (Screens/PLE.py:1283)  <- py>cpp (name match) CyUnit::setXY
- CvDebugTools.allBonuses  (base/CvDebugTools.py:259)  <- py>cpp CyPlot::setBonusType
- CvDebugTools.allImprovements  (base/CvDebugTools.py:267)  <- py>cpp CyPlot::setImprovementType
- CvWorldBuilderScreen.RevealCurrentPlot  (base/Screens/CvWorldBuilderScreen.py:2314)  <- py>cpp (name match) CyPlot::setRevealed
- CvWorldBuilderScreen.leftMouseDown  (base/Screens/CvWorldBuilderScreen.py:255)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.placeObject
- CvWorldBuilderScreen.mouseOverPlot  (base/Screens/CvWorldBuilderScreen.py:213)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.placeObject
- CvWorldBuilderScreen.placeMultipleObjects  (base/Screens/CvWorldBuilderScreen.py:1828)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.placeObject
- CvWorldBuilderScreen.removeMultipleObjects  (base/Screens/CvWorldBuilderScreen.py:1866)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.removeObject
- CvWorldBuilderScreen.revealAll  (base/Screens/CvWorldBuilderScreen.py:2304)  <- py>cpp CyPlot::setRevealed
- CvWorldBuilderScreen.rightMouseDown  (base/Screens/CvWorldBuilderScreen.py:285)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.removeObject
- CvWorldBuilderScreen.setAllPlots  (base/Screens/CvWorldBuilderScreen.py:414)  <- py>cpp CyMap::setAllPlotTypes
- CvWBDesc.applyInitialItems  (base/pyWB/CvWBDesc.py:1617)  <- py>cpp CyPlot::setRevealed
- CvWBDesc.applyMap  (base/pyWB/CvWBDesc.py:1559)  <- py>py (only target) base/pyWB/CvWBDesc.py CvPlotDesc.preApply

### level 5 (96)

- AbandonCityEventManager.__eventAbandonCityDestroyBuildingApply  (AbandonCityEventManager.py:221)  <- py>cpp CyCity::kill
- Deal.kill  (BUG/DealUtil.py:208)  <- py>cpp (name match) CyUnit::kill
- FeatureGenerator.addFeatures  (CvMapGeneratorUtil.py:1209)  <- py>py CvMapGeneratorUtil.py FeatureGenerator.addFeaturesAtPlot
- spawnUnit  (CvUtil.py:351)  <- py>cpp (name match) CyPlayer::initUnit
- applyBlackbeard1  (EntryPoints/CvRandomEventInterface.py:5138)  <- py>cpp CyPlayer::initUnit
- applyCityRuinsTreasure1  (EntryPoints/CvRandomEventInterface.py:7301)  <- py>cpp CyPlayer::initUnit
- applyClassicLiteratureDone2  (EntryPoints/CvRandomEventInterface.py:2571)  <- py>cpp CyTeam::setHasTech
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
- applySilverRain1  (EntryPoints/CvRandomEventInterface.py:7115)  <- py>cpp CyPlayer::initUnit
- applySilverRain3  (EntryPoints/CvRandomEventInterface.py:7162)  <- py>cpp CyUnit::kill
- applyStedeBonnet1  (EntryPoints/CvRandomEventInterface.py:5756)  <- py>cpp CyPlayer::initUnit
- applyTheBuccaneers1  (EntryPoints/CvRandomEventInterface.py:4996)  <- py>cpp CyPlayer::initUnit
- applyTheCorsairs1  (EntryPoints/CvRandomEventInterface.py:5909)  <- py>cpp CyPlayer::initUnit
- applyTheGoths1  (EntryPoints/CvRandomEventInterface.py:2099)  <- py>cpp CyPlayer::initUnit
- applyTheHuns1  (EntryPoints/CvRandomEventInterface.py:1877)  <- py>cpp CyPlayer::initUnit
- applyThePhilistines1  (EntryPoints/CvRandomEventInterface.py:2210)  <- py>cpp CyPlayer::initUnit
- applyTheTaliban1  (EntryPoints/CvRandomEventInterface.py:6255)  <- py>cpp CyPlayer::initUnit
- applyTheVandals1  (EntryPoints/CvRandomEventInterface.py:1988)  <- py>cpp CyPlayer::initUnit
- applyTheVedicAryans1  (EntryPoints/CvRandomEventInterface.py:2321)  <- py>cpp CyPlayer::initUnit
- applyTsunami1  (EntryPoints/CvRandomEventInterface.py:698)  <- py>cpp CyCity::kill
- doAssassinDiscovered3  (EntryPoints/CvRandomEventInterface.py:6914)  <- py>cpp CyPlayer::initUnit
- doNuclearProtest1  (EntryPoints/CvRandomEventInterface.py:4035)  <- py>cpp (name match) CyUnit::kill
- doSpyDiscovered3  (EntryPoints/CvRandomEventInterface.py:4001)  <- py>cpp CyPlayer::initUnit
- WorldBuilderRevealAllCB  (EntryPoints/CvScreensInterface.py:578)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.revealAll
- WorldBuilderUnRevealAllCB  (EntryPoints/CvScreensInterface.py:581)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.revealAll
- leftMouseDown  (EntryPoints/CvScreensInterface.py:891)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.leftMouseDown
- mouseOverPlot  (EntryPoints/CvScreensInterface.py:911)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.mouseOverPlot
- rightMouseDown  (EntryPoints/CvScreensInterface.py:901)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.rightMouseDown
- applyInitialItems  (EntryPoints/CvWBInterface.py:269)  <- py>py base/pyWB/CvWBDesc.py CvWBDesc.applyInitialItems
- applyMapDesc  (EntryPoints/CvWBInterface.py:265)  <- py>py base/pyWB/CvWBDesc.py CvWBDesc.applyMap
- readAndApplyDesc  (EntryPoints/CvWBInterface.py:232)  <- py>py base/pyWB/CvWBDesc.py CvWBDesc.applyMap
- advanceEra  (ModTools/ModTools.py:110)  <- py>cpp CyTeam::setHasTech
- PyCity.initUnit  (PyHelpers.py:620)  <- py>cpp CyPlayer::initUnit
- PyPlayer.initCity  (PyHelpers.py:336)  <- py>cpp CyPlayer::initCity
- PyPlayer.initUnit  (PyHelpers.py:284)  <- py>cpp CyPlayer::initUnit
- PyPlayer.setHasTech  (PyHelpers.py:141)  <- py>cpp CyTeam::setHasTech
- AIAutoPlay.doNewHuman  (Revolution/Gameready/AIAutoPlay.py:202)  <- py>cpp CyPlayer::initUnit
- BarbarianCiv.createMinorCiv  (Revolution/Gameready/BarbarianCiv.py:972)  <- py>cpp CyPlayer::initUnit
- BarbarianCiv.giveTechs  (Revolution/Gameready/BarbarianCiv.py:402)  <- py>cpp CyTeam::setHasTech
- BarbarianCiv.onCityAcquired  (Revolution/Gameready/BarbarianCiv.py:2017)  <- py>cpp CyPlayer::initUnit
- BarbarianCiv.settleMinorCiv  (Revolution/Gameready/BarbarianCiv.py:1326)  <- py>cpp CyPlayer::initUnit
- BarbarianCiv.setupFormerBarbCity  (Revolution/Gameready/BarbarianCiv.py:827)  <- py>cpp (name match) CyUnit::kill
- Revolution.doRevReinforcement  (Revolution/Gameready/Revolution.py:659)  <- py>cpp (name match) CyPlayer::initUnit
- Revolution.joinHumanHandler  (Revolution/Gameready/Revolution.py:6018)  <- py>cpp (name match) CyUnit::kill
- Revolution.launchRevolution  (Revolution/Gameready/Revolution.py:6189)  <- py>py Revolution/Gameready/Revolution.py Revolution.spawnRevolutionaries
- Revolution.makeRevolutionDecision  (Revolution/Gameready/Revolution.py:4192)  <- py>py Revolution/Gameready/Revolution.py Revolution.processRevolution
- Revolution.revolutionNetworkPopupHandler  (Revolution/Gameready/Revolution.py:4906)  <- py>py Revolution/Gameready/Revolution.py Revolution.processRevolution
- onSetPlayerAlive  (Revolution/Gameready/StartAsMinors.py:97)  <- py>cpp CyPlayer::initUnit
- assimilateHandler  (Revolution/RevEvents.py:1150)  <- py>cpp CyPlayer::assimilatePlayer
- checkForAssimilation  (Revolution/RevEvents.py:891)  <- py>cpp (only target) CyPlayer::assimilatePlayer
- checkRebelBonuses  (Revolution/RevEvents.py:451)  <- py>cpp CyPlayer::initUnit
- removeFloatingRebellions  (Revolution/RevEvents.py:851)  <- py>cpp (name match) CyUnit::kill
- changeCiv  (Revolution/RevUtils.py:1107)  <- py>cpp CyPlayer::changeCiv
- giveTechs  (Revolution/RevUtils.py:822)  <- py>cpp CyTeam::setHasTech
- RoMEventManager.onBeginPlayerTurn  (RoMEventManager.py:281)  <- py>cpp CyPlayer::initUnit
- RoMEventManager.onBuildingBuilt  (RoMEventManager.py:324)  <- py>cpp (name match) CyUnit::kill
- CvForeignAdvisor.drawActive  (Screens/CvForeignAdvisor.py:215)  <- py>cpp CyGameTextMgr::getDealString
- CvForeignAdvisor.handleInput  (Screens/CvForeignAdvisor.py:804)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawContents
- CvForeignAdvisor.interfaceScreen  (Screens/CvForeignAdvisor.py:115)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawContents
- CvForeignAdvisor.update  (Screens/CvForeignAdvisor.py:825)  <- py>py Screens/CvForeignAdvisor.py CvForeignAdvisor.drawContents
- PLE.doPromotion  (Screens/PLE.py:1653)  <- py>cpp (only target) CyUnit::promote
- PLE.selectGroup  (Screens/PLE.py:1297)  <- py>py Screens/PLE.py PLE.tempMove
- CvCameraControls.setDebugMode  (base/CvCameraControls.py:318)  <- py>cpp CyGame::toggleDebugMode
- CvDebugTools.applyTechCheat  (base/CvDebugTools.py:206)  <- py>cpp (name match) CyTeam::setHasTech
- CvDebugTools.putOneOfEveryUnit  (base/CvDebugTools.py:275)  <- py>cpp CyPlayer::initUnit
- CvFillMap.fillPlot  (base/CvPerfTest.py:52)  <- py>cpp CyPlayer::initCity
- CvWorldBuilderScreen.handleAllPlotsCB  (base/Screens/CvWorldBuilderScreen.py:363)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setAllPlots
- CvWorldBuilderScreen.handleTechCB  (base/Screens/CvWorldBuilderScreen.py:544)  <- py>cpp CyTeam::setHasTech
- CvWorldBuilderScreen.handleWorldBuilderTechByEraPullDownCB  (base/Screens/CvWorldBuilderScreen.py:497)  <- py>cpp CyTeam::setHasTech
- CvWorldBuilderScreen.placeRiverE  (base/Screens/CvWorldBuilderScreen.py:1162)  <- py>cpp CyPlot::setNOfRiver
- CvWorldBuilderScreen.placeRiverN  (base/Screens/CvWorldBuilderScreen.py:1125)  <- py>cpp CyPlot::setWOfRiver
- CvWorldBuilderScreen.placeRiverNE  (base/Screens/CvWorldBuilderScreen.py:1136)  <- py>cpp CyPlot::setNOfRiver
- CvWorldBuilderScreen.placeRiverNW  (base/Screens/CvWorldBuilderScreen.py:1111)  <- py>cpp CyPlot::setNOfRiver
- CvWorldBuilderScreen.placeRiverS  (base/Screens/CvWorldBuilderScreen.py:1184)  <- py>cpp CyPlot::setWOfRiver
- CvWorldBuilderScreen.placeRiverSE  (base/Screens/CvWorldBuilderScreen.py:1195)  <- py>cpp CyPlot::setNOfRiver
- CvWorldBuilderScreen.placeRiverSW  (base/Screens/CvWorldBuilderScreen.py:1173)  <- py>cpp CyPlot::setNOfRiver
- CvWorldBuilderScreen.placeRiverW  (base/Screens/CvWorldBuilderScreen.py:1151)  <- py>cpp CyPlot::setNOfRiver
- CvWorldBuilderScreen.setCurrentNormalPlayerIndex  (base/Screens/CvWorldBuilderScreen.py:1622)  <- py>cpp CyTeam::setHasTech
- CvWorldBuilderScreen.setMultipleReveal  (base/Screens/CvWorldBuilderScreen.py:1909)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.RevealCurrentPlot
- CvCityDesc.apply  (base/pyWB/CvWBDesc.py:858)  <- py>cpp (name match) CyPlayer::initCity
- CvUnitDesc.apply  (base/pyWB/CvWBDesc.py:673)  <- py>cpp (name match) CyPlayer::initUnit

### level 6 (45)

- Scoreboard.addPlayer  (BUG/Scoreboard.py:207)  <- py>cpp (name match) CyGame::addPlayer
- finderRegenerate  (Contrib/MapFinder.py:248)  <- py>cpp CyGame::regenerateMap
- regenerateForReal  (Contrib/MapFinder.py:67)  <- py>cpp CyGame::regenerateMap
- PickReligionPopup.__eventPickReligionApply  (Contrib/RevDCMReligionControl.py:225)  <- py>cpp CyPlayer::foundReligion
- ReligionControl.doHolyCity  (Contrib/RevDCMReligionControl.py:28)  <- py>cpp CyPlayer::foundReligion
- Carnation2Callback  (EntryPoints/CvRandomEventInterface.py:4601)  <- py>cpp CyPlayer::forcePeace
- doCarnation2  (EntryPoints/CvRandomEventInterface.py:4570)  <- py>cpp CyPlayer::forcePeace
- doHeroicGesture2  (EntryPoints/CvRandomEventInterface.py:1616)  <- py>cpp CyPlayer::forcePeace
- heroicGesture2Callback  (EntryPoints/CvRandomEventInterface.py:1642)  <- py>cpp CyPlayer::forcePeace
- WorldBuilderHandleAllPlotsCB  (EntryPoints/CvScreensInterface.py:605)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleAllPlotsCB
- WorldBuilderHandleTechCB  (EntryPoints/CvScreensInterface.py:659)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleTechCB
- WorldBuilderOnAllPlotsBrushSelected  (EntryPoints/CvScreensInterface.py:741)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleAllPlotsCB
- WorldBuilderOnNormalPlayerBrushSelected  (EntryPoints/CvScreensInterface.py:696)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setCurrentNormalPlayerIndex
- changeCivHandler  (Revolution/Development/ChangePlayer.py:133)  <- py>py Revolution/RevUtils.py changeCiv
- AIAutoPlay.onModNetMessage  (Revolution/Gameready/AIAutoPlay.py:561)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.doNewHuman
- AIAutoPlay.pickHumanHandler  (Revolution/Gameready/AIAutoPlay.py:227)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.doNewHuman
- BarbarianCiv.checkBarbCities  (Revolution/Gameready/BarbarianCiv.py:878)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.createMinorCiv
- BarbarianCiv.checkMinorCivs  (Revolution/Gameready/BarbarianCiv.py:1224)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.settleMinorCiv
- forceBarbCityToMinor  (Revolution/Gameready/BarbarianCiv.py:2049)  <- py>py (only target) Revolution/Gameready/BarbarianCiv.py BarbarianCiv.createMinorCiv
- Revolution.checkForRevReinforcement  (Revolution/Gameready/Revolution.py:641)  <- py>py Revolution/Gameready/Revolution.py Revolution.doRevReinforcement
- Revolution.chooseRevolutionCiv  (Revolution/Gameready/Revolution.py:3787)  <- py>cpp CyGame::addPlayer
- Revolution.controlLostNetworkHandler  (Revolution/Gameready/Revolution.py:5932)  <- py>py Revolution/RevUtils.py changeCiv
- Revolution.onEndPlayerTurn  (Revolution/Gameready/Revolution.py:585)  <- py>py Revolution/Gameready/Revolution.py Revolution.launchRevolution
- Revolution.onModNetMessage  (Revolution/Gameready/Revolution.py:7005)  <- py>py Revolution/Gameready/Revolution.py Revolution.revolutionNetworkPopupHandler
- Revolution.pickRevolutionStyle  (Revolution/Gameready/Revolution.py:2400)  <- py>py Revolution/Gameready/Revolution.py Revolution.makeRevolutionDecision
- Revolution.prepareRevolution  (Revolution/Gameready/Revolution.py:6137)  <- py>cpp (only target) CyUnit::setDamage
- init  (Revolution/Gameready/StartAsMinors.py:39)  <- py>py Revolution/Gameready/StartAsMinors.py onSetPlayerAlive
- TechDiffusion.diffuseTech  (Revolution/Gameready/TechDiffusion.py:103)  <- py>cpp CyTeam::setResearchProgress
- onCityAcquired  (Revolution/RevEvents.py:433)  <- py>py Revolution/RevEvents.py checkRebelBonuses
- onEndGameTurn  (Revolution/RevEvents.py:119)  <- py>py Revolution/RevEvents.py removeFloatingRebellions
- changeHuman  (Revolution/RevUtils.py:1153)  <- py>cpp CyGame::changeHumanPlayer
- PLE.doUpgrade  (Screens/PLE.py:1706)  <- py>cpp (only target) CyUnit::doCommand
- PLE.getPlotListButtonName  (Screens/PLE.py:815)  <- py>py Screens/PLE.py PLE.selectGroup
- PLE.unitPromotion  (Screens/PLE.py:766)  <- py>py Screens/PLE.py PLE.doPromotion
- CvDebugTools.allUnits  (base/CvDebugTools.py:256)  <- py>py base/CvDebugTools.py CvDebugTools.putOneOfEveryUnit
- CvDebugTools.applyUnitPicker  (base/CvDebugTools.py:152)  <- py>py PyHelpers.py PyPlayer.initCity
- CvEventManager.__eventAwardTechsAndGoldApply  (base/CvEventManager.py:999)  <- py>py base/CvDebugTools.py CvDebugTools.applyTechCheat
- CvEventManager.__eventWBAllPlotsPopupApply  (base/CvEventManager.py:1033)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleAllPlotsCB
- CvEventManager.onCityRazed  (base/CvEventManager.py:825)  <- py>cpp CyPlayer::initTriggeredData
- CvEventManager.onKbdEvent  (base/CvEventManager.py:218)  <- py>cpp CyUnit::setDamage
- CvFillMap.emptyMap  (base/CvPerfTest.py:24)  <- py>cpp CyPlayer::killUnits
- CvFillMap.fillMap  (base/CvPerfTest.py:30)  <- py>py base/CvPerfTest.py CvFillMap.fillPlot
- doGoody  (base/EntryPoints/CvGameInterface.py:216)  <- py>cpp (name match) CyPlayer::doGoody
- CvWorldBuilderDiplomacyScreen.handleVassalPullDownCB  (base/Screens/CvWorldBuilderDiplomacyScreen.py:351)  <- py>cpp CyTeam::assignVassal
- CvWorldBuilderScreen.handleInput  (base/Screens/CvWorldBuilderScreen.py:192)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleWorldBuilderTechByEraPullDownCB

### level 7 (61)

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
- PickReligionPopup.launchPopup  (Contrib/RevDCMReligionControl.py:194)  <- py>cpp CyGame::setAIAutoPlay
- CvAddBuilding  (CvUtil.py:114)  <- py>cpp (only target) CyCity::setNumRealBuilding
- EnhancedTechConquest.onCityAcquired  (EnhancedTechConquestUtils/EnhancedTechConquest.py:79)  <- py>cpp CyTeam::changeResearchProgress
- applyBlessedSea2  (EntryPoints/CvRandomEventInterface.py:82)  <- py>cpp (only target) CyCity::setNumRealBuilding
- applyCrusadeDone2  (EntryPoints/CvRandomEventInterface.py:2995)  <- py>cpp CyCity::setNumRealBuilding
- applyEarthDay2  (EntryPoints/CvRandomEventInterface.py:1507)  <- py>cpp CyPlayer::canTradeItem
- applyHurricane1  (EntryPoints/CvRandomEventInterface.py:618)  <- py>cpp CyCity::setNumRealBuilding
- applyLooters3  (EntryPoints/CvRandomEventInterface.py:507)  <- py>cpp CyCity::setNumRealBuilding
- applyTsunami2  (EntryPoints/CvRandomEventInterface.py:707)  <- py>cpp CyCity::setNumRealBuilding
- canApplyEarthDay2  (EntryPoints/CvRandomEventInterface.py:1485)  <- py>cpp CyPlayer::canTradeItem
- doWeddingFeud3  (EntryPoints/CvRandomEventInterface.py:325)  <- py>cpp CyTeam::declareWar
- weddingFeud3Callback  (EntryPoints/CvRandomEventInterface.py:357)  <- py>cpp CyTeam::declareWar
- handleWorldBuilderDiplomacyVassalPullDownCB  (EntryPoints/CvScreensInterface.py:861)  <- py>py base/Screens/CvWorldBuilderDiplomacyScreen.py CvWorldBuilderDiplomacyScreen.handleVassalPullDownCB
- PyCity.setNumRealBuildingIdx  (PyHelpers.py:694)  <- py>cpp CyCity::setNumRealBuilding
- changeHumanHandler  (Revolution/Development/ChangePlayer.py:220)  <- py>py Revolution/RevUtils.py changeHuman
- updateGraphics  (Revolution/Development/ChangePlayer.py:170)  <- py>cpp CyGame::setAIAutoPlay
- Tester.onBeginPlayerTurn  (Revolution/Development/Tester.py:214)  <- py>cpp CyTeam::declareWar
- Tester.waitingForHandler  (Revolution/Development/Tester.py:300)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.abdicate  (Revolution/Gameready/AIAutoPlay.py:581)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.disableMultiCheck  (Revolution/Gameready/AIAutoPlay.py:529)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.doCheckMultiplayerUpdate  (Revolution/Gameready/AIAutoPlay.py:387)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.onGameLoad  (Revolution/Gameready/AIAutoPlay.py:158)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.onKbdEvent  (Revolution/Gameready/AIAutoPlay.py:342)  <- py>cpp CyGame::setAIAutoPlay
- AIAutoPlay.onVictory  (Revolution/Gameready/AIAutoPlay.py:177)  <- py>cpp CyGame::setAIAutoPlay
- BarbarianCiv.barbSettleHandler  (Revolution/Gameready/BarbarianCiv.py:129)  <- py>py Revolution/RevUtils.py changeHuman
- BarbarianCiv.getScenario  (Revolution/Gameready/BarbarianCiv.py:209)  <- py>cpp CyGame::setAIAutoPlay
- BarbarianCiv.onBeginGameTurn  (Revolution/Gameready/BarbarianCiv.py:144)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.checkBarbCities
- BarbarianCiv.onEndPlayerTurn  (Revolution/Gameready/BarbarianCiv.py:159)  <- py>py Revolution/Gameready/BarbarianCiv.py BarbarianCiv.checkMinorCivs
- Revolution.checkForRevolution  (Revolution/Gameready/Revolution.py:2137)  <- py>py Revolution/Gameready/Revolution.py Revolution.pickRevolutionStyle
- Revolution.onBeginPlayerTurn  (Revolution/Gameready/Revolution.py:555)  <- py>py Revolution/Gameready/Revolution.py Revolution.checkForRevReinforcement
- onTechAcquired  (Revolution/Gameready/StartAsMinors.py:127)  <- py>cpp CyMap::verifyUnitValidPlot
- TechDiffusion.onBeginGameTurn  (Revolution/Gameready/TechDiffusion.py:77)  <- py>py Revolution/Gameready/TechDiffusion.py TechDiffusion.diffuseTech
- onSetPlayerAlive  (Revolution/RevEvents.py:196)  <- py>cpp CyGame::setAIAutoPlay
- updateRevolutionIndices  (Revolution/RevEvents.py:601)  <- py>cpp CyCity::setNumRealBuilding
- doRefortify  (Revolution/RevUtils.py:82)  <- py>cpp CySelectionGroup::setActivityType
- RevolutionInit.onGameLoad  (Revolution/RevolutionInit.py:98)  <- py>py Revolution/Gameready/StartAsMinors.py init
- RoMEventManager.addCityBuildings  (RoMEventManager.py:238)  <- py>cpp CyCity::setNumRealBuilding
- CvExoticForeignAdvisor.drawTechDeals  (Screens/CvExoticForeignAdvisor.py:1336)  <- py>cpp CyPlayer::canTradeItem
- CvMainInterface.updateScoreStrings  (Screens/CvMainInterface.py:5148)  <- py>py BUG/Scoreboard.py Scoreboard.addPlayer
- PLE.unitUpgrade  (Screens/PLE.py:837)  <- py>py Screens/PLE.py PLE.doUpgrade
- CvEventManager.__eventPlaceObjectApply  (base/CvEventManager.py:990)  <- py>py base/CvDebugTools.py CvDebugTools.applyUnitPicker
- emptyMap  (base/CvPerfTest.py:11)  <- py>py base/CvPerfTest.py CvFillMap.emptyMap
- fillMap  (base/CvPerfTest.py:7)  <- py>py base/CvPerfTest.py CvFillMap.fillMap
- CvWorldBuilderDiplomacyScreen.handleAtWarPullDownCB  (base/Screens/CvWorldBuilderDiplomacyScreen.py:368)  <- py>cpp CyTeam::declareWar
- CvWorldBuilderScreen.handleEditCityBuildingCB  (base/Screens/CvWorldBuilderScreen.py:552)  <- py>cpp (only target) CyCity::setNumRealBuilding
- CvWorldBuilderScreen.setEditButtonClicked  (base/Screens/CvWorldBuilderScreen.py:1650)  <- py>cpp (only target) CyCity::setNumRealBuilding
- CvWorldBuilderScreen.setEditCorporationSelected  (base/Screens/CvWorldBuilderScreen.py:1684)  <- py>cpp (only target) CyCity::setHasCorporation

### level 8 (36)

- doUpdate  (Contrib/FavoriteCivicDetector.py:63)  <- py>py BUG/PlayerUtil.py isGivingFavoriteCivicDenial
- ReInitInterceptorMision.doReInit  (Contrib/MonkeyTools.py:41)  <- py>cpp (only target) CySelectionGroup::pushMission
- MoreCiv4lertsEvent.CheckForAlerts  (Contrib/MoreCiv4lerts.py:183)  <- py>py Contrib/MoreCiv4lerts.py MoreCiv4lertsEvent.getTechTrades
- MoreCiv4lertsEvent.getBonusTrades  (Contrib/MoreCiv4lerts.py:443)  <- py>py BUG/TradeUtil.py getTradeableBonuses
- PickReligionPopup.__eventPickReligionBegin  (Contrib/RevDCMReligionControl.py:189)  <- py>py Contrib/RevDCMReligionControl.py PickReligionPopup.launchPopup
- AdjustBuilding  (CvUtil.py:379)  <- py>py PyHelpers.py PyCity.setNumRealBuildingIdx
- CvEnhancedTechConquestEventManager.onCityAcquired  (EnhancedTechConquestUtils/CvEnhancedTechConquestEventManager.py:23)  <- py>py EnhancedTechConquestUtils/EnhancedTechConquest.py EnhancedTechConquest.onCityAcquired
- applyChampion  (EntryPoints/CvRandomEventInterface.py:1014)  <- py>cpp CyUnit::setHasPromotion
- applyRubicon2  (EntryPoints/CvRandomEventInterface.py:4359)  <- py>cpp CyUnit::setHasPromotion
- doGreatMediator2  (EntryPoints/CvRandomEventInterface.py:1686)  <- py>cpp CyTeam::makePeace
- greatMediator2Callback  (EntryPoints/CvRandomEventInterface.py:1712)  <- py>cpp CyTeam::makePeace
- WorldBuilderHandleEditCityBuildingCB  (EntryPoints/CvScreensInterface.py:665)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleEditCityBuildingCB
- WorldBuilderOnWBEditBrushSelected  (EntryPoints/CvScreensInterface.py:711)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setEditButtonClicked
- WorldBuilderOnWBEditCorporationSelected  (EntryPoints/CvScreensInterface.py:729)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setEditCorporationSelected
- handleWorldBuilderDiplomacyAtWarPullDownCB  (EntryPoints/CvScreensInterface.py:864)  <- py>py base/Screens/CvWorldBuilderDiplomacyScreen.py CvWorldBuilderDiplomacyScreen.handleAtWarPullDownCB
- ChangePlayer.onKbdEvent  (Revolution/Development/ChangePlayer.py:60)  <- py>py Revolution/Development/ChangePlayer.py updateGraphics
- updateGraphicsHandler  (Revolution/Development/ChangePlayer.py:165)  <- py>py Revolution/Development/ChangePlayer.py updateGraphics
- AIAutoPlay.abdicateMultiCheck  (Revolution/Gameready/AIAutoPlay.py:537)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.abdicate
- AIAutoPlay.abdicateMultiCheckNoMessage  (Revolution/Gameready/AIAutoPlay.py:550)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.abdicate
- AIAutoPlay.onBeginGameTurn  (Revolution/Gameready/AIAutoPlay.py:408)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.doCheckMultiplayerUpdate
- AIAutoPlay.onEndPlayerTurn  (Revolution/Gameready/AIAutoPlay.py:281)  <- py>py Revolution/RevUtils.py doRefortify
- AIAutoPlay.onGameStart  (Revolution/Gameready/AIAutoPlay.py:155)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.onGameLoad
- Revolution.updatePlayerRevolution  (Revolution/Gameready/Revolution.py:1048)  <- py>py Revolution/Gameready/Revolution.py Revolution.checkForRevolution
- giveCityCulture  (Revolution/RevUtils.py:903)  <- py>cpp (name match) CyPlot::setCulture
- giveRebelUnitFreePromotion  (Revolution/RevUtils.py:651)  <- py>cpp (only target) CyUnit::setHasPromotion
- RevolutionInit.__init__  (Revolution/RevolutionInit.py:47)  <- py>py Revolution/RevolutionInit.py RevolutionInit.onGameLoad
- RevolutionInit.onGameStart  (Revolution/RevolutionInit.py:92)  <- py>py Revolution/RevolutionInit.py RevolutionInit.onGameLoad
- RoMEventManager.onModNetMessage  (RoMEventManager.py:151)  <- py>py RoMEventManager.py RoMEventManager.addCityBuildings
- CvMilitaryAdvisor.showSituationReport  (Screens/CvBUGMilitaryAdvisor.py:257)  <- py>py BUG/PlayerUtil.py getPossibleEmbargos
- CvMainInterface._setScrollingScoreboard  (Screens/CvMainInterface.py:6438)  <- py>py Screens/CvMainInterface.py CvMainInterface.updateScoreStrings
- CvMainInterface.changeScoreboardDisplay  (Screens/CvMainInterface.py:6250)  <- py>py Screens/CvMainInterface.py CvMainInterface.updateScoreStrings
- CvMainInterface.redraw  (Screens/CvMainInterface.py:1405)  <- py>py Screens/CvMainInterface.py CvMainInterface.updateScoreStrings
- CvWorldBuilderDiplomacyScreen.handleAIWeightResetAll  (base/Screens/CvWorldBuilderDiplomacyScreen.py:380)  <- py>cpp CyTeam::makePeace
- CvWorldBuilderScreen.handleCityEditCultureCB  (base/Screens/CvWorldBuilderScreen.py:446)  <- py>cpp (name match) CyPlot::setCulture
- CvWorldBuilderScreen.handlePromotionCB  (base/Screens/CvWorldBuilderScreen.py:518)  <- py>cpp (only target) CyUnit::setHasPromotion
- CvWorldBuilderScreen.setEditHeadquartersSelected  (base/Screens/CvWorldBuilderScreen.py:1694)  <- py>cpp CyGame::setHeadquarters

### level 9 (26)

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
- WorldBuilderHandleCityEditCultureCB  (EntryPoints/CvScreensInterface.py:620)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleCityEditCultureCB
- WorldBuilderHandlePromotionCB  (EntryPoints/CvScreensInterface.py:653)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handlePromotionCB
- WorldBuilderOnWBEditHeadquartersSelected  (EntryPoints/CvScreensInterface.py:735)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.setEditHeadquartersSelected
- forceScreenRedraw  (EntryPoints/CvScreensInterface.py:972)  <- py>py Screens/CvMainInterface.py CvMainInterface.redraw
- handleWorldBuilderDiplomacyAIWeightResetAllCB  (EntryPoints/CvScreensInterface.py:870)  <- py>py base/Screens/CvWorldBuilderDiplomacyScreen.py CvWorldBuilderDiplomacyScreen.handleAIWeightResetAll
- AIAutoPlay.AIChooserHandler  (Revolution/Gameready/AIAutoPlay.py:478)  <- py>py Revolution/Gameready/AIAutoPlay.py AIAutoPlay.abdicateMultiCheck
- CvMilitaryAdvisor.handleInput  (Screens/CvBUGMilitaryAdvisor.py:1178)  <- py>py Screens/CvBUGMilitaryAdvisor.py CvMilitaryAdvisor.showSituationReport
- CvMilitaryAdvisor.interfaceScreen  (Screens/CvBUGMilitaryAdvisor.py:179)  <- py>py Screens/CvBUGMilitaryAdvisor.py CvMilitaryAdvisor.showSituationReport
- CvExoticForeignAdvisor.drawInfoImproved  (Screens/CvExoticForeignAdvisor.py:525)  <- py>py Contrib/FavoriteCivicDetector.py doUpdate
- CvMainInterface.handleInput  (Screens/CvMainInterface.py:6262)  <- py>py Screens/CvMainInterface.py CvMainInterface.changeScoreboardDisplay
- CvMainInterface.setScrollingScoreboard  (Screens/CvMainInterface.py:6432)  <- py>py Screens/CvMainInterface.py CvMainInterface._setScrollingScoreboard
- CvPediaBonus.placeSpecial  (base/Screens/CvPediaBonus.py:190)  <- py>cpp CyGameTextMgr::getBonusHelp
- CvPediaTech.placeSpecial  (base/Screens/CvPediaTech.py:240)  <- py>cpp CyGameTextMgr::getTechHelp
- CvTechSplashScreen.interfaceScreen  (base/Screens/CvTechSplashScreen.py:92)  <- py>cpp CyGameTextMgr::getTechHelp
- CvWorldBuilderScreen.handleUnitAITypeEditPullDownCB  (base/Screens/CvWorldBuilderScreen.py:472)  <- py>cpp (only target) CyUnit::setUnitAIType
- CvWBPopups.applyEditCity  (base/pyWB/CvWBPopups.py:104)  <- py>py CvUtil.py AdjustBuilding

### level 10 (9)

- SevoPediaBonus.interfaceScreen  (Contrib/Sevopedia/SevoPediaBonus.py:85)  <- py>py Contrib/Sevopedia/SevoPediaBonus.py SevoPediaBonus.placeSpecial
- SevoPediaTech.interfaceScreen  (Contrib/Sevopedia/SevoPediaTech.py:82)  <- py>py Contrib/Sevopedia/SevoPediaTech.py SevoPediaTech.placeSpecial
- applyGeneralsPutsch3  (EntryPoints/CvRandomEventInterface.py:4470)  <- py>cpp CyPlayer::setCivics
- applyRubicon3  (EntryPoints/CvRandomEventInterface.py:4378)  <- py>cpp CyPlayer::setCivics
- WorldBuilderHandleUnitAITypeEditPullDownCB  (EntryPoints/CvScreensInterface.py:641)  <- py>py base/Screens/CvWorldBuilderScreen.py CvWorldBuilderScreen.handleUnitAITypeEditPullDownCB
- CvExoticForeignAdvisor.drawInfo  (Screens/CvExoticForeignAdvisor.py:456)  <- py>py Screens/CvExoticForeignAdvisor.py CvExoticForeignAdvisor.drawInfoImproved
- CvEventManager.__eventEditCityApply  (base/CvEventManager.py:981)  <- py>py base/pyWB/CvWBPopups.py CvWBPopups.applyEditCity
- CvPediaBonus.interfaceScreen  (base/Screens/CvPediaBonus.py:79)  <- py>py base/Screens/CvPediaBonus.py CvPediaBonus.placeSpecial
- CvPediaTech.interfaceScreen  (base/Screens/CvPediaTech.py:67)  <- py>py base/Screens/CvPediaTech.py CvPediaTech.placeSpecial

### level 11 (3)

- doSmallRevolts  (Revolution/RevEvents.py:1173)  <- py>cpp (only target) CyCity::setOccupationTimer
- onChangeWar  (Revolution/RevEvents.py:302)  <- py>cpp (only target) CyCity::setOccupationTimer
- CvPediaMain.pediaJump  (Screens/CvPediaMain.py:900)  <- py>py base/Screens/CvPediaBonus.py CvPediaBonus.interfaceScreen

### level 12 (8)

- onBeginPlayerTurn  (Contrib/RevDCMReligionControl.py:87)  <- py>cpp CyGame::setWinner
- PyCity.changeCulture  (PyHelpers.py:595)  <- py>cpp CyCity::changeCulture
- PyCity.setCulture  (PyHelpers.py:598)  <- py>cpp CyCity::setCulture
- onEndPlayerTurn  (Revolution/RevEvents.py:166)  <- py>py Revolution/RevEvents.py doSmallRevolts
- CvPediaMain.back  (Screens/CvPediaMain.py:948)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump
- CvPediaMain.forward  (Screens/CvPediaMain.py:955)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump
- CvPediaMain.link  (Screens/CvPediaMain.py:974)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump
- CvPediaMain.pediaShow  (Screens/CvPediaMain.py:961)  <- py>py Screens/CvPediaMain.py CvPediaMain.pediaJump

## Reach per start node

| start | reached | C++ | Python | members |
|---|---|---|---|---|
| CvPlot::updatePlotBuilder | 1178 | 901 | 277 | 0 |
| PEACE_TREATY_LENGTH | 1139 | 829 | 310 | 0 |
| CvPlot::updateFeatureSymbolEntity | 1066 | 807 | 259 | 0 |
| GRAPHICS_PAGING_ACTIVE_UNITS | 1059 | 800 | 259 | 0 |
| CvUnit::canPageGraphicsOut | 1058 | 799 | 259 | 0 |
| CvPlot::updateRouteSymbol | 1043 | 781 | 262 | 0 |
| GRAPHICS_PAGING_ACTIVE_CITIES | 1010 | 758 | 252 | 0 |
| GRAPHICS_PAGING_LOG | 1009 | 757 | 252 | 0 |
| CvCity::canPageGraphicsOut | 1009 | 757 | 252 | 0 |
| CvGame::m_iGraphicsMemoryPressure | 1008 | 756 | 252 | 0 |
| GRAPHICS_PAGING_REVEAL_MAX | 1007 | 755 | 252 | 0 |
| CvPlot::refreshRevealedGraphics | 1007 | 755 | 252 | 0 |
| CvGame::endBulkReveal | 1004 | 752 | 252 | 0 |
| CvPlayerAI::AI_goldPerTurnCostVal | 120 | 67 | 53 | 0 |
| CvPlayerAI::AI_tradeGiveVal | 119 | 66 | 53 | 0 |
| CvPlayerAI::AI_considerOffer | 115 | 62 | 53 | 0 |
| CvPlayerAI::AI_doDiplo | 113 | 60 | 53 | 0 |
| CvGame::reset | 11 | 11 | 0 | 0 |
| GRAPHICS_PAGING_MEMORY_RECOVER_SAMPLES | 4 | 4 | 0 | 0 |
| GRAPHICS_PAGING_MEMORY_RECOVER_MB | 4 | 4 | 0 | 0 |
| GRAPHICS_PAGING_MEMORY_CRITICAL_MB | 4 | 4 | 0 | 0 |
| GRAPHICS_PAGING_MEMORY_CONTROL | 4 | 4 | 0 | 0 |
| GRAPHICS_PAGING_MEMORY_CONSERVE_MB | 4 | 4 | 0 | 0 |
| CvGame::m_iGraphicsMemoryRecoverySamples | 4 | 4 | 0 | 0 |
| CvGame::m_iGraphicsMemoryAvailMB | 4 | 4 | 0 | 0 |
| CvGame::m_dwGraphicsMemorySampleTime | 4 | 4 | 0 | 0 |
| GRAPHICS_PAGING_MEMORY_CONSERVE_MAX_IN | 3 | 3 | 0 | 0 |
| GRAPHICS_PAGING_MAX_OUT | 3 | 3 | 0 | 0 |
| GRAPHICS_PAGING_MAX_IN | 3 | 3 | 0 | 0 |
| GRAPHICS_PAGING_CRITICAL_SELECTED_IN | 3 | 3 | 0 | 0 |
| CvGame::updateGraphicsMemoryPressure | 3 | 3 | 0 | 0 |
| GRAPHICS_PAGING_SYMBOLS | 2 | 2 | 0 | 0 |
| GRAPHICS_PAGING_PRESSURE_RANGE_X | 2 | 2 | 0 | 0 |
| GRAPHICS_PAGING_PRESSURE_RANGE_SOUTH | 2 | 2 | 0 | 0 |
| GRAPHICS_PAGING_PRESSURE_RANGE_NORTH | 2 | 2 | 0 | 0 |
| GRAPHICS_PAGING_MARGIN | 2 | 2 | 0 | 0 |
| CvPlayerAI::AI_dealNetVal | 2 | 2 | 0 | 0 |
| CvGame::pageGraphics | 2 | 2 | 0 | 0 |
| CvGame::m_bPagingPending | 2 | 2 | 0 | 0 |
| CvPlayerAI::AI_isMutuallyBeneficialDeal | 1 | 1 | 0 | 0 |
| CvGame::updateGraphicsPaging | 1 | 1 | 0 | 0 |
| CvPlayerAI::AI_counterPropose | 0 | 0 | 0 | 0 |
