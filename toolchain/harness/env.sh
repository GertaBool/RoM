# Sourced by the harness scripts. Uses the variables from toolchain/README.md:
#   VCTOOLKIT_DIR PSDK_DIR BTS_SDK_DIR WINEPREFIX
# Generated files and builds go to HARNESS_WORK (default: work/ next to this file).
: "${VCTOOLKIT_DIR:?}" "${PSDK_DIR:?}" "${BTS_SDK_DIR:?}" "${WINEPREFIX:?}"
export WINEARCH=win32 WINEDEBUG=-all
winpath() { echo "Z:$(realpath -s "$1" | tr / '\\')"; }
export INCLUDE="$(winpath "$VCTOOLKIT_DIR/include");$(winpath "$PSDK_DIR/Include")"
export LIB="$(winpath "$VCTOOLKIT_DIR/lib");$(winpath "$PSDK_DIR/Lib")"
CL="$VCTOOLKIT_DIR/bin/cl.exe"; LINK="$VCTOOLKIT_DIR/bin/link.exe"
H=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORK=${HARNESS_WORK:-$H/work}
mkdir -p "$WORK"
