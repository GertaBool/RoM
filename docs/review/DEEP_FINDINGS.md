# Deeper source findings and their simulation consequences

Update: [tested source patches](../../fixes/README.md) address D01, D02, D03 and D05, plus sparse-city effects and team rollover. D04 remains open. The observations below and their reproduction script deliberately retain the original source baseline.

Reviewed source: `1ab4f99a76adb530f86b278390ab8139ef41cc96`. **The bundled DLL is older than this source. None of these findings was reproduced in that binary or a complete BTS run.** The evidence below is extracted native source compiled with C++03 and undefined-behavior sanitization, or original Python bodies executed with narrow adapters.

Reproduce all five observations:

```sh
python3 docs/review/deep_source_probes.py /path/to/rise-of-mankind
```

The script checks the source commit and byte identity of the inspected files, then records source/fragment hashes in [deep-findings.json](deep-findings.json). It also verifies two normal source contracts: native handle lookup (C01) and partial effects after callback exceptions (C02). Exit zero means the documented observations reproduced; it is not a green game-regression result. The adapters are visible in [the probe script](deep_source_probes.py).

## D01 — Canal-only worker candidates always fail their value gate

**Confirmed arithmetic/control-flow defect; medium gameplay impact.** [AI_getPlotCanalValue](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayerAI.cpp#L24454) ends with:

```cpp
return 10 * std::min(0, pSecondWaterArea->getNumTiles() - 2);
```

All earlier returns are zero. A second water area of 1 tile gives −10; sizes 2, 3, 10, 100 and 1,000 all give zero. The expression can never provide a positive canal benefit.

[AI_fortTerritory](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvUnitAI.cpp#L19319) adds canal and optional airbase values, then requires a positive total before evaluating builds. Therefore a canal-only candidate cannot pass this gate, however useful its connection would be. An airbase score can still make a fort attractive; forts can arise through other paths. This is not a claim that the game can never contain canals.

**Probe:** compile the exact final expression, verify every return in the full method, and inspect the consumer gate. No host-path assumption is needed for the nonpositive-value conclusion.

**Candidate repair:** determine whether the intended formula was `max(0, size - 2)` and define the intended canal benefit before changing it. Test a useful connection, a one-tile lake, a preexisting adjacent city, competing worker tasks and route availability. Restoring a positive score alone does not establish a good canal policy.

**Simulation consequence:** retain current zero/negative compatibility values. Keep a separately named intended-policy experiment; never silently correct the formula in a reference model.

## D02 — Fort-build selection overwrites location utility and depends on build enumeration order

**Confirmed scoring defect; medium gameplay impact.** In [the build candidate loop](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvUnitAI.cpp#L19347), `iValue` initially holds the plot's strategic benefit. Each legal fort-like build overwrites it with `10000 / (build_time + 1)`. The code minimizes that inverse-time score, then later uses the final loop value to rank the location.

The compiled unchanged loop produces:

| Legal build times, in enumeration order | Original location benefit | Selected build time | Value remaining for location scoring |
|---|---:|---:|---:|
| 1,000, 2,000 | 500 | 2,000 | 4 |
| 2,000, 1,000 | 500 | 2,000 | 9 |
| 1,000, 2,000 | 10 | 2,000 | 4 |

The adapter makes both builds legal with identical defense. This isolates three problems: the slower equivalent build wins, the original location magnitude disappears, and reversing candidate order changes the retained location score while the chosen build stays the same.

The base XML has fort/bunker/future-bunker build times 1,000/1,200/2,000 and different defensive bonuses. A stronger bunker could legitimately be preferred. The flaw is the absence of an explicit utility tradeoff and the use of the **last evaluated** candidate's score, not proof that choosing an advanced bunker is always wrong. Actual simultaneous legality and mission selection require a game fixture.

**Candidate repair:** separate `locationValue`, `candidateBuildValue` and `bestBuildValue`; specify how defense, construction time and worker opportunity cost combine. Commit only the winning candidate's value. Test permutation invariance for unequal scores, explicit ties, and different defensive utility.

**Simulation consequence:** enumeration order is observable state in the current implementation. A simulator that sorts XML builds by name could conceal or change the defect.

## D03 — Save/load discards strategic history needed for equivalent continuation

**Confirmed source-state/decision divergence; high priority for simulation correctness.** [CvPlayerAI::read](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayerAI.cpp#L18689) resets the agenda, score, update turn, bad-start state, naval/logistics priorities, risk, expansion horizon, war posture and budgets. The corresponding writer does not serialize the agenda or derived priorities. Direct getters return these fields without lazy reconstruction.

The [agenda switch code](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayerAI.cpp#L4840) uses the previous agenda to apply hysteresis. That previous choice is history, not a disposable cache of the current world.

The probe executes the actual reset statements and switch block using base XML margins of 150 points and 12%. With incumbent land expansion scoring 1,000 and challenger science scoring 1,100, an uninterrupted review retains expansion; after the load reset it selects science. Separately, a naval-priority consumer changes its equal-value land/sea preference when priority resets from 900 to zero. These are controlled branch inputs, not an engine-derived campaign snapshot.

Even immediate recomputation cannot generally restore the previous hysteresis choice without its history. In sequential mode, movement can also consume priorities before the next economic `AI_doTurnPre` refresh. A matching engine trace is needed to quantify the precise divergence after supported save points.

**Candidate repair:** serialize decision-bearing agenda history and cadence state under a new save version; rebuild genuinely derived caches only after dependent world/rule state is ready. Define deterministic migration for older saves. Test saves before actions, after economic settlement and during operation recovery. Do not call a forced reevaluation “equivalent restore” unless the incumbent and cadence semantics are preserved.

**Simulation consequence:** distinguish three operations: simulator checkpoint/restore, source-compatible native save/load, and migration from an older binary. The simulator's own checkpoint should be lossless even when the source save/load path intentionally or accidentally loses state. Tests must not conflate those contracts.

## D04 — Research path valuation counts shared prerequisites more than once

**Confirmed heuristic distortion; medium planning impact.** [AI_cachedTechPathLength](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/CvPlayerAI.cpp#L5170) memoizes each technology's recursive scalar cost, but adds the scalars from AND prerequisites and the cheapest OR branch. Memoization avoids repeated computation; it does not deduplicate overlapping prerequisite sets.

The repository's base XML contains:

```text
Chariotry (120)
  AND Animal Husbandry (50)
  OR  The Wheel (48)
        AND Animal Husbandry (50)
```

With their other prerequisites already known, the compiled actual helper reports **4 steps and 268 cost**. The distinct required technologies are Animal Husbandry, The Wheel and Chariotry: **3 steps and 218 base cost**. The real base definitions supply this graph; the adapter supplies those costs as team research costs and marks other prerequisites known. Runtime modifiers and overlays are excluded.

The returned count can affect lookahead admission, and the cost feeds prerequisite-completion discounts. This is an inaccurate planning estimate, **not double charging by the research implementation**. The older `CvPlayer::findPathLength` also uses recursive scalar addition, so this need not be a newly introduced regression.

**Candidate repair:** specify the desired meaning first: recursive heuristic depth, distinct required technologies, or minimum cost of a legal research package. AND/OR DAG optimization with shared ancestors is not solved by a universal local `min` plus set union. For a bounded lookahead, retain alternative prerequisite sets, prune dominated packages and validate against exhaustive small graphs. Preserve the current heuristic as a compatibility mode.

**Simulation consequence:** expose both `source_heuristic_cost` and an independently computed legal-package cost in diagnostics. Do not replace the former with the latter when claiming source fidelity.

## D05 — Repeated Python load events accumulate upgrade mappings

**Confirmed lifecycle defect; low immediate gameplay severity.** [RoMEventManager.onLoadGame](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/Python/RoMEventManager.py#L244) appends all upgrade/obsolete pairs to instance arrays. Initialization creates empty arrays, but neither this load handler nor the corresponding game-start handler clears them before appending.

Executing the original initializer's mapping declarations and original load body on the same manager gives **83 → 166 → 249 entries** after three loads. Info lookups and profilers are narrow adapters. The tested bodies use no Python-2-specific division semantics.

The building-completion handler copies and repeatedly scans these arrays to remove obsolete buildings. Duplicate pairs mean extra memory, scans and repeated setter calls; this probe does not demonstrate repeated bonuses or a changed final building count. A fresh manager per load would avoid accumulation, so lifecycle scenarios should explicitly distinguish retained and recreated Python instances.

**Candidate repair:** construct fresh paired arrays once per initialization/load, or rebuild them atomically and replace the old values. Test repeated `OnLoad`, `GameStart → OnLoad`, module changes and missing rule types.

**Simulation consequence:** Python manager lifetime belongs in fixtures. Starting a fresh Python process for every simulated load would hide the retained-instance case.

## Further refinements to the model

**Entity identity already contains a native generation component.** [FFreeListTrashArray](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/blob/1ab4f99a76adb530f86b278390ab8139ef41cc96/Assets/CvGameCoreDLL/FFreeListTrashArray.h#L204) assigns a monotonically advanced ID component plus a 13-bit slot index. `getAt` checks the full ID when its generation bits are nonzero, but also accepts a low-bit-only slot lookup. This explains why iterating `getCity(0..count-1)` can appear to work before slots become sparse. Preserve full handles and the compatibility behavior of slot lookups; do not assume every native reference is vulnerable to simple slot reuse.

**Python callbacks can fail after mutating state.** BUG catches ordinary handler exceptions and continues with later handlers. No transaction rollback is supplied by that dispatcher. The simulator needs ordered partial mutations plus an exception outcome; treating the entire event as an atomic transaction would fabricate recovery behavior. Consumable input events and save events have distinct dispatch semantics.

C01 compiles the actual native lookup body and passes six checks: current full ID and slot lookup work before replacement; after slot replacement, the stale full ID fails while slot lookup and the new full ID work; the invalid ID fails. The adapter directly replaces a slot rather than executing the complete allocator. C02 executes the original ordinary-event dispatcher with synthetic handlers: the first changes gold from 1,000 to 1,010 and raises; the second observes 1,010 and adds five, leaving 1,015. This verifies dispatcher behavior without claiming native bridge or Python 2 runtime coverage.

**Some concerns remain hypotheses.** Operation-delivery cache freshness within a turn, host A* reuse/tie behavior, general/army separation after transport, and governor response under repeated disruptions need dedicated engine fixtures. Their presence in a test backlog is not evidence that they are defects. Extreme-integer policy inputs likewise should be separated from reachable game states before assigning gameplay severity.

The [simulation implementation plan](../../simulation/README.md) turns these findings into capability boundaries, checkpoint rules and acceptance gates. No proposed repair has been applied to game source.
