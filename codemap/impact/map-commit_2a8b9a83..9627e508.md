# Impact of 2a8b9a83eb5b..9627e508fedc

Commits:

- 9627e50 2026-11-21 Map trade fix, GPT fix also
- 9b85482 2026-11-20 Update 3 files
- 71de0ab 2026-10-25 Merge branch 'claude/paging-zoom' into 'main'
- 35abef1 2026-10-25 Graphics paging: no tile-art rebuild on page-in, at most GRAPHICS_PAGING_MAX_IN set-ups per update
- 8c3d192 2026-10-25 Merge branch 'claude/diplomacy-values' into 'main'
- 109bc67 2026-10-25 Diplomacy: trade values from effects, offers by value (AI_DIPLOMACY_FLAGS)
- 3bec049 2026-10-25 Merge branch 'claude/paging-interface' into 'main'
- 44c47e7 2026-10-25 Graphics paging: read the camera through CvScreensInterface, drop the mod's CvGameInterface.py
- 4ec8ebc 2026-10-25 Merge branch 'claude/paging-docs' into 'main'
- 60b153a 2026-10-25 Docs: graphics paging as main holds it after !60
- 1c24b6c 2026-10-25 Merge branch 'claude/paging-coherence' into 'main'
- cadd95b 2026-10-25 Graphics paging: the window is what the camera shows
- 006b784 2026-10-25 Graphics paging: a plot keeps its graphics while anything on it keeps its own
- d929b57 2026-10-25 Merge branch 'claude/graphics-paging-fix' into 'main'
- 9b3afb3 2026-10-25 Graphics paging: keep plot builders, a switch per part, getCameraZoom argument
- a459d0d 2026-10-25 Merge branch 'claude/graphics-paging' into 'main'
- ccbc1b5 2026-10-25 Graphics paging: CvGameInterface.py with getCameraZoom
- b8741b5 2026-10-25 Graphics paging (4/4): paging manager, plot paging with yield symbols and flags, billboard filter, no billboard debug log, defines
- d9d6092 2026-10-25 Graphics paging (3/4): CvCity paging, CvGame and CvPlot declarations, addEntityMission, guarded player calls
- 4b7f27d 2026-10-25 Graphics paging (2/4): CvUnit paging, guarded entity calls, addEntityMission
- 8c494eb 2026-10-25 Graphics paging (1/4): CvDLLEntity paged-out flag and guarded visual wrappers
- c42be8b 2026-10-24 Merge branch 'claude/pedia-localization' into 'main'
- 1e21694 2026-10-24 Civics text in five languages, part 6 (patch 0021)
- 4577065 2026-10-24 Civics text in five languages, part 5 (patch 0021)
- c0c306b 2026-10-24 Civics text in five languages, part 4 (patch 0021)
- cb9d70e 2026-10-24 Civics text in five languages, part 3 (patch 0021)
- a302b56 2026-10-24 Civics text in five languages, part 2 (patch 0021)
- 88a2015 2026-10-24 Civics text in five languages, part 1 (patch 0021)
- 002af76 2026-10-24 Civilopedia and strategy text: School of Scribes, River Port, Trade (patch 0020)
- 8cee347 2026-10-24 Siam: repair the é the connector re-encoded as UTF-8
- a0c809d 2026-10-24 Siam: put the languages of two entries back in order (patch 0020, 1/2)

```
 Assets/CvGameCoreDLL/CvCity.cpp                    |   94 +-
 Assets/CvGameCoreDLL/CvCity.h                      |    2 +
 Assets/CvGameCoreDLL/CvDLLEntity.cpp               |   57 +-
 Assets/CvGameCoreDLL/CvDLLEntity.h                 |    4 +
 Assets/CvGameCoreDLL/CvDeal.cpp                    |    6 +-
 Assets/CvGameCoreDLL/CvGame.cpp                    |  668 ++++++-
 Assets/CvGameCoreDLL/CvGame.h                      |   40 +
 Assets/CvGameCoreDLL/CvGameCoreUtils.cpp           |   28 +
 Assets/CvGameCoreDLL/CvGameCoreUtils.h             |   14 +
 Assets/CvGameCoreDLL/CvGameTextMgr.cpp             |    7 -
 Assets/CvGameCoreDLL/CvPlayer.cpp                  |   10 +-
 Assets/CvGameCoreDLL/CvPlayerAI.cpp                |  374 +++-
 Assets/CvGameCoreDLL/CvPlayerAI.h                  |    3 +
 Assets/CvGameCoreDLL/CvPlot.cpp                    |  215 ++-
 Assets/CvGameCoreDLL/CvPlot.h                      |   15 +
 Assets/CvGameCoreDLL/CvSelectionGroup.cpp          |    2 +-
 Assets/CvGameCoreDLL/CvTeamAI.cpp                  |    7 +
 Assets/CvGameCoreDLL/CvUnit.cpp                    |  165 +-
 Assets/CvGameCoreDLL/CvUnit.h                      |    2 +
 Assets/Python/EntryPoints/CvScreensInterface.py    |   31 +
 Assets/XML/BBAI_AI_Variables_GlobalDefines.xml     |   12 +
 Assets/XML/GlobalDefinesAlt.xml                    |   91 +
 Assets/XML/Text/RoM_CIV4GameText_Siam.xml          |    6 +-
 Assets/XML/Text/RoM_GameText_Civics.xml            | 1884 ++++++++++----------
 .../Text/RoM_GameText_Civilopedia_Buildings.xml    |   20 +-
 .../RoM_GameText_Civilopedia_CivicsReligion.xml    |   20 +-
 Assets/XML/Text/RoM_GameText_Civilopedia_Techs.xml |   10 +-
 Assets/XML/Text/RoM_GameText_Strategy.xml          |   66 +-
 Docs/DIPLOMACY_VALUES.md                           |   95 +
 Docs/GRAPHICS_PAGING.md                            |  245 +++
 30 files changed, 3092 insertions(+), 1101 deletions(-)
```

## Functions

- changed: 71; added: 31; removed: 0
  - changed CvCity::setupGraphical  (CvCity.cpp:737-760)
  - changed CvCity::isInfoDirty  (CvCity.cpp:8760-8768)
  - changed CvCity::isLayoutDirty  (CvCity.cpp:8777-8785)
  - changed CvCity::setRevealed  (CvCity.cpp:10862-10905)
  - changed CvDLLEntity::CvDLLEntity  (CvDLLEntity.cpp:6-9)
  - changed CvDLLEntity::setVisible  (CvDLLEntity.cpp:26-34)
  - changed CvDLLEntity::IsSelected  (CvDLLEntity.cpp:51-59)
  - changed CvDLLEntity::PlayAnimation  (CvDLLEntity.cpp:61-69)
  - changed CvDLLEntity::StopAnimation  (CvDLLEntity.cpp:71-79)
  - changed CvDLLEntity::MoveTo  (CvDLLEntity.cpp:81-89)
  - changed CvDLLEntity::QueueMove  (CvDLLEntity.cpp:91-99)
  - changed CvDLLEntity::ExecuteMove  (CvDLLEntity.cpp:101-109)
  - changed CvDLLEntity::SetPosition  (CvDLLEntity.cpp:111-119)
  - changed CvDLLEntity::NotifyEntity  (CvDLLEntity.cpp:121-129)
  - changed CvDLLEntity::SetSiegeTower  (CvDLLEntity.cpp:131-139)
  - changed CvDLLEntity::GetSiegeTower  (CvDLLEntity.cpp:141-149)
  - changed CvDeal::startTrade  (CvDeal.cpp:695-1094)
  - changed CvGame::reset  (CvGame.cpp:482-726)
  - changed CvGame::update  (CvGame.cpp:2170-2255)
  - changed CvGame::setActivePlayer  (CvGame.cpp:5343-5421)
  - changed CvGame::updateUnitEnemyGlow  (CvGame.cpp:5423-5439)
  - changed CvPlayer::setCurrentEra  (CvPlayer.cpp:12643-12713)
  - changed CvPlayer::doWarnings  (CvPlayer.cpp:18218-18297)
  - changed CvPlayerAI::AI_considerOffer  (CvPlayerAI.cpp:8936-9087)
  - changed CvPlayerAI::AI_counterPropose  (CvPlayerAI.cpp:9090-9641)
  - changed CvPlayerAI::AI_goldPerTurnTradeVal  (CvPlayerAI.cpp:9702-9708)
  - changed CvPlayerAI::AI_bonusTradeVal  (CvPlayerAI.cpp:10119-10159)
  - changed CvPlayerAI::AI_doDiplo  (CvPlayerAI.cpp:17242-19180)
  - changed CvPlot::reset  (CvPlot.cpp:179-266)
  - changed CvPlot::setupGraphical  (CvPlot.cpp:272-294)
  - changed CvPlot::updateSymbols  (CvPlot.cpp:846-898)
  - changed CvPlot::changeVisibilityCount  (CvPlot.cpp:7183-7263)
  - changed CvPlot::setRevealed  (CvPlot.cpp:7695-7810)
  - changed CvPlot::setRevealedImprovementType  (CvPlot.cpp:7876-7904)
  - changed CvPlot::setRevealedRouteType  (CvPlot.cpp:7928-7959)
  - changed CvPlot::updateFeatureSymbol  (CvPlot.cpp:8083-8095)
  - changed CvPlot::updateFlagSymbol  (CvPlot.cpp:8308-8411)
  - changed CvPlot::setLayoutDirty  (CvPlot.cpp:9674-9693)
  - changed CvPlot::updatePlotBuilder  (CvPlot.cpp:9695-9709)
  - changed CvSelectionGroup::startMission  (CvSelectionGroup.cpp:1371-2039)
  - changed CvTeamAI::AI_techTradeVal  (CvTeamAI.cpp:1691-1748)
  - changed CvUnit::setupGraphical  (CvUnit.cpp:434-459)
  - changed CvUnit::kill  (CvUnit.cpp:581-783)
  - changed CvUnit::NotifyEntity  (CvUnit.cpp:786-794)
  - changed CvUnit::updateAirStrike  (CvUnit.cpp:870-940)
  - changed CvUnit::updateAirCombat  (CvUnit.cpp:1077-1244)
  - changed CvUnit::updateCombat  (CvUnit.cpp:1394-1851)
  - changed CvUnit::attackForDamage  (CvUnit.cpp:3052-3169)
  - changed CvUnit::airCircle  (CvUnit.cpp:3921-3947)
  - changed CvUnit::nuke  (CvUnit.cpp:4335-4562)
  - changed CvUnit::recon  (CvUnit.cpp:4604-4633)
  - changed CvUnit::paradrop  (CvUnit.cpp:4703-4738)
  - changed CvUnit::airBomb  (CvUnit.cpp:4894-5205)
  - changed CvUnit::bombard  (CvUnit.cpp:5289-5349)
  - changed CvUnit::pillage  (CvUnit.cpp:5399-5570)
  - changed CvUnit::setXY  (CvUnit.cpp:10565-11027)
  - changed CvUnit::setPromotionReady  (CvUnit.cpp:11998-12021)
  - changed CvUnit::setHasPromotion  (CvUnit.cpp:12724-12825)
  - changed CvUnit::rangeStrike  (CvUnit.cpp:13590-13690)
  - changed CvUnit::isCombatVisible  (CvUnit.cpp:14319-14355)
  - changed CvUnit::airBomb1  (CvUnit.cpp:14532-14626)
  - changed CvUnit::airBomb2  (CvUnit.cpp:14683-14829)
  - changed CvUnit::airBomb3  (CvUnit.cpp:14886-15031)
  - changed CvUnit::airBomb4  (CvUnit.cpp:15127-15257)
  - changed CvUnit::airBomb5  (CvUnit.cpp:15314-15400)
  - changed CvUnit::bombardRanged  (CvUnit.cpp:15530-15757)
  - changed CvUnit::updateStackCombat  (CvUnit.cpp:15837-16254)
  - changed CvUnit::doOpportunityFire  (CvUnit.cpp:16258-16317)
  - changed CvUnit::doActiveDefense  (CvUnit.cpp:16321-16386)
  - changed CvUnit::archerBombard  (CvUnit.cpp:16446-16544)
  - changed CvUnit::fighterEngage  (CvUnit.cpp:16622-16718)
  - added CvCity::canPageGraphicsOut  (CvCity.cpp:763-766)
  - added CvCity::pageGraphics  (CvCity.cpp:770-806)
  - added CvDLLEntity::isGraphicsPagedOut  (CvDLLEntity.h:60-60)
  - added CvGame::isGraphicsPaging  (CvGame.cpp:2261-2264)
  - added CvGame::isGraphicsPagingSymbols  (CvGame.cpp:2266-2269)
  - added CvGame::isGraphicsPagingPlots  (CvGame.cpp:2271-2274)
  - added CvGame::isGraphicsPagingBuilders  (CvGame.cpp:2276-2279)
  - added CvGame::isInGraphicsWindow  (CvGame.cpp:2281-2293)
  - added CvGame::beginBulkReveal  (CvGame.cpp:2295-2306)
  - added CvGame::endBulkReveal  (CvGame.cpp:2308-2323)
  - added CvGame::deferRevealedGraphics  (CvGame.cpp:2325-2340)
  - added CvGame::processDeferredReveals  (CvGame.cpp:2342-2391)
  - added CvGame::updateGraphicsPaging  (CvGame.cpp:2393-2539)
  - added CvGame::graphicsWindowFromCamera  (CvGame.cpp:2549-2669)
  - added CvGame::pageGraphics  (CvGame.cpp:2677-2877)
  - added isAIDiplomacy  (CvGameCoreUtils.cpp:10-13)
  - added addEntityMission  (CvGameCoreUtils.cpp:218-237)
  - added CvPlayerAI::AI_bonusCityValue  (CvPlayerAI.cpp:10169-10277)
  - added bonusUnlockTechWeight  (CvPlayerAI.cpp:10282-10294)
  - added CvPlayerAI::AI_bonusUnlockVal  (CvPlayerAI.cpp:10299-10402)
  - added CvPlayerAI::AI_techOfferValue  (CvPlayerAI.cpp:10406-10418)
  - added CvPlot::deferRevealedGraphics  (CvPlot.cpp:296-299)
  - added CvPlot::refreshRevealedGraphics  (CvPlot.cpp:304-332)
  - added CvPlot::pageGraphics  (CvPlot.cpp:341-410)
  - added CvPlot::canPageGraphicsOut  (CvPlot.cpp:412-432)
  - added CvPlot::updateFeatureSymbolEntity  (CvPlot.cpp:8097-8136)
  - added CvPlot::isGraphicsPagedOut  (CvPlot.h:63-63)
  - added CvPlot::isRevealedGraphicsDirty  (CvPlot.h:67-67)
  - added CvPlot::setRevealedGraphicsDirty  (CvPlot.h:68-68)
  - added CvUnit::canPageGraphicsOut  (CvUnit.cpp:462-470)
  - added CvUnit::pageGraphics  (CvUnit.cpp:473-509)

## Member declarations

- added CvDLLEntity::m_bGraphicsPagedOut bool
- added CvGame::m_aiDeferredRevealPlots std::vector<int>
- added CvGame::m_bGraphicsPaging bool
- added CvGame::m_bGraphicsPagingBuilders bool
- added CvGame::m_bGraphicsPagingCities bool
- added CvGame::m_bGraphicsPagingPlots bool
- added CvGame::m_bGraphicsPagingSymbols bool
- added CvGame::m_bGraphicsPagingUnits bool
- added CvGame::m_bPagingPending bool
- added CvGame::m_bPagingPendingOut bool
- added CvGame::m_dwPagingCameraTime DWORD
- added CvGame::m_dwPagingShrinkSince DWORD
- added CvGame::m_dwPagingTime DWORD
- added CvGame::m_eBulkRevealTeam TeamTypes
- added CvGame::m_ePagingActivePlayer PlayerTypes
- added CvGame::m_iBulkRevealDepth int
- added CvGame::m_iPagingEast int
- added CvGame::m_iPagingMargin int
- added CvGame::m_iPagingNorth int
- added CvGame::m_iPagingSouth int
- added CvGame::m_iPagingStep int
- added CvGame::m_iPagingWest int
- added CvGame::m_iPagingX int
- added CvGame::m_iPagingY int
- added CvPlot::m_bGraphicsPagedOut bool
- added CvPlot::m_bPagedBuilder bool
- added CvPlot::m_bPagedPlots bool
- added CvPlot::m_bPagedSymbols bool
- added CvPlot::m_bRevealedGraphicsDirty bool
- added CvPlot::m_bRevealedRouteDirty bool

## Members written on changed lines

CvDLLEntity::m_bGraphicsPagedOut, CvGame::m_aiDeferredRevealPlots, CvGame::m_bGraphicsPaging, CvGame::m_bGraphicsPagingBuilders, CvGame::m_bGraphicsPagingCities, CvGame::m_bGraphicsPagingPlots, CvGame::m_bGraphicsPagingSymbols, CvGame::m_bGraphicsPagingUnits, CvGame::m_bPagingPending, CvGame::m_bPagingPendingOut, CvGame::m_dwPagingCameraTime, CvGame::m_dwPagingShrinkSince, CvGame::m_dwPagingTime, CvGame::m_eBulkRevealTeam, CvGame::m_ePagingActivePlayer, CvGame::m_iBulkRevealDepth, CvGame::m_iPagingEast, CvGame::m_iPagingMargin, CvGame::m_iPagingNorth, CvGame::m_iPagingSouth, CvGame::m_iPagingStep, CvGame::m_iPagingWest, CvGame::m_iPagingX, CvGame::m_iPagingY, CvPlot::m_bGraphicsPagedOut, CvPlot::m_bPagedBuilder, CvPlot::m_bPagedPlots, CvPlot::m_bPagedSymbols, CvPlot::m_bPlotLayoutDirty, CvPlot::m_bRevealedGraphicsDirty, CvPlot::m_bRevealedRouteDirty

## Global defines read on changed lines

- AI_DIPLOMACY_FLAGS in isAIDiplomacy (defined in BBAI_AI_Variables_GlobalDefines.xml)
- BILLBOARD_ACTIVE_TEAM_ONLY in CvGame::setActivePlayer (defined in GlobalDefinesAlt.xml)
- BILLBOARD_ACTIVE_TEAM_ONLY in CvPlot::changeVisibilityCount (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_CAMERA in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_CITIES in CvCity::setupGraphical (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_CITIES in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_INTERVAL_MS in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_LOG in CvGame::pageGraphics (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_LOG in CvGame::processDeferredReveals (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_LOG in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_MARGIN in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_MAX_IN in CvGame::pageGraphics (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_MAX_IN in CvGame::processDeferredReveals (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_MAX_OUT in CvGame::pageGraphics (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_PLOTS in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_PLOT_BUILDERS in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_RANGE_NORTH in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_RANGE_SOUTH in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_RANGE_X in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_SHRINK_MS in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_STEP in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_SYMBOLS in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_UNITS in CvGame::updateGraphicsPaging (defined in GlobalDefinesAlt.xml)
- GRAPHICS_PAGING_UNITS in CvUnit::setupGraphical (defined in GlobalDefinesAlt.xml)
- PEACE_TREATY_LENGTH in CvPlayerAI::AI_counterPropose (defined in GlobalDefines.xml)
- PEACE_TREATY_LENGTH in CvPlayerAI::AI_goldPerTurnTradeVal (defined in GlobalDefines.xml)

## XML files changed

- Assets/XML/BBAI_AI_Variables_GlobalDefines.xml     |   12 +
- Assets/XML/GlobalDefinesAlt.xml                    |   91 +
- Assets/XML/Text/RoM_CIV4GameText_Siam.xml          |    6 +-
- Assets/XML/Text/RoM_GameText_Civics.xml            | 1884 ++++++++++----------
- .../Text/RoM_GameText_Civilopedia_Buildings.xml    |   20 +-
- .../RoM_GameText_Civilopedia_CivicsReligion.xml    |   20 +-
- Assets/XML/Text/RoM_GameText_Civilopedia_Techs.xml |   10 +-
- Assets/XML/Text/RoM_GameText_Strategy.xml          |   66 +-

_Member uses and functions are read from the source at each commit; callers come from the compiler map at its own commit (see skeleton.md), so callers added since then are found only by name._

## Functions outside the compiler map

- CvCity::canPageGraphicsOut is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::pageGraphics, CvCity::setupGraphical; the name is also defined in CvPlot, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvDLLEntity::isGraphicsPagedOut is not in the compiler map (newer than its commit); name match: called from 6 function(s): CvGame::pageGraphics, CvGame::updateUnitEnemyGlow, CvPlayer::doWarnings, CvPlayer::setCurrentEra, CvPlot::canPageGraphicsOut, addEntityMission; the name is also defined in CvPlot, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvPlot::canPageGraphicsOut is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvPlot::pageGraphics, CvPlot::updateFlagSymbol; the name is also defined in CvCity, CvUnit, so calls through an object may be theirs
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvGame::isGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::setupGraphical, CvUnit::setupGraphical
- CvGame::isGraphicsPagingSymbols is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvPlot::pageGraphics
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::isGraphicsPagingPlots is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvPlot::pageGraphics
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::isGraphicsPagingBuilders is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvPlot::pageGraphics
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::isInGraphicsWindow is not in the compiler map (newer than its commit); name match: called from 5 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvGame::processDeferredReveals, CvUnit::setXY, CvUnit::setupGraphical
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvGame::processDeferredReveals is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::endBulkReveal, CvGame::updateGraphicsPaging
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::beginBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::setRevealed, CvPlot::deferRevealedGraphics; the name is also defined in CvPlot, so calls through an object may be theirs
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs
- CvGame::processDeferredReveals is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::endBulkReveal, CvGame::updateGraphicsPaging
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvGame::graphicsWindowFromCamera is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::updateGraphicsPaging
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- isAIDiplomacy is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvPlayerAI::AI_bonusCityValue is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvPlayerAI::AI_bonusTradeVal
- bonusUnlockTechWeight is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvPlayerAI::AI_bonusUnlockVal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvPlayerAI::AI_bonusTradeVal
- CvPlayerAI::AI_techOfferValue is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvPlayerAI::AI_doDiplo
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs
- CvPlot::refreshRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::processDeferredReveals
- CvGame::processDeferredReveals is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::endBulkReveal, CvGame::updateGraphicsPaging
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvPlot::canPageGraphicsOut is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvPlot::pageGraphics, CvPlot::updateFlagSymbol; the name is also defined in CvCity, CvUnit, so calls through an object may be theirs
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvPlot::updateFeatureSymbolEntity is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvPlot::pageGraphics, CvPlot::updateFeatureSymbol
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvPlot::isGraphicsPagedOut is not in the compiler map (newer than its commit); name match: called from 6 function(s): CvGame::pageGraphics, CvGame::updateUnitEnemyGlow, CvPlayer::doWarnings, CvPlayer::setCurrentEra, CvPlot::canPageGraphicsOut, addEntityMission; the name is also defined in CvDLLEntity, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvPlot::canPageGraphicsOut is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvPlot::pageGraphics, CvPlot::updateFlagSymbol; the name is also defined in CvCity, CvUnit, so calls through an object may be theirs
- CvPlot::pageGraphics is not in the compiler map (newer than its commit); name match: called from 9 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvPlot::updateFlagSymbol, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvUnit, so calls through an object may be theirs
- CvPlot::isRevealedGraphicsDirty is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::deferRevealedGraphics, CvGame::processDeferredReveals
- CvGame::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::setRevealed, CvPlot::deferRevealedGraphics; the name is also defined in CvPlot, so calls through an object may be theirs
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs
- CvGame::processDeferredReveals is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvGame::endBulkReveal, CvGame::updateGraphicsPaging
- CvGame::endBulkReveal is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvDeal::startTrade
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- CvPlot::setRevealedGraphicsDirty is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::deferRevealedGraphics
- CvGame::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvCity::setRevealed, CvPlot::deferRevealedGraphics; the name is also defined in CvPlot, so calls through an object may be theirs
- CvPlot::deferRevealedGraphics is not in the compiler map (newer than its commit); name match: called from 4 function(s): CvCity::setRevealed, CvPlot::setRevealed, CvPlot::setRevealedImprovementType, CvPlot::setRevealedRouteType; the name is also defined in CvGame, so calls through an object may be theirs
- CvUnit::canPageGraphicsOut is not in the compiler map (newer than its commit); name match: called from 2 function(s): CvUnit::pageGraphics, CvUnit::setupGraphical; the name is also defined in CvCity, CvPlot, so calls through an object may be theirs
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)
- CvUnit::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvGame, CvPlot, so calls through an object may be theirs
- CvCity::pageGraphics is not in the compiler map (newer than its commit); name match: called from 7 function(s): CvCity::setupGraphical, CvGame::pageGraphics, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvGame, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::pageGraphics is not in the compiler map (newer than its commit); name match: called from 8 function(s): CvCity::pageGraphics, CvCity::setupGraphical, CvGame::updateGraphicsPaging, CvUnit::isCombatVisible, CvUnit::pageGraphics, CvUnit::setXY, CvUnit::setupGraphical, addEntityMission; the name is also defined in CvCity, CvPlot, CvUnit, so calls through an object may be theirs
- CvGame::updateGraphicsPaging is not in the compiler map (newer than its commit); name match: called from 1 function(s): CvGame::update
- addEntityMission is not in the compiler map (newer than its commit); name match: called from 0 function(s)

## Member variables

- **CvDLLEntity::m_bGraphicsPagedOut**: written in 4 function(s), read in 16
  - written (or passed by address / method called): CvCity::pageGraphics, CvCity::setupGraphical, CvUnit::pageGraphics, CvUnit::setupGraphical
  - read: CvCity::isInfoDirty, CvCity::isLayoutDirty, CvCity::pageGraphics, CvDLLEntity::ExecuteMove, CvDLLEntity::GetSiegeTower, CvDLLEntity::IsSelected, CvDLLEntity::MoveTo, CvDLLEntity::NotifyEntity, CvDLLEntity::PlayAnimation, CvDLLEntity::QueueMove, CvDLLEntity::SetPosition, CvDLLEntity::SetSiegeTower ...
- **CvGame::m_aiDeferredRevealPlots**: written in 3 function(s), read in 3
  - written (or passed by address / method called): CvGame::deferRevealedGraphics, CvGame::processDeferredReveals, CvGame::reset
  - read: CvGame::deferRevealedGraphics, CvGame::processDeferredReveals, CvGame::reset
- **CvGame::m_bGraphicsPaging**: written in 3 function(s), read in 4
  - written (or passed by address / method called): CvGame::pageGraphics, CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isGraphicsPaging, CvGame::isInGraphicsWindow, CvGame::processDeferredReveals, CvGame::updateGraphicsPaging
- **CvGame::m_bGraphicsPagingBuilders**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isGraphicsPagingBuilders, CvGame::pageGraphics
- **CvGame::m_bGraphicsPagingCities**: written in 2 function(s), read in 1
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::pageGraphics
- **CvGame::m_bGraphicsPagingPlots**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isGraphicsPagingPlots, CvGame::pageGraphics
- **CvGame::m_bGraphicsPagingSymbols**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isGraphicsPagingSymbols, CvGame::pageGraphics
- **CvGame::m_bGraphicsPagingUnits**: written in 2 function(s), read in 1
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::pageGraphics
- **CvGame::m_bPagingPending**: written in 3 function(s), read in 1
  - written (or passed by address / method called): CvGame::pageGraphics, CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_bPagingPendingOut**: written in 3 function(s), read in 1
  - written (or passed by address / method called): CvGame::pageGraphics, CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_dwPagingCameraTime**: written in 2 function(s), read in 1
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_dwPagingShrinkSince**: written in 2 function(s), read in 1
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_dwPagingTime**: written in 2 function(s), read in 1
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_eBulkRevealTeam**: written in 3 function(s), read in 2
  - written (or passed by address / method called): CvGame::beginBulkReveal, CvGame::endBulkReveal, CvGame::reset
  - read: CvGame::beginBulkReveal, CvGame::deferRevealedGraphics
- **CvGame::m_ePagingActivePlayer**: written in 2 function(s), read in 1
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_iBulkRevealDepth**: written in 3 function(s), read in 4
  - written (or passed by address / method called): CvGame::beginBulkReveal, CvGame::endBulkReveal, CvGame::reset
  - read: CvGame::beginBulkReveal, CvGame::deferRevealedGraphics, CvGame::endBulkReveal, CvGame::processDeferredReveals
- **CvGame::m_iPagingEast**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isInGraphicsWindow, CvGame::updateGraphicsPaging
- **CvGame::m_iPagingMargin**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isInGraphicsWindow, CvGame::updateGraphicsPaging
- **CvGame::m_iPagingNorth**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isInGraphicsWindow, CvGame::updateGraphicsPaging
- **CvGame::m_iPagingSouth**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isInGraphicsWindow, CvGame::updateGraphicsPaging
- **CvGame::m_iPagingStep**: written in 2 function(s), read in 1
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::updateGraphicsPaging
- **CvGame::m_iPagingWest**: written in 2 function(s), read in 2
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isInGraphicsWindow, CvGame::updateGraphicsPaging
- **CvGame::m_iPagingX**: written in 2 function(s), read in 3
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isInGraphicsWindow, CvGame::pageGraphics, CvGame::updateGraphicsPaging
- **CvGame::m_iPagingY**: written in 2 function(s), read in 3
  - written (or passed by address / method called): CvGame::reset, CvGame::updateGraphicsPaging
  - read: CvGame::isInGraphicsWindow, CvGame::pageGraphics, CvGame::updateGraphicsPaging
- **CvPlot::m_bGraphicsPagedOut**: written in 3 function(s), read in 7
  - written (or passed by address / method called): CvPlot::pageGraphics, CvPlot::reset, CvPlot::setupGraphical
  - read: CvPlot::isGraphicsPagedOut, CvPlot::pageGraphics, CvPlot::setLayoutDirty, CvPlot::updateFeatureSymbolEntity, CvPlot::updateFlagSymbol, CvPlot::updatePlotBuilder, CvPlot::updateSymbols
- **CvPlot::m_bPagedBuilder**: written in 3 function(s), read in 3
  - written (or passed by address / method called): CvPlot::pageGraphics, CvPlot::reset, CvPlot::setupGraphical
  - read: CvPlot::pageGraphics, CvPlot::setLayoutDirty, CvPlot::updatePlotBuilder
- **CvPlot::m_bPagedPlots**: written in 3 function(s), read in 2
  - written (or passed by address / method called): CvPlot::pageGraphics, CvPlot::reset, CvPlot::setupGraphical
  - read: CvPlot::pageGraphics, CvPlot::updateFeatureSymbolEntity
- **CvPlot::m_bPagedSymbols**: written in 3 function(s), read in 3
  - written (or passed by address / method called): CvPlot::pageGraphics, CvPlot::reset, CvPlot::setupGraphical
  - read: CvPlot::pageGraphics, CvPlot::updateFlagSymbol, CvPlot::updateSymbols
- **CvPlot::m_bPlotLayoutDirty**: written in 3 function(s), read in 1
  - written (or passed by address / method called): CvPlot::pageGraphics, CvPlot::reset, CvPlot::setLayoutDirty
  - read: CvPlot::isLayoutDirty
- **CvPlot::m_bRevealedGraphicsDirty**: written in 4 function(s), read in 2
  - written (or passed by address / method called): CvPlot::refreshRevealedGraphics, CvPlot::reset, CvPlot::setRevealedGraphicsDirty, CvPlot::setupGraphical
  - read: CvPlot::isRevealedGraphicsDirty, CvPlot::refreshRevealedGraphics
- **CvPlot::m_bRevealedRouteDirty**: written in 4 function(s), read in 1
  - written (or passed by address / method called): CvPlot::refreshRevealedGraphics, CvPlot::reset, CvPlot::setRevealedRouteType, CvPlot::setupGraphical
  - read: CvPlot::refreshRevealedGraphics

The readers above are added to the reach (19 in the compiler map).

## Reach per changed function

| function | direct callers | all callers | exported reached | Python-bound reached |
|---|---|---|---|---|
| CvPlot::updateSymbols | 8 | 815 | 79 | 154 |
| CvPlot::updatePlotBuilder | 2 | 811 | 81 | 151 |
| CvDLLEntity::IsSelected | 23 | 794 | 80 | 145 |
| CvPlot::isLayoutDirty | 1 | 780 | 82 | 147 |
| CvPlot::setLayoutDirty | 11 | 779 | 81 | 147 |
| CvUnit::airCircle | 2 | 758 | 72 | 134 |
| CvUnit::NotifyEntity | 28 | 755 | 74 | 134 |
| CvDLLEntity::setVisible | 1 | 741 | 73 | 135 |
| CvPlot::setRevealedRouteType | 3 | 727 | 68 | 130 |
| CvDLLEntity::CvDLLEntity | 2 | 727 | 67 | 127 |
| CvCity::setRevealed | 4 | 725 | 67 | 130 |
| CvTeamAI::AI_techTradeVal | 5 | 724 | 66 | 127 |
| CvPlot::setRevealedImprovementType | 3 | 724 | 67 | 129 |
| CvPlot::setRevealed | 14 | 723 | 67 | 129 |
| CvPlayerAI::AI_goldPerTurnTradeVal | 3 | 722 | 66 | 127 |
| CvPlayerAI::AI_bonusTradeVal | 3 | 722 | 66 | 127 |
| CvUnit::setupGraphical | 3 | 721 | 67 | 128 |
| CvUnit::setPromotionReady | 3 | 720 | 67 | 128 |
| CvPlot::updateFeatureSymbol | 3 | 719 | 67 | 127 |
| CvPlayer::setCurrentEra | 3 | 718 | 66 | 128 |
| CvCity::setupGraphical | 2 | 718 | 67 | 127 |
| CvDLLEntity::SetSiegeTower | 1 | 718 | 67 | 127 |
| CvUnit::isCombatVisible | 5 | 717 | 66 | 127 |
| CvDLLEntity::ExecuteMove | 4 | 717 | 67 | 127 |
| CvDLLEntity::SetPosition | 1 | 717 | 67 | 127 |
| CvDLLEntity::QueueMove | 1 | 717 | 67 | 127 |
| CvUnit::kill | 52 | 716 | 66 | 127 |
| CvUnit::setXY | 11 | 716 | 66 | 127 |
| CvUnit::setHasPromotion | 8 | 716 | 66 | 127 |
| CvUnit::updateAirStrike | 4 | 716 | 66 | 127 |
| CvUnit::bombardRanged | 3 | 716 | 66 | 127 |
| CvUnit::archerBombard | 3 | 716 | 66 | 127 |
| CvPlot::changeVisibilityCount | 3 | 716 | 66 | 127 |
| CvUnit::updateCombat | 2 | 716 | 66 | 127 |
| CvUnit::updateAirCombat | 2 | 716 | 66 | 127 |
| CvUnit::rangeStrike | 2 | 716 | 66 | 127 |
| CvUnit::airBomb5 | 2 | 716 | 66 | 127 |
| CvUnit::airBomb4 | 2 | 716 | 66 | 127 |
| CvUnit::airBomb3 | 2 | 716 | 66 | 127 |
| CvUnit::airBomb2 | 2 | 716 | 66 | 127 |
| CvUnit::airBomb1 | 2 | 716 | 66 | 127 |
| CvSelectionGroup::startMission | 2 | 716 | 66 | 127 |
| CvUnit::updateStackCombat | 1 | 716 | 66 | 127 |
| CvUnit::recon | 1 | 716 | 66 | 127 |
| CvUnit::pillage | 1 | 716 | 66 | 127 |
| CvUnit::paradrop | 1 | 716 | 66 | 127 |
| CvUnit::nuke | 1 | 716 | 66 | 127 |
| CvUnit::fighterEngage | 1 | 716 | 66 | 127 |
| CvUnit::bombard | 1 | 716 | 66 | 127 |
| CvUnit::airBomb | 1 | 716 | 66 | 127 |
| CvDeal::startTrade | 1 | 716 | 66 | 127 |
| CvGame::updateUnitEnemyGlow | 1 | 47 | 18 | 8 |
| CvGame::setActivePlayer | 5 | 46 | 17 | 8 |
| CvPlayerAI::AI_considerOffer | 2 | 40 | 15 | 6 |
| CvPlayerAI::AI_doDiplo | 1 | 38 | 14 | 6 |
| CvUnit::doOpportunityFire | 1 | 37 | 14 | 6 |
| CvUnit::doActiveDefense | 1 | 37 | 14 | 6 |
| CvPlayer::doWarnings | 1 | 36 | 14 | 6 |
| CvPlot::reset | 3 | 13 | 3 | 1 |
| CvGame::reset | 3 | 11 | 6 | 0 |
| CvPlot::setupGraphical | 1 | 6 | 4 | 1 |
| CvUnit::attackForDamage | 1 | 3 | 1 | 1 |
| CvPlot::updateFlagSymbol | 1 | 1 | 2 | 0 |
| CvPlayerAI::AI_counterPropose | 0 | 0 | 0 | 0 |
| CvGame::update | 0 | 0 | 1 | 0 |
| CvDLLEntity::StopAnimation | 0 | 0 | 1 | 0 |
| CvDLLEntity::PlayAnimation | 0 | 0 | 1 | 0 |
| CvDLLEntity::NotifyEntity | 0 | 0 | 1 | 0 |
| CvDLLEntity::MoveTo | 0 | 0 | 1 | 0 |
| CvDLLEntity::GetSiegeTower | 0 | 0 | 1 | 0 |
| CvDLLEntity::CvDLLEntity | 0 | 0 | 1 | 0 |
| CvCity::isLayoutDirty | 0 | 0 | 1 | 0 |
| CvCity::isInfoDirty | 0 | 0 | 1 | 0 |

Rows include callers of functions newer than the map (name match) and readers of changed members, standing in for the new code they lead to.

## Callers (compiler call graph)

916 function(s) reach the changed code through calls; per level: 1: 140, 2: 232, 3: 215, 4: 212, 5: 57, 6: 25, 7: 22, 8: 12, 9: 1

### level 1 (140)

- CvCity::CvCity  (CvCity.cpp:43)
- CvCity::addProductionExperience  (CvCity.cpp:2899)
- CvCity::init  (CvCity.cpp:157)
- CvCity::setWorkingPlot  (CvCity.cpp:11847)
- CvCity::updateVisibility  (CvCity.cpp:1425)
- CvDLLButtonPopup::OnOkClicked  (CvDLLButtonPopup.cpp:75)
- CvDeal::addTrades  (CvDeal.cpp:119)
- CvGame::CvGame  (CvGame.cpp:50)
- CvGame::changeHumanPlayer  (CvGame.cpp:8924)
- CvGame::createBarbarianUnits  (CvGame.cpp:6838)
- CvGame::cyclePlotUnits  (CvGameInterface.cpp:848)
- CvGame::init  (CvGame.cpp:108)
- CvGame::nextActivePlayer  (CvGameInterface.cpp:2691)
- CvGame::read  (CvGame.cpp:8286)
- CvGame::replaceCorporation  (CvGame.cpp:3185)
- CvGame::selectUnit  (CvGame.cpp:2429)
- CvMap::setRevealedPlots  (CvMap.cpp:291)
- CvMap::setupGraphical  (CvMap.cpp:263)
- CvMap::updateFlagSymbols  (CvMap.cpp:343)
- CvMap::updateSymbols  (CvMap.cpp:396)
- CvPlayer::acquireCity  (CvPlayer.cpp:2337)
- CvPlayer::applyEvent  (CvPlayer.cpp:20650)
- CvPlayer::assimilatePlayer  (CvPlayer.cpp:22587)
- CvPlayer::changeCiv  (CvPlayer.cpp:1573)
- CvPlayer::disbandUnit  (CvPlayer.cpp:3124)
- CvPlayer::doAdvancedStartAction  (CvPlayer.cpp:16732)
- CvPlayer::doEspionageMission  (CvPlayer.cpp:16106)
- CvPlayer::doTurn  (CvPlayer.cpp:3918)
- CvPlayer::initFreeUnits  (CvPlayer.cpp:1848)
- CvPlayer::killGoldenAgeUnits  (CvPlayer.cpp:9580)
- CvPlayer::killUnits  (CvPlayer.cpp:3282)
- CvPlayer::receiveGoody  (CvPlayer.cpp:6344)
- CvPlayer::setTurnActive  (CvPlayer.cpp:12160)
- CvPlayer::setupGraphical  (CvPlayer.cpp:1815)
- CvPlayer::splitEmpire  (CvPlayer.cpp:22363)
- CvPlayerAI::AI_dealVal  (CvPlayerAI.cpp:8823)
- CvPlayerAI::AI_disbandUnit  (CvPlayerAI.cpp:20029)
- CvPlayerAI::AI_doAdvancedStart  (CvPlayerAI.cpp:23691)
- CvPlayerAI::AI_doPeace  (CvPlayerAI.cpp:862)
- CvPlayerAI::AI_doTurnPost  (CvPlayerAI.cpp:543)
- CvPlayerAI::AI_doTurnUnitsPost  (CvPlayerAI.cpp:625)
- CvPlayerAI::AI_espionageVal  (CvPlayerAI.cpp:14370)
- CvPlot::CvPlot  (CvPlot.cpp:44)
- CvPlot::changeAdjacentSight  (CvPlot.cpp:1698)
- CvPlot::changeStolenVisibilityCount  (CvPlot.cpp:7129)
- CvPlot::doCulture  (CvPlot.cpp:8732)
- CvPlot::erase  (CvPlot.cpp:293)
- CvPlot::getSelectedUnit  (CvPlot.cpp:2671)
- CvPlot::init  (CvPlot.cpp:108)
- CvPlot::nukeExplosion  (CvPlot.cpp:902)
- CvPlot::read  (CvPlot.cpp:8990)
- CvPlot::setBonusType  (CvPlot.cpp:5611)
- CvPlot::setFeatureType  (CvPlot.cpp:5441)
- CvPlot::setImprovementType  (CvPlot.cpp:5662)
- CvPlot::setIrrigated  (CvPlot.cpp:4627)
- CvPlot::setOwner  (CvPlot.cpp:4846)
- CvPlot::setPlotType  (CvPlot.cpp:5136)
- CvPlot::setRouteType  (CvPlot.cpp:5783)
- CvPlot::updateRiverSymbol  (CvPlot.cpp:8030)
- CvPlot::updateRouteSymbol  (CvPlot.cpp:7967)
- ... 80 more

### level 2 (232)

- CvCity::alterWorkingPlot  (CvCity.cpp:11915)
- CvCity::applyEvent  (CvCity.cpp:15152)
- CvCity::doMeltdown  (CvCity.cpp:13968)
- CvCity::doTask  (CvCity.cpp:1446)
- CvCity::emergencyConscript  (CvCity.cpp:16174)
- CvCity::initConscriptedUnit  (CvCity.cpp:4130)
- CvCity::kill  (CvCity.cpp:947)
- CvCity::liberate  (CvCity.cpp:15846)
- CvCity::popOrder  (CvCity.cpp:12842)
- CvCity::setHasCorporation  (CvCity.cpp:12397)
- CvCity::setPopulation  (CvCity.cpp:5961)
- CvCity::setWorkingPlot  (CvCity.cpp:11909)
- CvCity::updateYield  (CvCity.cpp:1407)
- CvCity::verifyWorkingPlot  (CvCity.cpp:1628)
- CvCityAI::AI_addBestCitizen  (CvCityAI.cpp:9768)
- CvCityAI::AI_assignWorkingPlots  (CvCityAI.cpp:245)
- CvCityAI::AI_juggleCitizens  (CvCityAI.cpp:10041)
- CvCityAI::AI_removeWorstCitizen  (CvCityAI.cpp:9917)
- CvCityAI::AI_updateWorkersNeededHere  (CvCityAI.cpp:13224)
- CvCityAI::CvCityAI  (CvCityAI.cpp:57)
- CvDeal::doTurn  (CvDeal.cpp:298)
- CvGame::cheatSpaceship  (CvGameInterface.cpp:2561)
- CvGame::doControl  (CvGameInterface.cpp:1613)
- CvGame::doGlobalWarming  (CvGame.cpp:6083)
- CvGame::doTurn  (CvGame.cpp:5921)
- CvGame::implementDeal  (CvGame.cpp:2623)
- CvGame::initFreeState  (CvGame.cpp:762)
- CvGame::initFreeUnits  (CvGame.cpp:822)
- CvGame::initSelection  (CvGameInterface.cpp:2763)
- CvGame::normalizeAddExtras  (CvGame.cpp:1724)
- CvGame::normalizeAddFoodBonuses  (CvGame.cpp:1509)
- CvGame::normalizeAddGoodTerrain  (CvGame.cpp:1619)
- CvGame::normalizeAddLakes  (CvGame.cpp:1274)
- CvGame::normalizeAddRiver  (CvGame.cpp:1182)
- CvGame::normalizeRemoveBadFeatures  (CvGame.cpp:1346)
- CvGame::normalizeRemovePeaks  (CvGame.cpp:1236)
- CvGame::processVote  (CvGame.cpp:7782)
- CvGame::regenerateMap  (CvGame.cpp:348)
- CvGame::removePlotExtraYield  (CvGame.cpp:9032)
- CvGame::setAIAutoPlay  (CvGame.cpp:4051)
- CvGame::setPlotExtraYield  (CvGame.cpp:8992)
- CvGame::toggleDebugMode  (CvGame.cpp:4520)
- CvGame::updateMoves  (CvGame.cpp:7223)
- CvGame::updateSelectionList  (CvGameInterface.cpp:527)
- CvGameAI::CvGameAI  (CvGameAI.cpp:13)
- CvGameAI::read  (CvGameAI.cpp:113)
- CvMap::erasePlots  (CvMap.cpp:280)
- CvMap::init  (CvMap.cpp:65)
- CvMap::read  (CvMap.cpp:1300)
- CvMap::setAllPlotTypes  (CvMap.cpp:306)
- CvMap::updateVisibility  (CvMap.cpp:374)
- CvMap::updateYield  (CvMap.cpp:516)
- CvMapGenerator::addFeatures  (CvMapGenerator.cpp:644)
- CvMapGenerator::addGoodies  (CvMapGenerator.cpp:888)
- CvMapGenerator::addLakes  (CvMapGenerator.cpp:262)
- CvMapGenerator::addNonUniqueBonusType  (CvMapGenerator.cpp:828)
- CvMapGenerator::addUniqueBonusType  (CvMapGenerator.cpp:712)
- CvMapGenerator::eraseBonuses  (CvMapGenerator.cpp:968)
- CvMapGenerator::eraseFeatures  (CvMapGenerator.cpp:957)
- CvMapGenerator::setPlotTypes  (CvMapGenerator.cpp:1078)
- ... 172 more

### files touched by the reach (functions per file)

CvUnitAI.cpp 170, CvUnit.cpp 108, CvPlayer.cpp 82, CvGame.cpp 61, CvPlot.cpp 61, CvCity.cpp 60, CvTeam.cpp 41, CvPlayerAI.cpp 37, CyPlayer.cpp 37, CvSelectionGroup.cpp 36, CyUnit.cpp 32, CyCity.cpp 26, CvCityAI.cpp 25, CyPlot.cpp 21, CvMap.cpp 20, CyTeam.cpp 20, CvMessageData.cpp 18, CvMapGenerator.cpp 18, CyMapGenerator.cpp 17, CvDLLEntity.cpp 12, CyGame.cpp 12, CvDeal.cpp 8, CvGameInterface.cpp 8, CyMap.cpp 8, CvSelectionGroupAI.cpp 7, FFreeListTrashArray.h 6, CySelectionGroup.cpp 6, CvTeamAI.cpp 4, CvGameCoreUtils.cpp 3, CvDLLButtonPopup.cpp 3, CvGameAI.cpp 3, CvDLLWidgetData.cpp 3, CvArea.cpp 2, CvDLLEntity.h 1, CyCityInterface1.cpp 1, CyUnitInterface1.cpp 1, CyGameInterface.cpp 1, CyPlayerInterface1.cpp 1, CyPlotInterface1.cpp 1, CvDLLPython.cpp 1

## Exits from the DLL among them

- called by the exe (exported): 121: CvCity::cheat  (CvCity.cpp:16117); CvCity::isInfoDirty  (CvCity.cpp:8703); CvCity::isLayoutDirty  (CvCity.cpp:8715); CvDLLButtonPopup::OnOkClicked  (CvDLLButtonPopup.cpp:75); CvDLLButtonPopup::launchButtonPopup  (CvDLLButtonPopup.cpp:855); CvDLLEntity::CvDLLEntity  (CvDLLEntity.cpp:7); CvDLLEntity::CvDLLEntity  (CvDLLEntity.h:); CvDLLEntity::ExecuteMove  (CvDLLEntity.cpp:72); CvDLLEntity::GetSiegeTower  (CvDLLEntity.cpp:92); CvDLLEntity::IsSelected  (CvDLLEntity.cpp:47); CvDLLEntity::MoveTo  (CvDLLEntity.cpp:62); CvDLLEntity::NotifyEntity  (CvDLLEntity.cpp:82); CvDLLEntity::PlayAnimation  (CvDLLEntity.cpp:52); CvDLLEntity::QueueMove  (CvDLLEntity.cpp:67); CvDLLEntity::SetPosition  (CvDLLEntity.cpp:77) ...
- bound for Python: 180: IsSelected, NotifyEntity, acquireCity, addBonuses, addFeatures, addGameElements, addGoodies, addLakes, addNonUniqueBonusType, addPlayer, addProductionExperience, addRivers, addTeam, addUniqueBonusType, alterSpecialistCount, alterWorkingPlot, assignVassal, assimilatePlayer, attackForDamage, changeBuildProgress, changeCiv, changeCombatExperience, changeCulture, changeCultureTimes100, changeDamage
- Python modules calling them: 45: AbandonCityEventManager.py, BUG/BugUnitPlot.py, BUG/DealUtil.py, BUG/Scoreboard.py, BUG/UnitPlotListUtil.py, Contrib/AStarTools.py, Contrib/EventSigns.py, Contrib/MapFinder.py, Contrib/MonkeyTools.py, Contrib/RevDCMReligionControl.py, Contrib/UnitNameEventManager.py, CvDiplomacy.py, CvMapGeneratorUtil.py, CvUtil.py, EnhancedTechConquestUtils/EnhancedTechConquest.py, EntryPoints/CvRandomEventInterface.py, ModTools/ModTools.py, ModTools/ModToolsUtils.py, PyHelpers.py, Revolution/Development/ChangePlayer.py, Revolution/Development/Tester.py, Revolution/Gameready/AIAutoPlay.py, Revolution/Gameready/BarbarianCiv.py, Revolution/Gameready/Revolution.py, Revolution/Gameready/StartAsMinors.py ...
