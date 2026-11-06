# The population model, step by step (D30, third version; R32.2, M78)

This replaces the second version (R31.1), which added an explicit death term.

**What you asked for (M75):**
- Health is weighed from several factors by itself.
- It lowers the growth rate or turns it negative.
- No death term inside the growth equation: starvation and population death already exist in the game.

This version does that. It also restores what the first version had and the second dropped: why the model does not
oscillate, the comparison of forms, and the precision lesson.

Every result is computed by `research/economy/plan/tools/pop_model_sim.py` in the DLL's integer arithmetic (64-bit
people, rates in parts per million, remainders carried).

## 1. One growth rate

```
people next year = people × (1 + g)  (+ migration, D33),   at most food ÷ biological minimum (starvation)
g = G_MAX × [ food drive × fertility culture × health  −  KAPPA × (1 − health) ]
```

**Three inputs, each built from the game state** (sections 2-4). **Five numbers:** `G_MAX`, `A`, `K`, `KAPPA`, `B`
(section 6).

## 2. The food drive

**`x` = satiety per head ÷ need** (the three food measures, `round_m75.md` section 2).

- **Surplus:** growth rises to the full rate when food reaches the target level plus a 30 % margin (`A`).
  - The ceiling `G_MAX` is 3 % a year. Birth rates reach 50-60 per 1,000 at most while deaths stay near 20-25 in
    good years (Clark), and the Hutterites' total fertility of 10.9 is the recorded high (Coale).
- **The target level** is exactly fed (`x` = 1) for a traditional society. It rises as fertility culture falls:
  - Clark's point: a lower birth schedule settles a population at a higher income.
  - A schooled, low-fertility city stops growing when it is 20 % better fed than it needs (case 12).
- **Shortfall (`x` < 1):** growth turns negative. `x` = 0.7 gives −6 % a year, so two such years cost about 11 %.
  The Great Famine of 1315-17 cost 10-15 %. In the Dutch Hunger Winter, births fell with the ration and recovered at
  once when food returned.
- **Starvation** stays the engine's floor: no city keeps more people than its food feeds at the biological minimum
  (1,500 of 2,600).

## 3. Fertility culture: what shapes the will and chance to have children

A product of factors, 1.0 neutral:

| Factor | Read from | Evidence |
|---|---|---|
| economy | food prices against wages, work for the people | England: high prices showed in fewer marriages (Wrigley and Schofield); Rostock: the share married drove fertility |
| town life | the urban share | Rostock: rural fertility higher, through marriage; Prussia: urban fertility far below rural by 1910 |
| norms | religiosity, secularization, diversity, media reach (D21) | religious affiliation and practice go with more children (Western Europe surveys); M76: prudish and poor against fertile and permissive eras |
| education and contraception | education civics and techs | female schooling lowers fertility, mostly by delaying marriage (Egypt, Turkey, Nigeria) |
| safety | enemy units near, recent war | estimate |

- It multiplies positive growth.
- It sets the target food level (section 2).
- It does not soften a famine.

## 4. Health: weighed from its factors

`health = 1 − sum of the weighted shortfalls` (1 = perfect):

| Factor | Its weight (most it can take) | Read from | Evidence |
|---|---:|---|---|
| water: supply and quality | 0.25 | the city's water supply level and quality (D31) | clean water about 43-50 % of the US urban mortality decline 1900-1936 (Cutler and Miller) |
| sanitation in dense quarters | 0.25 | urban density against sewers | London infant mortality 300-400 per 1,000 births against 180 nationally (mid-1700s) |
| nutrient coverage | 0.20 | the diet's coverage of nutrient groups | scurvy, beriberi, pellagra, iodine deficiency |
| dietary harms | 0.10 | processed and salted meat, sugar, grain-only diets | IARC Group 1 for processed meat; caries; bladder stones |
| medicine | 0.20 | medicine techs, hospitals | the fall of death rates from the late 1700s |

**How health acts:**
- It multiplies positive growth: poor health slows growth.
- Below perfect it also subtracts `KAPPA` × the lost health: bad health turns growth negative.
- Dense quarters without sewers (health 0.75) give about −1.3 % a year. London about 1700 needed about 8,000 migrants
  a year to make up its deaths.
- The worst health gives about −5 % a year.

**War** acts through these three inputs, not through a war term:
- pillage cuts food;
- fear lowers fertility culture;
- displacement and disease lower health.

## 5. Edge cases (computed)

| Case | Setting | Result |
|---|---|---|
| 1 | a healthy city at its food limit | no change |
| 2 | a town of 1,000 with food for 50,000 | 3 % a year (4,382 at 50 years, 19,210 at 100), then exactly 50,000 |
| 3 | harvests at 70 % in years 11-12 | 89,152 (−10.8 %), then recovery |
| 4 | 500,000 in dense quarters without sewers, no migrants | 429,192 after 40 years (−14 %): such a city needs migrants |
| 5 | the same with sewers and clean water from year 21 | recovers toward 500,000 (492,572 at year 40) |
| 6 | medicine from year 21, falling fertility culture from year 61, food growing 2 % a year | 1 million → 7.45 million in 140 years; growth 1.7-2.2 %, slowing to 1.1 % as fertility falls |
| 7 | polished rice (nutrient coverage 60 %) until year 15 | growth held near zero, then resumes |
| 8 | 30 years of war: a third of the food pillaged, fertility culture 0.8, health 0.8 | 607,185 after 30 years (−39 %), back to 1.06 million 30 years after peace |
| 9 | 1 million, half its food imported, imports cut | starvation cap at once (866,551), then down toward its own food (548,645 at year 15) |
| 10 | a hamlet of 10 with food for 40 | grows to 40 and holds |
| 11 | fed, bad water and half sanitation (health 0.70) | −9 % in 30 years |
| 12 | food 20 % above need: high-fertility culture against prudish and schooled | the first grows to its food limit; the second stays at 100,000, 20 % better fed |
| 13 | all food lost | emptied by the starvation cap |

## 6. The five numbers

| Number | Value | Basis |
|---|---|---|
| `G_MAX` | 3 % a year | Clark (birth and death rate ranges); Hutterites (Coale) |
| `A` | 0.30 | estimate; England 1086-1300 grew 0.4-0.5 % a year |
| `K` | 6.7 × `G_MAX` per unit shortfall (−6 % a year at `x` = 0.7) | Great Famine 10-15 % |
| `KAPPA` | 1.7 × `G_MAX` per unit of lost health | London's migrant need |
| `B` | 0.5 × lost fertility culture | estimate; Clark on the birth schedule |
| health weights | 0.25, 0.25, 0.20, 0.10, 0.20 | estimates, each tied to the evidence in section 4 |

**Open from the England 1300 check:** with 80 % milling, England's diet gives 2,354 satiety units a day, under the
2,600 used as need. Either need is about 2,350, or medieval extraction was higher (PR.F8.T4).

## 7. Why it does not oscillate, and why integers need care

- Near the target each year closes about a tenth of the gap to it (`G_MAX` ÷ `A`), so the approach is gentle. The
  discrete logistic map oscillates and turns chaotic only when its step is large (May 1976, *Nature* 261).
- Long early turns (50 years) run as yearly steps, so they follow the same path.
- **Precision:** with rates in per mille, the first version stalled 1 % short of the food limit (49,459 instead of
  50,000). Parts per million and carried remainders reach it exactly (case 2), and a hamlet of 10 still grows
  (case 10).

## 8. Forms compared

| Form | Bad health alone | Verdict |
|---|---|---|
| everything added | a big food surplus can hide a deadly city | rejected |
| everything multiplied | disease can slow growth but never shrink a city | rejected |
| **health multiplies growth and subtracts when bad** (this version) | slows, then reverses | proposed |
| births and deaths separately (second version) | the same outcomes, but with a death term | withdrawn (M75, M78) |

## 9. Good food besides growth

Each effect is one multiplier from the city's nutrition:
- **Work output:** Fogel estimated a fifth of people in late-1700s England and France were too weak to work.
- **Commerce, science and culture.** You named commercial output in M75; the earlier "no separate bonus" for commerce
  is withdrawn.
- **Cognition:** iodine deficiency costs 10-15 IQ points.
- **Unit strength:** one effect among these (D27).

## 10. Still to decide

- Whether this is the model you want.
- The estimates to source first.
- How the city size follows people.
