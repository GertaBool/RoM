#!/usr/bin/env python3
"""Read-only, whole-tree structural inventory; does not execute game code."""
import collections, csv, hashlib, io, json, re, subprocess, tokenize
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path('/workspace/rise-of-mankind')
OUT = Path(__file__).resolve().parent
SHA = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
paths = subprocess.check_output(['git','ls-files','-z'], cwd=ROOT).decode().split('\0')
paths = [p for p in paths if p]
extensions = collections.Counter(Path(p).suffix.lower() for p in paths)
files, symbols, xml_refs, callbacks = [], collections.defaultdict(list), [], []

def local(tag):
    return tag.split('}')[-1]

def subsystem(p):
    if p.startswith('Assets/Unloaded Modules/'): return 'Disabled module candidates'
    if p.startswith('Assets/Modules/'): return 'Modular rule/asset definitions'
    if p.startswith('Assets/CvGameCoreDLL/'): return 'Native engine and AI'
    if p.startswith('Assets/XML/'): return 'Base rules, text and assets'
    if p.startswith('Assets/Config/'): return 'BUG plugin configuration'
    if p.startswith('Assets/Python/'): return 'Python/' + (p.split('/')[2] if len(p.split('/')) > 3 else 'root')
    if p.startswith('PrivateMaps/'): return 'Map generation and scenarios'
    if p.startswith('Tools/'): return 'Host tools and regressions'
    return 'Other'

for p in paths:
    suffix = Path(p).suffix.lower()
    if suffix not in {'.py','.xml','.cpp','.cc','.h','.inl','.c','.hpp'}: continue
    data = (ROOT/p).read_bytes()
    s = data.decode('utf-8-sig', errors='replace')
    row = dict(path=p, kind=suffix[1:], subsystem=subsystem(p), bytes=len(data),
               lines=len(data.splitlines()), sha256=hashlib.sha256(data).hexdigest())
    if suffix == '.py':
        try:
            enc,_ = tokenize.detect_encoding(io.BytesIO(data).readline)
            s = data.decode(enc)
            row['encoding'] = enc
        except (SyntaxError,UnicodeDecodeError):
            s = data.decode('cp1252',errors='replace')
            row['encoding'] = 'cp1252 fallback'
        row['imports'] = sorted(set(re.findall(r'^\s*(?:from|import)\s+([\w.]+)', s, re.M)))
        row['classes'] = [{'name':m.group(1),'line':s[:m.start()].count('\n')+1} for m in re.finditer(r'^\s*class\s+(\w+)',s,re.M)]
        row['functions'] = [{'name':m.group(1),'line':s[:m.start()].count('\n')+1} for m in re.finditer(r'^\s*def\s+(\w+)\s*\(',s,re.M)]
        row['events_registered'] = re.findall(r'addEventHandler\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*([^\n)]+)',s)
        row['xml_type_literals'] = sorted(set(re.findall(r'getInfoTypeForString\s*\(\s*[\'"]([^\'"]+)[\'"]',s)))
        row['engine_import'] = 'CvPythonExtensions' in row['imports']
        row['rng_calls'] = len(re.findall(r'getSorenRandNum|getMapRandNum|\brandom\.',s))
    elif suffix == '.xml':
        try:
            root = ET.fromstring(data)
            row['parse'] = 'ok'
            row['root'] = local(root.tag)
            counts = collections.Counter(local(e.tag) for e in root.iter())
            row['elements'] = sum(counts.values())
            row['top_tags'] = counts.most_common(8)
            row['types'] = []
            row['callback_bindings'] = []
            for e in root.iter():
                tag, value = local(e.tag), (e.text or '').strip()
                if tag in {'Type','DefineName','Tag'} and value:
                    symbols[value].append({'path':p,'tag':tag})
                    row['types'].append(value)
                elif value and not len(e) and re.fullmatch(r'[A-Z][A-Z0-9_]+',value):
                    xml_refs.append({'path':p,'tag':tag,'symbol':value})
                if tag.startswith('Python') and value:
                    item = {'path':p,'tag':tag,'function':value}
                    row['callback_bindings'].append(item)
                    callbacks.append(item)
                if e.attrib.get('module'):
                    row.setdefault('module_bindings',[]).append(dict(element_tag=tag,attributes=dict(e.attrib)))
        except ET.ParseError as exc:
            row['parse'] = str(exc)
    else:
        row['includes'] = sorted(set(re.findall(r'^\s*#include\s+["<]([^">]+)',s,re.M)))
        row['methods'] = [{'name':m.group(1),'line':s[:m.start()].count('\n')+1} for m in re.finditer(r'^\w[^;\n]*?\b(\w+::\w+)\s*\([^;\n]*\)\s*(?:const\s*)?\n?\s*\{',s,re.M)]
    files.append(row)

module_paths = collections.defaultdict(list)
for f in files:
    if f['kind']=='py': module_paths[Path(f['path']).stem].append(f['path'])
edges = []
for f in files:
    for imp in f.get('imports',[]):
        for target in module_paths.get(imp.split('.')[0],[]):
            edges.append({'from':f['path'],'to':target,'kind':'lexical Python import'})
    for sym in f.get('xml_type_literals',[]):
        for target in symbols.get(sym,[]):
            edges.append({'from':f['path'],'to':target['path'],'kind':'XML Type lookup','symbol':sym})
function_index = collections.defaultdict(list)
for f in files:
    for func in f.get('functions',[]):
        function_index[func['name']].append({'path':f['path'],'line':func['line']})
for c in callbacks: c['candidates'] = function_index.get(c['function'],[])

summary = dict(commit=SHA,tracked_files=len(paths),extensions=dict(extensions),
               source_files=len(files),counts=dict(collections.Counter(f['kind'] for f in files)),
               lines=dict(collections.Counter({k:sum(f['lines'] for f in files if f['kind']==k) for k in sorted(set(f['kind'] for f in files))})),
               xml_errors=[{'path':f['path'],'error':f['parse']} for f in files if f['kind']=='xml' and f['parse']!='ok'],
               xml_callback_count=len(callbacks),xml_callbacks_without_local_definition=[c for c in callbacks if not c['candidates']],
               engine_importing_python=sum(bool(f.get('engine_import')) for f in files),
               note='Whole-tree lexical/structural inventory. Not a complete call graph, engine loader, schema validator, or behavioral proof. Imports, callbacks and definitions may be inactive, inherited from BTS, dynamic, or ambiguous.')
(OUT/'inventory.json').write_text(json.dumps(dict(summary=summary,files=files,edges=edges,xml_callbacks=callbacks),indent=2))
(OUT/'summary.json').write_text(json.dumps(summary,indent=2))
with (OUT/'file-inventory.csv').open('w') as out:
    w=csv.writer(out); w.writerow(['path','kind','subsystem','lines','bytes','sha256'])
    w.writerows([f[k] for k in ['path','kind','subsystem','lines','bytes','sha256']] for f in files)
(OUT/'xml-symbols.json').write_text(json.dumps(dict(definitions=symbols,references=xml_refs),indent=2))
print(json.dumps(summary,indent=2))
