"""Shared helpers: XML records and the mod's files (loose replace packed)."""
import os, xml.etree.ElementTree as ET
import fpk
L = lambda e: e.tag.split('}')[-1]
def records(assets, tag):
    for root, _, files in os.walk(assets):
        for f in files:
            if not f.lower().endswith('.xml'): continue
            try: r = ET.parse(os.path.join(root, f)).getroot()
            except Exception: continue
            for e in r.iter():
                if L(e) == tag: yield e
def kids(e): return {L(c): c for c in e}
def text(e, name): c = kids(e).get(name); return (c.text or '').strip() if c is not None else ''
def files(assets):
    out = {}
    for name in sorted(os.listdir(assets)):
        if name.lower().endswith('.fpk'):
            p = os.path.join(assets, name)
            for m, size, off in fpk.members(p): out.setdefault(m.lower(), ('fpk', p, size, off))
    for root, _, fs in os.walk(assets):
        for f in fs:
            p = os.path.join(root, f); out[os.path.relpath(p, assets).replace('\\', '/').lower()] = ('loose', p, os.path.getsize(p), 0)
    return out
def load(files, path):
    k = files.get(path.lower().replace('\\', '/'))
    if not k: return None
    return open(k[1], 'rb').read() if k[0] == 'loose' else fpk.read(k[1], k[2], k[3])
