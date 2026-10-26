#!/usr/bin/env python3
"""Map resource FontButtonIndex values to GameFont cells, with evidence.

The browser studio never infers a font index from a visual cell, because the mapping depends on the executable's
font reader and the DLL (in Rise of Mankind, CvBonusInfo::setChar adds 125). This helper establishes the mapping
for one mod from its own data instead of assuming it:

1. detects the glyph grid of GameFont.tga and GameFont_75.tga (the same marker rule as app/core.js detectCells);
2. takes a candidate resource block (by default the first row whose cells have the symbol size and that starts the
   bottom group of full rows) and numbers its cells in reading order;
3. reads every resource art define (modules included) and the resource buttons packed in the mod's FPK archives,
   and for each resource with a button compares the button, reduced to cell size, with every cell of the block;
4. reports how many resources land on cell = FontButtonIndex, against the number expected by chance, and lists
   the empty cells of the block, which are the slots a new resource can take;
5. reads the resource records (modules included) and lists every glyph that more than one resource shows.

It writes a JSON report and, with --sheet, a labelled contact sheet of the block for review. A strong match count is
evidence, not proof: check a new glyph in game at both font sizes before relying on it.
usage: font_index_map.py <mod folder> [--block-row N] [--out map.json] [--sheet prefix]"""
import argparse, glob, io, json, os, re, struct, sys

import numpy as np
from PIL import Image, ImageDraw


def read_rgba(path):
    return np.array(Image.open(path).convert('RGBA'))


def is_marker(px):
    r, g, b = px[..., 0].astype(int), px[..., 1].astype(int), px[..., 2].astype(int)
    return ((r == 255) & (g == 0) & (b == 255)) | ((r == 0) & (g == 255) & (b == 255))


def detect_cells(im):
    """Cells delimited by rows and columns made entirely of marker pixels; row and column numbers from 1."""
    m = is_marker(im)
    full_rows = m.all(axis=1)
    bands, start = [], None
    for y in range(im.shape[0] + 1):
        boundary = y == im.shape[0] or full_rows[y]
        if not boundary and start is None: start = y
        if boundary and start is not None: bands.append((start, y)); start = None
    cells = []
    for row, (top, bottom) in enumerate(bands, 1):
        cols = m[top:bottom].all(axis=0)
        left, col = None, 0
        for x in range(im.shape[1] + 1):
            boundary = x == im.shape[1] or cols[x]
            if not boundary and left is None: left = x
            if boundary and left is not None:
                col += 1
                if x - left <= 128 and bottom - top <= 128:
                    cells.append(dict(x=left, y=top, width=x - left, height=bottom - top, row=row, col=col))
                left = None
    return cells


def fpk_members(path):
    with open(path, 'rb') as f:
        head = f.read(13)
        if head[:4] == b'vers': return []  # a Git LFS pointer, not the archive
        version, magic, _, count = struct.unpack('<i4sBi', head)
        if magic != b'FPK_': return []
        out = []
        for _ in range(count):
            n, = struct.unpack('<i', f.read(4))
            name = bytes(c - 1 for c in f.read(n)).decode('latin-1').replace('\\', '/')
            f.read((4 - n % 4) % 4)
            _, size, offset = struct.unpack('<qii', f.read(16))
            out.append((name, size, offset))
        return out


def dds_rgba(b):
    h, w = struct.unpack_from('<II', b, 12)
    flags, fourcc, bits, rm, gm, bm, am = struct.unpack_from('<I4s5I', b, 80)
    if flags & 4: return np.array(Image.open(io.BytesIO(b)).convert('RGBA'))
    px = np.frombuffer(b, dtype='<u2' if bits == 16 else '<u4', count=w * h, offset=128).astype(np.uint32).reshape(h, w)

    def channel(mask):
        if not mask: return np.full((h, w), 255, np.uint8)
        shift = (mask & -mask).bit_length() - 1
        return (((px & mask) >> shift) * 255 // (mask >> shift)).astype(np.uint8)
    return np.dstack([channel(rm), channel(gm), channel(bm), channel(am)])


def packed_buttons(assets):
    found, lfs = {}, []
    for pak in sorted(glob.glob(os.path.join(assets, '*.FPK')) + glob.glob(os.path.join(assets, '*.fpk'))):
        members = fpk_members(pak)
        if not members and open(pak, 'rb').read(4) == b'vers': lfs.append(os.path.basename(pak)); continue
        with open(pak, 'rb') as f:
            for name, size, offset in members:
                n = name.lower()
                if n.endswith('.dds') and '/buttons/' in n:
                    f.seek(offset); found[n] = f.read(size)
    for root, _, files in os.walk(os.path.join(assets, 'Art')):
        for fn in files:
            if fn.lower().endswith('.dds'):
                p = os.path.join(root, fn); found[os.path.relpath(p, assets).replace('\\', '/').lower()] = open(p, 'rb').read()
    return found, lfs


def xml_text(path):
    """The file's text without XML comments, so that commented-out records do not count."""
    return re.sub(r'<!--.*?-->', '', open(path, encoding='latin-1').read(), flags=re.S)


def resource_art(assets):
    paths = [os.path.join(assets, 'XML', 'Art', 'CIV4ArtDefines_Bonus.xml')] + sorted(glob.glob(os.path.join(assets, 'Modules', '**', '*ArtDefines_Bonus.xml'), recursive=True))
    art = {}
    for p in paths:
        for b in re.findall(r'<BonusArtInfo>(.*?)</BonusArtInfo>', xml_text(p), re.S):
            t = re.search(r'<Type>(\w+)</Type>', b); fi = re.search(r'<FontButtonIndex>(\d+)</FontButtonIndex>', b); btn = re.search(r'<Button>([^<]*)</Button>', b)
            if not t: continue
            button = (btn.group(1) if btn else '').strip()
            path = (button.split(',')[1] if button.startswith(',') else button).strip().lower()
            art[t.group(1)] = dict(index=int(fi.group(1)) if fi else None, button=path)
    return art


def resource_records(assets):
    """Resource records (modules included; a later record of the same type replaces the earlier) and their art define."""
    paths = [os.path.join(assets, 'XML', 'Terrain', 'CIV4BonusInfos.xml')] + sorted(glob.glob(os.path.join(assets, 'Modules', '**', '*BonusInfos.xml'), recursive=True))
    records = {}
    for p in paths:
        for b in re.findall(r'<BonusInfo>(.*?)</BonusInfo>', xml_text(p), re.S):
            t = re.search(r'<Type>(\w+)</Type>', b); a = re.search(r'<ArtDefineTag>(\w+)</ArtDefineTag>', b)
            if t: records[t.group(1)] = a.group(1) if a else None
    return records


def shared_glyphs(records, art):
    """Font indices that more than one resource record shows, whether through one shared art define or two art
    defines with the same FontButtonIndex: the player cannot tell those resources apart in text."""
    by_index = {}
    for t, a in sorted(records.items()):
        idx = art.get(a, {}).get('index')
        if idx is not None: by_index.setdefault(idx, []).append(dict(resource=t, art=a))
    return {str(k): v for k, v in sorted(by_index.items()) if len(v) > 1}


def features(img, w, h):
    x = np.asarray(Image.fromarray(img).resize((w, h), Image.LANCZOS)).astype(float)
    return (x[..., :3] * x[..., 3:4] / 255).ravel()


def default_block_row(cells):
    """The first row of the last group of rows that share the symbol cell size and the widest cell count."""
    rows = {}
    for c in cells: rows.setdefault(c['row'], []).append(c)
    widest = max(len(v) for v in rows.values())
    full = [r for r, v in sorted(rows.items()) if len(v) == widest]
    group = [full[-1]]
    for r in reversed(full[:-1]):
        if r == group[0] - 1: group.insert(0, r)
        else: break
    return group[0]


def analyse(font_path, block_row, art, buttons):
    im = read_rgba(font_path)
    cells = detect_cells(im)
    row = block_row or default_block_row(cells)
    block = [c for c in cells if c['row'] >= row]
    w, h = block[0]['width'], block[0]['height']
    F = np.array([features(im[c['y']:c['y'] + c['height'], c['x']:c['x'] + c['width']], w, h) for c in block])
    known = [(t, a['index'], dds_rgba(buttons[a['button']])) for t, a in sorted(art.items()) if a['index'] is not None and a['button'] in buttons]
    matches = []
    for t, idx, img in known:
        d = np.linalg.norm(F - features(img, w, h), axis=1)
        best = int(np.argmin(d))
        matches.append(dict(art=t, index=idx, best_cell=best, on_index=best == idx))
    hits = sum(m['on_index'] for m in matches)
    empty = [k for k, c in enumerate(block) if not (im[c['y']:c['y'] + c['height'], c['x']:c['x'] + c['width'], 3] > 0).any()]
    used = sorted({a['index'] for a in art.values() if a['index'] is not None})
    return dict(font=os.path.basename(font_path), cells=len(cells), block_row=row, block_cells=len(block), cell_size=[w, h],
                compared=len(matches), on_index=hits, expected_by_chance=round(len(matches) / max(1, len(block)), 2), matches=matches,
                empty_cells=empty, free_unreferenced=[k for k in empty if k not in used],
                block=[dict(index=k, **c) for k, c in enumerate(block)]), im, block


def sheet(prefix, font, im, block, art, upto):
    names = {}
    for t, a in art.items():
        if a['index'] is not None: names.setdefault(a['index'], []).append(t.replace('ART_DEF_BONUS_', '')[:9])
    S, cols = 64, 12
    n = min(upto, len(block))
    out = Image.new('RGB', (cols * 110, ((n - 1) // cols + 1) * 96), (70, 70, 70)); d = ImageDraw.Draw(out)
    for k in range(n):
        c = block[k]
        g = Image.fromarray(im[c['y']:c['y'] + c['height'], c['x']:c['x'] + c['width']]).resize((S, S), Image.NEAREST)
        x, y = (k % cols) * 110 + 4, (k // cols) * 96 + 2
        bg = Image.new('RGBA', (S, S), (200, 200, 200, 255)); bg.alpha_composite(g); out.paste(bg.convert('RGB'), (x + 20, y))
        d.text((x, y + 66), '%d %s' % (k, '/'.join(names.get(k, ['-']))), fill=(255, 255, 255))
    path = '%s_%s.png' % (prefix, font.split('.')[0]); out.save(path); return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('mod'); ap.add_argument('--block-row', type=int); ap.add_argument('--out', default='font_index_map.json')
    ap.add_argument('--sheet'); ap.add_argument('--sheet-cells', type=int, default=120)
    a = ap.parse_args()
    assets = a.mod if os.path.basename(a.mod.rstrip('/\\')).lower() == 'assets' else os.path.join(a.mod, 'Assets')
    art = resource_art(assets)
    buttons, lfs = packed_buttons(assets)
    records = resource_records(assets)
    shared = shared_glyphs(records, art)
    report = dict(mod=os.path.abspath(a.mod), resources=len(records), art_defines=len(art), buttons_found=len(buttons), lfs_pointers=lfs,
                  shared_glyphs=shared, fonts=[])
    for name in ('GameFont.tga', 'GameFont_75.tga'):
        path = os.path.join(assets, 'res', 'Fonts', name)
        if not os.path.exists(path): continue
        r, im, block = analyse(path, a.block_row, art, buttons)
        if a.sheet: r['sheet'] = sheet(a.sheet, name, im, block, art, a.sheet_cells)
        report['fonts'].append(r)
        print('%s: %d cells; block from row %d, %d cells of %dx%d; %d of %d packed buttons match at cell = FontButtonIndex (chance %.2f); free cells from %s'
              % (name, r['cells'], r['block_row'], r['block_cells'], r['cell_size'][0], r['cell_size'][1], r['on_index'], r['compared'],
                 r['expected_by_chance'], r['free_unreferenced'][:6]))
    for k, v in shared.items(): print('glyph %s is shown by %s' % (k, ', '.join('%s (%s)' % (e['resource'], e['art']) for e in v)))
    if lfs: print('note: %s are Git LFS pointers; fetch them for more buttons to compare (git lfs pull --include ...)' % ', '.join(lfs))
    json.dump(report, open(a.out, 'w'), indent=1)


if __name__ == '__main__':
    main()
