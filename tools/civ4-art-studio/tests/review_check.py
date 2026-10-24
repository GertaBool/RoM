"""Browser review of a real Blender preparation snapshot, without loading mod XML."""
from pathlib import Path
import json,functools,http.server,threading
from playwright.sync_api import sync_playwright
import paths
R=Path(__file__).resolve().parents[1];OUT=R/'tests/output';fixture=OUT/'review-model-final/prepared';data=json.loads((fixture/'review.json').read_text());assert data['report']['sourceTriangles']>data['report']['triangles']
assert sum(p.get('coincidentVerticesWelded',0) for p in data['report']['parts'])>0
assert all(p['boundaryEdgesBeforeReduction']==0 for p in data['report']['parts'] if p.get('coincidentVerticesWelded',0))
assert all(p['boundaryEdgesAfterReduction']==0 for p in data['report']['parts'] if p.get('boundaryEdgesBeforeReduction')==0)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(R/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start();errors=[];external=[]
with sync_playwright() as p:
 b=paths.browser(p,args=['--no-sandbox','--disable-dev-shm-usage','--enable-unsafe-swiftshader']);page=b.new_page(viewport={'width':1400,'height':1050});page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:external.append(r.url) if not r.url.startswith(('http://127.0.0.1:','blob:','data:')) else None)
 page.goto(f'http://127.0.0.1:{server.server_port}/Civ4ArtStudio.html');page.locator('#reviewMode').click();page.locator('#geometryReviewFolder').set_input_files(str(fixture));page.wait_for_function('Q.data!==null');assert page.locator('#geometryReviewControls').is_visible()
 assert 'explicitly enabled' in page.locator('#geometryReviewReport').inner_text()
 source=page.locator('#reviewSourceCanvas').evaluate('e=>e.toDataURL()');converted=page.locator('#reviewConvertedCanvas').evaluate('e=>e.toDataURL()');assert source!=converted
 assert page.evaluate("[...Q.views.values()].every(v=>v.gl.getError()===v.gl.NO_ERROR)")
 page.locator('#reviewAzimuth').fill('90');page.locator('#reviewAzimuth').dispatch_event('input');page.wait_for_timeout(100);assert source!=page.locator('#reviewSourceCanvas').evaluate('e=>e.toDataURL()')
 page.locator('#reviewWire').check();page.locator('#reviewTexture').check();page.wait_for_timeout(100);assert 'baked diffuse' in page.locator('#reviewConvertedLabel').inner_text();assert page.evaluate("[...Q.views.values()].every(v=>v.gl.getError()===v.gl.NO_ERROR)")
 page.locator('#reviewReset').click();assert page.locator('#reviewAzimuth').input_value()=='155' and not page.locator('#reviewWire').is_checked()
 assert page.evaluate("()=>{const d=structuredClone(Q.data);d.converted.faces[0][0]=999999;try{validateReview(d);return false}catch{return true}}")
 # A source-too-large review still shows the converted mesh with explicit notice.
 assert page.evaluate("()=>{const d=structuredClone(Q.data);d.source=null;d.sourceOmitted='Source exceeds browser limit';return validateReview(d).source===null}")
 page.locator('#reviewFront').click();assert page.locator('#reviewAzimuth').input_value()=='180'
 page.locator('#reviewSide').click();assert page.locator('#reviewAzimuth').input_value()=='90'
 page.locator('#reviewReset').click();page.screenshot(path=str(OUT/'geometry-review-preview.png'),full_page=True)
 page.evaluate("()=>{const d=structuredClone(Q.data);d.source=null;const bounds=reviewBounds(d);reviewView('reviewSourceCanvas',null,bounds);reviewView('reviewConvertedCanvas',d.converted,bounds);Q.data=d;renderReview()}")
 assert page.evaluate("[...Q.views.values()].every(v=>v.gl.getError()===v.gl.NO_ERROR)")
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 page.locator('#reviewMode').focus();page.keyboard.press('ArrowRight');assert page.locator('#buttonMode').get_attribute('aria-selected')=='true';assert page.locator('#reviewWorkspace').is_hidden();page.locator('#buttonMode').focus();page.keyboard.press('ArrowLeft');assert page.locator('#reviewMode').get_attribute('aria-selected')=='true';assert not errors,errors;assert not external,external
 b.close()
server.shutdown();report={'passed':['Split GLB seams welded before reduction; closed parts remain closed','Review loads without mod XML','Source and reduced mesh render differently under shared bounds','Synchronized rotation, wire overlay, texture toggle and reset','Invalid indices rejected, omitted source handled explicitly','Responsive layout, keyboard tab wrap, no script/WebGL errors or external requests'],'sourceTriangles':data['report']['sourceTriangles'],'convertedTriangles':data['report']['triangles'],'in_game_tested':False};(OUT/'geometry-review-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
