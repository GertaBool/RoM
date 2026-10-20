#!/usr/bin/env python3
"""Query the code map (codemap/map/*.tsv).

usage: query.py find <regex>              functions whose Scope::name matches
       query.py callees <function> [depth]  what it calls, as a tree (default depth 1)
       query.py callers <function> [depth]  who calls it, as a tree
       query.py path <from> <to>          a shortest call path between two functions
A function is given as an id, as Scope::name, or as a regex matching exactly one Scope::name.
Virtual calls are followed into the overriding methods of the object's class and its subclasses.
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
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'find':
        for i in F:
            if re.search(args[0], name[i]): print(f"{i}\t{name[i]}\t{F[i]['file']}:{F[i]['line']}")
    elif cmd in ('callees', 'callers'):
        tree(resolve(args[0]), down if cmd == 'callees' else up, int(args[1]) if len(args) > 1 else 1)
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
