# Unsaved state that survives a turn: why a reloaded game diverged

This is a static audit of the source at commit 81ae534, which is patch 0014: GitLab
`main` 005988c. Line numbers refer to that tree.

It answers one question. The game was saved at the start of turn 150, Mediterranean,
seed 7. Writing the loaded state back gave byte-identical data. Why did the reloaded game
still part from the running one during turn 150?

The harness random-number log located the first differing draw:

- `getSorenRandNum(5, "AI Worker build Fort with Priority")` in `CvUnitAI::AI_workerMove`
  (CvUnitAI.cpp:1689).
- The running game drew it.
- The reloaded game returned earlier from the same worker's move without drawing.

The conclusion was confirmed by fixing it (patch 0015). Afterwards the reloaded game
played identically to the running one for 12 turns, and on a second map for 25 turns.

## The worker's path to the roll

Before `AI_workerMove`:

- `CvUnitAI::AI_update` calls `AI_handleSettlerTransport`, `AI_afterAttack` and
  `AI_operationMove`. The last reads `m_aiMilitaryOperations`, which is saved.
- An old move or route mission goes through `groupPathTo` → `generatePath`.

Inside `AI_workerMove`, before the roll:

- `canBuildRoute`, plot owner, `getWorkingCity`, `AI_getWorkersNeeded/Have` (saved).
- `AI_retreatToCity` (plot danger, `generatePath`).
- `AI_load` (area unit-AI counts, exact mission index, `generatePath`).
- `canDefend`, `AI_isPlotThreatened`.
- `isConnectedToCapital` (plot groups, saved).
- `AI_connectPlot`, `AI_improveBonus` (`m_aiBonusValue`, saved).
- `AI_connectCity`, `AI_improveCity` → `AI_bestCityBuild` (saved best builds).
- `AI_improveLocalPlot`.

Every `generatePath` reaches the path callbacks:

- `pathDestValid` calls `AI_getAnyPlotDanger(pToPlot)` (CvGameCoreUtils.cpp:1659).
- `pathValidFrom` calls it for turn-start nodes (:2081).
- Both apply because a worker cannot fight and these searches do not pass
  `MOVE_IGNORE_DANGER`.

`AI_getAnyPlotDanger` (CvPlayerAI.cpp:3665):

- reads the active-player no-danger cache (:3676);
- reads the team border cache (:3687) for ranges of at least `DANGER_RANGE`;
- writes both caches.

## Unsaved members, by class

**`CvPlot`**
- `m_abIsTeamBorderCache` (CvPlot.h:619)
  - Carries across turns. Cleared only by `declareWar`/`makePeace`, by an owner change
    within four plots, and on load.
  - **On the worker path.**
- `m_bIsActivePlayerNoDangerCache`
  - Cleared at the end of every `setTurnActive`, before the autosave, so it holds
    nothing across a save.

**`CvPlayerAI`**
- Found values and settlement candidates (`m_iFoundValuesCacheTurn`,
  `m_aSettlementCandidates`, settle regions)
  - Refreshed every 8 turns unless a settler is active.
  - Reset on read, so a reloaded game recomputes them at once.
  - Not on this path.
- Wellbeing cache
  - Keyed by a generation counter and reset on load.
  - Used only for civic valuation.
- Attitude cache
  - Cleared each turn after patch 0014 and on read.
- Strategic context and operation delivery cache
  - Keyed by turn.

**Others**
- `CvUnitAI`: group-loss counters, per turn only.
- `CvSelectionGroup`: the stranded cache, cleared in every group `doTurn`.
- `CvCityAI`, `CvSelectionGroupAI`, `CvTeamAI`, `CvArea`, `CvMap`: fully saved.

**Static state**
- Mission-target indices: exact, rebuilt on epoch changes.
- Path-reuse owners: keyed by group, epoch, turn and moves; cleared on load and before
  every group update.

## Ranked suspects

1. **`CvPlot::m_abIsTeamBorderCache`** (high).
   - Set at CvPlayerAI.cpp:3719–3722 and :3727–3730; read at :3687.
   - The writes described as "reversible" also set the flag for the enemy team, on the
     querying plot and on the enemy's plot. That is wrong whenever the querying plot is
     unowned or inside a third party's land, and wrong for the distance-2 road rule.
   - The wrong flags stay until a war or peace change or a nearby owner change. In the
     running game they make a non-fighting worker reject destinations and turn-end
     plots, so it falls through to the roll. After a reload the flags are gone, the
     worker finds a job and returns before the roll.
   - **Fixed in patch 0015:** only the queried plot and team are flagged, and the
     flags are cleared each turn.
2. **Found values and settlement candidates** (certain to differ after a reload, but
   not on this path).
   - Recomputed on first use after a load; up to 7 turns old in the running game.
   - Both games refresh at the same moment whenever a settler exists.
3. **Attitude cache entries** filled between the team counters' update and the
   autosave (low).
4. **Wellbeing cache** (low; civic valuation only).

Ruled out for this roll: the no-danger cache, path reuse, mission-target indices, the
stranded cache, the group-loss counters, and everything in `CvCityAI`, `CvArea`,
`CvMap` and `CvTeamAI`.
