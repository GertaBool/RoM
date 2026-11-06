# Activity and energy need, intake ceilings, vitamin stores, and the game's health display (R39, M85)

## 1. Recorded (M85)

- **Size by the inverse curve:** "overall good". Accepted.
- **Whale:** if it is available, it is possible food. No culture gate.
- **Vitamin stores:** by the usual groups, water-soluble and fat-soluble (section 4).
- **Energy need and intake ceilings:** your caveat changes the "surplus goes to storage" rule (sections 2 and 3).

## 2. Energy need follows activity

**Facts:**
- **FAO/WHO/UNU, *Human energy requirements* (2004),** Table 5.1. The energy need is the basal rate times the physical activity level (PAL):
  - sedentary or light lifestyle: PAL 1.53;
  - active: 1.76;
  - vigorous: 2.25. The example is six hours of non-mechanized farm work, plus water and wood carrying and hand chores.
  
  For a man with a basal rate of 1,745 kcal, the vigorous level is 3,925 kcal a day.
- **The basal rate** (same report): men aged 18-30, BMR = 15.057 × weight + 692.2 kcal. For 68.1 kg (EFSA's reference man) that is 1,717 kcal:
  - × 1.53 = 2,627 kcal;
  - × 1.76 = 3,022 kcal;
  - × 2.25 = 3,863 kcal.
  
  Your 3,000-4,000 kcal for a manual labourer is the active to vigorous range.
- **Caffeine** (Dulloo et al. 1989, PMID 2912010):
  - 100 mg raised the resting metabolic rate by 3-4 % over 150 minutes;
  - 100 mg every two hours over a 12-hour day raised energy use by 8-11 % in that period;
  - the net effect was 150 kcal a day in lean volunteers.

**What changes in the model:**
- **The need per head is not a fixed 2,600.** For a city:

  `need = BMR × PAL`, where `PAL = Σ share of people in each kind of work × that work's PAL + stimulant effect`
  - Non-mechanized farm work, carrying and hauling are vigorous (2.25).
  - Shop, service and standing work are active (1.76).
  - Office and desk work, and people not working, are sedentary (1.53).
  - Machinery moves farm work down the scale. The PAL table sits with the tile formula's tools (PR.F7).
  - Tea and coffee add their caffeine effect, up to about 150 kcal a day at six cups of 100 mg.
- **Eating more than the need raises activity, then output.** Fogel's rule is already in the model (`pop_model_math.md` section 6): work output scales with the energy left for work. Energy eaten above the need raises the PAL up to the vigorous level, and with it work output. Only what cannot be eaten (section 3) or is not needed at the highest activity goes to storage.
- **Food sufficiency `x`** compares food with this need, so a city of labourers needs more food than a city of clerks for the same `x`.
- **Consequence for the England 1300 check** (PR.F8.T4): the diet gave 2,354 satiety units a day. Against a vigorous need of about 3,860 kcal the shortfall is larger than against 2,600. The check is to be rerun with the activity need.

## 3. How much people can eat: ceilings by food group

**Your examples:**
- very few people can eat a kilogram of cheese a day;
- many can eat a lot of pasta;
- sugar is easy to eat in quantity;
- about three litres of milk a day;
- more than a pound of ground beef gives heartburn;
- a whole watermelon can be eaten.

**Facts:**
- **Protein has a ceiling** (Bilsborough and Mann 2006, PMID 16779921):
  - the gut absorbs 1.3-10 g of amino acids an hour, and the liver can turn only so much excess nitrogen into urea;
  - protein above 35 % of energy is dangerous ("rabbit starvation");
  - a suggested maximum is about 25 % of energy (2-2.5 g per kg a day);
  - the theoretical safe maximum for an 80 kg person is 285-365 g a day.
- **Satiety per calorie differs by food** (Holt 1995, already in D27):
  - potatoes 323, fish 225, beef 176, cheese 146, white rice 138, white bread 100;
  - foods that fill less per calorie can be eaten in larger amounts of energy.

**Proposal: four limits per person per day, applied in order:**

| Limit | Rule | What it explains |
|---|---|---|
| Satiety | the sum of satiety units eaten stays under a daily capacity (Holt index × calories) | pasta and sugar can be eaten in quantity; cheese and fish fill fast |
| Protein | protein stays under 35 % of energy (danger), with 25 % as the comfortable limit | a pound of ground beef a day is about the limit; lean meat alone cannot feed a person |
| Per good | a daily maximum in grams where the body sets one: milk about 3 L by your estimate, with lactose tolerance by population (to source); fat-rich foods such as cheese by fat tolerance | a kilogram of cheese is too much; a whole watermelon is mostly water and fits |
| Volume | water-rich foods count by weight against the stomach, not by calories | a watermelon is eaten whole but gives few calories |

- **What is eaten:** the city eats its goods in order of its diet until each limit is reached.
- **The rest:** what cannot be eaten goes to storage (spoilage, D27 C), to trade, or to animals.

**Fat as context** (your note, not mapped): the value of fat depends on what the animals ate, freshness, vitamin E in unsaturated oils and the omega-3 to omega-6 ratio.

## 4. Vitamin stores: water-soluble and fat-soluble

**Facts:**
- Vitamins come in two groups: fat-soluble (A, D, E, K), stored in fat and the liver; and water-soluble (C and the B group), washed out and not easily stored (StatPearls, PMID 30860745).
- Within the water-soluble group: vitamin C runs out in about one to three months (scurvy after about four weeks in the Iowa study; scorbutic after three months, PMID 5411783); folate in four to nineteen months (PMID 29946471).
- B12 is the water-soluble exception: its liver store lasts years (PMID 33341967, 39149666).

**Model:**

| Group | Members | Store |
|---|---|---|
| water-soluble, short | C, B1 (thiamin), B2, B3 (niacin) | weeks to about three months |
| water-soluble, medium | folate | months |
| water-soluble, long | B12 | years |
| fat-soluble | A, D, E, K | months to years (liver and fat) |
| minerals | iron, zinc, iodine, calcium | iron store months to years; the others open |

- Short stores matter for voyages, sieges and seasons. Long stores matter only for a diet that lacks a group for years, for example B12 without animal foods.
- The exact sizes within each group (thiamin, vitamin A) stay to be sourced; the groups set the order of magnitude.

## 5. The game's health display (checked in the code)

**What the game already shows** (RoM main, `Assets/Python`, and the DLL on the economy branch d2a8f756):

| Place | What it shows | Where |
|---|---|---|
| City screen, health line | "good [healthy face] < bad [unhealthy face] = N [eaten food]" when unhealthy; good and bad counts otherwise | `CvMainInterface.py` lines 3782-3793; text `INTERFACE_CITY_HEALTH_BAD` (BUG) |
| Hover on the health line | every source by line: fresh water, features, power, resources, buildings, civics and civilization, handicap, espionage, and "from population" (one unhealthy face per size), with the total | `WIDGET_HELP_HEALTH`; `CvGameTextMgr::setBadHealthHelp` and `setGoodHealthHelp` |
| Effect | when bad exceeds good, the city eats the difference as extra food each turn | `CvCity::foodConsumption`, `healthRate` = min(0, good − bad) |
| Help texts | healthy and unhealthy face symbols on buildings, resources and civics | `HEALTHY_CHAR` and `UNHEALTHY_CHAR`, 24 uses in `CvGameTextMgr.cpp` |
| Alerts | "%s1 has become unhealthy", and a warning when a city is about to grow into unhealthiness | BUG `Civ4lerts.py`, `CityHealthiness` |
| Domestic advisors | a HEALTH column with net health in face symbols; the Revolution watch adds health as a revolution factor | `CvCustomizableDomesticAdvisor.py`, `RevolutionWatchAdvisor.py` |
| Demographics | a "Health" row: the player's good × 100 ÷ (good + bad), ranked against rivals | `CvInfoScreen.py` `getHealthValue` |

**What this means for the model:**
- **The ratio I proposed already exists in the game.** The demographics screen computes good ÷ (good + bad) for each player. The proposal applies the same ratio per city, as `H` in the health burden.
- **The size term:** "from population" adds one unhealthy face per size (`unhealthyPopulation`). Density is now its own term (the unsanitized penalty, from people not working plots and the mitigating infrastructure), so I propose leaving the size term out of `H` and showing the density term in its place.
- **The food penalty:** today bad health eats food. Under the population model, health acts through the burden: growth slows or turns negative. Keeping both would count bad health twice. I propose replacing the food penalty with the burden.
- **The display stays and gains lines.** The faces, the hover list, the alerts, the advisor column and the demographics row keep working. The hover list adds the burden's parts: water (D31), sanitation and density, deficiencies (by nutrient), war. The "eaten food" figure becomes the burden's effect on growth per 1,000.

**Questions for you:**
1. Replace the food penalty with the burden's effect on growth (recommended), or keep both?
2. Replace "from population" with the density term in the faces (recommended), or keep it?

## 6. Open

- The PAL of each kind of work and how machinery moves it; per-good ceilings for milk (lactose tolerance by population) and fat; the satiety capacity per day.
- Thiamin, vitamin A and mineral store sizes.
- The England 1300 check rerun with the activity need.
