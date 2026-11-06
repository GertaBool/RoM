"""R30.1 (D30): the population growth model in integer yearly steps, run on edge cases.

Model (research/economy/pop_model_math.md explains each part and its sources):
  x  = satiety per head / need                     food sufficiency (1.0 = exactly fed)
  Q  = drive from food:  x >= 1: min(1, (x - 1) / A)        surplus raises growth up to the ceiling
                         x <  1: (x - 1) * K_FAMINE / N_MAX  shortfall turns growth negative (scaled below)
  multipliers on positive growth (each in [0, 1]): health h, nutrient coverage c, economy e, safety w
  penalties (per year, subtracted): urban penalty U x density share unsanitized, war P_WAR x war pressure,
                                    bad health P_HEALTH x (1 - h)
  n  = N_MAX x Q x h x c x e x w - penalties      (when Q < 0 the shortfall term is used without the multipliers)
  N' = N + N n, in integers with the remainder carried, capped at food / biological minimum (starvation)
Every parameter is listed in PARAMS with its source or 'estimate'. Python ints stand for the C++ __int64.
usage: pop_model_sim.py [case]   (no argument: all cases)"""
import sys

PARAMS = {
    'N_MAX': (30, 'per mille a year: max natural increase; birth rates up to 50-60 per 1,000 (Clark), deaths about 20-25 in good years; Hutterite TFR 10.9 (Coale)'),
    'A': (300, 'per mille: food surplus at which growth reaches N_MAX (estimate; calibrate on England 1086-1300, 0.4-0.5 % a year)'),
    'K_FAMINE': (200, 'per mille a year per unit shortfall: x = 0.7 for two years loses about 12 % (Great Famine 1315-17: 10-15 %)'),
    'S_MIN_SHARE': (577, 'per mille of need: biological minimum 1,500 of 2,600 (Clark; open_questions.md section 7)'),
    'U': (13, 'per mille a year: urban penalty of a large city without sanitation (London about 1700 needed about 8,000 migrants a year; about 1 % of its people, population figure to source)'),
    'P_WAR': (25, 'per mille a year at full war pressure (Thirty Years War: 15-20 % over 30 years on average, over 50 % in the worst regions, mostly by plunder, famine and plague)'),
    'P_HEALTH': (10, 'per mille a year at no health (estimate; clean water about 43-50 % of the US urban mortality decline 1900-1936, Cutler and Miller)'),
}
P = {k: v[0] for k, v in PARAMS.items()}


def step(N, rem, food, need, h=1000, c=1000, e=1000, w=1000, dens_unsan=0, war=0):
    """One year. Parameters and multipliers in per mille; the rate n and food sufficiency x in parts per million,
    so that growth does not stall short of the food limit through rounding. Returns (N, remainder)."""
    if N <= 0:
        return 0, 0
    x = food * 1000000 // (need * N)                           # ppm; food x 10^6 < 2^63 for food < 9 x 10^12
    if x >= 1000000:
        q = min(1000000, (x - 1000000) * 1000 // P['A'])       # ppm
        n = P['N_MAX'] * q // 1000 * h // 1000 * c // 1000 * e // 1000 * w // 1000   # ppm
    else:
        n = (x - 1000000) * P['K_FAMINE'] // 1000              # ppm, negative
    n -= (P['U'] * dens_unsan + P['P_WAR'] * war + P['P_HEALTH'] * (1000 - h))      # per mille x per mille = ppm
    total = N * n + rem                                        # people x ppm, __int64 in C++
    dN, rem = divmod(total, 1000000) if total >= 0 else (-((-total) // 1000000), -((-total) % 1000000))
    N = N + dN
    cap = food * 1000 // (need * P['S_MIN_SHARE'])             # starvation: beyond food / minimum cannot live
    if N > cap:
        N, rem = cap, 0
    return max(N, 0), rem


def run(name, years, N, food_fn, **kw_fn):
    rem, rows = 0, []
    for y in range(1, years + 1):
        kw = {k: f(y) if callable(f) else f for k, f in kw_fn.items()}
        N, rem = step(N, rem, food_fn(y), 2600, **kw)
        rows.append((y, N))
    return rows


def show(title, rows, every):
    print('\n' + title)
    print('  ' + '  '.join('y%d %s' % (y, format(n, ',')) for y, n in rows if y % every == 0 or y == rows[-1][0]))


CASES = {
    'small_city': lambda: show('1. A town of 1,000 with land for 50,000 (food fixed): growth, then the food limit',
                               run('', 400, 1000, lambda y: 50000 * 2600), 50),
    'rounding': lambda: show('2. A hamlet of 10 people, 1 % growth: the carried remainder keeps it from stalling',
                             run('', 100, 10, lambda y: 20 * 2600 * 2), 20),
    'famine': lambda: show('3. Famine: 100,000 fed, then two harvests at 70 % (years 11-12), then normal again',
                           run('', 30, 100000, lambda y: (70 if y in (11, 12) else 100) * 1000 * 2600), 1),
    'blockade': lambda: show('4. A city of 1 million fed half by imports; imports cut in year 6 (blockade): starvation cap and shrinking',
                             run('', 20, 1000000, lambda y: (500000 if y >= 6 else 1000000) * 2600), 1),
    'urban_penalty': lambda: show('5. A city of 500,000, food just enough, no sanitation (all urban): it shrinks without migrants',
                                  run('', 50, 500000, lambda y: 500000 * 2600, dens_unsan=1000), 10),
    'sanitation': lambda: show('6. The same city with sanitation from year 26: the decline stops',
                               run('', 50, 500000, lambda y: 500000 * 2600, dens_unsan=lambda y: 1000 if y <= 25 else 0), 5),
    'war': lambda: show('7. A region of 1 million under full war pressure for 30 years, food unchanged (the penalty alone)',
                        run('', 30, 1000000, lambda y: 1100000 * 2600, war=1000), 5),
    'war_pillage': lambda: show('7b. The same with pillage: a third of the food lost while the war lasts (years 1-30), then peace',
                        run('', 60, 1000000, lambda y: (733000 if y <= 30 else 1100000) * 2600, war=lambda y: 1000 if y <= 30 else 0), 5),
    'surplus_cap': lambda: show('8. Huge surplus (food for 10x the people): growth stays at the 3 % ceiling, no explosion',
                                run('', 50, 100000, lambda y: 1000000 * 2600), 10),
    'bad_health': lambda: show('9. Fed, but health half: growth slowed by the multiplier and turned negative by the penalty',
                               run('', 30, 100000, lambda y: 100000 * 2600, h=500), 5),
    'long_turn': lambda: show('10. A 50-year turn is 50 yearly steps: the same path as case 1, no overshoot',
                              run('', 50, 1000, lambda y: 50000 * 2600), 10),
    'zero_food': lambda: show('11. All food lost: the starvation cap empties the city in one year (the engine keeps size 1 as now)',
                              run('', 3, 10000, lambda y: 0 if y >= 2 else 10000 * 2600), 1),
}


if __name__ == '__main__':
    for k, (v, src) in PARAMS.items():
        print('%-11s %5d  %s' % (k, v, src))
    for name in (sys.argv[1:] or CASES):
        CASES[name]()
