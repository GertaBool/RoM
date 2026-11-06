# A tile's output: research for D23 and D30 (R20, M66)

You asked (M66) for output to depend on the technology, the people actually working the tile, how qualified they
are, the tools and machinery they have, the tile's fertility, and the good itself (grain, rice, roots, meat, dairy,
fish, sugar, bananas). This file holds the facts with sources (section 1), a formula built from them (section 2),
a check against one real economy (section 3), and what is open (section 4). It replaces the "farmed share" question
of `population_formula.md`. Nothing is decided.

## 1. Facts (sources named; web search 2026-11-06)

**How agricultural output is modelled.**
- Hayami and Ruttan estimated cross-country Cobb-Douglas production functions for 38 countries (1957-62 data). The
  inputs were labour, land, livestock, fertiliser and machinery, plus education and research. They treat the common
  function as an envelope, a "meta-production function", of all countries' possibilities. Later re-estimates found
  constant returns to scale (USDA ERS report 528).
- Eberhardt and Vollrath find an average labour elasticity of 0.10-0.20 in modern cross-country data. I did not find
  pre-industrial elasticities.
- Clark (*A Farewell to Alms*, ch. 2) gives the shape: on fixed land each added worker adds less. The same land goes
  from loose grazing to dairy, then arable, then garden as labour rises. In 1800 one acre fed a family in coastal
  China and Japan, while England had nearly twenty acres per farm worker.

**Labour and machinery (wheat, USA; USDA history as compiled in teaching sources and USGS DS 689):**

| Year | Equipment | Hours per 100 bushels | Acres per 100 bushels | Hours per acre | Bushels per acre |
|---|---|---:|---:|---:|---:|
| 1830 | walking plough, brush harrow, hand sowing, sickle, flail | 250-300 | 5 | about 55 | 20 |
| 1890 | gang plough, seeder, harrow, binder, thresher, horses | 40-50 | 5 | about 9 | 20 |
| 1930 | tractor, gang plough, disc, harrow, 12-foot combine | 15-20 | 5 | about 3.5 | 20 |
| 1987 | tractor, 35-foot disc, 30-foot drill, 25-foot combine | 3 | 3 | about 1 | 33 |

From 1830 to 1930, labour per acre fell about 16-fold while the yield per acre stayed the same. Machinery changed
how much land a worker can work, not what an acre gives.

**Draught animals.**
- Langdon (1986), as cited in secondary sources: horses were about 50 % faster than oxen and worked more hours a
  day. Oxen were cheaper to keep and held their resale value.
- By about 1300, nearly half of English peasants' draught animals were horses. On demesnes, oxen still outnumbered
  horses two to one at the end of the 14th century.

**Skill.**
- Lockheed, Jamison and Lau (1980) and Jamison and Lau (1982) found that farmers' schooling raised farm efficiency in
  31 of 37 studies. The effect was much more often positive in modern farming than in traditional farming.
- The often-quoted "four years of schooling" gain is said to be oversimplified. I could not confirm its size.

**Rotation (fallow).**
- The two-field system left half the arable fallow each year. The three-field system left a third.
- The Norfolk four-course rotation (turnips and clover) left none, and clover adds nitrogen.
- I found no controlled yield comparison between the systems.

**Land use, England.**
- About 1086: 35 % arable, 25 % pasture, 15 % woodland, about 25 % moor, fen and heath (Wikipedia, economy of
  medieval England).
- About 1300: about 10.7 million acres arable, almost 60 % of it under grain (Campbell, as cited in a 2023 article).
- On demesnes, arable was about 60 % of land use by value in the early 14th century.

**Yields and labour by good:**
- **Wheat, England about 1300:** 0.515 t/ha gross and 0.385 t/ha net of seed (Winchester manors; Pretty 1990, in
  `proposals.json`).
  - Yields per acre in English open fields before the Black Death were not passed until about 1700 (Campbell and
    Overton).
  - Output per worker rose after the Black Death, then fell as population grew (Allen 2000).
- **Rice:** before the high-yield varieties, about 90-130 man-days per hectare for 1.0-1.5 t of paddy (one secondary
  source, harvest excluded). With high-yield varieties, 200-250 man-days and up to double the yield, given
  fertiliser.
- **Dairy:** London cows in the 1790s-1840s gave about 530-820 gallons a year, and 9 quarts a day in 1842 (about
  3,700 L a year). The modern UK average is 8,133 L (AHDB, 2022/23). I found no medieval figure.
- **Meat and pasture:** in a Danish study, crops fed about 27 people per hectare and livestock about 2.3, on a calorie
  basis. Livestock's advantage is land that cannot be cropped.
- **Fish:** the Dutch herring fishery peaked at nearly 80,000 t a year in the early 17th century. Catch per boat per
  year was by and large stable from 1600 to 1850 (Poulsen 2008). I found no catch per fisherman.
- **Sugar:** in Jamaica, about 1,760 kg of coarse sugar per hectare (Humboldt, citing Stewart). Plantation output
  per enslaved worker roughly doubled across the British Caribbean in 1700-1790 through how labour was organised and
  other innovations.
- **Bananas:**
  - Philippine smallholders averaged 9.8 t/ha a year (dessert bananas), and low-yield farms 4.3.
  - East African smallholders get about 30 t/ha per cycle against a potential of 60.
  - Plantations are often given as 40-60 t/ha (unverified).

## 2. The formula

For each good a tile makes:

```
output = yield(good, tech) × fertility(tile, good) × cropped(rotation) × area worked
area worked = min( usable area(tile, good), workers × skill × ha per worker(tools, draught, machinery) )
```

Each factor holds one thing you named. Each is a lookup in one dimension, not a web of modifiers.

| Factor | What sets it | Facts it rests on |
|---|---|---|
| `yield(good, tech)` | output per worked hectare (t, L or head): seeds, varieties, fertiliser | wheat 0.385 t/ha net about 1300, UK about 2 t/ha in the early 20th century; rice doubling with high-yield varieties; bananas 4-60 t/ha |
| `fertility(tile, good)` | terrain, fresh water, the placed resource, later land qualities (LD) | the multiplier that already exists in D23 |
| `cropped(rotation)` | the share of worked land that bears a crop each year: 1/2, 2/3, then 1 with the four-course rotation | two-field, three-field and Norfolk systems |
| `usable area(tile, good)` | the plot's land that can carry this good: arable for crops, grazing for animals, fishing grounds for fish; set by the terrain, the features (forest, marsh) and the improvement | England: 35 % arable in 1086, 29 % in 1300 |
| `workers` | the tile's share of the city's real people who work (D30 model) | |
| `skill` | above 1 with schooling, guild training (D29) and specialists; stronger in later stages | Jamison and Lau: effects mostly in modern farming |
| `ha per worker(...)` | how much land one worker can work: hand tools, ox, horse, horse machinery, tractor, combine | USDA: about 55 h/acre in 1830, 9 in 1890, 3.5 in 1930, 1 in 1987; horses 50 % faster than oxen |

**What this does:**
- **No fixed farmed share.** The worked part of a tile follows from its people, their tools and skill, up to what the
  land allows. A thinly settled tile is worked in part, and a crowded one hits its land.
- **Tools and machinery are goods.** `ha per worker` rises only while the city has the tools, draught animals or
  machinery (the industrial chain of D28). Without them, workers fall back to the hand-tool rate.
- **Animal goods use the same form.** `yield` is head per hectare × product per head (milk, meat, wool); `usable area`
  is grazing land, mostly the land that cannot be cropped; `ha per worker` is the land one herder keeps.
- **Fish use the same form.** `usable area` is the fishing grounds of the sea plots, `yield` the catch per km², and
  `ha per worker` the grounds one fisher's boat covers. Overfishing is D25's sea mechanics.
- **Sugar and bananas** are plantation crops: `yield` per hectare, and how labour is organised in `ha per worker`
  (the Caribbean doubling).

**Joined with the population model.** Food `F` in `K = F / s` (`population_formula.md`) is the sum of these outputs,
plus trade, minus spoilage. While land is free, more people mean proportionally more food and the population grows.
Once `usable area` binds, more people add nothing, the population stops at `K`, and only better yields, rotation,
fertility or more usable land raise it. That is Clark's Malthusian equilibrium without a separate rule.

## 3. Check: England and Wales about 1300

The inputs are all sourced figures, except the share of people who work (40 %, the estimate in D23) and the land
area of England and Wales (151,058 km²).

- **Arable:** 10.7 million acres is 4.33 million ha, or 29 % of the land (35 % in 1086). Grain covered 60 % of it,
  2.6 million ha, which is the `cropped` share of a system between two- and three-field.
- **Grain:** 2.6 million ha × 0.385 t/ha net gives 1.0 million t. For 4.5-5 million people that is 0.20-0.22 t each,
  close to the 0.25 t ration used in D23. Dairy, meat, fish and pulses came on top.
- **Labour:**
  - With 40 % of people working and 80 % of those in farming, about 1.44 million farm workers worked 4.33 million ha.
  - That is 3.0 ha each (3.4 at a 35 % working share, 2.7 at 45 %), the 3 ha per worker of D23's first stage, taken
    from Columella's labour days.
- **What follows:** labour and land were both used up at about the same point. The formula puts England in 1300 at
  the land limit, the Malthusian ceiling the population reached before the Black Death. On the formula, the
  "farmed share" of a plot is arable 29 % × cropped 60 % = 17 % of the land in grain. The "about a tenth" in
  `population_formula.md` was this product with lower yields.
- **What would contradict it:** a working share well away from 35-45 %, or a grain area of 1300 far from 60 % of
  10.7 million acres.

## 4. Open

- **Usable area per tile:** how the terrain, the features (forest, jungle, marsh, hills) and the improvements set the
  arable and grazing shares. England's national 29-35 % includes moor and woodland plots, so a farmed grassland plot
  is higher.
- **Pastoral numbers:** head per hectare, milk and meat per head by period. The medieval figures are not found yet;
  1840s London cows gave about 3,700 L and modern UK cows 8,133 L.
- **Fish:** catch per fisher or per boat by period, and sustainable catch per km².
- **Sugar and bananas:** labour per hectare, and Reid's Jamaica tables (hogsheads per worker).
- **Yield for each rotation:** the rotation effect beyond the fallow share (clover's nitrogen).
- **Skill:** the size of the effect. The sources agree only that it is larger in modern farming.
- **Diminishing returns inside a tile:** the `min` makes output per worker flat until the land binds. Clark's curve
  is smooth: more labour per hectare raises yield, as in China's gardens. A smooth version, output rising toward a
  ceiling, would add no variable. It is left for the decision.
