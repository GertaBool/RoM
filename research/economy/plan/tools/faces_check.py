"""R41.1 (M87): the two face proposals, computed for worked cases.

Proposal 1: the unhealthy faces "from population" count the dense population D (people not working plots) through the
            inverse size curve: F_dense = size_of(D), 0 below 1,000 people (today: F = size, CvCity::unhealthyPopulation).
Proposal 2: sanitation faces (the iHealth of buildings tagged sanitation in CIV4BuildingInfos.xml, plus fresh water,
            CvCity::getFreshWaterGoodHealth) are set first against the density faces:
              uncovered = max(0, F_dense - F_sanitation)
              U         = (D / N) x uncovered / F_dense          the unsanitized share (0 if F_dense = 0)
              urban penalty in the health burden = 13 x U per 1,000 a year (pop_model_math.md section 3)
            Sanitation faces beyond the density faces join the other healthy faces. The other faces (resources, forests,
            hospitals and medicine, pollution, flood plains) give H = good / (good + bad) for the base burden.
The display keeps all faces: good = all healthy faces, bad = density faces + other unhealthy faces; the city is shown
unhealthy (billboard symbol, diseased smoke, alerts) when bad > good, as today.
usage: faces_check.py
"""
TABLE = [0] + [int(s ** 2.8) * 1000 for s in range(1, 101)]


def size_of(n):
    if n < 1000:
        return 0
    s = 1
    while TABLE[s + 1] <= n:
        s += 1
    return s


# health of the buildings proposed as sanitation (iHealth, economy branch CIV4BuildingInfos.xml) and fresh water (BTS: 2)
SAN = {'fresh water': 2, 'Town Essentials': 3, 'City Essentials': 6, 'Metropolitan Essentials': 12, 'Aqueduct': 5,
       'Bath House': 3, 'Water Treatment Plant': 2, 'Recycling Center': 3}

CASES = [  # name, people, share working plots, sanitation present, other good faces, other bad faces
    ('farming district, no works', 1000000, 0.80, [], 4, 1),
    ('farming district, fresh water, Town Essentials', 1000000, 0.80, ['fresh water', 'Town Essentials'], 4, 1),
    ('trade city, no works', 1000000, 0.20, [], 4, 1),
    ('trade city, fresh water, Aqueduct', 1000000, 0.20, ['fresh water', 'Aqueduct'], 4, 1),
    ('trade city, + City Essentials, Bath House', 1000000, 0.20, ['fresh water', 'Aqueduct', 'City Essentials', 'Bath House'], 4, 1),
    ('ancient town, 50,000, fresh water', 50000, 0.20, ['fresh water'], 2, 0),
    ('city of 500,000, no works', 500000, 0.10, [], 3, 1),
    ('metropolis of 10 million, no works', 10000000, 0.10, [], 3, 1),
    ('metropolis of 10 million, full works', 10000000, 0.05,
     ['fresh water', 'Metropolitan Essentials', 'Aqueduct', 'Bath House', 'Water Treatment Plant', 'Recycling Center'], 8, 6),
]


def main():
    print('| Case | People | Dense people | Faces today (size) | Density faces | Sanitation faces | Uncovered | U | Urban penalty per 1,000 | H (other faces) | Shown: good / bad |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    for name, n, farm, san, og, ob in CASES:
        d = int(n * (1 - farm))
        fd = size_of(d)
        fs = sum(SAN[x] for x in san)
        unc = max(0, fd - fs)
        u = (d / n) * unc / fd if fd else 0.0
        spill = max(0, fs - fd)
        h = (og + spill) / float(og + spill + ob) if (og + spill + ob) else 1.0
        good, bad = og + fs, ob + fd
        print('| %s | %s | %s | %d | %d | %d | %d | %.2f | %.1f | %.2f | %d / %d%s |' % (
            name, format(n, ','), format(d, ','), size_of(n), fd, fs, unc, u, 13 * u, h, good, bad,
            ' (unhealthy)' if bad > good else ''))


if __name__ == '__main__':
    main()
