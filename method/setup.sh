#!/bin/sh
# Enable the method in this clone; safe to run again. Run by the SessionStart hook in
# .claude/settings.json, or by hand after a fresh clone: sh method/setup.sh
# Needs only git and python3. The analysis toolkit (toolchain/analysis/setup.sh) is separate:
# check_all.py uses it to reproduce registries where their inputs exist on the machine.
set -e
root=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
command -v python3 >/dev/null 2>&1 || { echo "method: python3 not found" >&2; exit 1; }
git -C "$root" config core.hooksPath method/hooks
python3 "$root/method/stats.py" >/dev/null
python3 "$root/method/ledger.py" --selftest >/dev/null
python3 "$root/method/ledger.py" check >&2 || { echo "method: ledger check failed (see above)" >&2; exit 1; }
echo "method: enabled (git hooks in method/hooks; gate self-test and check passed)" >&2
