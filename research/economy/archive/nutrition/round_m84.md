# Corrections, bioavailability, why the size curve works, yearly steps (R38, M84)

## 1. Recorded (M84)

| Topic | Decided |
|---|---|
| Too much food | Not a harm band. Food above need is surplus; leftovers go to long-term storage. Fat is not bad in itself: its value depends on what the animals ate, freshness, the vitamin E of unsaturated oils and their omega-3 to omega-6 ratio. This is context for the model, not something to map |
| Whale as food | only for cultures that hunted whales and had access to them |
| Age structure | abstracted away: one population with crude rates |
| Child and adult burdens | abstracted: one burden |
| Food box | progress in people toward the next size |
| Urban density | the people not working plots |
| Unsanitized penalty | set by density and mitigating infrastructure and hygiene, not by city size. Without hygiene, 500,000 and 10 million fare alike |
| Turn length | yearly steps inside a turn (shown in section 6) |

**What changes in `round_m83.md`:**
- Section 2c loses the upper band: excess food goes to storage.
- The coverage reading in 2b is corrected in section 2.

## 2. Corrections to my reading of the coverage table

**Liver has plenty of vitamin A.**
- USDA: beef liver 4,970 µg and pork liver 6,500 µg (RAE) per 100 g. That is 8.7 and 11.4 times the daily 570 µg in 100 g.
- What lacks vitamin A is muscle meat. The table ate only muscle meat in "beef only", so "meat lacks vitamin A" was wrong.

**Milk is an inland food and gives iodine.**
- The table already showed it: milk alone covers 4.55 times the iodine need (MEXT: 16 µg per 100 g).
- Across 34 countries, milk holds 5.5 to 49.9 µg per 100 g (median 17.3). It is higher in winter, and higher in conventional than in organic milk (systematic review, PMID 39033567).
- Concentrations follow the cows' iodine intake, the season, milk yield and farming (review, PMID 29221567), and dairy gives about 13-64 % of the recommended intake by country.
- So "inland foods lack iodine" was wrong. Inland plant foods and land meat carry little; milk and eggs carry it.

## 3. Bioavailability from PubMed

| Nutrient | Finding | Source |
|---|---|---|
| Iron | absorbed 14-18 % from mixed diets, 5-12 % from vegetarian diets (people without iron stores) | Hurrell and Egli 2010, PMID 20200263 |
| Iron | the meal's effects: tea cut absorption from a hamburger meal by 64 %, coffee by 39 %; coffee 1 h before the meal had no effect, 1 h after it had the full effect | PMID 6402915 |
| Iron | green tea lowered non-heme iron from couscous by 30.5 %, black tea by 36-61 % (rats) | PMID 7832583 |
| Iron | absorption rose with vitamin C and animal tissue in the diet, fell with phosphate | PMID 11124756 |
| Iron | more meat in a varied diet raised non-heme absorption by 35 % (4.81 % to 6.47 %) | PMID 16484527 |
| Iron, zinc | whole-grain and legume porridge (about 1 g phytic acid per 100 g) gave 2-3 % iron absorption; 90 % less phytate about doubles it | PMID 12949395 |
| Phytate | about 600 mg per 100 g dry in unrefined cereals and legumes, about 100 in refined cereals, under 20 in roots and tubers | PMID 20715598 |
| Zinc | a phytate-to-zinc molar ratio above 15 lowers fractional absorption by 0.14 (to 45 % of control) | meta-analysis, PMID 24739133 |
| Zinc | protein in the meal raises absorption; fermentation, germination and phytase lower phytate and raise it | Lönnerdal 2000, PMID 10801947 |
| Niacin | the niacin of maize, wheat and rice is only about one third available after ordinary cooking (rat assays); alkali treatment releases more. Tryptophan acts as niacin at about 1/60. Maize-eating peasants of Mexico and Central America were free of pellagra, while maize regions of Europe 1750-1850 had it | Carpenter 1983, PMID 6357846 |
| Vitamin A from plants | β-carotene to retinol: 2.9 : 1 from oil, 2.1-3.3 : 1 from biofortified maize, 1.9-2.3 : 1 from African leafy vegetables, 10 : 1 from spinach | PMID 18095563, 18616269, 20412609 |
| B12 | absorbed 42 % from fish, 56-89 % from sheep meat, 61-66 % from chicken, under 9 % from eggs; absorption saturates at 1.5-2 µg per meal | Watanabe 2007, PMID 17959839 |
| B12 | more available from dairy products | PMID 19190073 |
| Calcium | from calcium oxalate (as in spinach) 10 % absorbed alone, 14 % with milk | PMID 2801588 |
| Stores | vitamin C: scurvy after about a month (Iowa study, *Scurvy*); scorbutic after 3 months without it (PMID 5411783). Folate: liver store lasted 4 months in Herbert's 1962 experiment, 19 months in a 2012 self-experiment (PMID 29946471). B12: stores last years (PMID 33341967, 39149666). Thiamin and vitamin A: no human value found yet | as named |

**What this does to the model (section 2c of `round_m83.md`):**
- **Iron:** `a_Fe` runs from 0.05 (vegetarian, phytate-rich) to 0.18 (mixed diet with much meat). It is raised by vitamin C and meat and lowered by tea and coffee drunk with meals. Hurrell and Egli note that iron status matters more than the diet. The model can let absorption rise when the store is low.
- **Zinc:** absorption falls by 0.14 once the phytate-to-zinc ratio passes 15. Phytate per good comes from the three levels above: unrefined cereals and legumes, refined cereals, roots. Leavening, fermentation and milling lower it.
- **Niacin:** maize, wheat and rice count at one third. Nixtamalized maize (alkali, a technique of the maize cultures) counts in full. Tryptophan from protein adds at 1/60.
- **Vitamin A:** animal retinol counts in full. Plant carotene counts at 1/2 to 1/3 from oil and good vegetables and 1/10 from spinach-like greens. USDA's RAE already uses 12 : 1.
- **B12:** meat and fish count at about half or more, eggs under a tenth, and dairy well.
- **Stores:** vitamin C about a month, folate months, B12 years. Thiamin and vitamin A are still open.

## 4. Why city size = the inverse of today's curve works (`plan/tools/size_curve_check.py`)

**The rule:**
- people are counted (D30);
- size is the largest `s` with `int(s^2.8) × 1,000 ≤ people`, read from a table of 64-bit integers built at load;
- the food box shows the progress in people from this size to the next.

**First test: real cities get believable sizes** (largest cities from `population_model.md` section 3):

| City | People | Size | Food box (per mille) |
|---|---|---|---|
| Uruk, 3000 BC | 40,000-45,000 | 3 | 703 |
| largest, 2000 BC | 40,000-65,000 | 3-4 | 703 |
| Babylon, 500 BC | 150,000-200,000 | 6 | 0 |
| Paris, 1328 | 200,000 | 6 | 609 |
| Rome, 1 AD | 800,000-1,000,000 | 10-11 | 880 |
| London, 1801 | 1,010,000 | 11 | 820 |
| London, 1851 | 2,290,000 | 15 | 840 |
| London, 1901 | 6,230,000 | 22 | 647 |
| New York, 1950 | 12,500,000 | 29 | 51 |
| Tokyo, 2000 | 26,400,000 | 37 | 942 |
| Jakarta, 2025 | 41,900,000 | 44 | 746 |

- The whole of history fits in sizes 1 to about 44, the range the engine, its interface and its AI are built for.
- The old problem of R1 in `population_model.md` was that an average size-7 city at 1300 BC showed 232,000 people. It goes away: size now follows people, and people grow by the evidence-based model. A city of 40,000 is size 3.

**Second test: the land workers per km² of the worked plots** (the engine works `min(size, 20)` plots besides the city plot). This is the share of people on the land, spread over those plots:

| People | Size | Plots worked | Farm share | Huge Europe (1,770 km²) | Mediterranean Standard (4,470 km²) | RFC Earth (46,000 km²) |
|---|---|---|---|---|---|---|
| 1,000 | 1 | 1 | 80 % | 0.5 | 0.2 | 0.0 |
| 10,000 | 2 | 2 | 80 % | 2.3 | 0.9 | 0.1 |
| 50,000 | 4 | 4 | 80 % | 5.6 | 2.2 | 0.2 |
| 200,000 | 6 | 6 | 80 % | 15.1 | 6.0 | 0.6 |
| 1,000,000 | 11 | 11 | 80 % | 41.1 | 16.3 | 1.6 |
| 1,000,000 | 11 | 11 | 40 % | 20.5 | 8.1 | 0.8 |
| 4,500,000 | 20 | 20 | 80 % | 101.7 | 40.3 | 3.9 |
| 4,500,000 | 20 | 20 | 40 % | 50.8 | 20.1 | 2.0 |
| 10,000,000 | 26 | 20 | 5 % | 14.1 | 5.6 | 0.5 |

- The worked plots grow as about the 0.36th power of people. So the farmers per plot rise as a city grows.
- That is the path of intensification in `tile_output.md`: the same land goes from loose grazing to dairy, arable and garden as labour rises (Clark). In 1800 England had nearly twenty acres per farm worker; coastal China and Japan fed a family from one acre.
- On Mediterranean Standard, a district of 1 million with 80 % on the land has 16 per km² of worked land. England had 9-15 per km² in 1086 and about 35 in 1300 (`population_model.md` section 4).
- On maps with large plots (RFC Earth), the plots are mostly unworked land. The tile formula `area worked = min(usable area, workers × skill × ha per worker)` (PR.F7) then gives what the labour can work, so nothing breaks.
- Above 20 worked plots, the further size goes to people who do not work plots: the city's sectors, crafts and industry (D26). That matches large cities being mostly not farmers.

**Third test: the alternative, labour units** (size = land workers ÷ the workers one plot takes; farmland share 30 %, an estimate):

| People (80 % on the land) | Tools (ha per worker) | Huge Europe | Mediterranean Standard | RFC Earth |
|---|---|---|---|---|
| 10,000 | hand tools (3) | 0.45 | 0.18 | 0.02 |
| 200,000 | hand tools (3) | 9.04 | 3.58 | 0.35 |
| 1,000,000 | hand tools (3) | 45.20 | 17.90 | 1.74 |
| 1,000,000 | horse machinery (30) | 451.98 | 178.97 | 17.39 |
| 4,500,000 | tractor (100) | 6779.66 | 2684.56 | 260.87 |

- The same city would have a size 26 times larger on Huge Europe than on RFC Earth, and 10 to 33 times larger after machinery.
- Most values pass the 20 plots a city can work.
- Labour units therefore tie size to the map and the tools, not to the people. The inverse curve does not depend on either.

**What size still does under the inverse curve, and what it no longer does:**
- **Keeps** (the engine's rules as they are): happiness and health limits, buildings that need a size, culture, worked plots, specialists, the AI's city valuation. These are game balance, already tuned for sizes 1-40.
- **No longer does:** anything per person. Food eaten, goods consumed, clothing, workers and soldiers come from the people counted (FD.F1, PR.F7, the clothing need per person). `FOOD_CONSUMPTION_PER_POPULATION` (3 per size) is replaced by eating per person in the goods pass.

**What would contradict this:** a real city whose size comes out above the engine's range, or a common map on which the worked-plot densities fall far outside the historical range. The large-plot maps fall below that range, but the tile formula absorbs it, because output is bounded by labour.

## 5. Health balance, in plain terms

**What I meant.** In the game, every city shows two health numbers:
- **Green faces (healthy):** from fresh water, forests, health resources such as Wheat or Cow, and buildings such as the Aqueduct.
- **Red faces (unhealthy):** from the city's size, flood plains and jungle, buildings such as the Forge or Factory, and power plants.

Today, if the red count is larger, the city loses that much food every turn. The population model needs a health level from 0 to 1 to scale its base burden: the term `D × (2 − H)`, which doubles the burden in the worst health.

**Proposal:**
- **A.** H = green ÷ (green + red), from the engine's two numbers.
- **B.** Leave out the red faces that come from the city's size, since density is now its own term (the unsanitized penalty, section 1). Then H = green ÷ (green + red other than size).
- **I recommend B,** so density is not counted twice.

**Question for you:** should the engine's green and red faces stay and feed the burden this way, or should the burden replace them? If it replaces them, the faces would show the burden's parts: water, sanitation, deficiencies, density.

## 6. Yearly steps inside a turn (`pop_model_sim.py turns`)

**The rule:**
- each turn runs one step for every whole year it spans, and one part step (months ÷ 12 of the yearly rate) for the rest;
- the years per turn come from the game speed (`CIV4GameSpeedInfo.xml`, `iMonthIncrement` for `iTurnsPerIncrement` turns, from 6000 BC);
- on Normal speed that is 50 years a turn for the first 40 turns, falling to 3 months at the end.

**The test:** one city with the same history by calendar year under three speeds. Food grows slowly, faster after 1700 and 1900; medicine from 1880; schooling from 1920.

| Year | Normal (700 turns, 8,190 steps) | Marathon (1,470 turns, 8,531 steps) | Blitz (215 turns, 8,050 steps) |
|---|---|---|---|
| 4000 BC | turn 40: 6,690 | turn 80: 6,690 | turn 10: 6,690 |
| 2000 BC | turn 120: 22,208 | turn 160: 22,208 | turn 30: 22,208 |
| 1 AD | turn 215: 73,698 | turn 310: 73,698 | turn 50: 73,698 |
| 1000 | turn 270: 134,274 | turn 460: 134,274 | turn 70: 134,274 |
| 1500 | turn 330: 181,218 | turn 590: 181,218 | turn 95: 181,218 |
| 1800 | turn 390: 619,071 | turn 740: 619,071 | turn 130: 619,071 |
| 1900 | turn 440: 2,211,771 | turn 839: 2,211,771 | turn 150: 2,211,771 |
| 1950 | turn 465: 6,035,009 | turn 908: 6,018,089 | turn 167 (1951): 6,153,881 |
| 2000 | turn 510: 11,686,669 | turn 1008: 11,666,290 | turn 185: 11,686,669 |
| 2050 | turn 590: 17,199,872 | turn 1166: 17,178,722 | turn 215: 17,192,185 |

**What it shows:**
- **The city is the same at the same calendar year, whatever the speed.** It is identical to the person up to 1900, where all turns are whole years.
- After 1900 the turns are months long, and the part steps differ by at most 0.3 %. Blitz's 1950 row is read at its turn end in 1951.
- **Cost:** about 8,000 steps per city over a whole game, at most 200 in one turn (Blitz's 200-year turns). Each step is a few 64-bit multiplications.
- **Speed still matters where it should:** a faster speed has fewer turns per year, so fewer decisions per year. The people follow the calendar.

## 7. Open

- Whether the engine's health faces stay and feed the burden, or are replaced by it (section 5).
- Thiamin and vitamin A stores; phytate per good beyond the three levels.
- Whale as food: which cultures count (for example by a whaling tech or civic and a Whale resource within reach). A proposal follows with the goods list.
