# Food model: case report

Written by `plan/tools/food_model.py --md`; every number below comes from the run, nothing is typed by hand.

## farming town, temperate

### Inputs

| Variable | Value |
|---|---|
| body weight | 70 kg |
| share of men | 0.5 |
| age | 30 years |
| work class | manual labour |
| activity level asked (PAL) | 2.0 (user U157-U160) |
| air temperature | 12 °C |
| relative humidity | 75 % |
| altitude | 50 m |
| development group (Yamada HDI) | 2 |
| share of days with a hot work shift | 0.0 |
| culture (lactase persistence, user U163) | Germanic |
| milk pasteurised | False |
| lactose rule | none: raw milk is universally digestible (U163) |

| Good available | Composition record | g per person per day (cap from user ceilings) | kcal / protein g / fat g per 100 g |
|---|---|---|---|
| BONUS_WHEAT | default form BONUS_WHEAT:bread: USDA 172690 (Bread, whole-wheat, prepared from recipe) | 900 (cap 900) | 278 / 8.4 / 5.4 |
| BONUS_COW | default form BONUS_COW:whole: BONUS_COW:lean 72.7 % + BONUS_COW:fat (suet) 24.2 % + BONUS_COW:liver 2.0 % + BONUS_COW:heart 0.7 % + BONUS_COW:kidneys 0.3 % | 150 (cap 150) | 311 / 17.1 / 26.9 |
| BONUS_PIG | default form BONUS_PIG:whole: BONUS_PIG:lean 62.6 % + BONUS_PIG:fat (backfat) 34.2 % + BONUS_PIG:liver 2.3 % + BONUS_PIG:heart 0.5 % + BONUS_PIG:kidneys 0.5 % | 150 (cap 150) | 365 / 14.9 / 33.5 |
| BONUS_DAIRY | default form BONUS_DAIRY:milk: USDA 172217 (Milk, whole, 3.25% milkfat, without added vitamin A and vitamin D) | 600 (cap 600) | 61 / 3.1 / 3.3 |
| BONUS_APPLE | default form BONUS_APPLE:raw: USDA 171688 (Apples, raw, with skin (Includes foods for USDA's Food Distribution Program)) | 200 (cap 200) | 52 / 0.3 / 0.2 |
| BONUS_SALT | default form BONUS_SALT:table salt: USDA 173468 (Salt, table) | 15 (cap 15) | 0 / 0.0 / 0.0 |

### Results

| Measure | Value |
|---|---|
| resting expenditure | 1428.0 kcal |
| energy need (PAL x REE + caffeine) | 2856.0 kcal (caffeine 0.0 mg, +0.0 kcal) |
| energy of basal function (1.2 x REE) | 1713.6 kcal |
| starving | no |
| fullness eaten / fed level (user U089, U090) | 6207.7 / 3000.0 (coverage 1.0); no satiety index: none |
| energy eaten: main / with dessert | 2856.0 / 2856.0 kcal |
| labour capacity (PAL reached) | 1.0 (2.0) |
| nutrient minima covered (mean) | 1.0 |
| deficient (below minimum) | none |
| mean adequacy ratio | 0.9145 |
| coverage of athletes' optima (user U173-U189) | 0.3708 |
| strength (user U105 anchors) | 78.2 % |
| iodine / IQ (user U107 anchors) | 96.2 µg / 94.2 |
| mercury (fish, low-high) / tolerable | [0.0, 0.0] / 0.3 µg per kg bw a day |
| cadmium (shellfish, offal) / tolerable | 0.296 / 5.0 µg per kg bw a week |
| inorganic arsenic (rice, shellfish) / tolerable | 0.0 / 0.06 µg per kg bw a week |
| iron absorbed fraction | 0.16 (none applied (tea type and timing not relevant, M120)) |
| calcium absorbed, goods with a measured fraction | 217.0 mg (BONUS_DAIRY); no measured fraction: BONUS_APPLE, BONUS_COW, BONUS_PIG, BONUS_SALT, BONUS_WHEAT |
| zinc absorbed (Miller) / minimum | 3.36 / 3.55 mg |
| B12 absorbed at most (3 meals x per-meal saturation) | 5.25 µg |
| protein, per meal, absorption hours at 10 and 1.3 g/h | 108.8 g, 36.3 g, [3.6, 27.9] h |
| urea capacity | 284.2 g |
| fat | 137.2 g (sweating range: False) |
| alcohol | 0.0 g a week (with fat: False) |
| water: turnover / from food / metabolic / from drinks / to draw | 3758 / 491 / 500 / 900 / 1867 ml |
| repetition: goods over 5 % of energy / largest share | 4 / 0.48 |

| Good | Eaten g (main + dessert) | Left g | Quality | Keep class -> user class (spoilage % a year, user U168-U172) |
|---|---|---|---|---|
| BONUS_WHEAT | 493.2 (493.2 + 0) | 406.8 | 0.7 | grain_granary -> roots and grains (50.0) |
| BONUS_COW | 150.0 (150.0 + 0) | 0.0 | 0.65 | fresh -> others (90.0) |
| BONUS_PIG | 150.0 (150.0 + 0) | 0.0 | 0.65 | fresh -> others (90.0) |
| BONUS_DAIRY | 600.0 (600.0 + 0) | 0.0 | 0.828 | fresh -> others (90.0) |
| BONUS_APPLE | 200.0 (200.0 + 0) | 0.0 | 0.468 | fresh -> others (90.0) |
| BONUS_SALT | 15.0 (15.0 + 0) | 0.0 | 0.0 | dried -> dried (10.0) |

| Nutrient | Intake | Target | Athletes | Minimum | Ceiling | Where it comes from (share of intake) |
|---|---|---|---|---|---|---|
| protein (g) | 108.817 | 113.4 | 150.0 | 45.5 | — | BONUS_WHEAT 38 %, BONUS_COW 24 %, BONUS_PIG 21 %, BONUS_DAIRY 17 % |
| sodium (mg) | 7917.482 | 4995.0 | 10000.0 | 21.0 | 7000.0 **above** | BONUS_SALT 73 %, BONUS_WHEAT 22 % |
| potassium (mg) | 3313.938 | 3000.0 | 5000.0 | 1075.0 | — | BONUS_WHEAT 47 %, BONUS_DAIRY 24 %, BONUS_PIG 12 %, BONUS_COW 11 %, BONUS_APPLE 6 % |
| calcium (mg) | 885.2 | 800 | 3000.0 | 741 | 4000.0 | BONUS_DAIRY 77 %, BONUS_WHEAT 18 % |
| magnesium (mg) | 514.937 | 362.5 | 1000.0 | 165 | — | BONUS_WHEAT 78 %, BONUS_DAIRY 12 % |
| iron (mg) | 20.03 | 13.45 | 15.0 | 8.625 | 80.0 | BONUS_WHEAT 76 %, BONUS_COW 13 %, BONUS_PIG 9 % |
| zinc (mg) | 17.744 | 8.1 | 40.0 | — | 60.0 | BONUS_WHEAT 42 %, BONUS_COW 31 %, BONUS_PIG 14 %, BONUS_DAIRY 13 % |
| iodine (µg) | 96.15 | 200.0 | 1000.0 | 54.5 | 1100.0 | BONUS_DAIRY 100 % |
| selenium (µg) | 279.604 | 49 | 500.0 | 17 | 1600.0 | BONUS_WHEAT 68 %, BONUS_PIG 14 %, BONUS_COW 10 %, BONUS_DAIRY 8 % |
| vit_a_rae (µg RAE) | 662.657 | 466.5 | 3000.0 | 175.0 | 140000 | BONUS_DAIRY 42 %, BONUS_PIG 34 %, BONUS_COW 23 % |
| thiamin (mg) | 2.561 | 1.142 | 100.0 | 0.857 | — | BONUS_WHEAT 58 %, BONUS_PIG 26 %, BONUS_DAIRY 11 % |
| riboflavin (mg) | 2.906 | 1.4 | 50.0 | 0.5 | — | BONUS_WHEAT 39 %, BONUS_DAIRY 35 %, BONUS_PIG 13 %, BONUS_COW 11 % |
| niacin_ne (mg NE) | 43.208 | 19 | 100.0 | 12.566 | — | BONUS_WHEAT 38 %, BONUS_COW 26 %, BONUS_PIG 25 %, BONUS_DAIRY 10 % |
| vit_b6 (mg) | 2.593 | 1.701 | 100.0 | 0.6 | 117.0 | BONUS_WHEAT 38 %, BONUS_COW 25 %, BONUS_PIG 25 %, BONUS_DAIRY 8 % |
| folate_dfe (µg DFE) | 445.832 | 400 | 1000.0 | 300 | — | BONUS_WHEAT 86 %, BONUS_DAIRY 7 % |
| b12 (µg) | 8.783 | 5.6 | 5000.0 | 1 | — | BONUS_COW 50 %, BONUS_DAIRY 31 %, BONUS_PIG 19 % |
| vit_c (mg) | 10.536 | 100 | 2000.0 | 10 | 1000.0 | BONUS_APPLE 87 %, BONUS_PIG 12 % |

| Well-being list (separate from nutrition) | g | hyper-palatable | kcal per g | satiety index |
|---|---|---|---|---|
| BONUS_DAIRY | 600.0 | True | 0.61 | 350.0 |
| BONUS_WHEAT | 493.2 | True | 2.78 | 157.0 |
| BONUS_SALT | 15.0 | False | 0.0 | 200.0 |
| BONUS_APPLE | 200.0 | False | 0.52 | 197.0 |
| BONUS_COW | 150.0 | False | 3.11 | 300.0 |
| BONUS_PIG | 150.0 | False | 3.65 | 260.0 |

## fishing village, cool coast

### Inputs

| Variable | Value |
|---|---|
| body weight | 70 kg |
| share of men | 0.5 |
| age | 30 years |
| work class | manual labour |
| activity level asked (PAL) | 2.0 (user U157-U160) |
| air temperature | 8 °C |
| relative humidity | 85 % |
| altitude | 5 m |
| development group (Yamada HDI) | 2 |
| share of days with a hot work shift | 0.0 |
| culture (lactase persistence, user U163) | Germanic |
| milk pasteurised | False |
| lactose rule | none: raw milk is universally digestible (U163) |

| Good available | Composition record | g per person per day (cap from user ceilings) | kcal / protein g / fat g per 100 g |
|---|---|---|---|
| BONUS_FISH:region:Europe | catch of Europe (user U154): BONUS_FISH:mext:pond smelt, whole 4.0 % + BONUS_FISH:herring whole, year-round 20.0 % + BONUS_FISH:tuna (bluefin) 7.0 % + BONUS_FISH:whole 32.0 % + BONUS_FISH:salmon (Atlantic, wild) 22.0 % + BONUS_FISH:Atlantic mackerel 15.0 % | 2500 (cap 2500) | 151 / 18.3 / 8.1 |
| BONUS_FISH:herring whole, year-round | herring (USDA 175116) with whole-fish fat 12.0 % (user U155), kcal by Atwater 4/9/4 | 1000 (cap 1000) | 180 / 18.0 / 12.0 |
| BONUS_CLAM | default form BONUS_CLAM:raw: USDA 174214 (Mollusks, clam, mixed species, raw) | 300 (cap 300) | 86 / 14.7 / 1.0 |
| BONUS_WHEAT | default form BONUS_WHEAT:bread: USDA 172690 (Bread, whole-wheat, prepared from recipe) | 250 (cap 250) | 278 / 8.4 / 5.4 |
| BONUS_SALT | default form BONUS_SALT:table salt: USDA 173468 (Salt, table) | 15 (cap 15) | 0 / 0.0 / 0.0 |

### Results

| Measure | Value |
|---|---|
| resting expenditure | 1428.0 kcal |
| energy need (PAL x REE + caffeine) | 2856.0 kcal (caffeine 0.0 mg, +0.0 kcal) |
| energy of basal function (1.2 x REE) | 1713.6 kcal |
| starving | no |
| fullness eaten / fed level (user U089, U090) | 6672.4 / 3000.0 (coverage 1.0); no satiety index: none |
| energy eaten: main / with dessert | 2856.0 / 2856.0 kcal |
| labour capacity (PAL reached) | 1.0 (2.0) |
| nutrient minima covered (mean) | 1.0 |
| deficient (below minimum) | none |
| mean adequacy ratio | 0.9343 |
| coverage of athletes' optima (user U173-U189) | 0.5734 |
| strength (user U105 anchors) | 198.1 % |
| iodine / IQ (user U107 anchors) | 1030.7 µg / 115.0 |
| mercury (fish, low-high) / tolerable | [0.169, 3.373] / 0.3 µg per kg bw a day |
| cadmium (shellfish, offal) / tolerable | 9.51 / 5.0 µg per kg bw a week |
| inorganic arsenic (rice, shellfish) / tolerable | 0.3 / 0.06 µg per kg bw a week |
| iron absorbed fraction | 0.16 (none applied (tea type and timing not relevant, M120)) |
| calcium absorbed, goods with a measured fraction | 0 mg (none); no measured fraction: BONUS_CLAM, BONUS_FISH:herring whole, year-round, BONUS_FISH:region:Europe, BONUS_SALT, BONUS_WHEAT |
| zinc absorbed (Miller) / minimum | 4.38 / 3.55 mg |
| B12 absorbed at most (3 meals x per-meal saturation) | 5.25 µg |
| protein, per meal, absorption hours at 10 and 1.3 g/h | 280.0 g, 93.3 g, [9.3, 71.8] h |
| urea capacity | 284.2 g |
| fat | 128.6 g (sweating range: False) |
| alcohol | 0.0 g a week (with fat: False) |
| water: turnover / from food / metabolic / from drinks / to draw | 3725 / 1164 / 500 / 0 / 2060 ml |
| repetition: goods over 5 % of energy / largest share | 4 / 0.403 |

| Good | Eaten g (main + dessert) | Left g | Quality | Keep class -> user class (spoilage % a year, user U168-U172) |
|---|---|---|---|---|
| BONUS_FISH:region:Europe | 762.3 (762.3 + 0) | 1737.7 | 0.878 | fresh -> others (90.0) |
| BONUS_FISH:herring whole, year-round | 418.1 (418.1 + 0) | 581.9 | 0.809 | fresh -> others (90.0) |
| BONUS_CLAM | 300.0 (300.0 + 0) | 0.0 | 0.794 | fresh -> others (90.0) |
| BONUS_WHEAT | 250.0 (250.0 + 0) | 0.0 | 0.7 | grain_granary -> roots and grains (50.0) |
| BONUS_SALT | 15.0 (15.0 + 0) | 0.0 | 0.0 | dried -> dried (10.0) |

| Nutrient | Intake | Target | Athletes | Minimum | Ceiling | Where it comes from (share of intake) |
|---|---|---|---|---|---|---|
| protein (g) | 279.972 | 113.4 | 150.0 | 45.5 | — | BONUS_FISH:region:Europe 50 %, BONUS_FISH:herring whole, year-round 27 %, BONUS_CLAM 16 %, BONUS_WHEAT 8 % |
| sodium (mg) | 9378.72 | 4995.0 | 10000.0 | 21.0 | 7000.0 **above** | BONUS_SALT 62 %, BONUS_CLAM 19 %, BONUS_WHEAT 9 %, BONUS_FISH:region:Europe 6 % |
| potassium (mg) | 4995.545 | 3000.0 | 5000.0 | 1075.0 | — | BONUS_FISH:region:Europe 54 %, BONUS_FISH:herring whole, year-round 27 %, BONUS_WHEAT 16 % |
| calcium (mg) | 740.988 | 800 | 3000.0 | 741 | 4000.0 | BONUS_FISH:region:Europe 40 %, BONUS_FISH:herring whole, year-round 32 %, BONUS_CLAM 16 %, BONUS_WHEAT 11 % |
| magnesium (mg) | 678.827 | 362.5 | 1000.0 | 165 | — | BONUS_FISH:region:Europe 42 %, BONUS_WHEAT 30 %, BONUS_FISH:herring whole, year-round 20 %, BONUS_CLAM 8 % |
| iron (mg) | 24.102 | 13.45 | 15.0 | 8.625 | 80.0 | BONUS_WHEAT 32 %, BONUS_FISH:region:Europe 28 %, BONUS_CLAM 20 %, BONUS_FISH:herring whole, year-round 19 % |
| zinc (mg) | 14.762 | 8.1 | 40.0 | — | 60.0 | BONUS_FISH:region:Europe 36 %, BONUS_FISH:herring whole, year-round 28 %, BONUS_WHEAT 25 %, BONUS_CLAM 10 % |
| iodine (µg) | 1030.727 | 200.0 | 1000.0 | 54.5 | 1100.0 | BONUS_FISH:region:Europe 84 %, BONUS_CLAM 16 % |
| selenium (µg) | 607.712 | 49 | 500.0 | 17 | 1600.0 | BONUS_FISH:region:Europe 44 %, BONUS_FISH:herring whole, year-round 25 %, BONUS_WHEAT 16 %, BONUS_CLAM 15 % |
| vit_a_rae (µg RAE) | 4344.608 | 466.5 | 3000.0 | 175.0 | 140000 | BONUS_FISH:region:Europe 91 %, BONUS_CLAM 6 % |
| thiamin (mg) | 2.299 | 1.142 | 100.0 | 0.857 | — | BONUS_FISH:region:Europe 48 %, BONUS_WHEAT 33 %, BONUS_FISH:herring whole, year-round 17 % |
| riboflavin (mg) | 3.475 | 1.4 | 50.0 | 0.5 | — | BONUS_FISH:region:Europe 52 %, BONUS_FISH:herring whole, year-round 28 %, BONUS_WHEAT 16 % |
| niacin_ne (mg NE) | 112.148 | 19 | 100.0 | 12.566 | — | BONUS_FISH:region:Europe 58 %, BONUS_FISH:herring whole, year-round 24 %, BONUS_CLAM 10 %, BONUS_WHEAT 7 % |
| vit_b6 (mg) | 4.886 | 1.701 | 100.0 | 0.6 | 117.0 | BONUS_FISH:region:Europe 63 %, BONUS_FISH:herring whole, year-round 26 %, BONUS_WHEAT 10 % |
| folate_dfe (µg DFE) | 342.178 | 400 | 1000.0 | 300 | — | BONUS_WHEAT 57 %, BONUS_FISH:region:Europe 26 %, BONUS_FISH:herring whole, year-round 12 % |
| b12 (µg) | 138.514 | 5.6 | 5000.0 | 1 | — | BONUS_FISH:herring whole, year-round 41 %, BONUS_FISH:region:Europe 34 %, BONUS_CLAM 24 % |
| vit_c (mg) | 10.177 | 100 | 2000.0 | 10 | 1000.0 | BONUS_FISH:region:Europe 71 %, BONUS_FISH:herring whole, year-round 29 % |

| Well-being list (separate from nutrition) | g | hyper-palatable | kcal per g | satiety index |
|---|---|---|---|---|
| BONUS_WHEAT | 250.0 | True | 2.78 | 157.0 |
| BONUS_SALT | 15.0 | False | 0.0 | 200.0 |
| BONUS_CLAM | 300.0 | False | 0.86 | 400.0 |
| BONUS_FISH:region:Europe | 762.3 | False | 1.51 | 248.2 |
| BONUS_FISH:herring whole, year-round | 418.1 | False | 1.8 | 225.0 |

## rice town, hot season labour

### Inputs

| Variable | Value |
|---|---|
| body weight | 60 kg |
| share of men | 0.5 |
| age | 30 years |
| work class | manual labour |
| activity level asked (PAL) | 2.0 (user U157-U160) |
| air temperature | 30 °C |
| relative humidity | 70 % |
| altitude | 20 m |
| development group (Yamada HDI) | 2 |
| share of days with a hot work shift | 0.5 |
| culture (lactase persistence, user U163) | East Asians |
| milk pasteurised | False |
| lactose rule | none: raw milk is universally digestible (U163) |

| Good available | Composition record | g per person per day (cap from user ceilings) | kcal / protein g / fat g per 100 g |
|---|---|---|---|
| BONUS_RICE | default form BONUS_RICE:polished: USDA 169756 (Rice, white, long-grain, regular, raw, unenriched) | 900 (cap 900) | 365 / 7.1 / 0.7 |
| BONUS_FISH:region:Asia | catch of Asia (user U154): BONUS_FISH:mext:pond smelt, whole 55.0 % + BONUS_FISH:herring whole, year-round 14.0 % + BONUS_FISH:tuna (bluefin) 7.0 % + BONUS_FISH:whole 13.0 % + BONUS_FISH:salmon (Atlantic, wild) 2.0 % + BONUS_FISH:Atlantic mackerel 9.0 % | 200 (cap 200) | 112 / 16.3 / 5.1 |
| BONUS_BANANA | default form BONUS_BANANA:raw: USDA 173944 (Bananas, raw) | 200 (cap 200) | 89 / 1.1 / 0.3 |
| BONUS_TEA | default form BONUS_TEA:herbal, brewed: USDA 173232 (Beverages, tea, herb, other than chamomile, brewed) | 600 (cap 600) | 1 / 0.0 / 0.0 |
| BONUS_SALT | default form BONUS_SALT:table salt: USDA 173468 (Salt, table) | 20 (cap 20) | 0 / 0.0 / 0.0 |

### Results

| Measure | Value |
|---|---|
| resting expenditure | 1277.0 kcal |
| energy need (PAL x REE + caffeine) | 2599.0 kcal (caffeine 180.0 mg, +45.0 kcal) |
| energy of basal function (1.2 x REE) | 1532.4 kcal |
| starving | no |
| fullness eaten / fed level (user U089, U090) | 2942.3 / 3000.0 (coverage 0.9808); no satiety index: none |
| energy eaten: main / with dessert | 2599.0 / 2605.0 kcal |
| labour capacity (PAL reached) | 1.0 (2.035) |
| nutrient minima covered (mean) | 0.9359 |
| deficient (below minimum) | calcium, iron, thiamin, folate_dfe |
| mean adequacy ratio | 0.7525 |
| coverage of athletes' optima (user U173-U189) | 0.2375 |
| strength (user U105 anchors) | 63.8 % |
| iodine / IQ (user U107 anchors) | 123.1 µg / 97.4 |
| mercury (fish, low-high) / tolerable | [0.033, 0.667] / 0.3 µg per kg bw a day |
| cadmium (shellfish, offal) / tolerable | 0.0 / 5.0 µg per kg bw a week |
| inorganic arsenic (rice, shellfish) / tolerable | 7.023 / 0.06 µg per kg bw a week |
| iron absorbed fraction | 0.16 (none applied (tea type and timing not relevant, M120)) |
| calcium absorbed, goods with a measured fraction | 0 mg (none); no measured fraction: BONUS_BANANA, BONUS_FISH:region:Asia, BONUS_RICE, BONUS_SALT, BONUS_TEA |
| zinc absorbed (Miller) / minimum | 1.7 / 3.55 mg |
| B12 absorbed at most (3 meals x per-meal saturation) | 5.25 µg |
| protein, per meal, absorption hours at 10 and 1.3 g/h | 77.8 g, 25.9 g, [2.6, 19.9] h |
| urea capacity | 243.6 g |
| fat | 14.8 g (sweating range: False) |
| alcohol | 0.0 g a week (with fat: False) |
| water: turnover / from food / metabolic / from drinks / to draw | 4628 / 373 / 500 / 600 / 3154 ml |
| repetition: goods over 5 % of energy / largest share | 3 / 0.843 |

| Good | Eaten g (main + dessert) | Left g | Quality | Keep class -> user class (spoilage % a year, user U168-U172) |
|---|---|---|---|---|
| BONUS_RICE | 602.0 (602.0 + 0) | 298.0 | 0.371 | grain_granary -> roots and grains (50.0) |
| BONUS_FISH:region:Asia | 200.0 (200.0 + 0) | 0.0 | 0.875 | fresh -> others (90.0) |
| BONUS_BANANA | 200.0 (200.0 + 0) | 0.0 | 0.604 | fresh -> others (90.0) |
| BONUS_TEA | 600.0 (0.4 + 599.6) | 0.0 | 0.49 | dried -> dried (10.0) |
| BONUS_SALT | 20.0 (20.0 + 0) | 0.0 | 0.0 | dried -> dried (10.0) |

| Nutrient | Intake | Target | Athletes | Minimum | Ceiling | Where it comes from (share of intake) |
|---|---|---|---|---|---|---|
| protein (g) | 77.759 | 97.2 | 128.6 | 39.0 | — | BONUS_RICE 55 %, BONUS_FISH:region:Asia 42 % |
| sodium (mg) | 8071.654 | 7695.0 | 10000.0 | 2721.0 | 9700.0 | BONUS_SALT 96 % |
| potassium (mg) | 1889.837 | 3000.0 | 5000.0 | 1075.0 | — | BONUS_BANANA 38 %, BONUS_RICE 37 %, BONUS_FISH:region:Asia 23 % |
| calcium (mg) | 714.052 **below minimum** | 800 | 3000.0 | 741 | 4000.0 | BONUS_FISH:region:Asia 73 %, BONUS_RICE 24 % |
| magnesium (mg) | 276.111 | 362.5 | 1000.0 | 165 | — | BONUS_RICE 55 %, BONUS_FISH:region:Asia 24 %, BONUS_BANANA 20 % |
| iron (mg) | 7.77 **below minimum** | 13.45 | 15.0 | 8.625 | 80.0 | BONUS_RICE 62 %, BONUS_FISH:region:Asia 24 %, BONUS_BANANA 7 %, BONUS_TEA 6 % |
| zinc (mg) | 9.938 | 8.1 | 40.0 | — | 60.0 | BONUS_RICE 66 %, BONUS_FISH:region:Asia 28 % |
| iodine (µg) | 123.1 | 200.0 | 1000.0 | 54.5 | 1100.0 | BONUS_FISH:region:Asia 100 % |
| selenium (µg) | 149.662 | 49 | 500.0 | 17 | 1600.0 | BONUS_RICE 61 %, BONUS_FISH:region:Asia 38 % |
| vit_a_rae (µg RAE) | 592.496 | 466.5 | 3000.0 | 175.0 | 120000 | BONUS_FISH:region:Asia 99 % |
| thiamin (mg) | 0.682 **below minimum** | 1.04 | 100.0 | 0.78 | — | BONUS_RICE 62 %, BONUS_FISH:region:Asia 20 %, BONUS_BANANA 9 %, BONUS_TEA 9 % |
| riboflavin (mg) | 0.821 | 1.4 | 50.0 | 0.5 | — | BONUS_FISH:region:Asia 43 %, BONUS_RICE 36 %, BONUS_BANANA 18 % |
| niacin_ne (mg NE) | 25.343 | 19 | 100.0 | 11.436 | — | BONUS_FISH:region:Asia 48 %, BONUS_RICE 46 %, BONUS_BANANA 6 % |
| vit_b6 (mg) | 2.216 | 1.458 | 100.0 | 0.6 | 117.0 | BONUS_RICE 45 %, BONUS_BANANA 33 %, BONUS_FISH:region:Asia 22 % |
| folate_dfe (µg DFE) | 101.722 **below minimum** | 400 | 1000.0 | 300 | — | BONUS_RICE 47 %, BONUS_BANANA 39 %, BONUS_FISH:region:Asia 7 %, BONUS_TEA 6 % |
| b12 (µg) | 15.953 | 5.6 | 5000.0 | 1 | — | BONUS_FISH:region:Asia 100 % |
| vit_c (mg) | 19.346 | 100 | 2000.0 | 10 | 1000.0 | BONUS_BANANA 90 %, BONUS_FISH:region:Asia 10 % |

| Well-being list (separate from nutrition) | g | hyper-palatable | kcal per g | satiety index |
|---|---|---|---|---|
| BONUS_SALT | 20.0 | False | 0.0 | 200.0 |
| BONUS_TEA | 600.0 | False | 0.01 | 50.0 |
| BONUS_BANANA | 200.0 | False | 0.89 | 118.0 |
| BONUS_FISH:region:Asia | 200.0 | False | 1.12 | 239.1 |
| BONUS_RICE | 602.0 | False | 3.65 | 100.0 |

