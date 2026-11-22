#!/usr/bin/env python3
"""The Python API reference as a table, and which Python calls go to the DLL, which to the game exe.

usage: pyapi.py <AllClasses.html> <CvGameCoreDLL dir>   writes map/python_classes.tsv, map/py_api.tsv,
                                                         map/py_targets.tsv, map/py_api_check.tsv

AllClasses.html is the class reference of CvPythonExtensions for Beyond the Sword
(https://civ4bug.sourceforge.net/PythonAPI/AllClasses.html; BTS 3.17, written by a script from the game's own
docstrings, maintained by the BUG project). The game's Python reaches C++ only through these classes. Some
are bound by the DLL (map/python_defs.tsv: CyCity, CyPlayer, the Cv*Info classes ...); the rest are bound by
the exe (CyInterface, CyEngine, CyAudioGame, CyCamera ...), which the code map cannot see.

  python_bindings.tsv every .def("name", &f) in the DLL source, with the class it is bound on, its docstring and
                    the return type the docstring starts with ("CyCity (int iID)" -> CyCity)
  python_classes.tsv  every class the DLL registers for Python (python::class_<C, bases<B>>("Name")), with its
                    C++ class and bases, read from the DLL source
  py_api.tsv        class, method, return type, parameters, description, and where the class is bound:
                    dll (the DLL registers it) or exe (it does not)
  py_targets.tsv    every attribute call in the Python (map/py_calls.tsv, attribute = 1), with where its name
                    lands: dll (a name the DLL binds), exe (a method of an exe class in the reference), both,
                    or python (neither: a Python function, a builtin, a method of a Python object)
  py_api_check.tsv  for classes the DLL binds: methods in the reference the DLL does not bind (missing), and
                    methods the DLL binds that the reference does not list (added). The reference is 3.17
                    and unmodded, so "missing" is either a 3.19 change or a change of the mod; Python that calls a
                    missing name fails when it runs.
Names are matched as Python matches them when it runs: by method name. A call x.f() is "dll" when any DLL
class binds f; which class x is, Python decides at run time.
"""
import collections, csv, html, os, re, sys

M = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'map')


def read(n):
    with open(os.path.join(M, n), encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def write(n, header, rows):
    with open(os.path.join(M, n), 'w', encoding='utf-8') as o:
        o.write('\t'.join(header) + '\n')
        for r in rows:
            o.write('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in r) + '\n')


def text(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def parse(path):
    d = open(path, encoding='latin-1').read()
    rows = []
    # each method: <a name="Class.method"></a><li><span>RET name (params)</span><br>\nC++ signature - description<br>
    for m in re.finditer(r'<a name="([A-Za-z_]\w*)\.([A-Za-z_]\w*)"></a><li><span>(.*?)</span><br>\s*(.*?)<br>', d, re.S):
        cls, meth, head, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        h = text(head)
        ret, _, rest = h.partition(' ')
        params = rest[rest.find('('):] if '(' in rest else ''
        t = text(tail)
        desc = t.split(' - ', 1)[1] if ' - ' in t else ''
        rows.append([cls, meth, ret, params, desc])
    return rows


REG = re.compile(r'class_<\s*([\w:]+)\s*(?:,\s*(?:python::)?bases<\s*([\w:,\s]+?)\s*>\s*)?(?:,[^>]*)?>\s*\w*\s*\(\s*"(\w+)"')


def registrations(src):
    rows = []
    for f in sorted(os.listdir(src)):
        if f.endswith('.cpp'):
            d = open(os.path.join(src, f), encoding='latin-1').read()
            for m in REG.finditer(d):
                rows.append([m.group(3), m.group(1), ','.join(b.strip() for b in (m.group(2) or '').split(',') if b.strip()),
                             f, d.count('\n', 0, m.start()) + 1])
    return rows


def main(path, src):
    api = parse(path)
    defs = read('python_defs.tsv')
    reg = registrations(src)
    write('python_classes.tsv', ['python_class', 'cpp_class', 'bases', 'file', 'line'], reg)
    # every binding in the source: a .def("name", &f) belongs to the class_<X> it is chained to, the nearest
    # class_<X> above it in the same file (a registration, or a function taking python::class_<X>& x).
    # Read from the source rather than python_defs.tsv, which misses bindings of virtual methods (their address
    # is a vcall thunk in the listing) and of functions no unit compiles.
    own = collections.defaultdict(set)
    bind_rows = []
    for f in sorted(os.listdir(src)):
        if not f.endswith('.cpp'):
            continue
        d = open(os.path.join(src, f), encoding='latin-1').read()
        marks = [(m.start(), m.group(1)) for m in re.finditer(r'class_<\s*([\w:]+)', d)]
        for m in re.finditer(r'\.def\(\s*"(\w+)"\s*,\s*&?\s*([\w:]+)', d):
            if '//' in d[d.rfind('\n', 0, m.start()):m.start()]:
                continue
            ms = [c for pos, c in marks if pos < m.start()]
            cls = ms[-1] if ms else ''
            own[cls].add(m.group(1))
            rest = d[m.end():d.find('\n', m.end())]
            docs = re.findall(r'"([^"]*)"', rest)
            doc = docs[-1] if docs else ''
            ret = re.match(r'\s*([A-Za-z_]\w*)', doc)
            bind_rows.append([m.group(1), cls, m.group(2), f, d.count('\n', 0, m.start()) + 1, doc, ret.group(1) if ret else ''])
    write('python_bindings.tsv', ['python_name', 'cpp_class', 'target', 'file', 'line', 'doc', 'returns'], bind_rows)
    dll_names = {r[0] for r in bind_rows}
    cpp_of = {r[0]: r[1] for r in reg}
    base_of = {r[1]: [b for b in r[2].split(',') if b] for r in reg}

    def methods(cpp, seen=()):
        out = set(own.get(cpp, ()))
        for b in base_of.get(cpp, ()):
            if b not in seen:
                out |= methods(b, seen + (cpp,))
        return out

    bound_cls = {py: methods(cpp) for py, cpp in cpp_of.items()}
    api_cls = collections.defaultdict(set)
    for c, m, *_ in api:
        api_cls[c].add(m)
    where = {c: ('dll' if c in cpp_of else 'exe') for c in api_cls}
    write('py_api.tsv', ['class', 'method', 'returns', 'parameters', 'description', 'bound_by'],
          [r + [where[r[0]]] for r in api])
    exe_names = collections.defaultdict(set)
    for c, ms in api_cls.items():
        if where[c] == 'exe':
            for m in ms:
                exe_names[m].add(c)
    rows, count = [], collections.Counter()
    for c in read('py_calls.tsv'):
        if c['attribute'] != '1':
            continue
        n = c['name']
        a, b = n in dll_names, n in exe_names
        t = 'both' if a and b else 'dll' if a else 'exe' if b else 'python'
        count[t] += 1
        rows.append([c['module'], c['caller'], n, c['line'], t, ','.join(sorted(exe_names.get(n, ())))])
    write('py_targets.tsv', ['module', 'caller', 'name', 'line', 'lands_in', 'exe_classes'], rows)
    chk = []
    for c in sorted(api_cls):
        if where[c] != 'dll':
            continue
        for m in sorted(api_cls[c] - bound_cls[c]):
            chk.append([c, m, 'missing', 'in the reference, not bound by the DLL for this class',
                        'bound elsewhere in the DLL' if m in dll_names else ''])
        for m in sorted(bound_cls[c] - api_cls[c]):
            chk.append([c, m, 'added', 'bound by the DLL, not in the reference', ''])
    write('py_api_check.tsv', ['class', 'method', 'status', 'meaning', 'note'], chk)
    used = collections.Counter(r[2] for r in rows)
    miss_used = sorted({(r[0], r[1]) for r in chk if r[2] == 'missing' and r[1] in used and r[1] not in dll_names
                        and r[1] not in exe_names})
    print('reference: %d methods in %d classes (%d bound by the DLL, %d by the exe)'
          % (len(api), len(api_cls), sum(1 for v in where.values() if v == 'dll'), sum(1 for v in where.values() if v == 'exe')))
    print('Python attribute calls: ' + ', '.join('%s %d' % kv for kv in count.most_common()))
    print("check: %d missing, %d added; missing names that some Python call spells (a name match: the object may be another class): %d"
          % (sum(1 for r in chk if r[2] == 'missing'), sum(1 for r in chk if r[2] == 'added'), len(miss_used)))
    for c, m in miss_used:
        print('   %s.%s  called %d times' % (c, m, used[m]))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
