"""Read-only native NIF/KF preview. Samples skin deformation, never rewrites game files.
The browser renders sampled poses, not the Civ IV shader or KFM transition system.
"""
import base64,json,math,webbrowser
from pathlib import Path
from unit_model_convert import dependencies,load_nif
from motion_lab import quaternion,slerp,sequence,events

def vector(v):return [float(v.x),float(v.y),float(v.z)]
def value(v):return vector(v) if hasattr(v,'x') else [float(v)]
def keys(group,t):
 """Evaluate scalar/vector linear or quadratic NIF keys; refuse other curves."""
 k=list(group.keys)
 if not k:return None
 if t<=k[0].time:return value(k[0].value)
 if t>=k[-1].time:return value(k[-1].value)
 a,b=next((a,b) for a,b in zip(k,k[1:]) if a.time<=t<=b.time)
 u=(t-a.time)/(b.time-a.time);av,bv=value(a.value),value(b.value)
 if int(group.interpolation)==1:return [(1-u)*x+u*y for x,y in zip(av,bv)]
 if int(group.interpolation)==2:
  return [(2*u**3-3*u*u+1)*x+(-2*u**3+3*u*u)*y+(u**3-2*u*u+u)*f+(u**3-u*u)*g for x,y,f,g in zip(av,bv,value(a.forward),value(b.backward))]
 if all(value(x.value)==av for x in k):return av
 raise ValueError('Unsupported varying translation/scale/Euler curve type '+str(group.interpolation))

def spline(points,u):
 """Evaluate an open uniform clamped cubic B-spline (de Boor)."""
 if not points:return None
 n=len(points);degree=min(3,n-1)
 if not degree:return list(points[0])
 u=max(0,min(1,u));knots=[0.]*(degree+1)+[i/(n-degree) for i in range(1,n-degree)]+[1.]*(degree+1)
 k=n-1 if u==1 else next(i for i in range(degree,n) if knots[i]<=u<knots[i+1]);d=[list(points[j+k-degree]) for j in range(degree+1)]
 for r in range(1,degree+1):
  for j in range(degree,r-1,-1):
   i=j+k-degree;den=knots[i+degree-r+1]-knots[i];a=(u-knots[i])/den if den else 0
   d[j]=[(1-a)*x+a*y for x,y in zip(d[j-1],d[j])]
 return d[degree]

def quaternion_matrix(q):
 N,_,_=dependencies();w,x,y,z=quaternion(q);m=N.Matrix33()
 rows=[[1-2*(y*y+z*z),2*(x*y+w*z),2*(x*z-w*y)],[2*(x*y-w*z),1-2*(x*x+z*z),2*(y*z+w*x)],[2*(x*z+w*y),2*(y*z-w*x),1-2*(x*x+y*y)]]
 for i in range(3):
  for j in range(3):setattr(m,'m_%d%d'%(i+1,j+1),rows[i][j])
 return m

def transform_track(i,t,node,warnings):
 N,np,_=dependencies()
 if isinstance(i,N.NiBSplineTransformInterpolator):
  u=(t-i.start_time)/(i.stop_time-i.start_time) if i.stop_time>i.start_time else 0
  tr=spline(list(i.get_translations()),u);rot=spline(list(i.get_rotations()),u);sc=spline([[s] for s in i.get_scales()],u)
 elif isinstance(i,N.NiTransformInterpolator):
  tr=rot=sc=None;d=i.data
  if d:
   tr=keys(d.translations,t);sc=keys(d.scales,t)
   if d.num_rotation_keys:
    if int(d.rotation_type)==4:
     angles=[keys(g,t) for g in d.xyz_rotations]
     if not all(a is not None for a in angles):raise ValueError('Incomplete Euler rotation track')
     # NIF XYZ Euler uses row matrices Rx * Ry * Rz.
     mats=[]
     for axis,a in enumerate(angles):
      q=N.Quaternion();q.w=math.cos(a[0]/2);q.x=q.y=q.z=0;setattr(q,'xyz'[axis],math.sin(a[0]/2));mats.append(quaternion_matrix(q))
     node.rotation=mats[0]*mats[1]*mats[2]
    else:
     ks=list(d.quaternion_keys)
     if int(d.rotation_type)!=1 and len(ks)>1:
      warnings.add('Quaternion TBC/quadratic tracks use key-to-key slerp; their easing is approximate.')
     if t<=ks[0].time:rot=quaternion(ks[0].value)
     elif t>=ks[-1].time:rot=quaternion(ks[-1].value)
     else:
      a,b=next((a,b) for a,b in zip(ks,ks[1:]) if a.time<=t<=b.time);rot=slerp(quaternion(a.value),quaternion(b.value),(t-a.time)/(b.time-a.time))
 else:raise ValueError('Unsupported transform interpolator '+type(i).__name__)
 if tr is None and all(abs(x)<1e20 for x in vector(i.translation)):tr=vector(i.translation)
 if rot is None and not (getattr(getattr(i,'data',None),'rotation_type',0)==4) and abs(i.rotation.w)<1e20:rot=[getattr(i.rotation,c) for c in ('w','x','y','z')]
 if sc is None and abs(i.scale)<1e20:sc=[float(i.scale)]
 if tr is not None:node.translation.x,node.translation.y,node.translation.z=tr
 if sc is not None:node.scale=sc[0]
 if rot is not None:
  norm=math.sqrt(sum(x*x for x in rot))
  if norm<1e-10:raise ValueError('Invalid animation quaternion')
  q=N.Quaternion();q.w,q.x,q.y,q.z=[x/norm for x in rot];node.rotation=quaternion_matrix(q)

def texture_path(name,model,assets):
 rel=str(name).replace('\\','/');paths=[model.parent/Path(rel).name,model.parent/rel]
 if assets:paths.extend([assets/rel,assets/rel.removeprefix('Assets/').removeprefix('assets/')])
 for p in paths:
  if p.is_file():return p
  # Resolve Civ IV's case-insensitive references on Unix too.
  try:
   cur=Path(p.anchor)
   for part in p.parts[1:]:cur=next(c for c in cur.iterdir() if c.name.lower()==part.lower())
   if cur.is_file():return cur
  except (OSError,StopIteration):pass
 return None

def prepare(model,animations,output,assets=None,fps=24):
 N,np,Image=dependencies();model=Path(model).resolve();out=Path(output).resolve();assets=Path(assets).resolve() if assets else None
 if out.exists():raise ValueError('Choose a new HTML filename; existing files are not overwritten.')
 if out==model or out.suffix.lower()!='.html':raise ValueError('Output must be a new .html file.')
 if not 1<=len(animations)<=12:raise ValueError('Select 1–12 KF clips.')
 if not 1<=fps<=30:raise ValueError('Preview sampling must be 1–30 fps.')
 data=load_nif(model);blocks=list(data.get_global_iterator());roots=[x for x in data.roots if isinstance(x,N.NiAVObject)]
 if len(roots)!=1:raise ValueError('Preview needs one NIF scene root.')
 root=roots[0];nodes={};warnings=set();meshes=[];records=[];rest=[]
 for x in blocks:
  if isinstance(x,N.NiAVObject):
   name=x.name.decode('utf-8','replace');nodes.setdefault(name,[]).append(x);rest.append((x,(float(x.scale),x.rotation.get_copy(),vector(x.translation))))
 for g in blocks:
  if not isinstance(g,N.NiGeometry) or not g.data or not g.data.has_vertices:continue
  if any(isinstance(c,N.NiGeomMorpherController) for c in g.get_controllers()):raise ValueError('Morph-controlled geometry needs another previewer.')
  gd=g.data;faces=[list(f) for f in gd.get_triangles()]
  if not faces:continue
  tex=None;alpha=False;missing=None
  for p in g.properties:
   if isinstance(p,N.NiAlphaProperty):alpha=bool(p.flags & 1 or p.flags & 512)
   if isinstance(p,N.NiTexturingProperty) and p.has_base_texture and p.base_texture.source:
    name=p.base_texture.source.file_name.decode('utf-8','replace');path=texture_path(name,model,assets)
    if path:
     import io
     im=Image.open(path).convert('RGBA');im.thumbnail((1024,1024));buf=io.BytesIO();im.save(buf,format='PNG');tex='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
    else:missing=name;warnings.add('Missing diffuse texture: '+name)
  uv=[[float(t.u),float(t.v)] for t in gd.uv_sets[0]] if gd.num_uv_sets else [[0,0]]*len(gd.vertices)
  meshes.append({'name':g.name.decode('utf-8','replace'),'faces':faces,'uv':uv,'texture':tex,'alpha':alpha,'visible':not bool(g.flags & 1),'vertices':len(gd.vertices)});records.append(g)
 if not meshes or sum(m['vertices'] for m in meshes)>30000 or sum(len(m['faces']) for m in meshes)>30000:raise ValueError('Preview supports up to 30,000 vertices and triangles.')
 clips=[];rejected=[];lo=np.full(3,np.inf);hi=-lo
 def matrix(m):return np.array([[getattr(m,'m_%d%d'%(i+1,j+1)) for j in range(4)] for i in range(4)])
 def posed():
  result=[];normal_result=[]
  for g in records:
   source=np.array([vector(v) for v in g.data.vertices]);source_h=np.column_stack([source,np.ones(len(source))]);normal=np.array([vector(n) for n in g.data.normals]) if g.data.has_normals else np.zeros_like(source)
   if g.skin_instance:
    skin=g.skin_instance;v=np.zeros_like(source);ns=np.zeros_like(source);totals=np.zeros(len(source))
    for bone,bind in zip(skin.bones,skin.data.bone_list):
     transform=matrix(bind.get_transform()*bone.get_transform(skin.skeleton_root)*skin.data.get_transform());indices=np.array([w.index for w in bind.vertex_weights],dtype=int);weights=np.array([w.weight for w in bind.vertex_weights])
     if not len(indices):continue
     np.add.at(v,indices,(source_h[indices]@transform)[:,:3]*weights[:,None]);np.add.at(ns,indices,(normal[indices]@np.linalg.inv(transform[:3,:3]).T)*weights[:,None]);np.add.at(totals,indices,weights)
    if np.any(abs(totals-1)>.01):raise ValueError('Model has unweighted or invalidly weighted vertices')
   else:v=source;ns=normal
   world=matrix(g.get_transform(root));v=(np.column_stack([v,np.ones(len(v))])@world)[:,:3];ns=ns@np.linalg.inv(world[:3,:3]).T;ns/=np.maximum(np.linalg.norm(ns,axis=1)[:,None],1e-12)
   if not np.isfinite(v).all() or not np.isfinite(ns).all():raise ValueError('Nonfinite animated vertices or normals')
   result.append(np.round(v,5).tolist());normal_result.append(np.round(ns,5).tolist())
  return result,normal_result

 for path in animations:
  path=Path(path)
  try:
   _,seq=sequence(path);duration=float(seq.stop_time-seq.start_time)
   if duration>20:raise ValueError('Exceeds 20-second preview limit')
   for node,(scale,rotation,translation) in rest:
    node.scale=scale;node.rotation=rotation.get_copy();node.translation.x,node.translation.y,node.translation.z=translation
   tracks=[];used=set();clip_warnings=set();matched=0
   for b in seq.controlled_blocks:
    name=b.get_node_name().decode('utf-8','replace');i=b.interpolator
    if isinstance(i,(N.NiTransformInterpolator,N.NiBSplineTransformInterpolator)):
     match=nodes.get(name,[])
     if not match:match=[node for key,ns in nodes.items() if key.lower()==name.lower() for node in ns]
     if len(match)!=1:raise ValueError('Missing or ambiguous animated node '+name)
     if id(match[0]) in used:raise ValueError('Multiple transform tracks target '+name)
     used.add(id(match[0]));tracks.append((i,match[0]));matched+=1
    else:clip_warnings.add('Visibility/material/event controllers are listed but not played; use mesh visibility controls. ('+type(i).__name__+')')
   if not matched:raise ValueError('No matching skeleton tracks')
   count=math.ceil(duration*fps)+1;frames=[];normal_frames=[]
   if sum(len(c['frames']) for c in clips)+count>1200 or (sum(len(c['frames']) for c in clips)+count)*sum(m['vertices'] for m in meshes)>1800000:raise ValueError('Preview exceeds the frame/vertex budget; select fewer clips or lower sampling FPS.')
   for f in range(count):
    t=float(seq.start_time)+duration*f/(count-1)
    for i,node in tracks:transform_track(i,t,node,clip_warnings)
    positions,normals=posed();frames.append(positions);normal_frames.append(normals)
   for frame in frames:
    for vs in frame:
     v=np.asarray(vs);lo=np.minimum(lo,v.min(axis=0));hi=np.maximum(hi,v.max(axis=0))
   clips.append({'name':path.stem,'duration':duration,'frames':frames,'normals':normal_frames,'events':events(seq),'warnings':sorted(clip_warnings),'start':float(seq.start_time)})
  except (ValueError,IndexError,StopIteration,OSError,ZeroDivisionError,np.linalg.LinAlgError) as e:rejected.append(path.name+': '+str(e))
 if not clips:raise ValueError('No clips could be previewed.\n'+'\n'.join(rejected))
 payload={'model':model.name,'meshes':meshes,'clips':clips,'warnings':sorted(warnings),'rejected':rejected,'center':((lo+hi)/2).tolist(),'radius':float(max(hi-lo)/2)}
 if not payload['radius']>1e-8:raise ValueError('Model has no extent.')
 text=json.dumps(payload,separators=(',',':'),allow_nan=False).replace('<','\\u003c')
 if len(text)>150*1024*1024:raise ValueError('Preview exceeds 150 MB; choose fewer clips or a smaller model.')
 template=Path(__file__).with_name('unit_animation_viewer.html').read_text();out.parent.mkdir(parents=True,exist_ok=True);out.write_text(template.replace('/*PREVIEW_DATA*/',text),encoding='utf-8')
 return {'clips':[c['name'] for c in clips],'rejected':rejected,'warnings':sorted(warnings),'clipWarnings':{c['name']:c['warnings'] for c in clips},'vertices':sum(m['vertices'] for m in meshes),'output':str(out)}

def gui():
 import tkinter as tk
 from tkinter import ttk,filedialog,messagebox
 import threading
 w=tk.Tk();w.title('Civ IV — Textured Unit Animation Preview');w.geometry('820x640');f=ttk.Frame(w,padding=18);f.pack(fill='both',expand=True);f.columnconfigure(1,weight=1)
 model=tk.StringVar();assets=tk.StringVar();files=[]
 ttk.Label(f,text='Preview your actual unit and its native animations',font=('',14,'bold')).grid(row=0,column=0,columnspan=3,sticky='w',pady=10)
 def choose_model():
  p=filedialog.askopenfilename(filetypes=[('Civ IV model','*.nif')])
  if p:
   model.set(p);files[:]=sorted(Path(p).parent.glob('*.kf'));refresh()
   for parent in Path(p).parents:
    if parent.name.lower()=='assets':assets.set(str(parent));break
 ttk.Label(f,text='Unit NIF').grid(row=1,column=0);ttk.Entry(f,textvariable=model).grid(row=1,column=1,sticky='ew');ttk.Button(f,text='Choose model',command=choose_model).grid(row=1,column=2)
 ttk.Label(f,text='Assets folder').grid(row=2,column=0);ttk.Entry(f,textvariable=assets).grid(row=2,column=1,sticky='ew')
 def choose_assets():
  p=filedialog.askdirectory()
  if p:assets.set(p)
 ttk.Button(f,text='Browse',command=choose_assets).grid(row=2,column=2)
 ttk.Label(f,text='Select animation clips (Ctrl/Shift for several). Nearby KF files appear automatically.').grid(row=3,column=0,columnspan=3,sticky='w',pady=12)
 box=tk.Listbox(f,selectmode='extended',exportselection=False,height=14);box.grid(row=4,column=0,columnspan=3,sticky='nsew');f.rowconfigure(4,weight=1)
 def refresh():
  box.delete(0,'end')
  for p in files:box.insert('end',p.name)
  if files:box.selection_set(0)
 def add():
  for p in filedialog.askopenfilenames(filetypes=[('Civ IV animation','*.kf')]):
   if Path(p) not in files:files.append(Path(p))
  refresh()
 bar=ttk.Frame(f);bar.grid(row=5,column=0,columnspan=3,sticky='ew',pady=8);ttk.Button(bar,text='Add KF clips from another folder',command=add).pack(side='left');ttk.Label(bar,text='  Sampling FPS ').pack(side='left');rate=tk.StringVar(value='24');ttk.Combobox(bar,textvariable=rate,values=['24','12','6'],width=5,state='readonly').pack(side='left')
 ttk.Label(f,text='Uses original textured meshes and skin weights, including equipment. Works with exported model.nif too.\nMatching node names are checked; compatible skeletons/rest poses must still be chosen.\nPreview reports interpolation approximations and missing materials. It does not simulate game shaders, KFM transitions or effects.',wraplength=760).grid(row=6,column=0,columnspan=3,sticky='w')
 status=tk.StringVar();ttk.Label(f,textvariable=status,wraplength=760).grid(row=8,column=0,columnspan=3,sticky='w')
 def run():
  selected=[files[i] for i in box.curselection()]
  if not selected:messagebox.showerror('Select clips','Choose one or more animation clips.');return
  output=filedialog.asksaveasfilename(defaultextension='.html',filetypes=[('Offline animation preview','*.html')])
  if not output:return
  args=(model.get(),selected,output,assets.get() or None,int(rate.get()));button.config(state='disabled');status.set('Sampling native animation and skinning. The window stays responsive…')
  import queue
  results=queue.Queue()
  def worker():
   try:results.put((True,prepare(*args)))
   except Exception as e:results.put((False,str(e)))
  def poll():
   try:ok,result=results.get_nowait()
   except queue.Empty:w.after(100,poll);return
   button.config(state='normal')
   if ok:status.set('Preview ready. '+('; '.join(result['rejected']) if result['rejected'] else ''));webbrowser.open(Path(output).resolve().as_uri())
   else:status.set('Preview could not be built.');messagebox.showerror('Cannot preview',result)
  threading.Thread(target=worker,daemon=True).start();poll()
 button=ttk.Button(f,text='Build and open animated unit preview',command=run);button.grid(row=7,column=0,columnspan=3,sticky='ew',pady=15);w.mainloop()
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--model');p.add_argument('--kf',action='append');p.add_argument('--output');p.add_argument('--assets');p.add_argument('--fps',type=int,default=24);a=p.parse_args()
 if a.model:print(json.dumps(prepare(a.model,a.kf or [],a.output,a.assets,a.fps),indent=2))
 else:gui()
