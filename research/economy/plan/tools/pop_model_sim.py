"""R33.3 (D30, fourth version): the evidence-based second version, with the mortality side as a health burden (M75, M79).

The growth rate is fertility minus the health burden: health weighed from its causes lowers the rate or turns it
negative (M75); there is no separate death term. The burden is measured per 1,000 people a year, so the historical
death-rate evidence calibrates it.

research/economy/pop_model_math.md explains each part and its sources. All rates are per 1,000 people a year
(per mille) unless named otherwise; inputs between 0 and 1 are given in per mille (1000 = 1.0).

  x   food sufficiency: satiety per head / need (per mille)
  BIRTHS b = B(x) x f_nutrients x f_economy x f_urban x f_religion x f_education x f_safety
         B(x): 30 at x = 0.9, rising to 45 at x = 1.3 (earlier marriage when prosperous); below 0.9 it falls to 0
               at the biological minimum (the Hunger Winter: conceptions fell below a calorie threshold, dose-response)
  HEALTH BURDEN h = D_med x (2 - h)                         base mortality by medicine, doubled at the worst health
           + D_NUT x clamp((1.3 - x) / 0.4)           weakness and disease of the underfed (0 at x >= 1.3)
           + K_FAMINE x (1 - x) when x < 1            famine
           + D_DEF x (1 - c)                          deficiency diseases (scurvy, beriberi, pellagra, iodine)
           + U x unsanitized urban share              the urban penalty (infant deaths in towns)
           + P_WAR x war pressure
  g = b - h (per 1,000 a year); N' = N + N g / 1000 (+ migration, not here), capped at food / minimum (starvation)
Python ints stand for the C++ __int64; rates are carried in parts per million with remainders.
usage: pop_model_sim.py [case ...]"""
import sys

PARAMS = {
    'B_LOW': (30, 'births per 1,000 at x = 0.9 (pre-industrial England below 30 at times, Clark)'),
    'B_HIGH': (45, 'births per 1,000 at x >= 1.3 (birth rates up to 50-60 observed, Clark; Hutterite TFR 10.9)'),
    'D_PRE': (22, 'health burden per 1,000 (calibrated on crude death rates) in good health before modern medicine (life expectancy = 1 / death rate: 33 per 1,000 is 30 years, Clark)'),
    'D_MOD': (8, 'health burden per 1,000 with modern medicine and sanitation (estimate, to source)'),
    'D_NUT': (12, 'burden per 1,000 from weakness of the underfed between x = 1.3 and 0.9 (estimate: sets b = d near x = 1)'),
    'K_FAMINE': (200, 'burden per 1,000 per unit shortfall below x = 1 (Great Famine 1315-17: 10-15 %)'),
    'D_DEF': (15, 'burden per 1,000 at no nutrient coverage (estimate; beriberi struck 30 % of the Japanese navy a year; 27,000 deaths in 211,600 cases in 1904-05)'),
    'U': (13, 'burden per 1,000 in fully unsanitized dense quarters (London infant mortality 300-400 per 1,000 births against 180 nationally, mid-1700s; London needed about 8,000 migrants a year about 1700)'),
    'P_WAR': (25, 'burden per 1,000 at full war pressure (Thirty Years War, with plunder and plague)'),
    'MIN_SHARE': (577, 'biological minimum as per mille of need (1,500 of 2,600, Clark)'),
}
P = {k: v[0] for k, v in PARAMS.items()}


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def births(x, nutr=1000, econ=1000, urban=0, relig=1000, educ=0, safety=1000):
    """per million (ppm of people a year)"""
    if x >= 900:
        base = P['B_LOW'] * 1000 + (P['B_HIGH'] - P['B_LOW']) * 1000 * min(x - 900, 400) // 400
    else:
        base = P['B_LOW'] * 1000 * max(0, x - P['MIN_SHARE']) // (900 - P['MIN_SHARE'])
    f = base
    f = f * (800 + 200 * nutr // 1000) // 1000          # nutrient gaps lower fertility a little (estimate)
    f = f * econ // 1000                                  # economy acts through marriage (Wrigley and Schofield; Rostock)
    f = f * (1000 - 200 * urban // 1000) // 1000          # towns: fewer married, later (Rostock; Prussia after 1875)
    f = f * relig // 1000                                 # religiosity: more children (Europe surveys), 900-1100
    f = f * (1000 - 650 * educ // 1000) // 1000           # education and contraception: the transition (to source)
    f = f * safety // 1000
    return f


def health_burden(x, health=1000, medicine=0, nutr=1000, unsan=0, war=0):
    """per million"""
    d_base = (P['D_PRE'] * 1000 - (P['D_PRE'] - P['D_MOD']) * medicine) * (2000 - health) // 1000
    d = d_base
    d += P['D_NUT'] * 1000 * clamp(1300 - x, 0, 400) // 400
    if x < 1000:
        d += P['K_FAMINE'] * (1000 - x)
    d += P['D_DEF'] * (1000 - nutr)
    d += P['U'] * unsan + P['P_WAR'] * war
    return d


def step(N, rem, food, need=2600, months=12, **kw):
    if N <= 0:
        return 0, 0, 0, 0
    x = food * 1000 // (need * N)
    bk = {k: kw[k] for k in ('nutr', 'econ', 'urban', 'relig', 'educ', 'safety') if k in kw}
    dk = {k: kw[k] for k in ('health', 'medicine', 'nutr', 'unsan', 'war') if k in kw}
    b, d = births(x, **bk), health_burden(x, **dk)
    total = N * (b - d) * months // 12 + rem              # people x ppm; a turn of under a year takes its share
    dN, rem = divmod(total, 1000000) if total >= 0 else (-((-total) // 1000000), -((-total) % 1000000))
    N += dN
    cap = food * 1000 // (need * P['MIN_SHARE'])
    if N > cap:
        N, rem = cap, 0
    return max(N, 0), rem, b, d


def run(years, N, food, **kw):
    rem, rows = 0, []
    for y in range(1, years + 1):
        f = food(y) if callable(food) else food
        args = {k: (v(y) if callable(v) else v) for k, v in kw.items()}
        N, rem, b, d = step(N, rem, f, **args)
        rows.append((y, N, b, d))
    return rows


def show(title, rows, every):
    print('\n' + title)
    for y, n, b, d in rows:
        if y % every == 0 or y == rows[-1][0]:
            print('  year %4d  people %12s  fertility %5.1f  health burden %5.1f  growth %+5.1f per 1,000' % (y, format(n, ','), b / 1000, d / 1000, (b - d) / 1000))


# R38.10 (M84): yearly steps inside a turn, from the game speed's turn increments (CIV4GameSpeedInfo.xml,
# GameTurnInfos: iMonthIncrement for iTurnsPerIncrement turns; START_YEAR -6000). A turn of 600 months runs 50 yearly
# steps; a turn of 6 months runs one half step.
SPEEDS = {
    'NORMAL': [(600, 40), (300, 100), (240, 120), (120, 50), (60, 80), (24, 80), (12, 60), (6, 150), (3, 20)],
    'MARATHON': [(300, 160), (180, 100), (120, 100), (60, 180), (24, 201), (12, 129), (6, 180), (3, 264), (1, 156)],
    'BLITZ': [(2400, 10), (1200, 40), (600, 20), (300, 10), (240, 10), (120, 30), (60, 30), (36, 30), (24, 25), (12, 10)],
}


def run_turns(speed, N, food_by_year, kw_by_year, report_years, start_month=-6000 * 12):
    """Runs the model turn by turn: each turn runs one step per whole year it spans and one part step for the rest.
    food_by_year and kw_by_year take the calendar year. Returns {year: (turn, N)} at the first turn end at or past
    each report year, and the number of steps run."""
    month, rem, turn, steps, out = start_month, 0, 0, 0, {}
    todo = sorted(report_years)
    for inc, n in SPEEDS[speed]:
        for _ in range(n):
            left = inc
            while left > 0:
                m = min(12, left)
                y = month // 12
                N, rem, b, d = step(N, rem, food_by_year(y), months=m, **kw_by_year(y))
                month += m
                left -= m
                steps += 1
            turn += 1
            while todo and month // 12 >= todo[0]:
                out[todo.pop(0)] = (turn, month // 12, N)
    return out, steps, turn


def turns_demo():
    """One city under three game speeds with the same history by calendar year: its people match at the same years."""
    def food(y):                          # food in satiety units a year: slow growth, faster after 1700, faster after 1900
        base = 2000.0 * 1.0006 ** (y + 6000)
        if y > 1700:
            base *= 1.012 ** (y - 1700)
        if y > 1900:
            base *= 1.01 ** (y - 1900)
        return int(base) * K

    def kw(y):
        return {'medicine': 0 if y < 1880 else min(1000, (y - 1880) * 12), 'educ': 0 if y < 1920 else min(1000, (y - 1920) * 15)}
    years = [-4000, -2000, 0, 1000, 1500, 1800, 1900, 1950, 2000, 2050]
    print('\nYearly steps inside turns (R38.10): one city, the same history by calendar year, three game speeds')
    res = {}
    for sp in SPEEDS:
        out, steps, turns = run_turns(sp, 1000, food, kw, years)
        res[sp] = out
        print('  %-9s %4d turns, %5d steps in all' % (sp, turns, steps))
    print('  %6s ' % 'year' + ''.join('%28s' % sp for sp in SPEEDS))
    for y in years:
        print('  %6d ' % y + ''.join('%28s' % ('turn %d (yr %d): %s' % (res[sp][y][0], res[sp][y][1], format(res[sp][y][2], ','))
                                               if y in res[sp] else '-') for sp in SPEEDS))


K = 2600
CASES = {
    'equilibrium': lambda: show('1. Pre-industrial city at its food limit (x = 1): fertility and health burden balance near 33 per 1,000',
                                run(30, 100000, 100000 * K), 10),
    'frontier': lambda: show('2. A town of 1,000 with food for 50,000: growth near 2.3 % a year, then the food limit',
                             run(300, 1000, 50000 * K), 50),
    'famine': lambda: show('3. Famine: harvests at 70 % in years 11-12',
                           run(20, 100000, lambda y: (70000 if y in (11, 12) else 100000) * K), 1),
    'urban': lambda: show('4. A city of 500,000 at its food limit, all in unsanitized dense quarters, no migrants',
                          run(40, 500000, 500000 * K, urban=1000, unsan=1000), 10),
    'transition': lambda: show('5. Demographic transition: medicine and sanitation from year 21 (health burden falls), education from year 61 (fertility falls); food grows 2 % a year',
                               run(140, 1000000, lambda y: int(1050000 * 1.02 ** y) * K,
                                   medicine=lambda y: 0 if y <= 20 else min(1000, (y - 20) * 25),
                                   educ=lambda y: 0 if y <= 60 else min(1000, (y - 60) * 20)), 10),
    'beriberi': lambda: show('6. A rice city fed on polished rice: thiamine missing (nutrient coverage 60 %), then barley and meat from year 16',
                             run(30, 200000, 210000 * K, nutr=lambda y: 600 if y <= 15 else 1000), 5),
    'war_pillage': lambda: show('7. War for 30 years with a third of the food pillaged, then peace',
                                run(60, 1000000, lambda y: (733000 if y <= 30 else 1100000) * K, war=lambda y: 1000 if y <= 30 else 0, safety=lambda y: 800 if y <= 30 else 1000), 5),
    'blockade': lambda: show('8. A city of 1 million fed half by imports; imports cut in year 6',
                             run(15, 1000000, lambda y: (500000 if y >= 6 else 1000000) * K), 1),
    'hamlet': lambda: show('9. A hamlet of 10 with food for 40: remainders carried',
                           run(150, 10, 40 * K), 25),
    'bad_health': lambda: show('10. Fed, health balance at half (bad water, no aqueduct)',
                               run(30, 100000, 100000 * K, health=500), 10),
    'religion': lambda: show('11. Two cities with food 20 % above need: religious (fertility x 1.1) and secular with schooling (x 0.9, education 0.5)',
                             run(30, 100000, 120000 * K, relig=1100), 10) or show('    secular',
                             run(30, 100000, 120000 * K, relig=900, educ=500), 10),
    'turns': turns_demo,
    'zero_food': lambda: show('12. All food lost from year 2', run(3, 10000, lambda y: 0 if y >= 2 else 10000 * K), 1),
}

if __name__ == '__main__':
    for k, (v, s) in PARAMS.items():
        print('%-10s %5d  %s' % (k, v, s))
    for name in (sys.argv[1:] or CASES):
        CASES[name]()
