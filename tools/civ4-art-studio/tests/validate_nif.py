"""Independent development check. Requires PyFFI 2.2.3; not needed by the app."""
from pathlib import Path
import sys,time,math,json
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'work/deps').exists():sys.path.insert(0,str(ROOT/'work/deps'))
# PyFFI predates Python 3.8; restore its removed timing alias for this test only.
if not hasattr(time,'clock'):time.clock=time.perf_counter
from pyffi.formats.nif import NifFormat
files=list((ROOT/'tests/output').glob('mesh-*.nif'))
if (ROOT/'tests/output/browser-building.nif').exists():files.append(ROOT/'tests/output/browser-building.nif')
assert files,'Run test_mesh.js first.'
checks=[]
for path in files:
 data=NifFormat.Data()
 with path.open('rb') as f:data.read(f);assert f.tell()==path.stat().st_size
 assert data.version==0x14000004
 shapes=[x for x in data.get_global_iterator() if isinstance(x,NifFormat.NiTriShape)];assert len(shapes)==1
 shape=shapes[0];mesh=shape.data;assert mesh.has_normals and mesh.num_uv_sets==1;assert 0<mesh.num_triangles<=20000;assert mesh.num_vertices<65536
 assert all(t.v_1<mesh.num_vertices and t.v_2<mesh.num_vertices and t.v_3<mesh.num_vertices for t in mesh.triangles)
 assert math.isfinite(mesh.radius) and mesh.radius>0
 assert all(math.sqrt((v.x-mesh.center.x)**2+(v.y-mesh.center.y)**2+(v.z-mesh.center.z)**2)<=mesh.radius+1e-4 for v in mesh.vertices)
 assert len(mesh.uv_sets[0])==mesh.num_vertices
 assert all(math.isfinite(v.x) and math.isfinite(v.y) and math.isfinite(v.z) for v in mesh.vertices)
 assert all(abs(math.sqrt(n.x*n.x+n.y*n.y+n.z*n.z)-1)<1e-4 for n in mesh.normals)
 prop=next(x for x in shape.properties if isinstance(x,NifFormat.NiTexturingProperty));assert prop.has_base_texture and prop.base_texture.source.file_name.startswith(b'Art/') and prop.base_texture.source.file_name.endswith(b'/diffuse.dds')
 assert prop.base_texture.source.use_mipmaps==1
 checks.append(f'{path.name}: valid static scene, geometry, normals, UVs, bounds and linked diffuse texture')
print('\n'.join(checks));(ROOT/'tests/output/nif-validation.json').write_text(json.dumps({'decoder':'PyFFI 2.2.3','passed':checks,'in_game_tested':False},indent=2)+'\n')
