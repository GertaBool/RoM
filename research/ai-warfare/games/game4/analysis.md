# Game 4: Julius Caesar (Rome), PAE Europe V Large, Monarch, to turn 285 (250 BC)

Sources: the save `Julius Caesar BC-0250` (turn 285), loaded in the headless harness
(`toolchain/harness/sav2dat.py`, `harness.exe save` with `HARNESS_HISTORY_DIAG=1`); its
setup block, read by `toolchain/harness/initcore.py`; the war log `WarLog.log` (one
session, turns 0–284, no repeated or missing turns, last full turn 284); the scenario file
`PAE Europe V Large.CivBeyondSwordWBSave`. Tables: `tools/gamedata.py` (this folder's CSVs and
`summary.md`). Figures used below: `figures.py`. XML effects: `xmlread.py` records of
`rom-0018b` (the source tree of the war-log DLL), looked up on the day of writing. Code
references are to `rom-0018b`.

## 0. Questions and their sources

| # | Question | Source |
|---|---|---|
| Q1 | Map, options, victories, players, names, handicaps, starts, starting techs and units | setup block (`initcore.py`), scenario file, `H` and `P` lines → `players.csv` |
| Q2 | Each player's cities, pop, hammers, commerce, power, score and techs over the game; wars, captures and eliminations among all players | `M`, `X`, `W`, `Q`, `K`, `Z` lines → `economy.csv`, `techs.csv`, `wars.csv` |
| Q3 | The human's cities: founded where and when, captured from whom, razed | save cities (founding turn kept on capture) and `K`/`Z` lines |
| Q4 | The human's economy: civics, research, tech sources, buildings, worker builds, gold | `A` lines (`human_*.csv`), `X`, `N`, `D`, `M` lines |
| Q5 | The human's military: units, upgrades, promotions, wars declared, battles, captures, peace terms | `U`, `A`, `C`/`R`, `K`, `D`, `G` lines |
| Q6 | Diplomacy with the AIs: deals, requests and answers | `D`, `E` lines → `deals.csv`, `diplomacy.csv` |
| Q7 | The AI side of each war: the cities taken, their defenders, the AI's danger count, the AI's stacks and attacks | `Y`, `G`, `C`/`R` lines; AI code |

## 1. Setup

- **Map:** the scenario *PAE Europe V Large*, 84 × 64, no wrap (scenario file).
- **Speed:** Marathon (setup block; `H` line).
- **Options:** No Barbarians, No Vassal States, No Events, No Revolution, No Barbarian Civ,
  No Tech Diffusion, Dynamic Civ Names (setup block). They equal the scenario's options.
- **Victories:** score, conquest, religious, space race (setup block). Score victory is on in
  the game but not in the scenario file.
- **Players:** 19, one per team, nobody at war at the start (scenario team blocks).
  - Every leader name and civilization name in the save equals the scenario's: four custom
    leader names (Maglocunus for England, Vercingetorix for the Celts, Hiram for Joao's
    Carthage, Minos for Hannibal's Greece). Every civilization is called "… Tribe".
  - Whether the setup block holds the dynamic names at turn 285 or the setup names is *open*.
- **Handicap:** the human (player 3, Rome, Julius Caesar) Monarch, every AI Noble (setup block).
  The game's handicap is Monarch (`H` line, written from `CvGame::getHandicapType`,
  `CvGameCoreUtils.cpp:3348`).
  - The AI's production cost uses the game's handicap (`CvPlayer.cpp:7501`,
    `getAITrainPercent` of `GC.getGameINLINE().getHandicapType()`).
  - Monarch against Noble (records, `HandicapInfo`):

    | Field | Noble | Monarch |
    |---|---|---|
    | `iAITrainPercent` | 100 | 90 |
    | `iAIConstructPercent` | 100 | 90 |
    | `iAIGrowthPercent` | 100 | 95 |
    | `iAIWorkRateModifier` | 0 | 20 |
    | `iAIUnitCostPercent` | 100 | 90 |
    | `iAICivicUpkeepPercent` | 100 | 90 |
    | `iAIPerEraModifier` | 0 | −2 |

    For the human's own handicap:

    | Field | Noble | Monarch |
    |---|---|---|
    | `iResearchPercent` | 100 | 115 |
    | `iUnitCostPercent` | 50 | 70 |
    | `iCivicUpkeepPercent` | 80 | 95 |
    | `iNumCitiesMaintenancePercent` | 70 | 85 |
    | `iDistanceMaintenancePercent` | 75 | 90 |
    | `iFreeUnits` | 8 | 4 |
    | `iInflationPercent` | 90 | 100 |
  - `AIFreeTechs` (Archery) did not apply: no AI had Archery at turn 0, and the first had it
    at turn 113 (`X` lines). Whether `iAIStartingDefenseUnits` (1) applied is *open*.
- **Starts** (scenario Settler plots; `players.csv`):
  - The human starts at 27,26, with Masinissa (24,17) 9 steps away and Brennus (16,36) 11.
  - Room (flat or hill land within 8 steps, nearer to that start than to any other): 69 for
    the human.
  - The Greek starts are crowded: Pericles 42,22 (room 21), Leonidas 39,20 (room 11) and
    Hannibal 44,17 (room 54) lie within 5 steps of each other; Alexander is at 39,29.
- **Starting techs:** the human has Roman, Fishing, Agriculture, Hunting, Naturopathy (team
  block; equal to the turn-0 `X` lines). Each start has one Settler and one Scout.

## 2. The whole game (all players)

`summary.md` has every player at turns 50, 100, 150, 200, 250, 284.

- **Cities**, turn 50 → 284:
  - The human goes from 1 to 25.
  - AIs at turn 284: Ramesses (Egypt) 21; Ivan, Ashur and Willem 15 each; Henry and
    Gilgamesh 14; Charles V and Cyrus 12; the others 2–10.
  - Leonidas (Dorian Greece) has 6 cities at turn 200, 2 at turn 250, and his last `M` line
    is turn 272.
- **Score:**

  | Turn | Human | Best AI |
  |---|---|---|
  | 150 | 88 | 77 (Willem) |
  | 200 | 187 | 183 (Ramesses) |
  | 250 | 382 | 389 (Ramesses) |
  | 284 | 902 | 617 (Ramesses) |
- **Techs** (`X` lines, starting techs included):

  | Turn | Human | AI mean | AI best |
  |---|---|---|---|
  | 100 | 8 | 8.3 | 13 |
  | 200 | 16 | 14.7 | 19 |
  | 250 | 24 | 19.0 | 24 |
  | 284 | 39 | 24.1 | 32 (Cyrus) |
- **Hammers** (`M` lines):

  | Turn | Human | Best AI |
  |---|---|---|
  | 200 | 109 | 113 |
  | 250 | 532 | 309 |
  | 284 | 1,358 | 558 |

  Human commerce at turn 284: 1,724, against 820 for the best AI.
- **Power** at turn 284: the human 1,980; the best AI 990 (Ramesses).
- **Wars among AIs:**
  - 11 declarations from turn 174 (`W` lines) and 4 peaces.
  - The AIs took 10 cities from each other (`K` lines, turns 205–281). None took a city from
    the human.
- **The human:** declared 8 wars (section 3.4), took 16 cities (12 kept, 4 razed) and lost
  none.
  - Leonidas was eliminated by the human: his last two cities were taken on turns 272 and 273.
  - Mission metric at turn 284 (`summary.md`): K 15 taken, L 0 lost, techs 39/32, score 902/617.

## 3. The human: description

### 3.1 Turns 0–100: one city, then three

- Production to turn 50: 47 % workboats, 53 % land units (`spending.csv`).
- First orders at the capital: Workboat (0), Warrior and Workboat (10), Javelineer (25),
  Worker (49) (`human_orders.csv`).
- Research: Slavery first (chosen turn 0, known turn 34), then Mining (61), Pottery (87),
  Masonry (121) (`human_research.csv`, `techs.csv`).
- Civics:
  - Turn 2: Patriarch, Oral Law, No Taxes, Coastal, Peasantry, Homeschooling, Folklore,
    Tribal Warfare.
  - Turn 35: Oligarchy and Tribute.
  - Turn 88: Tablets.

  (`human_civics.csv`; the turn-2 set is the first civics line of the log.)
- Anarchy turns in the whole game (commerce 1 in the `M` lines): 35–36, 88, 138, 146,
  205–206, 245. The switches on turns 222, 229 and 268 show none.
- Effects (records, `CivicInfo`):
  - Oligarchy: `iFreeExperience` 3; Palace +6 happiness; `iDistanceMaintenanceModifier` 30.
  - Tribute: `CapitalYieldModifiers` [25, 25, 25]; `CapitalCommerceModifiers` [0, 0, 25];
    `YieldModifiers` [−10, 0, 0]; `iNumCitiesMaintenanceModifier` 10;
    `iDistanceMaintenanceModifier` 25; `iWarWearinessModifier` 50.
  - Tablets: `YieldModifiers` [−10, −10, −10]; `iDistanceMaintenanceModifier` −10;
    `iNumCitiesMaintenanceModifier` 10.
- First Settler ordered on turn 75. Second city 32,23 founded on turn 87; third 32,26 on
  turn 100. At turn 100 the human has 3 cities, the AIs 1–2.

### 3.2 Turns 100–206: ten founded cities

- Founded:

  | Turn | City | Steps from the capital |
  |---|---|---|
  | 116 | 25,29 | 3 |
  | 138 | 21,31 | 6 |
  | 156 | 26,33 | 7 |
  | 172 | 23,34 | 8 |
  | 181 | 32,21 | 5 |
  | 188 | 23,27 | 4 |
  | 206 | 23,23 | 4 |

  (save cities.) With the capital and the first two, that is 10 founded cities.
- Units, turns 100–199: Javelineers 15, Settlers 5, Workboats 5, Workers 3, one Galley, one
  Velites (`spending.csv`).
- AI cities inside the same ring (save cities and `K`/`Z` lines):
  - 33,29, founded on turn 169, Leonidas' until Alexander took it on turn 239.
  - 30,20 and 29,33, Leonidas', razed by the human on turns 238–239; their founding turns are
    not in the save.
- Buildings: Town Essentials, Walls, Obelisks, River Ports, Lighthouses, then Roman Forum
  and Forge from turn 180 (`buildings.csv`).
- Worker builds, turns 100–199: tracks 49, cottages 25, then farms, mines, camps, quarries,
  fishing boats, pastures (`human_builds.csv`).
- Civics: Spiritism (138), Elders (146), Standardized Tablets and Tutors (205).
- Deals (`deals.csv`):
  - Resources: Wine for Cow, Deer and Sheep (145, Willem); Wheat for Corn and Stone for
    Silk (170, 173, Cyrus).
  - Techs: Masonry for Animal Husbandry (177, Ivan); Masonry for Priesthood (188, Willem);
    Slavery for Writing (205, Suppiluliuma); Metal Casting for The Wheel (206, Brennus).
  - Given on request: Masonry to Cyrus (169), and The Wheel to Joao (214), Alexander (219),
    Afonso (227), Charles V (230). Each such gift comes with a 10-turn forced peace treaty
    (`DIPLOEVENT_GIVE_HELP` → `forcePeace`, `CvPlayer::handleDiploEvent`).
  - Refused requests: 12 times for help, 9 to join a war, 9 to stop trading
    (`diplomacy.csv`).

### 3.3 Turns 206–250: ten cities, no new ones

- Economy (`economy.csv`):

  | Turn | Pop | Hammers | Commerce | Research |
  |---|---|---|---|---|
  | 207 | 45 | 153 | 164 | 144 |
  | 249 | 79 | 512 | 745 | 651 |

  Slider 75 → 85 %. Golden age turns 229–243.
- Civics: Accounting (222), Metals and Fortification (229), Coinage and Proletariat (245).
  - Accounting: `CommerceModifiers` [25, 0, 0, 0].
  - Metals: `TradeYieldModifiers` [20, 0, −10]; `iImprovementUpgradeRateModifier` 15.
  - Coinage: `TradeYieldModifiers` [25, 0, 0]; `iTradeRoutes` 1.
  - Proletariat: farm +1 food, mine +1 hammer, workshop +1 food and +2 hammers, and others;
    `TradeYieldModifiers` [0, 50, 0]; `iWorkerSpeedModifier` 25.
  - Fortification: +1 happiness per military unit; Walls +3 happiness.
- Buildings, turns 200–249:
  - Forge 9, School of Scribes 7, City Essentials 7, Early Barracks 5, Jewellery 4, Roman
    Forum 4, Roman Depot 4, Town Essentials 3, Hellenic Temple 3, Obelisk 3, Irrigation
    Canals 3.
  - Courthouses and Ports follow from turn 250, with the wonders Praefectura Annonae (253)
    and Senate (258), both in the capital.
  - Effects (records, `BuildingInfo`):
    - Forge: +25 % hammers with Copper, Iron or Lead; −6 health.
    - Roman Forum: `CommerceModifiers` [25]; `iTradeRouteModifier` 30; 2 Merchants.
    - School of Scribes: +15 % research.
    - City Essentials: +15 % gold, +15 % land unit production, +5 happiness, +6 health, +1
      trade route, +25 % maintenance.
- Worker builds, turns 200–249: roads 26, mines 12, cottages 9, farms 5, wineries 5.
- Techs bought in deals: Mathematics and Fermentation for Monarchy (234, Suppiluliuma). The
  rest were researched.

### 3.4 Turns 238–285: eight wars, all declared by the human

`figures.py wars`. Every war starts with a human `CHANGEWAR` command.

| Declared | Target | Peace | Target cities / power / techs (turn before) | Human power / techs | Human attacks won / all | AI attacks | Cities taken (pop) | Razed | Peace terms to the human |
|---|---|---|---|---|---|---|---|---|---|
| 238 | Leonidas | 240 | 5 / 135 / 17 | 351 / 23 | 2/2 | 0 | 30,20 (1), 29,33 (2) | 2 | – |
| 252 | Pericles | 254 | 8 / 379 / 24 | 470 / 24 | 2/2 | 0 | 31,33 (1) | 0 | 220 gold |
| 257 | Alexander | 261 | 7 / 252 / 18 | 536 / 27 | 3/3 | 0 | 33,29 (2) | 0 | 255 gold |
| 268 | Masinissa | 270 | 9 / 437 / 23 | 940 / 32 | 3/3 | 0 | 16,29 (1), 28,20 (1) | 1 | 430 gold |
| 271 | Leonidas | – (eliminated 273) | 2 / 153 / 17 | 1148 / 32 | 20/20 | 0 | 38,23 (3), 39,20 (9) | 0 | – |
| 272 | Joao | open | 10 / 431 / 22 | 1199 / 32 | 2/2 | 0 | 30,16 (4) | 0 | – |
| 277 | Pericles | 285 | 7 / 454 / 28 | 1559 / 36 | 35/36 | 1 lost | 42,22 (14), 43,25 (4), 37,26 (5), 46,25 (5), 47,23 (5) | 0 | Monotheism, 1 gold/turn |
| 283 | Masinissa | open | 9 / 456 / 25 | 1794 / 37 | 12/12 | 0 | 24,17 (16), 14,26 (1) | 1 | – |

- **Military techs** before each declaration (`X` lines):
  - Turn 238: the human has Bronze Working, Mathematics and Metal Casting; Leonidas has Metal
    Casting only.
  - Turn 252: Pericles has Bronze Working, Iron Working, Mathematics, Metal Casting and
    Seafaring; the human gets Iron Working on turn 254.
  - Turns 268–283: Masinissa, Joao and Pericles have Bronze and Iron Working; Archery
    reached most AIs only from turn 258 on.
- **Gold:**
  - 1,457 at turn 267, 229 at turn 270.
  - Peace payments to the human: 905 in all (turns 254, 261, 270).
  - Tech sales: Archery to Pericles for 520 (264), Archery to Charles V for 380 (267),
    Fermentation to Ramesses for 660 (268), Seafaring to Willem for 80 (275).
  - Archery also went to Gilgamesh on request (260).
- **Upgrades:** 74 in all, 19 on turn 268 and 8 on turn 270: Velites, Javelineers, Triarii,
  Principes, Hastati (`human_commands.csv`). 280 promotions in the game.
- **Fiscus** adopted on turn 268 (`Hurrys` `HURRY_GOLD`; `CommerceModifiers` [50, 0, 0, 25]).
  Four gold rushes followed (turns 269, 269, 270, 280; `TASK` 9, hurry type 1 = `HURRY_GOLD`
  in the BTS `CIV4HurryInfo.xml`, which RoM does not replace).
- **Units built:**

  | Turns | Units |
  |---|---|
  | 220–259 | Hastati 12, Galleys 5, Ballista 1, Roman Colonists 2 |
  | 260–284 | Legionaries 24, Quinqueremes 11, Principes 7, Centurios 3, Catapults 2, Praetorian 1 |

  Unit stats (records, `UnitInfo`):

  | Unit | Strength | Moves | Cargo |
  |---|---|---|---|
  | Legionary | 10 | 2 | – |
  | Quinquereme | 8 | 4 | 4 |
  | Spearman (AI) | 4 | 1 | – |
  | Greek Phalanx (AI) | 7 | 1 | – |
  | Light Swordsman (AI) | 7 | 1 | – |

- **Buildings, turns 260–284:** Legion Barracks 11 (`UnitCombatFreeExperiences` melee 10),
  Barracks 9, Stables 8, Siege Workshops 5; Colosseum (278) and Forum Romanum (280).
- **Carthage, turns 283–284** (`A`, `Y`, `C`, `K` lines):
  - Turn 283: war declared. Carthage's `Y` lines show pop 17, 7 defenders (best Light
    Swordsman), defence 60 %, AI danger 0, no foreign land units within 2 plots. The city
    was building a Settler.
  - Turn 284:
    - Two quinqueremes move from 27,19 to 25,18, the sea plot next to the city.
    - Seven Legionaries, grouped on that plot, attack the city from the boats: 6 attacks at
      80.9–100 % win chance, all won. The attackers have 13–19 experience; the defenders
      (Axeman, Archer ×3, Spearman, War Dog) have 0–9.
    - The city is taken the same turn.
- **The defenders of the cities taken** (`figures.py cities`):
  - Turns 238–268, six cities of pop 1–2: 1–2 defenders each (Javelineer, Spearman or
    Archer) at 0–10 % defence. The three still standing at the save were founded on turns
    169, 243 and 248; the other three were razed.
  - Turns 272–285: Leonidas' 38,23 had 12 defenders (Spearmen) and 39,20 had 7. Pericles'
    cities had 2–5, best a Spearman or Phalanx, at 2–24 % defence.

## 4. Readings

Each reading uses the data of its own turns.

**R1. Turns 0–87: grow the capital on the coast before expanding; govern from the
capital.**
- Facts:
  - Two of the first three orders were Workboats; 47 % of hammers to turn 50 went to
    workboats.
  - Tribute's +25 % on all three yields in the capital, adopted on turn 35.
  - No Settler before turn 75.
- Options at turn 35:
  - The Leadership and Taxation civics the techs then allowed; Oligarchy and Tribute both
    need Slavery, the first tech researched.
  - Tribute's −10 % food in all cities costs least while there is one city.
- Contradicted if: the capital had no sea food resources to work (the turn-0 tiles are not
  in the save; *open*), or the Workboats went to other cities.

**R2. Turns 87–206: claim the land between Masinissa and Brennus with a compact ring of
cities, cheaply guarded.**
- Facts:
  - Ten cities, all within 8 steps of the capital, by turn 206.
  - Javelineers (strength 3) as the military build in turns 100–199, with one Velites.
  - Walls and Obelisks in the first buildings; tracks first in the worker builds.
- Against it: Leonidas held at least three cities inside the ring (section 3.2), one of them
  founded on turn 169, so the ring was not fully claimed by turn 206. The human took or razed
  all three on turns 238–257.
- Contradicted if: the human's own cities were founded where the AIs had already settled
  (none of the 10 is a captured city).

**R3. Turns 206–250: stop expanding and build the economy that the later army needs.**
- Facts:
  - No new city for 44 turns.
  - Hammers ×3.3 and commerce ×4.5 in the same 10 cities.
  - The buildings are multipliers: Forge +25 % hammers, Roman Forum and City Essentials +25 %
    and +15 % gold, School of Scribes +15 % research.
  - Civics Accounting, Metals, Coinage, Proletariat; worker builds turn to mines, roads,
    farms, wineries.
  - The golden age (229–243) falls in this span.
- Contradicted if: the hammers came from a few wonders' builds only (the hammer rise is
  spread over turns 207–249 in the `M` lines), or from captured cities (none before 238).

**R4. Turns 238–268: probing wars that pay for themselves.**
- Facts:
  - Four short wars (2–4 turns), each against a neighbour with less than half the human's
    power, except Pericles at 379 against 470.
  - Each takes one or two pop-1–2 cities held by one or two old defenders; three end with
    the AI paying gold (905 in all).
  - Techs sold for gold on turns 264–268 (1,560).
  - Gold peaks at 1,457 on turn 267. Fiscus (gold rushes) is adopted on 268, the turn of 19
    upgrades and of the war on Masinissa.
- Goal: turn the AIs' gold and weak border cities into an upgraded army without a long war.
- Contradicted if: the upgrades were paid from ordinary income (gold per turn on turns
  261–267 is 71–137, while gold fell by 1,228 from turn 267 to 270 after 430 gold of peace
  money), or if the AIs had attacked
  in these wars (they made no attack).

**R5. Turns 268–285: conquest with experienced Roman units, by land and sea.**
- Facts:
  - 11 Legion Barracks built (+10 melee experience), together with Oligarchy (+3),
    Spiritism's +3 for a state religion (the human's only `CONVERT` command is on turn 199)
    and Mars Temples (+3). Legionaries attacking with
    13–19 experience at 81–100 % odds.
  - 11 Quinqueremes built on turns 260–284; Carthage taken from the sea in one turn.
  - Three capitals taken in 11 turns: Leonidas' 39,20 (273), Pericles' 42,22 (280),
    Masinissa's 24,17 (284).
  - Peace with Pericles on turn 285 brings Monotheism.
- Contradicted if: the captures were made at low odds (the lowest human attack in the game
  was at 36 %, `summary.md`), or by units without these sources of experience (which
  experience came from where is not logged per unit; *open*).

## 5. The AI against this play

Each leaf gives the data, the function that produced it, and a status.

**A. The AI does not see an army at sea as a threat to its cities.**
- Data: Carthage's two `Y` lines on turn 283, both after the declaration: danger 0, no
  foreign land units within 2. The boats were 3 plots away, and the city was taken on turn 284 by units
  attacking from them.
- Code: `CvPlayerAI::AI_getPlotDanger` counts only units on plots of the city's own area
  (`pLoopPlot->area() == pPlotArea`, `CvPlayerAI.cpp:3842`). `AI_getEnemyPlotStrength` does
  the same, and is the input of the develop-or-defend branch in `CvCityAI::AI_chooseProduction`
  (`CvCityAI.cpp:1504`). A sea plot is another area, so loaded transports are never counted.
- Status: **traced** for the counting. What the city would have built with the boats counted
  is *open*; it needs the BBAI log of a replay from an autosave before turn 283.

**B. The AIs made no attack in seven of the eight wars, and one in the eighth.**
- Data:
  - `C` lines: AI attacks on the human, 1 of 81 battles.
  - `G` lines: Leonidas' 6 Spearmen with role `ATTACK_CITY` stayed in his own city 38,23
    (turns 238–240, 271). Pericles' stacks with role `ATTACK` or `ATTACK_CITY` stayed at
    37,26 and 39,21 (252–254) and at 45,26 (282–285). All had no mission target (−1).
- Status: *open*. The branch that left them in place needs the BBAI log of replayed turns.

**C. Garrisons of pop-1–2 cities near the human were one or two units at 0–10 % defence.**
- Data: section 3.4.
- Status: *open*: whether the minimum-defender branch of `AI_chooseProduction` ran for these
  cities. The AI's threat estimate counted the human's power by the paranoia rule
  (`AI_updateStrategyHash`); whether it raised the alert level for these owners on these
  turns is not logged.

**D. The AIs paid for peace soon after losing a city, and bought techs for large sums from
the player who then attacked them.**
- Data: peace for 220, 255 and 430 gold after 2–4 turns. Pericles paid 520 for Archery on
  turn 264 and was attacked on turn 277.
- Status: *open*. Who proposed each peace is not logged. The AI's trade values come from
  `AI_endWarVal` and `AI_techTradeVal`, which this analysis did not check against these
  turns.

**E. The AI's best defenders were a generation behind the human's attackers.**
- Data: Spearman (4), Phalanx (7) and Light Swordsman (7), all 1 move, with 0–9 experience,
  against Legionaries (10, 2 moves) with 13–19.
- Status: *open*: the AI's upgrade and defender-choice code against these turns.

## 6. Open data and caveats

- The user's `GlobalDefines.xml` is not known: the README installs only the DLL and
  `GlobalDefinesAlt.xml`.
  - GitLab `main` from !45 sets `COLLATERAL_COMBAT_DAMAGE` to 100; older RoM sets 10.
  - Collateral damage is not in the `C`/`R` lines, so this game cannot settle which.
- The harness's mod overlay lacks the four AI switch defines that the user's
  `GlobalDefinesAlt.xml` sets (`AI_STACK_FORECAST` 500, `AI_THREAT_VISIBLE_ARMY` 40,
  `AI_ATTACK_ODDS_FLOOR` 5, `AI_SACRIFICE_EV` 1). A replay for BBAI logs must use the user's
  file.
- Replay messages: 3,632 of 4,249 have empty text in the dump; foundings come from the
  save's city founding turns instead.

## 7. Tool changes made for this game

- `toolchain/harness/initcore.py`, new: reads the save's setup block (options, victories,
  custom names, handicaps), following `CvInitCore::read`.
  - Civilization and leader numbers are left as indices, because RoM's modular XML loading
    means file order is not index order. The names come from the `P` lines.
- `tools/xmlread.py`: each record now carries `_index`, its position in load order. Deal
  lines print tech and resource indices. Checked against six tech deals whose tech appears
  in the human's `X` lines on the deal turn.
- `tools/gamedata.py`:
  - `--scenario` and `--init` give `players.csv` and the setup tables in `summary.md`.
  - New tables: `deals.csv` and `diplomacy.csv`.
  - A city founded by the human on the plot of a city it razed now counts as founded, not
    captured. This changed game 4's split from 13/13 to 14/12. Game 3 has no such city
    (checked against its save dump), so its tables are unchanged.
