"""Coffee chain installer. No dependencies beyond Python 3; no arguments opens a folder chooser."""
from pathlib import Path
import argparse,datetime,hashlib,json,re,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def prepare(root):
 ops=json.loads((P/'changes.json').read_text(encoding='utf-8'));manifest=json.loads((P/'manifest.json').read_text());changes=[];skipped=[]
 assert sha((P/'changes.json').read_bytes())==manifest['changes_sha256'],'Damaged changes.json'
 paths=sorted(set(e['path'] for e in ops))
 for path in paths:
  items=[e for e in ops if e['path']==path];target=root/path
  if not target.exists() and all(e.get('optional') for e in items):skipped.append(path);continue
  old=target.read_bytes();m=re.search(br'encoding=["\']([^"\']+)',old[:150]);enc=m.group(1).decode() if m else 'utf-8';text=old.decode(enc)
  for e in items:
   if e['kind']=='replace':
    if text.count(e['old'])!=1:raise ValueError('Conflicting or already installed entry: '+e['key']+' in '+path+'. Nothing written. Rebase this entry before installing.')
    text=text.replace(e['old'],e['new'],1)
   else:
    if re.search(r'<(?:Type|Tag)>\s*'+re.escape(e['key'])+r'\s*</(?:Type|Tag)>',text):raise ValueError('Identifier already exists: '+e['key'])
    end='</'+e['container']+'>'
    if text.count(end)!=1:raise ValueError('Unexpected XML container: '+path)
    text=text.replace(end,e['new']+'\n\t'+end,1)
  new=text.encode(enc,errors='xmlcharrefreplace');ET.fromstring(new);changes.append((target,new,old))
 for e in manifest['assets']:
  target=root/e['path'];data=(P/'patch'/e['path']).read_bytes()
  if sha(data)!=e['sha256']:raise ValueError('Damaged package: '+e['path'])
  if target.exists():raise ValueError('Asset already exists: '+e['path'])
  if e['path'].endswith('.xml'):ET.fromstring(data)
  changes.append((target,data,None))
 # New IDs must also be unique in user-added modules and other XML files.
 newids=[e['key'] for e in ops if e['kind']=='append']+['TXT_KEY_BONUS_ROASTED_COFFEE','TXT_KEY_BONUS_ROASTED_COFFEE_PEDIA','TXT_KEY_BUILDING_COFFEE_ROASTERY_STRATEGY']
 pattern=re.compile(rb'<(?:Type|Tag)>\s*('+b'|'.join(k.encode('ascii') for k in newids)+rb')\s*</(?:Type|Tag)>')
 for f in (root/'Assets').rglob('*.xml'):
  m=pattern.search(f.read_bytes())
  if m:raise ValueError('Identifier collision in '+str(f)+': '+m.group(1).decode())
 return changes,skipped
def install(root,apply=False):
 changes,skipped=prepare(root);report='Validated %s files. Optional modules absent: %s.'%(len(changes),len(skipped))
 if not apply:return report+' Check only; no files changed.'
 backup=root/('CoffeeChain-backup-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'));backup.mkdir()
 for target,data,old in changes:
  if old is not None:
   f=backup/target.relative_to(root);f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(old)
 journal=[dict(path=t.relative_to(root).as_posix(),new_sha256=sha(data),existed=old is not None) for t,data,old in changes];(backup/'restore.json').write_text(json.dumps(journal,indent=2))
 written=[]
 try:
  for target,data,old in changes:target.parent.mkdir(parents=True,exist_ok=True);written.append((target,old));target.write_bytes(data)
 except Exception:
  for target,old in reversed(written):
   if old is None:target.unlink(missing_ok=True)
   else:target.write_bytes(old)
  raise
 return report+' Installed. Backup: '+str(backup)
def gui():
 import tkinter as tk
 from tkinter import filedialog,messagebox
 w=tk.Tk();w.withdraw();folder=filedialog.askdirectory(title='Select a COPY of your Rise of Mankind mod folder')
 if not folder:return
 root=Path(folder).resolve()
 try:
  report=install(root)
  if messagebox.askyesno('Coffee processing chain',report+'\n\nInstall Coffee Beans → Coffee Roastery → Roasted Coffee?\nUse a new game. Backups will be created.\n\n'+str(root)):messagebox.showinfo('Installed',install(root,True))
 except Exception as e:messagebox.showerror('Installation stopped',str(e))
 w.destroy()
if __name__=='__main__':
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('mod',nargs='?',type=Path);a.add_argument('--apply',action='store_true');args=a.parse_args()
 if args.mod:print(install(args.mod.resolve(),args.apply))
 else:gui()
