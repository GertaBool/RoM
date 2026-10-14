"""Compare two save runs: economy, production mix, units, settlers (end-state dumps + telemetry)."""
import json, sys, glob, collections

def states(prefix):
    fs = sorted(glob.glob(prefix + '.state*.json'), key=lambda f: int(f.rsplit('state', 1)[1].split('.')[0]))
    return json.load(open(fs[0])), json.load(open(fs[-1]))

def summarize(prefix):
    a, b = states(prefix)
    res = collections.OrderedDict()
    tot = collections.Counter()
    pa = {p['leader']: p for p in a['players']}
    for p in b['players']:
        e = p.get('econ', {})
        q = pa[p['leader']]
        u = p['units']
        mil = sum(v for k, v in u.items() if k not in ('worker', 'settle', 'worker sea', 'explore', 'explore sea', 'missionary', 'spy', 'great people', 'merchant', 'general'))
        nb = sum(len(c['buildings']) for c in p['cities'])
        nb0 = sum(len(c['buildings']) for c in q['cities'])
        orders = collections.Counter('unit' if c['order'].startswith('UNIT_') else 'bldg' if c['order'].startswith('BUILDING_') else 'other' for c in p['cities'])
        res[p['leader'][7:]] = dict(techs=len(p['techs']) - len(q['techs']), gold=p['gold'], rpct=e.get('pct', [0, 0])[1], research=p['researchRate'],
                                    mil=mil, bld=nb - nb0, ou=orders['unit'], ob=orders['bldg'], cities=len(p['cities']), settlers=len(p['settlers']),
                                    target=e.get('goldTarget', 0))
        for k in ('techs', 'mil', 'bld', 'ou', 'ob', 'research', 'gold', 'cities', 'settlers'):
            tot[k] += res[p['leader'][7:]][k]
    return b['turn'], res, tot

runs = [summarize(p) for p in sys.argv[1:]]
names = [p.rsplit('/', 1)[-1] for p in sys.argv[1:]]
keys = ['techs', 'research', 'rpct', 'gold', 'target', 'mil', 'bld', 'ou', 'ob', 'cities', 'settlers']
print('%-18s' % 'leader', ' | '.join('%-60s' % n for n in names))
for leader in runs[0][1]:
    row = []
    for t, res, tot in runs:
        r = res.get(leader, {})
        row.append(' '.join('%s=%-4s' % (k[:4], r.get(k, '-')) for k in keys))
    print('%-18s' % leader, ' | '.join(row))
for (t, res, tot), n in zip(runs, names):
    print('TOTAL', n, 'turn', t, dict(tot))
