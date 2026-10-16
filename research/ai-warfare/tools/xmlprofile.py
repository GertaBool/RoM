#!/usr/bin/env python3
"""Profile every field of one or more record types from xmlread.py's records.json:
records setting it (non-default), and its numeric range or most common values.
usage: xmlprofile.py <records.json> <RecordType>..."""
import json, sys, collections
R = json.load(open(sys.argv[1]))


def nd(v):
    return v not in (None, '', 0, 0.0, False, [], {}, 'NONE')


def leaves(v, path, out):
    if isinstance(v, dict):
        for k, x in v.items():
            leaves(x, path + '/' + k, out)
    elif isinstance(v, list):
        for x in v:
            leaves(x, path, out)
    elif nd(v):
        out.append((path, v))


for t in sys.argv[2:]:
    recs = R.get(t, {})
    print('=== %s: %d records' % (t, len(recs)))
    cnt, vals = collections.Counter(), collections.defaultdict(list)
    for key, r in recs.items():
        seen = set()
        for k, v in r.items():
            if k.startswith('_'):
                continue
            out = []
            leaves(v, k, out)
            for p, x in out:
                vals[p].append(x)
                if p not in seen:
                    cnt[p] += 1
                    seen.add(p)
    for p in sorted(cnt, key=lambda p: (-cnt[p], p)):
        v = vals[p]
        if all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
            s = 'range %s..%s' % (min(v), max(v))
        else:
            c = collections.Counter(str(x) for x in v)
            s = ', '.join('%s%s' % (a, '' if n == 1 else ' x%d' % n) for a, n in c.most_common(6)) + (' ...(%d distinct)' % len(c) if len(c) > 6 else '')
        print('  %-48s %4d  %s' % (p, cnt[p], s[:150]))
