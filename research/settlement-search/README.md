# Joint settlement destination and delivery search

This replaces the premature destination shortlist in patch 0006. The cumulative
publication targets GitLab `6222511c1a81649445fa69e8ca6dca79cf60c975` and includes
patch 0006's scoring and transport-entry corrections.

## Implemented behavior

A real settler no longer chooses among the two-to-six sites selected to estimate
empire production demand. The player retains every revealed site above its
existing minimum settlement threshold, with its independent found value captured
**before** hypothetical portfolio cities suppress nearby alternatives. That
production portfolio still serves production planning; increasing the movement
candidate pool does not increase its settler-demand count.

Both shore parties and loaded transports search the complete snapshot. A shore
party compares walking and available ferries for each destination. An island can
win even if the best walking destination is inland. The ferry query uses boats
at the current friendly port, checks assignments, capacity and every party
member's boarding/landing eligibility, and includes boarding and landing time.
The query does not load units or issue missions. Only the selected job does so.

Loaded carriers compare their sea delivery with unloading and walking. When an
escort is already aboard, its group joins the settler before the land path query,
so the query uses the party's movement capabilities. Actual FOUND reservations
exclude conflicting destinations within the XML minimum city range, replacing
the loaded carrier's fixed four-tile exclusion.

The old `preferSeaSettlement` policy and its overseas/local ratio threshold are
removed. They compared geography and naval priority before a concrete route was
known. Other naval-priority consumers, including capacity provisioning, remain.

`AI_settleMove` no longer founds immediately just because its current tile is on
the production shortlist, scraps a settler because that shortlist is empty, or
loads it using that preference ratio before the joint search. Initial founding
for a civilization with no city and existing immediate-danger responses remain.

Accepted land jobs are revalidated and continued. This includes a concrete land
job assigned by a ship unloading a party. Ordinary passenger update order cannot
reselect a different site merely because another score changes. A failed legality,
reservation or safe-path check returns the party to destination search. Sea jobs
retain the preceding dispatcher's commitment validation.

## Search algorithm and C++ cost

Candidates are sorted by independent site value, descending, with plot index as
a deterministic tie breaker. For each legal, unreserved candidate, the planner
queries feasible routes and computes the existing shared delivery utility:

```
U = floor(100 * foundValue / (100 + turnDiscount * deliveryTurns))
turnDiscount = 24 - floor(12 * logisticsPriority / 1000)
```

`deliveryValue` clamps its inputs and uses a wide intermediate product. Therefore
`U <= foundValue`. Once the next independent value cannot beat the best feasible
route utility, every remaining candidate is safely pruned. Unreachable sites do
not establish an incumbent and cannot prune reachable alternatives. There is no
fixed top-K or path-query cutoff that can silently discard the winner.

This is branch-and-bound over the existing utility, not a genetic algorithm.
Fresh searches maximize that utility over the eligible snapshot and supported
routes. Ties are deterministic; within a shore candidate, walking wins a utility
tie. A loaded carrier keeps the previous dispatcher's walking tie rule. Existing
commitments are deliberately continued rather than globally reoptimized each turn.

For P map plots and C eligible candidates, snapshot construction adds O(P + C log C)
time and O(C) transient memory to the normal found-value refresh. Each entry has
two integers. There is no persistent plan table, new save field, RNG draw, or
new XML setting. Read/reset clear the snapshot; the existing cache-invalid marker
forces reconstruction after loading an old save.

Let A be one native path query's cost and B the number of eligible local hulls.
A fresh shore search has worst-case O(C * (1 + 8B) * A), plus port/party and
reservation scans. A loaded search has at most C land and 8C water-approach
queries. The selected shore ferry is queried again before boarding to revalidate
it. Bound pruning reduces calls once a good route is known; it does not guarantee
a constant budget. Valid land commitments need one path query; sea commitments
need at most eight approach queries. Actual runtime on large BTS maps still needs
measurement. `SETTLEMENT_SEARCH` logs candidate counts, examined candidates and
winning utility without re-running the scorer or consuming RNG.

## Executed validation

`Tools/test_settlement_search.py` compiles production search and snapshot code
using C++03, warnings as errors and fatal undefined-behavior sanitization.

- 1,000 route-table fixtures compare the shore planner with an independent
  exhaustive oracle, including blocked, illegal and over-horizon destinations.
- Twelve higher-value unreachable sites cannot hide a lower-value reachable site.
- A lower raw-value island with better delivery wins; a better walking route wins
  when a boat is available. Both shore and loaded entry points are exercised.
- Bound pruning follows a feasible incumbent. A valid commitment bypasses a new
  search; invalidating that destination triggers replanning.
- Portfolio mutation cannot erase the independent candidate snapshot. Unrevealed
  and below-threshold plots are excluded; snapshot data is not serialized.
- The existing ferry fixture executes the extracted transport query and boarding
  code, including a check that query-only evaluation has no boarding side effects.

A production-fragment comparison with patch 0006 reproduces the ordering failure:
land site 1000 / 15 turns scores 270; island 900 / 3 delivery turns scores 584.
The previous function selects land; the new function selects the island.
All 22 isolated regression programs pass.

These adapters supply path and mission answers; they do not reproduce the closed
BTS pathfinder or execute a DLL. No in-game replay is claimed. The independent
oracle covers the stated utility, not the entire strategic value of a city.

## Scope of the objective

The premature-shortlist and land-first sequencing weaknesses are removed from
actual settler route selection. The underlying independent found value still
uses the game's tile/resource heuristics, with patch 0006's corrections. This
change does not implement the separate population, worker, technology and
maintenance rollout described in the settlement assessment. It also does not
add distant ship rendezvous or beach-to-inland multimodal paths. Those are not
silently treated as supported alternatives or as proven economically optimal.

[Apply the verified patch](../../fixes/README.md#joint-settlement-search).
[Regression output](../../fixes/joint-settlement-regression.log) ·
[Before/after counterexample](../../fixes/joint-settlement-before.log) ·
[Manifest](../../fixes/joint-settlement-manifest.json).
