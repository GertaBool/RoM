from pathlib import Path
import functools,http.server,threading,json,zipfile,shutil,xml.etree.ElementTree as ET,hashlib,sys
from PIL import Image
from playwright.sync_api import sync_playwright
import paths
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/output';OUT.mkdir(exist_ok=True)
SOURCE=paths.mod();fixture=OUT/'unit-fixture'
if fixture.exists():shutil.rmtree(fixture)
fixture.mkdir()
for p in (SOURCE/'Assets').rglob('*'):
 if p.is_file() and p.suffix.lower() in ['.xml','.py','.cpp','.h']:
  target=fixture/p.relative_to(SOURCE);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start();checks=[];errors=[];external=[]
def val(n,k):return next((x.text or '' for x in n if x.tag.split('}')[-1]==k),'')
def entries(root,tag):return [n for n in root.iter() if n.tag.split('}')[-1]==tag]
def review(page,success=True):
 print('Review',page.locator('#unitAction').input_value(),page.locator('#unitTemplate').input_value(),flush=True)
 page.locator('#reviewUnit').click();page.wait_for_function('!U.busy',timeout=120000)
 if success:assert page.locator('#downloadUnit').is_enabled(),page.locator('#unitStatus').inner_text()
 else:assert page.locator('#downloadUnit').is_disabled()
def download(page,name):
 with page.expect_download() as dl:page.locator('#downloadUnit').click()
 path=OUT/name;dl.value.save_as(str(path));return path
def node(z,path,tag,typ):return next(n for n in entries(ET.fromstring(z.read('patch/'+path)),tag) if val(n,'Type')==typ)
def load(page):
 page.locator('#unitModFolder').set_input_files(str(fixture));page.wait_for_function('U.ready&&!R.loading',timeout=180000)
with sync_playwright() as p:
 browser=paths.browser(p,headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);page=browser.new_page(viewport={'width':1400,'height':1100},accept_downloads=True);page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:','blob:','data:')) else None);page.on('dialog',lambda d:d.accept())
 page.goto(f'http://127.0.0.1:{server.server_port}/Civ4ArtStudio.html');page.locator('#unitMode').click();load(page);assert page.locator('#unitTemplate').input_value()=='UNIT_WARRIOR';page.locator('#unitFields details').evaluate_all('els=>els.forEach(e=>e.open=true)')
 page.locator('#unitName').fill('Frontier Guard');page.locator('#unitPedia').fill('Frontier guards protect remote settlements.');page.locator('#unitStrategy').fill('Use these troops to defend exposed frontiers.');page.locator('#u_iCombat').fill('4');page.locator('#unitTech').select_option('TECH_BRONZE_WORKING');page.locator('#unitAndBonus').select_option('BONUS_COPPER');page.locator('#unitOrBonuses').select_option(['BONUS_IRON','BONUS_OBSIDIAN']);page.locator('#unitPromotions').select_option(['PROMOTION_COMBAT1']);review(page)
 created=download(page,'unit-create.zip')
 with zipfile.ZipFile(created) as z:
  assert z.testzip() is None;m=json.loads(z.read('manifest.json'));assert m['unit']=='UNIT_FRONTIER_GUARD'
  for f in m['files']:
   b=z.read('patch/'+f['path']);assert hashlib.sha256(b).hexdigest()==f['newSHA256'];ET.fromstring(b)
   if f['originalSHA256']:assert z.read('backup/'+f['path'])==(fixture/f['path']).read_bytes()
  u=node(z,'Assets/XML/Units/CIV4UnitInfos.xml','UnitInfo','UNIT_FRONTIER_GUARD');assert val(u,'Class')=='UNITCLASS_FRONTIER_GUARD' and val(u,'iCombat')=='4' and val(u,'BonusType')=='BONUS_COPPER'
  c=node(z,'Assets/XML/Units/CIV4UnitClassInfos.xml','UnitClassInfo','UNITCLASS_FRONTIER_GUARD');assert val(c,'DefaultUnit')=='UNIT_FRONTIER_GUARD'
  schema=ET.parse(fixture/'Assets/XML/Units/CIV4UnitSchema.xml').getroot();definition=next(x for x in schema if x.attrib.get('name')=='UnitInfo');order=[x.attrib['type'] for x in definition if x.tag.split('}')[-1]=='element'];indices=[order.index(x.tag.split('}')[-1]) for x in u];assert indices==sorted(indices)
 checks.append('Real-mod create: linked standalone unit/class, AND/OR prerequisites, promotions, schema ordering, exact backups and hashes')
 page.locator('#u_iCombat').fill('5');assert page.locator('#downloadUnit').is_disabled();page.locator('#unitID').fill('UNIT_WARRIOR');review(page,False);assert 'already exists' in page.locator('#unitStatus').inner_text();page.locator('#unitID').fill('UNIT_FRONTIER_GUARD')
 page.locator('#unitScope').select_option('unique');page.locator('#unitCivs').select_option(['CIVILIZATION_GERMANY']);review(page)
 with zipfile.ZipFile(download(page,'unit-unique.zip')) as z:
  assert not any(x.endswith('CIV4UnitClassInfos.xml') for x in z.namelist());u=node(z,'Assets/XML/Units/CIV4UnitInfos.xml','UnitInfo','UNIT_FRONTIER_GUARD');assert val(u,'Class')=='UNITCLASS_WARRIOR';c=node(z,'Assets/XML/Civilizations/CIV4CivilizationInfos.xml','CivilizationInfo','CIVILIZATION_GERMANY');assert any(val(n,'UnitClassType')=='UNITCLASS_WARRIOR' and val(n,'UnitType')=='UNIT_FRONTIER_GUARD' for n in entries(c,'Unit'))
 checks.append('Civilization-specific unit replacement preserves original class; duplicate IDs and stale reviews blocked')
 page.locator('#unitAction').select_option('retire');review(page)
 with zipfile.ZipFile(download(page,'unit-retire.zip')) as z:
  u=node(z,'Assets/XML/Units/CIV4UnitInfos.xml','UnitInfo','UNIT_WARRIOR');assert val(u,'iCost')=='-1';assert len(json.loads(z.read('manifest.json'))['files'])==1
 page.locator('#unitAction').select_option('remove');review(page,False);assert 'Removal blocked' in page.locator('#unitStatus').inner_text();assert 'UNIT_WARRIOR' in page.locator('#unitConnections').inner_text()
 checks.append('Recruitment retirement changes only unit cost; dependent stock unit removal is blocked')
 # Install new unit into isolated fixture, then edit and remove it.
 with zipfile.ZipFile(created) as z:
  for path in z.namelist():
   if path.startswith('patch/'):
    f=fixture/path[6:];f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(z.read(path))
 load(page);page.locator('#unitAction').select_option('edit');page.locator('#unitTemplate').select_option('UNIT_FRONTIER_GUARD');page.locator('#unitFields details').evaluate_all('els=>els.forEach(e=>e.open=true)');page.locator('#u_iCombat').fill('6');review(page)
 checks.append('Generated unit can be edited again using owned text keys')
 page.locator('#unitUpgrades').select_option(['UNITCLASS_FRONTIER_GUARD']);review(page,False);assert 'cycle' in page.locator('#unitStatus').inner_text();page.locator('#unitUpgrades').select_option([])
 page.locator('#unitAction').select_option('remove')
 page.evaluate("R.files.set('assets/python/unit-test-ref.py',{path:'Assets/Python/unit-test-ref.py',file:new File(['unit = \"UNIT_FRONTIER_GUARD\"'],'unit-test-ref.py')})")
 review(page,False);assert 'unit-test-ref.py' in page.locator('#unitConnections').inner_text();page.evaluate("R.files.delete('assets/python/unit-test-ref.py');U.scanCache.clear()");review(page)
 with zipfile.ZipFile(download(page,'unit-remove.zip')) as z:
  assert not any(val(n,'Type')=='UNIT_FRONTIER_GUARD' for n in entries(ET.fromstring(z.read('patch/Assets/XML/Units/CIV4UnitInfos.xml')),'UnitInfo'));assert not any(val(n,'Type')=='UNITCLASS_FRONTIER_GUARD' for n in entries(ET.fromstring(z.read('patch/Assets/XML/Units/CIV4UnitClassInfos.xml')),'UnitClassInfo'))
 checks.append('Self-upgrade cycle and external Python reference rejected; unreferenced custom unit and exclusive class removed')
 # Existing archer style overrides and new custom art/button.
 page.locator('#unitAction').select_option('edit');page.locator('#unitTemplate').select_option('UNIT_ARCHER');page.locator('#unitFields details').evaluate_all('els=>els.forEach(e=>e.open=true)');page.locator('#unitArtMode').select_option('replace');Image.new('RGB',(64,64),(170,120,40)).save(OUT/'unit-button.png');page.locator('#unitButton').set_input_files(str(OUT/'unit-button.png'));page.wait_for_function('U.pending===0');review(page)
 with zipfile.ZipFile(download(page,'unit-art.zip')) as z:
  u=node(z,'Assets/XML/Units/CIV4UnitInfos.xml','UnitInfo','UNIT_ARCHER');assert val(u,'Civilopedia')=='TXT_KEY_UNIT_ARCHER_PEDIA';a=node(z,'Assets/XML/Art/CIV4ArtDefines_Unit.xml','UnitArtInfo','ART_DEF_UNIT_ARCHER_STUDIO');assert val(a,'KFM') and val(a,'NIF');assert any(x.endswith('unit_archer.dds') for x in z.namelist());r=ET.fromstring(z.read('patch/Assets/XML/Civilizations/CIV4UnitArtStyleTypeInfos.xml'));styles=[n for n in entries(r,'StyleUnit') if val(n,'UnitType')=='UNIT_ARCHER'];assert styles;assert all(n.text=='ART_DEF_UNIT_ARCHER_STUDIO' for s in styles for n in s.iter() if n.tag.split('}')[-1] in ['EarlyArtDefineTag','LateArtDefineTag','MiddleArtDefineTag'])
 checks.append('Art replacement preserves compatible NIF/KFM pair, exports DDS and updates civilization style overrides')
 with page.expect_download() as dl:page.locator('#saveUnitDraft').click()
 dl.value.save_as(str(OUT/'unit-draft.json'));page.locator('#unitDraftFile').set_input_files(str(OUT/'unit-draft.json'));page.wait_for_function("document.getElementById('unitStatus').textContent.startsWith('Draft restored')");assert page.evaluate('U.button===null');assert page.locator('#downloadUnit').is_disabled()
 page.locator('#unitFields details').evaluate_all('els=>els.forEach(e=>e.open=false)');page.locator('#unitFields details').first.evaluate('e=>e.open=true');page.locator('#unitFields details').nth(1).evaluate('e=>e.open=true');page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(OUT/'unit-screen.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');page.locator('#buttonMode').click();assert page.locator('#unitWorkspace').is_hidden();page.locator('#unitMode').click();page.locator('#unitMode').focus();page.keyboard.press('ArrowRight');assert page.locator('#buildingMode').get_attribute('aria-selected')=='true';assert not errors,errors;assert not external,external
 checks.append('Draft clears pending artwork; responsive layout, keyboard tabs, no script errors or external requests');browser.close()
server.shutdown();(OUT/'unit-validation.json').write_text(json.dumps({'passed':checks,'in_game_tested':False},indent=2)+'\n');print('\n'.join(checks))
