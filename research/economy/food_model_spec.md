# The food model: specification (version 4, M101)

Version 4 is a new model built from first principles. It replaces versions 1-3; their history is in the round files and in section 9. The reference implementation is `plan/tools/food_model.py`, which solves the model exactly. A worked example is in `food_model_worked_example.md`.

## 1. Principles

| | Principle | What it fixes in the model |
|---|---|---|
| (P1) | **Conservation.** A city eats only what it holds. | consumption ≤ availability |
| (P2) | **Physiology bounds intake.** The stomach (fullness), energy turnover, the liver's capacity for protein and the tolerance for single foods set ceilings. | four constraints and a ceiling per good |
| (P3) | **Needs are absolute.** Energy follows work; nutrients and water have fixed daily needs. | the adequacy terms |
| (P4) | **Priority** (M88, M96). Nutrition first: being fed and covering needs. Then well-being. Nutrition and well-being are separate quantities, ordered, never added. | a lexicographic program |
| (P5) | **Harm is a consequence, not a motive.** People do not ration alcohol or tobacco by their harm; the harm is an outcome. | harm terms as outputs |
| (P6) | **The city as a whole** (M101). All quantities are per person of the city's population, averaged. Body reserves belong to the growth formula; seasons are below the turn length. | no classes, stores or seasons |

## 2. Sets

| Symbol | Meaning |
|---|---|
| $\mathcal G$, index $g$ | food, drink and stimulant goods |
| $\mathcal S\subset\mathcal G$ | staples: Wheat, Rice, Corn, Potato, Salt |
| $\mathcal W=\mathcal G\setminus\mathcal S$ | goods that also give well-being: animal foods, fruit, sugar, olives, wine, beer, tea, coffee, tobacco |
| $\mathcal D\subset\mathcal G$ | drinks: Dairy, Wine, Alcohol, Tea, Coffee |
| $\mathcal T\subset\mathcal D$ | brewed stimulants without energy: Tea, Coffee |
| $\mathcal F\subset\mathcal G$ | fruit: Apple, Banana, Lemon |
| $\mathcal H\subset\mathcal G$ | harmful goods: Wine, Alcohol (alcohol); Tobacco |
| $\mathcal I$, index $i$ | adequacy components (15): fullness, energy, digestible protein, vitamins C, A, B1, B3, folate, B12, iron, zinc, calcium, iodine, potassium, sodium |

## 3. Parameters

### 3a. Per good (data files; one row per good)

| Symbol | Meaning | Unit | Source |
|---|---|---|---|
| $e_g$ | energy per gram as stored, eaten share included | kcal/g | nutrition.json (FAO) |
| $p_g,\ f_g$ | protein, fat per gram | g/g | nutrition.json |
| $d_g$ | protein quality (DIAAS, capped at 1) | – | nutrition.json |
| $n_{gi}$ | nutrient $i$ per gram, after bioavailability $b_{gi}$ | mg or µg/g | USDA SR Legacy, MEXT; $b_{gi}$: iron 0.18/0.16 animal, 0.10/0.16 plant (FAO/WHO 2004); maize niacin 1/3 (Carpenter 1983); otherwise 1 |
| $\sigma_g$ | fullness per kcal (white bread = 1); drinks × 0.5 | – | Holt et al. 1995 where measured; fitted formula otherwise (`satiety_fit.py`) |
| $\omega_g$ | water per gram of food eaten | ml/g | USDA SR Legacy |
| $h_g$ | hydration index ($g\in\mathcal D$): hydration from a volume of the drink relative to the same volume of water | – | nutrition.json (milk 1.5) |
| $u_g$ | ceiling per good: $\min(250\ \text{g}/f_g,\ 3{,}000\ \text{g milk},\ 116\ \text{g lemon})$ | g/(p·d) | the user (M86, M93); estimate (lemons) |
| $\alpha_g$ | harmful substance per gram ($g\in\mathcal H$): alcohol; tobacco | g/g | USDA SR Legacy; tobacco to add |
| $\delta_g$ | share of a year's leftover that spoils | – | nutrition.json (FAO storage) |
| $\ell_g\chi_g$ | caffeine per gram ($g\in\mathcal T$) | mg/g | MEXT brewing: tea 43 L/kg × 200 mg/L, coffee 15 L/kg × 600 mg/L |

### 3b. Scalars

| Symbol | Meaning | Value | Source |
|---|---|---|---|
| $B$ | basal metabolic rate of the average adult | 1,536 kcal/(p·d) | FAO/WHO/UNU 2004; EFSA weights |
| $\Lambda_k$ | activity level of work kind $k$ (vigorous, active, sedentary) | 2.25, 1.76, 1.53 | FAO 2004, Table 5.1 |
| $\Lambda^{\max}$ | highest sustainable activity level | 2.40 | FAO 2004, Table 5.3 |
| $\kappa,\gamma$ | caffeine: extra expenditure at the dose | 150 kcal at 600 mg | Dulloo et al. 1989 |
| $\bar\sigma$ | fullness per kcal of an average food | 1.36 | mean of Holt's 38 foods |
| $P^{\max}$ | protein the liver can handle | 3.6 g/kg × 63.3 kg = 228 g/(p·d) | Bilsborough and Mann 2006; EFSA mean weight |
| $Q^{\mathcal F}$ | all fruit | 4,518 g/(p·d) | one watermelon (USDA portion; M86) |
| $r_i$ | daily need of component $i$ | per nutrient | EFSA 2017; Japanese DRI 2025 (sodium) |
| $W^{\mathrm{need}}$ | total water | 2,250 ml/(p·d) | EFSA 2010 |
| $m$ | unit of diminishing returns in well-being | 100 kcal | definition |

## 4. Inputs and variables

| Symbol | Meaning | Domain | Unit |
|---|---|---|---|
| $N$ | people of the city | $N>0$ | persons |
| $S_g$ | stock available this year | $S_g\ge0$ | t |
| $w_k$ | share of people in work kind $k$ | $\sum_kw_k=1$ | – |
| $q_g$ | **decision:** grams eaten per person a day | $q_g\ge0$ | g/(p·d) |

## 5. Definitions

**Availability:**
$$
a_g=\frac{10^6\,S_g}{365\,N} \tag{1}
$$

**Stimulants (stage 0)** are drunk while available, up to the dose $\gamma$:
$$
q_g=\min\Bigl(a_g,\ \frac{\gamma-\text{caffeine already drunk}}{\ell_g\chi_g}\Bigr)\quad(g\in\mathcal T),\qquad c=\frac{\sum_{g\in\mathcal T}\ell_g\chi_gq_g}{\gamma} \tag{2}
$$

**Need and ceilings:**
$$
E^{\mathrm{need}}=B\sum_kw_k\Lambda_k+\kappa c,\qquad E^{\max}=B\Lambda^{\max}+\kappa c \tag{3}
$$
$$
r_{\mathrm{energy}}=E^{\mathrm{need}},\qquad r_{\mathrm{fullness}}=\bar\sigma E^{\mathrm{need}},\qquad F^{\max}=\bar\sigma E^{\max} \tag{4}
$$

**What a diet $\mathbf q$ delivers:**
$$
E(\mathbf q)=\sum_ge_gq_g,\quad F(\mathbf q)=\sum_g\sigma_ge_gq_g,\quad P(\mathbf q)=\sum_gp_gq_g,\quad P^{\mathrm d}(\mathbf q)=\sum_gd_gp_gq_g \tag{5}
$$
$$
c_i(\mathbf q)=\frac{\text{amount of } i \text{ delivered}}{r_i}:\quad c_{\mathrm{fullness}}=\frac{F}{r_{\mathrm{fullness}}},\ c_{\mathrm{energy}}=\frac{E}{r_{\mathrm{energy}}},\ c_{\mathrm{protein}}=\frac{P^{\mathrm d}}{r_{\mathrm{protein}}},\ c_i=\frac{\sum_gn_{gi}q_g}{r_i} \tag{6}
$$

**Nutrition adequacy:** the mean adequacy ratio. Each component counts up to its need, so a surplus of one cannot make up a lack of another:
$$
A(\mathbf q)=\frac{1}{\lvert\mathcal I\rvert}\sum_{i\in\mathcal I}\min\bigl(1,\ c_i(\mathbf q)\bigr) \tag{7}
$$

**Well-being:** diminishing returns per 100 kcal of each good, so variety pleases more than repetition:
$$
\Psi(\mathbf q)=\sum_{g\in\mathcal W}\ln\Bigl(1+\frac{e_gq_g}{m}\Bigr) \tag{8}
$$

## 6. The program

**Feasible diets:**
$$
\mathcal Q=\Bigl\{\mathbf q:\ 0\le q_g\le\min(a_g,u_g);\ \ F(\mathbf q)\le F^{\max};\ \ E(\mathbf q)\le E^{\max};\ \ P(\mathbf q)\le P^{\max};\ \ \sum_{g\in\mathcal F}q_g\le Q^{\mathcal F}\Bigr\} \tag{9}
$$

**Three stages, each keeping the optimum of the one before** (lexicographic optimisation):
$$
\begin{aligned}
\text{Stage 1 (nutrition):}\quad & A^*=\max_{\mathbf q\in\mathcal Q}A(\mathbf q) && (10)\\
\text{Stage 2 (well-being):}\quad & \Psi^*=\max_{\mathbf q\in\mathcal Q}\ \Psi(\mathbf q)\ \ \text{s.t.}\ \ A(\mathbf q)\ge A^* && (11)\\
\text{Stage 3 (even use of supply):}\quad & \mathbf q^*=\arg\min_{\mathbf q\in\mathcal Q}\ \sum_g\frac{q_g}{a_g}\ \ \text{s.t.}\ \ A\ge A^*,\ \Psi\ge\Psi^* && (12)
\end{aligned}
$$

- **Stage 3** decides only among diets equal in nutrition and well-being: it takes from the more plentiful stocks.
- **Each stage is a linear program.** In (7), $\min(1,c_i)$ becomes auxiliary variables $y_i\le1$, $y_i\le c_i$. In (8), $\ln(1+\cdot)$ becomes a concave piecewise-linear function with breakpoints at 0.5, 1, 2, 3, 5, 8, 12, 20 and 30 units of 100 kcal.
- **The game** solves the same three small programs, about 25 goods and 20 constraints per city per yearly step, with a bounded simplex method. The reference implementation uses HiGHS.

## 7. Outcomes

$$
x=\frac{E(\mathbf q^*)}{E^{\mathrm{need}}},\qquad \textit{fed}=\frac{F(\mathbf q^*)}{r_{\mathrm{fullness}}},\qquad c_i=c_i(\mathbf q^*),\qquad A^*,\ \Psi^* \tag{13}
$$
$$
\textit{harm}_{\mathrm{alcohol}}=\sum_{g\in\mathcal H}\alpha_gq^*_g,\qquad \textit{harm}_{\mathrm{tobacco}}=\alpha_{\mathrm{tob}}q^*_{\mathrm{tob}} \tag{14}
$$
$$
W^{\mathrm{in}}=\sum_{g\notin\mathcal D}\omega_gq^*_g+\sum_{g\in\mathcal D}h_gq^*_g,\qquad W^{\mathrm{plain}}=\max\bigl(0,\ W^{\mathrm{need}}-W^{\mathrm{in}}\bigr) \tag{15}
$$
$$
\textit{work}=\min(1,\ x) \tag{16}
$$
$$
U_g=\frac{365\,N\,q^*_g}{10^6},\qquad L_g=S_g-U_g,\qquad D_g=\delta_gL_g \tag{17}
$$
$$
\lambda^{(1)}_g=\frac{\partial A^*}{\partial a_g},\qquad \lambda^{(2)}_g=\frac{\partial\Psi^*}{\partial a_g} \tag{18}
$$

- **(13)** $x$ (energy sufficiency) feeds the growth formula, which also holds body reserves. $\textit{fed}$, the coverage $c_i$ and $A^*$ feed fertility and the deficiency burden. $\Psi^*$ feeds the happiness line.
- **(14)** feeds the health burden. Its harm coefficients are still to be sourced.
- **(15)** In the hydration equation, $h_g$ counts each ml of a drink as $h_g$ ml of water: 1 L of milk gives 1.5 L of water equivalent. Plain water comes from the city's supply (D31).
- **(16)** A shortfall of energy lowers work. Surplus energy goes to activity and to the growth formula, not to extra output.
- **(18)** These are the shadow values of the stocks: what one more gram of stock would add to adequacy, or to well-being. They are zero for goods in surplus. They are the basis for prices (section 8).

## 8. Prices (interface, to be established)

The model gives each good two scarcity values per city, $\lambda^{(1)}_g$ and $\lambda^{(2)}_g$, in adequacy and well-being per gram.
- A good that is plentiful has value 0. A good whose stock limits nutrition or well-being has a positive value.
- These are the quantities a price must reflect for the city's population as a whole.
- How they become gold prices in the game (a scale per currency, costs of production, trade between cities) belongs to the goods economy and is not set here.

## 9. Change log

| Version | Change |
|---|---|
| 1-3 (M85-M98) | the earlier models; history in `round_m85.md` to `round_m96.md`, `food_model_assessment.md` |
| 4 (M101) | **New model.** |

**Removed in version 4:**
- the satisfaction factor $s_g$ and its constants;
- the nutrient score $\nu_g$ and $E^{\mathrm{ref}}$;
- the well-being formula $\beta_g$ and its five weights and lightness constant;
- the keys $K^{(1)},K^{(2)}$, the two passes and the greedy algorithm;
- servings $m_g$ per good;
- the work bonus $\Omega$ and the activity floor in work;
- the iron absorption line ($a_0,a_1$);
- the salt ceiling;
- the protein ceiling tied to $E^{\max}$.

**Added in version 4:**
- the mean adequacy ratio $A$ (7) with fullness and energy as components;
- well-being $\Psi$ (8) per 100 kcal;
- the staples set $\mathcal S$ and the well-being set $\mathcal W$;
- the lexicographic program (10)-(12), solved exactly;
- bioavailability $b_{gi}$;
- the liver ceiling $P^{\max}$;
- harm outcomes (14);
- shadow values (18).

**Corrected in version 4:**
- F15 of the assessment is withdrawn: the hydration index is hydration relative to the same volume of water, as used in (15).
- Body reserves, seasons and classes are not part of this model (P6).
