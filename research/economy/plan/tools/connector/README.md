# Editing the mod through the GitLab connector

The mod branch (`plan.json` `repositories.mod`) is changed only through the GitLab MCP tools
(`mcp__gitlab__add_commit`). That tool is the connector named `gitlab`. A session notice that the plugin server
`plugin:gitlab:gitlab` needs authentication is about a different server: try `mcp__gitlab__list_commits` first.

## Procedure for large XML edits

1. Clone the branch into the scratchpad (`git clone -b claude/settlement-economy https://gitlab.com/aretemaxxing-group/rise-of-mankind.git`; the scratchpad is lost when the container goes).
2. Write a script that selects the records by rule and applies the edits to a worktree, saving minimal unique
   (old, new) pairs: `lq_f13_targets.py` and `lq_f13_edits.py` are the example (LQ.F13). Edit the base files,
   not a module of partial records, until GW.F7 fixes `copyNonDefaults`.
3. Send the pairs as `update` actions with `old_str`/`new_str`, in batches under about 27 KB of JSON (what one
   tool output can show), in file order: each pair is unique in the file as the earlier pairs leave it.
4. After each commit: `python3 verify.py <checkout> <pairs.json> <base commit> <pairs sent so far>` must print
   `identical` for every file. Record the GitLab commit ids in `plan.json` (task note) and `current`.

## Connector facts

- Files are CRLF: write `\r\n` in the JSON strings. Content with `encoding: base64` is stored as base64 text, not
  decoded: carry binaries in a patch (Tools/GameFontPatch).
- Files the connector edits come back in UTF-8: write non-ASCII as XML character references.
- Commit messages need `Serves: P..` naming registered predictions whose paths cover the files
  (`method/hooks/claude_external.py`).
