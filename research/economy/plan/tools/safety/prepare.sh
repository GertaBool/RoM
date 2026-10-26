#!/bin/bash
# prepare.sh <name> <mod commit> [<name> <commit>]...: a harness game folder per mod state, all with one harness
# DLL built from the mod clone's current DLL source (the economy branch changes XML only, so every arm runs the
# same DLL). Each state is extracted with git archive without art (Assets/Art, Sounds and model or texture
# files: the harness reads only XML) to $S/eco/src-<name>; game folders go to $S/hw/root-eco-<name>.
set -e
source "$(dirname "$0")/env.sh"
H=$REPO/toolchain/harness
if [ ! -f "$S/hw/b-eco/release/CvGameCoreDLL.dll" ]; then
  "$H/build_dll.sh" "$MOD/Assets/CvGameCoreDLL" "$S/hw/b-eco"
  "$H/build_harness.sh" "$S/hw/b-eco"
fi
mkdir -p "$S/eco"
while [ $# -ge 2 ]; do
  name=$1; rev=$2; shift 2
  wt=$S/eco/src-$name
  if [ ! -d "$wt" ]; then
    mkdir -p "$wt"
    git -C "$MOD" archive "$rev" -- Assets ':!Assets/Art' ':!Assets/Sounds' \
      ':!*.dds' ':!*.nif' ':!*.kfm' ':!*.kf' ':!*.tga' ':!*.bik' ':!*.mp3' ':!*.wav' | tar -x -C "$wt"
    echo "$rev" > "$wt/REV"
  fi
  "$H/mkroot.sh" "$S/hw/root-eco-$name" "$S/hw/b-eco" "$wt"
  echo "$name $(cat "$wt/REV") $(du -sh "$wt" | cut -f1) -> $S/hw/root-eco-$name"
done
