# The population model, step by step (D30, second version; R31.1, M77)

This replaces the first version (R30.1). You found health, fertility and much of what we had discussed missing
(M77). The model now counts **births** and **deaths** each from their causes, and every factor we discussed enters
one of them.

All results below are computed by `research/economy/plan/tools/pop_model_sim.py` in the integer arithmetic the DLL
would use (parts per million, remainders carried, 64-bit people). It is a proposal for your decision.

## 1. The bookkeeping

```
people next year = people + births − deaths + arrivals − departures
```

- Births and deaths are rates per 1,000 people a year (the demographers' crude birth and death rates).
- Arrivals and departures are migration (D33, `round_m76.md` section 2).
- **Life expectancy** follows from deaths: life expectancy at birth ≈ 1,000 ÷ deaths per 1,000. Clark: 33 per 1,000
  is 30 years. The city screen can show births, deaths and life expectancy.
- **On "no death term" (M75).** Deaths here are not an extra term bolted onto growth. They are half of the
  accounting every population obeys. Health lowers growth by raising deaths and lowering births, and turns it
  negative only when deaths outweigh births. Starvation stays as the hard floor.

## 2. Births: what raises and lowers fertility

```
births = B(food) × nutrients × economy × town life × religiosity × education × safety
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

## 3. Deaths: what kills

```
deaths = base mortality × (2 − health) + weakness of the underfed + famine + deficiency diseases + urban penalty + war
```

| Part | Size | Read from | Evidence |
|---|---|---|---|
| base mortality | 22 per 1,000 before modern medicine, falling to 8 with it | medicine and sanitation techs (Medicine, Modern Sanitation, Modern Health Care) | Clark (life expectancy = 1 / death rate); the modern value is an estimate to source |
| × (2 − health) | doubles base mortality at the worst health | the city's health balance: water supply and quality (D31), aqueduct, bath house, hospital, harms of the diet | clean water about 43-50 % of the US urban mortality decline 1900-1936 (Cutler and Miller) |
| weakness of the underfed | up to 12 per 1,000, falling to 0 at x = 1.3 | food sufficiency x | Fogel: a fifth of the people of England and France in the late 1700s too weak to work |
| famine | 200 per 1,000 × shortfall below x = 1 | x | Great Famine 1315-17: 10-15 % |
| deficiency diseases | up to 15 per 1,000 at no coverage | nutrient coverage | beriberi struck about 30 % of the Japanese navy each year; in 1904-05 it killed 27,000 of 211,600 cases |
| urban penalty | 13 per 1,000 × share in unsanitized dense quarters | urban density, sewer and water level (D31) | London infant mortality 300-400 per 1,000 births against 180 nationally (mid-1700s); London needed about 8,000 migrants a year about 1700 |
| war | 25 per 1,000 at full war pressure | enemy units in the plots, sieges, pillage | Thirty Years' War: 15-20 % average, over 50 % in the worst regions, mostly plunder, famine and plague |

**Starvation** stays as the floor: no city keeps more people than its food feeds at the biological minimum (1,500 of
2,600).

## 4. What decides the balance

**At the food limit** births and deaths meet at about 33 per 1,000 (case 1). That is the Malthusian equilibrium:
population settles where food per head meets need.

**What moves the balance:**
- **More food or better farming:** the city grows until food per head is back at the balance (case 2).
- **Better medicine and sanitation:** deaths fall, the city grows. If births stay high it grows fast; this is the
  first phase of the demographic transition (case 5, years 20-60).
- **Education, town life and secularization:** births fall and the city settles at a higher food per head. The
  equilibrium income rises, which is Clark's point about the birth schedule (case 11, secular).
- **Disease, bad water, deficiency, dense unsanitary quarters, war:** deaths rise. A city declines unless migrants
  come (cases 4, 6, 7, 10).

## 5. Edge cases (computed)

| Case | Setting | Result |
|---|---|---|
| 1 | a city at its food limit | births 33.4, deaths 33.3 per 1,000: balanced |
| 2 | a town of 1,000 with food for 50,000 | births 45, deaths 22: 2.3 % a year; reaches 50,500 and holds |
| 3 | two harvests at 70 % | −13.7 % over two years; births fall to 10.8 per 1,000 in the famine year, deaths reach 95; recovery afterwards |
| 4 | 500,000, all in unsanitized dense quarters, no migrants | 394,000 after 40 years (−21 %): such a city needs migrants |
| 5 | medicine from year 21, education from year 61, food growing 2 % a year | deaths 26 → 8, births 42 → 16 per 1,000; 1 million → 8.4 million in 140 years: the demographic transition |
| 6 | polished-rice diet (coverage 60 %), corrected in year 16 | deaths about 5 per 1,000 higher, slow decline; recovery after the diet changes |
| 7 | 30 years of war with a third of the food pillaged | −51 % (491,500); back to 947,000 30 years after peace |
| 8 | 1 million, half its food imported, imports cut | starvation cap at once (866,551), then deaths above 100 per 1,000 and births near 0, toward 525,000 |
| 9 | a hamlet of 10 with food for 40 | grows to 40 and holds (39-41) |
| 10 | health at half | deaths 40 against births 36: −10 % in 30 years |
| 11 | food 20 % above need: religious (× 1.1) against secular with schooling | religious grows to 122,700 and is then held by food; secular stays at 100,000, 20 % better fed |
| 12 | all food lost | emptied in one year (the engine keeps size 1) |

## 6. What good food does besides growth

| Effect | Rule | Evidence |
|---|---|---|
| work output | output per worker scales with the energy left for work; below the need, a share of people cannot work | Fogel (1790s England and France) |
| science and culture | multiplied by cognition, lowered by iodine and nutrient gaps | iodine deficiency 10-15 IQ points; US iodization +1 SD in the most deficient quarter |
| commerce | through work output and goods | |
| fertility and mortality | sections 2-3 | |
| unit strength | protein coverage for living units (D27) | |

## 7. Parameters

| Parameter | Value | Basis |
|---|---|---|
| births at x = 0.9 / 1.3 | 30 / 45 per 1,000 | Clark (range 30-60) |
| base mortality before / after modern medicine | 22 / 8 per 1,000 | Clark; modern value estimate |
| weakness of the underfed | 12 per 1,000 | estimate, set so births equal deaths near x = 1 |
| famine | 200 per 1,000 per unit shortfall | Great Famine |
| deficiency | 15 per 1,000 | estimate from beriberi rates |
| urban penalty | 13 per 1,000 | London infant mortality and migrants |
| war | 25 per 1,000 | Thirty Years' War |
| minimum | 1,500 of 2,600 | Clark |
| factor sizes (town 0.2, religiosity ± 0.1, education 0.65, safety 0.2, nutrients 0.2) | as in section 2 | sources named; sizes estimates |

## 8. Still to decide

- Whether these births and deaths, with these inputs, are the model you want.
- The estimates you want sourced first.
- How the city size follows people (the inverse curve or labour units).
