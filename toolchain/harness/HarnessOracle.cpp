// Expert oracle for the war AI: scores military decisions against what an expert
// would do, with the DLL's own combat rules. Enabled by HARNESS_ORACLE=<file>; one
// JSON line per record (README: "Expert oracle").
//
// - After a player's moves ("after"): for each plot holding its land units, what an
//   expert enemy could destroy there next turn with the enemy units that can reach
//   it, and at what cost; for each enemy city its stacks stand next to, the chance
//   of taking it next turn as the defences stand and with them bombarded to zero.
// - Before a player's moves ("before"): what an expert could destroy with this
//   player's own units this turn; "after" adds what the player actually destroyed.
// - At each attack ("atk"): the odds of the unit that attacked, the best odds any
//   other unit on its plot had against the same target, and whether a collateral
//   unit or a bombard was available but unused.
//
// Reads only. Battles are simulated here: hit points live in local arrays, random
// numbers come from a local generator, and neither the game's random numbers nor any
// AI or pathfinding cache is touched. Strengths come from CvUnit::maxCombatStr, so
// every modifier the game applies (terrain, fortification, city defence, unit class,
// promotions) is included. Simplifications: the attacker's river and amphibious
// penalties are those of its current plot; the defender chosen is the strongest
// against the attacker (the game's Lead From Behind choice may keep a valuable unit
// back); flanking strikes are not simulated; a ranged strike reaches only plots next
// to where the striker can stand.
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
#include "CvGameCoreUtils.h"
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <sstream>

namespace
{
	FILE* g_pOut = NULL;
	bool g_bOpened = false;
	unsigned int g_uiRng = 2463534242u;
	const int RUNS = 16;
	const int MAX_REACH = 12;   // plots; bounds the search on railroads

	PlayerTypes g_eMover = NO_PLAYER;  // player whose units are moving
	int g_iKillValue = 0;              // value of enemy units it destroyed this turn
	int g_iLossValue = 0;              // value of its own units lost while attacking
	int g_iKills = 0;

	FILE* out()
	{
		if (!g_bOpened)
		{
			g_bOpened = true;
			const char* sz = getenv("HARNESS_ORACLE");
			if (sz != NULL && *sz != '\0') g_pOut = fopen(sz, "a");
		}
		return g_pOut;
	}

	int rnd(int n)
	{
		g_uiRng ^= g_uiRng << 13; g_uiRng ^= g_uiRng >> 17; g_uiRng ^= g_uiRng << 5;
		return n <= 1 ? 0 : (int)(g_uiRng % (unsigned int)n);
	}

	int unitValue(const CvUnit* p)
	{
		return std::max(10, GC.getUnitInfo(p->getUnitType()).getProductionCost());
	}

	// Whether a unit's attacks do collateral damage. CvUnit::collateralCombat works on
	// integers: base strength 3 at 25 % (an archer) gives strength 0 and no damage.
	bool hasCollateral(const CvUnit* p)
	{
		return p->baseCombatStr() * p->collateralDamage() / 100 > 0 || p->getExtraCollateralDamage() > 0;
	}

	bool isCivEnemy(TeamTypes eTeam, TeamTypes eOther)
	{
		return eOther != NO_TEAM && eOther != eTeam && !GET_TEAM(eOther).isBarbarian() && !GET_TEAM(eOther).isMinorCiv() &&
			GET_TEAM(eTeam).isAtWar(eOther);
	}

	// Defender strength against pAttacker, optionally without the city's defence
	// (as after bombarding it to zero).
	int defenderMaxStr(const CvUnit* pD, const CvPlot* pPlot, const CvUnit* pA, bool bNoCityDefence)
	{
		if (!bNoCityDefence || pPlot->getPlotCity() == NULL)
		{
			return pD->maxCombatStr(pPlot, pA);
		}
		CombatDetails kDetails;
		pD->maxCombatStr(pPlot, pA, &kDetails);
		const int iModifier = kDetails.iModifierTotal - pPlot->getPlotCity()->getDefenseModifier(pA->ignoreBuildingDefense());
		const int iBase = pD->baseCombatStr();
		return std::max(1, iModifier > 0 ? iBase * (iModifier + 100) : (iBase * 10000) / (100 - iModifier));
	}

	// One battle's parameters, as CvUnit::resolveCombat computes them.
	struct Battle
	{
		int iDefOdds;      // defender's chance per round, out of COMBAT_DIE_SIDES
		int iDmgToA, iDmgToD;
		int iDefDamageCap; // the attack stops once the defender's damage would pass this
		bool bCanKill;
		int iWithdraw;     // attacker's withdrawal chance, %
		int iFsA, iFsAChance, iFsD, iFsDChance;
	};

	Battle battle(const CvUnit* pA, int iHPA, const CvUnit* pD, int iHPD, const CvPlot* pPlot, bool bNoCityDefence)
	{
		Battle b;
		const int iMaxA = pA->maxCombatStr(NULL, NULL);
		const int iMaxD = defenderMaxStr(pD, pPlot, pA, bNoCityDefence);
		const int iStrA = std::max(1, iMaxA * iHPA / pA->maxHitPoints());
		const int iStrD = std::max(1, iMaxD * iHPD / pD->maxHitPoints());
		const int iFireA = (iMaxA + iStrA + 1) / 2;
		const int iFireD = (iMaxD + iStrD + 1) / 2;
		const int iFactor = (iFireA + iFireD + 1) / 2;
		b.iDefOdds = (GC.getCOMBAT_DIE_SIDES() * iStrD) / (iStrA + iStrD);
		b.iDmgToA = std::max(1, (GC.getCOMBAT_DAMAGE() * (iFireD + iFactor)) / (iFireA + iFactor));
		b.iDmgToD = std::max(1, (GC.getCOMBAT_DAMAGE() * (iFireA + iFactor)) / (iFireD + iFactor));
		b.iDefDamageCap = pA->combatLimit();
		b.bCanKill = pA->combatLimit() >= pD->maxHitPoints();
		b.iWithdraw = pA->withdrawalProbability();
		b.iFsA = pD->immuneToFirstStrikes() ? 0 : pA->firstStrikes();
		b.iFsAChance = pD->immuneToFirstStrikes() ? 0 : pA->chanceFirstStrikes();
		b.iFsD = pA->immuneToFirstStrikes() ? 0 : pD->firstStrikes();
		b.iFsDChance = pA->immuneToFirstStrikes() ? 0 : pD->chanceFirstStrikes();
		return b;
	}

	// Exact chances that the defender dies and that the attacker dies.
	struct Odds { double kill; double die; double win; };

	struct OddsDP
	{
		double p;            // attacker wins a round
		double w;            // withdrawal chance
		bool bCanKill;
		int iNA, iND, iFA, iFD;
		std::vector<double> kill, die;
		std::vector<char> done;
		int idx(int a, int d, int fa, int fd) const { return ((a * (iND + 1) + d) * (iFA + 1) + fa) * (iFD + 1) + fd; }
		void solve(int a, int d, int fa, int fd, double& rk, double& rd)
		{
			if (a == 0) { rk = 1.0; rd = 0.0; return; }
			if (d == 0) { rk = 0.0; rd = 1.0 - w; return; }
			const int i = idx(a, d, fa, fd);
			if (done[i]) { rk = kill[i]; rd = die[i]; return; }
			const int fa2 = std::max(0, fa - 1), fd2 = std::max(0, fd - 1);
			double k1, d1, k2, d2;
			// the attacker wins the round: it hurts the defender unless the defender is still first-striking
			solve(fd > 0 ? a : a - 1, d, fa2, fd2, k1, d1);
			// the defender wins it: likewise
			solve(a, fa > 0 ? d : d - 1, fa2, fd2, k2, d2);
			rk = p * k1 + (1.0 - p) * k2;
			rd = p * d1 + (1.0 - p) * d2;
			kill[i] = rk; die[i] = rd; done[i] = 1;
		}
	};

	Odds odds(const Battle& b, int iHPA, int iHPD, int iMaxHPD)
	{
		Odds o = { 0.0, 0.0, 0.0 };
		OddsDP dp;
		dp.p = (double)(GC.getCOMBAT_DIE_SIDES() - b.iDefOdds) / GC.getCOMBAT_DIE_SIDES();
		dp.w = b.iWithdraw / 100.0;
		dp.bCanKill = b.bCanKill;
		const int iDamageD = iMaxHPD - iHPD;
		dp.iNA = b.bCanKill ? (iHPD + b.iDmgToD - 1) / b.iDmgToD
			: (iDamageD > b.iDefDamageCap ? 1 : (b.iDefDamageCap - iDamageD) / b.iDmgToD + 1);
		dp.iND = (iHPA + b.iDmgToA - 1) / b.iDmgToA;
		dp.iFA = b.iFsA + b.iFsAChance;
		dp.iFD = b.iFsD + b.iFsDChance;
		const int n = (dp.iNA + 1) * (dp.iND + 1) * (dp.iFA + 1) * (dp.iFD + 1);
		dp.kill.assign(n, 0.0); dp.die.assign(n, 0.0); dp.done.assign(n, 0);
		int iCases = 0;
		for (int fa = b.iFsA; fa <= b.iFsA + b.iFsAChance; ++fa)
		{
			for (int fd = b.iFsD; fd <= b.iFsD + b.iFsDChance; ++fd)
			{
				double k, d;
				dp.solve(dp.iNA, dp.iND, fa, fd, k, d);
				o.kill += k; o.die += d; ++iCases;
			}
		}
		o.win = o.kill / iCases; o.die /= iCases;
		o.kill = b.bCanKill ? o.win : 0.0;
		return o;
	}

	// A unit in a simulated fight.
	struct Fighter
	{
		const CvUnit* p;
		int iHP;
		bool bOut;   // dead (defenders) or has attacked (attackers)
		bool bDead;
	};

	// Plays one battle with local hit points. Returns true if the defender died.
	bool fight(Fighter& a, Fighter& d, const CvPlot* pPlot, bool bNoCityDefence)
	{
		const Battle b = battle(a.p, a.iHP, d.p, d.iHP, pPlot, bNoCityDefence);
		int iFsA = b.iFsA + rnd(b.iFsAChance + 1);
		int iFsD = b.iFsD + rnd(b.iFsDChance + 1);
		const int iMaxHPD = d.p->maxHitPoints();
		while (true)
		{
			if (rnd(GC.getCOMBAT_DIE_SIDES()) < b.iDefOdds)
			{
				if (iFsA == 0)
				{
					if (a.iHP - b.iDmgToA <= 0 && rnd(100) < b.iWithdraw) return false;   // withdraws
					a.iHP -= b.iDmgToA;
				}
			}
			else if (iFsD == 0)
			{
				const int iDamage = iMaxHPD - d.iHP;
				if (std::min(iMaxHPD, iDamage + b.iDmgToD) > b.iDefDamageCap)
				{
					d.iHP = iMaxHPD - b.iDefDamageCap;   // the combat limit stops the attack
					return false;
				}
				d.iHP -= b.iDmgToD;
			}
			if (iFsA > 0) --iFsA;
			if (iFsD > 0) --iFsD;
			if (a.iHP <= 0) { a.bDead = true; return false; }
			if (d.iHP <= 0) { d.bDead = true; d.bOut = true; return true; }
		}
	}

	// CvUnit::collateralCombat on local hit points.
	void collateral(const Fighter& a, std::vector<Fighter>& defenders, int iSkip)
	{
		static const int iBaseDamage = GC.getDefineINT("COLLATERAL_COMBAT_DAMAGE");
		const CvUnit* pA = a.p;
		const int iStrength = pA->baseCombatStr() * pA->collateralDamage() / 100;
		if (iStrength == 0 && pA->getExtraCollateralDamage() == 0) return;
		int iAlive = 0;
		for (size_t i = 0; i < defenders.size(); ++i) if (!defenders[i].bOut) ++iAlive;
		const int iTargets = std::min(iAlive - 1, pA->collateralDamageMaxUnits());
		std::vector<std::pair<int, int> > order;
		for (size_t i = 0; i < defenders.size(); ++i)
		{
			if (!defenders[i].bOut && (int)i != iSkip) order.push_back(std::make_pair((1 + rnd(10000)) * defenders[i].iHP, (int)i));
		}
		std::sort(order.rbegin(), order.rend());
		for (int k = 0; k < iTargets && k < (int)order.size(); ++k)
		{
			Fighter& d = defenders[order[k].second];
			if (pA->getUnitCombatType() != NO_UNITCOMBAT && d.p->getUnitInfo().getUnitCombatCollateralImmune(pA->getUnitCombatType())) continue;
			const int iTheirs = d.p->baseCombatStr();
			const int iFactor = (iStrength + iTheirs + 1) / 2;
			int iDamage = (iBaseDamage * (iStrength + iFactor)) / std::max(1, iTheirs + iFactor);
			iDamage *= 100 + pA->getExtraCollateralDamage();
			iDamage *= std::max(0, 100 - d.p->getCollateralDamageProtection());
			iDamage /= 100;
			iDamage /= 100;
			const int iMax = std::min(pA->collateralDamageLimit(), (pA->collateralDamageLimit() * (iStrength + iFactor)) / std::max(1, iTheirs + iFactor));
			const int iOld = d.p->maxHitPoints() - d.iHP;
			const int iNew = std::max(iOld, std::min(iOld + std::max(0, iDamage), iMax));
			d.iHP = d.p->maxHitPoints() - iNew;
			// A collateral limit of 100 % (RoM's mounted units) can kill: CvUnit::setDamage
			// kills at full damage when the attacker's collateral strength reaches the target's.
			if (d.iHP <= 0) { d.iHP = 0; d.bDead = true; d.bOut = true; }
		}
	}

	// Defender the game would put up against a: the strongest against it.
	int bestDefender(const Fighter& a, const std::vector<Fighter>& defenders, const CvPlot* pPlot, bool bNoCityDefence)
	{
		int iBest = -1;
		long long llBest = -1;
		for (size_t i = 0; i < defenders.size(); ++i)
		{
			if (defenders[i].bOut) continue;
			const long long ll = (long long)defenderMaxStr(defenders[i].p, pPlot, a.p, bNoCityDefence) * defenders[i].iHP / defenders[i].p->maxHitPoints();
			if (ll > llBest) { llBest = ll; iBest = (int)i; }
		}
		return iBest;
	}

	struct Result
	{
		double dKills, dKillValue, dLosses, dLossValue, dAllDead;
		Result() : dKills(0), dKillValue(0), dLosses(0), dLossValue(0), dAllDead(0) {}
	};

	bool canStrike(const CvUnit* p)
	{
		return p->airRange() > 0 && p->airBaseCombatStr() > 0 && p->canFight();
	}

	// CvUnit::rangeStrike on local hit points: collateral on the rest of the stack,
	// then damage to the target up to the striker's air combat limit. No risk.
	void strike(const Fighter& a, std::vector<Fighter>& defenders, int j, const CvPlot* pPlot)
	{
		static const int iRangeDamage = GC.getDefineINT("RANGE_COMBAT_DAMAGE");
		Fighter& d = defenders[j];
		const int iOurs = a.p->airMaxCombatStr(d.p) * a.iHP / a.p->maxHitPoints();
		const int iTheirs = d.p->maxCombatStr(pPlot, a.p);
		const int iFactor = (iOurs + iTheirs + 1) / 2;
		const int iDamage = std::max(1, (iRangeDamage * (iOurs + iFactor)) / std::max(1, iTheirs + iFactor));
		collateral(a, defenders, j);
		const int iOld = d.p->maxHitPoints() - d.iHP;
		const int iNew = std::max(iOld, std::min(iOld + iDamage, a.p->airCombatLimit()));
		d.iHP = d.p->maxHitPoints() - iNew;
	}

	// An expert's attack on pPlot: ranged strikes first (no risk), then collateral units
	// while two or more defenders stand, then the attacker with the best odds against
	// the defender it would face, as long as it is more likely to win than not or the
	// trade is worth it. A unit that strikes cannot attack in the same turn.
	Result expertAttack(const std::vector<const CvUnit*>& attackers, const std::vector<const CvUnit*>& defenders, const CvPlot* pPlot, bool bNoCityDefence)
	{
		Result r;
		if (attackers.empty() || defenders.empty()) return r;
		for (int iRun = 0; iRun < RUNS; ++iRun)
		{
			std::vector<Fighter> A, D;
			for (size_t i = 0; i < attackers.size(); ++i) { Fighter f = { attackers[i], attackers[i]->currHitPoints(), false, false }; A.push_back(f); }
			for (size_t i = 0; i < defenders.size(); ++i) { Fighter f = { defenders[i], defenders[i]->currHitPoints(), false, false }; D.push_back(f); }
			int iAlive = (int)D.size();
			// ranged strikes
			for (size_t i = 0; i < A.size(); ++i)
			{
				if (!canStrike(A[i].p)) continue;
				const int j = bestDefender(A[i], D, pPlot, bNoCityDefence);
				if (j < 0) break;
				strike(A[i], D, j, pPlot);
				A[i].bOut = true;
				iAlive = 0;
				for (size_t k = 0; k < D.size(); ++k) if (!D[k].bOut) ++iAlive;
				if (iAlive == 0) break;
			}
			// collateral units, strongest collateral first
			std::vector<std::pair<int, int> > siege;
			for (size_t i = 0; i < A.size(); ++i)
			{
				if (!A[i].bOut && hasCollateral(A[i].p)) siege.push_back(std::make_pair(A[i].p->baseCombatStr() * A[i].p->collateralDamage(), (int)i));
			}
			std::sort(siege.rbegin(), siege.rend());
			for (size_t k = 0; k < siege.size() && iAlive >= 2; ++k)
			{
				Fighter& a = A[siege[k].second];
				const int j = bestDefender(a, D, pPlot, bNoCityDefence);
				if (j < 0) break;
				collateral(a, D, j);
				iAlive = 0;
				for (size_t k = 0; k < D.size(); ++k) if (!D[k].bOut) ++iAlive;
				if (D[j].bOut) { a.bOut = true; continue; }
				if (fight(a, D[j], pPlot, bNoCityDefence)) --iAlive;
				a.bOut = true;
			}
			// the rest, best odds first
			while (iAlive > 0)
			{
				// candidates: the three attackers with the best strength ratio
				std::vector<std::pair<double, int> > ratio;
				for (size_t i = 0; i < A.size(); ++i)
				{
					if (A[i].bOut || A[i].bDead) continue;
					const int j = bestDefender(A[i], D, pPlot, bNoCityDefence);
					const double dA = (double)A[i].p->maxCombatStr(NULL, NULL) * A[i].iHP / A[i].p->maxHitPoints();
					const double dD = (double)defenderMaxStr(D[j].p, pPlot, A[i].p, bNoCityDefence) * D[j].iHP / D[j].p->maxHitPoints();
					ratio.push_back(std::make_pair(dA / std::max(1.0, dD), (int)i));
				}
				if (ratio.empty()) break;
				std::sort(ratio.rbegin(), ratio.rend());
				int iPick = -1, jPick = -1;
				Odds best = { -1.0, 0.0, 0.0 };
				for (size_t k = 0; k < ratio.size() && k < 3; ++k)
				{
					const int i = ratio[k].second;
					const int j = bestDefender(A[i], D, pPlot, bNoCityDefence);
					const Odds o = odds(battle(A[i].p, A[i].iHP, D[j].p, D[j].iHP, pPlot, bNoCityDefence), A[i].iHP, D[j].iHP, D[j].p->maxHitPoints());
					if (o.kill > best.kill) { best = o; iPick = i; jPick = j; }
				}
				if (iPick < 0) break;
				const double dTrade = best.kill * unitValue(D[jPick].p) - best.die * unitValue(A[iPick].p);
				if (best.kill < 0.5 && !(best.kill >= 0.3 && dTrade > 0)) break;
				if (fight(A[iPick], D[jPick], pPlot, bNoCityDefence)) --iAlive;
				A[iPick].bOut = true;
			}
			for (size_t i = 0; i < D.size(); ++i) if (D[i].bDead) { r.dKills += 1; r.dKillValue += unitValue(D[i].p); }
			for (size_t i = 0; i < A.size(); ++i) if (A[i].bDead) { r.dLosses += 1; r.dLossValue += unitValue(A[i].p); }
			if (iAlive == 0) r.dAllDead += 1;
		}
		r.dKills /= RUNS; r.dKillValue /= RUNS; r.dLosses /= RUNS; r.dLossValue /= RUNS; r.dAllDead /= RUNS;
		return r;
	}

	// Whether pUnit may pass through pPlot on its way (not its target).
	bool passable(const CvUnit* pUnit, const CvPlot* pPlot)
	{
		if (pPlot->isWater() || pPlot->isImpassable()) return false;
		const TeamTypes eTeam = pUnit->getTeam();
		const TeamTypes ePlotTeam = pPlot->getTeam();
		if (ePlotTeam != NO_TEAM && ePlotTeam != eTeam && !GET_TEAM(eTeam).isAtWar(ePlotTeam) &&
			!GET_TEAM(eTeam).isOpenBorders(ePlotTeam) && !GET_TEAM(ePlotTeam).isVassal(eTeam) && !GET_TEAM(eTeam).isVassal(ePlotTeam))
		{
			return false;
		}
		for (CLLNode<IDInfo>* pNode = pPlot->headUnitNode(); pNode != NULL; pNode = pPlot->nextUnitNode(pNode))
		{
			const CvUnit* pLoop = ::getUnit(pNode->m_data);
			if (pLoop != NULL && pLoop->canDefend() && GET_TEAM(eTeam).isAtWar(pLoop->getTeam())) return false;
		}
		return true;
	}

	// Plots from which pUnit could attack with iMoves movement points (it stands on
	// them with moves left). Dijkstra on CvPlot::movementCost; the game's pathfinder
	// is not used, so its caches stay as they are.
	void attackFrom(const CvUnit* pUnit, int iMoves, std::set<int>& plots)
	{
		CvMap& kMap = GC.getMapINLINE();
		const CvPlot* pStart = pUnit->plot();
		std::map<int, int> best;
		std::priority_queue<std::pair<int, int> > open;
		const int iStart = kMap.plotNumINLINE(pStart->getX_INLINE(), pStart->getY_INLINE());
		best[iStart] = iMoves;
		open.push(std::make_pair(iMoves, iStart));
		while (!open.empty())
		{
			const int iLeft = open.top().first;
			const int iPlot = open.top().second;
			open.pop();
			if (best[iPlot] != iLeft || iLeft <= 0) continue;
			plots.insert(iPlot);
			const CvPlot* pFrom = kMap.plotByIndexINLINE(iPlot);
			for (int iDir = 0; iDir < NUM_DIRECTION_TYPES; ++iDir)
			{
				const CvPlot* pTo = plotDirection(pFrom->getX_INLINE(), pFrom->getY_INLINE(), (DirectionTypes)iDir);
				if (pTo == NULL || stepDistance(pStart->getX_INLINE(), pStart->getY_INLINE(), pTo->getX_INLINE(), pTo->getY_INLINE()) > MAX_REACH) continue;
				if (!passable(pUnit, pTo)) continue;
				const int iTo = kMap.plotNumINLINE(pTo->getX_INLINE(), pTo->getY_INLINE());
				const int iLeftTo = std::max(0, iLeft - pTo->movementCost(pUnit, pFrom));
				std::map<int, int>::iterator it = best.find(iTo);
				if (it == best.end() || it->second < iLeftTo)
				{
					best[iTo] = iLeftTo;
					open.push(std::make_pair(iLeftTo, iTo));
				}
			}
		}
	}

	bool isFighter(const CvUnit* p)
	{
		return p != NULL && p->getDomainType() == DOMAIN_LAND && p->canAttack() && !p->isCargo() && p->baseCombatStr() > 0;
	}

	// Units of eTeam on pPlot that defend it.
	void defendersOf(const CvPlot* pPlot, TeamTypes eTeam, std::vector<const CvUnit*>& v)
	{
		for (CLLNode<IDInfo>* pNode = pPlot->headUnitNode(); pNode != NULL; pNode = pPlot->nextUnitNode(pNode))
		{
			const CvUnit* pLoop = ::getUnit(pNode->m_data);
			if (pLoop != NULL && pLoop->getTeam() == eTeam && pLoop->canDefend() && pLoop->getDomainType() == DOMAIN_LAND && !pLoop->isCargo()) v.push_back(pLoop);
		}
	}

	// For each target plot (adjacent to where the attackers can be), the attackers
	// that can reach it.
	void attackersByTarget(const std::vector<const CvUnit*>& units, bool bFullMoves, const std::set<int>& targets, std::map<int, std::vector<const CvUnit*> >& byTarget)
	{
		CvMap& kMap = GC.getMapINLINE();
		for (size_t u = 0; u < units.size(); ++u)
		{
			const CvUnit* pUnit = units[u];
			bool bNear = false;
			for (std::set<int>::const_iterator it = targets.begin(); it != targets.end() && !bNear; ++it)
			{
				const CvPlot* pT = kMap.plotByIndexINLINE(*it);
				bNear = stepDistance(pUnit->getX_INLINE(), pUnit->getY_INLINE(), pT->getX_INLINE(), pT->getY_INLINE()) <= MAX_REACH;
			}
			if (!bNear) continue;
			std::set<int> from;
			attackFrom(pUnit, bFullMoves ? pUnit->maxMoves() : pUnit->movesLeft(), from);
			std::set<int> hit;
			for (std::set<int>::const_iterator it = from.begin(); it != from.end(); ++it)
			{
				const CvPlot* pFrom = kMap.plotByIndexINLINE(*it);
				for (int iDir = 0; iDir < NUM_DIRECTION_TYPES; ++iDir)
				{
					const CvPlot* pTo = plotDirection(pFrom->getX_INLINE(), pFrom->getY_INLINE(), (DirectionTypes)iDir);
					if (pTo == NULL) continue;
					const int iTo = kMap.plotNumINLINE(pTo->getX_INLINE(), pTo->getY_INLINE());
					if (targets.count(iTo) && hit.insert(iTo).second) byTarget[iTo].push_back(pUnit);
				}
			}
		}
	}

	void enemyFighters(PlayerTypes ePlayer, std::vector<const CvUnit*>& v)
	{
		const TeamTypes eTeam = GET_PLAYER(ePlayer).getTeam();
		for (int iP = 0; iP < MAX_CIV_PLAYERS; ++iP)
		{
			const CvPlayer& kP = GET_PLAYER((PlayerTypes)iP);
			if (!kP.isAlive() || !isCivEnemy(eTeam, kP.getTeam())) continue;
			int iLoop;
			for (CvUnit* p = kP.firstUnit(&iLoop); p != NULL; p = kP.nextUnit(&iLoop)) if (isFighter(p)) v.push_back(p);
		}
	}

	bool atWarWithCiv(PlayerTypes ePlayer)
	{
		const TeamTypes eTeam = GET_PLAYER(ePlayer).getTeam();
		for (int iT = 0; iT < MAX_CIV_TEAMS; ++iT) if (GET_TEAM((TeamTypes)iT).isAlive() && isCivEnemy(eTeam, (TeamTypes)iT)) return true;
		return false;
	}

	std::string fmt(double d) { char sz[32]; _snprintf(sz, sizeof(sz), "%.2f", d); return sz; }
}

// Before ePlayer's units move: what an expert could destroy with them this turn.
void HH_oracleBeforeMoves(PlayerTypes ePlayer)
{
	g_eMover = ePlayer; g_iKillValue = 0; g_iLossValue = 0; g_iKills = 0;
	if (out() == NULL || ePlayer == NO_PLAYER || GET_PLAYER(ePlayer).isBarbarian() || !atWarWithCiv(ePlayer)) return;
	const CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	const TeamTypes eTeam = kPlayer.getTeam();
	CvMap& kMap = GC.getMapINLINE();
	std::vector<const CvUnit*> own, enemy;
	int iLoop;
	for (CvUnit* p = kPlayer.firstUnit(&iLoop); p != NULL; p = kPlayer.nextUnit(&iLoop)) if (isFighter(p) && p->movesLeft() > 0) own.push_back(p);
	enemyFighters(ePlayer, enemy);
	std::set<int> targets;
	for (size_t i = 0; i < enemy.size(); ++i)
	{
		const CvPlot* p = enemy[i]->plot();
		if (p->isCity()) continue;   // cities are judged in the siege records
		targets.insert(kMap.plotNumINLINE(p->getX_INLINE(), p->getY_INLINE()));
	}
	std::map<int, std::vector<const CvUnit*> > byTarget;
	attackersByTarget(own, false, targets, byTarget);
	double dGain = 0, dKills = 0;
	int iTargets = 0;
	std::ostringstream top;
	for (std::map<int, std::vector<const CvUnit*> >::iterator it = byTarget.begin(); it != byTarget.end(); ++it)
	{
		const CvPlot* pPlot = kMap.plotByIndexINLINE(it->first);
		std::vector<const CvUnit*> defenders;
		for (CLLNode<IDInfo>* pNode = pPlot->headUnitNode(); pNode != NULL; pNode = pPlot->nextUnitNode(pNode))
		{
			const CvUnit* pLoop = ::getUnit(pNode->m_data);
			if (pLoop != NULL && pLoop->canDefend() && isCivEnemy(eTeam, pLoop->getTeam()) && pLoop->getDomainType() == DOMAIN_LAND) defenders.push_back(pLoop);
		}
		const Result r = expertAttack(it->second, defenders, pPlot, false);
		const double dNet = r.dKillValue - r.dLossValue;
		if (dNet <= 0) continue;
		++iTargets; dGain += dNet; dKills += r.dKills;
		if (iTargets <= 5)
			top << (iTargets > 1 ? "," : "") << "[" << pPlot->getX_INLINE() << "," << pPlot->getY_INLINE() << "," << defenders.size() << "," << it->second.size()
				<< "," << fmt(r.dKills) << "," << fmt(r.dKillValue) << "," << fmt(r.dLossValue) << "]";
	}
	fprintf(out(), "{\"o\":\"before\",\"t\":%d,\"p\":%d,\"units\":%d,\"targets\":%d,\"gain\":%s,\"kills\":%s,\"top\":[%s]}\n",
		GC.getGameINLINE().getGameTurn(), (int)ePlayer, (int)own.size(), iTargets, fmt(dGain).c_str(), fmt(dKills).c_str(), top.str().c_str());
}

// Battles while a player moves: what it destroyed and lost in its own attacks.
void HH_oracleCombatResult(CvUnit* pWinner, CvUnit* pLoser)
{
	if (pWinner == NULL || pLoser == NULL || g_eMover == NO_PLAYER) return;
	if (pWinner->getOwnerINLINE() == g_eMover) { g_iKillValue += unitValue(pLoser); ++g_iKills; }
	else if (pLoser->getOwnerINLINE() == g_eMover) g_iLossValue += unitValue(pLoser);
}

// After ePlayer's units moved: what an expert enemy could do to them next turn, and
// how its sieges stand.
void HH_oracleAfterMoves(PlayerTypes ePlayer)
{
	const PlayerTypes eMover = g_eMover;
	g_eMover = NO_PLAYER;
	if (out() == NULL || ePlayer == NO_PLAYER || GET_PLAYER(ePlayer).isBarbarian() || !atWarWithCiv(ePlayer)) return;
	const CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	const TeamTypes eTeam = kPlayer.getTeam();
	CvMap& kMap = GC.getMapINLINE();
	std::set<int> ours;
	int iLoop;
	for (CvUnit* p = kPlayer.firstUnit(&iLoop); p != NULL; p = kPlayer.nextUnit(&iLoop))
	{
		if (p->getDomainType() == DOMAIN_LAND && !p->isCargo()) ours.insert(kMap.plotNumINLINE(p->getX_INLINE(), p->getY_INLINE()));
	}
	std::vector<const CvUnit*> enemy;
	enemyFighters(ePlayer, enemy);
	std::map<int, std::vector<const CvUnit*> > byTarget;
	attackersByTarget(enemy, true, ours, byTarget);

	// Exposure of each plot
	double dLossValue = 0, dLosses = 0, dCost = 0, dPunish = 0, dPunishOpen = 0, dCityFall = 0;
	int iExposed = 0, iUnitsExposed = 0, iCities = 0;
	std::vector<std::pair<double, std::string> > worst;
	for (std::map<int, std::vector<const CvUnit*> >::iterator it = byTarget.begin(); it != byTarget.end(); ++it)
	{
		const CvPlot* pPlot = kMap.plotByIndexINLINE(it->first);
		std::vector<const CvUnit*> defenders;
		defendersOf(pPlot, eTeam, defenders);
		if (defenders.empty()) continue;
		const Result r = expertAttack(it->second, defenders, pPlot, false);
		const bool bOwnCity = pPlot->isCity() && pPlot->getTeam() == eTeam;
		// Units that cannot defend (workers, settlers) are captured once the defenders are gone.
		int iCapturable = 0;
		for (CLLNode<IDInfo>* pNode = pPlot->headUnitNode(); pNode != NULL; pNode = pPlot->nextUnitNode(pNode))
		{
			const CvUnit* pLoop = ::getUnit(pNode->m_data);
			if (pLoop != NULL && pLoop->getTeam() == eTeam && pLoop->getDomainType() == DOMAIN_LAND && !pLoop->isCargo() && !pLoop->canDefend())
				iCapturable += unitValue(pLoop);
		}
		if (bOwnCity) { ++iCities; dCityFall += r.dAllDead; }
		++iExposed; iUnitsExposed += (int)defenders.size();
		const double dLost = r.dKillValue + r.dAllDead * iCapturable;
		dLossValue += dLost; dLosses += r.dKills; dCost += r.dLossValue;
		const double dNet = std::max(0.0, dLost - r.dLossValue);
		dPunish += dNet;
		const int iDefence = pPlot->defenseModifier(eTeam, false);
		if (!bOwnCity && iDefence <= 0) dPunishOpen += dNet;
		std::ostringstream s;
		s << "[" << pPlot->getX_INLINE() << "," << pPlot->getY_INLINE() << "," << (bOwnCity ? 1 : 0) << "," << defenders.size() << "," << iDefence << ","
			<< it->second.size() << "," << fmt(r.dKills) << "," << fmt(dLost) << "," << fmt(r.dLossValue) << "," << fmt(r.dAllDead) << "]";
		worst.push_back(std::make_pair(dNet, s.str()));
	}
	std::sort(worst.rbegin(), worst.rend());
	std::ostringstream top;
	for (size_t i = 0; i < worst.size() && i < 5; ++i) top << (i ? "," : "") << worst[i].second;

	// Sieges: enemy cities next to our land units.
	std::ostringstream siege;
	int iSieges = 0;
	std::set<int> seen;
	for (std::set<int>::const_iterator it = ours.begin(); it != ours.end(); ++it)
	{
		const CvPlot* pOurs = kMap.plotByIndexINLINE(*it);
		for (int iDir = 0; iDir < NUM_DIRECTION_TYPES; ++iDir)
		{
			const CvPlot* pCityPlot = plotDirection(pOurs->getX_INLINE(), pOurs->getY_INLINE(), (DirectionTypes)iDir);
			if (pCityPlot == NULL || !pCityPlot->isCity() || !isCivEnemy(eTeam, pCityPlot->getTeam())) continue;
			const int iCity = kMap.plotNumINLINE(pCityPlot->getX_INLINE(), pCityPlot->getY_INLINE());
			if (!seen.insert(iCity).second) continue;
			std::vector<const CvUnit*> attackers, defenders;
			int iSiege = 0, iBombard = 0;
			for (int iDir2 = 0; iDir2 < NUM_DIRECTION_TYPES; ++iDir2)
			{
				const CvPlot* pAdj = plotDirection(pCityPlot->getX_INLINE(), pCityPlot->getY_INLINE(), (DirectionTypes)iDir2);
				if (pAdj == NULL) continue;
				for (CLLNode<IDInfo>* pNode = pAdj->headUnitNode(); pNode != NULL; pNode = pAdj->nextUnitNode(pNode))
				{
					const CvUnit* pLoop = ::getUnit(pNode->m_data);
					if (pLoop == NULL || pLoop->getOwnerINLINE() != ePlayer || !isFighter(pLoop)) continue;
					attackers.push_back(pLoop);
					if (hasCollateral(pLoop)) ++iSiege;
					iBombard += pLoop->bombardRate();
				}
			}
			defendersOf(pCityPlot, pCityPlot->getTeam(), defenders);
			if (attackers.size() < 2) continue;
			const CvCity* pCity = pCityPlot->getPlotCity();
			const Result rNow = expertAttack(attackers, defenders, pCityPlot, false);
			const Result rZero = expertAttack(attackers, defenders, pCityPlot, true);
			siege << (iSieges++ ? "," : "") << "[" << pCityPlot->getX_INLINE() << "," << pCityPlot->getY_INLINE() << "," << (int)pCityPlot->getOwnerINLINE() << ","
				<< pCity->getDefenseModifier(false) << "," << pCity->getTotalDefense(false) << "," << defenders.size() << "," << attackers.size() << ","
				<< iSiege << "," << iBombard << "," << fmt(rNow.dAllDead) << "," << fmt(rNow.dLossValue) << "," << fmt(rZero.dAllDead) << "," << fmt(rZero.dLossValue) << "]";
		}
	}

	fprintf(out(), "{\"o\":\"after\",\"t\":%d,\"p\":%d,\"exposed\":%d,\"units\":%d,\"lossU\":%s,\"lossV\":%s,\"costV\":%s,\"punish\":%s,\"punishOpen\":%s,"
		"\"cities\":%d,\"cityFall\":%s,\"killV\":%d,\"lostV\":%d,\"kills\":%d,\"top\":[%s],\"siege\":[%s]}\n",
		GC.getGameINLINE().getGameTurn(), (int)ePlayer, iExposed, iUnitsExposed, fmt(dLosses).c_str(), fmt(dLossValue).c_str(), fmt(dCost).c_str(),
		fmt(dPunish).c_str(), fmt(dPunishOpen).c_str(), iCities, fmt(dCityFall).c_str(),
		eMover == ePlayer ? g_iKillValue : 0, eMover == ePlayer ? g_iLossValue : 0, eMover == ePlayer ? g_iKills : 0, top.str().c_str(), siege.str().c_str());
	fflush(out());
}

// At each attack: the attacker's odds, the best odds another unit on its plot had
// against the same plot, and whether a collateral unit or a bombard was left unused.
void HH_oracleAttack(CvUnit* pAttacker, CvUnit* pDefender)
{
	if (out() == NULL || pAttacker == NULL || pDefender == NULL || pAttacker->isBarbarian() || pAttacker->getDomainType() != DOMAIN_LAND) return;
	const CvPlot* pTarget = pDefender->plot();
	const CvPlot* pFrom = pAttacker->plot();
	if (pTarget == NULL || pFrom == NULL) return;
	const TeamTypes eDefTeam = pDefender->getTeam();
	const int iOdds = getCombatOdds(pAttacker, pDefender);
	int iBest = -1, iAlternatives = 0, iCollateralLeft = 0, iBombardLeft = 0;
	for (CLLNode<IDInfo>* pNode = pFrom->headUnitNode(); pNode != NULL; pNode = pFrom->nextUnitNode(pNode))
	{
		CvUnit* pLoop = ::getUnit(pNode->m_data);
		if (pLoop == NULL || pLoop == pAttacker || pLoop->getOwnerINLINE() != pAttacker->getOwnerINLINE() || !isFighter(pLoop) ||
			pLoop->isMadeAttack() || pLoop->movesLeft() <= 0) continue;
		++iAlternatives;
		if (hasCollateral(pLoop)) ++iCollateralLeft;
		if (pTarget->isCity() && pLoop->bombardRate() > 0 && pLoop->canBombard(pFrom)) ++iBombardLeft;
		// the defender pLoop would meet: the strongest against it
		int iWorst = 1000;
		for (CLLNode<IDInfo>* pD = pTarget->headUnitNode(); pD != NULL; pD = pTarget->nextUnitNode(pD))
		{
			CvUnit* pDef = ::getUnit(pD->m_data);
			if (pDef != NULL && pDef->getTeam() == eDefTeam && pDef->canDefend()) iWorst = std::min(iWorst, getCombatOdds(pLoop, pDef));
		}
		iBest = std::max(iBest, iWorst);
	}
	int iDefenders = 0;
	for (CLLNode<IDInfo>* pD = pTarget->headUnitNode(); pD != NULL; pD = pTarget->nextUnitNode(pD))
	{
		const CvUnit* pDef = ::getUnit(pD->m_data);
		if (pDef != NULL && pDef->getTeam() == eDefTeam && pDef->canDefend()) ++iDefenders;
	}
	const CvCity* pCity = pTarget->getPlotCity();
	// The oracle's own odds for this battle, to check its model against getCombatOdds.
	const Odds kMine = odds(battle(pAttacker, pAttacker->currHitPoints(), pDefender, pDefender->currHitPoints(), pTarget, false),
		pAttacker->currHitPoints(), pDefender->currHitPoints(), pDefender->maxHitPoints());
	fprintf(out(), "{\"o\":\"atk\",\"my\":%d,", (int)(1000.0 * kMine.win + 0.5));
	fprintf(out(), "\"t\":%d,\"p\":%d,\"ai\":%d,\"u\":\"%s\",\"city\":%d,\"def\":%d,\"nd\":%d,\"hpd\":%d,\"odds\":%d,\"best\":%d,\"alt\":%d,"
		"\"col\":%d,\"colLeft\":%d,\"bombLeft\":%d,\"group\":%d}\n",
		GC.getGameINLINE().getGameTurn(), (int)pAttacker->getOwnerINLINE(), (int)pAttacker->AI_getUnitAIType(), GC.getUnitInfo(pAttacker->getUnitType()).getType(),
		pCity != NULL ? 1 : 0, pCity != NULL ? pCity->getDefenseModifier(false) : 0, iDefenders, pDefender->currHitPoints(), iOdds, iBest, iAlternatives,
		hasCollateral(pAttacker) ? 1 : 0, iCollateralLeft, iBombardLeft,
		pAttacker->getGroup() != NULL ? pAttacker->getGroup()->getNumUnits() : 1);
}
