#!/bin/bash
# Rebuild the code map from a checkout of the DLL repository (GitLab rise-of-mankind).
# usage: build.sh <rise-of-mankind checkout> <base game Python dir> <Python 2.4 dir> <original SDK dir> <XML dir>...
#   base game Python dir: the Python folder of Beyond the Sword, which the mod's Python falls back to
#   Python 2.4 dir: the Windows Python 2.4 the game embeds (python.exe), run under Wine to parse the Python
#   original SDK dir: the CvGameCoreDLL folder of the BTS 3.19 SDK as Firaxis shipped it
#   XML dirs: the XML folders the game falls back to after the mod's, in order (Beyond the Sword's, then
#   Civilization IV's)
#   JOBS (environment): units compiled at once, default 4
#   A base game Python dir of "-" refreshes the DLL only: steps 1 and 3 run on the checkout, and the Python and
#   hard-coded tables of the previous build are kept (they need the base game's Python and XML); the commit line
#   says so.
# Needs: VCTOOLKIT_DIR PSDK_DIR BTS_SDK_DIR WINEPREFIX (toolchain/README.md), llvm-readobj-18,
# llvm-undname-18, universal-ctags, jq. Writes codemap/map/*.tsv and the pages codemap/*.md, codemap/files/.
set -eu
here=$(cd "$(dirname "$0")" && pwd); cm=$(dirname "$here")
src=$(cd "$1" && pwd); base=$2; py24=$3; sdk=$4; shift 4; jobs=${JOBS:-4}
export WINEARCH=win32 WINEDEBUG=-all
commit=$(git -C "$src" rev-parse --short=12 HEAD)
[ -z "$(git -C "$src" status --porcelain --untracked-files=no -- Assets/CvGameCoreDLL Assets/Python)" ] \
  || commit="$commit (with uncommitted changes)"
w=$(mktemp -d); trap 'rm -rf "$w"' EXIT
winpath() { echo "Z:$(realpath -s "$1" | tr / '\\')"; }

# 1. the DLL: compile every unit with the real compiler, then read the listings and the type records
"$here/compile.sh" "$src/Assets/CvGameCoreDLL" "$w" "$jobs"
dll_only=; [ "$base" = "-" ] && dll_only=1
if [ -n "$dll_only" ]; then
  keep=$(git -C "$cm" log -1 --format=%h -- map/py_functions.tsv 2>/dev/null || echo unknown)
  mkdir -p "$w/oldmap"; cp "$cm"/map/*.tsv "$w/oldmap/" 2>/dev/null || true
  commit="$commit (DLL; Python and hard-coded tables from the previous build, repository commit $keep)"
fi
rm -rf "$cm/map"; mkdir -p "$cm/map"
python3 -I "$here/extract_asm.py" "$w/out" "$w/b" "$cm/map"
# an independent count of the definitions in the same files, for map/completeness.tsv
(cd "$w/b" && find . -maxdepth 1 -type f \( -name '*.cpp' -o -name '*.h' -o -name '*.inl' \) ! -name '_codemap_types.cpp' \
   -printf '%f\n' | sort | xargs ctags --output-format=json --fields=+n --c++-kinds=f --language-force=c++ --extras=-q -f - 2>/dev/null) \
  | jq -r 'select(._type=="tag") | [.name, .path, .line] | @tsv' > "$w/ctags.tsv"

# 2. the Python: the modules the game loads, parsed by the game's own Python 2.4
if [ -n "$dll_only" ]; then
  ids="py_to_cpp.tsv cpp_to_py.tsv event_handlers.tsv hardcoded.tsv"   # tables that name functions by id
  for f in "$w"/oldmap/*.tsv; do b=$(basename "$f"); case " $ids " in *" $b "*) ;; *) [ -e "$cm/map/$b" ] || cp "$f" "$cm/map/";; esac; done
  python3 -I "$here/remap_ids.py" "$w/oldmap" "$cm/map" $ids
else
python3 -I "$here/extract_py.py" list "$w/py_modules.tsv" "$src/Assets/Python" "$base"
wine "$py24/python.exe" "$(winpath "$here/py24_scan.py")" "$(winpath "$w/py_modules.tsv")" "$(winpath "$cm/map")"
python3 -I "$here/extract_py.py" link "$cm/map" "$w/py_modules.tsv" "$src/Assets/Config"
rm "$cm/map/py_calls_raw.tsv"
fi

# 3. the pages
python3 -I "$here/render.py" "$cm" "$commit" "$w/ctags.tsv"

# 4. the hard-coded entries of the key functions, checked against the exe's SDK, the XML and Python
[ -n "$dll_only" ] || python3 -I "$here/hardcoded.py" "$cm" "$src" "$sdk" "$@"
