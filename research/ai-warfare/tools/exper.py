#!/usr/bin/env python3
"""Compare two AI variants from independent seeded runs (framework.md, section 7).

usage: exper.py <a.txt> <b.txt> [--min-runs 30]     one result per line, one run per seed

Prints n, median and mean of each, then the two-tailed Welch t-test on ranks (Luke,
Essentials of Metaheuristics, 11.1.2, after Wineberg and Christensen): pool, rank (ties get
their mean rank), Welch's test on the ranks. Effect size: the probability that a run of A beats
a run of B (Vargha-Delaney A, from the same ranks; 0.5 = no difference). Exit 2 if either
side has fewer than --min-runs results.
"""
import sys

from scipy import stats


def rank_welch(a, b):
    r = stats.rankdata(list(a) + list(b))
    ra, rb = r[:len(a)], r[len(a):]
    t = stats.ttest_ind(ra, rb, equal_var=False)
    na, nb = len(a), len(b)
    A = (ra.sum() / na - (na + 1) / 2) / nb
    return t.statistic, t.df, t.pvalue, A


def main():
    args = [x for x in sys.argv[1:] if not x.startswith('--')]
    mn = int(sys.argv[sys.argv.index('--min-runs') + 1]) if '--min-runs' in sys.argv else 30
    if '--min-runs' in sys.argv: args.remove(str(mn))
    a, b = ([float(l) for l in open(p) if l.strip()] for p in args[:2])
    for name, x in (('A', a), ('B', b)):
        print(f'{name}: n={len(x)} median={stats.scoreatpercentile(x, 50):.4g} mean={sum(x) / len(x):.4g}')
    t, df, p, A = rank_welch(a, b)
    print(f'rank Welch: t={t:.3f} dof={df:.1f} p={p:.4g}; P(A run > B run)={A:.3f}')
    if min(len(a), len(b)) < mn:
        print(f'fewer than {mn} runs on one side: an anecdote, not a result', file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
