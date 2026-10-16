# Recording games for the war-AI work

This DLL is built from GitLab `main` after !46. It is the 0018 war AI with the fixes and
!45, plus an optional log of everything that happens in war and every command a human
player gives.

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
| `X` | Tech acquired |
| `G` | After a player's moves, each of its stacks near or in enemy land: composition, role and target. AI stacks of 3+ military units, human stacks of 2+ |
| `A` | Every command of a human player: unit missions (moves, attacks, worker builds, pillage), unit commands (upgrade, promote, disband), grouping, city orders and tasks, research, civics, sliders, espionage, war, votes |
| `D`, `E` | Deals a human is part of; diplomacy answers involving a human |

Logging happens only when something happens, so it should not slow the game.
