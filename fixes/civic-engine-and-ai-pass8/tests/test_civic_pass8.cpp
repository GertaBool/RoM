#include <cassert>
#include <cstdio>
#include <cstdlib>
#include "AICivicPolicy.h"

static void testPlotProgressLatticeExactness()
{
	// Exhaustive verification across all RoM positive modifiers (0%..+250% step 5),
	// multiple upgrade targets (Normal, Epic, Marathon, Snail), and EVERY starting
	// progress p0 in [0, T-1] including off-lattice legacy-save / mid-upgrade values.
	const int aiTargets[] = { 1, 5, 10, 11, 20, 30, 40, 60, 90, 120 };
	const int iNumTargets = (int)(sizeof(aiTargets) / sizeof(aiTargets[0]));

	for (int iMod = 0; iMod <= 250; iMod += 5)
	{
		for (int iTi = 0; iTi < iNumTargets; ++iTi)
		{
			const int iT = aiTargets[iTi];
			for (int iP0 = 0; iP0 < iT; ++iP0)
			{
				const int iPredEven = AICivicPolicy::improvementUpgradeTurnsLeft(iP0, iT, 0, iMod);
				const int iPredOdd = AICivicPolicy::improvementUpgradeTurnsLeft(iP0, iT, 1, iMod);
				// Zero UI turn-parity flicker for all non-negative modifiers.
				assert(iPredEven == iPredOdd);

				int iProg = iP0;
				int iTurns = 0;
				int iPrevLeft = iPredEven;
				while (iProg < iT)
				{
					const int iStepA = AICivicPolicy::improvementUpgradeStep(iProg, iTurns, iMod);
					const int iStepB = AICivicPolicy::improvementUpgradeStep(iProg, iTurns + 1, iMod);
					// Zero turn-parity micro-exploit for all non-negative modifiers.
					assert(iStepA == iStepB);
					assert(iStepA >= 1);
					iProg += iStepA;
					++iTurns;
					if (iProg < iT)
					{
						const int iNowLeft = AICivicPolicy::improvementUpgradeTurnsLeft(iProg, iT, iTurns, iMod);
						assert(iNowLeft == iPrevLeft - 1);
						iPrevLeft = iNowLeft;
					}
				}
				assert(iTurns == iPredEven);
			}
		}
	}

	// Concrete RoM spot checks:
	// Normal Cottage (10): +0% -> 10t, +15% -> 9t, +25% -> 8t, +50% Peasantry -> 7t, +100% Trade School -> 5t
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 10, 0, 0) == 10);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 10, 0, 15) == 9);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 10, 0, 25) == 8);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 10, 0, 50) == 7);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 10, 0, 100) == 5);
	// Marathon Village (120): +10% Barter -> 110t, +20% Coinage -> 100t, +50% Peasantry -> 80t, +200% -> 40t
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 120, 0, 10) == 110);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 120, 0, 20) == 100);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 120, 0, 50) == 80);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(0, 120, 0, 200) == 40);

	// Conservative civic-toggle check: off-lattice p=2 under +50% snaps to 3 (step=1), never free-jumping.
	assert(AICivicPolicy::improvementUpgradeStep(2, 0, 50) == 1);
	// Already complete or negative progress guards.
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(10, 10, 0, 50) == 1);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(15, 10, 0, 50) == 1);
	assert(AICivicPolicy::improvementUpgradeStep(-5, 0, 50) == 1);
}

static void testNegativeModifierFallback()
{
	// Hypothetical modded negative modifiers (-75%, -50%, -25%) must never stall and
	// must match improvementUpgradeTurnsLeft() monotonically turn-for-turn.
	const int aiNegMods[] = { -75, -50, -25, -10 };
	for (int iMi = 0; iMi < 4; ++iMi)
	{
		const int iMod = aiNegMods[iMi];
		for (int iStartTurn = 0; iStartTurn < 17; ++iStartTurn)
		{
			const int iT = 12;
			int iProg = 0;
			int iTurn = iStartTurn;
			int iPrevLeft = AICivicPolicy::improvementUpgradeTurnsLeft(iProg, iT, iTurn, iMod);
			int iSim = 0;
			while (iProg < iT)
			{
				const int iStep = AICivicPolicy::improvementUpgradeStep(iProg, iTurn, iMod);
				assert(iStep == 0 || iStep == 1);
				iProg += iStep;
				++iTurn;
				++iSim;
				if (iProg < iT)
				{
					const int iNowLeft = AICivicPolicy::improvementUpgradeTurnsLeft(iProg, iT, iTurn, iMod);
					assert(iNowLeft == iPrevLeft - 1);
					iPrevLeft = iNowLeft;
				}
			}
			assert(iSim == AICivicPolicy::improvementUpgradeTurnsLeft(0, iT, iStartTurn, iMod));
		}
	}

	// Zero-rate clamp (-100% or lower): step=0, returns remaining progress.
	assert(AICivicPolicy::improvementUpgradeStep(0, 0, -100) == 0);
	assert(AICivicPolicy::improvementUpgradeTurnsLeft(3, 10, 0, -100) == 7);
}

static void testScaledWorkRateFloor()
{
	assert(AICivicPolicy::scaledWorkRate(0, 0, 0, false) == 0);
	assert(AICivicPolicy::scaledWorkRate(100, 0, 0, false) == 100);
	assert(AICivicPolicy::scaledWorkRate(100, -75, 0, false) == 25);
	// Stacked -100% or -150% floors at 10% (never zero-stalls).
	assert(AICivicPolicy::scaledWorkRate(100, -100, 0, false) == 10);
	assert(AICivicPolicy::scaledWorkRate(100, -150, 0, false) == 10);
	// Tiny base rate with heavy negative AI + civic modifier floors at 1.
	assert(AICivicPolicy::scaledWorkRate(5, -100, -100, true) == 1);
	// Positive bonuses scale normally.
	assert(AICivicPolicy::scaledWorkRate(100, 50, 20, true) == 180);
}

int main()
{
	testPlotProgressLatticeExactness();
	testNegativeModifierFallback();
	testScaledWorkRateFloor();
	std::printf("test_civic_pass8: ALL PASSED\n");
	return 0;
}
