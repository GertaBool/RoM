"""Every field with a set value of every record in Civ4 XML files, flattened to path = value (R15, M60).
A field counts as set unless it is empty, 0, -1, NONE or an empty list; repeated scalar children keep their position as [i]
(yields: 0 food, 1 production, 2 commerce; commerces: 0 gold, 1 research, 2 culture, 3 espionage).
Text keys are resolved to English where a text file of the same folder or the base text folder defines them.
usage: xml_fields.py <out.md> <record tag> <xml file>... [--text <dir>...]"""
import glob, os, re, sys
import xml.etree.ElementTree as ET

args = sys.argv[1:]; texts = []
if '--text' in args:
    i = args.index('--text'); texts = args[i + 1:]; args = args[:i]
out, tag, files = args[0], args[1], args[2:]
TXT = {}
for d in texts:
    for f in glob.glob(os.path.join(d, '**', '*.xml'), recursive=True):
        s = open(f, 'rb').read().decode('latin-1')
        for k, e in re.findall(r'<Tag>([^<]+)</Tag>\s*<English>(.*?)</English>', s, re.S):
            TXT.setdefault(k, re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', e)).strip())

def strip(t): return t.split('}', 1)[-1]
def unset(v): return v in ('', '0', '-1', 'NONE', '0.0', '0.00')

def walk(el, path, rows):
    kids = list(el)
    if not kids:
        v = (el.text or '').strip()
        if not unset(v):
            rows.append((path, v + ('  ("%s")' % TXT[v][:90] if v in TXT else '')))
        return
    tags = [strip(c.tag) for c in kids]
    for i, c in enumerate(kids):
        t = tags[i]
        # a list of scalars (iYield, iCommerce, ...) keeps each value's position: index 0 food, 1 production, ...
        idx = '[%d]' % tags[:i].count(t) if tags.count(t) > 1 and not list(c) else ''
        walk(c, path + '/' + t + idx, rows)

lines = []
for f in files:
    root = ET.fromstring(open(f, 'rb').read())
    recs = [e for e in root.iter() if strip(e.tag) == tag]
    lines.append('## %s (%d %s records)\n' % (os.path.basename(f), len(recs), tag))
    for r in recs:
        rows = []; walk(r, '', rows)
        t = next((v for p, v in rows if p == '/Type'), '?')
        lines.append('### %s\n' % t)
        lines += ['- `%s` = %s' % (p[1:], v) for p, v in rows if p != '/Type']
        lines.append('')
open(out, 'w').write('\n'.join(lines) + '\n')
print(out, sum(1 for l in lines if l.startswith('### ')), 'records', sum(1 for l in lines if l.startswith('- ')), 'fields')
