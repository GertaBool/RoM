# Nutrition and well-being as two sorted lists (R49, M96; specification version 2)

## 1. The change (`food_model_spec.md`, change log rows M96)

| Variable | Before (version 1) | After (version 2) |
|---|---|---|
| preference `V_g` | one key: satisfaction + nutrient density + well-being | removed |
| nutrition key `N_g` | — | satisfaction + nutrient density (E16) |
| well-being key `β_g` | added into `V_g` | its own key, its own sorted list (E16) |
| allocation | one pass on `V_g` | pass 1 on the nutrition list until the people are fed (fullness = 1.36 × need); pass 2 on the well-being list from there up to the fullness capacity (E17) |

Nothing else changed:
- the ceilings;
- the satiety (fullness) values;
- the nutrient density;
- the well-being formula;
- the water equation;
- the whole animals.

**Why:** you said nutrition and well-being are two separate variables and two separate sorted lists. In M88 you described the order: the best goods by nutrition, health and satiety first, then other things, "steak and potatoes, then dessert". My merging them into one sum in M91 was the error.

**Each good is on both lists.** Its ceiling (fat, milk, fruit, lemons, stock) is shared between the two passes.

## 2. The two lists, and the cities

Nutrition list (E16: satisfaction + nutrient density):
| Rank | Good | Satisfaction | Nutrient density | Key N_g | Fullness per kcal |
|---|---|---|---|---|---|
| 1 | Crab | 2.29 | 0.85 | 3.14 | 2.35 |
| 2 | Shrimp | 2.29 | 0.84 | 3.13 | 2.35 |
| 3 | Fish | 2.03 | 0.92 | 2.94 | 1.47 |
| 4 | Horse | 2.18 | 0.64 | 2.82 | 1.81 |
| 5 | Clam | 1.97 | 0.79 | 2.77 | 2.14 |
| 6 | Deer | 2.11 | 0.65 | 2.77 | 2.06 |
| 7 | Whale | 1.98 | 0.72 | 2.70 | 2.45 |
| 8 | Cow | 1.76 | 0.71 | 2.47 | 1.76 |
| 9 | Dairy | 1.27 | 0.79 | 2.06 | 0.78 |
| 10 | Sheep | 1.25 | 0.67 | 1.92 | 1.15 |
| 11 | Pig | 1.12 | 0.77 | 1.89 | 1.33 |
| 12 | Lemon | 1.01 | 0.67 | 1.68 | 2.02 |
| 13 | Potato | 0.96 | 0.66 | 1.62 | 3.23 |
| 14 | Wheat | 1.00 | 0.55 | 1.55 | 1.57 |
| 15 | Banana | 0.92 | 0.58 | 1.50 | 1.18 |
| 16 | Corn | 0.95 | 0.52 | 1.47 | 1.65 |
| 17 | Rice | 0.96 | 0.48 | 1.44 | 1.38 |
| 18 | Apple | 0.89 | 0.46 | 1.35 | 1.97 |
| 19 | Olives | 0.91 | 0.39 | 1.30 | 1.16 |
| 20 | Alcohol | 0.92 | 0.36 | 1.28 | 0.83 |
| 21 | Wine | 0.89 | 0.29 | 1.18 | 0.70 |
| 22 | Sugar | 0.89 | 0.17 | 1.06 | 1.00 |

Well-being list (E16: key beta_g; only goods above 0 are taken in pass 2):
| Rank | Good | Well-being |
|---|---|---|
| 1 | Lemon | 1.78 |
| 2 | Apple | 1.49 |
| 3 | Wine | 1.47 |
| 4 | Alcohol | 1.27 |
| 5 | Banana | 1.16 |
| 6 | Sugar | 1.07 |
| 7 | Dairy | 0.86 |
| 8 | Potato | 0.37 |
| 9 | Shrimp | 0.36 |
| 10 | Clam | 0.31 |
| 11 | Crab | 0.28 |
| 12 | Wheat | 0.13 |
| 13 | Corn | 0.13 |
| 14 | Horse | 0.10 |
| 15 | Deer | 0.10 |
| 16 | Fish | 0.10 |
| 17 | Whale | 0.09 |
| 18 | Rice | 0.07 |
| 19 | Olives | -0.09 |
| 20 | Cow | -0.14 |
| 21 | Sheep | -0.28 |
| 22 | Pig | -0.30 |


| City | Fed | Energy x | Vit C | Vit A | B12 | Iodine | Calcium | Work | Pass 1 (nutrition list), g/day | Pass 2 (well-being list), g/day |
|---|---|---|---|---|---|---|---|---|---|---|
| A. Market town | 1.14 | 1.08 | 0.11 | 0.72 | 0.89 | 0.58 | 1.17 | 1.20 | dairy 540, pig 79, apple 187, alcohol 408 | wheat 958 (both) |
| B. Coastal city | 1.22 | 1.20 | 0.47 | 4.64 | 0.92 | 9.45 | 0.22 | 1.20 | fish 476, banana 199 | rice 1024 (both) |
| C. Industrial city | 1.28 | 0.84 | 2.18 | 0.82 | 1.92 | 0.82 | 1.27 | 0.39 | wheat 224, dairy 672, cow 106 | potato 1507 (both), sugar 69 (both) |
| E. Rich city | 1.36 | 1.21 | 1.82 | 2.46 | 5.82 | 2.12 | 3.18 | 1.20 | cow 333, wheat 134 | dairy 1934 (both), potato 850 (both), apple 541 (both), sugar 42 (both), wine 397 (both) |
| F. Fishing village | 0.98 | 0.81 | 0.51 | 15.39 | 27.47 | 31.34 | 1.58 | 0.43 | fish 1580, crab 1085 | - |
| G. Potato labourers | 1.13 | 0.71 | 2.85 | 1.32 | 1.84 | 1.88 | 2.60 | 0.15 | dairy 1639 | potato 1970 (both) |
| H. Lemon groves | 0.96 | 0.84 | 0.42 | 3.16 | 0.63 | 6.45 | 0.34 | 0.50 | lemon 66, wheat 819, fish 325 | - |
| D. Besieged town | 0.45 | 0.39 | 0.01 | 0.18 | 0.17 | 0.00 | 0.14 | 0.00 | wheat 407, pig 52 | - |

**What the cities show:**
- **Pass 1 (nutrition list):** seafood, fish, game, beef, milk and pork come first wherever there is any, then the staples.
- **Pass 2 (well-being list):** starts once the people are fed. The rich city then takes milk, potatoes, apples, sugar and wine. It ends fed (1.36), with its energy met (1.21) and its vitamins covered.
- **Cities whose stock runs out in pass 1** (the fishing village, the lemon groves, the besieged town) never reach pass 2. They eat everything they have by nutrition.
- **In the market town and the coastal city,** the people are fed during pass 1. The rest of the bread and rice is then taken in pass 2, because grains have a small positive well-being (lightness).

## 3. Open

- Whether pass 2 should take only goods with a clearly positive well-being (for example above 0.5: fruit, wine, beer, sugar, milk) instead of every good above 0.
