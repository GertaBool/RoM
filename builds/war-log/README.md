# Recording games for the war-AI work

This DLL is GitLab `main` after !48: the war log plus the four AI fixes below. It writes a log of your game (with `WAR_LOG` = 1),
which is how I learn from the way you beat the AI, and it has four AI fixes, all on:

| Fix | What changes | Switch in `GlobalDefinesAlt.xml` (default; 0 = off) |
|---|---|---|
| Assault forecast | Next to a city, a stack attacks when the exact chance that this turn's attacks take it is high enough for the leader's personality. Before, it compared summed strengths | `AI_STACK_FORECAST` (500 = 50 %) |
| Attack floor | An AI unit does not attack at under 5 % true win chance, except siege units, or a city the forecast says can fall | `AI_ATTACK_ODDS_FLOOR` (5) |
| Sacrifice choice | A cheap unit is sent first to wear a defender down only when that has the higher expected value. Before, it was sent whenever the best attacker had under 68 % | `AI_SACRIFICE_EV` (1) |
| Visible armies | Land units of another civ that the AI sees inside its borders raise its alert level whatever its attitude. A human's intent counts as at least an even chance of war | `AI_THREAT_VISIBLE_ARMY` (40) |

The switches work even if your `GlobalDefinesAlt.xml` does not list them; these
defaults then apply.

## Setup (once)

1. Copy `CvGameCoreDLL.dll` over `Assets/CvGameCoreDLL.dll` in the mod. Back up the old
   one first.
2. In `Assets/XML/GlobalDefinesAlt.xml`, set `WAR_LOG` to `1`.
3. In `My Documents/My Games/Beyond the Sword/CivilizationIV.ini`, set
   `LoggingEnabled = 1`. The engine writes log files only with this set.
4. Optional: set `AutoSaveInterval = 5` in the same file, for a save every 5 turns.

## After each game

Put these in the shared Drive folder, or in a `.tar`:
- `My Games/Beyond the Sword/Logs/WarLog.log`. Rename it after each game, because the next
  game appends to it.
- The autosaves from `Saves/single/auto` (optional, but they let me see every unit at
  those turns).
- Your notes: a turn number and one sentence whenever the AI does something stupid or
  clever.

## What is logged

The log has one tab-separated line per event, in `Logs/WarLog.log`. The size is about
200 KB for a whole 450-turn Marathon game of 10 AIs.

| Line | Content |
|---|---|
| `H`, `P` | Header: speed, difficulty, map size; then one line per player (civilization, leader, human or not) |
| `T` | Turn and year |
| `W`, `Q` | War declared (with the AI's war plan); peace |
| `C` | Combat: attacker and defender (owner, unit, health, experience), plot (terrain, feature, hills), city defence, odds per mille, units on the plot |
| `R` | Combat result: winner (with health left) and loser |
| `S` | Ranged strike and damage |
| `B` | Bombard: city defence before and after |
| `K`, `Z` | City captured; razed |
| `U` | Unit built |
| `N` | Building built |
| `M` | Each player each turn: cities, population, land, food, hammers, commerce, research, gold per turn, gold, military units, power, score, research slider, golden-age turns left |
| `Y` | City state, for both sides when a war starts and every turn for a player at war with a human: population, hammers, current build, defenders, best defender, defence, the AI's danger count, foreign land units within 2 plots |
| `X` | Tech acquired |
| `G` | After a player's moves, each of its stacks near or in enemy land: composition, role and target. AI stacks of 3+ military units, human stacks of 2+ |
| `A` | Every command of a human player: unit missions (moves, attacks, worker builds by name, pillage), unit commands (upgrade, promote, disband, by name), grouping, city orders and tasks, research, civics, sliders, espionage, war, votes |
| `D`, `E` | Deals a human is part of; diplomacy answers involving a human |

Logging happens only when something happens, so it should not slow the game.
