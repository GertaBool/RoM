# AI behaviour over whole games

Four Marathon games played from turn 0 to turn 400 in the headless harness. They run
the real DLL of patch 0016 with the game's own base XML and record what every unit does.
The question: what do the AIs actually do, phase by phase, and where do they waste turns?

## Method

- **Games:** Mediterranean (10 civilizations) and Earth 12 (12 civilizations), seeds 1
  and 2, Marathon, Noble, 400 turns each.
- **Telemetry:** per turn and per player (cities, techs, gold, units, wars, score).
  `HARNESS_UNIT_ACTIVITY=1` adds, for every unit AI type, how many units are in a city,
  asleep or fortified, moved since the previous turn, or unmoved for 10 or 50 turns.
- **Snapshots:** taken at turns 100, 200, 300 and 400, for loading single positions
  again. Writing a snapshot does not change the game: checked against a run without
  snapshots, which was identical through turn 130.
- **Tools:** [tools/game-phases.py](tools/game-phases.py) (phase summary) and
  [tools/unit-activity.py](tools/unit-activity.py) (what units do).

Limits: the harness does not run RoM's Python. The rules that change the game are
mirrored in C++, but Revolution, BarbarianCiv and TechDiffusion are not run (see
[the harness README](../../toolchain/harness/README.md)).

## The four games in numbers

Means of the four games; "median AI" is the median over the alive civilizations.

| Turns | Turn time | Cities (median AI) | Techs (median AI) | Gold (median AI) | Units per city | Wars at once | Top score share |
|---|---|---|---|---|---|---|---|
| 1-100 | 0.07 s | 1.0 | 4.3 | 26 | 1.8 | 0.0 | 11 % |
| 101-200 | 0.28 s | 1.7 | 8.5 | 65 | 3.3 | 0.2 | 12 % |
| 201-300 | 0.53 s | 3.8 | 13.3 | 15 | 3.8 | 1.3 | 15 % |
| 301-400 | 1.37 s | 8.4 | 21.3 | 383 | 6.0 | 3.6 | 21 % |

The first war comes after turn 150. Turn time grows twentyfold, with the number of
units. The leader's share of the total score doubles.

## Findings

### 1. One civilization never founds a city (Earth 12)

Genghis Khan has no city for the whole game, in every Earth 12 game of this study and
of all earlier campaigns. Those games had 11 working civilizations, not 12.

- His starting plot (69,34) is plains without fresh water or coast. RoM allows cities
  on plains only with one of the two (`CIV4TerrainInfos.xml`), so he cannot found in
  place.
- On turn 1 his settler walks to (71,34). China then founds its capital next to it, and
  that plot becomes invalid too (minimum city distance 1).
- From then on `CvUnitAI::AI_found` accepts a land site only if the settler's group can
  defend itself or someone guards the site. A player without cities has no city to
  train an escort and no other unit, so the settler waits forever.
- The original RoM DLL from before these patches (d8cedd5) behaves the same.

**Fixed in patch 0017** ([fixes](../../fixes/README.md#settler-without-cities-interface-redraws-and-turn-time)):
a player without cities lets its settler travel alone. Genghis then founds his capital
on turn 1. Three lines in `AI_found`.

### 2. Expansion starts late, and settlers wait

The median AI has one city for the first 100 turns and 1.7 by turn 200.

- **Agriculture first.** RoM requires Agriculture for settlers. At turn 100, only 5 of
  10 Mediterranean AIs have it, although it has no prerequisites.
- **Settlers wait for escorts.**
  - Example: Mediterranean player 8's first settler was trained on turn 70. It stayed
    in the capital until turn 97, then founded on turn 101.
  - A settler leaves only with a defender. A defender is lent only if the city has
    more than its minimum garrison, so the city first has to train one more unit,
    which takes 15 to 30 early Marathon turns.
  - The Mediterranean scenario has barbarians turned off.
- **Over all games,** two thirds of settler time in turns 101-300 is spent inside a
  city, and a third of it unmoved for 10 turns or more.

### 3. Units built and then left idle

| Unit role (turns 301-400, per game) | Units | In a city | Unmoved 10+ turns | Unmoved 50+ turns |
|---|---|---|---|---|
| Troop transports (`ASSAULT_SEA`) | 59 | 92 % | 61 % | 17 % |
| Settler ships (`SETTLER_SEA`) | 19 | 75 % | 27 % | 4 % |
| Great Generals (`GENERAL`) | 12 | 78 % | 53 % | 17 % |
| City defenders (`CITY_DEFENSE`) | 78 | 94 % | 65 % | 11 % |

- **Transports.** Most transports wait in port for an invasion that never sails.
  Their share of all units reaches 14 % in one game.
- **Great Generals.** They mostly stay in cities instead of leading units or settling
  as instructors.
- **Explorers.** About 13 per game keep exploring through turn 300, long after the map
  is known. They should be disbanded or given another role.
- **Defenders** sitting still is expected.

### 4. Gold

- **Earth 12:** the median AI has about zero gold for 300 turns. It runs research at
  the maximum and keeps no reserve.
- **Mediterranean:** reserves stay modest until turn 300.
- **Epic** (one 300-turn game for comparison): in the last 50 turns the median AI holds
  25,000 gold and the richest 111,000. Research is already at its maximum, and nothing
  spends the surplus.

### 5. Armies and turn time

- Units per city rise from 1.8 to 6.0 on Marathon, and to 18.7 at the end of the Epic
  game.
- Unit count drives turn time: path searches for unit moves take more than half of a
  late turn ([engine research](../engine/README.md)).
- An army much larger than the AI uses costs the player waiting time without making
  the opponent stronger.

### 6. Python calls

Over a 400-turn game the DLL calls Python 10 to 13 million times. 93 % of these calls
come from three callbacks:

| Callback | What it does |
|---|---|
| `getUnitCostMod` | A missionary discount |
| `getExtraCost` | Always returns 0 |
| `getUpgradePriceOverride` | A replicator discount |

Moving these three into the DLL removes nine in ten calls.

## Faults found in the code

From the [AI hot-loop map](../engine/ai-hotloops-map.md#6-ai-behaviour-faults-noticed),
14 in all. The most visible:

- **`AI_guardCity` sends a defender to the first undefended city in list order, not the
  nearest.** The distance comparison in the loop is dead code.
- **Targets are ranked by one path measure and marched to by another.**
  `AI_attackCityMove` picks its target ignoring enemy units, then walks avoiding them.
- **The "best route" depends on the treasury.** Below the price of a road,
  `getBestRoute` falls back to the cheapest route. Route targets change with the gold
  balance within a turn.
- **Unit upgrade ties are biased** towards the last candidate, and random numbers are
  drawn for candidates that cannot upgrade anyway.

## What to fix first

1. **The no-city settler deadlock.** Fixed in patch 0017.
2. **Settler escorts:** send the settler alone when no danger is in range, or let the
   city's defender go when the city is not threatened. Measure expansion speed and
   settler losses to animals.
3. **Idle transports and settler ships:** build them against a planned operation and
   disband or reuse them after it.
4. **Explorers and Great Generals:** retire explorers once the map is known; use
   generals.
5. **The three Python callbacks:** move them into the DLL.
