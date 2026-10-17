<!-- Rendered by tools/docs.py from winning.md.in. Do not edit; edit the template. -->
# Why the human wins: the four logged games

Method: `framework.md`. The queries are declared in `study/queries_win.json` and turned into
figures by `tools/sqlfig.py`. Each table states what it counts, who, when, and from which
source. Facts come first, readings in section 7. The decision rules behind the human's play are
in `study/human.md`, and the tiles, trade and combat data in `study/data.md`.

## 1. Questions

- **Q1.** When does the human's lead open, and in what: cities, commerce, research or power?
  Source: M lines (game 3 and game 4; game 1 and game 2 have none) and K lines.
- **Q2.** What raises the human's commerce: new cities, population, civics, techs or golden ages?
  Source: M lines, CIVICS commands, X and K lines. The size of each civic's effect comes from the
  probe in the save dump, which swaps one civic and recalculates (`toolchain/analysis/dump.sh`).
- **Q3.** Do the AIs take the same civics and techs, and if not, what does their code value
  instead? Source: the save dump (civics, techs, the AI's tech values) and `CvPlayerAI.cpp`.
- **Q4.** How do the human's wars go, and what do the AIs do in them? Source: W, Q, C, R, K and
  G lines.

## 2. The whole game

Cities, commerce, research and power at every fiftieth turn and at the last full turn, human
against the AI median:

| turn | human_cities | ai_cities | human_commerce | ai_commerce | human_research | ai_research | human_power | ai_power | human_score_rank | human_power_rank | players |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 1.0 | 16 | 16.0 | 10 | 10.0 | 4 | 4.0 | 1 | 5 | 18 |
| 50 | 1 | 1.0 | 21 | 21.0 | 15 | 15.0 | 11 | 7.0 | 7 | 1 | 18 |
| 100 | 1 | 1.0 | 28 | 24.0 | 22 | 17.0 | 34 | 17.0 | 2 | 1 | 18 |
| 150 | 4 | 3.0 | 55 | 38.0 | 43 | 29.0 | 59 | 32.0 | 2 | 1 | 18 |
| 200 | 5 | 4.0 | 89 | 48.0 | 70 | 36.0 | 128 | 70.0 | 3 | 1 | 18 |
| 250 | 13 | 5.0 | 828 | 111.0 | 742 | 101.0 | 483 | 168.0 | 1 | 1 | 18 |
| 265 | 13 | 6.0 | 989 | 122.0 | 886 | 99.0 | 563 | 239.0 | 1 | 1 | 18 |

*cities; who: human and AI; turn: every 50th turn and the last full turn; rows counted: 7; source: M lines (end of each player's turn): the human's value, the median AI's, and the human's rank among all players by score and by power [game3]. Every value counted (7).*

| turn | human_cities | ai_cities | human_commerce | ai_commerce | human_research | ai_research | human_power | ai_power | human_score_rank | human_power_rank | players |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 1.0 | 16 | 16.0 | 10 | 10.0 | 2 | 4.0 | 2 | 14 | 19 |
| 50 | 1 | 1.0 | 21 | 22.5 | 15 | 15.5 | 13 | 8.5 | 5 | 2 | 19 |
| 100 | 3 | 1.5 | 22 | 30.0 | 16 | 21.0 | 25 | 17.5 | 3 | 3 | 19 |
| 150 | 5 | 3.0 | 43 | 44.5 | 31 | 38.0 | 59 | 42.0 | 1 | 1 | 19 |
| 200 | 8 | 5.0 | 146 | 75.5 | 119 | 63.5 | 149 | 86.0 | 1 | 1 | 19 |
| 250 | 11 | 7.0 | 777 | 173.5 | 677 | 145.0 | 441 | 275.0 | 2 | 3 | 19 |
| 284 | 25 | 10.0 | 1724 | 266.0 | 1289 | 195.0 | 1980 | 493.0 | 1 | 1 | 18 |

*cities; who: human and AI; turn: every 50th turn and the last full turn; rows counted: 7; source: M lines (end of each player's turn): the human's value, the median AI's, and the human's rank among all players by score and by power [game4]. Every value counted (7).*

Where the human's cities came from, in all four games:

| period_from | founded | captured | lost | razed |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 |
| 50 | 2 | 0 | 0 | 0 |
| 100 | 1 | 0 | 0 | 0 |
| 150 | 3 | 7 | 0 | 1 |
| 200 | 0 | 3 | 0 | 0 |

*cities; who: human; turn: by 50-turn period; rows counted: 5; source: cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game1]. Every value counted (5).*

| period_from | founded | captured | lost | razed |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 |
| 100 | 2 | 1 | 0 | 0 |
| 150 | 3 | 0 | 0 | 0 |
| 200 | 0 | 9 | 0 | 0 |

*cities; who: human; turn: by 50-turn period; rows counted: 4; source: cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game2]. Every value counted (4).*

| period_from | founded | captured | lost | razed |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 |
| 100 | 3 | 0 | 0 | 0 |
| 150 | 1 | 0 | 0 | 0 |
| 200 | 2 | 6 | 0 | 0 |

*cities; who: human; turn: by 50-turn period; rows counted: 4; source: cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game3]. Every value counted (4).*

| period_from | founded | captured | lost | razed |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 |
| 50 | 1 | 0 | 0 | 0 |
| 100 | 3 | 0 | 0 | 0 |
| 150 | 3 | 0 | 0 | 0 |
| 200 | 1 | 2 | 0 | 2 |
| 250 | 4 | 14 | 0 | 2 |

*cities; who: human; turn: by 50-turn period; rows counted: 6; source: cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game4]. Every value counted (6).*

## 3. Commerce

### 3.1 When it rises

The first turn of each run of turns in which the human's commerce rose by more than a quarter
over three turns:

| turn | commerce_3_turns_before | commerce | golden_age_turns | cities_captured | civics_set | techs |
|---|---|---|---|---|---|---|
| 70 | 18 | 25 | 0 | 0 | - | - |
| 111 | 27 | 34 | 0 | 0 | - | - |
| 195 | 82 | 112 | 0 | 0 | - | - |
| 206 | 87 | 134 | 0 | 3 | - | THE_WHEEL |
| 220 | 166 | 235 | 0 | 0 | OLIGARCHY,ACCOUNTING,TRIBUTE,BARTER,PEASANTRY,TUTORS,SPIRITISM,FORTIFICATION, | - |
| 243 | 348 | 759 | 0 | 0 | OLIGARCHY,ACCOUNTING,FISCUS,COINAGE,PROLETARIAT,TUTORS,SPIRITISM,FORTIFICATION, | - |

*turns; who: human; turn: whole game; rows counted: 6; source: M lines of the human: the first turn of each run of turns where commerce exceeds the M line three turns earlier by more than a quarter (turns after 50; a base of commerce 1, an anarchy turn, is left out), with the cities captured (K lines), the civics adopted (CIVICS commands) and the techs acquired (X lines) in the three turns ending there, and the golden-age turns left [game3]. Every value counted (6).*

| turn | commerce_3_turns_before | commerce | golden_age_turns | cities_captured | civics_set | techs |
|---|---|---|---|---|---|---|
| 62 | 21 | 28 | 0 | 0 | - | MINING |
| 143 | 30 | 38 | 0 | 0 | - | - |
| 173 | 57 | 72 | 0 | 0 | - | - |
| 184 | 70 | 102 | 0 | 0 | - | - |
| 194 | 88 | 111 | 0 | 0 | - | - |
| 199 | 115 | 146 | 0 | 0 | - | RELIGION_GREEK |
| 201 | 119 | 152 | 0 | 0 | - | - |
| 218 | 218 | 280 | 0 | 0 | - | - |
| 224 | 230 | 290 | 0 | 0 | OLIGARCHY,ACCOUNTING,TRIBUTE,COASTAL,PEASANTRY,TUTORS,SPIRITISM,TRIBAL_WARFARE, | - |
| 231 | 276 | 385 | 13 | 0 | OLIGARCHY,ACCOUNTING,TRIBUTE,METALS,PEASANTRY,TUTORS,SPIRITISM,FORTIFICATION, | FERMENTATION |
| 247 | 395 | 748 | 0 | 0 | OLIGARCHY,ACCOUNTING,TRIBUTE,COINAGE,PROLETARIAT,TUTORS,SPIRITISM,FORTIFICATION, | - |
| 260 | 758 | 1035 | 0 | 0 | OLIGARCHY,ACCOUNTING,TRIBUTE,COINAGE,PROLETARIAT,TUTORS,SPIRITISM,FORTIFICATION, | ARCHERY NAVAL_WARFARE |
| 262 | 877 | 1166 | 0 | 0 | - | SHIP_BUILDING |
| 267 | 1031 | 1296 | 0 | 0 | - | - |

*turns; who: human; turn: whole game; rows counted: 14; source: M lines of the human: the first turn of each run of turns where commerce exceeds the M line three turns earlier by more than a quarter (turns after 50; a base of commerce 1, an anarchy turn, is left out), with the cities captured (K lines), the civics adopted (CIVICS commands) and the techs acquired (X lines) in the three turns ending there, and the golden-age turns left [game4]. Every value counted (14).*

Anarchy shows in the M lines as commerce and research of one: `CvCity::isDisorder` is true while
the owner is in anarchy (`CvCity.cpp:4671–4674`), and a city in disorder yields no commerce. These turns
are left out above, and counted here for every player:

| who | players | median_turns_at_commerce_1 | max_turns | all_turns |
|---|---|---|---|---|
| AI | 17 | 8.0 | 17 | 146 |
| human | 1 | 11.0 | 11 | 11 |

*turns; who: every player; turn: turns 51 to the last M line; rows counted: 2; source: wl_M lines with commerce <= 1 (anarchy: CvCity::isDisorder includes the owner's anarchy, CvCity.cpp:4671) [game3]. Every value counted (2).*

| who | players | median_turns_at_commerce_1 | max_turns | all_turns |
|---|---|---|---|---|
| AI | 18 | 10.5 | 14 | 179 |
| human | 1 | 6.0 | 6 | 6 |

*turns; who: every player; turn: turns 51 to the last M line; rows counted: 2; source: wl_M lines with commerce <= 1 (anarchy: CvCity::isDisorder includes the owner's anarchy, CvCity.cpp:4671) [game4]. Every value counted (2).*

### 3.2 Every civic switch of the human

Each turn with a CIVICS command, with the last M line before it and the first after it that is
not an anarchy turn. The first column lists the civics adopted; the first row is the start:

| turn | adopted | before_turn | cities_before | pop_before | commerce_before | golden_before | anarchy_turns | after_turn | cities_after | pop_after | commerce_after | golden_after |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | PATRIARCH ORAL_LAW NO_TAXES PASTORAL PEASANTRY HOMESCHOOLING FOLKLORE TRIBAL_WARFARE | 1 | 1 | 1 | 16 | 0 | 0 | 2 | 1 | 1 | 16 | 0 |
| 32 | OLIGARCHY TRIBUTE | 31 | 1 | 1 | 15 | 0 | 2 | 34 | 1 | 1 | 20 | 0 |
| 66 | TABLETS | 65 | 1 | 3 | 18 | 0 | 1 | 67 | 1 | 3 | 18 | 0 |
| 130 | ELDERS | 129 | 3 | 8 | 31 | 0 | 1 | 131 | 3 | 8 | 38 | 0 |
| 156 | BARTER SPIRITISM | 155 | 4 | 10 | 48 | 0 | 2 | 158 | 4 | 10 | 59 | 0 |
| 197 | STANDARDIZED_TABLETS TUTORS | 196 | 5 | 19 | 83 | 0 | 2 | 199 | 5 | 19 | 89 | 0 |
| 218 | ACCOUNTING FORTIFICATION | 217 | 11 | 45 | 166 | 0 | 1 | 219 | 11 | 45 | 219 | 0 |
| 241 | FISCUS COINAGE PROLETARIAT | 240 | 13 | 76 | 348 | 0 | 2 | 243 | 13 | 76 | 759 | 0 |
| 253 | PATRICIAN | 252 | 13 | 88 | 780 | 0 | 1 | 254 | 13 | 88 | 902 | 0 |
| 261 | BOOKKEEPING | 260 | 13 | 99 | 977 | 0 | 1 | 262 | 13 | 99 | 1106 | 0 |

*turns; who: human; turn: each turn with a CIVICS command; rows counted: 10; source: every turn with a CIVICS command of the human (A lines; adopted: the civics of its last command that turn not in the previous one), with its last M line before that turn and its first M line from that turn on that are not anarchy turns (commerce 1), and the anarchy turns between; the M line is written at the end of the turn, after its commands [game3]. Every value counted (10).*

| turn | adopted | before_turn | cities_before | pop_before | commerce_before | golden_before | anarchy_turns | after_turn | cities_after | pop_after | commerce_after | golden_after |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | PATRIARCH ORAL_LAW NO_TAXES COASTAL PEASANTRY HOMESCHOOLING FOLKLORE TRIBAL_WARFARE | 1 | 1 | 1 | 16 | 0 | 0 | 2 | 1 | 1 | 16 | 0 |
| 35 | OLIGARCHY TRIBUTE | 34 | 1 | 2 | 18 | 0 | 2 | 37 | 1 | 2 | 21 | 0 |
| 88 | TABLETS | 87 | 2 | 6 | 21 | 0 | 1 | 89 | 2 | 6 | 23 | 0 |
| 138 | SPIRITISM | 137 | 4 | 15 | 26 | 0 | 1 | 139 | 5 | 16 | 32 | 0 |
| 146 | ELDERS | 145 | 5 | 17 | 37 | 0 | 1 | 147 | 5 | 17 | 43 | 0 |
| 205 | STANDARDIZED_TABLETS TUTORS | 204 | 9 | 44 | 153 | 0 | 2 | 207 | 10 | 45 | 164 | 0 |
| 222 | ACCOUNTING | 221 | 10 | 53 | 230 | 0 | 0 | 222 | 10 | 53 | 285 | 0 |
| 229 | METALS FORTIFICATION | 228 | 10 | 60 | 276 | 0 | 0 | 229 | 10 | 60 | 399 | 15 |
| 234 | (no change) | 233 | 10 | 66 | 519 | 11 | 0 | 234 | 10 | 67 | 529 | 10 |
| 245 | COINAGE PROLETARIAT | 244 | 10 | 78 | 395 | 0 | 1 | 246 | 10 | 78 | 723 | 0 |
| 258 | (no change) | 257 | 14 | 98 | 758 | 0 | 0 | 258 | 14 | 98 | 857 | 0 |
| 268 | FISCUS | 267 | 14 | 120 | 1296 | 0 | 0 | 268 | 15 | 121 | 1369 | 0 |

*turns; who: human; turn: each turn with a CIVICS command; rows counted: 12; source: every turn with a CIVICS command of the human (A lines; adopted: the civics of its last command that turn not in the previous one), with its last M line before that turn and its first M line from that turn on that are not anarchy turns (commerce 1), and the anarchy turns between; the M line is written at the end of the turn, after its commands [game4]. Every value counted (12).*

### 3.3 What each civic is worth at the save

The probe sets one civic of the human's to an alternative, recalculates the empire, records the
totals and restores the original. The table gives the change against the human's actual civics
(negative: the alternative is worse). It is static: the tiles worked and the buildings stay as
they are.

| option | current | alternative | d_commerce | d_research | d_gold | d_food | d_hammers |
|---|---|---|---|---|---|---|---|
| ADMINISTRATION | BOOKKEEPING | TABLETS | -84 | -55 | -23 | -46 | -36 |
| ADMINISTRATION | BOOKKEEPING | ORAL_LAW | -77 | -55 | -16 | -110 | -93 |
| ADMINISTRATION | BOOKKEEPING | STANDARDIZED_TABLETS | -22 | 0 | -16 | 0 | 0 |
| ADMINISTRATION | BOOKKEEPING | ACCOUNTING | -12 | 0 | -6 | 0 | 0 |
| ECONOMY | COINAGE | HUNTER_GATHERER | -304 | -288 | -16 | -60 | -35 |
| ECONOMY | COINAGE | COASTAL | -229 | -219 | -10 | -60 | -31 |
| ECONOMY | COINAGE | PASTORAL | -223 | -210 | -13 | -53 | -35 |
| ECONOMY | COINAGE | BARTER | -204 | -192 | -12 | -25 | -35 |
| ECONOMY | COINAGE | AGRICULTURAL | -186 | -176 | -10 | -60 | -35 |
| ECONOMY | COINAGE | METALS | -162 | -151 | -11 | -25 | -35 |
| EDUCATION | TUTORS | HOMESCHOOLING | -60 | -55 | -5 | -46 | -36 |
| EDUCATION | TUTORS | ELDERS | 0 | 0 | 0 | -46 | -36 |
| EMPLOYMENT | PROLETARIAT | PEASANTRY | -126 | -119 | -7 | 48 | -101 |
| EMPLOYMENT | PROLETARIAT | ABORIGINAL | -7 | -10 | 3 | -31 | -241 |
| EMPLOYMENT | PROLETARIAT | SLAVERY | -1 | -5 | 4 | 0 | -168 |
| LEADERSHIP | PATRICIAN | IMPERIUM | -129 | -106 | -23 | 0 | 0 |
| LEADERSHIP | PATRICIAN | PATRIARCH | -127 | -106 | -21 | 0 | 0 |
| LEADERSHIP | PATRICIAN | HEREDITARY_RULE | -116 | -106 | -10 | 0 | 0 |
| LEADERSHIP | PATRICIAN | OLIGARCHY | -116 | -106 | -10 | 0 | 0 |
| LEADERSHIP | PATRICIAN | PRIESTHOOD | -75 | -60 | -19 | 0 | 0 |
| MILITARY | FORTIFICATION | MERCENARIES | -16 | 0 | -16 | 0 | 0 |
| MILITARY | FORTIFICATION | STANDING_ARMY | -13 | 0 | -13 | 0 | 0 |
| MILITARY | FORTIFICATION | TRIBAL_WARFARE | 4 | 0 | 4 | 0 | 0 |
| MILITARY | FORTIFICATION | RAIDERS | 10 | 0 | 10 | 0 | 0 |
| RELIGION | SPIRITISM | STATE_RELIGION | -14 | 0 | -8 | 0 | 0 |
| RELIGION | SPIRITISM | FOLKLORE | -6 | 0 | 0 | 0 | 0 |
| TAXATION | FISCUS | TRIBUTE | -27 | 0 | -23 | -35 | 9 |
| TAXATION | FISCUS | CENSUS | -12 | 0 | -8 | 0 | 0 |
| TAXATION | FISCUS | NO_TAXES | 88 | 97 | -3 | 0 | 0 |

*derived xml; who: human; turn: save; rows counted: 29; source: probe (HH_probe, CvPlayer::setCivics then a full recalculation, worked tiles unchanged; every swap restored the baseline): the human's totals with each civic it could adopt in place of its current one, minus its actual totals. Negative: the current civic is worth that much [game3]. Every value counted (29).*

| option | current | alternative | d_commerce | d_research | d_gold | d_food | d_hammers |
|---|---|---|---|---|---|---|---|
| ADMINISTRATION | ACCOUNTING | TABLETS | -171 | -90 | -81 | -78 | -72 |
| ADMINISTRATION | ACCOUNTING | ORAL_LAW | -153 | -90 | -63 | -191 | -193 |
| ADMINISTRATION | ACCOUNTING | STANDARDIZED_TABLETS | -51 | 0 | -51 | 0 | 0 |
| ECONOMY | COINAGE | HUNTER_GATHERER | -716 | -571 | -145 | -178 | -58 |
| ECONOMY | COINAGE | PASTORAL | -493 | -395 | -98 | -170 | -58 |
| ECONOMY | COINAGE | COASTAL | -459 | -376 | -83 | -178 | -27 |
| ECONOMY | COINAGE | BARTER | -448 | -361 | -87 | -61 | -58 |
| ECONOMY | COINAGE | AGRICULTURAL | -439 | -354 | -85 | -178 | -58 |
| ECONOMY | COINAGE | METALS | -307 | -237 | -70 | -61 | -58 |
| EDUCATION | TUTORS | HOMESCHOOLING | -119 | -90 | -29 | -78 | -72 |
| EDUCATION | TUTORS | ELDERS | 0 | 0 | 0 | -78 | -72 |
| EMPLOYMENT | PROLETARIAT | PEASANTRY | -87 | -73 | -14 | 0 | -481 |
| EMPLOYMENT | PROLETARIAT | ABORIGINAL | -30 | -29 | -1 | -42 | -546 |
| EMPLOYMENT | PROLETARIAT | SLAVERY | 22 | -15 | 37 | -1 | -433 |
| LEADERSHIP | OLIGARCHY | IMPERIUM | -35 | 0 | -35 | 0 | 0 |
| LEADERSHIP | OLIGARCHY | PATRIARCH | -29 | 0 | -29 | 0 | 0 |
| LEADERSHIP | OLIGARCHY | HEREDITARY_RULE | -4 | 0 | -4 | 0 | 0 |
| LEADERSHIP | OLIGARCHY | PRIESTHOOD | 46 | 60 | -26 | 0 | 0 |
| LEADERSHIP | OLIGARCHY | PATRICIAN | 309 | 233 | 76 | 0 | 0 |
| MILITARY | FORTIFICATION | MERCENARIES | -61 | 0 | -61 | 0 | 0 |
| MILITARY | FORTIFICATION | STANDING_ARMY | -39 | 0 | -39 | 0 | 0 |
| MILITARY | FORTIFICATION | TRIBAL_WARFARE | 9 | 0 | 9 | 0 | 0 |
| MILITARY | FORTIFICATION | RAIDERS | 35 | 0 | 35 | 0 | 0 |
| RELIGION | SPIRITISM | FANATICISM | -323 | -265 | -47 | 0 | 0 |
| RELIGION | SPIRITISM | FOLKLORE | -8 | 0 | 0 | 0 | 0 |
| TAXATION | FISCUS | TRIBUTE | -119 | 0 | -114 | -59 | 24 |
| TAXATION | FISCUS | CENSUS | -56 | 0 | -49 | 0 | 0 |
| TAXATION | FISCUS | NO_TAXES | 147 | 193 | -35 | 0 | 0 |

*derived xml; who: human; turn: save; rows counted: 28; source: probe (HH_probe, CvPlayer::setCivics then a full recalculation, worked tiles unchanged; every swap restored the baseline): the human's totals with each civic it could adopt in place of its current one, minus its actual totals. Negative: the current civic is worth that much [game4]. Every value counted (28).*

## 4. What the AIs adopt and research

Civics held at the save:

| civic | human | ais |
|---|---|---|
| CIVIC_TUTORS | 1 | 17 |
| CIVIC_SPIRITISM | 1 | 16 |
| CIVIC_STANDARDIZED_TABLETS | 0 | 12 |
| CIVIC_FORTIFICATION | 1 | 11 |
| CIVIC_NO_TAXES | 0 | 11 |
| CIVIC_PRIESTHOOD | 0 | 11 |
| CIVIC_SLAVERY | 0 | 11 |
| CIVIC_COASTAL | 0 | 9 |
| CIVIC_PASTORAL | 0 | 7 |
| CIVIC_PEASANTRY | 0 | 6 |
| CIVIC_ACCOUNTING | 0 | 5 |
| CIVIC_CENSUS | 0 | 5 |
| CIVIC_HEREDITARY_RULE | 0 | 4 |
| CIVIC_MERCENARIES | 0 | 3 |
| CIVIC_TRIBAL_WARFARE | 0 | 2 |
| CIVIC_AGRICULTURAL | 0 | 1 |
| CIVIC_ASSEMBLY | 0 | 1 |
| CIVIC_DIVINE_RULE | 0 | 1 |
| CIVIC_IMPERIUM | 0 | 1 |
| CIVIC_MILITIA | 0 | 1 |
| CIVIC_TRIBUTE | 0 | 1 |
| CIVIC_BOOKKEEPING | 1 | 0 |
| CIVIC_COINAGE | 1 | 0 |
| CIVIC_FISCUS | 1 | 0 |
| CIVIC_PATRICIAN | 1 | 0 |
| CIVIC_PROLETARIAT | 1 | 0 |

*category; who: all players; turn: save; rows counted: 26; source: civics at the save (dump): how many players run each civic, the human and the AIs [game3]. Every value counted (26).*

| civic | human | ais |
|---|---|---|
| CIVIC_TUTORS | 1 | 17 |
| CIVIC_FORTIFICATION | 1 | 16 |
| CIVIC_SLAVERY | 0 | 15 |
| CIVIC_SPIRITISM | 1 | 14 |
| CIVIC_ACCOUNTING | 1 | 11 |
| CIVIC_CENSUS | 0 | 11 |
| CIVIC_COASTAL | 0 | 11 |
| CIVIC_PRIESTHOOD | 0 | 9 |
| CIVIC_NO_TAXES | 0 | 6 |
| CIVIC_PASTORAL | 0 | 6 |
| CIVIC_STANDARDIZED_TABLETS | 0 | 6 |
| CIVIC_HEREDITARY_RULE | 0 | 5 |
| CIVIC_IMPERIUM | 0 | 3 |
| CIVIC_PEASANTRY | 0 | 2 |
| CIVIC_DIVINE_RULE | 0 | 1 |
| CIVIC_FANATICISM | 0 | 1 |
| CIVIC_RAIDERS | 0 | 1 |
| CIVIC_SACRIFICE_CULT | 0 | 1 |
| CIVIC_COINAGE | 1 | 0 |
| CIVIC_FISCUS | 1 | 0 |
| CIVIC_OLIGARCHY | 1 | 0 |
| CIVIC_PROLETARIAT | 1 | 0 |

*category; who: all players; turn: save; rows counted: 22; source: civics at the save (dump): how many players run each civic, the human and the AIs [game4]. Every value counted (22).*

The techs that unlock them (the `TechPrereq` of each civic, in the appendix), held at the save:

| tech | human | ais |
|---|---|---|
| TECH_CODE_OF_LAWS | 1 | 1 |
| TECH_CURRENCY | 1 | 0 |
| TECH_MATHEMATICS | 1 | 12 |
| TECH_METAL_CASTING | 1 | 17 |
| TECH_TRADE | 1 | 17 |

*techs; who: all players; turn: save; rows counted: 5; source: techs at the save (dump), for the techs that enable the economy and taxation civics in play (TechPrereq of COINAGE, FISCUS, BARTER, METALS, ACCOUNTING, PATRICIAN): players holding each [game3]. Every value counted (5).*

| tech | human | ais |
|---|---|---|
| TECH_CODE_OF_LAWS | 1 | 6 |
| TECH_CURRENCY | 1 | 1 |
| TECH_MATHEMATICS | 1 | 16 |
| TECH_METAL_CASTING | 1 | 17 |
| TECH_TRADE | 1 | 17 |

*techs; who: all players; turn: save; rows counted: 5; source: techs at the save (dump), for the techs that enable the economy and taxation civics in play (TechPrereq of COINAGE, FISCUS, BARTER, METALS, ACCOUNTING, PATRICIAN): players holding each [game4]. Every value counted (5).*

Currency in each AI's research ranking at the save: the AI's own `AI_techValue` of every tech it
can research now, computed by the probe:

| player | currency_rank | researchable | currency_value | top_tech | top_value | researching |
|---|---|---|---|---|---|---|
| 0 | 11 | 19 | 71774 | MONOTHEISM | 321175 | SEAFARING |
| 1 | 9 | 21 | 70572 | IRON_WORKING | 621510 | IRON_WORKING |
| 2 | 13 | 18 | 766 | RELIGION_GREEK | 24202 | RELIGION_GREEK |
| 3 | 10 | 20 | 97449 | IRON_WORKING | 537272 | IRON_WORKING |
| 6 | 9 | 17 | 65188 | SEAFARING | 235772 | BRONZE_WORKING |
| 9 | 13 | 18 | 48242 | SEAFARING | 211446 | BRONZE_WORKING |
| 10 | 8 | 17 | 118076 | MONOTHEISM | 277422 | LITERATURE |
| 11 | 11 | 19 | 110360 | CITY_PLANNING | 304957 | MONOTHEISM |
| 13 | 6 | 20 | 121448 | CITY_PLANNING | 214925 | MACHINERY |
| 15 | 13 | 19 | 14805 | CHARIOTRY | 178857 | BRONZE_WORKING |
| 16 | 13 | 17 | 30951 | BRONZE_WORKING | 181559 | MONARCHY |
| 17 | 15 | 21 | 41488 | IRON_WORKING | 612503 | IRON_WORKING |

*rank; who: AI players; turn: save; rows counted: 12; source: probe: every AI's AI_techValue (path 1) of each tech it can research at the save; the rank of CURRENCY among them, its value, the top tech and its value, and what the AI researches [game3]. Every value counted (12).*

| player | currency_rank | researchable | currency_value | top_tech | top_value | researching |
|---|---|---|---|---|---|---|
| 0 | 5 | 19 | 102850 | DEMOCRACY | 191662 | CONSTRUCTION |
| 1 | 5 | 16 | 46839 | BRONZE_WORKING | 120138 | MONARCHY |
| 2 | 4 | 18 | 87809 | CONSTRUCTION | 169974 | CONSTRUCTION |
| 4 | 11 | 22 | 84837 | SIEGE_WARFARE | 305102 | SIEGE_WARFARE |
| 5 | 9 | 21 | 124556 | CALENDAR | 288020 | CALENDAR |
| 6 | 13 | 20 | 43919 | IRON_WORKING | 516544 | IRON_WORKING |
| 7 | 11 | 19 | 41893 | SIEGE_WARFARE | 291695 | SIEGE_WARFARE |
| 8 | 9 | 18 | 56757 | SIEGE_WARFARE | 200170 | - |
| 9 | 2 | 18 | 139212 | SEAFARING | 226436 | ALPHABET |
| 10 | 8 | 19 | 115595 | CALENDAR | 444173 | CALENDAR |
| 11 | 4 | 15 | 136293 | WATERWORKS | 231014 | WATERWORKS |
| 12 | 9 | 19 | 55116 | SIEGE_WARFARE | 183273 | - |
| 13 | 11 | 20 | 70444 | SIEGE_WARFARE | 267096 | SIEGE_WARFARE |
| 16 | 7 | 18 | 112257 | CODE_OF_LAWS | 179411 | - |
| 18 | 4 | 16 | 133589 | DEMOCRACY | 165927 | DEMOCRACY |

*rank; who: AI players; turn: save; rows counted: 15; source: probe: every AI's AI_techValue (path 1) of each tech it can research at the save; the rank of CURRENCY among them, its value, the top tech and its value, and what the AI researches [game4]. Every value counted (15).*

### 4.1 What the AI code values

In `CvPlayerAI::AI_techValue` (`CvPlayerAI.cpp:5943–5966`, GitLab `main`), each civic a tech
unlocks adds:
- `200`;
- `min(2400, 2400 * (new - current) / current)` of the AI's own civic values, when the new civic
  is valued above the one held;
- `600` when the civic is the leader's favourite.

So a civic that doubles the value of the one held gets the same term as one that is ten times
better. Currency unlocks Coinage, Fiscus and Proletariat (their `TechPrereq`, appendix), and no
leader has one of the three as `FavoriteCivic` in `LeaderHeadInfo`. The total is then divided by
the turns of research left (`CvPlayerAI.cpp:6141–6152`), and a random term is added
(`CvPlayerAI.cpp:5301–5310`). The probe records only the final value, so the share of the civic
term in it is not known (section 8).

An AI that holds the tech switches civics in `CvPlayerAI::AI_doCivics`
(`CvPlayerAI.cpp:16738–16825`): it scores every civic it can adopt, sums the best of each option
against the current set, and switches when `AICivicPolicy::shouldSwitch` accepts the gain against
the anarchy turns.

## 5. Technology

Techs held, and techs traded with the human in deals, by turn:

| turn | human_techs | ai_median_techs | ai_max_techs | human_techs_received_in_deals | human_techs_given_in_deals |
|---|---|---|---|---|---|
| 0 | 4 | 4.0 | 6 | 0 | 0 |
| 50 | 5 | 5.5 | 8 | 0 | 0 |
| 100 | 8 | 8.0 | 10 | 0 | 0 |
| 150 | 11 | 10.0 | 13 | 0 | 0 |
| 200 | 17 | 13.5 | 16 | 2 | 2 |
| 250 | 26 | 17.0 | 22 | 4 | 8 |
| 265 | 31 | 19.5 | 26 | 4 | 13 |

*techs; who: human and AI; turn: every 50th turn and the last; rows counted: 7; source: X lines (techs acquired, cumulative) and deal_items (techs received by the human in deals, cumulative) [game3]. Every value counted (7).*

| turn | human_techs | ai_median_techs | ai_max_techs | human_techs_received_in_deals | human_techs_given_in_deals |
|---|---|---|---|---|---|
| 0 | 5 | 4.0 | 7 | 0 | 0 |
| 50 | 6 | 5.0 | 8 | 0 | 0 |
| 100 | 8 | 8.0 | 13 | 0 | 0 |
| 150 | 10 | 10.0 | 15 | 0 | 0 |
| 200 | 16 | 15.0 | 19 | 2 | 3 |
| 250 | 24 | 18.0 | 24 | 5 | 11 |
| 284 | 39 | 24.0 | 32 | 6 | 21 |

*techs; who: human and AI; turn: every 50th turn and the last; rows counted: 7; source: X lines (techs acquired, cumulative) and deal_items (techs received by the human in deals, cumulative) [game4]. Every value counted (7).*

## 6. Wars

Every war between the human and an AI. The power ratio is the human's power over the
opponent's in the M lines of the turn before the declaration:

| t_start | declared_by | opp | turns | cities_taken | human_attacks | human_wins | ai_attacks | human_units_lost | power_ratio |
|---|---|---|---|---|---|---|---|---|---|
| 186 | human | 7 | 31 | 5 | 18 | 12 | 1 | 7 |  |
| 193 | human | 1 | 24 | 3 | 7 | 6 | 0 | 1 |  |
| 206 | human | 14 | 11 | 2 | 6 | 5 | 0 | 1 |  |

*battles; who: human and AI; turn: each war of the human; rows counted: 3; source: W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game1]. Every value counted (3).*

| t_start | declared_by | opp | turns | cities_taken | human_attacks | human_wins | ai_attacks | human_units_lost | power_ratio |
|---|---|---|---|---|---|---|---|---|---|
| 92 | human | 16 | 143 | 1 | 8 | 4 | 0 | 1 |  |
| 229 | human | 11 | 6 | 5 | 12 | 10 | 0 | 2 |  |
| 230 | human | 9 | 5 | 3 | 6 | 6 | 0 | 0 |  |

*battles; who: human and AI; turn: each war of the human; rows counted: 3; source: W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game2]. Every value counted (3).*

| t_start | declared_by | opp | turns | cities_taken | human_attacks | human_wins | ai_attacks | human_units_lost | power_ratio |
|---|---|---|---|---|---|---|---|---|---|
| 203 | human | 5 | 3 | 5 | 5 | 3 | 0 | 1 | 2.014 |
| 209 | human | 7 | 5 | 1 | 9 | 7 | 0 | 1 | 3.119 |

*battles; who: human and AI; turn: each war of the human; rows counted: 2; source: W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game3]. Every value counted (2).*

| t_start | declared_by | opp | turns | cities_taken | human_attacks | human_wins | ai_attacks | human_units_lost | power_ratio |
|---|---|---|---|---|---|---|---|---|---|
| 238 | human | 14 | 2 | 2 | 2 | 2 | 0 | 0 | 2.6 |
| 252 | human | 2 | 2 | 1 | 2 | 2 | 0 | 0 | 1.24 |
| 257 | human | 6 | 4 | 1 | 3 | 1 | 0 | 1 | 2.127 |
| 268 | human | 7 | 2 | 2 | 3 | 2 | 0 | 1 | 2.151 |
| 271 | human | 14 | 13 | 2 | 20 | 19 | 0 | 0 | 7.503 |
| 272 | human | 10 | 12 | 1 | 2 | 2 | 0 | 0 | 2.782 |
| 277 | human | 2 | 8 | 5 | 36 | 27 | 1 | 5 | 3.434 |
| 283 | human | 7 | 1 | 2 | 9 | 8 | 0 | 1 | 3.934 |

*battles; who: human and AI; turn: each war of the human; rows counted: 8; source: W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game4]. Every value counted (8).*

Every battle the human fought:

| side | battles | enemy_units_killed | human_units_lost | no_death |
|---|---|---|---|---|
| human attacking | 31 | 23 | 8 | 0 |
| human defending | 1 | 0 | 1 | 0 |

*battles; who: human; turn: whole game; rows counted: 2; source: C lines with the R line directly after: units the human's attacks and defences killed and lost [game1]. Every value counted (2).*

| side | battles | enemy_units_killed | human_units_lost | no_death |
|---|---|---|---|---|
| human attacking | 28 | 22 | 3 | 3 |

*battles; who: human; turn: whole game; rows counted: 1; source: C lines with the R line directly after: units the human's attacks and defences killed and lost [game2]. Every value counted (1).*

| side | battles | enemy_units_killed | human_units_lost | no_death |
|---|---|---|---|---|
| human attacking | 14 | 10 | 2 | 2 |

*battles; who: human; turn: whole game; rows counted: 1; source: C lines with the R line directly after: units the human's attacks and defences killed and lost [game3]. Every value counted (1).*

| side | battles | enemy_units_killed | human_units_lost | no_death |
|---|---|---|---|---|
| human attacking | 80 | 66 | 8 | 6 |
| human defending | 1 | 1 | 0 | 0 |

*battles; who: human; turn: whole game; rows counted: 2; source: C lines with the R line directly after: units the human's attacks and defences killed and lost [game4]. Every value counted (2).*

What the AI the human declared on did during the war (G lines are stacks, logged at the start of
each player's turn):

| t_start | opp | target_military_before | target_military_after | target_stacks | target_stacks_near_human_cities |
|---|---|---|---|---|---|
| 203 | 5 | 12 | 8 | 0 | 0 |
| 209 | 7 | 14 | 6 | 0 | 0 |

*units at save; who: AI players; turn: each war the human declared; rows counted: 2; source: M lines: the target's military units the turn before the declaration and at peace (or the last turn); G lines: the target's stacks near or in enemy land during the war, and those standing within 3 plots of a human city the human then owned (cities from MISSION_FOUND and K lines) [game3]. Every value counted (2).*

| t_start | opp | target_military_before | target_military_after | target_stacks | target_stacks_near_human_cities |
|---|---|---|---|---|---|
| 238 | 14 | 20 | 16 | 3 | 0 |
| 252 | 2 | 49 | 47 | 6 | 0 |
| 257 | 6 | 40 | 44 | 0 | 0 |
| 268 | 7 | 62 | 65 | 0 | 0 |
| 271 | 14 | 23 |  | 1 | 0 |
| 272 | 10 | 59 |  | 0 | 0 |
| 277 | 2 | 54 | 31 | 4 | 4 |
| 283 | 7 | 64 |  | 0 | 0 |

*units at save; who: AI players; turn: each war the human declared; rows counted: 8; source: M lines: the target's military units the turn before the declaration and at peace (or the last turn); G lines: the target's stacks near or in enemy land during the war, and those standing within 3 plots of a human city the human then owned (cities from MISSION_FOUND and K lines) [game4]. Every value counted (8).*

## 7. Readings

Each reading names its facts and what would refute it. The economic readings rest on two games,
the war readings on four.

1. **The lead opens late, and commerce grows much faster than cities.**
   - Facts (section 2):
     - in the fourth row of each trajectory, the human's commerce and research are below the AI
       median in game 4 and somewhat above it in game 3; in the fifth, under twice it in both;
     - in the sixth, they are several times the median, while the human's cities are under three
       times the median;
     - the human captures its first city in the period in which the commerce lead opens, in both
       games.
   - Refuted if: a further game where the human's commerce per city stays near the AIs' while
     it conquers.
2. **Coinage, Fiscus and Proletariat roughly double the human's commerce on the same land.**
   - Facts:
     - In game 3, the switch to Fiscus, Coinage and Proletariat leaves cities and population
       unchanged between the two M lines, while commerce more than doubles (section 3.2).
     - In game 4, the switch to Coinage and Proletariat comes right after a golden age ended. The
       commerce after it is above the level before the golden age ended, with the same cities and
       population.
     - At the save, the probe values Coinage over every other economy civic in both games, and
       Proletariat far above Peasantry in hammers in game 4 (section 3.3).
   - Not separated: the golden age in game 4, which began on the turn of the switch to Metals,
     and the probe's fixed tiles. A dynamic counterfactual is open.
   - Refuted if: a replay from the save before the switch, without it, reaching the same
     commerce within a few turns.
3. **The AIs neither research Currency nor run these civics.**
   - Facts:
     - at the save, no AI holds Coinage, Fiscus or Proletariat in either game;
     - in game 3 no AI holds Currency; in game 4 one does, acquired two turns before the last
       M line (X lines);
     - most AIs could research it now, and none ranks it first (section 4).
   - Candidate cause, not tested: the civic term of `AI_techValue` grows with the relative gain
     only up to its cap (section 4.1).
   - Refuted if: the AI's raw tech value, with the civic term at the probe's measured gain, still
     ranks Currency low (section 8).
4. **The human sells technology.**
   - Facts (section 5): after the first trades, it gives more techs in deals than it receives,
     in both games; by the save, several times as many. The gold it receives is in
     `study/data.md`, section 3.
5. **The human fights weaker AIs, and the AIs do not strike back.**
   - Facts (section 6):
     - every war in all four games was declared by the human;
     - wherever power is logged (game 3 and game 4), the human had more power than its opponent
       at the declaration;
     - in all four games, almost every battle is a human attack, and AI attacks on the human are
       zero or one in each war;
     - in game 3 and game 4, AI stacks near the human's cities appear in one war only.
   - Refuted if: a further game where an AI the human attacks takes cities back, or attacks the
     human's units in the field as often as it attacks other AIs.

## 8. Open

- **The civic term's weight.** A harness probe that returns the terms of `AI_techValue` before
  the turn normalisation would show how much of Currency's value comes from its civics, and what
  it would be with the measured gain. That answers reading 3. A change to the term is an AI change
  and is judged by experiment: seeded runs per arm in the number `framework.md` sets, fixed
  opponents, ranks compared.
- **A dynamic civic counterfactual** (reading 2): the same replay from a save with and without the
  switch.
- **Trade against city size and position**, and **combat against unit and terrain**, as in
  `study/data.md`.
- **Game 1 and game 2** have no M lines, so every reading but the fifth rests on two games.

## Appendix: XML records of the types counted

| CivicInfo | Fields set (records.json) |
|---|---|
| CIVIC_ACCOUNTING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [25,0,0]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -30; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CIVIC_AGRICULTURAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[0,0,1]}]; `TechPrereq` TECH_AGRICULTURE; `TradeYieldModifiers` [0,0,-30]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGreatPeopleRateModifier` -25; `iRevEnvironmentalProtection` -5; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxSwitchTo` 20 |
| CIVIC_ASSEMBLY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_AGORA","iHappinessChange":6},{"BuildingType":"BUILDINGCLASS_GUILDHALL","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_COURTHOUSE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_DEMOCRACY; `Upkeep` UPKEEP_MEDIUM; `bCanDoElection` True; `bFreeSpeech` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iCorporationMaintenanceModifier` 25; `iDistanceMaintenanceModifier` 30; `iDomesticGreatGeneralRateModifier` 100; `iGreatGeneralRateModifier` 30; `iGreatPeopleRateModifier` 30; `iImprovementUpgradeRateModifier` 25; `iMilitaryProductionModifier` -10; `iNumCitiesMaintenanceModifier` 25; `iRevDemocracyLevel` 5; `iRevIdxDistanceModifier` 20; `iRevIdxLocal` -1; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iWorkerSpeedModifier` 10 |
| CIVIC_BOOKKEEPING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [30,0,0,25]; `TechPrereq` TECH_LITERATURE; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -50; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CIVIC_CENSUS | `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [25,0,0,10]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| CIVIC_COASTAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FISHING_BOATS","ImprovementYields":[0,1,1]}]; `TechPrereq` TECH_FISHING; `TradeYieldModifiers` [0,0,-30]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` -2; `iRevIdxSwitchTo` 20 |
| CIVIC_COINAGE | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [25,0,0]; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 20; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iTradeRoutes` 1; `iWarWearinessModifier` 25 |
| CIVIC_DIVINE_RULE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_SACRIFICIAL_ALTAR","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_OBELISK","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_GREAT_PALACE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PYRAMID","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MAUSOLEUM_OF_MAUSSOLLOS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_TAJ_MAHAL","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MESOAMERICAN_MAGICIAN_PYRAMID","iHappinessChange":3}]; `CapitalCommerceModifiers` [50,0,25]; `CivicOptionType` CIVICOPTION_RELIGION; `SpecialistValids` [{"SpecialistType":"SPECIALIST_PRIEST","bValid":true}]; `TechPrereq` TECH_CEREMONIAL_BURIAL; `Upkeep` UPKEEP_HIGH; `bAllowInquisitions` True; `bStateReligion` True; `fRevIdxBadReligionMod` .5; `fRevIdxGoodReligionMod` .7; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.3; `iAnarchyLength` 1; `iGreatPeopleRateModifier` -50; `iRevIdxHolyCityBad` 1; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` 2; `iRevIdxNational` -1; `iRevIdxSwitchTo` 50; `iRevReligiousFreedom` -3; `iStateReligionBuildingProductionModifier` 25; `iStateReligionHappiness` 1; `iWarWearinessModifier` -50; `iWorkerSpeedModifier` 25 |
| CIVIC_FISCUS | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_TREASURY","iHappinessChange":-5}]; `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [50,0,0,25]; `Hurrys` [{"HurryType":"HURRY_GOLD","bHurry":true}]; `TechPrereq` TECH_CURRENCY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iLargestCityHappiness` -5; `iNumCitiesMaintenanceModifier` 20; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| CIVIC_FORTIFICATION | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_WALLS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MASONRY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAIWeight` 1; `iAnarchyLength` 1; `iDomesticGreatGeneralRateModifier` 100; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CIVIC_HEREDITARY_RULE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_NOBLE","bValid":true}]; `TechPrereq` TECH_MONARCHY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iRevDemocracyLevel` -5; `iRevIdxLocal` -1; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` -20 |
| CIVIC_IMPERIUM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_COURTHOUSE","iHappinessChange":6},{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iNumCitiesMaintenanceModifier` 25; `iRevIdxDistanceModifier` -50; `iRevIdxLocal` -1; `iRevIdxNational` -8; `iRevIdxSwitchTo` 20; `iWorkerSpeedModifier` 25 |
| CIVIC_MERCENARIES | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_TRADE; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.3; `iAnarchyLength` 1; `iFreeExperience` 5; `iGoldPerMilitaryUnit` 1; `iGoldPerUnit` 1; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` 1; `iRevIdxSwitchTo` 20 |
| CIVIC_MILITIA | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_DEMOCRACY; `Upkeep` UPKEEP_LOW; `bMilitaryFoodProduction` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iFreeUnitsPopulationPercent` 30; `iHappyPerMilitaryUnit` 1; `iRevDemocracyLevel` 5; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |
| CIVIC_NO_TAXES | `CivicOptionType` CIVICOPTION_TAXATION; `TradeYieldModifiers` [0,0,25]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` -1; `iAnarchyLength` 1; `iRevDemocracyLevel` 5; `iRevIdxDistanceModifier` -30; `iRevIdxLocal` -3; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20 |
| CIVIC_PASTORAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_PASTURE","ImprovementYields":[1,0,1]}]; `TechPrereq` TECH_ANIMAL_HUSBANDRY; `TradeYieldModifiers` [0,0,-30]; `Upkeep` UPKEEP_LOW; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` 5; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` -3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| CIVIC_PATRICIAN | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MARKET","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_BANK","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PRAEFECTUR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `TradeYieldModifiers` [0,0,25]; `Upkeep` UPKEEP_LOW; `bCanDoElection` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0.5; `fRevViolentMod` 0; `iAnarchyLength` 1; `iCorporationMaintenanceModifier` -10; `iDistanceMaintenanceModifier` 25; `iGreatGeneralRateModifier` 30; `iRevDemocracyLevel` 1; `iRevEnvironmentalProtection` -2; `iRevIdxDistanceModifier` 20; `iRevIdxLocal` 2; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 100 |
| CIVIC_PEASANTRY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_MANOR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_COTTAGE","ImprovementYields":[1,1,-1]},{"ImprovementType":"IMPROVEMENT_HAMLET","ImprovementYields":[2,2,-1]},{"ImprovementType":"IMPROVEMENT_VILLAGE","ImprovementYields":[2,3,-2]},{"ImprovementType":"IMPROVEMENT_TOWN","ImprovementYields":[2,4,-2]}]; `TechPrereq` TECH_AGRICULTURE; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iImprovementUpgradeRateModifier` 50; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -3; `iRevIdxSwitchTo` 20 |
| CIVIC_PRIESTHOOD | `CapitalCommerceModifiers` [0,25,50,0]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_PRIEST","bValid":true}]; `TechPrereq` TECH_PRIESTHOOD; `Upkeep` UPKEEP_MEDIUM; `bNoNonStateReligionSpread` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 3; `fRevIdxNationalityMod` 0; `fRevViolentMod` -0.5; `iAnarchyLength` 1; `iLargestCityHappiness` 2; `iNumCitiesMaintenanceModifier` 25; `iRevDemocracyLevel` -2; `iRevIdxDistanceModifier` 30; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iRevReligiousFreedom` -3; `iStateReligionBuildingProductionModifier` 25; `iWarWearinessModifier` -20 |
| CIVIC_PROLETARIAT | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_SHAFT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WORKSHOP","ImprovementYields":[1,2,0]},{"ImprovementType":"IMPROVEMENT_LUMBERMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WINDMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WATERMILL","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [0,50,0]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 3; `iWorkerSpeedModifier` 25 |
| CIVIC_SLAVERY | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `CommerceModifiers` [25,0,0]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[2,1,1]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_HIGH; `YieldModifiers` [0,10,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` -5; `iWarWearinessModifier` 50 |
| CIVIC_SPIRITISM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_ORACLE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_STONEHENGE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_RELIGION; `CommerceModifiers` [0,0,0,25]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[0,0,2]}]; `TechPrereq` TECH_MYSTICISM; `bStateReligion` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatPeopleRateModifier` 25; `iRevIdxSwitchTo` -30; `iRevReligiousFreedom` 7; `iStateReligionFreeExperience` 3 |
| CIVIC_STANDARDIZED_TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_WRITING; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -25; `iNumCitiesMaintenanceModifier` 10; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CIVIC_TRIBAL_WARFARE | `CivicOptionType` CIVICOPTION_MILITARY; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| CIVIC_TRIBUTE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CapitalCommerceModifiers` [0,0,25]; `CapitalYieldModifiers` [25,25,25]; `CivicOptionType` CIVICOPTION_TAXATION; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,0,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAIWeight` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iNumCitiesMaintenanceModifier` 10; `iRevDemocracyLevel` -3; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| CIVIC_TUTORS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_WRITING; `YieldModifiers` [10,10,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 30; `iGreatPeopleRateModifier` 30; `iRevIdxDistanceModifier` 25; `iRevIdxLocal` -1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| CivicInfo | Fields set (records.json) |
|---|---|
| CIVIC_ACCOUNTING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [25,0,0]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -30; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CIVIC_CENSUS | `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [25,0,0,10]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| CIVIC_COASTAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FISHING_BOATS","ImprovementYields":[0,1,1]}]; `TechPrereq` TECH_FISHING; `TradeYieldModifiers` [0,0,-30]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` -2; `iRevIdxSwitchTo` 20 |
| CIVIC_COINAGE | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [25,0,0]; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 20; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iTradeRoutes` 1; `iWarWearinessModifier` 25 |
| CIVIC_DIVINE_RULE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_SACRIFICIAL_ALTAR","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_OBELISK","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_GREAT_PALACE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PYRAMID","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MAUSOLEUM_OF_MAUSSOLLOS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_TAJ_MAHAL","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MESOAMERICAN_MAGICIAN_PYRAMID","iHappinessChange":3}]; `CapitalCommerceModifiers` [50,0,25]; `CivicOptionType` CIVICOPTION_RELIGION; `SpecialistValids` [{"SpecialistType":"SPECIALIST_PRIEST","bValid":true}]; `TechPrereq` TECH_CEREMONIAL_BURIAL; `Upkeep` UPKEEP_HIGH; `bAllowInquisitions` True; `bStateReligion` True; `fRevIdxBadReligionMod` .5; `fRevIdxGoodReligionMod` .7; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.3; `iAnarchyLength` 1; `iGreatPeopleRateModifier` -50; `iRevIdxHolyCityBad` 1; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` 2; `iRevIdxNational` -1; `iRevIdxSwitchTo` 50; `iRevReligiousFreedom` -3; `iStateReligionBuildingProductionModifier` 25; `iStateReligionHappiness` 1; `iWarWearinessModifier` -50; `iWorkerSpeedModifier` 25 |
| CIVIC_FANATICISM | `CivicOptionType` CIVICOPTION_RELIGION; `TechPrereq` TECH_MONOTHEISM; `TradeYieldModifiers` [0,0,-25]; `Upkeep` UPKEEP_LOW; `bAllowInquisitions` True; `bNoCorporations` True; `bNoForeignCorporations` True; `bNoNonStateReligionSpread` True; `bStateReligion` True; `bUpgradeAnywhere` True; `fRevIdxBadReligionMod` 1; `fRevIdxGoodReligionMod` 3; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iFreeUnitsPopulationPercent` 30; `iGreatGeneralRateModifier` 30; `iNonStateReligionHappiness` -3; `iRevIdxHolyCityBad` 1; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevReligiousFreedom` -5; `iStateReligionFreeExperience` 5; `iStateReligionHappiness` 6; `iStateReligionUnitProductionModifier` 50; `iWarWearinessModifier` -25 |
| CIVIC_FISCUS | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_TREASURY","iHappinessChange":-5}]; `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [50,0,0,25]; `Hurrys` [{"HurryType":"HURRY_GOLD","bHurry":true}]; `TechPrereq` TECH_CURRENCY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iLargestCityHappiness` -5; `iNumCitiesMaintenanceModifier` 20; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| CIVIC_FORTIFICATION | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_WALLS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MASONRY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAIWeight` 1; `iAnarchyLength` 1; `iDomesticGreatGeneralRateModifier` 100; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CIVIC_HEREDITARY_RULE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_NOBLE","bValid":true}]; `TechPrereq` TECH_MONARCHY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iRevDemocracyLevel` -5; `iRevIdxLocal` -1; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` -20 |
| CIVIC_IMPERIUM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_COURTHOUSE","iHappinessChange":6},{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iNumCitiesMaintenanceModifier` 25; `iRevIdxDistanceModifier` -50; `iRevIdxLocal` -1; `iRevIdxNational` -8; `iRevIdxSwitchTo` 20; `iWorkerSpeedModifier` 25 |
| CIVIC_NO_TAXES | `CivicOptionType` CIVICOPTION_TAXATION; `TradeYieldModifiers` [0,0,25]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` -1; `iAnarchyLength` 1; `iRevDemocracyLevel` 5; `iRevIdxDistanceModifier` -30; `iRevIdxLocal` -3; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20 |
| CIVIC_OLIGARCHY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 30; `iFreeExperience` 3; `iRevDemocracyLevel` -5; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |
| CIVIC_PASTORAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_PASTURE","ImprovementYields":[1,0,1]}]; `TechPrereq` TECH_ANIMAL_HUSBANDRY; `TradeYieldModifiers` [0,0,-30]; `Upkeep` UPKEEP_LOW; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` 5; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` -3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| CIVIC_PEASANTRY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_MANOR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_COTTAGE","ImprovementYields":[1,1,-1]},{"ImprovementType":"IMPROVEMENT_HAMLET","ImprovementYields":[2,2,-1]},{"ImprovementType":"IMPROVEMENT_VILLAGE","ImprovementYields":[2,3,-2]},{"ImprovementType":"IMPROVEMENT_TOWN","ImprovementYields":[2,4,-2]}]; `TechPrereq` TECH_AGRICULTURE; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iImprovementUpgradeRateModifier` 50; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -3; `iRevIdxSwitchTo` 20 |
| CIVIC_PRIESTHOOD | `CapitalCommerceModifiers` [0,25,50,0]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_PRIEST","bValid":true}]; `TechPrereq` TECH_PRIESTHOOD; `Upkeep` UPKEEP_MEDIUM; `bNoNonStateReligionSpread` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 3; `fRevIdxNationalityMod` 0; `fRevViolentMod` -0.5; `iAnarchyLength` 1; `iLargestCityHappiness` 2; `iNumCitiesMaintenanceModifier` 25; `iRevDemocracyLevel` -2; `iRevIdxDistanceModifier` 30; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iRevReligiousFreedom` -3; `iStateReligionBuildingProductionModifier` 25; `iWarWearinessModifier` -20 |
| CIVIC_PROLETARIAT | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_SHAFT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WORKSHOP","ImprovementYields":[1,2,0]},{"ImprovementType":"IMPROVEMENT_LUMBERMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WINDMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WATERMILL","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [0,50,0]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 3; `iWorkerSpeedModifier` 25 |
| CIVIC_RAIDERS | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_SEAFARING; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iBaseFreeUnits` 20; `iFreeExperience` 3; `iGreatGeneralRateModifier` 25; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| CIVIC_SACRIFICE_CULT | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_SACRIFICIAL_ALTAR","iHappinessChange":6},{"BuildingType":"BUILDINGCLASS_MESOAMERICAN_MAGICIAN_PYRAMID","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_RELIGION; `Hurrys` [{"HurryType":"HURRY_POPULATION","bHurry":true}]; `TechPrereq` TECH_BLOOD_CULT; `Upkeep` UPKEEP_LOW; `bStateReligion` True; `fRevIdxBadReligionMod` .5; `fRevIdxGoodReligionMod` .7; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iFreeExperience` 3; `iGreatGeneralRateModifier` 25; `iGreatPeopleRateModifier` -25; `iLargestCityHappiness` -3; `iRevIdxHolyCityBad` 1; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` 2; `iRevIdxNational` -1; `iRevIdxSwitchTo` 50; `iRevReligiousFreedom` -3; `iStateReligionBuildingProductionModifier` 25; `iStateReligionHappiness` 1; `iWarWearinessModifier` -50 |
| CIVIC_SLAVERY | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `CommerceModifiers` [25,0,0]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[2,1,1]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_HIGH; `YieldModifiers` [0,10,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` -5; `iWarWearinessModifier` 50 |
| CIVIC_SPIRITISM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_ORACLE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_STONEHENGE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_RELIGION; `CommerceModifiers` [0,0,0,25]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[0,0,2]}]; `TechPrereq` TECH_MYSTICISM; `bStateReligion` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatPeopleRateModifier` 25; `iRevIdxSwitchTo` -30; `iRevReligiousFreedom` 7; `iStateReligionFreeExperience` 3 |
| CIVIC_STANDARDIZED_TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_WRITING; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -25; `iNumCitiesMaintenanceModifier` 10; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CIVIC_TUTORS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_WRITING; `YieldModifiers` [10,10,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 30; `iGreatPeopleRateModifier` 30; `iRevIdxDistanceModifier` 25; `iRevIdxLocal` -1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| CivicInfo | Fields set (records.json) |
|---|---|
| ABORIGINAL | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevEnvironmentalProtection` 3; `iRevIdxLocal` -3; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 7; `iWorkerSpeedModifier` -25 |
| ACCOUNTING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [25,0,0]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -30; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| AGRICULTURAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[0,0,1]}]; `TechPrereq` TECH_AGRICULTURE; `TradeYieldModifiers` [0,0,-30]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGreatPeopleRateModifier` -25; `iRevEnvironmentalProtection` -5; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxSwitchTo` 20 |
| BARTER | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_TRADE; `TradeYieldModifiers` [20,0,-25]; `Upkeep` UPKEEP_LOW; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iImprovementUpgradeRateModifier` 10; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| BOOKKEEPING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [30,0,0,25]; `TechPrereq` TECH_LITERATURE; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -50; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| CENSUS | `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [25,0,0,10]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| COASTAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FISHING_BOATS","ImprovementYields":[0,1,1]}]; `TechPrereq` TECH_FISHING; `TradeYieldModifiers` [0,0,-30]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` -2; `iRevIdxSwitchTo` 20 |
| COINAGE | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [25,0,0]; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 20; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iTradeRoutes` 1; `iWarWearinessModifier` 25 |
| ELDERS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_MYSTICISM; `YieldModifiers` [0,0,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 25; `iGreatPeopleRateModifier` 25; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| FISCUS | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_TREASURY","iHappinessChange":-5}]; `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [50,0,0,25]; `Hurrys` [{"HurryType":"HURRY_GOLD","bHurry":true}]; `TechPrereq` TECH_CURRENCY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iLargestCityHappiness` -5; `iNumCitiesMaintenanceModifier` 20; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| FOLKLORE | `CivicOptionType` CIVICOPTION_RELIGION; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iFreeExperience` 3; `iRevReligiousFreedom` 5; `iWarWearinessModifier` -20 |
| FORTIFICATION | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_WALLS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MASONRY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAIWeight` 1; `iAnarchyLength` 1; `iDomesticGreatGeneralRateModifier` 100; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| HEREDITARY_RULE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_NOBLE","bValid":true}]; `TechPrereq` TECH_MONARCHY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iRevDemocracyLevel` -5; `iRevIdxLocal` -1; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` -20 |
| HOMESCHOOLING | `CivicOptionType` CIVICOPTION_EDUCATION; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxDistanceModifier` 80; `iRevIdxLocal` 3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| HUNTER_GATHERER | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[1,1,0]}]; `TradeYieldModifiers` [0,0,-50]; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iMilitaryProductionModifier` -25; `iRevIdxDistanceModifier` 80; `iRevIdxLocal` -3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iWorkerSpeedModifier` -25 |
| IMPERIUM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_COURTHOUSE","iHappinessChange":6},{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iNumCitiesMaintenanceModifier` 25; `iRevIdxDistanceModifier` -50; `iRevIdxLocal` -1; `iRevIdxNational` -8; `iRevIdxSwitchTo` 20; `iWorkerSpeedModifier` 25 |
| MERCENARIES | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_TRADE; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.3; `iAnarchyLength` 1; `iFreeExperience` 5; `iGoldPerMilitaryUnit` 1; `iGoldPerUnit` 1; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` 1; `iRevIdxSwitchTo` 20 |
| METALS | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_METAL_CASTING; `TradeYieldModifiers` [20,0,-10]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 15; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| NO_TAXES | `CivicOptionType` CIVICOPTION_TAXATION; `TradeYieldModifiers` [0,0,25]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` -1; `iAnarchyLength` 1; `iRevDemocracyLevel` 5; `iRevIdxDistanceModifier` -30; `iRevIdxLocal` -3; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20 |
| OLIGARCHY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 30; `iFreeExperience` 3; `iRevDemocracyLevel` -5; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |
| ORAL_LAW | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `YieldModifiers` [-25,-25,-10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 2; `iRevIdxNational` 2; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25; `iWorkerSpeedModifier` -25 |
| PASTORAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_PASTURE","ImprovementYields":[1,0,1]}]; `TechPrereq` TECH_ANIMAL_HUSBANDRY; `TradeYieldModifiers` [0,0,-30]; `Upkeep` UPKEEP_LOW; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` 5; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` -3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| PATRIARCH | `CivicOptionType` CIVICOPTION_LEADERSHIP; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 30; `iNumCitiesMaintenanceModifier` 30; `iRevDemocracyLevel` -3; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| PATRICIAN | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MARKET","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_BANK","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PRAEFECTUR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `TradeYieldModifiers` [0,0,25]; `Upkeep` UPKEEP_LOW; `bCanDoElection` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0.5; `fRevViolentMod` 0; `iAnarchyLength` 1; `iCorporationMaintenanceModifier` -10; `iDistanceMaintenanceModifier` 25; `iGreatGeneralRateModifier` 30; `iRevDemocracyLevel` 1; `iRevEnvironmentalProtection` -2; `iRevIdxDistanceModifier` 20; `iRevIdxLocal` 2; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 100 |
| PEASANTRY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_MANOR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_COTTAGE","ImprovementYields":[1,1,-1]},{"ImprovementType":"IMPROVEMENT_HAMLET","ImprovementYields":[2,2,-1]},{"ImprovementType":"IMPROVEMENT_VILLAGE","ImprovementYields":[2,3,-2]},{"ImprovementType":"IMPROVEMENT_TOWN","ImprovementYields":[2,4,-2]}]; `TechPrereq` TECH_AGRICULTURE; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iImprovementUpgradeRateModifier` 50; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -3; `iRevIdxSwitchTo` 20 |
| PRIESTHOOD | `CapitalCommerceModifiers` [0,25,50,0]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_PRIEST","bValid":true}]; `TechPrereq` TECH_PRIESTHOOD; `Upkeep` UPKEEP_MEDIUM; `bNoNonStateReligionSpread` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 3; `fRevIdxNationalityMod` 0; `fRevViolentMod` -0.5; `iAnarchyLength` 1; `iLargestCityHappiness` 2; `iNumCitiesMaintenanceModifier` 25; `iRevDemocracyLevel` -2; `iRevIdxDistanceModifier` 30; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iRevReligiousFreedom` -3; `iStateReligionBuildingProductionModifier` 25; `iWarWearinessModifier` -20 |
| PROLETARIAT | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_SHAFT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WORKSHOP","ImprovementYields":[1,2,0]},{"ImprovementType":"IMPROVEMENT_LUMBERMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WINDMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WATERMILL","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [0,50,0]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 3; `iWorkerSpeedModifier` 25 |
| RAIDERS | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_SEAFARING; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iBaseFreeUnits` 20; `iFreeExperience` 3; `iGreatGeneralRateModifier` 25; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| SLAVERY | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `CommerceModifiers` [25,0,0]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[2,1,1]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_HIGH; `YieldModifiers` [0,10,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` -5; `iWarWearinessModifier` 50 |
| SPIRITISM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_ORACLE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_STONEHENGE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_RELIGION; `CommerceModifiers` [0,0,0,25]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[0,0,2]}]; `TechPrereq` TECH_MYSTICISM; `bStateReligion` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatPeopleRateModifier` 25; `iRevIdxSwitchTo` -30; `iRevReligiousFreedom` 7; `iStateReligionFreeExperience` 3 |
| STANDARDIZED_TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_WRITING; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -25; `iNumCitiesMaintenanceModifier` 10; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| STANDING_ARMY | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MILITARY_TRAINING; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` -0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iFreeExperience` 5; `iGoldPerMilitaryUnit` 1; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| STATE_RELIGION | `CivicOptionType` CIVICOPTION_RELIGION; `SpecialistValids` [{"SpecialistType":"SPECIALIST_PRIEST","bValid":true}]; `TechPrereq` TECH_LITERATURE; `Upkeep` UPKEEP_HIGH; `bAllowInquisitions` True; `bNoNonStateReligionSpread` True; `bStateReligion` True; `fRevIdxBadReligionMod` 1; `fRevIdxGoodReligionMod` 3; `fRevIdxNationalityMod` 0; `fRevViolentMod` -0.5; `iAnarchyLength` 1; `iRevIdxHolyCityBad` 1; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` -1; `iRevIdxNational` -6; `iRevReligiousFreedom` -2; `iStateReligionBuildingProductionModifier` 25; `iStateReligionFreeExperience` 3; `iStateReligionHappiness` 6; `iStateReligionUnitProductionModifier` 25; `iWarWearinessModifier` -50 |
| TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_POTTERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,-10,-10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -10; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 10; `iRevIdxLocal` -1; `iRevIdxSwitchTo` 20 |
| TRIBAL_WARFARE | `CivicOptionType` CIVICOPTION_MILITARY; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| TRIBUTE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CapitalCommerceModifiers` [0,0,25]; `CapitalYieldModifiers` [25,25,25]; `CivicOptionType` CIVICOPTION_TAXATION; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,0,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAIWeight` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iNumCitiesMaintenanceModifier` 10; `iRevDemocracyLevel` -3; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| TUTORS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_WRITING; `YieldModifiers` [10,10,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 30; `iGreatPeopleRateModifier` 30; `iRevIdxDistanceModifier` 25; `iRevIdxLocal` -1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| CivicInfo | Fields set (records.json) |
|---|---|
| ABORIGINAL | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevEnvironmentalProtection` 3; `iRevIdxLocal` -3; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 7; `iWorkerSpeedModifier` -25 |
| ACCOUNTING | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `CommerceModifiers` [25,0,0]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -30; `iNumCitiesMaintenanceModifier` 15; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| AGRICULTURAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[0,0,1]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[0,0,1]}]; `TechPrereq` TECH_AGRICULTURE; `TradeYieldModifiers` [0,0,-30]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGreatPeopleRateModifier` -25; `iRevEnvironmentalProtection` -5; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxSwitchTo` 20 |
| BARTER | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_TRADE; `TradeYieldModifiers` [20,0,-25]; `Upkeep` UPKEEP_LOW; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iImprovementUpgradeRateModifier` 10; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| CENSUS | `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [25,0,0,10]; `TechPrereq` TECH_MATHEMATICS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| COASTAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FISHING_BOATS","ImprovementYields":[0,1,1]}]; `TechPrereq` TECH_FISHING; `TradeYieldModifiers` [0,0,-30]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` -2; `iRevIdxSwitchTo` 20 |
| COINAGE | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [25,0,0]; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 20; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iTradeRoutes` 1; `iWarWearinessModifier` 25 |
| ELDERS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_MYSTICISM; `YieldModifiers` [0,0,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 25; `iGreatPeopleRateModifier` 25; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| FANATICISM | `CivicOptionType` CIVICOPTION_RELIGION; `TechPrereq` TECH_MONOTHEISM; `TradeYieldModifiers` [0,0,-25]; `Upkeep` UPKEEP_LOW; `bAllowInquisitions` True; `bNoCorporations` True; `bNoForeignCorporations` True; `bNoNonStateReligionSpread` True; `bStateReligion` True; `bUpgradeAnywhere` True; `fRevIdxBadReligionMod` 1; `fRevIdxGoodReligionMod` 3; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iFreeUnitsPopulationPercent` 30; `iGreatGeneralRateModifier` 30; `iNonStateReligionHappiness` -3; `iRevIdxHolyCityBad` 1; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevReligiousFreedom` -5; `iStateReligionFreeExperience` 5; `iStateReligionHappiness` 6; `iStateReligionUnitProductionModifier` 50; `iWarWearinessModifier` -25 |
| FISCUS | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_TREASURY","iHappinessChange":-5}]; `CapitalYieldModifiers` [0,0,25]; `CivicOptionType` CIVICOPTION_TAXATION; `CommerceModifiers` [50,0,0,25]; `Hurrys` [{"HurryType":"HURRY_GOLD","bHurry":true}]; `TechPrereq` TECH_CURRENCY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iLargestCityHappiness` -5; `iNumCitiesMaintenanceModifier` 20; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| FOLKLORE | `CivicOptionType` CIVICOPTION_RELIGION; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iFreeExperience` 3; `iRevReligiousFreedom` 5; `iWarWearinessModifier` -20 |
| FORTIFICATION | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_WALLS","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MASONRY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAIWeight` 1; `iAnarchyLength` 1; `iDomesticGreatGeneralRateModifier` 100; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| HEREDITARY_RULE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_NOBLE","bValid":true}]; `TechPrereq` TECH_MONARCHY; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iRevDemocracyLevel` -5; `iRevIdxLocal` -1; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` -20 |
| HOMESCHOOLING | `CivicOptionType` CIVICOPTION_EDUCATION; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxDistanceModifier` 80; `iRevIdxLocal` 3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| HUNTER_GATHERER | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[1,1,0]}]; `TradeYieldModifiers` [0,0,-50]; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iMilitaryProductionModifier` -25; `iRevIdxDistanceModifier` 80; `iRevIdxLocal` -3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iWorkerSpeedModifier` -25 |
| IMPERIUM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_COURTHOUSE","iHappinessChange":6},{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iMilitaryProductionModifier` 25; `iNumCitiesMaintenanceModifier` 25; `iRevIdxDistanceModifier` -50; `iRevIdxLocal` -1; `iRevIdxNational` -8; `iRevIdxSwitchTo` 20; `iWorkerSpeedModifier` 25 |
| MERCENARIES | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_TRADE; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.3; `iAnarchyLength` 1; `iFreeExperience` 5; `iGoldPerMilitaryUnit` 1; `iGoldPerUnit` 1; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` 1; `iRevIdxSwitchTo` 20 |
| METALS | `CivicOptionType` CIVICOPTION_ECONOMY; `TechPrereq` TECH_METAL_CASTING; `TradeYieldModifiers` [20,0,-10]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iGoldPerUnit` 1; `iImprovementUpgradeRateModifier` 15; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25 |
| NO_TAXES | `CivicOptionType` CIVICOPTION_TAXATION; `TradeYieldModifiers` [0,0,25]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` -1; `iAnarchyLength` 1; `iRevDemocracyLevel` 5; `iRevIdxDistanceModifier` -30; `iRevIdxLocal` -3; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20 |
| OLIGARCHY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_PALACE","iHappinessChange":6}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 30; `iFreeExperience` 3; `iRevDemocracyLevel` -5; `iRevIdxDistanceModifier` 30; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |
| ORAL_LAW | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `YieldModifiers` [-25,-25,-10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 2; `iRevIdxNational` 2; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 25; `iWorkerSpeedModifier` -25 |
| PASTORAL | `CivicOptionType` CIVICOPTION_ECONOMY; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_PASTURE","ImprovementYields":[1,0,1]}]; `TechPrereq` TECH_ANIMAL_HUSBANDRY; `TradeYieldModifiers` [0,0,-30]; `Upkeep` UPKEEP_LOW; `bNoCorporations` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iRevEnvironmentalProtection` 5; `iRevIdxDistanceModifier` 50; `iRevIdxLocal` -3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| PATRIARCH | `CivicOptionType` CIVICOPTION_LEADERSHIP; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 30; `iNumCitiesMaintenanceModifier` 30; `iRevDemocracyLevel` -3; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| PATRICIAN | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_SENATE","iHappinessChange":12},{"BuildingType":"BUILDINGCLASS_FORUM_ROMANUM","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_MARKET","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_BANK","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_PRAEFECTUR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `TechPrereq` TECH_CODE_OF_LAWS; `TradeYieldModifiers` [0,0,25]; `Upkeep` UPKEEP_LOW; `bCanDoElection` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0.5; `fRevViolentMod` 0; `iAnarchyLength` 1; `iCorporationMaintenanceModifier` -10; `iDistanceMaintenanceModifier` 25; `iGreatGeneralRateModifier` 30; `iRevDemocracyLevel` 1; `iRevEnvironmentalProtection` -2; `iRevIdxDistanceModifier` 20; `iRevIdxLocal` 2; `iRevIdxNational` -3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 100 |
| PEASANTRY | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_MANOR","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_COTTAGE","ImprovementYields":[1,1,-1]},{"ImprovementType":"IMPROVEMENT_HAMLET","ImprovementYields":[2,2,-1]},{"ImprovementType":"IMPROVEMENT_VILLAGE","ImprovementYields":[2,3,-2]},{"ImprovementType":"IMPROVEMENT_TOWN","ImprovementYields":[2,4,-2]}]; `TechPrereq` TECH_AGRICULTURE; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iImprovementUpgradeRateModifier` 50; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -3; `iRevIdxSwitchTo` 20 |
| PRIESTHOOD | `CapitalCommerceModifiers` [0,25,50,0]; `CivicOptionType` CIVICOPTION_LEADERSHIP; `SpecialistValids` [{"SpecialistType":"SPECIALIST_PRIEST","bValid":true}]; `TechPrereq` TECH_PRIESTHOOD; `Upkeep` UPKEEP_MEDIUM; `bNoNonStateReligionSpread` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 3; `fRevIdxNationalityMod` 0; `fRevViolentMod` -0.5; `iAnarchyLength` 1; `iLargestCityHappiness` 2; `iNumCitiesMaintenanceModifier` 25; `iRevDemocracyLevel` -2; `iRevIdxDistanceModifier` 30; `iRevIdxHolyCityGood` 3; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20; `iRevReligiousFreedom` -3; `iStateReligionBuildingProductionModifier` 25; `iWarWearinessModifier` -20 |
| PROLETARIAT | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,2]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_SHAFT_MINE","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WORKSHOP","ImprovementYields":[1,2,0]},{"ImprovementType":"IMPROVEMENT_LUMBERMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WINDMILL","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_WATERMILL","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_CURRENCY; `TradeYieldModifiers` [0,50,0]; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxLocal` -3; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` 3; `iWorkerSpeedModifier` 25 |
| RAIDERS | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_SEAFARING; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iBaseFreeUnits` 20; `iFreeExperience` 3; `iGreatGeneralRateModifier` 25; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| SLAVERY | `CivicOptionType` CIVICOPTION_EMPLOYMENT; `CommerceModifiers` [25,0,0]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_FARM","ImprovementYields":[1,0,0]},{"ImprovementType":"IMPROVEMENT_OLIVE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_WINERY","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_APPLE_FARM","ImprovementYields":[1,0,1]},{"ImprovementType":"IMPROVEMENT_PLANTATION","ImprovementYields":[0,0,2]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM1","ImprovementYields":[2,1,1]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM2","ImprovementYields":[1,1,0]},{"ImprovementType":"IMPROVEMENT_LATIFUNDIUM3","ImprovementYields":[0,1,0]},{"ImprovementType":"IMPROVEMENT_MINE","ImprovementYields":[0,1,0]}]; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_HIGH; `YieldModifiers` [0,10,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 3; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iRevLaborFreedom` -5; `iWarWearinessModifier` 50 |
| SPIRITISM | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_ORACLE","iHappinessChange":3},{"BuildingType":"BUILDINGCLASS_STONEHENGE","iHappinessChange":3}]; `CivicOptionType` CIVICOPTION_RELIGION; `CommerceModifiers` [0,0,0,25]; `ImprovementYieldChanges` [{"ImprovementType":"IMPROVEMENT_JUNGLE_CAMP","ImprovementYields":[0,0,2]}]; `TechPrereq` TECH_MYSTICISM; `bStateReligion` True; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatPeopleRateModifier` 25; `iRevIdxSwitchTo` -30; `iRevReligiousFreedom` 7; `iStateReligionFreeExperience` 3 |
| STANDARDIZED_TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_WRITING; `Upkeep` UPKEEP_LOW; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -25; `iNumCitiesMaintenanceModifier` 10; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| STANDING_ARMY | `CivicOptionType` CIVICOPTION_MILITARY; `TechPrereq` TECH_MILITARY_TRAINING; `Upkeep` UPKEEP_MEDIUM; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` -0.5; `iAIWeight` 1; `iAnarchyLength` 1; `iFreeExperience` 5; `iGoldPerMilitaryUnit` 1; `iHappyPerMilitaryUnit` 1; `iRevIdxLocal` -3; `iRevIdxNational` -1; `iRevIdxSwitchTo` 20 |
| TABLETS | `CivicOptionType` CIVICOPTION_ADMINISTRATION; `TechPrereq` TECH_POTTERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,-10,-10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` -10; `iNumCitiesMaintenanceModifier` 10; `iRevIdxDistanceModifier` 10; `iRevIdxLocal` -1; `iRevIdxSwitchTo` 20 |
| TRIBAL_WARFARE | `CivicOptionType` CIVICOPTION_MILITARY; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0.5; `iAnarchyLength` 1; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` -1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20 |
| TRIBUTE | `BuildingHappinessChanges` [{"BuildingType":"BUILDINGCLASS_CASTLE","iHappinessChange":3}]; `CapitalCommerceModifiers` [0,0,25]; `CapitalYieldModifiers` [25,25,25]; `CivicOptionType` CIVICOPTION_TAXATION; `TechPrereq` TECH_SLAVERY; `Upkeep` UPKEEP_LOW; `YieldModifiers` [-10,0,0]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 1; `iAIWeight` 1; `iAnarchyLength` 1; `iDistanceMaintenanceModifier` 25; `iNumCitiesMaintenanceModifier` 10; `iRevDemocracyLevel` -3; `iRevIdxDistanceModifier` 30; `iRevIdxLocal` 1; `iRevIdxNational` 3; `iRevIdxSwitchTo` 20; `iWarWearinessModifier` 50 |
| TUTORS | `CivicOptionType` CIVICOPTION_EDUCATION; `TechPrereq` TECH_WRITING; `YieldModifiers` [10,10,10]; `fRevIdxBadReligionMod` 0; `fRevIdxGoodReligionMod` 0; `fRevIdxNationalityMod` 0; `fRevViolentMod` 0; `iAnarchyLength` 1; `iGreatGeneralRateModifier` 30; `iGreatPeopleRateModifier` 30; `iRevIdxDistanceModifier` 25; `iRevIdxLocal` -1; `iRevIdxNational` 1; `iRevIdxSwitchTo` 20 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| TechInfo | Fields set (records.json) |
|---|---|
| TECH_CODE_OF_LAWS | `Advisor` ADVISOR_RELIGION; `AndPreReqs` ["TECH_WRITING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_RELIGION","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_MONARCHY"]; `Quote` TXT_KEY_TECH_CODE_OF_LAWS_QUOTE; `Sound` AS2D_TECH_CODE_OF_LAWS; `SoundMP` AS2D_TECH_MP_CODE_OF_LAWS; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 11 |
| TECH_CURRENCY | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_MATHEMATICS","TECH_METAL_CASTING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_CURRENCY_QUOTE; `Sound` AS2D_TECH_CURRENCY; `SoundMP` AS2D_TECH_MP_CURRENCY; `bGoldTrading` True; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 400; `iGridX` 5; `iGridY` 7 |
| TECH_MATHEMATICS | `Advisor` ADVISOR_SCIENCE; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":1},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_MATHEMATICS_QUOTE; `Sound` AS2D_TECH_MATHEMATICS; `SoundMP` AS2D_TECH_MP_MATHEMATICS; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 250; `iFeatureProductionModifier` 50; `iGridX` 5; `iGridY` 5; `iPower` 6 |
| TECH_METAL_CASTING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":9},{"FlavorType":"FLAVOR_GOLD","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_MINING"]; `Quote` TXT_KEY_TECH_METAL_CASTING_QUOTE; `Sound` AS2D_TECH_METALCAST; `SoundMP` AS2D_TECH_MP_METALCAST; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 90; `iGridX` 3; `iGridY` 17; `iPower` 4 |
| TECH_TRADE | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_POTTERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_ANIMAL_HUSBANDRY","TECH_SAILING"]; `Quote` TXT_KEY_TECH_TRADE_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bOpenBordersTrading` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 85; `iGridX` 3; `iGridY` 3; `iTradeRoutes` 1 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| TechInfo | Fields set (records.json) |
|---|---|
| TECH_CODE_OF_LAWS | `Advisor` ADVISOR_RELIGION; `AndPreReqs` ["TECH_WRITING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":2},{"FlavorType":"FLAVOR_RELIGION","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":3},{"FlavorType":"FLAVOR_GOLD","iFlavor":5},{"FlavorType":"FLAVOR_GROWTH","iFlavor":4}]; `OrPreReqs` ["TECH_MONARCHY"]; `Quote` TXT_KEY_TECH_CODE_OF_LAWS_QUOTE; `Sound` AS2D_TECH_CODE_OF_LAWS; `SoundMP` AS2D_TECH_MP_CODE_OF_LAWS; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 350; `iGridX` 6; `iGridY` 11 |
| TECH_CURRENCY | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_MATHEMATICS","TECH_METAL_CASTING"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_CURRENCY_QUOTE; `Sound` AS2D_TECH_CURRENCY; `SoundMP` AS2D_TECH_MP_CURRENCY; `bGoldTrading` True; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 400; `iGridX` 5; `iGridY` 7 |
| TECH_MATHEMATICS | `Advisor` ADVISOR_SCIENCE; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_CLASSICAL; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":1},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":1},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10}]; `OrPreReqs` ["TECH_WRITING"]; `Quote` TXT_KEY_TECH_MATHEMATICS_QUOTE; `Sound` AS2D_TECH_MATHEMATICS; `SoundMP` AS2D_TECH_MP_MATHEMATICS; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 250; `iFeatureProductionModifier` 50; `iGridX` 5; `iGridY` 5; `iPower` 6 |
| TECH_METAL_CASTING | `Advisor` ADVISOR_MILITARY; `AndPreReqs` ["TECH_TRADE"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":7},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":9},{"FlavorType":"FLAVOR_GOLD","iFlavor":6},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":5},{"FlavorType":"FLAVOR_CULTURE","iFlavor":2}]; `OrPreReqs` ["TECH_MINING"]; `Quote` TXT_KEY_TECH_METAL_CASTING_QUOTE; `Sound` AS2D_TECH_METALCAST; `SoundMP` AS2D_TECH_MP_METALCAST; `bGoodyTech` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 16; `iCost` 90; `iGridX` 3; `iGridY` 17; `iPower` 4 |
| TECH_TRADE | `Advisor` ADVISOR_ECONOMY; `AndPreReqs` ["TECH_POTTERY"]; `Era` ERA_ANCIENT; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":2},{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_GROWTH","iFlavor":3}]; `OrPreReqs` ["TECH_ANIMAL_HUSBANDRY","TECH_SAILING"]; `Quote` TXT_KEY_TECH_TRADE_QUOTE; `Sound` AS2D_TECH_GENERIC; `bGoodyTech` True; `bOpenBordersTrading` True; `bTrade` True; `iAdvancedStartCost` 100; `iAsset` 8; `iCost` 85; `iGridX` 3; `iGridY` 3; `iTradeRoutes` 1 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `w.game3_trajectory` | table, 7 values | cities | human and AI | every 50th turn and the last full turn | 7 | M lines (end of each player's turn): the human's value, the median AI's, and the human's rank among all players by score and by power [game3] |
| `w.game4_trajectory` | table, 7 values | cities | human and AI | every 50th turn and the last full turn | 7 | M lines (end of each player's turn): the human's value, the median AI's, and the human's rank among all players by score and by power [game4] |
| `w.game1_city_sources` | table, 5 values | cities | human | by 50-turn period | 5 | cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game1] |
| `w.game2_city_sources` | table, 4 values | cities | human | by 50-turn period | 4 | cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game2] |
| `w.game3_city_sources` | table, 4 values | cities | human | by 50-turn period | 4 | cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game3] |
| `w.game4_city_sources` | table, 6 values | cities | human | by 50-turn period | 6 | cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) [game4] |
| `w.game3_commerce_jumps` | table, 6 values | turns | human | whole game | 6 | M lines of the human: the first turn of each run of turns where commerce exceeds the M line three turns earlier by more than a quarter (turns after 50; a base of commerce 1, an anarchy turn, is left out), with the cities captured (K lines), the civics adopted (CIVICS commands) and the techs acquired (X lines) in the three turns ending there, and the golden-age turns left [game3] |
| `w.game4_commerce_jumps` | table, 14 values | turns | human | whole game | 14 | M lines of the human: the first turn of each run of turns where commerce exceeds the M line three turns earlier by more than a quarter (turns after 50; a base of commerce 1, an anarchy turn, is left out), with the cities captured (K lines), the civics adopted (CIVICS commands) and the techs acquired (X lines) in the three turns ending there, and the golden-age turns left [game4] |
| `w.game3_anarchy_turns` | table, 2 values | turns | every player | turns 51 to the last M line | 2 | wl_M lines with commerce <= 1 (anarchy: CvCity::isDisorder includes the owner's anarchy, CvCity.cpp:4671) [game3] |
| `w.game4_anarchy_turns` | table, 2 values | turns | every player | turns 51 to the last M line | 2 | wl_M lines with commerce <= 1 (anarchy: CvCity::isDisorder includes the owner's anarchy, CvCity.cpp:4671) [game4] |
| `w.game3_civic_switches` | table, 10 values | turns | human | each turn with a CIVICS command | 10 | every turn with a CIVICS command of the human (A lines; adopted: the civics of its last command that turn not in the previous one), with its last M line before that turn and its first M line from that turn on that are not anarchy turns (commerce 1), and the anarchy turns between; the M line is written at the end of the turn, after its commands [game3] |
| `w.game4_civic_switches` | table, 12 values | turns | human | each turn with a CIVICS command | 12 | every turn with a CIVICS command of the human (A lines; adopted: the civics of its last command that turn not in the previous one), with its last M line before that turn and its first M line from that turn on that are not anarchy turns (commerce 1), and the anarchy turns between; the M line is written at the end of the turn, after its commands [game4] |
| `w.game3_civic_worth` | table, 29 values | derived xml | human | save | 29 | probe (HH_probe, CvPlayer::setCivics then a full recalculation, worked tiles unchanged; every swap restored the baseline): the human's totals with each civic it could adopt in place of its current one, minus its actual totals. Negative: the current civic is worth that much [game3] |
| `w.game4_civic_worth` | table, 28 values | derived xml | human | save | 28 | probe (HH_probe, CvPlayer::setCivics then a full recalculation, worked tiles unchanged; every swap restored the baseline): the human's totals with each civic it could adopt in place of its current one, minus its actual totals. Negative: the current civic is worth that much [game4] |
| `w.game3_economy_civics` | table, 26 values | category | all players | save | 26 | civics at the save (dump): how many players run each civic, the human and the AIs [game3] |
| `w.game4_economy_civics` | table, 22 values | category | all players | save | 22 | civics at the save (dump): how many players run each civic, the human and the AIs [game4] |
| `w.game3_economy_techs` | table, 5 values | techs | all players | save | 5 | techs at the save (dump), for the techs that enable the economy and taxation civics in play (TechPrereq of COINAGE, FISCUS, BARTER, METALS, ACCOUNTING, PATRICIAN): players holding each [game3] |
| `w.game4_economy_techs` | table, 5 values | techs | all players | save | 5 | techs at the save (dump), for the techs that enable the economy and taxation civics in play (TechPrereq of COINAGE, FISCUS, BARTER, METALS, ACCOUNTING, PATRICIAN): players holding each [game4] |
| `w.game3_currency_rank` | table, 12 values | rank | AI players | save | 12 | probe: every AI's AI_techValue (path 1) of each tech it can research at the save; the rank of CURRENCY among them, its value, the top tech and its value, and what the AI researches [game3] |
| `w.game4_currency_rank` | table, 15 values | rank | AI players | save | 15 | probe: every AI's AI_techValue (path 1) of each tech it can research at the save; the rank of CURRENCY among them, its value, the top tech and its value, and what the AI researches [game4] |
| `w.game3_tech_sources` | table, 7 values | techs | human and AI | every 50th turn and the last | 7 | X lines (techs acquired, cumulative) and deal_items (techs received by the human in deals, cumulative) [game3] |
| `w.game4_tech_sources` | table, 7 values | techs | human and AI | every 50th turn and the last | 7 | X lines (techs acquired, cumulative) and deal_items (techs received by the human in deals, cumulative) [game4] |
| `w.game1_war_ledger` | table, 3 values | battles | human and AI | each war of the human | 3 | W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game1] |
| `w.game2_war_ledger` | table, 3 values | battles | human and AI | each war of the human | 3 | W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game2] |
| `w.game3_war_ledger` | table, 2 values | battles | human and AI | each war of the human | 2 | W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game3] |
| `w.game4_war_ledger` | table, 8 values | battles | human and AI | each war of the human | 8 | W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) [game4] |
| `w.game1_units_ledger` | table, 2 values | battles | human | whole game | 2 | C lines with the R line directly after: units the human's attacks and defences killed and lost [game1] |
| `w.game2_units_ledger` | table, 1 values | battles | human | whole game | 1 | C lines with the R line directly after: units the human's attacks and defences killed and lost [game2] |
| `w.game3_units_ledger` | table, 1 values | battles | human | whole game | 1 | C lines with the R line directly after: units the human's attacks and defences killed and lost [game3] |
| `w.game4_units_ledger` | table, 2 values | battles | human | whole game | 2 | C lines with the R line directly after: units the human's attacks and defences killed and lost [game4] |
| `w.game3_ai_response` | table, 2 values | units at save | AI players | each war the human declared | 2 | M lines: the target's military units the turn before the declaration and at peace (or the last turn); G lines: the target's stacks near or in enemy land during the war, and those standing within 3 plots of a human city the human then owned (cities from MISSION_FOUND and K lines) [game3] |
| `w.game4_ai_response` | table, 8 values | units at save | AI players | each war the human declared | 8 | M lines: the target's military units the turn before the declaration and at peace (or the last turn); G lines: the target's stacks near or in enemy land during the war, and those standing within 3 plots of a human city the human then owned (cities from MISSION_FOUND and K lines) [game4] |
