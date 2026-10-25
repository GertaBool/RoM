#!/usr/bin/env python3
"""Facts for the land-and-industry design: the mod's terrain, feature, bonus, improvement, building and
unit records, and the plots of one WorldBuilder map. Reads only; writes JSON next to the document.

usage: extract.py <mod checkout> <WorldBuilder save> <out dir>
"""
import json, os, re, sys

mod, wbs, out = sys.argv[1:4]
X = os.path.join(mod, 'Assets', 'XML')


def records(path, tag):
    t = open(path, encoding='latin-1').read()
    return re.findall(r'<%s>.*?</%s>' % (tag, tag), t, re.S)


def one(r, tag, default=None):
    m = re.search(r'<%s>([^<]*)</%s>' % (tag, tag), r)
    return m.group(1).strip() if m else default


def ints(r, outer, inner):
    m = re.search(r'<%s>(.*?)</%s>' % (outer, outer), r, re.S)
    return [int(v) for v in re.findall(r'<%s>(-?\d+)</%s>' % (inner, inner), m.group(1))] if m else []


terrains = []
for r in records(os.path.join(X, 'Terrain', 'CIV4TerrainInfos.xml'), 'TerrainInfo'):
    terrains.append(dict(type=one(r, 'Type'), yields=ints(r, 'Yields', 'iYield'),
                         river=ints(r, 'RiverYieldChange', 'iYield'), hills=ints(r, 'HillsYieldChange', 'iYield'),
                         water=one(r, 'bWater') == '1'))

features = []
for r in records(os.path.join(X, 'Terrain', 'CIV4FeatureInfos.xml'), 'FeatureInfo'):
    features.append(dict(type=one(r, 'Type'), yields=ints(r, 'YieldChanges', 'iYieldChange'),
                         health=int(one(r, 'iHealthPercent', '0'))))

bonuses = []
for r in records(os.path.join(X, 'Terrain', 'CIV4BonusInfos.xml'), 'BonusInfo'):
    terr = re.findall(r'<TerrainType>(\w+)</TerrainType>\s*<bTerrain>1', r)
    feat = re.findall(r'<FeatureType>(\w+)</FeatureType>\s*<bFeature>1', r)
    featterr = re.findall(r'<TerrainType>(\w+)</TerrainType>\s*<bFeatureTerrain>1', r)
    bonuses.append(dict(type=one(r, 'Type'), cls=one(r, 'BonusClassType'), reveal=one(r, 'TechReveal'),
                        yields=ints(r, 'YieldChanges', 'iYieldChange'), health=int(one(r, 'iHealth', '0')),
                        happy=int(one(r, 'iHappiness', '0')), minlat=int(one(r, 'iMinLatitude', '0')),
                        maxlat=int(one(r, 'iMaxLatitude', '90')), hills=one(r, 'bHills') == '1',
                        flat=one(r, 'bFlatlands') == '1', terrains=terr, features=feat, featureterrains=featterr,
                        placement=int(one(r, 'iPlacementOrder', '-1'))))

improvements = []
for r in records(os.path.join(X, 'Terrain', 'CIV4ImprovementInfos.xml'), 'ImprovementInfo'):
    bys = {}
    for s in re.findall(r'<BonusTypeStruct>(.*?)</BonusTypeStruct>', r, re.S):
        b = one(s, 'BonusType')
        y = [int(v) for v in re.findall(r'<iYieldChange>(-?\d+)</iYieldChange>', s)]
        if b and any(y): bys[b] = y
    own = r[:r.index('<BonusTypeStructs>')] if '<BonusTypeStructs>' in r else r  # the improvement's own fields come first
    improvements.append(dict(type=one(r, 'Type'), yields=ints(own, 'YieldChanges', 'iYieldChange'),
                             irrigated=ints(own, 'IrrigatedYieldChange', 'iYield'),
                             requires_irrigation=one(own, 'bRequiresIrrigation') == '1',
                             upgrade=one(r, 'ImprovementUpgrade'), upgrade_time=int(one(r, 'iUpgradeTime', '0')),
                             pillage=one(r, 'ImprovementPillage'), bonus_yields=bys))

builds = []
for r in records(os.path.join(X, 'Units', 'CIV4BuildInfos.xml'), 'BuildInfo'):
    builds.append(dict(type=one(r, 'Type'), improvement=one(r, 'ImprovementType'), tech=one(r, 'PrereqTech'),
                       time=int(one(r, 'iTime', '0'))))

buildings = []
for r in records(os.path.join(X, 'Buildings', 'CIV4BuildingInfos.xml'), 'BuildingInfo'):
    pre_or = re.search(r'<PrereqBonuses>(.*?)</PrereqBonuses>', r, re.S)
    ors = [b for b in re.findall(r'<Bonus>(\w+)</Bonus>', pre_or.group(1)) if b != 'NONE'] if pre_or else []
    head = r[:pre_or.start()] if pre_or else r
    single = [b for b in re.findall(r'<Bonus>(\w+)</Bonus>', head) if b != 'NONE']
    mods = {}
    for s in re.findall(r'<BonusYieldModifier>(.*?)</BonusYieldModifier>', r, re.S):
        b = one(s, 'BonusType')
        y = [int(v) for v in re.findall(r'<iYield>(-?\d+)</iYield>', s)]
        if b and any(y): mods[b] = y
    buildings.append(dict(type=one(r, 'Type'), free_bonus=one(r, 'FreeBonus'),
                          num_free=int(one(r, 'iNumFreeBonuses', '0')), prereq=single[:1], prereq_or=ors,
                          cost=int(one(r, 'iCost', '0')), tech=one(r, 'PrereqTech'), bonus_yield_mods=mods))

units = []
for r in records(os.path.join(X, 'Units', 'CIV4UnitInfos.xml'), 'UnitInfo'):
    pre = re.search(r'<PrereqBonuses>(.*?)</PrereqBonuses>', r, re.S)
    head = r[:pre.start()] if pre else r
    single = re.findall(r'<BonusType>(\w+)</BonusType>', head)
    ors = [b for b in re.findall(r'<BonusType>(\w+)</BonusType>', pre.group(1)) if b != 'NONE'] if pre else []
    units.append(dict(type=one(r, 'Type'), prereq=[b for b in single if b != 'NONE'][:1], prereq_or=ors,
                      cost=int(one(r, 'iCost', '0')), combat=int(one(r, 'iCombat', '0'))))

# The map: grid, latitudes and every plot.
t = open(wbs, encoding='latin-1').read()
mp = re.search(r'BeginMap(.*?)EndMap', t, re.S).group(1)
grid = dict(width=int(re.search(r'grid width=(\d+)', mp).group(1)), height=int(re.search(r'grid height=(\d+)', mp).group(1)),
            top=int(re.search(r'top latitude=(-?\d+)', mp).group(1)), bottom=int(re.search(r'bottom latitude=(-?\d+)', mp).group(1)),
            wrapx=re.search(r'wrap X=(\d)', mp).group(1) == '1', wrapy=re.search(r'wrap Y=(\d)', mp).group(1) == '1')
players = []
for blk in re.findall(r'BeginPlayer(.*?)EndPlayer', t, re.S):
    civ = re.search(r'CivType=(\w+)', blk)
    st = re.search(r'StartingX=(-?\d+), StartingY=(-?\d+)', blk)
    if civ and st and civ.group(1) != 'NONE' and int(st.group(1)) >= 0:
        players.append(dict(civ=civ.group(1), x=int(st.group(1)), y=int(st.group(2))))
plots = []
for p in re.findall(r'BeginPlot(.*?)EndPlot', t, re.S):
    xy = re.search(r'x=(\d+),y=(\d+)', p)
    plots.append(dict(x=int(xy.group(1)), y=int(xy.group(2)), terrain=(re.search(r'TerrainType=(\w+)', p) or [None, None])[1],
                      plot=int((re.search(r'PlotType=(\d)', p) or [None, '2'])[1]),
                      feature=(re.search(r'FeatureType=(\w+)', p) or [None, None])[1],
                      bonus=(re.search(r'BonusType=(\w+)', p) or [None, None])[1],
                      river=bool(re.search(r'River(NS|WE)Direction', p))))

os.makedirs(out, exist_ok=True)
json.dump(dict(source=dict(mod=mod, map=os.path.basename(wbs)), terrains=terrains, features=features, bonuses=bonuses,
               improvements=improvements, builds=builds, buildings=buildings, units=units, grid=grid, players=players, plots=plots),
          open(os.path.join(out, 'facts.json'), 'w'))
print('players %d ' % len(players) + 'terrains %d features %d bonuses %d improvements %d buildings %d units %d plots %d' %
      (len(terrains), len(features), len(bonuses), len(improvements), len(buildings), len(units), len(plots)))
