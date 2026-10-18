#!/usr/bin/env python3
"""Claude Code PreToolUse hook (Bash), before any git commit command:

1. run method/check_all.py; a failure blocks the command (exit 2), its errors go back to Claude;
2. if the commit would change method files (method/config.json "method") or add entries to the
   register or the late links, ask the human to confirm (permissionDecision "ask"), with what
   changes listed. These are the judgments the gate cannot compute: whether a prediction is new
   and its paths fit, whether a hypothesis is a new core, whether a method change is sound.

It works where the git hooks are not enabled, and whatever flags the commit carries (--no-verify).
The match is deliberately broad (any command with "git" and then "commit" on one line), so it can
also stop a command that only mentions them; it then blocks only if the checks fail. Files staged
by the same command (git add ... && git commit) are seen too: the working tree is compared with HEAD.
"""
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

git = lambda *a: subprocess.run(['git', '-C', root] + list(a), capture_output=True, text=True).stdout
changed = sorted({f for f in (git('diff', '--name-only', 'HEAD') + git('ls-files', '--others', '--exclude-standard')).split('\n') if f})
sys.path.insert(0, os.path.join(root, 'method'))
import ledger  # noqa: E402

method = [f for f in changed if ledger.kind_of(f) == 'method']
added = []
for name in ('register.json', 'late-links.json'):
    now = ledger.load(root, f'{ledger.M}/{name}') or []
    before = ledger.load_any(root, name, 'HEAD') or []
    for e in now[len(before):]:
        what = e.get('id') or e.get('commit', '')[:10]
        text = e.get('text') or e.get('reason') or json.dumps(e.get('claim', {}), sort_keys=True)[:160]
        added.append(f'{name} {what} ({e.get("type", "late link")}): {text}')
if method or added:
    parts = []
    if method: parts.append('method files: ' + ', '.join(method[:8]) + (' ...' if len(method) > 8 else ''))
    if added: parts.append('new entries: ' + ' | '.join(added[:6]) + (' ...' if len(added) > 6 else ''))
    print(json.dumps({'hookSpecificOutput': {
        'hookEventName': 'PreToolUse', 'permissionDecision': 'ask',
        'permissionDecisionReason': 'The checks pass. This commit needs your judgment, which the gate cannot compute: '
                                    + '; '.join(parts)}}))
sys.exit(0)
