# Scheduling lab: executable contract and limits

Run `python3 research/competence/run_lab.py` from the GitHub checkout. Requires Python 3 and g++ with C++03 and UBSan support; uses no Python packages. The runner builds in a temporary directory, executes tests, and writes `results.json` (or `--output PATH`).

This is an original model experiment. It does not import game code, decode a save, instantiate `CvCity`, or certify engine behavior. It isolates prerequisite scheduling, scarce slots and investments that change future production.

## State and transitions

A model has up to eight one-off jobs and a horizon of at most 64 integer turns. A job declares prerequisites, exclusive resource bits, positive effort, either production-work or fixed-duration progress, a production/income gain on completion, a one-off utility reward, and optional income suppression while active. Inputs are bounded and asserted. Prerequisite cycles are allowed as inputs and can correctly make a required package impossible.

At the start of a turn, choose a compatible subset of not-yet-started jobs whose prerequisites are already complete. A city-production slot and separate worker/water-activity slots are examples of resource bits. Slots represent capacity constraints; this model has no spatial movement or unit identities.

During the turn, income is accrued using the previously completed jobs unless an active anarchy job suppresses it. Active jobs consume one fixed-duration unit or the pre-completion production rate. They complete at the turn boundary; rewards, production and income gains then become available. Overflow is discarded. Prerequisites cannot use a completion from later in the same turn.

An optional known deadline requires the declared goal jobs to be complete at that boundary. Without a deadline, required jobs need only finish by the horizon; an empty required mask creates no mandatory defense goal. The terminal objective is accumulated income plus one-off rewards. Equal utility prefers fewer started jobs and then a deterministic state order.

This objective deliberately omits full city value: no food stock, growth, happiness, health, specialists, terrain legality, combat probability, maintenance, technology trading, production modifiers, gold spending, real anarchy rules, loss of units, native callbacks or opponent adaptation. Even the water example's production gain is a supplied model parameter, not a claim about a particular RoM fish tile or XML value.

## Algorithms

The exact solver performs layered forward state-space search. The state key is completed jobs, started jobs and remaining effort. Within one time layer, these determine all future legality, rates and deadlines; retaining the greatest accumulated utility for an identical key is sound because utility is not a spendable resource here. If gold becomes a resource, partial progress decays, or job histories affect rewards, this dominance rule must be reconsidered.

The optional beam ranks states using accrued utility plus current income projected through the horizon, with progress and stable keys as tie breakers. That ranking is a heuristic, **not a bound**. Discarding any state marks the result approximate, even if the final value matches an oracle. A complete goal-first schedule is validated separately and retained as a fallback, so beam pruning cannot discard an already known feasible answer.

Without truncation, finishing the finite horizon establishes the exact model optimum or model infeasibility. With truncation, no returned plan means only that this search and fallback found none. The `exact` flag on the greedy result is false; it never claims optimality.

For J jobs, each retained state enumerates at most `2^J` start subsets and checks O(J) task data. With width W and horizon H, candidate generation costs O(H W 2^J J), with additional ordered-map insertion and sorting costs; key comparisons themselves cost O(J). A conservative bound is O(H W 2^J J log(W 2^J)) time and O(W 2^J J) state storage before beam truncation. The exact solver replaces W with the possibly exponential number of reachable states per layer. This is not a polynomial general scheduling algorithm.

The lab advances one turn at a time so calendar validation stays simple. The proposed DLL planner would skip to relevant completion/rate-change events while preserving intervening accounting. Such event compression has not been implemented or validated here.

## Independent verification

The Python oracle enumerates every absolute job-start calendar, including omitted optional jobs, then replays its resource occupancy and prerequisites. This differs from the native state-space search/deduplication algorithm. For 160 seeded small models and five named cases, it establishes the best feasible utility independently. Returned native start/finish witnesses are replayed as an additional check.

The tests include changing production, concurrent independent slots, shared-slot exclusion, unavailable prerequisites, negative one-off rewards, optional anarchy, defense deadlines and infeasible goals. Additional explicit cycle, zero-gain and monotonic-horizon cases can extend coverage; the existing suite does not claim arbitrary input or engine equivalence.

Compiled validation uses `-std=c++03 -Wall -Wextra -Werror -fsanitize=undefined -fno-sanitize-recover=undefined`. An `-O2` binary measures seven 165-case batches after warmup. Recorded times include process launch, input/output and Python witness checks; they exclude the independent exhaustive oracle calculation and all engine services. Fixed-model timing does not establish a safe turn budget for late-game RoM.
