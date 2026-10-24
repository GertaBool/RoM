/* Civ IV Art Studio: binary image formats and marker-preserving glyph replacement. */
function createCiv4Core() {
  'use strict';
  const MAX_PIXELS = 16777216;
  function checkImage(im) {
    if (!Number.isInteger(im.width) || !Number.isInteger(im.height) || im.width < 1 || im.height < 1 || im.width * im.height > MAX_PIXELS || im.data.length !== im.width * im.height * 4) throw Error('Invalid image dimensions or pixel buffer.');
  }
  // Linear-light, premultiplied-alpha Lanczos-3. Transparent RGB cannot bleed into edges.
  function resample(im,width,height){
    checkImage(im);if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||height<1||width*height>MAX_PIXELS)throw Error('Invalid resize dimensions.');
    if(width===im.width&&height===im.height)return {width,height,data:new Uint8Array(im.data)};
    const lut=Float64Array.from({length:256},(_,i)=>{const v=i/255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;});
    const sinc=x=>Math.abs(x)<1e-9?1:Math.sin(Math.PI*x)/(Math.PI*x);
    function weights(src,dst){const scale=Math.max(1,src/dst),radius=3*scale;return Array.from({length:dst},(_,i)=>{const center=(i+.5)*src/dst-.5,a=[];let sum=0;for(let j=Math.max(0,Math.ceil(center-radius));j<=Math.min(src-1,Math.floor(center+radius));j++){const x=(j-center)/scale,w=sinc(x)*sinc(x/3);a.push([j,w]);sum+=w;}return a.map(([j,w])=>[j,w/sum]);});}
    const wx=weights(im.width,width),wy=weights(im.height,height),tmp=new Float32Array(width*im.height*4),out=new Uint8Array(width*height*4);
    for(let y=0;y<im.height;y++)for(let x=0;x<width;x++){const d=(y*width+x)*4;for(const [j,w]of wx[x]){const p=(y*im.width+j)*4,a=im.data[p+3]/255;for(let k=0;k<3;k++)tmp[d+k]+=lut[im.data[p+k]]*a*w;tmp[d+3]+=a*w;}}
    for(let y=0;y<height;y++)for(let x=0;x<width;x++){const v=[0,0,0,0],p=(y*width+x)*4;for(const [j,w]of wy[y]){const d=(j*width+x)*4;for(let k=0;k<4;k++)v[k]+=tmp[d+k]*w;}
      const a=Math.max(0,Math.min(1,v[3]));out[p+3]=Math.round(a*255);if(a<1/255)continue;
      for(let k=0;k<3;k++){const c=Math.max(0,Math.min(1,v[k]/v[3]));out[p+k]=Math.round(255*(c<=.0031308?12.92*c:1.055*c**(1/2.4)-.055));}}
    return {width,height,data:out};
  }
  function marker(d, p) { return d[p + 1] === 0 && d[p] === 255 && d[p + 2] === 255 || d[p] === 0 && d[p + 1] === 255 && d[p + 2] === 255; }
  function readTGA(input) {
    const b = new Uint8Array(input), v = new DataView(b.buffer, b.byteOffset, b.byteLength);
    if (b.length < 18) throw Error('This is not a complete TGA file.');
    const type = b[2], bits = b[16], width = v.getUint16(12, true), height = v.getUint16(14, true), desc = b[17];
    if (b[1] || ![2, 10].includes(type) || ![24, 32].includes(bits) || desc & 0xc0) throw Error('Use a true-color, non-interleaved 24/32-bit TGA (uncompressed or RLE). Indexed TGA is not supported.');
    if (!width || !height || width * height > MAX_PIXELS) throw Error('TGA dimensions exceed the 16-megapixel limit.');
    let at = 18 + b[0], count = 0; const stride = bits / 8, data = new Uint8Array(width * height * 4);
    function pixel(rgba) {
      const sx = count % width, sy = Math.floor(count / width), x = desc & 16 ? width - 1 - sx : sx, y = desc & 32 ? sy : height - 1 - sy;
      data.set(rgba, (y * width + x) * 4); count++;
    }
    function readPixel() {
      if (at + stride > b.length) throw Error('Truncated TGA pixel data.');
      const c = [b[at + 2], b[at + 1], b[at], stride === 4 ? b[at + 3] : 255]; at += stride; return c;
    }
    while (count < width * height) {
      let n = 1, repeat = false;
      if (type === 10) { if (at >= b.length) throw Error('Truncated TGA packet.'); const packet = b[at++]; n = (packet & 127) + 1; repeat = !!(packet & 128); }
      if (count + n > width * height) throw Error('Invalid TGA packet length.');
      if (repeat) { const c = readPixel(); for (let k = 0; k < n; k++) pixel(c); }
      else for (let k = 0; k < n; k++) pixel(readPixel());
    }
    return { width, height, data, bits, descriptor: desc, type, original: b, pixelOffset: 18 + b[0], pixelEnd: at };
  }
  function writeTGA(im, template) {
    checkImage(im);
    if (template && (template.width !== im.width || template.height !== im.height)) throw Error('GameFont dimensions must not change.');
    // Preserve header, ID and trailing bytes exactly for an uncompressed 32-bit template.
    const preserve = template && template.type === 2 && template.bits === 32;
    const id = template ? template.original.slice(18, template.pixelOffset) : new Uint8Array();
    const tail = preserve ? template.original.slice(template.pixelEnd) : new Uint8Array();
    const out = new Uint8Array(18 + id.length + im.data.length + tail.length), v = new DataView(out.buffer);
    if (template) out.set(template.original.slice(0, 18));
    out[0] = id.length; out[1] = 0; out[2] = 2; out.fill(0, 3, 8);
    v.setUint16(12, im.width, true); v.setUint16(14, im.height, true); out[16] = 32;
    out[17] = preserve ? template.descriptor : (template ? template.descriptor & 0x30 : 0) | 8;
    out.set(id, 18); let at = 18 + id.length;
    for (let sy = 0; sy < im.height; sy++) for (let sx = 0; sx < im.width; sx++) {
      const x = out[17] & 16 ? im.width - 1 - sx : sx, y = out[17] & 32 ? sy : im.height - 1 - sy, p = (y * im.width + x) * 4;
      out[at++] = im.data[p + 2]; out[at++] = im.data[p + 1]; out[at++] = im.data[p]; out[at++] = im.data[p + 3];
    }
    out.set(tail, at); return out;
  }
  function detectCells(im) {
    checkImage(im);
    // Only fully marker-filled rows and columns delimit cells. Never infer a glyph index.
    const bands = []; let start = -1;
    for (let y = 0; y <= im.height; y++) {
      let boundary = y === im.height;
      if (!boundary) { boundary = true; for (let x = 0; x < im.width; x++) if (!marker(im.data, (y * im.width + x) * 4)) { boundary = false; break; } }
      if (!boundary && start < 0) start = y;
      if (boundary && start >= 0) { bands.push([start, y]); start = -1; }
    }
    const cells = [];
    bands.forEach(([top, bottom], row) => {
      let left = -1, col = 0;
      for (let x = 0; x <= im.width; x++) {
        let boundary = x === im.width;
        if (!boundary) { boundary = true; for (let y = top; y < bottom; y++) if (!marker(im.data, (y * im.width + x) * 4)) { boundary = false; break; } }
        if (!boundary && left < 0) left = x;
        if (boundary && left >= 0) {
          col++;
          if (x - left <= 128 && bottom - top <= 128 && x - left >= 1 && bottom - top >= 1) cells.push({ x: left, y: top, width: x - left, height: bottom - top, row: row + 1, col });
          left = -1;
        }
      }
    });
    return cells;
  }
  function replaceCell(im, cell, glyph) {
    checkImage(im); checkImage(glyph);
    if (!cell || ![cell.x, cell.y, cell.width, cell.height].every(Number.isInteger) || cell.x < 0 || cell.y < 0 || cell.x + cell.width > im.width || cell.y + cell.height > im.height || glyph.width !== cell.width || glyph.height !== cell.height) throw Error('The artwork must exactly fit the selected cell.');
    const before = new Uint8Array(glyph.data.length); let avoided = 0, protectedPixels = 0;
    for (let y = 0; y < cell.height; y++) for (let x = 0; x < cell.width; x++) {
      const p = ((y + cell.y) * im.width + x + cell.x) * 4, q = (y * cell.width + x) * 4;
      before.set(im.data.subarray(p, p + 4), q);
      if (marker(im.data, p)) { protectedPixels++; continue; }
      im.data.set(glyph.data.subarray(q, q + 4), p);
      // Do not introduce exact separator colors, even in invisible RGB channels.
      if (marker(im.data, p)) { im.data[p + 2] = 254; avoided++; }
    }
    return { before, avoided, protectedPixels };
  }
  function restoreCell(im, cell, before) {
    if (before.length !== cell.width * cell.height * 4) throw Error('Invalid undo record.');
    for (let y = 0; y < cell.height; y++) im.data.set(before.subarray(y * cell.width * 4, (y + 1) * cell.width * 4), ((cell.y + y) * im.width + cell.x) * 4);
  }
  function verifyFont(original, edited, allowed) {
    checkImage(original); checkImage(edited);
    if (original.width !== edited.width || original.height !== edited.height) throw Error('Font dimensions changed.');
    const mask = new Uint8Array(original.width * original.height);
    for (const r of allowed) for (let y = r.y; y < r.y + r.height; y++) mask.fill(1, y * original.width + r.x, y * original.width + r.x + r.width);
    let changed = 0;
    for (let i = 0; i < mask.length; i++) {
      const p = i * 4, same = original.data[p] === edited.data[p] && original.data[p + 1] === edited.data[p + 1] && original.data[p + 2] === edited.data[p + 2] && original.data[p + 3] === edited.data[p + 3];
      if (!same && (!mask[i] || marker(original.data, p))) throw Error('Font protection check failed: an unrelated or marker pixel changed.');
      if (!marker(original.data, p) && marker(edited.data, p)) throw Error('Font protection check failed: a new marker color was introduced.');
      if (!same) changed++;
    }
    return changed;
  }
  function mip(im) {
    const width = Math.max(1, im.width >> 1), height = Math.max(1, im.height >> 1), data = new Uint8Array(width * height * 4);
    for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
      let a = 0, r = 0, g = 0, b = 0, n = 0;
      for (let j = 0; j < Math.min(2, im.height); j++) for (let i = 0; i < Math.min(2, im.width); i++) {
        const p = ((y * 2 + j) * im.width + x * 2 + i) * 4, alpha = im.data[p + 3];
        a += alpha; r += im.data[p] * alpha; g += im.data[p + 1] * alpha; b += im.data[p + 2] * alpha; n++;
      }
      const q = (y * width + x) * 4;
      data[q] = a ? Math.round(r / a) : 0; data[q + 1] = a ? Math.round(g / a) : 0; data[q + 2] = a ? Math.round(b / a) : 0; data[q + 3] = Math.round(a / n);
    }
    return { width, height, data };
  }
  const rgb565 = c => ((Math.round(c[0] * 31 / 255) << 11) | (Math.round(c[1] * 63 / 255) << 5) | Math.round(c[2] * 31 / 255));
  const from565 = c => [Math.round((c >> 11) * 255 / 31), Math.round(((c >> 5) & 63) * 255 / 63), Math.round((c & 31) * 255 / 31)];
  function dxt3(im) {
    const bw = Math.ceil(im.width / 4), bh = Math.ceil(im.height / 4), out = new Uint8Array(bw * bh * 16), view = new DataView(out.buffer); let at = 0;
    for (let by = 0; by < bh; by++) for (let bx = 0; bx < bw; bx++) {
      const px = [];
      for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) {
        const p = (Math.min(by * 4 + y, im.height - 1) * im.width + Math.min(bx * 4 + x, im.width - 1)) * 4;
        px.push([im.data[p], im.data[p + 1], im.data[p + 2], im.data[p + 3]]);
      }
      for (let i = 0; i < 16; i += 2) out[at + i / 2] = Math.round(px[i][3] / 17) | Math.round(px[i + 1][3] / 17) << 4;
      const visible = px.filter(c => c[3] > 0); const samples = visible.length ? visible : px;
      const mean = [0, 0, 0]; for (const c of samples) for (let j = 0; j < 3; j++) mean[j] += c[j] / samples.length;
      const cov = Array(9).fill(0);
      for (const c of samples) for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) cov[a * 3 + b] += (c[a] - mean[a]) * (c[b] - mean[b]);
      let axis = [0, 0, 0];
      const variance = [cov[0], cov[4], cov[8]]; axis[variance.indexOf(Math.max(...variance))] = 1;
      for (let k = 0; k < 5; k++) {
        const n = [0, 0, 0]; for (let a = 0; a < 3; a++) for (let b = 0; b < 3; b++) n[a] += cov[a * 3 + b] * axis[b];
        const len = Math.hypot(...n); if (len < 1e-8) break; axis = n.map(v => v / len);
      }
      let low = samples[0], high = samples[0], lo = Infinity, hi = -Infinity;
      for (const c of samples) { const score = c[0] * axis[0] + c[1] * axis[1] + c[2] * axis[2]; if (score < lo) { lo = score; low = c; } if (score > hi) { hi = score; high = c; } }
      let c0 = rgb565(high), c1 = rgb565(low); if (c0 < c1) [c0, c1] = [c1, c0];
      const a = from565(c0), b = from565(c1), colors = [a, b, a.map((v, j) => Math.floor((2 * v + b[j]) / 3)), a.map((v, j) => Math.floor((v + 2 * b[j]) / 3))];
      let indices = 0;
      for (let i = 0; i < 16; i++) {
        let best = Infinity, index = 0;
        for (let k = 0; k < 4; k++) { const error = colors[k].reduce((s, v, j) => s + (v - px[i][j]) ** 2, 0); if (error < best) { best = error; index = k; } }
        indices = (indices | index << (i * 2)) >>> 0;
      }
      view.setUint16(at + 8, c0, true); view.setUint16(at + 10, c1, true); view.setUint32(at + 12, indices, true); at += 16;
    }
    return out;
  }
  function writeDDS(im, format = 'DXT3', mipmaps = false) {
    checkImage(im);
    if (![im.width, im.height].every(n => (n & (n - 1)) === 0 && n <= 2048)) throw Error('DDS dimensions must be powers of two, up to 2048.');
    if (!['DXT3', 'RGBA'].includes(format)) throw Error('Choose DXT3 or uncompressed RGBA.');
    const levels = [im]; if (mipmaps) while (levels.at(-1).width > 1 || levels.at(-1).height > 1) levels.push(mip(levels.at(-1)));
    const blocks = levels.map(level => {
      if (format === 'DXT3') return dxt3(level);
      const out = new Uint8Array(level.data.length); for (let p = 0; p < out.length; p += 4) { out[p] = level.data[p + 2]; out[p + 1] = level.data[p + 1]; out[p + 2] = level.data[p]; out[p + 3] = level.data[p + 3]; } return out;
    });
    const out = new Uint8Array(128 + blocks.reduce((sum, b) => sum + b.length, 0)), v = new DataView(out.buffer);
    const u = (at, value) => v.setUint32(at, value, true);
    u(0, 0x20534444); u(4, 124); u(8, 0x1007 | (format === 'DXT3' ? 0x80000 : 8) | (mipmaps ? 0x20000 : 0));
    u(12, im.height); u(16, im.width); u(20, format === 'DXT3' ? blocks[0].length : im.width * 4); u(28, levels.length);
    u(76, 32); u(80, format === 'DXT3' ? 4 : 0x41);
    if (format === 'DXT3') u(84, 0x33545844);
    else { u(88, 32); u(92, 0x00ff0000); u(96, 0x0000ff00); u(100, 0x000000ff); u(104, 0xff000000); }
    u(108, 0x1000 | (levels.length > 1 ? 0x400008 : 0));
    let at = 128; for (const b of blocks) { out.set(b, at); at += b.length; } return out;
  }
  function crc32(b) { let crc = 0xffffffff; for (const c of b) { crc ^= c; for (let i = 0; i < 8; i++) crc = crc >>> 1 ^ (crc & 1 ? 0xedb88320 : 0); } return (crc ^ 0xffffffff) >>> 0; }
  function zip(files) {
    const entries = [], parts = []; let offset = 0;
    for (const file of files) {
      const name = new TextEncoder().encode(file.name), data = typeof file.data === 'string' ? new TextEncoder().encode(file.data) : new Uint8Array(file.data), crc = crc32(data);
      const local = new Uint8Array(30 + name.length), v = new DataView(local.buffer);
      v.setUint32(0, 0x04034b50, true); v.setUint16(4, 20, true); v.setUint16(6, 0x800, true); v.setUint16(12, 33, true);
      v.setUint32(14, crc, true); v.setUint32(18, data.length, true); v.setUint32(22, data.length, true); v.setUint16(26, name.length, true); local.set(name, 30);
      entries.push({ name, data, crc, offset }); parts.push(local, data); offset += local.length + data.length;
    }
    const centralStart = offset;
    for (const e of entries) {
      const h = new Uint8Array(46 + e.name.length), v = new DataView(h.buffer);
      v.setUint32(0, 0x02014b50, true); v.setUint16(4, 20, true); v.setUint16(6, 20, true); v.setUint16(8, 0x800, true); v.setUint16(14, 33, true);
      v.setUint32(16, e.crc, true); v.setUint32(20, e.data.length, true); v.setUint32(24, e.data.length, true); v.setUint16(28, e.name.length, true); v.setUint32(42, e.offset, true); h.set(e.name, 46); parts.push(h); offset += h.length;
    }
    const end = new Uint8Array(22), v = new DataView(end.buffer); v.setUint32(0, 0x06054b50, true); v.setUint16(8, entries.length, true); v.setUint16(10, entries.length, true); v.setUint32(12, offset - centralStart, true); v.setUint32(16, centralStart, true); parts.push(end);
    const result = new Uint8Array(offset + end.length); let at = 0; for (const p of parts) { result.set(p, at); at += p.length; } return result;
  }
  return { checkImage, resample, marker, readTGA, writeTGA, detectCells, replaceCell, restoreCell, verifyFont, writeDDS, mip, zip, crc32 };
}
if (typeof module !== 'undefined') module.exports = { createCiv4Core };
