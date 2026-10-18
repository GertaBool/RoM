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
#include "HarnessPeek.h"
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

	// Replay text and the like: plain ASCII inside a JSON string.
	void writeJsonText(FILE* f, const wchar_t* sz)
	{
		fputc('"', f);
		for (; sz != NULL && *sz != 0; ++sz)
		{
			const wchar_t ch = *sz;
			if (ch == L'"' || ch == L'\\') { fputc('\\', f); fputc((char)ch, f); }
			else if (ch >= 32 && ch < 127) fputc((char)ch, f);
			else fputc(' ', f);
		}
		fputc('"', f);
	}
}

// Settlement delivery regions exist from patch 0012 on; build_dll.sh defines
// HARNESS_SETTLE_REACH when the source has them, so older sources still build.
#ifdef HARNESS_SETTLE_REACH
#define HH_SETTLE_REACH(k, u, p) ((k).AI_canDeliverSettler((u)->plot(), (p)) ? 1 : 0) + ((k).AI_isSettleSiteDeliverable(p) ? 2 : 0)
#else
#define HH_SETTLE_REACH(k, u, p) (-1)
#endif

// Totals of one player after a full recalculation: commerce, research, gold per turn, food, hammers.
static void HH_totals(CvPlayer& k, int* aiOut)
{
	k.updateMaintenance(); k.updateTradeRoutes(); k.updateYield(); k.updateCommerce();
	aiOut[0] = k.calculateTotalCommerce(); aiOut[1] = k.calculateResearchRate(); aiOut[2] = k.calculateGoldRate();
	aiOut[3] = k.calculateTotalYield(YIELD_FOOD); aiOut[4] = k.calculateTotalYield(YIELD_PRODUCTION);
}

// Civic probe: for every civic option of ePlayer and every civic it could adopt there, the totals with
// that civic in place of the current one (worked tiles unchanged), then the civic put back; the
// baseline is measured again after each swap ("restored" is 1 when it came back exactly).
// Tech values: for every AI, AI_techValue (path 1) of every tech it can research now.
static void HH_probe(const char* szPath, PlayerTypes ePlayer)
{
	FILE* f = fopen(szPath, "w");
	if (f == NULL) return;
	CvPlayerAI& k = GET_PLAYER(ePlayer);
	int aiBase[5], aiNow[5], aiBack[5];
	HH_totals(k, aiBase);
	fprintf(f, "{\"player\":%d,\"baseline\":[%d,%d,%d,%d,%d],\"civics\":[", (int)ePlayer, aiBase[0], aiBase[1], aiBase[2], aiBase[3], aiBase[4]);
	bool bFirst = true;
	for (int iO = 0; iO < GC.getNumCivicOptionInfos(); ++iO)
	{
		const CivicOptionTypes eO = (CivicOptionTypes)iO;
		const CivicTypes eCur = k.getCivics(eO);
		for (int iC = 0; iC < GC.getNumCivicInfos(); ++iC)
		{
			const CivicTypes eC = (CivicTypes)iC;
			if (GC.getCivicInfo(eC).getCivicOptionType() != iO || eC == eCur || !k.canDoCivics(eC)) continue;
			k.setCivics(eO, eC); HH_totals(k, aiNow);
			k.setCivics(eO, eCur); HH_totals(k, aiBack);
			bool bOk = true;
			for (int j = 0; j < 5; ++j) if (aiBack[j] != aiBase[j]) bOk = false;
			fprintf(f, "%s\n[\"%s\",\"%s\",\"%s\",%d,%d,%d,%d,%d,%d]", bFirst ? "" : ",", GC.getCivicOptionInfo(eO).getType(),
				eCur != NO_CIVIC ? GC.getCivicInfo(eCur).getType() : "-", GC.getCivicInfo(eC).getType(),
				aiNow[0], aiNow[1], aiNow[2], aiNow[3], aiNow[4], bOk ? 1 : 0);
			bFirst = false;
		}
	}
	fprintf(f, "],\"techValues\":[");
	bFirst = true;
	int* aiRev = new int[GC.getNumBonusClassInfos()];
	int* aiUnrev = new int[GC.getNumBonusClassInfos()];
	int* aiHave = new int[GC.getNumBonusClassInfos()];
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		CvPlayerAI& kA = GET_PLAYER((PlayerTypes)i);
		if (!kA.isAlive() || i == (int)ePlayer) continue;
		CvTeam& kTA = GET_TEAM(kA.getTeam());
		// the bonus-class counts AI_bestTech prepares (CvPlayerAI.cpp)
		for (int b = 0; b < GC.getNumBonusClassInfos(); ++b) { aiRev[b] = 0; aiUnrev[b] = 0; aiHave[b] = 0; }
		for (int b = 0; b < GC.getNumBonusInfos(); ++b)
		{
			const TechTypes eR = (TechTypes)GC.getBonusInfo((BonusTypes)b).getTechReveal();
			const int eBC = GC.getBonusInfo((BonusTypes)b).getBonusClassType();
			if (eR == NO_TECH) continue;
			if (kTA.isHasTech(eR)) aiRev[eBC]++; else aiUnrev[eBC]++;
			if (kA.getNumAvailableBonuses((BonusTypes)b) > 0 || kA.countOwnedBonuses((BonusTypes)b) > 0) aiHave[eBC]++;
		}
		for (int t = 0; t < GC.getNumTechInfos(); ++t)
		{
			if (!kA.canResearch((TechTypes)t)) continue;
			fprintf(f, "%s\n[%d,\"%s\",%d,%d]", bFirst ? "" : ",", i, GC.getTechInfo((TechTypes)t).getType(),
				kA.AI_techValue((TechTypes)t, 1, false, false, aiRev, aiUnrev, aiHave), kA.getCurrentResearch() == (TechTypes)t ? 1 : 0);
			bFirst = false;
		}
	}
	delete [] aiRev; delete [] aiUnrev; delete [] aiHave;
	// Civic terms: the civic block of AI_techValue (CvPlayerAI.cpp, "Civic Value") recomputed for every AI,
	// tech it can research now and civic that tech unlocks: the AI's value of that civic and of the one it
	// holds in the option, the term with its cap and without, and the divisor AI_techValue applies after
	// (research turns left times 100 plus latency times the speed's research percent). eraPenalty is 1 when
	// the era-0 penalty of AI_techValue may scale the value further.
	fprintf(f, "],\"civicTerms\":[");
	bFirst = true;
	const int iLatency = std::max(0, GC.getDefineINT("AI_TECH_COMPLETION_LATENCY_TURNS"));
	const int iAdjustment = GC.getGameSpeedInfo(GC.getGameINLINE().getGameSpeedType()).getResearchPercent();
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		CvPlayerAI& kA = GET_PLAYER((PlayerTypes)i);
		if (!kA.isAlive() || i == (int)ePlayer) continue;
		const CivicTypes eFav = (CivicTypes)GC.getLeaderHeadInfo(kA.getPersonalityType()).getFavoriteCivic();
		for (int t = 0; t < GC.getNumTechInfos(); ++t)
		{
			if (!kA.canResearch((TechTypes)t)) continue;
			for (int c = 0; c < GC.getNumCivicInfos(); ++c)
			{
				if (GC.getCivicInfo((CivicTypes)c).getTechPrereq() != t) continue;
				const CivicTypes eHeld = kA.getCivics((CivicOptionTypes)GC.getCivicInfo((CivicTypes)c).getCivicOptionType());
				const int iNew = kA.AI_civicValue((CivicTypes)c);
				const int iCur = (eHeld != NO_CIVIC) ? kA.AI_civicValue(eHeld) : 0;
				int iCapped = 200, iUncapped = 200;
				if (eHeld != NO_CIVIC)
				{
					if (iNew > iCur)
					{
						iUncapped += (2400 * (iNew - iCur)) / std::max(1, iCur);
						iCapped += std::min(2400, (2400 * (iNew - iCur)) / std::max(1, iCur));
					}
					if ((CivicTypes)c == eFav) { iCapped += 600; iUncapped += 600; }
				}
				fprintf(f, "%s\n[%d,\"%s\",\"%s\",\"%s\",%d,%d,%d,%d,%d,%d]", bFirst ? "" : ",", i, GC.getTechInfo((TechTypes)t).getType(),
					GC.getCivicInfo((CivicTypes)c).getType(), eHeld != NO_CIVIC ? GC.getCivicInfo(eHeld).getType() : "-", iNew, iCur,
					iCapped, iUncapped, HarnessPeek::researchTurnsLeftTimes100(kA, (TechTypes)t) + iLatency * iAdjustment,
					(kA.getCurrentEra() == 0 && GC.getTechInfo((TechTypes)t).getEra() > 0) ? 1 : 0);
				bFirst = false;
			}
		}
	}
	fprintf(f, "]}\n");
	fclose(f);
}

extern "C" __declspec(dllexport) int HH_dumpState(const char* szPath)
{
	const HarnessPeekGuard kNoSideEffects;
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
		if (getenv("HARNESS_HISTORY_DIAG") != NULL)
		{
			// What the save remembers about the past: the per-turn history
			// series, partial research, the research queue and the cost terms.
			fprintf(f, "\"costs\":{\"unit\":%d,\"supply\":%d,\"maint\":%d,\"civic\":%d,\"pre\":%d,\"inflation\":%d,"
				"\"military\":%d,\"units\":%d},",
				k.calculateUnitCost(), k.calculateUnitSupply(), k.getTotalMaintenance(), k.getCivicUpkeep(),
				k.calculatePreInflatedCosts(), k.calculateInflationRate(), k.getNumMilitaryUnits(), k.getNumUnits());
			fprintf(f, "\"progress\":[");
			bool bFirstP = true;
			for (int t = 0; t < GC.getNumTechInfos(); ++t)
			{
				const int iProgress = kT.getResearchProgress((TechTypes)t);
				const int iQueue = k.getQueuePosition((TechTypes)t);
				if (kT.isHasTech((TechTypes)t) || (iProgress <= 0 && iQueue <= 0)) continue;
				fprintf(f, "%s[\"%s\",%d,%d,%d,%d]", bFirstP ? "" : ",", GC.getTechInfo((TechTypes)t).getType(), iProgress,
					kT.getResearchCost((TechTypes)t), iQueue, k.canResearch((TechTypes)t) ? 1 : 0);
				bFirstP = false;
			}
			fprintf(f, "],\"hist\":{");
			const char* aszSeries[] = {"score", "econ", "ind", "agr", "pow", "cult"};
			for (int s = 0; s < 6; ++s)
			{
				fprintf(f, "%s\"%s\":[", s ? "," : "", aszSeries[s]);
				for (int iT = 0; iT <= g.getGameTurn(); ++iT)
				{
					int iV = 0;
					switch (s)
					{
					case 0: iV = k.getScoreHistory(iT); break;
					case 1: iV = k.getEconomyHistory(iT); break;
					case 2: iV = k.getIndustryHistory(iT); break;
					case 3: iV = k.getAgricultureHistory(iT); break;
					case 4: iV = k.getPowerHistory(iT); break;
					default: iV = k.getCultureHistory(iT); break;
					}
					fprintf(f, "%s%d", iT ? "," : "", iV);
				}
				fprintf(f, "]");
			}
			fprintf(f, "},");
			// The AI's per-turn value of every civic it may adopt now.
			fprintf(f, "\"civicValues\":[");
			bool bFirstC = true;
			for (int c = 0; c < GC.getNumCivicInfos(); ++c)
			{
				if (!k.canDoCivics((CivicTypes)c)) continue;
				fprintf(f, "%s[\"%s\",%d,%d]", bFirstC ? "" : ",", GC.getCivicInfo((CivicTypes)c).getType(),
					GC.getCivicInfo((CivicTypes)c).getCivicOptionType(), k.isHuman() ? 0 : k.AI_civicValue((CivicTypes)c));
				bFirstC = false;
			}
			fprintf(f, "],");
			// Every unit: type, role, experience and where it stands.
			fprintf(f, "\"unitList\":[");
			int iUnitLoop;
			bool bFirstU = true;
			for (CvUnit* u = k.firstUnit(&iUnitLoop); u != NULL; u = k.nextUnit(&iUnitLoop))
			{
				CvWString w;
				getUnitAIString(w, u->AI_getUnitAIType());
				CvSelectionGroup* pG = u->getGroup();
				// then: unit id, damage, moves used, fortify turns, promotions ('|'-separated)
				CvString szPromos;
				for (int iPr = 0; iPr < GC.getNumPromotionInfos(); ++iPr)
				{
					if (!u->isHasPromotion((PromotionTypes)iPr)) continue;
					if (!szPromos.empty()) szPromos += "|";
					szPromos += GC.getPromotionInfo((PromotionTypes)iPr).getType() + 10;
				}
				fprintf(f, "%s[\"%s\",\"%s\",%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,\"%s\"]", bFirstU ? "" : ",",
					GC.getUnitInfo(u->getUnitType()).getType() + 5, CvString(w).GetCString(), u->getExperience(), u->getLevel(),
					u->canFight() ? 1 : 0, u->getX_INLINE(), u->getY_INLINE(), u->getArea(), g.getGameTurn() - u->getGameTurnCreated(),
					pG != NULL ? pG->getNumUnits() : 0, pG != NULL ? (int)pG->AI_getMissionAIType() : -1,
					u->plot()->getOwnerINLINE(), u->isCargo() ? 1 : 0, u->getID(), u->getDamage(), u->getMoves(),
					u->getFortifyTurns(), szPromos.c_str());
				bFirstU = false;
			}
			fprintf(f, "],");
			// Resources: available, imported, exported (non-zero only).
			fprintf(f, "\"bonuses\":[");
			bool bFirstB = true;
			for (int iB = 0; iB < GC.getNumBonusInfos(); ++iB)
			{
				const int iAv = k.getNumAvailableBonuses((BonusTypes)iB), iIm = k.getBonusImport((BonusTypes)iB), iEx = k.getBonusExport((BonusTypes)iB);
				if (iAv == 0 && iIm == 0 && iEx == 0) continue;
				fprintf(f, "%s[\"%s\",%d,%d,%d]", bFirstB ? "" : ",", GC.getBonusInfo((BonusTypes)iB).getType() + 6, iAv, iIm, iEx);
				bFirstB = false;
			}
			// Relations with every other living civilisation: met, war, war plan, open borders, defensive
			// pact, war weariness, war success, attitude and its value (AI only, else -99), memory counts.
			fprintf(f, "],\"worstEnemy\":%d,\"diplo\":[", k.isHuman() ? -1 : (int)kT.AI_getWorstEnemy());
			bool bFirstD = true;
			for (int j = 0; j < MAX_CIV_PLAYERS; ++j)
			{
				CvPlayerAI& kJ = GET_PLAYER((PlayerTypes)j);
				if (j == i || !kJ.isAlive()) continue;
				const TeamTypes eTJ = kJ.getTeam();
				fprintf(f, "%s[%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,[", bFirstD ? "" : ",", j, kT.isHasMet(eTJ) ? 1 : 0, kT.isAtWar(eTJ) ? 1 : 0,
					(int)kT.AI_getWarPlan(eTJ), kT.isOpenBorders(eTJ) ? 1 : 0, kT.isDefensivePact(eTJ) ? 1 : 0, kT.getWarWeariness(eTJ),
					kT.AI_getWarSuccess(eTJ), k.isHuman() ? -99 : (int)k.AI_getAttitude((PlayerTypes)j), k.isHuman() ? -99 : k.AI_getAttitudeVal((PlayerTypes)j));
				for (int m = 0; m < NUM_MEMORY_TYPES; ++m) fprintf(f, "%s%d", m ? "," : "", k.AI_getMemoryCount((PlayerTypes)j, (MemoryTypes)m));
				fprintf(f, "]]");
				bFirstD = false;
			}
			fprintf(f, "],");
		}
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
			// City tiles: worked (1/0), terrain, feature, improvement, hills, river, bonus, food, hammers,
			// commerce; then specialists and the improved tiles the city works or could work.
			fprintf(f, ",\"tiles\":[");
			bool bFirstT = true;
			int iImproved = 0, iRadius = 0;
			for (int iP = 0; iP < NUM_CITY_PLOTS; ++iP)
			{
				CvPlot* pP = c->getCityIndexPlot(iP);
				if (pP == NULL || pP->getWorkingCity() != c) continue;
				++iRadius;
				if (pP->getImprovementType() != NO_IMPROVEMENT) ++iImproved;
				const BonusTypes eB = pP->getBonusType(k.getTeam());
				fprintf(f, "%s[%d,\"%s\",\"%s\",\"%s\",%d,%d,\"%s\",%d,%d,%d]", bFirstT ? "" : ",", c->isWorkingPlot(iP) ? 1 : 0,
					GC.getTerrainInfo(pP->getTerrainType()).getType() + 8,
					pP->getFeatureType() != NO_FEATURE ? GC.getFeatureInfo(pP->getFeatureType()).getType() + 8 : "-",
					pP->getImprovementType() != NO_IMPROVEMENT ? GC.getImprovementInfo(pP->getImprovementType()).getType() + 12 : "-",
					pP->isHills() ? 1 : 0, pP->isRiver() ? 1 : 0, eB != NO_BONUS ? GC.getBonusInfo(eB).getType() + 6 : "-",
					pP->getYield(YIELD_FOOD), pP->getYield(YIELD_PRODUCTION), pP->getYield(YIELD_COMMERCE));
				bFirstT = false;
			}
			fprintf(f, "],\"spec\":%d,\"improved\":%d,\"radius\":%d,\"trade\":[%d,%d]", c->getSpecialistPopulation(), iImproved, iRadius,
				c->getTradeRoutes(), c->getTradeYield(YIELD_COMMERCE));
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
			if (getenv("HARNESS_DEFENCE_DIAG") != NULL && !k.isHuman())
			{
				// City defence: land defenders on the plot, the defenders the city AI wants, the staged forecast
				// of change S with all defenders and with the weakest left out (per mille), the city's danger
				// flag (AI_isDanger), and the owner's staged-forecast threshold. Reads only.
				CvCityAI* pAI = static_cast<CvCityAI*>(c);
				fprintf(f, ",\"def\":[%d,%d,%d,%d,%d,%d]", c->plot()->plotCount(PUF_canDefend, -1, -1, c->getOwnerINLINE(), NO_TEAM, PUF_isDomainType, DOMAIN_LAND),
					pAI->AI_neededDefenders(), pAI->AI_stagedForecast(false), pAI->AI_stagedForecast(true), pAI->AI_isDanger() ? 1 : 0,
					GC.getDefineINT("AI_STAGED_FORECAST", 0) + 10 * GET_PLAYER(c->getOwnerINLINE()).AI_getAttackOddsChange());
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
						k.AI_plotTargetMissionAIs(p, MISSIONAI_GUARD_CITY), (int)p->getOwnerINLINE(), HH_SETTLE_REACH(k, u, p),
						bPath ? 1 : 0, bPath ? iTurns : -1, bPathAny ? 1 : 0, bPathAny ? iTurnsAny : -1);
				}
				fprintf(f, "]");
#ifdef HARNESS_SETTLE_REACH
				// The deliverable candidates (any rank) and why AI_found passes them by.
				fprintf(f, ",\"deliverable\":[");
				int iShown = 0;
				for (int c = 0; c < iCands && iShown < 6; ++c)
				{
					int iFound; bool bByLand = false;
					CvPlot* p = k.AI_getSettlementCandidate(c, iFound);
					if (!k.AI_canDeliverSettler(u->plot(), p, &bByLand)) continue;
					int iTurns = -1;
					const bool bPath = u->generatePath(p, MOVE_SAFE_TERRITORY, false, &iTurns);
					fprintf(f, "%s{\"rank\":%d,\"x\":%d,\"y\":%d,\"v\":%d,\"land\":%d,\"canFound\":%d,\"enemy\":%d,\"otherFound\":%d,"
						"\"coastal\":%d,\"path\":%d,\"turns\":%d}",
						iShown ? "," : "", c, p->getX_INLINE(), p->getY_INLINE(), iFound, bByLand ? 1 : 0, u->canFound(p) ? 1 : 0,
						p->isVisibleEnemyUnit(u) ? 1 : 0, k.AI_plotTargetMissionAIs(p, MISSIONAI_FOUND, pGroup, GC.getMIN_CITY_RANGE()),
						p->isCoastalLand() ? 1 : 0, bPath ? 1 : 0, bPath ? iTurns : -1);
					++iShown;
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
#endif
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
	fprintf(f, "\n]");
	if (getenv("HARNESS_HISTORY_DIAG") != NULL)
	{
		// Units of each type created in the whole game (all players).
		fprintf(f, ",\"created\":{");
		bool bFirstT = true;
		for (int t = 0; t < GC.getNumUnitInfos(); ++t)
		{
			const int iCreated = g.getUnitCreatedCount((UnitTypes)t);
			if (iCreated <= 0) continue;
			fprintf(f, "%s\"%s\":%d", bFirstT ? "" : ",", GC.getUnitInfo((UnitTypes)t).getType(), iCreated);
			bFirstT = false;
		}
		fprintf(f, "}");
		// Every plot: x, y, terrain, plot type, feature, resource, improvement, route, owner, working city
		// (owner, x, y), upgrade progress, river, irrigated, worked, food, hammers, commerce, revealed to the
		// first human team, the improvement that team sees there.
		// A loaded save has its human seats handed to the AI (HarnessHooks.cpp), so isHuman() is false
		// here: HARNESS_HUMAN=<player> names the seat that was human (initcore.py reads it from the save).
		TeamTypes eHumanTeam = NO_TEAM;
		const char* szHuman = getenv("HARNESS_HUMAN");
		if (szHuman != NULL && atoi(szHuman) >= 0 && atoi(szHuman) < MAX_CIV_PLAYERS) eHumanTeam = GET_PLAYER((PlayerTypes)atoi(szHuman)).getTeam();
		fprintf(f, ",\"humanSeat\":%d", szHuman != NULL ? atoi(szHuman) : -1);
		CvMap& kMap = GC.getMapINLINE();
		// What a turn-0 scenario of this map needs (save2scn.py): the map's wrap and size, the game's
		// options and victories, every seat (team, civilization, leader, handicap, starting plot), and per
		// plot in plot order the river edges (direction when north / west of a river, else -1) and the
		// feature variety.
		fprintf(f, ",\"setup\":{\"w\":%d,\"h\":%d,\"wrapX\":%d,\"wrapY\":%d,\"top\":%d,\"bottom\":%d,\"era\":\"%s\",\"options\":[",
			kMap.getGridWidthINLINE(), kMap.getGridHeightINLINE(), kMap.isWrapXINLINE() ? 1 : 0, kMap.isWrapYINLINE() ? 1 : 0,
			kMap.getTopLatitude(), kMap.getBottomLatitude(), GC.getEraInfo(GC.getGameINLINE().getStartEra()).getType());
		bool bFirstO = true;
		for (int o = 0; o < NUM_GAMEOPTION_TYPES; ++o)
		{
			if (!GC.getGameINLINE().isOption((GameOptionTypes)o)) continue;
			fprintf(f, "%s\"%s\"", bFirstO ? "" : ",", GC.getGameOptionInfo((GameOptionTypes)o).getType());
			bFirstO = false;
		}
		fprintf(f, "],\"victories\":[");
		bFirstO = true;
		for (int v = 0; v < GC.getNumVictoryInfos(); ++v)
		{
			if (!GC.getGameINLINE().isVictoryValid((VictoryTypes)v)) continue;
			fprintf(f, "%s\"%s\"", bFirstO ? "" : ",", GC.getVictoryInfo((VictoryTypes)v).getType());
			bFirstO = false;
		}
		fprintf(f, "],\"seats\":[");
		bFirstO = true;
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			CvPlayer& kS = GET_PLAYER((PlayerTypes)i);
			if (kS.getCivilizationType() == NO_CIVILIZATION || kS.getLeaderType() == NO_LEADER) continue;
			const CvPlot* pS = kS.getStartingPlot();
			fprintf(f, "%s[%d,%d,\"%s\",\"%s\",\"%s\",%d,%d,%d]", bFirstO ? "" : ",", i, (int)kS.getTeam(),
				GC.getCivilizationInfo(kS.getCivilizationType()).getType(), GC.getLeaderHeadInfo(kS.getLeaderType()).getType(),
				GC.getHandicapInfo(kS.getHandicapType()).getType(), pS ? pS->getX_INLINE() : -1, pS ? pS->getY_INLINE() : -1,
				kS.isAlive() ? 1 : 0);
			bFirstO = false;
		}
		fprintf(f, "],\"plotx\":[");
		for (int iP = 0; iP < kMap.numPlotsINLINE(); ++iP)
		{
			CvPlot* pP = kMap.plotByIndexINLINE(iP);
			fprintf(f, "%s[%d,%d,%d]", iP ? "," : "", pP->isNOfRiver() ? (int)pP->getRiverWEDirection() : -1,
				pP->isWOfRiver() ? (int)pP->getRiverNSDirection() : -1, pP->getFeatureVariety());
		}
		fprintf(f, "]}");
		fprintf(f, ",\"plots\":[");
		for (int iP = 0; iP < kMap.numPlotsINLINE(); ++iP)
		{
			CvPlot* pP = kMap.plotByIndexINLINE(iP);
			CvCity* pW = pP->getWorkingCity();
			const ImprovementTypes eRI = eHumanTeam != NO_TEAM ? pP->getRevealedImprovementType(eHumanTeam, false) : NO_IMPROVEMENT;
			fprintf(f, "%s\n[%d,%d,\"%s\",%d,\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,\"%s\"]", iP ? "," : "",
				pP->getX_INLINE(), pP->getY_INLINE(), GC.getTerrainInfo(pP->getTerrainType()).getType() + 8, (int)pP->getPlotType(),
				pP->getFeatureType() != NO_FEATURE ? GC.getFeatureInfo(pP->getFeatureType()).getType() + 8 : "-",
				pP->getBonusType() != NO_BONUS ? GC.getBonusInfo(pP->getBonusType()).getType() + 6 : "-",
				pP->getImprovementType() != NO_IMPROVEMENT ? GC.getImprovementInfo(pP->getImprovementType()).getType() + 12 : "-",
				pP->getRouteType() != NO_ROUTE ? GC.getRouteInfo(pP->getRouteType()).getType() + 6 : "-",
				pP->getOwnerINLINE(), pW ? (int)pW->getOwnerINLINE() : -1, pW ? pW->getX_INLINE() : -1, pW ? pW->getY_INLINE() : -1,
				pP->getUpgradeProgress(), pP->isRiver() ? 1 : 0, pP->isIrrigated() ? 1 : 0, pP->isBeingWorked() ? 1 : 0,
				pP->getYield(YIELD_FOOD), pP->getYield(YIELD_PRODUCTION), pP->getYield(YIELD_COMMERCE),
				eHumanTeam != NO_TEAM && pP->isRevealed(eHumanTeam, false) ? 1 : 0,
				eRI != NO_IMPROVEMENT ? GC.getImprovementInfo(eRI).getType() + 12 : "-");
		}
		fprintf(f, "],\"memoryTypes\":[");
		for (int m = 0; m < NUM_MEMORY_TYPES; ++m) fprintf(f, "%s\"%s\"", m ? "," : "", GC.getMemoryInfo((MemoryTypes)m).getType());
		fprintf(f, "]");
		fprintf(f, ",\"replay\":[");
		for (uint r = 0; r < g.getNumReplayMessages(); ++r)
		{
			fprintf(f, "%s\n[%d,%d,%d,", r ? "," : "", g.getReplayMessageTurn(r), (int)g.getReplayMessagePlayer(r),
				(int)g.getReplayMessageType(r));
			writeJsonText(f, g.getReplayMessageText(r));
			fprintf(f, "]");
		}
		fprintf(f, "]");
	}
	fprintf(f, "}\n");
	fclose(f);
	// HARNESS_PROBE=<file> (with HARNESS_HUMAN): counterfactual civics of the human seat and the AIs'
	// tech values, inside the guard above, so random seeds and AI caches are restored afterwards.
	const char* szProbe = getenv("HARNESS_PROBE");
	static bool bProbed = false;
	if (szProbe != NULL && !bProbed && getenv("HARNESS_HUMAN") != NULL)
	{
		bProbed = true;
		HH_probe(szProbe, (PlayerTypes)atoi(getenv("HARNESS_HUMAN")));
	}
	return 0;
}
