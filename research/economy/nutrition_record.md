# Nutrition and food: the clean record (R56, M104; PubMed sources R57, M105)

This file replaces every earlier note on nutrition and food groups. It holds only two kinds of content:

- **Section 1** is your inputs, quoted or condensed, with the prompt they come from.
- **Section 2** is facts read in a PubMed record during this work; facts still resting on an institution are listed apart in 2g.

Section 3 lists known faults in the data files, section 4 the open gaps, and section 5 what was removed.

Earlier notes, models and tools are in `archive/nutrition/` (see its README). They are history, not a basis.

## 1. Your inputs

### 1a. What food is for

| Prompt | Input |
|---|---|
| M57 | Meat, dairy and fish provide the most nutrition and the most actual contribution to satiety. High-protein foods also give strength bonuses to units other than siege equipment, vehicles, robots and other machines. Cereal products, dried fruit, fermented dairy and cured meat and fish rank highest for shelf life and add most to the food storage. |
| M69 | Animal foods carry calories too. High-protein foods give the highest satiety. |
| M71 | Liquid milk is as valuable as fish or meat: extraordinary hydration, highly bioavailable protein and fat, and lactose as a stable carbohydrate. Drinks are measured as quantities per day, like drinking water or juice. |
| M75 | Population follows nutrient quality and quantity. Good food raises fertility, productivity, and commercial, scientific and cultural output. It is more than protein boosting strength by a margin. Calories, satiety and health are separate measures. |
| M84, M94 | Liver has plenty of vitamin A. Milk is an inland food and gives iodine. Animal foods provide the most bioavailable nutrition. |
| M83 | Seafood and milk provide iodine. Electrolytes are as important for life as macronutrients. The game needs one efficient model of deficiencies that covers all food sources. |
| M82 | Tea, lemons, apples, bananas and all fruits, wine grapes included, help against scurvy. Scurvy follows a plain, deficient diet. |
| M83 | Many teas carry real nutritional value against deficiency diseases. |
| M83, M85 | Wine is a luxury good; the vineyard's good counts as a kind of food. Whale: if it is available, it is possible food. |
| M91 | Fish is the whole animal as eaten historically: its fat, cod liver and roe, not lean fillet. |
| M84 | Fat is not bad in itself. Its value depends on the animals' diet, freshness, the vitamin E of unsaturated oils and the omega-3:6 ratio. This is context, not something to map. |
| M85 | Water-soluble and fat-soluble vitamins are the usual distinction for stores. |
| M83 | Fast food and stones were a general comment on how health works. |

### 1b. Needs and the body

| Prompt | Input |
|---|---|
| M85 | More calories, and stimulants such as caffeine, make people more active. A manual labourer of the early 1900s burned 3,000-4,000 kcal. |
| M102, M103 | Needs are not fixed. Hydration needs scale with labour. |
| M85, M88 | What a person can eat differs by food group: very few people can eat a kilogram of cheese a day; many can eat a lot of pasta; sugar is easy to eat; about three litres of milk a day; more than a pound of ground beef gives heartburn; a whole watermelon can be eaten. Appetite is set by what people can physically eat. |
| M86, M88 | The watermelon stands for fruit in general. A limit on total food weight would overcomplicate it. |
| M88, M93 | Fat from one good is a heuristic for the usual maximum of one good: first 100 g, raised to 250 g. |
| M92 | Nobody eats kilograms of lemons; lemons need an upper limit. |
| M91, M88 | 3 L is milk's limit. It is one part of an equation for a person's hydration. People drink 3 L of water or more. |
| M101 | The hydration index is how much hydration a drink gives compared with the same volume of water (milk 1.5). |
| M92, M93 | Fullness (satiety) is the gauge of being fed; calories are part of the equation. Grains and tubers kept people fed; nutrition makes them strong and healthy. The baseline is satiety being met; ideally people get all the calories they need from the best foods. |
| M84 | Food beyond what is eaten is surplus and goes to long-term storage. |
| M101 | Body reserves are part of the city growth formula. There are no seasons (turns of up to fifty years). The model applies to a city's population as a whole. |

### 1c. How people choose

| Prompt | Input |
|---|---|
| M88 | People prefer the goods of highest quality, those with the most nutrition, health and satiety. After that limit they eat other things: "steak and potatoes, then dessert". |
| M89, M90 | Fruit and many drinks matter for well-being; fruit gives satiety too. These are a different set of priorities, not a top tier (M91). |
| M96, M102 | Nutrition and well-being are two separate variables and two separate sorted lists. Nutrition comes first. |
| M91, M102 | Well-being covers how light a person feels after eating, the dopamine hit (reward) and health effects; repetition too. Sugar adds to well-being; a rich city eats sugar as today or as in 1900s Britain. |
| M102 | People draw on the higher-quality stocks. Prices adjust things afterwards and are not part of basic human nutrition. |
| M91 | In a rich city, surplus milk is partly turned into dairy products, and bread is eaten to some extent. |
| M101, M102 | Harm terms for alcohol and tobacco: harm is a consequence, not a motive. |
| M102 | The mean adequacy ratio is a good measure of nutrition. A city can only eat what it holds, economics aside. |

### 1d. Buildings, health and markets

| Prompt | Input |
|---|---|
| M88 | The Commercial Center and Commodity Market stand for modern logistics, just-in-time delivery, refrigeration and commoditized foods, nutraceuticals and medicines. They keep their health and cut spoilage (fresh by half, kept by a quarter, M91). |
| M88 | The Essentials tiers are stages of settlement development; actual sanitation comes only with the last tier. Water supply levels add sanitation faces (M88) and are part of the general health equation (M91). |
| M86 | Unhealthy faces are the most intuitive sign of missing infrastructure; the hover gains lines for water, sanitation and density, missing nutrients and war. |

## 2. Verified facts

Every fact cites a PubMed record (PMID) whose abstract or full text was read. Facts that still rest only on an institution's report are listed apart in section 2g, until a PubMed source replaces them (R57, M105).

### 2a. Energy

- **Energy need = basal rate × physical activity level (PAL).** PAL is total expenditure measured by doubly labelled water divided by basal rate (Black et al. 1996, 574 measurements, PMID 8641250).
- **Basal rate** is predicted from weight, or weight and height, by sex and age (Schofield 1985, PMID 4044297). Subjects from developing countries had lower rates per kg than European or North American subjects. The coefficients are not in the abstract (section 2g).
- **Range of PAL:**
  - the limits of daily expenditure are about 1.2 × and 4.5 × basal rate (non-ambulant people and elite endurance athletes; Black 1996, PMID 8641250);
  - PAL values of active people tend to be higher than assumed in the 1985 recommendations (same source);
  - the general population has an upper PAL of 2.2-2.5; endurance athletes keep energy balance at 4.0-5.0 (Westerterp 2001, PMID 11581332);
  - over events of 0.5 to 250+ days, sustained expenditure falls with duration and levels off below 3 × basal rate; food intake limits supply at about 2.5 × basal rate, beyond which body stores are drawn down (Thurber et al. 2019, PMID 31183404).
- **Hunter-gatherers:** Hadza foragers had a higher PAL than Westerners, but the same daily expenditure after adjusting for body size (Pontzer et al. 2012, PMID 22848382).
- **Caffeine** (Dulloo et al. 1989, PMID 2912010):
  - 100 mg raised the resting rate by 3-4 % for 150 minutes;
  - 100 mg every 2 h over 12 h raised expenditure by 8-11 %;
  - the net effect was +150 kcal a day in lean adults.
- **Caffeine and effort:** caffeine raises energy and effortful behaviour (PMID 20164571).

### 2b. Needs

**Protein:** a meta-analysis of nitrogen balance in 235 adults gave an average requirement of 105 mg N/kg a day (0.65 g good-quality protein/kg) and a 97.5th percentile of 132 mg N/kg (0.83 g/kg). Climate, age, sex and protein source had no significant effect (Rand et al. 2003, PMID 12499330).

**Calcium:** neutral balance in 155 adults was reached at 741 mg a day (95 % prediction interval 507-1,035), or 9.4 mg/kg, or 0.28 mg per kcal; age and sex had no effect (Hunt and Johnson 2007, PMID 17921384).

**Iodine:** an optimal adult intake is 150-250 µg a day; about 50 % of Europe remains mildly deficient (Zimmermann 2009, PMID 19460960).

**Vitamin C:**
- seven volunteers on under 5 mg a day, then seven doses from 30 to 2,500 mg: plasma level against dose is sigmoid, steepest between 30 and 100 mg a day; white cells saturate at 100 mg, plasma at 1,000 mg; no vitamin C appears in urine below 100 mg (Levine et al. 1996, PMID 8623000);
- volunteers deprived for 3 months developed signs of scurvy (Abboud et al. 1970, PMID 5411783; the depletion studies are Hodges et al. 1969 and 1971, PMID 4977512 and 5090631, which have no abstract on PubMed).

**Water, rising with labour and heat:**
- a daily total water intake of 3.7 L for men and 2.7 L for women meets the needs of most people; strenuous exercise and heat stress can greatly increase it (Sawka et al. 2005, PMID 16028570);
- **water turnover equation** (Yamada et al. 2022, *Science*, 5,604 people in 23 countries, PMID 36423296; equation from the full text, PMC9764345):

  WT (ml/d) = 1076 PAL + 14.34 BW + 374.9 Sex + 5.823 Hum + 1070 Ath + 104.6 HDI + 0.4726 Alt − 0.3529 Age² + 24.78 Age + 1.865 T² − 19.66 T − 713.1

  | Symbol | Meaning | Unit |
  |---|---|---|
  | WT | water turnover: all water in (drink, food, metabolic water) and out | ml per day |
  | PAL | physical activity level | ratio |
  | BW | body weight | kg |
  | Sex | 1 male, 0 female | — |
  | Hum | relative humidity | % |
  | Ath | 1 athlete, 0 not | — |
  | HDI | human development index group: 0 high, 1 middle, 2 low | — |
  | Alt | altitude | m |
  | Age | age | years |
  | T | air temperature | °C |

  It explains 47.1 % of the variation. One unit more PAL adds about 1,000 ml a day; 30 °C adds about 1,000 ml over the 0-10 °C minimum. Hunter-gatherers, subsistence farmers and manual labourers had higher size-adjusted turnover.
- wildland firefighters in arduous work had a water turnover of 6.7 L a day, against 3.8 L in active students, and lost body water over 5 days (Ruby et al. 2003, PMID 14523317).

**Sodium lost in sweat:**
- men working in heat: predicted losses of 4.8-6 g sodium per work shift, equal to 10-15 g salt; more in unacclimatised men (Bates and Miller 2008, PMID 18226265);
- 1,303 athletes: sweat rates 0.83-1.51 L per hour and sodium losses 27-56 mmol (0.6-1.3 g) per hour by sport (Barnes et al. 2019, PMID 31230518).

**Vitamin stores:**
- fat-soluble vitamins are stored in fat and liver; water-soluble ones wash out (PMID 30860745);
- the liver's folate store lasted 4 months in one experiment and 19 months in another (PMID 29946471);
- B12 stores last years (PMID 33341967, 39149666).

### 2c. Absorption (bioavailability)

- **Iron:**
  - absorbed 14-18 % from mixed diets and 5-12 % from vegetarian diets (Hurrell and Egli 2010, PMID 20200263);
  - tea cut absorption from a meal by 64 % and coffee by 39 % (PMID 6402915);
  - vitamin C and animal tissue raise absorption (PMID 11124756).
- **Zinc and phytate:**
  - phytate is about 600 mg per 100 g dry in unrefined cereals and legumes, about 100 in refined cereals and under 20 in roots and tubers (PMID 20715598);
  - a phytate-to-zinc molar ratio above 15 lowers fractional zinc absorption by 0.14 (PMID 24739133);
  - protein raises zinc absorption; fermentation and germination lower phytate (Lönnerdal 2000, PMID 10801947).
- **Niacin:**
  - the niacin of maize, wheat and rice is about one third available; alkali treatment releases more;
  - tryptophan acts as niacin at about 1/60;
  - maize-eating Mexico and Central America were free of pellagra (Carpenter 1983, PMID 6357846).
- **Vitamin A from plants:** 2-3 µg β-carotene give 1 µg retinol from oil or maize, 10 µg from spinach (PMID 18095563, 18616269, 20412609).
- **B12:** absorbed 42 % from fish, 56-89 % from mutton and 61-66 % from chicken, but under 9 % from eggs; absorption saturates at 1.5-2 µg per meal (Watanabe 2007, PMID 17959839). B12 from dairy is more bioavailable (PMID 19190073).
- **Calcium** from calcium oxalate is 10 % absorbed alone and 14 % with milk (PMID 2801588).

### 2d. What foods contain

- **Composition records:**
  - USDA FoodData Central SR Legacy (2018-04): energy, protein, fat, water, sugars, alcohol, vitamins and minerals per 100 g;
  - Japanese food tables (MEXT, 8th edition, 2023 supplement): iodine, tea infusions, whale;
  - both are held in `data/nutrient_profiles.json`.
- **Selected values:**
  - beef liver 4,968 µg vitamin A RAE and 59 µg B12 per 100 g (USDA 169451);
  - Pacific herring 195 kcal, 16.4 g protein and 13.9 g fat per 100 g (USDA 173669);
  - cod liver oil 30,000 µg vitamin A per 100 g (USDA 173577);
  - MEXT cod 350 µg iodine per 100 g.
- **Small fish eaten whole** (with bone, head and eyes) are nutrient-dense animal food, rich in haem iron, zinc and especially calcium, with preformed vitamin A (Kongsbak et al. 2008, PMID 17925053).
- **Iodine in milk:**
  - 5.5-49.9 µg per 100 g across 34 countries, median 17.3, higher in winter (PMID 39033567);
  - concentration follows the cows' iodine intake;
  - dairy gives 13-64 % of recommended intake (PMID 29221567).
- **Vitamin C in green tea** (MEXT): infusions of gyokuro 19 mg, sencha 6 mg and bancha 3 mg per 100 g; matcha powder 60 mg. Black tea infusion has none.
- **Tea and coffee:**

| Measure | Value | Source |
|---|---|---|
| caffeine in tea leaves | 16.3-19.3 mg/g | Boros 2016, PMID 27019564 |
| caffeine per serving of brewed tea | 14-61 mg | Chin 2008, PMID 19007524 |
| caffeine per dose of coffee | 58-259 mg | McCusker 2003, PMID 14607010 |
| sencha brewing | 10 g in 430 ml, 20 mg caffeine per 100 g of infusion | MEXT |
| black tea brewing | 5 g in 360 ml, 30 mg per 100 g of infusion | MEXT |
| coffee brewing | 10 g in 150 ml, 60 mg per 100 g of infusion | MEXT |

- **Serving weights:** one whole watermelon of 15 × 7.5 in weighs 4,518 g (USDA portion record).

### 2e. Satiety, appetite, reward

- **Holt et al. 1995** (PMID 7498104):
  - isoenergetic 240 kcal servings of 38 foods, white bread = 100;
  - boiled potatoes 323 (highest), croissant 47 (lowest);
  - the full list of 38 foods is in the paper's table.
  - Satiety rose with serving weight (r 0.66), water (0.64), fibre (0.46) and protein (0.37), and fell with fat (−0.43) and palatability (−0.64).
  - Holt measured satiety over 2 hours.
- **Fixed weight:** people tend to eat a consistent weight of food (Rolls 2009, PMID 19303887).
- **Liquids:** liquid calories satiate less, with incomplete compensation (PMID 14649371, 36771409).
- **Protein limits** (Bilsborough and Mann 2006, PMID 16779921):
  - the gut absorbs 1.3-10 g of amino acids an hour;
  - protein above 35 % of energy is dangerous;
  - about 25 % (2-2.5 g/kg) is a suggested maximum;
  - the theoretical safe maximum is 285-365 g a day for 80 kg.
- **Reward:**
  - fat and carbohydrate together are rewarded more than either alone (PMID 29909968);
  - a palatable fat-sugar milkshake released striatal dopamine (PMID 37375579);
  - alcohol releases striatal dopamine at low doses (meta-analysis, PMID 39729041).
- **Lightness:**
  - a high-fat, low-carbohydrate meal left people sleepier and more tired 2-3 h later than a low-fat, high-carbohydrate meal (Wells 1997, PMID 9145937);
  - a calorie-rich meal brings postprandial fatigue (PMID 29705519).
- **Sensory-specific satiety** is a short-term satiety signal (PMID 1752065).
- **Protein leverage:** protein is about 15 % of dietary energy and nearly constant across populations; the hypothesis is that people eat until a protein target is met, so a diet diluted in protein raises total energy intake (Simpson and Raubenheimer 2005, PMID 15836464; evidence reviewed in PMID 37820518).
- **Milk and later intake:** 34 boys given low-fat milk with breakfast ate 1,010 kcal at a buffet lunch 5 h later, against 1,059 after apple juice and 1,236 after water, and reported more satiety (Mehrabani et al. 2016, PMID 26099369).
- **Which foods draw addictive-like eating:** among 35 foods, processing was a large positive predictor; fat and glycemic load were large positive predictors in a separate model (Schulte et al. 2015, PMID 25692302). This ranks attributes, not a dopamine value per food.

### 2f. Harm

- **Alcohol:** across 195 countries the level of consumption that minimised harm across health outcomes was zero (95 % UI 0.0-0.8) standard drinks a week; a standard drink is 10 g ethanol (GBD 2016 Alcohol Collaborators 2018, PMID 30146330).
- **Tobacco:**
  - 1-4 cigarettes a day against never smoking: ischaemic heart disease death RR 2.74 in men and 2.94 in women; death from any cause RR 1.57 and 1.47 (Bjartveit and Tverdal 2005, PMID 16183982);
  - lifelong consistent smokers of under 1 cigarette a day: all-cause mortality HR 1.64; 1-10 a day: HR 1.87 (Inoue-Choi et al. 2017, PMID 27918784).

### 2g. Still resting on institutions only (to replace with PubMed sources)

| Fact | Institutional source | PubMed status |
|---|---|---|
| Basal rate coefficients, men 18-30: 15.057 × weight + 692.2 kcal; women 14.818 × weight + 486.6 | FAO/WHO/UNU 2004 tabulation of Schofield | Schofield 1985 (PMID 4044297) abstract has no coefficients |
| Thiamin 0.072 mg per MJ; niacin 1.3 mg NE per MJ | EFSA 2017 | not found in PubMed searches |
| Vitamin A 570 µg RE, folate 250 µg DFE, riboflavin 1.3 mg, B6 1.5 mg, B12 4 µg, magnesium 350 mg, selenium 70 µg, potassium 3,500 mg | EFSA 2017 | not found (potassium: PMID 32500831 gives a blood-pressure dose response, not a need) |
| Iron 6 mg at 16 % absorption; zinc 7.5-12.7 mg by phytate intake | EFSA 2017 | absorption facts in section 2c are PubMed; the needs are not |
| Sodium need without sweating, 600 mg | Japanese DRI 2025 | not found |
| Scurvy prevented at about 10 mg vitamin C a day | earlier read on Wikipedia | Hodges 1971 (PMID 5090631) has no abstract; not verified |
| Reference weights 68.1 kg men, 58.5 kg women | EFSA 2017 | not needed once a weight is chosen |

### 2h. Measures

- **Mean adequacy ratio:** the average over nutrients of intake ÷ requirement, each capped at 1. A standard measure of diet adequacy, approved by you (M102).
- **Hydration index:** the hydration a drink gives relative to the same volume of water (M101). Measured as water retained 2 h after 1 L, relative to still water, in 72 men: full-fat milk 1.50, skimmed milk 1.58, oral rehydration solution 1.54; cola, tea, coffee, lager, orange juice and sports drink did not differ from water (Maughan et al. 2016, PMID 26702122; also PMID 42884730).

## 3. Known faults in the data files (to fix before any model uses them)

| File | Fault |
|---|---|
| `nutrition.json` and `nutrient_profiles.json` | **Two bases.** Energy, protein and fat come from FAO "as bought" records (beef 150 kcal per 100 g); vitamins and minerals come from USDA records of a different form (beef carcass 291 kcal). A model mixing them mismatches energy and nutrients. One record per good, all values from the same food form, is needed. |
| `nutrient_profiles.json` | **Niacin.** USDA gives preformed niacin in mg; the need is in niacin equivalents, which include tryptophan / 60 (section 2c). Tryptophan (USDA nutrient 1210) must be added. |
| `nutrient_needs.json` | **Thiamin and niacin** are converted at a fixed 2,600 kcal. They are set per MJ (section 2g), so they must follow the actual energy turnover. |
| `nutrient_needs.json` | **Sodium** is fixed. Sweat losses of 4.8-6 g per shift in heat (section 2b) must be added with labour and heat. |
| `nutrient_needs.json` | **Water** is a fixed 2,250 ml. It must rise with labour and heat (M103); the Yamada equation (section 2b) gives about 1,000 ml per unit of PAL and per 30 °C. |
| `nutrient_needs.json` | **Vitamin C** uses EFSA's 90 mg. Levine (section 2b) shows the steep part of the curve at 30-100 mg and cell saturation at 100 mg; the dose that prevents scurvy is open (section 2g). |
| Fish | The "whole fish" shares used earlier (50 % herring, 45 % cod, 5 % liver) were unsourced. The starving fishing village came from these shares and from taking the low end of the protein range. Both are removed. |

## 4. Open: what has no solid record yet

- **PubMed sources for the needs in section 2g.**
- **A per-food measure of reward or dopamine:** no per-food values exist in the sources read. Section 2e gives the direction (fat with sugar, processing, glycemic load, alcohol, caffeine), not values per good.
- **Lightness per food:** only the direction is known (fat increases sleepiness; Holt's water and weight correlations).
- **Fullness per food:** only Holt's 38 foods are measured. A fitted formula reached R² 0.46 and is not a verified record.
- **Daily ceilings per food:** the values are yours (milk, fat per good, lemons, fruit as a watermelon). The liver's protein capacity is from Bilsborough and Mann; others have no source.
- **Whole-animal and catch compositions:** liver and roe shares for fish, cattle and pigs. A search for cod liver weight returned nothing.
- **Harm per amount:** section 2f gives the minimum (zero) and the risks at low doses; the full dose-response curves are not yet extracted.
- **Prices:** to be established in the goods economy.

## 5. Removed

Everything not in sections 1-4 is removed from the working basis. In particular:
- the food model versions 1-4, their worked examples and the assessment;
- my well-being and satisfaction formulas and their weights;
- the fitted satiety formula as a basis;
- the fish and liver shares;
- the starvation result for fish;
- the fixed water and vitamin needs;
- the protein ceiling choices;
- the "even use of supply" rule.
