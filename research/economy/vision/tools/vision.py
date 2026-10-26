#!/usr/bin/env python3
"""The Living Economy: the complete design. Builds vision/figures/*.png and vision/living-economy.pdf from the data of
research/economy (land model) and research/economy/settlement (games, model, measurements, derived needs).
usage: vision.py <research/economy dir>"""
import io, json, math, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image as PI
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, ListFlowable, ListItem

ROOT = sys.argv[1]
SET = os.path.join(ROOT, 'settlement', 'data')
J = lambda d, n: json.load(open(os.path.join(d, n)))
SN, YL, ND, BC = J(SET, 'snumbers.json'), J(SET, 'yields.json'), J(SET, 'needs_derived.json'), J(SET, 'bc.json')
LN = J(os.path.join(ROOT, 'data'), 'numbers.json')
VD = os.path.join(ROOT, 'vision', 'data')
GR, FF, TTJ, BD = J(VD, 'growth.json'), J(VD, 'food_facts.json'), J(VD, 'tech_turns.json'), J(VD, 'bounds.json')
FIG = os.path.join(ROOT, 'vision', 'figures'); OUT = os.path.join(ROOT, 'vision', 'living-economy.pdf')
C = dict(blue='#2a78d6', orange='#eb6834', aqua='#1baf7a', yellow='#eda100', violet='#6250d6', red='#e34948', ink='#0b0b0b', ink2='#52514e',
         grid='#e6e5e1', lb='#eef4fc', lo='#fdf0ea', lg='#f1f0ec', la='#e8f6f0')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.edgecolor': C['ink2'], 'axes.labelcolor': C['ink2'],
                     'xtick.color': C['ink2'], 'ytick.color': C['ink2'], 'axes.titlesize': 9, 'axes.titleweight': 'bold',
                     'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True, 'grid.color': C['grid'],
                     'lines.linewidth': 2, 'legend.frameon': False, 'savefig.dpi': 220})
W = 6.6


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + '.png'), bbox_inches='tight', pad_inches=0.04); plt.close(fig)


def node(ax, x, y, text, fc, ec, w=1.9, h=0.62, fs=7.2, bold=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle='round,pad=0.02,rounding_size=0.12', facecolor=fc, edgecolor=ec, lw=1))
    ax.text(x, y, text, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal', color=C['ink'])


def arrow(ax, a, b, col=None, lw=1.2, rad=0.0, label=None, ls='-'):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=col or C['ink2'], lw=lw, shrinkA=14, shrinkB=14,
                                                     connectionstyle='arc3,rad=%g' % rad, linestyle=ls))
    if label:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.12, label, fontsize=6.4, color=col or C['ink2'], ha='center')


# ---------- figure: the gestalt ----------
fig, ax = plt.subplots(figsize=(W, 4.5))
X = [0.0, 3.0, 6.0, 9.0, 12.0]
P = {'people': (X[0], 3.2), 'land': (X[0], 1.2), 'work': (X[1], 2.2), 'goods': (X[2], 2.2), 'industry': (X[2], 4.0), 'trade': (X[2], 0.4),
     'needs': (X[3], 4.0), 'market': (X[3], 2.2), 'army': (X[3], 0.4), 'growth': (X[4], 4.0), 'money': (X[4], 2.2), 'state': (X[4], 0.4)}
BW, BH, FS = 2.55, 0.95, 6.9
box = lambda k, t, fc, ec, bold=False: node(ax, *P[k], t, fc, ec, w=BW, h=BH, fs=FS, bold=bold)
box('land', 'Land\nclimate, soil,\nore, sea', C['la'], C['aqua']); box('people', 'People\ncitizens and\noccupations', C['la'], C['aqua'])
box('work', 'Work\nplots, workshops,\nservices', C['lb'], C['blue']); box('goods', 'Goods ledger\nmade, used,\nstored', C['lb'], C['blue'], True)
box('industry', 'Industry\nrecipes, tools,\npower', C['lb'], C['blue']); box('trade', 'Trade\nnetworks, convoys,\ncontracts', C['lg'], C['ink2'])
box('needs', 'Living standards\nstaple, everyday,\ncomfort, luxury', C['lo'], C['orange']); box('market', 'Markets\nprices from\nscarcity', C['lo'], C['orange'])
box('army', 'Armies\nbuilt and supplied\nfrom goods', C['lg'], C['ink2']); box('growth', 'Growth, health,\ncontentment', C['lo'], C['orange'])
box('money', 'Commerce\ngold, research,\nculture, espionage', C['lo'], C['orange']); box('state', 'State\ncivics, taxes,\nlaw', C['lg'], C['ink2'])
G = 0.08
def edge(k, side, off=0.0):
    x, y = P[k]
    return {'r': (x + BW / 2 + G, y + off), 'l': (x - BW / 2 - G, y + off), 't': (x + off, y + BH / 2 + G), 'b': (x + off, y - BH / 2 - G)}[side]
def link(a_, sa, b_, sb, oa=0.0, ob=0.0, col=None, rad=0.0, lw=1.3):
    ax.annotate('', xy=edge(b_, sb, ob), xytext=edge(a_, sa, oa), arrowprops=dict(arrowstyle='-|>', color=col or C['ink2'], lw=lw,
                shrinkA=0, shrinkB=0, connectionstyle='arc3,rad=%g' % rad))
link('people', 'r', 'work', 'l', 0, 0.2); link('land', 'r', 'work', 'l', 0, -0.2); link('work', 'r', 'goods', 'l')
link('goods', 'r', 'needs', 'l', 0.3, 0); link('goods', 'r', 'market', 'l'); link('goods', 'r', 'army', 'l', -0.3, 0)
link('needs', 'r', 'growth', 'l'); link('market', 'r', 'money', 'l'); link('money', 'b', 'state', 't'); link('state', 'l', 'army', 'r')
link('goods', 't', 'industry', 'b', -0.4, -0.4); link('industry', 'b', 'goods', 't', 0.4, 0.4)
link('goods', 'b', 'trade', 't', -0.4, -0.4); link('trade', 't', 'goods', 'b', 0.4, 0.4)
link('growth', 't', 'people', 't', col=C['aqua'], rad=0.32, lw=1.5)
link('army', 'b', 'land', 'b', col=C['red'], rad=-0.45, lw=1.5)
ax.text(6.0, 6.35, 'growth makes people', color=C['aqua'], fontsize=7, ha='center')
ax.text(4.5, -1.15, 'armies win land', color=C['red'], fontsize=7, ha='center')
ax.set_xlim(-1.5, 13.5); ax.set_ylim(-1.5, 6.6); ax.axis('off')
save(fig, 'v01_gestalt')

# ---------- figure: the arc from land to capital (measured) ----------
r = np.array([v if v else np.nan for v in YL['prod_ratio']['p50']])
share = np.clip(1 / r, 0, 1) * 100
fig, ax = plt.subplots(figsize=(W, 2.2))
x = np.arange(len(share))
ax.fill_between(x, 0, np.where(np.isnan(share), np.nan, np.minimum(share, 100)), color=C['aqua'], alpha=0.25, lw=0)
ax.plot(x, np.minimum(share, 100), color=C['aqua'])
ax.set_ylim(0, 105); ax.set_xlim(20, 149); ax.set_xlabel('turn (Normal speed, of 700)'); ax.set_ylabel('% of production')
ax.set_title('Share of production the worked plots account for, in the 30 games (median player)', loc='left')
save(fig, 'v02_land_to_capital')

# ---------- figure: the turn pipeline ----------
steps = ['1  Land and work', '2  Recipes', '3  Network market', '4  Deliveries', '5  Consumption', '6  Stores', '7  Yields as views', '8  Engine turn']
subs = ['plots, workshops,\nservices', 'in dependency\norder', 'supply, demand,\nprices', 'contracts,\nconvoys', 'citizens eat;\nneeds by tier',
        'food box, spoilage\nby technology', 'food, production,\ncommerce', 'growth, builds,\nresearch']
fig, ax = plt.subplots(figsize=(W, 2.5))
pos = [(i * 3.0, 1.6) for i in range(4)] + [((3 - i) * 3.0, 0.0) for i in range(4)]
for i, (st, sb) in enumerate(zip(steps, subs)):
    fc, ec = (C['lb'], C['blue']) if i < 7 else (C['lg'], C['ink2'])
    node(ax, *pos[i], st + '\n' + sb, fc, ec, w=2.5, h=1.05, fs=6.6)
for i in range(7):
    ax.annotate('', xy=pos[i + 1], xytext=pos[i], arrowprops=dict(arrowstyle='-|>', color=C['ink2'], lw=1.2, shrinkA=34, shrinkB=34))
ax.set_xlim(-1.5, 10.5); ax.set_ylim(-0.7, 2.3); ax.axis('off')
save(fig, 'v03_pipeline')

# ---------- figure: architecture ----------
fig, ax = plt.subplots(figsize=(W, 4.0))
layers = [('Executable (unchanged)', 3.45, C['lg'], C['ink2'], ['City screen: 3 yields,\n4 commerce sliders', 'Diplomacy screen:\ndeal items', 'Map: improvements,\nunits, overlays']),
          ('Python (new screens)', 2.35, C['la'], C['aqua'], ['City ledger screen', 'Market and\ncontracts screen', 'Land overlays,\nplot help']),
          ('DLL (new and changed)', 1.25, C['lb'], C['blue'], ['CvLedger,\nCvNetworkEconomy', 'CvMarket,\nCvContract', 'Yields as views,\nAI valuation']),
          ('XML (data)', 0.15, C['lo'], C['orange'], ['CIV4GoodInfos,\nneeds by tier', 'Recipes on buildings,\nspecialists', 'Goods costs on units,\ncivic levers'])]
for name, y, fc, ec, items in layers:
    ax.add_patch(FancyBboxPatch((-0.2, y - 0.45), 10.6, 0.95, boxstyle='round,pad=0.02,rounding_size=0.1', facecolor=fc, edgecolor=ec, lw=1))
    ax.text(0.0, y + 0.02, name, fontsize=7.4, fontweight='bold', va='center')
    for j, it in enumerate(items):
        ax.text(3.1 + j * 2.55, y + 0.02, it, fontsize=6.6, va='center', ha='left')
ax.set_xlim(-0.4, 10.6); ax.set_ylim(-0.45, 4.05); ax.axis('off')
save(fig, 'v04_architecture')

# ---------- figure: derived needs, verified ----------
ch = ND['chosen']; tg = ND['target']
fig, axs = plt.subplots(1, 2, figsize=(W, 2.3), gridspec_kw=dict(width_ratios=[1.3, 1]))
ks = list(tg)
axs[0].barh(range(len(ks)), [ch['met'][k] * 100 for k in ks], color=C['blue'], height=0.55, label='supplied in the 30 games')
axs[0].scatter([tg[k] * 100 for k in ks], range(len(ks)), color=C['orange'], zorder=3, s=26, label='target')
for i, k in enumerate(ks): axs[0].text(ch['met'][k] * 100 + 1.5, i, '%.0f %%' % (ch['met'][k] * 100), va='center', fontsize=7)
axs[0].set_yticks(range(len(ks))); axs[0].set_yticklabels(ks); axs[0].invert_yaxis(); axs[0].set_xlim(0, 105); axs[0].grid(axis='y', visible=False)
axs[0].set_xlabel('citizens fully supplied (%)'); axs[0].legend(fontsize=7, loc='lower right')
it = range(len(ND['history']))
for k, col in zip(ks, [C['blue'], C['aqua'], C['orange'], C['violet']]):
    axs[1].plot(it, [h['met'][k] * 100 for h in ND['history']], color=col, lw=1.5, marker='o', ms=3, label=k)
axs[1].set_xlabel('bisection step'); axs[1].set_title('Convergence', loc='left'); axs[1].legend(fontsize=6.5, ncol=2)
fig.tight_layout(); save(fig, 'v05_needs')

# ---------- figure: food, the box and spoilage ----------
LV = GR['levels']
fig, axs = plt.subplots(1, 2, figsize=(W, 2.5), gridspec_kw=dict(width_ratios=[1, 1.1]))
S_ILL, N_ILL = 400, 4  # an illustrative city: size 4, 400 t of grain a turn beyond what it eats
T_ILL = (30 + 10 * N_ILL) * 100
for lv, col in (('none', C['red']), ('pottery', C['orange']), ('refrigeration', C['blue'])):
    sg = LV[lv]['grain']; b = 0; ys = [0]
    for k in range(40):
        b = b + S_ILL; b -= b * sg // 1000; ys.append(b)
        if b >= T_ILL: break
    lab = {'none': 'no Pottery', 'pottery': 'Pottery', 'refrigeration': 'no loss'}[lv] + ' (%d per mille)' % sg
    axs[0].plot(range(len(ys)), ys, color=col, lw=1.6, label=lab)
axs[0].axhline(T_ILL, color=C['ink2'], lw=1, ls='--'); axs[0].text(21, T_ILL + 150, 'threshold at size %d: %s t' % (N_ILL, format(T_ILL, ',')), fontsize=6.6, color=C['ink2'])
axs[0].set_xlabel('turns'); axs[0].set_ylabel('food box (t)'); axs[0].set_ylim(0, T_ILL * 1.18); axs[0].legend(fontsize=6.3, loc='lower right')
axs[0].set_title('One city, 400 t surplus a turn', loc='left')
ks = sorted(GR['sweep'], key=int); base_f = GR['sweep']['0']['food']['traj']['150']['sim']; base_c = GR['sweep']['0']['capped']['traj']['150']['sim']
xs = [int(k) for k in ks]
axs[1].plot(xs, [GR['sweep'][k]['food']['traj']['150']['sim'] * 100 / base_f for k in ks], color=C['aqua'], marker='o', ms=3, lw=1.6, label='food the only limit')
axs[1].plot(xs, [GR['sweep'][k]['capped']['traj']['150']['sim'] * 100 / base_c for k in ks], color=C['violet'], marker='o', ms=3, lw=1.6, label='other limits as observed')
axs[1].axvline(100, color=C['ink2'], lw=0.8, ls=':'); axs[1].text(104, 3, 'the rates of section 6.2', fontsize=6.4, color=C['ink2'])
axs[1].set_xlabel('no-preservation rates, % of section 6.2'); axs[1].set_ylabel('population at turn 150 (% of no loss)')
axs[1].set_ylim(0, 105); axs[1].legend(fontsize=6.3, loc='upper right'); axs[1].set_title('All cities without Pottery, 30 games', loc='left')
fig.tight_layout(); save(fig, 'v06_food')

# ======================= the document =======================
TEXTW = A4[0] - 4.0 * cm
INK, INK2, BLUE = colors.HexColor('#0b0b0b'), colors.HexColor('#52514e'), colors.HexColor('#2a78d6')
ss = getSampleStyleSheet()
body = ParagraphStyle('body', parent=ss['BodyText'], fontName='Helvetica', fontSize=9.4, leading=13.3, textColor=INK, spaceAfter=5)
small = ParagraphStyle('small', parent=body, fontSize=8.2, leading=11)
cap = ParagraphStyle('cap', parent=body, fontSize=7.9, leading=10.4, textColor=INK2, spaceBefore=2, spaceAfter=10)
h1 = ParagraphStyle('h1', parent=ss['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=19, spaceBefore=10, spaceAfter=7, keepWithNext=1)
h2 = ParagraphStyle('h2', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=11.2, leading=14.5, spaceBefore=9, spaceAfter=4, keepWithNext=1)
h3 = ParagraphStyle('h3', parent=body, fontName='Helvetica-Bold', fontSize=9.6, spaceBefore=5, spaceAfter=2, keepWithNext=1)
title = ParagraphStyle('title', parent=h1, fontSize=26, leading=31, spaceAfter=10)
sub = ParagraphStyle('sub', parent=body, fontSize=12, leading=16, textColor=INK2)
cell = ParagraphStyle('cell', parent=body, fontSize=7.9, leading=10, spaceAfter=0)
cellb = ParagraphStyle('cellb', parent=cell, fontName='Helvetica-Bold')
box = ParagraphStyle('box', parent=body, fontSize=9.2, leading=13, backColor=colors.HexColor('#eef4fc'), borderColor=BLUE, borderWidth=0.6,
                     borderPadding=7, spaceBefore=6, spaceAfter=12)
story = []
Pp = lambda t, st=body: story.append(Paragraph(t, st))
EQ, FG = [0], []


def eq(tex, size=11.0):
    EQ[0] += 1
    f = plt.figure(figsize=(0.01, 0.01)); f.text(0, 0, '$' + tex + '$', fontsize=size, color='#0b0b0b')
    b = io.BytesIO(); f.savefig(b, format='png', dpi=300, bbox_inches='tight', pad_inches=0.03, transparent=True); plt.close(f)
    b.seek(0); w, h = PI.open(b).size; b.seek(0)
    t = Table([[Image(b, width=w * 72 / 300, height=h * 72 / 300), Paragraph('(%d)' % EQ[0], ParagraphStyle('n', parent=body, alignment=2, textColor=INK2))]],
              colWidths=[TEXTW - 1.2 * cm, 1.2 * cm])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (0, 0), 14)]))
    story.append(t); return EQ[0]


def figure(name, caption):
    FG.append(name); path = os.path.join(FIG, name + '.png'); w, h = PI.open(path).size
    story.append(KeepTogether([Image(path, width=TEXTW, height=TEXTW * h / w), Paragraph('<b>Figure %d.</b> %s' % (len(FG), caption), cap)]))
    return len(FG)


def table(rows, widths, header=True):
    data = [[Paragraph(str(c), cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#d9d8d3')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3),
          ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    if header: st.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f0ec')))
    t.setStyle(TableStyle(st)); story.append(t); story.append(Spacer(1, 8))


def bullets(items, st=body):
    story.append(ListFlowable([ListItem(Paragraph(i, st), leftIndent=10) for i in items], bulletType='bullet', start='•',
                              bulletFontName='Helvetica', leftIndent=12, bulletFontSize=8, spaceAfter=4))


S, MU, RT, OR, CAL, DE = SN['short'], SN['mult'], SN['routes'], SN['oral'], SN['calibration'], SN['deals']
bench = {(int(r['cities']), int(r['goods'])): r for r in SN['bench']}
b300, b600 = bench[(300, 100)], bench[(600, 40)]
pct = lambda x: '%.1f %%' % x
lev = ch['levels']; shape = ND['size_shape']

# ---------------- quantities used throughout ----------------
A = GR['arms']
pop_at = lambda k, t: A[k]['traj'][str(t)]['sim']
obs_at = lambda t: A['refrigeration_food']['traj'][str(t)]['obs']
spoil_pc = lambda k: A[k]['m'].get('spoiled', 0) * 100 / A[k]['m']['harvest']
starve_10k = lambda k: A[k]['m'].get('starve', 0) * 10000 / A[k]['m']['cityturns']
rel = lambda k, base, t=150: (pop_at(k, t) - pop_at(base, t)) * 100 / pop_at(base, t)
TL = {k: [int(round(v * sx)) for sx in shape] for k, v in lev.items()}  # tons per citizen and turn: village, town, city
FT = FF['techs']; LVL = GR['levels']
_pl = [p for g in TTJ for p in g['players'].values()]
e_pot = sorted(p['earliest']['TECH_POTTERY'] for p in _pl); e_fer = sorted(p['earliest']['TECH_FERMENTATION'] for p in _pl)
last_max = [max(p['last'] for p in g['players'].values()) for g in TTJ]
med = lambda v: v[len(v) // 2]
held = A['timed_capped']['m']
held_share = held['held_t'] * 100 / held['harvest']
held_per = held['held_t'] // max(1, held['held'])
n_max = BD['city_food'] // 3
box_max = (30 + 10 * n_max) * 100 + BD['city_tons']
NGOODS = 64
fmt = lambda v: format(int(v), ',')
spec = lambda name: {'none': 'none', 'pottery': 'Pottery', 'fermentation': 'Fermentation', 'refrigeration': 'Refrigeration'}[name]
clothing_town = TL['clothing'][1]


def turns_to(T, S_, sg):
    b = 0
    for k in range(1, 1000):
        b += S_; b -= b * sg // 1000
        if b >= T: return k
    return None


hunger = sorted(starve_10k(k) for k in A)
Y0, Y1 = TTJ[0]['years']

# ---------------- title ----------------
story.append(Spacer(1, 2.0 * cm))
Pp('The Living Economy', title)
Pp('A complete design for the economy of Rise of Mankind: land, people, food, goods, living standards, industry, markets, '
   'trade, the state and war, as one system', sub)
story.append(Spacer(1, 0.6 * cm))
Pp('<b>This document</b> describes the economy as it should be, whole, rather than a sequence of patches. It replaces the map\'s resource '
   'tokens, the on/off resources, the leasing of resources for gold, and the fixed yields of specialists with one ledger of goods counted in '
   'whole tons. That ledger is made by people working land and workshops, eaten and used by the population, transformed by industry, priced by '
   'markets, carried by trade and taxed by the state. Food works as the engine\'s food works today: a city eats first and grows from what is left; '
   'what is new is that the food it keeps can rot, and how much rots depends on the technologies it lacks. The game\'s three yields and four '
   'commerce outputs remain what the player sees, because the executable\'s screens show exactly those; underneath, they become views of the ledger.', box)
Pp('<b>What it rests on.</b> Every fact about today\'s game is from the mod\'s XML and DLL at GitLab <font face="Courier">main</font> '
   '<font face="Courier">3bec049</font> (the XML is unchanged at <font face="Courier">ae60523</font>). Every measured number is from '
   '<i>Land, not tokens</i>, <i>Settlement Economy</i> and the growth runs of this document (research/economy): 30 real harness games, rebuilt '
   'city by city, and deterministic models run on them. Every parameter is an anchor taken from the engine, a quantity solved from those '
   'measurements, or a design value stated as such, with the measured consequence of changing it (section 18).', small)
Pp('<b>Contents.</b> 1 Playing it · 2 Pillars · 3 The whole system · 4 What is cut, replaced and kept · 5 The ledger in whole tons · 6 Food · '
   '7 Land · 8 People and work · 9 Goods · 10 Living standards · 11 Production and industry · 12 Markets, money and the state · 13 Trade · '
   '14 War · 15 The eras · 16 The AI · 17 The interface · 18 Numbers and where they come from · 19 Architecture · 20 Building it · 21 Risks', small)
story.append(PageBreak())

# ---------------- 1 ----------------
Pp('1. Playing it', h1)
Pp('<b>4000 BC.</b> Your first village of three eats %s t of grain and fish a turn and harvests %s t. Before Pottery, the surplus sits in '
   'baskets and pits, and a share of it rots every turn: the ledger shows the food box filling, then slowing, then barely moving. Across the 30 '
   'measured games, cities that never learnt Pottery would have lost %.0f %% of their harvest to spoilage. Pottery is one technology away. You '
   'research it, the box fills, and the village grows.' % (fmt(3 * 300), fmt(3 * 300 + 400), spoil_pc('none_capped')))
Pp('<b>2000 BC.</b> Your capital sits where a river crosses warm plains. The overlay shows why the site was good: wheat suits the flood plain '
   'at 0.8, the hills to the north hold copper of grade 0.7, the coast is shelf water. The town of size 4 has two farmers, one herder and one '
   'fisher; it eats %s t a turn and grows from what is left, as cities always did. Its people also want meat or fruit, wool or cloth, and '
   'firewood. The ledger reads: <i>Clothing: 30 t of %s t; 2 of 4 citizens clothed</i>. A neighbour offers wool for your copper. You accept a '
   'contract: 30 t of wool a turn for 20 t of copper a turn, for 20 turns. Fermentation came last century: the fish is salted in jars and the '
   'fruit pressed into wine, so very little of either rots any more.' % (fmt(4 * 300), clothing_town * 4))
Pp('<b>400 AD.</b> Eleven cities, one network of roads and a river. The market shows grain cheap and wine dear; your coastal cities are fed by '
   'the inland farms, which is why the iron town in the hills could grow to 9 on rock. Three of your farm towns are as large as their health '
   'and contentment allow; their surplus, %s t a turn between them, goes down the river to the capital and out to sea under a grain contract. '
   'A merchant from the south sells you rice seed for 300 gold, and the river delta that was marsh becomes paddy over the next ten turns.' % fmt(3 * held_per))
Pp('<b>1850.</b> Coal and iron meet in the north; four mills turn them into steel, and the steel into rails and rifles. A third of your people '
   'now work in workshops and factories rather than fields, fed by grain bought abroad under a 50-turn contract. Refrigeration is still a '
   'generation away, so the beef from the pampas comes salted and the cities\' milk comes from their own hinterland. Your rival blockades the '
   'strait; the price of cotton doubles in a turn, two mills stand idle, and contentment in the textile towns falls. You can pay, fight, or '
   'plant cotton in the south, which the climate overlay says will grow at 0.4.')
Pp('Every one of these situations follows from the rules below. None needs a scripted event.')

# ---------------- 2 ----------------
Pp('2. Pillars', h1)
table([['Pillar', 'Meaning', 'Consequence for the design'],
       ['Material truth', 'Things are made of things. Nothing appears from nowhere or is used without being made', 'One conserved ledger in whole tons; recipes consume inputs; armies cost goods'],
       ['The land matters', 'Where you are decides what you can do easily, and what you must trade for', 'No tokens; climate, soil, ore and sea as qualities of every plot'],
       ['People are the economy', 'Output is work; what people need decides what they do and how content they are', 'Occupations; living standards counted in whole citizens; needs grow with size'],
       ['Feeding comes first', 'A city eats before anything else; hunger is a crisis, not a background state', 'The engine\'s growth rule kept; spoilage only where technology is missing'],
       ['Legibility', 'Every number can be traced to its cause in two clicks, and reads as a quantity', 'Tons and citizens on every screen; never a fraction or a ratio'],
       ['Consequence without micromanagement', 'Choices are about direction, not clicks', 'Automatic distribution within networks; governors that know needs; contracts that run themselves'],
       ['AI parity', 'The AI plays the same economy and understands it', 'One valuation engine for every AI decision (section 16)'],
       ['Determinism', 'Every computer reaches the same result, bit for bit', 'Whole tons in integers sized so they cannot overflow; exact rationing; the game\'s synchronised random numbers']],
      [3.2 * cm, 6.4 * cm, 7.4 * cm])

# ---------------- 3 ----------------
Pp('3. The whole system', h1)
figure('v01_gestalt', 'The economy as one system. Land and people produce work; work fills the goods ledger; goods feed living standards, '
       'industry, markets, trade and armies; markets produce commerce for the state; growth makes people; armies win land; policy shapes work.')
Pp('There are three loops, and every mechanic belongs to at least one. The <b>loop of life</b>: land and work make food and everyday goods; '
   'citizens eat, and the surplus makes the city grow, which makes more work. The <b>loop of wealth</b>: surplus goods are sold in markets, '
   'commerce is taxed into gold, research and culture, which buy buildings and technology that make work more productive. The <b>loop of '
   'power</b>: goods make and supply armies, armies take or protect land and trade, and land and trade feed the other two loops.')
Pp('The design\'s central measured fact is in figure 2: in the 30 games, the worked plots account for nearly all production at first and for '
   'about a quarter of it by turn 150 (production %.2f times what the plots give, middle half %.1f to %.1f). A game of Rise of Mankind is the '
   'passage from an economy of land to an economy of capital. The Living Economy makes that passage visible and material: the same share that '
   'is a modifier today becomes workshops, tools, power and the goods they consume.' % (MU['prod']['150'], SN['mult']['prod_iqr150'][0], SN['mult']['prod_iqr150'][1]))
figure('v02_land_to_capital', 'The share of production that the worked plots account for, as the median player\'s plots\' production divided by its '
       'observed production (CvCity::getYieldRate), in the 30 games. The rest comes from buildings, civics and specialists.')

# ---------------- 4 ----------------
Pp('4. What is cut, replaced and kept', h1)
table([['Today', 'In the Living Economy', 'Why'],
       ['Resource tokens on plots; improvements that unlock them', 'Cut. Land qualities: crop suitability, ore grade and depth, fishing grounds', 'Places get character; resources follow geography (Land, not tokens)'],
       ['A resource is on or off for a network', 'Cut. Goods are quantities in whole tons, made and used each turn', 'Scarcity, specialisation and trade become possible'],
       ['+1 happiness or health per resource, whatever the city\'s size', 'Replaced. Living standards in tons per citizen, counted in whole citizens supplied', 'Large cities need more; luxury becomes a matter of supply'],
       ['Leasing a resource copy for gold per turn', 'Replaced. Shipments and contracts in tons, seeds and livestock, packages', 'Between AIs, %d of %d resource deals were swaps of copies and %d paid gold' % (dict(DE['composition']).get('resource for resource', 0), DE['resource_deals'], dict(DE['composition']).get('gold per turn for resource', 0))],
       ['Buildings that need resources present and give a copy', 'Replaced. Recipes that turn inputs into outputs, run by workers', 'Factories should use what they need'],
       ['Specialists with fixed yields', 'Replaced. Occupations that produce goods (smith, weaver, miller) or services (merchant, scholar, priest)', 'Work is what makes goods'],
       ['Trade routes worth 1.00 commerce times modifiers', 'Replaced. Convoys that carry goods, earning on what they carry', 'On this map %d of %d routes paid exactly the floor' % (RT['149']['at_floor'], RT['149']['routes'])],
       ['Food box, growth threshold, starvation when the box is empty', 'Kept, in tons: 300 t per citizen, threshold (30 + 10 &times; size) &times; 100 t; the box can spoil', 'The pacing of 700 turns rests on them; a city eats before it stores'],
       ['Food, production, commerce on the city screen', 'Kept, as views of the ledger', 'The executable\'s screens show exactly these'],
       ['Gold, research, culture, espionage sliders', 'Kept. They split taxed commerce as today', 'Same'],
       ['Civics, technologies, buildings', 'Kept and re-aimed: civics become economic levers; Pottery, Fermentation and Refrigeration stop spoilage; buildings become capital', 'The tree and the tech web stay; their effects become material']],
      [4.4 * cm, 6.6 * cm, 6.0 * cm])

# ---------------- 5 ----------------
story.append(PageBreak())
Pp('5. The ledger in whole tons', h1)
Pp('5.1 The unit', h2)
Pp('Every good is counted in whole tons (t). One unit of today\'s food yield is 100 t, so a citizen eats 300 t a turn '
   '(FOOD_CONSUMPTION_PER_POPULATION = 3) and a city of size 4 grows when its box holds (30 + 10 &times; 4) &times; 100 = 7,000 t '
   '(BASE_CITY_GROWTH_THRESHOLD = 30, CITY_GROWTH_MULTIPLIER = 10, Normal speed 100 %). There are no fractions anywhere: every rule that '
   'divides rounds down, and the remainder stays where it was, so rounding neither creates nor destroys a ton. A quantity on any screen or '
   'in any deal is a whole number of tons, and a living standard is a whole number of citizens supplied (section 10), never a ratio.')
Pp('The ton is the game\'s unit of account, not a census. The length of a turn on Normal runs from %d years for the first %d turns to %d months for '
   'the last %d (CIV4GameSpeedInfo.xml), and the engine\'s population figure is 1,000 &times; size<super>2.8</super> '
   '(<font face="Courier">CvCity::getRealPopulation</font>), so no fixed ration per turn could be a historical ration at every point of '
   'the game. 100 t per unit of food was chosen because every yield in the game today stays a whole number of tons, the smallest flows worth '
   'naming (a few tons of salt or dye) are still whole, and deals read naturally: 400 t of grain a turn for 20 turns.' %
   (FF['calendar_normal'][0]['months'] // 12, FF['calendar_normal'][0]['turns'], FF['calendar_normal'][-1]['months'], FF['calendar_normal'][-1]['turns']))
Pp('5.2 The ledger', h2)
Pp('Every city keeps one ledger: for every good <i>g</i>, its stock <i>X</i>, what it made <i>q</i>, received <i>m</i>, used <i>u</i> and sent '
   '<i>x</i> this turn, in tons. Every flow in the game is a line in some ledger, so goods are conserved exactly. What is left after use loses '
   'its spoilage rate &sigma;<sub>g</sub>(<i>K</i>), in tons per thousand, for the set <i>K</i> of technologies the owner knows (section 6), '
   'and is held up to the city\'s storage <i>C</i><sub>g</sub>:')
eq(r'X_{g,t+1} = \min\left(C_g,\ Y_{g,t} - \left\lfloor \frac{\sigma_g(K)\, Y_{g,t}}{1000} \right\rfloor\right), \qquad Y_{g,t} = X_{g,t} + q_{g,t} + m_{g,t} - u_{g,t} - x_{g,t}')
Pp('5.3 The three yields as views', h2)
Pp('The three yields become views of the ledger, so the city screen, the growth rule, the build queue and the sliders work unchanged:')
eq(r'\mathrm{Food} = \left\lfloor \frac{1}{100}\sum_{g \in food} (q_g + m_g) \right\rfloor')
eq(r'\mathrm{Production} = \frac{1}{100}\, L_{work}\, \pi_0 \,(1 + \tau)(1 + \kappa) + P_{ind}')
eq(r'\mathrm{Commerce} = \frac{1}{100}\left(\sum_g p_g\, \mathrm{sold}_g\, \mu + \mathrm{services} + \mathrm{convoys}\right)')
Pp('Food is the harvest and imports of food goods in hundreds of tons, so <font face="Courier">CvCity::foodDifference</font> = Food &minus; 3 '
   '&times; population keeps its meaning on the city screen while the ledger holds the exact tons. Production is the work of the citizens not '
   'producing goods, times their tools &tau; and power &kappa;, plus <i>P<sub>ind</sub></i>, what industry produces as construction capacity. '
   'Commerce is what the city\'s market earns from goods sold at price <i>p</i> with margin &mu;, plus services (merchants, banks) and convoys. '
   'The sliders split commerce into gold, research, culture and espionage exactly as now. The engine\'s percentage modifiers '
   '(<font face="Courier">CvCity::getBaseYieldRateModifier</font>) stay, applied to these views, so every building and civic that changes a '
   'yield keeps working while it is re-aimed at goods.')

# ---------------- 6 ----------------
story.append(PageBreak())
Pp('6. Food', h1)
Pp('6.1 The rule', h2)
Pp('Food keeps the rule of <font face="Courier">CvCity::doGrowth</font>, with every quantity in tons and one new term, spoilage. Each turn, in '
   'each city:')
bullets(['<b>Harvest.</b> The worked plots yield food goods: grain, fish, meat and dairy, fruit. Imports arrive.',
         '<b>Eat.</b> Each citizen eats 300 t, taken from the harvest and the box together, the most perishable good first (fish, then meat and '
         'dairy, then fruit, then grain), so the food that keeps is the food that is kept.',
         '<b>Keep.</b> What is left is the food box. Each food good in it loses its spoilage rate for the technologies the owner lacks (6.2).',
         '<b>Grow.</b> When the box reaches the threshold, the city grows by one and keeps a share of the threshold: 20 % from Settlement '
         'Essentials (free from the ancient era), 30 % from Town Essentials (Masonry and Pottery), as today\'s records give.',
         '<b>Hunger.</b> If harvest and box together cannot feed every citizen, the box empties and the city loses one citizen, exactly as today. '
         'This is the only way a citizen goes hungry.'])
Pp('A city is therefore not short of food by default. It eats first; only the surplus is stored, grows the city or spoils. A city with a '
   'bad harvest draws on its box; it loses a citizen only when the box is empty.')
eq(r'\mathrm{lost}_g = \left\lfloor \frac{\sigma_g(K)\, B_g}{1000} \right\rfloor, \qquad \sum_g B_g \geq (30 + 10\,n)\times 100 \Rightarrow n \to n+1')
Pp('6.2 Spoilage by missing technology', h2)
Pp('Spoilage depends only on what the owner does not know. The rates are tons lost per thousand held, per turn. With all three technologies, '
   'nothing rots.')
table([['Food good', 'No preservation', 'Pottery', 'Fermentation', 'Refrigeration', 'What stops the loss']] +
      [[g, str(LVL['none'][g]), str(LVL['pottery'][g]), str(LVL['fermentation'][g]), str(LVL['refrigeration'][g]), w] for g, w in
       (('grain', 'Sealed jars and granaries (Pottery)'), ('fruit', 'Wine, cider, dried fruit (Fermentation)'),
        ('dairy', 'Cheese, cured meat (Fermentation); cold store (Refrigeration)'), ('fish', 'Salted and fermented fish in jars (Pottery, Fermentation); ice (Refrigeration)'))],
      [1.7 * cm, 2.4 * cm, 1.6 * cm, 2.3 * cm, 2.5 * cm, 6.5 * cm])
Pp('The three technologies exist in RoM today, and their records place them well: <b>Pottery</b> (cost %d, ancient, %d technology from the start '
   'for every civilization in the 30 games, which all begin with Fishing) unlocks Town Essentials, the Cottage and Tablets. <b>Fermentation</b> '
   '(cost %d, ancient, needs Agriculture, Naturopathy and Pottery) gives +1 food on farms and pastures, the Brewery, the Winery and the olive and '
   'apple farms. <b>Refrigeration</b> (cost %s, industrial, at least %d technologies known) unlocks the Commercial Center (keeps 10 %% of the box, '
   '+8 health) and the Cereal Mills, and +1 commerce on pastures. In the Living Economy each keeps what its record gives and adds the end of a '
   'loss: the +1 food that Fermentation gives farms today becomes the grain and fruit that no longer rot.' %
   (FT['TECH_POTTERY']['cost'], FT['TECH_POTTERY']['fewest'] - 1, FT['TECH_FERMENTATION']['cost'], fmt(FT['TECH_REFRIGERATION']['cost']), FT['TECH_REFRIGERATION']['fewest']))
Pp('A box that loses a share each turn cannot grow without limit. With a steady surplus <i>S</i> and rate &sigma;, it settles where the loss '
   'equals the surplus, and the city can grow only while that level is above its threshold:')
eq(r'B^{*} = \frac{S\,(1000 - \sigma)}{\sigma}, \qquad \mathrm{growth\ to\ size\ } n \mathrm{\ only\ if\ } B^{*} \geq (30 + 10\,n) \times 100')
Pp('Figure 3 (left) shows one city of size 4 with 400 t of grain to spare each turn: without Pottery its box settles at %s t, below the '
   '7,000 t it needs; with Pottery it grows in %d turns instead of %d with no loss. A village without Pottery is therefore held small by its own surplus, '
   'not by hunger, and the larger its surplus the larger it can become.' %
   (fmt(400 * (1000 - LVL['none']['grain']) // LVL['none']['grain']),
    turns_to(7000, 400, LVL['pottery']['grain']), turns_to(7000, 400, 0)))
Pp('6.3 What it does in the 30 games', h2)
Pp('The rule was run on the cities of the 30 games. Each city is founded at size 1 on its observed plot and turn (captures and razings as '
   'observed) and from then on grows only from its own food: the rebuilt plots of <i>Settlement Economy</i>, worked by the game\'s governor '
   'rule, with the deterministic harvest weather. Two modes bracket what else limits a city. With <b>food the only limit</b>, cities grow as fast '
   'as their land allows. With <b>other limits as observed</b>, a player\'s cities may not together exceed its observed population at that '
   'turn, which holds health and happiness as the games had them; a city at that limit keeps its box at the threshold, as '
   '<font face="Courier">CvCity::doGrowth</font> does under avoid-growth.')
Pp('Without spoilage, the first mode overshoots the games early and meets them late: %s citizens against %s observed at turn 50, %s against '
   '%s at turn 150. The rebuilt harvest leaves out the food that went into settlers and workers and the &minus;25 %% of Oral Law, which may be '
   'why it overshoots early (<i>open</i>). The second mode meets the observed population at turn 50 and falls %.1f %% short at turn 150. Spoilage is '
   'judged against the no-loss run of the same mode, so these gaps are common to every arm.' %
   (fmt(pop_at('refrigeration_food', 50)), fmt(obs_at(50)), fmt(pop_at('refrigeration_food', 150)), fmt(obs_at(150)), (obs_at(150) - pop_at('refrigeration_capped', 150)) * 100 / obs_at(150)))
rows = [['Preservation known', 'Population at turn 50 / 100 / 150', 'vs no loss, turn 150', 'Harvest spoiled', 'Hunger, per 10,000 city-turns']]
for lab, k in (('none, all game', 'none_capped'), ('Pottery, all game', 'pottery_capped'), ('Pottery and Fermentation, all game', 'fermentation_capped'),
               ('each at its earliest turn', 'timed_capped'), ('all three (no loss, today)', 'refrigeration_capped')):
    rows.append([lab, ' / '.join(fmt(pop_at(k, t)) for t in (50, 100, 150)), '%+.1f %%' % rel(k, 'refrigeration_capped'), pct(spoil_pc(k)), '%.1f' % starve_10k(k)])
Pp('<b>Other limits as observed</b> (the closer bracket to the games):', small)
table(rows, [4.6 * cm, 4.4 * cm, 2.6 * cm, 2.4 * cm, 3.0 * cm])
rows = [['Preservation known', 'Population at turn 50 / 100 / 150', 'vs no loss, turn 150', 'Harvest spoiled', 'Hunger, per 10,000 city-turns']]
for lab, k in (('none, all game', 'none_food'), ('Pottery, all game', 'pottery_food'), ('Pottery and Fermentation, all game', 'fermentation_food'),
               ('each at its earliest turn', 'timed_food'), ('all three (no loss, today)', 'refrigeration_food')):
    rows.append([lab, ' / '.join(fmt(pop_at(k, t)) for t in (50, 100, 150)), '%+.1f %%' % rel(k, 'refrigeration_food'), pct(spoil_pc(k)), '%.1f' % starve_10k(k)])
Pp('<b>Food the only limit:</b>', small)
table(rows, [4.6 * cm, 4.4 * cm, 2.6 * cm, 2.4 * cm, 3.0 * cm])
figure('v06_food', 'Left: the food box of one city of size 4 with 400 t of grain to spare each turn, under the grain rates of section 6.2; '
       'without Pottery the box settles below the threshold. Right: population at turn 150 in the 30 games with no city knowing Pottery, as the '
       'no-preservation rates are scaled from 0 to 3 times those of section 6.2, against no loss.')
Pp('<b>When the technologies arrive.</b> Telemetry counts each player\'s technologies but does not name them, so the turn of Pottery is known '
   'only as a bound: the earliest turn at which a player\'s count had risen by the technologies it lacked. For Pottery that is turn %d to %d '
   '(median %d) for all %d players; for Fermentation turn %d to %d (median %d). No player could have known Refrigeration by turn 150: the most '
   'advanced player of each game held %d to %d technologies, and Refrigeration needs at least %d. The row "each at its earliest turn" uses '
   'these bounds, so it is the most favourable case.' %
   (e_pot[0], e_pot[-1], med(e_pot), len(_pl), e_fer[0], e_fer[-1], med(e_fer), min(last_max), max(last_max), FT['TECH_REFRIGERATION']['fewest']))
Pp('<b>The food a city can sell.</b> With other limits as observed, a city whose box reaches the threshold while its owner is at its health and '
   'happiness limit cannot grow. That happened on %s city-turns, holding %s t a time on average: %.1f %% of the whole harvest of the 30 games '
   '(each Pottery and Fermentation at its earliest turn). Today that food is lost at the threshold. In the Living Economy it is the surplus that '
   'feeds cities without farmland, fills granaries for war and sells abroad, without slowing anyone\'s growth.' %
   (fmt(held['held']), fmt(held_per), held_share))
Pp('<b>Oral Law.</b> Every civilization starts under Oral Law, whose record gives food &minus;25 %%. Applied to the harvest under this rule (the '
   'governor seeing it), it leaves %s citizens at turn 150 instead of %s (%+.1f %%), with other limits as observed; hunger stays at %.1f per '
   '10,000 city-turns, because the governor works more food plots.' %
   (fmt(pop_at('oral_timed_capped', 150)), fmt(pop_at('timed_capped', 150)), rel('oral_timed_capped', 'timed_capped'), starve_10k('oral_timed_capped')))
Pp('6.4 Readings', h2)
Pp('Each reading below rests on the facts named and would be contradicted by the evidence named.', small)
bullets(['<b>Hunger is an event, not a state.</b> In every arm, a city empties its box and loses a citizen on %.1f to %.1f of 10,000 city-turns. '
         'The previous model counted %s of citizen-turns short of staple, because it split each player\'s observed population among its cities '
         'and fed each turn on its own, with no box. Contradicted if the games themselves starve far more often than the rebuilt cities: '
         'telemetry has no food per city, so this is <i>open</i>.' % (hunger[0], hunger[-1], pct(ch['staple_short'] * 100)),
         '<b>Pottery matters, early.</b> A civilization that never learns it ends turn 150 with %.0f %% fewer citizens; one that learns it '
         'and Fermentation at the earliest turns loses %.1f %% to spoilage in all. The design relies on the AI valuing Pottery by the food it '
         'saves (section 16). Contradicted if the AI, valuing it, still researches it late; its research order is not in telemetry (<i>open</i>).'
         % (-rel('none_capped', 'refrigeration_capped'), -rel('timed_capped', 'refrigeration_capped')),
         '<b>The rates are levers, and the curve is steep.</b> Figure 3 (right): halving the no-preservation rates costs %.0f %% of turn-150 '
         'population instead of %.0f %%; tripling them costs %.0f %%. The values of section 6.2 put the cost of missing Pottery between a '
         'nuisance and a lock.' % (100 - GR['sweep']['50']['capped']['traj']['150']['sim'] * 100 / GR['sweep']['0']['capped']['traj']['150']['sim'],
                                     100 - GR['sweep']['100']['capped']['traj']['150']['sim'] * 100 / GR['sweep']['0']['capped']['traj']['150']['sim'],
                                     100 - GR['sweep']['300']['capped']['traj']['150']['sim'] * 100 / GR['sweep']['0']['capped']['traj']['150']['sim']),
         '<b>On a quarter of city-turns, something other than food stopped growth.</b> Cities held at the threshold on %s of %s city-turns; '
         'on the rest, food set the pace. Contradicted if the held turns came from the cap\'s allocation among cities rather than from real '
         'limits; the cap is per player, not per city.' %
         (fmt(held['held']), fmt(held['cityturns'])),
         '<b>Oral Law\'s food penalty cannot stay a percentage.</b> At &minus;25 %% of the harvest the model loses a quarter of its population, '
         'while the games reached %s citizens at turn 150 starting under it. Either players leave Oral Law early or the rebuilt land is short; '
         'civic adoption is not in telemetry (<i>open</i>). Either way, Oral Law becomes a lever on what the state sees and on waste in stores '
         '(section 12.4), not on the harvest.' % fmt(obs_at(150))])

# ---------------- 7 ----------------
story.append(PageBreak())
Pp('7. Land', h1)
Pp('Land is described in <i>Land, not tokens</i> and adopted whole: per plot, a climate (annual temperature, seasons that turn with the hemisphere, '
   'water, growing season), a soil that wears with farming and recovers, geological provinces with ore grade and three layers of reserves, and '
   'for water, a carrying capacity for fish. On the 30 games\' map the reconstruction checked it against the games themselves: the rebuilt '
   'cities\' worked plots feed their observed populations on %s of city-turns.' % pct(100 - CAL['3']['share'] * 100))
table([['Land use (the improvement)', 'What it makes', 'Depends on'],
       ['Farm (of a crop the civilization knows)', 'Grain or a cash crop', 'Crop suitability, soil, irrigation; Latifundium stages as estates'],
       ['Pasture', 'Meat and dairy, wool, hides, horses', 'Grass, climate; the breed known'],
       ['Orchard, vineyard, olive grove', 'Fruit, oil, wine', 'Mediterranean climate; years to bear'],
       ['Plantation', 'Sugar, cotton, coffee, tea, tobacco, spices', 'Tropical climate; labour regime (section 12.4)'],
       ['Mine, Shaft Mine, Modern Mine', 'Ores, coal, stone, salt', 'Province grade; depth reached; reserves left'],
       ['Lumber camp, then forestry', 'Timber, charcoal', 'Forest; regrowth'],
       ['Fishing fleet', 'Fish', 'Fishing ground capacity and stock'],
       ['Town, then city district', 'Services, housing', 'Population; the land\'s commerce today']], [5.2 * cm, 5.2 * cm, 6.6 * cm])

# ---------------- 8 ----------------
Pp('8. People and work', h1)
Pp('Every citizen has an occupation. The engine already distinguishes citizens working a plot from specialists; the Living Economy uses '
   'that distinction and fills it with meaning. RoM defines 19 specialist types today; they become the occupations below, defined in XML.')
table([['Occupation', 'Where', 'Makes'],
       ['Farmer, herder, fisher, miner, forester', 'A worked plot', 'The plot\'s goods (section 7)'],
       ['Artisan: smith, weaver, potter, miller, brewer, carpenter', 'A workshop slot of a building', 'The building\'s recipe, one run per artisan'],
       ['Worker (from the industrial era)', 'A factory slot', 'The factory\'s recipe, several runs per worker with power'],
       ['Merchant', 'A market slot', 'Commerce: margin on goods sold; convoy capacity'],
       ['Scholar, priest, artist, official', 'Library, temple, theatre, court', 'Research, culture, contentment, administration'],
       ['Labourer (no slot)', 'The city', 'Production: building and training work']], [5.0 * cm, 4.6 * cm, 7.4 * cm])
Pp('The city governor assigns occupations by marginal value: each citizen goes where one more worker adds most to the city\'s living standard '
   'and output (section 16). In the model that measured this, a governor that knew the city\'s needs lowered the share of citizens short of fuel '
   'from %s to %s and of everyday food variety from %s to %s compared with one that ranked plots by yields alone.' %
   (pct(S['network_store_spoil']['fuel']), pct(S['aware_network_store_spoil']['fuel']), pct(S['network_store_spoil']['variety']), pct(S['aware_network_store_spoil']['variety'])))
Pp('<b>Labour regimes</b> are civics, and they change how work is done, not a percentage: tribal labour (everyone farms), slavery (cheap '
   'plantation and mine labour, unrest, no artisans above a size), serfdom (estates bound to land), free labour (artisans and merchants '
   'possible; wages), industrial labour (factory workers). Each sets which occupations exist, their output per worker and their effect on contentment.')

# ---------------- 9 ----------------
story.append(PageBreak())
Pp('9. Goods', h1)
Pp('About forty goods carry the whole game, each counted in tons. The catalogue keeps today\'s resource types as names wherever they fit, so that '
   'existing art, Civilopedia text and requirements can be reused.')
table([['Era of first use', 'Raw goods', 'Made goods (inputs)'],
       ['Ancient', 'Grain (wheat, rice, maize, potato), fish, meat and dairy, fruit, wool, hides, timber, stone, clay, copper, salt', 'Pottery (clay, fuel), bronze (copper, tin from trade), cloth (wool), beer and wine (grain, fruit)'],
       ['Classical', 'Iron ore, tin, marble, olives, grapes, incense, dye', 'Iron tools and arms (iron, charcoal), oil (olives), fine cloth (wool, dye), coin metal (silver, gold)'],
       ['Medieval', 'Horses, silk, spices, furs', 'Plate armour (iron), paper and books (timber, scholars), glass (sand, fuel), furniture (timber)'],
       ['Renaissance', 'Sugar, coffee, tea, tobacco, cotton', 'Gunpowder (sulphur, saltpetre), ships\' stores, refined sugar, porcelain'],
       ['Industrial', 'Coal, lead, sulphur, rubber', 'Steel (iron, coal), machinery (steel), rails (steel), textiles (cotton), ammunition (lead, sulphur), chemicals, tinned food'],
       ['Modern', 'Oil, bauxite, uranium', 'Fuel (oil), aluminium (bauxite, power), plastics, electronics, consumer goods, fertilizer, medicine'],
       ['Transhuman and future', '(engineered)', 'Nanotubes, nanobots, personal replicators: the goods that end scarcity, as RoM\'s future era already names them']],
      [2.6 * cm, 6.6 * cm, 7.8 * cm])
Pp('<b>Rules for the catalogue.</b> A good exists only if a choice turns on it: a different land, a different building, a different trade '
   'partner. Goods that would always travel together are one good (meat and dairy). Each era adds goods that make the previous era\'s goods '
   'more valuable (iron makes tools that make every farm more productive). Every made good has at least one raw good that some civilizations '
   'lack, so that trade is never optional for everyone. Every good has a spoilage rate per technology level (food in section 6.2; timber, '
   'cloth and metals 0). The catalogue size costs almost nothing to compute: %.2f ms per turn at 300 cities and 100 goods (section 19.5).' % (float(b300['us_per_turn']) / 1000))

# ---------------- 10 ----------------
Pp('10. Living standards', h1)
Pp('Beyond food, each citizen wants goods from three tiers, in tons per turn. A city of <i>n</i> citizens wanting <i>l</i> t each of a tier\'s goods '
   'and holding <i>S</i> t of them supplies a whole number of citizens, and the rest go without:')
eq(r'k = \min\left(n,\ \left\lfloor \frac{S}{\ell} \right\rfloor\right), \qquad \mathrm{without} = n - k')
Pp('The city screen says it in those words, here for a city of size 10: <i>Clothing: %d t of %d t wanted; 8 of 10 citizens clothed</i>. Every '
   'effect counts citizens, so it is a whole number like every other effect in the game. Tiers are nested: a citizen counts for comforts only if '
   'clothed, fed with some variety and warm.' % (8 * TL['clothing'][2], 10 * TL['clothing'][2]))
table([['Tier', 'Goods (substitutes in each line)', 'Per citizen supplied', 'Per citizen without'],
       ['Food', 'grain · fish · meat and dairy · fruit (section 6)', 'Eats; the surplus grows the city', 'Only when the box is empty: the city loses a citizen'],
       ['Everyday', 'meat, dairy or fruit (variety) · wool or cloth · timber, charcoal or coal', 'Nothing: this is the norm', 'Variety: 1 discontent; clothing or fuel: 1 unhealthiness, which eats 100 t of food (CvCity::foodConsumption)'],
       ['Comfort', 'salt · wine or beer · pottery or furniture · (later) sugar, tea, coffee', '1 contentment; artisans and merchants possible', 'Nothing lost'],
       ['Luxury', 'spices, silk, fine cloth, dye, jewellery, porcelain', 'Culture and great-person points', 'Nothing lost: luxury is aspiration']],
      [1.8 * cm, 6.0 * cm, 4.0 * cm, 5.2 * cm])
Pp('<b>Levels by development.</b> A village (size 1 to 3) wants the base level per citizen; a town (4 to 8) %.1f times it; a city (9 and more) %.1f '
   'times. The base levels were solved, not chosen (section 18.3): they are the levels at which, in the 30 games, 8 of 10 citizens have their '
   'everyday goods and 5 of 10 their comforts. In whole tons per citizen and turn:' % (shape[1], shape[2]))
table([['Need', 'Village (1 to 3)', 'Town (4 to 8)', 'City (9 and more)']] +
      [[nm, '%d t' % TL[k][0], '%d t' % TL[k][1], '%d t' % TL[k][2]] for nm, k in (('Everyday food variety', 'variety'), ('Clothing', 'clothing'), ('Fuel', 'fuel'), ('Comfort', 'luxury'))],
      [5.0 * cm, 4.0 * cm, 4.0 * cm, 4.0 * cm])

# ---------------- 11 ----------------
Pp('11. Production and industry', h1)
Pp('A building with a recipe has slots; each artisan in a slot runs the recipe once per turn if the inputs are there. Output follows the scarcest '
   'input (fixed proportions), and tools and power raise output per worker:')
eq(r'n_k = \min\left(\left\lfloor w_k\, r_k (1 + \tau)(1 + \kappa) \right\rfloor,\ \min_g \left\lfloor \frac{\alpha_{g,k} X_g}{a_{g,k}} \right\rfloor\right)')
Pp('<i>w</i> is the number of workers, <i>r</i> runs per worker, &alpha; the building\'s share of a scarce input (exact proportional rationing in '
   'whole tons), <i>a</i> the tons of input per run. Tools are themselves a good that wears out: every so many worker-turns use up a ton of '
   'tools, so iron and fuel stay in demand for the whole game. Power (from the industrial era) is a network good produced by plants from fuel.')
Pp('<b>The industrial revolution</b> is the moment workshops overtake land, which figure 2 shows happening already in the 30 games\' first 150 '
   'turns. In the Living Economy it is the moment coal, iron and power let a worker run several recipes instead of one, which draws people from '
   'farms into factories and makes the empire depend on fed cities it does not feed itself. Refrigeration, at the same time, lets meat, milk and '
   'fish travel without loss, which is what lets a city outgrow its own hinterland.')

# ---------------- 12 ----------------
story.append(PageBreak())
Pp('12. Markets, money and the state', h1)
Pp('12.1 Markets', h2)
Pp('Each trade network has one market. After production and recipes, every surplus is offered and every unmet need bid; goods move from '
   'surplus to need inside the network automatically, in whole tons, limited by the network\'s transport capacity. The price of a good in the '
   'network follows its scarcity, within bounds so that no single turn can ruin a city:')
eq(r'p_g = p^0_g\ \mathrm{clamp}\left(\left(\frac{D_g}{S_g}\right)^{1/\varepsilon_g},\ \frac{1}{5},\ 5\right)')
Pp('Prices are shown to the player and used by the AI. Food is the largest market: the surplus held at the threshold (section 6.3, %.1f %% of the '
   'harvest in the 30 games) moves first to cities in the network that can still grow, then to stores, then abroad.' % held_share)
Pp('12.2 Money', h2)
Pp('Commerce is what the market earns: the margin on goods sold, plus services. The state taxes it, and the sliders split the tax into gold, '
   'research, culture and espionage as today. Coin metal (silver, gold) raises the margin a market can take; banks raise it further. Money is '
   'what buys goods across networks and from other civilizations; it is never created except by trade and taxation.')
Pp('12.3 Buildings as capital', h2)
Pp('Buildings keep their roles but act on goods: the essentials buildings keep their share of the food box after growth (Settlement '
   'Essentials 20 %%, Town and City Essentials 30 %%, Metropolitan Essentials 40 %% in today\'s records) and set the city\'s storage; a market '
   'adds merchant slots and margin; a harbour adds sea transport capacity and fishing fleets; a forge is a workshop of smiths. Of today\'s %d '
   'buildings, %d give specialist slots, which become workshop slots; %d add trade routes, which become transport capacity.' %
   (SN['bc']['buildings'], SN['bc']['specialists'], SN['bc']['trade_routes']))
Pp('12.4 Civics as economic levers', h2)
table([['Civic category', 'Today (examples)', 'In the Living Economy'],
       ['Administration (Oral Law, Tablets, ...)', 'Oral Law: food &minus;25 %, production &minus;25 %, commerce &minus;10 %', 'How much of the ledger the state sees and taxes; waste in state stores'],
       ['Economy (Hunter-Gatherer, Barter, Coinage, Planned, ...)', 'Trade yield modifiers; Planned: trade gives +50 % food and production', 'How markets clear: barter (no money, swaps only), coinage (prices), planned (the state allocates)'],
       ['Employment (Slavery, Caste System, Labor Allocation, ...)', 'Yields added to classes of improvements', 'The labour regime (section 8): which occupations exist and their output'],
       ['Taxation (Tribute, Census, National Debt, ...)', 'Capital and yield modifiers', 'The share of commerce taxed, tariffs on foreign goods, debt'],
       ['Trade policy (inside Economy today)', 'National Socialism forbids foreign trade', 'Free trade, mercantilism (tariffs, colonies), autarky (embargo)']],
      [4.2 * cm, 6.0 * cm, 6.8 * cm])
Pp('The starting civic Oral Law shows why civics must become levers on the ledger rather than percentages: its &minus;25 % food, applied to '
   'the harvest, costs a quarter of the population by turn 150 (section 6.3).')

# ---------------- 13 ----------------
Pp('13. Trade', h1)
Pp('<b>Inside a civilization</b> goods move freely within a network (roads, rivers, harbours connect it); between a civilization\'s separate '
   'networks they move by convoy. <b>Between civilizations</b> they move by convoys along trade routes, under contracts or as spot sales. Every '
   'quantity offered, asked or delivered is a whole number of tons.')
table([['Instrument', 'What it is', 'Engine'],
       ['Spot sale', 'Tons of a good sold now at the partner\'s market price', 'One deal item: good and tons'],
       ['Contract', 'Tons per turn, for a term, at a price; penalties for default; cancelled by war', 'One deal item per good, repeated each turn of the term'],
       ['Seeds, breeding stock, techniques', 'The means to produce a good: the buyer can plant, breed or build it', 'A deal item like a technology'],
       ['Package', 'Any combination with gold, technologies, treaties', 'The existing deal structure'],
       ['Tariffs, embargo, blockade', 'A share of value taken at the border; no trade; ships cut a sea route', 'Civics; diplomacy; naval units on route plots']],
      [3.4 * cm, 7.6 * cm, 6.0 * cm])
Pp('A deal item is a type and one 32-bit integer (<font face="Courier">TradeData</font>, CvStructs.h, exported to the executable). A goods item '
   'packs the good and the tons into that integer, <i>d</i> = tons &times; <i>N</i> + good for <i>N</i> goods, and refuses more tons than fit. '
   'With <i>N</i> = %d, one item carries up to %s t a turn; more takes a second item. Whether the executable\'s own trade screen reads the '
   'integer of a resource item directly is not known from the DLL source (<i>open</i>; the first test of milestone M4).' % (NGOODS, fmt((2**31 - 1) // NGOODS)))
Pp('A trade route becomes a convoy\'s capacity: it carries goods worth its capacity per turn and earns the price difference. In the 30 games, '
   'all trade that could happen between players needed %.2f units per route per turn with one route per city, so routes become a real constraint '
   'only as trade grows, which is the intent: harbours, roads and ships matter because they carry goods. Food travels well only once it keeps: '
   'before Fermentation a convoy of fish loses a fifth of its load each turn on the road.' % SN['route_need']['per_route'])
Pp('<b>The AI trades by value.</b> A deal is worth the sum of the marginal values (section 16) of what is received minus what is given, '
   'including the strategic value of giving a rival the means to produce. This replaces the random offers and fixed resource values that the '
   'diplomacy work of merge request !63 began to remove.')

# ---------------- 14 ----------------
Pp('14. War', h1)
Pp('Units are built from production and goods (a legion needs iron arms; a ship of the line timber, cannon and canvas; a tank steel, fuel and '
   'ammunition). Armies in the field eat 300 t per unit and turn from the nearest connected city, and their food spoils on the road like any '
   'other; a unit cut off loses strength. Battles consume ammunition from the industrial era on. Blockades and raids on provinces become ways to '
   'win: a country without steel cannot replace its tanks, and a besieged city lives on its box. An arsenal stores arms in peace; the model '
   'showed a 90-turn war emptying a 60-unit arsenal by its eleventh turn (Land, not tokens, section 9).')

# ---------------- 15 ----------------
story.append(PageBreak())
Pp('15. The eras', h1)
table([['Era', 'The economy\'s question', 'What changes'],
       ['Ancient', 'Can we keep what we harvest, and clothe ourselves?', 'Pottery and Fermentation end most spoilage; everyday goods; bronze needs copper and tin, rarely found together'],
       ['Classical', 'Who controls iron and the roads?', 'Iron tools raise all work; coinage creates markets; roads join networks'],
       ['Medieval', 'Can the towns grow beyond the land?', 'Guild workshops; mills (power from water and wind); estates and serfdom'],
       ['Renaissance', 'Who controls the sea and the colonial goods?', 'Comfort goods from the tropics; banks; mercantilist trade'],
       ['Industrial', 'Coal, iron and the factory', 'Workers run several recipes; power; railways move goods; Refrigeration ends spoilage; cities outgrow their farms'],
       ['Modern', 'Oil and the consumer', 'Oil and electricity; consumer goods raise living standards; global supply chains'],
       ['Transhuman', 'Automation', 'Androids (RoM\'s specialist) and automated factories: work stops being people'],
       ['Future', 'The end of scarcity', 'Replicators make goods from energy; the ledger\'s constraints relax by design']],
      [2.4 * cm, 5.0 * cm, 9.6 * cm])
Pp('A Normal game lasts 700 turns (Marathon 1,470); the 30 measured games cover its first 150, from %d BC to %d BC. Each era\'s goods should '
   'become important within its first third and remain useful after: the design target is that no good introduced in an era stops mattering '
   'before the era after next.' % (-Y0, -Y1))

# ---------------- 16 ----------------
Pp('16. The AI', h1)
Pp('The AI uses one quantity for every economic decision: the marginal value of one more ton per turn of each good to each of its networks, the '
   'change in its weighted living standards and output when that supply rises:')
eq(r'v_g = V(\mathbf{q} + \mathbf{e}_g) - V(\mathbf{q}), \qquad V = \sum_{cities} \left(\sum_{tier} \omega_{tier}\, k_{tier} + \omega_B\, B + \omega_F F + \omega_P P + \omega_C C\right)')
Pp('<i>k</i> is the citizens supplied in each tier (section 10) and <i>B</i> the food box, so food saved from spoilage has a value like food '
   'grown, and Pottery, Fermentation and Refrigeration are researched for the tons they save. Computed by recomputing the network once per good, '
   'it costs %.0f ms per turn at 300 cities and 100 goods on the measured host, against a late turn of about 20.8 s today (section 19.5). It '
   'drives: occupations and plots (the governor); what to build (recipes whose outputs are worth more than their inputs and labour); what to '
   'research, plant and prospect; what to offer, ask and accept in trade; when stores are worth filling; and which provinces and routes are worth '
   'a war. Because every decision uses the same values, the AI cannot be inconsistent across them, which is the failure mode of today\'s '
   'separate fixed weights.' % (float(b300['us_per_turn_with_ai_marginals']) / 1000))

# ---------------- 17 ----------------
Pp('17. The interface', h1)
bullets(['<b>City ledger screen</b> (Python): every good made, used, stored, received and spoiled, in tons; each tier as "8 of 10 citizens '
         'clothed", with what is missing and where it could come from.',
         '<b>Food box</b>: the tons held, the threshold, the tons lost to spoilage this turn and the technology that would stop them.',
         '<b>Land overlays</b>: crop suitability, ore grade and depth, fishing grounds, climate; on the map through coloured plots, the API the '
         'strategy overlay already uses.',
         '<b>Market screen</b>: the network\'s prices and their history; what is short; what sells.',
         '<b>Contracts and convoys</b>: tons in and out, with whom, until when.',
         '<b>Plot and city help</b>: every number names its cause (this plot, this worker, this building, this civic).',
         '<b>Advisors</b>: shortages and opportunities in one line each: "Iron town: 600 t of grain short for 3 turns; the road to the farms is cut".'])

# ---------------- 18 ----------------
story.append(PageBreak())
Pp('18. Numbers and where they come from', h1)
Pp('18.1 Anchors from the engine', h2)
table([['Quantity', 'Value', 'Source'],
       ['Food per citizen', '3 a turn, so 300 t', 'FOOD_CONSUMPTION_PER_POPULATION (GlobalDefines.xml)'],
       ['Growth threshold', '(30 + 10 &times; size) &times; 100 t', 'BASE_CITY_GROWTH_THRESHOLD, CITY_GROWTH_MULTIPLIER; CvPlayer::getGrowthThreshold'],
       ['Hunger', 'box below zero: emptied, one citizen lost', 'CvCity::doGrowth'],
       ['Box kept after growth', 'Settlement 20 %, Town and City 30 %, Metropolitan 40 % Essentials', 'iFoodKept, CIV4BuildingInfos.xml'],
       ['Pottery, Fermentation, Refrigeration', 'cost %d, %d, %s; %d, %d, %d technologies at least' % (FT['TECH_POTTERY']['cost'], FT['TECH_FERMENTATION']['cost'], fmt(FT['TECH_REFRIGERATION']['cost']), FT['TECH_POTTERY']['fewest'], FT['TECH_FERMENTATION']['fewest'], FT['TECH_REFRIGERATION']['fewest']), 'CIV4TechInfos.xml'],
       ['Plots per city', '21', 'NUM_CITY_PLOTS'],
       ['Game length', '700 turns Normal, 1,470 Marathon', 'CIV4GameSpeedInfo.xml'],
       ['Yields and commerce outputs shown', '3 and 4', 'YieldTypes and CommerceTypes, compiled into the executable'],
       ['Deal item', 'a type and one 32-bit integer', 'TradeData (CvStructs.h), exported to the executable'],
       ['Specialist types today', '19', 'CIV4SpecialistInfos.xml']], [4.2 * cm, 5.4 * cm, 7.4 * cm])
Pp('18.2 Measured in the 30 games', h2)
table([['Quantity', 'Value', 'Source'],
       ['Rebuilt cities fed by their plots', pct(100 - CAL['3']['share'] * 100) + ' of city-turns', 'Settlement Economy, section 4'],
       ['Production over plots, turn 150', '%.2f (median player)' % MU['prod']['150'], 'Settlement Economy, section 5.3'],
       ['Trade routes at the 1.00 floor, turn 150', '%d of %d' % (RT['149']['at_floor'], RT['149']['routes']), 'Settlement Economy, section 5.4'],
       ['Hunger under the food rule', '%.1f to %.1f per 10,000 city-turns' % (min(starve_10k(k) for k in A), max(starve_10k(k) for k in A)), 'Section 6.3'],
       ['Population lost without Pottery, turn 150', '%.0f %%' % -rel('none_capped', 'refrigeration_capped'), 'Section 6.3'],
       ['Food held at the threshold', '%.1f %% of the harvest' % held_share, 'Section 6.3'],
       ['Allocations changed by floating-point order', '%d of %d' % (SN['float']['alloc_differs'], SN['float']['rations']), 'Settlement Economy, section 7.5'],
       ['Resource deals between AIs that paid gold', '%d of %d' % (dict(DE['composition']).get('gold per turn for resource', 0), DE['resource_deals']), 'Settlement Economy, section 5.1'],
       ['Cost per turn, 300 cities and 100 goods', '%.2f ms; %.0f ms with marginal values' % (float(b300['us_per_turn']) / 1000, float(b300['us_per_turn_with_ai_marginals']) / 1000), 'Settlement Economy, section 7.8']],
      [6.0 * cm, 4.6 * cm, 6.4 * cm])
Pp('18.3 Need levels solved from targets', h2)
Pp('The targets are design intents: everyday goods for 8 of 10 citizens, comforts for 5 of 10. Under the recommended rules (goods shared in '
   'the network, stores, spoilage, a governor that knows needs; levels by development, a town %.1f and a city %.1f times a village), a bisection '
   'over one level per need, run on all 30 games each step, gives the levels of section 10. With them, %s of citizens have everyday food '
   'variety, %s clothing, %s fuel and %s comforts. These runs took each city\'s size from the games (the observed population split among a '
   'player\'s cities), so they measure supply, not growth; growth is measured by the food rule of section 6.' %
   (shape[1], shape[2], pct(ch['met']['variety'] * 100), pct(ch['met']['clothing'] * 100), pct(ch['met']['fuel'] * 100), pct(ch['met']['luxury'] * 100)))
figure('v05_needs', 'Left: the share of citizens fully supplied with each need at the solved levels, against its target. Right: how the bisection converged.')
Pp('18.4 Design values and their levers', h2)
Pp('The spoilage rates of section 6.2 are design values: their order follows how fast each food spoils (fish, then meat and dairy, then fruit, '
   'then grain), and their size was set so that missing Pottery costs %.0f %% of turn-150 population and knowing all three costs nothing. '
   'Figure 3 (right) is the lever: the measured cost at every scale from none to three times these rates. These levels hold for the land alone '
   'in the first 150 turns of one scenario. Each later era adds workshops and imports to the supply and must be solved the same way, with the '
   'scenario set widened to the map types RoM ships.' % -rel('none_capped', 'refrigeration_capped'))

# ---------------- 19 ----------------
Pp('19. Architecture', h1)
figure('v04_architecture', 'Where each part lives. The executable is not changed; everything new is DLL, XML and Python.')
Pp('19.1 New classes', h2)
table([['Class', 'Holds', 'Saved'],
       ['CvGoodInfo (XML: CIV4GoodInfos.xml)', 'Tier, spoilage per technology, storage, base price, elasticity, the resource type it reuses for art and text', 'no'],
       ['CvLedger (in CvCity)', 'Per good: stock, made, used, received, sent, spoiled (int tons)', 'yes, behind CvCity\'s uiFlag'],
       ['CvNetworkEconomy (per CvPlotGroup)', 'Recipes in dependency order, rationing, transport capacity, the market', 'derived each turn'],
       ['CvMarket', 'Prices and their history per good', 'yes'],
       ['CvContract (per player pair, in CvDeal)', 'Good, tons per turn, term, price, penalty', 'yes']], [5.0 * cm, 9.0 * cm, 3.0 * cm])
Pp('19.2 Changed functions', h2)
bullets(['<font face="Courier">CvPlayer::doTurn</font>: the economy pass (figure 6) before the loop over cities.',
         '<font face="Courier">CvCity::getBaseYieldRate</font>: food, production and commerce as views of the ledger (equations 2 to 4).',
         '<font face="Courier">CvCity::doGrowth</font>: the box in tons, eaten perishable first, spoiling by the owner\'s technologies; '
         'growth, kept share and hunger unchanged.',
         '<font face="Courier">CvPlot::calculateYield</font> and improvement yields: from land qualities, not resources.',
         '<font face="Courier">CvCity::changeFreeBonus</font>: the bridge that lets resource-type requirements read the ledger during the transition.',
         '<font face="Courier">CvDeal</font>: goods items in tons and contracts; <font face="Courier">CvPlayerAI</font>, <font face="Courier">CvCityAI</font>: the valuation engine.',
         'Map scripts and WorldBuilder loading: provinces from the old resource plots, then the plots cleared.'])
figure('v03_pipeline', 'One economy turn, per trade network, before the engine\'s own turn.')
Pp('19.3 Integers that cannot overflow', h2)
Pp('Every quantity is an integer number of tons, and its width is chosen from a bound taken from the records, not from what the games happened '
   'to reach:')
bullets(['<b>One city, one good: 32-bit.</b> The most food any city could harvest in a turn, with the best plot of every kind on all 21 plots '
         'and every food building and civic at once, is %s food, %s t (the bound is far above any real city). Size is limited by food to %s, '
         'whose threshold is %s t, so a box never exceeds %s t: %s times below the 32-bit limit of %s. In the 30 games the largest harvest was '
         '%s t and the largest box %s t.' % (fmt(BD['city_food']), fmt(BD['city_tons']), fmt(n_max), fmt((30 + 10 * n_max) * 100), fmt(box_max),
                                              fmt((2**31 - 1) // box_max), fmt(2**31 - 1), fmt(A['refrigeration_food']['m']['max_harvest']), fmt(A['refrigeration_food']['m']['max_box'])),
         '<b>Stores are capped.</b> Every stock is held to its storage <i>C</i><sub>g</sub> (equation 1); a delivery beyond it is refused at the '
         'sender, so nothing overflows and nothing vanishes.',
         '<b>Sums and products: 64-bit.</b> Totals over cities, players and the world, and every product (price &times; tons, tons &times; rate) '
         'are computed in 64-bit integers (<font face="Courier">__int64</font>, which the MSVC 2003 compiler of the DLL supports), dividing last.',
         '<b>Deal items</b> carry at most %s t each (section 13); a larger deal takes more items.' % fmt((2**31 - 1) // NGOODS)])
Pp('19.4 Determinism and saves', h2)
Pp('All rules are integer arithmetic in tons, rationing is exact (largest remainders, ties by index), and every random draw (harvests) uses the '
   'synchronised generator; the growth runs of section 6 gave the same result twice. New data sits behind the version flags the classes already '
   'read first. Old saves load with empty ledgers and their food boxes converted at 100 t per unit.')
Pp('19.5 Performance budget', h2)
Pp('Measured in C on the study host: %.2f ms per turn for the goods pass at 300 cities and 100 goods, %.0f ms with the AI\'s marginal values; at 600 '
   'cities and 40 goods, %.2f ms and %.0f ms. The budget for the whole economy is 1 %% of a turn; at today\'s late-turn time of about 20.8 s that is '
   '200 ms.' % (float(b300['us_per_turn']) / 1000, float(b300['us_per_turn_with_ai_marginals']) / 1000, float(b600['us_per_turn']) / 1000, float(b600['us_per_turn_with_ai_marginals']) / 1000))

# ---------------- 20 ----------------
story.append(PageBreak())
Pp('20. Building it', h1)
Pp('The Living Economy is built on one branch, as a whole, not merged piece by piece into today\'s economy. The branch is playable at every '
   'milestone because the bridge (CvCity::changeFreeBonus) keeps every unconverted rule reading goods as resources.')
table([['Milestone', 'Content', 'Done when'],
       ['M1 Ledger, land and food', 'Goods XML; CvLedger in tons; land qualities; plots make goods; the food box in tons with spoilage by technology; the three yields as views; the bridge',
        'Harness: no crash or slower turns (5 seeds); hunger no more frequent than today\'s rule; population at turn 150 within the bracket of section 6.3'],
       ['M2 People and living standards', 'Occupations; workshops; tiers counted in whole citizens; the needs-aware governor; the ledger screen',
        'Harness: 8 of 10 citizens with everyday goods and 5 of 10 with comforts, within 3 points (30 seeds)'],
       ['M3 Markets and money', 'Network markets, prices, commerce from sales; civics as levers', 'Harness: commerce per citizen within 15 % of today\'s by era'],
       ['M4 Trade', 'Goods deal items in tons, convoys, contracts, seeds, the AI\'s deal valuation; the Python trade screen', 'Harness: AI trade volume and its balance; the executable\'s trade screen shows goods items; the user\'s games'],
       ['M5 Industry and war', 'Recipes with tools and power; units costing goods; supply; ammunition', 'Harness: war outcomes against fixed opponents (30 seeds)'],
       ['M6 Later eras and balance', 'Industrial, modern and future goods; need levels per era solved again', 'The user\'s games through the late game']],
      [3.0 * cm, 8.2 * cm, 5.8 * cm])
Pp('Each milestone is a registered prediction judged under the repository\'s rules. The deterministic models are extended with each milestone '
   'first, so every rule is measured on real cities before it is written in the DLL.')

# ---------------- 21 ----------------
Pp('21. Risks', h1)
table([['Risk', 'How the design answers it'],
       ['The AI cannot play it', 'One valuation engine for every decision; measured affordable; each milestone judged on AI outcomes first'],
       ['Too much to manage', 'Distribution is automatic; governors assign work; contracts run themselves; the player sets direction'],
       ['Spoilage stunts the early game', 'Pottery is one technology from every start; its absence costs %.0f %% and its earliest arrival %.1f %% of turn-150 population; the rates are levers with a measured curve' % (-rel('none_capped', 'refrigeration_capped'), -rel('timed_capped', 'refrigeration_capped'))],
       ['Balance collapses when one part changes', 'Need levels and prices are solved from targets, not tuned by hand; the model re-solves them for every change'],
       ['Numbers overflow or drift', 'Whole tons in integers sized from bounds in the records; 64-bit sums; exact rationing; floating point was shown to change allocations'],
       ['The executable\'s screens cannot show it', 'Three yields and four commerce outputs kept as views; new information in Python screens; goods deal items tested first in M4'],
       ['Old saves and scenarios', 'Provinces from old resource plots; version flags; empty ledgers on load'],
       ['Later eras untested', 'M6 re-solves them; the 30 games cover only the first 150 of 700 turns, and no player reached Refrigeration']], [5.4 * cm, 11.6 * cm])


def on_page(c, doc):
    c.saveState(); c.setFont('Helvetica', 7.5); c.setFillColor(INK2)
    if doc.page > 1:
        c.drawString(2.0 * cm, 1.2 * cm, 'The Living Economy: a complete design for Rise of Mankind')
        c.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, str(doc.page))
    c.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.8 * cm, bottomMargin=1.9 * cm,
                        title='The Living Economy', author='Rise of Mankind research', subject='A complete design for the economy')
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUT, EQ[0], 'equations', len(FG), 'figures')
