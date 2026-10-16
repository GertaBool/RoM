# AI hot loops in the RoM DLL: path searches and other per-turn work

Source: `/home/user/src/rom-upstream/Assets/CvGameCoreDLL` (read only). All file:line
references are to that tree unless a path says otherwise. Profile: turn-400 Marathon
snapshot, Mediterranean (64 x 44 = 2,816 plots, no wrap), 342 cities, about 1,800
units, 3 AI turns, 20.48 s in `CvGame::update`.

## 0. Summary

- Path finding is 55 % of the turn: 29,654 `generatePath` calls, 11.25 s inclusive.
  Over the 3 turns that is 1.83 million node expansions, which is the
  "pathValid move through" count: the memo misses once per expanded parent. An average
  search expands 62 nodes. Per search: 428 `pathValid`, 296 `pathCost` and 77
  `pathAdd` calls. Everything included, one expansion costs 6.1 us.
- No candidate loop in the unit AI sorts its candidates or uses a lower bound, except
  `AI_explore`, `AI_exploreRange` and `AI_loadForCoastalAttack`. Every other loop runs
  a full, unbounded search per candidate. It then rejects the result with
  `iPathTurns <= N`, or divides a value by the turns.
- The DLL already has an admissible lower bound on path turns:
  `CvUnitAI::AI_minPathStepsPerTurn` / `AI_minPathTurns` (CvUnitAI.cpp:134-191).
  Only the explore functions use it.
- **Prototype result (coordinator, same 3 turns).** A global turn limit in `pathValid`
  rejects expansion from a parent whose `m_iData2` exceeds the limit. Reuse is off for
  bounded searches, and the owner is invalidated afterwards. It is applied only in
  `AI_guardCity`, with limit = `iMaxPath`.
  - `AI_guardCity`: 3,868 -> 1,267 ms inclusive, same 2,898 calls.
  - Whole update: 20.48 -> 18.44 s (-10.0 %).
  - The game diverges. Section 2.3 explains why, and how to get a variant whose
    decisions are identical.
- **getBestRoute.** Pre-sorting route builds saved only 270 ms because sorting does
  not cut the expensive calls. `CvPlayer::canBuild` runs the plot check
  (`CvPlot::canBuild`, which includes 9-plot bonus-connectivity tests) *before* the
  tech check (CvPlayer.cpp:7836 vs 7841). So every route build ranked above the plot's
  current route is still plot-checked, even when the team lacks the tech for it. That
  is most of them in a medieval-era game. 444,219 calls x up to 8 non-current route
  builds = up to 3.55 M of the 3.80 M `canBuild` calls. Section 5.1 gives the fix:
  check tech first, and hoist the call out of the yield loops.

### 0.1 Measurement caveat: the harness FAStar is not the game's

The profile was taken in the headless harness. There `FAStar` is the harness's own A*,
in `/home/user/RoM/toolchain/harness/engine.cpp:91-279`, not the game executable's.

- `reset()` clears all 2,816 nodes on every fresh, non-reused search (engine.cpp:120-131).
- `popBest()` is a linear scan of the open list (engine.cpp:166-179).
- On reuse with a new destination it rescores the heuristic of every open node
  (engine.cpp:218-222).
- When a cheaper route reaches a closed node, it pushes the improvement down that
  node's subtree (engine.cpp:148-165, 257-272).

So the 3.40 s *self* time of `generatePath` (30 % of path time) is harness overhead.
Fewer fresh searches save reset time in the harness that the real engine may not
spend, or may spend differently. What transfers to the real game is the number of
callback calls (`pathValid`, `pathCost`, `pathAdd`). Report those beside milliseconds
when judging path changes.

### 0.2 What "identical" can mean for path changes

All AI queries share one reused search tree per finder (`AIPathReuse.h`). A reused
query's answer depends on the tree's history in two ways:

- **Ties.** Equal-cost alternatives are broken by open-list order (engine.cpp:171-172).
- **Path-dependent costs.** `pathCost` depends on the parent's moves left, so a plot's
  label depends on which parent reached it first.

Any change in the sequence of searches on a finder can therefore change a later,
unrelated query by a tie. That includes skipping one search, or invalidating the reuse
owner. Two levels of identity follow:

- **Decision-identical:** the caller makes the same choice given the same path answers.
  This is provable for lower-bound skips, branch and bound with tie order kept, and
  the cost-bounded search of section 2.4.
- **Game-identical:** the whole game replays the same. This is only testable, never
  guaranteed, for any change that alters the search sequence.

Two ways to test (details in section 2.6):

- A shadow oracle in a debug build: run the optimized and the baseline query and
  assert the same `(found, turns, end-turn plot)`.
- A/B games with reuse disabled in *both* builds. Then results no longer depend on
  history.

## 1. Path search mechanics that matter for bounds

| Piece | Where | Behaviour |
|---|---|---|
| Search entry | CvSelectionGroup.cpp:70-93 (`generatePathOn`) | admits reuse via `AIPathReuse::Owner` (key: group, groups epoch, game turn, least moves left; CvSelectionGroup.cpp:52-68); returns `m_iData2` of the last node as `iPathTurns` |
| Secondary finder | CvSelectionGroup.cpp:5470-5480 | used for "other group" queries inside loops (patch 0010) |
| `pathAdd` | CvGameCoreUtils.cpp:2186-2249 | `m_iData1` = moves left after entering the node (min over units); `m_iData2` = turn index of arrival, starting at 1; child turns = parent turns + 1 if parent moves == 0; start node moves = min `movesLeft()` (or max `maxMoves()` with `MOVE_MAX_MOVES`) |
| `pathCost` | CvGameCoreUtils.cpp:1733-2004 | non-final step of a turn: 1000 x movementCost (1883); turn-ending step: 1000 x all remaining moves (1808) + 3 if foreign (1812) + avoid-enemy multiplier (1871-1875, `AIPathPolicy::threatAdjustedCost`: x3 / x1.5 for WEIGHT_3, x2 / x4/3 for WEIGHT_2) + defence 10 x (200 - plot defence) for units that can fight (1950); attack destination with a visible defender: defence at the from-plot, +100 if not from a city, river +100 x 25 and +1000 x moves left (1957-1975); +2 per step, +1 per diagonal (1994-1999) |
| Weights | CvGameCoreUtils.cpp:23-31 | MOVEMENT 1000, RIVER 100, CITY 100, DEFENSE 10, TERRITORY 3, STEP 2, STRAIGHT 1; `PATH_DAMAGE_WEIGHT` is 0 in XML (GlobalDefines.xml:1654), so the damage/extra-cost block at 1816-1827 never runs |
| `pathValid` | CvGameCoreUtils.cpp:2121-2183 | parent-only tests memoized per expanded parent (2013-2024, 2167-2182); the memo key has finder, parent, group, x, y, flags, turn-start |
| `pathHeuristic` | CvGameCoreUtils.cpp:1727-1730 | `stepDistance x 1000` |
| Movement cost | CvPlot.cpp:2763-2844 | route cost = min(iMovement + team change, iFlatMovement x baseMoves) (2832-2835); `MOVE_DENOMINATOR` = 120 (GlobalDefines.xml:193) |

**Key property.** Within a turn, the movement charges add up to the moves the group had
at the start of that turn. Non-final steps charge their cost and the turn-ending step
charges the remainder. So:

- a full turn costs 1000 x (maxMoves of the unit `pathCost` picks), which is 120,000
  x baseMoves;
- the first turn costs 1000 x the start node's moves.

Movement cost therefore encodes "turns first, then moves used in the last turn". Only
the extra terms can make a path with more turns cheaper than one with fewer: defence,
territory, avoid multipliers and attack-destination terms.

## 2. Bounded search

### 2.1 How `pathAdd` counts, and what a bound must test

A child reached through parent P arrives in turn `P->m_iData2 + (P->m_iData1 == 0 ? 1 : 0)`
(CvGameCoreUtils.cpp:2224-2228). `pathValid(parent, node)` sees the parent before
`pathCost`/`pathAdd` run for the child, so it can reject in two ways:

- **parent side** (the prototype): reject every child when `P->m_iData2 > N`. A parent
  at turn N with 0 moves left still generates turn-(N+1) children, which then are
  never expanded.
- **child side** (tighter): reject when `P->m_iData2 + (P->m_iData1 == 0) > N`. This
  saves one ring of `pathCost`/`pathAdd` calls around the turn-N frontier.

### 2.2 When a turn-bounded search answers differently from "unbounded, then `<= N`"

Let P* be the cheapest path found by the unbounded search and T(P*) its turns.

1. If T(P*) <= N, both accept, but the bounded search can return a different
   equal-cost path or turn count. Its open list holds different nodes, so ties break
   differently: section 2.3.
2. If T(P*) > N but a costlier path with <= N turns exists, the unbounded search
   rejects and the bounded one accepts. The unit then moves by `pushMission`, which
   calls `generatePath` again *unbounded* (CvSelectionGroup.cpp:4358, 4668, 6263). So
   it may follow P* and take more than N turns. Costlier-but-faster paths arise from:
   - **Avoid-enemy flags** (`MOVE_AVOID_ENEMY_WEIGHT_2/3`). The turn-ending step in or
     next to enemy land costs up to 3x, so detours that take an extra turn become
     cheaper. This is common for `AI_goToTargetCity`, `AI_pickTargetCity` called with
     WEIGHT_2, `AI_assaultSea*` and `AI_pirateBlockade`.
   - **Attack destinations across a river.** +1000 x moves left at the attacking step
     (CvGameCoreUtils.cpp:1973) can exceed a full turn's cost, so arriving later
     without a river crossing wins. This affects `AI_anyAttack`, `AI_cityAttack`,
     `AI_stackAttackCity` and `AI_leaveAttack`, whose destinations hold enemy units.
   - **Defence terms alone** (flags 0, no attack). One extra turn adds at least
     1000 x (cheapest step) of movement. The fewer-turn path can only lose if its
     turn-end defence terms exceed the more-turn path's by more than that: at most
     about 2,000 per turn end, so roughly (T+1) x 2,000 + 3 per turn end.
     - Roads (60, or 40 after Motorized Transportation), paved (40), Roman and modern
       roads (30): impossible for T <= 9.
     - Railroad for 1-move units (12,000 per step): possible from T of about 5.
     - Jumplane (3,000 per step): possible from T = 1.
     - At turn 400 on Marathon there are no railroads, so for flags 0 and N <= 7 the
       turn bound changes no decision in this save.
3. **Path-dependent labels.** A plot keeps only its cheapest-g parent. If that parent
   is pruned, the plot gets a costlier label with fewer turns and possibly more moves
   left. Its descendants can then reach the destination by a path the unbounded search
   never considered. This is an edge case.

### 2.3 Why the prototype diverges

Three sources. Section 2.2 shows the first is almost certainly not the cause for
`AI_guardCity`, whose flags are 0 and whose destination is a city with no visible
enemy:

1. A genuine decision change from 2.2, case 2.
2. **Different tie-breaking inside the bound.** In the unbounded search, a turn-(N+1)
   node with a small first step can have g < C* and be popped and expanded *before* the
   destination. In the prototype it is popped but not expanded. The open vector then
   differs, and the harness's "first minimum" pick (engine.cpp:169-176) can choose a
   different equal-cost path. That gives a different `getPathEndTurnPlot`, which is
   the plot `AI_guardCity` actually moves to (CvUnitAI.cpp:11620, 11654).
3. **Reuse disabled and owner invalidated.** In the original game the next helpers in
   the same `AI_update` continue the tree `AI_guardCity` grew: same group, flags 0,
   for example `AI_heal`, `AI_group`, `AI_guardCity(false, true, 3)` and
   `AI_retreatToCity`. In the prototype they start fresh. Equal-cost ties then
   resolve differently.

**Telling them apart.** In a debug build, run each bounded query also unbounded on a
scratch finder and log any mismatch in found / turns <= N / end-turn plot. If none
appear, the divergence is all source 3.

### 2.4 An exact bound: prune by cost, on the parent side

Prune expansion from a parent whose known cost exceeds U(N). U(N) is any upper bound on
the cost of a path with at most N turns:

```
U(N) = 1003 x (S0 + (N-1) x Mmax)                  movement + step/diagonal weights
     + (N+1) x A x (3 + Dmax)                       turn-end territory + defence
     + (A-1) x 1000 x Mmax x N                      avoid multiplier on turn-end steps
     + Xdest                                         attack-destination terms
S0   = start node m_iData1 (as pathAdd sets it)
Mmax = max maxMoves() over the group's units
A    = 1 (no avoid flag), 2 (WEIGHT_2), 3 (WEIGHT_3)
Dmax = 10 x (200 - min(0, lowest plot defence in XML)), at least 2000
Xdest= if AI-controlled and the destination may hold a visible defender:
       Dmax + 100 + 100 x (-RIVER_ATTACK_MODIFIER) + 1000 x Mmax; else 0
```

The 1003 factor works because each step costs at least 1 move unit.

In `pathValid`, before the memo:

```
if (finder == s_kBound.pFinder && parent->m_iKnownCost > s_kBound.iCost) return FALSE;
```

Why this is exact, sketched:

- If T(P*) <= N, then C* <= U. With a consistent heuristic (the current one is
  consistent: every edge costs >= 1,002 and h changes by <= 1,000 per step), every node
  popped before the destination has g <= f <= C* <= U. So the pruning never fires
  before the destination is popped.
- Children are still *generated* and added to the open list, so the open vector
  evolves exactly as in the unbounded search, including tie order.
- The answer and the stored tree are identical at that moment.
- If T(P*) > N, both reject: no path with <= N turns can exist when C* > U.

Strength:

- Without avoid flags, U(N) is N turns plus a few thousand cost units, almost as tight
  as the turn bound.
- With WEIGHT_2/3 it allows up to 2-3x the turn-ending step costs. Weaker, but still
  exact.

Reuse rules:

- Add the bound to `AIPathReuse::Key`, so only queries with the same bound reuse the
  tree. A candidate loop keeps its reuse.
- Keep the owner after a *successful* bounded query. The tree equals the unbounded
  tree at that point, so even later unbounded queries continue identically.
- Invalidate the owner after a bounded query that *drained* without reaching the
  destination. That tree differs from the unbounded one.

Implementation notes:

- `pathValid` also serves the interface finder (CvMap/CvGlobals set it up with the
  same callbacks), so key the bound by finder.
- Set the bound in `generatePathOn` and clear it afterwards. Add an `int iMaxPath = -1`
  parameter to `generatePath`. K-Mod's replacement unit path finder offers the same
  kind of max-path argument, as far as I know.
- Combine with a lower-bound pre-filter: skip the candidate when
  `AI_minPathTurns(plot, steps) > N`. That is decision-identical and avoids even the
  search call, which in the harness means a 2,816-node reset per fresh search.
  `AI_minPathStepsPerTurn` rescans all plots per call (CvUnitAI.cpp:154-163); compute
  it once per loop, or keep per-route plot counts updated in `CvPlot::setRouteType`.

### 2.5 Which callers a bound can serve

**Safe**, with flags 0 / SAFE / NO_ENEMY, short N, and no attack destination. Even the
turn bound changes no decision without railroads:

- `AI_guardCity` (N = 1, 3, 7)
- `AI_group` (1-10)
- `AI_groupMergeRange` (range + 2)
- `AI_shadow` (4)
- `AI_load` (1-4)
- `AI_guardCityMinDefender` (10; could deviate once railroads exist)
- `AI_cityOffenseSpy`, `AI_bonusOffenseSpy` (5 or 10, or the range)
- `AI_exploreRange` (3), `AI_reconSpy` (range)
- `AI_retreatToCity` pass 2 (1)
- `AI_moveIntoCity`, `AI_defend`, `AI_safety`, `AI_hide` (1)
- `AI_foundRange`, `AI_found` (range or horizon), `AI_pickupStranded`

**Behaviour-changing with the turn bound** (use the cost bound):

- `AI_goToTargetCity` with WEIGHT_2 (CvUnitAI.cpp:2517, 3304-3335)
- `AI_pickTargetCity` called with WEIGHT_2 and N = 12
- `AI_assaultSeaReinforce` (N = 2 with WEIGHT_3, 17651)
- `AI_assaultSeaTransport`, `AI_pirateBlockade`
- The attack family `AI_anyAttack`, `AI_cityAttack`, `AI_stackAttackCity`,
  `AI_leaveAttack`: their destinations get the attack and river terms.

**Counterproductive at any bound.** The increasing-limit chain in `AI_attackCityMove`
(CvUnitAI.cpp:3304-3335) calls `AI_goToTargetCity(AVOID_2, 5 / 8 / 12 / MAX_INT)` for
one target:

- A bound only saves work when a call fails inside its bound.
- In this chain, a failure is followed by the next call with a larger bound. That call
  must re-search, because reuse needs an equal bound.
- Unbounded, the chain costs one search plus cheap reuses.

### 2.6 Validation recipe

1. **Shadow oracle.** Under a debug define, `generatePathOn` with a bound also runs the
   query unbounded on a scratch finder. It asserts that the found flag, whether turns
   <= N, and the end-turn plot all agree, and counts mismatches by caller.
2. **History-free A/B.** A build switch forces `bReuse = false` in both baseline and
   candidate. Decision-identical changes must then give identical games, apart from
   the time they save.
3. **Callback counts.** Report `pathValid`/`pathCost` call counts per caller, not only
   ms, because of the caveat in section 0.1.

## 3. Path searches by caller

None of these loops sorts its candidates, except `AI_explore` (sorted by bound,
CvUnitAI.cpp:15083-15115) and `AI_loadForCoastalAttack` (bound prune, 10861-10895).
All use `bReuse = true`, so the first query of a group state is fresh and later ones
continue the same tree. The tree grows to the farthest candidate examined.

"Lower bound" below means `AI_minPathTurns` (stepDistance / max steps per turn, using
the cheapest route on the map) used either to skip candidates with minTurns > N, or for
branch and bound when the value is divided by turns. "Needs":

- R = only reachable within N;
- T = turns used in the value;
- P = the actual path (end-turn plot used for the move).

| Caller (search line) | Loop bound | N / use | Needs | Lower bound usable | Profile (incl ms / calls) |
|---|---|---|---|---|---|
| `AI_guardCity` (11611) | own cities in list order, stops at the first with a path <= N (break 11630) | 1, 3, 7, or MAX_INT (4398, 4567) | R, P | yes: skip minTurns > N; with MAX_INT the "first found" rule leaves nothing to bound (fault F1) | 3,868 / 2,898 |
| `AI_guardCityMinDefender` (11392) | own cities in area under min defenders | <= 10; value = need x 20 + ... - turns | T, P | yes (skip > 10; branch and bound on value) | below the 290 ms cutoff |
| `AI_pickTargetCity` (15322, 15354) | all potential-enemy cities in the area, all players | MAX_INT (attackCityMove 2924) or 12; value = cityValue x 1000 / (4 + turns^2) | T | yes: compute the non-path value first (`AI_targetCityValue` costs about 77 us), branch and bound on value / (4 + minTurns^2); the bombard add (15406) only raises turns | 1,502 / 122 |
| `AI_goToTargetCity` adjacent loop (15462) | 8 plots around the target | 1, 4, 5, 8, 12, MAX_INT; usually WEIGHT_2 | T, P | little: the 8 plots share one distance | "plot attack" 737 / 28 (26 ms per call) |
| `AI_goToTargetBarbCity` (15554, 15590) | barbarian cities, then 8 adjacent plots | < N for cities, <= N for plots (F4) | T, P | yes | small |
| `AI_group` (10673) | all selection groups of the player that pass the filters | iMaxPath 1-10; value = 1000(t+1)(4+cargo)/units, minimized | R, T | yes: skip minTurns > N; branch and bound on value | 782 / 2,628 |
| `AI_groupMergeRange` (10787) | units on plots within range r <= 2 | r + 2 | R, T | rarely needed | part of the callers' time |
| `AI_shadow` (10506) | all units of the player that are heads of the given UnitAI | 4 | R, T | yes | small |
| `AI_load` (11155) | all units (transports) of the player | 1-4 | R, T | yes | 132 / 2,130 |
| `AI_nextCityToImprove` (19302) + `AI_bestCityBuild` (1076, 1128) | cities in the area with worker need; per city, pass 0 (1 search) and maybe pass 1 (up to 21) | value / (turns + 1) | T | yes: upper bound = cityValue x 1000 x (2 if capital) / (minTurns(city) - radius + 1), checked *before* calling `AI_bestCityBuild` | 1,153 / 409 (`AI_bestCityBuild` 1,070 / 3,179) |
| `AI_routeTerritory` (20331) | every map plot owned by the player that needs a better route | 10000 / (turns + 1) | T | yes: process by stepDistance, stop when minTurns > best turns (keep index tie order) | 704 / 446 (getBestRoute inside) |
| `AI_retreatToCity` (20541) | 4 passes x all own cities | MAX_INT, except pass 2: 1 with IGNORE_DANGER | T, P | yes: nearest-first branch and bound per pass | 357 / 470 |
| `AI_cityOffenseSpy` (23032) -> `AI_getEspionageTargetValue` (22974) | all cities of eligible foreign players in the area | 5 or 10 | R | yes, but the RNG draw at 22949 must stay before the skip | `AI_spyMove` 359 / 22 |
| `AI_explore` / `AI_exploreRange` (15092, 15205) | all plots / plots in range | value-bound / iRange | T / R | already used | 337 / 5 and 337 / 21 |
| `AI_protect` (14462) | owned plots with visible enemies; odds checked first | 5, 8 | T | yes | small |
| `AI_anyAttack`, `AI_cityAttack`, `AI_leaveAttack`, `AI_stackAttackCity`, `AI_pillageRange` | plots in range r | r | R, T | mostly local; guards against unreachable-plot floods | `AI_anyAttack` 194 / 2,202 |
| `AI_pillage` (16847) | all map plots | value / (turns + 1), raw-value prune present | T | tighten with minTurns | 85 / 116 |
| `AI_guardBonus`, `AI_guardFort`, `AI_moveToStagingCity`, `AI_irrigateTerritory`, `AI_settlerSeaFerry`, `AI_carrierSeaTransport` | plots or cities | value / (turns + k) | T | branch and bound | small each |
| `isHasPathToAreaPlayerCity` (CvSelectionGroup.cpp:3785) | cities of one player in the area, stops at the first reachable | -1 (any) or N | R | nearest-first order; identical boolean | 310 / 137 |
| `AI_assaultSeaReinforce` (17651, 17710, 17717) | plots in range, then all groups with secondary queries | 2, relative turns; WEIGHT_3 | T | risky | 170 ms *self* in 12 calls (loops, not paths) |
| `pushMission` -> `groupPathTo` (CvSelectionGroup.cpp:4358, 4668) | one search per move | none | P | n/a; this is where a better heuristic pays off | 815 / 3,168 incl. the move itself |

### 3.1 Which callers produce the searches

The profile has no per-caller count of `generatePath` calls. The inclusive times give
the time split; the call split below is an estimate and should be measured.

| Group | Estimated searches (of 29,654) | Path time (of 11.25 s) |
|---|---|---|
| Worker AI: `AI_bestCityBuild` + `AI_nextCityToImprove` (at least 2 x 3,179, mostly reused), `AI_routeTerritory` (446 calls x 5-30 targets), connect, improve, irrigate | 10-15 k | about 1.8 s (16 %) |
| `AI_guardCity` (2,898 calls x 1-5 candidates searched) | 4-8 k | about 3.6 s (32 %); the measured bound removed 2.6 s of it |
| Grouping: `AI_group`, `AI_groupMergeRange`, `AI_shadow`, `AI_load` | 3-6 k | about 0.8 s (7 %) |
| City attack: `AI_pickTargetCity` (122 calls x 10-40 enemy cities), adjacent loops | 2-4 k | about 2.2 s (20 %); few searches, but long, and with WEIGHT_2 |
| Retreat, explore, spy, protect, the attack family, `isHasPath*`, sea, `pushMission` | 3-5 k | about 2.5 s (22 %) |

To get exact counts, add a per-caller tag: a static `const char*` set by an RAII guard
at the top of each `AI_*` loop. Have `generatePathOn` count searches, fresh vs reused,
and `pathValid` calls per tag.

### 3.2 Ranking: which callers besides `AI_guardCity` would profit from a bound

The measured scale is 2.6 s saved on 3.87 s, which is 67 %. That happened where the
first candidates are typically far away and fail, and the searches were unbounded.

| Rank | Caller | At stake | Why it profits | Expected saving | Bound safety |
|---|---|---|---|---|---|
| 1 | `AI_group` (CvUnitAI.cpp:10567-10718) | 782 ms | hundreds of candidate groups per call, N mostly 1-6; reuse makes the tree grow to the farthest candidate examined | 300-450 ms | safe (flags 0); keep reuse among same-bound queries; add the minTurns skip and value branch and bound |
| 2 | Spy offense: `AI_cityOffenseSpy` (23002), `AI_bonusOffenseSpy` (23062) | 359 ms in 22 calls | every foreign city in the area is searched; spies path through foreign land; N = 5 or 10 | 150-250 ms | safe (flags 0); keep the RNG draw at 22949 |
| 3 | `AI_retreatToCity` pass 2 (20541) | part of 357 ms | flags change (IGNORE_DANGER) gives a fresh full search per city; N = 1 | 50-120 ms (plus 100-150 ms from nearest-first branch and bound in the other passes) | safe |
| 4 | `AI_exploreRange(3)` (15205) | 292 ms ("AI_exploreRange 3") | lower bound already applied; the bound still cuts floods behind water or blockers | 80-150 ms | safe (NO_ENEMY_TERRITORY, no avoid weights) |
| 5 | `AI_pickTargetCity` with finite N (barbarians 12, 2919; `AI_goToTargetCity(AVOID_2, 12)` from `AI_attackMove`, 2517) | part of 1,502 ms | 12 turns spans most of the continent, so the bound is weak | 100-300 ms | turn bound is behaviour-changing (WEIGHT_2); use the cost bound; branch and bound gives more (section 7, rank 3) |
| 6 | Attack family with range r (`AI_anyAttack` 15968, `AI_cityAttack` 15872, `AI_stackAttackCity` 23915, `AI_leaveAttack` 16114, `AI_pillageRange` 16979, `AI_pillageAroundCity` 15669) | about 300 ms together | candidates are local; the gain comes only from candidates that are unreachable or behind a detour, whose search otherwise drains the whole reachable area | 50-150 ms | attack and river terms: cost bound only |
| 7 | `AI_shadow` (N 4), `AI_load` (N 1-4), `AI_groupMergeRange` (r + 2) | under 250 ms together | loops over all units of the player | 50-100 ms | safe |
| 8 | `AI_guardCityMinDefender` (N 10) | under 290 ms | city-defense units searching all cities; N = 10 is weak | 30-100 ms | safe until railroads |
| 9 | `AI_protect` (N 5, 8) | small | the odds pre-check already limits searches | under 30 ms | safe |
| 10 | Sea: `AI_assaultSeaReinforce` (N 2), `AI_seaBombardRange`, `AI_pickupStranded` | small path share | WEIGHT_3 | uncertain | cost bound only |

Not bound candidates, because they have no N: `AI_pickTargetCity(..., MAX_INT)` from
`AI_attackCityMove`, `AI_nextCityToImprove`, `AI_routeTerritory`, `AI_guardBonus`,
`AI_guardFort`, `AI_moveToStagingCity`, `AI_pillage`, `AI_irrigateTerritory`. Use
branch and bound on the lower bound instead (section 3 table, section 7). Also excluded: the
`AI_goToTargetCity` chain (section 2.5) and `AI_guardCity` with MAX_INT (fault F1).

## 4. Heuristic

`pathHeuristic` = stepDistance x 1000 (CvGameCoreUtils.cpp:1727-1730).

- **Admissible and consistent.** Every edge costs at least 1,000 x 1 + 2, and h changes
  by at most 1,000 per step.
- **Very weak.** A tile's true cost is 1,000 x movementCost: 120,000 off-road for a
  1-move unit. The ratio h / true cost per tile is:

| Route (CIV4RouteInfos.xml) | iMovement / iFlatMovement | Cost per tile, 1-move unit | Tiles per turn (unit with bm moves) | h / true |
|---|---|---|---|---|
| none / ROUTE_TRACK | 120 / 120 | 120,000 | bm (terrain permitting) | 0.8 % |
| ROUTE_ROAD | 60 / 60 (-20 with TECH_MOTORIZED_TRANSPORTATION) | 60,000 (40,000) | 2 bm (3 bm) | 1.7 % (2.5 %) |
| ROUTE_PAVED (needs Stone) | 40 / 40 | 40,000 | 3 bm | 2.5 % |
| ROUTE_ROMAN_ROAD | 30 / 30 | 30,000 | 4 bm | 3.3 % |
| ROUTE_MODERN_ROAD | 30 / 30 (-6 Miniaturization, -4 Skyroads) | 30,000 (20,000) | 4 bm (6 bm) | 3.3 % (5 %) |
| ROUTE_RAILROAD | 30 / 12 | min(30, 12 bm): 12,000 | 10 (bm <= 2), 12 (bm >= 3) | 8.3 % |
| ROUTE_RAILROAD_ELECTRIC | 30 / 10 | 10,000 | 12 | 10 % |
| ROUTE_GRAVTUBE | 20 / 6 | 6,000 | 20 (bm <= 3), 24 (bm >= 4) | 16.7 % |
| ROUTE_JUMPLANE | 15 / 3 | 3,000 | 40 (bm <= 5), more above | 33 % |

The flat cost is multiplied by `baseMoves` (CvPlot.cpp:2834-2835). Railroads and later
routes therefore give a fixed number of tiles per turn regardless of unit speed. Before
railroads the search is effectively Dijkstra.

**A stronger admissible heuristic.** Let K = max tiles per turn, which is what
`AI_minPathStepsPerTurn` computes, and Mmin = min maxMoves in the group. Every full
turn costs at least 1,000 x Mmin. A distance d needs at least ceil(d / K) turns
counting both partial ends, so:

```
h(d) = max(1002 x d, 1000 x Mmin x (ceil(d / K) - 2))
```

- **Strength.** For d = 20, roads, bm = 1, K = 4 (Roman roads present): 360,000
  against 20,000 today, against a true 600,000 to 1,200,000.
- **Admissible but not consistent.** h can drop by a full turn's cost across one cheap
  route step.
- **Needs group context.** The callback signature is `(x1, y1, x2, y2)`
  (CvDLLFAStarIFaceBase.h), so K and Mmin must sit in a static that `generatePathOn`
  sets, keyed by finder. The engine's own interface searches share the callback.

Where it pays:

- Single-target long searches: `pushMission` -> `groupPathTo` (815 ms including the
  move), and the 8-plot cluster in `AI_goToTargetCity` (26 ms per call with WEIGHT_2).
- Not the candidate scans. Their reuse relies on Dijkstra-like uniform growth; a
  goal-directed tree for candidate 1 makes candidate 2 cost more.

Risks:

- Expansion order changes, so ties change: behaviour-changing.
- The harness rescores open nodes on reuse (engine.cpp:218-222). Whether the game's
  FAStar does is unknown. If it does not, stale strong h values would be inadmissible
  for the new destination.
- With an inconsistent h, correctness relies on the engine re-improving closed nodes.
  The harness does (engine.cpp:257-272); patch 0010's notes say the engine does not
  reopen closed nodes.
- Recommendation: use it only on non-reused single-target queries, for example a flag
  set by `groupPathTo`, after bounds and branch and bound. Landmark (ALT) heuristics
  do not fit, because costs depend on group, moves left and danger.

## 5. Other per-turn work that scales badly

### 5.1 `CvPlayer::getBestRoute`: 444,219 calls, 1,408 ms incl, 633 ms self

- **Code.** CvPlayer.cpp:7887-7922 loops over all 55+ build infos. For each of the 9
  route builds (CIV4BuildInfos.xml) it calls `canBuild(pPlot, build)` unless the plot
  already has that route.
- **Why it is slow.** `CvPlayer::canBuild` (7832-7869) calls `CvPlot::canBuild` first.
  For a route ranked above the current one, that runs the prerequisite-bonus and
  OR-bonus tests, each `isAdjacentPlotGroupConnectedBonus` over 9 plots
  (CvPlot.cpp:2370-2398). The tech test comes only afterwards (CvPlayer.cpp:7841-7850).
  At turn 400 the team lacks most of PAVED, MODERN, RAILROAD, ELECTRIC, GRAVTUBE,
  JUMPLANE and maybe ROMAN, so each call does up to about 6 wasted plot checks.
- **Callers:**
  - `routeValid` (CvGameCoreUtils.cpp:2442) in the route-finder floods of
    `CvCityAI::AI_updateRouteToCity`: per city per turn, a flood over the player's
    best-route network (CvCityAI.cpp:6513-6561, from AI_doTurn 221).
  - `AI_routeTerritory`: every owned plot, per worker call (CvUnitAI.cpp:20296).
  - `calculateImprovementYieldChange(..., bBestRoute = true)`: once per yield per
    improvement (CvPlot.cpp:6247-6250), from `AI_getImprovementValue`
    (CvCityAI.cpp:7549-7567) and `AI_bestPlotBuild` (11494-11520).
- **Gold dependency.** `canBuild` needs gold >= build cost (CvPlayer.cpp:7862), and
  route builds cost 2-100 gold. The best route of a plot therefore depends on the
  treasury, and a per-plot per-turn cache would not be exact (fault F7).

Replacements (all identical, since `USE_CAN_BUILD_CALLBACK` is 0 and every test is
pure):

- (a) Route builds in a static list sorted by (route value desc, build index asc). This
  is what was measured: 270 ms. Keep the stable order: ROMAN and MODERN both have
  value 4.
- (b) **Check tech first.** Keep a per-team bitmask of route builds whose
  `getTechPrereq` the team has, updated on tech change. In the sorted scan:
  `route == current -> return it; else if (techBit && canBuild) -> return route`.
  Builds without tech cost one bit test.
- (c) Also move the tech test ahead of `pPlot->canBuild` inside `CvPlayer::canBuild`
  itself. Both are pure conjuncts, and it speeds every other caller too.
- (d) Hoist `getBestRoute` out of the per-yield loops. Compute it once per plot in
  `AI_getImprovementValue` / `AI_bestPlotBuild`, and pass the route to a
  `calculateImprovementYieldChange` overload. That is 6 to 12 calls -> 1 per plot.
- **Estimate:** 0.6-1.0 s beyond the 270 ms already measured. Confirm with a
  `PROFILE("getBestRoute canBuild")` around the inner call.

### 5.2 `canBuild` volume: 3.80 M calls, 826 ms self

- **Sources:** `getBestRoute` (above, most of it); `CvCityAI::AI_bestPlotBuild`
  (11073: improvements x builds, 11303-11345, plus feature-clear and chop loops
  11799, 11832); `AI_getImprovementValue` (7426); the worker AI through
  `CvUnit::canBuild` (CvUnitAI.cpp:1071, 19126, 19467, 19588, 19741, 20034);
  `countUnimprovedBonuses` (CvPlayer.cpp:4870).
- **Replacements:**
  - The tech-first order of 5.1 (c). Identical.
  - A static improvement -> builds index for the I x B loop in `AI_bestPlotBuild`
    (11303-11330): O(I x B) -> O(B) build-info reads per plot. Identical; this part is
    in its 118 ms self time.

### 5.3 `CvCity::canTrain`: 1.06 M calls, 1,454 ms incl, 1,179 ms self

- **Code.** CvCity.cpp:2143-2226 calls `allUpgradesAvailable` (1979-2060) and
  `isForceObsoleteUnitClassAvailable` (1927-1975). Both call `canTrain` on other units
  recursively:
  - `allUpgradesAvailable` walks the whole upgrade DAG with no memo, so shared
    sub-trees are visited once per path;
  - `isForceObsoleteUnitClassAvailable` loops over all unit classes x their upgrade
    classes.
  So one top-level `canTrain` costs O(upgrade paths x unit classes). Most of the 1.06 M
  calls are these inner calls.
- **Top-level callers:** `AI_chooseProduction` (215 calls, 1.82 s incl, via
  `AI_bestUnitAI` 3799 and 3380); `AI_buildingValueThreshold` (6,980 calls, through
  `canTrain(UnitCombatTypes)` at 4618, which loops over all unit classes,
  CvCity.cpp:2229-2247); the conscript loops (CvCity.cpp:4016); `AI_upgrade` /
  `canUpgrade`; `AI_goldToUpgradeAllUnits` (CvPlayerAI.cpp:22480-22487).
- **Replacements:**
  - (a) Static, per civilization: for each unit, the list of force-obsolete unit types
    and the deduplicated set of reachable upgrade units. That drops the
    all-unit-classes scans. Identical.
  - (b) A scoped memo: an RAII `CanTrainScope` in `AI_chooseProduction`,
    `AI_bestUnitAI`, `AI_buildingValueThreshold` and `AI_upgrade`. It caches
    `canTrain(city, unit, flags)` and the `allUpgradesAvailable` results while no game
    state changes. Identical inside the scope.
  - (c) `canTrain(UnitCombatTypes)` per city, cached for the same scope.
- **Estimate:** 0.6-0.9 s.

### 5.4 `AI_plotValue` (33,463 calls, 912 incl / 659 self ms) and `calculateImprovementYieldChange` (1.05 M calls, 656 ms)

- **Callers.** `AI_addBestCitizen` (3,782 calls; CvCityAI.cpp:9858),
  `AI_removeWorstCitizen` (9983) and `AI_juggleCitizens` (10066) evaluate every
  candidate plot for the same city state. That is O(population x 21 plots) per
  assignment.
- **Cost per evaluation.** About 20 us self:
  - `AI_yieldValue` (10228-) is called twice per plot and re-queries city state that
    does not depend on the plot: happiness, health, `foodDifference`,
    `growthThreshold`, commerce modifiers per commerce type, hurry anger,
    `getBestYieldAvailable`.
  - A loop over all bonus infos with tech checks (10870-10885) depends only on (team
    techs, improvement).
- **Replacements:**
  - (a) A `CityYieldContext` struct filled once per `AI_addBestCitizen` /
    `AI_removeWorstCitizen` / `AI_juggleCitizens` call and passed to `AI_yieldValue`.
    Identical, because the state is constant during the candidate loop.
  - (b) Per team: the count of discoverable bonuses per improvement, refreshed on tech
    change. Identical.
  - (c) `calculateImprovementYieldChange`: drop the repeated `getBestRoute` (5.1 d).
    The final-vs-current pair at 10848 is cheap.
- **Estimate:** 0.35-0.5 s.

### 5.5 `AI_unitValue` (437,018 calls, 590 ms) and `AI_upgrade` (4,386 calls, 697 ms incl, 234 self)

- **Code.** `AI_upgrade` (CvUnitAI.cpp:605-677), per unit with
  `isReadyForUpgrade`:
  - loops over all unit classes, filtered by the cached `upgradeAvailable`;
  - calls `AI_unitValue` per candidate in pass 0, and again in pass 1 for the same
    candidates;
  - then `canUpgrade` -> `getUpgradeCity` -> `findCity` / `canTrain`.
  437,018 / 4,386 = about 100 `AI_unitValue` calls per upgrade check.
- **What `AI_unitValue` depends on** (CvPlayerAI.cpp:10698-11789): (unit, UnitAI,
  area) plus player-level weights. It loops over combat types, unit classes and units.
  The missionary and executive branches read unit counts.
- **Replacements:**
  - (a) Memoize across the two passes. Identical; halves the calls for pass-0
    candidates.
  - (b) A per-player memo keyed (unit, UnitAI, area) for one `AI_unitUpdate` slice,
    invalidated on unit creation or death and on tech or civic change. Identical with
    that invalidation. Without the unit-count part it is only near-identical, for the
    missionary and executive AIs.
  - (c) `AI_goldToUpgradeAllUnits` already caches per unit type (fault F8).
- **Estimate:** 0.25-0.35 s.

### 5.6 `AI_neededDefenders` (37,112 calls, 325 ms) and `AI_isDefended` (30,773 calls, 291 ms)

- **Code.** `AI_isDefended` (CvCityAI.cpp:6096-6101) is a `plotCount` over the city
  plot's units plus `AI_neededDefenders` (6191-). The latter re-evaluates per call:
  - `hasActiveWorldWonder`, `isCapital`, `isHolyCity`;
  - strategies, area AI, `AI_isDanger`;
  - `findCommerceRateRank`, an O(cities) loop under CULTURE3.
- **Main caller.** `AI_guardCity`'s candidate loop (11605): one call per city before
  the path test.
- **Replacements:**
  - (a) In `AI_guardCity`, apply the minTurns > iMaxPath skip *before*
    `AI_isDefended` and `AI_plotTargetMissionAIs`. Pure conjuncts, so identical.
  - (b) Per city, cache the turn-static part of the needed count: wonder, holy city,
    capital, culture rank, strategy bits, area AI. Invalidate on ownership, building or
    religion change. `AI_isDanger` and turns-since-acquired stay live. Identical.
- **Estimate:** 0.1-0.2 s.

### 5.7 `AI_routeTerritory` (446 calls, 704 incl / 149 self ms)

- **Cost.** CvUnitAI.cpp:20267-20359 scans all 2,816 plots per call. For each owned
  plot it calls `getBestRoute`, plus `AI_plotTargetMissionAIs` and a search for each
  plot that needs a route. Value = 10,000 / (turns + 1), so the nearest plot wins and
  ties go to the lowest plot index.
- **Replacement.**
  - Collect the cheap-filter survivors with stepDistance.
  - Process them in (minTurns, plot index) order.
  - Stop once minTurns > best turns.
  - Call `getBestRoute` only for plots that can still win.
  Identical with the index tie order. Collecting survivors needs only owner and
  `AI_plotValid`; keep a per-player owned-plot list instead of the full map scan.
- **Estimate:** 0.3-0.45 s. Overlaps with 5.1.

### 5.8 `CvMap::findCity` (63,935 calls, 129 ms)

- **Cost.** CvMap.cpp:706-760 is O(players + cities) per call, about 2 us. Callers are
  spread out (32 sites), for example `getUpgradeCity` from `canUpgrade`
  (CvUnit.cpp:8259), `AI_goldToUpgradeAllUnits` (CvPlayerAI.cpp:22486) and
  `AI_targetCityValue` (3589).
- **Replacement.** Per-team (or per-player) city lists by area, with a nearest search
  that breaks ties in the original (player, city-list) order. Identical. Saving under
  0.1 s; low priority.

### 5.9 `AI_updateRouteToCity` route floods

- **Cost.** CvCityAI.cpp:6513-6561 is one route-finder flood per city per turn,
  reused across that city's targets. `routeValid` calls `getBestRoute` for each
  neighbour test.
- **Replacement.** One component labelling of "plots on the player's best route" per
  player, invalidated by `setRouteType`, `setOwner` and gold-threshold changes (fault
  F7). Identical only with exact invalidation. 5.1 (b) already makes each
  `getBestRoute` cheap, so do that first.

### 5.10 Path callbacks themselves

- **`pathCost` per-unit loop** (1783-1990). Evaluate units with the same movement
  signature once: baseMoves, terrain and feature double-move masks, ignore-terrain,
  flat-movement, can-fight, no-defensive-bonus, can-attack, always-hostile, river.
  Identical. Most groups are 1-3 units, so 0.1-0.3 s.
- **`pathAdd` loop.** Same idea.
- **`AI_minPathStepsPerTurn`.** Rescans all plots per call (CvUnitAI.cpp:154-163).
  Keep per-route plot counters updated in `CvPlot::setRouteType`. O(1) and exact.

## 6. AI behaviour faults noticed

- **F1. `AI_guardCity` takes the first city in city-list order, not the nearest**
  (CvUnitAI.cpp:11588-11635, `break` at 11630-11633). The `iValue = iPathTurns`
  minimization is dead code. With iMaxPath = MAX_INT (`AI_cityDefenseMove` 4398,
  `AI_cityDefenseExtraMove` 4567), a defender walks to the first undefended city in the
  list, however far, past nearer undefended ones. Fix: nearest by turns, with
  branch and bound on minTurns. That changes behaviour.
- **F2. Two guard functions, two rules.** `AI_guardCityMinDefender` scores need, age
  and occupation minus turns, with N = 10 (11396-11402). `AI_guardCity` takes the first
  city. They also count defenders differently: `AI_minDefenders` plus GUARD_CITY
  missions, against `AI_isDefended` with group-head defenders. So the same city can
  look defended to one and undefended to the other.
- **F3. Target chosen and approached by different metrics.** `AI_attackCityMove`
  picks the target with flags 0 (`AI_pickTargetCity(0, MAX_INT)`, 2924) but marches
  with `MOVE_AVOID_ENEMY_WEIGHT_2` (3304-3335). The turns used to rank targets are not
  the turns the march takes.
- **F4. `AI_goToTargetBarbCity` is inconsistent.** It uses `iPathTurns < iMaxPathTurns`
  for the city (15556) but `<=` for the attack plots (15592). Its river bonus is
  10 x 25 (15598), against 12 x 25 in `AI_goToTargetCity` (15470).
- **F5. `AI_upgrade` ties are biased** (CvUnitAI.cpp:655-663). A tie replaces the
  incumbent with probability 1/2, so with k tied candidates the last one wins half the
  time. The RNG is also drawn before `canUpgrade`, so failed candidates consume draws.
- **F6. `AI_routeTerritory` treats every route target as equal** (20333-20341). The
  nearest wins, and ties go to the lowest plot index (row-major from y = 0), a fixed
  geographic bias. It ignores whether the plot is worked or links anything.
- **F7. The "best route" depends on the treasury** (CvPlayer.cpp:7862 with route build
  costs of 2-100 gold). Below the cost of a road, `getBestRoute` falls back to TRACK
  (cost 0) or the existing route. `routeValid` (route-to-city connectivity) and
  `AI_routeTerritory` targets then flip with the gold balance, within a turn.
- **F8. `AI_goldToUpgradeAllUnits` caches per unit type only**
  (CvPlayerAI.cpp:22436-22447). The first unit of a type fixes the price for all units
  of that type through its UnitAI, area and location (`findCity`). This is
  order-dependent.
- **F9. Spy targeting draws RNG per candidate before the path test**
  (`AI_getEspionageTargetValue`, 22949). The RNG stream depends on the candidate set,
  so any pruning must keep the draw. `AI_explore`'s sorted branch and bound already
  changed its draw order (15094).
- **F10. The increasing-limit chain** in `AI_attackCityMove` (3304-3335) re-asks the
  same target at 5, 8, 12 and MAX_INT turns, with loads in between. It is cheap only
  thanks to reuse. A load between the calls can change the group and invalidate reuse.
- **F11. Two turn conventions.** `AI_bestCityBuild` and `AI_improveLocalPlot` add a
  turn when the path ends with 0 moves (1080-1083, 19209), counting arrival-without-
  moves as a turn. Other callers do not, so worker targets are ranked on a different
  scale.
- **F12. `AI_retreatToCity` repeats work.** Pass 1 repeats pass 0's loop with the same
  flags; pass 2 switches to IGNORE_DANGER, a fresh search over all cities for a 1-turn
  limit (20541). Ties go to list order.
- **F13. Duplicate evaluations in `AI_groupMergeRange`** (10764-10807). It iterates
  units, not groups, so a stack is evaluated once per unit. Reuse makes the repeated
  searches cheap, but `AI_allowGroup` runs per unit.
- **F14. Mixed groups.** `pathCost` takes the turn-end defence term from the one unit
  with the least moves left (min cost among ties, 1802-1987). Mixed groups get an
  arbitrary unit's defence weighting.

## 7. Ranked optimizations

Shares are of the 20.48 s turn set and overlap somewhat; the totals below are not
additive.

- **Decision-identical:** the same choice for the same path answers. Game identity is
  testable but not guaranteed when the search sequence changes (section 0.2).
- **Identical:** no path-sequence change.

| Rank | Change | Est. saving | Result | Size |
|---|---|---|---|---|
| 1 | Bounded search in `AI_guardCity`: cost bound U(N) on the parent side, child-side turn ring, minTurns pre-skip before `AI_isDefended`, reuse keyed by bound | 2.0-2.3 s (10-11 %); prototype measured -2.04 s with a turn bound | cost-bound version decision-identical; the prototype diverges (section 2.3) | S: about 60 lines in CvGameCoreUtils.cpp, CvSelectionGroup.cpp, AIPathReuse.h and the loop |
| 2 | `getBestRoute` tech-first scan (per-team bitmask), tech-first `CvPlayer::canBuild`, hoist out of `calculateImprovementYieldChange` | 0.6-1.0 s (3-5 %) beyond the measured 0.27 s | identical | S |
| 3 | `AI_pickTargetCity` branch and bound: non-path value first, upper bound with minTurns, process by bound, original-order tie rule | 0.6-1.0 s (3-5 %) | decision-identical | S-M |
| 4 | `canTrain`: static force-obsolete and upgrade lists per civilization, scoped memo of `allUpgradesAvailable` / `canTrain` | 0.6-0.9 s (3-4 %) | identical (scoped) | M |
| 5 | `AI_nextCityToImprove` branch and bound before `AI_bestCityBuild` | 0.5-0.8 s (2.5-4 %) | decision-identical | S |
| 6 | `AI_group`: bound (N 1-10) + minTurns skip + value branch and bound | 0.3-0.45 s (1.5-2 %) | decision-identical with the cost bound | S |
| 7 | `AI_plotValue`: per-call city context for `AI_yieldValue`, per-team discover counts | 0.35-0.5 s (2 %) | identical | M |
| 8 | `AI_routeTerritory`: distance-ordered branch and bound, owned-plot list, `getBestRoute` only for plots that can win | 0.3-0.45 s (2 %; overlaps 2) | decision-identical | S |
| 9 | `AI_upgrade` / `AI_unitValue` memo (passes; per-slice per (unit, AI, area)) | 0.25-0.35 s (1.5 %) | identical (scoped) | S |
| 10 | Spy offense loops: bound 5/10, RNG draw kept | 0.15-0.25 s (1 %) | decision-identical | S |
| 11 | `AI_retreatToCity`: nearest-first branch and bound per pass, bound N = 1 in pass 2 | 0.15-0.25 s (1 %) | decision-identical | S |
| 12 | `isHasPathToAreaPlayerCity`: nearest-first order | 0.1-0.15 s (0.5 %) | identical boolean | XS |
| 13 | `AI_exploreRange(3)`, attack family, `AI_shadow` / `AI_load` / `AI_groupMergeRange`, `AI_guardCityMinDefender`: bounds | 0.2-0.4 s together (1-2 %) | cost bound decision-identical; turn bound changes attack-family behaviour | S each |
| 14 | `AI_neededDefenders` static-part cache, `AI_guardCity` filter reorder | 0.1-0.2 s (0.5-1 %) | identical | S |
| 15 | `pathCost` / `pathAdd` by movement signature; O(1) route counters for `AI_minPathStepsPerTurn` | 0.1-0.3 s (0.5-1.5 %) | identical | M |
| 16 | `AI_updateRouteToCity` per-player route components | 0.1-0.3 s | identical only with exact invalidation | M |
| 17 | Stronger admissible heuristic for non-reused single-target queries (`groupPathTo`, adjacent-plot cluster) | 0-1.0 s, uncertain | behaviour-changing (tie order; engine reuse semantics unknown) | M |
| 18 | `findCity` per-area city lists | under 0.1 s | identical | S |
| 19 | Fix F1 (nearest undefended city, MAX_INT callers) and F3/F4/F5 | small time effect | behaviour-changing (intended) | S |

Totals: rank 1 is measured at about -2.0 s. Ranks 2-12 together plausibly save
another 3.5-5 s, part of which overlaps. Applying all of the identical and
decision-identical items should take the turn set from 20.5 s to roughly 13-15 s in the
harness. Measure callback counts as well, because the harness's own A* overhead
(section 0.1) inflates the gain from avoided fresh searches.
