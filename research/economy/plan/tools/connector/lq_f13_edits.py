"""LQ.F13 edits on a checkout: applies them and saves minimal unique (old, new) pairs."""
import json, os, re, sys
root, out = sys.argv[1], sys.argv[2]
sys.argv = ['t', root]; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lq_f13_targets.py')).read().split("if __name__")[0])
pairs = []
def load(rel): return open(os.path.join(root, rel), 'rb').read().decode('latin-1')
def save(rel, s): open(os.path.join(root, rel), 'wb').write(s.encode('latin-1'))
def unique(s, x, y):
    sub = s[x:y]; i = s.find(sub); return i == x and s.find(sub, i + 1) < 0
def replace_at(rel, s, a0, b0, new):
    """Replace s[a0:b0] by new; the old text is the shortest run of whole lines around it that is unique."""
    a = s.rindex('\n', 0, a0) + 1; b = s.index('\n', b0) + 1
    ups = [a]; downs = [b]
    for _ in range(400):
        if ups[-1] > 0: ups.append(s.rfind('\n', 0, ups[-1] - 1) + 1)
        if downs[-1] < len(s): downs.append(s.index('\n', downs[-1]) + 1)
    cand = sorted(((y - x), x, y) for x in ups for y in downs)
    for _, x, y in cand:
        if unique(s, x, y): a, b = x, y; break
    else: raise SystemExit('no unique anchor at %d' % a0)
    pairs.append(dict(file=rel, old=s[a:b], new=s[a:a0] + new + s[b0:b]))
    return s[:a0] + new + s[b0:]
def entries(goods, ind):
    return ''.join('%s<BonusProductionModifier>\r\n%s\t<BonusType>%s</BonusType>\r\n%s\t<iProductonModifier>%d</iProductonModifier>\r\n%s</BonusProductionModifier>\r\n' % (ind, ind, g, ind, v, ind) for g, v in goods)
def add_bpm(rel, s, tag, typ, goods):
    i = s.index('<Type>%s</Type>' % typ); e = s.index('</%s>' % tag, i)
    st = s.rindex('<%s>' % tag, 0, i)
    j = s.find('<BonusProductionModifiers/>', st, e)
    if j >= 0:
        ind = s[s.rindex('\n', 0, j) + 1:j]
        return replace_at(rel, s, j, j + len('<BonusProductionModifiers/>'), '<BonusProductionModifiers>\r\n' + entries(goods, ind + '\t') + ind + '</BonusProductionModifiers>')
    j = s.find('</BonusProductionModifiers>', st, e); assert j >= 0, typ
    ind = s[s.rindex('\n', 0, j) + 1:j]
    k = s.rindex('\n', 0, j) + 1
    return replace_at(rel, s, k, k, entries(goods, ind + '\t'))

B = 'Assets/XML/Buildings/CIV4BuildingInfos.xml'; s = load(B)
for typ in sorted(buildings):
    s = add_bpm(B, s, 'BuildingInfo', typ, [('BONUS_TIMBER', 15)])
# T1: Timber's +3 % production in the essentials buildings goes (replaced by the construction speed above)
yt = '\t\t\t\t<BonusYieldModifier>\r\n\t\t\t\t\t<BonusType>BONUS_TIMBER</BonusType>\r\n\t\t\t\t\t<YieldModifiers>\r\n\t\t\t\t\t\t<iYield>0</iYield>\r\n\t\t\t\t\t\t<iYield>3</iYield>\r\n\t\t\t\t\t\t<iYield>0</iYield>\r\n\t\t\t\t\t</YieldModifiers>\r\n\t\t\t\t</BonusYieldModifier>\r\n'
for b in ('SETTLEMENT', 'TOWN', 'CITY', 'METROPOLITAN'):
    i = s.index('<Type>BUILDING_%s_ESSENTIALS</Type>' % b); j = s.index(yt, i); assert j < s.index('</BuildingInfo>', i)
    s = replace_at(B, s, j, j + len(yt), '')
# T4: Timber at the Forge and the Iron Forge, the step of each of their inputs
yf = '\t\t\t\t<BonusYieldModifier>\r\n\t\t\t\t\t<BonusType>BONUS_TIMBER</BonusType>\r\n\t\t\t\t\t<YieldModifiers>\r\n\t\t\t\t\t\t<iYield>0</iYield>\r\n\t\t\t\t\t\t<iYield>25</iYield>\r\n\t\t\t\t\t\t<iYield>0</iYield>\r\n\t\t\t\t\t</YieldModifiers>\r\n\t\t\t\t</BonusYieldModifier>\r\n'
for typ in ('BUILDING_FORGE', 'BUILDING_IRON_FORGE'):
    i = s.index('<Type>%s</Type>' % typ); e = s.index('</BuildingInfo>', i)
    j = s.index('</BonusYieldModifiers>', i); assert j < e
    k = s.rindex('\n', 0, j) + 1
    s = replace_at(B, s, k, k, yf)
save(B, s)

U = 'Assets/XML/Units/CIV4UnitInfos.xml'; s = load(U)
for typ, (c, era, goods) in sorted(units.items()):
    s = add_bpm(U, s, 'UnitInfo', typ, [(g, 15) for g in goods])
save(U, s)

N = 'Assets/XML/Terrain/CIV4BonusInfos.xml'; s = load(N)
i = s.index('<Type>BONUS_TIMBER</Type>'); j = s.index('<iHealth>0</iHealth>', i); assert j < s.index('</BonusInfo>', i)
s = replace_at(N, s, j, j + len('<iHealth>0</iHealth>'), '<iHealth>1</iHealth>'); save(N, s)
json.dump(pairs, open(out, 'w'), indent=1)
import collections
print(len(pairs), 'edits', collections.Counter(p['file'] for p in pairs), 'chars', sum(len(p['old']) + len(p['new']) for p in pairs))
