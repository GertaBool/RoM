#!/usr/bin/env python3
"""Render the map (map/*.tsv) as Markdown pages: an overview, the entry points, the Python side, and one
outline page per source file.

usage: render.py <codemap dir> <source commit> <ctags tsv>

Writes <codemap dir>/skeleton.md, entry_points.md, python.md, files/<source file>.md and
map/completeness.tsv. Every count on the pages is computed here from the map; nothing is typed in.
"""
import collections, csv, os, re, sys

GROUPS = [   # (group, rule on the file name without extension); first match wins; by name only
    ('engine interface', r'^(CvDLL\w*IFaceBase|FDataStreamBase)$'),
    ('Python wrappers', r'^Cy'),
    ('AI', r'(^AI|AI$|^BetterBTSAI$)'),
    ('game objects', r'^Cv(Game|Player|Team|City|Unit|SelectionGroup|Plot|PlotGroup|Map|Area|Deal)$'),
    ('game data and XML loading', r'^Cv(Infos|InfoWater|XMLLoadUtility\w*|Globals|ArtFileMgr|InitCore)$'),
    ('interface, text and messages', r'^Cv(DLLWidgetData|GameTextMgr|DLLButtonPopup|Popup\w+|TalkingHeadMessage|'
                                     r'DiploParameters|Message\w+|Replay\w+|HallOfFameInfo|Statistics|EventReporter|'
                                     r'DllPythonEvents|DllTranslator)$'),
    ('other', r''),
]
SUBST = 5   # backbone: a callee is shown when it calls at least this many different functions of the source
TURN = {'update', 'doTurn', 'AI_doTurn', 'AI_doTurnPre', 'AI_doTurnPost', 'AI_doTurnUnitsPre', 'AI_doTurnUnitsPost',
        'AI_update', 'doTurnUnits'}


def read(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def group(file):
    m = os.path.splitext(file)[0]
    return next(g for g, r in GROUPS if re.search(r, m))


def main():
    root, commit, ctags = sys.argv[1], sys.argv[2], sys.argv[3]
    M = os.path.join(root, 'map')
    F = {int(r['id']): r for r in read(os.path.join(M, 'functions.tsv'))}
    calls = read(os.path.join(M, 'calls.tsv'))
    over = read(os.path.join(M, 'overrides.tsv'))
    pydefs = read(os.path.join(M, 'python_defs.tsv'))
    pycalls = read(os.path.join(M, 'cpp_to_py.tsv'))
    evh = read(os.path.join(M, 'event_handlers.tsv'))
    units = read(os.path.join(M, 'units.tsv'))
    bases = read(os.path.join(M, 'bases.tsv'))
    classes = read(os.path.join(M, 'classes.tsv'))
    pyf = read(os.path.join(M, 'py_functions.tsv'))
    p2c = read(os.path.join(M, 'py_to_cpp.tsv'))

    count = collections.Counter((F[i]['scope'], F[i]['name']) for i in F)

    def short(i):
        r = F[i]; s = r['scope'] + '::' if r['scope'] else ''
        return s + (r['sig'] if count[(r['scope'], r['name'])] > 1 else r['name'])

    callees = collections.defaultdict(list); callers = collections.defaultdict(set); refs = collections.defaultdict(list)
    objcls = collections.defaultdict(set)   # (caller, callee) -> the object's class of a virtual call, '' if not known
    for c in calls:
        a, b = int(c['caller']), int(c['callee'])
        (refs if c['kind'] == 'ref' else callees)[a].append(b); callers[b].add(a)
        if c['kind'] == 'virtual': objcls[(a, b)].add(c['object_class'])
    overriders = collections.defaultdict(set); overrides = collections.defaultdict(set)
    for o in over: overriders[int(o['overrides'])].add(int(o['method'])); overrides[int(o['method'])].add(int(o['overrides']))
    def closure(i, seen=None):   # every method that may run for a call to i: overrides of overrides too
        seen = set() if seen is None else seen
        for o in overriders.get(i, ()):
            if o not in seen: seen.add(o); closure(o, seen)
        return seen
    overriders = {b: closure(b) for b in list(overriders)}
    parents = collections.defaultdict(set)
    for b in read(os.path.join(M, 'bases.tsv')): parents[b['class']].add(b['base'])
    def ancestors(c, seen=None):
        seen = {c} if seen is None else seen
        for p in parents.get(c, ()):
            if p not in seen: seen.add(p); ancestors(p, seen)
        return seen
    def may_run(a, b):   # the overrides of b that a's call may reach: those of the object's class and below
        cls = objcls.get((a, b))   # a direct call runs b itself (the compiler knew the object's class)
        if not cls: return []
        if '' in cls: return sorted(overriders.get(b, ()))
        return sorted(o for o in overriders.get(b, ()) if cls & ancestors(F[o]['scope']))
    pyname = collections.defaultdict(list)
    for p in pydefs: pyname[int(p['function'])].append(p['python_name'])
    defs = [i for i in F if F[i]['definition'] == '1']
    derived = {b['base'] for b in read(os.path.join(M, 'bases.tsv'))}   # classes with a subclass in the source
    def from_exe(i):   # a pure virtual the source never implements, in a class the source never derives from
        return F[i]['pure'] == '1' and not overriders.get(i) and F[i]['scope'] not in derived

    # completeness against ctags (functions the compiler wrote itself have no source line and are left out)
    def nn(x): return re.sub(r'<[^()]*>$', '', x).replace(' ', '')
    written = [i for i in defs if F[i]['line']]
    have = collections.defaultdict(list)
    for i in written: have[(F[i]['file'], nn(F[i]['name']))].append(int(F[i]['line']))
    ct = [l.rstrip('\n').split('\t') for l in open(ctags, encoding='utf-8') if l.strip()]
    ct_only = sorted((f, int(l), n) for n, f, l in ct if not any(abs(x - int(l)) <= 3 for x in have.get((f, nn(n)), [])))
    tags = collections.defaultdict(list)
    for n, f, l in ct: tags[(f, nn(n))].append(int(l))
    compiled_only = [i for i in written if not any(abs(x - int(F[i]['line'])) <= 3 for x in tags.get((F[i]['file'], nn(F[i]['name'])), []))]
    with open(os.path.join(M, 'completeness.tsv'), 'w', encoding='utf-8') as o:
        o.write('found_by\tfile\tline\tname\n')
        for f, l, n in ct_only: o.write(f'ctags only\t{f}\t{l}\t{n}\n')
        for i in sorted(compiled_only, key=lambda i: (F[i]['file'], int(F[i]['line']), i)):
            o.write(f"compiled only\t{F[i]['file']}\t{F[i]['line']}\t{short(i)}\n")

    # file and group level linkage
    G = {i: group(F[i]['file']) for i in F}
    gl = collections.Counter(); fl = collections.Counter()
    for c in calls:
        a, b = int(c['caller']), int(c['callee'])
        gl[(G[a], G[b])] += 1
        if F[a]['file'] != F[b]['file']: fl[(F[a]['file'], F[b]['file'])] += 1
    files = sorted({F[i]['file'] for i in F})   # files that define or declare functions
    gnames = [g for g, _ in GROUPS]

    S = []
    S.append('# Skeleton of the DLL\n')
    S.append(f'Generated by `codemap/tool/build.sh` from the GitLab source at commit `{commit}`, compiled by the '
             'real compiler (Visual C++ Toolkit 2003) with the release build\'s defines and no inlining. Counts below '
             'are computed from `map/`. How it was made and its limits: `README.md`.\n')
    S.append('## Size\n')
    S.append(f'- {len(files)} source files with functions; {len(defs)} functions compiled '
             f'({sum(1 for i in defs if F[i]["kind"] == "generated")} of them written by the compiler: implicit '
             f'constructors, destructors and the like); {sum(1 for i in F if F[i]["definition"] == "0")} virtual methods '
             'that are called but have no function in the DLL (pure virtual, or provided by the exe).')
    S.append(f'- Calls between functions of the source: {sum(1 for c in calls if c["kind"] == "call")} direct, '
             f'{sum(1 for c in calls if c["kind"] == "virtual")} virtual, and {sum(1 for c in calls if c["kind"] == "ref")} '
             'places where a function\'s address is taken.')
    S.append(f'- {len(classes)} classes and structs, {len(bases)} base-class links, {len(over)} overrides.')
    S.append(f'- {len(pydefs)} functions exposed to Python; {len(pycalls)} places where the DLL calls Python; '
             f'{len({e["event"] for e in evh})} events posted to Python.\n')
    unres = read(os.path.join(M, 'unresolved.tsv'))
    S.append('## Completeness\n')
    S.append(f'- {len(units)} units compiled, {sum(1 for u in units if u["errors"] != "0")} with errors, '
             f'{sum(int(u["warnings"]) for u in units)} compiler warnings (`map/units.tsv`).')
    why = collections.Counter(u['reason'] for u in unres)
    S.append(f'- {len(unres)} calls in the compiled code are not resolved to one function (`map/unresolved.tsv`): '
             + '; '.join(f'{n} {r}' for r, n in sorted(why.items())) + '. Ambiguous virtual calls are in `calls.tsv` '
             'once for each candidate.')
    S.append(f'- Against universal-ctags on the same files (`map/completeness.tsv`): {len(ct_only)} definitions in the '
             'source that no unit compiles (inline functions nothing uses, templates never instantiated, code the '
             f'release build leaves out by #ifdef, or names written differently), {len(compiled_only)} compiled that ctags '
             'does not see (functions written by macros or several on one line).\n')
    S.append('## Groups of files\n')
    S.append('Grouped by file name only (rules in `tool/render.py`), not by what the code does.\n')
    S.append('| group | files | functions defined | calls inside the group | calls to other groups | calls from other groups |')
    S.append('|---|---|---|---|---|---|')
    for g in gnames:
        fs = [f for f in files if group(f) == g]
        S.append(f'| {g} | {len(fs)} | {sum(1 for i in defs if G[i] == g)} | {gl[(g, g)]} | '
                 f'{sum(v for (a, b), v in gl.items() if a == g and b != g)} | {sum(v for (a, b), v in gl.items() if b == g and a != g)} |')
    S.append('\nCalls from group (row) to group (column):\n')
    S.append('| from \\ to | ' + ' | '.join(gnames) + ' |')
    S.append('|---' * (len(gnames) + 1) + '|')
    for a in gnames: S.append(f'| {a} | ' + ' | '.join(str(gl[(a, b)]) for b in gnames) + ' |')
    S.append('\n## Files\n')
    S.append('Calls are counted between files (calls inside a file are left out). "Calls most" and "called most by" '
             'list up to three files with the count.\n')
    S.append('| file | group | functions defined | calls to other files | called from other files | calls most | called most by |')
    S.append('|---|---|---|---|---|---|---|')
    for f in sorted(files, key=lambda f: (gnames.index(group(f)), f)):
        out = sorted(((v, b) for (a, b), v in fl.items() if a == f), reverse=True)
        inn = sorted(((v, a) for (a, b), v in fl.items() if b == f), reverse=True)
        S.append(f'| [{f}](files/{f}.md) | {group(f)} | {sum(1 for i in defs if F[i]["file"] == f)} | {sum(v for v, _ in out)} | '
                 f'{sum(v for v, _ in inn)} | ' + ', '.join(f'{b} {v}' for v, b in out[:3]) + ' | '
                 + ', '.join(f'{a} {v}' for v, a in inn[:3]) + ' |')
    S.append('\n## Class hierarchy\n')
    S.append('Classes of the source with their base classes (bases outside the source in parentheses).\n')
    kids = collections.defaultdict(list); has_base = set(); known = {c['class'] for c in classes}
    for b in bases: kids[b['base']].append(b['class']); has_base.add(b['class'])
    nmeth = collections.Counter(F[i]['scope'] for i in defs)
    def tree(c, d, seen):
        S.append('  ' * d + f'- {c}' + (f' ({nmeth[c]} methods)' if nmeth[c] else '') + ('' if c in known else ' (outside the source)'))
        for k in sorted(kids.get(c, [])):
            if k not in seen: tree(k, d + 1, seen | {k})
    for c in sorted({b['base'] for b in bases} - has_base): tree(c, 0, {c})
    S.append('\n## Turn and update backbone\n')
    S.append('Every function named ' + ', '.join(f'`{n}`' for n in sorted(TURN)) + ', with the functions it calls, '
             f'two levels deep. Only callees that themselves call at least {SUBST} different functions of the source are '
             'shown, so getters and small helpers drop out; the full lists are on the file pages. '
             'A virtual call is followed into the methods that override it, marked ⇢.\n')
    def nonleaf(i): return len(set(callees.get(i, ()))) >= SUBST
    def expand(i):
        out = []
        for b in dict.fromkeys(callees.get(i, [])):
            if nonleaf(b): out.append((b, ''))
            for o in may_run(i, b):
                if nonleaf(o): out.append((o, '⇢ '))
        return list(dict.fromkeys(out))
    roots = sorted((i for i in defs if F[i]['name'] in TURN and F[i]['scope'] and nonleaf(i)), key=lambda i: (F[i]['scope'], F[i]['name']))
    for r in roots:
        S.append(f'- **{short(r)}** ({F[r]["file"]}:{F[r]["line"]})')
        for b, mark in expand(r):
            sub = [mk + short(x) for x, mk in expand(b)]
            S.append(f'  - {mark}{short(b)}' + (': ' + ', '.join(sub) if sub else ''))
    open(os.path.join(root, 'skeleton.md'), 'w', encoding='utf-8').write('\n'.join(S) + '\n')

    # entry points
    E = ['# Entry points of the DLL\n', 'How control reaches the source from outside, from `map/`.\n']
    exp = [i for i in F if F[i]['exported'] == '1']
    E.append(f'## Offered to the game exe: exported functions ({len(exp)})\n')
    E.append('Functions declared `DllExport` (directly, or as members of a class declared `DllExport`): the DLL '
             'offers them to the exe. Which of them the exe actually calls cannot be seen from the source.\n')
    by = collections.defaultdict(list)
    for i in exp: by[F[i]['scope'] or '(global)'].append(i)
    for s in sorted(by):
        E.append(f'- **{s}** ({len(by[s])}): ' + ', '.join(sorted({F[i]["name"] for i in by[s]})))
    impl = [i for i in F if from_exe(i)]
    E.append(f'\n## Implemented by the game exe ({len(impl)})\n')
    E.append('Pure virtual methods of classes the source never derives from and never implements: the DLL calls '
             'them through the interface pointers the exe hands it (`gDLL` and the like), so the exe provides them.\n')
    by = collections.defaultdict(list)
    for i in impl: by[F[i]['scope']].append(i)
    for s in sorted(by):
        n = collections.Counter(len(callers.get(i, ())) for i in by[s])
        used = sum(1 for i in by[s] if callers.get(i))
        E.append(f'- **{s}** ({len(by[s])}, {used} called from the source)')
    E.append(f'\n## Called from Python: functions exposed by boost::python ({len(pydefs)})\n')
    E.append('Per C++ class: how many functions are exposed. The full list with Python names is `map/python_defs.tsv`.\n')
    byc = collections.Counter(p['cpp_scope'] or '(global)' for p in pydefs)
    E.append('| C++ class | exposed |'); E.append('|---|---|')
    for s, n in sorted(byc.items()): E.append(f'| {s} | {n} |')
    E.append(f'\n## The DLL calls Python ({len(pycalls)} sites)\n')
    E.append('`callFunction(module, "function")` sites. A module shown as ? is chosen at run time (the map script).\n')
    E.append('| Python function | defined in | called from |'); E.append('|---|---|---|')
    byf = collections.defaultdict(set); where = {}
    for p in pycalls:
        k = f"{p['module']}.{p['python_function']}"
        if p['caller']: byf[k].add(short(int(p['caller'])))
        where[k] = f"{p['python_file']}:{p['python_line']}" if p['python_file'] else 'not found'
    for k in sorted(byf): E.append(f'| {k} | {where[k]} | ' + ', '.join(sorted(byf[k])) + ' |')
    E.append(f'\n## Events posted to Python ({len({e["event"] for e in evh})})\n')
    E.append('Each `CvDllPythonEvents` report function posts one event; the handlers are every registration found: '
             'the event manager\'s map, `addEventHandler` calls, and the BUG configuration XML.\n')
    E.append('| event | posted by | handlers |'); E.append('|---|---|---|')
    byev = collections.defaultdict(list); poster = {}
    for e in evh:
        poster[e['event']] = short(int(e['function'])) if e['function'] else ''
        if e['handler']: byev[e['event']].append(f"{e['handler']} ({e['file']}:{e['line']})")
    for ev in sorted(poster): E.append(f'| {ev} | {poster[ev]} | ' + ('; '.join(byev[ev]) or 'none registered') + ' |')
    open(os.path.join(root, 'entry_points.md'), 'w', encoding='utf-8').write('\n'.join(E) + '\n')

    # python side
    P = ['# The Python side\n',
         'The mod\'s Python and the base game\'s Python it falls back to (paths starting with base/), scanned by name '
         '(`tool/extract_py.py`). Links from Python into the DLL are name matches: a method name exposed by several '
         'C++ classes gives several candidates.\n']
    mods = collections.Counter(p['module'] for p in pyf)
    tocpp = collections.Counter(r['module'] for r in p2c)
    single = collections.Counter(r['module'] for r in p2c if r['candidates'] == '1')
    P.append(f'{len(mods)} modules, {len(pyf)} functions and classes, {len(p2c)} call sites of names the DLL exposes '
             f'({sum(single.values())} with one candidate).\n')
    P.append('| module | functions and classes | calls into the DLL | of them with one candidate |'); P.append('|---|---|---|---|')
    for m in sorted(mods): P.append(f'| {m} | {mods[m]} | {tocpp[m]} | {single[m]} |')
    open(os.path.join(root, 'python.md'), 'w', encoding='utf-8').write('\n'.join(P) + '\n')

    # one outline page per source file
    os.makedirs(os.path.join(root, 'files'), exist_ok=True)
    for f in os.listdir(os.path.join(root, 'files')):
        if f.endswith('.md'): os.remove(os.path.join(root, 'files', f))
    for f in files:
        L = [f'# {f}\n', f'Group: {group(f)}. Functions in line order: what each calls (in order of first call), '
             'what it takes the address of, and who calls it. Callees in another file carry the file. '
             'A virtual callee lists its overrides after ⇢.\n']
        for i in sorted((i for i in F if F[i]['file'] == f), key=lambda i: (int(F[i]['line'] or 10 ** 9), i)):
            r = F[i]; flags = [k for k in ('exported', 'virtual', 'static') if r[k] == '1']
            if r['pure'] == '1': flags.append('pure virtual' + (', provided by the exe' if from_exe(i) else ''))
            elif r['definition'] == '0': flags.append('declared, not defined in the source')
            if pyname.get(i): flags.append('Python: ' + ', '.join(sorted(set(pyname[i]))))
            if overrides.get(i): flags.append('overrides ' + ', '.join(short(b) for b in sorted(overrides[i])))
            if r['kind'] == 'generated': flags.append('written by the compiler')
            L.append(f"- **{r['line'] or '·'}** `{r['scope'] + '::' if r['scope'] else ''}{r['sig']}`" + (f" ({'; '.join(flags)})" if flags else ''))
            def name(b, ref=False):
                s = short(b) + ('' if F[b]['file'] == f else f" [{F[b]['file']}]")
                run = sorted(overriders.get(b, ())) if ref else may_run(i, b)
                if run: s += ' ⇢ ' + ', '.join(short(o) for o in run)
                return s
            cs = list(dict.fromkeys(callees.get(i, [])))
            if cs: L.append('  - calls: ' + ', '.join(name(b) for b in cs))
            rs = list(dict.fromkeys(refs.get(i, [])))
            if rs: L.append('  - takes the address of: ' + ', '.join(name(b, True) for b in rs))
            cl = sorted(callers.get(i, ()), key=short)
            if cl: L.append(f'  - called by ({len(cl)}): ' + ', '.join(short(a) for a in cl[:12]) + (' …' if len(cl) > 12 else ''))
        open(os.path.join(root, 'files', f + '.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'{len(files)} file pages; {len(ct_only)} ctags-only and {len(compiled_only)} compiled-only definitions', file=sys.stderr)


if __name__ == '__main__':
    main()
