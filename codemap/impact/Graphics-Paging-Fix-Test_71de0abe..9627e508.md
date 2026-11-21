# Impact of 71de0abe5dc8..9627e508fedc

Commits:

- 9627e50 2026-11-21 Map trade fix, GPT fix also
- 9b85482 2026-11-20 Update 3 files

```
 Assets/CvGameCoreDLL/CvCity.cpp     |  26 +++-
 Assets/CvGameCoreDLL/CvDeal.cpp     |   6 +-
 Assets/CvGameCoreDLL/CvGame.cpp     | 232 ++++++++++++++++++++++++++++++++----
 Assets/CvGameCoreDLL/CvGame.h       |  11 +-
 Assets/CvGameCoreDLL/CvPlayerAI.cpp |  55 ++++-----
 Assets/CvGameCoreDLL/CvPlot.cpp     |  69 +++++++++--
 Assets/CvGameCoreDLL/CvPlot.h       |   7 ++
 Assets/XML/GlobalDefinesAlt.xml     |   7 +-
 8 files changed, 345 insertions(+), 68 deletions(-)
```

## Functions

- changed: 13; added: 8; removed: 0
  - changed CvCity::setRevealed  (CvCity.cpp:10862-10905)
  - changed CvDeal::startTrade  (CvDeal.cpp:695-1094)
  - changed CvGame::reset  (CvGame.cpp:482-726)
  - changed CvGame::updateGraphicsPaging  (CvGame.cpp:2393-2539)
  - changed CvGame::pageGraphics  (CvGame.cpp:2677-2877)
  - changed CvPlayerAI::AI_counterPropose  (CvPlayerAI.cpp:9090-9641)
  - changed CvPlayerAI::AI_goldPerTurnTradeVal  (CvPlayerAI.cpp:9702-9708)
  - changed CvPlayerAI::AI_doDiplo  (CvPlayerAI.cpp:17242-19180)
  - changed CvPlot::reset  (CvPlot.cpp:179-266)
  - changed CvPlot::setupGraphical  (CvPlot.cpp:272-294)
  - changed CvPlot::setRevealed  (CvPlot.cpp:7695-7810)
  - changed CvPlot::setRevealedImprovementType  (CvPlot.cpp:7876-7904)
  - changed CvPlot::setRevealedRouteType  (CvPlot.cpp:7928-7959)
  - added CvGame::beginBulkReveal  (CvGame.cpp:2295-2306)
  - added CvGame::endBulkReveal  (CvGame.cpp:2308-2323)
  - added CvGame::deferRevealedGraphics  (CvGame.cpp:2325-2340)
  - added CvGame::processDeferredReveals  (CvGame.cpp:2342-2391)
  - added CvPlot::deferRevealedGraphics  (CvPlot.cpp:296-299)
  - added CvPlot::refreshRevealedGraphics  (CvPlot.cpp:304-332)
  - added CvPlot::isRevealedGraphicsDirty  (CvPlot.h:67-67)
  - added CvPlot::setRevealedGraphicsDirty  (CvPlot.h:68-68)

## Member declarations

- added CvGame::m_aiDeferredRevealPlots std::vector<int>
- added CvGame::m_bPagingPendingOut bool
- added CvGame::m_eBulkRevealTeam TeamTypes
- added CvGame::m_iBulkRevealDepth int
- added CvPlot::m_bRevealedGraphicsDirty bool
- added CvPlot::m_bRevealedRouteDirty bool

## Members written on changed lines

CvGame::m_aiDeferredRevealPlots, CvGame::m_bPagingPending, CvGame::m_bPagingPendingOut, CvGame::m_eBulkRevealTeam, CvGame::m_iBulkRevealDepth, CvPlot::m_bRevealedGraphicsDirty, CvPlot::m_bRevealedRouteDirty

## Global defines read on changed lines

- GRAPHICS_PAGING_LOG in CvGame::pageGraphics (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_LOG in CvGame::processDeferredReveals (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_MAX_IN in CvGame::processDeferredReveals (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_MAX_OUT in CvGame::pageGraphics (defined in GlobalDefinesAlt.xml)
- PEACE_TREATY_LENGTH in CvPlayerAI::AI_counterPropose (defined in GlobalDefines.xml)
- PEACE_TREATY_LENGTH in CvPlayerAI::AI_goldPerTurnTradeVal (defined in GlobalDefines.xml)

## XML files changed

- Assets/XML/GlobalDefinesAlt.xml     |   7 +-

_Member uses and functions are read from the source at each commit; callers come from the compiler map at its own commit (see skeleton.md), so callers added since then are found only by name._

## Member variables

- **CvGame::m_aiDeferredRevealPlots**: written in 3 function(s), read in 3
  - written (or passed by address / method called): CvGame::deferRevealedGraphics, CvGame::processDeferredReveals, CvGame::reset
  - read: CvGame::deferRevealedGraphics, CvGame::processDeferredReveals, CvGame::reset
- **CvGame::m_bPagingPending**: written in 3 function(s), read in 1
  - written (or passed by address / method called): CvGame::pageGraphics, CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_bPagingPendingOut**: written in 3 function(s), read in 1
  - written (or passed by address / method called): CvGame::pageGraphics, CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_eBulkRevealTeam**: written in 3 function(s), read in 2
  - written (or passed by address / method called): CvGame::beginBulkReveal, CvGame::endBulkReveal, CvGame::reset
  - read: CvGame::beginBulkReveal, CvGame::deferRevealedGraphics
- **CvGame::m_iBulkRevealDepth**: written in 3 function(s), read in 4
  - written (or passed by address / method called): CvGame::beginBulkReveal, CvGame::endBulkReveal, CvGame::reset
  - read: CvGame::beginBulkReveal, CvGame::deferRevealedGraphics, CvGame::endBulkReveal, CvGame::processDeferredReveals
- **CvPlot::m_bRevealedGraphicsDirty**: written in 4 function(s), read in 2
  - written (or passed by address / method called): CvPlot::refreshRevealedGraphics, CvPlot::reset, CvPlot::setRevealedGraphicsDirty, CvPlot::setupGraphical
  - read: CvPlot::isRevealedGraphicsDirty, CvPlot::refreshRevealedGraphics
- **CvPlot::m_bRevealedRouteDirty**: written in 4 function(s), read in 1
  - written (or passed by address / method called): CvPlot::refreshRevealedGraphics, CvPlot::reset, CvPlot::setRevealedRouteType, CvPlot::setupGraphical
  - read: CvPlot::refreshRevealedGraphics

The readers above are added to the reach (8 in the compiler map).

## Reach per changed function

| function | direct callers | all callers | exported reached | Python-bound reached |
|---|---|---|---|---|
| CvPlot::isRevealedGraphicsDirty | 2 | 736 | 68 | 131 |
| CvPlot::setRevealedGraphicsDirty | 1 | 733 | 68 | 131 |
| CvGame::deferRevealedGraphics | 1 | 732 | 68 | 131 |
| CvPlot::deferRevealedGraphics | 4 | 731 | 68 | 131 |
| CvPlot::setRevealedRouteType | 3 | 727 | 68 | 130 |
| CvCity::setRevealed | 4 | 725 | 67 | 130 |
| CvPlot::setRevealedImprovementType | 3 | 724 | 67 | 129 |
| CvPlot::setRevealed | 14 | 723 | 67 | 129 |
| CvPlayerAI::AI_goldPerTurnTradeVal | 2 | 722 | 66 | 127 |
| CvPlot::refreshRevealedGraphics | 1 | 720 | 66 | 127 |
| CvGame::processDeferredReveals | 2 | 719 | 66 | 127 |
| CvGame::endBulkReveal | 1 | 717 | 66 | 127 |
| CvGame::beginBulkReveal | 1 | 717 | 66 | 127 |
| CvDeal::startTrade | 1 | 716 | 66 | 127 |
| CvPlayerAI::AI_doDiplo | 1 | 38 | 14 | 6 |
| CvPlot::reset | 3 | 13 | 3 | 1 |
| CvGame::reset | 3 | 11 | 6 | 0 |
| CvPlot::setupGraphical | 1 | 6 | 4 | 1 |
| CvGame::pageGraphics | 1 | 2 | 1 | 0 |
| CvGame::updateGraphicsPaging | 1 | 1 | 1 | 0 |
| CvPlayerAI::AI_counterPropose | 0 | 0 | 0 | 0 |

Rows include the readers of changed members.

## Callers (compiler call graph)

739 function(s) reach the changed code through calls; per level: 1: 28, 2: 64, 3: 94, 4: 117, 5: 107, 6: 77, 7: 202, 8: 32, 9: 12, 10: 5, 11: 1

### level 1 (28)

- CvCity::init  (CvCity.cpp:157)
- CvDeal::addTrades  (CvDeal.cpp:119)
- CvGame::CvGame  (CvGame.cpp:50)
- CvGame::init  (CvGame.cpp:108)
- CvGame::read  (CvGame.cpp:8952)
- CvGame::update  (CvGame.cpp:2171)
- CvMap::setRevealedPlots  (CvMap.cpp:291)
- CvMap::setupGraphical  (CvMap.cpp:263)
- CvPlayer::acquireCity  (CvPlayer.cpp:2337)
- CvPlayer::assimilatePlayer  (CvPlayer.cpp:22593)
- CvPlayer::doAdvancedStartAction  (CvPlayer.cpp:16735)
- CvPlayer::initFreeUnits  (CvPlayer.cpp:1848)
- CvPlayer::receiveGoody  (CvPlayer.cpp:6344)
- CvPlayer::splitEmpire  (CvPlayer.cpp:22369)
- CvPlayerAI::AI_dealVal  (CvPlayerAI.cpp:8823)
- CvPlayerAI::AI_doAdvancedStart  (CvPlayerAI.cpp:23991)
- CvPlayerAI::AI_doTurnPost  (CvPlayerAI.cpp:543)
- CvPlot::CvPlot  (CvPlot.cpp:44)
- CvPlot::changeStolenVisibilityCount  (CvPlot.cpp:7281)
- CvPlot::changeVisibilityCount  (CvPlot.cpp:7184)
- CvPlot::init  (CvPlot.cpp:108)
- CvPlot::read  (CvPlot.cpp:9181)
- CvPlot::setImprovementType  (CvPlot.cpp:5813)
- CvPlot::setRouteType  (CvPlot.cpp:5934)
- CvTeam::addTeam  (CvTeam.cpp:520)
- CvTeam::resetPlotAndCityData  (CvTeam.cpp:433)
- CyCity::setRevealed  (CyCity.cpp:2236)
- CyPlot::setRevealed  (CyPlot.cpp:967)

### level 2 (64)

- CvCity::applyEvent  (CvCity.cpp:15236)
- CvCity::doTask  (CvCity.cpp:1504)
- CvCity::kill  (CvCity.cpp:1005)
- CvCity::liberate  (CvCity.cpp:15930)
- CvDeal::doTurn  (CvDeal.cpp:298)
- CvGame::doGlobalWarming  (CvGame.cpp:6749)
- CvGame::implementDeal  (CvGame.cpp:3270)
- CvGame::initFreeState  (CvGame.cpp:786)
- CvGame::initFreeUnits  (CvGame.cpp:846)
- CvGame::processVote  (CvGame.cpp:8448)
- CvGame::regenerateMap  (CvGame.cpp:348)
- CvGameAI::CvGameAI  (CvGameAI.cpp:13)
- CvGameAI::read  (CvGameAI.cpp:113)
- CvMap::init  (CvMap.cpp:65)
- CvMap::read  (CvMap.cpp:1300)
- CvMapGenerator::addGoodies  (CvMapGenerator.cpp:888)
- CvNetAdvancedStartAction::Execute  (CvMessageData.cpp:484)
- CvNetEmpireSplit::Execute  (CvMessageData.cpp:588)
- CvPlayer::applyEvent  (CvPlayer.cpp:20656)
- CvPlayer::doEspionageMission  (CvPlayer.cpp:16109)
- CvPlayer::doGoody  (CvPlayer.cpp:6546)
- CvPlayer::doTurn  (CvPlayer.cpp:3918)
- CvPlayer::initCity  (CvPlayer.cpp:2320)
- CvPlayer::initInGame  (CvPlayer.cpp:445)
- CvPlayer::setTurnActive  (CvPlayer.cpp:12160)
- CvPlayerAI::AI_advancedStartDoRoute  (CvPlayerAI.cpp:23752)
- CvPlayerAI::AI_advancedStartPlaceCity  (CvPlayerAI.cpp:23638)
- CvPlayerAI::AI_advancedStartPlaceExploreUnits  (CvPlayerAI.cpp:23529)
- CvPlayerAI::AI_advancedStartRevealRadius  (CvPlayerAI.cpp:23613)
- CvPlayerAI::AI_advancedStartRouteTerritory  (CvPlayerAI.cpp:23788)
- CvPlayerAI::AI_considerOffer  (CvPlayerAI.cpp:8937)
- CvPlayerAI::AI_doSplit  (CvPlayerAI.cpp:20180)
- CvPlayerAI::AI_stopTradingTradeVal  (CvPlayerAI.cpp:10641)
- CvPlot::applyEvent  (CvPlot.cpp:10189)
- CvPlot::changeAdjacentSight  (CvPlot.cpp:1849)
- CvPlot::changeBuildProgress  (CvPlot.cpp:7975)
- CvPlot::doImprovementUpgrade  (CvPlot.cpp:688)
- CvPlot::erase  (CvPlot.cpp:444)
- CvPlot::nukeExplosion  (CvPlot.cpp:1053)
- CvPlot::removeGoody  (CvPlot.cpp:3692)
- CvPlot::setFeatureType  (CvPlot.cpp:5592)
- CvPlot::setOwner  (CvPlot.cpp:4997)
- CvPlot::updateCityRoute  (CvPlot.cpp:5981)
- CvTeam::setHasTech  (CvTeam.cpp:5947)
- CvTeam::setStolenVisibilityTimer  (CvTeam.cpp:4270)
- CvUnit::airBomb  (CvUnit.cpp:4895)
- CvUnit::airBomb1  (CvUnit.cpp:14533)
- CvUnit::bombardRanged  (CvUnit.cpp:15531)
- CvUnit::pillage  (CvUnit.cpp:5400)
- CvUnit::sabotage  (CvUnit.cpp:5803)
- CvUnit::setXY  (CvUnit.cpp:10566)
- CyCityPythonInterface1  (CyCityInterface1.cpp:15)
- CyMap::setRevealedPlots  (CyMap.cpp:34)
- CyPlayer::acquireCity  (CyPlayer.cpp:153)
- CyPlayer::assimilatePlayer  (CyPlayer.cpp:2518)
- CyPlayer::receiveGoody  (CyPlayer.cpp:496)
- CyPlayer::splitEmpire  (CyPlayer.cpp:2483)
- CyPlot::changeVisibilityCount  (CyPlot.cpp:936)
- CyPlot::setImprovementType  (CyPlot.cpp:776)
- CyPlot::setRouteType  (CyPlot.cpp:787)
- ... 4 more

### files touched by the reach (functions per file)

CvUnitAI.cpp 165, CvUnit.cpp 80, CvPlayer.cpp 67, CvGame.cpp 58, CvCity.cpp 39, CvPlot.cpp 39, CvTeam.cpp 37, CyPlayer.cpp 34, CvPlayerAI.cpp 28, CvSelectionGroup.cpp 21, CyCity.cpp 19, CyTeam.cpp 18, CyUnit.cpp 18, CvMessageData.cpp 17, CyPlot.cpp 15, CvMap.cpp 13, CvCityAI.cpp 13, CvMapGenerator.cpp 10, CyMapGenerator.cpp 10, CvDeal.cpp 8, CyMap.cpp 7, CyGame.cpp 6, CvSelectionGroupAI.cpp 6, CvDLLButtonPopup.cpp 3, CvTeamAI.cpp 3, CySelectionGroup.cpp 3, CvPlot.h 2, CvGameAI.cpp 2, FFreeListTrashArray.h 2, CvGameInterface.cpp 2, CyCityInterface1.cpp 1, CyPlotInterface1.cpp 1, CvDLLPython.cpp 1, CvGlobals.cpp 1, CyMapInterface.cpp 1, CyPlayerInterface2.cpp 1, CyPlayerInterface1.cpp 1, CyTeamInterface.cpp 1, CyGameInterface.cpp 1, CyUnitInterface1.cpp 1

## Exits from the DLL among them

- called by the exe (exported): 74: CvCity::cheat  (CvCity.cpp:16201); CvDLLButtonPopup::OnOkClicked  (CvDLLButtonPopup.cpp:75); CvDLLButtonPopup::launchButtonPopup  (CvDLLButtonPopup.cpp:855); CvDeal::kill  (CvDeal.cpp:78); CvGame::CvGame  (CvGame.cpp:50); CvGame::cheatSpaceship  (CvGameInterface.cpp:2561); CvGame::implementDeal  (CvGame.cpp:3270); CvGame::init  (CvGame.cpp:108); CvGame::initDiplomacy  (CvGame.cpp:730); CvGame::initFreeState  (CvGame.cpp:786); CvGame::initFreeUnits  (CvGame.cpp:846); CvGame::nextActivePlayer  (CvGameInterface.cpp:2691); CvGame::normalizeStartingPlots  (CvGame.cpp:2048); CvGame::read  (CvGame.cpp:8952); CvGame::regenerateMap  (CvGame.cpp:348) ...
- bound for Python: 131: acquireCity, addFeatures, addGameElements, addGoodies, addLakes, addPlayer, addProductionExperience, addTeam, assignVassal, assimilatePlayer, attackForDamage, changeBuildProgress, changeCiv, changeCombatExperience, changeCulture, changeCultureTimes100, changeDamage, changeEspionagePointsAgainstTeam, changeExperience, changeExtraWaterSeeFromCount, changeOccupationTimer, changeProjectCount, changeResearchProgress, changeTechShareCount, changeVisibilityCount
- Python modules calling them: 36: AbandonCityEventManager.py, BUG/DealUtil.py, BUG/Scoreboard.py, Contrib/AStarTools.py, Contrib/MapFinder.py, Contrib/MonkeyTools.py, Contrib/RevDCMReligionControl.py, CvDiplomacy.py, CvMapGeneratorUtil.py, CvUtil.py, EnhancedTechConquestUtils/EnhancedTechConquest.py, EntryPoints/CvRandomEventInterface.py, ModTools/ModTools.py, ModTools/ModToolsUtils.py, PyHelpers.py, Revolution/Development/ChangePlayer.py, Revolution/Development/Tester.py, Revolution/Gameready/AIAutoPlay.py, Revolution/Gameready/BarbarianCiv.py, Revolution/Gameready/Revolution.py, Revolution/Gameready/StartAsMinors.py, Revolution/Gameready/TechDiffusion.py, Revolution/RevEvents.py, Revolution/RevUtils.py, RoMEventManager.py ...
