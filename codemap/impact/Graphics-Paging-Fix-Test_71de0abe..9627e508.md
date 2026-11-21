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

## Functions outside the compiler map

- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvGame::beginBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::setRevealed, CvPlot::deferRevealedGraphics; the name is also defined in CvPlot, so calls through an object may be theirs
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs
- CvGame::processDeferredReveals is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::endBulkReveal, CvGame::updateGraphicsPaging
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs
- CvPlot::refreshRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::processDeferredReveals
- CvGame::processDeferredReveals is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::endBulkReveal, CvGame::updateGraphicsPaging
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvPlot::isRevealedGraphicsDirty is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::deferRevealedGraphics, CvGame::processDeferredReveals
- CvGame::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::setRevealed, CvPlot::deferRevealedGraphics; the name is also defined in CvPlot, so calls through an object may be theirs
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs
- CvGame::processDeferredReveals is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::endBulkReveal, CvGame::updateGraphicsPaging
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvPlot::setRevealedGraphicsDirty is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::deferRevealedGraphics
- CvGame::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::setRevealed, CvPlot::deferRevealedGraphics; the name is also defined in CvPlot, so calls through an object may be theirs
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs

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

The readers above are added to the reach (1 in the compiler map).

## Reach per changed function

| function | direct callers | all callers | exported reached | Python-bound reached |
|---|---|---|---|---|
| CvPlot::setRevealedRouteType | 3 | 727 | 68 | 130 |
| CvCity::setRevealed | 4 | 725 | 67 | 130 |
| CvPlot::setRevealedImprovementType | 3 | 724 | 67 | 129 |
| CvPlot::setRevealed | 14 | 723 | 67 | 129 |
| CvPlayerAI::AI_goldPerTurnTradeVal | 3 | 722 | 66 | 127 |
| CvUnit::setupGraphical | 3 | 721 | 67 | 128 |
| CvCity::setupGraphical | 2 | 718 | 67 | 127 |
| CvUnit::isCombatVisible | 5 | 717 | 66 | 127 |
| CvUnit::setXY | 11 | 716 | 66 | 127 |
| CvDeal::startTrade | 1 | 716 | 66 | 127 |
| CvPlayerAI::AI_doDiplo | 1 | 38 | 14 | 6 |
| CvPlot::reset | 3 | 13 | 3 | 1 |
| CvGame::reset | 3 | 11 | 6 | 0 |
| CvPlot::setupGraphical | 1 | 6 | 4 | 1 |
| CvPlayerAI::AI_counterPropose | 0 | 0 | 0 | 0 |
| CvGame::update | 0 | 0 | 1 | 0 |

Rows include callers of functions newer than the map (name match) and readers of changed members, standing in for the new code they lead to.

## Callers (compiler call graph)

741 function(s) reach the changed code through calls; per level: 1: 45, 2: 122, 3: 142, 4: 116, 5: 220, 6: 36, 7: 30, 8: 23, 9: 7

### level 1 (45)

- CvCity::init  (CvCity.cpp:157)
- CvDeal::addTrades  (CvDeal.cpp:119)
- CvGame::CvGame  (CvGame.cpp:50)
- CvGame::init  (CvGame.cpp:108)
- CvGame::read  (CvGame.cpp:8286)
- CvMap::setRevealedPlots  (CvMap.cpp:291)
- CvMap::setupGraphical  (CvMap.cpp:263)
- CvPlayer::acquireCity  (CvPlayer.cpp:2337)
- CvPlayer::assimilatePlayer  (CvPlayer.cpp:22587)
- CvPlayer::doAdvancedStartAction  (CvPlayer.cpp:16732)
- CvPlayer::doEspionageMission  (CvPlayer.cpp:16106)
- CvPlayer::initFreeUnits  (CvPlayer.cpp:1848)
- CvPlayer::receiveGoody  (CvPlayer.cpp:6344)
- CvPlayer::setupGraphical  (CvPlayer.cpp:1815)
- CvPlayer::splitEmpire  (CvPlayer.cpp:22363)
- CvPlayerAI::AI_dealVal  (CvPlayerAI.cpp:8823)
- CvPlayerAI::AI_doAdvancedStart  (CvPlayerAI.cpp:23691)
- CvPlayerAI::AI_doTurnPost  (CvPlayerAI.cpp:543)
- CvPlot::CvPlot  (CvPlot.cpp:44)
- CvPlot::changeStolenVisibilityCount  (CvPlot.cpp:7129)
- CvPlot::changeVisibilityCount  (CvPlot.cpp:7033)
- CvPlot::init  (CvPlot.cpp:108)
- CvPlot::read  (CvPlot.cpp:8990)
- CvPlot::setImprovementType  (CvPlot.cpp:5662)
- CvPlot::setRouteType  (CvPlot.cpp:5783)
- CvSelectionGroup::setRemoteTransportUnit  (CvSelectionGroup.cpp:5064)
- CvTeam::addTeam  (CvTeam.cpp:520)
- CvTeam::resetPlotAndCityData  (CvTeam.cpp:433)
- CvUnit::airlift  (CvUnit.cpp:4136)
- CvUnit::attackForDamage  (CvUnit.cpp:2986)
- CvUnit::espionage  (CvUnit.cpp:7265)
- CvUnit::init  (CvUnit.cpp:100)
- CvUnit::jumpToNearestValidPlot  (CvUnit.cpp:3149)
- CvUnit::kill  (CvUnit.cpp:520)
- CvUnit::move  (CvUnit.cpp:3106)
- CvUnit::paradrop  (CvUnit.cpp:4637)
- CvUnit::reloadEntity  (CvUnit.cpp:83)
- CvUnit::testSpyIntercepted  (CvUnit.cpp:7333)
- CvUnit::updateAirCombat  (CvUnit.cpp:1011)
- CvUnit::updateAirStrike  (CvUnit.cpp:804)
- CvUnit::updateCombat  (CvUnit.cpp:1328)
- CvUnit::updateStackCombat  (CvUnit.cpp:15735)
- CyCity::setRevealed  (CyCity.cpp:2236)
- CyPlot::setRevealed  (CyPlot.cpp:967)
- CyUnit::setXY  (CyUnit.cpp:1192)

### level 2 (122)

- CvCity::applyEvent  (CvCity.cpp:15152)
- CvCity::doTask  (CvCity.cpp:1446)
- CvCity::kill  (CvCity.cpp:947)
- CvCity::liberate  (CvCity.cpp:15846)
- CvCity::popOrder  (CvCity.cpp:12842)
- CvDeal::doTurn  (CvDeal.cpp:298)
- CvGame::createBarbarianUnits  (CvGame.cpp:6838)
- CvGame::doGlobalWarming  (CvGame.cpp:6083)
- CvGame::implementDeal  (CvGame.cpp:2623)
- CvGame::initFreeState  (CvGame.cpp:762)
- CvGame::initFreeUnits  (CvGame.cpp:822)
- CvGame::processVote  (CvGame.cpp:7782)
- CvGame::regenerateMap  (CvGame.cpp:348)
- CvGame::replaceCorporation  (CvGame.cpp:3185)
- CvGameAI::CvGameAI  (CvGameAI.cpp:13)
- CvGameAI::read  (CvGameAI.cpp:113)
- CvMap::init  (CvMap.cpp:65)
- CvMap::read  (CvMap.cpp:1300)
- CvMapGenerator::addGoodies  (CvMapGenerator.cpp:888)
- CvNetAdvancedStartAction::Execute  (CvMessageData.cpp:484)
- CvNetEmpireSplit::Execute  (CvMessageData.cpp:588)
- CvPlayer::applyEvent  (CvPlayer.cpp:20650)
- CvPlayer::changeCiv  (CvPlayer.cpp:1573)
- CvPlayer::disbandUnit  (CvPlayer.cpp:3124)
- CvPlayer::doGoody  (CvPlayer.cpp:6546)
- CvPlayer::doTurn  (CvPlayer.cpp:3918)
- CvPlayer::init  (CvPlayer.cpp:191)
- CvPlayer::initCity  (CvPlayer.cpp:2320)
- CvPlayer::initInGame  (CvPlayer.cpp:445)
- CvPlayer::initUnit  (CvPlayer.cpp:3107)
- CvPlayer::killGoldenAgeUnits  (CvPlayer.cpp:9580)
- CvPlayer::killUnits  (CvPlayer.cpp:3282)
- CvPlayer::setTurnActive  (CvPlayer.cpp:12160)
- CvPlayerAI::AI_advancedStartDoRoute  (CvPlayerAI.cpp:23452)
- CvPlayerAI::AI_advancedStartPlaceCity  (CvPlayerAI.cpp:23338)
- CvPlayerAI::AI_advancedStartPlaceExploreUnits  (CvPlayerAI.cpp:23229)
- CvPlayerAI::AI_advancedStartRevealRadius  (CvPlayerAI.cpp:23313)
- CvPlayerAI::AI_advancedStartRouteTerritory  (CvPlayerAI.cpp:23488)
- CvPlayerAI::AI_considerOffer  (CvPlayerAI.cpp:8937)
- CvPlayerAI::AI_disbandUnit  (CvPlayerAI.cpp:20029)
- CvPlayerAI::AI_doSplit  (CvPlayerAI.cpp:19880)
- CvPlayerAI::AI_doTurnUnitsPost  (CvPlayerAI.cpp:625)
- CvPlayerAI::AI_stopTradingTradeVal  (CvPlayerAI.cpp:10347)
- CvPlot::applyEvent  (CvPlot.cpp:9998)
- CvPlot::changeAdjacentSight  (CvPlot.cpp:1698)
- CvPlot::changeBuildProgress  (CvPlot.cpp:7810)
- CvPlot::doCulture  (CvPlot.cpp:8732)
- CvPlot::doImprovementUpgrade  (CvPlot.cpp:537)
- CvPlot::erase  (CvPlot.cpp:293)
- CvPlot::nukeExplosion  (CvPlot.cpp:902)
- CvPlot::removeGoody  (CvPlot.cpp:3541)
- CvPlot::setFeatureType  (CvPlot.cpp:5441)
- CvPlot::setOwner  (CvPlot.cpp:4846)
- CvPlot::updateCityRoute  (CvPlot.cpp:5830)
- CvPlot::verifyUnitValidPlot  (CvPlot.cpp:806)
- CvSelectionGroup::continueMission  (CvSelectionGroup.cpp:2043)
- CvSelectionGroup::groupAttack  (CvSelectionGroup.cpp:4392)
- CvSelectionGroup::groupMove  (CvSelectionGroup.cpp:4697)
- CvSelectionGroup::groupStackAttack  (CvSelectionGroup.cpp:6368)
- CvSelectionGroup::startMission  (CvSelectionGroup.cpp:1372)
- ... 62 more

### files touched by the reach (functions per file)

CvUnitAI.cpp 165, CvUnit.cpp 84, CvPlayer.cpp 68, CvGame.cpp 52, CvCity.cpp 40, CvPlot.cpp 37, CvTeam.cpp 37, CyPlayer.cpp 34, CvPlayerAI.cpp 28, CvSelectionGroup.cpp 21, CyCity.cpp 19, CyUnit.cpp 19, CyTeam.cpp 18, CvMessageData.cpp 17, CyPlot.cpp 15, CvMap.cpp 13, CvCityAI.cpp 13, CvMapGenerator.cpp 10, CyMapGenerator.cpp 10, CvDeal.cpp 8, CyMap.cpp 7, CyGame.cpp 6, CvSelectionGroupAI.cpp 6, CvDLLButtonPopup.cpp 3, CvTeamAI.cpp 3, CySelectionGroup.cpp 3, CvGameAI.cpp 2, FFreeListTrashArray.h 2, CvGameInterface.cpp 2, CyCityInterface1.cpp 1, CyPlotInterface1.cpp 1, CyUnitInterface1.cpp 1, CvDLLPython.cpp 1, CvGlobals.cpp 1, CyMapInterface.cpp 1, CyPlayerInterface2.cpp 1, CyPlayerInterface1.cpp 1, CyTeamInterface.cpp 1, CyGameInterface.cpp 1, CyMapGeneratorInterface.cpp 1

## Exits from the DLL among them

- called by the exe (exported): 75: CvCity::cheat  (CvCity.cpp:16117); CvDLLButtonPopup::OnOkClicked  (CvDLLButtonPopup.cpp:75); CvDLLButtonPopup::launchButtonPopup  (CvDLLButtonPopup.cpp:855); CvDeal::kill  (CvDeal.cpp:78); CvGame::CvGame  (CvGame.cpp:50); CvGame::cheatSpaceship  (CvGameInterface.cpp:2561); CvGame::implementDeal  (CvGame.cpp:2623); CvGame::init  (CvGame.cpp:108); CvGame::initDiplomacy  (CvGame.cpp:706); CvGame::initFreeState  (CvGame.cpp:762); CvGame::initFreeUnits  (CvGame.cpp:822); CvGame::nextActivePlayer  (CvGameInterface.cpp:2691); CvGame::normalizeStartingPlots  (CvGame.cpp:2024); CvGame::read  (CvGame.cpp:8286); CvGame::regenerateMap  (CvGame.cpp:348) ...
- bound for Python: 132: acquireCity, addFeatures, addGameElements, addGoodies, addLakes, addPlayer, addProductionExperience, addTeam, assignVassal, assimilatePlayer, attackForDamage, changeBuildProgress, changeCiv, changeCombatExperience, changeCulture, changeCultureTimes100, changeDamage, changeEspionagePointsAgainstTeam, changeExperience, changeExtraWaterSeeFromCount, changeOccupationTimer, changeProjectCount, changeResearchProgress, changeTechShareCount, changeVisibilityCount
- Python modules calling them: 36: AbandonCityEventManager.py, BUG/DealUtil.py, BUG/Scoreboard.py, Contrib/AStarTools.py, Contrib/MapFinder.py, Contrib/MonkeyTools.py, Contrib/RevDCMReligionControl.py, CvDiplomacy.py, CvMapGeneratorUtil.py, CvUtil.py, EnhancedTechConquestUtils/EnhancedTechConquest.py, EntryPoints/CvRandomEventInterface.py, ModTools/ModTools.py, ModTools/ModToolsUtils.py, PyHelpers.py, Revolution/Development/ChangePlayer.py, Revolution/Development/Tester.py, Revolution/Gameready/AIAutoPlay.py, Revolution/Gameready/BarbarianCiv.py, Revolution/Gameready/Revolution.py, Revolution/Gameready/StartAsMinors.py, Revolution/Gameready/TechDiffusion.py, Revolution/RevEvents.py, Revolution/RevUtils.py, RoMEventManager.py ...
