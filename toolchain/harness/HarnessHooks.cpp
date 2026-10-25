// Harness-only entry points, compiled into CvGameCoreDLL builds used by the
// headless harness. The real engine reaches these functions through Python
// (CyMap, CyPlayer, ...); the harness has no Python, so they are exported here.
// Nothing in this file changes game logic.
#include "CvGameCoreDLL.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvUnit.h"
#include "CvCity.h"
#include "CvSelectionGroup.h"
#include "CvInfos.h"
#include "CvInitCore.h"
#include "CvDLLFAStarIFaceBase.h"
#include "FAStarNode.h"
#include "CvGameCoreUtils.h"
#include <cstdio>

extern "C" __declspec(dllexport) int HH_type(const char* szType)
{
	return GC.getInfoTypeForString(szType);
}

extern "C" __declspec(dllexport) void HH_setPlot(int iX, int iY, int ePlotType, int eTerrain)
{
	CvPlot* pPlot = GC.getMapINLINE().plotINLINE(iX, iY);
	pPlot->setPlotType((PlotTypes)ePlotType, false, false);
	pPlot->setTerrainType((TerrainTypes)eTerrain, false, false);
}

extern "C" __declspec(dllexport) void HH_finishMap()
{
	GC.getMapINLINE().recalculateAreas();
}

extern "C" __declspec(dllexport) void HH_revealAll(int eTeam)
{
	GC.getMapINLINE().setRevealedPlots((TeamTypes)eTeam, true);
}

extern "C" __declspec(dllexport) void HH_setTech(int eTeam, int eTech)
{
	GET_TEAM((TeamTypes)eTeam).setHasTech((TechTypes)eTech, true, NO_PLAYER, false, false);
}

extern "C" __declspec(dllexport) int HH_initCity(int ePlayer, int iX, int iY)
{
	CvCity* pCity = GET_PLAYER((PlayerTypes)ePlayer).initCity(iX, iY, true, true);
	return pCity ? pCity->getID() : -1;
}

extern "C" __declspec(dllexport) int HH_initUnit(int ePlayer, int eUnit, int iX, int iY, int eUnitAI)
{
	CvUnit* pUnit = GET_PLAYER((PlayerTypes)ePlayer).initUnit((UnitTypes)eUnit, iX, iY, (UnitAITypes)eUnitAI);
	return pUnit ? pUnit->getID() : -1;
}

// One line per unit and city: enough to follow a voyage turn by turn.
extern "C" __declspec(dllexport) int HH_snapshot(int ePlayer, char* szBuf, int iSize)
{
	CvPlayerAI& kPlayer = GET_PLAYER((PlayerTypes)ePlayer);
	int iLen = 0;
	int iLoop;
	for (CvCity* pCity = kPlayer.firstCity(&iLoop); pCity != NULL; pCity = kPlayer.nextCity(&iLoop))
	{
		iLen += _snprintf(szBuf + iLen, iSize - iLen, "  city %d at %d,%d pop %d area %d\n",
			pCity->getID(), pCity->getX_INLINE(), pCity->getY_INLINE(), pCity->getPopulation(), pCity->getArea());
		if (iLen >= iSize) return iSize;
	}
	for (CvUnit* pUnit = kPlayer.firstUnit(&iLoop); pUnit != NULL; pUnit = kPlayer.nextUnit(&iLoop))
	{
		CvSelectionGroup* pGroup = pUnit->getGroup();
		CvPlot* pMissionPlot = pGroup ? pGroup->AI_getMissionAIPlot() : NULL;
		CvUnit* pTransport = pUnit->getTransportUnit();
		iLen += _snprintf(szBuf + iLen, iSize - iLen,
			"  unit %d %s ai %d at %d,%d moves %d/%d group %d (%d units, head %d) missionAI %d -> %d,%d cargo %d transport %d activity %d\n",
			pUnit->getID(), GC.getUnitInfo(pUnit->getUnitType()).getType(), pUnit->AI_getUnitAIType(),
			pUnit->getX_INLINE(), pUnit->getY_INLINE(), pUnit->getMoves(), pUnit->maxMoves(),
			pUnit->getGroupID(), pGroup ? pGroup->getNumUnits() : 0,
			(pGroup && pGroup->getHeadUnit()) ? pGroup->getHeadUnit()->getID() : -1,
			pGroup ? (int)pGroup->AI_getMissionAIType() : -2,
			pMissionPlot ? pMissionPlot->getX_INLINE() : -1, pMissionPlot ? pMissionPlot->getY_INLINE() : -1,
			pUnit->getCargo(), pTransport ? pTransport->getID() : -1,
			pGroup ? (int)pGroup->getActivityType() : -2);
		if (iLen >= iSize) return iSize;
	}
	return iLen;
}

// New single-player game with AI players only. aszCivs/aszLeaders name each
// civ player's civilization and leader; everyone else's slot is closed.
extern "C" __declspec(dllexport) void HH_newGame(int iW, int iH, int iNumCivs, const char** aszCivs,
	const char** aszLeaders, const char* szHandicap, const char* szSpeed, const char* szEra, const char** aszOptions, int iNumOptions,
	unsigned int uiSeed)
{
	CvInitCore& kInit = GC.getInitCore();
	kInit.init(GAMEMODE_NORMAL);   // clears slots, applies default game options
	kInit.setType(GAME_SP_NEW);
	kInit.setMode(GAMEMODE_NORMAL);
	kInit.setWorldSize((WorldSizeTypes)GC.getInfoTypeForString("WORLDSIZE_SMALL"));
	kInit.setClimate((ClimateTypes)0);
	kInit.setSeaLevel((SeaLevelTypes)GC.getInfoTypeForString("SEALEVEL_MEDIUM"));
	kInit.setEra((EraTypes)GC.getInfoTypeForString(szEra));
	kInit.setGameSpeed((GameSpeedTypes)GC.getInfoTypeForString(szSpeed));
	kInit.setCalendar((CalendarTypes)0);
	kInit.setSyncRandSeed(uiSeed);
	kInit.setMapRandSeed(uiSeed);
	for (int i = 0; i < iNumOptions; ++i) kInit.setOption((GameOptionTypes)GC.getInfoTypeForString(aszOptions[i]), true);
	const HandicapTypes eHandicap = (HandicapTypes)GC.getInfoTypeForString(szHandicap);
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		const PlayerTypes eP = (PlayerTypes)i;
		if (i < iNumCivs)
		{
			kInit.setSlotStatus(eP, SS_COMPUTER);
			kInit.setSlotClaim(eP, SLOTCLAIM_ASSIGNED);
			kInit.setCiv(eP, (CivilizationTypes)GC.getInfoTypeForString(aszCivs[i]));
			kInit.setLeader(eP, (LeaderHeadTypes)GC.getInfoTypeForString(aszLeaders[i]));
			kInit.setTeam(eP, (TeamTypes)i);
			kInit.setHandicap(eP, eHandicap);
			kInit.setColor(eP, (PlayerColorTypes)GC.getCivilizationInfo(kInit.getCiv(eP)).getDefaultPlayerColor());
		}
		else
		{
			kInit.setSlotStatus(eP, SS_CLOSED);
		}
	}
	// The engine fills the barbarian slot itself during game setup.
	kInit.setSlotStatus(BARBARIAN_PLAYER, SS_COMPUTER);
	kInit.setCiv(BARBARIAN_PLAYER, (CivilizationTypes)GC.getDefineINT("BARBARIAN_CIVILIZATION"));
	kInit.setLeader(BARBARIAN_PLAYER, (LeaderHeadTypes)GC.getDefineINT("BARBARIAN_LEADER"));
	kInit.setTeam(BARBARIAN_PLAYER, BARBARIAN_TEAM);
	kInit.setHandicap(BARBARIAN_PLAYER, (HandicapTypes)GC.getDefineINT("BARBARIAN_HANDICAP"));
	kInit.setColor(BARBARIAN_PLAYER, (PlayerColorTypes)GC.getCivilizationInfo(kInit.getCiv(BARBARIAN_PLAYER)).getDefaultPlayerColor());
	GC.getGameINLINE().init(eHandicap);
	CvMapInitData kMap(iW, iH, 60, -60, false, false);
	GC.getMapINLINE().init(&kMap);
}

extern "C" __declspec(dllexport) void HH_startGame(int eActivePlayer)
{
	for (int i = 0; i < MAX_TEAMS; ++i) GET_TEAM((TeamTypes)i).init((TeamTypes)i);
	for (int i = 0; i < MAX_PLAYERS; ++i) GET_PLAYER((PlayerTypes)i).init((PlayerTypes)i);
	GC.getGameINLINE().initDiplomacy();
	GC.getGameINLINE().initFreeState();
	GC.getGameINLINE().setActivePlayer((PlayerTypes)eActivePlayer, false);
}

extern "C" __declspec(dllexport) void HH_beginPlay()
{
	GC.getGameINLINE().initScoreCalculation();
	GC.getGameINLINE().setFinalInitialized(true);
}

extern "C" __declspec(dllexport) int HH_gameTurn() { return GC.getGameINLINE().getGameTurn(); }
extern "C" __declspec(dllexport) void HH_update() { GC.getGameINLINE().update(); }

// Graphics, as the executable sets them up after loading a game: plots, then each player's cities
// and units. HARNESS_DEFINES ("NAME=value,NAME=value") overrides integer defines first.
extern "C" __declspec(dllexport) void HH_setupGraphics()
{
	const char* szDefines = getenv("HARNESS_DEFINES");
	if (szDefines != NULL)
	{
		char szName[128];
		int iValue, iRead;
		for (const char* p = szDefines; sscanf(p, " %127[^=]=%d%n", szName, &iValue, &iRead) == 2; p += iRead + (p[iRead] == ',' ? 1 : 0))
		{
			GC.setDefineINT(szName, iValue);
			if (p[iRead] != ',') break;
		}
	}
	GC.SetGraphicsInitialized(true);
	GC.getMapINLINE().setupGraphical();
	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		if (GET_PLAYER((PlayerTypes)i).isAlive()) GET_PLAYER((PlayerTypes)i).setupGraphical();
	}
}

// The camera for HARNESS_GRAPHICS: a sweep of the map, one plot along a row every
// HARNESS_CAMERA_PERIOD calls (default 20), back and forth, rows 20 plots apart.
extern "C" __declspec(dllexport) CvPlot* HH_lookAtPlot()
{
	static long s_iCalls = 0;
	const char* szPeriod = getenv("HARNESS_CAMERA_PERIOD");
	const long iPeriod = std::max(1L, szPeriod != NULL ? atol(szPeriod) : 20L);
	CvMap& kMap = GC.getMapINLINE();
	const int iW = kMap.getGridWidthINLINE(), iH = kMap.getGridHeightINLINE();
	const long iStep = (s_iCalls++) / iPeriod;
	const int iRows = std::max(1, iH / 20);
	const int iRow = (int)((iStep / iW) % iRows);
	const int iX = (iRow % 2 == 0) ? (int)(iStep % iW) : iW - 1 - (int)(iStep % iW);
	return kMap.plotINLINE(iX, std::min(iH - 1, 10 + 20 * iRow));
}
extern "C" __declspec(dllexport) int HH_numCities(int ePlayer) { return GET_PLAYER((PlayerTypes)ePlayer).getNumCities(); }
extern "C" __declspec(dllexport) int HH_cityAt(int iX, int iY)
{
	CvCity* pCity = GC.getMapINLINE().plotINLINE(iX, iY)->getPlotCity();
	return pCity ? (int)pCity->getOwnerINLINE() : -1;
}

// Diagnostics: how the player's settlement candidates look to a given settler
// and ship (the checks AI_settlerSeaTransport applies, evaluated directly).
extern "C" __declspec(dllexport) int HH_debugSites(int ePlayer, int iSettlerID, int iShipID, char* szBuf, int iSize)
{
	CvPlayerAI& kPlayer = GET_PLAYER((PlayerTypes)ePlayer);
	CvUnit* pSettler = kPlayer.getUnit(iSettlerID);
	CvUnit* pShip = kPlayer.getUnit(iShipID);
	int iLen = _snprintf(szBuf, iSize, "  horizon %d, logistics %d, candidates %d, min found %d\n",
		kPlayer.AI_getExpansionHorizon(), kPlayer.AI_getLogisticsPriority(), kPlayer.AI_getNumSettlementCandidates(),
		kPlayer.AI_getMinFoundValue());
	for (int i = 0; i < kPlayer.AI_getNumSettlementCandidates() && iLen < iSize; ++i)
	{
		int iFound;
		CvPlot* p = kPlayer.AI_getSettlementCandidate(i, iFound);
		int iBestSail = -1;
		if (pShip != NULL)
		{
			for (int d = 0; d < NUM_DIRECTION_TYPES; ++d)
			{
				CvPlot* a = plotDirection(p->getX_INLINE(), p->getY_INLINE(), (DirectionTypes)d);
				int iTurns;
				if (a && a->isWater() && pShip->getGroup()->generatePath(pShip->plot(), a, MOVE_NO_ENEMY_TERRITORY, false, &iTurns) &&
					(iBestSail < 0 || iTurns < iBestSail)) iBestSail = iTurns;
			}
		}
		iLen += _snprintf(szBuf + iLen, iSize - iLen,
			"  site %d,%d found %d area %d coastal %d canFound %d settlerCanEnter %d targeted %d sail %d\n",
			p->getX_INLINE(), p->getY_INLINE(), iFound, p->getArea(), p->isCoastalLand(),
			pSettler ? pSettler->canFound(p) : -1, pSettler ? pSettler->canMoveInto(p) : -1,
			kPlayer.AI_plotTargetMissionAIs(p, MISSIONAI_FOUND, NULL, GC.getMIN_CITY_RANGE()), iBestSail);
	}
	return std::min(iLen, iSize);
}

extern "C" __declspec(dllexport) int HH_probePath(int ePlayer, int iUnitID, int iX, int iY, char* szBuf, int iSize)
{
	CvUnit* pUnit = GET_PLAYER((PlayerTypes)ePlayer).getUnit(iUnitID);
	CvPlot* pTo = GC.getMapINLINE().plotINLINE(iX, iY);
	int iTurns = -1;
	const bool bPath = pUnit->getGroup()->generatePath(pUnit->plot(), pTo, 0, false, &iTurns);
	const int iDest = pathDestValid(iX, iY, pUnit->getGroup(), &GC.getPathFinder());
	FAStarNode* pLast = gDLL->getFAStarIFace()->GetLastNode(&GC.getPathFinder());
	return _snprintf(szBuf, iSize, "  probe unit %d (%d,%d)->(%d,%d): canMoveInto %d destValid %d path %d turns %d last %p water %d area %d->%d domain %d\n",
		iUnitID, pUnit->getX_INLINE(), pUnit->getY_INLINE(), iX, iY, pUnit->canMoveInto(pTo), iDest, bPath, iTurns, pLast,
		pTo->isWater(), pUnit->plot()->getArea(), pTo->getArea(), (int)pUnit->getDomainType());
}

extern "C" __declspec(dllexport) void HH_setGold(int ePlayer, int iGold)
{
	GET_PLAYER((PlayerTypes)ePlayer).setGold(iGold);
}

extern "C" __declspec(dllexport) void HH_setCityPopulation(int iX, int iY, int iPop)
{
	CvCity* pCity = GC.getMapINLINE().plotINLINE(iX, iY)->getPlotCity();
	if (pCity != NULL) pCity->setPopulation(iPop);
}

extern "C" __declspec(dllexport) int HH_economy(int ePlayer, char* szBuf, int iSize)
{
	CvPlayerAI& k = GET_PLAYER((PlayerTypes)ePlayer);
	int iLoop;
	int iWorked = 0, iPop = 0;
	for (CvCity* c = k.firstCity(&iLoop); c != NULL; c = k.nextCity(&iLoop)) { iWorked += c->getWorkingPopulation(); iPop += c->getPopulation(); }
	return _snprintf(szBuf, iSize,
		"  economy: gold %d, gold rate %d, research rate %d, gold/turn %d, %%gold %d %%research %d, inflated costs %d (units %d, supply %d, maintenance %d, civics %d), pop %d worked %d, trouble %d\n",
		k.getGold(), k.getCommerceRate(COMMERCE_GOLD), k.getCommerceRate(COMMERCE_RESEARCH), k.getGoldPerTurn(),
		k.getCommercePercent(COMMERCE_GOLD), k.getCommercePercent(COMMERCE_RESEARCH), k.calculateInflatedCosts(),
		k.calculateUnitCost(), k.calculateUnitSupply(), k.getTotalMaintenance(), k.getCivicUpkeep(),
		iPop, iWorked, k.AI_isFinancialTrouble());
}
