#!/usr/bin/env python3
"""The goods catalogue and the building chains, read from the mod's XML (D3: the existing resource types are the
goods). For every resource: class, techs, yields, health and happiness, placement rules, the improvements that yield
and trade it, the buildings that give it, and everything that uses it today (buildings, units, corporations). The
proposed unit, category and land kind come from proposals.json, which the plan owns; this tool joins the two and
reports any resource without a proposal. Writes catalogue.json.
usage: catalogue.py <mod checkout> [plan dir]"""
import json, os, re, sys, glob, collections

MOD = sys.argv[1]
HERE = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X = os.path.join(MOD, 'Assets', 'XML')


def recs(paths, tag):
    out = []
    for p in paths:
        t = open(p, encoding='latin-1').read()
        out += [m.group(1) for m in re.finditer(r'<%s>(.*?)</%s>' % (tag, tag), t, re.S)]
    return out


def one(b, n, d=''):
    m = re.search(r'<%s>([^<]*)</%s>' % (n, n), b)
    return m.group(1).strip() if m else d


def ints(b, outer, inner):
    m = re.search(r'<%s>(.*?)</%s>' % (outer, outer), b, re.S)
    return [int(x) for x in re.findall(r'<%s>(-?\d+)</%s>' % (inner, inner), m.group(1))] if m else []


def mods(pattern):
    return sorted(glob.glob(os.path.join(MOD, 'Assets', 'Modules', '**', pattern), recursive=True))


# art defines (font glyph index, button)
art = {}
for b in recs([os.path.join(X, 'Art', 'CIV4ArtDefines_Bonus.xml')] + mods('*ArtDefines_Bonus.xml'), 'BonusArtInfo'):
    fi = one(b, 'FontButtonIndex')
    art[one(b, 'Type')] = dict(font_index=int(fi) if fi else None, button=one(b, 'Button'))

goods = collections.OrderedDict()
for b in recs([os.path.join(X, 'Terrain', 'CIV4BonusInfos.xml')] + mods('*BonusInfos.xml'), 'BonusInfo'):
    ty = one(b, 'Type')
    terr = re.findall(r'<TerrainType>(\w+)</TerrainType>\s*<bTerrain>1', b)
    feat = re.findall(r'<FeatureType>(\w+)</FeatureType>\s*<bFeature>1', b)
    fterr = re.findall(r'<FeatureTerrainType>(\w+)</FeatureTerrainType>\s*<bFeatureTerrain>1', b)
    placement = dict(terrains=terr, features=feat, feature_terrains=fterr, hills=one(b, 'bHills') == '1', flatlands=one(b, 'bFlatlands') == '1',
                     no_river_side=one(b, 'bNoRiverSide') == '1', latitude=[int(one(b, 'iMinLatitude', '0')), int(one(b, 'iMaxLatitude', '90'))],
                     area=one(b, 'bArea') == '1', tiles_per=int(one(b, 'iTilesPer', '0')), const_appearance=int(one(b, 'iConstAppearance', '0')))
    a = art.get(one(b, 'ArtDefineTag'), {})
    goods[ty] = dict(cls=one(b, 'BonusClassType'), art=one(b, 'ArtDefineTag'), font_index=a.get('font_index'), button=a.get('button', ''),
                     tech_reveal=one(b, 'TechReveal'), tech_trade=one(b, 'TechCityTrade'), tech_obsolete=one(b, 'TechObsolete'),
                     yields=ints(b, 'YieldChanges', 'iYieldChange'), health=int(one(b, 'iHealth', '0')), happiness=int(one(b, 'iHappiness', '0')),
                     placed=bool(terr or feat or fterr) and placement['const_appearance'] + placement['tiles_per'] > 0, placement=placement,
                     improvements=[], given_by_buildings=[], used_by=collections.defaultdict(list))

for b in recs([os.path.join(X, 'Terrain', 'CIV4ImprovementInfos.xml')], 'ImprovementInfo'):
    imp = one(b, 'Type')
    for s in re.findall(r'<BonusTypeStruct>(.*?)</BonusTypeStruct>', b, re.S):
        g = one(s, 'BonusType')
        if g in goods and (one(s, 'bBonusTrade') == '1' or one(s, 'bBonusMakesValid') == '1'):
            goods[g]['improvements'].append(dict(improvement=imp, trade=one(s, 'bBonusTrade') == '1', makes_valid=one(s, 'bBonusMakesValid') == '1',
                                                 yields=ints(s, 'YieldChanges', 'iYieldChange')))

LIMITS = {}
for b in recs([os.path.join(X, 'Buildings', 'CIV4BuildingClassInfos.xml')] + mods('*BuildingClassInfos.xml'), 'BuildingClassInfo'):
    LIMITS[one(b, 'Type')] = dict(world=int(one(b, 'iMaxGlobalInstances', '-1')), team=int(one(b, 'iMaxTeamInstances', '-1')), player=int(one(b, 'iMaxPlayerInstances', '-1')))


def kind(cls):
    l = LIMITS.get(cls, {})
    if l.get('world', -1) > 0: return 'world wonder'
    if l.get('team', -1) > 0: return 'team wonder'
    if l.get('player', -1) > 0: return 'national wonder'
    return 'building'


BUILDINGS = {}
for b in recs([os.path.join(X, 'Buildings', 'CIV4BuildingInfos.xml')] + mods('*BuildingInfos.xml'), 'BuildingInfo'):
    ty = one(b, 'Type')
    need = re.findall(r'<BuildingClassNeeded>\s*<BuildingClassType>(\w+)</BuildingClassType>\s*<bNeededInCity>1', b)
    BUILDINGS[ty] = dict(cls=one(b, 'BuildingClass'), tech=one(b, 'PrereqTech'), techs=[t for t in re.findall(r'<TechTypes>(.*?)</TechTypes>', b, re.S)[0:1] for t in re.findall(r'<PrereqTech>(\w+)', t) if t != 'NONE'] if '<TechTypes>' in b else [],
                         cost=int(one(b, 'iCost', '0')), needs=need, food_kept=int(one(b, 'iFoodKept', '0')), health=int(one(b, 'iHealth', '0')),
                         happiness=int(one(b, 'iHappiness', '0')), free_start_era=one(b, 'FreeStartEra'), kind=kind(one(b, 'BuildingClass')),
                         requires=[x for x in [one(b, 'Bonus')] if x and x != 'NONE'],
                         requires_one_of=re.findall(r'<BonusType>(\w+)</BonusType>', (re.search(r'<PrereqBonuses>(.*?)</PrereqBonuses>', b, re.S) or [None, ''])[1]),
                         free_bonus=one(b, 'FreeBonus'), free_bonus_count=int(one(b, 'iNumFreeBonuses', '0')))
    pre = one(b, 'Bonus')
    if pre in goods: goods[pre]['used_by']['building_requires'].append(ty)
    m = re.search(r'<PrereqBonuses>(.*?)</PrereqBonuses>', b, re.S)
    for g in re.findall(r'<BonusType>(\w+)</BonusType>', m.group(1)) if m else []:
        if g in goods: goods[g]['used_by']['building_requires_one_of'].append(ty)
    fb = one(b, 'FreeBonus')
    if fb in goods: goods[fb]['given_by_buildings'].append(ty)
    for outer, key in (('BonusHealthChanges', 'building_health'), ('BonusHappinessChanges', 'building_happiness'), ('BonusYieldModifiers', 'building_yield'),
                       ('BonusProductionModifiers', 'building_build_speed')):
        m = re.search(r'<%s>(.*?)</%s>' % (outer, outer), b, re.S)
        for g in set(re.findall(r'<BonusType>(\w+)</BonusType>', m.group(1))) if m else []:
            if g in goods: goods[g]['used_by'][key].append(ty)

for b in recs([os.path.join(X, 'Units', 'CIV4UnitInfos.xml')], 'UnitInfo'):
    ty = one(b, 'Type')
    pre = one(b, 'BonusType')
    if pre in goods: goods[pre]['used_by']['unit_requires'].append(ty)
    m = re.search(r'<PrereqBonuses>(.*?)</PrereqBonuses>', b, re.S)
    for g in re.findall(r'<BonusType>(\w+)</BonusType>', m.group(1)) if m else []:
        if g in goods: goods[g]['used_by']['unit_requires_one_of'].append(ty)

CORP = {}
for b in recs([os.path.join(X, 'GameInfo', 'CIV4CorporationInfo.xml')] + mods('*CorporationInfo*.xml'), 'CorporationInfo'):
    ty = one(b, 'Type')
    m = re.search(r'<PrereqBonuses>(.*?)</PrereqBonuses>', b, re.S)
    for g in re.findall(r'<BonusType>(\w+)</BonusType>', m.group(1)) if m else []:
        if g in goods: goods[g]['used_by']['corporation_consumes'].append(ty)
    p = one(b, 'BonusProduced')
    if p in goods:
        goods[p]['used_by']['corporation_produces'].append(ty)
        CORP[ty] = dict(produces=p, consumes=re.findall(r'<BonusType>(\w+)</BonusType>', m.group(1)) if m else [], tech=one(b, 'TechPrereq'))

# building chains
by_cls = {v['cls']: k for k, v in BUILDINGS.items()}


def chain_from(start):
    out = [start]
    while True:
        nxt = [k for k, v in BUILDINGS.items() if BUILDINGS[out[-1]]['cls'] in v['needs'] and 'WONDER' not in k]
        if not nxt: return out
        out.append(sorted(nxt)[0])


chains = dict(essentials=[k for k in ('BUILDING_SETTLEMENT_ESSENTIALS', 'BUILDING_TOWN_ESSENTIALS', 'BUILDING_CITY_ESSENTIALS', 'BUILDING_METROPOLITAN_ESSENTIALS') if k in BUILDINGS],
              market=chain_from('BUILDING_MARKET'))
chain_detail = {k: {b: BUILDINGS[b] for b in v} for k, v in chains.items()}
storage = {k: BUILDINGS[k] for k, v in BUILDINGS.items() if v['food_kept']}
processing = sorted({b for g in goods.values() for key in ('building_requires', 'building_requires_one_of') for b in g['used_by'][key]})

# origins of every good not placed on the map: the buildings, wonders and corporations that give it, with their tech and inputs
origins = {}
for ty, g in goods.items():
    if g['placed']: continue
    givers = [dict(source=bt, kind=BUILDINGS[bt]['kind'], tech=BUILDINGS[bt]['tech'], copies=BUILDINGS[bt]['free_bonus_count'],
                   requires=BUILDINGS[bt]['requires'], requires_one_of=BUILDINGS[bt]['requires_one_of'], cost=BUILDINGS[bt]['cost'])
              for bt in sorted(g['given_by_buildings']) if bt in BUILDINGS]
    givers += [dict(source=ct, kind='corporation', tech=c['tech'], consumes=c['consumes']) for ct, c in sorted(CORP.items()) if c['produces'] == ty]
    origins[ty] = givers

prop_path = os.path.join(HERE, 'proposals.json')
props = json.load(open(prop_path)) if os.path.exists(prop_path) else {}
missing = []
for ty, g in goods.items():
    p = props.get('goods', {}).get(ty)
    if p: g['proposed'] = p
    else: missing.append(ty)
    g['used_by'] = {k: sorted(v) for k, v in g['used_by'].items()}
out = dict(source='mod XML at the checked commit', goods=goods, origins=origins, chains=chain_detail, storage_buildings=storage,
           buildings_requiring_goods=processing, without_proposal=missing)
json.dump(out, open(os.path.join(HERE, 'catalogue.json'), 'w'), indent=1)
print('%d goods (%d placed on the map), %d without a proposal; essentials %s; market %s; %d storage buildings; %d buildings require goods; %d off-map goods without an origin: %s'
      % (len(goods), sum(g['placed'] for g in goods.values()), len(missing), chains['essentials'], chains['market'], len(storage), len(processing),
         sum(1 for v in origins.values() if not v), [k for k, v in origins.items() if not v]))
