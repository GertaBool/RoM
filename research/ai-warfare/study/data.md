<!-- Rendered by method/docs.py from data.md.in. Do not edit; edit the template. -->
# Tiles, diplomacy, trade, units and combat: game 3 and game 4

The data behind `study/human.md`, from sources not used before:
- the extended save dump (`toolchain/analysis/dump.sh`), which adds every map plot, the relations
  between all players, resources, unit promotions and city trade;
- every line of the war log (`tools/extract.py`).

The queries are declared in `study/queries.json` and turned into figures by `tools/sqlfig.py`.
Each table states what it counts, who, when, and from which source. Facts come first; the
readings are in the last section.

## 1. Tiles

### 1.1 What became of the human's build orders

Each plot and build ordered is counted once and compared with what stands on that plot at the
save.

| build | outcome | owner_now | plots |
|---|---|---|---|
| BUILD_CAMP | other improvement | human | 10 |
| BUILD_CAMP | same improvement | human | 3 |
| BUILD_COTTAGE | other improvement | human | 15 |
| BUILD_COTTAGE | grown or upgraded | human | 13 |
| BUILD_FARM | same improvement | human | 21 |
| BUILD_FISHING_BOATS | same improvement | human | 9 |
| BUILD_MINE | same improvement | human | 31 |
| BUILD_MINE | other improvement | human | 2 |
| BUILD_MINE | grown or upgraded | human | 1 |
| BUILD_OLIVE_FARM | same improvement | human | 2 |
| BUILD_PASTURE | same improvement | human | 3 |
| BUILD_PAVED | route as ordered or better | human | 12 |
| BUILD_PAVED | route as ordered or better | nobody | 2 |
| BUILD_QUARRY | same improvement | human | 3 |
| BUILD_ROAD | route as ordered or better | human | 42 |
| BUILD_ROAD | route as ordered or better | nobody | 1 |
| BUILD_TRACK | route as ordered or better | human | 64 |
| BUILD_WINERY | same improvement | human | 5 |
| BUILD_WORKSHOP | other improvement | human | 2 |
| BUILD_WORKSHOP | same improvement | human | 1 |

*distinct plots; who: human; turn: orders over the game; plots at the save; rows counted: 20; source: wl_A MISSION_BUILD (distinct plot and build) joined to plots at the save; build_info; improvement_info upgrade chains [game4]. Every value counted (20).*

| build | outcome | owner_now | plots |
|---|---|---|---|
| BUILD_APPLE_FARM | same improvement | human | 2 |
| BUILD_CAMP | same improvement | human | 7 |
| BUILD_CAMP | other improvement | human | 1 |
| BUILD_COTTAGE | grown or upgraded | human | 20 |
| BUILD_COTTAGE | same improvement | human | 14 |
| BUILD_COTTAGE | other improvement | human | 4 |
| BUILD_FARM | same improvement | human | 17 |
| BUILD_FARM | other improvement | human | 1 |
| BUILD_MINE | same improvement | human | 14 |
| BUILD_MINE | no improvement | human | 1 |
| BUILD_QUARRY | same improvement | human | 1 |
| BUILD_QUARRY | same improvement | nobody | 1 |
| BUILD_ROAD | route as ordered or better | human | 23 |
| BUILD_ROAD | route as ordered or better | nobody | 1 |
| BUILD_TRACK | route as ordered or better | human | 50 |

*distinct plots; who: human; turn: orders over the game; plots at the save; rows counted: 15; source: wl_A MISSION_BUILD (distinct plot and build) joined to plots at the save; build_info; improvement_info upgrade chains [game3]. Every value counted (15).*

Ordered improvements now replaced by another, and whether a later order of the human explains
it:

| build | now_there | cause | plots |
|---|---|---|---|
| BUILD_CAMP | WINERY | own later order | 4 |
| BUILD_CAMP | MINE | own later order | 2 |
| BUILD_CAMP | HAMLET | own later order | 1 |
| BUILD_CAMP | OLIVE_FARM | own later order | 1 |
| BUILD_CAMP | PASTURE | own later order | 1 |
| BUILD_CAMP | WORKSHOP | own later order | 1 |
| BUILD_COTTAGE | MINE | own later order | 11 |
| BUILD_COTTAGE | FARM | own later order | 3 |
| BUILD_COTTAGE | PASTURE | own later order | 1 |
| BUILD_MINE | QUARRY | own later order | 1 |
| BUILD_MINE | VILLAGE | own later order | 1 |
| BUILD_WORKSHOP | FARM | own later order | 1 |
| BUILD_WORKSHOP | HAMLET | no later order of the human | 1 |

*distinct plots; who: human; turn: orders over the game; plots at the save; rows counted: 13; source: ordered improvements now replaced by another (not by their own upgrade): what stands there, and whether the human later ordered that build on the same plot [game4]. Every value counted (13).*

| build | now_there | cause | plots |
|---|---|---|---|
| BUILD_CAMP | VILLAGE | own later order | 1 |
| BUILD_COTTAGE | FARM | own later order | 3 |
| BUILD_COTTAGE | MINE | own later order | 1 |
| BUILD_FARM | HAMLET | no later order of the human | 1 |
| BUILD_MINE | - | no later order of the human | 1 |

*distinct plots; who: human; turn: orders over the game; plots at the save; rows counted: 5; source: ordered improvements now replaced by another (not by their own upgrade): what stands there, and whether the human later ordered that build on the same plot [game3]. Every value counted (5).*

### 1.2 Land use at the save

| owner_class | surface | plots | improved | with_route | worked | worked_improved | worked_unimproved |
|---|---|---|---|---|---|---|---|
| ai | land | 1623 | 888 | 1162 | 862 | 648 | 214 |
| ai | water | 682 | 120 | 0 | 153 | 104 | 49 |
| human | land | 150 | 94 | 120 | 123 | 91 | 32 |
| human | water | 115 | 20 | 0 | 40 | 18 | 22 |
| nobody | land | 1759 | 35 | 110 | 0 | 0 | 0 |
| nobody | water | 1047 | 15 | 0 | 0 | 0 | 0 |

*tiles at save; who: all players; turn: save; rows counted: 6; source: plots at the save, by owner (the human, any AI, nobody) and land or water (plot type 3) [game4]. Every value counted (6).*

| owner_class | surface | plots | improved | with_route | worked | worked_improved | worked_unimproved |
|---|---|---|---|---|---|---|---|
| ai | land | 1092 | 578 | 777 | 517 | 383 | 134 |
| ai | water | 534 | 90 | 0 | 124 | 82 | 42 |
| human | land | 151 | 109 | 127 | 106 | 91 | 15 |
| human | water | 6 | 2 | 0 | 3 | 2 | 1 |
| nobody | land | 1335 | 1 | 92 | 0 | 0 | 0 |
| nobody | water | 746 | 0 | 0 | 0 | 0 | 0 |

*tiles at save; who: all players; turn: save; rows counted: 6; source: plots at the save, by owner (the human, any AI, nobody) and land or water (plot type 3) [game3]. Every value counted (6).*

Yields of worked tiles (food, hammers and commerce as separate means):

| owner_class | surface | worked_tiles | food | hammers | commerce |
|---|---|---|---|---|---|
| ai | land | 862 | 3.689 | 3.102 | 1.099 |
| ai | water | 153 | 5.451 | 0.536 | 2.033 |
| human | land | 123 | 3.602 | 3.593 | 1.545 |
| human | water | 40 | 4.65 | 0.0 | 1.25 |

*food per tile; who: all players; turn: save; rows counted: 4; source: worked plots at the save; food, hammers and commerce are separate columns (each a mean per worked tile) [game4]. Every value counted (4).*

| owner_class | surface | worked_tiles | food | hammers | commerce |
|---|---|---|---|---|---|
| ai | land | 517 | 3.681 | 2.749 | 1.217 |
| ai | water | 124 | 5.298 | 0.46 | 2.081 |
| human | land | 106 | 3.67 | 2.557 | 1.764 |
| human | water | 3 | 5.667 | 0.0 | 1.0 |

*food per tile; who: all players; turn: save; rows counted: 4; source: worked plots at the save; food, hammers and commerce are separate columns (each a mean per worked tile) [game3]. Every value counted (4).*

Every improvement on owned land:

| improvement | human_worked | human_unworked | ai_worked | ai_unworked |
|---|---|---|---|---|
| - | 54 | 97 | 263 | 1034 |
| MINE | 34 | 0 | 216 | 50 |
| FARM | 21 | 2 | 175 | 35 |
| FISHING_BOATS | 18 | 2 | 104 | 16 |
| HAMLET | 8 | 0 | 17 | 8 |
| VILLAGE | 7 | 0 | 3 | 0 |
| PASTURE | 6 | 0 | 65 | 1 |
| WINERY | 5 | 0 | 1 | 2 |
| CAMP | 3 | 0 | 71 | 75 |
| QUARRY | 3 | 0 | 16 | 3 |
| OLIVE_FARM | 2 | 0 | 8 | 1 |
| CITY_RUINS | 0 | 1 | 0 | 0 |
| SHAFT_MINE | 1 | 0 | 5 | 1 |
| WORKSHOP | 1 | 0 | 15 | 5 |
| APPLE_FARM | 0 | 0 | 10 | 0 |
| COTTAGE | 0 | 0 | 31 | 53 |
| FORT | 0 | 0 | 0 | 1 |
| PLANTATION | 0 | 0 | 13 | 5 |
| SILK_FARM | 0 | 0 | 2 | 0 |

*tiles at save; who: all players; turn: save; rows counted: 19; source: plots at the save: every improvement, on land owned by the human or by an AI, worked or not [game4]. Every value counted (19).*

| improvement | human_worked | human_unworked | ai_worked | ai_unworked |
|---|---|---|---|---|
| - | 16 | 30 | 176 | 782 |
| MINE | 21 | 0 | 58 | 41 |
| FARM | 20 | 0 | 98 | 22 |
| HAMLET | 16 | 2 | 40 | 0 |
| COTTAGE | 6 | 10 | 51 | 36 |
| CAMP | 9 | 5 | 55 | 76 |
| VILLAGE | 9 | 0 | 12 | 0 |
| PASTURE | 5 | 0 | 40 | 3 |
| QUARRY | 3 | 1 | 10 | 9 |
| APPLE_FARM | 2 | 0 | 2 | 0 |
| FISHING_BOATS | 2 | 0 | 82 | 8 |
| OLIVE_FARM | 0 | 0 | 7 | 2 |
| PLANTATION | 0 | 0 | 3 | 1 |
| SHAFT_MINE | 0 | 0 | 2 | 0 |
| SILK_FARM | 0 | 0 | 0 | 3 |
| WINERY | 0 | 0 | 4 | 0 |
| WORKSHOP | 0 | 0 | 1 | 2 |

*tiles at save; who: all players; turn: save; rows counted: 17; source: plots at the save: every improvement, on land owned by the human or by an AI, worked or not [game3]. Every value counted (17).*

The cottage line (progress in turns of worked growth):

| improvement | owner_class | tiles | worked | mean_progress |
|---|---|---|---|---|
| COTTAGE | ai | 88 | 31 | 4.227 |
| HAMLET | ai | 29 | 17 | 22.655 |
| HAMLET | human | 8 | 8 | 24.5 |
| VILLAGE | ai | 6 | 3 | 23.167 |
| VILLAGE | human | 7 | 7 | 31.714 |

*tiles at save; who: all players; turn: save; rows counted: 5; source: plots at the save with a cottage-line improvement; upgrade_progress is in turns of worked progress [game4]. Every value counted (5).*

| improvement | owner_class | tiles | worked | mean_progress |
|---|---|---|---|---|
| COTTAGE | ai | 87 | 51 | 7.77 |
| COTTAGE | human | 16 | 6 | 13.75 |
| HAMLET | ai | 40 | 40 | 26.55 |
| HAMLET | human | 18 | 16 | 23.0 |
| VILLAGE | ai | 12 | 12 | 27.333 |
| VILLAGE | human | 9 | 9 | 42.667 |

*tiles at save; who: all players; turn: save; rows counted: 6; source: plots at the save with a cottage-line improvement; upgrade_progress is in turns of worked progress [game3]. Every value counted (6).*

### 1.3 What the human's map shows

Plots the human has revealed where the improvement it sees differs from the one there:

| land | revealed | seen_differs |
|---|---|---|
| foreign land | 1462 | 326 |
| nobody | 1055 | 6 |
| own land | 265 | 0 |

*tiles at save; who: human; turn: save; rows counted: 3; source: plots the human has revealed: the improvement it sees against the one there [game4]. Every value counted (3).*

| land | revealed | seen_differs |
|---|---|---|
| foreign land | 990 | 213 |
| nobody | 903 | 0 |
| own land | 157 | 0 |

*tiles at save; who: human; turn: save; rows counted: 3; source: plots the human has revealed: the improvement it sees against the one there [game3]. Every value counted (3).*

## 2. Diplomacy

Each AI's attitude toward the human at the save, against its mean attitude value toward the
other AIs it has met:

| player | attitude | attitude_val | war | warplan | worst_enemy_is_human | mean_val_to_others |
|---|---|---|---|---|---|---|
| 0 | ATTITUDE_ANNOYED | -7 | 0 | NO_WARPLAN | 1 | 1.857 |
| 1 | ATTITUDE_ANNOYED | -7 | 0 | NO_WARPLAN | 0 | -0.063 |
| 2 | ATTITUDE_FURIOUS | -10 | 0 | NO_WARPLAN | 1 | 4.688 |
| 4 | ATTITUDE_ANNOYED | -6 | 0 | NO_WARPLAN | 0 | -2.875 |
| 5 | ATTITUDE_ANNOYED | -6 | 0 | NO_WARPLAN | 1 | 2.938 |
| 6 | ATTITUDE_CAUTIOUS | -2 | 0 | NO_WARPLAN | 0 | 3.563 |
| 7 | ATTITUDE_FURIOUS | -14 | 1 | WARPLAN_ATTACKED_RECENT | 1 | 2.813 |
| 8 | ATTITUDE_PLEASED | 3 | 0 | NO_WARPLAN | 0 | 1.875 |
| 9 | ATTITUDE_ANNOYED | -4 | 0 | NO_WARPLAN | 1 | 4.625 |
| 10 | ATTITUDE_FURIOUS | -17 | 1 | WARPLAN_ATTACKED | 1 | 3.125 |
| 11 | ATTITUDE_ANNOYED | -6 | 0 | NO_WARPLAN | 0 | -0.714 |
| 12 | ATTITUDE_PLEASED | 3 | 0 | NO_WARPLAN | 0 | -0.071 |
| 13 | ATTITUDE_CAUTIOUS | -2 | 0 | NO_WARPLAN | 0 | 1.625 |
| 15 | ATTITUDE_PLEASED | 4 | 0 | NO_WARPLAN | 0 | -0.438 |
| 16 | ATTITUDE_ANNOYED | -3 | 0 | NO_WARPLAN | 1 | 2.786 |
| 17 | ATTITUDE_CAUTIOUS | 2 | 0 | NO_WARPLAN | 0 | 4.375 |
| 18 | ATTITUDE_CAUTIOUS | -2 | 0 | NO_WARPLAN | 1 | 3.063 |

*xml; who: AI players; turn: save; rows counted: 17; source: diplo at the save: each AI's attitude toward the human (AttitudeTypes) and its value, war state and plan (WarPlanTypes), and its mean attitude value toward the other AIs it has met [game4]. Every value counted (17).*

| player | attitude | attitude_val | war | warplan | worst_enemy_is_human | mean_val_to_others |
|---|---|---|---|---|---|---|
| 0 | ATTITUDE_PLEASED | 7 | 0 | NO_WARPLAN | 0 | 1.563 |
| 1 | ATTITUDE_CAUTIOUS | 1 | 0 | NO_WARPLAN | 0 | 2.813 |
| 2 | ATTITUDE_CAUTIOUS | 2 | 0 | NO_WARPLAN | 0 | 1.688 |
| 3 | ATTITUDE_PLEASED | 5 | 0 | NO_WARPLAN | 0 | -0.563 |
| 4 | ATTITUDE_ANNOYED | -6 | 0 | NO_WARPLAN | 0 | -0.125 |
| 5 | ATTITUDE_PLEASED | 8 | 0 | NO_WARPLAN | 0 | 2.125 |
| 6 | ATTITUDE_PLEASED | 6 | 0 | NO_WARPLAN | 0 | 3.125 |
| 7 | ATTITUDE_ANNOYED | -3 | 0 | NO_WARPLAN | 0 | 2.313 |
| 8 | ATTITUDE_CAUTIOUS | 2 | 0 | NO_WARPLAN | 0 | 2.333 |
| 9 | ATTITUDE_PLEASED | 5 | 0 | NO_WARPLAN | 0 | 2.938 |
| 10 | ATTITUDE_PLEASED | 5 | 0 | NO_WARPLAN | 0 | 0.313 |
| 11 | ATTITUDE_PLEASED | 6 | 0 | NO_WARPLAN | 0 | 3.813 |
| 13 | ATTITUDE_PLEASED | 4 | 0 | NO_WARPLAN | 0 | 0.438 |
| 14 | ATTITUDE_ANNOYED | -9 | 0 | NO_WARPLAN | 0 | -0.875 |
| 15 | ATTITUDE_ANNOYED | -5 | 0 | NO_WARPLAN | 0 | 0.875 |
| 16 | ATTITUDE_CAUTIOUS | -1 | 0 | NO_WARPLAN | 0 | 3.8 |
| 17 | ATTITUDE_PLEASED | 6 | 0 | NO_WARPLAN | 0 | 3.75 |

*xml; who: AI players; turn: save; rows counted: 17; source: diplo at the save: each AI's attitude toward the human (AttitudeTypes) and its value, war state and plan (WarPlanTypes), and its mean attitude value toward the other AIs it has met [game3]. Every value counted (17).*

What the AIs remember of the human, against what they remember of each other:

| memory | about_human | about_other_ais |
|---|---|---|
| DECLARED_WAR_ON_FRIEND | 83 | 66 |
| RECEIVED_TECH_FROM_ANY | 41 | 479 |
| TRADED_TECH_TO_US | 14 | 39 |
| REFUSED_HELP | 9 | 0 |
| DENIED_JOIN_WAR | 7 | 0 |
| GIVE_HELP | 7 | 0 |
| DECLARED_WAR | 6 | 7 |
| DENIED_STOP_TRADING | 3 | 0 |
| CANCELLED_OPEN_BORDERS | 1 | 9 |
| RAZED_CITY | 0 | 2 |
| HIRED_WAR_ALLY | 0 | 1 |

*xml; who: AI players; turn: save; rows counted: 11; source: memory at the save (AI_getMemoryCount): counts held by AIs about the human, and about other AIs, by memory type [game4]. Every value counted (11).*

| memory | about_human | about_other_ais |
|---|---|---|
| DECLARED_WAR_ON_FRIEND | 17 | 40 |
| RECEIVED_TECH_FROM_ANY | 13 | 501 |
| DENIED_STOP_TRADING | 9 | 0 |
| TRADED_TECH_TO_US | 8 | 40 |
| REFUSED_HELP | 8 | 0 |
| DENIED_JOIN_WAR | 4 | 0 |
| GIVE_HELP | 4 | 0 |
| DECLARED_WAR | 2 | 6 |
| ACCEPTED_RELIGION | 1 | 0 |
| CANCELLED_OPEN_BORDERS | 0 | 4 |

*xml; who: AI players; turn: save; rows counted: 10; source: memory at the save (AI_getMemoryCount): counts held by AIs about the human, and about other AIs, by memory type [game3]. Every value counted (10).*

Diplomatic events with the human:

| diplo_event | direction | n |
|---|---|---|
| DIPLOEVENT_AI_CONTACT | to human | 102 |
| DIPLOEVENT_CONTACT | to human | 66 |
| DIPLOEVENT_REFUSED_HELP | to human | 12 |
| DIPLOEVENT_GIVE_HELP | to human | 10 |
| DIPLOEVENT_NO_JOIN_WAR | to human | 9 |
| DIPLOEVENT_NO_STOP_TRADING | to human | 9 |
| DIPLOEVENT_NO_CONVERT | to human | 2 |

*deals; who: human and AI; turn: whole game; rows counted: 7; source: E lines (DiploEventTypes) involving the human, by direction [game4]. Every value counted (7).*

| diplo_event | direction | n |
|---|---|---|
| DIPLOEVENT_AI_CONTACT | to human | 88 |
| DIPLOEVENT_CONTACT | to human | 42 |
| DIPLOEVENT_NO_STOP_TRADING | to human | 11 |
| DIPLOEVENT_REFUSED_HELP | to human | 11 |
| DIPLOEVENT_NO_JOIN_WAR | to human | 6 |
| DIPLOEVENT_GIVE_HELP | to human | 5 |
| DIPLOEVENT_CONVERT | to human | 1 |

*deals; who: human and AI; turn: whole game; rows counted: 7; source: E lines (DiploEventTypes) involving the human, by direction [game3]. Every value counted (7).*

## 3. Trade

Deals with the human, by item and direction:

| item | direction | items | data_sum |
|---|---|---|---|
| TRADE_GOLD | human receives | 8 | 2685 |
| TRADE_GOLD_PER_TURN | human receives | 3 | 17 |
| TRADE_OPEN_BORDERS | human gives | 57 | 38 |
| TRADE_OPEN_BORDERS | human receives | 57 | 38 |
| TRADE_PEACE_TREATY | human gives | 15 | 0 |
| TRADE_PEACE_TREATY | human receives | 15 | 0 |
| TRADE_RESOURCES | human gives | 13 | 388 |
| TRADE_RESOURCES | human receives | 10 | 240 |
| TRADE_TECHNOLOGIES | human gives | 21 | 1516 |
| TRADE_TECHNOLOGIES | human receives | 7 | 327 |

*deals; who: human; turn: whole game; rows counted: 10; source: deal_items (D lines) with the human as one side; data is the amount or index of the item [game4]. Every value counted (10).*

| item | direction | items | data_sum |
|---|---|---|---|
| TRADE_GOLD | human receives | 4 | 1520 |
| TRADE_GOLD_PER_TURN | human receives | 1 | 6 |
| TRADE_OPEN_BORDERS | human gives | 51 | 34 |
| TRADE_OPEN_BORDERS | human receives | 51 | 34 |
| TRADE_PEACE_TREATY | human gives | 6 | 0 |
| TRADE_PEACE_TREATY | human receives | 6 | 0 |
| TRADE_RESOURCES | human gives | 22 | 973 |
| TRADE_RESOURCES | human receives | 19 | 490 |
| TRADE_TECHNOLOGIES | human gives | 13 | 1202 |
| TRADE_TECHNOLOGIES | human receives | 4 | 183 |

*deals; who: human; turn: whole game; rows counted: 10; source: deal_items (D lines) with the human as one side; data is the amount or index of the item [game3]. Every value counted (10).*

Resources and trade routes at the save:

| who | kinds_available | imported | exported |
|---|---|---|---|
| ai mean | 18.412 | 2.824 | 2.824 |
| human | 25.0 | 6.0 | 6.0 |

*xml; who: all players; turn: save; rows counted: 2; source: bonuses at the save: resource kinds available, imported and exported, the human against the mean AI [game4]. Every value counted (2).*

| who | kinds_available | imported | exported |
|---|---|---|---|
| ai mean | 13.813 | 2.25 | 2.063 |
| human | 31.0 | 13.0 | 16.0 |

*xml; who: all players; turn: save; rows counted: 2; source: bonuses at the save: resource kinds available, imported and exported, the human against the mean AI [game3]. Every value counted (2).*

| who | cities | routes_per_city | trade_commerce_per_city |
|---|---|---|---|
| ai | 179 | 2.978 | 7.447 |
| human | 26 | 5.846 | 20.615 |

*cities at save; who: all players; turn: save; rows counted: 2; source: cities at the save: trade routes and trade commerce per city [game4]. Every value counted (2).*

| who | cities | routes_per_city | trade_commerce_per_city |
|---|---|---|---|
| ai | 116 | 2.302 | 4.759 |
| human | 13 | 4.846 | 17.308 |

*cities at save; who: all players; turn: save; rows counted: 2; source: cities at the save: trade routes and trade commerce per city [game3]. Every value counted (2).*

## 4. Units and combat

Combat by side. The result is the R line written directly after the C line; with no R line, no
unit died:

| side | battles | attacker_won | defender_won | no_death | median_odds | under_half |
|---|---|---|---|---|---|---|
| AI against AI | 153 | 97 | 37 | 19 | 732.0 | 38 |
| AI attacks the human | 1 | 0 | 1 | 0 | 471.0 | 1 |
| human attacks | 80 | 66 | 8 | 6 | 978.0 | 3 |

*battles; who: all players; turn: whole game; rows counted: 3; source: C lines; result from the R line directly after (none: no unit died); odds per mille [game4]. Every value counted (3).*

| side | battles | attacker_won | defender_won | no_death | median_odds | under_half |
|---|---|---|---|---|---|---|
| AI against AI | 52 | 29 | 17 | 6 | 856.5 | 17 |
| human attacks | 14 | 10 | 2 | 2 | 810.5 | 0 |

*battles; who: all players; turn: whole game; rows counted: 2; source: C lines; result from the R line directly after (none: no unit died); odds per mille [game3]. Every value counted (2).*

Attacks by odds band:

| odds_from | human_attacks | human_won | ai_attacks | ai_won |
|---|---|---|---|---|
| 0 | 0 | 0 | 16 | 2 |
| 200 | 2 | 1 | 18 | 4 |
| 400 | 5 | 3 | 22 | 12 |
| 600 | 9 | 2 | 35 | 20 |
| 800 | 64 | 60 | 63 | 59 |

*battles; who: human and AI; turn: whole game; rows counted: 5; source: C lines: attacks by odds band (per mille, bands of 200) and who attacked, with the result from the next line [game4]. Every value counted (5).*

| odds_from | human_attacks | human_won | ai_attacks | ai_won |
|---|---|---|---|---|
| 0 | 0 | 0 | 10 | 0 |
| 200 | 0 | 0 | 6 | 1 |
| 400 | 0 | 0 | 3 | 1 |
| 600 | 4 | 3 | 6 | 3 |
| 800 | 10 | 7 | 27 | 24 |

*battles; who: human and AI; turn: whole game; rows counted: 5; source: C lines: attacks by odds band (per mille, bands of 200) and who attacked, with the result from the next line [game3]. Every value counted (5).*

Promotions at the save:

| who | units | promotions_per_unit | xp_per_unit | with_three_or_more |
|---|---|---|---|---|
| ai | 1137 | 1.011 | 1.961 | 97 |
| human | 85 | 3.671 | 11.635 | 50 |

*units at save; who: all players; turn: save; rows counted: 2; source: units at the save that can fight: promotions per unit, the human against the AIs [game4]. Every value counted (2).*

| who | units | promotions_per_unit | xp_per_unit | with_three_or_more |
|---|---|---|---|---|
| ai | 494 | 1.538 | 2.621 | 95 |
| human | 35 | 6.914 | 7.714 | 32 |

*units at save; who: all players; turn: save; rows counted: 2; source: units at the save that can fight: promotions per unit, the human against the AIs [game3]. Every value counted (2).*

| promotion | human_units | ai_units |
|---|---|---|
| COMBAT1 | 50 | 484 |
| COMMANDO | 37 | 0 |
| MARCH | 37 | 0 |
| COMBAT2 | 36 | 41 |
| AMPHIBIOUS | 26 | 87 |
| GUERILLA1 | 19 | 191 |
| GUERILLA2 | 17 | 28 |
| MEDIC1 | 12 | 5 |
| SHOCK | 11 | 49 |
| NAVIGATION1 | 11 | 8 |

*units at save; who: all players; turn: save; rows counted: 10; source: unit_promotions at the save: the ten promotions most held by the human's units, with the AI's count [game4]. Every value counted (10).*

| promotion | human_units | ai_units |
|---|---|---|
| GUERILLA1 | 32 | 148 |
| GUERILLA2 | 32 | 37 |
| COMBAT1 | 30 | 252 |
| WOODSMAN1 | 28 | 23 |
| WOODSMAN2 | 28 | 17 |
| LOOTER | 28 | 15 |
| WOODSMAN3 | 28 | 15 |
| GUERILLA3 | 23 | 1 |
| SHOCK | 8 | 44 |
| LEADER | 2 | 1 |

*units at save; who: all players; turn: save; rows counted: 10; source: unit_promotions at the save: the ten promotions most held by the human's units, with the AI's count [game3]. Every value counted (10).*

The human's move orders, by group size:

| group_size | orders | mean_steps | median_steps | max_steps |
|---|---|---|---|---|
| 1 | 442 | 2.088 | 1.0 | 10 |
| 2-3 | 73 | 2.849 | 2.0 | 13 |
| 4-6 | 10 | 2.0 | 1.5 | 4 |
| 7+ | 3 | 1.0 | 1.0 | 1 |

*orders; who: human; turn: whole game; rows counted: 4; source: wl_A MISSION_MOVE_TO: steps from the unit to its target (the larger of the x and y distances) by group size [game4]. Every value counted (4).*

| group_size | orders | mean_steps | median_steps | max_steps |
|---|---|---|---|---|
| 1 | 195 | 1.928 | 1.0 | 8 |
| 2-3 | 4 | 3.5 | 2.5 | 8 |
| 4-6 | 3 | 1.333 | 1.0 | 2 |

*orders; who: human; turn: whole game; rows counted: 3; source: wl_A MISSION_MOVE_TO: steps from the unit to its target (the larger of the x and y distances) by group size [game3]. Every value counted (3).*

Stacks near or in enemy land:

| who | stacks | turns | mean_military | max_military |
|---|---|---|---|---|
| ai | 227 | 82 | 5.159 | 10 |
| human | 14 | 10 | 4.714 | 9 |

*units at save; who: all players; turn: whole game; rows counted: 2; source: G lines: stacks near or in enemy land after each player's moves (AI stacks of 3+ military units, human stacks of 2+) [game4]. Every value counted (2).*

| who | stacks | turns | mean_military | max_military |
|---|---|---|---|---|
| ai | 71 | 41 | 4.183 | 7 |
| human | 4 | 4 | 3.5 | 4 |

*units at save; who: all players; turn: whole game; rows counted: 2; source: G lines: stacks near or in enemy land after each player's moves (AI stacks of 3+ military units, human stacks of 2+) [game3]. Every value counted (2).*

## 5. Readings

Each reading names its facts and what would refute it. All rest on two games.

1. **Tiles are re-planned as techs arrive.**
   - Facts: nearly every ordered improvement now replaced was replaced by a later order of the
     human (section 1.1). The largest group is cottages that became mines in game 4.
   - Refuted if: in a further game, the replacements are mostly not the human's own later
     orders.
2. **Working every cottage holds in game 4 only.**
   - Game 4: no cottage remains on the human's land, and every hamlet and village is worked.
   - Game 3: many of the human's cottages are unworked, while the AI works most of its own
     (section 1.2). The game 4 pattern is not a rule.
   - Refuted: as a general rule, by game 3.
3. **Commerce comes from trade, not only from tiles.**
   - Facts: the human's cities have about twice the AI's trade routes per city, and much more
     trade commerce (section 3).
   - Not yet separated from city size and position; that is open.
4. **The human almost never attacks at under even odds, and the AIs almost never attack the
   human.**
   - Facts: the column for attacks under one half, and the attacks by the AI on the human, in
     both combat tables (section 4).
   - Not supported: that the human's median odds are higher than the AI's. Game 3's are lower
     than the AI-against-AI median.
   - Refuted if: in a further game, the human attacks under even odds as often as the AI does.
5. **Experience is concentrated in few units.**
   - Facts: the human's fighting units carry several times the AI's promotions and experience
     per unit (section 4).
6. **The human sells technology.**
   - Facts: in both games it gives more tech items than it receives, and receives gold (section 3).
7. **The human's map of foreign land is out of date in places.** It plays with partial
   information, which `study/human.md` respects by using only lines before each decision.
   - Facts: section 1.3.

## 6. Open

- Trade commerce against city size and position.
- Combat against the units and terrain involved: the C lines carry both.
- What the AIs' memories did to their requests and deals with the human (the E and D lines
  over time).

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `d.game4_build_outcome` | table, 20 values | distinct plots | human | orders over the game; plots at the save | 20 | wl_A MISSION_BUILD (distinct plot and build) joined to plots at the save; build_info; improvement_info upgrade chains [game4] |
| `d.game3_build_outcome` | table, 15 values | distinct plots | human | orders over the game; plots at the save | 15 | wl_A MISSION_BUILD (distinct plot and build) joined to plots at the save; build_info; improvement_info upgrade chains [game3] |
| `d.game4_replacements` | table, 13 values | distinct plots | human | orders over the game; plots at the save | 13 | ordered improvements now replaced by another (not by their own upgrade): what stands there, and whether the human later ordered that build on the same plot [game4] |
| `d.game3_replacements` | table, 5 values | distinct plots | human | orders over the game; plots at the save | 5 | ordered improvements now replaced by another (not by their own upgrade): what stands there, and whether the human later ordered that build on the same plot [game3] |
| `d.game4_land_use` | table, 6 values | tiles at save | all players | save | 6 | plots at the save, by owner (the human, any AI, nobody) and land or water (plot type 3) [game4] |
| `d.game3_land_use` | table, 6 values | tiles at save | all players | save | 6 | plots at the save, by owner (the human, any AI, nobody) and land or water (plot type 3) [game3] |
| `d.game4_worked_yield` | table, 4 values | food per tile | all players | save | 4 | worked plots at the save; food, hammers and commerce are separate columns (each a mean per worked tile) [game4] |
| `d.game3_worked_yield` | table, 4 values | food per tile | all players | save | 4 | worked plots at the save; food, hammers and commerce are separate columns (each a mean per worked tile) [game3] |
| `d.game4_improvements_owned` | table, 19 values | tiles at save | all players | save | 19 | plots at the save: every improvement, on land owned by the human or by an AI, worked or not [game4] |
| `d.game3_improvements_owned` | table, 17 values | tiles at save | all players | save | 17 | plots at the save: every improvement, on land owned by the human or by an AI, worked or not [game3] |
| `d.game4_cottage_line` | table, 5 values | tiles at save | all players | save | 5 | plots at the save with a cottage-line improvement; upgrade_progress is in turns of worked progress [game4] |
| `d.game3_cottage_line` | table, 6 values | tiles at save | all players | save | 6 | plots at the save with a cottage-line improvement; upgrade_progress is in turns of worked progress [game3] |
| `d.game4_stale_map` | table, 3 values | tiles at save | human | save | 3 | plots the human has revealed: the improvement it sees against the one there [game4] |
| `d.game3_stale_map` | table, 3 values | tiles at save | human | save | 3 | plots the human has revealed: the improvement it sees against the one there [game3] |
| `d.game4_attitude_to_human` | table, 17 values | xml | AI players | save | 17 | diplo at the save: each AI's attitude toward the human (AttitudeTypes) and its value, war state and plan (WarPlanTypes), and its mean attitude value toward the other AIs it has met [game4] |
| `d.game3_attitude_to_human` | table, 17 values | xml | AI players | save | 17 | diplo at the save: each AI's attitude toward the human (AttitudeTypes) and its value, war state and plan (WarPlanTypes), and its mean attitude value toward the other AIs it has met [game3] |
| `d.game4_memory_of_human` | table, 11 values | xml | AI players | save | 11 | memory at the save (AI_getMemoryCount): counts held by AIs about the human, and about other AIs, by memory type [game4] |
| `d.game3_memory_of_human` | table, 10 values | xml | AI players | save | 10 | memory at the save (AI_getMemoryCount): counts held by AIs about the human, and about other AIs, by memory type [game3] |
| `d.game4_diplo_events` | table, 7 values | deals | human and AI | whole game | 7 | E lines (DiploEventTypes) involving the human, by direction [game4] |
| `d.game3_diplo_events` | table, 7 values | deals | human and AI | whole game | 7 | E lines (DiploEventTypes) involving the human, by direction [game3] |
| `d.game4_deals` | table, 10 values | deals | human | whole game | 10 | deal_items (D lines) with the human as one side; data is the amount or index of the item [game4] |
| `d.game3_deals` | table, 10 values | deals | human | whole game | 10 | deal_items (D lines) with the human as one side; data is the amount or index of the item [game3] |
| `d.game4_resources` | table, 2 values | xml | all players | save | 2 | bonuses at the save: resource kinds available, imported and exported, the human against the mean AI [game4] |
| `d.game3_resources` | table, 2 values | xml | all players | save | 2 | bonuses at the save: resource kinds available, imported and exported, the human against the mean AI [game3] |
| `d.game4_trade_routes` | table, 2 values | cities at save | all players | save | 2 | cities at the save: trade routes and trade commerce per city [game4] |
| `d.game3_trade_routes` | table, 2 values | cities at save | all players | save | 2 | cities at the save: trade routes and trade commerce per city [game3] |
| `d.game4_combat` | table, 3 values | battles | all players | whole game | 3 | C lines; result from the R line directly after (none: no unit died); odds per mille [game4] |
| `d.game3_combat` | table, 2 values | battles | all players | whole game | 2 | C lines; result from the R line directly after (none: no unit died); odds per mille [game3] |
| `d.game4_attack_odds` | table, 5 values | battles | human and AI | whole game | 5 | C lines: attacks by odds band (per mille, bands of 200) and who attacked, with the result from the next line [game4] |
| `d.game3_attack_odds` | table, 5 values | battles | human and AI | whole game | 5 | C lines: attacks by odds band (per mille, bands of 200) and who attacked, with the result from the next line [game3] |
| `d.game4_promotion_depth` | table, 2 values | units at save | all players | save | 2 | units at the save that can fight: promotions per unit, the human against the AIs [game4] |
| `d.game3_promotion_depth` | table, 2 values | units at save | all players | save | 2 | units at the save that can fight: promotions per unit, the human against the AIs [game3] |
| `d.game4_promotions` | table, 10 values | units at save | all players | save | 10 | unit_promotions at the save: the ten promotions most held by the human's units, with the AI's count [game4] |
| `d.game3_promotions` | table, 10 values | units at save | all players | save | 10 | unit_promotions at the save: the ten promotions most held by the human's units, with the AI's count [game3] |
| `d.game4_moves` | table, 4 values | orders | human | whole game | 4 | wl_A MISSION_MOVE_TO: steps from the unit to its target (the larger of the x and y distances) by group size [game4] |
| `d.game3_moves` | table, 3 values | orders | human | whole game | 3 | wl_A MISSION_MOVE_TO: steps from the unit to its target (the larger of the x and y distances) by group size [game3] |
| `d.game4_stacks` | table, 2 values | units at save | all players | whole game | 2 | G lines: stacks near or in enemy land after each player's moves (AI stacks of 3+ military units, human stacks of 2+) [game4] |
| `d.game3_stacks` | table, 2 values | units at save | all players | whole game | 2 | G lines: stacks near or in enemy land after each player's moves (AI stacks of 3+ military units, human stacks of 2+) [game3] |
