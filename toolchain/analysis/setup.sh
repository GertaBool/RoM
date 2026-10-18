#!/bin/bash
# Analysis toolkit: Python packages (pinned) in ~/.cache/rom-ana, and command-line tools.
# Idempotent; run by the SessionStart hook in .claude/settings.json (in the background).
# Tools: research/ai-warfare/tools/{exper,q,divaudit}.py run with ~/.cache/rom-ana/bin/python.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
V=$HOME/.cache/rom-ana
LOG=$HOME/.cache/rom-ana-setup.log
{
  if [ ! -x "$V/bin/python" ]; then python3 -m venv "$V"; fi
  want=$(sha256sum "$HERE/requirements.txt" | cut -d' ' -f1)
  if [ "$(cat "$V/.req-sha" 2>/dev/null)" != "$want" ]; then
    "$V/bin/pip" install -q -r "$HERE/requirements.txt" && echo "$want" > "$V/.req-sha"
  fi
  missing=""
  for t in hyperfine parallel ctags sqlite3; do command -v $t >/dev/null || missing="$missing $t"; done
  if [ -n "$missing" ]; then
    pk=$(echo "$missing" | sed 's/ctags/universal-ctags/')
    apt-get install -y -q $pk >/dev/null 2>&1 || { apt-get update -q >/dev/null 2>&1 && apt-get install -y -q $pk >/dev/null 2>&1; } || true
  fi
  echo "rom-ana ready $(date -u +%FT%TZ)"
} >"$LOG" 2>&1
