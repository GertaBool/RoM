# Settlement Economy: the implementation plan

- `statement.md`: the design statement. The plan implements it and nothing beyond it.
- `plan.json`: components (Groundwork, Land qualities, Production, Food and growth, Consumption and needs, Storage
  and distribution, Industry and units, Trade and diplomacy, AI valuation, Interface, optional Market prices), each
  with what the player sees, the statement sections it implements, its dependencies and decisions, and features
  that name the code they change and the checks that say when they are done. Decisions record what is decided and
  what is still open; the invariants hold after every component.
- `tools/check_plan.py <mod checkout>`: validates the plan, confirms every code anchor still exists in the mod
  source, evaluates the checks (text the work adds, the icon and font audits, evidence files, in-game confirmations)
  and lists the components that can start. Exit 1 if the plan is invalid or an anchor is broken.
- `confirmations.json` (created when needed): in-game confirmations, keyed by check id (`GW.F2.2`, `I3`), each
  `{"date": ..., "note": ...}`.

Work proceeds component by component in dependency order; a component is done when every feature's checks pass.
