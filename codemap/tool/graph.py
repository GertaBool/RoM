#!/usr/bin/env python3
"""The whole map as one dependency graph: C++ functions, Python functions, member variables, XML tags, defines.

Imported by impact.py and graph_html.py. A node id is
  c:<n>                  C++ function n of map/functions.tsv
  p:<module>:<name>      Python function (or class, or <module> for module-level code) of map/py_functions.tsv
  s:<Scope::name>        C++ function seen by the syntactic scan but not in the compiler map (newer source)
  m:<Class>::<member>    data member of a class (map/fields.tsv)
  t:<tag>                XML element name (map/xml_tags.tsv); a member's files are those its class (or a class
                         derived from it) is loaded from (map/xml_classes.tsv) that hold the tag
  d:<NAME>               global define (map/defines_used.tsv, map/xml_defines.tsv)

dep[a] holds the nodes a change of a reaches directly, each with the kind of link:
  call      C++ caller of a C++ function (map/calls.tsv; virtual calls into overrides, as query.py)
  py>cpp    Python call of a C++ function bound for Python, resolved (map/py_resolved.tsv)
  py>py     Python caller of a Python function, resolved: imports, self and bases, typed receivers
  ... (only target)  the receiver's type is not fixed, but the name has one possible target in all the code
  ... (name match)   unresolved: every function bearing the name (py_to_cpp.tsv; for Python, a name defined
            in one module only)
  cpp>py    C++ function that calls a Python function (map/cpp_to_py.tsv)
  event     C++ function posting the event a Python handler is registered for (map/event_handlers.tsv)
  read      function reading a member (map/field_access.tsv: read, ref, call)
  fill      member an XML tag fills (map/field_strings.tsv, XML loader calls)
  define    function reading a global define (map/defines_used.tsv)
writes[f] holds the members function f writes: followed only from functions that are themselves changed
(their new code may store different values), never from callers.
"""
import collections, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
M = os.path.join(HERE, '..', 'map')


def read(n):
    p = os.path.join(M, n)
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


TPL = re.compile(r'<.*?>')


def key(scope, name):
    return (TPL.sub('', scope or ''), TPL.sub('', name or ''))


class Graph:
    def __init__(self, layer=None):
        """layer: an impact.Layer-like object with functions, fields, access, strings, defines (the syntactic
        layer); None reads the stored tables."""
        import query as Q
        self.Q = Q
        self.info = {}                       # id -> dict(kind, label, file, line, ...)
        self.dep = collections.defaultdict(dict)   # id -> {id: link kind}
        self.writes = collections.defaultdict(set)
        # C++ functions
        self.by_key = collections.defaultdict(list)
        exported = {i for i, r in Q.F.items() if r['exported'] == '1'}
        bound = collections.defaultdict(list)
        for r in read('python_defs.tsv'):
            bound[int(r['function'])].append(r['python_name'])
        self.bound = bound
        for i, r in Q.F.items():
            if r['definition'] != '1':
                continue
            nid = 'c:%d' % i
            self.info[nid] = dict(kind='cpp', label=(r['scope'] + '::' if r['scope'] else '') + r['name'],
                                  file=r['file'], line=int(r['line'] or 0), exported=i in exported, bound=i in bound)
            self.by_key[key(r['scope'], r['name'])].append(nid)
        for i, callers in Q.up.items():
            for c in callers:
                if 'c:%d' % i in self.info and 'c:%d' % c in self.info:
                    self.dep['c:%d' % i]['c:%d' % c] = 'call'
        # Python functions
        pyf = read('py_functions.tsv')
        self.py_by_mod = collections.defaultdict(dict)    # module -> {qualname: id}
        mods = {r['module'] for r in pyf} | {r['module'] for r in read('py_calls.tsv')}
        for m in mods:
            self.pynode(m, '<module>')
        for r in pyf:
            self.pynode(r['module'], r['name'], int(r['line']), r['kind'])
        self.modname = collections.defaultdict(list)     # bare module name -> module paths
        for m in mods:
            self.modname[os.path.splitext(os.path.basename(m))[0]].append(m)
        # Python calls: resolved as Python resolves them where the source fixes the target (py_resolve.py,
        # map/py_resolved.tsv); a name match only for calls left unresolved, labelled so
        res = read('py_resolved.tsv')
        unres = {(r['module'], r['caller'], r['name'], r['line']) for r in res if r['how'] == 'unresolved'} if res else None
        for r in res:
            how, tgt = r['how'], r['target']
            if how not in ('cpp', 'cpp-only', 'py', 'py-only'):
                continue
            src = self.pycaller(r['module'], r['caller'])
            if how.startswith('cpp'):
                for t in tgt.split(','):
                    scope, _, name = t.rpartition('::')
                    for nid in self.by_key.get(key(scope, name), []):
                        self.dep[nid].setdefault(src, 'py>cpp' if how == 'cpp' else 'py>cpp (only target)')
            else:
                m, q = tgt.split(':', 1)
                node = self.py_by_mod[m].get(q)
                if node and node != src:
                    self.dep[node].setdefault(src, 'py>py' if how == 'py' else 'py>py (only target)')
        for r in read('py_to_cpp.tsv'):
            if unres is not None and (r['module'], r['caller'], r['name'], r['line']) not in unres:
                continue
            src = self.pycaller(r['module'], r['caller'])
            for f in r['functions'].split(','):
                if f.strip().isdigit() and 'c:' + f.strip() in self.info:
                    self.dep['c:' + f.strip()].setdefault(src, 'py>cpp (name match)')
        api_names = {r['method'] for r in read('py_api.tsv')} | {r['python_name'] for r in read('python_defs.tsv')}
        defined = collections.defaultdict(set)   # last name -> modules defining it
        for r in pyf:
            defined[r['name'].split('.')[-1]].add(r['module'])
        for r in read('py_calls.tsv'):
            if unres is not None and (r['module'], r['caller'], r['name'], r['line']) not in unres:
                continue
            src = self.pycaller(r['module'], r['caller'])
            n = r['name']
            if r['attribute'] == '1' and n not in api_names and len(defined.get(n, ())) == 1:
                m = next(iter(defined[n]))
                hits = [v for q, v in self.py_by_mod[m].items() if q.split('.')[-1] == n]
                if len(hits) == 1 and hits[0] != src:
                    self.dep[hits[0]].setdefault(src, 'py>py (name match)')
        for r in read('cpp_to_py.tsv'):
            if r['python_file']:
                tgt = self.py_by_mod[r['python_file']].get(r['python_function'])
                if tgt and 'c:' + r['caller'] in self.info:
                    self.dep[tgt]['c:' + r['caller']] = 'cpp>py'
        # BUG <gameutils> dispatch: CvGameInterface.<cb> -> CvGameUtils / RoMGameUtils / RevDCMReligionControl / etc.
        gi_mods = self.modname.get('CvGameInterface', [])
        for r in read('py_gameutils.tsv'):
            htgt = self.py_by_mod[r['module']].get(r['handler'])
            if not htgt:
                continue
            for gm in gi_mods:
                gsrc = self.py_by_mod[gm].get(r['callback'])
                if gsrc and gsrc != htgt:
                    self.dep[htgt].setdefault(gsrc, 'py>py')
        for r in read('event_handlers.tsv'):
            h = self.handler(r)
            if h and 'c:' + r['function'] in self.info:
                self.dep[h]['c:' + r['function']] = 'event'
                self.info[h].setdefault('events', set()).add(r['event'])
        # the syntactic layer: members, XML tags, defines
        if layer is None:
            import impact
            layer = impact.Layer()
        self.layer = layer
        for r in layer.fields:
            nid = 'm:%s::%s' % (r['cls'], r['field'])
            self.info[nid] = dict(kind='member', label='%s::%s' % (r['cls'], r['field']), file=r['file'],
                                  line=int(r['line']), type=r['type'], saved=False, tags=set())
        for a in layer.access:
            f = self.cnode_at(a['function'], a.get('file', ''), int(a['line']) if str(a.get('line', '')).isdigit() else 0)
            for c in a['cls'].split(','):
                m = 'm:%s::%s' % (c, a['field'])
                if m not in self.info:
                    continue
                if a['kind'] in ('read', 'ref', 'call'):
                    self.dep[m].setdefault(f, 'read')
                if a['kind'] in ('write', 'ref', 'call'):
                    self.writes[f].add(m)
                if a['function'].split('::')[-1] in ('read', 'write') and self.in_stream(a['file'], int(a['line'])):
                    self.info[m]['saved'] = True
        xml = collections.defaultdict(list)
        for r in read('xml_tags.tsv'):
            xml[r['tag']].append(r)
        self.xml = xml
        for s in layer.strings:
            if 'XmlVal' in s['call'] or 'TagPair' in s['call'] or s['call'].startswith(('Set', 'Get')):
                t = 't:' + s['string']
                if t not in self.info:
                    self.info[t] = dict(kind='tag', label='<%s>' % s['string'], files=xml.get(s['string'], []))
                for c in s['cls'].split(','):
                    m = 'm:%s::%s' % (c, s['field'])
                    if m in self.info:
                        self.dep[t][m] = 'fill'
                        self.info[m]['tags'].add(s['string'])
        # which files feed a member: the files loaded into its class or a class derived from it (xml_classes.tsv),
        # including WoC modular overrides under Assets/Modules/ (*_<FileName>.xml).
        kids = collections.defaultdict(set)
        for r in read('bases.tsv'):
            kids[r['base']].add(r['class'])
        loads = collections.defaultdict(set)
        for r in read('xml_classes.tsv'):
            loads[r['cls']].add(r['file'].lower())

        def below(c, seen=None):
            seen = set() if seen is None else seen
            if c not in seen:
                seen.add(c)
                for k in kids.get(c, ()):
                    below(k, seen)
            return seen
        for nid, i in self.info.items():
            if i['kind'] == 'member' and i['tags']:
                files = set().union(*(loads.get(c, set()) for c in below(i['label'].split('::')[0])))
                basenames = {os.path.basename(f) for f in files}
                i['xml'] = {}
                for t in i['tags']:
                    if not files:
                        rows = []
                    else:
                        rows = []
                        for r in xml.get(t, []):
                            rf = r['file'].lower()
                            if rf in files:
                                rows.append(r)
                            elif r.get('layer') == 'mod-module':
                                rb = os.path.basename(rf)
                                if rb in basenames or any(rb.endswith('_' + b) for b in basenames):
                                    rows.append(r)
                    i['xml'][t] = (rows, bool(files))
        dfile = collections.defaultdict(list)
        for r in read('xml_defines.tsv'):
            dfile[r['define']].append(r)
        for d in layer.defines:
            nid = 'd:' + d['define']
            if nid not in self.info:
                self.info[nid] = dict(kind='define', label=d['define'], files=dfile.get(d['define'], []))
            fn = self.cnode_at(d['function'], d.get('file', ''), int(d['line']) if str(d.get('line', '')).isdigit() else 0)
            self.dep[nid].setdefault(fn, 'define')

    def in_stream(self, file, line):
        """Is this source line inside a read/write(FDataStreamBase*) function (serialization)?"""
        if not hasattr(self, '_stream'):
            self._stream = collections.defaultdict(list)
            for i, r in self.Q.F.items():
                if r['name'] in ('read', 'write') and 'FDataStreamBase' in r['sig'] and r['line'] and r['end']:
                    self._stream[r['file']].append((int(r['line']), int(r['end'])))
        return any(a <= line <= b for a, b in self._stream.get(file, ()))

    def pynode(self, module, name, line=0, kind='def'):
        nid = 'p:%s:%s' % (module, name)
        if nid not in self.info:
            self.info[nid] = dict(kind='py', label='%s %s' % (module, name), file=module, line=line, pykind=kind)
            self.py_by_mod[module][name] = nid
        elif line:
            self.info[nid]['line'] = line
        return nid

    def pycaller(self, module, caller):
        if caller in self.py_by_mod[module]:
            return self.py_by_mod[module][caller]
        # a nested function or lambda: the nearest enclosing name the scan has
        parts = caller.split('.')
        while parts:
            q = '.'.join(parts)
            if q in self.py_by_mod[module]:
                return self.py_by_mod[module][q]
            parts.pop()
        return self.pynode(module, '<module>')

    def handler(self, r):
        """The Python function an event_handlers.tsv row registers, or None."""
        src, h, f = r['source'], r['handler'], r['file']
        if src == 'EventHandlerMap':
            return self.py_by_mod[f].get(h)
        if src == 'addEventHandler':
            caller, _, attr = h.partition(': ')
            attr = attr.replace('self.', '')
            cls = caller.split('.')[0]
            return self.py_by_mod[f].get('%s.%s' % (cls, attr)) or self.py_by_mod[f].get(attr)
        if src == 'BUG config':
            mod, _, fn = h.partition('.')
            for m in self.modname.get(mod, []):
                if fn in self.py_by_mod[m]:
                    return self.py_by_mod[m][fn]
                short = fn.split('.')[-1]
                hit = [v for q, v in self.py_by_mod[m].items() if q.split('.')[-1] == short]
                if hit:
                    return hit[0]
        return None

    def cnode_at(self, fid, file='', line=0):
        """Exact C++ function node for Scope::name at (file, line), disambiguating overloads by line span."""
        scope, _, name = fid.rpartition('::')
        ids = self.by_key.get(key(scope, name))
        if ids:
            if len(ids) == 1 or not line:
                return ids[0]
            for nid in ids:
                r = self.Q.F.get(int(nid[2:]))
                if not r or not r['line'] or not r['end']:
                    continue
                if (not file or r['file'] == file) and int(r['line']) <= line <= int(r['end']):
                    return nid
            # Fallback: nearest overload in the same file whose start <= line
            same_file = [(int(self.Q.F[int(nid[2:])]['line']), nid) for nid in ids
                         if self.Q.F.get(int(nid[2:]), {}).get('file') == file and self.Q.F[int(nid[2:])].get('line')]
            before = [x for x in same_file if x[0] <= line]
            if before:
                return max(before)[1]
            return ids[0]
        nid = 's:' + fid
        if nid not in self.info:
            self.info[nid] = dict(kind='new', label=fid, file=file, line=line)
        return nid

    def cnode(self, fid):
        """Node of a C++ function named Scope::name by the syntactic scan."""
        return self.cnode_at(fid)

    def cnodes(self, fid):
        scope, _, name = fid.rpartition('::')
        return self.by_key.get(key(scope, name)) or [self.cnode(fid)]

    def reach(self, seeds, follow_writes=True):
        """{node: (level, via, link)} of everything a change of the seeds reaches. With follow_writes, the members
        a seed function writes are reached at level 1 (link 'writes'), and their readers from there."""
        lv = {s: (0, None, None) for s in seeds}
        frontier, d = list(seeds), 0
        while frontier:
            d += 1
            nxt = []
            for a in frontier:
                edges = list(self.dep.get(a, {}).items())
                if follow_writes and lv[a][0] == 0:
                    edges += [(m, 'writes') for m in sorted(self.writes.get(a, ()))]
                for b, link in edges:
                    if b not in lv:
                        lv[b] = (d, a, link)
                        nxt.append(b)
            frontier = nxt
        return lv
