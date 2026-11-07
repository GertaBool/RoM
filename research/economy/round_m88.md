# Sanitation and markets, ceilings, caffeine, and the eating order (R42, M88)

## 1. Recorded (M88)

| Topic | Decided |
|---|---|
| Commercial Center (+8 health), Commodity Market (+5) | keep their health: modern logistics, just-in-time delivery, refrigeration, and food, nutraceuticals and medicines commoditized on the market |
| Essentials tiers | stages of settlement development with many functions; only the last tier, Metropolitan Essentials (municipal services), is sanitation |
| Water supply levels (wells, aqueduct, piped water) | add sanitation faces through the same tag |
| Appetite | set by what a person can physically eat: ceilings per food (so much cheese, so much meat), not a headroom |
| Food-weight limit | dropped; fruit counts as watermelon |
| Fat from one good | 100 g a day, accepted |
| Drinks | no total cap: people drink 3 L of water or more; only milk is capped at 3 L |
| Caffeine and infusion | from PubMed (section 4) |
| Eating order | the best goods first by nutrition, health and satiety up to their ceilings, then the rest: "steak and potatoes, then dessert" |

## 2. Sanitation faces, updated (`plan/tools/faces_check.py`)

**Sanitation (`bSanitation`):**
- fresh water (+2);
- Metropolitan Essentials (+12);
- Aqueduct (+5) and Pont du Gard (+6);
- Bath House (+3), Ottoman Hammam (+5), Khmer Baray (+5);
- Water Treatment Plant (+2);
- Recycling Center (+3);
- the D31 water supply levels (section 3).

Town and City Essentials, Commercial Center and Commodity Market stay in the general health balance.

| Case | People | Dense people | Faces today (size) | Density faces | Sanitation faces | Uncovered | U | Urban penalty per 1,000 | H (other faces) | Shown: good / bad |
|---|---|---|---|---|---|---|---|---|---|---|
| farming district, no works | 1,000,000 | 199,999 | 11 | 6 | 0 | 6 | 0.20 | 2.6 | 0.80 | 4 / 7 (unhealthy) |
| farming district, fresh water | 1,000,000 | 199,999 | 11 | 6 | 2 | 4 | 0.13 | 1.7 | 0.80 | 6 / 7 (unhealthy) |
| farming district, fresh water, Aqueduct | 1,000,000 | 199,999 | 11 | 6 | 7 | 0 | 0.00 | 0.0 | 0.83 | 11 / 7 |
| trade city, no works | 1,000,000 | 800,000 | 11 | 10 | 0 | 10 | 0.80 | 10.4 | 0.80 | 4 / 11 (unhealthy) |
| trade city, fresh water, Aqueduct | 1,000,000 | 800,000 | 11 | 10 | 7 | 3 | 0.24 | 3.1 | 0.80 | 11 / 11 |
| trade city, + Bath House | 1,000,000 | 800,000 | 11 | 10 | 10 | 0 | 0.00 | 0.0 | 0.80 | 14 / 11 |
| trade city, + Bath House, Water Treatment Plant | 1,000,000 | 800,000 | 11 | 10 | 12 | 0 | 0.00 | 0.0 | 0.86 | 16 / 11 |
| ancient town, 50,000, fresh water | 50,000 | 40,000 | 4 | 3 | 2 | 1 | 0.27 | 3.5 | 1.00 | 4 / 3 |
| city of 500,000, no works | 500,000 | 450,000 | 9 | 8 | 0 | 8 | 0.90 | 11.7 | 0.75 | 3 / 9 (unhealthy) |
| metropolis of 10 million, no works | 10,000,000 | 9,000,000 | 26 | 25 | 0 | 25 | 0.90 | 11.7 | 0.75 | 3 / 26 (unhealthy) |
| metropolis of 10 million, full works | 10,000,000 | 9,500,000 | 26 | 26 | 27 | 0 | 0.00 | 0.0 | 0.60 | 35 / 32 |

**What changed against `round_m87.md`:** without Town Essentials as sanitation, a farming district needs fresh water and an aqueduct to cover its six density faces. A trade city needs an aqueduct and baths for its ten.

## 3. Water supply levels as sanitation faces (D31)

**D31 (decided, M73):**
- the city's water supply in m³ a day, from fresh water, wells, aqueducts and treatment;
- domestic water by the WHO levels: 20, 50 and 100 L per head a day (Howard and Bartram 2003);
- effects through the engine's health.

**Proposal: the supply level covers density faces in proportion to the WHO level reached:**

```
L          = water supply per head a day (litres)
level      = 0 below 20 L; 0.25 at 20 L (basic); 0.5 at 50 L (intermediate); 1.0 at 100 L (optimal); straight lines between
F_water    = round(F_dense × level)        sanitation faces from the water supply
```

- **The buildings stay the source of supply.** Fresh water, wells, the Aqueduct and the Water Treatment Plant add m³ a day; their fixed health is then replaced by `F_water`, so the same water is not counted twice.
- **The faces follow the city.** A growing city outgrows its aqueduct: `L` falls, `F_water` falls, uncovered faces appear. The hover can say "water: 38 L per head; 50 L would cover 2 more faces".
- **The level values** (0.25, 0.5, 1.0 at the WHO thresholds) are my proposal for you to judge.

## 4. Caffeine and tea infusion (PubMed, with the Japanese tables for brewing)

| Measure | Value | Source |
|---|---|---|
| caffeine in tea leaves | white 16.79, green 16.28, oolong 19.31, black 17.73 mg/g (37 commercial teas) | Boros et al. 2016, PMID 27019564 |
| caffeine in a cup of tea | 14-61 mg per serving (6 or 8 oz) for white, green and black tea; none in herbal teas | Chin et al. 2008, PMID 19007524 |
| caffeine in a cup of tea, by brewing | 4-14 mg per 200 ml by type at standard brewing; up to 53 mg after 10 min; black tea 39 mg from cup bags, 24 mg loose | PMID 40647065 (2025) |
| caffeine in brewed coffee | 58-259 mg per dose; mean 188 mg for a 16-oz (473 ml) cup | McCusker et al. 2003, PMID 14607010 |
| energy effect of caffeine | +3-4 % resting rate for 100 mg; +150 kcal a day at 6 × 100 mg | Dulloo et al. 1989, PMID 2912010 |
| brewing per kg (Japanese food tables, remarks of the infusion records) | sencha 10 g in 430 ml, 20 mg caffeine per 100 g; black tea 5 g in 360 ml, 30 mg; coffee 10 g ground in 150 ml, 60 mg | MEXT, 8th edition, 2023 supplement |

**Per kg of the good:**

| Good | Litres of drink per kg | Caffeine per litre | Caffeine drunk per kg | Check |
|---|---|---|---|---|
| Tea (green, as sencha) | 43 | 200 mg | 8.6 g | about half the 16-19 g per kg in the leaf (Boros): the rest stays in the leaf at a 1-minute brew |
| Tea (black) | 72 | 300 mg | 21.6 g | above Boros's 17.7 g per kg mean; MEXT's leaf is stronger or its brew more complete |
| Coffee | 15 | 600 mg | 9 g | a 150 ml cup has 90 mg, within McCusker's 58-259 mg per dose |

- The model uses the sencha values for Tea and the coffee values for Coffee.
- The caffeine effect counts up to 600 mg a day, the dose Dulloo measured. More than 600 mg adds no energy effect in the model.

## 5. The food model with the eating order (`plan/tools/food_model.py`)

### 5a. Ceilings (what a person can physically eat)

| Ceiling | Value | Basis |
|---|---|---|
| energy, all foods | `E_max = BMR × 2.40` (+ caffeine) | FAO 2004: activity above 2.40 is hard to keep up |
| protein | 35 % of `E_max` | Bilsborough and Mann 2006 |
| fat from one good | 100 g a day | accepted (M88) |
| milk | 3 L a day | your figure |
| fruit, all together | 4,518 g a day: one whole watermelon (USDA portion, 15 × 7.5 in) | your rule: fruit as watermelon |
| salt | 10 g a day | estimate |
| water and other drinks | none | M88 |

### 5b. The eating order

**Quality of a good** = satiety × (1 + nutrient density).
- **Satiety:** Holt et al.'s measured index where the food was measured: potatoes 323, fish 225, oranges 202 (for lemons), apples 197, beef 176, white rice 138, bananas 118, white bread 100 for wheat. These are the values as Wikipedia's "Satiety value" table reproduces them (PMID 7498104). Other goods keep the protein-factor formula of the generator.
  - Holt's abstract gives the reason the formula alone fell short: water (r 0.64), fibre (0.46) and protein (0.37) raise satiety, and fat lowers it (−0.43). The formula carried only protein.
- **Nutrient density:** as in the Nutrient Rich Foods index (Drewnowski and Fulgoni 2011, PMID 21272703). Per 100 kcal, each of the 12 nutrients and protein is taken as a share of its daily need, capped at 1, and averaged.

*(M89, M90: fruit and drinks are taken for well-being before the satiety order, keeping their satiety and energy; see `round_m89.md`.)*

**Eating:**
1. Tea and coffee first, as much as there is, up to 600 mg caffeine.
2. Then each food good in order of quality, as much as there is, up to its own ceilings and the energy and protein room left.
3. What is not eaten stays in stock: storage and spoilage, trade, animal feed.

The best foods are eaten first up to their ceilings. Lesser foods fill what room remains: "steak and potatoes, then dessert".

**The order the formula gives:**

Eating order (quality = satiety factor x (1 + nutrient density per 100 kcal)):
| Rank | Good | Satiety (Holt where measured) | Quality |
|---|---|---|---|
| 1 | Potato | 3.23 (Holt) | 3.42 |
| 2 | Crab | 2.29 | 2.89 |
| 3 | Shrimp | 2.29 | 2.75 |
| 4 | Fish | 2.25 (Holt) | 2.67 |
| 5 | Deer | 2.11 | 2.57 |
| 6 | Horse | 2.18 | 2.55 |
| 7 | Clam | 1.97 | 2.50 |
| 8 | Whale | 1.98 | 2.43 |
| 9 | Lemon | 2.02 (Holt) | 2.34 |
| 10 | Apple | 1.97 (Holt) | 2.02 |
| 11 | Cow | 1.76 (Holt) | 1.89 |
| 12 | Rice | 1.38 (Holt) | 1.44 |
| 13 | Dairy | 1.27 | 1.39 |
| 14 | Sheep | 1.25 | 1.34 |
| 15 | Banana | 1.18 (Holt) | 1.23 |
| 16 | Pig | 1.12 | 1.23 |
| 17 | Olives | 0.91 | 1.05 |
| 18 | Wheat | 1.00 (Holt) | 1.05 |
| 19 | Corn | 0.95 | 0.99 |
| 20 | Alcohol | 0.92 | 0.94 |
| 21 | Wine | 0.89 | 0.90 |
| 22 | Sugar | 0.89 | 0.89 |

### 5c. Cities (constructed stocks to show the arithmetic)

#### A. Market town, 20,000; 70 % vigorous, 20 % active, 10 % sedentary
| Good (in eating order) | Stock t | Per head g/day | Eaten g/day | Stopped by | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|---|
| Apple | 1,500 | 205 | 205 | stock | 1,500 | 0 | 0 |
| Dairy | 4,000 | 548 | 548 | stock | 4,000 | 0 | 0 |
| Pig | 600 | 82 | 82 | stock | 600 | 0 | 0 |
| Wheat | 7,000 | 959 | 959 | stock | 7,000 | 0 | 0 |
| Alcohol | 3,000 | 411 | 411 | stock | 3,000 | 0 | 0 |
| Salt | 60 | 8 | 8 | stock | 60 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Drink ml (from goods) | From water supply ml | Caffeine mg | PAL actual | Work |
|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3685 | 3464 | 1.08 | 122 (14 %) | 1134 | 665 | 0 | 2.26 | 1.20 |

Coverage (1.00 = need met; iron after absorption 12 %):
| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.11 | 0.46 | 5.11 | 3.44 | 1.40 | 0.75 | 3.14 | 2.57 | 1.18 | 0.59 | 1.18 | 5.83 |

#### B. Coastal city, 200,000; 50 % vigorous, 30 % active, 20 % sedentary
| Good (in eating order) | Stock t | Per head g/day | Eaten g/day | Stopped by | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|---|
| Tea | 600 | 8 | 8 | stock | 600 | 0 | 0 |
| Fish | 35,000 | 479 | 479 | stock | 35,000 | 0 | 0 |
| Rice | 75,000 | 1027 | 1027 | stock | 75,000 | 0 | 0 |
| Banana | 15,000 | 205 | 205 | stock | 15,000 | 0 | 0 |
| Salt | 500 | 7 | 7 | stock | 500 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Drink ml (from goods) | From water supply ml | Caffeine mg | PAL actual | Work |
|---|---|---|---|---|---|---|---|---|---|
| 3025 | 3702 | 3306 | 1.09 | 112 (14 %) | 507 | 1292 | 70 | 2.15 | 1.20 |

Coverage (1.00 = need met; iron after absorption 14 %):
| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.49 | 0.11 | 7.71 | 5.54 | 1.24 | 1.09 | 2.21 | 2.62 | 0.24 | 11.19 | 1.52 | 4.95 |

#### C. Industrial city, 1,000,000; 40 % vigorous, 30 % active, 30 % sedentary
| Good (in eating order) | Stock t | Per head g/day | Eaten g/day | Stopped by | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|---|
| Coffee | 3,000 | 8 | 8 | stock | 3,000 | 0 | 0 |
| Potato | 600,000 | 1644 | 1644 | stock | 600,000 | 0 | 0 |
| Cow | 40,000 | 110 | 110 | stock | 40,000 | 0 | 0 |
| Dairy | 250,000 | 685 | 685 | stock | 250,000 | 0 | 0 |
| Wheat | 220,000 | 603 | 603 | stock | 220,000 | 0 | 0 |
| Sugar | 30,000 | 82 | 82 | stock | 30,000 | 0 | 0 |
| Salt | 3,000 | 8 | 8 | stock | 3,000 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Drink ml (from goods) | From water supply ml | Caffeine mg | PAL actual | Work |
|---|---|---|---|---|---|---|---|---|---|
| 2916 | 3703 | 3600 | 1.23 | 128 (14 %) | 808 | 991 | 73 | 2.34 | 1.20 |

Coverage (1.00 = need met; iron after absorption 13 %):
| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.37 | 0.55 | 5.12 | 3.87 | 1.56 | 1.50 | 3.08 | 2.60 | 1.43 | 0.84 | 2.65 | 6.07 |

#### E. Rich city, 100,000, everything in surplus; 20 % vigorous, 40 % active, 40 % sedentary
| Good (in eating order) | Stock t | Per head g/day | Eaten g/day | Stopped by | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|---|
| Potato | 60,000 | 1644 | 1644 | stock | 60,000 | 0 | 0 |
| Apple | 20,000 | 548 | 548 | stock | 20,000 | 0 | 0 |
| Cow | 20,000 | 548 | 548 | stock | 20,000 | 0 | 0 |
| Dairy | 150,000 | 4110 | 2457 | energy ceiling | 89,691 | 60,309 | 60,309 |
| Wheat | 40,000 | 1096 | 0 | energy ceiling | 0 | 40,000 | 2,000 |
| Wine | 15,000 | 411 | 0 | energy ceiling | 0 | 15,000 | 2,250 |
| Sugar | 8,000 | 219 | 0 | energy ceiling | 0 | 8,000 | 800 |
| Salt | 500 | 14 | 10 | salt | 365 | 135 | 14 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Drink ml (from goods) | From water supply ml | Caffeine mg | PAL actual | Work |
|---|---|---|---|---|---|---|---|---|---|
| 2711 | 3685 | 3685 | 1.36 | 209 (23 %) | 2926 | 0 | 0 | 2.40 | 1.20 |

Coverage (1.00 = need met; iron after absorption 17 %):
| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.65 | 2.01 | 4.36 | 3.24 | 1.37 | 6.42 | 2.93 | 3.64 | 3.92 | 2.73 | 3.29 | 8.88 |

#### F. Fishing village, 5,000, seafood only in plenty; 70 % vigorous
| Good (in eating order) | Stock t | Per head g/day | Eaten g/day | Stopped by | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|---|
| Crab | 2,000 | 1096 | 1096 | stock | 2,000 | 0 | 0 |
| Fish | 6,000 | 3288 | 2141 | protein ceiling | 3,908 | 2,092 | 2,092 |
| Salt | 15 | 8 | 8 | stock | 15 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Drink ml (from goods) | From water supply ml | Caffeine mg | PAL actual | Work |
|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3685 | 1885 | 0.59 | 322 (68 %) | 0 | 1800 | 0 | 1.40 | 0.00 |

Coverage (1.00 = need met; iron after absorption 18 %):
| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.60 | 0.49 | 3.21 | 5.23 | 2.53 | 29.53 | 3.05 | 5.21 | 1.76 | 49.96 | 3.56 | 12.59 |

#### D. Besieged town, 20,000, grain and salt pork only
| Good (in eating order) | Stock t | Per head g/day | Eaten g/day | Stopped by | Used t | Left t | Spoiled t |
|---|---|---|---|---|---|---|---|
| Pig | 400 | 55 | 55 | stock | 400 | 0 | 0 |
| Wheat | 3,000 | 411 | 411 | stock | 3,000 | 0 | 0 |
| Salt | 60 | 8 | 8 | stock | 60 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Drink ml (from goods) | From water supply ml | Caffeine mg | PAL actual | Work |
|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3685 | 1276 | 0.40 | 46 (14 %) | 0 | 1800 | 0 | 1.40 | 0.00 |

Coverage (1.00 = need met; iron after absorption 11 %):
| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 0.00 | 2.25 | 1.45 | 0.50 | 0.07 | 1.26 | 1.04 | 0.14 | 0.00 | 0.40 | 5.37 |

**What the cities show:**
- **The rich city (E)** eats potatoes, apples and beef first, then milk until the energy ceiling. Bread, wine and sugar stay in stock: there is no room left for dessert. Fresh leftovers spoil within the year.
- **The fishing village (F)** has fish in plenty but stops at the protein ceiling with 1,885 kcal against a need of 3,193. Seafood alone starves, as lean game does.
- **Where stocks are short (A, B, D)** everything is eaten and the order does not matter. Where they are ample (C, E), the order decides what is left over.
- **The water supply** makes up whatever drinks do not give of the 1.8 L.

## 6. What the markets' health stands for

The Commercial Center and Commodity Market keep their health (section 1).

**Proposal, following your reason (refrigeration, logistics):** they also lower the spoilage of fresh goods in their city, for example fresh by half and kept by a quarter. The values are estimates for you to judge. They would make the health they give visible in the goods: more fresh food reaches the table.

## 7. Open

- The water supply level values (section 3).
- The markets' spoilage effect (section 6).
- Holt values for the goods not measured (milk, pork, mutton, seafood other than fish, maize, sugar, wine, beer, olives); the formula stands in for them.
