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
//   HARNESS_HM_OFF=a,b,...    components left to the AI: research, civics, slider, cities, expand, war, tactics, borders,
//                            trade, upgrade
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
#include <algorithm>
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
		// war state (study/war.md, section 10)
		int iState;            // 0 idle, 1 staging (the strike group marches to the objective), 3 at war
		int iTarget;           // team
		int iObjX, iObjY;      // the objective: a city of the target team
		int iStageX, iStageY;  // the staging plot, next to the objective
		int iSince;            // turn the state began
		int iTargetCities;     // the target's cities at the last turn of the war
		int iCaptures;         // cities the target lost in this war
		int iLastCaptureTurn;
		int iLastPeaceTry;
		int iIdleSince;        // turn the last war or preparation ended
		int iLastSale;
		int iLastOpenBorders;  // turn of the last round of open-borders offers
		std::set<int> strike;  // unit ids of the strike group
		std::map<int, int> aiPicks;   // city id -> template picks since the AI's last pick
		Policy() : bLoaded(false), bActive(false), iPlayer(-1), log(NULL), iState(0), iTarget(-1), iObjX(-1), iObjY(-1), iStageX(-1),
			iStageY(-1), iSince(0), iTargetCities(0), iCaptures(0), iLastCaptureTurn(0), iLastPeaceTry(-100), iIdleSince(-100),
			iLastSale(-100), iLastOpenBorders(-100) {}
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

	// The strike group goes back to the AI: its orders are cleared.
	void releaseStrike()
	{
		for (std::set<int>::const_iterator it = g.strike.begin(); it != g.strike.end(); ++it)
		{
			CvUnit* u = GET_PLAYER((PlayerTypes)g.iPlayer).getUnit(*it);
			if (u != NULL && u->getGroup() != NULL) u->getGroup()->clearMissionQueue();
		}
		g.strike.clear();
	}

	void endWar(CvTeamAI& t, const char* szWhy)
	{
		if (g.iTarget >= 0 && !t.isAtWar((TeamTypes)g.iTarget) && offensivePlan(t.AI_getWarPlan((TeamTypes)g.iTarget)))
			t.AI_setWarPlan((TeamTypes)g.iTarget, NO_WARPLAN);
		note("war state %d against %d ends: %s", g.iState, g.iTarget, szWhy);
		releaseStrike();
		g.iState = 0; g.iTarget = -1; g.iObjX = g.iObjY = g.iStageX = g.iStageY = -1; g.iIdleSince = GC.getGameINLINE().getGameTurn();
	}

	// Distance from a plot to the nearest city of a player.
	int distToCities(const CvPlayer& k, int x, int y)
	{
		int iBest = MAX_INT, iLoop;
		for (CvCity* c = k.firstCity(&iLoop); c != NULL; c = k.nextCity(&iLoop))
			iBest = std::min(iBest, plotDistance(x, y, c->getX_INLINE(), c->getY_INLINE()));
		return iBest;
	}

	bool hasCityInArea(const CvPlayer& k, int iArea)
	{
		int iLoop;
		for (CvCity* c = k.firstCity(&iLoop); c != NULL; c = k.nextCity(&iLoop)) if (c->getArea() == iArea) return true;
		return false;
	}

	// A land unit that can join a strike group: it can attack, and it is not the last defender a city keeps.
	bool strikeCandidate(CvUnit* u, PlayerTypes eMe)
	{
		if (u->getDomainType() != DOMAIN_LAND || !u->canAttack() || u->isCargo() || u->getUnitCombatType() == NO_UNITCOMBAT) return false;
		if (u->plot()->isCity() && u->plot()->getNumDefenders(eMe) <= Param("home_keep", 1)) return false;
		return true;
	}

	int ownUnitsNear(const CvPlayerAI& k, int x, int y, int r)
	{
		int n = 0, iLoop;
		for (CvUnit* u = k.firstUnit(&iLoop); u != NULL; u = k.nextUnit(&iLoop))
			if (u->getDomainType() == DOMAIN_LAND && u->canFight() && plotDistance(u->getX_INLINE(), u->getY_INLINE(), x, y) <= r) ++n;
		return n;
	}

	int strikeNear(int x, int y, int r)
	{
		int n = 0;
		for (std::set<int>::const_iterator it = g.strike.begin(); it != g.strike.end(); ++it)
		{
			CvUnit* u = GET_PLAYER((PlayerTypes)g.iPlayer).getUnit(*it);
			if (u != NULL && plotDistance(u->getX_INLINE(), u->getY_INLINE(), x, y) <= r) ++n;
		}
		return n;
	}

	// Odds (per mille) of a unit against the best defender of a city, as if at war; 1000 for an empty city.
	int oddsAgainst(CvUnit* u, CvCity* c)
	{
		CvUnit* pDef = c->plot()->getBestDefender(c->getOwnerINLINE(), u->getOwnerINLINE(), u);
		return pDef == NULL ? 1000 : getCombatOdds(u, pDef);
	}

	// Members of the strike group within two plots of the city that would attack it at attack_min_odds.
	int strikeCapable(CvCity* c)
	{
		int n = 0;
		for (std::set<int>::const_iterator it = g.strike.begin(); it != g.strike.end(); ++it)
		{
			CvUnit* u = GET_PLAYER((PlayerTypes)g.iPlayer).getUnit(*it);
			if (u != NULL && plotDistance(u->getX_INLINE(), u->getY_INLINE(), c->getX_INLINE(), c->getY_INLINE()) <= 2 &&
				oddsAgainst(u, c) >= Param("attack_min_odds", 710)) ++n;
		}
		return n;
	}

	// The staging plot of an objective: a land plot next to the city, free of other players' units, nearest
	// to the seat's cities; NULL if none.
	CvPlot* stagingPlot(const CvPlayer& kMe, CvCity* c)
	{
		CvPlot* pBest = NULL; int iBest = MAX_INT;
		for (int d = 0; d < NUM_DIRECTION_TYPES; ++d)
		{
			CvPlot* q = plotDirection(c->getX_INLINE(), c->getY_INLINE(), (DirectionTypes)d);
			if (q == NULL || q->isWater() || q->isImpassable() || q->isCity() || q->getArea() != c->getArea()) continue;
			if (q->isVisibleEnemyUnit(kMe.getID())) continue;
			bool bOther = false;
			for (CLLNode<IDInfo>* n = q->headUnitNode(); n != NULL; n = q->nextUnitNode(n))
				if (::getUnit(n->m_data) != NULL && ::getUnit(n->m_data)->getOwnerINLINE() != kMe.getID()) bOther = true;
			if (bOther) continue;
			const int v = distToCities(kMe, q->getX_INLINE(), q->getY_INLINE()) * 100 - q->defenseModifier(kMe.getTeam(), false);
			if (v < iBest) { iBest = v; pBest = q; }
		}
		return pBest;
	}

	// The objective: among the cities of teams the seat may attack and outweighs by prep_ratio_pct, with
	// open borders (or already at war), on a landmass where the seat has a city, within target_max_distance
	// of its cities, and that one of its strike candidates would attack at attack_min_odds (the human took
	// cities only at such odds): the nearest, then the one with most of its units within two plots.
	CvCity* chooseObjective(CvTeamAI& t, CvPlayerAI& kMe, int iOnlyTeam)
	{
		CvCity* pBest = NULL; int iBestD = MAX_INT, iBestNear = -1;
		const int iPow = std::max(1, t.getPower(true));
		int nMet = 0, nDeclarable = 0, nBorders = 0, nOutweighed = 0, nInReach = 0, nWinnable = 0;
		for (int i = 0; i < MAX_CIV_PLAYERS; ++i)
		{
			CvPlayer& kP = GET_PLAYER((PlayerTypes)i);
			const TeamTypes eT = kP.getTeam();
			if (!kP.isAlive() || eT == t.getID() || kP.isBarbarian() || kP.isMinorCiv() || !t.isHasMet(eT)) continue;
			if (iOnlyTeam >= 0 && eT != iOnlyTeam) continue;
			++nMet;
			if (iOnlyTeam < 0)
			{
				if (t.isAtWar(eT) || !t.canDeclareWar(eT)) continue;
				++nDeclarable;
				if (!t.isOpenBorders(eT)) continue;
				++nBorders;
				if (iPow * 100 / std::max(1, GET_TEAM(eT).getPower(true)) < Param("prep_ratio_pct", 100)) continue;
				++nOutweighed;
			}
			int iLoop;
			for (CvCity* c = kP.firstCity(&iLoop); c != NULL; c = kP.nextCity(&iLoop))
			{
				if (!hasCityInArea(kMe, c->getArea())) continue;
				const int d = distToCities(kMe, c->getX_INLINE(), c->getY_INLINE());
				if (d > Param(iOnlyTeam < 0 ? "target_max_distance" : "next_target_max_distance", 6)) continue;
				++nInReach;
				if (d > iBestD) continue;   // the nearest wins: a farther city needs no odds test
				bool bWin = false; int iUnit;
				for (CvUnit* u = kMe.firstUnit(&iUnit); u != NULL && !bWin; u = kMe.nextUnit(&iUnit))
					bWin = strikeCandidate(u, kMe.getID()) && oddsAgainst(u, c) >= Param("attack_min_odds", 710);
				if (!bWin) continue;
				++nWinnable;
				const int nr = ownUnitsNear(kMe, c->getX_INLINE(), c->getY_INLINE(), 2);
				if (d < iBestD || (d == iBestD && nr > iBestNear)) { pBest = c; iBestD = d; iBestNear = nr; }
			}
		}
		if (pBest == NULL && iOnlyTeam < 0 && GC.getGameINLINE().getGameTurn() % 10 == 0)
			note("no objective: teams met %d, at peace and declarable %d, with open borders %d, outweighed %d; cities in reach %d, winnable %d",
				nMet, nDeclarable, nBorders, nOutweighed, nInReach, nWinnable);
		return pBest;
	}

	// Strike group for the objective: its defenders plus strike_margin, among the candidates within
	// stage_max_turns of the staging plot: first those that would attack the city at attack_min_odds (the
	// human raided with its best attackers), nearest first, then the nearest others; existing members stay.
	void formStrike(CvPlayerAI& kMe, CvCity* c, CvPlot* pStage)
	{
		const int iNeed = c->plot()->getNumDefenders(c->getOwnerINLINE()) + Param("strike_margin", 2);
		std::vector<std::pair<std::pair<int, int>, int> > cand;   // ((not at the odds, path turns), unit id)
		int iLoop;
		for (CvUnit* u = kMe.firstUnit(&iLoop); u != NULL; u = kMe.nextUnit(&iLoop))
		{
			if (g.strike.count(u->getID()) || !strikeCandidate(u, kMe.getID())) continue;
			int iTurns = 0;
			if (u->plot() != pStage && !u->generatePath(pStage, 0, false, &iTurns)) continue;
			if (iTurns > Param("stage_max_turns", 15)) continue;
			const int bWeak = oddsAgainst(u, c) >= Param("attack_min_odds", 710) ? 0 : 1;
			cand.push_back(std::make_pair(std::make_pair(bWeak, iTurns), u->getID()));
		}
		std::sort(cand.begin(), cand.end());
		// units at the odds join until they alone make up the group, whatever weaker members it holds
		int iCapable = 0;
		for (std::set<int>::const_iterator it = g.strike.begin(); it != g.strike.end(); ++it)
		{
			CvUnit* u = kMe.getUnit(*it);
			if (u != NULL && oddsAgainst(u, c) >= Param("attack_min_odds", 710)) ++iCapable;
		}
		for (size_t i = 0; i < cand.size(); ++i)
		{
			const bool bCapable = cand[i].first.first == 0;
			if ((bCapable && iCapable < iNeed) || (!bCapable && (int)g.strike.size() < iNeed))
			{
				g.strike.insert(cand[i].second);
				if (bCapable) ++iCapable;
			}
		}
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
// choice in every ai_every, which is where the AI builds its units; during a preparation or war one in
// every ai_every_war is a fighting unit, the AI's best for the attack. Every other choice: a settler when the seat has a site and no settler, else the
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
	if (iEvery > 0 && iPicks >= iEvery - 1)
	{
		iPicks = 0;
		if (!inWarMode()) return false;
		// a preparation or war: the AI's pick is a fighting unit (the AI's best for the role), as the human
		// built more of them before its wars (study/war.md, section 3); the AI knows of no war plan here
		const UnitAITypes aeRole[] = { UNITAI_ATTACK, UNITAI_ATTACK_CITY, UNITAI_COUNTER };
		for (int r = 0; r < 3; ++r)
		{
			const UnitTypes eUnit = c->AI_bestUnitAI(aeRole[r]);
			if (eUnit == NO_UNIT || !c->canTrain(eUnit)) continue;
			c->pushOrder(ORDER_TRAIN, eUnit, aeRole[r], false, false, false);
			note("city %d,%d train %s for the war", c->getX_INLINE(), c->getY_INLINE(), GC.getUnitInfo(eUnit).getType());
			return true;
		}
		return false;
	}
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

// War (study/war.md, section 10), before the AI's own war planning (which still keeps the plans and answers
// wars on the seat, whether or not one of the seat's own is under way). One war of its own at a time, from
// war_min_turn:
//   objective   chooseObjective(): the nearest city the seat can reach and win, of a team it matches by
//               prep_ratio_pct, then the one with most of its units near
//   staging     a strike group (the city's defenders plus strike_margin) marches to the plot next to the city
//               and holds there (HH_hmTactics); upgrades and promotions run meanwhile
//   declaration once the whole group stands within two plots of the city, as many of them as the city has
//               defenders (at least one) at attack_min_odds, and the seat outweighs the team by decl_ratio_pct;
//               given up after prep_max_turns
//   war         the attack rule; after a capture the next objective is the nearest city of the same target
//               within next_target_max_distance of the seat's cities; peace once no city has fallen for
//               war_stall_turns after the first capture, or after war_max_turns, asking the loser for its gold
bool HH_hmDoWar(CvTeamAI* t)
{
	if (!on(t->getLeaderID(), "war")) return false;
	CvGame& kGame = GC.getGameINLINE();
	const int iTurn = kGame.getGameTurn();
	CvPlayerAI& kMe = GET_PLAYER(t->getLeaderID());
	// prune the strike group of units that died or were taken
	for (std::set<int>::iterator it = g.strike.begin(); it != g.strike.end();)
		if (kMe.getUnit(*it) == NULL) g.strike.erase(it++); else ++it;
	if (g.iState != 0)
	{
		CvTeamAI& kT = GET_TEAM((TeamTypes)g.iTarget);
		if (!kT.isAlive()) { endWar(*t, "target eliminated"); return false; }
		upgradeAll(kMe);
		CvPlot* pObj = GC.getMapINLINE().plot(g.iObjX, g.iObjY);
		const bool bObjHeld = pObj == NULL || !pObj->isCity() || pObj->getTeam() != g.iTarget;
		if (g.iState == 3)
		{
			if (!t->isAtWar((TeamTypes)g.iTarget)) { endWar(*t, "peace"); return false; }
			if (kT.getNumCities() < g.iTargetCities) { g.iCaptures += g.iTargetCities - kT.getNumCities(); g.iLastCaptureTurn = iTurn; }
			g.iTargetCities = kT.getNumCities();
			if (bObjHeld)
			{
				CvCity* pNext = chooseObjective(*t, kMe, g.iTarget);
				CvPlot* pSt = pNext != NULL ? stagingPlot(kMe, pNext) : NULL;
				if (pNext != NULL && pSt != NULL)
				{
					g.iObjX = pNext->getX_INLINE(); g.iObjY = pNext->getY_INLINE(); g.iStageX = pSt->getX_INLINE(); g.iStageY = pSt->getY_INLINE();
					formStrike(kMe, pNext, pSt);
					note("next objective %d,%d defenders %d strike %d", g.iObjX, g.iObjY, pNext->plot()->getNumDefenders(pNext->getOwnerINLINE()), (int)g.strike.size());
				}
				else g.iObjX = g.iObjY = -1;
			}
			const bool bStall = g.iCaptures > 0 && iTurn - g.iLastCaptureTurn >= Param("war_stall_turns", 2);
			const bool bLong = iTurn - g.iSince >= Param("war_max_turns", 6);
			if ((bStall || bLong) && iTurn > g.iLastPeaceTry)
			{
				g.iLastPeaceTry = iTurn;
				if (tryPeace(*t, (TeamTypes)g.iTarget)) endWar(*t, "peace made");
			}
			return false;
		}
		// staging
		if (t->isAtWar((TeamTypes)g.iTarget))
		{
			note("at war with %d before the declaration (declared on the seat)", g.iTarget);
			g.iState = 3; g.iSince = iTurn; g.iCaptures = 0; g.iLastCaptureTurn = iTurn; g.iTargetCities = kT.getNumCities();
			return false;
		}
		if (bObjHeld || !t->canDeclareWar((TeamTypes)g.iTarget)) { endWar(*t, "objective lost or war barred"); return false; }
		if (iTurn - g.iSince > Param("prep_max_turns", 30)) { endWar(*t, "no declaration in time"); return false; }
		CvCity* pCity = pObj->getPlotCity();
		CvPlot* pStage = GC.getMapINLINE().plot(g.iStageX, g.iStageY);
		formStrike(kMe, pCity, pStage);
		const int iDef = pObj->getNumDefenders(pCity->getOwnerINLINE());
		const int iNeed = iDef + Param("strike_margin", 2);
		const int iThere = strikeNear(g.iObjX, g.iObjY, 2);
		const int iCapable = strikeCapable(pCity);
		const int iRatio = std::max(1, t->getPower(true)) * 100 / std::max(1, kT.getPower(true));
		if ((iTurn - g.iSince) % 5 == 0)
			note("staging on %d at %d,%d: strike group %d of %d, near %d, at the odds %d of %d, power ratio %d of %d", g.iTarget, g.iObjX, g.iObjY,
				(int)g.strike.size(), iNeed, iThere, iCapable, std::max(1, iDef), iRatio, Param("decl_ratio_pct", 200));
		if ((int)g.strike.size() >= iNeed && iThere >= iNeed && iCapable >= std::max(1, iDef) && iRatio >= Param("decl_ratio_pct", 200))
		{
			note("declare on %d at %d,%d: %d of the strike group near, %d of them at the odds, %d defenders, power ratio %d", g.iTarget, g.iObjX, g.iObjY, iThere, iCapable, iDef, iRatio);
			t->declareWar((TeamTypes)g.iTarget, true, WARPLAN_TOTAL);
			g.iState = 3; g.iSince = iTurn; g.iCaptures = 0; g.iLastCaptureTurn = iTurn; g.iTargetCities = kT.getNumCities();
		}
		return false;
	}
	if (iTurn < Param("war_min_turn", 193) || iTurn - g.iIdleSince < Param("war_gap_turns", 3)) return false;
	CvCity* pCity = chooseObjective(*t, kMe, -1);   // one war of its own at a time: the state machine; wars on the seat stay with the AI
	if (pCity == NULL) return false;
	CvPlot* pStage = stagingPlot(kMe, pCity);
	if (pStage == NULL) return false;
	g.iState = 1; g.iTarget = pCity->getTeam(); g.iSince = iTurn;
	g.iObjX = pCity->getX_INLINE(); g.iObjY = pCity->getY_INLINE(); g.iStageX = pStage->getX_INLINE(); g.iStageY = pStage->getY_INLINE();
	formStrike(kMe, pCity, pStage);
	note("objective %d,%d of team %d: distance %d, defenders %d, strike group %d, staging %d,%d", g.iObjX, g.iObjY, g.iTarget,
		distToCities(kMe, g.iObjX, g.iObjY), pCity->plot()->getNumDefenders(pCity->getOwnerINLINE()), (int)g.strike.size(), g.iStageX, g.iStageY);
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
	const int iTurn = GC.getGameINLINE().getGameTurn();
	// Open borders with every AI met and not at war, from ob_min_turn, offered again every ob_every turns
	// (study/war.md, section 4: the human had them with nearly every AI before its wars).
	if (on(p->getID(), "borders") && iTurn >= Param("ob_min_turn", 126) && iTurn - g.iLastOpenBorders >= Param("ob_every", 10))
	{
		g.iLastOpenBorders = iTurn;
		for (int j = 0; j < MAX_CIV_PLAYERS; ++j)
		{
			CvPlayerAI& kJ = GET_PLAYER((PlayerTypes)j);
			if (j == p->getID() || !kJ.isAlive() || kJ.isBarbarian() || kJ.isMinorCiv() || kJ.getTeam() == p->getTeam()) continue;
			CvTeamAI& kT = GET_TEAM(p->getTeam());
			if (!kT.isHasMet(kJ.getTeam()) || kT.isAtWar(kJ.getTeam()) || kT.isOpenBorders(kJ.getTeam())) continue;
			CLinkList<TradeData> ours, theirs;
			TradeData a; setTradeItem(&a, TRADE_OPEN_BORDERS);
			if (!p->canTradeItem((PlayerTypes)j, a, true) || !kJ.canTradeItem(p->getID(), a, true)) continue;
			ours.insertAtEnd(a); theirs.insertAtEnd(a);
			if (kJ.AI_considerOffer(p->getID(), &ours, &theirs))
			{
				GC.getGameINLINE().implementDeal(p->getID(), (PlayerTypes)j, &ours, &theirs, true);
				note("open borders with %d", j);
			}
		}
	}
	if (!on(p->getID(), "trade")) return;
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

// Tactics, at the top of each unit update, before the AI moves anything (one action per update; the AI's own
// moves follow once none is left, and they may still attack at lower odds):
//   - at war: a land unit attacks an adjacent enemy plot when its odds (getCombatOdds, per mille) reach
//     attack_min_odds, or walks into an adjacent enemy city without defenders; a member of the strike group
//     next to the objective may attack it at siege_min_odds when the city holds at least siege_defenders
//   - the strike group marches to the staging plot (one multi-turn order, which the AI leaves alone), and
//     its members within two plots of the objective hold there (MISSION_SKIP) until they attack
bool HH_hmTactics(CvPlayerAI* p)
{
	if (!on(p->getID(), "tactics")) return false;
	CvTeamAI& t = GET_TEAM(p->getTeam());
	if (p->hasBusyUnit()) return false;
	static int iTurn = -1;
	static std::set<int> tried;
	if (GC.getGameINLINE().getGameTurn() != iTurn) { iTurn = GC.getGameINLINE().getGameTurn(); tried.clear(); }
	CvPlot* pObj = GC.getMapINLINE().plot(g.iObjX, g.iObjY);
	const bool bSiege = pObj != NULL && pObj->isCity() && g.iTarget >= 0 && pObj->getTeam() == g.iTarget &&
		pObj->getNumDefenders(pObj->getOwnerINLINE()) >= Param("siege_defenders", 11);
	int iLoop;
	if (warsWith(t) > 0)
	{
		const int iMin = Param("attack_min_odds", 710);
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
					const bool bSiegeHere = bSiege && q == pObj && g.strike.count(u->getID());
					if (iOdds < (bSiegeHere ? Param("siege_min_odds", 350) : iMin)) continue;
				}
				tried.insert(u->getID());
				if (u->getGroup()->getNumUnits() > 1) u->joinGroup(NULL);
				u->getGroup()->clearMissionQueue();
				note("attack %s %d,%d -> %d,%d odds %d %s", GC.getUnitInfo(u->getUnitType()).getType(), u->getX_INLINE(), u->getY_INLINE(),
					q->getX_INLINE(), q->getY_INLINE(), iOdds, pDef == NULL ? "empty city" : (bEnemyCity ? "city" : "field"));
				u->getGroup()->pushMission(MISSION_MOVE_TO, q->getX_INLINE(), q->getY_INLINE(), MOVE_DIRECT_ATTACK);
				return true;
			}
		}
	}
	// the strike group: march, then hold next to the objective
	CvPlot* pStage = GC.getMapINLINE().plot(g.iStageX, g.iStageY);
	if (g.iState == 0 || pObj == NULL || pStage == NULL) return false;
	for (std::set<int>::const_iterator it = g.strike.begin(); it != g.strike.end(); ++it)
	{
		CvUnit* u = p->getUnit(*it);
		if (u == NULL || tried.count(u->getID()) || !u->canMove() || u->isCargo()) continue;
		tried.insert(u->getID());
		if (u->getGroup()->getNumUnits() > 1) u->joinGroup(NULL);
		if (plotDistance(u->getX_INLINE(), u->getY_INLINE(), g.iObjX, g.iObjY) <= 2 && (u->plot() == pStage || g.iState == 3 ||
			plotDistance(u->getX_INLINE(), u->getY_INLINE(), g.iObjX, g.iObjY) <= 1))
		{
			u->getGroup()->clearMissionQueue();
			u->getGroup()->pushMission(MISSION_SKIP);
			return true;
		}
		if (u->getGroup()->headMissionQueueNode() != NULL) continue;   // already marching
		u->getGroup()->pushMission(MISSION_MOVE_TO, g.iStageX, g.iStageY);
		note("strike %s %d,%d -> %d,%d", GC.getUnitInfo(u->getUnitType()).getType(), u->getX_INLINE(), u->getY_INLINE(), g.iStageX, g.iStageY);
		return true;
	}
	return false;
}
