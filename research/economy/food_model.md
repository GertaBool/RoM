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
- **The cow is the whole animal as eaten** (M84, M94): meat, liver, heart and kidneys in the shares 41.4 : 1.12 : 0.37 : 0.18 (% of live weight; `whole_animal.cow_as_eaten`). The pig is muscle only: its organ shares have no stated base in the sources read.
- **Tea and iron:** one cup of tea with a meal lowered non-haem iron absorption 64 %, a cup of coffee 39 % (Morck 1983; US study, the tea not named, black tea assumed); tea one hour after the meal had no effect (Ahmad Fuzi 2017). The model applies the 64 % only to black tea drunk with meals, the 39 % to coffee with meals, and nothing to green tea (no study read measures it) or to tea after meals (`absorption.iron_inhibitors`).
- **Caffeine** raises the energy need by 150 kcal at 600 mg, in proportion below (Dulloo 1989; M85); caffeine per 100 g from MEXT brewing (black tea 30, sencha 20, coffee 60 mg). The tool solves again until caffeine eaten and energy need agree.
- **Maize niacin** is one third available unless the case treats maize with alkali (Carpenter 1983).
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

$$0\le x_g\le\bar a_g,\qquad \bar a_g=\min\!\left(a_g,\ \tfrac{250}{c_{g,\text{fat}}},\ 453.6\ \text{if }g\text{ is meat},\ 1000\ \text{if cheese},\ 3000\ \text{if milk}\right)$$

(the user's ceilings per good, M85, M88, M93; `user_ceilings_g`)
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
| calcium absorbed | $\sum_g f_g\,c_{g,\text{Ca}}x_g$ over goods with a measured fraction (milk 0.32, small fish eaten whole 0.238); the others listed | `absorption.calcium_fraction_by_good` |
| B12 absorbed at most | three meals × 1.5-2 µg (per-meal saturation) | `absorption.b12_absorbed` (Watanabe 2007) |
| caffeine | mg eaten and kcal added to the need | `caffeine_mg_per_100g` |
| alcohol with fat | flag (alcohol and fat raise ad libitum intake 2.8 MJ a day, Tremblay 1995; intake is capped at the need here) | record 2f |
| keeping | grams left per day, the good's keep class and its spoilage per year with the basis as written in `nutrition.json` | `nutrition.json` |
| repetition | number of goods over 5 % of energy; largest good's energy share | well-being |
| deficiencies | nutrients with intake $<m_k$ | §4 |
| harms | nutrients with intake $>c^{\max}_k$; protein $>2.5\,W$ or $>35\,\%$ of energy; fat $\ge300$ g (sweating) | `nutrients.*.ceiling`, `gut_limits.fat_g` |
| protein per meal | $\frac13\sum_g c_{g,\text{protein}}x_g$, and the hours to absorb it at 10 and 1.3 g an hour | `nutrients.protein.gut_absorption_g_per_h` (Bilsborough and Mann 2006) |
| absorbed zinc | Miller 2013 eq. 2 with dietary zinc, phytate (600 mg/100 g dry for cereals, 20 for tubers), calcium and protein | `absorption.zinc_equation`, `absorption.phytate_mg_per_100g_dry` |
| water to draw | $\text{WT}-\text{water in food}-500-\sum_{\text{drinks}}\text{HI}_g x_g$ | Yamada 2022 (WT), Tipton 2025 (500 ml metabolic), Maughan 2016 (HI: milk 1.5, tea and beer 1.0) |
| alcohol | $7\sum_g c_{g,\text{alcohol}}x_g$ g a week, against Wood 2018 bands | `harm.alcohol_g_per_week` |
| fullness | mean Holt index of the energy eaten from goods with a tested food, and that share of energy | `satiety_index.json` |
| well-being list (separate) | goods eaten, sorted: hyper-palatable first (Fazzino 2019 criteria from composition), then lighter (lower kcal per g: shorter stomach residence, Hunt and Stubbs 1975) | record 2e |

## 8. Cases

The case report is `food_model_cases_report.md`, written by `plan/tools/food_model.py food_model_cases.json --md food_model_cases_report.md`. For each case it gives first the inputs (person, climate and culture variables; every good available with its composition record, amount and energy, protein and fat per 100 g), then the results, every nutrient with intake, target, minimum, ceiling and the goods it comes from, the keeping of what is left, and the well-being list. No table is typed by hand.

## 9. What the model does not yet do

| Item | Why |
|---|---|
| Satiety as the gauge of being fed (M92, M93) | the satiety index is measured for 11 of the goods (Holt 1995); being fed is measured by energy, and fullness is reported where measured |
| Lemons' ceiling (M92) | no value given yet |
| "Then dessert" (M88) | after nutrition, stage 5 takes the better goods first and fills with the rest; no further energy is eaten beyond the need, so no separate dessert intake |
| Health effects in the well-being list (M91) | deficiencies and harm flags are listed beside it; no combined measure |
| Whale blubber (M83, M85) | no source read gives the share of blubber in a whale as eaten |
| Pig organs | organ shares have no stated base |
| Rich city: surplus milk into dairy products, bread (M91) | needs conversion yields (milk to cheese and butter, grain to bread) from a source |
| Food effects in the game (M57, M75) | a design decision: how labour capacity, deficiencies and harms map to fertility, productivity and strength |
| Children and the elderly | the record holds adult levels only |
