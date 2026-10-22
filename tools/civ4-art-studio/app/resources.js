'use strict';
// Resource workshop: explicit, template-based edits; original files are never written.
const R = { files: new Map(), docs: [], records: {}, texts: new Map(), translations: {}, language: 'English', artwork: null, slots: {}, fonts: {}, plan: null, dirty: false, loading: false };
const languages = ['English', 'French', 'German', 'Italian', 'Spanish'];
const entryTags = ['BonusInfo','BonusArtInfo','TechInfo','TerrainInfo','BonusClassInfo','ImprovementInfo','BuildingInfo','UnitInfo'];
const direct = (node, tag) => [...node.children].find(n => n.localName === tag);
const value = (node, tag) => direct(node, tag)?.textContent.trim() || '';
const typeOf = node => value(node, 'Type');
const readable = text => text.replace(/^(BONUS|ART_DEF_BONUS|TECH|IMPROVEMENT|BUILDING|UNIT|TERRAIN|BONUSCLASS)_/, '').toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
const selected = id => [...$(id).selectedOptions].map(o => o.value);
function sayResource(message, error = false) { $('resourceStatus').textContent = message; $('resourceStatus').classList.toggle('error', error); }
function invalidateResource() { R.plan = null; R.dirty = true; $('downloadResource').disabled = true; $('resourceReview').hidden = true; }
function xmlParse(text, path) {
  if (/<!DOCTYPE|<!ENTITY/i.test(text)) throw Error(`${path}: external entities and DTDs are not supported.`);
  const doc = new DOMParser().parseFromString(text.replace(/>\s+</g, '><'), 'application/xml');
  if (doc.getElementsByTagName('parsererror').length) throw Error(`${path}: invalid XML; fix the file before editing.`);
  return doc;
}
function setValue(node, tag, text) { const target = direct(node, tag); if (!target) throw Error(`Template is missing ${tag}. Choose a compatible Civ IV template.`); target.textContent = String(text); }
function child(node, tag, text) { const el = node.ownerDocument.createElementNS(node.namespaceURI, tag); if (text !== undefined) el.textContent = String(text); return el; }
function listValues(node, tag, item, values) { const target = direct(node, tag); if (!target) throw Error(`Template is missing ${tag}.`); target.replaceChildren(...values.map(v => child(node, item, v))); }
function integer(id, min = -100, max = 100) { const n = Number($(id).value); if (!$(id).value.trim() || !Number.isInteger(n) || n < min || n > max) throw Error(`${$(id).labels?.[0]?.firstChild?.textContent || id}: enter a whole number between ${min} and ${max}.`); return n; }
function records(tag) { return R.records[tag] || []; }
function record(tag, type) { const matches = records(tag).filter(r => typeOf(r.node) === type); if (matches.length !== 1) throw Error(`${type}: ${matches.length ? 'multiple definitions; module load order must be resolved before editing' : 'definition not found'}.`); return matches[0]; }
function labelFor(node) { const key = value(node, 'Description'); return R.texts.get(key)?.English || readable(typeOf(node)); }
function options(id, rows, none = false) {
  const el = $(id); el.replaceChildren(); if (none) el.add(new Option('None', 'NONE'));
  const counts = new Map(); rows.forEach(r => counts.set(typeOf(r.node), (counts.get(typeOf(r.node)) || 0) + 1));
  rows.filter((r,i,a) => a.findIndex(x => typeOf(x.node) === typeOf(r.node)) === i).sort((a,b) => labelFor(a.node).localeCompare(labelFor(b.node))).forEach(r => {
    const type = typeOf(r.node), o = new Option(`${labelFor(r.node)}${counts.get(type) > 1 ? ' [multiple definitions]' : ''}`, type); o.disabled = counts.get(type) > 1; el.add(o);
  });
}
function chooseMany(id, types) { const set = new Set(types); for (const o of $(id).options) o.selected = set.has(o.value); }
async function readXML(file, path) {
  const bytes = await file.arrayBuffer(), head = new TextDecoder().decode(bytes.slice(0, 250));
  const encoding = head.match(/encoding\s*=\s*["']([^"']+)/i)?.[1] || 'utf-8';
  let text; try { text = new TextDecoder(encoding, { fatal: true }).decode(bytes); } catch { throw Error(`${path}: cannot decode ${encoding}.`); }
  return { path, text, doc: xmlParse(text, path), bytes: new Uint8Array(bytes) };
}
async function loadMod(files) {
  if (R.loading) return;
  if (R.dirty && !confirm('Load another folder and discard the current draft? Save the draft first if needed.')) return;
  R.loading = true; R.plan = null; R.dirty = false; R.files = new Map(); R.docs = []; R.records = {}; R.texts = new Map(); R.fonts = {}; R.slots = {}; R.artwork = null;
  $('resourceFields').disabled = true; $('reviewResource').disabled = $('downloadResource').disabled = $('saveRecipe').disabled = true;
  $('resourceReview').hidden = true; $('slotVerified').checked = false; $('resourceArtwork').value = ''; $('resourcePreview').getContext('2d').clearRect(0,0,64,64); $('resourceArtworkInfo').textContent='No new artwork. The selected resource’s button is retained.';
  try {
    sayResource('Reading the selected folder…');
    for (const file of files) {
      const name = file.webkitRelativePath || file.name, parts = name.replaceAll('\\','/').split('/'), start = parts.findIndex(p => p.toLowerCase() === 'assets');
      if (start < 0) continue; const path = parts.slice(start).join('/');
      if (parts.some(p => p === '..') || R.files.has(path.toLowerCase())) throw Error('Ambiguous or unsafe file paths in the folder.');
      R.files.set(path.toLowerCase(), { file, path });
    }
    if (!R.files.size) throw Error('Choose a mod folder containing Assets, or the Assets folder itself.');
    const candidates = [...R.files.values()].filter(x => /\.xml$/i.test(x.path) && !/schema\.xml$/i.test(x.path));
    for (let i = 0; i < candidates.length; i++) {
      const item = candidates[i];
      // Only files used by this editor. Include every matching module, regardless of activation.
      if (!/(?:BonusInfos|ArtDefines_Bonus|TechInfos|TerrainInfos|BonusClassInfos|ImprovementInfos|BuildingInfos|UnitInfos)\.xml$/i.test(item.path) && !/\/Text\//i.test(item.path)) continue;
      if (item.file.size > 40 * 1024 * 1024) throw Error(`${item.path} exceeds the 40 MB XML limit.`);
      const d = await readXML(item.file, item.path); if (!/\/Text\//i.test(item.path)) R.docs.push(d);
      for (const tag of entryTags) for (const node of d.doc.getElementsByTagName(tag)) {
        if (!typeOf(node)) continue; (R.records[tag] ||= []).push({ node, source: d });
      }
      for (const node of d.doc.getElementsByTagName('TEXT')) {
        const key = value(node, 'Tag'); if (!key) continue;
        const translated = {};
        for (const lang of languages) { const el = direct(node, lang); translated[lang] = el ? (direct(el, 'Text')?.textContent || el.textContent).trim() : ''; }
        // Used only as display labels / starting text. Existing text documents are not modified.
        if (!R.texts.has(key)) R.texts.set(key, translated);
      }
      if (i % 15 === 0) { sayResource(`Reading mod definitions… ${i + 1}/${candidates.length}`); await new Promise(resolve => setTimeout(resolve, 0)); }
    }
    if (!records('BonusInfo').length || !records('BonusArtInfo').length) throw Error('No resource definitions and resource art definitions were found.');
    options('resourceTemplate', records('BonusInfo')); options('resourceArt', records('BonusArtInfo'));
    for (const id of ['revealTech','tradeTech','obsoleteTech']) options(id, records('TechInfo'), true);
    options('resourceClass', records('BonusClassInfo'));
    if (!$('resourceClass').options.length) { const classes = [...new Set(records('BonusInfo').map(r => value(r.node,'BonusClassType')))]; for (const c of classes) $('resourceClass').add(new Option(readable(c),c)); }
    options('resourceImprovements', records('ImprovementInfo')); options('resourceProducers', records('BuildingInfo')); options('resourceBuildings', records('BuildingInfo')); options('resourceUnits', records('UnitInfo'));
    $('terrainOptions').replaceChildren(); for (const r of records('TerrainInfo')) { const l = document.createElement('label'); l.className = 'check'; const input = document.createElement('input'); input.type = 'checkbox'; input.value = typeOf(r.node); l.append(input, document.createTextNode(labelFor(r.node))); $('terrainOptions').append(l); }
    for (const [role, name] of [['large','GameFont.tga'],['small','GameFont_75.tga']]) {
      const item = R.files.get(`assets/res/fonts/${name.toLowerCase()}`); if (!item) continue;
      if (item.file.size > 80 * 1024 * 1024) throw Error('GameFont exceeds 80 MB.');
      const im = C.readTGA(await item.file.arrayBuffer()); if (im.bits !== 32 || (im.descriptor & 15) !== 8) throw Error(`${name} needs 32-bit RGBA.`);
      R.fonts[role] = { image: im, cells: C.detectCells(im), path: item.path };
    }
    $('resourceTemplate').value = records('BonusInfo').some(r => typeOf(r.node) === 'BONUS_BAUXITE') ? 'BONUS_BAUXITE' : [...$('resourceTemplate').options].find(o => !o.disabled)?.value || '';
    $('modSummary').textContent = `${records('BonusInfo').length} resource definitions · ${records('BuildingInfo').length} buildings · ${records('UnitInfo').length} units. Modules included in collision checks.`;
    $('resourceFields').disabled = false; $('reviewResource').disabled = $('saveRecipe').disabled = false;
    populateResource(); sayResource('Mod loaded. Choose a template and name your resource.'); R.dirty = false;
  } catch (error) { sayResource(error.message, true); $('modSummary').textContent = 'Folder could not be loaded.'; }
  finally { R.loading = false; }
}
function populateResource() {
  try {
    const r = record('BonusInfo', $('resourceTemplate').value), n = r.node, editing = $('resourceAction').value === 'edit';
    for(const id of ['resourceImprovements','resourceProducers','resourceBuildings','resourceUnits']) { $(id+'Search').value=''; for(const o of $(id).options)o.hidden=false; }
    $('resourceName').value = editing ? labelFor(n) : ''; $('resourceID').value = editing ? typeOf(n) : ''; $('resourceID').readOnly = editing;
    $('resourceKind').value = Number(value(n,'iPlacementOrder')) < 0 ? 'manufactured' : 'natural'; $('resourceClass').value = value(n,'BonusClassType');
    for (const [id,tag] of Object.entries({ revealTech:'TechReveal', tradeTech:'TechCityTrade', obsoleteTech:'TechObsolete', resourceHealth:'iHealth', resourceHappiness:'iHappiness', appearance:'iConstAppearance' })) $(id).value = value(n,tag);
    $('placementOrder').value = Math.max(0, Number(value(n,'iPlacementOrder')));
    const yields = [...(direct(n,'YieldChanges')?.children || [])].map(x => x.textContent);
    ['yieldFood','yieldProduction','yieldCommerce'].forEach((id,i) => $(id).value = yields[i] || '0');
    $('resourceHills').checked = value(n,'bHills') === '1'; $('resourceFlat').checked = value(n,'bFlatlands') === '1';
    const terrains = [...(direct(n,'TerrainBooleans')?.children || [])].filter(x => value(x,'bTerrain') === '1').map(x => value(x,'TerrainType'));
    for (const cb of $('terrainOptions').querySelectorAll('input')) cb.checked = terrains.includes(cb.value);
    $('placementSummary').textContent = `Inherited: latitude ${value(n,'iMinLatitude')}–${value(n,'iMaxLatitude')}, minimum area ${value(n,'iMinAreaSize')}, player scaling ${value(n,'iPlayer')}, tiles per resource ${value(n,'iTilesPer')}. Forest/jungle eligibility, grouping and random weights stay as in ${labelFor(n)}.`;
    const impTypes = records('ImprovementInfo').filter(r => [...(direct(r.node,'BonusTypeStructs')?.children || [])].some(x => value(x,'BonusType') === typeOf(n) && value(x,'bBonusTrade') === '1')).map(r => typeOf(r.node));
    chooseMany('resourceImprovements', impTypes);
    for (const [id,tag,field] of [['resourceProducers','BuildingInfo','FreeBonus'],['resourceBuildings','BuildingInfo','Bonus'],['resourceUnits','UnitInfo','BonusType']]) {
      for (const o of $(id).options) {
        const matches = records(tag).filter(r => typeOf(r.node) === o.value), other = matches.length === 1 ? value(matches[0].node,field) : 'CONFLICT';
        o.disabled = matches.length !== 1 || (!!other && other !== 'NONE' && !(editing && other === typeOf(n)));
        o.selected = editing && other === typeOf(n);
      }
    }
    const producers = records('BuildingInfo').filter(r => value(r.node,'FreeBonus') === typeOf(n));
    $('producerCount').value = editing && producers.length ? value(producers[0].node,'iNumFreeBonuses') : '1';
    $('resourceArt').value = value(n,'ArtDefineTag'); $('resourceSymbol').value = 'inherit'; $('slotVerified').checked = false; R.slots = {};
    const names = R.texts.get(value(n,'Description')) || {}, pedia = R.texts.get(value(n,'Civilopedia')) || {};
    R.translations = Object.fromEntries(languages.map(l => [l, { name: editing ? names[l] || '' : '', pedia: editing ? pedia[l] || '' : '' }]));
    R.language = 'English'; $('textLanguage').value = 'English'; showLanguage(); kindChanged(); artChanged(); slotRows(); invalidateResource();
  } catch (e) { sayResource(e.message, true); }
}
function kindChanged() { const natural=$('resourceKind').value==='natural'; $('naturalSettings').hidden=!natural; $('resourceImprovements').disabled=!natural; if(!natural)chooseMany('resourceImprovements',[]); }
function artChanged() {
  try { const a = record('BonusArtInfo', $('resourceArt').value).node;
    $('resourceArtInfo').textContent = `Map model: ${value(a,'NIF') || 'none'} · existing text-symbol index: ${value(a,'FontButtonIndex')}. The model’s textures remain in your mod.`;
    $('resourceSlotPanel').hidden = $('resourceSymbol').value !== 'custom'; slotOccupancy();
  } catch (e) { sayResource(e.message,true); }
}
function saveLanguage() { R.translations[R.language] = { name: $('translatedName').value, pedia: $('resourcePedia').value }; }
function showLanguage() { const t = R.translations[R.language] || {}; $('translatedName').value = t.name || ''; $('resourcePedia').value = t.pedia || ''; }
function slotOccupancy() {
  const index = Number($('resourceIndex').value), occupied = records('BonusArtInfo').filter(r => Number(value(r.node,'FontButtonIndex')) === index);
  $('slotOccupancy').textContent = occupied.length ? `Occupied: ${occupied.map(r => readable(typeOf(r.node))).join(', ')}. Choose another index; shared or modular symbols are protected.` : 'No resource art definition in the selected folder references this number. This does not establish that the cell is free or that the DLL maps this number to it.';
  return occupied;
}
function slotRows() {
  const f = R.fonts[$('slotSize').value]; $('slotRow').replaceChildren();
  if (f) for (const row of [...new Set(f.cells.map(c => c.row))]) $('slotRow').add(new Option(`Row ${row}`,row));
  slotGallery();
}
function slotGallery() {
  const role = $('slotSize').value, f = R.fonts[role], row = Number($('slotRow').value), gallery = $('slotGallery'); gallery.replaceChildren();
  if (!f) { gallery.textContent = 'This font was not found in Assets/res/Fonts.'; return; }
  for (const cell of f.cells.filter(c => c.row === row)) {
    const b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-pressed', R.slots[role]?.row === cell.row && R.slots[role]?.col === cell.col ? 'true' : 'false');
    const c = canvas(cell.width, cell.height), data = new Uint8Array(cell.width * cell.height * 4);
    for (let y=0;y<cell.height;y++) data.set(f.image.data.subarray(((cell.y+y)*f.image.width+cell.x)*4,((cell.y+y)*f.image.width+cell.x+cell.width)*4),y*cell.width*4);
    put(c,{width:cell.width,height:cell.height,data}); b.append(c,document.createTextNode(`Column ${cell.col}`)); b.onclick = () => { R.slots[role] = {...cell}; $('slotVerified').checked = false; invalidateResource(); slotGallery(); }; gallery.append(b);
  }
  $('slotSelection').textContent = ['large','small'].map(k => `${k === 'large' ? 'GameFont' : 'GameFont_75'}: ${R.slots[k] ? `row ${R.slots[k].row}, column ${R.slots[k].col}` : 'not selected'}`).join(' · ');
}
function resourceImage(w,h) {
  const c = canvas(w,h), ctx = c.getContext('2d'), im = R.artwork; if (!im) return c;
  const pad = Math.min(2, Math.floor(Math.min(w,h)/8)), scale = Math.min((w-pad*2)/im.width,(h-pad*2)/im.height);
  ctx.imageSmoothingQuality = 'high'; ctx.drawImage(im,(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale); return c;
}
function serialized(node) { return new XMLSerializer().serializeToString(node).replace(/ xmlns="[^"]*"/, ''); }
function patchDocument(source, edits, additions) {
  let text = source.text;
  for (const {original,node} of edits) {
    const tag = original.localName, target = typeOf(original), pattern = new RegExp(`<${tag}(?:\\s[^>]*)?>[\\s\\S]*?<\\/${tag}\\s*>`, 'g');
    let hits = 0;
    text = text.replace(pattern, raw => { const m = raw.match(/<Type\s*>\s*([^<]+)\s*<\/Type>/); if (m?.[1].trim() !== target) return raw; hits++; return serialized(node); });
    if (hits !== 1) throw Error(`${source.path}: could not uniquely locate ${target}; no patch exported.`);
  }
  for (const {parent,node} of additions) { const closing = `</${parent}>`; if (text.split(closing).length !== 2) throw Error(`${source.path}: ambiguous container ${parent}.`); text = text.replace(closing, `${serialized(node)}\n\t${closing}`); }
  if (/^\s*<\?xml/i.test(text)) text = text.replace(/<\?xml[^?]*\?>/, '<?xml version="1.0" encoding="UTF-8"?>'); else text = '<?xml version="1.0" encoding="UTF-8"?>\n'+text;
  xmlParse(text,source.path); return text;
}
function recipe() {
  saveLanguage(); const fields = {};
  for (const el of $('resourceFields').querySelectorAll('input,select,textarea')) {
    if (!el.id || el.type === 'file' || ['slotRow','slotSize','textLanguage','translatedName','resourcePedia','slotVerified'].includes(el.id)) continue;
    fields[el.id] = el.multiple ? selected(el.id) : el.type === 'checkbox' ? el.checked : el.value;
  }
  return {format:'civ4-resource-draft',version:1,fields,terrains:[...$('terrainOptions').querySelectorAll('input:checked')].map(x=>x.value),translations:R.translations,slots:R.slots};
}
async function sha256(data) { if (!crypto.subtle) throw Error('This browser requires localhost or a secure context for backup checksums. Serve the app locally if needed.'); return [...new Uint8Array(await crypto.subtle.digest('SHA-256', typeof data === 'string' ? new TextEncoder().encode(data) : data))].map(x=>x.toString(16).padStart(2,'0')).join(''); }
async function prepareResource() {
  saveLanguage();
  const editing = $('resourceAction').value === 'edit', template = record('BonusInfo',$('resourceTemplate').value), type = $('resourceID').value.trim(), name = $('resourceName').value.trim(), natural = $('resourceKind').value === 'natural';
  if (!/^BONUS_[A-Z][A-Z0-9_]{0,63}$/.test(type)) throw Error('Use an identifier such as BONUS_LITHIUM (uppercase letters, numbers and underscores).');
  if (!name) throw Error('Enter the resource’s display name.');
  if (editing && type !== typeOf(template.node)) throw Error('An existing resource cannot be renamed internally.');
  if (!editing && records('BonusInfo').some(r=>typeOf(r.node)===type)) throw Error('That resource identifier is already used, including in modules.');
  const english = R.translations.English || {}; english.name = name; R.translations.English = english;
  if (!english.pedia?.trim()) throw Error('Write an English Civilopedia description before exporting.');
  const n = template.node.cloneNode(true), artTemplate = record('BonusArtInfo',$('resourceArt').value), a = artTemplate.node.cloneNode(true), artType = `ART_DEF_${type}_STUDIO`, textKey = `TXT_KEY_${type}_STUDIO`;
  const existingArt = records('BonusArtInfo').filter(r=>typeOf(r.node)===artType);
  const ownArt = editing && value(template.node,'ArtDefineTag') === artType && existingArt.length === 1 && !records('BonusInfo').some(r=>typeOf(r.node)!==type && value(r.node,'ArtDefineTag')===artType);
  if(existingArt.length && !ownArt) throw Error('The generated art identifier is already used by another definition.');
  const ownText = editing && value(template.node,'Description')===textKey && value(template.node,'Civilopedia')===textKey+'_PEDIA';
  if ((R.texts.has(textKey) || R.texts.has(textKey+'_PEDIA')) && !ownText) throw Error('Generated text keys already exist. Choose a unique resource identifier.');
  for (const [tag,v] of Object.entries({Type:type, Description:textKey, Civilopedia:textKey+'_PEDIA', ArtDefineTag:artType, BonusClassType:$('resourceClass').value, TechReveal:$('revealTech').value, TechCityTrade:$('tradeTech').value, TechObsolete:$('obsoleteTech').value, iHealth:integer('resourceHealth'),iHappiness:integer('resourceHappiness')})) setValue(n,tag,v);
  if (!$('resourceClass').value) throw Error('Choose a resource class.');
  for (const id of ['revealTech','tradeTech','obsoleteTech']) if (!$(id).value) throw Error('Choose a technology or None for each discovery setting.');
  listValues(n,'YieldChanges','iYieldChange',['yieldFood','yieldProduction','yieldCommerce'].map(id=>integer(id)));
  const terrain = direct(n,'TerrainBooleans'); if (!terrain) throw Error('Template has no terrain list.');
  if (natural) {
    setValue(n,'iPlacementOrder',integer('placementOrder',0,100)); setValue(n,'iConstAppearance',integer('appearance',0,10000)); setValue(n,'bHills',$('resourceHills').checked ? 1:0); setValue(n,'bFlatlands',$('resourceFlat').checked ? 1:0);
    const chosen = [...$('terrainOptions').querySelectorAll('input:checked')].map(x=>x.value);
    if (!chosen.length && !direct(n,'FeatureBooleans')?.children.length) throw Error('Choose eligible terrain for a natural resource.');
    terrain.replaceChildren(...chosen.map(t => { const el = child(n,'TerrainBoolean'); el.append(child(n,'TerrainType',t),child(n,'bTerrain',1)); return el; }));
  } else {
    for (const [tag,v] of Object.entries({iPlacementOrder:-1,iConstAppearance:0,iPlayer:0,iTilesPer:0,bHills:0,bFlatlands:0,bNormalize:0})) setValue(n,tag,v);
    for (const tag of ['TerrainBooleans','FeatureBooleans','FeatureTerrainBooleans']) direct(n,tag)?.replaceChildren();
    for (const x of direct(n,'Rands')?.children || []) x.textContent='0';
    if (!selected('resourceProducers').length) throw Error('Choose at least one building to produce a manufactured resource.');
  }
  if(!/^\d+$/.test(value(a,'FontButtonIndex')))throw Error('Selected art has no valid font index.');
  setValue(a,'Type',artType);
  const changes = new Map(), extra = [], notes = [], changeLog = [];
  const group = source => { if (!changes.has(source.path)) changes.set(source.path,{source,edits:[],additions:[]}); return changes.get(source.path); };
  const edit = (r,node) => { group(r.source).edits.push({original:r.node,node}); };
  const add = (r,node) => group(r.source).additions.push({parent:r.node.parentNode.localName,node});
  if (editing) edit(template,n); else add(template,n); if(ownArt)edit(existingArt[0],a);else add(artTemplate,a);
  const buttonPath = `Assets/Art/Interface/Buttons/Custom/${type.toLowerCase()}.dds`;
  if (R.artwork) { if (R.files.has(buttonPath.toLowerCase()) && !(ownArt && value(existingArt[0].node,'Button').toLowerCase()===buttonPath.slice(7).toLowerCase())) throw Error('The generated button path already exists; choose a different resource identifier.'); setValue(a,'Button',buttonPath.slice(7)); extra.push({name:buttonPath,data:C.writeDDS(pixels(resourceImage(64,64)),'DXT3',false)}); }
  let testOnly = false;
  if ($('resourceSymbol').value === 'custom') {
    const index = integer('resourceIndex',0,4095); if (slotOccupancy().length) throw Error('That font index is already referenced. Choose an unused resource index.');
    if (!R.artwork) throw Error('Choose PNG/JPG artwork for the custom symbol.');
    setValue(a,'FontButtonIndex',index); testOnly = !$('slotVerified').checked;
    for (const role of ['large','small']) {
      const f = R.fonts[role], cell = R.slots[role]; if (!f || !cell || !f.cells.some(c=>c.row===cell.row && c.col===cell.col && c.x===cell.x && c.y===cell.y && c.width===cell.width && c.height===cell.height)) throw Error('Select a valid symbol cell in each font size.');
      // Do not overwrite artwork hidden in an apparently blank cell; custom mode is for empty slots only.
      for(let y=cell.y;y<cell.y+cell.height;y++) for(let x=cell.x;x<cell.x+cell.width;x++) { const p=(y*f.image.width+x)*4; if (!C.marker(f.image.data,p) && f.image.data[p+3]>0) throw Error(`${role}: selected cell already contains visible artwork. Choose an empty slot.`); }
      const copy = {...f.image,data:f.image.data.slice()}; C.replaceCell(copy,cell,pixels(resourceImage(cell.width,cell.height))); C.verifyFont(f.image,copy,[cell]);
      const bytes=C.writeTGA(copy,f.image), decoded=C.readTGA(bytes); C.verifyFont(f.image,decoded,[cell]);
      if (decoded.data.some((v,i)=>v!==copy.data[i])) throw Error('GameFont round-trip validation failed.');
      extra.push({name:f.path,data:bytes});
    }
    notes.push(testOnly ? 'TEST ONLY: custom font mapping has not been verified in game.' : 'Custom font mapping is user-verified; no automatic DLL/index verification is claimed.');
  } else notes.push(`Reuses ${labelFor(artTemplate.node)} text symbol (index ${value(a,'FontButtonIndex')}); font sheets stay unchanged.`);
  // Improvement connections: copy bonus structs while preserving all unrelated definitions.
  const chosenImp=new Set(natural?selected('resourceImprovements'):[]);
  for (const r of records('ImprovementInfo')) {
    const sourceList=direct(r.node,'BonusTypeStructs'); if(!sourceList) continue;
    const old=[...sourceList.children].filter(e=>value(e,'BonusType')===type), want=chosenImp.has(typeOf(r.node));
    if (!want && !old.length || want && old.length && old.every(e=>value(e,'bBonusTrade')==='1')) continue;
    record('ImprovementInfo',typeOf(r.node)); const copy=r.node.cloneNode(true), list=direct(copy,'BonusTypeStructs');
    const existing=[...list.children].filter(e=>value(e,'BonusType')===type);
    if (!want) { for(const e of existing) { setValue(e,'bBonusTrade',0); if(!natural) { setValue(e,'iDiscoverRand',0); setValue(e,'bBonusMakesValid',0); } } }
    else if(existing.length) { for(const e of existing) setValue(e,'bBonusTrade',1); }
    else {
      let model=[...sourceList.children].find(e=>value(e,'BonusType')===typeOf(template.node));
      if(model) model=model.cloneNode(true);
      else { model=child(copy,'BonusTypeStruct'); model.append(child(copy,'BonusType',type),child(copy,'bBonusMakesValid',1),child(copy,'bBonusTrade',1),child(copy,'iDiscoverRand',0),child(copy,'YieldChanges')); }
      setValue(model,'BonusType',type);setValue(model,'bBonusTrade',1);list.append(model);
    }
    edit(r,copy);changeLog.push(`${labelFor(r.node)}: ${want?'connects':'no longer connects'} ${name}`);
  }
  for(const [id,tag,field,label] of [['resourceProducers','BuildingInfo','FreeBonus','produces'],['resourceBuildings','BuildingInfo','Bonus','requires'],['resourceUnits','UnitInfo','BonusType','requires']]) {
    const wanted=new Set(selected(id));
    for(const r of records(tag)) {
      const original=value(r.node,field), want=wanted.has(typeOf(r.node)); if(!want && original!==type) continue;
      record(tag,typeOf(r.node)); if(want && original && original!=='NONE' && original!==type) throw Error(`${labelFor(r.node)} already ${label} a different resource.`);
      const g=group(r.source), prior=g.edits.find(e=>e.original===r.node), copy=prior?.node || r.node.cloneNode(true);
      setValue(copy,field,want?type:'NONE');if(field==='FreeBonus')setValue(copy,'iNumFreeBonuses',want?integer('producerCount',1,100):0);
      if(!prior) edit(r,copy); changeLog.push(`${labelFor(r.node)}: ${want?label:'no longer '+label} ${name}`);
    }
  }
  const textPath=`Assets/XML/Text/CIV4GameText_Studio_${type}.xml`;
  if(R.files.has(textPath.toLowerCase())) {
    if(!ownText)throw Error('The generated localization file already exists.');
    const stored=R.files.get(textPath.toLowerCase()); const doc=await readXML(stored.file,stored.path);
    if(!doc || [...doc.doc.getElementsByTagName('TEXT')].some(t=>![textKey,textKey+'_PEDIA'].includes(value(t,'Tag'))))throw Error('The localization file contains other entries and cannot be replaced safely.');
  }
  const textDoc=xmlParse('<?xml version="1.0" encoding="UTF-8"?><Civ4GameText xmlns="http://www.firaxis.com"/>','new text');
  for(const [suffix,field] of [['','name'],['_PEDIA','pedia']]) { const entry=child(textDoc.documentElement,'TEXT');entry.append(child(entry,'Tag',textKey+suffix));for(const l of languages){const t=R.translations[l]?.[field]?.trim() || english[field];entry.append(child(entry,l,t));}textDoc.documentElement.append(entry); }
  extra.push({name:textPath,data:new XMLSerializer().serializeToString(textDoc)});
  const fallback=languages.filter(l=>l!=='English' && (!R.translations[l]?.name?.trim() || !R.translations[l]?.pedia?.trim()));if(fallback.length) notes.push(`English fallback used where missing: ${fallback.join(', ')}.`);
  notes.push('Start a new game. Natural placement depends on your map script; existing maps are not populated automatically.');
  notes.push('No DLL is rebuilt. New resources may affect padded symbol categories; test existing happiness, health, trade and other icons as well as the new symbol.');
  if(!natural) notes.push('Natural placement disabled. Producer buildings supply the configured FreeBonus; conversion inputs must be configured separately.');
  if(natural && !chosenImp.size) notes.push('No improvement connects this resource.');
  if(template.source.path.includes('/Modules/') || artTemplate.source.path.includes('/Modules/')) notes.push('Template is in a module: that module must be enabled for these definitions to load.');
  notes.push('Model, animation, terrain features, random placement weights and unexposed rules are inherited from the selected templates. Custom scripts and packed art are not resolved by this editor.');
  const files=[];
  for(const g of changes.values()) { if(g.edits.length || g.additions.length) files.push({name:g.source.path,data:patchDocument(g.source,g.edits,g.additions)}); }
  files.push(...extra);
  const manifest={format:'civ4-resource-patch',version:1,resource:type,name,action:editing?'edit':'create',template:typeOf(template.node),testOnly,notes,changes:changeLog,files:[]};
  const backups=[];
  for(const f of files) { const original=R.files.get(f.name.toLowerCase()); let old=null;if(original){const bytes=new Uint8Array(await original.file.arrayBuffer());old=await sha256(bytes);backups.push({name:'backup/'+original.path,data:bytes});}manifest.files.push({path:f.name,originalSHA256:old,newSHA256:await sha256(f.data)}); }
  const summary=[`${testOnly?'TEST ONLY — ':''}${editing?'Update':'Create'} ${name} (${type})`,`Template: ${labelFor(template.node)} · ${natural?'Natural':'Manufactured'}`,`Health ${value(n,'iHealth')} · happiness ${value(n,'iHappiness')}`,`Tile yields: ${['yieldFood','yieldProduction','yieldCommerce'].map(id=>$(id).value).join(' / ')} (food / production / commerce)`,`Reveal: ${$('revealTech').selectedOptions[0]?.text} · Trade: ${$('tradeTech').selectedOptions[0]?.text}`,`Map art: ${value(a,'NIF')}`,`\n${files.length} files in patch:\n${files.map(f=>f.name).join('\n')}`,`\nConnections:\n${changeLog.join('\n') || 'No direct producer or consumer changes.'}`,`\nNotes:\n${notes.join('\n')}`].join('\n');
  const instructions=`${summary}\n\nINSTALL\n1. Copy your mod to a test installation and start with the exact files you loaded into this editor.\n2. Compare manifest.json originalSHA256 values if the installation may have changed. Do not apply this patch over a newer draft.\n3. Copy the CONTENTS of patch/ into that test mod folder, merging Assets. Do not copy backup/ into Assets.\n4. Restart Civ IV, start a new game, and inspect the resource in Civilopedia and WorldBuilder. Check both font sizes, improvement connection, city trade, producers, consumers and unrelated symbols.\n5. For natural resources, test newly generated maps. For manufactured resources, build the selected producer.\n\nROLLBACK\nRestore original files from backup/ to the same relative paths. Delete files whose originalSHA256 in manifest.json is null.\n\nThis patch is based on the uploaded folder. It does not install itself, edit saved games, generate map models, or prove DLL/font index compatibility.\n`;
  return {summary,manifest,files,zipEntries:[...files.map(f=>({name:'patch/'+f.name,data:f.data})),...backups,{name:'manifest.json',data:JSON.stringify(manifest,null,2)},{name:'resource-draft.json',data:JSON.stringify(recipe(),null,2)},{name:'INSTALL.txt',data:instructions}]};
}
$('resourceMode').onclick=()=>{$('artWorkspace').hidden=true;$('resourceWorkspace').hidden=false;for(const id of ['buttonMode','fontMode'])$(id).setAttribute('aria-selected','false');$('resourceMode').setAttribute('aria-selected','true');};
$('modFolder').onchange=e=>loadMod([...e.target.files]);
$('resourceAction').onchange=$('resourceTemplate').onchange=populateResource;
$('resourceKind').onchange=kindChanged;
$('resourceArt').onchange=$('resourceSymbol').onchange=artChanged;
$('resourceIndex').oninput=()=>{$('slotVerified').checked=false;slotOccupancy();};
$('slotSize').onchange=slotRows;$('slotRow').onchange=slotGallery;
$('resourceName').oninput=()=>{if($('resourceAction').value==='create')$('resourceID').value='BONUS_'+$('resourceName').value.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toUpperCase().replace(/[^A-Z0-9]+/g,'_').replace(/^_+|_+$/g,'');R.translations.English ||= {};R.translations.English.name=$('resourceName').value;if(R.language==='English')$('translatedName').value=$('resourceName').value;};
$('translatedName').oninput=()=>{if(R.language==='English')$('resourceName').value=$('translatedName').value;};
$('textLanguage').onchange=()=>{saveLanguage();R.language=$('textLanguage').value;showLanguage();};
$('resourceFields').addEventListener('input',invalidateResource);$('resourceFields').addEventListener('change',invalidateResource);
$('resourceArtwork').onchange=async e=>{const file=e.target.files[0];R.artwork=null;invalidateResource();if(!file)return;try{if(!/\.(png|jpe?g)$/i.test(file.name)||file.size>50*1024*1024)throw Error('Choose a PNG/JPG up to 50 MB.');const im=await createImageBitmap(file,{imageOrientation:'from-image'});if(im.width*im.height>40000000){im.close();throw Error('Use artwork up to 40 megapixels.');}const scale=Math.min(1,2048/Math.max(im.width,im.height)),c=canvas(Math.max(1,Math.round(im.width*scale)),Math.max(1,Math.round(im.height*scale)));c.getContext('2d').drawImage(im,0,0,c.width,c.height);im.close();R.artwork=c;invalidateResource();put($('resourcePreview'),pixels(resourceImage(64,64)));$('resourceArtworkInfo').textContent=`${file.name} · 64×64 DXT3 button. Symbols use the same artwork fitted to their cells. Transparent PNG is best.`;}catch(e){sayResource(e.message,true);}};
$('reviewResource').onclick=async()=>{R.plan=null;$('downloadResource').disabled=true;$('reviewResource').disabled=true;$('modFolder').disabled=$('recipeFile').disabled=true;$('resourceFields').disabled=true;sayResource('Building and checking your patch…');try{R.plan=await prepareResource();$('resourceReview').textContent=R.plan.summary;$('resourceReview').hidden=false;$('downloadResource').disabled=false;sayResource('Patch checked. Review the file list and notes, then download. Original files are unchanged.');}catch(e){sayResource(e.message,true);}finally{$('reviewResource').disabled=false;$('resourceFields').disabled=false;$('modFolder').disabled=$('recipeFile').disabled=false;}};
$('downloadResource').onclick=()=>{if(!R.plan)return;download(`${R.plan.manifest.resource}${R.plan.manifest.testOnly?'-TEST-ONLY':''}-patch.zip`,C.zip(R.plan.zipEntries),'application/zip');R.dirty=false;sayResource('Patch downloaded with original-file backups, checksums, draft and install instructions. Test in a copy of your mod.');};
$('saveRecipe').onclick=()=>{download('civ4-resource-draft.json',JSON.stringify(recipe(),null,2),'application/json');R.dirty=false;sayResource('Draft saved. Reload this mod folder before opening it again. Artwork must be reselected.');};
$('recipeFile').onchange=async e=>{try{if(!records('BonusInfo').length)throw Error('Load the mod folder first.');const file=e.target.files[0];if(!file)return;if(file.size>1000000)throw Error('Draft exceeds 1 MB.');const d=JSON.parse(await file.text());if(d.format!=='civ4-resource-draft'||d.version!==1)throw Error('Not a supported resource draft.');$('resourceAction').value=d.fields.resourceAction;$('resourceTemplate').value=d.fields.resourceTemplate;populateResource();for(const [id,v] of Object.entries(d.fields)){const el=$(id);if(!el||!$('resourceFields').contains(el)||el.type==='file'||id==='slotVerified')continue;if(el.multiple)chooseMany(id,v);else if(el.type==='checkbox')el.checked=!!v;else el.value=v;}for(const cb of $('terrainOptions').querySelectorAll('input'))cb.checked=d.terrains.includes(cb.value);R.artwork=null;$('resourceArtwork').value='';$('resourcePreview').getContext('2d').clearRect(0,0,64,64);$('resourceArtworkInfo').textContent='Reselect artwork for this draft, or retain the template button.';R.translations=d.translations;R.slots=d.slots||{};R.language='English';$('textLanguage').value='English';$('slotVerified').checked=false;showLanguage();kindChanged();artChanged();slotRows();invalidateResource();sayResource('Draft loaded. Reselect artwork; slot verification must be repeated for the current mod files.');}catch(e){sayResource(e.message,true);}};
window.addEventListener('beforeunload',e=>{if(R.dirty){e.preventDefault();e.returnValue='';}});

for(const id of ['resourceImprovements','resourceProducers','resourceBuildings','resourceUnits']) $(id+'Search').oninput=()=>{const q=$(id+'Search').value.trim().toLowerCase();for(const o of $(id).options)o.hidden=!!q && !o.text.toLowerCase().includes(q);};
