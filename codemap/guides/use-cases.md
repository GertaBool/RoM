# Using the code map: use cases, compared with code graphs elsewhere

What code maps and code graphs are used for, which of those uses this map serves, how, and what it
cannot do. Written by hand from the map at GitLab commit `ede81881b7de`. Every count below is printed by
`python3 codemap/tool/measure.py <rise-of-mankind checkout> 2a8b9a83eb5b` or by the `query.py` command
shown with it.

Sections 1 to 6 describe. Section 7 holds the readings: what the facts suggest, the facts each rests on,
and what would contradict it.

## Contents

1. [Kinds of code graph](#1-kinds-of-code-graph)
2. [The use cases](#2-the-use-cases)
3. [What this map holds](#3-what-this-map-holds)
4. [Use cases against this map](#4-use-cases-against-this-map)
5. [Worked examples](#5-worked-examples)
6. [What the map cannot answer, and what each answer would need](#6-what-the-map-cannot-answer-and-what-each-answer-would-need)
7. [Readings](#7-readings)
8. [Errors found while writing this guide](#8-errors-found-while-writing-this-guide)
9. [Sources](#9-sources)

## 1. Kinds of code graph

A code graph has program elements as nodes and relations between them as edges. They differ in four
ways: what the nodes are, which relations are edges, how the graph is built, and whether it errs on the
side of too many edges or too few.

| Kind | Nodes | Edges | Typical builders | Answers |
|---|---|---|---|---|
| Symbol index (cross-reference) | definitions, references, documents | reference → definition | SCIP, LSIF, Kythe, ctags, tree-sitter | go to definition, find references, find implementations |
| Call graph | functions | call, address taken | compilers, CodeQL, Doxygen, this map | who calls whom, paths, reachability |
| Class hierarchy | classes, methods | base, override | compilers, type records | which override may run |
| Module / dependency graph | files, packages, modules | include, import, link | build systems, Repository Intelligence Graph | layering, build order, coupling |
| Control-flow graph | basic blocks of one function | jump, fall-through | compilers, Joern | paths inside a function, dominance inside it |
| Data-flow / program dependence graph | statements, variables | definition → use, control dependence | CodeQL, Joern | where a value comes from and goes, taint |
| Code property graph | all of the above in one graph | AST + CFG + data dependence | Joern (Yamaguchi et al.) | vulnerability patterns as graph queries |
| Repository map for language models | files, definitions | references, ranked | Aider (tree-sitter + PageRank), RepoGraph, CodexGraph | what to put in a model's context |
| Dynamic call graph / profile | functions | calls observed at run time, with counts and time | profilers, tracing | where the time goes, what ran |

How a graph is built decides its errors:
- **From text** (ctags, tree-sitter, regular expressions): fast and works on any code. It does not
  resolve overloads, macros, templates or virtual dispatch, so it both misses edges and invents them.
- **From the compiler** (SCIP indexers, CodeQL, compiler listings): each direct call is the one the
  compiler resolved. What is left open is dynamic: virtual calls, function pointers, calls by name.
- **From running the program**: exact for what ran, silent about what did not.

For dynamic calls, analyses choose between **sound** (every possible target, so too many edges) and
**optimistic** (likely targets, so possibly too few). Class Hierarchy Analysis (CHA) is sound and coarse;
Rapid Type Analysis (RTA) keeps only targets of classes the program creates; variable-type and points-to
analyses narrow further. The usual sound treatment of a function pointer is: any function whose address
is taken may be called.

## 2. The use cases

The use cases gathered from the tools and studies in section 9, grouped by the task they serve. Sillito,
Murphy and De Volder catalogued 44 kinds of question programmers ask during change tasks. Most groups
below answer some of them: where is this, who uses this, how does control get from here to there, what
does a change affect.

### A. Navigation and comprehension

| # | Use case | Question | Graph needed |
|---|---|---|---|
| A1 | Find a definition | where is `X` defined? | symbol index |
| A2 | Callers | who calls `X`, directly and transitively? | call graph, reversed |
| A3 | Callees | what does `X` call, down to depth *n*? | call graph |
| A4 | Paths | how does control get from `X` to `Y`? | call graph, path search |
| A5 | Overview | what are the parts and how do they talk? | grouped call or module graph |
| A6 | Key functions | which functions matter most? | centrality (degree, PageRank) or dominance |
| A7 | Dispatch | which override runs for this virtual call? | class hierarchy + call graph |
| A8 | Onboarding | where does a newcomer start? | overview + key functions + entry points |

### B. Changing code

| # | Use case | Question | Graph needed |
|---|---|---|---|
| B1 | Impact analysis | what can a change to `X` affect? | transitive callers (and data flow, for precision) |
| B2 | Regression test selection | which tests can reach the change? | call graph with tests as entry points |
| B3 | Refactoring safety | can `X` be renamed, removed or re-signed? | references, exports, overrides, bindings |
| B4 | Interface contracts | what must stay as it is for an outside caller? | exports, imports, enums, file formats |
| B5 | Rewrite a function | what does a new version have to keep? | callers, callees, hard-coded entries |
| B6 | Review a patch | what does this diff reach? | B1 for the changed functions |

### C. Quality and architecture

| # | Use case | Question | Graph needed |
|---|---|---|---|
| C1 | Dead code | what can never run? | reachability from every entry point |
| C2 | Hotspots | which functions everything depends on, or that depend on everything? | fan-in, fan-out |
| C3 | Cycles | which functions call each other round? | strongly connected components |
| C4 | Layering and coupling | do the parts depend on each other as intended? | module graph, design structure matrix |
| C5 | Architecture recovery | what modules does the code really have? | clustering of the dependency graph |
| C6 | Completeness | is all of the source in the graph? | compare two independent extractions |

### D. Correctness and security

| # | Use case | Question | Graph needed |
|---|---|---|---|
| D1 | Taint and data flow | can untrusted input reach a dangerous call? | data-flow graph, code property graph |
| D2 | Bug patterns | where does this pattern of calls occur? | call graph + AST, or CPG queries |
| D3 | Determinism | can code that should not touch shared state reach it? | call graph to the shared-state functions |
| D4 | Resource lifetime | is everything allocated freed, once? | data flow, or paired functions |

### E. Language and process boundaries

| # | Use case | Question | Graph needed |
|---|---|---|---|
| E1 | Bindings | which script calls land in which native function, and back? | cross-language links |
| E2 | Host boundary | what does the host program call in us, and we in it? | exports, imports, interface calls |
| E3 | Events | which handlers run for an event, and who posts it? | event names linked on both sides |

### F. Language-model agents

| # | Use case | Question | Graph needed |
|---|---|---|---|
| F1 | Map in context | a compact overview the model reads before a task | ranked repository map |
| F2 | Graph-guided retrieval | expand a search hit to its neighbours | call or reference graph |
| F3 | Graph queries as a tool | the agent asks callers, paths, impact | queryable graph (database, MCP server, command line) |

### G. Run-time evidence

| # | Use case | Question | Graph needed |
|---|---|---|---|
| G1 | Profile | where does the time go, along which calls? | dynamic call graph with times |
| G2 | Coverage | what did a test or a game exercise? | dynamic call graph |

## 3. What this map holds

How it is made is in `../README.md`. In short: every unit of `Assets/CvGameCoreDLL` is compiled by the
compiler the DLL is built with (Visual C++ Toolkit 2003, under Wine), without optimisation or inlining.
The tools read the assembly listings, the objects' export directives and the type records. The mod's
Python is parsed by the game's own Python 2.4.

At `ede81881b7de`:

| Content | Size | Table |
|---|---|---|
| Functions defined | 13405, in 178 files; 2447 exported to the exe, 3863 bound for Python | `functions.tsv` |
| Virtual methods called but not defined in the DLL | 645 (pure, or provided by the exe) | `functions.tsv` |
| Direct calls | 151484, each the target the compiler resolved | `calls.tsv` |
| Virtual calls | 17689, of them 10907 with the object's class shown in the code | `calls.tsv` |
| Addresses taken | 4313 (callbacks, function pointers) | `calls.tsv` |
| Classes, bases, overrides | 333 classes, 161 base links, 563 overrides | `classes.tsv`, `bases.tsv`, `overrides.tsv` |
| Calls not tied to one function | 1609: 1430 virtual `delete`, 106 through a function pointer, 56 with several candidates, 17 matching no name | `unresolved.tsv` |
| Python | 277 modules, 6681 functions and classes, 63566 call sites, 0 modules that failed to parse | `py_*.tsv` |
| Python → DLL | 29043 call sites whose name the DLL exposes, 16784 of them with one candidate | `py_to_cpp.tsv` |
| DLL → Python | 183 `callFunction` sites, 130 landing in a Python function found in the mod | `cpp_to_py.tsv` |
| Events | 81 posted, 222 event-handler links | `events.tsv`, `event_handlers.tsv` |
| Hard-coded entries of the 12 key functions | 252, each checked against the file holding its other end | `hardcoded.tsv` |

Its precision, in the terms of section 1:
- Direct calls are exact: overloads, macros, templates and `#ifdef`s are resolved by the compiler.
- Virtual calls are matched by slot, by the method names written in the statement and, where the code
  shows it, by the object's class. Calls follow overrides only in that class and below. Where several
  methods remain, every candidate is kept. This is narrower than CHA when the object's class is known
  and equal to CHA otherwise.
- Function pointers are not followed. The functions whose address is taken are recorded (`ref`).
- Python links are name matches, as Python resolves names when it runs.
- The map is one snapshot, of the commit named at the top of `../skeleton.md`, and holds no run-time
  data.

The ways to read it:
- **Pages:** `../skeleton.md` (overview, groups, backbone), `../entry_points.md`, `../python.md`,
  `../hardcoded.md`, `../files/<file>.md`.
- **Queries:** `../tool/query.py` (`find`, `callers`, `callees`, `path`, `rank`).
- **Tables:** `../map/*.tsv`, tab-separated with a header row, for anything else.

## 4. Use cases against this map

*Yes*: the map answers it as it is. *Partial*: it answers part, or with a known limit. *No*: it does not
hold what the answer needs. Results are at `ede81881b7de`.

| # | Use case | Here | How | Result here |
|---|---|---|---|---|
| A1 | Find a definition | Yes | `query.py find <regex>`; `functions.tsv` file and line | 13405 definitions |
| A2 | Callers | Yes | `query.py callers <f> [depth]` | virtual calls reach overrides of the object's class and below |
| A3 | Callees | Yes | `query.py callees <f> [depth]`; `files/<file>.md` | |
| A4 | Paths | Yes | `query.py path <from> <to>`, a shortest path | example in 5.2 |
| A5 | Overview | Yes | `skeleton.md`: groups by file name, call matrix, backbone two levels deep | 7 groups |
| A6 | Key functions | Yes | `query.py rank [n]`, by dominance | 12 functions; `key-functions.md` |
| A7 | Dispatch | Partial | `overrides.tsv`; ambiguous calls keep every candidate | 56 calls with several candidates |
| A8 | Onboarding | Yes | `skeleton.md`, `entry_points.md`, `key-functions.md` | |
| B1 | Impact analysis | Partial | transitive callers; no data flow | 2a8b9a8 → ede8188: 217 functions changed, 1331 can reach one (5.4) |
| B2 | Test selection | Partial | the mod's `Tools/test_*.py` take named functions out of the DLL source (and 10 compile them); match them to the changed functions | 7 of 33 tests take a changed function (5.11) |
| B3 | Refactoring safety | Partial | callers, `exported`, overrides, `python_defs.tsv` | calls by name from Python, and through pointers, are not exact |
| B4 | Interface contracts | Yes, for the 12 key functions | `hardcoded.md`: exports, exe calls, enums, XML, defines, text keys, Python, logs | 252 entries, none whose other end is missing |
| B5 | Rewrite a function | Yes, for the 12 key functions | `hardcoded.md`, `key-functions.md` | |
| B6 | Review a patch | Partial | B1 for the patch's functions (5.4 shows the method) | |
| C1 | Dead code | Partial | functions no one reaches | 187 candidates (5.5) |
| C2 | Hotspots | Yes | fan-in and fan-out from `calls.tsv` | 209 functions with fan-in ≥ 100 (5.6) |
| C3 | Cycles | Yes | strongly connected components of `calls.tsv` | largest: 215 functions (5.6) |
| C4 | Layering | Partial | `skeleton.md` call matrix between file groups | groups by file name, not by design |
| C5 | Architecture recovery | No | no clustering is computed | the tables would support it |
| C6 | Completeness | Yes | `completeness.tsv` against ctags; `units.tsv` | 273 definitions no unit compiles, 203 that ctags does not see |
| D1 | Taint, data flow | No | no data-flow edges | |
| D2 | Bug patterns | Partial | call patterns only (who calls what, from where) | |
| D3 | Determinism | Yes, for calls | reach of the synchronised random generator (5.7) | 1015 functions can reach it |
| D4 | Resource lifetime | No | `new` and `delete` are calls; who owns what is not | |
| E1 | Bindings | Yes, by name | `python_defs.tsv`, `py_to_cpp.tsv`, `cpp_to_py.tsv` | 16784 of 29043 Python sites with one candidate |
| E2 | Host boundary | Partial | exports and interface calls; which exports the exe uses is not known | 2447 exports |
| E3 | Events | Yes | `events.tsv`, `event_handlers.tsv`, `entry_points.md` | 81 events, 222 links (5.8) |
| F1 | Map in context | Yes | `skeleton.md` (84 KB), `key-functions.md` | ranked by dominance, not PageRank |
| F2 | Graph-guided retrieval | Partial | `files/<file>.md` lists each function's callees and up to 12 callers | no search integration |
| F3 | Graph queries as a tool | Yes | `query.py` from a shell | |
| G1 | Profile | No | no run-time data; the harness has `profile` builds | |
| G2 | Coverage | No | no run-time data | |

## 5. Worked examples

### 5.1 Find and callers (A1, A2)

```
$ python3 codemap/tool/query.py find 'AI_doWar'
9698	CvTeamAI::AI_doWar()	CvTeamAI.cpp:4762
$ python3 codemap/tool/query.py callers 'CvTeamAI::AI_doWar' 1
CvTeamAI::AI_doWar()  [9698] CvTeamAI.cpp:4762
  CvTeamAI::AI_doTurnPost()  [9601] CvTeamAI.cpp:189
```

The war decision has one caller. A change to when wars are considered goes through `AI_doTurnPost`.

### 5.2 How control gets from the game tick to a city's production choice (A4)

```
$ python3 codemap/tool/query.py path 'CvGame::update' 'CvCityAI::AI_chooseProduction'
CvGame::update()  [2248] CvGame.cpp:2176
CvGame::doTurn()  [2518] CvGame.cpp:7059
CvPlayer::setTurnActive(bool, bool)  [7154] CvPlayer.cpp:12162
CvPlayer::doTurn()  [7560] CvPlayer.cpp:3916
CvCity::doTurn()  [475] CvCity.cpp:1230
CvCity::doProduction(bool)  [502] CvCity.cpp:13789
CvCityAI::AI_chooseProduction()  [1225] CvCityAI.cpp:726
```

`path` gives one shortest path. Other paths may exist; `callers` with a depth lists them.

### 5.3 Key functions (A6)

`query.py rank 12` lists the functions that dominate the most others. Function A dominates B when every
call path from outside the DLL into B passes through A. The twelve, and what each does, are in
`key-functions.md`. Dominance is used rather than degree or PageRank: the call graph has one cycle of
215 functions (5.6), in which every function reaches every other, so counting what a function reaches
does not separate them.

### 5.4 Impact of a change (B1, B6)

The 44 commits between `2a8b9a83eb5b` and `ede81881b7de` changed 30 files of the DLL. Mapping the changed
lines to functions (`functions.tsv` first and last line) and following callers (`measure.py`):

- 217 functions are new or edited;
- 1331 functions can reach one of them, 9 % of all;
- of those, 168 are exported to the exe and 214 are bound for Python.

The same method reviews a patch: take the files and lines of the diff, then the transitive callers of the
functions they fall in. The result is an upper bound: a caller that reaches a changed function may never
take the branch that calls it, and may not use what changed.

### 5.5 Dead-code candidates (C1)

Functions with no caller in the DLL, not exported, not bound for Python, whose address is never taken,
and that are not virtual: 187. The most are in `CvInfos.cpp` (21), `CvGlobals.cpp` (16) and
`CvPlayer.cpp` (12). Examples: `CvCity::getAdditionalCommerceBySpecialist`,
`CvCity::getNumCorpProducedBonuses`, `CvCity::getExtraProductionDifference`.

They are candidates, not dead code: comparison operators (`operator<`, `operator()`) are called by
standard-library templates, and calls from those templates are left out of the map. A function in
`completeness.tsv` that no unit compiles is not in this count at all.

Reachability from outside the DLL reaches all 13405 functions. That is so by construction: a function
with no caller counts as an entry, because the exe may call it. Dead code therefore cannot be found by
reachability from the entries; the candidates above are found by the absence of callers.

### 5.6 Hotspots and cycles (C2, C3)

Fan-in, counted as distinct calling functions of the DLL:
- highest: `CvGlobals::getInstance` 3114 (the `GC` macro), `CvGlobals::getDLLIFace` 1351 (`gDLL`),
  `CvPlayerAI::getPlayer` 1044 (`GET_PLAYER`), `CvGlobals::getGameINLINE` 804;
- median 1; 209 functions have a fan-in of 100 or more.

Fan-out, counted as distinct callees:
- highest: the Python binding functions `CyInfoPythonInterface1` 549 and `CyInfoPythonInterface3` 547;
- then the AI's `CvCityAI::AI_buildingValueThreshold` 294 and the interface's
  `CvGameTextMgr::setPlotHelp` 258.

Cycles: 11 groups of functions call each other round. The largest has 215 functions: 67 in
`CvUnit.cpp`, 30 in `CvCity.cpp`, 29 in `CvPlayer.cpp`, 28 in `CvTeam.cpp`, 16 in
`CvSelectionGroup.cpp`, 15 in `CvPlot.cpp`. The next largest has 11.

### 5.7 Synchronised random numbers (D3)

In a network game every machine must draw the same synchronised random numbers in the same order. The
generator is `CvGame::getSorenRandNum`. Following callers from it:
- 1015 functions can reach it;
- 104 of them are exported and 157 bound for Python;
- 44 are in the interface files `CvDLLWidgetData.cpp` and `CvGameTextMgr.cpp`, which build tooltips
  on one machine only.

One such path, through a unit tooltip:

```
$ python3 codemap/tool/query.py path 'CvDLLWidgetData::parseTrainHelp' 'CvGame::getSorenRandNum'
CvDLLWidgetData::parseTrainHelp(CvWidgetDataStruct&, CvWStringBuffer&)  [1761] CvDLLWidgetData.cpp:1834
CvGameTextMgr::setUnitHelp(...)  [3051] CvGameTextMgr.cpp:9844
CvPlayerAI::AI_unitValue(UnitTypes, UnitAITypes, CvArea*) const  [7830] CvPlayerAI.cpp:11419
CvPlayerAI::AI_isDoStrategy(int) const  [7976] CvPlayerAI.cpp:22335
CvPlayerAI::AI_getStrategyHash() const  [7978] CvPlayerAI.cpp:22356
CvPlayerAI::AI_getStrategyRand() const  [7975] CvPlayerAI.cpp:22324
CvGame::getSorenRandNum(int, char const*)  [2550] CvGame.cpp:9152
```

What the source shows at the end of that path:
- `AI_getStrategyRand` draws from the generator only while `m_iStrategyRand` is 0
  (`CvPlayerAI.cpp:22325-22327`).
- `m_iStrategyRand` is set to 0 when a player is reset (line 322), and when a save whose flag is below 3
  is read (line 20054). Otherwise it is read from the save (line 20050).
- `AI_isDoStrategy` returns before the hash for human players (line 22336).

Section 7, reading 1, says what this suggests.

### 5.8 Event wiring (E3)

`event_handlers.tsv` lists, for each event the DLL posts, every handler registered for it. For
`BeginPlayerTurn`, posted by function 2034 of `CvDllPythonEvents`, there are 12 handlers:
- 8 by `addEventHandler` in the mod's Python: Revolution, AIAutoPlay, DynamicCivNames, RoMEventManager
  and others;
- the base `CvEventManager.onBeginPlayerTurn`;
- 3 in BUG configuration XML: `BUG Core.xml`, `Better Espionage.xml`, `RevDCM.xml`.

### 5.9 What a rewrite has to keep (B4, B5)

`hardcoded.md` lists, for each of the 12 key functions, every entry written into its own lines: exports,
calls into the exe, enum values, XML files and record order, defines, BUG options, text keys, sounds,
Python calls and events, log formats, and lines changed by this fork. Each is checked against the file
that holds the other end. At `ede81881b7de` there are 252 entries, and none whose other end is missing or
differs.

### 5.10 A language model working on the DLL (F1, F3)

The pattern the agent studies of section 9 describe, applied here:
1. read `skeleton.md` (84 KB) and `key-functions.md` before the task;
2. read `files/<file>.md` for the file being changed;
3. ask `query.py` for callers, paths and the key functions while working;
4. use the impact method of 5.4 on the diff before committing.

### 5.11 Which tests a change concerns (B2)

The mod's repository has 33 tests in `Tools/test_*.py`. 15 of them take named functions out of the DLL
source with `block(text, signature)`. 10 of those 15 compile what they take, with stand-ins for the engine,
and run it; the other 5 check the function's text. Matching the signatures to `functions.tsv`
(`measure.py`) ties 14 of the tests to functions of the map:
- 75 `block()` calls name 63 distinct functions; 10 calls do not match a function of the map by name;
- 12 of the 217 functions changed between `2a8b9a83eb5b` and `ede81881b7de` are taken by a test;
- 7 tests take one: `test_crash_fixes.py`, `test_diplomacy_fixes.py`, `test_late_game_fixes.py`,
  `test_patch_0018.py`, `test_unit_ai_corrections.py`, `test_upkeep_traps.py`, `test_war_ai_fixes.py`.

A test of this kind runs or reads the function's own lines, not its callers, so it is selected by the
changed function itself, not by the transitive callers of 5.4. Of the 7, `test_crash_fixes.py`,
`test_late_game_fixes.py`, `test_patch_0018.py` and `test_war_ai_fixes.py` check text only. The other 19
tests are not tied to functions this way.

## 6. What the map cannot answer, and what each answer would need

| Gap | Use cases | What it would need | Available here |
|---|---|---|---|
| Fields: who reads and writes `m_iGold` | B1, D1, D3, save formats | the member accesses of each function | the listings address members as `this` plus an offset; the type records give each class's member offsets |
| Control flow inside a function | B1 precision, D2 | branches and blocks per function | the listings hold every jump and label |
| Data flow, taint | D1, D4 | definitions and uses across calls | not in the listings in usable form; a CodeQL or Joern database of the source would hold it |
| Function pointers | A2, B1 | points-to analysis | 106 calls through pointers are listed with their statement, and 4313 addresses taken |
| Which exports the exe uses | E2, C1 | the exe's import table | not in the repository |
| Python called by computed name | E1 | run-time tracing | 50 `callFunction` sites have a module or function known only at run time |
| XML to code, beyond the 12 key functions | B4 | the `hardcoded.py` checks applied to all functions | the checks exist and run per function |
| Run time: profile, coverage | G1, G2 | call counts and times from games | the harness builds with `profile`, and BBAI logs |
| Tests for most changed functions | B2 | tests that take or call the other 205 changed functions | 14 tests take 63 functions (5.11) |
| Change between commits | B6 | two maps, or a diff mapped to functions | 5.4's method; `measure.py` does it for one diff |
| Clustering | C5 | an algorithm on `calls.tsv` | the tables |

## 7. Readings

What the facts above suggest. Each reading names the facts it rests on and what would contradict it.

**1. A tooltip may draw from the synchronised random generator, and could cause a network game to go
out of sync.** *Open.*
- *Facts:* the path in 5.7 runs from the unit tooltip `parseTrainHelp` to `getSorenRandNum`.
  `AI_getStrategyRand` draws while `m_iStrategyRand` is 0. That value is 0 after a reset and after
  reading an old save. `AI_isDoStrategy` stops early only for human players.
- *Would contradict it:* every player's `m_iStrategyRand` being set by game code before any tooltip can
  be shown, for example by an AI turn processed before the first interface update. Or `AI_unitValue` not
  reaching `AI_isDoStrategy` for the units a tooltip asks about.
- *Test:* in the harness, log every call of `AI_getStrategyRand` that draws, with its caller, from a new
  game and from an old save.

**2. Dominance is the right measure of importance for this DLL; degree and PageRank are not.**
- *Facts:* one cycle of 215 functions (5.6). The highest fan-in belongs to accessors (`GC`, `gDLL`,
  `GET_PLAYER`). The highest fan-out belongs to Python binding functions.
- *Would contradict it:* a ranking by PageRank that places the turn and update functions of
  `key-functions.md` above the accessors.

**3. Most of the 187 dead-code candidates are not dead.**
- *Facts:* the candidates include comparison operators that standard-library templates call. Those
  template calls are left out of the map. The exe may call functions the map does not record as
  exported.
- *Would contradict it:* candidates that are not operators, not declared in an interface header, and
  that the source never names except at their definition. A text search per candidate would show which.

**4. An impact set from callers alone is too large to choose what to test, and the function-level
tests cover few of the changed functions.**
- *Facts:* 217 changed functions reach 1331 others (9 %), including 168 exports. The tests that take
  functions from the source take 12 of the 217 (5.11).
- *Would contradict it:* most of the 1331 taking the branch to the change in every game; or the other
  205 changed functions being exercised by the 19 tests not matched here. A coverage run in the harness
  (section 6) would show the first; reading those 19 tests would show the second.

**5. The map fits the "map in context" pattern that recent agent studies found useful.**
- *Facts:* `skeleton.md` is a compact overview built by the real compiler. The Repository Intelligence
  Graph and The Navigation Paradox report that deterministic structural maps help on architecture
  questions.
- *Would contradict it:* agents answering this repository's architecture questions no better with the
  map than without it, on the same questions.

## 8. Errors found while writing this guide

Checking the 183 `callFunction` sites of `cpp_to_py.tsv` against their source lines:
- 10 had module and function swapped. In `callFunction(PYRandomEventModule, <name at run time>, ...)`
  the only string is the module, but the extractor took a lone string as the function. The rows were
  `CvRandomEventInterface` (8) and `CvScreensInterface` (2), in `CvCity.cpp`, `CvDLLButtonPopup.cpp`,
  `CvGameTextMgr.cpp`, `CvPlayer.cpp` and `CvUnit.cpp`.
- Fixed in `extract_asm.py` (commit `5e81df1`): it now reads the module and function from the call's own
  arguments, a string literal or a `#define` of one, following `#define` chains such as
  `PYBugOptionsModule` → `PYCivModule` → `"CvAppInterface"`.
- After the fix: those 10 rows changed and nothing else did. 40 sites have a module known only at run
  time: 39 map-script calls and one with neither argument known. 11 have a function name known only at
  run time.

## 9. Sources

Program comprehension:
- J. Sillito, G. C. Murphy, K. De Volder, [Questions programmers ask during software evolution tasks](https://dblp.org/rec/conf/sigsoft/SillitoMV06), FSE 2006.

Symbol indexes:
- Sourcegraph, [SCIP, a better code indexing format than LSIF](https://sourcegraph.com/blog/announcing-scip).
- [SCIP repository](https://github.com/sourcegraph/scip).
- GitLab, [Code intelligence](https://docs.gitlab.com/user/project/code_intelligence/).

Code property graphs and data flow:
- [Code property graph](https://en.wikipedia.org/wiki/Code_property_graph).
- [Joern](https://raw.githubusercontent.com/joernio/joern/master/README.md).
- [LLMxCPG](https://arxiv.org/pdf/2507.16585).
- CodeQL, [Analyzing data flow in C and C++](https://codeql.github.com/docs/codeql-language-guides/analyzing-data-flow-in-cpp).

Impact analysis and test selection:
- O. Legunsen et al., [An extensive study of static regression test selection](https://mir.cs.illinois.edu/~marinov/publications/LegunsenETAL16StaticRTS.pdf).
- X. Ren et al., [Chianti](https://www.cs.purdue.edu/homes/xyzhang/fall07/Papers/chianti.pdf).
- B. Ryder, F. Tip, [Change impact analysis for object-oriented programs](https://www.rose-hulman.edu/class/csse/csse575/Resources/impact%20OOIA-RyderTip.pdf).

Call-graph precision:
- [Detecting call graph unsoundness](https://arxiv.org/pdf/2604.00885).
- [Bacon and Sweeney's RTA](https://www2.eecs.berkeley.edu:443/Pubs/TechRpts/1998/CSD-98-1017.pdf).
- [Call graphs and function pointers, lecture slides](https://fileadmin.cs.lth.se/cs/Education/EDAP15/2022/web/slides-10.pdf).

Architecture recovery:
- T. Lutellier et al., [Measuring the impact of code dependencies on software architecture recovery techniques](https://www.cs.purdue.edu/homes/lintan/publications/archrec-tse17.pdf).
- [Discovery of layered software architecture using ego networks](https://arxiv.org/pdf/2106.03040).

Centrality and dominance:
- [Ragex graph algorithms](https://hexdocs.pm/ragex/algorithms.html).
- [Twiggy: dominators and retained size](https://rustwasm.github.io/twiggy/concepts/dominators-and-retained-size.html).
- K. Cooper, T. Harvey, K. Kennedy, "A simple, fast dominance algorithm" (2001), used by `query.py`.

Language-model agents:
- Aider, [Building a better repository map with tree-sitter](https://aider.chat/2023/10/22/repomap.html).
- [RepoGraph](https://arxiv.org/html/2410.14684v2).
- [CodexGraph](https://arxiv.org/pdf/2408.03910).
- [Repository Intelligence Graph](https://arxiv.org/html/2601.10112v1).
- [The Navigation Paradox in large-context agentic coding](https://arxiv.org/html/2602.20048v1).
- [LARGER](https://arxiv.org/pdf/2605.16352).

Cross-language graphs:
- [Cross-language call graphs to C/C++ foreign functions, SANER 2023](https://computer.org/csdl/proceedings-article/saner/2023/527800a155/1Nc0HUyqYFi).
- [Lightweight multilingual software analysis](https://www.academia.edu/114943799/Lightweight_Multilingual_Software_Analysis).
