#!/usr/bin/env python3
"""Emulate MSVC 7.1 legacy for-scope in a mirror: hoist `for (T X = ...` declarations
whose variable is used after the loop (reported by clang as undeclared) to just before the for.
usage: forscope.py <mirror-dir> <clang-log>..."""
import re, sys
from pathlib import Path
mirror = Path(sys.argv[1]); fixes = {}
for log in sys.argv[2:]:
    for line in open(log, errors='replace'):
        m = re.match(r"(\S+?\.cpp):(\d+):\d+: error: use of undeclared identifier '(\w+)'", line)
        if m: fixes.setdefault(m.group(1).lstrip('./'), set()).add((int(m.group(2)), m.group(3)))
for name, uses in fixes.items():
    p = mirror / name; lines = p.read_text(errors='replace').split('\n'); done = set()
    for ln, var in sorted(uses):
        pat = re.compile(r'for\s*\(\s*(int|unsigned int|short)\s+' + re.escape(var) + r'\b')
        for i in range(ln - 2, max(-1, ln - 400), -1):
            if pat.search(lines[i]):
                if i not in done:
                    t = pat.search(lines[i]).group(1)
                    lines[i] = pat.sub('{0} {1}; for ({1}'.format(t, var), lines[i], count=1)
                    # 'int X; for (X = ...' — keep same line count
                    lines[i] = lines[i].replace('for ({0}'.format(var), 'for ({0}'.format(var))
                    done.add(i)
                break
    p.write_text('\n'.join(lines))
    print(name, len(done), 'hoisted')
