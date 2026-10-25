"""check_quotes.py <notes.md> <doc.txt>: every quotation in the notes must occur in the source text.

A quotation is text between straight double quotes on one line, or between curly double quotes.
Omissions inside a quotation are written ' ... ' (or an ellipsis character); each fragment is checked.
Comparison ignores case, whitespace, punctuation and hyphens (line breaks and hyphenation in the
extracted text), so the words and their order must match exactly. Fragments under 4 words are
reported as too short to verify. When the bullet names pages ('p. 7' or 'pp. 7-8'), the quotation
must occur on those pages (or straddle onto the next page).
Exit 1 if any quotation is not found."""
import re, sys, unicodedata

def key(s):
    s = unicodedata.normalize('NFKC', s).lower()
    return re.sub(r'[\W_]+', '', s)

notes, doc = sys.argv[1], sys.argv[2]
text = open(doc, encoding='utf-8', errors='replace').read()
pages = {}
for m in re.finditer(r'\[\[page (\d+)\]\]\n(.*?)(?=\[\[page \d+\]\]|\Z)', text, re.S):
    pages[int(m.group(1))] = key(m.group(2))
whole = key(re.sub(r'\[\[page \d+\]\]', '', text))
bad = short = ok = 0
for ln, line in enumerate(open(notes, encoding='utf-8'), 1):
    quotes = re.findall(r'"([^"]+)"', line) + re.findall(r'“([^”]+)”', line)
    pm = re.search(r'\bpp?\.\s*(\d+)(?:\s*[-–]\s*(\d+))?', line)
    for q in quotes:
        for frag in re.split(r'\s*(?:\.\.\.|…)\s*', q):
            if not frag.strip(): continue
            if len(frag.split()) < 4:
                short += 1; continue
            k = key(frag)
            if k not in whole:
                bad += 1; print(f'{notes}:{ln}: not in source: "{frag}"'); continue
            if pm and pages:
                a = int(pm.group(1)); b = int(pm.group(2) or a)
                span = ''.join(pages.get(p, '') for p in range(a, b + 2))
                if k not in span:
                    bad += 1; found = [p for p, t in pages.items() if k in t]
                    print(f'{notes}:{ln}: not on p. {a}{"-"+str(b) if b != a else ""} (found on p. {found}): "{frag[:60]}"'); continue
            ok += 1
print(f'{notes}: {ok} quotations verified, {bad} not found, {short} fragments too short to verify')
sys.exit(1 if bad else 0)
