# Decisions of M75, the three food measures, a reworked D30, the food box, and discussions (R29)

## 1. Recorded as decided (M75)

| Decision | What you decided | What it means for the plan |
|---|---|---|
| D24 | B: the three layers (XML defaults, map-wide, per plot, saved state), with `Config/Economy.xml` | built with LD and TR.F3; a large change |
| D21 | Media are services that can be imported and exported, by **reach**. Reach scales with technology, buildings and infrastructure, and applies across the country where those exist, as the Forge unlocks Gold's value in the main branch | see 1a |
| D27 | C: one spoilage rate per good set by technology (Fermentation, Refrigeration and the like), and also by **infrastructure** (granary, storehouse, cellar, cold store) and **climate** | see 1b |
| D28 | No Flour | clothes to be discussed (section 7) |
| D29 a | Once per game only where the luxury rests on a secret technique (Glassblowers, Drapers); the other twelve are national | |
| D29 c | Three grades: common; fine × 1.5; masterwork × 2-2.5 | |
| D29 d | Guild councils, fixed prices and limited craftsman places, tied to civics, with UI and AI integration | the AI must know these rules, as for every mechanic |
| D29 e | Workshops come with the guild or the guild hall, sized by the population proportion; not specialists | see 1c |
| D29 b | to discuss again (section 8) | |

### 1a. Media by reach (D21)

**Each medium has a reach that technology and infrastructure widen:**

| Medium | Before broadcasting | With infrastructure |
|---|---|---|
| Drama | performed locally: a theatre, odeon or amphitheatre serves its own city; similar performances elsewhere need their own theatres | recorded and broadcast drama only with radio and television; streamed with the internet |
| Music | local performance; travelling musicians reach nearby cities on the trade network | the gramophone and radio carry it nationally; recordings are a good |
| Movies | the cinema serves its city | television (an affordable set) carries them to every connected city; cable, satellite and the internet carry them across borders |

**The rules:**
- **The supply** is the buildings that make the medium (Broadway, Rock'n'Roll and Hollywood wonders, theatres, cinemas).
- **The reach** comes from the technologies and network buildings (broadcast tower, cable, satellite, internet infrastructure). Until broadcasting, reach is local or regional.
- **Import and export:** a city outside the maker's reach can import the service through a trade or deal (licensing), within the reach the infrastructure allows.

### 1b. Spoilage by technology, infrastructure and climate (D27)

`spoilage of good g in city c = base(g) × tech factor(owner) × store factor(c) × climate factor(c)`

| Factor | What sets it |
|---|---|
| base | the good's own rate (fresh meat high; grain low; FAO: traditional grain storage about 5 % a year, poor storage 20-40 %) |
| tech factor | preservation techs the owner has: Pottery, Fermentation, salting with Salt, Refrigeration, and the Cannery's process (a building effect: the Cannery lengthens shelf life; there is no canned good, as D28 decided) |
| store factor | the city's storage buildings (Granary, Storehouse and the like) |
| climate factor | the city's latitude or terrain: hot and humid raises spoilage, cold lowers it; a climate field per plot when LD brings it |

**Correction.** The R22 table listed a "canned" form at 2 %. That was a mistake: D28 dropped Canned Food (M58) and gave the Cannery a shelf-life effect instead. The form is removed (PR.F8.T5).

### 1c. Guild workshops sized by population (D29 e)

- A guild hall opens workshop capacity in proportion to the city's urban people, not a fixed count.
- **The share** (*estimate* to be sourced): in English towns the craft guilds' masters, journeymen and apprentices were a large part of the working townspeople; the share for each trade is open.
- **Workshops are not citizens or specialists.** They are a part of the urban people (D30) working in the trade at a master's rate.
- **Entry control (D29 d)** caps the share; abolishing the guilds removes the cap.

## 2. Calories, satiety and health: three separate measures

**What was wrong.** The R23/R24 measure folded protein into one "satiety" number. It gave no place to health, and it
read grains as moderately satiating. You pointed out that the three are different: apples and olives are healthy but
barely satiate; cured meat satiates and gives strength but harms health; grains satiate little and bring ailments.

### 2a. The measures

| Measure | What it is | Unit | Source of values |
|---|---|---|---|
| **Calories** | energy | kcal per kg of the good | FAO Annex I |
| **Satiety** | how much a food stills hunger per calorie, measured | index per 240 kcal, white bread = 100 | Holt et al. 1995, where measured; protein share and quality (DIAAS) as the fallback for goods not measured |
| **Health** | what a food adds to or takes from health: nutrients it covers, harms it brings | coverage of nutrient groups, and harm points | the sources below |

- A food's satiety per kg is its calories × its satiety index. The two stay separate quantities: an apple has a high
  index (197) but so few calories (48 per 100 g) that a kilogram stills little hunger.
- Health is independent of both.

### 2b. Measured satiety indices (Holt et al. 1995; white bread 100)

| Food | Index |
|---|---:|
| Boiled potatoes | 323 |
| Ling fish | 225 |
| Porridge (oats) | 209 |
| Oranges | 202 |
| Apples | 197 |
| Brown pasta | 188 |
| Beef | 176 |
| Grapes | 162 |
| Wholemeal bread | 157 |
| Eggs | 150 |
| Cheese | 146 |
| White rice | 138 |
| Lentils | 133 |
| White pasta | 119 |
| Bananas | 118 |
| White bread | 100 |
| Yogurt | 88 |
| Croissant | 47 |

Bread, rice and pasta sit at 100-157; fish, meat, potatoes and oats well above.

### 2c. Health: nutrients, deficiency diseases and harms (sourced)

**Diseases of a diet that lacks something:**
- **Scurvy (no vitamin C).** Lind's citrus trial (1747); the Royal Navy issued citrus daily from 1795.
- **Beriberi (no thiamine)** where polished white rice is the staple.
  - In the Japanese navy about 30 % of men were affected each year until Takaki changed rations to bread, meat and
    barley; within a decade it was under 1 %.
  - In the Russo-Japanese War, 211,600 soldiers had beriberi and 27,000 died of it, against 47,000 combat deaths.
- **Pellagra (no available niacin)** where maize is the staple without nixtamalization (lime treatment).
  - About 3 million cases and 100,000 deaths in the US South, 1906-1940.
  - Goldberger showed the dietary cause (1915); niacin was identified in 1937.
  - Mesoamerican maize eaters who treated maize with lime did not get it.
- **Iodine deficiency.** Moderate deficiency is associated with 10-15 IQ points lost (Bleichrodt and Born 1994, as
  cited). US salt iodization (1924) raised IQ by about one standard deviation in the most deficient quarter
  (Feyrer, Politi and Weil 2017).

**Harms:**
- **Dental caries** rose with the adoption of agriculture, varying with the cereal staple. Maize populations had more
  than rice populations.
- **Childhood bladder stones.** Norfolk had by far the highest incidence in Britain in the 18th and 19th centuries,
  possibly from its grain-based diet; one in 38 patients at the Norfolk and Norwich Hospital (1772-1816) was
  treated for them. Dairy cattle were inversely related to stone prevalence. Endemic stones occur where animal
  protein is low and hydration poor.
- **Processed meat** is IARC Group 1 for colorectal cancer (2015): about +18 % risk per 50 g a day (a measure of
  evidence, not of size of risk). Red meat is Group 2A.

### 2d. The health profile of each food good (a proposal; dimensions sourced above, values to be set from them)

The dimensions:
- protein quality;
- vitamin C (against scurvy);
- B vitamins: thiamine against beriberi, niacin against pellagra;
- iodine;
- fat;
- harms: processed or salted; refined starch or sugar (caries); stone risk in grain-only diets.

| Good | Calories (per 100 g) | Satiety index | Health profile |
|---|---:|---|---|
| Wheat (bread) | 334 | 100-157 (white-wholemeal) | thiamine and niacin present in wholemeal; low protein quality (DIAAS 0.40-0.48); no vitamin C; caries and stones when it is nearly the whole diet |
| Rice | 280 paddy | 138 (white) | polished rice lacks thiamine (beriberi); DIAAS 0.47 |
| Maize | 356 | not measured | niacin unavailable without lime treatment (pellagra); DIAAS 0.36; most caries of the cereals |
| Potato | 67 | 323 | vitamin C (potatoes counter scurvy: to source) |
| Beef, mutton, game, horse | 85-263 | 176 (beef) | complete protein (DIAAS 1.12 beef); B vitamins |
| Pig | 326 | not measured | complete protein; thiamine (to source); cured forms are processed-meat harm |
| Dairy (milk) | 61 | 88 (yogurt) | complete protein (1.14); against stones (Norfolk: dairy inversely related); hydration 1.5 (section 4b of open_questions) |
| Fish, shellfish, crustaceans | 15-86 | 225 (ling) | complete protein; iodine (seafood: to source with values); salted fish a salt harm |
| Whale | 136 | not measured | complete protein; fat |
| Apple | 48 | 197 | vitamin C (to source amount); fibre |
| Lemon | 15 | (oranges 202) | vitamin C: against scurvy (Lind) |
| Banana | 60 | 118 | potassium, vitamin C (to source) |
| Olives | 175 | not measured | fat; healthy oil (to source) |
| Sugar | 373 | not measured (sugary foods low: jellybeans 118, Mars bar 70) | caries; no nutrients |
| Wine, ale | 68, 49 | not measured | alcohol harm (to source); ale gave calories |
| Salt | 0 | - | carries iodine once iodized (1924); preserving; salt harm in excess (to source) |

### 2e. How a city's diet acts (proposal)

- **Calories** decide whether people have the energy to work and grow (section 3).
- **Satiety** decides how much food people want. A city eating low-satiety grains eats more of them for the same
  contentment. Satiety enters the food need: hunger is met when satiety per head reaches the need.
- **Health:**
  - each nutrient group is covered or not by the city's diet as a whole (a share of need);
  - an uncovered group brings its disease as bad health and lost output: scurvy, beriberi, pellagra, iodine
    deficiency, the latter costing science and culture through cognition;
  - harms add bad health per amount eaten.
- **Strength** (D27's protein bonus) becomes one effect of protein coverage among several, not a separate margin.

## 3. D30 reworked from your principles

**Your principles (M75):**
- Population grows and behaves by nutrient quality and quantity.
- Good food raises fertility, productivity, commerce, science and culture.
- Players decide how well a city does; not a curve.
- Urban density, the economy, and the threat of war and pillage matter.
- No growth rates by era: technologies, improvements, trade and densities shape growth by themselves.
- Health lowers growth or turns it negative, rather than a separate death term; starvation exists already.

**Facts for each factor:**
- **Nutrition and fertility.** In the Dutch Hunger Winter (1944-45), conceptions resulting in births fell markedly
  below a calorie threshold. They tracked the official daily ration (dose-response) after a lag of about two months,
  and recovered at once when the famine ended (Stein and Susser 1975).
- **Nutrition and productivity.**
  - Fogel: about a fifth of the people of England and France in the late 1700s were too weak to work.
  - Average intake about 2,290 kcal per consuming unit in France and 2,700 in England.
  - Better diets and the work efficiency they brought are credited with about 30-50 % of British growth since 1790
    (estimates differ; contested as glib).
- **Nutrition and cognition:** iodine (section 2c): 10-15 IQ points; one standard deviation in the most deficient
  quarter.
- **Urban density.** Until the 20th century cities were deadlier than the countryside (the "urban penalty"). In the
  17th-18th centuries they were demographic sinks that needed immigrants. British urban life expectancy converged
  with rural in the 1930s and then passed it.
- **The economy.** In England, high food prices showed up more in fewer marriages than in more deaths (Wrigley and
  Schofield, as discussed).
- **War and pillage.** The Thirty Years' War cost the German lands about 15-20 % of their people, and over 50 % in
  the worst regions (Württemberg, Pomerania). Most civilian deaths came from plague, famine and disease, famine
  driven by repeated plundering of the same areas.
- **Health and water:** clean water about 43-50 % of the US urban mortality decline 1900-1936 (Cutler and Miller).

**The proposal.** One growth rate per year, the sum of contributions each read from the game state. No era table and
no separate death term.

```
g = a·(nutrition − 1) + b·(economy) − c·(bad health) − d·(urban density × (1 − sanitation)) − e·(war pressure)
N ← N·(1 + g)        (g may be negative; starvation as now when stores are empty)
```

| Term | Read from | Sources for the size of its coefficient |
|---|---|---|
| nutrition | satiety per head against the need, times the share of nutrient groups covered (section 2e) | Dutch Hunger Winter dose-response; Fogel |
| economy | food price against wages, or work for the people (goods economy) | Wrigley and Schofield: prices act through marriage |
| bad health | the city's health balance (water, disease, nutrient gaps, harms) | Cutler and Miller; deficiency diseases |
| density | urban people per km² against the water and sewer level (D31) | the urban penalty, closing in the 1930s with sanitation |
| war pressure | enemy units in the city's plots, pillaged plots, siege | the Thirty Years' War, by plunder and famine |

**Good food beyond growth:**

| Effect | Proposal | Source |
|---|---|---|
| Productivity | each worker's output scales with energy available for work, reaching full output at the need; a fifth of people too weak at 1790s intakes | Fogel |
| Commerce | follows from productivity (more goods, more trade); no separate bonus | |
| Science and culture | cognition through iodine and overall nutrition | iodine studies |
| Unit strength | protein coverage for living units (D27), kept as one effect | |

**Coefficients.** `a` to `e` are calibrated so that England 1300, the Hunger Winter and the 1900-1936 US cities are
reproduced (`check_england1300.py` extended). That is five numbers, each tied to a source case.

**Still to choose:**
- (i) the additive form above, or a multiplicative one (each factor scales the positive rate);
- (ii) how the city size follows people (the inverse curve, or labour units);
- (iii) migration (section 6).

## 4. The food box and what the game draws (R29.4, code map at d2a8f756)

**What the executable asks the DLL for** (`codemap/entry_points.md`, exported CvCity and CvGameTextMgr methods):

| Exported function | What it returns now | What draws it |
|---|---|---|
| `CvCity::getFoodBarPercentages` | three fractions: stored, rate, rate extra (`getFood()`, `foodDifference()`, `growthThreshold()`) | the city bar above the city on the map |
| `CvCity::getCitySizeType` | `getPopulation() / 7`, capped at the size classes | which city art (buildings) the map shows |
| `CvGameTextMgr::buildCityBillboardCitySizeString` | the number `getPopulation()` | the size number on the city bar |
| `CvCity::getCityBillboardSizeIconColors`, `CvGameTextMgr::getCityBillboardFoodbarColors` | colours | the bar and icon colours |

**The city screen** is Python: `CvMainInterface.updateCityScreen` draws its food bar and texts from `growthThreshold`
(14 calls), `getFood`, `foodDifference` and `getFoodTurnsLeft`. Python can draw anything there.

**What follows:**
- The executable never computes growth. It asks for fractions, a size class, a string and colours.
- The growth mechanics can be replaced entirely in the DLL, and the same exported functions refilled:
  - the bar shows the city's progress in people toward the next size: stored = (N − people at this size) ÷ (people
    at the next size − people at this size); rate = this year's growth in the same terms; red when shrinking;
  - the billboard string can show the size, or people in thousands;
  - the map art follows the size class from people.
- The city screen can be redrawn in Python with the new numbers: people, nutrition, health, water.
- **The one engine tie to keep:** the number of citizens working plots is `getPopulation()`. The size from people
  must stay an integer that the engine uses for worked plots.
- **To check in game** (only you can see the screen): that a refilled bar and string display as expected.

## 5. Why canned food was listed

It should not have been. D28 (M58) dropped Canned Food and gave the Cannery a shelf-life effect. The "canned 2 %" row
in the spoilage table of `open_questions.md` section 5 and in `nutrition.json` contradicted that decision. Both are
corrected under PR.F8.T5.

## 6. Migration: points for our discussion

1. **Within a player:**
   - do people move between your own cities toward better food, work, health and safety on their own, or only when
     the player permits or drives it (civics, policies)?
   - how fast: a share of the gap a year, limited by distance and roads?
2. **Between players:**
   - do people cross borders (immigration, refugees from war and famine)?
   - should civics or borders control it (closed borders, emancipation, serfdom binding peasants to land)?
3. **City growth:** cities were demographic sinks that grew by migration from the countryside. Should a city's
   growth beyond its own births come only from migration out of its hinterland and other cities?
4. **Who moves:** workers and their families, so skill and culture move too (guild craftsmen; the Venetian
   glassmakers' emigration ban)?
5. **Effects:** on the place left (labour shortage, land abandoned) and the place reached (crowding, unrest,
   culture and religion).
6. **AI:** the AI must see migration in its city valuation (the D29 d principle).

## 7. Clothes (D28): points for our discussion

**What the game has:**
- fibre and skin resources: Wool (restored as a good), Cotton, Silk, Fur, Leather, and Cannabis (hemp);
- Dye;
- no flax or linen resource.

**Questions:**
1. **Need:** is clothing a need per person scaled by climate (cold plots need more), as warmth, or also as status
   (fine cloth as a luxury)?
2. **Chain:** fibre to yarn (spinning) to cloth (weaving) to garments (tailoring), with dyeing and fulling. Which
   steps are goods, and which happen inside the city as with bread?
3. **Fibres:** what each brings: wool for warmth; cotton for light cloth; linen (missing: add flax or not); silk as a
   luxury; fur for cold climates; leather for shoes and belts.
4. **Technology:** the spinning wheel, flying shuttle, spinning jenny, water frame and power loom. Textiles were the
   largest pre-industrial manufacture and led industrialization.
5. **Wear:** clothes last a time and are replaced, so the need is a flow per person a year.
6. **Guilds:** Drapers make fine cloth (a luxury; D29); whether weavers, fullers and dyers are part of it.

## 8. The guild luxuries (D29 b): points for our discussion

The proposed table (`open_questions.md` section 8), with the questions for each:
- **Glassblowers** (once per game): crystal glass and mirrors (Venice).
- **Drapers** (once per game): fine cloth (Florentine finishing). Is the secret the dyeing or the finishing?
- **Goldsmiths:** hallmarked jewellery and plate. Is the Jewellery building's role here?
- **Blacksmiths:** fine blades and locks, or clocks and instruments?
- **Carpenters:** fine furniture, or ships' fittings?
- **Masons:** carved stone and sculpture, or a construction effect instead of a luxury?
- **Equestrians:** bred warhorses, as a good or as a unit quality?
- **Clerks:** books and manuscripts, or a science effect?
- **Artists:** art (Drama exists as a medium, D21).
- **Bakers, Butchers, Fishmongers, Grocers:** fine foods (pastry, hams, smoked fish, preserves and confectionery). Do
  victualling guilds make luxuries, or improve the city's food health and keeping (section 2)?
- **Mercers:** trade only, or a luxury of their own?

## 9. Plan changes in this round

- design.json: D24, D21, D27 (open item), D28 (Flour), D29 a/c/d/e recorded; D30 keeps open with the principles and
  the reworked proposal.
- plan.json: PR.F8.T5 (nutrition table and generator to three measures, the canned form removed, D27 C); FD.F1's
  fields become calories, satiety index and health profile.
