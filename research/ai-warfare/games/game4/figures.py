#!/usr/bin/env python3
"""Figures for game 4's analysis, computed from the generated tables in this folder.

usage: python3 -I figures.py [section ...]   sections: wars, cities, econ (default: all)
Every figure is printed with its turn; nothing here interprets.
"""
import collections, csv, os, sys

D = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: list(csv.DictReader(open(os.path.join(D, f), newline='')))
H = '3'
E = {(int(r['turn']), r['player']): r for r in rd('economy.csv')}
X = collections.defaultdict(list)
for r in rd('techs.csv'): X[r['player']].append(int(r['turn']))
ntech = lambda p, t: sum(1 for x in X[p] if x <= t)
LEAD = {r['player']: r['leader'] for r in rd('players.csv')}
WARS = rd('wars.csv'); BAT = rd('battles.csv'); Y = rd('cities_war.csv'); DEALS = rd('deals.csv')


def wars():
    decl = [(int(r['turn']), r['b']) for r in WARS if r['kind'] == 'war' and r['a'] == H]
    print('| Declared | Target | Peace | Turns | Target cities / power / techs the turn before | Human power / techs |'
          ' Battles (human attacks won/all, AI attacks won/all) | Cities taken (pop) | Razed | Peace terms to the human |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for t, b in decl:
        peace = next((int(r['turn']) for r in WARS if r['kind'] == 'peace' and {r['a'], r['b']} == {H, b} and int(r['turn']) >= t), None)
        end = peace if peace is not None else 10 ** 6
        e = E.get((t - 1, b)); h = E.get((t - 1, H))
        bs = [x for x in BAT if t <= int(x['turn']) <= end and {x['att'], x['def']} == {H, b}]
        ha = [x for x in bs if x['att'] == H]; aa = [x for x in bs if x['att'] == b]
        cap = [x for x in WARS if x['kind'] == 'captured' and x['a'] == b and x['b'] == H and t <= int(x['turn']) <= end]
        rz = [x for x in WARS if x['kind'] == 'razed' and x['a'] == b and x['b'] == H and t <= int(x['turn']) <= end]
        terms = [f"{d['item']} {d['value']}" for d in DEALS if peace is not None and int(d['turn']) == peace and d['giver'] == b
                 and d['taker'] == H and d['item'] not in ('peace_treaty',)]
        print(f"| {t} | {b} {LEAD[b]} | {peace if peace is not None else 'open at save'} | {(peace if peace else 284) - t} | "
              f"{e['cities']} / {e['power']} / {ntech(b, t - 1)} | {h['power']} / {ntech(H, t - 1)} | "
              f"{sum(1 for x in ha if x['result'] == 'attacker')}/{len(ha)}, {sum(1 for x in aa if x['result'] == 'attacker')}/{len(aa)} | "
              f"{', '.join(f'{x[chr(116)+chr(117)+chr(114)+chr(110)]}: {x[chr(120)]},{x[chr(121)]} ({x[chr(112)+chr(111)+chr(112)]})' for x in cap) or '-'} | "
              f"{len(rz)} | {', '.join(terms) or '-'} |")


def cities():
    # The defending city on the turn of each capture by the human, from the Y lines of that turn or the turn before.
    print('| Captured | Owner | Plot | Pop | Defenders (best) | Defence % | Danger | Foreign land units within 2 | Y line turn |')
    print('|---|---|---|---|---|---|---|---|---|')
    for k in [x for x in WARS if x['kind'] == 'captured' and x['b'] == H]:
        t = int(k['turn'])
        ys = [y for y in Y if y['owner'] == k['a'] and (y['x'], y['y']) == (k['x'], k['y']) and int(y['turn']) <= t]
        y = max(ys, key=lambda y: int(y['turn'])) if ys else None
        print(f"| {t} | {k['a']} {LEAD[k['a']]} | {k['x']},{k['y']} | {k['pop']} | "
              + (f"{y['defenders']} ({y['best_defender']}) | {y['defence_pct']} | {y['danger']} | {y['foreign_units']} | {y['turn']} |" if y else 'no Y line | | | | |'))


def econ():
    print('| Turn | Cities | Pop | Hammers | Commerce | Research | Slider | Gold | Gold/turn | Military units | Power | Golden age |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for t in (50, 87, 100, 150, 200, 206, 228, 229, 243, 250, 267, 270, 284):
        r = E[(t, H)]
        print(f"| {t} | {r['cities']} | {r['pop']} | {r['hammers']} | {r['commerce']} | {r['research']} | {r['research_slider']} | "
              f"{r['gold']} | {r['gold_rate']} | {r['military']} | {r['power']} | {r['golden_age_turns']} |")


for s in (sys.argv[1:] or ['econ', 'wars', 'cities']):
    print(f'\n### {s}\n'); globals()[s]()
