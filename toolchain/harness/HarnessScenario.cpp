// Harness-only: load a WorldBuilder scenario (converted by wbs2scn.py) and
// report the diplomatic state every turn. Compiled only into harness builds of
// CvGameCoreDLL; nothing here changes game logic. Setup follows the order of
// the game's CvWBDesc.py: game options and slots, map, plots, teams, players,
// units, cities.
#include "CvGameCoreDLL.h"
#include <cstdlib>
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvUnit.h"
#include "CvCity.h"
#include "CvDeal.h"
#include "CvCityAI.h"
#include "CvUnitAI.h"
#include "CvSelectionGroupAI.h"
#include "CvPlotGroup.h"
#include "CvInfos.h"
#include "CvInitCore.h"
#include "CvGameCoreUtils.h"
#include "AI_Defines.h"
#include "HarnessPeek.h"
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <sstream>
#include <math.h>

namespace
{
	std::vector<std::string> split(const std::string& s, char c)
	{
		std::vector<std::string> out;
		std::string cur;
		for (size_t i = 0; i < s.size(); ++i)
		{
			if (s[i] == c) { if (!cur.empty()) out.push_back(cur); cur.clear(); }
			else if (s[i] != '\r' && s[i] != '\n') cur += s[i];
		}
		if (!cur.empty()) out.push_back(cur);
		return out;
	}

	int type(const std::string& s)
	{
		if (s.empty() || s == "-") return -1;
		return GC.getInfoTypeForString(s.c_str(), true);
	}

	int num(const std::string& s) { return atoi(s.c_str()); }

	std::string g_szLoadLog;
	void note(const char* fmt, const char* a, int b = 0)
	{
		char buf[256];
		_snprintf(buf, sizeof(buf), fmt, a, b);
		buf[sizeof(buf) - 1] = 0;
		g_szLoadLog += buf;
		g_szLoadLog += "\n";
	}
}

// Returns the number of active civ players, or -1 on failure. szSpeed and
// szHandicap override the scenario ("-" keeps the scenario's speed; the game
// handicap sets the AI modifiers, as the human's handicap would).
extern "C" __declspec(dllexport) int HH_loadScenario(const char* szPath, const char* szSpeed, const char* szHandicap,
	unsigned int uiSeed, char* szLog, int iLogSize)
{
	g_szLoadLog.clear();
	FILE* f = fopen(szPath, "r");
	if (f == NULL) return -1;
	std::vector<std::vector<std::string> > recs;
	char line[4096];
	while (fgets(line, sizeof(line), f)) recs.push_back(split(line, ' '));
	fclose(f);

	CvInitCore& kInit = GC.getInitCore();
	kInit.init(GAMEMODE_NORMAL);
	kInit.setType(GAME_SP_SCENARIO);
	kInit.setMode(GAMEMODE_NORMAL);
	kInit.setSyncRandSeed(uiSeed);
	kInit.setMapRandSeed(uiSeed);
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i) kInit.setSlotStatus((PlayerTypes)i, SS_CLOSED);
	for (int i = 0; i < GC.getNumVictoryInfos(); ++i) kInit.setVictory((VictoryTypes)i, false);

	int iW = 0, iH = 0, iTop = 90, iBottom = -90, iStartYear = 0, iGameTurn = 0, iMaxTurns = 0, iPlayers = 0;
	bool bWrapX = false, bWrapY = false;
	std::string szScenarioSpeed = "-";
	const HandicapTypes eGameHandicap = (HandicapTypes)type(szHandicap);
	for (size_t r = 0; r < recs.size(); ++r)
	{
		const std::vector<std::string>& a = recs[r];
		if (a.empty()) continue;
		if (a[0] == "GAME" && a.size() >= 7)
		{
			if (type(a[1]) >= 0) kInit.setEra((EraTypes)type(a[1]));
			if (type(a[2]) >= 0) kInit.setCalendar((CalendarTypes)type(a[2]));
			iStartYear = num(a[3]); iGameTurn = num(a[4]); iMaxTurns = num(a[5]); szScenarioSpeed = a[6];
		}
		else if (a[0] == "OPTION" && a.size() >= 2)
		{
			if (type(a[1]) >= 0) kInit.setOption((GameOptionTypes)type(a[1]), true);
			else note("unknown option %s", a[1].c_str());
		}
		else if (a[0] == "VICTORY" && a.size() >= 2)
		{
			if (type(a[1]) >= 0) kInit.setVictory((VictoryTypes)type(a[1]), true);
			else note("unknown victory %s", a[1].c_str());
		}
		else if (a[0] == "MAP" && a.size() >= 10)
		{
			iW = num(a[1]); iH = num(a[2]); bWrapX = num(a[3]) != 0; bWrapY = num(a[4]) != 0;
			if (type(a[5]) >= 0) kInit.setWorldSize((WorldSizeTypes)type(a[5]));
			if (type(a[6]) >= 0) kInit.setClimate((ClimateTypes)type(a[6]));
			if (type(a[7]) >= 0) kInit.setSeaLevel((SeaLevelTypes)type(a[7]));
			iTop = num(a[8]); iBottom = num(a[9]);
		}
		else if (a[0] == "PLAYER" && a.size() >= 10)
		{
			const PlayerTypes eP = (PlayerTypes)num(a[1]);
			const int eCiv = type(a[3]), eLeader = type(a[4]);
			if (eP < 0 || eP >= MAX_CIV_PLAYERS || eCiv < 0 || eLeader < 0)
			{
				note("skipped player (civ or leader unknown): %s", (a[3] + "/" + a[4]).c_str());
				continue;
			}
			kInit.setSlotStatus(eP, SS_COMPUTER);
			kInit.setSlotClaim(eP, SLOTCLAIM_ASSIGNED);
			kInit.setCiv(eP, (CivilizationTypes)eCiv);
			kInit.setLeader(eP, (LeaderHeadTypes)eLeader);
			kInit.setTeam(eP, (TeamTypes)num(a[2]));
			kInit.setHandicap(eP, type(a[5]) >= 0 ? (HandicapTypes)type(a[5]) : eGameHandicap);
			kInit.setColor(eP, (PlayerColorTypes)GC.getCivilizationInfo((CivilizationTypes)eCiv).getDefaultPlayerColor());
			++iPlayers;
		}
	}
	const std::string szUseSpeed = (szSpeed && strcmp(szSpeed, "-") != 0) ? szSpeed : (szScenarioSpeed != "-" ? szScenarioSpeed : "GAMESPEED_NORMAL");
	kInit.setGameSpeed((GameSpeedTypes)type(szUseSpeed));
	kInit.setSlotStatus(BARBARIAN_PLAYER, SS_COMPUTER);
	kInit.setCiv(BARBARIAN_PLAYER, (CivilizationTypes)GC.getDefineINT("BARBARIAN_CIVILIZATION"));
	kInit.setLeader(BARBARIAN_PLAYER, (LeaderHeadTypes)GC.getDefineINT("BARBARIAN_LEADER"));
	kInit.setTeam(BARBARIAN_PLAYER, BARBARIAN_TEAM);
	kInit.setHandicap(BARBARIAN_PLAYER, (HandicapTypes)GC.getDefineINT("BARBARIAN_HANDICAP"));
	kInit.setColor(BARBARIAN_PLAYER, (PlayerColorTypes)GC.getCivilizationInfo(kInit.getCiv(BARBARIAN_PLAYER)).getDefaultPlayerColor());
	if (iMaxTurns > 0) kInit.setMaxTurns(iMaxTurns);
	GC.getGameINLINE().init(eGameHandicap);
	CvMapInitData kMap(iW, iH, iTop, iBottom, bWrapX, bWrapY);
	GC.getMapINLINE().init(&kMap);

	for (int i = 0; i < MAX_TEAMS; ++i) GET_TEAM((TeamTypes)i).init((TeamTypes)i);
	for (int i = 0; i < MAX_PLAYERS; ++i) GET_PLAYER((PlayerTypes)i).init((PlayerTypes)i);
	GC.getGameINLINE().initDiplomacy();
	GC.getGameINLINE().initFreeState();
	GC.getGameINLINE().setActivePlayer(NO_PLAYER, false);
	GC.getGameINLINE().setStartYear(iStartYear);
	GC.getGameINLINE().setGameTurn(iGameTurn);

	// Plots: types and terrain first (CvPlotDesc.preApply), then areas, then the rest.
	for (size_t r = 0; r < recs.size(); ++r)
	{
		const std::vector<std::string>& a = recs[r];
		if (a.size() < 12 || a[0] != "PLOT") continue;
		CvPlot* p = GC.getMapINLINE().plot(num(a[1]), num(a[2]));
		if (p == NULL) continue;
		p->setPlotType((PlotTypes)num(a[3]), false, false);
		if (type(a[4]) >= 0) p->setTerrainType((TerrainTypes)type(a[4]), false, false);
	}
	GC.getMapINLINE().recalculateAreas();
	for (size_t r = 0; r < recs.size(); ++r)
	{
		const std::vector<std::string>& a = recs[r];
		if (a.size() < 12 || a[0] != "PLOT") continue;
		CvPlot* p = GC.getMapINLINE().plot(num(a[1]), num(a[2]));
		if (p == NULL) continue;
		if (num(a[10]) >= 0) p->setNOfRiver(true, (CardinalDirectionTypes)num(a[10]));
		if (num(a[11]) >= 0) p->setWOfRiver(true, (CardinalDirectionTypes)num(a[11]));
		if (type(a[5]) >= 0) p->setFeatureType((FeatureTypes)type(a[5]), num(a[6]));
		if (type(a[7]) >= 0) p->setBonusType((BonusTypes)type(a[7]));
		if (type(a[8]) >= 0) p->setImprovementType((ImprovementTypes)type(a[8]));
		if (type(a[9]) >= 0) p->setRouteType((RouteTypes)type(a[9]), false);
	}
	GC.getMapINLINE().recalculateAreas();

	for (size_t r = 0; r < recs.size(); ++r)
	{
		const std::vector<std::string>& a = recs[r];
		if (a.empty()) continue;
		if (a[0] == "TECH" && a.size() >= 3)
		{
			const TeamTypes eT = (TeamTypes)num(a[1]);
			if (type(a[2]) >= 0 && GET_TEAM(eT).isAlive()) GET_TEAM(eT).setHasTech((TechTypes)type(a[2]), true, NO_PLAYER, false, false);
		}
		else if (a[0] == "CONTACT" && a.size() >= 3)
		{
			const TeamTypes eT = (TeamTypes)num(a[1]), eO = (TeamTypes)num(a[2]);
			if (eO < MAX_CIV_TEAMS && GET_TEAM(eT).isAlive() && GET_TEAM(eO).isAlive()) GET_TEAM(eT).meet(eO, false);
		}
		else if (a[0] == "TEAM" && a.size() >= 3)
		{
			if (num(a[2]) != 0 && GET_TEAM((TeamTypes)num(a[1])).isAlive()) GC.getMapINLINE().setRevealedPlots((TeamTypes)num(a[1]), true);
		}
		else if (a[0] == "PLAYER" && a.size() >= 10)
		{
			CvPlayerAI& k = GET_PLAYER((PlayerTypes)num(a[1]));
			if (!k.isAlive() && kInit.getSlotStatus(k.getID()) != SS_COMPUTER) continue;
			CvPlot* pStart = GC.getMapINLINE().plot(num(a[6]), num(a[7]));
			if (pStart != NULL) k.setStartingPlot(pStart, true);
			k.setGold(num(a[8]));
			if (type(a[9]) >= 0) k.setLastStateReligion((ReligionTypes)type(a[9]));
		}
		else if (a[0] == "CIVIC" && a.size() >= 4)
		{
			if (type(a[2]) >= 0 && type(a[3]) >= 0) GET_PLAYER((PlayerTypes)num(a[1])).setCivics((CivicOptionTypes)type(a[2]), (CivicTypes)type(a[3]));
		}
	}

	for (size_t r = 0; r < recs.size(); ++r)
	{
		const std::vector<std::string>& a = recs[r];
		if (a.size() < 10 || a[0] != "UNIT") continue;
		const int eOwner = num(a[1]), eUnit = type(a[4]);
		if (eOwner < 0 || eOwner >= MAX_PLAYERS || eUnit < 0 || kInit.getSlotStatus((PlayerTypes)eOwner) != SS_COMPUTER)
		{
			note("skipped unit %s", a[4].c_str());
			continue;
		}
		const int eAI = type(a[5]);
		CvUnit* pUnit = GET_PLAYER((PlayerTypes)eOwner).initUnit((UnitTypes)eUnit, num(a[2]), num(a[3]), eAI >= 0 ? (UnitAITypes)eAI : NO_UNITAI);
		if (pUnit == NULL) continue;
		pUnit->setLevel(std::max(1, num(a[6])));
		pUnit->setExperience(num(a[7]));
		pUnit->setDamage(num(a[8]));
		if (a[9] != "-")
		{
			std::vector<std::string> ps = split(a[9], ',');
			for (size_t i = 0; i < ps.size(); ++i) if (type(ps[i]) >= 0) pUnit->setHasPromotion((PromotionTypes)type(ps[i]), true);
		}
	}
	for (size_t r = 0; r < recs.size(); ++r)
	{
		const std::vector<std::string>& a = recs[r];
		if (a.size() < 8 || a[0] != "CITY") continue;
		const int eOwner = num(a[1]);
		if (eOwner < 0 || eOwner >= MAX_PLAYERS || kInit.getSlotStatus((PlayerTypes)eOwner) != SS_COMPUTER) { note("skipped city of %s", "player", eOwner); continue; }
		CvCity* pCity = GET_PLAYER((PlayerTypes)eOwner).initCity(num(a[2]), num(a[3]), true, true);
		if (pCity == NULL) continue;
		pCity->setPopulation(std::max(1, num(a[4])));
		std::vector<std::string> bs = a[5] != "-" ? split(a[5], ',') : std::vector<std::string>();
		for (size_t i = 0; i < bs.size(); ++i) if (type(bs[i]) >= 0) pCity->setNumRealBuilding((BuildingTypes)type(bs[i]), 1);
		std::vector<std::string> rs = a[6] != "-" ? split(a[6], ',') : std::vector<std::string>();
		for (size_t i = 0; i < rs.size(); ++i) if (type(rs[i]) >= 0) pCity->setHasReligion((ReligionTypes)type(rs[i]), true, false, false);
		std::vector<std::string> hs = a[7] != "-" ? split(a[7], ',') : std::vector<std::string>();
		for (size_t i = 0; i < hs.size(); ++i) if (type(hs[i]) >= 0) GC.getGameINLINE().setHolyCity((ReligionTypes)type(hs[i]), pCity, false);
	}
	GC.getGameINLINE().initScoreCalculation();
	GC.getGameINLINE().setFinalInitialized(true);

	if (szLog != NULL && iLogSize > 0)
	{
		_snprintf(szLog, iLogSize, "%s", g_szLoadLog.c_str());
		szLog[iLogSize - 1] = 0;
	}
	return iPlayers;
}

//////////////////////////////////////////////////////////////////////////////
// Telemetry: one JSON object per call (call once per game turn).
//////////////////////////////////////////////////////////////////////////////
namespace
{
	std::set<int> g_seenDeals;
	// Every trade as it is agreed (build_dll.sh adds the call to the harness copy
	// of CvDeal::addTrades); one-time items never appear as a standing deal.
	std::vector<std::string> g_tradeLog;
	std::map<int, int> g_cityOwner;     // plot index -> owner
	std::set<int> g_alive;

	void items(std::ostringstream& o, const CLinkList<TradeData>* pList)
	{
		o << "[";
		bool bFirst = true;
		for (CLLNode<TradeData>* n = pList->head(); n != NULL; n = pList->next(n))
		{
			o << (bFirst ? "" : ",") << "[" << (int)n->m_data.m_eItemType << "," << n->m_data.m_iData << "]";
			bFirst = false;
		}
		o << "]";
	}
}

void HH_noteTrade(PlayerTypes eFirst, PlayerTypes eSecond, const CLinkList<TradeData>* pFirst,
	const CLinkList<TradeData>* pSecond)
{
	std::ostringstream o;
	o << "{\"trade\":[" << (int)eFirst << "," << (int)eSecond << "],\"ai\":";
	if (pFirst != NULL) items(o, pFirst); else o << "[]";
	o << ",\"bi\":";
	if (pSecond != NULL) items(o, pSecond); else o << "[]";
	o << "}";
	g_tradeLog.push_back(o.str());
}

extern "C" __declspec(dllexport) void HH_telemetryReset()
{
	g_tradeLog.clear();
	g_seenDeals.clear();
	g_cityOwner.clear();
	g_alive.clear();
}

// Header: static facts about the players, written once.
extern "C" __declspec(dllexport) int HH_telemetryHeader(char* szBuf, int iSize)
{
	std::ostringstream o;
	CvGame& kGame = GC.getGameINLINE();
	o << "{\"hdr\":1,\"speed\":\"" << GC.getGameSpeedInfo(kGame.getGameSpeedType()).getType()
	  << "\",\"handicap\":\"" << GC.getHandicapInfo(kGame.getHandicapType()).getType()
	  << "\",\"maxTurns\":" << kGame.getMaxTurns() << ",\"w\":" << GC.getMapINLINE().getGridWidthINLINE()
	  << ",\"h\":" << GC.getMapINLINE().getGridHeightINLINE() << ",\"victories\":[";
	bool bFirst = true;
	for (int i = 0; i < GC.getNumVictoryInfos(); ++i)
	{
		if (!kGame.isVictoryValid((VictoryTypes)i)) continue;
		o << (bFirst ? "" : ",") << "\"" << GC.getVictoryInfo((VictoryTypes)i).getType() << "\"";
		bFirst = false;
	}
	o << "],\"players\":[";
	bFirst = true;
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		CvPlayerAI& k = GET_PLAYER((PlayerTypes)i);
		if (!k.isAlive()) continue;
		o << (bFirst ? "" : ",") << "{\"id\":" << i << ",\"team\":" << (int)k.getTeam()
		  << ",\"civ\":\"" << GC.getCivilizationInfo(k.getCivilizationType()).getType()
		  << "\",\"leader\":\"" << GC.getLeaderHeadInfo(k.getLeaderType()).getType()
		  << "\",\"personality\":\"" << GC.getLeaderHeadInfo(k.getPersonalityType()).getType() << "\"}";
		bFirst = false;
	}
	o << "]}";
	const std::string s = o.str();
	_snprintf(szBuf, iSize, "%s", s.c_str());
	szBuf[iSize - 1] = 0;
	return (int)std::min((size_t)iSize - 1, s.size());
}

// iDetail: 0 = state and events; 1 = also attitude components and memories.
// Returns the length written, or -(needed size) if the buffer is too small.
extern "C" __declspec(dllexport) int HH_telemetry(char* szBuf, int iSize, int iDetail, int iTurnMs)
{
	const HarnessPeekGuard kNoSideEffects;
	// HARNESS_TELEMETRY_MINIMAL=1 leaves out attitudes, their components and
	// memories (to check that the full telemetry does not change the game).
	static const bool bMinimal = getenv("HARNESS_TELEMETRY_MINIMAL") != NULL;
	CvGame& kGame = GC.getGameINLINE();
	std::ostringstream o;
	o << "{\"t\":" << kGame.getGameTurn() << ",\"y\":" << kGame.getGameTurnYear() << ",\"ms\":" << iTurnMs
	  << ",\"state\":" << (int)kGame.getGameState() << ",\"winner\":" << (int)kGame.getWinner()
	  << ",\"victory\":" << (int)kGame.getVictory();

	std::vector<int> aiP, aiT;
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i) if (GET_PLAYER((PlayerTypes)i).isAlive()) aiP.push_back(i);
	for (int i = 0; i < MAX_CIV_TEAMS; ++i) if (GET_TEAM((TeamTypes)i).isAlive()) aiT.push_back(i);

	o << ",\"p\":[";
	for (size_t a = 0; a < aiP.size(); ++a)
	{
		CvPlayerAI& k = GET_PLAYER((PlayerTypes)aiP[a]);
		CvTeamAI& kT = GET_TEAM(k.getTeam());
		int iTechs = 0;
		for (int t = 0; t < GC.getNumTechInfos(); ++t) if (kT.isHasTech((TechTypes)t)) ++iTechs;
		int iBuildings = 0;   // real buildings in all cities
		int iCityLoop;
		for (CvCity* pCity = k.firstCity(&iCityLoop); pCity != NULL; pCity = k.nextCity(&iCityLoop))
		{
			for (int iB = 0; iB < GC.getNumBuildingInfos(); ++iB) iBuildings += pCity->getNumRealBuilding((BuildingTypes)iB);
		}
		o << (a ? "," : "") << "{\"id\":" << aiP[a] << ",\"score\":" << kGame.getPlayerScore(k.getID())
		  << ",\"cities\":" << k.getNumCities() << ",\"pop\":" << k.getTotalPopulation() << ",\"land\":" << k.getTotalLand()
		  << ",\"techs\":" << iTechs << ",\"power\":" << k.getPower() << ",\"mil\":" << k.getNumMilitaryUnits()
		  << ",\"units\":" << k.getNumUnits() << ",\"gold\":" << k.getGold() << ",\"bld\":" << iBuildings
		  << ",\"gr\":" << k.getCommerceRate(COMMERCE_GOLD) << ",\"rr\":" << k.getCommerceRate(COMMERCE_RESEARCH)
		  << ",\"cr\":" << k.getCommerceRate(COMMERCE_CULTURE) << ",\"er\":" << k.getCommerceRate(COMMERCE_ESPIONAGE)
		  << ",\"culture\":" << k.countTotalCulture() << ",\"rel\":" << (int)k.getStateReligion()
		  << ",\"agenda\":" << (int)k.AI_getAgenda() << ",\"agendaScore\":" << k.AI_getAgendaScore()
		  << ",\"vic\":" << HarnessPeek::victoryHash(k) << ",\"strat\":" << HarnessPeek::strategyHash(k)
		  << ",\"trouble\":" << (k.AI_isFinancialTrouble() ? 1 : 0) << ",\"att\":[";
		for (size_t b = 0; b < aiP.size(); ++b)
		{
			const PlayerTypes eO = (PlayerTypes)aiP[b];
			if (b) o << ",";
			if (eO == k.getID() || !kT.isHasMet(GET_PLAYER(eO).getTeam()) || bMinimal) o << "null";
			else o << k.AI_getAttitudeVal(eO);
		}
		o << "]";
		if (iDetail > 0 && !bMinimal)
		{
			// Attitude components toward each met player, in a fixed order
			// (see the analysis scripts), then the non-zero memory counts.
			o << ",\"attc\":{";
			bool bFirst = true;
			for (size_t b = 0; b < aiP.size(); ++b)
			{
				const PlayerTypes eO = (PlayerTypes)aiP[b];
				if (eO == k.getID() || !kT.isHasMet(GET_PLAYER(eO).getTeam())) continue;
				o << (bFirst ? "" : ",") << "\"" << (int)eO << "\":["
				  << k.AI_getCloseBordersAttitude(eO) << "," << k.AI_getWarAttitude(eO) << "," << k.AI_getPeaceAttitude(eO) << ","
				  << k.AI_getSameReligionAttitude(eO) << "," << k.AI_getDifferentReligionAttitude(eO) << ","
				  << k.AI_getBonusTradeAttitude(eO) << "," << k.AI_getOpenBordersAttitude(eO) << ","
				  << k.AI_getDefensivePactAttitude(eO) << "," << k.AI_getRivalDefensivePactAttitude(eO) << ","
				  << k.AI_getRivalVassalAttitude(eO) << "," << k.AI_getShareWarAttitude(eO) << ","
				  << k.AI_getFavoriteCivicAttitude(eO) << "," << k.AI_getTradeAttitude(eO) << ","
				  << k.AI_getRivalTradeAttitude(eO) << "," << k.AI_getColonyAttitude(eO) << ","
				  << k.AI_getFirstImpressionAttitude(eO) << "," << k.AI_getTeamSizeAttitude(eO) << ","
				  << k.AI_getBetterRankDifferenceAttitude(eO) << "," << k.AI_getWorseRankDifferenceAttitude(eO) << ","
				  << k.AI_getLowRankAttitude(eO) << "," << k.AI_getLostWarAttitude(eO) << ",[";
				bool bFirstMem = true;
				for (int m = 0; m < NUM_MEMORY_TYPES; ++m)
				{
					const int iMem = k.AI_getMemoryCount(eO, (MemoryTypes)m);
					if (iMem == 0) continue;
					o << (bFirstMem ? "" : ",") << m << "," << iMem << "," << k.AI_getMemoryAttitude(eO, (MemoryTypes)m);
					bFirstMem = false;
				}
				o << "]]";
				bFirst = false;
			}
			o << "}";
		}
		o << "}";
	}
	o << "]";

	// Team relations: directed matrices over alive civ teams, in aiT order.
	o << ",\"teams\":[";
	for (size_t a = 0; a < aiT.size(); ++a) o << (a ? "," : "") << aiT[a];
	o << "],\"rel\":[";
	for (size_t a = 0; a < aiT.size(); ++a)
	{
		CvTeamAI& kA = GET_TEAM((TeamTypes)aiT[a]);
		o << (a ? "," : "") << "[";
		for (size_t b = 0; b < aiT.size(); ++b)
		{
			const TeamTypes eB = (TeamTypes)aiT[b];
			// bits: 1 met, 2 war, 4 open borders, 8 defensive pact, 16 a is vassal of b, 32 permanent alliance (same team)
			int iBits = 0;
			if (aiT[a] != aiT[b])
			{
				if (kA.isHasMet(eB)) iBits |= 1;
				if (kA.isAtWar(eB)) iBits |= 2;
				if (kA.isOpenBorders(eB)) iBits |= 4;
				if (kA.isDefensivePact(eB)) iBits |= 8;
				if (kA.isVassal(eB)) iBits |= 16;
			}
			o << (b ? "," : "") << "[" << iBits << "," << (aiT[a] != aiT[b] ? (int)kA.AI_getWarPlan(eB) : -1) << ","
			  << (aiT[a] != aiT[b] ? kA.AI_getWarSuccess(eB) : 0) << "]";
		}
		o << "]";
	}
	o << "]";

	// Events since the previous call: new and ended deals, city ownership changes, eliminations.
	o << ",\"ev\":[";
	bool bFirstEv = true;
	std::set<int> current;
	int iLoop;
	for (CvDeal* pDeal = kGame.firstDeal(&iLoop); pDeal != NULL; pDeal = kGame.nextDeal(&iLoop))
	{
		current.insert(pDeal->getID());
		if (g_seenDeals.count(pDeal->getID())) continue;
		o << (bFirstEv ? "" : ",") << "{\"deal\":" << pDeal->getID() << ",\"a\":" << (int)pDeal->getFirstPlayer()
		  << ",\"b\":" << (int)pDeal->getSecondPlayer() << ",\"ai\":";
		items(o, pDeal->getFirstTrades());
		o << ",\"bi\":";
		items(o, pDeal->getSecondTrades());
		o << "}";
		bFirstEv = false;
	}
	for (std::set<int>::const_iterator it = g_seenDeals.begin(); it != g_seenDeals.end(); ++it)
	{
		if (current.count(*it)) continue;
		o << (bFirstEv ? "" : ",") << "{\"dealEnd\":" << *it << "}";
		bFirstEv = false;
	}
	g_seenDeals = current;
	for (size_t i = 0; i < g_tradeLog.size(); ++i)
	{
		o << (bFirstEv ? "" : ",") << g_tradeLog[i];
		bFirstEv = false;
	}
	g_tradeLog.clear();

	std::map<int, int> owners;
	for (size_t a = 0; a <= aiP.size(); ++a)
	{
		const PlayerTypes eP = a < aiP.size() ? (PlayerTypes)aiP[a] : BARBARIAN_PLAYER;
		for (CvCity* pCity = GET_PLAYER(eP).firstCity(&iLoop); pCity != NULL; pCity = GET_PLAYER(eP).nextCity(&iLoop))
			owners[GC.getMapINLINE().plotNum(pCity->getX_INLINE(), pCity->getY_INLINE())] = (int)eP;
	}
	for (std::map<int, int>::const_iterator it = owners.begin(); it != owners.end(); ++it)
	{
		std::map<int, int>::const_iterator old = g_cityOwner.find(it->first);
		if (old == g_cityOwner.end())
		{
			o << (bFirstEv ? "" : ",") << "{\"found\":" << it->first << ",\"by\":" << it->second << "}";
			bFirstEv = false;
		}
		else if (old->second != it->second)
		{
			o << (bFirstEv ? "" : ",") << "{\"capture\":" << it->first << ",\"from\":" << old->second << ",\"by\":" << it->second << "}";
			bFirstEv = false;
		}
	}
	for (std::map<int, int>::const_iterator it = g_cityOwner.begin(); it != g_cityOwner.end(); ++it)
	{
		if (owners.count(it->first)) continue;
		o << (bFirstEv ? "" : ",") << "{\"razed\":" << it->first << ",\"owner\":" << it->second << "}";
		bFirstEv = false;
	}
	g_cityOwner = owners;
	std::set<int> alive(aiP.begin(), aiP.end());
	for (std::set<int>::const_iterator it = g_alive.begin(); it != g_alive.end(); ++it)
	{
		if (alive.count(*it)) continue;
		o << (bFirstEv ? "" : ",") << "{\"eliminated\":" << *it << "}";
		bFirstEv = false;
	}
	g_alive = alive;
	o << "]}";

	const std::string s = o.str();
	if ((int)s.size() + 1 > iSize) return -(int)(s.size() + 1);
	memcpy(szBuf, s.c_str(), s.size() + 1);
	return (int)s.size();
}

extern "C" __declspec(dllexport) int HH_gameState() { return (int)GC.getGameINLINE().getGameState(); }

//////////////////////////////////////////////////////////////////////////////
// Python callbacks whose result the DLL uses directly. The harness has no
// Python, so these mirror the game's scripts: calculateScore from BTS
// CvGameUtils.py with CvUtil.getScoreComponent, doCityCaptureGold and
// doPillageGold from RoM's RoMGameUtils.py (Himeji Castle rule as intended:
// the pillager's active castle doubles pillage gold, the victim's castle
// cancels it; the script's per-city loop let only the last city decide).
//////////////////////////////////////////////////////////////////////////////
namespace
{
	// Python 2 semantics: integer division unless the final-victory branch has
	// already turned iMax into a float.
	int scoreComponent(int iRaw, int iInitial, int iMax, int iFactor, bool bExponential, bool bFinal, bool bVictory)
	{
		CvGame& g = GC.getGameINLINE();
		if (g.getEstimateEndTurn() == 0) return 0;
		double fScore;
		if (bFinal && bVictory)
		{
			const double fTurnRatio = (double)g.getGameTurn() / (double)g.getEstimateEndTurn();
			const double fMax = (bExponential && iInitial != 0) ? iInitial * pow((double)(iMax / iInitial), fTurnRatio)
				: iInitial + fTurnRatio * (iMax - iInitial);
			const double fFree = (GC.getDefineINT("SCORE_FREE_PERCENT") * fMax) / 100;
			fScore = (fFree + fMax) != 0 ? (iFactor * (iRaw + fFree)) / (fFree + fMax) : iFactor;
		}
		else
		{
			const int iFree = (GC.getDefineINT("SCORE_FREE_PERCENT") * iMax) / 100;
			fScore = (iFree + iMax) != 0 ? (iFactor * (iRaw + iFree)) / (iFree + iMax) : iFactor;
		}
		if (bVictory) fScore = (double)(int)(((100 + GC.getDefineINT("SCORE_VICTORY_PERCENT")) * (int)fScore) / 100);
		if (bFinal) fScore = (double)(int)(((100 + GC.getDefineINT("SCORE_HANDICAP_PERCENT_OFFSET") + ((int)g.getHandicapType() * GC.getDefineINT("SCORE_HANDICAP_PERCENT_PER"))) * (int)fScore) / 100);
		return (int)fScore;
	}

	bool hasActiveBuilding(PlayerTypes ePlayer, BuildingTypes eBuilding)
	{
		if (ePlayer == NO_PLAYER || eBuilding == NO_BUILDING) return false;
		const TechTypes eObsolete = (TechTypes)GC.getBuildingInfo(eBuilding).getObsoleteTech();
		if (eObsolete != NO_TECH && GET_TEAM(GET_PLAYER(ePlayer).getTeam()).isHasTech(eObsolete)) return false;
		int iLoop;
		for (CvCity* c = GET_PLAYER(ePlayer).firstCity(&iLoop); c != NULL; c = GET_PLAYER(ePlayer).nextCity(&iLoop))
			if (c->getNumActiveBuilding(eBuilding) > 0) return true;
		return false;
	}
}

extern "C" __declspec(dllexport) int HH_pyCalculateScore(int ePlayer, int bFinal, int bVictory)
{
	CvPlayer& k = GET_PLAYER((PlayerTypes)ePlayer);
	CvGame& g = GC.getGameINLINE();
	return scoreComponent(k.getPopScore(), g.getInitPopulation(), g.getMaxPopulation(), GC.getDefineINT("SCORE_POPULATION_FACTOR"), true, bFinal != 0, bVictory != 0)
		+ scoreComponent(k.getLandScore(), g.getInitLand(), g.getMaxLand(), GC.getDefineINT("SCORE_LAND_FACTOR"), true, bFinal != 0, bVictory != 0)
		+ scoreComponent(k.getTechScore(), g.getInitTech(), g.getMaxTech(), GC.getDefineINT("SCORE_TECH_FACTOR"), true, bFinal != 0, bVictory != 0)
		+ scoreComponent(k.getWondersScore(), g.getInitWonders(), g.getMaxWonders(), GC.getDefineINT("SCORE_WONDER_FACTOR"), false, bFinal != 0, bVictory != 0);
}

extern "C" __declspec(dllexport) int HH_pyCityCaptureGold(void* pCity)
{
	CvCity* c = (CvCity*)pCity;
	if (c == NULL) return 0;
	CvGame& g = GC.getGameINLINE();
	int iGold = GC.getDefineINT("BASE_CAPTURE_GOLD") + c->getPopulation() * GC.getDefineINT("CAPTURE_GOLD_PER_POPULATION");
	iGold += g.getSorenRandNum(GC.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1");
	iGold += g.getSorenRandNum(GC.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2");
	const int iMaxTurns = GC.getDefineINT("CAPTURE_GOLD_MAX_TURNS");
	if (iMaxTurns > 0) iGold = iGold * range(g.getGameTurn() - c->getGameTurnAcquired(), 0, iMaxTurns) / iMaxTurns;
	if (hasActiveBuilding(c->getOwnerINLINE(), (BuildingTypes)GC.getInfoTypeForString("BUILDING_HIMEJI_CASTLE", true))) iGold = 0;
	return iGold;
}

extern "C" __declspec(dllexport) int HH_pyPillageGold(void* pPlotV, void* pUnitV)
{
	CvPlot* p = (CvPlot*)pPlotV;
	CvUnit* u = (CvUnit*)pUnitV;
	if (p == NULL || u == NULL || p->getImprovementType() == NO_IMPROVEMENT) return 0;
	CvGame& g = GC.getGameINLINE();
	const int iBase = GC.getImprovementInfo(p->getImprovementType()).getPillageGold();
	int iGold = g.getSorenRandNum(iBase, "Pillage Gold 1") + g.getSorenRandNum(iBase, "Pillage Gold 2");
	iGold += (u->getPillageChange() * iGold) / 100;
	const BuildingTypes eHimeji = (BuildingTypes)GC.getInfoTypeForString("BUILDING_HIMEJI_CASTLE", true);
	if (hasActiveBuilding(u->getOwnerINLINE(), eHimeji)) iGold *= 2;
	if (hasActiveBuilding(p->getOwnerINLINE(), eHimeji)) iGold = 0;
	return iGold;
}

//////////////////////////////////////////////////////////////////////////////
// Save loading: sav2dat.py splits a save into the CvInitCore block and the
// inflated game stream; this reads them in the engine's order (init core,
// game, map, teams, players). CvMap::read sets up the path finders itself.
//////////////////////////////////////////////////////////////////////////////
#include "FDataStreamBase.h"
namespace
{
	class MemStream : public FDataStreamBase
	{
	public:
		std::vector<char> m_data;
		unsigned int m_pos;
		bool m_bOverrun;
		MemStream() : m_pos(0), m_bOverrun(false) {}
		bool load(const char* szPath)
		{
			FILE* f = fopen(szPath, "rb");
			if (f == NULL) return false;
			fseek(f, 0, SEEK_END); const long n = ftell(f); fseek(f, 0, SEEK_SET);
			m_data.resize(n > 0 ? n : 1);
			const size_t got = fread(&m_data[0], 1, n, f);
			fclose(f);
			m_data.resize(got);
			m_pos = 0;
			return true;
		}
		void raw(void* p, unsigned int n)
		{
			if (m_pos + n > m_data.size()) { m_bOverrun = true; memset(p, 0, n); m_pos = (unsigned int)m_data.size(); return; }
			if (n) memcpy(p, &m_data[m_pos], n);
			m_pos += n;
		}
		int len() { int n = 0; raw(&n, 4); return (n < 0 || n > (1 << 24)) ? (m_bOverrun = true, 0) : n; }

		void Rewind() { m_pos = 0; }
		bool AtEnd() { return m_pos >= m_data.size(); }
		void FastFwd() { m_pos = (unsigned int)m_data.size(); }
		unsigned int GetPosition() const { return m_pos; }
		void SetPosition(unsigned int p) { m_pos = p; }
		void Truncate() {}
		void Flush() {}
		unsigned int GetEOF() const { return (unsigned int)m_data.size(); }
		unsigned int GetSizeLeft() const { return (unsigned int)m_data.size() - m_pos; }
		void CopyToMem(void* mem) { if (!m_data.empty()) memcpy(mem, &m_data[0], m_data.size()); }

		// Writing appends at the end (snapshots are written front to back).
		void put(const void* p, unsigned int n) { const char* c = (const char*)p; m_data.insert(m_data.end(), c, c + n); m_pos = (unsigned int)m_data.size(); }
		void putLen(int n) { put(&n, 4); }
		bool save(const char* szPath) const
		{
			FILE* f = fopen(szPath, "wb");
			if (f == NULL) return false;
			const bool bOk = m_data.empty() || fwrite(&m_data[0], 1, m_data.size(), f) == m_data.size();
			return fclose(f) == 0 && bOk;
		}
		unsigned int WriteString(const wchar* sz) { const int n = sz ? (int)wcslen(sz) : 0; putLen(n); put(sz, n * 2); return n; }
		unsigned int WriteString(const char* sz) { const int n = sz ? (int)strlen(sz) : 0; putLen(n); put(sz, n); return n; }
		unsigned int WriteString(const std::string& sz) { return WriteString(sz.c_str()); }
		unsigned int WriteString(const std::wstring& sz) { return WriteString(sz.c_str()); }
		unsigned int WriteString(int count, std::string values[]) { for (int i = 0; i < count; ++i) WriteString(values[i]); return count; }
		unsigned int WriteString(int count, std::wstring values[]) { for (int i = 0; i < count; ++i) WriteString(values[i]); return count; }

		unsigned int ReadString(char* sz) { const int n = len(); raw(sz, n); sz[n] = 0; return n; }
		unsigned int ReadString(wchar* sz) { const int n = len(); raw(sz, n * 2); sz[n] = 0; return n; }
		unsigned int ReadString(std::string& s)
		{
			const int n = len(); std::vector<char> b(n + 1, 0); raw(&b[0], n); s.assign(&b[0], n); return n;
		}
		unsigned int ReadString(std::wstring& s)
		{
			const int n = len(); std::vector<wchar> b(n + 1, 0); raw(&b[0], n * 2); s.assign(&b[0], n); return n;
		}
		unsigned int ReadString(int count, std::string values[]) { for (int i = 0; i < count; ++i) ReadString(values[i]); return count; }
		unsigned int ReadString(int count, std::wstring values[]) { for (int i = 0; i < count; ++i) ReadString(values[i]); return count; }
		char* ReadString() { const int n = len(); char* s = new char[n + 1]; raw(s, n); s[n] = 0; return s; }
		wchar* ReadWideString() { const int n = len(); wchar* s = new wchar[n + 1]; raw(s, n * 2); s[n] = 0; return s; }

		void Read(char* v) { raw(v, 1); }
		void Read(byte* v) { raw(v, 1); }
		void Read(int count, char values[]) { raw(values, count); }
		void Read(int count, byte values[]) { raw(values, count); }
		void Read(bool* v) { raw(v, 1); }
		void Read(int count, bool values[]) { raw(values, count); }
		void Read(short* v) { raw(v, 2); }
		void Read(unsigned short* v) { raw(v, 2); }
		void Read(int count, short values[]) { raw(values, count * 2); }
		void Read(int count, unsigned short values[]) { raw(values, count * 2); }
		void Read(int* v) { raw(v, 4); }
		void Read(unsigned int* v) { raw(v, 4); }
		void Read(int count, int values[]) { raw(values, count * 4); }
		void Read(int count, unsigned int values[]) { raw(values, count * 4); }
		void Read(long* v) { raw(v, 4); }
		void Read(unsigned long* v) { raw(v, 4); }
		void Read(int count, long values[]) { raw(values, count * 4); }
		void Read(int count, unsigned long values[]) { raw(values, count * 4); }
		void Read(float* v) { raw(v, 4); }
		void Read(int count, float values[]) { raw(values, count * 4); }
		void Read(double* v) { raw(v, 8); }
		void Read(int count, double values[]) { raw(values, count * 8); }

		void Write(char v) { put(&v, 1); }
		void Write(byte v) { put(&v, 1); }
		void Write(int count, const char values[]) { put(values, count); }
		void Write(int count, const byte values[]) { put(values, count); }
		void Write(bool v) { put(&v, 1); }
		void Write(int count, const bool values[]) { put(values, count); }
		void Write(short v) { put(&v, 2); }
		void Write(unsigned short v) { put(&v, 2); }
		void Write(int count, const short values[]) { put(values, count * 2); }
		void Write(int count, const unsigned short values[]) { put(values, count * 2); }
		void Write(int v) { put(&v, 4); }
		void Write(unsigned int v) { put(&v, 4); }
		void Write(int count, const int values[]) { put(values, count * 4); }
		void Write(int count, const unsigned int values[]) { put(values, count * 4); }
		void Write(long v) { put(&v, 4); }
		void Write(unsigned long v) { put(&v, 4); }
		void Write(int count, const long values[]) { put(values, count * 4); }
		void Write(int count, const unsigned long values[]) { put(values, count * 4); }
		void Write(float v) { put(&v, 4); }
		void Write(int count, const float values[]) { put(values, count * 4); }
		void Write(double v) { put(&v, 8); }
		void Write(int count, const double values[]) { put(values, count * 8); }
	};
}

extern "C" __declspec(dllexport) int HH_loadSave(const char* szInit, const char* szGame, char* szLog, int iLogSize)
{
	std::ostringstream o;
	MemStream si, sg;
	if (!si.load(szInit) || !sg.load(szGame)) { _snprintf(szLog, iLogSize, "cannot read input files\n"); return -1; }
	GC.getInitCore().read(&si);
	o << "init core: read " << si.GetPosition() << " of " << si.GetEOF() << (si.m_bOverrun ? " (OVERRUN)" : "") << "\n";
	fprintf(stderr, "%s", o.str().c_str()); fflush(stderr);
	GC.getGameINLINE().read(&sg);
	o << "game: at " << sg.GetPosition() << ", turn " << GC.getGameINLINE().getGameTurn() << "\n";
	fprintf(stderr, "game: at %u, turn %d\n", sg.GetPosition(), GC.getGameINLINE().getGameTurn()); fflush(stderr);
	GC.getMapINLINE().read(&sg);
	o << "map: at " << sg.GetPosition() << ", " << GC.getMapINLINE().getGridWidthINLINE() << "x" << GC.getMapINLINE().getGridHeightINLINE() << "\n";
	for (int i = 0; i < MAX_TEAMS; ++i) GET_TEAM((TeamTypes)i).read(&sg);
	o << "teams: at " << sg.GetPosition() << "\n";
	int iAlive = 0;
	for (int i = 0; i < MAX_PLAYERS; ++i) { GET_PLAYER((PlayerTypes)i).read(&sg); if (GET_PLAYER((PlayerTypes)i).isAlive()) ++iAlive; }
	o << "players: at " << sg.GetPosition() << " of " << sg.GetEOF() << ", alive " << iAlive << (sg.m_bOverrun ? " (OVERRUN)" : "") << "\n";
	// HARNESS_RESEED=n: another continuation of the same save (the game's
	// synchronized random sequence restarts from n).
	if (getenv("HARNESS_RESEED") != NULL)
	{
		const unsigned long ulSeed = strtoul(getenv("HARNESS_RESEED"), NULL, 10);
		GC.getGameINLINE().getSorenRand().reseed(ulSeed);
		o << "sync random reseeded with " << ulSeed << "\n";
	}
	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		CvPlayerAI& k = GET_PLAYER((PlayerTypes)i);
		if (!k.isAlive()) continue;
		o << "  player " << i << " " << GC.getLeaderHeadInfo(k.getLeaderType()).getType() << (k.isHuman() ? " HUMAN" : "")
		  << " cities " << k.getNumCities() << " units " << k.getNumUnits() << " turnActive " << k.isTurnActive() << "\n";
	}
	const std::string s = o.str();
	_snprintf(szLog, iLogSize, "%s", s.c_str());
	szLog[iLogSize - 1] = 0;
	return (si.m_bOverrun || sg.m_bOverrun) ? -2 : iAlive;
}

// Python events the DLL reports (CvDllPythonEvents::report*), counted because the
// harness runs without Python: build_dll.sh adds a call at the top of each one.
// In the game each becomes a Python call with wrapped arguments.
namespace { std::map<std::string, long> g_eventCounts; }
void HH_countEvent(const char* szEvent) { ++g_eventCounts[szEvent]; }
extern "C" __declspec(dllexport) int HH_eventCounts(char* szBuf, int iSize)
{
	std::ostringstream o;
	for (std::map<std::string, long>::const_iterator it = g_eventCounts.begin(); it != g_eventCounts.end(); ++it)
		o << it->first << " " << it->second << "\n";
	const std::string s = o.str();
	_snprintf(szBuf, iSize, "%s", s.c_str());
	szBuf[iSize - 1] = 0;
	return (int)s.size();
}

// A snapshot in the format HH_loadSave reads: the init core and the game
// stream (game, map, teams, players), as the engine writes a save. Returns the
// size of the game stream, or -1 if a file cannot be written.
extern "C" __declspec(dllexport) int HH_saveState(const char* szInit, const char* szGame)
{
	MemStream si, sg;
	std::ostringstream idx;   // where each part ends, for comparing snapshots
	GC.getInitCore().write(&si);
	GC.getGameINLINE().write(&sg);
	idx << "game " << sg.GetEOF() << "\n";
	GC.getMapINLINE().write(&sg);
	idx << "map " << sg.GetEOF() << "\n";
	for (int i = 0; i < MAX_TEAMS; ++i) { GET_TEAM((TeamTypes)i).write(&sg); idx << "team" << i << " " << sg.GetEOF() << "\n"; }
	for (int i = 0; i < MAX_PLAYERS; ++i) { GET_PLAYER((PlayerTypes)i).write(&sg); idx << "player" << i << " " << sg.GetEOF() << "\n"; }
	if (!si.save(szInit) || !sg.save(szGame)) return -1;
	FILE* f = fopen((std::string(szGame) + ".idx").c_str(), "w");
	if (f != NULL) { fputs(idx.str().c_str(), f); fclose(f); }
	// HARNESS_SNAPSHOT_OBJECTS=1: every plot group, city, unit and selection
	// group written on its own (<game>.obj, index in <game>.objidx), to locate
	// a difference between two snapshots.
	if (getenv("HARNESS_SNAPSHOT_OBJECTS") != NULL)
	{
		MemStream so;
		std::ostringstream oidx;
		for (int i = 0; i < MAX_PLAYERS; ++i)
		{
			CvPlayerAI& k = GET_PLAYER((PlayerTypes)i);
			if (!k.isAlive()) continue;
			int iLoop;
			unsigned int uiStart;
			for (CvPlotGroup* pGroup = k.firstPlotGroup(&iLoop); pGroup != NULL; pGroup = k.nextPlotGroup(&iLoop))
			{
				uiStart = so.GetEOF(); pGroup->write(&so);
				oidx << i << " plotgroup " << pGroup->getID() << " " << uiStart << " " << so.GetEOF() << "\n";
			}
			for (CvCity* pCity = k.firstCity(&iLoop); pCity != NULL; pCity = k.nextCity(&iLoop))
			{
				uiStart = so.GetEOF(); static_cast<CvCityAI*>(pCity)->write(&so);
				oidx << i << " city " << pCity->getID() << " " << uiStart << " " << so.GetEOF() << "\n";
			}
			for (CvUnit* pUnit = k.firstUnit(&iLoop); pUnit != NULL; pUnit = k.nextUnit(&iLoop))
			{
				uiStart = so.GetEOF(); static_cast<CvUnitAI*>(pUnit)->write(&so);
				oidx << i << " unit " << pUnit->getID() << " " << uiStart << " " << so.GetEOF() << "\n";
			}
			for (CvSelectionGroup* pSel = k.firstSelectionGroup(&iLoop); pSel != NULL; pSel = k.nextSelectionGroup(&iLoop))
			{
				uiStart = so.GetEOF(); static_cast<CvSelectionGroupAI*>(pSel)->write(&so);
				oidx << i << " group " << pSel->getID() << " " << uiStart << " " << so.GetEOF() << "\n";
			}
		}
		so.save((std::string(szGame) + ".obj").c_str());
		FILE* fo = fopen((std::string(szGame) + ".objidx").c_str(), "w");
		if (fo != NULL) { fputs(oidx.str().c_str(), fo); fclose(fo); }
	}
	return (int)sg.GetEOF();
}

// For players whose turn is still open: their turn flags and every group that
// is ready to move or busy (head unit, UnitAI, position, moves, activity,
// mission queue head, mission AI). Used when a turn does not end.
extern "C" __declspec(dllexport) int HH_stuckReport(char* szBuf, int iSize)
{
	const HarnessPeekGuard kNoSideEffects;
	std::ostringstream o;
	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		CvPlayerAI& k = GET_PLAYER((PlayerTypes)i);
		if (!k.isAlive() || !k.isTurnActive()) continue;
		o << "player " << i << " " << GC.getLeaderHeadInfo(k.getLeaderType()).getType() << " human " << k.isHuman()
		  << " autoMoves " << k.isAutoMoves() << " endTurn " << k.isEndTurn() << " busyUnit " << k.hasBusyUnit()
		  << " readyUnit " << k.hasReadyUnit(true) << "\n";
		int iLoop;
		int iShown = 0;
		for (CvSelectionGroup* g = k.firstSelectionGroup(&iLoop); g != NULL; g = k.nextSelectionGroup(&iLoop))
		{
			const bool bReady = g->readyToMove(true), bBusy = g->isBusy();
			if (!bReady && !bBusy) continue;
			CvUnit* h = g->getHeadUnit();
			CvPlot* pMission = g->AI_getMissionAIPlot();
			CLLNode<MissionData>* m = g->headMissionQueueNode();
			o << "  group " << g->getID() << (bReady ? " READY" : "") << (bBusy ? " BUSY" : "") << " units " << g->getNumUnits();
			if (h != NULL)
				o << " head " << GC.getUnitInfo(h->getUnitType()).getType() << " ai " << (int)h->AI_getUnitAIType()
				  << " at " << h->getX_INLINE() << "," << h->getY_INLINE() << " moves " << h->getMoves() << "/" << h->maxMoves()
				  << " cargo " << h->getCargo() << " transport " << (h->getTransportUnit() ? h->getTransportUnit()->getID() : -1);
			o << " activity " << (int)g->getActivityType() << " queue " << g->getLengthMissionQueue();
			if (m != NULL) o << " mission " << (int)m->m_data.eMissionType << " to " << m->m_data.iData1 << "," << m->m_data.iData2;
			o << " missionAI " << (int)g->AI_getMissionAIType();
			if (pMission != NULL) o << " -> " << pMission->getX_INLINE() << "," << pMission->getY_INLINE();
			o << "\n";
			if (++iShown >= 40) { o << "  ...\n"; break; }
		}
	}
	const std::string s = o.str();
	_snprintf(szBuf, iSize, "%s", s.c_str());
	szBuf[iSize - 1] = 0;
	return (int)std::min((size_t)iSize - 1, s.size());
}

// Info counts that size the arrays in saved records (for checking a save's layout).
extern "C" __declspec(dllexport) int HH_infoCounts(char* szBuf, int iSize)
{
	return _snprintf(szBuf, iSize,
		"units %d unitclasses %d buildingclasses %d buildings %d projects %d civics %d votes %d religions %d corporations %d votesources %d "
		"specialunits %d specialbuildings %d techs %d bonuses %d improvements %d features %d terrains %d routes %d promotions %d "
		"civs %d leaders %d handicaps %d speeds %d eras %d specialists %d hurries %d upkeeps %d cultures %d emphasize %d events %d eventtriggers %d "
		"espionagemissions %d builds %d gameoptions %d players %d\n",
		GC.getNumUnitInfos(), GC.getNumUnitClassInfos(), GC.getNumBuildingClassInfos(), GC.getNumBuildingInfos(), GC.getNumProjectInfos(),
		GC.getNumCivicInfos(), GC.getNumVoteInfos(), GC.getNumReligionInfos(), GC.getNumCorporationInfos(), GC.getNumVoteSourceInfos(),
		GC.getNumSpecialUnitInfos(), GC.getNumSpecialBuildingInfos(), GC.getNumTechInfos(), GC.getNumBonusInfos(), GC.getNumImprovementInfos(),
		GC.getNumFeatureInfos(), GC.getNumTerrainInfos(), GC.getNumRouteInfos(), GC.getNumPromotionInfos(), GC.getNumCivilizationInfos(),
		GC.getNumLeaderHeadInfos(), GC.getNumHandicapInfos(), GC.getNumGameSpeedInfos(), GC.getNumEraInfos(), GC.getNumSpecialistInfos(),
		GC.getNumHurryInfos(), GC.getNumUpkeepInfos(), GC.getNumCultureLevelInfos(), GC.getNumEmphasizeInfos(), GC.getNumEventInfos(),
		GC.getNumEventTriggerInfos(), GC.getNumEspionageMissionInfos(), GC.getNumBuildInfos(), (int)NUM_GAMEOPTION_TYPES, MAX_PLAYERS);
}

// Hand every human seat to the AI for iTurns turns (the mod's AIAutoPlay), as
// when a save was made during an autorun. Returns the number of seats handed over.
extern "C" __declspec(dllexport) int HH_autoPlayHumans(int iTurns)
{
	int iCount = 0;
	for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
	{
		CvPlayerAI& k = GET_PLAYER((PlayerTypes)i);
		if (k.isAlive() && (k.isHuman() || k.isHumanDisabled()))
		{
			GC.getGameINLINE().setAIAutoPlay((PlayerTypes)i, iTurns);
			++iCount;
		}
	}
	return iCount;
}
