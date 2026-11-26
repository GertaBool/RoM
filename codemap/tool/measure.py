#!/usr/bin/env python3
"""The figures of guides/use-cases.md, measured on the map (map/*.tsv): one section per use case.

usage: measure.py <rise-of-mankind checkout> <old commit>
  The checkout is the source the map was built from (its HEAD); <old commit> is the commit a change is
  measured from, for the impact section (the functions changed between it and HEAD, and what reaches them).
Prints counts only; reads the map through query.py, so virtual calls reach overrides as there.
"""
import collections, csv, os, re, subprocess, sys

src, old = sys.argv[1:3]
new = 'HEAD'
repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(repo, 'codemap', 'tool'))
import query as Q   # noqa: E402

M = os.path.join(repo, 'codemap', 'map')
def read(n): return list(csv.DictReader(open(os.path.join(M, n), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
F, down, up, name = Q.F, Q.down, Q.up, Q.name
defs = {i for i in F if F[i]['definition'] == '1'}
py = {int(r['function']) for r in read('python_defs.tsv')}
exported = {i for i in defs if F[i]['exported'] == '1'}
refd = {int(c['callee']) for c in read('calls.tsv') if c['kind'] == 'ref'}
over = {int(o['method']) for o in read('overrides.tsv')}
virt = {i for i in defs if F[i]['virtual'] == '1'}
def sec(t): print('\n## ' + t)

def reach(starts, g):
    seen, st = set(starts), list(starts)
    while st:
        x = st.pop()
        for y in g[x]:
            if y not in seen: seen.add(y); st.append(y)
    return seen

sec('size')
print('functions defined', len(defs), '| exported', len(exported), '| bound for Python', len(py & defs))

sec('fan-in / fan-out (distinct callers / callees, own functions only)')
fin = {i: len(set(up[i]) & defs) for i in defs}; fout = {i: len(set(down[i]) & defs) for i in defs}
for lab, d in (('fan-in', fin), ('fan-out', fout)):
    top = sorted(d, key=lambda i: -d[i])[:8]
    print(lab + ':', '; '.join(f'{name[i]} {d[i]}' for i in top))
nz = sorted(fin.values()); print('median fan-in', nz[len(nz) // 2], '| functions with fan-in >= 100:', sum(v >= 100 for v in nz))

sec('strongly connected components (call cycles)')
idx, low, onst, st, comps, k = {}, {}, set(), [], [], [0]
sys.setrecursionlimit(100000)
def scc(v):
    idx[v] = low[v] = k[0]; k[0] += 1; st.append(v); onst.add(v)
    for w in down[v]:
        if w not in defs: continue
        if w not in idx: scc(w); low[v] = min(low[v], low[w])
        elif w in onst: low[v] = min(low[v], idx[w])
    if low[v] == idx[v]:
        c = []
        while True:
            w = st.pop(); onst.discard(w); c.append(w)
            if w == v: break
        comps.append(c)
for v in defs:
    if v not in idx: scc(v)
big = sorted(comps, key=len, reverse=True)
print('largest cycle:', len(big[0]), 'functions; next:', [len(c) for c in big[1:5]], '| recursive (size>1) components:', sum(len(c) > 1 for c in comps))
files = collections.Counter(F[i]['file'] for i in big[0]); print('largest cycle by file:', files.most_common(6))

sec('reachability from outside the DLL')
entries = [i for i in defs if not up[i] or i in exported or i in py]
r = reach(entries, down) & defs
print('entry functions', len(entries), '| reached', len(r), 'of', len(defs))

sec('dead-code candidates')
cand = [i for i in defs if not (set(up[i]) & defs) and i not in exported and i not in py and i not in refd
        and i not in over and i not in virt and F[i]['kind'] != 'generated' and not F[i]['name'].startswith(('_$E', '~', '_DllMain'))]
byf = collections.Counter(F[i]['file'] for i in cand)
print('no caller, not exported, not bound for Python, address never taken, not virtual:', len(cand))
print('by file:', byf.most_common(8))
print('examples:', '; '.join(name[i] for i in sorted(cand)[:6]))

sec('synchronised random numbers (out-of-sync risk)')
rng = [i for i in defs if F[i]['scope'] == 'CvGame' and F[i]['name'] == 'getSorenRandNum']
rr = reach(rng, up) & defs
print('getSorenRandNum ids', rng, '| functions that can reach it:', len(rr), '| of them bound for Python:', len(rr & py), '| exported:', len(rr & exported))
ui = [i for i in rr if F[i]['file'].startswith(('CvDLLWidgetData', 'CvGameTextMgr'))]
print('of them in the interface files (CvDLLWidgetData, CvGameTextMgr):', len(ui), '; e.g.', '; '.join(name[i] for i in sorted(ui)[:4]))

sec('impact of a change: functions changed between the two commits, and what reaches them')
diff = subprocess.run(['git', '-C', src, 'diff', '-U0', old, new, '--', 'Assets/CvGameCoreDLL'], capture_output=True, text=True, errors='replace').stdout
changed_lines = collections.defaultdict(set); cur = None
for ln in diff.split('\n'):
    m = re.match(r'^\+\+\+ b/Assets/CvGameCoreDLL/(.+)$', ln)
    if m: cur = m.group(1); continue
    m = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', ln)
    if m and cur:
        a, n = int(m.group(1)), int(m.group(2) or 1)
        changed_lines[cur].update(range(a, a + max(n, 1)))
ch = {i for i in defs if F[i]['line'] and any(int(F[i]['line']) <= l <= int(F[i]['end']) for l in changed_lines.get(F[i]['file'], ()))}
imp = reach(ch, up) & defs
print('functions changed (new or edited):', len(ch), '| functions that can reach a changed one:', len(imp), f'({100 * len(imp) // len(defs)} % of all)')
print('entry points affected: exported', len(imp & exported), '| bound for Python', len(imp & py))
print('changed files:', len(changed_lines))

sec('tests: Tools/test_*.py that take functions from the DLL source (block(text, signature))')
import glob
byq = collections.defaultdict(set)
for i in defs: byq[(F[i]['scope'] + '::' if F[i]['scope'] else '') + F[i]['name']].add(i)
tests = sorted(glob.glob(os.path.join(src, 'Tools', 'test_*.py')))
uses, nblock, unmatched = {}, 0, 0
for t in tests:
    got = set()
    for m in re.finditer(r"block\(\s*[^,]+,\s*[rbu]?['\"]([^'\"]+)['\"]", open(t, encoding='utf-8', errors='replace').read()):
        nblock += 1
        q = re.search(r'([A-Za-z_]\w*(?:::[A-Za-z_~]\w*)+)\s*\(', m.group(1))
        if q and q.group(1) in byq: got |= byq[q.group(1)]
        else: unmatched += 1
    uses[os.path.basename(t)] = got
taken = set().union(*uses.values()) if uses else set()
print('tests', len(tests), '| taking named functions', sum(1 for g in uses.values() if g), '| block() calls', nblock,
      '| not matched to a function', unmatched, '| distinct functions taken', len(taken))
sel = sorted(t for t, g in uses.items() if g & ch)
print('changed functions taken by a test:', len(ch & taken), 'of', len(ch), '| tests taking one:', len(sel), sel)

sec('Python <-> DLL')
p2c = read('py_to_cpp.tsv'); c2p = read('cpp_to_py.tsv'); eh = read('event_handlers.tsv')
print('Python call sites whose name the DLL exposes:', len(p2c), '| with one candidate:', sum(r['candidates'] == '1' for r in p2c))
print('DLL calls into Python:', len(c2p), '| landing in a found Python function:', sum(bool(r['python_function'] and r['python_file']) for r in c2p))
print('events:', len(read('events.tsv')), '| event-handler links:', len(eh))

sec('unresolved')
u = collections.Counter(r['reason'] for r in read('unresolved.tsv')); print(dict(u))
