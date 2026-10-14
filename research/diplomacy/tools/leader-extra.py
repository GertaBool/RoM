#!/usr/bin/env python3
"""Extra derived analyses on leaders.json produced by leader_stats.py. Read-only."""
import json, os, statistics, itertools, collections, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HERE, "..", "data", "leaders.json")))
ROOT = sys.argv[1] if len(sys.argv) > 1 else "Assets"  # the mod's Assets folder
v = lambda l, k: l.get(k, 0)
keys = sorted({k for l in L for k, x in l.items() if isinstance(x, int)})

print("## Fields constant across all 82 leaders")
const = [k for k in keys if len({v(l, k) for l in L}) == 1]
print(len(const), const)
print("\n## Fields where one value covers >= 90% of leaders (but not all)")
for k in keys:
    c = collections.Counter(v(l, k) for l in L)
    val, n = c.most_common(1)[0]
    if 1 < len(c) and n >= 0.9 * len(L):
        print(f"  {k}: {val} x{n}  others={dict(c)}")

print("\n## Pair diffs for nearest clones")
by = {l['Type']: l for l in L}
for a, b in [("LEADER_FRANCO", "LEADER_JUSTINIAN"), ("LEADER_KANGXI", "LEADER_CATHERINE"),
             ("LEADER_HIROHITO", "LEADER_CHARLEMAGNE"), ("LEADER_JOANOFARC", "LEADER_BRENNUS"),
             ("LEADER_IVAN", "LEADER_MONTEZUMA"), ("LEADER_CETSHWAYO", "LEADER_SHAKA")]:
    d = {k: (v(by[a], k), v(by[b], k)) for k in keys if v(by[a], k) != v(by[b], k)}
    print(f"  {a} vs {b}: {len(d)} diffs: {d}")

# AI-AI first-impression peace-weight attitude: 4 - |pw_a - pw_b|, pw = base + U{0,1,2}
print("\n## AI-AI peace-weight attitude term 4-|pwA-pwB| (pw = iBasePeaceWeight + rand(iPeaceWeightRand))")
terms = []
for a, b in itertools.permutations(L, 2):
    for ra in range(v(a, 'iPeaceWeightRand') or 1):
        for rb in range(v(b, 'iPeaceWeightRand') or 1):
            terms.append(4 - abs(v(a, 'iBasePeaceWeight') + ra - v(b, 'iBasePeaceWeight') - rb))
c = collections.Counter(terms)
print("  min %d max %d mean %.2f" % (min(terms), max(terms), statistics.mean(terms)))
print("  share <= -3 (alone enough for ANNOYED from 0): %.1f%%; share >= 3 (alone PLEASED): %.1f%%" %
      (100 * sum(n for t, n in c.items() if t <= -3) / len(terms), 100 * sum(n for t, n in c.items() if t >= 3) / len(terms)))
wm = [min(v(a, 'iWarmongerRespect'), v(b, 'iWarmongerRespect')) for a, b in itertools.permutations(L, 2)]
print("  warmonger-respect term min(a,b): mean %.2f dist %s" % (statistics.mean(wm), dict(collections.Counter(wm))))

# Victory: stage-1 probability per leader; correlated dice
OFF = {"Culture": 10, "Space": 50, "Conquest": 30, "Domination": 70, "Diplomacy": 90}
print("\n## Victory stage>=1 activation over the 100 equiprobable values of StrategyRand%100 (no game options)")
per = []
for l in L:
    w = {n: v(l, f"i{n}VictoryWeight") for n in OFF}
    on = {n: sum(1 for r in range(100) if w[n] + (r + OFF[n]) % 100 >= 100) for n in OFF}
    none = sum(1 for r in range(100) if all(w[n] + (r + OFF[n]) % 100 < 100 for n in OFF))
    per.append((l['Type'], w, on, none))
nonevals = [p[3] for p in per]
print("  P(no victory inclination at all) per leader: min %d%% max %d%% mean %.1f%%" % (min(nonevals), max(nonevals), statistics.mean(nonevals)))
print("  leaders with >=50%% chance of no inclination:", [(p[0], p[3]) for p in per if p[3] >= 50])
# options
for opt, adj in [("AGGRESSIVE_AI", {"Culture": -20, "Space": -20, "Conquest": 20, "Domination": 20, "Diplomacy": -20}),
                 ("ALWAYS_PEACE", {"Culture": 30, "Space": 30, "Conquest": -999, "Domination": -999, "Diplomacy": 30})]:
    m = {n: statistics.mean(max(0, min(100, v(l, f"i{n}VictoryWeight") + adj[n])) for l in L) for n in OFF}
    print(f"  with {opt}: mean P(stage1) = " + ", ".join(f"{n} {m[n]:.1f}%" for n in OFF))

# Victory-weight vs war-rand: are 'conquest' leaders actually the war-prone ones?
def pearson(a, b):
    ma, mb = statistics.mean(a), statistics.mean(b)
    sa = sum((x - ma) ** 2 for x in a) ** .5; sb = sum((y - mb) ** 2 for y in b) ** .5
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)
pwar = [1 / v(l, 'iMaxWarRand') + (1 - 1 / v(l, 'iMaxWarRand')) / v(l, 'iLimitedWarRand') for l in L]
print("\n## corr(conquest weight, per-turn total+limited war trigger prob) = %.2f" % pearson([v(l, 'iConquestVictoryWeight') for l in L], pwar))
print("## corr(culture weight, flavor culture) = %.2f" % pearson([v(l, 'iCultureVictoryWeight') for l in L], [v(l, 'Flavor:FLAVOR_CULTURE') for l in L]))
print("## corr(space weight, flavor science) = %.2f" % pearson([v(l, 'iSpaceVictoryWeight') for l in L], [v(l, 'Flavor:FLAVOR_SCIENCE') for l in L]))

# War trigger expectations per game speed (threshold 0, unaggressive, no war plans, AIDeclareWarProb 100)
SPEEDS = {"Blitz": 215, "Quick": 352, "Normal": 700, "Epic": 1050, "Marathon": 1470, "Snail": 3000}
print("\n## Expected war-plan dice successes per game if eligible every turn (threshold 0: P=1/rand)")
def p_any(l, t=0):
    T, Li, D = v(l, 'iMaxWarRand'), v(l, 'iLimitedWarRand'), v(l, 'iDogpileWarRand')
    pT = min(1, (t + 1) / T); pL = min(1, 1 / Li); pD = min(1, 1 / D)
    return pT, (1 - pT) * pL, (1 - pT) * (1 - pL) * pD
rows = []
for l in L:
    pT, pL, pD = p_any(l)
    rows.append((l['Type'], pT, pL, pD))
for lab, sel in [("most warlike (min MaxWarRand)", min(rows, key=lambda r: -r[1] - r[2])),
                 ("least warlike", min(rows, key=lambda r: r[1] + r[2])),]:
    print(f"  {lab}: {sel[0]} per-turn total {sel[1]*100:.2f}% limited {sel[2]*100:.2f}% dogpile {sel[3]*100:.2f}%")
mean_p = statistics.mean(r[1] + r[2] + r[3] for r in rows)
print("  roster mean per-turn P(any war dice success) = %.2f%%" % (100 * mean_p))
for s, n in SPEEDS.items():
    print(f"   {s:9s} {n:5d} turns: roster-mean expected successes {mean_p*n:6.1f};"
          f" most-warlike {(max(r[1]+r[2]+r[3] for r in rows))*n:6.1f}; least {(min(r[1]+r[2]+r[3] for r in rows))*n:5.1f}")
mp = [1 / v(l, 'iMakePeaceRand') for l in L]
print("  makePeace per-turn gate P: min %.1f%% max %.1f%% mean %.1f%%" % (100 * min(mp), 100 * max(mp), 100 * statistics.mean(mp)))

# Memory decay half-life (turns) for key memories; per-turn decrement prob 1/rand
print("\n## Memory decay: expected turns per decrement (=rand) vs game length")
for k in sorted(x for x in keys if x.startswith('MemoryDecay:')):
    vals = sorted({v(l, k) for l in L})
    print(f"  {k[12:]}: rand values {vals}")
missing = [k for k in keys if k.startswith('MemoryAtt:') and 'MemoryDecay:' + k[10:] not in keys]
print("  memories with attitude but no decay entry (permanent):", [m[10:] for m in missing])

# Flavor -> tech value sensitivity
def load(path, tag):
    t = ET.parse(path)
    for el in t.iter():
        if '}' in el.tag: el.tag = el.tag.split('}')[1]
    return list(t.getroot().iter(tag))
techs = load(os.path.join(ROOT, 'XML/Technologies/CIV4TechInfos.xml'), 'TechInfo')
FL = ["FLAVOR_MILITARY", "FLAVOR_RELIGION", "FLAVOR_PRODUCTION", "FLAVOR_GOLD", "FLAVOR_SCIENCE", "FLAVOR_CULTURE", "FLAVOR_GROWTH", "FLAVOR_ESPIONAGE"]
tf = [{f.findtext('FlavorType'): int(f.findtext('iFlavor')) for f in t.iter('Flavor')} for t in techs]
def bonus(l, t):
    lf = {f: max(0, v(l, 'Flavor:' + f)) for f in FL}
    mass = sum(lf.values()); dot = sum(lf[f] * max(0, t.get(f, 0)) for f in FL)
    aff = (5 * dot) // mass if dot > 0 and mass > 0 else 0
    return aff * 20 * 35 // 100
allb = [[bonus(l, t) for t in tf] for l in L]
flat = [x for row in allb for x in row]
print("\n## Tech flavor bonus (affinity*20*35/100) added to AI_techValue")
print("  over all leader x tech: min %d max %d mean %.1f" % (min(flat), max(flat), statistics.mean(flat)))
spread = [max(allb[i][j] for i in range(len(L))) - min(allb[i][j] for i in range(len(L))) for j in range(len(tf))]
print("  per-tech spread across leaders (max-min): mean %.1f max %d" % (statistics.mean(spread), max(spread)))
bl = load(os.path.join(ROOT, 'XML/Buildings/CIV4BuildingInfos.xml'), 'BuildingInfo')
bf = [{f.findtext('FlavorType'): int(f.findtext('iFlavor')) for f in b.iter('Flavor')} for b in bl]
bf = [x for x in bf if x]
def baff(l, t):
    lf = {f: max(0, v(l, 'Flavor:' + f)) for f in FL}
    mass = sum(lf.values()); dot = sum(lf[f] * max(0, t.get(f, 0)) for f in FL)
    return (5 * dot) // mass if dot > 0 and mass > 0 else 0
bb = [[baff(l, t) for t in bf] for l in L]
fb = [x for r in bb for x in r]
print("  buildings with flavors (core XML): %d; building affinity added to AI_buildingValue: min %d max %d mean %.1f" % (len(bf), min(fb), max(fb), statistics.mean(fb)))
vals = collections.Counter(x for t in bf for x in t.values())
print("  building flavor magnitudes:", dict(sorted(vals.items())))

print("\n## Strategy-hash flavor thresholds")
print("  FLAVOR_PRODUCTION>=2 (AI_STRATEGY_PRODUCTION):", sum(1 for l in L if v(l, 'Flavor:FLAVOR_PRODUCTION') >= 2), "leaders")
dag = [12000 // max(100, 50 + v(l, 'iMaxWarRand')) for l in L]
print("  dagger personality part 12000/max(100,50+MaxWarRand): values", sorted(set(dag)), "(then *(rand%11)/10; +5*min(8,MIL) ->", sorted({5 * min(8, v(l, 'Flavor:FLAVOR_MILITARY')) for l in L}), ")")
civ = [25000 // max(100, 100 + v(l, 'iMaxWarRand')) for l in L]
print("  civic iWarmongerPercent 25000/max(100,100+MaxWarRand):", dict(sorted(collections.Counter(civ).items())))
bu = [3 + v(l, 'iBuildUnitProb') // 3 for l in L]
print("  city iMaxUnitSpending base 3+BuildUnitProb/3 (non-aggressive):", dict(sorted(collections.Counter(bu).items())))
ao = [(v(l, 'iBaseAttackOddsChange'), v(l, 'iBaseAttackOddsChange') + 2 * (v(l, 'iAttackOddsChangeRand') - 1) / 2) for l in L]
print("  attack-odds optimism: base range %d..%d, mean of base+2*E[rand] = %.1f" % (min(a for a, _ in ao), max(a for a, _ in ao), statistics.mean(b for _, b in ao)))
