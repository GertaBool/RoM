#!/bin/sh
# The gate end to end: a scratch clone of this repository with the real git hooks (method/setup.sh),
# and commits that must pass or be refused, each for the reason expected. Run by
# hand after a change to the gate (sh method/tests/e2e_gate.sh); needs git, python3 and the analysis
# toolkit check_all.py uses.
# The clone is removed afterwards; this repository is not touched.
#   1. git commit --only through the hooks leaves the commit and the index clean
#   2. a gated file without "Serves:" is refused
#   3. a method file without "Method:" is refused
#   4. a toy prediction: registering passes, the evidence commit that decides it passes,
#      a code commit serving it afterwards is refused
set -eu
src=$(git rev-parse --show-toplevel)
w=$(mktemp -d)
trap 'rm -rf "$w"' EXIT
git clone -q "$src" "$w/r"
cd "$w/r"
git config user.email e2e@example.invalid
git config user.name e2e
git checkout -q -b e2e-gate
sh method/setup.sh
for f in method/README.md toolchain/harness/README.md research/ai-warfare/study/doctrine.md.in; do
  [ -f "$f" ] || { echo "e2e: $f is missing; this test needs updating"; exit 1; }
done

fail() { echo "e2e FAIL: $1"; cat "$w/out"; exit 1; }
passes() {  # label, commit arguments...
  label=$1; shift
  head=$(git rev-parse HEAD)
  git commit -q "$@" > "$w/out" 2>&1 || fail "$label: refused"
  [ "$(git rev-parse HEAD)" != "$head" ] || fail "$label: no commit made"
  echo "e2e ok: $label"
}
refused() {  # label, expected message, commit arguments...
  label=$1; want=$2; shift 2
  head=$(git rev-parse HEAD)
  if git commit -q "$@" > "$w/out" 2>&1; then fail "$label: passed"; fi
  grep -qF -- "$want" "$w/out" || fail "$label: refused, but not with: $want"
  [ "$(git rev-parse HEAD)" = "$head" ] || fail "$label: HEAD moved"
  git reset -q --hard HEAD
  echo "e2e ok: $label"
}

# 1. commit --only: the hooks run with a temporary index; nothing of their own may enter the commit
echo "e2e" > research/ai-warfare/e2e-only.txt
echo "untracked" > e2e-untracked.txt
git add research/ai-warfare/e2e-only.txt
passes "commit --only" --only research/ai-warfare/e2e-only.txt -m "e2e: commit --only"
[ "$(git diff HEAD^ HEAD --name-only)" = "research/ai-warfare/e2e-only.txt" ] || fail "commit --only: the commit holds other files: $(git diff HEAD^ HEAD --name-only | tr '\n' ' ')"
[ -z "$(git status --porcelain --untracked-files=no)" ] || fail "commit --only: index or tree left dirty: $(git status --porcelain --untracked-files=no)"
rm -f e2e-untracked.txt

# 2. gated path without a Serves trailer
echo "e2e" >> toolchain/harness/README.md
git add toolchain/harness/README.md
refused "gated file without Serves" 'staged gated paths need a "Serves: P.." trailer' -m "e2e: no trailer"

# 3. method path without a Method trailer
echo "e2e" >> method/README.md
git add method/README.md
refused "method file without Method" 'staged method paths need a "Method: <reason>" trailer' -m "e2e: no trailer"

# 4. a toy prediction through registration, deciding evidence, and a code commit after the decision
doc=research/ai-warfare/study/doctrine.md.in
pr=$(sed -n 's/^- \*\*\(D[0-9][0-9]*\)\..*/\1/p' "$doc" | head -1)
gap=$(sed -n 's/^- \*\*\(R[0-9][0-9]*\)\..*/\1/p' "$doc" | head -1)
[ -n "$pr" ] && [ -n "$gap" ] || { echo "e2e: no principle or reading found in $doc"; exit 1; }
python3 - "$pr" "$gap" <<'EOF'
import json, sys
p = 'method/mission/register.json'
r = json.load(open(p))
r += [{"id": "HE2E", "type": "hypothesis", "line": "e2e", "principle": sys.argv[1], "gap": sys.argv[2],
       "text": "end-to-end test of the gate"},
      {"id": "PE2E", "type": "prediction", "line": "e2e", "hypotheses": ["HE2E"], "variable": "completed",
       "evidence": "runs", "change": "end-to-end test of the gate",
       "claim": {"direction": "a>b", "alpha": 0.05, "min_effect": 0.6, "min_n": 30, "seat": 0},
       "paths": ["toolchain/harness/README.md"]}]
open(p, 'w').write(json.dumps(r, indent=1) + '\n')
EOF
git add method/mission/register.json
passes "register a prediction" -m "e2e: register PE2E"
mkdir -p method/mission/evidence/PE2E
i=0
for s in $(python3 method/ledger.py seeds PE2E 30); do
  printf '%s\t%d\n' "$s" $((3 + i % 3)) >> method/mission/evidence/PE2E/a.tsv
  printf '%s\t%d\n' "$s" $((i % 3)) >> method/mission/evidence/PE2E/b.tsv
  i=$((i + 1))
done
printf '\n- End-to-end test of the gate. PE2E: corroborated.\n' >> "$doc"
python3 method/docs.py render "$doc"
git add method/mission/evidence "$doc" "${doc%.in}"
passes "the evidence commit that decides its prediction" -m "e2e: evidence PE2E

Serves: PE2E"
echo "e2e" >> toolchain/harness/README.md
git add toolchain/harness/README.md
refused "code serving a decided prediction" "PE2E is corroborated" -m "e2e: code after the decision

Serves: PE2E"
echo "e2e: all passed"
