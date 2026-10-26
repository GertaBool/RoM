#!/usr/bin/env python3
"""Install an art patch (JSON) into a mod: glyph cells into GameFont.tga and GameFont_75.tga, and whole files such as
buttons. Standard library only, so it runs wherever the patch arrives through a channel that carries only text.

The patch (format 2) lists, per font file, the cells to fill (position, size, RGBA pixels compressed with zlib and
encoded in base64) and the SHA-256 of the file before and after; and per file (a path below the mod folder) its bytes,
compressed the same way, with their SHA-256. The script refuses a font that is not an uncompressed 32-bit TGA, writes
only into cells that hold no visible pixel, never overwrites a marker pixel (magenta or cyan grid lines), never
introduces a marker colour, keeps the header, image ID and trailing bytes, and, when the font was exactly the one the
patch was made from, checks that the result is byte for byte the expected file. It refuses a file whose bytes do not
match their SHA-256 and does not overwrite a different existing file. A backup of each font is written first, and a
second run reports what is already in place.
usage: apply_font_patch.py <patch.json> <mod folder> [--check]"""
import base64, hashlib, json, os, shutil, struct, sys, zlib


def unpack(s): return zlib.decompress(base64.b64decode(s))


def is_marker(r, g, b):
    return (r == 255 and g == 0 and b == 255) or (r == 0 and g == 255 and b == 255)


def load_tga(data):
    id_len, cmap, kind = data[0], data[1], data[2]
    w, h = struct.unpack_from('<HH', data, 12)
    bits, desc = data[16], data[17]
    if cmap or kind != 2 or bits != 32 or desc & 0xC0:
        raise SystemExit('not an uncompressed 32-bit TGA; use the original font files')
    start = 18 + id_len
    return w, h, desc, start


def offset(w, h, desc, start, x, y):
    """Byte offset of pixel (x, y), with y counted from the top of the image."""
    sx = w - 1 - x if desc & 16 else x
    sy = y if desc & 32 else h - 1 - y
    return start + (sy * w + sx) * 4


def apply_font(font_path, entry, check_only):
    data = bytearray(open(font_path, 'rb').read())
    before = hashlib.sha256(data).hexdigest()
    if before == entry['sha256_after']: return 'already applied'
    exact = before == entry['sha256_before']
    w, h, desc, start = load_tga(data)
    for c in entry['cells']:
        if c['x'] + c['width'] > w or c['y'] + c['height'] > h: raise SystemExit('%s: cell outside the image' % font_path)
        if len(unpack(c['rgba_zb64'])) != c['width'] * c['height'] * 4: raise SystemExit('%s: cell %d is damaged' % (font_path, c['index']))
        for y in range(c['y'], c['y'] + c['height']):
            for x in range(c['x'], c['x'] + c['width']):
                p = offset(w, h, desc, start, x, y)
                b, g, r, a = data[p:p + 4]
                if not is_marker(r, g, b) and a > 0:
                    raise SystemExit('%s: cell %d at %d,%d already holds artwork; this patch targets empty cells only' % (font_path, c['index'], c['x'], c['y']))
    if check_only:
        return 'ready (%s)' % ('exact original' if exact else 'different file, target cells empty')
    shutil.copyfile(font_path, font_path + '.before-font-patch')
    for c in entry['cells']:
        px = unpack(c['rgba_zb64'])
        for j in range(c['height']):
            for i in range(c['width']):
                p = offset(w, h, desc, start, c['x'] + i, c['y'] + j)
                b0, g0, r0, _ = data[p:p + 4]
                if is_marker(r0, g0, b0): continue
                q = (j * c['width'] + i) * 4
                r, g, b, a = px[q:q + 4]
                if is_marker(r, g, b): b = 254
                data[p:p + 4] = bytes((b, g, r, a))
    after = hashlib.sha256(data).hexdigest()
    if exact and after != entry['sha256_after']:
        shutil.copyfile(font_path + '.before-font-patch', font_path)
        raise SystemExit('%s: result differs from the expected file; original restored' % font_path)
    open(font_path, 'wb').write(data)
    return 'written%s; backup %s' % (' and verified' if exact else ' (font differed from the patch source: target cells were empty, result not hash-checked)', font_path + '.before-font-patch')


def apply_file(path, entry, check_only):
    data = unpack(entry['zb64'])
    if hashlib.sha256(data).hexdigest() != entry['sha256']: raise SystemExit('%s: the patch copy is damaged (SHA-256 differs)' % path)
    if os.path.exists(path):
        if hashlib.sha256(open(path, 'rb').read()).hexdigest() == entry['sha256']: return 'already in place'
        raise SystemExit('%s exists with other content; not overwritten' % path)
    if check_only: return 'ready'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(data)
    return 'written'


def main():
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    patch = json.load(open(sys.argv[1]))
    if patch.get('format') != 2: raise SystemExit('unknown patch format %s' % patch.get('format'))
    mod, check_only = sys.argv[2], '--check' in sys.argv[3:]
    for rel, entry in sorted(patch.get('files', {}).items()):  # all checked before any font is touched
        state = apply_file(os.path.join(mod, rel), entry, True)
        if check_only: print('%s: %s' % (rel, state))
    for name, entry in patch['fonts'].items():
        path = os.path.join(mod, 'Assets', 'res', 'Fonts', name)
        if not os.path.exists(path): raise SystemExit('missing ' + path)
        print('%s: %d cells: %s' % (name, len(entry['cells']), apply_font(path, entry, check_only)))
    if not check_only:
        for rel, entry in sorted(patch.get('files', {}).items()):
            print('%s: %s' % (rel, apply_file(os.path.join(mod, rel), entry, False)))


if __name__ == '__main__':
    main()
