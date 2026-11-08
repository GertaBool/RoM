"""R75.1 (M125): checks that data/user_inputs_m120.csv holds the user's ODS cell by cell.
1. LibreOffice (headless) converts the ODS independently; every cell is compared with the CSV (notes stripped).
2. Every non-text cell: the text shown must equal the stored value (as % or with its unit).
3. The columns item, unit, needed_for, nuance are compared with the template sent (data/user_inputs_template.csv):
   every edit the user made outside your_value and your_nuance is printed.
usage: python3 research/economy/plan/tools/ods_audit.py <scratch dir>"""
import csv, glob, os, re, subprocess, sys, zipfile, shutil
import xml.etree.ElementTree as ET
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')
S = sys.argv[1]; os.makedirs(S, exist_ok=True)
shutil.copy(os.path.join(DATA, 'user_inputs_m120.ods'), os.path.join(S, 'in.ods'))
subprocess.run(['soffice', '--headless', '--convert-to', 'csv:Text - txt - csv (StarCalc):44,34,76,1,,0,false,true,false,false,false,-1', 'in.ods'], cwd=S, capture_output=True)
lo = [f for f in glob.glob(os.path.join(S, '*.csv'))][0]
def trim(rows):
    for r in rows:
        while r and r[-1] == '': r.pop()
    while rows and not rows[-1]: rows.pop()
    return rows
A = trim(list(csv.reader(open(lo, encoding='utf-8'))))
B = trim([[re.sub(r'\s*\[note: .*\]$', '', c, flags=re.S) for c in r] for r in csv.reader(open(os.path.join(DATA, 'user_inputs_m120.csv'), encoding='utf-8'))])
print('rows', len(A), len(B), '| columns', max(map(len, A)), max(map(len, B)), '| header equal', A[0] == B[0])
NS = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0', 'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
T, O = '{%s}' % NS['table'], '{%s}' % NS['office']
root = ET.fromstring(zipfile.ZipFile(os.path.join(S, 'in.ods')).read('content.xml'))
print('sheets', [t.get(T + 'name') for t in root.iter(T + 'table')], '| annotations', sum(1 for _ in root.iter(O + 'annotation')))
bad, numeric = 0, 0
for i in range(max(len(A), len(B))):
    a = A[i] if i < len(A) else []; b = B[i] if i < len(B) else []
    for j in range(max(len(a), len(b))):
        x = a[j] if j < len(a) else ''; y = b[j] if j < len(b) else ''
        if x == y: continue
        m = re.fullmatch(r'([0-9.]+)(%|kg)?', y)               # shown text vs stored value
        ok = m and abs(float(m.group(1)) / (100 if m.group(2) == '%' else 1) - float(x.rstrip('%')) / (100 if x.endswith('%') else 1)) < 1e-9
        numeric += 1
        if not ok:
            bad += 1; print('DIFF row', i + 1, 'col', j + 1, repr(x), repr(y))
print('cells differing only in number format (shown vs stored, equal values):', numeric - bad, '| real differences:', bad)
Tm = {r['id']: r for r in csv.DictReader(open(os.path.join(DATA, 'user_inputs_template.csv'), encoding='utf-8'))}
Us = {r['id']: r for r in csv.DictReader(open(os.path.join(DATA, 'user_inputs_m120.csv'), encoding='utf-8'))}
print('ids equal', set(Tm) == set(Us))
for i in sorted(Us):
    for c in ('section', 'item', 'unit', 'needed_for', 'nuance'):
        if (Tm[i].get(c) or '') != (Us[i].get(c) or ''):
            print('EDIT', i, c, '|', repr((Tm[i][c] or '')[:90]), '->', repr((Us[i][c] or '')[:90]))
