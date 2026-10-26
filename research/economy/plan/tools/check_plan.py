#!/usr/bin/env python3
"""Check the Settlement Economy files together: design.json (the design and its decisions), plan.json (the
implementation: components, features, tasks), requests.json (every prompt verbatim, and the requests with items).

  check_plan.py --summary            no mod checkout needed: open requests, design coverage, decisions, progress,
                                     the features that can start and their open tasks. Run it first in every session.
  check_plan.py <mod checkout>       also confirms every code anchor, runs every check and invariant, prints the report
                                     per component and writes status.json.
  check_plan.py task <ID> done|todo [--note TEXT]     mark a task (e.g. LQ.F1.T2) and save plan.json
  check_plan.py item <ID> open|planned|done [--where TEXT]   mark a request item (e.g. R1.5) and save requests.json

A feature is done when all its tasks are done and all its checks pass. Check kinds: 'added' (text the work adds, or a
file), 'audit' (icons, font_pinned, catalogue, callsites_classified, callsites_converted with 'classes'), 'evidence'
(a file in this repository), 'manual' (confirmations.json under the check id, e.g. LQ.F5.0), 'plan_valid'.
Exit 1 when the files are inconsistent or an anchor is broken."""
import argparse, datetime, glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
J = lambda n, d=None: json.load(open(os.path.join(HERE, n))) if os.path.exists(os.path.join(HERE, n)) else d
SAVE = lambda n, obj: json.dump(obj, open(os.path.join(HERE, n), 'w'), indent=1, ensure_ascii=False)
DESIGN, PLAN, REQ = J('design.json'), J('plan.json'), J('requests.json')
CONF, STATUS = J('confirmations.json', {}), J('status.json', {})
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DECISIONS = {d['id']: d for d in DESIGN['decisions']}
ELEMENTS = {e['id']: e for e in DESIGN['elements']}
FEATURES = {f['id']: (c, f) for c in PLAN['components'] for f in c['features']}
TASKS = {t['id']: (f, t) for c in PLAN['components'] for f in c['features'] for t in f['tasks']}
ITEMS = {i['id']: (r, i) for r in REQ['requests'] for i in r['items']}
TODAY = datetime.date.today().isoformat()

# ---------- edits ----------
if len(sys.argv) > 1 and sys.argv[1] in ('task', 'item'):
    ap = argparse.ArgumentParser(); ap.add_argument('what'); ap.add_argument('id'); ap.add_argument('status')
    ap.add_argument('--note'); ap.add_argument('--where'); e = ap.parse_args()
    if e.what == 'task':
        if e.id not in TASKS or e.status not in ('todo', 'done'): sys.exit('unknown task %s or status %s' % (e.id, e.status))
        t = TASKS[e.id][1]; t['status'] = e.status
        if e.status == 'done': t['done'] = TODAY
        else: t.pop('done', None)
        if e.note: t['note'] = e.note
        SAVE('plan.json', PLAN)
    else:
        if e.id not in ITEMS or e.status not in ('open', 'planned', 'done'): sys.exit('unknown item %s or status %s' % (e.id, e.status))
        r, i = ITEMS[e.id]; i['status'] = e.status
        if e.where: i['where'] = e.where
        r['status'] = 'done' if all(x['status'] == 'done' for x in r['items']) else 'open'
        SAVE('requests.json', REQ)
    print('%s %s: %s' % (e.what, e.id, e.status)); sys.exit(0)

ap = argparse.ArgumentParser()
ap.add_argument('mod', nargs='?'); ap.add_argument('--summary', action='store_true'); ap.add_argument('--component')
a = ap.parse_args()
_cache = {}


def text(rel):
    p = os.path.join(a.mod, rel)
    if p not in _cache: _cache[p] = open(p, encoding='latin-1').read() if os.path.isfile(p) else None
    return _cache[p]


# ---------- validation ----------
def closure(cid, seen=None):
    seen = set() if seen is None else seen
    for d in next(c for c in PLAN['components'] if c['id'] == cid)['depends_on']:
        if d not in seen: seen.add(d); closure(d, seen)
    return seen


def cycles(graph):
    errs, seen, stack = [], set(), set()

    def visit(n):
        if n in stack: errs.append('cycle through %s' % n); return
        if n in seen: return
        stack.add(n)
        for m in graph.get(n, []): visit(m)
        stack.discard(n); seen.add(n)
    for n in graph: visit(n)
    return errs


def dups(name, v):
    d = sorted({x for x in v if v.count(x) > 1})
    return ['duplicate %s ids %s' % (name, d)] if d else []


def validate():
    errs = []
    cids = [c['id'] for c in PLAN['components']]
    errs += dups('component', cids) + dups('feature', [f['id'] for c in PLAN['components'] for f in c['features']])
    errs += dups('task', [t['id'] for c in PLAN['components'] for f in c['features'] for t in f['tasks']])
    errs += dups('decision', [d['id'] for d in DESIGN['decisions']]) + dups('design element', [e['id'] for e in DESIGN['elements']])
    errs += dups('prompt', [p['id'] for p in REQ['prompts']]) + dups('request item', [i['id'] for r in REQ['requests'] for i in r['items']])
    for c in PLAN['components']:
        errs += ['%s depends on unknown %s' % (c['id'], d) for d in c['depends_on'] if d not in cids]
        errs += ['%s names unknown decision %s' % (c['id'], d) for d in c['decisions'] if d not in DECISIONS]
        for f in c['features']:
            if not f['id'].startswith(c['id'] + '.'): errs.append('%s is not named after %s' % (f['id'], c['id']))
            for key in ('code', 'checks', 'tasks', 'design'):
                if not f.get(key): errs.append('%s has no %s' % (f['id'], key))
            errs += ['%s serves unknown design element %s' % (f['id'], x) for x in f.get('design', []) if x not in ELEMENTS]
            for t in f['tasks']:
                if not t['id'].startswith(f['id'] + '.T'): errs.append('task %s is not named after %s' % (t['id'], f['id']))
                if t.get('status') not in ('todo', 'done'): errs.append('task %s has status %s' % (t['id'], t.get('status')))
            for x in f.get('after', []):
                if x not in FEATURES: errs.append('%s comes after unknown %s' % (f['id'], x))
                elif FEATURES[x][0]['id'] != c['id'] and FEATURES[x][0]['id'] not in closure(c['id']):
                    errs.append('%s comes after %s, whose component %s is not among %s\'s dependencies' % (f['id'], x, FEATURES[x][0]['id'], c['id']))
    for d in DESIGN['decisions']:
        if d['status'] == 'decided' and not d.get('choice'): errs.append('%s decided without a choice' % d['id'])
        if d['status'] == 'open' and not d.get('options'): errs.append('%s open without options' % d['id'])
    pids = {p['id'] for p in REQ['prompts']}
    for r in REQ['requests']:
        if r.get('prompt') not in pids: errs.append('request %s names unknown prompt %s' % (r['id'], r.get('prompt')))
        errs += ['item %s has status %s' % (i['id'], i['status']) for i in r['items'] if i['status'] not in ('open', 'planned', 'done')]
    errs += ['components: ' + e for e in cycles({c['id']: c['depends_on'] for c in PLAN['components']})]
    errs += ['features: ' + e for e in cycles({k: f.get('after', []) for k, (c, f) in FEATURES.items()})]
    return errs


def coverage():
    served = {x for c in PLAN['components'] for f in c['features'] for x in f['design']}
    return [e['id'] for e in DESIGN['elements'] if e['id'] not in served and not e.get('cross_cutting')]


# ---------- audits ----------
def records(paths, tag):
    """Records of the files, without those inside XML comments (the game does not load them)."""
    out = []
    for p in paths:
        live = re.sub(r'<!--.*?-->', '', open(p, encoding='latin-1').read(), flags=re.S)
        out += re.findall(r'<%s>(.*?)</%s>' % (tag, tag), live, re.S)
    return out


def xml_paths(base, pattern):
    A = os.path.join(a.mod, 'Assets')
    return [os.path.join(A, base)] + sorted(glob.glob(os.path.join(A, 'Modules', '**', pattern), recursive=True))


def audit_icons(chk):
    art = {}
    for b in records(xml_paths('XML/Art/CIV4ArtDefines_Bonus.xml', '*ArtDefines_Bonus.xml'), 'BonusArtInfo'):
        fi = re.search(r'<FontButtonIndex>(\d+)', b); btn = re.search(r'<Button>([^<]*)', b)
        art[re.search(r'<Type>(\w+)', b).group(1)] = (int(fi.group(1)) if fi else None, btn.group(1) if btn else '')
    bonus = {re.search(r'<Type>(\w+)', b).group(1): re.search(r'<ArtDefineTag>(\w+)', b).group(1)
             for b in records(xml_paths('XML/Terrain/CIV4BonusInfos.xml', '*BonusInfos.xml'), 'BonusInfo')}
    problems, by_index = [], {}
    for g, tag in sorted(bonus.items()):
        if tag not in art: problems.append('%s: art define %s missing' % (g, tag)); continue
        if art[tag][0] is None: problems.append('%s: no FontButtonIndex' % g)
        else: by_index.setdefault(art[tag][0], []).append(g)
        if not art[tag][1].strip(','): problems.append('%s: no button' % g)
    problems += ['glyph %d shared by %s' % (i, ', '.join(gs)) for i, gs in sorted(by_index.items()) if len(gs) > 1]
    return not problems, '%d goods, %d art defines; %s' % (len(bonus), len(art), '; '.join(problems) or 'every good has its own glyph and button')


FIRST_SYMBOL = 8483   # first symbol code the BTS executable passes to CvGameTextMgr::assignFontIds (not in the mod's sources)
EXTRAS_AT = 75        # both GameFont sheets hold the happy face 50 cells before resource cell 0 = bonus base + 125 - 50


def symbol_base():
    """The bonus base S of CvGameTextMgr::assignFontIds, step by step as the code runs: yields, a step to the next
    multiple of 25, commerce, two steps, two codes per religion and corporation, a step (two below 25 codes). Counts
    from the DLL enums and the XML, modules included."""
    enums = text('Assets/CvGameCoreDLL/CvEnums.h') or ''
    def count(name):
        body = re.search(r'enum %s\b[^{]*\{(.*?)\}' % name, enums, re.S).group(1)
        return len([x for x in (y.strip() for y in re.sub(r'//.*', '', body).split(',')) if x and not x.startswith(('NO_', 'NUM_', '#'))])
    step = lambda c: c + 25 - c % 25   # do { ++c; } while (c % 25 != 0)
    rel = len({re.search(r'<Type>(\w+)', b).group(1) for b in records(xml_paths('XML/GameInfo/CIV4ReligionInfo.xml', '*ReligionInfo*.xml'), 'ReligionInfo')})
    corp = len({re.search(r'<Type>(\w+)', b).group(1) for b in records(xml_paths('XML/GameInfo/CIV4CorporationInfo.xml', '*CorporationInfo*.xml'), 'CorporationInfo')})
    c = step(FIRST_SYMBOL + count('YieldTypes'))
    c = step(step(c + count('CommerceTypes')))
    c = step(c + 2 * (rel + corp))
    return step(c) if 2 * (rel + corp) < 25 else c


def audit_font_pinned(chk):
    m = re.search(r'<DefineName>WOC_GAMEFONT_RESOURCE_FIX</DefineName>\s*<iDefineIntVal>(-?\d+)', text('Assets/XML/GlobalDefinesAlt.xml') or '')
    v = int(m.group(1)) if m else None
    want = symbol_base() + EXTRAS_AT
    return v == want, 'WOC_GAMEFONT_RESOURCE_FIX = %s, the fonts\' extra symbols at %d' % (v, want)


def audit_catalogue(chk):
    xml = sorted({re.search(r'<Type>(\w+)', b).group(1) for b in records(xml_paths('XML/Terrain/CIV4BonusInfos.xml', '*BonusInfos.xml'), 'BonusInfo')})
    cat = J('catalogue.json', {}).get('goods', {}); prop = J('proposals.json', {}).get('goods', {})
    probs = []
    if sorted(cat) != xml: probs.append('catalogue.json out of date (run tools/catalogue.py): %s' % sorted(set(xml) ^ set(cat))[:6])
    miss = [g for g in xml if g not in prop]
    if miss: probs.append('no proposal for %s' % miss[:6])
    return not probs, '; '.join(probs) or '%d goods, all with a proposal' % len(xml)


def callsite_scan():
    import callsites
    return callsites.scan(a.mod), J('callsites.json', {}).get('classes', {})


def audit_callsites_classified(chk):
    sites, classes = callsite_scan()
    un = sorted({s['function'] for s in sites if s['function'] not in classes})
    return not un, ('%d call sites, all classified' % len(sites)) if not un else 'unclassified (run tools/callsites.py, then classify): %s' % un[:8]


def audit_callsites_converted(chk):
    sites, classes = callsite_scan()
    left = [s for s in sites if classes.get(s['function']) in chk['classes']]
    return not left, ('no token reads left in classes %s' % chk['classes']) if not left else '%d token reads left in classes %s, e.g. %s' % (
        len(left), chk['classes'], ', '.join(sorted({s['function'] for s in left})[:5]))


AUDITS = dict(icons=audit_icons, font_pinned=audit_font_pinned, catalogue=audit_catalogue,
              callsites_classified=audit_callsites_classified, callsites_converted=audit_callsites_converted)


def run_check(chk, cid):
    k = chk['kind']
    if k == 'added':
        t = text(chk['file'])
        if 'text' not in chk: return t is not None, chk['file'] + (' exists' if t is not None else ' not yet')
        return t is not None and chk['text'] in t, '%s in %s' % (chk['text'], chk['file'])
    if k == 'audit': return AUDITS[chk['name']](chk)
    if k == 'manual':
        c = CONF.get(cid)
        return c is not None, ('confirmed %s: %s' % (c.get('date'), c.get('note', ''))) if c else 'to confirm in game: ' + chk['what']
    if k == 'evidence':
        return os.path.exists(os.path.join(REPO, chk['path'].replace('<component>', cid.split('.')[0]))), chk['path']
    if k == 'plan_valid':
        e = validate(); return not e, '; '.join(e) or 'valid'
    return False, 'unknown check kind ' + k


# ---------- summary ----------
def tasks_done(f): return sum(t['status'] == 'done' for t in f['tasks'])


def feature_done(f): return tasks_done(f) == len(f['tasks']) and STATUS.get('checks', {}).get(f['id'], False)


def summary():
    m = PLAN['repositories']['mod']
    print('Settlement Economy. Mod work: %s, branch %s (%s). Checks recorded: %s' % (m['project'], m['branch'], m['access'],
          '%s, mod %s' % (STATUS.get('checked'), STATUS.get('mod_commit')) if STATUS else 'none yet'))
    cur = PLAN.get('current', {})
    if cur:
        print('CURRENT (read first; update it with every commit): %s, as of %s' % (cur.get('mod_head', '?'), cur.get('updated', '?')))
        for k in ('in_flight', 'next', 'environment'):
            for l in cur.get(k, []): print('  %s: %s' % (k, l))
    print('Requests open:')
    for r in REQ['requests']:
        for i in r['items']:
            if i['status'] != 'done': print('  %s [%s] %s%s' % (i['id'], i['status'], i['what'], ' -> ' + i['where'] if i.get('where') else ''))
    un = coverage()
    print('Design: %d elements, %s' % (len(DESIGN['elements']), 'all served by features' if not un else 'NOT SERVED: ' + ', '.join(un)))
    print('Decisions:')
    for d in DESIGN['decisions']:
        print('  %s %s: %s' % (d['id'], d['question'], d['choice'] if d['status'] == 'decided' else 'OPEN, proposed: %s' % d.get('proposal', '-')))
    done_c = set()
    for c in PLAN['components']:
        fd = sum(feature_done(f) for f in c['features'])
        td = sum(tasks_done(f) for f in c['features']); tt = sum(len(f['tasks']) for f in c['features'])
        if fd == len(c['features']): done_c.add(c['id'])
        print('  %s %s: features %d/%d, tasks %d/%d%s' % (c['id'], c['title'], fd, len(c['features']), td, tt, ' (after ' + ', '.join(c['depends_on']) + ')' if c['depends_on'] else ''))
    ready = [c for c in PLAN['components'] if c['id'] not in done_c and all(x in done_c for x in c['depends_on'])]
    for c in ready[:1]:
        od = [d for d in c['decisions'] if DECISIONS[d]['status'] == 'open']
        print('Next component: %s %s%s' % (c['id'], c['title'], ' (open decisions: %s)' % ', '.join(od) if od else ''))
        for f in c['features']:
            if feature_done(f): continue
            waiting = [x for x in f.get('after', []) if not feature_done(FEATURES[x][1])]
            print('  %s %s %s' % ('can start:' if not waiting else 'after %s:' % ', '.join(waiting), f['id'], f['what']))
            if not waiting:
                for t in f['tasks']:
                    if t['status'] != 'done': print('      %s %s' % (t['id'], t['text']))
    for l in PLAN.get('resume', []): print(l)


errors = validate()
if errors:
    print('FILES INCONSISTENT'); [print('  ' + e) for e in errors]; sys.exit(1)
if a.summary or not a.mod:
    summary(); sys.exit(0)

broken, report, checks_ok = [], [], {}
for c in PLAN['components']:
    if a.component and c['id'] != a.component: continue
    lines, aok, an = [], 0, 0
    for f in c['features']:
        for s in f['code']:
            an += 1; t = text(s['file'])
            ok = t is not None and ('anchor' not in s or s['anchor'] in t)
            aok += ok
            if not ok: broken.append('%s: %s' % (s['file'], s.get('anchor', '(file)'))); lines.append('    ANCHOR BROKEN ' + broken[-1])
        res = [run_check(chk, '%s.%d' % (f['id'], i)) for i, chk in enumerate(f['checks'])]
        checks_ok[f['id']] = all(r[0] for r in res)
        done = checks_ok[f['id']] and tasks_done(f) == len(f['tasks'])
        lines.append('  [%s] %s %s (tasks %d/%d)' % ('x' if done else ' ', f['id'], f['what'][:85], tasks_done(f), len(f['tasks'])))
        lines += ['        - ' + m[:220] for ok, m in res if not ok]
    od = [d for d in c['decisions'] if DECISIONS[d]['status'] == 'open']
    report.append('%s %s: anchors %d/%d%s' % (c['id'], c['title'], aok, an, ', open decisions ' + ', '.join(od) if od else ''))
    report += lines
print('\n'.join(report)); print()
for inv in PLAN['invariants']:
    ok, msg = run_check(inv['check'], inv['id'])
    print('invariant %s %s: %s' % (inv['id'], 'ok' if ok else 'OPEN', msg[:220]))
un = coverage()
print('design: %s' % ('every element served' if not un else 'not served: ' + ', '.join(un)))
if not a.component:
    try: commit = subprocess.run(['git', '-C', a.mod, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip() or None
    except Exception: commit = None
    try: branch = subprocess.run(['git', '-C', a.mod, 'branch', '--show-current'], capture_output=True, text=True).stdout.strip() or None
    except Exception: branch = None
    SAVE('status.json', dict(checked=TODAY, mod_commit=commit, mod_branch=branch, checks=checks_ok, broken_anchors=broken))
    if branch and branch != PLAN['repositories']['mod']['branch']:
        print('NOTE: the checkout is on %s, the plan\'s branch is %s' % (branch, PLAN['repositories']['mod']['branch']))
sys.exit(1 if broken else 0)
