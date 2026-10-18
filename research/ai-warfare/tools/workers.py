#!/usr/bin/env python3
"""Worker figures for one game, into a figure registry (tools/figlib.py).

usage: workers.py <game dir> <human id> <state0.json> <records.json> <CvEnums.h> <out.fig.json>
"""
import csv, json, os, re, statistics as st, sys

sys.path.insert(0, os.path.dirname(__file__))
from figlib import Registry

G, H, DUMP, REC, ENUMS, OUT = sys.argv[1:7]
rd = lambda f: list(csv.DictReader(open(os.path.join(G, f + '.csv'), newline='')))
C, TI = rd('human_commands'), rd('tiles')
R = json.load(open(REC)); d = json.load(open(DUMP))
T = d['turn']
reg = Registry(OUT, [os.path.join(G, 'human_commands.csv'), os.path.join(G, 'tiles.csv'), DUMP, REC, ENUMS], R)
who = f'human (player {H})'
F = lambda c: c['fields'].split('|')
span = lambda rows: f"{min(int(r['turn']) for r in rows)}-{max(int(r['turn']) for r in rows)}"

# orders
B = [dict(turn=c['turn'], unit=F(c)[0], xy=(F(c)[1], F(c)[2]), build=F(c)[5]) for c in C
     if c['kind'] == 'MISSION' and F(c)[4] == 'MISSION_BUILD']
reg.census_table('builds', B, 'build', 'orders', who, span(B), 'A lines MISSION_BUILD (human_commands.csv)',
                 group='unit', xml='BuildInfo')
seen, D = set(), []
for b in B:
    if (b['xy'], b['build']) not in seen: seen.add((b['xy'], b['build'])); D.append(b)
reg.census_table('builds_distinct', D, 'build', 'distinct plots', who, span(B),
                 'A lines MISSION_BUILD, first order per plot and build')
RT = [dict(turn=c['turn'], unit=F(c)[0]) for c in C if c['kind'] == 'MISSION' and F(c)[4] == 'MISSION_ROUTE_TO']
reg.census_table('route_to', RT, 'unit', 'orders', who, span(RT), 'A lines MISSION_ROUTE_TO')
src = open(ENUMS).read()
names = re.findall(r'\b(AUTOMATE_\w+)', src[src.index('enum AutomateTypes'):src.index('NUM_AUTOMATE_TYPES')])
AU = [dict(turn=c['turn'], unit=F(c)[0], type=names[int(F(c)[5])]) for c in C if c['kind'] == 'COMMAND' and F(c)[4] == 'COMMAND_AUTOMATE']
reg.census_table('automate', AU, 'unit', 'orders', who, span(AU), 'A lines COMMAND_AUTOMATE; type from CvEnums.h AutomateTypes',
                 group='type')

# improvements at the save, every tile (land and water)
for r in TI: r['where'] = r['group'] + (' worked' if r['worked'] == '1' else ' unworked')
gs = [g + w for g in ('human_founded', 'human_captured', 'ai') for w in (' worked', ' unworked')]
reg.census_table('impr', TI, 'improvement', 'tiles at save', 'all players', f'save {T}', 'tiles.csv (save dump)',
                 group='where', groups=gs, xml='ImprovementInfo')
W = [r for r in TI if r['worked'] == '1']
for y, u in (('food', 'food per tile'), ('hammers', 'hammers per tile'), ('commerce', 'commerce per tile')):
    reg.census_table(f'yield_{y}', W, 'improvement', u, 'all players', f'save {T}', 'tiles.csv, worked tiles',
                     group='group', groups=['human_founded', 'human_captured', 'ai'],
                     value=lambda s, y=y: st.mean(int(r[y]) for r in s), fmt='{:.2f}', stat='mean')

# the rules: work rate, build time, upgrade time and rate (code cited in each source)
for u in sorted({b['unit'] for b in B}):
    reg.fig(f'workrate_{u}', R['UnitInfo']['UNIT_' + u]['iWorkRate'], 'xml', u, 'fixed', f'UnitInfo UNIT_{u} iWorkRate')
speed = R['GameSpeedInfo']['GAMESPEED_MARATHON']; era = R['EraInfo']['ERA_ANCIENT']
reg.fig('build_pct', speed['iBuildPercent'], 'xml', 'all', 'fixed', 'GameSpeedInfo MARATHON iBuildPercent (CvPlot::getBuildTime)')
reg.fig('upgrade_pct', speed['iImprovementPercent'], 'xml', 'all', 'fixed', 'GameSpeedInfo MARATHON iImprovementPercent (CvGame::getImprovementUpgradeTime)')
h = R['HandicapInfo']['HANDICAP_MONARCH']['iAIWorkRateModifier']
reg.fig('ai_workrate_mod', h, 'xml', 'AI players', 'fixed', 'HandicapInfo MONARCH iAIWorkRateModifier, game handicap (CvUnit::workRate)')
k, chain = 'IMPROVEMENT_COTTAGE', []
while k and k != 'NONE' and k in R['ImprovementInfo']:
    rec = R['ImprovementInfo'][k]; t = rec['iUpgradeTime']
    if rec.get('ImprovementUpgrade') not in (None, '', 'NONE'):
        n = k[12:]
        chain.append(n)
        reg.fig(f'upgrade_turns_{n}', t * speed['iImprovementPercent'] // 100 * era['iImprovementPercent'] // 100,
                'derived xml', 'all', 'fixed', f'{k} iUpgradeTime {t} x Marathon and Ancient iImprovementPercent '
                '(CvGame::getImprovementUpgradeTime); progress grows only while the tile is worked (CvPlot::doImprovementUpgrade)')
    else:
        chain.append(k[12:])
    k = rec.get('ImprovementUpgrade')
reg.fig('cottage_chain', ' > '.join(chain), 'xml', 'all', 'fixed', 'ImprovementInfo ImprovementUpgrade')
setters = sorted({t for t, tab in R.items() for v in tab.values() if v.get('iImprovementUpgradeRateModifier')})
reg.fig('rate_setters', ', '.join(setters), 'xml', 'all', 'fixed', 'records.json, every record type, iImprovementUpgradeRateModifier set')
P = {str(p['id']): p for p in d['players']}
mod = lambda p: sum(R['CivicInfo'][c].get('iImprovementUpgradeRateModifier') or 0 for c in p['civics'])
reg.fig('rate_mod_human', mod(P[H]), 'xml', who, f'save {T}', 'civics in force (save dump) x CivicInfo iImprovementUpgradeRateModifier')
reg.fig('rate_human', 1 * (100 + mod(P[H])) // 100, 'derived xml', who, f'save {T}',
        'CvPlayer::getImprovementUpgradeRate: 1 x (100 + modifier) / 100, integer division')
ai = [p for k2, p in P.items() if k2 != H and p['cities']]
reg.fig('rate_ai_above1', sum(1 for p in ai if (100 + mod(p)) // 100 > 1), 'derived xml', 'AI players with cities',
        f'save {T}', 'same rule, AI civics in force', n=len(ai))
reg.fig('n_ai', len(ai), 'xml', 'AI players with cities', f'save {T}', 'save dump')
reg.save()
