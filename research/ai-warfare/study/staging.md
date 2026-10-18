<!-- Rendered by method/docs.py from staging.md.in. Do not edit; edit the template. -->
# How the human opens a war, and what the AI's city defence sees

Method: `method/docs/framework.md`. The queries are declared in `study/queries_staging.json` and
turned into figures by `tools/sqlfig.py` over the five logged games. Code facts name their file and
line in the GitLab source as of commit `efcb5e4`. Facts come first; the readings are in section 4,
each with the facts it rests on and what would contradict it. Section 5 is a proposed AI change; it
is not built.

This study reads the decisive events of each war: the declaration, the cities that fell at once,
and what the AI's cities held at that moment. It started from one event of game 5 (`games/game5/
analysis.md`, section 5): two units landed from a galley took a city on the turn of the
declaration.

## 1. Questions

- **Q1.** How do the human's wars begin, in all five games, and how soon does the first city fall?
  Source: `W`, `Q` and `K` lines.
- **Q2.** What did the target's cities hold when each war started: defenders, the AI's own danger
  count, foreign units nearby? Source: `Y` lines (game 3 to game 5; game 1 and game 2 have none).
- **Q3.** What does the AI's city defence count as danger, and what can raise its defenders while
  at peace? Source: `CvPlayerAI.cpp`, `CvCityAI.cpp`.
- **Q4.** In game 5, what did Frisia build and where was its army while the human took its cities?
  Source: `Y`, `G` and `M` lines.

## 2. The facts

### 2.1 Every declaration of the human

The human's team declared every war of the five games; no AI declared on the human (the last
column). Per declaration: the target's other wars open at that moment, the first city the human
took from it, and how many fell on the declaration turn or the next:

| turn | target | target_other_wars | first_capture | taken_within_1 | wars_on_human |
|---|---|---|---|---|---|
| 186 | 7 | 0 | 187 | 2 | 0 |
| 193 | 1 | 0 | 194 | 2 | 0 |
| 206 | 14 | 0 | 207 | 1 | 0 |

*cities; who: human; turn: each declaration of the human; rows counted: 3; source: W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game1]. Every value counted (3).*

| turn | target | target_other_wars | first_capture | taken_within_1 | wars_on_human |
|---|---|---|---|---|---|
| 92 | 16 | 0 | 110 | 0 | 0 |
| 229 | 11 | 0 | 229 | 4 | 0 |
| 230 | 9 | 0 | 230 | 2 | 0 |

*cities; who: human; turn: each declaration of the human; rows counted: 3; source: W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game2]. Every value counted (3).*

| turn | target | target_other_wars | first_capture | taken_within_1 | wars_on_human |
|---|---|---|---|---|---|
| 203 | 5 | 0 | 203 | 4 | 0 |
| 209 | 7 | 1 | 213 | 0 | 0 |

*cities; who: human; turn: each declaration of the human; rows counted: 2; source: W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game3]. Every value counted (2).*

| turn | target | target_other_wars | first_capture | taken_within_1 | wars_on_human |
|---|---|---|---|---|---|
| 238 | 14 | 2 | 238 | 2 | 0 |
| 252 | 2 | 1 | 252 | 1 | 0 |
| 257 | 6 | 2 | 257 | 1 | 0 |
| 268 | 7 | 1 | 268 | 2 | 0 |
| 271 | 14 | 3 | 272 | 1 | 0 |
| 272 | 10 | 0 | 272 | 1 | 0 |
| 277 | 2 | 1 | 280 | 0 | 0 |
| 283 | 7 | 1 | 284 | 2 | 0 |

*cities; who: human; turn: each declaration of the human; rows counted: 8; source: W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game4]. Every value counted (8).*

| turn | target | target_other_wars | first_capture | taken_within_1 | wars_on_human |
|---|---|---|---|---|---|
| 210 | 8 | 1 | 210 | 1 | 0 |

*cities; who: human; turn: each declaration of the human; rows counted: 1; source: W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game5]. Every value counted (1).*

### 2.2 The target's cities when the war started

The `Y` lines written at the moment of each declaration, one per city of the target, split by
whether the human took the city on the declaration turn or the next. `danger_zero`: the owner's
danger count was zero; `foreign_within_2`: land units able to attack of another team stood within
two plots; `one_defender_or_less`: at most one defender in the city.

| outcome | cities | danger_zero | foreign_within_2 | one_defender_or_less | median_defenders | median_foreign |
|---|---|---|---|---|---|---|
| not taken within one turn | 4 | 2 | 0 | 2 | 1.5 | 0.0 |
| taken within one turn | 4 | 4 | 3 | 4 | 1.0 | 2.5 |

*cities; who: the target of each declaration of the human; turn: the moment each war starts; rows counted: 2; source: Y lines written when the war starts (the first Y line of each city of the target's players after the W line and before the next T line): defenders, the owner's danger count (AI_getPlotDanger: enemy units within three plots, as the AI counts it), land units able to attack of other teams within two plots, whether the human took the city on the declaration turn or the next (K lines). Team of a player as in the declarations table [game3]. Every value counted (2).*

| outcome | cities | danger_zero | foreign_within_2 | one_defender_or_less | median_defenders | median_foreign |
|---|---|---|---|---|---|---|
| not taken within one turn | 47 | 40 | 23 | 2 | 3.0 | 0.0 |
| taken within one turn | 10 | 8 | 9 | 6 | 1.0 | 3.5 |

*cities; who: the target of each declaration of the human; turn: the moment each war starts; rows counted: 2; source: Y lines written when the war starts (the first Y line of each city of the target's players after the W line and before the next T line): defenders, the owner's danger count (AI_getPlotDanger: enemy units within three plots, as the AI counts it), land units able to attack of other teams within two plots, whether the human took the city on the declaration turn or the next (K lines). Team of a player as in the declarations table [game4]. Every value counted (2).*

| outcome | cities | danger_zero | foreign_within_2 | one_defender_or_less | median_defenders | median_foreign |
|---|---|---|---|---|---|---|
| not taken within one turn | 6 | 5 | 0 | 3 | 1.5 | 0.0 |
| taken within one turn | 1 | 1 | 0 | 0 | 2.0 | 0.0 |

*cities; who: the target of each declaration of the human; turn: the moment each war starts; rows counted: 2; source: Y lines written when the war starts (the first Y line of each city of the target's players after the W line and before the next T line): defenders, the owner's danger count (AI_getPlotDanger: enemy units within three plots, as the AI counts it), land units able to attack of other teams within two plots, whether the human took the city on the declaration turn or the next (K lines). Team of a player as in the declarations table [game5]. Every value counted (2).*

Each city that fell at once:

| declared | taken | target | x | y | pop | defenders | danger | foreign | orders |
|---|---|---|---|---|---|---|---|---|---|
| 203 | 203 | 5 | 26 | 40 | 4 | 1 | 0 | 3 | BUILDING_SLAVE_MARKET |
| 203 | 203 | 5 | 28 | 40 | 2 | 1 | 0 | 3 | UNIT_SPEARMAN |
| 203 | 204 | 5 | 23 | 40 | 3 | 1 | 0 | 0 | UNIT_SPEARMAN |
| 203 | 204 | 5 | 33 | 39 | 4 | 0 | 0 | 2 | UNIT_SPEARMAN |

*cities; who: the target of each declaration of the human; turn: the moment each war starts; rows counted: 4; source: as war_start_cities, the cities taken on the declaration turn or the next, one row each, with the turn the human took it and the city's current order [game3]. Every value counted (4).*

| declared | taken | target | x | y | pop | defenders | danger | foreign | orders |
|---|---|---|---|---|---|---|---|---|---|
| 238 | 238 | 14 | 30 | 20 | 2 | 1 | 0 | 5 | UNIT_WORKER |
| 238 | 239 | 14 | 29 | 33 | 3 | 1 | 0 | 1 | UNIT_GALLEY |
| 252 | 252 | 2 | 31 | 33 | 2 | 1 | 0 | 3 | BUILDING_WALLS |
| 257 | 257 | 6 | 33 | 29 | 3 | 2 | 0 | 3 | UNIT_RAM |
| 268 | 268 | 7 | 16 | 29 | 1 | 1 | 0 | 1 | UNIT_WORKBOAT |
| 268 | 268 | 7 | 28 | 20 | 2 | 1 | 0 | 4 | BUILDING_OBELISK |
| 271 | 272 | 14 | 38 | 23 | 4 | 12 | 16 | 10 | UNIT_SPEARMAN |
| 272 | 272 | 10 | 30 | 16 | 5 | 2 | 0 | 4 | UNIT_AXEMAN |
| 283 | 284 | 7 | 14 | 26 | 1 | 1 | 14 | 9 | UNIT_WARLORDI |
| 283 | 284 | 7 | 24 | 17 | 17 | 7 | 0 | 0 | UNIT_SETTLER |

*cities; who: the target of each declaration of the human; turn: the moment each war starts; rows counted: 10; source: as war_start_cities, the cities taken on the declaration turn or the next, one row each, with the turn the human took it and the city's current order [game4]. Every value counted (10).*

| declared | taken | target | x | y | pop | defenders | danger | foreign | orders |
|---|---|---|---|---|---|---|---|---|---|
| 210 | 210 | 8 | 20 | 44 | 8 | 2 | 0 | 0 | UNIT_SPEARMAN |

*cities; who: the target of each declaration of the human; turn: the moment each war starts; rows counted: 1; source: as war_start_cities, the cities taken on the declaration turn or the next, one row each, with the turn the human took it and the city's current order [game5]. Every value counted (1).*

The city of game 5 shows no foreign unit within two plots: the galley carrying the two attackers was
three plots out at the declaration and closed in during the human's turn (`games/game5/analysis.md`,
section 5).

### 2.3 What the AI counts as danger (code)

- A city is in danger (`CvCityAI::AI_isDanger`, `CvCityAI.cpp:6452`) when
  `CvPlayerAI::AI_getAnyPlotDanger` finds a unit within two plots. The owner's danger count of the
  `Y` lines is `CvPlayerAI::AI_getPlotDanger` over three plots (`CvGameCoreUtils.cpp:3604`). Both
  loops have the same two filters:
  - only plots in the city's own area (`pLoopPlot->area() == pPlotArea`, `CvPlayerAI.cpp:3842` and
    the same test in `AI_getAnyPlotDanger`): a ship at sea is in a water area, so the units it
    carries are never counted for a coastal city, at war or not;
  - only units of a team at war with the owner (`pLoopUnit->isEnemy(eTeam)`, `CvPlayerAI.cpp:3874`):
    an army of a team at peace counts nothing, however close.
- The defenders a city wants (`CvCityAI::AI_neededDefenders`, from `CvCityAI.cpp:6214`) start at one.
  One more for a capital, a holy city or a city with a world wonder, and one more again there under
  the alert strategy `AI_STRATEGY_ALERT1`; one more in a city off hills under `AI_STRATEGY_ALERT2` or
  in a defensive area; plus the floating defenders of the area (`AI_neededFloatingDefenders`), and
  terms for a last stand, cultural and space victory and the revolution index. Danger (`AI_isDanger`)
  raises them only in a city acquired in the last turns.
- The visible-army change of the war-AI fixes (`AI_THREAT_VISIBLE_ARMY`, `CvPlayerAI.cpp:21618`) adds
  paranoia per land unit of another player seen on the owner's plots, which can switch on the alert
  strategies above. It acts for the whole player, not for the city the army stands next to. Game 5
  was played with it on.

### 2.4 Frisia in game 5

Frisia's cities while at war with the human, their current orders counted over city-turns with the
owner's danger count above zero and at zero:

| orders | danger_above_zero | danger_zero |
|---|---|---|
| UNIT_GALLEY | 13 | 6 |
| UNIT_SPEARMAN | 11 | 5 |
| UNIT_SETTLER | 4 | 1 |
| UNIT_SLAVE | 4 | 0 |
| UNIT_RAM | 3 | 18 |
| UNIT_WORKER | 3 | 7 |
| BUILDING_TOWN_ESSENTIALS | 3 | 6 |
| BUILDING_SLAVE_MARKET | 0 | 2 |

*lines; who: Frisia (player 8); turn: every Frisian turn at war with the human (turns 210 to 223); rows counted: 8; source: Y lines of Frisia's cities while at war with the human: the city's current order, counted over city-turns with the owner's danger count above zero and at zero [game5]. Every value counted (8).*

Its stacks near or in enemy land (all on the Gallic front), and the two sides' military and power:

| turn | x | y | military | head_ai | units |
|---|---|---|---|---|---|
| 207 | 17 | 38 | 4 | ATTACK_CITY | JAVELINEER:4 |
| 214 | 17 | 38 | 5 | ATTACK_CITY | JAVELINEER:5 |
| 215 | 17 | 37 | 5 | ATTACK_CITY | JAVELINEER:5 |

*lines; who: Frisia (player 8); turn: as logged; rows counted: 3; source: G lines: Frisia's stacks near or in enemy land after its moves (AI stacks of three or more military units): plot, military units, the head's unit AI, units [game5]. Every value counted (3).*

| turn | player | cities | military | power |
|---|---|---|---|---|
| 200 | 0 | 7 | 11 | 117 |
| 200 | 8 | 5 | 20 | 99 |
| 207 | 0 | 7 | 15 | 157 |
| 207 | 8 | 6 | 26 | 123 |
| 210 | 0 | 9 | 18 | 192 |
| 210 | 8 | 6 | 26 | 126 |
| 215 | 0 | 9 | 22 | 227 |
| 215 | 8 | 6 | 23 | 121 |
| 220 | 0 | 11 | 29 | 308 |
| 220 | 8 | 5 | 17 | 97 |
| 223 | 0 | 14 | 31 | 341 |
| 223 | 8 | 2 | 10 | 58 |

*units at save; who: Frisia (player 8) and the human; turn: turns 200, 207 (Frisia declares on Gaul), 210 (the human declares on Frisia), 215, 220, 223; rows counted: 12; source: M lines (end of each player turn): cities, military units and power [game5]. Every value counted (12).*

## 3. Summary of the facts

- The human opens every war itself, and in most wars the first city falls on the declaration turn
  or the next (section 2.1).
- Most cities that fell at once had, at the declaration, a danger count of zero and one or two
  defenders, and in game 3 and game 4 most had foreign units within two plots. In game 3 and game 4
  the cities that held had more defenders (section 2.2).
- The AI's danger counts cannot see an army of a team at peace, nor units aboard ships; at peace a
  city's wanted defenders rise only through player-wide alert strategies (section 2.3).
- In game 5, Frisia's one attack stack stayed on the Gallic front, and its threatened cities built
  galleys, settlers, workers and rams as well as spearmen (section 2.4).

## 4. Readings

- **R1. The human's method is to stage at peace and strike at once.** Facts: section 2.1 (every war
  declared by the human, the first capture mostly within a turn) and section 2.2 (the cities taken at
  once had units of another team next to them and few defenders at the declaration). Contradicted
  if the foreign units within two plots of those cities were not the human's: the `Y` lines count
  every other team's units, and only game 5 logs the human's unit positions (`L` lines).
- **R2. The AI cannot defend against this, by construction.** Facts: section 2.3. A city sizes its
  defence by a danger count that is zero until the war exists, and the human declares and attacks
  within its own turn, so the city never sees the danger before it falls. Contradicted if cities
  with the visible-army change on (game 5 onward) show more defenders before a declaration than
  before the change; the `Y` lines only start at the declaration, so the earlier turns are not
  logged.
- **R3. The human picks the weakest city in reach.** Facts: in game 4 about half of the cities that
  held also had foreign units within two plots, with more defenders than the cities that fell
  (section 2.2). Contradicted if the human's choice of first target is better explained by distance
  or by the city's value than by its defenders.
- **R4. An AI at war elsewhere leaves its cities to their minimum.** Facts: game 5 only (Frisia's
  stack on the Gallic front, cities at one or two defenders). One case; contradicted if, in the
  other games, the targets that were at war elsewhere held as many defenders as those at peace.
- **R5. A threatened city keeps developing.** Facts: section 2.4, with the war-AI fixes on. This is
  defect A of `diagnosis-1.md`, seen again.

## 5. Proposed change (not built)

**S. Defend against staged forces.** In `CvCityAI::AI_neededDefenders`:
- **What it counts.** Land units able to attack that could reach the city this turn and belong to a
  team the owner is not at war with. A team counts unless it is the owner's vassal, master or
  permanent ally. Units aboard ships count too, by the ship's moves. The area test of section 2.3 is
  not applied.
- **What it computes.** With `CvSelectionGroupAI::AI_assaultForecast`, already in the source: the
  chance that those units, attacking now one after another, would take the city from its present
  defenders.
- **What it changes.** While that chance is at least the owner's threshold, the city wants one more
  defender than it has. Production and the city-defence unit AI then fill it; the next turn's check
  sees the new defender.
- **Each leader's character.** The threshold moves with the leader's attack-odds personality, as
  the attack threshold `AI_STACK_FORECAST` does (`CvSelectionGroup.cpp:4477`). Bold leaders accept
  more risk.
- **The human.** As in the visible-army change, a human's intent counts as at least an even chance
  of war, whatever the leader's attitude.
- **Switch.** A define in `GlobalDefinesAlt.xml`, off at zero.
- **Cost.** One look over the plots within reach per city per turn, and a forecast only where foreign
  attackers stand.
- **What it leaves alone.** Danger as the unit AI uses it (workers, settlers, moves) is unchanged, so
  armies passing at peace do not make workers flee.

**Risks.**
- AIs stage against each other too, so AI wars may open more slowly.
- More defenders means less development near busy borders.

Both would show in the harness runs as fewer AI-against-AI captures and slower growth; they bear on
the mission's second half, keeping each leader's character.

**The prediction it would serve** (to register before building, on the essential variable `taken`):
- **Claim.** With S on, the human takes fewer cities by the claim turn, at Noble, than in the
  reference games.
- **Counting.** Counted only for games logged from the first turn by a build made under the
  prediction. As P2, but as its own line, so that its games do not count for P2 and P2's do not
  count for it.
- **A check that can be computed.** For game 5's first city, the forecast S would have used at the
  turn start before the declaration can be computed from the `L` and `J` lines of that turn start
  (the human's units aboard the galley and the city's defenders). In game 3 and game 4 the human's unit
  positions are not logged.

## 6. Open

- Whether the foreign units within two plots of the cities that fell in game 3 and game 4 were the
  human's (R1).
- The AI's defenders in the turns before a declaration (R2); the `Y` lines begin at the war.
- Whether S, by keeping cities defended, also changes when the AIs declare on each other.

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `s.game1_declarations` | table, 3 values | cities | human | each declaration of the human | 3 | W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game1] |
| `s.game2_declarations` | table, 3 values | cities | human | each declaration of the human | 3 | W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game2] |
| `s.game3_declarations` | table, 2 values | cities | human | each declaration of the human | 2 | W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game3] |
| `s.game4_declarations` | table, 8 values | cities | human | each declaration of the human | 8 | W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game4] |
| `s.game5_declarations` | table, 1 values | cities | human | each declaration of the human | 1 | W lines declared by the human's team; the target's other wars open at that moment (W lines of the target or on it without a later Q line); K lines of cities the human took from the target's players: the first such capture, and how many fell on the declaration turn or the next. A player's team is its P line's team, or the player id where the log has no P line for it (game 5, whose header lists the human only; in its setup every player's team is its id) [game5] |
| `s.game3_war_start_cities` | table, 2 values | cities | the target of each declaration of the human | the moment each war starts | 2 | Y lines written when the war starts (the first Y line of each city of the target's players after the W line and before the next T line): defenders, the owner's danger count (AI_getPlotDanger: enemy units within three plots, as the AI counts it), land units able to attack of other teams within two plots, whether the human took the city on the declaration turn or the next (K lines). Team of a player as in the declarations table [game3] |
| `s.game4_war_start_cities` | table, 2 values | cities | the target of each declaration of the human | the moment each war starts | 2 | Y lines written when the war starts (the first Y line of each city of the target's players after the W line and before the next T line): defenders, the owner's danger count (AI_getPlotDanger: enemy units within three plots, as the AI counts it), land units able to attack of other teams within two plots, whether the human took the city on the declaration turn or the next (K lines). Team of a player as in the declarations table [game4] |
| `s.game5_war_start_cities` | table, 2 values | cities | the target of each declaration of the human | the moment each war starts | 2 | Y lines written when the war starts (the first Y line of each city of the target's players after the W line and before the next T line): defenders, the owner's danger count (AI_getPlotDanger: enemy units within three plots, as the AI counts it), land units able to attack of other teams within two plots, whether the human took the city on the declaration turn or the next (K lines). Team of a player as in the declarations table [game5] |
| `s.game3_quick_captures` | table, 4 values | cities | the target of each declaration of the human | the moment each war starts | 4 | as war_start_cities, the cities taken on the declaration turn or the next, one row each, with the turn the human took it and the city's current order [game3] |
| `s.game4_quick_captures` | table, 10 values | cities | the target of each declaration of the human | the moment each war starts | 10 | as war_start_cities, the cities taken on the declaration turn or the next, one row each, with the turn the human took it and the city's current order [game4] |
| `s.game5_quick_captures` | table, 1 values | cities | the target of each declaration of the human | the moment each war starts | 1 | as war_start_cities, the cities taken on the declaration turn or the next, one row each, with the turn the human took it and the city's current order [game5] |
| `s.frisia_orders` | table, 8 values | lines | Frisia (player 8) | every Frisian turn at war with the human (turns 210 to 223) | 8 | Y lines of Frisia's cities while at war with the human: the city's current order, counted over city-turns with the owner's danger count above zero and at zero [game5] |
| `s.frisia_front` | table, 3 values | lines | Frisia (player 8) | as logged | 3 | G lines: Frisia's stacks near or in enemy land after its moves (AI stacks of three or more military units): plot, military units, the head's unit AI, units [game5] |
| `s.frisia_power` | table, 12 values | units at save | Frisia (player 8) and the human | turns 200, 207 (Frisia declares on Gaul), 210 (the human declares on Frisia), 215, 220, 223 | 12 | M lines (end of each player turn): cities, military units and power [game5] |
