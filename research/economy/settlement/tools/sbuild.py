#!/usr/bin/env python3
"""Builds settlement-economy.pdf from figures/ and data/. Every quoted number is read from data/.
usage: sbuild.py <settlement dir>"""
import io, json, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image as PI
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, ListFlowable, ListItem

ROOT = sys.argv[1]
D = lambda n: json.load(open(os.path.join(ROOT, 'data', n)))
N, MOD, SER, FA = D('snumbers.json'), D('model.json'), D('series.json'), D('facts_medstd.json')
FIG = os.path.join(ROOT, 'figures'); OUT = os.path.join(ROOT, 'settlement-economy.pdf')
TEXTW = A4[0] - 4.0 * cm
INK, INK2, BLUE = colors.HexColor('#0b0b0b'), colors.HexColor('#52514e'), colors.HexColor('#2a78d6')
ss = getSampleStyleSheet()
body = ParagraphStyle('body', parent=ss['BodyText'], fontName='Helvetica', fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=5)
small = ParagraphStyle('small', parent=body, fontSize=8.2, leading=11)
cap = ParagraphStyle('cap', parent=body, fontSize=7.9, leading=10.4, textColor=INK2, spaceBefore=2, spaceAfter=10)
h1 = ParagraphStyle('h1', parent=ss['Heading1'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=INK, spaceBefore=10, spaceAfter=7, keepWithNext=1)
h2 = ParagraphStyle('h2', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=11.2, leading=14.5, textColor=INK, spaceBefore=9, spaceAfter=4, keepWithNext=1)
h3 = ParagraphStyle('h3', parent=body, fontName='Helvetica-Bold', fontSize=9.6, spaceBefore=5, spaceAfter=2, keepWithNext=1)
title = ParagraphStyle('title', parent=h1, fontSize=23, leading=28, spaceAfter=10)
sub = ParagraphStyle('sub', parent=body, fontSize=11.5, leading=15.5, textColor=INK2)
cell = ParagraphStyle('cell', parent=body, fontSize=7.9, leading=10, spaceAfter=0)
cellb = ParagraphStyle('cellb', parent=cell, fontName='Helvetica-Bold')
box = ParagraphStyle('box', parent=body, fontSize=9.1, leading=12.8, backColor=colors.HexColor('#eef4fc'), borderColor=BLUE,
                     borderWidth=0.6, borderPadding=7, spaceBefore=6, spaceAfter=12)
story = []
P = lambda t, st=body: story.append(Paragraph(t, st))
EQN, FIGN = [0], [0]
FIGORDER = []


def eq(tex, size=11.0, note=None):
    EQN[0] += 1
    fig = plt.figure(figsize=(0.01, 0.01)); fig.text(0, 0, '$' + tex + '$', fontsize=size, color='#0b0b0b')
    buf = io.BytesIO(); fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0.03, transparent=True); plt.close(fig)
    buf.seek(0); w, h = PI.open(buf).size; buf.seek(0)
    img = Image(buf, width=w * 72 / 300, height=h * 72 / 300)
    t = Table([[img, Paragraph('(%d)' % EQN[0], ParagraphStyle('n', parent=body, alignment=2, textColor=INK2))]], colWidths=[TEXTW - 1.2 * cm, 1.2 * cm])
    t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (0, 0), (0, 0), 14), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    story.append(t)
    if note: P(note, small)
    return EQN[0]


def figno(name):
    if name not in FIGORDER: FIGORDER.append(name)
    return FIGORDER.index(name) + 1


def figure(name, caption, width=TEXTW):
    n = figno(name)
    path = os.path.join(FIG, name + '.png'); w, h = PI.open(path).size
    story.append(KeepTogether([Image(path, width=width, height=width * h / w), Paragraph('<b>Figure %d.</b> %s' % (n, caption), cap)]))


def table(rows, widths, header=True):
    data = [[Paragraph(str(c), cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#d9d8d3')), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]
    if header: st.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f0ec')))
    t.setStyle(TableStyle(st)); story.append(t); story.append(Spacer(1, 8))


def bullets(items, st=body):
    story.append(ListFlowable([ListItem(Paragraph(i, st), leftIndent=10) for i in items], bulletType='bullet', start='•',
                              bulletFontName='Helvetica', leftIndent=12, bulletFontSize=8, spaceAfter=4))


# figure numbers in reading order (referenced before they appear)
for nm in ['s01_games', 's02_sizes', 's03_calibration', 's04_deals', 's11_multipliers', 's05_staple', 's06_bysize', 's07_needs_time', 's08_capacity', 's09_trade', 's10_cost']:
    figno(nm)
F_ = lambda n: 'figure %d' % figno(n)

S, G, CAL, DE = N['short'], N['games'], N['calibration'], N['deals']
pct = lambda x: '%.1f %%' % x
rec = G['recon']
bench = {(int(r['cities']), int(r['goods'])): r for r in N['bench']}
b300 = bench[(300, 100)]; b120 = bench[(120, 12)]
fl = N['float']
res_deals = DE['resource_deals']; swaps = dict(DE['composition']).get('resource for resource', 0)
gpt_deals = dict(DE['composition']).get('gold per turn for resource', 0)
gifts = dict(DE['composition']).get(' for resource', 0)
ob = dict(DE['composition']).get('open borders for open borders', 0)

# ---------------- title ----------------
story.append(Spacer(1, 2.0 * cm))
P('Settlement Economy', title)
P('A quantitative design study: how goods made, used and traded by settlements would behave in Rise of Mankind, measured on '
  '%d real games, and what each implementation choice in the codebase changes' % G['n'], sub)
story.append(Spacer(1, 0.5 * cm))
P('<b>Findings.</b><br/>'
  '1. The settlements of %d harness games were rebuilt from their telemetry; the rebuilt city counts match the games\' own on '
  '%d of %d player-turns.<br/>'
  '2. With the game\'s own yields and governor, the plots those cities work feed their observed populations on all but %s of city-turns.<br/>'
  '3. Treating staple food as a good that cities keep to themselves raises the share of citizens short of food from %s (today\'s rule) to %s; '
  'sharing it within a trade network lowers it to %s; stores lower it to %s, and spoilage brings it back to %s.<br/>'
  '4. Whole-unit arithmetic throws away %s of all production to truncation; hundredths lose nothing.<br/>'
  '5. Single-precision floating point gave a different allocation for the same goods, depending only on the order in which cities '
  'were summed, in %d of %d rationings: unusable in multiplayer.<br/>'
  '6. Needs not matched to what the land can give stay unmet whatever the distribution: fuel and tools are short for most citizens in every '
  'variant. A governor that knows the city\'s needs lowers the fuel shortage from %s to %s.<br/>'
  '7. Between AIs today, %d of %d deals involve resources, %d of them swaps of one resource for another and %d for gold per turn. '
  'With goods, players lack every turn what others have spare: on average %s units of variety food per game alone.<br/>'
  '8. The goods pass costs %.2f ms per turn at %d cities and %d goods; the AI\'s marginal values for every good %.0f ms.<br/>'
  '9. Buildings, civics and specialists add as much as the land: production is %.2f times what the worked plots give at turn 150, commerce %.1f times; '
  'and on this map every trade route pays the 1.00 floor before modifiers.' %
  (G['n'], rec['agree'], rec['total'], pct(CAL['3']['share'] * 100), pct(S['today_food']['staple']), pct(S['goods_local']['staple']),
   pct(S['goods_network']['staple']), pct(S['network_store']['staple']), pct(S['network_store_spoil']['staple']),
   pct(N['round_loss']['whole_units']), fl.get('alloc_differs', 0), fl.get('rations', 0), pct(S['network_store_spoil']['fuel']),
   pct(S['aware_network_store_spoil']['fuel']), res_deals, DE['deals'], swaps, gpt_deals, '{:,.0f}'.format(N['trade'].get('variety', 0)),
   float(b300['us_per_turn']) / 1000, 300, 100, float(b300['us_per_turn_with_ai_marginals']) / 1000, N['mult']['prod']['150'], N['mult']['com']['150']), box)
P('<b>How it was made.</b> Telemetry of the 30 harness games of build 504830a0dee0 (GitLab <font face="Courier">main</font> '
  '<font face="Courier">3bec049</font>) that served as the baseline of predictions P18 and P19; the map they were played on; the mod\'s XML '
  'records and DLL source at the same commit. Scripts in <font face="Courier">research/economy/settlement/tools</font>: '
  '<font face="Courier">games.py</font> (settlements and deals), <font face="Courier">model.py</font> (the reference model), '
  '<font face="Courier">calibrate.py</font>, <font face="Courier">analysis.py</font>, <font face="Courier">bench.c</font> and '
  '<font face="Courier">sfigures.py</font>. Every number in the text is read from what they wrote. Parameters that are design choices are '
  'marked as assumptions and collected in the appendix. Companion to <i>Land, not tokens</i> (research/economy).', small)
story.append(PageBreak())

# ---------------- 1 ----------------
P('1. Questions and sources', h1)
P('Each question is answered from a named source; the model was built only for what no source answers (section 6).')
table([['Question', 'Source'],
       ['How many settlements does a game have, how large, and how fast do they grow?', '30 harness games: per-player cities and population each turn; founding, capture and raze events with their plots'],
       ['Can the rebuilt settlements be trusted?', 'Rebuilt city counts against the telemetry\'s; the food balance of the rebuilt cities against the populations the games fed'],
       ['How does trade in resources work today, and how do the AIs use it?', 'CvDeal.cpp (TRADE_RESOURCES), CvStructs.h (TradeData), CvEnums.h (TradeableItems); the deals in the 30 games'],
       ['How do buildings, civics and trade routes change food, growth, production and commerce, and by how much?', 'CvCity::getYieldRate, getBaseYieldRateModifier, getBaseTradeProfit; CIV4BuildingInfos.xml, CIV4CivicInfos.xml (bc.py); observed production and commerce rates against the rebuilt plots (yields.py)'],
       ['What do food and growth do today?', 'CvCity::foodConsumption, foodDifference, doGrowth; CvPlayer::getGrowthThreshold; GlobalDefines.xml'],
       ['What would each implementation choice change for these settlements?', 'The reference model (section 6) run on the rebuilt settlements'],
       ['What does it cost per turn and in the save?', 'bench.c, the model\'s per-turn pass in C, timed; byte counts of its state'],
       ['Is it deterministic, and does it conserve goods?', 'The model\'s state hashed per run; integer accounting; the same rationing in floating point']],
      [7.5 * cm, 9.5 * cm])

# ---------------- 2 ----------------
P('2. Setup', h1)
P('<b>Scenario.</b> PrivateMaps/Mediterranean, Standard (%d by %d plots, %d land), 10 civilizations, all AI; Normal speed, Noble; no barbarians, '
  'no events, no tech diffusion (the scenario file\'s options); 150 turns; build 504830a0dee0. %d games, one per seed from '
  '<font face="Courier">ledger.py seeds P18</font>, all of which reached turn 150.' %
  (FA['grid']['width'], FA['grid']['height'], MOD['land']['land'], G['n']))
P('<b>The engine\'s food rules</b> (DLL and XML at 3bec049):')
bullets(['A citizen eats <font face="Courier">FOOD_CONSUMPTION_PER_POPULATION</font> = 3 food per turn; unhealthiness adds to it '
         '(<font face="Courier">CvCity::foodConsumption</font> = population &times; 3 &minus; health rate).',
         'A city grows when its stored food reaches <font face="Courier">BASE_CITY_GROWTH_THRESHOLD</font> + size &times; '
         '<font face="Courier">CITY_GROWTH_MULTIPLIER</font> = 30 + 10 &times; size, scaled by game speed, start era and the AI\'s handicap, '
         'all 100 % here (<font face="Courier">CvPlayer::getGrowthThreshold</font>).',
         'A city works up to <font face="Courier">NUM_CITY_PLOTS</font> = 21 plots, the fat cross of radius 2. Its own plot yields at least '
         '3 food, 2 production and 1 commerce (<font face="Courier">iMinCity</font>, CIV4YieldInfos.xml).',
         'Food is local: each city\'s surplus or deficit changes only its own store (<font face="Courier">CvCity::doGrowth</font>).'])

# ---------------- 3 ----------------
P('3. The games', h1)
P('Over 150 turns a game grows to %.1f cities on average (10th to 90th percentile %d to %d) and %.1f citizens (%s).' %
  (G['cities_end'], G['cities_p10_end'], G['cities_p90_end'], G['pop_end'], F_('s01_games')))
figure('s01_games', 'Cities (left; line: mean of the %d games, band: 10th to 90th percentile) and citizens (right; mean) over the games.' % G['n'])
P('The telemetry gives each player\'s total population, not each city\'s. It is split among the player\'s cities by one of two rules: '
  'equally, or in proportion to the square root of each city\'s age (older cities larger). Every result below is computed under the age rule '
  'and checked under the equal rule (section 7.6). %s shows the city sizes the two rules give.' % F_('s02_sizes').capitalize())
figure('s02_sizes', 'Share of cities by size at turns 50, 100 and 150 under the two splitting rules (first 10 games).')

# ---------------- 4 ----------------
P('4. Rebuilding the settlements', h1)
P('4.1 Method', h2)
P('Cities are replayed from the events: a founding creates a city on its plot, a capture changes its owner, a razing removes it. Each plot '
  'within a city\'s fat cross belongs to the nearest city, ties to the older one. A city of size <i>n</i> works its own plot and <i>n</i> of its '
  'plots chosen as the game\'s governor would: by rank (food 3, production 2, commerce 1; assumption), and if those cannot feed the city, the '
  '<i>n</i> plots richest in food, as <font face="Courier">CvCityAI::AI_juggleCitizens</font> avoids starvation. Plot yields are the XML\'s: '
  'terrain, feature, river, hills (&minus;1 food, +1 production, <font face="Courier">iHillsChange</font>), and the improvements a worker would '
  'have built: an irrigated Farm (+%d food) on flat grassland and plains with fresh water, irrigation chains from turn %d (assumption), a Mine '
  '(+%d production) on hills, a Cottage elsewhere, and on the map\'s resource plots the improvement with the best bonus yield.' %
  (MOD['land']['farm_irrigated_food'], 60, MOD['land']['mine_prod']))
P('4.2 Validation', h2)
P('<b>City counts.</b> The rebuilt cities match the number of cities the telemetry reports for each player on <b>%d of %d</b> player-turns.' % (rec['agree'], rec['total']))
P('<b>Food.</b> The games fed their populations: a city whose food fell short would have shrunk. So the share of rebuilt city-turns whose '
  'worked plots cannot feed the observed population measures how far the rebuilt yields fall short of the real ones. %s shows it in three stages:' % F_('s03_calibration').capitalize())
figure('s03_calibration', 'Share of city-turns whose worked plots give less than 3 food per citizen, as the reconstruction adds the map\'s '
       'resources and irrigation chains, then the governor\'s starvation avoidance. All %d games.' % G['n'])
P('Plot yields alone leave %s of city-turns short; adding the map\'s resources and irrigation chains, %s; adding the governor\'s rule, '
  '<b>%s</b> (%s with equal city sizes). The remaining shortfall is food the reconstruction does not model, such as Lighthouse and Harbor '
  'food on water plots and building effects, and brief starvation the real game allowed. It is the baseline against which every variant is compared.' %
  (pct(CAL['1']['share'] * 100), pct(CAL['2']['share'] * 100), pct(CAL['3']['share'] * 100), pct(CAL['3_equal']['share'] * 100)))

# ---------------- 5 ----------------
P('5. Trade, buildings and civics today', h1)
P('5.1 Trade in resources', h2)
P('<b>In the code.</b> A deal item is a <font face="Courier">TradeData</font>: an item type and one integer (<font face="Courier">CvStructs.h</font>), '
  'exported to the executable. <font face="Courier">TRADE_RESOURCES</font> moves one copy of a resource for as long as the deal lasts '
  '(<font face="Courier">CvDeal::startTrade</font> calls <font face="Courier">changeBonusExport</font> and <font face="Courier">changeBonusImport</font> by 1); '
  'either side may cancel after <font face="Courier">PEACE_TREATY_LENGTH</font> = 10 turns (<font face="Courier">CvDeal::turnsToCancel</font>). '
  'There is no quantity: a deal gives a copy or nothing. The list of item types, <font face="Courier">TradeableItems</font> (<font face="Courier">CvEnums.h</font>), '
  'is compiled into the executable too, with a different numbering on its side (<font face="Courier">#ifdef _USRDLL</font>), so new item types are not '
  'a DLL-only change.')
P('<b>In the games.</b> The AIs made %d deals. %d were open borders for open borders. <b>%d involved resources</b>: %d swaps of one resource for '
  'another, %d resources given for nothing, and %d for gold per turn. Resource deals lasted a median of %d turns (%d with a recorded end). '
  'Food resources lead: %s (%s).' %
  (DE['deals'], ob, res_deals, swaps, gifts, gpt_deals, DE['resource_deal_durations']['median'], DE['resource_deal_durations']['n'],
   ', '.join('%s %d' % (k.lower(), v) for k, v in DE['resource_types'][:5]), F_('s04_deals')))
figure('s04_deals', 'What the AIs traded in the %d games: deals by content (left), and the resources in them (right).' % G['n'])
P('Between AIs, then, the resource economy is barter of on/off copies, almost never paid for. Paying gold per turn for a copy is how the AI '
  'treats the human, which is the case the user describes; it does not arise between AIs at all.')

MU, OR, RT, BCN, BX, CX, RN = N['mult'], N['oral'], N['routes'], N['bc'], N['bex'], N['cex'], N['route_need']
P('5.2 How buildings and civics change a city\'s yields', h2)
P('The engine computes every yield of a city the same way (<font face="Courier">CvCity::getYieldRate</font>): a base, the sum of its worked '
  'plots, its specialists, the buildings\' flat yields and, for commerce, its trade routes, times a modifier that adds up the city\'s '
  'buildings, the resources it holds, power, its landmass, the player\'s civics and, in the capital, the capital bonus '
  '(<font face="Courier">CvCity::getBaseYieldRateModifier</font>):')
YEQ = eq(r'Y = \left\lfloor \frac{B \cdot \max\left(0,\ 100 + m_{buildings} + m_{resources} + m_{power} + m_{area} + m_{civics} + m_{capital}\right)}{100} \right\rfloor')
P('The same formula applies to food, so a civic or building that changes food by a percentage changes growth directly. Growth also depends '
  'on how much of the food box a city keeps when it grows (<font face="Courier">iFoodKept</font>, used by <font face="Courier">CvCity::doGrowth</font>).')
table([['Effect in CIV4BuildingInfos.xml', 'Buildings'],
       ['Food by percent / flat food / food on sea plots', '%d / %d / %d' % (BCN['food_pct'], BCN['flat_food'], BCN['sea_food'])],
       ['Food kept after growth', BCN['food_kept']],
       ['Production by percent / with power', '%d / %d' % (BCN['prod_pct'], BCN['power_prod'])],
       ['Gold or research by percent', BCN['gold_research_pct']],
       ['Trade routes / trade route yield by percent', '%d / %d' % (BCN['trade_routes'], BCN['trade_pct'])],
       ['Health / happiness', '%d / %d' % (BCN['health'], BCN['happy'])],
       ['Specialist slots', BCN['specialists']]], [11.0 * cm, 6.0 * cm])
te = BX.get('TOWN_ESSENTIALS', {}); fo = BX.get('FORGE', {}); fa = BX.get('FACTORY', {}); ha = BX.get('HARBOR', {}); ma = BX.get('MARKET', {})
P('Examples from the records (of %d buildings): Town Essentials (cost %d) adds %d %% food, %d food on every sea plot, keeps %d %% of the food box '
  'after growth, adds %d %% gold, %d trade route, %d health and %d happiness. The Forge adds %d %% commerce and costs %d health; the Factory adds '
  '%d %% production; the Market %d %% gold and %d %% trade route yield; the Harbor %d trade routes and %d %% trade route yield.' %
  (BCN['buildings'], te.get('cost', 0), te.get('yield_mod', [0])[0], te.get('sea', [0])[0], te.get('kept', 0), te.get('com', [0])[0], te.get('tr', 0),
   te.get('health', 0), te.get('happy', 0), fo.get('yield_mod', [0, 0, 0])[2], -fo.get('health', 0), fa.get('yield_mod', [0, 0])[1],
   ma.get('com', [0])[0], ma.get('trm', 0), ha.get('tr', 0), ha.get('trm', 0)))
ol, hg, bt, pe, ns = CX.get('ORAL_LAW', {}), CX.get('HUNTER_GATHERER', {}), CX.get('BARTER', {}), CX.get('PLANNED', {}), CX.get('NATIONAL_SOCIALISM', {})
P('Of %d civics, %d change yields by percent, %d change what trade routes yield, %d change the yields of improvements and %d add trade routes. '
  'Every civilization starts with Oral Law (food %d %%, production %d %%, commerce %d %%) and Hunter-Gatherer (commerce from trade %d %%). '
  'Barter turns trade into food (+%d %%); Planned (an Economy civic) into food and production (+%d %%, +%d %%). The Employment civics add yield to whole classes '
  'of improvements: Caste System %s to farms, Labor Allocation %s to farms, pastures and fishing boats. National Socialism forbids foreign trade.' %
  (BCN['civics'], BCN['civ_yield'], BCN['civ_trade'], BCN['civ_imp'], BCN['civ_routes'], ol.get('yield_mod', [0, 0, 0])[0], ol.get('yield_mod', [0, 0, 0])[1],
   ol.get('yield_mod', [0, 0, 0])[2], hg.get('trade', [0, 0, 0])[2], bt.get('trade', [0])[0], pe.get('trade', [0, 0])[0], pe.get('trade', [0, 0])[1],
   '+%d food' % CX.get('CASTE_SYSTEM', {}).get('imp', {}).get('IMPROVEMENT_FARM', [0])[0],
   '+%d food' % CX.get('LABOR_ALLOCATION', {}).get('imp', {}).get('IMPROVEMENT_FARM', [0])[0]))
P('5.3 Their measured effect in the games', h2)
P('The telemetry records each player\'s production as the sum of its cities\' <font face="Courier">getYieldRate(YIELD_PRODUCTION)</font>, and its '
  'gold, research, culture and espionage rates: what the game produced after every building, civic, specialist and trade route. Dividing them '
  'by what the rebuilt cities\' worked plots give measures, turn by turn, how much everything other than the land adds (%s).' % F_('s11_multipliers'))
figure('s11_multipliers', 'Observed production and commerce divided by what the worked plots give, per player and turn (line: median over the '
       'players of the %d games; band: middle half). Dashed: the plots alone. Logarithmic scale.' % G['n'])
P('Production equals the plots\' at turn 50 (median ratio %.2f): Oral Law\'s %d %% is roughly offset by early buildings. It is %.2f times the plots at turn 100 '
  'and <b>%.2f</b> at turn 150 (middle half %.1f to %.1f): by the end, about three quarters of production comes from buildings, civics and specialists, not '
  'from land. Commerce is several times the plots\' throughout (%.1f, %.1f and %.1f at turns 50, 100 and 150): the palace, trade routes, specialists '
  'and percentage buildings, on top of the little commerce the plots give.' %
  (MU['prod']['50'], ol.get('yield_mod', [0, 0])[1], MU['prod']['100'], MU['prod']['150'], MU['prod_iqr150'][0], MU['prod_iqr150'][1],
   MU['com']['50'], MU['com']['100'], MU['com']['150']))
P('<b>Food under the starting civic.</b> The telemetry has no food rate. If Oral Law\'s %d %% food held, the rebuilt cities\' worked plots could not '
  'feed the observed population on <b>%s</b> of %s city-turns, against %s without it. Reading: the AIs leave Oral Law early, or their cities draw '
  'food from sources the reconstruction lacks; it would be contradicted if the games\' cities kept Oral Law long, which a civics field in the '
  'telemetry would show.' % (OR['mod'][0], pct(OR['short_oral']), '{:,}'.format(OR['cityturns']), pct(OR['short_plain'])))
P('5.4 Trade routes', h2)
P('A route\'s profit is (<font face="Courier">CvCity::getBaseTradeProfit</font>) the smaller of the partner\'s size times '
  '<font face="Courier">THEIR_POPULATION_TRADE_PERCENT</font> (50) and the distance times the world\'s <font face="Courier">iTradeProfitPercent</font> '
  '(50 on a Standard map), times <font face="Courier">TRADE_PROFIT_PERCENT</font> (20 %), at least 1.00, then times the route modifiers (buildings, '
  'capital +25 %, overseas +50 %, foreign +100 %) and turned into yields by the civics\' trade yield modifiers:')
eq(r'\pi = \max\left(1.00,\ \frac{20}{100}\cdot\frac{\min(50\,P_{partner},\ 50\,d)}{100}\right)\cdot\frac{100 + m_{route}}{100}')
P('For the rebuilt cities, the best domestic partner pays the floor of 1.00 on <b>%d of %d</b> routes at turn 50, <b>%d of %d</b> at turn 100 and '
  '<b>%d of %d</b> at turn 150 (mean %.2f). On a map this size a route is worth 1.00 times its modifiers; its value comes from the number of routes and '
  'the modifiers, never from what or whom it connects.' %
  (RT['49']['at_floor'], RT['49']['routes'], RT['99']['at_floor'], RT['99']['routes'], RT['149']['at_floor'], RT['149']['routes'], RT['149']['mean']))
P('5.5 What this means for a goods economy', h2)
table([['Today', 'In the goods economy', 'Measured or computed here'],
       ['Percentage yield modifiers of buildings and civics', 'The same formula (equation %d) applied to each good\'s output, with modifiers per good or per category (food, metals, textiles)' % YEQ,
        'Late production is %.1f times the plots\': buildings must remain the main producers' % MU['prod']['150']],
       ['Food kept after growth (Granary, Town Essentials %d %%)' % te.get('kept', 0), 'The granary reserve of staple (section 6.5)', 'Stores cut the staple shortage to %s' % pct(S['network_store']['staple'])],
       ['Food on sea plots (Town Essentials +%d)' % te.get('sea', [0])[0], 'Fish output of worked sea plots', 'Fish is the good stores lose most (spoilage)'],
       ['Specialists (%d buildings give slots)' % BCN['specialists'], 'Recipes run by people: a smith makes tools, a weaver cloth', 'Fuel and tools short in every variant from plots alone'],
       ['Civics on yields and improvements', 'Policies on goods: Oral Law %d %% on staple and goods; Caste System +2 staple per farm; Barter turns trade into food' % ol.get('yield_mod', [0])[0],
        'With Oral Law\'s food the rebuilt cities would starve on %s of city-turns' % pct(OR['short_oral'])],
       ['Trade routes: 1.00 commerce each, times modifiers', 'Channels for goods: each route carries a capacity of goods per turn between cities and civilizations',
        'Moving all potential trade needs %.2f units per route per turn with one route per city (%.1f units per turn per game, %.1f cities)' % (RN['per_route'], RN['units_per_turn'], RN['cities_mean'])],
       ['No foreign trade (National Socialism)', 'An embargo on goods with other civilizations', 'Removes the inter-player flows of section 7.7']],
      [4.6 * cm, 6.6 * cm, 5.8 * cm])

# ---------------- 6 ----------------
story.append(PageBreak())
P('6. The reference model', h1)
P('No source says what a goods economy would do to these settlements, so the model was built for it. It applies the proposed rules to the '
  'rebuilt cities, turn by turn, without changing the games: populations stay as observed. Every quantity is an integer in hundredths of a '
  'unit, as the DLL would hold it; no floating point enters a rule.')
P('6.1 Goods and needs', h2)
needs = MOD['needs']
table([['Need', 'Goods that meet it (in order)', 'Per citizen per turn, ancient / classical / medieval']] +
      [[n[0], ', '.join(n[1]), ' / '.join('%.2f' % (x / 100) for x in n[2])] for n in needs], [3.0 * cm, 5.4 * cm, 8.6 * cm])
P('The staple need is 3 per citizen so that one unit of staple is one unit of the game\'s food. The other levels, the eras (turns 1 to %d, '
  '%d to %d, %d to 150) and the twelve goods are assumptions chosen for illustration; section 7.3 shows how to set them from the land.' %
  (MOD['era_turns'][0], MOD['era_turns'][0] + 1, MOD['era_turns'][1], MOD['era_turns'][1] + 1))
P('6.2 Production', h2)
P('A worked plot <i>j</i> gives goods from its yields and its qualities; for a land plot with food <i>f</i>, the grades <i>G</i> (0 to 100) of the '
  'provinces seeded from the map\'s resource plots, as in <i>Land, not tokens</i>:')
eq(r'q_{grain} = 100\,f \ (\mathrm{farmed}),\ \ 70\,f\ (\mathrm{else});\quad q_{dairy} = 30\,f + \frac{G_{sheep}}{2};\quad q_{wool} = 0.4\,G_{sheep};\quad q_{fruit} = 0.6\,G_{wine};\quad q_{wine} = 0.4\,G_{wine}')
eq(r'q_{wood} = 100\,[\mathrm{forest}];\quad q_{iron,copper,coal} = G_{iron,copper,coal}\,[\mathrm{hills}];\quad q_{fish} = 100\,f + G_{fish}\ (\mathrm{water})')
P('Grain, fruit and dairy are multiplied by a harvest factor of 80 to 120 % per region and turn, drawn from the game\'s seed by a fixed integer '
  'generator (xorshift), so a game\'s weather is the same every time it is replayed.')
P('6.3 Recipes', h2)
P('Each city runs two recipes up to a capacity <i>c</i> = 100 (1 + &lfloor;<i>b</i>/4&rfloor;) hundredths per turn, <i>b</i> its share of the '
  'player\'s buildings: tools from iron and fuel (wood first, then coal), and cloth from wool, one for one (assumptions).')
eq(r'n_{tools} = \min(c,\ q_{iron},\ q_{wood} + q_{coal}), \qquad n_{cloth} = \min(c,\ q_{wool})')
P('6.4 Distribution and rationing', h2)
P('Within a group of cities (one city, or all cities of a player, the trade network), each need is met from its goods in order. When a good '
  'is short, it is shared in proportion to what each city still needs, in exact integers by largest remainders, ties broken by city index:')
REQ = eq(r'x_i = \left\lfloor \frac{A\,d_i}{\sum_k d_k} \right\rfloor + [\,i \in R\,], \qquad |R| = A - \sum_k \left\lfloor \frac{A\,d_k}{\sum_j d_j} \right\rfloor')
P('<i>A</i> is the amount available, <i>d</i><sub>i</sub> city <i>i</i>\'s demand, and <i>R</i> the cities with the largest remainders '
  '<i>A d</i><sub>i</sub> mod &Sigma;<i>d</i>. The shares sum to <i>A</i> exactly. The goods taken are then drawn from the cities that hold them, '
  'by the same rule. A variant loses 10 % of what moves between cities.')
P('6.5 Stores, spoilage and growth', h2)
P('Surplus staple food fills the food box, as today; with stores, a granary reserve of three turns\' need fills first. Other surpluses are lost '
  'without stores; with stores they are kept up to 10 units per citizen per good, and perishable goods lose a share each turn (fish 50 %, '
  'dairy 20 %, fruit 10 %, grain 2 %; assumptions):')
eq(r'X_{t+1} = \min\left(C,\ X_t + q_t - u_t - \left\lfloor \frac{s\,(X_t + q_t - u_t)}{100} \right\rfloor\right)')
P('6.6 Governors', h2)
P('Two rules choose the plots a city works. The <b>yield governor</b> is the game\'s, as rebuilt in section 4. The <b>goods-aware governor</b> fills '
  'each slot with the plot that adds most, counting its contribution to needs still open (staple twice) plus its ranked yields. It is greedy '
  'and deterministic.')
P('6.7 Determinism and conservation', h2)
P('The model\'s state after each turn is hashed. Run twice on the same game and variant, the hashes are <b>%s</b>. All arithmetic is integer, '
  'so goods are conserved exactly: everything produced is consumed, stored, spoiled, sent to growth, lost in transport or, without stores, lost.' %
  ('identical' if N['determinism']['same_hash_twice'] else 'different'))
P('6.8 The variants', h2)
table([['Variant', 'Staple', 'Distribution', 'Stores', 'Other']] +
      [['Today: food local, goods on top', 'local food, as today', 'goods kept in the city', 'no', ''],
       ['Staple as goods, kept in the city', 'a good', 'city', 'no', ''],
       ['Staple as goods, shared in the network', 'a good', 'player network', 'no', ''],
       ['Shared, 10 % lost in transport', 'a good', 'network, 10 % loss', 'no', ''],
       ['Shared, with stores', 'a good', 'network', 'yes', 'no spoilage'],
       ['Shared, stores, spoilage', 'a good', 'network', 'yes', 'spoilage'],
       ['Shared, whole units only', 'a good', 'network', 'no', 'integers in whole units'],
       ['Shared, needs by city size', 'a good', 'network', 'no', 'need levels by size, not era'],
       ['Shared, equal city sizes', 'a good', 'network', 'no', 'equal population split'],
       ['Shared, goods-aware governor', 'a good', 'network', 'no', 'goods-aware governor'],
       ['Shared, stores, spoilage, goods-aware', 'a good', 'network', 'yes', 'spoilage, goods-aware governor']],
      [5.6 * cm, 2.5 * cm, 3.2 * cm, 1.5 * cm, 4.2 * cm])

# ---------------- 7 ----------------
story.append(PageBreak())
P('7. What each choice changes', h1)
P('7.1 Food: a good or not, local or shared', h2)
P('%s gives the share of citizens in cities short of staple food under each variant, over all city-turns of the %d games.' % (F_('s05_staple').capitalize(), G['n']))
figure('s05_staple', 'Citizens in cities short of staple food, by variant (% of citizen-turns). Gray: today\'s rule, the baseline.')
P('Making food a good and keeping it in the city is slightly worse than today (%s against %s), because the harvest now varies. Sharing it '
  'within the network halves the shortage (%s): surpluses of farming cities cover deficits of mining and coastal ones. A 10 %% transport loss '
  'barely changes that (%s). Stores nearly remove it (%s): the granary reserve absorbs bad harvests. Spoilage takes back part of the gain (%s).' %
  (pct(S['goods_local']['staple']), pct(S['today_food']['staple']), pct(S['goods_network']['staple']), pct(S['goods_network_loss']['staple']),
   pct(S['network_store']['staple']), pct(S['network_store_spoil']['staple'])))
bs = N['bysize']
P('By city size (%s), sharing helps the middle sizes most: cities of size 4 to 6 short of staple fall from %s of city-turns under today\'s '
  'rule to %s when shared, and 7 to 10 from %s to %s.' % (F_('s06_bysize'), pct(bs['today_food'][1]), pct(bs['goods_network'][1]), pct(bs['today_food'][2]), pct(bs['goods_network'][2])))
figure('s06_bysize', 'City-turns short of staple food by city size, for four variants.')
P('<b>What this means for the code.</b> Shared staple changes who grows: today a city grows only from its own food '
  '(<font face="Courier">CvCity::doGrowth</font>), so food-poor sites stay small. With sharing, a mining town fed by its farming neighbours grows. '
  'The network pass must run before the cities\' growth, that is in <font face="Courier">CvPlayer::doTurn</font> before the loop that calls '
  '<font face="Courier">CvCity::doTurn</font>, and <font face="Courier">CvCity::foodDifference</font> must read the staple the city received '
  'instead of its own food yield.')
P('7.2 Needs over the game', h2)
figure('s07_needs_time', 'Citizens fully supplied with each need, per turn, for four variants. Tools are needed from the classical era on. '
       'Vertical lines: the era boundaries.')
P(('With staple shared, %s of citizen-turns are short of staple; %s are fully supplied with variety food, %s with clothing and %s with luxury; '
  'fuel and tools stay short for most citizens in every variant. ') % (pct(S['goods_network']['staple']), pct(100 - S['goods_network']['variety']),
  pct(100 - S['goods_network']['clothing']), pct(100 - S['goods_network']['luxury'])) + 'Stores raise variety, clothing and fuel by carrying surpluses forward. The '
  'goods-aware governor lifts fuel (%s short against %s) and variety (%s against %s) by working forests and pastures, at a small cost in staple '
  '(%s against %s).' %
  (pct(S['aware_network_store_spoil']['fuel']), pct(S['network_store_spoil']['fuel']), pct(S['aware_network_store_spoil']['variety']),
   pct(S['network_store_spoil']['variety']), pct(S['aware_network_store_spoil']['staple']), pct(S['network_store_spoil']['staple'])))
P('7.3 Setting needs from the land', h2)
cp = N['capacity']; cs = N['capacity_staple']
P('Whether a need can be met is decided before distribution: by what the land the cities own could give. %s compares, for each need, what '
  'all plots of all cities could give per citizen if every one were worked, with the need per citizen. At turn 150 the land could give %.2f '
  'staple per citizen against a need of 3; for fuel %.2f against %.2f; for tools %.2f against %.2f; for luxury %.2f against %.2f.' %
  (F_('s08_capacity').capitalize(), cs['149'], cp['149']['fuel'], needs[3][2][2] / 100, cp['149']['tools'], needs[4][2][2] / 100,
   cp['149']['luxury'], needs[5][2][2] / 100))
figure('s08_capacity', 'What the land of all cities could give per citizen if every plot were worked (bars), against the need per citizen '
       '(dots), at turns 50, 100 and 150. Logarithmic scale.')
P('<b>Design rule.</b> A need level <i>u</i> per citizen is sustainable only if the land can give it with the share of plots a city can spare '
  'from food. With staple taking 3 per citizen out of a land capacity <i>K</i><sub>staple</sub>, the share of worked plots left for a good '
  '<i>g</i> is roughly 1 &minus; 3/<i>K</i><sub>staple</sub>, and')
eq(r'u_g \ \leq\ \left(1 - \frac{3}{K_{staple}}\right) K_g')
Ks = cs['149']; spare = 1 - 3.0 / Ks
over = [(c, spare * cp['149'][c], needs[i + 1][2][2] / 100) for i, c in enumerate(['variety', 'clothing', 'fuel', 'tools', 'luxury'])]
P(('At turn 150, <i>K</i><sub>staple</sub> = %.2f, so a share of %.2f of the land is spare for other goods, and the bounds are: ' % (Ks, spare)) +
  '; '.join('%s %.2f against a need of %.2f' % (c, b, u) for c, b, u in over) + '. ' +
  ('Every need set at its medieval level is above its bound. ' if all(u > b for c, b, u in over) else
   'Needs above their bound: %s. ' % ', '.join(c for c, b, u in over if u > b)) +
  'Such a good must come from trade, from buildings (charcoal, a forge) or from a lower need. As the cities fill their land, '
  '<i>K</i><sub>staple</sub> falls (%.1f at turn 50, %.1f at turn 100, %.1f at turn 150), and with it the room for everything else. The model '
  'makes the bound computable on any map before a line of game code is written.' % (cs['49'], cs['99'], cs['149']))
P('7.4 Stores and spoilage', h2)
wa = N['waste']
P('Waste as a share of everything produced: %s with goods kept in the city and no stores, %s shared, %s with stores, %s with stores and '
  'spoilage, %s with the goods-aware governor. Stores turn waste into supply; spoilage costs %.1f points of production but makes '
  'perishable goods behave as they should: fish must be eaten where it is landed.' %
  (pct(wa['goods_local']), pct(wa['goods_network']), pct(wa['network_store']), pct(wa['network_store_spoil']),
   pct(wa['aware_network_store_spoil']), wa['network_store_spoil'] - wa['network_store']))
P('7.5 Units and arithmetic', h2)
P('<b>Whole units.</b> Rounding each plot\'s goods down to whole units loses <b>%s</b> of all production, and the needs met fall with it '
  '(staple short %s, variety short %s, against %s and %s in hundredths). Goods must be held in hundredths, or every small plot yield of a '
  'good disappears.' % (pct(N['round_loss']['whole_units']), pct(S['whole_units']['staple']), pct(S['whole_units']['variety']),
                         pct(S['goods_network']['staple']), pct(S['goods_network']['variety'])))
P('<b>Floating point.</b> The same rationing was repeated in single-precision floating point, summing the cities\' demands in two orders. '
  'Of <b>%d</b> rationings, the total differed between the two orders in <b>%d</b> and the allocation to some city in <b>%d</b>. In multiplayer each '
  'computer must reach the same result bit for bit, or the game goes out of sync. Separately, rounding shares down without the remainder step '
  'left goods unallocated in %d of the rationings; the largest-remainder step of equation %d is needed whatever the arithmetic. Integer rationing '
  'with largest remainders is exact and order-independent by construction.' % (fl.get('rations', 0), fl.get('sum_differs', 0),
                                                          fl.get('alloc_differs', 0), fl.get('unconserved', 0), REQ))
P('7.6 Need tiers and population splits', h2)
P('Need levels by city size instead of era lower the shortages (variety short %s against %s, fuel %s against %s), because small cities need '
  'less. Splitting each player\'s population equally instead of by age changes the staple shortage from %s to %s and variety from %s to %s: '
  'the conclusions do not depend on the splitting rule.' %
  (pct(S['tiers_size']['variety']), pct(S['goods_network']['variety']), pct(S['tiers_size']['fuel']), pct(S['goods_network']['fuel']),
   pct(S['goods_network']['staple']), pct(S['equal_split']['staple']), pct(S['goods_network']['variety']), pct(S['equal_split']['variety'])))
P('7.7 What could be traded', h2)
P('Each turn, some players are short of a need that others have spare goods for. Summed over the game, the amount that could change hands, '
  'the smaller of the spare supply and the unmet need, is the market goods would create (%s).' % F_('s09_trade'))
figure('s09_trade', 'Units per game, by need, that some players lack while others have them spare (shared staple, no stores).')
P('Against today\'s %d resource deals in %d games, mostly swaps of copies, this is a continuous flow every turn of %s. The AI must decide '
  'every turn what to sell, at what price and to whom, which is why its valuation (section 8.4) is the centre of the implementation.' %
  (res_deals, G['n'], ', '.join('%s %s' % (k, '{:,.0f}'.format(v)) for k, v in N['trade'].items())))
P('7.8 Cost', h2)
P('%s gives the per-turn cost of the goods pass, written in C as the DLL would run it, for 60 to 600 cities and 12, 40 and 100 goods; '
  'and the cost of the AI\'s marginal values computed by brute force, one recomputation of its network per good.' % F_('s10_cost').capitalize())
figure('s10_cost', 'Milliseconds per game turn for the goods pass (left) and with the AI\'s marginal values (right). Host: Intel Xeon 2.1 GHz, '
       'gcc 13 -O2; the game\'s MSVC 2003 build will differ by a constant factor.')
P('At this scenario\'s size (%d cities, 12 goods) the pass takes %.3f ms per turn and %.1f ms with marginal values. At %d cities and %d goods, '
  '%.2f ms and %.0f ms. A late turn of a large RoM game takes about 20.8 s (research/graphics); even the largest case is below half a percent of '
  'it. The state to save is %s bytes at %d cities and %d goods.' %
  (120, float(b120['us_per_turn']) / 1000, float(b120['us_per_turn_with_ai_marginals']) / 1000, 300, 100, float(b300['us_per_turn']) / 1000,
   float(b300['us_per_turn_with_ai_marginals']) / 1000, '{:,}'.format(int(b300['bytes_state'])), 300, 100))

# ---------------- 8 ----------------
story.append(PageBreak())
P('8. Implementation in the codebase', h1)
P('8.1 Data', h2)
table([['Where', 'What', 'Saved'],
       ['XML: a new CIV4GoodInfos.xml, or new tags on CIV4BonusInfos.xml', 'Unit, category, spoilage, storage, base value; needs per citizen by era or size', 'no'],
       ['XML: CIV4BuildingInfos.xml', 'Recipes: inputs and outputs per run, capacity; storage capacity', 'no'],
       ['XML: CIV4UnitInfos.xml', 'Goods cost per unit; supply use per turn in the field', 'no'],
       ['CvPlot', 'Province grades and reserves (Land, not tokens)', 'yes, with a version flag'],
       ['CvCity', 'Per good: stock, last turn\'s production, use and receipts (int, hundredths); per need: share met', 'yes: CvCity::read and write take a uiFlag'],
       ['CvPlayer', 'Contracts in force; prices if markets are used', 'yes']],
      [5.0 * cm, 8.4 * cm, 3.6 * cm])
P('8.2 The turn', h2)
bullets(['<b>CvPlayer::doTurn</b>, before the loop over <font face="Courier">CvCity::doTurn</font>: for each trade network (the engine\'s '
         '<font face="Courier">CvPlotGroup</font>), collect production, run recipes in dependency order, deliver contracts, ration needs, '
         'update stocks.',
         '<b>CvCity::foodDifference</b>: the staple received replaces the city\'s own food yield, so <font face="Courier">doGrowth</font> keeps working unchanged.',
         '<b>CvCity::changeFreeBonus</b>: a city supplied with a good holds its resource count, so building and unit requirements and happiness '
         'rules read goods without change (section 2 of Land, not tokens).',
         '<b>CvCity::getProductionNeeded</b> and the unit builder: goods costs drawn from the city\'s stock when a unit is completed.',
         '<b>Randomness</b> (harvests): the game\'s synchronised generator, <font face="Courier">getSorenRandNum</font>, never the system\'s.'])
P('8.3 Trade', h2)
P('Three ways to carry goods in deals, from least to most engine risk:')
table([['Option', 'How', 'Risk'],
       ['Reuse TRADE_RESOURCES', 'One item per unit per turn of a good: a contract of 5 wheat per turn is five items. The screen shows them as it shows '
        'resources today.', 'Low; clumsy for large quantities'],
       ['Pack the quantity', 'm_iData = good &times; 65,536 + quantity, interpreted by the DLL. Whether the executable\'s screen can show such an item\'s '
        'text is open.', 'Medium; needs a test in the game'],
       ['A Python trade screen', 'Contracts, shipments, seeds and packages in a screen of RoM\'s own, sending its result to the DLL.', 'Low for the engine; '
        'most interface work']],
      [3.6 * cm, 9.6 * cm, 3.8 * cm])
P('8.4 The AI', h2)
P('The AI needs one quantity everywhere: the marginal value of a unit of each good to each of its networks, the change in its weighted needs '
  'met and production when that good\'s supply rises by one unit. Section 7.8 shows that computing it by brute force every turn is affordable. '
  'It then drives: the governor\'s choice of plots (section 6.6), building choice (recipes whose outputs are worth more than their inputs), '
  'what to offer and accept in trade, and when to go to war over a province. This generalises the valuation of merge request !63, which values '
  'today\'s resources by their effect in the AI\'s own cities.')
P('8.5 Saves and multiplayer', h2)
P('New fields go behind the version flag each class already reads first (<font face="Courier">CvCity::read</font> reads '
  '<font face="Courier">uiFlag</font>); old saves load with empty stocks. All rules are integer and use the synchronised generator, '
  'so the game stays in sync; section 7.5 shows why floating point cannot be used.')

# ---------------- 9 ----------------
P('9. Recommendations', h1)
table([['Decision', 'Recommended', 'Evidence'],
       ['Scale and arithmetic', 'Integers in hundredths; one staple unit = one food', 'Whole units lose %s of production; floats changed allocations in %d rationings' % (pct(N['round_loss']['whole_units']), fl.get('alloc_differs', 0))],
       ['Food', 'Staple is a good, shared in the network, feeding the existing food box', 'Staple shortage %s shared against %s local' % (pct(S['goods_network']['staple']), pct(S['goods_local']['staple']))],
       ['Catalogue', '25 to 40 goods', 'Cost is negligible at any size; the limit is AI and interface, not CPU'],
       ['Need tiers', 'By city size, rising with era', 'Variety short %s by size against %s by era' % (pct(S['tiers_size']['variety']), pct(S['goods_network']['variety']))],
       ['Need levels', 'Set from the land\'s capacity (7.3) per map type', 'Fuel and tools short in every variant at the assumed levels'],
       ['Stores and spoilage', 'Both, from the start', 'Stores: staple short %s; spoilage keeps fish local' % pct(S['network_store_spoil']['staple'])],
       ['Distribution', 'Automatic within a network; transport loss optional', 'Loss of 10 %% changes staple shortage by %.1f points' % (S['goods_network_loss']['staple'] - S['goods_network']['staple'])],
       ['Governor', 'Goods-aware', 'Fuel short %s against %s' % (pct(S['aware_network_store_spoil']['fuel']), pct(S['network_store_spoil']['fuel']))],
       ['Buildings and civics', 'Keep the modifier formula; give it per-good modifiers; specialists run recipes', 'Late production %.1f times the plots\'' % N['mult']['prod']['150']],
       ['Trade routes', 'Goods channels with a capacity per route, beside their commerce', 'All routes at the 1.00 floor; %.2f units per route per turn would carry all trade' % N['route_need']['per_route']],
       ['Trade', 'Contracts as repeated TRADE_RESOURCES items first; a Python screen later', 'TradeData has no quantity; the item list is the executable\'s'],
       ['Order of work', 'Goods and needs in cities, then trade, then industry and units', 'Trade and industry need the goods accounts and the AI\'s marginal values']],
      [3.0 * cm, 6.0 * cm, 8.0 * cm])

# ---------------- 10 ----------------
P('10. How the implementation would be judged', h1)
P('Under the repository\'s rules: each step registered as a prediction before it is built; safety claims (no crash, not slower) by 5 seeded '
  'harness runs per arm; claims that play gets better by at least 30; the human\'s experience by the user\'s games. The model gives each step a '
  'number to predict before the game code exists: for example, that with shared staple and stores fewer than %s of citizen-turns in this scenario '
  'are short of food, measured by the harness from the real cities instead of the rebuilt ones.' % pct(max(1.0, S['network_store_spoil']['staple'])))

# ---------------- 11 ----------------
P('11. Limits', h1)
bullets(['Populations are taken from the games, not simulated: the model says what goods would do to these cities, not how the cities would '
         'have grown differently. Feeding the model\'s growth back needs the rules in the DLL and the harness.',
         'City sizes are split from player totals by an assumed rule; section 7.6 shows the results do not hinge on it.',
         'The reconstruction leaves %s of city-turns short of food under today\'s rules (section 4.2); every comparison is against that baseline.' % pct(CAL['3']['share'] * 100),
         'Need levels, recipes, spoilage and storage are illustrative; the method, not these values, is the result.',
         'One scenario, all AI, 150 turns: late-game industry is not reached.',
         'The goods model counts plots only; section 5.3 shows buildings, civics and specialists add as much again by turn 150, and they enter the goods '
         'economy as modifiers and recipes not simulated here.'], small)

# ---------------- appendix ----------------
P('Appendix: parameters, data and fingerprints', h1)
table([['Parameter', 'Value', 'Kind'],
       ['Staple per citizen', '3 (FOOD_CONSUMPTION_PER_POPULATION)', 'fact'],
       ['Growth threshold', '30 + 10 &times; size', 'fact'],
       ['Plot ranking', 'food 3, production 2, commerce 1', 'assumption'],
       ['Irrigation chains', 'from turn 60', 'assumption'],
       ['Harvest factor', '80 to 120 % per region (16 by 11 plots) and turn', 'assumption'],
       ['Province widths', 'ores 1.5 plots, wine and livestock 2, fish 1.5', 'assumption'],
       ['Spoilage per turn', ', '.join('%s %d %%' % (k, v) for k, v in MOD['spoil'].items()), 'assumption'],
       ['Storage', '10 units per citizen per good; granary 3 turns of staple', 'assumption'],
       ['Transport loss', '10 % (one variant)', 'assumption'],
       ['Recipe capacity', '1 + buildings per city / 4 units per turn', 'assumption']], [4.5 * cm, 8.5 * cm, 4.0 * cm])
P('<b>Fingerprints</b> (first 16 hex digits of the hash of every state of every game, per variant): ' +
  '; '.join('%s <font face="Courier">%s</font>' % (k, v) for k, v in N['hash'].items()) + '.', small)
P('<b>Data.</b> research/economy/settlement/data: games.json (settlements and deals of the %d games), facts_medstd.json (records and map), '
  'model.json, series.json, calibration.json, deals.json, bench.csv, snumbers.json.' % G['n'], small)


def on_page(c, doc):
    c.saveState(); c.setFont('Helvetica', 7.5); c.setFillColor(INK2)
    if doc.page > 1:
        c.drawString(2.0 * cm, 1.2 * cm, 'Settlement Economy: a quantitative design study for Rise of Mankind')
        c.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, str(doc.page))
    c.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.8 * cm, bottomMargin=1.9 * cm,
                        title='Settlement Economy', author='Rise of Mankind research', subject='Goods, needs and trade of settlements')
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUT, EQN[0], 'equations', len(FIGORDER), 'figures')
