#!/usr/bin/env python3
"""What RoM's buildings and civics do to a city's food, production, commerce, growth and trade, from
CIV4BuildingInfos.xml and CIV4CivicInfos.xml. Writes data/bc.json.
usage: bc.py <mod checkout> <settlement dir>"""
import collections, json, os, re, sys

mod, root = sys.argv[1:3]
X = os.path.join(mod, 'Assets', 'XML')


def recs(path, tag):
    return re.findall(r'<%s>.*?</%s>' % (tag, tag), open(path, encoding='latin-1').read(), re.S)


def one(r, tag, d=None):
    m = re.search(r'<%s>([^<]*)</%s>' % (tag, tag), r)
    return m.group(1).strip() if m else d


def vec(r, outer, inner, n):
    m = re.search(r'<%s>(.*?)</%s>' % (outer, outer), r, re.S)
    v = [int(x) for x in re.findall(r'<%s>(-?\d+)</%s>' % (inner, inner), m.group(1))] if m else []
    return (v + [0] * n)[:n]


B = []
for r in recs(os.path.join(X, 'Buildings', 'CIV4BuildingInfos.xml'), 'BuildingInfo'):
    B.append(dict(type=one(r, 'Type'), cls=one(r, 'BuildingClass'), cost=int(one(r, 'iCost', '0')), tech=one(r, 'PrereqTech'),
                  yield_change=vec(r, 'YieldChanges', 'iYield', 3), yield_mod=vec(r, 'YieldModifiers', 'iYield', 3),
                  sea=vec(r, 'SeaPlotYieldChanges', 'iYield', 3), river=vec(r, 'RiverPlotYieldChanges', 'iYield', 3),
                  global_sea=vec(r, 'GlobalSeaPlotYieldChanges', 'iYield', 3), commerce_mod=vec(r, 'CommerceModifiers', 'iCommerce', 4),
                  commerce_change=vec(r, 'CommerceChanges', 'iCommerce', 4), food_kept=int(one(r, 'iFoodKept', '0')),
                  trade_routes=int(one(r, 'iTradeRoutes', '0')), trade_mod=int(one(r, 'iTradeRouteModifier', '0')),
                  foreign_trade_mod=int(one(r, 'iForeignTradeRouteModifier', '0')), health=int(one(r, 'iHealth', '0')),
                  happy=int(one(r, 'iHappiness', '0')), power=one(r, 'bPower') == '1',
                  power_mod=vec(r, 'PowerYieldModifiers', 'iYield', 3), area_mod=vec(r, 'AreaYieldModifiers', 'iYield', 3),
                  global_mod=vec(r, 'GlobalYieldModifiers', 'iYield', 3),
                  bonus_mods=len(re.findall(r'<BonusYieldModifier>', r)),
                  specialists=sum(int(x) for x in re.findall(r'<iSpecialistCount>(\d+)</iSpecialistCount>', r)),
                  free_specialist=int(one(r, 'iFreeSpecialist', '0')),
                  is_wonder=bool(re.search(r'<iMaxGlobalInstances>1<|<iMaxPlayerInstances>1<', r))))
CV = []
for r in recs(os.path.join(X, 'GameInfo', 'CIV4CivicInfos.xml'), 'CivicInfo'):
    iy = re.findall(r'<ImprovementYieldChange>(.*?)</ImprovementYieldChange>', r, re.S)
    imp = {}
    for s in iy:
        k = one(s, 'ImprovementType'); y = [int(x) for x in re.findall(r'<iYield>(-?\d+)</iYield>', s)]
        if k and any(y): imp[k] = (y + [0, 0, 0])[:3]
    CV.append(dict(type=one(r, 'Type'), option=one(r, 'CivicOptionType'), tech=one(r, 'TechPrereq'),
                   yield_mod=vec(r, 'YieldModifiers', 'iYield', 3), capital_yield_mod=vec(r, 'CapitalYieldModifiers', 'iYield', 3),
                   trade_yield_mod=vec(r, 'TradeYieldModifiers', 'iYield', 3), commerce_mod=vec(r, 'CommerceModifiers', 'iCommerce', 4),
                   capital_commerce_mod=vec(r, 'CapitalCommerceModifiers', 'iCommerce', 4), improvement_yields=imp,
                   trade_routes=int(one(r, 'iTradeRoutes', '0')), no_foreign_trade=one(r, 'bNoForeignTrade') == '1',
                   health=int(one(r, 'iExtraHealth', '0')), happy=int(one(r, 'iHappinessChange', '0') or 0),
                   worker_speed=int(one(r, 'iWorkerSpeedModifier', '0')), upgrade_rate=int(one(r, 'iImprovementUpgradeRateModifier', '0')),
                   military_food=one(r, 'bMilitaryFoodProduction') == '1', free_specialist=int(one(r, 'iFreeSpecialist', '0')),
                   largest_city_happy=int(one(r, 'iLargestCityHappiness', '0'))))
json.dump(dict(buildings=B, civics=CV), open(os.path.join(root, 'data', 'bc.json'), 'w'))

nb = [b for b in B if not b['is_wonder']]
count = lambda pred: sum(1 for b in nb if pred(b))
summary = collections.OrderedDict([
    ('buildings', len(B)), ('ordinary', len(nb)),
    ('flat food', count(lambda b: b['yield_change'][0] > 0)), ('food %', count(lambda b: b['yield_mod'][0] > 0)),
    ('sea plot food', count(lambda b: b['sea'][0] > 0)), ('river plot yields', count(lambda b: any(b['river']))),
    ('food kept', count(lambda b: b['food_kept'] > 0)),
    ('flat production', count(lambda b: b['yield_change'][1] > 0)), ('production %', count(lambda b: b['yield_mod'][1] > 0)),
    ('power production %', count(lambda b: b['power_mod'][1] > 0)), ('commerce %', count(lambda b: b['yield_mod'][2] > 0)),
    ('gold or research %', count(lambda b: b['commerce_mod'][0] > 0 or b['commerce_mod'][1] > 0)),
    ('trade routes', count(lambda b: b['trade_routes'] > 0)), ('trade route %', count(lambda b: b['trade_mod'] > 0 or b['foreign_trade_mod'] > 0)),
    ('health', count(lambda b: b['health'] > 0)), ('happiness', count(lambda b: b['happy'] > 0)),
    ('bonus yield %', count(lambda b: b['bonus_mods'] > 0)), ('specialist slots', count(lambda b: b['specialists'] > 0)),
])
print(json.dumps(summary))
print('civics', len(CV), 'yield %', sum(1 for c in CV if any(c['yield_mod'])), 'trade yield', sum(1 for c in CV if any(c['trade_yield_mod'])),
      'improvement yields', sum(1 for c in CV if c['improvement_yields']), 'trade routes', sum(1 for c in CV if c['trade_routes']),
      'no foreign trade', [c['type'] for c in CV if c['no_foreign_trade']])
