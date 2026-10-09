import collections, html, json, subprocess
from pathlib import Path
from urllib.parse import quote
OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'inventory.json').read_text())
sha=data['summary']['commit']
base='https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/'+sha+'/'
by_name=collections.defaultdict(list)
for f in data['files']:by_name[Path(f['path']).name].append(f['path'])
for f in data['files']:
    for name in f.get('includes',[]):
        for p in by_name.get(name,[]):
            data['edges'].append({'from':f['path'],'to':p,'kind':'native include'})
    for b in f.get('module_bindings',[]):
        for p in by_name.get(b['attributes']['module']+'.py',[]):
            data['edges'].append({'from':f['path'],'to':p,'kind':'BUG XML module binding'})
for cb in data['xml_callbacks']:
    for target in cb['candidates']:
        data['edges'].append({'from':cb['path'],'to':target['path'],'kind':'XML callback candidate','symbol':cb['function']})
data['audit']=json.loads((OUT/'audit-findings.json').read_text())
(OUT/'dependency-edges.json').write_text(json.dumps(data['edges'],indent=2))

# Each Python/XML/native file gets an index entry, with full details in JSON/HTML.
lines=['# Complete tracked source inventory','',f'Revision `{sha}`. Every tracked Python, XML, C/C++ source/header and inline file is listed. Counts include disabled modules, support code and backup files; presence is not activation. Function/import matching is lexical; XML is parsed structurally.','', '| File | Kind | Lines | Structural summary |','|---|---|---:|---|']
for f in data['files']:
    if f['kind']=='py':desc=f"{len(f['functions'])} functions/methods; {len(f['classes'])} classes; {len(f['imports'])} import names; {len(f['events_registered'])} event registrations"
    elif f['kind']=='xml':desc=f"{f.get('root','documentation fragment')}; {len(f.get('types',[]))} declarations; {len(f.get('callback_bindings',[]))} Python bindings; {f['parse']}"
    else:desc=f"{len(f.get('includes',[]))} includes; {len(f.get('methods',[]))} recognized qualified methods"
    lines.append(f"| [{f['path']}]({base+quote(f['path'])}) | {f['kind']} | {f['lines']:,} | {desc} |")
(OUT/'FILE_CATALOG.md').write_text('\n'.join(lines)+'\n')

subprocess.run(['dot','-Tsvg',str(OUT/'architecture.dot'),'-o',str(OUT/'architecture.svg')],check=True)
svg=(OUT/'architecture.svg').read_text();svg=svg[svg.index('<svg'):]
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Rise of Mankind source explorer</title>
<style>body{font:16px/1.5 system-ui,sans-serif;margin:0;background:#f8fafc;color:#152238}main{max-width:1500px;margin:auto;padding:28px}h1{margin-bottom:4px}p{max-width:1050px}a{color:#1456a0}input,select,button{font:inherit;padding:9px;border:1px solid #94a3b8;border-radius:5px;background:white}input{width:min(620px,80%)}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:8px;border-bottom:1px solid #cbd5e1;text-align:left;vertical-align:top}th{background:#e2e8f0}tr:hover{background:#eef2ff}button{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#e2e8f0;padding:16px}.diagram{overflow:auto;background:white;border:1px solid #cbd5e1;border-radius:8px}.diagram svg{width:100%;height:auto;min-width:950px}.grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(300px,.8fr);gap:20px}.detail{position:sticky;top:8px;max-height:85vh;overflow:auto}summary{cursor:pointer;font-weight:600}.chip{display:inline-block;padding:5px 10px;margin:4px;background:#dbeafe;border-radius:5px}code{background:#e2e8f0;padding:2px 4px}small{color:#475569}@media(max-width:850px){.grid{display:block}.detail{position:static;max-height:none}}</style>
<main><h1>Rise of Mankind — source explorer</h1><p>Revision <code>1ab4f99</code>. Search all 252 Python and 956 XML files, plus native source. Select a file to inspect definitions, imports, XML declarations and candidate relationships. Links open the fixed GitLab revision.</p>
<p><span class="chip">12 / 14 regression programs passed</span><span class="chip">950 XML documents parsed + 6 documentation fragments</span><span class="chip">252 Python files structurally parsed</span></p>
<p>This is a structural index with a focused behavioral review. It is not a complete call graph or a claim that every file was behaviorally executed. Dynamic BUG exports and module activation matter; candidate edges alone do not establish runtime behavior. See <a href="REVIEW.md">the review</a>, <a href="GAMEFLOW_MODEL.md">simulator model</a>, and <a href="regression.log">baseline output</a>.</p>
<details open><summary>Architecture and feedback paths</summary><p><a href="architecture.svg" target="_blank" rel="noopener">Open the full-size vector diagram</a></p><div class="diagram">__SVG__</div></details>
<h2>Explore files</h2><p><input id="query" aria-label="Search source" placeholder="Search a file, function, event, XML Type, or import…"> <select id="kind" aria-label="File type"><option value="">All types</option><option>py</option><option>xml</option><option>cpp</option><option>h</option><option>cc</option><option>c</option><option>inl</option></select> <select id="subsystem" aria-label="Subsystem"><option value="">All subsystems</option></select></p><p id="count" aria-live="polite"></p>
<div class="grid"><div><table><thead><tr><th>File</th><th>Kind</th><th>Lines</th></tr></thead><tbody id="rows"></tbody></table><button id="more">Show 100 more</button></div><aside class="detail"><h2 id="selected">Choose a file</h2><div id="details"></div></aside></div></main>
<script>const data=__DATA__; const base=__BASE__; const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const el=id=>document.getElementById(id);let limit=100;const searchable=data.files.map(f=>JSON.stringify(f).toLowerCase());
for(const s of [...new Set(data.files.map(f=>f.subsystem))].sort()){let o=document.createElement('option');o.value=s;o.textContent=s;el('subsystem').append(o)}
function link(path){return base+path.split('/').map(encodeURIComponent).join('/')}
function select(path){let f=data.files.find(f=>f.path===path);el('selected').textContent=f.path;let edges=data.edges.filter(e=>e.from===path||e.to===path);el('details').innerHTML='<p><a target="_blank" rel="noopener" href="'+link(path)+'">Open source on GitLab</a></p><p>'+esc(f.subsystem)+' · '+f.lines.toLocaleString()+' lines</p><h3>Candidate connections ('+edges.length+')</h3>';
let list=document.createElement('div');for(let e of edges.slice(0,180)){let p=document.createElement('p');let other=e.from===path?e.to:e.from;let b=document.createElement('button');b.textContent=other;b.onclick=()=>select(other);p.append((e.from===path?'→ ':'← ')+e.kind+' '+(e.symbol||'')+' ');p.append(b);list.append(p)}if(edges.length>180){let p=document.createElement('p');p.textContent='First 180 connections shown. Full data: dependency-edges.json.';list.append(p)}el('details').append(list);let pre=document.createElement('pre');pre.textContent=JSON.stringify(f,null,2);el('details').append(pre)}
function render(){let q=el('query').value.toLowerCase(),k=el('kind').value,s=el('subsystem').value;let rows=data.files.filter((f,i)=>(!q||searchable[i].includes(q))&&(!k||f.kind===k)&&(!s||f.subsystem===s));el('count').textContent=rows.length+' matching files; showing '+Math.min(limit,rows.length);el('rows').replaceChildren();for(let f of rows.slice(0,limit)){let tr=document.createElement('tr'),td=document.createElement('td'),b=document.createElement('button');b.textContent=f.path;b.onclick=()=>select(f.path);td.append(b);tr.append(td);for(let v of [f.kind,f.lines.toLocaleString()]){let c=document.createElement('td');c.textContent=v;tr.append(c)}el('rows').append(tr)}el('more').hidden=rows.length<=limit}
for(let id of ['query','kind','subsystem'])el(id).addEventListener('input',()=>{limit=100;render()});el('more').onclick=()=>{limit+=100;render()};render();</script></html>'''
page=page.replace('__SVG__',svg).replace('__DATA__',json.dumps(data).replace('<','\\u003c')).replace('__BASE__',json.dumps(base))
(OUT/'explorer.html').write_text(page)
print('Wrote explorer.html, FILE_CATALOG.md, architecture.svg and dependency-edges.json')
