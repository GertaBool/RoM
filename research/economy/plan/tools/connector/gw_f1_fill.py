"""GW.F1.T3: GoodUnit and GoodCategory in every resource record proposals.json gives them (D22, M50).
Base CIV4BonusInfos.xml and Guilds_CIV4BonusInfos.xml (BONUS_CGUILDPAPER): two lines before each record's
</BonusInfo>, the end of the element order the schema sets. The Guilds schema declares the two tags as the base
schema does (gw_f1_edits.py). The Corporations module's partial records stay as they are and inherit through
copyNonDefaults. Each pair runs from the record's </BonusInfo> to the next record's <Type> line (or </BonusInfos>).
Check afterwards: research/economy/plan/tools/goods_fields.py <mod checkout>.
usage: gw_f1_fill.py <mod checkout> <pairs.json out>"""
import json, os, re, sys

mod, out = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
GOODS = json.load(open(os.path.join(HERE, '..', '..', 'proposals.json')))['goods']
pairs = []

def load(f):
    s = open(os.path.join(mod, f), 'rb').read().decode('latin-1')
    return s, ('\r\n' if '\r\n' in s else '\n')

def save(f, s):
    open(os.path.join(mod, f), 'wb').write(s.encode('latin-1'))

def fill(f):
    s, nl = load(f)
    for m in list(re.finditer(r'<Type>(BONUS_[A-Z0-9_]+)</Type>', s)):
        t = m.group(1); g = GOODS.get(t, {})
        if not g.get('unit'): continue
        i = s.index(m.group(0))                       # positions move as records grow
        end = s.index('</BonusInfo>', i)
        close = s.rfind(nl, i, end) + len(nl)         # start of the </BonusInfo> line
        indent = s[close:end]
        # the anchor: </BonusInfo> through the next record's <Type> line (or </BonusInfos>), unique by that Type
        nxt = re.compile(r'<Type>[^<]*</Type>|</BonusInfos>').search(s, end)
        old = s[close:nxt.end()]
        assert s.count(old) == 1, (f, t)
        ins = indent + '\t<GoodUnit>%s</GoodUnit>%s' % (g['unit'], nl) + indent + '\t<GoodCategory>%s</GoodCategory>%s' % (g['category'], nl)
        pairs.append({'file': f, 'old': old, 'new': ins + old})
        s = s[:close] + ins + s[close:]
    save(f, s)

fill('Assets/XML/Terrain/CIV4BonusInfos.xml')
G = 'Assets/Modules/Projects/Vincentz/Guilds/'
fill(G + 'Guilds_CIV4BonusInfos.xml')

# the Guilds schema: the same two declarations as the base schema
f = G + 'Guilds_CIV4TerrainSchema.xml'
s, nl = load(f)
for old, new in (
        ('\t\t<element type="bUseLSystem" minOccurs="0"/>\n\t</ElementType>\n\t<ElementType name="BonusInfos" content="eltOnly">',
         '\t\t<element type="bUseLSystem" minOccurs="0"/>\n\t\t<element type="GoodUnit" minOccurs="0"/>\n'
         '\t\t<element type="GoodCategory" minOccurs="0"/>\n\t</ElementType>\n\t<ElementType name="BonusInfos" content="eltOnly">'),
        ('\t<ElementType name="ArtDefineTag" content="textOnly"/>\n\t<ElementType name="Type" content="textOnly"/>',
         '\t<ElementType name="ArtDefineTag" content="textOnly"/>\n'
         '\t<ElementType name="GoodUnit" content="textOnly"/>\n\t<ElementType name="GoodCategory" content="textOnly"/>\n'
         '\t<ElementType name="Type" content="textOnly"/>')):
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert s.count(old) == 1, (f, old[:60])
    s = s.replace(old, new); pairs.append({'file': f, 'old': old, 'new': new})
save(f, s)

json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes')
