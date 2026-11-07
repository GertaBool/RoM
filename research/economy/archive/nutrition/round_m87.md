# The faces in detail, and one food model on the game's goods (R41, M87)

## Part 1. The faces

### 1.1 What the game does today (economy branch d2a8f756)

- **Healthy faces** (`CvCity::goodHealth`): fresh water, good features (forests), power, health resources, good buildings (area and player-wide included), civics and civilization, handicap.
- **Unhealthy faces** (`CvCity::badHealth`): **one per size** (`unhealthyPopulation`, unless a building sets `bNoUnhealthyPopulation`), bad features (flood plains, jungle), power plants, bad resources, polluting buildings, espionage, extra building bad health.
- **Shown** on the city screen, in the hover by source, on the city bar, as the diseased smoke, in alerts and advisors (`round_m85.md` section 5, `round_m86.md` section 1).
- **Buildings with health** (`iHealth` in `CIV4BuildingInfos.xml`, 74 records with health effects):
  - **positive:** Metropolitan Essentials 12, Hospital 10, Commercial Center 8, City Essentials 6, Pont du Gard 6 (+2 area), Aqueduct 5, Ottoman Hammam 5, Khmer Baray 5, Research Hospital 5, Commodity Market 5, Bath House 3, Recycling Center 3, Town Essentials 3, Water Treatment Plant 2, Pharmacy 1, Cannery 1, and others;
  - **negative:** Forge, Iron Forge and Mali Mint −6, Commercial Airport and Brothel −3, Steel Mill, Coal Plant, Factory and other industry −1 to −2;
  - **`bNoUnhealthyPopulation`:** National Park, Body Exchange Clinic.
  - The Essentials are the settlement tiers: Town Essentials "Communal Organization", City Essentials "Civil Schema", Metropolitan Essentials "Municipal Services".

### 1.2 Proposal 1: density faces instead of size faces

**Rule:**
```
D        = people not working plots (the city's sector workers and their households)
F_dense  = size_of(D)        the same inverse curve as city size; 0 below 1,000 people
```
`unhealthyPopulation` returns `F_dense` instead of the size.

**Why this curve:**
- The faces stay in the range players know from today. A city whose people all live densely shows as many faces as its size.
- The count rises slowly with people, so faces stay readable at 10 million (25-26 faces against 26 today).
- A farming district shows fewer faces than a trade city of the same people. That is what you described: faces show missing infrastructure where people live densely.

**Edge cases:**
- **Fewer than 1,000 dense people:** no density faces.
- **`bNoUnhealthyPopulation`** (National Park, Body Exchange Clinic): sets density faces to 0, as today for size faces.
- **Timing:** `D` is taken from last turn's workforce, as the goods pass already takes last turn's flows (GW.F5).
- **Angry citizens:** `badHealth(bNoAngry)` subtracts angry citizens today. With density faces, the angry share is taken off `D` before the curve.

### 1.3 Proposal 2: the unsanitized share from uncovered density faces

**Sanitation faces:** a building's health counts as sanitation when its record says so. A new field, for example `bSanitation` on `BuildingInfo`, is set in XML. Fresh water counts as sanitation.

**Proposed list:**

| Sanitation (`bSanitation`) | Health | Why |
|---|---|---|
| fresh water (river or lake) | +2 | water supply (D31) |
| Town Essentials, City Essentials, Metropolitan Essentials | +3, +6, +12 | the settlement tiers: communal organization, civil schema, municipal services |
| Aqueduct, Pont du Gard | +5, +6 | water supply |
| Bath House, Ottoman Hammam, Khmer Baray | +3, +5, +5 | baths and reservoirs |
| Water Treatment Plant | +2 | clean water |
| Recycling Center | +3 | waste |

**Not sanitation; these stay in the general balance:** Hospital, Research Hospital, Pharmacy and Medical Center (medicine), resources, forests, wonders such as the Hanging Gardens. Commercial Center (+8) and Commodity Market (+5) carry health in the XML without a stated reason. I left them general and ask you below.

**Rule:**
```
F_san     = sum of sanitation faces
uncovered = max(0, F_dense − F_san)
U         = (D / N) × uncovered / F_dense          (0 when F_dense = 0)
urban penalty = 13 × U per 1,000 a year            (pop_model_math.md section 3)
spill     = max(0, F_san − F_dense)                sanitation beyond the density joins the healthy faces
H         = (other good + spill) / (other good + spill + other bad)     the base burden's health level
```

**Shown as today:** good = all healthy faces; bad = density faces + other unhealthy faces. The city is unhealthy (symbol, smoke, alert, no We Love the King Day) when bad > good.

### 1.4 Worked cases (`plan/tools/faces_check.py`)

| Case | People | Dense people | Faces today (size) | Density faces | Sanitation faces | Uncovered | U | Urban penalty per 1,000 | H (other faces) | Shown: good / bad |
|---|---|---|---|---|---|---|---|---|---|---|
| farming district, no works | 1,000,000 | 199,999 | 11 | 6 | 0 | 6 | 0.20 | 2.6 | 0.80 | 4 / 7 (unhealthy) |
| farming district, fresh water, Town Essentials | 1,000,000 | 199,999 | 11 | 6 | 5 | 1 | 0.03 | 0.4 | 0.80 | 9 / 7 |
| trade city, no works | 1,000,000 | 800,000 | 11 | 10 | 0 | 10 | 0.80 | 10.4 | 0.80 | 4 / 11 (unhealthy) |
| trade city, fresh water, Aqueduct | 1,000,000 | 800,000 | 11 | 10 | 7 | 3 | 0.24 | 3.1 | 0.80 | 11 / 11 |
| trade city, + City Essentials, Bath House | 1,000,000 | 800,000 | 11 | 10 | 16 | 0 | 0.00 | 0.0 | 0.91 | 20 / 11 |
| ancient town, 50,000, fresh water | 50,000 | 40,000 | 4 | 3 | 2 | 1 | 0.27 | 3.5 | 1.00 | 4 / 3 |
| city of 500,000, no works | 500,000 | 450,000 | 9 | 8 | 0 | 8 | 0.90 | 11.7 | 0.75 | 3 / 9 (unhealthy) |
| metropolis of 10 million, no works | 10,000,000 | 9,000,000 | 26 | 25 | 0 | 25 | 0.90 | 11.7 | 0.75 | 3 / 26 (unhealthy) |
| metropolis of 10 million, full works | 10,000,000 | 9,500,000 | 26 | 26 | 27 | 0 | 0.00 | 0.0 | 0.60 | 35 / 32 |

In each case the other healthy and unhealthy faces (resources, forests, pollution) are set as inputs to show the arithmetic.

**What the cases show:**
- **A farming district and a trade city of the same million differ:** 6 against 10 density faces. The farming district is covered by fresh water and Town Essentials; the trade city needs an aqueduct, baths and the next settlement tier.
- **Your rule holds:** without works, 500,000 and 10 million in the same urban share carry the same penalty (U 0.90, 11.7 per 1,000). Only the number of faces differs.
- **Each sanitation building closes faces one for one,** so the hover can say exactly what is missing ("3 uncovered: an aqueduct would cover them").
- **A fully built metropolis** shows healthy (35 against 32) and carries no urban penalty. Its industry (other bad faces) still weighs on `H`.

### 1.5 Hover lines (`CvGameTextMgr::setBadHealthHelp`, `setGoodHealthHelp`)

Example for the trade city with fresh water and an aqueduct:

```
Sanitation: 10 [unhealthy] from 800,000 dense people; 7 [healthy] from fresh water (2) and Aqueduct (5)
            3 uncovered: 24 % of the people live unsanitized (+3.1 per 1,000 a year)
Water:      supply and quality (D31)
Nutrition:  short of vitamin C (49 %), vitamin A (11 %), calcium (24 %)
War:        none
Health burden: 30.4 per 1,000 a year; growth +2.1 per 1,000
```

### 1.6 The AI

- The AI values buildings by the health they add against its deficit (`CvCity::getAdditionalHealthByBuilding`, `CvCityAI::AI_buildingValueThreshold`). With density faces in `badHealth`, a trade city's AI values the aqueduct more than a farming district's does, without new code.
- One new valuation term: a sanitation building is worth the burden it removes, `13 × ΔU`, converted to people saved per turn. This goes into `AI_buildingValue` with the other health terms.

### 1.7 Questions

1. The sanitation list: do the three Essentials stand for municipal sanitation, and should the Commercial Center (+8) and Commodity Market (+5) keep their health?
2. Should the water supply levels of D31 (wells, aqueduct, piped water) add sanitation faces through the same field?

## Part 2. One food model on the game's goods

### 2.1 Where it runs

- **The goods pass** (`CvPlayer::doGoods`, GW.F5): produce, recipes, distribute, **consume**, store and spoil. Each city keeps a stock of each good in tonnes.
- **This model fills `consumeGoods`** for food and drink.
- **Timing:** it runs once per yearly step of the turn (`round_m84.md` section 6). Each step uses the year's share of the turn's goods.

### 2.2 The data each food good carries (`CIV4BonusInfos.xml`, written by the generator from the research files)

| Field | Meaning | Source | Status |
|---|---|---|---|
| `iKcalPerTonne` | energy per tonne as stored × edible share | nutrition.json (FAO) | to add |
| `iSatietyPerTonne` | satiety units per tonne (kcal × protein factor, fitted to Holt 1995) | nutrition.json | generator written |
| `iProteinPerTonne` | kg protein per tonne × edible | nutrition.json | generator written |
| `iFatPerTonne` | kg fat per tonne × edible | nutrition.json | to add |
| `iEdiblePercent` | share eaten (extraction, bones, peel) | nutrition.json | to add (now inside the per-tonne values) |
| `NutrientValues` | 12 nutrients per tonne eaten (vitamins C, A, B1, B3, folate, B12; iron, zinc, calcium, iodine, potassium, sodium) | nutrient_profiles.json (USDA, MEXT) | to add |
| `iWaterPercent` | water share (fruit counts toward drink) | nutrient_profiles.json | to add |
| `iHydrationPercent` | drinks: hydration index × 100 | nutrition.json | generator written |
| `iMaxGramsPerDay` | the body's ceiling for this good, where one exists (milk 3,000) | M86 | to add |
| `iCaffeinePerKg` | tea and coffee | to source | to add |
| keeping form | spoilage per year by form | nutrition.json (FAO storage) | in use |

### 2.3 The model, step by step

For a city with `N` people and stocks `S_g` (tonnes this year), per person and day:

```
(1)  a_g      = S_g × 10^6 / (N × 365)                          grams available, as stored
(2)  BMR      = mean of FAO 2004 men (68.1 kg) and women (58.5 kg) = 1,536 kcal
(3)  PAL_work = Σ_k share_k × PAL_k                               sedentary 1.53, active 1.76, vigorous 2.25
(4)  c_caf    = min(1, caffeine available ÷ 600 mg)
(5)  E_need   = BMR × PAL_work + 150 × c_caf
(6)  E_max    = BMR × 2.40 + 150 × c_caf
(7)  A        = E_need × (1 + h)                                  appetite, in satiety units (bread-kcal)
(8)  q_g      = min(t × a_g, cap_g)                               eaten grams; one factor t for all goods
     cap_g    = min(a_g, 100 g fat ÷ fat per g, iMaxGramsPerDay)
     t        = the largest value in [0, 1] with:
                Σ q_g × satiety_g ≤ A            appetite
                Σ q_g × kcal_g ≤ E_max           energy
                4 × Σ q_g × protein_g ≤ 0.35 × E_max     protein
                Σ (food, not drink) q_g × edible_g ≤ 6,000 g     food mass (fruit as watermelon)
                Σ drinks ≤ 3,500 ml              drink
(9)  E_in     = Σ q_g × kcal_g                    x = E_in ÷ E_need      (the population model's food sufficiency)
(10) I_i      = Σ q_g × edible_g × n_{g,i}        nutrient intake; iron × absorption a_Fe ÷ 0.16
     a_Fe     = 0.10 + 0.08 × animal share of protein
(11) c_i      = I_i ÷ need_i;  store_i updated by (c_i − 1) up to its group's limit (round_m85.md section 4)
(12) drink    = Σ drinks × hydration + fruit water;  short of 1,800 ml → from the water supply (D31)
(13) PAL_act  = clamp(E_in ÷ BMR, 1.40, 2.40);  work = clamp((PAL_act − 1.40) ÷ (PAL_work − 1.40), 0, 1.20)
(14) used_g   = q_g × N × 365 ÷ 10^6 tonnes;  left_g = S_g − used_g;  spoiled_g = left_g × spoilage(form)
```

**What each output feeds:**

| Output | Feeds |
|---|---|
| `x` | fertility `B(x)` and the burden (weakness, famine) in the population model |
| `c_i`, stores | the deficiency burden, the nutrients factor of fertility, output (iodine → science and culture; iron → work) |
| protein | unit strength (D27) |
| `work` | the output of physical work (plots, mines, industry) |
| drink | the water need (D31), the city's water supply |
| `used`, `left`, `spoiled` | the stock, storage and trade (SD), the food line of the city screen |
| everything | the hover: energy against need, appetite, the binding limit, each short nutrient |

### 2.4 Worked cities (`plan/tools/food_model.py`)

The stocks are constructed inputs to show the arithmetic, not records of a game. Goods are the branch's food goods with their nutrition.json values.

**A. Market town, 20,000; 70 % vigorous, 20 % active, 10 % sedentary**

| Good | Stock t | Per head g/day | Eaten g/day | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|
| Wheat | 7,000 | 959 | 959 | 7,000 | 0 | 0 |
| Dairy | 4,000 | 548 | 548 | 4,000 | 0 | 0 |
| Pig | 600 | 82 | 82 | 600 | 0 | 0 |
| Apple | 1,500 | 205 | 205 | 1,500 | 0 | 0 |
| Alcohol | 3,000 | 411 | 411 | 3,000 | 0 | 0 |
| Salt | 60 | 8 | 8 | 60 | 0 | 0 |

| Need kcal | Appetite | Eaten kcal | Satiety eaten | x | Protein g (share) | Food mass g | Drink ml | Caffeine | PAL actual | Work | Binding |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3672 | 3464 | 3560 | 1.08 | 122 (14 %) | 1054 | 1134 | 0.00 | 2.26 | 1.20 | none: all eaten |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.11 | 0.46 | 5.11 | 3.44 | 1.40 | 0.75 | 3.14 | 2.57 | 1.18 | 0.59 | 1.18 | 5.83 |

**B. Coastal city, 200,000; 50 % vigorous, 30 % active, 20 % sedentary**

| Good | Stock t | Per head g/day | Eaten g/day | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|
| Rice | 75,000 | 1027 | 1027 | 75,000 | 0 | 0 |
| Fish | 35,000 | 479 | 479 | 35,000 | 0 | 0 |
| Tea | 600 | 8 | 8 | 600 | 0 | 0 |
| Banana | 15,000 | 205 | 205 | 15,000 | 0 | 0 |
| Salt | 500 | 7 | 7 | 500 | 0 | 0 |

| Need kcal | Appetite | Eaten kcal | Satiety eaten | x | Protein g (share) | Food mass g | Drink ml | Caffeine | PAL actual | Work | Binding |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3059 | 3518 | 3306 | 3490 | 1.08 | 112 (14 %) | 1712 | 507 | 0.34 | 2.15 | 1.20 | none: all eaten |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.49 | 0.11 | 7.71 | 5.54 | 1.24 | 1.09 | 2.21 | 2.62 | 0.24 | 11.19 | 1.52 | 4.95 |

**C. Industrial city, 1,000,000; 40 % vigorous, 30 % active, 30 % sedentary**

| Good | Stock t | Per head g/day | Eaten g/day | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|
| Wheat | 220,000 | 603 | 539 | 196,607 | 23,393 | 1,170 |
| Potato | 600,000 | 1644 | 1469 | 536,200 | 63,800 | 31,900 |
| Sugar | 30,000 | 82 | 73 | 26,810 | 3,190 | 319 |
| Dairy | 250,000 | 685 | 612 | 223,417 | 26,583 | 26,583 |
| Cow | 40,000 | 110 | 98 | 35,747 | 4,253 | 4,253 |
| Coffee | 3,000 | 8 | 7 | 2,681 | 319 | 32 |
| Salt | 3,000 | 8 | 7 | 2,681 | 319 | 32 |

| Need kcal | Appetite | Eaten kcal | Satiety eaten | x | Protein g (share) | Food mass g | Drink ml | Caffeine | PAL actual | Work | Binding |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2922 | 3360 | 3217 | 3360 | 1.10 | 114 (14 %) | 2071 | 619 | 0.16 | 2.10 | 1.20 | appetite |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.12 | 0.49 | 4.57 | 3.46 | 1.40 | 1.34 | 2.75 | 2.32 | 1.28 | 0.75 | 2.37 | 5.43 |

**D. Besieged town, 20,000, grain and salt pork only**

| Good | Stock t | Per head g/day | Eaten g/day | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|
| Wheat | 3,000 | 411 | 411 | 3,000 | 0 | 0 |
| Pig | 400 | 55 | 55 | 400 | 0 | 0 |
| Salt | 60 | 8 | 8 | 60 | 0 | 0 |

| Need kcal | Appetite | Eaten kcal | Satiety eaten | x | Protein g (share) | Food mass g | Drink ml | Caffeine | PAL actual | Work | Binding |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3672 | 1276 | 1299 | 0.40 | 46 (14 %) | 383 | 0 | 0.00 | 1.40 | 0.00 | none: all eaten |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 0.00 | 2.25 | 1.45 | 0.50 | 0.07 | 1.26 | 1.04 | 0.14 | 0.00 | 0.40 | 5.37 |

**What the cities show:**
- **The same calculation runs on every city:** stocks in tonnes → grams a head → eaten → energy, satiety, protein, nutrients and drink → `x`, coverage, work → tonnes used, left and spoiled.
- **The market town** is fed (x 1.08) and works at the vigorous level. It is short of vitamin C (0.11; few apples), vitamin A and iodine (inland, milk gives some). Beer and milk give 1.1 L of its 1.8 L drink; the rest comes from the water supply.
- **The coastal city** gets iodine from fish (11 times the need) and caffeine and vitamin C from tea. It is short of calcium and vitamin A: no dairy, no liver, no vegetables.
- **The industrial city** has more than it eats. Appetite binds, so the surplus stays in stock. Fresh dairy and meat left over spoil within the year (100 %); grain and sugar keep. Potatoes cover vitamin C twice.
- **The besieged town** has 40 % of its energy need, no vitamin C, A or iodine, and works at the minimum. The population model then applies famine, weakness and deficiency.

### 2.5 Parameters

| Parameter | Value | Basis |
|---|---|---|
| BMR | 1,536 kcal | FAO/WHO/UNU 2004 equations, EFSA weights |
| PAL by kind of work | 1.53, 1.76, 2.25 | FAO 2004 Table 5.1 |
| PAL range | 1.40-2.40 | FAO 2004 Table 5.3 |
| caffeine | up to 150 kcal at 600 mg a day | Dulloo 1989 |
| appetite headroom `h` | 0.15 | estimate; option B, not yet decided |
| protein | ≤ 35 % of `E_max` | Bilsborough and Mann 2006 |
| fat from one good | 100 g a day | estimate from your milk and beef examples |
| milk | 3 L a day | your estimate |
| food mass | 6 kg a day | estimate: a whole watermelon |
| drinks | 3.5 L a day | estimate |
| salt eaten | ≤ 10 g a day | estimate |
| drink need | 1.8 L | FD.drink (M71) |
| iron absorption | 10-18 % by animal protein share | FAO 2004 (line between, estimate) |
| caffeine in leaf and bean; tea infusion per kg | 25 g, 12 g; 43 L | estimates to source or verify |

### 2.6 In the DLL

- **All in integers:** grams per day in `int`, tonnes and people in `__int64`, satiety and kcal per tonne from the XML.
- **`t` by bisection** in per mille, ten steps.
- **Nutrients** in micrograms per day as integers; coverage in per mille.
- **One function per city** in `consumeGoods`, called once per yearly step; the city stores the year's outputs (`x`, coverage, work, drink) for the population model, the display and the AI.

## Open

- **Faces:** the sanitation list and its field; D31 water levels as sanitation faces.
- **Food:** appetite option and headroom; caffeine per kg; the tea infusion yield; lactose tolerance by population; preferences among goods (today all are eaten in proportion to what is there).
