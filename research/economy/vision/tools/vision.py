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
subs = ['plots, workshops,\nservices', 'in dependency\norder', 'supply, demand,\nprices', 'contracts,\nconvoys', 'needs by tier,\nrationing',
        'spoilage,\ncapacity', 'food, production,\ncommerce', 'growth, builds,\nresearch']
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

# ---------------- title ----------------
story.append(Spacer(1, 2.0 * cm))
Pp('The Living Economy', title)
Pp('A complete design for the economy of Rise of Mankind: land, people, goods, living standards, industry, markets, '
   'trade, the state and war, as one system', sub)
story.append(Spacer(1, 0.6 * cm))
Pp('<b>This document</b> describes the economy as it should be, whole, rather than a sequence of patches. It replaces the map\'s resource '
   'tokens, the on/off resources, the leasing of resources for gold, and the fixed yields of specialists with one ledger of goods. That '
   'ledger is made by people working land and workshops, consumed by the population according to its standard of living, transformed by '
   'industry, priced by markets, carried by trade and taxed by the state. The game\'s three yields and four commerce outputs remain what the '
   'player sees, because the executable\'s screens show exactly those; underneath, they become views of the ledger.', box)
Pp('<b>What it rests on.</b> Every fact about today\'s game is from the mod\'s XML and DLL at GitLab <font face="Courier">main</font> '
   '<font face="Courier">3bec049</font>. Every measured number is from <i>Land, not tokens</i> and <i>Settlement Economy</i> '
   '(research/economy): 30 real harness games, rebuilt city by city, and a deterministic model of goods run on them. Every parameter is either '
   'an anchor taken from the engine, a quantity derived from those measurements, or a design intent stated as such (section 17). The need '
   'levels in this document were not chosen: they were solved for, so that the stated targets are met in the 30 games (section 17.3).', small)
Pp('<b>Contents.</b> 1 Playing it · 2 Pillars · 3 The whole system · 4 What is cut, replaced and kept · 5 The ledger and the three yields · '
   '6 Land · 7 People and work · 8 Goods · 9 Living standards · 10 Production and industry · 11 Markets, money and the state · 12 Trade · '
   '13 War · 14 The eras · 15 The AI · 16 The interface · 17 Numbers and where they come from · 18 Architecture · 19 Building it · 20 Risks', small)
story.append(PageBreak())

# ---------------- 1 ----------------
Pp('1. Playing it', h1)
Pp('<b>2000 BC.</b> Your capital sits where a river crosses warm plains. The overlay shows why the site was good: wheat suits the flood plain '
   'at 0.8, the hills to the north hold copper of grade 0.7, the coast is shelf water. The city of size 4 has two farmers, one herder and one '
   'fisher; it eats 12 units of staple a turn and grows from the surplus as it always did. Its people also want a little meat, wool and firewood; '
   'the ledger shows wool short, so a weaver\'s slot sits empty and two citizens wear rags, which costs one point of contentment. A neighbour '
   'offers wool for your copper. You accept a contract: 2 wool a turn for 1 copper a turn, 20 turns.')
Pp('<b>400 AD.</b> Eleven cities, one network of roads and a river. The market shows grain cheap and wine dear; your coastal cities are fed by '
   'the inland farms, which is why the iron town in the hills could grow to 9 on rock. You know olives and grapes, not rice or sugar; a merchant '
   'from the south sells you rice seed for 300 gold, and the river delta that was marsh becomes paddy over the next ten turns. Your iron province '
   'is running thin at the shallow layer; Explosives is three techs away. You build an arsenal and start putting by arms, because the empire to '
   'the east has twice your swords and its supply of tin runs through your port.')
Pp('<b>1850.</b> Coal and iron meet in the north; four mills turn them into steel, and the steel into rails and rifles. A third of your people '
   'now work in workshops and factories rather than fields, fed by grain bought abroad under a 50-turn contract you renegotiate every war. The '
   'cotton you import is turned into cloth and sold back at three times its price. Your rival blockades the strait; the price of cotton doubles '
   'in a turn, two mills stand idle, and contentment in the textile towns falls. You can pay, fight, or plant cotton in the south, which the '
   'climate overlay says will grow at 0.4.')
Pp('Every one of these situations follows from the rules below. None needs a scripted event.')

# ---------------- 2 ----------------
Pp('2. Pillars', h1)
table([['Pillar', 'Meaning', 'Consequence for the design'],
       ['Material truth', 'Things are made of things. Nothing appears from nowhere or is used without being made', 'One conserved ledger; recipes consume inputs; armies cost goods'],
       ['The land matters', 'Where you are decides what you can do easily, and what you must trade for', 'No tokens; climate, soil, ore and sea as qualities of every plot'],
       ['People are the economy', 'Output is work; what people need decides what they do and how content they are', 'Occupations; living standards by tier; needs grow with size'],
       ['Legibility', 'Every number can be traced to its cause in two clicks', 'Ledger screen; overlays; help text that names the plot, worker and building'],
       ['Consequence without micromanagement', 'Choices are about direction, not clicks', 'Automatic distribution within networks; governors that know needs; contracts that run themselves'],
       ['AI parity', 'The AI plays the same economy and understands it', 'One valuation engine for every AI decision (section 15)'],
       ['Determinism', 'Every computer reaches the same result, bit for bit', 'Integers in hundredths; exact rationing; the game\'s synchronised random numbers']],
      [3.2 * cm, 6.4 * cm, 7.4 * cm])

# ---------------- 3 ----------------
Pp('3. The whole system', h1)
figure('v01_gestalt', 'The economy as one system. Land and people produce work; work fills the goods ledger; goods feed living standards, '
       'industry, markets, trade and armies; markets produce commerce for the state; growth makes people; armies win land; policy shapes work.')
Pp('There are three loops, and every mechanic belongs to at least one. The <b>loop of life</b>: land and work make staple and everyday goods, '
   'which make people grow and stay content, which makes more work. The <b>loop of wealth</b>: surplus goods are sold in markets, commerce is '
   'taxed into gold, research and culture, which buy buildings and technology that make work more productive. The <b>loop of power</b>: goods '
   'make and supply armies, armies take or protect land and trade, and land and trade feed the other two loops.')
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
       ['A resource is on or off for a network', 'Cut. Goods are quantities, made and used each turn', 'Scarcity, specialisation and trade become possible'],
       ['+1 happiness or health per resource, whatever the city\'s size', 'Replaced. Living standards by tier, met per citizen', 'Large cities need more; luxury becomes a matter of supply'],
       ['Leasing a resource copy for gold per turn', 'Replaced. Shipments, contracts, seeds and livestock, packages', 'Between AIs, %d of %d resource deals were swaps of copies and %d paid gold' % (dict(DE['composition']).get('resource for resource', 0), DE['resource_deals'], dict(DE['composition']).get('gold per turn for resource', 0))],
       ['Buildings that need resources present and give a copy', 'Replaced. Recipes that turn inputs into outputs, run by workers', 'Factories should use what they need'],
       ['Specialists with fixed yields', 'Replaced. Occupations that produce goods (smith, weaver, miller) or services (merchant, scholar, priest)', 'Work is what makes goods'],
       ['Trade routes worth 1.00 commerce times modifiers', 'Replaced. Convoys that carry goods, earning on what they carry', 'On this map %d of %d routes paid exactly the floor' % (RT['149']['at_floor'], RT['149']['routes'])],
       ['Food, production, commerce on the city screen', 'Kept, as views of the ledger', 'The executable\'s screens show exactly these'],
       ['Gold, research, culture, espionage sliders', 'Kept. They split taxed commerce as today', 'Same'],
       ['Growth thresholds, food per citizen', 'Kept: 3 staple per citizen, threshold 30 + 10 &times; size', 'The pacing of 700 turns rests on them'],
       ['Civics, technologies, buildings', 'Kept and re-aimed: civics become economic levers; buildings become capital', 'The tree and the tech web stay; their effects become material']],
      [4.4 * cm, 6.6 * cm, 6.0 * cm])

# ---------------- 5 ----------------
story.append(PageBreak())
Pp('5. The ledger and the three yields', h1)
Pp('Every city keeps one ledger: for every good <i>g</i>, its stock <i>X</i>, what it made <i>q</i>, received <i>m</i>, used <i>u</i> and sent '
   '<i>x</i> this turn, in integer hundredths. Every flow in the game is a line in some ledger, so goods are conserved exactly:')
eq(r'X_{g,t+1} = \min\left(C_g,\ X_{g,t} + q_{g,t} + m_{g,t} - u_{g,t} - x_{g,t} - \left\lfloor \frac{s_g (X_{g,t} + q_{g,t} + m_{g,t} - u_{g,t} - x_{g,t})}{100} \right\rfloor \right)')
Pp('The three yields become views of the ledger, so the city screen, the growth rule, the build queue and the sliders work unchanged:')
eq(r'\mathrm{Food} = \frac{1}{100}\sum_{g \in staple} (q_g + m_g + \mathrm{draw}_g)')
eq(r'\mathrm{Production} = \frac{1}{100}\, L_{work}\, \pi_0 \,(1 + \tau)(1 + \kappa) + P_{ind}')
eq(r'\mathrm{Commerce} = \frac{1}{100}\left(\sum_g p_g\, \mathrm{sold}_g\, \mu + \mathrm{services} + \mathrm{convoys}\right)')
Pp('Food is the staple a city has to eat this turn, so <font face="Courier">CvCity::foodDifference</font> = Food &minus; 3 &times; population '
   'keeps its meaning. Production is the work of the citizens not producing goods, times their tools &tau; and power &kappa;, plus <i>P<sub>ind</sub></i>, what '
   'industry produces as construction capacity. Commerce is what the city\'s market earns from goods sold at price <i>p</i> with margin &mu;, '
   'plus services (merchants, banks) and convoys. The sliders split commerce into gold, research, culture and espionage exactly as now. The '
   'engine\'s percentage modifiers (<font face="Courier">CvCity::getBaseYieldRateModifier</font>) stay, applied to these views, so every '
   'building and civic that changes a yield keeps working while it is re-aimed at goods.')

# ---------------- 6 ----------------
Pp('6. Land', h1)
Pp('Land is described in <i>Land, not tokens</i> and adopted whole: per plot, a climate (annual temperature, seasons that turn with the hemisphere, '
   'water, growing season), a soil that wears with farming and recovers, geological provinces with ore grade and three layers of reserves, and '
   'for water, a carrying capacity for fish. On the 30 games\' map the reconstruction checked it against the games themselves: the rebuilt '
   'cities\' worked plots feed their observed populations on %s of city-turns.' % pct(100 - CAL['3']['share'] * 100))
table([['Land use (the improvement)', 'What it makes', 'Depends on'],
       ['Farm (of a crop the civilization knows)', 'Staple or a cash crop', 'Crop suitability, soil, irrigation; Latifundium stages as estates'],
       ['Pasture', 'Meat, dairy, wool, hides, horses', 'Grass, climate; the breed known'],
       ['Orchard, vineyard, olive grove', 'Fruit, oil, wine', 'Mediterranean climate; years to bear'],
       ['Plantation', 'Sugar, cotton, coffee, tea, tobacco, spices', 'Tropical climate; labour regime (section 11.4)'],
       ['Mine, Shaft Mine, Modern Mine', 'Ores, coal, stone, salt', 'Province grade; depth reached; reserves left'],
       ['Lumber camp, then forestry', 'Timber, charcoal', 'Forest; regrowth'],
       ['Fishing fleet', 'Fish', 'Fishing ground capacity and stock'],
       ['Town, then city district', 'Services, housing', 'Population; the land\'s commerce today']], [5.2 * cm, 5.2 * cm, 6.6 * cm])

# ---------------- 7 ----------------
Pp('7. People and work', h1)
Pp('Every citizen has an occupation. The engine already distinguishes citizens working a plot from specialists; the Living Economy uses '
   'that distinction and fills it with meaning. RoM defines 19 specialist types today; they become the occupations below, defined in XML.')
table([['Occupation', 'Where', 'Makes'],
       ['Farmer, herder, fisher, miner, forester', 'A worked plot', 'The plot\'s goods (section 6)'],
       ['Artisan: smith, weaver, potter, miller, brewer, carpenter', 'A workshop slot of a building', 'The building\'s recipe, one run per artisan'],
       ['Worker (from the industrial era)', 'A factory slot', 'The factory\'s recipe, several runs per worker with power'],
       ['Merchant', 'A market slot', 'Commerce: margin on goods sold; convoy capacity'],
       ['Scholar, priest, artist, official', 'Library, temple, theatre, court', 'Research, culture, contentment, administration'],
       ['Labourer (no slot)', 'The city', 'Production: building and training work']], [5.0 * cm, 4.6 * cm, 7.4 * cm])
Pp('The city governor assigns occupations by marginal value: each citizen goes where one more worker adds most to the city\'s living standard '
   'and output (section 15). In the model that measured this, a governor that knew the city\'s needs lowered the share of citizens short of fuel '
   'from %s to %s and of everyday food variety from %s to %s compared with one that ranked plots by yields alone.' %
   (pct(S['network_store_spoil']['fuel']), pct(S['aware_network_store_spoil']['fuel']), pct(S['network_store_spoil']['variety']), pct(S['aware_network_store_spoil']['variety'])))
Pp('<b>Labour regimes</b> are civics, and they change how work is done, not a percentage: tribal labour (everyone farms), slavery (cheap '
   'plantation and mine labour, unrest, no artisans above a size), serfdom (estates bound to land), free labour (artisans and merchants '
   'possible; wages), industrial labour (factory workers). Each sets which occupations exist, their output per worker and their effect on contentment.')

# ---------------- 8 ----------------
story.append(PageBreak())
Pp('8. Goods', h1)
Pp('About forty goods carry the whole game. The catalogue keeps today\'s resource types as names wherever they fit, so that existing art, '
   'Civilopedia text and requirements can be reused.')
table([['Era of first use', 'Raw goods', 'Made goods (inputs)'],
       ['Ancient', 'Grain (wheat, rice, maize, potato), fish, meat and dairy, fruit, wool, hides, timber, stone, clay, copper, salt', 'Pottery (clay, fuel), bronze (copper, tin from trade), cloth (wool), beer and wine (grain, fruit)'],
       ['Classical', 'Iron ore, tin, marble, olives, grapes, incense, dye', 'Iron tools and arms (iron, charcoal), oil (olives), fine cloth (wool, dye), coin metal (silver, gold)'],
       ['Medieval', 'Horses, silk, spices, furs', 'Plate armour (iron), paper and books (timber, scholars), glass (sand, fuel), furniture (timber)'],
       ['Renaissance', 'Sugar, coffee, tea, tobacco, cotton', 'Gunpowder (sulphur, saltpetre), ships\' stores, refined sugar, porcelain'],
       ['Industrial', 'Coal, lead, sulphur, rubber', 'Steel (iron, coal), machinery (steel), rails (steel), textiles (cotton), ammunition (lead, sulphur), chemicals'],
       ['Modern', 'Oil, bauxite, uranium', 'Fuel (oil), aluminium (bauxite, power), plastics, electronics, consumer goods, fertilizer, medicine'],
       ['Transhuman and future', '(engineered)', 'Nanotubes, nanobots, personal replicators: the goods that end scarcity, as RoM\'s future era already names them']],
      [2.6 * cm, 6.6 * cm, 7.8 * cm])
Pp('<b>Rules for the catalogue.</b> A good exists only if a choice turns on it: a different land, a different building, a different trade '
   'partner. Goods that would always travel together are one good (meat and dairy). Each era adds goods that make the previous era\'s goods '
   'more valuable (iron makes tools that make every farm more productive). Every made good has at least one raw good that some civilizations '
   'lack, so that trade is never optional for everyone. The catalogue size costs almost nothing to compute: %.2f ms per turn at 300 cities and '
   '100 goods (section 18.4).' % (float(b300['us_per_turn']) / 1000))

# ---------------- 9 ----------------
Pp('9. Living standards', h1)
Pp('Each citizen consumes from four tiers. A tier is met in a city when every good of the tier is supplied at its level per citizen. Tiers are '
   'nested: a city aspires to comforts only once its everyday goods are met.')
table([['Tier', 'Goods (substitutes in each line)', 'If met', 'If short'],
       ['Staple', 'grain · fish', 'Growth from the surplus', 'Starvation (the engine\'s rule)'],
       ['Everyday', 'meat, dairy or fruit · wool or cloth · timber, charcoal or coal', 'Health, +1 contentment', 'Illness, &minus;1 contentment, less work'],
       ['Comfort', 'salt · wine or beer · pottery or furniture · (later) sugar, tea, coffee', '+1 or +2 contentment; artisans and merchants possible', 'No unrest; no higher occupations'],
       ['Luxury', 'spices, silk, fine cloth, dye, jewellery, porcelain', 'Culture, great people, contentment', 'Nothing lost: luxury is aspiration']],
      [2.0 * cm, 6.8 * cm, 4.6 * cm, 3.6 * cm])
Pp('<b>Levels by development.</b> A village (size 1 to 3) wants the base level; a town (4 to 8) %.1f times it per citizen; a city (9 and more) '
   '%.1f times. Contentment from a tier grows with the share met, with diminishing returns:' % (shape[1], shape[2]))
eq(r'\eta_{tier} = H_{tier}\left(1 - e^{-\,c/k}\right), \qquad c = \frac{\mathrm{supplied}}{\mathrm{level} \times \mathrm{population}}')
Pp('The base levels were solved for, not chosen (section 17.3). With the targets that most citizens have their everyday goods (%d %%) and half '
   'have comforts (%d %%), the levels that meet them in the 30 games are, per citizen of a village and turn: everyday food %.2f, clothing %.2f, '
   'fuel %.2f; comfort %.2f.' % (round(ND['target']['variety'] * 100), round(ND['target']['luxury'] * 100), lev['variety'] / 100, lev['clothing'] / 100,
                                 lev['fuel'] / 100, lev['luxury'] / 100))

# ---------------- 10 ----------------
Pp('10. Production and industry', h1)
Pp('A building with a recipe has slots; each artisan in a slot runs the recipe once per turn if the inputs are there. Output follows the scarcest '
   'input (fixed proportions), and tools and power raise output per worker:')
eq(r'n_k = \min\left(w_k\, r_k (1 + \tau)(1 + \kappa),\ \min_g \frac{\alpha_{g,k} X_g}{a_{g,k}}\right)')
Pp('<i>w</i> is the number of workers, <i>r</i> runs per worker, &alpha; the building\'s share of a scarce input (exact proportional rationing). '
   'Tools are themselves a good that wears out: each worker using tools consumes a fraction of a tool per turn, so iron and fuel stay in demand '
   'for the whole game. Power (from the industrial era) is a network good produced by plants from fuel.')
Pp('<b>The industrial revolution</b> is the moment workshops overtake land, which figure 2 shows happening already in the 30 games\' first 150 '
   'turns. In the Living Economy it is the moment coal, iron and power let a worker run several recipes instead of one, which draws people from '
   'farms into factories and makes the empire depend on fed cities it does not feed itself.')

# ---------------- 11 ----------------
story.append(PageBreak())
Pp('11. Markets, money and the state', h1)
Pp('11.1 Markets', h2)
Pp('Each trade network has one market. After production and recipes, every surplus is offered and every unmet need bid; goods move from '
   'surplus to need inside the network automatically, limited by the network\'s transport capacity. The price of a good in the network follows '
   'its scarcity, within bounds so that no single turn can ruin a city:')
eq(r'p_g = p^0_g\ \mathrm{clamp}\left(\left(\frac{D_g}{S_g}\right)^{1/\varepsilon_g},\ \frac{1}{5},\ 5\right)')
Pp('Prices are shown to the player and used by the AI. Sharing within a network is what keeps cities fed: in the 30 games, staple kept in each '
   'city left %s of citizen-turns short; shared in the network %s; with granaries %s.' % (pct(S['goods_local']['staple']), pct(S['goods_network']['staple']), pct(S['network_store']['staple'])))
Pp('11.2 Money', h2)
Pp('Commerce is what the market earns: the margin on goods sold, plus services. The state taxes it, and the sliders split the tax into gold, '
   'research, culture and espionage as today. Coin metal (silver, gold) raises the margin a market can take; banks raise it further. Money is '
   'what buys goods across networks and from other civilizations; it is never created except by trade and taxation.')
Pp('11.3 Buildings as capital', h2)
Pp('Buildings keep their roles but act on goods: a granary stores staple and keeps part of the food box after growth (Town Essentials keeps 30 %% '
   'today); a market adds merchant slots and margin; a harbour adds sea transport capacity and fishing fleets; a forge is a workshop of smiths. '
   'Of today\'s %d buildings, %d give specialist slots, which become workshop slots; %d add trade routes, which become transport capacity.' %
   (SN['bc']['buildings'], SN['bc']['specialists'], SN['bc']['trade_routes']))
Pp('11.4 Civics as economic levers', h2)
table([['Civic category', 'Today (examples)', 'In the Living Economy'],
       ['Administration (Oral Law, Tablets, ...)', 'Oral Law: food &minus;25 %, production &minus;25 %, commerce &minus;10 %', 'How much of the ledger the state sees and taxes; spoilage and waste in stores'],
       ['Economy (Hunter-Gatherer, Barter, Coinage, Planned, ...)', 'Trade yield modifiers; Planned: trade gives +50 % food and production', 'How markets clear: barter (no money, swaps only), coinage (prices), planned (the state allocates)'],
       ['Employment (Slavery, Caste System, Labor Allocation, ...)', 'Yields added to classes of improvements', 'The labour regime (section 7): which occupations exist and their output'],
       ['Taxation (Tribute, Census, National Debt, ...)', 'Capital and yield modifiers', 'The share of commerce taxed, tariffs on foreign goods, debt'],
       ['Trade policy (inside Economy today)', 'National Socialism forbids foreign trade', 'Free trade, mercantilism (tariffs, colonies), autarky (embargo)']],
      [4.2 * cm, 6.0 * cm, 6.8 * cm])
Pp('The starting civic Oral Law shows why civics must become levers on the ledger rather than percentages: applied to food, its &minus;25 %% would '
   'leave the rebuilt cities unable to feed their observed populations on %s of city-turns instead of %s (Settlement Economy, section 5.3).' % (pct(OR['short_oral']), pct(OR['short_plain'])))

# ---------------- 12 ----------------
Pp('12. Trade', h1)
Pp('<b>Inside a civilization</b> goods move freely within a network (roads, rivers, harbours connect it); between a civilization\'s separate '
   'networks they move by convoy. <b>Between civilizations</b> they move by convoys along trade routes, under contracts or as spot sales.')
table([['Instrument', 'What it is', 'Engine'],
       ['Spot sale', 'Goods sold now at the partner\'s market price', 'A deal item per good and quantity'],
       ['Contract', 'Quantity per turn, for a term, at a price; penalties for default; cancelled by war', 'Repeated TRADE_RESOURCES items at first (TradeData has no quantity field); a Python trade screen later'],
       ['Seeds, breeding stock, techniques', 'The means to produce a good: the buyer can plant, breed or build it', 'A deal item like a technology'],
       ['Package', 'Any combination with gold, technologies, treaties', 'The existing deal structure'],
       ['Tariffs, embargo, blockade', 'A share of value taken at the border; no trade; ships cut a sea route', 'Civics; diplomacy; naval units on route plots']],
      [3.4 * cm, 7.6 * cm, 6.0 * cm])
Pp('A trade route becomes a convoy\'s capacity: it carries goods worth its capacity per turn and earns the price difference. In the 30 games, '
   'all trade that could happen between players needed %.2f units per route per turn with one route per city, so routes become a real constraint '
   'only as trade grows, which is the intent: harbours, roads and ships matter because they carry goods.' % SN['route_need']['per_route'])
Pp('<b>The AI trades by value.</b> A deal is worth the sum of the marginal values (section 15) of what is received minus what is given, '
   'including the strategic value of giving a rival the means to produce. This replaces the random offers and fixed resource values that the '
   'diplomacy work of merge request !63 began to remove.')

# ---------------- 13 ----------------
Pp('13. War', h1)
Pp('Units are built from production and goods (a legion needs iron arms; a ship of the line timber, cannon and canvas; a tank steel, fuel and '
   'ammunition). Armies in the field draw supplies each turn from the nearest connected city; a unit cut off loses strength. Battles consume '
   'ammunition from the industrial era on. Blockades and raids on provinces become ways to win: a country without steel cannot replace its '
   'tanks. An arsenal stores arms in peace; the model showed a 90-turn war emptying a 60-unit arsenal by its eleventh turn (Land, not tokens, '
   'section 9).')

# ---------------- 14 ----------------
story.append(PageBreak())
Pp('14. The eras', h1)
table([['Era', 'The economy\'s question', 'What changes'],
       ['Ancient', 'Can we feed ourselves and clothe ourselves?', 'Staple and everyday tiers; bronze needs copper and tin, rarely found together'],
       ['Classical', 'Who controls iron and the roads?', 'Iron tools raise all work; coinage creates markets; roads join networks'],
       ['Medieval', 'Can the towns grow beyond the land?', 'Guild workshops; mills (power from water and wind); estates and serfdom'],
       ['Renaissance', 'Who controls the sea and the colonial goods?', 'Comfort goods from the tropics; banks; mercantilist trade'],
       ['Industrial', 'Coal, iron and the factory', 'Workers run several recipes; power; railways move goods; cities outgrow their farms'],
       ['Modern', 'Oil and the consumer', 'Oil and electricity; consumer goods raise living standards; global supply chains'],
       ['Transhuman', 'Automation', 'Androids (RoM\'s specialist) and automated factories: work stops being people'],
       ['Future', 'The end of scarcity', 'Replicators make goods from energy; the ledger\'s constraints relax by design']],
      [2.4 * cm, 5.0 * cm, 9.6 * cm])
Pp('A Normal game lasts 700 turns (Marathon 1,470); the 30 measured games cover its first 150. Each era\'s goods should become important within '
   'its first third and remain useful after: the design target is that no good introduced in an era stops mattering before the era after next.')

# ---------------- 15 ----------------
Pp('15. The AI', h1)
Pp('The AI uses one quantity for every economic decision: the marginal value of one unit per turn of each good to each of its networks, the '
   'change in its weighted living standards and output when that supply rises by one:')
eq(r'v_g = V(\mathbf{q} + \mathbf{e}_g) - V(\mathbf{q}), \qquad V = \sum_{cities} \left(\sum_{tier} \omega_{tier}\, \eta_{tier} + \omega_F F + \omega_P P + \omega_C C\right)')
Pp('Computed by recomputing the network once per good, it costs %.0f ms per turn at 300 cities and 100 goods on the measured host, against a '
   'late turn of about 20.8 s today (section 18.4). It drives: occupations and plots (the governor); what to build (recipes whose outputs are '
   'worth more than their inputs and labour); what to plant and where to prospect; what to offer, ask and accept in trade; when stores are '
   'worth filling; and which provinces and routes are worth a war. Because every decision uses the same values, the AI cannot be '
   'inconsistent across them, which is the failure mode of today\'s separate fixed weights.' % (float(b300['us_per_turn_with_ai_marginals']) / 1000))

# ---------------- 16 ----------------
Pp('16. The interface', h1)
bullets(['<b>City ledger screen</b> (Python): every good made, used, stored, received; each tier\'s share met, with the citizens short and why.',
         '<b>Land overlays</b>: crop suitability, ore grade and depth, fishing grounds, climate; on the map through coloured plots, the API the '
         'strategy overlay already uses.',
         '<b>Market screen</b>: the network\'s prices and their history; what is short; what sells.',
         '<b>Contracts and convoys</b>: what flows in and out, with whom, until when.',
         '<b>Plot and city help</b>: every number names its cause (this plot, this worker, this building, this civic).',
         '<b>Advisors</b>: shortages and opportunities in one line each: "Iron town short of grain for 3 turns: the road to the farms is cut".'])

# ---------------- 17 ----------------
story.append(PageBreak())
Pp('17. Numbers and where they come from', h1)
Pp('17.1 Anchors from the engine', h2)
table([['Quantity', 'Value', 'Source'],
       ['Staple per citizen', '3 per turn', 'FOOD_CONSUMPTION_PER_POPULATION (GlobalDefines.xml)'],
       ['Growth threshold', '30 + 10 &times; size', 'BASE_CITY_GROWTH_THRESHOLD, CITY_GROWTH_MULTIPLIER; CvPlayer::getGrowthThreshold'],
       ['Plots per city', '21', 'NUM_CITY_PLOTS'],
       ['Game length', '700 turns Normal, 1,470 Marathon', 'CIV4GameSpeedInfo.xml'],
       ['Yields and commerce outputs shown', '3 and 4', 'YieldTypes and CommerceTypes, compiled into the executable'],
       ['Deal item', 'a type and one integer', 'TradeData (CvStructs.h), exported to the executable'],
       ['Mine depths', 'Mine, Shaft Mine, Modern Mine: production +1, +2, +8', 'CIV4ImprovementInfos.xml'],
       ['Specialist types today', '19', 'CIV4SpecialistInfos.xml']], [4.2 * cm, 5.0 * cm, 7.8 * cm])
Pp('17.2 Measured in the 30 games', h2)
table([['Quantity', 'Value', 'Source'],
       ['Rebuilt cities fed by their plots', pct(100 - CAL['3']['share'] * 100) + ' of city-turns', 'Settlement Economy, section 4'],
       ['Production over plots, turn 150', '%.2f (median player)' % MU['prod']['150'], 'Settlement Economy, section 5.3'],
       ['Trade routes at the 1.00 floor, turn 150', '%d of %d' % (RT['149']['at_floor'], RT['149']['routes']), 'Settlement Economy, section 5.4'],
       ['Staple short: local / shared / with stores', '%s / %s / %s' % (pct(S['goods_local']['staple']), pct(S['goods_network']['staple']), pct(S['network_store']['staple'])), 'Settlement Economy, section 7.1'],
       ['Production lost to whole units', pct(SN['round_loss']['whole_units']), 'Settlement Economy, section 7.5'],
       ['Allocations changed by floating-point order', '%d of %d' % (SN['float']['alloc_differs'], SN['float']['rations']), 'Settlement Economy, section 7.5'],
       ['Resource deals between AIs that paid gold', '%d of %d' % (dict(DE['composition']).get('gold per turn for resource', 0), DE['resource_deals']), 'Settlement Economy, section 5.1'],
       ['Cost per turn, 300 cities and 100 goods', '%.2f ms; %.0f ms with marginal values' % (float(b300['us_per_turn']) / 1000, float(b300['us_per_turn_with_ai_marginals']) / 1000), 'Settlement Economy, section 7.8']],
      [6.0 * cm, 4.6 * cm, 6.4 * cm])
Pp('17.3 Need levels solved from targets', h2)
Pp('The targets are design intents: everyday goods for %d %% of citizens, comforts for %d %%, and staple shortage no worse than today\'s rules '
   '(%s). Under the recommended rules (staple shared, granaries, spoilage, a governor that knows needs; levels by development, a town %.1f and a '
   'city %.1f times a village), a bisection over one level per need, run on all 30 games each step, gives the levels in section 9. With them, '
   '%s of citizens have everyday food, %s clothing, %s fuel and %s comforts, and %s of citizen-turns are short of staple.' %
   (round(ND['target']['variety'] * 100), round(ND['target']['luxury'] * 100), pct(S['today_food']['staple']), shape[1], shape[2],
    pct(ch['met']['variety'] * 100), pct(ch['met']['clothing'] * 100), pct(ch['met']['fuel'] * 100), pct(ch['met']['luxury'] * 100), pct(ch['staple_short'] * 100)))
figure('v05_needs', 'Left: the share of citizens fully supplied with each need at the solved levels, against its target. Right: how the bisection converged.')
Pp('These levels hold for the land alone in the first 150 turns of one scenario. Each later era adds workshops and imports to the supply and '
   'must be solved the same way, with the scenario set widened to the map types RoM ships.')

# ---------------- 18 ----------------
Pp('18. Architecture', h1)
figure('v04_architecture', 'Where each part lives. The executable is not changed; everything new is DLL, XML and Python.')
Pp('18.1 New classes', h2)
table([['Class', 'Holds', 'Saved'],
       ['CvGoodInfo (XML: CIV4GoodInfos.xml)', 'Unit, tier, spoilage, storage, base price, elasticity, the resource type it reuses for art and text', 'no'],
       ['CvLedger (in CvCity)', 'Per good: stock, made, used, received, sent (int hundredths)', 'yes, behind CvCity\'s uiFlag'],
       ['CvNetworkEconomy (per CvPlotGroup)', 'Recipes in dependency order, rationing, transport capacity, the market', 'derived each turn'],
       ['CvMarket', 'Prices and their history per good', 'yes'],
       ['CvContract (per player pair, in CvDeal)', 'Good, quantity per turn, term, price, penalty', 'yes']], [5.0 * cm, 9.0 * cm, 3.0 * cm])
Pp('18.2 Changed functions', h2)
bullets(['<font face="Courier">CvPlayer::doTurn</font>: the economy pass (figure 5) before the loop over cities.',
         '<font face="Courier">CvCity::getBaseYieldRate</font>: food, production and commerce as views of the ledger (equations 2 to 4).',
         '<font face="Courier">CvCity::foodDifference</font>, <font face="Courier">doGrowth</font>: unchanged in form; they read the views.',
         '<font face="Courier">CvPlot::calculateYield</font> and improvement yields: from land qualities, not resources.',
         '<font face="Courier">CvCity::changeFreeBonus</font>: the bridge that lets resource-type requirements read the ledger during the transition.',
         '<font face="Courier">CvDeal</font>: contracts; <font face="Courier">CvPlayerAI</font>, <font face="Courier">CvCityAI</font>: the valuation engine.',
         'Map scripts and WorldBuilder loading: provinces from the old resource plots, then the plots cleared.'])
figure('v03_pipeline', 'One economy turn, per trade network, before the engine\'s own turn.')
Pp('18.3 Determinism and saves', h2)
Pp('All rules are integer arithmetic in hundredths, rationing is exact (largest remainders, ties by index), and every random draw (harvests) '
   'uses the synchronised generator. New data sits behind the version flags the classes already read first. Old saves load with empty ledgers.')
Pp('18.4 Performance budget', h2)
Pp('Measured in C on the study host: %.2f ms per turn for the goods pass at 300 cities and 100 goods, %.0f ms with the AI\'s marginal values; at 600 '
   'cities and 40 goods, %.2f ms and %.0f ms. The budget for the whole economy is 1 %% of a turn; at today\'s late-turn time of about 20.8 s that is '
   '200 ms.' % (float(b300['us_per_turn']) / 1000, float(b300['us_per_turn_with_ai_marginals']) / 1000, float(b600['us_per_turn']) / 1000, float(b600['us_per_turn_with_ai_marginals']) / 1000))

# ---------------- 19 ----------------
story.append(PageBreak())
Pp('19. Building it', h1)
Pp('The Living Economy is built on one branch, as a whole, not merged piece by piece into today\'s economy. The branch is playable at every '
   'milestone because the bridge (CvCity::changeFreeBonus) keeps every unconverted rule reading goods as resources.')
table([['Milestone', 'Content', 'Done when'],
       ['M1 Ledger and land', 'Goods XML; CvLedger; land qualities; plots make goods; staple as a shared good; the three yields as views; the bridge',
        'Harness: no crash or slower turns (5 seeds); food shortage within 1 point of today\'s; growth curves within 10 %'],
       ['M2 People and living standards', 'Occupations; workshops; tiers and contentment; the needs-aware governor; the ledger screen',
        'Harness: tier shares in the target bands of section 17.3 (30 seeds)'],
       ['M3 Markets and money', 'Network markets, prices, commerce from sales; civics as levers', 'Harness: commerce per citizen within 15 % of today\'s by era'],
       ['M4 Trade', 'Convoys, contracts, seeds, the AI\'s deal valuation; the Python trade screen', 'Harness: AI trade volume and its balance; the user\'s games'],
       ['M5 Industry and war', 'Recipes with tools and power; units costing goods; supply; ammunition', 'Harness: war outcomes against fixed opponents (30 seeds)'],
       ['M6 Later eras and balance', 'Industrial, modern and future goods; need levels per era solved again', 'The user\'s games through the late game']],
      [3.0 * cm, 8.2 * cm, 5.8 * cm])
Pp('Each milestone is a registered prediction judged under the repository\'s rules. The deterministic model of Settlement Economy is extended '
   'with each milestone first, so every rule is measured on real cities before it is written in the DLL.')

# ---------------- 20 ----------------
Pp('20. Risks', h1)
table([['Risk', 'How the design answers it'],
       ['The AI cannot play it', 'One valuation engine for every decision; measured affordable; each milestone judged on AI outcomes first'],
       ['Too much to manage', 'Distribution is automatic; governors assign work; contracts run themselves; the player sets direction'],
       ['Balance collapses when one part changes', 'Need levels and prices are solved from targets, not tuned by hand; the model re-solves them for every change'],
       ['Multiplayer goes out of sync', 'Integer arithmetic and exact rationing; floating point was shown to change allocations'],
       ['The executable\'s screens cannot show it', 'Three yields and four commerce outputs kept as views; new information in Python screens'],
       ['Old saves and scenarios', 'Provinces from old resource plots; version flags; empty ledgers on load'],
       ['Later eras untested', 'M6 re-solves them; the 30 games cover only the first 150 of 700 turns']], [5.4 * cm, 11.6 * cm])


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
