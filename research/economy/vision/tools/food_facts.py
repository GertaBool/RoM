#!/usr/bin/env python3
"""The records the food design rests on, read from the mod: the three preservation techs (Pottery, Fermentation,
Refrigeration) with their cost, era, prerequisites, the fewest techs needed to reach each, and every building,
improvement, build, civic and bonus that names them; the buildings that keep food after growth; the growth and
consumption defines; the Normal calendar. Writes data/food_facts.json.
usage: food_facts.py <mod checkout> <out dir>"""
import json, os, re, sys
import xml.etree.ElementTree as ET

MOD, OUT = sys.argv[1], sys.argv[2]
A = os.path.join(MOD, 'Assets', 'XML')
PRES = ['TECH_POTTERY', 'TECH_FERMENTATION', 'TECH_REFRIGERATION']


def records(path, tag):
    txt = open(path, encoding='latin-1').read()
    txt = re.sub(r'\sxmlns="[^"]+"', '', txt, count=1)
    return ET.fromstring(txt.encode('latin-1')).iter(tag)


def one(r, tag, d=None):
    e = r.find(tag)
    return d if e is None or e.text is None else e.text.strip()


def texts(r, path):
    return [e.text.strip() for e in r.findall(path) if e.text]


# techs: cost, era, prerequisites (all of And, one of Or)
T = {}
for r in records(os.path.join(A, 'Technologies', 'CIV4TechInfos.xml'), 'TechInfo'):
    T[one(r, 'Type')] = dict(cost=int(one(r, 'iCost', '0')), era=one(r, 'Era'), and_=texts(r, 'AndPreReqs/PrereqTech'), or_=texts(r, 'OrPreReqs/PrereqTech'))

memo = {}


def fewest(t):
    """The smallest set of techs that must be known to research t, t included (Or prerequisites: the cheapest branch
    by count, ties by name; a set, so shared prerequisites count once)."""
    if t in memo: return memo[t]
    s = {t}
    for p in T[t]['and_']: s |= fewest(p)
    if T[t]['or_']:
        s |= min((fewest(p) for p in T[t]['or_']), key=lambda x: (len(x), sorted(x)))
    memo[t] = frozenset(s)
    return memo[t]


techs = {t: dict(T[t], fewest=len(fewest(t)), fewest_cost=sum(T[x]['cost'] for x in fewest(t))) for t in PRES}

# what names the preservation techs
uses = {t: [] for t in PRES}
B = []
for r in records(os.path.join(A, 'Buildings', 'CIV4BuildingInfos.xml'), 'BuildingInfo'):
    ty = one(r, 'Type'); pre = [one(r, 'PrereqTech')] + texts(r, 'TechTypes/PrereqTech')
    kept = int(one(r, 'iFoodKept', '0'))
    for t in PRES:
        if t in pre:
            uses[t].append(dict(kind='building', type=ty, food_kept=kept, health=int(one(r, 'iHealth', '0')), cost=int(one(r, 'iCost', '0'))))
    if kept:
        B.append(dict(type=ty, tech=one(r, 'PrereqTech'), food_kept=kept, free_start_era=one(r, 'FreeStartEra'), cost=int(one(r, 'iCost', '0')),
                      wonder=one(r, 'BuildingClass', '').startswith('BUILDINGCLASS_') and int(one(r, 'iMaxGlobalInstances', '-1')) == 1))
for path, tag, kind, fields in [(('Terrain', 'CIV4ImprovementInfos.xml'), 'ImprovementInfo', 'improvement', ['PrereqTech']),
                                (('Units', 'CIV4BuildInfos.xml'), 'BuildInfo', 'build', ['PrereqTech', 'ObsoleteTech']),
                                (('GameInfo', 'CIV4CivicInfos.xml'), 'CivicInfo', 'civic', ['TechPrereq']),
                                (('Terrain', 'CIV4BonusInfos.xml'), 'BonusInfo', 'bonus', ['TechReveal', 'TechCityTrade', 'TechObsolete'])]:
    for r in records(os.path.join(A, *path), tag):
        body = ET.tostring(r, encoding='unicode')
        for t in PRES:
            if '>' + t + '<' in body:
                where = [f for f in fields if one(r, f) == t] or ['other field']
                uses[t].append(dict(kind=kind, type=one(r, 'Type'), field=where))

G = {}
for r in records(os.path.join(A, 'GlobalDefines.xml'), 'Define'):
    n = one(r, 'DefineName')
    if n in ('BASE_CITY_GROWTH_THRESHOLD', 'CITY_GROWTH_MULTIPLIER', 'FOOD_CONSUMPTION_PER_POPULATION'): G[n] = int(one(r, 'iDefineIntVal'))

cal = []
for r in records(os.path.join(A, 'GameInfo', 'CIV4GameSpeedInfo.xml'), 'GameSpeedInfo'):
    if one(r, 'Type') == 'GAMESPEED_NORMAL':
        G['growth_percent_normal'] = int(one(r, 'iGrowthPercent'))
        cal = [dict(months=int(one(e, 'iMonthIncrement')), turns=int(one(e, 'iTurnsPerIncrement'))) for e in r.iter('GameTurnInfo')]

salt = None
for r in records(os.path.join(A, 'Terrain', 'CIV4BonusInfos.xml'), 'BonusInfo'):
    if one(r, 'Type') == 'BONUS_SALT':
        salt = dict(reveal=one(r, 'TechReveal'), city_trade=one(r, 'TechCityTrade'), health=int(one(r, 'iHealth', '0')), yields=texts(r, 'YieldChanges/iYieldChange'))
json.dump(dict(techs=techs, uses=uses, food_kept_buildings=B, defines=G, calendar_normal=cal, bonus_salt=salt), open(os.path.join(OUT, 'food_facts.json'), 'w'), indent=1)
for t in PRES: print(t, techs[t]['cost'], techs[t]['era'], 'fewest', techs[t]['fewest'], [(u['kind'], u['type']) for u in uses[t]])
print(G, cal, salt)
print([(b['type'], b['tech'], b['food_kept'], b['free_start_era']) for b in B])
