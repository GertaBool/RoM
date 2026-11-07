# The food model: specification (version 2, M96)

This file is the authority for the food model. The code (`plan/tools/food_model.py`) implements it equation by equation, and the round files (`round_m85.md` to `round_m94.md`) are history. Every later change is first written here, as a change log entry (section 6), and only then made in the code.

## 1. What it does

For one city and one year, it turns the city's stocks of food and drink goods into:
1. what each person eats and drinks a day;
2. how fed, how strong and how well nourished the people are;
3. how much water they still need from the water supply;
4. how many tonnes are used, left and spoiled.

It runs in the goods pass, in the `consumeGoods` step (GW.F5), once per yearly step of a turn.

## 2. Notation

| Symbol | Meaning | Unit |
|---|---|---|
| `g` | a food or drink good | |
| `i` | a nutrient: protein, vitamins C, A, B1, B3, folate, B12, iron, zinc, calcium, iodine, potassium, sodium | |
| `k` | a kind of work: vigorous, active, sedentary | |
| `N` | the city's people | persons |
| `S_g` | stock of good `g` available this year | tonnes, as stored |
| `w_k` | share of people in work kind `k` (Σ `w_k` = 1) | |
| `q_g` | grams of `g` eaten per person a day | g, as stored |
| `e_g`, `p_g`, `f_g` | energy, protein, fat per gram eaten (`= kcal, protein, fat per 100 g × edible share ÷ 100`) | kcal/g, g/g |
| `n_gi` | amount of nutrient `i` per 100 g eaten | mg or µg |
| `σ_g` | fullness per kcal of `g` (white bread = 1) | |
| `s_g` | satisfaction per kcal of `g` (protein factor) | |
| `ν_g` | nutrient density of `g` against the requirement (0 to 1) | |
| `β_g` | well-being per kcal of `g` | |
| `N_g` | nutrition key: satisfaction + nutrient density | |
| `m_g` | one serving of `g` | g |

## 3. The model

### Step 1. What is available

```
(E1)  a_g = S_g × 10^6 ÷ (N × 365)                      grams per person a day
```

### Step 2. Need and ceilings

```
(E2)  BMR   = ½ × [(15.057 × 68.1 + 692.2) + (14.818 × 58.5 + 486.6)] = 1,536 kcal
(E3)  PAL_w = Σ_k w_k × PAL_k                            PAL_vigorous 2.25, active 1.76, sedentary 1.53
(E4)  c     = min(1, caffeine drunk ÷ 600 mg)            caffeine from tea and coffee (step 3a)
(E5)  E_need = BMR × PAL_w + 150 × c                     kcal a day
(E6)  E_max  = BMR × 2.40 + 150 × c                      the energy ceiling
(E7)  F_cap  = 1.36 × E_max                              the fullness capacity (1.36 = mean of Holt's 38 foods)
(E8)  P_max  = 0.35 × E_max ÷ 4                          the protein ceiling, g
```

### Step 3. What is eaten

**3a. Tea, coffee and salt**, outside the allocation, because they carry no energy:
```
(E9)  tea and coffee: drunk as available until caffeine reaches 600 mg
      caffeine per g = litres per kg × mg per litre ÷ 1,000   (tea 43 L × 200 mg; coffee 15 L × 600 mg)
(E10) salt: q_salt = min(a_salt, 10 g)
```

**3b. Each good's own ceiling:**
```
(E11) cap_g = min( a_g,  250 g ÷ f_g,  3,000 g if milk,  116 g if lemon )
```

**3c. The three motives and the preference, per kcal:**
```
(E12) σ_g = Holt index ÷ 100 where measured, else exp(0.080 + 0.222 ln(W_g/W_bread) + 0.661 P_g + 0.031 Fib_g − 0.213 Fat_g),
            × 0.5 for drinks
            W_g = grams per 240 kcal; P_g, Fat_g = protein and fat shares of energy; Fib_g = fibre g per 100 kcal
(E13) s_g = (1 + 2.0 × p × q) ÷ (1 + 2.0 × 0.146 × 0.44)
            p = protein share of energy; q = protein quality (DIAAS, capped at 1)
(E14) ν_g = average over the 13 nutrients i of  min(1, (n_gi per kcal) ÷ (need_i ÷ 2,600))
(E15) β_g = sugar share + 2 × fat share × carbohydrate share + alcohol share
            + min(1, water per kcal ÷ 3 g) − 0.5 × fat share
(E16) two separate sorted lists (M96; M88: "steak and potatoes, then dessert"):
      nutrition list:  key N_g = s_g + ν_g            (nutrition, health and satiety)
      well-being list: key β_g                        (lightness, reward)
```

**3d. The allocation, in two passes over the two lists.** Steps of 10 kcal. In each pass, each step goes to the good with the highest marginal value on that pass's list, among goods still within their limits. A good's ceiling is shared between the passes.

```
(E17) marginal_g = key_g ÷ (1 + q_g ÷ m_g)              key = N_g in pass 1, β_g in pass 2 (only goods with β_g > 0)
      limits: q_g ≤ cap_g;  Σ q_g p_g ≤ P_max;  Σ fruit eaten ≤ 4,518 g
      each step: E += 10;  F += 10 × σ_g
      pass 1 (nutrition):  until F ≥ 1.36 × E_need (fed), or E ≥ E_max, or no good within its limits
      pass 2 (well-being): from there until F ≥ F_cap, or E ≥ E_max, or no good with β_g > 0 within its limits
```

### Step 4. Outcomes

```
(E18) fed      = F ÷ (1.36 × E_need)                    being fed: fullness met at the need
(E19) x        = E ÷ E_need                              energy sufficiency
(E20) I_i      = Σ_g q_g × edible_g ÷ 100 × n_gi         nutrient intake (tea: litres of infusion)
(E21) a_Fe     = 0.10 + 0.08 × (animal protein ÷ all protein)
(E22) cov_i    = I_i ÷ need_i,   iron × a_Fe ÷ 0.16
(E23) W_food   = Σ (foods) q_g × edible_g ÷ 100 × water%_g
      W_drink  = Σ (drinks) q_g × edible_g × hydration index_g   (tea and coffee: litres made)
      W_plain  = max(0, 2,250 ml − W_food − W_drink)             from the city's water supply
(E24) PAL_act  = clamp(E ÷ BMR, 1.40, 2.40)
(E25) work     = clamp((PAL_act − 1.40) ÷ (PAL_w − 1.40), 0, 1.20)
(E26) used_g = q_g × N × 365 ÷ 10^6;  left_g = S_g − used_g;  spoiled_g = left_g × spoilage(form_g)
```

### What the outcomes feed (proposed, M93)

| Outcome | Feeds |
|---|---|
| `fed` | fertility and the famine term of the population model |
| `x` | the weakness of the underfed, and `work` |
| `cov_i` | the deficiency burden, the nutrients factor of fertility, output (iodine, iron) |
| `W_plain` | the demand on the water supply (D31) |
| `left`, `spoiled` | the stock, storage, trade and recipes (milk to cheese) |

## 4. Parameters

| Parameter | Value | Source or status |
|---|---|---|
| BMR equations (18-30 y) | (E2) | FAO/WHO/UNU, *Human energy requirements*, 2004 |
| reference weights | 68.1 kg, 58.5 kg | EFSA DRV summary report 2017, Table 17 |
| PAL by kind of work | 2.25, 1.76, 1.53 | FAO 2004, Table 5.1 |
| PAL range | 1.40-2.40 | FAO 2004, Table 5.3 |
| caffeine effect | 150 kcal at 600 mg | Dulloo et al. 1989, PMID 2912010 |
| tea, coffee brewing | 43 L/kg at 200 mg/L; 15 L/kg at 600 mg/L | MEXT food tables, remarks of the infusion records; checked against PubMed (PMID 27019564, 19007524, 14607010) |
| protein ceiling | 35 % of energy | Bilsborough and Mann 2006, PMID 16779921 |
| fat from one good | 250 g a day | the user (M93); heuristic for the usual maximum of a good |
| milk | 3,000 g a day | the user (M86) |
| fruit, all together | 4,518 g a day | one whole watermelon (USDA portion); the user's rule (M86) |
| lemons | 116 g a day | estimate: two lemons (M92) |
| salt | 10 g a day | estimate |
| fullness capacity factor | 1.36 | mean of Holt's 38 satiety values (PMID 7498104) |
| satiety formula (E12) | coefficients as given | fitted to 29 Holt foods, R² 0.46 (`satiety_fit.py`) |
| liquid satiety | × 0.5 | estimate (liquid calories satiate less, PMID 14649371) |
| protein factor (E13) | k 2.0, bread 0.146 × 0.44 | fitted to Holt's beef against bread (`open_questions.md` section 4) |
| nutrient needs | per nutrient | EFSA 2017; sodium from the Japanese DRI 2025 (`data/nutrient_needs.json`) |
| well-being weights (E15) | 1, 2, 1, 1, −0.5 | estimates on sourced effects (PMID 29909968, 37375579, 39729041, 9145937) |
| servings `m_g` | USDA household portions | `food_model.py` `SERVING_G` |
| total water need | 2,250 ml | EFSA 2010 (men 2.5 L, women 2.0 L) |
| iron absorption | 10-18 % | FAO/WHO 2004; the straight line is an estimate |
| work bonus ceiling | 1.20 | estimate |
| Fish good | 50 % herring, 45 % cod, 5 % liver; 15 % bones | estimates to source; USDA composition |
| Cow and Pig | 97 % meat, 3 % liver | estimate to source; USDA composition |

## 5. Data per good

| Data | File | Source |
|---|---|---|
| energy, protein, fat, edible share, keeping form, hydration index | `data/nutrition.json` | FAO; DIAAS; Holt |
| nutrients, water | `data/nutrient_profiles.json` | USDA SR Legacy; MEXT for iodine and tea |
| needs | `data/nutrient_needs.json` | EFSA 2017; Japanese DRI 2025 |
| fitted satiety | `data/satiety_fit.json` | `satiety_fit.py` |

## 6. Change log

Each row is a variable that was added, removed or changed. "Now" refers to sections 3 and 4.

| Round | Variable | Change | Before → after | Reason |
|---|---|---|---|---|
| M85 | energy need | changed | fixed 2,600 kcal → BMR × PAL by work, + caffeine (E2-E5) | the user: labourers burn 3,000-4,000 kcal; stimulants raise activity |
| M85 | intake ceilings | added | none → satiety, protein, per good, volume (proposal) | the user's examples (cheese, milk, beef, watermelon) |
| M85 | vitamin stores | added | → water-soluble and fat-soluble groups | the user |
| M86 | energy ceiling `E_max` | added | → BMR × 2.40 (E6) | FAO: PAL above 2.40 hard to keep up |
| M86 | food sufficiency `x` | changed | satiety units ÷ 2,600 → energy ÷ E_need (E19) | need varies with work |
| M86 | fat per good, milk, food mass | added | → 100 g, 3 L, 6 kg | the user's examples |
| M86 | work factor | added | → (E25), bonus ceiling 1.20 | Fogel's energy for work |
| M87 | stocks to grams | added | → (E1) | the goods pass counts tonnes |
| M87 | appetite headroom `h` | added | → 0.15 | estimate |
| M87 | drink cap, salt cap | added | → 3.5 L, 10 g | estimates |
| M87 | nutrient coverage, iron absorption | added | → (E20)-(E22) | the deficiency model (`round_m83.md`) |
| M88 | headroom `h`, food mass, drink cap | removed | 0.15, 6 kg, 3.5 L → none | the user: set by physiology; food weight overcomplicates; drink cap nonsense |
| M88 | fruit ceiling | added | → 4,518 g (one watermelon) | the user: fruit as watermelon |
| M88 | caffeine | changed | estimated 25 and 12 g/kg → MEXT brewing (E9), 600 mg | the user: quote PubMed |
| M88 | eating order | added | proportional → greedy by satiety × (1 + nutrient density) | the user: best goods first |
| M88 | nutrient density | added | → per 100 kcal ÷ daily need (**wrongly scaled; corrected M94**) | Nutrient Rich Foods index |
| M89-M90 | well-being tier | added, then withdrawn in M91 | → fruit and drinks first | misread of the user's point |
| M91 | water | changed | drink 1.8 L → total water 2,250 ml with food water, drinks, plain water (E23) | the user: one hydration equation |
| M91 | eating order | changed | greedy tiers → diminishing returns in servings (E17) | the user: no tiers; bread and sugar eaten in part |
| M91 | satiety for unmeasured goods | changed | protein factor → fitted formula (E12), drinks × 0.5 | the user: a correct formula |
| M91 | well-being `β_g` | added | → (E15) | the user: lightness, reward, health |
| M91 | Fish good | changed | fillet 64 kcal → whole animal 156 kcal | the user: the whole animal |
| M92 | fullness capacity `F_cap` | added | → 1.36 × E_max (E7), eating stops at it | the user: gauge by fullness |
| M92 | lemon ceiling | added | → 116 g | the user: no kilograms of lemons |
| M93 | fat per good | changed | 100 g → 250 g | the user |
| M93 | `fed` | added | → (E18) | the user: satiety met is the baseline of being fed |
| M93 | preference ÷ fullness | added, then withdrawn in M94 | | made filling foods rank last |
| M94 | nutrient density `ν_g` | changed | per 100 kcal ÷ daily need (beef 0.07) → per kcal ÷ requirement per kcal (beef 0.71) (E14) | scaling error |
| M94 | Cow, Pig | changed | muscle only → 97 % meat + 3 % liver | the user: liver; the whole animal |
| M94 | preference `V_g` | changed | Holt satiety + ν + β → protein satisfaction + ν + β (E16); Holt only for fullness (E12, E17) | the user (M88, M69): prefer nutrition, health, satiety |
| M96 | preference `V_g` | removed | one summed key → two keys, `N_g = s_g + ν_g` and `β_g` (E16) | the user: nutrition and well-being are two separate variables and two sorted lists |
| M96 | allocation | changed | one pass on `V_g` → pass 1 on the nutrition list until fed, pass 2 on the well-being list up to the fullness capacity (E17) | M88: the best goods by nutrition, health and satiety first, then other things ("then dessert") |

## 7. Rules for changes

1. A change is written here first: the equation or parameter in sections 3-4, and a row in section 6 with the round, the before and after, and the reason.
2. The code changes only what that row names, and the commit names the row.
3. Results are rerun and published with the version of this file they come from.
