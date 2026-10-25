"""Structural checks using a prepared folder and the source mod (no game rendering)."""
import sys,json,hashlib,functools,http.server,threading
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
import paths
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'helpers'))
from unit_model_convert import load_nif,dependencies
prepared=Path(sys.argv[1]);source=Path(sys.argv[2]);m=json.loads((prepared/'model.json').read_text());N,_,_=dependencies();data=load_nif(prepared/'model.nif');g=next(x for x in data.get_global_iterator() if isinstance(x,N.NiGeometry) and x.name.decode()==m['report']['donorMesh'])
assert g.data.num_vertices==m['report']['vertices'];assert len(g.data.get_triangles())==m['report']['triangles']
assert all(0<len(w)<=4 and abs(sum(v for _,v in w)-1)<1e-4 for w in g.get_vertex_weights())
p=g.skin_instance.skin_partition or g.skin_instance.data.skin_partition
assert p and sum(x.num_triangles for x in p.skin_partition_blocks)==m['report']['triangles']
assert all(x.num_bones<=18 and x.num_weights_per_vertex<=4 for x in p.skin_partition_blocks)
with Image.open(prepared/'diffuse.dds') as im:assert im.size==(512,512);im.load()
fixture=ROOT/'tests/output/unit-fixture';donor=next(x for x in source.rglob('*.nif') if x.relative_to(source).as_posix().lower()==('Assets/'+m['donor']['nif']).lower());target=fixture/donor.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(donor.read_bytes())
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(ROOT/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as p:
 browser=paths.browser(p,args=['--no-sandbox','--disable-dev-shm-usage']);page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto(f'http://127.0.0.1:{server.server_port}/Civ4ArtStudio.html');page.locator('#unitMode').click();page.locator('#unitModFolder').set_input_files(str(fixture));page.wait_for_function('U.ready&&!R.loading',timeout=180000)
 page.locator('#unitFields details').evaluate_all('els=>els.forEach(e=>e.open=true)');page.locator('#unitName').fill('Test Model');page.locator('#unitPedia').fill('Test model.');page.locator('#unitStrategy').fill('Test model.');page.locator('#unitArtMode').select_option('reconstructed');page.locator('#unitModelFolder').set_input_files(str(prepared));page.wait_for_function('U.pending===0');assert page.evaluate('!!U.model'),page.locator('#unitStatus').inner_text()
 assert page.evaluate("unitAnimationPairs(unitArtRecord().node).every(r=>value(r.node,'NIF')===value(unitArtRecord().node,'NIF'))")
 result=page.evaluate("async()=>{const p=await prepareUnit();return {files:p.files.map(f=>f.name),notes:p.manifest.notes}}")
 assert 'Assets/Art/Units/Studio/UNIT_TEST_MODEL/model.nif' in result['files'];assert any('EXPERIMENTAL' in x for x in result['notes'])
 page.locator('#unitID').fill('UNIT_WRONG_ID');assert 'Unit ID must match' in page.evaluate("async()=>{try{await prepareUnit();return ''}catch(e){return e.message}}")
 page.locator('#unitID').fill('UNIT_TEST_MODEL');page.evaluate("$('unitAnimation').value='invalid'");assert 'known animation pairing' in page.evaluate("async()=>{try{await prepareUnit();return ''}catch(e){return e.message}}")
 # Alter bytes after generation; hashes must reject the import.
 result=page.evaluate("""async()=>{const files=[...$('unitModelFolder').files].map(f=>f.name==='diffuse.dds'?new File(['DDS bad'],f.name):f);try{await importUnitModel(files);return ''}catch(e){return e.message}}""")
 assert 'Checksum mismatch' in result;assert not errors,errors;browser.close()
server.shutdown();report={'passed':['NIF roundtrip, triangle coverage, normalized weights and partition limits','DDS decoded independently','Prepared folder import and patch paths','Wrong unit ID, invalid animation and corrupted texture rejected'],'in_game_tested':False,'fixture':'Synthetic geometry; no external reconstruction service used'};(ROOT/'tests/output/unit-model-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
