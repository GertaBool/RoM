#!/usr/bin/env python3
"""Trades in harness runs (run.jsonl of harness.exe save): the deals standing at the first turn, and
the trades agreed in the turns after it, by kind. Item codes are the DLL's TradeableItems.
usage: trades.py <run dir>... > trades.json"""
import collections, json, os, sys
NAMES = ['gold', 'gold per turn', 'map', 'vassal', 'surrender', 'open borders', 'defensive pact',
         'permanent alliance', 'peace treaty', 'tech', 'resource', 'city', 'peace', 'war', 'embargo', 'civic', 'religion']
def kind(items):
    return '+'.join(sorted(NAMES[i[0]] for i in items)) or 'nothing'
def shape(a, b):
    x, y = sorted([kind(a), kind(b)])
    return f'{x} / {y}'
standing, agreed, runs, turns = collections.Counter(), collections.Counter(), 0, 0
gold_for_tech = []
for d in sys.argv[1:]:
    lines = [json.loads(l) for l in open(os.path.join(d, 'run.jsonl')) if l.startswith('{"t"')]
    if not lines: continue
    runs += 1; turns += len(lines) - 1
    for e in lines[0].get('ev') or []:
        if 'deal' in e: standing[shape(e['ai'], e['bi'])] += 1
    for t in lines[1:]:
        for e in t.get('ev') or []:
            if 'trade' in e:
                agreed[shape(e['ai'], e['bi'])] += 1
                for x, y in ((e['ai'], e['bi']), (e['bi'], e['ai'])):
                    if kind(x) == 'tech' and kind(y) == 'gold': gold_for_tech.append(y[0][1])
json.dump(dict(runs=runs, turns_after_first=turns, standing_at_first_turn=standing.most_common(),
               agreed_after_first_turn=agreed.most_common(), gold_paid_for_one_tech=sorted(gold_for_tech)), sys.stdout, indent=1)
print()
