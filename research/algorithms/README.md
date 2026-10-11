# Algorithms for Rise of Mankind's AI

**Recommendation: combine exact local optimization, bounded strategic search, and
offline learning.** A genetic algorithm, MCTS, or an A* search over entire turns
would not be a good universal replacement for this AI. Different decisions have
different mathematical structure, information, and execution costs.

This study maps algorithms to the [reviewed game flow](../../docs/review/AI_AND_GAME_LOGIC.md),
inspects research implementations, and includes independently checked C++03
experiments. Source references use the original GitLab revision
`1ab4f99a76adb530f86b278390ab8139ef41cc96`; the existing
[correctness patch](../../fixes/README.md) remains separate. No algorithm in this
study has been installed in the DLL. Research pass: 11 October 2026.

## 1. Define what “optimal” means

Three different claims must stay separate:

1. **Exact subproblem solution:** cheapest legal research package under fixed
   costs, or highest-value assignment under an additive cost matrix. These are
   testable against exhaustive small-instance oracles.
2. **Best plan within a model and budget:** a limited combat or economic search
   returns its best evaluated plan. Its quality depends on omitted actions,
   prediction error, evaluation weights, and the opponent model.
3. **Best game policy:** maximizing victory probability against a distribution
   of opponents, maps and hidden states. Neither a local optimum nor an arbitrary
   finite MCTS/GA run proves this. RoM has stochastic combat, hidden information,
   several players, diplomacy, and long-delayed consequences.

Optimize a declared objective. At the empire level, use estimated victory
probability with survival, legality and resource constraints. At subordinate
levels, use calibrated marginal values: time to obtain a capability, expected
unit losses, delivered fighting power, food security or production delivered by
a deadline. Raw production, territory, score and combat kills are proxies that
can conflict with winning. Emergency constraints should not disappear merely
because an evaluator offers enough compensating points.

The source's base XML contains **308 technologies, 373 unit types, 389 buildings,
68 civics and 8 civic categories**. These are inspected base-file counts, not
the effective modular runtime registry. Full search over these tables is the
wrong starting point. Build relevant local candidate sets from effective rules
and the current state, and record what was excluded.

## 2. Recommended algorithms by decision

In the table, `C` means the cost of constructing/evaluating one candidate or
simulating one transition; it is not assumed constant in the game. Definitions
and important qualifications follow below.

| Decision and source entry | First choice | Why it fits | Principal cost and guarantee |
|---|---|---|---|
| Research: `AI_bestTech`, `AI_cachedTechPathLength` | Deduplicated prerequisite closure for AND-only graphs; exact subset DP for small mixed graphs; bounded best-first search for larger graphs | Shared prerequisites make independent scalar branch costs inaccurate | AND-only `O(k+e)`; dense subset DP `O(k 2^k)` time, `O(2^k)` memory; exact only for the represented fixed-cost problem |
| Worker/escort/reinforcement allocation | Dense assignment or sparse min-cost flow after legality filtering | Stops several units independently consuming the same attractive task | Dense matching `O(n^3)`; cost construction/path queries are additional; exact for separable assignment with represented capacities |
| Citizen assignment: `AI_assignWorkingPlots`, `AI_juggleCitizens` | Bounded integer/DP allocation plus local exchanges | Citizens compete for plot/specialist slots under food and capacity constraints | A cardinality/food DP can cost `O(J P F)`; more state dimensions multiply this; exact only for included effects |
| Production and gold hurry: `AI_chooseProduction`, `AI_goldHurryScore` | Shortlist, deadline-aware rolling-horizon beam search; knapsack-style allocation for shared gold | Build order, shared treasury and unit delivery deadlines couple decisions | Beam `O(H W B (C + log(WB)))` with sorting; one-resource integer DP `O(NG)` is pseudo-polynomial |
| Civics: `AI_doCivics` | Exact enumeration of a small legal shortlist, then bounded branch-and-bound | Category-wise best choices miss package interactions and joint switching cost | `O((product r_j) C_package)` without pruning; complete enumeration gives an exact shortlist optimum |
| Military operations: `AI_updateMilitaryOperations`, `AI_operationMove` | Existing operation state machine with hierarchical task decomposition and bounded maneuver search | Assembly, transport, siege and recovery require different legal actions and resources | Method selection can be cheap; general task planning is still combinatorial; cap candidates and expansions |
| Movement: host A* through `generatePath` | Retain native semantics; reduce redundant queries and cache correctly first | Arrival time, remaining moves, domain, danger, diplomacy and group composition affect the path | Dijkstra/consistent-A* on an explicit graph: `O((V+E) log V)` with a binary heap; graph-state size and callback cost matter |
| Repeated route repair | D* Lite/LPA* or AD* only after measured reuse; HPA* only after map abstraction validation | Can reuse work when a similar query changes locally | No universal per-query speedup; incremental maintenance can approach a fresh search or cost more |
| Tactical attack/retreat ordering | Exact combat probabilities for supported slices, then bounded expectimax/MCTS | Defender choice, collateral and remaining attackers make order matter | Expectation trees remain exponential; sampled search costs simulations × rollout work, without a finite-budget optimality guarantee |
| Settlement: `AI_foundValue` and settlers | Existing fast scorer, diversity-aware shortlist, then short economic rollouts/local search | Multiple settlements compete for land, workers and maintenance budget | Single-site scan `O(M C)`; selecting interacting sites becomes combinatorial |
| Diplomacy: `AI_considerOffer`, `AI_counterPropose`, `AI_doDiplo` | Preserve hard denials, then bounded offer-bundle search with an opponent model | A mutually valuable bundle differs from a unilateral score maximum | General bundles `O(2^q C)`; additive bounded integer formulations admit cheaper DP |
| Strategic weights and evaluation | Offline CMA-ES or other evolutionary search; constrained NSGA-II for explicit multiple objectives; supervised value/ranking models | Expensive experimentation can improve a cheap deployed evaluator | Training is dominated by campaign evaluations; inference can be `O(d)` for a linear model |

The matching and flow recommendations are supported by inspected OR-Tools
implementations [R1–R3]. Those modern implementations are references, not libraries
to link into Visual C++ 2003 unchanged. The lab supplies an independent small
legacy-style matching implementation, not a port of OR-Tools.

## 3. Research planning: the highest-priority algorithm correction

### The actual integration problem

The [current helper](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayerAI.cpp#L5170)
sums memoized AND costs and the cheapest OR cost. Memoization saves computation
but does not eliminate duplicated prerequisite work. `AI_bestTech` uses the
step count for admission and the cost for completion-time adjustment.
[AI_chooseResearch](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayerAI.cpp#L7239)
currently chooses depth **6 in the ancient era and 3 later**, with special
cultural/human cases. A replacement must preserve a defined horizon rather than
silently equate cheapness with a short path.

There is a second integration point:
[CvPlayer::pushResearch](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayer.cpp#L14661)
constructs a queue using its own recursive OR selection. Fixing the evaluator
alone need not cause the evaluated package to be executed. Carry the chosen
legal package/order into queue construction, or deliberately execute its next
currently legal technology and replan on completion. Test the queue and its
callbacks, not just the estimated cost. Coordinate with shared team research
and the Python choice override.

### Why simply using sets is insufficient

The base-XML Chariotry fixture has three unknown technologies costing
`50 + 48 + 120 = 218`; the current recursive estimate returns `268` by counting
Animal Husbandry twice. Set union fixes that example.

However, suppose two required intermediate technologies each cost 1. The first
can use prerequisite A (cost 6) or B (cost 4); the second can use A (6) or C (4).
The goal costs 1 and requires both intermediates. Independent local choices
select B and C for total **11**. Sharing A produces total **9**. Deduplicating
the two locally selected packages still returns 11.

The lab verifies both examples. Consequently:

* Keep alternative packages until their interactions are resolved.
* Do not discard a package solely because its standalone cost is larger. Its
  included technologies may satisfy another branch. Sound dominance needs the
  relevant future state/inclusions, not just a scalar cost.
* General shared AND/OR package selection is NP-hard. A simple reduction is set
  cover: purchasable root technologies represent sets; each element technology
  has an OR over the sets covering it; the goal requires all elements. Minimizing
  distinct purchased roots is minimum set cover. This is a complexity argument
  about the generalized model, not a claim that every RoM instance is hard.

### Practical solver design

Normalize an actor-specific graph using effective rules. Already owned techs
satisfy prerequisites; queued techs are commitments, not automatically completed
capabilities. Retain partial research, legality and team state. If any OR
prerequisite is owned, that OR group is satisfied. Never remove unknown
prerequisites simply because a candidate cap was reached: report approximation
or unsupported scope instead.

For `k` remaining relevant technologies, a state is the subset `S` completed by
the proposed plan. A technology is available when all its AND prerequisites and
at least one required OR prerequisite are satisfied. Transition to `S union {t}`
and charge `t` once. Under frozen nonnegative costs, this is an acyclic subset
state graph. The [lab](lab.cpp) implements dense DP, reconstructs a legal order,
and checks it against an independent subset/fixed-point oracle.

Use these paths in production:

1. Detect an AND-only remaining closure and compute its distinct cost and count
   in linear graph time. Do not pay an exponential cost for a tree/DAG that only
   needs a visited set. Validate references and reject unsatisfied mandatory
   cycles; a cheap set without a legal research order is not a feasible package.
2. For genuinely small mixed closures, use exact DP or best-first subset search.
   Starting a prototype with `k <= 16` is a reasonable **experimental limit**,
   not a measured engine budget. If the objective includes a maximum number of
   steps, enforce it within the search; the cheapest unrestricted package may
   violate the horizon.
3. For larger closures, run bounded best-first search with a legal incumbent,
   sparse state storage and a deterministic expansion cap. An admissible cost
   lower bound can sum distinct still-missing mandatory AND ancestors while
   ignoring additional optional-branch costs. A zero lower bound is safe but
   weaker. Do not sum overlapping independent estimates.
4. Revalidate the first action after a technology trade, war/economic change,
   altered research modifiers or Python intervention. Cache immutable structure
   separately from actor-dependent costs and legal state.

Frozen beaker cost is only one objective. Minimizing turns with partial progress,
rate changes, discounts and useful intermediate unlocks needs a richer state or
a rolling-horizon model. The lab intentionally does not model those effects.
Likewise, a cost frontier and a depth frontier cannot be combined arbitrarily
as though they describe the same research package.

## 4. Coordinating units: assignment and flow before population search

The native code has separate worker, reinforcement, transport and role decisions.
When several agents compete for tasks, independent greedy choices can lose value
even if every local evaluator is correct. The lab's two-unit utility matrix is:

| | Task A | Task B |
|---|---:|---:|
| Unit 1 | 10 | 9 |
| Unit 2 | 9 | 0 |

Unit 1 taking A first yields total 10. Joint assignment chooses Unit 1→B and
Unit 2→A for 18. Dense Hungarian-style assignment finds an exact optimum for
this additive model in `O(n^3)` time, with `O(n^2)` matrix storage and `O(n)`
auxiliary storage. Pad a rectangular problem appropriately and include explicit
idle alternatives; a solver must not force a harmful assignment.

For several interchangeable slots in a task/role, use a min-cost-flow network.
A successive-shortest-augmenting-path implementation with integral flow `F`,
potentials and a binary heap costs roughly `O(VE + F E log V)` when an initial
Bellman–Ford pass is needed for negative costs. Other flow implementations have
different bounds: the inspected cost-scaling OR-Tools solver documents
`O(V^2 E log(VCmax))` [R2]. Do not mix their complexity claims.

Limits of the reduction matter. Multiple workers accelerating one improvement,
army composition bonuses, unsplittable cargo sizes, geographic task interference
and sequencing are not all additive flow costs. Use explicit capacity/composition
constraints or a higher-level plan; otherwise the solver optimizes a simplified
problem that can still produce a bad army.

The expensive step may be building edges. With 100 units and 300 tasks, an
unfiltered matrix requests 30,000 unit/task evaluations, potentially including
30,000 paths. Region/domain filters, reusable distance fields for truly identical
movement profiles, and bounded candidate lists can reduce this dramatically.
An exact assignment over a pruned graph is exact **only over that graph**.
Measure missed opportunity against wider small-instance graphs.

Keep existing valid missions as candidates, include a switch penalty, reserve
tasks, and commit assignments in stable native-ID order. Revalidate each mission
against the live world: earlier movement or callbacks may invalidate a later
assignment. Do not rerun a global allocator on every unit's update call.

## 5. Economy, production, civics and settlement

### Citizen allocation

Start from job slots: workable plots and legal specialist capacities. For an
additive objective without coupling, sorting marginal values may be enough.
Food, population, specialist caps and nonlinear thresholds turn this into a
constrained integer problem. A DP over job index `J`, assigned population `P`
and a bounded food balance `F` can be exact for that abstraction in `O(J P F)`
time; rolling layers reduce memory to `O(P F)`. Handle signed food balances
explicitly. Great-person thresholds, happiness, growth and multi-turn starvation
can require additional dimensions or a short simulator.

The existing [citizen assignment](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvCityAI.cpp#L244)
and [juggling](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvCityAI.cpp#L10111)
are useful baselines. Compare the current result to an exact small-city oracle
before replacing the algorithm. A bounded one/two-job exchange is a sensible
large-city fallback; it is a local optimum, not an exact allocation guarantee.

### Production and shared treasury

Use a rolling horizon: propose a few meaningful build/hurry choices, simulate
their economic effects for a short horizon, choose a plan, execute the first
decision, then replan at a meaningful event. Beam width `W`, branching `B` and
horizon `H` give about `H W B` candidate transitions. Heap/sorting overhead is
additional, and simulation cost will dominate if every candidate scans the empire.

Preserve the incumbent build and emergencies in the candidate set. Include time
to delivery, overflow, anarchy, maintenance, workers needed to realize an unlock,
and transport availability. A unit finishing after a war's decisive window is
not equivalent to one delivered in time.

Gold-hurry choices can start as a multiple-choice knapsack: at most one immediate
choice per city, a shared treasury budget and a reserve. Integer-budget DP is
pseudo-polynomial, not polynomial in the number of input bits. Rounding budgets
changes guarantees; choose conservative feasibility rounding and measure regret.
Successive purchases and production completions can change later choices, so
recompute after committed effects. Use a richer beam only where this coupling
actually changes decisions. Knapsack/branch-and-bound references are in [R3].

### Civic packages

[AI_doCivics](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayerAI.cpp#L16681)
scores candidates separately, reduces by category, then tests the selected
package against anarchy/horizon thresholds. It does not optimize every joint
combination. There are eight base categories: retaining three candidates each
means 6,561 packages; four means 65,536. Whether this is affordable depends on
the package evaluator, not just the small-looking category count.

Keep current and legally important choices; build a pure package evaluator from
an empire snapshot and deltas. Reusing scores computed against the old package
does not capture cross-category interactions. Enumerate small shortlists exactly;
for larger ones use branch-and-bound with a genuinely optimistic bound, then
retain the best feasible incumbent when capped. Include joint legality, anarchy,
cooldowns, recurring costs and changed economic rates. Do not mutate the live
player through speculative revolutions.

### Settlement

The current settlement scorer and its training tools offer a natural learned
ranking baseline. Improve the shortlist with geography, access, maintenance,
workers, defense and overlapping catchments, then use short economic rollouts
for close candidates. Choosing several interacting sites resembles constrained
facility-location/set-packing problems; sorting independent city values is not
an exact multi-site optimum. Local swaps and small beams are easier to budget
than a broad online GA over all possible city locations.

## 6. Military planning, combat and pathfinding

### Use the existing hierarchy

Keep the existing separation between team war planning, player agenda,
operations, groups and unit roles. Model operation methods such as assemble,
stage, transport, land, besiege, assault and recover. Hierarchical task planning
provides useful domain structure; it does not make arbitrary plan search cheap.

At operation review, compare a few alternatives: reinforce, switch target,
wait for siege, embark, attack or withdraw. Carry supply, capturers, bombardment,
arrival deadlines and retreat capacity into the evaluation. Preserve the current
plan unless expected improvement exceeds the switching cost. The existing
operation state machine remains the legal execution and recovery mechanism.

### Tactical search

Use exact probabilities/DP for a small supported combat transition when practical,
then search short action sequences. The model must preserve native defender
selection, collateral, first strikes, withdrawal, combat limits and post-combat
effects. Scoring each attack independently misses the value of changing the
next defender or preserving the final capturer.

Alpha–beta is appropriate for deterministic, two-player, perfect-information,
zero-sum abstractions. Its worst case is `O(b^d)`; the familiar roughly
`O(b^(d/2))` best case requires excellent ordering and the appropriate tree.
RoM's stochastic multiplayer campaign is not such a tree. Expectiminimax adds
chance outcomes and can grow faster. The inspected OpenSpiel API explicitly
states these assumptions [R5].

For supported stochastic tactical slices, use bounded MCTS with useful rollout
policies, progressive widening, transpositions and a separate planning RNG.
With `I` simulations and rollout length `L`, an implementation may cost
`O(I [C_clone + L(b + C_step) + C_eval])`; scanning all children, cloning state
and callback execution are not free. Cap a preallocated node arena. Full child
expansion can create `O(I b)` nodes; an `O(I)` claim requires a corresponding
restricted expansion policy.

UCT's asymptotic results do not make a small finite search optimal. A biased or
incorrect simulator can reward a worse policy more confidently. OpenSpiel's
inspected MCTS implementation supports sequential multiplayer/chance games but
explicitly provides no special treatment for imperfect information or non-zero-sum
negotiation [R4]. Do not mistake a max-n backup for coalition reasoning.

Under hidden information, use information-set search or sampled belief scenarios
only after a belief/observation model exists. Avoid choosing different actions
based on hidden facts the same information set cannot distinguish. A future
fair-information policy and compatibility with native AI information access are
separate experiments. Keep a supported deterministic heuristic fallback.

### Pathfinding

First optimize how often the source calls the existing engine pathfinder. The
DLL supplies legality/cost callbacks, but the host implementation controls search
and reuse. A new A* with a plausible heuristic can still disagree on path ties,
arrival turn, residual movement and the end-turn plot.

For an explicit graph with nonnegative costs, Dijkstra is a safe exact baseline.
A* retains an optimality claim only with an appropriate admissible heuristic and
correct reopening/termination rules; a consistent heuristic gives the familiar
graph-search behavior. Expanded states may need movement remaining, domain and
transport context, not merely plot coordinates. Danger penalties can change
what “shortest” means.

Consider further methods only with measurements:

* **HPA*/region abstraction:** useful on large maps and repeated cross-region
  travel, but portal choices and refined paths can be suboptimal. Verify naval
  passages, borders, rail/road costs and changing access.
* **D* Lite/LPA*/AD*:** useful for related queries with localized changes. Shared
  caches across different unit profiles, targets or visibility states need an
  explicit validity argument. Reuse is not automatically cheaper.
* **Weighted A*/ARA*:** a declared path-quality/effort tradeoff. The bound applies
  to the modeled path cost under the algorithm's assumptions and completed search
  conditions, not to game victory. The inspected ARA* implementation maintains
  OPEN/INCONS information and decreases its inflation factor [R6]; copying only
  an inflated heuristic does not reproduce the full anytime algorithm.
* **Jump Point Search:** not a default fit for this weighted, state-dependent
  movement graph. Its usual grid symmetry assumptions need proof before use.

Path caches must include composition/movement profile, flags, starts/goals,
remaining movement and relevant world, visibility and diplomacy epochs. Record
negative queries too. Defer replacement of the host search until captured engine
paths provide a trustworthy comparison set.

## 7. Diplomacy, uncertainty, and learning

Preserve source legality and denials before optimization. Optimize offer bundles
for the proposing player's objective subject to predicted acceptance and treaty
constraints. Maintain separate estimates for each party's valuation. An opponent
model can learn contact/acceptance behavior, but acceptance predictions are not
legal guarantees and human responses must remain explicit decisions.

Use bounded enumeration or branch-and-bound for small bundles; additive
approximations can support integer DP. Technologies, resources, peace, vassalage
and war commitments have different temporal and strategic effects. Recurrent
payments cannot be treated as interchangeable immediate gold without the source
conversion rules and cancellation horizon. General negotiation and coalition
formation are not solved by a bilateral zero-sum minimax.

Contextual bandits may help choose among already safe strategies or allocate
offline experiments. Stationary-bandit regret claims do not transfer directly
to a changing diplomatic world with delayed, confounded rewards. Begin with
supervised ranking/value prediction and calibrated uncertainty; adapt online
only where rewards and update cadence have a clear meaning.

## 8. Where genetic algorithms and CMA-ES belong

**Use evolutionary computation primarily to train a cheap evaluator offline.**
The source already has explicit weights, policy functions, agenda parameters and
settlement training infrastructure. These are natural parameterizations.

* **CMA-ES:** a strong candidate for modest-dimensional continuous policy weights
  with interactions and noisy campaign fitness. The authors' implementation
  documents covariance adaptation, bounds, constraints and noise handling [R7].
  Dense covariance storage is `O(d^2)`; sampling/rank updates are quadratic per
  relevant operation and periodic dense eigendecomposition is `O(d^3)`. Diagonal
  or limited-memory variants change both cost and search behavior.
* **Genetic algorithms/memetic search:** useful for discrete plan templates,
  mixed rule choices or build-order chromosomes. Repair/validate legality after
  crossover and mutation. Combine with local improvement where useful. Population
  `P`, chromosome size `d`, generations `G` and evaluation cost `C_fit` imply at
  least about `O(G P (d + C_fit))` for ordinary operators; custom selection and
  repair can add more. A finite run offers no global optimum guarantee.
* **NSGA-II:** useful when the product genuinely wants a Pareto set, such as
  strength versus compute cost versus fragility. Classic nondominated sorting
  is `O(M P^2)` per generation for `M` objectives, plus fitness evaluations.
  The inspected implementation uses ranking, crowding, constraint-aware
  tournaments, crossover and mutation [R8]. Choose a deployment tradeoff from
  held-out results rather than hiding it inside arbitrary weights.

The dominant cost is usually simulation: evaluating `P` candidates on `R`
scenarios over `T` turns costs approximately `P R T C_turn` each generation.
Cheap algebraic fitness can optimize its own blind spots. Do not claim policy
strength from it until engine-backed outcomes support the model.

An online GA for a very small, expensive combinatorial subproblem remains an
experiment, not a forbidden option. Compare it against enumeration, DP, beam
search and local search at equal total transition budgets. It earns deployment
only if measured solution quality outweighs its stochastic variance, repair cost
and latency. For routine unit assignment and small civic packages, exact methods
are much easier to justify.

Training protocol:

1. Freeze game/rules identity, observation access, parameter ranges and objectives.
2. Split maps/scenarios by lineage, era, geography, civilization and opponent;
   reserve an untouched final evaluation set.
3. Compare paired scenarios and seeds, but do not replay mismatched RNG requests
   after policies branch. Report unsupported/crashed runs alongside outcomes.
4. Evaluate against several fixed opponents and past policy versions, not only
   self-play. Rotate player positions and map advantages.
5. Report confidence intervals, runtime distributions and failure modes. Account
   for repeated selection on validation data; a lucky best seed is not evidence.
6. Export bounded weights or a compact model to deterministic C++ inference.
   Training can use modern tooling outside the legacy DLL; inference need not.

## 9. C++03 integration and turn-time control

The [Makefile](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/Makefile#L2)
names Visual C++ Toolkit 2003 and links Boost 1.32/Python 2.4. A GCC
`-std=c++03` check helps, but does not establish VC7.1 compatibility or the
Windows DLL ABI. Current OR-Tools/OpenSpiel interfaces use newer C++ features.

Keep `Cv*` classes responsible for world access and effects. Put algorithms in
small policy modules operating on immutable, typed snapshots and caller-owned
scratch storage. This fits the existing `AI*Policy.h` pattern. A solver returns
an action/plan plus evidence; it must not call `revolution`, push missions, draw
game RNG or dispatch Python while evaluating hypothetical branches.

```mermaid
flowchart LR
    A[Native phase and event] --> B[Legal candidates and immutable snapshot]
    B --> C[Agenda and operation planning]
    C --> D[Exact or bounded allocation]
    D --> E[Tactical choice and path service]
    E --> F[Revalidate and commit first action]
    F --> G[Native and Python effects]
    G --> H[Observed outcome and cache invalidation]
    H --> B
```

This is a decision pipeline, not a replacement turn scheduler. In this source,
sequential economic settlement occurs on deactivation; simultaneous-player
settlement occurs on activation. Insert work at the existing phase and honor
initial-turn guards and synchronous callbacks. Replanning after a meaningful
change should not imply rescanning the whole empire in every unit call.

Implementation rules:

* Use dense local indices, contiguous `std::vector` storage, `reserve`, reusable
  heaps and explicit work queues. Map back to owner/full native entity IDs before
  committing; never replace generation-aware handles with array indices.
* Prefer straightforward templates/functions and POD-like snapshots over a large
  solver class hierarchy. Keep engine queries outside inner loops. Avoid
  allocation per node, recursive deep searches and repeated `std::map` lookups
  where compact IDs suffice. Profile before micro-optimizing.
* Use explicit-width intent and the existing compiler's wide integer convention.
  Check multiplication, accumulation, infinity sentinels, shifts and narrowing.
  Saturating a utility may change rankings; use saturation only where its meaning
  is declared. Signed overflow is not a deterministic arithmetic policy.
* Preserve stable candidate ordering and tie rules. Standard containers and
  iteration choices must not inject address-dependent behavior. If a selected
  algorithm needs floating point, audit cross-build determinism and tie handling;
  fixed-point comparisons are often simpler in synchronized decisions.
* Give planning its own reproducible random stream derived from serialized run,
  actor and decision identity. Merely “not using gameplay RNG” is insufficient if
  planning randomness is seeded by wall time or consumes a shared unsaved stream.
* Do not stop synchronized planning based on elapsed milliseconds. Different
  machines can choose different actions. Use deterministic expansion/evaluation
  quotas; use wall-clock measurements to tune those quotas and detect regressions.
* Default to one game thread. Existing globals, host pathfinder reuse, Python and
  mutable caches are not demonstrated thread-safe. Parallelize independent
  offline games first. Worker threads would need immutable snapshots, no engine
  calls and a deterministic reduction/commit order.

Each search result should distinguish `Exact`, `FeasibleBudgetLimited`,
`InfeasibleProven` and `Unsupported`. Include objective/scope, explored-state count,
incumbent value, and a valid bound/gap when available. Exhausting a budget does
not prove infeasibility. A beam's best retained node is not a certified bound
on discarded alternatives. Retain a validated fallback for interruptions.

Allocate budgets by event importance and reuse: cheap legality/forced actions
first, ordinary role decisions next, then major civic/research/war choices.
Count actual expensive operations separately: path requests, node expansions,
state copies, city evaluations and Python callbacks. Measure per-player and
whole-turn median/p95/p99 on large late-game saves. No universal millisecond target
can be justified without that engine profile.

## 10. What the C++03 experiments establish

Run:

```sh
python3 research/algorithms/run_lab.py --source /path/to/rise-of-mankind
```

`--source` additionally verifies the real technology XML against its recorded
hash. Without it, the recorded fixture remains an explicit input assumption.
The runner compiles one UBSan validation binary and one optimized measurement
binary. It checks 300 small research instances against an independent subset
oracle and 160 assignment matrices against exhaustive permutations, plus
zero-cost/cycle/overflow/tie and constructed counterexample cases.

The [recorded results](results.json) show:

| Experiment | Observation |
|---|---|
| Base-XML research diamond | Recursive scalar estimate 268; exact distinct package 218 |
| Shared OR counterexample | Independent branch choices 11; joint package optimum 9 |
| Two-unit assignment | Greedy utility 10; exact assignment utility 18 |
| Research oracle, `k=16` | 65,536 scanned states, 524,288 candidate checks, 768 KiB of DP tables |
| Research oracle, `k=20` | 1,048,576 scanned states, 10,485,760 candidate checks, 12 MiB of DP tables |
| Dense assignment, `n=128` | 101,715 scanned edges for this fixture; 64 KiB input matrix |

On this Linux/GCC instance, median measured CPU times were approximately
**1.82 ms** and **30.63 ms** for those two dense research stresses, and **0.41 ms**
for the 128×128 assignment. Seven measurements follow one warmup. These exclude
world snapshots, pathfinding and game simulation, and are not Windows turn-time
predictions. Matrix construction is outside the assignment timing; allocations
inside each solver are included.

The research timing fixture deliberately stresses dense table scanning on a
pure-AND graph. A production implementation should solve that graph with the
linear closure fast path. It demonstrates the cost of using a generic exponential
oracle indiscriminately, not the expected cost of typical research choices.
Random dense assignment timing likewise does not establish its cubic worst case.

## 11. Implementation order and acceptance gates

1. **Measure before broad replacement.** Add phase/candidate/path counters and
   comparison traces; verify instrumentation leaves decisions and RNG unchanged.
   Collect effective-rule and representative late-game state exports.
2. **Research-package planner.** Implement normalized closures, linear fast path,
   bounded exact search and explicit queue integration. Compare to exhaustive
   small graphs, the diamond/shared-OR cases, horizon limits and real research
   queues. Include trade, partial progress, team and override cases.
3. **Joint task assignment.** Begin with one separable domain, such as workers
   choosing independent single-worker jobs in one region. Compare to the current
   AI at equal path budgets; test idling, ties, invalidated tasks and scarce roles.
4. **Economic package experiments.** Exact civic shortlists and small-city
   allocation oracles come before a large economic planner. Add rolling-horizon
   production only when its transition model reproduces the relevant accounting.
5. **Operation/tactical search.** Add a small set of macro-actions, then tactical
   rollouts after movement/combat/callback slices match engine traces. Compare
   against simpler heuristics at equal transition budgets.
6. **Offline training.** Use CMA-ES/GA/NSGA-II only after reliable scenario
   execution and held-out evaluation exist. Deploy compact inference and retain
   regression fixtures for every learned-policy failure.

These algorithms are candidates for stronger decisions, not a proof that one
configuration will dominate all opponents. The most valuable near-term work is
research-package correctness and coordinated allocation. Large search or evolution
should follow a trustworthy simulator and measured engine costs.

## 12. Research sources and access limits

The [source ledger](sources.json) records inspected upstream commits, URLs and
content hashes. The references below are **implementation documentation/code
actually retrieved and inspected**. Mathematical bounds not asserted by those
implementations are stated as algorithm analysis for the particular formulation
used here; laboratory results are identified separately.

* **[R1] Google OR-Tools, linear assignment:** cost-scaling assignment, integral
  costs, feasibility, complexity and references to Goldberg–Kennedy (1995).
  [Inspected source](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/graph/linear_assignment.h).
* **[R2] Google OR-Tools, min-cost flow:** model, potentials, feasibility and
  cost-scaling complexity; references to Goldberg–Tarjan (1990).
  [Inspected source](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/graph/min_cost_flow.h).
* **[R3] Google OR-Tools, knapsack:** integer DP and branch-and-bound alternatives.
  [Inspected source](https://github.com/google/or-tools/blob/100f66e6242ab8bf8d32feb8f3bf086db66ae2b5/ortools/algorithms/knapsack_solver.h).
* **[R4] OpenSpiel, MCTS and algorithm catalog:** simulation/evaluation interface,
  UCT/PUCT, max-n backups and information assumptions. The catalog points to
  Kocsis–Szepesvári (2006), MCTS survey literature and information-set MCTS.
  [Implementation](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/algorithms/mcts.h),
  [catalog](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/docs/algorithms.md).
* **[R5] OpenSpiel, minimax/expectiminimax:** explicit deterministic/stochastic,
  two-player, perfect-information, zero-sum contracts.
  [Inspected source](https://github.com/google-deepmind/open_spiel/blob/48401890ee9857e611678302371378175a8e4c6b/open_spiel/algorithms/minimax.h).
* **[R6] Search-Based Planning Library, Maxim Likhachev and contributors:**
  ARA*/AD* implementation, heuristic inflation and reuse machinery.
  [ARA* header](https://github.com/sbpl/sbpl/blob/4d654845aa3b92aa1b4282a342e9011bac95aeb9/src/include/sbpl/planners/araplanner.h),
  [implementation](https://github.com/sbpl/sbpl/blob/4d654845aa3b92aa1b4282a342e9011bac95aeb9/src/planners/araplanner.cpp),
  [AD*](https://github.com/sbpl/sbpl/blob/4d654845aa3b92aa1b4282a342e9011bac95aeb9/src/planners/adplanner.cpp).
* **[R7] CMA-ES/pycma, Nikolaus Hansen and contributors:** optimization scope,
  covariance adaptation, constraints, noise and implementation.
  [README](https://github.com/CMA-ES/pycma/blob/48a821b166eceef544847a0b9b66113ac26f1530/README.md),
  [strategy implementation](https://github.com/CMA-ES/pycma/blob/48a821b166eceef544847a0b9b66113ac26f1530/cma/evolution_strategy.py).
* **[R8] pymoo, NSGA-II:** rank/crowding survival, constraint-aware selection and
  variation operators.
  [Inspected source](https://github.com/anyoptimization/pymoo/blob/23110c155aa8f31b5f1b86928227fb3931ba7f00/pymoo/algorithms/moo/nsga2.py).

Direct retrieval of the CMA-ES tutorial on arXiv, the Essex MCTS survey, Koenig's
D* Lite paper, the UCT author-hosted paper and the Alberta HPA* paper was blocked
by the environment's network policy. Their full texts were not inspected in
this pass. This is a source-grounded engineering study with an explicit literature
access limit, not a claimed exhaustive academic survey.
