"""Model copies on the map for a game state: each unit draws its formation of iGroupSize models
(UnitMeshGroups), each city draws its buildings' models. Weighted by the model file size where the
model is in the mod (a proxy for its scene-graph size; base-game models are counted, size unknown).
usage: instances.py <mod Assets dir> <harness state0.json>"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import active_lib as A
assets, state = sys.argv[1:3]
d = json.load(open(state))
groups = {}
for e in A.records(assets, 'UnitInfo'):
    t = A.text(e, 'Type'); mg = next((g for g in e.iter() if A.L(g) == 'UnitMeshGroups'), None)
    if mg is None: continue
    groups[t] = (int(A.text(mg, 'iGroupSize') or 0), [A.text(m, 'EarlyArtDefineTag') for m in mg.iter() if A.L(m) == 'UnitMeshGroup'],
                 [int(A.text(m, 'iRequired') or 0) for m in mg.iter() if A.L(m) == 'UnitMeshGroup'])
unit_art = {A.text(e, 'Type'): A.text(e, 'NIF') for e in A.records(assets, 'UnitArtInfo')}
files = A.files(assets)
size = lambda p: files.get(p.lower().replace('\\', '/'), (None, None, None))[2]
units = collections.Counter(('UNIT_' + u[0]) for p in d['players'] for u in p['unitList'])
tot_models = 0; tot_bytes = 0; unknown = 0; rows = []
for u, n in units.items():
    gs, tags, req = groups.get(u, (1, [], [1]))
    models = n * max(gs, 1)
    nif = unit_art.get(tags[0], '') if tags else ''
    s = size(nif) if nif else None
    tot_models += models
    if s: tot_bytes += models * s
    else: unknown += models
    rows.append((models, n, gs, u, nif, s))
rows.sort(reverse=True)
print('unit models on the map: %d (from %d units); mod models x copies %.0f MB; %d copies of base-game models' % (tot_models, sum(units.values()), tot_bytes / 2**20, unknown))
for models, n, gs, u, nif, s in rows[:15]:
    print('  %5d copies = %4d units x %d  %-28s %8s  %s' % (models, n, gs, u, ('%.0f KB' % (s / 1024)) if s else 'base game', nif))
