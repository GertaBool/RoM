#!/usr/bin/env python3
"""Resolve the Python's calls as Python resolves them, wherever the source shows the target.

usage: py_resolve.py          reads codemap/map, writes map/py_resolved.tsv

Inputs: py_calls.tsv (each call with its receiver expression), py_functions.tsv, py_classes.tsv,
py_args.tsv, py_assign.tsv, py_returns.tsv, py_imports.tsv, py_modules.tsv (the module each import name loads: mod, then
Beyond the Sword, then Civilization IV), and for the C++ side python_classes.tsv, python_bindings.tsv,
function_returns.tsv (clang) and py_api.tsv (the class reference, for classes the exe registers).

A name is looked up as Python looks it up: the function's own assignments, the enclosing functions', then the
module (its defs, classes, assignments and imports; `from X import *` brings X's names; CvPythonExtensions is the
C++ side). A value has a type when the source fixes it:
  - a module (import X), a Python class or function, a C++-side class (CyGlobalContext);
  - an instance: calling a class, `self` (the first parameter of a method), an attribute set in the class
    (self.x = ...), or the result of a C++ method, typed by the C++ function's declared return type;
  - a variable whose every assignment in its scope gives the same type; the result of a Python function whose
    every return statement gives the same type (py_returns.tsv); a parameter, when every call of its function is
    resolved and passes the same type there (py_params.tsv), the function is never used as a value
    (py_values.tsv), no unresolved call has its name, and no call passes keyword or star arguments or leaves the
    parameter to its default. Other parameters have no type.
How each call resolves (column how):
  py         a Python function or method (bases followed); target: module:qualname
  cpp        a method of a class the DLL registers, on a receiver of known type; target: the C++ function(s)
  exe        a method of a class the exe registers (CyInterface ...); target: Class.method
  api-class  a call constructing a C++-side class (CyGlobalContext()); target: the class
  builtin    a Python builtin (len, range ...)
  cpp-only, py-only  the receiver's type is not fixed, but the name has one possible target in all the code: one
             DLL binding, or one Python function, and no exe class, other Python function or built-in type method
  unresolved the receiver's type is not fixed by the source (an event argument, a list element ...) and several
             targets carry the name; graph.py falls back to a name match for these, and labels the link so
"""
import collections, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, '..', 'map')
BUILTINS = set('''abs all any apply basestring bool buffer callable chr classmethod cmp coerce compile complex delattr dict dir
divmod enumerate eval execfile file filter float frozenset getattr globals hasattr hash help hex id input int intern
isinstance issubclass iter len list locals long map max min object oct open ord pow property range raw_input reduce
reload repr reversed round set setattr slice sorted staticmethod str sum super tuple type unichr unicode vars xrange
zip __import__'''.split())


def read(n):
    p = os.path.join(M, n)
    if not os.path.exists(p):
        return []
    with open(p, encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


class Resolver:
    def __init__(self):
        self.mod_of = {}                                  # bare module name -> module path (first layer wins)
        for r in read('py_modules.tsv'):
            self.mod_of.setdefault(os.path.splitext(os.path.basename(r['module']))[0], r['module'])
        self.defs = collections.defaultdict(dict)        # module -> qualname -> kind
        for r in read('py_functions.tsv'):
            self.defs[r['module']][r['name']] = r['kind']
        self.bases = {(r['module'], r['class']): [b for b in r['bases'].split(',') if b] for r in read('py_classes.tsv')}
        self.args = {(r['module'], r['function']): r['args'].split(',') if r['args'] else [] for r in read('py_args.tsv')}
        self.assign = collections.defaultdict(list)      # (module, scope, target) -> [expr]
        for r in read('py_assign.tsv'):
            self.assign[(r['module'], r['scope'], r['target'])].append(r['expr'])
        self.selfattr = collections.defaultdict(list)    # (module, class, attr) -> [(scope, expr)]
        for (m, scope, t), es in list(self.assign.items()):
            if '.' in t:
                obj, attr = t.split('.', 1)
                cls = self.class_of(m, scope)
                if cls and self.first_arg(m, scope) == obj:
                    self.selfattr[(m, cls, attr)] += [(scope, e) for e in es]
        self.returns = collections.defaultdict(list)     # (module, function) -> [expr of each return]
        for r in read('py_returns.tsv'):
            self.returns[(r['module'], r['function'])].append(r['expr'])
        self.imports = collections.defaultdict(list)     # (module, scope) -> rows
        for r in read('py_imports.tsv'):
            self.imports[(r['module'], r['scope'])].append(r)
        # C++ side
        self.pyclass_cpp = {r['python_class']: r['cpp_class'] for r in read('python_classes.tsv')}
        self.cpp_pyclass = {v: k for k, v in self.pyclass_cpp.items()}
        self.cpp_bases = {r['cpp_class']: [b for b in r['bases'].split(',') if b] for r in read('python_classes.tsv')}
        self.binds = collections.defaultdict(lambda: collections.defaultdict(list))   # cpp class -> name -> targets
        for r in read('python_bindings.tsv'):
            self.binds[r['cpp_class']][r['python_name']].append(r['target'].lstrip('&'))
        self.ret = {r['function']: r['returns'] for r in read('function_returns.tsv')}
        self.api = collections.defaultdict(dict)          # class -> method -> returns (reference)
        self.api_by = {}
        for r in read('py_api.tsv'):
            self.api[r['class']][r['method']] = r['returns']
            self.api_by[r['class']] = r['bound_by']
        self.api_names = set(self.pyclass_cpp) | set(self.api)
        self.memo = {}
        self.ptypes = {}                                  # (module, function) -> {parameter: type}
        self.valued = {r['name'] for r in read('py_values.tsv')}

    def type_parameters(self, calls, resolved):
        """One round: a parameter gets a type when every call of its function is resolved and passes that type."""
        unresolved_names = {c['name'] for c, (how, t) in zip(calls, resolved) if how in ('unresolved', 'py-only')}
        sites = collections.defaultdict(list)            # (module, function) -> [(positional types, complete)]
        for c, (how, tgt) in zip(calls, resolved):
            if how != 'py':
                continue
            m, q = tgt.split(':', 1)
            if self.defs[m].get(q) != 'def':
                continue
            args = [a for a in c.get('args', '').split('|') if a] if c.get('args') else []
            star = '*' in args
            types = [self.eval(c['module'], c['caller'], a) for a in args if a != '*']
            parent = q.rsplit('.', 1)[0] if '.' in q else ''
            offset = 0
            if self.defs[m].get(parent) == 'class':
                recv = self.eval(c['module'], c['caller'], c.get('recv', '')) if c['attribute'] == '1' else None
                via_instance = c['attribute'] == '1' and recv is not None and recv[0] == 'inst'
                ctor = q.endswith('.__init__') and not (c['attribute'] == '1' and c['name'] == '__init__')
                offset = 1 if (via_instance or ctor) else 0
            sites[(m, q)].append((offset, types, star))
        new = {}
        for (m, q), lst in sites.items():
            short = q.split('.')[-1]
            if short in self.valued or short in unresolved_names:
                continue
            params = self.args.get((m, q), [])
            typed = {}
            for k, p in enumerate(params):
                ts = []
                for offset, types, star in lst:
                    i = k - offset
                    if star or i < 0 or i >= len(types):
                        ts = None
                        break
                    ts.append(types[i])
                if ts:
                    t = self.same(ts)
                    if t is not None and t[0] == 'inst':
                        typed[p] = t
            if typed:
                new[(m, q)] = typed
        return new

    # ---- scopes ----
    def class_of(self, m, scope):
        parts = scope.split('.')
        for k in range(len(parts) - 1, 0, -1):
            if self.defs[m].get('.'.join(parts[:k])) == 'class':
                return '.'.join(parts[:k])
        return None

    def first_arg(self, m, scope):
        """The first parameter of the method holding scope (the instance), or None."""
        parts = scope.split('.')
        for k in range(len(parts), 0, -1):
            q = '.'.join(parts[:k])
            if self.defs[m].get(q) == 'def' and self.defs[m].get('.'.join(parts[:k - 1])) == 'class':
                a = self.args.get((m, q), [])
                return a[0] if a else None
        return None

    def scopes(self, scope):
        """scope, its enclosing functions (not classes), then <module>."""
        out = []
        parts = scope.split('.') if scope != '<module>' else []
        while parts:
            out.append('.'.join(parts))
            parts.pop()
        return out + ['<module>']

    # ---- names ----
    def lookup(self, m, scope, name, depth=0):
        """Value of a name in module m, scope: ('module', path) | ('pyclass', m, q) | ('pyfunc', m, q) |
        ('apiclass', C) | ('inst', type) | ('builtin', name) | None"""
        key = ('L', m, scope, name)
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = None
        v = self._lookup(m, scope, name, depth)
        self.memo[key] = v
        return v

    def _lookup(self, m, scope, name, depth):
        if depth > 12:
            return None
        for s in self.scopes(scope):
            if s != '<module>':
                if name in self.args.get((m, s), []):
                    parent = s.rsplit('.', 1)[0] if '.' in s else ''
                    if self.defs[m].get(parent) == 'class' and self.args[(m, s)][0] == name:
                        return ('inst', ('py', m, parent))   # the instance: first parameter of a method
                    return self.ptypes.get((m, s), {}).get(name)   # typed by every call site, else none
                if (m, s, name) in self.assign:
                    return self.same([self.eval(m, s, e, depth + 1) for e in self.assign[(m, s, name)]])
                q = s + '.' + name
                if self.defs[m].get(q) == 'def':
                    return ('pyfunc', m, q)
                if self.defs[m].get(q) == 'class':
                    return ('pyclass', m, q)
            for r in self.imports.get((m, s), []):
                v = self.from_import(r, name, depth)
                if v is not None:
                    return v
        if self.defs[m].get(name) == 'def':
            return ('pyfunc', m, name)
        if self.defs[m].get(name) == 'class':
            return ('pyclass', m, name)
        if (m, '<module>', name) in self.assign:
            return self.same([self.eval(m, '<module>', e, depth + 1) for e in self.assign[(m, '<module>', name)]])
        if name in BUILTINS:
            return ('builtin', name)
        return None

    def from_import(self, r, name, depth):
        if r['kind'] == 'import':
            bound = r['alias'] or r['source'].split('.')[0]
            if bound == name:
                return self.module(r['source'] if r['alias'] else r['source'].split('.')[0])
            return None
        src = r['source']
        if r['name'] == '*':
            if src == 'CvPythonExtensions':
                return ('apiclass', name) if name in self.api_names else None
            sm = self.mod_of.get(src.split('.')[-1])
            if sm and (self.defs[sm].get(name) or (sm, '<module>', name) in self.assign):
                return self.lookup(sm, '<module>', name, depth + 1)
            return None
        if (r['alias'] or r['name']) == name:
            if src == 'CvPythonExtensions':
                return ('apiclass', r['name']) if r['name'] in self.api_names else None
            sm = self.mod_of.get(src.split('.')[-1])
            if sm:
                if self.defs[sm].get(r['name']) or (sm, '<module>', r['name']) in self.assign or \
                        any(x for x in self.imports.get((sm, '<module>'), [])):
                    return self.lookup(sm, '<module>', r['name'], depth + 1)
                return self.module(src + '.' + r['name'])
        return None

    def module(self, dotted):
        if dotted == 'CvPythonExtensions':
            return ('module', 'CvPythonExtensions')
        p = self.mod_of.get(dotted.split('.')[-1])
        return ('module', p) if p else None

    @staticmethod
    def same(vals):
        vals = set(vals)
        return vals.pop() if len(vals) == 1 and None not in vals else None

    # ---- expressions ----
    def eval(self, m, scope, e, depth=0):
        key = ('E', m, scope, e)
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = None
        v = self._eval(m, scope, e, depth)
        self.memo[key] = v
        return v

    def _eval(self, m, scope, e, depth):
        if not e or '?' in e or depth > 12:
            return None
        ops = re.findall(r'\(\)|\.?[A-Za-z_]\w*', e)
        if ''.join(ops) != e or not ops or ops[0] == '()':
            return None
        v = self.lookup(m, scope, ops[0], depth)
        for op in ops[1:]:
            if v is None:
                return None
            if op == '()':
                v = self.call(v)
            else:
                v = self.attr(v, op[1:], depth)
        return v

    def call(self, v):
        k = v[0]
        if k == 'pyclass':
            return ('inst', ('py', v[1], v[2]))
        if k == 'apiclass':
            return ('inst', ('api', v[1]))
        if k == 'apimethod':
            return self.api_return(v[1], v[2])
        if k == 'pyfunc':                             # the type every return statement of the function gives
            key = ('R', v[1], v[2])
            if key in self.memo:
                return self.memo[key]
            self.memo[key] = None
            es = self.returns.get((v[1], v[2]), [])
            t = self.same([self.eval(v[1], v[2], e) for e in es]) if es else None
            self.memo[key] = t
            return t
        return None

    def attr(self, v, a, depth):
        k = v[0]
        if k == 'module':
            if v[1] == 'CvPythonExtensions':
                return ('apiclass', a) if a in self.api_names else None
            return self.lookup(v[1], '<module>', a, depth + 1)
        if k == 'inst' and v[1][0] == 'api':
            return ('apimethod', v[1][1], a)
        if k == 'inst' and v[1][0] == 'py':
            meth = self.py_method(v[1][1], v[1][2], a, depth)
            if meth:
                return ('pyfunc',) + meth
            t = self.py_attr(v[1][1], v[1][2], a, depth)
            return t
        if k == 'pyclass':
            meth = self.py_method(v[1], v[2], a, depth)
            return ('pyfunc',) + meth if meth else None
        return None

    def py_method(self, m, cls, name, depth, seen=None):
        """(module, qualname) of method name in Python class cls or its bases."""
        seen = seen or set()
        if (m, cls) in seen or depth > 12:
            return None
        seen.add((m, cls))
        if self.defs[m].get(cls + '.' + name) == 'def':
            return (m, cls + '.' + name)
        for b in self.bases.get((m, cls), []):
            bv = self.eval(m, '<module>', b, depth + 1)
            if bv and bv[0] == 'pyclass':
                r = self.py_method(bv[1], bv[2], name, depth + 1, seen)
                if r:
                    return r
        return None

    def py_attr(self, m, cls, a, depth):
        es = self.selfattr.get((m, cls, a), [])
        return self.same([self.eval(m, s, e, depth + 1) for s, e in es]) if es else None

    def api_return(self, cls, meth):
        """Type of the result of C++-side method cls.meth: the declared return type of the bound C++ function,
        else the class reference's."""
        for t in self.api_targets(cls, meth):
            r = self.ret.get(t)
            if r:
                c = re.sub(r'\b(const|class|struct)\b|[*&]', '', r).strip()
                if c in self.cpp_pyclass:
                    return ('inst', ('api', self.cpp_pyclass[c]))
                return None
        r = self.api.get(cls, {}).get(meth)
        if r and r in self.api_names:
            return ('inst', ('api', r))
        return None

    def api_targets(self, cls, meth, seen=None):
        """C++ functions bound as cls.meth (cls a Python class name of the DLL), bases followed."""
        cpp = self.pyclass_cpp.get(cls)
        if not cpp:
            return []
        seen = seen or set()
        out, todo = [], [cpp]
        while todo:
            c = todo.pop()
            if c in seen:
                continue
            seen.add(c)
            out += self.binds.get(c, {}).get(meth, [])
            if out:
                break
            todo += self.cpp_bases.get(c, [])
        return out

    # ---- the only possible target of a name ----
    def only_target(self, name):
        """For x.name() with x of unknown type: the one target Python could reach, if there is only one: the name is
        bound by one DLL class, by no exe class, defined by no Python function, and no method of a built-in type."""
        if not hasattr(self, '_cands'):
            self._cands = collections.defaultdict(set)
            for cpp, names in self.binds.items():
                for n, ts in names.items():
                    for t in ts:
                        self._cands[n].add(('cpp', t))
            for cls, ms in self.api.items():
                if self.api_by.get(cls) == 'exe':
                    for n in ms:
                        self._cands[n].add(('exe', cls))
            for m, ds in self.defs.items():
                for q, kind in ds.items():
                    if kind == 'def':
                        self._cands[q.split('.')[-1]].add(('py', '%s:%s' % (m, q)))
            for t in (str, list, dict, tuple, set, int, float, bytes, type(None)):
                for n in dir(t):
                    self._cands[n].add(('builtin', t.__name__))
            for n in ('has_key', 'iteritems', 'iterkeys', 'itervalues', 'readline', 'readlines', 'write', 'close', 'read',
                      'next', 'seek', 'tell', 'flush', 'xreadlines', 'decode', 'encode'):
                self._cands[n].add(('builtin', 'py2'))
        c = self._cands.get(name, set())
        if len(c) == 1:
            k, t = next(iter(c))
            if k in ('cpp', 'py'):
                return k + '-only', t
        return None

    # ---- calls ----
    def resolve(self, c):
        how, tgt = self._resolve(c)
        if how == 'unresolved' and c['attribute'] == '1':
            o = self.only_target(c['name'])
            if o:
                return o
        return how, tgt

    def _resolve(self, c):
        m, scope, name, recv = c['module'], c['caller'], c['name'], c.get('recv', '')
        if c['attribute'] == '0':
            v = self.lookup(m, scope, name)
        else:
            rv = self.eval(m, scope, recv)
            if rv is None:
                return 'unresolved', ''
            v = self.attr(rv, name, 0)
            if v is None and rv[0] == 'inst' and rv[1][0] == 'api':
                v = ('apimethod', rv[1][1], name)
        if v is None:
            return 'unresolved', ''
        k = v[0]
        if k == 'pyfunc':
            return 'py', '%s:%s' % (v[1], v[2])
        if k == 'pyclass':
            init = self.py_method(v[1], v[2], '__init__', 0)
            return 'py', '%s:%s' % (init if init else (v[1], v[2]))
        if k == 'apiclass':
            return 'api-class', v[1]
        if k == 'builtin':
            return 'builtin', v[1]
        if k == 'apimethod':
            cls, meth = v[1], v[2]
            if cls in self.pyclass_cpp:
                ts = self.api_targets(cls, meth)
                return ('cpp', ','.join(ts)) if ts else ('unresolved', '')
            return 'exe', '%s.%s' % (cls, meth)
        return 'unresolved', ''


def main():
    R = Resolver()
    calls = read('py_calls.tsv')
    for rnd in range(8):                                 # parameters typed from call sites, to a fixed point
        R.memo = {}
        resolved = [R.resolve(c) for c in calls]
        new = R.type_parameters(calls, resolved)
        print('round %d: %d unresolved, %d functions with typed parameters' % (
            rnd + 1, sum(1 for h, t in resolved if h == 'unresolved'), len(new)), file=sys.stderr)
        if new == R.ptypes:
            break
        R.ptypes = new
    R.memo = {}
    rows, count = [], collections.Counter()
    for c in calls:
        how, tgt = R.resolve(c)
        count[how] += 1
        rows.append((c['module'], c['caller'], c['name'], c['attribute'], c['line'], c.get('recv', ''), how, tgt))
    with open(os.path.join(M, 'py_params.tsv'), 'w', encoding='utf-8') as o:
        o.write('module\tfunction\tparameter\ttype\n')
        for (m, q), d in sorted(R.ptypes.items()):
            for p, t in sorted(d.items()):
                o.write('%s\t%s\t%s\t%s\n' % (m, q, p, t[1][1] if t[1][0] == 'api' else '%s:%s' % (t[1][1], t[1][2])))
    with open(os.path.join(M, 'py_resolved.tsv'), 'w', encoding='utf-8') as o:
        o.write('module\tcaller\tname\tattribute\tline\trecv\thow\ttarget\n')
        for r in rows:
            o.write('\t'.join(r) + '\n')
    print('%d calls: %s' % (len(rows), ', '.join('%s %d' % kv for kv in count.most_common())))


if __name__ == '__main__':
    main()
