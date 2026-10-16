#!/usr/bin/env python3
"""Replace generated base-game XML with the game's own files.

The game resolves XML the mod does not ship from Beyond the Sword's Assets/XML,
then from the original game's Assets/XML. gen_bts_xml.py can only approximate
those files; with copies of the two folders, this script lays them over its
output in the same order (original game first, Beyond the Sword on top), so
every file found there is the game's own. Generated files remain for anything
the copies lack.

A trailing " (1)" on a file or folder name (left by some downloads of the
folders) is dropped.
usage: overlay_game_xml.py <out XML dir> <original game Assets/XML> <BTS Assets/XML>
"""
import os, re, shutil, sys

out, base, bts = sys.argv[1:4]


def clean(name):
    return re.sub(r' \(\d+\)(?=\.[^.]+$|$)', '', name)


generated = set()
for dirpath, _, files in os.walk(out):
    generated.update(os.path.relpath(os.path.join(dirpath, f), out).lower() for f in files)
written = set()
for src in (base, bts):
    for dirpath, _, files in os.walk(src):
        rel = os.path.relpath(dirpath, src)
        rel = '' if rel == '.' else os.path.join(*[clean(p) for p in rel.split(os.sep)])
        for f in files:
            if not f.lower().endswith('.xml'):
                continue
            dst = os.path.join(out, rel, clean(f))
            # The engine opens files case-insensitively; keep the generated spelling.
            folder = os.path.dirname(dst)
            os.makedirs(folder, exist_ok=True)
            same = [g for g in os.listdir(folder) if g.lower() == os.path.basename(dst).lower()]
            if same:
                dst = os.path.join(folder, same[0])
            written.add(os.path.relpath(dst, out).lower())
            shutil.copyfile(os.path.join(dirpath, f), dst)
print('game XML: %d of %d generated files replaced, %d files added'
      % (len(written & generated), len(generated), len(written - generated)))
