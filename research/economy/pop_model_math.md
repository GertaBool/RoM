# The population model, step by step (D30; R30.1, M76)

This explains the proposed model from the ground up: what each part does, why, its sources, and how it behaves in
edge cases. Every result below is computed by `research/economy/plan/tools/pop_model_sim.py`, which runs the model
in the integer arithmetic the DLL would use. It is a proposal for your decision.

## 1. The bookkeeping

A city's people change each year by four flows:

```
N(next year) = N + births − deaths + people arriving − people leaving
```

- Births minus deaths is **natural growth**. Arrivals minus departures is **migration** (section 7).
- The model gives natural growth as one rate `n` per year, so `N(next) = N × (1 + n)` before migration.
- You asked that health and the rest slow growth or turn it negative, not add a separate death term (M75). So
  `n` is one rate built from factors.

## 2. The driver: food per head against need

`x = satiety available per head ÷ satiety needed per head`

- `x = 1` means exactly fed, `x = 1.3` a 30 % surplus, `x = 0.7` a 30 % shortfall.
- Satiety comes from the three-measure food model (calories × satiety index, `round_m75.md` section 2).

**Why food per head is the driver:**
- The Malthusian model (Clark): births rise and deaths fall with living standards.
- Living standards fall as people press on fixed land.
- Population therefore settles where food per head meets need.

**The two sides of `x = 1`:**
- **Surplus (`x > 1`).** Growth rises with the surplus up to a ceiling:
  `Q = min(1, (x − 1) ÷ A)`, with `A` = 0.30, so a 30 % surplus gives the full ceiling. The ceiling `N_MAX` is 3 % a
  year. Birth rates reach 50-60 per 1,000 at most (Clark) while deaths stay near 20-25 in good years, and the
  Hutterites' total fertility of 10.9 is the recorded high (Coale).
- **Shortfall (`x < 1`).** Growth turns negative in proportion to the shortfall: `n = −K × (1 − x)`, with `K` = 0.2 a
  year.
  - So `x = 0.7` loses 6 % a year, and two such years lose about 11 %. The Great Famine of 1315-17 cost 10-15 %.
  - In the Dutch Hunger Winter, conceptions fell below a calorie threshold, tracked the ration, and recovered at once
    when food returned.
- **Starvation (the floor).** No city can keep more people than its food feeds at the biological minimum (1,500 of
  2,600 a day). Anyone beyond that does not survive the year. This is the game's starvation as now, expressed in
  people.

**Why the model returns to balance and does not oscillate:**
- As people increase with food fixed, `x` falls, and growth slows to zero at `x = 1`.
- Near balance each year closes about `N_MAX ÷ A` = 10 % of the remaining gap to the food limit: a gentle approach,
  never an overshoot.
- The classic discrete logistic map oscillates and turns chaotic when its growth parameter is large (May 1976,
  *Nature* 261). Here the step is small (10 % of the gap a year).
- Long turns (50 years early in the game) run 50 yearly steps rather than one big step, so they follow the same path
  (case 10).

## 3. What slows growth: multipliers between 0 and 1

Positive growth is `N_MAX × Q × h × c × e × w`, each factor between 0 and 1:

| Factor | Meaning | Read from | Evidence |
|---|---|---|---|
| `h` health | the city's health balance (water, disease, harms) | health (D31 water terms, nutrient gaps) | clean water about 43-50 % of the US urban mortality decline 1900-1936 (Cutler and Miller) |
| `c` nutrient coverage | share of nutrient groups the diet covers (protein quality, vitamin C, B vitamins, iodine) | the diet (round_m75.md section 2) | scurvy, beriberi, pellagra and iodine deficiency |
| `e` economy | food price against wages, or work for the people | the goods economy | in England high prices showed up mostly as fewer marriages (Wrigley and Schofield) |
| `w` safety | the absence of war threat | enemy units near, recent war | a population expecting war marries and settles less (estimate) |

Multipliers slow growth when things are imperfect, but cannot by themselves make it negative.

## 4. What turns growth negative: penalties

Subtracted from `n` each year:

| Penalty | Size at full strength | Read from | Evidence |
|---|---|---|---|
| urban penalty `U` × share of people in dense quarters without sanitation | 1.3 % a year | urban people, density, sewer and water level (D31) | cities deadlier than the countryside until sanitation; London about 1700 needed about 8,000 migrants a year (Wrigley) |
| war `P_WAR` × war pressure | 2.5 % a year | enemy units in the city's plots, siege, pillaged plots | Thirty Years' War: 15-20 % over 30 years on average, over 50 % in the worst regions, mostly through plunder, famine and plague |
| bad health `P_HEALTH` × (1 − h) | 1 % a year at no health | the health balance | estimate |

**The full rate:**

```
if x ≥ 1:  n = N_MAX × Q × h × c × e × w − penalties
if x < 1:  n = −K × (1 − x) − penalties
N(next) = min( N × (1 + n),  food ÷ minimum per head )
```

This is the **hybrid form**: multipliers slow, penalties reverse. Compared with the other two forms:

| Form | Bad health alone | Good food, bad city | Verdict |
|---|---|---|---|
| Additive (all terms added) | can make growth negative | a big surplus can hide a deadly city | a surplus outweighs disease, which is wrong |
| Multiplicative (all factors multiply) | slows growth to zero, never below | cannot shrink a city by disease or war | misses decline |
| **Hybrid** (multipliers on growth, penalties subtract) | slows and, past a point, reverses | decline when disease or war outweigh births | recommended |

## 5. Edge cases (computed by `pop_model_sim.py`)

| Case | Setting | Result | Reading |
|---|---|---|---|
| 1 | a town of 1,000 with food for 50,000 | 4,382 at 50 years, 19,210 at 100, 49,292 at 150, 50,000 at 250 | S-shaped growth to the food limit, reached exactly |
| 2 | a hamlet of 10 with food for 40 | 17, 31, 39, 40 | the remainder is carried between years, so small cities do not stall on rounding |
| 3 | 100,000 fed; harvests at 70 % in years 11-12 | 94,000, then 89,200; recovers to 98,378 by year 30 | famine losses of about 11 %; slow recovery as the surplus is shared again |
| 4 | a city of 1 million fed half by imports; imports cut in year 6 | 866,551 at once (starvation cap), then down toward 500,000 (516,120 at year 20) | a blockade starves at once to what food can keep alive, then shrinks toward its own food |
| 5 | 500,000 just fed, all in dense quarters, no sanitation | 459,817 at 10 years, settling near 442,600 | without migrants an unsanitary city shrinks until food per head rises enough for births to cover its deaths |
| 6 | the same, sanitation from year 26 | recovers toward 500,000 (496,073 at year 50) | sanitation lifts the penalty |
| 7 | 1 million, full war pressure for 30 years, food unchanged | 882,179 (−12 %) | the penalty alone is weak, because survivors are better fed |
| 7b | the same with a third of the food pillaged during the war | 592,104 after 30 years (−41 %); back to 1.06 million 30 years after peace | war acting through food and directly gives the losses of the worst regions of the Thirty Years' War |
| 8 | food for 10 times the people | 3 % a year: 438,389 from 100,000 in 50 years | the ceiling holds; no explosion |
| 9 | fed, health at half | slow decline to 92,574 in 30 years | the multiplier slows births, the penalty tips into decline |
| 10 | a 50-year turn | the same path as case 1 | yearly steps inside a turn |
| 11 | all food lost | emptied in one year by the starvation cap | the engine keeps size 1, as it does now |

**What the cases teach:**
- War must act both through food (pillaged plots, cut trade) and directly. Either alone is too weak or too sudden.
- A dense city without sanitation needs migrants to grow, as history shows. Migration is part of the model, not an
  extra.
- Integer arithmetic must use parts per million and carry remainders. With per mille, case 1 stalled 1 % short of its
  food limit (49,459 instead of 50,000), and the switch fixed it.

## 6. Parameters and how they are set

| Parameter | Value | Source or calibration |
|---|---|---|
| `N_MAX` | 3 % a year | Clark (birth and death rate ranges); Hutterites (Coale) |
| `A` | 0.30 | estimate; calibrate on England 1086-1300 (0.4-0.5 % a year) |
| `K` | 0.2 a year | Great Famine 10-15 %; Hunger Winter dose-response |
| minimum | 1,500 of 2,600 | Clark |
| `U` | 1.3 % a year | London migrants about 1700 (population figure to source) |
| `P_WAR` | 2.5 % a year | Thirty Years' War |
| `P_HEALTH` | 1 % a year | estimate; Cutler and Miller for the size of the water effect |

That is seven numbers. Each is tied to a case history and checked in `pop_model_sim.py` and `check_england1300.py`.

## 7. Good food beyond growth

| Effect | Proposed rule | Evidence |
|---|---|---|
| work output | a worker's output scales with the energy left for work, full at the need; below it, a share of people cannot work | Fogel: about a fifth of the people of England and France in the late 1700s too weak to work; 2,700 and 2,290 kcal per consuming unit |
| science and culture | multiplied by cognition, which falls with iodine and overall nutrient gaps | moderate iodine deficiency 10-15 IQ points; iodization +1 standard deviation in the most deficient quarter |
| commerce | through work output and goods; no separate bonus | |
| fertility | the food driver and `c` above | Hunger Winter |
| unit strength | protein coverage for living units (D27), one effect among these | |

## 8. Still to decide

- **The form:** hybrid, additive or multiplicative (hybrid recommended).
- **The parameters:** whether you accept the seven values and their calibration cases.
- **City size from people:** the inverse curve, or labour units.
- **Migration:** section 2 of `round_m76.md`.
