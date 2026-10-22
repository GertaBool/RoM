const assert = require('node:assert/strict'), fs = require('node:fs'), path = require('node:path');
const { createCiv4Core } = require('../app/core.js'); const C = createCiv4Core();
const out = path.resolve(__dirname, 'output'); fs.mkdirSync(out, { recursive: true });
const image = (w, h, color) => { const data = new Uint8Array(w * h * 4); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) data.set(color(x, y), (y * w + x) * 4); return { width: w, height: h, data }; };
const save = (n, b) => fs.writeFileSync(path.join(out, n), b);
let passed = 0; function test(name, fn) { fn(); passed++; console.log('PASS', name); }
test('TGA retains hidden RGB, alpha, origins and footer in a no-op round trip', () => {
  const im = image(7, 3, (x, y) => [x * 30, y * 60, 255 - x, x % 2 ? 255 : 0]);
  for (const orientation of [0, 16, 32, 48]) {
    const first = C.readTGA(C.writeTGA(im)); first.descriptor = orientation | 8;
    const header = first.original.slice(); header[17] = first.descriptor; first.original = header;
    const data = C.writeTGA(im, first), read = C.readTGA(data); assert.deepEqual(read.data, im.data); assert.deepEqual(C.writeTGA(read, read), data);
  }
  const file = C.writeTGA(im), withTail = new Uint8Array(file.length + 10); withTail.set(file); withTail.set([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], file.length);
  const decoded = C.readTGA(withTail); assert.deepEqual(C.writeTGA(decoded, decoded), withTail); save('tga-fixture.tga', file); save('tga-expected.bin', im.data);
});
test('RLE TGA decodes repeated and literal packets', () => {
  const h = new Uint8Array(18); h[2] = 10; h[12] = 3; h[14] = 2; h[16] = 32; h[17] = 40;
  const packets = [0x82, 30, 20, 10, 255, 2, 3, 2, 1, 4, 6, 5, 4, 7, 9, 8, 7, 10]; const file = new Uint8Array(18 + packets.length); file.set(h); file.set(packets, 18);
  const im = C.readTGA(file); assert.deepEqual([...im.data], [10,20,30,255,10,20,30,255,10,20,30,255,1,2,3,4,4,5,6,7,7,8,9,10]);
  assert.deepEqual(C.readTGA(C.writeTGA(im, im)).data, im.data); save('rle-fixture.tga', file);
  const bad = file.slice(); bad[18] = 0xff; assert.throws(() => C.readTGA(bad), /packet length/);
  assert.throws(() => C.readTGA(file.slice(0, 20)), /Truncated/);
});
test('Marker grid detection, reserved-color avoidance, undo, and corruption guard', () => {
  const im = image(9, 9, (x, y) => x % 4 === 0 || y % 4 === 0 ? [255, 0, 255, 0] : [255,255,255,0]);
  im.data.set([0,255,255,0], (3 * 9 + 4) * 4);
  const original = { ...im, data: im.data.slice() }, cells = C.detectCells(im); assert.equal(cells.length, 4); assert.deepEqual(cells[0], { x:1,y:1,width:3,height:3,row:1,col:1 });
  const result = C.replaceCell(im, cells[0], image(3, 3, () => [255,0,255,255])); assert.equal(result.avoided, 9); assert.equal(C.verifyFont(original, im, [cells[0]]), 9);
  im.data[0] = 0; assert.throws(() => C.verifyFont(original, im, [cells[0]]), /protection/); im.data[0] = 255;
  C.restoreCell(im, cells[0], result.before); assert.deepEqual(im.data, original.data);
  const inside = image(3,3, (x,y) => x === 1 && y === 1 ? [0,255,255,0] : [255,255,255,0]); const cell = {x:0,y:0,width:3,height:3};
  C.replaceCell(inside, cell, image(3,3, () => [250,50,50,255])); assert.deepEqual([...inside.data.slice(16,20)], [0,255,255,0]);
});
test('DDS output validates dimensions, headers, level sizes and alpha-aware mipmaps', () => {
  const im = image(16, 8, (x,y) => [255, 0, 0, Math.round(x * 255 / 15)]); save('dds-expected.bin', im.data);
  for (const format of ['DXT3','RGBA']) for (const mips of [false,true]) {
    const bytes = C.writeDDS(im, format, mips), view = new DataView(bytes.buffer); assert.equal(view.getUint32(0,true), 0x20534444); assert.equal(view.getUint32(12,true), 8); assert.equal(view.getUint32(16,true), 16); assert.equal(view.getUint32(28,true), mips ? 5 : 1);
    assert.equal(bytes.length, format === 'DXT3' ? (mips ? 128+128+32+16+16+16 : 256) : (mips ? 128+512+128+32+8+4 : 640)); save(`red-${format}-${mips}.dds`, bytes);
  }
  const m = C.mip(image(2,2,(x,y)=>x===0&&y===0?[255,0,0,255]:[0,0,255,0])); assert.deepEqual([...m.data],[255,0,0,64]);
  assert.throws(()=>C.writeDDS(image(3,4,()=>[0,0,0,0])),/powers of two/);
  const contrast = image(4,4,(x,y)=>(x+y)%2?[255,0,0,255]:[0,255,0,255]); save('contrast.dds',C.writeDDS(contrast));save('contrast-expected.bin',contrast.data);
  const gradient = image(64,64,(x,y)=>[x*4,y*4,(x+y)*2,255]); save('gradient.dds',C.writeDDS(gradient)); save('gradient-expected.bin',gradient.data);
});
test('ZIP supports Unicode names and binary payload', () => {
  assert.equal(C.crc32(new TextEncoder().encode('123456789')), 0xcbf43926);
  save('bundle.zip',C.zip([{name:'GameFont.tga',data:fs.readFileSync(path.join(out,'tga-fixture.tga'))},{name:'édition.json',data:'{"ok":true}'}]));
});
const fontDir = process.argv[2];
if (fontDir) for (const name of ['GameFont.tga','GameFont_75.tga']) test('Real '+name+': lossless markers and unrelated pixels',()=>{
  const bytes = new Uint8Array(fs.readFileSync(path.join(fontDir,name))), im=C.readTGA(bytes), original={...im,data:im.data.slice()},cells=C.detectCells(im);
  assert.ok(cells.length > 400); assert.deepEqual(C.writeTGA(im,im),bytes); const cell=cells.find(r=>r.row===5&&r.col===1); assert.ok(cell); assert.ok(cell.width>10&&cell.height>10);
  const result=C.replaceCell(im,cell,image(cell.width,cell.height,(x,y)=>[250,80,20, x===y?255:0])); C.verifyFont(original,im,[cell]);
  const modified=C.writeTGA(im,im); assert.deepEqual(C.readTGA(modified).data,im.data);save('edited-'+name,modified);save('cell-'+name+'.json',JSON.stringify(cell));C.restoreCell(im,cell,result.before);assert.deepEqual(im.data,original.data);
  console.log(' ',cells.length,'cells; selected',cell);
});
console.log(`${passed} core test groups passed`);
