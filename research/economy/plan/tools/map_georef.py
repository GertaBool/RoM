"""Where on Earth a regional scenario lies, and the real land inside it (PR.F6.T3, D23).
Fits each map's longitude-latitude box (equirectangular or Mercator rows) so that real land and sea (Natural Earth
1:50m land, public domain) at the plot centres agree best with the map's own land and sea plots; then measures the
real land area inside the box (geodesic, WGS84) and divides it by the map's land plots: km2 per plot.
The fit is a search from a starting box (read off the map's rendering), so its result is a reading to inspect:
the score (share of plots that agree) is printed with it.
usage: map_georef.py <ne_50m_land.shp> <scenario.CivBeyondSwordWBSave> <lon0> <lon1> <lat0> <lat1> [steps]
       (lat0 the bottom edge, lat1 the top edge, degrees)"""
import math, re, sys
import numpy as np
import shapefile
from shapely.geometry import shape, box
from shapely.ops import unary_union
from shapely import contains_xy
from pyproj import Geod

shp, scn = sys.argv[1], sys.argv[2]
start = [float(x) for x in sys.argv[3:7]]
steps = int(sys.argv[7]) if len(sys.argv) > 7 else 4000

def scenario_land(path):
    s = open(path, 'rb').read().decode('latin-1')
    m = s[s.find('BeginMap'):s.find('EndMap')]
    W = int(re.search(r'grid width=(\d+)', m).group(1)); H = int(re.search(r'grid height=(\d+)', m).group(1))
    grid = np.zeros((H, W), bool)
    for b in re.findall(r'BeginPlot(.*?)EndPlot', s, re.S):
        x = int(re.search(r'x=(\d+)', b).group(1)); y = int(re.search(r'y=(\d+)', b).group(1))
        pt = re.search(r'PlotType=(\d)', b)
        grid[y, x] = bool(pt and pt.group(1) in '012')    # y = 0 is the bottom row
    return grid

land = unary_union([shape(s.__geo_interface__) for s in shapefile.Reader(shp).shapes()])
grid = scenario_land(scn)
H, W = grid.shape

def merc(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
def imerc(v): return math.degrees(2 * math.atan(math.exp(v)) - math.pi / 2)

def centres(p, proj):
    lon0, lon1, lat0, lat1 = p
    xs = lon0 + (np.arange(W) + 0.5) * (lon1 - lon0) / W
    if proj == 'equirect':
        ys = lat0 + (np.arange(H) + 0.5) * (lat1 - lat0) / H
    else:
        m0, m1 = merc(max(-85, lat0)), merc(min(85, lat1))
        ys = np.array([imerc(m0 + (j + 0.5) * (m1 - m0) / H) for j in range(H)])
    X, Y = np.meshgrid(((xs + 180) % 360) - 180, ys)
    return X, Y

def score(p, proj):
    if p[1] - p[0] < 1 or p[3] - p[2] < 1 or p[2] < -89 or p[3] > 89: return -1
    X, Y = centres(p, proj)
    return float((contains_xy(land, X, Y) == grid).mean())

rng = np.random.default_rng(0)
best = {}
for proj in ('equirect', 'mercator'):
    p = list(start); s = score(p, proj); scale = 4.0
    for k in range(steps):
        q = [v + rng.normal(0, scale) for v in p]
        t = score(q, proj)
        if t > s: p, s = q, t
        if k % 500 == 499: scale = max(0.1, scale * 0.6)
    best[proj] = (s, p)
proj = max(best, key=lambda k: best[k][0]); s, p = best[proj]
g = Geod(ellps='WGS84')
lon0, lon1, lat0, lat1 = p
if lon1 - lon0 >= 360:
    inbox = land.intersection(box(-180, lat0, 180, lat1))
else:
    a, b = ((lon0 + 180) % 360) - 180, ((lon1 + 180) % 360) - 180
    inbox = land.intersection(box(a, lat0, b, lat1)) if a < b else \
        unary_union([land.intersection(box(a, lat0, 180, lat1)), land.intersection(box(-180, lat0, b, lat1))])
real = abs(g.geometry_area_perimeter(inbox)[0]) / 1e6 if not inbox.is_empty else 0.0
boxarea = abs(g.geometry_area_perimeter(box(lon0, lat0, lon1, lat1))[0]) / 1e6
nland = int(grid.sum())
print('fit %s score %.3f (other %s %.3f) box lon %.1f..%.1f lat %.1f..%.1f' % (proj, s, [k for k in best if k != proj][0],
      best[[k for k in best if k != proj][0]][0], lon0, lon1, lat0, lat1))
print('real land in box %.0f km2; land plots %d -> %.0f km2 per plot; whole box %.0f km2 / %d plots -> %.0f km2 per plot'
      % (real, nland, real / max(1, nland), boxarea, W * H, boxarea / (W * H)))
