"""The rank-based Welch test without SciPy (framework.md, section 7; Luke, Essentials of
Metaheuristics, 11.1.2, after Wineberg and Christensen), so the gate runs on python3 alone.

Pool the two samples and rank them (ties get their mean rank), then Welch's t-test on the ranks:
t = (mean rank a - mean rank b) / sqrt(var a / na + var b / nb), with the Welch-Satterthwaite
degrees of freedom; the two-sided p is I_x(df/2, 1/2), x = df / (df + t^2), the regularized
incomplete beta function (continued fraction, modified Lentz; Numerical Recipes, section 6.4).
Effect size: Vargha-Delaney A, the chance that a run of a beats a run of b, from the same ranks.
Two samples without variance give no p (nan), as scipy.stats.ttest_ind does.
"""
import math


def ranks(x):
    order = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def _betacf(a, b, x):
    tiny, eps = 1e-300, 3e-16
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 10000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c; c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c; c = c if abs(c) > tiny else tiny
        de = d * c
        h *= de
        if abs(de - 1) < eps:
            break
    return h


def betai(a, b, x):
    """The regularized incomplete beta function I_x(a, b)."""
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * _betacf(a, b, x) / a
    return 1 - math.exp(lb) * _betacf(b, a, 1 - x) / b


def rank_welch(a, b):
    """(t, df, two-sided p, A) of the rank Welch test of samples a and b."""
    r = ranks(list(a) + list(b))
    ra, rb = r[:len(a)], r[len(a):]
    na, nb = len(ra), len(rb)
    ma, mb = sum(ra) / na, sum(rb) / nb
    va = sum((v - ma) ** 2 for v in ra) / (na - 1)
    vb = sum((v - mb) ** 2 for v in rb) / (nb - 1)
    A = (sum(ra) / na - (na + 1) / 2) / nb
    se2 = va / na + vb / nb
    if se2 == 0:
        return math.nan, math.nan, math.nan, A
    t = (ma - mb) / math.sqrt(se2)
    df = se2 ** 2 / ((va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1))
    p = betai(df / 2, 0.5, df / (df + t * t))
    return t, df, p, A


def selftest():
    """Against SciPy where it is installed; known values otherwise."""
    import random
    assert ranks([3, 1, 3, 2]) == [3.5, 1.0, 3.5, 2.0]
    assert abs(betai(2, 3, 0.4) - 0.5248) < 1e-4  # I_0.4(2, 3) = 0.5248
    assert math.isnan(rank_welch([5] * 30, [5] * 30)[2])
    try:
        from scipy import stats as S
    except ImportError:
        return 'scipy absent: checked against known values only'
    rnd = random.Random(7)
    for k in range(40):
        a = [rnd.randint(0, 6) for _ in range(rnd.randint(3, 40))]
        b = [rnd.randint(0, 8) for _ in range(rnd.randint(3, 40))]
        rr = S.rankdata(a + b)
        ref = S.ttest_ind(rr[:len(a)], rr[len(a):], equal_var=False)
        t, df, p, A = rank_welch(a, b)
        if math.isnan(ref.pvalue): assert math.isnan(p); continue
        assert abs(t - ref.statistic) < 1e-9 and abs(df - ref.df) < 1e-7 and abs(p - ref.pvalue) < 1e-9, (k, p, ref.pvalue)
    return 'matches scipy'


if __name__ == '__main__':
    print('stats selftest:', selftest())
