"""Civ IV FPK packs: list and read members.
Layout (version 4): int32 version, b'FPK_', 1 byte, int32 count; per member: int32 name length,
the name with every byte plus one, zero padding to a multiple of 4, int64 timestamp, int32 size,
int32 offset from the start of the file."""
import struct, sys

def members(path):
    with open(path, 'rb') as f:
        head = f.read(13)
        version, magic, _, count = struct.unpack('<i4sBi', head)
        assert magic == b'FPK_' and version == 4, (version, magic)
        out = []
        for _ in range(count):
            n, = struct.unpack('<i', f.read(4))
            name = bytes(c - 1 for c in f.read(n)).decode('latin-1').replace('\\', '/')
            f.read((4 - n % 4) % 4)
            stamp, size, offset = struct.unpack('<qii', f.read(16))
            out.append((name, size, offset))
        return out

def read(path, size, offset):
    with open(path, 'rb') as f:
        f.seek(offset); return f.read(size)

if __name__ == '__main__':
    for name, size, offset in members(sys.argv[1])[:int(sys.argv[2]) if len(sys.argv) > 2 else None]:
        print(size, offset, name)
