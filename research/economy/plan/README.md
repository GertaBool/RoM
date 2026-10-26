# Settlement Economy

Start every session with `python3 tools/check_plan.py --summary`. These files hold the work, not memory.

| File | Tracks |
|---|---|
| `statement.md` | The design statement, verbatim |
| `design.json` | The design structure: the statement as elements, each quoting its text; every decision with its source |
| `plan.json` | The implementation: repository and branch (mod work goes to GitLab `claude/settlement-economy`), components, features with the design elements they serve, code anchors, data, order, tasks (todo or done), acceptance, checks |
| `requests.json` | Every prompt verbatim with what it led to; requests split into items with status and location |
| `proposals.json` | Proposed unit, category, land kind and need of every good |
| `catalogue.json` | Generated from the mod XML (`tools/catalogue.py`): resources, origins, building chains |
| `callsites.json` | Generated from the mod source (`tools/callsites.py`): every read of a plot's resource token, classified |
| `status.json` | Written by `tools/check_plan.py <checkout>`: features passing their checks, broken anchors, mod commit and branch |
| `confirmations.json` | In-game confirmations of manual checks |

Commands: `tools/check_plan.py --summary`; `tools/check_plan.py <checkout>`; `tools/check_plan.py task LQ.F1.T1 done`;
`tools/check_plan.py item R1.5 done --where "..."`. A feature is done when all its tasks are done and its checks pass.
