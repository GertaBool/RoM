<!-- Rendered by tools/docs.py from playstyle.md.in. Do not edit; edit the template. -->
# The human's playstyle: a synthesis of the four logged games

The studies before this one describe parts: the decisions (`study/human.md`), tiles, trade and
combat (`study/data.md`), the economy and the wars (`study/winning.md`), and workers, builds
and movement (`study/operations.md`). This one proposes the whole they belong to, and checks each
part against it.

## 1. Method

- **The whole and the parts.** Schleiermacher: "each part can be understood only out of the
  whole to which it belongs, and vice versa", and an interpreter working from "disconnected
  observations can never reach an independent interpretation" (Mueller-Vollmer, *The
  Hermeneutics Reader*, §20 and 21, p. 84). Here the whole is a plan. Section 7 states
  it; every element names the facts it explains and what would refute it. A fact the plan
  cannot place is listed as such.
- **Phases.** The human's per-turn activity is cut into phases by an exact optimal partition.
  Each phase costs a fixed penalty, the parsimony pressure of `framework.md` (section 6), so a
  phase is kept only when it explains enough (`tools/phases.py`). A boundary that survives with
  the penalty halved and doubled is taken as real.
- **Choices among options.** For the choice of whom to attack, candidate rules are compared by
  maximum-likelihood strategy classification. Each rule is assumed to be followed with errors at
  a constant rate, and it must beat guessing (Bröder, in Gigerenzer, Hertwig and Pachur,
  *Heuristics*, chapter 17; `tools/strategy.py`). One candidate is the distance-decay heuristic of
  geographic profiling: offenders act near home (Snook, Taylor and Bennell, chapter 29, p. 593).
- **Sources.** Every number comes from the registries named at the top of this page. The
  readings of the other studies are cited by section and not repeated.

## 2. The phases of a game

| phase | turns | length | build_per_turn | move_per_turn | train_per_turn | construct_per_turn | found_per_turn | attack_per_turn | war_share | cities_at_end |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0-59 | 60 | 0.08 | 0.22 | 0.08 | 0.0 | 0.02 | 0.0 | 0.0 | 1 |
| 2 | 60-167 | 108 | 0.53 | 0.74 | 0.23 | 0.26 | 0.04 | 0.0 | 0.0 | 5 |
| 3 | 168-185 | 18 | 0.33 | 2.61 | 1.0 | 0.39 | 0.11 | 0.0 | 0.0 | 7 |
| 4 | 186-195 | 10 | 0.6 | 8.6 | 1.2 | 1.0 | 0.0 | 1.9 | 1.0 | 13 |
| 5 | 196-217 | 22 | 0.86 | 5.86 | 0.36 | 1.82 | 0.0 | 0.55 | 1.0 | 16 |

*orders; who: human; turn: turns 0-217; rows counted: 218; source: phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game1; means of the raw series per turn. Every value counted (5).*

| phase | turns | length | build_per_turn | move_per_turn | train_per_turn | construct_per_turn | found_per_turn | attack_per_turn | war_share | cities_at_end |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0-91 | 92 | 0.08 | 0.12 | 0.08 | 0.01 | 0.01 | 0.0 | 0.0 | 1 |
| 2 | 92-198 | 107 | 0.65 | 0.95 | 0.23 | 0.42 | 0.05 | 0.07 | 1.0 | 7 |
| 3 | 199-225 | 27 | 1.22 | 1.78 | 0.48 | 1.33 | 0.0 | 0.0 | 1.0 | 7 |
| 4 | 226-235 | 10 | 2.5 | 9.7 | 1.6 | 2.3 | 0.0 | 1.8 | 1.0 | 15 |

*orders; who: human; turn: turns 0-235; rows counted: 236; source: phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game2; means of the raw series per turn. Every value counted (4).*

| phase | turns | length | build_per_turn | move_per_turn | train_per_turn | construct_per_turn | found_per_turn | attack_per_turn | war_share | cities_at_end |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0-94 | 95 | 0.24 | 0.22 | 0.06 | 0.0 | 0.01 | 0.0 | 0.0 | 1 |
| 2 | 95-202 | 108 | 0.66 | 0.78 | 0.18 | 0.21 | 0.04 | 0.0 | 0.0 | 5 |
| 3 | 203-214 | 12 | 1.08 | 3.33 | 0.5 | 1.17 | 0.0 | 1.17 | 0.83 | 11 |
| 4 | 215-265 | 51 | 1.69 | 1.1 | 0.37 | 2.02 | 0.04 | 0.0 | 0.0 | 13 |

*orders; who: human; turn: turns 0-265; rows counted: 266; source: phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game3; means of the raw series per turn. Every value counted (4).*

| phase | turns | length | build_per_turn | move_per_turn | train_per_turn | construct_per_turn | found_per_turn | attack_per_turn | war_share | cities_at_end |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0-75 | 76 | 0.18 | 0.13 | 0.11 | 0.0 | 0.01 | 0.0 | 0.0 | 1 |
| 2 | 76-237 | 162 | 1.09 | 1.26 | 0.35 | 0.48 | 0.05 | 0.0 | 0.0 | 9 |
| 3 | 238-267 | 30 | 2.47 | 4.1 | 0.97 | 2.7 | 0.07 | 0.23 | 0.37 | 13 |
| 4 | 268-284 | 17 | 2.0 | 10.12 | 2.47 | 4.88 | 0.12 | 3.59 | 1.0 | 24 |

*orders; who: human; turn: turns 0-284; rows counted: 285; source: phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game4; means of the raw series per turn. Every value counted (4).*

Where the phases start with the penalty halved, as set, and doubled:

| penalty_factor | phase_starts |
|---|---|
| 0.5 | 60 168 186 196 206 |
| 1 | 60 168 186 196 |
| 2 | 186 |

*turn; who: human; turn: turns 0-217; rows counted: 218; source: phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled. Every value counted (3).*

| penalty_factor | phase_starts |
|---|---|
| 0.5 | 92 119 199 226 |
| 1 | 92 199 226 |
| 2 | 92 226 |

*turn; who: human; turn: turns 0-235; rows counted: 236; source: phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled. Every value counted (3).*

| penalty_factor | phase_starts |
|---|---|
| 0.5 | 95 203 215 230 |
| 1 | 95 203 215 |
| 2 | 203 215 |

*turn; who: human; turn: turns 0-265; rows counted: 266; source: phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled. Every value counted (3).*

| penalty_factor | phase_starts |
|---|---|
| 0.5 | 55 134 238 252 271 |
| 1 | 76 238 268 |
| 2 | 76 238 268 |

*turn; who: human; turn: turns 0-284; rows counted: 285; source: phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled. Every value counted (3).*

## 3. Research and civics

Every civic the human adopted after the start, with the tech it requires and when the human
got that tech:

| civic | civic_option | prerequisite | tech_turn | adopted_turn | lag_turns | ais_holding_it_at_save |
|---|---|---|---|---|---|---|
| OLIGARCHY | LEADERSHIP | SLAVERY | 31 | 32 | 1 | 0 |
| TRIBUTE | TAXATION | SLAVERY | 31 | 32 | 1 | 1 |
| TABLETS | ADMINISTRATION | POTTERY | 65 | 66 | 1 | 0 |
| ELDERS | EDUCATION | MYSTICISM | 129 | 130 | 1 | 0 |
| BARTER | ECONOMY | TRADE | 155 | 156 | 1 | 0 |
| SPIRITISM | RELIGION | MYSTICISM | 129 | 156 | 27 | 16 |
| STANDARDIZED_TABLETS | ADMINISTRATION | WRITING | 197 | 197 | 0 | 12 |
| TUTORS | EDUCATION | WRITING | 197 | 197 | 0 | 17 |
| ACCOUNTING | ADMINISTRATION | MATHEMATICS | 217 | 218 | 1 | 5 |
| FORTIFICATION | MILITARY | MASONRY | 117 | 218 | 101 | 11 |
| COINAGE | ECONOMY | CURRENCY | 240 | 241 | 1 | 0 |
| FISCUS | TAXATION | CURRENCY | 240 | 241 | 1 | 0 |
| PROLETARIAT | EMPLOYMENT | CURRENCY | 240 | 241 | 1 | 0 |
| PATRICIAN | LEADERSHIP | CODE_OF_LAWS | 252 | 253 | 1 | 0 |
| BOOKKEEPING | ADMINISTRATION | LITERATURE | 260 | 261 | 1 | 0 |

*turns; who: human; turn: each civic adopted after the start; rows counted: 15; source: civics in each CIVICS command of the human not in its previous one (A lines), the tech each requires (CivicInfo TechPrereq) and the turn the human got it (X lines; turn 0: held from the start), and the AIs holding that civic at the save [game3]. Every value counted (15).*

| civic | civic_option | prerequisite | tech_turn | adopted_turn | lag_turns | ais_holding_it_at_save |
|---|---|---|---|---|---|---|
| OLIGARCHY | LEADERSHIP | SLAVERY | 34 | 35 | 1 | 0 |
| TRIBUTE | TAXATION | SLAVERY | 34 | 35 | 1 | 0 |
| TABLETS | ADMINISTRATION | POTTERY | 87 | 88 | 1 | 0 |
| SPIRITISM | RELIGION | MYSTICISM | 137 | 138 | 1 | 14 |
| ELDERS | EDUCATION | MYSTICISM | 137 | 146 | 9 | 0 |
| STANDARDIZED_TABLETS | ADMINISTRATION | WRITING | 205 | 205 | 0 | 6 |
| TUTORS | EDUCATION | WRITING | 205 | 205 | 0 | 17 |
| ACCOUNTING | ADMINISTRATION | MATHEMATICS | 221 | 222 | 1 | 11 |
| FORTIFICATION | MILITARY | MASONRY | 121 | 229 | 108 | 16 |
| METALS | ECONOMY | METAL_CASTING | 191 | 229 | 38 | 0 |
| COINAGE | ECONOMY | CURRENCY | 244 | 245 | 1 | 0 |
| PROLETARIAT | EMPLOYMENT | CURRENCY | 244 | 245 | 1 | 0 |
| FISCUS | TAXATION | CURRENCY | 244 | 268 | 24 | 0 |

*turns; who: human; turn: each civic adopted after the start; rows counted: 13; source: civics in each CIVICS command of the human not in its previous one (A lines), the tech each requires (CivicInfo TechPrereq) and the turn the human got it (X lines; turn 0: held from the start), and the AIs holding that civic at the save [game4]. Every value counted (13).*

Every tech the human acquired, against the AIs:

| tech | human_turn | via | ai_median_turn | ais_with_it | ais_before_human |
|---|---|---|---|---|---|
| SLAVERY | 31 | research | 122.0 | 17 | 0 |
| POTTERY | 65 | research | 136.5 | 18 | 1 |
| MINING | 84 | research | 81.5 | 18 | 11 |
| NATUROPATHY | 97 | research | 56.0 | 18 | 18 |
| MASONRY | 117 | research | 194.5 | 18 | 5 |
| MYSTICISM | 129 | research | 31.0 | 18 | 18 |
| RELIGION_NORDIC | 138 | research |  | 0 | 0 |
| TRADE | 155 | research | 162.5 | 18 | 7 |
| METAL_CASTING | 173 | research | 190.5 | 18 | 4 |
| SAILING | 181 | deal | 139.0 | 17 | 13 |
| BRONZE_WORKING | 192 | research | 239.0 | 9 | 0 |
| PRIESTHOOD | 196 | research | 177.5 | 18 | 15 |
| WRITING | 197 | deal | 205.0 | 18 | 7 |
| THE_WHEEL | 205 | research | 229.0 | 13 | 0 |
| MATHEMATICS | 217 | research | 248.0 | 12 | 2 |
| FERMENTATION | 221 | deal | 239.5 | 10 | 3 |
| CITY_PLANNING | 229 | research | 236.0 | 1 | 0 |
| MONARCHY | 236 | deal | 254.0 | 13 | 3 |
| CURRENCY | 240 | research |  | 0 | 0 |
| MILITARY_TRAINING | 246 | research |  | 0 | 0 |
| IRON_WORKING | 248 | research | 246.0 | 5 | 3 |
| ARCHERY | 249 | research | 263.0 | 3 | 0 |
| CODE_OF_LAWS | 252 | research | 262.0 | 1 | 0 |
| ALPHABET | 256 | research | 266.0 | 1 | 0 |
| LITERATURE | 260 | research |  | 0 | 0 |
| SEAFARING | 261 | research | 238.0 | 5 | 5 |
| CONSTRUCTION | 265 | research |  | 0 | 0 |

*turn; who: every player; turn: acquisition turns; rows counted: 27; source: X lines (the first of each player and tech; turn 0 is the start); source: a deal item giving the human that tech on the same turn (deal_items, TRADE_TECHNOLOGIES; the tech index of TechInfo, checked: every such item has the receiver's X line on its turn) [game3]. Every value counted (27).*

| tech | human_turn | via | ai_median_turn | ais_with_it | ais_before_human |
|---|---|---|---|---|---|
| SLAVERY | 34 | research | 110.0 | 19 | 2 |
| MINING | 61 | research | 85.0 | 19 | 2 |
| POTTERY | 87 | research | 152.0 | 19 | 0 |
| MASONRY | 121 | research | 169.0 | 19 | 4 |
| MYSTICISM | 137 | research | 33.0 | 19 | 19 |
| SAILING | 166 | research | 133.0 | 19 | 16 |
| ANIMAL_HUSBANDRY | 177 | deal | 32.0 | 19 | 19 |
| TRADE | 181 | research | 169.0 | 19 | 13 |
| PRIESTHOOD | 188 | deal | 176.0 | 19 | 13 |
| METAL_CASTING | 191 | research | 194.0 | 19 | 9 |
| RELIGION_GREEK | 198 | research |  | 0 | 0 |
| WRITING | 205 | deal | 202.0 | 19 | 11 |
| THE_WHEEL | 206 | deal | 210.0 | 19 | 8 |
| MATHEMATICS | 221 | research | 234.0 | 17 | 4 |
| BRONZE_WORKING | 228 | research | 254.0 | 15 | 2 |
| FERMENTATION | 231 | research | 268.0 | 14 | 1 |
| MONARCHY | 234 | deal | 248.0 | 17 | 5 |
| CITY_PLANNING | 237 | research | 270.0 | 12 | 0 |
| CURRENCY | 244 | research | 283.0 | 1 | 0 |
| CODE_OF_LAWS | 252 | research | 279.0 | 6 | 1 |
| IRON_WORKING | 254 | research | 263.0 | 14 | 4 |
| SEAFARING | 255 | research | 272.0 | 10 | 4 |
| MILITARY_TRAINING | 257 | research | 278.0 | 7 | 0 |
| ARCHERY | 258 | research | 267.5 | 12 | 2 |
| NAVAL_WARFARE | 259 | research |  | 0 | 0 |
| SHIP_BUILDING | 261 | research |  | 0 | 0 |
| SIEGE_WARFARE | 264 | research | 268.0 | 2 | 1 |
| MACHINERY | 272 | research |  | 0 | 0 |
| CONSTRUCTION | 274 | research | 273.0 | 4 | 2 |
| CHARIOTRY | 275 | research |  | 0 | 0 |
| HORSEBACK_RIDING | 276 | research |  | 0 | 0 |
| SCULPTURE | 277 | research |  | 0 | 0 |
| CALENDAR | 283 | deal | 262.0 | 5 | 4 |
| WATERWORKS | 284 | research |  | 0 | 0 |
| MONOTHEISM | 285 | deal | 245.0 | 1 | 1 |

*turn; who: every player; turn: acquisition turns; rows counted: 35; source: X lines (the first of each player and tech; turn 0 is the start); source: a deal item giving the human that tech on the same turn (deal_items, TRADE_TECHNOLOGIES; the tech index of TechInfo, checked: every such item has the receiver's X line on its turn) [game4]. Every value counted (35).*

## 4. Expansion

The turn of each player's first to eighth founded city, the human against the AI median:

| city_number | human_turn | ai_median_turn | ais_reaching_it |
|---|---|---|---|
| 1 | 0 | 0.0 | 17 |
| 2 | 108 | 106.0 | 17 |
| 3 | 127 | 140.0 | 17 |
| 4 | 146 | 178.0 | 16 |
| 5 | 165 | 202.5 | 14 |
| 6 | 221 | 199.0 | 9 |
| 7 | 225 | 222.5 | 8 |
| 8 |  | 237.0 | 7 |

*turn; who: every player; turn: founding turns; rows counted: 8; source: the turn of each player's k-th city founded: the human's from its FOUND commands (A lines), the AIs' from the founding turn of the save's cities, credited to the first owner (the old owner of the first K or Z line on the plot); AI cities razed before the save are not in the save and are missing [game3]. Every value counted (8).*

| city_number | human_turn | ai_median_turn | ais_reaching_it |
|---|---|---|---|
| 1 | 0 | 0.0 | 18 |
| 2 | 87 | 103.5 | 18 |
| 3 | 100 | 135.0 | 18 |
| 4 | 116 | 181.0 | 16 |
| 5 | 138 | 196.5 | 16 |
| 6 | 156 | 211.5 | 16 |
| 7 | 172 | 241.0 | 15 |
| 8 | 188 | 246.0 | 14 |

*turn; who: every player; turn: founding turns; rows counted: 8; source: the turn of each player's k-th city founded: the human's from its FOUND commands (A lines), the AIs' from the founding turn of the save's cities, credited to the first owner (the old owner of the first K or Z line on the plot); AI cities razed before the save are not in the save and are missing [game4]. Every value counted (8).*

The distance of each new city to the founder's nearest earlier city:

| side | cities | median_distance | d_2_or_less | d_3 | d_4 | d_5 | d_6_plus |
|---|---|---|---|---|---|---|---|
| human | 6 | 3.5 | 0 | 3 | 2 | 1 | 0 |
| AI | 105 | 4.0 | 18 | 32 | 20 | 16 | 19 |

*cities; who: every player; turn: founding turns; rows counted: 2; source: every city after a player's first: grid distance (map wrap ignored) to the nearest city the same player founded before it, as in the expansion table [game3]. Every value counted (2).*

| side | cities | median_distance | d_2_or_less | d_3 | d_4 | d_5 | d_6_plus |
|---|---|---|---|---|---|---|---|
| human | 12 | 3.0 | 3 | 4 | 4 | 1 | 0 |
| AI | 174 | 3.0 | 45 | 43 | 38 | 18 | 30 |

*cities; who: every player; turn: founding turns; rows counted: 2; source: every city after a player's first: grid distance (map wrap ignored) to the nearest city the same player founded before it, as in the expansion table [game4]. Every value counted (2).*

## 5. War

### 5.1 Whom the human attacks

Each declaration: the options, and the target's rank among them on each cue (the first rank: the
least power, the least distance, the most cities):

| turn | target | options | power_rank | distance_rank | cities_rank | target_power | least_power | target_distance | least_distance |
|---|---|---|---|---|---|---|---|---|---|
| 203 | 5 | 17 | 8 | 1 | 2 | 71 | 20 | 2 | 2 |
| 209 | 7 | 17 | 7 | 1 | 15 | 67 | 23 | 4 | 4 |

*rank; who: human; turn: each declaration of the human (cues from the turn before); rows counted: 2; source: strategy.py: W lines of game3; options: AIs with an M line the turn before, holding a city, not at war with the human, not unmet at the save; rank 1 = the least power, the least distance, the most cities. Every value counted (2).*

| turn | target | options | power_rank | distance_rank | cities_rank | target_power | least_power | target_distance | least_distance |
|---|---|---|---|---|---|---|---|---|---|
| 238 | 14 | 18 | 4 | 1 | 11 | 135 | 49 | 3 | 3 |
| 252 | 2 | 18 | 15 | 4 | 6 | 379 | 77 | 4 | 2 |
| 257 | 6 | 18 | 6 | 3 | 11 | 252 | 93 | 4 | 2 |
| 268 | 7 | 18 | 13 | 1 | 9 | 437 | 90 | 3 | 3 |
| 271 | 14 | 18 | 2 | 7 | 17 | 153 | 102 | 6 | 3 |
| 272 | 10 | 17 | 9 | 13 | 8 | 431 | 108 | 15 | 3 |
| 277 | 2 | 16 | 8 | 1 | 13 | 454 | 124 | 3 | 3 |
| 283 | 7 | 15 | 6 | 1 | 10 | 456 | 143 | 3 | 3 |

*rank; who: human; turn: each declaration of the human (cues from the turn before); rows counted: 8; source: strategy.py: W lines of game4; options: AIs with an M line the turn before, holding a city, not at war with the human, not unmet at the save; rank 1 = the least power, the least distance, the most cities. Every value counted (8).*

The candidate rules:

| strategy | choices_matched | decisions | error_rate | log_likelihood | bic |
|---|---|---|---|---|---|
| weakest | 0 | 10 | 1.0 | -27.83 | 57.96 |
| nearest | 6 | 10 | 0.4 | -21.47 | 45.25 |
| nearest_then_weak | 3 | 10 | 0.7 | -25.56 | 53.42 |
| weak_of_near_half | 0 | 10 | 1.0 | -27.83 | 57.96 |
| most_cities | 0 | 10 | 1.0 | -27.83 | 57.96 |
| weakest_ratio | 0 | 10 | 1.0 | -27.83 | 57.96 |
| guessing |  | 10 |  | -28.43 | 56.86 |

*category; who: human; turn: each declaration of the human; rows counted: 10; source: strategy.py: maximum-likelihood classification over the declarations of every game given. Every value counted (7).*

| strategy | choices_matched | decisions | error_rate | log_likelihood | bic |
|---|---|---|---|---|---|
| weakest | 0 | 2 | 1.0 | -5.55 | 11.78 |
| nearest | 2 | 2 | 0.0 | 0.0 | 0.69 |
| nearest_then_weak | 2 | 2 | 0.0 | 0.0 | 0.69 |
| weak_of_near_half | 0 | 2 | 1.0 | -5.55 | 11.78 |
| most_cities | 0 | 2 | 1.0 | -5.55 | 11.78 |
| weakest_ratio | 0 | 2 | 1.0 | -5.55 | 11.78 |
| guessing |  | 2 |  | -5.67 | 11.33 |

*category; who: human; turn: each declaration of the human; rows counted: 2; source: strategy.py: maximum-likelihood classification over the declarations of game3. Every value counted (7).*

| strategy | choices_matched | decisions | error_rate | log_likelihood | bic |
|---|---|---|---|---|---|
| weakest | 0 | 8 | 1.0 | -22.29 | 46.65 |
| nearest | 4 | 8 | 0.5 | -20.29 | 42.65 |
| nearest_then_weak | 1 | 8 | 0.875 | -22.47 | 47.01 |
| weak_of_near_half | 0 | 8 | 1.0 | -22.29 | 46.65 |
| most_cities | 0 | 8 | 1.0 | -22.29 | 46.65 |
| weakest_ratio | 0 | 8 | 1.0 | -22.29 | 46.65 |
| guessing |  | 8 |  | -22.77 | 45.53 |

*category; who: human; turn: each declaration of the human; rows counted: 8; source: strategy.py: maximum-likelihood classification over the declarations of game4. Every value counted (7).*

### 5.2 Before the declaration

City orders for units, upgrades and moves in the ten turns before each declaration, against the
rate over the fifty turns before those:

| turn | target | train_10_before | train_per_10_earlier | upgrades_10_before | upgrades_per_10_earlier | moves_10_before | moves_per_10_earlier |
|---|---|---|---|---|---|---|---|
| 186 | 7 | 9 | 4.4 | 0 | 0.4 | 32 | 10.6 |
| 193 | 1 | 15 | 5.0 | 0 | 0.4 | 73 | 11.6 |
| 206 | 14 | 0 | 7.2 | 0 | 1.2 | 58 | 29.8 |

*orders; who: human; turn: the ten turns before each declaration, against the fifty before those; rows counted: 3; source: A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game1]. Every value counted (3).*

| turn | target | train_10_before | train_per_10_earlier | upgrades_10_before | upgrades_per_10_earlier | moves_10_before | moves_per_10_earlier |
|---|---|---|---|---|---|---|---|
| 92 | 16 | 1 | 0.8 | 0 | 0.0 | 3 | 0.4 |
| 229 | 11 | 10 | 3.4 | 8 | 0.4 | 18 | 13.0 |
| 230 | 9 | 13 | 3.4 | 7 | 0.6 | 34 | 12.6 |

*orders; who: human; turn: the ten turns before each declaration, against the fifty before those; rows counted: 3; source: A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game2]. Every value counted (3).*

| turn | target | train_10_before | train_per_10_earlier | upgrades_10_before | upgrades_per_10_earlier | moves_10_before | moves_per_10_earlier |
|---|---|---|---|---|---|---|---|
| 203 | 5 | 4 | 1.8 | 2 | 0.0 | 6 | 7.0 |
| 209 | 7 | 2 | 2.0 | 6 | 0.4 | 22 | 7.2 |

*orders; who: human; turn: the ten turns before each declaration, against the fifty before those; rows counted: 2; source: A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game3]. Every value counted (2).*

| turn | target | train_10_before | train_per_10_earlier | upgrades_10_before | upgrades_per_10_earlier | moves_10_before | moves_per_10_earlier |
|---|---|---|---|---|---|---|---|
| 238 | 14 | 11 | 3.6 | 9 | 0.4 | 12 | 13.2 |
| 252 | 2 | 7 | 4.4 | 0 | 3.2 | 38 | 15.0 |
| 257 | 6 | 9 | 4.8 | 0 | 3.2 | 47 | 16.4 |
| 268 | 7 | 16 | 6.2 | 24 | 3.0 | 32 | 23.6 |
| 271 | 14 | 21 | 6.4 | 49 | 3.2 | 46 | 24.2 |
| 272 | 10 | 20 | 7.0 | 51 | 3.2 | 51 | 24.6 |
| 277 | 2 | 21 | 8.2 | 37 | 7.0 | 84 | 27.2 |
| 283 | 7 | 19 | 11.0 | 2 | 14.0 | 94 | 36.4 |

*orders; who: human; turn: the ten turns before each declaration, against the fifty before those; rows counted: 8; source: A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game4]. Every value counted (8).*

### 5.3 The attacks

Every battle the human started, by the attacking unit:

| att_unit | battles | won | lost | median_odds_per_mille | median_experience | against_city_defence |
|---|---|---|---|---|---|---|
| CELTIC_WARBAND | 29 | 22 | 7 | 830.0 | 9.0 | 26 |
| GALLEY | 2 | 1 | 1 | 676.0 | 6.0 | 0 |

*battles; who: human; turn: whole game; rows counted: 2; source: C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game1]. Every value counted (2).*

| att_unit | battles | won | lost | median_odds_per_mille | median_experience | against_city_defence |
|---|---|---|---|---|---|---|
| GREEK_PHALANX | 10 | 10 | 0 | 1000.0 | 16.0 | 5 |
| JAVELINEER | 8 | 4 | 1 | 280.0 | 6.0 | 6 |
| SARISSA | 3 | 3 | 0 | 995.0 | 9.0 | 2 |
| TRIREME | 3 | 3 | 0 | 1000.0 | 13.0 | 0 |
| GALLEY | 2 | 0 | 2 | 488.0 | 12.5 | 0 |
| HYPASPIST2 | 1 | 1 | 0 | 1000.0 | 16.0 | 1 |
| WARLORDI | 1 | 1 | 0 | 994.0 | 19.0 | 1 |

*battles; who: human; turn: whole game; rows counted: 7; source: C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game2]. Every value counted (7).*

| att_unit | battles | won | lost | median_odds_per_mille | median_experience | against_city_defence |
|---|---|---|---|---|---|---|
| WARBAND | 14 | 10 | 2 | 810.5 | 6.0 | 14 |

*battles; who: human; turn: whole game; rows counted: 1; source: C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game3]. Every value counted (1).*

| att_unit | battles | won | lost | median_odds_per_mille | median_experience | against_city_defence |
|---|---|---|---|---|---|---|
| ROME_LEGIONARY | 53 | 45 | 5 | 972.0 | 15.0 | 37 |
| HASTATI | 10 | 6 | 3 | 915.0 | 9.0 | 6 |
| CENTURIO | 7 | 5 | 0 | 980.0 | 29.0 | 5 |
| QUINQUEREME | 6 | 6 | 0 | 992.0 | 8.0 | 0 |
| AUXILIAR | 2 | 2 | 0 | 928.0 | 4.5 | 1 |
| PRINCIPES | 2 | 2 | 0 | 984.5 | 10.0 | 2 |

*battles; who: human; turn: whole game; rows counted: 6; source: C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game4]. Every value counted (6).*

### 5.4 The peace

What the AI gave in the deal made on the day of each peace:

| turn | opp | gold_to_human | gold_per_turn_to_human | techs_to_human | cities_to_human | items_from_human |
|---|---|---|---|---|---|---|
| 206 | 5 | 0 | 0 | 0 | 0 | 0 |
| 214 | 7 | 0 | 0 | 0 | 0 | 0 |

*gold; who: human and the AI it made peace with; turn: each peace; rows counted: 2; source: Q lines of the human and the deal between the same two players on that turn (deal_items: TRADE_GOLD 0, TRADE_GOLD_PER_TURN 1, TRADE_TECHNOLOGIES 9, TRADE_CITIES 11; the peace treaty items, 8, left out) [game3]. Every value counted (2).*

| turn | opp | gold_to_human | gold_per_turn_to_human | techs_to_human | cities_to_human | items_from_human |
|---|---|---|---|---|---|---|
| 240 | 14 | 0 | 0 | 0 | 0 | 0 |
| 254 | 2 | 220 | 0 | 0 | 0 | 0 |
| 261 | 6 | 255 | 0 | 0 | 0 | 0 |
| 270 | 7 | 430 | 0 | 0 | 0 | 0 |
| 285 | 2 | 0 | 1 | 1 | 0 | 0 |

*gold; who: human and the AI it made peace with; turn: each peace; rows counted: 5; source: Q lines of the human and the deal between the same two players on that turn (deal_items: TRADE_GOLD 0, TRADE_GOLD_PER_TURN 1, TRADE_TECHNOLOGIES 9, TRADE_CITIES 11; the peace treaty items, 8, left out) [game4]. Every value counted (5).*

## 6. Parts from the other studies

| Part | Where |
|---|---|
| The capital trains the units; the other cities build | `study/human.md`, section 6, reading 1 |
| The slider follows the sign of gold per turn | `study/human.md`, section 6, reading 2 |
| Workers are directed by hand; fighting units build too; the land next to the cities first | `study/operations.md`, section 6, readings on workers |
| Captured workers make up a large part of the human's workers | `study/operations.md`, section 2.2 |
| City orders are mostly buildings; the human almost never queues | `study/operations.md`, section 3.1 |
| Tiles are re-planned as techs arrive; cottages become mines | `study/data.md`, section 5, reading 1 |
| Trade routes per city are about twice the AI's | `study/data.md`, section 3 |
| Commerce about doubles at the switch to Coinage, Fiscus and Proletariat | `study/winning.md`, section 7, reading 2 |
| Tech is sold to the AIs, several times more given than received | `study/winning.md`, section 5 |
| Wars at a power advantage; the AIs barely strike back | `study/winning.md`, section 6 |
| Single units in short steps, converging on the target | `study/operations.md`, section 4 |

## 7. The playstyle

The plan the parts fit, in the order a game runs. Each element names its facts and what would
refute it.

1. **A long, quiet opening.** One city for the first phase, with little activity of any kind.
   - Facts: the first phase of every game ends with one city (section 2). The AIs found their
     second city at about the same time (section 4), so this is the game's pace, not the
     human's choice.
2. **Research is planned around civics, and each civic is taken the moment it is open.**
   - Facts:
     - most civics are adopted on the turn their tech arrives or the next (section 3);
     - the first target is Slavery, which opens Oligarchy and Tribute, both adopted at once,
       far earlier than the AIs get Slavery;
     - the later targets open Accounting (Mathematics) and Coinage, Fiscus and Proletariat
       (Currency). Their XML effects are in the appendix.
   - The exceptions fit the same plan. Fortification is taken shortly before or after a war.
     Metals comes with the start of a golden age, when a switch costs no anarchy
     (`study/winning.md`, section 3.2).
   - Mysticism, which the AIs take early, comes after every AI in both games; when it comes, its
     civics are adopted at once. Animal Husbandry comes only by trade in game 4.
   - Refuted if: in a further game, civics follow their tech by many turns as a rule.
3. **Expansion in the middle game, dense and near.**
   - Facts (section 4):
     - the human founds its third to fifth city well before the AI median in game 3, and its
       second to eighth in game 4; in game 3 its later cities come by capture;
     - it never founds a city six or more plots from its others, while the AIs often do.
4. **An economy of buildings, worked land and trade, run by hand.**
   - Facts: section 6, the rows from `study/human.md`, `study/operations.md` and `study/data.md`.
     The development phase is the longest of every game, with more build orders and building
     orders than before (section 2).
5. **Technology is a currency.** The human researches the civic techs itself and sells techs.
   - Facts: section 3 (research or deal for each tech) and `study/winning.md`, section 5.
6. **Conquest comes late, against the nearest neighbour, prepared and short.**
   - Facts:
     - the fighting starts in the third or fourth phase of every game, and that boundary holds
       at every penalty (section 2);
     - the target is best predicted by distance alone: the nearest-neighbour rule matches more
       declarations than any other rule, with the best likelihood and BIC. The weakest AI is
       never the target, and the targets' power ranks are spread over the field (section 5.1);
     - in the ten turns before a declaration, the human gives more unit orders than before in
       nearly every case, and in game 2, game 3 and game 4 the first declaration of a campaign follows a burst
       of upgrades (section 5.2);
     - the attacks are made at high odds with experienced units, and in game 1, game 3 and
       game 4 mostly with one unit type (section 5.3; promotions in `study/data.md`, section 4);
     - in game 3 and game 4 the wars are short; in game 4 most of its peace deals pay the human
       gold (section 5.4; `study/winning.md`, section 6);
     - captured workers are part of the gain (`study/operations.md`, section 2.2).
   - Refuted if: a further game where the human attacks a distant AI while a nearer one is
     open, or declares without a build-up.
7. **After a conquest: build, or conquer again.** In game 3 the war is followed by a long
   building phase. In game 4 a second, larger campaign follows within a phase (section 2).

What the plan does not place:
- Game 2 opens a war in its second phase that lasts most of the game with almost no
  attacks (section 2; `study/winning.md`, section 6). It reads as a war declared and left
  open, but nothing in the log says why.
- The Javelineers' low-odds attacks in game 2 (section 5.3).

## 8. What it implies for the AI

These are the points where the plan meets an AI weakness found in the other studies. Each is
a candidate for an AI change, judged only by experiment (CLAUDE.md, rule 9).
- **Civics.** The AIs neither research Currency nor run its civics (`study/winning.md`,
  reading 3).
- **The nearest neighbour is the target.** The AI closest to the human is the one attacked
  (section 5.1). Whether the AI's defence takes account of that is open.
- **No counter-attack.** The human's wars are won without the AIs attacking its units or
  cities (`study/winning.md`, reading 5).
- **The build-up is visible.** Unit orders, and in most campaigns upgrades, rise before a
  declaration (section 5.2). Those are the human's own commands; what the AI sees of them is its units near the
  border.
- **Workers left in reach** are taken (`study/operations.md`, section 2.2).
- **Peace is bought** with gold in game 4 (section 5.4).

## 9. Open

- **More games.** The war-target rule rests on ten declarations in two games, and the civic
  timing on two games. Game 1 and game 2 have no M lines and no save dump, so their power and
  cities cannot be compared.
- **What the AI sees** of the build-up: units near its border before a declaration, from G lines
  or saves at intervals.
- **Why game 2's first war stays open** without fighting.

## Appendix: XML records of the types counted

| CivicInfo | Fields set (records.json) |
|---|---|
| ACCOUNTING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [25,0,0]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -30; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| BARTER | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_TRADE; `TradeYieldModifiers` [20,0,-25]; `Upkeep` UPKEEP_LOW; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iImprovementUpgradeRateModifier` 10; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| BOOKKEEPING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [30,0,0,25]; `TechPrereq` TECH_LITERATURE; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -50; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| COINAGE | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [25,0,0]; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 20; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iTradeRoutes` 1; `iWarWearinessModifier` 25 |
| ELDERS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_MYSTICISM; `YieldModifiers` [0,0,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 25; `iGreatPeopleRateModifier` 25; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| FISCUS | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_TREASURY","iHappinessChange":-5}]; `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [50,0,0,25]; `Hurrys` [{"HurryType":"HURRY_GOLD","bHurry":true}]; `TechPrereq` TECH_CURRENCY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iLargestCityHappiness` -5; `iNumCitiesMaintenanceModifier` 20; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| FORTIFICATION | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_WALLS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MASONRY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAIWeight` 1; `iAnarchyLength` 1; `iDomesticGreatGeneralRateModifier` 100; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| OLIGARCHY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 30; `iFreeExperience` 3; `iRevDemocracyLevel` -5; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |
| PATRICIAN | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MARKET","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_BANK","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PRAEFECTUR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `TradeYieldModifiers` [0,0,25]; `Upkeep` UPKEEP_LOW; `bCanDoElection` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0.5; `fRevViolentMod` 0; `iAnarchyLength` 1; `iCorporationMaintenanceModifier` -10; `iDistanceMaintenanceModifier` 25; `iGreatGeneralRateModifier` 30; `iRevDemocracyLevel` 1; `iRevEnvironmentalProtection` -2; `iRevIdxDistanceModifier` 20; `iRevIdxLocal` 2; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 100 |
| PROLETARIAT | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_SHAFT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WORKSHOP","ImprovementYields":[1,2,0]},{"ImprovementType":"IMPROVEMENT_LUMBERMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WINDMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WATERMILL","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [0,50,0]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 3; `iWorkerSpeedModifier` 25 |
| SPIRITISM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_ORACLE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_STONEHENGE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_RELIGION; `CommerceModifiers` [0,0,0,25]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[0,0,2]}]; `TechPrereq` TECH_MYSTICISM; `bStateReligion` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatPeopleRateModifier` 25; `iRevIdxSwitchTo` -30; `iRevReligiousFreedom` 7; `iStateReligionFreeExperience` 3 |
| STANDARDIZED_TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_WRITING; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -25; `iNumCitiesMaintenanceModifier` 10; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_POTTERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,-10,-10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -10; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 10; `iRevIdxLocal` -1; `iRevIdxSwitchTo` 20 |
| TRIBUTE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CapitalCommerceModifiers` [0,0,25]; `CapitalYieldModifiers` [25,25,25]; `CivicOptionType` CIVICOPTION_TAXATION; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,0,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAIWeight` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iNumCitiesMaintenanceModifier` 10; `iRevDemocracyLevel` -3; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| TUTORS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_WRITING; `YieldModifiers` [10,10,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 30; `iGreatPeopleRateModifier` 30; `iRevIdxDistanceModifier` 25; `iRevIdxLocal` -1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| CivicInfo | Fields set (records.json) |
|---|---|
| ACCOUNTING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [25,0,0]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -30; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| COINAGE | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [25,0,0]; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 20; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iTradeRoutes` 1; `iWarWearinessModifier` 25 |
| ELDERS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_MYSTICISM; `YieldModifiers` [0,0,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 25; `iGreatPeopleRateModifier` 25; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| FISCUS | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_TREASURY","iHappinessChange":-5}]; `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [50,0,0,25]; `Hurrys` [{"HurryType":"HURRY_GOLD","bHurry":true}]; `TechPrereq` TECH_CURRENCY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iLargestCityHappiness` -5; `iNumCitiesMaintenanceModifier` 20; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| FORTIFICATION | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_WALLS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MASONRY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAIWeight` 1; `iAnarchyLength` 1; `iDomesticGreatGeneralRateModifier` 100; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| METALS | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_METAL_CASTING; `TradeYieldModifiers` [20,0,-10]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 15; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| OLIGARCHY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 30; `iFreeExperience` 3; `iRevDemocracyLevel` -5; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |
| PROLETARIAT | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_SHAFT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WORKSHOP","ImprovementYields":[1,2,0]},{"ImprovementType":"IMPROVEMENT_LUMBERMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WINDMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WATERMILL","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [0,50,0]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 3; `iWorkerSpeedModifier` 25 |
| SPIRITISM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_ORACLE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_STONEHENGE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_RELIGION; `CommerceModifiers` [0,0,0,25]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[0,0,2]}]; `TechPrereq` TECH_MYSTICISM; `bStateReligion` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatPeopleRateModifier` 25; `iRevIdxSwitchTo` -30; `iRevReligiousFreedom` 7; `iStateReligionFreeExperience` 3 |
| STANDARDIZED_TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_WRITING; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -25; `iNumCitiesMaintenanceModifier` 10; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_POTTERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,-10,-10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -10; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 10; `iRevIdxLocal` -1; `iRevIdxSwitchTo` 20 |
| TRIBUTE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CapitalCommerceModifiers` [0,0,25]; `CapitalYieldModifiers` [25,25,25]; `CivicOptionType` CIVICOPTION_TAXATION; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,0,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAIWeight` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iNumCitiesMaintenanceModifier` 10; `iRevDemocracyLevel` -3; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| TUTORS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_WRITING; `YieldModifiers` [10,10,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 30; `iGreatPeopleRateModifier` 30; `iRevIdxDistanceModifier` 25; `iRevIdxLocal` -1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| TechInfo | Fields set (records.json) |
|---|---|
| ALPHABET | `Advisor` ADVISOR_SCIENCE; `CommerceFlexible` [false,false,false,true]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":8},{"FlavorType":"FLAVOR_GOLD","iFlavor":4},{"FlavorType":"FLAVOR_ESPIONAGE","iFlavor":10}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_ALPHABET_QUOTE; `Sound` AS2D_TECH_ALPHABET; `SoundMP` AS2D_TECH_MP_ALPHABET; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 240; `iGridX` 5; `iGridY` 3; `iPower` 4 |
| ARCHERY | `Advisor` ADVISOR_MILITARY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_HUNTING"]; `Quote` TXT_KEY_TECH_ARCHERY_QUOTE; `Sound` AS2D_TECH_ARCHERY; `SoundMP` AS2D_TECH_MP_ARCHERY; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 60; `iGridX` 2; `iGridY` 8; `iPower` 6 |
| BRONZE_WORKING | `Advisor` ADVISOR_MILITARY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":6},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":5},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_CULTURE","iFlavor":1}]; `OrPreReqs` ["TECH_METAL_CASTING"]; `Quote` TXT_KEY_TECH_BRONZE_WORKING_QUOTE; `Sound` AS2D_TECH_BRONZEWORK; `SoundMP` AS2D_TECH_MP_BRONZEWORK; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 160; `iGridX` 4; `iGridY` 17; `iPower` 8 |
| CITY_PLANNING | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_MATHEMATICS"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_CULTURE","iFlavor":9}]; `OrPreReqs` ["TECH_SAILING","TECH_ANIMAL_HUSBANDRY"]; `Quote` TXT_KEY_TECH_CITY_PLANNING_QUOTE; `Sound` AS2D_TECH_GENERIC; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 260; `iGridX` 6; `iGridY` 13 |
| CODE_OF_LAWS | `Advisor` ADVISOR_RELIGION; `AndPreReqs` ["TECH_WRITING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_RELIGION","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_MONARCHY"]; `Quote` TXT_KEY_TECH_CODE_OF_LAWS_QUOTE; `Sound` AS2D_TECH_CODE_OF_LAWS; `SoundMP` AS2D_TECH_MP_CODE_OF_LAWS; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 11 |
| CONSTRUCTION | `Advisor` ADVISOR_GROWTH; `AndPreReqs` ["TECH_MASONRY"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_RELIGION","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":1},{"FlavorType":"FLAVOR_GROWTH","iFlavor":2}]; `OrPreReqs` ["TECH_MATHEMATICS"]; `Quote` TXT_KEY_TECH_CONSTRUCTION_QUOTE; `Sound` AS2D_TECH_CONSTRUCTION; `SoundMP` AS2D_TECH_MP_CONSTRUCTION; `bBridgeBuilding` True; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 5; `iPower` 4 |
| CURRENCY | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_MATHEMATICS","TECH_METAL_CASTING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_CURRENCY_QUOTE; `Sound` AS2D_TECH_CURRENCY; `SoundMP` AS2D_TECH_MP_CURRENCY; `bGoldTrading` True; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 400; `iGridX` 5; `iGridY` 7 |
| FERMENTATION | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_AGRICULTURE","TECH_NATUROPATHY","TECH_POTTERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":6},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `Quote` TXT_KEY_TECH_FERMENTATION_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 95; `iGridX` 4; `iGridY` 3 |
| IRON_WORKING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_MONARCHY"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":6}]; `OrPreReqs` ["TECH_BRONZE_WORKING"]; `Quote` TXT_KEY_TECH_IRON_WORKING_QUOTE; `Sound` AS2D_TECH_IRONWORK; `SoundMP` AS2D_TECH_MP_IRONWORK; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 200; `iGridX` 6; `iGridY` 17; `iPower` 10 |
| LITERATURE | `Advisor` ADVISOR_CULTURE; `AndPreReqs` ["TECH_ALPHABET"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_RELIGION","iFlavor":4},{"FlavorType":"FLAVOR_CULTURE","iFlavor":10},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10}]; `Quote` TXT_KEY_TECH_LITERATURE_QUOTE; `Sound` AS2D_TECH_LITERATURE; `SoundMP` AS2D_TECH_MP_LITERATURE; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 1 |
| MASONRY | `Advisor` ADVISOR_ECONOMY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_RELIGION","iFlavor":8},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_MINING"]; `Quote` TXT_KEY_TECH_MASONRY_QUOTE; `Sound` AS2D_TECH_MASONRY; `SoundMP` AS2D_TECH_MP_MASONRY; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 64; `iGridX` 3; `iGridY` 15 |
| MATHEMATICS | `Advisor` ADVISOR_SCIENCE; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":1},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_MATHEMATICS_QUOTE; `Sound` AS2D_TECH_MATHEMATICS; `SoundMP` AS2D_TECH_MP_MATHEMATICS; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 250; `iFeatureProductionModifier` 50; `iGridX` 5; `iGridY` 5; `iPower` 6 |
| METAL_CASTING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":9},{"FlavorType":"FLAVOR_GOLD","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_MINING"]; `Quote` TXT_KEY_TECH_METAL_CASTING_QUOTE; `Sound` AS2D_TECH_METALCAST; `SoundMP` AS2D_TECH_MP_METALCAST; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 90; `iGridX` 3; `iGridY` 17; `iPower` 4 |
| MILITARY_TRAINING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_HUNTING"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_BRONZE_WORKING"]; `Quote` TXT_KEY_TECH_MILITARY_TRAINING_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 10; `iCost` 176; `iGridX` 5; `iGridY` 15; `iPower` 10 |
| MINING | `Advisor` ADVISOR_ECONOMY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":8},{"FlavorType":"FLAVOR_GOLD","iFlavor":5},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":3}]; `Quote` TXT_KEY_TECH_MINING2_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 40; `iGridX` 2; `iGridY` 16; `iPower` 2 |
| MONARCHY | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_TRADE","TECH_METAL_CASTING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":6},{"FlavorType":"FLAVOR_RELIGION","iFlavor":4},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":9}]; `OrPreReqs` ["TECH_WRITING","TECH_PRIESTHOOD","TECH_MONOTHEISM","TECH_BRONZE_WORKING","TECH_CASTE_SYSTEM"]; `Quote` TXT_KEY_TECH_MONARCHY_QUOTE; `Sound` AS2D_TECH_MONARCHY; `SoundMP` AS2D_TECH_MP_MONARCHY; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 240; `iGridX` 5; `iGridY` 9 |
| MYSTICISM | `Advisor` ADVISOR_RELIGION; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":9},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":8},{"FlavorType":"FLAVOR_GROWTH","iFlavor":2}]; `Quote` TXT_KEY_TECH_MYSTICISM_QUOTE; `Sound` AS2D_TECH_MYSTICISM; `SoundMP` AS2D_TECH_MP_MYSTICISM; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 40; `iGridX` 1; `iGridY` 11 |
| NATUROPATHY | `Advisor` ADVISOR_GROWTH; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":3},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `OrPreReqs` ["TECH_HUNTING"]; `Quote` TXT_KEY_TECH_NATUROPATHY_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 40; `iGridX` 2; `iGridY` 14 |
| POTTERY | `Advisor` ADVISOR_ECONOMY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":3},{"FlavorType":"FLAVOR_CULTURE","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":9}]; `OrPreReqs` ["TECH_AGRICULTURE","TECH_FISHING"]; `Quote` TXT_KEY_TECH_POTTERY_QUOTE; `Sound` AS2D_TECH_POTTERY; `SoundMP` AS2D_TECH_MP_POTTERY; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 60; `iGridX` 2; `iGridY` 3 |
| PRIESTHOOD | `Advisor` ADVISOR_RELIGION; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":6}]; `OrPreReqs` ["TECH_MYSTICISM"]; `Quote` TXT_KEY_TECH_PRIESTHOOD_QUOTE; `Sound` AS2D_TECH_PRIESTHOOD; `SoundMP` AS2D_TECH_MP_PRIESTHOOD; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 50; `iGridX` 3; `iGridY` 9 |
| RELIGION_NORDIC | `Advisor` ADVISOR_RELIGION; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":6},{"FlavorType":"FLAVOR_CULTURE","iFlavor":6},{"FlavorType":"FLAVOR_GROWTH","iFlavor":6}]; `OrPreReqs` ["TECH_MYSTICISM"]; `Sound` AS2D_UNIT_BUILD_AXEMAN; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 30; `iGridX` 1; `iGridY` 19 |
| SAILING | `Advisor` ADVISOR_GROWTH; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":1},{"FlavorType":"FLAVOR_GOLD","iFlavor":3},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":6},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_FISHING"]; `Quote` TXT_KEY_TECH_SAILING_QUOTE; `Sound` AS2D_TECH_SAILING; `SoundMP` AS2D_TECH_MP_SAILING; `TerrainTrades` [{"TerrainType":"TERRAIN_COAST","bTerrainTrade":true}]; `bGoodyTech` True; `bRiverTrade` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 80; `iGridX` 2; `iGridY` 1; `iPower` 2 |
| SEAFARING | `Advisor` ADVISOR_GROWTH; `AndPreReqs` ["TECH_SAILING"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":7},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":6}]; `OrPreReqs` ["TECH_NAVAL_WARFARE","TECH_TRADE"]; `Quote` TXT_KEY_TECH_SEAFARING_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 93; `iGridX` 4; `iGridY` 1; `iPower` 2 |
| SLAVERY | `Advisor` ADVISOR_MILITARY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":5},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":2}]; `OrPreReqs` ["TECH_HUNTING"]; `Quote` TXT_KEY_TECH_SLAVERY_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 40; `iGridX` 2; `iGridY` 10; `iPower` 6 |
| THE_WHEEL | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_ANIMAL_HUSBANDRY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":4},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":8},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `Quote` TXT_KEY_TECH_THE_WHEEL_QUOTE; `Sound` AS2D_TECH_THE_WHEEL; `SoundMP` AS2D_TECH_MP_THE_WHEEL; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 48; `iGridX` 2; `iGridY` 12; `iPower` 4 |
| TRADE | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_POTTERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_ANIMAL_HUSBANDRY","TECH_SAILING"]; `Quote` TXT_KEY_TECH_TRADE_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bOpenBordersTrading` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 85; `iGridX` 3; `iGridY` 3; `iTradeRoutes` 1 |
| WRITING | `Advisor` ADVISOR_SCIENCE; `AndPreReqs` ["TECH_PRIESTHOOD","TECH_TRADE"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10},{"FlavorType":"FLAVOR_CULTURE","iFlavor":6}]; `Quote` TXT_KEY_TECH_WRITING_QUOTE; `Sound` AS2D_TECH_WRITING; `SoundMP` AS2D_TECH_MP_WRITING; `bGoodyTech` True; `bTechTrading` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 96; `iGridX` 4; `iGridY` 5 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| TechInfo | Fields set (records.json) |
|---|---|
| ANIMAL_HUSBANDRY | `Advisor` ADVISOR_GROWTH; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_RELIGION","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":4},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":1},{"FlavorType":"FLAVOR_GROWTH","iFlavor":9}]; `OrPreReqs` ["TECH_HUNTING","TECH_AGRICULTURE"]; `Quote` TXT_KEY_TECH_ANIMAL_HUSBANDRY_QUOTE; `Sound` AS2D_TECH_ANIMALHUSB; `SoundMP` AS2D_TECH_MP_ANIMALHUSB; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 50; `iGridX` 2; `iGridY` 5; `iPower` 2 |
| ARCHERY | `Advisor` ADVISOR_MILITARY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_HUNTING"]; `Quote` TXT_KEY_TECH_ARCHERY_QUOTE; `Sound` AS2D_TECH_ARCHERY; `SoundMP` AS2D_TECH_MP_ARCHERY; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 60; `iGridX` 2; `iGridY` 8; `iPower` 6 |
| BRONZE_WORKING | `Advisor` ADVISOR_MILITARY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":6},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":5},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_CULTURE","iFlavor":1}]; `OrPreReqs` ["TECH_METAL_CASTING"]; `Quote` TXT_KEY_TECH_BRONZE_WORKING_QUOTE; `Sound` AS2D_TECH_BRONZEWORK; `SoundMP` AS2D_TECH_MP_BRONZEWORK; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 160; `iGridX` 4; `iGridY` 17; `iPower` 8 |
| CALENDAR | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_SAILING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":5},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":6},{"FlavorType":"FLAVOR_GROWTH","iFlavor":1}]; `OrPreReqs` ["TECH_MATHEMATICS"]; `Quote` TXT_KEY_TECH_CALENDAR_QUOTE; `Sound` AS2D_TECH_CALENDAR; `SoundMP` AS2D_TECH_MP_CALENDAR; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 7 |
| CHARIOTRY | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_ANIMAL_HUSBANDRY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_RELIGION","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":4},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":1},{"FlavorType":"FLAVOR_GROWTH","iFlavor":5}]; `OrPreReqs` ["TECH_THE_WHEEL"]; `Quote` TXT_KEY_TECH_CHARIOTRY_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 120; `iGridX` 3; `iGridY` 19; `iPower` 2 |
| CITY_PLANNING | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_MATHEMATICS"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_CULTURE","iFlavor":9}]; `OrPreReqs` ["TECH_SAILING","TECH_ANIMAL_HUSBANDRY"]; `Quote` TXT_KEY_TECH_CITY_PLANNING_QUOTE; `Sound` AS2D_TECH_GENERIC; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 260; `iGridX` 6; `iGridY` 13 |
| CODE_OF_LAWS | `Advisor` ADVISOR_RELIGION; `AndPreReqs` ["TECH_WRITING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_RELIGION","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_MONARCHY"]; `Quote` TXT_KEY_TECH_CODE_OF_LAWS_QUOTE; `Sound` AS2D_TECH_CODE_OF_LAWS; `SoundMP` AS2D_TECH_MP_CODE_OF_LAWS; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 11 |
| CONSTRUCTION | `Advisor` ADVISOR_GROWTH; `AndPreReqs` ["TECH_MASONRY"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_RELIGION","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":1},{"FlavorType":"FLAVOR_GROWTH","iFlavor":2}]; `OrPreReqs` ["TECH_MATHEMATICS"]; `Quote` TXT_KEY_TECH_CONSTRUCTION_QUOTE; `Sound` AS2D_TECH_CONSTRUCTION; `SoundMP` AS2D_TECH_MP_CONSTRUCTION; `bBridgeBuilding` True; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 5; `iPower` 4 |
| CURRENCY | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_MATHEMATICS","TECH_METAL_CASTING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_CURRENCY_QUOTE; `Sound` AS2D_TECH_CURRENCY; `SoundMP` AS2D_TECH_MP_CURRENCY; `bGoldTrading` True; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 400; `iGridX` 5; `iGridY` 7 |
| FERMENTATION | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_AGRICULTURE","TECH_NATUROPATHY","TECH_POTTERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":6},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `Quote` TXT_KEY_TECH_FERMENTATION_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 95; `iGridX` 4; `iGridY` 3 |
| HORSEBACK_RIDING | `Advisor` ADVISOR_MILITARY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":8},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":1},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":5}]; `OrPreReqs` ["TECH_CHARIOTRY"]; `Quote` TXT_KEY_TECH_HORSEBACK_RIDING_QUOTE; `Sound` AS2D_TECH_HORSERIDING; `SoundMP` AS2D_TECH_MP_HORSERIDING; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 150; `iGridX` 4; `iGridY` 19; `iPower` 10 |
| IRON_WORKING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_MONARCHY"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":6}]; `OrPreReqs` ["TECH_BRONZE_WORKING"]; `Quote` TXT_KEY_TECH_IRON_WORKING_QUOTE; `Sound` AS2D_TECH_IRONWORK; `SoundMP` AS2D_TECH_MP_IRONWORK; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 200; `iGridX` 6; `iGridY` 17; `iPower` 10 |
| MACHINERY | `Advisor` ADVISOR_MILITARY; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":6},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":10},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4}]; `OrPreReqs` ["TECH_SIEGE_WARFARE"]; `Quote` TXT_KEY_TECH_MACHINERY_QUOTE; `Sound` AS2D_TECH_MACHINERY; `SoundMP` AS2D_TECH_MP_MACHINERY; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 24; `iCost` 700; `iGridX` 8; `iGridY` 15; `iPower` 8 |
| MASONRY | `Advisor` ADVISOR_ECONOMY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_RELIGION","iFlavor":8},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_MINING"]; `Quote` TXT_KEY_TECH_MASONRY_QUOTE; `Sound` AS2D_TECH_MASONRY; `SoundMP` AS2D_TECH_MP_MASONRY; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 64; `iGridX` 3; `iGridY` 15 |
| MATHEMATICS | `Advisor` ADVISOR_SCIENCE; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":1},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_MATHEMATICS_QUOTE; `Sound` AS2D_TECH_MATHEMATICS; `SoundMP` AS2D_TECH_MP_MATHEMATICS; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 250; `iFeatureProductionModifier` 50; `iGridX` 5; `iGridY` 5; `iPower` 6 |
| METAL_CASTING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":9},{"FlavorType":"FLAVOR_GOLD","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_MINING"]; `Quote` TXT_KEY_TECH_METAL_CASTING_QUOTE; `Sound` AS2D_TECH_METALCAST; `SoundMP` AS2D_TECH_MP_METALCAST; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 90; `iGridX` 3; `iGridY` 17; `iPower` 4 |
| MILITARY_TRAINING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_HUNTING"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_BRONZE_WORKING"]; `Quote` TXT_KEY_TECH_MILITARY_TRAINING_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 10; `iCost` 176; `iGridX` 5; `iGridY` 15; `iPower` 10 |
| MINING | `Advisor` ADVISOR_ECONOMY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":8},{"FlavorType":"FLAVOR_GOLD","iFlavor":5},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":3}]; `Quote` TXT_KEY_TECH_MINING2_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 40; `iGridX` 2; `iGridY` 16; `iPower` 2 |
| MONARCHY | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_TRADE","TECH_METAL_CASTING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":6},{"FlavorType":"FLAVOR_RELIGION","iFlavor":4},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_CULTURE","iFlavor":9}]; `OrPreReqs` ["TECH_WRITING","TECH_PRIESTHOOD","TECH_MONOTHEISM","TECH_BRONZE_WORKING","TECH_CASTE_SYSTEM"]; `Quote` TXT_KEY_TECH_MONARCHY_QUOTE; `Sound` AS2D_TECH_MONARCHY; `SoundMP` AS2D_TECH_MP_MONARCHY; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 240; `iGridX` 5; `iGridY` 9 |
| MONOTHEISM | `Advisor` ADVISOR_RELIGION; `AndPreReqs` ["TECH_PRIESTHOOD","TECH_MASONRY","TECH_WRITING"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":10},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":8}]; `Quote` TXT_KEY_TECH_MONOTHEISM_QUOTE; `Sound` AS2D_TECH_MONOTHEISM; `SoundMP` AS2D_TECH_MP_MONOTHEISM; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 120; `iGridX` 4; `iGridY` 12 |
| MYSTICISM | `Advisor` ADVISOR_RELIGION; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":9},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":8},{"FlavorType":"FLAVOR_GROWTH","iFlavor":2}]; `Quote` TXT_KEY_TECH_MYSTICISM_QUOTE; `Sound` AS2D_TECH_MYSTICISM; `SoundMP` AS2D_TECH_MP_MYSTICISM; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 40; `iGridX` 1; `iGridY` 11 |
| NAVAL_WARFARE | `Advisor` ADVISOR_GROWTH; `AndPreReqs` ["TECH_ARCHERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_SAILING"]; `Quote` TXT_KEY_TECH_NAVAL_WARFARE_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 88; `iGridX` 3; `iGridY` 1; `iPower` 2 |
| POTTERY | `Advisor` ADVISOR_ECONOMY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":3},{"FlavorType":"FLAVOR_CULTURE","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":9}]; `OrPreReqs` ["TECH_AGRICULTURE","TECH_FISHING"]; `Quote` TXT_KEY_TECH_POTTERY_QUOTE; `Sound` AS2D_TECH_POTTERY; `SoundMP` AS2D_TECH_MP_POTTERY; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 60; `iGridX` 2; `iGridY` 3 |
| PRIESTHOOD | `Advisor` ADVISOR_RELIGION; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":6}]; `OrPreReqs` ["TECH_MYSTICISM"]; `Quote` TXT_KEY_TECH_PRIESTHOOD_QUOTE; `Sound` AS2D_TECH_PRIESTHOOD; `SoundMP` AS2D_TECH_MP_PRIESTHOOD; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 50; `iGridX` 3; `iGridY` 9 |
| RELIGION_GREEK | `Advisor` ADVISOR_RELIGION; `AndPreReqs` ["TECH_MYSTICISM"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":20},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":8},{"FlavorType":"FLAVOR_GROWTH","iFlavor":8},{"FlavorType":"FLAVOR_MILITARY","iFlavor":8}]; `OrPreReqs` ["TECH_GREEK","TECH_ROMAN"]; `Sound` AS2D_TECH_GENERIC; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 60; `iGridX` 2; `iGridY` 20 |
| SAILING | `Advisor` ADVISOR_GROWTH; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":1},{"FlavorType":"FLAVOR_GOLD","iFlavor":3},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":6},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_FISHING"]; `Quote` TXT_KEY_TECH_SAILING_QUOTE; `Sound` AS2D_TECH_SAILING; `SoundMP` AS2D_TECH_MP_SAILING; `TerrainTrades` [{"TerrainType":"TERRAIN_COAST","bTerrainTrade":true}]; `bGoodyTech` True; `bRiverTrade` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 80; `iGridX` 2; `iGridY` 1; `iPower` 2 |
| SCULPTURE | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_POTTERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_RELIGION","iFlavor":6},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":1},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_CULTURE","iFlavor":10}]; `OrPreReqs` ["TECH_CEREMONIAL_BURIAL","TECH_MASONRY"]; `Quote` TXT_KEY_TECH_SCULPTURE_QUOTE; `Sound` AS2D_TECH_GENERIC; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 120; `iGridX` 4; `iGridY` 14 |
| SEAFARING | `Advisor` ADVISOR_GROWTH; `AndPreReqs` ["TECH_SAILING"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":3},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":7},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":6}]; `OrPreReqs` ["TECH_NAVAL_WARFARE","TECH_TRADE"]; `Quote` TXT_KEY_TECH_SEAFARING_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 93; `iGridX` 4; `iGridY` 1; `iPower` 2 |
| SHIP_BUILDING | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_METAL_CASTING","TECH_NAVAL_WARFARE"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":9},{"FlavorType":"FLAVOR_GOLD","iFlavor":5},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":7},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":6}]; `OrPreReqs` ["TECH_SEAFARING"]; `Quote` TXT_KEY_TECH_SEAFARING_QUOTE; `Sound` AS2D_TECH_GENERIC; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 160; `iGridX` 5; `iGridY` 1; `iPower` 2 |
| SIEGE_WARFARE | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_MATHEMATICS","TECH_THE_WHEEL"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":4},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":6},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_IRON_WORKING"]; `Quote` TXT_KEY_TECH_SIEGE_WARFARE_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 300; `iGridX` 7; `iGridY` 16; `iPower` 10 |
| SLAVERY | `Advisor` ADVISOR_MILITARY; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":5},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":1},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":2}]; `OrPreReqs` ["TECH_HUNTING"]; `Quote` TXT_KEY_TECH_SLAVERY_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 40; `iGridX` 2; `iGridY` 10; `iPower` 6 |
| THE_WHEEL | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_ANIMAL_HUSBANDRY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":4},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":8},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `Quote` TXT_KEY_TECH_THE_WHEEL_QUOTE; `Sound` AS2D_TECH_THE_WHEEL; `SoundMP` AS2D_TECH_MP_THE_WHEEL; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 48; `iGridX` 2; `iGridY` 12; `iPower` 4 |
| TRADE | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_POTTERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_ANIMAL_HUSBANDRY","TECH_SAILING"]; `Quote` TXT_KEY_TECH_TRADE_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bOpenBordersTrading` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 85; `iGridX` 3; `iGridY` 3; `iTradeRoutes` 1 |
| WATERWORKS | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_CITY_PLANNING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `OrPreReqs` ["TECH_CONSTRUCTION"]; `Quote` TXT_KEY_TECH_WATERWORKS_QUOTE; `Sound` AS2D_TECH_GENERIC; `bIrrigation` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 24; `iCost` 1000; `iGridX` 7; `iGridY` 5 |
| WRITING | `Advisor` ADVISOR_SCIENCE; `AndPreReqs` ["TECH_PRIESTHOOD","TECH_TRADE"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10},{"FlavorType":"FLAVOR_CULTURE","iFlavor":6}]; `Quote` TXT_KEY_TECH_WRITING_QUOTE; `Sound` AS2D_TECH_WRITING; `SoundMP` AS2D_TECH_MP_WRITING; `bGoodyTech` True; `bTechTrading` True; `bTrade` True; `iAITradeModifier` 10; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 96; `iGridX` 4; `iGridY` 5 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| CELTIC_WARBAND | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_CELTIC_WARBAND; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_RELIGION_CELTIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_CELTIC_SWORDSMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SCHILDTRAEGER_CELTIC","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 6; `iCombatLimit` 100; `iConscription` 3; `iCost` 40; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| GALLEY | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_GALLEY; `Combat` UNITCOMBAT_WOODEN_SHIPS; `DefaultUnitAI` UNITAI_ASSAULT_SEA; `Domain` DOMAIN_SEA; `DomainCargo` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_SAILING; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `UnitAIs` [{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SETTLER_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_MISSIONARY_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SPY_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_GALLEON","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_FLUYT","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_COG","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_GALLEY","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCargo` 4; `iCombat` 3; `iCombatLimit` 100; `iCost` 25; `iMinAreaSize` 20; `iMoves` 4; `iNukeRange` -1; `iPower` 4; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| GALLEY | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_GALLEY; `Combat` UNITCOMBAT_WOODEN_SHIPS; `DefaultUnitAI` UNITAI_ASSAULT_SEA; `Domain` DOMAIN_SEA; `DomainCargo` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_SAILING; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `UnitAIs` [{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SETTLER_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_MISSIONARY_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SPY_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_GALLEON","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_FLUYT","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_COG","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_GALLEY","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCargo` 4; `iCombat` 3; `iCombatLimit` 100; `iCost` 25; `iMinAreaSize` 20; `iMoves` 4; `iNukeRange` -1; `iPower` 4; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| GREEK_PHALANX | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_AXEMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqTech` TECH_BRONZE_WORKING; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_MACEMAN","bUnitClassUpgrade":true}]; `UnitCombatCollateralImmunes` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatCollateralImmune":1}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":50},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_GREEK_PHALANX","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 7; `iCombatLimit` 100; `iConscription` 4; `iCost` 60; `iCultureGarrison` 4; `iHillsDefense` 25; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 8; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| HYPASPIST2 | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_HYPASPIST2; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_GREEK"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SWORDSMAN","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_MACEMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_HYPASPIST_2","iRequired":1}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":7,"iMeleeWaveSize":4,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 4; `iCityAttack` 10; `iCombat` 9; `iCombatLimit` 100; `iConscription` 2; `iCost` 75; `iCultureGarrison` 5; `iExtraCost` 2; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 20; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| JAVELINEER | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":10},{"BonusType":"BONUS_OBSIDIAN","iProductonModifier":10}]; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_CAMP","bBuild":true}]; `Class` UNITCLASS_JAVELINEER; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true}]; `PrereqTech` TECH_HUNTING; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SPEARMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELINEER","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 3; `iCombatLimit` 100; `iConscription` 2; `iCost` 25; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 4; `iWithdrawalProb` 25; `iWorkRate` 100; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| SARISSA | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_SARISSA; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_GREEK"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatCollateralImmunes` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatCollateralImmune":1}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":100},{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SARISSA_MACEDON_2","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCityDefense` 25; `iCombat` 7; `iCombatLimit` 100; `iConscription` 5; `iCost` 40; `iCultureGarrison` 6; `iHillsDefense` 25; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 12; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| TRIREME | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_TRIREME; `Combat` UNITCOMBAT_WOODEN_SHIPS; `DefaultUnitAI` UNITAI_ATTACK_SEA; `Domain` DOMAIN_SEA; `DomainCargo` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_SHIP_BUILDING; `TechTypes` ["TECH_NAVAL_WARFARE"]; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ESCORT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_EXPLORE_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_CARAVEL","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_SLOOP","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_COG","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_TRIREME","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCargo` 2; `iCombat` 6; `iCombatLimit` 100; `iCost` 50; `iMinAreaSize` 20; `iMoves` 4; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| WARLORDI | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_GOLD","iProductonModifier":10},{"BonusType":"BONUS_SILVER","iProductonModifier":10},{"BonusType":"BONUS_GEMS","iProductonModifier":10},{"BonusType":"BONUS_PEARLS","iProductonModifier":10}]; `Builds` [{"BuildType":"BUILD_FORT","bBuild":true}]; `Capture` UNITCLASS_WARLORDIS; `Class` UNITCLASS_WARLORDI; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_GENERAL; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_LEADER","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqTech` TECH_MILITARY_TRAINING; `UnitAIs` [{"UnitAIType":"UNITAI_GENERAL","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_WARLORDII","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_VWARLORD_ANCIENT","iRequired":1},{"EarlyArtDefineTag":"ART_DEF_UNIT_SPEARMAN_BARBARIAN","iRequired":2},{"EarlyArtDefineTag":"ART_DEF_UNIT_AXEMAN_BARBARIAN","iRequired":2}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":5,"iMeleeWaveSize":5,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bNoCapture` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCollateralDamage` 10; `iCollateralDamageLimit` 10; `iCollateralDamageMaxUnits` 1; `iCombat` 10; `iCombatLimit` 100; `iCost` 100; `iCultureGarrison` 12; `iExtraCost` 1; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 5; `iWorkRate` 100; `iXPValueAttack` 4; `iXPValueDefense` 2 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| WARBAND | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_WARBAND; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_RELIGION_NORDIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WARBAND_GERMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 6; `iCombatLimit` 100; `iConscription` 3; `iCost` 45; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| AUXILIAR | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_AUXILIAR; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_AUXILIAR","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 8; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 13; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| CENTURIO | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_CENTURIO; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true},{"PromotionType":"PROMOTION_LEADER","bFreePromotion":true},{"PromotionType":"PROMOTION_LEADERSHIP","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_SENATE; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_CENTURIO","iRequired":1},{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_LEGIONARY","iRequired":7}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":8,"iMeleeWaveSize":4,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCombat` 15; `iCombatLimit` 100; `iCost` 150; `iCultureGarrison` 5; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 30; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| HASTATI | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_AXEMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_LIGHT_SWORDSMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_HASTATI","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 7; `iCombatLimit` 100; `iConscription` 8; `iCost` 50; `iCultureGarrison` 4; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 10; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| PRINCIPES | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_LIGHT_SWORDSMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_ROME_LEGIONARY","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_PRINCIPES","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 8; `iCombatLimit` 100; `iCost` 50; `iCultureGarrison` 6; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 16; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| QUINQUEREME | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_QUINQUEREME; `Combat` UNITCOMBAT_WOODEN_SHIPS; `DefaultUnitAI` UNITAI_ATTACK_SEA; `Domain` DOMAIN_SEA; `DomainCargo` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_SHIP_BUILDING; `TechTypes` ["TECH_ROMAN","TECH_SIEGE_WARFARE","NONE"]; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_ESCORT_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SLOOP","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_BRIGANTINE","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_QUINQUEREME","iRequired":3}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAirCombat` 1; `iAirCombatLimit` 50; `iAirRange` 1; `iAsset` 1; `iBombardRate` 10; `iCargo` 4; `iCombat` 8; `iCombatLimit` 100; `iCost` 60; `iMinAreaSize` 20; `iMoves` 4; `iNukeRange` -1; `iPower` 16; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| ROME_LEGIONARY | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_ROME_LEGIONARY; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK_CITY; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_COMITATENSES","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_LEGIONARY","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 4; `iCombat` 10; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 5; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 24; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `ph.game1_phases` | table, 5 values | orders | human | turns 0-217 | 218 | phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game1; means of the raw series per turn |
| `ph.game2_phases` | table, 4 values | orders | human | turns 0-235 | 236 | phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game2; means of the raw series per turn |
| `ph.game3_phases` | table, 4 values | orders | human | turns 0-265 | 266 | phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game3; means of the raw series per turn |
| `ph.game4_phases` | table, 4 values | orders | human | turns 0-284 | 285 | phases.py: exact optimal partition (segments of at least 10 turns, penalty p ln n per segment, p = 7 series: build, move, train, construct, found, attack, war) of the war log of game4; means of the raw series per turn |
| `ph.game1_phase_beta` | table, 3 values | turn | human | turns 0-217 | 218 | phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled |
| `ph.game2_phase_beta` | table, 3 values | turn | human | turns 0-235 | 236 | phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled |
| `ph.game3_phase_beta` | table, 3 values | turn | human | turns 0-265 | 266 | phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled |
| `ph.game4_phase_beta` | table, 3 values | turn | human | turns 0-284 | 285 | phases.py: the turns where a phase starts, with the penalty halved, as set, and doubled |
| `st.game3_civic_tech_lag` | table, 15 values | turns | human | each civic adopted after the start | 15 | civics in each CIVICS command of the human not in its previous one (A lines), the tech each requires (CivicInfo TechPrereq) and the turn the human got it (X lines; turn 0: held from the start), and the AIs holding that civic at the save [game3] |
| `st.game4_civic_tech_lag` | table, 13 values | turns | human | each civic adopted after the start | 13 | civics in each CIVICS command of the human not in its previous one (A lines), the tech each requires (CivicInfo TechPrereq) and the turn the human got it (X lines; turn 0: held from the start), and the AIs holding that civic at the save [game4] |
| `st.game3_tech_lead` | table, 27 values | turn | every player | acquisition turns | 27 | X lines (the first of each player and tech; turn 0 is the start); source: a deal item giving the human that tech on the same turn (deal_items, TRADE_TECHNOLOGIES; the tech index of TechInfo, checked: every such item has the receiver's X line on its turn) [game3] |
| `st.game4_tech_lead` | table, 35 values | turn | every player | acquisition turns | 35 | X lines (the first of each player and tech; turn 0 is the start); source: a deal item giving the human that tech on the same turn (deal_items, TRADE_TECHNOLOGIES; the tech index of TechInfo, checked: every such item has the receiver's X line on its turn) [game4] |
| `st.game3_expansion` | table, 8 values | turn | every player | founding turns | 8 | the turn of each player's k-th city founded: the human's from its FOUND commands (A lines), the AIs' from the founding turn of the save's cities, credited to the first owner (the old owner of the first K or Z line on the plot); AI cities razed before the save are not in the save and are missing [game3] |
| `st.game4_expansion` | table, 8 values | turn | every player | founding turns | 8 | the turn of each player's k-th city founded: the human's from its FOUND commands (A lines), the AIs' from the founding turn of the save's cities, credited to the first owner (the old owner of the first K or Z line on the plot); AI cities razed before the save are not in the save and are missing [game4] |
| `st.game3_city_spacing` | table, 2 values | cities | every player | founding turns | 2 | every city after a player's first: grid distance (map wrap ignored) to the nearest city the same player founded before it, as in the expansion table [game3] |
| `st.game4_city_spacing` | table, 2 values | cities | every player | founding turns | 2 | every city after a player's first: grid distance (map wrap ignored) to the nearest city the same player founded before it, as in the expansion table [game4] |
| `tg.game3_war_targets` | table, 2 values | rank | human | each declaration of the human (cues from the turn before) | 2 | strategy.py: W lines of game3; options: AIs with an M line the turn before, holding a city, not at war with the human, not unmet at the save; rank 1 = the least power, the least distance, the most cities |
| `tg.game4_war_targets` | table, 8 values | rank | human | each declaration of the human (cues from the turn before) | 8 | strategy.py: W lines of game4; options: AIs with an M line the turn before, holding a city, not at war with the human, not unmet at the save; rank 1 = the least power, the least distance, the most cities |
| `tg.war_target_strategies_pooled` | table, 7 values | category | human | each declaration of the human | 10 | strategy.py: maximum-likelihood classification over the declarations of every game given |
| `tg.game3_war_target_strategies` | table, 7 values | category | human | each declaration of the human | 2 | strategy.py: maximum-likelihood classification over the declarations of game3 |
| `tg.game4_war_target_strategies` | table, 7 values | category | human | each declaration of the human | 8 | strategy.py: maximum-likelihood classification over the declarations of game4 |
| `st.game1_war_preparation` | table, 3 values | orders | human | the ten turns before each declaration, against the fifty before those | 3 | A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game1] |
| `st.game2_war_preparation` | table, 3 values | orders | human | the ten turns before each declaration, against the fifty before those | 3 | A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game2] |
| `st.game3_war_preparation` | table, 2 values | orders | human | the ten turns before each declaration, against the fifty before those | 2 | A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game3] |
| `st.game4_war_preparation` | table, 8 values | orders | human | the ten turns before each declaration, against the fifty before those | 8 | A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those [game4] |
| `st.game1_attack_units` | table, 2 values | battles | human | whole game | 2 | C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game1] |
| `st.game2_attack_units` | table, 7 values | battles | human | whole game | 7 | C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game2] |
| `st.game3_attack_units` | table, 1 values | battles | human | whole game | 1 | C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game3] |
| `st.game4_attack_units` | table, 6 values | battles | human | whole game | 6 | C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus [game4] |
| `st.game3_peace_terms` | table, 2 values | gold | human and the AI it made peace with | each peace | 2 | Q lines of the human and the deal between the same two players on that turn (deal_items: TRADE_GOLD 0, TRADE_GOLD_PER_TURN 1, TRADE_TECHNOLOGIES 9, TRADE_CITIES 11; the peace treaty items, 8, left out) [game3] |
| `st.game4_peace_terms` | table, 5 values | gold | human and the AI it made peace with | each peace | 5 | Q lines of the human and the deal between the same two players on that turn (deal_items: TRADE_GOLD 0, TRADE_GOLD_PER_TURN 1, TRADE_TECHNOLOGIES 9, TRADE_CITIES 11; the peace treaty items, 8, left out) [game4] |
