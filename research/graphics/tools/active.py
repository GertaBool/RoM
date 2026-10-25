"""The art a game state uses: unit and building types -> the mod's art definitions -> NIF models
-> the textures named inside each model, with the bytes each texture takes once loaded.
usage: active.py <mod Assets dir> <textures.csv> <harness state0.json> <out prefix>
Unit art: every UnitMeshGroup tag (early, middle, late) and every civilization art-style override
of the unit, so an upper bound for the eras in play. Building art: the building's ArtDefineTag.
Models or textures not in the mod (the base game's own art) are counted as missing."""
import csv, json, os, re, sys, collections, xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpk
assets, texcsv, state, prefix = sys.argv[1:5]
L = lambda e: e.tag.split('}')[-1]

def records(tag):
    for root, _, files in os.walk(assets):
        for f in files:
            if not f.lower().endswith('.xml'): continue
            p = os.path.join(root, f)
            try: r = ET.parse(p).getroot()
            except Exception: continue
            for e in r.iter():
                if L(e) == tag: yield e
def kids(e): return {L(c): c for c in e}
def text(e, name): c = kids(e).get(name); return (c.text or '').strip() if c is not None else ''

unit_art = {text(e, 'Type'): {k: text(e, k) for k in ('NIF', 'SHADERNIF', 'KFM')} for e in records('UnitArtInfo')}
bld_art = {text(e, 'Type'): {k: text(e, k) for k in ('NIF', 'LSystem')} for e in records('BuildingArtInfo')}
unit_tags = collections.defaultdict(set)
for e in records('UnitInfo'):
    t = text(e, 'Type')
    for g in e.iter():
        if L(g) in ('EarlyArtDefineTag', 'MiddleArtDefineTag', 'LateArtDefineTag') and (g.text or '').strip(): unit_tags[t].add(g.text.strip())
for e in records('UnitArtStyleTypeInfo'):
    for s in e.iter():
        if L(s) == 'StyleUnit':
            u = text(s, 'UnitType')
            for g in s.iter():
                if L(g) in ('EarlyArtDefineTag', 'MiddleArtDefineTag', 'LateArtDefineTag') and (g.text or '').strip(): unit_tags[u].add(g.text.strip())
bld_tag = {text(e, 'Type'): text(e, 'ArtDefineTag') for e in records('BuildingInfo')}

# files: loose replaces packed
files = {}
for name in sorted(os.listdir(assets)):
    if name.lower().endswith('.fpk'):
        p = os.path.join(assets, name)
        for m, size, off in fpk.members(p): files.setdefault(m.lower(), ('fpk', p, size, off))
for root, _, fs in os.walk(assets):
    for f in fs:
        p = os.path.join(root, f); files[os.path.relpath(p, assets).replace('\\', '/').lower()] = ('loose', p, 0, 0)
def load(path):
    k = files.get(path.lower().replace('\\', '/'))
    if not k: return None
    return open(k[1], 'rb').read() if k[0] == 'loose' else fpk.read(k[1], k[2], k[3])
tex = {r['path']: r for r in csv.DictReader(open(texcsv))}
for r in csv.DictReader(open(texcsv)):
    if r['source'] == 'loose': tex[r['path']] = r

d = json.load(open(state))
units = collections.Counter(('UNIT_' + u[0]) for p in d['players'] for u in p['unitList'])
blds = collections.Counter(b for p in d['players'] for c in p['cities'] for b in c['buildings'])
nifs = collections.defaultdict(set)          # nif path -> users
for u in units:
    for tag in unit_tags.get(u, ()):
        a = unit_art.get(tag, {})
        for k in ('NIF', 'SHADERNIF'):
            if a.get(k): nifs[a[k]].add(u)
for b in blds:
    a = bld_art.get(bld_tag.get(b, ''), {})
    if a.get('NIF'): nifs[a['NIF']].add(b)

TEX = re.compile(rb'[\x20-\x7e]{1,200}?\.(?:dds|tga|bmp)', re.I)
used = collections.defaultdict(set); missing_nif = []; missing_tex = collections.defaultdict(set)
for nif, who in nifs.items():
    b = load(nif)
    if b is None: missing_nif.append(nif); continue
    base = os.path.dirname(nif.replace('\\', '/'))
    for m in set(TEX.findall(b)):
        name = m.decode('latin-1').replace('\\', '/').lstrip('./').split('\x00')[-1]
        name = re.sub(r'^[^A-Za-z0-9_]+', '', name)
        cands = [name, base + '/' + name, base + '/' + os.path.basename(name)]
        hit = next((c.lower() for c in cands if c.lower() in tex), None)
        if hit: used[hit] |= who
        else: missing_tex[name.lower()] |= who
rows = [dict(path=p, users=len(w), **{k: tex[p][k] for k in ('fmt', 'w', 'h', 'mips', 'data', 'sha1', 'source')}) for p, w in used.items()]
with open(prefix + '.csv', 'w', newline='') as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(sorted(rows, key=lambda r: -int(r['data'])))
MB = lambda x: x / 2**20
tot = sum(int(r['data']) for r in rows)
unc = [r for r in rows if r['fmt'][0] in 'AX' or r['fmt'].startswith('TGA')]
shas = collections.Counter(r['sha1'] for r in rows)
dup = sum(int(r['data']) for r in rows if shas[r['sha1']] > 1) - sum(int(next(x for x in rows if x['sha1'] == s)['data']) for s, n in shas.items() if n > 1)
summary = dict(unit_types=len(units), units=sum(units.values()), building_types=len(blds), buildings=sum(blds.values()),
               models=len(nifs), models_missing=len(missing_nif), textures=len(rows), texture_MB=round(MB(tot), 1),
               uncompressed=len(unc), uncompressed_MB=round(MB(sum(int(r['data']) for r in unc)), 1),
               duplicate_extra_MB=round(MB(dup), 1), textures_missing=len(missing_tex))
json.dump(dict(summary=summary, missing_models=sorted(missing_nif), missing_textures=sorted(missing_tex)), open(prefix + '.json', 'w'), indent=1)
print(json.dumps(summary, indent=1))
