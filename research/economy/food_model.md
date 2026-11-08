# Food consumption of a city population: the model (R64, M112)

This file replaces `archive/nutrition/food_model_spec.md`. Every parameter comes from `nutrition_record.md` through the data files below; nothing is typed here that is not in them. The tool `plan/tools/food_model.py` implements each equation; the cases are in `food_model_cases.json`.

| File | What it holds | Written by |
|---|---|---|
| `data/nutrient_needs.json` (version 2) | four levels per nutrient, energy, water, absorption, gut limits, harm | `plan/tools/nutrient_needs_build.py`, from record sections 2a-2j |
| `data/nutrient_profiles.json` | nutrients per 100 g per good (USDA SR Legacy 2018-04; MEXT for iodine) | `plan/tools/nutrient_profile.py` |
| `data/satiety_index.json` | Holt 1995 satiety index, 38 foods, mapped to 11 goods (reference; the model uses the user's values) | `plan/tools/nutrient_needs_build.py` |
| `data/user_inputs.json` | the user's values from `data/user_inputs_m120.ods` (M120): satiety index of every good and form, fed fullness, drinks, dessert, ceilings, default forms, fish catch by region, animal shares, PAL by work, lactase persistence, spoilage, athletes' optima, strength and IQ anchors, contaminants | `plan/tools/ods_read.py` (ODS to CSV), `plan/tools/user_inputs_apply.py` (CSV to JSON, row by row; a row that does not parse stops the run) |

## 1. Principles (the user's decisions)

| | Principle | Source |
|---|---|---|
| P1 | A city eats only what it holds; what is not eaten stays in store (surplus) | M84, M102 |
| P2 | The population is one average adult-equivalent person; body reserves belong to the growth formula; no seasons | M101 |
| P3 | Needs are not fixed: energy follows work; thiamin and niacin follow energy; protein and vitamin A follow body weight; B6 follows protein; water follows work, weight and climate; sodium follows sweat | M102, M103 |
| P4 | First the energy of basal function, then being fed (fullness by the satiety index, then energy for labour), then the nutrient minima (the body's functions), then nutrition (mean adequacy ratio), then towards athletes' levels, then the better stocks first, then dessert beyond the need; well-being is a separate sorted list, never added to nutrition | M88, M93, M96, M102, M114, M116, M118, M120 |
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
| $\Lambda$ | physical activity level asked by the work: manual labour 2.0, sedentary 1.5, soldier 2.5, slaves in quarries or mines 3.0 | – | `user_inputs.pal_by_work` (U157-U160), by the case's `work` |
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

- **A bare good is the user's default form** (U136-U153, `user_inputs.default_form`): wheat as bread (USDA 172690, whole-wheat from recipe, not enriched), rice polished, maize grain, potato boiled, cow, pig, fish and whale whole as eaten, clam raw, milk, banana and apple raw, lemon as juice, olives as oil, brown sugar, grapes, herbal tea brewed (USDA 173232), table salt. A case may name another form: `GOOD:form` (USDA) or `GOOD:mext:form` (MEXT; niacin equivalents as MEXT gives them). MEXT iodine fills a USDA gap only for a good's first USDA form.
- **Composites** are mixes of records by weight, $c_{\text{mix},k}=\sum_p w_p c_{p,k}/\sum_p w_p$; the report prints each recipe:
  - **cod as eaten** (`BONUS_FISH:whole`, the default fish): fillet 36, liver 5, roe 4 % of round weight (Torry); the meal *mølje* (Brustad 2004). Liver record: lingcod liver; its vitamin A from cod liver oil times the liver's fat; iodine MEXT cod.
  - **herring eaten whole**: the herring record with whole-fish fat, year-round 12 % (user U155), and the Faroese 7.9 % (May) and 19.5 % (August) for reference; energy by Atwater 4/9/4.
  - **fish by region** (`BONUS_FISH:region:<region>`): the user's catch shares (U154) of six categories, each a record: freshwater fish → pond smelt whole (MEXT 10276); small pelagic → herring whole, year-round; large pelagic → bluefin tuna (USDA 173706); demersal → cod as eaten; salmonids → wild Atlantic salmon (173686); other marine fish → Atlantic mackerel (175119).
  - **cow, sheep, deer, horse as eaten**: the user's lean : fat : organs (U117-U120: cow 60 : 20 : 2.5, sheep 60 : 25 : 2.5, deer 70 : 10 : 3, horse 65 : 15 : 2.5), normalised over the parts eaten. Fat is beef suet (170193) for all four, the nearest record; organs split liver : heart : kidneys as the cow's 1.12 : 0.37 : 0.18; deer organs are sheep organs and horse organs cow organs (nearest records).
  - **pig as eaten**: lean 55, back fat 30, liver 2, heart 0.4, kidneys 0.4 (U112-U116).
  - **whale as eaten**: meat 30, blubber 40 (bowhead), liver 2 and other organs 12 (U108-U111); other organs take the liver record, the nearest held, so the whale's vitamin A is an upper value.
- **Caffeine** raises the energy need by 150 kcal at 600 mg, in proportion below (Dulloo 1989; M85); the tool solves again until caffeine eaten and energy need agree.
- **Iron:** no inhibitor is applied; the user marked tea type and tea timing not relevant (M120).
- **Niacin equivalents:** $c_{g,\text{NE}}=\beta_g\,c_{g,\text{niacin}}+1000\,c_{g,\text{tryptophan}}/60$, with $\beta_g=1/3$ for wheat, rice and maize (Carpenter 1983), else 1. Maize treated with alkali is not a case variable (marked not relevant, M120).
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

$$0\le x_g\le\bar a_g,\qquad \bar a_g=\min\!\left(a_g,\ \tfrac{250}{c_{g,\text{fat}}},\ \text{the good's ceiling}\right)$$

with the user's ceilings (U121-U135, `user_inputs.ceilings_g`): lemon 30 g, lemon juice 1,000 g, cheese 1,000, milk 3,000, sugar 300, olives 200, wine 2,000, beer 2,000, salt 20, tea 2,000, coffee 2,000, clams 800, whale 800; fat 250 g from one good (U125).
$$\sum_g c_{g,\text{kcal}}x_g\le E,\qquad \sum_g c_{g,\text{protein}}x_g\le P^{\lim},\qquad \sum_{g\in\text{meat}}x_g\le 1000,\qquad \sum_{g\in\text{fruit}}x_g\le 4518$$

(meat: all cow, pig, sheep, deer and horse together, the user's maximum, U122; fruit: banana, lemon, apple, grapes and raisins, one watermelon, U126).

**Lactose** (U163, M113): raw milk is digestible by everyone, and cultured dairy, cheese and butter are not limited. Only when the case's milk is pasteurised: $x_{\text{milk}}\le \pi\cdot3000+(1-\pi)\cdot13.5/c_{\text{milk,lactose}}$, with $\pi$ the culture's lactase-persistent share (Germanic 0.9, Southern European 0.5, Eastern European 0.75, Indians 0.4, East Asians 0.1, steppe peoples and pastoralists 0.9, Africans 0.3) and 13.5 g the lactose the others tolerate (Wilt 2010).

$$u_k\,m_k\le\sum_g c_{g,k}x_g,\quad u_E\,E^0\le\sum_g c_{g,\text{kcal}}x_g,\quad z_F\,F^0\le\sum_g \sigma_g x_g,\quad zE\le\sum_g c_{g,\text{kcal}}x_g,\quad v_k\,t_k\le\sum_g c_{g,k}x_g,\quad w_k\,t^{A}_k\le\sum_g c_{g,k}x_g$$

with every $u,z,v,w\in[0,1]$ and
- $\sigma_g=\dfrac{SI_g}{100}\,c_{g,\text{kcal}}\,\delta_g$, the fullness of one gram: $SI_g$ the user's satiety index (white bread 100; U001-U088) of the form, else of the good; a composite without its own index takes the energy-weighted index of its parts; $\delta_g=0.8$ for drinks (milk, beer, wine, tea, coffee, lemon juice; U090), else 1;
- $F^0=3000$: the fullness of 3,000 kcal of white bread counts as fed (U089);
- $t^A_k$: the athletes' or heavy labourers' optimum (U173-U189), never below $t_k$; protein 300 g for a 140 kg wrestler, scaled by $W/140$.

Each stage holds the optimum of the stages before it:
1. **Basal function:** $u_E^*=\max u_E$.
2. **Fullness (being fed):** $z_F^*=\max z_F$ (M92, M93).
3. **Energy for labour:** $z^*=\max z$.
4. **Nutrient minima:** $S^*=\max\frac{1}{K'}\sum_k u_k$ over the nutrients with a minimum.
5. **Nutrition:** $\text{MAR}^*=\max\frac1K\sum_k v_k$.
6. **Towards athletes' levels** (M118): $A^*=\max\frac1{K}\sum_k w_k$.
7. **Better stocks first:** $\min\sum_g(1-q_g)\,c_{g,\text{kcal}}\,x_g$.
8. **Dessert** (M88; U091-U093): after the meal, dessert goods still in store are eaten beyond the need, up to $1.0\,E$ more energy (U092), in the user's order: sugar; then fruit (banana, lemon, apple, grapes, raisins); then wine and beer; then tea and olives. Within a group the better good (higher $q_g$) comes first; the ceilings above still hold.

Energy in stages 1-7 is capped at $E$: food beyond the need stays in store (P1) unless it is dessert. Protein counts as energy at 4 kcal/g up to $P^{\lim}$ (P7). Harm ceilings $c^{\max}_k$ are not constraints (P5).

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
| keeping | grams left per day; the good's keep class in `nutrition.json` mapped to the user's class (grain and root → roots and grains 50 %; kept → cured, salted, fermented 15 %; dried 10 %; canned 2 %; fresh → others 90 % a year) | `user_inputs.spoilage_per_year` (U168-U172) |
| repetition | number of goods over 5 % of energy; largest good's energy share | well-being |
| deficiencies | nutrients with intake $<m_k$ | §4 |
| harms | nutrients with intake $>c^{\max}_k$; protein $>2.5\,W$ or $>35\,\%$ of energy; fat $\ge300$ g (sweating) | `nutrients.*.ceiling`, `gut_limits.fat_g` |
| protein per meal | $\frac13\sum_g c_{g,\text{protein}}x_g$, and the hours to absorb it at 10 and 1.3 g an hour | `nutrients.protein.gut_absorption_g_per_h` (Bilsborough and Mann 2006) |
| absorbed zinc | Miller 2013 eq. 2 with dietary zinc, phytate (600 mg/100 g dry for cereals, 20 for tubers), calcium and protein | `absorption.zinc_equation`, `absorption.phytate_mg_per_100g_dry` |
| water to draw | $\text{WT}-\text{water in food}-500-\sum_{\text{drinks}}\text{HI}_g x_g$ | Yamada 2022 (WT), Tipton 2025 (500 ml metabolic), Maughan 2016 (HI: milk 1.5, tea and beer 1.0) |
| alcohol | $7\sum_g c_{g,\text{alcohol}}x_g$ g a week, against Wood 2018 bands | `harm.alcohol_g_per_week` |
| fullness | $\sum_g\sigma_g x_g$ against $F^0$, and goods without an index | §5 |
| dessert | grams eaten as dessert per good; energy of the meal and with dessert | §5 stage 8 |
| athletes' coverage | $A^*$ and each $t^A_k$ | §5 stage 6 |
| strength | the user's anchors (U105): 50 g protein 30 %, $1.6W$ g 80 %, $P^{\lim}$ 200 % (cap); linear in $\ln$ protein between them | `user_inputs.strength_anchors` |
| IQ from iodine | the user's anchors (U107): 150 µg 100, 1,000 µg 115, 5,000 µg 115, 5,000,000 µg 0; below 150 µg towards 70 at 15 µg (the reading of "possibly two standard deviations less"); linear in $\log_{10}$ iodine | `user_inputs.iq_from_iodine_anchors` |
| contaminants | mercury: fish eaten × 0.01-0.20 mg/kg, per kg body weight a day, against 0.3 µg; cadmium: (shellfish + organ share of the animals) × 0.317 mg/kg, a week, against 5 µg; inorganic arsenic: brown rice 0.15, polished 0.10, shellfish 0.01 mg/kg, a week, against 0.06 µg | `user_inputs.contaminants` (U191-U196) |
| well-being list (separate) | goods eaten, sorted: hyper-palatable first (Fazzino 2019 criteria from composition), then lighter (lower kcal per g: shorter stomach residence, Hunt and Stubbs 1975) | record 2e |

## 8. Cases

The case report is `food_model_cases_report.md`, written by `plan/tools/food_model.py food_model_cases.json --md food_model_cases_report.md`. For each case it gives first the inputs (person, climate and culture variables; every good available with its composition record, amount and energy, protein and fat per 100 g), then the results, every nutrient with intake, target, minimum, ceiling and the goods it comes from, the keeping of what is left, and the well-being list. No table is typed by hand.

## 9. What the model does not yet do, and the user's inputs not applied (R72.2)

| Item | Why |
|---|---|
| Game effects (U100-U104, U106): labour to production, deficiency and harms to health, MAR to growth, nutrition to commerce, starving to population | design inputs kept verbatim in `user_inputs.game_effects`; labour to production "needs to be discussed" (U100); they map model outputs to the game and change no intake |
| Rich city (U094-U099): cheese 10 kg milk per kg, butter 20, bread 0.6 kg per kg grain, 70 % of surplus milk to dairy, sugar 50 g a day | stored in `user_inputs.rich_city`; the conversion runs on a city's stores between turns, outside the daily diet; a case can name cheese, butter or bread directly |
| Body weight by diet (U161) | the user's text is kept; body weight is a case input, and a diet-driven weight needs the growth formula (P2) |
| Fish bones eaten (U156: only small fish, cooked or fermented) | already the case: small fish enter whole (pond smelt, loach, mezashi); the other fish records hold no bone |
| Not relevant (U162, U164-U167, U197) | children and their adult equivalent, tea type, tea timing, maize alkali, pork cooking, parasite risk: removed from the model |
| Iodine above sufficiency (U190) | the user's IQ anchors are applied as given; no study is cited for them |
| Health effects in the well-being list (M91) | deficiencies, harm flags and contaminants are listed beside it; no combined measure until the game effects are decided |
| Whale organs other than liver | no record held; the liver record stands in (upper value for vitamin A) |

## 10. Benefits above the optimum and harms of one-sided diets (R70, applied in R72)

The proposal of R70 is applied with the user's values (M120): stage 6 raises each nutrient's adequacy towards the athletes' optimum (U173-U189), and contaminants, strength and IQ are outputs (§7). Iodine above its ceiling stays a reported harm. Pork parasites were marked not relevant (U197).
