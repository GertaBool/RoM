# Fed by satiety, strong by energy and nutrients; fat limit 250 g (R46, M93)

## 1. Recorded (M93)

- **Fullness as Holt measured it stays** (option A of `round_m92.md`). Grains and tubers kept people fed: they are full. Nutrition makes people strong and healthy.
- **The baseline is satiety being met.** Ideally people get all the calories they need from the best foods.
- **The fat limit per good is raised to 250 g.**

## 2. What changed (`plan/tools/food_model.py`)

**Two measures of how well a city eats:**
```
fed      = fullness eaten ÷ (1.36 × E_need)      satiety met at the need: being fed (hunger, famine)
energy x = energy eaten ÷ E_need                  strength and work (activity, physical output)
nutrients: coverage per nutrient                  health (deficiency burden, fertility, output)
```

**Proposal for the population model:**
- **Fertility and the famine term** read `fed`: a full city is not starving.
- **The weakness of the underfed and work output** read `energy x`. A city fed on staples is full but weaker.
- **The deficiency burden** reads the nutrient coverage, as before.

**The eating order weighs what a good delivers per unit of fullness**, because fullness is the limit:
```
value per fullness unit = (1 per kcal of energy + nutrient density + well-being) ÷ satiety
```

- **Filling staples** (potatoes, bread) fill fast and deliver less per unit of fullness.
- **Milk, fruit, sugar and wine** fill little for what they deliver. So where they are available, people reach their calories from them.

## 3. The values

| Good | Satiety | Nutrition | Well-being | Value per fullness unit | Serving g |
|---|---|---|---|---|---|
| Wine | 0.70 | 0.02 | 1.47 | 3.55 | 147 |
| Alcohol | 0.83 | 0.02 | 1.27 | 2.74 | 356 |
| Dairy | 0.78 | 0.10 | 0.86 | 2.52 | 244 |
| Sugar | 1.00 | 0.01 | 1.07 | 2.08 | 4.2 |
| Banana | 1.18 | 0.04 | 1.16 | 1.86 | 126 |
| Lemon | 2.02 | 0.16 | 1.78 | 1.46 | 58 |
| Apple | 1.97 | 0.02 | 1.49 | 1.28 | 242 |
| Olives | 1.16 | 0.16 | -0.09 | 0.92 | 42 |
| Fish | 1.47 | 0.25 | 0.10 | 0.92 | 85 |
| Rice | 1.38 | 0.04 | 0.07 | 0.80 | 158 |
| Wheat | 1.57 | 0.05 | 0.13 | 0.76 | 64 |
| Clam | 2.14 | 0.27 | 0.31 | 0.74 | 85 |
| Corn | 1.65 | 0.04 | 0.13 | 0.71 | 234 |
| Horse | 1.81 | 0.17 | 0.10 | 0.70 | 85 |
| Sheep | 1.15 | 0.08 | -0.28 | 0.69 | 85 |
| Shrimp | 2.35 | 0.20 | 0.36 | 0.67 | 85 |
| Crab | 2.35 | 0.26 | 0.28 | 0.65 | 85 |
| Deer | 2.06 | 0.22 | 0.10 | 0.64 | 85 |
| Pig | 1.33 | 0.09 | -0.30 | 0.59 | 113 |
| Whale | 2.45 | 0.23 | 0.09 | 0.54 | 85 |
| Cow | 1.76 | 0.07 | -0.14 | 0.53 | 85 |
| Potato | 3.23 | 0.06 | 0.37 | 0.44 | 300 |


**A weakness I see:**
- **Beef, game and seafood rank low** per unit of fullness. Their energy counts like any other calorie, and their nutrient density score is small (beef 0.07) next to the energy term.
- **Drinks rank high** because their satiety is halved.
- **So the weight of nutrients against energy decides** whether meat counts as an "ideal food". It needs your judgement: a larger nutrient weight, or protein quality counted in, would lift meat, fish and dairy.

## 4. The cities

| City | Fed (fullness / need) | Energy x | Protein share | Vit C | Vit A | B12 | Iodine | Calcium | Work | Eaten (g/day) |
|---|---|---|---|---|---|---|---|---|---|---|
| A. Market town | 1.14 | 1.08 | 14 % | 0.10 | 0.45 | 0.73 | 0.58 | 1.17 | 1.20 | wheat 958, dairy 540, pig 79, apple 187, alcohol 408 |
| B. Coastal city | 1.22 | 1.20 | 14 % | 0.47 | 4.64 | 0.92 | 9.45 | 0.22 | 1.20 | rice 1024, fish 476, tea 8, banana 199 |
| C. Industrial city | 1.27 | 0.94 | 15 % | 1.55 | 0.54 | 1.47 | 0.79 | 1.32 | 0.80 | wheat 434, potato 1074, sugar 80, dairy 672, cow 106, coffee 8 |
| E. Rich city | 1.27 | 1.36 | 17 % | 1.28 | 2.45 | 4.58 | 3.23 | 4.78 | 1.20 | cow 179, dairy 2999, potato 477, wheat 217, apple 541, sugar 48, wine 397, tea 10 |
| F. Fishing village | 0.98 | 0.81 | 50 % | 0.51 | 15.39 | 27.47 | 31.34 | 1.58 | 0.43 | fish 1580, crab 1085 |
| G. Potato labourers | 1.13 | 0.71 | 15 % | 2.85 | 1.32 | 1.84 | 1.88 | 2.60 | 0.15 | potato 1970, dairy 1639 |
| H. Lemon groves | 0.96 | 0.84 | 19 % | 0.42 | 3.16 | 0.63 | 6.45 | 0.34 | 0.50 | lemon 66, wheat 819, fish 325 |
| D. Besieged town | 0.45 | 0.39 | 14 % | 0.00 | 0.00 | 0.07 | 0.00 | 0.14 | 0.00 | wheat 407, pig 52 |

**What the cities show:**
- **The rich city** gets its calories (energy 1.36, fed 1.27). It eats 3 L of milk, beef, potatoes, bread, apples, 48 g of sugar and wine. Before this change it filled up on potatoes at 0.87 of its energy need.
- **The potato labourers and the industrial city** are fed (1.13, 1.27) but short of energy (0.71, 0.94). They are full and weaker, as you described.
- **The fishing village,** with the fat limit at 250 g, eats 1.58 kg of whole fish and crab. It is nearly fed (0.98) and now stopped by the protein ceiling.
- **The besieged town** is neither fed (0.45) nor strong.

## 5. Open

- **The weight of nutrients against energy** in the eating order, and whether protein quality should count (section 3).
- **Whether the population model's famine and fertility terms read `fed`** and the weakness term reads energy (section 2).
