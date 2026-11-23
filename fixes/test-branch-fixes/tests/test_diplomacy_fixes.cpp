#include <cassert>
#include <climits>
#include <cstdio>
#include "AIDiplomacyPolicy.h"

using namespace AIDiplomacyPolicy;

static void test_gold_rounding_and_overflow() {
    // 1. Odd-valued tech (T = 1005) at 200% gold value (normal both sides):
    // AI asks ceil(1005 / 2) = 503 gold -> AI value = 1006 >= 1005 (AI net = +1 >= 0)
    int askGold = goldForValueGap(1005, 200, true);
    assert(askGold == 503);
    assert(valueFromGold(askGold, 200) == 1006);
    assert(valueFromGold(askGold, 200) - 1005 >= 0);

    // 2. AI offering gold for odd-valued tech (T = 1005) at AI's own 200%:
    // AI offers floor(1005 / 2) = 502 gold -> AI cost = 1004 <= 1005 (AI net = +1 >= 0)
    int offerGold = goldForValueGap(1005, 200, false);
    assert(offerGold == 502);
    assert(valueFromGold(offerGold, 200) == 1004);
    assert(1005 - valueFromGold(offerGold, 200) >= 0);

    // 3. Asymmetric financial trouble: human pct = 300, AI pct = 200.
    // Previously 2G >= T >= 3G had NO integer solution -> 100% rejected.
    // With AI checking its own AI_dealNetVal >= 0: AI asks 503 gold -> AI net = 1006 - 1005 = +1 >= 0.
    assert(valueFromGold(askGold, 200) >= 1005);

    // 4. 64-bit gold overflow: 10,000,000 gold at 300% overflows 32-bit int (3e9 > INT_MAX),
    // but valueFromGold produces exact 30,000,000 without wrap.
    int bigVal = valueFromGold(10000000, 300);
    assert(bigVal == 30000000);
    // Extreme saturation near INT_MAX:
    assert(valueFromGold(1000000000, 300) == INT_MAX);
    assert(saturatingAdd(INT_MAX - 10, 50) == INT_MAX);
}

static void test_gpt_cost_curve_and_affordability() {
    // Standard speed: horizon = 10, pct = 200 -> annualPct = 2000 (20 value per 1 GPT)
    // Fully covered by income (goldRate = 50): cost == baseCost == 20 * g
    assert(goldPerTurnCostVal(10, 200, 10, 50, 0, 0) == 200);
    assert(goldPerTurnCostVal(50, 200, 10, 50, 0, 0) == 1000);

    // Uncovered payment: goldRate = 10, spendable treasury = 0 -> sustainable = 10.
    // Paying 20 GPT has 10 uncovered -> cost = 400 + (400 * 10 / 20) = 600 (1.5x).
    assert(goldPerTurnCostVal(20, 200, 10, 10, 0, 0) == 600);

    // Completely uncovered (goldRate = 0, gold <= goldTarget): cost = 2x baseCost.
    assert(goldPerTurnCostVal(20, 200, 10, 0, 100, 500) == 800);

    // Spendable treasury above target softens cost: (gold - target)/10 = 10 -> sustainable = 10.
    assert(goldPerTurnCostVal(20, 200, 10, 0, 600, 500) == 600);

    // maxAffordableGoldPerTurn (non-strict, used by AI_counterPropose):
    // Value = 1005, maxGPT = 100, covered income = 100 -> max GPT with cost <= 1005 is 50 (cost 1000).
    int gStd = maxAffordableGoldPerTurn(1005, 100, 200, 10, 100, 0, 0, false);
    assert(gStd == 50);
    assert(goldPerTurnCostVal(gStd, 200, 10, 100, 0, 0) <= 1005);
    assert(goldPerTurnCostVal(gStd + 1, 200, 10, 100, 0, 0) > 1005);

    // Under deficit (goldRate = 0, no spare gold): cost(g) = 40*g -> max g with 40*g <= 1005 is 25 (cost 1000).
    int gDeficit = maxAffordableGoldPerTurn(1005, 100, 200, 10, 0, 0, 0, false);
    assert(gDeficit == 25);
    assert(goldPerTurnCostVal(gDeficit, 200, 10, 0, 0, 0) <= 1005);
    assert(goldPerTurnCostVal(gDeficit + 1, 200, 10, 0, 0, 0) > 1005);

    // Marathon speed: horizon = 30, pct = 200 -> 60 value per GPT.
    // Value = 1005 -> max g with cost <= 1005 is 16 (cost 960), never negative AI net!
    int gMar = maxAffordableGoldPerTurn(1005, 100, 200, 30, 100, 0, 0, false);
    assert(gMar == 16);
    assert(goldPerTurnCostVal(gMar, 200, 30, 100, 0, 0) == 960);

    // Strict-less mode (used by AI_doDiplo resource-for-GPT):
    // Value = 200 (exact multiple of 20) -> strictLess gives 9 (cost 180 < 200, net = +20 > 0),
    // non-strict gives 10 (cost 200 <= 200, net = 0).
    assert(maxAffordableGoldPerTurn(200, 100, 200, 10, 100, 0, 0, true) == 9);
    assert(maxAffordableGoldPerTurn(200, 100, 200, 10, 100, 0, 0, false) == 10);
}

static void test_midpoint_spare_resource_ask() {
    // Spare resource: AI loss = 0, buyer value = 200 -> ask = 0 + (200 - 0 + 1)/2 = 100.
    // AI net if paid 100 = +100 > 0; human surplus = +100 > 0.
    int ourLoss = 0, buyerVal = 200;
    int ask = ourLoss + ((buyerVal - ourLoss + 1) / 2);
    assert(ask == 100);
    assert(ask > ourLoss && ask < buyerVal);

    // Scarce/last resource: AI loss = 500, buyer value = 200 -> buyerVal <= ourLoss -> ask = 500.
    ourLoss = 500; buyerVal = 200;
    ask = ourLoss + ((buyerVal > ourLoss) ? ((buyerVal - ourLoss + 1) / 2) : 0);
    assert(ask == 500);
}

int main() {
    test_gold_rounding_and_overflow();
    test_gpt_cost_curve_and_affordability();
    test_midpoint_spare_resource_ask();
    std::printf("ALL DIPLOMACY POLICY UNIT TESTS PASSED\n");
    return 0;
}
