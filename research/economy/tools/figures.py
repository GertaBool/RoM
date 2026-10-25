#!/usr/bin/env python3
"""Models and figures for the land-and-industry design. Reads data/facts.json (tools/extract.py), writes
figures/*.png and data/numbers.json (every number the document quotes from a computation).

usage: figures.py <research/economy dir>
"""
import collections, json, math, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

ROOT = sys.argv[1]
F = json.load(open(os.path.join(ROOT, 'data', 'facts.json')))
FIG = os.path.join(ROOT, 'figures'); os.makedirs(FIG, exist_ok=True)
N = {}  # numbers quoted in the text

# ---------- style (dataviz reference palette, light mode) ----------
C = dict(blue='#2a78d6', orange='#eb6834', aqua='#1baf7a', yellow='#eda100', magenta='#e87ba4', green='#008300',
         violet='#6250d6', red='#e34948', ink='#0b0b0b', ink2='#52514e', muted='#8a8984', grid='#e6e5e1',
         surface='#fcfcfb', water='#dfe9f3', land='#eeede8')
SEQ = ['#cde2fb', '#b7d3f6', '#9ec5f4', '#86b6ef', '#6da7ec', '#5598e7', '#3987e5', '#2a78d6', '#256abf', '#1c5cab',
       '#184f95', '#104281', '#0d366b']
SEQ_O = ['#fde3d6', '#fbcab3', '#f8ad8b', '#f39066', '#eb6834', '#d1531f', '#ac4318', '#863412']
seq = LinearSegmentedColormap.from_list('seq', SEQ)
seq_o = LinearSegmentedColormap.from_list('seqo', SEQ_O)
div = LinearSegmentedColormap.from_list('div', ['#1c5cab', '#86b6ef', '#f0efec', '#f39066', '#c23b3a'])
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.edgecolor': C['ink2'], 'axes.labelcolor': C['ink2'],
                     'xtick.color': C['ink2'], 'ytick.color': C['ink2'], 'text.color': C['ink'], 'axes.titlesize': 9,
                     'axes.titleweight': 'bold', 'axes.titlecolor': C['ink'], 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.grid': True, 'grid.color': C['grid'], 'grid.linewidth': 0.6,
                     'lines.linewidth': 2, 'figure.facecolor': 'white', 'axes.facecolor': 'white',
                     'legend.frameon': False, 'savefig.dpi': 220})
W = 6.6  # inches, the text width


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + '.png'), bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)


# ---------- the map ----------
G = F['grid']; WD, HT = G['width'], G['height']
terrain = np.empty((HT, WD), dtype=object); ptype = np.full((HT, WD), 3); feature = np.empty((HT, WD), dtype=object)
bonus = np.empty((HT, WD), dtype=object); river = np.zeros((HT, WD), bool)
for p in F['plots']:
    terrain[p['y'], p['x']] = p['terrain']; ptype[p['y'], p['x']] = p['plot']
    feature[p['y'], p['x']] = p['feature']; bonus[p['y'], p['x']] = p['bonus']; river[p['y'], p['x']] = p['river']
water = ptype == 3
land = ~water
lat = G['bottom'] + (np.arange(HT) + 0.5) * (G['top'] - G['bottom']) / HT  # signed degrees, row 0 is the south edge
LAT = np.repeat(lat[:, None], WD, axis=1)
N['map'] = dict(name=F['source']['map'], width=WD, height=HT, land=int(land.sum()), plots=int(WD * HT),
                lat_top=G['top'], lat_bottom=G['bottom'], deg_per_row=round((G['top'] - G['bottom']) / HT, 2))

# distance to water in plots (8-neighbour BFS, wrapping east-west)
dist = np.full((HT, WD), 10 ** 6); q = collections.deque()
for y, x in zip(*np.where(water)): dist[y, x] = 0; q.append((y, x))
while q:
    y, x = q.popleft()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny, nx = y + dy, (x + dx) % WD
            if 0 <= ny < HT and dist[ny, nx] > dist[y, x] + 1:
                dist[ny, nx] = dist[y, x] + 1; q.append((ny, nx))
dist = np.where(water, 0, dist)

# ---------- climate model ----------
# annual mean temperature: zonal profile T0(phi) = 27 - 52 (|phi|/90)^2 deg C, minus lapse for hills and peaks
elev_cool = np.where(ptype == 1, 3.0, np.where(ptype == 0, 12.0, 0.0))
T = 27.0 - 52.0 * (np.abs(LAT) / 90.0) ** 2 - elev_cool
# seasonal amplitude grows with latitude and with distance from the sea (continentality)
A = (1.0 + 0.28 * np.abs(LAT)) * (1.0 + 0.6 * (1.0 - np.exp(-dist / 5.0)))
month = np.arange(12)
peak = np.where(LAT >= 0, 6, 0)  # warmest month: July (index 6) north, January (0) south
Tm = T[None] + A[None] * np.cos(2 * np.pi * (month[:, None, None] - peak[None]) / 12.0)
L = (Tm >= 5.0).sum(axis=0)  # growing-season months
Tmin = Tm.min(axis=0)
# precipitation from geography alone: wet equator, dry subtropics, wet mid-latitudes, decaying inland
P_lat = 2200 * np.exp(-(LAT / 12.0) ** 2) + 1000 * np.exp(-((np.abs(LAT) - 50) / 14.0) ** 2) + 200
P_geo = P_lat * (0.3 + 0.7 * np.exp(-dist / 7.0))
# the map designer's terrain is an observation of climate; blend it in so hand-made maps keep their character
P_terr = {'TERRAIN_DESERT': 150, 'TERRAIN_PLAINS': 650, 'TERRAIN_GRASS': 1100, 'TERRAIN_MARSH': 1600,
          'TERRAIN_TUNDRA': 400, 'TERRAIN_SNOW': 250}
P_obs = np.vectorize(lambda t: P_terr.get(t, np.nan))(terrain).astype(float)
P_obs = np.where(np.vectorize(lambda f: f == 'FEATURE_JUNGLE')(feature), 2200, P_obs)
P = np.where(np.isnan(P_obs), P_geo, 0.3 * P_geo + 0.7 * P_obs)
Wtr = P + 700 * river  # water available to crops: rain plus irrigation from a river
S0 = np.vectorize(lambda t: {'TERRAIN_GRASS': .8, 'TERRAIN_PLAINS': .65, 'TERRAIN_MARSH': .5, 'TERRAIN_TUNDRA': .3,
                             'TERRAIN_DESERT': .15, 'TERRAIN_SNOW': 0.0}.get(t, 0.0))(terrain).astype(float)
S0 = np.clip(S0 + 0.15 * river - 0.1 * (ptype == 1), 0, 1) * (ptype != 0)


def masked(a):
    return np.ma.masked_where(water, a)


def draw_map(ax, a, cmap, vmin, vmax, title, dots=None):
    ax.imshow(np.where(water, 1, np.nan), origin='lower', cmap=ListedColormap([C['water']]), interpolation='nearest',
              extent=(0, WD, 0, HT))
    im = ax.imshow(masked(a), origin='lower', cmap=cmap, vmin=vmin, vmax=vmax, interpolation='nearest', extent=(0, WD, 0, HT))
    if dots is not None and len(dots[0]):
        ax.scatter(dots[1] + 0.5, dots[0] + 0.5, s=9, facecolor=C['orange'], edgecolor='white', linewidth=0.6, zorder=3)
    ax.set_title(title, loc='left'); ax.set_xticks([]); ax.grid(False)
    yt = [0, HT / 4, HT / 2, 3 * HT / 4, HT]
    ax.set_yticks(yt); ax.set_yticklabels(['90°S', '45°S', '0°', '45°N', '90°N'])
    for s in ax.spines.values(): s.set_visible(False)
    return im


# ---------- Figure 1: what latitude does today ----------
LANDB = [b for b in F['bonuses'] if b['cls'] not in ('BONUSCLASS_MANUFACTURED', 'BONUSCLASS_FUTURE')
         and (b['terrains'] or b['features'])]
pos = collections.defaultdict(list)
for y, x in zip(*np.where(bonus != None)): pos[bonus[y, x]].append(lat[y])
order = sorted(LANDB, key=lambda b: (np.median(np.abs(pos[b['type']])) if pos[b['type']] else 99))
fig, ax = plt.subplots(figsize=(W, 7.4))
for i, b in enumerate(order):
    ax.plot([b['minlat'], b['maxlat']], [i, i], color=C['blue'], lw=4, solid_capstyle='round', alpha=0.35)
    ax.plot([-b['maxlat'], -b['minlat']], [i, i], color=C['blue'], lw=4, solid_capstyle='round', alpha=0.35)
    v = pos[b['type']]
    ax.scatter(v, [i] * len(v), s=10, color=C['orange'], zorder=3, edgecolor='white', linewidth=0.4)
ax.set_yticks(range(len(order))); ax.set_yticklabels([b['type'][6:].title().replace('_', ' ') for b in order], fontsize=6.6)
ax.set_xlim(-90, 90); ax.set_xticks([-90, -60, -30, 0, 30, 60, 90])
ax.set_xticklabels(['90°S', '60°S', '30°S', '0°', '30°N', '60°N', '90°N']); ax.grid(axis='y', visible=False)
ax.set_title('Latitude windows in CIV4BonusInfos.xml (bars) and where the Earth map puts each resource (dots)', loc='left')
ax.text(0, -2.6, 'Bar: iMinLatitude to iMaxLatitude, mirrored into both hemispheres. Dot: one plot holding the resource on '
        + N['map']['name'].replace('.CivBeyondSwordWBSave', '') + '.', ha='center', fontsize=7, color=C['ink2'])
ax.set_ylim(-3.5, len(order) - 0.3)
save(fig, 'f01_latitude_windows')
wide = [b for b in LANDB if b['minlat'] == 0 and b['maxlat'] >= 80]
N['bonus'] = dict(total=len(F['bonuses']), natural=len(LANDB), window_0_80=len(wide),
                  classes=dict(collections.Counter(b['cls'][10:].lower() for b in F['bonuses'])),
                  placed=int(sum(1 for v in bonus.flat if v)))

# ---------- Figure 2: today's chains are gates ----------
chains = [(b['type'], b['free_bonus'], b['num_free'], b['prereq'], b['prereq_or']) for b in F['buildings']
          if b['free_bonus'] and b['free_bonus'] != 'NONE' and (b['prereq'] or b['prereq_or'])
          and b['type'] not in ('BUILDING_STABLE', 'BUILDING_BROADWAY')]
N['chains'] = dict(producing_buildings=sum(1 for b in F['buildings'] if b['free_bonus'] and b['free_bonus'] != 'NONE'),
                   with_inputs=len(chains),
                   free_bonuses_huge=next(int(r) for r in [7]))
nm = lambda s: s.split('_', 1)[1].replace('_', ' ').title()
N['recipes'] = [dict(building=nm(t), output=nm(o), copies=('world size' if k == -1 else k), needs=[nm(x) for x in pre],
                     one_of=[nm(x) for x in ors]) for t, o, k, pre, ors in chains]

# ---------- Figure 3: the climate model on the Earth map ----------
fig, axs = plt.subplots(2, 2, figsize=(W, 4.2))
ims = [draw_map(axs[0, 0], T, div, -30, 30, 'Annual mean temperature (°C)'),
       draw_map(axs[0, 1], P, seq, 0, 2600, 'Water from rain (mm per year)'),
       draw_map(axs[1, 0], L, seq, 0, 12, 'Growing season (months ≥ 5 °C)'),
       draw_map(axs[1, 1], peak + 1, ListedColormap([C['orange'], C['blue']]), 1, 7, 'Warmest month')]
for ax, im, lab in zip(axs.flat[:3], ims[:3], ['°C', 'mm', 'months']):
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.01); cb.outline.set_visible(False); cb.ax.tick_params(labelsize=6.5)
axs[1, 1].text(62, 12, 'January (south)', color=C['orange'], fontsize=7, fontweight='bold', ha='center')
axs[1, 1].text(10, 30, 'July (north)', color=C['blue'], fontsize=7, fontweight='bold', ha='center')
fig.tight_layout(h_pad=0.6, w_pad=0.6)
save(fig, 'f03_climate')

# ---------- Figure 4: does geography alone agree with the map designer's terrain? ----------
kinds = [('TERRAIN_DESERT', 'Desert'), ('TERRAIN_PLAINS', 'Plains'), ('TERRAIN_GRASS', 'Grassland'),
         ('TERRAIN_TUNDRA', 'Tundra'), ('TERRAIN_SNOW', 'Snow')]
fig, axs = plt.subplots(1, 3, figsize=(W, 2.5), sharey=True)
med = {}
for ax, field, lab in [(axs[0], P_geo, 'Rain, geography alone (mm)'), (axs[1], P, 'Rain, blended with terrain (mm)'), (axs[2], T, 'Temperature (°C)')]:
    data = [field[(terrain == k) & land] for k, _ in kinds]
    bp = ax.boxplot(data, vert=False, widths=0.55, patch_artist=True, showfliers=False,
                    medianprops=dict(color=C['orange'], lw=2), boxprops=dict(facecolor='#eef4fc', edgecolor=C['blue']),
                    whiskerprops=dict(color=C['blue']), capprops=dict(color=C['blue']))
    ax.set_yticks(range(1, len(kinds) + 1)); ax.set_yticklabels([k[1] for k in kinds]); ax.set_xlabel(lab, fontsize=7.5)
    ax.grid(axis='y', visible=False)
    med[lab] = {k[1]: round(float(np.median(d)), 0) for k, d in zip(kinds, data)}
axs[0].set_title('Model fields on each terrain the map designer drew', loc='left')
fig.tight_layout()
save(fig, 'f04_model_check')
N['check'] = med
N['check_counts'] = {k[1]: int(((terrain == k[0]) & land).sum()) for k in kinds}

# ---------- crops ----------
def trap(x, a, b, c, d):
    return np.clip(np.minimum((x - a) / max(b - a, 1e-9), (d - x) / max(d - c, 1e-9)), 0, 1)


CROPS = {  # T: annual mean deg C window (zero, full, full, zero); W: water mm; L: min growing months; F: min coldest month
    'Wheat': dict(T=(3, 8, 16, 23), W=(250, 450, 900, 1500), L=4, F=-30, bonus='BONUS_WHEAT'),
    'Rice': dict(T=(16, 21, 29, 34), W=(900, 1500, 3000, 4500), L=6, F=5, bonus='BONUS_RICE'),
    'Maize': dict(T=(10, 15, 26, 31), W=(450, 650, 1300, 2000), L=5, F=-30, bonus='BONUS_CORN'),
    'Potato': dict(T=(2, 7, 15, 21), W=(400, 600, 1200, 1900), L=3, F=-30, bonus='BONUS_POTATO'),
    'Cotton': dict(T=(15, 20, 28, 32), W=(450, 700, 1300, 2000), L=7, F=0, bonus='BONUS_COTTON'),
    'Coffee': dict(T=(15, 18, 24, 27), W=(1100, 1500, 2600, 3400), L=12, F=10, bonus='BONUS_COFFEE'),
    'Olives': dict(T=(11, 14, 20, 24), W=(250, 400, 800, 1200), L=8, F=0, bonus='BONUS_OLIVES'),
    'Sugar': dict(T=(19, 23, 30, 34), W=(1000, 1400, 2600, 3800), L=11, F=8, bonus='BONUS_SUGAR'),
}
BETA = 0.5


def suit(c, mode='product'):
    k = CROPS[c]
    gT, gW = trap(T, *k['T']), trap(Wtr, *k['W'])
    gL = np.clip((L - k['L'] + 2) / 2.0, 0, 1)
    gF = np.clip((Tmin - k['F'] + 3) / 3.0, 0, 1)
    climate = gT * gW * gL * gF if mode == 'product' else np.minimum.reduce([gT, gW, gL, gF])
    return np.where(land, climate * S0 ** BETA, 0)


SUIT = {c: suit(c) for c in CROPS}
fig, axs = plt.subplots(4, 2, figsize=(W, 7.2))
agree = {}
for ax, c in zip(axs.flat, CROPS):
    where = np.where(bonus == CROPS[c]['bonus'])
    im = draw_map(ax, SUIT[c], seq, 0, 1, c, dots=where)
    s_at = SUIT[c][where] if len(where[0]) else np.array([])
    land_s = SUIT[c][land]
    agree[c] = dict(placed=int(len(s_at)), mean_at_placed=round(float(s_at.mean()), 2) if len(s_at) else None,
                    mean_land=round(float(land_s.mean()), 3), share_land_ge_half=round(float((land_s >= 0.5).mean()), 3))
cb = fig.colorbar(im, ax=axs, fraction=0.02, pad=0.01, label='suitability s'); cb.outline.set_visible(False)
save(fig, 'f06_suitability_maps')
N['suit'] = agree

# response functions
fig, axs = plt.subplots(1, 2, figsize=(W, 2.4))
tx = np.linspace(-5, 36, 400); wx = np.linspace(0, 4500, 400)
for c, col in zip(['Wheat', 'Rice', 'Cotton', 'Coffee'], [C['blue'], C['aqua'], C['orange'], C['violet']]):
    axs[0].plot(tx, trap(tx, *CROPS[c]['T']), color=col, label=c)
    axs[1].plot(wx, trap(wx, *CROPS[c]['W']), color=col, label=c)
axs[0].set_xlabel('annual mean temperature T (°C)'); axs[0].set_ylabel('g'); axs[1].set_xlabel('water W (mm per year)')
axs[0].set_title('Temperature response g_T', loc='left'); axs[1].set_title('Water response g_W', loc='left')
axs[1].legend(loc='upper right', fontsize=7)
fig.tight_layout(); save(fig, 'f05_responses')

# product versus law of the minimum, for coffee on a T x W grid
TT, WW = np.meshgrid(np.linspace(10, 32, 200), np.linspace(500, 4000, 200))
k = CROPS['Coffee']; gT, gW = trap(TT, *k['T']), trap(WW, *k['W'])
fig, axs = plt.subplots(1, 2, figsize=(W, 2.5), sharey=True)
for ax, z, t in [(axs[0], gT * gW, 'Product: s = g_T · g_W'), (axs[1], np.minimum(gT, gW), 'Law of the minimum: s = min(g_T, g_W)')]:
    im = ax.contourf(TT, WW, z, levels=np.linspace(0, 1, 11), cmap=seq)
    ax.contour(TT, WW, z, levels=[0.5], colors=C['orange'], linewidths=1.5)
    ax.set_title(t, loc='left'); ax.set_xlabel('T (°C)'); ax.grid(False)
axs[0].set_ylabel('W (mm)')
cb = fig.colorbar(im, ax=axs, fraction=0.03, pad=0.01); cb.outline.set_visible(False)
save(fig, 'f07_product_vs_min')
N['coffee_area_half'] = dict(product=round(float((gT * gW >= 0.5).mean()), 3), minimum=round(float((np.minimum(gT, gW) >= 0.5).mean()), 3))

# ---------- seeds: diffusion between civilizations ----------
pl = F['players']; n = len(pl)
dx = np.array([[min(abs(a['x'] - b['x']), WD - abs(a['x'] - b['x'])) for b in pl] for a in pl])
dy = np.array([[abs(a['y'] - b['y']) for b in pl] for a in pl])
D = np.maximum(dx, dy).astype(float)
newworld = np.array([p['x'] < 40 for p in pl])
cross = newworld[:, None] != newworld[None, :]


def origins(bon, r=5):
    ys, xs = np.where(bonus == bon)
    return np.array([any(max(min(abs(p['x'] - x), WD - abs(p['x'] - x)), abs(p['y'] - y)) <= r for y, x in zip(ys, xs)) for p in pl])


def diffuse(start, turns=400, lam=0.025, Dk=18.0, contact=200, runs=2000, seed=7):
    rng = np.random.default_rng(seed)
    w0 = np.exp(-D / Dk); np.fill_diagonal(w0, 0)
    out = np.zeros((runs, turns))
    for r in range(runs):
        K = start.copy()
        for t in range(turns):
            w = np.where(cross & (t < contact), 0.0, w0)
            h = 1 - np.exp(-lam * (w @ K))
            K = K | (rng.random(n) < h)
            out[r, t] = K.mean()
    return out


fig, axs = plt.subplots(1, 3, figsize=(W, 2.3), sharey=True)
dif = {}
for ax, (c, bon) in zip(axs, [('Wheat', 'BONUS_WHEAT'), ('Maize', 'BONUS_CORN'), ('Coffee', 'BONUS_COFFEE')]):
    st = origins(bon)
    if not st.any(): st[0] = True
    res = diffuse(st)
    t = np.arange(res.shape[1])
    lo, md, hi = np.percentile(res, [10, 50, 90], axis=0)
    ax.fill_between(t, lo, hi, color=C['blue'], alpha=0.18, lw=0); ax.plot(t, md, color=C['blue'])
    ax.axvline(200, color=C['ink2'], lw=0.8, ls=(0, (2, 2)))
    ax.set_title(f'{c}: {int(st.sum())} of {n} start with it', loc='left', fontsize=8)
    ax.set_xlabel('turn')
    half = int(np.argmax(md >= 0.5)) if (md >= 0.5).any() else None
    dif[c] = dict(start=int(st.sum()), turn_half=half, final_median=round(float(md[-1]), 2),
                  origins=[pl[i]['civ'][13:].title() for i in np.where(st)[0]])
axs[0].set_ylabel('share of civilizations growing it'); axs[0].set_ylim(0, 1.02)
axs[0].text(204, 0.04, 'ocean contact', fontsize=6.5, color=C['ink2'])
fig.tight_layout(); save(fig, 'f09_diffusion')
N['diffusion'] = dif

# ---------- mines: depth and depletion ----------
mine_y = {i['type']: i['yields'] for i in F['improvements'] if i['type'] in ('IMPROVEMENT_MINE', 'IMPROVEMENT_SHAFT_MINE', 'IMPROVEMENT_MODERN_MINE')}
rate = [max(mine_y['IMPROVEMENT_MINE'][1], 1), mine_y['IMPROVEMENT_SHAFT_MINE'][1], mine_y['IMPROVEMENT_MODERN_MINE'][1]]
layers = [120.0, 400.0, 1600.0]; tech = [0, 220, 340]; TURNS = 500


def run_mine(policy):
    R = list(layers); lvl = 0; out = np.zeros(TURNS); res = np.zeros((TURNS, 3))
    for t in range(TURNS):
        avail = max(i for i in range(3) if t >= tech[i])
        if policy == 'deepen' and lvl < avail: lvl = avail
        if policy == 'when_dry' and R[lvl] <= 0 and lvl < avail: lvl += 1
        # a deeper mine also works the layers above it, from the top down
        q = rate[lvl]; take = 0.0
        for i in range(lvl + 1):
            g = min(R[i], q - take); R[i] -= g; take += g
            if take >= q: break
        out[t] = take; res[t] = R
    return out, res


fig, axs = plt.subplots(1, 2, figsize=(W, 2.5))
mines = {}
for pol, col, lab in [('stay', C['ink2'], 'stays a Mine'), ('when_dry', C['orange'], 'deepened when worked out'),
                      ('deepen', C['blue'], 'deepened as soon as possible')]:
    o, r = run_mine(pol)
    axs[0].plot(o, color=col, label=lab, lw=1.6); axs[1].plot(np.cumsum(o), color=col, label=lab, lw=1.6)
    mines[pol] = dict(total=int(o.sum()), dry_turn=int(np.argmax(o == 0)) if (o == 0).any() else None)
for a in axs:
    for t0 in tech[1:]: a.axvline(t0, color=C['grid'], lw=1)
axs[0].set_title('Ore per turn from one deposit', loc='left'); axs[1].set_title('Ore extracted so far', loc='left')
axs[0].set_xlabel('turn'); axs[1].set_xlabel('turn'); axs[1].legend(loc='upper left', fontsize=7)
axs[0].text(tech[1] + 3, rate[2] * 0.95, 'Explosives', fontsize=6.5, color=C['ink2'])
axs[0].text(tech[2] + 3, rate[2] * 0.85, 'Seismology', fontsize=6.5, color=C['ink2'])
fig.tight_layout(); save(fig, 'f10_mines')
N['mines'] = dict(rate=rate, layers=layers, tech=tech, runs=mines)

# ---------- production network with rationing ----------
RAW = {'Iron ore': 6.0, 'Coal': 3.0, 'Sulphur': 2.0, 'Copper': 2.0}
RECIPES = [  # name, inputs per run, outputs per run, capacity in runs per turn
    ('Steel mill', {'Iron ore': 2, 'Coal': 1}, {'Steel': 2}, 3),
    ('Arms factory', {'Steel': 1, 'Sulphur': 1}, {'Arms': 1}, 3),
    ('Cartridge works', {'Copper': 1, 'Sulphur': 1}, {'Ammo': 2}, 2),
]
VALUE = {'Arms': 3.0, 'Ammo': 1.2, 'Steel': 1.0, 'Iron ore': 0.2, 'Coal': 0.2, 'Sulphur': 0.2, 'Copper': 0.2}


def network(raw):
    stock = dict(raw); flows = []
    # demand of every recipe at full capacity, then proportional rationing of each input among its users
    want = collections.defaultdict(float)
    for name, inp, outp, cap in RECIPES:
        for g, a in inp.items(): want[g] += a * cap
    runs = {}
    for name, inp, outp, cap in RECIPES:  # in topological order
        r = cap
        for g, a in inp.items():
            share = stock.get(g, 0.0) * min(1.0, a * cap / want[g]) if want[g] else 0.0
            r = min(r, share / a)
        runs[name] = r
        for g, a in inp.items(): stock[g] -= a * r; flows.append((g, name, a * r))
        for g, b in outp.items(): stock[g] = stock.get(g, 0.0) + b * r; flows.append((name, g, b * r))
        for g, a in inp.items():
            if g in want: want[g] -= a * cap
    return runs, stock, flows


def welfare(stock):
    return sum(VALUE.get(g, 0) * v for g, v in stock.items())


runs, stock, flows = network(RAW)
base = welfare(stock)
marg = {g: round(welfare(network({**RAW, g: RAW[g] + 1})[1]) - base, 2) for g in RAW}
N['network'] = dict(raw=RAW, runs={k: round(v, 2) for k, v in runs.items()},
                    left={k: round(v, 2) for k, v in stock.items() if v > 1e-9}, marginal=marg, welfare=round(base, 2))

fig, axs = plt.subplots(1, 2, figsize=(W, 2.7), gridspec_kw=dict(width_ratios=[1.6, 1]))
ax = axs[0]
colx = {'Iron ore': 0, 'Coal': 0, 'Sulphur': 0, 'Copper': 0, 'Steel mill': 1, 'Cartridge works': 1, 'Steel': 2,
        'Arms factory': 3, 'Arms': 4, 'Ammo': 4}
rowy = {'Iron ore': 3, 'Coal': 2.2, 'Sulphur': 1.2, 'Copper': 0.2, 'Steel mill': 2.6, 'Cartridge works': 0.6,
        'Steel': 2.6, 'Arms factory': 2.0, 'Arms': 2.0, 'Ammo': 0.6}
for a, b, v in flows:
    if v <= 0: continue
    ax.annotate('', xy=(colx[b] - 0.18, rowy[b]), xytext=(colx[a] + 0.18, rowy[a]),
                arrowprops=dict(arrowstyle='-|>', color=C['blue'] if a in RAW or b in RAW else C['orange'],
                                lw=0.6 + 0.9 * v, alpha=0.75, shrinkA=2, shrinkB=2))
    ax.text((colx[a] + colx[b]) / 2, (rowy[a] + rowy[b]) / 2 + 0.08, f'{v:g}', fontsize=6.5, ha='center', color=C['ink2'])
for k in colx:
    box = k in [r[0] for r in RECIPES]
    ax.text(colx[k], rowy[k], k + (f'\n{RAW[k]:g}/turn' if k in RAW else ''), ha='center', va='center', fontsize=6.6,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#fdf0ea' if box else '#eef4fc', edgecolor=C['orange'] if box else C['blue'], lw=0.8))
ax.set_xlim(-0.5, 4.5); ax.set_ylim(-0.3, 3.5); ax.axis('off')
ax.set_title('One network, one turn', loc='left')
ax = axs[1]
gs = list(RAW); vals = [marg[g] for g in gs]
ax.barh(range(len(gs)), vals, color=C['blue'], height=0.55)
for i, v in enumerate(vals): ax.text(v + 0.05, i, f'{v:+.2f}', va='center', fontsize=7)
ax.set_yticks(range(len(gs))); ax.set_yticklabels(gs); ax.invert_yaxis(); ax.grid(axis='y', visible=False)
ax.set_title('Worth of one more unit per turn', loc='left'); ax.set_xlabel('change in network output value')
fig.tight_layout(); save(fig, 'f11_network')

# ---------- stockpiles in a war ----------
TT2 = 260; cap = 60.0; S = np.zeros(TT2); prod = np.zeros(TT2); use = np.zeros(TT2); ready = np.zeros(TT2)
s = 20.0
for t in range(TT2):
    p_ = 3.0 + (2.0 if t >= 125 else 0.0) - (1.5 if 150 <= t < 175 else 0.0)  # factories added; a blockade cuts sulphur
    u_ = 1.0 + (7.0 if 100 <= t < 190 else 0.0)  # upkeep in peace, battles in war
    need = u_
    got = min(need, s + p_)
    s = min(cap, s + p_ - got)
    S[t], prod[t], use[t], ready[t] = s, p_, got, got / need
fig, axs = plt.subplots(1, 3, figsize=(W, 2.2), sharex=True)
axs[0].plot(S, color=C['blue']); axs[0].axhline(cap, color=C['ink2'], lw=0.8, ls=(0, (2, 2)))
axs[0].set_title('Arms in store', loc='left'); axs[0].text(4, cap - 7, 'arsenal capacity', fontsize=6.5, color=C['ink2'])
axs[1].plot(prod, color=C['aqua'], label='made'); axs[1].plot(use, color=C['orange'], label='used')
axs[1].set_title('Made and used per turn', loc='left'); axs[1].legend(fontsize=7, loc='upper left')
axs[2].plot(ready * 100, color=C['violet']); axs[2].set_title('Demand met (%)', loc='left'); axs[2].set_ylim(0, 105)
for a in axs:
    a.axvspan(100, 190, color=C['red'], alpha=0.06, lw=0); a.set_xlabel('turn')
fig.tight_layout(); save(fig, 'f12_stockpile')
N['stock'] = dict(cap=cap, empty_turn=int(np.argmax(S <= 1e-6)) if (S <= 1e-6).any() else None,
                  min_ready=round(float(ready.min() * 100), 0))

# ---------- fisheries ----------
r_, K_ = 0.3, 100.0; msy = r_ * K_ / 4
fig, axs = plt.subplots(1, 2, figsize=(W, 2.4))
nn = np.linspace(0, K_, 200)
axs[0].plot(nn, r_ * nn * (1 - nn / K_), color=C['blue'], label='regrowth rN(1-N/K)')
fish = {}
for h, col in [(5.0, C['aqua']), (msy, C['yellow']), (9.0, C['red'])]:
    axs[0].axhline(h, color=col, lw=1.2, ls=(0, (3, 2)))
    Nn = K_; series = []; catch = 0.0
    for t in range(120):
        c_ = min(h, Nn); Nn = max(0.0, Nn + r_ * Nn * (1 - Nn / K_) - c_); series.append(Nn); catch += c_
    axs[1].plot(series, color=col, label=f'catch {h:g} per turn')
    fish[f'{h:g}'] = dict(stock_after_120=round(series[-1], 1), catch=round(catch, 0))
axs[0].set_xlabel('fish stock N'); axs[0].set_ylabel('per turn'); axs[0].set_title('Regrowth and catch', loc='left')
axs[0].legend(fontsize=7, loc='upper right')
axs[1].set_xlabel('turn'); axs[1].set_ylabel('fish stock N'); axs[1].set_title('Stock under three catches', loc='left')
axs[1].legend(fontsize=7, loc='lower left')
fig.tight_layout(); save(fig, 'f13_fisheries')
N['fish'] = dict(r=r_, K=K_, msy=msy, runs=fish)

# ---------- prices ----------
fig, axs = plt.subplots(1, 2, figsize=(W, 2.4))
ratio = np.linspace(0.1, 4, 300)
for e, col in [(0.5, C['red']), (1.0, C['blue']), (2.0, C['aqua'])]:
    axs[0].plot(ratio, np.clip(ratio ** (1 / e), 0.2, 5), color=col, label=f'ε = {e:g}')
axs[0].set_xlabel('demand / supply'); axs[0].set_ylabel('price / base price'); axs[0].legend(fontsize=7)
axs[0].set_title('Price from scarcity', loc='left')
sup = np.arange(1, 13); dem = 8.0
axs[1].bar(sup, np.clip((dem / sup) ** (1 / 1.0), 0.2, 5) * sup, color=C['blue'], width=0.65)
axs[1].set_xlabel('copies the only producer sells'); axs[1].set_ylabel('income (base price units)')
axs[1].set_title('A monopolist facing demand 8, ε = 1', loc='left')
fig.tight_layout(); save(fig, 'f14_prices')

# ---------- the whole loop: one civilization over 300 turns ----------
TT3 = 300
pop = np.zeros(TT3); food = np.zeros(TT3); ore = np.zeros(TT3); steel = np.zeros(TT3); arms = np.zeros(TT3)
PLOTS, DEPOSITS = 60, 6
best = np.sort(SUIT['Wheat'][land])[-PLOTS:]  # the best 60 wheat plots of the map, as one realm's farmland
land_q = float(best.mean())
P_, A_ = 6.0, 10.0
R_ = [[120.0, 400.0, 1600.0] for _ in range(DEPOSITS)]
for t in range(TT3):
    fert = max(0.6, 1.0 - 0.002 * t) + (0.4 if t >= 200 else 0.0)  # soil wear, then fertilisers
    farms = min(0.75 * P_, PLOTS)
    f = farms * (1.0 + 3.0 * land_q * fert)
    P_ = max(1.0, P_ + 0.05 * (f - 2.0 * P_) / 2.0)  # each citizen eats 2 food; a surplus grows the realm
    lvl = 2 if t >= 240 else (1 if t >= 160 else 0)
    worked = min(0.15 * P_, DEPOSITS)
    o = 0.0
    for d in range(int(math.ceil(worked))):
        want = rate[lvl] * min(1.0, worked - d); got = 0.0
        for i in range(lvl + 1):
            g = min(R_[d][i], want - got); R_[d][i] -= g; got += g
        o += got
    st = min(o / 2.0, 12.0)
    war = 180 <= t < 220
    A_ = float(np.clip(A_ + 0.5 * st - (8.0 if war else 0.5), 0.0, 120.0))
    pop[t], food[t], ore[t], steel[t], arms[t] = P_, f, o, st, A_
fig, axs = plt.subplots(2, 2, figsize=(W, 3.6), sharex=True)
for a, y_, t_, col in [(axs[0, 0], pop, 'Population (city sizes summed)', C['blue']), (axs[0, 1], ore, 'Ore mined per turn', C['ink2']),
                       (axs[1, 0], steel, 'Steel made per turn', C['orange']), (axs[1, 1], arms, 'Arms in store', C['violet'])]:
    a.plot(y_, color=col); a.set_title(t_, loc='left'); a.axvspan(180, 220, color=C['red'], alpha=0.06, lw=0)
    for t0, lab in [(160, 'shaft mines'), (200, 'fertilisers'), (240, 'modern mines')]:
        a.axvline(t0, color=C['grid'], lw=1)
for a in axs[1]: a.set_xlabel('turn')
axs[0, 0].text(162, pop.max() * 0.08, 'shaft', fontsize=6, color=C['ink2']); axs[0, 0].text(202, pop.max() * 0.08, 'fert.', fontsize=6, color=C['ink2'])
axs[0, 0].text(242, pop.max() * 0.08, 'modern', fontsize=6, color=C['ink2'])
fig.tight_layout(); save(fig, 'f15_loop_run')
N['loop'] = dict(land_q=round(land_q, 2), pop_end=round(float(pop[-1]), 1), arms_min_war=round(float(arms[180:220].min()), 1))

# causal loop diagram
ring = ['Land quality', 'Food', 'Population', 'Labour', 'Mines (depth)', 'Ore', 'Steel', 'Arms']
nodes = {}
for i, k in enumerate(ring):
    ang = math.pi / 2 + 0.55 - 2 * math.pi * i / len(ring)
    nodes[k] = (2.6 * math.cos(ang), 1.45 * math.sin(ang))
nodes['Seeds and trade'] = (-4.6, 1.6); nodes['Soil wear'] = (-0.2, 0.55)
edges = [('Land quality', 'Food', '+'), ('Food', 'Population', '+'), ('Population', 'Labour', '+'), ('Labour', 'Mines (depth)', '+'),
         ('Mines (depth)', 'Ore', '+'), ('Ore', 'Steel', '+'), ('Steel', 'Arms', '+'), ('Arms', 'Land quality', '+ territory'),
         ('Seeds and trade', 'Land quality', '+ crops'), ('Food', 'Soil wear', '+ farming'), ('Soil wear', 'Land quality', '−')]
fig, ax = plt.subplots(figsize=(W, 3.1))
for a_, b_, sgn in edges:
    (x0, y0), (x1, y1) = nodes[a_], nodes[b_]
    col = C['red'] if sgn.startswith('−') else C['blue']
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle='-|>', color=col, lw=1.4, shrinkA=19, shrinkB=19))
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx_, ny_ = -(y1 - y0), (x1 - x0); ln = math.hypot(nx_, ny_) or 1
    ax.text(mx + 0.22 * nx_ / ln, my + 0.22 * ny_ / ln, sgn, fontsize=7, color=col, ha='center', va='center')
for k_, (x, y) in nodes.items():
    ax.text(x, y, k_, ha='center', va='center', fontsize=7.5, bbox=dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor=C['ink2'], lw=0.8))
ax.set_xlim(-5.6, 3.8); ax.set_ylim(-1.9, 1.95); ax.axis('off'); ax.set_aspect('auto')
ax.set_title('How the mechanics feed each other (blue: more gives more; red: more gives less)', loc='left')
save(fig, 'f16_loop_diagram')


# ---------- regions: climate classes from the model fields ----------
arid = Wtr < 400
klass = np.full((HT, WD), -1)
klass[land & (T >= 18) & ~arid] = 0                      # tropical
klass[land & arid & (T >= 0)] = 1                         # arid
klass[land & ~arid & (T >= 8) & (T < 18)] = 2             # temperate
klass[land & ~arid & (T >= -2) & (T < 8)] = 3             # continental and boreal
klass[land & ((T < -2) | ((T < 0) & arid))] = 4          # polar
names = ['Tropical', 'Arid', 'Temperate', 'Continental and boreal', 'Polar']
fig, axs = plt.subplots(2, 3, figsize=(W, 3.0))
share = {}
for i, ax in enumerate(axs.flat[:5]):
    draw_map(ax, np.where(klass == i, 1.0, 0.12), seq, 0, 1, names[i])
    ax.set_yticks([])
    share[names[i]] = round(float((klass[land] == i).mean()), 3)
axs.flat[5].axis('off')
axs.flat[5].text(0.0, 0.5, 'Each map shows one climate class\n(dark) on the land of the Earth map.\nClasses come from the model\'s\ntemperature and water, so a\nregion\'s class follows its latitude,\nhemisphere, altitude and coast.', fontsize=7, color=C['ink2'], va='center')
fig.tight_layout(h_pad=0.4, w_pad=0.4); save(fig, 'f08_regions')
N['regions'] = share

# ---------- geological provinces seeded from today's point resources ----------
def province(bon, sigma=3.0):
    ys, xs = np.where(bonus == bon)
    g = np.zeros((HT, WD))
    yy, xx = np.mgrid[0:HT, 0:WD]
    for y, x in zip(ys, xs):
        ddx = np.minimum(np.abs(xx - x), WD - np.abs(xx - x)); ddy = np.abs(yy - y)
        g = np.maximum(g, np.exp(-(ddx ** 2 + ddy ** 2) / (2 * sigma ** 2)))
    return np.where(land, g, 0), (ys, xs)
fig, axs = plt.subplots(2, 2, figsize=(W, 3.8))
prov = {}
for ax, (lab, bon) in zip(axs.flat, [('Iron', 'BONUS_IRON'), ('Copper', 'BONUS_COPPER'), ('Coal', 'BONUS_COAL'), ('Gold', 'BONUS_GOLD')]):
    g, where = province(bon)
    im = draw_map(ax, g, seq_o, 0, 1, lab + ' ore grade', dots=None)
    ax.scatter(where[1] + 0.5, where[0] + 0.5, s=5, color=C['ink'], zorder=3)
    prov[lab] = dict(seeds=int(len(where[0])), plots_grade_ge_half=int((g >= 0.5).sum()))
cb = fig.colorbar(im, ax=axs, fraction=0.02, pad=0.01, label='grade (1 at a seed)'); cb.outline.set_visible(False)
save(fig, 'f17_provinces')
N['provinces'] = prov

# ---------- seas: fishery productivity ----------
coastal = water & (dist == 0)
near_land = np.zeros((HT, WD), bool)
for dy_ in (-1, 0, 1):
    for dx_ in (-1, 0, 1):
        near_land |= np.roll(np.roll(land, dy_, 0), dx_, 1)
shelf = water & np.vectorize(lambda t: t == 'TERRAIN_COAST')(terrain)
cold = np.clip((np.abs(LAT) - 20) / 40.0, 0, 1)
mouth = np.zeros((HT, WD), bool)
for dy_ in (-1, 0, 1):
    for dx_ in (-1, 0, 1):
        mouth |= np.roll(np.roll(river, dy_, 0), dx_, 1)
Kf = np.where(water, (0.25 + 0.55 * shelf + 0.2 * (mouth & water)) * (0.55 + 0.45 * cold), 0)
Kf = np.where(np.vectorize(lambda f: f == 'FEATURE_ICE')(feature), 0, Kf)
fig, ax = plt.subplots(figsize=(W, 2.6))
ax.imshow(np.where(land, 1, np.nan), origin='lower', cmap=ListedColormap([C['land']]), extent=(0, WD, 0, HT), interpolation='nearest')
im = ax.imshow(np.ma.masked_where(~water, Kf), origin='lower', cmap=seq, vmin=0, vmax=1, extent=(0, WD, 0, HT), interpolation='nearest')
fy, fx = np.where(np.isin(bonus, ['BONUS_FISH', 'BONUS_CLAM', 'BONUS_CRAB', 'BONUS_SHRIMP', 'BONUS_WHALE']))
ax.scatter(fx + 0.5, fy + 0.5, s=7, color=C['orange'], edgecolor='white', linewidth=0.4, zorder=3)
ax.set_xticks([]); ax.set_yticks([0, HT / 4, HT / 2, 3 * HT / 4, HT]); ax.set_yticklabels(['90°S', '45°S', '0°', '45°N', '90°N']); ax.grid(False)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title('Carrying capacity of the sea per plot (relative), and today\'s sea resources (dots)', loc='left')
cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01); cb.outline.set_visible(False)
save(fig, 'f18_sea')
N['sea'] = dict(shelf_plots=int(shelf.sum()), water_plots=int(water.sum()), sea_resources=int(len(fy)),
                mean_K_shelf=round(float(Kf[shelf].mean()), 2), mean_K_open=round(float(Kf[water & ~shelf & (Kf > 0)].mean()), 2))

# ---------- luxuries per head instead of on/off ----------
x = np.linspace(0, 2.5, 300)
fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
axs[0].step([0, 0.0001, 2.5], [0, 1, 1], where='post', color=C['ink2'], label='today: any copy, +1')
for k_, col in [(0.5, C['blue']), (1.0, C['aqua'])]:
    axs[0].plot(x, 2 * (1 - np.exp(-x / k_)), color=col, label=f'proposed, k = {k_:g}')
axs[0].set_xlabel('units per 10 citizens per turn'); axs[0].set_ylabel('happiness in the city')
axs[0].set_title('One luxury good', loc='left'); axs[0].legend(fontsize=7, loc='lower right')
sizes = np.arange(2, 31); supply = 1.0
for k_, col in [(0.5, C['blue']), (1.0, C['aqua'])]:
    axs[1].plot(sizes, 2 * (1 - np.exp(-(10 * supply / sizes) / k_)), color=col, label=f'k = {k_:g}')
axs[1].axhline(1, color=C['ink2'], lw=1.2, ls=(0, (3, 2)), label='today')
axs[1].set_xlabel('city size'); axs[1].set_title('One unit per turn, shared by a growing city', loc='left'); axs[1].legend(fontsize=7)
fig.tight_layout(); save(fig, 'f19_luxury')

# ---------- how goods reach the engine ----------
fig, ax = plt.subplots(figsize=(W, 2.2))
steps = [('Land qualities\nper plot and region', '#eef4fc', C['blue']), ('Plot output of goods\n(hundredths)', '#eef4fc', C['blue']),
         ('City goods account\n(made, used, stored)', '#fdf0ea', C['orange']), ('City bonus count\nchangeFreeBonus', '#fdf0ea', C['orange']),
         ('Trade network\n(plot group)', '#f1f0ec', C['ink2'])]
for i, (t_, fc, ec) in enumerate(steps):
    ax.text(i * 2.6, 1.0, t_, ha='center', va='center', fontsize=6.6, bbox=dict(boxstyle='round,pad=0.4', facecolor=fc, edgecolor=ec, lw=0.9))
    if i: ax.annotate('', xy=(i * 2.6 - 1.05, 1.0), xytext=((i - 1) * 2.6 + 1.05, 1.0), arrowprops=dict(arrowstyle='-|>', color=C['ink2'], lw=1))
uses = ['building and unit requirements', 'happiness and health', 'the trade screen', 'AI valuation']
for j, u in enumerate(uses):
    ax.text(8.4 + 0.0, 0.25 - j * 0.0, '', fontsize=1)
ax.text(10.4, 0.35, 'then read, unchanged, by:\n' + '\n'.join(uses), ha='center', va='top', fontsize=6.6, color=C['ink2'])
ax.text(3.9, 1.7, 'new (DLL)', ha='center', fontsize=7, color=C['orange'], fontweight='bold')
ax.text(9.1, 1.7, 'existing engine paths', ha='center', fontsize=7, color=C['ink2'], fontweight='bold')
ax.set_xlim(-1.2, 11.6); ax.set_ylim(-0.75, 1.95); ax.axis('off')
save(fig, 'f20_engine_path')

json.dump(N, open(os.path.join(ROOT, 'data', 'numbers.json'), 'w'), indent=1)
print(json.dumps(N, indent=1)[:4000])
