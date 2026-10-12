#!/bin/bash
# usage: diffcheck.sh <baseline CvGameCoreDLL dir> <patched CvGameCoreDLL dir> [files...]
# Compiles both trees (MSVC 7.1 for-scope emulated) with bug-finding warnings and
# reports diagnostics present only in the patched tree, keyed by file, message and
# source-line text. Exits non-zero if a new error appears.
# Environment: BTS_SDK_DIR; GATE_WORK (default /tmp/rom-clang-gate).
HERE=$(dirname "$(readlink -f "$0")")
export GATE_WORK=${GATE_WORK:-/tmp/rom-clang-gate}
base=$1; pat=$2; shift 2
W="-Wno-everything -Wuninitialized -Wsometimes-uninitialized -Wconditional-uninitialized -Wself-assign -Wtautological-overlap-compare -Warray-bounds -Wreturn-type -Wunused-value -Wparentheses -Wlogical-op-parentheses -Wint-in-bool-context -Wsizeof-array-argument -Wdangling-else -Wloop-analysis -Wbool-operation -Wpointer-bool-conversion -Wundefined-bool-conversion -Wnull-dereference -Wdivision-by-zero -Winteger-overflow -Wenum-compare -Wliteral-conversion -Wconstant-conversion -Wunused-comparison -Wempty-body -Wformat -Wnon-pod-varargs -Wshadow -Wunused-variable"
for side in base pat; do
  src=$([ $side = base ] && echo "$base" || echo "$pat")
  m=$GATE_WORK/m-$side
  "$HERE/mirror.sh" "$src" "$m" >/dev/null
  "$HERE/forscope-pass.sh" "$m" >/dev/null 2>&1
  mkdir -p "$GATE_WORK/l-$side"; rm -f "$GATE_WORK/l-$side"/*
  files="$@"; [ -z "$files" ] && files=$(cd "$m" && ls *.cpp)
  (cd "$m" && printf '%s\n' $files | xargs -P 8 -I{} sh -c "CASEDIR=$m '$HERE/check.sh' $m {} $W > $GATE_WORK/l-$side/{}.log 2>&1 || true")
done
python3 - <<'PY'
import re, glob, os
work = os.environ['GATE_WORK']
def diags(side):
    out = set()
    for log in glob.glob(f'{work}/l-{side}/*.log'):
        for line in open(log, errors='replace'):
            m = re.match(r'(.+?):(\d+):\d+: (?:fatal )?(error|warning): (.*)', line)
            if not m or m.group(1).startswith('/'):
                continue  # SDK, system and shim headers
            f, ln, kind, msg = m.group(1), int(m.group(2)), m.group(3), m.group(4)
            try: text = open(os.path.join(f'{work}/m-{side}', f), errors='replace').read().split('\n')[ln-1].strip()
            except Exception: text = ''
            out.add((os.path.basename(f), kind, msg, text))
    return out
b, p = diags('base'), diags('pat')
new = sorted(p - b); fixed = sorted(b - p)
nb = sum(1 for d in b if d[1]=='error'); np_ = sum(1 for d in p if d[1]=='error')
print(f'baseline: {nb} errors/{len(b)-nb} warnings; patched: {np_} errors/{len(p)-np_} warnings; new: {len(new)}; resolved: {len(fixed)}')
for e in new: print('NEW  ', e)
for e in fixed: print('GONE ', e)
raise SystemExit(1 if any(d[1]=='error' for d in new) else 0)
PY
