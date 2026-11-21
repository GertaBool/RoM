#!/usr/bin/env python3
"""Write codemap/graph.html: one self-contained page to browse the map and see what a change reaches.

usage: graph_html.py [<out.html>]

It reads only codemap/map/*.tsv (the compiler map and the syntactic layer from syntax.py) and embeds them.
Views:
  Files    every source file as a node, coloured by group (render.py's rules), linked by the calls between
           them; click a file for its neighbours, functions and members.
  Impact   search a function, member variable, XML tag, global define or file: the item on the right, its
           callers level by level to the left (compiler call graph, overrides followed as in query.py),
           with counts per level, the files reached, and the exits (exe, Python).
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import query as Q
import render
from impact import read, exported, py_bound, py_callers, xml_files, define_file

out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'graph.html')

ids = sorted(i for i, r in Q.F.items() if r['definition'] == '1')
ix = {i: k for k, i in enumerate(ids)}
files = sorted({Q.F[i]['file'] for i in ids})
fx = {f: k for k, f in enumerate(files)}
groups = [g for g, _ in render.GROUPS]
fn = []
for i in ids:
    r = Q.F[i]
    flags = (1 if i in exported else 0) | (2 if i in py_bound else 0)
    fn.append([(r['scope'] + '::' if r['scope'] else '') + r['name'], fx[r['file']], int(r['line'] or 0), flags])
up = [sorted(ix[c] for c in Q.up.get(i, ()) if c in ix) for i in ids]
pymods = sorted({m for i in ids for m in py_callers.get(i, ())})
pmx = {m: k for k, m in enumerate(pymods)}
py = {ix[i]: sorted(pmx[m] for m in py_callers[i]) for i in ids if i in py_callers}

fe = collections.Counter()
for i in ids:
    for c in Q.up.get(i, ()):
        if c in ix and Q.F[c]['file'] != Q.F[i]['file']:
            fe[(fx[Q.F[c]['file']], fx[Q.F[i]['file']])] += 1
file_edges = [[a, b, n] for (a, b), n in fe.items()]

name_ix = collections.defaultdict(list)
for k, r in enumerate(fn):
    name_ix[r[0]].append(k)
sf = {}   # syntactic function name -> string index


def sfi(name):
    if name not in sf:
        sf[name] = len(sf)
    return sf[name]


fields = read('fields.tsv')
fk = {(r['cls'], r['field']): k for k, r in enumerate(fields)}
acc = collections.defaultdict(list)
KIND = {'read': 0, 'write': 1, 'ref': 2, 'call': 3}
for a in read('field_access.tsv'):
    for c in a['cls'].split(','):
        if (c, a['field']) in fk:
            acc[fk[(c, a['field'])]].append([sfi(a['function']), KIND[a['kind']]])
fill = collections.defaultdict(set)
for s in read('field_strings.tsv'):
    if 'XmlVal' in s['call'] or 'TagPair' in s['call'] or s['call'].startswith(('Set', 'Get')):
        for c in s['cls'].split(','):
            if (c, s['field']) in fk:
                fill[s['string']].add(fk[(c, s['field'])])
tags = {t: [sorted(fill[t]), xml_files.get(t, [])[:40]] for t in fill}
defs = collections.defaultdict(set)
for d in read('defines_used.tsv'):
    defs[d['define']].add(sfi(d['function']))
defines = {d: [sorted(v), define_file.get(d, '')] for d, v in defs.items()}
sfnames = sorted(sf, key=sf.get)
sf_to_fn = [name_ix.get(n, []) for n in sfnames]

data = dict(groups=groups, files=[[f, groups.index(render.group(f))] for f in files], fn=fn, up=up,
            pymods=pymods, py=py, file_edges=file_edges,
            fields=[[r['cls'], r['field'], r['type'], r['file'], int(r['line'])] for r in fields],
            acc={k: v for k, v in acc.items()}, sfnames=sfnames, sf_to_fn=sf_to_fn, tags=tags, defines=defines,
            commit=open(os.path.join(HERE, '..', 'map', 'syntax_meta.tsv')).read().strip().split('\n')[-1]
            if os.path.exists(os.path.join(HERE, '..', 'map', 'syntax_meta.tsv')) else '')
blob = json.dumps(data, separators=(',', ':'))
with open(os.path.join(HERE, 'graph_template.html'), encoding='utf-8') as h:
    page = h.read().replace('/*DATA*/null', blob)
with open(out_path, 'w', encoding='utf-8') as h:
    h.write(page)
print('wrote %s (%.1f MB): %d functions, %d files, %d file links, %d members' %
      (out_path, len(page) / 1e6, len(fn), len(files), len(file_edges), len(fields)))
