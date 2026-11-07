# Hydration, one allocation, satiety, well-being and whole fish (R44, M91)

## 1. Recorded (M91)

| Topic | Decided or corrected |
|---|---|
| Drinks | milk's 3 L is only milk's ceiling; it is one part of one equation for a person's water (section 2) |
| Fruit and drinks | they matter for different reasons, not with a priority tier; the tier of `round_m89.md` is withdrawn (section 4) |
| Rich city | surplus milk partly into dairy products; bread eaten to some extent; sugar eaten as today or in 1900s Britain, adding to well-being (sections 4, 9) |
| Fish | the whole animal as eaten historically: fat, liver, roe; not lean fillet (section 7) |
| Water supply faces | accepted (WHO levels), and part of the general health equation too (section 10) |
| Markets and spoilage | accepted: fresh spoilage halved, kept spoilage cut by a quarter |
| Well-being | which food goods feed the happiness line: a ranking by lightness, reward and health (section 6) |
| Satiety without a Holt value | other references; a formula is fine if it is correct (section 5) |

## 2. Hydration: one equation

I wrote "no overall cap; only milk stops at 3 L". That mixed a good's ceiling with a person's water. The water a person takes in each day is:

```
water in  = water in food eaten  +  Σ drinks × hydration index  +  plain water
need      = 2.25 L a day (EFSA 2010: total water 2.5 L for men, 2.0 L for women, food water included)
plain water = max(0, need − water in food − drinks)        drawn from the city's water supply (D31)
```

- **Milk** counts with its hydration index (1.5) up to its own 3 L ceiling.
- **Tea and coffee** count as infusion (MEXT recipes).
- **Beer and wine** count by volume.
- **Fruit and cooked foods** bring their water (USDA water content).
- **Plain water** fills the rest and is limited only by the city's supply. People drink 3 L or more when they need it; heat and labour raise the need. That rise is still to be sourced.

**In the cities** (section 8):
- the market town takes 314 ml from food, 1,219 ml from beer and milk, and 716 ml of plain water;
- the besieged town takes almost all of its 2.25 L as plain water.

## 3. What "food weight dropped, fruit as watermelon" meant

- **In `round_m87.md` I had a limit of 6 kg of food a day,** all foods together, to stand for the stomach. You said this overcomplicates it, and I dropped it.
- **"Fruit as watermelon"** meant only that fruit has its own ceiling: as much fruit in all as one whole watermelon a day. That is 4,518 g, the USDA weight of a whole melon of 15 × 7.5 inches.
- No other food has a weight limit. Meat and cheese stop at 100 g fat, milk at 3 L, and everything at the energy and protein ceilings.

## 4. One allocation, no tiers

The tier of `round_m89.md` (well-being goods first) is withdrawn. Every good carries three values per kcal: satiety, nutrition and well-being. They are eaten together, with diminishing returns:

```
value_g     = satiety_g + nutrition_g + well-being_g                 (per kcal)
marginal_g  = value_g ÷ (1 + eaten_g ÷ serving_g)                    each further serving is worth less
eat         = step by step (10 kcal), always the good with the highest marginal value,
              within the ceilings (energy, protein, fat per good, milk, fruit), until the energy ceiling
```

**Why this fits your description:**
- **"Steak and potatoes, then dessert":** the first serving of the best goods comes first. Each further serving of the same good is worth less, so bread, sugar and wine come in after the first servings of meat and potatoes, not after they run out.
- **A rich city eats some bread and some sugar,** because their first servings beat a fourth serving of beef.
- **Fruit and drinks enter for their own reasons:** well-being, nutrients, water. They have no priority over food.

**Servings** are the USDA household portions:
- 2 slices of bread (64 g);
- 1 cup of cooked rice (158 g) or porridge (234 g);
- 1 large potato (300 g);
- 3 oz of meat or fish (85 g);
- 1 cup of milk (244 g);
- 1 apple (242 g), 1 banana (126 g), 1 lemon (58 g);
- 1 teaspoon of sugar (4.2 g);
- 5 fl oz of wine (147 g), 1 can of beer (356 g).

## 5. Satiety: a formula fitted to Holt, and where it stands (`plan/tools/satiety_fit.py`)

**The old formula** carried only protein. Holt's abstract (PMID 7498104) shows what drives satiety:
- serving weight (r 0.66);
- water (0.64);
- fibre (0.46);
- protein (0.37);
- fat lowers it (−0.43).

**The new formula** is fitted by least squares on 29 of Holt's 38 foods, with USDA composition of the food as eaten:

fit on 29 Holt foods: ln(SI/100) = 0.080 + 0.222 ln(W/W_bread) + 0.661 protein share + 0.031 fibre/100 kcal + -0.213 fat share; R2 = 0.46
| Holt food | SI measured | SI fitted | Leave-one-out | g per 240 kcal |
|---|---|---|---|---|
| white bread | 100 | 119 | 121 | 90 |
| potatoes (boiled) | 323 | 156 | 145 | 279 |
| fish (as cooked cod) | 225 | 233 | 248 | 229 |
| beef steak | 176 | 155 | 148 | 117 |
| eggs (poached) | 150 | 138 | 134 | 168 |
| cheese (cheddar) | 146 | 98 | 89 | 60 |
| white rice | 138 | 135 | 134 | 185 |
| brown rice | 132 | 140 | 140 | 195 |
| white pasta | 119 | 137 | 139 | 152 |
| oranges | 202 | 195 | 193 | 511 |
| apples | 197 | 181 | 176 | 462 |
| bananas | 118 | 155 | 159 | 270 |
| grapes | 162 | 156 | 154 | 348 |
| popcorn | 154 | 119 | 110 | 62 |
| peanuts | 84 | 90 | 92 | 41 |
| jellybeans | 118 | 100 | 94 | 64 |
| ice cream | 96 | 109 | 111 | 116 |
| yogurt (low fat fruit) | 88 | 147 | 160 | 242 |
| croissant | 47 | 96 | 102 | 59 |
| cake | 65 | 98 | 102 | 68 |
| doughnuts | 68 | 93 | 96 | 57 |
| cookies | 120 | 89 | 86 | 49 |
| crackers | 127 | 89 | 86 | 47 |
| potato chips | 91 | 86 | 86 | 45 |
| lentils | 133 | 196 | 262 | 207 |
| baked beans | 168 | 177 | 178 | 255 |
| porridge | 209 | 165 | 159 | 338 |
| wholemeal bread | 157 | 131 | 128 | 95 |
| grain bread (rye) | 154 | 124 | 122 | 93 |
median leave-one-out error: 22 %

| Game good | Eaten form (USDA) | SI fitted | Holt measured |
|---|---|---|---|
| Wheat | whole-wheat bread | 131 | 157 |
| Rice | white rice, cooked | 135 | 138 |
| Corn | porridge stands in for maize porridge (oats) | 165 | - |
| Potato | boiled potatoes | 156 | 323 |
| Cow | beef steak, broiled | 155 | 176 |
| Pig | pork loin, raw | 133 | - |
| Sheep | lamb, raw | 115 | - |
| Deer | deer, raw | 206 | - |
| Horse | horse, raw | 181 | - |
| Fish | herring, raw | 147 | - |
| Clam | clam, raw | 214 | - |
| Crab | crab, raw | 235 | - |
| Shrimp | shrimp, raw | 235 | - |
| Whale | beluga meat, raw | 245 | - |
| Dairy | whole milk | 155 | - |
| Banana | banana | 155 | 118 |
| Lemon | lemon | 258 | - |
| Apple | apple | 181 | 197 |
| Olives | ripe olives | 116 | - |
| Sugar | sugar | 100 | - |
| Wine | red wine | 140 | - |
| Alcohol | beer | 167 | - |
| Cheese | cheddar | 98 | 146 |
| Butter | butter | 70 | - |


**How good it is:**
- It explains about half the spread (R² 0.46). The median out-of-sample error is 22 %.
- **It underrates:** boiled potatoes (156 against 323), cheese, popcorn, cookies and crackers.
- **It overrates:** croissants, cake, doughnuts, yogurt and lentils.

**Use:**
- Holt's measured value wherever the food was measured.
- The formula for the rest: pork, mutton, game, seafood, milk, maize, olives, sugar, wine, beer.
- **Drinks are halved** (an estimate): liquid energy satiates less (Almiron-Roig et al. 2003, "Liquid calories and the failure of satiety", PMID 14649371). Holt measured no drinks.
- Other measured references for milk, pork and seafood are still to find. The formula is the stand-in until then.

## 6. Well-being: which goods feed it, and a ranking

**What the sources say:**
- **Reward:**
  - fat and carbohydrate together are rewarded more than either alone (DiFeliceantonio et al. 2018, PMID 29909968);
  - a fat-and-sugar milkshake released striatal dopamine in people (PMID 37375579);
  - alcohol releases striatal dopamine at low doses (meta-analysis, PMID 39729041);
  - caffeine raises energy and effortful behaviour (PMID 20164571).
- **Lightness:** a high-fat meal left people sleepier and more tired two to three hours later than a high-carbohydrate meal (Wells et al. 1997, PMID 9145937). Holt found palatability lowers satiety (r −0.64).

**The score** (per kcal; the weights are estimates for you to judge):

```
well-being = sugar share of energy + 2 × fat share × carbohydrate share + alcohol share of energy
             + lightness (water per kcal, up to 3 g per kcal) − 0.5 × fat share
```

**The three values per good, and the total that orders eating:**

| Good | Satiety | Nutrition | Well-being | Value per kcal | Serving g |
|---|---|---|---|---|---|
| Lemon | 2.02 | 0.16 | 1.78 | 3.96 | 58 |
| Potato | 3.23 | 0.06 | 0.37 | 3.66 | 300 |
| Apple | 1.97 | 0.02 | 1.49 | 3.49 | 242 |
| Shrimp | 2.35 | 0.20 | 0.36 | 2.92 | 85 |
| Crab | 2.35 | 0.26 | 0.28 | 2.89 | 85 |
| Whale | 2.45 | 0.23 | 0.09 | 2.76 | 85 |
| Clam | 2.14 | 0.27 | 0.31 | 2.72 | 85 |
| Deer | 2.06 | 0.22 | 0.10 | 2.38 | 85 |
| Banana | 1.18 | 0.04 | 1.16 | 2.38 | 126 |
| Wine | 0.70 | 0.02 | 1.47 | 2.18 | 147 |
| Alcohol | 0.83 | 0.02 | 1.27 | 2.12 | 356 |
| Horse | 1.81 | 0.17 | 0.10 | 2.08 | 85 |
| Sugar | 1.00 | 0.01 | 1.07 | 2.08 | 4.2 |
| Fish | 1.47 | 0.25 | 0.10 | 1.82 | 85 |
| Corn | 1.65 | 0.04 | 0.13 | 1.82 | 234 |
| Wheat | 1.57 | 0.05 | 0.13 | 1.76 | 64 |
| Dairy | 0.78 | 0.10 | 0.86 | 1.73 | 244 |
| Cow | 1.76 | 0.07 | -0.14 | 1.69 | 85 |
| Rice | 1.38 | 0.04 | 0.07 | 1.49 | 158 |
| Olives | 1.16 | 0.16 | -0.09 | 1.23 | 42 |
| Pig | 1.33 | 0.09 | -0.30 | 1.12 | 113 |
| Sheep | 1.15 | 0.08 | -0.28 | 0.94 | 85 |


**Which goods feed the happiness line:**
- **By this score:** fruit (lemon, apple, banana), wine, beer, sugar and milk, and tea and coffee through caffeine.
- **Fatty meats score low on well-being** (heavy) but high on satiety.
- **Proposal:** a good gives one happy face to the city when its people eat at least one serving of it per head a day, as a luxury resource does today.
- **Lemons** rank high by water and vitamin C, but they are sour. Palatability per good is not in the score yet.

## 7. Fish as the whole animal

**The Fish good is now a catch, not a fillet:**
- half fatty fish (herring);
- 45 % lean fish flesh (cod);
- 5 % liver (lingcod liver, 42 g fat per 100 g). Its vitamin A is scaled from cod liver oil (30,000 µg per 100 g) by the liver's fat share.

All values are from USDA SR Legacy. The shares are estimates to source (catch composition, liver about 5 % of a cod's weight). 15 % is bones and fins.

**Per 100 g:** 156 kcal, 16.5 g protein, 9.3 g fat, 651 µg vitamin A. The old fillet value was 64 kcal and 2.2 g fat.

**In the fishing village:** the people now reach 2,170 kcal against 3,193.
- **What binds is the 100 g fat ceiling per good:** 1.26 kg of whole fish holds 100 g fat.
- **Question:** should the 100 g fat ceiling apply to fish eaten whole? Fishing and sea-mammal peoples ate more fat than that.

## 8. The cities (constructed stocks)

#### A. Market town, 20,000; 70 % vigorous, 20 % active, 10 % sedentary
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Wheat | 7,000 | 959 | 958 | 6 | 0 |
| Dairy | 4,000 | 548 | 541 | 51 | 51 |
| Pig | 600 | 82 | 80 | 18 | 18 |
| Apple | 1,500 | 205 | 188 | 131 | 131 |
| Alcohol | 3,000 | 411 | 408 | 20 | 3 |
| Salt | 60 | 8 | 8 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3685 | 3440 | 1.08 | 122 (14 %) | 314 | 1219 | 716 | 0 | 2.24 | 1.20 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.10 | 0.45 | 5.07 | 3.42 | 1.40 | 0.73 | 3.13 | 2.56 | 1.17 | 0.58 | 1.17 | 5.82 |

#### B. Coastal city, 200,000; 50 % vigorous, 30 % active, 20 % sedentary
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Rice | 75,000 | 1027 | 1025 | 175 | 9 |
| Fish | 35,000 | 479 | 476 | 228 | 228 |
| Tea | 600 | 8 | 8 | 0 | 0 |
| Banana | 15,000 | 205 | 200 | 400 | 400 |
| Salt | 500 | 7 | 7 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|
| 3025 | 3702 | 3620 | 1.20 | 129 (14 %) | 599 | 353 | 1296 | 70 | 2.36 | 1.20 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.47 | 4.64 | 7.62 | 5.42 | 1.22 | 0.92 | 2.26 | 2.58 | 0.22 | 9.45 | 1.42 | 4.88 |

#### C. Industrial city, 1,000,000; 40 % vigorous, 30 % active, 30 % sedentary
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Wheat | 220,000 | 603 | 603 | 71 | 4 |
| Potato | 600,000 | 1644 | 1642 | 746 | 373 |
| Sugar | 30,000 | 82 | 80 | 643 | 64 |
| Dairy | 250,000 | 685 | 672 | 4,672 | 4,672 |
| Cow | 40,000 | 110 | 107 | 1,067 | 1,067 |
| Coffee | 3,000 | 8 | 8 | 0 | 0 |
| Salt | 3,000 | 8 | 8 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|
| 2916 | 3703 | 3580 | 1.23 | 126 (14 %) | 1389 | 1131 | 0 | 73 | 2.33 | 1.20 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.37 | 0.54 | 5.10 | 3.86 | 1.56 | 1.47 | 3.06 | 2.58 | 1.41 | 0.83 | 2.64 | 6.06 |

#### E. Rich city, 100,000, everything in surplus; 20 % vigorous, 40 % active, 40 % sedentary
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Cow | 20,000 | 548 | 367 | 6,617 | 6,617 |
| Dairy | 150,000 | 4110 | 1082 | 110,508 | 110,508 |
| Potato | 60,000 | 1644 | 1642 | 75 | 37 |
| Wheat | 40,000 | 1096 | 292 | 29,345 | 1,467 |
| Apple | 20,000 | 548 | 542 | 229 | 229 |
| Sugar | 8,000 | 219 | 24 | 7,119 | 712 |
| Wine | 15,000 | 411 | 397 | 507 | 76 |
| Tea | 400 | 11 | 11 | 0 | 0 |
| Salt | 500 | 14 | 10 | 135 | 14 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|
| 2735 | 3708 | 3710 | 1.36 | 158 (17 %) | 1968 | 2491 | 0 | 94 | 2.40 | 1.20 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.96 | 0.90 | 4.58 | 3.68 | 1.41 | 3.66 | 3.54 | 3.12 | 1.98 | 1.26 | 3.04 | 7.77 |

#### F. Fishing village, 5,000, fish (whole animal) and crab in plenty; 70 % vigorous
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Fish | 6,000 | 3288 | 1255 | 3,709 | 3,709 |
| Crab | 2,000 | 1096 | 1085 | 20 | 20 |
| Salt | 15 | 8 | 8 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3685 | 2170 | 0.68 | 276 (51 %) | 1723 | 0 | 526 | 0 | 1.41 | 0.02 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 12.23 | 2.15 | 3.64 | 2.21 | 26.84 | 2.27 | 4.65 | 1.52 | 24.89 | 2.28 | 11.57 |

#### D. Besieged town, 20,000, grain and salt pork only
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Wheat | 3,000 | 411 | 408 | 22 | 1 |
| Pig | 400 | 55 | 52 | 19 | 19 |
| Salt | 60 | 8 | 8 | 0 | 0 |

| Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|
| 3193 | 3685 | 1260 | 0.39 | 45 (14 %) | 77 | 0 | 2172 | 0 | 1.40 | 0.00 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 0.00 | 2.20 | 1.43 | 0.50 | 0.07 | 1.24 | 1.03 | 0.14 | 0.00 | 0.39 | 5.36 |

## 9. The rich city, and what still needs work

**The rich city (E) now eats:**
- potatoes 1.6 kg, apples 542 g, wine 397 g;
- milk 1.1 L, beef 367 g, bread grain 292 g;
- sugar 24 g, tea.

**Bread and sugar are eaten in part.**

**Milk to dairy products:** the goods pass runs its recipes before consumption (`runGoodsRecipes` before `consumeGoods`, GW.F5). Milk the city cannot drink fresh is turned into cheese and butter where it has the dairy buildings (IN.F1). Cheese keeps (kept form, 15 % a year). The ratio of milk to cheese is to be sourced.

**Sugar:**
- **What the model gives:** the rich city eats 24 g a day (about 9 kg a year).
- **No source yet:** I have not found a sourced figure for Britain around 1900 to check it against.
- **Why it is low:** the serving of one teaspoon makes sugar's returns fall fast. A source for historical sugar intake would set its serving, or its well-being weight.

## 10. Water supply in the general health

- **Accepted:** water supply levels set sanitation faces (WHO levels).
- **Order:** they cover the density faces first, and what is left joins the healthy faces in the general health level `H` (`round_m87.md` section 1.3).
- **Water quality** (D31) also enters `H`.

## 11. Open

- Should the fat ceiling apply to whole fish (section 7)?
- The weights of the well-being score, and palatability (section 6).
- A sourced figure for sugar intake in 1900s Britain or today (section 9).
- The catch composition and liver share of the Fish good.
- How heat and labour raise the water need.
- Measured satiety for milk, pork and seafood.
