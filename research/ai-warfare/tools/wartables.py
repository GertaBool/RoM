#!/usr/bin/env python3
"""War tables from xmlread.py's records.json (the resolved, loaded RoM XML).

- Research distance of every tech: its cost plus the cheapest way through its
  prerequisites (all AndPreReqs, the cheapest of the OrPreReqs), in base research
  cost (speed and handicap scale all techs alike, so the order holds everywhere).
- Every land combat unit that is its class's default unit, in that order, with the
  values that decide battles and the resources and buildings it needs.
- Every building with a defence value, in the same order.
- Per strategic resource: the unit lines that need it.
usage: wartables.py <records.json> <out.md>"""
import json, sys, functools, collections

R = json.load(open(sys.argv[1]))
OUT = open(sys.argv[2], 'w')
T, U, B, UC, BC = R['TechInfo'], R['UnitInfo'], R['BuildingInfo'], R['UnitClassInfo'], R['BuildingClassInfo']


def lst(v):
    v = v if isinstance(v, list) else [v]
    return [x for x in v if x not in (None, '', 'NONE')]


@functools.lru_cache(None)
def reach(t):
    """(research distance, set of techs) to own tech t."""
    if t not in T:
        return (10 ** 9, frozenset())
    rec = T[t]
    techs = {t}
    for a in lst(rec.get('AndPreReqs')):
        techs |= reach(a)[1]
    ors = [reach(o) for o in lst(rec.get('OrPreReqs'))]
    if ors:
        techs |= min(ors, key=lambda r: r[0])[1]
    return (sum(max(0, T[x].get('iCost') or 0) for x in techs if x in T), frozenset(techs))


def dist(techs):
    s = set()
    for t in techs:
        s |= reach(t)[1]
    return sum(max(0, T[x].get('iCost') or 0) for x in s if x in T)


def unit_techs(u):
    return [x for x in [u.get('PrereqTech')] + lst(u.get('TechTypes')) if x and x != 'NONE']


def era(t):
    return (T.get(t, {}).get('Era') or '?').replace('ERA_', '').title()


def eff_coll(u):
    s = (u.get('iCombat') or 0) * (u.get('iCollateralDamage') or 0) // 100
    return s


w = OUT.write
w('# RoM war tables (generated from the XML by wartables.py)\n\n')
w('Research distance: base research cost to own the tech, through its cheapest prerequisites.\n\n')

# ---- land units ----
defaults = {c['DefaultUnit'] for c in UC.values()}
rows = []
for k, u in U.items():
    if k not in defaults or u.get('Domain') != 'DOMAIN_LAND' or not (u.get('iCombat') or 0):
        continue
    techs = unit_techs(u)
    if not techs:
        continue
    d = dist(techs)
    rows.append((d, k, u, techs))
rows.sort(key=lambda r: (r[0], r[1]))
w('## Land combat units (class defaults), by research distance\n\n')
w('| Dist | Era | Unit | Combat | Str | Cost | Mv | City atk/def | Hills d | FS | Wd | Limit | Coll (eff/%/n/max) | Bomb | Ranged (rng/air/lim) | Ign. walls | No def bonus | Vs class/combat | Flank vs | Coll. immune | Forest/jungle atk | Needs bonus (all / any) | Needs building |\n')
w('|' + '---|' * 23 + '\n')
for d, k, u, techs in rows:
    mods = ['%s %+d' % (m['UnitClassType'].replace('UNITCLASS_', '').lower(), m['iUnitClassMod']) for m in lst(u.get('UnitClassAttackMods')) if isinstance(m, dict)]
    mods += ['%s %+d' % (m['UnitCombatType'].replace('UNITCOMBAT_', '').lower(), m['iUnitCombatMod']) for m in lst(u.get('UnitCombatMods')) if isinstance(m, dict)]
    mods += ['def vs %s %+d' % (m['UnitClassType'].replace('UNITCLASS_', '').lower(), m['iUnitClassMod']) for m in lst(u.get('UnitClassDefenseMods')) if isinstance(m, dict)]
    flank = ['%s %d' % (m['FlankingStrikeUnitClass'].replace('UNITCLASS_', '').lower(), m['iFlankingStrength']) for m in lst(u.get('FlankingStrikes')) if isinstance(m, dict)]
    imm = [m['UnitCombatType'].replace('UNITCOMBAT_', '').lower() for m in lst(u.get('UnitCombatCollateralImmunes')) if isinstance(m, dict)]
    feat = ['%s %+d' % (m['FeatureType'].replace('FEATURE_', '').lower(), m['iFeatureAttack']) for m in lst(u.get('FeatureAttacks')) if isinstance(m, dict) and m.get('iFeatureAttack')]
    coll = '%d/%d/%d/%d' % (eff_coll(u), u.get('iCollateralDamage') or 0, u.get('iCollateralDamageMaxUnits') or 0, u.get('iCollateralDamageLimit') or 0) if u.get('iCollateralDamage') else ''
    rng = '%d/%d/%d' % (u.get('iAirRange') or 0, u.get('iAirCombat') or 0, u.get('iAirCombatLimit') or 0) if u.get('iAirRange') and u.get('iAirCombat') else ''
    bon = '' if u.get('BonusType') in (None, '', 'NONE') else u['BonusType'].replace('BONUS_', '').lower()
    anyb = '/'.join(x.replace('BONUS_', '').lower() for x in lst(u.get('PrereqBonuses')))
    w('| %d | %s | %s | %s | %d | %d | %d | %s/%s | %s | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n' % (
        d, era(max(techs, key=lambda t: reach(t)[0])), k.replace('UNIT_', ''), (u.get('Combat') or '').replace('UNITCOMBAT_', '').lower(),
        u.get('iCombat') or 0, u.get('iCost') or 0, u.get('iMoves') or 0, u.get('iCityAttack') or 0, u.get('iCityDefense') or 0,
        u.get('iHillsDefense') or '', u.get('iFirstStrikes') or '', ('+%d' % u['iChanceFirstStrikes']) if u.get('iChanceFirstStrikes') else '',
        u.get('iWithdrawalProb') or '', u.get('iCombatLimit') if (u.get('iCombatLimit') or 100) != 100 else '', coll, u.get('iBombardRate') or '', rng,
        'yes' if u.get('bIgnoreBuildingDefense') else '', 'yes' if u.get('bNoDefensiveBonus') else '', ', '.join(mods), ', '.join(flank), ', '.join(imm),
        ', '.join(feat), ' + '.join(x for x in [bon, anyb and '(' + anyb + ')'] if x), (u.get('PrereqBuilding') or '').replace('BUILDING_', '').lower()))

# ---- buildings with defence ----
w('\n## Buildings with city defence, by research distance\n\n| Dist | Era | Building | Defence | Bombard def. | All cities | Obsolete | Needs bonus | Conquest survival % |\n|---|---|---|---|---|---|---|---|---|\n')
brows = []
for k, b in B.items():
    if not (b.get('iDefense') or b.get('iBombardDefense') or b.get('iAllCityDefense')):
        continue
    techs = [x for x in [b.get('PrereqTech')] + lst(b.get('TechTypes')) if x and x != 'NONE']
    brows.append((dist(techs) if techs else 0, k, b, techs))
for d, k, b, techs in sorted(brows, key=lambda r: (r[0], r[1])):
    w('| %d | %s | %s | %s | %s | %s | %s | %s | %s |\n' % (d, era(max(techs, key=lambda t: reach(t)[0])) if techs else '-', k.replace('BUILDING_', ''),
      b.get('iDefense') or '', b.get('iBombardDefense') or '', b.get('iAllCityDefense') or '', (b.get('ObsoleteTech') or '').replace('TECH_', ''),
      ' '.join(x.replace('BONUS_', '').lower() for x in lst(b.get('PrereqBonus')) + lst(b.get('PrereqBonuses'))), b.get('iConquestProb') if b.get('iConquestProb') is not None else ''))

# ---- strategic resources ----
w('\n## Strategic resources: land unit lines that need them\n\n| Resource | Needed by (all) | One of (any) |\n|---|---|---|\n')
need_all, need_any = collections.defaultdict(list), collections.defaultdict(list)
for d, k, u, techs in rows:
    if u.get('BonusType') and u['BonusType'] != 'NONE':
        need_all[u['BonusType']].append(k.replace('UNIT_', '').lower())
    for x in lst(u.get('PrereqBonuses')):
        need_any[x].append(k.replace('UNIT_', '').lower())
for bn in sorted(set(need_all) | set(need_any)):
    w('| %s | %s | %s |\n' % (bn.replace('BONUS_', '').lower(), ', '.join(need_all[bn]), ', '.join(need_any[bn])))

# ---- leaders ----
L = R['LeaderHeadInfo']
civ_of = collections.defaultdict(set)
for c, cv in R['CivilizationInfo'].items():
    for g in lst(cv.get('Leaders')):
        if isinstance(g, dict) and g.get('bLeaderAvailability'):
            civ_of[g['LeaderName']].add(c.replace('CIVILIZATION_', '').lower())
w('\n## Leaders: war personality\n\nAttack odds = iBaseAttackOddsChange + rand(iAttackOddsChangeRand). Wars are planned with probability 1/rand: smaller iMaxWarRand / iLimitedWarRand / iDogpileWarRand = more wars.\n\n')
w('| Leader | Civ | Traits | Odds +rand | Build unit % | Max war rand | Limited war rand | Dogpile rand | Make peace rand | Nearby PR | Distant PR | Limited PR | Raze % | Conquest/Domination | Flavours | Unit AI weights |\n|' + '---|' * 16 + '\n')
for k in sorted(L):
    v = L[k]
    if k == 'LEADER_BARBARIAN':
        continue
    w('| %s | %s | %s | %d+%d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d/%d | %s | %s |\n' % (
        k.replace('LEADER_', ''), ','.join(sorted(civ_of.get(k, []))), ','.join(x.replace('TRAIT_', '').lower() for x in
        [t['TraitType'] for t in lst(v.get('Traits')) if isinstance(t, dict) and t.get('bTrait')]),
        v.get('iBaseAttackOddsChange') or 0, v.get('iAttackOddsChangeRand') or 0, v.get('iBuildUnitProb') or 0, v.get('iMaxWarRand') or 0,
        v.get('iLimitedWarRand') or 0, v.get('iDogpileWarRand') or 0, v.get('iMakePeaceRand') or 0, v.get('iMaxWarNearbyPowerRatio') or 0,
        v.get('iMaxWarDistantPowerRatio') or 0, v.get('iLimitedWarPowerRatio') or 0, v.get('iRazeCityProb') or 0,
        v.get('iConquestVictoryWeight') or 0, v.get('iDominationVictoryWeight') or 0,
        ', '.join('%s %d' % (f['FlavorType'].replace('FLAVOR_', '').lower(), f['iFlavor']) for f in lst(v.get('Flavors')) if isinstance(f, dict) and f.get('iFlavor')),
        ', '.join('%s %d' % (f['UnitAIType'].replace('UNITAI_', '').lower(), f['iWeightModifier']) for f in lst(v.get('UnitAIWeightModifiers')) if isinstance(f, dict) and f.get('iWeightModifier'))))

# ---- civics and buildings with military effects ----
CIV_F = ['iFreeExperience', 'iStateReligionFreeExperience', 'iMilitaryProductionModifier', 'iStateReligionUnitProductionModifier', 'iWarWearinessModifier',
         'iGreatGeneralRateModifier', 'iDomesticGreatGeneralRateModifier', 'iHappyPerMilitaryUnit', 'iGoldPerUnit', 'iGoldPerMilitaryUnit', 'iBaseFreeUnits',
         'iFreeUnitsPopulationPercent', 'iMaxConscript', 'bUpgradeAnywhere', 'bMilitaryFoodProduction']
w('\n## Civics with military effects\n\n| Civic | Option | Tech | Effects |\n|---|---|---|---|\n')
for k in sorted(R['CivicInfo']):
    v = R['CivicInfo'][k]
    eff = ['%s %s' % (f[1:] if f[0] in 'ib' else f, v[f]) for f in CIV_F if v.get(f)]
    eff += ['hurry ' + h['HurryType'].replace('HURRY_', '').lower() for h in lst(v.get('Hurrys')) if isinstance(h, dict) and h.get('bHurry')]
    if eff:
        w('| %s | %s | %s | %s |\n' % (k.replace('CIVIC_', ''), (v.get('CivicOptionType') or '').replace('CIVICOPTION_', '').lower(), (v.get('TechPrereq') or '').replace('TECH_', ''), '; '.join(eff)))
B_F = ['iMilitaryProductionModifier', 'iExperience', 'iGlobalExperience', 'iHealRateChange', 'iWarWearinessModifier', 'iGlobalWarWearinessModifier',
       'iEnemyWarWearinessModifier', 'iGreatGeneralRateModifier', 'iDomesticGreatGeneralRateModifier', 'iUnitUpgradePriceModifier', 'iAirModifier', 'iNukeModifier',
       'bBorderObstacle', 'iAirlift', 'iEspionageDefense']
w('\n## Buildings with military effects\n\n| Building | Tech | Effects |\n|---|---|---|\n')
for k in sorted(B):
    v = B[k]
    eff = ['%s %s' % (f[1:], v[f]) for f in B_F if v.get(f)]
    eff += ['xp %s +%d' % (x['UnitCombatType'].replace('UNITCOMBAT_', '').lower(), x['iExperience']) for x in lst(v.get('UnitCombatFreeExperiences')) if isinstance(x, dict) and x.get('iExperience')]
    eff += ['xp %s +%d' % (x['DomainType'].replace('DOMAIN_', '').lower(), x['iExperience']) for x in lst(v.get('DomainFreeExperiences')) if isinstance(x, dict) and x.get('iExperience')]
    eff += ['%s production +%d%%' % (x['DomainType'].replace('DOMAIN_', '').lower(), x['iProductionModifier']) for x in lst(v.get('DomainProductionModifiers')) if isinstance(x, dict) and x.get('iProductionModifier')]
    if v.get('FreePromotion') not in (None, '', 'NONE'):
        eff.append('promotion ' + v['FreePromotion'].replace('PROMOTION_', '').lower())
    if eff:
        w('| %s | %s | %s |\n' % (k.replace('BUILDING_', ''), (v.get('PrereqTech') or '').replace('TECH_', ''), '; '.join(eff)))
OUT.close()
print('units', len(rows), 'defence buildings', len(brows))
