# The food penalty in the code, the faces, and the full energy and intake model (R40, M86)

## 1. The food penalty: what the code does (economy branch d2a8f756)

**How health enters food today:**

```
healthRate      = min(0, goodHealth − badHealth)                       CvCity.cpp 5396
badHealth       = unhealthyPopulation (= size) − the negative sources  CvCity.cpp 5331, 5250
foodConsumption = size × FOOD_CONSUMPTION_PER_POPULATION (3) − healthRate   CvCity.cpp 5403
foodDifference  = food yield − foodConsumption                          CvCity.cpp 5408
doGrowth:  food box += foodDifference                                    CvCity.cpp 13595
           box ≥ growthThreshold (30 + 10 × size, scaled) → size + 1
           box < 0 → box emptied, size − 1
```

- **Each unhealthy face beyond the healthy ones eats one food a turn.** A citizen eats 3, so each face past the limit costs a third of a citizen's food.
- **The effect is a food-box effect:** growth slows, and when the surplus turns negative the city shrinks one size each time the box empties.
- **The same face costs the same food at any size,** while the box grows with size (30 + 10 × size). So one face slows a small city far more than a large one.
- **Health is in effect a size cap.** Past the healthy limit, each further citizen costs 4 food instead of 3. Without health, the largest size the food can carry is (food + good − other bad) ÷ 4.

**Other uses of `healthRate < 0` in the code:**
- the city bar shows the unhealthy symbol (`CvGameTextMgr::buildCityBillboardIconString`);
- the city graphic shows `EFFECT_CITY_DISEASED` (`CvCity::getVisibleEffects`);
- We Love the King Day is blocked (`CvCity::doTurn`);
- the AI reads it in tile, building, improvement, hurry and target-size valuations (`CvCityAI`, `CvPlayerAI`: 14 callers of `healthRate`, 20 of `badHealth`);
- the food help text, plot help, alerts, advisors and demographics read it too (`round_m85.md` section 5).

**What the population model implements instead:**
- **Growth comes from people, not from a food box.** People change by fertility minus the health burden each year (`pop_model_math.md`); size follows people by the inverse curve; the bar shows the progress in people (decided, M84).
- **Food enters as food sufficiency `x`** in fertility and the burden.
- **Health enters as `H`** in the base burden, `D × (2 − H)`.
- **Eating is per person in the goods pass** (section 3). The engine's `size × 3` consumption, and the `− healthRate` added to it, are no longer what feeds or starves the city.

**Side by side** (computed):

| | Engine today | Population model |
|---|---|---|
| Unit of the effect | food per turn, into the food box | per 1,000 people a year, in the growth rate |
| Size 10, surplus 5 food, three faces beyond the healthy | surplus 2: the box fills in 65 turns instead of 26 (at 25 years a turn, growth 0.016 % a year instead of 0.041 %) | depends on H and on food per head |
| Bad health with plenty of food | still costs food; growth slows by the same amount | the burden rises; growth slows, but food per head still drives fertility |
| Where the city settles | the size where food = 3 × size + the faces' food | the people where fertility = burden: H = 0.7 holds 6 % fewer people than H = 1, H = 0.41 holds 14 % fewer, H = 0 holds 23 % fewer |
| Shrinking | one size when the box runs dry | people fall when the burden exceeds fertility |

**Proposal:**
- **The food term goes, by construction.** The goods pass replaces `foodConsumption`, so the `− healthRate` food cost is no longer there. Bad health acts once, through `H` in the burden. That is the same direction as today (bad health slows growth and caps the city), but in the population model's units.
- **`healthRate` and `badHealth` stay** with their meaning (unhealthy faces exceed healthy ones), so the billboard symbol, the diseased smoke, the We Love the King Day rule, the alerts, the advisors and the AI's valuations keep working.
- **`foodDifference`** becomes food produced minus food eaten by the people (the surplus to storage). The bar, the growth-turns text and the AI's food checks read it with that meaning. Where the AI used it to time growth, it reads the people's growth rate instead.

## 2. The faces stay as the sign of missing infrastructure

**As you said:** the unhealthy faces are the most intuitive way to show that a city lacks key infrastructure. They stay, and the hover gains lines for water, sanitation and density, missing nutrients and war.

**What the faces should count:**
- **"From population"** today adds one unhealthy face per size.
  - **Proposal:** count it from the dense population, the people not working plots, through the same inverse curve.
  - Then a farming district of 1 million with few town dwellers shows few faces. A trade city of the same size shows many, until aqueducts, baths and sewers (healthy faces) balance them.
- **The infrastructure buildings keep their healthy faces:** Aqueduct, Bath House, Hospital and the rest, as in the XML.

**The faces feed the model in two places:**
- `H = good ÷ (good + bad)` for the base burden, the same ratio the demographics screen already uses.
- **The unsanitized share:** `U = urban share × max(0, faces from dense population − healthy faces from sanitation buildings) ÷ faces from dense population`. When the sanitation faces cover the density faces, U is 0. Without them, U equals the urban share whatever the city's size. That matches your rule that without hygiene 500,000 and 10 million fare alike.

**Hover lines** (`CvGameTextMgr::setBadHealthHelp` and `setGoodHealthHelp`):
- water: supply level and quality (D31);
- sanitation and density: dense people, sewer level, `U`;
- missing nutrients: each short nutrient with its coverage;
- war: enemy units, siege, pillage;
- the result: the burden in per 1,000 a year, and its effect on growth.

## 3. The energy and intake model, in full (`plan/tools/energy_intake.py`)

### 3a. Need

```
BMR      = mean of men 15.057 × 68.1 + 692.2 and women 14.818 × 58.5 + 486.6  = 1,536 kcal a day
PAL_work = Σ_k share_k × PAL_k            sedentary 1.53, active 1.76, vigorous 2.25
E_need   = BMR × PAL_work + 150 × caffeine supply (0..1)
E_max    = BMR × 2.40 + 150 × caffeine supply
```

| Term | Source |
|---|---|
| BMR equations (ages 18-30) | FAO/WHO/UNU, *Human energy requirements* (2004) |
| reference weights 68.1 kg and 58.5 kg | EFSA 2017, Table 17 |
| PAL 1.53, 1.76, 2.25 | FAO 2004, Table 5.1 (the vigorous example is non-mechanized farm work) |
| PAL range 1.40-2.40; above 2.40 hard to keep up | FAO 2004, Table 5.3 |
| caffeine: up to 150 kcal a day (100 mg every 2 h over 12 h) | Dulloo et al. 1989 |

- **One abstracted adult** stands for the population (M84). Children and the old are not split out.
- **The kinds of work** come from the city's sectors (D26) and tools:
  - non-mechanized farm, mine and haul work is vigorous;
  - shop and service work is active;
  - desk work and people out of work are sedentary.
  - Machinery moves a sector down the scale.

### 3b. Intake: what is eaten

The city's food goods per head are eaten in proportion to what it has. They are scaled together until the first limit binds:

| Limit | Rule | Source or basis |
|---|---|---|
| Energy (appetite) | eaten energy ≤ `E_max` | FAO's upper activity level |
| Protein | protein × 4 ≤ 35 % of `E_max` | Bilsborough and Mann 2006: above 35 % of energy is dangerous ("rabbit starvation"); about 25 % is a suggested maximum |
| Fat from one good | ≤ 100 g a day | estimate from your examples: 3 L of whole milk holds 98 g, a pound of 80/20 ground beef 91 g |
| Milk | ≤ 3 L a day | your estimate; lactose tolerance by population to add |
| Food mass | ≤ 6 kg wet weight a day (drinks not counted) | estimate: a whole watermelon, with fruit as watermelon (your rule) |

**Fruit as watermelon:** fruit is mostly water. Watermelon is 91 % water at 30 kcal per 100 g, oranges 87 % at 47, apples 86 % at 52 (USDA). So fruit is limited by mass, not by appetite. A whole watermelon a day is possible, but gives few calories. Its water also counts toward the day's drink (FD.drink).

**What is not eaten** stays as goods: to storage (spoilage, D27 C), trade or animal feed.

### 3c. Outcome

```
x         = E_in ÷ E_need                         food sufficiency, used by the population model
PAL_act   = clamp(E_in ÷ BMR, 1.40, 2.40)         activity follows what is eaten (M85)
work      = clamp((PAL_act − 1.40) ÷ (PAL_work − 1.40), 0, 1.20)   physical work output factor
```

- **Below need:** activity and work output fall; Fogel's energy for work is in `pop_model_math.md` section 6. Fertility falls and the burden rises through `x`.
- **Above need:** activity rises, up to 2.40, and physical output rises by up to 20 %. That bonus cap is an estimate.
- **The satiety index** (Holt 1995) measures fullness over two hours. It is not a daily limit: potatoes, the most filling food per calorie, fed whole populations. It stays as a property of the goods (how often people eat, how full a diet feels), not as a cap.

### 3d. Test cases (computed)

| Case | Need kcal | Eaten kcal | x | Protein % of energy | Food mass g | PAL actual | Work factor | Binding limit | Left over (g) |
|---|---|---|---|---|---|---|---|---|---|
| labourers, bread, milk, beef, cabbage, ample | 3454 | 3685 | 1.07 | 18 | 1247 | 2.40 | 1.18 | energy | wheat bread 98, milk 108, beef 21, cabbage 32 |
| labourers, bread and beer only, scarce | 3454 | 2607 | 0.75 | 13 | 600 | 1.70 | 0.35 | none: ate what was there | - |
| clerks, same ample food as the labourers | 2349 | 3685 | 1.57 | 18 | 1247 | 2.40 | 1.20 | energy | wheat bread 98, milk 108, beef 21, cabbage 32 |
| clerks with coffee (6 cups) | 2499 | 2396 | 0.96 | 18 | 950 | 1.56 | 1.20 | none: ate what was there | - |
| potato labourers (boiled potatoes, milk) | 3454 | 3685 | 1.07 | 11 | 3499 | 2.40 | 1.18 | energy | potato 1500, milk 450 |
| fruit only, abundant (fruit as watermelon) | 2702 | 1800 | 0.67 | 8 | 6000 | 1.40 | 0.00 | mass | watermelon 6000 |
| apples only, abundant (fruit as watermelon) | 2702 | 3120 | 1.15 | 2 | 6000 | 2.03 | 1.20 | mass | apple 6000 |
| lean game only, abundant (deer) | 3454 | 1685 | 0.49 | 77 | 1404 | 1.40 | 0.00 | protein | deer 2595 |
| cheese only, abundant | 2702 | 1209 | 0.45 | 23 | 300 | 1.40 | 0.00 | fat (cheese) | cheese 1699 |
| beef 80/20 only, abundant | 2702 | 1270 | 0.47 | 27 | 500 | 1.40 | 0.00 | fat (beef) | beef 2500 |
| pasta only, abundant | 2702 | 3685 | 1.36 | 15 | 2332 | 2.40 | 1.20 | energy | pasta 3667 |
| sugar added to a scarce bread diet | 2702 | 3183 | 1.18 | 8 | 900 | 2.07 | 1.20 | none: ate what was there | - |
| mixed city: half farm, quarter shop, quarter desk | 2990 | 3685 | 1.23 | 16 | 1637 | 2.40 | 1.20 | energy | wheat bread 91, milk 91, beef 17, potato 68, apple 34 |

**What the cases show:**
- **Your examples come out of the limits:**
  - cheese stops at 300 g, by fat;
  - 80/20 beef at 500 g, by fat;
  - milk at about 3 L;
  - pasta, potatoes and sugar can be eaten in quantity;
  - a whole watermelon fits but feeds no one alone (1,800 kcal);
  - lean game alone starves by the protein limit (1,685 kcal against 3,454): rabbit starvation.
- **Labourers need about 3,450 kcal and clerks about 2,350.** Coffee adds 150.
- **One property to decide:** every well-fed city eats up to the top activity level (PAL 2.40), clerks included (x 1.57). That follows "more food, more activity" literally.

**Options for the appetite:**
- **A.** As computed: appetite up to PAL 2.40 whenever food is there.
- **B. (recommended)** Appetite up to the need plus a headroom, for example 15 % (an estimate). Activity rises with food, but a desk city does not eat like labourers. The headroom grows with stimulants.

## 4. Changes to earlier rounds

- **Food sufficiency `x` is measured in energy** against the activity need, not in satiety units against 2,600. The satiety index stays a property of the goods, not the limit.
- **The England 1300 check** (PR.F8.T4) is to be rerun with energy and the activity need.

## 5. Open

- Appetite option A or B, and the headroom.
- The masses per good where the body sets one (lactose tolerance by population); a source for the daily food mass. Rolls finds that people tend to eat a consistent weight of food (PMID 19303887); the 6 kg is the watermelon estimate.
- The PAL of each sector with and without machinery.
