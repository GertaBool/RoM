#!/bin/bash
# Lay out a game folder: harness.exe and DLLs, the mod under Mods\, base XML under BTS\.
# usage: mkroot.sh <root> <build dir from build_dll.sh> <mod checkout containing Assets>
set -e
root=$1; dll=$2; mod=$3
source "$(dirname "$0")/env.sh"
mkdir -p "$root/Mods" "$root/BTS/Assets" "$root/logs"
rm -f "$root/Mods/Rise of Mankind" "$root/BTS/Assets/XML"
ln -s "$(readlink -f "$mod")" "$root/Mods/Rise of Mankind"
ln -s "$WORK/btsxml" "$root/BTS/Assets/XML"
cp "$WORK/obj/harness.exe" "$dll/release/CvGameCoreDLL.dll" "$WORK/out/python24.dll" "$WORK/out/boost_python-vc71-mt-1_32.dll" "$root/"
