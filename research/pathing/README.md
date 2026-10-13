# Pathfinding, naval transport, settlers and siege lethality

This is the investigation behind [patch 0010](../../fixes/0010-pathing-transport-and-siege.patch).
It targets GitLab **`main` at `a9b1fce`** (patch 0009 merged, tree `e3cbb9a8`). The
applied tree is `147f6d1f`. It landed on GitLab `main` as
[!35](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/35) (merge commit
`86af2ab`, same tree). The DLL built from it is
[`builds/0010/CvGameCoreDLL.dll`](../../builds/0010/CvGameCoreDLL.dll).

The request was to look for ways to improve pathfinding, naval transport, settler
and escort behavior, operational efficiency and lethality. Every change below
corrects a defect or removes repeated work with an identical result. Nothing
retunes AI weights without evidence. Settler transport and escort production were
already reworked by patches 0005–0008, so this round audited them, found one
remaining gap, and left the rest alone.

## How the defects were found

- **Compiler scan for ignored results.** clang's `-Wunused-but-set-variable` over all
  AI sources flags variables that are computed and never read. Of 35 hits, two were
  real decisions thrown away (`AI_choke`, `AI_assaultSeaReinforce`). The rest are
  harmless leftovers from BTS and BBAI.
- **Scan for unguarded "best" choices.** Every assignment to a `pBest…`/`eBest…`
  variable was checked for a value comparison. This found the `AI_choke` defect a
  second way, plus the inconsistent comparison in `AI_bestCityBuild`.
- **Path query discipline.** Every `generatePath` call was classified by whose
  search it is and whether it runs inside another search's candidate loop.

## Pathfinding

### How reuse works, and how it was lost

All AI path queries go through one engine A* instance (`GC.getPathFinder()`). With
`bReuse`, the engine continues its last search when the start plot and flags are
unchanged, so scoring N candidates from one group costs one incremental search.
Nearly every AI loop passes `bReuse = true`.

Five call sites query a *different* group's route in the middle of such a loop:

| Caller | Foreign query | Effect |
|---|---|---|
| `AI_pickTargetCity` | `AI_cityTargetUnitsByPath` → other stacks near a visible city | every later city restarts the attacker's search |
| `AI_assaultSeaMove` | `AI_unitTargetMissionAIs(…, 3)` → groups coming to join | restarts, with `bReuse = false` |
| `AI_assaultSeaReinforce` | the other fleet's route to a synchronized landing | every candidate fleet restarts both searches |
| `AI_loadForCoastalAttack` | each ship's route to the target's coast | every ship restarts the land unit's boarding search |
| `AI_workerMove` | `AI_isPlotThreatened` → each enemy unit's route | one fresh search per unit (below) |

With 12 visible enemy cities and 5 stacks around them, `AI_pickTargetCity` ran
72 full searches where one incremental search suffices. A model of the engine's
reuse rule reproduces exactly that count; see
[`test_path_queries.py`](../../Tools/test_path_queries.py). Siege turns in the
late game are where these loops run most.

**Change.** `CvSelectionGroup::generatePathSecondary` runs the same query on a
second engine finder. The DLL creates it in `CvMap::setup`, beside the engine's own,
and releases it in `CvGlobals::uninit` before the engine shuts down. The five call
sites use it, and only for the result and turn count, which they were already the
only things read.

### Reuse ownership

The engine decides reuse from the start plot and flags alone; the DLL cannot see
anything else in its rule. A stored search tree, however, belongs to one group in
one state: the start node's moves come from the group when the search began.
Continuing it is wrong for:

- a different group on the same plot (the original foreign queries above did this);
- the same group after units joined or left;
- the same group after it spent moves without moving (pillage, fortify, bombard);
- the same group on a later turn (other units moved, routes were built).

`AIPathReuse.h` keeps an owner key per finder: group, membership epoch, game turn and
the group's least moves left. `generatePath` passes reuse to the engine only when
the key is unchanged. The test drives 20,000 random queries while groups, moves,
membership and turns change between them. Every answer equals a fresh search for
the querying group, and reuse occurs exactly as often as it is valid. A control
shows that the engine rule alone returns 2 turns for a group that needs 8.

### Repeated threat searches

`AI_isPlotThreatened` (the worker AI's "is this plot threatened" check) ran one fresh
search for every enemy unit in range. Every unit of a stack asked its group the same
question, so a 20-unit stack cost 20 identical searches. Each group is now searched
once per call. Over 3,000 random boards the answer is identical to the original
loop, and the number of searches never exceeds the number of distinct qualifying
groups.

### Considered and not done

- **A tighter A\* heuristic.** The heuristic charges 1,000 per tile, while flat
  terrain costs 120,000 (`MOVE_DENOMINATOR` is 120 in RoM). The search is therefore
  nearly Dijkstra. A larger multiplier is admissible on average, but turn-ending
  moves can be as cheap as one move point. The heuristic would then be inconsistent,
  and the engine does not reopen closed nodes, so paths could become suboptimal.
  That needs in-game profiling first.
- **Per-unit loops inside `pathCost`/`pathValid`.** These are O(units) per expanded
  edge for large stacks. Grouping units by movement signature is possible, but it is
  invasive to verify without the engine.

## Escort and stack grouping

`AI_group` decides which escort or attacker joins which group. It scans every group
of the player and, for each candidate, calls `AI_unitTargetMissionAIs`, which scans
every group again. That is Θ(candidates × groups) per call, and every attack,
reserve and city-defense unit calls `AI_group` several times per turn.

`AIMissionTargetIndex::UnitIndex` buckets groups by their target unit. To guarantee
it never costs more than the walk, the first query of an epoch still walks. The
second query in the same epoch builds the index in Θ(groups), and later queries read
only the groups aimed at the unit. The epoch now also changes when a group's target
unit changes (`AI_setMissionAI`). Over 10,000 random queries with groups, targets,
skip groups and wildcards changing, the answers equal the original walk.

**Overflow.** In the path variant, a group with no path keeps `MAX_INT`. If it could
not all move this turn, the code then did `iPathTurns++`. That is signed overflow,
which in practice wraps negative and passes `iPathTurns <= iMaxPathTurns`, so the
unreachable group counted as "joining soon". `AI_assaultSeaMove` uses this count to
decide whether a loaded transport without escorts waits in port. The upstream
function triggers UBSan's "signed integer overflow" in the test; such a group no
longer counts.

## Naval transport: synchronized landings

`AI_assaultSeaReinforce` lets a loaded transport join another fleet's landing that
it can reach just after the fleet arrives. Its check "can every passenger fight at
the landing plot" was computed and then never read (clang:
`bCanCargoAllUnload set but not used`). Transports with artillery (combat limit
below 100%) joined landings on unseen cities, and transports joined landings whose
visible defenders their cargo could not attack.

Applying the check as written would have been wrong too: unlike
`AI_assaultSeaTransport`'s version, it treated a city with no visible defenders as
unassailable. The check now uses the same rule as `AI_assaultSeaTransport`: visible
defenders must be attackable, an unseen city rules out siege-only cargo, and an empty
city is a valid landing. The executed test covers all three cases. Upstream joins
the artillery landing.

## Siege lethality: choke positioning

`AI_attackCityMove` calls `AI_choke` when its stack is not yet strong enough to
assault. `AI_choke(1, true)` means "seek defensive ground when the enemy is
stronger", and `AI_choke(1)` means "sit on the city's best tiles to strangle
production". Both computed a value per plot and then let every reachable plot
replace the previous one. Plots are scanned from (−1, −1) to (+1, +1), so the stack
always went to the *last* valued plot, usually south-east, rather than the hill or
forest the value preferred. Each candidate also started a fresh path search
(`bReuse` omitted). The best value now wins, and one incremental search serves all
candidates. If every plot is worth nothing (open ground everywhere), `AI_choke` now
returns false, and the stack moves on to its other options instead of standing on
worthless open ground.

## Worker target choice

`AI_bestCityBuild` has two passes: the city's single best build, then a search that
divides each plot's value by its path turns. The second pass compared a candidate's
*raw* value against the best *per-turn* value. A plot worth 120 four turns away
(30 per turn) displaced one worth 100 next door (100 per turn). Both sides are now
per-turn values; the raw comparison remains as a valid prune, since per-turn value
is never more than raw value.

## Settlers and escorts

The escort supply chain was audited end to end:

- City AI trains an escort when a settler is present.
- City-defense, attack and reserve units join lone settlers through `AI_group`.
- `AI_settleMove` sends an unescorted settler back to a city and waits.
- `AI_found` keeps a committed site and checks escort or guard coverage.

One gap remains. In BTS, a settler standing on its best site founds *before* the
escort rule. In RoM, founding happens inside `AI_found`, after it. So a settler
whose escort died to a non-capturing attacker (a ship, bombardment or an animal) or
was split off by the danger rule walked home from its reached site. It now founds
when it stands on its accepted site and the site is still legal. The danger check
still runs first, and the escort rule still applies everywhere else. The test covers
all four cases; upstream sends the settler home.

Waiting for an escort before leaving a city is a deliberate safety rule against
RoM's barbarians and animals. Relaxing it for routes entirely inside our own borders
would speed expansion, but it changes risk and needs game evidence first.

## Interaction with agendas, operations and governors

- **Operations.** Operation targets, delivery and reinforcement code is unchanged.
  Operation stacks call `AI_attackCityMove` → `AI_pickTargetCity`, so they benefit
  from the preserved search, and their stacks now stand on the plots `AI_choke`
  actually ranks best while they wait for strength. Assault thresholds
  (`AIDecisionPolicy::assaultThreshold`) are unchanged.
- **Agendas.** No agenda input changes. Unit counts per mission (`AI_unitTargetMissionAIs`,
  `AI_plotTargetMissionAIs`) are identical, except that unreachable non-moving
  groups no longer count as arriving.
- **City governors.** Governors set production probabilities. Worker choice now
  follows the per-turn value that `AI_bestCityBuild` already intended, so governors
  that raise improvement priority get closer improvements first.
- **Save format** is unchanged. The second finder and the indexes hold no saved state.

## Validation

| Check | Result |
|---|---|
| Regression suite (24 programs) | 0 failures ([log](../../fixes/pathing-regression.log)) |
| New tests on unmodified `main` | 13 of 13 fail ([log](../../fixes/pathing-before.log)) |
| Patch application on a fresh clone of `main` | applied tree = tested tree `147f6d1f` ([log](../../fixes/pathing-patch-validation.log)) |
| MSVC 2003 build | 0 errors, 0 warnings, 2,451 exports identical to the shipped DLL |
| clang whole-DLL differential gate | 0 new diagnostics |
| clang `-Wunused-but-set-variable` | both defect warnings resolved, no new ones |

**Not done:** the game executable was not run and no save was replayed.

## In-game acceptance checklist

1. Install [`builds/0010/CvGameCoreDLL.dll`](../../builds/0010/CvGameCoreDLL.dll) with GitLab
   `main`'s files and load an existing save (save format unchanged).
2. In a late-game war, compare turn times against the
   [0009 DLL](../../builds/0009/CvGameCoreDLL.dll) on the same save. Turns with many
   visible enemy cities and large stacks should benefit most.
3. Watch a siege the AI cannot yet win outright: its stack should stand on hills or
   forests next to the city, not on open ground.
4. Watch naval invasions: transports carrying siege units should not join landings on
   unseen cities.
5. With unit logging at level 2, watch a settler whose escort dies at the site: it
   should found the city.

## Backlog

- Profile pathfinding in game, then decide on a per-group admissible heuristic
  (route-aware lower bound) together with an A* that reopens nodes.
- `AI_eventValue` computes war and pillage values for events and never uses them
  (BTS leftover).
- `CvUnit::upgradeAvailable`, the per-candidate path searches in whole-area
  scans, and `AI_techValue`'s full unlock loops (see the
  [turn-time report](../turn-time/README.md#backlog)).
