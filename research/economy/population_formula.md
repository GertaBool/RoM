# A compact population formula (R19, M65): research and proposal for D30

The aim (M65): better modelling in general, disasters set aside, and a formula that raises or lowers population
without thousands of variables. Facts with sources come first (section 1), then the proposal (section 2), then
checks against the facts (section 3) and what stays open (section 4). The proposal is for your decision.

## 1. What the literature says (sources named; read 2026-11-05)

**The Malthusian model** (Clark, *A Farewell to Alms*, 2007, ch. 2, read from the chapter's text). It needs three
assumptions:
1. The birth rate rises with material living standards.
2. The death rate falls as living standards rise.
3. Living standards fall as population rises, because land is fixed (Ricardo's diminishing returns).

Facts from the chapter:
- **Subsistence income.** It is the income at which births equal deaths. Only the birth and death schedules set it.
  Technology and land only set how many people live at that income.
- **Technology.** An improvement raises income for a while, until population grows into it. In the long run only
  population rises.
- **Lower mortality.** Better sanitation, order or public relief in bad harvests also ends in more people at a
  lower income.
- **The two curves cross at about two surviving children per woman.** From about 1300 to about 1800, populations in
  western Europe grew only from 5.8 to 8.7 million (England) and from 17 to 27.2 million (France). Each had about 2.03
  to 2.10 surviving children per woman (Clark, table 2.1).
- **Numbers:**
  - Birth rates ran from under 30 per 1,000 (pre-industrial England) to over 50 (the highest observed is 50-60).
  - Life expectancy at birth is the inverse of the death rate: 33 per 1,000 means 30 years.
  - Two pounds of wheat a day (about 2,400 kcal, about 0.33 t a year) keeps a labourer fit to work. The biological
    minimum is about 1,500 kcal.
  - An English farm labourer's wage was about 18 lb of wheat a day in 1400 and 9 lb in 1650. Both were years of stable
    population, so the "subsistence" income itself differed by society and period.
  - In 1800 an acre fed a family in coastal China and Japan, while England had nearly twenty acres per farm worker.
    How hard land is worked rises with the people on it.

**Other evidence:**
- **Technology raised density, not income** (Ashraf and Galor 2011, *AER*). From 1 to 1500 CE, more advanced
  technology and better land raised population density but had no significant effect on living standards. An earlier
  start of farming also gave higher density at a similar income.
- **The feedback is real but weak and slow** (Lee 1987 and related work; I could not read the original, which
  returned HTTP 503).
  - Population fluctuated around a trend, and its swings moved real wages; wages in turn fed back weakly on fertility
    and mortality (an estimated fertility elasticity to wages of about 0.4).
  - The equilibrium depended strongly on the background level of mortality.
  - In England, population responded to wages as Malthus assumed until about the 17th century (a VAR study of
    1541-1840).
- **Population drives technology** (Kremer 1993). For most of history, the growth rate rose with population size:
  more people, more ideas.
- **Population drives how hard land is worked** (Boserup 1965). Land use moves from long forest fallow (20-25 years)
  through bush and short fallow to annual and multiple cropping as density rises. Output per hour falls at first.
  The evidence is mixed.
- **Farm productivity caps the urban share** (Bairoch; Wrigley).
  - The share of people in towns is bounded by the food surplus farms produce, unless food is imported. England
    imported grain in the 18th century.
  - Urban demand in turn pushed farm output up.
  - In England, about 68 % of men were still in farming around 1600 (Wallis, Colson and Chilosi 2017).
- **The demographic transition.** As incomes rose, fertility fell. In rich countries the relation between income and
  fertility later turns up again (estimated turning points of about 21,000-33,000 dollars a head; few observations).

## 2. The proposal: one equation, one cap, one share

Each city's people `N` are an `__int64` (rule F). Each year (a turn of several years runs its years in a loop; with
turns under a year, the fraction):

```
K = F / s                              carrying capacity: the food the city has, over food per head
N ← N + r · N · (K − N) / K            logistic growth toward K (shrinking when N > K)
N ← min(N, F / s_min)                  people beyond the biological minimum do not survive the year
u = max(0, 1 − s / q)                  urban share: the people farms do not need
```

**What goes in:**
- **F** is the city's food for the year, in tonnes of grain equivalent: production (D23), net trade and drawing on
  stores. It is computed by the goods economy already.
- **s** is food per head at equilibrium, in tonnes. It is set by the era or techs, and is the only lever on living
  standards:
  - the existing health balance lowers it (lower mortality means more people at a lower income: Clark);
  - the demographic-transition techs raise it (fewer births mean a higher income at equilibrium).
- **r** is the growth rate per year, which sets how fast `N` approaches `K`.
- **s_min** is the biological minimum, about 1,500 / 2,400 × the 0.33 t of Clark's working ration, so about 0.2 t.
  It is a constant.
- **q** is food produced per rural person, from D23's output per worker.

**What it replaces.** The food box (30 + 10 × size), the 3 food per citizen, and `size^2.8 × 1000` as the source of
people. The city's size (its number of citizens) follows from the people through the inverse of the curve the game
shows today: `size = (N / 1000)^(1/2.8)`. The display and the number of citizens keep their present scale and
meaning, but now follow food:

| People | 5,000 | 50,000 | 200,000 | 1,000,000 | 6,500,000 | 26,400,000 |
|---|---:|---:|---:|---:|---:|---:|
| Size | 1.8 | 4.0 | 6.6 | 11.8 | 23.0 | 37.9 |

**Three numbers to set** (r, s and s_min). Everything else comes from the goods economy and techs that exist.

## 3. Checks against the facts

- **Equilibrium at subsistence:** the formula reaches `N = K = F / s`, the Malthusian equilibrium (Clark). More food
  or better technology gives more people, not more per head (Ashraf and Galor), unless `s` rises.
- **Growth speed:**
  - England grew from about 1.5-2 million in 1086 to 4.5 million in 1300, about 0.4-0.5 % a year; the world averaged
    about 0.27 % a year in 1500-1820.
  - With `r` = 1 % a year, a city grows from 1,000 toward a capacity of 50,000 in 600 years to 90 %. In integer
    steps it reaches 25,444 after 400 years and 49,826 after 1,000.
  - With `r` = 2 % the same takes 300 years. A Bronze Age city then fills its land in 6-12 turns of 50 years.
- **City sizes:** if `F` is right, the sizes come out right without a separate rule. A city fed like Uruk (about
  40,000) is size 4; one fed like Rome (about 1 million, with imported grain) is size 12; Tokyo is size 38.
- **Urban share:** if farm workers make 1.35 times what they eat, `u` is 26 %, close to Rome's 20-30 %. At 1.05 times
  it is 5 %, near medieval Europe's 2-3 % to 10 %. The share follows farm productivity (Bairoch, Wrigley).
- **What the check shows about D23** (the tile's farmland share is open there):
  - At Agriculture (0.5 t/ha gross, a quarter kept as seed), a fully farmed 4,470 km² plot would feed about 500,000-
    670,000 people at 0.25-0.33 t each.
  - England's Domesday density (9-15 per km²) is 40,000-67,000 per plot.
  - So the farmed share of a plot, after fallow, pasture, forest and waste, has to be about a tenth of its area at
    that stage. Boserup's fallow stages are the natural way to raise it with density and techs.
  - This is the one figure the formula depends on that is not yet set.

## 4. Open

- `r` from a sourced series of growth rates by period (England 1541-1871, Wrigley and Schofield). The values above
  are illustrations.
- Food per head by era: Clark's 1400 and 1650 English wages show it varied.
- Whether `s` should also move with happiness or civics, or stay a function of techs and health.
- The tile's farmed share (D23 question 3), with Boserup's stages.
- How the AI values growth when the food box is gone (a reading of `CvCityAI`, not done).
- Migration between cities: by the same logic, people move toward the city where `F / N` is highest. That is one
  more rule, not more variables. It is left out here.
