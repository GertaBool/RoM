# The key functions of the DLL

The twelve functions that rank above the rest, what each does, and what a hand rewrite of one has to keep.
Written by hand from the source at commit `2a8b9a83eb5b`, the commit the map was built from; line numbers
refer to it. The hard-coded entries are listed in full, and checked, in `../hardcoded.md`.

## How they rank

Function A ranks above function B when every call path from outside the DLL into B passes through A
(A dominates B). Calls from outside enter at every function the game exe or Python can call: exported
functions, functions bound for Python, and functions with no caller in the DLL. A function's rank is the
number of functions only reachable through it. `python3 codemap/tool/query.py rank 12` prints this:

```
CvGame::update                         the exe calls it every game tick
├── CvGame::updateMoves
│   └── CvPlayerAI::AI_unitUpdate
│       └── CvSelectionGroupAI::AI_update
│           └── CvUnitAI::AI_update
└── CvGame::doTurn                     ··· switches on CvPlayer::setTurnActive (below)

CvXMLLoadUtility::LoadPreMenuGlobals   the exe, at startup
CvPlayer::setTurnActive                the exe, and six other functions of the DLL
└── CvPlayer::doTurn
CvXMLLoadUtility::LoadPostMenuGlobals  the exe, when a game starts
CvDLLWidgetData::parseHelp             the exe, when the mouse is over the interface
CvGlobals::deleteInfoArrays            on a reload and at cleanup
```

Ranked by how many functions each reaches, the list would be flat: thousands of functions reach each other
through one large cycle of calls. That is why the rank counts what only one function leads to.

## What each one does

**The game tick**

- **`CvGame::update`** (CvGame.cpp:2147). Called by the exe every tick. Outside World Builder it:
  1. sends player options and posts the Python event `gameUpdate`;
  2. autosaves on the first tick;
  3. recounts the players whose turn is active and repairs the stored count when it is wrong;
  4. runs `doTurn` when no player's turn is active;
  5. updates score, war, unit moves (`updateMoves`), timers and worker assignment, and checks who is alive;
  6. ends the game when no human is left, unless an AI autoplay or autorun is going.
- **`CvGame::updateMoves`** (CvGame.cpp:7223). For every living player whose turn is active, in shuffled
  order when turns are simultaneous, it runs `AI_unitUpdate`. An AI player with no busy or ready unit is
  switched to automatic moves, and every one of its groups then runs its queued mission.
- **`CvPlayerAI::AI_unitUpdate`** (CvPlayerAI.cpp:1572). It splits the groups marked for separation, except
  those in the middle of an attack. A human player's groups are updated in cycle order; an AI player's are
  sorted by `AI_movementPriority` first. It stops at the first group whose update returns true, because
  objects may then have been deleted. A guard ends the moves of a unit that keeps losing its group
  without moving, so the turn can end.
- **`CvSelectionGroupAI::AI_update`** (CvSelectionGroupAI.cpp:184). It wakes a sleeping AI group. While the
  group is ready to move, it finishes a pending group attack or calls `AI_update` on the head unit. After
  100 rounds it logs "Unit stuck in loop" and ends the units' moves. AI units that can still move then try
  to join another group (`AI_follow`); if none does, the group skips its turn.
- **`CvUnitAI::AI_update`** (CvUnitAI.cpp:195). The decision for one unit:
  1. it can hand the unit to Python (`AI_unitUpdate`, when the define `USE_AI_UNIT_UPDATE_CALLBACK` is set);
  2. it handles a settler waiting for transport, land units at sea or on a transport, what follows an
     attack, and city range strikes;
  3. automated groups branch on the automation (build, network, city, explore, religion); all others,
     after `AI_operationMove`, branch on the unit's AI role, one move routine per role (`AI_settleMove`,
     `AI_attackCityMove`, `AI_cityDefenseMove`, `AI_workerMove`, the sea and air moves and so on).

**The turn change**

- **`CvGame::doTurn`** (CvGame.cpp:5921). The end of the game turn: the begin-turn event, caches and the
  border-danger flags reset, score and deals, every team's and the map's turn, barbarian cities and units,
  global warming, holy cities, corporation headquarters, diplomatic votes, the AI autoplay countdown, the
  turn counter. It then switches on the first player's turn (all of them at once when turns are
  simultaneous), checks for victory and autosaves.
- **`CvPlayer::setTurnActive`** (CvPlayer.cpp:12160). Switching on: it writes the AI logs (score, wars,
  war plans), resets the turn timer, makes the player active in hotseat or play-by-email, runs
  `doTurnUnits` (and `doTurn` when turns are simultaneous), plays the new-turn sound or message, and
  writes the war log's turn start. Switching off: it runs `doTurn` when turns are sequential, then switches
  on the next living player or team. This is how the turn moves from player to player.
- **`CvPlayer::doTurn`** (CvPlayer.cpp:3918). One player's end of turn: `AI_doTurnPre`; the revolution,
  conversion, free-unit, golden-age and anarchy countdowns; worked plots; gold, research, espionage and the
  AI's gold rushes; every city's `doTurn`; opportunity fire and active defence for every unit; civics,
  trade routes, war weariness and events; the history graphs; `AI_doTurnPost`.

**Loading and freeing the rules**

- **`CvXMLLoadUtility::LoadPreMenuGlobals`** (CvXMLLoadUtilitySet.cpp:768). Loads the XML rule sets needed
  before the main menu: game speeds and options, terrain, eras, techs, promotions, traits, handicaps,
  bonuses, improvements, buildings, projects, civics, leaders, units, civilizations and others. It finishes
  building classes, vote sources and unit classes in a third pass, sorts leaders and civilizations, registers
  the cursor types and counts the playable civilizations.
- **`CvXMLLoadUtility::LoadPostMenuGlobals`** (CvXMLLoadUtilitySet.cpp:949). Loads the rest when a game
  starts: throne room, events and their triggers, routes and rivers, processes, missions, commands,
  automations, votes, cameras, interface modes, formations and diplomacy.
- **`CvGlobals::deleteInfoArrays`** (CvGlobals.cpp:3809). Frees every loaded rule table, one line per
  table. Called on a reload (`doResetInfoClasses`) and at cleanup (`CleanUpGlobalVariables`).

**The interface**

- **`CvDLLWidgetData::parseHelp`** (CvDLLWidgetData.cpp:53). Writes the tooltip for whatever the mouse is
  over: one switch over the widget types, each case calling its own help builder.

## What a rewrite has to keep

Each point is checked in `../hardcoded.md`, with the lines it rests on.

1. **The exported names.** `CvGame::update`, `CvPlayer::setTurnActive`, both XML loaders and `parseHelp`
   are called by the exe by their compiled names. Name, argument types, class and `const` must stay as in
   the original SDK; what happens inside may change.
2. **Enum values.** The exe was compiled with the original `CvEnums.h`. RoM keeps every original value
   and only adds at the end of an enum. New values go at the end, never in the middle.
3. **Switches.** `parseHelp` has no case, and no default, for some widget types; their tooltip stays empty.
   The explore switch in `CvUnitAI::AI_update` has no case for `DOMAIN_IMMOBILE` and falls to a default that
   only asserts. A rewrite that changes these changes what happens for those values.
4. **XML names, paths and order.** The loaders name each file by name, folder and element path; module
   files named `*_<file>.xml` add records. Files whose record order mirrors an enum (missions, commands,
   controls, interface modes, yields, commerce and others) must keep that order. The third passes run only
   after the files they refer to are loaded.
5. **Freeing what was loaded.** Every table the loaders fill is freed once in `deleteInfoArrays`. A new
   table needs a line in both places, or it leaks or crashes on a reload.
6. **When Python events fire.** `gameUpdate`, `BeginGameTurn`, `PreEndGameTurn`, `EndGameTurn`,
   `BeginPlayerTurn` and `EndPlayerTurn` have handlers in Revolution, AIAutoPlay, BUG and the event manager,
   which expect them at their place in the turn.
7. **Synchronised random numbers.** `updateMoves` and `doTurn` shuffle the players with the synchronised
   generator when turns are simultaneous. Adding, removing or moving such a call shifts every later random
   result: network games go out of sync, and games replayed from the same seed no longer match.
8. **Return values.** `CvSelectionGroupAI::AI_update` returning true means "stop, objects may be gone";
   its callers break out of their loops on it.
9. **Shared counters.** The active-turn count, a player's turn flag and a group's attack flag are also set
   by other functions, which a rewrite must stay consistent with.
10. **This fork's own fixes.** Lines changed since each file entered the mod's repository are listed by
    commit in `../hardcoded.md` (the turn-count repair, the unit-update watchdog, the border-danger reset,
    the war-AI range strike, the war-log call and others). A rewrite from the original SDK would lose them.
11. **Logs our tools read.** The war log written from `setTurnActive` is read by the war-analysis tools,
    and one AI log line ("setTurnActive for turn") by `research/rome-and-settlers/tools/settlebal.py`.
