"""Check a batch of connector edits against the branch: replays the first N (old, new) pairs of a pairs file on the
files at a base commit and compares the result with the files at the fetched branch head, byte for byte.
usage: verify.py <mod checkout> <pairs.json> <base commit> <N> [branch]   (default branch claude/settlement-economy)
The checkout's origin is the GitLab project; the script fetches the branch first."""
import json, subprocess, sys

mod, pairs_path, base, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
branch = sys.argv[5] if len(sys.argv) > 5 else 'claude/settlement-economy'
subprocess.run(['git', '-C', mod, 'fetch', '-q', 'origin', branch], check=True)
show = lambda rev, f: subprocess.run(['git', '-C', mod, 'show', '%s:%s' % (rev, f)], capture_output=True, check=True).stdout
state = {}
for p in json.load(open(pairs_path))[:n]:
    f = p['file']
    if f not in state: state[f] = show(base, f).decode('latin-1')
    assert state[f].count(p['old']) == 1, (f, p['old'][:80])
    state[f] = state[f].replace(p['old'], p['new'])
bad = 0
for f, s in state.items():
    same = show('FETCH_HEAD', f) == s.encode('latin-1')
    bad += not same
    print(f, 'identical' if same else 'DIFFERS')
sys.exit(1 if bad else 0)
