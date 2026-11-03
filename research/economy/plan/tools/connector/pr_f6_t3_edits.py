"""PR.F6.T3: every scenario and map script of the mod declares its map scale (map_scale.json).
Scenarios: a BeginEconomy block appended at the end of the file (read by CvWBInterface.py, PR.F6.T2).
Map scripts: a getPlotAreaKm2() function appended at the end (asked by CvMap::reset, PR.F6.T1), the Earth-sized
planet rule. Files with non-ASCII bytes are left out (the connector rewrites an edited file in UTF-8); they are listed.
Each pair's old text is the shortest run of last lines unique in the file, through its end.
usage: pr_f6_t3_edits.py <mod checkout> <pairs.json out>"""
import json, os, sys

mod, out = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, '..', '..', 'map_scale.json')))
pairs, skipped = [], []

FUNC = ('\n# Settlement Economy (PR.F6): the map scale, km2 of one plot, asked by the DLL when the map is generated.\n'
        '# This script makes a whole world, taken as an Earth-sized planet: 510,100,000 km2 over the plots.\n'
        'def getPlotAreaKm2():\n'
        '\tiPlots = CyMap().getGridWidth() * CyMap().getGridHeight()\n'
        '\tif iPlots <= 0:\n'
        '\t\treturn 0\n'
        '\treturn max(1, 510100000 // iPlots)\n')

def occurrences(s, sub):
    # overlapping occurrences: str.count does not see them, and the connector replaces the first (RoM_PerfectWorld.py,
    # whose five closing blank lines held the four-line anchor twice)
    n, i = 0, s.find(sub)
    while i >= 0:
        n += 1; i = s.find(sub, i + 1)
    return n

def append(rel, text):
    p = os.path.join(mod, rel)
    b = open(p, 'rb').read()
    try:
        s = b.decode('ascii')
    except UnicodeDecodeError:
        skipped.append(rel); return
    nl = '\r\n' if '\r\n' in s else '\n'
    text = text.replace('\n', nl)
    if not s.endswith(nl):
        text = nl + text
    lines = s.split(nl)            # the last element is '' when the file ends with a newline
    k = 2
    while True:
        old = nl.join(lines[-k:])
        if occurrences(s, old) == 1 and s.endswith(old):
            break
        k += 1
    new = old + text
    open(p, 'wb').write((s + text).encode('ascii'))
    pairs.append({'file': rel, 'old': old, 'new': new})

for e in T['scenarios']:
    append(e['file'], 'BeginEconomy\n\tplot area km2=%d\nEndEconomy\n' % e['plot_area_km2'])
for rel in T['map_scripts']['files']:
    append(rel, FUNC)

json.dump({'pairs': pairs, 'skipped': skipped}, open(out, 'w'), indent=0)
print(len(pairs), 'pairs', sum(len(json.dumps(p)) for p in pairs), 'bytes; skipped (non-ASCII):', skipped)
