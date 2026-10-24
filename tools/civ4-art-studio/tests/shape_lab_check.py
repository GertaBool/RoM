"""Run in Blender: blender --background --python tests/shape_lab_check.py."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'helpers'));import shape_lab
out=ROOT/'tests/output/shape-lab';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);shape_lab.register();s=bpy.context.scene.studio_shape
counts={}
# Generation is deterministic in object/triangle budget; unrelated objects survive rebuild.
bpy.ops.mesh.primitive_cube_add(location=(20,20,20));sentinel=bpy.context.object;sentinel.name='Unrelated scene object'
for style in ['CLOTH','MAIL','PLATE']:
 s.style=style;col=shape_lab.build(s);assert bpy.data.objects.get(sentinel.name) is sentinel
 deps=bpy.context.evaluated_depsgraph_get();count=0
 for ob in col.objects:
  e=ob.evaluated_get(deps);mesh=e.to_mesh();count+=sum(len(p.vertices)-2 for p in mesh.polygons);assert all(all(__import__('math').isfinite(v) for v in point.co) for point in mesh.vertices);e.to_mesh_clear()
 counts[style]=count;assert 500<count<10000
 coords=[ob.matrix_world @ v.co for ob in col.objects for v in ob.data.vertices]
 assert min(v.z for v in coords)>-.02 and max(v.z for v in coords)<2.05
 assert max(abs(v.x) for v in coords)<1.1
# Height must transform every part in world space, including rotated limbs.
s.height=1;col=shape_lab.build(s);before=[tuple(v.co) for ob in col.objects for v in ob.data.vertices]
s.height=1.3;col=shape_lab.build(s);after=[tuple(v.co) for ob in col.objects for v in ob.data.vertices]
assert len(before)==len(after)
assert all(abs(a[0]-b[0])<1e-5 and abs(a[1]-b[1])<1e-5 and abs(a[2]*1.3-b[2])<1e-5 for a,b in zip(before,after))
s.height=1;shape_lab.build(s)
bpy.data.objects.remove(sentinel,do_unlink=True);s.output=str(out/'soldier.glb')
if Path(s.output).exists():Path(s.output).unlink()
assert bpy.ops.studio.export_shape()=={'FINISHED'}
try:bpy.ops.studio.export_shape();raise AssertionError('Overwrite accepted')
except RuntimeError as e:assert 'Output exists' in str(e)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'soldier.blend'))
# Render diagnostic presentation, not included in model export.
bpy.ops.mesh.primitive_plane_add(size=200);floor=bpy.context.object;floor.data.materials.append(shape_lab.material('Backdrop',(.045,.065,.07)))
bpy.ops.object.camera_add(location=(3,-5,2.6));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,1))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=2.65;bpy.context.scene.camera=camera
for name,pos,power,size in [('Key',(-3,-4,5),550,4),('Fill',(4,-1,3),350,3),('Rim',(0,3,4),650,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);light=bpy.context.object;light.name=name;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(Vector((0,0,1))-light.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100;scene.world=bpy.data.worlds.new('Studio world');scene.world.use_nodes=True;scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.15,.18,.2,1);scene.render.filepath=str(out/'preview.png');bpy.ops.render.render(write_still=True)
(ROOT/'tests/output/shape-lab-validation.json').write_text(json.dumps({'triangles':counts,'checks':['All three armor types generated','Unrelated scene preserved','Finite coordinates, shape bounds, triangle budget and world-space height scaling','Neutral GLB export and overwrite refusal','Blender render produced'],'in_game_tested':False},indent=2)+'\n')
