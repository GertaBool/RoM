#!/bin/bash
# Rebuild the code map from a checkout of the DLL repository (GitLab rise-of-mankind).
# usage: build.sh <rise-of-mankind checkout> <base game Python dir>
# Needs: BTS_SDK_DIR (as for toolchain/clang-gate), clang++ 18 (for the for-scope pass), the analysis
# Python with libclang (toolchain/analysis), universal-ctags, jq. Nothing of the DLL is compiled or run.
# Writes codemap/map/*.tsv and the pages codemap/*.md, codemap/files/*.md.
set -eu
here=$(cd "$(dirname "$0")" && pwd); cm=$(dirname "$here"); gate="$here/../../toolchain/clang-gate"
src=$(cd "$1" && pwd); base=$2
py=${ANALYSIS_PYTHON:-$HOME/.cache/rom-ana/bin/python}
: "${BTS_SDK_DIR:?set BTS_SDK_DIR to the BTS SDK CvGameCoreDLL folder}"
commit=$(git -C "$src" rev-parse --short=12 HEAD)
[ -z "$(git -C "$src" status --porcelain --untracked-files=no -- Assets/CvGameCoreDLL)" ] || commit="$commit (with uncommitted changes)"
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
"$gate/mirror.sh" "$src/Assets/CvGameCoreDLL" "$w/src" > /dev/null
"$gate/forscope-pass.sh" "$w/src" > /dev/null 2>&1
# DllExport as an annotation clang keeps (it ignores __declspec(dllexport) outside Windows targets); same line count
grep -q '^#define DllExport' "$w/src/CvGameCoreDLL.h"
sed -i 's/^#define DllExport.*$/#define DllExport __attribute__((annotate("DllExport")))/' "$w/src/CvGameCoreDLL.h"
mkdir -p "$cm/map"
"$py" -I "$here/extract_cpp.py" "$w/src" "$cm/map"
(cd "$w/src" && find . -maxdepth 1 -type f \( -name '*.cpp' -o -name '*.h' -o -name '*.inl' \) -printf '%f\n' | sort \
   | xargs ctags --output-format=json --fields=+n --c++-kinds=f --language-force=c++ --extras=-q -f - 2>/dev/null) \
  | jq -r 'select(._type=="tag") | [.name, .path, .line] | @tsv' > "$w/ctags.tsv"
python3 -I "$here/extract_py.py" "$cm/map" "$src/Assets/Python" "$base" --config "$src/Assets/Config"
python3 -I "$here/render.py" "$cm" "$commit" "$w/ctags.tsv"
