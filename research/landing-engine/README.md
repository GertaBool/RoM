# Settler landing, checked against the real DLL

You reported that settler landings still failed after patch 0008. The galley
sailed to the tile in front of the chosen site and stayed there, with the
settler and escort aboard. Patch 0008 ([research/landing](../landing/README.md))
had been checked only by unit tests whose stand-ins for engine functions behaved
differently from the engine. This round ran the real DLL instead, found the cause,
fixed it, and confirmed the fix the same way.

Patch: [fixes/0011-settler-landing-escort.patch](../../fixes/0011-settler-landing-escort.patch),
landed on GitLab `main` as
[!36](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/36).
DLL: [builds/0011/CvGameCoreDLL.dll](../../builds/0011/CvGameCoreDLL.dll).

## How it was checked

[toolchain/harness](../../toolchain/harness/README.md) runs a real
`CvGameCoreDLL.dll` built from the mod source, under Wine and without the game. The
DLL loads the mod's XML and plays a scripted map. Path finding calls the DLL's own
A* callbacks. Python is off; callbacks whose result the DLL reads anyway get the
BTS/RoM defaults.

Each scenario places one player on a 3x3 island with no room for a second city.
The player has a capital, a settler, two warriors and a galley. An empty island lies
to the east. The AI plays 30 turns.

## What the unmodified DLL does

Taken from [runs/plain/main/run-mid.log](runs/plain/main/run-mid.log) and
[bbai-mid.log](runs/plain/main/bbai-mid.log), site at (21,6):

```text
turn 0      Settler ferry to 21,6: walking 2147483647, sea including transfers 5
turns 1-2   the galley sails with settler and warrior aboard; by turn 2 it is at 20,5, next to the site
turn 3      Settler transport 32771: MISSING_ESCORT_OR_CAPACITY
turns 3-30  the galley stays at 20,5 with the same message every turn; no second city
```

On turn 0, in port, the settler's ferry code loads the party and sends the galley
to the water tile in front of the site. When the galley arrives, its own routine,
`CvUnitAI::AI_settlerSeaTransport`, takes over. It looks for the settler and an
escort among its cargo:

```cpp
if (aCargo[i]->getDomainType() == DOMAIN_LAND && aCargo[i]->canDefend() && ...)
    pEscort = aCargo[i];
```

`CvUnit::canDefend(const CvPlot* pPlot = NULL)` uses the unit's own plot when no
plot is given. It then requires `pPlot->isValidDomainForAction(*this)`, unless
`LAND_UNITS_CAN_ATTACK_WATER_CITIES` is set, and in Rise of Mankind it is 0. A
warrior aboard a galley is on a water tile, and land units cannot act on water, so
`canDefend()` is false for every land unit at sea. The ship found no escort,
logged `MISSING_ESCORT_OR_CAPACITY`, tried to pick one up, and skipped the turn.
That repeated every turn. Patch 0008's landing code comes after this check, so it
never ran in the game.

The Codex tests passed for two reasons:

- Their stand-in was `bool canDefend(){return defense;}`. It ignores the plot, so
  a warrior at sea "could defend".
- Their stand-in `move()` kept units in their group on landing. The real
  `CvUnit::setXY` does `if (!bGroup || isCargo()) joinGroup(NULL, true);`, which
  puts every unit leaving a ship into a new group of its own. That new group has no
  `MISSIONAI_FOUND`. The tests asserted that the landed party stays one group with
  its founding job, which the real engine does not do.

## The fix

1. Recognise escorts with `canFight()`. That is the check `canDefend()` makes
   apart from the plot, and the cargo scan wants the unit, not its current tile.
2. After a delivered landing, rejoin the escort to the settler's group and restore
   `MISSIONAI_FOUND` with the site. The settler cannot found on the landing turn:
   moving from water to land costs a land unit all its moves (`CvPlot::movementCost`
   returns `maxMoves()` when the start plot is invalid for the unit's domain). Next
   turn, the patch 0010 rule in `AI_settleMove` ("a settler standing on its
   accepted site founds now") applies.

I first also wrote a branch that founds at once if the settler still had moves.
Because of the movement rule above, that branch could never run, so it was removed.

## Results

30 AI turns, three distances, two start modes. Default mode is Settler difficulty
with 1000 gold and a size-3 capital, so unit upkeep cannot disband the ship or
escort mid-test. `MODE=plain` is Noble difficulty with neither. All six results
were the same in both modes ([summary](runs/summary-default.txt),
[plain](runs/summary-plain.txt)):

| Build | Site 6 tiles away | Site 10 tiles away | Site 16 tiles away |
|---|---|---|---|
| GitLab `main` 86af2ab | 29 `MISSING_ESCORT` waits next to the site, no city | 28 waits, no city | no voyage |
| Escort change only | lands turn 2, founds turn 3 | lands turn 3, founds turn 4 | no voyage |
| Patch 0011 | lands turn 2, founds turn 3 | lands turn 3, founds turn 4 | no voyage |

The 16-tile site lies beyond the AI's settlement candidate range, so no voyage is
planned. That is not a transport problem.

The escort change alone is enough in these scenarios. When the landed settler,
alone and without a job, re-plans, the site it stands on is still the best one.
The regroup removes that dependency. The settler keeps the site it sailed for, and
the escort stays with it if anything delays founding. The corrected unit tests
show the difference: on `main` 9 of the 14 landing cases fail; with only the escort
change, the 2 cases that require the founding job to survive landing fail; with
the patch all pass ([before log](../../fixes/landing-escort-before.log)).

## Validation

- Regression suite: 24 programs, 0 failures. Application checked on a fresh clone:
  the staged tree equals the tested tree `2f144cfd` and the GitLab `main` tree
  ([log](../../fixes/landing-escort-patch-validation.log)).
- MSVC 2003 release build: 0 errors, 0 warnings, the same 2451 exports as before.
  clang differential gate on `CvUnitAI.cpp`: no new diagnostics.
- Not run in the game client, and no save was replayed. The harness runs the
  DLL's code but not RoM's Python, and only one player is on the map.

## A harness bug worth knowing about

The first harness runs disbanded the escort for "financial trouble" before the
voyage. `CvPlayer::calculatePreInflatedCosts` calls the Python `getExtraCost`
callback and adds its result without initialising it. The harness Python stub did
not write a result, so the costs were garbage. The stub now writes the BTS/RoM
default for every callback whose result the DLL reads. The game always runs Python,
so this is not a game bug, but it is why the harness's Python defaults matter.

## If a landing still fails in your game

At unit log level 2 (BBAI log), look for these lines from the galley:
`MISSING_ESCORT_OR_CAPACITY` (escort not recognised, now fixed),
`WAIT_LANDING_PARTY` (a passenger has no moves), `LANDING_PATH_BLOCKED`,
`LANDED_PARTY`. If you send the log and the save, the scenario can be rebuilt in the
harness.
