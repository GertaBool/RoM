'use strict';
const C = createCiv4Core(), $ = id => document.getElementById(id);
const state = { mode: 'button', art: null, artName: '', activeFont: 'large', fonts: { large: null, small: null }, rendered: null, busy: false };
function status(message, error = false) { $('status').textContent = message; $('status').classList.toggle('error', error); }
function safeName(value) { return value.replace(/\.(dds|png|jpe?g|tga)$/i, '').replace(/[^a-z0-9_-]/gi, '_').replace(/_+/g, '_').slice(0, 80) || 'my_button'; }
function currentFont() { return state.fonts[state.activeFont]; }
function dimensions() {
  if (state.mode === 'font') { const f = currentFont(); return f && f.selected ? [f.selected.width, f.selected.height] : [32, 32]; }
  if ($('size').value !== 'custom') return [Number($('size').value), Number($('size').value)];
  const w = Number($('width').value), h = Number($('height').value);
  if (![w, h].every(n => Number.isInteger(n) && n >= 4 && n <= 2048 && (n & (n - 1)) === 0)) throw Error('Custom DDS dimensions must be powers of two from 4 to 2048.');
  return [w, h];
}
function canvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function pixels(c) { return { width: c.width, height: c.height, data: new Uint8Array(c.getContext('2d').getImageData(0, 0, c.width, c.height).data) }; }
function put(c, im) { c.width = im.width; c.height = im.height; c.getContext('2d').putImageData(new ImageData(new Uint8ClampedArray(im.data), im.width, im.height), 0, 0); }
function drawFramed(w, h) {
  const out = canvas(w, h), ctx = out.getContext('2d'); if (!state.art) return out;
  const source = state.art, art = canvas(source.width, source.height), a = art.getContext('2d'); a.drawImage(source, 0, 0);
  if ($('keyEnabled').checked) {
    const im = a.getImageData(0, 0, art.width, art.height), hex = $('keyColor').value, key = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16));
    const tolerance = Math.max(0, Math.min(180, Number($('keyTolerance').value) || 0));
    for (let p = 0; p < im.data.length; p += 4) {
      const distance = Math.max(...key.map((v, j) => Math.abs(v - im.data[p + j])));
      im.data[p + 3] = Math.round(im.data[p + 3] * Math.max(0, Math.min(1, (distance - tolerance) / 12)));
    }
    a.putImageData(im, 0, 0);
  }
  const pad = Math.min(Number($('padding').value), Math.floor((Math.min(w, h) - 1) / 2)), innerW = w - pad * 2, innerH = h - pad * 2;
  ctx.save();
  if (state.mode === 'button' && $('round').checked) { ctx.beginPath(); ctx.roundRect(0, 0, w, h, Math.min(w, h) / 8); ctx.clip(); }
  if (state.mode === 'button' && $('solidBg').checked) { ctx.fillStyle = $('bgColor').value; ctx.fillRect(0, 0, w, h); }
  const fit = $('fit').value;
  ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
  if (fit === 'cover') {
    const scale = Math.max(innerW / source.width, innerH / source.height), sw = innerW / scale, sh = innerH / scale;
    const sx = (source.width - sw) * Number($('focusX').value) / 100, sy = (source.height - sh) * Number($('focusY').value) / 100;
    ctx.drawImage(art, sx, sy, sw, sh, pad, pad, innerW, innerH);
  } else if (fit === 'stretch') ctx.drawImage(art, pad, pad, innerW, innerH);
  else {
    const scale = Math.min(innerW / source.width, innerH / source.height), dw = source.width * scale, dh = source.height * scale;
    ctx.drawImage(art, pad + (innerW - dw) / 2, pad + (innerH - dh) / 2, dw, dh);
  }
  if (state.mode === 'button' && $('rim').checked) {
    ctx.strokeStyle = '#d8b472'; ctx.lineWidth = Math.max(1, Math.min(w, h) / 64);
    const inset = ctx.lineWidth / 2;
    ctx.beginPath(); ctx.roundRect(inset, inset, w - inset * 2, h - inset * 2, $('round').checked ? Math.min(w, h) / 8 : 0); ctx.stroke();
  }
  ctx.restore(); return out;
}
function updateActions() {
  const f = currentFont(), art = !!state.rendered && !!state.art, busy = state.busy;
  $('exportDDS').disabled = !art || busy; $('exportPNG').disabled = !art || busy;
  $('applyGlyph').disabled = !art || !f?.selected || busy;
  $('undoGlyph').disabled = !f?.history.length || busy;
  $('exportFont').disabled = !f?.history.length || busy;
  $('exportPair').disabled = !state.fonts.large?.history.length || !state.fonts.small?.history.length || busy;
  $('selectCell').disabled = !f || busy;
}
function render() {
  $('customSize').hidden = $('size').value !== 'custom';
  $('focusX').disabled = $('focusY').disabled = $('fit').value !== 'cover';
  $('xmlSnippet').textContent = `<Button>Art/Interface/Buttons/Custom/${safeName($('outputName').value)}.dds</Button>`;
  $('previewContent').hidden = !state.art; $('emptyPreview').hidden = !!state.art;
  try {
    const [w, h] = dimensions(), maxPad = Math.min(12, Math.floor((Math.min(w, h) - 1) / 2));
    $('padding').max = maxPad; if (Number($('padding').value) > maxPad) $('padding').value = maxPad;
    $('paddingValue').textContent = $('padding').value;
    if (!state.art) { state.rendered = null; updateActions(); return; }
    state.rendered = drawFramed(w, h); const data = pixels(state.rendered); put($('preview'), data); put($('nativePreview'), data);
    const scale = 192 / Math.max(w, h); $('preview').style.width = `${w * scale}px`; $('preview').style.height = `${h * scale}px`;
    $('nativePreview').style.width = `${w}px`; $('nativePreview').style.height = `${h}px`;
    $('previewInfo').textContent = `${w} × ${h} pixels\n${state.mode === 'font' ? (currentFont()?.selected ? 'Selected cell artwork' : 'Select a font cell to set the size') : w <= 128 && h <= 128 ? 'Small view: actual size' : 'Small view: scaled to fit'}`;
  } catch (error) { state.rendered = null; status(error.message, true); }
  updateActions();
}
function selectMode(mode) {
  if ($('resourceWorkspace')) { $('resourceWorkspace').hidden = true; $('artWorkspace').hidden = false; $('resourceMode').setAttribute('aria-selected', 'false'); }
  state.mode = mode;
  $('buttonMode').setAttribute('aria-selected', mode === 'button'); $('fontMode').setAttribute('aria-selected', mode === 'font');
  for (const id of ['buttonSettings', 'buttonOutput', 'buttonFinish']) $(id).hidden = mode !== 'button';
  for (const id of ['fontSettings', 'fontOutput']) $(id).hidden = mode !== 'font';
  renderFont(); render(); status(mode === 'font' ? 'Load your original font sheet, then click the symbol you want to replace.' : 'Choose a size and format, then download your DDS.');
}
function renderFont() {
  const f = currentFont(), c = $('fontCanvas');
  $('largeTab').setAttribute('aria-pressed', state.activeFont === 'large'); $('smallTab').setAttribute('aria-pressed', state.activeFont === 'small');
  c.hidden = !f; $('emptyFont').hidden = !!f;
  if (!f) { $('cellInfo').textContent = 'No cell selected'; updateActions(); return; }
  const copy = new Uint8ClampedArray(f.image.data);
  if ($('showMarkers').checked) for (let p = 3; p < copy.length; p += 4) copy[p] = 255;
  c.width = f.image.width; c.height = f.image.height; const ctx = c.getContext('2d'); ctx.putImageData(new ImageData(copy, c.width, c.height), 0, 0);
  const zoom = Number($('fontZoom').value); c.style.width = `${c.width * zoom}px`; c.style.height = `${c.height * zoom}px`;
  if (f.selected) {
    const r = f.selected; ctx.strokeStyle = '#ffbb33'; ctx.lineWidth = 1; ctx.strokeRect(r.x - .5, r.y - .5, r.width + 1, r.height + 1);
    $('cellInfo').textContent = `Visual row ${r.row}, column ${r.col} · ${r.width} × ${r.height} px · ${f.history.length} replacement(s)`;
    $('cellRow').value = r.row; $('cellCol').value = r.col;
  } else $('cellInfo').textContent = `${f.cells.length} cells detected. Click a cell or enter its visual row and column.`;
  updateActions();
}
function chooseCell(r, scroll) {
  const f = currentFont(); if (!f || !r) { if (f) { f.selected = null; renderFont(); render(); } status('No detected cell at that position. Select inside a cell, not on a divider.', true); return; }
  f.selected = r; renderFont(); render();
  if (scroll) { const z = Number($('fontZoom').value); $('fontScroll').scrollLeft = Math.max(0, r.x * z - 60); $('fontScroll').scrollTop = Math.max(0, r.y * z - 60); }
  status(`Selected ${state.activeFont === 'large' ? 'GameFont' : 'GameFont_75'} row ${r.row}, column ${r.col}. This is a visual position, not a game index.`);
}
async function loadFont(file, role) {
  if (!file) return;
  if (state.fonts[role]?.history.length && !confirm('Replace this loaded sheet and discard its unsaved edits? Download it first if you want to keep them.')) return;
  try {
    if (file.size > 80 * 1024 * 1024) throw Error('This TGA is too large. Limit: 80 MB.');
    const image = C.readTGA(await file.arrayBuffer());
    if (image.bits !== 32 || (image.descriptor & 15) !== 8) throw Error('GameFont needs a 32-bit TGA with 8 alpha bits. This file does not declare that format.');
    const cells = C.detectCells(image); if (!cells.length) throw Error('No intact GameFont cell grid was detected. Use an original sheet with magenta/cyan dividers.');
    state.fonts[role] = { image, original: { width: image.width, height: image.height, data: image.data.slice() }, cells, selected: null, history: [], fileName: file.name };
    $(role === 'large' ? 'fontInfo' : 'smallFontInfo').textContent = `${file.name} · ${image.width} × ${image.height} · ${cells.length} cells`;
    state.activeFont = role; renderFont(); render(); status('Sheet loaded. Select the cell that already belongs to your symbol.');
  } catch (error) { status(error.message, true); }
}
function download(name, data, type = 'application/octet-stream') {
  const url = URL.createObjectURL(data instanceof Blob ? data : new Blob([data], { type })), a = document.createElement('a');
  a.href = url; a.download = name; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 60000);
}
function fontExport(role) {
  const f = state.fonts[role]; if (!f || !f.history.length) throw Error('Apply artwork to this sheet first.');
  const changedPixels = C.verifyFont(f.original, f.image, f.history.map(h => h.cell)), bytes = C.writeTGA(f.image, f.image);
  const decoded = C.readTGA(bytes); C.verifyFont(f.original, decoded, f.history.map(h => h.cell));
  for (let p = 0; p < decoded.data.length; p++) if (decoded.data[p] !== f.image.data[p]) throw Error('TGA round-trip check failed.');
  return { bytes, log: { output: role === 'large' ? 'GameFont.tga' : 'GameFont_75.tga', input: f.fileName, width: f.image.width, height: f.image.height, changedPixels, replacements: f.history.map(h => ({ ...h.cell, artwork: h.artwork })), markerPixelsPreserved: true, gameIndexNotInferred: true } };
}
async function encodeDDS(im, format, mips) {
  const source = `const C=(${createCiv4Core.toString()})();onmessage=e=>{try{const r=C.writeDDS(e.data.im,e.data.format,e.data.mips);postMessage({bytes:r},[r.buffer]);}catch(error){postMessage({error:error.message});}};`;
  const url = URL.createObjectURL(new Blob([source], { type: 'text/javascript' })); let worker;
  try {
    worker = new Worker(url);
    return await new Promise((resolve, reject) => {
      worker.onmessage = e => e.data.error ? reject(Error(e.data.error)) : resolve(e.data.bytes);
      worker.onerror = () => reject(Error('The browser could not start the local encoder. Open this file in a current version of Chrome, Edge or Firefox.'));
      worker.postMessage({ im, format, mips }, [im.data.buffer]);
    });
  } finally { worker?.terminate(); URL.revokeObjectURL(url); }
}
$('artFile').addEventListener('change', async e => {
  const file = e.target.files[0]; if (!file) return;
  try {
    if (!/\.(png|jpe?g)$/i.test(file.name) || file.size > 50 * 1024 * 1024) throw Error('Choose a JPG or PNG up to 50 MB.');
    const image = await createImageBitmap(file, { imageOrientation: 'from-image' });
    if (image.width * image.height > 40000000) { image.close(); throw Error('Use artwork up to 40 megapixels.'); }
    // Keep a high-quality working image; avoid allocating a full-resolution canvas on every slider movement.
    const scale = Math.min(1, 2048 / Math.max(image.width, image.height)), working = canvas(Math.max(1, Math.round(image.width * scale)), Math.max(1, Math.round(image.height * scale)));
    const ctx = working.getContext('2d'); ctx.imageSmoothingQuality = 'high'; ctx.drawImage(image, 0, 0, working.width, working.height);
    $('artInfo').textContent = `${file.name} · ${image.width} × ${image.height}${scale < 1 ? ' · working copy reduced to 2048 px' : ''}`; image.close();
    state.art = working; state.artName = file.name; $('outputName').value = safeName(file.name); render(); status('Artwork loaded. Adjust framing, then export a button or choose a font cell.');
  } catch (error) { status('Could not load artwork: ' + error.message, true); }
});
$('buttonMode').onclick = () => selectMode('button'); $('fontMode').onclick = () => selectMode('font');
for (const id of ['fit', 'focusX', 'focusY', 'padding', 'keyEnabled', 'keyColor', 'keyTolerance', 'solidBg', 'bgColor', 'round', 'rim', 'size', 'format', 'mipmaps', 'width', 'height', 'outputName']) $(id).addEventListener('input', render);
$('resetFraming').onclick = () => { $('fit').value = 'contain'; $('focusX').value = $('focusY').value = '50'; $('padding').value = '2'; $('keyEnabled').checked = false; render(); status('Framing reset.'); };
$('fontFile').onchange = e => loadFont(e.target.files[0], 'large'); $('smallFontFile').onchange = e => loadFont(e.target.files[0], 'small');
$('largeTab').onclick = () => { state.activeFont = 'large'; renderFont(); render(); }; $('smallTab').onclick = () => { state.activeFont = 'small'; renderFont(); render(); };
$('fontZoom').oninput = renderFont; $('showMarkers').oninput = renderFont;
$('fontCanvas').onclick = e => { const f = currentFont(); if (!f) return; const b = e.target.getBoundingClientRect(), x = (e.clientX - b.left) * f.image.width / b.width, y = (e.clientY - b.top) * f.image.height / b.height; chooseCell(f.cells.find(r => x >= r.x && x < r.x + r.width && y >= r.y && y < r.y + r.height), false); };
$('selectCell').onclick = () => { const f = currentFont(); chooseCell(f?.cells.find(r => r.row === Number($('cellRow').value) && r.col === Number($('cellCol').value)), true); };
$('applyGlyph').onclick = () => {
  try {
    const f = currentFont(); if (!f?.selected || !state.rendered) throw Error('Choose artwork and a font cell first.');
    const result = C.replaceCell(f.image, f.selected, pixels(state.rendered));
    f.history.push({ cell: { ...f.selected }, before: result.before, artwork: state.artName }); renderFont();
    status(`Artwork applied to ${state.activeFont === 'large' ? 'GameFont' : 'GameFont_75'}. Grid and marker pixels preserved.${result.avoided ? ` ${result.avoided} reserved-color pixels adjusted by one blue level.` : ''} Download to keep these edits.`);
  } catch (error) { status(error.message, true); }
};
$('undoGlyph').onclick = () => { const f = currentFont(); if (!f?.history.length) return; const last = f.history.pop(); C.restoreCell(f.image, last.cell, last.before); renderFont(); status('Last replacement undone.'); };
$('exportFont').onclick = () => { try { const r = fontExport(state.activeFont); download(r.log.output, r.bytes); status(`Downloaded ${r.log.output}. ${r.log.changedPixels} changed pixels; all markers and unrelated pixels preserved.`); } catch (error) { status(error.message, true); } };
$('exportPair').onclick = () => {
  try {
    const a = fontExport('large'), b = fontExport('small');
    const log = { tool: 'Civ IV Art Studio 1.0', files: [a.log, b.log], note: 'Visual row and column are not game symbol IDs. Replace existing assigned cells; XML indices are unchanged. Back up original fonts and test in game.' };
    const bytes = C.zip([{ name: 'GameFont.tga', data: a.bytes }, { name: 'GameFont_75.tga', data: b.bytes }, { name: 'edit-log.json', data: JSON.stringify(log, null, 2) }, { name: 'READ-ME.txt', data: 'Back up your original files. Place the two TGA files in your mod Assets/res/Fonts folder. Symbol XML indices are not changed by this tool. Test both font sizes in game. Magenta and cyan marker pixels and all pixels outside your edited cells were verified unchanged.\n' }]);
    download('GameFont-edited.zip', bytes, 'application/zip'); status('Both edited font sheets and their change log downloaded.');
  } catch (error) { status(error.message, true); }
};
$('exportDDS').onclick = async () => {
  if (!state.rendered || state.busy) return;
  state.busy = true; updateActions(); status('Encoding DDS…');
  try { const name = safeName($('outputName').value), im = pixels(state.rendered), format = $('format').value, mips = $('mipmaps').checked; const bytes = await encodeDDS(im, format, mips); download(name + '.dds', bytes); status(`${name}.dds downloaded · ${format}${mips ? ' with mipmaps' : ', no mipmaps'}.`); }
  catch (error) { status(error.message, true); }
  finally { state.busy = false; updateActions(); }
};
$('exportPNG').onclick = () => { if (state.rendered) { const name = safeName($('outputName').value); state.rendered.toBlob(blob => { if (blob) download(name + '.png', blob, 'image/png'); else status('PNG export failed.', true); }); } };
$('copyXML').onclick = async () => { try { await navigator.clipboard.writeText($('xmlSnippet').textContent); status('Button XML copied.'); } catch { status('Select the XML text and copy it manually; this browser does not allow clipboard access here.'); } };
window.addEventListener('beforeunload', e => { if (Object.values(state.fonts).some(f => f?.history.length)) { e.preventDefault(); e.returnValue = ''; } });
// Keyboard access for the mode tabs.
for (const id of ['buttonMode', 'fontMode', 'resourceMode']) $(id).addEventListener('keydown', e => { if (['ArrowLeft','ArrowRight'].includes(e.key)) { e.preventDefault(); const tabs=['buttonMode','fontMode','resourceMode'], next=tabs[(tabs.indexOf(id)+(e.key==='ArrowRight'?1:2))%3]; $(next).click(); $(next).focus(); } });
render(); renderFont();
