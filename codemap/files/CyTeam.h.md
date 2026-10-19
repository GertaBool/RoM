# CyTeam.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **13** `CyTeam::operator=(const CyTeam &)`
  - called by (1): CyGlobalContext::getCyTeam
- **18** `CyTeam::getTeam()`
- **20** `CyTeam::isNone()` (Python: isNone)
  - called by (1): CyTeamPythonInterface
