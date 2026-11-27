<!-- Rendered by method/docs.py from passes-2-8.md.in. Do not edit; edit the template. -->
# The GitLab passes in play: `c08a472` against `main`

What the AI did in the harness before and after the third to eighth passes (`bf17674`, `d5fa0d1`),
for the agenda planner, the city governors, the military operations and turn time. The reading that
led here is `codemap/guides/passes-2-8-review.md`, section seven; the hypothesis is H10 and the
predictions P18 and P19 (`method/mission/register.json`).

## Setup

- Two harness DLLs (`toolchain/harness/build_dll.sh`): `c08a472` (before the second pass) and
  `ede81881b7de` (`main`), each with the XML of its own commit. On `main` that switches the passes on
  (`AI_CUNNING_FLAGS` and `AI_ECONOMY_FLAGS` as committed).
- The mod's Mediterranean scenario, Standard WorldBuilder map, from turn zero, all seats AI, Noble,
  Marathon (`med-standard.scn`, the same as P17).
- Seeds from `ledger.py seeds` for P18 and for P19: 20 runs of `c08a472` and
  20 of `main`, pooled below. Four runs at a time, the two commits of each seed side by side.
- The telemetry reads each AI player's agenda, financial trouble, its team's war plans, its active
  operations and its cities per governor type on every turn (`plans`, `ops`, `gov`, added for this).

## Description

**Completion.** 20 runs of `c08a472` and 20 of `main` reached their result line.

**Turn time.** Median seconds per run: `c08a472` 120.5, `main` 110.1.
P18, on its own runs: rank Welch test p 0.0041, A 0.86 (the probability that a run of
`c08a472` takes longer than one of `main`).

**War plans, financial trouble and operations,** per thousand player-turns
(70214 player-turns of `c08a472`, 70186 of `main`):

| measure | c08a472 | main |
|---|---|---|
| player-turns under a war plan | 303.7 | 533.3 |
| player-turns in financial trouble | 19.8 | 11.0 |
| active operations, summed over player-turns | 104.4 | 83.4 |

*per mille; who: every AI player of the Mediterranean scenario (10 players, all AI); turn: turns 1 to 350, Marathon; rows counted: 140400; source: toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: per mille of player-turns (operations: per thousand player-turns). Every value counted (3).*

**Agenda,** per thousand player-turns:

| agenda | c08a472 | main |
|---|---|---|
| Survive | 43.1 | 106.3 |
| Recover | 3.1 | 2.4 |
| Expand land | 614.8 | 664.1 |
| Expand maritime | 180.0 | 58.1 |
| Consolidate | 40.1 | 25.9 |
| Power spike | 0.0 | 0.0 |
| Conquest | 89.1 | 127.6 |
| Science | 29.6 | 15.4 |
| Culture | 0.0 | 0.0 |

*per mille; who: every AI player of the Mediterranean scenario (10 players, all AI); turn: turns 1 to 350, Marathon; rows counted: 140000; source: toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: per mille of player-turns with an agenda. Every value counted (9).*

**Governors,** per thousand city-turns with a governor:

| governor | c08a472 | main |
|---|---|---|
| Steward | 197.4 | 200.3 |
| Agriculturalist | 132.1 | 126.5 |
| Harbourmaster | 110.6 | 86.8 |
| Merchant | 43.8 | 47.5 |
| Industrialist | 324.8 | 315.9 |
| Scholar | 133.7 | 172.2 |
| Curator | 30.8 | 21.5 |
| Castellan | 3.2 | 9.2 |
| Colonial | 23.6 | 20.1 |

*per mille; who: every AI city with a governor; turn: turns 1 to 350, Marathon; rows counted: 439722; source: toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: per mille of city-turns with a governor. Every value counted (9).*

## Readings

**The passes do not slow the AI here; `main` is faster.**
- *Facts:* the turn-time line above. P18 predicted `c08a472` no slower than `main` and is not
  corroborated: the difference runs the other way.
- *What it contradicts:* reading three of the review (the passes make the AI spend more time per turn).
  The added scans exist, but something else the passes changed costs less, or the AI does less.
- *Would contradict this reading:* the same comparison on a later, larger map with the opposite result.

**War plans are set far more often, and the agenda follows them.**
- *Facts:* the war-plan row and the Survive and Conquest rows. This is what AG1 to AG4 of the review
  predicted from the anti-hegemon branch of `AI_doWar`.
- *Would contradict it:* the same share of war-plan turns with the anti-hegemon branch switched off
  (cunning flag bit `256` cleared), which would point to another cause.

**Fewer operations.**
- *Facts:* the operations row, lower on `main` while war plans are more frequent.
- *Would contradict it as an effect of garrisons (OP1 to OP4):* the same drop with the peacetime danger
  scan off (cunning flag bit `128` cleared).

**Castellans are rare in this scenario.**
- *Facts:* the Castellan row: more on `main`, but a small share of all governed cities. The governor
  churn of GV3 was not measured: the telemetry counts types, not replacements.
- *What it weakens:* reading five of the review, as far as governors go, for this map.

**Not measured here:** the economy-focus loss of GV1 (no building counts per governor type), governor
replacements, and whether peacetime danger fired (`AI_isDanger` fills caches; the telemetry does not
call it).

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `runs_c08a472` | 20 | runs | every AI player of the Mediterranean scenario (10 players, all AI) | turns 1 to 350, Marathon |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py |
| `runs_main` | 20 | runs | every AI player of the Mediterranean scenario (10 players, all AI) | turns 1 to 350, Marathon |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py |
| `done_c08a472` | 20 | runs | every AI player of the Mediterranean scenario (10 players, all AI) | turn 350 |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: runs whose run.log has the RESULT line |
| `done_main` | 20 | runs | every AI player of the Mediterranean scenario (10 players, all AI) | turn 350 |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: runs whose run.log has the RESULT line |
| `secs_median_c08a472` | 120.5 | seconds | the harness run | turns 1 to 350, Marathon |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: sum of the turn records' ms, median over the runs |
| `secs_median_main` | 110.1 | seconds | the harness run | turns 1 to 350, Marathon |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: sum of the turn records' ms, median over the runs |
| `p18_p` | 0.0041 | share | the harness run | turns 1 to 350, Marathon | 20 | method/stats.py rank_welch on P18 arm a (c08a472) against arm b (main), seconds per run |
| `p18_A` | 0.86 | share | the harness run | turns 1 to 350, Marathon | 20 | Vargha-Delaney A of P18 arm a over arm b (probability that a run of c08a472 takes longer) |
| `pt_c08a472` | 70214 | turns | every AI player of the Mediterranean scenario (10 players, all AI) | turns 1 to 350, Marathon |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: player-turn records with the new fields |
| `pt_main` | 70186 | turns | every AI player of the Mediterranean scenario (10 players, all AI) | turns 1 to 350, Marathon |  | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: player-turn records with the new fields |
| `state` | table, 3 values | per mille | every AI player of the Mediterranean scenario (10 players, all AI) | turns 1 to 350, Marathon | 140400 | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: per mille of player-turns (operations: per thousand player-turns) |
| `agenda` | table, 9 values | per mille | every AI player of the Mediterranean scenario (10 players, all AI) | turns 1 to 350, Marathon | 140000 | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: per mille of player-turns with an agenda |
| `governor` | table, 9 values | per mille | every AI city with a governor | turns 1 to 350, Marathon | 439722 | toolchain/harness telemetry (run.jsonl, run.log), research/passes-2-8/passes_runs.py: per mille of city-turns with a governor |
