"""LQ.F13 targets by rule, from a checkout's XML."""
import re, sys, os
root = sys.argv[1]; X = os.path.join(root, 'Assets/XML')
rd = lambda f: re.sub(r'<!--.*?-->', lambda m: ' ' * len(m.group(0)), open(os.path.join(X, f), encoding='latin-1').read(), flags=re.S)
tech = {re.search(r'<Type>(\w+)', b).group(1): re.search(r'<Era>(\w+)', b).group(1) for b in re.findall(r'<TechInfo>(.*?)</TechInfo>', rd('Technologies/CIV4TechInfos.xml'), re.S)}
EARLY = {'ERA_ANCIENT', 'ERA_CLASSICAL', 'ERA_MEDIEVAL'}
def recs(f, tag):
    for b in re.findall(r'<%s>(.*?)</%s>' % (tag, tag), rd(f), re.S):
        t = re.search(r'<PrereqTech>(\w+)', b)
        yield re.search(r'<Type>(\w+)', b).group(1), b, tech.get(t.group(1) if t else 'NONE', 'none')
buildings = {ty: era for ty, b, era in recs('Buildings/CIV4BuildingInfos.xml', 'BuildingInfo') if era in EARLY}
units = {}
for ty, b, era in recs('Units/CIV4UnitInfos.xml', 'UnitInfo'):
    c = re.search(r'<Combat>(\w+)', b); c = c.group(1) if c else 'NONE'
    g = []
    civil = c in ('UNITCOMBAT_SETTLER', 'UNITCOMBAT_WORKER') and era in EARLY | {'none', 'ERA_RENAISSANCE', 'ERA_INDUSTRIAL'}
    if civil or c == 'UNITCOMBAT_WOODEN_SHIPS' or (c in ('UNITCOMBAT_ARCHER', 'UNITCOMBAT_SIEGE') and era in EARLY): g.append('BONUS_TIMBER')
    if civil or c == 'UNITCOMBAT_MOUNTED' or (c in ('UNITCOMBAT_MELEE', 'UNITCOMBAT_ARCHER') and era in ('ERA_ANCIENT', 'ERA_CLASSICAL')): g.append('BONUS_LEATHER')
    if ty == 'UNIT_MODERN_WORKBOAT': g = []
    if ty == 'UNIT_WORKBOAT': g = ['BONUS_TIMBER']
    if g: units[ty] = (c, era, g)
if __name__ == '__main__':
    import collections
    print('buildings', len(buildings), collections.Counter(buildings.values()))
    print('units', len(units), collections.Counter((c, tuple(g)) for c, e, g in units.values()))
    for ty, v in units.items():
        if v[0] in ('UNITCOMBAT_SETTLER','UNITCOMBAT_WORKER'): print(' ', ty, v)
