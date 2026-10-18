<!-- Rendered by tools/docs.py from workers-game4.md.in. Do not edit; edit the template. -->
# Workers, game 4

Figures from `tools/workers.py` (registry `games/game4/workers.fig.json`). Every number below comes
from that registry; the table at the end gives each figure's unit, actor, turn and source.

## Description

**Build orders, by build and by the unit that was ordered.** These are orders. The war log
does not record whether an order was completed.

| build | HASTATI | JAVELINEER | PRINCIPES | ROME_LEGIONARY | WORKBOAT | WORKER |
|---|---|---|---|---|---|---|
| BUILD_TRACK | 1 | 37 | 0 | 0 | 0 | 31 |
| BUILD_ROAD | 4 | 0 | 1 | 2 | 0 | 41 |
| BUILD_MINE | 0 | 0 | 0 | 0 | 0 | 42 |
| BUILD_COTTAGE | 0 | 0 | 0 | 0 | 0 | 35 |
| BUILD_FARM | 0 | 0 | 0 | 0 | 0 | 28 |
| BUILD_PAVED | 1 | 0 | 1 | 8 | 0 | 4 |
| BUILD_CAMP | 0 | 9 | 0 | 0 | 0 | 4 |
| BUILD_FISHING_BOATS | 0 | 0 | 0 | 0 | 9 | 0 |
| BUILD_WINERY | 0 | 0 | 0 | 0 | 0 | 6 |
| BUILD_QUARRY | 1 | 0 | 0 | 0 | 0 | 3 |
| BUILD_PASTURE | 0 | 0 | 0 | 0 | 0 | 3 |
| BUILD_WORKSHOP | 0 | 0 | 0 | 0 | 0 | 3 |
| BUILD_OLIVE_FARM | 0 | 0 | 0 | 0 | 0 | 2 |
| all values | 7 | 46 | 2 | 10 | 9 | 202 |

*orders; who: human (player 3); turn: 49-285; rows counted: 276; source: A lines MISSION_BUILD (human_commands.csv). Every value counted (13).*

What each build is (every build ordered):

| BuildInfo | Fields set (records.json) |
|---|---|
| BUILD_TRACK | `RouteType` ROUTE_TRACK; `iTime` 150 |
| BUILD_ROAD | `PrereqTech` TECH_THE_WHEEL; `RouteType` ROUTE_ROAD; `iCost` 2; `iTime` 200 |
| BUILD_MINE | `ImprovementType` IMPROVEMENT_MINE; `PrereqTech` TECH_MINING; `iTime` 400 |
| BUILD_COTTAGE | `ImprovementType` IMPROVEMENT_COTTAGE; `PrereqTech` TECH_POTTERY; `iTime` 400 |
| BUILD_FARM | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300},{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_FARM; `PrereqTech` TECH_AGRICULTURE; `iTime` 500 |
| BUILD_PAVED | `PrereqTech` TECH_CONSTRUCTION; `RouteType` ROUTE_PAVED; `bShiftDown` True; `iCost` 4; `iTime` 250 |
| BUILD_CAMP | `FeatureStructs` [{"FeatureType":"FEATURE_SWAMP","PrereqTech":"TECH_WATERWORKS","bRemove":true,"iProduction":0,"iTime":800}]; `ImprovementType` IMPROVEMENT_CAMP; `PrereqTech` TECH_HUNTING; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_FISHING_BOATS | `ImprovementType` IMPROVEMENT_FISHING_BOATS; `PrereqTech` TECH_FISHING; `bKill` True; `iHotKeyPriority` 1 |
| BUILD_WINERY | `FeatureStructs` [{"FeatureType":"FEATURE_JUNGLE","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":20,"iTime":400},{"FeatureType":"FEATURE_FOREST","PrereqTech":"TECH_BRONZE_WORKING","bRemove":true,"iProduction":30,"iTime":300}]; `ImprovementType` IMPROVEMENT_WINERY; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |
| BUILD_QUARRY | `ImprovementType` IMPROVEMENT_QUARRY; `PrereqTech` TECH_MASONRY; `iTime` 600 |
| BUILD_PASTURE | `ImprovementType` IMPROVEMENT_PASTURE; `PrereqTech` TECH_ANIMAL_HUSBANDRY; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 400 |
| BUILD_WORKSHOP | `ImprovementType` IMPROVEMENT_WORKSHOP; `PrereqTech` TECH_METAL_CASTING; `iTime` 600 |
| BUILD_OLIVE_FARM | `ImprovementType` IMPROVEMENT_OLIVE_FARM; `PrereqTech` TECH_FERMENTATION; `bShiftDown` True; `iHotKeyPriority` 1; `iTime` 500 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

**The same orders, each plot and build counted once:**

| build | all |
|---|---|
| BUILD_TRACK | 64 |
| BUILD_ROAD | 43 |
| BUILD_MINE | 34 |
| BUILD_COTTAGE | 28 |
| BUILD_FARM | 21 |
| BUILD_PAVED | 14 |
| BUILD_CAMP | 13 |
| BUILD_FISHING_BOATS | 9 |
| BUILD_WINERY | 5 |
| BUILD_QUARRY | 3 |
| BUILD_PASTURE | 3 |
| BUILD_WORKSHOP | 3 |
| BUILD_OLIVE_FARM | 2 |
| all values | 242 |

*distinct plots; who: human (player 3); turn: 49-285; rows counted: 242; source: A lines MISSION_BUILD, first order per plot and build. Every value counted (13).*

**Route-to orders** (a road along a path):

| unit | all |
|---|---|
| WORKER | 24 |
| all values | 24 |

*orders; who: human (player 3); turn: 206-283; rows counted: 24; source: A lines MISSION_ROUTE_TO. Every value counted (1).*

**Automation orders:**

| unit | AUTOMATE_BUILD | AUTOMATE_EXPLORE |
|---|---|---|
| WORKBOAT | 8 | 0 |
| GALLEY | 0 | 7 |
| SCOUT | 0 | 1 |
| JAVELINEER | 0 | 1 |
| EXPLORER | 0 | 1 |
| all values | 8 | 10 |

*orders; who: human (player 3); turn: 0-276; rows counted: 18; source: A lines COMMAND_AUTOMATE; type from CvEnums.h AutomateTypes. Every value counted (5).*

**Work rates of the units that were ordered to build.** Rates are per turn, against a build's
`iTime` scaled by Marathon's `iBuildPercent` 75 (`CvPlot::getBuildTime`):

| Unit | `iWorkRate` |
|---|---|
| Worker | 100 |
| Javelineer | 100 |
| Workboat | 100 |
| Rome Legionary | 175 |
| Hastati | 175 |
| Principes | 175 |

At the game handicap (Monarch) the AI's work rate is raised by 20 %
(`iAIWorkRateModifier`, `CvUnit::workRate`).

**Improvements on every city tile at the save, land and water, worked and unworked:**

| improvement | human_founded worked | human_founded unworked | human_captured worked | human_captured unworked | ai worked | ai unworked |
|---|---|---|---|---|---|---|
| - | 31 | 70 | 23 | 20 | 263 | 947 |
| MINE | 29 | 0 | 5 | 0 | 216 | 45 |
| FARM | 18 | 0 | 3 | 0 | 175 | 32 |
| CAMP | 3 | 0 | 0 | 0 | 71 | 71 |
| FISHING_BOATS | 14 | 1 | 4 | 1 | 104 | 16 |
| COTTAGE | 0 | 0 | 0 | 0 | 31 | 53 |
| PASTURE | 3 | 0 | 3 | 0 | 65 | 1 |
| HAMLET | 6 | 0 | 2 | 0 | 17 | 8 |
| WORKSHOP | 1 | 0 | 0 | 0 | 15 | 5 |
| QUARRY | 3 | 0 | 0 | 0 | 16 | 1 |
| PLANTATION | 0 | 0 | 0 | 0 | 13 | 5 |
| OLIVE_FARM | 2 | 0 | 0 | 0 | 8 | 1 |
| APPLE_FARM | 0 | 0 | 0 | 0 | 10 | 0 |
| VILLAGE | 7 | 0 | 0 | 0 | 3 | 0 |
| WINERY | 5 | 0 | 0 | 0 | 1 | 2 |
| SHAFT_MINE | 1 | 0 | 0 | 0 | 5 | 1 |
| SILK_FARM | 0 | 0 | 0 | 0 | 2 | 0 |
| CITY_RUINS | 0 | 1 | 0 | 0 | 0 | 0 |
| FORT | 0 | 0 | 0 | 0 | 0 | 1 |
| all values | 123 | 72 | 40 | 21 | 1015 | 1189 |

*tiles at save; who: all players; turn: save 285; rows counted: 2460; source: tiles.csv (save dump). Every value counted (19).*

What each improvement is (every improvement present):

| ImprovementInfo | Fields set (records.json) |
|---|---|
| - | (none: no record) |
| MINE | `BonusTypeStructs` [[{"BonusType":"BONUS_BAUXITE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COAL","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COPPER","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GEMS","YieldChanges":0,-1,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GOLD","YieldChanges":0,-1,6,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_IRON","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SILVER","YieldChanges":0,-1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_URANIUM","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SULPHUR","YieldChanges":0,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_LEAD","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `ImprovementUpgrade` IMPROVEMENT_SHAFT_MINE; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,1,0]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,2,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,2,0]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,0]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_EXPLOSIVES","TechYields":[-1,1,0]},{"PrereqTech":"TECH_SEISMOLOGY","TechYields":[0,1,0]}]; `YieldChanges` [0,1,0]; `bHillsMakesValid` True; `bOutsideBorders` True; `iAdvancedStartCost` 24; `iAirBombDefense` 10; `iPillageGold` 10; `iUpgradeTime` 40 |
| FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_CORN","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_RICE","YieldChanges":1,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_WHEAT","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_POTATO","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `IrrigatedYieldChange` [2,0,0]; `PrereqNatureYields` [1,0,0]; `TechYieldChanges` [{"PrereqTech":"TECH_FERMENTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[1,0,0]},{"PrereqTech":"TECH_CROP_ROTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_BIOLOGY","TechYields":[1,0,0]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,0]},{"PrereqTech":"TECH_MACHINE_TOOLS","TechYields":[1,-1,0]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[1,-1,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true},{"TerrainType":"TERRAIN_MARSH","bMakesValid":true}]; `bCarriesIrrigation` True; `bFreshWaterMakesValid` True; `bRequiresFlatlands` True; `bRequiresIrrigation` True; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| CAMP | `BonusTypeStructs` [[{"BonusType":"BONUS_DEER","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":2500},{"BonusType":"BONUS_FUR","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":3000},{"BonusType":"BONUS_IVORY","YieldChanges":0,2,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COW","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_HORSE","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PIG","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHEEP","YieldChanges":1,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CANNABIS","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SUGAR","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_APPLE","YieldChanges":1,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_OLIVES","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_DYE","YieldChanges":0,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COFFEE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_BANANA","YieldChanges":2,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COTTON","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_INCENSE","YieldChanges":0,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_LEMON","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SPICES","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TEA","YieldChanges":1,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TOBACCO","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_WINE","YieldChanges":1,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `FeatureMakesValids` [{"FeatureType":"FEATURE_FOREST","bMakesValid":true}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATCHLOCK","TechYields":[0,0,1]},{"PrereqTech":"TECH_SEMI_AUTOMATIC_WEAPONS","TechYields":[0,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[2,0,0]}]; `YieldChanges` [1,0,0]; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 5 |
| FISHING_BOATS | `BonusTypeStructs` [[{"BonusType":"BONUS_CLAM","YieldChanges":3,0,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CRAB","YieldChanges":2,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_FISH","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PEARLS","YieldChanges":1,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHRIMP","YieldChanges":3,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_SONAR","TechYields":[1,0,1]},{"PrereqTech":"TECH_AQUACULTURE","TechYields":[1,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `bWater` True; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| COTTAGE | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementUpgrade` IMPROVEMENT_HAMLET; `TechYieldChanges` [{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true},{"TerrainType":"TERRAIN_MARSH","bMakesValid":true}]; `YieldChanges` [0,0,1]; `bFreshWaterMakesValid` True; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 10; `iUpgradeTime` 10 |
| PASTURE | `BonusTypeStructs` [[{"BonusType":"BONUS_COW","YieldChanges":3,2,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_HORSE","YieldChanges":0,2,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_PIG","YieldChanges":4,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SHEEP","YieldChanges":3,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_FERMENTATION","TechYields":[1,0,0]},{"PrereqTech":"TECH_MATHEMATICS","TechYields":[2,0,0]},{"PrereqTech":"TECH_REFRIGERATION","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[0,0,2]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[2,0,0]}]; `iAdvancedStartCost` 24; `iAirBombDefense` 5; `iPillageGold` 5 |
| HAMLET | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementPillage` IMPROVEMENT_COTTAGE; `ImprovementUpgrade` IMPROVEMENT_VILLAGE; `TechYieldChanges` [{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `YieldChanges` [0,0,2]; `iAdvancedStartCost` -1; `iAirBombDefense` 5; `iDefenseModifier` 10; `iPillageGold` 15; `iUpgradeTime` 20 |
| WORKSHOP | `PrereqNatureYields` [1,0,0]; `RouteYieldChanges` [{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,1,0]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,1,1]},{"RouteType":"ROUTE_JUMPLANE","RouteYields":[0,1,1]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,1]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_GUILDS","TechYields":[0,1,0]},{"PrereqTech":"TECH_CHEMISTRY","TechYields":[0,1,0]},{"PrereqTech":"TECH_ORGANIC_CHEMISTRY","TechYields":[0,1,0]},{"PrereqTech":"TECH_DNA_COMPUTING","TechYields":[0,0,1]},{"PrereqTech":"TECH_WIRELESS_ELECTRICITY","TechYields":[0,1,0]}]; `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true}]; `YieldChanges` [-1,1,0]; `bFreshWaterMakesValid` True; `bRequiresFlatlands` True; `iAdvancedStartCost` 36; `iAirBombDefense` 5; `iPillageGold` 5 |
| QUARRY | `BonusTypeStructs` [[{"BonusType":"BONUS_MARBLE","YieldChanges":0,1,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_STONE","YieldChanges":0,2,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SALT","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_OBSIDIAN","YieldChanges":0,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `RouteYieldChanges` [{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,1,0]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,1,0]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,0]},{"PrereqTech":"TECH_IRON_WORKING","TechYields":[0,1,0]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_EXPLOSIVES","TechYields":[0,1,0]},{"PrereqTech":"TECH_CIVIL_ENGINEERING","TechYields":[0,0,1]},{"PrereqTech":"TECH_ANDROIDS","TechYields":[0,2,0]}]; `bOutsideBorders` True; `iAdvancedStartCost` 36; `iAirBombDefense` 10; `iPillageGold` 5 |
| PLANTATION | `BonusTypeStructs` [[{"BonusType":"BONUS_BANANA","YieldChanges":4,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_DYE","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_INCENSE","YieldChanges":0,0,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SPICES","YieldChanges":1,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_SUGAR","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_CANNABIS","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COFFEE","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_LEMON","YieldChanges":1,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_COTTON","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TOBACCO","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_RUBBER","YieldChanges":0,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0},{"BonusType":"BONUS_TEA","YieldChanges":1,1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_PESTICIDES","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[0,0,2]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[0,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| OLIVE_FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_OLIVES","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_CURRENCY","TechYields":[0,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_GLOBALIZATION","TechYields":[0,0,1]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| APPLE_FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_APPLE","YieldChanges":4,0,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_CURRENCY","TechYields":[0,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_GLOBALIZATION","TechYields":[0,0,1]},{"PrereqTech":"TECH_GENEMANIPULATION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| VILLAGE | `BonusTypeStructs` [[{"BonusType":"BONUS_BERNSTEIN","YieldChanges":0,0,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `ImprovementPillage` IMPROVEMENT_HAMLET; `ImprovementUpgrade` IMPROVEMENT_TOWN; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,0,1]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,0,1]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,0,1]},{"RouteType":"ROUTE_GRAVTUBE","RouteYields":[0,0,1]}]; `TechYieldChanges` [{"PrereqTech":"TECH_PRINTING_PRESS","TechYields":[0,0,1]},{"PrereqTech":"TECH_PERSONAL_ROBOTS","TechYields":[0,2,0]},{"PrereqTech":"TECH_VERTICAL_FARMING","TechYields":[1,0,0]},{"PrereqTech":"TECH_ORGANIC_CITIES","TechYields":[1,0,0]}]; `YieldChanges` [0,0,3]; `bActsAsCity` True; `iAdvancedStartCost` -1; `iAirBombDefense` 5; `iDefenseModifier` 15; `iPillageGold` 20; `iUpgradeTime` 40 |
| WINERY | `BonusTypeStructs` [[{"BonusType":"BONUS_WINE","YieldChanges":2,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[1,0,1]},{"PrereqTech":"TECH_PESTICIDES","TechYields":[1,0,1]},{"PrereqTech":"TECH_ARTIFICIAL_EVOLUTION","TechYields":[1,0,0]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 10 |
| SHAFT_MINE | `BonusTypeStructs` [[{"BonusType":"BONUS_BAUXITE","YieldChanges":0,1,1,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COAL","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_COPPER","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GEMS","YieldChanges":0,-1,5,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_GOLD","YieldChanges":0,-1,6,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_IRON","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SILVER","YieldChanges":0,-1,4,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_URANIUM","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_SULPHUR","YieldChanges":0,0,2,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000},{"BonusType":"BONUS_LEAD","YieldChanges":0,1,0,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":10000}]]; `ImprovementPillage` IMPROVEMENT_MINE; `RouteYieldChanges` [{"RouteType":"ROUTE_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_PAVED","RouteYields":[0,1,0]},{"RouteType":"ROUTE_ROMAN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_MODERN_ROAD","RouteYields":[0,1,0]},{"RouteType":"ROUTE_RAILROAD","RouteYields":[0,2,0]},{"RouteType":"ROUTE_RAILROAD_ELECTRIC","RouteYields":[0,2,0]}]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,1,0]},{"PrereqTech":"TECH_MACHINERY","TechYields":[0,1,0]},{"PrereqTech":"TECH_WATERWORKS","TechYields":[0,1,0]},{"PrereqTech":"TECH_EXPLOSIVES","TechYields":[-1,0,0]},{"PrereqTech":"TECH_SEISMOLOGY","TechYields":[0,1,0]}]; `YieldChanges` [0,2,1]; `bOutsideBorders` True; `iAdvancedStartCost` 48; `iAirBombDefense` 10; `iHappiness` -1; `iPillageGold` 10 |
| SILK_FARM | `BonusTypeStructs` [[{"BonusType":"BONUS_SILK","YieldChanges":0,0,3,"bBonusMakesValid":true,"bBonusTrade":true,"iDiscoverRand":0}]]; `TechYieldChanges` [{"PrereqTech":"TECH_MATHEMATICS","TechYields":[0,0,1]},{"PrereqTech":"TECH_CURRENCY","TechYields":[0,0,1]},{"PrereqTech":"TECH_MERCANTILISM","TechYields":[0,0,1]},{"PrereqTech":"TECH_REPLACEABLE_PARTS","TechYields":[0,0,1]},{"PrereqTech":"TECH_COMPUTERS","TechYields":[0,0,1]},{"PrereqTech":"TECH_PLASTIC_ELECTRONICS","TechYields":[0,0,1]}]; `iAdvancedStartCost` 30; `iAirBombDefense` 5; `iPillageGold` 5 |
| CITY_RUINS | `iAdvancedStartCost` -1; `iAirBombDefense` 10; `iDefenseModifier` 15 |
| FORT | `TerrainMakesValids` [{"TerrainType":"TERRAIN_GRASS","bMakesValid":true},{"TerrainType":"TERRAIN_PLAINS","bMakesValid":true},{"TerrainType":"TERRAIN_DESERT","bMakesValid":true},{"TerrainType":"TERRAIN_TUNDRA","bMakesValid":true},{"TerrainType":"TERRAIN_SNOW","bMakesValid":true},{"TerrainType":"TERRAIN_MARSH","bMakesValid":true}]; `bActsAsCity` True; `bOutsideBorders` True; `iAdvancedStartCost` 60; `iAirBombDefense` 20; `iDefenseModifier` 50 |

*Yield arrays are food, production, commerce; commerce arrays gold, research, culture, espionage.*

**Yields of worked tiles at the save**, by improvement. Food, hammers and commerce are given
separately:

| improvement | human_founded | human_captured | ai |
|---|---|---|---|
| - | 3.00 | 2.30 | 2.88 |
| MINE | 1.31 | 0.40 | 0.49 |
| FARM | 9.11 | 7.67 | 7.92 |
| FISHING_BOATS | 6.86 | 6.00 | 6.53 |
| CAMP | 5.00 | - | 3.58 |
| PASTURE | 8.33 | 9.00 | 8.05 |
| COTTAGE | - | - | 1.65 |
| HAMLET | 1.17 | 1.50 | 2.35 |
| QUARRY | 1.67 | - | 0.56 |
| WORKSHOP | 2.00 | - | 1.00 |
| PLANTATION | - | - | 3.23 |
| APPLE_FARM | - | - | 9.00 |
| OLIVE_FARM | 4.50 | - | 5.00 |
| VILLAGE | 1.57 | - | 3.00 |
| WINERY | 6.00 | - | 6.00 |
| SHAFT_MINE | 2.00 | - | 0.80 |
| SILK_FARM | - | - | 2.00 |

*food per tile; who: all players; turn: save 285; rows counted: 1178; source: tiles.csv, worked tiles. Every value counted (17).*

| improvement | human_founded | human_captured | ai |
|---|---|---|---|
| - | 0.97 | 1.52 | 1.59 |
| MINE | 8.21 | 8.00 | 6.62 |
| FARM | 0.28 | 0.33 | 0.68 |
| FISHING_BOATS | 0.00 | 0.00 | 0.79 |
| CAMP | 1.67 | - | 2.01 |
| PASTURE | 2.67 | 2.00 | 3.05 |
| COTTAGE | - | - | 2.19 |
| HAMLET | 1.50 | 1.00 | 2.35 |
| QUARRY | 8.33 | - | 6.62 |
| WORKSHOP | 7.00 | - | 3.47 |
| PLANTATION | - | - | 1.23 |
| APPLE_FARM | - | - | 1.20 |
| OLIVE_FARM | 2.00 | - | 1.88 |
| VILLAGE | 2.00 | - | 5.00 |
| WINERY | 0.60 | - | 2.00 |
| SHAFT_MINE | 10.00 | - | 7.40 |
| SILK_FARM | - | - | 1.00 |

*hammers per tile; who: all players; turn: save 285; rows counted: 1178; source: tiles.csv, worked tiles. Every value counted (17).*

| improvement | human_founded | human_captured | ai |
|---|---|---|---|
| - | 0.97 | 0.70 | 0.98 |
| MINE | 0.66 | 2.40 | 0.59 |
| FARM | 1.00 | 1.00 | 0.84 |
| FISHING_BOATS | 1.57 | 1.50 | 2.52 |
| CAMP | 0.67 | - | 1.00 |
| PASTURE | 1.33 | 1.00 | 1.62 |
| COTTAGE | - | - | 0.97 |
| HAMLET | 2.17 | 2.50 | 2.00 |
| QUARRY | 0.67 | - | 0.94 |
| WORKSHOP | 1.00 | - | 1.27 |
| PLANTATION | - | - | 7.00 |
| APPLE_FARM | - | - | 2.00 |
| OLIVE_FARM | 8.00 | - | 6.25 |
| VILLAGE | 4.14 | - | 1.33 |
| WINERY | 7.60 | - | 7.00 |
| SHAFT_MINE | 1.00 | - | 1.00 |
| SILK_FARM | - | - | 6.50 |

*commerce per tile; who: all players; turn: save 285; rows counted: 1178; source: tiles.csv, worked tiles. Every value counted (17).*

**The cottage line.** The chain is COTTAGE > HAMLET > VILLAGE > TOWN. Turns of worked progress per step on
Marathon: cottage 30, hamlet 60, village
120. Progress grows only on a tile that is being worked
(`CvPlot::doImprovementUpgrade`).

**Upgrade rate.**
- The only record type that sets `iImprovementUpgradeRateModifier` is: CivicInfo.
- The human's civics at the save give a modifier of 20 %.
- `CvPlayer::getImprovementUpgradeRate` computes `1 × (100 + modifier) / 100` in integer
  arithmetic. The rate is 1: a modifier under `100` % changes nothing.
- AI players with cities whose rate is above one: 0 of 17.

## Readings

Each reading names the facts it rests on and what would refute it.

1. **Cottages are built where they will be worked.**
   - Facts: the impr table. No human city tile holds a cottage at the save. Every hamlet and
     village in the human's cities is worked. On the AI's side, most cottages are on unworked
     tiles, where they cannot grow.
   - Refuted if: the human's cottage orders went mostly to plots that no city worked
     afterwards. This is open, because the save dump has no plot coordinates
     (`toolkit.md`, section 5.2).
2. **Roman infantry are road builders.**
   - Facts: the builds table and the work rates. Legionaries, Hastati and Principes work
     faster than a Worker, and were given road and paved-road orders.
   - Refuted if: their build orders were not on routes.
3. **Most camp orders and over half the track orders went to Javelineers, not Workers** (builds table).
   - Refuted if: those orders were cancelled. Completions are not logged, so this is open.

## Open

- Which orders were completed. This needs plot coordinates in the save dump or an outcome
  line in the war log (`toolkit.md`, section 6).
- Roads before wars: not restated here. The earlier figure had no control for the human's
  own new cities.

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `builds` | table, 13 values | orders | human (player 3) | 49-285 | 276 | A lines MISSION_BUILD (human_commands.csv) |
| `builds_distinct` | table, 13 values | distinct plots | human (player 3) | 49-285 | 242 | A lines MISSION_BUILD, first order per plot and build |
| `route_to` | table, 1 values | orders | human (player 3) | 206-283 | 24 | A lines MISSION_ROUTE_TO |
| `automate` | table, 5 values | orders | human (player 3) | 0-276 | 18 | A lines COMMAND_AUTOMATE; type from CvEnums.h AutomateTypes |
| `build_pct` | 75 | xml | all | fixed |  | GameSpeedInfo MARATHON iBuildPercent (CvPlot::getBuildTime) |
| `workrate_WORKER` | 100 | xml | WORKER | fixed |  | UnitInfo UNIT_WORKER iWorkRate |
| `workrate_JAVELINEER` | 100 | xml | JAVELINEER | fixed |  | UnitInfo UNIT_JAVELINEER iWorkRate |
| `workrate_WORKBOAT` | 100 | xml | WORKBOAT | fixed |  | UnitInfo UNIT_WORKBOAT iWorkRate |
| `workrate_ROME_LEGIONARY` | 175 | xml | ROME_LEGIONARY | fixed |  | UnitInfo UNIT_ROME_LEGIONARY iWorkRate |
| `workrate_HASTATI` | 175 | xml | HASTATI | fixed |  | UnitInfo UNIT_HASTATI iWorkRate |
| `workrate_PRINCIPES` | 175 | xml | PRINCIPES | fixed |  | UnitInfo UNIT_PRINCIPES iWorkRate |
| `ai_workrate_mod` | 20 | xml | AI players | fixed |  | HandicapInfo MONARCH iAIWorkRateModifier, game handicap (CvUnit::workRate) |
| `impr` | table, 19 values | tiles at save | all players | save 285 | 2460 | tiles.csv (save dump) |
| `yield_food` | table, 17 values | food per tile | all players | save 285 | 1178 | tiles.csv, worked tiles |
| `yield_hammers` | table, 17 values | hammers per tile | all players | save 285 | 1178 | tiles.csv, worked tiles |
| `yield_commerce` | table, 17 values | commerce per tile | all players | save 285 | 1178 | tiles.csv, worked tiles |
| `cottage_chain` | COTTAGE > HAMLET > VILLAGE > TOWN | xml | all | fixed |  | ImprovementInfo ImprovementUpgrade |
| `upgrade_turns_COTTAGE` | 30 | derived xml | all | fixed |  | IMPROVEMENT_COTTAGE iUpgradeTime 10 x Marathon and Ancient iImprovementPercent (CvGame::getImprovementUpgradeTime); progress grows only while the tile is worked (CvPlot::doImprovementUpgrade) |
| `upgrade_turns_HAMLET` | 60 | derived xml | all | fixed |  | IMPROVEMENT_HAMLET iUpgradeTime 20 x Marathon and Ancient iImprovementPercent (CvGame::getImprovementUpgradeTime); progress grows only while the tile is worked (CvPlot::doImprovementUpgrade) |
| `upgrade_turns_VILLAGE` | 120 | derived xml | all | fixed |  | IMPROVEMENT_VILLAGE iUpgradeTime 40 x Marathon and Ancient iImprovementPercent (CvGame::getImprovementUpgradeTime); progress grows only while the tile is worked (CvPlot::doImprovementUpgrade) |
| `rate_setters` | CivicInfo | xml | all | fixed |  | records.json, every record type, iImprovementUpgradeRateModifier set |
| `rate_mod_human` | 20 | xml | human (player 3) | save 285 |  | civics in force (save dump) x CivicInfo iImprovementUpgradeRateModifier |
| `rate_human` | 1 | derived xml | human (player 3) | save 285 |  | CvPlayer::getImprovementUpgradeRate: 1 x (100 + modifier) / 100, integer division |
| `rate_ai_above1` | 0 | derived xml | AI players with cities | save 285 | 17 | same rule, AI civics in force |
| `n_ai` | 17 | xml | AI players with cities | save 285 |  | save dump |
