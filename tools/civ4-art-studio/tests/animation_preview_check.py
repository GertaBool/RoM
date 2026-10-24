"""Independent rigid/skin motion expectations and real-asset browser playback checks.
Native fixture is read from the local game only; it is never packaged or published.
"""
import sys,json,tempfile,math,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'helpers'))
from unit_animation_preview import prepare,spline,quaternion_matrix,transform_track
from unit_model_convert import dependencies
N,np,Image=dependencies()
# The cubic spline with 4 points is a Bezier curve, with an independent midpoint.
assert np.allclose(spline([[0],[0],[1],[1]],.5),[.5])
assert spline([[0],[1],[3],[8],[10]],0)==[0] and spline([[0],[1],[3],[8],[10]],1)==[10]
q=N.Quaternion();q.w=math.sqrt(.5);q.z=math.sqrt(.5);q.x=q.y=0;m=quaternion_matrix(q);v=N.Vector3();v.x=1;v.y=v.z=0;v=v*m
assert np.allclose([v.x,v.y,v.z],[0,1,0],atol=1e-6)
# A native skin with one bone, and a known translation track (0 -> 2 along X).
root=N.NiNode();root.name=b'Root';bone=N.NiNode();bone.name=b'Bone';g=N.NiTriShape();g.name=b'Triangle';root.add_child(bone);root.add_child(g)
g.data=N.NiTriShapeData();g.data.num_vertices=3;g.data.has_vertices=True;g.data.vertices.update_size();g.data.has_normals=True;g.data.normals.update_size()
for dst,xyz in zip(g.data.vertices,[(0,0,0),(1,0,0),(0,0,1)]):dst.x,dst.y,dst.z=xyz
for n in g.data.normals:n.x,n.y,n.z=0,-1,0
g.data.set_triangles([(0,1,2)]);g.skin_instance=N.NiSkinInstance();g.skin_instance.skeleton_root=root;g.skin_instance.data=N.NiSkinData();g.skin_instance.num_bones=1;g.skin_instance.bones.update_size();g.skin_instance.bones[0]=bone;g.skin_instance.data.num_bones=1;g.skin_instance.data.bone_list.update_size();bd=g.skin_instance.data.bone_list[0];bd.num_vertices=3;bd.vertex_weights.update_size()
for index,w in enumerate(bd.vertex_weights):w.index=index;w.weight=1
seq=N.NiControllerSequence();seq.name=b'known translation';seq.start_time=0;seq.stop_time=1;b=seq.add_controlled_block();b.set_node_name(b'Bone');b.interpolator=N.NiTransformInterpolator();i=b.interpolator;i.rotation.w=1;i.rotation.x=i.rotation.y=i.rotation.z=0;i.scale=1;i.data=N.NiTransformData();group=i.data.translations;group.num_keys=2;group.interpolation=1;group.keys.update_size()
for key,t,x in zip(group.keys,[0,1],[0,2]):key.time=t;key.value.x=x;key.value.y=key.value.z=0
out=R/'tests/output';out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
 tmp=Path(tmp)
 for name,r in [('synthetic.nif',root),('move.kf',seq)]:
  data=N.Data(version=0x14000004);data.header.endian_type=1;data.roots=[r]
  with (tmp/name).open('wb') as f:data.write(f)
 result=prepare(tmp/'synthetic.nif',[tmp/'move.kf'],tmp/'preview.html',fps=2)
 text=(tmp/'preview.html').read_text();payload=json.loads(text.split('const D=',1)[1].split(';\nconst $=',1)[0]);frames=payload['clips'][0]['frames']
 assert np.allclose(np.asarray(frames[1][0])-np.asarray(frames[0][0]),[1,0,0])
 assert np.allclose(np.asarray(frames[2][0])-np.asarray(frames[0][0]),[2,0,0])
 try:prepare(tmp/'synthetic.nif',[tmp/'move.kf'],tmp/'preview.html')
 except ValueError:pass
 else:raise AssertionError('Overwrite was not refused')
# Integration with a real humanoid and both compressed and ordinary KF tracks.
model=Path('/workspace/rise-of-mankind/Assets/art/units/GreatLeader_Sioux/medieval/Warlord_Ancient.nif');clips=[model.with_name('Warlord_Ancient_MD_'+n+'.kf') for n in ['Run','Idle']];tracked=[model,*clips];before=[hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked]
preview=out/'native-animation-local.html'
if preview.exists():preview.unlink()
report=prepare(model,clips,preview,model.parents[3],fps=24)
assert len(report['clips'])==2,report
assert [hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked]==before
report['checks']=['Quaternion row-matrix rotation','Independent cubic endpoint/midpoint expectations','Known skinned translation at start/mid/end','Existing output protected','Native humanoid Run and Idle clips exported','Source model and clips unchanged'];report.pop('output');report['in_game_tested']=False
(out/'animation-preview-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
