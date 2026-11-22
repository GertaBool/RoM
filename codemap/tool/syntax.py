#!/usr/bin/env python3
"""Syntactic layer of the code map: functions, member variables and what touches them, read from the source.

usage: syntax.py <CvGameCoreDLL dir> [<XML dir> ...] [--out <dir>]   write the tables (default: codemap/map/)
  XML dirs in the game's order: the mod's, Beyond the Sword's, Civilization IV's (named mod, bts, civ4; or name=dir)

The compiler map (calls.tsv and the rest) gives exact calls at the commit it was built from. This layer is
read straight from the source with tree-sitter (a C++ parser; no compiler, no headers), so it can be rerun
on any checkout in seconds. It adds what the compiler map does not have:
  syntax_functions.tsv  every function definition: scope, name, file, first and last line
  (with --parser-members only; members_clang.py writes these four exactly, with clang:)
  fields.tsv            every data member declared in a class or struct: class, name, declared type
  field_access.tsv      every use of a data member inside a function: read, write, ref (&m_x passed on),
                        call (a method of the member is called, e.g. m_aUnits.push_back)
  field_strings.tsv     a member and a string literal passed to the same call, e.g.
                        pXML->GetChildXmlValByName(&m_iCost, "iCost"): the XML tag that fills the member
  defines_used.tsv      GC.getDefineINT("NAME") and the like: which function reads which global define
  xml_tags.tsv          for each XML element name: the XML files that hold it, their layer, whether the game
                        loads that file (a file of the mod shadows the base game's file of the same path),
                        and how often
  xml_classes.tsv       which XML file fills which info class (LoadGlobalClassInfo calls)
  xml_defines.tsv       for each <DefineName>: the XML file and layer that define it, and whether it is loaded
  syntax_calls.tsv      calls of names the compiler map (functions.tsv) does not define: the callers of code
                        added after the map's commit, matched by name
  syntax_parse.tsv      per file: parse errors tree-sitter reported (MSVC macros it could not read)

Limits: it is a parser, not a compiler. A member is matched by name: an unqualified name inside a method is the
member of that class (or a base) unless a parameter or local of the same name hides it; obj->m_x is the
member of whichever classes declare m_x (all of them listed when several do). #ifdef branches are all read.
The module is also imported by impact.py, which parses the checkout it is pointed at, at that moment.
"""
import collections, csv, os, re, sys

import tree_sitter as ts
import tree_sitter_cpp

LANG = ts.Language(tree_sitter_cpp.language())
PARSER = ts.Parser(LANG)
SRC_EXT = ('.cpp', '.h', '.inl')


def txt(n):
    return n.text.decode('latin-1')


# MSVC words tree-sitter does not know; blanked with spaces of the same length, so lines and columns stay
BLANK = re.compile(rb'\b(DllExport|__forceinline|__cdecl|__stdcall|__fastcall|_cdecl|PYTHON_API)\b')


def parse(data):
    return PARSER.parse(BLANK.sub(lambda m: b' ' * len(m.group(0)), data))


# ---------- functions ----------

def _declarator_name(d):
    """(scope, name) of a function_definition's declarator, or None."""
    while d is not None and d.type in ('pointer_declarator', 'reference_declarator', 'attributed_declarator'):
        d = d.child_by_field_name('declarator') or (d.named_children[-1] if d.named_children else None)
    if d is None or d.type != 'function_declarator':
        return None
    n = d.child_by_field_name('declarator')
    if n is None:
        return None
    if n.type == 'qualified_identifier':
        parts = []
        while n is not None and n.type == 'qualified_identifier':
            s = n.child_by_field_name('scope')
            if s is not None:
                parts.append(re.sub(r'<.*', '', txt(s)))
            n = n.child_by_field_name('name')
        return '::'.join(parts), (txt(n) if n is not None else '')
    return '', txt(n)


def _enclosing_classes(node):
    out = []
    p = node.parent
    while p is not None:
        if p.type in ('class_specifier', 'struct_specifier', 'union_specifier'):
            nm = p.child_by_field_name('name')
            if nm is not None:
                out.append(txt(nm))
        elif p.type == 'namespace_definition':
            nm = p.child_by_field_name('name')
            if nm is not None:
                out.append(txt(nm))
        p = p.parent
    return '::'.join(reversed(out))


def _walk(node, types):
    stack = [node]
    while stack:
        n = stack.pop()
        if n.type in types:
            yield n
        stack.extend(reversed(n.children))


# ---------- classes and fields ----------

def _field_names(decl):
    """Names declared by a field_declaration that is a data member (not a method)."""
    out = []
    for d in decl.children_by_field_name('declarator'):
        x = d
        while x is not None and x.type in ('pointer_declarator', 'reference_declarator', 'array_declarator',
                                            'init_declarator', 'bitfield_clause', 'attributed_declarator'):
            if x.type == 'function_declarator':
                break
            x = x.child_by_field_name('declarator') or (x.named_children[0] if x.named_children else None)
        if x is not None and x.type == 'field_identifier':
            out.append((txt(x), d))
    return out


def scan_classes(tree, fname):
    classes, bases, fields = {}, [], []
    for c in _walk(tree.root_node, ('class_specifier', 'struct_specifier', 'union_specifier')):
        nm = c.child_by_field_name('name')
        body = c.child_by_field_name('body')
        if nm is None or body is None:
            continue
        cname = re.sub(r'<.*', '', txt(nm))
        classes[cname] = (fname, c.start_point[0] + 1)
        for b in c.children:
            if b.type == 'base_class_clause':
                for t in b.named_children:
                    if t.type in ('type_identifier', 'qualified_identifier', 'template_type'):
                        bases.append((cname, re.sub(r'<.*', '', txt(t))))
        for fd in body.named_children:
            if fd.type != 'field_declaration':
                continue
            if any(x.type == 'function_declarator' for x in _walk(fd, ('function_declarator',))):
                continue
            ty = fd.child_by_field_name('type')
            static = any(ch.type == 'storage_class_specifier' and txt(ch) == 'static' for ch in fd.children)
            for name, d in _field_names(fd):
                prefix = txt(d)[:len(txt(d)) - len(txt(d).lstrip('*&'))]
                fields.append(dict(cls=cname, field=name, type=(txt(ty) if ty else '') + prefix,
                                   static=int(static), file=fname, line=d.start_point[0] + 1))
    return classes, bases, fields


# ---------- uses inside one function ----------

WRITE_OPS = ('=', '+=', '-=', '*=', '/=', '%=', '|=', '&=', '^=', '<<=', '>>=')


def _access_kind(node):
    """read / write / ref / call for an identifier node naming a member."""
    cur = node
    while True:
        p = cur.parent
        if p is None:
            return 'read'
        if p.type == 'parenthesized_expression' or (p.type == 'subscript_expression' and p.child_by_field_name('argument') == cur):
            cur = p; continue
        if p.type == 'field_expression' and p.child_by_field_name('argument') == cur:
            # m_x.y : a call of m_x.y(...) is a method call on the member; otherwise follow the access
            if p.parent is not None and p.parent.type == 'call_expression' and p.parent.child_by_field_name('function') == p:
                return 'call'
            cur = p; continue
        if p.type == 'pointer_expression':
            op = p.child_by_field_name('operator') or p.children[0]
            if txt(op) == '&':
                return 'ref'
            cur = p; continue
        if p.type == 'assignment_expression' and p.child_by_field_name('left') == cur:
            return 'write'
        if p.type == 'update_expression':
            return 'write'
        return 'read'


def _locals(fn):
    names = set()
    for d in _walk(fn, ('parameter_declaration', 'optional_parameter_declaration', 'declaration', 'init_declarator')):
        for i in _walk(d, ('identifier',)):
            par = i.parent
            if par is not None and par.type in ('init_declarator', 'parameter_declaration', 'declaration',
                                                 'pointer_declarator', 'reference_declarator', 'array_declarator',
                                                 'optional_parameter_declaration'):
                if par.child_by_field_name('declarator') == i or par.type in ('pointer_declarator', 'reference_declarator', 'array_declarator'):
                    names.add(txt(i))
    return names


DEFINE_CALL = re.compile(r'getDefine(INT|FLOAT|STRING)$')


def scan_function(fn, scope, name, fname, own_fields, field_owners, out):
    """Collect member uses, member+string pairs, define reads and call names of one function_definition."""
    body = fn.child_by_field_name('body')
    if body is None:
        return
    fid = (scope + '::' if scope else '') + name
    hidden = _locals(fn)
    for n in _walk(body, ('identifier', 'field_identifier')):
        nm = txt(n)
        if n.type == 'identifier':
            if nm in hidden or nm not in own_fields:
                continue
            p = n.parent
            if p is not None and p.type == 'qualified_identifier':
                continue
            owners = [own_fields[nm]]
            node = n
        else:
            p = n.parent
            if p is None or p.type != 'field_expression' or p.child_by_field_name('field') != n:
                continue
            arg = p.child_by_field_name('argument')
            if arg is not None and txt(arg) == 'this':
                owners = [own_fields[nm]] if nm in own_fields else sorted(field_owners.get(nm, ()))
            else:
                owners = sorted(field_owners.get(nm, ()))
            if not owners:
                continue
            node = p
        kind = _access_kind(node)
        for o in owners:
            out['access'].append(dict(function=fid, cls=o, field=nm, kind=kind, file=fname, line=n.start_point[0] + 1))
    for c in _walk(body, ('call_expression',)):
        f = c.child_by_field_name('function')
        args = c.child_by_field_name('arguments')
        if f is None:
            continue
        callee = txt(f.child_by_field_name('field')) if f.type == 'field_expression' and f.child_by_field_name('field') else txt(f)
        form = 'self' if f.type == 'identifier' else ('qualified' if f.type == 'qualified_identifier' else 'member')
        out['calls'].append(dict(function=fid, callee=callee, form=form, file=fname, line=c.start_point[0] + 1))
        if args is None:
            continue
        strs = [txt(a)[1:-1] for a in args.named_children if a.type == 'string_literal']
        if DEFINE_CALL.search(callee) and strs:
            out['defines'].append(dict(function=fid, define=strs[0], kind=DEFINE_CALL.search(callee).group(1),
                                       file=fname, line=c.start_point[0] + 1))
            continue
        if not strs:
            continue
        for a in args.named_children:
            for i in _walk(a, ('identifier', 'field_identifier')):
                nm = txt(i)
                if (i.type == 'identifier' and nm in own_fields and nm not in hidden) or \
                   (i.type == 'field_identifier' and nm in field_owners):
                    o = own_fields.get(nm) or ','.join(sorted(field_owners[nm]))
                    out['strings'].append(dict(function=fid, cls=o, field=nm, string=strs[0], call=callee,
                                               file=fname, line=c.start_point[0] + 1))
                    break
            else:
                continue
            break


# ---------- whole tree ----------

def read_sources(src):
    files = {}
    for f in sorted(os.listdir(src)):
        if f.endswith(SRC_EXT):
            with open(os.path.join(src, f), 'rb') as h:
                files[f] = h.read()
    return files


def scan(files):
    """files: {name: bytes}. Returns dict of row lists."""
    trees = {f: parse(d) for f, d in files.items()}
    classes, bases, fields, errors = {}, collections.defaultdict(set), [], []
    for f, t in trees.items():
        c, b, fl = scan_classes(t, f)
        classes.update(c)
        for x, y in b:
            bases[x].add(y)
        fields += fl
        errors.append(dict(file=f, errors=sum(1 for _ in _walk(t.root_node, ('ERROR',)))))
    by_class = collections.defaultdict(dict)
    owners = collections.defaultdict(set)
    for r in fields:
        by_class[r['cls']][r['field']] = r['cls']
        owners[r['field']].add(r['cls'])

    def visible(cls, seen=None):   # members of cls and its bases, nearest wins
        seen = set() if seen is None else seen
        if cls in seen:
            return {}
        seen.add(cls)
        out = {}
        for b in bases.get(cls, ()):
            out.update(visible(b, seen))
        out.update(by_class.get(cls, {}))
        return out

    cache = {}
    out = dict(functions=[], access=[], strings=[], defines=[], calls=[])
    for f, t in trees.items():
        for fn in _walk(t.root_node, ('function_definition',)):
            r = _declarator_name(fn.child_by_field_name('declarator'))
            if r is None:
                continue
            scope, name = r
            if not scope:
                scope = _enclosing_classes(fn)
            cls = scope.split('::')[-1] if scope else ''
            if cls not in cache:
                cache[cls] = visible(cls) if cls else {}
            out['functions'].append(dict(scope=scope, name=name, file=f, line=fn.start_point[0] + 1, end=fn.end_point[0] + 1))
            scan_function(fn, scope, name, f, cache[cls], owners, out)
    out.update(classes=classes, bases=bases, fields=fields, errors=errors)
    return out


def scan_loaders(files):
    """Which XML file fills which info class: LoadGlobalClassInfo(GC.getTechInfo(), "CIV4TechInfos",
    "Technologies", ...) with std::vector<CvTechInfo*>& getTechInfo() from the headers, and
    ARTFILEMGR.getUnitArtInfo() for CvArtInfoUnit (ART_INFO_DECL(Unit))."""
    vec = {}
    for f, d in files.items():
        if f.endswith('.h'):
            t = d.decode('latin-1')
            for m in re.finditer(r'std::vector<\s*(\w+)\s*\*\s*>\s*&\s*(get\w+)\s*\(', t):
                vec[m.group(2)] = m.group(1)
            for m in re.finditer(r'ART_INFO_DECL\((\w+)\)', t):
                vec['get%sArtInfo' % m.group(1)] = 'CvArtInfo' + m.group(1)
    rows = []
    for f, d in sorted(files.items()):
        if not f.endswith('.cpp'):
            continue
        t = d.decode('latin-1')
        for m in re.finditer(r'LoadGlobalClassInfo\(\s*[\w.]*?(get\w+)\(\)\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"', t):
            if t.rfind('//', t.rfind('\n', 0, m.start()), m.start()) != -1:
                continue
            rows.append(dict(cls=vec.get(m.group(1), ''), getter=m.group(1), file='%s/%s.xml' % (m.group(3), m.group(2)),
                             xpath=m.group(4), src=f, line=t.count('\n', 0, m.start()) + 1))
    return rows


def scan_xml(layers):
    """layers: [(name, dir)] in the order the game looks (the mod's XML first). The game loads a file from the
    first layer that has its path; the same path in a later layer is shadowed (loaded = 0)."""
    tags = collections.defaultdict(collections.Counter)
    defines = []
    seen = set()
    tag_re = re.compile(rb'<([A-Za-z_][\w.:-]*)[\s>/]')
    def_re = re.compile(rb'<DefineName>\s*([^<\s]+)\s*</DefineName>')
    for layer, xml_dir in layers:
        mine = set()
        for root, _, fs in os.walk(xml_dir):
            for f in fs:
                if not f.lower().endswith('.xml'):
                    continue
                p = os.path.join(root, f)
                rel = os.path.relpath(p, xml_dir).replace(os.sep, '/')
                loaded = int(rel.lower() not in seen)
                mine.add(rel.lower())
                with open(p, 'rb') as h:
                    d = h.read()
                for m in tag_re.finditer(d):
                    tags[m.group(1).decode('latin-1')][(rel, layer, loaded)] += 1
                for m in def_re.finditer(d):
                    defines.append(dict(define=m.group(1).decode('latin-1'), file=rel, layer=layer, loaded=loaded))
        seen |= mine
    rows = [dict(tag=t, file=f, layer=l, loaded=ld, count=n) for t in sorted(tags)
            for (f, l, ld), n in sorted(tags[t].items(), key=lambda kv: (-kv[0][2], kv[0][0]))]
    return rows, defines


def write(path, rows, cols):
    with open(path, 'w', encoding='utf-8', newline='') as h:
        w = csv.writer(h, delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='\\')
        w.writerow(cols)
        for r in rows:
            w.writerow([str(r[c]).replace('\t', ' ').replace('\n', ' ') for c in cols])


def main(argv):
    args = [a for a in argv if not a.startswith('--')]   # --parser-members: also write the parser's member tables
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'map')
    if '--out' in argv:
        out_dir = argv[argv.index('--out') + 1]
        args.remove(out_dir)
    if not args:
        sys.exit(__doc__)
    s = scan(read_sources(args[0]))
    write(os.path.join(out_dir, 'syntax_functions.tsv'), s['functions'], ['scope', 'name', 'file', 'line', 'end'])
    if '--parser-members' in argv:   # the member tables come from members_clang.py; this is the parser's fallback
        write(os.path.join(out_dir, 'fields.tsv'), sorted(s['fields'], key=lambda r: (r['cls'], r['line'])),
              ['cls', 'field', 'type', 'static', 'file', 'line'])
        write(os.path.join(out_dir, 'field_access.tsv'), s['access'], ['function', 'cls', 'field', 'kind', 'file', 'line'])
        write(os.path.join(out_dir, 'field_strings.tsv'), s['strings'], ['function', 'cls', 'field', 'string', 'call', 'file', 'line'])
        write(os.path.join(out_dir, 'defines_used.tsv'), s['defines'], ['function', 'define', 'kind', 'file', 'line'])
    write(os.path.join(out_dir, 'syntax_parse.tsv'), s['errors'], ['file', 'errors'])
    write(os.path.join(out_dir, 'xml_classes.tsv'), scan_loaders(read_sources(args[0])),
          ['cls', 'getter', 'file', 'xpath', 'src', 'line'])
    # calls of names the compiler map does not define (functions newer than the map): impact.py follows them by name
    known = set()
    fpath = os.path.join(out_dir, 'functions.tsv')
    if os.path.exists(fpath):
        with open(fpath, encoding='utf-8') as h:
            known = {r['name'] for r in csv.DictReader(h, delimiter='\t', quoting=csv.QUOTE_NONE)}
    write(os.path.join(out_dir, 'syntax_calls.tsv'), [c for c in s['calls'] if c['callee'].split('::')[-1] not in known],
          ['function', 'callee', 'form', 'file', 'line'])
    import subprocess
    try:
        rev = subprocess.run(['git', '-C', args[0], 'log', '-1', '--format=%h %cs %D'], capture_output=True,
                             text=True, check=True).stdout.strip()
    except Exception:
        rev = 'unknown'
    with open(os.path.join(out_dir, 'syntax_meta.tsv'), 'w') as h:
        h.write('source\nSyntactic layer (members, XML tags, defines) read from the source at %s; callers from the '
                'compiler map at the commit named in skeleton.md\n' % rev)
    if len(args) > 1:
        names = ['mod', 'bts', 'civ4']
        layers = [(a.split('=', 1) if '=' in a else (names[k] if k < 3 else 'base%d' % k, a)) for k, a in enumerate(args[1:])]
        tags, defs = scan_xml(layers)
        write(os.path.join(out_dir, 'xml_tags.tsv'), tags, ['tag', 'file', 'layer', 'loaded', 'count'])
        write(os.path.join(out_dir, 'xml_defines.tsv'), defs, ['define', 'file', 'layer', 'loaded'])
    print('functions %d, fields %d, member uses %d, member+string %d, define reads %d, files with parse errors %d'
          % (len(s['functions']), len(s['fields']), len(s['access']), len(s['strings']), len(s['defines']),
             sum(1 for e in s['errors'] if e['errors'])))


if __name__ == '__main__':
    main(sys.argv[1:])
