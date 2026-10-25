#!/usr/bin/env python3
"""Figures of the settlement economy study, from data/ (games.py, model.py, analysis.py, calibrate.py, bench.c).
Writes figures/*.png and data/snumbers.json (every number the text quotes).
usage: sfigures.py <settlement dir>"""
import csv, json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = sys.argv[1]
D = lambda n: json.load(open(os.path.join(ROOT, 'data', n)))
MOD, SER, CAL, DEA = D('model.json'), D('series.json'), D('calibration.json'), D('deals.json')
BEN = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'bench.csv'))))
FIG = os.path.join(ROOT, 'figures'); os.makedirs(FIG, exist_ok=True)
N = {}
C = dict(blue='#2a78d6', orange='#eb6834', aqua='#1baf7a', yellow='#eda100', magenta='#e87ba4', green='#008300', violet='#6250d6',
         red='#e34948', ink='#0b0b0b', ink2='#52514e', grid='#e6e5e1')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.5, 'axes.edgecolor': C['ink2'], 'axes.labelcolor': C['ink2'],
                     'xtick.color': C['ink2'], 'ytick.color': C['ink2'], 'text.color': C['ink'], 'axes.titlesize': 9,
                     'axes.titleweight': 'bold', 'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': True,
                     'grid.color': C['grid'], 'grid.linewidth': 0.6, 'lines.linewidth': 2, 'legend.frameon': False, 'savefig.dpi': 220})
W = 6.6


def save(fig, name):
    fig.savefig(os.path.join(FIG, name + '.png'), bbox_inches='tight', pad_inches=0.04); plt.close(fig)


V = MOD['variants']
LABEL = {'today_food': 'Today: food local, goods on top', 'goods_local': 'Staple as goods, kept in the city',
         'goods_network': 'Staple as goods, shared in the network', 'goods_network_loss': 'Shared, 10 % lost in transport',
         'network_store': 'Shared, with stores', 'network_store_spoil': 'Shared, stores, spoilage',
         'whole_units': 'Shared, whole units only', 'tiers_size': 'Shared, needs by city size', 'equal_split': 'Shared, equal city sizes',
         'aware_network': 'Shared, goods-aware governor', 'aware_network_store_spoil': 'Shared, stores, spoilage, goods-aware'}
NEEDS = [n[0] for n in MOD['needs']]

# ---------- the games ----------
g = SER['games']; t = np.arange(len(g['cities']))
fig, axs = plt.subplots(1, 2, figsize=(W, 2.3))
axs[0].fill_between(t, g['cities_p10'], g['cities_p90'], color=C['blue'], alpha=0.18, lw=0); axs[0].plot(t, g['cities'], color=C['blue'])
axs[0].set_title('Cities in the game', loc='left'); axs[0].set_xlabel('turn')
axs[1].plot(t, g['pop'], color=C['orange']); axs[1].set_title('Citizens in the game', loc='left'); axs[1].set_xlabel('turn')
fig.tight_layout(); save(fig, 's01_games')
N['games'] = dict(n=MOD['variants']['today_food']['games'], cities_end=round(g['cities'][-1], 1), pop_end=round(g['pop'][-1], 1),
                  cities_p10_end=g['cities_p10'][-1], cities_p90_end=g['cities_p90'][-1], recon=SER['reconstruction'])

fig, axs = plt.subplots(1, 3, figsize=(W, 2.2), sharey=True)
for ax, tt in zip(axs, (49, 99, 149)):
    for rule, col, off in [('age', C['blue'], -0.2), ('equal', C['orange'], 0.2)]:
        rows = [(n, c) for (t_, n, c) in SER['games']['sizes'][rule] if t_ == tt]
        tot = sum(c for _, c in rows) or 1
        ax.bar([n + off for n, _ in rows], [c / tot for _, c in rows], width=0.4, color=col, label='older cities larger' if rule == 'age' else 'equal split')
    ax.set_title(f'Turn {tt + 1}', loc='left'); ax.set_xlabel('city size')
axs[0].set_ylabel('share of cities'); axs[2].legend(fontsize=7)
fig.tight_layout(); save(fig, 's02_sizes')

# ---------- calibration ----------
stages = [('1', 'Plot yields only'), ('2', '+ map resources and irrigation chains'), ('3', '+ governor avoids starvation'), ('3_equal', 'same, equal city sizes')]
fig, ax = plt.subplots(figsize=(W, 1.8))
vals = [CAL[k]['share'] * 100 for k, _ in stages]
ax.barh(range(len(stages)), vals, color=[C['ink2'], C['ink2'], C['blue'], C['blue']], height=0.55)
for i, v in enumerate(vals): ax.text(v + 0.4, i, f'{v:.1f} %', va='center', fontsize=7.5)
ax.set_yticks(range(len(stages))); ax.set_yticklabels([s[1] for s in stages]); ax.invert_yaxis(); ax.grid(axis='y', visible=False)
ax.set_xlabel('city-turns whose worked plots cannot feed the observed population (%)')
save(fig, 's03_calibration')
N['calibration'] = {k: CAL[k] for k, _ in stages}

# ---------- today's deals ----------
fig, axs = plt.subplots(1, 2, figsize=(W, 2.5), gridspec_kw=dict(width_ratios=[1, 1.1]))
comp = [(k if k.strip() and not k.startswith(' ') else 'nothing' + k, v) for k, v in DEA['composition']]
lab = [k.replace(' for ', ' for\n') if len(k) > 26 else k for k, _ in comp]
axs[0].barh(range(len(comp)), [v for _, v in comp], color=C['blue'], height=0.6)
for i, (_, v) in enumerate(comp): axs[0].text(v + 15, i, str(v), va='center', fontsize=7)
axs[0].set_yticks(range(len(comp))); axs[0].set_yticklabels(lab, fontsize=7); axs[0].invert_yaxis(); axs[0].grid(axis='y', visible=False)
axs[0].set_title('Deals between AIs, 30 games', loc='left')
rt = DEA['resource_types'][:12]
axs[1].barh(range(len(rt)), [v for _, v in rt], color=C['orange'], height=0.6)
axs[1].set_yticks(range(len(rt))); axs[1].set_yticklabels([k for k, _ in rt], fontsize=7); axs[1].invert_yaxis(); axs[1].grid(axis='y', visible=False)
axs[1].set_title('Resources in those deals', loc='left')
fig.tight_layout(); save(fig, 's04_deals')
N['deals'] = DEA

# ---------- staple shortfall by variant and by city size ----------
order = ['today_food', 'goods_local', 'goods_network', 'goods_network_loss', 'network_store', 'network_store_spoil',
         'whole_units', 'tiers_size', 'equal_split', 'aware_network', 'aware_network_store_spoil']
pt = {k: V[k]['m']['popturns'] for k in order}
short = {k: {n: V[k]['m'].get('shortpop_' + n, 0) / pt[k] for n in NEEDS} for k in order}
fig, ax = plt.subplots(figsize=(W, 3.0))
ys = range(len(order))
ax.barh(ys, [short[k]['staple'] * 100 for k in order], color=[C['ink2']] + [C['blue']] * (len(order) - 1), height=0.6)
for i, k in enumerate(order): ax.text(short[k]['staple'] * 100 + 0.2, i, f"{short[k]['staple'] * 100:.1f} %", va='center', fontsize=7)
ax.set_yticks(ys); ax.set_yticklabels([LABEL[k] for k in order], fontsize=7.5); ax.invert_yaxis(); ax.grid(axis='y', visible=False)
ax.set_xlabel('citizens in cities short of staple food (% of citizen-turns)')
save(fig, 's05_staple')
N['short'] = {k: {n: round(v * 100, 1) for n, v in short[k].items()} for k in order}
N['waste'] = {k: round(V[k]['waste'] / max(1, sum(V[k]['produced'])) * 100, 1) for k in order}
N['round_loss'] = {k: round(V[k]['round_loss'] / max(1, sum(V[k]['produced'])) * 100, 2) for k in order}
N['hash'] = {k: V[k]['hash'] for k in order}
N['determinism'] = MOD['determinism']

fig, ax = plt.subplots(figsize=(W, 2.2))
bins = ['1-3', '4-6', '7-10', '11+']
for k, col, off in [('today_food', C['ink2'], -0.27), ('goods_local', C['orange'], -0.09), ('goods_network', C['blue'], 0.09),
                    ('network_store_spoil', C['aqua'], 0.27)]:
    b = np.array(SER[k]['bysize']); sh = b[:, 0] / np.maximum(b[:, 1], 1) * 100
    ax.bar(np.arange(4) + off, sh, width=0.18, color=col, label=LABEL[k])
ax.set_xticks(range(4)); ax.set_xticklabels(['size ' + b for b in bins]); ax.set_ylabel('city-turns short of staple (%)')
ax.legend(fontsize=6.8, ncol=2, loc='upper left'); ax.grid(axis='x', visible=False)
save(fig, 's06_bysize')
N['bysize'] = {k: [round(x[0] / max(1, x[1]) * 100, 1) for x in SER[k]['bysize']] for k in ('today_food', 'goods_local', 'goods_network', 'network_store_spoil')}
N['float'] = SER['goods_network']['float']

# ---------- needs over time ----------
show = [('today_food', C['ink2']), ('goods_network', C['blue']), ('network_store_spoil', C['aqua']), ('aware_network_store_spoil', C['orange'])]
fig, axs = plt.subplots(2, 3, figsize=(W, 3.9), sharex=True, sharey=True)
for ni, (ax, nm) in enumerate(zip(axs.flat, NEEDS)):
    for k, col in show:
        s = np.array(SER[k]['share'])[:, ni] * 100
        if nm == 'tools': s[:50] = np.nan
        ax.plot(s, color=col, lw=1.5, label=LABEL[k])
    ax.set_title(nm.title(), loc='left'); ax.set_ylim(0, 102)
    for x in MOD['era_turns']: ax.axvline(x, color=C['grid'], lw=1)
for ax in axs[1]: ax.set_xlabel('turn')
axs[0, 0].set_ylabel('citizens fully supplied (%)'); axs[1, 0].set_ylabel('citizens fully supplied (%)')
fig.legend(*axs[0, 0].get_legend_handles_labels(), loc='lower center', ncol=2, fontsize=7, bbox_to_anchor=(0.5, -0.06))
fig.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, 's07_needs_time')

# ---------- carrying capacity against needs ----------
capc = SER['capacity_per_citizen']; goods_of = {n[0]: n[1] for n in MOD['needs']}
fig, axs = plt.subplots(1, 3, figsize=(W, 2.5), sharey=True)
capn = {}
for ax, (tt, era) in zip(axs, [('49', 0), ('99', 1), ('149', 2)]):
    cats = NEEDS[1:]
    cv = [sum(capc[tt][x] for x in goods_of[c]) + (capc[tt]['iron'] if c == 'tools' else 0) + (capc[tt]['wool'] if c == 'clothing' else 0) for c in cats]
    nv = [MOD['needs'][i + 1][2][era] / 100 for i in range(len(cats))]
    ax.bar(np.arange(len(cats)), cv, color=C['blue'], width=0.6, label='land could give')
    ax.scatter(np.arange(len(cats)), nv, color=C['orange'], zorder=3, s=22, label='need per citizen')
    ax.set_xticks(range(len(cats))); ax.set_xticklabels([c[:5] for c in cats], fontsize=7, rotation=0)
    ax.set_title(f'Turn {int(tt) + 1}', loc='left'); ax.set_yscale('log'); ax.grid(axis='x', visible=False)
    capn[tt] = {c: round(v, 3) for c, v in zip(cats, cv)}
axs[0].set_ylabel('units per citizen per turn'); axs[2].legend(fontsize=7, loc='upper right')
fig.tight_layout(); save(fig, 's08_capacity')
N['capacity'] = capn
N['capacity_staple'] = {tt: round(capc[tt]['grain'] + capc[tt]['fish'], 2) for tt in capc}

# ---------- trade potential ----------
tp = np.array(V['goods_network']['trade_potential']) / 100.0
turns = V['goods_network']['turns']; games_n = V['goods_network']['games']
first = {n[1][0]: n[0] for n in MOD['needs']}
cats = [(first[gname], tp[i] / games_n) for i, gname in enumerate(MOD['goods']) if gname in first and tp[i] > 0]
fig, ax = plt.subplots(figsize=(W, 2.1))
ax.barh(range(len(cats)), [v for _, v in cats], color=C['blue'], height=0.55)
for i, (_, v) in enumerate(cats): ax.text(v * 1.01, i, f'{v:,.0f}', va='center', fontsize=7)
ax.set_yticks(range(len(cats))); ax.set_yticklabels([c for c, _ in cats]); ax.invert_yaxis(); ax.grid(axis='y', visible=False)
ax.set_xlabel('units per game that some players lack while others have them spare')
save(fig, 's09_trade')
N['trade'] = {c: round(v, 0) for c, v in cats}
N['trade_turns_per_game'] = round(turns / games_n, 1)

# ---------- cost ----------
fig, axs = plt.subplots(1, 2, figsize=(W, 2.4), sharey=False)
for gs, col in [('12', C['blue']), ('40', C['orange']), ('100', C['aqua'])]:
    rows = [r for r in BEN if r['goods'] == gs]
    x = [int(r['cities']) for r in rows]
    axs[0].plot(x, [float(r['us_per_turn']) / 1000 for r in rows], color=col, marker='o', ms=4, label=f'{gs} goods')
    axs[1].plot(x, [float(r['us_per_turn_with_ai_marginals']) / 1000 for r in rows], color=col, marker='o', ms=4, label=f'{gs} goods')
for ax, tt in zip(axs, ['Goods pass per turn', 'With the AI\'s marginal values']):
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel('cities in the game'); ax.set_title(tt, loc='left')
    ax.set_xticks([60, 120, 300, 600]); ax.set_xticklabels(['60', '120', '300', '600']); ax.minorticks_off()
axs[0].set_ylabel('milliseconds'); axs[1].legend(fontsize=7)
fig.tight_layout(); save(fig, 's10_cost')
N['bench'] = BEN


# ---------- buildings, civics, specialists and trade routes ----------
Y = D('yields.json'); BC = D('bc.json')
fig, axs = plt.subplots(1, 2, figsize=(W, 2.4), sharey=True)
for ax, key, col, tt in [(axs[0], 'prod_ratio', C['blue'], 'Production: observed / plots'), (axs[1], 'com_ratio', C['orange'], 'Commerce: observed / plots')]:
    r = Y[key]; x = np.arange(len(r['p50']))
    lo = np.array([v if v is not None else np.nan for v in r['p25']]); md = np.array([v if v is not None else np.nan for v in r['p50']])
    hi = np.array([v if v is not None else np.nan for v in r['p75']])
    ax.fill_between(x, lo, hi, color=col, alpha=0.18, lw=0); ax.plot(x, md, color=col)
    ax.axhline(1, color=C['ink2'], lw=0.8, ls=(0, (2, 2))); ax.set_title(tt, loc='left'); ax.set_xlabel('turn'); ax.set_yscale('log')
    ax.set_xlim(10, 149)
axs[0].set_ylabel('ratio (log scale)')
fig.tight_layout(); save(fig, 's11_multipliers')
pick = lambda a, t: a[t]
N['mult'] = dict(prod={t + 1: pick(Y['prod_ratio']['p50'], t) for t in (49, 99, 149)}, com={t + 1: pick(Y['com_ratio']['p50'], t) for t in (49, 99, 149)},
                 prod_iqr150=[Y['prod_ratio']['p25'][149], Y['prod_ratio']['p75'][149]])
N['oral'] = dict(mod=Y['oral'], short_plain=round(Y['food']['short_plain'] / Y['food']['cityturns'] * 100, 1),
                 short_oral=round(Y['food']['short_oral'] / Y['food']['cityturns'] * 100, 1), cityturns=Y['food']['cityturns'])
N['routes'] = Y['profit']
B = BC['buildings']
cnt = lambda f: sum(1 for b in B if f(b))
N['bc'] = dict(buildings=len(B), civics=len(BC['civics']), food_pct=cnt(lambda b: b['yield_mod'][0] > 0), flat_food=cnt(lambda b: b['yield_change'][0] > 0),
               sea_food=cnt(lambda b: b['sea'][0] > 0), food_kept=cnt(lambda b: b['food_kept'] > 0), prod_pct=cnt(lambda b: b['yield_mod'][1] > 0),
               power_prod=cnt(lambda b: b['power_mod'][1] > 0), gold_research_pct=cnt(lambda b: b['commerce_mod'][0] > 0 or b['commerce_mod'][1] > 0),
               trade_routes=cnt(lambda b: b['trade_routes'] > 0), trade_pct=cnt(lambda b: b['trade_mod'] > 0 or b['foreign_trade_mod'] > 0),
               health=cnt(lambda b: b['health'] > 0), happy=cnt(lambda b: b['happy'] > 0), specialists=cnt(lambda b: b['specialists'] > 0),
               civ_yield=sum(1 for c in BC['civics'] if any(c['yield_mod'])), civ_trade=sum(1 for c in BC['civics'] if any(c['trade_yield_mod'])),
               civ_imp=sum(1 for c in BC['civics'] if c['improvement_yields']), civ_routes=sum(1 for c in BC['civics'] if c['trade_routes']))
EX = {b['type']: b for b in B}
N['bex'] = {k[9:]: dict(yield_mod=EX[k]['yield_mod'], sea=EX[k]['sea'], kept=EX[k]['food_kept'], com=EX[k]['commerce_mod'], tr=EX[k]['trade_routes'],
                        trm=EX[k]['trade_mod'], health=EX[k]['health'], happy=EX[k]['happy'], cost=EX[k]['cost'])
            for k in ('BUILDING_TOWN_ESSENTIALS', 'BUILDING_FORGE', 'BUILDING_FACTORY', 'BUILDING_MARKET', 'BUILDING_LIBRARY', 'BUILDING_HARBOR', 'BUILDING_LIGHTHOUSE') if k in EX}
CVX = {c['type']: c for c in BC['civics']}
N['cex'] = {k[6:]: dict(yield_mod=CVX[k]['yield_mod'], trade=CVX[k]['trade_yield_mod'], tr=CVX[k]['trade_routes'], imp=CVX[k]['improvement_yields'],
                        nofor=CVX[k]['no_foreign_trade'], option=CVX[k]['option'])
            for k in ('CIVIC_ORAL_LAW', 'CIVIC_TABLETS', 'CIVIC_HUNTER_GATHERER', 'CIVIC_BARTER', 'CIVIC_PLANNED', 'CIVIC_SLAVERY', 'CIVIC_CASTE_SYSTEM',
                      'CIVIC_LABOR_ALLOCATION', 'CIVIC_NATIONAL_SOCIALISM', 'CIVIC_PUBLIC_SCHOOLS') if k in CVX}
# would trade routes bind as goods channels? the potential trade per turn against one route per city
tp_per_turn = sum(N['trade'].values()) / max(1, N['trade_turns_per_game'])
N['route_need'] = dict(units_per_turn=round(tp_per_turn, 1), cities_mean=round(float(np.mean(g['cities'][20:])), 1),
                       per_route=round(tp_per_turn / max(1.0, float(np.mean(g['cities'][20:]))), 3))

json.dump(N, open(os.path.join(ROOT, 'data', 'snumbers.json'), 'w'), indent=1)
print('ok')
