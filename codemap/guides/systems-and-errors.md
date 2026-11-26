# The systems of Rise of Mankind, and the errors found in them

Every function of the DLL sorted into a category and a system, the Python and XML around it, including
the modules the game loads (Guilds among them), and every error the checks found, with its status.
Written by hand from the map at GitLab commit `ede81881b7de`. The figures are printed by:

```sh
python3 codemap/tool/systems.py                                                     # sections 2-3
python3 codemap/tool/check_links.py <rom> <BTS XML> <Civ4 XML> --base-python <BTS Python> <Civ4 Python>   # section 5
python3 codemap/tool/measure.py <rom> 2a8b9a83eb5b                                   # reach and cycles
```

Sections 1 to 5 describe. Section 6 holds the readings. Section 7 lists what is still open.

## Contents

1. [How the sorting works](#1-how-the-sorting-works)
2. [The DLL: categories](#2-the-dll-categories)
3. [The DLL: systems within each category](#3-the-dll-systems-within-each-category)
4. [Around the DLL: Python, XML and the modules](#4-around-the-dll-python-xml-and-the-modules)
5. [Error register](#5-error-register)
6. [Readings](#6-readings)
7. [Open questions](#7-open-questions)

## 1. How the sorting works

`codemap/tool/systems.py` sorts the 13405 functions of `map/functions.tsv` in two steps:
1. **Category, by file.** Seven categories, each a list of file names (`CATEGORIES` in the script).
   Container templates (`FFreeList…`, `CLinkList`) go to infrastructure wherever they are instantiated.
2. **System, by name.** In the game-state and AI categories, the first of 28 name rules that matches
   (`SYSTEMS`). Examples: names with `ombat`, `ttack` or `Odds` are combat; `eligion` or `issionar` are
   religion. A function no rule matches falls back to its class: `CvCity` functions are "city (other)".
   AI functions also carry their layer, taken from the class: unit, group, city, player, team or game AI.

This sorts by name and file, not by what the code does. A function named `getAdvancedStartUnitCost` is
"economy" because of `Cost`, although it serves the advanced start. Every function lands in exactly one
system; none is unassigned.

Calls are counted as distinct caller-callee pairs between the DLL's own functions: 71100 pairs.

## 2. The DLL: categories

| # | Category | Files (examples) | Functions | Lines | What it holds |
|---|---|---|---|---|---|
| 1 | Engine boundary | `CvGameCoreDLL.cpp`, `CvDLL*IFaceBase.h`, `CvGameInterface.cpp`, `CvDLLEntity` | 123 | 3473 | the DLL's entry point, the exe's interfaces, functions the exe calls for the interface |
| 2 | Infrastructure | `FFreeListTrashArray.h`, `LinkedList.h`, `CvString.h`, `CvRandom`, `CvMessageData` | 989 | 6497 | containers, strings, asserts, the random generator, network messages |
| 3 | Rule data | `CvInfos`, `CvXMLLoadUtility*`, `CvGlobals`, `CvInitCore`, `CvArtFileMgr` | 4061 | 106047 | the rule records read from XML, the loaders, the global tables, game setup |
| 4 | Game state and rules | `CvGame`, `CvMap`, `CvPlot`, `CvPlayer`, `CvTeam`, `CvCity`, `CvUnit`, `CvSelectionGroup`, `CvDeal` | 3764 | 93136 | the game's objects and the rules that change them |
| 5 | AI | `*AI.cpp`, the 17 `AI*Policy.h` headers, `ResearchPathPlan.h` | 1015 | 71510 | every decision the computer players make |
| 6 | Interface | `CvGameTextMgr`, `CvDLLWidgetData`, `CvDLLButtonPopup`, replays, statistics | 700 | 29481 | tooltips, popups, messages, replays |
| 7 | Python bridge | `Cy*` (62 files), `CvDllPythonEvents`, `CvEventReporter` | 2753 | 17621 | what Python can call in the DLL, and the events the DLL posts to Python |

Calls between categories (distinct pairs; the row calls the column):

| from \ to | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| 1 engine boundary | 58 | 62 | 272 | 328 | 30 | 16 | 53 |
| 2 infrastructure | 271 | 843 | 162 | 154 | 38 | 1 | 6 |
| 3 rule data | 1041 | 3069 | 10275 | 12 | 19 | 2 | 11 |
| 4 game state and rules | 334 | 1411 | 6943 | 14565 | 1035 | 105 | 358 |
| 5 AI | 38 | 84 | 2738 | 7854 | 2978 | 14 | 28 |
| 6 interface | 82 | 1483 | 2949 | 1808 | 288 | 880 | 97 |
| 7 Python bridge | 308 | 197 | 2197 | 2072 | 6 | 159 | 3366 |

What the matrix shows:
- Rule data calls almost nothing above it: 12 pairs into game state, 19 into AI.
- Game state calls AI in 1035 pairs. The objects hand their decisions to their AI subclasses
  (`CvCity::doTurn` → `CvCityAI::AI_chooseProduction`).
- The interface calls AI in 288 pairs: tooltips show AI values (`AI_unitValue`, `AI_buildingValue`).
- AI calls the interface in 14 pairs. All 14 are the AI preparing the diplomacy screen for the human
  (`CvDiploParameters`, `CvPopupInfo` in `AI_doDiplo` and `AI_doPeace`). This is the original BTS design.

## 3. The DLL: systems within each category

### 3.1 Game state and rules (3764 functions)

| System | Functions | Lines | Examples |
|---|---|---|---|
| map and geometry | 445 | 8024 | `CvUnit::setXY`, `CvPlot::setPlotType`, `CvGame::assignStartingPlots` |
| combat | 344 | 8657 | `CvUnit::maxCombatStr`, `CvUnit::updateCombat`, `CvUnit::updateStackCombat` |
| production and building | 274 | 7170 | `CvCity::popOrder`, `CvCity::canConstruct` |
| movement and paths | 233 | 6926 | `CvSelectionGroup::startMission`, `continueMission`, `pathCost` |
| economy | 192 | 3359 | gold, commerce, maintenance, inflation, hurry |
| diplomacy and war | 190 | 5699 | `CvTeam::declareWar`, `CvDeal::startTrade`, `CvPlayer::canTradeItem` |
| improvements, routes and bonuses | 139 | 3312 | `CvPlot::doFeature`, `CvPlot::canHaveImprovement` |
| religion | 95 | 1956 | `CvUnit::performInquisition`, `CvGame::doHolyCity` |
| culture and borders | 88 | 1700 | `CvPlot::setOwner`, `CvCity::setCultureLevel` |
| visibility | 69 | 1305 | `CvPlot::setRevealed`, `CvPlot::updateSight` |
| growth and food | 62 | 735 | `CvCity::setPopulation`, `CvCity::doGrowth` |
| promotions and experience | 63 | 1247 | `CvUnit::setHasPromotion`, `CvUnit::getUpgradeCity` |
| research | 59 | 1987 | `CvTeam::setHasTech`, `CvTeam::processTech` |
| happiness and health | 60 | 780 | `CvCity::updateFeatureHappiness` |
| great people and golden age | 57 | 659 | `CvPlayer::createGreatPeople`, `CvCity::doGreatPeople` |
| corporations | 55 | 1233 | `CvGame::doHeadquarters`, `CvCity::setHasCorporation` |
| votes and diplomatic victory | 55 | 1815 | `CvGame::doVoteResults`, `CvGame::processVote` |
| turn and update | 49 | 4386 | `CvPlayer::setTurnActive`, the `reset` functions |
| espionage | 48 | 1892 | `CvPlayer::doEspionageMission` |
| civics | 42 | 842 | `CvPlayer::setCivics`, `CvPlayer::getCivicAnarchyLength` |
| events | 41 | 3414 | `CvPlayer::applyEvent`, `CvPlayer::initTriggeredData` |
| victory and score | 47 | 1181 | `CvGame::testVictory`, `CvGame::updateScore` |
| logging (war log) | 26 | 417 | `warLogTurnStart`, `warLogStacks` |
| graphics paging | 23 | 1106 | `CvGame::pageGraphics`, `CvGame::updateGraphicsPaging` |
| save and load | 22 | 3138 | `CvPlayer::read`, `CvPlayer::write` |
| settlement | 17 | 610 | `CvPlayer::canFound`, `CvUnit::found` |
| random numbers | 7 | 170 | `CvMap::syncRandPlot` |
| by class, no name rule | 962 | | unit 251, player 246, city 168, game 157, team 75, free functions 61, 4 functions of 3 small structs |

The full list, with calls in and out, is printed by `systems.py`.

### 3.2 AI (1015 functions)

| Layer | Functions | Lines | Its largest systems |
|---|---|---|---|
| player AI | 325 | 25305 | diplomacy and war 69, religion 23, movement 20, settlement 17, victory 13, research 12 |
| unit AI | 211 | 24019 | movement and paths 50, combat 43, espionage 10, workers 8, religion 7 |
| city AI | 121 | 13634 | production and building 24 (`AI_chooseProduction`, 7060 lines in the system), improvements 11, combat 8 |
| team AI | 129 | 5373 | diplomacy and war 70 (`AI_doWar`, `AI_surrenderTrade`), map 8 |
| AI policies | 120 | 972 | 17 headers: `AIDecisionPolicy` 18, `AIMissionTargetIndex` 15, `AIBuildingLinePolicy` 13, `AIDiplomacyPolicy` 10 … |
| AI support | 65 | 1208 | `ResearchPathPlan`, `CvResearchGraph`, `AI_assaultForecast` |
| group AI | 32 | 910 | `AI_update`, attack and sacrifice choice |
| game AI | 12 | 89 | work assignment |

### 3.3 The other categories

| Category | System | Functions | Lines |
|---|---|---|---|
| rule data | rule records (infos) | 2668 | 23297 |
| | globals and setup | 965 | 6090 |
| | XML loading | 421 | 76570 |
| | BUG options | 7 | 90 |
| infrastructure | containers, strings, asserts | 741 | 5439 |
| | network messages | 237 | 998 |
| | random numbers | 11 | 60 |
| interface | tooltips and help | 381 | 25207 |
| | messages, replays, statistics | 219 | 1353 |
| | popups | 100 | 2921 |
| Python bridge | bindings | 2575 | 16104 |
| | events to Python | 178 | 1517 |

## 4. Around the DLL: Python, XML and the modules

### 4.1 Python (277 modules, 6681 functions and classes)

| Part | Functions and classes | What it is |
|---|---|---|
| `BUG/` | 1547 | the BUG framework: options, configuration, event dispatch, game-utils dispatcher |
| `Contrib/` | 1087 | features run through BUG: Sevopedia, Civ4lerts, Reminder, StatusDump, autolog … |
| `Screens/` | 874 | the mod's screens (advisors, Pedia, main interface) |
| top level | 672 | `RoMEventManager.py`, `PyHelpers.py`, `AbandonCityEventManager.py` … |
| `EntryPoints/` | 635 | the modules the exe and the DLL call: `CvScreensInterface`, `CvAppInterface`, `CvRandomEventInterface` … |
| `Revolution/` | 294 | Revolution, BarbarianCiv, AIAutoPlay, DynamicCivNames |
| `BUFFY/` | 25 | the BUFFY DLL probe |
| other folders | 15 | `EnhancedTechConquestUtils` and others |
| base game modules | 1532 | Beyond the Sword's, then Civilization IV's, where the mod has none: `CvEventManager`, `CvGameUtils`, `CvGameInterface`, base screens, `System/` |

Links with the DLL: 29043 Python call sites use a name the DLL binds; 183 DLL calls go into Python; 81
events, with 222 event-handler links.

### 4.2 XML and the modules

The game reads the mod's `Assets/XML` and `Assets/res`, then the modules (`Assets/Modules`). With the
exe's own modular loading off (`ModularLoading = 0` in `Rise of Mankind.ini`), the DLL decides which
modules load, from the MLF files (`CvXMLLoadUtility::ModularLoadingControlXML`):
- an entry `<bLoad>1</bLoad>` under the default configuration, whose folder exists, loads;
- an entry whose folder has its own MLF file is resolved through that file;
- `Assets/Unloaded Modules` is never read.

| Module group | Loaded folders | Listed, no folder |
|---|---|---|
| Custom Leaderheads | 23 | 0 |
| Custom ArtStyles | 14 | 79 |
| Custom Units | 11 | 1 |
| Projects/Vincentz | 2: **Corporations**, **Guilds** | 8 (Silent Hunter, SpySat, Thor, Improve, Promo, VCivics, Seaharvest, Icons) |
| Holy Wars | 1: Christianity | 11 |
| Buildings | 1: UNMission | 2 |
| Builds | 1: JungleCamp | 1 |
| top level | — | 71 (Translations, Sarkyn, Brandenburg Gate …) |
| Custom Civilizations | 0 | 54 |
| **Total** | **53 folders, 451 XML files** | **227** |

The loaded XML is 677 files of the mod (226 in `Assets/XML` and `res`, 451 in modules) plus 75 base game
files the mod does not replace. Together they define 694 global defines, 7620 type names and 15904 text
keys.

## 5. Error register

**Status:**
- *confirmed*: the fact and its effect follow from the source.
- *dormant*: wrong, but no caller or setting reaches it.
- *open*: needs evidence not on this machine.
- *not an error*: flagged by a check, cleared on reading.
- *map limit*: the map cannot see it.

**Origin:**
- *stock*: as in the Firaxis SDK, base Python or base XML.
- *mod*: added by Rise of Mankind or a component it ships.

### 5.1 Compile and parse

| Check | Checked | Failed |
|---|---|---|
| DLL units compiled with the real compiler (`/W3`) | 105 | 0 errors, 0 warnings |
| Python modules parsed by the game's Python 2.4 | 277 | 0 |
| Loaded mod XML files well-formed | 677 | 6 |

The 6 are `README_CIV4*.xml` in `XML/BasicInfos` and `XML/GameInfo`. Each holds only comments, with no
root element, and no loader names them. *Not an error*: they are notes, not loaded data.

### 5.2 Errors in the code

| ID | Where | Fact | Effect | Status | Origin |
|---|---|---|---|---|---|
| C1 | `CvGameCoreUtils.cpp:1041`, `getCombatOddsSpecific` | The BUG option "Ignore Barb Free Wins" is read as a global define: `GC.getDefineINT("ACO_IgnoreBarbFreeWins")`. No define of that name exists, so it is always 0. The option is `ACO__IgnoreBarbFreeWins` in `Config/Advanced Combat Odds.xml`, and the same tooltip reads it correctly at `CvGameTextMgr.cpp:2225` with `getBugOptionBOOL`. | The combat-odds tooltip (`setCombatPlotHelp`) always applies the barbarian free-win rule in its odds, whatever the option says. Interface only. | confirmed | mod (ACO) |
| C2 | `CvCity.cpp:2343`, `CvCity::canConstruct` | `CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding);` comes before `if (eBuilding == NO_BUILDING) return false;`. With -1 it reads `m_paBuildingInfo[-1]`, outside the table. The stock SDK tests first; the binding came in with RevDCM's "CanConstruct Performance" block. | Undefined behaviour for `NO_BUILDING`. Reached from Python by C3. | confirmed | mod (RevDCM) |
| C3 | `Python/Revolution/Gameready/BarbarianCiv.py:804`, then `:1104`, `:1574`, `:1605`, `:1643` | `iGranary` is the civilization's building for `BUILDINGCLASS_GRANARY`, which is -1 (D1). It is passed to `city.canConstruct(iGranary)` when a barbarian civilization settles. | Reaches C2 with -1; the granary step never builds anything. | confirmed | mod (Revolution) + D1 |
| C4 | `CvPlayerAI.cpp:22324`, `AI_getStrategyRand` | Draws from the synchronised generator the first time it is called for a player whose value is 0. Tooltip code reaches it (`use-cases.md`, 5.7). | Possibly a network desync. | open | mod (BBAI) |
| C5 | `Python/PyHelpers.py:1356`, `UnitInfo.getPrereqOrTechIDList` | Reads the define `NUM_UNIT_OR_TECH_PREREQS`, which does not exist (the defines are `NUM_OR_TECH_PREREQS` and `NUM_UNIT_AND_TECH_PREREQS`). The loop runs 0 times. If it ran, `getPrereqOrTechs` is not bound for unit infos. | The list is always empty. | dormant | stock (both base games) |

### 5.3 Errors in the data (XML and modules)

| ID | Where | Fact | Effect | Status | Origin |
|---|---|---|---|---|---|
| D1 | `XML/Buildings/CIV4BuildingClassInfos.xml` (16), **`Modules/Projects/Vincentz/Guilds/Guildhalls_CIV4BuildingClassInfos.xml` (5)** | 21 building classes name a `DefaultBuilding` that nothing the game loads defines. Base: `BUILDING_GRANARY`, `MODERN_GRANARY`, `MEETING_HALL`, `FISHERMAN_HUT`, `BUTCHERY`, `BAKERY`, `ARTESIAN_WELL`, `HEALERHUT`, `DOCTOR`, `TANNERY`, `BAZAAR`, `PAVED_ROADS`, `GROCER`, `SUPERMARKET`, `SHOPPING_DISTRICT`, `SEWER_SYSTEM`. Guilds: `BUILDING_GUILDHALL_32`, `_36`, `_39`, `_41`, `_43`; the module defines guildhalls 30, 31, 33–35, 37, 40, 42 and 44. `getInfoTypeForString` returns -1 and logs to `xml.log`; the class keeps `NO_BUILDING`. | The 21 classes have no building for any civilization. Five event triggers require one of them and can never fire: `EVENTTRIGGER_SPOILED_GRAIN` (granary), `POISON_ARROWS` (healer hut), `TANNERY_GLUE` (tannery), `RURAL_FARMERS` and `CRAB_CAKES` (grocer). `BarbarianCiv.py` gets -1 (C3). | confirmed | mod; present since the repository's first commit `8cc9168` |
| D2 | `XML/Terrain/CIV4BonusInfos.xml:4121`, `BONUS_WOOL` | `<TechCityTrade>TECH_WEAVING</TechCityTrade>`; no technology `TECH_WEAVING` exists (only its text keys do). `CvBonusInfo::read` resolves it with `FindInInfoClass`, which on a miss shows the dialog "Tag: TECH_WEAVING in Info class was incorrect". | An XML error dialog while the rules load. `getTechCityTrade()` is -1, and `CvTeam::isHasTech(NO_TECH)` returns true, so wool can be traded between cities from the start. | confirmed | mod |
| D3 | `CvGlobals.cpp:3043`; `XML/PythonCallbackDefines.xml` | The switch `USE_CANNOT_CREATE_PROJECT_CALLBACK` is read, but no XML defines it. It is always 0. | The Python callback `cannotCreateProject` (`CvCity.cpp:2647`) can never be switched on without adding the define. | dormant | mod |
| D4 | the MLF files of `Assets/Modules` | 227 entries with `bLoad` 1 name folders that do not exist (54 in `Custom Civilizations`, 79 in `Custom ArtStyles`, 71 at the top level, 8 in `Projects/Vincentz` …). The DLL logs "No valid module" for each. | None beyond the log. | not an error (leftovers) | mod |

### 5.4 Errors between the DLL, Python and text

| ID | Where | Fact | Effect | Status | Origin |
|---|---|---|---|---|---|
| L1 | 91 `TXT_KEY_…` literals, 77 of them in the DLL (64 uses in `CvGameTextMgr.cpp`), 14 in Python | Not defined by any `<Tag>` in the mod, its loaded or unloaded modules, or the supplied base game text. None differs from a defined key only by case. Examples: `TXT_KEY_ATTITUDE_MASTER_OF`, `TXT_KEY_ATTITUDE_VASSAL_OF`, `TXT_KEY_TRADE_VASSAL`, `TXT_KEY_TRADE_CAPITULATE`, `TXT_KEY_BUILDING_BORDER_OBSTACLE`, `TXT_KEY_ACTION_LEAD_TROOPS`. | Where a key is missing, the game shows the key itself. | open (see 7) | mixed |
| L2 | `CvGame.cpp:7602`, `CvGame::doHeadquarters` | Calls `CvGameInterface.doHeadquarters` on every game turn, with no switch. No supplied Python file contains `doHeadquarters`. The stock SDK makes the same call. | If the function is missing in the installed game, every turn produces a failed Python call (a Python error), and the DLL continues as if it returned 0. | open (see 7) | stock |
| L3 | `CvUnit.cpp:6445` | Calls `CvGameInterface.cannotSpreadReligion`, which `CvGameInterface.py` does not define. Guarded by `USE_CANNOT_SPREAD_RELIGION_CALLBACK`, which is 0 in the mod's `PythonCallbackDefines.xml`. | None while the switch is 0. | dormant | stock |
| L4 | `CvMessageData.cpp:1172` | Calls `CvAppInterface.netAddReminder`. It is assigned at run time by `ReminderEventManager.py:50` (`CvAppInterface.netAddReminder = netAddReminder`). | None. | not an error (map limit) | mod |
| L5 | Python bindings in `CyInfoInterface3.cpp:599`, `CyCityInterface1.cpp:97`, `CyUnitInterface1.cpp:76-77` | `getReligionRequired` is bound to `CvEventTriggerInfo::getBonusRequired`. `getProjectProductionModifier` (declared `int (int eProject)`) is bound to the no-argument `CyCity::getProductionModifier()`. `canRecon` and `canReconAt` are each bound twice, the second time to `canParadrop`/`canParadropAt`, which take effect. | Wrong results or an argument error, if called. No Python in the mod or the base games calls them. | dormant | stock |
| L6 | `AbandonCityEventManager.py:121` | A handler for the event `StartAbandonCity`, which neither the DLL nor any Python posts. The feature starts from the BUG shortcut Ctrl+A (`Config/Abandon City Mod.xml`), which calls the module-level function directly. | None: the registration is dead, the feature works. | not an error | mod |
| L7 | `Python/BUFFY/Buffy.py:64,68` | `gc.isBuffy()` and `gc.getBuffyApiVersion()` are not bound by this DLL. They are called inside `try`, to detect the BUFFY DLL. | None. | not an error | mod (BUFFY) |

The other 80 of the 84 bindings whose Python name differs from their C++ name are naming conventions
(`cy` and `py` prefixes, `getCyGame` for `getGame`). Of the 22 type references the check flags in the
loaded XML, D1 holds 21 and D2 the last.

### 5.5 Errors in the map, found by these checks

| Where | Fact | Status |
|---|---|---|
| `map/python_defs.tsv` | When one statement binds the same Python name twice (L5), both rows carry the line of the first binding (2 pairs). | minor, open |
| `map/unresolved.tsv` | 17 virtual calls match no method name: 12 deletes inside the `ART_INFO_DEFN` macro, 4 `Py_DECREF`, and a progress callback through a function pointer. | map limit |
| `codemap/tool/check_links.py`, while writing this | The Python comment filter `^\s*#` swallowed line breaks, so line numbers shifted. Fixed to `^[ \t]*#` before the figures above were taken. | fixed |

### 5.6 Totals

| Status | Count | IDs |
|---|---|---|
| confirmed | 5 | C1, C2, C3, D1, D2 |
| dormant | 4 | C5, D3, L3, L5 |
| open | 3 | C4, L1, L2 |
| not an error | 5 | the README files, D4, L4, L6, L7 |

## 6. Readings

**1. D1 and D2 are leftovers of buildings and a technology removed before the repository began.**
- *Facts:* the missing names never appear as definitions in the repository's history. Their text keys
  (`TXT_KEY_TECH_WEAVING`) and art (`ART_DEF_BUILDING_GRANARY`) remain. The classes and triggers that
  name them still load.
- *Would contradict it:* the definitions appearing in a file the game loads that this check does not
  read, such as an FPK archive.

**2. The Guilds module was trimmed without its building classes.**
- *Facts:* `Guildhalls_CIV4BuildingInfos.xml` defines nine guildhalls. `Guildhalls_CIV4BuildingClassInfos.xml`
  names five more as defaults (32, 36, 39, 41, 43), defined nowhere, and nothing else names their classes.
- *Would contradict it:* those five buildings being defined in another loaded file under a different
  file name.

**3. C1, C2 and C3 show components merged without checking their joins.**
- *Facts:* C1 reads a BUG option by the define system, next to code that reads it correctly. C2 is a
  performance change that moved a lookup above its guard. C3 is Revolution code that relies on a class
  the mod's XML left empty.
- *Would contradict it:* these lines coming from the components' own releases unchanged. Their own
  repositories would show that.

**4. The layers are cleanly separated, except where the interface asks the AI.**
- *Facts:* rule data calls game state in 12 pairs and AI in 19. AI calls the interface only to prepare
  diplomacy (14 pairs). The interface calls AI in 288 pairs, and through them reaches the synchronised
  generator (C4).
- *Would contradict it:* the 288 interface-to-AI calls being pure reads, with no state change. C4 is the
  case that would decide it.

## 7. Open questions

- **L1 and L2 need a full Beyond the Sword install.** The supplied base game Python and XML may be
  incomplete or an older version: no supplied file contains `doHeadquarters`, which the stock SDK calls
  every turn, nor the standard vassal keys `TXT_KEY_TRADE_VASSAL` and `TXT_KEY_TRADE_CAPITULATE`.
  Checking the installed game's `Assets/Python/EntryPoints/CvGameInterface.py` and `Assets/XML/Text`
  settles both.
- **C4 needs a harness run:** log every draw of `AI_getStrategyRand` with its caller, from a new game and
  from an old save.
- **Files the checks do not read:** FPK archives (`RoMPak0.FPK`, `RoMPak1.FPK`, `RevDCM.FPK`) hold art,
  and the exe's own lookups (sounds, art) are not checked here.
