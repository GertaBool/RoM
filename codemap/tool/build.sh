#!/bin/bash
# Rebuild the code map from a checkout of the DLL repository (GitLab rise-of-mankind).
# usage: build.sh <rise-of-mankind checkout> <base game Python dir> <Python 2.4 dir> [jobs]
#   base game Python dir: the Python folder of Beyond the Sword, which the mod's Python falls back to
#   Python 2.4 dir: the Windows Python 2.4 the game embeds (python.exe), run under Wine to parse the Python
# Needs: VCTOOLKIT_DIR PSDK_DIR BTS_SDK_DIR WINEPREFIX (toolchain/README.md), llvm-readobj-18,
# llvm-undname-18, universal-ctags, jq. Writes codemap/map/*.tsv and the pages codemap/*.md, codemap/files/.
set -eu
here=$(cd "$(dirname "$0")" && pwd); cm=$(dirname "$here")
src=$(cd "$1" && pwd); base=$2; py24=$3; jobs=${4:-4}
export WINEARCH=win32 WINEDEBUG=-all
commit=$(git -C "$src" rev-parse --short=12 HEAD)
[ -z "$(git -C "$src" status --porcelain --untracked-files=no -- Assets/CvGameCoreDLL Assets/Python)" ] \
  || commit="$commit (with uncommitted changes)"
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
winpath() { echo "Z:$(realpath -s "$1" | tr / '\\')"; }

# 1. the DLL: compile every unit with the real compiler, then read the listings and the type records
"$here/compile.sh" "$src/Assets/CvGameCoreDLL" "$w" "$jobs"
rm -rf "$cm/map"; mkdir -p "$cm/map"
python3 -I "$here/extract_asm.py" "$w/out" "$w/b" "$cm/map"
# an independent count of the definitions in the same files, for map/completeness.tsv
(cd "$w/b" && find . -maxdepth 1 -type f \( -name '*.cpp' -o -name '*.h' -o -name '*.inl' \) ! -name '_codemap_types.cpp' \
   -printf '%f\n' | sort | xargs ctags --output-format=json --fields=+n --c++-kinds=f --language-force=c++ --extras=-q -f - 2>/dev/null) \
  | jq -r 'select(._type=="tag") | [.name, .path, .line] | @tsv' > "$w/ctags.tsv"

# 2. the Python: the modules the game loads, parsed by the game's own Python 2.4
python3 -I "$here/extract_py.py" list "$w/py_modules.tsv" "$src/Assets/Python" "$base"
wine "$py24/python.exe" "$(winpath "$here/py24_scan.py")" "$(winpath "$w/py_modules.tsv")" "$(winpath "$cm/map")"
python3 -I "$here/extract_py.py" link "$cm/map" "$w/py_modules.tsv" "$src/Assets/Config"
rm "$cm/map/py_calls_raw.tsv"

# 3. the pages
python3 -I "$here/render.py" "$cm" "$commit" "$w/ctags.tsv"
