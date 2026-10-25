#!/usr/bin/env python3
"""Builds land-and-industry.pdf from figures/ and data/ (tools/figures.py). Every quoted number is read
from data/numbers.json or data/facts.json; equations are rendered with matplotlib's mathtext.

usage: build_pdf.py <research/economy dir>
"""
import io, json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle, ListFlowable, ListItem)

ROOT = sys.argv[1]
N = json.load(open(os.path.join(ROOT, 'data', 'numbers.json')))
F = json.load(open(os.path.join(ROOT, 'data', 'facts.json')))
FIG = os.path.join(ROOT, 'figures')
OUT = os.path.join(ROOT, 'land-and-industry.pdf')
TEXTW = A4[0] - 4.0 * cm

INK, INK2, BLUE, ORANGE = colors.HexColor('#0b0b0b'), colors.HexColor('#52514e'), colors.HexColor('#2a78d6'), colors.HexColor('#eb6834')
ss = getSampleStyleSheet()
body = ParagraphStyle('body', parent=ss['BodyText'], fontName='Helvetica', fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=5)
small = ParagraphStyle('small', parent=body, fontSize=8.2, leading=11)
cap = ParagraphStyle('cap', parent=body, fontSize=7.9, leading=10.4, textColor=INK2, spaceBefore=2, spaceAfter=10)
h1 = ParagraphStyle('h1', parent=ss['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=INK, spaceBefore=10, spaceAfter=7)
h2 = ParagraphStyle('h2', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=11.2, leading=14.5, textColor=INK, spaceBefore=9, spaceAfter=4)
h3 = ParagraphStyle('h3', parent=body, fontName='Helvetica-Bold', fontSize=9.6, spaceBefore=5, spaceAfter=2)
title = ParagraphStyle('title', parent=h1, fontSize=24, leading=29, spaceAfter=10)
sub = ParagraphStyle('sub', parent=body, fontSize=11.5, leading=15.5, textColor=INK2)
cell = ParagraphStyle('cell', parent=body, fontSize=7.9, leading=10, spaceAfter=0)
cellb = ParagraphStyle('cellb', parent=cell, fontName='Helvetica-Bold')
box = ParagraphStyle('box', parent=body, fontSize=9.2, leading=13, backColor=colors.HexColor('#eef4fc'),
                     borderColor=BLUE, borderWidth=0.6, borderPadding=7, spaceBefore=6, spaceAfter=12)

for _st in (h1, h2, h3): _st.keepWithNext = 1
story = []
P = lambda t, st=body: story.append(Paragraph(t, st))
EQN = [0]


def eq(tex, size=11.5, note=None):
    """A numbered display equation rendered by mathtext."""
    EQN[0] += 1
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, '$' + tex + '$', fontsize=size, color='#0b0b0b')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0.03, transparent=True)
    plt.close(fig)
    buf.seek(0)
    from PIL import Image as PI
    w, h = PI.open(buf).size; buf.seek(0)
    scale = 72.0 / 300
    img = Image(buf, width=w * scale, height=h * scale)
    t = Table([[img, Paragraph('(%d)' % EQN[0], ParagraphStyle('n', parent=body, alignment=2, textColor=INK2))]],
              colWidths=[TEXTW - 1.2 * cm, 1.2 * cm])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (0, 0), 14),
                           ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    story.append(t)
    if note: P(note, small)
    return EQN[0]


FIGN = [0]


def figure(name, caption, width=TEXTW):
    FIGN[0] += 1
    from PIL import Image as PI
    path = os.path.join(FIG, name + '.png')
    w, h = PI.open(path).size
    img = Image(path, width=width, height=width * h / w)
    story.append(KeepTogether([img, Paragraph('<b>Figure %d.</b> %s' % (FIGN[0], caption), cap)]))
    return FIGN[0]


def table(rows, widths, header=True, size=None):
    data = [[Paragraph(str(c), cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#d9d8d3')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
          ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    if header: st.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f0ec')))
    t.setStyle(TableStyle(st))
    story.append(t); story.append(Spacer(1, 8))


def bullets(items, st=body):
    story.append(ListFlowable([ListItem(Paragraph(i, st), leftIndent=10) for i in items],
                              bulletType='bullet', start='\u2022', bulletFontName='Helvetica', leftIndent=12, bulletFontSize=8, spaceAfter=4))


m = N['map']; b = N['bonus']; s_ = N['suit']; ch = N['check']
mapname = m['name'].replace('.CivBeyondSwordWBSave', '')
imp = {i['type']: i for i in F['improvements']}
bld = {x['type']: x for x in F['builds']}

# ---------------- title ----------------
story.append(Spacer(1, 2.2 * cm))
P('Land, not tokens', title)
P('A design for land qualities, agriculture, mining, fisheries and industry in Rise of Mankind, '
  'replacing the point resources of the map', sub)
story.append(Spacer(1, 0.6 * cm))
P('<b>What this document proposes.</b> Resources stop being objects on single plots. Every plot, region and sea '
  'gets measurable qualities: temperature, water, growing season, soil, ore grade and depth, and fish. A city produces '
  'goods (wheat, coffee, iron, steel, arms) from the land it works, the knowledge it holds and the buildings it has, in '
  'quantities that are made, used up, stored and traded. The resource types of today survive only as the names of goods, '
  'which lets the engine\'s existing paths (building and unit requirements, happiness and health, the trade screen) keep working.', box)
P('<b>How it was made.</b> The facts about today\'s game come from the mod\'s XML records and DLL source at GitLab '
  '<font face="Courier">main</font> <font face="Courier">3bec049</font>, read by <font face="Courier">research/economy/tools/extract.py</font>. '
  'The maps and simulations use the WorldBuilder map <i>%s</i> (%d by %d plots, latitude %d to %d degrees) and are produced by '
  '<font face="Courier">tools/figures.py</font>; every number in the text is read from what that script computed. '
  'Parameters that are design choices rather than facts are marked as assumptions and collected in section 15.' %
  (mapname, m['width'], m['height'], m['lat_bottom'], m['lat_top']), small)
story.append(Spacer(1, 0.4 * cm))
P('<b>Contents</b>', h3)
toc = ['1. The game today', '2. The proposal in brief', '3. The land: climate, soil and regions', '4. Agriculture',
       '5. Seeds and the spread of crops', '6. Minerals: provinces, grades and depth', '7. The sea', '8. Goods and quantities',
       '9. Industry and war', '10. Trade and prices', '11. How the mechanics interlock', '12. Fitting it into the engine',
       '13. Three ways to build it', '14. Roadmap and how each step is judged', '15. Assumptions and open questions',
       'Appendix: parameters and notation']
for t in toc: P(t, small)
story.append(PageBreak())

# ---------------- 1 ----------------
P('1. The game today', h1)
P('This section describes what the game does now, from its records and code, before any proposal.', body)
P('1.1 Resources are tokens on plots', h2)
bullets([
    'The mod defines <b>%d resource types</b> (<font face="Courier">CIV4BonusInfos.xml</font>). %d of them can stand on a map plot; '
    'the others are produced by buildings or come later in the game.' % (b['total'], b['natural']),
    'A plot holds <b>at most one</b> resource: <font face="Courier">CvPlot</font> stores it in a single field, '
    '<font face="Courier">m_eBonusType</font>.',
    'The Earth map places <b>%d</b> resource plots on %d land plots and %d water plots.' % (b['placed'], m['land'], m['plots'] - m['land']),
    'A resource counts for a trade network once it is connected. A second copy adds nothing to the network that holds it; it '
    'can only be traded away. Happiness and health from a luxury are +1 or +2 for every city, whatever the city\'s size.',
])
P('1.2 Latitude barely shapes where things are', h2)
P('Each resource has a latitude window (<font face="Courier">iMinLatitude</font>, <font face="Courier">iMaxLatitude</font>) used when a map '
  'script places resources at random. Of the %d natural resources, <b>%d have the window 0 to 80 degrees</b>, which covers almost all land. '
  'Hand-made WorldBuilder maps ignore the windows altogether. The game\'s latitude function, <font face="Courier">CvPlot::getLatitude</font>, '
  'returns the absolute value; only <font face="Courier">getLatitudeMinutes</font> keeps the hemisphere\'s sign, and nothing in the '
  'economy uses it.' % (b['natural'], b['window_0_80']))
figure('f01_latitude_windows', 'For each natural resource, its latitude window from the XML (blue bars, shown in both hemispheres) and '
       'the latitude of every plot the Earth map gives it (orange dots). Sorted by the median distance of the dots from the equator; resources the map does not place are at the top. '
       'Most windows span the whole habitable range; where a resource sits is decided by the map maker or the terrain and feature it needs.')
P('1.3 Factories are gates, not flows', h2)
P('%d buildings produce a resource (<font face="Courier">FreeBonus</font>); %d of them need other resources first. The requirement is only '
  'that the inputs be present in the city\'s network: <b>nothing is used up</b>. A Steel Mill needs Coal and Iron and gives the network '
  'one Steel; a Weapon Factory needs Sulphur and one of Steel, Iron or Copper and gives Ammo. Where the XML says <font face="Courier">-1</font>, '
  'the number of copies comes from the world size (<font face="Courier">CvGame::getNumFreeBonuses</font>), %d on a Huge map.' %
  (N['chains']['producing_buildings'], N['chains']['with_inputs'], N['chains']['free_bonuses_huge']))
rows = [['Building', 'Gives', 'Copies', 'Needs', 'And one of']]
for r in N['recipes']:
    rows.append([r['building'], r['output'], r['copies'], ', '.join(r['needs']) or '-', ', '.join(r['one_of']) or '-'])
table(rows, [3.4 * cm, 3.0 * cm, 1.5 * cm, 3.2 * cm, 5.9 * cm])
P('1.4 Mines already have depths; fields and seas do not', h2)
mi, sh, mo = imp['IMPROVEMENT_MINE'], imp['IMPROVEMENT_SHAFT_MINE'], imp['IMPROVEMENT_MODERN_MINE']
P('RoM has three mine improvements, each built by workers once a technology is known: Mine (%s), Shaft Mine (%s) and Modern Mine (%s). '
  'Their yields are food, production and commerce %s, %s and %s; a Mine also turns into a Shaft Mine by itself after %d turns of work '
  '(<font face="Courier">iUpgradeTime</font>). The same upgrade mechanism grows the Latifundium through five stages and the Cottage into a Town. '
  'Farms and fishing boats have one level each, and the sea\'s food sits on %d resource plots of the Earth map.' %
  (bld['BUILD_MINE']['tech'][5:].title(), bld['BUILD_SHAFT_MINE']['tech'][5:].title(), bld['BUILD_MODERN_MINE']['tech'][5:].title(),
   mi['yields'], sh['yields'], mo['yields'], mi['upgrade_time'], N['sea']['sea_resources']))

# ---------------- 2 ----------------
story.append(PageBreak())
P('2. The proposal in brief', h1)
P('2.1 Principles', h2)
bullets([
    '<b>The land is the resource.</b> Every land plot has a climate (temperature, water, growing season, hemisphere) and a soil; every plot '
    'lies in geological provinces with an ore grade and depth for each mineral; every sea plot has a carrying capacity for fish.',
    '<b>Production is land times work times knowledge.</b> A farm grows the crop its owner chooses among those the civilization knows and '
    'the land suits; a mine extracts what its province holds, down to the depth its technology reaches; a fishing fleet takes what the sea renews.',
    '<b>Goods are quantities.</b> They are made, moved within a trade network, used up by buildings, units and citizens, stored and traded.',
    '<b>No tokens on the map.</b> No plot holds a resource. What the player sees is the land itself, through overlays, the plot help text '
    'and the improvements built on it.',
    '<b>Resource types become goods.</b> The entries of <font face="Courier">CIV4BonusInfos.xml</font> stay, as the list of goods. A city that '
    'makes or imports enough of a good holds it as a resource count, so every rule that reads resources today keeps working.',
])
figure('f20_engine_path', 'How goods made from land reach the rest of the game. The two blue and two orange steps are new DLL code; the '
       'city\'s resource count is fed through <font face="Courier">CvCity::changeFreeBonus</font>, which already updates the city\'s trade '
       'network (<font face="Courier">updatePlotGroupBonus</font>). Everything to the right reads those counts as it does now.')
P('2.2 Today and proposed', h2)
table([['', 'Today', 'Proposed'],
       ['Where goods come from', 'A resource token on one plot, improved by the matching improvement', 'Land qualities of the worked plot and its region'],
       ['Climate and hemisphere', 'Implied by terrain and features; latitude windows are loose and used only by random maps',
        'Modelled per plot: temperature, water, growing season, warmest month'],
       ['Crops', 'Fixed where the map put them', 'Planted wherever the land suits and the civilization knows the crop'],
       ['Minerals', 'One token; one to three improvement levels', 'Provinces with grade, layered reserves, depth by technology, exhaustion'],
       ['Sea', 'Fish, crab, clam and whale tokens', 'Carrying capacity of every sea plot; stocks that regrow and can collapse'],
       ['Quantity', 'Present or absent; extra copies only for trade', 'Made, used, stored, traded per turn'],
       ['Factories', 'Need inputs present; use nothing', 'Turn inputs into outputs at a rate, limited by the scarcest input'],
       ['Luxuries and health', '+1 or +2 per city whatever its size', 'Grow with consumption per head, with diminishing returns'],
       ['Weapons', 'Gate a unit if the resource is present', 'Units cost goods to build, and stores of arms run down in war']],
      [3.3 * cm, 6.4 * cm, 7.3 * cm])

# ---------------- 3 ----------------
story.append(PageBreak())
P('3. The land: climate, soil and regions', h1)
P('A plot\'s qualities are computed once when the game starts, from the map, and change only through play (soil wear, depletion, '
  'improvements). The model below uses only what every map already has: each plot\'s row (its latitude), terrain, plot type '
  '(flat, hills, peak), feature, river, and its distance to water.', body)
P('3.1 Temperature and seasons', h2)
P('For a plot in row <i>y</i> of a map <i>H</i> rows high, between latitudes &phi;<sub>bottom</sub> and &phi;<sub>top</sub>:')
eq(r'\varphi(y) = \varphi_{bottom} + (y + \frac{1}{2})\,\frac{\varphi_{top} - \varphi_{bottom}}{H}')
P('The annual mean temperature falls with the square of latitude and with altitude (hills 3 &deg;C, peaks 12 &deg;C cooler). The '
  'coefficients fit the zonal means of Earth: 27 &deg;C at the equator, about 13 &deg;C at 45&deg; and -25 &deg;C at the poles (assumption).')
eq(r'\bar T = 27 - 52\,\left(\frac{|\varphi|}{90}\right)^{2} - \Delta_{elev}')
P('Seasons have an amplitude that grows with latitude and with distance <i>d</i> from the sea (continentality), and they peak in July '
  'in the north and January in the south. This is where the hemisphere enters.')
eq(r'A = (1 + 0.28\,|\varphi|)\,\left(1 + 0.6\,(1 - e^{-d/5})\right), \qquad T_m = \bar T + A\,\cos\frac{2\pi (m - m_0)}{12}',
   note='with month <i>m</i> from 1 to 12 and <i>m</i><sub>0</sub> = 7 (July) where &phi; &ge; 0 and 1 (January) where &phi; &lt; 0.')
eq(r'L = \#\{\,m : T_m \geq 5\,^{\circ}\mathrm{C}\,\}, \qquad T_{min} = \min_m T_m')
P('<i>L</i> is the growing season in months and <i>T</i><sub>min</sub> the coldest month, which decides frost-sensitive crops such as coffee and sugar.')
P('3.2 Water', h2)
P('Rain from geography alone follows the global belts (wet equator, dry subtropics, wet mid-latitudes) and decays inland:')
eq(r'P_{geo} = \left(2200\,e^{-(\varphi/12)^2} + 1000\,e^{-((|\varphi| - 50)/14)^2} + 200\right)\left(0.3 + 0.7\,e^{-d/7}\right)\ \mathrm{mm}')
P('Hand-made maps do not place climates where geography alone predicts. Figure 4 shows it on the Earth map: from geography alone, the plots the '
  'map maker drew as desert get a median of <b>%d mm</b>, more than grassland\'s <b>%d mm</b>, because this map puts its great deserts close '
  'to the equator. The terrain the map maker drew is therefore treated as an observation of climate and blended in with weight 0.7 '
  '(desert 150 mm, plains 650, grassland 1100, marsh 1600, tundra 400, snow 250, jungle 2200; assumptions), and a river adds irrigation water:' %
  (ch['Rain, geography alone (mm)']['Desert'], ch['Rain, geography alone (mm)']['Grassland']))
eq(r'P = 0.3\,P_{geo} + 0.7\,P_{terrain}, \qquad W = P + 700\cdot[\mathrm{river}]')
P('After the blend the order is right: desert %d mm, plains %d, grassland %d. Temperature needs no blend: geography alone already ranks the '
  'drawn terrains as a map maker would (snow %d &deg;C, tundra %d, grassland %d, plains %d, desert %d).' %
  (ch['Rain, blended with terrain (mm)']['Desert'], ch['Rain, blended with terrain (mm)']['Plains'], ch['Rain, blended with terrain (mm)']['Grassland'],
   ch['Temperature (°C)']['Snow'], ch['Temperature (°C)']['Tundra'], ch['Temperature (°C)']['Grassland'], ch['Temperature (°C)']['Plains'],
   ch['Temperature (°C)']['Desert']))
figure('f03_climate', 'The climate model on the Earth map: annual mean temperature, water from rain (blended with the drawn terrain), '
       'growing season, and the warmest month, which flips at the equator.')
figure('f04_model_check', 'The model fields on the plots of each terrain the map maker drew (box: middle half; line: median; whiskers: '
       'range without outliers). Geography alone gets the deserts wrong on this map; blending the drawn terrain in puts them right. Plots: '
       + ', '.join('%s %d' % (k.lower(), v) for k, v in N['check_counts'].items() if v) + '.')
P('3.3 Soil', h2)
P('Soil fertility <i>S</i> in [0, 1] starts from the terrain (grassland 0.8, plains 0.65, marsh 0.5, tundra 0.3, desert 0.15; assumptions), '
  '+0.15 beside a river (flood plains), -0.1 on hills, 0 on peaks. It then changes with use: intensive farming wears it, fallow and manure '
  'restore it, and fertilisers (already a manufactured resource) add to it:')
eq(r'S_{t+1} = S_t - \delta\,u_t + \rho\,(S_0 - S_t) + \phi\,f_t, \qquad 0 \leq S \leq 1')
P('with <i>u</i> the intensity of use (1 for a farm worked every turn), &delta; the wear per turn, &rho; the recovery rate and <i>f</i> the fertiliser applied.')
P('3.4 Regions', h2)
P('The user\'s idea of qualities that belong to a region or a landmass can be built three ways. They differ in what a "region" is.')
table([['Option', 'What a region is', 'For', 'Against'],
       ['A. Landmass', 'The engine\'s <font face="Courier">CvArea</font>: one per continent or island, already computed',
        'No new map data; easy to explain ("Africa grows coffee")', 'Too coarse: a continent spans many climates'],
       ['B. Climate class per plot', 'A class from the model fields (figure 5); contiguous plots of one class form a region',
        'Follows latitude, hemisphere, altitude and coast; automatic on every map', 'Regions have no names or history'],
       ['C. Named regions', 'Clusters of plots of one class on one landmass, named at map start (e.g. "the Nile valley"), with region-wide '
        'attributes such as a famous crop or ore', 'Gives places identity; regions can carry events and trade reputations', 'Needs a clustering step and naming data'],
       ], [2.6 * cm, 5.4 * cm, 4.6 * cm, 4.4 * cm])
P('<b>Recommended:</b> qualities per plot (option B underneath), shown and reasoned about by named region (option C) in the interface and '
  'in AI plans. Shares of the Earth map\'s land by class: ' + ', '.join('%s %d %%' % (k.lower(), round(v * 100)) for k, v in N['regions'].items()) + '.')
figure('f08_regions', 'The five climate classes of the model on the Earth map, one map per class. Thresholds: tropical: mean 18 &deg;C or more and '
       'not arid; arid: less than 400 mm of water; temperate 8 to 18 &deg;C; continental and boreal -2 to 8 &deg;C; polar below -2 &deg;C.')

# ---------------- 4 ----------------
story.append(PageBreak())
P('4. Agriculture', h1)
P('4.1 How well a crop grows on a plot', h2)
P('Each crop <i>c</i> has a response to temperature and to water: zero outside a window, rising to full, a plateau, then falling. With the four '
  'corners <i>a</i> &lt; <i>b</i> &le; <i>c</i> &lt; <i>d</i> of the window:')
eq(r'g(x; a,b,c,d) = \max\left(0,\ \min\left(1,\ \frac{x - a}{b - a},\ \frac{d - x}{d - c}\right)\right)')
P('The growing season and frost act the same way: a crop needing <i>L</i><sub>c</sub> months gets <i>g</i><sub>L</sub> = clamp((<i>L</i> - <i>L</i><sub>c</sub> + 2)/2), '
  'and one that cannot stand a coldest month below <i>F</i><sub>c</sub> gets <i>g</i><sub>F</sub> = clamp((<i>T</i><sub>min</sub> - <i>F</i><sub>c</sub> + 3)/3). '
  'The suitability of the plot multiplies the climate terms and weights the soil with an exponent &beta; = 0.5 (assumption), so poor soil hurts but does not forbid:')
eq(r's_c = g_T(\bar T)\; g_W(W)\; g_L(L)\; g_F(T_{min})\; S^{\beta}')
figure('f05_responses', 'Temperature and water responses of four crops. The windows are approximate agronomic ranges (assumptions; '
       'appendix table A1) and would be XML fields of each crop, so modders tune them without code.')
P('<b>Product or law of the minimum.</b> Liebig\'s law of the minimum takes the worst factor instead of the product: <i>s</i> = min(<i>g</i><sub>T</sub>, '
  '<i>g</i><sub>W</sub>, &hellip;). The product penalises a plot that is merely adequate on several counts; the minimum forgives it. For coffee, '
  'the share of the temperature and water grid of figure 7 with <i>s</i> &ge; 0.5 is %d %% under the product and %d %% under the minimum. The product is '
  'recommended: it rewards the best land more, which gives regions their character.' %
  (round(N['coffee_area_half']['product'] * 100), round(N['coffee_area_half']['minimum'] * 100)))
figure('f07_product_vs_min', 'Coffee\'s suitability over temperature and water under the two rules; the orange line is <i>s</i> = 0.5.')
P('4.2 Where crops would grow on the Earth map', h2)
rows = [['Crop', 'Plots holding it today', 'Mean s on those plots', 'Mean s on all land', 'Land with s &ge; 0.5']]
for c, v in s_.items():
    rows.append([c, v['placed'], v['mean_at_placed'], v['mean_land'], '%d %%' % round(v['share_land_ge_half'] * 100)])
table(rows, [2.6 * cm, 3.4 * cm, 3.6 * cm, 3.6 * cm, 3.8 * cm])
P('The model was not fitted to the map\'s resource plots, so they are a check. Where the map maker put maize, cotton, coffee, olives and sugar, '
  'the model\'s suitability is three to five times the land average; for wheat, rice and potato it is about 1.5 times. The potatoes of this map '
  'sit in the Andes, which the map draws as flat plains and grassland, so the model sees no highland cool there: altitude on maps that draw '
  'mountains as flat land is a known limit (section 15).')
figure('f06_suitability_maps', 'Suitability of eight crops on the Earth map (blue, 0 to 1), with the plots where the map puts the crop today '
       '(orange dots). Under this design those dots disappear; the blue is what the land offers.')
P('4.3 What a farm produces', h2)
P('A farm on plot <i>p</i> growing crop <i>c</i> produces the crop as a good, plus food or commerce as the crop\'s record says:')
eq(r'q_{p,c} = Q_c\; s_{p,c}\; (1 + \tau_c)\; \lambda_p')
P('<i>Q</i><sub>c</sub> is the yield of perfect land, &tau;<sub>c</sub> the sum of technology and building bonuses (irrigation, crop rotation, '
  'fertilisers), and &lambda;<sub>p</sub> the improvement level (a Farm, or a Latifundium stage). The plot\'s food is part of the same output: '
  'grain crops give most of <i>q</i> as food, cash crops as commerce and as goods.')
P('<b>Integer yields.</b> The engine keeps plot yields as integers. The DLL would compute in hundredths and hand each worked plot an integer by '
  'error diffusion within the city, so the city\'s total is exact and no plot\'s yield flickers:')
eq(r'y_i = \left\lfloor \sum_{j \leq i} \frac{q_j}{100} \right\rfloor - \left\lfloor \sum_{j < i} \frac{q_j}{100} \right\rfloor')
P('with the plots taken in a fixed order (the city\'s plot index). Goods are kept in hundredths in the city\'s account (section 8) and need no rounding.')
P('<b>Choosing the crop.</b> Options, from simplest: (a) the worker builds "Farm (crop)", one build per crop, valid where <i>s</i> &ge; 0.25 and the '
  'crop is known; (b) one Farm build, and the city governor picks the crop each turn among the known ones by marginal value (section 8.4); '
  '(c) as (b), with a switching cost of a few turns of lost output so fields are not replanted every turn. Option (c) is recommended: it keeps '
  'workers\' actions as they are and gives the AI a single decision rule.')

# ---------------- 5 ----------------
P('5. Seeds and the spread of crops', h1)
P('A civilization can plant only the crops it knows. Knowledge starts where crops were domesticated and spreads by contact and trade, '
  'as wheat, maize and coffee spread on Earth.')
P('5.1 Model', h2)
P('Let <i>K</i><sub>i,c</sub> = 1 if civilization <i>i</i> knows crop <i>c</i>. At the start, the civilizations near the crop\'s origin know it. '
  'On a WorldBuilder map the origins can be read from where the map puts the crop today: here, a civilization knows the crop if its start lies '
  'within 5 plots of one of those plots. Each turn an unknowing civilization learns it with probability')
eq(r'h_{i,c} = 1 - \exp\left(-\lambda \sum_{j} K_{j,c}\, w_{ij}\right), \qquad w_{ij} = e^{-D_{ij}/D_0}\cdot[\,\mathrm{contact}_{ij}\,]')
P('<i>D</i><sub>ij</sub> is the distance between the two capitals, <i>D</i><sub>0</sub> the reach of contact, and contact is cut between continents '
  'separated by ocean until a technology allows crossing it (here at turn 200; assumption). In a full implementation <i>w</i><sub>ij</sub> would be '
  'the number of trade routes and open borders between the two, which the game already counts.')
dif = N['diffusion']
P('Figure 9 shows 2,000 simulated games on the Earth map\'s 18 starting positions (&lambda; = 0.025, <i>D</i><sub>0</sub> = 18 plots; assumptions). '
  'Wheat starts with %d civilizations of the Old World and soon reaches all of it; maize starts with %d (%s) and reaches half the civilizations '
  'around turn %d, soon after the oceans open; coffee starts with %d (%s).' %
  (dif['Wheat']['start'], dif['Maize']['start'], ', '.join(dif['Maize']['origins']), dif['Maize']['turn_half'] or 0,
   dif['Coffee']['start'], ', '.join(dif['Coffee']['origins'])))
figure('f09_diffusion', 'Share of the 18 civilizations that know each crop, over 400 turns (line: median of 2,000 simulated games; band: 10th '
       'to 90th percentile). The dashed line is the opening of ocean contact.')
P('5.2 Ways to give seeds', h2)
table([['Option', 'How a civilization gets a crop', 'Comment'],
       ['Contact', 'By the hazard above, from trading partners and neighbours', 'Organic; needs no new interface'],
       ['Trade item', 'Seeds offered on the trade screen like a technology', 'Needs a new trade item type in the DLL; the screen is the executable\'s, '
        'so it would appear as a technology-like entry (open question)'],
       ['Expedition', 'A unit (botanist, explorer) carries seeds home from a foreign region', 'Gameplay for scouts and colonial powers'],
       ['Technology', 'Botany or Biology unlocks crops the civilization has seen', 'Simple; fits the tech tree']],
      [2.6 * cm, 7.2 * cm, 7.2 * cm])

# ---------------- 6 ----------------
story.append(PageBreak())
P('6. Minerals: provinces, grades and depth', h1)
P('Ores are not uniform qualities of land: they come in deposits. In this design a deposit is a province, a field of ore grade that is highest at '
  'its centre and fades over a few plots, with reserves in layers that only deeper mines reach.')
P('6.1 Provinces', h2)
P('For a mineral <i>m</i> with province centres <i>k</i> at plots <b>x</b><sub>k</sub>, the grade at plot <b>x</b> is')
eq(r'G_m(\mathbf{x}) = \max_k\ \exp\left(-\frac{\|\mathbf{x} - \mathbf{x}_k\|^2}{2\sigma^2}\right)')
P('with &sigma; = 3 plots (assumption). The centres can come from three sources: (a) on existing WorldBuilder maps, from today\'s resource plots, which '
  'converts the mod\'s many scenario maps without redrawing them (figure 10 does this for the Earth map); (b) on random maps, from noise biased to '
  'hills and peaks; (c) hidden until prospected, so geology and exploration matter. Provinces of grade 0.5 or more on the Earth map: ' +
  ', '.join('%s %d plots from %d centres' % (k.lower(), v['plots_grade_ge_half'], v['seeds']) for k, v in N['provinces'].items()) + '.')
figure('f17_provinces', 'Ore grade of four minerals on the Earth map, with today\'s resource plots as province centres (black dots).')
P('6.2 Depth and exhaustion', h2)
mn = N['mines']
P('Each province holds reserves in three layers, <i>R</i><sub>1</sub>, <i>R</i><sub>2</sub>, <i>R</i><sub>3</sub>, scaled by the grade. The three '
  'mine improvements RoM already has become the three depths: a Mine works layer 1, a Shaft Mine layers 1 and 2, a Modern Mine all three. The '
  'extraction rate per turn follows each improvement\'s production yield in the XML, %d, %d and %d, times the plot\'s grade:' % tuple(mn['rate']))
eq(r'e_t = \min\left(r_{l}\, G,\ \sum_{i \leq l} R_{i,t}\right), \qquad R_{i,t+1} = R_{i,t} - e_{i,t}')
P('with <i>l</i> the mine\'s depth and the extraction taken from the top layer down. When the layers a mine reaches are empty, it is worked out: the '
  'player deepens it (if the technology is known) or abandons it. Figure 11 follows one deposit (layers %d, %d and %d units; assumptions) with the '
  'technologies at turns %d (Explosives) and %d (Seismology; illustrative). A mine left as it is yields %d units and is dry at turn %d; deepened '
  'when it runs dry it yields %d; deepened as soon as each technology arrives it yields %d.' %
  (mn['layers'][0], mn['layers'][1], mn['layers'][2], mn['tech'][1], mn['tech'][2], mn['runs']['stay']['total'], mn['runs']['stay']['dry_turn'],
   mn['runs']['when_dry']['total'], mn['runs']['deepen']['total']))
figure('f10_mines', 'One deposit worked three ways: left as a Mine (gray), deepened when worked out (orange), deepened as soon as possible (blue). '
       'Vertical lines: the technologies of the Shaft Mine and the Modern Mine.')
P('Depletion makes geography move over a game: early iron provinces run out, later ones are reached by depth. A further option is the Hotelling '
  'rule for the AI: extract more slowly when the good\'s price is expected to rise faster than the interest of holding gold, which in game terms '
  'means saving a nearly worked-out deposit for war.')

# ---------------- 7 ----------------
P('7. The sea', h1)
P('Instead of fish, crabs and whales on single plots, every sea plot has a carrying capacity <i>K</i> for fish: highest on the continental shelf '
  '(coast terrain), at river mouths, and in cold water, lowest in open ocean and under ice (weights are assumptions):')
eq(r'K = \left(0.25 + 0.55\,[\mathrm{shelf}] + 0.2\,[\mathrm{river\ mouth}]\right)\left(0.55 + 0.45\,\mathrm{clamp}\left(\frac{|\varphi| - 20}{40}\right)\right)')
sea = N['sea']
P('On the Earth map the shelf has %d plots of %d water plots, with mean capacity %.2f against %.2f in the open sea.' %
  (sea['shelf_plots'], sea['water_plots'], sea['mean_K_shelf'], sea['mean_K_open']))
figure('f18_sea', 'Carrying capacity of the sea on the Earth map, and today\'s %d sea resource plots (orange) for comparison.' % sea['sea_resources'])
P('The stock <i>N</i> of a fishing ground (the sea plots a city works, or a named sea region) grows logistically and is reduced by the catch <i>H</i>:')
fs = N['fish']
eq(r'N_{t+1} = N_t + r\,N_t\left(1 - \frac{N_t}{K}\right) - H_t, \qquad H_{MSY} = \frac{rK}{4}\ \ \mathrm{at}\ \ N = \frac{K}{2}')
P('The most that can be taken every turn for ever is the maximum sustainable yield <i>rK</i>/4. With <i>r</i> = %.1f and <i>K</i> = %d (assumptions) '
  'it is %.1f. A catch of 5 keeps the stock near %.0f and lands %d over 120 turns; a catch of %.1f lands %d; a catch of 9 collapses the stock and lands '
  'only %d. Fishing fleets, overfishing, treaties over fishing grounds and naval blockades of them all follow from these two lines.' %
  (fs['r'], fs['K'], fs['msy'], fs['runs']['5']['stock_after_120'], fs['runs']['5']['catch'], fs['msy'], fs['runs']['7.5']['catch'], fs['runs']['9']['catch']))
figure('f13_fisheries', 'Left: regrowth of the stock against three catch levels; the stock is stable where a catch line meets the curve. '
       'Right: the stock over 120 turns under each catch.')

# ---------------- 8 ----------------
story.append(PageBreak())
P('8. Goods and quantities', h1)
P('8.1 The city\'s account', h2)
P('Each city keeps, for every good <i>g</i>, what it made, received, used and stored this turn. Within a trade network, surpluses flow to deficits '
  '(the network is the engine\'s plot group, which already carries resources between connected cities):')
eq(r'X_{g,t+1} = \min\left(C_g,\ X_{g,t} + q_{g,t} + m_{g,t} - u_{g,t} - x_{g,t}\right)')
P('<i>X</i>: stock, <i>q</i>: production, <i>m</i>: imports, <i>u</i>: use by buildings, units and citizens, <i>x</i>: exports, <i>C</i>: storage capacity '
  '(granaries, warehouses, arsenals). Goods that cannot be stored (fresh fish, electricity) have <i>C</i> = 0.')
P('8.2 Recipes', h2)
P('A building <i>k</i> is a recipe: per run it takes inputs <b>a</b><sub>k</sub> and gives outputs <b>b</b><sub>k</sub>, up to a capacity of <i>c</i><sub>k</sub> '
  'runs per turn. With fixed proportions (Leontief) the runs possible are limited by the scarcest input:')
eq(r'n_k = \min\left(c_k,\ \min_{g}\ \frac{\alpha_{g,k}\,X_g}{a_{g,k}}\right), \qquad \alpha_{g,k} = \min\left(1, \frac{a_{g,k}\,c_k}{\sum_j a_{g,j}\,c_j}\right)')
P('&alpha;<sub>g,k</sub> is building <i>k</i>\'s share of good <i>g</i> when several buildings want it: proportional rationing by demand. Recipes are '
  'evaluated in the order of their dependency graph (ore before steel before arms), once per network per turn. A production function with '
  'substitution (constant elasticity, CES) is the alternative where inputs can replace each other, such as coal and charcoal in iron making:')
eq(r'n_k = c_k\left(\sum_g \theta_g \left(\frac{X_g}{a_{g,k} c_k}\right)^{\rho}\right)^{1/\rho},\qquad \rho < 1')
net = N['network']
P('Figure 14 shows one network for one turn: %s per turn of iron ore, coal, sulphur and copper, a steel mill (2 ore and 1 coal give 2 steel), an '
  'arms factory (1 steel and 1 sulphur give 1 arms) and a cartridge works (1 copper and 1 sulphur give 2 ammunition). The steel mill runs at full '
  'capacity (%g runs); sulphur is shared by the two users, so the arms factory runs %g times and the cartridge works %g times, and %g steel is left over.' %
  ('/'.join('%g' % v for v in net['raw'].values()), net['runs']['Steel mill'], net['runs']['Arms factory'], net['runs']['Cartridge works'], net['left'].get('Steel', 0)))
P('8.3 What a good is worth', h2)
P('The value of one more unit of a good is the change in what the network produces with it, valued at the AI\'s weights for food, production, '
  'commerce and goods:')
eq(r'v_g = \frac{\partial V}{\partial q_g} \approx V(\mathbf{q} + \mathbf{e}_g) - V(\mathbf{q})')
P('In the example one more sulphur is worth <b>%+.2f</b>, ten times one more iron ore (<b>%+.2f</b>), because sulphur binds both factories and iron '
  'binds nothing. No fixed weight per good can say this; the AI must compute it. This is the same principle the diplomacy change of merge request '
  '!63 applies to today\'s resources: value a good by what it changes in the valuer\'s own cities.' % (net['marginal']['Sulphur'], net['marginal']['Iron ore']))
figure('f11_network', 'Left: goods flows in one network for one turn (arrow width: quantity). Right: the value of one more unit per turn of each raw good, by recomputing the network.')
P('8.4 Luxuries and health per head', h2)
P('Today a luxury gives a fixed bonus to every city. With quantities, a city\'s happiness from a good grows with consumption per head, with '
  'diminishing returns, so a large city needs more of it:')
eq(r'\eta_g = H_g\left(1 - e^{-c_g/k_g}\right), \qquad c_g = \frac{10\,u_g}{\mathrm{population}}')
P('<i>H</i><sub>g</sub> is the most the good can give (2 here), <i>k</i><sub>g</sub> the consumption per ten citizens that gives 63 % of it. The same '
  'form serves health from food variety. Figure 15 compares it with today\'s +1.')
figure('f19_luxury', 'Left: happiness from one luxury as consumption per ten citizens grows, today and under two values of <i>k</i>. '
       'Right: one unit per turn shared by a city as it grows.')
P('8.5 Into the engine', h2)
P('Building and unit requirements, the trade screen and happiness rules read the city\'s resource counts. The bridge sets each count from the account: '
  'a city that has, per turn, at least one unit of good <i>g</i> available (made, received or drawn from store) holds <i>g</i> once for every unit:')
eq(r'\mathrm{FreeBonus}_g = \left\lfloor \frac{X_g + q_g + m_g}{U_g} \right\rfloor')
P('where <i>U</i><sub>g</sub> is the good\'s unit size. The counts are updated through <font face="Courier">changeFreeBonus</font> once per turn, '
  'after the network\'s recipes have run. With happiness per head (8.4) the engine\'s own luxury rule is switched off for goods and the new rule applied.')

# ---------------- 9 ----------------
P('9. Industry and war', h1)
P('Arms become goods that are made, stored and used. The ladder of options, from today:')
table([['Level', 'Rule', 'What changes in play'],
       ['0 (today)', 'A unit needs a resource present', 'Having one copy is enough for an empire'],
       ['1', 'Building a unit costs goods: a Rifleman 2 arms, a Cannon 3 steel and 2 arms (illustrative)', 'Armies need industry; output caps how fast an army grows'],
       ['2', 'Units in the field use supplies each turn (ammunition, fuel)', 'Long wars drain industry; peace lets stores refill'],
       ['3', 'Battles use ammunition; a unit without it fights at reduced strength', 'Blockades and raids on factories decide wars']],
      [2.0 * cm, 7.4 * cm, 7.6 * cm])
P('The arsenal\'s stock follows the account of section 8.1 with the demand of war added. When the stock is empty, demand is met only from current production:')
eq(r'\mathrm{met}_t = \frac{\min(D_t,\ X_t + q_t)}{D_t}')
stk = N['stock']
P('Figure 16 runs a 90-turn war (turns 100 to 190) on an arsenal of capacity %d: the store is empty at turn %d, new factories raise production at '
  'turn 125, a blockade cuts it at turns 150 to 175, and the share of demand met falls to %d %%.' % (stk['cap'], stk['empty_turn'], stk['min_ready']))
figure('f12_stockpile', 'An arsenal through a war (shaded): stock, production and use, and the share of the army\'s demand met.')

# ---------------- 10 ----------------
story.append(PageBreak())
P('10. Trade and prices', h1)
P('Goods move between civilizations through the trade screen (as resources do today) and along trade routes. With quantities, a price per good '
  'lets the AI judge deals and lets a scarce good earn its holder something:')
eq(r'p_g = p^{0}_{g}\ \mathrm{clamp}\left(\left(\frac{D_g}{S_g}\right)^{1/\varepsilon},\ 0.2,\ 5\right)')
P('<i>D</i> and <i>S</i> are the world\'s (or the trading partners\') demand and supply of the good, &epsilon; its elasticity, <i>p</i><sup>0</sup> its '
  'base price. A monopolist that sells <i>s</i> units against demand <i>D</i> earns <i>p</i>(<i>s</i>) <i>s</i>; with &epsilon; = 1 that is constant in <i>s</i> wherever the price '
  'cap does not bind, so selling more earns nothing more, and with &epsilon; &lt; 1 selling less earns more: the incentive to hoard a monopoly good, which coffee or '
  'spices had historically.')
figure('f14_prices', 'Left: price against the ratio of demand to supply for three elasticities. Right: a monopolist\'s income as it sells more copies.')
P('For the AI, a deal\'s worth is the sum of marginal values (section 8.3) of what it gets minus what it gives, and gold is worth what it buys at '
  'current prices. Where the game is not a market (most of history), prices can be used only inside the AI\'s valuation and never shown.')

# ---------------- 11 ----------------
P('11. How the mechanics interlock', h1)
P('The mechanics form loops. Good land feeds people; people work mines; ore becomes steel and arms; arms win land. Farming wears the soil, which '
  'lowers the land\'s quality until fertilisers or rest restore it; seeds and trade raise what the land can grow.')
figure('f16_loop_diagram', 'Feedback between the mechanics. Each arrow says how a change in one quantity moves the next.')
lp = N['loop']
P('Figure 19 runs a deliberately small version of the loop for 300 turns: a realm with the 60 best wheat plots of the Earth map (mean suitability %.2f), '
  'six iron deposits with the layers of section 6, soil that wears until fertilisers arrive at turn 200, shaft mines at 160 and modern mines at 240, '
  'and a war at turns 180 to 220. Population stalls as the soil wears and grows again with fertilisers; the war empties the arsenal (lowest store %.0f) '
  'because the mines are still shallow; modern mines then raise ore and steel several times over. The point is not the numbers, which come from '
  'illustrative parameters, but that the outcome depends on the order in which land, technology and war arrive.' % (lp['land_q'], lp['arms_min_war']))
figure('f15_loop_run', 'One realm over 300 turns with the loop of figure 18 (war shaded; vertical lines: shaft mines, fertilisers, modern mines).')

# ---------------- 12 ----------------
story.append(PageBreak())
P('12. Fitting it into the engine', h1)
P('Civilization IV splits into the executable (rendering, interface screens, map display), the DLL (all rules; source available), XML (data) and '
  'Python (screens, map scripts, events). The proposal changes the DLL, XML and Python; it works around the executable.')
table([['Piece', 'Layer', 'What changes', 'Risk'],
       ['Plot qualities', 'DLL', 'New fields on CvPlot: temperature, water, season, soil, province grades, reserves, crop, fish stock '
        '(about 20 bytes per plot); computed at game start; saved with a version flag', 'Low'],
       ['Crop and goods records', 'XML + DLL', 'Crop windows and yields on CIV4BonusInfos entries (new tags); recipes on buildings '
        '(input and output quantities); unit goods costs', 'Low'],
       ['Plot yields', 'DLL', 'CvPlot::calculateNatureYield and calculateImprovementYieldChange read qualities instead of the bonus', 'Medium'],
       ['City accounts and recipes', 'DLL', 'New per-city arrays; a per-network pass each turn in CvPlayer::doTurn', 'Medium'],
       ['Bridge to resources', 'DLL', 'changeFreeBonus from the accounts (section 8.5)', 'Low'],
       ['No tokens on the map', 'DLL + Python', 'Map scripts place no resources (CvMapGenerator::addBonuses skipped); WorldBuilder maps converted at load '
        '(provinces and crop origins from their resource plots, then the plots cleared)', 'Medium'],
       ['Showing the land', 'Python', 'Overlays of suitability, grade and fish through colored plots (the engine API the strategy overlay uses); '
        'plot help text; a land screen', 'Low'],
       ['Resource models on the map', 'Executable', 'Not drawn any more, as no plot holds a resource; improvements (farms, mines, boats) still drawn', 'None'],
       ['Trade screen', 'Executable', 'Unchanged: goods appear as resources do now', 'Low'],
       ['AI', 'DLL', 'Marginal values of goods; crop choice; mine deepening; worker plans; trade and war plans with stocks', 'High'],
       ['Saves', 'DLL', 'Old saves load with qualities computed at load; new saves are not readable by old DLLs', 'Medium']],
      [3.0 * cm, 2.0 * cm, 9.8 * cm, 2.2 * cm])
P('<b>Cost per turn.</b> Suitability is static: %d plots times 8 crops is %d evaluations once at game start. Per turn the new work is one pass over '
  'each network\'s recipes (tens of buildings) and one over its cities\' accounts (cities times goods), well below what the AI already spends on '
  'city governors each turn.' % (m['plots'], m['plots'] * 8))
P('<b>Determinism.</b> Everything above is deterministic except seed spreading, which must use the game\'s synchronised random number generator '
  '(as all game rules do) so multiplayer and the headless test harness stay in sync.')

# ---------------- 13 ----------------
P('13. Three ways to build it', h1)
table([['', 'A. Bridge', 'B. Quantities', 'C. Full economy'],
       ['Land qualities', 'Climate, soil, provinces, fish capacity', 'Same', 'Same, plus soil wear, depletion, fish stocks'],
       ['Crops', 'Farms grow known crops where suitable', 'Same, with yields by suitability', 'Same, with seed spreading and switching costs'],
       ['Goods', 'Present or absent per city (resource counts)', 'Counted per turn; recipes use inputs', 'Stored, traded with prices'],
       ['Luxuries', 'As today', 'Per head (8.4)', 'Per head'],
       ['Military', 'Gates as today', 'Unit build costs in goods', 'Supplies and ammunition in war'],
       ['AI work', 'Crop choice; valuation of land', 'Marginal values; production planning', 'Stocks, prices, war logistics'],
       ['Size', 'Smallest; playable alone', 'Medium', 'Largest'],
       ['Risk to the game', 'Low', 'Medium: AI must plan production', 'High: AI must plan stocks and trade']],
      [2.8 * cm, 4.6 * cm, 4.6 * cm, 5.0 * cm])
P('Each path contains the previous one. <b>A</b> already removes the tokens and gives land its qualities; <b>B</b> makes quantities matter; <b>C</b> '
  'adds time (stores, depletion, regrowth) and markets.')

# ---------------- 14 ----------------
P('14. Roadmap and how each step is judged', h1)
P('Under the repository\'s rules each step is a registered prediction, built, then judged: a safety claim (no crash, not slower) by 5 seeded harness '
  'runs per arm, a claim that play gets better by at least 30, and what only a human game can show by the user\'s games.')
table([['Step', 'Content', 'Judged by'],
       ['1', 'Plot qualities computed and shown (overlays, help text); nothing else changes', 'Safety runs; the overlays in the game'],
       ['2', 'Tokens removed; farms grow crops by suitability; mines and boats by provinces and sea; bridge to resource counts (path A)',
        'Safety runs; play runs on cities founded and food per city against the current game'],
       ['3', 'AI for crop choice and land valuation', 'Play runs: food and production per city of AI civilizations'],
       ['4', 'Counted goods and recipes; luxuries per head (path B)', 'Safety runs; play runs; the user\'s games for balance'],
       ['5', 'Unit costs in goods; mine depth and exhaustion', 'Play runs on war outcomes against fixed opponents'],
       ['6', 'Stocks, seeds spreading, fish stocks, prices (path C)', 'Play runs; the user\'s games']],
      [1.2 * cm, 10.0 * cm, 5.8 * cm])

# ---------------- 15 ----------------
P('15. Assumptions and open questions', h1)
P('<b>Assumptions</b> (design parameters to tune, not facts):', h3)
bullets(['Temperature profile 27 - 52 (|&phi;|/90)<super>2</super> &deg;C, lapse 3 &deg;C for hills and 12 &deg;C for peaks, seasonal amplitude formula.',
         'Rain belts and inland decay; terrain rain values; blend weight 0.7 for the drawn terrain; river irrigation 700 mm.',
         'Soil values per terrain; soil exponent &beta; = 0.5; the crop windows of table A1.',
         'Seed spreading: &lambda; = 0.025, reach 18 plots, ocean contact at turn 200, origins within 5 plots of today\'s resource plots.',
         'Province width &sigma; = 3 plots; reserve layers 120, 400 and 1,600 units; technology turns 220 and 340.',
         'Fish regrowth <i>r</i> = 0.3, capacity weights; price clamp 0.2 to 5; recipe quantities and unit costs in sections 8 and 9.'], small)
P('<b>Open questions</b>', h3)
bullets(['Maps that draw mountains as flat land give the model no altitude (the Andes potatoes of section 4.2). A map field for altitude, or peaks and hills in the maps, would fix it.',
         'Whether the trade screen can show seeds as an item: the screen is the executable\'s; resources and technologies are the item types it knows.',
         'How the player reads the land without tokens: overlays and help text are proposed; whether that is enough is for play to show.',
         'Balance across eras: how much land quality should matter against buildings and technology.',
         'How far the AI can be taught production planning (path B) before path C is worth starting.'], small)

# ---------------- appendix ----------------
story.append(PageBreak())
P('Appendix: parameters and notation', h1)
P('<b>Table A1.</b> Crop windows used in the figures (assumptions; would be XML fields).', small)
CROPS = [('Wheat', '3, 8, 16, 23', '250, 450, 900, 1500', 4, '-'), ('Rice', '16, 21, 29, 34', '900, 1500, 3000, 4500', 6, 5),
         ('Maize', '10, 15, 26, 31', '450, 650, 1300, 2000', 5, '-'), ('Potato', '2, 7, 15, 21', '400, 600, 1200, 1900', 3, '-'),
         ('Cotton', '15, 20, 28, 32', '450, 700, 1300, 2000', 7, 0), ('Coffee', '15, 18, 24, 27', '1100, 1500, 2600, 3400', 12, 10),
         ('Olives', '11, 14, 20, 24', '250, 400, 800, 1200', 8, 0), ('Sugar', '19, 23, 30, 34', '1000, 1400, 2600, 3800', 11, 8)]
table([['Crop', 'Temperature window a, b, c, d (&deg;C)', 'Water window (mm)', 'Season (months)', 'Coldest month at least (&deg;C)']] +
      [list(c) for c in CROPS], [2.2 * cm, 4.6 * cm, 4.2 * cm, 2.6 * cm, 3.4 * cm])
P('<b>Notation</b>', h3)
table([['Symbol', 'Meaning'], ['&phi;', 'latitude, degrees (negative south)'], ['<i>T</i>, <i>T</i><sub>m</sub>, <i>T</i><sub>min</sub>', 'annual mean, monthly and coldest-month temperature'],
       ['<i>A</i>', 'seasonal amplitude'], ['<i>L</i>', 'growing season, months'], ['<i>d</i>', 'distance to water, plots'],
       ['<i>P</i>, <i>W</i>', 'rain; water available to crops'], ['<i>S</i>', 'soil fertility, 0 to 1'], ['<i>s</i><sub>c</sub>', 'suitability of a plot for crop <i>c</i>'],
       ['<i>G</i><sub>m</sub>', 'ore grade of mineral <i>m</i>'], ['<i>R</i><sub>i</sub>', 'reserves of layer <i>i</i>'], ['<i>K</i>, <i>N</i>, <i>r</i>', 'fish capacity, stock, regrowth rate'],
       ['<i>X</i>, <i>q</i>, <i>u</i>, <i>m</i>, <i>x</i>, <i>C</i>', 'stock, production, use, imports, exports, storage capacity of a good'],
       ['<i>n</i><sub>k</sub>, <i>c</i><sub>k</sub>', 'runs and capacity of recipe <i>k</i>'], ['<i>v</i><sub>g</sub>', 'marginal value of good <i>g</i>'],
       ['<i>p</i><sub>g</sub>, &epsilon;', 'price and elasticity of good <i>g</i>']], [4.0 * cm, 13.0 * cm])
P('<b>Sources.</b> GitLab aretemaxxing-group/rise-of-mankind <font face="Courier">main</font> <font face="Courier">3bec049</font>: '
  'Assets/XML/Terrain (CIV4TerrainInfos, CIV4FeatureInfos, CIV4BonusInfos, CIV4ImprovementInfos), Assets/XML/Buildings/CIV4BuildingInfos.xml, '
  'Assets/XML/Units (CIV4UnitInfos, CIV4BuildInfos), Assets/XML/GameInfo/CIV4WorldInfo.xml, PrivateMaps/%s, and the DLL source '
  '(CvPlot.cpp, CvCity.cpp, CvGame.cpp). Scripts and data: GertaBool/RoM research/economy.' % m['name'], small)


def on_page(c, doc):
    c.saveState()
    c.setFont('Helvetica', 7.5); c.setFillColor(INK2)
    if doc.page > 1:
        c.drawString(2.0 * cm, 1.2 * cm, 'Land, not tokens: land qualities and industry for Rise of Mankind')
        c.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, str(doc.page))
    c.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.8 * cm, bottomMargin=1.9 * cm,
                        title='Land, not tokens', author='Rise of Mankind research', subject='Land qualities, agriculture, mining and industry')
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUT, EQN[0], 'equations', FIGN[0], 'figures')
