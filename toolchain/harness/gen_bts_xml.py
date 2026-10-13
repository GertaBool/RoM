#!/usr/bin/env python3
"""Provide the Beyond the Sword XML files that Rise of Mankind does not ship.

The game resolves these from the base game install, which the harness does not
have. Files whose entry count is bound to a DLL enum are generated from the
mod's own CvEnums.h, so the indices match exactly. Interface, camera and art
lists get one inert entry. Files with gameplay numbers that AdvCiv carries
unmodified from BTS (goodies, hurries, sea levels, vote sources, landscapes)
are copied from AdvCiv. Upkeep percentages are placeholders: they only scale
civic gold costs, not unit movement or settlement.
usage: gen_bts_xml.py <CvGameCoreDLL dir> <advciv xml dir> <out XML dir>
"""
import os, re, sys, shutil

dll, advciv, out = sys.argv[1:4]
enums_src = re.sub(r'//[^\n]*', '', open(os.path.join(dll, 'CvEnums.h'), errors='replace').read())

def enum(name):
    m = re.search(r'enum\s+(?:DllExport\s+)?' + name + r'\s*\{(.*?)\}', enums_src, re.S)
    items = []
    for x in re.sub(r'#\w+[^\n]*', '', m.group(1)).split(','):
        x = x.strip().split('=')[0].strip()
        if x and not x.startswith('NO_') and not x.startswith('NUM_'):
            items.append(x)
    return items

loader = open(os.path.join(dll, 'CvXMLLoadUtilitySet.cpp'), errors='replace').read()
xpaths = {}
for m in re.finditer(r'LoadGlobalClassInfo\([^,]+,\s*"(\w+)",\s*"(\w+)",\s*"([\w/]+)"', loader):
    xpaths[(m.group(2), m.group(1))] = m.group(3)

def write(folder, fname, entries, extra=lambda t: '', typed=True):
    parts = xpaths[(folder, fname)].split('/')
    body = ''.join('\t\t<%s>\n%s\t\t\t<Description>TXT_KEY_%s</Description>\n%s\t\t</%s>\n'
                   % (parts[-1], ('\t\t\t<Type>%s</Type>\n' % t) if typed else '', t, extra(t), parts[-1]) for t in entries)
    os.makedirs(os.path.join(out, folder), exist_ok=True)
    for tag in reversed(parts[:-1]):
        body = '<%s>\n%s</%s>\n' % (tag, body, tag)
    with open(os.path.join(out, folder, fname + '.xml'), 'w') as f:
        f.write('<?xml version="1.0"?>\n' + body)

copied = [('GameInfo', 'CIV4GoodyInfo'), ('GameInfo', 'CIV4HurryInfo'), ('GameInfo', 'CIV4SeaLevelInfo'),
          ('GameInfo', 'CIV4VoteSourceInfos'), ('Terrain', 'CIV4TerrainSettings')]
for folder, fname in copied:
    os.makedirs(os.path.join(out, folder), exist_ok=True)
    shutil.copy(os.path.join(advciv, folder, fname + '.xml'), os.path.join(out, folder, fname + '.xml'))

write('BasicInfos', 'CIV4UnitAIInfos', enum('UnitAITypes'))
write('BasicInfos', 'CIV4DomainInfos', enum('DomainTypes'))
write('BasicInfos', 'CIV4AttitudeInfos', enum('AttitudeTypes'))
write('BasicInfos', 'CIV4DenialInfos', enum('DenialTypes'))
write('BasicInfos', 'CIV4CalendarInfos', enum('CalendarTypes'))
write('BasicInfos', 'CIV4CityTabInfos', enum('CityTabTypes'))
write('BasicInfos', 'CIV4BasicInfos', ['CONCEPT_HARNESS'])
write('BasicInfos', 'CIV4SeasonInfos', ['SEASON_WINTER', 'SEASON_SPRING', 'SEASON_SUMMER', 'SEASON_AUTUMN'])
write('BasicInfos', 'CIV4MonthInfos', ['MONTH_%d' % i for i in range(1, 13)])
write('GameInfo', 'CIV4ForceControlInfos', enum('ForceControlTypes'))
write('GameInfo', 'CIV4MPOptionInfos', enum('MultiplayerOptionTypes') if 'MultiplayerOptionTypes' in enums_src else
      ['MPOPTION_SIMULTANEOUS_TURNS', 'MPOPTION_TAKEOVER_AI', 'MPOPTION_SHUFFLE_TEAMS', 'MPOPTION_ANONYMOUS', 'MPOPTION_TURN_TIMER'])
write('GameInfo', 'CIV4PlayerOptionInfos', enum('PlayerOptionTypes'), lambda t: '\t\t\t<bDefault>0</bDefault>\n')
write('GameInfo', 'CIV4GraphicOptionInfos', enum('GraphicOptionTypes'), lambda t: '\t\t\t<bDefault>0</bDefault>\n')
write('GameInfo', 'CIV4ClimateInfo', ['CLIMATE_TEMPERATE'])
cursors = set(['CURSOR_DEFAULT'])
for top in ('XML',):
    for d, _, files in os.walk(os.path.join(os.path.dirname(dll.rstrip('/')), top)):
        for f in files:
            if f.lower().endswith('.xml'):
                cursors.update(re.findall(r'CURSOR_[A-Z_]+', open(os.path.join(d, f), errors='replace').read()))
write('GameInfo', 'CIV4CursorInfo', sorted(cursors))
write('GameInfo', 'CIV4TurnTimerInfo', ['TURNTIMER_STATIC', 'TURNTIMER_SNAIL', 'TURNTIMER_SLOW', 'TURNTIMER_MEDIUM',
                                        'TURNTIMER_FAST', 'TURNTIMER_BLAZING'])
write('GameInfo', 'CIV4EmphasizeInfo', ['EMPHASIZE_AVOID_GROWTH', 'EMPHASIZE_FOOD', 'EMPHASIZE_PRODUCTION', 'EMPHASIZE_COMMERCE',
                                        'EMPHASIZE_GOLD', 'EMPHASIZE_RESEARCH', 'EMPHASIZE_CULTURE', 'EMPHASIZE_GREAT_PEOPLE'])
upkeep = {'UPKEEP_LOW': (5, 50), 'UPKEEP_MEDIUM': (10, 100), 'UPKEEP_HIGH': (15, 150)}
write('GameInfo', 'CIV4UpkeepInfo', ['UPKEEP_LOW', 'UPKEEP_MEDIUM', 'UPKEEP_HIGH'],
      lambda t: '\t\t\t<iPopulationPercent>%d</iPopulationPercent>\n\t\t\t<iCityPercent>%d</iCityPercent>\n' % upkeep[t])
write('Interface', 'CIV4AdvisorInfos', ['ADVISOR_MILITARY', 'ADVISOR_RELIGION', 'ADVISOR_ECONOMY', 'ADVISOR_SCIENCE',
                                        'ADVISOR_CULTURE', 'ADVISOR_GROWTH'])
for folder, fname in [('Interface', 'CIV4CameraInfos'), ('Interface', 'CIV4SlideShowInfos'), ('Interface', 'CIV4SlideShowRandomInfos'),
                      ('Interface', 'CIV4ThroneRoomCameraInfos'), ('Interface', 'CIV4ThroneRoomInfos'),
                      ('Interface', 'CIV4ThroneRoomStyleInfos'), ('Interface', 'Civ4SpaceShipInfos'),
                      ('Misc', 'CIV4AttachableInfos'), ('Misc', 'CIV4CameraOverlayInfos'), ('Misc', 'CIV4RiverInfos'),
                      ('Misc', 'CIV4TerrainPlaneInfos'), ('Misc', 'CIV4WaterPlaneInfos'), ('Misc', 'Civ4QuestInfos'),
                      ('Misc', 'Civ4TutorialInfos'), ('Art', 'CIV4RiverModelInfos'), ('Units', 'CIV4AnimationInfos')]:
    write(folder, fname, [fname.upper().replace('CIV4', '') + '_HARNESS'])
write('Units', 'CIV4AnimationPathInfos', enum('AnimationPathTypes'))
write('Units', 'CIV4AutomateInfos', enum('AutomateTypes'),
      lambda t: '\t\t\t<Command>COMMAND_AUTOMATE</Command>\n\t\t\t<Automate>%s</Automate>\n\t\t\t<bVisible>1</bVisible>\n' % t,
      typed=False)   # as in BTS: automate infos are indexed by AutomateTypes, not by a Type tag
# Entity events are named by the mod's build and formation infos.
assets = os.path.dirname(dll.rstrip('/'))
events = set()
for top in ('XML', 'Modules'):
    for d, _, files in os.walk(os.path.join(assets, top)):
        for f in files:
            if f.lower().endswith('.xml'):
                events.update(re.findall(r'ENTITY_EVENT_[A-Z_]+', open(os.path.join(d, f), errors='replace').read()))
write('Units', 'CIV4EntityEventInfos', sorted(events))
write('Units', 'CIV4CommandInfos', enum('CommandTypes'))
write('Units', 'CIV4ControlInfos', enum('ControlTypes'))
n = sum(len(f) for _, _, f in os.walk(out))
print(n, 'files in', out)
