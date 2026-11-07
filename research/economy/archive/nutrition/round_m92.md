# Appetite by fullness, the fat heuristic, and a lemon limit (R45, M92)

## 1. Recorded (M92)

- **Appetite is gauged by fullness:** people eat until they feel full, counted in satiety units. Calories stay part of the equation: food sufficiency `x` is still energy eaten against energy need.
- **The 100 g fat per good stays** as a heuristic for the usual maximum of a good, not as a physiological law.
- **Lemons have an upper limit:** no one eats kilograms of lemons.

## 2. What changed in the model (`plan/tools/food_model.py`)

```
fullness eaten   = Σ kcal eaten × satiety of the good            (satiety units: white-bread kcal)
fullness capacity = 1.36 × E_max                                  1.36 = mean of Holt's 38 satiety values;
                                                                  a person eating average foods is full at PAL 2.40
eating stops when fullness reaches the capacity, or energy reaches E_max, or no good is left within its limits
lemons           ≤ 116 g a day (two lemons, USDA serving 58 g; the number is an estimate)
```

All other parts are unchanged from `round_m91.md`:
- one allocation with diminishing returns;
- the hydration equation;
- the whole fish;
- the ceilings for protein, fat per good, milk and fruit.

## 3. Results: fullness as Holt measured it, against two alternatives

| City | x, fullness as Holt (A) | x, fullness damped (B, satiety^0.5) | x, energy ceiling only (M91) |
|---|---|---|---|
| A. Market town | 1.08 (3440 kcal) | 1.08 (3440 kcal) | 1.08 (3440 kcal) |
| B. Coastal city | 1.20 (3620 kcal) | 1.20 (3620 kcal) | 1.20 (3620 kcal) |
| C. Industrial city | 0.78 (2260 kcal) | 1.07 (3120 kcal) | 1.23 (3580 kcal) |
| E. Rich city | 0.87 (2370 kcal) | 1.16 (3170 kcal) | 1.36 (3710 kcal) |
| F. Fishing village | 0.68 (2170 kcal) | 0.68 (2170 kcal) | 0.68 (2170 kcal) |
| G. Potato labourers | 0.58 (1880 kcal) | 0.84 (2730 kcal) | 1.13 (3690 kcal) |
| H. Lemon groves | 0.84 (2630 kcal) | 0.84 (2630 kcal) | 0.84 (2630 kcal) |
| D. Besieged town | 0.39 (1260 kcal) | 0.39 (1260 kcal) | 0.39 (1260 kcal) |

**What the table shows:**
- **Where food is short (A, B, D, F, H),** the gauge makes no difference. Everything available within the limits is eaten.
- **Where potatoes are plentiful (C, E, G),** fullness as Holt measured it stops people at 58-87 % of their energy need. Boiled potatoes score 323, more than three times white bread, so a potato diet fills a person long before it feeds them.
- **Holt's index measures fullness over two hours after a single 240 kcal serving.** The model uses it for a whole day. Whether people living on potatoes ate more than that is the question. I found no quantitative source on historical potato intake in PubMed in this round.
- **The fishing village** is held by the fat heuristic (1.26 kg of whole fish holds 100 g fat), not by fullness. It reaches 3,638 of 5,011 fullness units.
- **The lemon groves** eat 67 g of lemons a day (the allocation stops short of the 116 g limit) and fill up on bread and fish.

**Options:**
- **A.** Fullness as Holt measured it (now in the model). Plentiful potatoes leave people full but underfed.
- **B.** Fullness per kcal = satiety^0.5: the filling effect counts, but less than over two hours. The exponent is an estimate; a source on daily intake of very filling foods would set it.
- **C.** Energy as the ceiling and satiety only in the eating order (the model before M92).

## 4. The cities under option A (as now in the model)

#### A. Market town, 20,000; 70 % vigorous, 20 % active, 10 % sedentary
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Wheat | 7,000 | 959 | 958 | 6 | 0 |
| Dairy | 4,000 | 548 | 541 | 51 | 51 |
| Pig | 600 | 82 | 80 | 18 | 18 |
| Apple | 1,500 | 205 | 188 | 131 | 131 |
| Alcohol | 3,000 | 411 | 408 | 20 | 3 |
| Salt | 60 | 8 | 8 | 0 | 0 |

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4965 / 5011 | 3193 | 3685 | 3440 | 1.08 | 122 (14 %) | 314 | 1219 | 716 | 0 | 2.24 | 1.20 |

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

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5028 / 5035 | 3025 | 3702 | 3620 | 1.20 | 129 (14 %) | 599 | 353 | 1296 | 70 | 2.36 | 1.20 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.47 | 4.64 | 7.62 | 5.42 | 1.22 | 0.92 | 2.26 | 2.58 | 0.22 | 9.45 | 1.42 | 4.88 |

#### C. Industrial city, 1,000,000; 40 % vigorous, 30 % active, 30 % sedentary
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Wheat | 220,000 | 603 | 198 | 147,601 | 7,380 |
| Potato | 600,000 | 1644 | 1642 | 746 | 373 |
| Sugar | 30,000 | 82 | 16 | 24,129 | 2,413 |
| Dairy | 250,000 | 685 | 672 | 4,672 | 4,672 |
| Cow | 40,000 | 110 | 107 | 1,067 | 1,067 |
| Coffee | 3,000 | 8 | 8 | 0 | 0 |
| Salt | 3,000 | 8 | 8 | 0 | 0 |

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5044 / 5037 | 2916 | 3703 | 2260 | 0.78 | 87 (15 %) | 1345 | 1131 | 0 | 73 | 1.47 | 0.15 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.37 | 0.54 | 3.52 | 2.60 | 1.06 | 1.47 | 1.79 | 1.66 | 1.22 | 0.83 | 2.28 | 6.02 |

#### E. Rich city, 100,000, everything in surplus; 20 % vigorous, 40 % active, 40 % sedentary
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Cow | 20,000 | 548 | 153 | 14,403 | 14,403 |
| Dairy | 150,000 | 4110 | 443 | 133,844 | 133,844 |
| Potato | 60,000 | 1644 | 1478 | 6,067 | 3,034 |
| Wheat | 40,000 | 1096 | 120 | 35,629 | 1,781 |
| Apple | 20,000 | 548 | 542 | 229 | 229 |
| Sugar | 8,000 | 219 | 11 | 7,609 | 761 |
| Wine | 15,000 | 411 | 382 | 1,044 | 157 |
| Tea | 400 | 11 | 11 | 0 | 0 |
| Salt | 500 | 14 | 10 | 135 | 14 |

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5048 / 5043 | 2735 | 3708 | 2370 | 0.87 | 78 (13 %) | 1701 | 1517 | 0 | 94 | 1.54 | 0.39 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.73 | 0.39 | 3.08 | 2.40 | 0.95 | 1.52 | 1.97 | 1.60 | 0.92 | 0.57 | 2.30 | 7.08 |

#### F. Fishing village, 5,000, fish (whole animal) and crab in plenty; 70 % vigorous
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Fish | 6,000 | 3288 | 1255 | 3,709 | 3,709 |
| Crab | 2,000 | 1096 | 1085 | 20 | 20 |
| Salt | 15 | 8 | 8 | 0 | 0 |

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3638 / 5011 | 3193 | 3685 | 2170 | 0.68 | 276 (51 %) | 1723 | 0 | 526 | 0 | 1.41 | 0.02 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.48 | 12.23 | 2.15 | 3.64 | 2.21 | 26.84 | 2.27 | 4.65 | 1.52 | 24.89 | 2.28 | 11.57 |

#### G. Potato labourers, 10,000, potatoes and milk in plenty; 80 % vigorous
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Potato | 30,000 | 8219 | 2164 | 22,101 | 11,050 |
| Dairy | 6,000 | 1644 | 705 | 3,427 | 3,427 |
| Salt | 30 | 8 | 8 | 0 | 0 |

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5016 / 5011 | 3269 | 3685 | 1880 | 0.58 | 57 (12 %) | 1666 | 1057 | 0 | 0 | 1.40 | 0.00 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3.13 | 0.57 | 3.36 | 2.25 | 1.01 | 0.79 | 0.96 | 0.98 | 1.21 | 0.90 | 2.61 | 5.96 |

#### H. Lemon groves, 5,000, lemons, wheat and fish
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Lemon | 6,000 | 3288 | 67 | 5,878 | 5,878 |
| Wheat | 1,500 | 822 | 820 | 4 | 0 |
| Fish | 600 | 329 | 325 | 7 | 7 |
| Salt | 15 | 8 | 8 | 0 | 0 |

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4090 / 5011 | 3118 | 3685 | 2630 | 0.84 | 125 (19 %) | 369 | 0 | 1880 | 0 | 1.71 | 0.50 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.42 | 3.16 | 3.52 | 2.95 | 1.10 | 0.63 | 3.01 | 2.01 | 0.34 | 6.45 | 1.03 | 5.58 |

#### D. Besieged town, 20,000, grain and salt pork only
| Good | Stock t | Per head g/day | Eaten g/day | Left t | Spoiled t |
|---|---|---|---|---|---|
| Wheat | 3,000 | 411 | 408 | 22 | 1 |
| Pig | 400 | 55 | 52 | 19 | 19 |
| Salt | 60 | 8 | 8 | 0 | 0 |

| Fullness eaten / capacity | Need kcal | Ceiling kcal | Eaten kcal | x | Protein g (share) | Water from food ml | from drinks ml | plain water ml | Caffeine mg | PAL | Work |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1937 / 5011 | 3193 | 3685 | 1260 | 0.39 | 45 (14 %) | 77 | 0 | 2172 | 0 | 1.40 | 0.00 |

| C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 0.00 | 2.20 | 1.43 | 0.50 | 0.07 | 1.24 | 1.03 | 0.14 | 0.00 | 0.39 | 5.36 |

## 5. Open

- Option A, B or C for fullness, and a source on daily intake of very filling foods (potatoes).
- The lemon limit (two a day is an estimate); other goods with a usual maximum.
