"""Checks the resource-icon helpers end to end on a synthetic mod: font_index_map.py finds the resource block, maps
FontButtonIndex to cells and reports a shared glyph; goods_batch.py makes framed buttons and glyphs (cutout, fill and
existing-button sources) into empty cells only; apply_font_patch.py reproduces the edited fonts and the buttons byte
for byte, refuses a filled cell and a damaged copy, and reports a second run as already applied. Markers and every pixel outside the new cells stay unchanged.
python tests/goods_check.py   (needs Node.js, Pillow, numpy and OpenCV)"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]; H = ROOT / 'helpers'
MAG, CYAN = (255, 0, 255, 255), (0, 255, 255, 255)


def font(path, cw, ch, glyphs):
    """A GameFont-like sheet: two rows of 25 symbol cells, then the resource block of 4 rows of 92 cells."""
    rows = [25, 25, 92, 92, 92, 92]
    W, Hh = 92 * (cw + 1) + 1, len(rows) * (ch + 1) + 1
    a = np.zeros((Hh, W, 4), np.uint8)
    for r, n in enumerate(rows):
        y0 = r * (ch + 1)
        a[y0, :] = MAG
        a[y0:y0 + ch + 2, n * (cw + 1):] = MAG  # the unused rest of a short row is marker colour
        for k in range(n + 1): a[y0:y0 + ch + 2, k * (cw + 1)] = CYAN if r % 2 else MAG
    a[-1, :] = MAG
    for k, g in glyphs.items():
        x, y = (k % 92) * (cw + 1) + 1, (2 + k // 92) * (ch + 1) + 1
        a[y:y + ch, x:x + cw] = np.asarray(g.resize((cw, ch), Image.LANCZOS))
    a[5 * (ch + 1) + 3, 1 * (cw + 1) + 4] = (0, 255, 255, 255)  # a stray marker-coloured pixel inside a cell of the block
    Image.fromarray(a, 'RGBA').save(path)


def obj(color, shape):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    (d.ellipse if shape == 'o' else d.rectangle)([12, 14, 52, 50], fill=color, outline=(30, 30, 30, 255))
    return im


def main():
    node = shutil.which('node') or sys.exit('needs Node.js')
    tmp = Path(tempfile.mkdtemp()); mod = tmp / 'mod'; A = mod / 'Assets'
    (A / 'res/Fonts').mkdir(parents=True); (A / 'XML/Art').mkdir(parents=True); (A / 'XML/Terrain').mkdir(parents=True)
    (A / 'Art/Interface/Buttons/Test').mkdir(parents=True)
    frame = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); ImageDraw.Draw(frame).rounded_rectangle([2, 2, 61, 61], 10, outline=(90, 95, 140, 255), width=2)
    colors = [((200, 40, 40, 255), 'o'), ((40, 160, 60, 255), 's'), ((40, 60, 200, 255), 'o'), ((220, 200, 40, 255), 's'), ((150, 90, 40, 255), 'o'), ((120, 120, 120, 255), 's')]
    art, bonus, glyph75, glyph = [], [], {}, {}
    for i, (c, s) in enumerate(colors):
        o = obj(c, s); b = o.copy(); b.alpha_composite(frame)
        raw = tmp / 'b.rgba'; np.asarray(b).tofile(raw)
        subprocess.run([node, str(H / 'core_bridge.js'), 'dds', str(raw), '64', '64', 'DXT3', str(A / f'Art/Interface/Buttons/Test/B{i}.dds')], check=True)
        idx = [0, 1, 2, 3, 4, 4][i]  # the last two share index 4
        art.append(f'<BonusArtInfo><Type>ART_DEF_BONUS_T{i}</Type><Button>Art/Interface/Buttons/Test/B{i}.dds</Button><FontButtonIndex>{idx}</FontButtonIndex></BonusArtInfo>')
        bonus.append(f'<BonusInfo><Type>BONUS_T{i}</Type><ArtDefineTag>ART_DEF_BONUS_T{i}</ArtDefineTag></BonusInfo>')
        if i < 5: glyph[idx] = o; glyph75[idx] = o
    bonus.append('<!-- <BonusInfo><Type>BONUS_OFF</Type><ArtDefineTag>ART_DEF_BONUS_T0</ArtDefineTag></BonusInfo> -->')
    (A / 'XML/Art/CIV4ArtDefines_Bonus.xml').write_text('<Civ4ArtDefines><BonusArtInfos>' + ''.join(art) + '</BonusArtInfos></Civ4ArtDefines>')
    (A / 'XML/Terrain/CIV4BonusInfos.xml').write_text('<Civ4BonusInfos><BonusInfos>' + ''.join(bonus) + '</BonusInfos></Civ4BonusInfos>')
    font(A / 'res/Fonts/GameFont.tga', 21, 20, glyph); font(A / 'res/Fonts/GameFont_75.tga', 16, 16, glyph75)

    r = subprocess.run([sys.executable, str(H / 'font_index_map.py'), str(mod), '--out', str(tmp / 'map.json')], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    m = json.loads((tmp / 'map.json').read_text())
    assert m['resources'] == 6, m['resources']  # the commented-out record does not count
    for f in m['fonts']:
        assert f['block_row'] == 3 and f['block_cells'] == 368, (f['block_row'], f['block_cells'])
        assert f['on_index'] >= 5, f['matches']
        assert f['free_unreferenced'][:3] == [5, 6, 7], f['free_unreferenced'][:3]
    assert list(m['shared_glyphs']) == ['4'] and len(m['shared_glyphs']['4']) == 2, m['shared_glyphs']

    photo = Image.new('RGB', (300, 200), (255, 255, 255)); d = ImageDraw.Draw(photo)
    d.ellipse([90, 40, 210, 160], fill=(170, 110, 50)); d.rectangle([0, 0, 60, 60], fill=(120, 70, 30))
    for x in range(0, 60, 6): d.line([(x, 0), (x, 60)], fill=(90, 50, 20))
    photo.save(tmp / 'photo.png')
    spec = dict(mod=str(mod), out=str(tmp / 'out'), goods=[
        dict(art='ART_DEF_BONUS_NEW1', font_index=5, button='Art/Interface/Buttons/Goods/New1.dds', source=dict(file='photo.png', title='synthetic', license='CC0'),
             make=dict(method='cutout', crop=[80, 30, 220, 170], key=dict(color=[255, 255, 255], tol=40))),
        dict(art='ART_DEF_BONUS_NEW2', font_index=6, button='Art/Interface/Buttons/Goods/New2.dds', source=dict(file='photo.png', title='synthetic', license='CC0'),
             make=dict(method='fill', shapes=[dict(circle=[0.5, 0.5, 0.4], crop=[0, 0, 60, 60])]), adjust=dict(tint=[255, 230, 200], smooth=1)),
        dict(art='ART_DEF_BONUS_T5', font_index=7, source=dict(button='Art/Interface/Buttons/Test/B5.dds'), make=dict(method='button'))])
    (tmp / 'spec.json').write_text(json.dumps(spec))
    r = subprocess.run([sys.executable, str(H / 'goods_batch.py'), str(tmp / 'spec.json')], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    out = tmp / 'out'; man = json.loads((out / 'ASSETS.json').read_text()); patch = json.loads((out / 'font_patch.json').read_text())
    assert len(man['goods']) == 3 and 'median of 6' in man['frame'], man['frame']
    for n in ('New1', 'New2'):
        b = np.asarray(Image.open(out / f'patch/Assets/Art/Interface/Buttons/Goods/{n}.dds').convert('RGBA')).astype(int)
        assert b.shape == (64, 64, 4) and b[32, 32, 3] == 255, n               # the object fills the middle
        assert np.abs(b[2, 20:44, :3] - [90, 95, 140]).max() < 24, n          # the frame of the mod's buttons
        assert b[0, 0, 3] == 0, n                                             # transparent corner
    for name, cw, ch in (('GameFont.tga', 21, 20), ('GameFont_75.tga', 16, 16)):
        before = np.asarray(Image.open(A / 'res/Fonts' / name).convert('RGBA')).astype(int)
        after = np.asarray(Image.open(out / 'fonts' / name).convert('RGBA')).astype(int)
        cells = patch['fonts'][name]['cells']; mask = np.zeros(before.shape[:2], bool)
        for c in cells: mask[c['y']:c['y'] + c['height'], c['x']:c['x'] + c['width']] = True
        assert (before[~mask] == after[~mask]).all(), name                       # nothing else changed
        mk = lambda a: ((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255)) | ((a[..., 0] == 0) & (a[..., 1] == 255) & (a[..., 2] == 255))
        assert (mk(before) == mk(after)).all(), name                             # markers neither lost nor added
        for c in cells: assert after[c['y']:c['y'] + c['height'], c['x']:c['x'] + c['width'], 3].max() > 0, (name, c['index'])
        assert [c['index'] for c in cells] == [5, 6, 7]
        g = after[cells[0]['y']:cells[0]['y'] + ch, cells[0]['x']:cells[0]['x'] + cw]
        assert g[..., 3].max() == 255 and (g[..., 3] == 0).any(), name           # an opaque object on a clear ground

    mod2 = tmp / 'mod2'; shutil.copytree(A / 'res/Fonts', mod2 / 'Assets/res/Fonts'); fonts2 = mod2 / 'Assets/res/Fonts'
    run = lambda *x: subprocess.run([sys.executable, str(H / 'apply_font_patch.py'), str(out / 'font_patch.json'), str(mod2), *x], capture_output=True, text=True)
    assert sorted(patch['files']) == ['Assets/Art/Interface/Buttons/Goods/New1.dds', 'Assets/Art/Interface/Buttons/Goods/New2.dds'], sorted(patch['files'])
    r = run('--check'); assert r.returncode == 0 and r.stdout.count('ready (exact original)') == 2 and r.stdout.count(': ready\n') == 2, r.stdout + r.stderr
    r = run(); assert r.returncode == 0 and r.stdout.count('written and verified') == 2 and r.stdout.count(': written\n') == 2, r.stdout + r.stderr
    for name in ('GameFont.tga', 'GameFont_75.tga'): assert (fonts2 / name).read_bytes() == (out / 'fonts' / name).read_bytes(), name
    for n in ('New1', 'New2'):
        rel = f'Art/Interface/Buttons/Goods/{n}.dds'
        assert (mod2 / 'Assets' / rel).read_bytes() == (out / 'patch/Assets' / rel).read_bytes(), n
    r = run(); assert r.returncode == 0 and r.stdout.count('already applied') == 2, r.stdout
    edited = bytearray((fonts2 / 'GameFont.tga').read_bytes()); edited[-30] ^= 1  # a patched font that differs elsewhere
    (fonts2 / 'GameFont.tga').write_bytes(bytes(edited))
    r = run('--check'); assert r.returncode != 0 and 'already holds artwork' in r.stdout + r.stderr, r.stdout + r.stderr
    damaged = json.loads((out / 'font_patch.json').read_text()); f = damaged['files']['Assets/Art/Interface/Buttons/Goods/New1.dds']
    f['zb64'] = __import__('base64').b64encode(__import__('zlib').compress(b'not the button')).decode()
    (tmp / 'damaged.json').write_text(json.dumps(damaged))
    r = subprocess.run([sys.executable, str(H / 'apply_font_patch.py'), str(tmp / 'damaged.json'), str(mod2)], capture_output=True, text=True)
    assert r.returncode != 0 and 'damaged' in r.stdout + r.stderr, r.stdout + r.stderr
    print('goods helpers: map, batch, buttons, glyphs and patch checked on a synthetic mod')
    shutil.rmtree(tmp)


if __name__ == '__main__':
    main()
