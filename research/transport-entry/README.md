# Transport ownership after manual boarding or autoplay changes

**Implemented follow-up:** [Joint destination and route search](../settlement-search/README.md)
removes premature portfolio pruning and land-first ferry selection. This report
records the preceding investigation.

Base: GitLab `6222511` (“AI decisionmaking reworked. New sea transport fixes”).
The user confirms the latest autoplay run used a DLL rebuilt from that commit.
This report therefore concerns the patched source, not an older bundled DLL.
The new observation is an assembled settler/escort party sitting at port and
then walking inland after autoplay resumes.

## Objective

Competence means selecting and completing a worthwhile settlement plan, whether
it uses walking, sailing or both. Boat utilization is not the objective. Compare
arrival and founding time, destination payoff, actual exposure and the opportunity
cost of the party. Preserve a feasible accepted plan through ordinary update
order changes; replan when its assumptions materially change. Existing route
tests include both a faster sea winner and a faster land winner. The current
heuristic does not yet evaluate that complete economic objective.

## Gap in the previous change

The previous dispatcher was reached through `UNITAI_SETTLER_SEA`. The generic
`CvUnitAI::AI_update` still sent other ship roles to their ordinary controllers.
A galley has an assault default role in XML; manually boarding a settler does
not itself change that role or create `MISSIONAI_FOUND`.

Passengers also retain their own AI roles. At a land port, generic update only
held cargo when the carrier had already moved or had a queued mission. The
settler-specific guard added previously required an existing FOUND mission.
Before the carrier's first planning update, a settler could therefore enter its
land planner and an escort its defense/attack planner. Role dispatch and update
order could undo the assembled party before the new voyage controller ran.

Those are concrete source entry-path gaps. Without an engine trace, they are
not proven to be the exact cause of every idle turn in the reported game.
There is also a distinct legitimate `LAND_JOB` branch: a loaded boat can choose
a higher-valued inland site. Poor site values or a shortlist without useful
coastal alternatives can make that choice strategically wrong even when the
transport controller executes as written. The accompanying settlement review
and scoring corrections address several upstream errors in that decision.

## Changes

`AI_handleSettlerTransport` now runs before the legacy land-cargo logic,
after-attack logic and role switch, while respecting the optional Python update
callback. Human-controlled units retain their ordinary controls.

- AI land passengers aboard a hull containing a settler yield their independent
  decision to the carrier even when no destination has been set yet.
- AI ships carrying settlers enter the civilian voyage controller regardless of
  their previous role. Existing FOUND destinations survive role changes.
- Grouped follower hulls carrying settlers are separated at friendly ports
  before a differently assigned group head can control their cargo. This reuses
  one separation routine from both generic entry and settler-ship movement.
- `AI_setUnitAIType` creates a new selection group. The code copies the mission
  type/plot before changing role and restores the destination afterward.
- `LAND_JOB` logs now include destination coordinates, land utility and best sea
  utility. New `WAIT_TRANSPORT` and `ADOPT_SETTLER_TRANSPORT` records distinguish
  passenger delegation and role adoption from path or cargo blockers.

No new save state or XML rule is required. Per-unit entry adds a cargo query;
the native cargo query scans units on the plot. Group separation only scans
multi-unit sea groups at a friendly port. This is not a global fleet optimizer.

## Evidence and next runtime checks

`Tools/test_settler_transport_entry.py` executes the actual entry, separation,
route, dispatch and reservation-release functions with explicit host adapters.
The test supplies an adapter for `AI_settlerSeaMove` that directly invokes the
real dispatcher, so emergency retreat and the full engine scheduler remain out
of scope. Role changes deliberately reset the adapter's group state to exercise
mission preservation, matching the relevant native side effect.

Cases include manual boarding without FOUND intent; assault-role carriers;
passenger-first and ship-first updates; existing destination through role
mutation; a settler-carrying follower behind an assault head; human control; and
ordinary troop cargo with no settler. A separate source contract checks that the
hook precedes legacy decisions. The combined suite has 21 passing programs.

For an in-game trace, record the existing BBAI unit log with `gUnitLogLevel >= 2`
(`BetterBTSAI.h` defines it as 3 when compiled with `LOG_AI`, otherwise 0), plus IDs, group/transport membership, remaining
moves, role, mission and destination before/after each decision. Interpret:

| Outcome | Meaning |
|---|---|
| `WAIT_TRANSPORT` | Passenger handed decision ownership to its loaded carrier. |
| `ADOPT_SETTLER_TRANSPORT` | Loaded carrier entered civilian control from another role. |
| `ASSIGNED_ESCORT` | Dispatcher consolidated a missing escort at port. |
| `SAIL` / `LAND` | Accepted voyage advanced or issued a landing mission. |
| `WAIT_MOVES` | Required movement for the next step is unavailable. |
| `LAND_JOB`, positive sea utility | Evaluator preferred the land job to a feasible sea alternative. |
| `LAND_JOB`, zero sea utility | No positive sea candidate survived the present shortlist/path evaluation. |
| `MISSING_ESCORT_OR_CAPACITY` | Manifest is incomplete; legacy required-escort pickup can still intervene. |
| `NO_REACHABLE_SITE` | No accepted or newly evaluated destination is feasible. |

A negative or absent runtime outcome must be investigated at its own layer.
Do not equate successful fragment tests with a completed engine replay. Still
unresolved are distant pickup, retry leases, site shortlist diversity, transport
via intermediate beaches to inland destinations, shared multi-ship operations,
and production demand based on actual transport jobs. The revised tests do not
claim to solve these systems.

[Patch and application instructions](../../fixes/README.md#settlement-placement).
