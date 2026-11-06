"""R32.2 (D30, third version): one growth rate, no death term (M75), in integer yearly steps, on edge cases.

As the user asked (M75): health is weighed from several factors by itself, and it lowers the growth rate or turns
it negative; starvation stays the engine's own floor. research/economy/pop_model_math.md explains each part.

  x  food sufficiency = satiety per head / need                                  (per mille; 1000 = exactly fed)
  F  food drive:  x >= 1: min(1, (x - 1) / A)            surplus raises growth to the ceiling
                  x <  1: -K x (1 - x)                   shortfall turns it negative
  Phi fertility culture = economy x town life x norms x education x safety       (per mille each, 1000 neutral)
  H  health, weighed from its factors (per mille, 1000 = perfect):
       H = 1000 - sum of weighted shortfalls: water, sanitation in dense quarters, nutrient coverage, dietary
           harms, medicine; war and pillage enter through food, safety and health (displaced, sick)
  g  = G_MAX x [ F x Phi x H  -  KAPPA x (1000 - H) ]       growth slowed by poor health, negative when it is bad
  N' = N + N g, capped at food / biological minimum (the engine's starvation)
Python ints stand for the C++ __int64; rates in parts per million with carried remainders.
usage: pop_model_sim.py [case ...]"""
import sys

PARAMS = {
    'G_MAX': (30, 'per mille a year: the most a population grows (birth rates up to 50-60 per 1,000 against deaths near 20-25 in good years, Clark; Hutterite TFR 10.9)'),
    'A': (300, 'per mille: the food surplus that gives the full rate (estimate; England 1086-1300 grew 0.4-0.5 % a year)'),
    'K': (6700, 'per mille of G_MAX per unit shortfall: x = 0.7 gives -6 % a year, two such years about -12 % (Great Famine 1315-17: 10-15 %)'),
    'KAPPA': (1700, 'per mille of G_MAX per unit of lost health: dense quarters without sewers (health 0.75) give about -1.3 % a year (London needed about 8,000 migrants a year about 1700); the worst health about -5 % a year'),
    'B': (500, 'ppm of need per per mille of lost fertility culture: culture 0.6 settles the city 20 % above need (estimate; the demographic transition: Clark on the birth schedule)'),
    'MIN': (577, 'biological minimum as per mille of need: 1,500 of 2,600 (Clark)'),
}
HEALTH_WEIGHTS = {   # how much each factor can take from health (per mille of 1000); estimates to calibrate
    'water': 250,       # supply and quality (D31): clean water about 43-50 % of the US urban mortality decline 1900-1936
    'sanitation': 250,  # dense quarters without sewers: London infant mortality 300-400 against 180 per 1,000 births
    'nutrients': 200,   # coverage of nutrient groups: scurvy, beriberi, pellagra, iodine deficiency
    'harms': 100,       # processed and salted meat, sugar, grain-only diets (round_m75.md section 2)
    'medicine': 200,    # medicine techs and hospitals: the fall of death rates from the late 1700s
}
P = {k: v[0] for k, v in PARAMS.items()}


def health(water=1000, sanitation=1000, nutrients=1000, harms=0, medicine=1000):
    """Each input in per mille of perfect (harms: per mille of the worst)."""
    w = HEALTH_WEIGHTS
    short = (w['water'] * (1000 - water) + w['sanitation'] * (1000 - sanitation) + w['nutrients'] * (1000 - nutrients)
             + w['harms'] * harms + w['medicine'] * (1000 - medicine)) // 1000
    return max(0, 1000 - short)


def step(N, rem, food, need=2600, phi=1000, H=1000):
    if N <= 0:
        return 0, 0, 0
    x = food * 1000000 // (need * N)                                   # ppm
    # the food level at which growth stops rises as fertility culture falls (Clark: a lower birth schedule settles
    # the population at a higher income); a high-fertility culture does not push it below exactly fed
    target = 1000000 + P['B'] * max(0, 1000 - phi)                       # ppm of need
    if x >= 1000000:
        F = min(1000000, (x - target) * 1000 // P['A']) if x >= target else (x - target) * 1000 // P['A']
    else:
        F = -(P['K'] * (1000000 - x) // 1000)                          # ppm, negative
    if F >= 0:
        drive = F * min(phi, 1100) // 1000 * H // 1000
    else:
        drive = F                                                      # a famine is not softened by culture
    g = P['G_MAX'] * (drive - P['KAPPA'] * (1000 - H)) // 1000          # ppm of people a year
    total = N * g + rem
    dN, rem = divmod(total, 1000000) if total >= 0 else (-((-total) // 1000000), -((-total) % 1000000))
    N += dN
    cap = food * 1000 // (need * P['MIN'])
    if N > cap:
        N, rem = cap, 0
    return max(N, 0), rem, g


def run(years, N, food, phi=1000, H=1000):
    rem, rows = 0, []
    for y in range(1, years + 1):
        f = food(y) if callable(food) else food
        p = phi(y) if callable(phi) else phi
        h = H(y) if callable(H) else H
        N, rem, g = step(N, rem, f, phi=p, H=h)
        rows.append((y, N, g))
    return rows


def show(title, rows, every):
    print('\n' + title)
    print('  ' + '  '.join('y%d %s (%+.1f%%)' % (y, format(n, ','), g / 10000) for y, n, g in rows
                           if y % every == 0 or y == rows[-1][0]))


K2 = 2600
UNSAN = health(sanitation=0)                  # dense quarters with no sewers or clean water supply
BAD_WATER = health(water=300, sanitation=500)
CASES = {
    'balance': lambda: show('1. A city at its food limit, healthy: no growth, no decline', run(30, 100000, 100000 * K2), 10),
    'frontier': lambda: show('2. A town of 1,000 with food for 50,000: up to 3 % a year, then the limit', run(300, 1000, 50000 * K2), 50),
    'famine': lambda: show('3. Harvests at 70 % in years 11-12', run(20, 100000, lambda y: (70000 if y in (11, 12) else 100000) * K2), 2),
    'urban': lambda: show('4. 500,000 in dense quarters without sewers (health %d), no migrants' % UNSAN,
                          run(40, 500000, 500000 * K2, H=UNSAN), 10),
    'sanitation': lambda: show('5. The same, sewers and clean water from year 21', run(40, 500000, 500000 * K2, H=lambda y: UNSAN if y <= 20 else 1000), 5),
    'transition': lambda: show('6. Medicine raises health from year 21; education and town life lower fertility culture from year 61; food grows 2 % a year',
                               run(140, 1000000, lambda y: int(1050000 * 1.02 ** y) * K2,
                                   H=lambda y: health(medicine=300 if y <= 20 else min(1000, 300 + (y - 20) * 20)),
                                   phi=lambda y: 1000 if y <= 60 else max(350, 1000 - (y - 60) * 15)), 20),
    'beriberi': lambda: show('7. Polished rice: nutrient coverage 60 % until year 15', run(30, 200000, 210000 * K2, H=lambda y: health(nutrients=600) if y <= 15 else 1000), 5),
    'war': lambda: show('8. War for 30 years: a third of the food pillaged, fear (fertility culture 0.8), sickness (health 0.8), then peace',
                        run(60, 1000000, lambda y: (733000 if y <= 30 else 1100000) * K2, phi=lambda y: 800 if y <= 30 else 1000,
                            H=lambda y: 800 if y <= 30 else 1000), 10),
    'blockade': lambda: show('9. 1 million, half its food imported, imports cut in year 6', run(15, 1000000, lambda y: (500000 if y >= 6 else 1000000) * K2), 3),
    'hamlet': lambda: show('10. A hamlet of 10 with food for 40', run(150, 10, 40 * K2), 25),
    'bad_water': lambda: show('11. Fed, bad water and half sanitation (health %d)' % BAD_WATER, run(30, 100000, 110000 * K2, H=BAD_WATER), 10),
    'norms': lambda: show('12. Food 20 % above need: high-fertility culture (1.1) against prudish and schooled (0.6)',
                          run(40, 100000, 120000 * K2, phi=1100), 10) or show('    low-fertility culture', run(40, 100000, 120000 * K2, phi=600), 10),
    'zero_food': lambda: show('13. All food lost from year 2', run(3, 10000, lambda y: 0 if y >= 2 else 10000 * K2), 1),
}

if __name__ == '__main__':
    for k, (v, s) in PARAMS.items():
        print('%-6s %5d  %s' % (k, v, s))
    print('health weights:', HEALTH_WEIGHTS)
    for name in (sys.argv[1:] or CASES):
        CASES[name]()
