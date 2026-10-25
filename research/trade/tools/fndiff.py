#!/usr/bin/env python3
"""Diff named functions of two C++ source trees (comments and blank lines removed, whitespace collapsed).
usage: fndiff.py <tree A> <tree B> <File.cpp>::<Class::function> ...   (prints a unified diff per function)"""
import difflib, re, sys

def body(path, name):
    s = open(path, encoding='latin-1').read()
    m = re.search(r'^[^\n;]*\b' + re.escape(name) + r'\s*\(', s, re.M)
    if not m: return None
    i = s.index('{', m.end()); d = 0
    for j in range(i, len(s)):
        d += {'{': 1, '}': -1}.get(s[j], 0)
        if d == 0: break
    text = s[m.start():j + 1]
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'//[^\n]*', '', text)
    return [re.sub(r'\s+', ' ', l).strip() for l in text.splitlines() if l.strip()]

A, B = sys.argv[1], sys.argv[2]
for spec in sys.argv[3:]:
    f, name = spec.split('::', 1)
    a, b = body(f'{A}/{f}', name), body(f'{B}/{f}', name)
    if a is None or b is None:
        print(f'== {name}: missing in {"A" if a is None else "B"}'); continue
    d = list(difflib.unified_diff(a, b, 'vanilla', 'rom', n=1, lineterm=''))
    print(f'== {name}: {len(a)} vs {len(b)} lines, {sum(1 for l in d if l[:1] in "+-" and l[:3] not in ("+++", "---"))} changed')
    for l in d[2:]: print('   ' + l)
