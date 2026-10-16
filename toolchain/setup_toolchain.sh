#!/bin/bash
# Unpack the toolchain without running any Windows installer.
# usage: setup_toolchain.sh <toolkit-installer.exe> <PlatformSDK_Svr2003SP1.img> <dest>
# Needs: innoextract, 7z, msiextract (msitools), wine32. Prints the environment for build_dll.sh.
set -e
installer=$1; iso=$2; dest=$(readlink -f "$3"); mkdir -p "$dest"
innoextract -s -d "$dest/toolkit" "$installer"
tk="$dest/toolkit/app/Microsoft Visual C++ Toolkit 2003"
mkdir -p "$dest/iso" "$dest/msi"
(cd "$dest/iso" && 7z x -y "$(readlink -f "$iso")" >/dev/null)
msiextract -C "$dest/msi" "$dest/iso/Setup/PSDK-x86.msi" >/dev/null
psdk_src=$(find "$dest/msi" -maxdepth 3 -type d -name "Microsoft Platform SDK*" | head -1)
mkdir -p "$dest/psdk"; cp -r "$psdk_src/Include" "$psdk_src/Lib" "$psdk_src/Bin" "$dest/psdk/"
# MSVC asks for headers and libraries case-insensitively; Linux filesystems are not.
for d in "$tk/include" "$tk/lib" "$dest/psdk/Include" "$dest/psdk/Lib"; do
  find "$d" -type f | while read -r f; do
    dir=$(dirname "$f"); b=$(basename "$f"); lb=$(echo "$b" | tr 'A-Z' 'a-z')
    [ "$b" != "$lb" ] && [ ! -e "$dir/$lb" ] && ln -s "$b" "$dir/$lb"
  done
done
ln -sfn "$tk" "$dest/vctk"
WINEARCH=win32 WINEPREFIX="$dest/wine32" wineboot -i >/dev/null 2>&1 || true
echo "export VCTOOLKIT_DIR=$dest/vctk PSDK_DIR=$dest/psdk WINEPREFIX=$dest/wine32"
