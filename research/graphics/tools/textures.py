"""Every texture the mod ships (FPK members and loose files under Assets): format, size, mipmaps,
bytes once loaded, and identical copies.
usage: textures.py <mod Assets dir> <out.csv>
Loaded bytes: a DDS is uploaded as stored, so its data size counts; TGA/BMP/JPG are decoded to
32-bit with a full mip chain (4/3 of the top level) unless noted."""
import csv, hashlib, os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fpk

FOURCC_BPP = {b'DXT1': 4, b'DXT2': 8, b'DXT3': 8, b'DXT4': 8, b'DXT5': 8}

def dds_info(b):
    if b[:4] != b'DDS ' or len(b) < 128: return None
    h, w, pitch, depth, mips = struct.unpack_from('<5I', b, 12)
    flags, fourcc, bits, rm, gm, bm, am = struct.unpack_from('<I4s5I', b, 80)
    caps2 = struct.unpack_from('<I', b, 112)[0]
    if flags & 4: fmt = fourcc.decode('latin-1')
    else: fmt = ('A' if (flags & 1) and am else 'X') + str(bits)
    return dict(w=w, h=h, mips=max(mips, 1), fmt=fmt, cube=bool(caps2 & 0x200), data=len(b) - 128)

def tga_info(b):
    if len(b) < 18: return None
    w, h, bits = struct.unpack_from('<HHB', b, 12)
    return dict(w=w, h=h, mips=1, fmt='TGA%d' % bits, cube=False, data=w * h * 4 * 4 // 3)

def info(name, b):
    n = name.lower()
    if n.endswith('.dds'): return dds_info(b)
    if n.endswith('.tga'): return tga_info(b)
    return None

def walk(assets):
    for name in sorted(os.listdir(assets)):
        if name.lower().endswith('.fpk'):
            p = os.path.join(assets, name)
            for m, size, off in fpk.members(p):
                if m.lower().endswith(('.dds', '.tga')): yield name, m, fpk.read(p, size, off)
    for root, dirs, files in os.walk(assets):
        for f in files:
            if f.lower().endswith(('.dds', '.tga')):
                p = os.path.join(root, f); yield 'loose', os.path.relpath(p, assets).replace('\\', '/'), open(p, 'rb').read()

if __name__ == '__main__':
    assets, out = sys.argv[1:3]; rows = []; seen = {}
    for src, name, b in walk(assets):
        i = info(name, b)
        if i is None: i = dict(w=0, h=0, mips=0, fmt='unreadable', cube=False, data=len(b))
        h = hashlib.sha1(b).hexdigest()
        rows.append(dict(source=src, path=name.lower(), bytes=len(b), sha1=h, dup_of=seen.get(h, ''), **i))
        seen.setdefault(h, name.lower())
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print(len(rows), 'textures')
