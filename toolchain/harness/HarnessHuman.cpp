// Harness-only: a model of the human player's strategic decisions for one seat (the "human model").
//
// The seat is an ordinary AI player; this file takes over the decisions the studies of the logged
// games describe (research/ai-warfare/study/playstyle.md and humanmodel.md) and leaves everything else
// (unit moves, combat, workers, the slider, diplomacy other than tech sales) to the AI. Every decision
// goes through the game's own functions (pushResearch, revolution, pushOrder, AI_setWarPlan,
// AI_considerOffer and implementDeal), so the seat follows the rules and the other AIs answer it as
// they answer any player.
//
// Switches (environment):
//   HARNESS_HM_PLAYER=<id>   the seat; without it nothing here acts
//   HARNESS_HM_POLICY=<file> the policy, written by research/ai-warfare/tools/hmpolicy.py:
//       TECH <type>                       research order: the first tech that can be researched
//       CIVIC <option> <tier> <tier> ...  per option, tiers in order, later preferred; a tier is one
//                                         civic or several joined by '|', of which the AI's own civic
//                                         value picks one; a tier marked '*' (the human waited) is taken
//                                         only when the AI values it above the civic held from the tier before
//       BUILD <buildingclass>             the template of every city but the capital, in order
//       PARAM <name> <value>              see Param() below
//   HARNESS_HM_OFF=a,b,...    components left to the AI: research, civics, slider, cities, expand, war, tactics, trade, upgrade
//   HARNESS_HM_LOG=<file>    one line per decision: turn, kind, details
//
// Hooks (build_dll.sh adds them in its copy of the source): at the top of CvPlayerAI::AI_chooseResearch,
// CvPlayerAI::AI_doCivics, CvPlayerAI::AI_doCommerce, CvPlayerAI::AI_unitUpdate, CvCityAI::AI_chooseProduction, CvTeamAI::AI_doWar and CvPlayerAI::AI_doDiplo,
// and after the AI_doWar call in CvTeamAI::AI_doTurnPost.
#include "CvGameCoreDLL.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvUnitAI.h"
#include "CvCityAI.h"
#include "CvInfos.h"
#include "CvGameCoreUtils.h"
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <set>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>

namespace
{
	struct Policy
	{
		bool bLoaded, bActive;
		int iPlayer;
		std::set<std::string> off;
		std::vector<int> techs;
		std::vector<std::pair<int, std::vector<std::vector<int> > > > civics;   // option -> tiers, later preferred
		std::map<std::pair<int, int>, bool> lateTier;                            // (option entry, tier) -> the human waited
		std::vector<int> build;                                                  // building classes
		std::map<std::string, int> params;
		FILE* log;
		// war state
		int iState;            // 0 idle, 1 preparing (PREPARING_TOTAL), 2 marching (TOTAL, not yet at war), 3 at war
		int iTarget;           // team
		int iSince;            // turn the state began
		int iTargetCities;     // the target's cities at the last turn of the war
		int iCaptures;         // cities the target lost in this war
		int iLastCaptureTurn;
		int iLastPeaceTry;
		int iIdleSince;        // turn the last war or preparation ended
		int iLastSale;
		std::map<int, int> aiPicks;   // city id -> template picks since the AI's last pick
		Policy() : bLoaded(false), bActive(false), iPlayer(-1), log(NULL), iState(0), iTarget(-1), iSince(0),
			iTargetCities(0), iCaptures(0), iLastCaptureTurn(0), iLastPeaceTry(-100), iIdleSince(-100), iLastSale(-100) {}
	};
	Policy g;

	int infoType(const std::string& s)
	{
		return GC.getInfoTypeForString(s.c_str(), true);
	}

	void load()
	{
		if (g.bLoaded) return;
		g.bLoaded = true;
		const char* szP = getenv("HARNESS_HM_PLAYER");
		if (szP == NULL) return;
		g.iPlayer = atoi(szP);
		g.bActive = g.iPlayer >= 0 && g.iPlayer < MAX_CIV_PLAYERS;
		const char* szOff = getenv("HARNESS_HM_OFF");
		if (szOff != NULL)
		{
			std::stringstream ss(szOff); std::string t;
			while (std::getline(ss, t, ',')) if (!t.empty()) g.off.insert(t);
		}
		const char* szLog = getenv("HARNESS_HM_LOG");
		if (szLog != NULL) g.log = fopen(szLog, "w");
		const char* szPol = getenv("HARNESS_HM_POLICY");
		int nUnknown = 0;
		if (szPol != NULL)
		{
			std::ifstream in(szPol);
			std::string line;
			while (std::getline(in, line))
			{
				std::stringstream ls(line); std::string k; ls >> k;
				if (k == "TECH") { std::string t; ls >> t; int e = infoType(t); if (e >= 0) g.techs.push_back(e); else ++nUnknown; }
				else if (k == "CIVIC")
				{
					std::string o, tier; ls >> o; const int eO = infoType(o);
					std::vector<std::vector<int> > v;
					while (ls >> tier)
					{
						if (!tier.empty() && tier[0] == '*') { g.lateTier[std::make_pair((int)g.civics.size(), (int)v.size())] = true; tier = tier.substr(1); }
						std::vector<int> t; std::stringstream ts(tier); std::string c;
						while (std::getline(ts, c, '|')) { int e = infoType(c); if (e >= 0) t.push_back(e); else ++nUnknown; }
						if (!t.empty()) v.push_back(t);
					}
					if (eO >= 0) g.civics.push_back(std::make_pair(eO, v)); else ++nUnknown;
				}
				else if (k == "BUILD") { std::string c; ls >> c; int e = infoType(c); if (e >= 0) g.build.push_back(e); else ++nUnknown; }
				else if (k == "PARAM") { std::string n; int v = 0; ls >> n >> v; g.params[n] = v; }
			}
		}
		if (g.log) fprintf(g.log, "policy seat=%d techs=%d civic_options=%d build=%d params=%d unknown=%d off=%s\n", g.iPlayer,
			(int)g.techs.size(), (int)g.civics.size(), (int)g.build.size(), (int)g.params.size(), nUnknown, szOff ? szOff : "-");
	}

	bool on(int iPlayer, const char* szPart)
	{
		load();
		return g.bActive && iPlayer == g.iPlayer && g.off.find(szPart) == g.off.end();
	}

	// Parameters (hmpolicy.py writes each from the logged games; these defaults are only fallbacks).
	int Param(const char* n, int iDefault)
	{
		std::map<std::string, int>::const_iterator it = g.params.find(n);
		return it == g.params.end() ? iDefault : it->second;
	}

	void note(const char* szFmt, ...)
	{
		if (!g.log) return;
		fprintf(g.log, "%d ", GC.getGameINLINE().getGameTurn());
		va_list a; va_start(a, szFmt); vfprintf(g.log, szFmt, a); va_end(a);
		fprintf(g.log, "\n"); fflush(g.log);
	}

	bool inWarMode() { return g.iState != 0; }

	// Grid distance between the nearest cities of two teams, MAX_INT if either has none.
	int teamDistance(TeamTypes eA, TeamTypes eB)
	{
		int iBest = MAX_INT, iL1, iL2;
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			CvPlayer& kA = GET_PLAYER((PlayerTypes)i);
			if (!kA.isAlive() || kA.getTeam() != eA) continue;
			for (CvCity* a = kA.firstCity(&iL1); a != NULL; a = kA.nextCity(&iL1))
				for (int j = 0; j < MAX_CIV_PLAYERS; ++j)
				{
					CvPlayer& kB = GET_PLAYER((PlayerTypes)j);
					if (!kB.isAlive() || kB.getTeam() != eB) continue;
					for (CvCity* b = kB.firstCity(&iL2); b != NULL; b = kB.nextCity(&iL2))
						iBest = std::min(iBest, plotDistance(a->getX_INLINE(), a->getY_INLINE(), b->getX_INLINE(), b->getY_INLINE()));
				}
		}
		return iBest;
	}

	// The seat's land units that can fight within two plots of a city of the target team.
	int unitsNear(const CvPlayerAI& k, TeamTypes eTarget)
	{
		int n = 0, iLoop, iCityLoop;
		for (CvUnit* u = k.firstUnit(&iLoop); u != NULL; u = k.nextUnit(&iLoop))
		{
			if (!u->canFight() || u->getDomainType() != DOMAIN_LAND) continue;
			bool bNear = false;
			for (int j = 0; j < MAX_CIV_PLAYERS && !bNear; ++j)
			{
				CvPlayer& kJ = GET_PLAYER((PlayerTypes)j);
				if (!kJ.isAlive() || kJ.getTeam() != eTarget) continue;
				for (CvCity* c = kJ.firstCity(&iCityLoop); c != NULL && !bNear; c = kJ.nextCity(&iCityLoop))
					bNear = plotDistance(u->getX_INLINE(), u->getY_INLINE(), c->getX_INLINE(), c->getY_INLINE()) <= 2;
			}
			if (bNear) ++n;
		}
		return n;
	}

	int warsWith(const CvTeamAI& t)
	{
		int n = 0;
		for (int i = 0; i < MAX_CIV_TEAMS; ++i) if (i != t.getID() && GET_TEAM((TeamTypes)i).isAlive() && t.isAtWar((TeamTypes)i)) ++n;
		return n;
	}

	bool offensivePlan(WarPlanTypes e)
	{
		return e == WARPLAN_PREPARING_LIMITED || e == WARPLAN_PREPARING_TOTAL || e == WARPLAN_LIMITED || e == WARPLAN_TOTAL || e == WARPLAN_DOGPILE;
	}

	void upgradeAll(CvPlayerAI& k)
	{
		if (!on(k.getID(), "upgrade")) return;
		int iLoop, iGold = k.getGold();
		for (CvUnit* u = k.firstUnit(&iLoop); u != NULL; u = k.nextUnit(&iLoop))
		{
			if (u->canFight()) ((CvUnitAI*)u)->AI_upgrade();
		}
		if (k.getGold() != iGold) note("upgrade gold %d -> %d", iGold, k.getGold());
	}

	bool tryPeace(CvTeamAI& t, TeamTypes eTarget)
	{
		const PlayerTypes eMe = t.getLeaderID(), eThem = GET_TEAM(eTarget).getLeaderID();
		int iGold = std::min(GET_PLAYER(eThem).AI_maxGoldTrade(eMe), GET_PLAYER(eThem).getGold());
		for (int pass = 0; pass < 2; ++pass)
		{
			CLinkList<TradeData> ours, theirs;
			TradeData item;
			setTradeItem(&item, TRADE_PEACE_TREATY); ours.insertAtEnd(item); theirs.insertAtEnd(item);
			if (pass == 0 && iGold > 0) { setTradeItem(&item, TRADE_GOLD, iGold); theirs.insertAtEnd(item); }
			if (GET_PLAYER(eThem).AI_considerOffer(eMe, &ours, &theirs))
			{
				GC.getGameINLINE().implementDeal(eMe, eThem, &ours, &theirs, true);
				note("peace with %d gold %d", (int)eTarget, pass == 0 ? iGold : 0);
				return true;
			}
		}
		note("peace refused by %d", (int)eTarget);
		return false;
	}

	void endWar(CvTeamAI& t, const char* szWhy)
	{
		if (g.iTarget >= 0 && !t.isAtWar((TeamTypes)g.iTarget) && offensivePlan(t.AI_getWarPlan((TeamTypes)g.iTarget)))
			t.AI_setWarPlan((TeamTypes)g.iTarget, NO_WARPLAN);
		note("war state %d against %d ends: %s", g.iState, g.iTarget, szWhy);
		g.iState = 0; g.iTarget = -1; g.iIdleSince = GC.getGameINLINE().getGameTurn();
	}
}

// Research: the first tech of the policy's order that can be researched now.
bool HH_hmResearch(CvPlayerAI* p)
{
	if (!on(p->getID(), "research")) return false;
	for (size_t i = 0; i < g.techs.size(); ++i)
	{
		if (p->canResearch((TechTypes)g.techs[i]))
		{
			p->clearResearchQueue();
			p->pushResearch((TechTypes)g.techs[i]);
			note("research %s", GC.getTechInfo((TechTypes)g.techs[i]).getType());
			return true;
		}
	}
	return false;   // the list is exhausted: the AI chooses
}

// Civics: in each option the latest tier with a civic that can be adopted. A civic held from that tier
// is kept; otherwise the AI's value picks within the tier, and for a tier marked late the civic held
// from the tier before (or, for the first tier, the civic held) is kept while the AI values it at least
// as much. One revolution for all changes.
bool HH_hmCivics(CvPlayerAI* p)
{
	if (!on(p->getID(), "civics")) return false;
	const int nO = GC.getNumCivicOptionInfos();
	std::vector<CivicTypes> v(nO);
	for (int o = 0; o < nO; ++o) v[o] = p->getCivics((CivicOptionTypes)o);
	bool bChange = false;
	for (size_t i = 0; i < g.civics.size(); ++i)
	{
		const int o = g.civics[i].first;
		const std::vector<std::vector<int> >& tiers = g.civics[i].second;
		const int held = v[o];
		for (int j = (int)tiers.size() - 1; j >= 0; --j)
		{
			int iBest = -1, iBestValue = MIN_INT;
			bool bHeldHere = false;
			for (size_t m = 0; m < tiers[j].size(); ++m)
			{
				const int c = tiers[j][m];
				if (c == held) bHeldHere = true;
				if (!p->canDoCivics((CivicTypes)c)) continue;
				const int iValue = tiers[j].size() > 1 ? p->AI_civicValue((CivicTypes)c) : 0;
				if (iValue > iBestValue) { iBestValue = iValue; iBest = c; }
			}
			if (iBest < 0) continue;
			if (bHeldHere) break;
			if (g.lateTier.count(std::make_pair((int)i, j)))
			{
				bool bStay = j == 0;
				if (j > 0) for (size_t m = 0; m < tiers[j - 1].size(); ++m) if (tiers[j - 1][m] == held) bStay = true;
				if (bStay && p->AI_civicValue((CivicTypes)held) >= p->AI_civicValue((CivicTypes)iBest)) break;
			}
			v[o] = (CivicTypes)iBest; bChange = true;
			break;
		}
	}
	if (bChange && p->canRevolution(&v[0]))
	{
		std::string s;
		for (int o = 0; o < nO; ++o) if (v[o] != p->getCivics((CivicOptionTypes)o)) { s += " "; s += GC.getCivicInfo(v[o]).getType(); }
		p->revolution(&v[0]);
		note("civics%s", s.c_str());
	}
	return true;   // the AI's own civic choice never runs for this seat
}

// The slider: research at the highest rate whose gold per turn is not negative (culture and
// espionage at zero), as the human ran it.
bool HH_hmCommerce(CvPlayerAI* p)
{
	if (!on(p->getID(), "slider") || !p->isCommerceFlexible(COMMERCE_RESEARCH)) return false;
	if (p->isCommerceFlexible(COMMERCE_CULTURE)) p->setCommercePercent(COMMERCE_CULTURE, 0);
	if (p->isCommerceFlexible(COMMERCE_ESPIONAGE)) p->setCommercePercent(COMMERCE_ESPIONAGE, 0);
	const int iStep = std::max(1, GC.getDefineINT("COMMERCE_PERCENT_CHANGE_INCREMENTS"));
	const int iOld = p->getCommercePercent(COMMERCE_RESEARCH);
	int iPct = 100;
	for (; iPct > 0; iPct -= iStep)
	{
		p->setCommercePercent(COMMERCE_RESEARCH, iPct);
		if (p->calculateGoldRate() >= 0) break;
	}
	if (iPct <= 0) p->setCommercePercent(COMMERCE_RESEARCH, 0);
	if (p->getCommercePercent(COMMERCE_RESEARCH) != iOld) note("slider research %d", p->getCommercePercent(COMMERCE_RESEARCH));
	return true;
}

// City production: the capital and cities in danger or without a defender are the AI's; so is one
// choice in every ai_every (ai_every_war during a war or its preparation), which is where the AI
// builds its units. Every other choice: a settler when the seat has a site and no settler, else the
// first building of the template the city can build, else the AI's.
bool HH_hmChooseProduction(CvCityAI* c)
{
	if (!on(c->getOwnerINLINE(), "cities")) return false;
	CvPlayerAI& k = GET_PLAYER(c->getOwnerINLINE());
	if (c->isCapital()) return false;
	if (c->plot()->getNumDefenders(c->getOwnerINLINE()) < 1 || c->AI_isDanger()) return false;
	if (c->getOrderQueueLength() > 0 && c->getProduction() > 0) return true;     // keep what is under way
	int& iPicks = g.aiPicks[c->getID()];
	const int iEvery = inWarMode() ? Param("ai_every_war", 2) : Param("ai_every", 3);
	if (iEvery > 0 && iPicks >= iEvery - 1) { iPicks = 0; return false; }
	const CvCivilizationInfo& kCiv = GC.getCivilizationInfo(k.getCivilizationType());
	if (on(k.getID(), "expand") && k.AI_getNumCitySites() > 0 && c->getPopulation() >= Param("settler_min_pop", 3)
		&& k.getNumCities() < Param("max_cities", 40))
	{
		const UnitClassTypes eClass = (UnitClassTypes)GC.getInfoTypeForString("UNITCLASS_SETTLER");
		const UnitTypes eSettler = (UnitTypes)kCiv.getCivilizationUnits(eClass);
		if (eSettler != NO_UNIT && k.getUnitClassCountPlusMaking(eClass) == 0 && c->canTrain(eSettler))
		{
			c->pushOrder(ORDER_TRAIN, eSettler, -1, false, false, false);
			note("city %d,%d train %s", c->getX_INLINE(), c->getY_INLINE(), GC.getUnitInfo(eSettler).getType());
			++iPicks;
			return true;
		}
	}
	for (size_t i = 0; i < g.build.size(); ++i)
	{
		const BuildingTypes b = (BuildingTypes)kCiv.getCivilizationBuildings(g.build[i]);
		if (b == NO_BUILDING || c->getNumBuilding(b) > 0 || !c->canConstruct(b)) continue;
		c->pushOrder(ORDER_CONSTRUCT, b, -1, false, false, false);
		note("city %d,%d build %s", c->getX_INLINE(), c->getY_INLINE(), GC.getBuildingInfo(b).getType());
		++iPicks;
		return true;
	}
	return false;
}

// War, before the AI's own war planning runs (which then still keeps the plans and answers wars on the
// seat): one war of its own at a time, on the nearest team the seat outweighs by decl_ratio_pct;
// prep_min_turns of preparation (WARPLAN_PREPARING_TOTAL), then WARPLAN_TOTAL, under which the AI's
// stacks march (and may declare as they cross the border); the seat declares itself once decl_units
// of its fighting units stand within two plots of the target's cities, as the human declared with the
// army at the cities;
// peace once no city has fallen for war_stall_turns after the first capture, or after war_max_turns,
// asking the loser for its gold.
bool HH_hmDoWar(CvTeamAI* t)
{
	if (!on(t->getLeaderID(), "war")) return false;
	CvGame& kGame = GC.getGameINLINE();
	const int iTurn = kGame.getGameTurn();
	const int iPow = std::max(1, t->getPower(true));
	CvPlayerAI& kMe = GET_PLAYER(t->getLeaderID());
	if (g.iState != 0)
	{
		CvTeamAI& kT = GET_TEAM((TeamTypes)g.iTarget);
		if (!kT.isAlive()) { endWar(*t, "target eliminated"); return false; }
		upgradeAll(kMe);
		if (g.iState == 3)
		{
			if (!t->isAtWar((TeamTypes)g.iTarget)) { endWar(*t, "peace"); return false; }
			if (kT.getNumCities() < g.iTargetCities) { g.iCaptures += g.iTargetCities - kT.getNumCities(); g.iLastCaptureTurn = iTurn; }
			g.iTargetCities = kT.getNumCities();
			const bool bStall = g.iCaptures > 0 && iTurn - g.iLastCaptureTurn >= Param("war_stall_turns", 2);
			const bool bLong = iTurn - g.iSince >= Param("war_max_turns", 6);
			if ((bStall || bLong) && iTurn > g.iLastPeaceTry)
			{
				g.iLastPeaceTry = iTurn;
				if (tryPeace(*t, (TeamTypes)g.iTarget)) endWar(*t, "peace made");
			}
			return false;
		}
		if (t->isAtWar((TeamTypes)g.iTarget))
		{
			note("at war with %d after %d turns of state %d, ratio %d", g.iTarget, iTurn - g.iSince, g.iState,
				iPow * 100 / std::max(1, kT.getPower(true)));
			g.iState = 3; g.iSince = iTurn; g.iCaptures = 0; g.iLastCaptureTurn = iTurn; g.iTargetCities = kT.getNumCities();
			return false;
		}
		if (!t->canDeclareWar((TeamTypes)g.iTarget)) { endWar(*t, "cannot declare"); return false; }
		if (iTurn - g.iSince > Param("prep_max_turns", 30)) { endWar(*t, "no declaration in time"); return false; }
		if (g.iState == 2 && unitsNear(kMe, (TeamTypes)g.iTarget) >= Param("decl_units", 5))
		{
			note("declare on %d with %d units near", g.iTarget, unitsNear(kMe, (TeamTypes)g.iTarget));
			t->declareWar((TeamTypes)g.iTarget, true, WARPLAN_TOTAL);
			return false;   // the next turn records the war
		}
		if (g.iState == 1 && iTurn - g.iSince >= Param("prep_min_turns", 3))
		{
			t->AI_setWarPlan((TeamTypes)g.iTarget, WARPLAN_TOTAL);
			g.iState = 2;
			note("march on %d", g.iTarget);
		}
		else if (t->AI_getWarPlan((TeamTypes)g.iTarget) != (g.iState == 1 ? WARPLAN_PREPARING_TOTAL : WARPLAN_TOTAL))
		{
			t->AI_setWarPlan((TeamTypes)g.iTarget, g.iState == 1 ? WARPLAN_PREPARING_TOTAL : WARPLAN_TOTAL);
		}
		return false;
	}
	if (iTurn < Param("war_min_turn", 193) || iTurn - g.iIdleSince < Param("war_gap_turns", 3)) return false;
	if (warsWith(*t) >= Param("max_wars", 1)) return false;
	int iBest = -1, iBestD = MAX_INT, iBestRatio = 0;
	for (int i = 0; i < MAX_CIV_TEAMS; ++i)
	{
		CvTeamAI& kT = GET_TEAM((TeamTypes)i);
		if (i == t->getID() || !kT.isAlive() || kT.isBarbarian() || kT.isMinorCiv() || !t->isHasMet((TeamTypes)i)) continue;
		if (kT.getNumCities() == 0 || t->isAtWar((TeamTypes)i) || !t->canDeclareWar((TeamTypes)i)) continue;
		const int iRatio = iPow * 100 / std::max(1, kT.getPower(true));
		if (iRatio < Param("decl_ratio_pct", 200)) continue;
		const int d = teamDistance(t->getID(), (TeamTypes)i);
		if (d < iBestD) { iBest = i; iBestD = d; iBestRatio = iRatio; }
	}
	if (iBest < 0 || iBestD > Param("max_distance", 30)) return false;
	g.iState = 1; g.iTarget = iBest; g.iSince = iTurn;
	t->AI_setWarPlan((TeamTypes)iBest, WARPLAN_PREPARING_TOTAL);
	note("prepare against %d ratio %d distance %d", iBest, iBestRatio, iBestD);
	return false;
}

// After the AI's war planning: plans it started against anyone the model did not choose are dropped
// before any unit can act on them (wars already under way, and wars on the seat, are left to the AI).
void HH_hmAfterWar(CvTeamAI* t)
{
	if (!on(t->getLeaderID(), "war")) return;
	for (int i = 0; i < MAX_CIV_TEAMS; ++i)
	{
		if (i == t->getID() || i == g.iTarget || !GET_TEAM((TeamTypes)i).isAlive() || t->isAtWar((TeamTypes)i)) continue;
		const WarPlanTypes e = t->AI_getWarPlan((TeamTypes)i);
		if (offensivePlan(e))
		{
			t->AI_setWarPlan((TeamTypes)i, NO_WARPLAN);
			note("dropped AI plan %d against %d", (int)e, i);
		}
	}
}

// Tech sales: from trade_min_turn, one sale every trade_every turns at most: the cheapest tech the
// seat can trade to the AI that can pay most (at least trade_min_gold), for that gold; never to the
// war target.
void HH_hmDiplo(CvPlayerAI* p)
{
	if (!on(p->getID(), "trade")) return;
	const int iTurn = GC.getGameINLINE().getGameTurn();
	if (iTurn < Param("trade_min_turn", 261) || iTurn - g.iLastSale < Param("trade_every", 4)) return;
	int iBestJ = -1, iBestGold = 0;
	for (int j = 0; j < MAX_CIV_PLAYERS; ++j)
	{
		CvPlayerAI& kJ = GET_PLAYER((PlayerTypes)j);
		if (j == p->getID() || !kJ.isAlive() || kJ.isBarbarian() || kJ.isMinorCiv()) continue;
		if (!GET_TEAM(p->getTeam()).isHasMet(kJ.getTeam()) || GET_TEAM(p->getTeam()).isAtWar(kJ.getTeam())) continue;
		if (inWarMode() && kJ.getTeam() == g.iTarget) continue;
		const int iGold = std::min(kJ.AI_maxGoldTrade(p->getID()), kJ.getGold());
		if (iGold >= Param("trade_min_gold", 200) && iGold > iBestGold) { iBestGold = iGold; iBestJ = j; }
	}
	if (iBestJ < 0) return;
	int iBestTech = -1, iBestCost = MAX_INT;
	for (int t = 0; t < GC.getNumTechInfos(); ++t)
	{
		TradeData item; setTradeItem(&item, TRADE_TECHNOLOGIES, t);
		if (!p->canTradeItem((PlayerTypes)iBestJ, item, true)) continue;
		const int iCost = GC.getTechInfo((TechTypes)t).getResearchCost();
		if (iCost < iBestCost) { iBestCost = iCost; iBestTech = t; }
	}
	if (iBestTech < 0) return;
	CLinkList<TradeData> ours, theirs;
	TradeData a, b; setTradeItem(&a, TRADE_TECHNOLOGIES, iBestTech); setTradeItem(&b, TRADE_GOLD, iBestGold);
	ours.insertAtEnd(a); theirs.insertAtEnd(b);
	if (GET_PLAYER((PlayerTypes)iBestJ).AI_considerOffer(p->getID(), &ours, &theirs))
	{
		GC.getGameINLINE().implementDeal(p->getID(), (PlayerTypes)iBestJ, &ours, &theirs, true);
		g.iLastSale = iTurn;
		note("sold %s to %d for %d", GC.getTechInfo((TechTypes)iBestTech).getType(), iBestJ, iBestGold);
	}
}

// Tactics, at the top of each unit update while the seat is at war, before the AI moves anything: one
// of its land units attacks an adjacent enemy plot when its odds (getCombatOdds, per mille) reach
// attack_min_odds, or walks into an adjacent enemy city without defenders. One action per update;
// the AI's own moves follow once no such action is left (they may still attack at lower odds).
bool HH_hmTactics(CvPlayerAI* p)
{
	if (!on(p->getID(), "tactics")) return false;
	CvTeamAI& t = GET_TEAM(p->getTeam());
	if (warsWith(t) == 0 || p->hasBusyUnit()) return false;
	static int iTurn = -1;
	static std::set<int> tried;
	if (GC.getGameINLINE().getGameTurn() != iTurn) { iTurn = GC.getGameINLINE().getGameTurn(); tried.clear(); }
	const int iMin = Param("attack_min_odds", 710);
	int iLoop;
	for (CvUnit* u = p->firstUnit(&iLoop); u != NULL; u = p->nextUnit(&iLoop))
	{
		if (tried.count(u->getID()) || !u->canMove() || !u->canAttack() || u->getDomainType() != DOMAIN_LAND || u->isCargo() || u->isMadeAttack()) continue;
		for (int d = 0; d < NUM_DIRECTION_TYPES; ++d)
		{
			CvPlot* q = plotDirection(u->getX_INLINE(), u->getY_INLINE(), (DirectionTypes)d);
			if (q == NULL) continue;
			const bool bEnemyCity = q->isCity() && q->getTeam() != NO_TEAM && t.isAtWar(q->getTeam());
			CvUnit* pDef = q->getBestDefender(NO_PLAYER, p->getID(), u, true);
			int iOdds = 1000;
			if (pDef == NULL)
			{
				if (!bEnemyCity || !u->canMoveInto(q)) continue;
			}
			else
			{
				if (!u->canMoveInto(q, true)) continue;
				iOdds = getCombatOdds(u, pDef);
				if (iOdds < iMin) continue;
			}
			tried.insert(u->getID());
			if (u->getGroup()->getNumUnits() > 1) u->joinGroup(NULL);
			note("attack %s %d,%d -> %d,%d odds %d %s", GC.getUnitInfo(u->getUnitType()).getType(), u->getX_INLINE(), u->getY_INLINE(),
				q->getX_INLINE(), q->getY_INLINE(), iOdds, pDef == NULL ? "empty city" : (bEnemyCity ? "city" : "field"));
			u->getGroup()->pushMission(MISSION_MOVE_TO, q->getX_INLINE(), q->getY_INLINE(), MOVE_DIRECT_ATTACK);
			return true;
		}
	}
	return false;
}
