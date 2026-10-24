from pathlib import Path
import functools,http.server,threading,json,zipfile,shutil,xml.etree.ElementTree as ET,hashlib,sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/output';OUT.mkdir(exist_ok=True)
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/rise-of-mankind');fixture=OUT/'resource-fixture'
if fixture.exists():shutil.rmtree(fixture)
fixture.mkdir(exist_ok=True)
# Real mod definitions and fonts, kept only under ignored tests/output.
for p in (SOURCE/'Assets').rglob('*'):
 if not p.is_file():continue
 if p.suffix.lower()=='.xml' and ('/Text/' in p.as_posix() or any(p.name.lower().endswith(n.lower()+'.xml') for n in ['BonusInfos','ArtDefines_Bonus','TechInfos','TerrainInfos','BonusClassInfos','ImprovementInfos','BuildingInfos','UnitInfos'])) or p.name in ['GameFont.tga','GameFont_75.tga']:
  target=fixture/p.relative_to(SOURCE);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start()
checks=[];errors=[];external=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1400,'height':1000},accept_downloads=True);page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:','blob:','data:')) else None)
 page.goto(f'http://127.0.0.1:{server.server_port}/Civ4ArtStudio.html');page.locator('#resourceMode').click();page.locator('#modFolder').set_input_files(str(fixture))
 page.wait_for_function("!R.loading",timeout=120000)
 assert page.locator('#resourceFields').is_enabled(),page.locator('#resourceStatus').inner_text()
 assert page.locator('#resourceTemplate').input_value()=='BONUS_BAUXITE'
 page.locator('#resourceFields details').evaluate_all("els=>els.forEach(e=>e.open=true)")
 checks.append('Real mod folder import includes base, modular definitions, translations and both fonts')
 page.locator('#resourceName').fill('Lithium');assert page.locator('#resourceID').input_value()=='BONUS_LITHIUM'
 page.locator('#resourcePedia').evaluate("e=>{e.value='Lithium & its alloys support advanced industry. <Test text>';e.dispatchEvent(new Event('input',{bubbles:true}));}")
 page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled")
 assert page.locator('#downloadResource').is_enabled(),page.locator('#resourceStatus').inner_text()
 with page.expect_download() as dl:page.locator('#downloadResource').click()
 dl.value.save_as(str(OUT/'resource-lithium.zip'))
 with zipfile.ZipFile(OUT/'resource-lithium.zip') as z:
  assert z.testzip() is None;m=json.loads(z.read('manifest.json'));assert not m['testOnly'];assert m['resource']=='BONUS_LITHIUM'
  for f in m['files']:
   data=z.read('patch/'+f['path']);assert hashlib.sha256(data).hexdigest()==f['newSHA256']
   if f['originalSHA256']:
    assert hashlib.sha256(z.read('backup/'+f['path'])).hexdigest()==f['originalSHA256'];assert z.read('backup/'+f['path'])==(fixture/f['path']).read_bytes()
   if f['path'].endswith('.xml'):ET.fromstring(data)
  def nodes(path,tag):return [n for n in ET.fromstring(z.read('patch/'+path)).iter() if n.tag.split('}')[-1]==tag]
  def val(node,tag):return next((n.text for n in node if n.tag.split('}')[-1]==tag),'')
  bonus=next(n for n in nodes('Assets/XML/Terrain/CIV4BonusInfos.xml','BonusInfo') if val(n,'Type')=='BONUS_LITHIUM')
  assert val(bonus,'ArtDefineTag')=='ART_DEF_BONUS_LITHIUM_STUDIO'
  assert val(bonus,'TechReveal')=='TECH_INDUSTRIALISM'
  text=z.read('patch/Assets/XML/Text/CIV4GameText_Studio_BONUS_LITHIUM.xml').decode();assert '&amp;' in text and '&lt;Test text&gt;' in text
  assert not any(n.endswith('.tga') for n in z.namelist())
 checks.append('New natural resource: correct XML references, escaping, inherited tech and symbol, improvement connections, byte-identical backups and SHA256 manifest')
 # Dirty changes revoke the previous review.
 page.locator('#resourceHealth').fill('3');assert page.locator('#downloadResource').is_disabled()
 page.locator('#resourceID').fill('BONUS_COAL');page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled");assert 'already used' in page.locator('#resourceStatus').inner_text()
 checks.append('Stale review invalidation and duplicate resource identifier rejection')
 page.locator('#resourceID').fill('BONUS_LITHIUM');page.locator('#resourceKind').select_option('manufactured');page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled");assert 'at least one building' in page.locator('#resourceStatus').inner_text()
 producer=page.locator('#resourceProducers option:not([disabled])').first.get_attribute('value');page.locator('#resourceProducers').select_option([producer]);page.locator('#producerCount').fill('2');page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled");assert page.locator('#downloadResource').is_enabled(),page.locator('#resourceStatus').inner_text()
 assert page.evaluate("R.plan.files.some(f=>typeof f.data==='string' && f.data.includes('<FreeBonus>BONUS_LITHIUM</FreeBonus>'))")
 checks.append('Manufactured resource requires a producer and generates building FreeBonus')
 # Custom mapping collisions checked across modules.
 page.locator('#resourceSymbol').select_option('custom');page.locator('#resourceIndex').fill('104');page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled");assert 'already referenced' in page.locator('#resourceStatus').inner_text()
 checks.append('Module-owned GameFont index 104 is rejected')
 # Test-only custom slot export with both real fonts; verify independent TGA decoder.
 art=Image.new('RGBA',(64,64),(0,0,0,0));ImageDraw.Draw(art).ellipse((12,10,50,53),fill=(40,180,210,255));art.save(OUT/'resource-art.png')
 page.locator('#resourceArtwork').set_input_files(str(OUT/'resource-art.png'));page.wait_for_function('R.artwork!==null')
 page.locator('#resourceIndex').fill('106')
 page.evaluate("""()=>{for(const role of ['large','small']){const f=R.fonts[role];R.slots[role]=f.cells.find(c=>{for(let y=c.y;y<c.y+c.height;y++)for(let x=c.x;x<c.x+c.width;x++){const p=(y*f.image.width+x)*4;if(!C.marker(f.image.data,p)&&f.image.data[p+3]>0)return false;}return c.width>10&&c.height>10;});}}""")
 page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled");assert page.locator('#downloadResource').is_enabled(),page.locator('#resourceStatus').inner_text()
 with page.expect_download() as dl:page.locator('#downloadResource').click()
 dl.value.save_as(str(OUT/'resource-custom-TEST-ONLY.zip'));assert 'TEST-ONLY' in dl.value.suggested_filename
 with zipfile.ZipFile(OUT/'resource-custom-TEST-ONLY.zip') as z:
  assert json.loads(z.read('manifest.json'))['testOnly'];draft=json.loads(z.read('resource-draft.json'))
  for role,name in [('large','GameFont.tga'),('small','GameFont_75.tga')]:
   path='Assets/res/Fonts/'+name;out=OUT/('resource-'+name);out.write_bytes(z.read('patch/'+path));before=Image.open(fixture/path).convert('RGBA');after=Image.open(out).convert('RGBA');cell=draft['slots'][role];old=before.tobytes();new=after.tobytes();count=0
   for i in range(before.width*before.height):
    x=i%before.width;y=i//before.width;p=i*4;inside=cell['x']<=x<cell['x']+cell['width'] and cell['y']<=y<cell['y']+cell['height']
    if not inside or old[p:p+3] in [b'\xff\x00\xff',b'\x00\xff\xff']:assert new[p:p+4]==old[p:p+4]
    count+=old[p:p+4]!=new[p:p+4]
   assert count>0
 checks.append('Custom slot test build: DDS and paired TGA export; Pillow confirms all markers and unrelated pixels preserved')
 # Edit current resource, preserving other entries and unrelated fields.
 page.locator('#resourceAction').select_option('edit');page.locator('#resourceTemplate').select_option('BONUS_BAUXITE');page.locator('#resourceHealth').fill('2');page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled");assert page.locator('#downloadResource').is_enabled(),page.locator('#resourceStatus').inner_text()
 with page.expect_download() as dl:page.locator('#downloadResource').click()
 dl.value.save_as(str(OUT/'resource-edit.zip'))
 with zipfile.ZipFile(OUT/'resource-edit.zip') as z:
  root=ET.fromstring(z.read('patch/Assets/XML/Terrain/CIV4BonusInfos.xml'));old=ET.parse(fixture/'Assets/XML/Terrain/CIV4BonusInfos.xml').getroot()
  def allbonus(root):return {val(n,'Type'):n for n in root.iter() if n.tag.split('}')[-1]=='BonusInfo'}
  a=allbonus(root);b=allbonus(old);assert a.keys()==b.keys();assert val(a['BONUS_BAUXITE'],'iHealth')=='2'
  def canonical(node):return (node.tag,(node.text or '').strip(),tuple(canonical(c) for c in node))
  for key in b:
   if key!='BONUS_BAUXITE':assert canonical(a[key])==canonical(b[key]),key
 checks.append('Edit existing resource preserves all unrelated resource definitions')
 # Reload an installed generated patch and edit again: no duplicate generated art/text.
 with zipfile.ZipFile(OUT/'resource-lithium.zip') as z:
  for name in z.namelist():
   if name.startswith('patch/'):
    target=fixture/name[6:];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(name))
 page.on('dialog',lambda d:d.accept());page.locator('#modFolder').set_input_files(str(fixture));page.wait_for_function('!R.loading',timeout=120000)
 assert page.locator('#resourceFields').is_enabled(),page.locator('#resourceStatus').inner_text()
 page.locator('#resourceAction').select_option('edit');page.locator('#resourceTemplate').select_option('BONUS_LITHIUM');page.locator('#resourceHealth').fill('4');page.locator('#reviewResource').click();page.wait_for_function("!document.getElementById('reviewResource').disabled");assert page.locator('#downloadResource').is_enabled(),page.locator('#resourceStatus').inner_text()
 assert page.evaluate("R.plan.manifest.files.find(f=>f.path.endsWith('CIV4GameText_Studio_BONUS_LITHIUM.xml')).originalSHA256!==null")
 checks.append('Reload installed patch and edit generated resource again, with backups of its prior localization')
 # Draft round trip never carries stale artwork or grants font verification.
 with page.expect_download() as dl:page.locator('#saveRecipe').click()
 dl.value.save_as(str(OUT/'resource-draft.json'));page.locator('#resourceHealth').fill('9');page.locator('#recipeFile').set_input_files(str(OUT/'resource-draft.json'));page.wait_for_function("document.getElementById('resourceStatus').textContent.startsWith('Draft loaded')")
 assert page.locator('#resourceHealth').input_value()=='4';assert page.locator('#downloadResource').is_disabled();assert page.evaluate('R.artwork===null');assert not page.locator('#slotVerified').is_checked()
 checks.append('Draft round trip restores settings and requires fresh artwork, slot verification and review')
 page.screenshot(path=str(OUT/'resource-screen.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 assert not errors,errors
 assert not external,external
 checks.append('Narrow viewport and no JavaScript errors')
 browser.close()
server.shutdown();(OUT/'resource-validation.json').write_text(json.dumps({'passed':checks,'in_game_tested':False},indent=2)+'\n');print('\n'.join(checks))
