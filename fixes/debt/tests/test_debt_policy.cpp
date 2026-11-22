// Native checks of AIDebtPolicy.h (the debt arithmetic of the DLL), without the game.
// usage: g++ -std=c++98 -I <Assets/CvGameCoreDLL> test_debt_policy.cpp -o t && ./t
#include <cstdio>
#include <cstdlib>
#include "AIDebtPolicy.h"
using namespace AIDebtPolicy;

static int failures = 0;
#define CHECK(c) do { if (!(c)) { std::printf("FAIL %s:%d %s\n", __FILE__, __LINE__, #c); ++failures; } } while (0)

// Run a loan to its end with every payment made; return what is left owed.
static long long simulateLoan(int principal, int rate, int turns, long long* paid)
{
	long long owed = principal;
	const int payment = annuityPayment(principal, rate, turns);
	*paid = 0;
	for (int t = 0; t < turns && owed > 0; ++t)
	{
		owed += interestFor((int)owed, rate);
		long long pay = owed < payment ? owed : payment;
		owed -= pay;
		*paid += pay;
	}
	return owed;
}

int main()
{
	// Interest rounds up and is zero only for zero amounts or rates.
	CHECK(interestFor(1000, 4000) == 4);
	CHECK(interestFor(1, 1) == 1);
	CHECK(interestFor(0, 5000) == 0 && interestFor(100, 0) == 0);

	// Annuities repay within their term, never pay less than the principal, and cost
	// little more than the principal at low rates.
	const int principals[] = { 10, 100, 1000, 25000, 400000 };
	const int rates[] = { 0, 1, 500, 4000, 12000, 30000, 100000 };
	const int terms[] = { 1, 5, 10, 21, 63, 105, 214 };
	for (int a = 0; a < 5; ++a)
		for (int b = 0; b < 7; ++b)
			for (int c = 0; c < 7; ++c)
			{
				long long paid = 0;
				const long long left = simulateLoan(principals[a], rates[b], terms[c], &paid);
				CHECK(left == 0);
				CHECK(paid >= principals[a]);
				CHECK(annuityPayment(principals[a], rates[b], terms[c]) > 0);
			}
	// Zero rate: the principal split over the term, rounded up.
	CHECK(annuityPayment(100, 0, 10) == 10 && annuityPayment(101, 0, 10) == 11);
	// A known case: 1000 at 1% for 10 turns pays about 105.6 a turn.
	CHECK(annuityPayment(1000, 10000, 10) >= 105 && annuityPayment(1000, 10000, 10) <= 107);

	// Speed conversion: Normal unchanged; longer games get a lower rate per turn that
	// compounds to the same growth over the same share of the game.
	CHECK(rateForSpeed(4000, 100) == 4000);
	const int r210 = rateForSpeed(4000, 210);
	CHECK(r210 < 4000 && r210 > 1800);
	CHECK(growthFactor(r210, 210) >= growthFactor(4000, 100));
	CHECK(growthFactor(r210 - 1, 210) < growthFactor(4000, 100));
	const int r31 = rateForSpeed(4000, 31);
	CHECK(r31 > 4000);
	CHECK(growthFactor(r31, 31) >= growthFactor(4000, 100));
	CHECK(scaleTurns(10, 210) == 21 && scaleTurns(10, 31) == 3 && scaleTurns(0, 100) == 1);

	// Credit: better figures give a better score; spreads fall as scores rise.
	CHECK(creditScore(0, false, 0, false, false, 30) == 90);
	CHECK(creditScore(80, true, 30, true, true, 0) == 0);
	CHECK(creditScore(10, false, 0, false, false, 10) > creditScore(30, false, 0, false, false, 10));
	for (int s = 0; s < 100; ++s)
	{
		CHECK(creditSpread(s, 12000) >= creditSpread(s + 1, 12000));
	}
	CHECK(creditSpread(100, 12000) == 0 && creditSpread(0, 12000) == 12000);

	// Limits: the payment of the largest loan fits the room, one more gold does not.
	const int limit = borrowingLimit(200, 25, 10, 4000, 21, false, 100000);
	CHECK(limit > 0);
	CHECK(annuityPayment(limit, 4000, 21) <= 40);
	CHECK(annuityPayment(limit + 1, 4000, 21) > 40);
	CHECK(borrowingLimit(200, 25, 50, 4000, 21, false, 100000) == 0);
	CHECK(borrowingLimit(200, 25, 0, 4000, 21, false, 300) == 300);
	const int bondLimit = borrowingLimit(200, 25, 0, 4000, 21, true, 1000000);
	CHECK(couponPayment(bondLimit, 4000) <= 50 && couponPayment(bondLimit + 1000, 4000) > 50);

	// Present value: no discount sums the payments; discounting lowers it.
	CHECK(presentValue(10, 5, 100, 0) == 150);
	CHECK(presentValue(10, 5, 100, 10000) < 150);
	// A loan priced at the lender's own hurdle with certain payment is worth about zero.
	const int pay = annuityPayment(1000, 10000, 20);
	const int v = loanValueToLender(1000, pay, 20, 0, 10000, 100);
	CHECK(v >= 0 && v < 20);
	CHECK(loanValueToLender(1000, pay, 20, 0, 10000, 80) < 0);

	if (failures == 0) std::printf("all debt policy checks passed\n");
	return failures ? 1 : 0;
}
