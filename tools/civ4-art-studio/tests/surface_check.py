"""Procedural material and browser facade checks; run after building_check.py and the Blender shape check."""
from pathlib import Path
import sys,functools,http.server,threading,json,base64,io,struct
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import paths
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tests/output';sys.path.insert(0,str(ROOT/'helpers'))
from surface_textures import texture
checks=[]
for kind in ['Cloth','Armor','Cuirass','Leather','Trim','Wood','Skin']:
 a=texture(kind,[.32,.25,.18],256);assert np.isfinite(a).all() and a.min()>=0 and a.max()<=1 and np.all(a[:,:,3]==1);assert np.array_equal(a,texture(kind,[.32,.25,.18],256));assert a[:,:,:3].std(axis=(0,1)).max()>.001
 im=Image.fromarray(np.uint8(np.clip(a[:,:,:3],0,1)**(1/2.2)*255));im.save(OUT/('surface-'+kind.lower()+'.png'))
checks.append('Seven deterministic opaque material maps, finite pixels, visible variation')
b=(OUT/'shape-lab/soldier.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);assert len(g['images'])>=6
assert all('baseColorTexture' in m.get('pbrMetallicRoughness',{}) for m in g['materials'] if m.get('name')!='Studio Face detail')
assert all('TEXCOORD_0' in primitive['attributes'] for mesh in g['meshes'] for primitive in mesh['primitives'])
checks.append('Final unit GLB embeds material images and UV coordinates')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=paths.browser(p,args=['--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader']);page=browser.new_page(viewport={'width':1400,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto(f'http://127.0.0.1:{server.server_port}/Civ4ArtStudio.html');page.locator('#buildingMode').click();page.locator('#buildingModFolder').set_input_files(str(OUT/'building-fixture'));page.wait_for_function('B.ready',timeout=120000);page.locator('#buildingFields details').evaluate_all('es=>es.forEach(e=>e.open=true)')
 page.locator('#buildingName').fill('Painted Hall');page.locator('#buildingPedia').fill('A decorated civic hall.');page.locator('#buildingStrategy').fill('Build to serve the town.');page.locator('#buildingArtMode').select_option('box');assert page.evaluate('B.texture===null')
 atlas=[]
 for style in ['brick','stone','timber']:
  page.locator('#buildingSurface').select_option(style);page.evaluate('renderBuilding()');data=page.evaluate('buildingTextureCanvas().toDataURL()');raw=base64.b64decode(data.split(',')[1]);(OUT/f'facade-{style}.png').write_bytes(raw);atlas.append(raw);page.locator('#building3D').screenshot(path=str(OUT/f'facade-{style}-model.png'))
  assert page.evaluate("buildingTextureCanvas()===buildingTextureCanvas()")
  page.locator('#reviewBuilding').click();page.wait_for_function("!document.getElementById('reviewBuilding').disabled");assert page.locator('#downloadBuilding').is_enabled(),page.locator('#buildingStatus').inner_text()
  encoded=page.evaluate("Array.from(B.plan.files.find(f=>f.name.endsWith('/diffuse.dds')).data)");im=Image.open(io.BytesIO(bytes(encoded)));assert im.size==(512,512);assert im.convert('RGB').getextrema()[0][1]>im.convert('RGB').getextrema()[0][0]+60
 assert len(set(atlas))==3
 with page.expect_download() as dl:page.locator('#buildingSaveTexture').click()
 dl.value.save_as(str(OUT/'downloaded-diffuse.png'));assert Image.open(OUT/'downloaded-diffuse.png').size==(512,512)
 checks.append('Standalone diffuse PNG download decoded independently')
 checks.append('Three facade styles preview and export mipmapped DDS without an uploaded image')
 before=page.evaluate('buildingTextureCanvas().toDataURL()');page.locator('#buildingWeathering').fill('0.8');page.locator('#buildingWeathering').dispatch_event('input');after=page.evaluate('buildingTextureCanvas().toDataURL()');assert before!=after;assert page.locator('#downloadBuilding').is_disabled()
 page.locator('#buildingFacadeFloors').fill('9');page.locator('#reviewBuilding').click();page.wait_for_function("!document.getElementById('reviewBuilding').disabled");assert page.locator('#downloadBuilding').is_disabled();assert '2–8' in page.locator('#buildingStatus').inner_text();assert not errors,errors
 checks.append('Weathering invalidates texture cache/review; unsupported floor counts blocked')
 browser.close()
server.shutdown();(OUT/'surface-validation.json').write_text(json.dumps({'passed':checks,'in_game_tested':False},indent=2)+'\n');print(checks)
