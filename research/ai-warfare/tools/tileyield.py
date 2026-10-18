#!/usr/bin/env python3
"""The exact yield of every worked plot at the save, rebuilt from the XML records and split by source.

usage: tileyield.py <registry.fig.json> <records.json> <game.duckdb> ...   (databases with a save dump)

The model is CvPlot::calculateYield, calculateNatureYield and calculateImprovementYieldChange
(CvPlot.cpp:6129-6470, GitLab main), term by term:
  nature      terrain yield; the YieldInfo hills change on hills and lake change on a lake; the resource's yield when the
              owner's team holds its TechReveal; the river change and the hills change of the
              feature (or of the terrain when there is none); the feature's yield; at least 0
  improvement the improvement's yield, its river-side, hills and irrigated changes (irrigation
              available: the plot irrigated or with fresh water, i.e. on a river or next to a lake or
              a feature with bAddsFreshWater, or next to an irrigated plot; a lake is a water area of at
              most LAKE_MAX_AREA_SIZE plots, 8-neighbour, map wrap ignored), its
              change for the route on the plot, and its change for the visible resource
  tech        the improvement's TechYieldChanges for techs the owner's team holds
  civic       the CivicInfo ImprovementYieldChanges of the owner's civics
  route       the route's own yield
  city        the working city's RiverPlotYieldChanges and SeaPlotYieldChanges (its buildings, with the
              free buildings the owner's buildings grant, FreeBuilding),
              the owner's GlobalSeaPlotYieldChanges; on a city plot, the YieldInfo city change and
              its minimum
  bonus       the trait ExtraYieldThresholds (EXTRA_YIELD when reached) and, in a golden age, the
              YieldInfo golden-age yield when its threshold is reached
The model is compared with the yields in the save dump (CvPlot::getYield). The check table gives,
per side and yield, the plots predicted exactly; only exactly predicted plots enter the source
tables, so every source figure there adds up to the plot's real yield.
Tables: <game>_yield_check, <game>_yield_sources (per side, improvement and yield: plots, actual
mean, and the mean of each source).
"""
import collections, json, os, sys

import duckdb

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

REG, RECS, DBS = sys.argv[1], sys.argv[2], sys.argv[3:]
R = json.load(open(RECS))
T, F, B, I, RT, Y, C, BU = (R[k] for k in ('TerrainInfo', 'FeatureInfo', 'BonusInfo', 'ImprovementInfo', 'RouteInfo', 'YieldInfo',
                                           'CivicInfo', 'BuildingInfo'))
YN = ['YIELD_FOOD', 'YIELD_PRODUCTION', 'YIELD_COMMERCE']
vec = lambda v: (list(v) + [0, 0, 0])[:3] if isinstance(v, list) else [0, 0, 0]
yi = lambda k: [Y[y].get(k) or 0 for y in YN]
LAKE_MAX = R['Define']['LAKE_MAX_AREA_SIZE']['iDefineIntVal']
EXTRA = R['Define'].get('EXTRA_YIELD', {}).get('iDefineIntVal') or 0
GROUPS = {'COTTAGE': 'cottage', 'HAMLET': 'hamlet', 'VILLAGE': 'village', 'TOWN': 'town', 'FARM': 'farm', 'MINE': 'mine',
          'SHAFT_MINE': 'mine', 'CAMP': 'camp', 'WORKSHOP': 'workshop', '-': 'none'}
SRC = ['nature', 'improvement', 'tech', 'civic', 'route', 'city', 'bonus']


def model(p, ctx):
    """p: plot row (dict); ctx: owner's techs, civics, traits, golden age, city buildings, global sea yield."""
    out = {s: [0, 0, 0] for s in SRC}
    if p['plot_type'] == 0: return out                                 # peaks are impassable
    t = T['TERRAIN_' + p['terrain']]; f = F.get('FEATURE_' + p['feature']) if p['feature'] != '-' else None
    hills = p['plot_type'] == 1; river = p['river'] == 1
    bonus = None
    if p['bonus'] != '-':
        b = B['BONUS_' + p['bonus']]
        rev = (b.get('TechReveal') or 'NONE')
        if rev == 'NONE' or rev.removeprefix('TECH_') in ctx['techs']: bonus = 'BONUS_' + p['bonus']
    for i in range(3):
        v = vec(t.get('Yields'))[i]
        if hills: v += yi('iHillsChange')[i]
        if ctx['lake'](p): v += yi('iLakeChange')[i]
        if bonus: v += vec(B[bonus].get('YieldChanges'))[i]
        if river: v += vec((f or t).get('RiverYieldChange'))[i]
        if hills: v += vec((f or t).get('HillsYieldChange'))[i]
        if f: v += vec(f.get('YieldChanges'))[i]
        out['nature'][i] = max(0, v)
    imp = I.get('IMPROVEMENT_' + p['improvement']) if p['improvement'] != '-' else None
    if imp:
        for i in range(3):
            v = vec(imp.get('YieldChanges'))[i]
            if river: v += vec(imp.get('RiverSideYieldChange'))[i]
            if hills: v += vec(imp.get('HillsYieldChange'))[i]
            if ctx['irrigation'](p): v += vec(imp.get('IrrigatedYieldChange'))[i]
            for ry in imp.get('RouteYieldChanges') or []:
                if p['route'] != '-' and ry.get('RouteType') == 'ROUTE_' + p['route']: v += vec(ry.get('RouteYields'))[i]
            if bonus:
                for grp in imp.get('BonusTypeStructs') or []:
                    for bs in (grp if isinstance(grp, list) else [grp]):
                        if bs.get('BonusType') == bonus: v += vec((bs.get('YieldChanges') or [[0, 0, 0]])[0])[i]
            out['improvement'][i] = v
            out['tech'][i] = sum(vec(ty.get('TechYields'))[i] for ty in imp.get('TechYieldChanges') or []
                                 if (ty.get('PrereqTech') or '').removeprefix('TECH_') in ctx['techs'])
            out['civic'][i] = sum(vec(iy.get('ImprovementYields'))[i] for c in ctx['civics'] for iy in (C[c].get('ImprovementYieldChanges') or [])
                                  if iy.get('ImprovementType') == 'IMPROVEMENT_' + p['improvement'])
    if p['route'] != '-':
        out['route'] = vec(RT['ROUTE_' + p['route']].get('Yields'))
    cb = ctx['city_buildings'].get((p['wc_x'], p['wc_y']), [])
    water = p['plot_type'] == 3
    for i in range(3):
        v = 0
        if river and not water: v += sum(vec(BU[b].get('RiverPlotYieldChanges'))[i] for b in cb if b in BU)
        if water: v += sum(vec(BU[b].get('SeaPlotYieldChanges'))[i] for b in cb if b in BU) + ctx['global_sea'][i]
        out['city'][i] = v
    is_city = (p['x'], p['y']) in ctx['city_plots']
    tot = [sum(out[s][i] for s in SRC) for i in range(3)]
    for i in range(3):
        if is_city:
            v = tot[i] + yi('iCityChange')[i]
            v = max(v, yi('iMinCity')[i]); out['city'][i] += v - tot[i]; tot[i] = v
        add = 0
        thr = ctx['extra_threshold'][i]
        if thr > 0 and tot[i] >= thr: add += EXTRA
        if ctx['golden'] and yi('iGoldenAgeYield')[i] and tot[i] + add >= yi('iGoldenAgeYieldThreshold')[i]: add += yi('iGoldenAgeYield')[i]
        out['bonus'][i] = add
    return out


reg = Registry(REG, [RECS] + DBS, R)
for db in DBS:
    g = os.path.basename(db).split('.')[0]
    con = duckdb.connect(db, read_only=True)
    cols = [d[0] for d in con.execute('select * from plots limit 0').description]
    plots = [dict(zip(cols, r)) for r in con.execute('select * from plots').fetchall()]
    at = {(p['x'], p['y']): p for p in plots}
    human = con.execute('select player from players where human=1').fetchone()[0]
    techs = collections.defaultdict(set); civics = collections.defaultdict(list); cbs = collections.defaultdict(dict)
    for pl, t in con.execute('select player, tech from techs').fetchall(): techs[pl].add(t.removeprefix('TECH_'))
    for pl, c in con.execute('select player, civic from civics').fetchall():
        if c in C: civics[pl].append(c)
    for pl, x, y, b in con.execute('select player, x, y, building from city_buildings').fetchall(): cbs[pl].setdefault((x, y), []).append(b)
    # free buildings (BuildingInfo FreeBuilding, e.g. the Pyramids' Irrigation Canals) are in every city of the owner; the
    # dump lists real buildings only (CvCity::getNumRealBuilding), so they are added here as the class's default building
    for pl, cities_b in cbs.items():
        free = {BU[b]['FreeBuilding'] for bl in cities_b.values() for b in bl if b in BU and BU[b].get('FreeBuilding') not in (None, 'NONE')}
        for fc in free:
            d = R['BuildingClassInfo'].get(fc, {}).get('DefaultBuilding')
            for bl in cities_b.values():
                if d and d not in bl: bl.append(d)
    city_plots = {(x, y) for x, y in con.execute('select x, y from cities').fetchall()}
    st = con.execute("select turn from snapshots where state='state'").fetchone() if con.execute(
        "select count(*) from information_schema.tables where table_name='snapshots'").fetchone()[0] else None
    last = con.execute('select max(turn) from wl_M').fetchone()[0]
    golden = {pl for pl, gd in con.execute('select player, golden from wl_M where turn=?', [last]).fetchall() if gd and gd > 0}
    leaders = dict(con.execute('select player, leader from players').fetchall())
    def traits(pl):
        lh = R['LeaderHeadInfo'].get(leaders.get(pl), {})
        return [t['TraitType'] for t in (lh.get('Traits') or []) if isinstance(t, dict) and t.get('bTrait')]
    # water areas (8-neighbour components, map wrap ignored); a lake is one of at most LAKE_MAX_AREA_SIZE plots (CvArea::isLake)
    comp, size = {}, {}
    for p0 in plots:
        if p0['plot_type'] != 3 or (p0['x'], p0['y']) in comp: continue
        stack, k = [(p0['x'], p0['y'])], len(size); comp[stack[0]] = k; n = 0
        while stack:
            x, y = stack.pop(); n += 1
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    q = at.get((x + dx, y + dy))
                    if q is not None and q['plot_type'] == 3 and (q['x'], q['y']) not in comp:
                        comp[(q['x'], q['y'])] = k; stack.append((q['x'], q['y']))
        size[k] = n
    lake = lambda q: q['plot_type'] == 3 and size[comp[(q['x'], q['y'])]] <= LAKE_MAX
    fresh_feature = {k[8:] for k, v in F.items() if v.get('bAddsFreshWater')}
    def fresh(p):                                    # CvPlot::isFreshWater
        if p['plot_type'] == 3: return False
        if p['river'] == 1: return True
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = at.get((p['x'] + dx, p['y'] + dy))
                if q is not None and (lake(q) or q['feature'] in fresh_feature): return True
        return False
    def irrigation(p):                               # CvPlot::isIrrigationAvailable
        if p['irrigated'] == 1 or fresh(p): return True
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                q = at.get((p['x'] + dx, p['y'] + dy))
                if q is not None and q is not p and q['irrigated'] == 1: return True
        return False
    rows = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, [0.0] * 3, {s: [0.0] * 3 for s in SRC}]))
    check = collections.defaultdict(lambda: [0, [0, 0, 0], 0, 0])
    last_t = con.execute('select max(turn) from wl_T').fetchone()[0]
    fought = {(x, y) for x, y in con.execute('select distinct x, y from wl_C where turn >= ?', [last_t - 10]).fetchall()}
    for p in plots:
        if p['worked'] != 1 or p['owner'] < 0: continue
        pl = p['owner']
        ctx = dict(techs=techs[pl], civics=civics[pl], irrigation=irrigation, lake=lake, city_buildings=cbs[pl], city_plots=city_plots,
                   golden=pl in golden,
                   global_sea=[sum(vec(BU[b].get('GlobalSeaPlotYieldChanges'))[i] for bl in cbs[pl].values() for b in bl if b in BU) for i in range(3)],
                   extra_threshold=[max([vec(R['TraitInfo'][t].get('ExtraYieldThresholds'))[i] for t in traits(pl)] or [0]) for i in range(3)])
        m = model(p, ctx)
        pred = [sum(m[s][i] for s in SRC) for i in range(3)]
        act = [p['food'], p['hammers'], p['commerce']]
        side = 'human' if pl == human else 'AI'
        ok = [pred[i] == act[i] for i in range(3)]
        ch = check[side]; ch[0] += 1
        for i in range(3): ch[1][i] += ok[i]
        ch[2] += all(ok)
        if not all(ok):
            ch[3] += (p['x'], p['y']) in fought
            continue
        grp = 'water' if p['plot_type'] == 3 else 'city plot' if (p['x'], p['y']) in city_plots else GROUPS.get(p['improvement'], 'other')
        r = rows[side][grp]; r[0] += 1
        for i in range(3):
            r[1][i] += act[i]
            for s in SRC: r[2][s][i] += m[s][i]
    crow = [[side, n, ok[0], ok[1], ok[2], allok, n - allok, bat] for side, (n, ok, allok, bat) in sorted(check.items(), reverse=True)]
    reg.result_table(f'{g}_yield_check', ['side', 'worked_plots', 'food_exact', 'hammers_exact', 'commerce_exact', 'all_three_exact', 'missed',
                                          'missed_with_a_battle_there'], crow,
                     'tiles at save', 'every player', 'save', 'tileyield.py: the model against CvPlot::getYield in the save dump; a battle '
                     'there: a C line on the plot in the last ten turns (DCM battle effects, BATTLE_EFFECT_LESS_FOOD and _COMMERCE, are not in the dump)',
                     [r[0] for r in crow], n=sum(r[1] for r in crow))
    srows = []
    for side in sorted(rows, reverse=True):
        for grp in sorted(rows[side], key=lambda k: -rows[side][k][0]):
            n, act, src = rows[side][grp]
            for i, yname in enumerate(('food', 'hammers', 'commerce')):
                srows.append([f'{side}, {grp}, {yname}', n, round(act[i] / n, 2)] + [round(src[s][i] / n, 2) for s in SRC])
    reg.result_table(f'{g}_yield_sources', ['side_improvement_yield', 'plots', 'actual'] + SRC, srows, 'food per tile', 'every player', 'save',
                     'tileyield.py: exactly predicted worked plots; mean yield per plot and the mean of each source term '
                     '(food, hammers and commerce rows; the unit applies to each row\'s own yield)', [r[0] for r in srows], n=sum(r[1] for r in srows) // 3)
    print(g, crow, file=sys.stderr)
reg.save()
