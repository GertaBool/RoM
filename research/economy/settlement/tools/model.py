#!/usr/bin/env python3
"""Settlement economy reference model: a deterministic, integer-only simulation of goods in the cities of real
harness games. Cities and their sizes come from data/games.json (tools/games.py); the land from
data/facts_medstd.json (the map the games were played on). Quantities are integers in hundredths of a unit, as
the DLL would hold them; no floating point enters a game rule, so every run is bit-identical.

The model does not change the games: populations are taken as observed. It measures what each implementation
variant of the goods system would say about these cities: whether they could feed themselves, which needs go
unmet, what is wasted, what could be traded, and what it costs.

usage: model.py <settlement dir>
"""
import collections, hashlib, json, math, os, sys, time
import numpy as np

ROOT = sys.argv[1]
F = json.load(open(os.path.join(ROOT, 'data', 'facts_medstd.json')))
G = json.load(open(os.path.join(ROOT, 'data', 'games.json')))['games']
WD, HT = F['grid']['width'], F['grid']['height']
NP = WD * HT
OUT = {}

# ---------------- the land: yields of every plot from the XML records ----------------
TER = {t['type']: t for t in F['terrains']}
FEA = {f['type']: f for f in F['features']}
YLD = lambda v: (v + [0, 0, 0])[:3]
plot = [None] * NP
for p in F['plots']:
    plot[p['y'] * WD + p['x']] = p
river = np.zeros(NP, bool); water = np.zeros(NP, bool); hills = np.zeros(NP, bool); peak = np.zeros(NP, bool)
terrain = np.empty(NP, dtype=object); feature = np.empty(NP, dtype=object); bonus = np.empty(NP, dtype=object)
for i, p in enumerate(plot):
    terrain[i], feature[i], bonus[i] = p['terrain'], p['feature'], p['bonus']
    river[i] = p['river']; water[i] = p['plot'] == 3; hills[i] = p['plot'] == 1; peak[i] = p['plot'] == 0
XY = np.array([(i % WD, i // WD) for i in range(NP)])


def neighbours(i, r):
    x, y = i % WD, i // WD
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if abs(dx) == r and abs(dy) == r and r == 2:
                continue  # the fat cross: 21 plots
            nx, ny = x + dx, y + dy
            if 0 <= nx < WD and 0 <= ny < HT:
                yield ny * WD + nx


near_river = np.array([river[i] or any(river[j] for j in neighbours(i, 1)) for i in range(NP)])
base = np.zeros((NP, 3), int)
for i in range(NP):
    y = np.array(YLD(TER[terrain[i]]['yields']))
    if feature[i]: y = y + np.array(YLD(FEA[feature[i]]['yields']))
    if river[i]: y = y + np.array(YLD(TER[terrain[i]]['river']))
    if hills[i]: y = y + np.array([-1, 1, 0])  # CIV4YieldInfos iHillsChange
    if peak[i]: y = np.array([0, 0, 0])
    base[i] = np.maximum(y, 0)
IMP = {i['type']: i for i in F['improvements']}
farm_irr = YLD(IMP['IMPROVEMENT_FARM']['irrigated'])[0]
mine_prod = YLD(IMP['IMPROVEMENT_MINE']['yields'])[1]
cottage_com = YLD(IMP['IMPROVEMENT_COTTAGE']['yields'])[2]
flat_arable = np.array([terrain[i] in ('TERRAIN_GRASS', 'TERRAIN_PLAINS') and not hills[i] and not peak[i] and
                        feature[i] in (None, 'FEATURE_FLOOD_PLAINS') for i in range(NP)])
farmable = flat_arable & near_river  # a farm needs irrigation; fresh water from a river (assumption: no chains)
forest = np.array([feature[i] == 'FEATURE_FOREST' for i in range(NP)])
BON = {b['type']: b for b in F['bonuses']}
# the improvement a worker would build on each resource, with its bonus yields (CIV4ImprovementInfos BonusTypeStructs)
best_imp = {}
for im in F['improvements']:
    for b, y in im['bonus_yields'].items():
        y3 = YLD(y)
        if im['type'] in ('IMPROVEMENT_FARM', 'IMPROVEMENT_PASTURE', 'IMPROVEMENT_FISHING_BOATS', 'IMPROVEMENT_MINE', 'IMPROVEMENT_PLANTATION',
                          'IMPROVEMENT_WINERY', 'IMPROVEMENT_CAMP', 'IMPROVEMENT_QUARRY', 'IMPROVEMENT_OLIVE_FARM', 'IMPROVEMENT_WHALING_BOATS'):
            if b not in best_imp or sum(np.array(y3) * [3, 2, 1]) > sum(np.array(best_imp[b][1]) * [3, 2, 1]):
                best_imp[b] = (im['type'], y3)


def improve(chains, bonuses=True):
    """Plot yields with the improvements a worker would have built; chains: farms irrigate farms (Civil Service);
    bonuses: the map's resources with their improvements' bonus yields."""
    imp = base.copy()
    farm_ok = flat_arable & (near_river | chains)
    imp[farm_ok, 0] += farm_irr
    imp[hills & ~forest & ~water, 1] += mine_prod
    imp[flat_arable & ~farm_ok, 2] += cottage_com
    for i in range(NP if bonuses else 0):
        b = bonus[i]
        if b and BON[b]['cls'] not in ('BONUSCLASS_MANUFACTURED',):
            imp[i] += np.array(YLD(BON[b]['yields']))
            if b in best_imp:
                imp[i] += np.array(best_imp[b][1])
    return np.maximum(imp, 0), farm_ok


improved_early, farm_early = improve(False)
improved_late, farm_late = improve(True)
CHAIN_TURN = 60  # irrigation chains from this turn on (assumption)
improved, farmable = improved_early, farm_early
OUT['land'] = dict(plots=NP, land=int((~water).sum()), farmable=int(farmable.sum()), arable=int(flat_arable.sum()),
                   hills=int(hills.sum()), forest=int(forest.sum()), farm_irrigated_food=farm_irr, mine_prod=mine_prod)


# provinces from the map's resource plots (the conversion path of the land-quality design)
def province(names, sigma):
    g = np.zeros(NP)
    seeds = [i for i in range(NP) if bonus[i] in names]
    for s in seeds:
        d2 = ((XY - XY[s]) ** 2).sum(axis=1)
        g = np.maximum(g, np.exp(-d2 / (2 * sigma ** 2)))
    return np.round(g * 100).astype(int), len(seeds)  # grade in percent: integers from here on


GRADE = {}
for k, names, sg in [('iron', ['BONUS_IRON'], 1.5), ('copper', ['BONUS_COPPER'], 1.5), ('coal', ['BONUS_COAL'], 1.5),
                     ('wine', ['BONUS_WINE', 'BONUS_OLIVES'], 2.0), ('sheep', ['BONUS_SHEEP', 'BONUS_COW', 'BONUS_PIG'], 2.0),
                     ('fish', ['BONUS_FISH', 'BONUS_CLAM', 'BONUS_CRAB', 'BONUS_SHRIMP'], 1.5)]:
    GRADE[k], n = province(names, sg)
    OUT.setdefault('province_seeds', {})[k] = n

# ---------------- goods, needs and recipes ----------------
GOODS = ['grain', 'fish', 'dairy', 'fruit', 'wool', 'wood', 'iron', 'copper', 'coal', 'tools', 'cloth', 'wine']
GI = {g: i for i, g in enumerate(GOODS)}
NG = len(GOODS)
SPOIL = {'grain': 2, 'fish': 50, 'dairy': 20, 'fruit': 10}  # percent per turn (assumptions)
ERA_TURNS = (50, 100)  # era 0 ancient, 1 classical, 2 medieval for this 150-turn Normal game (assumption)
# needs per citizen per turn in hundredths, by era, as (category, goods that satisfy it in preference order)
NEEDS = [('staple', ['grain', 'fish'], (300, 300, 300)),   # FOOD_CONSUMPTION_PER_POPULATION = 3
         ('variety', ['dairy', 'fruit'], (20, 35, 50)),
         ('clothing', ['cloth', 'wool'], (10, 15, 20)),
         ('fuel', ['coal', 'wood'], (15, 20, 30)),
         ('tools', ['tools'], (0, 3, 6)),
         ('luxury', ['wine'], (3, 6, 10))]
NN = len(NEEDS)
W_RANK = np.array([3, 2, 1])  # the governor's ranking of plots: food 3, production 2, commerce 1 (assumption)


def tile_goods(i, food, prod, farmed):
    """Goods per turn (hundredths) from one worked plot."""
    g = np.zeros(NG, int)
    if water[i]:
        g[GI['fish']] = 100 * food + GRADE['fish'][i]
        return g
    if farmed:
        g[GI['grain']] = 100 * food
    else:
        g[GI['grain']] = 70 * food; g[GI['dairy']] = 30 * food + GRADE['sheep'][i] // 2
    if forest[i]: g[GI['wood']] = 100
    if hills[i]:
        g[GI['iron']] = GRADE['iron'][i]; g[GI['copper']] = GRADE['copper'][i]; g[GI['coal']] = GRADE['coal'][i]
    if not water[i] and not peak[i]:
        g[GI['wool']] = GRADE['sheep'][i] * 40 // 100
        g[GI['fruit']] = GRADE['wine'][i] * 60 // 100; g[GI['wine']] = GRADE['wine'][i] * 40 // 100
    return g


def tables(imp, farm):
    tg = np.array([tile_goods(i, int(imp[i][0]), int(imp[i][1]), bool(farm[i])) for i in range(NP)], np.int64)
    ctg = np.array([tile_goods(i, max(int(imp[i][0]), 3), max(int(imp[i][1]), 1), True) for i in range(NP)], np.int64)  # the city plot: iMinCity
    return tg, ctg, (imp * W_RANK).sum(axis=1)


EARLY, LATE = tables(improved_early, farm_early), tables(improved_late, farm_late)
_bare, _bare_farm = improve(False, bonuses=False)
BARE = tables(_bare, _bare_farm)  # calibration stage 1: no resources, no irrigation chains
TG, CITY_TG, RANK = EARLY


def xorshift(seed):
    x = seed & 0xFFFFFFFF or 1
    x ^= (x << 13) & 0xFFFFFFFF; x ^= x >> 17; x ^= (x << 5) & 0xFFFFFFFF
    return x & 0xFFFFFFFF


def weather(seed, turn, region):
    """Harvest factor in percent, 80 to 120, from the game seed: deterministic."""
    return 80 + xorshift(seed * 1000003 + turn * 7919 + region * 104729) % 41


def ration(avail, demand):
    """Integer proportional rationing with largest remainders, ties by index: deterministic and exact."""
    tot = int(demand.sum())
    if tot <= avail: return demand.copy()
    if tot == 0 or avail <= 0: return np.zeros_like(demand)
    give = demand * avail // tot
    rem = avail - int(give.sum())
    frac = demand * avail - give * tot
    order = np.lexsort((np.arange(len(demand)), -frac))
    give[order[:rem]] += 1
    return give


# ---------------- reconstructing the cities of a game ----------------
def cities_by_turn(game):
    ev = sorted(game['events'], key=lambda e: e['t'])
    alive = {}  # plot -> [owner, founded]
    k = 0; out = []
    for t in range(game['turns']):
        while k < len(ev) and ev[k]['t'] <= t:
            e = ev[k]; k += 1
            if e['kind'] == 'found': alive[e['plot']] = [e['owner'], e['t']]
            elif e['kind'] == 'capture' and e['plot'] in alive: alive[e['plot']][0] = e['owner']
            elif e['kind'] == 'capture': alive[e['plot']] = [e['owner'], e['t']]
            elif e['kind'] == 'razed': alive.pop(e['plot'], None)
        out.append({p: tuple(v) for p, v in alive.items()})
    return out


def sizes(game, t, cities, rule):
    """Each player's observed population split among its cities: 'equal' or 'age' (weight sqrt(age+1))."""
    res = {}
    byp = collections.defaultdict(list)
    for p, (o, f0) in cities.items(): byp[o].append((f0, p))
    for o, lst in byp.items():
        lst.sort()
        rows = game['players'].get(str(o)) or game['players'].get(o)
        P = rows[t][2] if rows and t < len(rows) else len(lst)
        P = max(P, len(lst))
        w = np.array([1000 if rule == 'equal' else int(1000 * math.sqrt(t - f0 + 1)) for f0, _ in lst], dtype=np.int64)
        # largest-remainder split of P - n extra citizens by weight, each city at least 1
        extra = P - len(lst)
        share = w * extra // int(w.sum())
        rem = extra - int(share.sum())
        frac = w * extra - share * int(w.sum())
        order = np.lexsort((np.arange(len(w)), -frac))
        share[order[:rem]] += 1
        for (f0, p), s in zip(lst, share): res[p] = 1 + int(s)
    return res


def owned_plots(cities):
    """Each plot belongs to the nearest city (fat-cross distance), ties to the older city."""
    own = {}
    for p, (o, f0) in sorted(cities.items(), key=lambda kv: (kv[1][1], kv[0])):
        for j in neighbours(p, 2):
            if j == p: continue
            d = max(abs(XY[j][0] - XY[p][0]), abs(XY[j][1] - XY[p][1]))
            if j not in own or d < own[j][1]: own[j] = (p, d)
    res = collections.defaultdict(list)
    for j, (p, d) in own.items():
        if j not in cities: res[p].append(j)
    out = {}
    for p in res:
        by_rank = sorted(res[p], key=lambda j: (-int(RANK[j]), j))
        by_food = sorted(res[p], key=lambda j: (-int(TG[j][0] + TG[j][1]), -int(RANK[j]), j))
        out[p] = (by_rank, by_food)
    return out




def city_tiles_aware(p, n, plots, needvec):
    """A governor that knows the city's needs: each slot goes to the plot that adds most, counting what it gives
    towards needs still open (staple first, twice) and then its ranked yields; greedy and deterministic."""
    if not plots: return []
    cand = list(plots[0])
    have = np.zeros(NN, np.int64)
    have[0] = CITY_TG[p][GI['grain']] + CITY_TG[p][GI['fish']]
    for ni, (cat, goods, per) in enumerate(NEEDS[1:], 1):
        have[ni] = sum(int(CITY_TG[p][GI[x]]) for x in goods) + (int(CITY_TG[p][GI['iron']]) if cat == 'tools' else 0) + \
                   (int(CITY_TG[p][GI['wool']]) if cat == 'clothing' else 0)
    chosen = []
    for _ in range(min(n, len(cand))):
        best, bj = None, None
        for j in cand:
            sc = int(RANK[j]) * 100
            gj = TG[j]
            for ni, (cat, goods, per) in enumerate(NEEDS):
                sup = sum(int(gj[GI[x]]) for x in goods) + (int(gj[GI['iron']]) if cat == 'tools' else 0)
                open_ = max(0, int(needvec[ni]) - int(have[ni]))
                sc += min(open_, sup) * (2 if ni == 0 else 1)
            if best is None or sc > best: best, bj = sc, j
        chosen.append(bj); cand.remove(bj)
        gj = TG[bj]
        for ni, (cat, goods, per) in enumerate(NEEDS):
            have[ni] += sum(int(gj[GI[x]]) for x in goods) + (int(gj[GI['iron']]) if cat == 'tools' else 0)
    return chosen


def city_tiles(p, n, plots, rank_only=False):
    """The plots a city of size n works, as the game's governor avoids starvation (CvCityAI::AI_juggleCitizens):
    the n best by rank; if they do not feed the city, the n richest in food."""
    if not plots: return []
    by_rank, by_food = plots
    t = by_rank[:n]
    food = CITY_TG[p][0] + CITY_TG[p][1] + int(TG[t][:, 0].sum() + TG[t][:, 1].sum()) if t else 0
    if food >= 300 * n or rank_only: return t
    return by_food[:n]


# ---------------- one game under one variant ----------------
def run(game, V):
    """V: dict(rule, staple ('separate'|'goods'), dist ('local'|'network'|'network_loss'), store (bool),
    spoil (bool), units (100 = hundredths, 1 = whole units), tiers ('era'|'size'))."""
    hist = cities_by_turn(game)
    stock = {}
    m = collections.Counter(); per_era = np.zeros((3, NN, 2), np.int64)
    surplus_t = []  # per turn: player -> net surplus vector after own needs (for trade potential)
    waste = 0; produced_total = np.zeros(NG, np.int64); round_loss = 0
    cons_total = np.zeros(NG, np.int64); stock_delta = np.zeros(NG, np.int64)
    state_hash = hashlib.sha256()
    q = V['units']
    last_key = None; plots = {}
    series = np.zeros((game['turns'], NN, 2), np.int64)  # per turn and need: population fully supplied, population
    bysize = np.zeros((4, 2), np.int64)  # staple short city-turns and city-turns, by size 1-3, 4-6, 7-10, 11+
    fl = collections.Counter()
    for t in range(game['turns']):
        cities = hist[t]
        if not cities: surplus_t.append({}); continue
        era = 0 if t < ERA_TURNS[0] else (1 if t < ERA_TURNS[1] else 2)
        sz = sizes(game, t, cities, V['rule'])
        global TG, CITY_TG, RANK
        TG, CITY_TG, RANK = BARE if V.get('cal') == 1 else (LATE if t >= CHAIN_TURN else EARLY)
        key = (tuple(sorted(cities)), t >= CHAIN_TURN, V.get('cal'))
        if key != last_key: plots = owned_plots(cities); last_key = key
        ids = sorted(cities)
        prod = np.zeros((len(ids), NG), np.int64); need = np.zeros((len(ids), NN), np.int64); food_local = np.zeros(len(ids), np.int64)
        pop = np.array([sz[p] for p in ids], np.int64)
        for ci, p in enumerate(ids):
            needv = np.array([(per[era] if V['tiers'] == 'era' else per[min(2, 0 if sz[p] < 4 else (1 if sz[p] < 9 else 2))]) * sz[p]
                              for (cat, goods, per) in NEEDS], np.int64)
            if V.get('governor') == 'aware':
                tiles = city_tiles_aware(p, sz[p], plots.get(p), needv)
            else:
                tiles = city_tiles(p, sz[p], plots.get(p), V.get('cal') in (1, 2))
            region = (XY[p][0] // 16) * 4 + XY[p][1] // 11
            wx = weather(game['seed'], t, region)
            g = CITY_TG[p] + (TG[tiles].sum(axis=0) if tiles else 0)
            food_local[ci] = (g[GI['grain']] + g[GI['fish']]) // 100
            for k in ('grain', 'fruit', 'dairy'):
                g[GI[k]] = g[GI[k]] * wx // 100
            if q == 1:  # whole units: what truncation loses
                lost = g % 100; round_loss += int(lost.sum()); g = g - lost
            prod[ci] = g
            for ni, (cat, goods, per) in enumerate(NEEDS):
                lvl = per[era] if V['tiers'] == 'era' else per[min(2, 0 if sz[p] < 4 else (1 if sz[p] < 9 else 2))]
                need[ci, ni] = lvl * sz[p]
        produced_total += prod.sum(axis=0)
        # recipes: tools from iron and wood or coal; cloth from wool (capacity from the player's buildings per city)
        for ci, p in enumerate(ids):
            o = cities[p][0]
            rows = game['players'].get(str(o)) or game['players'].get(o)
            nc = max(1, rows[t][1]) if rows and t < len(rows) else 1
            cap = 100 * (1 + (rows[t][3] // nc if rows and t < len(rows) else 0) // 4)
            fuel = prod[ci, GI['wood']] + prod[ci, GI['coal']]
            run_tools = min(cap, prod[ci, GI['iron']], fuel)
            prod[ci, GI['iron']] -= run_tools
            take_w = min(run_tools, prod[ci, GI['wood']]); prod[ci, GI['wood']] -= take_w; prod[ci, GI['coal']] -= run_tools - take_w
            prod[ci, GI['tools']] += run_tools
            run_cloth = min(cap, prod[ci, GI['wool']]); prod[ci, GI['wool']] -= run_cloth; prod[ci, GI['cloth']] += run_cloth
        # supply: production plus stock
        if V['store']:
            for ci, p in enumerate(ids):
                prod[ci] += stock.get(p, np.zeros(NG, np.int64))
        # distribution and consumption
        owners = sorted({cities[p][0] for p in ids})
        got = np.zeros_like(need)
        left = prod.copy()
        groups = [[ci] for ci in range(len(ids))] if V['dist'] == 'local' else \
                 [[ci for ci, p in enumerate(ids) if cities[p][0] == o] for o in owners]
        if V['staple'] == 'separate':
            # today's rule: food stays in its city; staple is not a good
            for ci in range(len(ids)):
                avail = food_local[ci] * 100
                got[ci, 0] = min(avail, need[ci, 0])
                left[ci, GI['grain']] = 0; left[ci, GI['fish']] = 0
        for grp in groups:
            loss = 10 if V['dist'] == 'network_loss' and len(grp) > 1 else 0
            for ni, (cat, goods, per) in enumerate(NEEDS):
                if V['staple'] == 'separate' and ni == 0: continue
                for gname in goods:
                    gi = GI[gname]
                    pool = int(left[grp, gi].sum())
                    if len(grp) > 1 and loss:
                        moved = int(sum(max(0, left[c, gi] - need[c, ni]) for c in grp))
                        pool -= moved * loss // 100
                    want = need[grp, ni] - got[grp, ni]
                    give = ration(pool, want)
                    if V.get('floatcheck') and len(grp) > 1 and int(want.sum()) > pool > 0:
                        # the same rationing in single-precision floating point, summing the cities in two orders
                        w32 = want.astype(np.float32); a32 = np.float32(pool) / np.float32(100)
                        f_fwd = np.float32(0); f_rev = np.float32(0)
                        for v in w32 / np.float32(100): f_fwd = np.float32(f_fwd + v)
                        for v in (w32 / np.float32(100))[::-1]: f_rev = np.float32(f_rev + v)
                        g_fwd = np.floor(w32 / np.float32(100) * (a32 / f_fwd) * np.float32(100)).astype(np.int64)
                        g_rev = np.floor(w32 / np.float32(100) * (a32 / f_rev) * np.float32(100)).astype(np.int64)
                        fl['rations'] += 1
                        fl['sum_differs'] += int(f_fwd != f_rev)
                        fl['alloc_differs'] += int((g_fwd != g_rev).any())
                        fl['unconserved'] += int(abs(int(g_fwd.sum()) - pool) > 0)
                    got[grp, ni] += give
                    # take what was given from the cities, own production first, then pro rata from the others
                    taken = int(give.sum())
                    if taken:
                        share = ration(taken, left[grp, gi].copy())
                        left[grp, gi] -= share
                    cons_total[gi] += taken
        # what is left becomes stock (with spoilage) or is lost
        newstock = {}
        for ci, p in enumerate(ids):
            rest = left[ci].copy()
            # surplus staple fills the food box (growth), after a granary reserve of three turns' need when stores exist
            staple = int(rest[GI['grain']] + rest[GI['fish']])
            reserve = min(staple, 3 * int(need[ci, 0])) if V['store'] else 0
            m['to_growth'] += staple - reserve
            grain_keep = min(int(rest[GI['grain']]), reserve); rest[GI['grain']] = grain_keep; rest[GI['fish']] = reserve - grain_keep  # grain keeps; fish only to fill
            if V['store']:
                if V['spoil']:
                    for gname, pc in SPOIL.items():
                        s = rest[GI[gname]] * pc // 100; waste += int(s); rest[GI[gname]] -= s
                cap_s = 1000 * sz[p]  # storage: 10 units per citizen per good (assumption)
                over = np.maximum(rest - cap_s, 0); waste += int(over.sum()); rest -= over
                newstock[p] = rest
            else:
                waste += int(rest.sum())
        stock = newstock
        # bookkeeping
        met = got * 100 // np.maximum(need, 1)
        for ni in range(NN):
            msk = need[:, ni] > 0
            per_era[era, ni, 0] += int((met[msk, ni] >= 100).sum()); per_era[era, ni, 1] += int(msk.sum())
            m['short_' + NEEDS[ni][0]] += int(((met[:, ni] < 100) & msk).sum())
            m['shortpop_' + NEEDS[ni][0]] += int(pop[(met[:, ni] < 100) & msk].sum())
        m['cityturns'] += len(ids); m['popturns'] += int(pop.sum())
        for ni in range(NN):
            msk = need[:, ni] > 0
            series[t, ni, 0] += int(pop[msk & (met[:, ni] >= 100)].sum()); series[t, ni, 1] += int(pop[msk].sum())
        sb = np.minimum(np.searchsorted([3, 6, 10], pop, side='left'), 3)
        for b in range(4):
            bysize[b, 0] += int(((met[:, 0] < 100) & (sb == b)).sum()); bysize[b, 1] += int((sb == b).sum())
        m['food_deficit_local'] += int((food_local < 3 * pop).sum())
        # each player's surplus after its own needs: what it could export, and its unmet needs: what it could import
        sp = {}
        for o in owners:
            idx = [ci for ci, p in enumerate(ids) if cities[p][0] == o]
            sur = left[idx].sum(axis=0) if not V['store'] else np.array([max(0, int(x)) for x in left[idx].sum(axis=0)])
            unmet = (need[idx] - got[idx]).sum(axis=0)
            sp[o] = (sur, unmet)
        surplus_t.append(sp)
        state_hash.update(left.tobytes()); state_hash.update(got.tobytes())
    return dict(series=series, bysize=bysize, fl=fl, m=m, per_era=per_era, surplus=surplus_t, waste=waste, produced=produced_total, round_loss=round_loss,
                consumed=cons_total, hash=state_hash.hexdigest())


if __name__ == '__main__':
    base_v = dict(rule='age', staple='separate', dist='local', store=False, spoil=False, units=100, tiers='era')
    VARIANTS = {
        'today_food': dict(base_v),
        'goods_local': dict(base_v, staple='goods'),
        'goods_network': dict(base_v, staple='goods', dist='network'),
        'goods_network_loss': dict(base_v, staple='goods', dist='network_loss'),
        'network_store': dict(base_v, staple='goods', dist='network', store=True),
        'network_store_spoil': dict(base_v, staple='goods', dist='network', store=True, spoil=True),
        'whole_units': dict(base_v, staple='goods', dist='network', units=1),
        'tiers_size': dict(base_v, staple='goods', dist='network', tiers='size'),
        'equal_split': dict(base_v, staple='goods', dist='network', rule='equal'),
    }
    games = [g for g in G if g['completed']]
    res = {}
    t0 = time.time()
    VARIANTS['aware_network'] = dict(base_v, staple='goods', dist='network', governor='aware')
    VARIANTS['aware_network_store_spoil'] = dict(base_v, staple='goods', dist='network', store=True, spoil=True, governor='aware')
    for name, V in VARIANTS.items():
        agg = collections.Counter(); pe = np.zeros((3, NN, 2), np.int64); waste = 0; prodt = np.zeros(NG, np.int64)
        rl = 0; hashes = []; trade = np.zeros(NG, np.int64); trade_pairs = 0; turns_n = 0
        for g in games:
            r = run(g, V)
            agg.update(r['m']); pe += r['per_era']; waste += r['waste']; prodt += r['produced']; rl += r['round_loss']
            hashes.append(r['hash'])
            for sp in r['surplus']:
                if not sp: continue
                turns_n += 1
                S = sum((v[0] for v in sp.values()), np.zeros(NG, np.int64)); D = sum((v[1] for v in sp.values()), np.zeros(NN, np.int64))
                # potential trade per need: the goods that satisfy it, surplus of some players against unmet need of others
                for ni, (cat, goods, per) in enumerate(NEEDS):
                    sup = int(sum(S[GI[x]] for x in goods))
                    trade[GI[goods[0]]] += min(sup, int(D[ni]))
        res[name] = dict(V=V, m=dict(agg), per_era=pe.tolist(), waste=waste, produced=prodt.tolist(), round_loss=rl,
                         trade_potential=trade.tolist(), turns=turns_n, games=len(games),
                         hash=hashlib.sha256(''.join(hashes).encode()).hexdigest()[:16])
        print(name, 'done', round(time.time() - t0, 1), 's', flush=True)
    # determinism: run one variant twice
    again = run(games[0], VARIANTS['network_store_spoil'])['hash']
    first = run(games[0], VARIANTS['network_store_spoil'])['hash']
    OUT['determinism'] = dict(same_hash_twice=again == first, hash=first[:16])
    OUT['variants'] = res
    OUT['goods'] = GOODS; OUT['needs'] = [(n[0], n[1], n[2]) for n in NEEDS]; OUT['spoil'] = SPOIL; OUT['era_turns'] = ERA_TURNS
    json.dump(OUT, open(os.path.join(ROOT, 'data', 'model.json'), 'w'), indent=1)
    print(json.dumps({k: (v['m'].get('short_staple', 0) / max(1, v['m']['cityturns'])) for k, v in res.items()}, indent=1))
