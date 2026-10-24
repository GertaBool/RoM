"""Desktop companion: external image reconstruction -> GLB -> Civ IV rig transfer."""
import hashlib,json,os,shutil,subprocess,sys,threading,webbrowser,xml.etree.ElementTree as ET
from pathlib import Path
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
HERE=Path(__file__).resolve().parent

def catalog(mod):
 root=Path(mod).resolve();assets=root/'Assets'
 if not assets.is_dir():raise ValueError('Select a mod folder containing Assets.')
 files={p.relative_to(root).as_posix().lower():p for p in assets.rglob('*') if p.is_file()};rows=[]
 for path in files.values():
  if not path.name.lower().endswith('artdefines_unit.xml'):continue
  raw=path.read_bytes()
  if len(raw)>40*1024*1024 or b'<!DOCTYPE' in raw or b'<!ENTITY' in raw:raise ValueError('Unsupported XML: '+str(path))
  tree=ET.fromstring(raw)
  for n in tree.iter():
   if n.tag.split('}')[-1]!='UnitArtInfo':continue
   v={c.tag.split('}')[-1]:(c.text or '').strip() for c in n}
   nif=v.get('NIF','');loose=files.get(('Assets/'+nif).lower())
   if loose and v.get('KFM') not in ('',None,'NONE'):
    rows.append(dict(type=v.get('Type'),path=path.relative_to(root).as_posix(),nif=nif,kfm=v['KFM'],shader=v.get('SHADERNIF',''),file=str(loose)))
 return rows

def prepare(mod,blender,model,output,unit,donor,animation,mesh_index,rotation=0,keep=True,size=512,triangles=2500,simplify=False,allow_alpha=False,allow_normals=False):
 import unit_model_convert as converter
 if (donor['nif'].lower(),donor['shader'].lower())!=(animation['nif'].lower(),animation['shader'].lower()):raise ValueError('Animation selection is not an existing pairing for this donor.')
 if not output.strip():raise ValueError('Choose an empty output folder.')
 if not any(r==donor for r in catalog(mod)):raise ValueError('Donor selection is stale. Scan the selected mod again.')
 out=Path(output).resolve()
 if out.exists() and any(out.iterdir()):raise ValueError('Choose an empty output folder.')
 if Path(model).suffix.lower() not in ('.glb','.gltf','.fbx','.obj','.blend'):raise ValueError('Import a reconstructed GLB, glTF, FBX, OBJ or Blender model.')
 if not Path(blender).is_file():raise ValueError('Select the Blender executable (Blender 4.x).')
 out.mkdir(parents=True,exist_ok=True);baked=out/'prepared';baked.mkdir()
 cmd=[str(blender),'--background','--threads','2','--python-exit-code','1','--python',str(HERE/'prepare_building.py'),'--',str(Path(model).resolve()),str(baked),'--size',str(size),'--triangles',str(triangles)]
 if simplify:cmd.append('--simplify')
 if allow_alpha:cmd.append('--allow-alpha-flatten')
 if allow_normals:cmd.append('--allow-normal-loss')
 run=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace');(out/'blender.log').write_text(run.stdout,encoding='utf-8')
 if run.returncode:
  reasons=__import__('re').findall(r'RuntimeError: ([^\n]+)',run.stdout)
  reason=reasons[-1][:700] if reasons else 'Blender preparation failed.'
  raise ValueError(reason+' See blender.log; use a fresh output folder after fixing the model or changing the explicit loss options.')
 preparation=json.loads((baked/'preparation.json').read_text())
 if preparation['triangles']>10000:raise ValueError('Source exceeds the unit exporter’s 10,000-triangle limit. Review it in Blender and explicitly choose budget simplification if appropriate. No NIF was produced.')
 report=converter.convert(donor['file'],baked,out,unit,mesh_index,rotation,keep)
 d={k:v for k,v in donor.items() if k!='file'};a={k:v for k,v in animation.items() if k!='file'}
 manifest={'format':'civ4-reconstructed-unit','version':1,'unit':unit,'donor':d,'animation':a,'report':report,'preparation':preparation,'files':{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in ['model.nif','diffuse.dds']}}
 (out/'model.json').write_text(json.dumps(manifest,indent=2)+'\n');(out/'READ-ME.txt').write_text('EXPERIMENTAL RIG TRANSFER\nImport this folder in Art Studio Units > Prepared reconstructed model.\nThe GLB is genuinely new geometry; the selected donor skeleton, bind matrices and animation dependencies are retained.\nAutomatic weights need a similar body/rest pose. Inspect all movement, combat and death animations in game. Meshy/Tripo animations are not converted into Civ IV KF files.\nKeep the source mod installed: animation and retained material/weapon dependencies are not redistributed.\nThe main body is uniformly fitted to the donor height; other body parts/weapons are retained unless disabled.\n')
 return manifest

def gui():
 w=tk.Tk();w.title('Civ IV — Image to Unit Model');w.geometry('950x850');w.minsize(760,680)
 viewport=tk.Canvas(w,highlightthickness=0);scroll=ttk.Scrollbar(w,orient='vertical',command=viewport.yview);scroll.pack(side='right',fill='y');viewport.pack(side='left',fill='both',expand=True);viewport.configure(yscrollcommand=scroll.set);frame=ttk.Frame(viewport,padding=16);window=viewport.create_window((0,0),window=frame,anchor='nw');frame.bind('<Configure>',lambda e:viewport.configure(scrollregion=viewport.bbox('all')));viewport.bind('<Configure>',lambda e:viewport.itemconfigure(window,width=e.width));frame.columnconfigure(1,weight=1)
 vals={k:tk.StringVar() for k in ['image','mod','model','blender','output','unit']};vals['unit'].set('UNIT_NEW_MODEL');vals['blender'].set(shutil.which('blender') or '')
 for pattern in ['C:/Program Files/Blender Foundation/Blender 4.*/blender.exe']:
  hits=sorted(__import__('glob').glob(pattern))
  if hits and not vals['blender'].get():vals['blender'].set(hits[-1])
 row=0
 def heading(text):
  nonlocal row
  ttk.Label(frame,text=text,font=('',12,'bold')).grid(row=row,column=0,columnspan=3,sticky='w',pady=(12,6));row+=1
 def field(label,key,directory=False,filetypes=None):
  nonlocal row
  ttk.Label(frame,text=label).grid(row=row,column=0,sticky='w');ttk.Entry(frame,textvariable=vals[key]).grid(row=row,column=1,sticky='ew',padx=8)
  def browse():
   p=filedialog.askdirectory() if directory else filedialog.askopenfilename(filetypes=filetypes or [('All files','*')])
   if p:vals[key].set(p)
  ttk.Button(frame,text='Browse',command=browse).grid(row=row,column=2);row+=1
 heading('Inspect the actual unit · Textured animation playback')
 def open_shape():
  exe=vals['blender'].get()
  if not Path(exe).is_file():messagebox.showerror('Blender required','Select the Blender executable below first.');return
  subprocess.Popen([exe,'--python',str(HERE/'shape_lab.py')])
 def open_motion():subprocess.Popen([sys.executable,str(HERE/'motion_lab.py')])
 def open_preview():subprocess.Popen([sys.executable,str(HERE/'unit_animation_preview.py')])
 internal=ttk.Frame(frame);internal.grid(row=row,column=0,columnspan=3,sticky='w');row+=1
 ttk.Button(internal,text='Preview textured NIF + animations',command=open_preview).pack(side='left',padx=4);ttk.Button(internal,text='Edit native KF tracks',command=open_motion).pack(side='left',padx=4)
 ttk.Label(frame,text='Preview the original unit or your exported model.nif with the donor’s KF clips. Inspect its body, equipment and animation before using it in game.',wraplength=850).grid(row=row,column=0,columnspan=3,sticky='w');row+=1
 ttk.Button(frame,text='Optional blockout utility (not finished unit art)',command=open_shape).grid(row=row,column=0,columnspan=3,sticky='w');row+=1
 heading('1 · Load a finished model, or reconstruct from an image externally')
 field('Reference image','image',filetypes=[('Images','*.png *.jpg *.jpeg')])
 def external(url):
  if not vals['image'].get():messagebox.showinfo('Choose an image','Select a reference image first.');return
  messagebox.showinfo('External reconstruction','Upload your selected image in the provider website, then download a textured GLB.\n\nFor humanoids, use a neutral A/T pose with limbs separated, facing forward.\nProvider accounts, charges and upload terms apply. This companion does not upload anything automatically.');webbrowser.open(url)
 bar=ttk.Frame(frame);bar.grid(row=row,column=0,columnspan=3,sticky='w');ttk.Button(bar,text='Open Meshy image-to-3D',command=lambda:external('https://www.meshy.ai/')).pack(side='left',padx=4);ttk.Button(bar,text='Open Tripo image-to-3D',command=lambda:external('https://www.tripo3d.ai/')).pack(side='left',padx=4);row+=1
 field('Reconstructed model','model',filetypes=[('3D models','*.glb *.gltf *.fbx *.obj *.blend')])
 heading('2 · Choose a Civ IV donor and known animation pairing')
 field('Mod folder','mod',True);donorbox=ttk.Combobox(frame,state='readonly');animbox=ttk.Combobox(frame,state='readonly');meshbox=ttk.Combobox(frame,state='readonly');rows=[];anims=[];meshes=[]
 def choose_donor(event=None):
  nonlocal anims,meshes
  meshes=[];anims=[];meshbox.set('');meshbox['values']=[];animbox.set('');animbox['values']=[]
  try:
   import unit_model_convert as converter
   d=rows[donorbox.current()];anims=[r for r in rows if (r['nif'].lower(),r['shader'].lower())==(d['nif'].lower(),d['shader'].lower())];animbox['values']=[r['kfm']+' — '+r['type'] for r in anims];animbox.current(0);meshes=converter.meshes(d['file']);meshbox['values']=[f'{n} ({v} vertices)' for _,n,v in meshes]
   if not meshes:raise ValueError('No skinned mesh found. Choose a different donor.')
   meshbox.current(max(range(len(meshes)),key=lambda i:meshes[i][2]));status.set('Choose the donor body mesh. Match the generated model’s body plan and rest pose. Exact NIF pairings are evidence, not a deformation test.')
  except ImportError:messagebox.showerror('Dependencies missing','Install the companion requirements first:\npython -m pip install -r helpers/unit-model-requirements.txt')
  except Exception as e:messagebox.showerror('Cannot use donor',str(e))
 def scan():
  nonlocal rows
  try:
   rows=catalog(vals['mod'].get());donorbox['values']=[r['type']+' — '+r['path'] for r in rows]
   if not rows:raise ValueError('No animated donor NIFs found as loose files. Extract required game art first; FPK archives are not read here.')
   donorbox.current(0);choose_donor()
  except Exception as e:messagebox.showerror('Scan failed',str(e))
 ttk.Button(frame,text='Scan donor models',command=scan).grid(row=row,column=0,columnspan=3,sticky='w',pady=5);row+=1
 for label,box in [('Donor model',donorbox),('Animation set',animbox),('Body mesh to replace',meshbox)]:ttk.Label(frame,text=label).grid(row=row,column=0,sticky='w');box.grid(row=row,column=1,columnspan=2,sticky='ew',padx=8,pady=3);row+=1
 donorbox.bind('<<ComboboxSelected>>',choose_donor)
 keep=tk.BooleanVar(value=True);ttk.Checkbutton(frame,text='Keep other donor meshes (weapons, equipment and attachments)',variable=keep).grid(row=row,column=0,columnspan=3,sticky='w');row+=1
 heading('3 · Bake, transfer weights and prepare the import folder')
 field('Blender 4.x executable','blender');field('Empty output folder','output',True);ttk.Label(frame,text='Art Studio unit ID').grid(row=row,column=0,sticky='w');ttk.Entry(frame,textvariable=vals['unit']).grid(row=row,column=1,columnspan=2,sticky='ew',padx=8);row+=1
 settings=ttk.Frame(frame);settings.grid(row=row,column=0,columnspan=3,sticky='w');row+=1
 angle=tk.StringVar(value='0');budget=tk.StringVar(value='2500');size=tk.StringVar(value='512')
 for label,var,choices in [('Z rotation',angle,['0','90','180','270']),('Triangle target',budget,['1000','2500','5000','10000']),('Texture size',size,['256','512','1024'])]:ttk.Label(settings,text=label).pack(side='left',padx=6);ttk.Combobox(settings,textvariable=var,values=choices,state='readonly',width=8).pack(side='left')
 simplify=tk.BooleanVar(value=False);allow_alpha=tk.BooleanVar(value=False);allow_normals=tk.BooleanVar(value=False)
 for label,var in [('Reduce geometry to triangle target (off preserves source shape)',simplify),('Accept flattening transparency/cutout detail into an opaque texture',allow_alpha),('Accept omitting linked normal/bump detail from the diffuse bake',allow_normals)]:
  ttk.Checkbutton(frame,text=label,variable=var).grid(row=row,column=0,columnspan=3,sticky='w');row+=1
 status=tk.StringVar(value='External generation produces the new shape. Automatic rig transfer is experimental; it cannot guarantee matching poses or clean animation.')
 ttk.Label(frame,textvariable=status,wraplength=850).grid(row=row,column=0,columnspan=3,sticky='w',pady=12);row+=1
 def generate():
  try:
   if donorbox.current()<0 or animbox.current()<0 or meshbox.current()<0:raise ValueError('Scan the mod and select a donor body and animation.')
   args=[vals[k].get() for k in ['mod','blender','model','output','unit']]+[dict(rows[donorbox.current()]),dict(anims[animbox.current()]),meshes[meshbox.current()][0],float(angle.get()),keep.get(),int(size.get()),int(budget.get()),simplify.get(),allow_alpha.get(),allow_normals.get()]
  except Exception as e:messagebox.showerror('Missing selection',str(e));return
  go['state']='disabled';status.set('Baking and transferring skin weights… This may take a few minutes.')
  def worker():
   try:
    report=prepare(*args)
    w.after(0,lambda:status.set('Prepared '+args[4]+' in '+args[3]+': '+str(report['report']['triangles'])+' triangles. Source: '+str(report['preparation']['sourceTriangles'])+'. Open Art Studio → Model review and select the output folder to compare source and prepared geometry. Then import the output folder in Art Studio. TEST IN GAME before using in a campaign.'))
   except Exception as e:
    msg=str(e);w.after(0,lambda:messagebox.showerror('Conversion stopped',msg))
   finally:w.after(0,lambda:go.configure(state='normal'))
  threading.Thread(target=worker,daemon=True).start()
 go=ttk.Button(frame,text='Prepare reconstructed unit model',command=generate);go.grid(row=row,column=0,columnspan=3,sticky='ew');w.mainloop()
if __name__=='__main__':gui()
