# Tools, data, faults and fixes

What I have to work with, what each piece can and cannot show, how I use it, where I have
gone wrong, and what to change so it does not happen again.

## 1. The data

| Source | What it holds | Turns | What it cannot show |
|---|---|---|---|
| War log (`WarLog.log`) | Lines H P T W Q C R S B K Z U N M V Y X G A D E (`builds/war-log/README.md`) | Every turn | Results of human orders. `A` lines are orders as given: no line records an improvement finished, upgraded or pillaged |
| Save (`.CivBeyondSwordSave`) → `sav2dat.py` → `harness.exe save` | `state0.json`: cities and their tiles, units, techs, civics, history series, replay messages | The save's turn only (the history series and replay messages excepted) | Any earlier turn's map state |
| Setup block (`<save>.init`) → `initcore.py` | Options, victories, custom names, civ, leader, team, handicap per slot | Game start | — |
| Scenario map (`.CivBeyondSwordWBSave`) | Starting terrain, plot type, feature, river, resource per plot | Turn 0 | Chopping, new improvements, roads |
| RoM XML → `xmlread.py` → `records.json` | Every record and field, with `_index` in load order | Fixed | Base BTS files the mod does not ship (HurryInfo and others) |
| DLL source (`/home/user/src/rom-0018b`) | The rules: formulas, conditions, defines | Fixed | — |
| BBAI log (harness replay) | Which AI code branch made each choice | Turns after the save | The human; the turns before the save |

Per game:

| Game | War log | Save dump | Setup block | Scenario | BBAI replay |
|---|---|---|---|---|---|
| 1, 2 | yes | no | no | no | no |
| 3 | yes | yes | not read | yes | yes (20 turns) |
| 4 | yes | yes | yes | yes (PAE Europe V Large) | no |

## 2. The tools

**Project pipeline** (in order):

| Step | Tool | Output |
|---|---|---|
| 1 | `toolchain/harness/sav2dat.py` | `.init`, `.game` |
| 2 | `toolchain/harness/initcore.py` | setup per slot |
| 3 | `harness.exe save …` with `HARNESS_HISTORY_DIAG=1` | `state0.json` |
| 4 | `research/ai-warfare/tools/xmlread.py` (on the real `Assets/`, not a symlinked tree) | `records.json` |
| 5 | `tools/gamedata.py` | the fixed table set per game (`games/gameN/*.csv`, `summary.md`) |
| 6 | `tools/decisions.py` | macro figures across games (`decisions/figures.md`) |
| 7 | `tools/micro.py` | micro figures per game (`decisions/micro-gameN.md`) |
| — | `xmlprofile.py`, `wartables.py`, `xmlaudit.py`, `defines.py` | XML field profiles, unit/tech tables, combat audit, all defines with readers |
| — | `wbs2scn.py`, `harness.exe scenario` | constructed test positions |
| — | `build_dll.sh`, `build_harness.sh`, `clang-gate/check.sh` | DLL builds (MSVC 2003 under Wine), whole-file semantic check |

Harness switches: `HARNESS_HISTORY_DIAG`, `HARNESS_VALUE_DIAG`, `HARNESS_SETTLER_DIAG`,
`HARNESS_RESEED`, `HARNESS_ORACLE`, `HARNESS_UNIT_ACTIVITY` and others (`grep getenv
toolchain/harness/*.cpp`).

**Analysis toolkit.** Installed by `toolchain/analysis/setup.sh` at every session start (the
`SessionStart` hook in `.claude/settings.json`), with pinned versions in
`toolchain/analysis/requirements.txt`. Python tools run with `~/.cache/rom-ana/bin/python`.

| Tool | Use | Checked against |
|---|---|---|
| `tools/figlib.py`, `docs.py`, `check_all.py` | figures with unit, actor, turn and source; rendered documents; the commit gate | its own self-test of seven faults |
| `tools/extract.py <log> <db> [--state] [--oracle]` | every field of every war-log line (named from the DLL's format strings), the whole save dump and oracle records into one DuckDB file; each table's rows checked against its source lines | games 1–4: 0 conservation errors; matches `economy.csv` (5406), `battles.csv` (234) and the build orders (276) |
| `toolchain/analysis/seeds.sh <save dir> <out> <turns> <a> <b>` | seeded continuations of a save on all cores, with the oracle; hard-linked copies, own `logs/` per run | same seed twice: identical; template files unchanged |
| `toolchain/analysis/dump.sh <save dir> <out> <human> [dll]` | the full save dump: plots, relations and memories, resources, unit promotions, city trade | old sections byte-identical to the earlier dump |
| `tools/sqlfig.py <spec> <registry> name=db ...` | declared SQL queries (`study/queries.json`) as checked figure tables; one thread and total orders, so reruns are identical | two runs identical; reproduced at every commit |
| `toolchain/analysis/rebuild.sh` | every database, case table, model test and query figure, in order, then render and check (55 s) | `check_all`: 0 errors |
| `tools/seedmetrics.py <out> <metric>` | one value per seed (kills available and made, kill share, exposed value, city fall) for `exper.py` | a sample against itself: p = 1, P = 0.5 |
| `tools/q.py <game dir or db> "<sql>"` | exact SQL (DuckDB) over an `extract.py` database, or over a game's CSVs plus a `cmd` view of the A lines; for exploration, not for documents | builders of build orders, game 4: Worker 202, Javelineer 46 |
| `tools/exper.py a.txt b.txt` | Welch's t-test on ranks, and P(A beats B); refuses fewer than 30 runs a side | Luke's worked example: tied ranks 4.5 and 9 |
| `tools/divaudit.py <DLL src>` | integer divisions by 100; lists small-base cases as candidates, not bugs | finds `CvPlayer::getImprovementUpgradeRate` (19 of 805 divisions listed) |
| SciPy, scikit-learn | tests; rival models (trees, regression) for the cue models | — |
| Hypothesis, pytest | property tests with constructed inputs for producers | — |
| tree-sitter (C++), libclang | syntax and AST queries over the DLL source | — |
| hyperfine | repeated timing with spread, for turn-time comparisons | — |
| GNU parallel | general use; not for Wine: the harness aborts (`free(): invalid pointer`) under it, so `seeds.sh` uses `xargs -P` | — |
| universal-ctags, sqlite3 | symbol index of the DLL; plain SQL from the shell | — |

**Session tools:**
- shell: python3, wine with MSVC 2003, clang;
- file read, search and edit;
- sub-agents for parallel searches;
- GitHub (`gertabool/rom`);
- GitLab: needs to be authorised again in the claude.ai connector settings before I can use it;
- web fetch and search;
- the Drive helpers in the scratchpad (`drive_list.py`, `drive_get.sh`), which keep each
  download in its own directory and treat it as untrusted.

## 3. Which source answers which question

| Question | Source | Join needed |
|---|---|---|
| What did the human order, when | `A` lines (`human_commands.csv`) | unit type is field 0 |
| What exists on a plot at the save | `state0.json` tiles | plot coordinates (missing, see 5.2) |
| What a plot was at the start | scenario map | — |
| What an improvement, unit or civic does | `records.json` | type name |
| How the rule applies (growth, cost, odds) | DLL source | — |
| What the AI decided and why | BBAI log, `Y` and `G` lines | — |
| Outcomes over time (cities, power, gold) | `M`, `K`, `Z`, `X` lines | turn |

## 4. How I will use them, every time

1. **Census before selection.** For every table I use, list every value of every category
   column (every improvement, build, unit, mission, automation type), for the human and for
   the AI, before writing a line about it. Nothing is left out by a hand-picked list.
2. **Name the unit of each count:** order, distinct plot, completed, or present at the save.
   Name the actor (unit type, automated or not), the group, the turn, and the denominator.
3. **Effects from the XML for every type in the census**, generated, not looked up one at
   a time. The rule that applies them comes from the DLL source.
4. **Controls for every comparison.** A "before the war" shift is compared with what else
   explains it (the human's own new cities, the number of cities, the same window in peace).
5. **Description, then reading.** A reading names the facts it rests on and what would
   refute it.
6. **Self-check before delivering:** census complete; every figure carries its unit, actor,
   turn and denominator; every reading carries its test.

## 5. Faults

### 5.1 Faults in my work (game 4 workers, this round)

| Fault | Fact | Category |
|---|---|---|
| Omitted improvement types | `micro.py` section 3 tabulated a hand list (mine, farm, cottage, hamlet, village, winery) and land tiles only. At the save, the human-founded cities' 123 worked tiles hold 31 unimproved, 29 mines, 18 farms, **14 fishing boats**, 7 villages, 6 hamlets, 5 wineries, 3 pastures, 3 quarries, 3 camps, 2 olive farms, 1 workshop, 1 shaft mine. My paragraph left out the **cottage line** (35 cottage orders, the fourth most common build. At the save no tile of a human city holds a cottage; founded cities work 7 villages and 6 hamlets, captured ones 2 hamlets) and fishing boats. It did not say what they do. A cottage upgrades only while the plot is worked (`CvPlot::doImprovementUpgrade`, `isBeingWorked()`). The AI has 84 cottages at the save, 53 of them on unworked tiles | selection before census |
| Orders counted as improvements | "Mines on hills (42 of 42)" counts orders. 276 build orders cover 242 distinct plot and build pairs. Completion is not logged | wrong unit of count |
| Builder ignored | Of the 276 build orders: Workers 202, Javelineers 46, Rome Legionaries 10, Workboats 9, Hastati 7, Principes 2. The early camps and tracks were mostly Javelineers' | missing join (actor) |
| Automation ignored | 8 orders put Workboats on `AUTOMATE_BUILD` (enum 0), so most fishing boats were not ordered one by one: 20 lie in the human's cities at the save, against 9 build orders. Land workers were never automated | missing join (automation) |
| Yield figure misstated | 9.32 was food + hammers + commerce summed, on land tiles of founded cities only. Captured cities: 6.93. AI: 7.89 | wrong unit, hidden selection |
| Road shift read as war preparation | The 268 count includes cities captured or founded later. Roads near the target also connect the human's new border cities (30,19 founded 250; 19,29 founded 254) | no control |

Earlier faults of the same kinds:
- names taken from the XML type order (load order);
- `xmlread` run on a symlinked tree (8 files read);
- founded and captured cities mixed up;
- strongest unit used where most-built was meant.

The categories recur: **selection before census** and **missing join**. That is why steps 1
and 2 of section 4 are now fixed steps.

### 5.2 Faults in the tools

| Tool | Fault | Effect |
|---|---|---|
| `HarnessState.cpp` tile dump | Writes no plot coordinates, and only plots the city works or could work, in city-index order | Orders cannot be joined to what exists at the save. Matching tiles to plots by terrain and hills left 185 of 205 cities ambiguous; adding feature and resource compatibility still left 55 of the human's 256 tiles unresolved and 7 cities unmatched |
| Dump | No plot owner, route, upgrade progress or pillage state | Roads, cottage growth and pillage cannot be read at the save |
| War log | No line for an improvement or route finished, upgraded or pillaged | Orders only, never outcomes |
| `micro.py`, `decisions.py` | Hand-coded type lists; some figures without denominators | Omissions like the one above |
| `records.json` | Base BTS XML absent | Hurry and similar effects need the BTS files |
| Harness replay of a save | Human seats are handed to the AI | Says nothing of the human after the save |

## 6. Optimisations

Ranked by what they fix per hour.

1. **`census.py`** (analysis only, no build). Writes every value of every category column of
   every table, by group, and of every `A` line kind with its actor and automation flag.
   `micro.py` and `decisions.py` then loop over census values instead of fixed lists.
2. **`effects.py`** (analysis only). For every type in the census, writes the XML fields that
   matter, with game-speed scaling applied where the DLL applies it (for example
   `CvGame::getImprovementUpgradeTime`: `iUpgradeTime` × speed `iImprovementPercent` × start
   era `iImprovementPercent`). This is the automation for unambiguous XML stats.
3. **Builds table with actor.** `gamedata.py` writes `human_builds.csv` with unit type,
   distinct-plot flag and repeat count, and a separate automation table.
4. **Plot dump in the harness:** x, y, owner, working city, improvement, route, upgrade
   progress for every plot. This needs a rebuild of the harness DLL, which CLAUDE.md rule 1
   forbids for an analysis, so it waits for your go-ahead. It would settle completion,
   growth, roads and pillage at the save.
5. **War-log lines for outcomes:** improvement and route finished, upgraded and pillaged.
   This is a change to the DLL you play with, so it is your call. It would give outcomes over
   time instead of only at the save.
6. **One script per game** that runs steps 1–7 of section 2 in order, so the tables never
   come from different versions of a tool.

## 7. Data gaps found in the audit of every source against the scripts

| Gap | Fact | Remedy |
|---|---|---|
| Lines never extracted before `extract.py` | G (stacks), S (ranged strikes), B (bombards); the dump's turn-by-turn history, units, replay messages, costs and economy split | now in the database |
| War plan never recorded | the W lines carried `-1` in every declaration: `warLogWar` logged the argument of `CvTeam::declareWar`, which most callers pass as `NO_WARPLAN` | fixed: the plan the team holds as it declares is logged (`fixes/war-log-warplan.patch`). Verified on a 20-turn continuation of game 3: the three declarations show plans 4 and 5 (limited, total) instead of `-1`, and every other line of the log is identical. In the harness builds now; for the DLL the user plays it needs a GitLab merge (the shipped DLL's commit is not in the local clone, so it is not rebuilt here) |
| Plots of tiles | the dump had no coordinates | fixed: `HarnessState.cpp` writes every plot (`toolchain/analysis/dump.sh`; `HARNESS_HUMAN` names the human seat, which the harness hands to the AI) |
| Combat results | `gamedata.py` matched results to combats by turn, owners and unit types: a fight inherited the result of another between the same types that turn (game 4: 204 attacker wins counted, 163 true; 20 were withdrawals with no death) | fixed: the result is the R line written directly after the C line; every `battles.csv` regenerated |
| AI decisions in the human's war | not measured before | the oracle on seeded continuations of the user's saves (`seeds.sh`) |
