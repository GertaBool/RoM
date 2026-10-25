#!/usr/bin/env python3
"""Print lines <from>-<to> of a C++ file with comments blanked, keeping line numbers (blank lines dropped).
usage: view.py <file> <from> <to>"""
import re, sys
s = open(sys.argv[1], encoding='latin-1').read()
s = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), s, flags=re.S)
s = re.sub(r'//[^\n]*', '', s)
a, b = int(sys.argv[2]), int(sys.argv[3])
for i, l in enumerate(s.split('\n')[a - 1:b], a):
    if l.strip(): print(f'{i}: {l.rstrip()}')
