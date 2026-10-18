# method/: checks, figure system and prediction gate

Everything that decides whether a commit may go in lives here. It needs only `git` and `python3`.

| Path | What it does |
|---|---|
| `setup.sh` | Enables the method in a clone: git hooks, self-tests, ledger check. Safe to rerun |
| `config.json` | Paths and limits: what is gated, what counts as method, the document roots, the stall and depth limits, the minimum runs |
| `check_all.py` | Every check before a commit: figure-system self-test, every template renders and matches, registries reproduce, `UNCHECKED` lists only shrink, the ledger self-test and check, the statistics self-test |
| `figlib.py`, `docs.py` | The figure system: registries refuse figures without unit, actor, turn and source; templates may not type numbers |
| `ledger.py` | The prediction register, evaluator and commit gate (rules in its docstring) |
| `variables.py` | This project's essential variables, as hashed functions (war logs, harness runs) |
| `stats.py`, `exper.py` | The rank-based Welch test in pure Python (checked against SciPy where installed), and its command line |
| `hooks/` | `pre-commit` (all checks), `commit-msg` (the gate), `claude_precommit.py` (the Claude Code Bash hook) |
| `mission/` | `register.json`, `variables.json`, `late-links.json` (all append-only) and `evidence/<P>/` |
| `docs/` | The framework (`framework.md.in`), the analysis protocol and the mission |

Old paths under `research/ai-warfare/tools/` forward here, so analysis tools, recorded registry
commands and old command lines keep working.

## In a new session or clone

`sh method/setup.sh`. The SessionStart hook in `.claude/settings.json` runs it, and the PreToolUse
hook runs `check_all.py` before any `git commit` the session issues, whatever its flags. The analysis
toolkit (`toolchain/analysis/setup.sh`) is separate: `check_all.py` uses it only to reproduce
registries whose inputs exist on the machine.

## Working with the gate

1. **Register before you build.** Append a prediction to `mission/register.json`: its `line`, the
   `hypotheses` it rests on, the `variable` (from `mission/variables.json`), the `evidence` kind,
   the `claim` and the `change`. A runs claim gives `direction` (`a<b` or `a>b`), `alpha`,
   `min_effect` (Vargha-Delaney A), `min_n` and `seat`. A games claim gives `turn`, `handicap`,
   `requires_snapshot`, `op`, `reference` (`[game, war log sha256, value]`) and `min_n`. A prediction
   on a non-essential variable names the prediction it `serves`.
2. **Commit with a trailer.** `Serves: P7` for code, tools, builds, patches or evidence;
   `Method: <reason>` for anything in `method/`, `.claude/` or the forwarders. A build's
   `provenance.json` lists `"serves"`.
3. **Collect evidence with the prediction's seeds.** `ledger.py seeds P7 40` prints them; run the
   harness with `HARNESS_RESEED=<seed>` into directories named `s<seed>`, then
   `ledger.py collect P7 a <seat> <dirs>` (and `b` for the baseline). For a logged game:
   `ledger.py game P7 <WarLog.log> <name>`. Commit the evidence with `Serves: P7`.
4. **Read the ledger.** `ledger.py evaluate` writes `mission/ledger.json`, a dated report. Gate
   decisions never read it; they evaluate live.
5. **Withdraw, do not edit.** Append `{"id": "W1", "type": "withdrawal", "of": "P7", "reason": ...}`.
   After evidence exists, a withdrawal counts as not corroborated.
6. **A missed trailer** is linked in `mission/late-links.json` (commit, what it served, why), never
   repaired by rewriting history. The ledger counts late links.

## Edge cases it handles

- **Evidence before the claim:** run seeds come from the SHA-256 of the prediction's own text.
- **Tuning on the test:** once evidence exists, only evidence commits may serve the prediction.
- **Changing the question:** registered entries are append-only; a variable's code is hashed.
- **Switching the gate off:** a deleted register is an error; a bypassed hook is caught by the
  history audit at the next check; a moved register is followed through its earlier directories
  (`legacy_register_dirs`).
- **Detours:** a non-essential variable needs a chain to an essential one within `max_depth`; a
  line with `stall_commits` code commits since its last decision accepts only evidence.
- **Degeneration:** two failed predictions in a row block a line until evidence or a new line.
- **Old or unfit games:** a game counts only if logged from turn 0 to the claim's turn, at its
  handicap, with turn-start lines when required, and not as one of its references. Logs are
  hashed, not the databases rebuilt from them.
- **A stale ledger:** a committed ledger would change the history it summarises, so the gate never
  reads it.

## Limits

- It checks that a commit cites an open prediction, not that the work serves it. The links are
  visible in the commit log for review.
- `Method:` commits can change the checks themselves; they are visible, not preventable.
- Commits made outside this repository (the GitLab connector) are seen only through the builds
  they produce.
- The war log does not name the DLL that wrote it, so a game cannot yet be tied to one build.

## In another project

Copy `method/`, edit `config.json` (gated and method paths, document roots, analysis Python),
replace `variables.py` with that project's variables, start with empty files in `mission/`, add the
two hooks of `.claude/settings.json`, and run `sh method/setup.sh`.
