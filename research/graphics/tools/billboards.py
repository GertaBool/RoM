"""City billboard rebuilds from CvGameTextMgr_buildCityBillboardString.log (RoM's debug logging,
written only with LoggingEnabled = 1): how often, how bunched, how often the same city again.
usage: billboards.py <billboard log> <out.json>"""
import collections, json, re, sys
per = collections.Counter(); cities = collections.Counter(); last = {}; again = 0; n = 0; lines = 0; first = None
for l in open(sys.argv[1], encoding='latin-1'):
    lines += 1
    m = re.match(r'\[(\d+\.\d+)\] === City (.*) religion icons ===', l)
    if not m: continue
    t = float(m.group(1)); c = m.group(2); n += 1; first = first if first is not None else t
    per[int(t)] += 1; cities[c] += 1
    if c in last and t - last[c] < 0.2: again += 1
    last[c] = t
burst = [s for s, k in per.items() if k >= 100]
out = dict(rebuilds=n, log_lines=lines, distinct_cities=len(cities), first_s=first, last_s=t, span_s=round(t - first),
           seconds_with_rebuilds=len(per), burst_seconds_ge100=len(burst), rebuilds_in_bursts=sum(per[s] for s in burst),
           max_per_second=max(per.values()), same_city_within_0_2s=again,
           most_rebuilt=cities.most_common(3))
json.dump(out, open(sys.argv[2], 'w'), indent=1); print(json.dumps(out, indent=1))
