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
| P4 | First the body's functions (every nutrient minimum and the energy of basal function), then energy for labour, then nutrition (mean adequacy ratio), then the better stocks first; well-being is a separate sorted list, never added to nutrition | M88, M93, M96, M102, M114 |
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

- Each good is its first, as-eaten form in `nutrient_profiles.json`.
- **Fish is the whole animal as eaten, not fillet** (M91, M113). The parts and their sources are in `nutrient_needs.json` `whole_animal`:
  - **cod as eaten** (`BONUS_FISH`): the coastal meal *mølje* is cod, cod liver, fresh cod-liver oil and roe (Skjervøy, northern Norway; Brustad et al. 2004). By the Torry part shares (fillet 36, liver 5, roe 4 % of round weight), $c_{\text{fish}}=(36\,c_{\text{cod}}+5\,c_{\text{liver}}+4\,c_{\text{roe}})/45$: 125 kcal, 16.9 g protein, 5.8 g fat per 100 g. The liver record is lingcod liver (42 % fat; no raw cod liver record exists); its vitamin A is cod liver oil's 30,000 µg/100 g times the liver fat share.
  - **herring eaten whole** (`BONUS_FISH:herring whole, May` and `…, August`): the USDA herring record with the fat of whole herring measured with head and intestines, 7.9 % in May and 19.5 % about 1 August (Faroese data, 1950s); energy by Atwater factors: 143 and 247 kcal per 100 g.
  - Heads and viscera (Bechtel 2003) and farmed-cod liver lipid are recorded but not used: no source shows heads and viscera eaten as food, and the liver figure is from farmed fish.
- A case can choose any other form of a good as `GOOD:form`.
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

1. **Body functions:** $S^*=\max\frac{1}{K'+1}\left(\sum_{k}u_k+u_E\right)$ over the nutrients with a minimum and the basal energy.
2. **Labour:** $z^*=\max z$.
3. **Nutrition:** $\text{MAR}^*=\max\frac1K\sum_k v_k$.
4. **Better stocks first:** $\min\sum_g(1-q_g)\,c_{g,\text{kcal}}\,x_g$.

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
| deficiencies | nutrients with intake $<m_k$ | §4 |
| harms | nutrients with intake $>c^{\max}_k$; protein $>2.5\,W$ or $>35\,\%$ of energy; fat $\ge300$ g (sweating) | `nutrients.*.ceiling`, `gut_limits.fat_g` |
| protein per meal | $\frac13\sum_g c_{g,\text{protein}}x_g$, and the hours to absorb it at 10 and 1.3 g an hour | `nutrients.protein.gut_absorption_g_per_h` (Bilsborough and Mann 2006) |
| absorbed zinc | Miller 2013 eq. 2 with dietary zinc, phytate (600 mg/100 g dry for cereals, 20 for tubers), calcium and protein | `absorption.zinc_equation`, `absorption.phytate_mg_per_100g_dry` |
| water to draw | $\text{WT}-\text{water in food}-500-\sum_{\text{drinks}}\text{HI}_g x_g$ | Yamada 2022 (WT), Tipton 2025 (500 ml metabolic), Maughan 2016 (HI: milk 1.5, tea and beer 1.0) |
| alcohol | $7\sum_g c_{g,\text{alcohol}}x_g$ g a week, against Wood 2018 bands | `harm.alcohol_g_per_week` |
| fullness | mean Holt index of the energy eaten from goods with a tested food, and that share of energy | `satiety_index.json` |
| well-being list (separate) | goods eaten, sorted: hyper-palatable first (Fazzino 2019 criteria from composition), then lighter (lower kcal per g: shorter stomach residence, Hunt and Stubbs 1975) | record 2e |

## 8. Cases (`food_model_cases.json`, run 2026-11-07)

| Case | Energy need (kcal) | Minima covered | Starving | Deficient | Labour capacity (PAL reached) | MAR | Harms |
|---|---|---|---|---|---|---|---|
| farming town, temperate, dairy culture (wheat, pig, dairy, apple, salt) | 3,442 | 1.000 | no | none | 1.000 (2.41) | 0.864 | none |
| fishing village, cool coast, May (cod as eaten 2 kg, whole herring at 7.9 % fat 2 kg, clams 300 g, wheat 250 g, salt 15 g) | 3,442 | 0.990 | no | folate | 0.627 (1.96) | 0.924 | iodine; protein above 2.5 g/kg and 35 % of energy |
| fishing village, cool coast, August (the same with whole herring at 19.5 % fat) | 3,442 | 0.983 | no | calcium, folate | 1.000 (2.41) | 0.918 | sodium, iodine; protein above 2.5 g/kg |
| rice town, hot-season labour (rice, fish, banana, tea, salt) | 3,078 | 0.941 | no | calcium, folate | 1.000 (2.41) | 0.816 | none |

**The fishing village.** No one starves in either season. In August the village does all its work. In May whole herring carries 7.9 % fat; with protein at the liver's daily capacity (284 g, about 95 g a meal) the energy eaten allows 63 % of the asked work: the village is fed but labours less. Folate falls below its minimum in both seasons (no green food in the case), calcium in August. The year's fat comes from what is kept (dried fish, liver oil, grain); in the model that is the store (P1), and the turn is long enough to hold seasons (P2). The May and August runs bound the year; neither is a season inside the model.

## 9. What the data files do not yet give

- **Children and the elderly:** the levels are for adults; the city is an adult-equivalent person.
- **Free fructose:** the profiles hold total sugars only, so the fructose limit (25 g alone; Rao 2007) is not applied.
- **Iron inhibitors:** tea (−64 %) and coffee (−39 %) are in the data but not applied, because their effect depends on whether they are drunk with meals.
- **Well-being:** the reward, lightness and repetition measures are listed per good; how they combine into one ordering beyond the sort above is open (R55.3).
- **Annual fat of the catch:** the model runs on one composition per good; the year's mean fat of whole herring is not in the sources read (seasonal values 7.9-19.5 %; Canadian annual means of 9.8 and 11.2 % cover June to October only).
