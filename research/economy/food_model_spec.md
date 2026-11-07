# The food model: specification (version 3, M98)

Version 3 restates version 2 in standard mathematical notation. No variable, parameter or equation changed (change log, section 8). The code (`plan/tools/food_model.py`) implements equations (1)-(30) and Algorithm 1. A full worked example in the same notation is in `food_model_worked_example.md`.

## 0. Conventions

| Convention | Rule here | Basis |
|---|---|---|
| Order of declaration | sets and indices, then parameters (given data), then variables, then equations, then the procedure. Nothing is used before it is declared | the algebraic modelling layout of the GAMS tutorial (indices, given data, decision variables, constraints) |
| Symbols | one Latin or Greek letter per quantity, with sub- and superscripts; italic in the formulas | ISO/IEC 80000: quantity symbols are single italic letters |
| Legend | every symbol has a name, a domain (the set it is indexed over), a unit and a source | GAMS: each entity has a domain and a description; units stated with every quantity |
| Procedure | an algorithm with numbered lines; `←` is assignment | the usual pseudocode form |
| Units | in square brackets; `d` = day, `t` = tonne, `p` = person | |

## 1. The model as a map

For one city and one year:

$$
\Phi:\;(N,\;\mathbf S,\;\mathbf w)\;\longmapsto\;\bigl(\mathbf q,\;\textit{fed},\;x,\;\mathbf c,\;W^{\mathrm{plain}},\;\mathbf L,\;\mathbf D\bigr)
$$

**Inputs:**
- the people $N$;
- the stocks $\mathbf S=(S_g)$;
- the shares of people in each kind of work $\mathbf w=(w_k)$.

**Outputs:**
- grams eaten per person a day $\mathbf q$;
- how fed the people are, $\textit{fed}$;
- energy sufficiency $x$;
- nutrient coverage $\mathbf c$;
- plain water still needed $W^{\mathrm{plain}}$;
- stock left $\mathbf L$ and spoiled $\mathbf D$.

The model has five modules: availability (M1), need and bounds (M2), indicators per good (M3), allocation (M4), outcomes (M5).

## 2. Sets and indices

| Symbol | Meaning | Members |
|---|---|---|
| $\mathcal G$, index $g$ | food and drink goods | the branch's food goods (nutrition.json) |
| $\mathcal G^{\mathrm{A}}\subset\mathcal G$ | animal goods | Cow, Pig, Sheep, Deer, Horse, Fish, Clam, Crab, Shrimp, Whale, Dairy |
| $\mathcal G^{\mathrm{D}}\subset\mathcal G$ | drinks | Dairy, Wine, Alcohol, Tea, Coffee |
| $\mathcal G^{\mathrm{F}}\subset\mathcal G$ | fruit | Apple, Banana, Lemon |
| $\mathcal G^{\mathrm{T}}\subset\mathcal G$ | brewed drinks (no energy) | Tea, Coffee |
| $\mathcal G^{\mathrm{E}}=\mathcal G\setminus(\mathcal G^{\mathrm T}\cup\{\text{Salt}\})$ | goods eaten for energy | |
| $\mathcal I$, index $i$ | nutrients, $\lvert\mathcal I\rvert=13$ | protein, vitamin C, vitamin A, thiamin, niacin, folate, B12, iron, zinc, calcium, iodine, potassium, sodium |
| $\mathcal K$, index $k$ | kinds of work | vigorous, active, sedentary |
| $\mathcal P$, index $\rho$ | passes of the allocation | 1 (nutrition), 2 (well-being) |

## 3. Parameters (given data)

### 3a. Per good $g\in\mathcal G$ (data files)

| Symbol | Meaning | Unit | Source |
|---|---|---|---|
| $\varepsilon_g$ | energy per 100 g as stored | kcal / 100 g | nutrition.json (FAO) |
| $\pi_g$ | protein per 100 g as stored | g / 100 g | nutrition.json |
| $\varphi_g$ | fat per 100 g as stored | g / 100 g | nutrition.json |
| $\eta_g$ | edible share | – | nutrition.json |
| $\delta_g$ | protein quality (DIAAS); defaults 1.0 animal, 0.44 plant | – | nutrition.json |
| $n_{gi}$ | nutrient $i$ per 100 g eaten | mg or µg / 100 g | nutrient_profiles.json (USDA SR Legacy, MEXT) |
| $\epsilon^{\mathrm U}_g$ | energy per 100 g of the USDA form behind $n_{gi}$ | kcal / 100 g | nutrient_profiles.json |
| $\omega_g$ | water per 100 g eaten | g / 100 g | nutrient_profiles.json |
| $\theta_g$ | sugars per 100 g | g / 100 g | USDA SR Legacy |
| $\alpha_g$ | alcohol per 100 g | g / 100 g | USDA SR Legacy |
| $h_g$ | hydration index (drinks) | – | nutrition.json |
| $m_g$ | one serving | g | USDA household portions |
| $H_g$ | Holt satiety index, where measured (white bread = 100) | – | Holt et al. 1995 |
| $\bar\delta_g$ | spoilage of a year's leftover by keeping form | – | nutrition.json (FAO storage) |
| $\ell_g,\;\chi_g$ | brewing: litres of drink per kg; caffeine per litre ($g\in\mathcal G^{\mathrm T}$) | L/kg; mg/L | MEXT (43, 200 tea; 15, 600 coffee) |

### 3b. Scalars

| Symbol | Meaning | Value | Unit | Source |
|---|---|---|---|---|
| $B$ | basal metabolic rate of the abstracted adult | 1,536 | kcal / (p·d) | FAO/WHO/UNU 2004; EFSA weights |
| $\Lambda_k$ | activity level of work kind $k$ | 2.25, 1.76, 1.53 | – | FAO 2004, Table 5.1 |
| $\Lambda^{\min},\Lambda^{\max}$ | activity range | 1.40, 2.40 | – | FAO 2004, Table 5.3 |
| $\kappa$ | energy effect of caffeine at the dose $\gamma$ | 150 | kcal / (p·d) | Dulloo et al. 1989 |
| $\gamma$ | caffeine dose for the full effect | 600 | mg / (p·d) | Dulloo et al. 1989 |
| $E^{\mathrm{ref}}$ | reference energy for nutrient densities | 2,600 | kcal / (p·d) | nutrient_needs.json |
| $r_i$ | daily need of nutrient $i$ | per nutrient | mg, µg or g / (p·d) | EFSA 2017; Japanese DRI 2025 (sodium) |
| $\bar\sigma$ | mean Holt index of Holt's 38 foods ÷ 100 | 1.36 | – | Holt et al. 1995 |
| $\lambda$ | fullness factor of drinks | 0.5 | – | estimate (PMID 14649371) |
| $b_0,\dots,b_4$ | fitted satiety formula | 0.0796, 0.2218, 0.6614, 0.0308, −0.2127 | – | fitted to 29 Holt foods (`satiety_fit.py`) |
| $\kappa_s,\;\bar p,\;\bar\delta$ | protein factor: slope, bread's protein share, wheat's DIAAS | 2.0, 0.146, 0.44 | – | fitted to Holt's beef against bread |
| $u_1,\dots,u_5$ | well-being weights | 1, 2, 1, 1, 0.5 | – | estimates on sourced effects |
| $\beta^{\mathrm W}$ | water per kcal at which lightness is full | 3 | g / kcal | estimate |
| $\pi^{\max}$ | protein ceiling, share of energy | 0.35 | – | Bilsborough and Mann 2006 |
| $\Phi^{\max}$ | fat from one good | 250 | g / (p·d) | the user (M93) |
| $Q^{\mathrm{milk}},Q^{\mathrm{lemon}},Q^{\mathrm{fruit}},Q^{\mathrm{salt}}$ | ceilings: milk, lemons, all fruit, salt | 3,000; 116; 4,518; 10 | g / (p·d) | the user; estimate; USDA watermelon; estimate |
| $W^{\mathrm{need}}$ | total water need | 2,250 | ml / (p·d) | EFSA 2010 |
| $a_0,a_1,a^{\mathrm{ref}}$ | iron absorption: base, slope by animal protein share, EFSA's assumption | 0.10, 0.08, 0.16 | – | FAO/WHO 2004; EFSA 2017 |
| $\Omega$ | ceiling of the work factor | 1.20 | – | estimate |
| $\Delta$ | step of the allocation | 10 | kcal | numerical |

## 4. Variables

| Symbol | Meaning | Domain | Unit |
|---|---|---|---|
| $q_g$ | grams eaten per person a day | $g\in\mathcal G$, $q_g\ge0$ | g / (p·d) |
| $E$ | energy eaten | $E\ge0$ | kcal / (p·d) |
| $F$ | fullness eaten | $F\ge0$ | fullness units (white-bread kcal) / (p·d) |
| $P$ | protein eaten | $P\ge0$ | g / (p·d) |
| $R$ | fruit eaten | $R\ge0$ | g / (p·d) |

## 5. Equations

### M1. Availability

$$
a_g=\frac{S_g\cdot10^{6}}{365\,N}\qquad g\in\mathcal G \tag{1}
$$

### M2. Need and bounds

$$
\begin{aligned}
q_g&=\min\!\Bigl(a_g,\;\frac{1000\,\bigl(\gamma-\textstyle\sum_{g'<g}q_{g'}\ell_{g'}\chi_{g'}/1000\bigr)}{\ell_g\chi_g}\Bigr)\qquad g\in\mathcal G^{\mathrm T}\\
c&=\min\!\Bigl(1,\;\frac{1}{\gamma}\sum_{g\in\mathcal G^{\mathrm T}} q_g\,\frac{\ell_g\chi_g}{1000}\Bigr)
\end{aligned} \tag{2}
$$

$$
\Lambda^{\mathrm w}=\sum_{k\in\mathcal K} w_k\Lambda_k \tag{3}
$$

$$
E^{\mathrm{need}}=B\,\Lambda^{\mathrm w}+\kappa c \tag{4}
$$

$$
E^{\max}=B\,\Lambda^{\max}+\kappa c \tag{5}
$$

$$
F^{\mathrm{fed}}=\bar\sigma E^{\mathrm{need}},\qquad F^{\max}=\bar\sigma E^{\max} \tag{6}
$$

$$
P^{\max}=\frac{\pi^{\max}E^{\max}}{4} \tag{7}
$$

$$
q_{\mathrm{salt}}=\min(a_{\mathrm{salt}},Q^{\mathrm{salt}}) \tag{8}
$$

### M3. Indicators per good $g\in\mathcal G^{\mathrm E}$

**Energy, protein and fat per gram eaten:**

$$
e_g=\frac{\varepsilon_g\eta_g}{100},\qquad \hat\pi_g=\frac{\pi_g\eta_g}{100},\qquad \hat\varphi_g=\frac{\varphi_g\eta_g}{100} \tag{9}
$$

**Energy shares:**

$$
p_g=\frac{4\pi_g}{\varepsilon_g},\quad f_g=\min\!\Bigl(1,\frac{9\varphi_g}{\varepsilon_g}\Bigr),\quad l_g=\frac{7\alpha_g}{\varepsilon_g},\quad k_g=\max(0,\,1-f_g-p_g-l_g),\quad z_g=\frac{4\theta_g}{\varepsilon_g} \tag{10}
$$

**Fullness per kcal:**

$$
\sigma_g=\Bigl[\frac{H_g}{100}\ \text{if measured, else}\ \exp\bigl(b_0+b_1\ln\tfrac{W_g}{W_{\mathrm{bread}}}+b_2p_g+b_3\,\mathrm{fib}_g+b_4f_g\bigr)\Bigr]\cdot\begin{cases}\lambda& g\in\mathcal G^{\mathrm D}\\1&\text{otherwise}\end{cases} \tag{11}
$$

Here $W_g$ is the grams in 240 kcal and $\mathrm{fib}_g$ the fibre in g per 100 kcal.

**Satisfaction (protein factor):**

$$
s_g=\frac{1+\kappa_s\,p_g\min(\delta_g,1)}{1+\kappa_s\,\bar p\,\bar\delta} \tag{12}
$$

**Nutrient density against the requirement density:**

$$
\nu_g=\frac{1}{\lvert\mathcal I\rvert}\sum_{i\in\mathcal I}\min\!\Bigl(1,\;\frac{n_{gi}/\epsilon^{\mathrm U}_g}{r_i/E^{\mathrm{ref}}}\Bigr) \tag{13}
$$

For protein, $n_{gi}/\epsilon^{\mathrm U}_g$ is replaced by $\pi_g/\varepsilon_g$.

**Well-being:**

$$
\beta_g=u_1z_g+u_2f_gk_g+u_3l_g+u_4\min\!\Bigl(1,\frac{\omega_g/\epsilon^{\mathrm U}_g}{\beta^{\mathrm W}}\Bigr)-u_5f_g \tag{14}
$$

**The two keys** (two separate sorted lists, M96):

$$
K^{(1)}_g=s_g+\nu_g\quad\text{(nutrition)},\qquad K^{(2)}_g=\beta_g\quad\text{(well-being)} \tag{15}
$$

**The ceiling of each good:**

$$
\bar q_g=\min\Bigl(a_g,\;\frac{\Phi^{\max}}{\hat\varphi_g},\;Q^{\mathrm{milk}}\,[g=\text{Dairy}],\;Q^{\mathrm{lemon}}\,[g=\text{Lemon}]\Bigr) \tag{16}
$$

A bracketed condition means the term applies only to that good.

### M4. Allocation

The marginal value of the next $\Delta$ kcal of good $g$ in pass $\rho$ falls with what has been eaten:

$$
\mu^{(\rho)}_g(q_g)=\frac{K^{(\rho)}_g}{1+q_g/m_g} \tag{17}
$$

A good is admissible when the next step keeps it within its own ceiling, the protein ceiling and the fruit ceiling:

$$
\mathcal A(\mathbf q)=\Bigl\{g\in\mathcal G^{\mathrm E}:\;q_g+\tfrac{\Delta}{e_g}\le\bar q_g,\;\;P+\tfrac{\Delta}{e_g}\hat\pi_g\le P^{\max},\;\;[g\in\mathcal G^{\mathrm F}]\Rightarrow R+\tfrac{\Delta}{e_g}\eta_g\le Q^{\mathrm{fruit}}\Bigr\} \tag{18}
$$

**Algorithm 1 (allocation):**
```
 1  q_g ← 0 for all g ∈ G^E;  E ← 0;  F ← 0;  P ← 0;  R ← 0
 2  for ρ in (1, 2):
 3      F^stop ← F^fed if ρ = 1 else F^max
 4      while E < E^max and F < F^stop:
 5          A* ← { g ∈ A(q) : K^(ρ)_g > 0 }
 6          if A* is empty: break
 7          g* ← argmax over g ∈ A* of μ^(ρ)_g(q_g)
 8          q_g* ← q_g* + Δ / e_g*
 9          E ← E + Δ;   F ← F + Δ σ_g*;   P ← P + (Δ / e_g*) π̂_g*
10          if g* ∈ G^F: R ← R + (Δ / e_g*) η_g*
11  return q, E, F, P
```

### M5. Outcomes

$$
\textit{fed}=\frac{F}{F^{\mathrm{fed}}},\qquad x=\frac{E}{E^{\mathrm{need}}} \tag{19}
$$

$$
I_i=\sum_{g\in\mathcal G}\frac{q_g\eta_g}{100}\,n_{gi}\quad(\text{for } g\in\mathcal G^{\mathrm T}\text{, } q_g\eta_g \text{ is replaced by } q_g\ell_g) \tag{20}
$$

$$
a^{\mathrm{Fe}}=a_0+a_1\frac{\sum_{g\in\mathcal G^{\mathrm A}}q_g\hat\pi_g}{P} \tag{21}
$$

$$
c_i=\frac{I_i}{r_i}\cdot\begin{cases}a^{\mathrm{Fe}}/a^{\mathrm{ref}}&i=\text{iron}\\1&\text{otherwise}\end{cases} \tag{22}
$$

$$
W^{\mathrm{food}}=\sum_{g\notin\mathcal G^{\mathrm D}}\frac{q_g\eta_g}{100}\,\omega_g,\qquad
W^{\mathrm{drink}}=\sum_{g\in\mathcal G^{\mathrm D}\setminus\mathcal G^{\mathrm T}}q_g\eta_gh_g+\sum_{g\in\mathcal G^{\mathrm T}}q_g\ell_g \tag{23}
$$

$$
W^{\mathrm{plain}}=\max\bigl(0,\;W^{\mathrm{need}}-W^{\mathrm{food}}-W^{\mathrm{drink}}\bigr) \tag{24}
$$

$$
\Lambda^{\mathrm{act}}=\min\bigl(\Lambda^{\max},\max(\Lambda^{\min},E/B)\bigr) \tag{25}
$$

$$
\textit{work}=\min\Bigl(\Omega,\max\bigl(0,\tfrac{\Lambda^{\mathrm{act}}-\Lambda^{\min}}{\Lambda^{\mathrm w}-\Lambda^{\min}}\bigr)\Bigr) \tag{26}
$$

$$
U_g=\frac{365\,N\,q_g}{10^{6}},\qquad L_g=S_g-U_g,\qquad D_g=\bar\delta_g L_g \tag{27}
$$

The Fish, Cow and Pig goods are composites (whole animals). Their $\varepsilon,\pi,\varphi,n_{gi}$ are weighted means of their parts:

$$
\varepsilon_g=\sum_j\xi_{gj}\varepsilon_{gj},\ \dots \qquad \text{Fish: } \xi=(0.50\ \text{herring},\ 0.45\ \text{cod},\ 0.05\ \text{liver});\ \text{Cow, Pig: } (0.97\ \text{meat},\ 0.03\ \text{liver}) \tag{28}
$$

## 6. Properties

**(P1) Energy at a fullness stop.** From Algorithm 1, line 9, $F=\sum_g\sigma_g\,e_gq_g$ and $E=\sum_g e_gq_g$. When eating stops because $F$ reached $F^{\mathrm{stop}}$:

$$
E=\frac{F^{\mathrm{stop}}}{\tilde\sigma},\qquad \tilde\sigma=\frac{\sum_g\sigma_g\,e_gq_g}{\sum_g e_gq_g}, \tag{29}
$$

the energy-weighted mean fullness of the diet. Filling diets give less energy at the same fullness.

**(P2) What each pass optimises.** The marginal value (17) is the derivative, per kcal, of

$$
V^{(\rho)}_g(q_g)=K^{(\rho)}_g\,e_g\,m_g\ln\!\Bigl(1+\frac{q_g}{m_g}\Bigr). \tag{30}
$$

Taking always the largest marginal value in equal energy steps is the greedy method for a separable concave objective under one linear budget. So each pass approximates, to within one step $\Delta$:

$$
\max_{\mathbf q}\ \sum_{g}V^{(\rho)}_g(q_g)\quad\text{subject to}\quad \sum_g e_gq_g\le E^{(\rho)},\ \ q_g\le\bar q_g,\ \ P\le P^{\max},\ \ R\le Q^{\mathrm{fruit}},
$$

where $E^{(\rho)}$ is the energy at which the pass stops (fullness or $E^{\max}$).

**(P3) Step overshoot.** $F$ and $E$ can exceed their stop by at most one step: $\Delta\max_g\sigma_g$ and $\Delta$.

## 7. What the outcomes feed (proposed, M93)

| Outcome | Feeds |
|---|---|
| $\textit{fed}$ | fertility and the famine term of the population model |
| $x$, $\textit{work}$ | the weakness of the underfed; physical output |
| $c_i$ | the deficiency burden, the nutrients factor of fertility, output |
| $W^{\mathrm{plain}}$ | demand on the water supply (D31) |
| $L_g$, $D_g$ | stock, storage, trade, recipes |

## 8. Change log

| Version (round) | Variable | Change | Before → after | Reason |
|---|---|---|---|---|
| 1 (M85) | $E^{\mathrm{need}}$ | changed | 2,600 kcal → (4) | the user: activity and stimulants |
| 1 (M86) | $E^{\max}$ | added | → (5) | FAO PAL ceiling |
| 1 (M86) | $x$ | changed | satiety ÷ 2,600 → $E/E^{\mathrm{need}}$ (19) | need varies with work |
| 1 (M86) | $\textit{work}$, $\Omega$ | added | → (26) | Fogel |
| 1 (M87) | $a_g$ | added | → (1) | the goods pass counts tonnes |
| 1 (M87) | $c_i$, $a^{\mathrm{Fe}}$ | added | → (20)-(22) | deficiency model |
| 1 (M88) | headroom, food mass, drink cap | removed | 0.15, 6 kg, 3.5 L → none | the user |
| 1 (M88) | $Q^{\mathrm{fruit}}$; brewing $\ell_g,\chi_g$; $\gamma$ | added | → 4,518 g; MEXT; 600 mg | the user |
| 1 (M91) | $W^{\mathrm{need}}$, (23)-(24) | changed | drink 1.8 L → total water 2,250 ml | the user: one hydration equation |
| 1 (M91) | $m_g$, (17) | added | → diminishing returns per serving | the user: no tiers |
| 1 (M91) | $\sigma_g$ formula, $\lambda$ | added | → (11) | the user: a correct formula |
| 1 (M91) | $\beta_g$ | added | → (14) | the user: well-being |
| 1 (M91) | Fish | changed | fillet → composite (28) | the user: whole animal |
| 1 (M92) | $F^{\max}$, $\bar\sigma$; $Q^{\mathrm{lemon}}$ | added | → (6); 116 g | the user: fullness; lemons |
| 1 (M93) | $\Phi^{\max}$ | changed | 100 → 250 g | the user |
| 1 (M93) | $\textit{fed}$, $F^{\mathrm{fed}}$ | added | → (6), (19) | the user: satiety is the baseline |
| 1 (M94) | $\nu_g$ | changed | per 100 kcal ÷ daily need → (13) | scaling error (beef 0.07 → 0.71) |
| 1 (M94) | Cow, Pig | changed | muscle → composite with liver (28) | the user |
| 2 (M96) | preference $V_g=s_g+\nu_g+\beta_g$ | removed | one key → $K^{(1)},K^{(2)}$ (15) | the user: two separate variables and sorted lists |
| 2 (M96) | allocation | changed | one pass → two passes (Algorithm 1) | M88: nutrition first, then well-being |
| 3 (M98) | — | presentation only | prose and code-style formulas → sets, parameters, variables, equations (1)-(30), Algorithm 1, legend | the user: proper notation and a full legend |

## 9. Rules for changes

1. A change is written here first, in sections 2-5, with a row in section 8.
2. The code changes only what the row names; the commit names the row.
3. Results are published with the version they come from.
