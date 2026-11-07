# Food model: case report

Written by `plan/tools/food_model.py --md`; every number below comes from the run, nothing is typed by hand.

## farming town, temperate

### Inputs

| Variable | Value |
|---|---|
| body weight | 70 kg |
| share of men | 0.5 |
| age | 30 years |
| activity level asked (PAL) | 2.41 |
| air temperature | 12 °C |
| relative humidity | 75 % |
| altitude | 50 m |
| development group (Yamada HDI) | 2 |
| share of days with a hot work shift | 0.0 |
| lactase persistent | True |
| dairy culture | True |
| tea timing | with_meal |
| maize treated with alkali | False |

| Good available | Composition record | g per person per day | kcal / protein g / fat g per 100 g |
|---|---|---|---|
| BONUS_WHEAT | USDA 168890 (Wheat, hard red winter) | 900 | 327 / 12.6 / 1.5 |
| BONUS_COW | cow as eaten: USDA 169430 meat, 169451 liver, 168625 heart, 169449 kidneys (41.4:1.12:0.37:0.18) | 150 | 285 / 17.4 / 23.3 |
| BONUS_PIG | USDA 167818 (Pork, fresh, loin, whole, separable lean and fat, raw) | 150 | 198 / 19.7 / 12.6 |
| BONUS_DAIRY | USDA 172217 (Milk, whole, 3.25% milkfat, without added vitamin A and vitamin D) | 600 | 61 / 3.1 / 3.3 |
| BONUS_APPLE | USDA 171688 (Apples, raw, with skin (Includes foods for USDA's Food Distribution Program)) | 200 | 52 / 0.3 / 0.2 |
| BONUS_SALT | USDA 173468 (Salt, table) | 15 | 0 / 0.0 / 0.0 |

### Results

| Measure | Value |
|---|---|
| resting expenditure | 1428.0 kcal |
| energy need (PAL x REE + caffeine) | 3441.5 kcal (caffeine 0.0 mg, +0.0 kcal) |
| energy of basal function (1.2 x REE) | 1713.6 kcal |
| starving | no |
| labour capacity (PAL reached) | 1.0 (2.41) |
| nutrient minima covered (mean) | 1.0 |
| deficient (below minimum) | none |
| mean adequacy ratio | 0.9067 |
| iron absorbed fraction | 0.16 (no inhibitor) |
| calcium absorbed, goods with a measured fraction | 217.0 mg (BONUS_DAIRY); no measured fraction: BONUS_APPLE, BONUS_COW, BONUS_PIG, BONUS_SALT, BONUS_WHEAT |
| zinc absorbed (Miller) / minimum | 3.64 / 3.55 mg |
| B12 absorbed at most (3 meals x per-meal saturation) | 5.25 µg |
| protein, per meal, absorption hours at 10 and 1.3 g/h | 156.6 g, 52.2 g, [5.2, 40.1] h |
| urea capacity | 284.2 g |
| fat | 77.6 g (sweating range: False) |
| alcohol | 0.0 g a week (with fat: False) |
| water: turnover / from food / metabolic / from drinks / to draw | 4199 / 421 / 500 / 900 / 2378 ml |
| fullness (Holt index, where measured) | 1.611 over 0.829 of energy |
| repetition: goods over 5 % of energy / largest share | 4 / 0.684 |

| Good | Eaten g | Left g | Quality | Keep class (spoilage % a year; basis) |
|---|---|---|---|---|
| BONUS_WHEAT | 719.5 | 180.5 | 0.662 | grain_granary (5; FAOstorage, traditional storage) |
| BONUS_COW | 139.2 | 10.8 | 0.708 | fresh (100; eaten in the year it is made) |
| BONUS_PIG | 112.4 | 37.6 | 0.698 | fresh (100; eaten in the year it is made) |
| BONUS_DAIRY | 600.0 | 0.0 | 0.842 | fresh (100; eaten in the year it is made) |
| BONUS_APPLE | 200.0 | 0.0 | 0.506 | fresh (100; eaten in the year it is made) |
| BONUS_SALT | 15.0 | 0.0 | 0.0 | dried (10; stockfish keeps several years; estimate for dried fruit) |

| Nutrient | Intake | Target | Minimum | Ceiling | Where it comes from (share of intake) |
|---|---|---|---|---|---|
| protein (g) | 156.558 | 113.4 | 45.5 | — | BONUS_WHEAT 58 %, BONUS_COW 15 %, BONUS_PIG 14 %, BONUS_DAIRY 12 % |
| sodium (mg) | 6227.959 | 4995.0 | 21.0 | 7000.0 | BONUS_SALT 93 % |
| potassium (mg) | 4392.589 | 3000.0 | 1075.0 | — | BONUS_WHEAT 59 %, BONUS_DAIRY 18 %, BONUS_PIG 9 %, BONUS_COW 9 % |
| calcium (mg) | 933.525 | 800 | 741 | 4000.0 | BONUS_DAIRY 73 %, BONUS_WHEAT 22 % |
| magnesium (mg) | 1024.064 | 362.5 | 165 | — | BONUS_WHEAT 89 %, BONUS_DAIRY 6 % |
| iron (mg) | 27.014 | 13.45 | 8.625 | 80.0 | BONUS_WHEAT 85 %, BONUS_COW 10 % |
| zinc (mg) | 28.291 | 8.1 | — | 60.0 | BONUS_WHEAT 67 %, BONUS_COW 18 %, BONUS_DAIRY 8 %, BONUS_PIG 7 % |
| iodine (µg) | 97.274 | 200.0 | 54.5 | 1100.0 | BONUS_DAIRY 99 % |
| selenium (µg) | 594.944 | 49 | 17 | 1600.0 | BONUS_WHEAT 86 %, BONUS_PIG 6 % |
| vit_a_rae (µg RAE) | 466.554 | 466.5 | 175.0 | 140000 | BONUS_DAIRY 59 %, BONUS_COW 39 % |
| thiamin (mg) | 4.197 | 1.377 | 1.032 | — | BONUS_WHEAT 66 %, BONUS_PIG 24 %, BONUS_DAIRY 7 % |
| riboflavin (mg) | 2.513 | 1.4 | 0.5 | — | BONUS_DAIRY 40 %, BONUS_WHEAT 33 %, BONUS_COW 14 %, BONUS_PIG 11 % |
| niacin_ne (mg NE) | 56.749 | 19 | 15.143 | — | BONUS_WHEAT 57 %, BONUS_COW 18 %, BONUS_PIG 17 %, BONUS_DAIRY 8 % |
| vit_b6 (mg) | 3.475 | 1.701 | 0.6 | 117.0 | BONUS_WHEAT 62 %, BONUS_PIG 15 %, BONUS_COW 14 %, BONUS_DAIRY 6 % |
| folate_dfe (µg DFE) | 331.006 | 400 | 300 | — | BONUS_WHEAT 83 %, BONUS_DAIRY 9 %, BONUS_COW 6 % |
| b12 (µg) | 9.278 | 5.6 | 1 | — | BONUS_COW 64 %, BONUS_DAIRY 29 %, BONUS_PIG 6 % |
| vit_c (mg) | 10.0 | 100 | 10 | 1000.0 | BONUS_APPLE 92 %, BONUS_PIG 7 % |

| Well-being list (separate from nutrition) | g | hyper-palatable | kcal per g | satiety index |
|---|---|---|---|---|
| BONUS_DAIRY | 600.0 | True | 0.61 | not measured |
| BONUS_SALT | 15.0 | False | 0.0 | not measured |
| BONUS_APPLE | 200.0 | False | 0.52 | 197 |
| BONUS_PIG | 112.4 | False | 1.98 | not measured |
| BONUS_COW | 139.2 | False | 2.85 | 176 |
| BONUS_WHEAT | 719.5 | False | 3.27 | 157 |

## fishing village, cool coast

### Inputs

| Variable | Value |
|---|---|
| body weight | 70 kg |
| share of men | 0.5 |
| age | 30 years |
| activity level asked (PAL) | 2.41 |
| air temperature | 8 °C |
| relative humidity | 85 % |
| altitude | 5 m |
| development group (Yamada HDI) | 2 |
| share of days with a hot work shift | 0.0 |
| lactase persistent | True |
| dairy culture | False |
| tea timing | with_meal |
| maize treated with alkali | False |

| Good available | Composition record | g per person per day | kcal / protein g / fat g per 100 g |
|---|---|---|---|
| BONUS_FISH | cod as eaten: USDA 171955 cod, 175132 roe, 169810 lingcod liver (Torry shares 36:4:5) | 1000 | 125 / 16.9 / 5.8 |
| BONUS_FISH:herring | USDA 175116 (Fish, herring, Atlantic, raw) | 1500 | 158 / 18.0 / 9.0 |
| BONUS_FISH:Atlantic mackerel | USDA 175119 (Fish, mackerel, Atlantic, raw) | 1000 | 205 / 18.6 / 13.9 |
| BONUS_CLAM | USDA 174214 (Mollusks, clam, mixed species, raw) | 300 | 86 / 14.7 / 1.0 |
| BONUS_WHEAT | USDA 168890 (Wheat, hard red winter) | 250 | 327 / 12.6 / 1.5 |
| BONUS_SALT | USDA 173468 (Salt, table) | 15 | 0 / 0.0 / 0.0 |

### Results

| Measure | Value |
|---|---|
| resting expenditure | 1428.0 kcal |
| energy need (PAL x REE + caffeine) | 3441.5 kcal (caffeine 0.0 mg, +0.0 kcal) |
| energy of basal function (1.2 x REE) | 1713.6 kcal |
| starving | no |
| labour capacity (PAL reached) | 1.0 (2.41) |
| nutrient minima covered (mean) | 0.9263 |
| deficient (below minimum) | calcium, folate_dfe, vit_c |
| mean adequacy ratio | 0.8754 |
| iron absorbed fraction | 0.16 (no inhibitor) |
| calcium absorbed, goods with a measured fraction | 0 mg (none); no measured fraction: BONUS_FISH, BONUS_FISH:Atlantic mackerel, BONUS_FISH:herring, BONUS_SALT, BONUS_WHEAT |
| zinc absorbed (Miller) / minimum | 4.17 / 3.55 mg |
| B12 absorbed at most (3 meals x per-meal saturation) | 5.25 µg |
| protein, per meal, absorption hours at 10 and 1.3 g/h | 284.2 g, 94.7 g, [9.5, 72.9] h |
| urea capacity | 284.2 g |
| fat | 174.8 g (sweating range: False) |
| alcohol | 0.0 g a week (with fat: False) |
| water: turnover / from food / metabolic / from drinks / to draw | 4166 / 940 / 500 / 0 / 2725 ml |
| fullness (Holt index, where measured) | 1.623 over 0.258 of energy |
| repetition: goods over 5 % of energy / largest share | 3 / 0.596 |

| Good | Eaten g | Left g | Quality | Keep class (spoilage % a year; basis) |
|---|---|---|---|---|
| BONUS_FISH | 55.1 | 944.9 | 0.897 | fresh (100; eaten in the year it is made) |
| BONUS_FISH:herring | 319.6 | 1180.4 | 0.829 | fresh (100; eaten in the year it is made) |
| BONUS_FISH:Atlantic mackerel | 1000.0 | 0.0 | 0.745 | fresh (100; eaten in the year it is made) |
| BONUS_CLAM | 0.0 | 300.0 | 0.811 | fresh (100; eaten in the year it is made) |
| BONUS_WHEAT | 250.0 | 0.0 | 0.662 | grain_granary (5; FAOstorage, traditional storage) |
| BONUS_SALT | 15.0 | 0.0 | 0.0 | dried (10; stockfish keeps several years; estimate for dried fruit) |

| Nutrient | Intake | Target | Minimum | Ceiling | Where it comes from (share of intake) |
|---|---|---|---|---|---|
| protein (g) | 284.2 | 113.4 | 45.5 | — | BONUS_FISH:Atlantic mackerel 65 %, BONUS_FISH:herring 20 %, BONUS_WHEAT 11 % |
| sodium (mg) | 7034.549 | 4995.0 | 21.0 | 7000.0 **above** | BONUS_SALT 83 %, BONUS_FISH:Atlantic mackerel 13 % |
| potassium (mg) | 5286.441 | 3000.0 | 1075.0 | — | BONUS_FISH:Atlantic mackerel 59 %, BONUS_FISH:herring 20 %, BONUS_WHEAT 17 % |
| calcium (mg) | 386.68 **below minimum** | 800 | 741 | 4000.0 | BONUS_FISH:herring 47 %, BONUS_FISH:Atlantic mackerel 31 %, BONUS_WHEAT 19 % |
| magnesium (mg) | 1192.486 | 362.5 | 165 | — | BONUS_FISH:Atlantic mackerel 64 %, BONUS_WHEAT 26 %, BONUS_FISH:herring 9 % |
| iron (mg) | 28.098 | 13.45 | 8.625 | 80.0 | BONUS_FISH:Atlantic mackerel 58 %, BONUS_WHEAT 28 %, BONUS_FISH:herring 13 % |
| zinc (mg) | 16.351 | 8.1 | — | 60.0 | BONUS_WHEAT 41 %, BONUS_FISH:Atlantic mackerel 39 %, BONUS_FISH:herring 19 % |
| iodine (µg) | 192.919 | 200.0 | 54.5 | 1100.0 | BONUS_FISH 100 % |
| selenium (µg) | 750.96 | 49 | 17 | 1600.0 | BONUS_FISH:Atlantic mackerel 59 %, BONUS_WHEAT 24 %, BONUS_FISH:herring 16 % |
| vit_a_rae (µg RAE) | 1370.246 | 466.5 | 175.0 | 140000 | BONUS_FISH 57 %, BONUS_FISH:Atlantic mackerel 36 %, BONUS_FISH:herring 7 % |
| thiamin (mg) | 3.07 | 1.377 | 1.032 | — | BONUS_FISH:Atlantic mackerel 57 %, BONUS_WHEAT 31 %, BONUS_FISH:herring 10 % |
| riboflavin (mg) | 4.217 | 1.4 | 0.5 | — | BONUS_FISH:Atlantic mackerel 74 %, BONUS_FISH:herring 18 %, BONUS_WHEAT 7 % |
| niacin_ne (mg NE) | 160.626 | 19 | 15.143 | — | BONUS_FISH:Atlantic mackerel 78 %, BONUS_FISH:herring 13 %, BONUS_WHEAT 7 % |
| vit_b6 (mg) | 5.821 | 1.701 | 0.6 | 117.0 | BONUS_FISH:Atlantic mackerel 69 %, BONUS_FISH:herring 17 %, BONUS_WHEAT 13 % |
| folate_dfe (µg DFE) | 143.957 **below minimum** | 400 | 300 | — | BONUS_WHEAT 66 %, BONUS_FISH:herring 22 %, BONUS_FISH:Atlantic mackerel 7 % |
| b12 (µg) | 131.674 | 5.6 | 1 | — | BONUS_FISH:Atlantic mackerel 66 %, BONUS_FISH:herring 33 % |
| vit_c (mg) | 7.461 **below minimum** | 100 | 10 | 1000.0 | BONUS_FISH:Atlantic mackerel 54 %, BONUS_FISH:herring 30 %, BONUS_FISH 16 % |

| Well-being list (separate from nutrition) | g | hyper-palatable | kcal per g | satiety index |
|---|---|---|---|---|
| BONUS_SALT | 15.0 | False | 0.0 | not measured |
| BONUS_FISH | 55.1 | False | 1.25 | 225 |
| BONUS_FISH:herring | 319.6 | False | 1.58 | not measured |
| BONUS_FISH:Atlantic mackerel | 1000.0 | False | 2.05 | not measured |
| BONUS_WHEAT | 250.0 | False | 3.27 | 157 |

## rice town, hot season labour

### Inputs

| Variable | Value |
|---|---|
| body weight | 60 kg |
| share of men | 0.5 |
| age | 30 years |
| activity level asked (PAL) | 2.41 |
| air temperature | 30 °C |
| relative humidity | 70 % |
| altitude | 20 m |
| development group (Yamada HDI) | 2 |
| share of days with a hot work shift | 0.5 |
| lactase persistent | False |
| dairy culture | False |
| tea timing | with_meal |
| maize treated with alkali | False |

| Good available | Composition record | g per person per day | kcal / protein g / fat g per 100 g |
|---|---|---|---|
| BONUS_RICE:polished | USDA 169756 (Rice, white, long-grain, regular, raw, unenriched) | 900 | 365 / 7.1 / 0.7 |
| BONUS_FISH:mext:pond smelt, whole | MEXT 10276 (pond smelt, whole) | 200 | 71 / 14.4 / 1.7 |
| BONUS_BANANA | USDA 173944 (Bananas, raw) | 200 | 89 / 1.1 / 0.3 |
| BONUS_TEA:mext:sencha infusion | MEXT 16037 (sencha infusion) | 600 | 2 / 0.2 / 0.0 |
| BONUS_SALT | USDA 173468 (Salt, table) | 20 | 0 / 0.0 / 0.0 |

### Results

| Measure | Value |
|---|---|
| resting expenditure | 1277.0 kcal |
| energy need (PAL x REE + caffeine) | 3085.1 kcal (caffeine 28.5 mg, +7.5 kcal) |
| energy of basal function (1.2 x REE) | 1532.4 kcal |
| starving | no |
| labour capacity (PAL reached) | 1.0 (2.416) |
| nutrient minima covered (mean) | 0.941 |
| deficient (below minimum) | thiamin, folate_dfe |
| mean adequacy ratio | 0.7204 |
| iron absorbed fraction | 0.16 (no inhibitor) |
| calcium absorbed, goods with a measured fraction | 200.5 mg (BONUS_FISH:mext:pond smelt, whole); no measured fraction: BONUS_BANANA, BONUS_RICE:polished, BONUS_SALT, BONUS_TEA:mext:sencha infusion |
| zinc absorbed (Miller) / minimum | 2.03 / 3.55 mg |
| B12 absorbed at most (3 meals x per-meal saturation) | 5.25 µg |
| protein, per meal, absorption hours at 10 and 1.3 g/h | 83.6 g, 27.9 g, [2.8, 21.4] h |
| urea capacity | 243.6 g |
| fat | 8.9 g (sweating range: False) |
| alcohol | 0.0 g a week (with fat: False) |
| water: turnover / from food / metabolic / from drinks / to draw | 5069 / 533 / 500 / 0 / 4036 ml |
| fullness (Holt index, where measured) | 1.18 over 0.058 of energy |
| repetition: goods over 5 % of energy / largest share | 2 / 0.898 |

| Good | Eaten g | Left g | Quality | Keep class (spoilage % a year; basis) |
|---|---|---|---|---|
| BONUS_RICE:polished | 759.3 | 140.7 | 0.416 | grain_granary (5; FAOstorage, traditional storage) |
| BONUS_FISH:mext:pond smelt, whole | 187.2 | 12.8 | 0.87 | fresh (100; eaten in the year it is made) |
| BONUS_BANANA | 200.0 | 0.0 | 0.631 | fresh (100; eaten in the year it is made) |
| BONUS_TEA:mext:sencha infusion | 142.6 | 457.4 | 0.565 | dried (10; stockfish keeps several years; estimate for dried fruit) |
| BONUS_SALT | 20.0 | 0.0 | 0.0 | dried (10; stockfish keeps several years; estimate for dried fruit) |

| Nutrient | Intake | Target | Minimum | Ceiling | Where it comes from (share of intake) |
|---|---|---|---|---|---|
| protein (g) | 83.564 | 97.2 | 39.0 | — | BONUS_RICE:polished 65 %, BONUS_FISH:mext:pond smelt, whole 32 % |
| sodium (mg) | 8170.327 | 7695.0 | 2721.0 | 9700.0 | BONUS_SALT 95 % |
| potassium (mg) | 1853.955 | 3000.0 | 1075.0 | — | BONUS_RICE:polished 47 %, BONUS_BANANA 39 %, BONUS_FISH:mext:pond smelt, whole 12 % |
| calcium (mg) | 1074.265 | 800 | 741 | 4000.0 | BONUS_FISH:mext:pond smelt, whole 78 %, BONUS_RICE:polished 20 % |
| magnesium (mg) | 293.68 | 362.5 | 165 | — | BONUS_RICE:polished 65 %, BONUS_BANANA 18 %, BONUS_FISH:mext:pond smelt, whole 16 % |
| iron (mg) | 8.631 | 13.45 | 8.625 | 80.0 | BONUS_RICE:polished 70 %, BONUS_FISH:mext:pond smelt, whole 20 %, BONUS_BANANA 6 % |
| zinc (mg) | 12.341 | 8.1 | — | 60.0 | BONUS_RICE:polished 67 %, BONUS_FISH:mext:pond smelt, whole 30 % |
| iodine (µg) | 54.5 | 200.0 | 54.5 | 1100.0 | BONUS_FISH:mext:pond smelt, whole 100 % |
| selenium (µg) | 157.863 | 49 | 17 | 1600.0 | BONUS_RICE:polished 73 %, BONUS_FISH:mext:pond smelt, whole 26 % |
| vit_a_rae (µg RAE) | 191.37 | 466.5 | 175.0 | 120000 | BONUS_FISH:mext:pond smelt, whole 97 % |
| thiamin (mg) | 0.612 **below minimum** | 1.234 | 0.926 | — | BONUS_RICE:polished 87 %, BONUS_BANANA 10 % |
| riboflavin (mg) | 0.851 | 1.4 | 0.5 | — | BONUS_RICE:polished 44 %, BONUS_FISH:mext:pond smelt, whole 31 %, BONUS_BANANA 17 %, BONUS_TEA:mext:sencha infusion 8 % |
| niacin_ne (mg NE) | 24.1 | 19 | 13.575 | — | BONUS_RICE:polished 60 %, BONUS_FISH:mext:pond smelt, whole 31 %, BONUS_BANANA 7 % |
| vit_b6 (mg) | 2.312 | 1.458 | 0.6 | 117.0 | BONUS_RICE:polished 54 %, BONUS_BANANA 32 %, BONUS_FISH:mext:pond smelt, whole 14 % |
| folate_dfe (µg DFE) | 100.741 **below minimum** | 400 | 300 | — | BONUS_RICE:polished 60 %, BONUS_BANANA 40 % |
| b12 (µg) | 14.792 | 5.6 | 1 | — | BONUS_FISH:mext:pond smelt, whole 100 % |
| vit_c (mg) | 27.829 | 100 | 10 | 1000.0 | BONUS_BANANA 63 %, BONUS_TEA:mext:sencha infusion 31 %, BONUS_FISH:mext:pond smelt, whole 7 % |

| Well-being list (separate from nutrition) | g | hyper-palatable | kcal per g | satiety index |
|---|---|---|---|---|
| BONUS_SALT | 20.0 | False | 0.0 | not measured |
| BONUS_TEA:mext:sencha infusion | 142.6 | False | 0.02 | not measured |
| BONUS_FISH:mext:pond smelt, whole | 187.2 | False | 0.71 | not measured |
| BONUS_BANANA | 200.0 | False | 0.89 | 118 |
| BONUS_RICE:polished | 759.3 | False | 3.65 | not measured |

