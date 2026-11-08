"""R76.1 (M126): lossless extraction of an OpenDocument spreadsheet, checked against an independent reader.

For every cell of every sheet it records: sheet, row, column, header name, the text shown, the stored value and its
type (string, float, percentage, currency, date, time, boolean), the number format (pattern and suffix text, read
from the data style), a formula if any, and the note. It writes two files next to the output stem:
  <stem>.cells.csv   one line per non-empty cell (the lossless record)
  <stem>.csv         the sheet as shown, one line per row (what a person sees)
Checks, each of which stops the run when it fails (nothing is written):
  - features this tool does not translate: formulas, merged or covered cells, hidden rows or columns, more than one
    sheet, rich-text runs, links, images;
  - for every number cell, the shown text must equal the stored value rendered with its own format;
  - LibreOffice (headless) converts the file twice, once as shown and once as stored values; both must equal this
    tool's output cell by cell.
usage: ods_extract.py <file.ods> <out stem> <scratch dir>
"""
import csv
from decimal import Decimal
import os
import re
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
      'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0', 'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
      'number': 'urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0', 'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'}
T, O, X, S_, N_ = ('{%s}' % NS[k] for k in ('table', 'office', 'text', 'style', 'number'))
FAIL = []


def stop(msg):
    FAIL.append(msg)


def text_of(el):
    out = []

    def walk(e):
        tag = e.tag.split('}')[1]
        if tag == 's':
            out.append(' ' * int(e.get(X + 'c', 1)))
        elif tag == 'line-break':
            out.append('\n')
        elif tag == 'tab':
            out.append('\t')
        elif tag in ('span', 'a'):
            stop('rich text or link in a cell (%s)' % tag)
        if e.text and tag != 's':
            out.append(e.text)
        for c in e:
            if c.tag.split('}')[1] == 'annotation':
                continue
            walk(c)
            if c.tail:
                out.append(c.tail)
    walk(el)
    return ''.join(out)


def data_styles(z):
    """cell style name -> (data style name, pattern): decimals, percent, suffix text."""
    fmt, cell = {}, {}
    for part in ('styles.xml', 'content.xml'):
        root = ET.fromstring(z.read(part))
        for ds in root.iter():
            tag = ds.tag.split('}')[1]
            if tag in ('number-style', 'percentage-style', 'currency-style', 'date-style', 'time-style', 'boolean-style', 'text-style'):
                name = ds.get(S_ + 'name')
                num = ds.find('number:number', NS)
                dec = int(num.get(N_ + 'decimal-places')) if num is not None and num.get(N_ + 'decimal-places') is not None else None
                minint = int(num.get(N_ + 'min-integer-digits', 1)) if num is not None else None
                texts = [t.text or '' for t in ds.findall('number:text', NS)]
                fmt[name] = {'kind': tag, 'decimals': dec, 'min_int': minint, 'grouping': num is not None and num.get(N_ + 'grouping') == 'true',
                             'text': ''.join(texts)}
        for st in root.iter(S_ + 'style'):
            if st.get(S_ + 'family') == 'table-cell' and st.get(S_ + 'data-style-name'):
                cell[st.get(S_ + 'name')] = st.get(S_ + 'data-style-name')
    return fmt, cell


def dec(d):
    """A Decimal written without exponent or trailing zeros (exact: no binary floating point)."""
    s = format(d, 'f')
    return s.rstrip('0').rstrip('.') if '.' in s else s


def render(value, f):
    """The stored number written with its data style, as LibreOffice shows it (exact decimal arithmetic)."""
    v = Decimal(value)
    if f is not None and f['kind'] == 'percentage-style':
        v *= 100
    if f is None or f['decimals'] is None:
        return dec(v) + ('' if f is None else f['text'])
    return format(v.quantize(Decimal(1).scaleb(-f['decimals'])), 'f') + f['text']


def read(path):
    z = zipfile.ZipFile(path)
    names = z.namelist()
    if any(n.startswith('Pictures/') or n.startswith('Objects') for n in names):
        stop('images or embedded objects in the file')
    fmt, cellstyle = data_styles(z)
    root = ET.fromstring(z.read('content.xml'))
    tables = list(root.iter(T + 'table'))
    if len(tables) != 1:
        stop('%d sheets (this tool translates one)' % len(tables))
    for col in root.iter(T + 'table-column'):
        if col.get(T + 'visibility', 'visible') != 'visible':
            stop('hidden column')
    cells, grid = [], []
    t = tables[0]
    colstyles = []
    for col in t.iter(T + 'table-column'):
        colstyles += [col.get(T + 'default-cell-style-name')] * min(int(col.get(T + 'number-columns-repeated', 1)), 1024)
    r = 0
    for row in t.iter(T + 'table-row'):
        if row.get(T + 'visibility', 'visible') != 'visible':
            stop('hidden row %d' % (r + 1))
        rep = int(row.get(T + 'number-rows-repeated', 1))
        line, c = [], 0
        for cell in row:
            tag = cell.tag.split('}')[1]
            if tag == 'covered-table-cell' or cell.get(T + 'number-columns-spanned') or cell.get(T + 'number-rows-spanned'):
                stop('merged or covered cell at row %d' % (r + 1))
            if tag != 'table-cell':
                continue
            n = int(cell.get(T + 'number-columns-repeated', 1))
            if cell.get(T + 'formula'):
                stop('formula at row %d col %d' % (r + 1, c + 1))
            shown = '\n'.join(text_of(p) for p in cell.findall('text:p', NS))
            vt = cell.get(O + 'value-type') or ('string' if shown else '')
            val = cell.get(O + 'value') or cell.get(O + 'date-value') or cell.get(O + 'time-value') or cell.get(O + 'boolean-value') or ''
            st = cell.get(T + 'style-name') or (colstyles[c] if c < len(colstyles) else None)
            dsn = cellstyle.get(st)
            f = fmt.get(dsn)
            note = cell.find('office:annotation', NS)
            nt = '\n'.join(text_of(p) for p in note.findall('text:p', NS)) if note is not None else ''
            for k in range(min(n, 1024)):
                if shown or val or nt:
                    cells.append({'row': r + 1, 'col': c + 1, 'shown': shown, 'type': vt, 'value': val, 'format': dsn or '',
                                  'format_text': (f or {}).get('text', ''), 'decimals': '' if not f or f['decimals'] is None else f['decimals'], 'note': nt})
                    if vt in ('float', 'percentage', 'currency'):
                        exp = render(val, f)
                        if exp != shown:
                            stop('row %d col %d: shown %r but stored %s renders as %r' % (r + 1, c + 1, shown, val, exp))
                line.append(shown)
                c += 1
        while line and line[-1] == '':
            line.pop()
        for k in range(min(rep, 1 if not line else rep)):
            grid.append(list(line))
            r += 1
        if not line and rep > 1:
            r += rep - 1
    while grid and not grid[-1]:
        grid.pop()
    return cells, grid


def libreoffice(path, scratch, as_shown):
    d = os.path.join(scratch, 'shown' if as_shown else 'stored')
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    shutil.copy(path, os.path.join(d, 'in.ods'))
    opt = 'csv:Text - txt - csv (StarCalc):44,34,76,1,,0,false,true,%s,false,false,-1' % ('true' if as_shown else 'false')
    subprocess.run(['soffice', '--headless', '--convert-to', opt, 'in.ods'], cwd=d, capture_output=True, check=True)
    out = [f for f in os.listdir(d) if f.endswith('.csv')]
    rows = list(csv.reader(open(os.path.join(d, out[0]), encoding='utf-8')))
    for row in rows:
        while row and row[-1] == '':
            row.pop()
    while rows and not rows[-1]:
        rows.pop()
    return rows


def main():
    path, stem, scratch = sys.argv[1], sys.argv[2], sys.argv[3]
    cells, grid = read(path)
    header = grid[0]
    shown_lo, stored_lo = libreoffice(path, scratch, True), libreoffice(path, scratch, False)
    if shown_lo != grid:
        for i in range(max(len(grid), len(shown_lo))):
            a = grid[i] if i < len(grid) else None
            b = shown_lo[i] if i < len(shown_lo) else None
            if a != b:
                stop('as shown, row %d differs from LibreOffice: %r / %r' % (i + 1, a, b))
                break
    stored = {(c['row'], c['col']): c for c in cells}
    for i, row in enumerate(stored_lo):
        for j, v in enumerate(row):
            c = stored.get((i + 1, j + 1))
            mine = '' if c is None else (c['shown'] if c['type'] == 'string' else
                                         (dec(Decimal(c['value']) * 100) + '%' if c['type'] == 'percentage' else dec(Decimal(c['value']))))
            if mine != v:
                stop('stored value row %d col %d: %r here, %r in LibreOffice' % (i + 1, j + 1, mine, v))
    if FAIL:
        print('STOPPED:\n  ' + '\n  '.join(FAIL))
        sys.exit(1)
    with open(stem + '.cells.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['row', 'col', 'column', 'shown', 'type', 'value', 'format', 'format_text', 'decimals', 'note'])
        w.writeheader()
        for c in cells:
            w.writerow(dict(c, column=header[c['col'] - 1] if c['col'] - 1 < len(header) else ''))
    with open(stem + '.csv', 'w', newline='', encoding='utf-8') as fh:
        csv.writer(fh).writerows(grid)
    types = {}
    for c in cells:
        types[c['type']] = types.get(c['type'], 0) + 1
    print('%d rows, %d columns, %d non-empty cells %s; matches LibreOffice as shown and as stored' % (
        len(grid), max(map(len, grid)), len(cells), types))


if __name__ == '__main__':
    main()
