<!-- Rendered by method/docs.py from playstyle.md.in. Do not edit; edit the template. -->
# The human's playstyle in detail

The four logged games, read as one way of playing. Game 3 is Germany (Charles V) and game 4 is
Rome (Julius Caesar) (P lines). Most tables are from those two, the games with M lines and a save
dump. The parts come from the earlier studies: decisions (`study/human.md`), tiles, trade and
combat (`study/data.md`), economy and wars (`study/winning.md`), and workers, builds and
movement (`study/operations.md`). New figures are in the tables below. Section 10 puts it all
together as a sequence of play.

## 1. Method

- **The whole and the parts.** "Each part can be understood only out of the whole to which it
  belongs, and vice versa." An interpreter working from "disconnected observations can never
  reach an independent interpretation" (Schleiermacher, in Mueller-Vollmer, *The Hermeneutics
  Reader*, §20 and 21, p. 84). Every mechanism below names the facts it rests on. Section 10
  states the whole and what would refute each part of it.
- **What a building, civic, tech or improvement does** is read from its XML record, in the
  appendix, never from memory (CLAUDE.md, rule 4). A value quoted in the text is taken from that
  record when the page is rendered.
- **Phases** come from an exact optimal partition of the human's per-turn activity with a
  parsimony penalty, checked at half and twice the penalty (`tools/phases.py`). **The choice of
  target** comes from maximum-likelihood strategy classification against guessing (Bröder, in
  *Heuristics*, chapter 17; `tools/strategy.py`).
- **The gold ledger** (section 6.2) splits each change of the human's gold into income, deals and
  a residual named by the events of the turn. The residual on turns without any event is its
  running check: it stays small, so the named residuals are spending and windfalls, not error.

## 2. The course of a game

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

## 3. The tech tree

### 3.1 Every tech, against the AIs

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

### 3.2 What each tech was used for, and how soon

For each tech, the turns until the human first adopted a civic, ordered a building or unit, or
ordered a build that the tech unlocks:

| tech | acquired | civic_after | building_after | unit_after | build_after |
|---|---|---|---|---|---|
| SLAVERY | 31 | 1 |  |  |  |
| POTTERY | 65 | 1 |  |  | 3 |
| MINING | 84 |  |  |  | 1 |
| NATUROPATHY | 97 |  |  |  |  |
| MASONRY | 117 | 101 | 7 |  | 11 |
| MYSTICISM | 129 | 1 | 8 |  |  |
| RELIGION_NORDIC | 138 |  |  |  |  |
| TRADE | 155 | 1 | 12 | 6 |  |
| METAL_CASTING | 173 |  | 2 | 12 |  |
| SAILING | 181 |  | 1 |  |  |
| BRONZE_WORKING | 192 |  |  | 1 |  |
| PRIESTHOOD | 196 |  |  |  |  |
| WRITING | 197 | 0 | 7 |  |  |
| THE_WHEEL | 205 |  |  |  | 19 |
| MATHEMATICS | 217 | 1 |  |  |  |
| FERMENTATION | 221 |  | 2 |  | 0 |
| CITY_PLANNING | 229 |  | 1 |  |  |
| MONARCHY | 236 |  | 0 |  |  |
| CURRENCY | 240 | 1 | 20 |  |  |
| MILITARY_TRAINING | 246 |  | 1 | 12 |  |
| IRON_WORKING | 248 |  |  |  |  |
| ARCHERY | 249 |  | 8 |  |  |
| CODE_OF_LAWS | 252 | 1 | 1 |  |  |
| ALPHABET | 256 |  |  |  |  |
| LITERATURE | 260 | 1 | 1 |  |  |
| SEAFARING | 261 |  |  |  |  |
| CONSTRUCTION | 265 |  |  |  |  |

*turns; who: human; turn: acquisition turns; rows counted: 27; source: X lines of the human; for each tech, the turns until the human first used what it unlocks: a civic adopted (CIVICS command; CivicInfo TechPrereq), a building ordered (ORDER type 1; BuildingInfo PrereqTech), a unit ordered (ORDER type 0; UnitInfo PrereqTech), a build ordered (MISSION_BUILD; BuildInfo PrereqTech); empty: not used before the save. Unlocks through other fields (TechTypes, AndPreReqs of later techs) are not counted [game3]. Every value counted (27).*

| tech | acquired | civic_after | building_after | unit_after | build_after |
|---|---|---|---|---|---|
| SLAVERY | 34 | 1 |  |  |  |
| MINING | 61 |  |  |  | 6 |
| POTTERY | 87 | 1 |  |  | 10 |
| MASONRY | 121 | 108 | 1 |  | 7 |
| MYSTICISM | 137 | 1 | 1 |  |  |
| SAILING | 166 |  | 1 | 10 |  |
| ANIMAL_HUSBANDRY | 177 |  |  |  | 2 |
| TRADE | 181 |  | 6 |  |  |
| PRIESTHOOD | 188 |  |  |  |  |
| METAL_CASTING | 191 | 38 | 1 | 7 | 55 |
| RELIGION_GREEK | 198 |  |  |  |  |
| WRITING | 205 | 0 | 4 | 17 |  |
| THE_WHEEL | 206 |  |  |  | 3 |
| MATHEMATICS | 221 | 1 |  | 29 |  |
| BRONZE_WORKING | 228 |  | 1 | 2 |  |
| FERMENTATION | 231 |  | 1 |  | 3 |
| MONARCHY | 234 |  | 6 |  |  |
| CITY_PLANNING | 237 |  | 1 | 5 |  |
| CURRENCY | 244 | 1 |  |  |  |
| CODE_OF_LAWS | 252 |  | 1 |  |  |
| IRON_WORKING | 254 |  |  | 6 |  |
| SEAFARING | 255 |  |  |  |  |
| MILITARY_TRAINING | 257 |  | 1 |  |  |
| ARCHERY | 258 |  |  |  |  |
| NAVAL_WARFARE | 259 |  |  |  |  |
| SHIP_BUILDING | 261 |  | 1 | 4 |  |
| SIEGE_WARFARE | 264 |  | 1 | 2 |  |
| MACHINERY | 272 |  |  |  |  |
| CONSTRUCTION | 274 |  | 2 |  | 1 |
| CHARIOTRY | 275 |  | 1 |  |  |
| HORSEBACK_RIDING | 276 |  |  |  |  |
| SCULPTURE | 277 |  |  |  |  |
| CALENDAR | 283 |  |  |  |  |
| WATERWORKS | 284 |  | 1 |  |  |
| MONOTHEISM | 285 |  |  |  |  |

*turns; who: human; turn: acquisition turns; rows counted: 35; source: X lines of the human; for each tech, the turns until the human first used what it unlocks: a civic adopted (CIVICS command; CivicInfo TechPrereq), a building ordered (ORDER type 1; BuildingInfo PrereqTech), a unit ordered (ORDER type 0; UnitInfo PrereqTech), a build ordered (MISSION_BUILD; BuildInfo PrereqTech); empty: not used before the save. Unlocks through other fields (TechTypes, AndPreReqs of later techs) are not counted [game4]. Every value counted (35).*

### 3.3 Civics, the moment they open

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

### 3.4 The logic

- **The order is the same in both games:**
  1. Slavery, for Oligarchy and Tribute.
  2. Mining and Pottery, for mines, cottages and Tablets.
  3. Masonry, for Town Essentials and Walls.
  4. Mysticism, for the Obelisk and the religion civic.
  5. Sailing and Trade, for river ports and the market.
  6. Metal Casting, for the Forge and Jewellery.
  7. Writing, for Tutors, Standardized Tablets and the School of Scribes.
  8. Mathematics, for Accounting.
  9. City Planning, for City Essentials, Irrigation Canals and the Port.
  10. Currency, for Coinage, Fiscus and Proletariat.
  11. Code of Laws, for courthouses, Patrician (game 3) or the Senate (game 4).
  12. Last, a run of military techs.
- **Each tech is used at once.** The civic or building it opens is usually taken within a few
  turns (sections 3.2 and 3.3).
- **Where the human leads:** it is among the first to the economic gateways (Slavery, Pottery,
  Masonry, Mathematics, City Planning, Currency). Few or no AIs have them first.
- **Where it trails, or trades:** the religious and early techs the AIs take first (Mysticism,
  Animal Husbandry, Priesthood). In game 4, several cheap techs come by deal: Animal Husbandry,
  Priesthood, Writing, The Wheel, Monarchy.
- **The military techs come last, just before the campaigns.** Bronze Working, Military Training,
  Iron Working, Siege Warfare and Construction arrive in the turns before and during the wars in
  game 4; Bronze Working before the war in game 3. Each opens a unit or building
  the human orders soon after.

## 4. Buildings and wonders

### 4.1 The order of buildings in each city

Each building the human completed: in how many of its cities, its median place in each city's
order of completions, how soon after its tech, and the same for the AIs' cities:

| building | kind | human_cities | human_median_rank_in_city | human_first | turns_after_tech | ai_cities | ai_median_rank_in_city |
|---|---|---|---|---|---|---|---|
| TOWN_ESSENTIALS | building | 9 | 1.0 | 128 | 11 | 68 | 2.0 |
| COURIER_SYSTEM | national | 1 | 1.0 | 206 | 9 | 5 | 9.0 |
| OBELISK | building | 12 | 1.5 | 137 | 8 | 60 | 1.0 |
| WALLS | building | 11 | 3.0 | 136 | 19 | 28 | 1.0 |
| FORGE | building | 13 | 4.0 | 178 | 5 | 7 | 6.0 |
| CITY_ESSENTIALS | building | 13 | 5.0 | 231 | 2 | 3 | 6.0 |
| SCHOOL_OF_SCRIBES | building | 7 | 5.0 | 204 | 7 | 14 | 7.0 |
| LIGHTHOUSE | building | 1 | 6.0 | 237 | 56 | 17 | 4.0 |
| RIVER_PORT | building | 10 | 6.5 | 184 | 3 | 32 | 3.0 |
| IRRIGATION_CANALS | building | 10 | 7.5 | 233 | 4 | 3 | 7.0 |
| JEWELLERY | building | 6 | 8.5 | 181 | 8 | 12 | 5.5 |
| MARKET | building | 6 | 8.5 | 174 | 19 | 10 | 5.0 |
| NORDIC_TEMPLE | building | 3 | 9.0 | 206 |  | 0 |  |
| BREWERY | national | 1 | 10.0 | 224 | 3 | 1 | 10.0 |
| COURTHOUSE | building | 10 | 10.5 | 256 | 4 | 0 |  |
| BARRACKS | building | 5 | 12.0 | 247 | 1 | 0 |  |
| BROTHEL | building | 1 | 13.0 | 260 | 20 | 0 |  |
| CELTIC_TEMPLE | building | 1 | 13.0 | 258 |  | 4 | 9.5 |
| TREASURY | national | 1 | 13.0 | 238 | 2 | 4 | 11.0 |
| ARCHERY_RANGE | building | 4 | 14.0 | 257 | 8 | 0 |  |
| NORDIC_SHRINE | world wonder | 1 | 14.0 | 260 | 122 | 0 |  |
| LIBRARY | building | 4 | 15.0 | 264 | 4 | 0 |  |

*cities; who: every player; turn: whole game; rows counted: 22; source: N lines: each building the human completed, the number of its cities that completed it, its median position in each city's order of completions (1: the city's first), the first completion, its distance in turns from the human's X line of the building's PrereqTech (empty when the building needs no tech; its other prerequisites, such as TechTypes, a religion or a building, are not counted); the same count and position for the AIs' cities [game3]. Every value counted (22).*

| building | kind | human_cities | human_median_rank_in_city | human_first | turns_after_tech | ai_cities | ai_median_rank_in_city |
|---|---|---|---|---|---|---|---|
| TOWN_ESSENTIALS | building | 16 | 1.0 | 126 | 5 | 118 | 2.0 |
| WALLS | building | 8 | 2.0 | 137 | 16 | 83 | 1.0 |
| OBELISK | building | 14 | 2.5 | 142 | 5 | 61 | 1.0 |
| BREWERY | national | 1 | 4.0 | 241 | 10 | 7 | 11.0 |
| FORGE | building | 12 | 4.5 | 197 | 6 | 22 | 6.0 |
| RIVER_PORT | building | 6 | 4.5 | 171 | 5 | 46 | 3.0 |
| LIGHTHOUSE | building | 9 | 5.0 | 175 | 9 | 39 | 4.0 |
| CITY_ESSENTIALS | building | 13 | 6.0 | 239 | 2 | 48 | 6.0 |
| SCHOOL_OF_SCRIBES | building | 10 | 7.0 | 209 | 4 | 33 | 7.0 |
| COURIER_SYSTEM | national | 1 | 8.0 | 218 | 13 | 14 | 8.5 |
| HELLENIC_TEMPLE | building | 7 | 9.0 | 212 |  | 0 |  |
| JEWELLERY | building | 11 | 10.0 | 209 | 18 | 35 | 7.0 |
| ROMAN_FORUM | building | 9 | 10.0 | 194 | 13 | 0 |  |
| EARLY_BARRACKS | building | 6 | 10.0 | 229 | 1 | 0 |  |
| PORT | building | 12 | 10.5 | 258 | 21 | 11 | 10.0 |
| STATUE_OF_ZEUS | building | 1 | 11.0 | 251 |  | 0 |  |
| COURTHOUSE | building | 11 | 12.0 | 254 | 2 | 5 | 6.0 |
| ROMAN_DEPOT | building | 9 | 13.0 | 242 | 5 | 0 |  |
| IRRIGATION_CANALS | building | 7 | 13.0 | 247 | 10 | 17 | 11.0 |
| MARS_TEMPLE | building | 5 | 14.0 | 221 | 221 | 0 |  |
| TREASURY | national | 1 | 15.0 | 242 | 8 | 4 | 11.0 |
| BARRACKS | building | 11 | 16.0 | 259 | 2 | 17 | 8.0 |
| PRAEFECTUR | building | 1 | 17.0 | 264 | 27 | 0 |  |
| HELLENIC_CATHEDRAL | building | 2 | 17.5 | 234 |  | 0 |  |
| LEGION_BARRACKS | building | 11 | 18.0 | 265 | 1 | 0 |  |
| PRAEFECTURA_ANNONAE | world wonder | 1 | 18.0 | 253 | 1 | 0 |  |
| SHIPYARD | building | 4 | 18.5 | 262 | 1 | 0 |  |
| SENATE | world wonder | 1 | 19.0 | 258 | 6 | 0 |  |
| STABLE | building | 8 | 19.5 | 276 | 1 | 0 |  |
| HIGH_WALLS | building | 4 | 20.0 | 272 | 8 | 0 |  |
| SIEGE_WORKSHOP | building | 5 | 21.0 | 277 | 13 | 6 | 11.5 |
| SCOTLAND_YARD | building | 1 | 24.0 | 270 |  | 0 |  |
| COLOSSEUM | world wonder | 1 | 25.0 | 278 | 4 | 0 |  |
| FORUM_ROMANUM | world wonder | 1 | 26.0 | 280 | 6 | 0 |  |

*cities; who: every player; turn: whole game; rows counted: 34; source: N lines: each building the human completed, the number of its cities that completed it, its median position in each city's order of completions (1: the city's first), the first completion, its distance in turns from the human's X line of the building's PrereqTech (empty when the building needs no tech; its other prerequisites, such as TechTypes, a religion or a building, are not counted); the same count and position for the AIs' cities [game4]. Every value counted (34).*

### 4.2 Wonders

| kind | human | human_first | all_ais | most_by_one_ai |
|---|---|---|---|---|
| national | 3 | 206 | 10 | 3 |
| world wonder | 1 | 260 | 7 | 3 |

*units built; who: every player; turn: whole game; rows counted: 2; source: N lines of world wonders (BuildingClassInfo iMaxGlobalInstances 1) and national wonders (iMaxPlayerInstances or iMaxTeamInstances 1) [game3]. Every value counted (2).*

| kind | human | human_first | all_ais | most_by_one_ai |
|---|---|---|---|---|
| national | 3 | 218 | 27 | 3 |
| world wonder | 4 | 253 | 9 | 2 |

*units built; who: every player; turn: whole game; rows counted: 2; source: N lines of world wonders (BuildingClassInfo iMaxGlobalInstances 1) and national wonders (iMaxPlayerInstances or iMaxTeamInstances 1) [game4]. Every value counted (2).*

### 4.3 What the city template gives

From the XML records (appendix):
- **Upgrade lines.** In RoM a building of a line removes the ones it replaces when it is built
  (`RoMEventManager.py:71` and `RoMEventManager.py:102`, the two lists, applied in
  `onBuildingBuilt`, `RoMEventManager.py:324`). So a city holds one tier of each line, and the effects of the
  tiers do not add up:
  - City Essentials replaces Town Essentials, which replaces Settlement Essentials;
  - Barracks replaces Early Barracks, and Legion Barracks replaces both;
  - Port replaces River Port and Harbor;
  - the Library replaces the School of Scribes;
  - the Forum is the Roman market.
- **The Essentials line is also the granary.** Each tier keeps part of the food store when the
  city grows (`iFoodKept`): Settlement `20`,
  Town `30`, City
  `30` per cent. Section 6.5 has the
  effect on growth.
- **Town Essentials**, the human's first building in a city in both games (the AIs build
  Walls or the Obelisk first):
  - land-unit production `[{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]`;
  - gold `[15]` per cent;
  - a merchant slot.
- **City Essentials**, built in nearly every city within a few turns of City Planning; the AIs
  build it in a minority of their cities:
  - the same land-unit production `[{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]`;
  - gold `[15]` per cent;
  - merchant slots `[{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":3}]`.
- **The Forge**, early in the order in nearly every city the human founded:
  - production bonuses from metal resources, `[{"BonusType":"BONUS_GOLD","YieldModifiers":[0,0,25]},{"BonusType":"BONUS_SILVER","YieldModifiers":[0,0,15]},{"BonusType":"BONUS_GEMS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COPPER","YieldModifiers":[0,25,0]},{"BonusType":"BONUS_IRON","YieldModifiers":[0,25,0]},{"BonusType":"BONUS_LEAD","YieldModifiers":[0,25,0]}]`;
  - an engineer slot.
- **The trade buildings:**
  - River Port: trade routes `1`, route yield
    `20` per cent;
  - Roman Forum: route yield `30` per cent,
    gold `[25]` per cent;
  - Jewellery: route yield `25` per cent;
  - Port: trade routes `3`, route yield
    `50` per cent.
- **The Courthouse**, in most cities soon after Code of Laws (the AIs build almost none):
  maintenance `-25` per cent.
- **The military buildings come last:** Barracks, Early Barracks, Legion Barracks, Stable, Siege
  Workshop. They are built in most cities only in the war phases, one or two turns after their
  tech.
- **Wonders.** The human builds world wonders only late, after the city template is in place: a
  religious shrine in game 3, and in game 4 the Roman wonders of the last phases, which then
  outnumber any single AI's (section 4.2). It does not race for early wonders; its production
  goes first into the city template and units.

### 4.4 The result, at the save

| city_group | cities | pop | food | hammers | commerce | trade_routes | trade_commerce | buildings |
|---|---|---|---|---|---|---|---|---|
| human founded | 6 | 5.5 | 19.5 | 56.5 | 51.5 | 5.0 | 15.0 | 8.5 |
| human captured | 6 | 7.5 | 22.5 | 49.0 | 43.0 | 5.0 | 12.0 | 7.0 |
| human capital | 1 | 17.0 | 9.0 | 79.0 | 160.0 | 5.0 | 25.0 | 16.0 |
| AI other | 99 | 4.0 | 5.0 | 9.0 | 10.0 | 2.0 | 2.0 | 2.0 |
| AI capitals | 17 | 11.0 | 7.0 | 34.0 | 41.0 | 3.0 | 11.0 | 6.0 |

*cities at save; who: every player; turn: save; rows counted: 5; source: cities in the save dump: population, food, hammers, commerce, trade routes and their commerce, and buildings; human cities split into the capital (BUILDING_PALACE), the cities it captured (K lines) and those it founded; AI capitals and other AI cities [game3]. Every value counted (5).*

| city_group | cities | pop | food | hammers | commerce | trade_routes | trade_commerce | buildings |
|---|---|---|---|---|---|---|---|---|
| human founded | 12 | 10.5 | 24.5 | 81.0 | 80.0 | 7.0 | 35.0 | 14.5 |
| human captured | 13 | 5.0 | 2.0 | 11.0 | 11.0 | 4.0 | 6.0 | 3.0 |
| human capital | 1 | 24.0 | 49.0 | 185.0 | 235.0 | 10.0 | 88.0 | 24.0 |
| AI other | 162 | 4.0 | 7.0 | 14.0 | 12.0 | 3.0 | 4.0 | 2.0 |
| AI capitals | 17 | 13.0 | 22.0 | 52.0 | 63.0 | 4.0 | 19.0 | 10.0 |

*cities at save; who: every player; turn: save; rows counted: 5; source: cities in the save dump: population, food, hammers, commerce, trade routes and their commerce, and buildings; human cities split into the capital (BUILDING_PALACE), the cities it captured (K lines) and those it founded; AI capitals and other AI cities [game4]. Every value counted (5).*

The human's ordinary founded cities make more hammers and commerce than the AIs' capitals, and
have more trade routes and many more buildings than the AIs' other cities. Captured cities are
behind: in game 4 most were taken in the last turns.

## 5. Tiles

### 5.1 What is built where

Every build order by the plot's traits:

| build | orders | hill | flat_river | flat_dry | water | with_resource |
|---|---|---|---|---|---|---|
| BUILD_TRACK | 51 | 28 | 15 | 8 | 0 | 19 |
| BUILD_COTTAGE | 38 | 20 | 10 | 8 | 0 | 8 |
| BUILD_ROAD | 28 | 13 | 14 | 1 | 0 | 8 |
| BUILD_FARM | 21 | 0 | 21 | 0 | 0 | 1 |
| BUILD_MINE | 16 | 16 | 0 | 0 | 0 | 8 |
| BUILD_CAMP | 8 | 4 | 2 | 2 | 0 | 6 |
| BUILD_APPLE_FARM | 2 | 0 | 1 | 1 | 0 | 2 |
| BUILD_QUARRY | 2 | 2 | 0 | 0 | 0 | 2 |

*orders; who: human; turn: order turns; plot traits at the save; rows counted: 8; source: A lines MISSION_BUILD by the plot's traits in the save dump: hills, flat land on a river or not, water, and a resource on it; terrain type and river do not change in play, a resource can be revealed later [game3]. Every value counted (8).*

| build | orders | hill | flat_river | flat_dry | water | with_resource |
|---|---|---|---|---|---|---|
| BUILD_TRACK | 69 | 43 | 20 | 6 | 0 | 24 |
| BUILD_ROAD | 48 | 25 | 20 | 3 | 0 | 16 |
| BUILD_MINE | 42 | 42 | 0 | 0 | 0 | 13 |
| BUILD_COTTAGE | 35 | 25 | 5 | 5 | 0 | 5 |
| BUILD_FARM | 28 | 0 | 28 | 0 | 0 | 6 |
| BUILD_PAVED | 14 | 6 | 4 | 4 | 0 | 6 |
| BUILD_CAMP | 13 | 8 | 2 | 3 | 0 | 11 |
| BUILD_FISHING_BOATS | 9 | 0 | 0 | 0 | 9 | 9 |
| BUILD_WINERY | 6 | 1 | 3 | 2 | 0 | 6 |
| BUILD_QUARRY | 4 | 4 | 0 | 0 | 0 | 4 |
| BUILD_PASTURE | 3 | 1 | 2 | 0 | 0 | 3 |
| BUILD_WORKSHOP | 3 | 0 | 1 | 2 | 0 | 0 |
| BUILD_OLIVE_FARM | 2 | 2 | 0 | 0 | 0 | 2 |

*orders; who: human; turn: order turns; plot traits at the save; rows counted: 13; source: A lines MISSION_BUILD by the plot's traits in the save dump: hills, flat land on a river or not, water, and a resource on it; terrain type and river do not change in play, a resource can be revealed later [game4]. Every value counted (13).*

### 5.2 The worked land at the save, against the AIs

| plots | worked | unimproved | cottage_line | mines | farms | other |
|---|---|---|---|---|---|---|
| human, hill | 54 | 11 | 14 | 21 | 0 | 8 |
| human, flat, river | 43 | 4 | 12 | 0 | 20 | 7 |
| human, flat, dry | 9 | 0 | 5 | 0 | 0 | 4 |
| AI, hill | 232 | 60 | 62 | 60 | 1 | 49 |
| AI, flat, river | 201 | 43 | 30 | 0 | 84 | 44 |
| AI, flat, dry | 84 | 31 | 11 | 0 | 13 | 29 |

*tiles at save; who: every player; turn: save; rows counted: 6; source: worked land plots in the save dump by owner and trait (as in build_plot_class), and the improvement on them; cottage line: cottage, hamlet, village, town [game3]. Every value counted (6).*

| plots | worked | unimproved | cottage_line | mines | farms | other |
|---|---|---|---|---|---|---|
| human, hill | 77 | 25 | 8 | 35 | 0 | 9 |
| human, flat, river | 33 | 4 | 2 | 0 | 21 | 6 |
| human, flat, dry | 13 | 3 | 5 | 0 | 0 | 5 |
| AI, hill | 377 | 94 | 9 | 220 | 0 | 54 |
| AI, flat, river | 316 | 63 | 17 | 1 | 147 | 88 |
| AI, flat, dry | 169 | 57 | 25 | 0 | 28 | 59 |

*tiles at save; who: every player; turn: save; rows counted: 6; source: worked land plots in the save dump by owner and trait (as in build_plot_class), and the improvement on them; cottage line: cottage, hamlet, village, town [game4]. Every value counted (6).*

### 5.3 The logic

- **Part of the rule is the game's.** A farm needs flat land with irrigation, which a river
  gives (`bRequiresFlatlands`, `bRequiresIrrigation`, `bFreshWaterMakesValid`); a mine needs
  hills (`bHillsMakesValid`); resource improvements need their resource (appendix).
  - Every farm the human ordered is on a river flat, and every mine on a hill, in both games.
- **The choices.**
  - Resources first: the first orders of game 4 are camps on resources and tracks
    (`study/operations.md`, section 2.1).
  - Cottages from Pottery on, on hills as well as on flats: most of game 4's cottages are on
    hills. Those hill cottages are later replaced by mines when production is wanted, mostly
    in the last phases (`study/data.md`, section 1.1).
  - Farms on the river flats.
  - Mines on hills from Mining on, and in large numbers only in the period before the wars
    (section 3.2 and `study/operations.md`, section 2.1).
  - Tracks, then roads, to connect the cities.
- **The tile mix is not the edge.** At the save, the human's shares of farms on river flats
  and of mines on hills differ from the AIs' in both directions, by game (section 5.2). No mix
  of improvements sets it apart. Its edge is elsewhere:
  - when it builds: early cottages, then mines before the wars;
  - how close to its cities it works: the first ring first, by hand (`study/operations.md`,
    section 6);
  - what the cities add on top: the template of section 4 and the civics of section 3.3.

### 5.4 The exact yield of the worked tiles

`tools/tileyield.py` rebuilds every worked plot's yield from the XML with the game's own formula
(`CvPlot::calculateYield`), and checks it against the yield in the save dump:

| side | worked_plots | food_exact | hammers_exact | commerce_exact | all_three_exact | missed | missed_with_a_battle_there |
|---|---|---|---|---|---|---|---|
| human | 109 | 109 | 108 | 108 | 108 | 1 | 0 |
| AI | 641 | 641 | 641 | 641 | 641 | 0 | 0 |

*tiles at save; who: every player; turn: save; rows counted: 750; source: tileyield.py: the model against CvPlot::getYield in the save dump; a battle there: a C line on the plot in the last ten turns (DCM battle effects, BATTLE_EFFECT_LESS_FOOD and _COMMERCE, are not in the dump). Every value counted (2).*

| side | worked_plots | food_exact | hammers_exact | commerce_exact | all_three_exact | missed | missed_with_a_battle_there |
|---|---|---|---|---|---|---|---|
| human | 163 | 157 | 163 | 157 | 157 | 6 | 6 |
| AI | 1015 | 1012 | 1011 | 1009 | 1008 | 7 | 2 |

*tiles at save; who: every player; turn: save; rows counted: 1178; source: tileyield.py: the model against CvPlot::getYield in the save dump; a battle there: a C line on the plot in the last ten turns (DCM battle effects, BATTLE_EFFECT_LESS_FOOD and _COMMERCE, are not in the dump). Every value counted (2).*

The few misses are plots fought over in the last turns: RoM's battle effects lower food and
commerce there, and the dump does not record them. For the exactly predicted plots, the mean
yield of each improvement and the source of every point of it:

| side_improvement_yield | plots | actual | nature | improvement | tech | civic | route | city | bonus |
|---|---|---|---|---|---|---|---|---|---|
| human, mine, food | 21 | 1.24 | 0.67 | 0.0 | 0.0 | 0.0 | 0.0 | 0.57 | 0.0 |
| human, mine, hammers | 21 | 6.67 | 2.67 | 2.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| human, mine, commerce | 21 | 1.24 | 0.29 | 0.95 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, farm, food | 20 | 7.45 | 1.7 | 2.2 | 2.0 | 1.0 | 0.0 | 0.55 | 0.0 |
| human, farm, hammers | 20 | 0.4 | 0.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, farm, commerce | 20 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, hamlet, food | 16 | 2.38 | 1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.88 | 0.0 |
| human, hamlet, hammers | 16 | 1.5 | 1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, hamlet, commerce | 16 | 2.06 | 0.06 | 2.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, city plot, food | 13 | 3.0 | 0.92 | 0.0 | 0.0 | 0.0 | 0.0 | 2.08 | 0.0 |
| human, city plot, hammers | 13 | 2.08 | 1.15 | 0.0 | 0.0 | 0.0 | 0.0 | 0.92 | 0.0 |
| human, city plot, commerce | 13 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, other, food | 10 | 6.8 | 1.6 | 2.5 | 1.7 | 0.2 | 0.0 | 0.8 | 0.0 |
| human, other, hammers | 10 | 2.9 | 1.3 | 1.0 | 0.6 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, other, commerce | 10 | 3.0 | 0.9 | 1.3 | 0.4 | 0.4 | 0.0 | 0.0 | 0.0 |
| human, village, food | 9 | 1.89 | 1.44 | 0.0 | 0.0 | 0.0 | 0.0 | 0.44 | 0.0 |
| human, village, hammers | 9 | 1.44 | 1.44 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, village, commerce | 9 | 5.11 | 0.44 | 4.67 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, camp, food | 8 | 3.88 | 1.75 | 1.5 | 0.0 | 0.0 | 0.0 | 0.62 | 0.0 |
| human, camp, hammers | 8 | 2.0 | 1.5 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, camp, commerce | 8 | 1.0 | 0.5 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, cottage, food | 6 | 2.17 | 1.33 | 0.0 | 0.0 | 0.0 | 0.0 | 0.83 | 0.0 |
| human, cottage, hammers | 6 | 1.5 | 1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, cottage, commerce | 6 | 1.17 | 0.17 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, water, food | 3 | 5.67 | 2.67 | 2.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| human, water, hammers | 3 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, water, commerce | 3 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, none, food | 2 | 2.5 | 1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| human, none, hammers | 2 | 1.5 | 1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, none, commerce | 2 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, water, food | 124 | 5.3 | 2.71 | 1.77 | 0.0 | 0.0 | 0.0 | 0.74 | 0.08 |
| AI, water, hammers | 124 | 0.46 | 0.0 | 0.0 | 0.0 | 0.46 | 0.0 | 0.0 | 0.0 |
| AI, water, commerce | 124 | 2.08 | 1.05 | 0.55 | 0.0 | 0.46 | 0.0 | 0.0 | 0.02 |
| AI, city plot, food | 116 | 3.0 | 0.79 | 0.0 | 0.0 | 0.0 | 0.0 | 2.21 | 0.0 |
| AI, city plot, hammers | 116 | 2.08 | 1.22 | 0.0 | 0.0 | 0.0 | 0.0 | 0.85 | 0.0 |
| AI, city plot, commerce | 116 | 1.03 | 0.75 | 0.0 | 0.0 | 0.0 | 0.0 | 0.28 | 0.0 |
| AI, farm, food | 98 | 7.42 | 2.03 | 2.55 | 1.77 | 0.92 | 0.0 | 0.1 | 0.05 |
| AI, farm, hammers | 98 | 0.72 | 0.72 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, farm, commerce | 98 | 1.14 | 0.87 | 0.0 | 0.0 | 0.28 | 0.0 | 0.0 | 0.0 |
| AI, other, food | 66 | 5.89 | 1.45 | 2.24 | 1.74 | 0.38 | 0.0 | 0.06 | 0.02 |
| AI, other, hammers | 66 | 3.15 | 1.89 | 1.02 | 0.24 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, other, commerce | 66 | 2.44 | 0.44 | 1.23 | 0.2 | 0.5 | 0.0 | 0.0 | 0.08 |
| AI, mine, food | 60 | 0.1 | 0.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, mine, hammers | 60 | 6.47 | 2.87 | 1.9 | 0.92 | 0.78 | 0.0 | 0.0 | 0.0 |
| AI, mine, commerce | 60 | 1.35 | 0.35 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, camp, food | 55 | 3.0 | 1.2 | 1.56 | 0.0 | 0.0 | 0.0 | 0.18 | 0.05 |
| AI, camp, hammers | 55 | 2.25 | 1.96 | 0.29 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, camp, commerce | 55 | 0.85 | 0.4 | 0.45 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, cottage, food | 51 | 1.75 | 0.8 | 0.0 | 0.0 | 0.94 | 0.0 | 0.0 | 0.0 |
| AI, cottage, hammers | 51 | 3.04 | 2.1 | 0.0 | 0.0 | 0.94 | 0.0 | 0.0 | 0.0 |
| AI, cottage, commerce | 51 | 0.33 | 0.27 | 1.0 | 0.0 | -0.94 | 0.0 | 0.0 | 0.0 |
| AI, hamlet, food | 40 | 2.75 | 1.0 | 0.0 | 0.0 | 1.75 | 0.0 | 0.0 | 0.0 |
| AI, hamlet, hammers | 40 | 3.5 | 1.75 | 0.0 | 0.0 | 1.75 | 0.0 | 0.0 | 0.0 |
| AI, hamlet, commerce | 40 | 1.52 | 0.3 | 2.1 | 0.0 | -0.88 | 0.0 | 0.0 | 0.0 |
| AI, none, food | 18 | 1.67 | 1.67 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, none, hammers | 18 | 1.83 | 1.83 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, none, commerce | 18 | 0.72 | 0.72 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, village, food | 12 | 3.17 | 1.17 | 0.0 | 0.0 | 2.0 | 0.0 | 0.0 | 0.0 |
| AI, village, hammers | 12 | 4.83 | 1.83 | 0.0 | 0.0 | 3.0 | 0.0 | 0.0 | 0.0 |
| AI, village, commerce | 12 | 1.33 | 0.0 | 3.33 | 0.0 | -2.0 | 0.0 | 0.0 | 0.0 |
| AI, workshop, food | 1 | 1.0 | 2.0 | -1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, workshop, hammers | 1 | 3.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, workshop, commerce | 1 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |

*food per tile; who: every player; turn: save; rows counted: 749; source: tileyield.py: exactly predicted worked plots; mean yield per plot and the mean of each source term (food, hammers and commerce rows; the unit applies to each row's own yield). Every value counted (63).*

| side_improvement_yield | plots | actual | nature | improvement | tech | civic | route | city | bonus |
|---|---|---|---|---|---|---|---|---|---|
| human, water, food | 40 | 4.65 | 2.55 | 1.27 | 0.0 | 0.0 | 0.0 | 0.82 | 0.0 |
| human, water, hammers | 40 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, water, commerce | 40 | 1.25 | 1.0 | 0.25 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, mine, food | 35 | 1.2 | 0.74 | 0.0 | 0.0 | 0.0 | 0.0 | 0.46 | 0.0 |
| human, mine, hammers | 35 | 8.23 | 2.26 | 1.97 | 3.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| human, mine, commerce | 35 | 0.91 | 0.2 | 0.71 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, farm, food | 21 | 8.9 | 1.9 | 2.38 | 3.0 | 1.0 | 0.0 | 0.62 | 0.0 |
| human, farm, hammers | 21 | 0.29 | 0.29 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, farm, commerce | 21 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, city plot, food | 20 | 3.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 | 0.0 |
| human, city plot, hammers | 20 | 2.0 | 1.15 | 0.0 | 0.0 | 0.0 | 0.0 | 0.85 | 0.0 |
| human, city plot, commerce | 20 | 1.0 | 0.75 | 0.0 | 0.0 | 0.0 | 0.0 | 0.25 | 0.0 |
| human, other, food | 16 | 6.0 | 1.62 | 1.88 | 1.56 | 0.44 | 0.0 | 0.5 | 0.0 |
| human, other, hammers | 16 | 2.88 | 1.31 | 0.81 | 0.75 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, other, commerce | 16 | 3.94 | 0.88 | 1.62 | 0.56 | 0.88 | 0.0 | 0.0 | 0.0 |
| human, hamlet, food | 8 | 1.25 | 1.25 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, hamlet, hammers | 8 | 1.38 | 1.38 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, hamlet, commerce | 8 | 2.25 | 0.25 | 2.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, village, food | 7 | 1.57 | 0.86 | 0.0 | 0.0 | 0.0 | 0.0 | 0.71 | 0.0 |
| human, village, hammers | 7 | 2.0 | 2.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, village, commerce | 7 | 4.14 | 0.14 | 4.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, none, food | 6 | 1.33 | 1.33 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, none, hammers | 6 | 2.17 | 2.17 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, none, commerce | 6 | 0.5 | 0.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, camp, food | 3 | 5.0 | 2.0 | 2.67 | 0.0 | 0.0 | 0.0 | 0.33 | 0.0 |
| human, camp, hammers | 3 | 1.67 | 1.67 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, camp, commerce | 3 | 0.67 | 0.33 | 0.33 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| human, workshop, food | 1 | 2.0 | 2.0 | -1.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| human, workshop, hammers | 1 | 7.0 | 1.0 | 1.0 | 3.0 | 2.0 | 0.0 | 0.0 | 0.0 |
| human, workshop, commerce | 1 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, mine, food | 221 | 0.49 | 0.35 | 0.0 | 0.0 | 0.0 | 0.0 | 0.14 | 0.0 |
| AI, mine, hammers | 221 | 6.64 | 2.53 | 2.14 | 1.0 | 0.97 | 0.0 | 0.0 | 0.0 |
| AI, mine, commerce | 221 | 0.6 | 0.19 | 0.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.01 |
| AI, city plot, food | 177 | 3.0 | 0.83 | 0.0 | 0.0 | 0.0 | 0.0 | 2.17 | 0.0 |
| AI, city plot, hammers | 177 | 2.05 | 1.19 | 0.0 | 0.0 | 0.0 | 0.0 | 0.86 | 0.0 |
| AI, city plot, commerce | 177 | 1.01 | 0.62 | 0.0 | 0.0 | 0.0 | 0.0 | 0.4 | 0.0 |
| AI, farm, food | 175 | 7.92 | 1.99 | 2.54 | 1.88 | 0.97 | 0.0 | 0.31 | 0.23 |
| AI, farm, hammers | 175 | 0.68 | 0.68 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, farm, commerce | 175 | 0.84 | 0.84 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, water, food | 152 | 5.46 | 2.74 | 1.85 | 0.0 | 0.0 | 0.0 | 0.76 | 0.11 |
| AI, water, hammers | 152 | 0.54 | 0.0 | 0.0 | 0.0 | 0.54 | 0.0 | 0.0 | 0.0 |
| AI, water, commerce | 152 | 2.04 | 1.07 | 0.43 | 0.0 | 0.54 | 0.0 | 0.0 | 0.01 |
| AI, other, food | 115 | 6.21 | 1.67 | 1.95 | 1.82 | 0.45 | 0.0 | 0.22 | 0.1 |
| AI, other, hammers | 115 | 3.05 | 1.64 | 1.14 | 0.27 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, other, commerce | 115 | 2.62 | 0.58 | 1.15 | 0.2 | 0.68 | 0.0 | 0.0 | 0.01 |
| AI, camp, food | 67 | 3.66 | 1.63 | 1.79 | 0.0 | 0.0 | 0.0 | 0.18 | 0.06 |
| AI, camp, hammers | 67 | 2.03 | 1.78 | 0.25 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, camp, commerce | 67 | 0.82 | 0.36 | 0.46 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, none, food | 35 | 1.91 | 1.89 | 0.0 | 0.0 | 0.0 | 0.0 | 0.03 | 0.0 |
| AI, none, hammers | 35 | 1.49 | 1.49 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, none, commerce | 35 | 0.86 | 0.86 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, cottage, food | 31 | 1.65 | 0.97 | 0.0 | 0.0 | 0.48 | 0.0 | 0.19 | 0.0 |
| AI, cottage, hammers | 31 | 2.19 | 1.71 | 0.0 | 0.0 | 0.48 | 0.0 | 0.0 | 0.0 |
| AI, cottage, commerce | 31 | 0.97 | 0.32 | 1.13 | 0.0 | -0.48 | 0.0 | 0.0 | 0.0 |
| AI, hamlet, food | 17 | 2.35 | 1.29 | 0.0 | 0.0 | 0.82 | 0.0 | 0.24 | 0.0 |
| AI, hamlet, hammers | 17 | 2.35 | 1.53 | 0.0 | 0.0 | 0.82 | 0.0 | 0.0 | 0.0 |
| AI, hamlet, commerce | 17 | 2.0 | 0.18 | 2.24 | 0.0 | -0.41 | 0.0 | 0.0 | 0.0 |
| AI, workshop, food | 15 | 1.0 | 1.6 | -1.0 | 0.0 | 0.0 | 0.0 | 0.4 | 0.0 |
| AI, workshop, hammers | 15 | 3.47 | 1.47 | 1.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, workshop, commerce | 15 | 1.27 | 0.27 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| AI, village, food | 3 | 3.0 | 1.0 | 0.0 | 0.0 | 2.0 | 0.0 | 0.0 | 0.0 |
| AI, village, hammers | 3 | 5.0 | 2.0 | 0.0 | 0.0 | 3.0 | 0.0 | 0.0 | 0.0 |
| AI, village, commerce | 3 | 1.33 | 0.0 | 3.33 | 0.0 | -2.0 | 0.0 | 0.0 | 0.0 |

*food per tile; who: every player; turn: save; rows counted: 1165; source: tileyield.py: exactly predicted worked plots; mean yield per plot and the mean of each source term (food, hammers and commerce rows; the unit applies to each row's own yield). Every value counted (63).*

What the tables show:
- **Farms and mines.** In game 4 the human's farms give more food, and its mines more hammers,
  than the AIs'; in game 3 they are about equal. In game 4 the difference is in two columns:
  - tech: the improvement's `TechYieldChanges` (for a farm: Fermentation, Mathematics and
    Waterworks, food each; for a mine: Mathematics, Machinery and Waterworks, hammers each).
    The human holds these techs earlier (section 3.1);
  - city: Irrigation Canals, `[1,0]`
    on every river plot of the city (food, hammers), built in most of the human's cities and few
    of the AIs' (section 6.5).
  - The human's mines also carry food: they are on river hills of cities with the canals.
- **The cottage line.** The AIs' cottages, hamlets and villages carry a civic column of plus
  food and hammers and minus commerce. That is Peasantry, held by some AIs
  (`study/winning.md`, section 4), which turns the cottage line into production tiles. The
  human, under Proletariat, keeps their commerce, and its villages give several times the AIs'.
- **Water.** The human's water tiles get food from the city column: the Essentials'
  `SeaPlotYieldChanges`.
- **Unimproved and city plots** are alike on both sides.

## 6. Production, gold and the build-up

### 6.1 Output per city

| turn | human_pop | ai_pop | human_hammers | ai_hammers | human_commerce | ai_commerce | human_food | ai_food |
|---|---|---|---|---|---|---|---|---|
| 100 | 5.0 | 3.0 | 20.0 | 6.0 | 28.0 | 23.0 | 15.0 | 16.0 |
| 125 | 3.5 | 3.0 | 10.0 | 6.5 | 17.5 | 17.5 | 17.0 | 16.0 |
| 150 | 2.5 | 3.0 | 9.0 | 7.67 | 13.75 | 13.33 | 12.25 | 13.33 |
| 175 | 2.8 | 3.2 | 10.0 | 7.8 | 13.8 | 13.33 | 13.6 | 14.33 |
| 200 | 3.8 | 4.0 | 21.8 | 10.2 | 17.8 | 13.33 | 20.4 | 16.33 |
| 225 | 4.08 | 3.67 | 21.08 | 12.0 | 20.38 | 15.5 | 25.31 | 17.6 |
| 250 | 6.69 | 4.73 | 40.15 | 15.2 | 63.69 | 22.2 | 37.85 | 23.4 |

*yield per turn; who: every player; turn: every 25th turn from 100; rows counted: 7; source: M lines: population, hammers, commerce and food of the whole empire divided by its cities; AI: the median over AI players; anarchy turns show commerce 1 [game3]. Every value counted (7).*

| turn | human_pop | ai_pop | human_hammers | ai_hammers | human_commerce | ai_commerce | human_food | ai_food |
|---|---|---|---|---|---|---|---|---|
| 100 | 2.33 | 3.0 | 7.0 | 5.0 | 7.33 | 17.25 | 12.67 | 16.25 |
| 125 | 3.0 | 3.0 | 7.25 | 5.0 | 6.75 | 16.0 | 15.5 | 15.17 |
| 150 | 3.6 | 3.33 | 9.8 | 7.0 | 8.6 | 14.83 | 17.6 | 15.33 |
| 175 | 4.29 | 4.0 | 10.43 | 9.5 | 11.57 | 15.0 | 19.71 | 19.75 |
| 200 | 5.25 | 4.25 | 13.63 | 11.08 | 18.25 | 16.88 | 23.75 | 21.0 |
| 225 | 5.9 | 4.62 | 25.6 | 15.81 | 30.5 | 22.02 | 29.0 | 23.55 |
| 250 | 7.55 | 4.92 | 48.36 | 20.71 | 70.64 | 26.89 | 40.0 | 26.32 |
| 275 | 8.11 | 5.57 | 55.63 | 22.54 | 73.89 | 28.83 | 41.95 | 28.19 |

*yield per turn; who: every player; turn: every 25th turn from 100; rows counted: 8; source: M lines: population, hammers, commerce and food of the whole empire divided by its cities; AI: the median over AI players; anarchy turns show commerce 1 [game4]. Every value counted (8).*

- **Hammers.** The gap opens in the rows after the middle of the game. By the last rows of both
  games, the human's hammers per city are more than twice the AI median.
- **Commerce.** Its commerce per city overtakes the AIs' only from about the same rows. In game 4
  it is below the AI median before that: the early empire is built for production and growth,
  not commerce.

### 6.2 Where the gold comes from and where it goes

| item | turns_0_149 | turns_150_199 | turns_200_249 | turns_250_on | total | turns_nonzero |
|---|---|---|---|---|---|---|
| deals: tech sold |  |  |  | 1520 | 1520 | 3 |
| income: gold per turn | 6 | -85 | 131 | 188 | 240 | 130 |
| residual: anarchy | 1 | 1 | 20 | -59 | -37 | 6 |
| residual: capture |  |  | 244 |  | 244 | 2 |
| residual: capture+upgrade |  |  | -33 |  | -33 | 2 |
| residual: no event (check) | 0 | 6 | -98 | -78 | -170 | 60 |
| residual: trade mission |  | 193 |  |  | 193 | 2 |
| residual: trade mission+upgrade |  | 22 |  |  | 22 | 1 |
| residual: upgrade |  | -80 |  |  | -80 | 1 |

*gold; who: human; turn: by period; rows counted: 9; source: M lines of the human: the change of its gold between consecutive M lines is split into the gold per turn of the earlier line (income), the gold of deals that turn (deal_items TRADE_GOLD: on a peace turn, Q lines; on a turn it gave a tech; other), and a residual named by the events of the turn: a city taken (K), a trade mission (MISSION_TRADE), a hurry (TASK 9, TASK_HURRY), an upgrade (COMMAND_UPGRADE), anarchy; the residual on turns with no such event is the check of the ledger (gold per turn changes within a turn) [game3]. Every value counted (9).*

| item | turns_0_149 | turns_150_199 | turns_200_249 | turns_250_on | total | turns_nonzero |
|---|---|---|---|---|---|---|
| deals: peace |  |  |  | 905 | 905 | 3 |
| deals: tech sold |  |  |  | 1780 | 1780 | 5 |
| income: gold per turn | 8 | 38 | 470 | 4192 | 4708 | 132 |
| residual: anarchy | -2 |  | 103 |  | 101 | 4 |
| residual: capture |  |  | 65 | 884 | 949 | 7 |
| residual: capture+hurry |  |  |  | -945 | -945 | 1 |
| residual: capture+upgrade |  |  | -109 | -844 | -953 | 3 |
| residual: hurry |  |  |  | -1165 | -1165 | 1 |
| residual: hurry+upgrade |  |  |  | -932 | -932 | 1 |
| residual: no event (check) | -1 | -11 | -44 | -3 | -59 | 90 |
| residual: upgrade |  |  | -361 | -1548 | -1909 | 12 |
| residual: upgrade+anarchy |  |  | -37 |  | -37 | 1 |

*gold; who: human; turn: by period; rows counted: 12; source: M lines of the human: the change of its gold between consecutive M lines is split into the gold per turn of the earlier line (income), the gold of deals that turn (deal_items TRADE_GOLD: on a peace turn, Q lines; on a turn it gave a tech; other), and a residual named by the events of the turn: a city taken (K), a trade mission (MISSION_TRADE), a hurry (TASK 9, TASK_HURRY), an upgrade (COMMAND_UPGRADE), anarchy; the residual on turns with no such event is the check of the ledger (gold per turn changes within a turn) [game4]. Every value counted (12).*

- **Game 3.** Tech sales bring more gold than the gold per turn. Great Merchant trade missions
  and city captures add more.
- **Game 4.**
  - Income: the gold per turn grows to the largest source after the civic switch. Tech sales,
    the peace payments and city plunder come on top.
  - Spending: the largest items are upgrades and hurries in the war phases.
  - The row of turns without events stays small, so the named rows are real flows.

### 6.3 The army is upgraded, not trained

| to_unit | upgrades | first_turn | last_turn | trained | attacks_by_that_type |
|---|---|---|---|---|---|
| CELTIC_SWORDSMAN | 9 | 207 | 217 | 3 | 0 |
| CELTIC_WARBAND | 5 | 172 | 193 | 19 | 29 |
| SPEARMAN | 2 | 162 | 211 | 5 | 0 |

*orders; who: human; turn: whole game; rows counted: 3; source: A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game1]. Every value counted (3).*

| to_unit | upgrades | first_turn | last_turn | trained | attacks_by_that_type |
|---|---|---|---|---|---|
| SARISSA | 6 | 223 | 234 | 2 | 3 |
| SPEARMAN | 5 | 171 | 228 | 2 | 0 |

*orders; who: human; turn: whole game; rows counted: 2; source: A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game2]. Every value counted (2).*

| to_unit | upgrades | first_turn | last_turn | trained | attacks_by_that_type |
|---|---|---|---|---|---|
| WARBAND | 8 | 193 | 204 | 23 | 14 |

*orders; who: human; turn: whole game; rows counted: 1; source: A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game3]. Every value counted (1).*

| to_unit | upgrades | first_turn | last_turn | trained | attacks_by_that_type |
|---|---|---|---|---|---|
| AUXILIAR | 25 | 267 | 274 | 0 | 2 |
| VELITES | 18 | 206 | 258 | 4 | 0 |
| TRIARII | 15 | 262 | 270 | 0 | 0 |
| ROME_LEGIONARY | 10 | 268 | 270 | 24 | 53 |
| PRINCIPES | 6 | 262 | 265 | 7 | 2 |

*orders; who: human; turn: whole game; rows counted: 5; source: A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game4]. Every value counted (5).*

- **Game 4.** The units that fight are largely old units upgraded with gold:
  - Auxiliaries and Triarii are never trained, only upgraded;
  - the Legionaries are both trained and upgraded;
  - the upgrades cluster in the turns just before the campaign (section 7.2).
- **Game 3.** Warbands are trained and upgraded before the war.
- **The supply.** The garrison was built cheaply in earlier phases: the capital trains units,
  `study/human.md`, reading 1.

### 6.4 The army is veteran from the start

- **Free experience from the XML:**
  - Oligarchy, held throughout game 4 and until after the war in game 3, gives every new unit
    `3` experience;
  - Legion Barracks give melee units `[{"UnitCombatType":"UNITCOMBAT_MELEE","iExperience":10},{"UnitCombatType":"UNITCOMBAT_RECON","iExperience":3},{"UnitCombatType":"UNITCOMBAT_ANIMAL","iExperience":2},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iExperience":2},{"UnitCombatType":"UNITCOMBAT_SIEGE","iExperience":1}]`;
    they need Barracks to be built (`BuildingClassNeededs`) and then replace them (section 4.3),
    so the Barracks' `[{"UnitCombatType":"UNITCOMBAT_MELEE","iExperience":3},{"UnitCombatType":"UNITCOMBAT_RECON","iExperience":3},{"UnitCombatType":"UNITCOMBAT_ANIMAL","iExperience":2},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iExperience":2},{"UnitCombatType":"UNITCOMBAT_SIEGE","iExperience":1}]` does not add;
  - a Mars Temple gives `3`.
- **The match with the log.** A melee unit trained under Oligarchy in a city with Legion
  Barracks and a Mars Temple starts with the sum of the three. The Legionaries that attack in
  game 4 carry a median experience of the same size (section 7.3). Much of their experience came
  with the unit, not from fighting. This fits the human's units carrying several times the AIs'
  promotions (`study/data.md`, section 4).
- **Production for war.** Military production is raised by the barracks tier the city holds
  (Early and Legion Barracks:
  `25` per cent), the
  Roman Depot and the Mars Temple. These add to the land-unit production of the Essentials tier
  the city holds.
- **Holding Oligarchy.** This explains why the human keeps Oligarchy in game 4 although the probe
  values Patrician higher in commerce (`study/winning.md`, section 3.3). In game 3 it switches to
  Patrician only after its war.
- **Fortification.** Adopted next to the wars, it gives
  `1` happiness per military
  unit, so a large garrison also keeps the cities content.

### 6.5 Growth

`tools/growth.py` computes, for every city at the save, its growth with the game's rules:
- the threshold of `CvPlayer::getGrowthThreshold`, lower for the AIs at higher difficulties
  (`iAIGrowthPercent`);
- the food kept on growth, the sum of the city's buildings' `iFoodKept`;
- the food a new citizen then costs, and the turns to it at the present surplus;
- the city's food, split into the plots it works and the rest. Food from trade routes is
  estimated from the city's route commerce and the owner's trade-yield modifiers.

| cities | n | pop | food | food_from_tiles | food_other | trade_commerce | trade_food_est | trade_hammers_est | surplus | growing | threshold | kept_pct | food_per_growth | turns_per_growth | happy_margin | health_margin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| human capital | 1 | 17 | 60 | 39 | 21 | 25 | 5.0 | 10.0 | 9 | 1 | 400 | 30 | 280 | 32 | 25 | 5 |
| human founded | 6 | 5.5 | 36.0 | 24.5 | 12.5 | 15.0 | 3.0 | 6.0 | 19.5 | 6 | 170.0 | 30.0 | 119.0 | 6.5 | 26.5 | 16.0 |
| human captured | 6 | 7.5 | 45.5 | 31.0 | 14.5 | 12.0 | 2.4 | 4.8 | 22.5 | 6 | 210.0 | 30.0 | 147.0 | 6.5 | 22.0 | 13.5 |
| AI capitals | 17 | 11 | 42 | 35 | 5 | 11 | 0.0 | 0.0 | 7 | 14 | 280 | 30 | 196 | 17.0 | 8 | 4 |
| AI other | 99 | 4 | 18 | 16 | 3 | 2 | 0.0 | 0.0 | 5 | 81 | 140 | 30 | 98 | 14 | 8 | 10 |

*cities at save; who: every player; turn: save; rows counted: 129; source: growth.py on the save dump of game3 (GAMESPEED_MARATHON, HANDICAP_NOBLE); medians per group; growing: cities with a food surplus; cities in disorder left out. Every value counted (5).*

| cities | n | pop | food | food_from_tiles | food_other | trade_commerce | trade_food_est | trade_hammers_est | surplus | growing | threshold | kept_pct | food_per_growth | turns_per_growth | happy_margin | health_margin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| human capital | 1 | 24 | 124 | 56 | 68 | 88 | 22.0 | 44.0 | 49 | 1 | 540 | 50 | 270 | 6 | 45 | -3 |
| human founded | 12 | 10.5 | 53.0 | 32.5 | 20.5 | 35.0 | 8.8 | 17.5 | 24.5 | 12 | 270.0 | 40.0 | 162.0 | 7.0 | 17.0 | 9.5 |
| human captured | 13 | 5 | 26 | 8 | 12 | 6 | 1.5 | 3.0 | 2 | 7 | 160 | 30 | 112 | 8 | 9 | 11 |
| AI capitals | 17 | 13 | 60 | 46 | 14 | 19 | 0.0 | 0.0 | 22 | 16 | 297 | 30 | 208 | 10.5 | 15 | 6 |
| AI other | 162 | 4.0 | 20.0 | 16.0 | 4.0 | 4.0 | 0.0 | 0.0 | 7.0 | 146 | 130.0 | 30.0 | 91.0 | 13.0 | 11.0 | 15.0 |

*cities at save; who: every player; turn: save; rows counted: 205; source: growth.py on the save dump of game4 (GAMESPEED_MARATHON, HANDICAP_MONARCH); medians per group; growing: cities with a food surplus; cities in disorder left out. Every value counted (5).*

Cities by the food they keep on growth, and the buildings that give food or keep it:

| cities_by_food_kept | cities |
|---|---|
| human, 30 per cent | 13 |
| AI, 20 per cent | 52 |
| AI, 30 per cent | 64 |

*cities at save; who: every player; turn: save; rows counted: 129; source: growth.py: each city's sum of iFoodKept over its buildings, real and free. Every value counted (3).*

| cities_by_food_kept | cities |
|---|---|
| human, 20 per cent | 3 |
| human, 30 per cent | 11 |
| human, 40 per cent | 11 |
| human, 50 per cent | 1 |
| AI, 20 per cent | 67 |
| AI, 30 per cent | 112 |

*cities at save; who: every player; turn: save; rows counted: 205; source: growth.py: each city's sum of iFoodKept over its buildings, real and free. Every value counted (6).*

| building | food_kept_pct | human_cities | ai_cities |
|---|---|---|---|
| CITY_ESSENTIALS | 30 | 13 | 3 |
| IRRIGATION_CANALS | 0 | 10 | 3 |
| TOWN_ESSENTIALS | 30 | 0 | 61 |
| SETTLEMENT_ESSENTIALS | 20 | 0 | 52 |

*cities at save; who: every player; turn: save; rows counted: 129; source: growth.py: buildings with iFoodKept, a food RiverPlotYieldChanges or SeaPlotYieldChanges, or a food YieldModifiers or YieldChanges (BuildingInfo), and the cities holding each, real or free. Every value counted (4).*

| building | food_kept_pct | human_cities | ai_cities |
|---|---|---|---|
| CITY_ESSENTIALS | 30 | 17 | 44 |
| ROMAN_DEPOT | 10 | 13 | 0 |
| IRRIGATION_CANALS | 0 | 9 | 27 |
| TOWN_ESSENTIALS | 30 | 5 | 68 |
| SETTLEMENT_ESSENTIALS | 20 | 4 | 67 |
| PRAEFECTURA_ANNONAE | 10 | 1 | 0 |
| VIKING_TRADING_POST | 0 | 0 | 4 |

*cities at save; who: every player; turn: save; rows counted: 205; source: growth.py: buildings with iFoodKept, a food RiverPlotYieldChanges or SeaPlotYieldChanges, or a food YieldModifiers or YieldChanges (BuildingInfo), and the cities holding each, real or free. Every value counted (7).*

What the tables show:
- **Surplus.** The human's founded cities, and in game 3 its captured ones, have a food surplus
  several times the AIs' ordinary cities'. They grow a citizen in about half the turns, although
  a citizen costs more food at their larger size. The cities captured in game 4's last turns
  are still small and nearly stalled.
- **Food from tiles.** The tiles give the human's cities more food. They work more tiles, and in
  game 4 each farm and river tile yields more, by the tech and canal columns of section 5.4. RoM
  sets `FOOD_CONSUMPTION_PER_POPULATION` to `3`, so every food point above a tile's eater
  counts.
- **Food from elsewhere.** A large part of the human's food does not come from tiles at all.
  - Trade routes give food under Coinage
    (`[25,0,0]` per cent of the route's yield:
    food, hammers, commerce) and hammers under Proletariat
    (`[0,50,0]`).
  - With its many routes per city, that is a large share of the human's food and of its hammers
    (the trade columns).
  - The AIs' economy civics (Coastal, Pastoral, Agricultural) give routes no food and cut their
    commerce, so their trade columns are zero at the median.
  - The rest of the non-tile food is percentage modifiers (Tutors,
    `[10,10,10]`, and in Rome's capital the Praefectura
    Annonae) and specialists.
- **The granary.**
  - The human's founded cities keep `30`
    per cent with City Essentials, and in game 4
    `10` more with the Roman Depot. The Roman
    capital adds the Praefectura Annonae.
  - Most AI cities hold Town or Settlement Essentials.
  - The difference in food kept is modest; the difference in surplus is not.
- **Happiness and health.**
  - The human's cities have a larger happiness margin than the AIs': far larger in game 3, and in
    game 4 for its founded cities and capital. So they can keep growing.
  - Fortification's happiness per military unit (section 6.4) and the large garrison are one
    source.
  - The capital of game 4 is over its health limit (a negative margin), which adds to its
    consumption.
- **Over the game** (section 6.1): in game 4 the human's population per city passes the AI
  median during the development phase; in game 3 only after the war. Its food per city pulls
  away with it.

## 7. War

### 7.1 Whom the human attacks

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

### 7.2 Before the declaration

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

### 7.3 The attacks

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

### 7.4 The peace

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

## 8. Expansion

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

## 9. Parts from the other studies

| Part | Where |
|---|---|
| The capital trains the units; the other cities build | `study/human.md`, section 6, reading 1 |
| The slider follows the sign of gold per turn | `study/human.md`, section 6, reading 2 |
| Workers are directed by hand; the land next to the cities first | `study/operations.md`, section 6 |
| A large part of the workers are captured | `study/operations.md`, section 2.2 |
| Cottages become mines; tiles are re-planned as techs arrive | `study/data.md`, section 5, reading 1 |
| Trade routes per city about twice the AI's | `study/data.md`, section 3 |
| Commerce about doubles at the switch to Coinage, Fiscus and Proletariat | `study/winning.md`, section 7, reading 2 |
| Wars at a power advantage; the AIs barely strike back | `study/winning.md`, section 6 |
| Single units in short steps, converging on the target | `study/operations.md`, section 4 |

## 10. The playstyle

A game in the order it runs. Each step names its facts; the refutation follows each.

1. **Opening, one city.** The capital is the only city through the first phase, as the AIs'
   are (sections 2 and 8). Research goes straight to Slavery, a tech the AIs reach much
   later; Oligarchy and Tribute follow the next turn (section 3.3).
   - Tribute's capital yields, `[25,25,25]`,
     feed the capital that trains the units.
   - Oligarchy's free experience makes every unit trained from then on a veteran.
   - The first worker orders are camps on resources and tracks.
   - *Refuted if:* a further game where the human opens with another government tech.
2. **Development, the longest phase.** The second city comes with the AIs' second. From the third
   on, the cities come faster and denser than the AIs' (section 8).
   - Research follows the economic gateways in a fixed order, and each civic is taken the turn
     it opens (sections 3.3 and 3.4).
   - Every new city gets the same template, in the same order: Town Essentials first, then
     Obelisk and Walls, then Forge, River Port and School of Scribes, then City Essentials,
     Jewellery, the market, Irrigation Canals and the Courthouse (section 4.1). Most of them
     come within a few turns of their tech, and most raise land-unit production, gold or trade
     routes (section 4.3).
   - The workers, few and directed by hand, put farms on river flats, cottages on hills and
     flats, and mines on hills. They work the ring next to each city first (section 5).
   - The capital trains units, which are kept as a cheap garrison (section 6.3).
   - Cheap techs the AIs have are bought in deals; the human's own techs are sold for gold
     (section 3.1; section 6.2).
   - *Refuted if:* in a further game, the human's cities follow different orders of
     buildings, or build them long after their techs.
3. **The economic switch.** Currency is researched and Coinage, Fiscus and Proletariat are
   adopted at once. A switch in a golden age costs no anarchy (section 3.3). Commerce about
   doubles on the same land (`study/winning.md`, reading 2). Courthouses cut maintenance.
   - Coinage and Proletariat also turn every trade route into food and hammers, on top of
     its commerce. With several routes per city, this is a large part of the cities' food
     surplus and production from then on (section 6.5).
   - With City Planning shortly before, City Essentials (the third granary tier) and Irrigation
     Canals (food on every river plot) go into most cities (sections 4.1 and 5.4).
   - *Refuted if:* a replay without the switch reaching the same commerce.
4. **Build-up.** In the turns before a declaration:
   - the military techs arrive and open their units and buildings, used within a turn or two
     (section 3.2);
   - Barracks and Legion Barracks go up in nearly every city the human founded (section 4.1);
   - unit orders rise, and gold built up by income and tech sales pays for mass upgrades of the
     old garrison (sections 6.2, 6.3 and 7.2).
   - The army that results is large, modern and veteran without having been trained at its
     current level (section 6.4).
   - *Refuted if:* a further game where the attacking army is mostly trained new, or the
     upgrades come after the declaration.
5. **Conquest of the nearest neighbour.** The war goes to the AI whose cities are closest, not
   the weakest (section 7.1).
   - The attacks are made at high odds by veterans, in game 1, game 3 and game 4 mostly with one
     unit type (section 7.3).
   - The cities fall within a few turns, and the AIs barely strike back.
   - Undefended workers are taken.
   - The peace is sold for gold, in game 4 (section 7.4).
   - City plunder adds to the gold, which pays for the next upgrades (section 6.2).
   - *Refuted if:* a further game where the human attacks a distant AI while a nearer one is
     open.
6. **After a war: consolidate or go again.** In game 3, a long building phase follows, and
   the leadership civic moves from Oligarchy to Patrician. In game 4, a second, larger campaign
   follows at once, against the next nearest neighbours (sections 2 and 7.1).

What this does not explain:
- the war of game 2 that stays open for most of the game with almost no fighting;
- the low-odds Javelineer attacks of game 2.

## 11. What it implies for the AI

Where the plan meets an AI weakness. Each is a candidate for an AI change, judged only by
experiment (CLAUDE.md, rule 9):
- **The city template.** The AIs build few City Essentials, Courthouses or Forges, the
  buildings that raise production, gold and maintenance in every city (section 4.1).
- **Civic techs.** The AIs neither research Currency nor run its civics (`study/winning.md`,
  reading 3). Their usual economy civics (Coastal, Pastoral, Agricultural) cut trade commerce and
  give routes no food or hammers (section 6.5).
- **Growth.** The AIs' cities have a food surplus several times smaller. Irrigation Canals and
  City Essentials are rare in them, and the yield techs (Mathematics for farms and mines) come
  later (sections 5.4 and 6.5).
- **The upgrade economy.** The human's war-time army is bought with gold upgrades of a cheap
  garrison. An AI that sells techs to the human funds this.
- **Free experience.** Oligarchy and the barracks line are what give the human's units their
  promotions.
- **The nearest neighbour is the target,** and its build-up is visible in the turns before
  (section 7).
- **Workers in reach are taken, and peace is bought** (sections 7.4 and 6.2).

## 12. Open

- **More games.** Most of this rests on game 3 and game 4. Game 1 and game 2 have no M lines
  and no save dump.
- **Unlocks the use table cannot see:** buildings that need a tech through `TechTypes` (in
  RoM, Town Essentials needs Pottery that way) and techs that open later techs.
- **Hurry turns.** In game 4, the turns with a hurry spend more gold than a hurry of a single
  item would. Spending without a command line (for example, group upgrades) is possible and
  would show there.
- **The war of game 2 that stays open.**
- **The few worked plots the yield model misses** without a battle on them (section 5.4).
- **Growth over the game.** The growth model is exact at the save only; the M lines give the
  population and food per city over time, not per city.

## Appendix: XML records of the types counted

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

| BuildingInfo | Fields set (records.json) |
|---|---|
| ARCHERY_RANGE | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_ARCHERY_RANGE; `ConstructSound` AS2D_BUILD_ARCHERY_RANGE; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `ObsoleteTech` TECH_RIFLING; `PrereqTech` TECH_ARCHERY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGGRESSIVE","iProductionTrait":100}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 40; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 3 |
| BARRACKS | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_BARRACKS; `ConstructSound` AS2D_BUILD_BARRACKS; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `PrereqTech` TECH_MILITARY_TRAINING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGGRESSIVE","iProductionTrait":100}]; `UnitCombatFreeExperiences` [{"UnitCombatType":"UNITCOMBAT_MELEE","iExperience":3},{"UnitCombatType":"UNITCOMBAT_RECON","iExperience":3},{"UnitCombatType":"UNITCOMBAT_ANIMAL","iExperience":2},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iExperience":2},{"UnitCombatType":"UNITCOMBAT_SIEGE","iExperience":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 50; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 3 |
| BREWERY | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_BREWERY; `ConstructSound` AS2D_BUILD_BREWERY; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `FreeBonus` BONUS_ALCOHOL; `PrereqBonuses` ["BONUS_APPLE","BONUS_WHEAT","BONUS_RICE","BONUS_SUGAR","BONUS_CORN"]; `PrereqTech` TECH_FERMENTATION; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iCost` 100; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iNumFreeBonuses` -1 |
| BROTHEL | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_BROTHEL; `CommerceHappinesses` [0,0,4]; `CommerceModifiers` [0,0,0,25]; `ConstructSound` AS2D_BUILD_BROTHEL; `Flavors` [{"FlavorType":"FLAVOR_CULTURE","iFlavor":2},{"FlavorType":"FLAVOR_GROWTH","iFlavor":5},{"FlavorType":"FLAVOR_ESPIONAGE","iFlavor":3}]; `PrereqTech` TECH_CURRENCY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_DECEIVER","iProductionTrait":100}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 75; `iDCMAirbombMission` 2; `iHappiness` 5; `iHealth` -3; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| CELTIC_TEMPLE | `Advisor` ADVISOR_RELIGION; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":50}]; `BuildingClass` BUILDINGCLASS_CELTIC_TEMPLE; `ConstructSound` AS2D_BUILD_CONFUCIAN; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":10},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":1}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `PrereqReligion` RELIGION_CELTIC; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SPIRITUAL","iProductionTrait":100}]; `ReligionChanges` [{"ReligionType":"RELIGION_CELTIC","iReligionChange":1}]; `ReligionType` RELIGION_CELTIC; `SpecialBuildingType` SPECIALBUILDING_TEMPLE; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_PRIEST","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 4; `iConquestProb` 20; `iCost` 80; `iDefense` 10; `iExperience` 1; `iHappiness` 1; `iHealRateChange` 10; `iHurryAngerModifier` -25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iWarWearinessModifier` -10 |
| CITY_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_APPLE","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_BANANA","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_LEMON","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_CITY_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_TOWN_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_COURTHOUSE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_STONE","BONUS_MARBLE","BONUS_COPPER","BONUS_IRON","BONUS_LEAD"]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":3}]; `TechTypes` ["TECH_BRONZE_WORKING","TECH_MASONRY","TECH_SAILING","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 30; `iConquestProb` 100; `iCost` 200; `iDCMAirbombMission` 2; `iDefense` 20; `iEspionageDefense` 20; `iFoodKept` 30; `iHappiness` 5; `iHealRateChange` 9; `iHealth` 6; `iMaintenanceModifier` 25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |
| COURIER_SYSTEM | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_HORSE","iProductonModifier":100}]; `BuildingClass` BUILDINGCLASS_COURIER_SYSTEM; `CommerceChangeDoubleTimes` [0,0,1000]; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `GreatPeopleUnitClass` UNITCLASS_GREAT_SPY; `MaxStartEra` ERA_RENAISSANCE; `ObsoleteSafeCommerceChanges` [0,0,4]; `ObsoleteTech` TECH_COMBUSTION; `PrereqTech` TECH_WRITING; `TechTypes` ["TECH_ANIMAL_HUSBANDRY","NONE","NONE","NONE"]; `bNukeImmune` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAllCityDefense` 10; `iAnarchyModifier` -25; `iAsset` 5; `iCost` 200; `iGlobalTradeRoutes` 1; `iGreatGeneralRateModifier` 10; `iGreatPeopleRateChange` 1; `iGreatPeopleRateModifier` 10; `iHurryCostModifier` 50; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 10 |
| COURTHOUSE | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_COURTHOUSE; `CommerceChanges` [0,0,0,2]; `ConstructSound` AS2D_BUILD_COURTHOUSE; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_ESPIONAGE","iFlavor":3}]; `FreeStartEra` ERA_MODERN; `PrereqTech` TECH_CODE_OF_LAWS; `ProductionTraits` [{"ProductionTraitType":"TRAIT_ORGANIZED","iProductionTrait":100}]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_SPY","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 120; `iDCMAirbombMission` 2; `iMaintenanceModifier` -25; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| FORGE | `Advisor` ADVISOR_ECONOMY; `BonusYieldModifiers` [{"BonusType":"BONUS_GOLD","YieldModifiers":[0,0,25]},{"BonusType":"BONUS_SILVER","YieldModifiers":[0,0,15]},{"BonusType":"BONUS_GEMS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COPPER","YieldModifiers":[0,25,0]},{"BonusType":"BONUS_IRON","YieldModifiers":[0,25,0]},{"BonusType":"BONUS_LEAD","YieldModifiers":[0,25,0]}]; `BuildingClass` BUILDINGCLASS_FORGE; `ConstructSound` AS2D_BUILD_FORGE; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":10}]; `FreeStartEra` ERA_RENAISSANCE; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_LEAD","BONUS_GOLD","BONUS_SILVER"]; `PrereqTech` TECH_METAL_CASTING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_INDUSTRIOUS","iProductionTrait":100}]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_ENGINEER","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 3; `iHealth` -6; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 5 |
| IRRIGATION_CANALS | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_IRRIGATION_CANALS; `ConstructSound` AS2D_BUILD_AQUEDUCT; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGRICULTURAL","iProductionTrait":100}]; `RiverPlotYieldChanges` [1,0]; `bRiver` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 90; `iCost` 100; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| JEWELLERY | `Advisor` ADVISOR_ECONOMY; `BonusHappinessChanges` [{"BonusType":"BONUS_GEMS","iHappinessChange":1},{"BonusType":"BONUS_GOLD","iHappinessChange":1},{"BonusType":"BONUS_SILVER","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1}]; `BuildingClass` BUILDINGCLASS_JEWELLERY; `CommerceModifiers` [10]; `ConstructSound` AS2D_BUILD_JEWELLERY; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `ObsoleteTech` TECH_MOTION_PICTURES; `PrereqBonuses` ["BONUS_GOLD","BONUS_SILVER","BONUS_GEMS","BONUS_PEARLS","BONUS_BERNSTEIN"]; `PrereqTech` TECH_METAL_CASTING; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 2; `iTradeRouteModifier` 25 |
| LIBRARY | `Advisor` ADVISOR_SCIENCE; `BuildingClass` BUILDINGCLASS_LIBRARY; `CommerceChangeDoubleTimes` [0,0,1000]; `CommerceModifiers` [0,20]; `ConstructSound` AS2D_BUILD_LIBRARY; `Flavors` [{"FlavorType":"FLAVOR_SCIENCE","iFlavor":15}]; `FreeStartEra` ERA_MODERN; `ObsoleteSafeCommerceChanges` [0,0,2]; `PrereqTech` TECH_LITERATURE; `ProductionTraits` [{"ProductionTraitType":"TRAIT_CREATIVE","iProductionTrait":100}]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_SCIENTIST","iSpecialistCount":2}]; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iCost` 90; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| LIGHTHOUSE | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_LIGHTHOUSE; `ConstructSound` AS2D_BUILD_LIGHTHOUSE; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `FreeStartEra` ERA_MEDIEVAL; `PrereqTech` TECH_SAILING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SEAFARING","iProductionTrait":100}]; `bWater` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 2; `iForeignTradeRouteModifier` 50; `iMaxLatitude` 90; `iMinAreaSize` 10; `iTradeRouteModifier` 25 |
| MARKET | `Advisor` ADVISOR_ECONOMY; `BonusHappinessChanges` [{"BonusType":"BONUS_FUR","iHappinessChange":1},{"BonusType":"BONUS_IVORY","iHappinessChange":1},{"BonusType":"BONUS_SILK","iHappinessChange":1},{"BonusType":"BONUS_WHALE","iHappinessChange":1},{"BonusType":"BONUS_COTTON","iHappinessChange":1},{"BonusType":"BONUS_WINE","iHappinessChange":1},{"BonusType":"BONUS_OLIVES","iHappinessChange":1},{"BonusType":"BONUS_DYE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1}]; `BuildingClass` BUILDINGCLASS_MARKET; `CommerceModifiers` [20]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `FreeStartEra` ERA_INDUSTRIAL; `PrereqBonuses` ["BONUS_BERNSTEIN","BONUS_SILK","BONUS_WINE","BONUS_FUR","BONUS_IVORY"]; `PrereqTech` TECH_TRADE; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":2}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 75; `iCost` 150; `iDCMAirbombMission` 2; `iForeignTradeRouteModifier` 25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRouteModifier` 25 |
| NORDIC_SHRINE | `Advisor` ADVISOR_RELIGION; `BuildingClass` BUILDINGCLASS_NORDIC_SHRINE; `CommerceChangeDoubleTimes` [0,0,100]; `ConstructSound` AS2D_BUILD_OBELISK; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":10},{"FlavorType":"FLAVOR_GOLD","iFlavor":1},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":1}]; `FreeSpecialistCounts` [{"SpecialistType":"SPECIALIST_PRIEST","iFreeSpecialistCount":1}]; `GreatPeopleUnitClass` UNITCLASS_PROPHET; `HolyCity` RELIGION_NORDIC; `MovieDefineTag` ART_DEF_MOVIE_OAK; `ObsoleteSafeCommerceChanges` [0,0,4]; `PrereqTech` TECH_RELIGION_NORDIC; `ReligionChanges` [{"ReligionType":"RELIGION_NORDIC","iReligionChange":2}]; `ReligionType` RELIGION_NORDIC; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 3; `iConquestProb` 100; `iCost` -1; `iGreatPeopleRateChange` 1; `iHappiness` 1; `iHealRateChange` 10; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRouteModifier` 50; `iTradeRoutes` 1 |
| NORDIC_TEMPLE | `Advisor` ADVISOR_RELIGION; `BuildingClass` BUILDINGCLASS_NORDIC_TEMPLE; `ConstructSound` AS2D_BUILD_TAOIST; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":7}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `PrereqReligion` RELIGION_NORDIC; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SPIRITUAL","iProductionTrait":100}]; `ReligionChanges` [{"ReligionType":"RELIGION_NORDIC","iReligionChange":1}]; `ReligionType` RELIGION_NORDIC; `SpecialBuildingType` SPECIALBUILDING_TEMPLE; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_PRIEST","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 4; `iConquestProb` 20; `iCost` 80; `iDefense` 10; `iExperience` 1; `iHappiness` 1; `iHealRateChange` 10; `iHurryAngerModifier` -25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iWarWearinessModifier` -25 |
| OBELISK | `Advisor` ADVISOR_CULTURE; `BuildingClass` BUILDINGCLASS_OBELISK; `CommerceChangeDoubleTimes` [0,0,1000]; `ConstructSound` AS2D_BUILD_OBELISK; `Flavors` [{"FlavorType":"FLAVOR_CULTURE","iFlavor":10}]; `HappinessTraits` [{"HappinessTraitType":"TRAIT_CHARISMATIC","iHappinessTrait":1}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `ObsoleteTech` TECH_ASTRONOMY; `PrereqTech` TECH_MYSTICISM; `bCenterInCity` True; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 30; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| RIVER_PORT | `Advisor` ADVISOR_ECONOMY; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1}]; `BuildingClass` BUILDINGCLASS_RIVER_PORT; `ConstructSound` AS2D_BUILD_RIVER_PORT; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `ObsoleteTech` TECH_RAILROAD; `PrereqTech` TECH_SAILING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":100}]; `bRiver` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 100; `iCost` 70; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRouteModifier` 20; `iTradeRoutes` 1 |
| SCHOOL_OF_SCRIBES | `Advisor` ADVISOR_SCIENCE; `BuildingClass` BUILDINGCLASS_SCHOOL_OF_SCRIBES; `CommerceChangeDoubleTimes` [0,0,1000]; `CommerceModifiers` [0,15]; `ConstructSound` AS2D_BUILD_LIBRARY; `Flavors` [{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `ObsoleteTech` TECH_PRINTING_PRESS; `PrereqTech` TECH_WRITING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SCIENTIFIC","iProductionTrait":100}]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_SCIENTIST","iSpecialistCount":1}]; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iCost` 60; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| TOWN_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_TOWN_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_SETTLEMENT_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_SALT","BONUS_BERNSTEIN","BONUS_FUR","BONUS_STONE","BONUS_MARBLE"]; `PrereqTech` TECH_MASONRY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":1}]; `TechTypes` ["TECH_POTTERY","NONE","NONE","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 16; `iConquestProb` 100; `iCost` 70; `iDCMAirbombMission` 2; `iDefense` 10; `iEspionageDefense` 10; `iFoodKept` 30; `iHappiness` 3; `iHealRateChange` 6; `iHealth` 3; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |
| TREASURY | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_TREASURY; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_PALACE","bNeededInCity":true}]; `CommerceModifiers` [10]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `GlobalCommerceModifiers` [10]; `MovieDefineTag` ART_DEF_MOVIE_TREASURY; `PrereqTech` TECH_MONARCHY; `bNeverCapture` True; `fVisibilityPriority` 100.0; `iAdvancedStartCost` -1; `iAsset` 3; `iCitiesPrereq` 4; `iCost` 150; `iHurryCostModifier` 100; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| WALLS | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":100}]; `BuildingClass` BUILDINGCLASS_WALLS; `CommerceChanges` [0,0,1]; `ConstructSound` AS2D_BUILD_WALLS; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `ObsoleteTech` TECH_RIFLING; `PrereqTech` TECH_MASONRY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_PROTECTIVE","iProductionTrait":100}]; `bCenterInCity` True; `fVisibilityPriority` 1000.0; `iAdvancedStartCost` 100; `iAsset` 1; `iBombardDefense` 20; `iConquestProb` 20; `iCost` 50; `iDCMAirbombMission` 2; `iDefense` 30; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 2 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| BuildingInfo | Fields set (records.json) |
|---|---|
| BARRACKS | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_BARRACKS; `ConstructSound` AS2D_BUILD_BARRACKS; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `PrereqTech` TECH_MILITARY_TRAINING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGGRESSIVE","iProductionTrait":100}]; `UnitCombatFreeExperiences` [{"UnitCombatType":"UNITCOMBAT_MELEE","iExperience":3},{"UnitCombatType":"UNITCOMBAT_RECON","iExperience":3},{"UnitCombatType":"UNITCOMBAT_ANIMAL","iExperience":2},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iExperience":2},{"UnitCombatType":"UNITCOMBAT_SIEGE","iExperience":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 50; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 3 |
| BREWERY | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_BREWERY; `ConstructSound` AS2D_BUILD_BREWERY; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `FreeBonus` BONUS_ALCOHOL; `PrereqBonuses` ["BONUS_APPLE","BONUS_WHEAT","BONUS_RICE","BONUS_SUGAR","BONUS_CORN"]; `PrereqTech` TECH_FERMENTATION; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iCost` 100; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iNumFreeBonuses` -1 |
| CITY_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_APPLE","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_BANANA","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_LEMON","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_CITY_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_TOWN_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_COURTHOUSE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_STONE","BONUS_MARBLE","BONUS_COPPER","BONUS_IRON","BONUS_LEAD"]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":3}]; `TechTypes` ["TECH_BRONZE_WORKING","TECH_MASONRY","TECH_SAILING","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 30; `iConquestProb` 100; `iCost` 200; `iDCMAirbombMission` 2; `iDefense` 20; `iEspionageDefense` 20; `iFoodKept` 30; `iHappiness` 5; `iHealRateChange` 9; `iHealth` 6; `iMaintenanceModifier` 25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |
| COLOSSEUM | `Advisor` ADVISOR_ECONOMY; `Bonus` BONUS_STONE; `BuildingClass` BUILDINGCLASS_COLOSSEUM; `CommerceChanges` [0,0,2]; `ConstructSound` AS2D_BUILD_COLOSSEUM; `GreatPeopleUnitClass` UNITCLASS_ENGINEER; `ObsoleteTech` TECH_REALISM; `PrereqTech` TECH_CONSTRUCTION; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `TechTypes` ["TECH_ROMAN"]; `bNoUnhappiness` True; `fVisibilityPriority` 1.0; `iAIWeight` 1; `iAdvancedStartCost` 100; `iAsset` 12; `iConquestProb` 100; `iCost` 300; `iDCMAirbombMission` 2; `iGreatPeopleRateChange` 3; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| COURIER_SYSTEM | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_HORSE","iProductonModifier":100}]; `BuildingClass` BUILDINGCLASS_COURIER_SYSTEM; `CommerceChangeDoubleTimes` [0,0,1000]; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `GreatPeopleUnitClass` UNITCLASS_GREAT_SPY; `MaxStartEra` ERA_RENAISSANCE; `ObsoleteSafeCommerceChanges` [0,0,4]; `ObsoleteTech` TECH_COMBUSTION; `PrereqTech` TECH_WRITING; `TechTypes` ["TECH_ANIMAL_HUSBANDRY","NONE","NONE","NONE"]; `bNukeImmune` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAllCityDefense` 10; `iAnarchyModifier` -25; `iAsset` 5; `iCost` 200; `iGlobalTradeRoutes` 1; `iGreatGeneralRateModifier` 10; `iGreatPeopleRateChange` 1; `iGreatPeopleRateModifier` 10; `iHurryCostModifier` 50; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 10 |
| COURTHOUSE | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_COURTHOUSE; `CommerceChanges` [0,0,0,2]; `ConstructSound` AS2D_BUILD_COURTHOUSE; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10},{"FlavorType":"FLAVOR_ESPIONAGE","iFlavor":3}]; `FreeStartEra` ERA_MODERN; `PrereqTech` TECH_CODE_OF_LAWS; `ProductionTraits` [{"ProductionTraitType":"TRAIT_ORGANIZED","iProductionTrait":100}]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_SPY","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 120; `iDCMAirbombMission` 2; `iMaintenanceModifier` -25; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| EARLY_BARRACKS | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_EARLY_BARRACKS; `ConstructSound` AS2D_BUILD_BARRACKS; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `ObsoleteTech` TECH_SMITHING; `PrereqTech` TECH_BRONZE_WORKING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGGRESSIVE","iProductionTrait":100}]; `TechTypes` ["TECH_ROMAN"]; `UnitCombatFreeExperiences` [{"UnitCombatType":"UNITCOMBAT_MELEE","iExperience":3},{"UnitCombatType":"UNITCOMBAT_RECON","iExperience":3},{"UnitCombatType":"UNITCOMBAT_ANIMAL","iExperience":2},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iExperience":2},{"UnitCombatType":"UNITCOMBAT_SIEGE","iExperience":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 40; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMilitaryProductionModifier` 25; `iMinAreaSize` -1; `iPower` 2 |
| FORGE | `Advisor` ADVISOR_ECONOMY; `BonusYieldModifiers` [{"BonusType":"BONUS_GOLD","YieldModifiers":[0,0,25]},{"BonusType":"BONUS_SILVER","YieldModifiers":[0,0,15]},{"BonusType":"BONUS_GEMS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COPPER","YieldModifiers":[0,25,0]},{"BonusType":"BONUS_IRON","YieldModifiers":[0,25,0]},{"BonusType":"BONUS_LEAD","YieldModifiers":[0,25,0]}]; `BuildingClass` BUILDINGCLASS_FORGE; `ConstructSound` AS2D_BUILD_FORGE; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":10}]; `FreeStartEra` ERA_RENAISSANCE; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_LEAD","BONUS_GOLD","BONUS_SILVER"]; `PrereqTech` TECH_METAL_CASTING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_INDUSTRIOUS","iProductionTrait":100}]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_ENGINEER","iSpecialistCount":1}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 3; `iHealth` -6; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 5 |
| FORUM_ROMANUM | `Advisor` ADVISOR_ECONOMY; `Bonus` BONUS_MARBLE; `BuildingClass` BUILDINGCLASS_FORUM_ROMANUM; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_PALACE","bNeededInCity":true}]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":10}]; `MovieDefineTag` ART_DEF_MOVIE_FORUM_ROMANUM; `ObsoleteSafeCommerceChanges` [0,0,10]; `PrereqReligion` RELIGION_HELLENISM; `PrereqTech` TECH_CONSTRUCTION; `TechTypes` ["TECH_ROMAN"]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 6; `iConquestProb` 100; `iCost` 300; `iFreeSpecialist` 1; `iGoldenAgeModifier` 50; `iGreatPeopleRateModifier` 25; `iHappiness` 1; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 3 |
| HELLENIC_CATHEDRAL | `Advisor` ADVISOR_RELIGION; `BonusHappinessChanges` [{"BonusType":"BONUS_INCENSE","iHappinessChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":100},{"BonusType":"BONUS_MARBLE","iProductonModifier":15}]; `BuildingClass` BUILDINGCLASS_HELLENIC_CATHEDRAL; `CommerceModifiers` [0,0,50]; `ConstructSound` AS2D_BUILD_CHRISTIAN; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":10}]; `PrereqBuildingClasses` [{"BuildingClassType":"BUILDINGCLASS_HELLENIC_TEMPLE","iNumBuildingNeeded":2}]; `PrereqReligion` RELIGION_HELLENISM; `ReligionChanges` [{"ReligionType":"RELIGION_HELLENISM","iReligionChange":3}]; `ReligionType` RELIGION_HELLENISM; `SpecialBuildingType` SPECIALBUILDING_PANTHEON; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_PRIEST","iSpecialistCount":2}]; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 6; `iCost` 300; `iMaxLatitude` 90; `iMinAreaSize` -1; `iStateReligionHappiness` 2 |
| HELLENIC_TEMPLE | `Advisor` ADVISOR_RELIGION; `BuildingClass` BUILDINGCLASS_HELLENIC_TEMPLE; `CommerceChangeDoubleTimes` [0,0,1000]; `ConstructSound` AS2D_BUILD_CHRISTIAN; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":10}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `PrereqReligion` RELIGION_HELLENISM; `ReligionChanges` [{"ReligionType":"RELIGION_HELLENISM","iReligionChange":1}]; `ReligionType` RELIGION_HELLENISM; `SpecialBuildingType` SPECIALBUILDING_TEMPLE; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_PRIEST","iSpecialistCount":1}]; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 4; `iCost` 80; `iMaxLatitude` 90; `iMinAreaSize` -1; `iStateReligionHappiness` 2 |
| HIGH_WALLS | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":100}]; `BuildingClass` BUILDINGCLASS_HIGH_WALLS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_WALLS","bNeededInCity":true}]; `CommerceChanges` [0,0,1]; `ConstructSound` AS2D_BUILD_WALLS; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `ObsoleteTech` TECH_RIFLING; `PrereqTech` TECH_SIEGE_WARFARE; `ProductionTraits` [{"ProductionTraitType":"TRAIT_PROTECTIVE","iProductionTrait":100}]; `bCenterInCity` True; `fVisibilityPriority` 1000.0; `iAdvancedStartCost` 100; `iAsset` 1; `iBombardDefense` 40; `iConquestProb` 30; `iCost` 100; `iDCMAirbombMission` 2; `iDefense` 50; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 2 |
| IRRIGATION_CANALS | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_IRRIGATION_CANALS; `ConstructSound` AS2D_BUILD_AQUEDUCT; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGRICULTURAL","iProductionTrait":100}]; `RiverPlotYieldChanges` [1,0]; `bRiver` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 90; `iCost` 100; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| JEWELLERY | `Advisor` ADVISOR_ECONOMY; `BonusHappinessChanges` [{"BonusType":"BONUS_GEMS","iHappinessChange":1},{"BonusType":"BONUS_GOLD","iHappinessChange":1},{"BonusType":"BONUS_SILVER","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1}]; `BuildingClass` BUILDINGCLASS_JEWELLERY; `CommerceModifiers` [10]; `ConstructSound` AS2D_BUILD_JEWELLERY; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `ObsoleteTech` TECH_MOTION_PICTURES; `PrereqBonuses` ["BONUS_GOLD","BONUS_SILVER","BONUS_GEMS","BONUS_PEARLS","BONUS_BERNSTEIN"]; `PrereqTech` TECH_METAL_CASTING; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 2; `iTradeRouteModifier` 25 |
| LEGION_BARRACKS | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_LEGION_BARRACKS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_BARRACKS","bNeededInCity":true}]; `ConstructSound` AS2D_BUILD_BARRACKS; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `ObsoleteTech` TECH_GUNPOWDER; `PrereqTech` TECH_SIEGE_WARFARE; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `TechTypes` ["TECH_ROMAN","TECH_IRON_WORKING"]; `UnitCombatFreeExperiences` [{"UnitCombatType":"UNITCOMBAT_MELEE","iExperience":10},{"UnitCombatType":"UNITCOMBAT_RECON","iExperience":3},{"UnitCombatType":"UNITCOMBAT_ANIMAL","iExperience":2},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iExperience":2},{"UnitCombatType":"UNITCOMBAT_SIEGE","iExperience":1}]; `fVisibilityPriority` 1.0; `iAIWeight` 10; `iAdvancedStartCost` 100; `iAsset` 4; `iCost` 60; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMilitaryProductionModifier` 25; `iMinAreaSize` -1; `iPower` 10 |
| LIGHTHOUSE | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_LIGHTHOUSE; `ConstructSound` AS2D_BUILD_LIGHTHOUSE; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `FreeStartEra` ERA_MEDIEVAL; `PrereqTech` TECH_SAILING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SEAFARING","iProductionTrait":100}]; `bWater` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 2; `iForeignTradeRouteModifier` 50; `iMaxLatitude` 90; `iMinAreaSize` 10; `iTradeRouteModifier` 25 |
| MARS_TEMPLE | `Advisor` ADVISOR_RELIGION; `BuildingClass` BUILDINGCLASS_MARS_TEMPLE; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_HELLENIC_TEMPLE","bNeededInCity":true}]; `CommerceChangeDoubleTimes` [0,0,1000]; `ConstructSound` AS2D_BUILD_CHRISTIAN; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":5},{"FlavorType":"FLAVOR_RELIGION","iFlavor":5}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `PrereqReligion` RELIGION_HELLENISM; `PrereqTech` TECH_ROMAN; `ReligionChanges` [{"ReligionType":"RELIGION_HELLENISM","iReligionChange":1}]; `ReligionType` RELIGION_HELLENISM; `SpecialBuildingType` SPECIALBUILDING_TEMPLE; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_PRIEST","iSpecialistCount":1}]; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 4; `iCost` 200; `iDefense` 10; `iExperience` 3; `iMaxLatitude` 90; `iMilitaryProductionModifier` 10; `iMinAreaSize` -1; `iStateReligionHappiness` 2 |
| OBELISK | `Advisor` ADVISOR_CULTURE; `BuildingClass` BUILDINGCLASS_OBELISK; `CommerceChangeDoubleTimes` [0,0,1000]; `ConstructSound` AS2D_BUILD_OBELISK; `Flavors` [{"FlavorType":"FLAVOR_CULTURE","iFlavor":10}]; `HappinessTraits` [{"HappinessTraitType":"TRAIT_CHARISMATIC","iHappinessTrait":1}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `ObsoleteTech` TECH_ASTRONOMY; `PrereqTech` TECH_MYSTICISM; `bCenterInCity` True; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 30; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| PORT | `Advisor` ADVISOR_ECONOMY; `BonusHappinessChanges` [{"BonusType":"BONUS_FUR","iHappinessChange":1},{"BonusType":"BONUS_SILK","iHappinessChange":1},{"BonusType":"BONUS_WINE","iHappinessChange":1},{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_CLAM","iHealthChange":1},{"BonusType":"BONUS_CRAB","iHealthChange":1},{"BonusType":"BONUS_FISH","iHealthChange":1},{"BonusType":"BONUS_SHRIMP","iHealthChange":1}]; `BuildingClass` BUILDINGCLASS_PORT; `CommerceChangeDoubleTimes` [0,0,1000]; `ConstructSound` AS2D_BUILD_PORT; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `FreeStartEra` ERA_INDUSTRIAL; `ObsoleteSafeCommerceChanges` [0,0,1]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":100}]; `TechTypes` ["TECH_SEAFARING","NONE","NONE","NONE"]; `bWater` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 100; `iCost` 100; `iDCMAirbombMission` 2; `iForeignTradeRouteModifier` 25; `iHealth` -1; `iMaxLatitude` 90; `iMinAreaSize` 10; `iTradeRouteModifier` 50; `iTradeRoutes` 3 |
| PRAEFECTUR | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_PRAEFECTUR; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_COURTHOUSE","bNeededInCity":true}]; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":6}]; `FreeSpecialistCounts` [{"SpecialistType":"SPECIALIST_NOBLE","iFreeSpecialistCount":1}]; `PrereqBuildingClasses` [{"BuildingClassType":"BUILDINGCLASS_COURTHOUSE","iNumBuildingNeeded":4}]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_ORGANIZED","iProductionTrait":100}]; `TechTypes` ["TECH_CODE_OF_LAWS","TECH_ROMAN"]; `bGovernmentCenter` True; `bNeverCapture` True; `bNukeImmune` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 8; `iCost` 200; `iHurryCostModifier` 50; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| PRAEFECTURA_ANNONAE | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_PRAEFECTURA_ANNONAE; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_PALACE","bNeededInCity":true}]; `ConstructSound` AS2D_BUILD_GRANARY; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":5}]; `ObsoleteTech` TECH_INDUSTRIALISM; `PrereqTech` TECH_CODE_OF_LAWS; `ProductionTraits` [{"ProductionTraitType":"TRAIT_ORGANIZED","iProductionTrait":100}]; `TechTypes` ["TECH_ROMAN"]; `YieldModifiers` [25,10,0]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 20; `iCost` 100; `iDCMAirbombMission` 2; `iFoodKept` 10; `iFreeSpecialist` 1; `iMaintenanceModifier` -10; `iMaxLatitude` 90; `iMinAreaSize` -1; `iWarWearinessModifier` -10 |
| RIVER_PORT | `Advisor` ADVISOR_ECONOMY; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1}]; `BuildingClass` BUILDINGCLASS_RIVER_PORT; `ConstructSound` AS2D_BUILD_RIVER_PORT; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `ObsoleteTech` TECH_RAILROAD; `PrereqTech` TECH_SAILING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_EXPANSIVE","iProductionTrait":100}]; `bRiver` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 100; `iCost` 70; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRouteModifier` 20; `iTradeRoutes` 1 |
| ROMAN_DEPOT | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_ROMAN_DEPOT; `ConstructSound` AS2D_BUILD_GRANARY; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":5}]; `ObsoleteTech` TECH_INDUSTRIALISM; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_ORGANIZED","iProductionTrait":100}]; `TechTypes` ["TECH_ROMAN"]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 60; `iDCMAirbombMission` 2; `iDefense` 10; `iFoodKept` 10; `iHealRateChange` 30; `iHealth` 2; `iMaxLatitude` 90; `iMilitaryProductionModifier` 10; `iMinAreaSize` -1; `iPower` 5; `iWarWearinessModifier` -10 |
| ROMAN_FORUM | `Advisor` ADVISOR_ECONOMY; `BonusHappinessChanges` [{"BonusType":"BONUS_FUR","iHappinessChange":1},{"BonusType":"BONUS_IVORY","iHappinessChange":1},{"BonusType":"BONUS_SILK","iHappinessChange":1},{"BonusType":"BONUS_WHALE","iHappinessChange":1},{"BonusType":"BONUS_COTTON","iHappinessChange":1},{"BonusType":"BONUS_WINE","iHappinessChange":1},{"BonusType":"BONUS_OLIVES","iHappinessChange":1},{"BonusType":"BONUS_DYE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1}]; `BuildingClass` BUILDINGCLASS_MARKET; `CommerceModifiers` [25]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `FreeStartEra` ERA_INDUSTRIAL; `PrereqBonuses` ["BONUS_MARBLE","BONUS_WINE","BONUS_SILK","BONUS_OLIVES","BONUS_DYE"]; `PrereqTech` TECH_TRADE; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":2}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 4; `iConquestProb` 75; `iCost` 150; `iDCMAirbombMission` 2; `iForeignTradeRouteModifier` 40; `iGreatPeopleRateModifier` 25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRouteModifier` 30 |
| SCHOOL_OF_SCRIBES | `Advisor` ADVISOR_SCIENCE; `BuildingClass` BUILDINGCLASS_SCHOOL_OF_SCRIBES; `CommerceChangeDoubleTimes` [0,0,1000]; `CommerceModifiers` [0,15]; `ConstructSound` AS2D_BUILD_LIBRARY; `Flavors` [{"FlavorType":"FLAVOR_SCIENCE","iFlavor":10}]; `ObsoleteSafeCommerceChanges` [0,0,1]; `ObsoleteTech` TECH_PRINTING_PRESS; `PrereqTech` TECH_WRITING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SCIENTIFIC","iProductionTrait":100}]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_SCIENTIST","iSpecialistCount":1}]; `bNeverCapture` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iCost` 60; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| SCOTLAND_YARD | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_SCOTLAND_YARD; `CommerceModifiers` [0,0,0,100]; `Flavors` [{"FlavorType":"FLAVOR_ESPIONAGE","iFlavor":10}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 8; `iConquestProb` 100; `iCost` -1; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 8 |
| SENATE | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_SENATE; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_PALACE","bNeededInCity":true}]; `CommerceModifiers` [0,0,5,10]; `ConstructSound` AS2D_BUILD_AGORA; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10},{"FlavorType":"FLAVOR_CULTURE","iFlavor":5},{"FlavorType":"FLAVOR_ESPIONAGE","iFlavor":5}]; `GreatPeopleUnitClass` UNITCLASS_GREAT_SPY; `ObsoleteTech` TECH_LEADERSHIP; `PrereqTech` TECH_CODE_OF_LAWS; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_SPY","iSpecialistCount":3}]; `TechTypes` ["TECH_ROMAN"]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 15; `iCost` 300; `iGreatPeopleRateChange` 10; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 2 |
| SHIPYARD | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_SHIPYARD; `ConstructSound` AS2D_BUILD_DRYDOCK; `DomainProductionModifiers` [{"DomainType":"DOMAIN_SEA","iProductionModifier":50}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":10}]; `PrereqTech` TECH_SHIP_BUILDING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SEAFARING","iProductionTrait":100}]; `bWater` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 1; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 3; `iHealth` -1; `iMaxLatitude` 90; `iMinAreaSize` 20; `iPower` 2 |
| SIEGE_WORKSHOP | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_SIEGE_WORKSHOP; `ConstructSound` AS2D_BUILD_SIEGE_WORKSHOP; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `ObsoleteTech` TECH_ARTILLERY; `PrereqTech` TECH_SIEGE_WARFARE; `UnitCombatFreeExperiences` [{"UnitCombatType":"UNITCOMBAT_ARCHER","iExperience":3},{"UnitCombatType":"UNITCOMBAT_SIEGE","iExperience":2}]; `fVisibilityPriority` 1.0; `iAIWeight` 300; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 100; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 3 |
| STABLE | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_STABLE; `ConstructSound` AS2D_BUILD_STABLE; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `FreeBonus` BONUS_HORSE; `ObsoleteTech` TECH_VERTICAL_FLIGHT; `PrereqBonuses` ["BONUS_HORSE","BONUS_IVORY","NONE","NONE","NONE"]; `PrereqTech` TECH_CHARIOTRY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_NOMAD","iProductionTrait":100}]; `UnitCombatFreeExperiences` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iExperience":2}]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 60; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1; `iNumFreeBonuses` 1; `iPower` 2 |
| STATUE_OF_ZEUS | `Advisor` ADVISOR_RELIGION; `BuildingClass` BUILDINGCLASS_STATUE_OF_ZEUS; `CommerceChangeDoubleTimes` [0,0,1000]; `CommerceChangeOriginalOwners` [false,false,true]; `Flavors` [{"FlavorType":"FLAVOR_RELIGION","iFlavor":10}]; `GlobalReligionCommerce` RELIGION_HELLENISM; `GreatPeopleUnitClass` UNITCLASS_PROPHET; `HolyCity` RELIGION_HELLENISM; `MovieDefineTag` ART_DEF_MOVIE_STATUE_OF_ZEUS; `ObsoleteSafeCommerceChanges` [0,0,10]; `ReligionChanges` [{"ReligionType":"RELIGION_HELLENISM","iReligionChange":1}]; `ReligionType` RELIGION_HELLENISM; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_PRIEST","iSpecialistCount":3}]; `bNukeImmune` True; `bTeamShare` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` -1; `iAsset` 8; `iConquestProb` 100; `iCost` -1; `iEnemyWarWearinessModifier` 100; `iGreatPeopleRateChange` 2; `iHurryCostModifier` 50; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 4 |
| TOWN_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_TOWN_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_SETTLEMENT_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_SALT","BONUS_BERNSTEIN","BONUS_FUR","BONUS_STONE","BONUS_MARBLE"]; `PrereqTech` TECH_MASONRY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":1}]; `TechTypes` ["TECH_POTTERY","NONE","NONE","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 16; `iConquestProb` 100; `iCost` 70; `iDCMAirbombMission` 2; `iDefense` 10; `iEspionageDefense` 10; `iFoodKept` 30; `iHappiness` 3; `iHealRateChange` 6; `iHealth` 3; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |
| TREASURY | `Advisor` ADVISOR_ECONOMY; `BuildingClass` BUILDINGCLASS_TREASURY; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_PALACE","bNeededInCity":true}]; `CommerceModifiers` [10]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `Flavors` [{"FlavorType":"FLAVOR_GOLD","iFlavor":10}]; `GlobalCommerceModifiers` [10]; `MovieDefineTag` ART_DEF_MOVIE_TREASURY; `PrereqTech` TECH_MONARCHY; `bNeverCapture` True; `fVisibilityPriority` 100.0; `iAdvancedStartCost` -1; `iAsset` 3; `iCitiesPrereq` 4; `iCost` 150; `iHurryCostModifier` 100; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| WALLS | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_STONE","iProductonModifier":100}]; `BuildingClass` BUILDINGCLASS_WALLS; `CommerceChanges` [0,0,1]; `ConstructSound` AS2D_BUILD_WALLS; `Flavors` [{"FlavorType":"FLAVOR_MILITARY","iFlavor":10}]; `ObsoleteTech` TECH_RIFLING; `PrereqTech` TECH_MASONRY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_PROTECTIVE","iProductionTrait":100}]; `bCenterInCity` True; `fVisibilityPriority` 1000.0; `iAdvancedStartCost` 100; `iAsset` 1; `iBombardDefense` 20; `iConquestProb` 20; `iCost` 50; `iDCMAirbombMission` 2; `iDefense` 30; `iMaxLatitude` 90; `iMinAreaSize` -1; `iPower` 2 |

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

| BuildingInfo | Fields set (records.json) |
|---|---|
| CITY_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_APPLE","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_BANANA","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_LEMON","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_CITY_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_TOWN_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_COURTHOUSE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_STONE","BONUS_MARBLE","BONUS_COPPER","BONUS_IRON","BONUS_LEAD"]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":3}]; `TechTypes` ["TECH_BRONZE_WORKING","TECH_MASONRY","TECH_SAILING","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 30; `iConquestProb` 100; `iCost` 200; `iDCMAirbombMission` 2; `iDefense` 20; `iEspionageDefense` 20; `iFoodKept` 30; `iHappiness` 5; `iHealRateChange` 9; `iHealth` 6; `iMaintenanceModifier` 25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |
| IRRIGATION_CANALS | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_IRRIGATION_CANALS; `ConstructSound` AS2D_BUILD_AQUEDUCT; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGRICULTURAL","iProductionTrait":100}]; `RiverPlotYieldChanges` [1,0]; `bRiver` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 90; `iCost` 100; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| SETTLEMENT_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1}]; `BonusYieldModifiers` [{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]}]; `BuildingClass` BUILDINGCLASS_SETTLEMENT_ESSENTIALS; `ConstructSound` AS2D_BUILD_BUTCHERY; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `FreeStartEra` ERA_ANCIENT; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 10; `iConquestProb` 100; `iCost` 10; `iDCMAirbombMission` 2; `iFoodKept` 20; `iHealRateChange` 3; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| TOWN_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_TOWN_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_SETTLEMENT_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_SALT","BONUS_BERNSTEIN","BONUS_FUR","BONUS_STONE","BONUS_MARBLE"]; `PrereqTech` TECH_MASONRY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":1}]; `TechTypes` ["TECH_POTTERY","NONE","NONE","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 16; `iConquestProb` 100; `iCost` 70; `iDCMAirbombMission` 2; `iDefense` 10; `iEspionageDefense` 10; `iFoodKept` 30; `iHappiness` 3; `iHealRateChange` 6; `iHealth` 3; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| BuildingInfo | Fields set (records.json) |
|---|---|
| CITY_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_APPLE","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_BANANA","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_LEMON","YieldModifiers":[0,0,5]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_CITY_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_TOWN_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_COURTHOUSE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_STONE","BONUS_MARBLE","BONUS_COPPER","BONUS_IRON","BONUS_LEAD"]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":3}]; `TechTypes` ["TECH_BRONZE_WORKING","TECH_MASONRY","TECH_SAILING","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 30; `iConquestProb` 100; `iCost` 200; `iDCMAirbombMission` 2; `iDefense` 20; `iEspionageDefense` 20; `iFoodKept` 30; `iHappiness` 5; `iHealRateChange` 9; `iHealth` 6; `iMaintenanceModifier` 25; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |
| IRRIGATION_CANALS | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_IRRIGATION_CANALS; `ConstructSound` AS2D_BUILD_AQUEDUCT; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_AGRICULTURAL","iProductionTrait":100}]; `RiverPlotYieldChanges` [1,0]; `bRiver` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 90; `iCost` 100; `iDCMAirbombMission` 2; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| PRAEFECTURA_ANNONAE | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_PRAEFECTURA_ANNONAE; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_PALACE","bNeededInCity":true}]; `ConstructSound` AS2D_BUILD_GRANARY; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":5}]; `ObsoleteTech` TECH_INDUSTRIALISM; `PrereqTech` TECH_CODE_OF_LAWS; `ProductionTraits` [{"ProductionTraitType":"TRAIT_ORGANIZED","iProductionTrait":100}]; `TechTypes` ["TECH_ROMAN"]; `YieldModifiers` [25,10,0]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 20; `iCost` 100; `iDCMAirbombMission` 2; `iFoodKept` 10; `iFreeSpecialist` 1; `iMaintenanceModifier` -10; `iMaxLatitude` 90; `iMinAreaSize` -1; `iWarWearinessModifier` -10 |
| ROMAN_DEPOT | `Advisor` ADVISOR_MILITARY; `BuildingClass` BUILDINGCLASS_ROMAN_DEPOT; `ConstructSound` AS2D_BUILD_GRANARY; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":5}]; `ObsoleteTech` TECH_INDUSTRIALISM; `PrereqTech` TECH_CITY_PLANNING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_ORGANIZED","iProductionTrait":100}]; `TechTypes` ["TECH_ROMAN"]; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 2; `iCost` 60; `iDCMAirbombMission` 2; `iDefense` 10; `iFoodKept` 10; `iHealRateChange` 30; `iHealth` 2; `iMaxLatitude` 90; `iMilitaryProductionModifier` 10; `iMinAreaSize` -1; `iPower` 5; `iWarWearinessModifier` -10 |
| SETTLEMENT_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1}]; `BonusYieldModifiers` [{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]}]; `BuildingClass` BUILDINGCLASS_SETTLEMENT_ESSENTIALS; `ConstructSound` AS2D_BUILD_BUTCHERY; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":2},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `FreeStartEra` ERA_ANCIENT; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 10; `iConquestProb` 100; `iCost` 10; `iDCMAirbombMission` 2; `iFoodKept` 20; `iHealRateChange` 3; `iMaxLatitude` 90; `iMinAreaSize` -1 |
| TOWN_ESSENTIALS | `Advisor` ADVISOR_GROWTH; `BonusHappinessChanges` [{"BonusType":"BONUS_ALCOHOL","iHappinessChange":1},{"BonusType":"BONUS_PEARLS","iHappinessChange":1},{"BonusType":"BONUS_TEA","iHappinessChange":1},{"BonusType":"BONUS_COFFEE","iHappinessChange":1},{"BonusType":"BONUS_BERNSTEIN","iHappinessChange":1},{"BonusType":"BONUS_FUR","iHappinessChange":1}]; `BonusHealthChanges` [{"BonusType":"BONUS_SALT","iHealthChange":1},{"BonusType":"BONUS_CORN","iHealthChange":1},{"BonusType":"BONUS_RICE","iHealthChange":1},{"BonusType":"BONUS_WHEAT","iHealthChange":1},{"BonusType":"BONUS_POTATO","iHealthChange":1},{"BonusType":"BONUS_INCENSE","iHealthChange":1},{"BonusType":"BONUS_TEA","iHealthChange":1}]; `BonusProductionModifiers` [{"BonusType":"BONUS_MARBLE","iProductonModifier":25},{"BonusType":"BONUS_STONE","iProductonModifier":25}]; `BonusYieldModifiers` [{"BonusType":"BONUS_WHEAT","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CORN","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_RICE","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_POTATO","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_DEER","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_COW","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_PIG","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHEEP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_FISH","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_CLAM","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_SHRIMP","YieldModifiers":[3,0,0]},{"BonusType":"BONUS_IVORY","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SILK","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_SPICES","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_PEARLS","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_ALCOHOL","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_BERNSTEIN","YieldModifiers":[0,0,4]},{"BonusType":"BONUS_COFFEE","YieldModifiers":[0,20,10]},{"BonusType":"BONUS_TEA","YieldModifiers":[0,10,4]},{"BonusType":"BONUS_SALT","YieldModifiers":[0,10,0]},{"BonusType":"BONUS_WINE","YieldModifiers":[0,0,4]}]; `BuildingClass` BUILDINGCLASS_TOWN_ESSENTIALS; `BuildingClassNeededs` [{"BuildingClassType":"BUILDINGCLASS_SETTLEMENT_ESSENTIALS","bNeededInCity":true}]; `CommerceModifiers` [15]; `ConstructSound` AS2D_BUILD_MARKETPLACE; `DomainProductionModifiers` [{"DomainType":"DOMAIN_LAND","iProductionModifier":15}]; `Flavors` [{"FlavorType":"FLAVOR_PRODUCTION","iFlavor":6},{"FlavorType":"FLAVOR_GOLD","iFlavor":8},{"FlavorType":"FLAVOR_SCIENCE","iFlavor":4},{"FlavorType":"FLAVOR_MILITARY","iFlavor":4},{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `PrereqBonuses` ["BONUS_SALT","BONUS_BERNSTEIN","BONUS_FUR","BONUS_STONE","BONUS_MARBLE"]; `PrereqTech` TECH_MASONRY; `ProductionTraits` [{"ProductionTraitType":"TRAIT_IMPERIALIST","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `SpecialistCounts` [{"SpecialistType":"SPECIALIST_MERCHANT","iSpecialistCount":1}]; `TechTypes` ["TECH_POTTERY","NONE","NONE","NONE"]; `fVisibilityPriority` 1.0; `iAIWeight` 200; `iAdvancedStartCost` 100; `iAsset` 16; `iConquestProb` 100; `iCost` 70; `iDCMAirbombMission` 2; `iDefense` 10; `iEspionageDefense` 10; `iFoodKept` 30; `iHappiness` 3; `iHealRateChange` 6; `iHealth` 3; `iMaxLatitude` 90; `iMinAreaSize` -1; `iTradeRoutes` 1 |
| VIKING_TRADING_POST | `Advisor` ADVISOR_GROWTH; `BuildingClass` BUILDINGCLASS_LIGHTHOUSE; `ConstructSound` AS2D_BUILD_LIGHTHOUSE; `Flavors` [{"FlavorType":"FLAVOR_GROWTH","iFlavor":10}]; `FreePromotion` PROMOTION_COASTAL_ASSAULT1; `FreeStartEra` ERA_MEDIEVAL; `PrereqTech` TECH_SAILING; `ProductionTraits` [{"ProductionTraitType":"TRAIT_SEAFARING","iProductionTrait":100}]; `SeaPlotYieldChanges` [1,0,0]; `bWater` True; `fVisibilityPriority` 1.0; `iAdvancedStartCost` 100; `iAsset` 3; `iConquestProb` 75; `iCost` 60; `iDCMAirbombMission` 2; `iForeignTradeRouteModifier` 50; `iMaxLatitude` 90; `iMinAreaSize` 10; `iPower` 1; `iTradeRouteModifier` 25 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| CELTIC_SWORDSMAN | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_CELTIC_SWORDSMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqTech` TECH_MILITARY_TRAINING; `TechTypes` ["TECH_RELIGION_CELTIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_SWORDSMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SWORDSMAN_CELTIC","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 7; `iCombatLimit` 100; `iConscription` 3; `iCost` 60; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 14; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| CELTIC_WARBAND | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_CELTIC_WARBAND; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_RELIGION_CELTIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_CELTIC_SWORDSMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SCHILDTRAEGER_CELTIC","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 6; `iCombatLimit` 100; `iConscription` 3; `iCost` 40; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| SPEARMAN | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_SPEARMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqTech` TECH_METAL_CASTING; `TechTypes` ["TECH_HUNTING"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_PIKEMAN","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_WARBAND","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_CELTIC_WARBAND","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_TRIARII","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_AUXILIAR","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_SARISSA","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SPEARMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 4; `iCombatLimit` 100; `iConscription` 3; `iCost` 35; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 6; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| SARISSA | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_SARISSA; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_GREEK"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatCollateralImmunes` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatCollateralImmune":1}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":100},{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SARISSA_MACEDON_2","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCityDefense` 25; `iCombat` 7; `iCombatLimit` 100; `iConscription` 5; `iCost` 40; `iCultureGarrison` 6; `iHillsDefense` 25; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 12; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| SPEARMAN | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_SPEARMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqTech` TECH_METAL_CASTING; `TechTypes` ["TECH_HUNTING"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_PIKEMAN","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_WARBAND","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_CELTIC_WARBAND","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_TRIARII","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_AUXILIAR","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_SARISSA","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SPEARMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 4; `iCombatLimit` 100; `iConscription` 3; `iCost` 35; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 6; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| WARBAND | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_WARBAND; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_RELIGION_NORDIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_WARBAND_GERMAN","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 6; `iCombatLimit` 100; `iConscription` 3; `iCost` 45; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

| UnitInfo | Fields set (records.json) |
|---|---|
| AUXILIAR | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_AUXILIAR; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_AUXILIAR","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 8; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 13; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| PRINCIPES | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_LIGHT_SWORDSMAN; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_ROME_LEGIONARY","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MELEE","iUnitCombatMod":25},{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":25}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_PRINCIPES","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 3; `iCombat` 8; `iCombatLimit` 100; `iCost` 50; `iCultureGarrison` 6; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 16; `iWithdrawalProb` 25; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| ROME_LEGIONARY | `Advisor` ADVISOR_MILITARY; `Builds` [{"BuildType":"BUILD_TRACK","bBuild":true},{"BuildType":"BUILD_ROAD","bBuild":true},{"BuildType":"BUILD_PAVED","bBuild":true},{"BuildType":"BUILD_ROMAN_ROAD","bBuild":true},{"BuildType":"BUILD_MODERN_ROAD","bBuild":true},{"BuildType":"BUILD_RAILROAD","bBuild":true},{"BuildType":"BUILD_QUARRY","bBuild":true},{"BuildType":"BUILD_FORT","bBuild":true},{"BuildType":"BUILD_REMOVE_JUNGLE","bBuild":true},{"BuildType":"BUILD_REMOVE_FOREST","bBuild":true},{"BuildType":"BUILD_LATIFUNDIUM","bBuild":true}]; `Class` UNITCLASS_ROME_LEGIONARY; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_ATTACK_CITY; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_MARCH","bFreePromotion":true},{"PromotionType":"PROMOTION_COMMANDO","bFreePromotion":true}]; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON"]; `PrereqBuilding` BUILDING_LEGION_BARRACKS; `PrereqTech` TECH_SIEGE_WARFARE; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_ATTACK","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true},{"UnitAIType":"UNITAI_WORKER","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_COMITATENSES","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_LEGIONARY","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 4; `iCombat` 10; `iCombatLimit` 100; `iCost` 60; `iCultureGarrison` 5; `iFirstStrikes` 1; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 24; `iWorkRate` 175; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| TRIARII | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_TRIARII; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `PrereqBonuses` ["BONUS_COPPER","BONUS_IRON","BONUS_OBSIDIAN"]; `PrereqBuilding` BUILDING_BARRACKS; `PrereqTech` TECH_IRON_WORKING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_DEFENSE","bUnitAI":true}]; `UnitClassDefenseMods` [{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":25}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_AUXILIAR","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_HEAVY_PIKEMAN","bUnitClassUpgrade":true}]; `UnitCombatMods` [{"UnitCombatType":"UNITCOMBAT_MOUNTED","iUnitCombatMod":50}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_ROME_TRIARII","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCityDefense` 25; `iCombat` 6; `iCombatLimit` 100; `iCost` 50; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 1; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| VELITES | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_SPEARMAN; `Combat` UNITCOMBAT_ARCHER; `DefaultUnitAI` UNITAI_ATTACK; `Domain` DOMAIN_LAND; `FeatureDefenses` [{"FeatureType":"FEATURE_FOREST","iFeatureDefense":50},{"FeatureType":"FEATURE_JUNGLE","iFeatureDefense":50}]; `FormationType` FORMATION_TYPE_RANGED; `PrereqTech` TECH_METAL_CASTING; `TechTypes` ["TECH_ROMAN"]; `UnitAIs` [{"UnitAIType":"UNITAI_COLLATERAL","bUnitAI":true},{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true}]; `UnitClassAttackMods` [{"UnitClassType":"UNITCLASS_WAR_ELEPHANT","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_ELEPHANT_RIDER","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_AXEMAN","iUnitClassMod":50},{"UnitClassType":"UNITCLASS_SARISSA","iUnitClassMod":50}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_TRIARII","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_AUXILIAR","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_JAVELIN_ROME","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":3}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `iAdvancedStartCost` 100; `iAnimalCombat` 50; `iAsset` 2; `iCollateralDamage` 25; `iCollateralDamageLimit` 50; `iCollateralDamageMaxUnits` 2; `iCombat` 4; `iCombatLimit` 100; `iCost` 30; `iCultureGarrison` 4; `iFirstStrikes` 2; `iHillsDefense` 25; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 6; `iWithdrawalProb` 25; `iXPValueAttack` 6; `iXPValueDefense` 3 |

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
| `st.game3_tech_lead` | table, 27 values | turn | every player | acquisition turns | 27 | X lines (the first of each player and tech; turn 0 is the start); source: a deal item giving the human that tech on the same turn (deal_items, TRADE_TECHNOLOGIES; the tech index of TechInfo, checked: every such item has the receiver's X line on its turn) [game3] |
| `st.game4_tech_lead` | table, 35 values | turn | every player | acquisition turns | 35 | X lines (the first of each player and tech; turn 0 is the start); source: a deal item giving the human that tech on the same turn (deal_items, TRADE_TECHNOLOGIES; the tech index of TechInfo, checked: every such item has the receiver's X line on its turn) [game4] |
| `st.game3_tech_use` | table, 27 values | turns | human | acquisition turns | 27 | X lines of the human; for each tech, the turns until the human first used what it unlocks: a civic adopted (CIVICS command; CivicInfo TechPrereq), a building ordered (ORDER type 1; BuildingInfo PrereqTech), a unit ordered (ORDER type 0; UnitInfo PrereqTech), a build ordered (MISSION_BUILD; BuildInfo PrereqTech); empty: not used before the save. Unlocks through other fields (TechTypes, AndPreReqs of later techs) are not counted [game3] |
| `st.game4_tech_use` | table, 35 values | turns | human | acquisition turns | 35 | X lines of the human; for each tech, the turns until the human first used what it unlocks: a civic adopted (CIVICS command; CivicInfo TechPrereq), a building ordered (ORDER type 1; BuildingInfo PrereqTech), a unit ordered (ORDER type 0; UnitInfo PrereqTech), a build ordered (MISSION_BUILD; BuildInfo PrereqTech); empty: not used before the save. Unlocks through other fields (TechTypes, AndPreReqs of later techs) are not counted [game4] |
| `st.game3_civic_tech_lag` | table, 15 values | turns | human | each civic adopted after the start | 15 | civics in each CIVICS command of the human not in its previous one (A lines), the tech each requires (CivicInfo TechPrereq) and the turn the human got it (X lines; turn 0: held from the start), and the AIs holding that civic at the save [game3] |
| `st.game4_civic_tech_lag` | table, 13 values | turns | human | each civic adopted after the start | 13 | civics in each CIVICS command of the human not in its previous one (A lines), the tech each requires (CivicInfo TechPrereq) and the turn the human got it (X lines; turn 0: held from the start), and the AIs holding that civic at the save [game4] |
| `st.game3_building_template` | table, 22 values | cities | every player | whole game | 22 | N lines: each building the human completed, the number of its cities that completed it, its median position in each city's order of completions (1: the city's first), the first completion, its distance in turns from the human's X line of the building's PrereqTech (empty when the building needs no tech; its other prerequisites, such as TechTypes, a religion or a building, are not counted); the same count and position for the AIs' cities [game3] |
| `st.game4_building_template` | table, 34 values | cities | every player | whole game | 34 | N lines: each building the human completed, the number of its cities that completed it, its median position in each city's order of completions (1: the city's first), the first completion, its distance in turns from the human's X line of the building's PrereqTech (empty when the building needs no tech; its other prerequisites, such as TechTypes, a religion or a building, are not counted); the same count and position for the AIs' cities [game4] |
| `st.game3_wonders` | table, 2 values | units built | every player | whole game | 2 | N lines of world wonders (BuildingClassInfo iMaxGlobalInstances 1) and national wonders (iMaxPlayerInstances or iMaxTeamInstances 1) [game3] |
| `st.game4_wonders` | table, 2 values | units built | every player | whole game | 2 | N lines of world wonders (BuildingClassInfo iMaxGlobalInstances 1) and national wonders (iMaxPlayerInstances or iMaxTeamInstances 1) [game4] |
| `gr.game4_food_buildings` | table, 7 values | cities at save | every player | save | 205 | growth.py: buildings with iFoodKept, a food RiverPlotYieldChanges or SeaPlotYieldChanges, or a food YieldModifiers or YieldChanges (BuildingInfo), and the cities holding each, real or free |
| `st.game3_city_profile` | table, 5 values | cities at save | every player | save | 5 | cities in the save dump: population, food, hammers, commerce, trade routes and their commerce, and buildings; human cities split into the capital (BUILDING_PALACE), the cities it captured (K lines) and those it founded; AI capitals and other AI cities [game3] |
| `st.game4_city_profile` | table, 5 values | cities at save | every player | save | 5 | cities in the save dump: population, food, hammers, commerce, trade routes and their commerce, and buildings; human cities split into the capital (BUILDING_PALACE), the cities it captured (K lines) and those it founded; AI capitals and other AI cities [game4] |
| `st.game3_build_plot_class` | table, 8 values | orders | human | order turns; plot traits at the save | 8 | A lines MISSION_BUILD by the plot's traits in the save dump: hills, flat land on a river or not, water, and a resource on it; terrain type and river do not change in play, a resource can be revealed later [game3] |
| `st.game4_build_plot_class` | table, 13 values | orders | human | order turns; plot traits at the save | 13 | A lines MISSION_BUILD by the plot's traits in the save dump: hills, flat land on a river or not, water, and a resource on it; terrain type and river do not change in play, a resource can be revealed later [game4] |
| `st.game3_worked_by_class` | table, 6 values | tiles at save | every player | save | 6 | worked land plots in the save dump by owner and trait (as in build_plot_class), and the improvement on them; cottage line: cottage, hamlet, village, town [game3] |
| `st.game4_worked_by_class` | table, 6 values | tiles at save | every player | save | 6 | worked land plots in the save dump by owner and trait (as in build_plot_class), and the improvement on them; cottage line: cottage, hamlet, village, town [game4] |
| `yl.game3_yield_check` | table, 2 values | tiles at save | every player | save | 750 | tileyield.py: the model against CvPlot::getYield in the save dump; a battle there: a C line on the plot in the last ten turns (DCM battle effects, BATTLE_EFFECT_LESS_FOOD and _COMMERCE, are not in the dump) |
| `yl.game4_yield_check` | table, 2 values | tiles at save | every player | save | 1178 | tileyield.py: the model against CvPlot::getYield in the save dump; a battle there: a C line on the plot in the last ten turns (DCM battle effects, BATTLE_EFFECT_LESS_FOOD and _COMMERCE, are not in the dump) |
| `yl.game3_yield_sources` | table, 63 values | food per tile | every player | save | 749 | tileyield.py: exactly predicted worked plots; mean yield per plot and the mean of each source term (food, hammers and commerce rows; the unit applies to each row's own yield) |
| `yl.game4_yield_sources` | table, 63 values | food per tile | every player | save | 1165 | tileyield.py: exactly predicted worked plots; mean yield per plot and the mean of each source term (food, hammers and commerce rows; the unit applies to each row's own yield) |
| `st.game3_per_city_output` | table, 7 values | yield per turn | every player | every 25th turn from 100 | 7 | M lines: population, hammers, commerce and food of the whole empire divided by its cities; AI: the median over AI players; anarchy turns show commerce 1 [game3] |
| `st.game4_per_city_output` | table, 8 values | yield per turn | every player | every 25th turn from 100 | 8 | M lines: population, hammers, commerce and food of the whole empire divided by its cities; AI: the median over AI players; anarchy turns show commerce 1 [game4] |
| `st.game3_gold_ledger` | table, 9 values | gold | human | by period | 9 | M lines of the human: the change of its gold between consecutive M lines is split into the gold per turn of the earlier line (income), the gold of deals that turn (deal_items TRADE_GOLD: on a peace turn, Q lines; on a turn it gave a tech; other), and a residual named by the events of the turn: a city taken (K), a trade mission (MISSION_TRADE), a hurry (TASK 9, TASK_HURRY), an upgrade (COMMAND_UPGRADE), anarchy; the residual on turns with no such event is the check of the ledger (gold per turn changes within a turn) [game3] |
| `st.game4_gold_ledger` | table, 12 values | gold | human | by period | 12 | M lines of the human: the change of its gold between consecutive M lines is split into the gold per turn of the earlier line (income), the gold of deals that turn (deal_items TRADE_GOLD: on a peace turn, Q lines; on a turn it gave a tech; other), and a residual named by the events of the turn: a city taken (K), a trade mission (MISSION_TRADE), a hurry (TASK 9, TASK_HURRY), an upgrade (COMMAND_UPGRADE), anarchy; the residual on turns with no such event is the check of the ledger (gold per turn changes within a turn) [game4] |
| `st.game1_upgrade_targets` | table, 3 values | orders | human | whole game | 3 | A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game1] |
| `st.game2_upgrade_targets` | table, 2 values | orders | human | whole game | 2 | A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game2] |
| `st.game3_upgrade_targets` | table, 1 values | orders | human | whole game | 1 | A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game3] |
| `st.game4_upgrade_targets` | table, 5 values | orders | human | whole game | 5 | A lines COMMAND_UPGRADE: the unit type upgraded to (the first log version gives its UnitInfo index, mapped by XML order: every mapped target but one is in the named unit's UnitClassUpgrades); the named unit can be another member of the group, so the source type is not used; U lines of that type; C lines of the human attacking with it [game4] |
| `gr.game3_growth` | table, 5 values | cities at save | every player | save | 129 | growth.py on the save dump of game3 (GAMESPEED_MARATHON, HANDICAP_NOBLE); medians per group; growing: cities with a food surplus; cities in disorder left out |
| `gr.game4_growth` | table, 5 values | cities at save | every player | save | 205 | growth.py on the save dump of game4 (GAMESPEED_MARATHON, HANDICAP_MONARCH); medians per group; growing: cities with a food surplus; cities in disorder left out |
| `gr.game3_food_kept` | table, 3 values | cities at save | every player | save | 129 | growth.py: each city's sum of iFoodKept over its buildings, real and free |
| `gr.game4_food_kept` | table, 6 values | cities at save | every player | save | 205 | growth.py: each city's sum of iFoodKept over its buildings, real and free |
| `gr.game3_food_buildings` | table, 4 values | cities at save | every player | save | 129 | growth.py: buildings with iFoodKept, a food RiverPlotYieldChanges or SeaPlotYieldChanges, or a food YieldModifiers or YieldChanges (BuildingInfo), and the cities holding each, real or free |
| `tg.game3_war_targets` | table, 2 values | rank | human | each declaration of the human (cues from the turn before) | 2 | strategy.py: W lines of game3; options: AIs with an M line the turn before, holding a city, not at war with the human, not unmet at the save; rank 1 = the least power, the least distance, the most cities |
| `tg.game4_war_targets` | table, 8 values | rank | human | each declaration of the human (cues from the turn before) | 8 | strategy.py: W lines of game4; options: AIs with an M line the turn before, holding a city, not at war with the human, not unmet at the save; rank 1 = the least power, the least distance, the most cities |
| `tg.war_target_strategies_pooled` | table, 10 values | category | human | each declaration of the human | 10 | strategy.py: maximum-likelihood classification over the declarations of every game given |
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
| `st.game3_expansion` | table, 8 values | turn | every player | founding turns | 8 | the turn of each player's k-th city founded: the human's from its FOUND commands (A lines), the AIs' from the founding turn of the save's cities, credited to the first owner (the old owner of the first K or Z line on the plot); AI cities razed before the save are not in the save and are missing [game3] |
| `st.game4_expansion` | table, 8 values | turn | every player | founding turns | 8 | the turn of each player's k-th city founded: the human's from its FOUND commands (A lines), the AIs' from the founding turn of the save's cities, credited to the first owner (the old owner of the first K or Z line on the plot); AI cities razed before the save are not in the save and are missing [game4] |
| `st.game3_city_spacing` | table, 2 values | cities | every player | founding turns | 2 | every city after a player's first: grid distance (map wrap ignored) to the nearest city the same player founded before it, as in the expansion table [game3] |
| `st.game4_city_spacing` | table, 2 values | cities | every player | founding turns | 2 | every city after a player's first: grid distance (map wrap ignored) to the nearest city the same player founded before it, as in the expansion table [game4] |
