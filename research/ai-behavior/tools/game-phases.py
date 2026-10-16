#!/usr/bin/env python3
"""Per game phase: expansion, research, economy, armies, wars and turn time.

usage: game-phases.py <run.jsonl> [turns per phase]
Players are the alive civilizations in each record (barbarians excluded).
"""
import json, sys, statistics as st

recs = [json.loads(l) for l in open(sys.argv[1]) if l.startswith('{') and '"t"' in l and '"p"' in l]
step = int(sys.argv[2]) if len(sys.argv) > 2 else 50
rows = {}
for r in recs:
    if r['t'] < 1:
        continue
    ph = (r['t'] - 1) // step
    d = rows.setdefault(ph, {'ms': [], 'cities': [], 'techs': [], 'gold': [], 'goldmax': [], 'upc': [], 'trouble': [], 'wars': [], 'top': [], 'rr': [], 'players': []})
    ps = r['p']
    d['ms'].append(r['ms'])
    d['players'].append(len(ps))
    d['cities'].append(st.median(p['cities'] for p in ps))
    d['techs'].append(st.median(p['techs'] for p in ps))
    d['gold'].append(st.median(p['gold'] for p in ps))
    d['goldmax'].append(max(p['gold'] for p in ps))
    d['rr'].append(st.median(p['rr'] for p in ps))
    c = sum(p['cities'] for p in ps)
    d['upc'].append(sum(p['units'] for p in ps) / max(1, c))
    d['trouble'].append(sum(1 for p in ps if p['trouble']) / len(ps))
    rel = r.get('rel', [])
    d['wars'].append(sum(1 for a in range(len(rel)) for b in range(a + 1, len(rel)) if rel[a][b][0] & 2))
    sc = sorted((p['score'] for p in ps), reverse=True)
    d['top'].append(sc[0] / max(1, sum(sc)))
print('%-9s %5s %7s %6s %6s %5s %7s %7s %6s %6s %5s %6s' % ('turns', 'civs', 'ms/turn', 'cities', 'techs', 'rr', 'gold', 'goldmax', 'u/city', 'troub%', 'wars', 'top%'))
for ph in sorted(rows):
    d = rows[ph]
    m = lambda k: st.mean(d[k])
    print('%-9s %5.1f %7.0f %6.1f %6.1f %5.0f %7.0f %7.0f %6.1f %6.1f %5.1f %6.1f' % (
        '%d-%d' % (ph * step + 1, (ph + 1) * step), m('players'), m('ms'), m('cities'), m('techs'), m('rr'), m('gold'), m('goldmax'),
        m('upc'), 100 * m('trouble'), m('wars'), 100 * m('top')))
