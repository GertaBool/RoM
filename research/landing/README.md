# Settler landing: complete the handoff to the land party

> **Correction.** On its own this change did not make settlers land in the game. Its landing
> code never ran there: aboard a ship at sea no land unit counted as an escort, so the ship
> waited in front of the site indefinitely. The tests missed this because their stand-in for
> `canDefend()` ignored the unit's plot. Patch 0011 fixes the escort check and the landed
> party's grouping, and was checked by running the real DLL; see
> [research/landing-engine](../landing-engine/README.md). The landing code below is still used.

This fix targets GitLab **`b8c379c1ffad9cd5408ca0e43dca88daf8ba85ee`**, including the user's imports of settlement placement and joint settlement planning. It changes only `CvUnitAI::AI_settlerSeaTransport` at runtime. Apply [patch 0008](../../fixes/0008-settler-landing.patch) with its [manifest](../../fixes/landing-manifest.json); do not reapply 0007 to this base.

## What the investigation establishes

The old dispatcher correctly finds an adjacent water approach, but its final action is another **ship** `MISSION_MOVE_TO`, aimed at the land site. That request must pass the carrier's path machinery and then `CvSelectionGroup::groupAmphibMove`, which creates separate passenger movement orders.

Three concrete source problems occur at this boundary:

1. The dispatcher waits for `canCargoAllMove()`, including passengers outside the chosen settler/escort party. Escort selection also overwrites its choice with the last defender, even if that defender cannot move and another can.
2. Passenger selection groups can contain units outside this hull's manifest. Native `canJoinGroup` checks owner, plot and domain, not transport identity. The generic amphibious code then checks whether the **entire cargo group** can move. An immobile member on another ship can block the selected pair.
3. `groupAmphibMove` forwards the passenger move without mission-AI arguments. Their default is `NO_MISSIONAI`, so the land party loses the founding destination. Reaching land and preserving the accepted settlement plan are separate requirements.

The new tests reproduce these failures against unmodified `b8c379c`. They execute the real dispatcher, `isAmphibPlot`, `groupAmphibMove` and `groupMove`, with explicit host adapters. These establish faulty source mechanisms consistent with the report; they do **not** identify the exact cause of the user's stalled galley without a matching engine trace.

The earlier voyage fixtures stopped after inspecting the ship's queued mission. They did not execute this handoff, so passing them was insufficient evidence of successful landing. This is a correction to that coverage gap.

## Narrow correction

Once the chosen water approach is reached:

- Prefer a movable defending passenger over an immobile alternative. Preserve the previous last-defender tie order when readiness is equal.
- Restrict the landing group to the selected settler and escort; unrelated cargo stays aboard its own carrier. Do not restructure a busy party.
- Wait for that party's readiness. Boarding exhaustion still permits sailing; an exhausted required escort still prevents a partial landing.
- Validate the party's landing path and issue its move **directly to the land group**, carrying `MISSIONAI_FOUND` and the destination.
- Use native group movement to enter land and detach cargo. Do not call `unloadAll` on water, teleport units, change movement allowances, or alter global amphibious behavior.
- Hold the ship while movement is queued. After synchronous execution, reacquire passengers by full native IDs before inspecting them, because movement callbacks can change groups or remove units.
- If the landing path is rejected, release the failed commitment and request the existing retreat-to-city recovery. When no recovery route exists, remain aboard and expose the blocked state; no movement through illegal terrain is invented.

The flags match native amphibious passenger forwarding: `MOVE_NO_ENEMY_TERRITORY | MOVE_IGNORE_DANGER`. Existing destination validation still requires a foundable site, no visible enemy unit, and entry legality for both passengers. This patch does not introduce a new blanket safety policy or preference for boats over walking.

## Validation and audit boundaries

The registered source suite has **17 passing programs**, including **14 landing cases**. Against clean upstream, **8 of those 14 landing cases fail assertions**; the six controls pass. Tests cover preserved founding intent, extra immobile cargo, foreign group members, required-escort exhaustion, queued movement, busy groups, movement callback removal, path rejection/recovery, invalid destinations, passenger-first holds, departure after boarding, walking preference and stable sea commitments.

Path graphs, scheduling, busy state and per-unit movement effects remain controlled adapters. A simulated callback removes an ID from lookup; it is not execution of the Python event system. No full DLL compilation, host A* replay or autoplay-save replay is claimed.

The clean upstream's existing 16-program suite had four failures before the fix: tests still referenced removed reserve/sea-preference helpers or expected queue double counting. This patch restores their previously tested assertions for the already imported runtime changes. It adds coverage rather than changing runtime economics to satisfy stale tests. The six previously published regression files not imported into GitLab are not silently counted in the 17-program total.

Review passes performed:

| Pass | Evidence / conclusion |
|---|---|
| Current-source audit | Refreshed GitLab and reviewed `b8c379c`; no assumption that the user still runs `6222511` |
| Native handoff audit | Traced movement, cargo readiness, grouping, mission defaults and cargo detachment; avoided changing the shared military amphibious handler |
| Mutation/recovery audit | Checked busy parties, synchronous/deferred movement, full-ID lookup after callbacks and failed-path recovery |
| Regression/application audit | C++03 with fatal UBSan, failing upstream controls, current suite, byte-preserving patch application and exact tree comparison |

Runtime work remains local to the selected expedition: the existing cargo scan, constant-size party handling and one explicit adjacent landing-path check. There is no additional whole-map search, new per-turn empire scan, save state or XML change. Native mission execution can query a path again; no measured claim of zero performance regression is made without Windows DLL profiles.

This is the highest-confidence narrow correction supported by this session's source evidence. It is **not** a claim that naval transport has no remaining gaps. Distant pickup, multi-stop voyages, hidden-information strategy and engine-specific scheduling still require their own evidence. The economic planner is also separate from this runtime fix.

## Engine acceptance run

Rebuild the DLL from the manifest's applied tree and record its hash. Resume a save with a settler and escort already off the chosen coast, then repeat with an extra immobile defender and with manually rearranged cargo. Verify actual land positions, cleared transport references, retained founding destination and eventual founding. Also test a blocked destination and a faster walking option.

At unit log level 2, the dispatcher emits `WAIT_LANDING_PARTY`, `LANDING_PATH_BLOCKED`, `LANDING_QUEUED`, `LANDED_PARTY` or `LANDING_PARTY_CHANGED`. A queued order is not reported as a delivered party. Report a remaining stall with these transitions and the rebuilt DLL/source identity.
