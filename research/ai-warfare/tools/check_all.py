#!/usr/bin/env python3
"""Check every document under research/ai-warfare before a commit.

usage: check_all.py            all checks, exit 1 on any error
       check_all.py --render   render every template first, then check

1. Self-test: docs.py and figlib.py must reject each kind of fault they exist to catch
   (a typed number, an unknown figure, a unit outside figlib.UNITS, a table that drops values
   without a reason, a table of XML types without their effects, a stale input, a counted type
   with no XML record) and must pass a correct document.
2. Every <name>.md.in renders without errors, and <name>.md equals what it renders.
3. Every registry (*.fig.json) whose inputs are all present is produced again by its recorded
   command into a temporary file, and must equal the committed one: figures are reproducible.
4. Every other .md is listed in UNCHECKED (documents written before the figure system), and
   UNCHECKED gains no entry against the last commit: a new document goes through a template.
5. The prediction register and commit gate (ledger.py): its self-test passes, the register and
   variables are valid and append-only, and every commit since the anchor keeps the commit rules.
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
        R.result_table('rt', ['k', 'type'], [['a', 'X'], ['b', 'Y']], 'orders', 'all', 'save 285', 'q', ['a', 'b'], n=2,
                       xml='ImprovementInfo', xml_vals=['X', 'Y'])
        for bad, why in ((lambda: R.fig('u', 1, 'yield per tile', 'h', '1', 's'), 'unit outside UNITS'),
                         (lambda: R.fig('w', 1, 'orders', '', '1', 's'), 'missing who'),
                         (lambda: R.census_table('s', rows, 'a', 'tiles at save', 'h', '1', 's', show=['X']), 'dropped values, no reason'),
                         (lambda: R.census_table('x', rows + [{'a': 'Z', 'g': '1'}], 'a', 'tiles at save', 'h', '1', 's', xml='ImprovementInfo'), 'type without record'),
                         (lambda: R.fig('sh', 1, 'share', 'h', '1', 's'), 'share without n'),
                         (lambda: R.census_table('m', rows, 'a', 'turn', 'h', '1', 's', value=len, stat='mean'), 'mean on an ordinal scale'),
                         (lambda: R.census_table('m2', rows, 'a', 'tiles at save', 'h', '1', 's', value=len), 'value without stat'),
                         (lambda: R.result_table('rx', ['k', 'type'], [['a', 'Z']], 'orders', 'h', '1', 's', ['a'], n=1,
                                                 xml='ImprovementInfo', xml_vals=['Z']), 'result type without record')):
            try: bad(); errs.append(f'selftest: figlib accepted {why}')
            except figlib.FigureError: pass
        R.save()
        cases = {
            'good': ('{{n}} orders ([[§17 Satz 1]], [[pp. 18–19]]).\n\n{{table:t}}\n\n{{effects:t}}\n\n{{table:t2}}\n\n{{table:rt}}\n\n{{effects:rt}}\n', None),
            'number': ('The human gave 35 orders.\n', 'number:'),
            'cite': ('A figure hidden in a citation: [[35 orders]].\n', 'number:'),
            'id': ('{{nope}}\n', 'id:'),
            'effects': ('{{table:t}}\n', 'effects:'),
            'result_effects': ('{{table:rt}}\n', 'effects:'),
        }
        for name, (body, want) in cases.items():
            p = os.path.join(d, name + '.md.in'); open(p, 'w').write('<!-- registry: r.json -->\n' + body)
            _, e = docs.process(p)
            if want is None and e: errs.append(f'selftest: correct document rejected: {e}')
            if want and not any(x.startswith(want) for x in e): errs.append(f'selftest: {name} fault not caught: {e}')
        dup = os.path.join(d, 'dup.md.in')
        open(dup, 'w').write('<!-- registry: r.json -->\n<!-- registry: r.json -->\n{{n}}\n')
        if not any('two registries' in x for x in docs.process(dup)[1]): errs.append('selftest: duplicate ids across registries not caught')
        al = os.path.join(d, 'alias.md.in')
        open(al, 'w').write('<!-- registry: r.json as one -->\n<!-- registry: r.json as two -->\n{{one.n}} {{two.n}}\n')
        if docs.process(al)[1]: errs.append(f'selftest: aliased registries rejected: {docs.process(al)[1]}')
        open(inp, 'a').write('Z,3\n')
        _, e = docs.process(os.path.join(d, 'good.md.in'))
        if not any(x.startswith('stale:') for x in e): errs.append('selftest: changed input not caught')
    return errs


def reproduce(path):
    d = json.load(open(path))
    cmd = d.get('command')
    if not cmd: return [f'{os.path.relpath(path, ROOT)}: no recorded command']
    for p in d['inputs']:
        a = p if os.path.isabs(p) else os.path.join(os.path.dirname(path), p)
        if not os.path.exists(a): return []          # inputs not on this machine: not checkable here
    with tempfile.TemporaryDirectory() as t:
        out = os.path.join(t, 'r.fig.json'); me = '@repo/' + os.path.relpath(path, REPO)
        args = [out if a == me else (os.path.join(REPO, a[6:]) if a.startswith('@repo/') else a) for a in cmd]
        py = os.path.expanduser('~/.cache/rom-ana/bin/python')   # the analysis toolkit (toolchain/analysis)
        r = subprocess.run([py if os.path.exists(py) else sys.executable] + args, capture_output=True, text=True, cwd=REPO)
        if r.returncode: return [f'{me}: producer failed: {r.stderr.strip()[-300:]}']
        e = json.load(open(out))
        return [f'{me}: not reproduced by its command ({k} differ)' for k in ('figures', 'xml') if e.get(k) != d.get(k)]


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
            if f.endswith('.fig.json'):
                errs += reproduce(p)
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
    # 5. The prediction register and commit gate (ledger.py): its self-test, then its checks.
    py = os.path.expanduser('~/.cache/rom-ana/bin/python')
    for args in (['--selftest'], ['check']):
        r = subprocess.run([py if os.path.exists(py) else sys.executable, os.path.join(HERE, 'ledger.py')] + args, capture_output=True, text=True)
        if r.returncode:
            errs += [l for l in r.stdout.splitlines() if l.strip()] or [f'ledger.py {args[0]}: {r.stderr.strip()[-400:]}']
    for e in errs: print(e, file=sys.stderr)
    print(f'check_all: {len(errs)} error(s)', file=sys.stderr)
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
