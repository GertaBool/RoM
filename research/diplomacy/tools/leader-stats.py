#!/usr/bin/env python3
"""Parse RoM leaderhead XML (core + loaded Custom Leaderheads modules) and report
per-field statistics, correlations and copy-paste detection. Read-only."""
import glob, os, re, sys, statistics, itertools, json
import xml.etree.ElementTree as ET

ROOT = sys.argv[1] if len(sys.argv) > 1 else "Assets"  # the mod's Assets folder
FILES = [os.path.join(ROOT, "XML/Civilizations/CIV4LeaderHeadInfos.xml")] + sorted(
    glob.glob(os.path.join(ROOT, "Modules/Custom Leaderheads/*/*LeaderHeadInfos.xml")))

ATT = ["ATTITUDE_FURIOUS", "ATTITUDE_ANNOYED", "ATTITUDE_CAUTIOUS", "ATTITUDE_PLEASED", "ATTITUDE_FRIENDLY"]

def strip_ns(tree):
    for el in tree.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]

def parse_leader(el, src):
    d = {"_src": os.path.relpath(src, ROOT)}
    for ch in el:
        tag = ch.tag
        if tag.startswith("i") and (ch.text or "").strip().lstrip("-").isdigit():
            d[tag] = int(ch.text.strip())
        elif tag.endswith("AttitudeThreshold"):
            d[tag] = ATT.index(ch.text.strip()) if ch.text and ch.text.strip() in ATT else -1
        elif tag in ("FavoriteCivic", "FavoriteReligion", "Type"):
            d[tag] = (ch.text or "").strip()
        elif tag == "Flavors":
            for f in ch:
                d["Flavor:" + f.findtext("FlavorType").strip()] = int(f.findtext("iFlavor"))
        elif tag == "ContactRands":
            for f in ch:
                d["ContactRand:" + f.findtext("ContactType").strip()] = int(f.findtext("iContactRand"))
        elif tag == "ContactDelays":
            for f in ch:
                d["ContactDelay:" + f.findtext("ContactType").strip()] = int(f.findtext("iContactDelay"))
        elif tag == "MemoryDecays":
            for f in ch:
                d["MemoryDecay:" + f.findtext("MemoryType").strip()] = int(f.findtext("iMemoryRand"))
        elif tag == "MemoryAttitudePercents":
            for f in ch:
                d["MemoryAtt:" + f.findtext("MemoryType").strip()] = int(f.findtext("iMemoryAttitudePercent"))
        elif tag == "NoWarAttitudeProbs":
            for f in ch:
                d["NoWarProb:" + f.findtext("AttitudeType").strip()] = int(f.findtext("iNoWarProb"))
        elif tag == "UnitAIWeightModifiers":
            for f in ch:
                d["UnitAIWeight:" + f.findtext("UnitAIType").strip()] = int(f.findtext("iWeightModifier"))
        elif tag == "ImprovementWeightModifiers":
            for f in ch:
                d["ImprovementWeight:" + f.findtext("ImprovementType").strip()] = int(f.findtext("iWeightModifier"))
        elif tag == "Traits":
            d["Traits"] = sorted(t.findtext("TraitType").strip() for t in ch if (t.findtext("bTrait") or "0").strip() == "1")
    return d

leaders = []
for f in FILES:
    t = ET.parse(f)
    strip_ns(t)
    for el in t.getroot().iter("LeaderHeadInfo"):
        leaders.append(parse_leader(el, f))

all_leaders = leaders
leaders = [l for l in leaders if l["Type"] != "LEADER_BARBARIAN"]
print(f"files: {len(FILES)}; LeaderHeadInfo entries: {len(all_leaders)}; non-barbarian: {len(leaders)}")
print("core:", sum(1 for l in leaders if l['_src'].startswith('XML')), " modules:", sum(1 for l in leaders if not l['_src'].startswith('XML')))

# Array-valued fields default to 0 when absent (SetVariableListTagPair init); scalars default 0 too.
keys = set()
for l in leaders:
    keys |= {k for k, v in l.items() if isinstance(v, int)}
keys = sorted(keys)

def val(l, k):
    return l.get(k, 0)

rows = []
for k in keys:
    vs = [val(l, k) for l in leaders]
    present = sum(1 for l in leaders if k in l)
    rows.append((k, present, min(vs), max(vs), statistics.mean(vs), statistics.pstdev(vs), len(set(vs))))

print("\n## Per-field stats (absent => 0, as the DLL loads it)")
print(f"{'field':55s} {'present':>7s} {'min':>6s} {'max':>6s} {'mean':>8s} {'sd':>8s} {'nDist':>5s}")
for r in rows:
    print(f"{r[0]:55s} {r[1]:7d} {r[2]:6d} {r[3]:6d} {r[4]:8.2f} {r[5]:8.2f} {r[6]:5d}")

# Distribution details for key fields
def hist(k):
    from collections import Counter
    c = Counter(val(l, k) for l in leaders)
    return dict(sorted(c.items()))

KEY = ["iCultureVictoryWeight", "iSpaceVictoryWeight", "iConquestVictoryWeight", "iDominationVictoryWeight",
       "iDiplomacyVictoryWeight", "iMaxWarRand", "iLimitedWarRand", "iDogpileWarRand", "iMakePeaceRand",
       "iBasePeaceWeight", "iPeaceWeightRand", "iBuildUnitProb", "iRazeCityProb", "iWarmongerRespect",
       "iBaseAttitude", "iEspionageWeight", "iWonderConstructRand", "iDeclareWarTradeRand",
       "iMaxWarNearbyPowerRatio", "iMaxWarDistantPowerRatio", "iMaxWarMinAdjacentLandPercent",
       "iLimitedWarPowerRatio", "iFreedomAppreciation", "iVassalPowerModifier",
       "iTechTradeKnownPercent", "iNoTechTradeThreshold", "iRefuseToTalkWarThreshold",
       "iBaseAttackOddsChange", "iAttackOddsChangeRand", "iDemandRebukedSneakProb", "iDemandRebukedWarProb",
       "iMaxGoldTradePercent", "iMaxGoldPerTurnTradePercent",
       "NoWarProb:ATTITUDE_ANNOYED", "NoWarProb:ATTITUDE_CAUTIOUS", "NoWarProb:ATTITUDE_PLEASED", "NoWarProb:ATTITUDE_FRIENDLY",
       "ContactRand:CONTACT_TRADE_TECH", "ContactRand:CONTACT_DEMAND_TRIBUTE", "ContactRand:CONTACT_OPEN_BORDERS"]
print("\n## Histograms (value: count)")
for k in KEY:
    print(f"{k}: {hist(k)}")

thr = [k for k in keys if k.endswith("AttitudeThreshold")]
print("\n## Attitude thresholds histograms (0=FURIOUS..4=FRIENDLY, -1 none)")
for k in thr:
    print(f"{k}: {hist(k)}")

flav = [k for k in keys if k.startswith("Flavor:")]
print("\n## Flavors")
for k in flav:
    print(f"{k}: {hist(k)}")
mass = [sum(val(l, k) for k in flav) for l in leaders]
print("flavor L1 mass: min %d max %d mean %.2f distinct %s" % (min(mass), max(mass), statistics.mean(mass), sorted(set(mass))))
nflav = [sum(1 for k in flav if val(l, k) > 0) for l in leaders]
from collections import Counter
print("number of nonzero flavors per leader:", dict(sorted(Counter(nflav).items())))

# Victory weight sum
vw = ["iCultureVictoryWeight", "iSpaceVictoryWeight", "iConquestVictoryWeight", "iDominationVictoryWeight", "iDiplomacyVictoryWeight"]
sums = [sum(val(l, k) for k in vw) for l in leaders]
print("\nvictory weight sum per leader: min %d max %d mean %.1f" % (min(sums), max(sums), statistics.mean(sums)))
print("leaders with all victory weights 0:", [l['Type'] for l in leaders if sum(val(l, k) for k in vw) == 0])
print("leaders with any victory weight >= 100 (auto-on at stage 1):", [(l['Type'], {k[1:-13]: val(l, k) for k in vw if val(l, k) >= 100}) for l in leaders if any(val(l, k) >= 100 for k in vw)])
print("leaders with any negative victory weight:", [(l['Type'], {k[1:-13]: val(l, k) for k in vw if val(l, k) < 0}) for l in leaders if any(val(l, k) < 0 for k in vw)])

# Probability that each victory stage-1 flag is set, given BBAI's iNonsense%100 (single uniform r in 0..99,
# victory roll = (r + offset) % 100; no ALWAYS_PEACE / AGGRESSIVE_AI). Culture needs >=100, space >=100 etc.
OFF = {"iCultureVictoryWeight": 10, "iSpaceVictoryWeight": 50, "iConquestVictoryWeight": 30,
       "iDominationVictoryWeight": 70, "iDiplomacyVictoryWeight": 90}
def pon(w):
    return max(0, min(100, w))  # P(w + U[0,99] >= 100) = w/100 for 0<=w<=100
print("\n## Expected share of leaders with each victory stage-1 flag (mean of w/100, clipped)")
for k in vw:
    print(f"{k}: mean P = {statistics.mean(pon(val(l,k)) for l in leaders):.1f}%")
# joint distribution over r for whole roster
cnt = Counter()
for l in leaders:
    for r in range(100):
        on = tuple(k[1:-15] for k in vw if val(l, k) + (r + OFF[k]) % 100 >= 100)
        cnt[len(on)] += 1
tot = sum(cnt.values())
print("number of victory stage-1 flags simultaneously on (roster x 100 rolls):", {k: f"{100*v/tot:.1f}%" for k, v in sorted(cnt.items())})

# Correlations
def pearson(a, b):
    ma, mb = statistics.mean(a), statistics.mean(b)
    sa = sum((x - ma) ** 2 for x in a) ** .5
    sb = sum((y - mb) ** 2 for y in b) ** .5
    if sa == 0 or sb == 0:
        return float('nan')
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)

CORR = ["iMaxWarRand", "iLimitedWarRand", "iDogpileWarRand", "iMakePeaceRand", "iBasePeaceWeight", "iBuildUnitProb",
        "iRazeCityProb", "iWarmongerRespect", "iConquestVictoryWeight", "iDominationVictoryWeight",
        "iCultureVictoryWeight", "iSpaceVictoryWeight", "iDiplomacyVictoryWeight", "Flavor:FLAVOR_MILITARY",
        "Flavor:FLAVOR_CULTURE", "Flavor:FLAVOR_SCIENCE", "iEspionageWeight", "iWonderConstructRand", "iBaseAttitude",
        "NoWarProb:ATTITUDE_CAUTIOUS", "NoWarProb:ATTITUDE_PLEASED"]
print("\n## Pearson correlation matrix (selected)")
short = {k: re.sub(r'^(i|Flavor:FLAVOR_|NoWarProb:ATTITUDE_)', '', k)[:10] for k in CORR}
print(" " * 12 + " ".join(f"{short[k]:>10s}" for k in CORR))
data = {k: [val(l, k) for l in leaders] for k in CORR}
for a in CORR:
    print(f"{short[a]:>12s}" + " ".join(f"{pearson(data[a], data[b]):10.2f}" for b in CORR))

print("\n## Strongest |r| pairs among all scalar/array fields with >2 distinct values")
cands = [k for k in keys if len(set(val(l, k) for l in leaders)) > 2]
pairs = []
for a, b in itertools.combinations(cands, 2):
    r = pearson([val(l, a) for l in leaders], [val(l, b) for l in leaders])
    if r == r:
        pairs.append((abs(r), r, a, b))
pairs.sort(reverse=True)
for p in pairs[:40]:
    print(f"{p[1]:+.2f}  {p[2]}  ~  {p[3]}")

# Copy-paste detection: fingerprint of all non-flavor/non-trait/non-favorite numeric fields
print("\n## Copy-paste detection")
FP_EXCL = lambda k: k.startswith("Flavor:") or k.startswith("UnitAIWeight:") or k.startswith("ImprovementWeight:")
fpkeys = [k for k in keys if not FP_EXCL(k)]
groups = {}
for l in leaders:
    fp = tuple(val(l, k) for k in fpkeys)
    groups.setdefault(fp, []).append(l['Type'])
dups = [g for g in groups.values() if len(g) > 1]
print("identical full numeric profiles (excluding flavors/unitAI/improvement weights):", dups)
# array blocks identical across leaders
for prefix in ["ContactRand:", "ContactDelay:", "MemoryDecay:", "MemoryAtt:", "NoWarProb:"]:
    ks = [k for k in keys if k.startswith(prefix)]
    g = Counter(tuple(val(l, k) for k in ks) for l in leaders)
    print(f"{prefix:14s} distinct blocks: {len(g):3d}; largest identical group: {g.most_common(1)[0][1]}")
# attitude block
ks = [k for k in keys if 'Attitude' in k and k.startswith('i')]
g = Counter(tuple(val(l, k) for k in ks) for l in leaders)
print(f"attitude scalar block distinct: {len(g)}; largest identical group {g.most_common(1)[0][1]}")
# near duplicates: number of differing fields
print("\nnearest-neighbour count of differing numeric fields (excluding flavors/unitAI/improvement):")
nn = []
for a in leaders:
    best = None
    for b in leaders:
        if a is b: continue
        d = sum(1 for k in fpkeys if val(a, k) != val(b, k))
        if best is None or d < best[0]:
            best = (d, b['Type'])
    nn.append((best[0], a['Type'], best[1]))
nn.sort()
for x in nn[:25]:
    print(f"  {x[1]:28s} closest {x[2]:28s} differs in {x[0]} of {len(fpkeys)} fields")

# Module leaders vs core: fields missing
print("\n## Fields absent from module leaders (=> 0 at load)")
core_keys = set().union(*[set(k for k, v in l.items() if isinstance(v, int)) for l in leaders if l['_src'].startswith('XML')])
for l in leaders:
    if not l['_src'].startswith('XML'):
        miss = sorted(k for k in core_keys if k not in l and not k.startswith(('UnitAIWeight:', 'ImprovementWeight:', 'Flavor:')))
        if miss:
            print(f"  {l['Type']}: {len(miss)} missing: {miss[:12]}{'...' if len(miss) > 12 else ''}")

print("\n## Favourite civic / religion")
print("FavoriteCivic:", dict(Counter(l.get('FavoriteCivic', '') for l in leaders).most_common()))
print("FavoriteReligion:", dict(Counter(l.get('FavoriteReligion', '') for l in leaders).most_common()))
print("\n## UnitAI / Improvement weight modifiers in use")
for k in keys:
    if k.startswith("UnitAIWeight:") or k.startswith("ImprovementWeight:"):
        print(k, {l['Type']: val(l, k) for l in leaders if val(l, k) != 0})

# dump table
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "leaders.json"), "w") as fh:
    json.dump(leaders, fh, indent=1)
