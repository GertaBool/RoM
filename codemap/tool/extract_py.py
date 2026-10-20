#!/usr/bin/env python3
"""The Python side of the map: which modules the game loads, and their links with the DLL.

usage: extract_py.py list <out file> <mod Assets/Python dir> [<base game Python dir> ...]
       extract_py.py link <map dir> <module list from list> <mod Assets/Config dir>

list: the modules the game can import, one line each (name as shown in the map, path for Wine). Modules
  are imported by name from the mod's folder first, then the base game's, so a base module whose name the
  mod also has is left out (shadowed); a file whose name is not a Python module name cannot be imported
  and is left out; a " (1)" in a base path (a download artefact) is dropped from the name.
  py24_scan.py, run by the game's own Python 2.4, then parses them: py_functions.tsv, py_calls_raw.tsv,
  py_handlers.tsv, py_errors.tsv.
link: from those and the DLL tables (python_defs.tsv, python_calls.tsv, events.tsv):
  py_calls.tsv        call sites, with the target when the name is defined once in the same module
  py_to_cpp.tsv       attribute calls whose name the DLL exposes, with the candidate C++ functions (several
                      when classes share a method name; listed up to five). Python resolves names when it
                      runs, so these are name matches, not proven targets.
  cpp_to_py.tsv       DLL callFunction(module, "name") sites, with the Python function they land in
  event_handlers.tsv  events posted by CvDllPythonEvents and every handler registered for them: the event
                      manager's EventHandlerMap, addEventHandler("event", f) calls, and <event type=...
                      module=... function=.../> entries of the BUG configuration XML
"""
import csv, os, re, sys

MODULE = re.compile(r'^[A-Za-z_]\w*$')


def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def write(path, header, rows):
    with open(path, 'w', encoding='utf-8') as o:
        o.write('\t'.join(header) + '\n')
        for r in rows: o.write('\t'.join(str(x) for x in r) + '\n')


def modules(roots):
    rows, taken = [], set()
    for k, root in enumerate(roots):
        files = []
        for dp, dn, fn in os.walk(root):
            for f in fn:
                if f.endswith('.py'):
                    p = os.path.join(dp, f)
                    files.append((os.path.relpath(p, root).replace(' (1)', ''), p))
        files.sort(key=lambda r: (r[0], ' (1)' in r[1]))   # the unsuffixed copy first
        mine = set()
        for rel, p in files:
            m = os.path.basename(rel)[:-3]
            if not MODULE.match(m) or m in taken or m in mine: continue
            mine.add(m); rows.append((('base/' if k else '') + rel, p))
        taken |= mine
    return rows


def link(mapdir, listed, config):
    defs = read(os.path.join(mapdir, 'py_functions.tsv'))
    calls = read(os.path.join(mapdir, 'py_calls_raw.tsv'))
    by_mod = {}
    for d in defs: by_mod.setdefault((d['module'], d['name'].split('.')[-1]), []).append(d['name'])
    write(os.path.join(mapdir, 'py_calls.tsv'), ['module', 'caller', 'name', 'attribute', 'line', 'same_module_target'],
          [(c['module'], c['caller'], c['name'], c['attribute'], c['line'],
            by_mod[(c['module'], c['name'])][0] if len(by_mod.get((c['module'], c['name']), [])) == 1 else '') for c in calls])
    exposed = {}
    for r in read(os.path.join(mapdir, 'python_defs.tsv')): exposed.setdefault(r['python_name'], set()).add(r['function'])
    rows = []
    for c in calls:
        if c['attribute'] == '1' and c['name'] in exposed:
            ids = sorted(exposed[c['name']], key=int)
            rows.append((c['module'], c['caller'], c['name'], c['line'], len(ids), ','.join(ids) if len(ids) <= 5 else ''))
    write(os.path.join(mapdir, 'py_to_cpp.tsv'), ['module', 'caller', 'name', 'line', 'candidates', 'functions'], rows)
    mods = {}
    for d in defs: mods.setdefault(os.path.splitext(os.path.basename(d['module']))[0], []).append(d)
    rows = []
    for r in read(os.path.join(mapdir, 'python_calls.tsv')):
        hit = next((d for d in mods.get(r['module'], []) if d['name'] == r['python_function']), None)
        rows.append((r['caller'], r['module'], r['python_function'], r['file'], r['line'],
                     hit['module'] if hit else '', hit['line'] if hit else ''))
    write(os.path.join(mapdir, 'cpp_to_py.tsv'),
          ['caller', 'module', 'python_function', 'file', 'line', 'python_file', 'python_line'], rows)
    handlers = {}
    em = next((d['module'] for d in defs if d['name'] == 'CvEventManager' and d['kind'] == 'class'), None)
    for h in read(os.path.join(mapdir, 'py_handlers.tsv')):
        handlers.setdefault(h['event'], []).append(('addEventHandler', h['caller'] + ': ' + h['handler'], h['module'], h['line']))
    if em:   # the event manager's map, read from the module the game loads
        path = next((p for m, p in listed if m == em), None)
        if path:
            for ln, line in enumerate(open(path, encoding='latin-1'), 1):
                for k, h in re.findall(r"""['"](\w+)['"]\s*:\s*self\.(\w+)""", line):
                    handlers.setdefault(k, []).append(('EventHandlerMap', 'CvEventManager.' + h, em, ln))
    for dp, dn, fn in os.walk(config):
        for f in sorted(fn):
            if not f.endswith('.xml'): continue
            p = os.path.join(dp, f)
            for ln, line in enumerate(open(p, encoding='latin-1'), 1):
                for ev in re.finditer(r'<event\s+([^>]*)>', line):
                    at = dict(re.findall(r'(\w+)="([^"]*)"', ev.group(1)))
                    if 'type' in at:
                        handlers.setdefault(at['type'], []).append(
                            ('BUG config', at.get('module', '?') + '.' + at.get('function', '?'), 'Config/' + os.path.relpath(p, config), ln))
    rows = []
    for r in read(os.path.join(mapdir, 'events.tsv')):
        for h in handlers.get(r['event'], [('', '', '', '')]): rows.append((r['function'], r['event']) + h)
    write(os.path.join(mapdir, 'event_handlers.tsv'), ['function', 'event', 'source', 'handler', 'file', 'line'], rows)
    print(f'{len(defs)} Python functions and classes, {len(calls)} call sites, '
          f'{len(read(os.path.join(mapdir, "py_errors.tsv")))} modules Python 2.4 could not parse', file=sys.stderr)


if __name__ == '__main__':
    if sys.argv[1] == 'list':
        rows = modules(sys.argv[3:])
        with open(sys.argv[2], 'w', encoding='utf-8') as o:
            for name, p in rows: o.write(f"{name}\t{'Z:' + os.path.abspath(p).replace('/', chr(92))}\n")
        print(f'{len(rows)} modules', file=sys.stderr)
    elif sys.argv[1] == 'link':
        listed = [(l.split('\t')[0], l.rstrip('\n').split('\t')[1][2:].replace(chr(92), '/'))
                  for l in open(sys.argv[3], encoding='utf-8') if l.strip()]
        link(sys.argv[2], listed, sys.argv[4])
    else:
        sys.exit(__doc__)
