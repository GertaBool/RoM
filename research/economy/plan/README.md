# Settlement Economy: the implementation plan

- `statement.md`: the design statement. The plan implements it and nothing beyond it.
- `plan.json`: components in dependency order (Geography and tiles, Groundwork, Production, Food and growth,
  Consumption and needs, Storage and distribution, Industry and units, Trade and diplomacy, AI valuation, Interface,
  optional Market prices), each
  with what the player sees, the statement sections it implements, its dependencies and decisions, and features
  that name the code they change and the checks that say when they are done. Decisions record what is decided and
  what is still open; the invariants hold after every component.
- `tools/check_plan.py --summary`: the decisions, the components in order with their progress, the next features and how to resume. Run it first in every session.
- `tools/check_plan.py <mod checkout>`: validates the plan, confirms every code anchor still exists in the mod
  source, evaluates the checks (text the work adds, the icon and font audits, evidence files, in-game confirmations)
  and lists the components that can start. Exit 1 if the plan is invalid or an anchor is broken.
- `status.json`: what the last checker run against a mod checkout found (features done, broken anchors, the commit); `--summary` reads it, so a session without a checkout still knows where the work stands.
- `confirmations.json` (created when needed): in-game confirmations, keyed by check id (`GW.F2.2`, `I3`), each
  `{"date": ..., "note": ...}`.

Work proceeds component by component in dependency order; a component is done when every feature's checks pass.
