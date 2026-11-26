#!/usr/bin/env python3
"""Check the names the DLL, the mod's Python and the mod's XML use against what the game loads.

usage: check_links.py <rise-of-mankind checkout> <XML dir>... [--base-python <dir>...]
  XML dirs: the folders the game falls back to after the mod's (Beyond the Sword's, then Civilization IV's).
  --base-python: the Python folders the mod's Python falls back to, in the same order.
Prints one section per check: what was checked, how many failed, and each failure with its file and line.
It reports; it does not judge. A " (1)" in a downloaded folder or file name is ignored.

What the game loads (as the DLL does it, with the exe's own modular loading off, ModularLoading = 0):
  - the mod's Assets/XML and Assets/res;
  - the modules of Assets/Modules that the MLF files load: an entry with <bLoad>1</bLoad> under the
    DefaultConfiguration, whose folder exists (names compared without case, as Windows does); an entry
    whose folder has its own MLF file is resolved through it; Assets/Unloaded Modules is never read;
  - a base game file only where the mod has no file at the same path (Beyond the Sword's before
    Civilization IV's).

Checks:
  modules     the MLF entries: loaded, switched off, and listed for folders that do not exist
  xml         files of the loaded mod XML that are not well-formed
  defines     literals passed to getDefineINT/FLOAT/STRING in the DLL and the Python, against <DefineName>
  types       literals passed to getInfoTypeForString, against <Type>, the strings of GlobalTypes.xml and
              the sound <ScriptID>s
  text        TXT_KEY_ literals in the DLL and the Python, against the <Tag> of the loaded text XML
  references  type names written in the loaded mod XML (prefix of a known family, e.g. TECH_, UNIT_),
              defined nowhere in what the game loads
  gc          Python calls gc.<name>(...) on CyGlobalContext that the DLL does not bind
  events      handlers registered for an event name the DLL never posts and no Python names elsewhere
  bindings    functions bound for Python under a name that differs from their C++ name
  py-landing  DLL calls into Python, both names known, landing in no Python function of the map
"""
import collections, csv, os, re, sys
import xml.etree.ElementTree as ET

args = sys.argv[1:]
base_py = args[args.index('--base-python') + 1:] if '--base-python' in args else []
args = args[:args.index('--base-python')] if '--base-python' in args else args
rom, base_xml = args[0], args[1:]
A = os.path.join(rom, 'Assets')
M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'map')
csv.field_size_limit(1 << 30)


def read(n): return list(csv.DictReader(open(os.path.join(M, n), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
def clean(p): return re.sub(r' \(\d+\)(?=\.[^.]+$|$|/)', '', p.replace('\\', '/')).lower()


def files(root, ext):
    for dp, _, fs in os.walk(root):
        for f in sorted(fs):
            if f.lower().endswith(ext): yield os.path.join(dp, f)


def section(title, checked, bad, note=''):
    print(f'\n## {title}\nchecked {checked}, failed {len(bad)}' + (f'\n{note}' if note else ''))
    for b in bad: print('  ' + '\t'.join(str(x) for x in b))


def line_of(t, pos): return t.count('\n', 0, pos) + 1


# --- modules -----------------------------------------------------------------------------------------
def ci(d, name):
    if not os.path.isdir(d): return None
    return next((os.path.join(d, x) for x in os.listdir(d) if x.lower() == name.lower()), None)


def mlf(d):
    p = ci(d, 'MLF_CIV4ModularLoadingControls.xml')
    if not p: return None
    t = open(p, encoding='latin-1').read()
    dc = re.search(r'<DefaultConfiguration>\s*(\S+?)\s*</DefaultConfiguration>', t)
    blocks = re.findall(r'<ConfigurationInfo>(.*?)</ConfigurationInfo>', t, re.S)
    use = [b for b in blocks if dc and re.search(r'<Type>\s*' + re.escape(dc.group(1)) + r'\s*</Type>', b)] or blocks[:1]
    return [(m[0].strip(), m[1] == '1') for b in use
            for m in re.findall(r'<Directory>([^<]*)</Directory>\s*<bLoad>\s*(\d)\s*</bLoad>', b)]


loaded, off, missing = [], [], []
def walk(d):
    for name, on in mlf(d) or ():
        sub = ci(d, name)
        if not sub: missing.append((os.path.relpath(os.path.join(d, name), rom), int(on))); continue
        if not on: off.append(os.path.relpath(sub, rom)); continue
        if mlf(sub) is not None: walk(sub)
        else: loaded.append(sub)
if mlf(os.path.join(A, 'Modules')) is not None: walk(os.path.join(A, 'Modules'))
mod_xml = [p for r in (os.path.join(A, 'XML'), os.path.join(A, 'res')) for p in files(r, '.xml')] + \
          [p for r in loaded for p in files(r, '.xml')]
allmods = list(files(os.path.join(A, 'Modules'), '.xml'))
section('modules: MLF entries', len(loaded) + len(off) + len(missing),
        [('listed, no folder', m, f'bLoad={o}') for m, o in missing] + [('bLoad=0', m, '') for m in off],
        f'loaded {len(loaded)} module folders ({len(mod_xml) - sum(1 for r in ("XML", "res") for _ in files(os.path.join(A, r), ".xml"))} '
        f'XML files of {len(allmods)} under Assets/Modules); the loaded folders:\n' +
        '\n'.join('  loaded\t' + os.path.relpath(l, rom) for l in loaded))

# --- what the loaded XML defines ---------------------------------------------------------------------
have = {clean(os.path.relpath(p, os.path.join(A, 'XML'))) for p in files(os.path.join(A, 'XML'), '.xml')}
base_files = []
for b in base_xml:   # Beyond the Sword's first: a file there hides Civilization IV's of the same path
    for p in files(b, '.xml'):
        k = clean(os.path.relpath(p, b))
        if k not in have: have.add(k); base_files.append(p)
defines, types, tags, broken = set(), set(), set(), []
texts = {}
for p in mod_xml + base_files:
    raw = open(p, 'rb').read()
    t = raw.decode('latin-1'); texts[p] = t
    if p in mod_xml:
        try: ET.fromstring(raw)
        except ET.ParseError as e: broken.append((os.path.relpath(p, rom), str(e)))
    defines |= set(re.findall(r'<DefineName>\s*([^<\s]+)\s*</DefineName>', t))
    types |= set(re.findall(r'<Type>\s*([^<\s]+)\s*</Type>', t))
    tags |= set(re.findall(r'<Tag>\s*([^<\s]+)\s*</Tag>', t))
    types |= set(re.findall(r'<ScriptID>\s*([^<\s]+)\s*</ScriptID>', t))   # sound scripts (AS2D_, AS3D_)
    if os.path.basename(p).lower() == 'globaltypes.xml':   # SetGlobalStringArray registers each string as a type
        types |= set(re.findall(r'>\s*([A-Z][A-Z0-9_]+)\s*<', t))
section('xml: loaded files of the mod that are not well-formed XML', len(mod_xml), broken,
        'A file the DLL never names is not loaded even when it lies in a loaded folder.')

# --- literals in the code ----------------------------------------------------------------------------
def strip_comments(t, kind):
    if kind == 'py': return re.sub(r'(?m)^[ \t]*#.*$', '', t)   # spaces and tabs only: \s would eat line breaks
    t = re.sub(r'/\*.*?\*/', lambda m: '\n' * m.group(0).count('\n'), t, flags=re.S)
    return re.sub(r'//[^\n]*', '', t)


code = [(p, 'dll') for p in files(os.path.join(A, 'CvGameCoreDLL'), ('.cpp', '.h', '.inl'))] + \
       [(p, 'py') for p in files(os.path.join(A, 'Python'), '.py')]
RX = {'defines': re.compile(r'getDefine(?:INT|FLOAT|STRING)\s*\(\s*"([A-Za-z0-9_]+)"'),
      'types': re.compile(r'getInfoTypeForString\s*\(\s*"([A-Za-z0-9_]+)"'),
      'text': re.compile(r'"(TXT_KEY_[A-Za-z0-9_]+)"')}
uses = collections.defaultdict(list)
src_text = {}
for p, kind in code:
    t = strip_comments(open(p, encoding='latin-1').read(), kind); src_text[p] = t
    for name, rx in RX.items():
        for m in rx.finditer(t):
            if m.group(1).endswith('_'): continue   # a prefix completed at run time ("TXT_KEY_BUILDING_" + name)
            uses[name].append((m.group(1), os.path.relpath(p, rom), line_of(t, m.start()), kind))
for name, known in (('defines', defines), ('types', types), ('text', tags)):
    u = uses[name]; bad = sorted(x for x in u if x[0] not in known)
    section(f'{name}: literals not defined in the loaded XML ({len({x[0] for x in u})} distinct names, '
            f'{len({x[0] for x in bad})} of them not defined)', len(u), bad)

# --- references between XML records ------------------------------------------------------------------
fam = collections.Counter(t.split('_')[0] for t in types if '_' in t)
families = {f for f, n in fam.items() if n >= 5 and f not in ('TXT', 'NONE')}
REF = re.compile(r'<(\w+)>\s*([A-Z][A-Z0-9]*_[A-Z0-9_]+)\s*</\1>')
SKIP_TAGS = {'Type', 'DefineName', 'Tag', 'DefineTextVal', 'ScriptID', 'Text'}   # definitions, and text
refs, bad = 0, []
for p in mod_xml:
    t = texts[p]
    for m in REF.finditer(t):
        tag, val = m.group(1), m.group(2)
        if tag in SKIP_TAGS or val.split('_')[0] not in families: continue
        refs += 1
        if val not in types: bad.append((val, tag, os.path.relpath(p, rom), line_of(t, m.start())))
section(f'references: type names in the loaded mod XML defined nowhere in what the game loads '
        f'({len({b[0] for b in bad})} distinct names)', refs, sorted(bad, key=lambda b: (b[2], b[3])),
        f'families checked: {len(families)} prefixes with at least 5 defined types')

# --- Python calls on gc --------------------------------------------------------------------------------
bound = collections.defaultdict(set)
for r in read('python_defs.tsv'): bound[r['cpp_scope']].add(r['python_name'])
GC = re.compile(r'\bgc\.([A-Za-z_]\w*)\s*\(')
seen, bad = 0, []
for p, kind in code:
    if kind != 'py': continue
    t = src_text[p]
    if not re.search(r'\bgc\s*=\s*CyGlobalContext\s*\(', t): continue
    for m in GC.finditer(t):
        seen += 1
        if m.group(1) not in bound['CyGlobalContext']: bad.append((m.group(1), os.path.relpath(p, rom), line_of(t, m.start())))
section(f'gc: Python calls gc.<name>() that the DLL does not bind for CyGlobalContext ({len(bound["CyGlobalContext"])} bound)',
        seen, sorted(bad))

# --- events -------------------------------------------------------------------------------------------
posted = {r['event'] for r in read('events.tsv')}
regs = read('py_event_registrations.tsv')
alltext = '\n'.join(src_text[p] for p, k in code if k == 'py') + '\n' + \
          '\n'.join(open(x, encoding='latin-1').read() for b in base_py for x in files(b, '.py'))
bad = []
for e in sorted({r['event'] for r in regs} - posted):
    if len(re.findall(r'["\']' + re.escape(e) + r'["\']', alltext)) <= sum(1 for r in regs if r['event'] == e and r['source'] != 'BUG config'):
        bad += [(e, r['source'], r['handler'], r['file'], r['line']) for r in regs if r['event'] == e]
section(f'events: handlers for an event name the DLL never posts and no Python names elsewhere ({len(posted)} posted)', len(regs), bad)

# --- binding names -------------------------------------------------------------------------------------
defs = read('python_defs.tsv')
bad = [(r['python_name'], r['cpp_scope'] + '::' + r['cpp_name'], r['file'], r['line']) for r in defs
       if r['python_name'].lower() != r['cpp_name'].lower()]
section('bindings: Python name differs from the C++ name it is bound to', len(defs), sorted(bad))

# --- DLL calls into Python landing nowhere -----------------------------------------------------------
c2p = read('cpp_to_py.tsv')
bad = [(r['module'], r['python_function'], r['file'], r['line']) for r in c2p
       if r['module'] != '?' and r['python_function'] != '?' and not r['python_file']]
section('py-landing: DLL calls into Python, both names known, landing in no Python function of the map', len(c2p), bad)
print(f'\n(loaded XML read: {len(mod_xml)} of the mod, {len(base_files)} of the base games; '
      f'defines {len(defines)}, types {len(types)}, text keys {len(tags)})')
