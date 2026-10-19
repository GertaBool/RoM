# CyPlayer.h

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **18** `CyPlayer::operator=(const CyPlayer &)`
  - called by (1): CyGlobalContext::getCyPlayer
- **23** `CyPlayer::getPlayer()`
- **24** `CyPlayer::isNone()` (Python: isNone)
  - called by (1): CyPlayerPythonInterface1
- **492** `CyPlayer::setGoldPerTurnByPlayer(int, int)` (declared, not defined in the source)
