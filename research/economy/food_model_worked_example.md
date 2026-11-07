# The food model, worked through (R50, M97; specification version 2)

Every number below is produced by `plan/tools/food_model_trace.py` from the data files. Equation numbers refer to `food_model_spec.md`.

## 1. The formulas

```
Per good g (per kcal):
 (E12) σ_g = Holt_g / 100  (else the fitted formula);  × 0.5 for drinks                 fullness
 (E13) s_g = (1 + 2.0 · p_g · min(q_g,1)) / (1 + 2.0 · 0.146 · 0.44)                     satisfaction
       p_g = 4 · protein_g / kcal_g ;  q_g = DIAAS (animal default 1.0, plant 0.44)
 (E14) ν_g = (1/13) · Σ_i min(1, (n_gi / kcal_g) / (need_i / 2600))                      nutrient density
 (E15) β_g = 4·sugar_g/kcal_g + 2 · F_g · C_g + 7·alcohol_g/kcal_g + min(1, water_g/kcal_g / 3) − 0.5 · F_g
       F_g = min(1, 9 · fat_g / kcal_g) ;  C_g = 1 − F_g − p_g − alcohol share               well-being
 (E16) N_g = s_g + ν_g  (nutrition list) ;  β_g (well-being list)

Per city (per person and day):
 (E1) a_g = S_g · 10^6 / (N · 365)
 (E3) PAL_w = Σ_k w_k · PAL_k        (E4) c = min(1, caffeine / 600 mg)
 (E5) E_need = 1536 · PAL_w + 150 c  (E6) E_max = 1536 · 2.40 + 150 c
 (E7) F_cap = 1.36 · E_max           (E8) P_max = 0.35 · E_max / 4
 (E11) cap_g = min(a_g, 250 / fat per g, 3000 if milk, 116 if lemon)
 (E17) pass 1: repeat { g* = argmax N_g / (1 + q_g / m_g) over goods within limits; q_g* += 10 / e_g*;
                        E += 10; F += 10 · σ_g* }  until F ≥ 1.36 · E_need
       pass 2: the same with β_g (β_g > 0)                                               until F ≥ F_cap
       (also stop at E ≥ E_max or when no good is within limits)
 (E18) fed = F / (1.36 · E_need)     (E19) x = E / E_need
```

**One identity explains most result changes.** At the stop, `F = Σ kcal_g · σ_g`, so

```
E = F / σ̄,   σ̄ = Σ kcal_g σ_g / Σ kcal_g   (the kcal-weighted mean fullness of what was eaten)
```

When eating stops at the fullness capacity, the energy eaten is the capacity divided by the average fullness per kcal of the diet. A diet of filling foods (potatoes, σ 3.23) gives less energy at the same fullness than one of milk (σ 0.78) or sugar (σ 1.00).

## 2. Three goods, term by term


Cow: per 100 g kcal 150, protein 18.5 g, fat 7.9 g; DIAAS 1.12
  E13  s = (1 + 2 x 0.493 x 1.00) / (1 + 2 x 0.146 x 0.44) = 1.760
  E14  terms: protein 1.00, vit_c 0.00, vit_a_rae 1.00, thiamin 0.97, niacin 1.00, folate_dfe 0.56, b12 1.00, iron 1.00, zinc 1.00, calcium 0.10, iodine 0.00, potassium 0.70, sodium 0.90
       nu = 9.226 / 13 = 0.710
  E15  beta = 0.000 + 2 x 0.474 x 0.033 + 0.000 + min(1, 0.201 / 3) - 0.5 x 0.474 = -0.139
  E16  N = s + nu = 2.470;  beta = -0.139;   E12  sigma = 1.760

Potato: per 100 g kcal 67, protein 1.6 g, fat 0.1 g; DIAAS 0.44
  E13  s = (1 + 2 x 0.096 x 0.44) / (1 + 2 x 0.146 x 0.44) = 0.961
  E14  terms: protein 1.00, vit_c 1.00, vit_a_rae 0.00, thiamin 1.00, niacin 1.00, folate_dfe 1.00, b12 0.00, iron 1.00, zinc 0.96, calcium 0.20, iodine 0.20, potassium 1.00, sodium 0.20
       nu = 8.562 / 13 = 0.659
  E15  beta = 0.053 + 2 x 0.013 x 0.891 + 0.000 + min(1, 0.885 / 3) - 0.5 x 0.013 = 0.365
  E16  N = s + nu = 1.620;  beta = 0.365;   E12  sigma = 3.230

Apple: per 100 g kcal 48, protein 0.1 g, fat 0.3 g; DIAAS 0.44
  E13  s = (1 + 2 x 0.008 x 0.44) / (1 + 2 x 0.146 x 0.44) = 0.893
  E14  terms: protein 0.12, vit_c 1.00, vit_a_rae 0.26, thiamin 1.00, niacin 0.32, folate_dfe 0.60, b12 0.00, iron 1.00, zinc 0.22, calcium 0.40, iodine 0.00, potassium 1.00, sodium 0.08
       nu = 6.005 / 13 = 0.462
  E15  beta = 0.866 + 2 x 0.056 x 0.935 + 0.000 + min(1, 1.645 / 3) - 0.5 x 0.056 = 1.491
  E16  N = s + nu = 1.355;  beta = 1.491;   E12  sigma = 1.970


**What the terms show:**
- **Beef:** ν = 0.71 because 9 of 13 nutrients reach the cap of 1 (protein, vitamin A from the 3 % liver, B1, B3, B12, iron, zinc), sodium is 0.90 and potassium 0.70. Vitamin C, iodine and calcium are about 0.
- **Potato:** ν = 0.66 because its protein density (1.6 g per 67 kcal = 0.024 g/kcal) exceeds the requirement density (45 g / 2,600 kcal = 0.017 g/kcal) and caps at 1. The cap counts adequacy per kcal, not protein quality; quality enters satisfaction `s` (potato 0.96 against beef 1.76).
- **Beef's well-being** is negative because of its fat term: fat share 0.47, so −0.5 × 0.47 outweighs its lightness of 0.067.

## 3. The rich city, version 1 against version 2

E. Rich city, 100,000, everything in surplus; 20 % vigorous, 40 % active, 40 % sedentary
  E3  PAL_w = 0.2 x 2.25 + 0.4 x 1.76 + 0.4 x 1.53 = 1.766
  E4  caffeine 94 mg -> c = 0.157
  E5  E_need = 1,536 x 1.766 + 150 x 0.157 = 2735 kcal
  E6  E_max = 1,536 x 2.40 + 150 x 0.157 = 3709 kcal
  E7  F_cap = 1.36 x E_max = 5044;  fed at 1.36 x E_need = 3720;  E8  P_max = 325 g
  E11 caps g: Cow 547, Dairy 3000, Potato 1643, Wheat 1095, Apple 547, Sugar 219, Wine 410
  version 1 (one pass on V): ends at E 2960 kcal, F 5046
  version 2: pass 1 ends at E 2120 kcal, F 3735 (fed); pass 2 ends at E 3300 kcal, F 5062

| Good | V (v1) | N (v2) | beta (v2) | sigma | serving g | eaten v1 g | eaten v2 g | kcal v1 | kcal v2 |
|---|---|---|---|---|---|---|---|---|---|
| Cow | 2.33 | 2.47 | -0.14 | 1.76 | 85 | 340 | 333 | 510 | 500 |
| Dairy | 2.92 | 2.06 | 0.86 | 0.78 | 244 | 1262 | 1934 | 769 | 1179 |
| Potato | 1.98 | 1.62 | 0.37 | 3.23 | 300 | 970 | 850 | 649 | 569 |
| Wheat | 1.68 | 1.55 | 0.13 | 1.57 | 64 | 164 | 134 | 440 | 360 |
| Apple | 2.85 | 1.35 | 1.49 | 1.97 | 242 | 541 | 541 | 260 | 260 |
| Sugar | 2.13 | 1.06 | 1.07 | 1.00 | 4.2 | 16 | 42 | 60 | 159 |
| Wine | 2.64 | 1.18 | 1.47 | 0.70 | 147 | 397 | 397 | 270 | 270 |
| total | | | | | | | | 2959 | 3299 |

**Why the numbers changed from version 1 to version 2:**

| Change | Cause in the formulas |
|---|---|
| Energy eaten 2,959 → 3,299 kcal | both versions stop at the fullness capacity (F ≈ 5,044). By the identity, E = F / σ̄: σ̄ fell from 5,046 / 2,960 = 1.70 to 5,062 / 3,300 = 1.53 because version 2 ate more milk (σ 0.78) and sugar (σ 1.00) and fewer potatoes (σ 3.23) |
| Milk 1,262 → 1,934 g | v1 key V = 2.92 is close to the other goods, so diminishing returns spread intake. In v2, pass 2 ranks by β: milk's β 0.86 is the highest of the goods still below their limits once apples (541 g, stock) and wine (397 g, stock) are used up |
| Sugar 16 → 42 g | in v1 sugar's V (2.13) is below potatoes and bread after diminishing returns; in v2 pass 2, sugar's β (1.07) is second only to fruit and wine, which ran out |
| Potatoes 970 → 850 g, bread 164 → 134 g | in v2 they enter in pass 1 by N (1.62, 1.55) and in pass 2 only with small β (0.37, 0.13) |
| Beef 340 → 333 g | almost unchanged: beef has the highest N (2.47) here, so pass 1 takes it first in both versions |
| Apples and wine unchanged | all the stock is eaten in both versions (541 g, 397 g) |
