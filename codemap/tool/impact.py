#!/usr/bin/env python3
"""What a change reaches, across the whole map: C++ and Python functions, member variables, XML, defines.

usage: impact.py diff <rise-of-mankind checkout> <base> [<head>]   a change between two commits (head: HEAD):
                                                                   C++, Python and XML files
       impact.py func <Scope::name | regex>                         C++ function(s)
       impact.py py <module path>[:<name>]                          Python function(s), e.g. CvEventManager.py:CvEventManager.onCityBuilt
       impact.py field <Class::m_x | m_x>                            member variable(s)
       impact.py tag <XML element>                                  an XML tag: the members it fills, and on
       impact.py define <NAME>                                      a global define
       impact.py file <file.cpp | module.py | XML path>             every function of a file; for XML, every tag in it
options: --depth N    levels listed by name (default 3; all levels are always counted)
         --src DIR    CvGameCoreDLL dir to read the syntactic layer from live (default: codemap/map tables)

The reach follows the links of graph.py: C++ callers, Python callers of a C++ function, Python callers of a
Python function, C++ code calling a Python function, the DLL event a Python handler serves, readers of a member,
members an XML tag fills, readers of a define. Members a changed function writes are followed too (for diff: the
members written on changed lines). Every listed node shows the node it was reached from and the link.
"""
import collections, csv, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
M = os.path.join(HERE, '..', 'map')
DLL, PY, XML = 'Assets/CvGameCoreDLL', 'Assets/Python', 'Assets/XML'


def read(n):
    p = os.path.join(M, n)
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


class Layer:
    """The syntactic layer: stored tables, or a live scan of a source dir (or of {file: bytes})."""

    def __init__(self, src=None, files=None):
        if src or files:
            import syntax
            s = syntax.scan(files if files is not None else syntax.read_sources(src))
            self.functions, self.fields, self.access = s['functions'], s['fields'], s['access']
            self.strings, self.defines, self.calls = s['strings'], s['defines'], s['calls']
        else:
            self.functions = read('syntax_functions.tsv')
            self.fields, self.access = read('fields.tsv'), read('field_access.tsv')
            self.strings, self.defines, self.calls = read('field_strings.tsv'), read('defines_used.tsv'), read('syntax_calls.tsv')
        for r in self.functions:
            r['line'], r['end'] = int(r['line']), int(r['end'])
        self.call_rows = collections.defaultdict(list)
        for c in self.calls:
            self.call_rows[c['callee'].split('::')[-1]].append(c)

    def callers_by_name(self, fid):
        """Callers of Scope::name seen by the scan: an unqualified call only from the same scope, a qualified
        call only when its scope matches, a call through an object (x.f(), x->f()) from anywhere."""
        scope, _, nm = fid.rpartition('::')
        res = set()
        for c in self.call_rows.get(nm, ()):
            if c.get('form') == 'self' and c['function'].rpartition('::')[0] != scope:
                continue
            if c.get('form') == 'qualified' and c['callee'].rpartition('::')[0].split('::')[-1] != scope.split('::')[-1]:
                continue
            if c['function'] != fid:
                res.add(c['function'])
        return res


def graph(layer):
    import graph as G
    g = G.Graph(layer)
    # functions newer than the compiler map: callers by name
    for nid in [n for n, i in g.info.items() if i['kind'] == 'new']:
        for f in layer.callers_by_name(g.info[nid]['label']):
            g.dep[nid].setdefault(g.cnode(f), 'call (name match)')
    return g


# ---------- the report ----------

KINDS = [('member', 'member variables'), ('cpp', 'C++ functions'), ('new', 'C++ functions newer than the map'),
         ('py', 'Python functions'), ('tag', 'XML tags'), ('define', 'defines')]


def label(g, n):
    i = g.info[n]
    if i['kind'] in ('cpp', 'new', 'py'):
        return '%s  (%s:%s)' % (i['label'] if i['kind'] != 'py' else i['label'].split(' ', 1)[1], i['file'], i['line'])
    return i['label']


def xml_where(g, tag):
    rows = g.xml.get(tag, [])
    loaded = ['%s [%s]' % (r['file'], r['layer']) for r in rows if r['loaded'] == '1']
    shadow = sum(1 for r in rows if r['loaded'] != '1')
    return ', '.join(loaded[:8]) + (' ...' if len(loaded) > 8 else '') + \
        ('; %d shadowed copies in the base game' % shadow if shadow else '') if rows else 'in no XML file of the scan'


def member_line(g, m):
    i = g.info[m]
    bits = [i['type']]
    if i['saved']:
        bits.append('serialized in read/write(FDataStreamBase*): a change of type or order changes the stream (save) format')
    for t in sorted(i['tags']):
        rows, known = i.get('xml', {}).get(t, ([], False))
        if known:
            ld = ['%s [%s]' % (r['file'], r['layer']) for r in rows if r['loaded'] == '1']
            sh = ['%s [%s]' % (r['file'], r['layer']) for r in rows if r['loaded'] != '1']
            bits.append('filled from XML <%s> in %s%s' % (t, ', '.join(ld) or 'no loaded file holding the tag',
                                                        (' (shadowed: %s)' % ', '.join(sh)) if sh else ''))
        else:
            bits.append('filled from XML <%s> (loader of the class not found; files holding the tag: %s)' % (t, xml_where(g, t)))
    return '- %s (%s:%s): %s' % (i['label'], i['file'], i['line'], '; '.join(bits))


def report(g, seeds, out, depth, follow_writes=True, title=None):
    seeds = [s for s in dict.fromkeys(seeds) if s in g.info]
    if title:
        out.append(title)
    if not seeds:
        out.append('\nNothing in the map to start from.')
        return {}
    lv = g.reach(seeds, follow_writes)
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for n, (d, via, link) in lv.items():
        by[g.info[n]['kind']][d].append(n)
    out.append('\n## Reach\n')
    out.append('| | start | reached | per level |')
    out.append('|---|---|---|---|')
    for k, name in KINDS:
        if k in by:
            lvls = by[k]
            out.append('| %s | %d | %d | %s |' % (name, len(lvls.get(0, [])), sum(len(v) for d, v in lvls.items() if d),
                                                 ', '.join('%d: %d' % (d, len(lvls[d])) for d in sorted(lvls) if d)))
    nodes = list(lv)
    ex = [n for n in nodes if g.info[n].get('exported')]
    pb = [n for n in nodes if g.info[n].get('bound')]
    ev = [n for n in nodes if g.info[n].get('events')]
    mods = collections.Counter(g.info[n]['file'] for n in nodes if g.info[n]['kind'] == 'py')
    cfiles = collections.Counter(g.info[n]['file'] for n in nodes if g.info[n]['kind'] == 'cpp')
    out.append('\n- C++ functions the exe calls (exported): %d%s' % (len(ex), (': ' + ', '.join(sorted(g.info[n]['label'] for n in ex)[:12]) + (' ...' if len(ex) > 12 else '')) if ex else ''))
    out.append('- C++ functions bound for Python: %d' % len(pb))
    out.append('- Python event handlers: %d%s' % (len(ev), (': ' + ', '.join(sorted('%s (%s)' % (g.info[n]['label'].split(' ', 1)[1], ','.join(sorted(g.info[n]['events']))) for n in ev)[:12])) if ev else ''))
    out.append('- C++ files: ' + (', '.join('%s %d' % kv for kv in cfiles.most_common(25)) or 'none'))
    out.append('- Python modules: ' + (', '.join('%s %d' % kv for kv in mods.most_common(25)) or 'none'))
    mem = sorted((n for n in nodes if g.info[n]['kind'] == 'member'), key=lambda n: (lv[n][0], n))
    if mem:
        out.append('\n## Member variables (%d)\n' % len(mem))
        for n in mem[:80]:
            d, via, link = lv[n]
            out.append(member_line(g, n) + ('' if d == 0 else '  [level %d, %s %s]' % (d, link, g.info[via]['label'])))
        if len(mem) > 80:
            out.append('- ... %d more' % (len(mem) - 80))
    tags = [n for n in nodes if g.info[n]['kind'] in ('tag', 'define')]
    if tags:
        out.append('\n## XML tags and defines\n')
        for n in sorted(tags):
            i = g.info[n]
            where = xml_where(g, i['label'][1:-1]) if i['kind'] == 'tag' else \
                ', '.join('%s [%s]' % (r['file'], r['layer']) for r in i['files'] if r['loaded'] == '1') or 'in no XML file of the scan'
            out.append('- %s %s: %s' % (i['kind'], i['label'], where))
    for k, name in (('cpp', 'C++ functions'), ('new', 'C++ functions newer than the map'), ('py', 'Python functions')):
        if k not in by:
            continue
        out.append('\n## %s, level by level\n' % name)
        for d in sorted(by[k]):
            if d > depth:
                out.append('\n(levels above %d: %d more)' % (depth, sum(len(v) for dd, v in by[k].items() if dd > depth)))
                break
            ns = sorted(by[k][d], key=lambda n: g.info[n]['label'])
            out.append('\n### level %d (%d)\n' % (d, len(ns)))
            for n in ns[:50]:
                _, via, link = lv[n]
                out.append('- %s%s' % (label(g, n), '' if via is None else '  <- %s %s' % (link, g.info[via]['label'])))
            if len(ns) > 50:
                out.append('- ... %d more' % (len(ns) - 50))
    if len(seeds) > 1:
        out.append('\n## Reach per start node\n')
        out.append('| start | reached | C++ | Python | members |')
        out.append('|---|---|---|---|---|')
        rows = []
        for s in seeds:
            r = g.reach([s], follow_writes)
            c = collections.Counter(g.info[n]['kind'] for n in r if n != s)
            rows.append((len(r) - 1, g.info[s]['label'], c['cpp'] + c['new'], c['py'], c['member']))
        for n, lab, c, p, m in sorted(rows, reverse=True)[:60]:
            out.append('| %s | %d | %d | %d | %d |' % (lab, n, c, p, m))
    return lv


# ---------- Python source: function extents ----------

DEF = re.compile(r'^(\s*)(def|class)\s+(\w+)')


def py_extents(text):
    """[(qualname, first, last)] of the defs and classes of a Python 2 file, by indentation."""
    lines = text.split('\n')
    out, stack = [], []
    for k, line in enumerate(lines, 1):
        s = line.expandtabs(4)
        if not s.strip() or s.lstrip().startswith('#'):
            continue
        ind = len(s) - len(s.lstrip())
        while stack and ind <= stack[-1][0]:
            q = stack.pop()
            out.append((q[1], q[2], q[3]))
        m = DEF.match(s)
        if m:
            q = '.'.join([x[1].split('.')[-1] for x in stack] + [m.group(3)]) if stack else m.group(3)
            stack.append([ind, q, k, k])
        for x in stack:
            x[3] = k
    out += [(q[1], q[2], q[3]) for q in stack]
    return out


# ---------- diff ----------

def git(repo, *a):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True, check=True).stdout


def hunks(repo, base, head, root):
    """{path under root: (head_lines, base_lines)} changed lines per file."""
    d = git(repo, 'diff', '-U0', base, head, '--', root).decode('latin-1')
    out = collections.defaultdict(lambda: (set(), set()))
    f = None
    for line in d.split('\n'):
        if line.startswith('--- ') and line[4:] != '/dev/null':
            f = line[6:][len(root) + 1:]
        elif line.startswith('+++ ') and line[4:] != '/dev/null':
            f = line[6:][len(root) + 1:]
        elif line.startswith('@@') and f:
            m = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            b0, bn, h0, hn = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)
            out[f][0].update(range(h0, h0 + hn))
            out[f][1].update(range(b0, b0 + bn))
    return out


def files_at(repo, rev):
    names = git(repo, 'ls-tree', '--name-only', rev, DLL + '/').decode().split()
    import syntax
    return {os.path.basename(p): git(repo, 'show', '%s:%s' % (rev, p)) for p in names if p.endswith(syntax.SRC_EXT)}


def show(repo, rev, path):
    try:
        return git(repo, 'show', '%s:%s' % (rev, path)).decode('latin-1')
    except subprocess.CalledProcessError:
        return ''


def fid(f):
    return (f['scope'] + '::' if f['scope'] else '') + f['name']


def diff(repo, base, head, depth):
    out = []
    hb = git(repo, 'rev-parse', '--short=12', base).decode().strip()
    hh = git(repo, 'rev-parse', '--short=12', head).decode().strip()
    out.append('# Impact of %s..%s\n' % (hb, hh))
    out.append('Commits:\n\n' + git(repo, 'log', '--format=- %h %ad %s', '--date=short', '%s..%s' % (base, head)).decode())
    out.append('```\n' + git(repo, 'diff', '--stat', base, head).decode() + '```')
    LH, LB = Layer(files=files_at(repo, head)), Layer(files=files_at(repo, base))
    g = graph(LH)
    seeds = []
    # C++
    H = {os.path.basename(k): v for k, v in hunks(repo, base, head, DLL).items()}

    def touched(L, side):
        res = collections.OrderedDict()
        for fn in L.functions:
            lines = H.get(fn['file'], (set(), set()))[side]
            if lines and any(fn['line'] <= x <= fn['end'] for x in lines):
                res[fid(fn)] = fn
        return res

    th, tb = touched(LH, 0), touched(LB, 1)
    hn, bn = {fid(f) for f in LH.functions}, {fid(f) for f in LB.functions}
    added, removed, changed = [f for f in th if f not in bn], [f for f in tb if f not in hn], [f for f in th if f in bn]
    out.append('\n## C++ functions\n')
    out.append('- changed: %d; added: %d; removed: %d' % (len(changed), len(added), len(removed)))
    for lab, lst, L in (('changed', changed, th), ('added', added, th), ('removed', removed, tb)):
        for f in lst:
            out.append('  - %s %s  (%s:%d-%d)' % (lab, f, L[f]['file'], L[f]['line'], L[f]['end']))
    for f in changed + added:
        seeds += g.cnodes(f)
    fh = {(r['cls'], r['field']): r for r in LH.fields}
    fb = {(r['cls'], r['field']): r for r in LB.fields}
    decl = []
    for k in sorted(set(fh) | set(fb)):
        a, b = fh.get(k), fb.get(k)
        if a and not b:
            decl.append(('added', k, a['type']))
        elif b and not a:
            decl.append(('removed', k, b['type']))
        elif a['type'] != b['type'] or a['static'] != b['static']:
            decl.append(('retyped %s -> %s' % (b['type'], a['type']), k, ''))
    out.append('\n## Member declarations\n')
    out += ['- %s %s::%s %s' % (d, k[0], k[1], t) for d, k, t in decl] or ['- none changed']
    wr = set()
    for a in LH.access:
        if int(a['line']) in H.get(a['file'], (set(), set()))[0] and a['kind'] in ('write', 'ref', 'call'):
            for c in a['cls'].split(','):
                wr.add('m:%s::%s' % (c, a['field']))
    wr |= {'m:%s::%s' % k for d, k, t in decl if d != 'removed'}
    if wr:
        out.append('\n## Members written on changed lines, or declared new\n')
        out.append(', '.join(sorted(w[2:] for w in wr)))
    seeds += sorted(wr)
    dl = sorted({d['define'] for d in LH.defines if int(d['line']) in H.get(d['file'], (set(), set()))[0]})
    if dl:
        out.append('\n## Defines read on changed lines\n')
        out.append(', '.join(dl))
        seeds += ['d:' + d for d in dl]
    # Python
    P = hunks(repo, base, head, PY)
    if P:
        out.append('\n## Python\n')
        for path, (hl, bl) in sorted(P.items()):
            if not path.endswith('.py'):
                continue
            eh, eb = py_extents(show(repo, head, PY + '/' + path)), py_extents(show(repo, base, PY + '/' + path))
            ch = {q for q, a, b in eh if any(a <= x <= b for x in hl)}
            cb = {q for q, a, b in eb if any(a <= x <= b for x in bl)}
            inner = lambda ext, qs: {q for q in qs if not any(o != q and o.startswith(q + '.') for o in qs)}
            ch, cb = inner(eh, ch), inner(eb, cb)
            hq, bq = {q for q, a, b in eh}, {q for q, a, b in eb}
            out.append('- %s: changed %s; added %s; removed %s' % (
                path, ', '.join(sorted(q for q in ch if q in bq)) or 'module-level code',
                ', '.join(sorted(q for q in ch if q not in bq)) or 'none', ', '.join(sorted(q for q in cb if q not in hq)) or 'none'))
            for q in (ch or {'<module>'}):
                nid = 'p:%s:%s' % (path, q)
                if nid in g.info:
                    seeds.append(nid)
                else:
                    out.append('  - %s is not in the map\'s Python scan (newer than the map)' % q)
    # XML
    X = hunks(repo, base, head, XML)
    if X:
        out.append('\n## XML\n')
        tag_re = re.compile(r'<([A-Za-z_][\w.:-]*)[\s>/]')
        for path, (hl, bl) in sorted(X.items()):
            if not path.lower().endswith('.xml'):
                continue
            tags, defs = set(), set()
            for rev, lines in ((head, hl), (base, bl)):
                text = show(repo, rev, XML + '/' + path).split('\n')
                for x in sorted(lines):
                    if 1 <= x <= len(text):
                        tags.update(m.group(1) for m in tag_re.finditer(text[x - 1] + ' '))
                        for k in range(x - 1, max(-1, x - 8), -1):   # the <DefineName> of a changed define value
                            m = re.search(r'<DefineName>\s*([^<\s]+)', text[k])
                            if m:
                                defs.add(m.group(1))
                                break
            tags -= {'DefineName', 'Define', 'iDefineIntVal', 'fDefineFloatVal', 'DefineTextVal'} if defs else set()
            out.append('- %s: tags on changed lines: %s%s' % (path, ', '.join(sorted(tags)) or 'none',
                                                              ('; defines: ' + ', '.join(sorted(defs))) if defs else ''))
            seeds += ['t:' + t for t in sorted(tags) if 't:' + t in g.info] + ['d:' + d for d in sorted(defs) if 'd:' + d in g.info]
    report(g, seeds, out, depth, follow_writes=False)
    if removed:
        out.append('\n## Callers of removed C++ functions\n')
        for f in removed:
            cs = sorted({g.info[c]['label'] for n in g.cnodes(f) for c in g.dep.get(n, {})})
            out.append('- %s <- %s' % (f, ', '.join(cs[:15]) or 'none'))
    return '\n'.join(out)


def main(argv):
    depth, src = 3, None
    if '--depth' in argv:
        k = argv.index('--depth'); depth = int(argv[k + 1]); del argv[k:k + 2]
    if '--src' in argv:
        k = argv.index('--src'); src = argv[k + 1]; del argv[k:k + 2]
    if len(argv) < 2:
        sys.exit(__doc__)
    cmd, args = argv[0], argv[1:]
    if cmd == 'diff':
        print(diff(args[0], args[1], args[2] if len(args) > 2 else 'HEAD', depth))
        return
    L = Layer(src=src)
    g = graph(L)
    out, seeds = [], []
    q = args[0]
    if cmd == 'func':
        seeds = [n for n, i in g.info.items() if i['kind'] in ('cpp', 'new') and re.fullmatch(q, i['label'])]
    elif cmd == 'py':
        mod, _, name = q.partition(':')
        seeds = [n for n, i in g.info.items() if i['kind'] == 'py' and (i['file'] == mod or i['file'].endswith('/' + mod))
                 and (not name or n.split(':', 2)[2] == name)]
    elif cmd == 'field':
        seeds = [n for n in g.info if n.startswith('m:') and (n[2:] == q or n.endswith('::' + q))]
    elif cmd == 'tag':
        seeds = ['t:' + q]
    elif cmd == 'define':
        seeds = ['d:' + q]
    elif cmd == 'file':
        if q.lower().endswith('.xml'):
            seeds = ['t:' + t for t, rows in g.xml.items() if any(r['file'] == q and r['loaded'] == '1' for r in rows) and 't:' + t in g.info]
        else:
            seeds = [n for n, i in g.info.items() if i['kind'] in ('cpp', 'py') and (i['file'] == q or i['file'].endswith('/' + q))]
    else:
        sys.exit(__doc__)
    report(g, seeds, out, depth, follow_writes=cmd in ('func', 'py', 'file'),
           title='# Impact of %s %s (%d start node%s)' % (cmd, q, len(seeds), '' if len(seeds) == 1 else 's'))
    print('\n'.join(out))


if __name__ == '__main__':
    main(sys.argv[1:])
