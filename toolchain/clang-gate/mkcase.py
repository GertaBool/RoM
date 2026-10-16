#!/usr/bin/env python3
"""Create case-variant symlinks so MSVC-style #include names resolve on Linux."""
import re, sys, os
from pathlib import Path
src = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
names = {p.name.lower(): p for p in src.iterdir() if p.is_file()}
for p in list(src.glob('*.cpp')) + list(src.glob('*.h')) + list(src.glob('*.inl')):
    for inc in re.findall(r'#\s*include\s*"([^"]+)"', p.read_text(errors='replace')):
        base = inc.replace('\\', '/').split('/')[-1]
        if not (src / base).exists() and base.lower() in names:
            link = out / base
            if not link.exists(): os.symlink(names[base.lower()].resolve(), link)
