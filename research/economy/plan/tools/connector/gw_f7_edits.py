"""GW.F7.T1/T2 (and the other classes copy_audit.py lists): copyNonDefaults copies every member the XML read sets.
For each class and member the audit reports, a line before the end of X::copyNonDefaults:
    if (m_x == <constructor default>) m_x = pClassInfo->m_x;
the rule the other members already follow (a module record leaves a field at its default to inherit it).
The default is read from the class's constructor initialiser list.
usage: gw_f7_edits.py <mod checkout> <pairs.json out>"""
import json, os, re, subprocess, sys

mod, out = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
f = 'Assets/CvGameCoreDLL/CvInfos.cpp'
p = os.path.join(mod, f)
audit = subprocess.run([sys.executable, os.path.join(HERE, '..', 'copy_audit.py'), os.path.dirname(p)], capture_output=True, text=True).stdout
missing = {cls: [m.strip() for m in ms.split(',')] for cls, ms in (l.split(': ', 1) for l in audit.splitlines() if ': ' in l)}
s = open(p, 'rb').read().decode('latin-1'); nl = '\r\n' if '\r\n' in s else '\n'

def body_span(cls, fn):
    m = re.search(r'^void\s+%s::%s\s*\([^)]*\)\s*\{' % (cls, fn), s, re.M)
    i, depth = m.end(), 1
    while depth:
        depth += {'{': 1, '}': -1}.get(s[i], 0); i += 1
    return m.start(), i   # i is just past the closing brace

def default(cls, member):
    m = re.search(r'^%s::%s\(\)\s*:(.*?)\{' % (cls, cls), s, re.M | re.S)
    d = re.search(r'\b%s\(([^)]*)\)' % member, m.group(1))
    return d.group(1).strip()

pairs = []
for cls in sorted(missing):
    a, b = body_span(cls, 'copyNonDefaults')
    close = s.rindex('}', a, b)
    lines = ['\t// GW.F7: members the XML read sets that this copy did not carry (research/economy/plan/tools/copy_audit.py)']
    for m in missing[cls]:
        lines.append('\tif (%s == %s) %s = pClassInfo->%s;' % (m, default(cls, m), m, m))
    # anchor: the last line before the closing brace, through the brace, unique in the file
    k = s.rfind(nl, a, close - len(nl)) ; k = s.rfind(nl, a, k) + len(nl)
    old = s[k:close + 1]
    while s.count(old) != 1:
        k = s.rfind(nl, a, k - len(nl)) + len(nl); old = s[k:close + 1]
    new = s[k:close] + nl.join(lines) + nl + '}'
    pairs.append({'file': f, 'old': old, 'new': new})
    s = s[:k] + new + s[close + 1:]
open(p, 'wb').write(s.encode('latin-1'))
json.dump(pairs, open(out, 'w'), indent=0)
print(len(pairs), 'pairs;', sum(len(v) for v in missing.values()), 'members')
