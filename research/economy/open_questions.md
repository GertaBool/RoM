# The plan's open questions: resolutions and proposals (R22, M68)

This file works through every open question in `research/economy/plan/design.json` and the open sections of the
research files (`population_formula.md`, `tile_output.md`, `food_resources.md`, `guilds/README.md`).

Each item is marked **Resolved** (the facts settle it) or **Proposal** (the facts do not; a detailed proposal for
your decision). Every number is marked as sourced (with its source) or *estimate*. Decisions stay with you; nothing
in design.json is changed to "decided" by this file.

## Contents

1. Tile yields by good and technology (PR.F1's missing tables) — Resolved for crops; Proposal for animals, timber, ore
2. Usable land per tile — Proposal
3. Skill, rotation and diminishing returns — Resolved / Proposal
4. Counting food: kcal, protein and edible shares — Resolved
5. Keeping and preserved forms (D27) — Proposal
6. Flour and fine cloth (D28) — Proposal
7. The population model (D30): parameters, migration and the AI — Proposal with sourced parameters
8. The guilds (D29): five open items — Proposal
9. Map-declared data (D24) — Proposal
10. Entertainment media (D21) — Proposal

---

## 1. Tile yields by good and technology (PR.F1)

**Resolved for crops.** USDA NASS *Crop Production Historical Track Records* (April 2026, `croptr26.txt`) gives US
yields from 1866 (rice from 1895, sugarcane from 1909). Converted to tonnes per hectare: corn bushel = 25.4 kg,
wheat bushel = 27.2 kg, hundredweight = 45.4 kg, short ton = 907 kg.

| Good | Pre-modern (source) | 1866-1900 (NASS) | 1930 (NASS) | 1950 | 1970 | 2000 |
|---|---|---:|---:|---:|---:|---:|
| Wheat, t/ha | 0.515 gross, 0.385 net, England about 1300 (Pretty 1990) | 0.74-0.82 | 0.95 | 1.11 | 2.08 | 2.82 |
| Maize, t/ha | | 1.53-1.76 | 1.29 | 2.40 | 4.54 | |
| Potato, t/ha | | 5.8-6.2 | 7.4 | 17.1 | 25.7 | 42.7 |
| Rice (paddy), t/ha | 1.0-1.5 before high-yield varieties (secondary) | 1.28 (1895) | 2.35 | 2.66 | 5.18 | 7.04 (8.46 in 2025) |
| Sugarcane, t cane/ha | Jamaica about 1.76 t coarse sugar/ha (Humboldt) | 33.6 (1909) | 34.7 | 76.4 | | 78.5 |
| Bananas, t/ha | smallholders 4.3-9.8 (Philippines), 30 per cycle (East Africa) | | | | | plantations 40-60 (unverified) |

**What the table shows:**
- Yields per hectare barely moved from 1866 to 1930. They rose two- to sixfold after 1940 (fertiliser, hybrid seed,
  pesticides).
- Labour per acre fell from about 55 hours to 3.5 over 1830-1930 (`tile_output.md`).
- So the game's tech stages split into two kinds:
  - **labour stages** (tools, draught animals, horse machinery, tractors) raise `ha per worker`;
  - **yield stages** (rotation, fertiliser, hybrids, pesticides, gene techs) raise `yield`.
- Per hectare in food energy (FAO kcal per 100 g): wheat 1866 2.5 million kcal, maize 5.5, potato 4.2, rice 3.6;
  English wheat 1300 net 1.3. That is why maize and potatoes spread wherever they arrived.

**Mapping to the mod's farm techs** (the stage list in `proposals.json` production, IMPROVEMENT_FARM
TechYieldChanges):

| Tech | Kind | Wheat t/ha (net) | Basis |
|---|---|---:|---|
| Agriculture | base | 0.385 | Pretty 1990 |
| Fermentation | food value, not yield (M54) | - | M54 |
| Mathematics | labour and estate management | 0.6 | *estimate*, Kent about 0.8 gross (Mate 1985) |
| Crop Rotation | yield; cropped share 2/3 to 1 | 0.8 | NASS 1866-1900 frontier 0.74-0.82 (low labour) |
| Biology | yield | 1.1 | NASS 1950 |
| Machine Tools | labour (100 ha per worker) | 1.1 | NASS: 1930 yield with 1930 labour |
| Pesticides | yield | 2.1 | NASS 1970 |
| Gene Manipulation | yield | 2.8 | NASS 2000 |

- **Other crops:** scale each stage by the NASS ratio of crop to wheat in the same year. In 1866-1930, maize is 1.4-2.1×,
  potato 7-8× (fresh weight) and rice 1.6-2.5× (paddy).

**Proposal for animals:**
- **Sourced:**
  - dressing share of live weight: cattle about 60-62 %, sheep about 50-54 %, pigs about 70-75 %;
  - boneless meat about 80 % of the carcass (South Dakota State; Montana State extension);
  - milk: London cows 1790s-1840s about 3,700 L a year, UK 1930s-40s 470-542 gallons (2,100-2,460 L), UK 2022/23
    8,133 L (AHDB);
  - the 14th-century Worcester estates kept about 0.8 cattle per 10 sheep.
- **Not found:** medieval milk yields, carcass weights and stocking rates.
- **Proposal** (*estimates* to be replaced when sources are found):
  - milk about 600 L per cow a year before Crop Rotation, 2,200 L at Biology, 8,000 L at Gene Manipulation;
  - live weight: cattle 250 kg, sheep 30 kg, pig 70 kg before improvement breeding; double at Biology;
  - grazing: 1 cattle or 5 sheep per hectare of grazing land.

**Proposal for timber:**
- **Sourced:**
  - coppice 2.5 t dry wood per ha a year (ash, oak, chestnut) and 6 t (poplar, willow) (UK conservation handbook);
  - chestnut 9-21 m³ per ha a year (Italy), 5.2-38.1 m³ (Spain).
- Use 2.5 t/ha a year for unmanaged forest, and raise it with managed forestry (the Lumbermill stage).

**Proposal for ore:**
- **Sourced:**
  - a small bloomery gave about 10 kg of iron per smelt;
  - a 14th-century high bloomery gave up to about 150 kg;
  - 3.2-4 kg of charcoal per kg of bloom (experimental smelts).
- Iron is made per furnace by smelts. With charcoal from timber, the Forge's iron output is bounded by charcoal:
  about 4 t of charcoal per t of iron. Ore per tile follows the deposit's grade (LD.F1).

## 2. Usable land per tile

**Proposal.**
- **Sourced:**
  - England 1086: 35 % arable, 25 % pasture, 15 % woodland, about 25 % moor, fen and heath;
  - about 1300: 29 % arable.
- **Proposal:** the shares of a plot that can carry crops (`arable`) and animals (`grazing`), by terrain and feature.
  These are *estimates*, set so that a mixed English-type landscape averages near the 1086 split.

| Plot | Arable | Grazing | Note |
|---|---:|---:|---|
| Grassland | 0.55 | 0.35 | |
| Plains | 0.45 | 0.45 | |
| Flood plains | 0.80 | 0.15 | |
| Hills (on any terrain) | × 0.5 | × 1.2 | terraces raise the arable share |
| Desert | 0 | 0.05 | oasis and flood plains as their own rows |
| Tundra | 0 | 0.30 | |
| Marsh | 0.05 | 0.35 | drained marsh becomes grassland |
| Forest | 0.05 | 0.15 | cleared to the terrain beneath; woodland gives timber |
| Jungle | 0.05 | 0.05 | |
| Snow | 0 | 0 | |
| Coast, ocean | fishing grounds | | section 1 of `tile_output.md` |

Placed resources keep the bonus multiplier (`fertility`) of D23.

## 3. Skill, rotation and diminishing returns

- **Skill: Resolved.**
  - Four years of schooling raised farm output 7.4 % on average: 10 % in modernising farming, 1 % in traditional
    farming (Lockheed, Jamison and Lau 1979/80; Phillips 1994 meta-analysis: 6 %).
  - So `skill` in farming is small: × 1.01 before the modern era and × 1.10 with schooling (Education and later).
  - Guild skill (D29) applies to crafts, not to fields.
- **Rotation: Resolved for the fallow share, open for the nitrogen effect.**
  - Two-field 1/2, three-field 2/3, Norfolk four-course 1 (no fallow).
  - No controlled yield comparison was found. The yield stages above carry the rest.
- **Diminishing returns: Proposal.** Keep D23's `min` (output per worker flat until the land binds). The England 1300
  check matches it without a smooth curve, and it adds no variable.

## 4. Counting food: kcal, protein and edible shares

**Resolved, with the per-good values sourced:**
- Food counts in kcal, for the population formula's `F`, and in protein, for D27's strength bonus. This is option
  (b) of `food_resources.md`.
- The values per 100 g come from FAO's *Food Balance Sheets* handbook, Annex I.

**Edible shares (sourced):**
- milling extraction: stone mills about 80 %, roller mills over 90 %; British white bread flour about 75 %, brown
  80-85 %; 60 lb of wheat gave 47-52 lb of flour (78-87 %);
- meat: dressing share as in section 1, times 80 % boneless;
- FAO's own values are per retail weight, so shells and bones are already out of molluscs and fish.

**Check:**
- England 1300 had 1.0 million t of net grain for about 4.75 million people. At 334 kcal per 100 g that is 1,926
  kcal per head a day from grain.
- Grain gave up to 80 % of a harvest worker's calories, which means about 2,400 kcal in all.
- That matches Clark's 2,400 kcal for 2 lb of wheat a day.

## 5. Keeping and preserved forms (D27)

**Proposal, built on sourced keeping times:**
- **Sourced:**
  - stockfish (dried, unsalted cod) keeps several years;
  - barrel-salted herring and salt cod keep for long voyages and months of overland transport;
  - traditional grain storage loses about 5 % a year, insects mostly (FAO); 20-40 % in poor storage; rats up to
    20 % a year in some villages.
- **Proposal:** a yearly spoilage rate per good. The goods pass (GW.F5) already stores and spoils.

| Form | Spoilage per year | Basis |
|---|---:|---|
| Fresh meat, fish, milk, fruit | 100 % (eaten in the year it is made) | |
| Grain in a granary | 5 % | FAO traditional storage |
| Grain without a granary | 25 % | FAO 20-40 % poor storage |
| Cheese, cured meat, salted fish | 15 % | *estimate* |
| Stockfish, dried fruit | 10 % | "several years" |
| Canned (with the Cannery) | 2 % | *estimate* |

- **How preserved forms arise:** a city with Salt preserves a share of its meat and fish, at *estimate* 0.2 t of salt
  per t of fish. Dairy becomes cheese by recipe (Settlement Essentials stages). There are no separate preserved
  goods; each food carries a fresh and a kept part. This stays within the 32-bit limit on new records (M59).

## 6. Flour and fine cloth (D28)

**Proposal:**
- **No Flour good.** Bread is made by the city's recipe straight from grain, at 0.8 extraction (stone milling, before
  Industrialism) and 0.9 after (roller mills). This follows M59: no mills for flour; the city makes goods from base
  goods.
- **Fine cloth is a guild luxury good** of the Drapers (section 8), not a general stage of cloth.

## 7. The population model (D30)

**Proposal: the compact model with the tile formula, with these sourced parameters.**
- `s`, food per head at equilibrium: 2,400 kcal a day before the demographic transition (Clark; England 1300 check).
  It rises with the transition techs to an *estimate* of 3,000 at Medicine and 3,400 at Refrigeration.
- `s_min`: 1,500 kcal a day (Clark's biological minimum).
- `r`, the growth rate:
  - England grew 0.4-0.5 % a year in 1086-1300 and 0.95 % a year in 1681-1821;
  - it reached about 1.5-1.75 % in the 1820s (Wrigley and Schofield, as tabulated by Munro, Toronto);
  - so `r` = 1 % before Medicine and 1.75 % from Medicine to Sanitation. It falls back to 0.5 % after the transition
    techs (fertility falls), an *estimate*.
- **Workers:** 40 % of people (the D23 estimate). It fits England 1300 at 3 ha per farm worker (section 3 of
  `tile_output.md`).
- **Migration:** each year a share `m` of the gap in food per head between connected cities moves people toward the
  better-fed city. *Estimate* `m` = 2 %. London's about 8,000 migrants a year around 1700 (Wrigley) is the scale to
  check it against.
- **The AI:**
  - `CvCityAI::AI_yieldValue` values food through `foodDifference()`, `growthThreshold()` and
    `FOOD_CONSUMPTION_PER_POPULATION` (CvCityAI.cpp around lines 10246-10621).
  - Proposal: keep those three as a translation layer.
    - `growthThreshold()` returns the people needed for the next size, `(size+1)^2.8 × 1000 − N`, in food units.
    - `foodDifference()` returns this year's logistic growth in the same units.
  - The AI's plot choice keeps working unchanged while the model underneath counts people. No AI rewrite is needed
    for the first version.

## 8. The guilds (D29)

**Facts:**
- **Venice:**
  - About 1271 the glassmakers' guild forbade telling trade secrets outside Venice.
  - In 1291 the Senate moved the furnaces to Murano, officially for fire, which also kept the secrets under control.
  - Emigrating masters faced a death penalty for a time; it was applied twice (Kidd 1979, as cited).
- **England:**
  - In 1300 Edward I's statute made the Goldsmiths' wardens assay silver from shop to shop and mark sterling (92.5 %)
    with the leopard's head; a maker's mark followed in 1363 and a date letter in 1478.
  - The Statute of Artificers (1563) set seven-year apprenticeships, ending no earlier than age 24, and one
    journeyman per three apprentices in certain trades. A master had to make a masterpiece.
- **Florence:** the Ordinances of Justice of 1293 put sovereignty with the popolo drawn from the seven major guilds,
  and excluded 152 magnate families from office.

**Proposal for each open item:**

**a. Once per game or national.** The criterion from the facts: a guild stays once per game, a world corporation,
where its luxury rests on a secret technique (Murano). It is national where its role is a public standard (the
Goldsmiths' hallmark) or a common craft.

| Guild | Kind | Luxury good it enables | Basis |
|---|---|---|---|
| Glassblowers | once per game | Crystal glass and mirrors | Murano secrecy |
| Drapers | once per game | Fine cloth (scarlet broadcloth) | finishing and dyeing secrets, Florentine Calimala (*proposal*) |
| Goldsmiths | national | Jewellery and plate, hallmarked | 1300 statute: a public standard |
| Blacksmiths | national | Fine blades and locks | *proposal* |
| Carpenters | national | Fine furniture | *proposal* |
| Masons | national | Carved stone and sculpture | *proposal* |
| Equestrians | national | Bred horses (warhorses) | *proposal* |
| Clerks | national | Books and manuscripts | *proposal* |
| Artists | national | Art (the existing Drama resource) | *proposal* |
| Bakers | national | Fine pastry and white bread | *proposal* |
| Butchers | national | Hams and sausages | *proposal* |
| Fishmongers | national | Delicacies (smoked and pickled fish) | *proposal* |
| Grocers | national | Preserves and confectionery (with Sugar) | *proposal* |
| Mercers | national | none of its own; trades the others' luxuries (+ trade route yield) | *proposal* |

The once-per-game guilds spread their technique as now (Master units, deals, espionage). The national guilds are
national wonders with their halls, option 3 of `guilds/README.md`.

**b. Quality grades.** Three grades, with the guild as assayer (the 1300 statute):
- **Common:** any maker.
- **Fine:** made in a city with the guild hall. It counts × 1.5 toward its need and trades at × 1.5 (*estimate*).
- **Masterwork:** made in the city of the world master guild or by a great person's workshop. It counts × 2 and
  trades at × 2.5 (*estimate*).

Only luxury goods and the trade's refined goods carry grades; staples do not.

**c. Political role.** Downstream effects, no public-order bonus:
- **Guild government:** under the Guilds civic, cities with three or more guild halls elect guild councils (the
  Florentine pattern). Changing a civic that guilds oppose raises their Revolution index. The Revolution mod's
  indices exist, and the Guilds civic already sets nationality and distance mods.
- **Price control:** a guild fixes the price of its trade's goods in its cities. Shortages show up as rationing, not
  as price spikes.
- **Entry control:** guilds limit craftsman places (d). Abolishing the guilds (the halls obsolete at Machine Tools)
  frees the places and removes the fixed prices.

**d. Master craftsmen and the population.** A craftsman place is a workshop in real people, not a citizen. At the
Statute of Artificers ratio it is 1 master + 1 journeyman + 3 apprentices = 5 people, drawn from the city's urban
people (D30 model). A guild hall opens *estimate* 4 places per 100,000 people, at most 40. The workshop makes the
trade's refined goods at a master's rate and its luxury goods at a grade.

## 9. Map-declared data (D24)

**Proposal: the schema of the BeginEconomy block, in three layers.** XML defaults come first, map values override
them, and the game state saves with the plot and the city.

```
BeginEconomy
    plot area km2=4470                       (exists, PR.F6)
    start era food per head=2400             (optional; default from the era)
    BeginPlot x=12,y=40
        deposit=BONUS_IRON, reserve t=2000000, grade=45
        fertility=BONUS_WHEAT:120
    EndPlot
    BeginPlayer id=0
        stock=BONUS_WHEAT seed:200, BONUS_COW head:500
    EndPlayer
    option=ECONOMY_LOANS:1, ECONOMY_CENTRAL_PLANNING:0
EndEconomy
```

- **XML defaults:**
  - fertility ranges per terrain and resource;
  - the deposit size per ore resource (proposal, section 1: reserve tonnes from grade);
  - starting seed stocks per era.
- **Map scripts:** they have no block, so they get their values from functions (as `getPlotAreaKm2` does).
- **The game options file:** a `Config/Economy.xml` with options as Revolution does. Its screens (loans, bonds,
  national budget, central planning, senate) are designed with you first, as recorded.

## 10. Entertainment media (D21)

**Proposal: services (option 2).**
- Drama, Music and Movies are made by their buildings and consumed by every city connected to the maker's trade
  network, without stock or shipping, while the network holds.
- This matches what media are: one performance or film serves many at no extra goods cost.
- It needs nothing until CN, as the present proposal says. It replaces "keep today's form" only in its target.

## Still open after this pass

- Medieval milk yields, carcass weights and stocking rates. A lead: the 13th-century *Hosebondrie* computes milk,
  butter and cheese per cow.
- Fish catch per fisher. A lead: Gloucester schooners landed 5,180 t of cod from 81 schooners in 1861, with crews in
  the fishing agreements.
- How much clover's nitrogen raised yields under the Norfolk rotation.
- How much salt preserving takes per tonne of fish or meat.
- Every value marked *estimate* above.
