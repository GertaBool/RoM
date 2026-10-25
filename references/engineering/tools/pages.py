"""pages.py <doc.txt>: insert a line [[page N]] at the start of every page (pdftotext marks page ends with form feeds)."""
import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', errors='replace').read()
if '[[page 1]]' not in t and '\f' in t:
    parts = t.split('\f')
    open(p, 'w', encoding='utf-8').write(''.join(f'[[page {i+1}]]\n{x}' + ('\n' if not x.endswith('\n') else '') for i, x in enumerate(parts) if x.strip() or i < len(parts) - 1))
