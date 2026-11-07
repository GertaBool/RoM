# Nutrition and food: the clean record (R56, M104; PubMed sources R57-R59, M105-M107)

This file replaces every earlier note on nutrition and food groups. It holds only two kinds of content:

- **Section 1** is your inputs, quoted or condensed, with the prompt they come from.
- **Section 2** is facts read in a PubMed record during this work.

Section 3 lists known faults in the data files, section 4 the limits of the record, and section 5 what was removed.

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
| M108 | Calcium is important and must not be ignored. It comes from drinking water and food. The most effective sources are dairy, animal bones and cooked small fish such as sardines. |
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

Every fact cites a primary study, by PMID where PubMed indexes it, whose abstract or full text was read (R57-R59, M105-M107). Where only the abstract was reachable through another index, or the record is a research station's measurement note, the entry says so. No fact rests on an institution's recommendation.

### 2a. Energy

- **Energy need = basal rate × physical activity level (PAL).** PAL is total expenditure measured by doubly labelled water divided by basal rate (Black et al. 1996, 574 measurements, PMID 8641250).
- **Resting rate** (Mifflin et al. 1990, 498 adults aged 19-78, measured by indirect calorimetry, R² 0.71; PMID 2305711):

  REE (kcal/d) = 9.99 W + 6.25 H − 4.92 A + 166 S − 161

  | Symbol | Meaning | Unit |
  |---|---|---|
  | REE | resting energy expenditure | kcal per day |
  | W | body weight | kg |
  | H | height | cm |
  | A | age | years |
  | S | 1 male, 0 female | — |

  Weight alone gives REE = 15.1 W + 371 (R² 0.56); fat-free mass alone gives 19.7 FFM + 413 (R² 0.64). The Harris-Benedict equations of 1919 overestimated measured REE by 5 %.
- Earlier basal-rate equations by age band come from Schofield 1985 (PMID 4044297). They overestimate basal rate in many communities; 47 % of their subjects were Italian (Henry 2005, PMID 16277825). Subjects from developing countries had lower rates per kg (Schofield).
- **Range of PAL:**
  - the limits of daily expenditure are about 1.2 × and 4.5 × basal rate (non-ambulant people and elite endurance athletes; Black 1996, PMID 8641250);
  - PAL values of active people tend to be higher than assumed in the 1985 recommendations (same source);
  - the general population has an upper PAL of 2.2-2.5; endurance athletes keep energy balance at 4.0-5.0 (Westerterp 2001, PMID 11581332);
  - over events of 0.5 to 250+ days, sustained expenditure falls with duration and levels off below 3 × basal rate; food intake limits supply at about 2.5 × basal rate, beyond which body stores are drawn down (Thurber et al. 2019, PMID 31183404).
- **Farmers and labourers:** Rwandan farmers had a PAL of 2.41, 1.5 times that of urban office workers (Harris et al. 2025, PMID 40970487); rural Gambian men spent 3,880 ± 994 kcal a day by doubly labelled water, 64 kcal/kg (Heini et al. 1996, PMID 8735308).
- **Ceiling by duration:** sustained expenditure falls from about 10 × basal rate for 1-day events to about 2.5 × at about 28 weeks; tested in 14 ultra-endurance athletes (Best et al. 2025, PMID 41118725, testing the Thurber model).
- **Hunter-gatherers:** Hadza foragers had a higher PAL than Westerners, but the same daily expenditure after adjusting for body size (Pontzer et al. 2012, PMID 22848382).
- **Caffeine** (Dulloo et al. 1989, PMID 2912010):
  - 100 mg raised the resting rate by 3-4 % for 150 minutes;
  - 100 mg every 2 h over 12 h raised expenditure by 8-11 %;
  - the net effect was +150 kcal a day in lean adults.
- **Caffeine and effort:** caffeine raises energy and effortful behaviour (PMID 20164571).

### 2b. Needs

Each need below is the intake at which a measured marker (balance, a blood or urine level, a body store) stops changing. Where the study gives a need per energy, per kg or per gram of protein, that form is given too, because it scales with the city's work.

**Protein:** a meta-analysis of nitrogen balance in 235 adults gave an average requirement of 105 mg N/kg a day (0.65 g good-quality protein/kg) and a 97.5th percentile of 132 mg N/kg (0.83 g/kg). Climate, age, sex and protein source had no significant effect (Rand et al. 2003, PMID 12499330).

**Calcium need:** neutral balance in 155 adults was reached at 741 mg a day (95 % prediction interval 507-1,035), or 9.4 mg/kg, or 0.28 mg per kcal; age and sex had no effect (Hunt and Johnson 2007, PMID 17921384).

**Magnesium:** neutral balance in 243 adults (27 controlled studies) at 165 mg a day (95 % prediction interval 113-237), or 2.36 mg/kg, or 0.075 mg per kcal; age and sex had no effect (Hunt and Johnson 2006, PMID 17023712).

**Iron:**
- body iron excretion measured by isotope turnover: median 1.18 mg a day in 29 men, 1.58 mg in 19 menstruating women (1.66 without hormonal contraception), 0.99 mg in 5 postmenopausal women; menstrual iron explained 90 % of the variation in women (Hunt et al. 2009, PMID 19386738);
- absorbed iron needed by adult menstruating women, 95th percentile: 2.84 mg a day. Whole-diet absorption in people without iron stores: 14 % (Swedish diet), 16 % (French), 16.6 % (US) (Hallberg and Rossander-Hultén 1991, PMID 1957820).

**Zinc absorption** (Miller et al. 2013, isotope studies in healthy adults, R² 0.88; PMID 22617116, equation 2 and Table 3 of the full text, PMC3683099):

  TAZ = ½ [ X + A_MAX + Z − √( (X + A_MAX + Z)² − 4 A_MAX Z ) ], with Z = TDZ (1 + B_Pr TDPr) and X = K_T (1 + TDP (1 − B_Ca TDC) / K_P)

  | Symbol | Meaning | Unit | Estimate (augmented data, n 54) |
  |---|---|---|---|
  | TAZ | total daily absorbed zinc | mmol/d | — |
  | TDZ | total daily dietary zinc | mmol/d | — |
  | TDP | total daily dietary phytate | mmol/d | — |
  | TDC | total daily dietary calcium | mmol/d | — |
  | TDPr | total daily dietary protein | g/d | — |
  | A_MAX | maximum zinc absorption | mmol/d | 0.084 (95 % CI 0.076-0.095) |
  | K_T | zinc-transporter dissociation constant | mmol/d | 0.069 (0.022-0.38) |
  | K_P | zinc-phytate dissociation constant | mmol/d | 0.44 (0.19-0.90) |
  | B_Ca | calcium parameter | per mmol/d | 0.017 (0.0091-0.022) |
  | B_Pr | protein parameter | per g/d | 0.012 (0.0017-0.092) |

  Iron had no discernible effect and was dropped. In the 43 diets fitted, absorbed zinc averaged 3.04 mg a day (1.44-5.10) from 10.6 mg eaten, a fractional absorption of 0.32 (0.14-0.69). In the full text the phytate term TDP (1 − B_Ca TDC) is a fraction over K_P.

**Selenium:** in 98 Chinese adults eating 14 µg a day, plasma selenoprotein P was optimised by a 35 µg supplement, i.e. 49 µg a day in total; about 75 µg a day is postulated for full expression of selenoproteins in US residents after adjusting for weight and individual variation (Xia et al. 2010, PMID 20573787).

**Potassium:**
- 159 reconstructed Stone Age diets averaged 400 ± 125 mEq potassium a day, more than four times current intakes (Sebastian et al. 2006, PMID 17275582);
- the Yanomamo, without salt, excreted 60 mmol potassium a day (women) and 67 (men) with no hypertension (Mancilha-Carvalho et al. 1989, PMID 2810327);
- in 32 trials of 30-140 mmol supplements, the blood-pressure fall weakened above an extra 30 mmol a day and reversed above about 80 mmol (Filippini et al. 2020, PMID 32500831).
- **minimum need:** in 14 balance studies on 11 healthy men, urinary potassium fell to equal intake within 4-7 days at 25-30 mEq a day; at 14 mEq a day it fell to 19-27 mEq by day 8, and urinary loss stayed above intake whenever intake was below 14 mEq; at under 1 mEq a day it fell to about 9-13 mEq by day 8 and 4.2 mEq in the third week. Skin loss at normal intake is about 4 mEq a day (Squires and Huth 1959, PMID 13664789, read from the full text).

**Sodium without sweating:**
- Yanomamo adults excreted 0.9 mmol (21 mg) sodium a day; 84 % excreted under 1 mmol; blood pressure did not rise with age (Mancilha-Carvalho et al. 1989, PMID 2810327); renin and aldosterone were raised, as in acutely salt-restricted people (Oliver et al. 1975, PMID 1132118);
- in balance studies, the sodium intake needed to keep calcium and magnesium balance positive was 68 mg/kg a day (Nishimuta et al. 2018, PMID 29710036).

**Thiamin:** young men on a metabolic ward at 2,800 or 3,600 kcal: the minimum need was 0.30 mg per 1,000 kcal when the extra calories came from carbohydrate; need rises with energy intake and expenditure (Sauberlich et al. 1979, PMID 495541).

**Niacin:**
- in US Public Health Service studies of 1920-1936, fifty of over 400 women developed pellagra on diets now calculated to give 7.2-10.6 mg niacin equivalents (NE) per 1,000 kcal; most of these diets had under 60 % of the riboflavin allowance (Carpenter and Lewin 1985, PMID 3998856);
- men on 6.1 and 10.1 NE a day showed low urinary niacin metabolites against 19 NE a day (Jacob et al. 1989, PMID 2522982);
- in Japanese women the tryptophan-to-niacin factor was 67 mg tryptophan per mg niacin, against the conventional 60 (Fukuwatari et al. 2004, PMID 15895512).

**Riboflavin:** in 78 Chinese men spending 15.4 MJ a day, plasma and urinary riboflavin rose sharply above a total intake of about 1.4 mg a day, the estimated average need (Guo et al. 2016, PMID 27188899).

**Vitamin B6:** 0.015 mg per g of protein normalised most status markers in young women on 1.55 g protein/kg; 0.020 mg/g normalised all but one (Kretsch et al. 1995, PMID 7733034). Combined data from five studies give an average need of 1.2 mg a day, or 0.015 mg/g protein (Hansen et al. 2001, PMID 11385067).

**Folate:** 17 women on 200, 300 or 400 µg a day for 70 days: serum folate fell at 200 and 300 µg, with low values, and rose at 400 µg (O'Keefe et al. 1995, PMID 7562109).

**Vitamin B12:** all status markers levelled off at a dietary intake of 4.2-7.0 µg a day in 299 adults aged 18-50 (Bor et al. 2010, PMID 20071646) and at about 6 µg in 98 postmenopausal women (Bor et al. 2006, PMID 16400049).

**Vitamin A:** the intake that kept the body pool unchanged was 254-400 µg a day in Bangladeshi men, equal to 362-571 µg for a 70 kg man (Haskell et al. 2011, PMID 21248191); 285-330 µg RAE a day in US women (Sheftel et al. 2021, PMID 32492125).

**Iodine:** an optimal adult intake is 150-250 µg a day; about 50 % of Europe remains mildly deficient (Zimmermann 2009, PMID 19460960).

**Vitamin C:**
- seven volunteers on under 5 mg a day, then seven doses from 30 to 2,500 mg: plasma level against dose is sigmoid, steepest between 30 and 100 mg a day; white cells saturate at 100 mg, plasma at 1,000 mg; no vitamin C appears in urine below 100 mg (Levine et al. 1996, PMID 8623000);
- "the minimal amount of ascorbic acid necessary to prevent or cure scurvy appears to be slightly less than 10 mg daily"; "the full clinical syndrome does not appear until the normal body pool has been depleted to less than 300 mg" (Hodges et al. 1971, PMID 5090631; abstract as indexed by Scilit, the paper itself is closed access);
- frank scurvy appeared in all subjects when the pool fell to 300 mg; depletion is exponential, repletion linear and proportional to intake (Baker et al. 1971, PMID 5090632, same route); symptoms began at about 300 mg, when catabolism had fallen below 2.5 mg a day (Hodges et al. 1969, PMID 4977512, same route);
- the 1953 Sheffield study found 10 mg a day prevents scurvy (as reported by Hemilä 2026, PMID 41424103; also Riddoch et al. 1998, PMID 9505156);
- half-life 10-20 days, depending on plasma level; a pool of 20 mg/kg is kept by a turnover of 60 mg a day (Hornig 1981, PMID 7029735);
- the body pool rises to about 20 mg/kg with intake and is reached by 95 % of people at about 100 mg a day (Kallner et al. 1979, PMID 420145); smokers need at least 140 mg for the same pool (Kallner et al. 1981, PMID 7258125);
- volunteers deprived for 3 months developed signs of scurvy (Abboud et al. 1970, PMID 5411783). The Iowa depletion papers (Hodges 1969 and 1971, Baker 1971; PMID 4977512, 5090631, 5090632) have no abstract on PubMed and are closed access.

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
- in miners, construction workers in hot climates and soldiers, daily water losses can reach 10-12 L (Maughan and Shirreffs review, PMID 26290298);
- wildland firefighters in arduous work had a water turnover of 6.7 L a day, against 3.8 L in active students, and lost body water over 5 days (Ruby et al. 2003, PMID 14523317).

**Sodium lost in sweat:**
- men working in heat: predicted losses of 4.8-6 g sodium per work shift, equal to 10-15 g salt; more in unacclimatised men (Bates and Miller 2008, PMID 18226265);
- 1,303 athletes: sweat rates 0.83-1.51 L per hour and sodium losses 27-56 mmol (0.6-1.3 g) per hour by sport (Barnes et al. 2019, PMID 31230518).

**Vitamin stores:**
- fat-soluble vitamins are stored in fat and liver; water-soluble ones wash out (PMID 30860745);
- the liver's folate store lasted 4 months in one experiment and 19 months in another (PMID 29946471);
- B12 stores last years (PMID 33341967, 39149666).

### 2c. Absorption (bioavailability)

- **Calcium, by source** (fraction absorbed, measured with calcium isotopes in the same people where stated):

  | Source | Absorbed | Compared with | Study |
  |---|---|---|---|
  | Milk | 0.28-0.36 at 200-300 mg loads | — | the studies below |
  | Small soft-boned fish eaten whole (Bengali fish, 397 mg Ca in a meal) | 23.8 % | skimmed milk 21.8 % (no difference) | Hansen et al. 1998, PMID 9857327, 19 adults |
  | Calcium-rich mineral water (30 mg tracer load) | 21.6-22.6 % | milk 23.2 % | PMID 15365401 |
  | High-calcium mineral waters, pooled | equal to milk or slightly better | milk | Heaney 2006, PMID 16895885 |
  | Kale (low oxalate), 300 mg | 0.41 | milk 0.32 in the same 11 women | Heaney and Weaver 1990, PMID 2321572 |
  | Calcium oxalate | 0.10 alone, 0.14 with milk | milk 0.36 | Heaney and Weaver 1989, PMID 2801588 |
  | Spinach, 200 mg | 5.1 % | milk 27.6 % in the same 13 adults | Heaney et al. 1988, PMID 3354496 |
  | Ice cream | 26-28 % | milk 31 % | PMID 19394469 |

- **Load:** absorption of calcium salts with a light breakfast was 36.0 % at a 300 mg load and 28.4 % at 1,000 mg (Heaney et al. 1999, PMID 10367025). In rats, fractional absorption fell with both the meal's calcium and the previous intake, from 89 % to 11 % (PMID 8881718).
- **Vitamin D:** vitamin D and its metabolites raised calcium absorption from a 300 mg load (Heaney et al. 1997, PMID 9398723); serum 25(OH)D correlated with absorption from milk and from a plant source (PMID 25809682).
- **Plants in general:** the quantity of vegetables needed for sufficient calcium makes an exclusively plant diet impractical for most people without fortified foods or supplements; salt, protein and caffeine lower calcium retention (Weaver et al. 1999, PMID 10479229).

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
- **Calcium in drinking water:** Chinese public water held 2.5-155 mg/L (mean 40.4); in high-calcium cities water could supply up to 52 % of the adult average need (PMID 36342636). In a UK cohort, domestic water averaged 52.6 mg/L calcium (PMID 39784501).
- **Calcium in milk:** about 110 mg per 100 ml; lactose and casein phosphopeptides keep it soluble (Aoe 2018, PMID 29593135).
- **Calcium in bone broth:** cooking bones in water extracts little; lowering pH from 8.38 to 5.32 and cooking over 8 h raised extraction, but home-made and commercial broths held no more than a few tenths of a mg of calcium per serving, under 5 % of the daily need; lead and cadmium were a few µg per serving (Hsu et al. 2017, PMID 28804437). The bones themselves, eaten, are the calcium (whole small fish above; dried powdered bone is about 31 % calcium, PMID 33310253).
- **Parts of a cod** as % of whole ungutted weight (Torry Research Station, Advisory Note 17, reissued by FAO 2001; a measurement record, not a recommendation): head 21, guts 5-8 (average 7), liver 2-7 (5), roe 1-7 (4), backbone etc. 14, fins and lugs 10, skin 3, skinned fillet 36. "Weights of liver, guts, roe, etc., can fluctuate enormously with season, ground, condition of fish."
- **Cod liver index** (liver weight ÷ body weight) in 200 Norwegian coastal cod: 0.039 north, 0.027 west, 0.026 east; range 0.010-0.107 (Valdersnes et al. 2017, PMC5439708, Table 1).
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
- **How long food stays in the stomach:** across 33 studies of meals of 50-1,250 ml, the denser the meal in kcal per ml, the less volume left the stomach per minute, but energy delivered per minute still rose with density (Hunt and Stubbs 1975, PMID 1127608). A larger, denser meal therefore stays longer.
- **Meal type and sleepiness:** a solid meal shortened sleep latency against an equal volume of water, but high-fat, high-carbohydrate and mixed meals did not differ (Orr et al. 1997, PMID 9284488). This contrasts with Wells 1997 above.
- **Texture and eating rate:** hard ultra-processed meals were eaten at 25.9 g/min against 61.2 g/min for soft ones and gave 32 % more fullness for the same energy (PMID 42176807); slow eating of low energy-density food gave 573 kcal (50 %) less intake than fast eating of high energy-density food (PMID 40516651).
- **Eggs:** an egg breakfast cut intake over the next 24 hours in 21 men against an isoenergetic bagel breakfast (Ratliff et al. 2010, PMID 20226994).
- **Sensory-specific satiety** is a short-term satiety signal (PMID 1752065).
- **Protein leverage:** protein is about 15 % of dietary energy and nearly constant across populations; the hypothesis is that people eat until a protein target is met, so a diet diluted in protein raises total energy intake (Simpson and Raubenheimer 2005, PMID 15836464; evidence reviewed in PMID 37820518).
- **Milk and later intake:** 34 boys given low-fat milk with breakfast ate 1,010 kcal at a buffet lunch 5 h later, against 1,059 after apple juice and 1,236 after water, and reported more satiety (Mehrabani et al. 2016, PMID 26099369).
- **Hyper-palatable foods, defined from composition** (Fazzino et al. 2019, PMID 31689013): fat and sodium (> 25 % of kcal from fat, ≥ 0.30 % sodium by weight); fat and simple sugars (> 20 % kcal from fat, > 20 % from sugar); carbohydrate and sodium (> 40 % kcal from carbohydrate, ≥ 0.20 % sodium). 62 % of 7,757 foods in the US food database met a criterion. This gives a per-food classification from composition alone.
- **Per-food palatability ratings:** the food-pics database holds normative ratings of palatability and desire to eat for 568 foods from 1,988 people (Blechert et al. 2014, PMID 25009514).
- **Palatable food and dopamine:** palatable food intake releases dopamine in two phases, at tasting and after ingestion (Thanarajah et al. 2019, PMID 30595479).
- **Which foods draw addictive-like eating:** among 35 foods, processing was a large positive predictor; fat and glycemic load were large positive predictors in a separate model (Schulte et al. 2015, PMID 25692302). This ranks attributes, not a dopamine value per food.

### 2f. Daily ceilings set by the gut

- **Fat:** healthy subjects given corn and olive oil up to 639 g a day absorbed more than 98 % over 20 days; one tolerated 500-600 g without symptoms; daily fat of 300-400 g regularly caused marked sweating (Kasper 1970, PMID 5495429, abstract).
- **Fructose alone:** no healthy subject malabsorbed 15 g; 10 % malabsorbed 25 g (without symptoms); 80 % malabsorbed 50 g and 55 % had symptoms (Rao et al. 2007, PMID 17625977). With an equal amount of glucose, 50 g fructose was absorbed by all; sucrose up to 100 g was absorbed by all (Rumessen and Gudmand-Høyer 1986, PMID 3781328). Fruit high in free fructose therefore has a ceiling that sugar does not.
- **Lactose:** lactose malabsorption has a global prevalence of 68 % (PMID 31953721). Most people with lactose intolerance tolerate 12-15 g lactose (about one cup of milk); symptoms grow above 12 g, are appreciable after 24 g, and 50 g causes symptoms in most (systematic review, Wilt et al. 2010, PMID 20629478). Women who maldigest lactose ate a dairy diet with about 1,500 mg calcium a day without major symptoms (Suarez et al. 1998, PMID 9808231).
- **Protein:** see section 2e (Bilsborough and Mann 2006).
- **Alcohol and fat together:** ad libitum, alcohol and a high-fat diet added up to 2.8 MJ a day of overfeeding (Tremblay et al. 1995, PMID 7661127).

### 2g. Harm

- **Alcohol, dose-response:** in 599,912 current drinkers (83 studies), all-cause mortality rose curvilinearly with intake, lowest at or below 100 g a week. Stroke rose by HR 1.14 per 100 g a week, fatal hypertensive disease by 1.24, heart failure by 1.09; myocardial infarction fell (HR 0.94). Against >0-100 g a week, life expectancy at 40 was about 6 months lower at 100-200 g, 1-2 years at 200-350 g and 4-5 years above 350 g (Wood et al. 2018, PMID 29676281).
- **Alcohol, minimum:** across 195 countries the level of consumption that minimised harm across health outcomes was zero (95 % UI 0.0-0.8) standard drinks a week; a standard drink is 10 g ethanol (GBD 2016 Alcohol Collaborators 2018, PMID 30146330).
- **Tobacco:**
  - 1-4 cigarettes a day against never smoking: ischaemic heart disease death RR 2.74 in men and 2.94 in women; death from any cause RR 1.57 and 1.47 (Bjartveit and Tverdal 2005, PMID 16183982);
  - lifelong consistent smokers of under 1 cigarette a day: all-cause mortality HR 1.64; 1-10 a day: HR 1.87 (Inoue-Choi et al. 2017, PMID 27918784);
  - British doctors born 1900-1930 who kept smoking cigarettes died about 10 years younger than lifelong non-smokers; stopping at 60, 50, 40 or 30 gained about 3, 6, 9 or 10 years (Doll et al. 2004, PMID 15213107).

### 2h. Measures

- **Mean adequacy ratio:** the average over nutrients of intake ÷ requirement, each capped at 1. A standard measure of diet adequacy, approved by you (M102).
- **Hydration index:** the hydration a drink gives relative to the same volume of water (M101). Measured as water retained 2 h after 1 L, relative to still water, in 72 men: full-fat milk 1.50, skimmed milk 1.58, oral rehydration solution 1.54; cola, tea, coffee, lager, orange juice and sports drink did not differ from water (Maughan et al. 2016, PMID 26702122; also PMID 42884730).

### 2i. Four levels per nutrient (R61, M109)

**The four levels are kept apart:**

| Level | Meaning | What a study must show |
|---|---|---|
| **Minimum** | the lowest intake at which a deficiency sign stays absent, or balance is kept | depletion, balance or deficiency-disease studies |
| **Mean / median intake** | what a population actually eats; not a target | intake surveys or 24 h urine collections |
| **Optimum** | the intake at which a status marker levels off (plateau, saturation, store kept) | dose-response studies on a marker |
| **Ceiling** | the intake above which a harm appears | toxicity, intolerance or risk studies |

**Units.** Each nutrient has one unit, per person per day. Where a study ties the need to energy, body weight or protein, that form is the unit, because it scales with the city's work and diet. Conversions are by molar mass: 1 mmol (mEq) sodium = 23.0 mg; 1 mmol potassium = 39.1 mg. Where no study found a plateau or a harm, the cell says so and gives what was measured instead.

**Mean / median source.** Unless stated, the mean or median is the US usual intake from naturally occurring sources only (no fortification, no supplements), NHANES 2003-2006, people aged 2 and older (Fulgoni et al. 2011, PMC3174857, Table 1, 50th percentile). This is one modern population, kept for consistency; it is not a target.

| Nutrient | Unit | Minimum | Mean / median intake | Optimum | Ceiling |
|---|---|---|---|---|---|
| Protein | g/kg | 0.65 (nitrogen balance, average; Rand 2003) | 1.2 mean in adults aged about 64 (PMID 42549120) | 1.62: no further gain in fat-free mass with resistance training above this (95 % CI 1.03-2.20; Morton et al. 2018, *BJSM*, 49 trials) | 2-2.5 suggested maximum, about 25 % of energy; above 35 % of energy dangerous (Bilsborough and Mann 2006) |
| Water | L | about 1 to drink at rest in mild conditions (total about 1.5, of which about 0.5 is metabolic water); urine at least about 0.5 to clear a 600 mOsm solute load (Tipton, *Exp Physiol* 2025, review) | 3.8 turnover in active students (Ruby 2003) | 3.7 men, 2.7 women meet the needs of most people at rest (Sawka 2005); rises with PAL, weight and heat (Yamada 2022) | kidneys excrete at most about 0.8-0.9 L per hour; above that, plasma sodium falls (Noakes et al. 2001, PMID 11732457) |
| Sodium | mg | 21 excreted by healthy Yanomamo (Mancilha-Carvalho 1989) | 3,950 global mean, 2010 (Powles et al. 2013, PMID 24366578) | 4,000-5,990 was the reference range in 17 countries; below 3,000 the risk of death and cardiovascular events was higher (OR 1.27), as it was at ≥ 7,000 (O'Donnell et al. 2014, PMID 25119607; observational, from estimated urinary excretion); plus sweat losses of 4,800-6,000 per hot work shift (Bates and Miller 2008) | ≥ 7,000 raised risk; ≥ 6,000 in people with hypertension (O'Donnell 2014) |
| Potassium | mg | 980-1,170 (25-30 mmol): urine fell to equal intake; below 550 (14 mmol) loss exceeded intake (Squires and Huth 1959) | 2,490 | no plateau found: risk fell as excretion rose above 1,500 (O'Donnell 2014); cardiovascular risk fell 15 % per extra 1,000 mg (meta-analysis of 56 studies). Stone Age diets, 15,600 ± 4,900 (400 ± 125 mmol; Sebastian 2006), are an intake, not an optimum | supplements above about 3,100 (80 mmol) extra a day raised blood pressure (Filippini 2020) |
| Calcium | mg | 741 (neutral balance; 0.28 mg/kcal) (Hunt and Johnson 2007) | 828; national averages 175-1,233 across 74 countries (Balk et al. 2017, PMID 29026938) | about 800: cardiovascular mortality rose below and above it; all-cause mortality did not fall further above 900 (dose-response meta-analysis, PMC4199062) | milk-alkali syndrome classically above 4,000, lower with high vitamin D or kidney disease (PMC3875933) |
| Magnesium | mg | 165 (neutral balance; 0.075 mg/kcal) (Hunt and Johnson 2006) | 254 | no plateau found: all-cause mortality fell 6 % per extra 100 mg of dietary magnesium (dose-response meta-analysis of 19 cohorts, PMC8321838) | diarrhoea from supplemental magnesium, the basis of the 350 mg supplemental limit (PMID 37487817) |
| Iron (absorbed) | mg absorbed | 1.18 men, 1.58 menstruating women (median losses; Hunt 2009); 2.84 for 95 % of menstruating women (Hallberg 1991) | 9.4 eaten (about 14-16.6 % absorbed from whole diets, Hallberg 1991) | dietary iron that covers the absorbed need at 15 % absorption: about 8 for men (1.18 ÷ 0.15) and 18.9 for 95 % of menstruating women (Hallberg 1991) | 80 mg supplemental iron raised constipation; 20-60 mg showed no dose effect (PMID 39582678); acute poisoning above 20 mg/kg (section 2j) |
| Zinc | mg absorbed | 3.9 men, 3.2 women absorbed a day to offset endogenous losses (Hambidge, Miller and Krebs 2011, *Int J Vitam Nutr Res* 81:1); dietary amount by Miller's absorption equation (section 2b) | 10.3 | dietary amount that supplies the absorbed need: 9.4 men, 6.8 women (dietary average requirement cited by Hambidge 2011); depends on phytate by Miller's equation (section 2b) | 60 a day for 10 weeks lowered copper status; 450-1,600 a day caused anaemia, copper deficiency and myeloneuropathy (PMID 38999082) |
| Iodine | µg | 51-58: minimum iodine excretion in three balance studies (obligatory loss; *Biomed Environ Sci* 2025) | food iodine 240-300 men, 190-210 women in the US, mostly from iodised salt and dairy (older estimate in the CDC nutrition report) | 150-250 (Zimmermann 2009) | urinary iodine ≥ 300 µg/L raised subclinical hypothyroidism, OR 1.45 (PMID 40274899); a concentration, not an intake |
| Selenium | µg | 17 prevents Keshan disease (Yang and Xia 1995, PMID 8561918) | 101 | 40 keeps glutathione peroxidase at plateau (Yang and Xia 1995); 49 optimises selenoprotein P, about 75 after adjustment (Xia 2010) | about 1,600 kept selenosis fingernail changes; patients recovered at 819 ± 126 (Yang and Xia 1995); intoxication outbreak at 4,990 mean (Yang et al. 1983, PMID 6846228) |
| Vitamin A | µg RAE | 150-200 offsets daily elimination (Japanese DRI 2025 estimate; institutional) | 380 | 362-571 keeps the body pool for a 70 kg man (Haskell 2011) | chronic toxicity at 2 mg retinol/kg a day in oil for months, 0.2 mg/kg in water-miscible forms within weeks (Myhre et al. 2003, PMID 14668278); high dietary retinol raised hip fracture risk, RR 1.23 (meta-analysis, PMID 34105132) |
| Thiamin | mg per 1,000 kcal | 0.30 (Sauberlich 1979) | 0.9 mg a day | status counts as adequate when the erythrocyte transketolase activation coefficient is below 1.15; 0.4 per 1,000 kcal is the EU reference for that (EFSA 2016; institutional) | none found by mouth: oral thiamin has not been linked to adverse events (LiverTox); 100-500 mg a day caused no side effects |
| Riboflavin | mg | above 0.5: 6 of 10 women on about 0.5 a day developed ariboflavinosis (*Public Health Reports* 1941) | 1.6 | 1.4: plasma and urinary riboflavin break point (Guo 2016) | none found: no adverse effects reported; absorption tops out at about 27 mg per dose (EU SCF) |
| Niacin | mg NE | 8.8 NE for the first 2,000 kcal is the base line for pellagra (Elgin State Hospital studies, Horwitt); 6.1 and 10.1 NE a day gave low metabolites (Jacob 1989); pellagra appeared at 7.2-10.6 NE per 1,000 kcal on riboflavin-poor diets (Carpenter and Lewin 1985) | 16.3 mg preformed niacin | 19 NE a day gave normal metabolites (Jacob 1989) | flushing from 30-50 mg nicotinic acid; liver injury mainly with extended-release nicotinic acid at lipid-lowering doses (MSD Manual) |
| Vitamin B6 | mg per g protein | on 0.16 mg a day blood B6 vanished within 25 days; 0.6-0.9 mg a day reversed the changes (US depletion studies, abstracts via Scilit) | 1.5 mg a day | 0.015 normalised most markers, 0.020 all but one (Kretsch 1995) | neuropathy at a mean of 117 mg a day (Dalton and Dalton 1987, PMID 3630649) |
| Folate | µg DFE | above 300: serum folate fell at 200 and 300 (O'Keefe 1995) | 189 | 400: serum folate rose (O'Keefe 1995) | above 1,000 synthetic folic acid can mask B12 deficiency by correcting its anaemia while nerve damage continues |
| Vitamin B12 | µg | about 1: 0.25-1.0 µg injected daily gave reticulocyte responses in pernicious anaemia, 0.1 µg did not (Darby; West and Reisner; 1965 *NEJM* review); about 1 µg is the daily loss (Carmel 2008, *Blood*) | 4.0 | 4.2-7.0: all markers level off (Bor 2010) | none found: oral high-dose trials of up to 7 years showed no side effects beyond placebo; acne is rare, mostly with injected hydroxocobalamin (PMC8377299) |
| Vitamin C | mg | just under 10 prevents or cures scurvy (Hodges 1971) | 63 | about 100: body pool full for 95 % (Kallner 1979), white cells saturated (Levine 1996) | at 1,000 urinary oxalate and urate rose; above 500 per dose the absorbed excess is excreted (Levine 1996) |


### 2j. Recommendations, athletes' intakes, upper limits, toxic and lethal doses (R62, M110)

Kept apart from section 2i because they are of a different kind:
- **Recommended intake**: set by an institution to cover nearly everyone (US National Academies RDA or AI; EU values where stated). It lies above the minimum and is not the optimum.
- **For athletes**: a sports-nutrition body's range, or sweat losses where no range exists. Reference intakes for athletes are not differentiated from the general population for most vitamins and minerals (review, PMC12845069).
- **Upper limit (UL)**: an institution's intake judged safe over time; harm usually starts well above it.
- **Toxic dose**: where harm has been seen in people.
- **Lethal dose**: the acute fatal dose in people where reported, and the oral LD50 in animals (single dose killing half of them, mg per kg body weight; PubChem, safety data sheets, RTECS, JECFA). Both describe poisoning, not diet.

| Nutrient | Recommended intake, adults | For athletes | Upper limit (UL) | Toxic dose in people | Lethal dose (people) / LD50 (oral) |
|---|---|---|---|---|---|
| Protein | 0.8 g/kg (RDA) | 1.4-2.0 g/kg; 2.3-3.1 g/kg to keep lean mass in an energy deficit; 0.25 g/kg or 20-40 g per meal (ISSN position stand 2017, PMC5477153) | none set | above 35 % of energy; 200-400 g a day may exceed the liver's capacity to make urea (Bilsborough and Mann 2006) | no LD50 exists for a food protein; death on protein-only diets ("rabbit starvation") is described but not quantified |
| Water | 1 ml per kcal spent, often 1.5 ml per kcal (US National Research Council) | towards 4 L and more when active in heat (Tipton 2025); daily losses of 10-12 L in miners and hot-climate workers (Maughan and Shirreffs, PMID 26290298) | none set | drinking faster than about 0.9 L an hour lowers plasma sodium (Noakes 2001) | people: deaths after about 7 L in under 90 minutes, and after about 1.9 L in 20 minutes; rat: 90 g/kg caused distress but not death |
| Sodium | 1,500 mg (AI); reduce intakes above 2,300 mg (chronic disease risk reduction value, National Academies 2019) | sweat holds 200-2,000 mg per L; sports drinks 500-700 mg per L; some athletes may need over 10,000 mg a day; targeted replacement needed only beyond 4 h, sweat over 1.8 L/h and drinking over 70 % of losses (PMID 35616504) | none set as UL (2,300 mg is a risk-reduction value) | replacing 100 % of sweat losses in under-hydrated athletes risks hypernatraemia | people: 0.75-3 g NaCl per kg (case literature); rat: about 3,000 mg/kg NaCl |
| Potassium | 3,400 mg men, 2,600 mg women (AI, National Academies 2019; 4,700 mg in the 2004 values); 3,500 mg (EFSA AI) | sweat holds 78-312 mg per L (2-8 mmol/L) | none set (no intake-response for harm with healthy kidneys, National Academies 2019) | severe hyperkalaemia in 5 of 13 oral overdoses of 6-120 g KCl (median 24 g); rare with normal kidneys | rat: 2,600-3,020 mg/kg KCl |
| Calcium | 1,000 mg; 1,200 mg for women from 51 and men from 71 (RDA) | 1,000-1,500 mg; 1,500 mg with the female athlete triad (consumer sources) | 2,500 mg to age 50, 2,000 mg from 51 (US); 2,500 mg (EU SCF 2003) | milk-alkali syndrome classically above 4 g a day, lower with high vitamin D or kidney disease (PMC3875933) | rat: 6,450 mg/kg calcium carbonate |
| Magnesium | 400-420 mg men, 310-320 mg women (RDA) | 250-900 mg, endurance athletes at the top (consumer handout); supplementation shows no performance effect (JISSN 2005 review) | 350 mg from supplements only, set for mild diarrhoea; a 2023 review argues for raising it (PMID 37487817) | diarrhoea first; serious toxicity mainly above 5,000 mg a day (consumer source) | rat: 2,800 mg/kg magnesium chloride |
| Iron | 8 mg men, 18 mg women 19-50 (RDA) | 10-15 mg (consumer handout); sweat holds about 0.3 mg per L; iron is critical in heavy endurance training (German Nutrition Society 2020) | 45 mg (US) | acute: under 20 mg/kg non-toxic, 20-60 mg/kg moderate, above 60 mg/kg severe | people: above 100-120 mg/kg often fatal; rat: 319 mg/kg ferrous sulfate |
| Zinc | 11 mg men, 8 mg women (RDA) | sweat holds about 0.5 mg per L; no separate range (PMC12845069) | 40 mg (US); 25 mg (EFSA) | 60 mg a day for 10 weeks lowered copper status; 450-1,600 mg a day caused anaemia, copper deficiency and myeloneuropathy (PMID 38999082) | rat: 1,710 mg/kg zinc sulfate dihydrate |
| Iodine | 150 µg (RDA) | no separate range (PMC12845069) | 1,100 µg (US, set on thyrotropin response); 600 µg (EFSA) | urinary iodine ≥ 300 µg/L raised subclinical hypothyroidism, OR 1.45 (PMID 40274899) | rat: 2,484-3,129 mg/kg potassium iodide; mouse: 1,000 mg/kg |
| Selenium | 55 µg (RDA) | no separate range (PMC12845069) | 400 µg (US); 255 µg (EFSA 2023) | about 1,600 µg kept selenosis fingernail changes (Yang and Xia 1995) | people: intoxication outbreak at a mean intake of 4,990 µg a day (Yang et al. 1983); rat: 7-12.7 mg/kg sodium selenite |
| Vitamin A | 900 µg RAE men, 700 µg women (RDA) | no athlete value; evidence sparse (PMC12845069) | 3,000 µg preformed (US and EFSA) | 2 mg retinol/kg a day in oil for months, 0.2 mg/kg in water-miscible forms within weeks (Myhre et al. 2003) | mouse: 2,570 mg/kg retinol (10-day); 4,100 mg/kg retinyl acetate |
| Thiamin | 1.2 mg men, 1.1 mg women (RDA) | thiamin is lost in sweat; B-complex supplements help only where intake is insufficient (PMC12845069) | none set; 100 mg supplemental as guidance (UK EVM, no adverse effects found) | none by mouth (LiverTox); high-dose intravenous use linked to rare liver injury | rat: 3,710 mg/kg thiamine hydrochloride |
| Riboflavin | 1.3 mg men, 1.1 mg women (RDA) | riboflavin is lost in sweat; supplements help only where intake is insufficient (PMC12845069) | none set | none reported; single doses up to 60 mg without effects | rat: > 10,000 mg/kg (JECFA) |
| Niacin | 16 mg NE men, 14 mg women (RDA) | no separate range (PMC12845069) | 35 mg supplemental (US), set on flushing; 10 mg nicotinic acid, 900 mg nicotinamide (EFSA) | flushing from 30-50 mg nicotinic acid; liver injury mainly with extended-release forms at lipid-lowering doses | rat: 6,450-7,000 mg/kg nicotinic acid |
| Vitamin B6 | 1.3 mg to age 50; 1.7 mg men, 1.5 mg women from 51 (RDA) | no separate range (PMC12845069) | 100 mg (US); 12 mg (EFSA 2023, set on peripheral neuropathy) | neuropathy at a mean of 117 mg a day (Dalton and Dalton 1987) | rat: 4,000 mg/kg pyridoxine hydrochloride (other sheets above 6,600) |
| Folate | 400 µg DFE (RDA) | no separate range (PMC12845069) | 1,000 µg synthetic folic acid (US) | above 1,000 µg folic acid can mask B12 deficiency | 10,000 mg/kg folic acid (species not stated; Swedish Medical Products Agency assessment) |
| Vitamin B12 | 2.4 µg (RDA) | no separate range (PMC12845069) | none set; 2,000 µg used to treat deficiency | none by mouth in trials up to 7 years; rare acne with injections (PMC8377299) | mouse and rat: > 5,000 mg/kg cyanocobalamin |
| Vitamin C | 90 mg men, 75 mg women (RDA); 30-75 mg across countries | 200-500 mg reduced soreness; larger doses may blunt training adaptation (secondary sources; PMC12845069) | 2,000 mg (US); none (EFSA, insufficient data) | urinary oxalate and urate rose at 1,000 mg (Levine 1996) | rat: 11,900 mg/kg ascorbic acid |

## 3. Known faults in the data files, and their status (R64, M112)

| File | Fault | Status |
|---|---|---|
| `nutrition.json` and `nutrient_profiles.json` | **Two bases.** Energy, protein and fat in `nutrition.json` come from FAO "as bought" records (beef 150 kcal per 100 g); vitamins and minerals from USDA records of another form (beef carcass 291 kcal). | **Fixed for the food model:** `food_model.py` takes every value, energy included, from `nutrient_profiles.json` (one USDA form per good). **Open for the goods XML:** `nutrition.json` still feeds `tools/connector/food_values_edits.py`. |
| `nutrient_profiles.json` | **Niacin** was preformed only. | **Fixed:** tryptophan (USDA 1210) added; the model counts NE = niacin + tryptophan mg / 60. |
| `nutrient_needs.json` | **Thiamin and niacin** at a fixed 2,600 kcal. | **Fixed:** version 2 scales thiamin per 1,000 kcal; niacin's minimum per 1,000 kcal. |
| `nutrient_needs.json` | **All needs** were single EFSA values mixing the levels. | **Fixed:** version 2 holds the four levels of section 2i and the values of section 2j. |
| `nutrient_needs.json` | **Sodium** fixed. | **Fixed:** sweat losses per hot shift added with the case's share of hot-shift days. |
| `nutrient_needs.json` | **Water** fixed at 2,250 ml. | **Fixed:** the Yamada equation. |
| `nutrient_needs.json` | **Vitamin C** at 90 mg. | **Fixed:** minimum 10, optimum 100, ceiling 1,000. |
| Fish | The earlier "whole fish" shares (50 % herring, 45 % cod, 5 % liver) were unsourced. | **Replaced:** the whole cod by Torry part shares (fillet 36, liver 5, roe 4). The catch mix of a coast is not set from a source (`food_model.md` section 8). |

## 4. Limits of the record

- **Reward per food:** no study measures dopamine per food. What exists per food: the hyper-palatability criteria from composition (Fazzino 2019), palatability and desire-to-eat ratings for 568 foods (food-pics, Blechert 2014), and the attributes that predict addictive-like eating (processing, fat, glycemic load; Schulte 2015) (section 2e).
- **Lightness per food:** no per-food scale exists. Stomach residence rises with energy density (Hunt and Stubbs 1975); a solid meal causes sleepiness against water, but fat and carbohydrate meals did not differ (Orr 1997), while Wells 1997 found more sleepiness after a high-fat meal (section 2e).
- **Fullness per food:** the satiety index is measured for Holt's 38 foods and for breads in a later study (PMID 11478473); other foods follow the measured drivers: weight, water, fibre and protein raise fullness, fat and palatability lower it (Holt 1995), and energy density and eating rate set intake (PMID 40516651, 42176807).
- **Daily ceilings per food:** gut limits for fat, fructose, lactose and protein are in section 2f; your values for milk, lemons and fruit are the inputs beyond them.
- **Cattle and pig organs:**
  - steers of 500 and 600 kg: liver 1.12 % and 1.09 %, heart 0.37 % and 0.32 %, kidneys 0.18 % and 0.17 % (Serbian Domestic Spotted steers, *Tehnologija mesa* 27(4); the base, live or carcass weight, is not stated in the excerpt read);
  - beef animals: liver about 3.6-5.4 kg (8-12 lb), heart 1.4-2.3 kg (3-5 lb), tongue 0.5-1.4 kg (1-3 lb) (Michigan State extension bulletin E-1609, 1982);
  - Korean native cows of 297 kg: liver about 4.3 kg, heart about 1.36 kg;
  - pigs: liver 1.5 %, heart 0.3 %, tongue 0.2 %, diaphragm 0.3 % of slaughter by-products (García 2012, Cuba; base not stated).
- **Harm per amount:** the alcohol curve by 100 g a week and the tobacco risks are in section 2g. Further tobacco points: all-cause mortality HR 1.17 per 10 cigarettes a day (dose-response meta-analysis in breast cancer patients, PMC5347758); 60 % higher at 2-5 and 130 % higher at 11-15 cigarettes a day (recent cohort, as reported by News-Medical 2025).
- **Prices:** set later in the goods economy, by your decision (M102).

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
