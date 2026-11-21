#!/usr/bin/env python3
"""What a change reaches: functions, member variables, saves, XML and Python, down the call graph.

usage: impact.py diff <rise-of-mankind checkout> <base> [<head>]   a change between two commits (head: HEAD)
       impact.py func <Scope::name | regex>                         one function
       impact.py field <Class::m_x | m_x>                            one member variable
       impact.py tag <XML element>                                  the members an XML tag fills, and on
       impact.py define <NAME>                                      a global define and who reads it
       impact.py file <file.cpp|file.h>                             every function of one file
options: --depth N    caller levels listed by name (default 2; all levels are always counted)
         --src DIR    CvGameCoreDLL dir to read the syntactic layer from live (default: codemap/map tables)

How it reaches:
  1. A changed function reaches its callers, level by level, in the compiler call graph (map/calls.tsv, with
     virtual calls followed into the overrides of the object's class, as query.py does).
  2. A changed member variable reaches every function that reads it (map/field_access.tsv or the live scan),
     and from each of those its callers.
  3. Each member is also checked for: the save (read or written in a read/write(FDataStreamBase) function),
     the XML tag that fills it (field_strings.tsv) and the XML files holding that tag (xml_tags.tsv).
  4. Exits from the DLL among everything reached: functions the exe can call (exported), functions bound for
     Python and the Python modules that call them (py_to_cpp.tsv).
A function the compiler map does not know (added after the map's commit) is followed by name through the
calls the syntactic scan saw (marked "name match").
"""
import collections, csv, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
M = os.path.join(HERE, '..', 'map')
DLL = 'Assets/CvGameCoreDLL'


def read(n):
    p = os.path.join(M, n)
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


import query as Q   # compiler map: Q.F, Q.name, Q.up (callers, overrides included)

TPL = re.compile(r'<.*?>')


def key(scope, name):
    return (TPL.sub('', scope or ''), TPL.sub('', name or ''))


by_key = collections.defaultdict(list)
for i, r in Q.F.items():
    if r['definition'] == '1':
        by_key[key(r['scope'], r['name'])].append(i)
exported = {i for i, r in Q.F.items() if r['exported'] == '1'}
py_bound = collections.defaultdict(list)
for r in read('python_defs.tsv'):
    py_bound[int(r['function'])].append(r['python_name'])
py_callers = collections.defaultdict(set)
for r in read('py_to_cpp.tsv'):
    for f in r['functions'].split(','):
        if f.strip().isdigit():
            py_callers[int(f)].add(r['module'])
xml_files = collections.defaultdict(list)
for r in read('xml_tags.tsv'):
    xml_files[r['tag']].append((r['file'], int(r['count'])))
define_file = {r['define']: r['file'] for r in read('xml_defines.tsv')}


class Layer:
    """The syntactic layer: stored tables, or a live scan of a source dir (or of {file: bytes})."""

    def __init__(self, src=None, files=None):
        if src or files:
            import syntax
            s = syntax.scan(files if files is not None else syntax.read_sources(src))
            self.functions, self.fields, self.access = s['functions'], s['fields'], s['access']
            self.strings, self.defines, self.calls = s['strings'], s['defines'], s['calls']
            for r in self.functions:
                r['line'], r['end'] = int(r['line']), int(r['end'])
        else:
            self.functions = read('syntax_functions.tsv')
            for r in self.functions:
                r['line'], r['end'] = int(r['line']), int(r['end'])
            self.fields, self.access = read('fields.tsv'), read('field_access.tsv')
            self.strings, self.defines, self.calls = read('field_strings.tsv'), read('defines_used.tsv'), read('syntax_calls.tsv')
        self.uses = collections.defaultdict(list)          # (cls, field) -> access rows
        for a in self.access:
            for c in a['cls'].split(','):
                self.uses[(c, a['field'])].append(a)
        self.fill = collections.defaultdict(list)          # (cls, field) -> XML strings
        for s in self.strings:
            if 'XmlVal' in s['call'] or 'TagPair' in s['call'] or s['call'].startswith(('Set', 'Get')):
                for c in s['cls'].split(','):
                    self.fill[(c, s['field'])].append(s)
        self.call_rows = collections.defaultdict(list)    # callee's last name -> call rows
        for c in self.calls:
            self.call_rows[c['callee'].split('::')[-1]].append(c)
        self.defined_in = collections.defaultdict(set)   # name -> scopes defining it
        for r in self.functions:
            self.defined_in[r['name']].add(r['scope'])

    def callers_by_name(self, fid):
        """Callers of Scope::name seen by the scan: an unqualified call only from the same scope, a qualified
        call only when its scope matches, a call through an object (x.f(), x->f()) from anywhere."""
        scope, _, nm = fid.rpartition('::')
        res = set()
        for c in self.call_rows.get(nm, ()):
            if c['form'] == 'self' and c['function'].rpartition('::')[0] != scope:
                continue
            if c['form'] == 'qualified' and c['callee'].rpartition('::')[0].split('::')[-1] != scope.split('::')[-1]:
                continue
            if c['function'] == fid:
                continue
            res.add(c['function'])
        return res

    def field_rows(self, q):
        if '::' in q:
            c, f = q.rsplit('::', 1)
            return [r for r in self.fields if r['cls'] == c and r['field'] == f]
        return [r for r in self.fields if r['field'] == q]


def ids_of(fid):
    scope, _, name = fid.rpartition('::')
    return by_key.get(key(scope, name), [])


def callers(seeds):
    """{id: level} of every transitive caller of the seed ids (seeds at level 0)."""
    level = {s: 0 for s in seeds}
    frontier = list(seeds)
    d = 0
    while frontier:
        d += 1
        nxt = []
        for f in frontier:
            for c in Q.up.get(f, ()):
                if c not in level:
                    level[c] = d
                    nxt.append(c)
        frontier = nxt
    return level


def short(i):
    r = Q.F[i]
    return '%s%s  (%s:%s)' % (r['scope'] + '::' if r['scope'] else '', r['name'], r['file'], r['line'])


def field_report(L, cls, field, out):
    rows = L.uses.get((cls, field), [])
    w = sorted({r['function'] for r in rows if r['kind'] in ('write', 'ref', 'call')})
    rd = sorted({r['function'] for r in rows if r['kind'] in ('read', 'ref', 'call')})
    out.append('- **%s::%s**: written in %d function(s), read in %d' % (cls, field, len(w), len(rd)))
    if w:
        out.append('  - written (or passed by address / method called): ' + ', '.join(w[:12]) + (' ...' if len(w) > 12 else ''))
    if rd:
        out.append('  - read: ' + ', '.join(rd[:12]) + (' ...' if len(rd) > 12 else ''))
    save = sorted({r['function'] for r in rows if r['function'].split('::')[-1] in ('read', 'write')
                   and r['file'] != ''})
    if save:
        out.append('  - **save game**: in %s; a change of its type or of the order of reads/writes changes the save format'
                   % ', '.join(save))
    for s in L.fill.get((cls, field), []):
        files = xml_files.get(s['string'], [])
        out.append('  - **XML**: filled from tag `%s` (%s, %s:%s); tag found in %d XML file(s)%s'
                   % (s['string'], s['call'], s['file'], s['line'], len(files),
                      ': ' + ', '.join(f for f, _ in files[:6]) + (' ...' if len(files) > 6 else '') if files else ''))
    return rd


def reach_report(seed_ids, seed_names, depth, out, title='Callers'):
    lv = callers(seed_ids)
    reached = [i for i, d in lv.items() if d > 0]
    out.append('\n## %s (compiler call graph)\n' % title)
    if not seed_ids:
        out.append('No seed is in the compiler map.')
    by_level = collections.defaultdict(list)
    for i in reached:
        by_level[lv[i]].append(i)
    out.append('%d function(s) reach the changed code through calls; per level: %s'
               % (len(reached), ', '.join('%d: %d' % (d, len(by_level[d])) for d in sorted(by_level)) or 'none'))
    for d in sorted(by_level):
        if d > depth:
            break
        names = sorted(short(i) for i in by_level[d])
        out.append('\n### level %d (%d)\n' % (d, len(names)))
        out += ['- ' + n for n in names[:60]]
        if len(names) > 60:
            out.append('- ... %d more' % (len(names) - 60))
    files = collections.Counter(Q.F[i]['file'] for i in lv)
    out.append('\n### files touched by the reach (functions per file)\n')
    out.append(', '.join('%s %d' % kv for kv in files.most_common(40)))
    all_ids = set(lv)
    ex = sorted(short(i) for i in all_ids & exported)
    pb = sorted(i for i in all_ids if i in py_bound)
    mods = sorted({m for i in all_ids for m in py_callers.get(i, ())})
    out.append('\n## Exits from the DLL among them\n')
    out.append('- called by the exe (exported): %d%s' % (len(ex), (': ' + '; '.join(ex[:15]) + (' ...' if len(ex) > 15 else '')) if ex else ''))
    out.append('- bound for Python: %d%s' % (len(pb), (': ' + ', '.join(sorted({n for i in pb for n in py_bound[i]})[:25])) if pb else ''))
    out.append('- Python modules calling them: %d%s' % (len(mods), (': ' + ', '.join(mods[:25]) + (' ...' if len(mods) > 25 else '')) if mods else ''))
    return lv


def name_match(L, fids, out, seen=None):
    """Callers by name, for functions not in the compiler map; followed through other new functions until
    functions the compiler map knows are reached."""
    seen = set(fids) if seen is None else seen
    found = []
    for fid in fids:
        nm = fid.split('::')[-1]
        c = sorted(L.callers_by_name(fid)) if L.calls else []
        others = sorted(L.defined_in.get(nm, set()) - {fid.rpartition('::')[0]})
        out.append('- %s is not in the compiler map (newer than its commit); name match: called from %d function(s)%s%s'
                   % (fid, len(c), ': ' + ', '.join(c[:15]) if c else '',
                      ('; the name is also defined in %s, so calls through an object may be theirs' % ', '.join(others[:6])) if others else ''))
        for f in c:
            ids = ids_of(f)
            if ids:
                found += ids
            elif f not in seen:
                seen.add(f)
                found += name_match(L, [f], out, seen)
    return found


def analyse(L, seed_funcs, seed_fields, depth, out, written_fields=()):
    """seed_funcs: Scope::name strings; seed_fields: (cls, field)."""
    ids, unknown = [], []
    for f in seed_funcs:
        x = ids_of(f)
        (ids.extend(x) if x else unknown.append(f))
    nm_ids = set()
    if unknown:
        out.append('\n## Functions outside the compiler map\n')
        for f in unknown:
            nm_ids.update(name_match(L, [f], out))
        ids += sorted(nm_ids - set(ids))
    readers = set()
    fields = list(seed_fields) + [f for f in written_fields if f not in seed_fields]
    if fields:
        out.append('\n## Member variables\n')
        for cls, field in fields:
            readers.update(field_report(L, cls, field, out))
    fr = {i for f in readers for i in ids_of(f)}
    new_readers = sorted(f for f in readers if not ids_of(f) and f not in seed_funcs)
    if new_readers:
        out.append('\nReaders outside the compiler map, followed by name:')
        fr.update(name_match(L, new_readers, out))
    if fr:
        out.append('\nThe readers above are added to the reach (%d in the compiler map).' % len(fr))
    seeds = sorted(set(ids) | fr)
    if len(seeds) > 1:
        out.append('\n## Reach per changed function\n')
        out.append('| function | direct callers | all callers | exported reached | Python-bound reached |')
        out.append('|---|---|---|---|---|')
        rows = []
        for i in seeds:
            lv = callers([i])
            rows.append((len(lv) - 1, sum(1 for d in lv.values() if d == 1), Q.name[i].split('(')[0],
                         len(set(lv) & exported), sum(1 for x in lv if x in py_bound)))
        for n, d1, nm, ex, pb in sorted(rows, reverse=True):
            out.append('| %s | %d | %d | %d | %d |' % (nm, d1, n, ex, pb))
        if nm_ids:
            out.append('\nRows include callers of functions newer than the map (name match), standing in for the new code they lead to.')
        if fr:
            out.append('\nRows include the readers of changed members.')
    reach_report(seeds, seed_funcs, depth, out)


# ---------- diff ----------

def git(repo, *a):
    return subprocess.run(['git', '-C', repo] + list(a), capture_output=True, check=True).stdout


def hunks(repo, base, head):
    """{file: (head_lines, base_lines)} changed lines per source file of the DLL."""
    d = git(repo, 'diff', '-U0', base, head, '--', DLL).decode('latin-1')
    out = collections.defaultdict(lambda: (set(), set()))
    f = None
    for line in d.split('\n'):
        if line.startswith('+++ '):
            f = os.path.basename(line[6:]) if line[4:] != '/dev/null' else None
        elif line.startswith('--- ') and line[4:] != '/dev/null':
            f = os.path.basename(line[6:])
        elif line.startswith('@@') and f:
            m = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            b0, bn, h0, hn = int(m.group(1)), int(m.group(2) or 1), int(m.group(3)), int(m.group(4) or 1)
            out[f][0].update(range(h0, h0 + hn))
            out[f][1].update(range(b0, b0 + bn))
    return out


def files_at(repo, rev):
    names = git(repo, 'ls-tree', '--name-only', rev, DLL + '/').decode().split()
    import syntax
    out = {}
    for p in names:
        if p.endswith(syntax.SRC_EXT):
            out[os.path.basename(p)] = git(repo, 'show', '%s:%s' % (rev, p))
    return out


def diff(repo, base, head, depth):
    out = []
    hb = git(repo, 'rev-parse', '--short=12', base).decode().strip()
    hh = git(repo, 'rev-parse', '--short=12', head).decode().strip()
    H = hunks(repo, base, head)
    out.append('# Impact of %s..%s\n' % (hb, hh))
    log = git(repo, 'log', '--format=- %h %ad %s', '--date=short', '%s..%s' % (base, head)).decode()
    out.append('Commits:\n\n' + log)
    LH, LB = Layer(files=files_at(repo, head)), Layer(files=files_at(repo, base))
    stat = git(repo, 'diff', '--stat', base, head).decode()
    out.append('```\n' + stat + '```')

    def touched(L, side):
        res = collections.OrderedDict()
        for fn in L.functions:
            lines = H.get(fn['file'], (set(), set()))[side]
            if lines and any(fn['line'] <= x <= fn['end'] for x in lines):
                res[(fn['scope'] + '::' if fn['scope'] else '') + fn['name']] = fn
        return res

    th, tb = touched(LH, 0), touched(LB, 1)
    hn = {(f['scope'] + '::' if f['scope'] else '') + f['name'] for f in LH.functions}
    bn = {(f['scope'] + '::' if f['scope'] else '') + f['name'] for f in LB.functions}
    added = [f for f in th if f not in bn]
    removed = [f for f in tb if f not in hn]
    changed = [f for f in th if f in bn]
    out.append('\n## Functions\n')
    out.append('- changed: %d; added: %d; removed: %d' % (len(changed), len(added), len(removed)))
    for lab, lst, L in (('changed', changed, th), ('added', added, th), ('removed', removed, tb)):
        for f in lst:
            r = L[f]
            out.append('  - %s %s  (%s:%d-%d)' % (lab, f, r['file'], r['line'], r['end']))
    # member variables: declarations added/removed/retyped
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
    # members written on changed lines
    wr = set()
    for a in LH.access:
        lines = H.get(a['file'], (set(), set()))[0]
        if int(a['line']) in lines and a['kind'] in ('write', 'ref', 'call'):
            for c in a['cls'].split(','):
                wr.add((c, a['field']))
    if wr:
        out.append('\n## Members written on changed lines\n')
        out.append(', '.join('%s::%s' % k for k in sorted(wr)))
    for d, k, t in decl:
        if d != 'removed':
            wr.add(k)
    # defines read on changed lines
    dl = sorted({(d['define'], d['function']) for d in LH.defines
                 if int(d['line']) in H.get(d['file'], (set(), set()))[0]})
    if dl:
        out.append('\n## Global defines read on changed lines\n')
        out += ['- %s in %s (defined in %s)' % (n, f, define_file.get(n, 'no XML file of the scan')) for n, f in dl]
    xmlch = [l for l in stat.split('\n') if '.xml' in l.lower()]
    if xmlch:
        out.append('\n## XML files changed\n')
        out += ['- ' + l.strip() for l in xmlch]
    out.append('\n_Member uses and functions are read from the source at each commit; callers come from the '
               'compiler map at its own commit (see skeleton.md), so callers added since then are found only by name._')
    analyse(LH, changed + added, [], depth, out, written_fields=sorted(wr))
    if removed:
        out.append('\n## Callers of removed functions (at the map\'s commit)\n')
        for f in removed:
            out += ['- %s <- %s' % (f, ', '.join(sorted({Q.name[c] for i in ids_of(f) for c in Q.up.get(i, ())})[:15]) or 'none')]
    return '\n'.join(out)


def main(argv):
    depth = 2
    src = None
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
    out = []
    if cmd == 'func':
        fs = sorted({(f['scope'] + '::' if f['scope'] else '') + f['name'] for f in L.functions
                     if re.fullmatch(args[0], (f['scope'] + '::' if f['scope'] else '') + f['name'])})
        if not fs:
            fs = sorted({Q.name[i].split('(')[0] for i in [Q.resolve(args[0])]})
        out.append('# Impact of %s\n' % ', '.join(fs))
        analyse(L, fs, [], depth, out)
    elif cmd == 'field':
        rows = L.field_rows(args[0])
        out.append('# Impact of member %s\n' % args[0])
        for r in rows:
            out.append('- declared %s %s::%s (%s:%s)' % (r['type'], r['cls'], r['field'], r['file'], r['line']))
        analyse(L, [], [(r['cls'], r['field']) for r in rows], depth, out)
    elif cmd == 'tag':
        out.append('# XML tag `%s`\n' % args[0])
        out.append('Found in: ' + (', '.join('%s (%d)' % x for x in xml_files.get(args[0], [])) or 'no XML file of the scan'))
        flds = sorted({(c, s['field']) for k, v in L.fill.items() for s in v if s['string'] == args[0] for c in [k[0]]})
        analyse(L, [], flds, depth, out)
    elif cmd == 'define':
        out.append('# Define `%s` (in %s)\n' % (args[0], define_file.get(args[0], 'no XML file of the scan')))
        fs = sorted({d['function'] for d in L.defines if d['define'] == args[0]})
        out.append('Read directly in: ' + (', '.join(fs) or 'nothing (it may be read through a variable)'))
        analyse(L, fs, [], depth, out)
    elif cmd == 'file':
        fs = sorted({(f['scope'] + '::' if f['scope'] else '') + f['name'] for f in L.functions if f['file'] == args[0]})
        out.append('# Impact of every function of %s (%d)\n' % (args[0], len(fs)))
        analyse(L, fs, [], depth, out)
    else:
        sys.exit(__doc__)
    print('\n'.join(out))


if __name__ == '__main__':
    main(sys.argv[1:])
