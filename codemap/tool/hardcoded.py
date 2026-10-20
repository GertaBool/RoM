#!/usr/bin/env python3
"""Hard-coded entries of the key functions, each with what outside the function depends on it.

usage: hardcoded.py <codemap dir> <rise-of-mankind checkout> <original BTS SDK CvGameCoreDLL dir>
                    <XML dir> [<XML dir> ...] [--functions id,id,...]
  XML dirs: where the game looks for xml\\..., after the mod's own Assets/XML, in order: Beyond the
  Sword's, then Civilization IV's. A " (1)" in a folder name (a download artefact) is ignored.
  --functions: the functions to read (default: the twelve of `query.py rank 12`).
Writes <codemap dir>/map/hardcoded.tsv and <codemap dir>/hardcoded.md.

The entries are read from each function's own lines in the source (comments left out), and each is
checked against what holds the other end:
  export       an exported function: the exe calls it by its decorated name; is it in the original SDK
  exe call     a call into the exe's interfaces (gDLL->...): is the method in the original SDK's interfaces
  enum values  an enum the function uses: are the original SDK's values unchanged (the exe was compiled
               with the original CvEnums.h, which the SDK shares with it)
  enum switch  a switch over an enum: the values it has no case for
  xml file     a file loaded by name and path: which folder has it, does the path match its elements,
               how many records, how many module files add to it
  xml order    a loaded file whose records mirror an enum: is the order the same
  define       a global define read by name: in which loaded defines file, and its value
  bug option   a BUG option read by name: in the BUG configuration, and its fallback define
  text key     a TXT_KEY string: in which text folder
  sound        an AS2D_/AS3D_ sound: in which audio script file
  python call  a call into a Python function by name: the Python function it lands in
  event        an event posted to Python: the handlers registered for it
  random       a synchronised random number: its order of calls is part of network sync and of replays
  number       a numeric literal other than 0 and 1
  log format   a format string written to a log: the tools of this repository that read that text
  log call     a call writing this project's war log: the tools that read the war log
  state        a member variable set directly: the other functions that set it
  release      rule tables freed by name (deleteInfoArray): each against the tables the XML loaders fill
  return value a bool result: the functions that call it
  original     how many of the function's lines are as in the original SDK's function
  fork change  lines changed in the mod's repository after the file was added, by commit
"""
import collections, csv, os, re, subprocess, sys

KINDS = ['export', 'original', 'fork change', 'exe call', 'python call', 'event', 'xml file', 'xml order',
         'define', 'bug option', 'text key', 'sound', 'enum values', 'enum switch', 'random', 'number',
         'log format', 'log call', 'state', 'release', 'return value']
KEYWORDS = {'if', 'for', 'while', 'switch', 'return', 'sizeof', 'case', 'catch', 'defined'}


def read(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        return list(csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE))


def clean(text):
    """Comments blanked (newlines kept, so offsets keep their lines); string and char literals kept."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if text.startswith('//', i):
            j = text.find('\n', i); j = n if j < 0 else j
            out.append(' ' * (j - i)); i = j
        elif text.startswith('/*', i):
            j = text.find('*/', i + 2); j = n if j < 0 else j + 2
            out.append(re.sub(r'[^\n]', ' ', text[i:j])); i = j
        elif c in '"\'':
            j = i + 1
            while j < n and text[j] != c and text[j] != '\n': j += 2 if text[j] == '\\' else 1
            out.append(text[i:j + 1]); i = j + 1
        else:
            out.append(c); i += 1
    return ''.join(out)


STR = re.compile(r'L?"((?:[^"\\\n]|\\.)*)"')


def blank_strings(t):
    return STR.sub(lambda m: '"' + ' ' * (len(m.group(0)) - 2) + '"', t)


def match_close(t, i, o='(', c=')'):
    """Index of the bracket closing the one at t[i] (strings already blanked)."""
    d = 0
    for j in range(i, len(t)):
        if t[j] == o: d += 1
        elif t[j] == c:
            d -= 1
            if d == 0: return j
    return len(t) - 1


def split_args(s):
    out, d, cur = [], 0, ''
    for ch in s:
        if ch in '([{<' and ch != '<': d += 1
        if ch in ')]}': d -= 1
        if ch == ',' and d == 0: out.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    return out


def enums(paths):
    """{enum: {constant: value}} and whether each enum is DllExport, from the headers."""
    vals, exported = {}, set()
    for p in paths:
        t = blank_strings(clean(open(p, encoding='latin-1').read()))
        for m in re.finditer(r'\benum\s+(DllExport\s+)?(\w+)\s*\{', t):
            body = t[m.end():match_close(t, m.end() - 1, '{', '}')]
            body = '\n'.join(l for l in body.split('\n') if not l.strip().startswith('#'))
            v, cur = -1, {}
            for e in [x.strip() for x in body.split(',') if x.strip()]:
                k, _, ex = e.partition('=')
                k, ex = k.strip(), ex.strip()
                if not re.match(r'^\w+$', k): continue
                if ex:
                    try: v = int(ex.strip('()'), 0)
                    except ValueError: v = cur.get(ex.strip('()'), v + 1)
                else: v += 1
                cur[k] = v
            vals[m.group(2)] = cur
            if m.group(1): exported.add(m.group(2))
    return vals, exported


def norm(rel):
    return '/'.join(x.replace(' (1)', '') for x in rel.replace('\\', '/').split('/')).lower()


class Files:
    """The game's file lookup: the mod's folder first, then each further folder."""
    def __init__(self, roots):
        self.roots, self.index = roots, []
        for label, root in roots:
            idx = {}
            for dp, dn, fn in os.walk(root):
                dn.sort()
                for f in sorted(fn):
                    p = os.path.join(dp, f)
                    idx.setdefault(norm(os.path.relpath(p, root)), p)
            self.index.append((label, idx))

    def find(self, rel):
        for label, idx in self.index:
            if norm(rel) in idx: return label, idx[norm(rel)]
        return None, None

    def every(self, pattern):
        """(label, path) of every file whose normalised relative path matches the regex, in all folders."""
        rx = re.compile(pattern)
        return [(label, p) for label, idx in self.index for r, p in sorted(idx.items()) if rx.search(r)]


def blame(src, path, a, b):
    """{commit: (date, subject, [lines])} for lines a..b of path changed after the file was added."""
    added = subprocess.run(['git', '-C', src, 'log', '--diff-filter=A', '--format=%H', '--', path],
                           capture_output=True, text=True).stdout.split()
    if not added: return {}
    base = added[-1]
    out = subprocess.run(['git', '-C', src, 'blame', '--porcelain', '-L', f'{a},{b}', '--', path],
                         capture_output=True, text=True).stdout.split('\n')
    meta, res, cur = {}, collections.OrderedDict(), None
    for ln in out:
        m = re.match(r'^([0-9a-f]{40}) \d+ (\d+)', ln)
        if m: cur = (m.group(1), int(m.group(2))); meta.setdefault(cur[0], {}); continue
        if cur and ln.startswith('summary '): meta[cur[0]]['s'] = ln[8:]
        if cur and ln.startswith('author-time '): meta[cur[0]]['t'] = int(ln[12:])
        if cur and ln.startswith('\t'):
            if cur[0] != base: res.setdefault(cur[0], []).append(cur[1])
    import datetime
    day = lambda x: datetime.datetime.fromtimestamp(x, datetime.timezone.utc).strftime('%Y-%m-%d')
    return {c: (day(meta[c].get('t', 0)), meta[c].get('s', ''), ls)
            for c, ls in res.items()}


def ranges(ls):
    out, start, prev = [], None, None
    for x in sorted(ls):
        if start is None: start = prev = x
        elif x == prev + 1: prev = x
        else: out.append((start, prev)); start = prev = x
    if start is not None: out.append((start, prev))
    return ', '.join(f'{a}' if a == b else f'{a}-{b}' for a, b in out)


def original_body(sdk, file, scope, name):
    p = os.path.join(sdk, file)
    if not os.path.exists(p): return None
    t = clean(open(p, encoding='latin-1').read())
    m = re.search(r'\b' + re.escape(scope) + r'::' + re.escape(name) + r'\s*\([^;{]*\)\s*(const\s*)?\{', t)
    if not m: return None
    return t[m.end() - 1:match_close(blank_strings(t), m.end() - 1, '{', '}') + 1]


def code_lines(t):
    return [re.sub(r'\s+', ' ', l).strip() for l in t.split('\n') if l.strip() and l.strip() not in '{}']


def repo_text(repo):
    """The text files of this repository that tools read logs with (code and its docs, not the map)."""
    out = []
    for dp, dn, fn in os.walk(repo):
        dn[:] = sorted(d for d in dn if d not in ('.git', 'codemap', 'references', 'node_modules', '__pycache__'))
        for f in sorted(fn):
            if f.endswith(('.py', '.sh', '.sql', '.R', '.jl')):
                p = os.path.join(dp, f)
                try: out.append((os.path.relpath(p, repo), open(p, encoding='utf-8', errors='replace').read()))
                except OSError: pass
    return out


def main():
    args = sys.argv[1:]
    fsel = None
    if '--functions' in args:
        k = args.index('--functions'); fsel = [int(x) for x in args[k + 1].split(',')]; del args[k:k + 2]
    cm, src, sdk, xmldirs = args[0], args[1], args[2], args[3:]
    M = os.path.join(cm, 'map')
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    sys.argv = [sys.argv[0]]
    import query
    F = query.F
    if fsel is None: fsel = [i for i, _, _ in query.rank(12)]
    dll = os.path.join(src, 'Assets', 'CvGameCoreDLL')
    calls = read(os.path.join(M, 'calls.tsv'))
    callees = collections.defaultdict(list); callers = collections.defaultdict(set)
    for c in calls:
        callees[int(c['caller'])].append((int(c['callee']), c['line'])); callers[int(c['callee'])].add(int(c['caller']))
    events = {int(r['function']): r['event'] for r in read(os.path.join(M, 'events.tsv'))}
    regs = collections.defaultdict(list)
    for r in read(os.path.join(M, 'py_event_registrations.tsv')): regs[r['event']].append(r)
    overrides = collections.defaultdict(set)
    for r in read(os.path.join(M, 'overrides.tsv')): overrides[int(r['method'])].add(int(r['overrides']))
    cpp2py = collections.defaultdict(list)
    for r in read(os.path.join(M, 'cpp_to_py.tsv')): cpp2py[int(r['caller'])].append(r)

    R, _ = enums(sorted(os.path.join(dll, f) for f in os.listdir(dll) if f.endswith('.h')))
    O, _ = enums(sorted(os.path.join(sdk, f) for f in os.listdir(sdk) if f.endswith('.h')))
    const = {k: e for e, vs in R.items() for k in vs}
    ifaces = set()
    for f in os.listdir(sdk):
        if re.match(r'CvDLL\w*IFaceBase\.h$', f) or f == 'CvDLLUtilityIFaceBase.h':
            it = blank_strings(clean(open(os.path.join(sdk, f), encoding='latin-1').read()))
            ifaces |= {m.group(1) for m in (re.search(r'\b(\w+)\s*\(', l) for l in it.split('\n')) if m}   # every declared method
    osdk_exports = collections.defaultdict(set)   # class -> exported method names in the original SDK
    for f in os.listdir(sdk):
        if f.endswith('.h'):
            t = clean(open(os.path.join(sdk, f), encoding='latin-1').read()); cls = None
            for ln in t.split('\n'):
                m = re.match(r'\s*(?:class|struct)\s+(?:DllExport\s+)?(\w+)\b[^;]*$', ln)
                if m: cls = m.group(1)
                m = re.search(r'\bDllExport\b[^;(]*?\b(\w+)\s*\(', ln)
                if m and cls: osdk_exports[cls].add(m.group(1))

    mod = os.path.join(src, 'Assets')
    xml = Files([('mod', os.path.join(mod, 'XML'))] + [(f'base {k + 1}', d) for k, d in enumerate(xmldirs)])
    modules = Files([('modules', os.path.join(mod, 'Modules'))])
    labels = {'mod': 'mod', 'base 1': 'Beyond the Sword', 'base 2': 'Civilization IV'}
    # global defines: the files the loader reads, each looked up mod first, and the module files
    loader = clean(open(os.path.join(dll, 'CvXMLLoadUtilitySet.cpp'), encoding='latin-1').read())
    defines = {}
    def_files = []
    for f in re.findall(r'ReadGlobalDefines\("([^"]+)"', loader):
        f = f.replace('\\\\', '/').replace('\\', '/')
        if f.lower().startswith('xml/'): lab, p = xml.find(f[4:])
        else:
            p = os.path.join(mod, *f.split('/')); lab = 'mod' if os.path.exists(p) else None
        if p and p not in def_files: def_files.append(p)
    for pat in re.findall(r'enumerateFiles\(\w+,\s*"modules\\\\\*(_\w+\.xml)"', loader):
        if 'Defines' in pat: def_files += [p for _, p in modules.every(re.escape(pat.lower()) + '$')]
    for p in def_files:
        t = open(p, encoding='latin-1').read()
        for m in re.finditer(r'<DefineName>\s*([^<\s]+)\s*</DefineName>\s*<(\w+)>([^<]*)<', t):
            old = defines.get(m.group(1))   # read in the loader's order: a later file sets it again
            defines[m.group(1)] = (m.group(3), (old[1] + ', then ' if old else '') + os.path.relpath(p, mod))
    texts = {}
    for lab, p in xml.every(r'^text/.*\.xml$') + modules.every(r'text.*\.xml$|\.xml$'):
        if lab == 'modules' and 'text' not in p.lower(): continue
        for m in re.finditer(r'<Tag>\s*([^<\s]+)\s*</Tag>', open(p, encoding='latin-1').read()):
            texts.setdefault(m.group(1), lab)
    sounds = {}
    for lab, p in xml.every(r'^audio/.*\.xml$'):
        for m in re.finditer(r'<ScriptID>\s*([^<\s]+)\s*</ScriptID>', open(p, encoding='latin-1').read()):
            sounds.setdefault(m.group(1), lab)
    bug = {}
    cfg = os.path.join(mod, 'Config')
    for dp, dn, fn in os.walk(cfg):
        for f in sorted(fn):
            if f.endswith('.xml'):
                t = open(os.path.join(dp, f), encoding='latin-1').read()
                for mm in re.finditer(r'<mod\s+id="(\w+)"(.*?)</mod>', t, re.S):
                    for o in re.findall(r'<(?:option|list|accel)\s+id="(\w+)"', mm.group(2)):
                        bug.setdefault(mm.group(1) + '__' + o, os.path.relpath(os.path.join(dp, f), mod))
    repo = os.path.dirname(os.path.abspath(cm))
    rtext = repo_text(repo)
    warlog_readers = sorted({p for p, t in rtext if 'WarLog.log' in t})

    rows = []
    def add(fid, kind, entry, line, depends, status, detail=''):
        rows.append((fid, kind, entry, line, depends, status, detail))

    for fid in fsel:
        r = F[fid]; path = os.path.join(dll, r['file'])
        lines = open(path, encoding='latin-1').read().split('\n')
        a, b = int(r['line']), int(r['end'])
        decl_start = a
        while decl_start > 1 and lines[decl_start - 2].strip() and not lines[decl_start - 2].strip().startswith(('}', '/', '*')):
            decl_start -= 1
        decl = ' '.join(lines[decl_start - 1:a - 1])
        raw = '\n'.join(lines[a - 1:b])
        t = clean(raw); tb = blank_strings(t)
        def lineof(off): return a + t.count('\n', 0, off)
        full = r['scope'] + '::' + r['name'] if r['scope'] else r['name']

        # export, original, fork changes
        if r['exported'] == '1':
            ok = r['name'] in osdk_exports.get(r['scope'], ())
            add(fid, 'export', r['key'], a, 'the game exe calls it by this decorated name',
                'in the original SDK' if ok else 'not in the original SDK', 'its name, arguments, class and calling convention fix the name')
        ob = original_body(sdk, r['file'], r['scope'], r['name'])
        mine = code_lines(blank_strings(t))
        if ob is None:
            add(fid, 'original', full, a, 'the original SDK', 'not in the original SDK')
        else:
            theirs = collections.Counter(code_lines(blank_strings(ob)))
            same = 0
            for l in mine:
                if theirs[l] > 0: theirs[l] -= 1; same += 1
            add(fid, 'original', full, a, 'the original SDK', 'in the original SDK',
                f'{same} of {len(mine)} code lines as in the original function')
        for c, (date, subj, ls) in sorted(blame(src, os.path.relpath(path, src), a, b).items(), key=lambda x: (x[1][0], x[0])):
            add(fid, 'fork change', c[:12], min(ls), 'the mod repository', 'changed after the file was added',
                f'{date} {subj} ({len(ls)} lines: {ranges(ls)})')

        # calls with their arguments
        for m in re.finditer(r'\b([A-Za-z_]\w*)\s*\(', tb):
            nm = m.group(1)
            if nm in KEYWORDS: continue
            close = match_close(tb, m.end() - 1)
            argtext = t[m.end():close]
            ln = lineof(m.start())
            before = tb[max(0, m.start() - 60):m.start()]
            if re.search(r'gDLL\s*->\s*(?:\w+\s*\(\s*\)\s*->\s*)?$', before) and not tb[close + 1:].lstrip().startswith('->'):
                ok = nm in ifaces
                add(fid, 'exe call', nm, ln, 'the game exe implements it',
                    'in the original SDK interfaces' if ok else 'not in the original SDK interfaces')
            if nm in ('LoadGlobalClassInfo', 'LoadGlobalClassInfoModular', 'LoadDiplomacyInfo'):
                ar = split_args(argtext)
                s = [STR.fullmatch(x) for x in ar[1:4]] if len(ar) >= 4 else []
                if len(s) == 3 and all(s):
                    root, folder, xp = (x.group(1) for x in s)
                    lab, p = xml.find(f'{folder}/{root}.xml')
                    mods = modules.every(r'_' + re.escape(root.lower()) + r'\.xml$')
                    if not p:
                        add(fid, 'xml file', f'{folder}/{root}.xml', ln, 'xml folders', 'missing',
                            f'{ar[0]}; may be in a packed .FPK file'); continue
                    x = open(p, encoding='latin-1').read()
                    xc = re.sub(r'<!--.*?-->', '', x, flags=re.S)
                    els = xp.split('/')
                    rootel = re.search(r'<([A-Za-z_][\w.-]*)[\s>]', re.sub(r'<\?.*?\?>', '', xc))
                    bad = [] if rootel and rootel.group(1) == els[0] else [f'root element is <{rootel.group(1) if rootel else "?"}>']
                    bad += [f'no <{e}>' for e in els[1:] if not re.search(r'<' + re.escape(e) + r'[\s>]', xc)]
                    recs = re.findall(r'<' + re.escape(els[-1]) + r'[\s>](.*?)</' + re.escape(els[-1]) + r'>', xc, re.S)
                    add(fid, 'xml file', f'{folder}/{root}.xml', ln, labels.get(lab, lab) + ' XML folder',
                        'path differs: ' + '; '.join(bad) if bad else 'ok',
                        f'{ar[0]}; path {xp}; {len(recs)} records' + (f'; {len(mods)} module files add to it' if mods else ''))
                    types = [re.search(r'<Type>\s*([^<\s]+)\s*</Type>', rec) for rec in recs]
                    types = [m2.group(1) for m2 in types if m2]
                    e = const.get(types[0]) if types else None
                    order = [k for k, v in sorted(R[e].items(), key=lambda kv: kv[1])
                             if isinstance(v, int) and v >= 0 and not k.startswith(('NUM_', 'NO_', 'MAX_'))] if e else []
                    if order:
                        if types == order: st, det = 'ok', f'{len(types)} records in the order of {e}'
                        elif types[:len(order)] == order:
                            st, det = 'ok', (f'the {len(order)} values of {e} are its first records, in order; '
                                             f'{len(types) - len(order)} more records have no enum value')
                        else:
                            k = next((j for j in range(min(len(types), len(order))) if types[j] != order[j]), min(len(types), len(order)))
                            st = 'differs'
                            det = (f'{len(types)} records, {len(order)} values of {e}; first difference at position {k}: '
                                   f'{types[k] if k < len(types) else "(end)"} in the file, {order[k] if k < len(order) else "(end)"} in the enum')
                        add(fid, 'xml order', f'{folder}/{root}.xml', ln, f'enum {e} (CvEnums.h)', st,
                            det + ('; module files can add records after these' if mods else ''))
            if nm in ('getDefineINT', 'getDefineFLOAT', 'getDefineSTRING', 'getDefineBOOL'):
                s = STR.match(argtext.strip())
                if s:
                    d = defines.get(s.group(1))
                    add(fid, 'define', s.group(1), ln, 'the global defines the DLL loads',
                        'ok' if d else 'missing', f'{d[0]} in {d[1]}' if d else 'not in any defines file the loader reads')
            if nm.startswith('getBugOption'):
                ar = split_args(argtext)
                s = STR.fullmatch(ar[0]) if ar else None
                if s:
                    where = bug.get(s.group(1))
                    fb = STR.fullmatch(ar[2]).group(1) if len(ar) > 2 and STR.fullmatch(ar[2]) else None
                    d = defines.get(fb) if fb else None
                    add(fid, 'bug option', s.group(1), ln, 'the BUG configuration (Python), else a global define',
                        'ok' if where else 'missing', (f'in {where}' if where else 'no such option') +
                        (f'; fallback define {fb}: ' + (f'{d[0]} in {d[1]}' if d else 'missing') if fb else ''))
            if nm in ('genericEvent',):
                s = STR.match(argtext.strip())
                if s:
                    hs = regs.get(s.group(1), [])
                    add(fid, 'event', s.group(1), ln, 'Python handlers registered for the event',
                        f'{len(hs)} handlers', '; '.join(f"{h['handler']} ({h['file']}:{h['line']})" for h in hs))
            if re.match(r'(get\w*Rand\w*|shuffleArray)$', nm) and not re.match(r'get\w+Info$', nm):
                add(fid, 'random', nm, ln, 'network sync and replays from a seed',
                    'synchronised' if re.search(r'Soren|Map', nm + argtext) else 'not synchronised',
                    re.sub(r'\s+', ' ', t[m.start():close + 1])[:120])
            if nm in ('logBBAI', 'logMsg', 'sprintf', 'format', 'messageControlLog'):
                for s in STR.finditer(argtext):
                    fmt = s.group(1)
                    if '%' not in fmt and not fmt.endswith('\\n'): continue
                    # the longest fixed piece of the format is what a reader of the log would match on
                    piece = max((x.strip(' :(),;[]') for x in re.split(r'%[-+ #0-9.]*[a-zA-Z]|\\n', fmt)), key=len)
                    if not piece: continue   # a piece of a longer entry, with no text of its own
                    if len(piece) < 12:
                        add(fid, 'log format', fmt[:90], ln, 'tools that read the log', 'not searched',
                            f'its longest fixed text, "{piece}", is too short to search for'); continue
                    readers = sorted({p for p, txt in rtext if piece in txt})
                    add(fid, 'log format', fmt[:90], ln, 'tools that read the log',
                        f'read by {len(readers)} files' if readers else 'not read by the tools of this repository',
                        f'searched for "{piece}"' + (': ' + ', '.join(readers[:6]) if readers else ''))
            if nm.startswith('warLog'):
                add(fid, 'log call', nm, ln, 'Logs/WarLog.log and the tools that read it',
                    f'read by {len(warlog_readers)} files', ', '.join(warlog_readers[:8]))

        # strings by their form
        for s in STR.finditer(t):
            v, ln = s.group(1), lineof(s.start())
            if v.startswith('TXT_KEY_'):
                add(fid, 'text key', v, ln, 'the text XML', 'ok' if v in texts else 'missing',
                    f'in the {labels.get(texts[v], texts[v])} text' if v in texts else '')
            elif re.match(r'AS[23]D_\w+$', v):
                add(fid, 'sound', v, ln, 'the audio scripts', 'ok' if v in sounds else 'missing',
                    f'in the {labels.get(sounds[v], sounds[v])} audio XML' if v in sounds else '')

        # calls found by the compiler: Python functions and events
        for p in cpp2py.get(fid, []):
            add(fid, 'python call', f"{p['module']}.{p['python_function']}", int(p['line']), 'the Python function of that name',
                'ok' if p['python_file'] else 'missing', f"{p['python_file']}:{p['python_line']}" if p['python_file'] else '')
        for c, ln in callees.get(fid, []):
            if F[c]['scope'] != 'CvEventReporter': continue
            for d, _ in callees.get(c, []):
                if d in events:
                    hs = regs.get(events[d], [])
                    add(fid, 'event', events[d], int(ln) if ln else a, 'Python handlers registered for the event',
                        f'{len(hs)} handlers', '; '.join(f"{h['handler']} ({h['file']}:{h['line']})" for h in hs[:8]) + (' …' if len(hs) > 8 else ''))

        # enums
        used = collections.OrderedDict()
        for m in re.finditer(r'\b([A-Z][A-Z0-9_]*)\b', tb):
            if m.group(1) in const: used.setdefault(const[m.group(1)], lineof(m.start()))
        for e, ln in used.items():
            if e in O:
                moved = [k for k, v in O[e].items() if k in R[e] and R[e][k] != v and not k.startswith(('NUM_', 'MAX_'))]
                gone = [k for k in O[e] if k not in R[e]]
                added = [k for k in R[e] if k not in O[e] and not k.startswith('NUM_')]
                add(fid, 'enum values', e, ln, 'the game exe, compiled with the original values',
                    'differs' if moved or gone else 'ok',
                    f"{len(O[e])} values in the original SDK" +
                    (f'; {len(added)} added by the mod' if added else '') +
                    (f'; moved: {", ".join(moved[:5])}' if moved else '') + (f'; removed: {", ".join(gone[:5])}' if gone else ''))
            else:
                add(fid, 'enum values', e, ln, 'Python and XML by name', 'not in the original SDK')
        def switches(lo, hi):
            out = []
            for m in re.finditer(r'\bswitch\s*\(', tb[lo:hi]):
                p0 = lo + m.start(); pc = match_close(tb, lo + m.end() - 1)
                ob_ = tb.find('{', pc); cb = match_close(tb, ob_, '{', '}')
                out.append((p0, ob_, cb))
            return out
        allsw = switches(0, len(tb))
        for p0, ob_, cb in allsw:
            inner = [(x, y) for q, x, y in allsw if ob_ < q < cb]
            labs = [(m.group(1), ob_ + m.start()) for m in re.finditer(r'\bcase\s+([A-Za-z_]\w*)\s*:', tb[ob_:cb])]
            labs = [l for l, q in labs if not any(x < q < y for x, y in inner)]
            es = collections.Counter(const[l] for l in labs if l in const)
            if not es: continue
            e = es.most_common(1)[0][0]
            vals = [k for k, v in sorted(R[e].items(), key=lambda kv: kv[1])
                    if isinstance(v, int) and v >= 0 and not k.startswith(('NUM_', 'NO_', 'MAX_'))]
            miss = [k for k in vals if k not in labs]
            has_default = any(not any(x < ob_ + m.start() < y for x, y in inner) for m in re.finditer(r'\bdefault\s*:', tb[ob_:cb]))
            add(fid, 'enum switch', e, lineof(p0), f'enum {e}: a value added later needs a case',
                f'{len(miss)} values without a case' if miss else 'every value has a case',
                f'{len(set(labs))} cases of {len(vals)} values' + ('; default case present' if has_default else '; no default case') +
                (f'; without a case: {", ".join(miss[:12])}' + (' …' if len(miss) > 12 else '') if miss else ''))

        # numbers
        for m in re.finditer(r'(?<![\w.])(0x[0-9A-Fa-f]+|\d+(?:\.\d+)?f?)(?![\w.])', tb):
            v = m.group(1)
            if v in ('0', '1', '0.0f', '1.0f'): continue
            ln = lineof(m.start())
            add(fid, 'number', v, ln, 'fixed in the code', 'fixed', re.sub(r'\s+', ' ', lines[ln - 1]).strip()[:120])

        # member state set directly
        cls_files = sorted({F[i]['file'] for i in F if F[i]['scope'] == r['scope'] and F[i]['file'].endswith('.cpp')})
        members = collections.OrderedDict()
        for m in re.finditer(r'(?:\+\+|--)\s*(m_\w+)\b|\b(m_\w+)\s*(?:\[[^\]]*\]\s*)?(?:=(?!=)|\+=|-=|\+\+|--)', tb):
            members.setdefault(m.group(1) or m.group(2), lineof(m.start()))
        for mem, ln in members.items():
            others = set()
            for cf in cls_files:
                ct = blank_strings(clean(open(os.path.join(dll, cf), encoding='latin-1').read())).split('\n')
                for k, l in enumerate(ct, 1):
                    if re.search(r'(?:\+\+|--)\s*' + mem + r'\b|\b' + mem + r'\s*(?:\[[^\]]*\]\s*)?(?:=(?!=)|\+=|-=|\+\+|--)', l):
                        g = next((i for i in F if F[i]['file'] == cf and F[i]['line'] and int(F[i]['line']) <= k <= int(F[i]['end'])), None)
                        if g and g != fid: others.add(g)
            names = sorted(F[g]['name'] for g in others)
            add(fid, 'state', mem, ln, 'the other functions that set it', f'set by {len(others)} other functions',
                ', '.join(names[:8]) + (' …' if len(names) > 8 else ''))

        freed = [(m.group(1), lineof(m.start())) for m in re.finditer(r'\bdeleteInfoArray\s*\(\s*(m_\w+)\s*\)', tb)]
        if freed:
            g = blank_strings(clean(open(os.path.join(dll, 'CvGlobals.cpp'), encoding='latin-1').read()))
            getter = {m.group(1): m.group(2) for m in
                      re.finditer(r'CvGlobals::(\w+)\s*\(\s*\)\s*(?:const\s*)?\{\s*return\s+(m_\w+)\s*;', g)}
            filled = collections.defaultdict(list)   # member -> loader call sites
            for lf in sorted(f for f in os.listdir(dll) if f.startswith('CvXMLLoadUtility') and f.endswith('.cpp')):
                lt = clean(open(os.path.join(dll, lf), encoding='latin-1').read())
                for m in re.finditer(r'\bLoad(?:GlobalClassInfo\w*|DiplomacyInfo)\s*\(\s*GC\.(\w+)\(\)', lt):
                    filled[getter.get(m.group(1), m.group(1))].append(f'{lf}:{lt.count(chr(10), 0, m.start()) + 1}')
            fc = collections.Counter(x for x, _ in freed)
            add(fid, 'release', f'{len(freed)} tables', a, 'the tables the XML loaders fill',
                'ok' if not [k for k in filled if k not in fc] and max(fc.values()) == 1 else 'differs',
                f'{len(filled)} tables filled by LoadGlobalClassInfo/LoadDiplomacyInfo; '
                f'{len([k for k in filled if k in fc])} of them freed here')
            for k in sorted(filled):
                if k not in fc: add(fid, 'release', k, a, 'the tables the XML loaders fill', 'filled, not freed', ', '.join(filled[k]))
            for k, ln in freed:
                if fc[k] > 1: add(fid, 'release', k, ln, 'the tables the XML loaders fill', 'freed twice')
                if k not in filled: add(fid, 'release', k, ln, 'the tables the XML loaders fill',
                                        'freed, filled elsewhere', 'not filled by LoadGlobalClassInfo/LoadDiplomacyInfo')

        if re.match(r'\s*(?:virtual\s+)?bool\b', decl):
            # a virtual method is also called through each method it overrides
            via, todo = {fid}, [fid]
            while todo:
                x = todo.pop()
                for o in overrides.get(x, ()):
                    if o not in via: via.add(o); todo.append(o)
            cs = sorted({c for v in via for c in callers.get(v, ())}, key=lambda i: query.name[i])
            add(fid, 'return value', 'bool', a, 'the functions that call it', f'{len(cs)} callers',
                ', '.join(query.name[i] for i in cs[:8]) + (' …' if len(cs) > 8 else '') +
                (f' (through {", ".join(query.name[v] for v in sorted(via - {fid}))})' if len(via) > 1 else ''))

    order = {k: n for n, k in enumerate(KINDS)}
    pos = {f: n for n, f in enumerate(fsel)}
    seen, uniq = set(), []
    for x in sorted(rows, key=lambda x: (pos[x[0]], order[x[1]], x[3], x[2], x[6])):
        if x not in seen: seen.add(x); uniq.append(x)
    rows = uniq
    with open(os.path.join(M, 'hardcoded.tsv'), 'w', encoding='utf-8') as o:
        o.write('\t'.join(['function', 'kind', 'entry', 'line', 'depends_on', 'status', 'detail']) + '\n')
        for x in rows: o.write('\t'.join(str(v).replace('\t', ' ').replace('\n', ' ') for v in x) + '\n')
    render(cm, F, query, fsel, rows)
    print(f'{len(rows)} entries in {len(fsel)} functions', file=sys.stderr)


def render(cm, F, query, fsel, rows):
    by = collections.defaultdict(list)
    for x in rows: by[x[0]].append(x)
    ok = ('ok', 'fixed', 'synchronised', 'in the original SDK', 'in the original SDK interfaces', 'every value has a case',
          'freed, filled elsewhere')
    L = ['# Hard-coded entries of the key functions\n',
         'Generated by `codemap/tool/hardcoded.py`. For each key function (`query.py rank`), the entries written '
         'into its own lines, and what outside the function depends on each: the game exe, the XML, Python, '
         'the enums, the logs this repository reads. Each status is checked against the files that hold the '
         'other end. The table is `map/hardcoded.tsv`.\n',
         '## Counts\n',
         '| function | ' + ' | '.join(KINDS) + ' |', '|---|' + '---|' * len(KINDS)]
    for f in fsel:
        c = collections.Counter(x[1] for x in by[f])
        L.append(f'| {query.name[f]} | ' + ' | '.join(str(c[k]) if c[k] else '' for k in KINDS) + ' |')
    flagged = [x for x in rows if not x[5].startswith(ok) and x[1] not in ('number', 'state', 'return value', 'fork change',
                                                                      'original', 'log format', 'log call', 'event', 'enum switch')]
    L.append('\n## Entries whose other end is missing or differs\n')
    L.append('Statuses other than ok for exports, exe calls, XML, defines, BUG options, text, sounds, Python calls '
             'and enum values.\n')
    if flagged:
        L.append('| function | kind | entry | line | status | detail |'); L.append('|---|---|---|---|---|---|')
        for x in flagged: L.append(f'| {query.name[x[0]]} | {x[1]} | `{x[2]}` | {x[3]} | {x[5]} | {x[6]} |')
    else:
        L.append('None.')
    for f in fsel:
        r = F[f]
        L.append(f"\n## {query.name[f]}\n\n{r['file']}:{r['line']}-{r['end']}\n")
        L.append('| kind | entry | line | depends on | status | detail |'); L.append('|---|---|---|---|---|---|')
        for x in by[f]:
            L.append(f'| {x[1]} | `{x[2]}` | {x[3]} | {x[4]} | {x[5]} | {x[6]} |'.replace('`|', '`\\|'))
    open(os.path.join(cm, 'hardcoded.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
