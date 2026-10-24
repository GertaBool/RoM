"""Native KF preservation checks, using a local source mod; no game assets bundled."""
import sys,tempfile,json,hashlib,math
from pathlib import Path
import paths
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'helpers'))
from motion_lab import generate,sequence,channels,events,quaternion,motion
mod=paths.mod()
p=mod/'Assets/art/units/CEO_African/CEO_Sushi/CEO_Sushi_MD_Fortify_idle.kf';original=p.read_bytes();d,r=sequence(p);rows=channels(p);index=next(x['index'] for x in rows if x['bone']=='Bip01 Spine' and x['supported'])
with tempfile.TemporaryDirectory() as td:
 report=generate(mod,p,Path(td)/'patch',index,'X',3,2);target=Path(td)/'patch/patch'/p.relative_to(mod);nd,nr=sequence(target)
 assert events(r)==events(nr);assert (r.start_time,r.stop_time,r.cycle_type,r.frequency)==(nr.start_time,nr.stop_time,nr.cycle_type,nr.frequency)
 for j,(old,new) in enumerate(zip(r.controlled_blocks,nr.controlled_blocks)):
  assert old.get_node_name()==new.get_node_name()
  if j!=index:assert old.interpolator.get_hash(data=d)==new.interpolator.get_hash(data=nd),j
  else:
   for name in ['translations','scales']:assert getattr(old.interpolator.data,name).get_hash(data=d)==getattr(new.interpolator.data,name).get_hash(data=nd)
 old=r.controlled_blocks[index].interpolator.data.quaternion_keys;new=nr.controlled_blocks[index].interpolator.data.quaternion_keys
 for a,b in [(old[0],new[0]),(old[-1],new[-1])]:assert abs(abs(sum(x*y for x,y in zip(quaternion(a.value),quaternion(b.value))))-1)<1e-6
 for k in new:assert abs(sum(getattr(k.value,a)**2 for a in ['w','x','y','z'])-1)<1e-5
 assert any(abs(motion(i/100,3,2))>.02 for i in range(101));assert target.read_bytes()!=original
 assert (Path(td)/'patch/backup'/p.relative_to(mod)).read_bytes()==original;assert p.read_bytes()==original
 unsupported=next(x['index'] for x in rows if not x['supported'])
 try:generate(mod,p,Path(td)/'unsupported',unsupported);raise AssertionError('Unsupported track accepted')
 except ValueError as e:assert 'not supported' in str(e)
 try:generate(mod,p,Path(td)/'patch',index);raise AssertionError('Overwrite accepted')
 except ValueError as e:assert 'empty output' in str(e)
result={'passed':['Real KF roundtrip','Unselected interpolator hashes preserved, including compressed tracks','Selected translations/scales unchanged','Event markers and sequence timing unchanged','Normalized rotations and boundary orientations','Exact backup, original untouched, unsupported channels and overwrites rejected'],'in_game_tested':False};(ROOT/'tests/output/motion-lab-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
