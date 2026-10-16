#!/usr/bin/env python3
"""Convert a Civ4 BTS WorldBuilder save (Version=11) into the harness's flat
scenario format, read by HH_loadScenario in HarnessHooks.cpp.

The game reads these files with CvWBDesc.py, which ships with the base game and
needs Python. This converter keeps the same content and the same order of
application: map plots first, then teams, players, units and cities.

usage: wbs2scn.py <file.CivBeyondSwordWBSave> <out.scn>

Output: one record per line, fields separated by spaces, type names unchanged
(the DLL resolves them). Missing values are written as -.
  GAME <era> <calendar> <startyear> <gameturn> <maxturns> <speed>
  OPTION <GAMEOPTION_...>            VICTORY <VICTORY_...>
  MAP <w> <h> <wrapX> <wrapY> <worldsize> <climate> <sealevel> <toplat> <botlat>
  TEAM <id> <revealmap>              TECH <team> <TECH_...>
  CONTACT <team> <otherteam>
  PLAYER <id> <team> <civ> <leader> <handicap> <startX> <startY> <gold> <statereligion>
  CIVIC <player> <CIVICOPTION_...> <CIVIC_...>
  PLOT <x> <y> <plottype> <terrain> <feature> <variety> <bonus> <improvement> <route> <NofRiverDir> <WofRiverDir>
  UNIT <owner> <x> <y> <type> <unitai> <level> <experience> <damage> <promotions,comma-separated|->
  CITY <owner> <x> <y> <population> <buildings,|-> <religions,|-> <holyreligions,|->
"""
import re
import sys


def kv(line):
    """Split 'A=1, B=2' (WBS packs several keys on one line) into a dict."""
    out = {}
    for part in line.split(','):
        if '=' in part:
            k, v = part.split('=', 1)
            out[k.strip()] = v.strip()
        elif part.strip():
            out[part.strip()] = ''
    return out


def val(v):
    v = (v or '').strip()
    return v if v and v.upper() != 'NONE' else '-'


def main(src, dst):
    lines = open(src, encoding='latin-1').read().replace('\r', '').split('\n')
    game = {'Era': '-', 'Calendar': '-', 'StartYear': '-', 'GameTurn': '0', 'MaxTurns': '0', 'Speed': '-'}
    options, victories = [], []
    mapinfo = {}
    teams, players, plots, units, cities = [], [], [], [], []
    stack = []
    cur = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith('Begin'):
            sec = line[5:]
            stack.append((sec, cur))
            if sec == 'Team':
                cur = {'Tech': [], 'Contact': []}
                teams.append(cur)
            elif sec == 'Player':
                cur = {'Civic': []}
                players.append(cur)
            elif sec == 'Plot':
                cur = {}
                plots.append(cur)
            elif sec == 'Unit':
                u = {'Promotion': [], 'plot': cur}
                units.append(u)
                cur = u
            elif sec == 'City':
                c = {'Building': [], 'Religion': [], 'Holy': [], 'plot': cur}
                cities.append(c)
                cur = c
            else:
                cur = {}
            continue
        if line.startswith('End'):
            sec, cur = stack.pop() if stack else (None, None)
            continue
        d = kv(line)
        sec = stack[-1][0] if stack else None
        if sec == 'Game':
            for k, v in d.items():
                if k == 'Option':
                    options.append(v)
                elif k == 'Victory':
                    victories.append(v)
                else:
                    game[k] = v
        elif sec == 'Map':
            for k, v in d.items():
                mapinfo[k.replace(' ', '').lower()] = v
        elif sec == 'Team':
            for k, v in d.items():
                if k == 'Tech':
                    cur['Tech'].append(v)
                elif k == 'ContactWithTeam':
                    cur['Contact'].append(v)
                else:
                    cur[k] = v
        elif sec == 'Player':
            if 'CivicOption' in d:
                cur['Civic'].append((d['CivicOption'], d.get('Civic', '')))
            else:
                cur.update(d)
        elif sec == 'Plot':
            cur.update(d)
        elif sec == 'Unit':
            if 'PromotionType' in d:
                cur['Promotion'].append(d['PromotionType'])
            else:
                cur.update(d)
        elif sec == 'City':
            if 'BuildingType' in d:
                cur['Building'].append(d['BuildingType'])
            elif 'ReligionType' in d:
                cur['Religion'].append(d['ReligionType'])
            elif 'HolyCityReligionType' in d:
                cur['Holy'].append(d['HolyCityReligionType'])
            else:
                cur.update(d)

    out = []
    out.append('GAME %s %s %s %s %s %s' % (val(game.get('Era')), val(game.get('Calendar')), val(game.get('StartYear')),
                                           val(game.get('GameTurn')) if game.get('GameTurn') else '0',
                                           game.get('MaxTurns') or '0', val(game.get('Speed'))))
    out += ['OPTION ' + o for o in options]
    out += ['VICTORY ' + v for v in victories]
    m = mapinfo
    out.append('MAP %s %s %s %s %s %s %s %s %s' % (m['gridwidth'], m['gridheight'], m.get('wrapx', '0'), m.get('wrapy', '0'),
                                                   val(m.get('worldsize')), val(m.get('climate')), val(m.get('sealevel')),
                                                   m.get('toplatitude', '90'), m.get('bottomlatitude', '-90')))
    for t in teams:
        tid = t.get('TeamID')
        if tid is None:
            continue
        out.append('TEAM %s %s' % (tid, t.get('RevealMap', '0') or '0'))
        out += ['TECH %s %s' % (tid, x) for x in t['Tech'] if val(x) != '-']
        out += ['CONTACT %s %s' % (tid, x) for x in t['Contact'] if x != tid]
    for i, p in enumerate(players):
        civ, leader = val(p.get('CivType')), val(p.get('LeaderType'))
        if civ == '-' or leader == '-':
            continue
        out.append('PLAYER %d %s %s %s %s %s %s %s %s' % (i, p.get('Team', i), civ, leader, val(p.get('Handicap')),
                                                         p.get('StartingX', '-1') or '-1', p.get('StartingY', '-1') or '-1',
                                                         p.get('StartingGold', '0') or '0', val(p.get('StateReligion'))))
        out += ['CIVIC %d %s %s' % (i, o, c) for o, c in p['Civic'] if val(c) != '-']
    for p in plots:
        x, y = p['x'], p['y']
        nriver = p.get('RiverWEDirection', '-1') if 'isNOfRiver' in p else '-1'
        wriver = p.get('RiverNSDirection', '-1') if 'isWOfRiver' in p else '-1'
        out.append('PLOT %s %s %s %s %s %s %s %s %s %s %s' % (x, y, p.get('PlotType', '3'), val(p.get('TerrainType')),
                                                              val(p.get('FeatureType')), p.get('FeatureVariety', '0') or '0',
                                                              val(p.get('BonusType')), val(p.get('ImprovementType')),
                                                              val(p.get('RouteType')), nriver, wriver))
    for u in units:
        pl = u['plot']
        out.append('UNIT %s %s %s %s %s %s %s %s %s' % (u.get('UnitOwner', '-1'), pl['x'], pl['y'], val(u.get('UnitType')),
                                                        val(u.get('UnitAIType')), u.get('Level', '1') or '1',
                                                        u.get('Experience', '0') or '0', u.get('Damage', '0') or '0',
                                                        ','.join(u['Promotion']) or '-'))
    for c in cities:
        pl = c['plot']
        out.append('CITY %s %s %s %s %s %s %s' % (c.get('CityOwner', '-1'), pl['x'], pl['y'], c.get('CityPopulation', '1') or '1',
                                                  ','.join(c['Building']) or '-', ','.join(c['Religion']) or '-',
                                                  ','.join(c['Holy']) or '-'))
    open(dst, 'w').write('\n'.join(out) + '\n')
    print('%s: %d teams, %d players, %d plots, %d units, %d cities' % (
        dst, sum(1 for l in out if l.startswith('TEAM')), sum(1 for l in out if l.startswith('PLAYER')),
        len(plots), len(units), len(cities)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
