#!/usr/bin/env python3
"""Resolve the Python's calls as Python resolves them, wherever the source shows the target.

usage: py_resolve.py          reads codemap/map, writes map/py_resolved.tsv

Inputs: py_calls.tsv (each call with its receiver expression), py_functions.tsv, py_classes.tsv,
py_args.tsv, py_assign.tsv, py_returns.tsv, py_imports.tsv, py_modules.tsv (the module each import name loads: mod, then
Beyond the Sword, then Civilization IV), and for the C++ side python_classes.tsv, python_bindings.tsv,
python_free_funcs.tsv, python_enums.tsv, function_returns.tsv (clang) and py_api.tsv (the class reference, for classes
the exe registers).

A name is looked up as Python looks it up: the function's own assignments, the enclosing functions', then the
module (its defs, classes, assignments and imports; `from X import *` brings X's names; CvPythonExtensions is the
C++ side). A value has a type when the source fixes it:
  - a module (import X), a stdlib/external module, a Python class or function, a C++-side class (CyGlobalContext);
  - an instance: calling a class, `self` (the first parameter of a method), an attribute set in the class or its
    bases (self.x = ...), a builtin literal/constructor ($str, $list, $dict, $tuple, open()), or the result of a C++
    method, typed by the C++ function's declared return type;
  - a variable whose every non-None assignment in its scope gives the same type (including `for x in ...` loops,
    tuple unpacks, and homogeneous list.append() calls); the result of a Python function whose every non-None return
    statement gives the same type (py_returns.tsv); a parameter, when every resolved call of its function passes the
    same type there (py_params.tsv).
How each call resolves (column how):
  py         a Python function or method (bases followed); target: module:qualname
  cpp        a method or free function bound by the DLL, on a receiver of known type; target: the C++ function(s)
  exe        a method or free function of the exe (CyInterface, CyPitboss ...); target: Class.method or func
  api-class  a call constructing a C++-side class (CyGlobalContext()); target: the class
  api-enum   a C++-side enum constructor (ColorTypes(i)); target: the enum
  builtin    a Python builtin function, exception, or built-in type method (len, list.append, str.upper, file.write ...)
  stdlib     a Python standard library or external module call (os, sys, re, wx, StringIO ...)
  bug-option a dynamic BUG XML option getter/setter on BugCore.game.<Mod>; target: Mod.method
  cpp-only, py-only  the receiver's type is not fixed, but the name has one possible target in all the code: one
             DLL binding, or one Python function, and no exe class, other Python function or built-in type method
  unresolved the receiver's type is not fixed by the source (an event argument, a dynamic dispatch ...) and several
             targets carry the name; graph.py falls back to a name match for these, and labels the link so
"""
import collections, csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, '..', 'map')
BUILTINS = set('''abs all any apply basestring bool buffer callable chr classmethod cmp coerce compile complex delattr dict dir
divmod enumerate eval execfile file filter float frozenset getattr globals hasattr hash help hex id input int intern
isinstance issubclass iter len list locals long map max min object oct open ord pow property range raw_input reduce
reload repr reversed round set setattr slice sorted staticmethod str sum super tuple type unichr unicode vars xrange
zip __import__
Exception StandardError TypeError ValueError KeyError IndexError AttributeError RuntimeError IOError OSError ImportError
StopIteration NotImplementedError AssertionError ZeroDivisionError NameError LookupError ArithmeticError SystemError
UnicodeError UnicodeDecodeError UnicodeEncodeError Warning DeprecationWarning SyntaxError TabError IndentationError
OverflowError FloatingPointError MemoryError ReferenceError UnboundLocalError EOFError'''.split())

STDLIB = set('''os sys re math time random pickle cPickle StringIO cStringIO types codecs xml ConfigParser traceback copy
string operator struct socket threading thread dummy_thread gc inspect glob shutil stat sets md5 sha urllib urllib2
webbrowser Queue bisect weakref logging locale datetime itertools heapq array errno fnmatch tempfile pprint encodings
_winreg msvcrt winsound nt ntpath posixpath wx BaseHTTPServer SimpleHTTPServer SocketServer httplib urlparse mimetools
rfc822 email htmlentitydefs HTMLParser sgmllib xmllib zlib gzip zipfile tarfile binascii base64 quopri uu unicodedata
warnings atexit new imp marshal code codeop dis pdb profile hotshot timeit unittest doctest getopt optparse cmd shlex
csv select asyncore asynchat platform distutils ftplib poplib imaplib smtplib telnetlib xmlrpclib calendar decimal
colorsys gettext textwrap difflib Tkinter'''.split())

EXE_CLASSES = {'CyPitboss', 'CyInterfaceScreen'}
EXE_FUNCS = {'NiTextOut', 'getChtLvl', 'setChtLvl', 'getWBToolNormalMapTabCtrl', 'getWBToolAdvancedStartTabCtrl',
             'getWBToolPlayerTabCtrl', 'getWBToolUnitTabCtrl', 'isMouseOverGameSurface', 'getWBSaveExtension'}
EXE_FUNC_RET = {
    'getWBToolNormalMapTabCtrl': ('inst', ('api', 'CyGTabCtrl')),
    'getWBToolAdvancedStartTabCtrl': ('inst', ('api', 'CyGTabCtrl')),
    'getWBToolPlayerTabCtrl': ('inst', ('api', 'CyGTabCtrl')),
    'getWBToolUnitTabCtrl': ('inst', ('api', 'CyGTabCtrl')),
    'getWBSaveExtension': ('inst', ('builtin', 'str')),
    'isMouseOverGameSurface': ('inst', ('builtin', 'bool')),
}

BUILTIN_CTOR_RET = {
    'str': 'str', 'unicode': 'str', 'chr': 'str', 'unichr': 'str', 'repr': 'str',
    'open': 'file', 'file': 'file',
    'list': 'list', 'range': 'list', 'xrange': 'list', 'sorted': 'list', 'zip': 'list', 'map': 'list', 'filter': 'list',
    'dict': 'dict', 'tuple': 'tuple', 'set': 'set', 'frozenset': 'set',
    'int': 'num', 'long': 'num', 'float': 'num', 'len': 'num', 'abs': 'num', 'ord': 'num', 'round': 'num', 'hash': 'num',
    'bool': 'bool',
}

BUILTIN_METHODS = {
    'str': set(dir(str)) | {'decode', 'encode'},
    'list': set(dir(list)),
    'dict': set(dir(dict)) | {'has_key', 'iteritems', 'iterkeys', 'itervalues', 'viewkeys', 'viewvalues', 'viewitems'},
    'tuple': set(dir(tuple)),
    'set': set(dir(set)),
    'file': {'read', 'readline', 'readlines', 'write', 'writelines', 'close', 'flush', 'seek', 'tell', 'truncate', 'next',
             'xreadlines', 'fileno', 'isatty'},
    'num': set(dir(int)) | set(dir(float)),
    'bool': set(dir(bool)),
}

STR_RET_STR = {'upper', 'lower', 'strip', 'lstrip', 'rstrip', 'replace', 'join', 'title', 'capitalize', 'swapcase',
               'zfill', 'center', 'ljust', 'rjust', 'expandtabs', 'encode', 'decode', 'translate'}
STR_RET_LIST = {'split', 'rsplit', 'splitlines'}
STR_RET_NUM = {'find', 'rfind', 'index', 'rindex', 'count'}
STR_RET_BOOL = {'startswith', 'endswith', 'isdigit', 'isalpha', 'isalnum', 'isspace', 'islower', 'isupper', 'istitle'}

CPP_STR_TYPES = {'CvWString', 'CvString', 'std::string', 'std::wstring', 'string', 'wstring', 'unicode',
                 'STRING', 'WSTRING', 'char', 'wchar_t', 'wchar', 'CvWStringBuffer'}

API_TUPLE_ITERS = {
    ('CyPlayer', 'firstCity'): 'CyCity',
    ('CyPlayer', 'nextCity'): 'CyCity',
    ('CyPlayer', 'firstUnit'): 'CyUnit',
    ('CyPlayer', 'nextUnit'): 'CyUnit',
    ('CyPlayer', 'firstSelectionGroup'): 'CySelectionGroup',
    ('CyPlayer', 'nextSelectionGroup'): 'CySelectionGroup',
}

TOKEN_RE = re.compile(r'\(\)|\[\d*\]|\.?[A-Za-z_]\w*|\$[A-Za-z_]\w*(?:<[^>]+>)?')


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
        # Homogeneous list appends: (module, scope, var) -> [arg expr]
        self.list_appends = collections.defaultdict(list)
        for r in read('py_calls.tsv'):
            if r['attribute'] == '1' and r['name'] == 'append' and r.get('recv') and r.get('args'):
                a = r['args'].split('|')
                if len(a) == 1 and a[0] and a[0] != '*' and '?' not in a[0]:
                    self.list_appends[(r['module'], r['caller'], r['recv'])].append(a[0])
        # C++ side
        self.pyclass_cpp = {r['python_class']: r['cpp_class'] for r in read('python_classes.tsv')}
        self.cpp_pyclass = {v: k for k, v in self.pyclass_cpp.items()}
        self.cpp_bases = {r['cpp_class']: [b for b in r['bases'].split(',') if b] for r in read('python_classes.tsv')}
        self.binds = collections.defaultdict(lambda: collections.defaultdict(list))   # cpp class -> name -> targets
        for r in read('python_bindings.tsv'):
            self.binds[r['cpp_class']][r['python_name']].append(r['target'].lstrip('&'))
        self.free_funcs = {}                              # python_name -> (cpp_target, doc_ret)
        for r in read('python_free_funcs.tsv'):
            self.free_funcs[r['python_name']] = (r['target'].lstrip('&'), r.get('returns', ''))
        self.enums = {r['python_name'] for r in read('python_enums.tsv')}
        self.ret = {r['function']: r['returns'] for r in read('function_returns.tsv')}
        self.api = collections.defaultdict(dict)          # class -> method -> returns (reference)
        self.api_by = {}
        for r in read('py_api.tsv'):
            self.api[r['class']][r['method']] = r['returns']
            self.api_by[r['class']] = r['bound_by']
        for ec in EXE_CLASSES:
            self.api_by.setdefault(ec, 'exe')
        self.api_names = set(self.pyclass_cpp) | set(self.api) | EXE_CLASSES
        self.bug_mods = {r['mod_id'] for r in read('py_bug_options.tsv')}
        self.memo = {}
        self.ptypes = {}                                  # (module, function) -> {parameter: type}
        vals = read('py_values.tsv')
        self.valued = {r['name'] for r in vals}
        self.valued_by_mod = {(r['module'], r['name']) for r in vals}
        self._screen_input_mod = self.mod_of.get('ScreenInput')
        self._gameutils_mod = self.mod_of.get('CvGameUtils')

    def type_parameters(self, calls, resolved):
        """One round: a parameter gets a type when every resolved call of its function passes that type."""
        bare_unresolved = {c['name'] for c, (how, t) in zip(calls, resolved)
                           if how in ('unresolved', 'py-only') and c['attribute'] == '0'}
        sites = collections.defaultdict(list)            # (module, function) -> [(offset, types, star)]
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
            is_method = '.' in q and self.defs[m].get(q.rsplit('.', 1)[0]) == 'class'
            if not is_method:
                if short in self.valued or short in bare_unresolved:
                    continue
            else:
                if short != '__init__' and (m, short) in self.valued_by_mod:
                    continue
            params = self.args.get((m, q), [])
            typed = {}
            for k, p in enumerate(params):
                if is_method and k == 0:
                    continue
                ts = []
                for offset, types, star in lst:
                    i = k - offset
                    if star or i < 0 or i >= len(types):
                        ts = None
                        break
                    ts.append(types[i])
                if ts:
                    t = self.same(ts)
                    if t is not None and t[0] in ('inst', 'pyclass', 'bug-opt'):
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
        """Value of a name in module m, scope."""
        key = ('L', m, scope, name)
        if key in self.memo:
            return self.memo[key]
        self.memo[key] = None
        v = self._lookup(m, scope, name, depth)
        self.memo[key] = v
        return v

    def _assign_type(self, m, s, name, depth):
        es = self.assign[(m, s, name)]
        vals = [self.eval(m, s, e, depth + 1) for e in es]
        t = self.same(vals, allow_partial=True)
        # Refine untyped $list from homogeneous var.append(x) calls in the same scope
        if t == ('inst', ('builtin', 'list')):
            apps = self.list_appends.get((m, s, name))
            if apps:
                et = self.same([self.eval(m, s, a, depth + 1) for a in apps], allow_partial=True)
                if et is not None and et[0] == 'inst':
                    return ('inst', ('list', et))
        return t

    def _lookup(self, m, scope, name, depth):
        for s in self.scopes(scope):
            if s != '<module>':
                if name in self.args.get((m, s), []):
                    parent = s.rsplit('.', 1)[0] if '.' in s else ''
                    if self.defs[m].get(parent) == 'class' and self.args[(m, s)][0] == name:
                        return ('inst', ('py', m, parent))   # the instance: first parameter of a method
                    pt = self.ptypes.get((m, s), {}).get(name)
                    if pt is not None:
                        return pt
                    # Standard Civ4 engine-dispatched callback parameter types
                    short = s.split('.')[-1]
                    if name == 'inputClass' and short == 'handleInput' and self._screen_input_mod:
                        return ('inst', ('py', self._screen_input_mod, 'ScreenInput'))
                    if name == 'popupReturn':
                        return ('inst', ('api', 'CyPopupReturn'))
                    if (m, s, name) in self.assign:
                        return self._assign_type(m, s, name, depth)
                    return None
                if (m, s, name) in self.assign:
                    return self._assign_type(m, s, name, depth)
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
            return self._assign_type(m, '<module>', name, depth)
        if name in BUILTINS:
            return ('builtin', name)
        return None

    def _cvpyext_member(self, name):
        if name in self.api_names:
            return ('apiclass', name)
        if name in self.free_funcs:
            return ('apifunc', name)
        if name in self.enums:
            return ('apienum', name)
        if name in EXE_FUNCS:
            return ('exefunc', name)
        return None

    def from_import(self, r, name, depth):
        if r['kind'] == 'import':
            bound = r['alias'] or r['source'].split('.')[0]
            if bound == name:
                return self.module(r['source'] if r['alias'] else r['source'].split('.')[0])
            return None
        src = r['source']
        top = src.split('.')[0]
        if r['name'] == '*':
            if src == 'CvPythonExtensions':
                return self._cvpyext_member(name)
            sm = self.mod_of.get(src.split('.')[-1])
            if sm and (self.defs[sm].get(name) or (sm, '<module>', name) in self.assign):
                return self.lookup(sm, '<module>', name, depth + 1)
            return None
        if (r['alias'] or r['name']) == name:
            if src == 'CvPythonExtensions':
                return self._cvpyext_member(r['name'])
            sm = self.mod_of.get(src.split('.')[-1])
            if sm:
                if self.defs[sm].get(r['name']) or (sm, '<module>', r['name']) in self.assign or \
                        any(x for x in self.imports.get((sm, '<module>'), [])):
                    v = self.lookup(sm, '<module>', r['name'], depth + 1)
                    if v is not None:
                        return v
                return self.module(src + '.' + r['name'])
            if top in STDLIB:
                if src in ('StringIO', 'cStringIO') and r['name'] == 'StringIO':
                    return ('stdlib-ctor', src + '.StringIO', 'file')
                return ('stdlib', src + '.' + r['name'])
        return None

    def module(self, dotted):
        if dotted == 'CvPythonExtensions':
            return ('module', 'CvPythonExtensions')
        p = self.mod_of.get(dotted.split('.')[-1])
        if p:
            return ('module', p)
        top = dotted.split('.')[0]
        if top in STDLIB:
            return ('stdlib', dotted)
        return None

    @staticmethod
    def same(vals, allow_partial=False):
        non_none = [v for v in vals if v != ('builtin', 'None')]
        if not non_none:
            return None
        s = set(non_none)
        if len(s) == 1 and None not in s:
            return s.pop()
        # If one value is a typed list ('inst', ('list', T)) and another is untyped ('inst', ('builtin', 'list')), prefer typed
        if None not in s and len(s) == 2 and ('inst', ('builtin', 'list')) in s:
            other = (s - {('inst', ('builtin', 'list'))}).pop()
            if other[0] == 'inst' and other[1][0] == 'list':
                return other
        if allow_partial:
            # Ignore unknown (None) branches and 0 ($num) null-pointer initializers if all known non-sentinel values
            # agree on a single object class (api/py) or file/str instance.
            known = {v for v in s if v is not None}
            obj_types = {v for v in known if v[0] == 'inst' and v[1][0] in ('api', 'py')}
            if len(obj_types) == 1 and all(v in obj_types or v == ('inst', ('builtin', 'num')) for v in known):
                return next(iter(obj_types))
            if len(known) == 1:
                only = next(iter(known))
                if only[0] == 'inst' and only[1][0] in ('api', 'py', 'list'):
                    return only
        return None

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
        if not e or '?' in e:
            return None
        ops = TOKEN_RE.findall(e)
        if ''.join(ops) != e or not ops or ops[0] in ('()', '[]') or ops[0].startswith('['):
            return None
        head = ops[0]
        if head.startswith('$'):
            v = self._eval_literal(m, scope, head, depth)
        else:
            v = self.lookup(m, scope, head, depth)
        for op in ops[1:]:
            if v is None:
                return None
            if op == '()':
                v = self.call(v)
            elif op.startswith('['):
                v = self.subscript(v, op)
            else:
                v = self.attr(v, op[1:], depth)
        return v

    def _eval_literal(self, m, scope, tok, depth):
        if tok == '$None':
            return ('builtin', 'None')
        if tok == '$str':
            return ('inst', ('builtin', 'str'))
        if tok == '$num':
            return ('inst', ('builtin', 'num'))
        if tok == '$bool':
            return ('inst', ('builtin', 'bool'))
        if tok == '$list':
            return ('inst', ('builtin', 'list'))
        if tok == '$dict':
            return ('inst', ('builtin', 'dict'))
        if tok == '$tuple':
            return ('inst', ('builtin', 'tuple'))
        if tok.startswith('$list<') and tok.endswith('>'):
            inner = tok[6:-1]
            et = self.eval(m, scope, inner, depth + 1)
            return ('inst', ('list', et)) if (et is not None and et[0] == 'inst') else ('inst', ('builtin', 'list'))
        return None

    def subscript(self, v, op):
        if v[0] == 'inst':
            inner = v[1]
            if inner[0] == 'list':
                return inner[1]
            if inner[0] == 'tuple':
                idx = op[1:-1]
                if idx.isdigit() and int(idx) < len(inner[1]):
                    return inner[1][int(idx)]
                return None
            if inner == ('builtin', 'str'):
                return ('inst', ('builtin', 'str'))
        if v[0] == 'stdlib':
            return v
        return None

    def call(self, v):
        k = v[0]
        if k == 'pyclass':
            return ('inst', ('py', v[1], v[2]))
        if k == 'apiclass':
            return ('inst', ('api', v[1]))
        if k == 'apifunc':
            return self.free_return(v[1])
        if k == 'apienum':
            return ('inst', ('builtin', 'num'))
        if k == 'exefunc':
            return EXE_FUNC_RET.get(v[1])
        if k == 'apimethod':
            return self.api_return(v[1], v[2])
        if k == 'builtin':
            bt = BUILTIN_CTOR_RET.get(v[1])
            return ('inst', ('builtin', bt)) if bt else None
        if k == 'builtin-method':
            bt, meth = v[1], v[2]
            if bt == 'str':
                if meth in STR_RET_STR: return ('inst', ('builtin', 'str'))
                if meth in STR_RET_LIST: return ('inst', ('list', ('inst', ('builtin', 'str'))))
                if meth in STR_RET_NUM: return ('inst', ('builtin', 'num'))
                if meth in STR_RET_BOOL: return ('inst', ('builtin', 'bool'))
            elif bt == 'list' and meth == 'pop' and len(v) > 3 and v[3] is not None:
                return v[3]
            elif bt == 'file' and meth in ('read', 'readline'):
                return ('inst', ('builtin', 'str'))
            elif bt == 'file' and meth == 'readlines':
                return ('inst', ('list', ('inst', ('builtin', 'str'))))
            return None
        if k == 'stdlib-ctor':
            return ('inst', ('builtin', v[2]))
        if k == 'stdlib':
            return ('stdlib', v[1] + '()')
        if k == 'pyfunc':                             # the type every non-None return statement of the function gives
            # Special case: CvGameInterface.gameUtils() / BugGameUtils.getDispatcher()
            if (v[1].endswith('CvGameInterface.py') and v[2] == 'gameUtils') or \
               (v[1].endswith('BugGameUtils.py') and v[2] == 'getDispatcher'):
                if self._gameutils_mod:
                    return ('inst', ('py', self._gameutils_mod, 'CvGameUtils'))
            key = ('R', v[1], v[2])
            if key in self.memo:
                return self.memo[key]
            self.memo[key] = None
            es = self.returns.get((v[1], v[2]), [])
            t = self.same([self.eval(v[1], v[2], e) for e in es], allow_partial=True) if es else None
            self.memo[key] = t
            return t
        return None

    def attr(self, v, a, depth):
        k = v[0]
        if k == 'module':
            if v[1] == 'CvPythonExtensions':
                return self._cvpyext_member(a)
            if v[1].endswith('BugCore.py') and a == 'game':
                return ('bug-game',)
            return self.lookup(v[1], '<module>', a, depth + 1)
        if k == 'bug-game':
            return ('bug-opt', a)
        if k == 'bug-opt':
            return ('bug-opt-method', v[1], a)
        if k == 'stdlib':
            if v[1] in ('StringIO', 'cStringIO') and a == 'StringIO':
                return ('stdlib-ctor', v[1] + '.StringIO', 'file')
            return ('stdlib', v[1] + '.' + a)
        if k == 'inst' and v[1][0] == 'api':
            return ('apimethod', v[1][1], a)
        if k == 'inst' and v[1][0] == 'builtin':
            bt = v[1][1]
            if a in BUILTIN_METHODS.get(bt, ()):
                return ('builtin-method', bt, a)
            return None
        if k == 'inst' and v[1][0] == 'list':
            if a in BUILTIN_METHODS['list']:
                return ('builtin-method', 'list', a, v[1][1])
            return None
        if k == 'inst' and v[1][0] == 'py':
            meth = self.py_method(v[1][1], v[1][2], a, depth)
            if meth:
                return ('pyfunc',) + meth
            t = self.py_attr(v[1][1], v[1][2], a, depth)
            if t is not None:
                return t
            nested = self.py_nested_class(v[1][1], v[1][2], a, depth)
            if nested:
                return ('pyclass',) + nested
            return None
        if k == 'pyclass':
            meth = self.py_method(v[1], v[2], a, depth)
            if meth:
                return ('pyfunc',) + meth
            nested = self.py_nested_class(v[1], v[2], a, depth)
            if nested:
                return ('pyclass',) + nested
            return self.py_attr(v[1], v[2], a, depth)
        return None

    def py_method(self, m, cls, name, depth, seen=None):
        """(module, qualname) of method name in Python class cls or its bases."""
        seen = seen or set()
        if (m, cls) in seen:
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

    def py_nested_class(self, m, cls, name, depth, seen=None):
        """(module, qualname) of nested class name inside Python class cls or its bases."""
        seen = seen or set()
        if (m, cls) in seen:
            return None
        seen.add((m, cls))
        if self.defs[m].get(cls + '.' + name) == 'class':
            return (m, cls + '.' + name)
        for b in self.bases.get((m, cls), []):
            bv = self.eval(m, '<module>', b, depth + 1)
            if bv and bv[0] == 'pyclass':
                r = self.py_nested_class(bv[1], bv[2], name, depth + 1, seen)
                if r:
                    return r
        return None

    def py_attr(self, m, cls, a, depth, seen=None):
        """Instance or class attribute of Python class cls, walking bases."""
        seen = seen or set()
        if (m, cls) in seen:
            return None
        seen.add((m, cls))
        vals = []
        for s, e in self.selfattr.get((m, cls, a), []):
            vals.append(self.eval(m, s, e, depth + 1))
        for e in self.assign.get((m, cls, a), []):
            vals.append(self.eval(m, cls, e, depth + 1))
        t = self.same(vals, allow_partial=True) if vals else None
        if t is not None:
            return t
        for b in self.bases.get((m, cls), []):
            bv = self.eval(m, '<module>', b, depth + 1)
            if bv and bv[0] == 'pyclass':
                r = self.py_attr(bv[1], bv[2], a, depth + 1, seen)
                if r is not None:
                    return r
        return None

    def _cpp_type_to_py(self, r):
        if not r:
            return None
        c = re.sub(r'\b(const|class|struct)\b|[*&]', '', r).strip()
        if c in self.cpp_pyclass:
            return ('inst', ('api', self.cpp_pyclass[c]))
        if c in self.api_names:
            return ('inst', ('api', c))
        if c in CPP_STR_TYPES:
            return ('inst', ('builtin', 'str'))
        return None

    def free_return(self, name):
        tgt, doc_ret = self.free_funcs.get(name, ('', ''))
        if tgt in self.ret:
            v = self._cpp_type_to_py(self.ret[tgt])
            if v is not None:
                return v
        return self._cpp_type_to_py(doc_ret)

    def api_return(self, cls, meth):
        """Type of the result of C++-side method cls.meth: the declared return type of the bound C++ function,
        else the class reference's."""
        if (cls, meth) in API_TUPLE_ITERS:
            return ('inst', ('tuple', (('inst', ('api', API_TUPLE_ITERS[(cls, meth)])), ('inst', ('builtin', 'num')))))
        for t in self.api_targets(cls, meth):
            r = self.ret.get(t)
            if r:
                return self._cpp_type_to_py(r)
        r = self.api.get(cls, {}).get(meth)
        if r:
            return self._cpp_type_to_py(r)
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
        if k == 'apifunc':
            return 'cpp', self.free_funcs[v[1]][0]
        if k == 'apienum':
            return 'api-enum', v[1]
        if k == 'exefunc':
            return 'exe', v[1]
        if k == 'builtin':
            return 'builtin', v[1]
        if k == 'builtin-method':
            return 'builtin', '%s.%s' % (v[1], v[2])
        if k in ('stdlib', 'stdlib-ctor'):
            return 'stdlib', v[1]
        if k == 'bug-opt-method':
            return 'bug-option', '%s.%s' % (v[1], v[2])
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
                if t[0] == 'inst':
                    lbl = t[1][1] if t[1][0] in ('api', 'builtin') else ('list<%s>' % (t[1][1][1],) if t[1][0] == 'list' else '%s:%s' % (t[1][1], t[1][2]))
                elif t[0] == 'pyclass':
                    lbl = 'class %s:%s' % (t[1], t[2])
                else:
                    lbl = str(t)
                o.write('%s\t%s\t%s\t%s\n' % (m, q, p, lbl))
    with open(os.path.join(M, 'py_resolved.tsv'), 'w', encoding='utf-8') as o:
        o.write('module\tcaller\tname\tattribute\tline\trecv\thow\ttarget\n')
        for r in rows:
            o.write('\t'.join(r) + '\n')
    print('%d calls: %s' % (len(rows), ', '.join('%s %d' % kv for kv in count.most_common())))


if __name__ == '__main__':
    # No depth cap: cycles end at the memo (a key being resolved reads as unknown) and at `seen` for class
    # bases, so a chain is followed as far as it goes. A large stack lets deep chains recurse.
    import threading
    sys.setrecursionlimit(1000000)
    threading.stack_size(512 * 1024 * 1024)
    t = threading.Thread(target=main)
    t.start()
    t.join()
