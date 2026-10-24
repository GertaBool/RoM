"""Builds the two prepared unit models that unit_model_check.py and review_check.py read, from the Shape Lab soldier.
Run after the Blender shape check: python tests/prepare_models.py /path/to/rise-of-mankind. Needs Blender and PyFFI."""
import shutil,sys
from pathlib import Path
import paths
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/output';sys.path.insert(0,str(ROOT/'helpers'))
import unit_model_studio as studio
from unit_model_convert import meshes
mod=paths.mod();source=OUT/'shape-lab/soldier.glb'
if not source.exists():raise SystemExit('Run the Blender shape check first: '+str(source)+' is missing.')
donor=next(r for r in studio.catalog(mod) if r['type']=='ART_DEF_UNIT_SWORDSMAN_GERMAN');body=max(meshes(donor['file']),key=lambda m:m[2])[0]
for name,simplify in [('unit-model-prepared',False),('review-model-final',True)]:
 out=OUT/name
 if out.exists():shutil.rmtree(out)
 m=studio.prepare(mod,paths.blender(),source,str(out),'UNIT_TEST_MODEL',donor,donor,body,triangles=2500,simplify=simplify)
 print(name+':',m['preparation']['sourceTriangles'],'source triangles,',m['report']['triangles'],'exported')
