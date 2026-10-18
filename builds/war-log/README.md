# Recording games for the war-AI work

This DLL is GitLab `main` (d51ff25) plus the war-log snapshot change (branch
`claude/war-log-snapshot`, merge requests !51 (merged) and !52, patches `fixes/war-log-snapshot.patch` and
`fixes/war-log-build-id.patch`), build `7c35ba03ea0e`: the war log, which now also
records, as each of your turns begins, every unit you have, every foreign city near your
army with its defenders and the engine's own chance of taking it, and your relations to
every civilization you have met. It writes a log of your game (with `WAR_LOG` = 1), which
is how I learn from the way you beat the AI, and it has four AI fixes, all on:

| Fix | What changes | Switch in `GlobalDefinesAlt.xml` (default; 0 = off) |
|---|---|---|
| Assault forecast | Next to a city, a stack attacks when the exact chance that this turn's attacks take it is high enough for the leader's personality. Before, it compared summed strengths | `AI_STACK_FORECAST` (500 = 50 %) |
| Attack floor | An AI unit does not attack at under 5 % true win chance, except siege units, or a city the forecast says can fall | `AI_ATTACK_ODDS_FLOOR` (5) |
| Sacrifice choice | A cheap unit is sent first to wear a defender down only when that has the higher expected value. Before, it was sent whenever the best attacker had under 68 % | `AI_SACRIFICE_EV` (1) |
| Visible armies | Land units of another civ that the AI sees inside its borders raise its alert level whatever its attitude. A human's intent counts as at least an even chance of war | `AI_THREAT_VISIBLE_ARMY` (40) |


## Setup (once)

1. Copy `CvGameCoreDLL.dll` over `Assets/CvGameCoreDLL.dll` in the mod. Back up the old
   one first.
2. Copy `GlobalDefinesAlt.xml` over `Assets/XML/GlobalDefinesAlt.xml`. It is GitLab
   `main`'s file with `WAR_LOG` set to `1`; the AI fix switches are in it too, and
   `WAR_LOG_SEAT` = `0` (it is for headless test games and does nothing in yours).
3. In `My Documents/My Games/Beyond the Sword/CivilizationIV.ini`, set
   `LoggingEnabled = 1`. The engine writes log files only with this set.
4. Optional: set `AutoSaveInterval = 5` in the same file, for a save every 5 turns.

Start each game you record with this DLL, from turn 0. Only such games count as evidence for
the war-AI fixes: the log must cover the whole game, and its `H` line must name this build.

## After each game

Put these in the shared Drive folder, or in a `.tar`:
- `My Games/Beyond the Sword/Logs/WarLog.log`. Rename it after each game, because the next
  game appends to it.
- The autosaves from `Saves/single/auto` (optional, but they let me see every unit at
  those turns).
- Your notes: a turn number and one sentence whenever the AI does something stupid or
  clever.

## What is logged

The log has one tab-separated line per event, in `Logs/WarLog.log`. The event lines come
to about 200 KB for a whole 450-turn Marathon game of 10 AIs. The turn-start lines (`I`,
`L`, `J`, `O`) add about 10 KB per turn for a civilization of 44 units (measured on 20
turns of game 3), growing with the number of your units: a few MB for a whole game.

| Line | Content |
|---|---|
| `H`, `P` | Header: speed, difficulty, map size and the build that writes the log (`7c35ba03ea0e` for this DLL; earlier DLLs leave it out); then one line per player (civilization, leader, human or not) |
| `T` | Turn and year |
| `W`, `Q` | War declared, with the declaring team's war plan (`WarPlanTypes`; `-1` when it held none; DLLs before !50 always wrote `-1`); peace |
| `C` | Combat: attacker and defender (owner, unit, health, experience), plot (terrain, feature, hills), city defence, odds per mille, units on the plot |
| `R` | Combat result: winner (with health left) and loser |
| `S` | Ranged strike and damage |
| `B` | Bombard: city defence before and after |
| `K`, `Z` | City captured; razed |
| `U` | Unit built |
| `N` | Building built |
| `M` | Each player each turn: cities, population, land, food, hammers, commerce, research, gold per turn, gold, military units, power, score, research slider, golden-age turns left |
| `V` | Great person born, or used: golden age, discover, join a city, build, hurry, trade, great work |
| `Y` | City state, for both sides when a war starts and every turn for a player at war with a human: population, hammers, current build, defenders, best defender, defence, the AI's danger count, foreign land units within 2 plots |
| `X` | Tech acquired |
| `G` | After a player's moves, each of its stacks near or in enemy land: composition, role and target. AI stacks of 3+ military units, human stacks of 2+ |
| `A` | Every command of a human player: unit missions (moves, attacks, worker builds by name, pillage), unit commands (upgrade, promote, disband, by name), grouping, city orders and tasks, research, civics, sliders, espionage, war, votes |
| `D`, `E` | Deals a human is part of; diplomacy answers involving a human |
| `F` | City founded: owner, plot, turn founded, population. When a log begins, one `F` line for every city standing then, so a log started from a save knows every city |
| `I` | As your turn begins (after healing and production, before your moves): a header with the counts of the `L`, `J` and `O` lines that follow |
| `L` | One line per unit: owner, unit id, type, plot, health, experience, level, its group (head unit's id and size), the ship carrying it and units it carries, fortify turns, moves left, the group's activity and automation, its first queued mission with target (where a stack is heading), promotions. Your units, then the defenders of each `J` city |
| `J` | Each foreign city with one of your land units that can attack within 3 plots: owner, plot, population, defence %, whether you see it, whether you are at war, defenders, your units within 1 and within 3 plots (and on ships nearby), and the engine's assault forecast for each group: the chance that they would take the city if they attacked now, one after another, and the units you would expect to lose |
| `O` | Each civilization you have met: war, open borders, defensive pact, vassalage, their war plan against you and yours against them, your war weariness against them |

Lines written before this change keep their fields. Fields added at the end:
- `C`: the ids of attacker and defender;
- `U`: the new unit's id, experience, level and promotions;
- `A` unit missions, automations and commands: the unit's id.

They join every combat, every new unit and every order to the unit lines.

Logging happens only when something happens, and the turn-start lines read only what the
game already holds (no AI calculation, no random number), so they do not change the game.
