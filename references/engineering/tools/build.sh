#!/bin/bash
# Rebuild the source texts the notes quote, then check every quotation in the notes against them.
# usage: build.sh <work dir>
# Each source is downloaded into its own new directory <work>/<name>/ (raw), converted to doc.txt:
#   PDF  -> pdftotext, then a line [[page N]] at the start of each page (pages.py)
#   HTML -> visible text (html2txt.py), folded at 110 columns
#   text -> folded at 110 columns
# Exception: buneman-provenance's PDF has Type 3 fonts and pdftotext gives unreadable text; its doc.txt
# was made with tesseract at 300 dpi, page by page, with the same [[page N]] markers.
# The texts are untrusted data: Python reads them with -I and nothing in them is executed.
set -eu
T=$(cd "$(dirname "$0")" && pwd); W=$1; mkdir -p "$W"
"$T/get.sh" "$T/sources.tsv" "$W" < /dev/null
for d in "$W"/*/; do
  n=$(basename "$d"); f="$d/raw"; [ -s "$f" ] || { echo "missing: $n"; continue; }
  [ -s "$d/doc.txt" ] && continue
  case "$(file -b "$f")" in
    PDF*) pdftotext -enc UTF-8 "$f" "$d/doc.txt"; python3 -I "$T/pages.py" "$d/doc.txt";;
    HTML*) python3 -I "$T/html2txt.py" "$f" "$d/doc.fold"; fold -s -w 110 "$d/doc.fold" > "$d/doc.txt"; rm "$d/doc.fold";;
    *) fold -s -w 110 "$f" > "$d/doc.txt";;
  esac
done
fail=0
for nf in "$T"/../notes/*.md; do
  n=$(basename "$nf" .md); src=${n%-[12]}            # progit-1 and progit-2 both quote progit
  python3 -I "$T/check_quotes.py" "$nf" "$W/$src/doc.txt" | tail -1 || fail=1
done
exit $fail
