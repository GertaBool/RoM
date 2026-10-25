#!/usr/bin/env python3
"""Read the function map of the DLL from the real compiler's output (compile.sh): the assembly listings
(/FAs) and objects of every unit, and the CodeView type records of the precompiled header's object.

usage: extract_asm.py <compile.sh out dir> <compile.sh source copy dir> <map dir>

What each table comes from:
- A function is a PROC of a listing whose source file is one of the DLL's files (functions of the
  compiler's headers, Boost and Python are left out). Its first and last line are the first and last
  source line the listing shows inside it (the line of the opening brace, then the closing one).
- `call` is a direct call (`call ?name`), `ref` a function whose address the code takes
  (`OFFSET FLAT:?name`), `virtual` a call through the object's table of virtual functions
  (`call DWORD PTR [reg+N]`, slot N/4). A virtual call is resolved by the slot together with the
  method names written in the statement: a class whose slot N holds a method named there. The callee is
  that method of the class that introduces the slot; overrides.tsv lists what may run instead.
- Overrides come from the tables of virtual functions in the listings (`??_7Class@@6B@`): where a class
  has a different function in a slot than its base, it overrides the base's.
- Classes, bases and the names of virtual slots come from the type records (llvm-readobj --codeview).
- Exports are the /EXPORT directives of each object's .drectve section.
- Python bindings: in functions that call boost::python, a function address pushed right before a string
  (def("name", &f, ...) pushes its arguments right to left). Calls into Python: the two strings pushed
  in the statement of a call to CvDLLPythonIFaceBase::callFunction. Events: the string passed to
  CyArgsList::add in each CvDllPythonEvents report function.
Calls to the compiler's library, Boost and Python's C API, and imported functions, are left out.
"""
import collections, os, re, struct, subprocess, sys, zlib

SRC = re.compile(r'^; (\d+)\s*:(.*)$')
FILE = re.compile(r'^; File (.+)$')
PROC = re.compile(r'^(\S+)\s+PROC\b')
ANON = re.compile(r'\?A0x([0-9a-f]+)@')
ENDP = re.compile(r'^(\S+)\s+ENDP\b')
INSN = re.compile(r'^\t(\w+)\t?(.*?)\s*(?:;.*)?$')
OFFS = re.compile(r'OFFSET FLAT:([^\s,\]]+)')
STRDEF = re.compile(r'^(\$SG\d+)\s+DB\s+(.*?)\s*$')
DBCONT = re.compile(r'^\tDB\t(.*?)\s*$')
VFT = re.compile(r'^(\?\?_7\S+)\s+DD\s+FLAT:(\S+)')
DDENT = re.compile(r'^\tDD\tFLAT:(\S+)')
SLOT = re.compile(r'^DWORD PTR \[(e[a-z]{2})(?:\+(\d+))?\]$')
IDENT_CALL = re.compile(r'\b([A-Za-z_]\w*)\s*\(')
TEMP = re.compile(r'^DWORD PTR (tv\d+|\$T\d+)\[ebp\]$')
TEMPSET = re.compile(r'^DWORD PTR (tv\d+|\$T\d+)\[ebp\], eax$')
CALLCONV = re.compile(r'\b__(thiscall|cdecl|stdcall|fastcall)\b ')


def db_text(s):
    """The bytes of a DB directive as text: 'abc', 0aH, 'def' -> abc\\ndef (a trailing 00H ends it)."""
    out, i = [], 0
    for m in re.finditer(r"'((?:[^']|'')*)'|([0-9a-fA-F]+)H|(\d+)", s):
        if m.group(1) is not None: out.append(m.group(1).replace("''", "'"))
        else:
            v = int(m.group(2), 16) if m.group(2) else int(m.group(3))
            if v: out.append(chr(v))
    return ''.join(out)


def parse_listing(path, projdir):
    """One unit's listing: functions, call sites, strings, vftables."""
    text = open(path, encoding='latin-1').read().replace('\r\n', '\n')
    # the compiler names an anonymous namespace with a hash that changes with every compile; replace each by
    # a number fixed by the unit's name and its order of appearance, so that rebuilds give the same names
    anon = {}
    for h in ANON.findall(text): anon.setdefault(h, '%08x' % zlib.crc32(f'{os.path.basename(path)}:{len(anon)}'.encode()))
    lines = ANON.sub(lambda m: '?A0x' + anon[m.group(1)] + '@', text).split('\n')
    funcs, sites, strings, vfts = {}, [], {}, {}
    cur_file, fn, block, block_open, stmt_push, last_str = None, None, [], False, [], None
    vft, i = None, 0
    while i < len(lines):
        ln = lines[i]; i += 1
        m = FILE.match(ln)
        if m:
            p = m.group(1).strip().lower().replace('/', '\\')
            rest = p[len(projdir):] if p.startswith(projdir) else None
            cur_file = rest if rest and '\\' not in rest else None   # directly in the source folder (not Boost, Python)
            continue
        m = STRDEF.match(ln)
        if m and fn is None:
            label, body = m.group(1), m.group(2)
            while i < len(lines) and DBCONT.match(lines[i]):
                body += ', ' + DBCONT.match(lines[i]).group(1); i += 1
            strings[label] = db_text(body); continue
        if fn is None:
            m = VFT.match(ln)
            if m:
                vft = m.group(1); vfts[vft] = [] if m.group(2).startswith('??_R4') else [m.group(2)]; continue
            m = DDENT.match(ln)
            if m and vft: vfts[vft].append(m.group(1)); continue
            vft = None
            m = PROC.match(ln)
            if m and cur_file:
                fn = m.group(1); funcs[fn] = dict(file=cur_file, first=None, last=None)
                block, block_open, stmt_push, last_str = [], False, [], None
                recent, last_call, fn_text, temps = [], None, [], {}
            continue
        if ENDP.match(ln):
            fn = None; continue
        m = SRC.match(ln)
        if m:
            n = int(m.group(1))
            if not block_open: block, stmt_push = [], []; block_open = True
            block.append((n, m.group(2))); fn_text.append(m.group(2))
            if cur_file == funcs[fn]['file']:
                f = funcs[fn]; f['first'] = f['first'] or n; f['last'] = n
            continue
        m = INSN.match(ln)
        if not m: continue
        if block_open: last_call, recent = None, []   # a new statement: nothing carries over from the last one
        block_open = False
        op, arg = m.group(1), m.group(2)
        recent.append((op, arg))
        tm = TEMPSET.match(arg) if op == 'mov' else None
        if tm and last_call is not None: temps[tm.group(1)] = last_call   # a call's result kept in a temporary
        line = block[-1][0] if block else None
        text = ' '.join(t for _, t in block)
        for o in OFFS.findall(arg):
            if o.startswith('$SG'):
                if op == 'push': stmt_push.append(('s', o))
                continue
            if op == 'push': stmt_push.append(('f', o))
            sites.append(dict(caller=fn, kind='ref', target=o, file=cur_file, line=line))
        if op in ('call', 'jmp'):
            a = arg.strip()
            if a.startswith('SHORT ') or a.startswith('$'): continue
            if a.startswith('DWORD PTR __imp_'):
                sites.append(dict(caller=fn, kind='import', target=a[16:], file=cur_file, line=line)); continue
            s = SLOT.match(a)
            # the object of a call is what was last moved into ecx: `this`, the result of the call just before
            # (eax), or a temporary that held a call's result
            src_ecx = next((x[5:] for o, x in reversed(recent) if o == 'mov' and x.startswith('ecx, ')), None)
            if src_ecx == 'DWORD PTR _this$[ebp]': obj = 'this'
            elif src_ecx == 'eax': obj = last_call
            elif src_ecx and TEMP.match(src_ecx): obj = temps.get(TEMP.match(src_ecx).group(1))
            else: obj = None
            if s:
                sites.append(dict(caller=fn, kind='virtual', slot=int(s.group(2) or 0), file=cur_file, line=line,
                                  text=text, strs=[strings.get(x, x) for k, x in stmt_push if k == 's'], lines=list(block),
                                  obj=obj, idx=len(sites), fn_text=fn_text))
                last_call, recent = ('site', len(sites) - 1), []
                continue
            if a.startswith('?') or (a.startswith('_') and 'PTR' not in a):
                sites.append(dict(caller=fn, kind='call', target=a.split()[0], file=cur_file, line=line, text=text,
                                  strs=[x for k, x in stmt_push if k == 's'], pushes=list(stmt_push), lines=list(block)))
                last_call, recent = ('sym', a.split()[0]), []
                continue
            last_call, recent = None, []
            sites.append(dict(caller=fn, kind='pointer', target=a, file=cur_file, line=line, text=text))
    for s in sites:   # strings were collected per unit; resolve labels now that all are known
        if 'strs' in s: s['strs'] = [strings.get(x, x) for x in s['strs']]
        if 'pushes' in s: s['pushes'] = [(k, strings.get(x, x) if k == 's' else x) for k, x in s['pushes']]
    return funcs, sites, vfts


def exports(obj):
    d = open(obj, 'rb').read()
    if len(d) < 20: return set()
    nsec, opt = struct.unpack_from('<H', d, 2)[0], struct.unpack_from('<H', d, 16)[0]
    out = set()
    for k in range(nsec):
        o = 20 + opt + k * 40
        if d[o:o + 8].rstrip(b'\0') == b'.drectve':
            size, ptr = struct.unpack_from('<II', d, o + 16)
            for x in d[ptr:ptr + size].decode('latin-1').split():
                if x.lower().startswith(('/export:', '-export:')): out.add(x.split(':', 1)[1].split(',')[0])
    return out


def demangle(names):
    names = sorted(set(names))
    r = subprocess.run(['llvm-undname-18'], input='\n'.join(names) + '\n', capture_output=True, text=True)
    out, lines = {}, r.stdout.split('\n')
    for k in range(0, len(lines) - 1, 3):     # each input: its line, the result, a blank line
        if k + 1 < len(lines): out[lines[k]] = lines[k + 1]
    return out


def split_demangled(d):
    """'public: virtual bool __thiscall CvCity::isX(class CvPlot const *) const' ->
    (scope, name, args, flags)"""
    flags = set(w for w in ('virtual', 'static') if re.search(r'\b' + w + r'\b', d.split('(')[0]))
    m = CALLCONV.search(d)
    q = d[m.end():] if m else d
    depth, cut = 0, None
    for k, ch in enumerate(q):
        if ch == '<': depth += 1
        elif ch == '>': depth -= 1
        elif ch == '(' and depth == 0: cut = k; break
    if cut is None: return '', q, '', flags
    qual, rest = q[:cut], q[cut:]
    depth, parts, k0 = 0, [], 0
    for k, ch in enumerate(qual):
        if ch == '<': depth += 1
        elif ch == '>': depth -= 1
        elif qual.startswith('::', k) and depth == 0: parts.append(qual[k0:k]); k0 = k + 2
    parts.append(qual[k0:])
    clean = lambda s: re.sub(r'\b(class|struct|enum|union) ', '', s).replace(' *', '*').replace(' &', '&') \
        .replace('(void)', '()')
    return clean('::'.join(parts[:-1])), parts[-1], clean(rest), flags


def parse_types(cv_text):
    """Classes from llvm-readobj --codeview: name -> dict(bases=[(name, offset)], own={offset: name} for
    the virtual methods a class introduces, ovl=names of overloaded virtual methods it introduces, nslots,
    pure=names). For an overload set llvm-readobj prints one offset for every member, so its slots are
    not known: such a method is matched by name within the class's slots."""
    rec = {}
    for m in re.finditer(r'^  (\w+) \((0x[0-9A-F]+)\) \{\n(.*?)\n  \}$', cv_text, re.S | re.M):
        rec[m.group(2)] = (m.group(1), m.group(3))
    classes = {}
    for idx, (kind, body) in rec.items():
        if kind not in ('Class', 'Struct'): continue
        if 'ForwardReference' in body: continue
        name = re.search(r'^    Name: (.*)$', body, re.M).group(1)
        fl = re.search(r'FieldList: .*\((0x[0-9A-F]+)\)', body)
        vs = re.search(r'VShape: .*\((0x[0-9A-F]+)\)', body)
        nslots = 0
        if vs and vs.group(1) in rec:
            c = re.search(r'VFEntryCount: (\d+)', rec[vs.group(1)][1]); nslots = int(c.group(1)) if c else 0
        bases, virt, intro, pure, ovl = [], {}, set(), set(), set()
        fbody = rec.get(fl.group(1), ('', ''))[1] if fl else ''
        for b in re.finditer(r'    BaseClass \{.*?BaseType: (.*?) \(0x[0-9A-F]+\).*?BaseOffset: (0x[0-9A-F]+)', fbody, re.S):
            bases.append((b.group(1), int(b.group(2), 16)))
        rets = {}
        for om in re.finditer(r'    OneMethod \{(.*?)\n    \}', fbody, re.S):
            t = om.group(1); n = re.search(r'Name: (.*)', t).group(1)
            ty = re.search(r'Type: (.*?) [^ ]*::\(', t)
            if ty: rets[n] = ty.group(1)
            mk = re.search(r'MethodKind: (\w+)', t)
            if mk and 'Pure' in mk.group(1): pure.add(n)
            o = re.search(r'VFTableOffset: (0x[0-9A-F]+)', t)
            if o: virt[int(o.group(1), 16)] = n; intro.add(n)
        for ov in re.finditer(r'    OverloadedMethod \{.*?MethodListIndex: (0x[0-9A-F]+).*?Name: (.*?)\n', fbody, re.S):
            ml = rec.get(ov.group(1), ('', ''))[1]; n = ov.group(2)
            entries = re.findall(r'Method \[(.*?)\]', ml, re.S)
            offs = [int(o, 16) for e in entries for o in re.findall(r'VFTableOffset: (0x[0-9A-F]+)', e)]
            if any('Pure' in e for e in entries): pure.add(n)
            if offs: ovl.add(n); intro.add(n)   # the slots of an overload set are not known from the records
        if name not in classes or len(fbody) > classes[name].get('_len', 0):
            classes[name] = dict(bases=bases, own=virt, ovl=ovl, nslots=nslots, introduces=intro, pure=pure,
                                 rets=rets, _len=len(fbody))
    return classes


def main():
    out, bdir, mapdir = sys.argv[1], sys.argv[2], sys.argv[3]
    projdir = ('z:' + os.path.realpath(bdir).replace('/', '\\') + '\\').lower()
    projfiles = {f.lower(): f for f in os.listdir(bdir) if f.endswith(('.cpp', '.h', '.inl'))}
    funcs, sites, vfts, exp = {}, [], {}, set()
    units = sorted(f for f in os.listdir(out) if f.endswith('.asm'))
    for u in units:
        fs, ss, vs = parse_listing(os.path.join(out, u), projdir)
        for k, v in fs.items():
            v['file'] = projfiles.get(v['file'], v['file'])
            if k not in funcs or (funcs[k]['first'] is None and v['first']): funcs[k] = v
        base = len(sites)   # site indices were counted per unit
        for s in ss:
            if s.get('file'): s['file'] = projfiles.get(s['file'], s['file'])
            s['unit'] = u
            if 'idx' in s: s['idx'] += base
            if isinstance(s.get('obj'), tuple) and s['obj'][0] == 'site': s['obj'] = ('site', s['obj'][1] + base)
        sites += ss; vfts.update(vs)
        obj = os.path.join(out, u[:-4] + '.obj')
        if os.path.exists(obj): exp |= exports(obj)
    # the type records are read in full; llvm-readobj stops later, in the symbol records it does not
    # read for this compiler's version, which are not used
    cv = subprocess.run(['llvm-readobj-18', '--codeview', os.path.join(out, 'codemap_types.obj')],
                        capture_output=True, text=True).stdout
    classes = parse_types(cv)
    names = set(funcs) | {s['target'] for s in sites if s.get('target', '').startswith('?')} | set(vfts) | \
            {x for v in vfts.values() for x in v if x.startswith('?')}
    dm = demangle(names)

    # the project's classes: defined in the DLL's own files (by text: class/struct Name followed by { or :)
    src = '\n'.join(open(os.path.join(bdir, f), encoding='latin-1').read() for f in projfiles.values())
    own = set(re.findall(r'\b(?:class|struct)\s+(?:DllExport\s+)?([A-Za-z_]\w*)\s*(?::[^;{]*)?\{', src))
    base_name = lambda n: re.sub(r'<.*$', '', n).split('::')[-1]
    class_at, texts = {}, {}   # class name -> (header, line of its definition); file -> lines
    for f in sorted(projfiles.values()):
        texts[f] = open(os.path.join(bdir, f), encoding='latin-1').read().replace('\r\n', '\n').split('\n')
        for k, ln in enumerate(texts[f]):
            for cn in re.findall(r'^\s*(?:class|struct)\s+(?:DllExport\s+)?([A-Za-z_]\w*)\s*(?::[^;{]*)?\{?\s*$', ln):
                if f.endswith('.h') or cn not in class_at: class_at.setdefault(cn, (f, k + 1))

    def declared_at(c, name):
        """Where a method is declared: its line in the class's definition, by text."""
        loc = class_at.get(base_name(c))
        if not loc: return '', ''
        f, k0 = loc
        for k in range(k0 - 1, min(len(texts[f]), k0 + 3000)):
            if k > k0 and re.match(r'^\s*\};', texts[f][k]): break
            if re.search(r'\b' + re.escape(name) + r'\s*\(', texts[f][k]): return f, k + 1
        return f, ''
    pclasses = {n: c for n, c in classes.items() if base_name(n) in own}

    def table(c, seen=()):
        """slot offset -> method name for class c (own introductions over its primary base's)."""
        t = {}
        info = classes.get(c)
        if not info: return t
        prim = [b for b, off in info['bases'] if off == 0]
        if prim and prim[0] not in seen: t.update(table(prim[0], seen + (c,)))
        t.update(info['own'])
        return t
    tables = {c: table(c) for c in classes}

    def ovl_chain(c, seen=()):
        info = classes.get(c)
        if not info: return set()
        prim = [b for b, off in info['bases'] if off == 0]
        return set(info['ovl']) | (ovl_chain(prim[0], seen + (c,)) if prim and prim[0] not in seen else set())
    ovls = {c: ovl_chain(c) for c in classes}

    def ovl_introducer(c, name):
        info = classes.get(c)
        prim = [b for b, o in info['bases'] if o == 0] if info else []
        if prim and name in ovls.get(prim[0], ()): return ovl_introducer(prim[0], name)
        return c
    vft_of = {}
    for sym, entries in vfts.items():   # ??_7Class@@6B@ is the primary table of Class
        d = dm.get(sym, '')
        mm = re.match(r"const (.*)::`vftable'$", d)
        if mm and sym.endswith('@@6B@'): vft_of[re.sub(r'\b(class|struct) ', '', mm.group(1))] = entries

    def introducer(c, off, name):
        info = classes.get(c)
        prim = [b for b, o in info['bases'] if o == 0] if info else []
        if prim and tables.get(prim[0], {}).get(off) == name: return introducer(prim[0], off, name)
        return c

    nodes = {}   # key -> function record (defined functions and declared virtual methods)
    LIBRARY = re.compile(r'^(std|stdext|boost|__)\b|^_')   # library templates the compiler instantiated here
    for k, f in funcs.items():
        scope, name, args, flags = split_demangled(dm.get(k, k))
        if LIBRARY.match(scope): continue
        nodes[k] = dict(scope=scope, name=name, sig=name + args, file=f['file'], line=f['first'] or '',
                        end=f['last'] or '', definition=1, exported=int(k in exp), virtual=int('virtual' in flags),
                        pure=0, static=int('static' in flags), key=k,
                        kind=('generated' if f['first'] is None else    # written by the compiler: no source lines
                              'method' if scope and scope in classes or flags & {'virtual'} else 'function'))

    def method_node(c, off, name):
        """The callee for slot off of class c: its function in the table, or a declared (pure) method."""
        impl = (vft_of.get(c) or [None] * (off // 4 + 1))
        impl = impl[off // 4] if off // 4 < len(impl) else None
        if impl and impl in nodes: return impl
        k = f'{c}::{name}'
        if k not in nodes:
            df, dl = declared_at(c, name)
            nodes[k] = dict(scope=c, name=name, sig=name + '(…)', file=df, line=dl, end='', definition=0, exported=0,
                            virtual=1, pure=int(name in classes.get(c, {}).get('pure', ())), static=0, key=k,
                            kind='method')
        return k

    edges, unres, pydefs, pycalls, events = set(), [], set(), [], {}
    resolved = {}   # site index -> the class whose method a virtual call reached, when unique

    def cls_of(type_text):
        """'class CvTechInfo &' or 'CvDLLInterfaceIFaceBase*' -> the class name, if a class."""
        x = re.sub(r'\b(class|struct|const|volatile)\b|[&*]', ' ', type_text or '').strip()
        return x if x in classes else None

    def chain(c, seen=()):
        info = classes.get(c)
        out = [c]
        for b, o in (info['bases'] if info else []):
            if b not in seen: out += chain(b, seen + (c,))
        return out

    def static_class(s):
        o = s.get('obj')
        if o == 'this': return nodes[s['caller']]['scope'] or None
        if not o: return None
        if o[0] == 'sym':
            d = dm.get(o[1], '')
            m2 = CALLCONV.search(d)
            pre = re.sub(r'^(public|private|protected): ', '', d[:m2.start()] if m2 else '')
            return cls_of(re.sub(r'\b(virtual|static)\b', '', pre))
        r = resolved.get(o[1])
        return cls_of(classes.get(r[0], {}).get('rets', {}).get(r[1])) if r else None

    def at(s, name):
        """The source line of a call: in a statement over several lines, the one where the name is written."""
        return next((n for n, tx in s.get('lines', ()) if re.search(r'\b' + re.escape(name) + r'\s*\(', tx)), s['line'])
    for s in sites:
        c = s['caller']
        if c not in nodes: continue
        if s['kind'] in ('call', 'ref'):
            t = s['target']
            if t in nodes and (t != c or s['kind'] == 'call'):   # recursion is a call; a function's own address is not
                edges.add((c, t, s['kind'], s['file'], at(s, nodes[t]['name']) if s['kind'] == 'call' else s['line'], ''))
            if s['kind'] == 'call':
                d = dm.get(t, '')
                if 'boost::python::' in d and ('::def' in d or 'class_<' in d):
                    pu = s['pushes']
                    for j in range(len(pu) - 1):
                        if pu[j][0] == 'f' and pu[j][1] in nodes and pu[j + 1][0] == 's':
                            nm = pu[j + 1][1]
                            line = next((n for n, tx in s['lines'] if f'"{nm}"' in tx), s['line'])
                            pydefs.add((nm, pu[j][1], s['file'], line))
                if 'CyArgsList::add(char const *)' in d and nodes[c]['scope'] == 'CvDllPythonEvents' and s['strs'] \
                        and c not in events:
                    events[c] = s['strs'][-1]
        elif s['kind'] == 'virtual':
            said = set(IDENT_CALL.findall(s['text']))
            said |= {n + x for n in said for x in 'AW'}   # Windows headers rename MessageBox to MessageBoxA etc.
            sl = s['slot']
            cands = {(introducer(cl, sl, tables[cl][sl]), tables[cl][sl]) for cl in tables if tables[cl].get(sl) in said}
            if not cands:   # an overload set: the name, within the class's slots, in a slot no single method holds
                cands = {(ovl_introducer(cl, n), n) for cl in tables for n in ovls[cl] & said
                         if sl < 4 * classes[cl]['nslots'] and sl not in tables[cl]}
            if not cands:
                why = ('virtual destructor (delete)' if sl == 0 and re.search(r'\bdelete\b|SAFE_DELETE', s['text']) else
                       'virtual call: no class has a method named in the statement at its slot')
                unres.append((c, s['file'], s['line'], why, f'slot {sl // 4}: ' + s['text'][:150])); continue
            st = static_class(s)
            if st:
                ch = set(chain(st))
                narrowed = {(cl, n) for cl, n in cands if cl in ch}
                if not narrowed:   # the class introducing the method may lie below the static class's own table
                    narrowed = {(cl, n) for cl, n in cands if st in chain(cl) or cl in ch}
                cands = narrowed or cands
            for cl0 in {n for _, n in cands}:   # the receiver's declared type, from the function's own source lines
                r = re.search(r'([A-Za-z_]\w*)\s*(?:\.|->)\s*' + re.escape(cl0) + r'\s*\(', s['text'])
                if not r: continue
                var = re.escape(r.group(1))
                decl = re.search(r'\b([A-Za-z_]\w*)\s*(?:const\s*)?[&*]*\s*' + var + r'\s*(?:=|;|,|\))',
                                 ' '.join(s['fn_text']))
                if decl and decl.group(1) in classes:
                    ch = set(chain(decl.group(1)))
                    narrowed = {(cl, n) for cl, n in cands if n != cl0 or cl in ch}
                    if narrowed and len(narrowed) < len(cands): cands = narrowed
                    if not st and len({n for _, n in cands}) == 1: st = decl.group(1)
            own_c = {(cl, n) for cl, n in cands if base_name(cl) in own}
            cands = own_c or cands
            if len(cands) == 1: resolved[s['idx']] = next(iter(cands))
            for cl, n in sorted(cands):
                # with the static class known and its table in the DLL, the function in that table's slot; the
                # class is kept with the call, since only methods of it and its subclasses can run
                k = (vft_of[st][sl // 4] if st and st in vft_of and cl in chain(st) and sl // 4 < len(vft_of[st])
                     and vft_of[st][sl // 4] in nodes else method_node(cl, s['slot'], n))
                edges.add((c, k, 'virtual', s['file'], at(s, n), st if st and (cl in chain(st) or st in chain(cl)) else ''))
                if n == 'callFunction' and cl == 'CvDLLPythonIFaceBase':
                    ps = s['strs']
                    pycalls.append((c, ps[-1] if len(ps) >= 2 else '?', ps[-2] if len(ps) >= 2 else (ps[-1] if ps else '?'),
                                    s['file'], s['line']))
            if len(cands) > 1:
                unres.append((c, s['file'], s['line'], 'virtual call: several candidate methods',
                              f'{len(cands)} candidates: ' + s['text'][:150]))
        elif s['kind'] == 'pointer':
            unres.append((c, s['file'], s['line'], 'through a function pointer', s['text'][:160]))

    over = set()   # a class's table against its primary base's: a different function overrides the base's
    for cl, entries in vft_of.items():
        info = classes.get(cl)
        prim = [b for b, o in info['bases'] if o == 0] if info else []
        if not prim: continue
        b = prim[0]; bt = vft_of.get(b, [])
        for j, e in enumerate(entries):
            if e not in nodes: continue
            be = bt[j] if j < len(bt) else None
            if be == e: continue
            name = tables.get(cl, {}).get(4 * j) or nodes[e]['name']
            if j >= max(classes.get(b, {}).get('nslots', 0), len(bt)): continue   # a slot the base does not have
            target = be if be in nodes else method_node(introducer(b, 4 * j, name), 4 * j, name)
            over.add((e, target))

    ids = {k: i + 1 for i, k in enumerate(sorted(nodes, key=lambda k: (nodes[k]['file'], str(nodes[k]['line']), k)))}
    def w(name, header, rows):
        with open(os.path.join(mapdir, name), 'w', encoding='utf-8') as o:
            o.write('\t'.join(header) + '\n')
            for r in rows: o.write('\t'.join(('' if x is None else str(x)).replace('\t', ' ').replace('\n', ' ') for x in r) + '\n')
    os.makedirs(mapdir, exist_ok=True)
    cols = ['id', 'scope', 'name', 'sig', 'kind', 'file', 'line', 'end', 'definition', 'exported', 'virtual', 'pure',
            'static', 'key']
    w('functions.tsv', cols, [[ids[k]] + [nodes[k][c2] for c2 in cols[1:]] for k in sorted(nodes, key=ids.get)])
    w('calls.tsv', ['caller', 'callee', 'kind', 'file', 'line', 'object_class'],
      sorted(((ids[a], ids[b], kd, f, l, oc) for a, b, kd, f, l, oc in edges),
             key=lambda r: (r[0], r[4] is not None, r[4] or 0, r[1], r[2], r[3] or '', r[5])))
    w('overrides.tsv', ['method', 'overrides'], sorted((ids[a], ids[b]) for a, b in over))
    w('classes.tsv', ['class', 'virtual_slots', 'has_table_in_dll'],
      sorted((n, c['nslots'], int(n in vft_of)) for n, c in pclasses.items()))
    w('bases.tsv', ['class', 'base', 'offset'], sorted((n, b, o) for n, c in pclasses.items() for b, o in c['bases']))
    w('python_defs.tsv', ['python_name', 'function', 'cpp_scope', 'cpp_name', 'file', 'line'],
      sorted((n, ids[k], nodes[k]['scope'], nodes[k]['name'], f, l) for n, k, f, l in pydefs))
    w('python_calls.tsv', ['caller', 'module', 'python_function', 'file', 'line'],
      sorted((ids[c], m, fx, f, l) for c, m, fx, f, l in pycalls))
    w('events.tsv', ['function', 'event'], sorted((ids[c], e) for c, e in events.items()))
    w('unresolved.tsv', ['caller', 'file', 'line', 'reason', 'what'],
      sorted(((ids[c], f, l, r, t) for c, f, l, r, t in unres), key=lambda r: (r[0], r[1], str(r[2]), r[3])))
    ur = []
    for u in units:
        lg = os.path.join(out, u[:-4] + '.log')
        tx = open(lg, encoding='latin-1').read() if os.path.exists(lg) else ''
        ur.append((u[:-4] + '.cpp', len(re.findall(r'warning C\d+', tx)), len(re.findall(r'error C\d+', tx))))
    w('units.tsv', ['unit', 'warnings', 'errors'], ur)
    imp = collections.Counter(dm.get(s['target'], s['target']) for s in sites if s['kind'] == 'import' and s['caller'] in nodes)
    w('imports.tsv', ['imported_function', 'call_sites'], sorted(imp.items()))
    ndef = sum(1 for v in nodes.values() if v['definition'])
    print(f'{len(units)} units, {ndef} functions defined, {len(nodes) - ndef} declared virtual methods, '
          f'{len(edges)} edges, {len(over)} overrides, {len(unres)} unresolved', file=sys.stderr)


if __name__ == '__main__':
    main()
