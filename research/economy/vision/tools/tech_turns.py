#!/usr/bin/env python3
"""The earliest turn at which each player of the 30 games could have known Pottery and Fermentation: the first turn
its tech count exceeds its count at turn 0 by the fewest techs it still lacked (its civilization's free techs known,
CIV4CivilizationInfos.xml). A lower bound: telemetry counts techs, it does not name them. Also each game's highest
tech count at its last turn against the fewest techs Refrigeration needs. Writes data/tech_turns.json.
usage: tech_turns.py <mod checkout> <out dir> <run dir>..."""
import json, os, re, sys
import xml.etree.ElementTree as ET

MOD, OUT, RUNS = sys.argv[1], sys.argv[2], sys.argv[3:]
A = os.path.join(MOD, 'Assets', 'XML')


def records(path, tag):
    txt = re.sub(r'\sxmlns="[^"]+"', '', open(path, encoding='latin-1').read(), count=1)
    return ET.fromstring(txt.encode('latin-1')).iter(tag)


T = {}
for r in records(os.path.join(A, 'Technologies', 'CIV4TechInfos.xml'), 'TechInfo'):
    T[r.findtext('Type')] = ([e.text for e in r.findall('AndPreReqs/PrereqTech')], [e.text for e in r.findall('OrPreReqs/PrereqTech')])
FREE = {}
for r in records(os.path.join(A, 'Civilizations', 'CIV4CivilizationInfos.xml'), 'CivilizationInfo'):
    FREE[r.findtext('Type')] = {e.findtext('TechType') for e in r.findall('FreeTechs/FreeTech') if e.findtext('bFreeTech') == '1'}


def lacking(t, known, memo):
    if t in known: return frozenset()
    if t in memo: return memo[t]
    s = {t}
    a, o = T[t]
    for p in a: s |= lacking(p, known, memo)
    if o: s |= min((lacking(p, known, memo) for p in o), key=lambda x: (len(x), sorted(x)))
    memo[t] = frozenset(s)
    return memo[t]


out = []
for d in sorted(RUNS):
    hdr, rows = None, []
    for l in open(os.path.join(d, 'run.jsonl')):
        if l.startswith('{"hdr"'): hdr = json.loads(l)
        elif l.startswith('{"t"'): rows.append(json.loads(l))
    seed = int(os.path.basename(d.rstrip('/'))[1:])
    pl = {}
    for p in hdr['players']:
        known = FREE[p['civ']]
        need = {x: len(lacking(x, known, {})) for x in ('TECH_POTTERY', 'TECH_FERMENTATION', 'TECH_REFRIGERATION')}
        cnt = [next((q['techs'] for q in r['p'] if q['id'] == p['id']), None) for r in rows]
        c0 = cnt[0]
        first = {x: next((t for t, c in enumerate(cnt) if c is not None and c - c0 >= n), None) for x, n in need.items()}
        pl[p['id']] = dict(civ=p['civ'], free=sorted(known), start=c0, need=need, earliest=first, last=cnt[-1])
    out.append(dict(seed=seed, players=pl, turns=len(rows), years=[rows[0]['y'], rows[-1]['y']]))
json.dump(out, open(os.path.join(OUT, 'tech_turns.json'), 'w'), indent=1)
import statistics as st
for x in ('TECH_POTTERY', 'TECH_FERMENTATION', 'TECH_REFRIGERATION'):
    v = [p['earliest'][x] for g in out for p in g['players'].values()]
    got = [e for e in v if e is not None]
    print(x, 'players', len(v), 'reachable by the end', len(got), 'median earliest', st.median(got) if got else None, 'range', (min(got), max(got)) if got else None)
print('free techs', {c: sorted(f) for c, f in FREE.items() if c in {p['civ'] for g in out for p in g['players'].values()}})
