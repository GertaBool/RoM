#!/usr/bin/env python3
"""An upper bound on the food one city can harvest in a turn, from the records, to size the integers that hold tons:
the best plot (terrain, river, hills, feature, the best improvement with irrigation, its bonus yields, every tech and
route change to it, every civic change to it, every building's sea-plot food) times 21 plots, plus every building's
food, times every food modifier of buildings and civics at once. No city reaches it; it bounds what one could.
usage: bounds.py <mod checkout> <economy dir>"""
import json, os, re, sys
import xml.etree.ElementTree as ET

MOD, ROOT = sys.argv[1], sys.argv[2]
A = os.path.join(MOD, 'Assets', 'XML')
F = json.load(open(os.path.join(ROOT, 'data', 'facts.json')))
BC = json.load(open(os.path.join(ROOT, 'settlement', 'data', 'bc.json')))
y0 = lambda v: (v or [0])[0] if v else 0


def records(path, tag):
    txt = re.sub(r'\sxmlns="[^"]+"', '', open(path, encoding='latin-1').read(), count=1)
    return ET.fromstring(txt.encode('latin-1')).iter(tag)


tech_food, route_food = {}, {}
for r in records(os.path.join(A, 'Terrain', 'CIV4ImprovementInfos.xml'), 'ImprovementInfo'):
    ty = r.findtext('Type')
    tech_food[ty] = sum(int((c.findall('TechYields/iYield') or [ET.Element('x')])[0].text or 0) for c in r.findall('TechYieldChanges/TechYieldChange'))
    route_food[ty] = max([int((c.findall('RouteYields/iYield') or [ET.Element('x')])[0].text or 0) for c in r.findall('RouteYieldChanges/RouteYieldChange')] or [0])
terrain = max(y0(t['yields']) + y0(t['river']) for t in F['terrains'])
feature = max([y0(f['yields']) for f in F['features']] + [0])
bonus = max([y0(b['yields']) for b in F['bonuses']] + [0])
civic_imp = max([sum(v[0] for v in c['improvement_yields'].values()) for c in BC['civics']] + [0])
best_imp = max(y0(i['yields']) + y0(i['irrigated']) + max([y0(v) for v in i['bonus_yields'].values()] + [0]) + tech_food.get(i['type'], 0) + route_food.get(i['type'], 0)
               for i in F['improvements'])
sea = sum(max(b['sea'][0], 0) + max(b['global_sea'][0], 0) for b in BC['buildings'])
plot = terrain + feature + bonus + best_imp + civic_imp + sea
bld_food = sum(max(b['yield_change'][0], 0) for b in BC['buildings'])
mod = sum(max(b['yield_mod'][0], 0) for b in BC['buildings']) + sum(max(c['yield_mod'][0], 0) for c in BC['civics'])
city_food = (21 * plot + bld_food) * (100 + mod) // 100
out = dict(plot_parts=dict(terrain_river=terrain, feature=feature, bonus=bonus, improvement=best_imp, civic=civic_imp, building_sea=sea),
           plot=plot, building_food=bld_food, modifier_percent=mod, city_food=city_food, city_tons=city_food * 100,
           int32_max=2**31 - 1, int64_max=2**63 - 1)
json.dump(out, open(os.path.join(ROOT, 'vision', 'data', 'bounds.json'), 'w'), indent=1)
print(out)
