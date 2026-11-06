# Which resources can be food (R21, M67)

All 80 resource records of the mod were read on the GitLab branch `claude/settlement-economy` at `d2a8f756`
(`Assets/XML/Terrain/CIV4BonusInfos.xml`, plus the bonus files of the Guilds and Corporations modules). This file
holds those records (section 1), nutrition values (section 2), what history says about each candidate (section 3),
a reading of which resources can be food and in what role (section 4), and options (section 5). The plan's present
classing is in `research/economy/plan/proposals.json` (goods). Nothing is decided.

## 1. The resources as the XML defines them

Each entry gives its yield on the plot (food, production, commerce), its health and happiness, the tech that reveals
it and the tech that lets it be traded.

**15 resources give +1 food:**

| Resource | Class | Reveal / trade tech | Health | Terrain, features |
|---|---|---|---:|---|
| Wheat, Corn, Rice, Potato | GRAIN | none / Agriculture | +1 | grassland, plains, marsh; Rice jungle and swamp, Potato swamp |
| Cow, Sheep, Pig | LIVESTOCK | Hunting / Animal Husbandry | +1 | grassland, plains; Pig jungle |
| Deer | GENERAL | Hunting / Hunting | +1 | tundra, marsh, forest, swamp |
| Fish, Clam, Crab, Shrimp | SEAFOOD | none or Fishing / none | +1 | coast, ocean |
| Whale | SEAFOOD | Sailing / none | 0 | ocean (storm) |
| Banana | GENERAL | Naturopathy / Naturopathy | +1 | jungle |
| Lemon, Apple | GENERAL | Naturopathy / Naturopathy, Bronze Working | +1 | jungle, forest |
| Sugar | GENERAL | none / Naturopathy | 0 (+1 happiness) | jungle |

- **Dairy** (LIVESTOCK, +1 health) is not placed on the map (`iPlacementOrder` -1). Pastures make it (LQ.F8 and
  LQ.F11 on the branch).

**Resources a plot does not yield food from, but that are a plant or an animal:**

| Resource | Yield | Health / happiness | Note |
|---|---|---|---|
| Olives | +1 commerce | 0 / +1 | trade at Bronze Working |
| Wine | +1 commerce | 0 / +1 | plains |
| Alcohol | made, not placed | 0 / +1 | Fermentation |
| Salt | +1 commerce | +1 / 0 | plains, desert; Masonry |
| Spices | +1 commerce | 0 / +1 | jungle, forest |
| Tea, Coffee | +1 commerce | 0 / +1 | grassland, jungle, forest |
| Cotton | +1 production, +1 commerce | 0 / +1 | Agriculture |
| Cannabis | +1 commerce | 0 / +1 | Mysticism |
| Horse | +1 production | 0 / 0 | Animal Husbandry |
| Fur | +1 commerce | 0 / 0 | tundra, snow, forest |
| Ivory | +1 production | 0 / 0 | plains, jungle |
| Pearls | +1 commerce | 0 / +1 | coast |
| Silk, Dye, Incense, Tobacco, Rubber | commerce | 0 / +1 mostly | |

**Made goods that touch food:**
- Fertilizers: +2 health, Pesticides.
- Chemicals: -1 health.
- Biofuel: Biofuels.

Wool, Leather and Timber have no plot yield.

**Not food in any form:** the metals and ores (Copper, Iron, Lead, Gold, Silver, Bauxite, Aluminum, Steel), Stone,
Marble and Obsidian, the fuels (Coal, Oil, Diesel, Methane, Uranium), Gems, Bernstein (amber), Glass, Cement,
Ammo, the rubbers, Semiconductors, the future goods, Guild paper, Drama, Music and Movies, and the Ancient Temple
and Thermal Vent markers.

**The plan's present classing (`proposals.json`):**
- staple: Wheat, Rice, Corn, Potato, Fish;
- variety: Cow, Pig, Sheep, Deer, Clam, Crab, Shrimp, Banana, Lemon, Apple, Olives, Salt, Dairy;
- comforts: Sugar, Wine, Alcohol, Tea, Coffee, Spices;
- fuel: Whale (barrels);
- military supply: Horse.

## 2. Nutrition per 100 g (FAO, *Food Balance Sheets: a handbook*, 2001, Annex I)

These are per 100 g of retail weight, as bought, so shells and bones count. That is why molluscs show 15 kcal and
demersal fish 42.

| Item (FAO name) | kcal | Protein g | Fat g |
|---|---:|---:|---:|
| Wheat | 334 | 12.2 | 2.3 |
| Rice, milled (paddy) | 360 (280) | 6.7 (6.0) | 0.7 (1.4) |
| Maize | 356 | 9.5 | 4.3 |
| Potatoes | 67 | 1.6 | 0.1 |
| Bananas (plantains) | 60 (75) | 0.7 (0.8) | 0.3 |
| Apples | 48 | 0.1 | 0.3 |
| Lemons and limes | 15 | 0.6 | 0.2 |
| Olives | 175 | 1.3 | 17.5 |
| Olive oil, cottonseed oil, hempseed oil | 884 | 0 | 100 |
| Sugar, centrifugal raw (sugar cane) | 373 (30) | 0 | 0 |
| Honey | 298 | 0.4 | 0 |
| Beef, boneless | 150 | 18.5 | 7.9 |
| Pigmeat | 326 | 11.0 | 31.0 |
| Mutton and lamb (goat meat) | 263 (123) | 13.5 (14.0) | 22.8 (7.0) |
| Horsemeat | 85 | 15.5 | 2.0 |
| Game meat | 104 | 18.0 | 3.0 |
| Cow milk, whole fresh | 61 | 3.3 | 3.3 |
| Cheese, whole cow milk | 387 | 25.0 | 31.0 |
| Butter | 717 | 0.9 | 81.1 |
| Pelagic, demersal, freshwater fish | 86, 42, 69 | 12.6, 8.3, 10.9 | 3.6, 0.8, 2.5 |
| Crustaceans; molluscs (fresh) | 47; 15 | 9.3; 2.3 | 0.5; 0.2 |
| Aquatic mammals meat (whale) | 136 | 21.0 | 5.0 |
| Wine; beer (barley) | 68; 49 | 0; 0.5 | 0 |
| Coffee green; tea (dry) | 47; 40 | 6.7; 10.0 | 0 |
| Pepper; spices nes | 276; 337 | 10.7; 11.3 | 2.7; 15.5 |
| Cottonseed | 253 | 17.3 | 17.9 |
| Offals of cattle | 105 | 18.4 | 2.5 |
| Lard, tallow | 902, 884 | 0 | 100 |

Salt and the hempseed itself are not in the annex.

## 3. What history says about the candidates

- **Ale and beer:**
  - Grain gave up to 80 % of a harvest worker's calories in the early 14th century, 65-70 % for the lay nobility
    (*Food in Medieval England*, Oxford).
  - Dyer (1988) found that harvest workers' bread fell and their meat and ale rose over two centuries.
  - Institutions gave a gallon of ale a day per monk at Westminster.
  - An estimate from malt output puts an ordinary peasant at a third of a pint a day (contested).
- **Olive oil.** The average Roman ate about 20 L a year (up to 50 in some sources). That is about 12 % of calories
  and about 80 % of dietary fat (Wikipedia, Roman agriculture; the Herculaneum isotope study). Grain gave 70-80 % of
  calories.
- **Sugar** (Mintz). British use per head was about 4 lb a year in 1700-09, about 18 lb in 1800-09 and over 90 lb in
  1901. By 1900 sugar is said to have given nearly a fifth of English calories (from a summary; not checked against
  Mintz).
- **Salt.** Salted herring and cod were staples of northern Europe and kept famine away. Ordinary people ate the
  preserved fish while elites kept to fresh. The often-quoted 40-70 g a day per European measures salt used,
  including preserving, not salt eaten.
- **Citrus.** Lind's trial was in 1747 and his treatise in 1753. In 1795 the Royal Navy ordered citrus juice daily
  for every crew. Cheaper West Indian limes replaced lemons in the mid-19th century.
- **Horses and the steppe.** Dairy and meat from sheep, goats, cattle, camels and yaks dominated the Mongol diet, and
  herders kept animals alive for their milk. Horse meat was for feasts; mutton was everyday meat. Fermented mare's
  milk (kumis) was a staple drink.
- **Whale.** Aquatic mammal meat has 136 kcal, 21 g protein and 5 g fat per 100 g (FAO). The mod treats whale only as
  oil (fuel).
- **Cottonseed.** 253 kcal and 17.3 g protein per 100 g, and its oil 884 kcal. It yields oil and animal feed.

## 4. Reading: which resources can be food, and how

Each judgment cites the facts above. "Food role" means what it adds to a diet.

| Role | Resources | Basis |
|---|---|---|
| **Staple energy** (grain and roots) | Wheat, Rice, Corn, Potato; Banana in the tropics | 334-360 kcal per 100 g dry grain; potato 67 and banana 60 fresh, but high yields per hectare (`tile_output.md`) |
| **Animal protein** (D27 bonus) | Cow, Pig, Sheep, Deer, Dairy, Fish, Clam, Crab, Shrimp; also **Whale** and **Horse** | 15-21 g protein per 100 g of meat, cheese 25; whale meat 21 g; horse meat 15.5 g and mare's milk on the steppe |
| **Fat and oil** | **Olives** (now commerce), Pig (lard), Dairy (butter), Whale (blubber); later **Cotton** (cottonseed oil) | oils 884 kcal per 100 g; Roman oil about 12 % of calories and 80 % of fat |
| **Sugar** | **Sugar** (now a comfort) | 373 kcal per 100 g; nearly a fifth of English calories by 1900 (if Mintz's summary holds); a comfort before the 18th century, food energy after |
| **Fruit and vitamins** | Apple, Lemon, Banana | low energy (lemon 15 kcal); citrus prevents scurvy (Lind, 1795 Navy order) |
| **Drink with calories** | **Wine**, **Alcohol** (now comforts) | wine 68 kcal per 100 g, beer 49; ale a large share of workers' calories in the late Middle Ages |
| **Preserving, not eating** | **Salt** | no calories; preserved herring and cod staved off famine. It belongs with keeping food (D27 shelf life), not with variety |
| **Seasoning and stimulants** (no food role at the amounts eaten) | Spices, Tea, Coffee, Tobacco, Cannabis | the FAO energy is per dry leaf or bean, eaten in grams |
| **Inputs to food, not food** | Fertilizers (yield), Chemicals (preserving, pesticides), Horse (draught, `tile_output.md`) | |
| **Marginal food** | Fur (trapped animals were eaten), Ivory (elephant meat), Pearls (oyster meat) | the main product is not food; their meat could be a small by-product |

**What changes against the present classing:**
1. **Whale** is food as well as oil: meat and blubber.
2. **Horse** can give meat and milk, the steppe pattern, beside draught and mounts.
3. **Olives** give oil, a food fat, not only commerce.
4. **Sugar**, **Wine** and **Alcohol** carry calories. They can count as food energy as well as comforts, sugar more so
   from the 18th century.
5. **Salt** moves from variety to preserving: it lengthens the shelf life of meat and fish.
6. **Lemon** has a role beyond variety: scurvy at sea.
7. **Cotton** later gives an oil, and feed for animals.
8. **Fish** is protein first. It is classed staple now; the D27 nutrition rule already treats it as protein.

## 5. Options for counting food (for the decision; few variables, as M65 asked)

- **(a) One number:** every food good counts in kcal, as the "food" F of the population formula (`F / s`).
  Protein and variety are left out.
- **(b) Two numbers:** kcal for F, and protein for D27's strength bonus. The per-100 g values above set both per
  good.
- **(c) Two numbers and the number of food groups eaten:** variety as how many of the roles above a city has
  (staple, protein, fat, sugar, fruit, drink), not as a list of goods.

All three take their values per good from section 2, so no new variable is invented per good.

## Open

- Edible fraction and processing losses per good (retail weight versus what is eaten, milling, butchering).
- How much meat, milk, oil or blubber each animal or plant resource gives per head or per hectare (`tile_output.md`
  section 4).
- Feed: Corn, Potato and cottonseed fed to animals compete with people (the conversion losses).
- Seasonal and keeping values (D27): which forms keep, with Salt as the preserver.
