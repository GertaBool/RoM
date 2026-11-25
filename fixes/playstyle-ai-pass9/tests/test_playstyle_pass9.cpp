#include <cassert>
#include <climits>
#include <cstdio>
#include "AIPlaystylePolicy.h"

using namespace AIPlaystylePolicy;

int main()
{
	// --- Block #1: Projected Trade Routes for 0-Route Cities ---
	// 0-route city building Port (+3 routes, avg 4/slot) projects 12 yield instead of 0.
	assert(projectedTradeYield(0, 0, 3, 4, false) == 12);
	// 1-route city (yield 5) building Port (+3 routes) projects 5 + 3*5 = 20.
	assert(projectedTradeYield(5, 1, 3, 4, false) == 20);
	// 0-route city building pure modifier Lighthouse/Jewellery/Market projects 65% of 1 slot
	// (nonzero so it is not blind, while still ranking behind route-creating buildings).
	int iLighthouseProj = projectedTradeYield(0, 0, 0, 4, true);
	assert(iLighthouseProj >= 2 && iLighthouseProj < 12);
	// 0-route city unable to gain route soon stays 0.
	assert(projectedTradeYield(0, 0, 0, 4, false) == 0);
	// Overflow safety.
	assert(projectedTradeYield(INT_MAX, 1, 10, 100, false) == INT_MAX);

	// --- Block #2: Full Golden Age Valuation & Great People Math ---
	// Pending civic swaps (2 anarchy turns on 500 output/turn) + 150% multipliers + GP rate.
	int iGaNoSwap = goldenAgeTotalValue(1000, 150, 500, 0, 10, 20, false);
	int iGaWithSwap = goldenAgeTotalValue(1000, 150, 500, 2, 10, 20, false);
	assert(iGaNoSwap == 1500 + 20 * 10 * 3);
	assert(iGaWithSwap == iGaNoSwap + (500 * 2 * 120) / 100);
	// Already in Golden Age must not double-count anarchy skip.
	assert(goldenAgeTotalValue(1000, 150, 500, 2, 10, 20, true) == iGaNoSwap);
	// Overflow saturation.
	assert(goldenAgeTotalValue(INT_MAX, 350, INT_MAX, 6, 40, 500, false) == INT_MAX);

	// Academy NPV: high-share capital beats early GA; mediocre city loses to large-empire GA.
	int iSmallCapAcad = academyConstructNpv(40, 50, 60);
	int iMedCityAcad = academyConstructNpv(15, 50, 60);
	assert(iSmallCapAcad == 720);
	assert(iMedCityAcad == 270);
	assert(iMedCityAcad < iGaWithSwap);
	assert(academyConstructNpv(0, 50, 60) == 0);

	// Great Engineer wonder hurry discount: gold-hurriable or <= 4 turns heavily discounted.
	assert(engineerWonderHurryDiscountPct(true, 800, 1200, 15) == 25);
	assert(engineerWonderHurryDiscountPct(true, 1600, 900, 15) == 55);
	assert(engineerWonderHurryDiscountPct(false, 0, 0, 3) == 15);
	assert(engineerWonderHurryDiscountPct(false, 0, 0, 18) == 100);

	// Food corporation weighting scales with happy/health growth headroom.
	assert(foodCorporationYieldWeight(4, 3) == 170);
	assert(foodCorporationYieldWeight(2, 1) == 145);
	assert(foodCorporationYieldWeight(0, 3) == 120);
	assert(foodCorporationYieldWeight(-1, 2) == 90);

	// --- Block #2C: Tangential Tech-for-Gold Selling ---
	// Unaffordable expensive tech returns 0 instead of blocking cheaper tangential tech sales.
	assert(tangentialTechSaleScore(1200, 350, false, false, false, false, false) == 0);
	int iTangential = tangentialTechSaleScore(300, 350, false, false, false, false, false);
	int iMilitarySafe = tangentialTechSaleScore(300, 350, true, false, false, false, false);
	assert(iTangential > iMilitarySafe && iTangential > 0);
	// Refuse selling military tech to border threats, higher-rank rivals, or any tech to war targets.
	assert(tangentialTechSaleScore(300, 350, true, false, true, false, false) == 0);
	assert(tangentialTechSaleScore(300, 350, false, false, false, true, false) == 0);
	assert(tangentialTechSaleScore(300, 350, true, false, false, false, true) == 0);
	assert(tangentialTechSaleScore(300, 350, false, true, false, false, true) == 0);

	// --- Block #3: Land XML Ranged Combat, Collateral Ordering, Skirmish, Turn ROI ---
	// Zero effective damage returns 0 (never wastes volley on already-capped target).
	assert(rangeTargetScore(0, 0, 800, 25, true, 5, true, true) == 0);
	// Healthy defended city stack heavily outranks lone wounded field scout.
	int iCityStack = rangeTargetScore(30, 20, 600, 100, true, 5, true, true);
	int iWoundedScout = rangeTargetScore(15, 0, 200, 30, false, 1, false, false);
	assert(iCityStack > iWoundedScout * 5);

	// Collateral cavalry (Horse Archer collat=25, 4 targets, 45% odds) gets enough rank boost
	// to strike BEFORE a 70% Swordsman (450 + bonus > 700).
	int iHaBonus = collateralAttackPriorityBonus(450, 25, 4, 100);
	assert(450 + iHaBonus > 700);
	// Lone target or hopeless non-siege suicide gets 0 bonus.
	assert(collateralAttackPriorityBonus(450, 25, 0, 100) == 0);
	assert(collateralAttackPriorityBonus(100, 25, 4, 100) == 0);
	// Full siege (collat=100) still prioritizes softening large stacks even at low odds.
	assert(collateralAttackPriorityBonus(100, 100, 4, 100) > 400);

	// Land ranged unit valuation: Longbowman (airLim=90), Horse Archer (collat), Artillery (range 2).
	int iLongbowBonus = landRangedUnitValueBonus(600, 6, 1, 90, false);
	int iHaRangedBonus = landRangedUnitValueBonus(600, 6, 1, 75, true);
	int iArtilleryBonus = landRangedUnitValueBonus(1800, 18, 2, 50, true);
	assert(iLongbowBonus > 200);
	assert(iHaRangedBonus > iLongbowBonus);
	assert(iArtilleryBonus > iLongbowBonus * 2);
	assert(landRangedUnitValueBonus(600, 0, 0, 0, false) == 0);

	// Circumstantial 2-move skirmish: never abandons mixed stack, escort, or city.
	assert(!shouldSkirmishStepAndShoot(0, 600, 500, true, false, false));
	assert(!shouldSkirmishStepAndShoot(0, 600, 500, false, true, false));
	assert(!shouldSkirmishStepAndShoot(0, 600, 500, false, false, true));
	assert(shouldSkirmishStepAndShoot(400, 600, 500, false, false, false));
	assert(!shouldSkirmishStepAndShoot(600, 600, 500, false, false, false));
	assert(!shouldSkirmishRetreatAfterShot(500, 600, 0, 50, false, false, false));
	assert(shouldSkirmishRetreatAfterShot(500, 200, 0, 0, false, false, false));
	assert(shouldSkirmishRetreatAfterShot(500, 500, 0, 50, false, false, false));
	assert(!shouldSkirmishRetreatAfterShot(500, 0, 0, 50, true, false, false));

	// Turn-time ROI divisor steepens above 5 turns.
	assert(unitTurnTimeDivisor(4, false) == 7);
	assert(unitTurnTimeDivisor(5, false) == 8);
	assert(unitTurnTimeDivisor(11, false) == 17);

	// --- Block #4: Espionage Floor, RevDCM Research Floor, Upgrade Reserve, Coastal Threat ---
	assert(espionageFloorPercent(3, 80, false, true, 1) == 5);
	assert(espionageFloorPercent(3, 130, false, true, 2) == 10);
	assert(espionageFloorPercent(3, 130, true, true, 2) == 0);
	assert(espionageFloorPercent(3, 130, false, true, 0) == 0);
	assert(revDcmResearchFloorPercent(2, false, 500, -20) == 50);
	assert(revDcmResearchFloorPercent(2, false, 40, -20) == 0);
	assert(revDcmResearchFloorPercent(0, false, 500, 10) == 0);

	assert(urgentUpgradeReserve(600, true, false, false, 1000) == 600);
	assert(urgentUpgradeReserve(600, false, true, false, 1000) == 450);
	assert(urgentUpgradeReserve(600, false, false, false, 1000) == 240);
	assert(urgentUpgradeReserve(600, true, false, false, 300) == 300);

	assert(coastalNavalThreatDefenders(0, 0, true) == 0);
	assert(coastalNavalThreatDefenders(1, 2, true) == 2);
	assert(coastalNavalThreatDefenders(1, 2, false) == 1);
	assert(coastalNavalThreatDefenders(3, 0, true) == 1);

	std::printf("ALL Pass 9 AIPlaystylePolicy C++98 UNIT TESTS PASSED!\n");
	return 0;
}
