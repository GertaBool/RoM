"""R38.6 (M84): why city size = the inverse of today's curve works, computed.

Today the engine shows people = int(size^2.8) x 1000 (CvCity::getRealPopulation). The proposal turns it round:
people are counted (D30), and size is the largest s with int(s^2.8) x 1000 <= people, read from a table of 64-bit
integers (no floating point at run time). This prints:
  1. the table and the sizes of real cities (population_model.md section 3);
  2. the density of the people who work the land over the plots a city works (the engine works min(size, 20) plots
     besides the city's own), on three maps, against the historical densities;
  3. the same with labour units (size = land workers / workers one plot takes), for comparison.
usage: size_curve_check.py
"""
NUM_WORKABLE = 20             # the 21-plot fat cross less the city plot (CvDefines.h NUM_CITY_PLOTS 21)
MAPS = {'Huge Europe': 1770, 'Mediterranean Standard': 4470, 'RFC Earth': 46000}   # km2 per plot, map_scale.json

TABLE = [0] + [int(s ** 2.8) * 1000 for s in range(1, 101)]   # built once (load time); runtime uses integers only


def size_of(people):
    s = 1
    while s + 1 < len(TABLE) and TABLE[s + 1] <= people:
        s += 1
    return s


def bar(people):
    """the food box (decided, M84): progress in people from this size to the next, in per mille"""
    s = size_of(people)
    lo, hi = TABLE[s], TABLE[s + 1]
    return max(0, min(1000, (people - lo) * 1000 // (hi - lo)))


CITIES = [('Uruk, 3000 BC', 40000, 45000), ('largest, 2000 BC', 40000, 65000), ('Babylon, 500 BC', 150000, 200000),
          ('Paris, 1328', 200000, 200000), ('Rome, 1 AD', 800000, 1000000), ('London, 1801', 1010000, 1010000),
          ('London, 1851', 2290000, 2290000), ('London, 1901', 6230000, 6230000), ('New York, 1950', 12500000, 12500000),
          ('Tokyo, 2000', 26400000, 26400000), ('Jakarta, 2025', 41900000, 41900000)]


def main():
    print('1. Sizes from people (the inverse of int(size^2.8) x 1000)')
    print('| City | People | Size | Food box (per mille) |')
    print('|---|---|---|---|')
    for name, lo, hi in CITIES:
        sz = '%d' % size_of(lo) if size_of(lo) == size_of(hi) else '%d-%d' % (size_of(lo), size_of(hi))
        print('| %s | %s | %s | %s |' % (name, format(lo, ',') if lo == hi else '%s-%s' % (format(lo, ','), format(hi, ',')),
                                        sz, bar(lo)))

    print('\n2. People working the land per km2 of the plots the city works (inverse curve)')
    print('| People | Size | Plots worked | Farm share | ' + ' | '.join(MAPS) + ' |')
    print('|---|---|---|---|' + '---|' * len(MAPS))
    for people, share in [(1000, 80), (10000, 80), (50000, 80), (200000, 80), (1000000, 80), (1000000, 40),
                          (4500000, 80), (4500000, 40), (10000000, 5)]:
        s = size_of(people)
        plots = min(s, NUM_WORKABLE)
        dens = ['%.1f' % (people * share / 100 / (plots * a)) for a in MAPS.values()]
        print('| %s | %d | %d | %d %% | %s |' % (format(people, ','), s, plots, share, ' | '.join(dens)))

    print('\n3. Labour units for comparison: size = land workers / workers one plot takes')
    print('   (one plot takes area x farmland share / ha per worker; farmland share 30 %, an estimate)')
    print('| People (80 % on the land) | Tools: ha per worker | ' + ' | '.join(MAPS) + ' |')
    print('|---|---|' + '---|' * len(MAPS))
    for people in (10000, 200000, 1000000, 4500000):
        for tool, ha in (('hand tools', 3), ('horse machinery', 30), ('tractor', 100)):
            cells = []
            for a in MAPS.values():
                per_plot = a * 100 * 30 // 100 // ha          # workers one plot takes (100 ha per km2)
                cells.append('%.2f' % (people * 0.8 / per_plot))
            print('| %s | %s (%d) | %s |' % (format(people, ','), tool, ha, ' | '.join(cells)))


if __name__ == '__main__':
    main()
