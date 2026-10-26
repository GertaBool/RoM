#!/usr/bin/env node
/* Command-line bridge to app/core.js, so batch helpers use the same resampler, DDS writer and marker-protected
   GameFont replacement as the browser studio. Images travel as raw RGBA files (width*height*4 bytes).
   node core_bridge.js resample <in.rgba> <w> <h> <outW> <outH> <out.rgba>
   node core_bridge.js dds <in.rgba> <w> <h> <DXT3|RGBA> <out.dds>
   node core_bridge.js font <in.tga> <edits.json> <out.tga>
     edits.json: [{"cell": {"x","y","width","height"}, "rgba": "<file>"}]; every edit must target an empty cell
     (no visible pixel); the result is checked pixel by pixel outside the edited cells and after a decode round trip. */
'use strict';
const fs = require('fs'), path = require('path');
const { createCiv4Core } = require(path.join(__dirname, '..', 'app', 'core.js'));
const C = createCiv4Core();
const image = (file, w, h) => ({ width: w, height: h, data: new Uint8Array(fs.readFileSync(file)) });
const [op, ...a] = process.argv.slice(2);
if (op === 'resample') {
  const out = C.resample(image(a[0], +a[1], +a[2]), +a[3], +a[4]); fs.writeFileSync(a[5], out.data);
} else if (op === 'dds') {
  fs.writeFileSync(a[4], C.writeDDS(image(a[0], +a[1], +a[2]), a[3], false));
} else if (op === 'font') {
  const original = C.readTGA(fs.readFileSync(a[0])), edits = JSON.parse(fs.readFileSync(a[1], 'utf8'));
  const edited = { ...original, data: original.data.slice() }, cells = [];
  let protectedPixels = 0, avoided = 0;
  for (const e of edits) {
    const c = e.cell;
    for (let y = c.y; y < c.y + c.height; y++) for (let x = c.x; x < c.x + c.width; x++) {
      const p = (y * original.width + x) * 4;
      if (!C.marker(original.data, p) && original.data[p + 3] > 0) throw Error(`cell at ${c.x},${c.y} already holds visible artwork`);
    }
    const r = C.replaceCell(edited, c, image(e.rgba, c.width, c.height)); protectedPixels += r.protectedPixels; avoided += r.avoided; cells.push(c);
  }
  const changed = C.verifyFont(original, edited, cells);
  const bytes = C.writeTGA(edited, original), back = C.readTGA(bytes);
  C.verifyFont(original, back, cells);
  if (back.data.some((v, i) => v !== edited.data[i])) throw Error('round trip changed pixels');
  fs.writeFileSync(a[2], bytes);
  console.log(JSON.stringify({ cells: cells.length, changedPixels: changed, protectedMarkers: protectedPixels, recolouredToAvoidMarkers: avoided }));
} else {
  console.error('usage: core_bridge.js resample|dds|font ...'); process.exit(2);
}
