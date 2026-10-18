<!-- Rendered by tools/docs.py from war.md.in. Do not edit; edit the template. -->
# How the human plans, organises and fights its wars

The human's wars in game 3 and game 4, one by one: from the build-up before the declaration, through the
march and the assault, to the peace. Game 3 is Germany, game 4 Rome (P lines). These are the two
games with city-state (Y) lines. Method: `framework.md`. Every table is written by
`tools/warstudy.py` from the war logs, and the tool's header gives each table's source. Section 8
gives the readings, separately from the facts, and section 9 sets them against the literature.

## 1. Questions

- **Q1. Planning.** When does the human go to war, against whom, and with what forces? What does it
  build, upgrade and promote beforehand? Source: W, Q and M lines; U lines; A lines
  (COMMAND_UPGRADE, COMMAND_PROMOTION).
- **Q2. Organisation.** Where is the army when war is declared, how did it get there, and does it
  use ships? Source: Y lines (other players' units within two plots of each target city); A lines
  (move orders, group commands, orders of land units standing on water); naval moves.
- **Q3. Target choice.** Which of the target's cities does it take? Source: Y lines (each city's
  defenders, defence, size, the units near it), K lines; maximum-likelihood strategy classification
  (Bröder, in *Heuristics*, chapter 17).
- **Q4. Execution.** How are the cities taken: how many attacks, at what odds, with which units, in
  what order? Source: C, R, B and K lines.
- **Q5. The end.** When does it make peace, for what, and what happens at home meanwhile? Source: Q
  lines and the peace deal; Y lines of the human's cities; C and K lines with the human defending.

## 2. The wars

| war | target_player | power_ratio | target_cities | cities_taken | first_capture_day | attacks | enemy_units_killed | units_lost | peace_day |
|---|---|---|---|---|---|---|---|---|---|
| game3 203 | 5 | 2.01 | 6 | 5 | 0 | 5 | 4 | 1 | 3 |
| game3 209 | 7 | 3.12 | 2 | 1 | 4 | 9 | 8 | 1 | 5 |
| game4 238 | 14 | 2.6 | 5 | 2 | 0 | 2 | 2 | 0 | 2 |
| game4 252 | 2 | 1.24 | 8 | 1 | 0 | 2 | 2 | 0 | 2 |
| game4 257 | 6 | 2.13 | 7 | 1 | 0 | 3 | 2 | 1 | 4 |
| game4 268 | 7 | 2.15 | 9 | 2 | 0 | 3 | 2 | 1 | 2 |
| game4 271 | 14 | 7.5 | 2 | 2 | 1 | 20 | 20 | 0 | open |
| game4 272 | 10 | 2.78 | 10 | 1 | 0 | 2 | 2 | 0 | open |
| game4 277 | 2 | 3.43 | 7 | 5 | 3 | 36 | 31 | 6 | 8 |
| game4 283 | 7 | 3.93 | 9 | 2 | 1 | 9 | 8 | 1 | open |

*cities; who: human; turn: each war; rows counted: 10; source: warstudy.py on the war logs of game3, game4: W lines of the human team (war: game and declaration turn), the power of both the turn before (M lines), the target's cities on the declaration turn (Y lines), cities taken (K), attacks (C), units killed and lost (R), the peace (Q); days count from the declaration. Every value counted (10).*

- **Game 3:** two wars, each against a single target, with peace before the next.
- **Game 4:** the first four wars run the same way: one target at a time, peace before the next.
  Each of them took one or two cities and ended in peace a few days after the declaration. From
  the fifth declaration on, the wars overlap: the human was at war with several AIs at once, until
  the save.
- **Power ratio.** It was at least two in every war but one (game 4's second).
- **First capture.** In most wars the first city fell on the day of the declaration.

## 3. Planning: the build-up (Q1)

| war_window | counter | attack | attack_city | city_defense | assault_sea | attack_sea | other_units | upgrades | promotions |
|---|---|---|---|---|---|---|---|---|---|
| game3 203, the 30 turns before | 4 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 12 |
| game3 203, the 30 turns before those | 2 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 7 |
| game3 209, the 30 turns before | 6 | 0 | 0 | 0 | 0 | 0 | 2 | 8 | 17 |
| game3 209, the 30 turns before those | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 5 |
| game4 238, the 30 turns before | 6 | 2 | 0 | 0 | 4 | 0 | 5 | 10 | 23 |
| game4 238, the 30 turns before those | 2 | 2 | 0 | 0 | 0 | 0 | 5 | 1 | 5 |
| game4 252, the 30 turns before | 9 | 0 | 0 | 1 | 5 | 0 | 6 | 14 | 31 |
| game4 252, the 30 turns before those | 0 | 4 | 0 | 0 | 0 | 0 | 4 | 2 | 5 |
| game4 257, the 30 turns before | 12 | 0 | 0 | 1 | 4 | 0 | 5 | 14 | 43 |
| game4 257, the 30 turns before those | 0 | 4 | 0 | 0 | 1 | 0 | 6 | 2 | 7 |
| game4 268, the 30 turns before | 6 | 7 | 1 | 2 | 1 | 5 | 7 | 29 | 51 |
| game4 268, the 30 turns before those | 6 | 2 | 0 | 0 | 4 | 0 | 5 | 10 | 23 |
| game4 271, the 30 turns before | 5 | 7 | 3 | 2 | 1 | 8 | 7 | 51 | 59 |
| game4 271, the 30 turns before those | 7 | 2 | 0 | 0 | 4 | 0 | 3 | 14 | 30 |
| game4 272, the 30 turns before | 5 | 7 | 4 | 2 | 1 | 8 | 8 | 53 | 79 |
| game4 272, the 30 turns before those | 7 | 2 | 0 | 0 | 4 | 0 | 3 | 14 | 30 |
| game4 277, the 30 turns before | 5 | 9 | 11 | 2 | 1 | 9 | 9 | 58 | 132 |
| game4 277, the 30 turns before those | 7 | 0 | 0 | 0 | 4 | 0 | 3 | 14 | 27 |
| game4 283, the 30 turns before | 2 | 9 | 21 | 1 | 0 | 11 | 6 | 58 | 171 |
| game4 283, the 30 turns before those | 10 | 0 | 0 | 1 | 5 | 0 | 6 | 14 | 35 |

*units built; who: human; turn: the 60 turns before each declaration; rows counted: 20; source: warstudy.py on the war logs of game3, game4: U lines by DefaultUnitAI (UnitInfo) and A lines COMMAND_UPGRADE and COMMAND_PROMOTION, in the 30 turns before the declaration and the 30 before those; upgrades and promotions are commands. Every value counted (20).*

- **More of everything before each war.** In the thirty turns before each declaration, the human
  built more fighting units than in the thirty turns before those. It also gave more upgrade and
  promotion commands, every time.
- **New kinds of unit before game 4's later wars.** Siege units (DefaultUnitAI ATTACK_CITY) and
  warships (ATTACK_SEA) appear only from the fourth war on. Before the first three wars, the
  ships built are transports (ASSAULT_SEA).

| upgraded_to | game3 203 | game3 209 | game4 238 | game4 252 | game4 257 | game4 268 | game4 271 | game4 272 | game4 277 | game4 283 |
|---|---|---|---|---|---|---|---|---|---|---|
| AUXILIAR | 0 | 0 | 0 | 0 | 0 | 3 | 18 | 20 | 25 | 25 |
| TRIARII | 0 | 0 | 0 | 0 | 0 | 13 | 15 | 15 | 15 | 15 |
| VELITES | 0 | 0 | 10 | 14 | 14 | 7 | 2 | 2 | 2 | 2 |
| ROME_LEGIONARY | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 10 | 10 | 10 |
| PRINCIPES | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 6 | 6 | 6 |
| WARBAND | 2 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| all values | 2 | 8 | 10 | 14 | 14 | 29 | 51 | 53 | 58 | 58 |

*orders; who: human; turn: the 30 turns before each declaration; rows counted: 297; source: warstudy.py on the war logs of game3, game4: A lines COMMAND_UPGRADE, the unit type upgraded to. Every value counted (6).*

- **What the upgrades went to.**
  - Game 3: Warbands, before both wars.
  - Game 4's first three wars: Velites.
  - From the fourth war on: Triarii, Principes, Auxiliaries, and from the fifth also Roman
    Legionaries. These are units of 10 (Legionary) and
    8 (Auxiliary) strength. Velites have
    4 (records in the appendix).

## 4. Organisation: the approach and the staging (Q2)

| war_day | fighting_moves | units_in_them | moves_ending_near | units_ending_near | median_distance_from | median_distance_to |
|---|---|---|---|---|---|---|
| game3 203 day -10 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -9 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -8 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -7 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -6 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -5 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -4 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -3 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -2 | 0 | 0 | 0 | 0 |  |  |
| game3 203 day -1 | 1 | 3 | 1 | 3 | 4 | 2 |
| game3 203 day 0 | 7 | 7 | 5 | 5 | 2 | 1 |
| game3 209 day -10 | 0 | 0 | 0 | 0 |  |  |
| game3 209 day -9 | 0 | 0 | 0 | 0 |  |  |
| game3 209 day -8 | 0 | 0 | 0 | 0 |  |  |
| game3 209 day -7 | 1 | 3 | 0 | 0 | 7 | 6 |
| game3 209 day -6 | 7 | 7 | 0 | 0 | 6 | 6 |
| game3 209 day -5 | 5 | 6 | 0 | 0 | 7 | 8 |
| game3 209 day -4 | 2 | 2 | 0 | 0 | 12.0 | 13.5 |
| game3 209 day -3 | 2 | 2 | 0 | 0 | 13.5 | 13.0 |
| game3 209 day -2 | 0 | 0 | 0 | 0 |  |  |
| game3 209 day -1 | 0 | 0 | 0 | 0 |  |  |
| game3 209 day 0 | 2 | 5 | 1 | 4 | 5.5 | 3.0 |
| game4 238 day -10 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -9 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -8 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -7 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -6 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -5 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -4 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -3 | 1 | 1 | 1 | 1 | 6 | 1 |
| game4 238 day -2 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day -1 | 0 | 0 | 0 | 0 |  |  |
| game4 238 day 0 | 2 | 2 | 2 | 2 | 2.0 | 0.5 |
| game4 252 day -10 | 1 | 1 | 1 | 1 | 1 | 0 |
| game4 252 day -9 | 1 | 2 | 0 | 0 | 0 | 5 |
| game4 252 day -8 | 0 | 0 | 0 | 0 |  |  |
| game4 252 day -7 | 0 | 0 | 0 | 0 |  |  |
| game4 252 day -6 | 1 | 1 | 0 | 0 | 14 | 13 |
| game4 252 day -5 | 0 | 0 | 0 | 0 |  |  |
| game4 252 day -4 | 1 | 1 | 0 | 0 | 13 | 14 |
| game4 252 day -3 | 0 | 0 | 0 | 0 |  |  |
| game4 252 day -2 | 2 | 2 | 0 | 0 | 6.5 | 7.5 |
| game4 252 day -1 | 1 | 3 | 1 | 3 | 5 | 2 |
| game4 252 day 0 | 1 | 3 | 1 | 3 | 2 | 0 |
| game4 257 day -10 | 0 | 0 | 0 | 0 |  |  |
| game4 257 day -9 | 1 | 1 | 0 | 0 | 9 | 10 |
| game4 257 day -8 | 0 | 0 | 0 | 0 |  |  |
| game4 257 day -7 | 2 | 2 | 0 | 0 | 7.0 | 6.5 |
| game4 257 day -6 | 1 | 3 | 0 | 0 | 7 | 4 |
| game4 257 day -5 | 1 | 3 | 0 | 0 | 4 | 4 |
| game4 257 day -4 | 3 | 5 | 0 | 0 | 5 | 6 |
| game4 257 day -3 | 5 | 8 | 0 | 0 | 8 | 7 |
| game4 257 day -2 | 2 | 2 | 0 | 0 | 6.0 | 4.0 |
| game4 257 day -1 | 0 | 0 | 0 | 0 |  |  |
| game4 257 day 0 | 2 | 6 | 2 | 6 | 3.0 | 1.0 |
| game4 268 day -10 | 1 | 1 | 0 | 0 | 10 | 9 |
| game4 268 day -9 | 0 | 0 | 0 | 0 |  |  |
| game4 268 day -8 | 0 | 0 | 0 | 0 |  |  |
| game4 268 day -7 | 0 | 0 | 0 | 0 |  |  |
| game4 268 day -6 | 2 | 2 | 0 | 0 | 7.0 | 8.0 |
| game4 268 day -5 | 0 | 0 | 0 | 0 |  |  |
| game4 268 day -4 | 1 | 1 | 0 | 0 | 9 | 3 |
| game4 268 day -3 | 2 | 2 | 0 | 0 | 7.0 | 3.0 |
| game4 268 day -2 | 1 | 1 | 1 | 1 | 3 | 1 |
| game4 268 day -1 | 0 | 0 | 0 | 0 |  |  |
| game4 268 day 0 | 4 | 4 | 4 | 4 | 2.0 | 0.0 |
| game4 271 day -10 | 0 | 0 | 0 | 0 |  |  |
| game4 271 day -9 | 2 | 2 | 0 | 0 | 15.0 | 14.5 |
| game4 271 day -8 | 0 | 0 | 0 | 0 |  |  |
| game4 271 day -7 | 1 | 1 | 0 | 0 | 13 | 19 |
| game4 271 day -6 | 2 | 2 | 0 | 0 | 15.0 | 19.0 |
| game4 271 day -5 | 1 | 1 | 0 | 0 | 19 | 21 |
| game4 271 day -4 | 0 | 0 | 0 | 0 |  |  |
| game4 271 day -3 | 4 | 4 | 0 | 0 | 14.0 | 15.0 |
| game4 271 day -2 | 0 | 0 | 0 | 0 |  |  |
| game4 271 day -1 | 0 | 0 | 0 | 0 |  |  |
| game4 271 day 0 | 2 | 10 | 1 | 6 | 6.0 | 6.0 |
| game4 272 day -10 | 2 | 2 | 0 | 0 | 14.0 | 15.0 |
| game4 272 day -9 | 0 | 0 | 0 | 0 |  |  |
| game4 272 day -8 | 1 | 1 | 0 | 0 | 13 | 13 |
| game4 272 day -7 | 2 | 2 | 0 | 0 | 14.0 | 13.0 |
| game4 272 day -6 | 1 | 1 | 0 | 0 | 13 | 13 |
| game4 272 day -5 | 0 | 0 | 0 | 0 |  |  |
| game4 272 day -4 | 4 | 4 | 0 | 0 | 8.0 | 8.5 |
| game4 272 day -3 | 0 | 0 | 0 | 0 |  |  |
| game4 272 day -2 | 0 | 0 | 0 | 0 |  |  |
| game4 272 day -1 | 2 | 10 | 0 | 0 | 8.5 | 9.0 |
| game4 272 day 0 | 8 | 12 | 1 | 3 | 7.0 | 8.0 |
| game4 277 day -10 | 0 | 0 | 0 | 0 |  |  |
| game4 277 day -9 | 4 | 4 | 0 | 0 | 13.0 | 14.0 |
| game4 277 day -8 | 0 | 0 | 0 | 0 |  |  |
| game4 277 day -7 | 0 | 0 | 0 | 0 |  |  |
| game4 277 day -6 | 2 | 10 | 0 | 0 | 7.0 | 7.0 |
| game4 277 day -5 | 8 | 12 | 0 | 0 | 4.0 | 3.0 |
| game4 277 day -4 | 8 | 8 | 0 | 0 | 3.0 | 3.0 |
| game4 277 day -3 | 5 | 9 | 0 | 0 | 10 | 11 |
| game4 277 day -2 | 1 | 1 | 0 | 0 | 5 | 7 |
| game4 277 day -1 | 4 | 4 | 1 | 1 | 7.5 | 9.0 |
| game4 277 day 0 | 3 | 8 | 2 | 7 | 3 | 1 |
| game4 283 day -10 | 8 | 8 | 0 | 0 | 14.0 | 15.0 |
| game4 283 day -9 | 5 | 9 | 1 | 2 | 8 | 9 |
| game4 283 day -8 | 1 | 1 | 0 | 0 | 9 | 6 |
| game4 283 day -7 | 4 | 4 | 0 | 0 | 10.0 | 9.0 |
| game4 283 day -6 | 3 | 8 | 1 | 1 | 15 | 17 |
| game4 283 day -5 | 5 | 7 | 1 | 1 | 17 | 18 |
| game4 283 day -4 | 6 | 12 | 0 | 0 | 19.0 | 18.0 |
| game4 283 day -3 | 9 | 15 | 0 | 0 | 9 | 10 |
| game4 283 day -2 | 6 | 6 | 0 | 0 | 20.0 | 19.0 |
| game4 283 day -1 | 8 | 8 | 0 | 0 | 14.0 | 13.0 |
| game4 283 day 0 | 7 | 7 | 2 | 2 | 11 | 7 |

*orders; who: human; turn: the ten days before each declaration that took a city, and the declaration; rows counted: 110; source: warstudy.py on the war logs of game3, game4: A lines MISSION_MOVE_TO of the human's land units other than workers, settlers, explorers and merchants (DefaultUnitAI); units: group sizes; near: the target plot within two plots of a city the human took in that war; distances in grid plots from the unit's plot and from its target plot to the nearest such city. Every value counted (110).*

- **The approach.** In the days before each declaration, the human's fighting units were ordered
  toward the cities it then took. In both games' early wars, the moves of the declaration day ended
  next to those cities, often on them. In game 4's last wars the moves came from further away, and
  ended further from the cities taken, on several fronts at once.
- **How the orders were given.** One order sends a unit or group several turns away, so the table
  shows order days, not every day of the march.

| war | target_cities_with_foreign_units_near | foreign_units_near_first_taken | moves_on_declaration | units_moved | land_moves_from_sea_10_turns | naval_moves_10_turns | group_commands_10_turns |
|---|---|---|---|---|---|---|---|
| game3 203 | 3 | 3 | 8 | 8 | 0 | 0 | 10 |
| game3 209 | 0 | 0 | 2 | 5 | 0 | 0 | 12 |
| game4 238 | 5 | 5 | 6 | 7 | 1 | 2 | 6 |
| game4 252 | 5 | 3 | 4 | 6 | 1 | 9 | 5 |
| game4 257 | 4 | 3 | 4 | 8 | 1 | 9 | 10 |
| game4 268 | 5 | 1 | 10 | 10 | 0 | 9 | 34 |
| game4 271 | 2 | 10 | 8 | 16 | 1 | 18 | 54 |
| game4 272 | 6 | 4 | 18 | 26 | 8 | 26 | 72 |
| game4 277 | 3 | 2 | 9 | 18 | 10 | 40 | 88 |
| game4 283 | 2 | 0 | 10 | 12 | 8 | 32 | 83 |

*orders; who: human; turn: the declaration turn and the ten before; rows counted: 10; source: warstudy.py on the war logs of game3, game4: Y lines of the target's cities on the declaration turn ("foreign": other players' land units within two plots, before the human moves); A lines of the human: MISSION_MOVE_TO on the declaration turn (units: their group sizes), those from ten turns before to the declaration by land units standing on water (COAST, OCEAN) and by ships, and GROUP commands. Every value counted (10).*

- **Staging at the declaration.** At the moment of declaring, before its own moves, several of the
  human's units already stood within two plots of the first city it took in most wars. The
  exceptions are game 3's second war and game 4's last: no unit was near, and the first capture
  came later.
- **Access.** Units cannot enter another player's land in peace without an open-borders agreement.
  The human had made one with every target before the war, long before in most cases. For game 4's
  seventh war it was signed again the turn after the previous peace with that AI. It had one
  with nearly every AI it had met. Open borders are a standing policy, not a deal for one war, and
  they are what let the army stand next to the target's cities before the declaration.

| war | last_open_borders_deal_with_target | turns_before_declaration | ais_with_an_open_borders_deal | ais_met |
|---|---|---|---|---|
| game3 203 | 156 | 47 | 15 | 17 |
| game3 209 | 156 | 53 | 16 | 17 |
| game4 238 | 174 | 64 | 16 | 18 |
| game4 252 | 138 | 114 | 16 | 18 |
| game4 257 | 182 | 75 | 16 | 18 |
| game4 268 | 153 | 115 | 16 | 18 |
| game4 271 | 174 | 97 | 17 | 18 |
| game4 272 | 145 | 127 | 17 | 18 |
| game4 277 | 255 | 22 | 17 | 18 |
| game4 283 | 153 | 130 | 17 | 18 |

*turns; who: human; turn: each declaration turn; rows counted: 10; source: warstudy.py on the war logs of game3, game4: deal items TRADE_OPEN_BORDERS (D lines) between the human and the target before the declaration; open borders let units enter another's land in peace, and a declaration ends them; ais_with_an_open_borders_deal: the AIs with any such deal with the human before the declaration; ais_met: those and the AIs the human had met by the save (diplo). Every value counted (10).*

- **Groups and ships.** Group commands and naval moves were few before the early wars, and grew
  over game 4's wars. Orders given to land units standing on water show sea landings:
  - in single cases before game 4's first three wars;
  - in game 4's last three wars: the most such orders of any wars, and the most naval moves.

## 5. Target choice (Q3)

| war_city | pop | defenders | best_defender | defence_pct | foreign_units_near | distance | day_taken |
|---|---|---|---|---|---|---|---|
| game3 203 33,39 | 4 | 0 | - | 40 | 2 | 2 | 1 |
| game3 203 21,33 | 1 | 1 | JAVELINEER | 0 | 0 | 10 | - |
| game3 203 23,40 | 3 | 1 | JAVELINEER | 10 | 0 | 3 | 1 |
| game3 203 26,40 | 4 | 1 | JAVELINEER | 40 | 3 | 3 | 0 |
| game3 203 28,40 | 2 | 1 | JAVELINEER | 40 | 3 | 3 | 0 |
| game3 203 36,39 | 1 | 1 | JAVELINEER | 30 | 0 | 5 | 3 |
| game3 209 10,39 | 1 | 2 | JAVELINEER | 0 | 0 | 13 | - |
| game3 209 20,44 | 9 | 6 | JAVELINEER | 20 | 0 | 4 | 4 |
| game4 238 29,33 | 3 | 1 | JAVELINEER | 0 | 1 | 3 | 1 |
| game4 238 30,20 | 2 | 1 | JAVELINEER | 0 | 5 | 2 | 0 |
| game4 238 33,29 | 4 | 2 | SPEARMAN | 0 | 10 | 3 | - |
| game4 238 39,20 | 10 | 5 | SPEARMAN | 10 | 7 | 7 | - |
| game4 238 38,23 | 4 | 6 | SPEARMAN | 5 | 7 | 6 | - |
| game4 252 31,33 | 2 | 1 | SPEARMAN | 0 | 3 | 5 | 0 |
| game4 252 35,36 | 8 | 2 | GREEK_PHALANX | 40 | 1 | 9 | - |
| game4 252 44,28 | 6 | 2 | GREEK_PHALANX | 40 | 0 | 12 | - |
| game4 252 47,23 | 4 | 2 | GREEK_PHALANX | 40 | 1 | 15 | - |
| game4 252 42,22 | 15 | 3 | GREEK_PHALANX | 40 | 1 | 10 | - |
| game4 252 43,25 | 4 | 3 | GREEK_PHALANX | 40 | 0 | 11 | - |
| game4 252 37,26 | 6 | 7 | GREEK_PHALANX | 40 | 2 | 5 | - |
| game4 252 46,25 | 6 | 9 | GREEK_PHALANX | 40 | 0 | 14 | - |
| game4 257 41,28 | 1 | 1 | JAVELINEER | 10 | 0 | 9 | - |
| game4 257 42,34 | 1 | 1 | SPEARMAN | 10 | 5 | 10 | - |
| game4 257 33,29 | 3 | 2 | SPEARMAN | 10 | 3 | 3 | 0 |
| game4 257 37,32 | 1 | 2 | SPEARMAN | 40 | 1 | 6 | - |
| game4 257 47,30 | 7 | 3 | SPEARMAN | 40 | 0 | 15 | - |
| game4 257 39,29 | 11 | 4 | SPEARMAN | 50 | 0 | 7 | - |
| game4 257 37,39 | 1 | 6 | SPEARMAN | 10 | 1 | 6 | - |
| game4 268 16,29 | 1 | 1 | SPEARMAN | 10 | 1 | 3 | 0 |
| game4 268 28,20 | 2 | 1 | ARCHER | 10 | 4 | 2 | 0 |
| game4 268 15,21 | 5 | 2 | AXEMAN | 30 | 1 | 8 | - |
| game4 268 17,16 | 1 | 2 | AXEMAN | 10 | 0 | 7 | - |
| game4 268 19,17 | 7 | 2 | AXEMAN | 30 | 0 | 6 | - |
| game4 268 12,23 | 5 | 4 | AXEMAN | 20 | 0 | 7 | - |
| game4 268 25,13 | 9 | 4 | AXEMAN | 60 | 1 | 6 | - |
| game4 268 29,10 | 9 | 4 | AXEMAN | 30 | 1 | 9 | - |
| game4 268 24,17 | 16 | 7 | AXEMAN | 60 | 0 | 6 | - |
| game4 271 39,20 | 10 | 7 | SPEARMAN | 20 | 7 | 7 | 2 |
| game4 271 38,23 | 4 | 12 | SPEARMAN | 10 | 10 | 6 | 1 |
| game4 272 30,16 | 5 | 2 | SPEARMAN | 10 | 4 | 3 | 0 |
| game4 272 55,27 | 5 | 2 | AXEMAN | 40 | 3 | 17 | - |
| game4 272 58,20 | 2 | 2 | SPEARMAN | 10 | 0 | 20 | - |
| game4 272 60,22 | 1 | 2 | SPEARMAN | 10 | 1 | 22 | - |
| game4 272 63,23 | 1 | 2 | RAM | 10 | 1 | 25 | - |
| game4 272 56,25 | 8 | 3 | AXEMAN | 50 | 1 | 18 | - |
| game4 272 58,18 | 3 | 3 | AXEMAN | 20 | 0 | 20 | - |
| game4 272 58,22 | 7 | 3 | AXEMAN | 40 | 0 | 20 | - |
| game4 272 53,22 | 3 | 4 | AXEMAN | 40 | 0 | 15 | - |
| game4 272 62,26 | 4 | 5 | AXEMAN | 50 | 5 | 24 | - |
| game4 277 37,26 | 6 | 2 | GREEK_PHALANX | 40 | 2 | 3 | 5 |
| game4 277 44,28 | 7 | 2 | GREEK_PHALANX | 50 | 0 | 6 | - |
| game4 277 35,36 | 9 | 3 | GREEK_PHALANX | 40 | 0 | 4 | - |
| game4 277 43,25 | 5 | 3 | GREEK_PHALANX | 40 | 0 | 5 | 4 |
| game4 277 47,23 | 5 | 3 | GREEK_PHALANX | 50 | 2 | 8 | 8 |
| game4 277 42,22 | 15 | 11 | GREEK_PHALANX | 50 | 2 | 3 | 3 |
| game4 277 46,25 | 6 | 11 | GREEK_PHALANX | 50 | 0 | 7 | 7 |
| game4 283 14,26 | 1 | 1 | SPEARMAN | 10 | 9 | 3 | 1 |
| game4 283 14,15 | 1 | 2 | ARCHER | 10 | 0 | 9 | - |
| game4 283 15,21 | 6 | 2 | AXEMAN | 30 | 1 | 8 | - |
| game4 283 17,16 | 2 | 2 | AXEMAN | 20 | 0 | 7 | - |
| game4 283 19,17 | 8 | 2 | AXEMAN | 30 | 0 | 6 | - |
| game4 283 23,13 | 1 | 2 | AXEMAN | 10 | 0 | 7 | - |
| game4 283 25,13 | 11 | 3 | AXEMAN | 60 | 0 | 5 | - |
| game4 283 29,10 | 10 | 3 | AXEMAN | 30 | 0 | 6 | - |
| game4 283 24,17 | 17 | 7 | LIGHT_SWORDSMAN | 60 | 0 | 4 | 1 |

*cities; who: the human's targets; turn: each declaration turn; rows counted: 65; source: warstudy.py on the war logs of game3, game4: the first Y line of each city of the target on the declaration turn; distance: grid plots to the nearest city of the human that turn (its Y lines); day_taken: days after the declaration that the human took it in this war (K lines). Every value counted (65).*

| cue | cities_taken | chosen_was_best | error_rate | ln_likelihood | ln_likelihood_guessing | gain_over_guessing |
|---|---|---|---|---|---|---|
| fewest defenders | 17 | 9 | 0.47 | -26.56 | -27.91 | 1.34 |
| lowest defence modifier | 17 | 11 | 0.35 | -26.21 | -27.91 | 1.7 |
| nearest to the human's cities | 17 | 12 | 0.29 | -22.65 | -27.91 | 5.26 |
| most foreign units within two plots | 17 | 10 | 0.41 | -24.35 | -27.91 | 3.56 |
| smallest | 17 | 5 | 0.71 | -25.87 | -27.91 | 2.03 |
| largest | 17 | 5 | 0.71 | -29.74 | -27.91 | -1.84 |
| nearest, then fewest defenders | 17 | 10 | 0.41 | -23.4 | -27.91 | 4.51 |
| nearest, then lowest defence | 17 | 11 | 0.35 | -21.82 | -27.91 | 6.09 |
| most units near, then fewest defenders | 17 | 10 | 0.41 | -23.94 | -27.91 | 3.96 |
| fewest defenders, then nearest | 17 | 7 | 0.59 | -25.88 | -27.91 | 2.03 |
| nearest, then most units near | 17 | 11 | 0.35 | -20.9 | -27.91 | 7.01 |

*cities; who: human; turn: each city taken; rows counted: 17; source: warstudy.py on the war logs of game3, game4: each city the human took (K lines) with more than one city of the target that turn (Y lines); options: those cities; a cue's best options: its least value (defenders, defence modifier, distance to the human's cities including those taken before in the war, size) or most foreign units near; a pair of cues: the second decides among the first's best (take-the-best, Gigerenzer, Heuristics, chapter 14); maximum-likelihood classification with one error rate per cue (Bröder, in Heuristics, chapter 17), e on a grid of hundredths; guessing: each option 1/m; chosen_was_best counts ties as hits. Every value counted (11).*

- **The choice is spatial.** Of the single cues, the nearest city to the human's own is the best
  predictor of which city it took, with the lowest error rate. Next come the city with the most of
  the human's units near it, and the smallest city.
- **Weakness alone predicts less.** Fewest defenders and the lowest defence modifier predict less,
  and the largest city less than guessing.
- **The best rule:** take the nearest city, and among the nearest the one with the most units near
  it. It has the highest likelihood of the rules tried, each with one parameter.
- **The rows above show the pattern.**
  - The cities taken on the day of a declaration were small, near the human's border, defended by
    one or two units, and had the human's units next to them.
  - The target's large, walled cities further away were left, until game 4's last wars.

## 6. Execution (Q4)

| war_day | attacks | median_odds | lowest_odds | siege_unit_attacks | ship_attacks | bombards | units_lost | cities_taken |
|---|---|---|---|---|---|---|---|---|
| game3 203 day 0 | 3 | 779 | 712 | 0 | 0 | 0 | 1 | 2 |
| game3 203 day 1 | 1 | 712 | 712 | 0 | 0 | 0 | 0 | 2 |
| game3 203 day 3 | 1 | 830 | 830 | 0 | 0 | 0 | 0 | 1 |
| game3 209 day 0 | 0 |  |  | 0 | 0 | 0 | 0 | 0 |
| game3 209 day 2 | 4 | 804.0 | 759 | 0 | 0 | 0 | 0 | 0 |
| game3 209 day 3 | 2 | 844.0 | 817 | 0 | 0 | 0 | 1 | 0 |
| game3 209 day 4 | 3 | 914 | 818 | 0 | 0 | 0 | 0 | 1 |
| game4 238 day 0 | 1 | 749 | 749 | 0 | 0 | 0 | 0 | 1 |
| game4 238 day 1 | 1 | 996 | 996 | 0 | 0 | 0 | 0 | 1 |
| game4 252 day 0 | 1 | 915 | 915 | 0 | 0 | 0 | 0 | 1 |
| game4 252 day 1 | 1 | 1000 | 1000 | 0 | 0 | 0 | 0 | 0 |
| game4 257 day 0 | 3 | 915 | 755 | 0 | 0 | 0 | 1 | 1 |
| game4 268 day 0 | 3 | 994 | 767 | 0 | 0 | 0 | 1 | 2 |
| game4 271 day 0 | 6 | 972.0 | 925 | 6 | 0 | 1 | 0 | 0 |
| game4 271 day 1 | 7 | 957 | 586 | 5 | 1 | 0 | 0 | 1 |
| game4 271 day 2 | 7 | 1000 | 997 | 7 | 0 | 0 | 0 | 1 |
| game4 272 day 0 | 2 | 995.5 | 994 | 2 | 0 | 0 | 0 | 1 |
| game4 277 day 0 | 0 |  |  | 0 | 0 | 5 | 0 | 0 |
| game4 277 day 1 | 1 | 753 | 753 | 0 | 0 | 4 | 0 | 0 |
| game4 277 day 2 | 11 | 992 | 355 | 10 | 0 | 2 | 2 | 0 |
| game4 277 day 3 | 2 | 999.0 | 998 | 1 | 0 | 3 | 0 | 1 |
| game4 277 day 4 | 4 | 990.0 | 566 | 3 | 0 | 3 | 1 | 1 |
| game4 277 day 5 | 3 | 737 | 648 | 1 | 0 | 4 | 1 | 1 |
| game4 277 day 6 | 1 | 768 | 768 | 0 | 0 | 4 | 0 | 0 |
| game4 277 day 7 | 5 | 920 | 566 | 4 | 0 | 0 | 0 | 1 |
| game4 283 day 0 | 0 |  |  | 0 | 0 | 4 | 0 | 0 |
| game4 283 day 1 | 9 | 980 | 809 | 6 | 2 | 0 | 1 | 2 |

*battles; who: human; turn: each day with an attack or capture, and the declaration; rows counted: 27; source: warstudy.py on the war logs of game3, game4: C lines with the human attacking the target (odds per mille; siege units: DefaultUnitAI ATTACK_CITY; ships: SEA domain), B lines of the human, R lines with the human losing, K lines. Every value counted (27).*

| war_city | day_taken | defenders_at_declaration | attacks | attacks_in_order_unit_odds | attacks_under_500 |
|---|---|---|---|---|---|
| game3 203 26,40 | 0 | 1 | 2 | WARBAND:712 WARBAND:1000 | 0 |
| game3 203 28,40 | 0 | 1 | 1 | WARBAND:779 | 0 |
| game3 203 33,39 | 1 | 0 | 0 | (walked in) | 0 |
| game3 203 23,40 | 1 | 1 | 1 | WARBAND:712 | 0 |
| game3 203 36,39 | 3 | 1 | 1 | WARBAND:830 | 0 |
| game3 209 20,44 | 4 | 6 | 9 | WARBAND:804 WARBAND:804 WARBAND:804 WARBAND:759 WARBAND:817 WARBAND:871 WARBAND:818 WARBAND:914 WARBAND:941 | 0 |
| game4 238 30,20 | 0 | 1 | 1 | HASTATI:749 | 0 |
| game4 238 29,33 | 1 | 1 | 1 | HASTATI:996 | 0 |
| game4 252 31,33 | 0 | 1 | 1 | HASTATI:915 | 0 |
| game4 257 33,29 | 0 | 2 | 3 | HASTATI:755 HASTATI:915 HASTATI:1000 | 0 |
| game4 268 16,29 | 0 | 1 | 1 | PRINCIPES:995 | 0 |
| game4 268 28,20 | 0 | 1 | 2 | HASTATI:767 HASTATI:994 | 0 |
| game4 271 38,23 | 1 | 12 | 12 | ROME_LEGIONARY:978 ROME_LEGIONARY:925 ROME_LEGIONARY:969 ROME_LEGIONARY:972 ROME_LEGIONARY:972 ROME_LEGIONARY:978 ROME_LEGIONARY:922 ROME_LEGIONARY:925 ROME_LEGIONARY:989 ROME_LEGIONARY:957 ROME_LEGIONARY:586 AUXILIAR:990 | 0 |
| game4 271 39,20 | 2 | 7 | 7 | ROME_LEGIONARY:997 ROME_LEGIONARY:1000 ROME_LEGIONARY:1000 ROME_LEGIONARY:1000 ROME_LEGIONARY:999 ROME_LEGIONARY:1000 ROME_LEGIONARY:1000 | 0 |
| game4 272 30,16 | 0 | 2 | 2 | ROME_LEGIONARY:997 ROME_LEGIONARY:994 | 0 |
| game4 277 42,22 | 3 | 11 | 14 | CENTURIO:753 ROME_LEGIONARY:355 ROME_LEGIONARY:368 ROME_LEGIONARY:723 ROME_LEGIONARY:418 ROME_LEGIONARY:910 ROME_LEGIONARY:992 ROME_LEGIONARY:995 ROME_LEGIONARY:996 ROME_LEGIONARY:997 ROME_LEGIONARY:998 CENTURIO:998 ROME_LEGIONARY:998 CENTURIO:1000 | 3 |
| game4 277 43,25 | 4 | 3 | 4 | ROME_LEGIONARY:566 ROME_LEGIONARY:981 CENTURIO:1000 ROME_LEGIONARY:999 | 0 |
| game4 277 37,26 | 5 | 2 | 3 | ROME_LEGIONARY:648 HASTATI:737 AUXILIAR:866 | 0 |
| game4 277 46,25 | 7 | 11 | 6 | CENTURIO:768 CENTURIO:920 ROME_LEGIONARY:566 ROME_LEGIONARY:933 ROME_LEGIONARY:916 ROME_LEGIONARY:961 | 0 |
| game4 277 47,23 | 8 | 3 | 5 | ROME_LEGIONARY:767 CENTURIO:980 ROME_LEGIONARY:822 ROME_LEGIONARY:844 ROME_LEGIONARY:1000 | 0 |
| game4 283 24,17 | 1 | 7 | 6 | ROME_LEGIONARY:809 ROME_LEGIONARY:906 ROME_LEGIONARY:905 ROME_LEGIONARY:980 ROME_LEGIONARY:1000 ROME_LEGIONARY:1000 | 0 |
| game4 283 14,26 | 1 | 1 | 1 | PRINCIPES:974 | 0 |

*battles; who: human; turn: each city taken; rows counted: 22; source: warstudy.py on the war logs of game3, game4: for each city the human took, its attacks on that plot from the declaration to the capture turn (C lines, in order: unit and odds per mille); defenders: Y lines on the declaration turn. Every value counted (22).*

- **The early wars** (game 3's first, and game 4's first four) took each city with one to three
  attacks, or none:
  - all at high odds, none under five hundred per mille;
  - by Warbands in game 3, and by Hastati and Principes in game 4.
- **Game 3's second war** took a city of several defenders. Every attack was at high odds again,
  over the days of a march.
- **The later wars of game 4 were sieges of large cities with many defenders.** An assault there:
  - often opens with a Centurio. It is the strongest unit the human fielded, of strength
    15.
  - then comes a series of Legionary attacks.
  - at the largest city, some attacks at low odds came early in the series: units lost to wear the
    defenders down. The later attacks then won at high odds.
  - warships attacked as well (`ship_attacks`), and cities fell on consecutive days.

## 7. The end of a war, and the home front (Q5)

| war | peace_day | days_after_last_capture | gold_received | gold_per_turn_received | techs_received | techs_given | cities_received |
|---|---|---|---|---|---|---|---|
| game3 203 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| game3 209 | 5 | 1 | 0 | 0 | 0 | 0 | 0 |
| game4 238 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| game4 252 | 2 | 2 | 220 | 0 | 0 | 0 | 0 |
| game4 257 | 4 | 4 | 255 | 0 | 0 | 0 | 0 |
| game4 268 | 2 | 2 | 430 | 0 | 0 | 0 | 0 |
| game4 277 | 8 | 0 | 0 | 1 | 1 | 0 | 0 |

*turns; who: human; turn: each peace; rows counted: 7; source: warstudy.py on the war logs of game3, game4: Q lines and the deal items of the peace turn between the two (TRADE_GOLD, TRADE_GOLD_PER_TURN, TRADE_TECHNOLOGIES, TRADE_CITIES; given by side); gold in gold, techs and cities counted. Every value counted (7).*

- **When peace came.** The early wars ended in peace within a few days of the last capture.
- **What it brought.** In game 4, the peace of the second to fourth wars brought the loser's gold,
  and the seventh a tech and gold per turn.

| war | human_cities | median_defenders | cities_with_one_defender_or_none | attacks_on_human | cities_lost |
|---|---|---|---|---|---|
| game3 203 | 5 | 1 | 3 | 0 | 0 |
| game3 209 | 10 | 1.0 | 8 | 0 | 0 |
| game4 238 | 10 | 2.0 | 4 | 0 | 0 |
| game4 252 | 11 | 2 | 4 | 0 | 0 |
| game4 257 | 13 | 2 | 5 | 0 | 0 |
| game4 268 | 14 | 2.0 | 4 | 0 | 0 |
| game4 271 | 15 | 2 | 5 | 0 | 0 |
| game4 272 | 16 | 2.0 | 5 | 0 | 0 |
| game4 277 | 19 | 2 | 7 | 1 | 0 |
| game4 283 | 22 | 2.0 | 9 | 0 | 0 |

*cities; who: human; turn: each war; rows counted: 10; source: warstudy.py on the war logs of game3, game4: the human's Y lines on the declaration turn; C lines with the human defending against the target and K lines of cities it lost, during the war. Every value counted (10).*

- **The home front.** While at war, the human's own cities kept their usual garrisons, one or two
  defenders, and several had only one. The targets almost never attacked the human, and it lost no
  city in any war.

## 8. Readings

Each reading names the facts it rests on and what would contradict it.

- **R1. A war is a raid planned on one city at a time.**
  - The human chooses a city it can reach and take at once: the nearest, with its army already
    next to it. It declares only when the army stands there. The power advantage of about two is a
    precondition, not the trigger.
  - *Rests on:* sections 4 and 5 (staging, the classification); section 2 (first captures
    on the declaration day).
  - *Contradicted by:* declarations with no unit near any target city, followed by a long march.
    Game 3's second war and game 4's last are such cases.
- **R2. The build-up is gold turned into an army just before it is used.**
  - Upgrades and promotions rise sharply in the thirty turns before each war. They raise existing
    units to the newest class rather than training new ones.
  - *Rests on:* section 3; `study/playstyle.md` (the army is upgraded, not trained).
  - *Contradicted by:* upgrades spread evenly over the game, or coming after the declarations.
- **R3. The logistics follow the target.**
  - When the target is across water, the army goes by ship: transports before the early raids,
    warships and landings in the later wars.
  - *Rests on:* sections 3 and 4 (transports and warships built, orders of land units at sea,
    naval moves).
  - *Contradicted by:* sea landings where a land path existed. Open: the logs do not give the path
    the units could have taken.
- **R4. The assault spends units only where the city requires it.**
  - Small cities are taken by a few attacks at high odds.
  - Large cities by an opening attack of the strongest unit, accepted losses at low odds, then the
    main attack.
  - *Rests on:* section 6.
  - *Contradicted by:* low-odds attacks on weakly held cities.
- **R5. Peace is taken as soon as the objective is held, and the loser pays.**
  - *Rests on:* section 7.
  - *Contradicted by:* wars continued without further captures.
- **R6. The home front is left thin, because the AI does not strike back.**
  - Only the army near the target matters to the human. The AI's counter-attacks, which a thin
    home front would invite, did not come.
  - *Rests on:* section 7 (garrisons of one or two, no city lost, almost no attacks on the
    human).
  - *Contradicted by:* AI counter-offensives against the human's lightly held cities.
- **R7. Game 4's later wars are a second mode: a campaign.**
  - After the army was rebuilt as Legionaries, Auxiliaries and Centurios (with the techs these
    need), the human fought several AIs at once and besieged large cities.
  - *Rests on:* sections 2, 3 and 6.
  - *Open:* whether the switch follows the new units, the size of the army, or the end of the weak
    targets nearby.

## 9. The readings and the literature

Each reading is set against a classic of military thought, read for this study (`framework.md`,
section 9). A text supports a reading only where the logged facts already show it, and the
literature adds one test of its own.

- **R1, a raid on one city, and R5, peace once it is held.**
  - Clausewitz describes the attack "without the view to a great decision", directed at "some
    secondary object". With its attainment, "the whole falls again into a state of rest and
    equilibrium" (*On War*, Book VII, chapter XVI).
  - In such wars the fortress taken is the usual object, valued for "the convenience and facility
    with which it could be attacked" rather than "the value of the place itself" (same chapter).
  - The assailant "buys up prospective advantages which are to be turned to account hereafter in
    negotiations for peace" (Book VII, chapter V). The human's gold at the peace is that account.
- **R1, the nearest city.**
  - A conquest weakens the conqueror the less, "the more it is an annex of our own country, being
    contiguous to or embraced by it" (Book VIII, chapter VII).
  - Sun Tzu: "You can be sure of succeeding in your attacks if you only attack places which are
    undefended" (*The Art of War*, chapter VI, §7).
  - The classification of section 5 has the human choose by nearness first and by
    defencelessness after. It is one of the two Clausewitzian conditions, and it keeps the conquest
    an annex.
- **R1 and R2, staging and timing.**
  - Jomini's sequence of a campaign:
    1. a base;
    2. a first objective point;
    3. a line of operations toward it;
    4. "strategic positions" near it;
    5. the attack (*The Art of War*, chapter III, definition of strategy).
  - Sun Tzu: "Knowing the place and the time of the coming battle, we may concentrate from the
    greatest distances in order to fight" (chapter VI, §19).
  - The approach of section 4 runs through that sequence.
- **R4, sieges.**
  - Sun Tzu calls besieging walled cities "the worst policy of all", "if it can possibly be
    avoided" (chapter III, §3 and 4).
  - The human took walled cities only once its army was Legionaries and Centurios. Before that,
    it chose others.
- **R3, the sea.**
  - Mahan: changes in the means of transport alter the scale of distance and time, not "the
    principles which dictated the point at which the army should be concentrated" (*The Influence
    of Sea Power upon History*, introductory chapter).
  - Jomini: before gunpowder, "the transports were also the ships of war". In the records here, a
    galley and a quinquereme carry
    4 and 4 units
    (appendix).
- **R2, gold into an army.** Smith: "the great expense of firearms gives an evident advantage to
  the nation which can best afford that expense" (*The Wealth of Nations*, Book V, chapter I,
  part I). The human's commerce bought upgrades just before each war (section 3).
- **A test from the literature: the target already engaged.**
  - Jomini names among the cases where a landing can succeed a diversion "against a state already
    engaged in a great war, whose troops are occupied at a distance" (Article XL).
  - Of the 10 wars, the target was at war with another team in
    8. If the targets had been chosen without regard to their wars,
    about 4.2 would be expected. The exact chance of at least as many is
    0.0127.
  - *Caveat:* the cue was proposed after these wars were read, among several possible cues, and
    wars older than the first W line of a log are not seen.

| war | target_at_war_elsewhere | other_teams_at_war | other_teams | share_at_war |
|---|---|---|---|---|
| game3 203 | no | 4 | 17 | 0.24 |
| game3 209 | yes | 4 | 17 | 0.24 |
| game4 238 | yes | 3 | 18 | 0.17 |
| game4 252 | yes | 5 | 18 | 0.28 |
| game4 257 | yes | 10 | 18 | 0.56 |
| game4 268 | yes | 10 | 18 | 0.56 |
| game4 271 | yes | 10 | 18 | 0.56 |
| game4 272 | no | 10 | 18 | 0.56 |
| game4 277 | yes | 9 | 17 | 0.53 |
| game4 283 | yes | 9 | 17 | 0.53 |

*cities; who: every team; turn: each declaration turn; rows counted: 10; source: warstudy.py on the war logs of game3, game4: a team is at war with another when a W line of the pair precedes the declaration and no Q line of the pair ends it before; wars before the first W line of the log are not seen; other teams: teams other than the human's with a city in M lines the turn before; share_at_war: the chance that a team picked at random among them was at war, the expected count of targets at war being the sum of these shares. Every value counted (10).*

  - **The test, at the choice of team.** `tools/strategy.py` classifies each declaration among the
    AIs the human could have attacked. Its options and cues are in its header.
    - "Engaged" alone matches many choices, but at a high error rate: many AIs were at war at once,
      so it rarely singles one out.
    - Used after nearness, as a tie-breaker, it adds little to "nearest" alone. Compare the two
      rows of the table.
    - So the excess of engaged targets is largely explained by nearness: the nearest AIs were often
      at war. The model takes nearness as its rule and leaves "engaged" out.

| strategy | choices_matched | decisions | error_rate | log_likelihood | bic |
|---|---|---|---|---|---|
| weakest | 0 | 10 | 1.0 | -27.83 | 57.96 |
| nearest | 6 | 10 | 0.4 | -21.47 | 45.25 |
| nearest_then_weak | 3 | 10 | 0.7 | -25.56 | 53.42 |
| weak_of_near_half | 0 | 10 | 1.0 | -27.83 | 57.96 |
| most_cities | 0 | 10 | 1.0 | -27.83 | 57.96 |
| weakest_ratio | 0 | 10 | 1.0 | -27.83 | 57.96 |
| engaged | 8 | 10 | 0.2 | -24.93 | 52.16 |
| nearest_then_engaged | 6 | 10 | 0.4 | -21.25 | 44.81 |
| engaged_then_nearest | 5 | 10 | 0.5 | -24.23 | 50.76 |
| guessing |  | 10 |  | -28.43 | 56.86 |

*category; who: human; turn: each declaration of the human; rows counted: 10; source: strategy.py: maximum-likelihood classification over the declarations of every game given. Every value counted (10).*

## 10. What a model of this must do

The harness model's war rule (`study/humanmodel.md` in preparation) is one rule: a fixed power
threshold, the AI's own war plan, and a declaration once enough units are near. Its runs gave up
preparations when the AI's stacks never reached a border. The readings above call for these parts,
each to be checked against the logged wars before any campaign:

1. **Choose a city, not a team.**
   - Among the cities of teams the seat outweighs, take the nearest, preferring the one with the
     most of its units near (the classification of section 5).
   - Whether the team is already at war adds little at the choice of team (section 9), and is
     left out.
   - The objective is that city and the cities nearest it that fall the same way.
2. **Build up for it.**
   - Upgrade the army to the newest classes and promote it, in the thirty turns before.
   - Build transports when the city lies across water, and siege units and warships for a large
     city.
3. **Stage.**
   - Keep open borders with every AI met (section 4).
   - Move a strike group to within two plots of the city, by land or by transport. Its size is set
     by the city's defenders, as in the assault table.
   - Declare when it stands there.
4. **Assault.**
   - Attack in order of odds against a small city.
   - Against a large city: open with the strongest unit, accept losses at low odds while the
     defenders are many, then attack at high odds.
5. **End.** Make peace once the objective is held and no other target is staged, asking for gold.
   Keep the home garrison as it is.

Data gaps:
- the units' positions between orders;
- the paths open to them;
- the human's view of the AI's defences at the time of each choice.

The Y lines record a city's defenders, not what the human could see of them.

## Appendix: the units named

| UnitInfo | Fields set (records.json) |
|---|---|
| - | (none: no record) |
| ARCHER | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_ARCHER; `Combat` UNITCOMBAT_ARCHER; `DefaultUnitAI` UNITAI_CITY_DEFENSE; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_RANGED; `PrereqBuilding` BUILDING_ARCHERY_RANGE; `PrereqTech` TECH_ARCHERY; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SAGITTARII","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_LONGBOWMAN","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_CROSSBOWMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ARCHER","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAirCombat` 1; `iAirCombatLimit` 75; `iAirRange` 1; `iAsset` 1; `iCityDefense` 50; `iCollateralDamage` 25; `iCollateralDamageLimit` 50; `iCollateralDamageMaxUnits` 2; `iCombat` 3; `iCombatLimit` 100; `iCost` 30; `iCultureGarrison` 4; `iFirstStrikes` 1; `iHillsDefense` 25; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 4; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| AXEMAN | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_AXEMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqTech` TECH_BRONZE_WORKING; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SEARAIDER","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_MACEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_AXEMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 5; `iCombatLimit` 100; `iConscription` 4; `iCost` 40; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 8; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| GREEK_PHALANX | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_AXEMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqTech` TECH_BRONZE_WORKING; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_MACEMAN","bUnitClassUpgrade":true}]; `UnitCombatCollateralImmunes` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatCollateralImmune":1}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":50},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_GREEK_PHALANX","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 7; `iCombatLimit` 100; `iConscription` 4; `iCost` 60; `iCultureGarrison` 4; `iHillsDefense` 25; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 8; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| JAVELINEER | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":10},{"BonusType":"BONUS_OBSIDIAN","iProductonModifier":10}]; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true}]; `Class` UNITCLASS_JAVELINEER; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true}]; `PrereqTech` TECH_HUNTING; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SPEARMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELINEER","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 3; `iCombatLimit` 100; `iConscription` 2; `iCost` 25; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 4; `iWithdrawalProb` 25; `iWorkRate` 100; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| LIGHT_SWORDSMAN | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_LIGHT_SWORDSMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK_CITY; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SWORDSMAN","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_MACEMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SWORDSMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityAttack` 10; `iCombat` 7; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 5; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 12; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| RAM | `Advisor` ADVISOR_MILITARY; `Capture` UNITCLASS_RAM; `Class` UNITCLASS_RAM; `Combat` UNITCOMBAT_SIEGE; `DefaultUnitAI` UNITAI_ATTACK_CITY; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_METAL_CASTING; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_CATAPULT","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ASSYRIA_RAM","iRequired":2}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":2,"iMeleeWaveSize":2,"iRangedWaveSize":2}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bNoCapture` True; `iAdvancedStartCost` 100; `iAsset` 2; `iBombardRate` 5; `iCombat` 3; `iCombatLimit` 75; `iCost` 15; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 8; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| SPEARMAN | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_SPEARMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqTech` TECH_METAL_CASTING; `TechTypes` ["TECH_HUNTING"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_PIKEMAN","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_WARBAND","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_CELTIC_WARBAND","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_TRIARII","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_AUXILIAR","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_SARISSA","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SPEARMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 4; `iCombatLimit` 100; `iConscription` 3; `iCost` 35; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 6; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| AUXILIAR | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_AUXILIAR; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_AUXILIAR","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 8; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 13; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| TRIARII | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_TRIARII; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassDefenseMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":25}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_AUXILIAR","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_TRIARII","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 6; `iCombatLimit` 100; `iCost` 50; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| VELITES | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_SPEARMAN; `Combat` UNITCOMBAT_ARCHER; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FeatureDefenses` [{"FeatureType":"FEATURE_FOREST","iFeatureDefense":50},{"FeatureType":"FEATURE_JUNGLE","iFeatureDefense":50}]; `FormationType` FORMATION_TYPE_RANGED; `PrereqTech` TECH_METAL_CASTING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_COLLATERAL","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_WAR_ELEPHANT","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_ELEPHANT_RIDER","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_TRIARII","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_AUXILIAR","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELIN_ROME","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAnimalCombat` 50; `iAsset` 2; `iCollateralDamage` 25; `iCollateralDamageLimit` 50; `iCollateralDamageMaxUnits` 2; `iCombat` 4; `iCombatLimit` 100; `iCost` 30; `iCultureGarrison` 4; `iFirstStrikes` 2; `iHillsDefense` 25; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 6; `iWithdrawalProb` 25; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| ROME_LEGIONARY | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_ROME_LEGIONARY; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK_CITY; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_COMITATENSES","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_LEGIONARY","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 4; `iCombat` 10; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 5; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 24; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| PRINCIPES | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_LIGHT_SWORDSMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_ROME_LEGIONARY","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_PRINCIPES","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 8; `iCombatLimit` 100; `iCost` 50; `iCultureGarrison` 6; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 16; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| WARBAND | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_WARBAND; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_RELIGION_NORDIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WARBAND_GERMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 6; `iCombatLimit` 100; `iConscription` 3; `iCost` 45; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| AUXILIAR | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_AUXILIAR; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_AUXILIAR","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 8; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 13; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| CENTURIO | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_CENTURIO; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true},{"PromotionType":"PROMOTION_LEADER","bFreePromotion":true},{"PromotionType":"PROMOTION_LEADERSHIP","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_SENATE; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_CENTURIO","iRequired":1},{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_LEGIONARY","iRequired":7}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":8,"iMeleeWaveSize":4,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCombat` 15; `iCombatLimit` 100; `iCost` 150; `iCultureGarrison` 5; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 30; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| HASTATI | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_AXEMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_LIGHT_SWORDSMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_HASTATI","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 7; `iCombatLimit` 100; `iConscription` 8; `iCost` 50; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 10; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| PRINCIPES | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_LIGHT_SWORDSMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_ROME_LEGIONARY","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_PRINCIPES","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 8; `iCombatLimit` 100; `iCost` 50; `iCultureGarrison` 6; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 16; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| ROME_LEGIONARY | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_ROME_LEGIONARY; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK_CITY; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_COMITATENSES","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_LEGIONARY","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 4; `iCombat` 10; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 5; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 24; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| WARBAND | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_WARBAND; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_RELIGION_NORDIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WARBAND_GERMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 6; `iCombatLimit` 100; `iConscription` 3; `iCost` 45; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| GALLEY | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_GALLEY; `Combat` UNITCOMBAT_WOODEN_SHIPS; `DefaultUnitAI` UNITAI_ASSAULT_SEA; `Domain` DOMAIN_SEA; `DomainCargo` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_SAILING; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `UnitAIs` [{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SETTLER_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_MISSIONARY_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SPY_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_GALLEON","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_FLUYT","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_COG","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_GALLEY","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCargo` 4; `iCombat` 3; `iCombatLimit` 100; `iCost` 25; `iMinAreaSize` 20; `iMoves` 4; `iNukeRange` -1; `iPower` 4; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| QUINQUEREME | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_QUINQUEREME; `Combat` UNITCOMBAT_WOODEN_SHIPS; `DefaultUnitAI` UNITAI_ATTACK_SEA; `Domain` DOMAIN_SEA; `DomainCargo` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_SHIP_BUILDING; `TechTypes` ["TECH_ROMAN","TECH_SIEGE_WARFARE","NONE"]; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ESCORT_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SLOOP","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_BRIGANTINE","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_QUINQUEREME","iRequired":3}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAirCombat` 1; `iAirCombatLimit` 50; `iAirRange` 1; `iAsset` 1; `iBombardRate` 10; `iCargo` 4; `iCombat` 8; `iCombatLimit` 100; `iCost` 60; `iMinAreaSize` 20; `iMoves` 4; `iNukeRange` -1; `iPower` 16; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `wr.war_overview` | table, 10 values | cities | human | each war | 10 | warstudy.py on the war logs of game3, game4: W lines of the human team (war: game and declaration turn), the power of both the turn before (M lines), the target's cities on the declaration turn (Y lines), cities taken (K), attacks (C), units killed and lost (R), the peace (Q); days count from the declaration |
| `wr.war_buildup` | table, 20 values | units built | human | the 60 turns before each declaration | 20 | warstudy.py on the war logs of game3, game4: U lines by DefaultUnitAI (UnitInfo) and A lines COMMAND_UPGRADE and COMMAND_PROMOTION, in the 30 turns before the declaration and the 30 before those; upgrades and promotions are commands |
| `wr.war_upgrades` | table, 6 values | orders | human | the 30 turns before each declaration | 297 | warstudy.py on the war logs of game3, game4: A lines COMMAND_UPGRADE, the unit type upgraded to |
| `wr.war_approach` | table, 110 values | orders | human | the ten days before each declaration that took a city, and the declaration | 110 | warstudy.py on the war logs of game3, game4: A lines MISSION_MOVE_TO of the human's land units other than workers, settlers, explorers and merchants (DefaultUnitAI); units: group sizes; near: the target plot within two plots of a city the human took in that war; distances in grid plots from the unit's plot and from its target plot to the nearest such city |
| `wr.war_staging` | table, 10 values | orders | human | the declaration turn and the ten before | 10 | warstudy.py on the war logs of game3, game4: Y lines of the target's cities on the declaration turn ("foreign": other players' land units within two plots, before the human moves); A lines of the human: MISSION_MOVE_TO on the declaration turn (units: their group sizes), those from ten turns before to the declaration by land units standing on water (COAST, OCEAN) and by ships, and GROUP commands |
| `wr.war_access` | table, 10 values | turns | human | each declaration turn | 10 | warstudy.py on the war logs of game3, game4: deal items TRADE_OPEN_BORDERS (D lines) between the human and the target before the declaration; open borders let units enter another's land in peace, and a declaration ends them; ais_with_an_open_borders_deal: the AIs with any such deal with the human before the declaration; ais_met: those and the AIs the human had met by the save (diplo) |
| `wr.war_targets` | table, 65 values | cities | the human's targets | each declaration turn | 65 | warstudy.py on the war logs of game3, game4: the first Y line of each city of the target on the declaration turn; distance: grid plots to the nearest city of the human that turn (its Y lines); day_taken: days after the declaration that the human took it in this war (K lines) |
| `wr.war_choice` | table, 11 values | cities | human | each city taken | 17 | warstudy.py on the war logs of game3, game4: each city the human took (K lines) with more than one city of the target that turn (Y lines); options: those cities; a cue's best options: its least value (defenders, defence modifier, distance to the human's cities including those taken before in the war, size) or most foreign units near; a pair of cues: the second decides among the first's best (take-the-best, Gigerenzer, Heuristics, chapter 14); maximum-likelihood classification with one error rate per cue (Bröder, in Heuristics, chapter 17), e on a grid of hundredths; guessing: each option 1/m; chosen_was_best counts ties as hits |
| `wr.war_days` | table, 27 values | battles | human | each day with an attack or capture, and the declaration | 27 | warstudy.py on the war logs of game3, game4: C lines with the human attacking the target (odds per mille; siege units: DefaultUnitAI ATTACK_CITY; ships: SEA domain), B lines of the human, R lines with the human losing, K lines |
| `wr.war_assaults` | table, 22 values | battles | human | each city taken | 22 | warstudy.py on the war logs of game3, game4: for each city the human took, its attacks on that plot from the declaration to the capture turn (C lines, in order: unit and odds per mille); defenders: Y lines on the declaration turn |
| `wr.war_peace` | table, 7 values | turns | human | each peace | 7 | warstudy.py on the war logs of game3, game4: Q lines and the deal items of the peace turn between the two (TRADE_GOLD, TRADE_GOLD_PER_TURN, TRADE_TECHNOLOGIES, TRADE_CITIES; given by side); gold in gold, techs and cities counted |
| `wr.war_home` | table, 10 values | cities | human | each war | 10 | warstudy.py on the war logs of game3, game4: the human's Y lines on the declaration turn; C lines with the human defending against the target and K lines of cities it lost, during the war |
| `wr.war_ships` | table, 2 values | xml | human | whole game | 2 | the ships named in section 9 (UnitInfo records) |
| `wr.wars_counted` | 10 | cities | human | each declaration | 10 | W lines of the human team in the games given |
| `wr.targets_at_war_elsewhere` | 8 | cities | the human's targets | each declaration turn | 10 | war_engaged: wars whose target was at war with another team (counted per war) |
| `wr.targets_at_war_expected` | 4.2 | cities | the human's targets | each declaration turn | 10 | war_engaged: sum over wars of share_at_war, the count expected if targets were picked without regard to their wars |
| `wr.targets_at_war_p` | 0.0127 | share | the human's targets | each declaration turn | 10 | war_engaged: the chance of at least as many targets at war elsewhere if each war's target were a random other team (Poisson-binomial over the wars' shares, computed exactly) |
| `wr.war_engaged` | table, 10 values | cities | every team | each declaration turn | 10 | warstudy.py on the war logs of game3, game4: a team is at war with another when a W line of the pair precedes the declaration and no Q line of the pair ends it before; wars before the first W line of the log are not seen; other teams: teams other than the human's with a city in M lines the turn before; share_at_war: the chance that a team picked at random among them was at war, the expected count of targets at war being the sum of these shares |
| `tg.war_target_strategies_pooled` | table, 10 values | category | human | each declaration of the human | 10 | strategy.py: maximum-likelihood classification over the declarations of every game given |
