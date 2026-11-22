# Run by the game's own Python 2.4 (under Wine): parse the mod's Python with Python 2.4's compiler package
# and write its functions, calls and event-handler registrations, and the facts py_resolve.py needs to resolve
# calls as Python does. Written in Python 2.4.
# usage: python.exe py24_scan.py <file list> <out dir>
#   file list: one line per module: <name as shown in the map> TAB <path to the .py file>
# Writes
#   py_functions.tsv  (module, name, kind, line)
#   py_calls_raw.tsv  (module, caller, name, attribute, line, recv): recv is the receiver of x.f() written as an
#                     expression: gc.getPlayer(i).getCity(j).getOwner() has recv gc.getPlayer().getCity()
#   py_handlers.tsv   (module, caller, event, handler, line) for addEventHandler("event", handler) calls
#   py_assign.tsv     (module, scope, target, expr, line): x = expr and self.x = expr (one target name only)
#   py_imports.tsv    (module, scope, kind, source, name, alias, line): import X [as Y]; from X import a [as b], *
#   py_classes.tsv    (module, class, bases, line)
#   py_args.tsv       (module, function, args): parameter names, comma-separated
#   py_returns.tsv    (module, function, expr): the expression of each return statement
#   py_values.tsv     (module, scope, name): a name used as a value (passed, assigned, stored, returned),
#                     not called; py_calls_raw's args column holds the positional argument expressions
#                     separated by |, and * when keyword or star arguments are passed
#   py_errors.tsv     (module, error) for files Python 2.4 itself cannot parse.
import sys, compiler
from compiler import ast


def dotted(node):
    # the written name of a called expression: f, x.f, self.x.f
    if isinstance(node, ast.Name): return node.name
    if isinstance(node, ast.Getattr):
        inner = dotted(node.expr)
        if inner: return inner + '.' + node.attrname
        return '?.' + node.attrname
    return None


def expr(node):
    # an expression as the resolver reads it: names, attributes and calls; anything else is ?
    if isinstance(node, ast.Name): return node.name
    if isinstance(node, ast.Getattr): return expr(node.expr) + '.' + node.attrname
    if isinstance(node, ast.CallFunc): return expr(node.node) + '()'
    return '?'


class Scan:
    def __init__(self, module, out):
        self.module, self.out, self.stack = module, out, []

    def caller(self):
        if self.stack: return '.'.join(self.stack)
        return '<module>'

    def visit(self, node):
        if isinstance(node, ast.Function) or isinstance(node, ast.Class):
            kind = 'def'
            if isinstance(node, ast.Class):
                kind = 'class'
                self.out['k'].append((self.module, '.'.join(self.stack + [node.name]),
                                      ','.join([expr(b) for b in node.bases]), node.lineno))
            self.stack.append(node.name)
            self.out['f'].append((self.module, '.'.join(self.stack), kind, node.lineno))
            if kind == 'def':
                self.out['p'].append((self.module, '.'.join(self.stack), ','.join([str(a) for a in node.argnames])))
            for c in node.getChildNodes(): self.visit(c)
            self.stack.pop()
            return
        if isinstance(node, ast.CallFunc):
            f = node.node
            pos = []
            kw = 0
            for a in node.args:
                if isinstance(a, ast.Keyword): kw = 1
                else: pos.append(expr(a))
            if kw or node.star_args is not None or node.dstar_args is not None: pos.append('*')
            args = '|'.join(pos)
            if isinstance(f, ast.Name):
                self.out['c'].append((self.module, self.caller(), f.name, 0, node.lineno, '', args))
            elif isinstance(f, ast.Getattr):
                self.out['c'].append((self.module, self.caller(), f.attrname, 1, node.lineno, expr(f.expr), args))
                if f.attrname == 'addEventHandler' and len(node.args) >= 2 and isinstance(node.args[0], ast.Const):
                    self.out['h'].append((self.module, self.caller(), node.args[0].value,
                                          dotted(node.args[1]) or '?', node.lineno))
            # names used as values (callbacks): the function's callers are then not all known
            for a in node.args:
                if isinstance(a, ast.Keyword): a = a.expr
                if isinstance(a, ast.Name): self.out['v'].append((self.module, self.caller(), a.name))
                elif isinstance(a, ast.Getattr): self.out['v'].append((self.module, self.caller(), a.attrname))
        if isinstance(node, ast.Assign) or isinstance(node, ast.Dict) or isinstance(node, ast.List) or isinstance(node, ast.Tuple) \
                or isinstance(node, ast.Return):
            vals = []
            if isinstance(node, ast.Assign): vals = [node.expr]
            elif isinstance(node, ast.Dict): vals = [v for k, v in node.items]
            elif isinstance(node, ast.Return): vals = [node.value]
            else: vals = node.nodes
            for a in vals:
                if isinstance(a, ast.Name): self.out['v'].append((self.module, self.caller(), a.name))
                elif isinstance(a, ast.Getattr): self.out['v'].append((self.module, self.caller(), a.attrname))
        if isinstance(node, ast.Assign) and len(node.nodes) == 1:
            t = node.nodes[0]
            if isinstance(t, ast.AssName):
                self.out['a'].append((self.module, self.caller(), t.name, expr(node.expr), node.lineno))
            elif isinstance(t, ast.AssAttr) and isinstance(t.expr, ast.Name):
                self.out['a'].append((self.module, self.caller(), t.expr.name + '.' + t.attrname, expr(node.expr), node.lineno))
        if isinstance(node, ast.Return) and node.value is not None:
            self.out['r'].append((self.module, self.caller(), expr(node.value)))
        if isinstance(node, ast.Import):
            for name, alias in node.names:
                self.out['i'].append((self.module, self.caller(), 'import', name, '', alias or '', node.lineno))
        if isinstance(node, ast.From):
            for name, alias in node.names:
                self.out['i'].append((self.module, self.caller(), 'from', node.modname, name, alias or '', node.lineno))
        for c in node.getChildNodes(): self.visit(c)


def main():
    files, outdir = sys.argv[1], sys.argv[2]
    out = {'f': [], 'c': [], 'h': [], 'e': [], 'a': [], 'i': [], 'k': [], 'p': [], 'r': [], 'v': []}
    for line in open(files).read().split('\n'):
        if not line.strip(): continue
        module, path = line.split('\t')
        try:
            tree = compiler.parseFile(path)
        except Exception, e:
            out['e'].append((module, str(e).replace('\t', ' ').replace('\n', ' ')))
            continue
        Scan(module, out).visit(tree)
    for key, name, header in (('f', 'py_functions.tsv', 'module\tname\tkind\tline'),
                              ('c', 'py_calls_raw.tsv', 'module\tcaller\tname\tattribute\tline\trecv\targs'),
                              ('h', 'py_handlers.tsv', 'module\tcaller\tevent\thandler\tline'),
                              ('a', 'py_assign.tsv', 'module\tscope\ttarget\texpr\tline'),
                              ('i', 'py_imports.tsv', 'module\tscope\tkind\tsource\tname\talias\tline'),
                              ('k', 'py_classes.tsv', 'module\tclass\tbases\tline'),
                              ('p', 'py_args.tsv', 'module\tfunction\targs'),
                              ('r', 'py_returns.tsv', 'module\tfunction\texpr'),
                              ('v', 'py_values.tsv', 'module\tscope\tname'),
                              ('e', 'py_errors.tsv', 'module\terror')):
        o = open(outdir + '\\' + name, 'w')
        o.write(header + '\n')
        for r in out[key]: o.write('\t'.join([str(x).replace('\t', ' ') for x in r]) + '\n')
        o.close()

main()
