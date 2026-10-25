"""Integration checks for explicit simplification and loss guards; requires Blender 4.x."""
from pathlib import Path
import subprocess,tempfile,os,json,sys
import paths
R=Path(__file__).resolve().parents[1];OUT=R/'tests/output';env=dict(os.environ,BLENDER_USER_CONFIG=str(Path(tempfile.gettempdir())/'civ4-blender-config'),BLENDER_USER_SCRIPTS=str(Path(tempfile.gettempdir())/'civ4-blender-scripts'))
with tempfile.TemporaryDirectory() as td:
 t=Path(td);script=t/'fixture.py';script.write_text('''import bpy
from pathlib import Path
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16)
bpy.context.object.name='DetailedBody'
bpy.ops.mesh.primitive_cube_add(size=.1,location=(1.2,0,0));bpy.context.object.name='FineEquipment'
m=bpy.data.materials.new('Source');m.use_nodes=True
for o in bpy.context.scene.objects:o.data.materials.append(m)
p=Path(__file__).parent
bpy.ops.wm.save_as_mainfile(filepath=str(p/'opaque.blend'))
m.node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value=.2
bpy.ops.wm.save_as_mainfile(filepath=str(p/'alpha.blend'))
m.node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value=1
bump=m.node_tree.nodes.new('ShaderNodeBump');m.node_tree.links.new(bump.outputs['Normal'],m.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
bpy.ops.wm.save_as_mainfile(filepath=str(p/'normal.blend'))
''')
 def run(args):return subprocess.run([paths.blender(),'--background','--threads','2','--python-exit-code','1',*args],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 a=run(['--python',str(script)]);assert a.returncode==0,a.stdout[-3000:]
 def bake(name,source,flags=()):return run(['--python',str(R/'helpers/prepare_building.py'),'--',str(t/source),str(t/name),'--size','256','--triangles','400',*flags])
 a=bake('preserve','opaque.blend');assert a.returncode==0,a.stdout[-3000:];p=json.loads((t/'preserve/preparation.json').read_text());assert p['sourceTriangles']==p['triangles'] and not p['simplificationRequested']
 a=bake('reduce','opaque.blend',['--simplify']);assert a.returncode==0,a.stdout[-3000:];d=json.loads((t/'reduce/preparation.json').read_text());assert d['triangles']<p['triangles'];small=next(x for x in d['parts'] if 'FineEquipment' in x['name']);assert small['beforeTriangles']==small['afterTriangles']==12
 a=bake('alpha','alpha.blend');assert a.returncode!=0 and 'alpha/transparency' in a.stdout
 a=bake('normal','normal.blend');assert a.returncode!=0 and 'normal/bump input' in a.stdout
 a=bake('accepted','alpha.blend',['--allow-alpha-flatten']);assert a.returncode==0,a.stdout[-3000:];assert json.loads((t/'accepted/preparation.json').read_text())['materialLosses']
 report={'passed':['Source triangle count preserved by default','Simplification requires explicit opt-in and retains tiny equipment mesh','Transparency and linked normal detail rejected by default','Explicit accepted alpha loss recorded in preparation report'],'beforeTriangles':p['triangles'],'afterBudgetTriangles':d['triangles'],'in_game_tested':False};(OUT/'detail-preservation-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
