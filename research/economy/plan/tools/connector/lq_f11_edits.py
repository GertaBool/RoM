"""LQ.F11 (D20): a pasture and each Latifundium stage on an animal give every product of it through ProducedBonuses
(the mechanism of LQ.F10): sheep wool, dairy, leather; cow dairy, leather; horse leather; pig nothing more.
Wool's TechCityTrade TECH_WEAVING (a tech RoM does not have: the loader reports it and the field is -1) becomes
TECH_ANIMAL_HUSBANDRY, the trade tech of Sheep, Dairy and Leather.
Applies to a mod checkout that already has LQ.F10 and writes the (old, new) pairs, each unique in its file.
usage: lq_f11_edits.py <mod checkout> <pairs.json out>"""
import json, os, re, sys

mod, out = sys.argv[1], sys.argv[2]
PRODUCTS = [('BONUS_SHEEP', ['BONUS_WOOL', 'BONUS_DAIRY', 'BONUS_LEATHER']),
            ('BONUS_COW', ['BONUS_DAIRY', 'BONUS_LEATHER']),
            ('BONUS_HORSE', ['BONUS_LEATHER'])]
RECORDS = ['IMPROVEMENT_PASTURE'] + ['IMPROVEMENT_LATIFUNDIUM%d' % i for i in range(1, 6)]
pairs = []

def load(f):
    return open(os.path.join(mod, f), 'rb').read().decode('latin-1')

def save(f, s):
    open(os.path.join(mod, f), 'wb').write(s.encode('latin-1'))

def unique_window(s, i, j, nl):
    a, b = i, j
    while s.count(s[a:b]) != 1:
        a = s.rfind(nl, 0, a - len(nl)) + len(nl) if a > 0 else 0
        b = s.find(nl, b) + len(nl) if s.find(nl, b) >= 0 else len(s)
    return a, b

f = 'Assets/XML/Terrain/CIV4ImprovementInfos.xml'
s = load(f); nl = '\r\n' if '\r\n' in s else '\n'
block = ''.join('\t\t\t\t<ProducedBonus>%s\t\t\t\t\t<BonusType>%s</BonusType>%s\t\t\t\t\t<PrereqBonus>%s</PrereqBonus>%s\t\t\t\t</ProducedBonus>%s'
                % (nl, p, nl, a, nl, nl) for a, ps in PRODUCTS for p in ps)
block = '\t\t\t<ProducedBonuses>' + nl + block + '\t\t\t</ProducedBonuses>' + nl
for t in RECORDS:
    r0 = s.index('<Type>%s</Type>' % t)
    r1 = s.index('</ImprovementInfo>', r0)
    k = s.index('</BonusTypeStructs>' + nl, r0)
    assert k < r1 and '<ProducedBonuses>' not in s[r0:r1], t
    k += len('</BonusTypeStructs>' + nl)       # insert after this line
    a, b = unique_window(s, k - len('</BonusTypeStructs>' + nl), k, nl)
    old = s[a:b]; new = s[a:k] + block + s[k:b]
    pairs.append({'file': f, 'old': old, 'new': new})
    s = s[:a] + new + s[b:]
save(f, s)

f = 'Assets/XML/Terrain/CIV4BonusInfos.xml'
s = load(f); nl = '\r\n' if '\r\n' in s else '\n'
old = '<Civilopedia>TXT_KEY_BONUS_WOOL_PEDIA</Civilopedia>'
i = s.index(old); j = s.index('<TechCityTrade>TECH_WEAVING</TechCityTrade>', i) + len('<TechCityTrade>TECH_WEAVING</TechCityTrade>')
o = s[i:j]; n = o.replace('TECH_WEAVING', 'TECH_ANIMAL_HUSBANDRY')
assert s.count(o) == 1
pairs.append({'file': f, 'old': o, 'new': n}); save(f, s.replace(o, n))

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(x)) for x in pairs), 'bytes of JSON')
