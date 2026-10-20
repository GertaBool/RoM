# Run by the game's own Python 2.4 (under Wine): parse the mod's Python with Python 2.4's compiler package
# and write its functions, calls and event-handler registrations. Written in Python 2.4.
# usage: python.exe py24_scan.py <file list> <out dir>
#   file list: one line per module: <name as shown in the map> TAB <path to the .py file>
# Writes py_functions.tsv (module, name, kind, line), py_calls.tsv (module, caller, name, attribute, line),
# py_handlers.tsv (module, caller, event, handler, line) for addEventHandler("event", handler) calls, and
# py_errors.tsv (module, error) for files Python 2.4 itself cannot parse.
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


class Scan:
    def __init__(self, module, out):
        self.module, self.out, self.stack = module, out, []

    def caller(self):
        if self.stack: return '.'.join(self.stack)
        return '<module>'

    def visit(self, node):
        if isinstance(node, ast.Function) or isinstance(node, ast.Class):
            kind = 'def'
            if isinstance(node, ast.Class): kind = 'class'
            self.stack.append(node.name)
            self.out['f'].append((self.module, '.'.join(self.stack), kind, node.lineno))
            for c in node.getChildNodes(): self.visit(c)
            self.stack.pop()
            return
        if isinstance(node, ast.CallFunc):
            f = node.node
            if isinstance(f, ast.Name):
                self.out['c'].append((self.module, self.caller(), f.name, 0, node.lineno))
            elif isinstance(f, ast.Getattr):
                self.out['c'].append((self.module, self.caller(), f.attrname, 1, node.lineno))
                if f.attrname == 'addEventHandler' and len(node.args) >= 2 and isinstance(node.args[0], ast.Const):
                    self.out['h'].append((self.module, self.caller(), node.args[0].value,
                                          dotted(node.args[1]) or '?', node.lineno))
        for c in node.getChildNodes(): self.visit(c)


def main():
    files, outdir = sys.argv[1], sys.argv[2]
    out = {'f': [], 'c': [], 'h': [], 'e': []}
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
                              ('c', 'py_calls_raw.tsv', 'module\tcaller\tname\tattribute\tline'),
                              ('h', 'py_handlers.tsv', 'module\tcaller\tevent\thandler\tline'),
                              ('e', 'py_errors.tsv', 'module\terror')):
        o = open(outdir + '\\' + name, 'w')
        o.write(header + '\n')
        for r in out[key]: o.write('\t'.join([str(x) for x in r]) + '\n')
        o.close()

main()
