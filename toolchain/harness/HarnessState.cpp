// Harness-only: a JSON snapshot of every player's economy, cities and
// settlers, for checking what the AI builds, researches and settles.
// Nothing here changes game logic.
#include "CvGameCoreDLL.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvUnit.h"
#include "CvCity.h"
#include "CvCityAI.h"
#include <algorithm>
#include <vector>
#include "CvInfos.h"
#include <cstdio>
#include <string>
#include <sstream>
#include <cstdlib>

namespace
{
	const char* orderName(const OrderData& d)
	{
		switch (d.eOrderType)
		{
		case ORDER_TRAIN: return d.iData1 >= 0 ? GC.getUnitInfo((UnitTypes)d.iData1).getType() : "?";
		case ORDER_CONSTRUCT: return d.iData1 >= 0 ? GC.getBuildingInfo((BuildingTypes)d.iData1).getType() : "?";
		case ORDER_CREATE: return d.iData1 >= 0 ? GC.getProjectInfo((ProjectTypes)d.iData1).getType() : "?";
		case ORDER_MAINTAIN: return d.iData1 >= 0 ? GC.getProcessInfo((ProcessTypes)d.iData1).getType() : "?";
		default: return "-";
		}
	}
}

extern "C" __declspec(dllexport) int HH_dumpState(const char* szPath)
{
	FILE* f = fopen(szPath, "w");
	if (f == NULL) return -1;
	CvGame& g = GC.getGameINLINE();
	fprintf(f, "{\"turn\":%d,\"year\":%d,\"players\":[", g.getGameTurn(), g.getGameTurnYear());
	bool bFirstPlayer = true;
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		CvPlayerAI& k = GET_PLAYER((PlayerTypes)i);
		if (!k.isAlive()) continue;
		CvTeamAI& kT = GET_TEAM(k.getTeam());
		fprintf(f, "%s\n{\"id\":%d,\"leader\":\"%s\",\"human\":%d,\"gold\":%d,\"goldRate\":%d,\"researchRate\":%d,\"cultureRate\":%d,"
			"\"research\":\"%s\",\"agenda\":%d,\"vic\":%d,\"era\":%d,",
			bFirstPlayer ? "" : ",", i, GC.getLeaderHeadInfo(k.getLeaderType()).getType(), k.isHuman() ? 1 : 0, k.getGold(),
			k.getCommerceRate(COMMERCE_GOLD), k.getCommerceRate(COMMERCE_RESEARCH), k.getCommerceRate(COMMERCE_CULTURE),
			k.getCurrentResearch() != NO_TECH ? GC.getTechInfo(k.getCurrentResearch()).getType() : "-",
			(int)k.AI_getAgenda(), k.AI_getVictoryStrategyHash(), (int)k.getCurrentEra());
		bFirstPlayer = false;
		int iCommerceTotal = 0;
		for (int c = 0; c < NUM_COMMERCE_TYPES; ++c) iCommerceTotal += k.getCommerceRate((CommerceTypes)c);
		fprintf(f, "\"econ\":{\"pct\":[%d,%d,%d,%d],\"flex\":[%d,%d,%d,%d],\"goldTarget\":%d,\"extraGoldTarget\":%d,"
			"\"commerce\":%d,\"calcGold\":%d,\"calcResearch\":%d,\"costs\":%d,\"anarchy\":%d,\"avoidScience\":%d,"
			"\"finTrouble\":%d,\"wars\":%d,\"chosenWars\":%d,\"cities\":%d},",
			k.getCommercePercent(COMMERCE_GOLD), k.getCommercePercent(COMMERCE_RESEARCH), k.getCommercePercent(COMMERCE_CULTURE),
			k.getCommercePercent(COMMERCE_ESPIONAGE), k.isCommerceFlexible(COMMERCE_GOLD) ? 1 : 0, k.isCommerceFlexible(COMMERCE_RESEARCH) ? 1 : 0,
			k.isCommerceFlexible(COMMERCE_CULTURE) ? 1 : 0, k.isCommerceFlexible(COMMERCE_ESPIONAGE) ? 1 : 0,
			k.isHuman() ? -1 : k.AI_goldTarget(), k.AI_getExtraGoldTarget(), iCommerceTotal, k.calculateGoldRate(), k.calculateResearchRate(),
			k.calculateInflatedCosts(), k.isAnarchy() ? 1 : 0, k.AI_avoidScience() ? 1 : 0, k.AI_isFinancialTrouble() ? 1 : 0,
			kT.getAtWarCount(true), kT.getChosenWarCount(true), k.getNumCities());
		fprintf(f, "\"techs\":[");
		bool bFirst = true;
		for (int t = 0; t < GC.getNumTechInfos(); ++t)
		{
			if (!kT.isHasTech((TechTypes)t)) continue;
			fprintf(f, "%s\"%s\"", bFirst ? "" : ",", GC.getTechInfo((TechTypes)t).getType());
			bFirst = false;
		}
		fprintf(f, "],\"civics\":[");
		bFirst = true;
		for (int o = 0; o < GC.getNumCivicOptionInfos(); ++o)
		{
			const CivicTypes eCivic = k.getCivics((CivicOptionTypes)o);
			fprintf(f, "%s\"%s\"", bFirst ? "" : ",", eCivic != NO_CIVIC ? GC.getCivicInfo(eCivic).getType() : "-");
			bFirst = false;
		}
		fprintf(f, "],\"cities\":[");
		int iLoop;
		bFirst = true;
		for (CvCity* c = k.firstCity(&iLoop); c != NULL; c = k.nextCity(&iLoop))
		{
			const CLLNode<OrderData>* o = c->headOrderQueueNode();
			fprintf(f, "%s\n {\"x\":%d,\"y\":%d,\"pop\":%d,\"founded\":%d,\"happy\":%d,\"unhappy\":%d,\"good\":%d,\"bad\":%d,\"food\":%d,"
				"\"prod\":%d,\"commerce\":%d,\"culture\":%d,\"order\":\"%s\",\"orderTurns\":%d,\"buildings\":[",
				bFirst ? "" : ",", c->getX_INLINE(), c->getY_INLINE(), c->getPopulation(), c->getGameTurnFounded(),
				c->happyLevel(), c->unhappyLevel(), c->goodHealth(), c->badHealth(), c->foodDifference(),
				c->getYieldRate(YIELD_PRODUCTION), c->getYieldRate(YIELD_COMMERCE), c->getCommerceRate(COMMERCE_CULTURE),
				o != NULL ? orderName(o->m_data) : "-", o != NULL ? c->getProductionTurnsLeft() : -1);
			bFirst = false;
			bool bFirstB = true;
			for (int b = 0; b < GC.getNumBuildingInfos(); ++b)
			{
				if (c->getNumRealBuilding((BuildingTypes)b) <= 0) continue;
				fprintf(f, "%s\"%s\"", bFirstB ? "" : ",", GC.getBuildingInfo((BuildingTypes)b).getType());
				bFirstB = false;
			}
			fprintf(f, "]");
			if (getenv("HARNESS_VALUE_DIAG") != NULL && !k.isHuman())
			{
				// The city AI's own building values (AI_buildingValue draws no
				// random numbers and changes nothing), best first.
				std::vector<std::pair<int, int> > aValues;
				for (int b = 0; b < GC.getNumBuildingInfos(); ++b)
				{
					if (!c->canConstruct((BuildingTypes)b)) continue;
					aValues.push_back(std::make_pair(-static_cast<CvCityAI*>(c)->AI_buildingValue((BuildingTypes)b), b));
				}
				std::sort(aValues.begin(), aValues.end());
				fprintf(f, ",\"bv\":[");
				for (size_t v = 0; v < aValues.size() && v < 12; ++v)
				{
					const BuildingTypes eB = (BuildingTypes)aValues[v].second;
					fprintf(f, "%s[\"%s\",%d,%d,%d]", v ? "," : "", GC.getBuildingInfo(eB).getType(), -aValues[v].first,
						c->getProductionNeeded(eB), c->getProductionTurnsLeft(eB, 0));
				}
				fprintf(f, "]");
			}
			fprintf(f, "}");
		}
		fprintf(f, "],\"units\":{");
		std::map<std::string, int> aiCount;
		for (CvUnit* u = k.firstUnit(&iLoop); u != NULL; u = k.nextUnit(&iLoop))
		{
			CvWString w;
			getUnitAIString(w, u->AI_getUnitAIType());
			aiCount[CvString(w).GetCString()]++;
		}
		bFirst = true;
		for (std::map<std::string, int>::const_iterator it = aiCount.begin(); it != aiCount.end(); ++it)
		{
			fprintf(f, "%s\"%s\":%d", bFirst ? "" : ",", it->first.c_str(), it->second);
			bFirst = false;
		}
		fprintf(f, "},\"settlers\":[");
		bFirst = true;
		for (CvUnit* u = k.firstUnit(&iLoop); u != NULL; u = k.nextUnit(&iLoop))
		{
			if (u->AI_getUnitAIType() != UNITAI_SETTLE) continue;
			CvSelectionGroup* pGroup = u->getGroup();
			CvPlot* pTarget = pGroup ? pGroup->AI_getMissionAIPlot() : NULL;
			fprintf(f, "%s{\"x\":%d,\"y\":%d,\"age\":%d,\"groupUnits\":%d,\"missionAI\":%d,\"tx\":%d,\"ty\":%d,\"cargo\":%d,\"inCity\":%d",
				bFirst ? "" : ",", u->getX_INLINE(), u->getY_INLINE(), g.getGameTurn() - u->getGameTurnCreated(),
				pGroup ? pGroup->getNumUnits() : 0, pGroup ? (int)pGroup->AI_getMissionAIType() : -2,
				pTarget ? pTarget->getX_INLINE() : -1, pTarget ? pTarget->getY_INLINE() : -1,
				u->isCargo() ? 1 : 0, u->plot()->isCity() ? 1 : 0);
			bFirst = false;
			if (getenv("HARNESS_SETTLER_DIAG") != NULL && pGroup != NULL)
			{
				// The filters AI_found applies, per candidate, for this settler
				// (path searches only: no game state changes).
				fprintf(f, ",\"id\":%d,\"canDefend\":%d,\"horizon\":%d,\"minFound\":%d,\"area\":%d,\"cands\":[",
					u->getID(), pGroup->canDefend() ? 1 : 0, k.AI_getExpansionHorizon(), k.AI_getMinFoundValue(), u->getArea());
				const int iCands = k.AI_getNumSettlementCandidates();
				for (int c = 0; c < iCands && c < 8; ++c)
				{
					int iFound;
					CvPlot* p = k.AI_getSettlementCandidate(c, iFound);
					int iTurns = -1;
					const bool bPath = p->getArea() == u->getArea() && u->generatePath(p, MOVE_SAFE_TERRITORY, false, &iTurns);
					int iTurnsAny = -1;
					const bool bPathAny = p->getArea() == u->getArea() && u->generatePath(p, 0, false, &iTurnsAny);
					fprintf(f, "%s{\"x\":%d,\"y\":%d,\"v\":%d,\"area\":%d,\"canFound\":%d,\"enemy\":%d,\"otherFound\":%d,\"guard\":%d,"
						"\"owner\":%d,\"reach\":%d,\"path\":%d,\"turns\":%d,\"pathAny\":%d,\"turnsAny\":%d}",
						c ? "," : "", p->getX_INLINE(), p->getY_INLINE(), iFound, p->getArea(), u->canFound(p) ? 1 : 0,
						p->isVisibleEnemyUnit(u) ? 1 : 0,
						k.AI_plotTargetMissionAIs(p, MISSIONAI_FOUND, pGroup, GC.getMIN_CITY_RANGE()),
						k.AI_plotTargetMissionAIs(p, MISSIONAI_GUARD_CITY), (int)p->getOwnerINLINE(), (k.AI_canDeliverSettler(u->plot(), p) ? 1 : 0) + (k.AI_isSettleSiteDeliverable(p) ? 2 : 0),
						bPath ? 1 : 0, bPath ? iTurns : -1, bPathAny ? 1 : 0, bPathAny ? iTurnsAny : -1);
				}
				fprintf(f, "]");
				// Where a land-reachable site has no MOVE_SAFE_TERRITORY path: the
				// plots of the settler's land region the path search cannot reach
				// although a neighbour in the region can be reached.
				bool bProbe = false;
				for (int c = 0; c < iCands && c < 8 && !bProbe; ++c)
				{
					int iFound; bool bByLand = false;
					CvPlot* p = k.AI_getSettlementCandidate(c, iFound);
					int iTurns;
					bProbe = k.AI_canDeliverSettler(u->plot(), p, &bByLand) && bByLand && !u->plot()->isWater() &&
						!u->generatePath(p, MOVE_SAFE_TERRITORY, false, &iTurns);
				}
				if (bProbe)
				{
					fprintf(f, ",\"frontier\":[");
					int iOut = 0;
					CvMap& kMap = GC.getMapINLINE();
					std::vector<char> abOk(kMap.numPlotsINLINE(), 0), abIn(kMap.numPlotsINLINE(), 0);
					for (int i = 0; i < kMap.numPlotsINLINE(); ++i)
					{
						CvPlot* q = kMap.plotByIndexINLINE(i);
						bool bByLand = false;
						if (q->isWater() || !k.AI_canDeliverSettler(u->plot(), q, &bByLand) || !bByLand) continue;
						abIn[i] = 1;
						int iTurns;
						abOk[i] = u->generatePath(q, MOVE_SAFE_TERRITORY, true, &iTurns) ? 1 : 0;
					}
					for (int i = 0; i < kMap.numPlotsINLINE() && iOut < 12; ++i)
					{
						if (!abIn[i] || abOk[i]) continue;
						CvPlot* q = kMap.plotByIndexINLINE(i);
						bool bEdge = false;
						for (int d = 0; d < NUM_DIRECTION_TYPES && !bEdge; ++d)
						{
							CvPlot* a = plotDirection(q->getX_INLINE(), q->getY_INLINE(), (DirectionTypes)d);
							bEdge = a != NULL && abOk[GC.getMapINLINE().plotNumINLINE(a->getX_INLINE(), a->getY_INLINE())];
						}
						if (!bEdge) continue;
						fprintf(f, "%s{\"x\":%d,\"y\":%d,\"owner\":%d,\"terrain\":\"%s\",\"feature\":\"%s\",\"impassable\":%d,"
							"\"units\":%d,\"enemy\":%d,\"canEnter\":%d,\"danger\":%d,\"area\":%d}",
							iOut ? "," : "", q->getX_INLINE(), q->getY_INLINE(), (int)q->getOwnerINLINE(),
							GC.getTerrainInfo(q->getTerrainType()).getType(),
							q->getFeatureType() != NO_FEATURE ? GC.getFeatureInfo(q->getFeatureType()).getType() : "-",
							q->isImpassable() ? 1 : 0, q->getNumUnits(), q->isVisibleEnemyUnit(u) ? 1 : 0,
							u->canMoveInto(q) ? 1 : 0, k.AI_getAnyPlotDanger(q) ? 1 : 0, q->getArea());
						++iOut;
					}
					fprintf(f, "]");
				}
				CvUnit* pTr = u->getTransportUnit();
				if (pTr != NULL)
				{
					CvSelectionGroup* pTrGroup = pTr->getGroup();
					CvPlot* pTrTarget = pTrGroup->AI_getMissionAIPlot();
					CvWString w;
					getUnitAIString(w, pTr->AI_getUnitAIType());
					fprintf(f, ",\"tr\":{\"id\":%d,\"type\":\"%s\",\"ai\":\"%s\",\"x\":%d,\"y\":%d,\"missionAI\":%d,\"tx\":%d,\"ty\":%d,"
						"\"queue\":%d,\"activity\":%d,\"cargo\":%d,\"groupUnits\":%d,\"moves\":%d,\"damage\":%d,\"age\":%d}",
						pTr->getID(), GC.getUnitInfo(pTr->getUnitType()).getType(), CvString(w).GetCString(), pTr->getX_INLINE(), pTr->getY_INLINE(),
						(int)pTrGroup->AI_getMissionAIType(), pTrTarget ? pTrTarget->getX_INLINE() : -1, pTrTarget ? pTrTarget->getY_INLINE() : -1,
						pTrGroup->getLengthMissionQueue(), (int)pTrGroup->getActivityType(), pTr->getCargo(), pTrGroup->getNumUnits(),
						pTr->maxMoves(), pTr->getDamage(), g.getGameTurn() - pTr->getGameTurnCreated());
				}
			}
			fprintf(f, "}");
		}
		fprintf(f, "]}");
	}
	fprintf(f, "\n]}\n");
	fclose(f);
	return 0;
}
