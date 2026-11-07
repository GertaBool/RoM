# Food consumption of a city population: the model (R64, M112)

This file replaces `archive/nutrition/food_model_spec.md`. Every parameter comes from `nutrition_record.md` through the data files below; nothing is typed here that is not in them. The tool `plan/tools/food_model.py` implements each equation; the cases are in `food_model_cases.json`.

| File | What it holds | Written by |
|---|---|---|
| `data/nutrient_needs.json` (version 2) | four levels per nutrient, energy, water, absorption, gut limits, harm | `plan/tools/nutrient_needs_build.py`, from record sections 2a-2j |
| `data/nutrient_profiles.json` | nutrients per 100 g per good (USDA SR Legacy 2018-04; MEXT for iodine) | `plan/tools/nutrient_profile.py` |
| `data/satiety_index.json` | Holt 1995 satiety index, 38 foods, mapped to 11 goods | `plan/tools/nutrient_needs_build.py` |

## 1. Principles (the user's decisions)

| | Principle | Source |
|---|---|---|
| P1 | A city eats only what it holds; what is not eaten stays in store (surplus) | M84, M102 |
| P2 | The population is one average adult-equivalent person; body reserves belong to the growth formula; no seasons | M101 |
| P3 | Needs are not fixed: energy follows work; thiamin and niacin follow energy; protein and vitamin A follow body weight; B6 follows protein; water follows work, weight and climate; sodium follows sweat | M102, M103 |
| P4 | First the energy of basal function, then being fed (energy for labour; satiety being met is the baseline), then the nutrient minima (the body's functions), then nutrition (mean adequacy ratio), then the better stocks first; well-being is a separate sorted list, never added to nutrition | M88, M93, M96, M102, M114, M116 |
| P4a | Starvation is the body no longer able to fulfil its functions and people no longer able to labour; it is read from the minima, not from the energy need. Energy short of the need lowers the work people can do | M114 |
| P5 | Harm is a consequence, not a motive: harm thresholds are reported, never constraints | M101 |
| P6 | Only limits on what the body can take in, and the user's ceilings per good, constrain eating | M85, M86, M88, M93 |
| P7 | Protein is energy: excess protein is turned into glucose, up to the liver's daily capacity to make urea, a rate spread over the day's three meals | M114 |

## 2. Legend

| Symbol | Meaning | Unit | Source (data file key) |
|---|---|---|---|
| $g\in\mathcal G$ | goods available to the city (case `available_g`) | – | case |
| $a_g$ | amount of good $g$ available per person per day | g | case |
| $x_g$ | amount eaten (decision variable) | g | model |
| $W$ | body weight | kg | case |
| $s$ | share of men | – | case |
| $\Lambda$ | physical activity level asked by the work | – | case |
| $\Lambda^{\max}$ | alimentary ceiling, 2.5 | – | `energy.pal_limits` (Thurber 2019) |
| $R$ | resting energy expenditure, $15.1W+371$ | kcal/d | `energy.ree_kcal` (Mifflin 1990) |
| $E$ | energy need, $\min(\Lambda,\Lambda^{\max})\,R$ | kcal/d | – |
| $c_{g,k}$ | nutrient $k$ per gram of good $g$ | unit/g | `nutrient_profiles.json` (first form; whole cod for fish, §3) |
| $t_k$ | adequacy target of nutrient $k$ | unit/d | `nutrients.k.optimum`, or `recommended` where no plateau (§4) |
| $m_k$ | minimum (deficiency threshold) | unit/d | `nutrients.k.minimum` |
| $c^{\max}_k$ | ceiling of harm | unit/d | `nutrients.k.ceiling` |
| $P^{\lim}$ | protein the liver can turn into urea in a day, $4.06\,W$ (285-365 g for 80 kg), about a third per meal | g/d | `nutrients.protein.intake_limit` (Bilsborough and Mann 2006) |
| $E^{0}$ | energy of basal function, $1.2\,R$ (the lowest daily expenditure, non-ambulant people) | kcal/d | `energy.pal_limits.lowest` (Black 1996) |
| $u_k$, $u_E$ | coverage of minimum $k$ and of $E^0$, $\le1$ | – | model |
| $L$ | labour capacity, share of the asked work | – | model |
| $\phi$ | iron absorbed from the diet: 0.16 with animal foods, 0.085 without | – | `absorption.iron_fraction` (midpoints) |
| $h$ | share of days with a work shift in heat | – | case |
| $z$ | share of the energy need eaten (being fed) | – | model |
| $v_k$ | adequacy of nutrient $k$, $\le 1$ | – | model |
| $q_g$ | nutritional quality of good $g$ (§6) | – | model |

Ranges $[\ell,h]$ in the data enter as their midpoint; values by sex enter as $s\cdot\text{male}+(1-s)\cdot\text{female}$.

## 3. Composition

- Each good is its first form in `nutrient_profiles.json` unless the case names another form: `GOOD:form` (USDA) or `GOOD:mext:form` (MEXT; niacin equivalents taken as MEXT gives them). MEXT iodine fills a USDA gap only for the good's default form.
- **Fish is the whole animal as eaten, not fillet** (M91, M113). The parts and their sources are in `nutrient_needs.json` `whole_animal`:
  - **cod as eaten** (`BONUS_FISH`): the coastal meal *mølje* is cod, cod liver, fresh cod-liver oil and roe (Skjervøy, northern Norway; Brustad et al. 2004). By the Torry part shares (fillet 36, liver 5, roe 4 % of round weight), $c_{\text{fish}}=(36\,c_{\text{cod}}+5\,c_{\text{liver}}+4\,c_{\text{roe}})/45$: 125 kcal, 16.9 g protein, 5.8 g fat per 100 g. The liver record is lingcod liver (42 % fat; no raw cod liver record exists); its vitamin A is cod liver oil's 30,000 µg/100 g times the liver fat share.
  - **herring eaten whole** (`BONUS_FISH:herring whole, May` and `…, August`): the USDA herring record with the fat of whole herring measured with head and intestines, 7.9 % in May and 19.5 % about 1 August (Faroese data, 1950s); energy by Atwater factors: 143 and 247 kcal per 100 g.
  - Heads and viscera (Bechtel 2003) and farmed-cod liver lipid are recorded but not used: no source shows heads and viscera eaten as food, and the liver figure is from farmed fish.
- Fatty fish eaten year-round: Atlantic herring (USDA 175116, 9.0 g fat), Pacific herring (173669, 13.9 g), Atlantic mackerel (175119, 13.9 g). Small fish eaten whole: pond smelt (MEXT 10276, calcium 450 mg/100 g), loach (10213, 1,100 mg), whole dried sardine (10053, 18.9 g fat).
- **Tea with meals** lowers the iron absorbed by 64 % (record 2c); applied when the case drinks tea with meals.
- **Niacin equivalents:** $c_{g,\text{NE}}=\beta_g\,c_{g,\text{niacin}}+1000\,c_{g,\text{tryptophan}}/60$, with $\beta_g=1/3$ for wheat, rice and maize (Carpenter 1983), else 1.
- **Iodine:** SR Legacy holds none for these goods; the MEXT value of the same good is used.

## 4. Needs

$$t_k=\begin{cases}\text{optimum}_k\times B_k & \text{if an optimum exists}\\ \text{recommended}_k & \text{otherwise (potassium, magnesium)}\end{cases}\qquad B_k\in\{1,\ W,\ E/1000,\ t_{\text{protein}}\}$$

by the basis of nutrient $k$ (per day, per kg, per 1,000 kcal, per g protein). Particular cases:
- protein: $t=1.62\,W$, $m=0.65\,W$;
- iron: $t$ is the dietary optimum (8 men, 18.9 women); $m=$ absorbed losses $/\phi$;
- zinc: $t$ is the dietary amount (9.4 men, 6.8 women); the absorbed minimum (3.9 men, 3.2 women) is checked after with Miller's equation (§7);
- sodium: $t$, $m$ and $u$ each gain $h\times5{,}400$ mg (sweat per hot shift, midpoint of 4,800-6,000).

## 5. The program (lexicographic)

Constraints, all stages:

$$0\le x_g\le\bar a_g,\qquad \bar a_g=\min\!\left(a_g,\ \tfrac{250}{c_{g,\text{fat}}},\ 3000\ \text{if }g=\text{dairy}\right)$$
$$\sum_g c_{g,\text{kcal}}x_g\le E,\qquad \sum_g c_{g,\text{protein}}x_g\le P^{\lim}$$
$$\sum_{g\in\text{fruit}}x_g\le 4518\ \text{g (one watermelon)},\qquad c_{\text{milk},\text{lactose}}\,x_{\text{dairy}}\le 13.5\ \text{g only if the people are neither lactase persistent nor a dairy culture}$$
$$u_k\,m_k\le\sum_g c_{g,k}x_g,\qquad u_E\,E^0\le\sum_g c_{g,\text{kcal}}x_g,\qquad zE\le\sum_g c_{g,\text{kcal}}x_g,\qquad v_k\,t_k\le\sum_g c_{g,k}x_g$$

with every $u,z,v\in[0,1]$. Each stage holds the optimum of the stages before it.

1. **Basal function:** $u_E^*=\max u_E$.
2. **Being fed:** $z^*=\max z$ (M93: satiety being met is the baseline; energy is its measure here).
3. **Nutrient minima:** $S^*=\max\frac{1}{K'}\sum_k u_k$ over the nutrients with a minimum.
4. **Nutrition:** $\text{MAR}^*=\max\frac1K\sum_k v_k$.
5. **Better stocks first:** $\min\sum_g(1-q_g)\,c_{g,\text{kcal}}\,x_g$.

Energy eaten is capped at $E$: food beyond the need stays in store (P1). Protein counts as energy at 4 kcal/g up to $P^{\lim}$ (P7). The lactose limit comes from studies of pasteurised milk or lactose in water in lactase-deficient people (Wilt 2010); it is not applied to lactase-persistent people or dairy cultures (M113), and live-culture yogurt is digested in the gut (Kolars 1984). Harm ceilings $c^{\max}_k$ are not constraints (P5).

**Reading starvation and labour (P4a):**
- **starving** when energy eaten $<E^0$: the body cannot keep its basal functions;
- **deficient in $k$** when intake $<m_k$;
- **labour capacity** $L=\min\!\left(1,\max\!\left(0,\ \dfrac{\sum_g c_{g,\text{kcal}}x_g/R-1.2}{\Lambda-1.2}\right)\right)$: the share of the asked work the energy above basal function allows.

## 6. Quality of a good

$$q_g=\frac1K\sum_k\min\!\left(1,\ \frac{c_{g,k}\,E/c_{g,\text{kcal}}}{t_k}\right)$$

the mean adequacy of a diet of good $g$ alone at the energy need.

## 7. Outputs

| Output | Equation | Source |
|---|---|---|
| body functions, starving, deficient, labour | $S^*$; energy $<E^0$; intake $<m_k$; $L$ | §5 |
| energy share, MAR | $z^*$, $\text{MAR}^*$ | §5 |
| contributions | $c_{g,k}x_g$ for every nutrient and good: where each nutrient comes from | §3 |
| deficiencies | nutrients with intake $<m_k$ | §4 |
| harms | nutrients with intake $>c^{\max}_k$; protein $>2.5\,W$ or $>35\,\%$ of energy; fat $\ge300$ g (sweating) | `nutrients.*.ceiling`, `gut_limits.fat_g` |
| protein per meal | $\frac13\sum_g c_{g,\text{protein}}x_g$, and the hours to absorb it at 10 and 1.3 g an hour | `nutrients.protein.gut_absorption_g_per_h` (Bilsborough and Mann 2006) |
| absorbed zinc | Miller 2013 eq. 2 with dietary zinc, phytate (600 mg/100 g dry for cereals, 20 for tubers), calcium and protein | `absorption.zinc_equation`, `absorption.phytate_mg_per_100g_dry` |
| water to draw | $\text{WT}-\text{water in food}-500-\sum_{\text{drinks}}\text{HI}_g x_g$ | Yamada 2022 (WT), Tipton 2025 (500 ml metabolic), Maughan 2016 (HI: milk 1.5, tea and beer 1.0) |
| alcohol | $7\sum_g c_{g,\text{alcohol}}x_g$ g a week, against Wood 2018 bands | `harm.alcohol_g_per_week` |
| fullness | mean Holt index of the energy eaten from goods with a tested food, and that share of energy | `satiety_index.json` |
| well-being list (separate) | goods eaten, sorted: hyper-palatable first (Fazzino 2019 criteria from composition), then lighter (lower kcal per g: shorter stomach residence, Hunt and Stubbs 1975) | record 2e |

## 8. Cases (`food_model_cases.json`, run 2026-11-07)

Year-round compositions only (P2). Each table gives intake, target, minimum and the goods it comes from (share of the intake).

| Case | Energy need (kcal) | Starving | Labour capacity (PAL reached) | Minima covered | Deficient | MAR | Harms |
|---|---|---|---|---|---|---|---|
| farming town, temperate | 3,442 | no | 1.000 (2.41) | 1.000 | none | 0.864 | none |
| fishing village, cool coast | 3,442 | no | 1.000 (2.41) | 0.926 | calcium, folate_dfe, vit_c | 0.875 | sodium, protein above 2.5 g/kg |
| rice town, hot season labour | 3,078 | no | 1.000 (2.41) | 0.905 | iron, thiamin, folate_dfe | 0.759 | none |

**farming town, temperate** — eaten per person per day: wheat 818 g; pig 150 g; dairy 600 g; apple 200 g; salt 15 g.

| Nutrient | Intake | Target | Minimum | Where it comes from |
|---|---|---|---|---|
| protein (g) | 152.2 | 113.4 | 45.5 | wheat 68 %, pig 19 %, dairy 12 % |
| sodium (mg) | 6165.1 | 4995 | 21 | salt 94 % |
| potassium (mg) | 4510.1 | 3000 | 1075 | wheat 66 %, dairy 18 %, pig 12 % |
| calcium (mg) | 957.8 | 800 | 741 | dairy 71 %, wheat 25 % |
| magnesium (mg) | 1132.2 | 362.5 | 165 | wheat 91 %, dairy 5 % |
| iron (mg) | 27.7 | 13.4 | 8.6 | wheat 94 % |
| zinc (mg) | 26.6 | 8.1 | — | wheat 81 %, pig 10 %, dairy 8 % |
| iodine (µg) | 97.7 | 200 | 54.5 | dairy 98 % |
| selenium (µg) | 650.3 | 49 | 17 | wheat 89 %, pig 8 % |
| vit_a_rae (µg RAE) | 285 | 466.5 | 175 | dairy 97 % |
| thiamin (mg) | 4.8 | 1.4 | 1 | wheat 65 %, pig 28 %, dairy 6 % |
| riboflavin (mg) | 2.4 | 1.4 | 0.5 | dairy 43 %, wheat 40 %, pig 16 % |
| niacin_ne (mg NE) | 54.4 | 19 | 15.1 | wheat 67 %, pig 24 %, dairy 8 % |
| vit_b6 (mg) | 3.5 | 1.7 | 0.6 | wheat 71 %, pig 20 %, dairy 6 % |
| folate_dfe (µg DFE) | 348.3 | 400 | 300 | wheat 89 %, dairy 9 % |
| b12 (µg) | 3.5 | 5.6 | 1 | dairy 77 %, pig 23 % |
| vit_c (mg) | 10.1 | 100 | 10 | apple 91 %, pig 9 % |

**fishing village, cool coast** — eaten per person per day: fish 55 g; fish: herring 320 g; fish: atlantic mackerel 1,000 g; wheat 250 g; salt 15 g.

| Nutrient | Intake | Target | Minimum | Where it comes from |
|---|---|---|---|---|
| protein (g) | 284.2 | 113.4 | 45.5 | fish: atlantic mackerel 65 %, fish: herring 20 %, wheat 11 % |
| sodium (mg) | 7034.5 | 4995 | 21 | salt 83 %, fish: atlantic mackerel 13 % |
| potassium (mg) | 5286.4 | 3000 | 1075 | fish: atlantic mackerel 59 %, fish: herring 20 %, wheat 17 % |
| calcium (mg) | 386.7 (below minimum) | 800 | 741 | fish: herring 47 %, fish: atlantic mackerel 31 %, wheat 19 % |
| magnesium (mg) | 1192.5 | 362.5 | 165 | fish: atlantic mackerel 64 %, wheat 26 %, fish: herring 9 % |
| iron (mg) | 28.1 | 13.4 | 8.6 | fish: atlantic mackerel 58 %, wheat 28 %, fish: herring 13 % |
| zinc (mg) | 16.4 | 8.1 | — | wheat 41 %, fish: atlantic mackerel 39 %, fish: herring 19 % |
| iodine (µg) | 192.9 | 200 | 54.5 | fish 100 % |
| selenium (µg) | 751 | 49 | 17 | fish: atlantic mackerel 59 %, wheat 24 %, fish: herring 16 % |
| vit_a_rae (µg RAE) | 1370.2 | 466.5 | 175 | fish 57 %, fish: atlantic mackerel 36 %, fish: herring 7 % |
| thiamin (mg) | 3.1 | 1.4 | 1 | fish: atlantic mackerel 57 %, wheat 31 %, fish: herring 10 % |
| riboflavin (mg) | 4.2 | 1.4 | 0.5 | fish: atlantic mackerel 74 %, fish: herring 18 %, wheat 7 % |
| niacin_ne (mg NE) | 160.6 | 19 | 15.1 | fish: atlantic mackerel 78 %, fish: herring 13 %, wheat 7 % |
| vit_b6 (mg) | 5.8 | 1.7 | 0.6 | fish: atlantic mackerel 69 %, fish: herring 17 %, wheat 13 % |
| folate_dfe (µg DFE) | 144 (below minimum) | 400 | 300 | wheat 66 %, fish: herring 22 %, fish: atlantic mackerel 7 % |
| b12 (µg) | 131.7 | 5.6 | 1 | fish: atlantic mackerel 66 %, fish: herring 33 % |
| vit_c (mg) | 7.5 (below minimum) | 100 | 10 | fish: atlantic mackerel 54 %, fish: herring 30 %, fish 16 % |

**rice town, hot season labour** — eaten per person per day: rice: polished 752 g; fish:  pond smelt, whole 200 g; banana 200 g; tea:  sencha infusion 600 g; salt 20 g.

| Nutrient | Intake | Target | Minimum | Where it comes from |
|---|---|---|---|---|
| protein (g) | 85.8 | 97.2 | 39 | rice: polished 62 %, fish:  pond smelt, whole 34 % |
| sodium (mg) | 8209.2 | 7695 | 2721 | salt 94 % |
| potassium (mg) | 1984.6 | 3000 | 1075 | rice: polished 44 %, banana 36 %, fish:  pond smelt, whole 12 %, tea:  sencha infusion 8 % |
| calcium (mg) | 1143.4 | 800 | 741 | fish:  pond smelt, whole 79 %, rice: polished 18 % |
| magnesium (mg) | 304.3 | 362.5 | 165 | rice: polished 62 %, banana 18 %, fish:  pond smelt, whole 16 % |
| iron (mg) | 9.6 (below minimum) | 13.4 | 24 | rice: polished 63 %, fish:  pond smelt, whole 19 %, tea:  sencha infusion 12 %, banana 5 % |
| zinc (mg) | 12.5 | 8.1 | — | rice: polished 65 %, fish:  pond smelt, whole 32 % |
| iodine (µg) | 58.2 | 200 | 54.5 | fish:  pond smelt, whole 100 % |
| selenium (µg) | 159.6 | 49 | 17 | rice: polished 71 %, fish:  pond smelt, whole 28 % |
| vit_a_rae (µg RAE) | 204 | 466.5 | 175 | fish:  pond smelt, whole 97 % |
| thiamin (mg) | 0.6 (below minimum) | 1.2 | 0.9 | rice: polished 87 %, banana 10 % |
| riboflavin (mg) | 1.1 | 1.4 | 0.5 | rice: polished 34 %, tea:  sencha infusion 27 %, fish:  pond smelt, whole 26 %, banana 13 % |
| niacin_ne (mg NE) | 25.8 | 19 | 13.5 | rice: polished 56 %, fish:  pond smelt, whole 31 %, tea:  sencha infusion 7 %, banana 6 % |
| vit_b6 (mg) | 2.4 | 1.5 | 0.6 | rice: polished 52 %, banana 31 %, fish:  pond smelt, whole 14 % |
| folate_dfe (µg DFE) | 100.2 (below minimum) | 400 | 300 | rice: polished 60 %, banana 40 % |
| b12 (µg) | 15.8 | 5.6 | 1 | fish:  pond smelt, whole 100 % |
| vit_c (mg) | 55.4 | 100 | 10 | tea:  sencha infusion 65 %, banana 31 % |

**What the results rest on.**
- **Fishing village:** fed in full by mackerel and herring, protein at the liver's daily capacity (284 g, about 95 g a meal). Calcium, folate and vitamin C fall below their minima because the case holds fish fillet records (no bones), wheat and no gathered plants: the records of fish eaten with their bones, and of the shore plants and berries a fishing people gathers (M113), are not in the case.
- **Rice town:** fed in full. Thiamin falls below its minimum because the rice is polished (0.07 mg per 100 g; brown rice 0.541): beriberi is the deficiency of polished-rice diets. Iron falls below its minimum because tea with meals cuts absorption by 64 %, raising the dietary minimum to 24 mg. Calcium is covered by small fish eaten whole (pond smelt, 79 % of calcium). Folate is short: no greens in the case.
- **Farming town:** fed in full, every minimum met; vitamin C is exactly at its minimum (apples).

## 9. What the data files do not yet give

- **Children and the elderly:** the levels are for adults; the city is an adult-equivalent person.
- **Free fructose:** the profiles hold total sugars only, so the fructose limit (25 g alone; Rao 2007) is not applied.
- **Iron inhibitors:** tea (−64 %) and coffee (−39 %) are in the data but not applied, because their effect depends on whether they are drunk with meals.
- **Well-being:** the reward, lightness and repetition measures are listed per good; how they combine into one ordering beyond the sort above is open (R55.3).
- **Annual fat of the catch:** the model runs on one composition per good; the year's mean fat of whole herring is not in the sources read (seasonal values 7.9-19.5 %; Canadian annual means of 9.8 and 11.2 % cover June to October only).
