"""Convert a prepared textured mesh onto an existing Civ IV skeleton (experimental)."""
import hashlib,json,math,struct,time
from pathlib import Path
if not hasattr(time,'clock'):time.clock=time.perf_counter

def dependencies():
 from pyffi.formats.nif import NifFormat
 import numpy as np
 from PIL import Image
 return NifFormat,np,Image

def load_nif(path):
 N,_,_=dependencies();d=N.Data()
 with Path(path).open('rb') as f:d.read(f)
 if d.version!=0x14000004:raise ValueError('Use a Civ IV NIF 20.0.0.4 donor.')
 return d

def meshes(path):
 N,_,_=dependencies();d=load_nif(path)
 return [(i,x.name.decode('utf-8','replace'),x.data.num_vertices) for i,x in enumerate(d.get_global_iterator()) if isinstance(x,N.NiGeometry) and x.skin_instance and x.data and x.data.has_vertices]

def obj(path):
 v=[];uv=[];norm=[];vertices=[];coords=[];normals=[];tri=[]
 def idx(s,a):
  n=int(s);i=n-1 if n>0 else len(a)+n
  if not n or i<0 or i>=len(a):raise ValueError('Invalid OBJ index.')
  return a[i]
 for line in Path(path).read_text().splitlines():
  a=line.split()
  if not a or a[0].startswith('#'):continue
  if a[0] in ('v','vt','vn'):
   vals=[float(x) for x in a[1:]];need=2 if a[0]=='vt' else 3
   if len(vals)<need or not all(math.isfinite(x) for x in vals):raise ValueError('Invalid OBJ coordinates.')
   {'v':v,'vt':uv,'vn':norm}[a[0]].append(vals[:need])
  elif a[0]=='f':
   if len(a)!=4:raise ValueError('Prepared OBJ must be triangulated.')
   base=len(vertices)
   for ref in a[1:]:
    r=ref.split('/')
    if len(r)!=3 or not all(r):raise ValueError('OBJ requires UVs and normals.')
    vertices.append(idx(r[0],v));t=idx(r[1],uv);coords.append([t[0],1-t[1]]);normals.append(idx(r[2],norm))
   tri.append((base,base+1,base+2))
 if not tri or len(tri)>10000:raise ValueError('Use 1–10,000 triangles.')
 return vertices,coords,normals,tri

def dds(image,path):
 """Uncompressed RGBA DDS with full mip chain; standard Civ IV masks."""
 _,_,Image=dependencies();im=Image.open(image).convert('RGB').convert('RGBA');w,h=im.size
 if w!=h or w not in (256,512,1024):raise ValueError('Use a square 256/512/1024 baked texture.')
 levels=[]
 while True:
  levels.append(im.tobytes())
  if im.width==1:break
  im=im.resize((max(1,im.width//2),max(1,im.height//2)),Image.Resampling.LANCZOS)
 header=[124,0x2100F,h,w,w*4,0,len(levels)]+[0]*11+[32,0x41,0,32,0xff,0xff00,0xff0000,0xff000000,0x401008,0,0,0,0]
 Path(path).write_bytes(b'DDS '+struct.pack('<31I',*header)+b''.join(levels))

def convert(donor,prepared,output,unit_id,mesh_index,rotation=0,keep_other_meshes=True):
 N,np,_=dependencies();prepared=Path(prepared);out=Path(output)
 if not __import__('re').fullmatch(r'UNIT_[A-Z][A-Z0-9_]{0,63}',unit_id):raise ValueError('Use an ID such as UNIT_NEW_GUARD.')
 if any((out/n).exists() for n in ['model.nif','diffuse.dds','model.json']):raise ValueError('Choose a fresh output folder.')
 data=load_nif(donor);blocks=list(data.get_global_iterator());geom=blocks[int(mesh_index)]
 if not isinstance(geom,N.NiGeometry) or not geom.skin_instance:raise ValueError('Select a skinned body mesh.')
 if any(isinstance(c,N.NiGeomMorpherController) for c in geom.get_controllers()):raise ValueError('Morph-controlled donors require manual rigging.')
 if sum(isinstance(x,N.NiGeometry) and x.skin_instance is geom.skin_instance for x in blocks)!=1:raise ValueError('Shared skin instances need manual rigging.')
 root=next((r for r in data.roots if geom in list(r.get_global_iterator())),None)
 if root is None:raise ValueError('Cannot locate geometry scene root.')
 transform=geom.get_transform(relative_to=root);inverse=transform.get_inverse()
 def apply(points,matrix):
  result=[]
  for p in points:
   v=N.Vector3();v.x,v.y,v.z=map(float,p);v=v*matrix;result.append([v.x,v.y,v.z])
  return np.array(result)
 old=np.array([[v.x,v.y,v.z] for v in geom.data.vertices]);world=apply(old,transform);weights=geom.get_vertex_weights()
 if any(not w for w in weights):raise ValueError('Donor has unweighted vertices; choose another body mesh.')
 points,uv,normal,tri=obj(prepared/'building.obj');points=np.array(points);normal=np.array(normal)
 a=math.radians(float(rotation));rot=np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]])
 points=points@rot.T;normal=normal@rot.T
 lo=points.min(axis=0);hi=points.max(axis=0);target_lo=world.min(axis=0);target_hi=world.max(axis=0)
 if hi[2]-lo[2]<1e-6 or target_hi[2]-target_lo[2]<1e-6:raise ValueError('Model and donor must have vertical extent along Z.')
 scale=(target_hi[2]-target_lo[2])/(hi[2]-lo[2]);center=(lo+hi)/2;target_center=(target_lo+target_hi)/2
 points=(points-center)*scale+target_center;local=apply(points,inverse);normlocal=apply(points+normal,inverse)-local;lens=np.linalg.norm(normlocal,axis=1)
 if np.any(lens<1e-8):raise ValueError('Invalid surface normal.')
 normlocal/=lens[:,None]
 # Transfer nearest-surface weights in the same rest-space, with three-point inverse-distance blending.
 output_weights=[];distances=[]
 for start in range(0,len(local),256):
  delta=local[start:start+256,None,:]-old[None,:,:];dist=np.sum(delta*delta,axis=2);near=np.argsort(dist,axis=1)[:,:min(3,len(old))]
  for row,indices in enumerate(near):
   dd=dist[row,indices];distances.append(float(math.sqrt(dd.min())));mix=1/np.maximum(dd,1e-12);mix/=mix.sum();merged={}
   for index,factor in zip(indices,mix):
    for bone,weight in weights[index]:merged[bone]=merged.get(bone,0)+weight*float(factor)
   items=sorted(merged.items(),key=lambda kv:(-kv[1],kv[0]))[:4];total=sum(w for _,w in items)
   if total<=0:raise ValueError('Could not transfer skin weights.')
   output_weights.append([(b,w/total) for b,w in items])
 # Keep the original geometry node, skeleton links, controllers and bind matrices.
 new=type(geom.data)();new.num_vertices=len(local);new.has_vertices=True;new.vertices.update_size();new.has_normals=True;new.normals.update_size();new.num_uv_sets=1;new.uv_sets.update_size()
 for i,(p,n,t) in enumerate(zip(local,normlocal,uv)):
  new.vertices[i].x,new.vertices[i].y,new.vertices[i].z=map(float,p);new.normals[i].x,new.normals[i].y,new.normals[i].z=map(float,n);new.uv_sets[0][i].u,new.uv_sets[0][i].v=t
 if isinstance(new,N.NiTriStripsData):new.set_strips(tri)
 else:new.set_triangles(tri)
 geom.data=new;new.update_center_radius();skin=geom.skin_instance;skin.data=type(skin.data)().deepcopy(skin.data)
 for obj_ in [skin,skin.data]:
  if hasattr(obj_,'skin_partition'):obj_.skin_partition=None
 for bi,b in enumerate(skin.data.bone_list):
  entries=[(i,w) for i,ws in enumerate(output_weights) for bone,w in ws if bone==bi];b.num_vertices=len(entries);b.vertex_weights.update_size()
  for dst,(idx,w) in zip(b.vertex_weights,entries):dst.index=idx;dst.weight=w
  # Bone-space bounds; allow bones with no influence on the reconstructed surface.
  if entries:
   pts=apply([local[i] for i,_ in entries],b.get_transform());c=(pts.min(axis=0)+pts.max(axis=0))/2;b.bounding_sphere_offset.x,b.bounding_sphere_offset.y,b.bounding_sphere_offset.z=map(float,c);b.bounding_sphere_radius=float(np.linalg.norm(pts-c,axis=1).max())
  else:b.bounding_sphere_radius=0
 geom.update_skin_partition(maxbonesperpartition=18,maxbonespervertex=4,stripify=False)
 # Own property copies avoid repainting other parts that share a material.
 found=False
 for i,p in enumerate(geom.properties):
  if isinstance(p,N.NiTexturingProperty):
   q=type(p)().deepcopy(p);source=N.NiSourceTexture();source.use_external=1;source.file_name=('Art/Units/Studio/'+unit_id+'/diffuse.dds').encode();source.use_mipmaps=1;q.has_base_texture=True;q.base_texture.source=source;q.base_texture.uv_set=0
   for attr in ['has_dark_texture','has_detail_texture','has_gloss_texture','has_glow_texture','has_bump_map_texture','has_decal_0_texture','has_decal_1_texture','has_decal_2_texture','has_decal_3_texture']:
    if hasattr(q,attr):setattr(q,attr,False)
   geom.properties[i]=q;found=True
 if not found:raise ValueError('Donor body needs a standard NiTexturingProperty.')
 if not keep_other_meshes:
  for node in blocks:
   if isinstance(node,N.NiNode):
    children=[c for c in node.children if not isinstance(c,N.NiGeometry) or c is geom];node.num_children=len(children);node.children.update_size()
    for i,c in enumerate(children):node.children[i]=c
 out.mkdir(parents=True,exist_ok=True);dds(prepared/'diffuse.png',out/'diffuse.dds')
 with (out/'model.nif').open('wb') as f:data.write(f)
 check=load_nif(out/'model.nif');newgeom=next(x for x in check.get_global_iterator() if isinstance(x,N.NiGeometry) and x.name==geom.name and x.data.num_vertices==len(local))
 assert all(abs(sum(w for _,w in ws)-1)<1e-4 for ws in newgeom.get_vertex_weights())
 return {'triangles':len(tri),'vertices':len(local),'donorMesh':geom.name.decode('utf-8','replace'),'donorSHA256':hashlib.sha256(Path(donor).read_bytes()).hexdigest(),'maxTransferDistance':max(distances),'meanTransferDistance':sum(distances)/len(distances),'automaticWeights':True,'inGameTested':False,'keepOtherMeshes':keep_other_meshes}
