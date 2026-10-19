#!/usr/bin/env python3
"""Map the mod's Python (Python 2.4) and its links with the DLL, by name.

usage: extract_py.py <map dir> <mod Assets/Python dir> [<base game Python dir> ...] [--config <mod Assets/Config dir>]

The game imports Python modules by name from the mod's folder first, then the base game's. A base module
whose name the mod also defines is left out (shadowed). A " (1)" in a base path (a download artefact) is
dropped from the name.

The Python files are scanned, not parsed (Python 2 syntax): strings and comments are blanked, `def` and
`class` lines give the functions and their nesting by indentation, and `name(` gives call sites. A call
resolves only by name, so the links below are name matches, not proven targets:
  py_functions.tsv  every def and class: module, qualified name, line (module paths of the base game
                    start with base/)
  py_calls.tsv      call sites: calling function, called name, whether written as attribute (x.name()),
                    and the target when the name is defined once in the same module
  py_to_cpp.tsv     attribute calls whose name is exposed by the DLL (python_defs.tsv), with the candidate
                    C++ functions (several when classes share a method name; listed up to five)
  cpp_to_py.tsv     DLL callFunction(module, "name") sites resolved to the Python def they call
  event_handlers.tsv  event names posted by CvDllPythonEvents and every handler registered for them: the
                    event manager's EventHandlerMap, addEventHandler("event", f) calls, and <event type="event"
                    module="m" function="f"/> entries of the BUG configuration XML
Reads python_defs.tsv, python_calls.tsv and events.tsv written by extract_cpp.py in the same map dir.
"""
import csv, os, re, sys

KEYWORDS = set('and as assert break class continue def del elif else except exec finally for from global if '
               'import in is lambda not or pass print raise return try while with yield'.split())


def blank(text):
    """Strings and comments replaced by spaces, newlines kept, so line numbers and indentation survive."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '#':
            j = text.find('\n', i); j = n if j < 0 else j
            out.append(' ' * (j - i)); i = j
        elif c in '"\'':
            q = text[i:i + 3] if text[i:i + 3] in ('"""', "'''") else c
            j = i + len(q)
            while j < n:
                if text[j] == '\\': j += 2; continue
                if text.startswith(q, j): j += len(q); break
                if len(q) == 1 and text[j] == '\n': break
                j += 1
            out.append(q + ''.join('\n' if ch == '\n' else ' ' for ch in text[i + len(q):j - len(q)]) + q
                       if j - i >= 2 * len(q) else text[i:j]); i = j
        else:
            out.append(c); i += 1
    return ''.join(out)


def scan(path, rel):
    text = blank(open(path, encoding='latin-1').read().replace('\r\n', '\n').replace('\r', '\n'))
    defs, calls, stack = [], [], []           # stack: (indent, qualname)
    depth = 0                                  # bracket depth: continuation lines do not open blocks
    for ln, line in enumerate(text.split('\n'), 1):
        s = line.expandtabs(8)
        body = s.strip()
        if depth == 0 and body:
            ind = len(s) - len(s.lstrip())
            while stack and stack[-1][0] >= ind: stack.pop()
            m = re.match(r'(def|class)\s+([A-Za-z_]\w*)', body)
            if m:
                q = (stack[-1][1] + '.' if stack else '') + m.group(2)
                defs.append((rel, q, m.group(1), ln))
                stack.append((ind, q))
        caller = stack[-1][1] if stack else '<module>'
        for m in re.finditer(r'(\.)?\s*\b([A-Za-z_]\w*)\s*\(', line):
            name = m.group(2)
            if name in KEYWORDS: continue
            if re.match(r'\s*(def|class)\s+' + name + r'\b', line): continue
            calls.append((rel, caller, name, int(bool(m.group(1))), ln))
        depth = max(0, depth + sum(line.count(c) for c in '([{') - sum(line.count(c) for c in ')]}'))
    return defs, calls


def read(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def write(path, header, rows):
    with open(path, 'w', encoding='utf-8') as o:
        o.write('\t'.join(header) + '\n')
        for r in rows: o.write('\t'.join(str(x) for x in r) + '\n')


def main():
    args = sys.argv[1:]
    config = args[args.index('--config') + 1] if '--config' in args else None
    if config: i = args.index('--config'); del args[i:i + 2]
    mapdir, roots = args[0], args[1:]
    srcline = {}
    defs, calls, taken = [], [], set()
    for k, root in enumerate(roots):
        files = []
        for dp, dn, fn in os.walk(root):
            dn.sort()
            for f in sorted(fn):
                if f.endswith('.py'):
                    p = os.path.join(dp, f)
                    rel = os.path.relpath(p, root).replace(' (1)', '')
                    files.append((rel, p))
        files.sort(key=lambda r: (r[0], ' (1)' in r[1]))   # the unsuffixed copy first
        mine = set()
        for rel, p in files:
            mod = os.path.basename(rel)[:-3]
            if mod in taken or mod in mine: continue
            mine.add(mod)
            name = ('base/' if k else '') + rel
            d, c = scan(p, name)
            for i, s in enumerate(open(p, encoding='latin-1').read().replace('\r\n', '\n').split('\n'), 1):
                if 'addEventHandler' in s: srcline[(name, i)] = s
            defs += d; calls += c
        taken |= mine
    write(os.path.join(mapdir, 'py_functions.tsv'), ['module', 'name', 'kind', 'line'], defs)
    by_mod = {}
    for m, q, k, l in defs: by_mod.setdefault((m, q.split('.')[-1]), []).append(q)
    write(os.path.join(mapdir, 'py_calls.tsv'), ['module', 'caller', 'name', 'attribute', 'line', 'same_module_target'],
          [(m, c, n, a, l, by_mod[(m, n)][0] if len(by_mod.get((m, n), [])) == 1 else '') for m, c, n, a, l in calls])
    exposed = {}
    for r in read(os.path.join(mapdir, 'python_defs.tsv')):
        exposed.setdefault(r['python_name'], set()).add(r['function'])
    rows = []
    for m, c, n, a, l in calls:
        if a and n in exposed:
            ids = sorted(exposed[n], key=int)
            rows.append((m, c, n, l, len(ids), ','.join(ids) if len(ids) <= 5 else ''))   # many: the name alone decides nothing
    write(os.path.join(mapdir, 'py_to_cpp.tsv'), ['module', 'caller', 'name', 'line', 'candidates', 'functions'], rows)
    mods = {}
    for m, q, k, l in defs:
        mods.setdefault(os.path.splitext(os.path.basename(m))[0], []).append((m, q, l))
    rows = []
    for r in read(os.path.join(mapdir, 'python_calls.tsv')):
        hits = [(m, q, l) for m, q, l in mods.get(r['module'], []) if q == r['python_function']]
        rows.append((r['caller'], r['module'], r['python_function'], r['file'], r['line'],
                     hits[0][0] if hits else '', hits[0][2] if hits else ''))
    write(os.path.join(mapdir, 'cpp_to_py.tsv'),
          ['caller', 'module', 'python_function', 'file', 'line', 'python_file', 'python_line'], rows)
    handlers = {}   # event -> [(source, handler, file, line)]
    em = [m for m, q, k, l in defs if q == 'CvEventManager' and k == 'class']
    for m in em[:1]:   # the event manager the game loads (mod first, then base): its EventHandlerMap
        root = roots[1] if m.startswith('base/') else roots[0]
        p = next(os.path.join(dp, f) for dp, dn, fn in os.walk(root) for f in fn
                 if os.path.relpath(os.path.join(dp, f), root).replace(' (1)', '') == m.split('/', 1)[-1] or
                 os.path.relpath(os.path.join(dp, f), root).replace(' (1)', '') == m)
        for ln, line in enumerate(open(p, encoding='latin-1'), 1):
            for k, h in re.findall(r"""['"](\w+)['"]\s*:\s*self\.(\w+)""", line):
                handlers.setdefault(k, []).append(('EventHandlerMap', 'CvEventManager.' + h, m, ln))
    for m, c, n, a, l in calls:   # addEventHandler("event", handler) anywhere in the Python
        if n == 'addEventHandler':
            src = srcline.get((m, l), '')
            r = re.search(r"""addEventHandler\s*\(\s*['"](\w+)['"]\s*,\s*([\w.]+)""", src)
            if r: handlers.setdefault(r.group(1), []).append(('addEventHandler', c + ': ' + r.group(2), m, l))
    if config:
        for dp, dn, fn in os.walk(config):
            for f in sorted(fn):
                if not f.endswith('.xml'): continue
                p = os.path.join(dp, f)
                for ln, line in enumerate(open(p, encoding='latin-1'), 1):
                    for ev in re.finditer(r'<event\s+([^>]*)>', line):
                        at = dict(re.findall(r'(\w+)="([^"]*)"', ev.group(1)))
                        if 'type' in at:
                            handlers.setdefault(at['type'], []).append(
                                ('BUG config', at.get('module', '?') + '.' + at.get('function', '?'),
                                 'Config/' + os.path.relpath(p, config), ln))
    rows = []
    for r in read(os.path.join(mapdir, 'events.tsv')):
        for h in handlers.get(r['event'], [('', '', '', '')]):
            rows.append((r['function'], r['event']) + h)
    write(os.path.join(mapdir, 'event_handlers.tsv'), ['function', 'event', 'source', 'handler', 'file', 'line'], rows)
    print(f'{len(defs)} Python defs and classes, {len(calls)} call sites', file=sys.stderr)


if __name__ == '__main__':
    main()
