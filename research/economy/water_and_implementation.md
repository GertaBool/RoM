# Water, hydration and how to build the food system (R26, M72)

This file proposes how to implement hydration and water supply, and how the rest of the food, drink and
population work fits into the plan.

- Part A holds the facts: what the mod has, read from its XML and the DLL, and sourced history.
- Part B holds the water proposals.
- Part C holds the order of implementation for everything.

Nothing here is decided. A new decision D31 is recorded as open in design.json.

## A. Facts

### A1. What the mod has (GitLab `claude/settlement-economy` at d2a8f756; DLL GitLab main)

**Fresh water:**
- **City health.** A city on fresh water gets `FRESH_WATER_HEALTH_CHANGE` = 1 good health
  (`CvCity::updateFreshWaterHealth`, `GlobalDefines.xml`).
- **Features.** Oasis and Swamp add fresh water (`bAddsFreshWater`). Swamp has -50 % health, Flood plains -20 %.
- **Terrain.** Grassland, plains, desert, tundra, snow and marsh have `bFoundFreshWater`.
- **Farms** are valid by fresh water or irrigation (`bFreshWaterMakesValid`, `bRequiresIrrigation`,
  `bCarriesIrrigation`).
- **The Groundwater Well improvement** carries irrigation and gives +2 food and +1 commerce on grassland, plains,
  desert and marsh. `IMPROVEMENT_WELL` is a resource well: production and commerce on its bonus.

**Water buildings:**

| Building | Tech | Health | Other fields |
|---|---|---:|---|
| Aqueduct | Waterworks | +5 | `bCenterInCity`; +15 % production with Timber; Expansive trait at double speed |
| Bath House | Waterworks | +3 | needs an Aqueduct in the city and Marble; +10 % great people; obsolete at Modern Sanitation |
| Water Treatment Plant | Modern Sanitation | +2 | needs Metropolitan Essentials in the city |
| Pont du Gard (wonder) | Waterworks | +6, +2 in the area | needs Stone and 4 cities; great engineer points |
| Great Dam (wonder) | Plastics | | needs a river; clean power for the area; Cement, Iron, Steel |

**Related buildings:**
- Hospital (Medicine): +10 health.
- Harbor: +1 health per Fish, Clam, Crab and Shrimp.
- Brewery (Fermentation): needs Apple, Wheat, Rice, Sugar or Corn; gives the Alcohol resource and a merchant.

### A2. History (sources named; web search 2026-11-06)

**How much water people need:**
- **Drinking:** EFSA (2010) sets 2.0 L total water a day for women and 2.5 L for men, about 20 % of it from food.
  WHO gives 7.5 L a day as the minimum for a lactating woman in heat, for drinking and food.
- **All domestic use** (Howard and Bartram 2003, WHO):

  | Level | How it is reached | Litres per head a day | What it covers |
  |---|---|---:|---|
  | Basic | a source 100-1,000 m away, 5-30 minutes | about 20 | drinking assured; hygiene hard |
  | Intermediate | one tap on the plot | about 50 | hygiene, laundry and bathing assured |
  | Optimal | several taps, continuous | 100 or more | all needs met |

- **Drinks hydrate differently** (Maughan et al. 2016): milk 1.50-1.58, water 1.00; tea, coffee and lager about the
  same as water.

**City water supply:**
- **Rome.** In 97 AD Frontinus counted 12,755 quinariae of supply and 14,018 of deliveries. Modern estimates range
  from 520,000-635,000 m³ a day to 1,000,000 or more. That is roughly 800-1,600 L per head, depending on the
  population assumed (1-1.5 million).
- **London.** The City took the Tyburn springs in 1237 and began the Great Conduit in 1245, a lead pipe into the city.
  Shallow wells had become inadequate and polluted as population grew. Water-carriers delivered from the conduits to
  households.
- **Water quality and disease:**
  - Snow (1854) traced the Broad Street cholera deaths (420-616 by source) to one pump.
  - Before the 20th century, cities were almost always deadlier than the countryside, and gastrointestinal disease was
    a large part of that.
  - In US cities 1900-1936, clean water (filtration and chlorination) accounts for about 43-50 % of the fall in total
    mortality, about three-quarters of the fall in infant mortality and nearly two-thirds of the fall in child
    mortality. Filtration cut typhoid deaths by 46 % (Cutler and Miller 2005, *Demography*).
  - Other studies find that the cholera geography of English towns did not follow industrial water deficits, and
    that sanitation alone does not fully explain falling mortality.

**Livestock water** (government planning figures, Canada and New Zealand):
- dairy cows in milk 70-150 L a day, dry 20-45 L;
- sheep 3-4 L, ewes in milk 12-20 L;
- horses 20-55 L.

## B. Proposals for water and hydration (decision D31)

### B1. Two water needs per person

| Need | Quantity | What meets it | What a shortfall does |
|---|---|---|---|
| **Drink** | 1.8 L a day (EFSA total less the share from food) | drinks × their hydration index; water for the rest | below the need: thirst, which raises mortality in the population model; below 7.5 L of water for drinking and food, the city cannot hold its people |
| **Domestic water** | the WHO levels: 20, 50, 100 L a day | the city's water supply | the level sets the health from water (B3) |

That is two numbers per person and one per drink, as M65 asked.

### B2. The city's water supply, in m³ a day

The city's supply `W` is the sum of its sources:

| Source | Supply | Basis |
|---|---|---|
| Fresh water at the city (river, lake, oasis) | enough for the basic level (20 L per head), any size | water within 1 km (WHO basic) |
| No fresh water | basic for the first *estimate* 5,000 people, from wells and cisterns; then the level falls | London: wells fail as population grows |
| Groundwater Well on a worked plot | *estimate* 500 m³ a day | |
| Aqueduct | *estimate* 50,000 m³ a day | Rome's 520,000-1,000,000 m³ from about eleven aqueducts |
| Pont du Gard | the Aqueduct's supply again, and +2 health in the area as now | |
| Modern supply (Water Treatment Plant) | *estimate* 100 L per head for the whole city | |

- **Access level** = `W` / people, read against the WHO table: below 20 L, 20-50, 50-100, 100 and more.
- **Integers (rule F):** `W` is held in m³ a day as an `int`. People × litres is computed in `__int64`, because 22.8
  million people × 100 L is above 2³¹.

### B3. Water and health: through the engine's health system

The mod's health system (iHealth, good and bad health, already valued by the AI) carries the effect, so there is no
new kind of effect:
- **Access level.** Below 20 L a head: bad health of *estimate* 1 per 10 % of people short of water. Basic level: 0.
  Intermediate: the Aqueduct's +5, earned by the water it brings rather than as a fixed bonus. Optimal: +2 more.
- **Quality.** A city's water quality falls with its urban people when the water comes from local wells (London) and
  rises when it comes from distant springs by aqueduct (Tyburn, Rome). Filtering and chlorination raise it
  (the Water Treatment Plant). Bad quality gives bad health in proportion to urban people; *estimate* 1 per 50,000.
- **Bath House:** uses water (*estimate* 5,000 m³ a day). It gives its health only while the supply covers it.

**In the population model:**
- Health enters as a death term: `N ← N + r·N·(K−N)/K − m·u·N`, where `u` is the city's excess bad health.
- `m` is calibrated (*estimate*) so that moving a city from bad to clean water removes about 43-50 % of its excess
  urban mortality (Cutler and Miller).

### B4. Drinks as goods

- **The goods:** Milk (from Dairy), Ale and beer (Brewery: grain to ale), Wine, Alcohol, Tea, Coffee and juice
  (Lemon, Apple).
- **What each counts for:** each has a hydration index (milk 1.5, the others 1.0) and its satiety (section 4 of
  `open_questions.md`).
- **The daily pass:** drinks the city has are drunk first, up to 1.8 L a head × their index; water covers the rest
  of the drink need.
- **Stored drinks:** the essentials buildings carry casks (SD.F1). Milk spoils within days unless made into cheese
  or butter, which is D27's keeping rule.

### B5. Water for livestock

- A herd's goods (Dairy, Wool, Leather, meat) need water on the plot: fresh water, a river or a Groundwater Well.
  This is the same rule as farms (`bFreshWaterMakesValid`).
- Without water a pasture keeps *estimate* half its head.
- A dairy cow in milk needs 70-150 L a day, so milk output at high yields needs water.

### B6. What changes in the files

| Where | Change |
|---|---|
| `CIV4BuildingInfos.xml` | new fields `iWaterSupply` (m³ a day), `iWaterUse`, `iWaterQualityChange` (percent) on the Aqueduct, Bath House, Water Treatment Plant, Pont du Gard and the essentials stages (wells, cisterns) |
| `CIV4ImprovementInfos.xml` | `iWaterSupply` on the Groundwater Well; `bLivestockWater` on plots by fresh water |
| Goods catalogue (the BonusInfo records) | `iHydrationPercent` (milk 150, ale 100), `iSatietyPerTonne`, `iProteinPerTonne` |
| `GlobalDefines.xml` | `WATER_DRINK_PER_HEAD_ML` 1800; `WATER_LEVEL_BASIC` 20, `_INTERMEDIATE` 50, `_OPTIMAL` 100 (L) |
| DLL `CvCity` | `m_iWaterSupply`, `m_iWaterQuality`, `updateWaterSupply()`, a water health source beside `updateFreshWaterHealth()`, saved behind a new uiFlag |
| DLL goods pass (GW.F5) | a water step after produce and before consume: drinks first, then water, then the access level and health |
| City screen | one line: supply, need, level and quality, in the sector overview (D26) |
| AI | nothing new in the first version: it already values health |

## C. How to build the rest (order and gates)

**C1. Values on the goods, generated from sources.**
- A table `research/economy/data/nutrition.json` holds per good: FAO kcal, protein and fat; DIAAS; the as-eaten
  factor (bread 1.12 t per t of wheat, carcass share × 0.8); and the hydration index.
- A script writes `iSatietyPerTonne`, `iProteinPerTonne` and `iHydrationPercent` into the XML, the way the scale
  values were written (PR.F6.T3). No value is typed by hand.

**C2. Order:**
1. **PR.F1 production** with the tile formula (`tile_output.md`), the yield tables and usable land
   (`open_questions.md` sections 1-2). It now has its tables.
2. **FG food,** redefined: food counts in satiety per tonne as eaten, all foods, animal foods included; drinks count
   per day. FG.F1's "staple food goods feed the city" becomes "food goods feed the city by satiety".
3. **The population model** (D30, once you decide it): a new feature under FG, with the AI translation layer
   (section 7 of `open_questions.md`).
4. **CN needs:** add **CN.F4 water and drinks** (this file, part B).
5. **SD spoilage by form** (section 5 of `open_questions.md`).
6. **The guilds, land, trade and AI components** as planned.

**C3. Gates:**
- Each step is registered as a prediction before its evidence (CLAUDE.md rule 10).
- Safety: 5 seeded runs per arm.
- The food and population steps also get a deterministic check against England about 1300: about 1,926 kcal from
  grain per head a day and 3 ha per farm worker. This follows rule 9: computed, not simulated.

**C4. Plan entries proposed, not yet added:**
- FG.F4: the population model.
- CN.F4: water and drinks.
- PR.F7: usable land and the tile formula refresh.

They are added once you confirm D30 and D31.
