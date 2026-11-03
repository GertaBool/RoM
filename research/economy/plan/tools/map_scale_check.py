"""Lists every scenario and map script of the mod with the map scale it declares (PR.F6.T3), against map_scale.json.
Errors (exit 1): a scenario whose BeginEconomy block is missing or differs from map_scale.json; a map script without
getPlotAreaKm2() that map_scale.json does not list as skipped; a scenario or script on disk that map_scale.json
does not know.
usage: map_scale_check.py <mod checkout> [--list]"""
import glob, json, os, re, sys

mod = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, '..', 'map_scale.json')))
want = {e['file']: e['plot_area_km2'] for e in T['scenarios']}
scripts = set(T['map_scripts']['files']); skipped = set(T['map_scripts'].get('skipped', []))
errors, rows = [], []
for p in sorted(glob.glob(os.path.join(mod, 'PrivateMaps', '*.CivBeyondSwordWBSave'))):
    rel = 'PrivateMaps/' + os.path.basename(p)
    s = open(p, 'rb').read().decode('latin-1')
    m = re.search(r'BeginEconomy\s+plot area km2=(\d+)\s+EndEconomy', s)
    got = int(m.group(1)) if m else None
    rows.append((rel, got, want.get(rel)))
    if rel not in want: errors.append('%s: not in map_scale.json' % rel)
    elif got != want[rel]: errors.append('%s: declares %s, map_scale.json %s' % (rel, got, want[rel]))
for p in sorted(glob.glob(os.path.join(mod, 'PrivateMaps', '*.py'))):
    rel = 'PrivateMaps/' + os.path.basename(p)
    has = 'def getPlotAreaKm2(' in open(p, 'rb').read().decode('latin-1')
    rows.append((rel, 'function' if has else None, 'skipped' if rel in skipped else 'function'))
    if rel not in scripts: errors.append('%s: not in map_scale.json' % rel)
    elif not has and rel not in skipped: errors.append('%s: no getPlotAreaKm2()' % rel)
if '--list' in sys.argv:
    for r in rows: print('%-62s %-9s %s' % (r[0][12:], r[1], r[2]))
n_s = sum(1 for r in rows if r[0].endswith('Save')); n_ok = sum(1 for r in rows if r[1] is not None)
print('%d scenarios and %d map scripts; %d declare a scale; skipped: %s' % (n_s, len(rows) - n_s, n_ok, ', '.join(sorted(skipped)) or 'none'))
for e in errors: print('ERROR', e)
sys.exit(1 if errors else 0)
