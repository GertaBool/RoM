"""R72 (M120): read an OpenDocument spreadsheet (.ods) with the standard library only, every sheet as rows of cell text,
and write each sheet as CSV. Repeated cells and rows are expanded; trailing empty cells and rows are dropped.
Cell text keeps line breaks within a cell as '\\n'; a cell's annotation (comment) is appended after ' [note: ...]'.

usage: ods_read.py <file.ods> <out_dir>
"""
import csv
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
      'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
T = '{%s}' % NS['table']


def text_of(el):
    """All text of an element, text:s spaces and text:line-break included."""
    out = []

    def walk(e):
        tag = e.tag.split('}')[1]
        if tag == 's':
            out.append(' ' * int(e.get('{%s}c' % NS['text'], 1)))
        elif tag == 'line-break':
            out.append('\n')
        elif tag == 'tab':
            out.append('\t')
        if e.text and tag not in ('s',):
            out.append(e.text)
        for c in e:
            if c.tag.split('}')[1] == 'annotation':
                continue
            walk(c)
            if c.tail:
                out.append(c.tail)
    walk(el)
    return ''.join(out)


def cell_text(c):
    paras = [text_of(p) for p in c.findall('text:p', NS)]
    s = '\n'.join(paras)
    if not s:
        v = c.get('{%s}value' % NS['office']) or c.get('{%s}date-value' % NS['office']) or c.get('{%s}boolean-value' % NS['office'])
        s = v or ''
    note = c.find('office:annotation', NS)
    if note is not None:
        nt = '\n'.join(text_of(p) for p in note.findall('text:p', NS)).strip()
        if nt:
            s = (s + ' [note: %s]' % nt) if s else '[note: %s]' % nt
    return s


def read(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('content.xml'))
    sheets = {}
    for t in root.iter(T + 'table'):
        rows = []
        for r in t.iter(T + 'table-row'):
            cells = []
            for c in r:
                if c.tag not in (T + 'table-cell', T + 'covered-table-cell'):
                    continue
                n = int(c.get(T + 'number-columns-repeated', 1))
                cells += [cell_text(c)] * min(n, 1000)
            while cells and cells[-1] == '':
                cells.pop()
            rn = int(r.get(T + 'number-rows-repeated', 1))
            rows += [cells] * min(rn, 10000 if cells else 1)
        while rows and not rows[-1]:
            rows.pop()
        sheets[t.get(T + 'name')] = rows
    return sheets


def main():
    path, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for name, rows in read(path).items():
        fn = os.path.join(out, name.replace('/', '_') + '.csv')
        with open(fn, 'w', newline='', encoding='utf-8') as fh:
            csv.writer(fh).writerows(rows)
        print(fn, len(rows), 'rows', max((len(r) for r in rows), default=0), 'columns')


if __name__ == '__main__':
    main()
