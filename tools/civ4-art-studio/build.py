"""Builds dist/Civ4ArtStudio.html from app/, the download Civ4ArtStudio.zip and SHA256SUMS.json.
python build.py writes them; python build.py --check fails if any committed copy differs from a fresh build."""
import hashlib,io,json,sys,zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
# Files in the download besides the app, at these paths inside the ZIP.
EXTRA=['README.md','LICENSE','INTERNAL_ART_PIPELINE.md','UNIT_VISUAL_STUDY.md','building-texture-preview.png','shape-lab-preview.png']

def html():
 page=(root/'app/index.html').read_text()
 for name in ['core.js','app.js','resources.js','mesh.js','surfaces.js','buildings.js','units.js','review.js']:
  js=(root/'app'/name).read_text().replace('</script','<\\/script')
  page=page.replace(f'<script src="{name}"></script>','<script>\n'+js+'\n</script>')
 return page.encode()

def bundle(page):
 files=[('Civ4ArtStudio.html',page)]
 for name in EXTRA:
  data=(root/name).read_bytes()
  # Inside the ZIP the README's download line would point at itself.
  if name=='README.md':data=b''.join(l for l in data.splitlines(True) if not l.startswith(b'[Download the ready-to-use ZIP]'))
  files.append((name,data))
 files+=[('helpers/'+p.name,p.read_bytes()) for p in sorted((root/'helpers').iterdir()) if p.is_file() and p.suffix!='.pyc']
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w') as z:
  for name,data in files:
   info=zipfile.ZipInfo(name,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
   z.writestr(info,data,compresslevel=9)
 return out.getvalue()

def build():
 page=html();z=bundle(page)
 sums={'Civ4ArtStudio.zip':hashlib.sha256(z).hexdigest(),'dist/Civ4ArtStudio.html':hashlib.sha256(page).hexdigest()}
 return {'dist/Civ4ArtStudio.html':page,'Civ4ArtStudio.zip':z,'SHA256SUMS.json':(json.dumps(sums,indent=2)+'\n').encode()}

if __name__=='__main__':
 outputs=build()
 if '--check' in sys.argv:
  stale=[n for n,data in outputs.items() if not (root/n).exists() or (root/n).read_bytes()!=data]
  if stale:sys.exit('Out of date, run python build.py: '+', '.join(stale))
  print('Built files match app/ and the documents.')
 else:
  (root/'dist').mkdir(exist_ok=True)
  for n,data in outputs.items():(root/n).write_bytes(data)
  print('Built',', '.join(outputs))
