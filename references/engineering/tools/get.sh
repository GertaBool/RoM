#!/bin/bash
# get.sh <sources.tsv> <dest>: each source into its own new directory dest/<name>/, raw file only
dest=$2
while IFS=$'\t' read -r name url; do
  d="$dest/$name"; [ -s "$d/raw" ] && continue
  mkdir -p "$d"
  curl -sSL --max-time 120 -A 'Mozilla/5.0 (X11; Linux x86_64) research-reader' -o "$d/raw" "$url" 2>"$d/curl.err"
  printf '%s\t%s\t%s\t%s\n' "$name" "$(stat -c %s "$d/raw" 2>/dev/null || echo 0)" "$(file -b "$d/raw" | cut -c1-40)" "$url"
done < "$1"
