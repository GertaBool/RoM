# Headless simulation: implementation and validation plan

Status: **specification, validated interchange examples, and source probes; no game simulator yet.** Source target: `1ab4f99a76adb530f86b278390ab8139ef41cc96`. The bundled DLL is older. Read the [behavior guide](../docs/review/AI_AND_GAME_LOGIC.md), [game-flow model](../docs/review/GAMEFLOW_MODEL.md) and [new findings](../docs/review/DEEP_FINDINGS.md) together.

The first useful deliverable should answer a narrow question reproducibly: *given this source revision, explicit state, actor-visible inputs, rule configuration and host answers, why did this decision or transition occur?* A whole-game win-rate comparison is a later deliverable.

## 1. Three experiments that must remain distinct

| Track | Question | Oracle | Permitted conclusion |
|---|---|---|---|
| Source contract | Does an extracted method/policy do what we think? | Actual compiled/executed source with documented adapters | This fragment produces this output under this contract |
| Model experiment | Does a proposed rule or strategy improve a declared objective in a simplified world? | Explicit intended-rule assertions and statistical design | Result within the model's stated capabilities |
| Engine differential | Does the headless transition match a specific rebuilt game? | Matching source/build/rules snapshot and ordered engine trace | Equivalence for the covered scenario and observations |

An old-DLL trace remains useful evidence about that old binary, but cannot certify current-source equivalence. A synthetic scenario must never acquire an `engine_differential` claim just because its numbers look plausible. The example manifest deliberately declares source-contract scope and unsupported host services.

The source contains confirmed bugs. Preserve observed behavior in compatibility tests; place intended behavior in separately named tests/treatments. A green compatibility test can intentionally reproduce a defect. Never report that result as a healthy game rule.

## 2. Deliverables and stop conditions

| Milestone | Concrete deliverable | Acceptance gate | Stop when |
|---|---|---|---|
| M0: evidence laboratory | Pinned extraction probes, findings ledger, strict manifest/scenario/trace envelopes | Source identity checked; expected observations reproduced; malformed claims/traces rejected | Complete for the documented probes and envelope examples |
| M1: native policy runner | Batch CLI invoking production policy headers, with typed field units | Ordinary/boundary fixtures, deterministic output and sanitizer checks; provenance accompanies every run | A requested engine-dependent query lacks an implementation |
| M2: rules and state interchange | Effective-rule export/import; versioned state graph and entity iteration order | Symbols/IDs, merge order, defines, references, numeric widths and sparse handles round-trip | Required base BTS assets or effective rules are absent |
| M3: sequential scheduler slice | One complete sequential player cycle with accounting and one city | Named phases, counters, RNG, queues and nested callback mutations agree with reference fixtures | An unsupported callback, host query or deferred choice is reached |
| M4: missions and geography | Movement/cargo/path port, combat and capture slices | Replayed host paths first; replacement algorithm only after node/turn/tie tests | Legal-path success is the only evidence of parity |
| M5: strategy integration | Agenda → city/operation → mission → outcome → feedback scenarios | Multi-turn scenarios explain first divergence, preserve memory and survive checkpoints | Outcome metrics lack a complete supported transition path |
| M6: engine comparison and campaigns | Recorded rebuild, instrumentation, paired scenarios and then multi-seed campaigns | Exact covered transitions; save/load tracked separately; instrumentation does not change gameplay/RNG | Source/DLL/rules identities disagree or reference capture is incomplete |

This is a dependency graph, not a schedule promise. M1 policy tests can advance before a Windows rebuild. Reference capture work can advance alongside M2. Full map generation, simultaneous modes and multiplayer require separate capability gates; they are not implied by sequential support.

Do not repair the existing two baseline regression failures as part of a model implementation without separate game-source changes. Preserve their recorded baseline. Review and propose fixes in dedicated commits with targeted tests and save-format implications.

## 3. State schema and ownership

The simulator needs more than a set of visible game pieces:

| State partition | Required contents | Snapshot rule |
|---|---|---|
| Rules/build | Source commit, dirty-file digests, binary/build identity, BTS version, ordered modules, effective Type→ID map, defines and options | Immutable identity, plus ordered runtime-option changes |
| Scheduler | Mode, global/elapsed turn, slice, active flags/count, phase cursor, player/city/group iteration position, auto/end flags | Preserve exact continuation point |
| World | Plot coordinates/wrap, terrain/features/routes/resources, culture/ownership, visibility/revealed state, areas and plot groups | Preserve topology and observation state separately |
| Teams | Tech/progress, relations, plans and timers, projects/votes, vassal constraints and victories | Keep declared war separate from preparing a war |
| Players | Treasury, commerce, research queue, civics/religion/timers, modifier state and entity collections | Preserve native iteration and integer units |
| Cities | Population/food/culture, improvements/buildings, yield/commerce components, citizens/specialists, queues/overflow, revolt and governor memory | Distinguish stock, per-turn rate and rate-times-100 fields |
| Units/groups | Full native IDs, role/type, movement/damage/promotions, cargo, group order, missions and mission intentions | Ownership and membership changes are explicit effects |
| AI history | Agenda incumbent/cadence, operation state/progress, careers, governor terms, strategy memories and contact timers | Persist every field that can affect a later choice |
| Derived caches | Values, validity epoch, dependency keys, invalidation causes | Rebuild only when semantically safe; reproduce stale-state behavior in compatibility mode |
| Python | Manager lifetime, registered handler order, BUG/SdToolKit records, queued revolts, upgrade mappings and options | Capture or explicitly declare unsupported |
| Interaction | Pending human decision, popup context, accepted command ordering and transport/network handoff | No fabricated default answers |
| RNG | Map/gameplay streams and any selected Python/map-script stream; exact seed and draw index | Include zero-bound draws and conversion semantics |

Native entity IDs are not simple dense indices. `FFreeListTrashArray` combines generation bits with a 13-bit slot; low-bit-only lookup is a special compatibility path. Preserve full native IDs, slot order, free-list metadata and owning player. Add an external run identity for trace correlation, but do not replace native handle checks with a different invented identity model.

Represent arrays and ordered collections explicitly. JSON-object order must not accidentally choose a unit, diplomatic counterpart or tied production candidate. For cross-run equality, canonicalize field names while preserving all semantically ordered lists.

### Checkpoints versus native saves

A simulator checkpoint must preserve its continuation exactly. A source-native save/load transition may not: D03 shows agenda history being discarded. Model these as different commands:

```text
checkpoint_restore: lossless simulator state, including decision history
native_save_load: apply the reviewed source's write/read and lifecycle semantics
migrate_legacy_save: explicit versioned migration with declared defaults
```

Initially permit checkpoints only at quiescent phase boundaries: no active callback stack, unfinished combat resolution or pending unrecorded host call. Arbitrary mid-function continuation requires explicit continuation frames and is a separate milestone. Pending human decisions can be checkpointed only when the full decision context is represented.

## 4. Transition and failure semantics

```text
advance(state, command, manifest, services)
  -> completed(new_state, ordered_events)
   | yielded(new_state, pending_decision, ordered_events)
   | unsupported(partial_state, capability, ordered_events)
   | failed(partial_state, error, ordered_events)
```

“Unsupported” is a first-class result. Returning zero from an unknown `Cy*` function would silently create game rules. Record how far the transition progressed and prohibit outcome claims beyond that boundary.

Do not implement blanket transaction rollback. Native callbacks can mutate state and then raise; BUG's ordinary dispatcher catches an exception and proceeds to later handlers. Preserve that partial effect sequence. Record the exception and let the relevant fidelity/health gate decide whether the experiment can continue. Input-consumption callbacks and save callbacks need their own return-value contracts.

A command is more than an action name: actor, referenced native identities, inputs, accepted phase, command sequence and provenance are required. Revalidate legality when it executes; a queued mission's target can die, change owner or become inaccessible. Keep proposal, validation, acceptance, mutation and completion events distinct.

Scheduler rules must be explicit transitions rather than a generic `for player: take_turn()` loop. Encode sequential economics on deactivation, simultaneous-player economics on activation, initial-turn guards, team handoff, global counter reconciliation and old/new turn numbers on callbacks. Before supporting a mode, require its full phase-order fixture to pass.

## 5. Service boundaries and required answers

| Service | Inputs | Outputs and exactness requirement |
|---|---|---|
| Rule registry | Symbol/ID, active configuration and epoch | Typed resolved record with origin; absent symbol is distinct from numeric zero |
| Observation adapter | Actor, routine, world epoch | The exact information that routine consumes, including native AI/human asymmetries |
| Native policy kernel | Typed snapshot with units and enum versions | Decision plus decisive scores/guards; actual production policy where portable |
| Path service | Group composition, start/destination, flags, moves, visibility, diplomacy, world/cache epoch | Success, node path, costs, remaining moves and turn count; record failed queries too |
| Combat service | Chosen participants/defender, modifiers, first strikes, damage and RNG | Ordered rounds, collateral/flanking/withdrawal, deaths, movement/XP and callbacks |
| Python bridge | Registry, event arguments, live handles and interpreter semantics | Ordered handler results, nested effects, exceptions and updated script data |
| Decision provider | Complete human/event/diplomacy context | Explicit accepted response or yield; no implicit acceptance |
| Persistence | State version, supported boundary and external dependencies | Reproducible checkpoint or explicit source save/load behavior |
| Trace sink | Observations produced during execution | Append-only records; must consume no game RNG and make no stateful AI queries |

Path replay keys must include more than endpoints: group composition, current movement, flags and relevant world/diplomacy/visibility epochs affect answers. A recorded path can be reused only when its declared inputs match. Host A* tie-breaking and reuse behavior remain unresolved; a new search implementation is initially a model experiment.

Trace instrumentation should observe decisions as they are made. Re-running a scorer “for logging” can consume RNG, mutate caches or invoke callbacks. Log already-computed intermediates and compare logging-on/off traces under identical inputs.

## 6. Arithmetic and randomness

Use explicit Windows-target widths: 32-bit `int`/`unsigned long`, 16-bit native random bound and documented 64-bit intermediates. Linux C++03 fragment compilation does not establish the ABI of the production DLL. Probe adapters must state every type substitution.

Preserve C++ truncation toward zero, Python 2 integer division, per-expression clamping and rounding. Do not silently map signed overflow to Python's unlimited integers or call undefined C++ behavior a deterministic rule.

For `CvRandom::get`, the source-derived Windows recurrence is:

```text
native_bound = supplied_bound modulo 2^16
next_seed = (1103515245 * seed + 12345) modulo 2^32
value = (((next_seed >> 16) & 65535) * native_bound) // 65536
```

Even native bound zero advances the seed. Keep map RNG during gameplay: conquest code can consume it. The contract validator checks example draw records against this source formula, but production-target reference vectors remain an M6 gate.

Common seeds do not guarantee aligned randomness after policies branch. For strategy experiments, distinguish ordinary same-seed trajectories from an intervention using recorded exogenous events. Replaying every old RNG answer against a new sequence of requests is invalid unless the experiment explicitly defines that coupling.

## 7. Evidence-driven scenario backlog

The [scenario catalog](scenarios.json) records fixture inputs, compatibility expectations, proposed intended expectations and evidence status. It is a specification; it is not a general scenario executor. The source probes currently implement fixed corresponding cases independently.

| Priority | Scenario family | Acceptance evidence |
|---|---|---|
| P0 | Source/binary identity; old DLL excluded from current-source oracle | Manifest guard plus recorded build provenance |
| P0 | Full-ID versus slot lookup; sparse cities | Actual free-list contract and Python handler fixture |
| P0 | Agenda checkpoint versus native save/load | Preserve incumbent/cadence in checkpoints; reproduce D03 in native-load mode |
| P0 | Sequential/simultaneous scheduling and dead first team | Exact phase trace, no repeated unattended rollovers |
| P0 | Nested mutation followed by callback exception | Partial effects and next-handler execution match the dispatcher |
| P1 | Canal/fort candidate ranking | D01/D02 reproduction, plus separately specified corrected-policy tests |
| P1 | Shared prerequisite graph | D04 source output; independent legal-package oracle on small AND/OR graphs |
| P1 | Repeated Python lifecycle events | D05 retained-instance growth; recreated-instance control |
| P1 | One city: grow, produce, complete and invoke Python | Stocks/rates/overflow reconcile with ordered effects |
| P1 | Operation assembling/recovering/transport/capture | Unit capability and temporal gates; no shortcut based only on stack count |
| P1 | Diplomacy offer and cancellation | Denials before valuation; recurring effects and treaty state |
| P2 | Path ties, river/route corners, embark/disembark | Node-level rebuilt-engine comparisons |
| P2 | Combat, capture, revolt and victory interaction | Matching RNG and nested effect trace through the complete supported transition |

Stateful tests should generate legal sequences, not just random field combinations: found → grow → produce → capture → reload; assemble → embark → unload → recover → reinforce; propose → accept → tick → cancel. Shrink a failure by reducing the command sequence while preserving legality and the first divergence.

Metamorphic tests need carefully stated preconditions. Candidate permutation should preserve a unique-utility winner in an intended policy; the existing D02 implementation violates that. It is not valid to demand permutation invariance from every source routine, since native tie-breaking is often intentionally order-sensitive. Likewise a save round trip is not automatically a lossless source transition.

## 8. Differential debugging and campaign design

Compare at the earliest differing layer: manifest/rules → observations/cache epochs → legality → selected branch/score → RNG request → mutation → callback → digest. A different final winner is too late to locate the cause.

Each trace event carries run identity, sequence, turn/slice/phase, span and parent. The supplied envelope supports nested entry/exit, decisions, mutations, RNG, unsupported outcomes, exceptions and checkpoints. Mutation records contain old/new values and stable targets. These envelopes are an initial interchange contract, not a complete serialized world or a reproduction of the BTS save format.

For policy experiments, register hypothesis, treatment, unchanged controls, fixture provenance, outcome horizon and metric before running. Measure mechanism-level outcomes first: worker turns to connection, delivered capturers, time in stalled siege, research delivery time, reserve shortfalls. Then evaluate across multiple maps, civilizations, eras and seeds. Split related scenarios by lineage so sibling branches cannot enter both training and evaluation sets. Report failure/unsupported rates with performance metrics.

Do not claim a better policy from one favorable campaign or from a simulator that omits the costs the policy exploits. Use independently held-out scenarios and a matching engine subset before extrapolating model results.

## 9. Concrete contracts included here

```sh
python3 simulation/validate_contracts.py
python3 -m unittest discover -s simulation -p 'test_contracts.py' -v
python3 docs/review/deep_source_probes.py /path/to/rise-of-mankind
```

The first two require Python 3 and `jsonschema` 4.x (install with `python3 -m pip install -r simulation/requirements.txt` in a virtual environment). They validate envelopes, claim boundaries, trace nesting/sequences and RNG examples, including rejection cases. They do **not** validate source scheduler semantics, execute scenario catalog entries or prove the truth of evidence strings. The third requires `g++` with C++03 and UBSan support; it compiles actual source fragments and executes narrow Python lifecycle and dispatcher probes.

The next implementation step is M1's typed policy runner plus M2's effective-rule export contract. A whole-game loop should wait until the state, lifecycle and host-service boundaries can fail explicitly and explain their outputs.
