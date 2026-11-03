"""Builds research/economy/plan/map_scale.json: the plot area (km2) of every scenario and map script of the mod, with
its basis (PR.F6.T3, D23, M55). Method (land-based): the real land a map shows over its land plots.
Inputs: map_scale_facts.tsv (plots and land plots per scenario), the fitted boxes of tools/map_georef.py (FIT below,
run on 2026-11-03 against Natural Earth 1:50m land), sourced totals.
usage: map_scale_table.py <mod PrivateMaps dir>"""
import glob, json, math, os, sys

pm = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.join(HERE, '..')
facts = {l.split('\t')[0]: l.rstrip('\n').split('\t') for l in open(os.path.join(PLAN, 'map_scale_facts.tsv'))
         if not l.startswith('scenario')}
NE_LAND, NE_S60, NE_N66 = 146.7e6, 12.36e6, 134.43e6     # Natural Earth 1:50m land: all, south of 60 S, north of 66 S
MARS, EARTH = 144.8e6, 510.1e6

def facts_row(name):
    # map_scale_facts.tsv keeps names one character short (its first generator's slicing): match by prefix
    return next(v for k, v in facts.items() if name.startswith(k) and len(name) - len(k) <= 1)

def r3(x):
    k = 10 ** max(0, int(math.log10(x)) - 2)
    return int(round(x / k) * k)

FIT = {  # map_georef.py, 2026-11-03: real land in the fitted box (km2), score (share of plots agreeing), box
    "Australia and New Zealand": (9431720, 0.921, "lon 106.2..184.2, lat -49.1..-1.2, equirect"),
    "North and South America": (33000932, 0.910, "lon -126.9..-27.5, lat -49.6..56.6, mercator"),
    "Colonization 1500AD": (33000932, 0.910, "lon -126.9..-27.5, lat -49.6..56.6, mercator"),
    "New Zealand": (265244, 0.959, "lon 166.7..179.0, lat -47.2..-34.3, equirect"),
    "Nihon": (1019916, 0.947, "lon 124.2..148.2, lat 26.1..46.0, equirect"),
    "Europe": (11474302, 0.823, "lon -11.0..49.4, lat 29.0..63.8, equirect"),
    "Democragphica, Huge Mediterranean": (11474302, 0.823, "lon -11.0..49.4, lat 29.0..63.8, equirect (renders the same as Europe)"),
    "Huge Europe": (11218940, 0.957, "lon -11.1..47.8, lat 27.5..60.2, mercator"),
    "Huge_Europe_ancient_flattened_grecorome": (11218940, 0.957, "lon -11.1..47.8, lat 27.5..60.2, mercator"),
    "Huge_Europe_edited_v5": (11218940, 0.958, "lon -11.1..47.8, lat 27.5..60.2, mercator"),
    "Mediterranean, Standard": (8234186, 0.781, "lon -11.5..43.2, lat 28.3..54.0, mercator"),
    "Mediterranean_Standard_edited": (8234186, 0.781, "lon -11.5..43.2, lat 28.3..54.0, mercator"),
    "Mediterranean_Standard_edited_v5": (8234186, 0.781, "lon -11.5..43.2, lat 28.3..54.0, mercator"),
    "Mediterranean, Huge": (10602007, 0.742, "lon 2.9..47.9, lat 22.4..53.4, equirect; fits from other starts disagree (3,100-5,600 km2 per land plot)"),
    "Mediterranean_Huge_1000BC": (10602007, 0.742, "as Mediterranean, Huge"),
    "Mediterranean_Huge_edited": (10602007, 0.742, "as Mediterranean, Huge"),
    "PAE Europe III Standard": (7610500, 0.759, "lon -10.7..42.9, lat 29.4..54.1, equirect"),
    "PAE Europe IV Medium": (12523407, 0.744, "lon -8.6..52.4, lat 24.3..52.8, mercator"),
    "PAE Europe V Large": (14063445, 0.756, "lon -10.2..51.9, lat 24.4..60.2, mercator"),
    "Eurasia medium": (67911781, 0.888, "lon -22.8..139.8, lat -1.5..59.5, mercator"),
    "Eurasia": (56430438, 0.837, "lon -3.7..153.3, lat 12.0..66.4, equirect"),
    "africa": (34531638, 0.907, "lon -18.1..54.3, lat -36.4..38.8, mercator"),
}
WHOLE = ["Earth 12 preset civs, Standard", "Earth 23 preset civs, Standard", "Earth 3 preset civs, Standard",
         "Earth 18 preset civs, Huge", "Earth 28 preset civs, Huge", "Earth 3 preset civs, Huge",
         "RFC Earth with big Europe 50 civs", "Giant Earth Map 31 preset civs", "Giant Earth Map no preset civs", "Giant Earth Map"]

E = []
for f in sorted(os.path.basename(p) for p in glob.glob(os.path.join(pm, '*.CivBeyondSwordWBSave'))):
    n = f[:-len('.CivBeyondSwordWBSave')]
    row = facts_row(n); L, P = int(row[4]), int(row[3])
    e = {"file": "PrivateMaps/" + f}
    if n in FIT:
        a, sc, box = FIT[n]
        e.update(km2=a / L, basis="the real land inside the map's fitted box (Natural Earth 1:50m) over its %d land plots" % L,
                 confidence="low" if sc < 0.8 else "medium" if sc < 0.9 else "good", fit={"score": sc, "box": box, "land_km2": a})
    elif n in WHOLE:
        e.update(km2=NE_LAND / L, basis="the whole Earth: Natural Earth land (146.7 million km2) over its %d land plots" % L, confidence="good")
    elif n.startswith("CarterEarth"):
        e.update(km2=NE_N66 / L, basis="the whole Earth north of 66 S (the map's bottom latitude): Natural Earth land 134.4 million km2 over its %d land plots" % L, confidence="good")
    elif n == "Earth Ice Age":
        e.update(km2=NE_LAND / 3077, basis="chosen: the same globe and grid as the Huge Earth maps (124 x 68), so their km2 per plot (146.7 million km2 over 3,077 land plots); its extra land is ice-age land on the same globe", confidence="chosen")
    elif n == "Antarctica":
        e.update(km2=NE_S60 / L, basis="Antarctica, drawn as seen from above the pole (no box fits): Natural Earth land south of 60 S (12.36 million km2) over its %d land plots" % L, confidence="medium")
    elif n.startswith("Mars"):
        e.update(km2=MARS / P, basis="the whole of Mars (144.8 million km2, NASA) over all %d plots: the map's seas are a terraformed Mars, so the whole surface counts" % P, confidence="good")
    elif n in ("EarthSea", "Sirius", "Orion"):
        e.update(km2=EARTH / P, basis="chosen: a fictional world taken as an Earth-sized planet, 510.1 million km2 over its %d plots" % P, confidence="chosen")
    elif n.startswith("Tamriel"):
        e.update(km2=10e6 / L, basis="chosen: Tamriel as a Europe-sized continent, 10 million km2 of land over its %d land plots" % L, confidence="chosen")
    else:
        raise SystemExit('no rule for ' + n)
    e["plot_area_km2"] = r3(e.pop("km2"))
    E.append(e)

scripts = sorted(os.path.basename(p) for p in glob.glob(os.path.join(pm, '*.py')))
out = {"about": "Map scale per scenario and map script (PR.F6.T3, D23, M55): km2 of one plot and its basis, built by tools/map_scale_table.py. Method: land-based (the real land a map shows over its land plots), proposed to the user 2026-11-03.",
       "sources": ["Natural Earth 1:50m land, public domain: https://www.naturalearthdata.com/downloads/50m-physical-vectors/50m-land/ (146.7 million km2 of land, inland waters excluded)",
                   "Mars surface 144.8 million km2: NASA Mars fact sheet https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html",
                   "Earth surface 510.1 million km2"],
       "scenarios": E,
       "map_scripts": {"files": ["PrivateMaps/" + s for s in scripts],
                       "declaration": "def getPlotAreaKm2(): an Earth-sized planet, 510,100,000 km2 over the map's plots (CyMap grid width x height): the DLL's default rule, declared; scripts generate their land at random, so no real region is measured",
                       "note": "surface-based, while the Earth scenarios are land-based: on Earth Standard the two differ by about 27 % (the scenarios draw land larger than the sea)"}}
path = os.path.join(PLAN, 'map_scale.json')
open(path, 'w').write(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
for e in E:
    print('%-58s %7d  %s' % (e['file'][12:70], e['plot_area_km2'], e['confidence']))
print(len(E), 'scenarios,', len(scripts), 'map scripts')
