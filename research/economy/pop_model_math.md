# The population model, step by step (D30, fourth version; R33.3, M79)

This restores the evidence-based second version (R31.1), the one you were almost satisfied with (M79). It changes
only what you objected to in M75 and M78: there is no separate death term. Health is weighed from its causes and
lowers the growth rate, or turns it negative.

**Why the third version shrank it.** After M78 I removed the death term and also cut the model down to "five
numbers", citing your M65 wish for a formula without 10,000 variables. That was wrong in two ways:
- M65 was an earlier request; M77 ("health, fertility and much of what we discussed still seems missing") was the
  later one, and later decisions come first.
- Removing the death term never required discarding the evidence. The third version replaced the sourced fertility
  curve, the medicine levels, the famine, deficiency and urban figures with a few estimated weights.

All results are computed by `research/economy/plan/tools/pop_model_sim.py` in the DLL's integer arithmetic (64-bit
people, parts per million, remainders carried).

## 1. The bookkeeping

```
people next year = people × (1 + growth)  + arrivals − departures (migration, D33)
growth (per 1,000 a year) = fertility − health burden
```

- **Fertility** (section 2) is what adds people: the will and chance to have children.
- **Health burden** (section 3) is health weighed from its causes. It lowers growth and, when it outweighs fertility,
  turns growth negative. It is not a separate count of deaths. It is measured per 1,000 people a year so that the
  historical evidence (crude death rates, famine and epidemic losses) sets its size.
- **Starvation** stays the engine's own floor: no city keeps more people than its food feeds at the biological
  minimum.
- **The city screen** can show fertility, health burden and growth, each with what drives it.

## 2. Fertility: what raises and lowers it

```
fertility = B(food) × nutrients × economy × town life × religiosity × education × safety
```

**`B(food)`, the food driver** (the Malthusian core: births rise with living standards, Clark):
- 30 per 1,000 at food sufficiency `x` = 0.9, rising to 45 at `x` = 1.3 and above. Pre-industrial England was at
  times below 30; birth rates of 50-60 have been observed.
- Below 0.9 it falls to zero at the biological minimum. In the Dutch Hunger Winter, conceptions fell below a calorie
  threshold, tracked the daily ration, and recovered at once when food returned (Stein and Susser).

**The factors:**

| Factor | What it does | Read from (game state) | Evidence |
|---|---|---|---|
| nutrients | births × (0.8 + 0.2 × coverage) | the diet's coverage of nutrient groups (round_m75.md section 2) | estimate |
| economy | births follow marriage, which follows prices and work | food prices against wages, employment (goods economy) | England: high prices showed in fewer marriages (Wrigley and Schofield); Rostock: the proportion married drove overall fertility |
| town life | births × (1 − 0.2 × urban share) | urban share of the city's people | Rostock: rural fertility higher, mostly through marriage; Prussia: urban fertility far below rural by 1910 |
| religiosity | births × 0.9 to 1.1 | state religion and religious civics; secular civics | Western Europe: religious affiliation and practice still go with more children (Britain, France, Netherlands; Fertility and Family Surveys) |
| education and contraception | births × (1 − 0.65 × transition) | education civics and techs (Compulsory Education, Public Schools, later techs) | female schooling lowers fertility, largely by delaying marriage (Egypt, Turkey, Nigeria); the size is context-dependent |
| safety | births × 0.8 at full war threat | enemy units, recent war | estimate |

## 3. Health burden: health weighed from its causes

```
health burden = base burden(medicine) × (2 − health balance) + weakness of the underfed + famine + deficiency diseases + urban penalty + war
```

| Part | Size | Read from | Evidence |
|---|---|---|---|
| base burden | 22 per 1,000 before modern medicine, falling to 8 with it | medicine and sanitation techs (Medicine, Modern Sanitation, Modern Health Care) | Clark (life expectancy = 1 / death rate); the modern value is an estimate to source |
| × (2 − health balance) | doubles the base burden at the worst health balance | the city's health balance: water supply and quality (D31), aqueduct, bath house, hospital, harms of the diet | clean water about 43-50 % of the US urban mortality decline 1900-1936 (Cutler and Miller) |
| weakness of the underfed | up to 12 per 1,000, falling to 0 at x = 1.3 | food sufficiency x | Fogel: a fifth of the people of England and France in the late 1700s too weak to work |
| famine | 200 per 1,000 × shortfall below x = 1 | x | Great Famine 1315-17: 10-15 % |
| deficiency diseases | up to 15 per 1,000 at no coverage | nutrient coverage | beriberi struck about 30 % of the Japanese navy each year; in 1904-05 it killed 27,000 of 211,600 cases |
| urban penalty | 13 per 1,000 × share in unsanitized dense quarters | urban density, sewer and water level (D31) | London infant mortality 300-400 per 1,000 births against 180 nationally (mid-1700s); London needed about 8,000 migrants a year about 1700 |
| war | 25 per 1,000 at full war pressure | enemy units in the plots, sieges, pillage | Thirty Years' War: 15-20 % average, over 50 % in the worst regions, mostly plunder, famine and plague |

**Starvation** stays as the floor: no city keeps more people than its food feeds at the biological minimum (1,500 of
2,600).

## 4. What decides the balance

**At the food limit** fertility and the health burden meet at about 33 per 1,000 (case 1). That is the Malthusian equilibrium:
population settles where food per head meets need.

**What moves the balance:**
- **More food or better farming:** the city grows until food per head is back at the balance (case 2).
- **Better medicine and sanitation:** the health burden falls, the city grows. If fertility stays high it grows fast; this is the
  first phase of the demographic transition (case 5, years 20-60).
- **Education, town life and secularization:** fertility falls and the city settles at a higher food per head. The
  equilibrium income rises, which is Clark's point about the birth schedule (case 11, secular).
- **Disease, bad water, deficiency, dense unsanitary quarters, war:** the health burden rises. A city declines unless migrants
  come (cases 4, 6, 7, 10).

## 5. Edge cases (computed)

| Case | Setting | Result |
|---|---|---|
| 1 | a city at its food limit | fertility 33.4, health burden 33.3 per 1,000: balanced |
| 2 | a town of 1,000 with food for 50,000 | fertility 45, burden 22: 2.3 % a year; reaches 50,500 and holds |
| 3 | two harvests at 70 % | −13.7 % over two years; fertility falls to 10.8 per 1,000 in the famine year, the burden reaches 95; recovery afterwards |
| 4 | 500,000, all in unsanitized dense quarters, no migrants | 394,000 after 40 years (−21 %): such a city needs migrants |
| 5 | medicine from year 21, education from year 61, food growing 2 % a year | burden 26 → 8, fertility 42 → 16 per 1,000; 1 million → 8.4 million in 140 years: the demographic transition |
| 6 | polished-rice diet (coverage 60 %), corrected in year 16 | burden about 5 per 1,000 higher, slow decline; recovery after the diet changes |
| 7 | 30 years of war with a third of the food pillaged | −51 % (491,500); back to 947,000 30 years after peace |
| 8 | 1 million, half its food imported, imports cut | starvation cap at once (866,551), then burden above 100 per 1,000 and fertility near 0, toward 525,000 |
| 9 | a hamlet of 10 with food for 40 | grows to 40 and holds (39-41) |
| 10 | health at half | burden 40 against fertility 36: −10 % in 30 years |
| 11 | food 20 % above need: religious (× 1.1) against secular with schooling | religious grows to 122,700 and is then held by food; secular stays at 100,000, 20 % better fed |
| 12 | all food lost | emptied in one year (the engine keeps size 1) |

## 6. What good food does besides growth

| Effect | Rule | Evidence |
|---|---|---|
| work output | output per worker scales with the energy left for work; below the need, a share of people cannot work | Fogel (1790s England and France) |
| science and culture | multiplied by the city's nutrition and cognition, lowered by iodine and nutrient gaps | iodine deficiency 10-15 IQ points; US iodization +1 SD in the most deficient quarter |
| commerce | multiplied by the city's nutrition, as science and culture are (M75 named commercial output) | |
| fertility and mortality | sections 2-3 | |
| unit strength | protein coverage for living units (D27) | |

## 7. Parameters

| Parameter | Value | Basis |
|---|---|---|
| fertility at x = 0.9 / 1.3 | 30 / 45 per 1,000 | Clark (range 30-60) |
| base burden before / after modern medicine | 22 / 8 per 1,000 | Clark; modern value estimate |
| weakness of the underfed | 12 per 1,000 | estimate, set so fertility equals the burden near x = 1 |
| famine | 200 per 1,000 per unit shortfall | Great Famine |
| deficiency | 15 per 1,000 | estimate from beriberi rates |
| urban penalty | 13 per 1,000 | London infant mortality and migrants |
| war | 25 per 1,000 | Thirty Years' War |
| minimum | 1,500 of 2,600 | Clark |
| factor sizes (town 0.2, religiosity ± 0.1, education 0.65, safety 0.2, nutrients 0.2) | as in section 2 | sources named; sizes estimates |

## 8. Still to decide

- Whether this fertility and health burden, with these inputs, is the model you want.
- The estimates you want sourced first.
- How the city size follows people (the inverse curve or labour units).

## 9. Why it does not oscillate, and why integers need care

- Near the food limit, growth closes a small part of the gap each year (fertility rises and the burden falls only
  gently with food per head), so the approach is gradual. The discrete logistic map oscillates and turns chaotic
  only when its step is large (May 1976, *Nature* 261).
- Long early turns (50 years) run as yearly steps, so they follow the same path.
- **Precision:** with rates in per mille, an earlier version stalled 1 % short of the food limit. Parts per million
  and carried remainders reach it (case 2), and a hamlet of 10 still grows (case 9).

## 10. Forms compared

| Form | Verdict |
|---|---|
| everything added into one rate | a big food surplus can hide a deadly city |
| everything multiplied | disease can slow growth but never shrink a city |
| one rate with a few estimated weights (third version) | withdrawn: it dropped the evidence (M79) |
| births and deaths as separate terms (second version) | the same evidence, but with a death term (M75) |
| **fertility minus a health burden weighed from its causes** (this version) | proposed |

**Open from the England 1300 check:** with 80 % milling, England's diet gives 2,354 satiety units a day, under the
2,600 used as need (PR.F8.T4).
