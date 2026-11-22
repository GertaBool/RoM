#!/usr/bin/env python3
"""Member uses, XML fills and define reads, read by clang with full semantic analysis (not by name).

usage: members_clang.py <mirror dir> <BTS SDK CvGameCoreDLL dir> [--jobs N] [--out <map dir>]
  mirror dir: toolchain/clang-gate/mirror.sh <Assets/CvGameCoreDLL> <dir> (the source with case-fixed includes)
  BTS SDK dir: the folder holding Boost-1.32.0/ and Python24/ (the SDK tarball of the GitLab repository)

Every translation unit is parsed as toolchain/clang-gate/check.sh parses it (MSVC compatibility, the release
defines, the SDK's Boost and Python headers), except that templates are parsed where they are written, so the
bodies of template classes (FFreeListArray, CLinkList ...) are read too. Run toolchain/clang-gate/forscope-pass.sh
on the mirror first: it emulates MSVC 2003's for-loop scope without moving any line. Each expression naming a data member (clang MemberRefExpr) gives
the member's own class, from its declaration, so obj->m_x is tied to exactly one class. Its use:
  write  left side of =, +=, ... or operand of ++/--; also the object of a non-const operator= / operator+= ...
  ref    its address taken (&m_x), or passed to a non-const reference parameter
  call   a non-const method called on it (m_aUnits.push_back)
  read   anything else, including const methods (m_aUnits.size())
writes:
  fields.tsv         cls, field, type, static, file, line           (every data member declared; replaces the parser's)
  field_access.tsv   function, cls, field, kind, file, line         (replaces the parser's table)
  field_strings.tsv  function, cls, field, string, call, file, line (a member and a string literal in one call)
  defines_used.tsv   function, define, kind, file, line             (getDefineINT("NAME") and the like)
  function_returns.tsv  function, returns: the declared return type of every function and method (for py_resolve.py)
  members_clang.tsv  per unit: diagnostics clang reported (errors, warnings ignored)
The function is the one whose body holds the expression, named Scope::name as in functions.tsv.
"""
import collections, csv, multiprocessing, os, re, sys

import clang.cindex as ci

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, '..', '..', 'toolchain', 'clang-gate')
K = ci.CursorKind
FUNCS = {K.FUNCTION_DECL, K.CXX_METHOD, K.CONSTRUCTOR, K.DESTRUCTOR, K.FUNCTION_TEMPLATE, K.CONVERSION_FUNCTION}
SCOPES = {K.CLASS_DECL, K.STRUCT_DECL, K.UNION_DECL, K.NAMESPACE, K.CLASS_TEMPLATE, K.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION}
ASSIGN = {'=', '+=', '-=', '*=', '/=', '%=', '|=', '&=', '^=', '<<=', '>>='}
DEFINE_CALL = re.compile(r'getDefine(INT|FLOAT|STRING)$')


RESOURCE = os.popen('clang -print-resource-dir 2>/dev/null').read().strip()   # clang's own headers (stddef.h ...)


def args(mirror, sdk):
    return (['-resource-dir', RESOURCE] if RESOURCE else []) + ['-x', 'c++', '-std=gnu++98', '-fms-extensions', '-fms-compatibility',
            '-Wno-everything', '-ferror-limit=0', '-I' + GATE, '-I' + mirror,
            '-isystem', os.path.join(sdk, 'Boost-1.32.0', 'include'), '-isystem', os.path.join(sdk, 'Python24', 'include'),
            '-DWIN32', '-D_WINDOWS', '-D_USRDLL', '-DCVGAMECOREDLL_EXPORTS', '-DNDEBUG', '-DFINAL_RELEASE']


def qual(c):
    """Scope of a declaration: enclosing classes and namespaces, as functions.tsv writes them."""
    parts = []
    p = c.semantic_parent
    while p is not None and p.kind != K.TRANSLATION_UNIT:
        if p.kind in SCOPES:
            parts.append(p.spelling or "`anonymous namespace'")
        p = p.semantic_parent
    return '::'.join(reversed(parts))


def fname(f):
    s = qual(f)
    return (s + '::' if s else '') + f.spelling


def toks(c):
    return [t.spelling for t in c.get_tokens()]


def binop(c, kids):
    """The operator of a BINARY_OPERATOR: the token between its two operands."""
    if len(kids) != 2:
        return None
    end = kids[0].extent.end
    for t in c.get_tokens():
        if (t.location.line, t.location.column) >= (end.line, end.column):
            return t.spelling
    return None


def unop(c):
    ts = toks(c)
    if not ts:
        return None
    if ts[0] in ('++', '--', '&', '*', '!', '-', '~', '+'):
        return ts[0]
    if ts[-1] in ('++', '--'):
        return ts[-1] + 'post'
    return None


def access(stack):
    """Kind of use of the member expression at stack[-1]; stack holds (cursor, children) from the root."""
    k = len(stack) - 1
    node = stack[k][0]
    while k > 0:
        parent, kids = stack[k - 1]
        pk = parent.kind
        first = kids and kids[0] == node
        if pk in (K.PAREN_EXPR, K.UNEXPOSED_EXPR, K.CSTYLE_CAST_EXPR, K.CXX_FUNCTIONAL_CAST_EXPR):
            node, k = parent, k - 1
            continue
        if pk == K.ARRAY_SUBSCRIPT_EXPR:
            if first:
                node, k = parent, k - 1
                continue
            return 'read'
        if pk == K.MEMBER_REF_EXPR:      # m_x.y: follow the access of m_x.y; m_x.f(): see the call above
            ref = parent.referenced
            if ref is not None and ref.kind in (K.CXX_METHOD, K.CONVERSION_FUNCTION, K.FUNCTION_TEMPLATE):
                return 'read' if ref.kind == K.CXX_METHOD and ref.is_const_method() else 'call'
            node, k = parent, k - 1
            continue
        if pk == K.UNARY_OPERATOR:
            op = unop(parent)
            if op in ('++', '--', '++post', '--post'):
                return 'write'
            if op == '&':
                return 'ref'
            if op == '*':
                node, k = parent, k - 1
                continue
            return 'read'
        if pk == K.BINARY_OPERATOR:
            return 'write' if first and binop(parent, kids) in ASSIGN else 'read'
        if pk == K.COMPOUND_ASSIGNMENT_OPERATOR:
            return 'write' if first else 'read'
        if pk == K.CALL_EXPR:
            ref = parent.referenced
            if ref is not None and ref.spelling.startswith('operator') and first is False and len(kids) > 1 and kids[1] == node:
                pass
            if ref is not None and ref.spelling.startswith('operator') and node in kids[:2]:
                op = ref.spelling[8:].strip()
                obj_first = kids[0] == node or (len(kids) > 1 and kids[1] == node and kids[0].kind == K.UNEXPOSED_EXPR
                                                and kids[0].spelling.startswith('operator'))
                if op in ASSIGN and obj_first:
                    return 'write'
                if op in ('++', '--') and obj_first:
                    return 'write'
                if op in ('[]', '->', '*') and obj_first:
                    node, k = parent, k - 1
                    continue
            if ref is not None and ref.kind in FUNCS | {K.CXX_METHOD}:
                # an argument: by non-const reference is a ref
                pos = [x for x in kids[1:]]
                if node in pos:
                    i = pos.index(node)
                    params = list(ref.get_arguments())
                    if i < len(params):
                        t = params[i].type
                        if t.kind == ci.TypeKind.LVALUEREFERENCE and not t.get_pointee().is_const_qualified():
                            return 'ref'
            return 'read'
        return 'read'
    return 'read'


def string_value(c):
    for t in c.get_tokens():
        s = t.spelling
        if s.startswith('"') or s.startswith('L"'):
            return s[s.index('"') + 1:-1]
    return None


def scan_unit(job):
    mirror, sdk, f = job
    idx = ci.Index.create()
    tu = idx.parse(os.path.join(mirror, f), args=args(mirror, sdk),
                   options=ci.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD * 0)
    errors = sum(1 for d in tu.diagnostics if d.severity >= ci.Diagnostic.Error)
    acc, strs, defs, decls, rets = set(), set(), set(), set(), set()
    mir = os.path.realpath(mirror)

    def mine(c):
        loc = c.location
        return loc.file is not None and os.path.dirname(os.path.realpath(loc.file.name)) == mir

    def walk(c, stack, fn):
        kids = list(c.get_children())
        stack.append((c, kids))
        if c.kind in FUNCS and c.is_definition():
            fn = c
        if c.kind in (K.CXX_METHOD, K.FUNCTION_DECL) and mine(c):
            rets.add((fname(c), c.result_type.spelling))
        if c.kind == K.FIELD_DECL and mine(c):
            decls.add((qual(c), c.spelling, c.type.spelling, 0, os.path.basename(c.location.file.name), c.location.line))
        elif c.kind == K.VAR_DECL and mine(c) and c.semantic_parent is not None and c.semantic_parent.kind in (K.CLASS_DECL, K.STRUCT_DECL) \
                and c.lexical_parent is not None and c.lexical_parent.kind in (K.CLASS_DECL, K.STRUCT_DECL):
            decls.add((qual(c), c.spelling, c.type.spelling, 1, os.path.basename(c.location.file.name), c.location.line))
        if fn is not None and mine(c):
            if c.kind == K.MEMBER_REF_EXPR:
                ref = c.referenced
                if ref is not None and ref.kind == K.FIELD_DECL:
                    cls = qual(ref)
                    acc.add((fname(fn), cls, ref.spelling, access(stack), os.path.basename(c.location.file.name), c.location.line))
            elif c.kind == K.DECL_REF_EXPR:
                ref = c.referenced
                if ref is not None and ref.kind == K.VAR_DECL and ref.semantic_parent is not None and \
                        ref.semantic_parent.kind in (K.CLASS_DECL, K.STRUCT_DECL):   # static data member
                    acc.add((fname(fn), qual(ref), ref.spelling, access(stack), os.path.basename(c.location.file.name), c.location.line))
            elif c.kind == K.CALL_EXPR:
                callee = c.spelling
                lits = [string_value(x) for x in c.walk_preorder() if x.kind == K.STRING_LITERAL]
                lits = [x for x in lits if x is not None]
                if lits:
                    line, file = c.location.line, os.path.basename(c.location.file.name)
                    m = DEFINE_CALL.search(callee or '')
                    if m:
                        defs.add((fname(fn), lits[0], m.group(1), file, line))
                    else:
                        for a in kids[1:] if kids else []:
                            for x in a.walk_preorder():
                                if x.kind == K.MEMBER_REF_EXPR and x.referenced is not None and x.referenced.kind == K.FIELD_DECL:
                                    strs.add((fname(fn), qual(x.referenced), x.referenced.spelling, lits[0], callee, file, line))
                                    break
                            else:
                                continue
                            break
        for k in kids:
            walk(k, stack, fn)
        stack.pop()

    sys.setrecursionlimit(100000)
    for c in tu.cursor.get_children():
        if mine(c):
            walk(c, [], None)
    return f, errors, acc, strs, defs, decls, rets


def write(path, header, rows):
    with open(path, 'w', encoding='utf-8') as o:
        o.write('\t'.join(header) + '\n')
        for r in rows:
            o.write('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in r) + '\n')


def main(argv):
    jobs = 4
    out = os.path.join(HERE, '..', 'map')
    if '--jobs' in argv:
        k = argv.index('--jobs'); jobs = int(argv[k + 1]); del argv[k:k + 2]
    if '--out' in argv:
        k = argv.index('--out'); out = argv[k + 1]; del argv[k:k + 2]
    if len(argv) < 2:
        sys.exit(__doc__)
    mirror, sdk = os.path.abspath(argv[0]), os.path.abspath(argv[1])
    units = sorted(f for f in os.listdir(mirror) if f.endswith('.cpp') and f != '_precompile.cpp')
    acc, strs, defs, decls, rets, diag = set(), set(), set(), set(), set(), []
    with multiprocessing.Pool(jobs) as pool:
        for f, errors, a, s, d, dc, rt in pool.imap_unordered(scan_unit, [(mirror, sdk, f) for f in units]):
            acc |= a; strs |= s; defs |= d; decls |= dc; rets |= rt
            diag.append((f, errors))
            print('%-40s errors %d, member uses %d' % (f, errors, len(a)), file=sys.stderr)
    write(os.path.join(out, 'field_access.tsv'), ['function', 'cls', 'field', 'kind', 'file', 'line'], sorted(acc))
    write(os.path.join(out, 'field_strings.tsv'), ['function', 'cls', 'field', 'string', 'call', 'file', 'line'], sorted(strs))
    write(os.path.join(out, 'defines_used.tsv'), ['function', 'define', 'kind', 'file', 'line'], sorted(defs))
    write(os.path.join(out, 'fields.tsv'), ['cls', 'field', 'type', 'static', 'file', 'line'], sorted(decls))
    write(os.path.join(out, 'function_returns.tsv'), ['function', 'returns'], sorted(rets))
    write(os.path.join(out, 'members_clang.tsv'), ['unit', 'errors'], sorted(diag))
    print('%d units (%d with errors), %d member uses, %d member+string, %d define reads'
          % (len(units), sum(1 for d in diag if d[1]), len(acc), len(strs), len(defs)))


if __name__ == '__main__':
    main(sys.argv[1:])
