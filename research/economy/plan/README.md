# Settlement Economy: the implementation plan

Start every session with `python3 tools/check_plan.py --summary`. The plan holds the task structure, not memory.

| File | What it is | Made by |
|---|---|---|
| `statement.md` | The design statement; the plan implements it and nothing beyond it | the user |
| `plan.json` | Decisions; components in dependency order; per feature: the code it changes (anchors), ordered tasks, the data it adds, the features it comes after, acceptance, checks; invariants | edited with the work |
| `proposals.json` | Proposed unit, category, land kind and need for each existing resource | edited with the work |
| `catalogue.json` | Every resource from the mod XML: placement rules, improvements, givers, uses; the essentials and market chains; storage buildings; buildings that require goods; joined to the proposals | `tools/catalogue.py <checkout>` |
| `callsites.json` | Every call that reads a plot's resource token, with its function and class (what LQ changes, line by line) | `tools/callsites.py <checkout>`; classes edited with the work |
| `status.json` | Features done, broken anchors, the mod commit checked | `tools/check_plan.py <checkout>` |
| `confirmations.json` | In-game confirmations of manual checks, by check id (`LQ.F5.0`) | added when confirmed |

`tools/check_plan.py <checkout>` confirms every anchor in the mod source, runs the checks and audits (icons, font,
catalogue, call sites classified and converted) and writes `status.json`. Exit 1 if the plan is invalid or an anchor
is broken. Regenerate `catalogue.json` and `callsites.json` whenever the mod source changes.
