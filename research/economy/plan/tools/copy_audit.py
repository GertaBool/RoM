"""GW.F7.T3: for every info class with an XML read and a copyNonDefaults, the members the read sets that
copyNonDefaults (with copyNonDefaultsReadPass2) never mentions. A module file of partial records is merged by
copyNonDefaults, so such a member falls back to its default whenever a module overrides the record (M33).
A member counts as read when its name appears in X::read(CvXMLLoadUtility*) or X::readPass2..; as copied when it
appears in X::copyNonDefaults or X::copyNonDefaultsReadPass2, directly or through the getter the copy calls
(a getter is matched by the member it returns in CvInfos.cpp).
usage: copy_audit.py <Assets/CvGameCoreDLL> [class ...]   prints one line per class with missing members; exit 1 if any"""
import os, re, sys

src = sys.argv[1]; only = set(sys.argv[2:])
text = ''
for f in sorted(os.listdir(src)):
    if f.endswith('.cpp') and f.startswith('CvInfos') or f in ('CvInfos.cpp',):
        text += open(os.path.join(src, f), encoding='latin-1').read() + '\n'

def bodies(cls, name_re):
    """Bodies of the member functions of cls whose name matches name_re (brace-matched)."""
    out = []
    for m in re.finditer(r'^[\w:<>\*&\s]*\b%s::(%s)\s*\(([^)]*)\)[^{;]*\{' % (re.escape(cls), name_re), text, re.M):
        i, depth = m.end(), 1
        while depth and i < len(text):
            c = text[i]
            if c == '{': depth += 1
            elif c == '}': depth -= 1
            i += 1
        out.append((m.group(1), m.group(2), text[m.end():i]))
    return out

def members(body): return set(re.findall(r'\bm_[A-Za-z]\w*', body))

# Members the audit lists that need no copy, with the reason
KNOWN = {
    ('CvAnimationCategoryInfo', 'm_szDefaultTo'): 'read only to resolve m_kCategory during the read',
    ('CvBuildingClassInfo', 'm_aszExtraXMLforPass3'): 'copied through getDefaultBuildingIndexVectorElement',
    ('CvVoteSourceInfo', 'm_aszExtraXMLforPass3'): 'copied through its vector accessor in copyNonDefaults',
    ('CvUnitFormationInfo', 'm_fFacingDirection'): 'a field of the local CvUnitEntry read into the entry vectors',
    ('CvUnitFormationInfo', 'm_fFacingVariance'): 'a field of the local CvUnitEntry',
    ('CvUnitFormationInfo', 'm_fRadius'): 'a field of the local CvUnitEntry',
    ('CvUnitFormationInfo', 'm_position'): 'a field of the local CvUnitEntry',
}

classes = sorted(set(re.findall(r'\b(Cv\w+Info)::copyNonDefaults\s*\(', text)))
getter_member = {}
for cls in classes:
    for name, args, body in bodies(cls, r'(?:get|is)\w+'):
        ms = re.findall(r'return\s+\(?\s*(m_\w+)', body)
        if ms: getter_member[(cls, name)] = ms[0]

bad = 0
for cls in classes:
    if only and cls not in only: continue
    read = set()
    for name, args, body in bodies(cls, r'read\w*'):
        if 'CvXMLLoadUtility' in args: read |= members(body)
    copied = set()
    for name, args, body in bodies(cls, r'copyNonDefaults\w*'):
        copied |= members(body)
        for g in re.findall(r'pClassInfo->((?:get|is)\w+)\s*\(', body):
            if (cls, g) in getter_member: copied.add(getter_member[(cls, g)])
    missing = sorted(m for m in read - copied if (cls, m) not in KNOWN)
    if missing:
        bad += 1
        print('%s: %s' % (cls, ', '.join(missing)))
sys.exit(1 if bad else 0)
