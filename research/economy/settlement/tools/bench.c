/* Cost of the settlement economy's per-turn pass, as the DLL would run it: integer accounts in hundredths,
 * recipes, proportional rationing with largest remainders, stocks with spoilage. One trade network per player.
 * Prints microseconds per game turn for a grid of city counts and catalogue sizes, and the cost of the AI's
 * marginal values (one recomputation of its network per good).
 * build: gcc -O2 -o bench bench.c ; run: ./bench
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

static uint32_t rs = 2463534242u;
static uint32_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 17; rs ^= rs << 5; return rs; }

typedef struct { int64_t d; int64_t frac; int idx; } Rem;
static int cmp_rem(const void* a, const void* b)
{
	const Rem* x = (const Rem*)a; const Rem* y = (const Rem*)b;
	if (x->frac != y->frac) return x->frac > y->frac ? -1 : 1;
	return x->idx - y->idx;
}

/* give[i] = share of avail by demand[i], exact, deterministic */
static void ration(int64_t avail, const int64_t* demand, int64_t* give, int n, Rem* tmp)
{
	int64_t tot = 0; int i;
	for (i = 0; i < n; i++) tot += demand[i];
	if (tot <= avail) { memcpy(give, demand, n * sizeof(int64_t)); return; }
	if (tot == 0 || avail <= 0) { memset(give, 0, n * sizeof(int64_t)); return; }
	int64_t sum = 0;
	for (i = 0; i < n; i++) { give[i] = demand[i] * avail / tot; sum += give[i]; tmp[i].frac = demand[i] * avail - give[i] * tot; tmp[i].idx = i; }
	int64_t rem = avail - sum;
	if (rem > 0) { qsort(tmp, n, sizeof(Rem), cmp_rem); for (i = 0; i < rem && i < n; i++) give[tmp[i].idx] += 1; }
}

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec * 1e-9; }

/* one turn for one network of n cities, g goods, needs = g/2 (each need draws on 2 goods), r recipes per city */
static int64_t network_turn(int n, int g, int r, int64_t* prod, int64_t* stock, int64_t* need, int64_t* got, int64_t* tmpd, int64_t* tmpg, Rem* tmp)
{
	int c, k, j, nn = g / 2;
	int64_t check = 0;
	for (c = 0; c < n; c++)              /* supply = production + stock; recipes in dependency order */
	{
		int64_t* p = prod + (int64_t)c * g; int64_t* s = stock + (int64_t)c * g;
		for (k = 0; k < g; k++) p[k] += s[k];
		for (j = 0; j < r; j++)
		{
			int a = (j * 3) % g, b = (j * 5 + 1) % g, o = (j * 7 + 2) % g;
			int64_t runs = p[a] < p[b] ? p[a] : p[b]; if (runs > 500) runs = 500;
			p[a] -= runs; p[b] -= runs; p[o] += runs;
		}
	}
	for (k = 0; k < nn; k++)             /* each need, from its two goods, rationed across the network */
	{
		for (c = 0; c < n; c++) got[(int64_t)c * nn + k] = 0;
		for (j = 0; j < 2; j++)
		{
			int gi = (k * 2 + j) % g; int64_t pool = 0;
			for (c = 0; c < n; c++) { pool += prod[(int64_t)c * g + gi]; tmpd[c] = need[(int64_t)c * nn + k] - got[(int64_t)c * nn + k]; }
			ration(pool, tmpd, tmpg, n, tmp);
			int64_t taken = 0;
			for (c = 0; c < n; c++) { got[(int64_t)c * nn + k] += tmpg[c]; taken += tmpg[c]; tmpd[c] = prod[(int64_t)c * g + gi]; }
			ration(taken, tmpd, tmpg, n, tmp);
			for (c = 0; c < n; c++) prod[(int64_t)c * g + gi] -= tmpg[c];
		}
	}
	for (c = 0; c < n; c++)              /* leftovers to stock, spoilage on a quarter of the goods */
		for (k = 0; k < g; k++)
		{
			int64_t v = prod[(int64_t)c * g + k];
			if (k % 4 == 0) v -= v * 10 / 100;
			stock[(int64_t)c * g + k] = v; check += v;
		}
	return check;
}

int main(void)
{
	int cities[] = {60, 120, 300, 600};
	int goods[] = {12, 40, 100};
	int players = 18, reps = 200;
	printf("cities,goods,recipes_per_city,us_per_turn,us_per_turn_with_ai_marginals,bytes_state\n");
	for (int ci = 0; ci < 4; ci++)
		for (int gi = 0; gi < 3; gi++)
		{
			int C = cities[ci], g = goods[gi], r = g / 4, nn = g / 2;
			int n = C / players; if (n < 1) n = 1;
			int64_t* prod = malloc(sizeof(int64_t) * n * g); int64_t* stock = calloc(n * g, sizeof(int64_t));
			int64_t* need = malloc(sizeof(int64_t) * n * nn); int64_t* got = malloc(sizeof(int64_t) * n * nn);
			int64_t* tmpd = malloc(sizeof(int64_t) * n); int64_t* tmpg = malloc(sizeof(int64_t) * n); Rem* tmp = malloc(sizeof(Rem) * n);
			int64_t sink = 0; double t0 = now();
			for (int rep = 0; rep < reps; rep++)
				for (int p = 0; p < players; p++)
				{
					for (int i = 0; i < n * g; i++) prod[i] = rnd() % 800;
					for (int i = 0; i < n * nn; i++) need[i] = rnd() % 600;
					sink += network_turn(n, g, r, prod, stock, need, got, tmpd, tmpg, tmp);
				}
			double us = (now() - t0) / reps * 1e6;
			/* AI marginal values: per player, one extra recomputation of its network per good */
			t0 = now();
			for (int rep = 0; rep < reps / 10 + 1; rep++)
				for (int p = 0; p < players; p++)
					for (int k = 0; k < g; k++)
					{
						for (int i = 0; i < n * g; i++) prod[i] = rnd() % 800;
						for (int i = 0; i < n * nn; i++) need[i] = rnd() % 600;
						sink += network_turn(n, g, r, prod, stock, need, got, tmpd, tmpg, tmp);
					}
			double us_ai = (now() - t0) / (reps / 10 + 1) * 1e6;
			long bytes = (long)C * g * 4 * 2 + (long)C * nn * 4;  /* stock and last turn's flow per good (int32), met per need */
			printf("%d,%d,%d,%.1f,%.1f,%ld\n", C, g, r, us, us + us_ai, bytes);
			free(prod); free(stock); free(need); free(got); free(tmpd); free(tmpg); free(tmp);
			if (sink == 42) printf("!");
		}
	return 0;
}
