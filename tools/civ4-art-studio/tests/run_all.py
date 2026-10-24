"""Runs every check in the order their outputs depend on, and reports each as passed, failed or skipped.
python tests/run_all.py /path/to/rise-of-mankind   (or set CIV4_MOD; CHROMIUM and BLENDER as in paths.py)
Needs Node.js, Python with Pillow, numpy and Playwright; PyFFI 2.2.3 and Blender 4.x for the model checks, skipped without them."""
import importlib.util,os,shutil,subprocess,sys,time
from pathlib import Path
import paths
ROOT=Path(__file__).resolve().parents[1];T=ROOT/'tests'
mod=paths.mod();fonts=mod/'Assets/res/Fonts';py=sys.executable;node=shutil.which('node')
try:blender=paths.blender()
except SystemExit:blender=None
pyffi=importlib.util.find_spec('pyffi') is not None
# (name, command, what it needs that may be missing, checks whose outputs it reads)
steps=[
 ('build is current',[py,str(ROOT/'build.py'),'--check'],None,[]),
 ('test_core',[node,str(T/'test_core.js'),str(fonts)],None if node else 'Node.js',[]),
 ('test_mesh',[node,str(T/'test_mesh.js')],None if node else 'Node.js',[]),
 ('test_resample',[node,str(T/'test_resample.js')],None if node else 'Node.js',[]),
 ('check_formats',[py,str(T/'check_formats.py'),str(fonts)],None,['test_core']),
 ('validate_nif',[py,str(T/'validate_nif.py')],None if pyffi else 'PyFFI',['test_mesh']),
 ('browser_check',[py,str(T/'browser_check.py'),str(fonts)],None,[]),
 ('resource_check',[py,str(T/'resource_check.py'),str(mod)],None,[]),
 ('building_check',[py,str(T/'building_check.py'),str(mod)],None,[]),
 ('unit_check',[py,str(T/'unit_check.py'),str(mod)],None,[]),
 ('animation_preview_check',[py,str(T/'animation_preview_check.py'),str(mod)],None if pyffi else 'PyFFI',[]),
 ('animation_browser_check',[py,str(T/'animation_browser_check.py')],None,['animation_preview_check']),
 ('motion_lab_check',[py,str(T/'motion_lab_check.py'),str(mod)],None if pyffi else 'PyFFI',[]),
 ('shape_lab_check',[blender,'--background','--python-exit-code','1','--python',str(T/'shape_lab_check.py')],None if blender else 'Blender',[]),
 ('detail_preservation_check',[py,str(T/'detail_preservation_check.py')],None if blender else 'Blender',[]),
 ('surface_check',[py,str(T/'surface_check.py')],None,['building_check','shape_lab_check']),
 ('prepare_models',[py,str(T/'prepare_models.py'),str(mod)],None if blender and pyffi else 'Blender and PyFFI',['shape_lab_check']),
 ('unit_model_check',[py,str(T/'unit_model_check.py'),str(T/'output/unit-model-prepared'),str(mod)],None,['prepare_models','unit_check']),
 ('review_check',[py,str(T/'review_check.py')],None,['prepare_models']),
]
result={}
for name,cmd,missing,needs in steps:
 blocked=[n for n in needs if result.get(n)!='passed']
 if missing or blocked:
  result[name]='skipped';print(f'SKIP  {name}: needs {missing or ", ".join(blocked)}',flush=True);continue
 t=time.time();r=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',env=dict(os.environ,CIV4_MOD=str(mod)))
 result[name]='passed' if r.returncode==0 else 'failed'
 print(f'{"PASS" if r.returncode==0 else "FAIL"}  {name} ({time.time()-t:.0f} s)',flush=True)
 if r.returncode:print('\n'.join('      '+l for l in r.stdout.strip().splitlines()[-15:]),flush=True)
counts={k:list(result.values()).count(k) for k in ['passed','failed','skipped']}
print(f'{counts["passed"]} passed, {counts["failed"]} failed, {counts["skipped"]} skipped')
sys.exit(1 if counts['failed'] else 0)
