"""Summary of the graphics-paging runs: per seed pair (arm a paging on, b off) the game state at the
end, the telemetry without timings, the graphics lines, and the turn time.
usage: paging_summary.py <exp dir> <out.json>"""
import json, os, re, sys, filecmp, statistics as st
E, OUT = sys.argv[1], sys.argv[2]
G = re.compile(r'graphics turn (\d+): entities created (\d+), set up now (\d+), max (\d+), mean ([\d.]+); setup calls (\d+); visual calls (\d+), on entities not set up (\d+); missions (\d+)')
def runinfo(d):
    log = open(os.path.join(d, 'run.log'), errors='replace').read()
    g = [m.groups() for m in G.finditer(log)]
    lines = [json.loads(l) for l in open(os.path.join(d, 'run.jsonl')) if l.startswith('{"t"')]
    tele = [{k: v for k, v in x.items() if k != 'ms'} for x in lines]
    return dict(completed='RESULT save' in log, seconds=sum(x.get('ms', 0) for x in lines) / 1000.0,
                last=[int(v) for v in g[-1][1:4]] + [float(g[-1][4])] + [int(v) for v in g[-1][5:]] if g else None,
                setup_now=[int(x[2]) for x in g], tele=tele)
done = set(tuple(l.split()[:3]) for l in open(os.path.join(E, 'done.txt')))
out = {}
for P in sorted(os.listdir(E)):
    if not P.startswith('P'): continue
    rows = []
    for s in sorted(os.listdir(os.path.join(E, P, 'a'))):
        da, db = os.path.join(E, P, 'a', s), os.path.join(E, P, 'b', s)
        if (P, 'a', s[1:]) not in done or (P, 'b', s[1:]) not in done: continue
        a, b = runinfo(da), runinfo(db)
        same_state = filecmp.cmp(os.path.join(da, 'run.jsonl.state1.json'), os.path.join(db, 'run.jsonl.state1.json'), shallow=False) if os.path.exists(os.path.join(da, 'run.jsonl.state1.json')) and os.path.exists(os.path.join(db, 'run.jsonl.state1.json')) else False
        rows.append(dict(seed=s, a_completed=a['completed'], b_completed=b['completed'], same_state=same_state,
                         same_telemetry=a['tele'] == b['tele'], a_seconds=a['seconds'], b_seconds=b['seconds'],
                         a_last=a['last'], b_last=b['last'], a_setup_now=a['setup_now'], b_setup_now=b['setup_now'],
                         bare_equal=(a['last'] or [0]*9)[6] == (b['last'] or [0]*9)[6]))
    out[P] = rows
json.dump(out, open(OUT, 'w'), indent=1)
for P, rows in out.items():
    n = len(rows)
    print(P, 'pairs', n, 'completed a/b', sum(r['a_completed'] for r in rows), sum(r['b_completed'] for r in rows),
          'same state', sum(r['same_state'] for r in rows), 'same telemetry', sum(r['same_telemetry'] for r in rows),
          'bare visual equal', sum(r['bare_equal'] for r in rows))
    if n:
        print('  seconds a median %.1f b median %.1f' % (st.median(r['a_seconds'] for r in rows), st.median(r['b_seconds'] for r in rows)))
        print('  set up at last turn a mean %.0f b mean %.0f; mean over samples a %.0f b %.0f' % (
            st.mean(r['a_last'][1] for r in rows), st.mean(r['b_last'][1] for r in rows),
            st.mean(r['a_last'][3] for r in rows), st.mean(r['b_last'][3] for r in rows)))
