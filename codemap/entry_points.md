# Entry points of the DLL

How control reaches the source from outside, from `map/`.

## Offered to the game exe: exported functions (2446)

Functions declared `DllExport` (directly, or as members of a class declared `DllExport`): the DLL offers them to the exe. Which of them the exe actually calls cannot be seen from the source.

- **(global)** (14): DLLPublishToPython, XYCoords::operator<(struct XYCoords) const, XYCoords::operator<=(struct XYCoords) const, XYCoords::operator>(struct XYCoords) const, XYCoords::operator>=(struct XYCoords) const, atWar, directionAngle, estimateDirection, getCity, getUnit, isCardinalDirection, setTradeItem, shuffle
- **CombatDetails** (4): CombatDetails, operator=, ~CombatDetails
- **CvActionInfo** (36): CvActionInfo, getActionInfoIndex, getAutomateType, getButton, getCivilopedia, getCommandData, getCommandType, getControlType, getDescription, getHelp, getHotKey, getHotKeyDescription, getHotKeyPriority, getHotKeyPriorityAlt, getHotKeyVal, getHotKeyValAlt, getInterfaceModeType, getMissionData, getMissionType, getOrderPriority, getOriginalIndex, getStrategy, getSubType, getTextKeyWide, getType, isAltDown, isAltDownAlt, isConfirmCommand, isCtrlDown, isCtrlDownAlt, isShiftDown, isShiftDownAlt, isVisible, setOriginalIndex, setSubType, ~CvActionInfo
- **CvAirMissionDefinition** (6): CvAirMissionDefinition, getDamage, isDead, operator=, setDamage
- **CvAnimationCategoryInfo** (4): CvAnimationCategoryInfo, getCategoryBaseID, getCategoryDefaultTo, ~CvAnimationCategoryInfo
- **CvAnimationPathInfo** (7): CvAnimationPathInfo, getNumPathDefinitions, getPath, getPathCategory, getPathParameter, isMissionPath, ~CvAnimationPathInfo
- **CvArtFileMgr** (55): CvArtFileMgr, DeInit, GetInstance, Init, Reset, buildArtFileInfoMaps, getAssetArtInfo, getBonusArtInfo, getBuildingArtInfo, getCivilizationArtInfo, getFeatureArtInfo, getImprovementArtInfo, getInterfaceArtInfo, getLeaderheadArtInfo, getMiscArtInfo, getMovieArtInfo, getNumAssetArtInfos, getNumBonusArtInfos, getNumBuildingArtInfos, getNumCivilizationArtInfos, getNumFeatureArtInfos, getNumImprovementArtInfos, getNumInterfaceArtInfos, getNumLeaderheadArtInfos, getNumMiscArtInfos, getNumMovieArtInfos, getNumTerrainArtInfos, getNumUnitArtInfos, getTerrainArtInfo, getUnitArtInfo, ~CvArtFileMgr
- **CvArtInfoAsset** (6): CvArtInfoAsset, getKFM, getNIF, setKFM, setNIF, ~CvArtInfoAsset
- **CvArtInfoBonus** (5): CvArtInfoBonus, getFontButtonIndex, getShaderNIF, setShaderNIF, ~CvArtInfoBonus
- **CvArtInfoBuilding** (4): CvArtInfoBuilding, getLSystemName, isAnimated, ~CvArtInfoBuilding
- **CvArtInfoCivilization** (3): CvArtInfoCivilization, isWhiteFlag, ~CvArtInfoCivilization
- **CvArtInfoFeature** (9): CvArtInfoFeature, getFeatureDummyNodeName, getLightType, getNumVarieties, getTileArtType, getVariety, isAnimated, isRiverArt, ~CvArtInfoFeature
- **CvArtInfoImprovement** (5): CvArtInfoImprovement, getShaderNIF, isExtraAnimations, setShaderNIF, ~CvArtInfoImprovement
- **CvArtInfoInterface** (2): CvArtInfoInterface, ~CvArtInfoInterface
- **CvArtInfoLeaderhead** (6): CvArtInfoLeaderhead, getBackgroundKFM, getNoShaderNIF, setBackgroundKFM, setNoShaderNIF, ~CvArtInfoLeaderhead
- **CvArtInfoMisc** (2): CvArtInfoMisc, ~CvArtInfoMisc
- **CvArtInfoMovie** (2): CvArtInfoMovie, ~CvArtInfoMovie
- **CvArtInfoTerrain** (11): CvArtInfoTerrain, getBaseTexture, getBlendList, getDetailTexture, getGridTexture, getLayerOrder, setBaseTexture, setDetailTexture, setGridTexture, useAlphaShader, ~CvArtInfoTerrain
- **CvArtInfoUnit** (31): CvArtInfoUnit, getActAsAir, getActAsLand, getActAsRanged, getActionSoundScriptId, getAngleInterpRate, getBankRate, getBattleDistance, getCombatExempt, getDamageStates, getExchangeAngle, getPatrolSoundTag, getRangedDeathTime, getRunEndSoundTag, getRunLoopSoundTag, getSelectionSoundScriptId, getShaderNIF, getShadowAttachNode, getShadowNIF, getShadowScale, getSmoothMove, getTrailFadeFalloff, getTrailFadeStarTime, getTrailLength, getTrailTaper, getTrailTexture, getTrailWidth, getTrainSound, setShaderNIF, setTrainSound, ~CvArtInfoUnit
- **CvAssetInfoBase** (6): CvAssetInfoBase, getPath, getTag, setPath, setTag, ~CvAssetInfoBase
- **CvAttachableInfo** (4): CvAttachableInfo, getPath, setPath, ~CvAttachableInfo
- **CvAutomateInfo** (8): CvAutomateInfo, getAutomate, getCommand, getConfirmCommand, getVisible, setAutomate, setCommand, ~CvAutomateInfo
- **CvBattleDefinition** (26): CvBattleDefinition, addBattleRound, addDamage, addFirstStrikes, addNumMeleeRounds, addNumRangedRounds, checkBattleRound, checkBattleTimeType, clearBattleRounds, getBattleRound, getDamage, getFirstStrikes, getNumBattleRounds, getNumMeleeRounds, getNumRangedRounds, isAdvanceSquare, operator=, setAdvanceSquare, setBattleRound, setDamage, setFirstStrikes, setNumMeleeRounds, setNumRangedRounds, ~CvBattleDefinition
- **CvBattleRound** (12): CvBattleRound, addNumKilled, getNumAlive, getNumKilled, getWaveSize, isRangedRound, isValid, operator=, setNumAlive, setNumKilled, setRangedRound, setWaveSize
- **CvBonusInfo** (1): getArtInfo
- **CvBuildInfo** (2): getEntityEvent, getMissionType
- **CvCameraInfo** (4): CvCameraInfo, getPath, setPath, ~CvCameraInfo
- **CvCameraOverlayInfo** (7): CvCameraOverlayInfo, getBaseTexture, getCameraOverlayType, isVisible, read, setBaseTexture, ~CvCameraOverlayInfo
- **CvCity** (39): canBeSelected, cheat, getArtStyleType, getBarBackgroundColor, getBuildQueue, getBuildingArtInfo, getBuildingVisibilityPriority, getCityBillboardProductionIcon, getCityBillboardSizeIconColors, getCitySizeType, getFoodBarPercentages, getID, getIDInfo, getIndex, getMusicScriptId, getName, getNameKey, getNumOrdersQueued, getOrderData, getOwner, getProductionBarPercentages, getSoundscapeScriptId, getTeam, getVisibleBuildings, getVisibleEffects, getWallOverridePoints, getX, getY, isInfoDirty, isLayoutDirty, isRevealed, isStarCity, isVisible, isWallOverride, plot, setInfoDirty, setLayoutDirty, setWallOverridePoints, updateSelectedCity
- **CvCivilizationInfo** (34): CvCivilizationInfo, getActionSoundScriptId, getAdjective, getAdjectiveKey, getArtDefineTag, getArtInfo, getArtStyleType, getButton, getCityNames, getCivilizationBuildings, getCivilizationFreeUnitsClass, getCivilizationInitialCivics, getCivilizationUnits, getDefaultPlayerColor, getDerivativeCiv, getFlagTexture, getNumCityNames, getNumLeaders, getSelectionSoundScriptId, getShortDescription, getShortDescriptionKey, getUnitArtStyleType, isAIPlayable, isCivilizationDisableTechs, isCivilizationFreeBuildingClass, isCivilizationFreeTechs, isLeaders, isPlayable, read, readPass2, reset, setArtDefineTag, write, ~CvCivilizationInfo
- **CvColorInfo** (3): CvColorInfo, getColor, ~CvColorInfo
- **CvCommandInfo** (7): CvCommandInfo, getAll, getAutomate, getConfirmCommand, getVisible, setAutomate, ~CvCommandInfo
- **CvControlInfo** (2): CvControlInfo, ~CvControlInfo
- **CvCursorInfo** (1): getPath
- **CvDLLButtonPopup** (6): OnAltExecute, OnFocus, OnOkClicked, freeInstance, getInstance, launchButtonPopup
- **CvDLLEntity** (27): CvDLLEntity, ExecuteMove, GetSiegeTower, IsSelected, MoveTo, NotifyEntity, PlayAnimation, QueueMove, SetPosition, SetSiegeTower, StopAnimation, createCityEntity, createUnitEntity, destroyEntity, getCityEntity, getEntity, getUnitEntity, operator=, removeEntity, setEntity, setVisible, setup, ~CvDLLEntity
- **CvDLLWidgetData** (6): executeAction, executeAltAction, freeInstance, getInstance, isLink, parseHelp
- **CvDeal** (20): getFirstPlayer, getGoldItem, getGoldPerTurnItem, getID, getPeaceItem, getSecondPlayer, hasData, headFirstTradesNode, headSecondTradesNode, isAnnual, isCancelable, isDual, isEndWar, isGold, isVassal, isVassalTributeDeal, kill, nextFirstTradesNode, nextSecondTradesNode, turnsToCancel
- **CvDiploParameters** (37): CvDiploParameters, getAIContact, getChatText, getData, getDiploComment, getDiploCommentArgs, getHumanDiplo, getOurOfferList, getOurOffering, getPendingDelete, getRenegotiate, getTheirOfferList, getTheirOffering, getWhoTalkingTo, read, setAIContact, setChatText, setData, setDiploComment, setHumanDiplo, setOurOfferList, setOurOffering, setPendingDelete, setRenegotiate, setTheirOfferList, setTheirOffering, setWhoTalkingTo, write, ~CvDiploParameters
- **CvDiplomacyInfo** (13): CvDiplomacyInfo, getAttitudeTypes, getCivilizationTypes, getDiplomacyPowerTypes, getDiplomacyText, getLeaderHeadTypes, getNumDiplomacyText, getNumResponses, getResponse, read, uninit, write, ~CvDiplomacyInfo
- **CvDiplomacyResponse** (21): CvDiplomacyResponse, getAttitudeTypes, getCivilizationTypes, getDiplomacyPowerTypes, getDiplomacyText, getLeaderHeadTypes, getNumDiplomacyText, read, setAttitudeTypes, setCivilizationTypes, setDiplomacyPowerTypes, setDiplomacyText, setLeaderHeadTypes, setNumDiplomacyText, write, ~CvDiplomacyResponse
- **CvDiplomacyTextInfo** (12): CvDiplomacyTextInfo, getAttitudeTypes, getCivilizationTypes, getDiplomacyPowerTypes, getDiplomacyText, getLeaderHeadTypes, getNumDiplomacyText, getNumResponses, getResponse, init, uninit, ~CvDiplomacyTextInfo
- **CvDiplomacyTextInfo::Response** (2): Response, ~Response
- **CvDllTranslator** (3): initializeTags, replaceCt, replaceOur
- **CvEffectInfo** (10): CvEffectInfo, getPath, getProjectileArc, getProjectileSpeed, getUpdateRate, isProjectile, isSticky, setPath, setUpdateRate, ~CvEffectInfo
- **CvEntityEventInfo** (7): CvEntityEventInfo, getAnimationPathCount, getAnimationPathType, getEffectType, getEffectTypeCount, getUpdateFormation, ~CvEntityEventInfo
- **CvEventReporter** (21): chat, gameStart, getGameStatistics, getInstance, getPlayerStatistics, gotoPlotSet, init, kbdEvent, mouseEvent, newGame, newPlayer, plotPicked, preSave, readStatistics, reportModNetMessage, resetStatistics, unInit, unitSelected, update, windowActivation, writeStatistics
- **CvFeatureInfo** (1): getArtInfo
- **CvFlyoutMenuData** (4): CvFlyoutMenuData, operator=, ~CvFlyoutMenuData
- **CvForceControlInfo** (3): CvForceControlInfo, getDefault, ~CvForceControlInfo
- **CvFractal** (8): CvFractal, fracInit, fracInitHinted, getHeight, getHeightFromPercent, reset, uninit, ~CvFractal
- **CvGame** (170): CvGame, addDeal, applyFlyoutMenu, assignStartingPlots, calculateOptionsChecksum, calculateSyncChecksum, canDoPing, canHandleAction, canRegenerateMap, castVote, cheatSpaceship, cityPushOrder, countCivPlayersAlive, countCivPlayersEverAlive, countCivTeamsAlive, countCivTeamsEverAlive, countHumanPlayersAlive, countNumHumanGameTurnActive, cycleCities, cyclePlotUnits, cycleSelectionGroups, deleteDeal, firstDeal, getActiveCivilizationType, getActivePlayer, getActiveTeam, getBuildingArtInfo, getCalendar, getCurrentEra, getDeal, getEndTurnState, getGameSpeedType, getGameState, getGameTurn, getGlobeLayers, getGlobeviewConfigurationParameters, getHandicapType, getHotPbemBetweenTurns, getIndexAfterLastDeal, getInitialTime, getMaxCityElimination, getMaxTurnLen, getName, getNewHighlightPlot, getNextSoundtrack, getNumAdvancedStartPoints, getNumCities, getNumDeals, getNumHumanPlayers, getPausePlayer, getPitbossTurnTime, getPlayerScore, getPlotHighlightColor, getPlotUnit, getPlotUnits, getSoundtrackSpace, getSpaceVictory, getStartEra, getStartTurn, getSymbolID, getTeamScore, getTotalPopulation, getTurnSlice, getTurnSlicesRemaining, getUnitDomain, getVictory, getWidgetShow, getWinner, handleAction, handleCityPlotRightPicked, handleCityScreenPlotDoublePicked, handleCityScreenPlotPicked, handleCityScreenPlotRightPicked, handleDiplomacySetAIComment, handleMiddleMouse, implementDeal, init, initDiplomacy, initEvents, initFreeState, initFreeUnits, initScoreCalculation, initSelection, isDebugMode, isFinalInitialized, isForcedControl, isGameMultiPlayer, isHotSeat, isMPOption, isNetworkMultiPlayer, isOption, isPaused, isPbem, isPitboss, isPlayerOptionsSent, isSimultaneousTeamTurns, isSoundtrackOverride, isTeamGame, isWaterBuilding, loadBuildQueue, nextActivePlayer, nextDeal, normalizeStartingPlots, read, regenerateMap, reset, reviveActivePlayer, revivePlayer, selectAll, selectCity, selectGroup, selectUnit, selectedCitiesGameNetMessage, selectionListGameNetMessage, selectionListIgnoreBuildingDefense, selectionListMove, sendPlayerOptions, setAIAutoPlay, setActivePlayer, setFinalInitialized, setForceControl, setGameState, setGameTurn, setHandicapType, setHotPbemBetweenTurns, setInitialItems, setInitialTime, setMPOption, setMaxCityElimination, setMaxTurns, setName, setNumAdvancedStartPoints, setOption, setPausePlayer, setPbemTurnSent, setPitbossTurnTime, setReplayInfo, setStartTurn, setTargetScore, setVoteChosen, setupActionCache, shouldCenterMinimap, shouldDisplayEndTurn, shouldDisplayEndTurnButton, shouldDisplayFlag, shouldDisplayReturn, shouldDisplayUnitModel, shouldDisplayWaitingOthers, shouldDisplayWaitingYou, shouldShowResearchButtons, startFlyoutMenu, takeJPEGScreenShot, testExtendedGame, toggleDebugMode, update, updateBlockadedPlots, updateBuildingCommerce, updateCitySight, updateColoredPlots, updateDebugModeCache, updatePlotGroups, updateScore, updateSelectionList, updateTestEndTurn, updateTradeRoutes, updateUnitEnemyGlow, write, writeReplay, ~CvGame
- **CvGameOptionInfo** (4): CvGameOptionInfo, getDefault, getVisible, ~CvGameOptionInfo
- **CvGameText** (3): CvGameText, getNumLanguages, setNumLanguages
- **CvGameTextMgr** (152): CvGameTextMgr, DeInitialize, GetInstance, Initialize, Reset, assignFontIds, buildAdjustString, buildBonusRevealString, buildBridgeString, buildBuildingRequiresString, buildCityBillboardCityNameString, buildCityBillboardCitySizeString, buildCityBillboardIconString, buildCityBillboardProductionString, buildCivicRevealString, buildDefensivePactString, buildDomainExtraMovesString, buildFeatureProductionString, buildFinanceAwaySupplyString, buildFinanceCityMaintString, buildFinanceCivicUpkeepString, buildFinanceForeignIncomeString, buildFinanceInflationString, buildFinanceUnitCostString, buildFoundCorporationString, buildFoundReligionString, buildFreeTechString, buildFreeUnitString, buildGoldTradeString, buildHappinessRateString, buildHealthRateString, buildHintsList, buildIgnoreIrrigationString, buildImprovementString, buildIrrigationString, buildLOSString, buildMapCenterString, buildMapRevealString, buildMapTradeString, buildMoveString, buildObsoleteBonusString, buildObsoleteSpecialString, buildObsoleteString, buildOpenBordersString, buildPermanentAllianceString, buildProcessInfoString, buildPromotionString, buildRiverTradeString, buildSingleLineTechTreeString, buildSpecialBuildingString, buildTechTradeString, buildTechTreeString, buildTerrainTradeString, buildTradeRouteString, buildVassalStateString, buildWaterWorkString, buildWorkerRateString, buildYieldChangeString, getActiveDealsString, getAttitudeString, getBonusDataForWB, getBuildingDataForWB, getCityBillboardFoodbarColors, getCityBillboardProductionbarColors, getCityDataForAS, getCorporationDataForWB, getCurrentLanguage, getDealString, getEspionageString, getFontSymbols, getGlobeLayerName, getImprovementDataForAS, getImprovementDataForWB, getInterfaceCenterText, getPlotHelp, getPromotionDataForWB, getReligionDataForWB, getTechDataForAS, getTechDataForWB, getTerrainDataForWB, getTerritoryDataForWB, getTradeScreenHeader, getTradeScreenIcons, getTradeScreenTitleIcon, getTradeString, getTurnTimerText, getUnitDataForAS, getUnitDataForWB, getVisibilityDataForAS, parseCivInfos, parseCivicInfo, parseFreeSpecialistHelp, parseGreatGeneralHelp, parseGreatPeopleHelp, parseLeaderHeadHelp, parseLeaderLineHelp, parseLeaderShortTraits, parseLeaderTraits, parsePlayerTraits, parsePromotionHelp, parseSpecialistHelp, parseTraits, setAngerHelp, setBadHealthHelp, setBasicUnitHelp, setBonusHelp, setBonusTradeHelp, setBuildingHelp, setCityBarHelp, setCombatPlotHelp, setCommerceChangeHelp, setCommerceHelp, setConvertHelp, setCorporationHelp, setCorporationHelpCity, setDateStr, setEspionageCostHelp, setEspionageMissionHelp, setEventHelp, setFeatureHelp, setGoldStr, setGoodHealthHelp, setHappyHelp, setImprovementHelp, setInterfaceTime, setMinimizePopupHelp, setNetStats, setOOSSeeds, setPlotHelp, setPlotListHelp, setProcessHelp, setProductionHelp, setProjectHelp, setPromotionHelp, setReligionHelp, setReligionHelpCity, setResearchStr, setRevolutionHelp, setScoreHelp, setTechHelp, setTechTradeHelp, setTerrainHelp, setTimeStr, setTradeRouteHelp, setUnitCombatHelp, setUnitHelp, setVassalRevoltHelp, setYearStr, setYieldChangeHelp, setYieldHelp, ~CvGameTextMgr
- **CvGlobals** (289): CvGlobals, IsGraphicsInitialized, SetGraphicsInitialized, addToInfosVectors, cacheGlobals, clearTypesMap, enableDLLProfiler, getAIR_BOMB_HEIGHT, getASyncRand, getActionInfo, getActiveLandscapeID, getAnimationCategoryInfo, getAnimationOperatorTypes, getAnimationPathInfo, getAreaFinder, getArtStyleTypes, getAttachableInfo, getAutomateInfo, getBARBARIAN_PLAYER, getBARBARIAN_TEAM, getBonusInfo, getBorderFinder, getBuildInfo, getCAMERA_FAR_CLIP_Z_HEIGHT, getCAMERA_LOWER_PITCH, getCAMERA_MAX_TRAVEL_DISTANCE, getCAMERA_MAX_TURN_OFFSET, getCAMERA_MAX_YAW, getCAMERA_MIN_DISTANCE, getCAMERA_MIN_YAW, getCAMERA_SPECIAL_PITCH, getCAMERA_START_DISTANCE, getCAMERA_UPPER_PITCH, getCITY_HOME_PLOT, getCameraInfo, getCameraOverlayInfo, getCityPlotPriority, getCityPlotX, getCityPlotY, getCivilizationInfo, getClimateInfo, getColorInfo, getCommandInfo, getControlInfo, getCursorInfo, getDLLIFaceNonInl, getDefineBOOL, getDefineFLOAT, getDefineINT, getDefineSTRING, getDefinesVarSystem, getDiplomacyScreen, getDirectionTypes, getDropMgr, getEVENT_MESSAGE_TIME, getEffectInfo, getEntityEventInfo, getEntityEventTypes, getEraInfo, getFIELD_OF_VIEW, getFMPMgrPtr, getFeatureInfo, getFootstepAudioTags, getFootstepAudioTypeByTag, getFootstepAudioTypes, getForceControlInfo, getFunctionTypes, getGame, getGameOptionInfo, getGamePointer, getGameSpeedInfo, getGoodyInfo, getGraphicOptionInfo, getHandicapInfo, getHints, getHotMessageQueue, getINVALID_PLOT_COORD, getImprovementInfo, getInfoTypeForString, getIniInitCore, getInitCore, getInstance, getInterface, getInterfaceModeInfo, getInterfacePathFinder, getInterfacePtr, getLandscapeInfo, getLeaderHeadInfo, getLoadedInitCore, getLogging, getMAX_CIV_PLAYERS, getMAX_CIV_TEAMS, getMAX_PLAYERS, getMAX_PLOT_LIST_ROWS, getMAX_TEAMS, getMPDiplomacyScreen, getMPOptionInfo, getMainMenus, getMap, getMaxCivPlayers, getMaxNumSymbols, getMessageCodes, getMessageControl, getMessageQueue, getMissionInfo, getModLoadControlInfos, getNUM_CITY_PLOTS, getNUM_COMMERCE_TYPES, getNUM_CONTROL_TYPES, getNUM_ENGINE_DIRTY_BITS, getNUM_FORCECONTROL_TYPES, getNUM_HEALTHBAR_TYPES, getNUM_INFOBAR_TYPES, getNUM_INTERFACE_DIRTY_BITS, getNUM_LEADERANIM_TYPES, getNUM_YIELD_TYPES, getNumAIPlayableCivilizationInfos, getNumActionInfos, getNumAnimationCategoryInfos, getNumAnimationOperatorTypes, getNumAnimationPathInfos, getNumArtStyleTypes, getNumAttachableInfos, getNumAutomateInfos, getNumBasicItems, getNumBonusInfos, getNumBuildInfos, getNumCameraInfos, getNumCameraOverlayInfos, getNumCivilizationInfos, getNumClimateInfos, getNumColorInfos, getNumCommandInfos, getNumControlInfos, getNumCursorInfos, getNumDirections, getNumEffectInfos, getNumEntityEventInfos, getNumEntityEventTypes, getNumEraInfos, getNumFeatureInfos, getNumFootstepAudioTypes, getNumForceControlInfos, getNumGameOptionInfos, getNumGameOptions, getNumGameSpeedInfos, getNumGlobeLayers, getNumGoodyInfos, getNumGraphicLevels, getNumGraphicOptions, getNumHandicapInfos, getNumHints, getNumImprovementInfos, getNumLandscapeInfos, getNumLeaderHeadInfos, getNumMPOptionInfos, getNumMPOptions, getNumMainMenus, getNumMissionInfos, getNumPlayableCivilizationInfos, getNumPlayerColorInfos, getNumPlayerOptionInfos, getNumPythonModulesInfos, getNumRiverInfos, getNumRiverModelInfos, getNumRouteInfos, getNumRouteModelInfos, getNumSeaLevelInfos, getNumSlideShowInfos, getNumSlideShowRandomInfos, getNumSpaceShipInfos, getNumSpecialOptions, getNumTerrainInfos, getNumTerrainPlaneInfos, getNumThroneRoomCameras, getNumThroneRoomInfos, getNumThroneRoomStyleInfos, getNumTradeableHeadings, getNumTradeableItems, getNumTurnTimerInfos, getNumUnitFormationInfos, getNumVictoryInfos, getNumWaterPlaneInfos, getNumWorldInfos, getNumWorldPickerInfos, getPLOT_SIZE, getPathFinder, getPlayerColorInfo, getPlayerOptionInfo, getPlotCardinalDirectionX, getPlotCardinalDirectionY, getPlotDirectionX, getPlotDirectionY, getPlotGroupFinder, getPortal, getPt3CameraDir, getPt3Origin, getPythonModulesInfo, getRandLogging, getRiverInfo, getRiverModelInfo, getRouteFinder, getRouteInfo, getRouteModelInfo, getSHADOW_SCALE, getSeaLevelInfo, getSetupData, getSlideShowInfo, getSlideShowRandomInfo, getSpaceShipInfo, getStatsReporter, getStatsReporterPtr, getStepFinder, getSynchLogging, getTerrainInfo, getTerrainPlaneInfo, getThroneRoomCamera, getThroneRoomInfo, getThroneRoomStyleInfo, getTurnTimerInfo, getTypesEnum, getUNIT_MULTISELECT_DISTANCE, getUNIT_MULTISELECT_MAX, getUSE_FINISH_TEXT_CALLBACK, getUnitFormationInfo, getVictoryInfo, getWaterPlaneInfo, getWorldInfo, getWorldPickerInfo, getXYCityPlot, getXYDirection, infoTypeFromStringReset, infosReset, init, overwriteLogs, readBonusInfoArray, readBuildingInfoArray, readCivicInfoArray, readCivilizationInfoArray, readDiplomacyInfoArray, readEventInfoArray, readEventTriggerInfoArray, readHandicapInfoArray, readImprovementInfoArray, readLeaderHeadInfoArray, readPromotionInfoArray, readTechInfoArray, readUnitInfoArray, setActiveLandscapeID, setAreaFinder, setBorderFinder, setDLLIFace, setDLLProfiler, setDefineFLOAT, setDefineINT, setDefineSTRING, setDiplomacyScreen, setDropMgr, setHotJoinMessageQueue, setInterface, setInterfacePathFinder, setMPDiplomacyScreen, setMessageCodeTranslator, setMessageControl, setMessageQueue, setPathFinder, setPlotGroupFinder, setPortal, setRouteFinder, setSetupData, setStatsReport, setStepFinder, setTypesEnum, uninit, writeBonusInfoArray, writeBuildingInfoArray, writeCivicInfoArray, writeCivilizationInfoArray, writeDiplomacyInfoArray, writeEventInfoArray, writeEventTriggerInfoArray, writeHandicapInfoArray, writeImprovementInfoArray, writeLeaderHeadInfoArray, writePromotionInfoArray, writeTechInfoArray, writeUnitInfoArray, ~CvGlobals
- **CvGlobeLayerData** (4): CvGlobeLayerData, operator=, ~CvGlobeLayerData
- **CvGraphicOptionInfo** (3): CvGraphicOptionInfo, getDefault, ~CvGraphicOptionInfo
- **CvHotkeyInfo** (32): CvHotkeyInfo, getActionInfoIndex, getHotKey, getHotKeyDescription, getHotKeyPriority, getHotKeyPriorityAlt, getHotKeyVal, getHotKeyValAlt, getOrderPriority, isAltDown, isAltDownAlt, isCtrlDown, isCtrlDownAlt, isShiftDown, isShiftDownAlt, read, setActionInfoIndex, setAltDown, setAltDownAlt, setCtrlDown, setCtrlDownAlt, setHotKey, setHotKeyDescription, setHotKeyPriority, setHotKeyPriorityAlt, setHotKeyVal, setHotKeyValAlt, setOrderPriority, setShiftDown, setShiftDownAlt, write, ~CvHotkeyInfo
- **CvImprovementInfo** (3): getArtInfo, isGoody, isRequiresRiverSide
- **CvInfoBase** (8): CvInfoBase, getDescription, getHelp, getText, getTextKeyWide, getType, isGraphicalOnly, ~CvInfoBase
- **CvInitCore** (161): CvInitCore, closeInactiveSlots, getActivePlayer, getAdminPassword, getArtStyle, getAvailableSlot, getCalendar, getCalendarKey, getCiv, getCivAdjective, getCivAdjectiveKey, getCivDescription, getCivDescriptionKey, getCivPassword, getCivShortDesc, getCivShortDescKey, getClimate, getClimateKey, getColor, getCustomMapOption, getCustomMapOptions, getEmail, getEra, getEraKey, getFlagDecal, getForceControl, getForceControls, getGameMultiplayer, getGameName, getGamePassword, getGameSpeed, getGameSpeedKey, getGameTurn, getHandicap, getHotseat, getHuman, getLeader, getLeaderName, getLeaderNameKey, getMPOption, getMPOptions, getMapRandSeed, getMapScriptName, getMaxCityElimination, getMaxTurns, getMinorNationCiv, getMode, getMultiplayer, getNetID, getNewGame, getNumAdvancedStartPoints, getNumCustomMapOptions, getNumDefinedPlayers, getNumHiddenCustomMapOptions, getNumHumans, getNumVictories, getOption, getOptions, getPbem, getPitboss, getPitbossTurnTime, getPlayableCiv, getPythonCheck, getReady, getSavedGame, getSeaLevel, getSeaLevelKey, getSlotClaim, getSlotStatus, getSlotVacant, getSmtpHost, getStatReporting, getSyncRandSeed, getTargetScore, getTeam, getTurnTimer, getTurnTimerKey, getType, getVictories, getVictory, getWBMapNoPlayers, getWBMapScript, getWhiteFlag, getWorldSize, getWorldSizeKey, getXMLCheck, init, read, reassignPlayer, reopenInactiveSlots, resetAdvancedStartPoints, resetGame, resetPlayer, resetPlayers, setActivePlayer, setAdminPassword, setArtStyle, setCalendar, setCiv, setCivAdjective, setCivDescription, setCivPassword, setCivShortDesc, setClimate, setColor, setCustomMapOption, setCustomMapOptions, setEmail, setEra, setFlagDecal, setForceControl, setGameName, setGamePassword, setGameSpeed, setGameTurn, setHandicap, setLeader, setLeaderName, setMPOption, setMapRandSeed, setMapScriptName, setMaxCityElimination, setMaxTurns, setMinorNationCiv, setMode, setNetID, setNumAdvancedStartPoints, setOption, setPitbossTurnTime, setPlayableCiv, setPythonCheck, setReady, setSeaLevel, setSlotClaim, setSlotStatus, setSmtpHost, setStatReporting, setSyncRandSeed, setTargetScore, setTeam, setTurnTimer, setType, setVictories, setVictory, setWBMapNoPlayers, setWhiteFlag, setWorldSize, setXMLCheck, write, ~CvInitCore
- **CvInterfaceModeInfo** (9): CvInterfaceModeInfo, getCursorIndex, getGotoPlot, getHighlightPlot, getMissionType, getSelectAll, getSelectType, getVisible, ~CvInterfaceModeInfo
- **CvLandscapeInfo** (30): CvLandscapeInfo, getBlendMap, getFogB, getFogG, getFogR, getHeightMap, getHillScale, getHorizontalGameCell, getHorizontalVertCnt, getNormalMap, getPeakScale, getPlotsPerCellX, getPlotsPerCellY, getSkyArt, getTerrainMap, getTextureScaleX, getTextureScaleY, getVerticalGameCell, getVerticalVertCnt, getWaterHeight, getZScale, isRandomMap, isUseLightmap, isUseTerrainShader, setBlendMap, setHeightMap, setNormalMap, setSkyArt, setTerrainMap, ~CvLandscapeInfo
- **CvLeaderHeadInfo** (1): getArtInfo
- **CvMPOptionInfo** (3): CvMPOptionInfo, getDefault, ~CvMPOptionInfo
- **CvMainMenuInfo** (7): CvMainMenuInfo, getLoading, getLoadingSlideshow, getScene, getSceneNoShader, getSoundtrack, ~CvMainMenuInfo
- **CvMap** (40): CvMap, erasePlots, findCity, findSelectionGroup, getClimate, getCustomMapOption, getGridHeight, getGridWidth, getLandPlots, getNumAreas, getNumCustomMapOptions, getNumLandAreas, getOwnedPlots, getSeaLevel, getWorldSize, init, isPlot, isWrap, isWrapX, isWrapY, numPlots, plot, plotByIndex, plotNum, plotXToPointX, plotYToPointY, pointToPlot, pointXToPlotX, pointYToPlotY, read, reset, setupGraphical, updateCenterUnit, updateFlagSymbols, updateFog, updateMinimapColor, updateSymbolVisibility, updateVisibility, write, ~CvMap
- **CvMapGenerator** (14): CvMapGenerator, FreeInstance, GetInstance, addBonuses, addFeatures, addGameElements, addGoodies, addRivers, eraseBonuses, eraseFeatures, eraseGoodies, eraseRivers, generateRandomMap, ~CvMapGenerator
- **CvMessageControl** (7): getInstance, sendAdvancedStartAction, sendChangeWar, sendDoTask, sendJoinGroup, sendLaunch, sendPing
- **CvMessageData** (2): createMessage, getType
- **CvMissionDefinition** (10): CvMissionDefinition, getMissionTime, getMissionType, getPlot, getUnit, operator=, setMissionTime, setMissionType, setPlot, setUnit
- **CvMissionInfo** (9): CvMissionInfo, getEntityEvent, getTime, getVisible, getWaypoint, isBuild, isSound, isTarget, ~CvMissionInfo
- **CvNetAdvancedStartAction** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetAutoMission** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetAutoMoves** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetChangeVassal** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetChangeWar** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetChooseElection** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetConvert** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetDiploVote** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetDoCommand** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetDoTask** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetEmpireSplit** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetEspionageChange** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetEventTriggered** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetExtendedGame** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetFoundReligion** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetJoinGroup** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetLaunchSpaceship** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetModNetMessage** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetPercentChange** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetPing** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetPopOrder** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetPushMission** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetPushOrder** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetResearch** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetTurnComplete** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvNetUpdateCivics** (4): Debug, Execute, PutInBuffer, SetFromBuffer
- **CvPlayer** (172): addDiplomacy, addMessage, addPopup, applyEvent, buildTradeTable, canContact, canConvert, canDoEspionageMission, canEverResearch, canFound, canHurry, canRaze, canResearch, canRevolution, canTradeItem, canTrain, changeAdvancedStartPoints, changeCommercePercent, changeEspionageSpendingWeightAgainstTeam, changeGold, cheat, chooseTech, clearResearchQueue, clearSpaceShipPopups, convert, countNumCitiesConnectedToCapital, doAdvancedStartAction, expireMessages, firstCity, firstSelectionGroup, firstUnit, foundReligion, getAdvancedStartBuildingCost, getAdvancedStartCityCost, getAdvancedStartCultureCost, getAdvancedStartImprovementCost, getAdvancedStartPoints, getAdvancedStartPopCost, getAdvancedStartRouteCost, getAdvancedStartTechCost, getAdvancedStartUnitCost, getAdvancedStartVisibilityCost, getArtStyleType, getAssets, getBestAttackUnitName, getBuildingClassPrereqBuilding, getCapitalCity, getCity, getCivicAnarchyLength, getCivics, getCivilizationAdjective, getCivilizationAdjectiveKey, getCivilizationDescription, getCivilizationDescriptionKey, getCivilizationShortDescription, getCivilizationShortDescriptionKey, getCivilizationType, getCurrentEra, getCurrentResearch, getDiplomacy, getExtraHealth, getFlagDecal, getGameMessages, getGlobeLayerColors, getGold, getGoldenAgeTurns, getHandicapType, getHeadingTradeString, getID, getIntroMusicScriptId, getItemTradeString, getLandScore, getLeaderType, getMaxConscript, getMusicScriptId, getName, getNameKey, getNetID, getNumCities, getNumGovernmentCenters, getNumTradeableBonuses, getNumUnits, getOverflowResearch, getPbemEmailAddress, getPlayerColor, getPlayerTextColorA, getPlayerTextColorB, getPlayerTextColorG, getPlayerTextColorR, getPopScore, getPopups, getPower, getProductionNeeded, getReligionAnarchyLength, getResearchTurnsLeft, getRevolutionTimer, getSmtpHost, getStartingPlot, getStateReligion, getStateReligionHappiness, getStateReligionKey, getStateReligionName, getTeam, getTechScore, getTotalPopulation, getTotalTimePlayed, getTradeDenial, getUnit, getUnitArtInfo, getUnitButton, getWondersScore, getWorstEnemyName, greatPeopleThreshold, handleDiploEvent, hasAutoUnit, hasBusyUnit, hasReadyUnit, hasSpaceshipArrived, init, isAlive, isAnarchy, isBarbarian, isConnected, isEverAlive, isGoldenAge, isHuman, isLoyalMember, isNoNonStateReligionSpread, isOption, isPbemNewTurn, isPlayable, isResearchingTech, isSpecialistValid, isStrike, isTurnActive, isTurnDone, isWhiteFlag, launch, makeExtendedGame, nextCity, nextSelectionGroup, nextUnit, popFrontDiplomacy, popFrontPopup, pushResearch, reset, revolution, sendReminder, setAdvancedStartPoints, setAutoMoves, setEndTurn, setGold, setLoyalMember, setNetID, setOption, setPbemEmailAddress, setPbemNewTurn, setPlayable, setSmtpHost, setStartTime, setStartingPlot, setTurnActive, setTurnActiveForPbem, setupGraphical, showSpaceShip, splitEmpire, unitsGoldenAgeReady, unitsRequiredForGoldenAge, updateHuman, updateTradeList
- **CvPlayerAI** (5): AI_getGreeting, AI_maxGoldPerTurnTrade, AI_maxGoldTrade, areStaticsInitialized, getPlayerNonInl
- **CvPlayerColorInfo** (5): CvPlayerColorInfo, getColorTypePrimary, getColorTypeSecondary, getTextColorType, ~CvPlayerColorInfo
- **CvPlayerOptionInfo** (3): CvPlayerOptionInfo, getDefault, ~CvPlayerOptionInfo
- **CvPlayerRecord** (12): getLeader, getMinutesPlayed, getNumBuildingsBuilt, getNumCitiesBuilt, getNumCitiesRazed, getNumGoldenAges, getNumUnitsBuilt, getNumUnitsKilled, getNumUnitsWasKilled, getPlayerID, getReligionFounded, getVictory
- **CvPlot** (82): addFeatureDummyModel, checkLateEra, erase, get3DAudioScriptFootstepIndex, getAqueductSourceWeight, getAreaIdForGreatWall, getBestDefender, getBonusType, getCenterUnit, getDebugCenterUnit, getFeatureType, getFeatureVariety, getFlagSymbol, getFlagSymbolOffset, getImprovementType, getNumSymbols, getNumUnits, getNumVisibleUnits, getOwner, getPlotBuilder, getPlotCity, getPoint, getPointX, getPointY, getRevealedImprovementType, getRevealedOwner, getRevealedRouteType, getRevealedTeam, getRiverNSDirection, getRiverSymbol, getRiverWEDirection, getRouteSymbol, getRouteType, getSoundScriptId, getSymbolOffsetX, getSymbolOffsetY, getTerrainType, getUnitByIndex, getVisibleBonusState, getVisibleImprovementState, getX, getY, getYield, headUnitNode, isActiveVisible, isCity, isFighting, isGoody, isHills, isIrrigationAvailable, isLake, isLayoutDirty, isLayoutStateDifferent, isNOfRiver, isPeak, isRevealed, isRiverCrossing, isRiverCrossingFlowClockwise, isRiverMask, isRoute, isVisible, isVisibleEnemyUnit, isWOfRiver, isWater, nextUnitNode, pickFeatureDummyTag, prevUnitNode, resetFeatureModel, setFeatureDummyTexture, setFeatureDummyVisibility, setFeatureType, setImprovementType, setLayoutDirty, setLayoutStateToCurrent, setNOfRiver, setRevealed, setRouteType, setWOfRiver, shouldDisplayBridge, shouldUsePlotBuilder, tailUnitNode, updateFlagSymbol
- **CvPlotIndicatorData** (4): CvPlotIndicatorData, operator=, ~CvPlotIndicatorData
- **CvPopupInfo** (34): CvPopupInfo, `default ctor closure', addPythonButton, getButtonPopupType, getData1, getData2, getData3, getFlags, getNumPythonButtons, getOnClickedPythonCallback, getOnFocusPythonCallback, getOption1, getOption2, getPendingDelete, getPythonButtonArt, getPythonButtonText, getPythonModule, getText, operator=, read, setButtonPopupType, setData1, setData2, setData3, setFlags, setOnClickedPythonCallback, setOnFocusPythonCallback, setOption1, setOption2, setPendingDelete, setPythonModule, setText, write, ~CvPopupInfo
- **CvPythonModulesInfo** (9): getScreen, isCivicScreen, isCorporationScreen, isDomesticAdvisor, isEspionageAdvisor, isForeignAdvisor, isMainInterfaceScreen, isMilitaryAdvisor, isVictoryScreen
- **CvQuestInfo** (21): CvQuestInfo, getNumQuestLinks, getNumQuestMessages, getNumQuestSounds, getQuestBodyText, getQuestLinkName, getQuestLinkType, getQuestMessages, getQuestObjective, getQuestScript, getQuestSounds, initQuestLinks, reset, setNumQuestMessages, setNumQuestSounds, setQuestBodyText, setQuestMessages, setQuestObjective, setQuestScript, setQuestSounds, ~CvQuestInfo
- **CvQuestInfo::QuestLink** (1): QuestLink
- **CvRandom** (6): CvRandom, get, getFloat, getSeed, init, ~CvRandom
- **CvReplayInfo** (52): CvReplayInfo, addReplayMessage, clearReplayMessageMap, createInfo, getActivePlayer, getCalendar, getCivAdjective, getCivDescription, getClimate, getColor, getDifficulty, getEra, getFinalAgriculture, getFinalDate, getFinalEconomy, getFinalIndustry, getFinalScore, getFinalTurn, getGameSpeed, getInitialTurn, getLeader, getLeaderName, getMapHeight, getMapScriptName, getMapWidth, getMinimapPixels, getModName, getNormalizedScore, getNumPlayers, getNumReplayMessages, getPlayerAgriculture, getPlayerEconomy, getPlayerIndustry, getPlayerScore, getReplayMessageColor, getReplayMessagePlayer, getReplayMessagePlotX, getReplayMessagePlotY, getReplayMessageText, getReplayMessageTurn, getReplayMessageType, getSeaLevel, getShortCivDescription, getStartYear, getVictoryType, getWorldSize, isGameOption, isMultiplayer, isVictoryCondition, read, write, ~CvReplayInfo
- **CvRiverModelInfo** (10): CvRiverModelInfo, getBorderFile, getConnectString, getDeltaString, getModelFile, getRotateString, getTextureIndex, setBorderFile, setModelFile, ~CvRiverModelInfo
- **CvRouteModelInfo** (13): CvRouteModelInfo, getConnectString, getLateModelFile, getModelConnectString, getModelFile, getModelFileKey, getRotateString, getRouteType, isAnimated, setLateModelFile, setModelFile, setModelFileKey, ~CvRouteModelInfo
- **CvScalableInfo** (5): CvScalableInfo, getInterfaceScale, getScale, setInterfaceScale, setScale
- **CvSelectionGroup** (30): NotifyEntity, addUnit, autoMission, canAllMove, canDoCommand, canDoInterfaceMode, canDoInterfaceModeAt, canMoveInto, canMoveOrAttackInto, canStartMission, clearUnits, deleteUnitNode, getHeadUnit, getLengthMissionQueue, getNumUnits, getOwner, getUnitAt, getUnitIndex, headMissionQueueNode, headUnitNode, init, isBusy, lastMissionPlot, nextMissionQueueNode, nextUnitNode, plot, pushMission, readyToSelect, reset, uninit
- **CvSelectionGroupAI** (2): CvSelectionGroupAI, ~CvSelectionGroupAI
- **CvSlideShowInfo** (8): CvSlideShowInfo, getPath, getStartTime, getTransitionType, setPath, setStartTime, setTransitionType, ~CvSlideShowInfo
- **CvSlideShowRandomInfo** (4): CvSlideShowRandomInfo, getPath, setPath, ~CvSlideShowRandomInfo
- **CvSpaceShipInfo** (12): CvSpaceShipInfo, getArtType, getCameraUpAxis, getEventCode, getNodeName, getPartNumber, getProjectName, getProjectType, getSpaceShipInfoType, setNodeName, setProjectName, ~CvSpaceShipInfo
- **CvStatBase** (4): CvStatBase, operator=, ~CvStatBase
- **CvStatFloat** (4): CvStatFloat, operator=, ~CvStatFloat
- **CvStatInt** (4): CvStatInt, operator=, ~CvStatInt
- **CvStatString** (4): CvStatString, operator=, ~CvStatString
- **CvStatistics** (1): getPlayerRecord
- **CvTalkingHeadMessage** (21): CvTalkingHeadMessage, `default ctor closure', getDescription, getFlashColor, getFromPlayer, getIcon, getLength, getMessageType, getOffScreenArrows, getOnScreenArrows, getShown, getSound, getTarget, getTurn, getX, getY, setFromPlayer, setLength, setShown, setTarget, ~CvTalkingHeadMessage
- **CvTeam** (22): canDeclareWar, canLaunch, countNumHumanGameTurnActive, declareWar, finalizeProjectArtTypes, getAliveCount, getCompletedSpaceshipProjects, getName, getNumMembers, getProjectArtType, getProjectDefaultArtType, getProjectPartNumber, hasLaunched, init, isAlive, isAtWar, isProjectAndArtMaxedOut, makePeace, reset, setAtWar, setProjectArtType, setProjectDefaultArtType
- **CvTeamAI** (1): getTeamNonInl
- **CvTerrainInfo** (1): getArtDefineTag
- **CvTerrainPlaneInfo** (15): CvTerrainPlaneInfo, getBaseTexture, getCloseAlpha, getFogType, getMaterialAlpha, getTextureScalingU, getTextureScalingV, getTextureScrollRateU, getTextureScrollRateV, getZHeight, isGroundPlane, isVisible, read, setBaseTexture, ~CvTerrainPlaneInfo
- **CvThroneRoomCamera** (1): getFileName
- **CvThroneRoomInfo** (12): CvThroneRoomInfo, getAnimation, getEvent, getFromState, getNodeName, getToState, setAnimation, setEvent, setFromState, setNodeName, setToState, ~CvThroneRoomInfo
- **CvThroneRoomStyleInfo** (8): CvThroneRoomStyleInfo, getArtStyleType, getEraType, getFileName, setArtStyleType, setEraType, setFileName, ~CvThroneRoomStyleInfo
- **CvTutorialInfo** (8): CvTutorialInfo, getNextTutorialInfoType, getNumTutorialMessages, getTutorialMessage, initTutorialMessages, resetMessages, setNextTutorialInfoType, ~CvTutorialInfo
- **CvTutorialMessage** (10): CvTutorialMessage, getImage, getNumTutorialScripts, getSound, getText, getTutorialScriptByIndex, setImage, setSound, setText, ~CvTutorialMessage
- **CvUnit** (67): NotifyEntity, airCurrCombatStrFloat, airMaxCombatStrFloat, atPlot, canAirAttack, canAirDefend, canFight, canMove, cheat, currCombatStrFloat, currHitPoints, getAnimationMaxSpeed, getAnimationPadTime, getArtInfo, getBuildType, getButton, getCombatTimer, getCombatUnit, getDCMBombAccuracy, getDCMBombRange, getDamage, getDomainType, getFacingDirection, getFormationType, getGroup, getGroupDefinitions, getGroupSize, getHealthBarModifier, getHotKeyNumber, getID, getIDInfo, getLayerAnimationPaths, getLeaderUnitType, getName, getNameKey, getOwner, getRenderPriority, getSelectionSoundScript, getSubUnitCount, getSubUnitsAlive, getTeam, getUnitGroupRequired, getUnitType, getVisualOwner, getX, getY, hasMoved, isAttacking, isDead, isDefending, isFighting, isInfoBarDirty, isInvisible, isMechUnit, isPromotionReady, isRanged, isRenderAlways, isRenderBelowWater, isSuicide, isWaiting, joinGroup, maxCombatStrFloat, maxHitPoints, plot, setInfoBarDirty, shouldShowEnemyGlow, shouldShowFoundBorders
- **CvUnitFormationInfo** (11): CvUnitFormationInfo, addUnitEntry, getEventTypes, getFormationType, getGreatUnitEntry, getNumGreatUnitEntries, getNumSiegeUnitEntries, getNumUnitEntries, getSiegeUnitEntry, getUnitEntry, ~CvUnitFormationInfo
- **CvVictoryInfo** (1): isPermanent
- **CvWBData** (4): CvWBData, operator=, ~CvWBData
- **CvWaterPlaneInfo** (14): CvWaterPlaneInfo, getBaseTexture, getMaterialAlpha, getMaterialDiffuse, getMaterialEmmisive, getMaterialSpecular, getTextureScaling, getTextureScrollRateU, getTextureScrollRateV, getTransitionTexture, read, setBaseTexture, setTransitionTexture, ~CvWaterPlaneInfo
- **CvWidgetDataStruct** (1): operator=
- **CvWorldInfo** (1): getDefaultPlayers
- **CvWorldPickerInfo** (14): CvWorldPickerInfo, getClimatePath, getMapName, getModelFile, getNumClimates, getNumSizes, getNumWaterLevelDecals, getNumWaterLevelGloss, getSize, getWaterLevelDecalPath, getWaterLevelGlossPath, setMapName, setModelFile, ~CvWorldPickerInfo
- **CvXMLLoadUtility** (31): CleanUpGlobalVariables, CreateFXml, CvXMLLoadUtility, DestroyFXml, GetChildXmlValByName, GetNumProgressSteps, LoadBasicInfos, LoadCivXml, LoadGlobalText, LoadGraphicOptions, LoadPlayerOptions, LoadPostMenuGlobals, LoadPreMenuGlobals, MapChildren, ReadGlobalDefines, RegisterProgressCB, ResetGlobalEffectInfo, ResetLandscapeInfo, SetGlobalArtDefines, SetGlobalDefines, SetGlobalTypes, SetPostGlobalsGlobalDefines, SetupGlobalLandscapeInfo, SkipToNextVal, ~CvXMLLoadUtility
- **CyArgsList** (15): CyArgsList, add, clear, makeFunctionArgs, push_back, size
- **CyCity** (1): CyCity
- **CyMap** (1): CyMap
- **CyPlot** (3): CyPlot, getPoint
- **CyUnit** (1): CyUnit
- **FOWVis** (2): getOffsets, operator=
- **GameTurnInfo** (1): operator=
- **IDInfo** (5): IDInfo, `default ctor closure', operator=, operator==, reset
- **MissionData** (1): operator=
- **OrderData** (1): operator=
- **PBGameSetupData** (9): PBGameSetupData, getCustomMapOption, getMPOptionAt, getMapName, getOptionAt, getVictory, operator=, ~PBGameSetupData
- **PBPlayerAdminData** (7): PBPlayerAdminData, getName, getPing, getScore, operator=, ~PBPlayerAdminData
- **PBPlayerSetupData** (5): PBPlayerSetupData, getStatusText, operator=, ~PBPlayerSetupData
- **PopupReturn** (4): PopupReturn, operator=, read, write
- **TradeData** (1): operator=
- **XYCoords** (5): XYCoords, `default ctor closure', operator!=, operator=, operator==

## Implemented by the game exe (370)

Pure virtual methods of classes the source never derives from and never implements: the DLL calls them through the interface pointers the exe hands it (`gDLL` and the like), so the exe provides them.

- **CvArtFileMgr::ArtInfoItem** (3, 3 called from the source)
- **CvDLLEngineIFaceBase** (50, 50 called from the source)
- **CvDLLFAStarIFaceBase** (11, 11 called from the source)
- **CvDLLFeatureIFaceBase** (8, 8 called from the source)
- **CvDLLFlagEntityIFaceBase** (6, 6 called from the source)
- **CvDLLInterfaceIFaceBase** (125, 125 called from the source)
- **CvDLLPlotBuilderIFaceBase** (2, 2 called from the source)
- **CvDLLPythonIFaceBase** (5, 5 called from the source)
- **CvDLLRiverIFaceBase** (2, 2 called from the source)
- **CvDLLRouteIFaceBase** (5, 5 called from the source)
- **CvDLLSymbolIFaceBase** (9, 9 called from the source)
- **CvDLLUtilityIFaceBase** (119, 119 called from the source)
- **CvDLLXmlIFaceBase** (20, 20 called from the source)
- **FDataStreamBase** (5, 5 called from the source)

## Called from Python: functions exposed by boost::python (3892)

Per C++ class: how many functions are exposed. The full list with Python names is `map/python_defs.tsv`.

| C++ class | exposed |
|---|---|
| (global) | 53 |
| CvActionInfo | 10 |
| CvArtInfoAsset | 5 |
| CvArtInfoCivilization | 1 |
| CvAssetInfoBase | 4 |
| CvBonusClassInfo | 1 |
| CvBonusInfo | 35 |
| CvBuildInfo | 12 |
| CvBuildingClassInfo | 8 |
| CvBuildingInfo | 154 |
| CvCivicInfo | 77 |
| CvCivicOptionInfo | 1 |
| CvCivilizationInfo | 23 |
| CvClimateInfo | 11 |
| CvColorInfo | 1 |
| CvCommerceInfo | 5 |
| CvCorporationInfo | 15 |
| CvCultureLevelInfo | 2 |
| CvDiplomacyInfo | 8 |
| CvDiplomacyTextInfo | 8 |
| CvEmphasizeInfo | 4 |
| CvEraInfo | 28 |
| CvEspionageMissionInfo | 29 |
| CvEventInfo | 70 |
| CvEventTriggerInfo | 72 |
| CvFeatureInfo | 26 |
| CvForceControlInfo | 1 |
| CvGameOptionInfo | 2 |
| CvGameSpeedInfo | 23 |
| CvGameText | 3 |
| CvGoodyInfo | 16 |
| CvGraphicOptionInfo | 1 |
| CvHandicapInfo | 60 |
| CvHotkeyInfo | 10 |
| CvHurryInfo | 3 |
| CvImprovementBonusInfo | 4 |
| CvImprovementInfo | 38 |
| CvInfoBase | 10 |
| CvInterfaceModeInfo | 7 |
| CvLeaderHeadInfo | 88 |
| CvMPOptionInfo | 1 |
| CvMainMenuInfo | 5 |
| CvMissionInfo | 6 |
| CvPlayerColorInfo | 3 |
| CvPlayerOptionInfo | 1 |
| CvProcessInfo | 2 |
| CvProjectInfo | 20 |
| CvPromotionInfo | 52 |
| CvPythonModulesInfo | 9 |
| CvQuestInfo | 13 |
| CvRandom | 2 |
| CvReligionInfo | 18 |
| CvRouteInfo | 7 |
| CvRouteModelInfo | 7 |
| CvScalableInfo | 3 |
| CvSeaLevelInfo | 1 |
| CvSpecialBuildingInfo | 4 |
| CvSpecialUnitInfo | 4 |
| CvSpecialistInfo | 9 |
| CvTechInfo | 44 |
| CvTerrainInfo | 13 |
| CvTraitInfo | 25 |
| CvTurnTimerInfo | 4 |
| CvTutorialInfo | 3 |
| CvTutorialMessage | 5 |
| CvUnitClassInfo | 5 |
| CvUnitInfo | 168 |
| CvUpkeepInfo | 2 |
| CvVictoryInfo | 14 |
| CvVoteInfo | 18 |
| CvVoteSourceInfo | 6 |
| CvWorldInfo | 18 |
| CvYieldInfo | 13 |
| CyArea | 39 |
| CyArtFileMgr | 14 |
| CyCity | 512 |
| CyDeal | 13 |
| CyGame | 222 |
| CyGameTextMgr | 35 |
| CyGlobalContext | 275 |
| CyHallOfFameInfo | 3 |
| CyMap | 52 |
| CyMapGenerator | 21 |
| CyMessageControl | 13 |
| CyPlayer | 441 |
| CyPlot | 195 |
| CyReplayInfo | 46 |
| CySelectionGroup | 59 |
| CyTeam | 182 |
| CyUnit | 325 |
| EventMessage | 1 |
| FOWVis | 1 |
| PBGameSetupData | 5 |
| PBPlayerAdminData | 3 |
| PBPlayerSetupData | 1 |

## The DLL calls Python (181 sites)

`callFunction(module, "function")` sites. A module shown as ? is chosen at run time (the map script).

| Python function | defined in | called from |
|---|---|---|
| ?.? | not found | CvDLLButtonPopup::OnOkClicked |
| ?.CvRandomEventInterface | not found | CvCity::getTriggerValue, CvGameTextMgr::setEventHelp, CvPlayer::applyEvent, CvPlayer::canDoEvent, CvPlayer::checkExpireEvent, CvPlayer::initTriggeredData, CvPlayer::setTriggerFired, CvUnit::getTriggerValue |
| ?.CvScreensInterface | not found | CvDLLButtonPopup::OnFocus, CvDLLButtonPopup::launchPythonScreen |
| ?.addBonusType | not found | CvMapGenerator::addBonuses |
| ?.addBonuses | not found | CvMapGenerator::addBonuses |
| ?.addFeatures | not found | CvMapGenerator::addFeatures |
| ?.addGoodies | not found | CvMapGenerator::addGoodies |
| ?.addLakes | not found | CvMapGenerator::addLakes |
| ?.addRivers | not found | CvMapGenerator::addRivers |
| ?.afterGeneration | not found | CvMapGenerator::afterGeneration |
| ?.assignStartingPlots | not found | CvGame::assignStartingPlots |
| ?.beforeGeneration | not found | CvMapGenerator::generateRandomMap |
| ?.beforeInit | not found | CvMap::init |
| ?.canPlaceBonusAt | not found | CvMapGenerator::canPlaceBonusAt |
| ?.canPlaceGoodyAt | not found | CvMapGenerator::canPlaceGoodyAt |
| ?.findStartingArea | not found | CvPlayer::findStartingArea |
| ?.findStartingPlot | not found | CvPlayer::findStartingPlot |
| ?.generatePlotTypes | not found | CvMapGenerator::generatePlotTypes |
| ?.generateRandomMap | not found | CvMapGenerator::generateRandomMap |
| ?.generateTerrainTypes | not found | CvMapGenerator::generateTerrain |
| ?.getBottomLatitude | not found | CvMap::reset |
| ?.getCustomMapOptionDefault | not found | CvInitCore::refreshCustomMapOptions |
| ?.getGridSize | not found | CvMap::reset |
| ?.getNumCustomMapOptions | not found | CvInitCore::refreshCustomMapOptions |
| ?.getNumHiddenCustomMapOptions | not found | CvInitCore::refreshCustomMapOptions |
| ?.getRiverAltitude | not found | CvMapGenerator::getRiverValueAtPlot |
| ?.getRiverStartCardinalDirection | not found | CvMapGenerator::doRiver |
| ?.getTopLatitude | not found | CvMap::reset |
| ?.getWrapX | not found | CvMap::reset |
| ?.getWrapY | not found | CvMap::reset |
| ?.isBonusIgnoreLatitude | not found | CvGame::pythonIsBonusIgnoreLatitudes |
| ?.minStartingDistanceModifier | not found | CvPlayer::startingPlotRange |
| ?.normalizeAddExtras | not found | CvGame::normalizeStartingPlots |
| ?.normalizeAddFoodBonuses | not found | CvGame::normalizeStartingPlots |
| ?.normalizeAddGoodTerrain | not found | CvGame::normalizeStartingPlots |
| ?.normalizeAddLakes | not found | CvGame::normalizeStartingPlots |
| ?.normalizeAddRiver | not found | CvGame::normalizeStartingPlots |
| ?.normalizeRemoveBadFeatures | not found | CvGame::normalizeStartingPlots |
| ?.normalizeRemoveBadTerrain | not found | CvGame::normalizeStartingPlots |
| ?.normalizeRemovePeaks | not found | CvGame::normalizeStartingPlots |
| ?.normalizeStartingPlotLocations | not found | CvGame::normalizeStartingPlots |
| ?.startHumansOnSameTile | not found | CvPlayer::addFreeUnit |
| CvAppInterface.gameEndSave | EntryPoints/CvAppInterface.py:287 | CvGame::setGameState |
| CvAppInterface.gameExitSave | EntryPoints/CvAppInterface.py:292 | CvDLLButtonPopup::OnOkClicked |
| CvAppInterface.gameStartSave | EntryPoints/CvAppInterface.py:282 | CvGame::regenerateMap |
| CvAppInterface.getModNameAndVersion | EntryPoints/CvAppInterface.py:273 | CvDLLWidgetData::parseFlagHelp |
| CvAppInterface.getOptionBOOL | EntryPoints/CvAppInterface.py:216 | getBugOptionBOOL |
| CvAppInterface.getOptionINT | EntryPoints/CvAppInterface.py:230 | getBugOptionINT |
| CvAppInterface.netAddReminder | not found | CvNetAddReminder::Execute |
| CvEventInterface.onEvent | EntryPoints/CvEventInterface.py:28 | CvDllPythonEvents::postEvent |
| CvGameInterface.AI_chooseProduction | base/EntryPoints/CvGameInterface.py:148 | CvCityAI::AI_chooseProduction |
| CvGameInterface.AI_chooseTech | base/EntryPoints/CvGameInterface.py:143 | CvPlayerAI::AI_chooseFreeTech, CvPlayerAI::AI_chooseResearch |
| CvGameInterface.AI_doDiplo | base/EntryPoints/CvGameInterface.py:163 | CvPlayerAI::AI_doDiplo |
| CvGameInterface.AI_doWar | base/EntryPoints/CvGameInterface.py:158 | CvTeamAI::AI_doWar |
| CvGameInterface.AI_unitUpdate | base/EntryPoints/CvGameInterface.py:153 | CvUnitAI::AI_update |
| CvGameInterface.calculateScore | base/EntryPoints/CvGameInterface.py:168 | CvPlayer::calculateScore |
| CvGameInterface.canBuild | not found | CvPlot::canBuild |
| CvGameInterface.canConstruct | base/EntryPoints/CvGameInterface.py:119 | CvCity::canConstruct |
| CvGameInterface.canCreate | base/EntryPoints/CvGameInterface.py:127 | CvCity::canCreate |
| CvGameInterface.canDeclareWar | not found | CvTeam::canDeclareWar, CvTeam::canEventuallyDeclareWar |
| CvGameInterface.canDoCivic | base/EntryPoints/CvGameInterface.py:103 | CvPlayer::canDoCivics |
| CvGameInterface.canFoundCitiesOnWater | not found | CvPlayer::canFound |
| CvGameInterface.canMaintain | base/EntryPoints/CvGameInterface.py:135 | CvCity::canMaintain |
| CvGameInterface.canPickPlot | not found | CvGame::getPlotHighlightColor |
| CvGameInterface.canRazeCity | not found | CvPlayer::acquireCity, CvPlayer::canRaze |
| CvGameInterface.canResearch | base/EntryPoints/CvGameInterface.py:95 | CvPlayer::canResearch |
| CvGameInterface.canTrain | base/EntryPoints/CvGameInterface.py:111 | CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const |
| CvGameInterface.cannotConstruct | base/EntryPoints/CvGameInterface.py:123 | CvCity::canConstruct |
| CvGameInterface.cannotCreate | base/EntryPoints/CvGameInterface.py:131 | CvCity::canCreate |
| CvGameInterface.cannotDoCivic | base/EntryPoints/CvGameInterface.py:107 | CvPlayer::canDoCivics |
| CvGameInterface.cannotDoControl | base/EntryPoints/CvGameInterface.py:91 | CvGame::canDoControl |
| CvGameInterface.cannotFoundCity | not found | CvPlayer::canFound |
| CvGameInterface.cannotHandleAction | base/EntryPoints/CvGameInterface.py:79 | CvGame::canHandleAction |
| CvGameInterface.cannotMaintain | base/EntryPoints/CvGameInterface.py:139 | CvCity::canMaintain |
| CvGameInterface.cannotResearch | base/EntryPoints/CvGameInterface.py:99 | CvPlayer::canEverResearch |
| CvGameInterface.cannotSelectionListGameNetMessage | base/EntryPoints/CvGameInterface.py:87 | CvGame::selectionListGameNetMessage |
| CvGameInterface.cannotSelectionListMove | base/EntryPoints/CvGameInterface.py:83 | CvGame::selectionListMove |
| CvGameInterface.cannotSpreadReligion | not found | CvUnit::canSpread |
| CvGameInterface.cannotTrain | base/EntryPoints/CvGameInterface.py:115 | CvCity::canTrain(UnitTypes, bool, bool, bool, bool) const |
| CvGameInterface.citiesDestroyFeatures | not found | CvCity::init |
| CvGameInterface.createBarbarianCities | base/EntryPoints/CvGameInterface.py:31 | CvGame::createBarbarianCities |
| CvGameInterface.createBarbarianUnits | base/EntryPoints/CvGameInterface.py:35 | CvGame::createBarbarianUnits |
| CvGameInterface.doCityCaptureGold | not found | CvPlayer::acquireCity |
| CvGameInterface.doCombat | not found | CvSelectionGroup::groupAttack, CvSelectionGroup::groupStackAttack |
| CvGameInterface.doCulture | base/EntryPoints/CvGameInterface.py:200 | CvCity::doCulture |
| CvGameInterface.doGold | base/EntryPoints/CvGameInterface.py:180 | CvPlayer::doGold |
| CvGameInterface.doGoody | base/EntryPoints/CvGameInterface.py:188 | CvPlayer::doGoody |
| CvGameInterface.doGreatPeople | base/EntryPoints/CvGameInterface.py:212 | CvCity::doGreatPeople |
| CvGameInterface.doGrowth | base/EntryPoints/CvGameInterface.py:192 | CvCity::doGrowth |
| CvGameInterface.doHeadquarters | not found | CvGame::doHeadquarters |
| CvGameInterface.doHolyCity | base/EntryPoints/CvGameInterface.py:172 | CvGame::doHolyCity |
| CvGameInterface.doHolyCityTech | base/EntryPoints/CvGameInterface.py:176 | CvTeam::setHasTech |
| CvGameInterface.doMeltdown | base/EntryPoints/CvGameInterface.py:216 | CvCity::doMeltdown |
| CvGameInterface.doPillageGold | not found | CvUnit::pillage |
| CvGameInterface.doPlotCulture | base/EntryPoints/CvGameInterface.py:204 | CvCity::doPlotCulture |
| CvGameInterface.doProduction | base/EntryPoints/CvGameInterface.py:196 | CvCity::doProduction |
| CvGameInterface.doReligion | base/EntryPoints/CvGameInterface.py:208 | CvCity::doReligion |
| CvGameInterface.doResearch | base/EntryPoints/CvGameInterface.py:184 | CvPlayer::doResearch |
| CvGameInterface.doReviveActivePlayer | not found | CvGame::reviveActivePlayer, CvGame::revivePlayer |
| CvGameInterface.getBuildingCostMod | not found | CvCity::getProductionNeeded(BuildingTypes) const |
| CvGameInterface.getCityFoundValue | not found | CvPlayerAI::AI_recalculateFoundValues, CvPlayerAI::AI_updateFoundValues, CvPlot::getFoundValue |
| CvGameInterface.getConscriptUnitType | not found | CvCity::getConscriptUnit |
| CvGameInterface.getExperienceNeeded | not found | calculateExperience |
| CvGameInterface.getExtraCost | not found | CvPlayer::calculatePreInflatedCosts |
| CvGameInterface.getFirstRecommendedTech | base/EntryPoints/CvGameInterface.py:47 | CvDLLButtonPopup::launchChooseTechPopup |
| CvGameInterface.getRecommendedBuilding | base/EntryPoints/CvGameInterface.py:67 | CvDLLButtonPopup::launchProductionPopup |
| CvGameInterface.getRecommendedUnit | base/EntryPoints/CvGameInterface.py:63 | CvDLLButtonPopup::launchProductionPopup |
| CvGameInterface.getSecondRecommendedTech | base/EntryPoints/CvGameInterface.py:51 | CvDLLButtonPopup::launchChooseTechPopup |
| CvGameInterface.getUnitCostMod | not found | CvPlayer::getProductionNeeded(UnitTypes) const |
| CvGameInterface.getUpgradePriceOverride | not found | CvUnit::upgradePrice |
| CvGameInterface.isActionRecommended | base/EntryPoints/CvGameInterface.py:75 | CvUnit::isActionRecommended |
| CvGameInterface.isPlayerResearch | base/EntryPoints/CvGameInterface.py:27 | CvPlayer::isResearch |
| CvGameInterface.isVictory | not found | CvGame::testVictory(VictoryTypes, TeamTypes, bool*) const |
| CvGameInterface.isVictoryTest | base/EntryPoints/CvGameInterface.py:23 | CvGame::testVictory() |
| CvGameInterface.showExamineCityButton | base/EntryPoints/CvGameInterface.py:59 | CvDLLButtonPopup::launchProductionPopup |
| CvGameInterface.showTechChooserButton | base/EntryPoints/CvGameInterface.py:43 | CvDLLButtonPopup::launchChooseTechPopup |
| CvGameInterface.skipProductionPopup | base/EntryPoints/CvGameInterface.py:55 | CvDLLButtonPopup::launchProductionPopup |
| CvGameInterface.skipResearchPopup | base/EntryPoints/CvGameInterface.py:39 | CvDLLButtonPopup::launchChooseTechPopup |
| CvGameInterface.unitCannotMoveInto | not found | CvUnit::canMoveInto |
| CvGameInterface.updateColoredPlots | base/EntryPoints/CvGameInterface.py:71 | CvGame::updateColoredPlots |
| CvScreensInterface.WorldBuilderGetHighlightPlot | EntryPoints/CvScreensInterface.py:680 | CvGame::getNewHighlightPlot |
| CvScreensInterface.pediaBack | EntryPoints/CvScreensInterface.py:411 | CvDLLWidgetData::doPediaBack |
| CvScreensInterface.pediaForward | EntryPoints/CvScreensInterface.py:414 | CvDLLWidgetData::doPediaForward |
| CvScreensInterface.pediaJumpToBonus | EntryPoints/CvScreensInterface.py:477 | CvDLLWidgetData::doPediaBonusJump |
| CvScreensInterface.pediaJumpToBuilding | EntryPoints/CvScreensInterface.py:447 | CvDLLWidgetData::doPediaBuildingJump, CvDLLWidgetData::doPediaConstructJump |
| CvScreensInterface.pediaJumpToCiv | EntryPoints/CvScreensInterface.py:489 | CvDLLWidgetData::doPediaCivilizationJump |
| CvScreensInterface.pediaJumpToCivic | EntryPoints/CvScreensInterface.py:501 | CvDLLWidgetData::doPediaCivicJump |
| CvScreensInterface.pediaJumpToCorporation | EntryPoints/CvScreensInterface.py:513 | CvDLLWidgetData::doPediaCorporationJump |
| CvScreensInterface.pediaJumpToFeature | EntryPoints/CvScreensInterface.py:471 | CvDLLWidgetData::doPediaFeatureJump |
| CvScreensInterface.pediaJumpToImprovement | EntryPoints/CvScreensInterface.py:483 | CvDLLWidgetData::doPediaBuildJump, CvDLLWidgetData::doPediaImprovementJump |
| CvScreensInterface.pediaJumpToLeader | EntryPoints/CvScreensInterface.py:495 | CvDLLWidgetData::doPediaLeaderJump |
| CvScreensInterface.pediaJumpToProject | EntryPoints/CvScreensInterface.py:453 | CvDLLWidgetData::doPediaProjectJump |
| CvScreensInterface.pediaJumpToPromotion | EntryPoints/CvScreensInterface.py:441 | CvDLLWidgetData::doPediaPromotionJump |
| CvScreensInterface.pediaJumpToReligion | EntryPoints/CvScreensInterface.py:507 | CvDLLWidgetData::doPediaReligionJump |
| CvScreensInterface.pediaJumpToSpecialist | EntryPoints/CvScreensInterface.py:459 | CvDLLWidgetData::doPediaSpecialistJump |
| CvScreensInterface.pediaJumpToTech | EntryPoints/CvScreensInterface.py:423 | CvDLLWidgetData::doPediaTechJump |
| CvScreensInterface.pediaJumpToTerrain | EntryPoints/CvScreensInterface.py:465 | CvDLLWidgetData::doPediaTerrainJump |
| CvScreensInterface.pediaJumpToUnit | EntryPoints/CvScreensInterface.py:429 | CvDLLWidgetData::doPediaTrainJump, CvDLLWidgetData::doPediaUnitJump |
| CvScreensInterface.pediaJumpToUnitChart | EntryPoints/CvScreensInterface.py:435 | CvDLLWidgetData::doPediaUnitCombatJump |
| CvScreensInterface.pediaMain | EntryPoints/CvScreensInterface.py:417 | CvDLLWidgetData::doPediaMain |
| CvScreensInterface.pediaShow | EntryPoints/CvScreensInterface.py:407 | CvGame::doControl |
| CvScreensInterface.pediaShowHistorical | EntryPoints/CvScreensInterface.py:519 | CvDLLWidgetData::doPediaDescription |
| CvScreensInterface.refreshMilitaryAdvisor | EntryPoints/CvScreensInterface.py:1017 | CvDLLWidgetData::doRefreshMilitaryAdvisor |
| CvScreensInterface.showCivicsScreen | EntryPoints/CvScreensInterface.py:90 | CvDLLButtonPopup::OnOkClicked, CvGame::doControl |
| CvScreensInterface.showCorporationScreen | EntryPoints/CvScreensInterface.py:100 | CvGame::doControl |
| CvScreensInterface.showDomesticAdvisor | EntryPoints/CvScreensInterface.py:148 | CvGame::doControl |
| CvScreensInterface.showEspionageAdvisor | EntryPoints/CvScreensInterface.py:175 | CvGame::doControl |
| CvScreensInterface.showFinanceAdvisor | EntryPoints/CvScreensInterface.py:129 | CvGame::doControl |
| CvScreensInterface.showForeignAdvisorScreen | EntryPoints/CvScreensInterface.py:110 | CvDLLWidgetData::doForeignAdvisor, CvGame::doControl |
| CvScreensInterface.showHallOfFame | EntryPoints/CvScreensInterface.py:86 | CvGame::doControl |
| CvScreensInterface.showInfoScreen | EntryPoints/CvScreensInterface.py:223 | CvGame::doControl |
| CvScreensInterface.showMilitaryAdvisor | EntryPoints/CvScreensInterface.py:166 | CvGame::doControl |
| CvScreensInterface.showOptionsScreen | EntryPoints/CvScreensInterface.py:105 | CvDLLButtonPopup::OnOkClicked, CvGame::doControl |
| CvScreensInterface.showReligionScreen | EntryPoints/CvScreensInterface.py:95 | CvGame::doControl |
| CvScreensInterface.showTechChooser | EntryPoints/CvScreensInterface.py:81 | CvDLLButtonPopup::OnOkClicked, CvGame::doControl |
| CvScreensInterface.showVictoryScreen | EntryPoints/CvScreensInterface.py:263 | CvGame::doControl |
| PbMain.sendEmail | base/EntryPoints/PbMain.py:90 | CvPlayer::sendReminder |

## Events posted to Python (81)

Each `CvDllPythonEvents` report function posts one event; the handlers are every registration found: the event manager's map, `addEventHandler` calls, and the BUG configuration XML.

| event | posted by | handlers |
|---|---|---|
| BeginGameTurn | CvDllPythonEvents::reportBeginGameTurn | AIAutoPlay.__init__: self.onBeginGameTurn (Revolution/Gameready/AIAutoPlay.py:115); AIAutoPlay.removeEventHandlers: self.customEM.onBeginGameTurn (Revolution/Gameready/AIAutoPlay.py:148); BarbarianCiv.__init__: self.onBeginGameTurn (Revolution/Gameready/BarbarianCiv.py:87); TechDiffusion.__init__: self.onBeginGameTurn (Revolution/Gameready/TechDiffusion.py:42); CvEventManager.onBeginGameTurn (base/CvEventManager.py:85) |
| BeginPlayerTurn | CvDllPythonEvents::reportBeginPlayerTurn | EspionageEventEvent.__init__: self.onBeginPlayerTurn (Contrib/EspionageEventManager.py:49); AutoLogEvent.__init__: self.onBeginPlayerTurn (Contrib/autologEventManager.py:150); Tester.__init__: self.onBeginPlayerTurn (Revolution/Development/Tester.py:49); AIAutoPlay.__init__: self.onBeginPlayerTurn (Revolution/Gameready/AIAutoPlay.py:94); DynamicCivNames.__init__: self.onBeginPlayerTurn (Revolution/Gameready/DynamicCivNames.py:41); Revolution.__init__: self.onBeginPlayerTurn (Revolution/Gameready/Revolution.py:179); init: onBeginPlayerTurn (Revolution/RevEvents.py:79); RoMEventManager.__init__: self.onBeginPlayerTurn (RoMEventManager.py:46); CvEventManager.onBeginPlayerTurn (base/CvEventManager.py:87); BugUtil.doHotSeatCheck (Config/BUG Core.xml:98); ?.onBeginPlayerTurn (Config/Better Espionage.xml:80); RevDCMReligionControl.onBeginPlayerTurn (Config/RevDCM.xml:16) |
| EndGameTurn | CvDllPythonEvents::reportEndGameTurn | ReminderEventManager.__init__: self.onEndGameTurn (Contrib/ReminderEventManager.py:65); AutoLogEvent.__init__: self.onEndGameTurn (Contrib/autologEventManager.py:149); init: onEndGameTurn (Revolution/RevEvents.py:78); CvEventManager.onEndGameTurn (base/CvEventManager.py:86) |
| EndPlayerTurn | CvDllPythonEvents::reportEndPlayerTurn | AutoLogEvent.__init__: self.onEndPlayerTurn (Contrib/autologEventManager.py:151); AIAutoPlay.__init__: self.onEndPlayerTurn (Revolution/Gameready/AIAutoPlay.py:95); BarbarianCiv.__init__: self.onEndPlayerTurn (Revolution/Gameready/BarbarianCiv.py:88); Revolution.__init__: self.onEndPlayerTurn (Revolution/Gameready/Revolution.py:180); init: onEndPlayerTurn (Revolution/Gameready/StartAsMinors.py:51); init: onEndPlayerTurn (Revolution/RevEvents.py:80); CvEventManager.onEndPlayerTurn (base/CvEventManager.py:88) |
| GameEnd | CvDllPythonEvents::reportGameEnd | AutoLogEvent.__init__: self.onGameEnd (Contrib/autologEventManager.py:148); CvEventManager.onGameEnd (base/CvEventManager.py:83) |
| GameStart | CvDllPythonEvents::reportGameStart | BugEventManager.__init__: self.resetActiveTurn (BUG/BugEventManager.py:191); AbstractStatefulAlert.__init__: self.onGameStart (Contrib/Civ4lerts.py:167); EventSignsEventHandler.__init__: self.onGameStart (Contrib/EventSigns.py:450); FavoriteCivicDetector.__init__: self.onGameStart (Contrib/FavoriteCivicDetector.py:295); MoreCiv4lertsEvent.__init__: self.reset (Contrib/MoreCiv4lerts.py:66); ReminderEventManager.__init__: self.onGameStart (Contrib/ReminderEventManager.py:67); RevDCM.__init__: self.onGameStart (Contrib/RevDCM.py:29); AutoLogEvent.__init__: self.onGameStart (Contrib/autologEventManager.py:147); AIAutoPlay.__init__: self.onGameStart (Revolution/Gameready/AIAutoPlay.py:97); RevolutionInit.__init__: self.onGameStart (Revolution/RevolutionInit.py:67); RoMEventManager.__init__: self.onGameStart (RoMEventManager.py:45); CvEventManager.onGameStart (base/CvEventManager.py:82); BugData.onGameStart (Config/BUG Core.xml:102); ?.onGameStart (Config/Better Espionage.xml:77); ?.onGameStart (Config/Strategy Overlay.xml:88); CvTechChooser.resetTechPrefs (Config/init.xml:127) |
| Init | CvDllPythonEvents::reportInit | CvEventManager.onInit (base/CvEventManager.py:76) |
| ModNetMessage | CvDllPythonEvents::reportModNetMessage | AIAutoPlay.__init__: self.onModNetMessage (Revolution/Gameready/AIAutoPlay.py:89); Revolution.__init__: self.onModNetMessage (Revolution/Gameready/Revolution.py:181); RoMEventManager.__init__: self.onModNetMessage (RoMEventManager.py:43); ?.onModNetMessage (Config/Strategy Overlay.xml:98) |
| OnPreSave | CvDllPythonEvents::preSave | EventSignsEventHandler.__init__: self.onPreSave (Contrib/EventSigns.py:452); FavoriteCivicDetector.__init__: self.onPreSave (Contrib/FavoriteCivicDetector.py:297); ReminderEventManager.__init__: self.onPreSave (Contrib/ReminderEventManager.py:70); CvEventManager.onPreSave (base/CvEventManager.py:80); ?.onPreSave (Config/Strategy Overlay.xml:91) |
| PreEndGameTurn | CvDllPythonEvents::reportPreEndGameTurn | AIAutoPlay.__init__: self.onEndGameTurn (Revolution/Gameready/AIAutoPlay.py:90); Revolution.__init__: self.onEndGameTurn (Revolution/Gameready/Revolution.py:175) |
| UnInit | CvDllPythonEvents::reportUnInit | CvEventManager.onUnInit (base/CvEventManager.py:78) |
| UnitRename | CvDllPythonEvents::reportUnitRename | CvEventManager.onUnitRename (base/CvEventManager.py:114) |
| Update | CvDllPythonEvents::reportUpdate | CvEventManager.onUpdate (base/CvEventManager.py:77) |
| buildingBuilt | CvDllPythonEvents::reportBuildingBuilt | AutoLogEvent.__init__: self.onBuildingBuilt (Contrib/autologEventManager.py:156); init: onBuildingBuilt (Revolution/RevEvents.py:88); RoMEventManager.__init__: self.onBuildingBuilt (RoMEventManager.py:47); CvEventManager.onBuildingBuilt (base/CvEventManager.py:117); ?.onBuildingBuilt (Config/MovieMod.xml:4) |
| changeWar | CvDllPythonEvents::reportChangeWar | RefusesToTalk.__init__: self.onChangeWar (Contrib/Civ4lerts.py:823); AutoLogEvent.__init__: self.onChangeWar (Contrib/autologEventManager.py:172); Tester.__init__: self.onChangeWar (Revolution/Development/Tester.py:45); init: onChangeWar (Revolution/RevEvents.py:82); CvEventManager.onChangeWar (base/CvEventManager.py:127) |
| chat | CvDllPythonEvents::reportChat | CvEventManager.onChat (base/CvEventManager.py:125) |
| cityAcquired | CvDllPythonEvents::reportCityAcquired | MoreCiv4lertsEvent.__init__: self.OnCityAcquired (Contrib/MoreCiv4lerts.py:61); AutoLogEvent.__init__: self.onCityAcquired (Contrib/autologEventManager.py:176); CvEnhancedTechConquestEventManager.__init__: self.onCityAcquired (EnhancedTechConquestUtils/CvEnhancedTechConquestEventManager.py:18); BarbarianCiv.__init__: self.onCityAcquired (Revolution/Gameready/BarbarianCiv.py:91); DynamicCivNames.__init__: self.onCityAcquired (Revolution/Gameready/DynamicCivNames.py:44); Revolution.__init__: self.onCityAcquired (Revolution/Gameready/Revolution.py:169); init: onCityAcquired (Revolution/RevEvents.py:86); CvEventManager.onCityAcquired (base/CvEventManager.py:98) |
| cityAcquiredAndKept | CvDllPythonEvents::reportCityAcquiredAndKept | AbstractCityAlertManager.__init__: self.onCityAcquiredAndKept (Contrib/Civ4lerts.py:202) |
| cityBuildingBuilding | CvDllPythonEvents::reportCityBuildingBuilding | AbstractCanHurry.__init__: self.onCityBuildingBuilding (Contrib/Civ4lerts.py:634); AutoLogEvent.__init__: self.onCityBuildingBuilding (Contrib/autologEventManager.py:181); CvEventManager.onCityBuildingBuilding (base/CvEventManager.py:104) |
| cityBuildingProcess | CvDllPythonEvents::reportCityBuildingProcess | AbstractCanHurry.__init__: self.onCityBuildingProcess (Contrib/Civ4lerts.py:636) |
| cityBuildingProject | CvDllPythonEvents::reportCityBuildingProject | AbstractCanHurry.__init__: self.onCityBuildingProject (Contrib/Civ4lerts.py:635) |
| cityBuildingUnit | CvDllPythonEvents::reportCityBuildingUnit | AbstractCanHurry.__init__: self.onCityBuildingUnit (Contrib/Civ4lerts.py:633); AutoLogEvent.__init__: self.onCityBuildingUnit (Contrib/autologEventManager.py:180); CvEventManager.onCityBuildingUnit (base/CvEventManager.py:103) |
| cityBuilt | CvDllPythonEvents::reportCityBuilt | MoreCiv4lertsEvent.__init__: self.OnCityBuilt (Contrib/MoreCiv4lerts.py:62); BuildUnitName.__init__: self.onCityBuilt (Contrib/UnitNameEventManager.py:191); AutoLogEvent.__init__: self.onCityBuilt (Contrib/autologEventManager.py:174); AIAutoPlay.__init__: self.onCityBuilt (Revolution/Gameready/AIAutoPlay.py:108); AIAutoPlay.removeEventHandlers: self.customEM.onCityBuilt (Revolution/Gameready/AIAutoPlay.py:145); DynamicCivNames.__init__: self.onCityBuilt (Revolution/Gameready/DynamicCivNames.py:45); init: onCityBuilt (Revolution/RevEvents.py:85); RoMEventManager.__init__: self.onCityBuilt (RoMEventManager.py:50); CvEventManager.onCityBuilt (base/CvEventManager.py:96) |
| cityDoTurn | CvDllPythonEvents::reportCityProduction | CvEventManager.onCityDoTurn (base/CvEventManager.py:102) |
| cityGrowth | CvDllPythonEvents::reportCityGrowth | AutoLogEvent.__init__: self.onCityGrowth (Contrib/autologEventManager.py:179); CvEventManager.onCityGrowth (base/CvEventManager.py:101) |
| cityHurry | CvDllPythonEvents::reportCityHurry | none registered |
| cityLost | CvDllPythonEvents::reportCityLost | AbstractCityAlertManager.__init__: self.onCityLost (Contrib/Civ4lerts.py:203); MoreCiv4lertsEvent.__init__: self.OnCityLost (Contrib/MoreCiv4lerts.py:64); AutoLogEvent.__init__: self.onCityLost (Contrib/autologEventManager.py:177); Tester.__init__: self.onCityLost (Revolution/Development/Tester.py:46); init: onCityLost (Revolution/RevEvents.py:87); RoMEventManager.__init__: self.onCityLost (RoMEventManager.py:52); CvEventManager.onCityLost (base/CvEventManager.py:99) |
| cityRazed | CvDllPythonEvents::reportCityRazed | RefusesToTalk.__init__: self.onCityRazed (Contrib/Civ4lerts.py:824); MoreCiv4lertsEvent.__init__: self.OnCityRazed (Contrib/MoreCiv4lerts.py:63); AutoLogEvent.__init__: self.onCityRazed (Contrib/autologEventManager.py:175); RoMEventManager.__init__: self.onCityRazed (RoMEventManager.py:51); CvEventManager.onCityRazed (base/CvEventManager.py:97) |
| cityRename | CvDllPythonEvents::reportCityRename | CvEventManager.onCityRename (base/CvEventManager.py:105) |
| combatLogCollateral | CvDllPythonEvents::reportCombatLogCollateral | none registered |
| combatLogFlanking | CvDllPythonEvents::reportCombatLogFlanking | none registered |
| combatResult | CvDllPythonEvents::reportCombatResult | AutoLogEvent.__init__: self.onCombatResult (Contrib/autologEventManager.py:154); CvEventManager.onCombatResult (base/CvEventManager.py:90) |
| combatRetreat | CvDllPythonEvents::reportCombatRetreat | none registered |
| combatWithdrawal | CvDllPythonEvents::reportCombatWithdrawal | none registered |
| corporationFounded | CvDllPythonEvents::reportCorporationFounded | AutoLogEvent.__init__: self.onCorporationFounded (Contrib/autologEventManager.py:167) |
| corporationRemove | CvDllPythonEvents::reportCorporationRemove | AutoLogEvent.__init__: self.onCorporationRemove (Contrib/autologEventManager.py:169) |
| corporationSpread | CvDllPythonEvents::reportCorporationSpread | AutoLogEvent.__init__: self.onCorporationSpread (Contrib/autologEventManager.py:168) |
| cultureExpansion | CvDllPythonEvents::reportCultureExpansion | AutoLogEvent.__init__: self.onCultureExpansion (Contrib/autologEventManager.py:178); CvEventManager.onCultureExpansion (base/CvEventManager.py:100) |
| endGoldenAge | CvDllPythonEvents::reportEndGoldenAge | AutoLogEvent.__init__: self.onEndGoldenAge (Contrib/autologEventManager.py:171); CvEventManager.onEndGoldenAge (base/CvEventManager.py:124) |
| firstContact | CvDllPythonEvents::reportFirstContact | AutoLogEvent.__init__: self.onFirstContact (Contrib/autologEventManager.py:152); BarbarianCiv.__init__: self.onFirstContact (Revolution/Gameready/BarbarianCiv.py:89); CvEventManager.onFirstContact (base/CvEventManager.py:95) |
| goldenAge | CvDllPythonEvents::reportGoldenAge | AutoLogEvent.__init__: self.onGoldenAge (Contrib/autologEventManager.py:170); CvEventManager.onGoldenAge (base/CvEventManager.py:123) |
| goodyReceived | CvDllPythonEvents::reportGoodyReceived | BuildUnitName.__init__: self.onGoodyReceived (Contrib/UnitNameEventManager.py:192); AutoLogEvent.__init__: self.onGoodyReceived (Contrib/autologEventManager.py:160); CvEventManager.onGoodyReceived (base/CvEventManager.py:115) |
| gotoPlotSet | CvDllPythonEvents::reportGotoPlotSet | none registered |
| greatPersonBorn | CvDllPythonEvents::reportGreatPersonBorn | AutoLogEvent.__init__: self.onGreatPersonBorn (Contrib/autologEventManager.py:161); Tester.__init__: self.onGreatPersonBorn (Revolution/Development/Tester.py:42); CvEventManager.onGreatPersonBorn (base/CvEventManager.py:116) |
| improvementBuilt | CvDllPythonEvents::reportImprovementBuilt | AutoLogEvent.__init__: self.onImprovementBuilt (Contrib/autologEventManager.py:182); CvEventManager.onImprovementBuilt (base/CvEventManager.py:93) |
| improvementDestroyed | CvDllPythonEvents::reportImprovementDestroyed | AutoLogEvent.__init__: self.onImprovementDestroyed (Contrib/autologEventManager.py:183) |
| kbdEvent | CvDllPythonEvents::reportKbdEvent | BugEventManager.__init__: self.onKbdEvent (BUG/BugEventManager.py:189); StatusDumpEvent.__init__: self.onKbdEvent (Contrib/StatusDumpEventManager.py:44); BuildUnitName.__init__: self.onKbdEvent (Contrib/UnitNameEventManager.py:189); AutoLogEvent.__init__: self.onKbdEvent (Contrib/autologEventManager.py:145); ChangePlayer.__init__: self.onKbdEvent (Revolution/Development/ChangePlayer.py:40); Tester.__init__: self.onKbdEvent (Revolution/Development/Tester.py:47); AIAutoPlay.__init__: self.onKbdEvent (Revolution/Gameready/AIAutoPlay.py:85); BarbarianCiv.__init__: self.onKbdEvent (Revolution/Gameready/BarbarianCiv.py:95); DynamicCivNames.__init__: self.onKbdEvent (Revolution/Gameready/DynamicCivNames.py:43); Revolution.__init__: self.onKbdEvent (Revolution/Gameready/Revolution.py:184); RevolutionInit.__init__: self.onKbdEvent (Revolution/RevolutionInit.py:66); CvEventManager.onKbdEvent (base/CvEventManager.py:75) |
| mouseEvent | CvDllPythonEvents::reportMouseEvent | CvEventManager.onMouseEvent (base/CvEventManager.py:74) |
| nukeExplosion | CvDllPythonEvents::reportNukeExplosion | none registered |
| playerChangeStateReligion | CvDllPythonEvents::reportPlayerChangeStateReligion | none registered |
| playerGoldTrade | CvDllPythonEvents::reportPlayerGoldTrade | none registered |
| playerRevolution | CvDllPythonEvents::reportPlayerRevolution | none registered |
| plotFeatureRemoved | CvDllPythonEvents::reportPlotFeatureRemoved | none registered |
| plotPicked | CvDllPythonEvents::reportPlotPicked | none registered |
| plotRevealed | CvDllPythonEvents::reportPlotRevealed | EventSignsEventHandler.__init__: self.onPlotRevealed (Contrib/EventSigns.py:453); CvEventManager.onPlotRevealed (base/CvEventManager.py:84) |
| projectBuilt | CvDllPythonEvents::reportProjectBuilt | AutoLogEvent.__init__: self.onProjectBuilt (Contrib/autologEventManager.py:157); RoMEventManager.__init__: self.onProjectBuilt (RoMEventManager.py:48); CvEventManager.onProjectBuilt (base/CvEventManager.py:118) |
| religionFounded | CvDllPythonEvents::reportReligionFounded | AutoLogEvent.__init__: self.onReligionFounded (Contrib/autologEventManager.py:164); Tester.__init__: self.onReligionFounded (Revolution/Development/Tester.py:44); init: onReligionFounded (Revolution/RevEvents.py:83); CvEventManager.onReligionFounded (base/CvEventManager.py:121) |
| religionRemove | CvDllPythonEvents::reportReligionRemove | AutoLogEvent.__init__: self.onReligionRemove (Contrib/autologEventManager.py:166) |
| religionSpread | CvDllPythonEvents::reportReligionSpread | AutoLogEvent.__init__: self.onReligionSpread (Contrib/autologEventManager.py:165); CvEventManager.onReligionSpread (base/CvEventManager.py:122) |
| routeBuilt | CvDllPythonEvents::reportRouteBuilt | CvEventManager.onRouteBuilt (base/CvEventManager.py:94) |
| selectionGroupPushMission | CvDllPythonEvents::reportSelectionGroupPushMission | AutoLogEvent.__init__: self.onSelectionGroupPushMission (Contrib/autologEventManager.py:186) |
| setPlayerAlive | CvDllPythonEvents::reportSetPlayerAlive | AutoLogEvent.__init__: self.onSetPlayerAlive (Contrib/autologEventManager.py:173); BarbarianCiv.__init__: self.onSetPlayerAlive (Revolution/Gameready/BarbarianCiv.py:90); DynamicCivNames.__init__: self.onSetPlayerAlive (Revolution/Gameready/DynamicCivNames.py:42); init: onSetPlayerAlive (Revolution/Gameready/StartAsMinors.py:52); init: onSetPlayerAlive (Revolution/RevEvents.py:81); CvEventManager.onSetPlayerAlive (base/CvEventManager.py:128) |
| techAcquired | CvDllPythonEvents::reportTechAcquired | AutoLogEvent.__init__: self.onTechAcquired (Contrib/autologEventManager.py:162); init: onTechAcquired (Revolution/Gameready/StartAsMinors.py:53); TechDiffusion.__init__: self.onTechAcquired (Revolution/Gameready/TechDiffusion.py:43); CvEventManager.onTechAcquired (base/CvEventManager.py:119) |
| techSelected | CvDllPythonEvents::reportTechSelected | AutoLogEvent.__init__: self.onTechSelected (Contrib/autologEventManager.py:163); CvEventManager.onTechSelected (base/CvEventManager.py:120) |
| unitBuildImprovement | CvDllPythonEvents::reportUnitBuildImprovement | none registered |
| unitBuilt | CvDllPythonEvents::reportUnitBuilt | BuildUnitName.__init__: self.onUnitBuilt (Contrib/UnitNameEventManager.py:190); AutoLogEvent.__init__: self.onUnitBuilt (Contrib/autologEventManager.py:158); RoMEventManager.__init__: self.onUnitBuilt (RoMEventManager.py:49); CvEventManager.onUnitBuilt (base/CvEventManager.py:109) |
| unitCaptured | CvDllPythonEvents::reportUnitCaptured | none registered |
| unitCreated | CvDllPythonEvents::reportUnitCreated | CvEventManager.onUnitCreated (base/CvEventManager.py:108) |
| unitGifted | CvDllPythonEvents::reportUnitGifted | none registered |
| unitKilled | CvDllPythonEvents::reportUnitKilled | CvEventManager.onUnitKilled (base/CvEventManager.py:110) |
| unitLost | CvDllPythonEvents::reportUnitLost | CvEventManager.onUnitLost (base/CvEventManager.py:111) |
| unitMove | CvDllPythonEvents::reportUnitMove | CvEventManager.onUnitMove (base/CvEventManager.py:106) |
| unitPillage | CvDllPythonEvents::reportUnitPillage | AutoLogEvent.__init__: self.onUnitPillage (Contrib/autologEventManager.py:184) |
| unitPromoted | CvDllPythonEvents::reportUnitPromoted | AutoLogEvent.__init__: self.onUnitPromoted (Contrib/autologEventManager.py:159); CvEventManager.onUnitPromoted (base/CvEventManager.py:112) |
| unitSelected | CvDllPythonEvents::reportUnitSelected | CvEventManager.onUnitSelected (base/CvEventManager.py:113) |
| unitSetXY | CvDllPythonEvents::reportUnitSetXY | CvEventManager.onUnitSetXY (base/CvEventManager.py:107) |
| unitSpreadReligionAttempt | CvDllPythonEvents::reportUnitSpreadReligionAttempt | none registered |
| unitUpgraded | CvDllPythonEvents::reportUnitUpgraded | none registered |
| vassalState | CvDllPythonEvents::reportVassalState | AutoLogEvent.__init__: self.onVassalState (Contrib/autologEventManager.py:185); DynamicCivNames.__init__: self.onVassalState (Revolution/Gameready/DynamicCivNames.py:46) |
| victory | CvDllPythonEvents::reportVictory | AIAutoPlay.__init__: self.onVictory (Revolution/Gameready/AIAutoPlay.py:98); CvEventManager.onVictory (base/CvEventManager.py:126) |
| windowActivation | CvDllPythonEvents::reportWindowActivation | CvEnhancedTechConquestEventManager.__init__: self.onWindowActivation (EnhancedTechConquestUtils/CvEnhancedTechConquestEventManager.py:19); CvEventManager.onWindowActivation (base/CvEventManager.py:129) |
