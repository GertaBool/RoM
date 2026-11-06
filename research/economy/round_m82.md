# Food roles kept in view; scurvy and the whole diet (R36, M82)

## 1. Recorded (M82)

**The R21 roles are kept in view,** as you put it: "good roles to keep in mind".
- Whale as food.
- Horse meat and milk.
- Olives as oil.
- Sugar, Wine and Alcohol counted for calories.
- Salt as a preserver.
- Lemon is no longer the one good against scurvy (section 4).

**Your correction on scurvy:**
- Tea, lemons, apples, bananas and all fruit, wine grapes included, help against scurvy.
- Scurvy follows mostly from a diet that is plain and deficient.

## 2. Vitamin C in the goods (USDA SR Legacy, 2018-04, mg per 100 g)

Read from the USDA FoodData Central download (`FoodData_Central_sr_legacy_food_csv_2018-04`, nutrient 1162
"Vitamin C, total ascorbic acid"). The last column is how much of the food gives 10 mg, the daily amount that
prevents scurvy (section 3).

| Game good | USDA food (fdc id) | Vitamin C | For 10 mg a day |
|---|---|---:|---:|
| Lemon | Lemons, raw, without peel (167746) | 53 | 19 g |
| Lemon | Lemon juice, raw (167747) | 38.7 | 26 g |
| (lime) | Limes, raw (168155) | 29.1 | 34 g |
| (orange) | Oranges, raw (169097) | 53.2 | 19 g |
| Apple | Apples, raw, with skin (171688) | 4.6 | 217 g |
| Apple | Apples, dried, sulfured (171691) | 3.9 | 256 g |
| Banana | Bananas, raw (173944) | 8.7 | 115 g |
| Banana | Bananas, dehydrated (173945) | 7 | 143 g |
| Wine (the plot: grapes) | Grapes, red or green, raw (174683) | 3.2 | 313 g |
| Wine (dried grapes) | Raisins, dark, seedless (168165) | 2.3 | 435 g |
| Wine (the drink) | Wine, table, red (173190) and white (174837) | 0 | none |
| Alcohol | Beer (168746); distilled spirits (171919) | 0 | none |
| Tea | Tea, black, brewed (173227); green, brewed (171917) | 0 | none |
| Coffee | Coffee, brewed (171890) | 0 | none |
| Potato | Potatoes, raw (170026) | 19.7 | 51 g |
| Potato | Potatoes, boiled in skin (170438) | 13 | 77 g |
| (cabbage) | Cabbage, raw (169975) | 36.6 | 27 g |
| (sauerkraut) | Sauerkraut, canned (169279) | 14.7 | 68 g |
| Corn | Sweet corn, raw (169998) | 6.8 | 147 g |
| Wheat | Whole-grain wheat flour (168893) | 0 | none |
| Rice | White rice, raw (169756) | 0 | none |
| Olives | Ripe olives, canned (169094) | 0.9 | 1.1 kg |
| Olives | Olive oil (171413) | 0 | none |
| Horse | Horse, raw (175086) | 1 | 1 kg |
| Pig | Pork loin, raw (167818) | 0.6 | 1.7 kg |
| Deer | Deer, raw (173855) | 0 | none |
| Cow | Beef liver, raw (169451) | 1.3 | 770 g |
| Fish | Cod, raw (171955) | 1 | 1 kg |
| Crab | Blue crab, raw (174204) | 3 | 333 g |
| Clam, Shrimp | raw (174214, 174210) | 0 | none |
| Dairy | Whole cow's milk (171265) | 0 | none |
| (human milk) | Human milk (171279) | 5 | 200 g |
| Sugar, Salt | Granulated sugar (169655); table salt (173468) | 0 | none |
| Whale | Muktuk, bowhead skin and fat (167624) | no value in the file | open |

## 3. Scurvy: what the sources say (Wikipedia, *Scurvy* and *Vitamin C*)

**Amounts and timing:**
- As little as 10 mg of vitamin C a day from uncooked food prevents scurvy.
- Symptoms come after at least a month with little or none. An Iowa prison study saw the first signs after about
  four weeks.

**Losses before the food is eaten:**
- Cooking takes about 60 % from vegetables. Longer cooking takes more, and the cooking water carries part of it
  away.
- Storage loses it in proportion to the temperature. Pasteurization destroys the vitamin C of cow's milk.

**Who got it:**
- Sailors on long voyages that "relied on large staples of a limited variety of foods". Anson lost 1,300 of 2,000
  men in ten months.
- The Great Famine of Ireland (1845), the American Civil War, Scott's Antarctic expedition (1902), Gallipoli (1915),
  and refugees at 5 to 45 %.
- Infants fed pasteurized milk.
- Today: people on restricted diets, people with alcoholism, and old people living alone.

**What cured it:**
- Citrus. The Royal Navy issued lemon juice from 1795. When limes replaced lemons, the juice had much less vitamin C
  and was piped through copper; a 1918 test found it had almost no antiscorbutic power.
- Cartier's men in 1536: a "tea" of aneda tree needles (50 mg per 100 g). It was a conifer brew, not tea leaves.
  Spruce beer followed it.
- Sauerkraut, scurvygrass, wild onions.
- Potatoes and onion juice for infant scurvy.
- Uncooked fresh meat, especially liver. Horse meat in Napoleon's Egyptian campaign; seal meat with Scott.

## 4. What this means for the model (a reading)

**Facts it rests on:** sections 2 and 3.

**The reading:**
- **Scurvy comes from a plain diet,** as you said. Every case in section 3 is a diet narrowed to staples that carry
  no vitamin C: grain, rice, flour, salt meat, sugar, milk heated or stored. The ship's biscuit and salt pork diet
  is that diet.
- **Many goods help, at different doses.** A lemon covers the daily need with 19 g. Apples need about 220 g,
  bananas about 115 g, fresh grapes about 310 g, and boiled potatoes about 80 g. So fruit of every kind helps, and the
  potato is a major source. Ireland got scurvy in 1845 when the potato failed.
- **Two of the goods you named measure 0 mg in the USDA data:**
  - **Brewed tea.** Cartier's cure was a needle brew, not tea.
  - **Wine.** Fresh wine grapes carry 3.2 mg, raisins 2.3 mg, the wine itself 0 mg.
  - **Proposal:** the Wine plot yields grapes, which count as fruit when eaten fresh or dried; the drink gives
    calories and no vitamin C. Tea counts as a drink (D31, FD.drink) without vitamin C, unless you know a source
    that says otherwise. This is a point for you to settle.
- **Lemon's special role** is density and keeping. It covers the need in the smallest weight, and its juice keeps on
  a voyage. Ships and sieges value it. On land, any mix of fruit, vegetables, potatoes or fresh meat does the same
  work.

**How it would be computed:**
- `vitamin C coverage = Σ (good eaten per head a day × vitamin C of its form after storage and cooking) ÷ 10 mg`,
  capped at 1.
- Coverage below 1 for about a month raises the deficiency part of the health burden (`pop_model_math.md` section 3,
  `D_DEF`) and lowers the nutrients factor of fertility. Vitamin C is one group of the diet's coverage, alongside
  thiamine (beriberi) and the others.
- No single cure good is needed. A city whose diet is varied is covered. A city, army or fleet on staples is not.

**What would contradict it:** a sourced vitamin C value for brewed tea or wine above 0 that is large enough to
matter. A case of scurvy among people whose diet was varied and fresh would also contradict it.

## 5. Open

- **Whale (muktuk):** the USDA file has no value. A source on Arctic native foods is needed.
- **Storage and cooking losses by form:** fresh, dried, juice and cooked. Their values go into PR.F8.T5 with the
  three measures.
- **The amounts eaten per head of each good:** these come from the goods economy (CN.needs).
