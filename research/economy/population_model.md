# The population model: research for D30 (R17, M63)

The question (D30, from M62): should one citizen keep standing for the number of people the game's curve gives it,
or should population follow a model closer to real settlements? This file holds the facts first, each with its
source (sections 1 to 4). Readings come after them (section 5) and options for the decision last (section 6). Nothing
here is decided.

## 1. What the game does now (code and XML, GitLab main)

- **People shown.** `CvCity::getRealPopulation()` = `(long)pow(size, 2.8) * 1000`
  (`Assets/CvGameCoreDLL/CvCity.cpp`, line 6089). The player total `CvPlayer::getRealPopulation` adds up its cities.
- **Growth.** `CvPlayer::getGrowthThreshold(size)` = `BASE_CITY_GROWTH_THRESHOLD` (30) + size ×
  `CITY_GROWTH_MULTIPLIER` (10). This is then scaled by the game speed's and the start era's growth percent, and for
  the AI by the handicap's AI growth percent and per-era modifier (`CvPlayer.cpp`, line 23681; `GlobalDefines.xml`).
  The food needed for each new citizen grows by a fixed step per size.
- **Eating.** Each citizen eats `FOOD_CONSUMPTION_PER_POPULATION` = 3 food (`GlobalDefines.xml`), whatever its size.
- **The city's land.** A city works its own plot plus up to 20 others (the 21-plot fat cross). The plot area
  (PR.F6) is 4,470 km² on Mediterranean Standard (the harness map), 1,770 km² on Huge Europe and 46,000 km² on RFC
  Earth (`research/economy/plan/map_scale.json`).

The curve, worked out (people = `int(size^2.8) × 1000`; the last two columns divide by 21 plots of the two maps):

| Size | People | Per citizen | The last citizen adds | Per km², Medit. Standard | Per km², Huge Europe |
|---:|---:|---:|---:|---:|---:|
| 1 | 1,000 | 1,000 | 1,000 | 0.01 | 0.03 |
| 2 | 6,000 | 3,000 | 5,000 | 0.06 | 0.16 |
| 4 | 48,000 | 12,000 | 27,000 | 0.5 | 1.3 |
| 6 | 150,000 | 25,000 | 60,000 | 1.6 | 4.0 |
| 8 | 337,000 | 42,125 | 105,000 | 3.6 | 9.1 |
| 10 | 630,000 | 63,000 | 161,000 | 6.7 | 16.9 |
| 12 | 1,051,000 | 87,583 | 228,000 | 11.2 | 28.3 |
| 15 | 1,963,000 | 130,866 | 345,000 | 20.9 | 52.8 |
| 20 | 4,394,000 | 219,700 | 588,000 | 46.8 | 118.2 |
| 30 | 13,675,000 | 455,833 | 1,239,000 | 145.7 | 367.9 |
| 36 | 22,784,000 | 632,888 | 1,728,000 | 242.7 | 613.0 |

- **Food per person.** Growing from size 35 to 36 needs 380 food (before the percents) and adds 1,728,000 people.
  Growing from 1 to 2 needs 40 food and adds 5,000. A size-36 city eats 108 food a turn for 22.8 million people; a
  size-1 city eats 3 for 1,000.
- **D23 (decided in M54)** counts a tile's workers as people per citizen × 40 %. With the wheat stages in
  `proposals.json` (3 ha per worker at Agriculture, 100 at Machine Tools), on a 4,470 km² (447,000 ha) plot:

  | Size | Workers on one tile | Agriculture: area worked | Machine Tools: area worked |
  |---:|---:|---:|---:|
  | 2 | 1,200 | 3,600 ha (0.8 %) | 120,000 ha (27 %) |
  | 8 | 16,850 | 50,550 ha (11 %) | the whole plot |
  | 20 | 87,880 | 263,640 ha (59 %) | the whole plot |
  | 36 | 253,155 | the whole plot (needs 170 %) | the whole plot |

  The plot's farmland share is still open (D23, question 3). With less than the whole plot as farmland, the bound
  binds sooner.

## 2. How large cities get in this mod's games (harness telemetry)

- **Source and limits.** The 30 baseline games of P18 (Mediterranean Standard, 150 turns, 6000 BC to 1300 BC,
  `research/economy/settlement/data/games.json`). The telemetry has each player's number of cities and total
  population, not each city's size.
- **At turn 150 (1300 BC).** The players' average city size has a median of 6.8, ranging from 2.8 to 12.5
  (302 players). One game (P22, seed 958082699) had 100 cities with 693 citizens in all, an average of 6.9.
- **Captures.** 57 cities were captured; the largest had 10 citizens, the median 2.
- **Human games.** In the analysed human game 2 (6000 BC to 875 BC), the largest city taken had 9 citizens
  (`research/ai-warfare/games/game2/analysis.md`).
- **Open.** I have no record of city sizes after 875 BC in this mod. The longer headless games (450 turns) did not
  keep per-city sizes.

## 3. Real settlement sizes

**Largest city in the world by date.** These come from Wikipedia's list of largest cities throughout history, which
draws on Chandler, Modelski and Morris; the 2025 figures are from the UN World Urbanization Prospects.

| Date | Largest city, population |
|---|---|
| 3000 BC | Uruk, about 40,000-45,000 |
| 2000 BC | 40,000-65,000 |
| 500 BC | Babylon, 150,000-200,000 |
| 1 AD | Rome, 0.8-1 million |
| 500 | Constantinople, 400,000-500,000 |
| 1000 | Kaifeng about 1 million; Baghdad 1.2 million; Córdoba 350,000 |
| 1200 | Hangzhou or Baghdad, about 1 million |
| 1500 | Beijing, 0.6-1 million |
| 1700 | 0.65-1 million |
| 1800 | Beijing, 1.1 million |
| 1900 | London, 6.5 million |
| 1950 | New York, 12.5 million |
| 2000 | Tokyo, 26.4 million |
| 2025 | Jakarta 41.9 million, Dhaka 36.6 million, Tokyo 33.4 million (UN WUP 2025, its own urban-agglomeration definition) |

**Single cities over time:**
- London: about 1.01 million in 1801, 2.29 million in 1851, 6.23 million in 1901, 7.17 million in 2001 (Greater
  London, census).
- Paris: about 200,000 in 1328; about 350,000 in 1574.

**Size distribution.** City sizes in a country roughly follow Zipf's law: the n-th city has about 1/n of the largest
city's population, with an exponent near 1 (Gabaix 1999; the exponent varies by country and era).

**Output and city size.** Bettencourt et al. (2007) found output rising faster than population across modern cities
(an exponent of about 1.15). Later work disputes how general this is: for England and Wales, income scales about
linearly with city size (Arcaute et al. 2015).

## 4. Population, urban share and demography

**States and the world:**
- **Rome and Han China.** The Roman Empire had about 45-60 million people around 1 AD (Harper: 60 million). Han
  China's census counted about 60 million.
- **England.** About 1.25-2 million in 1086 (Domesday; about 9-15 people per km²). About 4.5 million or more around
  1300 (about 35 per km²). About 4.15 million in 1600.
- **The world.** About 4 million in 10,000 BC; 170-300 million in 1 AD; 265-295 million in 1000; about 425-461
  million in 1500; 0.9-1.0 billion in 1800 (the range of the HYDE, McEvedy-Jones and Maddison series as collected by
  Our World in Data and the US Census Bureau).

**Urban share:**
- **Europe.** About 2-3 % before the 1300s. In towns of 5,000 or more, about 10-11.5 % in 1500 and about 12-13 % in
  1700 (Bairoch). In towns of 10,000 or more, 7.4 % in 1500 and 10.1 % in 1800 (de Vries 1984).
- **The Roman Empire.** About 20 % (Hanson 2016, 1,388 cities); 25-30 % with a 5,000 threshold.
- **The world.** About 20 % urban in 1950, and a majority urban from 2007 by the UN's national definitions (Our World
  in Data).

**Who worked the land.** In England, about 80 % of the workforce in agriculture in 1300, about 74 % in 1500 (Allen),
about 60 % by 1560 (Clark), and 35-45 % by 1800.

**Births, deaths and migration:**
- **Before industry.** Birth and death rates were each about 40 per 1,000 a year, roughly in balance. Long-run growth
  was about 0.02-0.1 % a year, and about 0.27 % a year in 1500-1820 (Maddison).
- **Cities needed migrants.** Their deaths exceeded their births (the "urban graveyard"): London needed about 8,000
  migrants a year around 1700 (Wrigley 1967).
- **The demographic transition.** Death rates began to fall in north-western Europe in the late 18th century, birth
  rates in the late 19th. England's transition ran from about 1750 to about 1975.

**Hinterlands.** A medieval English market town drew on about 8-12.5 km around it (Dyer). London's grain came from
more than 4,000 square miles (about 10,400 km²) around 1300 (Campbell et al., *A Medieval Capital and its Grain
Supply*).

## 5. Readings (from the facts above; each says what would contradict it)

**R1. As a city alone, the curve is too large for the pre-modern eras.**
- At 1300 BC the median player's city is about size 7, which the game shows as 232,000 people. The largest real city
  of 2000 BC had 40,000-65,000, and Babylon around 500 BC had 150,000-200,000.
- So the average harness city at 1300 BC is shown as larger than any city on earth before about 500 BC.
- Contradicted if: a source puts several cities of 200,000 or more around 1300 BC.

**R2. At the top, the curve fits modern metropolitan areas.** Size 30-36 gives 13.7-22.8 million. That is the range
of New York in 1950 to Tokyo in 2000, so the curve's top end is a 20th-century agglomeration.

**R3. As a city with its countryside (21 plots), the curve gives believable rural densities in the middle sizes.**
- On Mediterranean Standard, sizes 10-15 give 7-21 people per km² over the 21 plots, close to England in 1086
  (9-15). Size 20 gives 47 per km², near England in 1300 (about 35).
- So the number reads better as a region's population than a city's. A Civ city then stands for a town plus its
  district, of which only a share is urban (2-3 % in early medieval Europe, 10-13 % in 1500-1800, about 20 % for Rome).
- Contradicted if: the 21 plots overlap so much in real games that the land per city is far smaller (shared plots
  are not counted twice). Also, on Huge Europe the same sizes give 2.5 times the density.

**R4. The curve grows people faster than food.**
- The food needed per growth step rises linearly (30 + 10 × size), while the people added rise as about size^1.8.
- So each new person costs less food the larger the city, and each citizen eats 3 food whether it stands for 1,000
  people or 633,000.
- Real growth runs the other way: it was slow (about 0.1 % a year) and bounded by food per person.
- For the goods economy this means consumption has to be counted per person (as D23 counts workers per person), not
  per citizen, or a large city eats far too little per head.

**R5. Your point about productivity, in these terms.** The citizen at size 36 stands for 1.73 million added people;
the first stands for 1,000. Under D23 that citizen's tile cannot use them: from about size 20 at Agriculture, and
size 4 at Machine Tools, the plot's land binds, not its workers. That matches the historical pattern, in which large
cities were mostly not farmers (England's farm share fell from 74 % to 35-45 % while London grew). It suggests the
large numbers should go to non-farm work (crafts, services, industry) and to consumption, not to the worked tile.

**R6. Craftsmen and guild places.** A master craftsman is one person with a few journeymen and apprentices. A citizen
of tens or hundreds of thousands cannot be one. The places a guild opens need a unit in real people (for example a
workshop of 5-10), independent of city size, and that needs a population counted in people.

## 6. Options for D30

**1. Keep `size^2.8 × 1000` (D23 as decided in M54).**
- How it works: workers and consumption are counted per person from this curve; citizens stay the unit of tiles and
  specialists.
- For: nothing changes in growth, saves or the AI.
- Against: R1 (early cities 4-6 times too large) and R4 (food per person falls with size).
- Craftsmen (R6) would have to be a share of a specialist's people, not places.

**2. A curve fitted to real sizes, by era.**
- How it works: for example, people = a × size^b with a and b set per era, so that a large city of the era matches
  the table in section 3 (about 50,000 in the Bronze Age, about 1 million from Rome to 1800, tens of millions only in
  the modern era).
- For: one function changes (`getRealPopulation`); the display becomes plausible.
- Against: the people per citizen still follow size, not food. R4 remains. A city's people jump when the era changes.

**3. Population as people (a demographic model); city size follows from it.**
- **How it works.** Each city keeps its people in an `__int64` (rule F), split into urban and rural. They change each
  year by births, deaths and migration:
  - Births and deaths depend on food per person, health and the era's medicine. Pre-industrial rates are near
    40 per 1,000 each; the transition comes with the right techs.
  - People move from the countryside to the city by the city's pull: jobs, food, happiness. The city's own excess
    deaths (the urban graveyard) are made up this way.
- **Citizens become labour units:**
  - A worked tile takes the rural workers its land can use (D23's min already does this).
  - Specialists and craftsman places take urban people in units of a real size (R6).
  - The city's size (the number of citizens) follows from the people and the era's land use, not from a food box.
- **For:**
  - It is the model a real economy has.
  - It answers R1 and R4 to R6.
  - Goods needs and consumption are per person, as SD and CN already assume.
  - The urban/rural split gives the craftsmen, guilds and industry their workforce.
- **Against:**
  - It is the largest change: growth, starvation, the food box, the city screen, saves and the AI's growth valuation
    are all touched.
  - It needs sourced rates per era, and a check that the AI still grows its cities.

**4. Between 2 and 3.**
- How it works: keep Civ's food-box growth for the number of citizens, and keep an `__int64` people count per city
  beside it. The people count grows toward a capacity set by the citizens, the era and the food stored, with an
  urban share by era (section 4).
- For: the display, consumption and craftsman places use people. The engine's growth, the AI and saves change little.
- Against: two population numbers that can drift apart. The UI must explain which one counts for what.

**What would decide between them.**
- How far the engine's growth and the AI's city valuation can change: a reading of `CvCity::doGrowth` and
  `CvCityAI` for options 3 and 4, not done yet.
- Whether citizens should stay tile workers at all in the industrial era (R5).

**Open (not researched here):**
- City sizes in this mod after 875 BC.
- How much the 21-plot crosses overlap in real games.
- Sourced birth and death rates per era beyond the pre-industrial and transition figures above.
