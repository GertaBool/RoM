# Sourced by the safety-run scripts. S is the session scratchpad (lost with the container: rebuild with
# toolchain/setup_toolchain.sh and toolchain/harness/setup.sh, see toolchain/harness/README.md).
: "${S:=/tmp/claude-0/-home-user-RoM/cd72ee4b-5cb9-57d5-996a-fd6ca15cd65f/scratchpad}"
export S
export VCTOOLKIT_DIR=$S/msvc/vctk PSDK_DIR=$S/msvc/psdk WINEPREFIX=$S/msvc/wine32 \
       BTS_SDK_DIR=$S/sdk/beyond-the-sword-sdk-develop/CvGameCoreDLL HARNESS_WORK=$S/hw
export WINEARCH=win32 WINEDEBUG=-all
REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../.." && pwd)
MOD=$S/main            # clone of GitLab rise-of-mankind (origin), branch claude/settlement-economy
