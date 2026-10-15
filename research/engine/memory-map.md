# Memory map of the RoM game core (CvGameCoreDLL)

Scope: the DLL built from `/home/user/src/rom-upstream/Assets/CvGameCoreDLL`
(MSVC 2003, 32-bit), its XML (`Assets/XML` plus `Assets/Modules`), a late
Marathon game on Mediterranean Standard. Repository files were only read.

Labels used for every number:

- `[C]` verified from code (declaration, allocation, `write()`), or exact count
- `[M]` measured: parsed from a harness snapshot of a real late game, or process
  RSS sampled while the real DLL runs in the harness
- `[E]` estimate (sizeof by hand, heap overhead, extrapolation)

Heap model for `[E]` byte counts: every `new T[n]` costs
`ceil((n*sizeof(T) + 8) / 8) * 8` bytes (Win32 heap: 8-byte header, 8-byte
granularity). VC7.1 library sizes: `std::string`/`std::wstring` (CvString,
CvWString) 28 B, `std::vector` 16 B, `std::list`/`CLinkList` 12 B,
`stdext::hash_map` about 44 B plus about 32 B per element.

## 0. Top findings

1. The per-object arrays scale with **info counts** and with **MAX_PLAYERS = 51**.
   RoM sets `MAX_CIV_PLAYERS` to 50 for Revolution (CvDefines.h:47) `[C]`.
   All 51 player and 51 team slots allocate every array, in use or not `[C][M]`.
2. **Cities are the largest consumer that grows**: about 23 KB per city `[E]`. 78% of
   that is 11 arrays sized by building (428), unit (422) and promotion (244)
   count. Measured density in a late game is 0.0 to 2.6% non-zero `[M]`.
3. **Plots** use about 3.4 MB on 64x44 `[M+E]`. Most of it is lazily allocated
   `[MAX_PLAYERS]`/`[MAX_TEAMS]` arrays with 0.1 to 16% non-default entries `[M]`.
4. The late game measured below holds about 13 MB of DLL game state `[E]`, and the
   reference game (342 cities) about 20 MB `[E]`. Measured RSS deltas match:
   +8 MB from a fresh game to the reloaded turn-481 state `[M]`.
5. A continuous run grows about **85 KB per turn more than its live state**
   `[M]`. The run from turn 400 to 481 ends at 77.0 MB RSS. The same game state
   reloaded runs at 70.0 MB. This is a leak or fragmentation, and on a long
   Marathon game it outgrows every array discussed here.
6. Save stream: 10.3 MB uncompressed, 0.53 MB after zlib `[M]`. Cities (24%), plots
   (26%) and the 51 player slots (16% fixed part) dominate the raw stream, almost
   entirely zeros.

## 1. Inputs

### 1.1 Map

`Mediterranean, Standard.scn` (the harness scenario converted from the WBS), read as data: `MAP 64 44 ...
WORLDSIZE_STANDARD`, 2816 `PLOT` records, 10 `PLAYER` records, 50 `TEAM`
records `[C]`. It is **64x44 = 2816 plots**, not 84x52. Land plots at turn 480 of
the measured game: 1842 `[M]`. Areas: 31, of which 15 are water and 16 are single
plots `[M]`.

### 1.2 Measured game used for verification

The harness game `hwork2/late/med-M1` (this map, Marathon, seed 1) has snapshots
at turn 400 and turn 480. I loaded the turn-480 snapshot with a newer harness DLL
(`hwork2/b-rom16`), ran 2 turns and dumped every object
(`HARNESS_SNAPSHOT=481 HARNESS_SNAPSHOT_OBJECTS=1`). Output stayed in the harness work directory (not published).

State at turn 481: 114 cities, 1521 units, 1048 selection groups, 47 plot groups,
6 players alive, 10 ever alive `[M]`.

The reference game in the task (342 cities, about 1800 units, 10 to 12 players)
is about 3x this game in cities. Totals for both are given in section 3.

### 1.3 Modules loaded

`Modules/MLF_CIV4ModularLoadingControls.xml` lists 79 directories with
`bLoad=1`. 71 of them do not exist; the 8 that exist (Buildings, Builds,
Custom ArtStyles, Custom Civilizations, Custom Leaderheads, Custom Units, Holy
Wars, Projects) are all listed and loaded. Their nested MLFs set no `bLoad=0`; `Junglecamp` vs.
`JungleCamp` differs only in case (Windows) `[C]`. Note: the harness
logs "default configuration ... NONE" (`logs/MLF.log`) and falls back to
enumerating every module file. The info counts it reports are identical to the
XML count below, so the result is the same either way.

### 1.4 Info counts (array lengths)

XML count: unique `<Type>` per info element over `Assets/XML` and
`Assets/Modules` (`research/tools/count_infos.py`). Runtime: `info counts:`
line printed by the real DLL in the harness (`hwork2/root-fix12/run-m410.log`).
Both agree wherever both exist `[C][M]`.

| Info type | Count | Module-only entries | Sizes per-object arrays in |
|---|---|---|---|
| BuildingInfos | 428 | 39 | CvCity x6, CvPlayer x3, CvTeam x1, CvGame x2 |
| BuildingClassInfos | 413 | 44 | CvPlayer x2, CvTeam x1, CvGame x1 |
| UnitInfos | 422 | 49 | CvCity x4, CvGame x1 |
| UnitClassInfos | 311 | 49 | CvPlayer x2, CvPlayerAI x1, CvTeam x1, CvGame x1 |
| TechInfos | 308 | 0 | CvTeam x4, CvPlayer x1, CvGame x1 |
| PromotionInfos | 244 | 0 | CvUnit x1 (bool), CvCity x1 |
| EventInfos | 517 | 0 | (infos only) |
| EventTriggerInfos | 310 | 0 | (infos only) |
| LeaderHeadInfos | 83 | 23 | - |
| BonusInfos | 73 | 1 | CvCity x4, CvPlayer x2, CvArea, CvMap x2, CvPlotGroup |
| CivicInfos | 69 | 1 | CvGame |
| BuildInfos | 56 | 1 | CvPlot (lazy) |
| ImprovementInfos | 54 | 1 | CvCity, CvPlayer (+[54][3]), CvTeam ([54][3]), CvArea |
| CivilizationInfos | 41 | 0 | - |
| UnitCombatInfos | 33 | 0 | CvUnit, CvCity, CvPlayerAI |
| CorporationInfos | 27 | 0 | CvCity, CvPlayer, CvGame |
| VoteInfos | 23 | 0 | CvGame |
| EspionageMissionInfos | 20 | 0 | - |
| SpecialistInfos | 18 | 0 | CvCity x4, CvPlayer (+[18][3]) |
| ProjectInfos | 17 | 0 | CvCity, CvTeam x3 |
| ReligionInfos | 16 | 0 | CvCity x3, CvPlayer, CvGame |
| SpecialBuildingInfos | 11 | 0 | CvPlayer, CvGame |
| TerrainInfos | 10 | 0 | CvUnit x3, CvTeam |
| Route / Victory / Handicap | 9 / 9 / 9 | 0 | CvTeam |
| Feature / Era / CivicOption | 8 / 8 / 8 | 0 | CvUnit x3 (feature), CvPlayer (civic option) |
| CultureLevelInfos | 7 | 0 | CvPlot (lazy, per player) |
| GameSpeed / SpecialUnit / Emphasize | 6 / 6 / 6 | 0 | CvGame, CvCityAI |
| Invisible / Process / Upkeep | 3 / 3 / 3 | 0 | CvPlot (lazy), CvPlayer |
| Hurry / VoteSource | 2 / 2 | 0 | CvPlayer, CvGame |

Hurry, Upkeep, Emphasize and VoteSource come from the base game's XML, not RoM
(runtime count `[M]`). Enum constants `[C]` (CvEnums.h, CvDefines.h):
NUM_YIELD_TYPES 3, NUM_COMMERCE_TYPES 4, NUM_DOMAIN_TYPES 4, NUM_UNITAI_TYPES 41,
NUM_MEMORY_TYPES 34, NUM_CONTACT_TYPES 14, NUM_FEAT_TYPES 31,
NUM_PLAYEROPTION_TYPES 22, NUM_DIRECTION_TYPES 8, NUM_CITY_PLOTS 21,
MAX_PLAYERS = MAX_TEAMS = 51 (CvDefines.h:47-57), MAX_TRADE_ROUTES 16
(GlobalDefines.xml:385).

## 2. Per-object memory

### 2.1 CvPlot (CvPlot.h:49-50, 570-610; CvPlot.cpp:43-90, lazy setters)

The whole map is one `new CvPlot[2816]` (CvMap.cpp:92), so there is no per-object
heap header.

| Part | Allocation | Bytes per plot | Line |
|---|---|---|---|
| Object (vptr, 2 battle ints, shorts, bitfields, 3 IDInfo, 25 pointers, unit list, symbol vector) | inline | ~220 `[E]` | CvPlot.h:570-610 |
| m_aiYield short[3] | always | 16 | CvPlot.cpp:45 |
| m_abIsTeamBorderCache bool[MAX_TEAMS] | always | 64 | CvPlot.cpp:53 |
| Lazy arrays (below) | first non-zero set | 0 to ~2300 | CvPlot.cpp:6639-8389 |
| Unit list node CLLNode<IDInfo> | per unit on plot | 24 per unit | CvPlot.h:608 |

Lazy arrays are allocated on the first non-default write and never freed while
the game runs `[C]`. The plot and density columns are from the turn-480 snapshot,
parsed by `research/tools/parse_map.py` `[M]`. Heap bytes are `[E]`.

| Array | Type x length | Heap B | Plots allocated | KB | Non-default entries / slots | Line |
|---|---|---|---|---|---|---|
| m_apaiCultureRangeCities (outer) | char*[51] | 216 | 2044 (73%) | 431 | inner arrays 3196 of 104,244 slots (3.1%) | 8313 |
| (inner per player) | char[7] | 16 | 3196 | 50 | - | 8322 |
| m_aiCulture | int[51] | 216 | 2011 (71%) | 424 | 4,477 / 102,561 (4.4%) | 6639 |
| m_aiPlotGroup | int[51] | 216 | 2006 (71%) | 423 | 12,812 / 102,306 (12.5%) | 6839 |
| m_aiVisibilityCount | short[51] | 112 | 2698 (96%) | 295 | 3,104 / 137,598 (2.3%) | 7046 |
| m_abRevealed | bool[51] | 64 | 2704 (96%) | 169 | 22,352 / 137,904 (16.2%) | 7557 |
| m_paiBuildProgress | short[56] | 120 | 1228 (44%) | 144 | **80 / 68,768 (0.1%)** | 7822 |
| m_aeRevealedRouteType | short[51] | 112 | 1243 (44%) | 136 | 7,525 / 63,393 (11.9%) | 7779 |
| m_aiRevealedOwner | char[51] | 64 | 2015 (72%) | 126 | 12,644 / 102,765 (12.3%) | 7282 |
| m_aeRevealedImprovementType | short[51] | 112 | 1120 (40%) | 123 | 5,690 / 57,120 (10.0%) | 7730 |
| m_aiPlayerCityRadiusCount | char[51] | 64 | 1850 (66%) | 116 | 1,851 / 94,350 (2.0%) | 6791 |
| m_aiFoundValue | short[51] | 112 | 891 (32%) | 97 | **177 / 45,441 (0.4%)** | 6748 |
| m_abRiverCrossing | bool[8] | 16 | 618 (22%) | 10 | - | 7499 |
| m_aiStolenVisibilityCount, m_aiBlockadedCount, m_apaiInvisibleVisibilityCount | - | - | 0 | 0 | never allocated | 7140, 7199, 8380 |

Per plot: fixed about 300 B, lazy 925 B on average (2.54 MB / 2816), in all
**about 3.4 MB for the map** `[M+E]`. The `[51]` dimension accounts for
about 2.3 MB of the lazy part. A game uses 11 to 13 of the 51 slots.

### 2.2 CvCity + CvCityAI (CvCity.h:1158-1374, CvCity.cpp:42-112, reset 384ff; CvCityAI.h:169-204, CvCityAI.cpp:58-62, 177)

Every array is allocated at init, not lazily `[C]`. Density is from the 114 cities
of the turn-481 dump (`research/tools/parse_cities.py`) `[M]`.

| Array | Type x length | Heap B `[E]` | Non-default entries per city `[M]` | Line (CvCity.cpp) |
|---|---|---|---|---|
| m_paiNumRealBuilding | int[428] | 1720 | 11.3 (2.6%) | 626ff |
| m_paiNumFreeBuilding | int[428] | 1720 | 0.05 | 626ff |
| m_paiBuildingProduction | int[428] | 1720 | 0.41 | 626 |
| m_paiBuildingProductionTime | int[428] | 1720 | 0.13 | 626ff |
| m_paiBuildingOriginalOwner | int[428] | 1720 | 11.3 (default -1; mirrors NumRealBuilding) | 626ff |
| m_paiBuildingOriginalTime | int[428] | 1720 | 11.3 (default MIN_INT; mirrors NumRealBuilding) | 626ff |
| m_paiUnitProduction | int[422] | 1696 | 0.25 | 644 |
| m_paiUnitProductionTime | int[422] | 1696 | 0.15 | 644ff |
| m_paiGreatPeopleUnitRate | int[422] | 1696 | 1.13 | 644ff |
| m_paiGreatPeopleUnitProgress | int[422] | 1696 | 2.04 | 644ff |
| m_paiFreePromotionCount | int[244] | 984 | **0.00** | 700 |
| m_paiNoBonus, m_paiFreeBonus, m_paiNumBonuses, m_paiNumCorpProducedBonuses | 4 x int[73] | 1216 | 0 / 0.26 / 26.2 / 0 | 606 |
| m_paiImprovementFreeSpecialists | int[54] | 224 | 0.00 | ~670 |
| 4 specialist arrays | 4 x int[18] | 320 | 1.3 / 2.8 / 0 / 0.3 | ~657 |
| religion (2 int, 1 bool), corporation (bool), unit combat, project, working plots, trade cities IDInfo[16] | - | 630 | small | 618-714 |
| Constructor arrays: 19 yield/commerce/domain, m_aiCulture/m_aiNumRevolts int[51], 4 x bool[51], rank caches | - | 1264 | culture 1.5 of 51, revealed 5.2 of 51 | 42-112 |
| CvCityAI: emphasize, special yield, m_aiPlayerCloseness int[51], m_pbEmphasize | - | 304 | - | CvCityAI.cpp:58-62, 177 |
| Object (CvDLLEntity + ~95 ints + 2 strings + order list + 5 vectors; CvCityAI adds m_aiBestBuildValue[21] + m_aeBestBuild[21]) | 1 block | ~1100 | - | CvCity.h, CvCityAI.h:181-183 |

Per city: **about 23.2 KB** `[E]`. The arrays alone are 21.9 KB `[E]`; their save
image is 21.07 KB `[M]`. The 11 building, unit and promotion arrays come to 18.1
KB, 78% of the city. Ten of them have 0 to 2.6% non-default entries in the
measured game. That game is slow to research (Marathon, 61 techs, 11 buildings
per city). In a high-tech game NumRealBuilding reaches perhaps 60 to 120 of 428,
still under 30%.

### 2.3 CvUnit + CvUnitAI (CvUnit.h:899-989, CvUnit.cpp:49, reset 391-420; CvUnitAI.h:76-84)

| Part | Type x length | Heap B `[E]` | Density `[M]` (1521 units) |
|---|---|---|---|
| m_pabHasPromotion | bool[244] | 256 | 2.93 promotions per unit (1.2%); 212 units have none |
| 3 terrain arrays (double move, attack, defense) | 3 x int[10] | 144 | 86% of units all zero |
| 3 feature arrays | 3 x int[8] | 120 | 99% all zero |
| m_paiExtraUnitCombatModifier | int[33] | 144 | 66% all zero |
| m_aiExtraDomainModifier | int[4] | 24 | - |
| Object (CvDLLEntity, ~62 ints, 2 strings, pointers; CvUnitAI +20 B) | 1 block | ~416 | - |
| List nodes: plot unit list + group unit list, free-list slot | 2 x 24 + 8 | 56 | - |

Per unit: **about 1.16 KB** `[E]`, of which arrays 688 B. All terrain, feature and
unit combat arrays are sums over the promotions the unit holds, so they can be
derived from `m_pabHasPromotion` and the promotion infos. Save record: 911 B per
unit `[M]`, 592 B of it these arrays `[C]`.

### 2.4 CvSelectionGroup + CvSelectionGroupAI (CvSelectionGroup.h:267-295, CvSelectionGroupAI.h:69-80)

Fixed members only: about 100 B object, plus the unit list (24 B per unit,
counted with units), the mission queue (about 40 B per queued mission) and
`m_aDifferentUnitCache` (vector). **About 150 B per group** `[E]`. Save
record: 83 B average `[M]`. Negligible.

### 2.5 CvPlayer + CvPlayerAI (CvPlayer.h:1246-1523, CvPlayer.cpp:62-79, 1061-1205; CvPlayerAI.h:613-735, CvPlayerAI.cpp:104-145, 372-386)

`m_aPlayers = new CvPlayerAI[MAX_PLAYERS]` (CvPlayerAI.cpp:73). All 51 slots
allocate everything below; the save holds 32,528 B for every slot never alive
`[M]`.

| Part | Arrays | Heap B per slot `[E]` |
|---|---|---|
| CvPlayer, constructor | 13 yield/commerce int[3/4], goldPerTurnByPlayer int[51], espionageSpendingWeight int[51], feats bool[31], options bool[22] | 816 |
| CvPlayer, building-sized | freeBuildingCount, extraBuildingHappiness, extraBuildingHealth: 3 x int[428] | 5,160 |
| CvPlayer, class-sized | unitClassCount/Making 2 x int[311], buildingClassCount/Making 2 x int[413] | 5,840 |
| CvPlayer, 2-D | specialistExtraYield [18][3], improvementYieldChange [54][3] (72 separate blocks) | 2,032 |
| CvPlayer, rest | bonus export/import, improvement count, researching tech bool[308], civics, religion, corporation, upkeep, ... | 1,696 |
| CvPlayerAI, player x player | 8 x int[51] counters, firstContact bool[51], attitude cache int[51], close-borders cache int[51] | 2,224 |
| CvPlayerAI, 2-D player x enum | m_aaiContactTimer [51][14], m_aaiMemoryCount [51][34]: 2 x 51 rows + 2 pointer arrays (104 blocks) | 11,040 |
| CvPlayerAI, rest | numTrainAIUnits/numAIUnits int[41], bonusValue int[73], unitClassWeights int[311], unitCombatWeights int[33], averages | 2,128 |
| Object (~150 ints, 4 wstrings, 5 free lists, 3 lists, 8 hash maps; AI: happiness/health headroom [41] each, strategic snapshot, vectors) | inline in m_aPlayers | ~2,350 |

Per slot: **about 33.3 KB** `[E]`; 51 slots = **1.70 MB**. The 39 slots unused in a
12-player game hold about 1.30 MB. Of each slot, 13.7 KB is `[MAX_PLAYERS]`
dimensioned.

Only for players that are alive (or were):

| Part | Size | Label |
|---|---|---|
| History: 8 `hash_map<int,int>` (score, economy, industry, agriculture, power, culture, espionage, revolution stability; CvPlayer.h:1509-1523), one entry per map per turn alive (CvPlayer.cpp:4026ff, CvGame.cpp:2278) | ~32 B per entry: about 125 KB per player at turn 491 | `[C]` count, `[E]` bytes |
| Settle reach `m_aiSettleLandRegion` + `m_aiSettleSeaRegion` (CvPlayerAI.cpp:24150) | 2 x numPlots x 4 = 22.5 KB per non-barbarian player | `[C]` |
| Settlement candidates (8 B each), city sites, military operations (248 B each), delivery cache (~340 B each) | small | `[C]` |
| Free-list slot arrays for cities, units, groups, plot groups, events (8 B per slot, capacity doubles) | ~16 KB for a 1000-unit player | `[E]` |

### 2.6 CvTeam + CvTeamAI (CvTeam.h:460-537, CvTeam.cpp:47-71, 307-402; CvTeamAI.cpp:35, 58-68)

`m_aTeams = new CvTeamAI[MAX_TEAMS]` (CvTeamAI.cpp:35). All 51 are fully
allocated; the save holds 12,695 B per team `[M]`.

| Part | Heap B `[E]` |
|---|---|
| 6 x int[51] + 8 x bool[51] (war, met, open borders, pacts, vassal, rebel ...) | 1,808 |
| CvTeamAI: 10 x int[51] counters + WarPlanTypes[51] | 2,376 |
| Tech: researchProgress int[308], techCount int[308], hasTech bool[308], noTradeTech bool[308] | 3,120 |
| unitClassCount int[311], buildingClassCount int[413], obsoleteBuildingCount int[428] | 4,640 |
| improvementYieldChange [54][3] (55 blocks) | 1,520 |
| project arrays incl. `std::vector<int>[17]`, commerce/moves int[4], route, terrain trade, victory, vote, canLaunch | 760 |
| Object | ~310 |

Per team **about 14.6 KB**; 51 teams = **0.74 MB** `[E]`.

### 2.7 CvGame + CvGameAI (CvGame.h:610-718, CvGame.cpp:51-56, 559-677)

One object. Arrays: ranks 6 x int[51], unit/unit class/building class created
counts (int[422]/[311]/[413]), shrine building and religion 2 x int[428], tech
can found religion bool[308], and small ones: **about 11 KB** `[E]`. The replay
message list is larger: about 200 KB of the 218 KB game section of the save `[M]`,
roughly 0.3 MB in memory `[E]`. `m_apaiPlayerVote` is declared but never
allocated `[C]`.

### 2.8 CvArea (CvArea.h:123-157, CvArea.cpp:20-51, 189-196)

| Part | Heap B `[E]` | Density `[M]` (31 areas) |
|---|---|---|
| m_aaiNumTrainAIUnits, m_aaiNumAIUnits: [51][41] each as 2 x 51 rows | 17,952 | 136 non-zero of 129,642 (0.1%) |
| 10 x int[51] per player + 4 x [51] per team | 3,024 | e.g. cities 11, units 18, power 17 non-zero |
| IDInfo[51] target cities, [51][3] yield modifier (51 rows) | 1,640 | yield modifier 0 non-zero |
| bonus int[73], improvement int[54], object | 656 | - |

Per area **about 23.9 KB**: 31 areas = **0.74 MB**. The 16 single-plot areas
(lakes, islets) cost 0.38 MB `[E]`. The number of areas depends on the map, not
on the game phase.

### 2.9 CvMap (CvMap.h:284-300, CvMap.cpp:92, 228-230, 248-255)

The plot array (2816 x ~220 B = 620 KB `[E]`), numBonus and numBonusOnLand
int[73] each, and the area free list. CvMap.cpp:248-255 also initializes 7 engine
A* finders sized width x height, plus the DLL's own secondary finder
(CvSelectionGroup.cpp:5483-5489). FAStarNode has 8 ints, 2 enum/bool fields and
12 pointers, about 88 B (FAStarNode.h). So each finder costs about 248 KB and 8
finders about 2 MB `[E]`. The executable allocates them, but the DLL decides how
many exist.

### 2.10 CvPlotGroup (CvPlotGroup.h:54-60, CvPlotGroup.cpp:67)

bonus int[73] (304 B) + 24 B per plot in the group. 47 groups use about 0.1 MB
`[E]`; save 1,647 B average `[M]`.

### 2.11 AI caches (sizes)

| Cache | Where | Size | Saved? |
|---|---|---|---|
| Found values per plot per player, short[51] lazy | CvPlot.cpp:6748, filled by CvPlayerAI.cpp:1225-1300 | 891 plots x 112 B = 100 KB `[M+E]`; 0.4% non-zero | yes, 94 KB of save; redundant because read() forces a refresh (CvPlayerAI.cpp:18888) |
| Best found value per area int[51] | CvArea | 216 B per area | yes |
| Settle reach regions | CvPlayerAI.cpp:24150 | 22.5 KB per player | no |
| Settlement candidates | CvPlayerAI.cpp:1309 | 8 B per candidate | no |
| Mission target index (static `s_kMissionTargetIndex`) | AIMissionTargetIndex.h:24-180, CvPlayerAI.cpp:12523 | 2 x numPlots x 4 = 22.5 KB + 24 B per group with a mission (~25 KB) | no |
| Unit target index (`s_kUnitTargetIndex`) | AIMissionTargetIndex.h:186-292, CvPlayerAI.cpp:12641 | 1024 x 8 = 8 KB + 24 B per entry | no |
| Path reuse owners | AIPathReuse.h, CvSelectionGroup.cpp:47-48 | 2 x 20 B (the reused search tree lives in the finder) | no |
| Secondary A* finder | CvSelectionGroup.cpp:50, 5483 | ~248 KB `[E]` (executable heap) | no |
| Attitude cache, close-borders attitude cache | CvPlayerAI.cpp:136, 145 | 2 x int[51] per slot | close-borders: yes |
| Strategic context snapshot | CvPlayerAI.h:669 | 108 B per player | no |
| Happiness and health headroom [41] each | CvPlayerAI.h:663-664 | 328 B per player | no |
| City best build per plot | CvCityAI.h:181-183 | 168 B per city | yes |
| Team border cache bool[51] per plot | CvPlot.cpp:53 | 180 KB `[E]` | no |
| City rank caches | CvCity.cpp ctor | 120 B per city | yes |

The AI caches total about 0.6 MB for the measured game, a small share of the
total `[E]`.

## 3. Totals and sanity check

### 3.1 DLL game state

| Component | Measured game, turn 481 (114 cities, 1521 units, 10 ever alive) | Reference game (342 cities, ~1800 units, 12 players, turn ~491) |
|---|---|---|
| Cities (23.2 KB each) | 2.64 MB | 7.9 MB |
| Plots, lazy arrays | 2.54 MB `[M]` counts | ~2.7 MB (more owned/worked plots) |
| Units (1.16 KB each) | 1.76 MB | 2.1 MB |
| 51 player slots | 1.70 MB | 1.70 MB |
| Player history maps | ~1.0 MB | ~1.5 MB |
| Plots, fixed | 0.85 MB | 0.85 MB |
| 51 teams | 0.74 MB | 0.74 MB |
| 31 areas | 0.74 MB | 0.74 MB |
| AI caches (incl. secondary finder) | 0.6 MB | 0.7 MB |
| Game + replay | 0.3 MB | 0.4 MB |
| Groups, plot groups | 0.27 MB | 0.4 MB |
| **Total** `[E]` | **~13 MB** | **~20 MB** |

Also loaded, but not game state: the XML infos. The arrays that `read()`
allocates from info counts alone come to about 8.4 MB `[E]`, of which
CvBuildingInfo is 3.6 MB (129 blocks per building) and CvUnitInfo 3.6 MB;
strings and other members come on top. The DLL code image is 6 MB.

### 3.2 Measured RSS (harness under Wine, whole process)

`research/run480b/mem3.tsv`, `mem4.tsv`, `mem5.tsv` `[M]`:

| Point | RSS |
|---|---|
| XML still loading (events) | 57.9 MB |
| Fresh game on this map, turn 2 | 62.0 MB |
| Turn-481 snapshot loaded, playing turn 481 | 69.5 to 70.3 MB |
| Continuous play from the turn-400 snapshot, at turn 411 / 437 / 461 / 481 | 70.0 / 72.6 / 74.7 / 77.0 MB |
| Earlier continuous runs (memA, another build): turn 233 / 400 / 515 | 65 / ~76 / 96.6 MB (`hwork2/memA/med-MARATHON-1/mem.tsv`) |

The step from a fresh game to the reloaded late state is +8 MB. The estimate
predicts +8.5 MB: 13 MB total minus about 4.5 MB already present in a fresh game
(fixed plots, slots, teams, areas). The table in 3.1 is consistent with the
measurement.

**Growth that is not live state** `[M]`: continuous play from turn 400 to 481 adds
7 MB. The state grew about 0.7 MB in that time (+400 units, history), and the
reloaded turn-481 state needs 7 MB less. That leaves about 6 MB per 81 turns, or
about 75 to 85 KB per turn. memA shows the same rate: +31 MB over 282 turns with
about 9 MB of state growth. Candidates: heap fragmentation from per-turn AI
temporaries, leaks of allocations handed to the engine stubs, or harness
telemetry. Reloading a snapshot and comparing RSS is a cheap leak test, and
`HARNESS_SNAPSHOT` makes it repeatable. Over 1500 Marathon turns this rate
would add about 120 MB, more than all the arrays in this document. It should be
attributed before the arrays are trimmed.

The task's figure of under 100 MB for the whole process matches: XML infos plus
code plus Wine come to about 58 MB, game state to 13-20 MB, and the unexplained
growth to the rest.

## 4. Largest consumers, ranked (reference game) and redundancy

| Rank | Consumer | Size `[E]` | Sparse / redundant |
|---|---|---|---|
| 1 | City building x6 and unit x4 arrays | 342 x 17.1 KB = 5.9 MB | 9 of 10 arrays have 0 to 2 non-zero entries out of 422-428 `[M]`. OriginalOwner and OriginalTime only carry information where NumRealBuilding is set (redundant indexing). |
| 2 | Plot `[51]` lazy arrays | ~2.4 MB | 0.1 to 16% density `[M]`; culture-range outer array 3.1% used |
| 3 | Unit arrays | 1800 x 0.69 KB = 1.24 MB | promotions 1.2% set; terrain, feature and unit-combat arrays are derivable from promotions and 66-99% all zero `[M]` |
| 4 | 51 player slots | 1.70 MB | 39 slots unused (1.3 MB); contact/memory 51 x 48 per slot = 0.56 MB, mostly unused rows |
| 5 | History hash maps | ~1.5 MB | 8 B of data per ~32 B node |
| 6 | City other arrays + object | 342 x 6 KB = 2.0 MB | FreePromotionCount, NoBonus, CorpProducedBonuses, ImprovementFreeSpecialists all zero `[M]` |
| 7 | Plot fixed (object + team border cache + yield) | 0.85 MB | team border cache could be 8 B inline |
| 8 | 51 teams | 0.74 MB | 39 teams unused (0.57 MB) |
| 9 | Areas | 0.74 MB | 99.9% zeros in the [51][41] unit AI counts `[M]` |
| 10 | AI caches, replay, groups | ~1.5 MB | found values saved needlessly |

Duplicated or derivable data `[C]`:

- `CvCity::m_paiBuildingOriginalOwner/Time` are keyed by building but meaningful
  only for real buildings.
- Unit terrain, feature and unit-combat modifier arrays equal sums over held
  promotions plus unit-type data (`processPromotion`).
- `CvPlot::m_aiFoundValue` is written to the save, but CvPlayerAI::read sets
  `m_iFoundValuesCacheTurn = -1`, so the values are recomputed after loading
  (CvPlayerAI.cpp:18888, 591-594).
- City rank caches (`m_aiBaseYieldRank`, valid flags) are saved but are caches.
- `CvPlayer::m_paiExtraBuildingYield/Commerce` (int**) are declared and never
  allocated; `CvGame::m_apaiPlayerVote` likewise.

## 5. Save file (`write()` functions)

Turn-481 stream: 10,336,583 B raw, 529,783 B zlib level 6. Real saves are zlib
compressed (`toolchain/harness/sav2dat.py`). Sections from `.game.idx` and
the object dump `[M]`:

| Section | Raw | % raw | zlib | Dominant arrays |
|---|---|---|---|---|
| Plots (CvPlot::write, CvPlot.cpp:9243) | 2.68 MB | 26% | 148 KB (with areas) | cultureRange 442 KB (51 x int count 0 per plot), culture 413, plotGroup 412, vis 278, fixed fields 251, buildProgress 149, revealed 141, revRoute 130, revImpr 117, revOwner 106, cityRadius 97, found 94 |
| Cities (CvCity::write, CvCity.cpp:14304) | 2.52 MB | 24% | 52 KB | 22.1 KB per city: 6 building arrays 10.3 KB, 4 unit arrays 6.75 KB, promotion 0.98 KB |
| Player slots, fixed part (CvPlayer.cpp:18993, CvPlayerAI.cpp:19139) | 51 x 32.5 KB = 1.66 MB | 16% | (in players) | building x3 5.1 KB, class x4 5.8 KB, contact+memory 9.8 KB per slot |
| Units (CvUnit.cpp:12895) | 1.39 MB | 13% | 59 KB | 911 B per unit, 592 B arrays (promotions 244) |
| Areas (CvArea.cpp:973) | 0.66 MB | 6% | (with plots) | 21,149 B per area, 16.7 KB of it [51][41] x2 |
| Teams (CvTeam.cpp:7434, CvTeamAI.cpp:4038) | 0.65 MB | 6% | 6 KB | 12,695 B per team |
| Other player data (history, free lists, events) | ~0.40 MB | 4% | ~200 KB | history 8 x 8 B per turn per player |
| Game (CvGame.cpp:8525) | 0.22 MB | 2% | 24 KB | replay messages |
| Groups, plot groups | 0.16 MB | 2% | 30 KB | - |

The raw stream is mostly zeros. Compressed, the most expensive parts are
player history and other non-object player data (about 200 KB), the plots (about
148 KB with areas), units (59 KB) and cities (52 KB). The raw size still matters:
the engine holds the whole stream in memory while saving and loading (10 MB here,
about 15 MB for the reference game `[E]`), and the time to write and parse it
grows with it.

## 6. Proposals

Savings are for the reference game. Save-format notes: every class writes a
`uiFlag` version first, so a new layout can be read alongside the old one. A
change that keeps writing the old dense layout needs no save change.

| # | Change | Saving `[E]` | Value range / correctness | Save format | Time effect | Risk |
|---|---|---|---|---|---|---|
| P1 | City sparse production: Building/Unit Production + ProductionTime and GreatPeopleUnitRate/Progress as small sorted vectors of (type, value) | 342 x 10.1 KB = **3.5 MB** | ints stay int: production on Marathon can exceed 32767 | new city uiFlag; old saves converted on read; or keep dense writes | lookup O(k), k <= 3 measured: same as now; loops that sum production get faster | medium: many accessors, Python API unchanged |
| P2 | City buildings: NumRealBuilding and NumFreeBuilding as bitsets (both are 0/1: CITY_MAX_NUM_BUILDINGS = 1, getNumBuilding clamps, CvCity.cpp:5633; char[428] if counts are wanted); OriginalOwner (char) and OriginalTime (short year) only in a per-real-building record | 342 x (3.3 + 3.1) KB = **2.2 MB** | owner -1..50 fits char; year fits short | as P1 | getNumRealBuilding O(1) stays; iterating real buildings becomes O(present) instead of O(428), faster | low-medium |
| P3 | City lazy arrays: FreePromotionCount, NoBonus, NumCorpProducedBonuses, ImprovementFreeSpecialists, FreeSpecialistCount, ForceSpecialistCount allocated on first non-zero write (the CvPlot pattern) | 342 x 2.0 KB = **0.7 MB** | measured all-zero | count-prefixed write as in CvPlot::write | one NULL test per read | low |
| P4 | Lazy player and team slots: allocate info-sized arrays only when a slot is first initialized for a real player (CvInitCore slot used, Revolution spawn, setAlive) | 39 x 33 KB + 39 x 14.6 KB = **1.9 MB** | accessors return 0 for NULL | write a 0/1 flag per array (as CvPlot) | none | medium: Revolution creates players mid-game; Python may query dead slots |
| P5 | Plot bit masks inline: m_abRevealed, m_abIsTeamBorderCache as uint64 (MAX_TEAMS 51 <= 64), m_abRiverCrossing as uint8 | 173 + 180 + 10 = **0.36 MB** | exact | keep writing bool[51] to stay compatible | faster (no indirection) | low |
| P6 | Plot culture range: replace char*[51] + char[7] per player by a small vector of (player, counts[7]) | **~0.43 MB** | exact | keep the old write layout or a count-prefixed list (saves 400 KB raw) | O(k), k ~1.6 | low-medium |
| P7 | Plot per-player values as sparse lists: culture (int), plotGroup (int id), cityRadius (char), revealedOwner/Imp/Route; visibility counts sparse plus a uint64 'visible' mask so the hot isVisible stays O(1) | **~1.2 MB** | culture must stay int (plot culture reaches millions); plot group ids include the free-list generation and stay int | keep dense writes or new flag | culture and plot-group reads O(k), k 2 to 6; visibility unchanged with the mask | medium: hot paths (culture spread, plot groups, pathing) |
| P8 | Plot build progress: free the array when all entries return to 0, or keep a (build, progress) list | **~0.14 MB** | exact | unchanged or smaller | none | low |
| P9 | Do not save CvPlot found values; or move them to CvPlayerAI as one vector<short> per alive AI | save -94 KB raw; memory ~0 to -30 KB | recomputed after load already | drop the array from the plot record (new flag) | none | low |
| P10 | Unit promotions as bitset (32 B) and terrain/feature/unit-combat arrays lazy (or derived from promotions on demand) | 1800 x ~0.5 KB = **0.9 MB** | exact | keep writing the dense arrays, or new unit flag (saves 500 B per unit raw) | bit test O(1); deriving modifiers costs a loop over ~3 promotions per combat query | low (lazy) / medium (derived) |
| P11 | History as `std::vector<int>` per metric indexed by turn - start turn, instead of hash_map | 12 x 8 x 491 x 28 B = **1.3 MB** | exact | write the same (turn, value) pairs | O(1) append and lookup, faster | low |
| P12 | Area unit AI counts [51][41] x2: allocate a player's row on first non-zero, or keep them in CvPlayerAI per area | 31 x 17.5 KB = **0.54 MB**, more on maps with many lakes | exact | count-prefixed rows | none | low |
| P13 | CvPlayerAI contact timers and memory counts as one contiguous short[51][14] and short[51][34] instead of 104 heap blocks | 51 x ~6 KB = **0.3 MB**, and 5,200 fewer heap blocks | timers are turns (< 32767); memory counts small, short is safe, char is not proven | keep writing ints | better locality | low |
| P14 | MAX_CIV_PLAYERS 50 -> 18 (BtS default) or 32 | about **4 MB** at 18 (plots 1.5, slots 1.2, teams 0.5, areas 0.5, cities 0.2) | Revolution and BarbarianCiv need free slots | breaks every save (arrays written without counts) | none | high |
| P15 | Find the ~80 KB/turn growth (section 3.2) before trimming arrays | up to tens of MB on long games | - | - | - | - |

P1 to P3 shrink a city from about 23 KB to about 5 KB. With P4, P10 and P11
they save about 10.5 MB of the 20 MB in the reference game, without changing
what a save contains, only its layout. Allocation count also falls: today one
city makes about 65 heap blocks, one player slot about 235.

int -> short/char candidates checked against value ranges `[C]`: building
counts (cap 1), original owner (-1..50), original time (game year, fits
short), production times (turns, fit short), visibility counts (already short),
contact timers (turns). Must stay int: culture (plot and city), production
progress, great-people progress, gold, plot-group ids, unit ids (free-list ids
carry a generation in the bits above bit 13, FFreeListTrashArray.h:23-26).

## 7. What the DLL does to the executable's memory

The executable's 4 GB address space (2 GB unless the exe is large-address-aware)
is filled mostly by art. The DLL's share is the ~60 MB process baseline plus
game state above. The DLL decides how much art is referenced and how many
engine objects exist:

| DLL-side choice | Count `[C]` | Effect on executable memory |
|---|---|---|
| Unit art defines: early/middle/late tag per unit, per unit art style (CvInfos.cpp:5280-5294; style from the civilization, CvUnit.cpp:14109-14111) | 885 unit art defines, 825 distinct unit NIFs, 559 KFM animation files, 22 unit art styles with 652 style overrides | each distinct NIF used by a visible unit is loaded and cached; more civs with own styles and a longer game (era switch at eras > 2 and > 4) touch more NIFs |
| One engine entity per unit and city (CvDLLEntity::createCityEntity CvCity.cpp:102, createUnitEntity CvUnit.cpp:61) | 1800 units, 342 cities | each unit entity draws GroupSize models (UnitMeshGroups), so models = units x group size; stacking or hiding units reduces it |
| Building art per city (CvCity layout) | 418 building art defines, 321 distinct NIFs | wonders and unique buildings each add a model |
| Plot symbols and flags (CvPlot.h:596-610: feature, route, river, flag, flag offset, yield symbols) | up to 2816 plots x several | engine objects scale with revealed plots |
| Improvement, bonus, leaderhead, movie art | 45 / 53 / 83 NIFs, 118 movies | leaderheads load on diplomacy; movies stream |
| Path finders (CvMap.cpp:248-255, CvSelectionGroup.cpp:5487) | 8 x width x height nodes | ~2 MB on 64x44, ~8 MB on a 120x80 map `[E]` |
| Save buffers | 10-15 MB raw stream | transient during save, autosave and load; P1-P4 roughly halve it |

Counts come from 96 art define files under `XML/Art` and the modules. The art
binaries are not in this checkout, so file sizes are not measured. Choices that
cut executable memory: fewer distinct unit art variants (art styles, era
variants), smaller GroupSize for common late units, fewer on-map unit entities,
fewer revealed-plot symbols.

## 8. Reproduce

- Info counts: `python3 -I research/tools/count_infos.py /home/user/src/rom-upstream/Assets`
- Plot and area density: `python3 -I research/tools/parse_map.py research/run480b/out.jsonl.t481.game 217906`
- City density: `python3 -I research/tools/parse_cities.py research/run480b/out.jsonl.t481.game.obj research/run480b/out.jsonl.t481.game.objidx`
- Snapshot run: in `research/run480b`, with `vers/env.sh` sourced,
  `HARNESS_SNAPSHOT=481 HARNESS_SNAPSHOT_OBJECTS=1 wine harness.exe save s480.init s480.game 2 out.jsonl 1 20000`
  (DLL from `hwork2/b-rom16`, snapshot from `hwork2/late/med-M1`).
- RSS: `research/run480b/mem3.tsv` (reload), `mem4.tsv` (fresh game),
  `mem5.tsv` (continuous turns 400-481: epoch, turn, RSS kB, data kB).

All paths are relative to the harness work directory (not published).
