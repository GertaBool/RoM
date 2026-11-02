"""Goods catalogue fields of every resource record (GW.F1.T3, D22).
Lists each BonusInfo of the base file and the module files with its GoodUnit and GoodCategory, and compares
them with proposals.json (goods: unit, category; units; categories). A module record without the tags
inherits the base record's through CvBonusInfo::copyNonDefaults and is listed as 'inherits'.
Errors (exit 1): a value outside proposals.json units or categories; a record whose fields differ from its
proposal; a record with a proposal but without fields (unless it inherits them); a record with fields but
no proposal; a module schema whose BonusInfo records carry the tags but whose schema does not declare them.
usage: goods_fields.py <mod checkout> [--list]"""
import glob, json, os, re, sys

mod = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
prop = json.load(open(os.path.join(HERE, '..', 'proposals.json')))
UNITS, CATS, GOODS = prop['units'], prop['categories'], prop['goods']

def records(path):
    s = open(path, 'rb').read().decode('latin-1')
    for body in re.findall(r'<BonusInfo>(.*?)</BonusInfo>', s, re.S):
        t = re.search(r'<Type>\s*(\S+?)\s*</Type>', body).group(1)
        get = lambda tag: (re.search(r'<%s>(.*?)</%s>' % (tag, tag), body, re.S) or [None, None])[1]
        yield t, get('GoodUnit'), get('GoodCategory')

base = os.path.join(mod, 'Assets/XML/Terrain/CIV4BonusInfos.xml')
files = [base] + sorted(f for f in glob.glob(os.path.join(mod, 'Assets/Modules/**/*_CIV4BonusInfos.xml'), recursive=True))
errors, rows, have = [], [], {}
for f in files:
    rel = os.path.relpath(f, mod)
    tagged = False
    for t, u, c in records(f):
        p = GOODS.get(t, {})
        want = (p.get('unit'), p.get('category'))
        if u is not None and u not in UNITS: errors.append('%s %s: unknown GoodUnit %r' % (rel, t, u))
        if c is not None and c not in CATS: errors.append('%s %s: unknown GoodCategory %r' % (rel, t, c))
        if u is not None or c is not None:
            tagged = True
            have[t] = (u, c)
            state = 'set'
            if (u, c) != want: errors.append('%s %s: %s / %s, proposal %s / %s' % (rel, t, u, c, want[0], want[1]))
        elif f != base and t in have:
            state = 'inherits'
        elif want != (None, None):
            state = 'MISSING'
            errors.append('%s %s: no fields, proposal %s / %s' % (rel, t, want[0], want[1]))
        else:
            state = 'none (no proposal)'
        rows.append((rel, t) + (have.get(t, (None, None)) if state == 'inherits' else (u, c)) + (state,))
    if tagged and f != base:
        sch = glob.glob(os.path.join(os.path.dirname(f), '*_CIV4TerrainSchema.xml'))
        txt = open(sch[0], 'rb').read().decode('latin-1') if sch else ''
        if 'name="GoodUnit"' not in txt or 'name="GoodCategory"' not in txt:
            errors.append('%s: records carry the tags but %s does not declare them' % (rel, sch[0] if sch else 'no schema'))

if '--list' in sys.argv:
    for r in rows: print('%-62s %-24s %-8s %-16s %s' % tuple('-' if x is None else x for x in r))
none = [r[1] for r in rows if r[4].startswith('none')]
print('%d records: %d set, %d inherit, %d without (%s)' % (len(rows), sum(r[4] == 'set' for r in rows),
      sum(r[4] == 'inherits' for r in rows), len(none), ', '.join(none)))
for e in errors: print('ERROR', e)
sys.exit(1 if errors else 0)
