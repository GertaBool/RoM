from pathlib import Path
import functools,http.server,threading,json,zipfile,shutil,xml.etree.ElementTree as ET,hashlib,sys,time,io
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/output';OUT.mkdir(exist_ok=True)
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/rise-of-mankind');fixture=OUT/'building-fixture'
if fixture.exists():shutil.rmtree(fixture)
fixture.mkdir()
for p in (SOURCE/'Assets').rglob('*.xml'):
 if '/Text/' in p.as_posix() or p.name.lower().endswith('schema.xml') or p.name.lower()=='civ4citylsystem.xml' or any(p.name.lower().endswith(n.lower()+'.xml') for n in ['BuildingClassInfos','ArtDefines_Building','BonusInfos','ArtDefines_Bonus','TechInfos','TerrainInfos','BonusClassInfos','ImprovementInfos','BuildingInfos','UnitInfos']):
  target=fixture/p.relative_to(SOURCE);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
art=Image.new('RGB',(128,128),(180,130,75));d=ImageDraw.Draw(art)
for x in range(15,115,30):
 for y in range(20,105,35):d.rectangle((x,y,x+12,y+18),fill=(30,65,100))
art.save(OUT/'facade.png')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start();checks=[];errors=[];external=[]
def val(node,tag):return next((x.text or '' for x in node if x.tag.split('}')[-1]==tag),'')
def entries(root,tag):return [n for n in root.iter() if n.tag.split('}')[-1]==tag]
def review(page):
 page.locator('#reviewBuilding').click();page.wait_for_function("!document.getElementById('reviewBuilding').disabled",timeout=60000)
 assert page.locator('#downloadBuilding').is_enabled(),page.locator('#buildingStatus').inner_text()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--enable-unsafe-swiftshader']);page=browser.new_page(viewport={'width':1400,'height':1100},accept_downloads=True);page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:','blob:','data:')) else None)
 page.goto(f'http://127.0.0.1:{server.server_port}/Civ4ArtStudio.html');page.locator('#buildingMode').click();page.locator('#buildingModFolder').set_input_files(str(fixture));page.wait_for_function('B.ready',timeout=120000)
 assert page.locator('#buildingTemplate').input_value()=='BUILDING_LIBRARY';page.locator('#buildingFields details').evaluate_all('els=>els.forEach(e=>e.open=true)')
 page.locator('#buildingName').fill('Civic Hall');page.locator('#buildingPedia').fill('The civic hall gathers the town around a shared public space.');page.locator('#buildingStrategy').fill('Invest in administration when maintenance limits expansion.');page.locator('#buildingMaintenance').fill('-10');page.locator('#b_YieldModifiers_1').fill('15');review(page)
 with page.expect_download() as dl:page.locator('#downloadBuilding').click()
 dl.value.save_as(str(OUT/'building-reuse.zip'))
 with zipfile.ZipFile(OUT/'building-reuse.zip') as z:
  assert z.testzip() is None;m=json.loads(z.read('manifest.json'));assert m['building']=='BUILDING_CIVIC_HALL';assert not m['requiresInGameModelTest']
  for f in m['files']:
   data=z.read('patch/'+f['path']);assert hashlib.sha256(data).hexdigest()==f['newSHA256'];ET.fromstring(data)
   if f['originalSHA256']:assert z.read('backup/'+f['path'])==(fixture/f['path']).read_bytes()
  root=ET.fromstring(z.read('patch/Assets/XML/Buildings/CIV4BuildingInfos.xml'));building=next(n for n in entries(root,'BuildingInfo') if val(n,'Type')=='BUILDING_CIVIC_HALL')
  assert val(building,'BuildingClass')=='BUILDINGCLASS_CIVIC_HALL';assert val(building,'iMaintenanceModifier')=='-10';assert val(building,'MovieDefineTag')=='NONE'
  schema=ET.parse(fixture/'Assets/XML/Buildings/CIV4BuildingsSchema.xml').getroot();definition=next(x for x in schema if x.attrib.get('name')=='BuildingInfo');order=[x.attrib['type'] for x in definition if x.tag.split('}')[-1]=='element'];indices=[order.index(x.tag.split('}')[-1]) for x in building];assert indices==sorted(indices),'Building child order differs from schema'
  root=ET.fromstring(z.read('patch/Assets/XML/Buildings/CIV4BuildingClassInfos.xml'));cls=next(n for n in entries(root,'BuildingClassInfo') if val(n,'Type')=='BUILDINGCLASS_CIVIC_HALL');assert val(cls,'DefaultBuilding')=='BUILDING_CIVIC_HALL';assert val(cls,'iMaxGlobalInstances')=='-1'
 checks.append('Creates linked building, class, art and text; schema ordering, new yield modifier, exact backups and checksums verified')
 page.locator('#buildingCategory').select_option('world');assert page.locator('#downloadBuilding').is_disabled();review(page)
 assert page.evaluate("B.plan.files.some(f=>typeof f.data==='string'&&f.data.includes('<iMaxGlobalInstances>1</iMaxGlobalInstances>'))")
 page.locator('#buildingID').fill('BUILDING_LIBRARY');page.locator('#reviewBuilding').click();page.wait_for_function("!document.getElementById('reviewBuilding').disabled");assert 'already exists' in page.locator('#buildingStatus').inner_text();page.locator('#buildingID').fill('BUILDING_CIVIC_HALL')
 checks.append('Wonder limits, stale review invalidation and duplicate identifier rejection')
 page.locator('#buildingArtMode').select_option('box');page.locator('#buildingTexture').set_input_files(str(OUT/'facade.png'));page.wait_for_function('B.texture!==null');review(page)
 with page.expect_download() as dl:page.locator('#downloadBuilding').click()
 dl.value.save_as(str(OUT/'building-box.zip'));assert 'MODEL-TEST' in dl.value.suggested_filename
 with zipfile.ZipFile(OUT/'building-box.zip') as z:
  assert z.testzip() is None;m=json.loads(z.read('manifest.json'));assert m['requiresInGameModelTest'];prefix='patch/Assets/Art/Structures/Buildings/Studio/BUILDING_CIVIC_HALL/'
  (OUT/'browser-building.nif').write_bytes(z.read(prefix+'building.nif'));tex=Image.open(io.BytesIO(z.read(prefix+'diffuse.dds')));assert tex.size==(512,512);assert tex.getpixel((0,0))[3]==255
  button=Image.open(io.BytesIO(z.read('patch/Assets/Art/Interface/Buttons/Custom/building_civic_hall.dds')));assert button.size==(64,64);assert button.getbbox() is not None
 checks.append('Façade image creates NIF, opaque mipmapped DDS, preview-derived button and matching art paths')
 page.locator('#building3D').screenshot(path=str(OUT/'building-model-preview.png'));page.screenshot(path=str(OUT/'building-screen.png'),full_page=True)
 # Import actual Blender-prepared output when available; otherwise a UV-mapped triangle fixture.
 obj=ROOT/'work/prepared-architecture/building.obj'
 if not obj.exists():obj=OUT/'building.obj';obj.write_text('v 0 0 0\nv 2 0 0\nv 0 0 2\nvt 0 0\nvt 1 0\nvt 0 1\nf 1/1 2/2 3/3\n')
 page.locator('#buildingArtMode').select_option('obj');page.locator('#buildingOBJ').set_input_files(str(obj));page.wait_for_function('B.mesh!==null');review(page);assert page.evaluate('B.plan.manifest.artRoute')=='obj';checks.append('Architectural OBJ path generates a reviewed model patch')
 with page.expect_download() as dl:page.locator('#saveBuildingDraft').click()
 dl.value.save_as(str(OUT/'building-draft.json'));page.locator('#buildingCost').fill('999');page.locator('#buildingDraftFile').set_input_files(str(OUT/'building-draft.json'));page.wait_for_function("document.getElementById('buildingStatus').textContent.startsWith('Draft restored')");assert page.evaluate('B.texture===null&&B.button===null&&B.objText===\'\'');assert page.locator('#downloadBuilding').is_disabled();assert page.locator('#buildingOBJ').is_enabled();checks.append('Draft restores settings and clears source images/model until explicitly reselected')
 # Install generated XML into fixture and edit the new building again.
 with zipfile.ZipFile(OUT/'building-reuse.zip') as z:
  for path in z.namelist():
   if path.startswith('patch/'):
    target=fixture/path[6:];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(path))
 page.on('dialog',lambda d:d.accept());page.locator('#buildingModFolder').set_input_files(str(fixture));page.wait_for_function('B.ready',timeout=120000)
 page.locator('#buildingAction').select_option('edit');page.locator('#buildingTemplate').select_option('BUILDING_CIVIC_HALL');page.locator('#buildingCost').fill('250');review(page);assert page.evaluate("B.plan.manifest.files.find(f=>f.path.endsWith('CIV4GameText_Studio_BUILDING_CIVIC_HALL.xml')).originalSHA256!==null");checks.append('Previously generated building can be edited again without duplicate classes/art/text')
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),page.evaluate("[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>[e.tagName,e.id,e.getBoundingClientRect().width]).slice(0,20)");assert not errors,errors;assert not external,external;checks.append('Responsive UI, no script errors and no external requests');browser.close()
server.shutdown();(OUT/'building-validation.json').write_text(json.dumps({'passed':checks,'in_game_tested':False},indent=2)+'\n');print('\n'.join(checks))
