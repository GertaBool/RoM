# Your answers, one deficiency model, and the population model in depth (R37, M83)

## 1. Recorded as you said it (M83)

| Topic | Your answer |
|---|---|
| Turn away from food now? | "Wait a second": not yet |
| Flax | a base good |
| Meat | depends on the livestock and deer the city has |
| Cloth, Fine Cloth, Coats, Dresses | made from base-good inputs |
| Charcoal | made from timber; a fuel good |
| Steel | made from ores; an industrial good |
| Machinery, tools, arms | manufactured goods; tools and arms can also be artisanal goods, especially early |
| Fast food, stones | a general comment on how health works, not a good |
| Clothing "per citizen" | per real person |
| "No building per step" | no building for each artisanal or industrial step ("Trinketmaker", "Sand gatherer"). The city itself makes most goods from the techs, buildings, infrastructure and people it already has. Reasons: what the game must consider and render, and clicking 200 buildings across fifty cities is no fun |
| Guild luxuries | probably none; other ideas welcome |
| Ancient Temples, thermal vents | outside the goods economy; volcanic activity matters for energy and electricity |
| Tea | many teas carry real value against deficiency diseases |
| Wine | a luxury good; the vineyard's good counts as a kind of food |
| Whale | minor; mostly for the Japanese and other cultures; blubber for lamps (and perfume) |
| Deficiencies | one efficient model over all nutrients and all food sources |
| Population model | discussed again in full depth, mathematically (section 4); you liked the fourth version, it may not be complete |

**Two notes on these, from the sources:**
- **Tea: you are right for green tea.** The USDA measures 0 mg of vitamin C in brewed black and green tea (`round_m82.md`). The Japanese food tables (MEXT, 8th edition, 2023 supplement) measure vitamin C, in mg per 100 g:
  - gyokuro infusion 19;
  - sencha infusion 6;
  - kamairi infusion 4;
  - bancha infusion 3;
  - black tea infusion 0.
  
  Matcha, where the whole leaf is drunk, has 60 per 100 g of powder, with vitamin A, iron and folate. So 600 g of sencha a day gives 36 mg, more than three times the 10 mg that prevents scurvy. `round_m82.md` is corrected by this.
- **Whale blubber: lamps, yes; perfume comes from elsewhere.** As far as I know, the perfume material is ambergris from the sperm whale's gut, and spermaceti (from its head) made candles. I have no fetched source for this yet, so it stays to be checked. The MEXT tables also give whale as food: red meat 24 g protein, 2.5 mg iron and 2.0 µg B12 per 100 g; skin (honkawa) 5 mg vitamin C and 130 µg vitamin A.

## 2. One deficiency model for all nutrients

### 2a. The data (sources and files)

- **What each good holds:** `data/nutrient_profiles.json`, written by `plan/tools/nutrient_profile.py`:
  - **USDA SR Legacy** (fdc ids), per 100 g: protein; vitamins C, A, D, B1 (thiamin), B2, B3 (niacin), folate and B12; iron, zinc, calcium, magnesium, potassium, sodium and selenium;
  - **MEXT**: iodine (SR Legacy holds none for these foods), tea infusions, whale.
- **What a person needs a day:** `data/nutrient_needs.json`:
  - EFSA 2017 average requirements or adequate intakes for an adult man of 68.1 kg;
  - the Japanese reference intakes 2025 for sodium: 600 mg, the unavoidable losses plus variation, for an adult who does not sweat. Heavy sweating in heat or labour loses a corresponding amount more.
- **How much of the iron in food is absorbed** (FAO/WHO 2004, chapter 13):
  - about 15 % in a good Western diet;
  - 18 % with very high meat intake;
  - 10-12 % with less meat and fish;
  - low in vegetarian diets.
  
  Meat, vitamin C with meals and little phytate-rich cereal raise it; tea or coffee with meals lowers it. EFSA's zinc requirement rises from 7.5 mg (300 mg phytate a day) to 12.7 mg (1,200 mg).

### 2b. What diets cover (computed by `plan/tools/diet_coverage.py`)

The figures are shares of the daily need: 1.00 means the need is met. The single-food rows eat that food up to 2,600 kcal. The mixed diets are constructed examples to show the arithmetic, not historical records. Iron is shown before absorption against EFSA's figure, which assumes 16 % absorption. A value marked ≥ leaves out foods with no iodine value. Vitamin C is measured against EFSA's 90 mg; the scurvy floor of 10 mg is 0.11 on this scale.

| diet | kcal | prot | C | A | B1 | B3 | fol | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wheat only | 2600 | 2.23 | 0.00 | 0.00 | 3.90 | 3.08 | 1.21 | 0.00 | 4.23 | 2.27 | 0.31 | 0.00 | 0.82 | 0.03 |
| polished rice only | 2600 | 1.13 | 0.00 | 0.00 | 0.64 | 0.81 | 0.23 | 0.00 | 0.95 | 0.83 | 0.27 | 0.00 | 0.23 | 0.06 |
| brown rice only | 2600 | 1.19 | 0.00 | 0.00 | 4.91 | 3.26 | 0.65 | 0.00 | 1.52 | 1.62 | 0.09 | 0.00 | 0.51 | 0.06 |
| maize only | 2600 | 1.49 | 0.00 | 0.14 | 3.52 | 1.83 | 0.54 | 0.00 | 3.22 | 1.69 | 0.07 | 0.00 | 0.58 | 0.42 |
| potato only | 2600 | 1.24 | 4.32 | 0.00 | 4.06 | 3.05 | 1.20 | 0.00 | 1.54 | 0.96 | 0.20 | 0.20 | 3.24 | 0.20 |
| beef only | 2600 | 3.44 | 0.00 | 0.00 | 0.92 | 2.24 | 0.25 | 5.96 | 2.73 | 3.43 | 0.10 | 0.00 | 0.68 | 0.88 |
| milk only | 2600 | 2.98 | 0.00 | 3.44 | 2.51 | 0.27 | 0.85 | 4.80 | 0.21 | 1.70 | 6.42 | 4.55 | 1.61 | 3.05 |
| cod only | 2599 | 12.55 | 0.35 | 0.67 | 3.09 | 4.64 | 0.89 | 7.21 | 2.01 | 1.53 | 0.68 | 73.98 | 3.74 | 2.85 |
| sailor: grain, salt pork, beer | 2659 | 2.82 | 0.02 | 0.01 | 5.98 | 3.28 | 1.01 | 0.45 | 3.09 | 2.00 | 0.32 | ≥0.02 | 0.90 | 6.79 |
| grain farmer | 2573 | 2.14 | 0.81 | 0.26 | 3.56 | 2.75 | 1.51 | 0.36 | 3.65 | 2.02 | 0.84 | ≥0.32 | 0.92 | 3.56 |
| herder | 2624 | 2.97 | 0.00 | 1.62 | 2.73 | 1.37 | 0.60 | 4.25 | 1.92 | 2.39 | 3.11 | ≥2.13 | 1.18 | 1.76 |
| coastal: rice, fish, green tea | 2296 | 2.55 | 1.69 | 0.10 | 4.13 | 3.01 | 0.99 | 0.91 | 1.56 | 1.37 | 0.27 | 9.35 | 1.23 | 3.72 |
| varied | 2605 | 2.63 | 1.18 | 0.70 | 3.38 | 2.31 | 2.31 | 4.54 | 3.48 | 2.02 | 0.86 | ≥0.61 | 1.24 | 2.82 |

Grams per day in the mixed diets:
- **Sailor:** wheat 500, pork 300, beer 1,000, salt 10.
- **Grain farmer:** wheat 650, cabbage 200, milk 300, beer 500, salt 5.
- **Herder:** milk 2,000, beef 300, barley 150.
- **Coastal:** brown rice 450, cod 400, boiled potato 300, cabbage 200, sencha 600, salt 5.
- **Varied:** wheat 350, boiled potato 300, beef 100, milk 300, egg 50, cabbage 150, apple 200, herring 100, lentils 60, butter 20, salt 3.

**What the table shows:**
- **No single food covers everything.**
  - Grains and meat lack vitamin C and vitamin A.
  - Plants lack B12.
  - Inland foods lack iodine. MEXT's cod has 350 µg per 100 g; grain and land meat have 0 or a trace.
  - Milk lacks iron.
- **Polished rice falls short in almost everything,** thiamin included (0.64), against 4.91 for brown rice. That matches beriberi on polished rice (`pop_model_math.md` section 3).
- **The sailor's diet** has vitamin C 0.02 and vitamin A 0.01, with plenty of energy, protein and salt. That is the scurvy diet of `round_m82.md`.
- **Sodium:** grain alone gives 0.03 of the need, and milk and meat give more (0.88 to 3.05). A grain diet needs salt; a herding diet hardly does. Potassium is high in potatoes (3.24) and low in grain and rice.
- **What the data cannot show:**
  - Iron absorption: plant iron is absorbed at a lower rate (above).
  - Bound niacin in maize, the cause of pellagra. To be sourced; the niacin and NIH pages refused automated access.
  - Iodine in plants, which follows the soil.

### 2c. The model

**One vector per good, one coverage per nutrient.** Let `q_g` be the grams of good `g` eaten per person a day, `n_{g,i}` the amount of nutrient `i` in 100 g of it, `r_{f,i}` what remains of nutrient `i` after storage and preparation in form `f`, and `a_i` the share absorbed:

```
intake_i   = Σ_g q_g / 100 × n_{g,i} × r_{f,i}
coverage_i = min(1, a_i × intake_i / (a_ref_i × need_i))
```

- **Absorption** (`a_i`) matters for iron and zinc only. The others are measured as absorbed in the requirement.
  - Iron: `a_Fe` = 0.10 + 0.08 × (animal share of protein). This passes through FAO's 10 % for little meat and 18 % for very high meat intake; the straight line between them is my estimate. EFSA's need assumes 0.16.
  - Zinc: the need follows the phytate of the diet (EFSA's table), and phytate comes from whole grains and pulses. Phytate values per good are open.
- **Losses** (`r`): cooking takes about 60 % of the vitamin C of vegetables. Drying, salting and long storage take more. The values per form are open (PR.F8.T5).
- **Stores carry the time.** Each nutrient has a store `S_i` in days of need, filled by surplus and drawn by shortfall:
  - `S_i(t+1) = min(S_max_i, S_i(t) + coverage_i − 1)`;
  - deficiency begins only when `S_i` reaches 0.
  - Vitamin C has at least a month (Wikipedia). The others are open: liver stores of vitamin A and B12 last much longer.
  
  This is what lets a voyage, a siege or a winter without fresh food cause disease while a varied year does not. With turns of a year or more, it matters for units away from home and for seasons.
- **Effects.** Three effects per nutrient, from a small table `W` (nutrients × effects):

| Effect | Formula | Where it acts |
|---|---|---|
| health burden | `D_DEF × Σ_i w_health,i × (1 − c_i)` | `pop_model_math.md` section 3 (deficiency diseases) |
| fertility | `× (1 − Σ_i w_fert,i × (1 − c_i))` | section 2 (the nutrients factor) |
| output | `× (1 − Σ_i w_out,i × (1 − c_i))` | work (iron, energy), science and culture (iodine), section 6 |

- **Weights to set** (with the evidence at hand):
  - vitamin C: health (scurvy);
  - thiamin: health (beriberi, 27,000 deaths in 211,600 cases);
  - niacin: health (pellagra);
  - iodine: output, cognition (10-15 IQ points);
  - iron: output, work;
  - vitamin A: health, child deaths;
  - protein: unit strength (D27).
  
  The sizes are estimates to calibrate against the cases in sections 3 and 4.

**Electrolytes:**
- Sodium and potassium enter as nutrients like the others.
- **Salt as a need:** salt per person a day = (sodium need + sweat losses − sodium in the food) ÷ 0.39, since salt is 39 % sodium. Then add the salt used for preserving (D27). From the table: a grain city needs salt, a herding or fishing city much less.
- **Water** (D31) and hydration (FD.drink) stay as decided.

*(M84: the upper band is withdrawn; food above need is surplus and goes to storage, and fat quality is context only. See `round_m84.md` section 1. The coverage reading above is corrected in `round_m84.md` section 2: liver is rich in vitamin A, and milk gives iodine inland.)*

**Excess, the general comment on health (withdrawn, M84):** the same model takes an upper band. Above a safe level, a nutrient or a harm raises the burden: sodium above the band raises blood pressure; sugar and fat above their bands, "fast food", raise the burden of the diseases of plenty. Bladder stones go with plain grain diets. So health is a band for each nutrient: too little harms, and too much harms.

**Why this is efficient:**
- One vector per good, about 13 numbers, read from USDA and MEXT.
- One store per nutrient per city.
- One small weight table.
- All in integer arithmetic.
- Fruit, tea, sea food, milk, meat and salt each help where their vector is strong; no good needs a special rule.

## 3. Wine, tea and whale in the goods

- **Wine:**
  - The vineyard gives grapes, a fruit, eaten fresh or dried as raisins: 3.2 mg vitamin C, 191 mg potassium per 100 g fresh.
  - Wine is a luxury good made from the grapes. It is a drink with calories (85 kcal per 100 g red) and, as a luxury, happiness.
- **Tea:**
  - A drink (FD.drink). Its value depends on the kind and how it is drunk: green infusions carry vitamin C and folate; black tea carries next to none; whole-leaf matcha carries much more.
  - **Proposal:** the Tea good stands for the green and black teas of its region, with one vector per kind by the culture's custom.
  - Tea with meals lowers iron absorption (FAO).
- **Whale:**
  - Food (meat, skin) for the cultures that eat it.
  - Oil for lamps.
  - A minor good, as you said.

## 4. The population model in depth

### 4a. The equations, every variable named

**The bookkeeping.** For each city, each year:
```
N(t+1) = min( N(t) + N(t) × g(t) / 1000 + M_in − M_out ,  F / (m × K) )
g      = b − h                                   (per 1,000 a year)
x      = F / (K × N)                             food sufficiency: satiety units per head ÷ need
```
- `F`: the city's food in satiety units a year.
- `K`: the need per head, 2,600 a day.
- `m`: the biological minimum, 1,500 of 2,600 (the starvation cap).
- `M_in`, `M_out`: migration (D33).

**Fertility** `b = B(x) × f_nut × f_econ × f_urb × f_rel × f_edu × f_safe`:
- `B(x) = 30 + 15 × min(x − 0.9, 0.4) / 0.4` for x ≥ 0.9.
- `B(x) = 30 × (x − m) / (0.9 − m)` below 0.9.

**Health burden:**
```
h = D(med) × (2 − H) + 12 × clamp((1.3 − x)/0.4) + 200 × max(0, 1 − x) + D_DEF × Σ w (1 − c) + 13 × U + 25 × W
```
- `D(med)`: 22 falling to 8 with medicine.
- `H`: the health balance, 0 to 1.
- `c`: coverage per nutrient (section 2).
- `U`: the share in unsanitized dense quarters.
- `W`: war pressure.

**What each input reads from the game:**

| Input | Read from | Status |
|---|---|---|
| F | the goods pass: food eaten, by satiety (FD.F1) | designed |
| c_i | section 2 | proposed here |
| H | the engine's health: good and bad health of the city | mapping open (proposal 4) |
| med | techs: Medicine, Modern Sanitation, Modern Health Care | to list |
| f_econ | food prices against wages, employment | after the goods economy |
| f_urb, U | urban share, density, sewer and water level | definition open (proposal 5) |
| f_rel | state religion, religious and secular civics | to list |
| f_edu | education civics and techs | to list |
| f_safe, W | enemy units in the city's plots, sieges, pillage | to define |

### 4b. What the equations imply (computed with `pop_model_sim.py`)

**The balance point:** fertility equals the burden at the food sufficiency `x*`:

| Setting | x* | fertility = burden |
|---|---|---|
| baseline | 0.99 | 33.4 |
| full medicine | 0.94 | 31.4 |
| full medicine and education | 1.12 | 13.4 |
| education at half | 1.15 | 26.6 |
| religious (× 1.1) | 0.98 | 36.2 |
| secular (× 0.9) | 1.01 | 30.7 |
| health balance at half | 1.12 | 38.4 |
| nutrient coverage 0.6 | 1.09 | 34.3 |
| all unsanitized and urban | 1.28 | 35.5 |
| full medicine, all urban, sanitized | 0.96 | 25.9 |
| permanent full war | none | births never reach the burden |

**What this says (a reading of the model, not of history):**
- **Better health gives more people, not better-fed people,** while fertility stays high. Medicine moves `x*` down from 0.99 to 0.94; bad health moves it up to 1.12. Clark argues this for the Malthusian era: anything that raises deaths raises income per head (the Black Death). Only education, town life and secularization (lower fertility) raise food per head at the balance: 1.12-1.15.
- **Unsanitized big cities hold only when very well fed** (x* 1.28) or with migrants. That matches London needing about 8,000 migrants a year.
- **Permanent war has no balance;** the city empties. A war that ends recovers (case 7).

**How fast it returns to balance:** near `x*`, growth falls by the slope of fertility plus the slope of the burden for each step in `x`.
- **Below** `x*` the famine term adds 200: the slope is about 37.5 + 30 + 200 per 1,000. A shortfall closes within a few years.
- **Above** it, the slope is about 67.5 per 1,000. A surplus is filled at about 7 % of the gap a year, so it takes about ten years to halve.
- Both are below 1 per yearly step, so there is no overshoot or oscillation (May 1976).

So the model has an asymmetry: hunger is corrected fast (famine, cases 3 and 8), plenty slowly (case 2).

### 4c. What is not yet complete

| # | Gap | Why it matters |
|---|---|---|
| 1 | No age structure | Children do not work or fight; the old need care; births come from women of childbearing age; a baby boom's echo (momentum) is missing |
| 2 | City size from people | The engine's size drives happiness, health, buildings and worked plots (D30's open question) |
| 3 | Health balance `H` from the engine | The burden needs a number from 0 to 1 |
| 4 | Urban share and density | Town life and the urban penalty need a definition |
| 5 | Economy factor | Needs prices and wages from the goods economy; 1 until then |
| 6 | Turn length | Turns of 1 to 50 years; the model runs in yearly steps inside a turn |
| 7 | Epidemics and disasters | Left out for now as you said (M65); the model can take them later as a burden term |
| 8 | Child and adult deaths in one burden | The burden is crude: infant deaths (water, urban penalty) and adult deaths (war, famine) are not told apart |

### 4d. Proposals (choose, change or reject each)

**Proposal 1. Age structure**
- **A.** None: crude rates as now. A city's workers are a fixed share of its people.
- **B. (recommended)** Three groups: children 0-14, adults 15-59, old 60+. Births go to children. Each year a fifteenth of the children become adults and a forty-fifth of the adults become old. The burden falls on each group by a weight, with children and the old higher. Workers and soldiers are the adults. This is three numbers per city and gives momentum, the dependency burden and the demographic transition's ageing.
- **C.** Five-year groups (a Leslie matrix with 18 groups): exact, but 18 numbers per city and more to calibrate.

**Proposal 2. City size from people** (the engine shows `size^2.8 × 1,000`, `CvCity::getRealPopulation`)
- **A. (recommended) The inverse curve:** size = (N / 1,000)^(1/2.8).
  - Examples: 1,000 people is size 1; 90,000 is 5; 631,000 is 10; 4.4 million is 20.
  - Happiness, health and buildings follow size as now.
  - The plots' output comes from the real workers (PR.F7, the tile formula). Workers beyond what the plots take go to the city's sectors (D26).
  - Size grows with the logarithm of people, as today.
- **B. Labour units:** size = workers ÷ workers per plot at the current tools and machinery. Size then means worked plots. Machinery would shrink sizes, and happiness per size would no longer follow people.
- **C. Hybrid:** worked plots from B, while size (for happiness, health, buildings) comes from A.

**Proposal 3. The food box** (the exe only reads the fractions the DLL gives, `getFoodBarPercentages`)
- **A. (recommended)** The bar shows the progress from this size to the next in people (N between the two sizes' people). It moves with growth and falls in a famine.
- **B.** The bar shows the food balance (food against need).

**Proposal 4. Health balance `H` from the engine's good and bad health**
- **A. (recommended)** H = good ÷ (good + bad): 1 when nothing is bad, 0.5 when they are equal.
- **B.** H = 0.5 + (good − bad) ÷ (2 × size), clamped from 0 to 1.

**Proposal 5. Urban share `u` and unsanitized share `U`**
- **A. (recommended)**
  - u is the share of people not working plots: the city's sector workers (D26) over its people.
  - U = u × (1 − sanitation level), where the level comes from the water and sewer level (D31: none, wells and aqueduct, sewers).
- **B.** u from size alone, for example u = min(1, size ÷ 30).

**Proposal 6. Child and adult burden (only with proposal 1 B)**
- Infant and child burden: water, the urban penalty, deficiencies (vitamin A), famine.
- Adult burden: war, famine, the base burden.
- The sizes come from the same sources (London infant mortality of 300-400 per 1,000 births against 180 nationally).

**Proposal 7. Turn length**
- **(recommended)** The model always runs in yearly steps. A 50-year turn runs 50 steps, a 1-year turn one step. Years per turn come from the game speed and the era (the game's turn increments).

## 5. Open

- Phytate per good (zinc), iron absorption by meal, losses per form, the stores' sizes, the weights `W`.
- Bound niacin in maize (pellagra) and iodine in plants by soil: sources to add.
- Whale perfume (ambergris and spermaceti): a source to add.
- The volcanic energy source (geothermal power on volcanic plots and thermal vents): for the energy chain, not the goods economy.
