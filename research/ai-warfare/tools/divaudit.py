#!/usr/bin/env python3
"""Find integer percentage scalings in the DLL that can truncate a modifier to no effect.

usage: divaudit.py <CvGameCoreDLL source dir> [--all]

Syntactic scan (tree-sitter C++, no headers needed) for divisions by an integer literal 100,
and for compound `x /= 100`. Each hit is printed with file:line, the enclosing function and the
expression. A hit is flagged SMALL when the dividend multiplies a literal of 1..9, or a variable
named like a rate, count or 1 (`iRate = 1`), with a modifier term: those are the cases where
(100 + m) / 100 truncates every m under 100 (framework.md, section 8). Without --all only
flagged hits are printed; the totals are printed in every case.
Facts only: whether a flagged line is a bug depends on what the value is used for.
"""
import os, re, sys

import tree_sitter_cpp
from tree_sitter import Language, Parser

P = Parser(Language(tree_sitter_cpp.language()))
SMALL_VAR = re.compile(r'\b(iRate|iCount|iNum\w*|iTurns?\w*)\b')


def func_name(n):
    while n is not None and n.type != 'function_definition': n = n.parent
    if n is None: return '?'
    d = n.child_by_field_name('declarator')
    return d.text.decode(errors='replace').split('(')[0] if d else '?'


def walk(n):
    yield n
    for c in n.children: yield from walk(c)


def main():
    src, show_all = sys.argv[1], '--all' in sys.argv
    tot = flagged = 0
    for f in sorted(os.listdir(src)):
        if not f.endswith(('.cpp', '.h')): continue
        code = open(os.path.join(src, f), 'rb').read()
        tree = P.parse(code)
        lines = code.split(b'\n')
        for n in walk(tree.root_node):
            hit = None
            if n.type == 'binary_expression' and n.child_by_field_name('operator').type == '/':
                r = n.child_by_field_name('right')
                if r.type == 'number_literal' and r.text == b'100': hit = n
            elif n.type == 'assignment_expression' and n.child_by_field_name('operator').type == '/=':
                r = n.child_by_field_name('right')
                if r.type == 'number_literal' and r.text == b'100': hit = n
            if hit is None: continue
            tot += 1
            ln = hit.start_point[0]
            ctx = b' '.join(l.strip() for l in lines[max(0, ln - 3):ln + 1]).decode(errors='replace')
            small = bool(re.search(r'=\s*[1-9]\s*;', ctx) and '100 +' in ctx.replace('(100 +', '100 +')) or (
                bool(SMALL_VAR.search(ctx)) and 'Modifier' in ctx)
            flagged += small
            if small or show_all:
                print(f'{"SMALL " if small else ""}{f}:{ln + 1} {func_name(hit)}: {hit.text.decode(errors="replace")[:100]}')
    print(f'{tot} integer divisions by 100; {flagged} flagged SMALL', file=sys.stderr)


if __name__ == '__main__':
    main()
