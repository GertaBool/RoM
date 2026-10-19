#!/usr/bin/env python3
"""Extract the function skeleton of the DLL source with clang: every function, every call between them.

usage: extract_cpp.py <mirror dir> <out dir> [--jobs N] [--delayed]

The mirror is the DLL source after toolchain/clang-gate/mirror.sh and forscope-pass.sh (same line numbers
as the source), with the DllExport macro of CvGameCoreDLL.h defined as a clang annotation (build.sh): clang
drops __declspec(dllexport) when it parses for a Linux target, the annotation survives. Each .cpp is parsed as a translation unit in MSVC compatibility mode with the flags of
toolchain/clang-gate/check.sh; nothing is compiled or run. Writes tab-separated files to <out dir>:
  functions.tsv   one row per function declared or defined in the source (key: clang USR)
  calls.tsv       caller -> callee, kind call (a call expression) or ref (address taken: callbacks)
  overrides.tsv   method -> the base method it overrides directly
  classes.tsv     classes defined in the source; bases.tsv: class -> base class
  python_defs.tsv functions exposed to Python by boost::python def("name", &f)
  python_calls.tsv  DLL -> Python: callFunction(module, "function") call sites
  events.tsv      CvDllPythonEvents report functions -> the event name they post to Python
  unresolved.tsv  call expressions clang could not resolve (dependent names in templates)
  diagnostics.tsv clang errors: statements whose calls may be missing from the map
  includes.tsv    file -> file it includes
"""
import ctypes, multiprocessing as mp, os, sys
import clang.cindex as ci

K = ci.CursorKind
FUNCS = {K.FUNCTION_DECL, K.CXX_METHOD, K.CONSTRUCTOR, K.DESTRUCTOR, K.CONVERSION_FUNCTION, K.FUNCTION_TEMPLATE}
SCOPES = {K.NAMESPACE, K.CLASS_DECL, K.STRUCT_DECL, K.UNION_DECL, K.CLASS_TEMPLATE,
          K.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION, K.LINKAGE_SPEC, K.UNEXPOSED_DECL}
CLASSES = {K.CLASS_DECL, K.STRUCT_DECL, K.UNION_DECL, K.CLASS_TEMPLATE}
GATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'toolchain', 'clang-gate')


def clang_args(mirror, delayed):
    sdk = os.environ['BTS_SDK_DIR']
    a = ['-x', 'c++', '-std=gnu++98', '-fms-extensions', '-fms-compatibility', '-Wno-everything',
         '-ferror-limit=0', '-Wno-error=non-pod-varargs', '-Wno-error=invalid-token-paste',
         '-resource-dir', os.environ.get('CLANG_RESOURCE_DIR', '/usr/lib/llvm-18/lib/clang/18'),
         '-I' + os.path.abspath(GATE), '-I' + mirror,
         '-isystem', sdk + '/Boost-1.32.0/include', '-isystem', sdk + '/Python24/include',
         '-DWIN32', '-D_WINDOWS', '-D_USRDLL', '-DCVGAMECOREDLL_EXPORTS', '-DNDEBUG', '-DFINAL_RELEASE']
    return a + (['-fdelayed-template-parsing'] if delayed else [])


def setup_lib():
    lib = ci.conf.lib
    lib.clang_getSpecializedCursorTemplate.argtypes = [ci.Cursor]
    lib.clang_getSpecializedCursorTemplate.restype = ci.Cursor
    lib.clang_getSpecializedCursorTemplate.errcheck = ci.Cursor.from_result   # None for the null cursor
    lib.clang_getOverriddenCursors.argtypes = [ci.Cursor, ctypes.POINTER(ctypes.POINTER(ci.Cursor)),
                                               ctypes.POINTER(ctypes.c_uint)]
    lib.clang_getOverriddenCursors.restype = None
    lib.clang_disposeOverriddenCursors.argtypes = [ctypes.POINTER(ci.Cursor)]
    lib.clang_disposeOverriddenCursors.restype = None
    return lib


def overridden(lib, c):
    arr, n = ctypes.POINTER(ci.Cursor)(), ctypes.c_uint(0)
    lib.clang_getOverriddenCursors(c, ctypes.byref(arr), ctypes.byref(n))
    out = [arr[i].get_usr() for i in range(n.value)]
    if n.value: lib.clang_disposeOverriddenCursors(arr)
    return out


def qualname(c):
    parts, p = [], c.semantic_parent
    while p is not None and p.kind != K.TRANSLATION_UNIT:
        if p.spelling: parts.append(p.spelling)
        p = p.semantic_parent
    return '::'.join(reversed(parts))


def literal(c):
    """First string literal under a cursor, without its quotes."""
    for d in c.walk_preorder():
        if d.kind == K.STRING_LITERAL:
            s = d.spelling
            return s[s.find('"') + 1:-1] if '"' in s else s
    return None


def first_function_ref(c):
    for d in c.walk_preorder():
        if d.kind in (K.DECL_REF_EXPR, K.MEMBER_REF_EXPR) and d.referenced is not None and d.referenced.kind in FUNCS:
            return d.referenced
    return None


def callee_loc(call):
    """Where the called name is written: clang dates a call in a chain a.f().g() to the start of the chain."""
    for ch in call.get_children():
        for d in [ch] + (list(ch.get_children())[:1] if ch.kind == K.UNEXPOSED_EXPR else []):
            if d.kind in (K.MEMBER_REF_EXPR, K.DECL_REF_EXPR) and d.location.file is not None:
                return d.location
        break
    return call.location


def work(job):
    path, mirror, delayed = job
    lib = setup_lib()
    tu = ci.Index.create().parse(path, args=clang_args(mirror, delayed))
    root = os.path.realpath(mirror).rstrip('/') + '/'
    real = {}

    def rel(f):
        """Path relative to the mirror, with case-alias symlinks resolved to the real file; None outside it."""
        if not f: return None
        if f not in real:
            r = os.path.realpath(f)
            real[f] = r[len(root):] if r.startswith(root) else None
        return real[f]
    out = {k: [] for k in ('funcs', 'calls', 'over', 'classes', 'bases', 'pydefs', 'pycalls', 'events',
                           'unres', 'diags', 'incl')}
    tname = os.path.basename(path)
    for d in tu.diagnostics:
        if d.severity >= ci.Diagnostic.Error and d.location.file is not None and rel(d.location.file.name):
            out['diags'].append((rel(d.location.file.name), d.location.line, tname, d.spelling))
    for inc in tu.get_includes():
        a, b = rel(inc.source.name), rel(inc.include.name)
        if a and b: out['incl'].append((a, b))

    def target(ref):
        """USR of the function a reference resolves to, folding template specializations onto their template."""
        t = lib.clang_getSpecializedCursorTemplate(ref)
        if t is not None and t.get_usr():
            return t.get_usr(), t
        return ref.get_usr(), ref

    def annotated(c):
        return any(ch.kind == K.DLLEXPORT_ATTR or (ch.kind == K.ANNOTATE_ATTR and ch.spelling == 'DllExport')
                   for ch in c.get_children())

    def record_func(c, f):
        p = c.semantic_parent   # MSVC: a class declared DllExport exports all its members
        exported = annotated(c) or (p is not None and p.kind in CLASSES and annotated(p))
        is_m = c.kind in (K.CXX_METHOD, K.CONSTRUCTOR, K.DESTRUCTOR, K.CONVERSION_FUNCTION)
        out['funcs'].append(dict(usr=c.get_usr(), name=c.spelling, scope=qualname(c), sig=c.displayname,
                                 kind=c.kind.name.lower(), file=f, line=c.extent.start.line,
                                 end=c.extent.end.line, definition=int(c.is_definition()), exported=int(exported),
                                 virtual=int(is_m and c.is_virtual_method()),
                                 pure=int(is_m and c.is_pure_virtual_method()),
                                 static=int(is_m and c.is_static_method())))
        if is_m and c.is_virtual_method():
            for b in overridden(lib, c): out['over'].append((c.get_usr(), b))

    def body(fn, fusr, fname):
        callee_refs = set()
        for d in fn.walk_preorder():
            if d.kind == K.CALL_EXPR:
                ref = d.referenced
                loc = callee_loc(d)
                if ref is None or ref.kind not in FUNCS:
                    if ref is None and d.spelling:
                        out['unres'].append((fusr, rel(loc.file.name) if loc.file else '', loc.line, d.spelling))
                    continue
                usr, t = target(ref)
                callee_refs.add((loc.line, loc.column))
                lf = t.location.file.name if t.location.file else None
                if rel(lf):
                    out['calls'].append((fusr, usr, 'call', rel(loc.file.name) if loc.file else '', loc.line))
                    if usr not in seen_decl:
                        seen_decl.add(usr); record_func(t, rel(lf))
                if d.spelling == 'callFunction':
                    args = list(d.get_arguments())
                    if len(args) >= 2:
                        out['pycalls'].append((fusr, literal(args[0]) or '?', literal(args[1]) or '?',
                                               rel(loc.file.name) if loc.file else '', loc.line))
                elif d.spelling == 'def' and (ref.semantic_parent.spelling in ('class_', 'python') or
                                              'boost' in (ref.get_usr() or '')):
                    args = list(d.get_arguments())
                    if len(args) >= 2:
                        f2 = first_function_ref(args[1])
                        if f2 is not None:
                            u2, t2 = target(f2)
                            out['pydefs'].append((literal(args[0]) or '?', u2, qualname(t2), t2.spelling,
                                                  rel(loc.file.name) if loc.file else '', loc.line))
                elif d.spelling == 'add' and fname.startswith('CvDllPythonEvents::') and not events_seen.get(fusr):
                    lit = literal(d)
                    if lit: events_seen[fusr] = lit; out['events'].append((fusr, lit))
        for d in fn.walk_preorder():   # function addresses taken (callbacks), not as the callee of a call
            if d.kind == K.DECL_REF_EXPR and d.referenced is not None and d.referenced.kind in FUNCS \
                    and (d.location.line, d.location.column) not in callee_refs:
                usr, t = target(d.referenced)
                lf = t.location.file.name if t.location.file else None
                if rel(lf) and usr != fusr:
                    out['calls'].append((fusr, usr, 'ref', rel(d.location.file.name), d.location.line))
                    if usr not in seen_decl:
                        seen_decl.add(usr); record_func(t, rel(lf))

    seen_decl, events_seen = set(), {}

    def visit(c):
        for ch in c.get_children():
            f = rel(ch.location.file.name) if ch.location.file else None
            if not f: continue
            if ch.kind in FUNCS:
                if ch.get_usr() not in seen_decl or ch.is_definition():
                    seen_decl.add(ch.get_usr()); record_func(ch, f)
                if ch.is_definition():
                    q = qualname(ch)
                    body(ch, ch.get_usr(), (q + '::' if q else '') + ch.spelling)
            elif ch.kind in SCOPES:
                if ch.kind in CLASSES and ch.is_definition() and ch.spelling:
                    out['classes'].append((ch.get_usr(), (qualname(ch) + '::' if qualname(ch) else '') + ch.spelling,
                                           ch.kind.name.lower(), f, ch.extent.start.line))
                    for b in ch.get_children():
                        if b.kind == K.CXX_BASE_SPECIFIER:
                            bd = b.referenced
                            out['bases'].append((ch.get_usr(), bd.get_usr() if bd else '', b.type.spelling,
                                                 b.access_specifier.name.lower()))
                visit(ch)
    visit(tu.cursor)
    return tname, out


STRIP = []   # the mirror's absolute path, which clang writes into names of anonymous types


def write(path, header, rows):
    def clean(x):
        x = str(x).replace('\t', ' ').replace('\n', ' ')
        for s in STRIP: x = x.replace(s, '')
        return x
    with open(path, 'w', encoding='utf-8') as o:
        o.write('\t'.join(header) + '\n')
        for r in rows: o.write('\t'.join(clean(x) for x in r) + '\n')


def main():
    mirror, outdir = os.path.abspath(sys.argv[1]), sys.argv[2]
    STRIP.extend([os.path.realpath(mirror) + '/', mirror + '/'])
    jobs = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else os.cpu_count()
    delayed = '--delayed' in sys.argv
    os.makedirs(outdir, exist_ok=True)
    cpps = sorted(os.path.join(mirror, f) for f in os.listdir(mirror) if f.endswith('.cpp'))
    funcs, sets = {}, {k: set() for k in ('calls', 'over', 'classes', 'bases', 'pydefs', 'pycalls', 'events',
                                          'unres', 'diags', 'incl')}
    with mp.Pool(jobs) as pool:
        for tname, out in pool.imap_unordered(work, [(p, mirror, delayed) for p in cpps]):
            for f in out['funcs']:   # a definition wins over a declaration; flags are the union over TUs
                old = funcs.get(f['usr'])
                if old is None or (f['definition'] and not old['definition']):
                    if old: f['exported'] |= old['exported']; f['virtual'] |= old['virtual']
                    funcs[f['usr']] = f
                else:
                    old['exported'] |= f['exported']; old['virtual'] |= f['virtual']
            for k in sets: sets[k].update(map(tuple, out[k]))
    ids = {u: i + 1 for i, u in enumerate(sorted(funcs, key=lambda u: (funcs[u]['file'], funcs[u]['line'], u)))}
    cols = ['id', 'scope', 'name', 'sig', 'kind', 'file', 'line', 'end', 'definition', 'exported', 'virtual',
            'pure', 'static', 'usr']
    write(os.path.join(outdir, 'functions.tsv'), cols,
          [[ids[u]] + [funcs[u][c] for c in cols[1:]] for u in sorted(funcs, key=ids.get)])
    calls = sorted({(ids[a], ids[b], k, f, l) for a, b, k, f, l in sets['calls'] if a in ids and b in ids},
                   key=lambda r: (r[0], r[4], r[1], r[2]))
    write(os.path.join(outdir, 'calls.tsv'), ['caller', 'callee', 'kind', 'file', 'line'], calls)
    write(os.path.join(outdir, 'overrides.tsv'), ['method', 'overrides'],
          sorted((ids[a], ids[b]) for a, b in sets['over'] if a in ids and b in ids))
    cls = {r[0]: r for r in sets['classes']}
    write(os.path.join(outdir, 'classes.tsv'), ['class', 'kind', 'file', 'line', 'usr'],
          sorted((r[1], r[2], r[3], r[4], r[0]) for r in cls.values()))
    write(os.path.join(outdir, 'bases.tsv'), ['class', 'base', 'access'],
          sorted((cls[a][1] if a in cls else a, (cls[b][1] if b in cls else t), acc) for a, b, t, acc in sets['bases']))
    write(os.path.join(outdir, 'python_defs.tsv'), ['python_name', 'function', 'cpp_scope', 'cpp_name', 'file', 'line'],
          sorted((n, ids.get(u, ''), s, cn, f, l) for n, u, s, cn, f, l in sets['pydefs']))
    write(os.path.join(outdir, 'python_calls.tsv'), ['caller', 'module', 'python_function', 'file', 'line'],
          sorted((ids.get(a, ''), m, fx, f, l) for a, m, fx, f, l in sets['pycalls']))
    write(os.path.join(outdir, 'events.tsv'), ['function', 'event'],
          sorted((ids.get(a, ''), e) for a, e in sets['events']))
    write(os.path.join(outdir, 'unresolved.tsv'), ['caller', 'file', 'line', 'spelling'],
          sorted((ids.get(a, ''), f, l, s) for a, f, l, s in sets['unres']))
    write(os.path.join(outdir, 'diagnostics.tsv'), ['file', 'line', 'unit', 'error'], sorted(sets['diags']))
    write(os.path.join(outdir, 'includes.tsv'), ['file', 'includes'], sorted(sets['incl']))
    print(f'{len(cpps)} units, {len(funcs)} functions, {len(calls)} call edges', file=sys.stderr)


if __name__ == '__main__':
    main()
