# The nutrient score error, whole animals, and the three motives shown (R47, M94)

## 1. What went wrong

**Error 1: the nutrient score was scaled wrongly** (in the model since `round_m88.md`). For each nutrient I took the amount in 100 kcal of the food and divided it by the whole day's need. 100 kcal is about 4 % of a day's energy, so no food could score much above 0.

Beef's shares were:

| Nutrient | Share (old score) |
|---|---|
| protein | 0.27 |
| B12 | 0.23 |
| zinc | 0.13 |
| iron | 0.11 |
| niacin | 0.09 |
| the rest | about 0 |

The average of these was 0.07. The low number came from my arithmetic, not from beef.

**Error 2: beef and pork were muscle only.** The liver, whose vitamin A and B12 we went through (`round_m84.md`: beef liver 4,970 µg vitamin A per 100 g, 8.7 times the daily need), was not in the Cow and Pig goods. Fish was already the whole animal (`round_m91.md`); the land animals were not.

**Error 3: in M93 I divided the preference by Holt's fullness.**
- That turned the order into energy per unit of fullness. Drinks and sugar came first, and filling foods (meat, fish, potatoes) came last.
- Well-being was still in the formula, but this division and the near-zero nutrient score hid it.
- It also contradicted M88, where you said people prefer the goods that offer the most nutrition, health and satiety.

## 2. The corrections (`plan/tools/food_model.py`)

**Nutrient density against the requirement density:**

```
for each nutrient: (amount per kcal in the food) ÷ (daily need ÷ 2,600 kcal), capped at 1
nutrition = average over protein and the 12 nutrients
```

- 1 means that every kcal of the food carries its full share of every nutrient.
- This is the requirement-density comparison used for nutrient adequacy. It replaces the per-100-kcal shares.

**Whole animals:**
- Cow and Pig are now 97 % meat and 3 % liver (USDA beef liver 169451, pork liver 167862). The 3 % is an estimate to source.
- Sheep, deer, horse and whale still lack liver records in the file.

**Preference and fullness are separate:**
- **Preference per kcal** = satisfaction + nutrition + well-being.
  - Satisfaction is the protein factor (protein share × protein quality, fitted to Holt's beef against bread): your M69 point that high-protein foods satisfy most.
  - Nutrition is the corrected score.
  - Well-being is as in `round_m91.md`.
- **Fullness** (Holt's measured index, the fitted formula elsewhere) decides only when eating stops (M92, M93). Potatoes and bread fill; they are not preferred for it.

## 3. The three motives per good

| Good | Satisfaction (protein factor) | Nutrition (0-1) | Well-being | Preference per kcal | Fullness per kcal (Holt) | Serving g |
|---|---|---|---|---|---|---|
| Shrimp | 2.29 | 0.84 | 0.36 | 3.49 | 2.35 | 85 |
| Lemon | 1.01 | 0.67 | 1.78 | 3.46 | 2.02 | 58 |
| Crab | 2.29 | 0.85 | 0.28 | 3.42 | 2.35 | 85 |
| Clam | 1.97 | 0.79 | 0.31 | 3.08 | 2.14 | 85 |
| Fish | 2.03 | 0.92 | 0.10 | 3.04 | 1.47 | 85 |
| Horse | 2.18 | 0.64 | 0.10 | 2.92 | 1.81 | 85 |
| Dairy | 1.27 | 0.79 | 0.86 | 2.92 | 0.78 | 244 |
| Deer | 2.11 | 0.65 | 0.10 | 2.87 | 2.06 | 85 |
| Apple | 0.89 | 0.46 | 1.49 | 2.85 | 1.97 | 242 |
| Whale | 1.98 | 0.72 | 0.09 | 2.78 | 2.45 | 85 |
| Banana | 0.92 | 0.58 | 1.16 | 2.66 | 1.18 | 126 |
| Wine | 0.89 | 0.29 | 1.47 | 2.64 | 0.70 | 147 |
| Alcohol | 0.92 | 0.36 | 1.27 | 2.55 | 0.83 | 356 |
| Cow | 1.76 | 0.71 | -0.14 | 2.33 | 1.76 | 85 |
| Sugar | 0.89 | 0.17 | 1.07 | 2.13 | 1.00 | 4.2 |
| Potato | 0.96 | 0.66 | 0.37 | 1.98 | 3.23 | 300 |
| Wheat | 1.00 | 0.55 | 0.13 | 1.68 | 1.57 | 64 |
| Sheep | 1.25 | 0.67 | -0.28 | 1.64 | 1.15 | 85 |
| Corn | 0.95 | 0.52 | 0.13 | 1.60 | 1.65 | 234 |
| Pig | 1.12 | 0.77 | -0.30 | 1.60 | 1.33 | 113 |
| Rice | 0.96 | 0.48 | 0.07 | 1.51 | 1.38 | 158 |
| Olives | 0.91 | 0.39 | -0.09 | 1.20 | 1.16 | 42 |


**Reading the table:**
- **Seafood, fish, game, dairy and beef** score 0.64-0.92 on nutrition and the highest on satisfaction.
- **Fruit, wine, beer and sugar** score highest on well-being.
- **Potatoes and grains** score high on fullness and middling on the rest.
- **Beef and pork** lose some well-being to their fat (heaviness after fatty meals, Wells et al. 1997). That is why beef ranks below fish and dairy.

## 4. The cities

| City | Fed (fullness / need) | Energy x | Protein share | Vit C | Vit A | B12 | Iodine | Calcium | Iron | Work | Eaten (g/day) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A. Market town | 1.14 | 1.08 | 14 % | 0.11 | 0.72 | 0.89 | 0.58 | 1.17 | 3.19 | 1.20 | wheat 958, dairy 540, pig 79, apple 187, alcohol 408 |
| B. Coastal city | 1.22 | 1.20 | 14 % | 0.47 | 4.64 | 0.92 | 9.45 | 0.22 | 2.26 | 1.20 | rice 1024, fish 476, tea 8, banana 199 |
| C. Industrial city | 1.27 | 0.81 | 15 % | 2.18 | 0.82 | 1.92 | 0.82 | 1.23 | 1.96 | 0.29 | wheat 261, potato 1507, sugar 24, dairy 672, cow 106, coffee 8 |
| E. Rich city | 1.36 | 1.08 | 18 % | 1.99 | 1.94 | 5.13 | 1.41 | 2.16 | 2.83 | 1.20 | cow 340, dairy 1262, potato 970, wheat 164, apple 541, sugar 16, wine 397, tea 10 |
| F. Fishing village | 0.98 | 0.81 | 50 % | 0.51 | 15.39 | 27.47 | 31.34 | 1.58 | 2.47 | 0.43 | fish 1580, crab 1085 |
| G. Potato labourers | 1.13 | 0.71 | 15 % | 2.85 | 1.32 | 1.84 | 1.88 | 2.60 | 1.04 | 0.15 | potato 1970, dairy 1639 |
| H. Lemon groves | 0.96 | 0.84 | 19 % | 0.42 | 3.16 | 0.63 | 6.45 | 0.34 | 3.01 | 0.50 | lemon 66, wheat 819, fish 325 |
| D. Besieged town | 0.45 | 0.39 | 14 % | 0.01 | 0.18 | 0.17 | 0.00 | 0.14 | 1.28 | 0.00 | wheat 407, pig 52 |

**What the cities show:**
- **The rich city:** beef 340 g, milk 1.3 L, potatoes 970 g, bread grain 164 g, apples, sugar and wine. It is fed (1.36) and gets its energy (1.08). Vitamin A, B12 and calcium are all covered with room to spare.
- **The market town** gains vitamin A (0.72 against 0.45) and B12 from the pork liver.
- **The industrial city and the potato labourers** are full on potatoes but short of energy (0.81, 0.71): fed, not strong.
- **The fishing village** is unchanged, held by the protein ceiling.

## 5. Open

- The liver share of the whole animal, and liver data for sheep, deer, horse and whale.
- The weights: satisfaction, nutrition and well-being count equally now.
