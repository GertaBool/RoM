from pathlib import Path
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import functools,http.server,threading,json,zipfile,sys
FONT_DIR=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/workspace/rise-of-mankind/Assets/res/Fonts')
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'tests/output';OUT.mkdir(exist_ok=True)
# Synthetic artwork, not game assets; asymmetric orientation and transparency.
im=Image.new('RGBA',(120,80),(255,255,255,255));d=ImageDraw.Draw(im);d.rectangle((15,8,55,70),fill=(220,50,20,255));d.ellipse((50,10,110,70),fill=(15,150,220,180));im.save(OUT/'artwork.png');im.convert('RGB').save(OUT/'artwork.jpg')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'dist')))
threading.Thread(target=server.serve_forever,daemon=True).start();errors=[];external=[];checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1380,'height':1100},accept_downloads=True)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:','blob:','data:')) else None)
 page.goto(f'http://127.0.0.1:{server.server_port}/Civ4ArtStudio.html')
 assert page.locator('#exportDDS').is_disabled()
 page.locator('#artFile').set_input_files(str(OUT/'artwork.png'));page.wait_for_function("document.querySelector('#artInfo').textContent.includes('120 × 80')")
 assert page.locator('#exportDDS').is_enabled();page.locator('#keyEnabled').check();page.locator('#rim').check()
 with page.expect_download() as dl:page.locator('#exportDDS').click()
 dl.value.save_as(str(OUT/'browser-button.dds'));button=Image.open(OUT/'browser-button.dds');assert button.size==(64,64);assert button.getpixel((0,0))[3]==0
 checks.append('PNG upload, transparent keyed background, rounded button, worker DDS export')
 with page.expect_download() as dl:page.locator('#exportPNG').click()
 dl.value.save_as(str(OUT/'browser-preview.png'));assert Image.open(OUT/'browser-preview.png').size==(64,64)
 page.locator('#size').select_option('custom');page.locator('#width').fill('100');assert page.locator('#exportDDS').is_disabled()
 page.locator('#width').fill('128');page.locator('#height').fill('64');page.locator('#format').select_option('RGBA');page.locator('#mipmaps').check()
 with page.expect_download() as dl:page.locator('#exportDDS').click()
 dl.value.save_as(str(OUT/'browser-texture.dds'));assert Image.open(OUT/'browser-texture.dds').size==(128,64)
 checks.append('Custom dimensions rejected if invalid; rectangular RGBA DDS with mipmaps')
 page.locator('#size').select_option('64');page.locator('#artFile').set_input_files(str(OUT/'artwork.jpg'));page.wait_for_function("document.querySelector('#artInfo').textContent.includes('artwork.jpg')")
 checks.append('JPEG artwork loads')
 page.screenshot(path=str(OUT/'button-screen.png'),full_page=True)
 page.locator('#fontMode').click();page.locator('#fontFile').set_input_files(str(FONT_DIR/'GameFont.tga'));page.wait_for_function("document.querySelector('#fontInfo').textContent.includes('1301 cells')")
 page.locator('#cellRow').fill('5');page.locator('#cellCol').fill('1');page.locator('#selectCell').click();assert '21 × 20' in page.locator('#cellInfo').inner_text()
 page.locator('#cellRow').fill('9999');page.locator('#selectCell').click();assert page.locator('#applyGlyph').is_disabled()
 page.locator('#cellRow').fill('5');page.locator('#cellCol').fill('1');page.locator('#selectCell').click()
 page.locator('#applyGlyph').click();assert page.locator('#exportFont').is_enabled();page.locator('#undoGlyph').click();assert page.locator('#exportFont').is_disabled()
 page.locator('#applyGlyph').click()
 with page.expect_download() as dl:page.locator('#exportFont').click()
 dl.value.save_as(str(OUT/'browser-GameFont.tga'))
 checks.append('Full-size font cell selection, apply, undo and export')
 page.locator('#smallFontFile').set_input_files(str(FONT_DIR/'GameFont_75.tga'));page.wait_for_function("document.querySelector('#smallFontInfo').textContent.includes('1325 cells')")
 assert page.locator('#applyGlyph').is_disabled();page.locator('#cellRow').fill('5');page.locator('#cellCol').fill('1');page.locator('#selectCell').click();assert '16 × 16' in page.locator('#cellInfo').inner_text()
 page.locator('#applyGlyph').click()
 with page.expect_download() as dl:page.locator('#exportPair').click()
 dl.value.save_as(str(OUT/'browser-fonts.zip'))
 with zipfile.ZipFile(OUT/'browser-fonts.zip') as z:
  assert z.testzip() is None;log=json.loads(z.read('edit-log.json'));assert len(log['files'])==2
  for f in log['files']:
   data=z.read(f['output']);(OUT/('browser-pair-'+f['output'])).write_bytes(data)
   original=Image.open(FONT_DIR/f['output']).convert('RGBA');result=Image.open(OUT/('browser-pair-'+f['output'])).convert('RGBA');assert original.size==result.size
   cell=f['replacements'][0];old=original.tobytes();new=result.tobytes();changed=0
   for i in range(original.width*original.height):
    pos=i*4;x=i%original.width;y=i//original.width
    inside=cell['x']<=x<cell['x']+cell['width'] and cell['y']<=y<cell['y']+cell['height']
    if not inside or old[pos:pos+3] in [b'\xff\x00\xff',b'\x00\xff\xff']:assert new[pos:pos+4]==old[pos:pos+4]
    if new[pos:pos+4]!=old[pos:pos+4]:changed+=1
   assert changed==f['changedPixels'] and changed>0
 checks.append('Independent matching-cell selection in small font; paired ZIP with validated edit log')
 checks.append('Pillow confirms every marker and unrelated pixel in both browser-exported font files')
 page.screenshot(path=str(OUT/'font-screen.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});page.locator('#buttonMode').click();assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
 checks.append('Narrow viewport does not overflow')
 assert not errors,errors;assert not external,external
 browser.close()
server.shutdown()
(OUT/'browser-validation.json').write_text(json.dumps({'passed':checks,'javascript_errors':errors,'external_requests':external,'in_game_tested':False,'tested_via':'local HTTP serving the standalone HTML'},indent=2)+'\n');print('\n'.join(checks))
