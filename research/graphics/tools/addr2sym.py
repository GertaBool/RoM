#!/usr/bin/env python3
"""Map DLL addresses (as printed by Wine backtraces) to function names. usage: addr2sym.py <map> <addr>..."""
import re, sys, bisect, subprocess
syms = []
for l in open(sys.argv[1], errors='replace'):
    m = re.match(r'\s*[0-9a-f]{4}:[0-9a-f]{8}\s+(\S+)\s+([0-9a-f]{8})\s', l)
    if m: syms.append((int(m.group(2), 16), m.group(1)))
syms.sort()
keys = [s[0] for s in syms]
for a in sys.argv[2:]:
    a = int(a, 16)
    i = bisect.bisect_right(keys, a) - 1
    d = subprocess.run(['llvm-undname', syms[i][1]], capture_output=True, text=True).stdout.strip().split('\n')[-1]
    print('%08x +%x %s' % (a, a - syms[i][0], d[:220]))
