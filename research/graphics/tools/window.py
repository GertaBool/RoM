"""Share of the map's unit models, cities and plots inside the busiest view window of a given size:
the most a camera-centred paging scheme would keep loaded at once.
usage: window.py <mod Assets dir> <harness state0.json> <width> <height>"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import active_lib as A
assets, state, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
d = json.load(open(state)); gs = {}
for e in A.records(assets, 'UnitInfo'):
    mg = next((g for g in e.iter() if A.L(g) == 'UnitMeshGroups'), None)
    gs[A.text(e, 'Type')] = max(int(A.text(mg, 'iGroupSize') or 1), 1) if mg is not None else 1
hdr = json.loads(open(state.replace('.state0.json', '')).readline())
MW, MH = hdr['w'], hdr['h']
models = collections.Counter(); cities = collections.Counter()
for p in d['players']:
    for u in p['unitList']: models[(u[5], u[6])] += gs.get('UNIT_' + u[0], 1)
    for c in p['cities']: cities[(c['x'], c['y'])] += 1
def inwin(cnt, x0, y0): return sum(v for (x, y), v in cnt.items() if x0 <= x < x0 + W and y0 <= y < y0 + H)
best = max(((inwin(models, x, y), inwin(cities, x, y), x, y) for x in range(0, MW - W + 1) for y in range(0, MH - H + 1)))
tm, tc = sum(models.values()), sum(cities.values())
print('map %dx%d = %d plots; window %dx%d = %d plots (%.0f%%)' % (MW, MH, MW * MH, W, H, W * H, 100 * W * H / (MW * MH)))
print('busiest window for unit models at (%d,%d): %d of %d unit models (%.0f%%), %d of %d cities (%.0f%%)' % (best[2], best[3], best[0], tm, 100 * best[0] / tm, best[1], tc, 100 * best[1] / tc))
bc = max(((inwin(cities, x, y), x, y) for x in range(0, MW - W + 1) for y in range(0, MH - H + 1)))
print('busiest window for cities at (%d,%d): %d cities (%.0f%%)' % (bc[1], bc[2], bc[0], 100 * bc[0] / tc))
