#!/usr/bin/env python3
"""Check the Settlement Economy plan (plan.json) against a mod checkout.

- validates the plan (unique ids, known dependencies and decisions, every feature has code and a check);
- confirms every code anchor still exists in the mod source (a moved or renamed function fails here);
- evaluates each feature's checks: 'added' (text the work adds), 'audit' (icons, font_pinned), 'evidence' (a file),
  'manual' (recorded in confirmations.json);
- reports per component: anchors, features done, open decisions, and which components can start next.
Exit code 1 when the plan is invalid or an anchor is broken.
With a checkout it writes status.json (each feature done or not, broken anchors, the commit checked); --summary
needs no checkout and prints the decisions, the components in order with their recorded progress, and what to do next.
usage: check_plan.py <mod checkout> [--plan plan.json] [--component ID] | check_plan.py --summary"""
import argparse, glob, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('mod', nargs='?'); ap.add_argument('--summary', action='store_true'); ap.add_argument('--plan', default=os.path.join(HERE, 'plan.json')); ap.add_argument('--component')
a = ap.parse_args()
P = json.load(open(a.plan))
CONF_PATH = os.path.join(os.path.dirname(a.plan), 'confirmations.json')
CONF = json.load(open(CONF_PATH)) if os.path.exists(CONF_PATH) else {}
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
_cache = {}


def text(rel):
    p = os.path.join(a.mod, rel)
    if p not in _cache:
        _cache[p] = open(p, encoding='latin-1').read() if os.path.isfile(p) else None
    return _cache[p]


def validate():
    errs = []
    ids = [c['id'] for c in P['components']]
    fids = [f['id'] for c in P['components'] for f in c['features']]
    dids = {d['id'] for d in P['decisions']}
    for name, v in (('component', ids), ('feature', fids), ('decision', [d['id'] for d in P['decisions']])):
        dup = {x for x in v if v.count(x) > 1}
        if dup: errs.append('duplicate %s ids %s' % (name, sorted(dup)))
    for c in P['components']:
        for d in c['depends_on']:
            if d not in ids: errs.append('%s depends on unknown %s' % (c['id'], d))
        for d in c['decisions']:
            if d not in dids: errs.append('%s names unknown decision %s' % (c['id'], d))
        for f in c['features']:
            if not f['id'].startswith(c['id'] + '.'): errs.append('%s is not named after %s' % (f['id'], c['id']))
            if not f.get('code'): errs.append('%s has no code section' % f['id'])
            if not f.get('checks'): errs.append('%s has no check' % f['id'])
    for d in P['decisions']:
        if d['status'] == 'decided' and not d.get('choice'): errs.append('%s decided without a choice' % d['id'])
        if d['status'] == 'open' and not d.get('options'): errs.append('%s open without options' % d['id'])
    # dependency cycles
    deps = {c['id']: c['depends_on'] for c in P['components']}
    seen, stack = set(), set()

    def visit(n):
        if n in stack: errs.append('dependency cycle through %s' % n); return
        if n in seen: return
        stack.add(n)
        for m in deps.get(n, []): visit(m)
        stack.discard(n); seen.add(n)
    for n in deps: visit(n)
    return errs


def records(paths, tag):
    out = []
    for f in paths:
        t = open(f, encoding='latin-1').read()
        out += [(m.group(1), os.path.relpath(f, a.mod)) for m in re.finditer(r'<%s>(.*?)</%s>' % (tag, tag), t, re.S)]
    return out


def audit_icons():
    A = os.path.join(a.mod, 'Assets')
    art = {}
    for body, f in records([os.path.join(A, 'XML/Art/CIV4ArtDefines_Bonus.xml')] + sorted(glob.glob(os.path.join(A, 'Modules/**/*ArtDefines_Bonus.xml'), recursive=True)), 'BonusArtInfo'):
        t = re.search(r'<Type>(\w+)', body).group(1)
        fi = re.search(r'<FontButtonIndex>(\d+)', body); btn = re.search(r'<Button>([^<]*)', body)
        art[t] = dict(index=int(fi.group(1)) if fi else None, button=btn.group(1) if btn else '')
    bonus = {}
    for body, f in records([os.path.join(A, 'XML/Terrain/CIV4BonusInfos.xml')] + sorted(glob.glob(os.path.join(A, 'Modules/**/*BonusInfos.xml'), recursive=True)), 'BonusInfo'):
        bonus[re.search(r'<Type>(\w+)', body).group(1)] = re.search(r'<ArtDefineTag>(\w+)', body).group(1)  # a module record replaces the base one
    problems, by_index = [], {}
    for b, tag in sorted(bonus.items()):
        if tag not in art: problems.append('%s: art define %s missing' % (b, tag)); continue
        if art[tag]['index'] is None: problems.append('%s: no FontButtonIndex' % b)
        else: by_index.setdefault(art[tag]['index'], []).append(b)
        if not art[tag]['button'].strip(','): problems.append('%s: no button' % b)
    for i, bs in sorted(by_index.items()):
        if len(bs) > 1: problems.append('glyph %d shared by %s' % (i, ', '.join(bs)))
    return not problems, '%d goods, %d art defines; %s' % (len(bonus), len(art), '; '.join(problems) if problems else 'every good has its own glyph and button')


def audit_font_pinned():
    t = text('Assets/XML/GlobalDefinesAlt.xml') or ''
    m = re.search(r'<DefineName>WOC_GAMEFONT_RESOURCE_FIX</DefineName>\s*<iDefineIntVal>(-?\d+)', t)
    v = int(m.group(1)) if m else None
    return bool(v and v > 0), 'WOC_GAMEFONT_RESOURCE_FIX = %s (%s)' % (v, 'pinned' if v and v > 0 else 'not pinned: adding goods shifts every symbol after the resources')


AUDITS = dict(icons=audit_icons, font_pinned=audit_font_pinned)


def run_check(chk, cid):
    k = chk['kind']
    if k == 'added':
        t = text(chk['file'])
        if 'text' not in chk: return (t is not None), chk['file'] + (' exists' if t is not None else ' not yet')
        return (t is not None and chk['text'] in t), '%s in %s' % (chk['text'], chk['file'])
    if k == 'audit':
        return AUDITS[chk['name']]()
    if k == 'manual':
        c = CONF.get(cid)
        return (c is not None), ('confirmed %s: %s' % (c.get('date'), c.get('note', '')) if c else 'to confirm in game: ' + chk['what'])
    if k == 'evidence':
        p = os.path.join(REPO, chk['path'].replace('<component>', cid.split('.')[0]))
        return os.path.exists(p), chk['path']
    if k == 'plan_valid':
        e = validate(); return not e, '; '.join(e) or 'valid'
    return False, 'unknown check kind ' + k


STATUS_PATH = os.path.join(os.path.dirname(a.plan), 'status.json')


def summary():
    st = json.load(open(STATUS_PATH)) if os.path.exists(STATUS_PATH) else {}
    feats = st.get('features', {})
    print('Settlement Economy plan: %s' % ('status of %s, %s' % (st.get('checked'), st.get('mod_commit')) if st else 'no status recorded yet'))
    for d in P['decisions']:
        print('  %s %s: %s' % (d['id'], d['question'], d.get('choice') if d['status'] == 'decided' else 'OPEN'))
    done = set()
    for c in P['components']:
        n = sum(1 for f in c['features'] if feats.get(f['id']))
        if n == len(c['features']): done.add(c['id'])
        print('  %s %s: %d/%d features done%s' % (c['id'], c['title'], n, len(c['features']), ' (after ' + ', '.join(c['depends_on']) + ')' if c['depends_on'] else ''))
    ready = [c for c in P['components'] if c['id'] not in done and all(x in done for x in c['depends_on'])]
    for c in ready[:1]:
        print('next: %s %s' % (c['id'], c['title']))
        for f in c['features']:
            if not feats.get(f['id']): print('  - %s %s' % (f['id'], f['what']))
    for l in P.get('resume', []): print(l)


if a.summary or not a.mod:
    errors = validate()
    if errors: print('PLAN INVALID: ' + '; '.join(errors)); sys.exit(1)
    summary(); sys.exit(0)

errors = validate()
if errors:
    print('PLAN INVALID'); [print('  ' + e) for e in errors]; sys.exit(1)
open_dec = {d['id'] for d in P['decisions'] if d['status'] == 'open'}
broken = 0; done_comp = set(); report = []; FEAT_DONE = {}; BROKEN = []
for c in P['components']:
    if a.component and c['id'] != a.component: continue
    anchors_ok = anchors = 0; fdone = 0; lines = []
    for f in c['features']:
        for s in f['code']:
            anchors += 1
            t = text(s['file'])
            ok = t is not None and (('anchor' not in s) or s['anchor'] in t)
            anchors_ok += ok
            if not ok:
                broken += 1; BROKEN.append('%s: %s' % (s['file'], s.get('anchor', '(file)'))); lines.append('    ANCHOR BROKEN %s: %s' % (s['file'], s.get('anchor', '(file)')))
        res = [(run_check(chk, f['id'] + '.%d' % i), chk) for i, chk in enumerate(f['checks'])]
        ok = all(r[0][0] for r in res)
        fdone += ok
        lines.append('  [%s] %s %s' % ('x' if ok else ' ', f['id'], f['what'][:90]))
        for (passed, msg), chk in res:
            if not passed: lines.append('        - %s' % msg[:200])
    blocked = sorted(set(c['decisions']) & open_dec)
    if fdone == len(c['features']): done_comp.add(c['id'])
    for f in c['features']:
        FEAT_DONE[f['id']] = all(run_check(chk, f['id'] + '.%d' % i)[0] for i, chk in enumerate(f['checks']))
    report.append((c, anchors_ok, anchors, fdone, blocked, lines))
for c, aok, an, fd, blocked, lines in report:
    print('%s %s: features %d/%d done, anchors %d/%d%s' % (c['id'], c['title'], fd, len(c['features']), aok, an,
                                                         ', waits on decision ' + ', '.join(blocked) if blocked else ''))
    for l in lines: print(l)
print()
for inv in P['invariants']:
    ok, msg = run_check(inv['check'], inv['id'])
    print('invariant %s %s: %s' % (inv['id'], 'ok' if ok else 'OPEN', msg[:220]))
if not a.component:
    ready = [c['id'] for c in P['components'] if c['id'] not in done_comp and all(d in done_comp for d in c['depends_on'])]
    print('\ndecisions open: %s' % (', '.join('%s %s' % (d['id'], d['question']) for d in P['decisions'] if d['status'] == 'open') or 'none'))
    print('components that can start: %s' % ', '.join(ready))
if not a.component:
    import datetime, subprocess
    try: commit = subprocess.run(['git', '-C', a.mod, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip() or None
    except Exception: commit = None
    json.dump(dict(checked=datetime.date.today().isoformat(), mod_commit=commit, features=FEAT_DONE, broken_anchors=BROKEN),
              open(STATUS_PATH, 'w'), indent=1)
sys.exit(1 if broken else 0)
