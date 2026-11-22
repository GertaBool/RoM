#!/usr/bin/env python3
"""A small WorldBuilder scenario for the headless harness (toolchain/harness, HH_loadScenario), to run the
debt build and its base against each other: one continent, six AI civilizations with two cities each,
all in contact, so that markets, loans between civilizations, wars and defaults can arise.

usage: make_scenario.py <mod Assets dir> <out.scn>
The map is fixed (no randomness): the runs differ only by HARNESS_RESEED.
"""
import re, sys

assets, out = sys.argv[1], sys.argv[2]
civ_xml = open(assets + '/XML/Civilizations/CIV4CivilizationInfos.xml', encoding='latin-1').read()
pairs = []
for block in re.findall(r'<CivilizationInfo>(.*?)</CivilizationInfo>', civ_xml, re.S):
    t = re.search(r'<Type>(CIVILIZATION_\w+)</Type>', block)
    playable = re.search(r'<bPlayable>1</bPlayable>', block)
    leader = re.search(r'<LeaderName>(LEADER_\w+)</LeaderName>', block)
    if t and playable and leader:
        pairs.append((t.group(1), leader.group(1)))
pairs = pairs[:6]
# Every team starts with the techs of the first era: without them the harness's AI economies sat at
# zero gold in both builds (seen in the first runs), which would leave debt nothing to act on.
tech_xml = open(assets + '/XML/Technologies/CIV4TechInfos.xml', encoding='latin-1').read()
techs = [re.search(r'<Type>(TECH_\w+)</Type>', b).group(1) for b in re.findall(r'<TechInfo>(.*?)</TechInfo>', tech_xml, re.S)
         if re.search(r'<Era>ERA_ANCIENT</Era>', b) and re.search(r'<Type>(TECH_\w+)</Type>', b)]
assert len(pairs) == 6, pairs

W, H = 52, 34
lines = ['GAME ERA_ANCIENT CALENDAR_DEFAULT -4000 0 0 GAMESPEED_NORMAL',
         'OPTION GAMEOPTION_NO_REVOLUTION', 'OPTION GAMEOPTION_NO_BARBARIAN_CIV', 'OPTION GAMEOPTION_NO_TECH_DIFFUSION',
         'VICTORY VICTORY_CONQUEST', 'VICTORY VICTORY_DOMINATION',
         'MAP %d %d 0 0 WORLDSIZE_SMALL CLIMATE_TEMPERATE SEALEVEL_MEDIUM 70 -70' % (W, H)]
# plot types: 0 peak, 1 hills, 2 land, 3 ocean
def land(x, y):
    return 3 <= x < W - 3 and 3 <= y < H - 3 and not (x in (25, 26) and 10 <= y <= 23)
for y in range(H):
    for x in range(W):
        if land(x, y):
            h = (x * 7 + y * 13) % 17
            ptype = 1 if h == 0 else 2
            terrain = 'TERRAIN_PLAINS' if (x + 2 * y) % 5 == 0 else 'TERRAIN_GRASS'
            feature = 'FEATURE_FOREST' if (x * 3 + y * 5) % 11 == 0 else '-'
            lines.append('PLOT %d %d %d %s %s 0 - - - -1 -1' % (x, y, ptype, terrain, feature))
        else:
            near = any(land(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            lines.append('PLOT %d %d 3 %s - 0 - - - -1 -1' % (x, y, 'TERRAIN_COAST' if near else 'TERRAIN_OCEAN'))
starts = [(7, 8), (18, 8), (33, 8), (44, 8), (12, 25), (39, 25)]
seconds = [(7, 15), (18, 15), (33, 15), (44, 15), (12, 18), (39, 18)]
for i, ((civ, leader), (sx, sy)) in enumerate(zip(pairs, starts)):
    lines.append('TEAM %d 0' % i)
    lines.append('PLAYER %d %d %s %s - %d %d 300 -' % (i, i, civ, leader, sx, sy))
    for t in techs:
        lines.append('TECH %d %s' % (i, t))
for i in range(6):
    for j in range(6):
        if i != j:
            lines.append('CONTACT %d %d' % (i, j))
for i, ((sx, sy), (tx, ty)) in enumerate(zip(starts, seconds)):
    lines.append('CITY %d %d %d 6 - - -' % (i, sx, sy))
    lines.append('CITY %d %d %d 4 - - -' % (i, tx, ty))
    for unit, ai in (('UNIT_WARRIOR', 'UNITAI_CITY_DEFENSE'), ('UNIT_WARRIOR', 'UNITAI_CITY_DEFENSE'),
                     ('UNIT_ARCHER', 'UNITAI_CITY_DEFENSE'), ('UNIT_WORKER', 'UNITAI_WORKER'),
                     ('UNIT_SETTLER', 'UNITAI_SETTLE')):
        lines.append('UNIT %d %d %d %s %s 1 0 0 -' % (i, sx, sy, unit, ai))
open(out, 'w').write('\n'.join(lines) + '\n')
print('%s: %d players, %dx%d' % (out, len(pairs), W, H))
