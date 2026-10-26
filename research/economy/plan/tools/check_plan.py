#!/usr/bin/env python3
"""Check the Settlement Economy plan (plan.json).

--summary (no mod checkout needed): validates the plan and prints the decisions, the components in order with their
recorded progress (status.json), the features that can start now, and how to resume. Run it first in every session.

<mod checkout>: also confirms every code anchor in the mod source, evaluates every check and invariant, prints the
report per component and writes status.json (features done, broken anchors, the commit checked).

Check kinds: 'added' (text the work adds, or a file), 'audit' (icons, font_pinned, catalogue, callsites_classified,
callsites_converted with 'classes'), 'evidence' (a file in this repository), 'manual' (an entry in confirmations.json
under the check id, e.g. LQ.F5.0), 'plan_valid'. Exit 1 when the plan is invalid or an anchor is broken.
usage: check_plan.py --summary | check_plan.py <mod checkout> [--component ID]"""
import argparse, datetime, glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
ap = argparse.ArgumentParser()
ap.add_argument('mod', nargs='?'); ap.add_argument('--summary', action='store_true'); ap.add_argument('--component')
a = ap.parse_args()
J = lambda n, d=None: json.load(open(os.path.join(HERE, n))) if os.path.exists(os.path.join(HERE, n)) else d
P = J('plan.json'); CONF = J('confirmations.json', {}); STATUS = J('status.json', {})
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
FEATURES = {f['id']: (c, f) for c in P['components'] for f in c['features']}
_cache = {}


def text(rel):
    p = os.path.join(a.mod, rel)
    if p not in _cache: _cache[p] = open(p, encoding='latin-1').read() if os.path.isfile(p) else None
    return _cache[p]


def closure(cid, seen=None):
    seen = set() if seen is None else seen
    for d in next(c for c in P['components'] if c['id'] == cid)['depends_on']:
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


def validate():
    errs = []
    cids = [c['id'] for c in P['components']]; dids = [d['id'] for d in P['decisions']]
    for name, v in (('component', cids), ('feature', [f for c in P['components'] for f in [x['id'] for x in c['features']]]), ('decision', dids)):
        dup = sorted({x for x in v if v.count(x) > 1})
        if dup: errs.append('duplicate %s ids %s' % (name, dup))
    for c in P['components']:
        errs += ['%s depends on unknown %s' % (c['id'], d) for d in c['depends_on'] if d not in cids]
        errs += ['%s names unknown decision %s' % (c['id'], d) for d in c['decisions'] if d not in dids]
        for f in c['features']:
            if not f['id'].startswith(c['id'] + '.'): errs.append('%s is not named after %s' % (f['id'], c['id']))
            for key in ('code', 'checks', 'tasks'):
                if not f.get(key): errs.append('%s has no %s' % (f['id'], key))
            for x in f.get('after', []):
                if x not in FEATURES: errs.append('%s comes after unknown %s' % (f['id'], x))
                elif FEATURES[x][0]['id'] != c['id'] and FEATURES[x][0]['id'] not in closure(c['id']):
                    errs.append('%s comes after %s, whose component %s is not among %s\'s dependencies' % (f['id'], x, FEATURES[x][0]['id'], c['id']))
    for d in P['decisions']:
        if d['status'] == 'decided' and not d.get('choice'): errs.append('%s decided without a choice' % d['id'])
        if d['status'] == 'open' and not d.get('options'): errs.append('%s open without options' % d['id'])
    errs += ['components: ' + e for e in cycles({c['id']: c['depends_on'] for c in P['components']})]
    errs += ['features: ' + e for e in cycles({k: f.get('after', []) for k, (c, f) in FEATURES.items()})]
    return errs


def records(paths, tag):
    out = []
    for p in paths:
        out += re.findall(r'<%s>(.*?)</%s>' % (tag, tag), open(p, encoding='latin-1').read(), re.S)
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


def audit_font_pinned(chk):
    m = re.search(r'<DefineName>WOC_GAMEFONT_RESOURCE_FIX</DefineName>\s*<iDefineIntVal>(-?\d+)', text('Assets/XML/GlobalDefinesAlt.xml') or '')
    v = int(m.group(1)) if m else None
    return bool(v and v > 0), 'WOC_GAMEFONT_RESOURCE_FIX = %s' % v


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


def summary():
    done_f = STATUS.get('features', {})
    print('Settlement Economy plan: %s' % ('status of %s, mod %s' % (STATUS.get('checked'), STATUS.get('mod_commit')) if STATUS else 'no status recorded yet'))
    for d in P['decisions']:
        print('  %s %s: %s' % (d['id'], d['question'], d['choice'] if d['status'] == 'decided' else 'OPEN, proposed: %s' % d.get('proposal', '-')))
    done_c = set()
    for c in P['components']:
        n = sum(1 for f in c['features'] if done_f.get(f['id']))
        if n == len(c['features']): done_c.add(c['id'])
        print('  %s %s: %d/%d features done%s' % (c['id'], c['title'], n, len(c['features']), ' (after ' + ', '.join(c['depends_on']) + ')' if c['depends_on'] else ''))
    ready = [c for c in P['components'] if c['id'] not in done_c and all(x in done_c for x in c['depends_on'])]
    for c in ready[:1]:
        open_dec = [d for d in c['decisions'] if next(x for x in P['decisions'] if x['id'] == d)['status'] == 'open']
        print('next component: %s %s%s' % (c['id'], c['title'], ' (open decisions: %s)' % ', '.join(open_dec) if open_dec else ''))
        for f in c['features']:
            if done_f.get(f['id']): continue
            can = all(done_f.get(x) for x in f.get('after', []))
            print('  %s %s %s' % ('can start:' if can else 'after %s:' % ', '.join(x for x in f['after'] if not done_f.get(x)), f['id'], f['what']))
            if can:
                for t in f['tasks']: print('      - ' + t)
    for l in P.get('resume', []): print(l)


errors = validate()
if errors:
    print('PLAN INVALID'); [print('  ' + e) for e in errors]; sys.exit(1)
if a.summary or not a.mod:
    summary(); sys.exit(0)

broken, report, feat_done = [], [], {}
for c in P['components']:
    if a.component and c['id'] != a.component: continue
    lines, aok, an = [], 0, 0
    for f in c['features']:
        for s in f['code']:
            an += 1; t = text(s['file'])
            ok = t is not None and ('anchor' not in s or s['anchor'] in t)
            aok += ok
            if not ok:
                broken.append('%s: %s' % (s['file'], s.get('anchor', '(file)'))); lines.append('    ANCHOR BROKEN ' + broken[-1])
        res = [run_check(chk, '%s.%d' % (f['id'], i)) for i, chk in enumerate(f['checks'])]
        feat_done[f['id']] = all(r[0] for r in res)
        lines.append('  [%s] %s %s' % ('x' if feat_done[f['id']] else ' ', f['id'], f['what'][:95]))
        lines += ['        - ' + m[:220] for ok, m in res if not ok]
    blocked = [d for d in c['decisions'] if next(x for x in P['decisions'] if x['id'] == d)['status'] == 'open']
    report.append('%s %s: features %d/%d done, anchors %d/%d%s' % (c['id'], c['title'], sum(feat_done[f['id']] for f in c['features']), len(c['features']),
                                                                aok, an, ', open decisions ' + ', '.join(blocked) if blocked else ''))
    report += lines
print('\n'.join(report)); print()
for inv in P['invariants']:
    ok, msg = run_check(inv['check'], inv['id'])
    print('invariant %s %s: %s' % (inv['id'], 'ok' if ok else 'OPEN', msg[:220]))
if not a.component:
    try: commit = subprocess.run(['git', '-C', a.mod, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip() or None
    except Exception: commit = None
    json.dump(dict(checked=datetime.date.today().isoformat(), mod_commit=commit, features=feat_done, broken_anchors=broken),
              open(os.path.join(HERE, 'status.json'), 'w'), indent=1)
    done_c = {c['id'] for c in P['components'] if all(feat_done[f['id']] for f in c['features'])}
    print('\ncomponents that can start: %s' % ', '.join(c['id'] for c in P['components'] if c['id'] not in done_c and all(d in done_c for d in c['depends_on'])))
    print('decisions open: %s' % (', '.join('%s %s' % (d['id'], d['question']) for d in P['decisions'] if d['status'] == 'open') or 'none'))
sys.exit(1 if broken else 0)
