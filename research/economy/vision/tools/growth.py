#!/usr/bin/env python3
"""Food in whole tons, with size following the food box, on the cities of the 30 games.

Each city is founded at size 1 on its observed plot and turn (captures and razings as observed) and then grows only
from its own food, under the rule of CvCity::doGrowth with every quantity in tons (1 food = 100 t):
harvest from the plots the governor works (settlement model: rebuilt plots, weather); citizens eat 300 t each,
perishable goods first; what is left is the food box, which loses each good's spoilage rate for the preservation
level; at the threshold (30 + 10 x size) x 100 t the city grows and keeps 20 % (Settlement Essentials); if the box
cannot cover what the citizens eat, the box empties and the city loses one citizen, as today.

Arms: spoilage rates by preservation level, held for the whole game (none, Pottery, Fermentation, Refrigeration =
no loss, which is today's rule). Modes: 'food' (food is the only limit) and 'capped' (a player's cities may not
together exceed its observed population at that turn: the game's other limits, health and happiness, held as observed).
usage: growth.py <economy dir>"""
import collections, importlib.util, json, multiprocessing as mp, os, sys
import numpy as np

ROOT = sys.argv[1]
SETTLE = os.path.join(ROOT, 'settlement')
TON = 100                     # tons per unit of food yield
EAT = 3 * TON                 # FOOD_CONSUMPTION_PER_POPULATION = 3
KEPT = 20                     # BUILDING_SETTLEMENT_ESSENTIALS iFoodKept, free from ERA_ANCIENT
FOOD = ['fish', 'dairy', 'fruit', 'grain']  # eating order: most perishable first
# spoilage of what stays in the box, per mille per turn, by preservation level (design values, section 'Food')
LEVELS = {
    'none':          {'fish': 300, 'dairy': 250, 'fruit': 150, 'grain': 60},
    'pottery':       {'fish': 200, 'dairy': 250, 'fruit': 100, 'grain': 10},
    'fermentation':  {'fish': 100, 'dairy': 50,  'fruit': 20,  'grain': 10},
    'refrigeration': {'fish': 0,   'dairy': 0,   'fruit': 0,   'grain': 0},
}


def load():
    sys.argv = ['model.py', SETTLE]
    spec = importlib.util.spec_from_file_location('model', os.path.join(SETTLE, 'tools', 'model.py'))
    M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
    return M


M = None


def threshold(size):
    return (30 + 10 * size) * TON


TT = None


def governor(p, n, pl, hf):
    """The settlement model's governor (M.city_tiles: the n best plots by rank; if they do not feed the city, the n richest
    in food), with the food it checks scaled by the harvest factor, so that it sees a civic's food modifier."""
    if not pl: return []
    by_rank, by_food = pl
    t = by_rank[:n]
    food = int(M.CITY_TG[p][0] + M.CITY_TG[p][1]) + (int(M.TG[t][:, 0].sum() + M.TG[t][:, 1].sum()) if t else 0)
    return t if food * hf // 100 >= EAT * n else by_food[:n]


def level_rates(game, o, t, rates):
    """rates: a dict of rates (one level all game), or 'timed': each player's level from the earliest turn it could know
    Pottery and Fermentation (data/tech_turns.json; a lower bound, so the most favourable case)."""
    if rates != 'timed': return rates
    if str(o) not in TT[game['seed']]: return LEVELS['pottery']  # barbarian cities: not in the header; Pottery from the start
    e = TT[game['seed']][str(o)]['earliest']
    if e['TECH_FERMENTATION'] is not None and t >= e['TECH_FERMENTATION']: return LEVELS['fermentation']
    if e['TECH_POTTERY'] is not None and t >= e['TECH_POTTERY']: return LEVELS['pottery']
    return LEVELS['none']


def simulate(gi, rates, capped, hf=100):
    global M, TT
    if M is None: M = load()
    if TT is None: TT = {g['seed']: g['players'] for g in json.load(open(os.path.join(ROOT, 'vision', 'data', 'tech_turns.json')))}
    game = M.GAMES[gi]
    hist = M.cities_by_turn(game)
    caps = {e['plot']: e.get('pop') for e in game['events'] if e['kind'] == 'capture'}
    city = {}  # plot -> dict(size, stock{good: t})
    fi = [M.GI[g] for g in FOOD]
    m = collections.Counter(); traj = []
    last_key = None; plots = {}
    for t in range(game['turns']):
        alive = hist[t]
        for p in list(city):
            if p not in alive: del city[p]
        for p, (o, f0) in alive.items():
            if p not in city: city[p] = dict(size=1, stock=np.zeros(len(FOOD), np.int64))
        prev = hist[t - 1] if t else {}
        for p, (o, f0) in alive.items():  # a capture: the observed size if the event gives one
            if p in prev and prev[p][0] != o and caps.get(p): city[p]['size'] = max(1, int(caps[p]))
        M.TG, M.CITY_TG, M.RANK = M.LATE if t >= M.CHAIN_TURN else M.EARLY
        key = (tuple(sorted(alive)), t >= M.CHAIN_TURN)
        if key != last_key: plots = M.owned_plots(alive); last_key = key
        room = {}
        if capped:
            tot = collections.Counter(); obs = {}
            for p, (o, f0) in alive.items(): tot[o] += city[p]['size']
            for o in tot:
                rows = game['players'].get(str(o)) or game['players'].get(o)
                obs[o] = rows[t][2] if rows and t < len(rows) else tot[o]
                room[o] = obs[o] - tot[o]
        for p in sorted(alive):
            c = city[p]; o = alive[p][0]; n = c['size']
            tiles = governor(p, n, plots.get(p), hf)
            g = M.CITY_TG[p] + (M.TG[tiles].sum(axis=0) if tiles else 0)
            wx = M.weather(game['seed'], t, (M.XY[p][0] // 16) * 4 + M.XY[p][1] // 11)
            rv = level_rates(game, o, t, rates); r = np.array([rv[x] for x in FOOD], np.int64)
            harvest = np.array([int(g[i]) * (wx if FOOD[k] != 'fish' else 100) // 100 * hf // 100 for k, i in enumerate(fi)], np.int64)
            avail = c['stock'] + harvest
            need = EAT * n
            m['max_harvest'] = max(m['max_harvest'], int(harvest.sum())); era = 0 if t < 50 else (1 if t < 100 else 2)
            m['harvest'] += int(harvest.sum()); m['eaten_need'] += need; m['cityturns'] += 1; m['popturns'] += n
            if int(avail.sum()) < need:  # the box cannot cover the citizens: it empties and the city starves
                m['eaten'] += int(avail.sum()); c['stock'][:] = 0
                m['starve'] += 1
                if n > 1: c['size'] -= 1; m['shrink'] += 1
                continue
            m['eaten'] += need
            left = avail.copy(); want = need
            for k in range(len(FOOD)):  # perishable first
                take = min(int(left[k]), want); left[k] -= take; want -= take
            lost = left * r // 1000
            m['spoiled'] += int(lost.sum()); left -= lost
            m['max_box'] = max(m['max_box'], int(left.sum()))
            T = threshold(n)
            if int(left.sum()) >= T:
                if capped and room.get(o, 1) <= 0:  # held at the threshold, as CvCity::doGrowth under avoid-growth
                    over = int(left.sum()) - T; m['held'] += 1; m['held_t'] += over; m['held_t_%d' % era] += over; m['held_n_%d' % era] += 1
                    for k in range(len(FOOD)):
                        d = min(int(left[k]), over); left[k] -= d; over -= d
                else:
                    use = T - T * KEPT // 100
                    for k in range(len(FOOD)):
                        d = min(int(left[k]), use); left[k] -= d; use -= d
                    c['size'] += 1; m['grow'] += 1
                    if capped: room[o] -= 1
            c['stock'] = left
        if t in (50, 100, 150) or t == game['turns'] - 1:
            sim = collections.Counter(); obs = collections.Counter()
            for p, (o, f0) in alive.items(): sim[o] += city[p]['size']
            for o in sim:
                rows = game['players'].get(str(o)) or game['players'].get(o)
                obs[o] = rows[t][2] if rows and t < len(rows) else 0
            sizes = sorted(city[p]['size'] for p in alive)
            traj.append(dict(t=t, sim=sum(sim.values()), obs=sum(obs.values()), cities=len(alive),
                             abs_err=sum(abs(sim[o] - obs[o]) for o in sim), median_size=sizes[len(sizes) // 2] if sizes else 0, max_size=sizes[-1] if sizes else 0))
    return dict(m=dict(m), traj=traj)


def arm(pool, rates, capped, hf=100):
    res = pool.starmap(simulate, [(gi, rates, capped, hf) for gi in range(len(M.GAMES))])
    m = collections.Counter(); tr = collections.defaultdict(collections.Counter); mx = 0
    for x in res:
        mb = x['m'].pop('max_box', 0); mx = max(mx, mb); mh = x['m'].pop('max_harvest', 0); m['max_harvest'] = max(m['max_harvest'], mh); m.update(x['m'])
        for row in x['traj']:
            for k, v in row.items():
                if k not in ('t', 'median_size', 'max_size'): tr[row['t']][k] += v
            tr[row['t']]['max_size'] = max(tr[row['t']]['max_size'], row['max_size'])
            tr[row['t']]['median_sum'] += row['median_size']; tr[row['t']]['games'] += 1
    m['max_box'] = mx
    return dict(m=dict(m), traj={t: dict(v) for t, v in sorted(tr.items())})


if __name__ == '__main__':
    M = load()
    out = dict(ton=TON, eat=EAT, kept=KEPT, food_order=FOOD, levels=LEVELS, games=len(M.GAMES), arms={})
    with mp.Pool(4) as pool:
        for capped in (False, True):
            for lv, rates in LEVELS.items():
                name = lv + ('_capped' if capped else '_food')
                out['arms'][name] = arm(pool, rates, capped)
                a = out['arms'][name]; mm = a['m']
                print(name, {t: (v['sim'], v['obs']) for t, v in a['traj'].items()}, 'starve/cityturn %.4f' % (mm.get('starve', 0) / mm['cityturns']),
                      'spoiled/harvest %.4f' % (mm.get('spoiled', 0) / mm['harvest']), 'max box', mm['max_box'], flush=True)
        out['arms']['timed_food'] = arm(pool, 'timed', False); out['arms']['timed_capped'] = arm(pool, 'timed', True)
        # Oral Law, the starting civic: food -25 % (CIV4CivicInfos.xml), applied to the harvest
        out['arms']['oral_timed_food'] = arm(pool, 'timed', False, 75); out['arms']['oral_timed_capped'] = arm(pool, 'timed', True, 75)
        for name in ('timed_food', 'timed_capped', 'oral_timed_food', 'oral_timed_capped'):
            a = out['arms'][name]; print(name, {t: (v['sim'], v['obs']) for t, v in a['traj'].items()}, 'starve/cityturn %.5f' % (a['m'].get('starve', 0) / a['m']['cityturns']), flush=True)
        # sweep: the no-preservation rates scaled, to show the lever
        out['sweep'] = {}
        for k in (0, 25, 50, 100, 150, 200, 300):
            sc = {g: v * k // 100 for g, v in LEVELS['none'].items()}
            out['sweep'][k] = dict(rates=sc, food=arm(pool, sc, False), capped=arm(pool, sc, True))
            print('sweep', k, out['sweep'][k]['food']['traj'][150]['sim'], out['sweep'][k]['capped']['traj'][150]['sim'], flush=True)
        # determinism: one game twice
        a1 = simulate(0, LEVELS['pottery'], True); a2 = simulate(0, LEVELS['pottery'], True)
        out['determinism'] = a1 == a2
    json.dump(out, open(os.path.join(ROOT, 'vision', 'data', 'growth.json'), 'w'), indent=1)
    print('deterministic', out['determinism'])
