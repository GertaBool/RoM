#!/usr/bin/env python3
"""Read every RoM XML file against its own XDR schema and write typed records.

Each XML file names its schema in its root (xmlns="x-schema:NAME.xml"). The schema
declares every element: content (textOnly/eltOnly), dt:type (int, boolean, float, or
string when absent) and, for containers, the child elements with min/maxOccurs. Every
record (an element whose schema has a Type, DefineName or Tag child) is written with
every field its schema declares: present values typed, absent ones as null. Fields that
may repeat (maxOccurs="*") are lists.

Load set and order follow the DLL (CvXMLLoadUtilitySetMod): Assets/XML first, then the
module directories under Assets/Modules that their MLF_CIV4ModularLoadingControls.xml
files load, in MLF order; Assets/Unloaded Modules is never read. A module record whose
Type already exists is merged as copyNonDefaults does: its non-default values replace
the old ones; lists are merged by their first value, the module's entry winning.

usage: xmlread.py <Assets dir> <out dir>
writes <out>/records.json (per record type: resolved records) and <out>/files.json
(every file: schema, record type, record count, loaded, load position)."""
import json, os, sys
import xml.etree.ElementTree as ET

A, OUT = sys.argv[1], sys.argv[2]
KEYS = ('Type', 'DefineName', 'Tag')
XDR = '{urn:schemas-microsoft-com:xml-data}'
DT = '{urn:schemas-microsoft-com:datatypes}type'


def local(tag):
    return tag.split('}', 1)[-1]


# ---------- schemas ----------
_schemas = {}
_by_name = {}
for p, _, fs in os.walk(A):
    for f in fs:
        if f.lower().endswith('.xml') and 'schema' in f.lower():
            _by_name.setdefault(f.lower(), os.path.join(p, f))


def schema(path):
    if path in _schemas:
        return _schemas[path]
    types = {}
    for e in ET.parse(path).getroot():
        if local(e.tag) != 'ElementType':
            continue
        kids = [(c.get('type'), c.get('minOccurs', '1'), c.get('maxOccurs', '1'))
                for c in e if local(c.tag) == 'element']
        types[e.get('name')] = {'content': e.get('content', 'mixed'), 'dt': e.get(DT, 'string'), 'children': kids}
    _schemas[path] = types
    return types


def schema_for(xml_path, root):
    ns = root.tag[1:].split('}', 1)[0] if root.tag.startswith('{') else ''
    if not ns.startswith('x-schema:'):
        return None
    name = ns[len('x-schema:'):]
    here = os.path.join(os.path.dirname(xml_path), name)
    return here if os.path.exists(here) else _by_name.get(name.lower())


# ---------- values ----------
def typed(text, dt):
    t = (text or '').strip()
    if dt == 'int':
        try:
            return int(t)
        except ValueError:
            return int(float(t)) if t else 0
    if dt == 'boolean':
        return t in ('1', 'true', 'True')
    if dt == 'float':
        return float(t) if t else 0.0
    return t


def value(e, types):
    """Typed value of element e: scalar, dict of children, or list."""
    st = types.get(local(e.tag))
    if st is None or st['content'] == 'textOnly' or not list(e):
        return typed(e.text, st['dt'] if st else 'string')
    rep = {c for c, _, mx in st['children'] if mx == '*'}
    kids = [k for k in e if isinstance(k.tag, str)]
    names = [local(k.tag) for k in kids]
    # a pure list container (all children the same repeated element) -> list
    if kids and len(set(names)) == 1 and (names[0] in rep or len(names) > 1):
        return [value(k, types) for k in kids]
    out = {}
    for k in kids:
        n = local(k.tag)
        v = value(k, types)
        if n in rep:
            out.setdefault(n, []).append(v)
        else:
            out[n] = v
    return out


def record(e, types):
    st = types.get(local(e.tag), {'children': []})
    out = {}
    for c, _, mx in st['children']:
        out[c] = [] if mx == '*' else None
    v = value(e, types)
    if isinstance(v, dict):
        out.update(v)
    return out


# ---------- load set and order (MLF) ----------
def mlf_order():
    """Module directories (relative to Assets/Modules) in load order, as the DLL builds them."""
    order = []

    def walk(rel):
        base = os.path.join(A, 'Modules', rel)
        mlf = os.path.join(base, 'MLF_CIV4ModularLoadingControls.xml')
        if not os.path.exists(mlf):
            order.append(rel)           # a leaf module: everything below it loads
            return
        root = ET.parse(mlf).getroot()
        for m in root.iter():
            if local(m.tag) != 'Module':
                continue
            d = {local(k.tag): (k.text or '').strip() for k in m}
            if d.get('Directory') and d.get('bLoad', '1') == '1':
                walk(os.path.join(rel, d['Directory']) if rel else d['Directory'])
    walk('')
    return order


def module_of(rel_path, order):
    parts = rel_path.replace('\\', '/').split('/')
    if parts[0] != 'Modules':
        return (0, '') if parts[0] != 'Unloaded Modules' else None
    sub = '/'.join(parts[1:-1]).lower()        # Windows paths: case-insensitive
    best = None
    for i, m in enumerate(order):
        mm = m.replace(os.sep, '/').lower()
        if sub == mm or sub.startswith(mm + '/') or mm == '':
            if best is None or len(mm) > len(best[1]):
                best = (i + 1, mm)
    return best


ORDER = mlf_order()
files, raw = {}, []
for p, _, fs in sorted(os.walk(A)):
    for f in sorted(fs):
        if not f.lower().endswith('.xml') or 'schema' in f.lower():
            continue
        path = os.path.join(p, f)
        rel = os.path.relpath(path, A).replace(os.sep, '/')
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as err:
            files[rel] = {'error': str(err)}
            continue
        sp = schema_for(path, root)
        pos = module_of(rel, ORDER)
        info = {'schema': os.path.relpath(sp, A).replace(os.sep, '/') if sp else None,
                'loaded': pos is not None, 'load_position': pos[0] if pos else None, 'records': 0, 'record_type': None}
        files[rel] = info
        if sp is None:
            continue
        types = schema(sp)
        for e in root.iter():
            st = types.get(local(e.tag))
            if not st or not any(c in KEYS for c, _, _ in st['children']):
                continue
            rec = record(e, types)
            key = next((rec.get(k) for k in KEYS if rec.get(k)), None)
            if not key:
                continue
            info['records'] += 1
            info['record_type'] = local(e.tag)
            if pos is not None:
                raw.append((pos[0], rel, local(e.tag), key, rec))


# ---------- resolve (copyNonDefaults) ----------
def nondefault(v):
    return v not in (None, '', 0, 0.0, False, [], {}, 'NONE')


def merge(old, new):
    out = dict(old)
    for k, v in new.items():
        if isinstance(v, list) and isinstance(old.get(k), list) and v:
            keyed = {}
            for item in old[k] + v:
                ik = json.dumps(item[next(iter(item))] if isinstance(item, dict) and item else item, sort_keys=True)
                keyed[ik] = item
            out[k] = list(keyed.values())
        elif nondefault(v):
            out[k] = v
    return out


records = {}
for pos, rel, rtype, key, rec in sorted(raw, key=lambda r: r[0]):
    table = records.setdefault(rtype, {})
    if key in table:
        table[key] = merge(table[key], rec)
        table[key]['_sources'] = table[key].get('_sources', []) + [rel]
    else:
        rec['_sources'] = [rel]
        table[key] = rec

os.makedirs(OUT, exist_ok=True)
json.dump(records, open(os.path.join(OUT, 'records.json'), 'w'), indent=1, sort_keys=True)
json.dump({'module_order': ORDER, 'files': files}, open(os.path.join(OUT, 'files.json'), 'w'), indent=1, sort_keys=True)
n = sum(len(t) for t in records.values())
print('files %d, with schema %d, loaded %d; record types %d, records %d' % (
    len(files), sum(1 for v in files.values() if v.get('schema')), sum(1 for v in files.values() if v.get('loaded')),
    len(records), n))
