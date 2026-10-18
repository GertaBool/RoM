#!/usr/bin/env python3
"""Claude Code PreToolUse hook for commits made in another repository through a connector (the
GitLab connector's add_commit). Such a commit never passes this repository's git hooks, so it is
checked here, before it is made: its message must carry "Serves: P.." for open predictions without
evidence, on lines neither degenerating nor stalled, whose paths name every file it touches (as
config.json "external_prefix" + path). A failure blocks the call (exit 2)."""
import json, os, sys

d = json.load(sys.stdin)
ti = d.get('tool_input', {})
files = []
for a in ti.get('actions') or []:
    for k in ('file_path', 'previous_path'):
        if a.get(k): files.append(a[k])
root = os.environ.get('CLAUDE_PROJECT_DIR') or d.get('cwd') or '.'
sys.path.insert(0, os.path.join(root, 'method'))
import ledger  # noqa: E402

errs = ledger.external(root, ti.get('commit_message', ''), sorted(set(files)))
if errs:
    sys.stderr.write('External commit blocked by method/ledger.py:\n' + '\n'.join(errs) + '\n')
    sys.exit(2)
sys.exit(0)
