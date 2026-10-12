#!/bin/bash
# usage: diffcheck.sh <baseline-src> <patched-src> [files...]
# Compiles both mirrors (with legacy for-scope emulation) and reports errors/warnings in the patched
# tree whose (file, message, source-line text) is absent in the baseline.
base=$1; pat=$2; shift 2
W="-Wno-everything -Wuninitialized -Wsometimes-uninitialized -Wconditional-uninitialized -Wself-assign -Wtautological-overlap-compare -Warray-bounds -Wreturn-type -Wunused-value -Wparentheses -Wlogical-op-parentheses -Wint-in-bool-context -Wsizeof-array-argument -Wdangling-else -Wloop-analysis -Wbool-operation -Wpointer-bool-conversion -Wundefined-bool-conversion -Wnull-dereference -Wdivision-by-zero -Winteger-overflow -Wenum-compare -Wliteral-conversion -Wconstant-conversion -Wunused-comparison -Wempty-body -Wformat -Wnon-pod-varargs -Wshadow -Wunused-variable"
for side in base pat; do
  src=$([ $side = base ] && echo "$base" || echo "$pat")
  m=/home/user/src/build/m-$side
  /home/user/src/shim/mirror.sh "$src" $m >/dev/null
  /home/user/src/shim/forscope-pass.sh $m >/dev/null 2>&1
  mkdir -p /home/user/src/build/l-$side; rm -f /home/user/src/build/l-$side/*
  files="$@"; [ -z "$files" ] && files=$(cd $m && ls *.cpp)
  (cd $m && printf '%s\n' $files | xargs -P 8 -I{} sh -c "CASEDIR=$m /home/user/src/shim/check.sh $m {} $W > /home/user/src/build/l-$side/{}.log 2>&1 || true")
done
python3 - <<'PY'
import re, glob, os
def diags(side):
    out = set()
    for log in glob.glob(f'/home/user/src/build/l-{side}/*.log'):
        for line in open(log, errors='replace'):
            m = re.match(r'(.+?):(\d+):\d+: (?:fatal )?(error|warning): (.*)', line)
            if not m: continue
            f, ln, kind, msg = m.group(1), int(m.group(2)), m.group(3), m.group(4)
            if f.startswith('/home/user/src/sdk') or f.startswith('/usr') or 'shim' in f: continue
            p = os.path.join(f'/home/user/src/build/m-{side}', f)
            try: text = open(p, errors='replace').read().split('\n')[ln-1].strip()
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
