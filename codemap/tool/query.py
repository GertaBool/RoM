#!/usr/bin/env python3
"""Query the code map (codemap/map/*.tsv).

usage: query.py find <regex>              functions whose Scope::name matches
       query.py callees <function> [depth]  what it calls, as a tree (default depth 1)
       query.py callers <function> [depth]  who calls it, as a tree
       query.py path <from> <to>          a shortest call path between two functions
       query.py rank [n]                  the n functions (default 12) that rank above the most others
A function is given as an id, as Scope::name, or as a regex matching exactly one Scope::name.
Virtual calls are followed into the overriding methods of the object's class and its subclasses.
rank: function A ranks above B when every call path from outside the DLL into B passes through A (A
dominates B). Calls from outside enter at every function the exe or Python can call: exported functions,
functions bound for Python, and functions with no caller in the DLL. A function's rank is the number of
functions it dominates; it is shown under the function that dominates it most closely.
"""
import collections, csv, os, re, sys

M = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'map')


def read(n):
    with open(os.path.join(M, n), encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


F = {int(r['id']): r for r in read('functions.tsv')}
name = {i: (r['scope'] + '::' if r['scope'] else '') + r['sig'] for i, r in F.items()}
down, up = collections.defaultdict(list), collections.defaultdict(list)
objcls = collections.defaultdict(set)   # (caller, callee) of a virtual call -> the object's class, '' if not known
for c in read('calls.tsv'):
    a, b = int(c['caller']), int(c['callee'])
    if b not in down[a]: down[a].append(b)
    if a not in up[b]: up[b].append(a)
    if c['kind'] == 'virtual': objcls[(a, b)].add(c['object_class'])
direct = collections.defaultdict(set)
for o in read('overrides.tsv'): direct[int(o['overrides'])].add(int(o['method']))
parents = collections.defaultdict(set)
for r in read('bases.tsv'): parents[r['class']].add(r['base'])


def ancestors(c, seen=None):
    seen = {c} if seen is None else seen
    for p in parents.get(c, ()):
        if p not in seen: seen.add(p); ancestors(p, seen)
    return seen


def overriders(b, seen=None):   # every method that may run for a call to b, overrides of overrides included
    seen = set() if seen is None else seen
    for m in direct.get(b, ()):
        if m not in seen: seen.add(m); overriders(m, seen)
    return seen


for (a, b), cls in list(objcls.items()):   # a virtual call may reach the overrides in the object's class and below
    for m in sorted(overriders(b)):
        if '' in cls or cls & ancestors(F[m]['scope']):
            if m not in down[a]: down[a].append(m); up[m].append(a)


def dominators():
    """The immediate dominator of every function reached from outside the DLL (0: entered from outside)."""
    py = {int(r['function']) for r in read('python_defs.tsv')}
    defs = [i for i in F if F[i]['definition'] == '1']
    succ = {0: sorted(i for i in defs if not up[i] or F[i]['exported'] == '1' or i in py)}
    order, seen, stack = [], {0}, [(0, iter(succ[0]))]
    while stack:   # reverse postorder, iteratively
        n, it = stack[-1]
        for m in it:
            if m not in seen: seen.add(m); stack.append((m, iter(down[m]))); break
        else: stack.pop(); order.append(n)
    rpo = order[::-1]; pos = {n: k for k, n in enumerate(rpo)}
    preds = collections.defaultdict(list)
    for n in rpo:
        for m in (succ[0] if n == 0 else down[n]): preds[m].append(n)
    idom = {0: 0}

    def meet(a, b):
        while a != b:
            while pos[a] > pos[b]: a = idom[a]
            while pos[b] > pos[a]: b = idom[b]
        return a
    changed = True
    while changed:   # Cooper, Harvey and Kennedy, "A simple, fast dominance algorithm" (2001)
        changed = False
        for n in rpo[1:]:
            ps = [p for p in preds[n] if p in idom]
            new = ps[0]
            for p in ps[1:]: new = meet(p, new)
            if idom.get(n) != new: idom[n] = new; changed = True
    kids = collections.defaultdict(list)
    for n, d in idom.items():
        if n: kids[d].append(n)
    size = {}
    for n in reversed(rpo): size[n] = 1 + sum(size[k] for k in kids[n])
    return idom, {n: size[n] - 1 for n in size if n}


def rank(n=12):
    """The n functions that dominate the most others, with their immediate dominators."""
    idom, size = dominators()
    top = sorted(size, key=lambda i: (-size[i], i))[:n]
    return [(i, size[i], idom[i]) for i in top]


def resolve(q):
    if q.isdigit(): return int(q)
    exact = [i for i, r in F.items() if (r['scope'] + '::' if r['scope'] else '') + r['name'] == q and r['definition'] == '1']
    if len(exact) == 1: return exact[0]
    hits = exact or [i for i in F if re.search(q, name[i])]
    if len(hits) == 1: return hits[0]
    for i in hits[:40]: print(f"{i}\t{name[i]}\t{F[i]['file']}:{F[i]['line']}")
    sys.exit(f'{len(hits)} functions match {q!r}; give one id')


def tree(i, g, depth, d=0, seen=()):
    print('  ' * d + f"{name[i]}  [{i}] {F[i]['file']}:{F[i]['line']}")
    if d < depth:
        for j in g[i]:
            if j not in seen: tree(j, g, depth, d + 1, seen + (i,))


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'find':
        for i in F:
            if re.search(args[0], name[i]): print(f"{i}\t{name[i]}\t{F[i]['file']}:{F[i]['line']}")
    elif cmd in ('callees', 'callers'):
        tree(resolve(args[0]), down if cmd == 'callees' else up, int(args[1]) if len(args) > 1 else 1)
    elif cmd == 'rank':
        top = rank(int(args[0]) if args else 12)
        chosen = {i for i, _, _ in top}
        idom, _ = dominators()

        def above(i):   # the closest chosen function that dominates i, 0 if none
            d = idom[i]
            while d and d not in chosen: d = idom[d]
            return d
        kids = collections.defaultdict(list)
        for i, s, _ in top: kids[above(i)].append((i, s))

        def show(i, s, d):
            print('  ' * d + f"{name[i]}  [{i}] dominates {s}  {F[i]['file']}:{F[i]['line']}")
            for j, t in kids[i]: show(j, t, d + 1)
        for i, s in kids[0]: show(i, s, 0)
    elif cmd == 'path':
        a, b = resolve(args[0]), resolve(args[1])
        prev, q = {a: None}, collections.deque([a])
        while q and b not in prev:
            x = q.popleft()
            for y in down[x]:
                if y not in prev: prev[y] = x; q.append(y)
        if b not in prev: sys.exit('no call path')
        p = [b]
        while prev[p[-1]] is not None: p.append(prev[p[-1]])
        for i in reversed(p): print(f"{name[i]}  [{i}] {F[i]['file']}:{F[i]['line']}")
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
