#!/usr/bin/env python3
"""The Python side of the map: which modules the game loads, and their links with the DLL.

usage: extract_py.py list <out file> <mod Assets/Python dir> [<base game Python dir> ...]
       extract_py.py link <map dir> <module list from list> <mod Assets/Config dir>
       extract_py.py layers <module list> <out tsv> <mod Python dir> <base Python dir>...   py_modules.tsv

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
  py_event_registrations.tsv  every such registration, for any event name (generic events are named by
                      the DLL at the call)
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
    write(os.path.join(mapdir, 'py_calls.tsv'), ['module', 'caller', 'name', 'attribute', 'line', 'same_module_target', 'recv', 'args'],
          [(c['module'], c['caller'], c['name'], c['attribute'], c['line'],
            by_mod[(c['module'], c['name'])][0] if len(by_mod.get((c['module'], c['name']), [])) == 1 else '',
            c.get('recv', ''), c.get('args', '')) for c in calls])
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
    # Known event names (from DLL events.tsv and EventHandlerMap) for matching BUG <events> classes
    known_events = {r['event'].lower(): r['event'] for r in read(os.path.join(mapdir, 'events.tsv'))}
    known_events.update({ev.lower(): ev for ev in handlers})
    # Known CvGameInterface callbacks called by the DLL (for matching BUG <gameutils> classes/handlers/listeners)
    gi_callbacks = sorted({r['python_function'] for r in read(os.path.join(mapdir, 'python_calls.tsv'))
                           if r['module'] == 'CvGameInterface'})
    gi_cb_set = set(gi_callbacks)
    gameutils_rows = []
    # Base CvGameUtils class methods
    for d in mods.get('CvGameUtils', []):
        if d['kind'] == 'def' and '.' in d['name']:
            mname = d['name'].split('.')[-1]
            if mname in gi_cb_set:
                gameutils_rows.append((mname, d['module'], d['name'], 'base', '', 0))
    bug_opts = []
    if config and os.path.isdir(config):
        for dp, dn, fn in os.walk(config):
            for f in sorted(fn):
                if not f.endswith('.xml'): continue
                p = os.path.join(dp, f)
                rel_cfg = 'Config/' + os.path.relpath(p, config)
                text = open(p, encoding='latin-1').read()
                mod_m = re.search(r'<mod\s+([^>]*)>', text, re.S)
                mod_at = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', mod_m.group(1))) if mod_m else {}
                default_mod = mod_at.get('module', '')
                cur_opt_mod = mod_at.get('id', '')
                # BUG options blocks (<options id="ModId"> ... <option id="..." get="..." set="..."/>)
                for m_opt in re.finditer(r'<(options|option)\s+([^>]*)>', text, re.S):
                    tag, body = m_opt.group(1), m_opt.group(2)
                    at = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', body))
                    ln = text.count('\n', 0, m_opt.start()) + 1
                    if tag == 'options':
                        cur_opt_mod = at.get('id', cur_opt_mod)
                    elif tag == 'option' and cur_opt_mod and 'id' in at:
                        oid = at['id']
                        getter = at.get('get', ('is' if at.get('type') == 'boolean' else 'get') + oid)
                        setter = at.get('set', 'set' + oid)
                        bug_opts.append((cur_opt_mod, oid, getter, setter, rel_cfg, ln))
                for m_ev in re.finditer(r'<(event|events|gameutils)\s+([^>]*)>', text, re.S):
                    tag, body = m_ev.group(1), m_ev.group(2)
                    at = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', body))
                    ln = text.count('\n', 0, m_ev.start()) + 1
                    if tag == 'event' and 'type' in at:
                        mname = at.get('module') or default_mod or '?'
                        handlers.setdefault(at['type'], []).append(
                            ('BUG config', mname + '.' + at.get('function', '?'), rel_cfg, ln))
                    elif tag == 'events':
                        mname = at.get('module') or default_mod
                        cname = at.get('class') or mname
                        if mname and mname in mods:
                            existing = {(h[1], h[2]) for hs in handlers.values() for h in hs}
                            for d in mods[mname]:
                                if d['kind'] != 'def': continue
                                short = d['name'].split('.')[-1]
                                if not short.startswith('on') or len(short) <= 2: continue
                                if cname and '.' in d['name'] and d['name'].split('.')[0] != cname: continue
                                ev_key = short[2:].lower()
                                ev_name = known_events.get(ev_key)
                                if ev_name and not any(d['module'] == ex[1] and short in ex[0] for ex in existing):
                                    handlers.setdefault(ev_name, []).append(
                                        ('BUG config', mname + '.' + d['name'], rel_cfg, ln))
                    elif tag == 'gameutils':
                        mname = at.get('module') or default_mod
                        cname = at.get('class', '')
                        hname = at.get('handler', '')
                        lname = at.get('listener', '')
                        if not mname or mname not in mods: continue
                        if hname:
                            hit = next((d for d in mods[mname] if d['kind'] == 'def' and d['name'].split('.')[-1] == hname), None)
                            cb = at.get('callback') or hname
                            if hit:
                                gameutils_rows.append((cb, hit['module'], hit['name'], 'handler', rel_cfg, ln))
                        if lname:
                            hit = next((d for d in mods[mname] if d['kind'] == 'def' and d['name'].split('.')[-1] == lname), None)
                            cb = at.get('callback') or (lname[:-8] if lname.endswith('Listener') else lname)
                            if hit:
                                gameutils_rows.append((cb, hit['module'], hit['name'], 'listener', rel_cfg, ln))
                        if cname or (not hname and not lname):
                            for d in mods[mname]:
                                if d['kind'] != 'def': continue
                                if cname and not d['name'].startswith(cname + '.'): continue
                                short = d['name'].split('.')[-1]
                                if short in gi_cb_set:
                                    gameutils_rows.append((short, d['module'], d['name'], 'class', rel_cfg, ln))
    write(os.path.join(mapdir, 'py_gameutils.tsv'), ['callback', 'module', 'handler', 'kind', 'config_file', 'line'],
          sorted(set(gameutils_rows)))
    write(os.path.join(mapdir, 'py_bug_options.tsv'), ['mod_id', 'option_id', 'getter', 'setter', 'config_file', 'line'],
          sorted(set(bug_opts)))
    write(os.path.join(mapdir, 'py_event_registrations.tsv'), ['event', 'source', 'handler', 'file', 'line'],
          sorted(((ev,) + h for ev, hs in handlers.items() for h in hs), key=lambda r: r[:4] + (int(r[4]),)))
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
    elif sys.argv[1] == 'layers':   # layers <module list> <out tsv> <mod dir> <base dir>...: each module's layer
        roots = [os.path.abspath(r) for r in sys.argv[4:]]
        names = ['mod', 'bts', 'civ4'] + ['base%d' % k for k in range(3, len(roots))]
        with open(sys.argv[3], 'w', encoding='utf-8') as o:
            o.write('module\tlayer\tfile\n')
            for l in open(sys.argv[2], encoding='utf-8'):
                if not l.strip(): continue
                m, p = l.rstrip('\n').split('\t')
                p = p[2:].replace(chr(92), '/')
                k = next((i for i, r in enumerate(roots) if p.startswith(r + '/')), 0)
                o.write('%s\t%s\t%s\n' % (m, names[k], os.path.relpath(p, roots[k])))
    elif sys.argv[1] == 'link':
        listed = [(l.split('\t')[0], l.rstrip('\n').split('\t')[1][2:].replace(chr(92), '/'))
                  for l in open(sys.argv[3], encoding='utf-8') if l.strip()]
        link(sys.argv[2], listed, sys.argv[4])
    else:
        sys.exit(__doc__)
