"""Exercise native humanoid preview controls. Requires animation_preview_check.py first."""
from pathlib import Path
import json,functools,http.server,threading
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];OUT=R/'tests/output'
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(OUT)));threading.Thread(target=s.serve_forever,daemon=True).start()
errors=[];external=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader']);page=b.new_page(viewport={'width':1280,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:','data:','blob:')) else None)
 page.goto(f'http://127.0.0.1:{s.server_port}/native-animation-local.html');page.wait_for_timeout(800);assert page.locator('#clip option').count()==2
 assert 'approximate' in page.locator('#issues').inner_text()
 initial=page.locator('#view').evaluate('e=>e.toDataURL()');page.locator('#timeline').fill('0.5');page.locator('#timeline').dispatch_event('input');middle=page.locator('#view').evaluate('e=>e.toDataURL()');assert initial!=middle
 page.locator('#play').click();page.wait_for_timeout(300);assert page.locator('#view').evaluate('e=>e.toDataURL()')!=middle;page.locator('#play').click();assert page.locator('#play').inner_text()=='Play'
 page.locator('#clip').select_option('1');assert page.locator('#timeline').input_value()=='0';assert '3.00 s' in page.locator('#time').inner_text()
 page.locator('#speed').select_option('0.25');page.locator('#loop').uncheck();page.locator('#timeline').fill('0.999');page.locator('#timeline').dispatch_event('input');page.locator('#play').click();page.wait_for_timeout(250);assert page.locator('#play').inner_text()=='Play'
 page.locator('#restart').click();assert page.locator('#timeline').input_value()=='0';before=page.locator('#view').evaluate('e=>e.toDataURL()');page.locator('#texture').uncheck();assert page.locator('#view').evaluate('e=>e.toDataURL()')!=before;page.locator('#texture').check();page.locator('#wire').check();assert page.evaluate('gl.getError()===gl.NO_ERROR');page.locator('#wire').uncheck()
 page.locator('#yaw').fill('90');page.locator('#yaw').dispatch_event('input');assert before!=page.locator('#view').evaluate('e=>e.toDataURL()');page.locator('#yaw').fill('155');page.locator('#yaw').dispatch_event('input')
 page.locator('#parts input').first.uncheck();assert page.evaluate('D.meshes[0].visible===false');page.locator('#parts input').first.check();page.screenshot(path=str(OUT/'native-animation-local.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');assert not errors,errors;assert not external,external;b.close()
s.shutdown();report=json.loads((OUT/'animation-preview-validation.json').read_text());report['browser_checks']=['Two native clips selectable','Scrubbing and playback change rendered pose','Speed, non-looping stop and restart','Diffuse, wireframe, orbit and part visibility controls','Mobile layout','No script/WebGL errors or external requests'];(OUT/'animation-preview-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
