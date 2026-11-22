#!/usr/bin/env python3
"""Where a value comes from and where it goes, read from the code graph (graph.py) only.

usage: flow.py --src <checkout> member <Class::m_x> [--depth N]     who writes a member, and the call chains above
                                                                       each writer up to the decisions that start them
       flow.py --src <checkout> callers <Scope::name> [--depth N]   who calls a function (C++ and Python), as a tree
       flow.py --src <checkout> readers <Scope::name|Class::m_x>    every function reading a member or calling a
                                                                       value function, one level, with file:line
       flow.py --src <checkout> paths <from regex> <to Scope::name> [--depth N]
                                                                     every call chain from functions matching <from>
                                                                       down to <to>, up to N calls long

The graph is required, and it must describe the code being analysed: --src names the checkout, and the tool
stops (exit 2) unless the map was built from that checkout's HEAD (codemap/skeleton.md) with no uncommitted
change in its DLL or Python folders. A question about other code needs the map rebuilt first
(codemap/tool/build.sh). Nothing here reads the source: every edge is a graph edge (call, py>cpp, read, writes),
so an answer is as complete as the map.

Everything is listed; --depth narrows the chains and says so.
"""
import argparse, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def require_fresh(src):
    import impact
    built = impact.map_commit()
    head = subprocess.run(['git', '-C', src, 'rev-parse', '--short=12', 'HEAD'], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git', '-C', src, 'status', '--porcelain', '--untracked-files=no', '--',
                            'Assets/CvGameCoreDLL', 'Assets/Python'], capture_output=True, text=True).stdout.strip()
    skeleton = open(os.path.join(HERE, '..', 'skeleton.md'), encoding='utf-8').read()
    problems = []
    if not head:
        problems.append(f'{src} is not a git checkout')
    elif not built or not (head.startswith(built) or built.startswith(head)):
        problems.append(f'the map was built from {built or "an unknown commit"}, the checkout is at {head}')
    if dirty:
        problems.append(f'{src} has uncommitted changes in Assets/CvGameCoreDLL or Assets/Python')
    if 'with uncommitted changes' in skeleton.split('\n', 4)[2] if skeleton.count('\n') > 2 else False:
        problems.append('the map itself was built from uncommitted changes')
    if problems:
        sys.exit('flow.py: the graph does not describe this code: ' + '; '.join(problems) +
                 '. Rebuild it: codemap/tool/build.sh ' + src + ' ...')
    return built


def label(g, n):
    i = g.info.get(n, {})
    where = f'{i.get("file")}:{i.get("line")}' if i.get('file') else ''
    tags = []
    if i.get('exported'): tags.append('exe calls it')
    if i.get('bound'): tags.append('bound for Python')
    return f'{i.get("label", n)}  {where}' + (f'  [{", ".join(tags)}]' if tags else '')


def callers_of(g, n):
    """Callers of a function node: C++ calls and resolved Python calls (graph dep edges, which point from a
    function to what a change of it reaches)."""
    return sorted(b for b, link in g.dep.get(n, {}).items() if link == 'call' or link.startswith('py>'))


def nodes_for(g, name):
    if '::m_' in name or name.startswith('m_'):
        n = 'm:' + name
        if n not in g.info and n not in g.dep:
            sys.exit(f'flow.py: no member {name} in the graph')
        return [n]
    scope, _, nm = name.rpartition('::')
    import graph as G
    ids = g.by_key.get(G.key(scope, nm), [])
    if not ids:
        sys.exit(f'flow.py: no function {name} in the graph')
    return ids


def tree(g, roots, depth, out):
    shown, cut = set(), 0
    def walk(n, d, seen):
        nonlocal cut
        for c in callers_of(g, n):
            if c in seen:
                continue
            out.append('  ' * d + '<- ' + label(g, c))
            if d >= depth:
                if callers_of(g, c): cut += 1
                continue
            if c in shown:
                out.append('  ' * (d + 1) + '(callers listed above)')
                continue
            shown.add(c)
            walk(c, d + 1, seen | {c})
    for r in roots:
        out.append(label(g, r))
        walk(r, 1, {r})
    if cut:
        out.append(f'(--depth {depth}: {cut} chains continue above this depth)')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--src', required=True)
    ap.add_argument('--depth', type=int, default=6)
    ap.add_argument('cmd', choices=['member', 'callers', 'readers', 'paths'])
    ap.add_argument('args', nargs='+')
    a = ap.parse_args()
    built = require_fresh(os.path.abspath(a.src))
    import graph as G
    g = G.Graph()
    out = [f'(graph of {built})']
    if a.cmd == 'member':
        m = nodes_for(g, a.args[0])[0]
        writers = sorted(f for f, ms in g.writes.items() if m in ms)
        out.append(f'{a.args[0]}: {len(writers)} functions write it')
        tree(g, writers, a.depth, out)
    elif a.cmd == 'callers':
        tree(g, nodes_for(g, a.args[0]), a.depth, out)
    elif a.cmd == 'readers':
        for n in nodes_for(g, a.args[0]):
            rs = sorted(b for b, link in g.dep.get(n, {}).items() if link in ('read', 'call') or link.startswith('py>'))
            out.append(f'{label(g, n)}: {len(rs)}')
            out += ['  <- ' + label(g, r) for r in rs]
    elif a.cmd == 'paths':
        rx = re.compile(a.args[0])
        target = nodes_for(g, a.args[1])
        paths = []
        def up(n, chain):
            if len(chain) > a.depth:
                return
            if rx.search(g.info.get(n, {}).get('label', '')) and len(chain) > 1:
                paths.append(list(reversed(chain)))
            for c in callers_of(g, n):
                if c not in chain:
                    up(c, chain + [c])
        for t in target:
            up(t, [t])
        out.append(f'{len(paths)} chains from /{a.args[0]}/ to {a.args[1]} (at most {a.depth} calls)')
        for p in paths:
            out.append('  ' + ' -> '.join(g.info[n]['label'] for n in p))
    print('\n'.join(out))


if __name__ == '__main__':
    main()
