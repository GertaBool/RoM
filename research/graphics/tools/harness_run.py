"""Memory and turn time of a headless harness run (the DLL without graphics) from its log and a
memory sample file of lines '<unix time> <vsz KB> <rss KB> <turns done>'.
usage: harness_run.py <run.log> <mem.txt> <out.json>"""
import json, re, sys
turns = [(int(m.group(1)), int(m.group(2))) for m in re.finditer(r'^turn (\d+) \((\d+) ms', open(sys.argv[1]).read(), re.M)]
mem = [l.split() for l in open(sys.argv[2]) if len(l.split()) == 4 and l.split()[0].isdigit() and int(l.split()[1]) > 500000]
rss = [int(x[2]) for x in mem]
played = [ms for t, ms in turns if ms > 0]
out = dict(first_turn=turns[0][0], last_turn=turns[-1][0], turns_played=len(played), mean_turn_s=round(sum(played) / len(played) / 1000, 1),
           max_turn_s=round(max(played) / 1000, 1), rss_MB_first=round(rss[0] / 1024, 1), rss_MB_last=round(rss[-1] / 1024, 1),
           rss_MB_max=round(max(rss) / 1024, 1), samples=len(rss))
json.dump(out, open(sys.argv[3], 'w'), indent=1); print(out)
