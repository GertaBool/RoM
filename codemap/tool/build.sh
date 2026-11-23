#!/bin/bash
# Rebuild the code map from a checkout of the DLL repository (GitLab rise-of-mankind).
# usage: build.sh <rise-of-mankind checkout> <Python 2.4 dir> <base game Python dir>...
#   Python 2.4 dir: the Windows Python 2.4 the game embeds (python.exe), run under Wine to parse the Python
#   base game Python dirs: the Python folders the mod's Python falls back to, in the game's order:
#   Beyond the Sword's, then Civilization IV's
#   JOBS (environment): units compiled at once, default 4
#   BASE_XML_DIRS (environment): the XML folders the game falls back to, in its order, separated by ':'
#     (Beyond the Sword's, then Civilization IV's); without it only the mod's XML is indexed
#   PYAPI_HTML (environment): a copy of https://civ4bug.sourceforge.net/PythonAPI/AllClasses.html; without it the
#     exe's Python classes are unknown to py_resolve.py
# Needs: VCTOOLKIT_DIR PSDK_DIR BTS_SDK_DIR WINEPREFIX (toolchain/README.md), llvm-readobj-18,
# llvm-undname-18, universal-ctags, jq, clang 18, pip packages tree-sitter tree-sitter-cpp libclang.
# Writes codemap/map/*.tsv, the pages codemap/*.md, codemap/files/, and codemap/graph.html.
set -eu
here=$(cd "$(dirname "$0")" && pwd); cm=$(dirname "$here")
src=$(cd "$1" && pwd); py24=$2; shift 2; jobs=${JOBS:-4}
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
python3 -I "$here/extract_py.py" list "$w/py_modules.tsv" "$src/Assets/Python" "$@"
wine "$py24/python.exe" "$(winpath "$here/py24_scan.py")" "$(winpath "$w/py_modules.tsv")" "$(winpath "$cm/map")"
python3 -I "$here/extract_py.py" link "$cm/map" "$w/py_modules.tsv" "$src/Assets/Config"
rm "$cm/map/py_calls_raw.tsv"
python3 -I "$here/extract_py.py" layers "$w/py_modules.tsv" "$cm/map/py_modules.tsv" "$src/Assets/Python" "$@"

# 3. members, XML fills and defines, exactly, with clang; then the XML layers, loaders and function extents
"$here/../../toolchain/clang-gate/mirror.sh" "$src/Assets/CvGameCoreDLL" "$w/mirror" >/dev/null
"$here/../../toolchain/clang-gate/forscope-pass.sh" "$w/mirror" >/dev/null
python3 "$here/members_clang.py" "$w/mirror" "$BTS_SDK_DIR" --jobs "$jobs" --out "$cm/map"
IFS=: read -r -a xmldirs <<< "${BASE_XML_DIRS:-}"
extra_xml=()
[ -d "$src/Assets/Modules" ] && extra_xml+=("mod-module=$src/Assets/Modules")
[ -d "$src/Assets/res" ] && extra_xml+=("mod-res=$src/Assets/res")
[ -d "$src/Assets/Config" ] && extra_xml+=("mod-config=$src/Assets/Config")
python3 "$here/syntax.py" "$src/Assets/CvGameCoreDLL" "$src/Assets/XML" "${xmldirs[@]}" "${extra_xml[@]}"

# 4. the Python's calls resolved as Python resolves them (with the exe's classes when PYAPI_HTML is given)
if [ -n "${PYAPI_HTML:-}" ]; then python3 "$here/pyapi.py" "$PYAPI_HTML" "$src/Assets/CvGameCoreDLL"; fi
python3 "$here/py_resolve.py"

# 5. the pages and the graph
python3 -I "$here/render.py" "$cm" "$commit" "$w/ctags.tsv"
python3 "$here/graph_html.py"

