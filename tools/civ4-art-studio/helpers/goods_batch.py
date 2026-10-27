#!/usr/bin/env python3
"""Batch-make resource icons: a 64x64 DDS button and a glyph in both GameFont sheets per good, in the style of the
mod's own resource art.

The style is read from the mod, not assumed: the button frame is the median of the mod's resource buttons over their
outer band (every Civilization IV resource button carries the same bevelled frame), and glyphs show the object alone,
filling the cell, with a soft dark edge so they read on the parchment of the city and trade screens.

The spec (JSON) lists the mod folder, an output folder and the goods. Per good:
  art         the resource art define (e.g. ART_DEF_BONUS_DAIRY)
  font_index  its FontButtonIndex: the cell of the resource block it takes (see font_index_map.py); must be empty;
              omit (or null) for art without a glyph, such as an improvement's button
  button      the button path inside Assets (e.g. Art/Interface/Buttons/Goods/Dairy.dds); omit to keep the existing
              button (glyph only)
  source      the photograph: file, title, page, author, license (recorded in ASSETS.json); or {"button": "<path in
              Assets>"} to take the object from an existing button, so that glyph and button show the same thing
  make        how the object is cut from the source; crops are [x0, y0, x1, y1] in pixels, or fractions when all <= 1:
              {"method": "cutout", "crop": [...], "inset": 0.04, "hull": false}   GrabCut inside the crop, largest
                                                    region, holes filled; "hull" keeps the convex hull (for jars)
              {"method": "cutout", "crop": [...], "key": {"color": [r, g, b], "tol": 40}}   colour key
              {"method": "fill", "shapes": [...]}   shapes on a square canvas (fractions), each filled with photo texture:
                  {"circle": [cx, cy, r]} | {"ellipse": [cx, cy, rx, ry]} | {"poly": [[x, y], ...]}
                  with "crop" (the texture for this shape, stretched over its bounding box) and optional "shade"
              {"method": "button"}                  the object of an existing button (frame removed)
  adjust      optional {"saturation": 1.1, "contrast": 1.05, "brightness": 1.0, "tint": [r, g, b] (multiplies, 255 = none),
              "smooth": blur radius in master pixels, for textures whose grain turns to noise at glyph size}
Buttons and glyphs go through app/core.js (helpers/core_bridge.js): linear-light Lanczos resampling, the DDS writer,
and GameFont replacement that preserves markers and verifies every pixel. Outputs, under the output folder:
patch/Assets/... (buttons), fonts/ (both edited sheets), font_patch.json (glyph cells and buttons, for
apply_font_patch.py, so that a channel carrying only text can install them), ASSETS.json
(sources, licences, SHA-256 of every file), masters/ and preview.png.
usage: goods_batch.py <spec.json>"""
import base64, hashlib, json, os, subprocess, sys, tempfile, zlib

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import font_index_map as fim

MASTER = 256   # working size of the object image
BAND = 6       # outer band of a 64x64 button that holds the frame
FILL = 0.80    # share of the button the object may take


def bridge(*args):
    r = subprocess.run(['node', os.path.join(HERE, 'core_bridge.js')] + [str(a) for a in args], capture_output=True, text=True)
    if r.returncode: raise SystemExit('core_bridge %s failed: %s' % (args[0], r.stderr.strip()[-400:]))
    return r.stdout.strip()


def box_px(im, box):
    w, h = im.size
    if all(v <= 1 for v in box): box = [box[0] * w, box[1] * h, box[2] * w, box[3] * h]
    return tuple(int(round(v)) for v in box)


def band_mask():
    y, x = np.mgrid[:64, :64]
    return np.minimum(np.minimum(x, 63 - x), np.minimum(y, 63 - y)) < BAND


def button_frame(buttons):
    """The frame shared by the mod's 64x64 resource buttons: their per-pixel median over the outer band."""
    imgs = [fim.dds_rgba(b) for b in buttons.values()]
    imgs = [i for i in imgs if i.shape == (64, 64, 4)]
    if len(imgs) < 5: raise SystemExit('too few 64x64 resource buttons to read the frame from (%d)' % len(imgs))
    med = np.median(np.stack(imgs).astype(float), axis=0)
    med[~band_mask()] = 0
    return Image.fromarray(med.round().astype(np.uint8), 'RGBA'), len(imgs)


def inner_mask(radius=10):
    """The inside of the frame: a rounded square inset by the band, whose corners follow the frame's."""
    y, x = np.mgrid[:64, :64].astype(float)
    lo, hi = BAND + radius, 63 - BAND - radius
    dx, dy = np.maximum(0, np.maximum(lo - x, x - hi)), np.maximum(0, np.maximum(lo - y, y - hi))
    return np.hypot(dx, dy) <= radius


def object_from_button(rgba):
    """The object of a button: what lies inside the frame."""
    a = np.array(rgba)
    a[~inner_mask(), 3] = 0
    im = Image.fromarray(a, 'RGBA')
    return im.crop(im.getbbox())


def cutout(src, make):
    im = src.crop(box_px(src, make.get('crop', [0, 0, 1, 1]))).convert('RGB')
    a = np.asarray(im)
    if 'key' in make:
        dist = np.linalg.norm(a.astype(float) - np.array(make['key']['color'], float), axis=2)
        mask = (dist > make['key'].get('tol', 40)).astype(np.uint8)
    else:
        import cv2
        h, w = a.shape[:2]
        m = np.zeros((h, w), np.uint8)
        inset = make.get('inset', 0.04)
        rect = (int(w * inset), int(h * inset), int(w * (1 - 2 * inset)), int(h * (1 - 2 * inset)))
        cv2.grabCut(cv2.cvtColor(a, cv2.COLOR_RGB2BGR), m, rect, np.zeros((1, 65)), np.zeros((1, 65)), 8, cv2.GC_INIT_WITH_RECT)
        mask = ((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD)).astype(np.uint8)
        k = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(cv2.morphologyEx(mask, cv2.MORPH_OPEN, k), cv2.MORPH_CLOSE, k)
        n, lab, stats, _ = cv2.connectedComponentsWithStats(mask)
        if n > 1: mask = (lab == 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)
        # background enclosed by the object belongs to it
        n, lab, stats, _ = cv2.connectedComponentsWithStats((1 - mask).astype(np.uint8))
        for i in range(1, n):
            x, y, ww, hh, _ = stats[i]
            if x > 0 and y > 0 and x + ww < w and y + hh < h: mask[lab == i] = 1
        if make.get('hull'):  # convex objects (jars, bottles): parts that match the background, such as a white label, stay in
            pts = cv2.findNonZero(mask)
            cv2.fillPoly(mask, [cv2.convexHull(pts)], 1)
    alpha = Image.fromarray(mask * 255).filter(ImageFilter.GaussianBlur(1.0))
    rgba = im.convert('RGBA'); rgba.putalpha(alpha)
    return rgba.crop(rgba.getbbox())


def fill(src, make):
    """Shapes filled with texture from the photograph, painted in order, each with a darker rim for volume."""
    S = MASTER * 2
    out = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    for s in make['shapes']:
        mask = Image.new('L', (S, S), 0); d = ImageDraw.Draw(mask)
        if 'circle' in s: cx, cy, r = s['circle']; d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=255)
        if 'ellipse' in s: cx, cy, rx, ry = s['ellipse']; d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=255)
        if 'poly' in s: d.polygon([(x * S, y * S) for x, y in s['poly']], fill=255)
        bb = mask.getbbox()
        tex = src.crop(box_px(src, s.get('crop', make.get('crop', [0, 0, 1, 1])))).convert('RGB').resize((bb[2] - bb[0], bb[3] - bb[1]), Image.LANCZOS)
        layer = Image.new('RGB', (S, S)); layer.paste(tex, bb[:2])
        m = np.asarray(mask, float) / 255
        edge = np.clip(m - np.asarray(mask.filter(ImageFilter.GaussianBlur(S * s.get('rim', 0.025))), float) / 255, 0, 1)
        rgb = np.asarray(layer, float) * s.get('shade', 1.0) * (1 - s.get('rim_dark', 0.45) * np.clip(edge * 2, 0, 1)[..., None])
        piece = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert('RGBA')
        piece.putalpha(mask.filter(ImageFilter.GaussianBlur(1.0)))
        out.alpha_composite(piece)
    return out.crop(out.getbbox())


def adjust(subject, adj):
    if not adj: return subject
    rgb, a = subject.convert('RGB'), subject.getchannel('A')
    rgb = ImageEnhance.Color(rgb).enhance(adj.get('saturation', 1))
    rgb = ImageEnhance.Contrast(rgb).enhance(adj.get('contrast', 1))
    rgb = ImageEnhance.Brightness(rgb).enhance(adj.get('brightness', 1))
    if 'smooth' in adj: rgb = rgb.filter(ImageFilter.GaussianBlur(adj['smooth']))
    if 'tint' in adj: rgb = Image.fromarray(np.clip(np.asarray(rgb, float) * np.array(adj['tint'], float) / 255, 0, 255).astype(np.uint8))
    out = rgb.convert('RGBA'); out.putalpha(a); return out


def master_of(subject):
    """The object centred on a square transparent canvas, taking FILL of it."""
    box = int(MASTER * FILL)
    s = min(box / subject.width, box / subject.height)
    sub = subject.resize((max(1, round(subject.width * s)), max(1, round(subject.height * s))), Image.LANCZOS)
    canvas = Image.new('RGBA', (MASTER, MASTER), (0, 0, 0, 0))
    canvas.alpha_composite(sub, ((MASTER - sub.width) // 2, (MASTER - sub.height) // 2))
    return canvas


def to_rgba_file(im, path):
    np.asarray(im.convert('RGBA'), np.uint8).tofile(path); return path


def resample(im, w, h, tmp):
    src = to_rgba_file(im, os.path.join(tmp, 'in.rgba')); out = os.path.join(tmp, 'out.rgba')
    bridge('resample', src, im.width, im.height, w, h, out)
    return Image.frombuffer('RGBA', (w, h), open(out, 'rb').read(), 'raw', 'RGBA', 0, 1).copy()


def button_of(master, frame, tmp):
    b = resample(master, 64, 64, tmp)
    b.alpha_composite(frame)
    return b


def glyph(subject, cw, ch, tmp):
    """The object fitted to the cell (one pixel kept free left and right, as the mod's glyphs do), standing on the
    cell's bottom, crisped for its size, over a soft dark edge."""
    bw, bh = cw - 2, ch - 1
    s = min(bw / subject.width, bh / subject.height)
    w, h = max(1, round(subject.width * s)), max(1, round(subject.height * s))
    g = resample(subject, w, h, tmp)
    rgb, a = g.convert('RGB'), g.getchannel('A')
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=0.6, percent=70, threshold=1))
    g = rgb.convert('RGBA'); g.putalpha(a)
    x, y = (cw - w) // 2, ch - 1 - h + (1 if h < bh else 0)
    halo = Image.new('L', (cw, ch), 0); halo.paste(a, (x, y))
    halo = halo.filter(ImageFilter.MaxFilter(3)).point(lambda v: int(v * 0.55))
    cell = Image.new('RGBA', (cw, ch), (24, 18, 12, 0)); cell.putalpha(halo)
    cell.alpha_composite(g, (x, y))
    return cell


def sha(path): return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def pack(data): return base64.b64encode(zlib.compress(data, 9)).decode()


def main():
    if len(sys.argv) != 2: raise SystemExit(__doc__)
    spec = json.load(open(sys.argv[1])); base = os.path.dirname(os.path.abspath(sys.argv[1]))
    mod, out = spec['mod'], spec['out']
    assets = os.path.join(mod, 'Assets')
    for d in ('fonts', 'masters'): os.makedirs(os.path.join(out, d), exist_ok=True)
    tmp = tempfile.mkdtemp()
    buttons, _ = fim.packed_buttons(assets)
    art = fim.resource_art(assets)
    frame, nframe = button_frame({a['button']: buttons[a['button']] for a in art.values() if a['button'] in buttons})
    frame.save(os.path.join(out, 'masters', 'frame.png'))
    manifest = dict(made_by='tools/civ4-art-studio/helpers/goods_batch.py',
                    frame='median of %d resource buttons of the mod over their outer %d pixels' % (nframe, BAND), goods=[])
    fonts = {}
    for name in ('GameFont.tga', 'GameFont_75.tga'):
        path = os.path.join(assets, 'res', 'Fonts', name)
        cells = fim.detect_cells(fim.read_rgba(path))
        row = spec.get('block_row') or fim.default_block_row(cells)
        fonts[name] = dict(path=path, block=[c for c in cells if c['row'] >= row], edits=[], patch=[])
    previews = []
    for g in spec['goods']:
        if g['make']['method'] == 'button':
            subject = object_from_button(Image.fromarray(fim.dds_rgba(buttons[g['source']['button'].lower()])))
        else:
            src = Image.open(os.path.join(base, g['source']['file'])).convert('RGB')
            subject = cutout(src, g['make']) if g['make']['method'] == 'cutout' else fill(src, g['make'])
        subject = adjust(subject, g.get('adjust'))
        master = master_of(subject)
        master.save(os.path.join(out, 'masters', g['art'] + '.png'))
        entry = dict(art=g['art'], font_index=g.get('font_index'), source=g['source'], make=g['make'])
        button = None
        if g.get('button'):
            button = button_of(master, frame, tmp)
            bpath = os.path.join(out, 'patch', 'Assets', g['button']); os.makedirs(os.path.dirname(bpath), exist_ok=True)
            bridge('dds', to_rgba_file(button, os.path.join(tmp, 'b.rgba')), 64, 64, spec.get('dds', 'DXT3'), bpath)
            entry.update(button=g['button'], button_sha256=sha(bpath))
        glyphs = {}
        for name, f in (fonts.items() if g.get('font_index') is not None else []):
            c = f['block'][g['font_index']]
            cell = glyph(subject, c['width'], c['height'], tmp)
            rp = to_rgba_file(cell, os.path.join(tmp, '%s_%s.rgba' % (name, g['art'])))
            f['edits'].append(dict(cell=dict(x=c['x'], y=c['y'], width=c['width'], height=c['height']), rgba=rp))
            f['patch'].append(dict(index=g['font_index'], art=g['art'], x=c['x'], y=c['y'], width=c['width'], height=c['height'],
                                   rgba_zb64=pack(open(rp, 'rb').read())))
            glyphs[name] = cell
        manifest['goods'].append(entry); previews.append((g, master, button, glyphs))
    patch = dict(format=2, made_by=manifest['made_by'], fonts={}, files={})
    for e in manifest['goods']:
        if 'button' in e:
            data = open(os.path.join(out, 'patch', 'Assets', e['button']), 'rb').read()
            patch['files']['Assets/' + e['button']] = dict(sha256=hashlib.sha256(data).hexdigest(), zb64=pack(data))
    for name, f in fonts.items():
        if not f['edits']: continue   # no glyph in this batch: the font stays as it is
        ej = os.path.join(tmp, name + '.json'); json.dump(f['edits'], open(ej, 'w'))
        dst = os.path.join(out, 'fonts', name)
        report = json.loads(bridge('font', f['path'], ej, dst))
        patch['fonts'][name] = dict(sha256_before=sha(f['path']), sha256_after=sha(dst), cells=f['patch'], check=report)
        manifest.setdefault('fonts', {})[name] = dict(sha256_before=patch['fonts'][name]['sha256_before'],
                                                      sha256_after=patch['fonts'][name]['sha256_after'], **report)
    json.dump(patch, open(os.path.join(out, 'font_patch.json'), 'w'), indent=1)
    json.dump(manifest, open(os.path.join(out, 'ASSETS.json'), 'w'), indent=1, ensure_ascii=False)
    preview(out, previews, fonts)
    print('%d goods; buttons under %s; fonts, font_patch.json, ASSETS.json and preview.png in %s' % (len(previews), os.path.join(out, 'patch'), out))


def preview(out, items, fonts):
    """Per good: the master, the button on dark and on parchment, and each glyph among font neighbours on parchment
    (enlarged above, actual size below)."""
    rowh, W, parch = 130, 1240, (205, 200, 185, 255)
    sheet = Image.new('RGB', (W, rowh * len(items) + 8), (52, 52, 52)); d = ImageDraw.Draw(sheet)
    srcs = {name: Image.open(f['path']).convert('RGBA') for name, f in fonts.items()}
    for i, (g, master, button, glyphs) in enumerate(items):
        y = i * rowh + 6
        m = master.resize((96, 96), Image.LANCZOS); sheet.paste(m, (6, y), m)
        if button is not None:
            for j, bg in enumerate(((24, 24, 24, 255), parch)):
                t = Image.new('RGBA', (64, 64), bg); t.alpha_composite(button); sheet.paste(t.convert('RGB'), (110 + j * 70, y + 4))
        x = 260
        for name, cell in glyphs.items():
            f, k = fonts[name], g['font_index']
            strip = Image.new('RGBA', (cell.width * 9, cell.height), parch)
            for n, kk in enumerate([99, 100, 101, 102, 104, k, 3, 12, 18]):
                c = f['block'][kk]
                im = cell if kk == k else srcs[name].crop((c['x'], c['y'], c['x'] + c['width'], c['y'] + c['height']))
                strip.alpha_composite(im, (n * cell.width, 0))
            z = 3 if cell.height > 16 else 4
            big = strip.resize((strip.width * z, strip.height * z), Image.NEAREST)
            sheet.paste(big.convert('RGB'), (x, y))
            sheet.paste(strip.convert('RGB'), (x, y + big.height + 6))
            x += big.width + 20
        d.text((6, y + 104), '%s  cell %s  %s (%s)' % (g['art'], g.get('font_index', '-'), g['source'].get('title', g['source'].get('button', ''))[:70],
                                                      g['source'].get('license', 'existing button')), fill=(235, 235, 235))
    sheet.save(os.path.join(out, 'preview.png'))


if __name__ == '__main__':
    main()
