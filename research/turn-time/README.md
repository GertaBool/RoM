# Turn time, research planning and compiler-found defects

This is the investigation behind [patch 0009](../../fixes/0009-turn-time-and-research-planning.patch).
It targets GitLab **`d8cedd551212c9a769230d66c219860c901798dd`**, which already contains
patch 0008's runtime change. The patch has landed on GitLab `main` as
[merge request !34](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/34)
(merge commit `a9b1fce`). Its tree `e3cbb9a8` is byte-identical to the tested tree.

The work had three goals, in this order: fix defects and reduce time complexity,
improve the AI opponents, and add a fitting feature. All three are covered below,
along with how each change interacts with agendas, operations and city governors.

## Building the real DLL

Previous rounds tested source fragments only. This round builds the whole
`CvGameCoreDLL.dll` with the compiler the game requires. The toolchain is
**Visual C++ Toolkit 2003** (`cl` 13.10.3077) with the **Platform SDK for Windows
Server 2003 SP1**, run under Wine 9.0 in a 32-bit prefix. The build uses the
repository's own `GNUmakefile` with `TARGET=release` and no `_MOD_*` switches,
like the shipped DLL. Neither installer was executed: the toolkit bundle was
unpacked with `innoextract` and the SDK image with `7z` and `msiextract`.
[`toolchain/`](../../toolchain/README.md) has the scripts.

| Build | Source | Errors / warnings | Exports | SHA-256 |
|---|---|---|---|---|
| [baseline](../../builds/d8cedd5-baseline/provenance.json) | unmodified `d8cedd5` | 0 / 0 | 2451, identical to the shipped DLL | `fa948d5d…` |
| [0009](../../builds/0009/provenance.json) | `d8cedd5` + patch 0009 (= GitLab `main`) | 0 / 0 | 2451, identical to the shipped DLL | `e07a920c…` |

The repository's bundled `Assets/CvGameCoreDLL.dll` predates its source, as its owner
confirmed, so it is not used as an oracle. The baseline build serves as the A/B
reference.

A **clang whole-DLL pass** complements MSVC. It compiles all 104 translation units in
MSVC compatibility mode against the SDK's Boost 1.32 and Python 2.4 headers, emulating
MSVC 7.1's legacy `for` scope. It runs bug-finding warnings and reports only
diagnostics that differ between two trees. Patch 0009 resolves 36 diagnostics and
introduces none.

## Defects

Each defect below is a real compile-time finding (clang diagnostics or analyzer) or
came from reading the code those findings led to. `Tools/test_static_findings.py`
pins each one, and all 10 of its checks fail on unmodified upstream.

| Location | Defect | Effect in game |
|---|---|---|
| `CvPlayerAI::AI_executiveValue` | `if (iSpreadExternalValue = 0)` assigns. The competing-corporation loop counts the corporation itself, not its rivals. | A headquarters owner whose own cities are saturated discards the foreign-spread value: executives are undervalued or never trained. Rival saturation was never measured. |
| `CvUnitInfo::write`, `CvCivicInfo::write` | `stream->Write(&m_x)` for 25 Revolution fields. The pointer converts to `bool true`. | The cached info stream writes one constant byte per field, which misaligns every later field for the matching `read`. |
| `CvTeamAI::AI_techTrade` | No Tech Brokering reads `eCurrentResearch`. That is uninitialized, or is our own team's research. | Tech-trade denial depends on garbage or on the wrong team. It now uses the receiver's research. |
| `CvPlayer::applyEvent` | Compares a player's **team** with a player **ID**. | In team games, tech-progress event messages go to the wrong players. |
| `CvUnitAI::AI_pickupStranded` | A transport already at the pickup plot reuses a stale `iPathTurns`, including as a divisor. | Pickup values use another plot's turn count. |
| `CvCityAI::AI_chooseProduction` | Operator precedence: `!bDanger && A \|\| B`. | Mid/late-game cities **in danger** could build production buildings or workers before defenders. |
| `CvGame` start normalization | `(2 + cond) ? 0 : 2` is always 0, so the call is `getSorenRandNum(0)`. | Bad features near starts were always removed instead of with probability 1/2 (no resource) or 1/4 (resource). |
| Logging and text calls | `CvWString` objects passed through `...` | Undefined behavior in `logBBAI` and in the hurry-overflow text. |
| `CyGameTextMgr(CvGameTextMgr*)` | Initializes its member from itself. | The Python text manager wrapper holds garbage. |
| `AI_getStrategicContext` | `AI_totalUnitAIs(UNITAI_SETTLE) + AI_getNumTrainAIUnits(...)` | Settlers in training counted twice, so expansion was believed further along than it was. |

The Python callbacks had rule errors of their own (`Tools/test_python_callbacks.py`):

- The Corporate building discount applied only when Imperium was *not* the leadership civic.
- The Fortification castle discount tested the administration civic option. Fortification is a military civic.
- The Replicators upgrade price halved the AI price four times, skipped Leonardo's modifier and the promotion discount, and returned `None` without the resource.
- The Observatory and Djenne terrain checks scanned a 5×5 square, including corner tiles of a neighbor's radius, instead of the city's own radius.

## Time complexity

### Mission targets per plot

`AI_plotTargetMissionAIs(pPlot, …)` counts units whose group targets a plot within
range. It is called **58 times in `CvUnitAI.cpp`**, mostly inside whole-map or
whole-area plot loops ("is anyone already going there?"). The original body walks
every selection group of the player on every call. With *P* plots and *G* groups,
one whole-map scan costs Θ(*P*·*G*), and each AI unit may run several per turn.

`AIMissionTargetIndex.h` buckets groups by their mission plot:

- **Rebuild** is Θ(*G*) after any change. Buckets carry a stamp, so stale entries are
  ignored without clearing *P* heads. Clearing is Θ(*P*) only when the map size changes.
- **A query** with range *r* visits the (2*r*+1)² plot window when that window has no
  more cells than the index has entries. Otherwise it scans the entries. The cost is
  O(min((2*r*+1)², *G*) + hits·*m*) for *m* requested mission types. Most calls use
  *r* = 0, which is one bucket.
- **A whole-map scan** therefore costs Θ(*P* + *G*) instead of Θ(*P*·*G*).
- **Invalidation** uses a global epoch. It is bumped on every membership insert or
  delete, clear, deserialization, `AI_reset` and every *actual* change of a group's
  mission type or plot. The index is keyed by (player, epoch, plot count). In the
  worst case, a change before every query, each query pays the Θ(*G*) rebuild, which
  is the same order as the old scan. It is never asymptotically worse.

The results are **identical** by construction, and the test checks it. Wrapping and step
distance come verbatim from `CvMap.h`/`CvGameCoreUtils.h`. 240,000 randomized queries
(wrapped and bounded maps, ranges −1…30 including window aliasing, skipped
groups, repeated types, the `NO_MISSIONAI` wildcard) match the original loop.
Source contracts require every mutation of `m_units` or the mission fields to
invalidate first. Nine hand-made mutants of those hooks are caught.

Measured with g++ -O0 on the host, not in game: one whole-map scan of a 144×96 map
with 600 groups took **247.5 ms** with the group walk and **0.82 ms** with the index,
including the rebuild.

### Technology path length

`CvPlayer::findPathLength` recursed into AND prerequisites and the cheapest OR
alternative without memoization. It expands the prerequisite DAG as a tree, so
shared ancestors are counted once per route. On RoM's 308-technology tree, the
deepest target from the opening state makes **1,090,348,606 calls**. The result also
overcounts the queue `pushResearch` actually builds, and the AI rated targets by
that wrong count. The replacement is a plan query (below), polynomial in the
number of technologies. The deepest target is planned in **0.33 ms**.

### Python callbacks

The game calls `getBuildingCostMod` for every building candidate in every city.
For Djenne, the old version walked all of the player's cities on each call,
Θ(*C*) per query and Θ(*C*²·*B*) per full evaluation. It now reads the player's
building-class count, which is constant time. `getUnitCostMod` resolved two info
types by linear search on every call. `cannotConstruct` copied two 83-entry lists
and searched them repeatedly per query. `zCivics.cannotConstructBuilding` resolved
type strings per query. All of these lookups are now resolved once, and each query is
constant time. A randomized check confirms the upgrade-line rewrite agrees with the
original algorithm for every building.

## Research planning

### The problem

To research a target *t*, the queue must contain *t*. For every queued technology, it must
also contain all missing AND prerequisites and **at least one** missing-or-known OR
prerequisite. Minimizing the beakers of such a queue is a **minimum-cost AND/OR
closure**. This is NP-hard: Set Cover reduces to it with one OR node per element
and one AND node requiring all elements. Optimal plans therefore need search,
but RoM's tree is small and narrow enough for exact answers in practice.

### The planner (`ResearchPathPlan.h`)

1. **Forced closure**: the AND-closure of the target plus everything reachable only
   through single-option ORs. Every valid plan contains it.
2. **Two greedy incumbents**: a marginal-cost greedy, and the former `pushResearch`
   rule (AND first, then the OR option with the shortest tree path). Their cheaper
   plan is the starting incumbent, **so no plan is ever dearer than the old rule**.
3. **Branch and bound** over the remaining OR choices, with bitset closures, a node
   budget of 256, and an admissible bound. That bound is the largest, over the
   unresolved OR groups, of the smallest forced marginal cost of an option. A search
   that finishes within budget proves the incumbent optimal.
4. **Emit** an irredundant, prerequisite-first queue. Each entry is the target or a
   prerequisite a later entry uses.

`CvResearchGraph.h` adapts the engine. "Satisfied" means known or already queued,
"researchable" is `canEverResearch`, and cost is `getResearchCost`. `pushResearch`,
`findPathLength` and `AI_bestTech` share one planner, so **the AI values exactly the
queue it will build**. The old code valued a tree count and queued something else.

### Results on the real tree

`Tools/test_research_plan.py` reads `CIV4TechInfos.xml` and plans every target from
300 random reachable research states:

| Measure | Result |
|---|---|
| Plans checked (valid, prerequisite-first, irredundant) | 44,396 |
| Proved optimal by branch and bound | 44,396 (100%) |
| Small cases equal to exhaustive search | 10,420 / 10,420 |
| Old rule fails (unresearchable route) | 0 |
| Old rule dearer / equal / cheaper | 7,159 / 37,237 / 0 |
| Saving where the plan is cheaper | mean 5.5% (≈ 6,000 beakers), max 83% |
| Old tree count below the real queue (unresearchable alternatives) | 63 plans |

## Interaction with agendas, operations and governors

These layers feed back into each other. A change that looks local can be undone or
amplified elsewhere, so each change was traced through every consumer.

**Research choice.** `AI_chooseResearch` calls Python `AI_chooseTech` first. RoM's
`BugGameUtils` default returns `NO_TECH`, and no module overrides it, so
`AI_bestTech` always decides. Its horizon is 6 steps in the ancient era and 3 later
(1 for culture victory). It measures steps with the plan size now:

- **Horizon.** Plan size never exceeds the tree count except in the 63 undercounts.
  A few more targets therefore fall inside the horizon: at depth 3, 5,436 → 5,486
  (+0.9%); at depth 6, 7,806 → 8,343 (+6.9%). These are targets whose prerequisites
  overlap, which the old count double-charged.
- **Path-length gates in `AI_techValue`.** Wonder, project and building bonuses use
  `iPathLength <= 1`. **None of 44,396 decisions changes.** The religion-founding bonus
  uses `<= 2`, and it changes in **11** cases. In each of those, the old count said 2,
  but the queue it would build has 3 or more entries, so the bonus was granted on a
  wrong premise.
- **Cost charge.** The prerequisite-cost charge in `AI_bestTech` now uses the plan's
  true beakers, without double counting.
- **Agenda demand.** `AI_getTechAgendaValue` is computed from the technology's
  unlocks and the agenda's needs, not from path length. Agenda-driven preferences are
  unchanged. They now compete against correctly costed paths.

**Operations and unit AI.** Operations and unit missions read
`AI_plotTargetMissionAIs` counts to avoid piling onto one target. The index returns
the same numbers, so their behavior is unchanged except for speed. Because the epoch
is bumped *before* each mutation, a unit that changes its mission is never
miscounted later in the same turn.

**City governors and the danger fix.** The governor layer adjusts `iBuildUnitProb`:
Castellan +10, Agriculturalist and Scholar −5. The agenda's military budget adjusts
it too. The precedence fix sits after those adjustments and only removes a path by
which an endangered city skipped its defenders. It does not change any probability.
Governors that bias toward defense are now more consistent with the danger branch,
not overridden by it.

**Economy feedback.** `AI_executiveValue` drives the city's corporate-executive
training decision (`CvCityAI.cpp:9620`). Before the fix, a headquarters owner
saturated at home lost all foreign-spread value, because the assignment zeroed it. Now
foreign spread is valued against attitude and open borders, as the original BBAI code
intended. The settler-count fix stops the strategic context from overstating the
settler pipeline, so agenda selection scores expansion from the true number.

**Save compatibility.** No save layout changes. The info-stream fix affects
`CvGlobals::write*InfoArray`, which the executable calls to serialize info arrays.
It is not part of saved games.

## Feature: research plan in technology help

Technology help now shows the queue that selecting the technology will build when
it needs prerequisites. It shows the number of technologies, the remaining beakers
and an estimate in turns at the current rate, for example:

> Research plan: 5 technologies, 4,310 beakers, about 23 turns

It uses the same planner as `pushResearch`, so the hover text, the queue and the AI
all agree. The text is in `Assets/XML/Text/RoM_GameText_ResearchPlan.xml` in all
five shipped languages, with a no-rate variant when research output is zero.

## Validation

| Check | Result |
|---|---|
| Regression suite on the final tree | 21 programs, 0 failures ([log](../../fixes/turn-time-regression.log)) |
| Upstream suite before the patch | 16 programs, 4 failures (stale tests 0008 restores) ([log](../../fixes/turn-time-before.log)) |
| Patch application on a fresh clone | applied tree = tested tree = GitLab `main` tree ([log](../../fixes/turn-time-patch-validation.log)) |
| MSVC 2003 build | 0 errors, 0 warnings; exports identical to the shipped DLL |
| clang whole-DLL gate | 0 new diagnostics, 36 resolved |

GitLab's web API reinterprets files as UTF-8. So that commits could not re-encode
anything, two spellings were changed before landing. The research plan text writes
`ó`/`í` as `&#243;`/`&#237;`. Firaxis's debug font-test string in `CvGameTextMgr.cpp`
writes its Latin-1/cp1252 characters as escapes. A test program compiled with MSVC
2003 shows both spellings produce identical wide strings. The DLL rebuilt from the
final tree differs from the previous build only in the PE and export timestamps
(4 bytes).

**Not done:** the game executable was not run, and no save was replayed. The checks
below need the game.

## In-game acceptance checklist

1. Back up `Assets/CvGameCoreDLL.dll`. Install [`builds/0009/CvGameCoreDLL.dll`](../../builds/0009/CvGameCoreDLL.dll)
   together with GitLab `main`'s Python and XML.
2. Load an existing save. It must load, because the save format is unchanged.
3. Hover a technology three or more steps away. The help should show "Research plan: N
   technologies, …". Select it, and the queue should contain exactly N entries.
4. Play or autoplay 50–100 turns from the same save with the
   [baseline DLL](../../builds/d8cedd5-baseline/CvGameCoreDLL.dll) and with 0009.
   Record turn times. Late-game turns with many units should benefit most.
5. Spot-check the corrected rules: the castle cost under Monarchy and/or Fortification,
   cathedrals while holding Djenne, the Replicators upgrade price, and corporate
   executives trained by a saturated headquarters owner.
6. With BBAI logging on, confirm that research choices and queues look sensible.

## Backlog

- `CvUnit::upgradeAvailable` searches upgrade chains depth-first without a visited set.
  Probing all 262 unit classes can reach 402 calls per query (≈ 2 million class
  checks per broad probe). Memoizing per unit class and turn would make it linear.
- Several unit-AI routines run `generatePath` against every candidate plot in an area.
  A single bounded Dijkstra per unit, or distance pruning, would cut that.
- `AI_techValue` loops over every building (389) and unit (375) for each candidate
  technology. Precomputing per-technology unlock lists at load would make it
  proportional to what the technology actually unlocks.
