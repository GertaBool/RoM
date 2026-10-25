# Working rules for this repository

The mission is in `method/docs/mission.md`. The method for analysing a game, and for
every AI change built from one, is in `method/docs/data-protocol.md`. Read both before
starting.

Hard rules (details in the protocol):
1. **Questions first,** each with its source. Build a tool only when no source answers a
   question. Do not rebuild the DLL for an analysis.
2. **Setup first:** scenario, options, players, starts. Then the whole game. Then the human.
3. **Describe before inferring.** No reasons in descriptions. Readings come separately, with
   the facts they rest on and what would contradict them.
4. **Effects from the XML records only,** looked up at the time of writing. Never from
   memory, notes or a context summary.
5. **Turns:** every figure carries its turn. Never use the save's state for an earlier turn.
6. **Fresh starts:** when told to start over, replace the old text; do not patch it.
7. **Work through to the end without mid-way questions.** Mark unknowns *open*. Deliver once.
8. **Figures only through the figure system.**
   - Every number in an analysis document comes from a registry written by
     `method/figlib.py`. A registry refuses a figure without a unit (from `figlib.UNITS`), an
     actor, a turn and a source, and refuses a table that drops values without a reason.
   - Documents are templates (`.md.in`) rendered by `method/docs.py`, which rejects typed
     numbers and requires the XML effects of every type a table counts.
   - `method/check_all.py` runs before every commit (`.claude/settings.json`;
     `method/hooks/pre-commit`, enabled by `sh method/setup.sh`). A failure
     blocks the commit.
   - Documents written before the system are listed in the `UNCHECKED` file of their folder. That
     list may only shrink.
9. **Evidence in proportion to the claim** (`method/docs/framework.md`, section 7).
   - An effect that follows from the code or a formula is computed, or shown by one deterministic run, not simulated.
   - A safety claim (no crash, not slower) gets `5` seeded runs per arm (`"test": "safety"`), decided by
     counting: a run that fails only with the change, or a median same-seed slowdown above 5 %, refutes it.
   - A claim that play gets better gets at least `30` independent seeded runs per arm (`HARNESS_RESEED`),
     tested with Welch's test on ranks against the best existing version, and judged against fixed
     opponents, never by self-play alone. Fewer runs give an anecdote, not a result.
10. **Changes are gated by predictions** (`method/ledger.py`, run by `method/check_all.py` and
    the `commit-msg` hook). A commit to code, tools, builds or patches carries `Serves: P..` naming a
    registered prediction (`method/mission/register.json`, append-only) on an essential
    variable, made before its evidence; changes to the checks carry `Method: <reason>`.

Everything the checks and the gate need is in `method/` (see `method/README.md`); a new session or
clone enables it with `sh method/setup.sh` (the SessionStart hook runs it).
