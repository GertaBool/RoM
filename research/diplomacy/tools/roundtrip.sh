#!/bin/bash
# Save/reload determinism: play to turn T+N with a snapshot at T, reload the
# snapshot, play N turns, compare the telemetry turn by turn.
# usage: roundtrip.sh <root> <build> <scn name> <speed> <seed> <T> <N>
# WORK: harness work dir with b-* builds and scn/ (converted WorldBuilder scenarios); MOD: the mod checkout; HARNESS: toolchain/harness
S=${WORK:?set WORK}; MOD=${MOD:?set MOD}; HARNESS=${HARNESS:-$(cd "$(dirname "$0")/../../../toolchain/harness" && pwd)}
root=$1; build=$2; scn=$3; speed=$4; seed=$5; T=$6; N=$7
source "$HARNESS/env.sh"
mkdir -p "$root"
"$HARNESS/mkroot.sh" "$root" "$build" "$MOD" >/dev/null
cp "$S/scn/$scn" "$root/map.scn"
cd "$root" && rm -f run.jsonl* reload.jsonl*
HARNESS_SNAPSHOT=$T timeout 20000 wine harness.exe scenario map.scn $speed HANDICAP_NOBLE $seed $((T + N)) run.jsonl 1 > run.log 2>&1
timeout 20000 wine harness.exe save run.jsonl.t$T.init run.jsonl.t$T.game $N reload.jsonl 1 > reload.log 2>&1
python3 - "$root" $T <<'PYEOF'
import json, sys
root, T = sys.argv[1], int(sys.argv[2])
def load(p):
    out = {}
    for l in open(p):
        try: r = json.loads(l)
        except ValueError: continue
        if 't' in r and 'p' in r:
            r.pop('ms', None)
            if r['t'] == T: r.pop('ev', None)
            out[r['t']] = r
    return out
a, b = load(root + '/run.jsonl'), load(root + '/reload.jsonl')
common = sorted(set(a) & set(b))
first = next((t for t in common if a[t] != b[t]), None)
if first is None:
    print('%s: identical for turns %d-%d' % (root, common[0], common[-1]))
else:
    pa = {p['id']: p for p in a[first]['p']}; pb = {p['id']: p for p in b[first]['p']}
    d = [(i, {k: (pa[i][k], pb[i].get(k)) for k in pa[i] if pa[i][k] != pb[i].get(k)}) for i in pa]
    d = [x for x in d if x[1]]
    print('%s: first difference at turn %d (of %d-%d): %s' % (root, first, common[0], common[-1], str(d[:2])[:600]))
PYEOF
