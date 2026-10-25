<!-- Rendered by method/docs.py from analysis.md.in. Do not edit; edit the template. -->
# Game 5: Maglocunus (Britain) on PAE Europe, Noble

Method: `method/docs/framework.md` and `method/docs/data-protocol.md`. The queries are declared in
`games/game5/queries.json` and turned into figures by `tools/sqlfig.py`; the war-decision cases come
from `tools/hmwar.py` (`study/model.md`). Facts come first; the readings are in section 7, each with
the facts it rests on and what would contradict it.

Inputs, from the shared folder of this game: the war log (`WarLog.log`), three autosaves of the
human's (`Maglocunus BC-0935`, `Maglocunus BC-0725`, `Maglocunus BC-0400`) and the game's Python
log (`PythonDbg.log`). The last save is dumped with `toolchain/analysis/dump.sh` (the state at its
turn); the two earlier saves are not used yet.

## 1. Questions

- **Q1. Setup.** Which map, speed, difficulty, options and players? Source: the game setup stored in
  the last save (`toolchain/harness/initcore.py`), the `H` and `P` lines, the save dump.
- **Q2. The whole game.** Who grew, who fought whom, who lost cities? Source: `M`, `W`, `Q` and `K`
  lines; the save's replay messages.
- **Q3. The human.** Where did its cities come from, and how did its war go? Source: `A`, `K`, `C`
  and `R` lines, with the queries of `study/winning.md`, `study/playstyle.md` and `study/data.md`
  applied unchanged.
- **Q4. The turn-start lines.** This is the first game logged with them. What do they hold before
  and during the human's war, and can the war-decision cases of `study/model.md` be built from them?
  Source: `I`, `L`, `J` and `O` lines; `tools/hmwar.py`.
- **Q5. The mission.** Does the game count as evidence for P2? Source: `method/ledger.py`.

## 2. Setup

From the setup in the last save (read with `initcore.py`):
- **Map:** the WorldBuilder scenario `PAE Europe V Large`, the map of game 4.
- **Speed and difficulty:** Marathon; Noble for every player.
- **Options:** no barbarians, no vassal states, no events, no revolution, no barbarian
  civilizations, no tech diffusion, dynamic civilization names.
- **Victories:** score, conquest, religious, space race.
- **The human:** the first seat of the list: England's civilization with Henry VIII as leader,
  renamed Maglocunus, "British Tribe". In game 4 on the same map the human played Rome at Monarch.
- **The AIs:**
  - Vercingetorix (Gaul) and Willem van Oranje (Frisia), the two civilizations whose cities the
    human's war took;
  - Pericles (Athens) and Alexander (Macedon); Julius Caesar (Rome); Ivan (Scythia); Ashur
    (Assyria); Masinissa (Carthage); Suppi (Hittites); Hiram (Phoenicia); Ramesses (Egypt); Ragnar
    (Vikings); Charles V (Saxony); Leonidas (Dorian Greece); Afonso (Iberia); Minos (Minoan Tribe);
    Cyrus (Persia); Gilgamesh (Sumer).

### 2.1 The log's header

| turn | speed | handicap | width | height | build | p_lines | human_p_lines |
|---|---|---|---|---|---|---|---|
| 0 | GAMESPEED_MARATHON | HANDICAP_NOBLE | 0 | 0 | none | 1 | 1 |

*lines; who: the log; turn: log start; rows counted: 1; source: H line and the number of P lines that follow it [game5]. Every value counted (1).*

The header names a map of no width or height, and one player, the human. The lines of every type,
with the first and last turn each appears:

| line | n | first_turn | last_turn |
|---|---|---|---|
| A | 1964 | 0 | 270 |
| C | 57 | 136 | 268 |
| D | 66 | 100 | 270 |
| E | 87 | 31 | 270 |
| F | 177 | 0 | 270 |
| G | 24 | 207 | 269 |
| I | 271 | 0 | 270 |
| J | 51 | 210 | 270 |
| K | 12 | 144 | 259 |
| L | 4140 | 1 | 270 |
| M | 5031 | 0 | 269 |
| N | 608 | 70 | 269 |
| O | 1092 | 31 | 270 |
| P | 1 |  |  |
| Q | 1 | 197 | 197 |
| R | 56 | 136 | 268 |
| T | 270 | 0 | 269 |
| U | 1352 | 7 | 269 |
| V | 58 | 178 | 269 |
| W | 5 | 133 | 258 |
| X | 429 | 0 | 269 |
| Y | 133 | 133 | 258 |

*lines; who: all players; turn: log start to last logged turn; rows counted: 22; source: every line of the war log by type (extract.py tables wl_<type>), with the first and last turn each type appears (none for P lines, which carry no turn) [game5]. Every value counted (22).*

How the header came to be written so, from the code (`CvGameCoreUtils.cpp`, `CvPlayer.cpp`, as of
commit `0f89732`):
- the header is written once, before the first line of the log (`warLogLine`);
- the `P` lines list the players that have ever been alive at that moment (`isEverAlive`);
- during game setup the first player to come alive gets its turn at once (`CvPlayer::setAlive`
  calls `setTurnActive(true)` while no turn is active);
- `setTurnActive` writes the tracked player's turn-start lines (`warLogTurnStart`).

With the human in the first seat, its turn-start lines were the log's first line, written before
the map and the other players existed. That snapshot holds no units. Game 3 and game 4 were logged
before the turn-start lines existed, and their headers are complete. The snapshot DLL wrote this
log. The build that fixes it (`a1d2e324699d`, commit `efcb5e4`,
[its merge request](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/53))
writes no turn-start lines before the game has finished its setup.

### 2.2 The players at the save

| player | leader | human | cities | units |
|---|---|---|---|---|
| 0 | LEADER_HENRY_VIII | 1 | 20 | 54 |
| 2 | LEADER_PERICLES | 0 | 7 | 34 |
| 3 | LEADER_JULIUS_CAESAR | 0 | 14 | 62 |
| 4 | LEADER_IVAN | 0 | 9 | 63 |
| 5 | LEADER_ASHUR | 0 | 13 | 81 |
| 6 | LEADER_ALEXANDER | 0 | 10 | 46 |
| 7 | LEADER_MASINISSA | 0 | 12 | 63 |
| 9 | LEADER_SUPPI | 0 | 7 | 41 |
| 10 | LEADER_JOAO | 0 | 10 | 59 |
| 11 | LEADER_RAMESSES | 0 | 8 | 72 |
| 12 | LEADER_RAGNAR | 0 | 7 | 36 |
| 13 | LEADER_CHARLES_V | 0 | 12 | 69 |
| 14 | LEADER_LEONIDAS | 0 | 7 | 23 |
| 15 | LEADER_AFONSO | 0 | 9 | 32 |
| 16 | LEADER_HANNIBAL | 0 | 6 | 28 |
| 17 | LEADER_CYRUS | 0 | 11 | 70 |
| 18 | LEADER_GILGAMESH | 0 | 15 | 95 |

*category; who: all players; turn: save (turn 270); rows counted: 17; source: the save dump (toolchain/analysis/dump.sh): players alive at the save, their leader, human flag, cities and units at the save [game5]. Every value counted (17).*

| turn | player | text |
|---|---|---|
| 216 | 1 | The Gallic Civilization has been destroyed!!! |
| 224 | 8 | The Frisian Civilization has been destroyed!!! |

*category; who: all players; turn: as logged; rows counted: 2; source: replay messages in the save dump (civilization destroyed) [game5]. Every value counted (2).*

## 3. The whole game

Each player's cities at three turns, and score and power at the last full turn (empty: the player
was gone by then):

| player | cities_100 | cities_200 | cities_last | score_last | power_last | last_m_turn |
|---|---|---|---|---|---|---|
| 0 | 1 | 7 | 19 | 736 | 765 | 269 |
| 1 | 1 | 1 |  |  |  | 216 |
| 2 | 1 | 2 | 7 | 195 | 245 | 269 |
| 3 | 1 | 5 | 13 | 291 | 372 | 269 |
| 4 | 1 | 3 | 9 | 231 | 353 | 269 |
| 5 | 1 | 5 | 13 | 352 | 462 | 269 |
| 6 | 1 | 3 | 10 | 202 | 220 | 269 |
| 7 | 2 | 4 | 13 | 258 | 288 | 269 |
| 8 | 2 | 5 |  |  |  | 223 |
| 9 | 1 | 3 | 7 | 211 | 261 | 269 |
| 10 | 2 | 6 | 10 | 220 | 296 | 269 |
| 11 | 1 | 4 | 8 | 315 | 514 | 269 |
| 12 | 1 | 5 | 7 | 235 | 242 | 269 |
| 13 | 2 | 4 | 11 | 287 | 360 | 269 |
| 14 | 2 | 5 | 7 | 142 | 113 | 269 |
| 15 | 1 | 3 | 8 | 162 | 125 | 269 |
| 16 | 1 | 4 | 6 | 162 | 162 | 269 |
| 17 | 1 | 5 | 11 | 332 | 458 | 269 |
| 18 | 1 | 5 | 15 | 410 | 606 | 269 |

*cities; who: all players; turn: turns 100 and 200 and the last full turn; rows counted: 19; source: M lines (end of each player turn): cities per player at turns 100, 200 and the last full turn, and score and power at the last full turn (empty: no M line, the player was gone) [game5]. Every value counted (19).*

Every war and peace of the game:

| turn | kind | team | target | warplan |
|---|---|---|---|---|
| 133 | war | 14 | 2 | 4 |
| 197 | peace | 14 | 2 | -1 |
| 207 | war | 8 | 1 | 5 |
| 210 | war | 0 | 8 | -1 |
| 250 | war | 4 | 2 | 4 |
| 258 | war | 6 | 14 | 5 |

*lines; who: all teams; turn: as logged; rows counted: 6; source: W lines (declarer team, target team, the declarer's war plan; -1 for a human) and Q lines (peace) [game5]. Every value counted (6).*

Every city that changed hands:

| turn | old_owner | new_owner | x | y | pop |
|---|---|---|---|---|---|
| 144 | 14 | 2 | 38 | 23 | 1 |
| 176 | 2 | 14 | 38 | 23 | 2 |
| 210 | 8 | 0 | 20 | 44 | 7 |
| 216 | 1 | 8 | 16 | 36 | 1 |
| 219 | 8 | 0 | 19 | 42 | 8 |
| 220 | 8 | 0 | 14 | 39 | 2 |
| 222 | 8 | 0 | 9 | 38 | 1 |
| 223 | 8 | 0 | 12 | 36 | 7 |
| 223 | 8 | 0 | 23 | 45 | 5 |
| 224 | 8 | 0 | 16 | 36 | 1 |
| 224 | 8 | 0 | 24 | 48 | 2 |
| 259 | 14 | 6 | 38 | 23 | 2 |

*cities; who: all players; turn: as logged; rows counted: 12; source: K lines: city captured (turn, old owner, new owner, plot, population) [game5]. Every value counted (12).*

## 4. The human

Human against the AI median, every fiftieth turn and the last full turn (the query of
`study/winning.md`):

| turn | human_cities | ai_cities | human_commerce | ai_commerce | human_research | ai_research | human_power | ai_power | human_score_rank | human_power_rank | players |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 1.0 | 16 | 16.0 | 10 | 10.0 | 2 | 4.0 | 2 | 14 | 19 |
| 50 | 1 | 1.0 | 26 | 22.0 | 20 | 14.5 | 15 | 9.0 | 7 | 1 | 19 |
| 100 | 1 | 1.0 | 24 | 25.0 | 18 | 18.5 | 28 | 17.5 | 3 | 1 | 19 |
| 150 | 4 | 3.0 | 37 | 38.5 | 36 | 32.0 | 41 | 37.5 | 2 | 7 | 19 |
| 200 | 7 | 4.0 | 133 | 60.5 | 109 | 48.5 | 117 | 72.0 | 1 | 2 | 19 |
| 250 | 17 | 7.0 | 1041 | 154.5 | 760 | 129.0 | 485 | 211.0 | 1 | 1 | 17 |
| 268 | 19 | 9.5 | 2286 | 192.0 | 2018 | 161.5 | 765 | 292.0 | 1 | 1 | 17 |

*cities; who: human and AI; turn: every 50th turn and the last full turn; rows counted: 7; source: M lines (end of each player's turn): the human's value, the median AI's, and the human's rank among all players by score and by power (study/queries_win.json, trajectory) [game5]. Every value counted (7).*

Where its cities came from:

| period_from | founded | captured | lost | razed |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 |
| 100 | 3 | 0 | 0 | 0 |
| 150 | 3 | 0 | 0 | 0 |
| 200 | 2 | 8 | 0 | 0 |
| 250 | 3 | 0 | 0 | 0 |

*cities; who: human; turn: by 50-turn period; rows counted: 5; source: cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) (study/queries_win.json, city_sources) [game5]. Every value counted (5).*

Its one war, and the battles in it:

| t_start | declared_by | opp | turns | cities_taken | human_attacks | human_wins | ai_attacks | human_units_lost | power_ratio |
|---|---|---|---|---|---|---|---|---|---|
| 210 | human | 8 | 59 | 8 | 26 | 21 | 1 | 3 | 1.348 |

*battles; who: human and AI; turn: each war of the human; rows counted: 1; source: W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) (study/queries_win.json, war_ledger) [game5]. Every value counted (1).*

| side | battles | enemy_units_killed | human_units_lost | no_death |
|---|---|---|---|---|
| human attacking | 26 | 21 | 2 | 3 |
| human defending | 1 | 0 | 1 | 0 |

*battles; who: human; turn: whole game; rows counted: 2; source: C lines with the R line directly after: units the human's attacks and defences killed and lost (study/queries_win.json, units_ledger) [game5]. Every value counted (2).*

The units it attacked with:

| att_unit | battles | won | lost | median_odds_per_mille | median_experience | against_city_defence |
|---|---|---|---|---|---|---|
| CELTIC_WARBAND | 25 | 20 | 2 | 980.0 | 10.0 | 13 |
| GALLEY | 1 | 1 | 0 | 996.0 | 6.0 | 0 |

*battles; who: human; turn: whole game; rows counted: 2; source: C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus (study/queries_style.json, attack_units) [game5]. Every value counted (2).*

| UnitInfo | Fields set (records.json) |
|---|---|
| CELTIC_WARBAND | `Advisor` ADVISOR_MILITARY; `BonusProductionModifiers` [{"BonusType":"BONUS_COPPER","iProductonModifier":15},{"BonusType":"BONUS_IRON","iProductonModifier":15}]; `Class` UNITCLASS_CELTIC_WARBAND; `Combat` UNITCOMBAT_MELEE; `DefaultUnitAI` UNITAI_COUNTER; `Domain` DOMAIN_LAND; `FormationType` FORMATION_TYPE_DEFAULT; `FreePromotions` [{"PromotionType":"PROMOTION_GUERILLA1","bFreePromotion":true},{"PromotionType":"PROMOTION_GUERILLA2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN1","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN2","bFreePromotion":true},{"PromotionType":"PROMOTION_WOODSMAN3","bFreePromotion":true},{"PromotionType":"PROMOTION_LOOTER","bFreePromotion":true}]; `PrereqTech` TECH_BRONZE_WORKING; `TechTypes` ["TECH_RELIGION_CELTIC"]; `UnitAIs` [{"UnitAIType":"UNITAI_RESERVE","bUnitAI":true},{"UnitAIType":"UNITAI_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_CITY_COUNTER","bUnitAI":true},{"UnitAIType":"UNITAI_ATTACK_CITY","bUnitAI":true},{"UnitAIType":"UNITAI_PILLAGE","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_CELTIC_SWORDSMAN","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_SCHILDTRAEGER_CELTIC","iRequired":3}],"fMaxSpeed":"1.75","fPadTime":"1","iGroupSize":3,"iMeleeWaveSize":3,"iRangedWaveSize":0}; `bMilitaryHappiness` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `iAdvancedStartCost` 100; `iAsset` 2; `iCombat` 6; `iCombatLimit` 100; `iConscription` 3; `iCost` 40; `iCultureGarrison` 4; `iMinAreaSize` -1; `iMoves` 2; `iNukeRange` -1; `iPower` 10; `iXPValueAttack` 6; `iXPValueDefense` 3 |
| GALLEY | `Advisor` ADVISOR_MILITARY; `Class` UNITCLASS_GALLEY; `Combat` UNITCOMBAT_WOODEN_SHIPS; `DefaultUnitAI` UNITAI_ASSAULT_SEA; `Domain` DOMAIN_SEA; `DomainCargo` DOMAIN_LAND; `FormationType` FORMATION_TYPE_MACHINE; `PrereqTech` TECH_SAILING; `TerrainImpassables` [{"TerrainType":"TERRAIN_OCEAN","bTerrainImpassable":true}]; `UnitAIs` [{"UnitAIType":"UNITAI_ASSAULT_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SETTLER_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_MISSIONARY_SEA","bUnitAI":true},{"UnitAIType":"UNITAI_SPY_SEA","bUnitAI":true}]; `UnitClassUpgrades` [{"UnitClassUpgradeType":"UNITCLASS_GALLEON","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_FLUYT","bUnitClassUpgrade":true},{"UnitClassUpgradeType":"UNITCLASS_COG","bUnitClassUpgrade":true}]; `UnitMeshGroups` {"UnitMeshGroup":[{"EarlyArtDefineTag":"ART_DEF_UNIT_GALLEY","iRequired":1}],"fMaxSpeed":"2.25","fPadTime":"1","iGroupSize":1,"iMeleeWaveSize":1,"iRangedWaveSize":1}; `bMechanized` True; `bMilitaryProduction` True; `bMilitarySupport` True; `bPillage` True; `bRenderBelowWater` True; `iAdvancedStartCost` 100; `iAsset` 1; `iCargo` 4; `iCombat` 3; `iCombatLimit` 100; `iCost` 25; `iMinAreaSize` 20; `iMoves` 4; `iNukeRange` -1; `iPower` 4; `iXPValueAttack` 6; `iXPValueDefense` 3 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

Every attack of the game by odds band, the human's and the AIs':

| odds_from | human_attacks | human_won | ai_attacks | ai_won |
|---|---|---|---|---|
| 0 | 0 | 0 | 2 | 0 |
| 200 | 0 | 0 | 9 | 3 |
| 400 | 1 | 1 | 3 | 1 |
| 600 | 6 | 4 | 4 | 1 |
| 800 | 19 | 16 | 13 | 13 |

*battles; who: human and AI; turn: whole game; rows counted: 5; source: C lines: attacks by odds band (per mille, bands of 200) and who attacked, with the result from the next line (study/queries.json, attack_odds) [game5]. Every value counted (5).*

What the human ordered in the turns before its declaration, against the turns before that:

| turn | target | train_10_before | train_per_10_earlier | upgrades_10_before | upgrades_per_10_earlier | moves_10_before | moves_per_10_earlier |
|---|---|---|---|---|---|---|---|
| 210 | 8 | 12 | 2.8 | 1 | 0.2 | 22 | 14.6 |

*orders; who: human; turn: the ten turns before each declaration, against the fifty before those; rows counted: 1; source: A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those (study/queries_style.json, war_preparation) [game5]. Every value counted (1).*

The Python log holds the game's debug messages (interface, BUG mod data, timers); it has no
error and no traceback.

## 5. The turn-start lines

The lines the human's turn starts wrote, by period:

| period_from | turn_starts | unit_lines | j_lines | defender_lines | o_lines |
|---|---|---|---|---|---|
| 0 | 30 | 37 | 0 | 0 | 0 |
| 30 | 30 | 72 | 0 | 0 | 29 |
| 60 | 30 | 104 | 0 | 0 | 30 |
| 90 | 30 | 183 | 0 | 0 | 36 |
| 120 | 30 | 237 | 0 | 0 | 63 |
| 150 | 30 | 314 | 0 | 0 | 112 |
| 180 | 30 | 478 | 0 | 0 | 169 |
| 210 | 30 | 1120 | 38 | 73 | 280 |
| 240 | 30 | 1442 | 11 | 22 | 360 |
| 270 | 1 | 55 | 2 | 3 | 13 |

*lines; who: human; turn: each turn start of the human; rows counted: 10; source: I lines (turn-start header: units, J cities, J defenders, O teams), summed by 30-turn period [game5]. Every value counted (10).*

No foreign city came within three plots of the human's attack-capable land units before the turn
of its declaration: the `J` lines begin then. Its relations at that turn start:

| team | war | open_borders | def_pact | vassal | plan_theirs | plan_ours | weariness |
|---|---|---|---|---|---|---|---|
| 2 | 0 | 1 | 0 | 0 | -1 | -1 | 0 |
| 3 | 0 | 1 | 0 | 0 | -1 | -1 | 0 |
| 4 | 0 | 1 | 0 | 0 | -1 | -1 | 0 |
| 8 | 0 | 1 | 0 | 0 | -1 | -1 | 0 |
| 12 | 0 | 1 | 0 | 0 | -1 | -1 | 0 |
| 13 | 0 | 1 | 0 | 0 | -1 | -1 | 0 |
| 17 | 0 | 1 | 0 | 0 | -1 | -1 | 0 |
| 18 | 0 | 0 | 0 | 0 | -1 | -1 | 0 |

*category; who: human; turn: turn start 210 (the declaration turn); rows counted: 8; source: O lines of the human at its turn start 210: every team met, war, open borders, defensive pact, vassal, war plans both ways, war weariness [game5]. Every value counted (8).*

Every Frisian city in a `J` line from the declaration to the last capture: its defenders, the
human's units within one and within three plots and aboard ships nearby, the engine's capture
chance for the units within one and within three plots, and the turn the human took it:

| turn | x | y | pop | def_mod | visible | war | defenders | near1 | near3 | on_ships | capture1 | capture3 | taken_turn |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 210 | 19 | 42 | 8 | 40 | 1 | 0 | 2 | 0 | 0 | 2 | 0 | 0 | 219 |
| 210 | 20 | 44 | 8 | 20 | 1 | 0 | 2 | 0 | 0 | 2 | 0 | 0 | 210 |
| 211 | 19 | 42 | 8 | 40 | 1 | 1 | 2 | 0 | 2 | 0 | 0 | 3 | 219 |
| 211 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 948 | 223 |
| 212 | 19 | 42 | 8 | 40 | 1 | 1 | 3 | 0 | 2 | 0 | 0 | 0 | 219 |
| 212 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 1000 | 223 |
| 213 | 19 | 42 | 8 | 40 | 1 | 1 | 3 | 1 | 2 | 0 | 0 | 0 | 219 |
| 213 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 1000 | 223 |
| 214 | 19 | 42 | 8 | 40 | 1 | 1 | 3 | 0 | 1 | 0 | 0 | 0 | 219 |
| 214 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 992 | 223 |
| 215 | 19 | 42 | 9 | 40 | 1 | 1 | 4 | 2 | 3 | 0 | 0 | 0 | 219 |
| 215 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 992 | 223 |
| 216 | 14 | 39 | 2 | 0 | 0 | 1 | 1 | 0 | 3 | 0 | 0 | 1000 | 220 |
| 216 | 19 | 42 | 9 | 40 | 1 | 1 | 3 | 0 | 4 | 0 | 0 | 746 | 219 |
| 216 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 992 | 223 |
| 217 | 14 | 39 | 2 | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 413 | 220 |
| 217 | 19 | 42 | 9 | 40 | 1 | 1 | 2 | 2 | 4 | 0 | 0 | 872 | 219 |
| 217 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 992 | 223 |
| 218 | 14 | 39 | 2 | 0 | 1 | 1 | 1 | 0 | 3 | 0 | 0 | 1000 | 220 |
| 218 | 19 | 42 | 9 | 40 | 1 | 1 | 2 | 0 | 4 | 0 | 0 | 988 | 219 |
| 218 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 992 | 223 |
| 219 | 14 | 39 | 2 | 0 | 1 | 1 | 1 | 0 | 3 | 0 | 0 | 1000 | 220 |
| 219 | 19 | 42 | 9 | 40 | 1 | 1 | 2 | 3 | 7 | 0 | 904 | 1000 | 219 |
| 219 | 23 | 45 | 5 | 10 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 992 | 223 |
| 220 | 14 | 39 | 3 | 10 | 1 | 1 | 1 | 0 | 4 | 0 | 0 | 1000 | 220 |
| 220 | 23 | 45 | 6 | 10 | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 992 | 223 |
| 221 | 12 | 36 | 8 | 10 | 1 | 1 | 2 | 0 | 2 | 0 | 0 | 823 | 223 |
| 221 | 16 | 36 | 1 | 0 | 0 | 1 | 5 | 0 | 3 | 0 | 0 | 0 | 224 |
| 221 | 23 | 45 | 6 | 10 | 0 | 1 | 2 | 0 | 1 | 0 | 0 | 0 | 223 |
| 222 | 9 | 38 | 2 | 0 | 1 | 1 | 1 | 3 | 3 | 0 | 1000 | 1000 | 222 |
| 222 | 12 | 36 | 8 | 10 | 1 | 1 | 2 | 0 | 6 | 0 | 0 | 1000 | 223 |
| 222 | 16 | 36 | 1 | 0 | 1 | 1 | 5 | 1 | 4 | 0 | 0 | 0 | 224 |
| 222 | 23 | 45 | 6 | 10 | 0 | 1 | 2 | 0 | 2 | 0 | 0 | 990 | 223 |
| 223 | 12 | 36 | 8 | 10 | 1 | 1 | 2 | 2 | 7 | 0 | 976 | 1000 | 223 |
| 223 | 16 | 36 | 1 | 0 | 1 | 1 | 4 | 3 | 4 | 0 | 0 | 76 | 224 |
| 223 | 23 | 45 | 6 | 10 | 1 | 1 | 1 | 3 | 4 | 0 | 1000 | 1000 | 223 |
| 224 | 16 | 36 | 1 | 0 | 1 | 1 | 2 | 3 | 4 | 2 | 998 | 1000 | 224 |
| 224 | 24 | 48 | 3 | 0 | 0 | 1 | 2 | 0 | 3 | 0 | 0 | 1000 | 224 |

*lines; who: human against the cities of player 8; turn: each turn start from the declaration (turn 210) to the last capture (turn 224); rows counted: 38; source: J lines of the human: each foreign city within 3 plots of one of its land units that can attack, with the engine's assault forecast (capture chance per mille, expected losses x100) for its units within 1 and within 3 plots, and the turn the human took that city (K line), if it did [game5]. Every value counted (38).*

The first capture, from the `L`, `A` and `C` lines of that turn:
- at the turn start, two Celtic Warbands sat aboard a galley a few plots off the city;
- the human declared war; its next orders moved the galley beside the city, unloaded it and moved
  onto the city;
- both Warbands' attacks won (`C` and `R` lines), and the city fell on the same turn (`K` line).

The `J` line of that turn start lists the two units under "aboard ships". In `warLogTurnStart` a unit
aboard a ship puts the city in a `J` line but is not given to the forecast, which takes only units on
land within one or three plots; so the capture chance reads zero for a city that fell that turn.

### 5.1 The war-decision cases

`tools/hmwar.py` built these cases from the game's turn starts (of 271):

| Class | Cases |
|---|---|
| declare | 0 |
| target | 0 |
| assault | 0 |
| peace | 14 |
| declarations on a team without a city in a `J` line | 1 |

These counts follow from the header. `hmwar.py` takes each player's team from the `P` lines
(`teams`), and this log has the human's only. No owner of a city in a `J` line then has a known
team: no city is a candidate for a declaration, none is an enemy city for an assault, and the
declaration counts as made on a team out of reach. The peace cases come from the `O` lines, which
name teams, but none of them can show a city within reach for the same reason.

## 6. The mission metric

| by_turn | taken | lost |
|---|---|---|
| 217 | 1 | 0 |
| 269 | 8 | 0 |

*cities; who: human; turn: by turn 217 and by the last logged turn; rows counted: 2; source: K lines with the human as new owner (taken) or old owner (lost), counted as method/variables.py v_cities counts them (turn <= the claim turn) [game5]. Every value counted (2).*

The prediction P2 counts a game only if its log names a build made under P2 (`ledger.py`,
`"builds": "served"`). This log names none (the header's build column), so P2 does not count the
game, although it is logged from the first turn, at Noble, with turn-start lines, and past the
claim's turn. The withdrawn P1 made the same claim without the build condition and would have
counted it.

## 7. Readings

- **R1. The human struck when its target was busy.** Facts: the table of wars shows Frisia
  declaring on Gaul a few turns before the human declared on Frisia, and Frisia taking Gaul's last
  city during the human's war. Contradicted if, in the human's other wars, the target was mostly at
  peace with everyone else when the human declared.
- **R2. The opening strike came from the sea, small and at high odds; the turn-start forecast cannot
  see it.** Facts: section 5 (two units aboard a galley, both attacks won, capture on the same turn;
  capture chance zero at that turn start). Contradicted if the human's other declarations come with
  armies already on land next to the target.
- **R3. The war was won with one unit type, attacking only at high odds.** Facts: the attack-unit
  table and the odds bands (most of the human's attacks in the top band), the units ledger.
  Contradicted if a later game shows the human attacking at odds under an even chance as often as
  above.
- **R4. Frisia hardly fought back.** Facts: the war ledger's AI attacks and the units ledger's
  defending row against the human's attacks. Contradicted if Frisia's units were mostly elsewhere
  (at war with Gaul); its unit positions are in the save dumps of the earlier saves, not yet read.

## 8. Open

- **The war-decision cases.** They need each player's team from a source other than the `P` lines
  (the setup in the save, or the `O` lines' teams), in `tools/hmwar.py`. That tool is gated and no
  registered prediction names it, so the change waits for a prediction of the human-model line.
  Games logged with build `a1d2e324699d` have a complete header and need no such change.
- **Models.** `study/model.md` fits each model on all games but one and scores it on the one left
  out; game 5 is the only game with turn-start lines, so no model can be judged yet.
- **The forecast and ships.** Whether the turn-start forecast should count units aboard ships next
  to a city (R2) is a design question for the log; it is not changed here.
- **The earlier saves** (`BC-0935`, `BC-0725`) are not dumped yet.

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `header` | table, 1 values | lines | the log | log start | 1 | H line and the number of P lines that follow it [game5] |
| `log_lines` | table, 22 values | lines | all players | log start to last logged turn | 22 | every line of the war log by type (extract.py tables wl_<type>), with the first and last turn each type appears (none for P lines, which carry no turn) [game5] |
| `players_at_save` | table, 17 values | category | all players | save (turn 270) | 17 | the save dump (toolchain/analysis/dump.sh): players alive at the save, their leader, human flag, cities and units at the save [game5] |
| `eliminations` | table, 2 values | category | all players | as logged | 2 | replay messages in the save dump (civilization destroyed) [game5] |
| `trajectory_all` | table, 19 values | cities | all players | turns 100 and 200 and the last full turn | 19 | M lines (end of each player turn): cities per player at turns 100, 200 and the last full turn, and score and power at the last full turn (empty: no M line, the player was gone) [game5] |
| `wars` | table, 6 values | lines | all teams | as logged | 6 | W lines (declarer team, target team, the declarer's war plan; -1 for a human) and Q lines (peace) [game5] |
| `captures` | table, 12 values | cities | all players | as logged | 12 | K lines: city captured (turn, old owner, new owner, plot, population) [game5] |
| `trajectory` | table, 7 values | cities | human and AI | every 50th turn and the last full turn | 7 | M lines (end of each player's turn): the human's value, the median AI's, and the human's rank among all players by score and by power (study/queries_win.json, trajectory) [game5] |
| `city_sources` | table, 5 values | cities | human | by 50-turn period | 5 | cities the human founded (MISSION_FOUND orders), captured (K lines, new owner) and lost (K lines, old owner) or razed (Z lines) (study/queries_win.json, city_sources) [game5] |
| `war_ledger` | table, 1 values | battles | human and AI | each war of the human | 1 | W/Q lines (wars and peace of the human), K lines (cities), C lines with the R line directly after (battles), M lines (power the turn before; empty without M lines) (study/queries_win.json, war_ledger) [game5] |
| `units_ledger` | table, 2 values | battles | human | whole game | 2 | C lines with the R line directly after: units the human's attacks and defences killed and lost (study/queries_win.json, units_ledger) [game5] |
| `attack_units` | table, 2 values | battles | human | whole game | 2 | C lines with the human attacking and the R line directly after (no R line: no unit died): the attacking unit type, the odds per mille the C line records, the attacker's experience, and battles where the defender had a city defence bonus (study/queries_style.json, attack_units) [game5] |
| `attack_odds` | table, 5 values | battles | human and AI | whole game | 5 | C lines: attacks by odds band (per mille, bands of 200) and who attacked, with the result from the next line (study/queries.json, attack_odds) [game5] |
| `war_preparation` | table, 1 values | orders | human | the ten turns before each declaration, against the fifty before those | 1 | A lines of the human: unit city orders (ORDER type 0), upgrades (COMMAND_UPGRADE) and move orders (MISSION_MOVE_TO) in the ten turns before each W line it declared, against the mean per ten turns over the fifty turns before those (study/queries_style.json, war_preparation) [game5] |
| `snapshot` | table, 10 values | lines | human | each turn start of the human | 10 | I lines (turn-start header: units, J cities, J defenders, O teams), summed by 30-turn period [game5] |
| `relations_210` | table, 8 values | category | human | turn start 210 (the declaration turn) | 8 | O lines of the human at its turn start 210: every team met, war, open borders, defensive pact, vassal, war plans both ways, war weariness [game5] |
| `war_reach` | table, 38 values | lines | human against the cities of player 8 | each turn start from the declaration (turn 210) to the last capture (turn 224) | 38 | J lines of the human: each foreign city within 3 plots of one of its land units that can attack, with the engine's assault forecast (capture chance per mille, expected losses x100) for its units within 1 and within 3 plots, and the turn the human took that city (K line), if it did [game5] |
| `hm.game5_turn_starts` | 271 | turns | human | all logged turns |  | hmwar.py, I lines with new_turn = 1 |
| `hm.game5_declare_cases` | 0 | turns | human | all logged turns |  | hmwar.py, class declare |
| `hm.game5_target_cases` | 0 | lines | human | all logged turns |  | hmwar.py, class target |
| `hm.game5_assault_cases` | 0 | turns | human | all logged turns |  | hmwar.py, class assault |
| `hm.game5_peace_cases` | 14 | turns | human | all logged turns |  | hmwar.py, class peace |
| `hm.game5_declared_out_of_reach` | 1 | lines | human | all logged turns |  | hmwar.py, W lines on a team without a J city |
| `mission_metric` | table, 2 values | cities | human | by turn 217 and by the last logged turn | 2 | K lines with the human as new owner (taken) or old owner (lost), counted as method/variables.py v_cities counts them (turn <= the claim turn) [game5] |
