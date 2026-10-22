#!/usr/bin/env python3
"""Refuse source patches that change line endings (fixes/*.patch).

usage: patchcheck.py <patch>...     errors on stderr, exit 1 if any
       patchcheck.py --selftest

A change block of a unified diff is a run of removed lines followed by added lines. An added line
that equals a removed line of its block once a trailing carriage return is dropped, but not before,
changes only its line ending. A patch with three or more such lines in one file is refused: an
editor or script rewrote the file's line endings along with the real change (the DLL sources use
CRLF), and the patch would carry thousands of lines that change nothing. Run by check_all.py.
"""
import collections, sys

LIMIT = 3


def line_ending_lines(text):
    """{file: number of added lines that differ from a removed line of their block only in a CR}."""
    out = collections.Counter()
    f, rem, add = None, [], []

    def flush():
        if rem and add:
            # per line content: pair removed and added lines with the same ending first; only what
            # is left over with the other ending on each side changed its line ending
            r = collections.Counter((x.rstrip('\r'), x.endswith('\r')) for x in rem)
            a = collections.Counter((x.rstrip('\r'), x.endswith('\r')) for x in add)
            for bare in {k for k, _ in a}:
                rcr, rlf, acr, alf = r[(bare, True)], r[(bare, False)], a[(bare, True)], a[(bare, False)]
                same_cr, same_lf = min(rcr, acr), min(rlf, alf)
                n = min(rcr - same_cr, alf - same_lf) + min(rlf - same_lf, acr - same_cr)
                if n: out[f] += n
        rem.clear(); add.clear()

    for line in text.split('\n'):
        if line.startswith('diff --git '):
            flush(); f = line.split(' b/', 1)[-1]
        elif line.startswith('--- ') or line.startswith('+++ '):
            flush()
        elif line.startswith('-'):
            if add: flush()
            rem.append(line[1:])
        elif line.startswith('+'):
            add.append(line[1:])
        else:
            flush()
    flush()
    return out


def errors(path):
    text = open(path, 'rb').read().decode('latin-1')
    return [f'{path}: {n} lines of {f} change only their line endings (rewrite the patch keeping the file\'s line endings)'
            for f, n in sorted(line_ending_lines(text).items()) if n >= LIMIT]


def selftest():
    crlf = ['int a;\r', 'int b;\r', 'int c;\r', 'int d;\r']
    def diff(old, new):
        return 'diff --git a/x.cpp b/x.cpp\n--- a/x.cpp\n+++ b/x.cpp\n@@ -1,4 +1,4 @@\n' + \
               ''.join(f'-{l}\n' for l in old) + ''.join(f'+{l}\n' for l in new)
    whole = diff(crlf, [l.rstrip('\r') for l in crlf])                                  # converted, nothing else
    mixed = diff(crlf, ['int a;', 'int b2;', 'int c;', 'int d;'])                        # converted with a real edit
    real = diff(crlf, ['int a;\r', 'int b2;\r', 'int c;\r', 'int d;\r'])                 # a real edit, endings kept
    assert line_ending_lines(whole) == {'x.cpp': 4}, line_ending_lines(whole)
    assert line_ending_lines(mixed) == {'x.cpp': 3}, line_ending_lines(mixed)
    assert not line_ending_lines(real), line_ending_lines(real)
    # repeated identical lines with the same ending on both sides change nothing (fixes/0005 has
    # blocks like this); a false positive here would refuse a correct patch
    repeated = diff(['{\r', '}\r', '{\r', 'x;\r'], ['{\r', '}\r', '{\r', '{\r', 'y;\r'])
    assert not line_ending_lines(repeated), line_ending_lines(repeated)
    print('patchcheck selftest: ok')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest(); sys.exit(0)
    errs = [e for p in sys.argv[1:] for e in errors(p)]
    for e in errs: print(e, file=sys.stderr)
    sys.exit(1 if errs else 0)
