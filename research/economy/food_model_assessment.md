# The food model: a semantic assessment and proposals (R53, M100)

**Subject:** specification version 3 (`food_model_spec.md`). Symbols and equation numbers are the specification's. Nothing here is implemented: each proposal is for decision, and an accepted proposal enters the specification's change log first.

## 0. Criteria

Every equation is tested against four questions:

| Criterion | Question |
|---|---|
| (C1) Dimensions | Are the terms of every sum in the same unit, so that adding them means something? |
| (C2) Meaning | Does the quantity measure what its name says? |
| (C3) Representation | Which real mechanism that matters for the outcome is missing? |
| (C4) Identifiability | Can each parameter be measured or sourced, or does it depend on an arbitrary choice? |

## 1. Findings

| # | Equation | Finding | Criterion |
|---|---|---|---|
| F1 | (15) $K^{(1)}_g=s_g+\nu_g$ | adds a satiety ratio (0.9-2.3) to a nutrient adequacy score (0-1); the implicit weight 1 : 1 has no meaning | C1, C4 |
| F2 | (13) $\nu_g$ | a property of the food alone. A food's nutritional value depends on what the diet already lacks: vitamin C from lemons is worth nothing to a person already covered, everything to one with scurvy | C2, C3 |
| F3 | (13) $\nu_g$ | all 13 nutrients weigh the same: sodium counts as much as B12 or iodine, whose lack causes far worse harm | C2 |
| F4 | (13) $\nu_g$ | needs are scaled per kcal with a fixed $E^{\mathrm{ref}}=2600$, while the person's energy need $E^{\mathrm{need}}$ varies from 2,350 to 3,450 kcal. Needs for vitamins and minerals do not scale with energy | C2 |
| F5 | (12) $s_g$ and (11) $\sigma_g$ | satiety appears twice: as preference ($s_g$, a protein-based fit to Holt) and as fullness ($\sigma_g$, Holt's index). Protein also appears a third time in $\nu_g$ | C2 |
| F6 | (14) $\beta_g$ | well-being per kcal. A lemon has few kcal, so its well-being per kcal is the highest of all goods; pleasure comes per serving, not per kcal. Fat enters three times, alcohol only as a benefit (its harm at higher doses is absent) | C1, C2, C3 |
| F7 | M5 | well-being is computed and spent (pass 2) but never measured: there is no outcome for it, so it can feed nothing | C3 |
| F8 | Algorithm 1 | pass 1 ignores well-being; pass 2 ignores nutrition. A fed person still short of vitamin C takes sugar over cabbage in pass 2. Pass 1 stops at "fed" even when nutrient gaps remain | C2 |
| F9 | (17), (30) | diminishing returns are counted in servings $m_g$ while steps are in kcal. By (P2) each good's total value scales with $e_gm_g$ (kcal per serving), so changing the definition of a serving changes what people eat | C4 |
| F10 | (7) $P^{\max}=0.35E^{\max}/4$ | the protein ceiling is tied to the energy ceiling, not to what is eaten. The fishing village eats 50 % of its energy as protein without consequence; the source (Bilsborough and Mann) states a share of energy eaten, and an absolute liver capacity | C2 |
| F11 | (6) $F^{\max}=\bar\sigma E^{\max}$ | the fullness capacity rests on the mean of the 38 foods Holt happened to test (1.36). A different food list gives a different capacity; Holt measured two hours after one serving, not a day | C4 |
| F12 | (25)-(26) | all energy eaten above the basal rate becomes activity ($\Lambda^{\mathrm{act}}=E/B$); there is no body store. Fat reserves that carry people through lean seasons, and that surplus becomes, are missing | C3 |
| F13 | (26) $\textit{work}$ | one factor for all work. Desk work does not scale with surplus energy as hauling does | C2 |
| F14 | (4) caffeine | caffeine only raises the energy need. Its effect on effort and alertness, the reason it matters (M85), is not in any outcome | C3 |
| F15 | (23) $W^{\mathrm{drink}}$ | grams of a drink times the hydration index. The beverage hydration index is retention relative to water over hours, measured by urine output (PMID 42884730), not water content: milk is 88 % water and is counted as 150 % | C1, C2 |
| F16 | $W^{\mathrm{need}}$ constant | the water need does not rise with work and heat, while the energy need does | C3 |
| F17 | (1) $a_g$ | stocks are spread evenly over the year. Fresh goods (fruit, milk in season, fresh fish) come in seasons; vitamin C deficiency is seasonal | C3 |
| F18 | the whole model | one representative person per city. Hunger and malnutrition fall on the poor first; a city whose average is fed can have a starving underclass | C3 |
| F19 | the whole model | choice depends on availability only. Once the goods economy has prices, the budget decides what the poor eat | C3 |

## 2. Proposals

Each proposal states the reasoning, the new equations, and the variables it adds, removes or changes.

### Proposal A. Nutrition as diet adequacy, driven by the gaps (fixes F1-F5, F9 for nutrition)

**Reasoning:**
- What makes a food nutritionally valuable at a given moment is how much it closes what the diet still lacks.
- A static per-food score (13) cannot express that. A diet-level adequacy function can, and its marginal value per good then changes as the diet fills.
- Weighting each nutrient by the harm its lack causes ties nutrition to the deficiency burden the population model already uses.
- Protein enters as digestible indispensable protein (protein × DIAAS), so protein quality lives in one place.
- Per-good bioavailability carries the PubMed findings of `round_m84.md`: iron, zinc, niacin, carotene.

**Equations:**

$$
c_i(\mathbf q)=\frac{1}{r_i}\sum_{g}\frac{q_g\eta_g}{100}\,b_{gi}\,n_{gi},\qquad
A(\mathbf q)=\sum_{i\in\mathcal I_0}\omega_i\,\min\bigl(1,\,c_i(\mathbf q)\bigr)
$$

- $\mathcal I_0=\mathcal I\cup\{\text{energy}\}$, with $c_{\text{energy}}=E/E^{\mathrm{need}}$ and $n_{g,\text{protein}}=\pi_g\min(\delta_g,1)$.
- The marginal value of good $g$ per kcal is the partial derivative

$$
\frac{\partial A}{\partial(e_gq_g)}=\frac{1}{e_g}\sum_{i:\,c_i<1}\omega_i\,\frac{\eta_g\,b_{gi}\,n_{gi}}{100\,r_i}.
$$

  It falls to zero for every nutrient already covered. Diminishing returns then come from the gaps closing, not from servings.

**Variables:**

| Change | Variable | Note |
|---|---|---|
| removed | $\nu_g$ (13), $s_g$ (12), $K^{(1)}_g$ (15), $E^{\mathrm{ref}}$, $\kappa_s,\bar p,\bar\delta$ (in the preference) | replaced |
| removed | $m_g$ in pass 1 | servings no longer drive nutritional diminishing returns |
| added | $\omega_i$ | weight of nutrient $i$: the deficiency-burden weights of the population model (`round_m83.md` section 2c); energy and protein weighted highest (protein leverage, PMID 37820518) |
| added | $b_{gi}$ | bioavailability of nutrient $i$ in good $g$: plant iron 0.05-0.12 against mixed 0.14-0.18 (Hurrell and Egli 2010); cereal niacin about 1/3 unless nixtamalized (Carpenter 1983); carotene 1/2 to 1/10; B12 by food (Watanabe 2007) |
| added | $A(\mathbf q)$ | diet adequacy, 0 to $\sum\omega_i$ |
| changed | $c_i$ | from an outcome (22) to a state updated during the allocation; (21) folds into $b_{gi}$ |

**What changes in results:**
- A city with milk and grain, short of vitamin C, takes its apples and potatoes for vitamin C until it is covered, then stops valuing them for it.
- Beef keeps its value while B12, iron or zinc are short.
- Sodium stops lifting meat once salt covers it.

### Proposal B. Well-being per serving, with sensory-specific satiety and an outcome (fixes F6, F7)

**Reasoning:**
- Pleasure comes in eating events. It falls with repetition of the same food: sensory-specific satiety, a short-term satiety signal (PMID 1752065). So well-being belongs per serving, with diminishing returns per food, not per kcal.
- Alcohol pleases at low doses and harms at higher ones (a biphasic dopamine response, PMID 39729041), so it needs a harm term.
- Fat should enter once, as reward (with carbohydrate) and as heaviness, not three times.
- The result must be an outcome, $\Psi$, so that it can feed the happiness line.

**Equations:**

$$
\Psi(\mathbf q)=\sum_{g}h_g\ln\!\Bigl(1+\frac{q_g}{m_g}\Bigr)\;-\;\zeta\,\max\bigl(0,\;\textstyle\sum_g q_g\eta_g\alpha_g/100-\alpha^{\mathrm{safe}}\bigr)
$$

$$
h_g=u_1z_g+u_2f_gk_g+u_3\,[\alpha_g>0]-u_5\,\mathrm{ED}_g\qquad(\text{per serving; }\mathrm{ED}_g=\text{energy density, kcal/g})
$$

**Variables:**

| Change | Variable | Note |
|---|---|---|
| removed | $\beta_g$ per kcal (14), the lightness term from water per kcal | replaced; lightness becomes low energy density, the property Wells et al. measured as heaviness |
| added | $h_g$ | hedonic value of one serving of $g$ |
| added | $\Psi$ | well-being attained per person a day: an outcome, to feed the happiness line (one happy face per step of $\Psi$, to be set) |
| added | $\zeta,\ \alpha^{\mathrm{safe}}$ | alcohol harm slope and safe daily alcohol (to source) |
| changed | $m_g$ | now only in $\Psi$, where a serving has a meaning: one eating event |

### Proposal C. One consumption program with two priorities (fixes F8, F9; replaces Algorithm 1)

**Reasoning:**
- Your rule is two separate variables in two sorted orders: nutrition first, then well-being ("steak and potatoes, then dessert").
- The exact mathematical form of "first A, then B, without giving up A" is a lexicographic optimisation.
- Stage 1 closes energy and nutrient gaps as far as the goods and the stomach allow.
- Stage 2 adds what pleases, in the room left, without undoing stage 1.
- This removes the arbitrary stop of pass 1 at "fed". People keep eating for nutrition while gaps remain, and well-being never displaces a nutrient they still lack.

**Equations:**

$$
\begin{aligned}
\text{Stage 1:}\quad & A^*=\max_{\mathbf q}\ A(\mathbf q)\\
\text{Stage 2:}\quad & \max_{\mathbf q}\ \Psi(\mathbf q)\quad\text{subject to}\quad A(\mathbf q)\ge A^*,\\
\text{both stages:}\quad & 0\le q_g\le\bar q_g,\quad F(\mathbf q)\le F^{\max},\quad E(\mathbf q)\le E^{\max},\quad P\le P^{\mathrm{abs}}\ (\text{Proposal E}),\quad R\le Q^{\mathrm{fruit}}.
\end{aligned}
$$

**Solution method:** the same step-by-step choice as now. Stage 1 always takes the good with the largest $\partial A/\partial(e_gq_g)$; stage 2 the good with the largest $\partial\Psi$ among steps that keep $A$. $A$ is concave (a sum of capped linear terms) and $\Psi$ is concave, so taking the steepest admissible step is the standard method.

**Variables:**

| Change | Variable | Note |
|---|---|---|
| removed | passes $\rho\in\{1,2\}$ with stops $F^{\mathrm{fed}}$ and $F^{\max}$; keys $K^{(1)},K^{(2)}$ | replaced by the two stages |
| added | $A^*$ | the best adequacy the goods allow |
| changed | $\textit{fed}$ (19) | stays as an outcome, $F/F^{\mathrm{fed}}$, no longer a stopping rule |

### Proposal D. One satiety construct (fixes F5, F11)

**Reasoning:**
- Fullness (how much a person can eat) and nutrition (what they need) are different things. Holt's index measures the first; it should appear once, as fullness.
- The protein factor $s_g$ was a stand-in for Holt (fitted to beef against bread). Under Proposal A, protein's pull is in $A$ through $\omega_{\text{protein}}$, so $s_g$ has no role left.
- The fullness capacity should not depend on which foods Holt chose to test. Calibrating it so that a reference diet is exactly fed at its need makes it a property of people, not of a food list.

**Equations:**

$$
F^{\max}=\Bigl(\frac{\sum_g\sigma_ge_gq^{\mathrm{ref}}_g}{\sum_ge_gq^{\mathrm{ref}}_g}\Bigr)\,E^{\max}
$$

Here $q^{\mathrm{ref}}$ is a documented reference diet: for example a sourced pre-industrial English or modern mixed diet.

**Variables:**

| Change | Variable | Note |
|---|---|---|
| removed | $s_g$, $\kappa_s$, $\bar p$, $\bar\delta$ | not needed under A |
| changed | $\bar\sigma$ | from Holt's sample mean (1.36) to the mean fullness of a reference diet $q^{\mathrm{ref}}$ |
| added | $q^{\mathrm{ref}}_g$ | a sourced reference diet (data to find) |

### Proposal E. Protein: an absolute ceiling and a share-based harm (fixes F10)

**Reasoning:** Bilsborough and Mann (2006) give two separate facts:
- a liver capacity: a theoretical safe maximum of 285-365 g a day for 80 kg, about 3.6-4.6 g per kg;
- a danger when protein exceeds 35 % of energy eaten.

The first is a hard ceiling. The second is a harm that rises with the share, not a reason to stop eating.

**Equations:**

$$
P\le P^{\mathrm{abs}}=3.6\ \text{g/kg}\times63.3\ \text{kg}\approx228\ \text{g},\qquad
\text{burden}_{\text{protein}}=\psi\,\max\Bigl(0,\;\frac{4P}{E}-0.35\Bigr)
$$

63.3 kg is the EFSA mean adult weight.

**Variables:**

| Change | Variable | Note |
|---|---|---|
| changed | $P^{\max}$ (7) | from $0.35E^{\max}/4$ to $P^{\mathrm{abs}}$ |
| added | $\psi$ | harm per unit of excess protein share (to source); enters the health burden |

**What changes in results:** the fishing village is no longer stopped at an arbitrary protein amount. It eats up to the liver's capacity and carries the harm of a 50 % protein diet.

### Proposal F. Energy balance with a body store (fixes F12)

**Reasoning:**
- Energy eaten is either spent or stored.
- People fatten in good seasons and live off reserves in lean ones. That is the buffer that keeps a bad harvest from becoming an immediate famine, and it is absent now.
- With a store, surplus energy is not all turned into activity. Activity follows work; surplus is stored up to a ceiling; deficits are drawn from the store at a limited rate.

**Equations:**

$$
\begin{aligned}
\Lambda^{\mathrm{act}}&=\min\Bigl(\Lambda^{\max},\;\frac{E+\min(Z/365,\ \bar z)}{B}\Bigr)\ \text{ capped at the work demand } \Lambda^{\mathrm w}\ \text{(plus the voluntary surplus, M85)}\\
Z_{t+1}&=\min\bigl(Z^{\max},\;Z_t+365\,(E-B\Lambda^{\mathrm{act}})\bigr)
\end{aligned}
$$

**Variables:**

| Change | Variable | Note |
|---|---|---|
| added | $Z$ | body energy store per person (a state carried from year to year, like the vitamin stores of `round_m85.md`) |
| added | $Z^{\max}$, $\bar z$ | store ceiling and the largest daily drawdown (to source) |
| changed | $\Lambda^{\mathrm{act}}$ (25) | from $E/B$ to the balance above |

### Proposal G. Work by kind of work, and what caffeine does (fixes F13, F14)

**Reasoning:**
- Physical work scales with the energy available for it.
- Desk work is lowered by a deficit but not raised by a surplus.
- Caffeine raises effort and alertness (PMID 20164571; Dulloo 1989 for the energy cost), so it belongs in work capacity as well as in the need.

**Equations:**

$$
\textit{work}_k=\begin{cases}\min\bigl(\Omega+\omega_cc,\ \max(0,\tfrac{\Lambda^{\mathrm{act}}-\Lambda^{\min}}{\Lambda_k-\Lambda^{\min}})\bigr)&k\in\{\text{vigorous, active}\}\\
\min\bigl(1+\omega'_cc,\ x\bigr)&k=\text{sedentary}\end{cases}
$$

**Variables:**

| Change | Variable | Note |
|---|---|---|
| changed | $\textit{work}$ (26) | becomes $\textit{work}_k$ per kind of work |
| added | $\omega_c,\ \omega'_c$ | caffeine's effect on physical and mental work capacity (to source) |

### Proposal H. Water as a balance in consistent units (fixes F15, F16)

**Reasoning:**
- A drink contributes the water it contains, times how well that water is retained. The hydration index is that retention, relative to water.
- The need rises with energy turnover (work, heat). Its slope still has to be sourced; I found no confirmed figure in this round.

**Equations:**

$$
W^{\mathrm{drink}}=\sum_{g\in\mathcal G^{\mathrm D}}q_g\eta_g\,\frac{\omega_g}{100}\,h_g,\qquad
W^{\mathrm{need}}=W_0+w_E\,(E^{\mathrm{need}}-E_0)
$$

For milk: $0.88\times1.5=1.32$ instead of $1.5$.

**Variables:**

| Change | Variable | Note |
|---|---|---|
| changed | $W^{\mathrm{drink}}$ (23) | water content × retention |
| changed | $W^{\mathrm{need}}$ | from a constant to a function of energy turnover |
| added | $W_0, E_0, w_E$ | base need at a reference energy, and the slope (to source) |

### Proposal I. Seasons for fresh goods (fixes F17)

**Reasoning:**
- Fresh goods are available in their season only.
- With the vitamin stores of `round_m85.md`, a city that eats fruit only in summer can run short of vitamin C by late winter, and the model should be able to show it.
- Two half-years are the smallest split that shows it.

**Equations:**

$$
a_{g,\tau}=\frac{a_g}{\lvert\mathcal T_g\rvert/\lvert\mathcal T\rvert}\ \text{ for } \tau\in\mathcal T_g,\ \ 0\ \text{otherwise};\qquad \text{the program runs once per } \tau\in\mathcal T=\{\text{summer},\text{winter}\}
$$

**Variables:**

| Change | Variable | Note |
|---|---|---|
| added | $\mathcal T$, index $\tau$ | seasons |
| added | $\mathcal T_g$ | the seasons in which good $g$ is fresh |
| changed | $a_g$ | becomes $a_{g,\tau}$; nutrient stores carry between seasons |

### Proposal J. Classes within the city (fixes F18), then prices (F19)

**Reasoning:**
- Food is not shared equally. Three classes are the least that show a fed average hiding a starving poor.
- When the goods economy has prices, each class's access becomes its budget, and the classic diet problem (cheapest diet meeting the needs, Stigler 1945) becomes a constraint of the same program.

**Equations:**

$$
\text{for each class } j:\quad a^{(j)}_g=a_g\,\frac{\theta^{\mathrm{access}}_j}{\theta^{\mathrm{pop}}_j};\qquad\text{later: } \sum_g p_gq^{(j)}_g\le Y_j
$$

**Variables:**

| Change | Variable | Note |
|---|---|---|
| added | class index $j\in\{\text{poor},\text{middle},\text{rich}\}$ | |
| added | $\theta^{\mathrm{pop}}_j$, $\theta^{\mathrm{access}}_j$ | population share and share of food access (from income distribution, to source) |
| added later | $p_g$, $Y_j$ | prices and budgets from the goods economy |
| changed | all outcomes | computed per class; the population model reads them per class or weighted |

## 3. The model after A-E, in one statement

$$
\begin{aligned}
&\textbf{Given: } N,\ \mathbf S,\ \mathbf w;\ \text{parameters of section 3 of the specification},\ \omega_i,\ b_{gi},\ h_g.\\
&\textbf{Stage 1: } A^*=\max_{\mathbf q}\ \sum_{i\in\mathcal I_0}\omega_i\min\bigl(1,c_i(\mathbf q)\bigr)\\
&\textbf{Stage 2: } \max_{\mathbf q}\ \sum_gh_g\ln(1+q_g/m_g)-\zeta\max(0,\text{alcohol}-\alpha^{\mathrm{safe}})\quad\text{s.t. } A(\mathbf q)\ge A^*\\
&\textbf{subject to: } 0\le q_g\le\bar q_g,\ \ \sum_g\sigma_ge_gq_g\le F^{\max},\ \ \sum_ge_gq_g\le E^{\max},\ \ \sum_g\hat\pi_gq_g\le P^{\mathrm{abs}},\ \ \sum_{g\in\mathcal G^{\mathrm F}}\eta_gq_g\le Q^{\mathrm{fruit}}\\
&\textbf{Outcomes: } x=E/E^{\mathrm{need}},\ \textit{fed}=F/F^{\mathrm{fed}},\ c_i,\ \Psi,\ \text{protein harm},\ W^{\mathrm{plain}},\ \textit{work}_k,\ L_g,\ D_g\ (+Z\ \text{with F})
\end{aligned}
$$

**Compared with version 3:**
- one satiety construct instead of three;
- weights that come from health ($\omega_i$) instead of a 1 : 1 sum;
- diminishing returns where they occur (in nutrient gaps and in repeated pleasures);
- an outcome for well-being;
- two priorities stated as what they are: a lexicographic order.

## 4. Order of decision

| Order | Proposal | Why first |
|---|---|---|
| 1 | A, C, D | they define what "nutrition" and "priority" mean; the rest builds on them |
| 2 | B | well-being per serving and its outcome |
| 3 | E, H | corrections of units and ceilings |
| 4 | G, F | work and the body store |
| 5 | I, J | seasons and classes add dimensions; they cost the most data and computation |
