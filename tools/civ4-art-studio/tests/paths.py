"""Where the checks find the mod, Chromium and Blender, on any machine.
Mod: the first argument, else CIV4_MOD (the folder that contains Assets). Chromium: CHROMIUM, else Playwright's own.
Blender: BLENDER, else blender on PATH."""
import os,shutil,sys
from pathlib import Path

def mod():
 p=sys.argv[1] if len(sys.argv)>1 else os.environ.get('CIV4_MOD')
 if not p:raise SystemExit('Give the Rise of Mankind folder (the one containing Assets) as the first argument or in CIV4_MOD.')
 return Path(p)

def browser(p,**kw):
 exe=os.environ.get('CHROMIUM')
 return p.chromium.launch(**({'executable_path':exe} if exe else {}),**kw)

def blender():
 b=os.environ.get('BLENDER') or shutil.which('blender')
 if not b:raise SystemExit('Blender not found: set BLENDER or put blender on PATH.')
 return b
