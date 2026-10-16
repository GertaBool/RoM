#!/usr/bin/env python3
"""War personality of every loaded leader (Assets/XML and loaded Modules; later files override).
usage: leaders.py <Assets dir>"""
import os, sys, statistics
import xml.etree.ElementTree as ET
A = sys.argv[1]
st = lambda t: t.split('}', 1)[-1]
L, civs = {}, {}
for p, _, fs in sorted(os.walk(A)):
    if 'Unloaded Modules' in p:
        continue
    for f in sorted(fs):
        if 'chema' in f or not f.endswith('.xml'):
            continue
        if f.endswith('LeaderHeadInfos.xml'):
            for e in ET.parse(os.path.join(p, f)).getroot().iter():
                if st(e.tag) != 'LeaderHeadInfo':
                    continue
                d = {st(k.tag): k for k in e}
                rec = L.setdefault((d['Type'].text or '').strip(), {})
                for k, v in d.items():
                    if list(v):
                        items = []
                        for g in v:
                            ks = [(x.text or '').strip() for x in g]
                            if ks and ks[-1] not in ('0', '', 'NONE'):
                                items.append(':'.join(ks))
                            elif not list(g) and (g.text or '').strip() not in ('', '0', 'NONE'):
                                items.append((g.text or '').strip())
                        if items:
                            rec[k] = items
                    elif (v.text or '').strip():
                        rec[k] = (v.text or '').strip()
        elif f.endswith('CivilizationInfos.xml'):
            for e in ET.parse(os.path.join(p, f)).getroot().iter():
                if st(e.tag) == 'CivilizationInfo':
                    d = {st(k.tag): k for k in e}
                    c = (d['Type'].text or '').strip()
                    if 'Leaders' in d:
                        for g in d['Leaders']:
                            ks = [(x.text or '').strip() for x in g]
                            if ks and ks[0].startswith('LEADER_'):
                                civs.setdefault(ks[0], set()).add(c.replace('CIVILIZATION_', ''))
L.pop('LEADER_BARBARIAN', None)
F = ['iBaseAttackOddsChange', 'iAttackOddsChangeRand', 'iBuildUnitProb', 'iMaxWarRand', 'iLimitedWarRand', 'iDogpileWarRand',
     'iMakePeaceRand', 'iMaxWarNearbyPowerRatio', 'iMaxWarDistantPowerRatio', 'iMaxWarMinAdjacentLandPercent',
     'iLimitedWarPowerRatio', 'iRazeCityProb', 'iWarmongerRespect', 'iBasePeaceWeight', 'iConquestVictoryWeight',
     'iDominationVictoryWeight', 'iDeclareWarTradeRand']
print('leaders', len(L), 'with a civilization', sum(1 for k in L if k in civs))
for f in F:
    vals = [int(v.get(f, '0')) for v in L.values()]
    print('%-34s min %5d median %7.1f max %5d' % (f, min(vals), statistics.median(vals), max(vals)))
for f in ['DeclareWarRefuseAttitudeThreshold', 'DeclareWarThemRefuseAttitudeThreshold']:
    c = {}
    for v in L.values():
        c[v.get(f, '?')] = c.get(v.get(f, '?'), 0) + 1
    print(f, c)
print('\nleader | civ | traits | odds+rand | buildUnit | maxWar | limWar | dogpile | peace | nearPR | distPR | adjLand | limPR | raze | conq/dom | flavors | unitAI weights | NoWarAttitudeProbs')
for k, v in sorted(L.items()):
    g = lambda f: v.get(f, '0')
    print(' | '.join([k.replace('LEADER_', ''), ','.join(sorted(civs.get(k, {'-'}))),
          ','.join(x.replace('TRAIT_', '')[:4] for x in v.get('Traits', [])), g('iBaseAttackOddsChange') + '+' + g('iAttackOddsChangeRand'),
          g('iBuildUnitProb'), g('iMaxWarRand'), g('iLimitedWarRand'), g('iDogpileWarRand'), g('iMakePeaceRand'),
          g('iMaxWarNearbyPowerRatio'), g('iMaxWarDistantPowerRatio'), g('iMaxWarMinAdjacentLandPercent'), g('iLimitedWarPowerRatio'),
          g('iRazeCityProb'), g('iConquestVictoryWeight') + '/' + g('iDominationVictoryWeight'),
          ','.join(x.replace('FLAVOR_', '') for x in v.get('Flavors', [])),
          ','.join(x.replace('UNITAI_', '') for x in v.get('UnitAIWeightModifiers', [])),
          ','.join(x.replace('ATTITUDE_', '') for x in v.get('NoWarAttitudeProbs', []))]))
