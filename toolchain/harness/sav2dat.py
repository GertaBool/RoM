#!/usr/bin/env python3
"""Split a BTS .CivBeyondSwordSave into the two inputs of HH_loadSave.

Layout (BTS 3.19 executable, save version 302):
  int version, string mod path, 7 ints, int length of the CvInitCore block,
  CvInitCore::write data, then the rest of the game as zlib data in blocks
  (int size, bytes; size 0 ends), then an engine trailer.
The CvInitCore block and the inflated stream are written unchanged.

usage: sav2dat.py <save> <out-prefix>   ->  <out-prefix>.init, <out-prefix>.game
"""
import struct
import sys
import zlib


def main(src, prefix):
    b = open(src, 'rb').read()
    pos = 0
    version = struct.unpack_from('<i', b, pos)[0]; pos += 4
    n = struct.unpack_from('<i', b, pos)[0]; pos += 4
    mod = b[pos:pos + n].decode('latin-1'); pos += n
    pos += 7 * 4
    init_len = struct.unpack_from('<i', b, pos)[0]; pos += 4
    init = b[pos:pos + init_len]
    pos += init_len
    # Blocks start at the first size field followed by a zlib header.
    while pos + 5 < len(b) and not (0 < struct.unpack_from('<i', b, pos)[0] <= 1 << 20 and b[pos + 4] == 0x78):
        pos += 4
    data = []
    while pos + 4 <= len(b):
        n = struct.unpack_from('<i', b, pos)[0]; pos += 4
        if n <= 0:
            break
        data.append(b[pos:pos + n]); pos += n
    game = zlib.decompressobj().decompress(b''.join(data))
    open(prefix + '.init', 'wb').write(init)
    open(prefix + '.game', 'wb').write(game)
    print('version %d, mod %s, init %d bytes, %d blocks, game stream %d bytes, trailer %d bytes'
          % (version, mod, len(init), len(data), len(game), len(b) - pos))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
