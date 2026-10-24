"""Native Civ IV KF motion layers. Preserves timeline, event markers and other tracks.
First version edits LINEAR quaternion channels only; compressed/Euler/TBC channels
are explicitly unsupported, not silently resampled or discarded.
"""
import math,json,hashlib
from pathlib import Path
from unit_model_convert import dependencies,load_nif

def quaternion(q):
 v=[float(getattr(q,k)) for k in ('w','x','y','z')];n=math.sqrt(sum(x*x for x in v))
 if not math.isfinite(n) or n<1e-8 or n>2:raise ValueError('Invalid quaternion channel.')
 return [x/n for x in v]

def slerp(a,b,t):
 dot=sum(x*y for x,y in zip(a,b))
 if dot<0:b=[-x for x in b];dot=-dot
 dot=max(-1,min(1,dot))
 if dot>.9995:
  q=[x+t*(y-x) for x,y in zip(a,b)];n=math.sqrt(sum(x*x for x in q));return [x/n for x in q]
 a0=math.acos(dot);den=math.sin(a0);return [(math.sin((1-t)*a0)*x+math.sin(t*a0)*y)/den for x,y in zip(a,b)]

def multiply(a,b):
 w,x,y,z=a;v,i,j,k=b
 return [w*v-x*i-y*j-z*k,w*i+x*v+y*k-z*j,w*j-x*k+y*v+z*i,w*k+x*j-y*i+z*v]

def sequence(path):
 N,_,_=dependencies();d=load_nif(path)
 if len(d.roots)!=1 or not isinstance(d.roots[0],N.NiControllerSequence):raise ValueError('Choose a single-sequence Civ IV KF file.')
 r=d.roots[0]
 if not math.isfinite(r.start_time+r.stop_time) or not 0<r.stop_time-r.start_time<=120:raise ValueError('Unsupported animation duration.')
 return d,r

def channels(path):
 N,_,_=dependencies();_,r=sequence(path);rows=[]
 for index,b in enumerate(r.controlled_blocks):
  i=b.interpolator;data=getattr(i,'data',None)
  supported=isinstance(i,N.NiTransformInterpolator) and data is not None and data.num_rotation_keys>=2 and data.rotation_type==1
  rows.append({'index':index,'bone':b.get_node_name().decode('utf-8','replace'),'supported':supported,'interpolator':type(i).__name__})
 return rows

def motion(u,degrees,cycles):
 # Zero offset and zero offset velocity at both boundaries: no added transition snap.
 return math.radians(degrees)*math.sin(2*math.pi*cycles*u)*math.sin(math.pi*u)**2

def events(r):return [(x.time,x.value.decode('utf-8','replace')) for x in r.text_keys.text_keys] if r.text_keys else []

def generate(mod,source,output,index,axis='X',degrees=2,cycles=1):
 N,_,_=dependencies();root=Path(mod).resolve();source=Path(source).resolve();out=Path(output).resolve()
 try:relative=source.relative_to(root)
 except ValueError:raise ValueError('The KF must be inside the selected mod.')
 if not relative.parts or relative.parts[0].lower()!='assets' or source.suffix.lower()!='.kf':raise ValueError('Choose a KF beneath this mod’s Assets folder.')
 if out==root or root in out.parents:raise ValueError('Export outside the installed mod to keep it unchanged.')
 if out.exists() and any(out.iterdir()):raise ValueError('Choose an empty output folder.')
 if axis not in ('X','Y','Z') or not math.isfinite(float(degrees)) or not 0<=float(degrees)<=15 or int(cycles)!=cycles or not 1<=cycles<=8:raise ValueError('Use a local X/Y/Z axis, 0–15 degrees and 1–8 whole cycles.')
 d,r=sequence(source);rows=channels(source)
 if not 0<=index<len(rows) or not rows[index]['supported']:raise ValueError('This channel is not supported. Choose a LINEAR quaternion track.')
 before_events=events(r);block=r.controlled_blocks[index];interp=block.interpolator
 # Isolate data shared by another controller without affecting that controller.
 new_interp=N.NiTransformInterpolator().deepcopy(interp);new_data=N.NiTransformData().deepcopy(interp.data);new_interp.data=new_data;block.interpolator=new_interp
 keys=[(k.time,quaternion(k.value)) for k in new_data.quaternion_keys]
 if any(not math.isfinite(t) for t,q in keys) or any(keys[j][0]>=keys[j+1][0] for j in range(len(keys)-1)):raise ValueError('Rotation keys must have increasing finite times.')
 if keys[0][0]<r.start_time-1e-4 or keys[-1][0]>r.stop_time+1e-4:raise ValueError('Rotation keys outside the sequence need manual editing.')
 start,stop=r.start_time,r.stop_time;frames=max(2,math.ceil((stop-start)*30));times=sorted(set([start,stop]+[t for t,q in keys]+[start+(stop-start)*i/frames for i in range(frames+1)]));values=[];j=0
 for t in times:
  while j<len(keys)-2 and keys[j+1][0]<t:j+=1
  if t<=keys[0][0]:base=keys[0][1]
  elif t>=keys[-1][0]:base=keys[-1][1]
  else:base=slerp(keys[j][1],keys[j+1][1],(t-keys[j][0])/(keys[j+1][0]-keys[j][0]))
  angle=motion((t-start)/(stop-start),degrees,cycles);delta=[math.cos(angle/2),0,0,0];delta['XYZ'.index(axis)+1]=math.sin(angle/2);q=multiply(base,delta)
  if values and sum(x*y for x,y in zip(values[-1],q))<0:q=[-x for x in q]
  values.append(q)
 new_data.num_rotation_keys=len(times);new_data.quaternion_keys.update_size()
 for key,t,q in zip(new_data.quaternion_keys,times,values):
  key.time=t
  for attr,v in zip(('w','x','y','z'),q):setattr(key.value,attr,v)
 target=out/'patch'/relative;target.parent.mkdir(parents=True,exist_ok=True)
 with target.open('wb') as f:d.write(f)
 _,check=sequence(target)
 if events(check)!=before_events:raise RuntimeError('Event preservation check failed.')
 original=source.read_bytes();backup=out/'backup'/relative;backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(original)
 report={'format':'civ4-motion-layer','version':1,'path':relative.as_posix(),'bone':rows[index]['bone'],'axis':axis,'degrees':degrees,'cycles':cycles,'duration':stop-start,'events':before_events,'originalSHA256':hashlib.sha256(original).hexdigest(),'newSHA256':hashlib.sha256(target.read_bytes()).hexdigest(),'inGameTested':False,'scope':'All units referencing this KF path share the change.'}
 (out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');(out/'INSTALL.txt').write_text('EXPERIMENTAL NATIVE KF MOTION LAYER\nUse a copy of the exact source mod. Check originalSHA256 in manifest.json before replacing the file. Copy patch/ into that copy. Restore backup/ to roll back.\nThe existing KFM continues referencing the same KF filename. No XML/KFM routing is changed; ALL units using this KF share the motion change.\nOnly the selected bone rotation channel changed. Unselected tracks, duration and event markers are preserved. Editing a root bone can alter root motion. No foot/hand contact solver or collision testing is provided. Test transitions, clipping and event timing in Civ IV.\n')
 return report

def gui():
 import tkinter as tk
 from tkinter import ttk,filedialog,messagebox
 w=tk.Tk();w.title('Civ IV — Native Motion Lab');w.geometry('800x650');f=ttk.Frame(w,padding=18);f.pack(fill='both',expand=True);f.columnconfigure(1,weight=1)
 mod=tk.StringVar();kf=tk.StringVar();output=tk.StringVar();axis=tk.StringVar(value='X');amp=tk.DoubleVar(value=2);cycles=tk.IntVar(value=1);rows=[];scanned=None
 ttk.Label(f,text='Add a controlled motion layer to an existing KF',font=('',13,'bold')).grid(row=0,column=0,columnspan=3,sticky='w',pady=10)
 def field(row,label,var,folder):
  ttk.Label(f,text=label).grid(row=row,column=0,sticky='w');ttk.Entry(f,textvariable=var).grid(row=row,column=1,sticky='ew',padx=8)
  def choose():
   p=filedialog.askdirectory() if folder else filedialog.askopenfilename(filetypes=[('Civ IV keyframes','*.kf')])
   if p:var.set(p)
  ttk.Button(f,text='Browse',command=choose).grid(row=row,column=2)
 field(1,'Mod folder',mod,True);field(2,'Source KF',kf,False);field(3,'Empty output folder',output,True)
 box=ttk.Combobox(f,state='readonly');box.grid(row=5,column=0,columnspan=3,sticky='ew',pady=8)
 def scan():
  nonlocal rows,scanned
  scanned=None;rows=[];box.set('');box['values']=[]
  try:
   rows=[r for r in channels(kf.get()) if r['supported']];scanned=(str(Path(kf.get()).resolve()),hashlib.sha256(Path(kf.get()).read_bytes()).hexdigest());box['values']=[r['bone']+' — channel '+str(r['index']) for r in rows]
   if rows:box.current(next((i for i,r in enumerate(rows) if r['bone'].lower().endswith('spine')),0))
   else:raise ValueError('No editable LINEAR quaternion tracks. Compressed, Euler and TBC tracks need another editor.')
  except Exception as e:messagebox.showerror('Cannot read animation',str(e))
 ttk.Button(f,text='Find editable bone tracks',command=scan).grid(row=4,column=0,columnspan=3,sticky='w',pady=8)
 ttk.Label(f,text='Local rotation axis').grid(row=6,column=0);ttk.Combobox(f,textvariable=axis,values=['X','Y','Z'],state='readonly').grid(row=6,column=1,sticky='ew')
 ttk.Label(f,text='Maximum offset (degrees)').grid(row=7,column=0);ttk.Scale(f,variable=amp,from_=0,to=15).grid(row=7,column=1,sticky='ew');ttk.Label(f,textvariable=amp).grid(row=7,column=2)
 ttk.Label(f,text='Whole cycles').grid(row=8,column=0);ttk.Spinbox(f,textvariable=cycles,from_=1,to=8).grid(row=8,column=1,sticky='ew')
 cv=tk.Canvas(f,height=120,background='#172124',highlightthickness=0);cv.grid(row=9,column=0,columnspan=3,sticky='ew',pady=12)
 def draw(*args):
  cv.delete('all');width=max(cv.winfo_width(),400);cv.create_line(0,60,width,60,fill='#6e8183')
  try:pts=[v for i in range(201) for v in (i*width/200,60-math.degrees(motion(i/200,amp.get(),cycles.get()))*3)];cv.create_line(*pts,fill='#edbf75',width=2)
  except (ValueError,tk.TclError):pass
 cv.bind('<Configure>',draw);amp.trace_add('write',draw);cycles.trace_add('write',draw)
 ttk.Label(f,text='Curve shows added rotation, not a 3D animation preview. Match the local axis to your donor.\nStart small on spine/neck tracks; avoid contact limbs until checked in game.\nThe patch affects every unit sharing the KF. Event times and other tracks stay unchanged.',wraplength=730).grid(row=10,column=0,columnspan=3,sticky='w')
 def export():
  try:
   if box.current()<0:raise ValueError('Select an editable bone track.')
   if scanned!=(str(Path(kf.get()).resolve()),hashlib.sha256(Path(kf.get()).read_bytes()).hexdigest()):raise ValueError('Source changed. Find editable tracks again.')
   r=generate(mod.get(),kf.get(),output.get(),rows[box.current()]['index'],axis.get(),amp.get(),cycles.get());messagebox.showinfo('Motion patch prepared','Wrote native KF patch and backup for '+r['bone']+'. Test in a copy of the mod.')
  except Exception as e:messagebox.showerror('Cannot export',str(e))
 ttk.Button(f,text='Export native KF patch + backup',command=export).grid(row=11,column=0,columnspan=3,sticky='ew',pady=15);w.mainloop()
if __name__=='__main__':gui()
