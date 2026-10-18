<!-- Rendered by tools/docs.py from operations.md.in. Do not edit; edit the template. -->
# Workers, tile improvements, city builds and unit movement: the human and the AI

Method: `framework.md`. The queries are declared in `study/queries_ops.json` and turned into
figures by `tools/sqlfig.py`; each table states what it counts, who, when and from which source.
Facts come first, readings in section 6. The outcome of the human's build orders at the save
(what still stands, what was replaced) is in `study/data.md`, section 1. The decision rules
fitted to the human's city orders are in `study/human.md`.

## 1. Questions and sources

| Question | Source |
|---|---|
| Q1. What do the human's builders do: which units, which commands, which builds, how far from its cities? | A lines (the human's commands); city founding and capture from FOUND commands and K lines |
| Q2. How many workers do the players have and build, and how much of their worked land is improved? | U lines; the save dump |
| Q3. What do the AIs' workers do? | Harness continuations from each save (section 1.1) |
| Q4. What does the human order in its cities, and how? What do all players complete? | A lines (ORDER); U and N lines |
| Q5. What do AI cities build while at war with the human, with and without danger? | Y lines |
| Q6. How does the human move its units, alone or grouped, and toward what? | A lines (MOVE_TO); W and Q lines; city owners over time |
| Q7. How do the AIs move theirs? | G lines; the continuations |
| Q8. How does the AI code choose builds, worker tasks and attack moves? | `CvCityAI.cpp`, `CvUnitAI.cpp`, `CvPlayerAI.cpp` (GitLab `main`) |

### 1.1 What the sources cannot give

- **Commands, not moves.** An A line is a command. A unit given a far target keeps moving on
  later turns without a new command, so the number of move commands is not the number of moves.
- **No unit identity in A lines.** The command names the unit's type, plot and group size, not
  its id, so one worker cannot be followed from order to order.
- **The AIs act without commands.** Their worker builds and unit moves are not in the log. Their
  completions are (U and N lines), and so are their stacks near enemy land (G lines) and the
  cities at war with a human (Y lines).
- **One save per game, no autosaves.** To see the AIs' workers and units act, the harness
  plays on from each save: one turn and ten turns, every seat played by the AI, the human's
  included (`toolchain/analysis/dump.sh` with a number of turns). The state before is the save
  dump itself, byte-identical to the one `study/data.md` uses. The continuation tables show the
  AI players only, and they describe the turns after the save, not the logged game.
- **Game 1 and game 2** used the first log version: no M, N or Y lines and no save dump, and builds
  are written as numbers. These are mapped to names by the XML load order. Every order's mapped
  build has its tech already held before the order (X lines), in all four games.
- **Distances** are grid distances on the map, without map wrap: the setting is not in the dump.

## 2. Workers and tile improvements

### 2.1 The human's builders

Every unit type that was given a build or route order, with all its commands:

| unit | build | route_to | move_to | automate | other | all_commands |
|---|---|---|---|---|---|---|
| WORKER | 51 | 2 | 59 | 0 | 9 | 121 |
| JAVELINEER | 25 | 0 | 29 | 0 | 30 | 84 |
| SLAVE | 12 | 0 | 12 | 0 | 0 | 24 |
| WORKBOAT | 3 | 0 | 4 | 5 | 0 | 12 |

*orders; who: human; turn: whole game; rows counted: 4; source: A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game1]. Every value counted (4).*

| unit | build | route_to | move_to | automate | other | all_commands |
|---|---|---|---|---|---|---|
| WORKER | 120 | 12 | 101 | 0 | 23 | 256 |
| JAVELINEER | 3 | 0 | 32 | 0 | 60 | 95 |
| WORKBOAT | 3 | 0 | 3 | 5 | 0 | 11 |

*orders; who: human; turn: whole game; rows counted: 3; source: A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game2]. Every value counted (3).*

| unit | build | route_to | move_to | automate | other | all_commands |
|---|---|---|---|---|---|---|
| WORKER | 137 | 28 | 107 | 0 | 2 | 274 |
| JAVELINEER | 29 | 0 | 40 | 0 | 42 | 111 |

*orders; who: human; turn: whole game; rows counted: 2; source: A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game3]. Every value counted (2).*

| unit | build | route_to | move_to | automate | other | all_commands |
|---|---|---|---|---|---|---|
| WORKER | 202 | 24 | 189 | 0 | 18 | 433 |
| ROME_LEGIONARY | 10 | 0 | 68 | 0 | 177 | 255 |
| JAVELINEER | 46 | 0 | 73 | 1 | 68 | 188 |
| HASTATI | 7 | 0 | 34 | 0 | 75 | 116 |
| PRINCIPES | 2 | 0 | 13 | 0 | 44 | 59 |
| WORKBOAT | 9 | 0 | 9 | 8 | 0 | 26 |

*orders; who: human; turn: whole game; rows counted: 6; source: A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game4]. Every value counted (6).*

Each build ordered, with the improvement or route it makes (BuildInfo, appendix), by period:

| build | improvement | route | orders | plots | turns_0_99 | turns_100_199 | turns_200_on | first_turn | last_turn |
|---|---|---|---|---|---|---|---|---|---|
| BUILD_TRACK | NONE | TRACK | 35 | 33 | 18 | 15 | 2 | 47 | 217 |
| BUILD_MINE | MINE | NONE | 24 | 23 | 2 | 13 | 9 | 75 | 217 |
| BUILD_FARM | FARM | NONE | 10 | 9 | 2 | 4 | 4 | 65 | 217 |
| BUILD_PASTURE | PASTURE | NONE | 7 | 6 | 3 | 4 | 0 | 86 | 186 |
| BUILD_CAMP | CAMP | NONE | 5 | 5 | 4 | 1 | 0 | 44 | 151 |
| BUILD_COTTAGE | COTTAGE | NONE | 3 | 2 | 0 | 3 | 0 | 116 | 140 |
| BUILD_FISHING_BOATS | FISHING_BOATS | NONE | 3 | 3 | 0 | 3 | 0 | 101 | 155 |
| BUILD_QUARRY | QUARRY | NONE | 2 | 2 | 0 | 2 | 0 | 103 | 107 |
| BUILD_APPLE_FARM | APPLE_FARM | NONE | 1 | 1 | 0 | 0 | 1 | 217 | 217 |
| BUILD_WINERY | WINERY | NONE | 1 | 1 | 0 | 0 | 1 | 210 | 210 |

*orders; who: human; turn: by order turn; rows counted: 10; source: A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game1]. Every value counted (10).*

| build | improvement | route | orders | plots | turns_0_99 | turns_100_199 | turns_200_on | first_turn | last_turn |
|---|---|---|---|---|---|---|---|---|---|
| BUILD_TRACK | NONE | TRACK | 32 | 27 | 6 | 22 | 4 | 74 | 206 |
| BUILD_MINE | MINE | NONE | 22 | 18 | 3 | 14 | 5 | 78 | 236 |
| BUILD_ROAD | NONE | ROAD | 14 | 11 | 0 | 0 | 14 | 212 | 235 |
| BUILD_PAVED | NONE | PAVED | 11 | 8 | 0 | 0 | 11 | 232 | 236 |
| BUILD_FARM | FARM | NONE | 10 | 6 | 0 | 7 | 3 | 116 | 234 |
| BUILD_QUARRY | QUARRY | NONE | 10 | 5 | 2 | 5 | 3 | 98 | 202 |
| BUILD_CAMP | CAMP | NONE | 8 | 6 | 1 | 7 | 0 | 87 | 199 |
| BUILD_OLIVE_FARM | OLIVE_FARM | NONE | 5 | 4 | 0 | 0 | 5 | 210 | 234 |
| BUILD_COTTAGE | COTTAGE | NONE | 4 | 3 | 2 | 2 | 0 | 96 | 191 |
| BUILD_PASTURE | PASTURE | NONE | 4 | 4 | 1 | 2 | 1 | 71 | 234 |
| BUILD_FISHING_BOATS | FISHING_BOATS | NONE | 3 | 3 | 0 | 2 | 1 | 144 | 201 |
| BUILD_WINERY | WINERY | NONE | 2 | 1 | 0 | 0 | 2 | 211 | 211 |
| BUILD_WORKSHOP | WORKSHOP | NONE | 1 | 1 | 0 | 0 | 1 | 230 | 230 |

*orders; who: human; turn: by order turn; rows counted: 13; source: A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game2]. Every value counted (13).*

| build | improvement | route | orders | plots | turns_0_99 | turns_100_199 | turns_200_on | first_turn | last_turn |
|---|---|---|---|---|---|---|---|---|---|
| BUILD_TRACK | NONE | TRACK | 51 | 50 | 14 | 36 | 1 | 30 | 204 |
| BUILD_COTTAGE | COTTAGE | NONE | 38 | 38 | 7 | 19 | 12 | 68 | 229 |
| BUILD_ROAD | NONE | ROAD | 28 | 24 | 0 | 0 | 28 | 224 | 262 |
| BUILD_FARM | FARM | NONE | 21 | 18 | 1 | 2 | 18 | 34 | 265 |
| BUILD_MINE | MINE | NONE | 16 | 15 | 1 | 3 | 12 | 85 | 266 |
| BUILD_CAMP | CAMP | NONE | 8 | 8 | 2 | 6 | 0 | 26 | 168 |
| BUILD_APPLE_FARM | APPLE_FARM | NONE | 2 | 2 | 0 | 0 | 2 | 221 | 226 |
| BUILD_QUARRY | QUARRY | NONE | 2 | 2 | 0 | 1 | 1 | 128 | 242 |

*orders; who: human; turn: by order turn; rows counted: 8; source: A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game3]. Every value counted (8).*

| build | improvement | route | orders | plots | turns_0_99 | turns_100_199 | turns_200_on | first_turn | last_turn |
|---|---|---|---|---|---|---|---|---|---|
| BUILD_TRACK | NONE | TRACK | 69 | 64 | 17 | 49 | 3 | 53 | 247 |
| BUILD_ROAD | NONE | ROAD | 48 | 43 | 0 | 0 | 48 | 209 | 277 |
| BUILD_MINE | MINE | NONE | 42 | 34 | 4 | 7 | 31 | 67 | 282 |
| BUILD_COTTAGE | COTTAGE | NONE | 35 | 28 | 1 | 25 | 9 | 97 | 239 |
| BUILD_FARM | FARM | NONE | 28 | 21 | 2 | 7 | 19 | 56 | 276 |
| BUILD_PAVED | NONE | PAVED | 14 | 14 | 0 | 0 | 14 | 275 | 285 |
| BUILD_CAMP | CAMP | NONE | 13 | 13 | 5 | 5 | 3 | 49 | 278 |
| BUILD_FISHING_BOATS | FISHING_BOATS | NONE | 9 | 9 | 1 | 5 | 3 | 91 | 259 |
| BUILD_WINERY | WINERY | NONE | 6 | 5 | 0 | 0 | 6 | 238 | 284 |
| BUILD_QUARRY | QUARRY | NONE | 4 | 3 | 0 | 3 | 1 | 128 | 242 |
| BUILD_PASTURE | PASTURE | NONE | 3 | 3 | 0 | 3 | 0 | 179 | 192 |
| BUILD_WORKSHOP | WORKSHOP | NONE | 3 | 3 | 0 | 0 | 3 | 246 | 285 |
| BUILD_OLIVE_FARM | OLIVE_FARM | NONE | 2 | 2 | 0 | 0 | 2 | 234 | 251 |

*orders; who: human; turn: by order turn; rows counted: 13; source: A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game4]. Every value counted (13).*

How far each build order was from the nearest city the human held on that turn:

| distance_to_own_city | improvement_orders | route_orders | all_orders |
|---|---|---|---|
| 1 | 46 | 18 | 64 |
| 2 | 9 | 13 | 22 |
| 3 | 1 | 2 | 3 |
| 4+ | 0 | 2 | 2 |

*orders; who: human; turn: by order turn; rows counted: 4; source: A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game1]. Every value counted (4).*

| distance_to_own_city | improvement_orders | route_orders | all_orders |
|---|---|---|---|
| 1 | 42 | 32 | 74 |
| 2 | 20 | 15 | 35 |
| 3 | 7 | 6 | 13 |
| 4+ | 0 | 4 | 4 |

*orders; who: human; turn: by order turn; rows counted: 4; source: A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game2]. Every value counted (4).*

| distance_to_own_city | improvement_orders | route_orders | all_orders |
|---|---|---|---|
| 1 | 66 | 50 | 116 |
| 2 | 21 | 16 | 37 |
| 3 | 0 | 5 | 5 |
| 4+ | 0 | 8 | 8 |

*orders; who: human; turn: by order turn; rows counted: 4; source: A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game3]. Every value counted (4).*

| distance_to_own_city | improvement_orders | route_orders | all_orders |
|---|---|---|---|
| 1 | 92 | 51 | 143 |
| 2 | 45 | 44 | 89 |
| 3 | 5 | 19 | 24 |
| 4+ | 3 | 17 | 20 |

*orders; who: human; turn: by order turn; rows counted: 4; source: A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game4]. Every value counted (4).*

### 2.2 Workers of every player

Workers built per fifty turns, the human against all AIs together and the AI that built the most:

| period_from | human | all_ais | most_by_one_ai |
|---|---|---|---|
| 0 | 0 | 11 | 1 |
| 50 | 1 | 12 | 2 |
| 100 | 1 | 17 | 3 |
| 150 | 1 | 17 | 4 |
| 200 | 1 | 11 | 3 |

*units built; who: every player; turn: by 50-turn period; rows counted: 5; source: U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game1]. Every value counted (5).*

| period_from | human | all_ais | most_by_one_ai |
|---|---|---|---|
| 0 | 0 | 12 | 1 |
| 50 | 1 | 15 | 2 |
| 100 | 0 | 15 | 2 |
| 150 | 0 | 10 | 3 |
| 200 | 0 | 50 | 8 |

*units built; who: every player; turn: by 50-turn period; rows counted: 5; source: U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game2]. Every value counted (5).*

| period_from | human | all_ais | most_by_one_ai |
|---|---|---|---|
| 0 | 1 | 11 | 1 |
| 50 | 0 | 14 | 2 |
| 100 | 0 | 15 | 2 |
| 150 | 1 | 21 | 4 |
| 200 | 2 | 65 | 13 |
| 250 | 0 | 26 | 5 |

*units built; who: every player; turn: by 50-turn period; rows counted: 6; source: U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game3]. Every value counted (6).*

| period_from | human | all_ais | most_by_one_ai |
|---|---|---|---|
| 0 | 0 | 12 | 1 |
| 50 | 1 | 10 | 2 |
| 100 | 2 | 14 | 2 |
| 150 | 1 | 19 | 4 |
| 200 | 3 | 88 | 12 |
| 250 | 1 | 79 | 11 |

*units built; who: every player; turn: by 50-turn period; rows counted: 6; source: U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game4]. Every value counted (6).*

Workers, cities and worked land at the save:

| player | human | cities | pop | workers | workers_per_city | worked_land | worked_land_improved |
|---|---|---|---|---|---|---|---|
| 12 | 1 | 13 | 104 | 7 | 0.54 | 106 | 91 |
| 0 | 0 | 5 | 40 | 10 | 2.0 | 31 | 26 |
| 1 | 0 | 6 | 43 | 11 | 1.83 | 44 | 37 |
| 2 | 0 | 9 | 60 | 9 | 1.0 | 34 | 25 |
| 3 | 0 | 5 | 37 | 6 | 1.2 | 35 | 30 |
| 4 | 0 | 5 | 35 | 4 | 0.8 | 24 | 19 |
| 5 | 0 | 3 | 6 | 3 | 1.0 | 9 | 6 |
| 6 | 0 | 13 | 47 | 9 | 0.69 | 39 | 23 |
| 7 | 0 | 1 | 2 | 1 | 1.0 | 3 | 0 |
| 8 | 0 | 3 | 14 | 4 | 1.33 | 15 | 12 |
| 9 | 0 | 11 | 42 | 9 | 0.82 | 39 | 28 |
| 10 | 0 | 12 | 70 | 11 | 0.92 | 61 | 46 |
| 11 | 0 | 10 | 47 | 11 | 1.1 | 34 | 23 |
| 13 | 0 | 11 | 77 | 13 | 1.18 | 64 | 49 |
| 14 | 0 | 5 | 26 | 6 | 1.2 | 24 | 19 |
| 15 | 0 | 6 | 21 | 6 | 1.0 | 17 | 9 |
| 16 | 0 | 4 | 18 | 6 | 1.5 | 14 | 9 |
| 17 | 0 | 7 | 34 | 6 | 0.86 | 30 | 22 |

*units at save; who: every player; turn: save; rows counted: 18; source: units of a type whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), cities and population, and worked plots that are not water (plot_type 3) with and without an improvement, from the save dump [game3]. Every value counted (18).*

| player | human | cities | pop | workers | workers_per_city | worked_land | worked_land_improved |
|---|---|---|---|---|---|---|---|
| 3 | 1 | 26 | 227 | 11 | 0.42 | 123 | 91 |
| 0 | 0 | 14 | 58 | 8 | 0.57 | 52 | 37 |
| 1 | 0 | 2 | 11 | 2 | 1.0 | 12 | 10 |
| 2 | 0 | 2 | 18 | 3 | 1.5 | 17 | 15 |
| 4 | 0 | 15 | 87 | 16 | 1.07 | 67 | 51 |
| 5 | 0 | 15 | 72 | 13 | 0.87 | 73 | 53 |
| 6 | 0 | 6 | 33 | 9 | 1.5 | 34 | 28 |
| 7 | 0 | 7 | 40 | 11 | 1.57 | 30 | 23 |
| 8 | 0 | 15 | 74 | 13 | 0.87 | 70 | 52 |
| 9 | 0 | 9 | 54 | 6 | 0.67 | 52 | 42 |
| 10 | 0 | 9 | 37 | 9 | 1.0 | 33 | 24 |
| 11 | 0 | 21 | 135 | 18 | 0.86 | 101 | 73 |
| 12 | 0 | 9 | 61 | 9 | 1.0 | 36 | 25 |
| 13 | 0 | 12 | 98 | 12 | 1.0 | 78 | 65 |
| 15 | 0 | 7 | 35 | 15 | 2.14 | 29 | 15 |
| 16 | 0 | 10 | 58 | 9 | 0.9 | 39 | 27 |
| 17 | 0 | 12 | 81 | 9 | 0.75 | 66 | 51 |
| 18 | 0 | 14 | 84 | 12 | 0.86 | 73 | 57 |

*units at save; who: every player; turn: save; rows counted: 18; source: units of a type whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), cities and population, and worked plots that are not water (plot_type 3) with and without an improvement, from the save dump [game4]. Every value counted (18).*

### 2.3 What the AIs' workers do

The task each land worker holds at the save, and whether it stood elsewhere one turn later
(AI players only, for the move):

| mission_ai | ai_workers | human_workers | ai_in_a_city | ai_moved_next_turn |
|---|---|---|---|---|
| MISSIONAI_BUILD | 116 | 0 | 3 | 15 |
| NO_MISSIONAI | 9 | 7 | 8 | 0 |

*units at save; who: every player (moves: AI players only); turn: save and save + 1; rows counted: 2; source: land workers at the save by the mission the unit's AI holds (CvUnit mission AI in the dump; MissionAITypes, CvEnums.h), whether they stand in a city, and whether the same unit (id) stands elsewhere after one continuation turn [game3]. Every value counted (2).*

| mission_ai | ai_workers | human_workers | ai_in_a_city | ai_moved_next_turn |
|---|---|---|---|---|
| MISSIONAI_BUILD | 154 | 0 | 5 | 54 |
| NO_MISSIONAI | 20 | 11 | 19 | 10 |

*units at save; who: every player (moves: AI players only); turn: save and save + 1; rows counted: 2; source: land workers at the save by the mission the unit's AI holds (CvUnit mission AI in the dump; MissionAITypes, CvEnums.h), whether they stand in a city, and whether the same unit (id) stands elsewhere after one continuation turn [game4]. Every value counted (2).*

Plots of each AI whose improvement or route changed in the ten turns after the save, against its
land workers:

| player | land_workers_at_save | improvements | routes | changes_per_worker |
|---|---|---|---|---|
| 0 | 10 | 8 | 2 | 1.0 |
| 1 | 11 | 11 | 6 | 1.55 |
| 2 | 9 | 6 | 3 | 1.0 |
| 3 | 6 | 9 | 14 | 3.83 |
| 4 | 4 | 5 | 2 | 1.75 |
| 5 | 3 | 1 | 0 | 0.33 |
| 6 | 9 | 7 | 8 | 1.67 |
| 8 | 4 | 6 | 7 | 3.25 |
| 9 | 9 | 8 | 10 | 2.0 |
| 10 | 11 | 10 | 12 | 2.0 |
| 11 | 11 | 6 | 12 | 1.64 |
| 13 | 13 | 12 | 24 | 2.77 |
| 14 | 6 | 12 | 5 | 2.83 |
| 15 | 6 | 3 | 4 | 1.17 |
| 16 | 6 | 4 | 2 | 1.0 |
| 17 | 6 | 7 | 5 | 2.0 |

*distinct plots; who: AI players; turn: save to save + 10; rows counted: 16; source: plots of each owner (at the end) whose improvement or route changed in the ten-turn continuation, and the owner's land workers at the save [game3]. Every value counted (16).*

| player | land_workers_at_save | improvements | routes | changes_per_worker |
|---|---|---|---|---|
| 0 | 8 | 11 | 14 | 3.13 |
| 1 | 2 | 1 | 3 | 2.0 |
| 2 | 3 | 3 | 9 | 4.0 |
| 4 | 16 | 18 | 17 | 2.19 |
| 5 | 13 | 18 | 19 | 2.85 |
| 6 | 9 | 5 | 4 | 1.0 |
| 7 | 11 | 12 | 5 | 1.55 |
| 8 | 13 | 14 | 23 | 2.85 |
| 9 | 6 | 1 | 3 | 0.67 |
| 10 | 9 | 1 | 0 | 0.11 |
| 11 | 18 | 17 | 29 | 2.56 |
| 12 | 9 | 7 | 6 | 1.44 |
| 13 | 12 | 9 | 7 | 1.33 |
| 15 | 15 | 17 | 9 | 1.73 |
| 16 | 9 | 6 | 3 | 1.0 |
| 17 | 9 | 10 | 27 | 4.11 |
| 18 | 12 | 8 | 31 | 3.25 |

*distinct plots; who: AI players; turn: save to save + 10; rows counted: 17; source: plots of each owner (at the end) whose improvement or route changed in the ten-turn continuation, and the owner's land workers at the save [game4]. Every value counted (17).*

What changed, on AI land. Some changes are not a worker's build: a cottage becomes a hamlet,
and a hamlet a village, by being worked (`ImprovementUpgrade` and `iUpgradeTime` in the appendix).

| improvement_before | improvement_after | plots |
|---|---|---|
| COTTAGE | HAMLET | 12 |
| - | FARM | 11 |
| - | MINE | 11 |
| - | COTTAGE | 10 |
| - | CAMP | 9 |
| - | FISHING_BOATS | 8 |
| - | PASTURE | 6 |
| CAMP | FARM | 6 |
| CAMP | MINE | 6 |
| MINE | COTTAGE | 5 |
| CAMP | COTTAGE | 4 |
| CAMP | PLANTATION | 4 |
| FARM | COTTAGE | 4 |
| COTTAGE | MINE | 3 |
| COTTAGE | QUARRY | 3 |
| - | WORKSHOP | 2 |
| COTTAGE | - | 2 |
| - | OLIVE_FARM | 1 |
| CAMP | APPLE_FARM | 1 |
| CAMP | WINERY | 1 |
| CAMP | WORKSHOP | 1 |
| COTTAGE | CAMP | 1 |
| COTTAGE | PASTURE | 1 |
| COTTAGE | WORKSHOP | 1 |
| HAMLET | VILLAGE | 1 |
| QUARRY | COTTAGE | 1 |

*distinct plots; who: AI players; turn: save to save + 10; rows counted: 26; source: plots whose improvement differs between the save dump and the dump after a harness continuation of ten turns (toolchain/analysis/dump.sh with turns), on plots an AI owns at the end (the human's seat, also played by the AI there, is left out) [game3]. Every value counted (26).*

| improvement_before | improvement_after | plots |
|---|---|---|
| - | MINE | 32 |
| - | COTTAGE | 16 |
| - | FARM | 15 |
| - | CAMP | 11 |
| - | FISHING_BOATS | 9 |
| - | WORKSHOP | 7 |
| CAMP | COTTAGE | 7 |
| CAMP | WORKSHOP | 6 |
| MINE | COTTAGE | 5 |
| - | PASTURE | 4 |
| CAMP | FARM | 4 |
| CAMP | MINE | 3 |
| COTTAGE | FARM | 3 |
| FARM | WORKSHOP | 3 |
| FISHING_BOATS | - | 3 |
| HAMLET | VILLAGE | 3 |
| WORKSHOP | FARM | 3 |
| CAMP | PLANTATION | 2 |
| COTTAGE | HAMLET | 2 |
| COTTAGE | WORKSHOP | 2 |
| MINE | SHAFT_MINE | 2 |
| WORKSHOP | COTTAGE | 2 |
| - | OLIVE_FARM | 1 |
| CAMP | - | 1 |
| CAMP | APPLE_FARM | 1 |
| CAMP | OLIVE_FARM | 1 |
| CAMP | WINERY | 1 |
| COTTAGE | CAMP | 1 |
| COTTAGE | PASTURE | 1 |
| FARM | - | 1 |
| FARM | COTTAGE | 1 |
| HAMLET | FARM | 1 |
| HAMLET | WORKSHOP | 1 |
| MINE | - | 1 |
| MINE | CAMP | 1 |
| SHAFT_MINE | MINE | 1 |

*distinct plots; who: AI players; turn: save to save + 10; rows counted: 36; source: plots whose improvement differs between the save dump and the dump after a harness continuation of ten turns (toolchain/analysis/dump.sh with turns), on plots an AI owns at the end (the human's seat, also played by the AI there, is left out) [game4]. Every value counted (36).*

## 3. City builds

### 3.1 The human's orders

Every city order by what it orders: units by their XML `DefaultUnitAI`. The columns follow the
order flags. No flag replaces the current order; shift appends; ctrl puts the order first and
keeps the current one; alt repeats it (`CvCity::pushOrder`, `CvCity.cpp:12667–12810`).

| category | replace_current | append | insert_first | repeat | all_orders |
|---|---|---|---|---|---|
| building | 83 | 0 | 2 | 0 | 85 |
| unit: COUNTER | 38 | 0 | 0 | 0 | 38 |
| unit: SETTLE | 6 | 2 | 1 | 0 | 9 |
| unit: WORKER_SEA | 7 | 0 | 2 | 0 | 9 |
| unit: ASSAULT_SEA | 3 | 2 | 0 | 0 | 5 |
| unit: WORKER | 3 | 0 | 1 | 0 | 4 |
| unit: MERCHANT | 3 | 0 | 0 | 0 | 3 |

*orders; who: human; turn: whole game; rows counted: 7; source: A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game1]. Every value counted (7).*

| category | replace_current | append | insert_first | repeat | all_orders |
|---|---|---|---|---|---|
| building | 109 | 0 | 0 | 0 | 109 |
| unit: COUNTER | 25 | 0 | 0 | 0 | 25 |
| unit: ATTACK_SEA | 8 | 0 | 0 | 0 | 8 |
| unit: WORKER_SEA | 7 | 0 | 0 | 0 | 7 |
| unit: CITY_DEFENSE | 6 | 0 | 0 | 0 | 6 |
| unit: ASSAULT_SEA | 5 | 0 | 0 | 0 | 5 |
| unit: SETTLE | 5 | 0 | 0 | 0 | 5 |
| unit: ATTACK | 2 | 0 | 0 | 0 | 2 |
| unit: WORKER | 2 | 0 | 0 | 0 | 2 |
| unit: GENERAL | 1 | 0 | 0 | 0 | 1 |

*orders; who: human; turn: whole game; rows counted: 10; source: A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game2]. Every value counted (10).*

| category | replace_current | append | insert_first | repeat | all_orders |
|---|---|---|---|---|---|
| building | 143 | 0 | 0 | 0 | 143 |
| unit: COUNTER | 36 | 0 | 0 | 0 | 36 |
| unit: SETTLE | 7 | 0 | 0 | 0 | 7 |
| process | 4 | 0 | 0 | 0 | 4 |
| unit: WORKER | 4 | 0 | 0 | 0 | 4 |
| unit: MERCHANT | 3 | 0 | 0 | 0 | 3 |
| unit: EXPLORE | 1 | 0 | 0 | 0 | 1 |
| unit: GENERAL | 1 | 0 | 0 | 0 | 1 |

*orders; who: human; turn: whole game; rows counted: 8; source: A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game3]. Every value counted (8).*

| category | replace_current | append | insert_first | repeat | all_orders |
|---|---|---|---|---|---|
| building | 236 | 5 | 3 | 0 | 244 |
| unit: ATTACK_CITY | 33 | 0 | 0 | 0 | 33 |
| unit: COUNTER | 33 | 0 | 0 | 0 | 33 |
| unit: ATTACK | 15 | 0 | 0 | 0 | 15 |
| unit: WORKER_SEA | 15 | 0 | 0 | 0 | 15 |
| unit: ATTACK_SEA | 12 | 1 | 0 | 0 | 13 |
| unit: SETTLE | 12 | 0 | 0 | 0 | 12 |
| unit: WORKER | 8 | 0 | 0 | 0 | 8 |
| unit: ASSAULT_SEA | 7 | 0 | 0 | 0 | 7 |
| unit: CITY_DEFENSE | 2 | 0 | 0 | 0 | 2 |
| unit: EXPLORE | 1 | 0 | 0 | 0 | 1 |

*orders; who: human; turn: whole game; rows counted: 11; source: A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game4]. Every value counted (11).*

### 3.2 What every player completes

Units by `DefaultUnitAI`, and buildings. The first log version has no N lines, so game 1 and
game 2 show units only:

| category | human | human_share | ais | ai_share |
|---|---|---|---|---|
| unit: COUNTER | 34 | 0.557 | 166 | 0.333 |
| unit: SETTLE | 7 | 0.115 | 85 | 0.17 |
| unit: WORKER_SEA | 8 | 0.131 | 74 | 0.148 |
| unit: WORKER | 4 | 0.066 | 68 | 0.136 |
| unit: ASSAULT_SEA | 5 | 0.082 | 42 | 0.084 |
| unit: EXPLORE | 0 | 0.0 | 42 | 0.084 |
| unit: ATTACK_CITY | 0 | 0.0 | 12 | 0.024 |
| unit: ATTACK | 0 | 0.0 | 7 | 0.014 |
| unit: MERCHANT | 3 | 0.049 | 3 | 0.006 |

*units built; who: every player; turn: whole game; rows counted: 9; source: U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game1]. Every value counted (9).*

| category | human | human_share | ais | ai_share |
|---|---|---|---|---|
| unit: COUNTER | 25 | 0.424 | 218 | 0.354 |
| unit: WORKER | 1 | 0.017 | 102 | 0.166 |
| unit: SETTLE | 5 | 0.085 | 86 | 0.14 |
| unit: WORKER_SEA | 7 | 0.119 | 76 | 0.124 |
| unit: ASSAULT_SEA | 5 | 0.085 | 54 | 0.088 |
| unit: EXPLORE | 0 | 0.0 | 44 | 0.072 |
| unit: ATTACK_CITY | 0 | 0.0 | 21 | 0.034 |
| unit: ATTACK | 2 | 0.034 | 12 | 0.02 |
| unit: CITY_DEFENSE | 5 | 0.085 | 2 | 0.003 |
| unit: ATTACK_SEA | 8 | 0.136 | 0 | 0.0 |
| unit: GENERAL | 1 | 0.017 | 0 | 0.0 |

*units built; who: every player; turn: whole game; rows counted: 11; source: U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game2]. Every value counted (11).*

| category | human | human_share | ais | ai_share |
|---|---|---|---|---|
| unit: COUNTER | 34 | 0.19 | 356 | 0.269 |
| building | 130 | 0.726 | 323 | 0.245 |
| unit: WORKER | 4 | 0.022 | 152 | 0.115 |
| unit: WORKER_SEA | 0 | 0.0 | 133 | 0.101 |
| unit: SETTLE | 6 | 0.034 | 128 | 0.097 |
| unit: ASSAULT_SEA | 0 | 0.0 | 107 | 0.081 |
| unit: ATTACK_CITY | 0 | 0.0 | 44 | 0.033 |
| unit: EXPLORE | 1 | 0.006 | 43 | 0.033 |
| unit: ATTACK | 0 | 0.0 | 15 | 0.011 |
| unit: CITY_DEFENSE | 0 | 0.0 | 11 | 0.008 |
| unit: MERCHANT | 3 | 0.017 | 9 | 0.007 |
| unit: GENERAL | 1 | 0.006 | 0 | 0.0 |

*units built; who: every player; turn: whole game; rows counted: 12; source: U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game3]. Every value counted (12).*

| category | human | human_share | ais | ai_share |
|---|---|---|---|---|
| unit: COUNTER | 30 | 0.087 | 989 | 0.346 |
| building | 220 | 0.638 | 750 | 0.263 |
| unit: WORKER_SEA | 15 | 0.043 | 228 | 0.08 |
| unit: WORKER | 8 | 0.023 | 222 | 0.078 |
| unit: ASSAULT_SEA | 6 | 0.017 | 209 | 0.073 |
| unit: SETTLE | 12 | 0.035 | 206 | 0.072 |
| unit: ATTACK_CITY | 26 | 0.075 | 144 | 0.05 |
| unit: EXPLORE | 1 | 0.003 | 41 | 0.014 |
| unit: MERCHANT | 0 | 0.0 | 35 | 0.012 |
| unit: CITY_DEFENSE | 2 | 0.006 | 26 | 0.009 |
| unit: GENERAL | 0 | 0.0 | 4 | 0.001 |
| unit: ATTACK | 14 | 0.041 | 1 | 0.0 |
| unit: ATTACK_SEA | 11 | 0.032 | 0 | 0.0 |

*units built; who: every player; turn: whole game; rows counted: 13; source: U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game4]. Every value counted (13).*

### 3.3 AI cities at war with the human

The order at the head of each AI city's queue on each turn of a war with the human, by threat:

| category | quiet | foreign_units_near | danger | all_city_turns |
|---|---|---|---|---|
| unit: COUNTER | 19 | 4 | 7 | 30 |
| building | 18 | 7 | 0 | 25 |
| unit: WORKER | 1 | 0 | 8 | 9 |
| unit: MERCHANT | 5 | 1 | 0 | 6 |
| unit: WORKER_SEA | 4 | 1 | 0 | 5 |
| unit: ASSAULT_SEA | 3 | 1 | 0 | 4 |
| unit: SETTLE | 2 | 0 | 0 | 2 |

*turns; who: AI players at war with the human; turn: every turn of such a war; rows counted: 7; source: Y lines of AI cities (written when a war with the human starts and every turn of it): the order at the head of the queue, by DefaultUnitAI for units; danger: the AI's danger count of the city; foreign: foreign land units within two plots [game3]. Every value counted (7).*

| category | quiet | foreign_units_near | danger | all_city_turns |
|---|---|---|---|---|
| unit: COUNTER | 99 | 63 | 30 | 192 |
| building | 85 | 43 | 3 | 131 |
| unit: WORKER | 8 | 5 | 9 | 22 |
| unit: SETTLE | 15 | 3 | 0 | 18 |
| unit: ATTACK_CITY | 8 | 2 | 3 | 13 |
| unit: ASSAULT_SEA | 5 | 4 | 0 | 9 |
| unit: GENERAL | 6 | 0 | 2 | 8 |
| unit: WORKER_SEA | 3 | 3 | 2 | 8 |
| unit: MERCHANT | 3 | 1 | 3 | 7 |
| unit: ATTACK | 0 | 0 | 2 | 2 |
| unit: EXPLORE | 0 | 1 | 0 | 1 |

*turns; who: AI players at war with the human; turn: every turn of such a war; rows counted: 11; source: Y lines of AI cities (written when a war with the human starts and every turn of it): the order at the head of the queue, by DefaultUnitAI for units; danger: the AI's danger count of the city; foreign: foreign land units within two plots [game4]. Every value counted (11).*

## 4. Unit movement

### 4.1 The human

Every move command, by the unit's `DefaultUnitAI`:

| unit_ai | peace | war | group_2_plus | group_5_plus | median_distance | max_distance | all_moves |
|---|---|---|---|---|---|---|---|
| COUNTER | 43 | 140 | 13 | 0 | 1.0 | 12 | 183 |
| ASSAULT_SEA | 26 | 47 | 0 | 0 | 3.0 | 22 | 73 |
| WORKER | 48 | 23 | 4 | 0 | 1.0 | 8 | 71 |
| EXPLORE | 10 | 3 | 1 | 0 | 1.0 | 1 | 13 |
| SETTLE | 9 | 2 | 3 | 0 | 1.0 | 7 | 11 |
| WORKER_SEA | 3 | 1 | 0 | 0 | 4.5 | 6 | 4 |
| MERCHANT | 1 | 0 | 0 | 0 | 1.0 | 1 | 1 |

*orders; who: human; turn: whole game; rows counted: 7; source: A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game1]. Every value counted (7).*

| unit_ai | peace | war | group_2_plus | group_5_plus | median_distance | max_distance | all_moves |
|---|---|---|---|---|---|---|---|
| WORKER | 4 | 97 | 41 | 0 | 1.0 | 9 | 101 |
| COUNTER | 1 | 58 | 2 | 0 | 1.0 | 5 | 59 |
| ATTACK_SEA | 0 | 45 | 0 | 0 | 2.0 | 17 | 45 |
| ASSAULT_SEA | 0 | 38 | 19 | 0 | 2.0 | 14 | 38 |
| EXPLORE | 6 | 0 | 0 | 0 | 1.5 | 2 | 6 |
| SETTLE | 0 | 5 | 0 | 0 | 1.0 | 5 | 5 |
| ATTACK | 0 | 3 | 1 | 0 | 1.0 | 1 | 3 |
| GENERAL | 0 | 3 | 1 | 0 | 1.0 | 1 | 3 |
| WORKER_SEA | 0 | 3 | 0 | 0 | 6.0 | 8 | 3 |
| CITY_DEFENSE | 0 | 1 | 0 | 0 | 1.0 | 1 | 1 |
| MISSIONARY | 0 | 1 | 0 | 0 | 5.0 | 5 | 1 |
| PROPHET | 0 | 1 | 0 | 0 | 5.0 | 5 | 1 |

*orders; who: human; turn: whole game; rows counted: 12; source: A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game2]. Every value counted (12).*

| unit_ai | peace | war | group_2_plus | group_5_plus | median_distance | max_distance | all_moves |
|---|---|---|---|---|---|---|---|
| WORKER | 104 | 3 | 0 | 0 | 1.0 | 7 | 107 |
| COUNTER | 47 | 36 | 6 | 0 | 2.0 | 8 | 83 |
| SETTLE | 6 | 0 | 1 | 0 | 6.0 | 8 | 6 |
| MERCHANT | 5 | 0 | 0 | 0 | 4.0 | 5 | 5 |
| PROPHET | 1 | 0 | 0 | 0 | 4.0 | 4 | 1 |

*orders; who: human; turn: whole game; rows counted: 5; source: A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game3]. Every value counted (5).*

| unit_ai | peace | war | group_2_plus | group_5_plus | median_distance | max_distance | all_moves |
|---|---|---|---|---|---|---|---|
| WORKER | 145 | 44 | 28 | 0 | 1.0 | 9 | 189 |
| COUNTER | 83 | 27 | 11 | 0 | 1.0 | 10 | 110 |
| ATTACK_CITY | 0 | 71 | 15 | 3 | 1.0 | 5 | 71 |
| ATTACK_SEA | 2 | 69 | 26 | 0 | 2.0 | 13 | 71 |
| ASSAULT_SEA | 24 | 10 | 1 | 0 | 2.0 | 10 | 34 |
| ATTACK | 6 | 20 | 4 | 2 | 1.0 | 6 | 26 |
| SETTLE | 11 | 3 | 1 | 0 | 3.0 | 8 | 14 |
| WORKER_SEA | 7 | 2 | 0 | 0 | 4.0 | 6 | 9 |
| MISSIONARY | 2 | 0 | 0 | 0 | 4.0 | 5 | 2 |
| GENERAL | 0 | 1 | 0 | 0 | 6.0 | 6 | 1 |
| PROPHET | 1 | 0 | 0 | 0 | 5.0 | 5 | 1 |

*orders; who: human; turn: whole game; rows counted: 11; source: A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game4]. Every value counted (11).*

The move commands of fighting units while at war, against the nearest city of an AI the human was
at war with:

| group_size | closer | same | farther | ending_next_to_enemy_city | median_start_distance | all_moves |
|---|---|---|---|---|---|---|
| 1 | 24 | 2 | 5 | 7 | 7.0 | 31 |
| 2-4 | 4 | 0 | 1 | 2 | 4.0 | 5 |

*orders; who: human; turn: turns at war; rows counted: 2; source: A lines MISSION_MOVE_TO of fighting units (UnitInfo iCombat above zero) made while at war: grid distance (map wrap ignored) from the start and from the target plot to the nearest city of an AI the human was at war with that turn; city owners over time from the save's cities and the K and Z lines on each plot [game3]. Every value counted (2).*

| group_size | closer | same | farther | ending_next_to_enemy_city | median_start_distance | all_moves |
|---|---|---|---|---|---|---|
| 1 | 67 | 26 | 50 | 15 | 8.0 | 143 |
| 2-4 | 30 | 7 | 12 | 18 | 4.0 | 49 |
| 5+ | 2 | 1 | 2 | 1 | 3.0 | 5 |

*orders; who: human; turn: turns at war; rows counted: 3; source: A lines MISSION_MOVE_TO of fighting units (UnitInfo iCombat above zero) made while at war: grid distance (map wrap ignored) from the start and from the target plot to the nearest city of an AI the human was at war with that turn; city owners over time from the save's cities and the K and Z lines on each plot [game4]. Every value counted (3).*

### 4.2 Stacks near or in enemy land

| side | head_ai | stack_turns | turns | median_military_units | max_military_units | with_target |
|---|---|---|---|---|---|---|
| human | COUNTER | 4 | 3 | 3.5 | 4 | 0 |

*turns; who: every player; turn: whole game; rows counted: 1; source: G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game1]. Every value counted (1).*

| side | head_ai | stack_turns | turns | median_military_units | max_military_units | with_target |
|---|---|---|---|---|---|---|
| AI | ATTACK_CITY | 33 | 31 | 6.0 | 8 | 0 |

*turns; who: every player; turn: whole game; rows counted: 1; source: G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game2]. Every value counted (1).*

| side | head_ai | stack_turns | turns | median_military_units | max_military_units | with_target |
|---|---|---|---|---|---|---|
| human | COUNTER | 4 | 4 | 4.0 | 4 | 0 |
| AI | ATTACK_CITY | 47 | 32 | 5.0 | 7 | 1 |
| AI | ATTACK | 24 | 24 | 3.0 | 4 | 1 |

*turns; who: every player; turn: whole game; rows counted: 3; source: G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game3]. Every value counted (3).*

| side | head_ai | stack_turns | turns | median_military_units | max_military_units | with_target |
|---|---|---|---|---|---|---|
| human | ATTACK_CITY | 6 | 6 | 7.5 | 9 | 0 |
| human | ATTACK | 5 | 5 | 2.0 | 9 | 0 |
| human | COUNTER | 3 | 3 | 2.0 | 3 | 0 |
| AI | ATTACK_CITY | 181 | 81 | 6.0 | 10 | 0 |
| AI | ATTACK | 46 | 43 | 4.0 | 7 | 1 |

*turns; who: every player; turn: whole game; rows counted: 5; source: G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game4]. Every value counted (5).*

### 4.3 The AIs' units in the turn after the save

Fighting units of the AIs, by their unit AI type:

| unit_ai | ai_units | ai_moved | ai_mean_distance_moved | ai_in_a_city |
|---|---|---|---|---|
| attack | 106 | 15 | 1.47 | 54 |
| city defense | 72 | 2 | 1.0 | 71 |
| assault sea | 70 | 3 | 2.67 | 64 |
| city counter | 52 | 2 | 1.0 | 46 |
| reserve | 48 | 2 | 1.5 | 33 |
| attack city | 36 | 0 |  | 18 |
| explore | 35 | 11 | 1.82 | 2 |
| counter | 26 | 0 |  | 15 |
| settler sea | 17 | 2 | 4.0 | 11 |
| pillage | 11 | 1 | 1.0 | 4 |
| attack sea | 9 | 0 |  | 2 |
| worker | 5 | 2 | 2.5 | 0 |
| collateral | 3 | 0 |  | 3 |

*units at save; who: AI players; turn: save and save + 1; rows counted: 13; source: fighting units (can_fight) at the save that still exist after one continuation turn (same id), by the unit's AI type at the save: moved or not, grid distance moved (map wrap ignored), and whether it started in a city [game3]. Every value counted (13).*

| unit_ai | ai_units | ai_moved | ai_mean_distance_moved | ai_in_a_city |
|---|---|---|---|---|
| city defense | 212 | 18 | 2.22 | 197 |
| attack | 204 | 101 | 2.19 | 98 |
| reserve | 133 | 27 | 1.7 | 83 |
| assault sea | 128 | 23 | 3.87 | 111 |
| counter | 124 | 55 | 2.22 | 68 |
| city counter | 112 | 13 | 1.92 | 102 |
| attack city | 78 | 20 | 2.05 | 44 |
| explore | 37 | 33 | 2.52 | 5 |
| attack sea | 26 | 16 | 2.88 | 9 |
| settler sea | 24 | 10 | 3.9 | 18 |
| pillage | 22 | 12 | 1.83 | 12 |
| collateral | 16 | 4 | 2.0 | 8 |
| worker | 12 | 9 | 2.89 | 3 |
| explore sea | 2 | 1 | 4.0 | 0 |

*units at save; who: AI players; turn: save and save + 1; rows counted: 14; source: fighting units (can_fight) at the save that still exist after one continuation turn (same id), by the unit's AI type at the save: moved or not, grid distance moved (map wrap ignored), and whether it started in a city [game4]. Every value counted (14).*

## 5. How the AI code chooses

All from GitLab `main`; each line was read in the source.

**City production**, `CvCityAI::AI_chooseProduction` (`CvCityAI.cpp:705–3432`). A list of
conditions in fixed order; the first that holds picks the order. Among them:
- A worker before defenders when `AIDecisionPolicy::developBeforeReinforcing` holds for the enemy
  strength within two plots against the city's own, and the area has fewer workers than
  `AI_neededWorkers` (`CvCityAI.cpp:1504–1519`).
- City defenders while the city has fewer than `AI_minDefenders()` plus the settlers on its plot
  (`CvCityAI.cpp:2253–2256`).
- Late in the list, a unit at all only if unit costs are under the spending cap and the AI is in a
  land war, has at most three cities in the first sixty turns, or wins a roll against its unit
  probability (`CvCityAI.cpp:3288–3296`).
- Many steps are rolls: `AI_chooseUnit` with odds takes the unit only if
  `getSorenRandNum(100) < iOdds` (`CvCityAI.cpp:9444–9446`).

**Workers.**
- How many: `CvPlayerAI::AI_neededWorkers` (`CvPlayerAI.cpp:11912–11945`): twice the unimproved
  bonuses plus three times each city's need, plus one, divided by three, capped by cities and
  population. A city's need counts two for each unimproved worked plot
  (`CvCityAI::AI_updateWorkersNeededHere`, `CvCityAI.cpp:13223`, `13323–13325`).
- What to do: `CvUnitAI::AI_workerMove` (`CvUnitAI.cpp:1546`) works through bonuses, city
  connections, the plot's own city when it needs workers (`CvUnitAI.cpp:1682–1684`), nearby
  plots, then other cities. It chooses another city by need over the workers already there
  (`CvUnitAI.cpp:19322–19325`).
- Which build: `CvCityAI::AI_bestPlotBuild` (`CvCityAI.cpp:11077`) scores the yield change, with
  food weighted `100`, production `60` and commerce `40` per cent before city priorities
  (`CvCityAI.cpp:11536–11540`). The current improvement is kept when nothing scores higher
  (`CvCityAI.cpp:11773–11777`).

**Attack stacks**, `CvUnitAI::AI_attackCityMove` (`CvUnitAI.cpp:2799`):
- The stack is ready only from a group size set per AI (`CvUnitAI.cpp:2868–2872`).
- The target is picked by `AI_pickTargetCity` (`CvUnitAI.cpp:15322`), whose value is divided by
  four plus the square of the path turns (`CvUnitAI.cpp:15429–15431`).
- It attacks when its strength against the city's reaches `BBAI_ATTACK_CITY_STACK_RATIO`
  (`CvUnitAI.cpp:2949`).

## 6. Readings

Each reading names its facts and what would refute it.

1. **The human directs every worker by hand, and lets fighting units build too.**
   - Facts (section 2.1):
     - in all four games, no worker was ever set to automate; the automate commands are of
       boats, scouts, an explorer, warbands and one Javelineer;
     - Javelineers build camps and tracks in all four games, and in game 4 Legionaries and
       other infantry build as well (their `Builds`, appendix).
   - Refuted if: a further game with automated workers doing most of the building.
2. **The human improves the land next to its cities first, with fewer workers than any AI.**
   - Facts:
     - in all four games, most improvement orders are one plot from a city, nearly all within
       two; the orders further out are mostly routes (section 2.1);
     - tracks come first; roads and paved roads only late, when their techs arrive;
     - in no period does the human build more workers than the AI that builds the most, and in
       the later periods far fewer;
     - at the save it has fewer workers per city than every AI in both games, yet improves about
       as large a share of its worked land as they do, or more (section 2.2);
     - it holds more workers at the save than it built in the whole game, in game 3 and game 4
       (U lines against the save).
   - Refuted if: a further game where the human's orders spread evenly over the city radius.
3. **The human's cities build buildings; its units are few and mostly one kind.**
   - Facts (section 3):
     - buildings are the largest category of the human's orders in all four games, and in game 3
       and game 4 the majority of its completions, against about a quarter of the AIs';
     - the AIs complete many more workers, settlers, transports and explorers;
     - the human almost never queues: nearly every order replaces the current one.
   - With `study/human.md`: the units come mostly from the capital.
4. **AI cities at war with the human keep building workers and buildings, also under danger.**
   - Facts (section 3.3):
     - in game 3, the turns with danger show more worker orders than any other kind;
     - in game 4, workers come second after counter units;
     - buildings stay at the head of the queue on many turns with foreign units near.
   - This fits the worker branch of the AI code, which can come before defenders
     (section 5).
   - Refuted if: the danger turns are those of cities the human never reached.
5. **The human moves units one by one in short steps and converges on the target.** The AIs
   move large stacks, and most of their units stand still in a given turn.
   - Facts (section 4):
     - most human move commands are of single units over one or two plots;
     - at war, more of its fighting units' moves bring them closer to an enemy city than take
       them farther;
     - groups of two to four end next to an enemy city more often than single units;
     - the human's stacks near enemy land are few: a handful of stack-turns per game;
     - AI attack stacks near enemy land are many, with a median of five or six units;
     - in the turn after the save, most AI city-defence units stay in their cities, and few or
       none of the AIs' city-attack units move.
   - Refuted if: in a further game, the human's attacks come from stacks formed far from the
     target.

## 7. Open

- **Where the human's extra workers came from.** Captured workers leave no line in the log.
- **The AIs' worker builds during the logged games.** Only their outcome at the save, and the
  continuations, are available. Saves at intervals would show them.
- **Moves against move commands.** A harness replay of the human's commands would separate
  orders from the moves they cause.
- **The AI's choices by branch.** A continuation with the AI's own log on would name the branch
  of `AI_chooseProduction` behind each order. That needs a harness build with logging.

## Appendix: XML records of the types counted

| UnitInfo | Fields set (records.json) |
|---|---|
| JAVELINEER | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":10},{"BonusType":"BONUS_OBSIDIAN","iProductonModifier":10}]; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true}]; `Class` UNITCLASS_JAVELINEER; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true}]; `PrereqTech` TECH_HUNTING; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SPEARMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELINEER","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 3; `iCombatLimit` 100; `iConscription` 2; `iCost` 25; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 4; `iWithdrawalProb` 25; `iWorkRate` 100; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| SLAVE | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_FARM","bBuild":true},{"BuildType":"BUILD_MINE","bBuild":true},{"BuildType":"BUILD_SHAFT_MINE","bBuild":true},{"BuildType":"BUILD_MODERN_MINE","bBuild":true},{"BuildType":"BUILD_WORKSHOP","bBuild":true},{"BuildType":"BUILD_LUMBERMILL","bBuild":true},{"BuildType":"BUILD_WINDMILL","bBuild":true},{"BuildType":"BUILD_WATERMILL","bBuild":true},{"BuildType":"BUILD_PLANTATION","bBuild":true},{"BuildType":"BUILD_SILK_FARM","bBuild":true},{"BuildType":"BUILD_OLIVE_FARM","bBuild":true},{"BuildType":"BUILD_APPLE_FARM","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_PASTURE","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true},{"BuildType":"BUILD_WINERY","bBuild":true},{"BuildType":"BUILD_COTTAGE","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_REMOVE_SWAMP","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Capture` UNITCLASS_WORKER; `Class` UNITCLASS_SLAVE; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBuilding` BUILDING_SLAVE_MARKET; `PrereqTech` TECH_SLAVERY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":25}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SLAVE","iRequired":2}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":2,"iMeleeWaveSize":2,"iRangedWaveSize":0}; `iAIWeight` 1; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 25; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100 |
| WORKBOAT | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_FISHING_BOATS","bBuild":true},{"BuildType":"BUILD_WHALING_BOATS","bBuild":true},{"BuildType":"BUILD_JUMPLANE","bBuild":true},{"BuildType":"BUILD_SEA_FORT","bBuild":true},{"BuildType":"BUILD_SEA_AIR_DEFENSE","bBuild":true}]; `Capture` UNITCLASS_WORKBOAT; `Class` UNITCLASS_WORKBOAT; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER_SEA; `Domain` DOMAIN_SEA; `FeatureImpassables` [{"FeatureType":"FEATURE_STORM","bFeatureImpassable":true}]; `FormationType` FORMATION_TYPE_MACHINE; `NotUnitAIs` [{"UnitAIType":"UNITAI_ESCORT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true}]; `PrereqTech` TECH_FISHING; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `TerrainPassableTechs` [{"PassableTech":"TECH_ASTRONOMY","TerrainType":"TERRAIN_OCEAN"}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_MODERN_WORKBOAT","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WORKBOAT","LateArtDefineTag":"ART_DEF_UNIT_WORKBOAT_MODERN","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPrereqBonuses` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 10; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100; `iXPValueDefense` 3 |
| WORKER | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD_ELECTRIC","bBuild":true},{"BuildType":"BUILD_GRAVTUBE","bBuild":true},{"BuildType":"BUILD_JUMPLANE","bBuild":true},{"BuildType":"BUILD_FARM","bBuild":true},{"BuildType":"BUILD_VERTICAL_FARM","bBuild":true},{"BuildType":"BUILD_MINE","bBuild":true},{"BuildType":"BUILD_SHAFT_MINE","bBuild":true},{"BuildType":"BUILD_MODERN_MINE","bBuild":true},{"BuildType":"BUILD_WORKSHOP","bBuild":true},{"BuildType":"BUILD_LUMBERMILL","bBuild":true},{"BuildType":"BUILD_WINDMILL","bBuild":true},{"BuildType":"BUILD_WATERMILL","bBuild":true},{"BuildType":"BUILD_PLANTATION","bBuild":true},{"BuildType":"BUILD_SILK_FARM","bBuild":true},{"BuildType":"BUILD_OLIVE_FARM","bBuild":true},{"BuildType":"BUILD_APPLE_FARM","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_PASTURE","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true},{"BuildType":"BUILD_WELL","bBuild":true},{"BuildType":"BUILD_WINERY","bBuild":true},{"BuildType":"BUILD_COTTAGE","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_REMOVE_SWAMP","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT","bBuild":true},{"BuildType":"BUILD_FOREST_PRESERVE","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT_RAPIDLY","bBuild":true},{"BuildType":"BUILD_GROUNDWATER_WELL","bBuild":true},{"BuildType":"BUILD_TREEFARM","bBuild":true},{"BuildType":"BUILD_HYBRID_FOREST","bBuild":true},{"BuildType":"BUILD_BUNKER","bBuild":true},{"BuildType":"BUILD_FUTURE_BUNKER","bBuild":true},{"BuildType":"BUILD_GREENFACILITY","bBuild":true},{"BuildType":"BUILD_WASTEREFINEMENT","bBuild":true},{"BuildType":"BUILD_DESERTWINDMILL","bBuild":true},{"BuildType":"BUILD_WINDTRAP","bBuild":true},{"BuildType":"BUILD_EXPLORETEMPLE","bBuild":true},{"BuildType":"BUILD_SAFARI","bBuild":true},{"BuildType":"BUILD_GEOTHERMAL_BOREHOLE","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true},{"BuildType":"BUILD_JUNGLE_CAMP","bBuild":true}]; `Capture` UNITCLASS_WORKER; `Class` UNITCLASS_WORKER; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":25}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WORKER","LateArtDefineTag":"ART_DEF_UNIT_WORKERMODERN","iRequired":2}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":2,"iMeleeWaveSize":2,"iRangedWaveSize":0}; `bFood` True; `iAIWeight` 1; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 25; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| JAVELINEER | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":10},{"BonusType":"BONUS_OBSIDIAN","iProductonModifier":10}]; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true}]; `Class` UNITCLASS_JAVELINEER; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true}]; `PrereqTech` TECH_HUNTING; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SPEARMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELINEER","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 3; `iCombatLimit` 100; `iConscription` 2; `iCost` 25; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 4; `iWithdrawalProb` 25; `iWorkRate` 100; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| WORKBOAT | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_FISHING_BOATS","bBuild":true},{"BuildType":"BUILD_WHALING_BOATS","bBuild":true},{"BuildType":"BUILD_JUMPLANE","bBuild":true},{"BuildType":"BUILD_SEA_FORT","bBuild":true},{"BuildType":"BUILD_SEA_AIR_DEFENSE","bBuild":true}]; `Capture` UNITCLASS_WORKBOAT; `Class` UNITCLASS_WORKBOAT; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER_SEA; `Domain` DOMAIN_SEA; `FeatureImpassables` [{"FeatureType":"FEATURE_STORM","bFeatureImpassable":true}]; `FormationType` FORMATION_TYPE_MACHINE; `NotUnitAIs` [{"UnitAIType":"UNITAI_ESCORT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true}]; `PrereqTech` TECH_FISHING; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `TerrainPassableTechs` [{"PassableTech":"TECH_ASTRONOMY","TerrainType":"TERRAIN_OCEAN"}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_MODERN_WORKBOAT","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WORKBOAT","LateArtDefineTag":"ART_DEF_UNIT_WORKBOAT_MODERN","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPrereqBonuses` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 10; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100; `iXPValueDefense` 3 |
| WORKER | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD_ELECTRIC","bBuild":true},{"BuildType":"BUILD_GRAVTUBE","bBuild":true},{"BuildType":"BUILD_JUMPLANE","bBuild":true},{"BuildType":"BUILD_FARM","bBuild":true},{"BuildType":"BUILD_VERTICAL_FARM","bBuild":true},{"BuildType":"BUILD_MINE","bBuild":true},{"BuildType":"BUILD_SHAFT_MINE","bBuild":true},{"BuildType":"BUILD_MODERN_MINE","bBuild":true},{"BuildType":"BUILD_WORKSHOP","bBuild":true},{"BuildType":"BUILD_LUMBERMILL","bBuild":true},{"BuildType":"BUILD_WINDMILL","bBuild":true},{"BuildType":"BUILD_WATERMILL","bBuild":true},{"BuildType":"BUILD_PLANTATION","bBuild":true},{"BuildType":"BUILD_SILK_FARM","bBuild":true},{"BuildType":"BUILD_OLIVE_FARM","bBuild":true},{"BuildType":"BUILD_APPLE_FARM","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_PASTURE","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true},{"BuildType":"BUILD_WELL","bBuild":true},{"BuildType":"BUILD_WINERY","bBuild":true},{"BuildType":"BUILD_COTTAGE","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_REMOVE_SWAMP","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT","bBuild":true},{"BuildType":"BUILD_FOREST_PRESERVE","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT_RAPIDLY","bBuild":true},{"BuildType":"BUILD_GROUNDWATER_WELL","bBuild":true},{"BuildType":"BUILD_TREEFARM","bBuild":true},{"BuildType":"BUILD_HYBRID_FOREST","bBuild":true},{"BuildType":"BUILD_BUNKER","bBuild":true},{"BuildType":"BUILD_FUTURE_BUNKER","bBuild":true},{"BuildType":"BUILD_GREENFACILITY","bBuild":true},{"BuildType":"BUILD_WASTEREFINEMENT","bBuild":true},{"BuildType":"BUILD_DESERTWINDMILL","bBuild":true},{"BuildType":"BUILD_WINDTRAP","bBuild":true},{"BuildType":"BUILD_EXPLORETEMPLE","bBuild":true},{"BuildType":"BUILD_SAFARI","bBuild":true},{"BuildType":"BUILD_GEOTHERMAL_BOREHOLE","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true},{"BuildType":"BUILD_JUNGLE_CAMP","bBuild":true}]; `Capture` UNITCLASS_WORKER; `Class` UNITCLASS_WORKER; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":25}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WORKER","LateArtDefineTag":"ART_DEF_UNIT_WORKERMODERN","iRequired":2}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":2,"iMeleeWaveSize":2,"iRangedWaveSize":0}; `bFood` True; `iAIWeight` 1; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 25; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| JAVELINEER | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":10},{"BonusType":"BONUS_OBSIDIAN","iProductonModifier":10}]; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true}]; `Class` UNITCLASS_JAVELINEER; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true}]; `PrereqTech` TECH_HUNTING; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SPEARMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELINEER","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 3; `iCombatLimit` 100; `iConscription` 2; `iCost` 25; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 4; `iWithdrawalProb` 25; `iWorkRate` 100; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| WORKER | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD_ELECTRIC","bBuild":true},{"BuildType":"BUILD_GRAVTUBE","bBuild":true},{"BuildType":"BUILD_JUMPLANE","bBuild":true},{"BuildType":"BUILD_FARM","bBuild":true},{"BuildType":"BUILD_VERTICAL_FARM","bBuild":true},{"BuildType":"BUILD_MINE","bBuild":true},{"BuildType":"BUILD_SHAFT_MINE","bBuild":true},{"BuildType":"BUILD_MODERN_MINE","bBuild":true},{"BuildType":"BUILD_WORKSHOP","bBuild":true},{"BuildType":"BUILD_LUMBERMILL","bBuild":true},{"BuildType":"BUILD_WINDMILL","bBuild":true},{"BuildType":"BUILD_WATERMILL","bBuild":true},{"BuildType":"BUILD_PLANTATION","bBuild":true},{"BuildType":"BUILD_SILK_FARM","bBuild":true},{"BuildType":"BUILD_OLIVE_FARM","bBuild":true},{"BuildType":"BUILD_APPLE_FARM","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_PASTURE","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true},{"BuildType":"BUILD_WELL","bBuild":true},{"BuildType":"BUILD_WINERY","bBuild":true},{"BuildType":"BUILD_COTTAGE","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_REMOVE_SWAMP","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT","bBuild":true},{"BuildType":"BUILD_FOREST_PRESERVE","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT_RAPIDLY","bBuild":true},{"BuildType":"BUILD_GROUNDWATER_WELL","bBuild":true},{"BuildType":"BUILD_TREEFARM","bBuild":true},{"BuildType":"BUILD_HYBRID_FOREST","bBuild":true},{"BuildType":"BUILD_BUNKER","bBuild":true},{"BuildType":"BUILD_FUTURE_BUNKER","bBuild":true},{"BuildType":"BUILD_GREENFACILITY","bBuild":true},{"BuildType":"BUILD_WASTEREFINEMENT","bBuild":true},{"BuildType":"BUILD_DESERTWINDMILL","bBuild":true},{"BuildType":"BUILD_WINDTRAP","bBuild":true},{"BuildType":"BUILD_EXPLORETEMPLE","bBuild":true},{"BuildType":"BUILD_SAFARI","bBuild":true},{"BuildType":"BUILD_GEOTHERMAL_BOREHOLE","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true},{"BuildType":"BUILD_JUNGLE_CAMP","bBuild":true}]; `Capture` UNITCLASS_WORKER; `Class` UNITCLASS_WORKER; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":25}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WORKER","LateArtDefineTag":"ART_DEF_UNIT_WORKERMODERN","iRequired":2}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":2,"iMeleeWaveSize":2,"iRangedWaveSize":0}; `bFood` True; `iAIWeight` 1; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 25; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| HASTATI | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_AXEMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_LIGHT_SWORDSMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_HASTATI","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 7; `iCombatLimit` 100; `iConscription` 8; `iCost` 50; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 10; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| JAVELINEER | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":10},{"BonusType":"BONUS_OBSIDIAN","iProductonModifier":10}]; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true}]; `Class` UNITCLASS_JAVELINEER; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true}]; `PrereqTech` TECH_HUNTING; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SPEARMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELINEER","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 3; `iCombatLimit` 100; `iConscription` 2; `iCost` 25; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 4; `iWithdrawalProb` 25; `iWorkRate` 100; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| PRINCIPES | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_LIGHT_SWORDSMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_ROME_LEGIONARY","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_PRINCIPES","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 8; `iCombatLimit` 100; `iCost` 50; `iCultureGarrison` 6; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 16; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| ROME_LEGIONARY | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_ROME_LEGIONARY; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK_CITY; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_COMITATENSES","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_LEGIONARY","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 4; `iCombat` 10; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 5; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 24; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| WORKBOAT | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_FISHING_BOATS","bBuild":true},{"BuildType":"BUILD_WHALING_BOATS","bBuild":true},{"BuildType":"BUILD_JUMPLANE","bBuild":true},{"BuildType":"BUILD_SEA_FORT","bBuild":true},{"BuildType":"BUILD_SEA_AIR_DEFENSE","bBuild":true}]; `Capture` UNITCLASS_WORKBOAT; `Class` UNITCLASS_WORKBOAT; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER_SEA; `Domain` DOMAIN_SEA; `FeatureImpassables` [{"FeatureType":"FEATURE_STORM","bFeatureImpassable":true}]; `FormationType` FORMATION_TYPE_MACHINE; `NotUnitAIs` [{"UnitAIType":"UNITAI_ESCORT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true}]; `PrereqTech` TECH_FISHING; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `TerrainPassableTechs` [{"PassableTech":"TECH_ASTRONOMY","TerrainType":"TERRAIN_OCEAN"}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_MODERN_WORKBOAT","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WORKBOAT","LateArtDefineTag":"ART_DEF_UNIT_WORKBOAT_MODERN","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPrereqBonuses` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 10; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100; `iXPValueDefense` 3 |
| WORKER | `Advisor` ADVISOR_ECONOMY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD_ELECTRIC","bBuild":true},{"BuildType":"BUILD_GRAVTUBE","bBuild":true},{"BuildType":"BUILD_JUMPLANE","bBuild":true},{"BuildType":"BUILD_FARM","bBuild":true},{"BuildType":"BUILD_VERTICAL_FARM","bBuild":true},{"BuildType":"BUILD_MINE","bBuild":true},{"BuildType":"BUILD_SHAFT_MINE","bBuild":true},{"BuildType":"BUILD_MODERN_MINE","bBuild":true},{"BuildType":"BUILD_WORKSHOP","bBuild":true},{"BuildType":"BUILD_LUMBERMILL","bBuild":true},{"BuildType":"BUILD_WINDMILL","bBuild":true},{"BuildType":"BUILD_WATERMILL","bBuild":true},{"BuildType":"BUILD_PLANTATION","bBuild":true},{"BuildType":"BUILD_SILK_FARM","bBuild":true},{"BuildType":"BUILD_OLIVE_FARM","bBuild":true},{"BuildType":"BUILD_APPLE_FARM","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_PASTURE","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true},{"BuildType":"BUILD_WELL","bBuild":true},{"BuildType":"BUILD_WINERY","bBuild":true},{"BuildType":"BUILD_COTTAGE","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_REMOVE_SWAMP","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT","bBuild":true},{"BuildType":"BUILD_FOREST_PRESERVE","bBuild":true},{"BuildType":"BUILD_SCRUB_FALLOUT_RAPIDLY","bBuild":true},{"BuildType":"BUILD_GROUNDWATER_WELL","bBuild":true},{"BuildType":"BUILD_TREEFARM","bBuild":true},{"BuildType":"BUILD_HYBRID_FOREST","bBuild":true},{"BuildType":"BUILD_BUNKER","bBuild":true},{"BuildType":"BUILD_FUTURE_BUNKER","bBuild":true},{"BuildType":"BUILD_GREENFACILITY","bBuild":true},{"BuildType":"BUILD_WASTEREFINEMENT","bBuild":true},{"BuildType":"BUILD_DESERTWINDMILL","bBuild":true},{"BuildType":"BUILD_WINDTRAP","bBuild":true},{"BuildType":"BUILD_EXPLORETEMPLE","bBuild":true},{"BuildType":"BUILD_SAFARI","bBuild":true},{"BuildType":"BUILD_GEOTHERMAL_BOREHOLE","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true},{"BuildType":"BUILD_JUNGLE_CAMP","bBuild":true}]; `Capture` UNITCLASS_WORKER; `Class` UNITCLASS_WORKER; `Combat` UNITCOMBAT_WORKER; `DefaultUnitAI` UNITAI_WORKER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":25}]; `UnitAIs` [{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WORKER","LateArtDefineTag":"ART_DEF_UNIT_WORKERMODERN","iRequired":2}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":2,"iMeleeWaveSize":2,"iRangedWaveSize":0}; `bFood` True; `iAIWeight` 1; `iAdvancedStartCost` 100; `iAsset` 1; `iCost` 25; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iWorkRate` 100 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| BuildInfo | Fields set (records.json) |
|---|---|
| BUILD_APPLE_FARM | `ImprovementType` IMPROVEMENT_APPLE_FARM; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |
| BUILD_CAMP | `FeatureStructs` [{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_CAMP; `PrereqTech` TECH_HUNTING; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_COTTAGE | `ImprovementType` IMPROVEMENT_COTTAGE; `PrereqTech` TECH_POTTERY; `iTime` 400 |
| BUILD_FARM | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300},{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_FARM; `PrereqTech` TECH_AGRICULTURE; `iTime` 500 |
| BUILD_FISHING_BOATS | `ImprovementType` IMPROVEMENT_FISHING_BOATS; `PrereqTech` TECH_FISHING; `bKill` True; `iHotKeyPriority` 1 |
| BUILD_MINE | `ImprovementType` IMPROVEMENT_MINE; `PrereqTech` TECH_MINING; `iTime` 400 |
| BUILD_PASTURE | `ImprovementType` IMPROVEMENT_PASTURE; `PrereqTech` TECH_ANIMAL_HUSBANDRY; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_QUARRY | `ImprovementType` IMPROVEMENT_QUARRY; `PrereqTech` TECH_MASONRY; `iTime` 600 |
| BUILD_TRACK | `RouteType` ROUTE_TRACK; `iTime` 150 |
| BUILD_WINERY | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300}]; `ImprovementType` IMPROVEMENT_WINERY; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| BuildInfo | Fields set (records.json) |
|---|---|
| BUILD_CAMP | `FeatureStructs` [{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_CAMP; `PrereqTech` TECH_HUNTING; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_COTTAGE | `ImprovementType` IMPROVEMENT_COTTAGE; `PrereqTech` TECH_POTTERY; `iTime` 400 |
| BUILD_FARM | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300},{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_FARM; `PrereqTech` TECH_AGRICULTURE; `iTime` 500 |
| BUILD_FISHING_BOATS | `ImprovementType` IMPROVEMENT_FISHING_BOATS; `PrereqTech` TECH_FISHING; `bKill` True; `iHotKeyPriority` 1 |
| BUILD_MINE | `ImprovementType` IMPROVEMENT_MINE; `PrereqTech` TECH_MINING; `iTime` 400 |
| BUILD_OLIVE_FARM | `ImprovementType` IMPROVEMENT_OLIVE_FARM; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |
| BUILD_PASTURE | `ImprovementType` IMPROVEMENT_PASTURE; `PrereqTech` TECH_ANIMAL_HUSBANDRY; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_PAVED | `PrereqTech` TECH_CONSTRUCTION; `RouteType` ROUTE_PAVED; `bShiftDown` True; `iCost` 4; `iTime` 250 |
| BUILD_QUARRY | `ImprovementType` IMPROVEMENT_QUARRY; `PrereqTech` TECH_MASONRY; `iTime` 600 |
| BUILD_ROAD | `PrereqTech` TECH_THE_WHEEL; `RouteType` ROUTE_ROAD; `iCost` 2; `iTime` 200 |
| BUILD_TRACK | `RouteType` ROUTE_TRACK; `iTime` 150 |
| BUILD_WINERY | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300}]; `ImprovementType` IMPROVEMENT_WINERY; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |
| BUILD_WORKSHOP | `ImprovementType` IMPROVEMENT_WORKSHOP; `PrereqTech` TECH_METAL_CASTING; `iTime` 600 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| BuildInfo | Fields set (records.json) |
|---|---|
| BUILD_APPLE_FARM | `ImprovementType` IMPROVEMENT_APPLE_FARM; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |
| BUILD_CAMP | `FeatureStructs` [{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_CAMP; `PrereqTech` TECH_HUNTING; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_COTTAGE | `ImprovementType` IMPROVEMENT_COTTAGE; `PrereqTech` TECH_POTTERY; `iTime` 400 |
| BUILD_FARM | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300},{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_FARM; `PrereqTech` TECH_AGRICULTURE; `iTime` 500 |
| BUILD_MINE | `ImprovementType` IMPROVEMENT_MINE; `PrereqTech` TECH_MINING; `iTime` 400 |
| BUILD_QUARRY | `ImprovementType` IMPROVEMENT_QUARRY; `PrereqTech` TECH_MASONRY; `iTime` 600 |
| BUILD_ROAD | `PrereqTech` TECH_THE_WHEEL; `RouteType` ROUTE_ROAD; `iCost` 2; `iTime` 200 |
| BUILD_TRACK | `RouteType` ROUTE_TRACK; `iTime` 150 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| BuildInfo | Fields set (records.json) |
|---|---|
| BUILD_CAMP | `FeatureStructs` [{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_CAMP; `PrereqTech` TECH_HUNTING; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_COTTAGE | `ImprovementType` IMPROVEMENT_COTTAGE; `PrereqTech` TECH_POTTERY; `iTime` 400 |
| BUILD_FARM | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300},{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_FARM; `PrereqTech` TECH_AGRICULTURE; `iTime` 500 |
| BUILD_FISHING_BOATS | `ImprovementType` IMPROVEMENT_FISHING_BOATS; `PrereqTech` TECH_FISHING; `bKill` True; `iHotKeyPriority` 1 |
| BUILD_MINE | `ImprovementType` IMPROVEMENT_MINE; `PrereqTech` TECH_MINING; `iTime` 400 |
| BUILD_OLIVE_FARM | `ImprovementType` IMPROVEMENT_OLIVE_FARM; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |
| BUILD_PASTURE | `ImprovementType` IMPROVEMENT_PASTURE; `PrereqTech` TECH_ANIMAL_HUSBANDRY; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_PAVED | `PrereqTech` TECH_CONSTRUCTION; `RouteType` ROUTE_PAVED; `bShiftDown` True; `iCost` 4; `iTime` 250 |
| BUILD_QUARRY | `ImprovementType` IMPROVEMENT_QUARRY; `PrereqTech` TECH_MASONRY; `iTime` 600 |
| BUILD_ROAD | `PrereqTech` TECH_THE_WHEEL; `RouteType` ROUTE_ROAD; `iCost` 2; `iTime` 200 |
| BUILD_TRACK | `RouteType` ROUTE_TRACK; `iTime` 150 |
| BUILD_WINERY | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300}]; `ImprovementType` IMPROVEMENT_WINERY; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |
| BUILD_WORKSHOP | `ImprovementType` IMPROVEMENT_WORKSHOP; `PrereqTech` TECH_METAL_CASTING; `iTime` 600 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| ImprovementInfo | Fields set (records.json) |
|---|---|
| - | (none: no record) |
| APPLE_FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_APPLE","YieldChanges":4,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_CURRENCY","TechYields":[0,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_GLOBALIZATION","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| CAMP | `BonusTypeStructs` [[{"BonusType":"BONUS_DEER","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":2500},{"BonusType":"BONUS_FUR","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":3000},{"BonusType":"BONUS_IVORY","YieldChanges":0,2,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COW","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_HORSE","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PIG","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHEEP","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CANNABIS","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SUGAR","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_APPLE","YieldChanges":1,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_OLIVES","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_DYE","YieldChanges":0,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COFFEE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_BANANA","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COTTON","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_INCENSE","YieldChanges":0,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_LEMON","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SPICES","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TEA","YieldChanges":1,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TOBACCO","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_WINE","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `FeatureMakesValids` [{"FeatureType":"FEATURE_FOREST","bMakesValid":true}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATCHLOCK","TechYields":[0,0,1]},{"PrereqTech":"TECH_SEMI_AUTOMATIC_WEAPONS","TechYields":[0,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[2,0,0]}]; `YieldChanges` [1,0,0]; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 5 |
| COTTAGE | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementUpgrade` IMPROVEMENT_HAMLET; `TechYieldChanges` [{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true},{"TerrainType":"TERRAIN_MARSH","bMakesValid":true}]; `YieldChanges` [0,0,1]; `bFreshWaterMakesValid` True; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 10; `iUpgradeTime` 10 |
| FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_CORN","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_RICE","YieldChanges":1,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_WHEAT","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_POTATO","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `IrrigatedYieldChange` [2,0,0]; `PrereqNatureYields` [1,0,0]; `TechYieldChanges` [{"PrereqTech":"TECH_FERMENTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[1,0,0]},{"PrereqTech":"TECH_CROP_ROTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_BIOLOGY","TechYields":[1,0,0]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,0]},{"PrereqTech":"TECH_MACHINE_TOOLS","TechYields":[1,-1,0]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[1,-1,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true},{"TerrainType":"TERRAIN_MARSH","bMakesValid":true}]; `bCarriesIrrigation` True; `bFreshWaterMakesValid` True; `bRequiresFlatlands` True; `bRequiresIrrigation` True; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| FISHING_BOATS | `BonusTypeStructs` [[{"BonusType":"BONUS_CLAM","YieldChanges":3,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CRAB","YieldChanges":2,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_FISH","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PEARLS","YieldChanges":1,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHRIMP","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_SONAR","TechYields":[1,0,1]},{"PrereqTech":"TECH_AQUACULTURE","TechYields":[1,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `bWater` True; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| HAMLET | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementPillage` IMPROVEMENT_COTTAGE; `ImprovementUpgrade` IMPROVEMENT_VILLAGE; `TechYieldChanges` [{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `YieldChanges` [0,0,2]; `iAdvancedStartCost` -1; `iAirBombDefense` 5; `iDefenseModifier` 10; `iPillageGold` 15; `iUpgradeTime` 20 |
| MINE | `BonusTypeStructs` [[{"BonusType":"BONUS_BAUXITE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COAL","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COPPER","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GEMS","YieldChanges":0,-1,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GOLD","YieldChanges":0,-1,6,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_IRON","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SILVER","YieldChanges":0,-1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_URANIUM","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SULPHUR","YieldChanges":0,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_LEAD","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `ImprovementUpgrade` IMPROVEMENT_SHAFT_MINE; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,1,0]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,2,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,2,0]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,0]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_EXPLOSIVES","TechYields":[-1,1,0]},{"PrereqTech":"TECH_SEISMOLOGY","TechYields":[0,1,0]}]; `YieldChanges` [0,1,0]; `bHillsMakesValid` True; `bOutsideBorders` True; `iAdvancedStartCost` 24; `iAirBombDefense` 10; `iPillageGold` 10; `iUpgradeTime` 40 |
| OLIVE_FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_OLIVES","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_CURRENCY","TechYields":[0,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_GLOBALIZATION","TechYields":[0,0,1]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| PASTURE | `BonusTypeStructs` [[{"BonusType":"BONUS_COW","YieldChanges":3,2,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_HORSE","YieldChanges":0,2,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PIG","YieldChanges":4,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHEEP","YieldChanges":3,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_FERMENTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_MATHEMATICS","TechYields":[2,0,0]},{"PrereqTech":"TECH_REFRIGERATION","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[0,0,2]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[2,0,0]}]; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 5 |
| PLANTATION | `BonusTypeStructs` [[{"BonusType":"BONUS_BANANA","YieldChanges":4,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_DYE","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_INCENSE","YieldChanges":0,0,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SPICES","YieldChanges":1,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SUGAR","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CANNABIS","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COFFEE","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_LEMON","YieldChanges":1,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COTTON","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TOBACCO","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_RUBBER","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TEA","YieldChanges":1,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_PESTICIDES","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[0,0,2]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[0,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| QUARRY | `BonusTypeStructs` [[{"BonusType":"BONUS_MARBLE","YieldChanges":0,1,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_STONE","YieldChanges":0,2,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SALT","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_OBSIDIAN","YieldChanges":0,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `RouteYieldChanges` [{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,1,0]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,1,0]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,0]},{"PrereqTech":"TECH_IRON_WORKING","TechYields":[0,1,0]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_EXPLOSIVES","TechYields":[0,1,0]},{"PrereqTech":"TECH_CIVIL_ENGINEERING","TechYields":[0,0,1]},{"PrereqTech":"TECH_ANDROIDS","TechYields":[0,2,0]}]; `bOutsideBorders` True; `iAdvancedStartCost` 36; `iAirBombDefense` 10; `iPillageGold` 5 |
| VILLAGE | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementPillage` IMPROVEMENT_HAMLET; `ImprovementUpgrade` IMPROVEMENT_TOWN; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,0,1]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,0,1]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,0,1]}]; `TechYieldChanges` [{"PrereqTech":"TECH_PRINTING_PRESS","TechYields":[0,0,1]},{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `YieldChanges` [0,0,3]; `bActsAsCity` True; `iAdvancedStartCost` -1; `iAirBombDefense` 5; `iDefenseModifier` 15; `iPillageGold` 20; `iUpgradeTime` 40 |
| WINERY | `BonusTypeStructs` [[{"BonusType":"BONUS_WINE","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 10 |
| WORKSHOP | `PrereqNatureYields` [1,0,0]; `RouteYieldChanges` [{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,1,0]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,1,1]},{"RouteType":"ROUTE_JUMPLANE","RouteYields":[0,1,1]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,1]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_GUILDS","TechYields":[0,1,0]},{"PrereqTech":"TECH_CHEMISTRY","TechYields":[0,1,0]},{"PrereqTech":"TECH_ORGANIC_CHEMISTRY","TechYields":[0,1,0]},{"PrereqTech":"TECH_DNA_COMPUTING","TechYields":[0,0,1]},{"PrereqTech":"TECH_WIRELESS_ELECTRICITY","TechYields":[0,1,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true}]; `YieldChanges` [-1,1,0]; `bFreshWaterMakesValid` True; `bRequiresFlatlands` True; `iAdvancedStartCost` 36; `iAirBombDefense` 5; `iPillageGold` 5 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| ImprovementInfo | Fields set (records.json) |
|---|---|
| - | (none: no record) |
| APPLE_FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_APPLE","YieldChanges":4,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_CURRENCY","TechYields":[0,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_GLOBALIZATION","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| CAMP | `BonusTypeStructs` [[{"BonusType":"BONUS_DEER","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":2500},{"BonusType":"BONUS_FUR","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":3000},{"BonusType":"BONUS_IVORY","YieldChanges":0,2,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COW","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_HORSE","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PIG","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHEEP","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CANNABIS","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SUGAR","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_APPLE","YieldChanges":1,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_OLIVES","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_DYE","YieldChanges":0,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COFFEE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_BANANA","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COTTON","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_INCENSE","YieldChanges":0,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_LEMON","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SPICES","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TEA","YieldChanges":1,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TOBACCO","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_WINE","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `FeatureMakesValids` [{"FeatureType":"FEATURE_FOREST","bMakesValid":true}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATCHLOCK","TechYields":[0,0,1]},{"PrereqTech":"TECH_SEMI_AUTOMATIC_WEAPONS","TechYields":[0,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[2,0,0]}]; `YieldChanges` [1,0,0]; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 5 |
| COTTAGE | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementUpgrade` IMPROVEMENT_HAMLET; `TechYieldChanges` [{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true},{"TerrainType":"TERRAIN_MARSH","bMakesValid":true}]; `YieldChanges` [0,0,1]; `bFreshWaterMakesValid` True; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 10; `iUpgradeTime` 10 |
| FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_CORN","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_RICE","YieldChanges":1,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_WHEAT","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_POTATO","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `IrrigatedYieldChange` [2,0,0]; `PrereqNatureYields` [1,0,0]; `TechYieldChanges` [{"PrereqTech":"TECH_FERMENTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[1,0,0]},{"PrereqTech":"TECH_CROP_ROTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_BIOLOGY","TechYields":[1,0,0]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,0]},{"PrereqTech":"TECH_MACHINE_TOOLS","TechYields":[1,-1,0]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[1,-1,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true},{"TerrainType":"TERRAIN_MARSH","bMakesValid":true}]; `bCarriesIrrigation` True; `bFreshWaterMakesValid` True; `bRequiresFlatlands` True; `bRequiresIrrigation` True; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| FISHING_BOATS | `BonusTypeStructs` [[{"BonusType":"BONUS_CLAM","YieldChanges":3,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CRAB","YieldChanges":2,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_FISH","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PEARLS","YieldChanges":1,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHRIMP","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_SONAR","TechYields":[1,0,1]},{"PrereqTech":"TECH_AQUACULTURE","TechYields":[1,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `bWater` True; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| HAMLET | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementPillage` IMPROVEMENT_COTTAGE; `ImprovementUpgrade` IMPROVEMENT_VILLAGE; `TechYieldChanges` [{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `YieldChanges` [0,0,2]; `iAdvancedStartCost` -1; `iAirBombDefense` 5; `iDefenseModifier` 10; `iPillageGold` 15; `iUpgradeTime` 20 |
| MINE | `BonusTypeStructs` [[{"BonusType":"BONUS_BAUXITE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COAL","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COPPER","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GEMS","YieldChanges":0,-1,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GOLD","YieldChanges":0,-1,6,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_IRON","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SILVER","YieldChanges":0,-1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_URANIUM","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SULPHUR","YieldChanges":0,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_LEAD","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `ImprovementUpgrade` IMPROVEMENT_SHAFT_MINE; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,1,0]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,2,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,2,0]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,0]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_EXPLOSIVES","TechYields":[-1,1,0]},{"PrereqTech":"TECH_SEISMOLOGY","TechYields":[0,1,0]}]; `YieldChanges` [0,1,0]; `bHillsMakesValid` True; `bOutsideBorders` True; `iAdvancedStartCost` 24; `iAirBombDefense` 10; `iPillageGold` 10; `iUpgradeTime` 40 |
| OLIVE_FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_OLIVES","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_CURRENCY","TechYields":[0,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_GLOBALIZATION","TechYields":[0,0,1]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| PASTURE | `BonusTypeStructs` [[{"BonusType":"BONUS_COW","YieldChanges":3,2,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_HORSE","YieldChanges":0,2,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PIG","YieldChanges":4,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHEEP","YieldChanges":3,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_FERMENTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_MATHEMATICS","TechYields":[2,0,0]},{"PrereqTech":"TECH_REFRIGERATION","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[0,0,2]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[2,0,0]}]; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 5 |
| PLANTATION | `BonusTypeStructs` [[{"BonusType":"BONUS_BANANA","YieldChanges":4,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_DYE","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_INCENSE","YieldChanges":0,0,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SPICES","YieldChanges":1,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SUGAR","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CANNABIS","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COFFEE","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_LEMON","YieldChanges":1,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COTTON","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TOBACCO","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_RUBBER","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TEA","YieldChanges":1,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_PESTICIDES","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[0,0,2]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[0,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| SHAFT_MINE | `BonusTypeStructs` [[{"BonusType":"BONUS_BAUXITE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COAL","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COPPER","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GEMS","YieldChanges":0,-1,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GOLD","YieldChanges":0,-1,6,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_IRON","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SILVER","YieldChanges":0,-1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_URANIUM","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SULPHUR","YieldChanges":0,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_LEAD","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `ImprovementPillage` IMPROVEMENT_MINE; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,1,0]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,2,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,2,0]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,0]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_EXPLOSIVES","TechYields":[-1,0,0]},{"PrereqTech":"TECH_SEISMOLOGY","TechYields":[0,1,0]}]; `YieldChanges` [0,2,1]; `bOutsideBorders` True; `iAdvancedStartCost` 48; `iAirBombDefense` 10; `iHappiness` -1; `iPillageGold` 10 |
| VILLAGE | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementPillage` IMPROVEMENT_HAMLET; `ImprovementUpgrade` IMPROVEMENT_TOWN; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,0,1]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,0,1]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,0,1]}]; `TechYieldChanges` [{"PrereqTech":"TECH_PRINTING_PRESS","TechYields":[0,0,1]},{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `YieldChanges` [0,0,3]; `bActsAsCity` True; `iAdvancedStartCost` -1; `iAirBombDefense` 5; `iDefenseModifier` 15; `iPillageGold` 20; `iUpgradeTime` 40 |
| WINERY | `BonusTypeStructs` [[{"BonusType":"BONUS_WINE","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 10 |
| WORKSHOP | `PrereqNatureYields` [1,0,0]; `RouteYieldChanges` [{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,1,0]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,1,1]},{"RouteType":"ROUTE_JUMPLANE","RouteYields":[0,1,1]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,1]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_GUILDS","TechYields":[0,1,0]},{"PrereqTech":"TECH_CHEMISTRY","TechYields":[0,1,0]},{"PrereqTech":"TECH_ORGANIC_CHEMISTRY","TechYields":[0,1,0]},{"PrereqTech":"TECH_DNA_COMPUTING","TechYields":[0,0,1]},{"PrereqTech":"TECH_WIRELESS_ELECTRICITY","TechYields":[0,1,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true}]; `YieldChanges` [-1,1,0]; `bFreshWaterMakesValid` True; `bRequiresFlatlands` True; `iAdvancedStartCost` 36; `iAirBombDefense` 5; `iPillageGold` 5 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `o.game1_builder_commands` | table, 4 values | orders | human | whole game | 4 | A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game1] |
| `o.game2_builder_commands` | table, 3 values | orders | human | whole game | 3 | A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game2] |
| `o.game3_builder_commands` | table, 2 values | orders | human | whole game | 2 | A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game3] |
| `o.game4_builder_commands` | table, 6 values | orders | human | whole game | 6 | A lines (MISSION and COMMAND) of every unit type that was given at least one build or route order; the unit is the one the command names, its group may hold others [game4] |
| `o.game1_build_orders` | table, 10 values | orders | human | by order turn | 10 | A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game1] |
| `o.game2_build_orders` | table, 13 values | orders | human | by order turn | 13 | A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game2] |
| `o.game3_build_orders` | table, 8 values | orders | human | by order turn | 8 | A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game3] |
| `o.game4_build_orders` | table, 13 values | orders | human | by order turn | 13 | A lines MISSION_BUILD (the build named in the order) at the plot where the unit stood; improvement and route from BuildInfo; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game4] |
| `o.game1_build_ring` | table, 4 values | orders | human | by order turn | 4 | A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game1] |
| `o.game2_build_ring` | table, 4 values | orders | human | by order turn | 4 | A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game2] |
| `o.game3_build_ring` | table, 4 values | orders | human | by order turn | 4 | A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game3] |
| `o.game4_build_ring` | table, 4 values | orders | human | by order turn | 4 | A lines MISSION_BUILD: plots from the order to the nearest city the human held on that turn (founded by a FOUND command or captured, K lines; until razed, Z lines); grid distance, map wrap ignored; the first log version (game 1 and game 2) names the build by its BuildTypes index, mapped by the XML load order (every mapped build's PrereqTech was held before its order, X lines) [game4] |
| `o.game1_workers_built` | table, 5 values | units built | every player | by 50-turn period | 5 | U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game1] |
| `o.game2_workers_built` | table, 5 values | units built | every player | by 50-turn period | 5 | U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game2] |
| `o.game3_workers_built` | table, 6 values | units built | every player | by 50-turn period | 6 | U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game3] |
| `o.game4_workers_built` | table, 6 values | units built | every player | by 50-turn period | 6 | U lines of units whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), all domains [game4] |
| `o.game3_workers_at_save` | table, 18 values | units at save | every player | save | 18 | units of a type whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), cities and population, and worked plots that are not water (plot_type 3) with and without an improvement, from the save dump [game3] |
| `o.game4_workers_at_save` | table, 18 values | units at save | every player | save | 18 | units of a type whose DefaultUnitAI is UNITAI_WORKER (UnitInfo), cities and population, and worked plots that are not water (plot_type 3) with and without an improvement, from the save dump [game4] |
| `o.game3_worker_tasks` | table, 2 values | units at save | every player (moves: AI players only) | save and save + 1 | 2 | land workers at the save by the mission the unit's AI holds (CvUnit mission AI in the dump; MissionAITypes, CvEnums.h), whether they stand in a city, and whether the same unit (id) stands elsewhere after one continuation turn [game3] |
| `o.game4_worker_tasks` | table, 2 values | units at save | every player (moves: AI players only) | save and save + 1 | 2 | land workers at the save by the mission the unit's AI holds (CvUnit mission AI in the dump; MissionAITypes, CvEnums.h), whether they stand in a city, and whether the same unit (id) stands elsewhere after one continuation turn [game4] |
| `o.game3_improvement_pace` | table, 16 values | distinct plots | AI players | save to save + 10 | 16 | plots of each owner (at the end) whose improvement or route changed in the ten-turn continuation, and the owner's land workers at the save [game3] |
| `o.game4_improvement_pace` | table, 17 values | distinct plots | AI players | save to save + 10 | 17 | plots of each owner (at the end) whose improvement or route changed in the ten-turn continuation, and the owner's land workers at the save [game4] |
| `o.game3_improvement_changes` | table, 26 values | distinct plots | AI players | save to save + 10 | 26 | plots whose improvement differs between the save dump and the dump after a harness continuation of ten turns (toolchain/analysis/dump.sh with turns), on plots an AI owns at the end (the human's seat, also played by the AI there, is left out) [game3] |
| `o.game4_improvement_changes` | table, 36 values | distinct plots | AI players | save to save + 10 | 36 | plots whose improvement differs between the save dump and the dump after a harness continuation of ten turns (toolchain/analysis/dump.sh with turns), on plots an AI owns at the end (the human's seat, also played by the AI there, is left out) [game4] |
| `o.game1_city_orders` | table, 7 values | orders | human | whole game | 7 | A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game1] |
| `o.game2_city_orders` | table, 10 values | orders | human | whole game | 10 | A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game2] |
| `o.game3_city_orders` | table, 8 values | orders | human | whole game | 8 | A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game3] |
| `o.game4_city_orders` | table, 11 values | orders | human | whole game | 11 | A lines ORDER: the order type (OrderTypes: 0 train, 1 construct, 2 create, 3 maintain), units by their DefaultUnitAI (UnitInfo); flags alt, shift, ctrl as CvNetPushOrder::Execute passes them to CvCity::pushOrder (CvMessageData.cpp:186-192): no flag pops the current order and puts the new one first, shift appends, ctrl puts it first and keeps the current one, alt repeats (CvCity.cpp:12667-12810) [game4] |
| `o.game1_completions` | table, 9 values | units built | every player | whole game | 9 | U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game1] |
| `o.game2_completions` | table, 11 values | units built | every player | whole game | 11 | U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game2] |
| `o.game3_completions` | table, 12 values | units built | every player | whole game | 12 | U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game3] |
| `o.game4_completions` | table, 13 values | units built | every player | whole game | 13 | U lines (units, by DefaultUnitAI in UnitInfo) and N lines (buildings) of every player; shares of each side's completions [game4] |
| `o.game3_ai_orders_under_threat` | table, 7 values | turns | AI players at war with the human | every turn of such a war | 7 | Y lines of AI cities (written when a war with the human starts and every turn of it): the order at the head of the queue, by DefaultUnitAI for units; danger: the AI's danger count of the city; foreign: foreign land units within two plots [game3] |
| `o.game4_ai_orders_under_threat` | table, 11 values | turns | AI players at war with the human | every turn of such a war | 11 | Y lines of AI cities (written when a war with the human starts and every turn of it): the order at the head of the queue, by DefaultUnitAI for units; danger: the AI's danger count of the city; foreign: foreign land units within two plots [game4] |
| `o.game1_human_moves` | table, 7 values | orders | human | whole game | 7 | A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game1] |
| `o.game2_human_moves` | table, 12 values | orders | human | whole game | 12 | A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game2] |
| `o.game3_human_moves` | table, 5 values | orders | human | whole game | 5 | A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game3] |
| `o.game4_human_moves` | table, 11 values | orders | human | whole game | 11 | A lines MISSION_MOVE_TO: the unit named (its DefaultUnitAI in UnitInfo; its group size at the order), from its plot to the target plot (grid distance, map wrap ignored); war: a W line of the human not yet ended by a Q line of the same pair [game4] |
| `o.game3_war_moves` | table, 2 values | orders | human | turns at war | 2 | A lines MISSION_MOVE_TO of fighting units (UnitInfo iCombat above zero) made while at war: grid distance (map wrap ignored) from the start and from the target plot to the nearest city of an AI the human was at war with that turn; city owners over time from the save's cities and the K and Z lines on each plot [game3] |
| `o.game4_war_moves` | table, 3 values | orders | human | turns at war | 3 | A lines MISSION_MOVE_TO of fighting units (UnitInfo iCombat above zero) made while at war: grid distance (map wrap ignored) from the start and from the target plot to the nearest city of an AI the human was at war with that turn; city owners over time from the save's cities and the K and Z lines on each plot [game4] |
| `o.game1_stacks` | table, 1 values | turns | every player | whole game | 1 | G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game1] |
| `o.game2_stacks` | table, 1 values | turns | every player | whole game | 1 | G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game2] |
| `o.game3_stacks` | table, 3 values | turns | every player | whole game | 3 | G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game3] |
| `o.game4_stacks` | table, 5 values | turns | every player | whole game | 5 | G lines (after a player's moves, each stack near or in enemy land: AI stacks of three or more military units, human stacks of two or more); head_ai: the unit AI of the stack's head; with target: a mission plot set [game4] |
| `o.game3_unit_moves` | table, 13 values | units at save | AI players | save and save + 1 | 13 | fighting units (can_fight) at the save that still exist after one continuation turn (same id), by the unit's AI type at the save: moved or not, grid distance moved (map wrap ignored), and whether it started in a city [game3] |
| `o.game4_unit_moves` | table, 14 values | units at save | AI players | save and save + 1 | 14 | fighting units (can_fight) at the save that still exist after one continuation turn (same id), by the unit's AI type at the save: moved or not, grid distance moved (map wrap ignored), and whether it started in a city [game4] |
