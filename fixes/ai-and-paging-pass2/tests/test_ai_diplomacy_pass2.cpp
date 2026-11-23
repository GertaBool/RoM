#include <cassert>
#include <climits>
#include <cstdio>

#include "AIDiplomacyPolicy.h"

static void test_resource_reservation_closes_1gpt_exploit()
{
	// Spare resource (ourLoss == 0), buyer values it at 200 (e.g., 10 GPT * 20 turns).
	// Creation floor at 40% demands 80 (4 GPT) — a 1 GPT offer (20) is rejected!
	const int createFloor = AIDiplomacyPolicy::resourceReservationVal(0, 200, 40);
	assert(createFloor == 80);
	assert(20 < createFloor);

	// Strategic military resource for non-friendly buyer at 50% demands 100 (5 GPT).
	const int strategicFloor = AIDiplomacyPolicy::resourceReservationVal(0, 200, 50);
	assert(strategicFloor == 100);

	// Counter-proposal asks 50% midpoint (100), which clears creation (80) and
	// renewal (30% = 60, with 10% hysteresis: 100 * 110 >= 60 * 100).
	const int renewFloor = AIDiplomacyPolicy::resourceReservationVal(0, 200, 30);
	assert(renewFloor == 60);
	assert(AIDiplomacyPolicy::isWeightedGreater(110, createFloor, 100, renewFloor));

	// Renegotiation when buyer outgrows an Ancient-Era 2-GPT deal (40 value):
	// Once buyer valuation climbs to 400 (20 GPT), 30% floor is 120; 40*110 < 120*100 -> cancel!
	const int lateRenewFloor = AIDiplomacyPolicy::resourceReservationVal(0, 400, 30);
	assert(lateRenewFloor == 120);
	assert(!AIDiplomacyPolicy::isWeightedGreater(110, 40, 100, lateRenewFloor));

	// When our own copy is pillaged (ourLoss == 180) and buyer values it at 200:
	// Reservation price = 180 + (20 * 30 / 100) = 186 -> forces cancellation of cheap deal!
	assert(AIDiplomacyPolicy::resourceReservationVal(180, 200, 30) == 186);

	// Tiny positive surplus rounds up to at least +1 above ourLoss so 0-value giveaway cannot sneak past.
	assert(AIDiplomacyPolicy::resourceReservationVal(0, 2, 40) == 1);
	assert(AIDiplomacyPolicy::resourceReservationVal(50, 50, 40) == 50);
	assert(AIDiplomacyPolicy::resourceReservationVal(50, 10, 40) == 50);
	assert(AIDiplomacyPolicy::resourceReservationVal(-10, 100, 40) == 40);
}

static void test_64bit_power_arithmetic_no_overflow()
{
	// Late-game RoM power reaches 10^7 - 10^9 where 32-bit int*220 or int*190 wraps negative.
	const int hugePower = 50000000; // 50M (32-bit 100*hugePower overflows!)
	assert(AIDiplomacyPolicy::powerRatioPercent(hugePower, hugePower) == 100);
	assert(AIDiplomacyPolicy::powerRatioPercent(2 * hugePower, hugePower) == 200);
	assert(AIDiplomacyPolicy::powerRatioPercent(hugePower, 0) == INT_MAX);

	// AI_surrenderTrade: 5*iVassalPower > 4*iAveragePower at 600M power (32-bit overflows!).
	const int pA = 600000000;
	const int pB = 700000000;
	assert(AIDiplomacyPolicy::isWeightedGreater(5, pA, 4, pB));  // 3.0B > 2.8B
	assert(AIDiplomacyPolicy::isWeightedGreater(3, pA, 2, pB));  // 1.8B > 1.4B
	assert(!AIDiplomacyPolicy::isWeightedGreater(3, 400000000, 2, 700000000)); // 1.2B < 1.4B

	// AI_endWarVal: 7 * (5 * iTheirPower) / (10 * (iOurPower + 4 * iTheirPower))
	const long long theirP = 200000000;
	const long long ourP = 300000000;
	// 1000 * (35 * 200M) / (10 * (300M + 800M)) = 1000 * 7000 / 11000 = 636
	assert(AIDiplomacyPolicy::scaleByRatio64(1000, 35 * theirP, 10 * (ourP + 4 * theirP)) == 636);

	// AI_surrenderTrade iVassalPower: getPower(true) * 190 / 100 at 50M power
	assert(AIDiplomacyPolicy::scaleByRatio64(hugePower, 190, 100) == 95000000);

	// AI_declareWarTradeVal: iValue * (50 + 100*warPower/(theirPower+warPower+1)) / 100
	const long long pSum = (long long)hugePower + (long long)hugePower + 1;
	const int factor = (int)(50 + ((long long)100 * hugePower) / pSum);
	assert(factor == 99);
	assert(AIDiplomacyPolicy::scaleByRatio64(1000, factor, 100) == 990);

	// Saturation bounds
	assert(AIDiplomacyPolicy::scaleByRatio64(INT_MAX, 10, 1) == INT_MAX);
	assert(AIDiplomacyPolicy::scaleByRatio64(INT_MIN, 10, 1) == INT_MIN);
}

static void test_gold_per_turn_and_gap_helpers()
{
	assert(AIDiplomacyPolicy::goldForValueGap(100, 100, true) == 100);
	assert(AIDiplomacyPolicy::goldForValueGap(101, 100, true) == 101);
	assert(AIDiplomacyPolicy::goldForValueGap(1, 3, true) == 34);
	assert(AIDiplomacyPolicy::goldForValueGap(1, 0, true) == 0);

	// GPT cost doubles uncovered portion when AI is in deficit
	const int covered = AIDiplomacyPolicy::goldPerTurnCostVal(10, 100, 20, 20, 0, 0);
	const int uncovered = AIDiplomacyPolicy::goldPerTurnCostVal(10, 100, 20, 0, 0, 0);
	assert(covered == 200);
	assert(uncovered == 400);
}

int main()
{
	test_resource_reservation_closes_1gpt_exploit();
	test_64bit_power_arithmetic_no_overflow();
	test_gold_per_turn_and_gap_helpers();
	std::printf("ALL AIDiplomacyPolicy pass-2 unit tests passed!\n");
	return 0;
}
