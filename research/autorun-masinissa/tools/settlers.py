"""Compare settler outcomes between two runs' state dumps (state0 = start, last = end)."""
import json, sys, glob

def load(prefix):
    files = sorted(glob.glob(prefix + '.state*.json'), key=lambda f: int(f.rsplit('state', 1)[1].split('.')[0]))
    return json.load(open(files[0])), json.load(open(files[-1]))

def summary(prefix):
    a, b = load(prefix)
    pa = {p['leader']: p for p in a['players']}
    out = {}
    for p in b['players']:
        q = pa.get(p['leader'])
        s = p['settlers']
        out[p['leader']] = (len(q['cities']) if q else 0, len(p['cities']), len(s),
                            sum(1 for x in s if x['missionAI'] == -1 and not x['cargo']), max([x['age'] for x in s] or [0]))
    return b['turn'], out

for prefix in sys.argv[1:]:
    t, o = summary(prefix)
    print('==', prefix.rsplit('/', 1)[-1], 'end turn', t)
    tot = [0, 0, 0, 0]
    for k, (c0, c1, n, idle, age) in sorted(o.items()):
        tot[0] += c0; tot[1] += c1; tot[2] += n; tot[3] += idle
        print('  %-26s cities %2d -> %2d  settlers %d idle %d oldest %d' % (k[7:], c0, c1, n, idle, age))
    print('  TOTAL cities %d -> %d, settlers %d, idle %d' % tuple(tot))
