# Review of the food model against the record (R67, M115)

## 1. The rice town's 0.816 (R67.1)

The figure is the arithmetic of the model as it stands: the mean of 17 ratios, each capped at 1 (run of 2026-11-07, `food_model_cases.json`).

| Nutrient | Intake | Target | Ratio | Counted |
|---|---|---|---|---|
| protein (g) | 83.0 | 97.2 | 0.85 | 0.854 |
| sodium (mg) | 7,885 | 7,695 | 1.02 | 1 |
| potassium (mg) | 3,308 | 3,000 | 1.10 | 1 |
| calcium (mg) | 104 | 800 | 0.13 | 0.130 |
| magnesium (mg) | 968 | 363 | 2.67 | 1 |
| iron (mg) | 10.9 | 13.4 | 0.81 | 0.812 |
| zinc (mg) | 16.8 | 8.1 | 2.08 | 1 |
| iodine (µg) | 525 | 200 | 2.63 | 1 |
| selenium (µg) | 173 | 49 | 3.53 | 1 |
| vitamin A (µg RAE) | 2,132 | 467 | 4.57 | 1 |
| thiamin (mg) | 4.2 | 1.2 | 3.42 | 1 |
| riboflavin (mg) | 1.1 | 1.4 | 0.79 | 0.791 |
| niacin (mg NE) | 38.0 | 19.0 | 2.00 | 1 |
| vitamin B6 (mg) | 4.6 | 1.5 | 3.13 | 1 |
| folate (µg DFE) | 259 | 400 | 0.65 | 0.647 |
| vitamin B12 (µg) | 2.4 | 5.6 | 0.43 | 0.433 |
| vitamin C (mg) | 20.7 | 100 | 0.21 | 0.207 |
| **mean** | | | | **0.816** |

The arithmetic is right; the inputs and the measure make the number wrong. What makes it wrong:

1. **The rice is brown rice.** The model eats the first form in `nutrient_profiles.json`, and the first form of BONUS_RICE is brown rice. That choice was never made from a source or a case. Brown rice has 0.541 mg thiamin, 116 mg magnesium and 0.477 mg B6 per 100 g; polished rice 0.07, 25 and 0.164. Thiamin (3.42 x target), magnesium (2.67) and B6 (3.13) come from it, and thiamin is the nutrient a polished-rice diet lacks (beriberi). The same unexamined default makes potatoes raw, wine grapes and tea black tea.
2. **The fish is North Atlantic cod with its liver.** A rice town's fish is not cod mølje. The cod liver gives the vitamin A (4.57 x target) and the MEXT cod value the iodine (2.63 x). Small fish eaten whole, which the record holds for such diets (Kongsbak 2008; Hansen 1998: calcium absorbed as well as from milk), are not in the composition.
3. **Tea counts nothing.** The model reads USDA brewed black tea (vitamin C 0). The record holds MEXT green tea infusions with vitamin C (gyokuro 19, sencha 6 mg per 100 g) and your input that teas help against scurvy (M82, M83). Tea's caffeine (Dulloo 1989) is not applied either.
4. **Iron is overstated.** 600 g of tea with meals lowers iron absorption by 64 % (record 2c); the model does not apply it, and brown rice phytate lowers it further.
5. **The mean hides deficiency.** Ten nutrients counted at 1 hide that calcium is at 13 % of target and below its minimum, B12 at 43 % and vitamin C at 21 %. A capped mean rewards surpluses it cannot use and lets them sit beside severe gaps.

## 2. Recorded inputs and facts the model does not apply (R67.2)

### Your inputs (nutrition_record.md section 1)

| Prompt | Input | In the model |
|---|---|---|
| M92, M93 | Fullness (satiety) is the gauge of being fed; satiety being met is the baseline; grains and tubers kept people fed | not applied: satiety is only reported |
| M85, M88 | Ceilings by food group: few can eat 1 kg of cheese; much pasta; sugar is easy; about 3 L milk; more than a pound of ground beef gives heartburn; a whole watermelon | only milk (3 L) and fruit (one watermelon) applied; meat and cheese ceilings not applied |
| M92 | Lemons need an upper limit | not applied (no value given) |
| M88, M93 | Fat from one good: 250 g | applied |
| M88 | Highest quality first, then other things: "steak and potatoes, then dessert" | stage 4 orders by nutritional quality; the "then dessert" step (well-being goods after the limit) is not modelled |
| M89, M90, M91, M96, M102 | Well-being: lightness after eating, dopamine (reward), health effects, repetition; fruit and many drinks matter for it; separate sorted list | a sorted list is reported (hyper-palatable flag, energy density); health and repetition are not in it; nothing is consumed for well-being |
| M91 | Rich city: surplus milk partly into dairy products; bread eaten to some extent; sugar as today or 1900s Britain | not applied |
| M57, M75 | High-protein foods give strength bonuses; good food raises fertility, productivity, commerce, science and culture | no mapping from model outputs to game effects |
| M57 | Cereal products, dried fruit, fermented dairy, cured meat and fish keep longest and add most to the store | spoilage and keeping not in the model (D2, D5) |
| M84, M94 | Liver has plenty of vitamin A; animal foods are most bioavailable; whole animals | land animals are eaten as muscle only; their liver and organs are not in the composition |
| M83, M85 | Whale: if available it is food | whale is lean meat only; blubber (MEXT honkawa 577 kcal) not used |
| M85 | More calories and stimulants such as caffeine make people more active | caffeine not applied |
| M85 | Water- and fat-soluble vitamins differ for stores | not applied (stores are in the growth formula, M101) |
| M101, M102 | Harm terms for alcohol and tobacco | alcohol reported; tobacco has no composition |
| M88, M91 | Commercial Center and Commodity Market keep health and cut spoilage (fresh by half, kept by a quarter) | not in the model (game side) |
| M113 | Fishing peoples lived on fish and what they gathered locally | cod, herring and clams in the case; seaweed, shore plants and berries are not game goods with records |

### Facts in the record not applied

| Section | Fact | In the model |
|---|---|---|
| 2c | Tea −64 %, coffee −39 % iron absorption; vitamin C and meat raise it | not applied |
| 2c | Calcium absorbed by source (milk 0.28-0.36, small fish 0.238, kale 0.41, spinach 0.051); falls with load | not applied: calcium is dietary |
| 2c | B12 absorption saturates at 1.5-2 µg per meal; absorbed share by food | not applied (three meals give at most 4.5-6 µg absorbed) |
| 2c | Phytate lowers zinc, iron, calcium | zinc only, reported after the solve |
| 2c | Maize niacin released by alkali treatment | not applied (maize niacin always one third) |
| 2a | Caffeine +150 kcal at 600 mg | not applied |
| 2e | Satiety index; fullness drivers (weight, water, fibre, protein); protein leverage | reported only |
| 2f | Free fructose limit (25 g alone; absorbed with glucose) | not applied (profiles hold total sugars) |
| 2f | Alcohol with fat raises intake 2.8 MJ a day | not applied |
| 2d | Small fish eaten whole: calcium, haem iron, zinc, vitamin A | no composition used |
| 4 | Organ weights of cattle and pigs | not applied |

### Choices in the model without a source

- First form of each good (brown rice, raw potato, grapes for wine, black tea, muscle meat).
- Midpoint of every range, and the male share weighting.
- A single adult-equivalent person (no children: the record has no child values).
- Equal weight of every nutrient in the MAR.
