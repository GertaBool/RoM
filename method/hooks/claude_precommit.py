#!/usr/bin/env python3
"""Claude Code PreToolUse hook (Bash): before any git commit command, run method/check_all.py.
A failing check blocks the command (exit 2); its errors go back to Claude on stderr. It works
even where the git hooks are not enabled, and whatever flags the commit carries (--no-verify).
The match is deliberately broad (any command with "git" and then "commit" on one line), so it
can also stop a command that only mentions them; it then blocks only if the checks fail."""
import json, os, re, subprocess, sys

d = json.load(sys.stdin)
cmd = d.get('tool_input', {}).get('command', '')
if not re.search(r'\bgit\b[^\n|;&]*\bcommit\b', cmd):
    sys.exit(0)
root = os.environ.get('CLAUDE_PROJECT_DIR') or d.get('cwd') or '.'
r = subprocess.run([sys.executable, os.path.join(root, 'method/check_all.py')], capture_output=True, text=True)
if r.returncode != 0:
    sys.stderr.write(r.stdout + r.stderr + '\nCommit blocked: method/check_all.py failed.\n')
    sys.exit(2)
sys.exit(0)
