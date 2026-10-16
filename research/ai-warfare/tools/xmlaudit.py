#!/usr/bin/env python3
"""Audit RoM's combat-relevant XML: land units (base file and every loaded module),
promotions, buildings' defence, combat defines. Reads only.
usage: xmlaudit.py <Assets dir> <out.md>"""
import os, re, sys, collections

A = sys.argv[1]
OUT = sys.argv[2]


def read(p):
    return open(p, encoding='latin-1').read()


def blocks(s, tag):
    return re.findall(r'<%s>(.*?)</%s>' % (tag, tag), s, re.S)


def scalar(b, tag, default=None):
    m = re.search(r'<%s>([^<]*)</%s>' % (tag, tag), b)
    return m.group(1).strip() if m else default


def num(b, tag):
    v = scalar(b, tag, '0')
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return 0


# --- techs -> era ---
techs = {}
for p, _, fs in os.walk(A):
    for f in fs:
        if f.endswith('TechInfos.xml'):
            for b in blocks(read(os.path.join(p, f)), 'TechInfo'):
                t = scalar(b, 'Type')
                if t:
                    techs[t] = scalar(b, 'Era', 'NONE').replace('C2C_ERA_', '').replace('ERA_', '')

# --- loaded module dirs (MLF) ---
def loaded(dirpath):
    """True unless an MLF control file in an ancestor switches this directory off."""
    rel = os.path.relpath(dirpath, os.path.join(A, 'Modules'))
    if rel.startswith('..'):
        return True
    parts = rel.split(os.sep)
    base = os.path.join(A, 'Modules')
    for part in parts:
        mlf = os.path.join(base, 'MLF_CIV4ModularLoadingControls.xml')
        if os.path.exists(mlf):
            s = read(mlf)
            for d, l in re.findall(r'<Directory>([^<]*)</Directory>\s*<bLoad>([^<]*)</bLoad>', s):
                if d == part and l.strip() == '0':
                    return False
        base = os.path.join(base, part)
    return True

units = collections.OrderedDict()
sources = {}
for p, _, fs in sorted(os.walk(A)):
    for f in sorted(fs):
        if not f.endswith('UnitInfos.xml') or 'Special' in f:
            continue
        if not loaded(p):
            continue
        src = os.path.relpath(os.path.join(p, f), A)
        for b in blocks(read(os.path.join(p, f)), 'UnitInfo'):
            t = scalar(b, 'Type')
            if not t:
                continue
            if t in units:
                sources[t] += ' + ' + src
            else:
                sources[t] = src
            units[t] = b

rows = []
for t, b in units.items():
    if scalar(b, 'Domain') != 'DOMAIN_LAND':
        continue
    combat = num(b, 'iCombat')
    if combat <= 0:
        continue
    u = {
        'type': t.replace('UNIT_', ''), 'class': (scalar(b, 'Class') or '').replace('UNITCLASS_', ''),
        'combat_type': (scalar(b, 'Combat') or 'NONE').replace('UNITCOMBAT_', ''),
        'era': techs.get(scalar(b, 'PrereqTech', 'NONE'), '?'), 'tech': (scalar(b, 'PrereqTech') or '').replace('TECH_', ''),
        'str': combat, 'moves': num(b, 'iMoves'), 'cost': num(b, 'iCost'), 'power': num(b, 'iPower'),
        'fs': num(b, 'iFirstStrikes'), 'cfs': num(b, 'iChanceFirstStrikes'), 'fsimm': num(b, 'bFirstStrikeImmune'),
        'wd': num(b, 'iWithdrawalProb'), 'limit': num(b, 'iCombatLimit'),
        'coll': num(b, 'iCollateralDamage'), 'colllim': num(b, 'iCollateralDamageLimit'), 'collmax': num(b, 'iCollateralDamageMaxUnits'),
        'air': num(b, 'iAirRange'), 'aircombat': num(b, 'iAirCombat'), 'airlim': num(b, 'iAirCombatLimit'),
        'bomb': num(b, 'iBombardRate'), 'ignbld': num(b, 'bIgnoreBuildingDefense'), 'nodef': num(b, 'bNoDefensiveBonus'),
        'onlydef': num(b, 'bOnlyDefensive'), 'cityatk': num(b, 'iCityAttack'), 'citydef': num(b, 'iCityDefense'),
        'hillsatk': num(b, 'iHillsAttack'), 'hillsdef': num(b, 'iHillsDefense'),
        'dcmrange': num(b, 'iDCMBombRange'), 'dcmacc': num(b, 'iDCMBombAccuracy'),
        'defai': (scalar(b, 'DefaultUnitAI') or '').replace('UNITAI_', ''),
        'ais': [a.replace('UNITAI_', '') for a, on in re.findall(r'<UnitAIType>([^<]*)</UnitAIType>\s*<bUnitAI>([^<]*)</bUnitAI>', b) if on.strip() == '1'],
        'prereqb': [x.replace('BUILDING_', '') for x in re.findall(r'<PrereqBuilding>([^<]*)</PrereqBuilding>', b) if x != 'NONE'],
        'cmods': ['%s%+d' % (c.replace('UNITCOMBAT_', ''), int(v)) for c, v in re.findall(r'<UnitCombatType>([^<]*)</UnitCombatType>\s*<iUnitCombatMod>(-?\d+)</iUnitCombatMod>', b) if int(v)],
        'src': sources[t],
    }
    u['effcoll'] = u['str'] * u['coll'] // 100
    rows.append(u)

ERA_ORDER = ['PREHISTORIC', 'ANCIENT', 'CLASSICAL', 'MEDIEVAL', 'RENAISSANCE', 'INDUSTRIAL', 'MODERN', 'TRANSHUMAN', 'INFORMATION', 'FUTURE', '?']
def era_key(e):
    return ERA_ORDER.index(e) if e in ERA_ORDER else len(ERA_ORDER)
rows.sort(key=lambda u: (era_key(u['era']), u['combat_type'], u['str']))

o = []
w = o.append
w('# RoM combat XML audit\n')
w('Read from `Assets/XML` and every module directory that `MLF_CIV4ModularLoadingControls.xml` loads (all are loaded). '
  'Land units with strength > 0: %d. Values are the XML values; derived columns are computed as the DLL does.\n' % len(rows))

# summary statistics
w('## Findings\n')
strikers = [u for u in rows if u['air'] > 0 and u['aircombat'] > 0]
coll = [u for u in rows if u['coll'] > 0]
coll0 = [u for u in coll if u['effcoll'] == 0]
limited = [u for u in rows if 0 < u['limit'] < 100]
bombers = [u for u in rows if u['bomb'] > 0]
ign = [u for u in rows if u['ignbld']]
dcm = [u for u in rows if u['dcmrange'] > 0]
w('- Units with a ranged strike (iAirRange > 0 and iAirCombat > 0): %d. By combat type: %s.' % (
    len(strikers), dict(collections.Counter(u['combat_type'] for u in strikers))))
w('- Units with iCollateralDamage > 0: %d, of which %d have **effective collateral 0** (integer strength x %% / 100), e.g. %s.' % (
    len(coll), len(coll0), ', '.join(sorted(set(u['type'] for u in coll0))[:12])))
w('- Combat-limited units (iCombatLimit < 100, cannot kill): %d, by type: %s.' % (len(limited), dict(collections.Counter(u['combat_type'] for u in limited))))
w('- Units that bombard city defences: %d; that ignore building defence: %d.' % (len(bombers), len(ign)))
w('- Units with a DCM ranged-bombard range (DCM_RANGE_BOMBARD is 0, so unused): %s.' % (', '.join(u['type'] for u in dcm) or 'none'))
# power
by_ct = collections.defaultdict(list)
for u in rows:
    if u['cost'] > 0 and u['power'] > 0:
        by_ct[u['combat_type']].append(u)
w('- **iPower per hammer and per strength point**, median by combat type (iPower feeds the AI\'s power '
  'comparisons and war decisions):')
w('')
w('| Combat type | Units | iPower / cost | iPower / strength | Example |')
w('|---|---|---|---|---|')
import statistics as st
for ct, us in sorted(by_ct.items(), key=lambda kv: -len(kv[1])):
    if len(us) < 2:
        continue
    ex = sorted(us, key=lambda u: u['cost'])[len(us) // 2]
    w('| %s | %d | %.2f | %.2f | %s: cost %d, str %d, power %d |' % (ct, len(us), st.median(u['power'] / u['cost'] for u in us),
      st.median(u['power'] / u['str'] for u in us), ex['type'], ex['cost'], ex['str'], ex['power']))
w('')
# roles
roles = collections.Counter()
for u in rows:
    for a in u['ais']:
        roles[(u['combat_type'], a)] += 1
w('- Unit AI roles allowed, by combat type (how often):')
w('')
w('| Combat type | Roles |')
w('|---|---|')
for ct in sorted(set(u['combat_type'] for u in rows)):
    rs = sorted(((a, n) for (c, a), n in roles.items() if c == ct), key=lambda x: -x[1])
    w('| %s | %s |' % (ct, ', '.join('%s %d' % x for x in rs)))
w('')
pre = collections.Counter()
for u in rows:
    for x in u['prereqb']:
        pre[(u['combat_type'], x)] += 1
w('- Building prerequisites of land units: ' + '; '.join('%s needs %s (%d)' % (c, x, n) for (c, x), n in sorted(pre.items(), key=lambda kv: -kv[1])[:20]) + '.')
w('')

# the full table
w('## Land units\n')
w('Columns: era, combat type, strength, moves, cost, iPower, first strikes (+chance), withdrawal %, combat limit, '
  'collateral % / limit / max units / **effective strength**, ranged strike (range, air combat, limit), bombard rate, '
  'ignores building defence, no defensive bonus, city attack / defence %, combat-type modifiers, roles (default first), '
  'building prerequisite, source file.\n')
w('| Unit | Era | Type | Str | Mv | Cost | Pow | FS | Wd | Lim | Coll | Strike | Bomb | IgnB | NoDef | City a/d | Mods | Roles | Needs | Src |')
w('|' + '---|' * 20)
for u in rows:
    collv = '%d/%d/%d/**%d**' % (u['coll'], u['colllim'], u['collmax'], u['effcoll']) if u['coll'] else ''
    strike = '%d/%d/%d' % (u['air'], u['aircombat'], u['airlim']) if u['air'] and u['aircombat'] else ''
    roles_s = u['defai'] + ('; ' + ','.join(a for a in u['ais'] if a != u['defai']) if u['ais'] else '')
    w('| %s | %s | %s | %d | %d | %d | %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
        u['type'], u['era'][:4], u['combat_type'], u['str'], u['moves'], u['cost'], u['power'],
        ('%d+%d' % (u['fs'], u['cfs'])) if (u['fs'] or u['cfs']) else '', u['wd'] or '', u['limit'] if u['limit'] != 100 else '',
        collv, strike, u['bomb'] or '', 'Y' if u['ignbld'] else '', 'Y' if u['nodef'] else '',
        ('%d/%d' % (u['cityatk'], u['citydef'])) if (u['cityatk'] or u['citydef']) else '', ' '.join(u['cmods']), roles_s,
        ','.join(u['prereqb']), u['src'].replace('XML/Units/CIV4UnitInfos.xml', 'base')))

# promotions
w('\n## Promotions with combat effects\n')
w('| Promotion | Str % | City atk | City def | Hills a/d | Collat % | Bomb % | Wd % | FS | Heal (same/adj) | Combat-type mods | Prereq |')
w('|---|---|---|---|---|---|---|---|---|---|---|---|')
for p, _, fs in os.walk(A):
    for f in fs:
        if f.endswith('PromotionInfos.xml') and loaded(p):
            for b in blocks(read(os.path.join(p, f)), 'PromotionInfo'):
                t = scalar(b, 'Type', '').replace('PROMOTION_', '')
                vals = [num(b, 'iCombatPercent'), num(b, 'iCityAttack'), num(b, 'iCityDefense'), num(b, 'iHillsAttack'), num(b, 'iHillsDefense'),
                        num(b, 'iCollateralDamageChange'), num(b, 'iBombardRateChange'), num(b, 'iWithdrawalChange'), num(b, 'iFirstStrikesChange'),
                        num(b, 'iSameTileHealChange'), num(b, 'iAdjacentTileHealChange')]
                mods = ['%s%+d' % (c.replace('UNITCOMBAT_', ''), int(v)) for c, v in re.findall(r'<UnitCombatType>([^<]*)</UnitCombatType>\s*<iUnitCombatMod>(-?\d+)</iUnitCombatMod>', b) if int(v)]
                if not any(vals) and not mods:
                    continue
                w('| %s | %s | %s | %s | %s/%s | %s | %s | %s | %s | %s/%s | %s | %s |' % (
                    t, *[v or '' for v in vals[:3]], vals[3] or '', vals[4] or '', *[v or '' for v in vals[5:9]], vals[9] or '', vals[10] or '',
                    ' '.join(mods), (scalar(b, 'PromotionPrereq') or '').replace('PROMOTION_', '')))

# buildings
w('\n## Buildings with defence\n')
w('| Building | iDefense | iBombardDefense | iAllCityDefense | Other |')
w('|---|---|---|---|---|')
for p, _, fs in os.walk(A):
    for f in fs:
        if f.endswith('BuildingInfos.xml') and loaded(p):
            for b in blocks(read(os.path.join(p, f)), 'BuildingInfo'):
                d, bd, ad = num(b, 'iDefense'), num(b, 'iBombardDefense'), num(b, 'iAllCityDefense')
                if d or bd or ad:
                    w('| %s | %s | %s | %s | %s |' % (scalar(b, 'Type', '').replace('BUILDING_', ''), d or '', bd or '', ad or '',
                                                     'needs ' + scalar(b, 'PrereqTech', '').replace('TECH_', '')))

open(OUT, 'w').write('\n'.join(o) + '\n')
print('units', len(rows), 'strikers', len(strikers), 'collateral', len(coll), 'zero-effective', len(coll0))
