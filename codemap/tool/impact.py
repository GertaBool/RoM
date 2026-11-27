#!/usr/bin/env python3
"""Who consumes what a range of commits changed: callers, state written, and readers of that state.

usage: impact.py <DLL repository> <base commit> <head commit> <out.tsv>
The map (codemap/map) must be built at <head commit>, with state.tsv from state.py. A function is changed when a
line of its definition at <head> is added or changed by `git diff <base> <head>` in Assets/CvGameCoreDLL.
Writes one row per link, with every link listed:
  changed  relation  other  member  where
- 'called by': each function that calls the changed one (virtual calls into it included); where: call lines.
- 'writes': each member the changed function writes, directly or through an accessor it calls.
- 'read by': each function that reads such a member, directly or through an accessor ('where' says which).
- 'writes through calls': each other member written directly by a function the changed one reaches through
  calls, at any depth; 'other' is one such writer, 'where' the call from the changed function that leads to
  it. Readers of these are not listed (query state.tsv for a member).
- 'reads': each member the changed function reads (what its result depends on).
Prints one line per changed function with the counts, then the totals, to stderr.
Not covered: functions deleted at <head> (they are not in the head map; compare the functions.tsv of maps
built at both commits), and effects through the exe or Python, which py_calls.tsv and cpp_to_py.tsv hold.
"""
import collections, csv, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import query as Q   # noqa: E402


def main():
    repo, base, head, out = sys.argv[1:5]
    diff = subprocess.run(['git', '-C', repo, 'diff', '-U0', base, head, '--', 'Assets/CvGameCoreDLL'],
                          capture_output=True, text=True, errors='replace', check=True).stdout
    changed_lines, cur = collections.defaultdict(set), None
    for ln in diff.split('\n'):
        m = re.match(r'^\+\+\+ (?:b/Assets/CvGameCoreDLL/(.+)|/dev/null)$', ln)
        if m: cur = m.group(1); continue
        m = re.match(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', ln)
        if m and cur:
            a, n = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
            changed_lines[cur].update(range(a, a + max(n, 1)))   # n == 0: a pure deletion after line a
    ch = sorted(i for i, r in Q.F.items() if r['definition'] == '1' and r['line'] and
                any(int(r['line']) <= l <= int(r['end']) for l in changed_lines.get(r['file'], ())))

    st = list(csv.DictReader(open(os.path.join(Q.M, 'state.tsv'), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
    by_fn = collections.defaultdict(list)
    readers = collections.defaultdict(list)
    for r in st:
        by_fn[int(r['function'])].append(r)
        if r['access'] == 'read': readers[(r['member'], r['class'])].append(r)
    lines = collections.defaultdict(list)
    for c in Q.read('calls.tsv'):
        lines[(int(c['caller']), int(c['callee']))].append(f"{c['file']}:{c['line']}")

    rows, summary = [], []
    for i in ch:
        callers = sorted(set(Q.up[i]))
        for c in callers:
            rows.append((i, 'called by', Q.name[c], '', ', '.join(sorted(set(lines.get((c, i), [])))) or 'virtual'))
        written = set({(r['member'], r['class']) for r in by_fn[i] if r['access'] == 'write'})
        nread = 0
        for m, cls in sorted(written):
            w = [r for r in by_fn[i] if r['access'] == 'write' and r['member'] == m and r['class'] == cls]
            rows.append((i, 'writes', '', f'{cls}::{m}', w[0]['line'] or 'via ' + Q.name[int(w[0]['via'])]))
            for r in sorted(readers[(m, cls)], key=lambda r: r['name']):
                if int(r['function']) == i: continue
                nread += 1
                rows.append((i, 'read by', r['name'], f'{cls}::{m}',
                             r['line'] if r['how'] == 'direct' else 'via ' + Q.name[int(r['via'])]))
        # members written further down: by any function the changed one reaches through calls
        first, todo = {}, [(c, c) for c in Q.down[i] if c != i]
        while todo:
            x, hop = todo.pop()
            if x in first or x == i: continue
            first[x] = hop
            todo += [(y, hop) for y in Q.down[x]]
        deep = {}
        for x, hop in first.items():
            for r in by_fn[x]:
                if r['access'] == 'write' and r['how'] == 'direct':
                    deep.setdefault((r['member'], r['class']), (x, hop))
        for (m, cls), (x, hop) in sorted(deep.items()):
            if (m, cls) not in written:
                rows.append((i, 'writes through calls', Q.name[x], f'{cls}::{m}', 'first call: ' + Q.name[hop]))
        rd = sorted({(r['member'], r['class']) for r in by_fn[i] if r['access'] == 'read'})
        for m, cls in rd:
            rows.append((i, 'reads', '', f'{cls}::{m}', ''))
        summary.append((Q.name[i], len(callers), len(written), nread, len(rd), len([k for k in deep if k not in written])))

    with open(out, 'w', encoding='utf-8') as f:
        f.write('changed\tname\trelation\tother\tmember\twhere\n')
        for i, rel, other, mem, where in rows:
            f.write(f'{i}\t{Q.name[i]}\t{rel}\t{other}\t{mem}\t{where}\n')
    for s in summary:
        print(f'{s[1]:5d} callers {s[2]:4d} members written {s[3]:6d} readers {s[5]:5d} written through calls '
              f'{s[4]:4d} members read  {s[0]}', file=sys.stderr)
    print(f'{len(ch)} changed functions, {len(rows)} links', file=sys.stderr)


if __name__ == '__main__':
    main()
