#!/usr/bin/env python3
"""Write codemap/graph.html: the whole map (graph.py) in one self-contained page.

usage: graph_html.py [<out.html>]

Views:
  Files    every C++ source file, Python module and loaded XML file as a node, linked by the C++ calls between
           files, Python calls into C++ and C++ calls into Python (event handlers included), Python calls
           between modules, and XML files to the C++ files whose functions read the members they fill.
  Impact   search any C++ or Python function, member, XML tag, define or file: what a change of it reaches,
           level by level, across C++, Python, members, XML and defines, each node with the link it came by.
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render
import graph as GR

out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'graph.html')
g = GR.Graph()
KIND = ['cpp', 'new', 'py', 'member', 'tag', 'define']
LINK = ['call', 'py>cpp', 'py>py', 'cpp>py', 'event', 'read', 'fill', 'define', 'writes', 'call (name match)',
        'py>cpp (only target)', 'py>py (only target)', 'py>cpp (name match)', 'py>py (name match)']
groups = [x for x, _ in render.GROUPS] + ['Python']
ids = sorted(g.info, key=lambda n: (KIND.index(g.info[n]['kind']), g.info[n]['label']))
ix = {n: k for k, n in enumerate(ids)}
files, fx = [], {}


def fi(f):
    if f not in fx:
        fx[f] = len(files)
        files.append(f)
    return fx[f]


K, L, F, LN, GP, FL = [], [], [], [], [], []
extra = {}
for n in ids:
    i = g.info[n]
    k = i['kind']
    K.append(KIND.index(k))
    L.append(i['label'].split(' ', 1)[1] if k == 'py' else i['label'])
    F.append(fi(i.get('file', '')))
    LN.append(i.get('line', 0))
    GP.append(groups.index(render.group(i['file'])) if k in ('cpp', 'new') and i['file'] else (len(groups) - 1 if k == 'py' else -1))
    FL.append((1 if i.get('exported') else 0) | (2 if i.get('bound') else 0) | (4 if i.get('saved') else 0))
    if k == 'member':
        extra[ix[n]] = dict(type=i['type'], xml=[[t, [[r['file'], r['layer'], int(r['loaded'])] for r in rows], known]
                                                 for t, (rows, known) in sorted(i.get('xml', {}).items())])
    elif k == 'tag':
        extra[ix[n]] = dict(files=[[r['file'], r['layer'], int(r['loaded']), int(r['count'])] for r in i['files']])
    elif k == 'define':
        extra[ix[n]] = dict(files=[[r['file'], r['layer'], int(r['loaded'])] for r in i['files']])
    elif k == 'py' and i.get('events'):
        extra[ix[n]] = dict(events=sorted(i['events']))
D = {}
for a, deps in g.dep.items():
    if a in ix:
        flat = []
        for b, link in deps.items():
            if b in ix:
                flat += [ix[b], LINK.index(link)]
        if flat:
            D[ix[a]] = flat
W = {ix[a]: sorted(ix[m] for m in ms if m in ix) for a, ms in g.writes.items() if a in ix and ms}

# the file graph: C++ files, Python modules, loaded XML files
fnode, fkind = {}, []


def fnode_of(name, kind):
    if (name, kind) not in fnode:
        fnode[(name, kind)] = len(fkind)
        fkind.append([name, kind, groups.index(render.group(name)) if kind == 'cpp' else (len(groups) - 1 if kind == 'py' else -1), 0])
    return fnode[(name, kind)]


for n in ids:
    i = g.info[n]
    if i['kind'] in ('cpp', 'py') and i['file']:
        fkind[fnode_of(i['file'], i['kind'])][3] += 1
fe = collections.Counter()
for a, deps in g.dep.items():
    ia = g.info.get(a)
    if not ia:
        continue
    for b, link in deps.items():
        ib = g.info.get(b)
        if not ib:
            continue
        if ia['kind'] in ('cpp', 'py') and ib['kind'] in ('cpp', 'py') and ia['file'] and ib['file'] and ia['file'] != ib['file']:
            # b depends on a: b's file calls into a's file
            fe[(fnode_of(ib['file'], ib['kind']), fnode_of(ia['file'], ia['kind']), link)] += 1
        elif ia['kind'] == 'member' and ib['kind'] in ('cpp', 'new') and ib['file']:
            for t, (rows, known) in ia.get('xml', {}).items():
                for r in rows:
                    if r['loaded'] == '1':
                        fe[(fnode_of(ib['file'], 'cpp'), fnode_of(r['file'], 'xml'), 'xml')] += 1
agg = collections.defaultdict(lambda: [0, set()])
for (a, b, link), c in fe.items():
    agg[(a, b)][0] += c
    agg[(a, b)][1].add(link)
file_edges = [[a, b, c, sorted(ls)] for (a, b), (c, ls) in agg.items()]

meta = open(os.path.join(HERE, '..', 'map', 'syntax_meta.tsv')).read().strip().split('\n')[-1]
data = dict(kinds=KIND, links=LINK, groups=groups, files=files, K=K, L=L, F=F, LN=LN, GP=GP, FL=FL, D=D, W=W,
            extra=extra, fnodes=fkind, fedges=file_edges, commit=meta)
blob = json.dumps(data, separators=(',', ':'))
with open(os.path.join(HERE, 'graph_template.html'), encoding='utf-8') as h:
    page = h.read().replace('/*DATA*/null', blob)
with open(out_path, 'w', encoding='utf-8') as h:
    h.write(page)
c = collections.Counter(K)
print('wrote %s (%.1f MB): %s; %d dependency links; file graph %d nodes, %d links' % (
    out_path, len(page) / 1e6, ', '.join('%s %d' % (KIND[k], v) for k, v in sorted(c.items())),
    sum(len(v) // 2 for v in D.values()), len(fkind), len(file_edges)))
