#!/usr/bin/env python3
"""City growth at the save, computed with the game's own rules for every city.

usage: growth.py <registry.fig.json> <records.json> <game.duckdb> ...   (databases with a save dump)

Per city (save dump: population, foodDifference, health, happiness, buildings; plots: exact yields):
  threshold   CvPlayer::getGrowthThreshold (CvPlayer.cpp:23672-23694): (BASE_CITY_GROWTH_THRESHOLD +
              pop * CITY_GROWTH_MULTIPLIER) * the speed's iGrowthPercent / 100 * the start era's
              iGrowthPercent / 100; for an AI also * the handicap's iAIGrowthPercent / 100 *
              (iAIPerEraModifier * era + 100) / 100; integer division at each step, at least 1
  kept        CvCity::getMaxFoodKeptPercent: the sum of iFoodKept of the city's buildings (CvCity.cpp:4382),
              with the free buildings the owner's buildings grant (FreeBuilding); the dump lists real ones only
  per growth  the food a new citizen costs once the kept store is full: threshold - threshold * kept / 100
              (CvCity::doGrowth, CvCity.cpp:13404-13420)
  turns       per growth / foodDifference, rounded up, for cities with a surplus
  food        the city's food rate: foodDifference + consumption, consumption = pop *
              FOOD_CONSUMPTION_PER_POPULATION - min(0, good - bad health) (CvCity::foodConsumption)
  tiles       the food of the plots it works (CvPlot::getYield in the dump); other = food - tiles: trade
              routes, specialists and percentage modifiers
  trade       food and hammers from trade routes, estimated: each route yields profit * the owner's trade
              yield modifier / 100 (CvCity::calculateTradeYield, CvCity.cpp:9510-9520), the modifier being the
              YieldInfo iTradeModifier plus the TradeYieldModifiers of the owner's civics and traits; so the
              food and hammers are the city's trade commerce (dump) * their modifier / the commerce modifier,
              rounding per route ignored
Cities with neither hammers nor commerce are in disorder (foodDifference is 0 there) and are left out.
Tables: <game>_growth (per group of cities: medians), <game>_food_kept (cities by their food-kept percentage).
"""
import collections, json, math, os, statistics, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

REG, RECS, DBS = sys.argv[1], sys.argv[2], sys.argv[3:]
R = json.load(open(RECS)); D = R['Define']; BU = R['BuildingInfo']
dv = lambda k: D[k]['iDefineIntVal']
reg = Registry(REG, [RECS] + DBS, R)
for db in DBS:
    g = os.path.basename(db).split('.')[0]
    con = duckdb.connect(db, read_only=True)
    speed, handicap = con.execute('select speed, handicap from wl_H').fetchone()
    sp = R['GameSpeedInfo'][speed]['iGrowthPercent']; hc = R['HandicapInfo'][handicap]
    # the start era is not in the log; iGrowthPercent is 100 for the ancient, classical and medieval eras alike, so any of them gives this
    start_era = 'ERA_ANCIENT'
    ep = R['EraInfo'][start_era]['iGrowthPercent']
    human = con.execute('select player from players where human=1').fetchone()[0]
    era = dict(con.execute('select player, era from players').fetchall())
    leaders = dict(con.execute('select player, leader from players').fetchall())
    civ = collections.defaultdict(list)
    for pl, c in con.execute('select player, civic from civics').fetchall(): civ[pl].append(c)
    def trade_mod(pl):
        m = [R['YieldInfo'][y].get('iTradeModifier') or 0 for y in ('YIELD_FOOD', 'YIELD_PRODUCTION', 'YIELD_COMMERCE')]
        srcs = [R['CivicInfo'][c].get('TradeYieldModifiers') for c in civ[pl] if c in R['CivicInfo']]
        lh = R['LeaderHeadInfo'].get(leaders.get(pl), {})
        srcs += [R['TraitInfo'][t['TraitType']].get('TradeYieldModifiers') for t in (lh.get('Traits') or []) if isinstance(t, dict) and t.get('bTrait')]
        for v in srcs:
            if isinstance(v, list):
                for i in range(3): m[i] += (v + [0, 0, 0])[i]
        return m
    cb = collections.defaultdict(list)
    for pl, x, y, b in con.execute('select player, x, y, building from city_buildings').fetchall(): cb[(pl, x, y)].append(b)
    for pl in {k[0] for k in cb}:
        free = {BU[b]['FreeBuilding'] for k, bl in cb.items() if k[0] == pl for b in bl if b in BU and BU[b].get('FreeBuilding') not in (None, 'NONE')}
        for fc in free:
            d = R['BuildingClassInfo'].get(fc, {}).get('DefaultBuilding')
            for k, bl in cb.items():
                if k[0] == pl and d and d not in bl: bl.append(d)
    tiles = collections.Counter()
    for x, y, f in con.execute('select wc_x, wc_y, food from plots where worked=1').fetchall(): tiles[(x, y)] += f
    captured = {(x, y) for x, y in con.execute('select x, y from wl_K').fetchall()}
    rows = collections.defaultdict(list); kept_count = collections.Counter()
    for pl, x, y, pop, fd, prod, com, good, bad, happy, unhappy, tcom in con.execute(
            'select player, x, y, pop, food, prod, commerce, good, bad, happy, unhappy, coalesce(trade_commerce, 0) from cities').fetchall():
        if prod == 0 and com == 0: continue
        b = cb[(pl, x, y)]
        cap = 'BUILDING_PALACE' in b
        grp = ('human capital' if cap else 'human captured' if (x, y) in captured else 'human founded') if pl == human else \
              ('AI capitals' if cap else 'AI other')
        t = (dv('BASE_CITY_GROWTH_THRESHOLD') + pop * dv('CITY_GROWTH_MULTIPLIER')) * sp // 100 * ep // 100
        if pl != human:
            t = t * hc['iAIGrowthPercent'] // 100
            t = t * max(0, hc['iAIPerEraModifier'] * (era.get(pl) or 0) + 100) // 100
        t = max(1, t)
        kept = sum(BU[k].get('iFoodKept') or 0 for k in b if k in BU)
        per = t - t * kept // 100
        food = fd + pop * dv('FOOD_CONSUMPTION_PER_POPULATION') - min(0, good - bad)
        tm = trade_mod(pl)
        tfood = tcom * tm[0] / tm[2] if tm[2] > 0 else 0
        tham = tcom * tm[1] / tm[2] if tm[2] > 0 else 0
        rows[grp].append(dict(pop=pop, surplus=fd, t=t, kept=kept, per=per, turns=math.ceil(per / fd) if fd > 0 else None,
                              food=food, tiles=tiles[(x, y)], other=food - tiles[(x, y)], happy=happy - unhappy, health=good - bad,
                              tfood=tfood, tham=tham, tcom=tcom))
        kept_count[('human' if pl == human else 'AI', kept)] += 1
    med = lambda v: round(statistics.median(v), 1) if v else ''
    out = []
    order = ['human capital', 'human founded', 'human captured', 'AI capitals', 'AI other']
    for grp in [o for o in order if o in rows]:
        r = rows[grp]
        out.append([grp, len(r), med([c['pop'] for c in r]), med([c['food'] for c in r]), med([c['tiles'] for c in r]), med([c['other'] for c in r]),
                    med([c['tcom'] for c in r]), med([c['tfood'] for c in r]), med([c['tham'] for c in r]),
                    med([c['surplus'] for c in r]), sum(1 for c in r if c['surplus'] > 0), med([c['t'] for c in r]), med([c['kept'] for c in r]),
                    med([c['per'] for c in r]), med([c['turns'] for c in r if c['turns'] is not None]), med([c['happy'] for c in r]), med([c['health'] for c in r])])
    reg.result_table(f'{g}_growth', ['cities', 'n', 'pop', 'food', 'food_from_tiles', 'food_other', 'trade_commerce', 'trade_food_est', 'trade_hammers_est', 'surplus', 'growing', 'threshold',
                                     'kept_pct', 'food_per_growth', 'turns_per_growth', 'happy_margin', 'health_margin'], out,
                     'cities at save', 'every player', 'save',
                     f'growth.py on the save dump of {g} ({speed}, {handicap}); medians per group; growing: cities with a food surplus; '
                     'cities in disorder left out', [r[0] for r in out], n=sum(r[1] for r in out))
    krows = [[f'{side}, {k} per cent', n] for (side, k), n in sorted(kept_count.items(), key=lambda z: (z[0][0] != 'human', z[0][1]))]
    reg.result_table(f'{g}_food_kept', ['cities_by_food_kept', 'cities'], krows, 'cities at save', 'every player', 'save',
                     'growth.py: each city\'s sum of iFoodKept over its buildings, real and free', [r[0] for r in krows], n=sum(r[1] for r in krows))
    # buildings that raise food or keep it on growth, and the cities holding each at the save
    fb = sorted(k for k, v in BU.items() if (v.get('iFoodKept') or 0) > 0 or (v.get('RiverPlotYieldChanges') or [0])[0] > 0
                or (v.get('SeaPlotYieldChanges') or [0])[0] > 0 or (v.get('YieldModifiers') or [0])[0] > 0 or (v.get('YieldChanges') or [0])[0] > 0)
    hold = collections.Counter()
    for (pl, x, y), bl in cb.items():
        for b in bl:
            if b in fb: hold[(b, pl == human)] += 1
    frows = [[b.removeprefix('BUILDING_'), BU[b].get('iFoodKept') or 0, hold[(b, True)], hold[(b, False)]] for b in fb if hold[(b, True)] or hold[(b, False)]]
    frows.sort(key=lambda r: (-r[2], -r[3], r[0]))
    reg.result_table(f'{g}_food_buildings', ['building', 'food_kept_pct', 'human_cities', 'ai_cities'], frows, 'cities at save', 'every player', 'save',
                     'growth.py: buildings with iFoodKept, a food RiverPlotYieldChanges or SeaPlotYieldChanges, or a food YieldModifiers or '
                     'YieldChanges (BuildingInfo), and the cities holding each, real or free', [r[0] for r in frows], n=len(cb),
                     xml='BuildingInfo', xml_vals=[r[0] for r in frows])
    print(g, out, file=sys.stderr)
reg.save()
