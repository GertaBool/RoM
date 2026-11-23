#include <cassert>
#include <cstdio>
#include <climits>

#include "AIBuildingLinePolicy.h"
#include "AIStrategicDefensePolicy.h"
#include "AIDiplomacyPolicy.h"

static void testNetUpgradeValue()
{
	// Normal upgrade: gross 300 replaces 200 -> net 100
	assert(AIBuildingLinePolicy::netUpgradeValue(300, 200) == 100);
	// No downgrade / lateral waste: gross <= replaced -> 0
	assert(AIBuildingLinePolicy::netUpgradeValue(150, 200) == 0);
	assert(AIBuildingLinePolicy::netUpgradeValue(200, 200) == 0);
	// No predecessor built: full gross value
	assert(AIBuildingLinePolicy::netUpgradeValue(250, 0) == 250);
	assert(AIBuildingLinePolicy::netUpgradeValue(250, -10) == 250);
	// Non-positive gross: 0
	assert(AIBuildingLinePolicy::netUpgradeValue(0, 100) == 0);
	assert(AIBuildingLinePolicy::netUpgradeValue(-50, 100) == 0);
}

static void testPrereqChainCredit()
{
	// Cheap bottleneck (10H Settlement Essentials gating 70H Town Essentials of value 400)
	// gets strong pull when downstream tech is known
	const int knownCheap = AIBuildingLinePolicy::prereqChainCredit(400, 10, 70, true);
	const int unknownCheap = AIBuildingLinePolicy::prereqChainCredit(400, 10, 70, false);
	const int knownExpensive = AIBuildingLinePolicy::prereqChainCredit(400, 100, 70, true);
	assert(knownCheap > unknownCheap);
	assert(knownCheap > knownExpensive);
	assert(knownCheap > 150 && knownCheap <= 600);
	assert(unknownCheap > 40);
	// Cap at 600 even for massive downstream values
	assert(AIBuildingLinePolicy::prereqChainCredit(100000, 10, 100, true) == 600);
	// Zero/negative downstream -> 0
	assert(AIBuildingLinePolicy::prereqChainCredit(0, 10, 70, true) == 0);
	assert(AIBuildingLinePolicy::prereqChainCredit(-50, 10, 70, true) == 0);
}

static void testObsolescenceFactor()
{
	assert(AIBuildingLinePolicy::obsolescenceFactorPercent(2, 2, true) == 0);
	assert(AIBuildingLinePolicy::obsolescenceFactorPercent(-1, 3, false) == 100);
	assert(AIBuildingLinePolicy::obsolescenceFactorPercent(2, 2, false) == 45);
	assert(AIBuildingLinePolicy::obsolescenceFactorPercent(1, 3, false) == 45);
	assert(AIBuildingLinePolicy::obsolescenceFactorPercent(3, 2, false) == 75);
	assert(AIBuildingLinePolicy::obsolescenceFactorPercent(4, 2, false) == 100);
}

static void testGoldenAgeAndMilitaryWonders()
{
	// Taj Mahal / Colossus (triggers GA) vs Mausoleum (50% longer GA)
	const int gaSmall = AIBuildingLinePolicy::goldenAgeBuildingValue(true, 0, 2, 10);
	const int gaLarge = AIBuildingLinePolicy::goldenAgeBuildingValue(true, 0, 12, 120);
	assert(gaSmall > 0 && gaLarge > gaSmall);
	assert(AIBuildingLinePolicy::goldenAgeBuildingValue(false, 50, 10, 80) > 0);
	assert(AIBuildingLinePolicy::goldenAgeBuildingValue(false, 0, 10, 80) == 0);

	// Art of War (-50% upgrade cost, +50% GG rate)
	const int aowPeace = AIBuildingLinePolicy::militaryWonderBonusValue(-50, 50, 30, 100, false);
	const int aowWar = AIBuildingLinePolicy::militaryWonderBonusValue(-50, 50, 30, 120, true);
	assert(aowPeace > 100);
	assert(aowWar > aowPeace);
	assert(AIBuildingLinePolicy::militaryWonderBonusValue(0, 0, 30, 100, true) == 0);
}

static void testPythonWonders()
{
	// World Bank scales with treasury & GPT
	const int wbPoor = AIBuildingLinePolicy::worldBankValue(100, 10, 5);
	const int wbRich = AIBuildingLinePolicy::worldBankValue(10000, 200, 15);
	assert(wbPoor >= 80 && wbRich > wbPoor && wbRich <= 900);

	// Crusade scales with war plan & warmonger flavor
	const int crusPeace = AIBuildingLinePolicy::crusadeWonderValue(100, false, 6);
	const int crusWar = AIBuildingLinePolicy::crusadeWonderValue(140, true, 6);
	assert(crusWar > crusPeace);

	// Djenne scales with desert tiles & state religion
	assert(AIBuildingLinePolicy::djenneWonderValue(0, 5, false) == 0);
	assert(AIBuildingLinePolicy::djenneWonderValue(8, 5, true) > AIBuildingLinePolicy::djenneWonderValue(8, 5, false));

	// Himeji Castle
	assert(AIBuildingLinePolicy::himejiWonderValue(120, true, 8) > AIBuildingLinePolicy::himejiWonderValue(80, false, 8));

	// Nanite Defuser: 0 if no enemy nukes or we hold overwhelming nuclear superiority
	assert(AIBuildingLinePolicy::naniteDefuserValue(0, 0) == 0);
	assert(AIBuildingLinePolicy::naniteDefuserValue(3, 7) == 0);
	assert(AIBuildingLinePolicy::naniteDefuserValue(5, 0) >= 350);
}

static void testCivicHorizonAndCorpProfit()
{
	// Normal (100% anarchy, delay 10) -> 20; Marathon (200%, delay 20) -> 80; Snail (400%, delay 40) -> 320
	assert(AIBuildingLinePolicy::scaledCivicHorizon(10, 100) == 20);
	assert(AIBuildingLinePolicy::scaledCivicHorizon(20, 200) == 80);
	assert(AIBuildingLinePolicy::scaledCivicHorizon(40, 400) == 320);

	// Corporation net value with inflation:
	// Gross 1200 + HQ 400 - maint 1000 * (1 + 100%) = 1600 - 2000 = -400 (net loss!)
	assert(AIBuildingLinePolicy::corporationNetValue100(1200, 400, 1000, 100) == -400);
	// Same corp at 0% inflation: 1600 - 1000 = +600 (profitable!)
	assert(AIBuildingLinePolicy::corporationNetValue100(1200, 400, 1000, 0) == 600);
	// Overflow safety
	assert(AIBuildingLinePolicy::corporationNetValue100(INT_MAX / 2, 1000, 0, 0) == INT_MAX / 2);
}

static void testStrategicDefensePolicies()
{
	// Staged garrison deficit: 4000 staged attack needs 5000 defense.
	// With 2000 defense across 2 defenders (avg 1000), gap is 3000 -> need 3 more defenders.
	assert(AIStrategicDefensePolicy::stagedGarrisonDeficit(4000, 2000, 2) == 3);
	// Already covered (5000 >= 5000) -> 0
	assert(AIStrategicDefensePolicy::stagedGarrisonDeficit(4000, 5000, 5) == 0);
	// Zero staged -> 0
	assert(AIStrategicDefensePolicy::stagedGarrisonDeficit(0, 1000, 1) == 0);
	// Capped at 6
	assert(AIStrategicDefensePolicy::stagedGarrisonDeficit(50000, 100, 1) == 6);

	// Proactive Open Borders cancellation
	// Non-friendly neighbor staging >= 90% of local garrison -> cancel!
	assert(AIStrategicDefensePolicy::shouldCancelOpenBordersForStaging(900, 1000, false, false, false));
	// Small scout stack (<90%) -> keep OB
	assert(!AIStrategicDefensePolicy::shouldCancelOpenBordersForStaging(500, 1000, false, false, false));
	// Friendly or vassal/master or already at war -> never cancel
	assert(!AIStrategicDefensePolicy::shouldCancelOpenBordersForStaging(5000, 1000, true, false, false));
	assert(!AIStrategicDefensePolicy::shouldCancelOpenBordersForStaging(5000, 1000, false, true, false));
	assert(!AIStrategicDefensePolicy::shouldCancelOpenBordersForStaging(5000, 1000, false, false, true));

	// Anti-hegemon detection (including 64-bit late-game powers)
	const long long bigTarget = 350000000LL;
	const long long bigTotal = 1000000000LL;
	assert(AIStrategicDefensePolicy::isHegemonThreat(bigTarget, bigTotal, 1000, 5000, 4, false));
	// Balanced power/score -> not a hegemon
	assert(!AIStrategicDefensePolicy::isHegemonThreat(200000000LL, bigTotal, 1000, 5000, 4, false));
	// Only 2 alive met teams (1v1 duel) -> don't trigger multi-team hegemon logic unless Victory Level 3
	assert(!AIStrategicDefensePolicy::isHegemonThreat(400, 1000, 400, 1000, 2, false));
	assert(AIStrategicDefensePolicy::isHegemonThreat(100, 1000, 100, 1000, 2, true));

	// 64-bit coalition power gate (no 32-bit overflow at 700M power)
	assert(AIStrategicDefensePolicy::coalitionCanMatchTarget(805000000LL, 700000000LL, 115));
	assert(!AIStrategicDefensePolicy::coalitionCanMatchTarget(804000000LL, 700000000LL, 115));
	assert(!AIStrategicDefensePolicy::coalitionCanMatchTarget(0, 100, 115));

	// Defensive counterstroke posture
	// 70% area power vs invader -> allow active counterstroke
	assert(AIStrategicDefensePolicy::defensiveCounterstrokeAllowed(7000, 10000, 0));
	// 50% area power -> turtle
	assert(!AIStrategicDefensePolicy::defensiveCounterstrokeAllowed(5000, 10000, 0));
	// Catastrophic war loss (-60 capitulation ratio) -> turtle even at 80%
	assert(!AIStrategicDefensePolicy::defensiveCounterstrokeAllowed(8000, 10000, -60));
}

int main()
{
	testNetUpgradeValue();
	testPrereqChainCredit();
	testObsolescenceFactor();
	testGoldenAgeAndMilitaryWonders();
	testPythonWonders();
	testCivicHorizonAndCorpProfit();
	testStrategicDefensePolicies();
	std::printf("ALL AI TRANSFORMATION POLICY TESTS PASSED\n");
	return 0;
}
