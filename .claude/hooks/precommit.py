#!/usr/bin/env python3
"""PreToolUse hook (Bash): before any git commit, run research/ai-warfare/tools/check_all.py.
A failing check blocks the commit (exit 2); its errors go back to Claude on stderr."""
import json, os, re, subprocess, sys

d = json.load(sys.stdin)
cmd = d.get('tool_input', {}).get('command', '')
if not re.search(r'\bgit\b[^\n|;&]*\bcommit\b', cmd):
    sys.exit(0)
root = os.environ.get('CLAUDE_PROJECT_DIR') or d.get('cwd') or '.'
r = subprocess.run([sys.executable, os.path.join(root, 'research/ai-warfare/tools/check_all.py')],
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.stderr.write(r.stdout + r.stderr + '\nCommit blocked: research/ai-warfare/tools/check_all.py failed.\n')
    sys.exit(2)
sys.exit(0)
