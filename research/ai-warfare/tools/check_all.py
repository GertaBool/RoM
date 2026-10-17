#!/usr/bin/env python3
"""Check every document under research/ai-warfare before a commit.

usage: check_all.py            all checks, exit 1 on any error
       check_all.py --render   render every template first, then check

1. Self-test: docs.py and figlib.py must reject each kind of fault they exist to catch
   (a typed number, an unknown figure, a unit outside figlib.UNITS, a table that drops values
   without a reason, a table of XML types without their effects, a stale input, a counted type
   with no XML record) and must pass a correct document.
2. Every <name>.md.in renders without errors, and <name>.md equals what it renders.
3. Every other .md is listed in UNCHECKED (documents written before the figure system), and
   UNCHECKED gains no entry against the last commit: a new document goes through a template.
Run by .claude/hooks/precommit.py and .githooks/pre-commit.
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # research/ai-warfare
REPO = os.path.dirname(os.path.dirname(ROOT))
sys.path.insert(0, HERE)
import docs, figlib


def selftest():
    errs = []
    with tempfile.TemporaryDirectory() as d:
        inp = os.path.join(d, 'in.csv'); open(inp, 'w').write('a,g\nX,1\nY,2\n')
        recs = {'ImprovementInfo': {'IMPROVEMENT_X': {'Type': 'IMPROVEMENT_X', 'YieldChanges': [0, 1, 0]},
                                    'IMPROVEMENT_Y': {'Type': 'IMPROVEMENT_Y', 'iUpgradeTime': 10}}}
        R = figlib.Registry(os.path.join(d, 'r.json'), [inp], recs)
        R.fig('n', 3, 'orders', 'human', '10-20', 'A lines')
        rows = [{'a': 'X', 'g': '1'}, {'a': 'Y', 'g': '2'}, {'a': 'X', 'g': '2'}]
        R.census_table('t', rows, 'a', 'tiles at save', 'all', 'save 285', 'tiles.csv', group='g', xml='ImprovementInfo')
        R.census_table('t2', rows, 'a', 'tiles at save', 'all', 'save 285', 'tiles.csv', show=['X'], reason='test')
        for bad, why in ((lambda: R.fig('u', 1, 'yield per tile', 'h', '1', 's'), 'unit outside UNITS'),
                         (lambda: R.fig('w', 1, 'orders', '', '1', 's'), 'missing who'),
                         (lambda: R.census_table('s', rows, 'a', 'tiles at save', 'h', '1', 's', show=['X']), 'dropped values, no reason'),
                         (lambda: R.census_table('x', rows + [{'a': 'Z', 'g': '1'}], 'a', 'tiles at save', 'h', '1', 's', xml='ImprovementInfo'), 'type without record'),
                         (lambda: R.fig('sh', 1, 'share', 'h', '1', 's'), 'share without n')):
            try: bad(); errs.append(f'selftest: figlib accepted {why}')
            except figlib.FigureError: pass
        R.save()
        cases = {
            'good': ('{{n}} orders.\n\n{{table:t}}\n\n{{effects:t}}\n\n{{table:t2}}\n', None),
            'number': ('The human gave 35 orders.\n', 'number:'),
            'id': ('{{nope}}\n', 'id:'),
            'effects': ('{{table:t}}\n', 'effects:'),
        }
        for name, (body, want) in cases.items():
            p = os.path.join(d, name + '.md.in'); open(p, 'w').write('<!-- registry: r.json -->\n' + body)
            _, e = docs.process(p)
            if want is None and e: errs.append(f'selftest: correct document rejected: {e}')
            if want and not any(x.startswith(want) for x in e): errs.append(f'selftest: {name} fault not caught: {e}')
        open(inp, 'a').write('Z,3\n')
        _, e = docs.process(os.path.join(d, 'good.md.in'))
        if not any(x.startswith('stale:') for x in e): errs.append('selftest: changed input not caught')
    return errs


def git_head(path):
    try:
        return subprocess.run(['git', '-C', REPO, 'show', 'HEAD:' + os.path.relpath(path, REPO)],
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None


def main():
    render = '--render' in sys.argv
    errs = selftest()
    ulist = os.path.join(ROOT, 'UNCHECKED')
    listed = {l.strip() for l in open(ulist) if l.strip() and not l.startswith('#')} if os.path.exists(ulist) else set()
    old = git_head(ulist)
    if old is not None:
        before = {l.strip() for l in old.split('\n') if l.strip() and not l.startswith('#')}
        for n in sorted(listed - before): errs.append(f'UNCHECKED: {n} added; new documents must be rendered from a template')
    for dp, dn, fn in os.walk(ROOT):
        for f in sorted(fn):
            p = os.path.join(dp, f); rel = os.path.relpath(p, ROOT)
            if f.endswith('.md.in'):
                body, e = docs.process(p)
                errs += [f'{rel}: {x}' for x in e]
                out = p[:-3]
                if render and not e: open(out, 'w', encoding='utf-8').write(body)
                if not os.path.exists(out): errs.append(f'{rel}: not rendered')
                elif open(out, encoding='utf-8').read() != body: errs.append(f'{rel[:-3]}: differs from its template (edited by hand, or not re-rendered)')
            elif f.endswith('.md') and not os.path.exists(p + '.in') and rel not in listed:
                errs.append(f'{rel}: neither rendered from a template nor listed in UNCHECKED')
    for n in sorted(listed):
        if not os.path.exists(os.path.join(ROOT, n)): errs.append(f'UNCHECKED: {n} does not exist; remove it from the list')
    for e in errs: print(e, file=sys.stderr)
    print(f'check_all: {len(errs)} error(s)', file=sys.stderr)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
