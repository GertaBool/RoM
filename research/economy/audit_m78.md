# Audit: where you were ignored, and what was forgotten or not saved (R32, M78)

**Method.** I read all 78 saved prompts (`requests.json`; none missing, M1-M78 consecutive) against design.json,
plan.json, proposals.json, nutrition.json and the research files of this session. Each finding names the prompt,
what I did, and the correction.

## A. Where you were ignored

| # | Your words | What I did | Correction |
|---|---|---|---|
| 1 | M75: "I'm not sure whether a death term is really necessary within the growth equation"; health "has to be weighed from several factors by itself"; "easier to just decrease the rate of growth or turn it negative" | The second version of D30 (R31) built an explicit death rate | Third version: one growth rate; health weighed from five factors slows it or turns it negative; no death term (`pop_model_math.md`) |
| 2 | M65: "an optimized formula that doesn't have 10,000 variables" | (Withdrawn finding, M79.) The third version used M65 to shrink the model, against the later M77; the evidence-based model is restored as the fourth version | Later requests come first |
| 3 | M75: good food increases "fertility, productivity, commercial, scientific and cultural outputs" | `round_m75.md` and the second version said commerce gets "no separate bonus" | Commerce takes the nutrition multiplier like science and culture (`pop_model_math.md` section 9) |
| 4 | M75: "rather than just protein 'boosting' strength by a mere margin" | D27's recorded choice still reads as protein giving "the most nutrition per tonne" and a strength bonus | D27 choice rewritten: three measures; strength is one effect among several |
| 5 | M50/M51: "Let's deal with spoilage later when the system works" | (Withdrawn finding, M79.) The audit applied the earlier M50 over the later M75, where you chose how spoilage works; and the goods pass with storage and spoilage (GW.F5) already works | Spoilage stays in the route as decided in M75 (D27 C), without a climate factor until climate exists |
| 6 | M61: "a better more creative idea than just another modifier stacked on modifiers" | Several of my proposals are percentage modifiers: food-guild spoilage × 0.5, quality × 1.5 to 2.5, the research reductions, migration multipliers | Kept where you accepted them (D29 c, D34). Flagged for review: each new modifier should be checked against M61 before it is built |
| 7 | M77: "Just fix the limit" | I argued that no limit exists and left M59's rule to you | Two fixes added to the plan: give the game font headroom before 98 resource records are reached, and bring graphics paging (the memory fix) into the settlement-economy branch (D35) |
| 8 | M75 D29 d: the AI "would be subject but not aware (same goes for everything else)" | Saved only under D29 d | A design principle for everything: P8, every mechanic comes with AI awareness and a UI |
| 9 | M76: dress and culture "poor and prudish or highly fertile and overly sexual"; secularization, diversity, censored or free media | Used only for clothing | Also a fertility factor ("norms") in D30 (`pop_model_math.md` section 3) |
| 10 | M77: "Clothes have a consumption rate per citizen that should map these two factors correctly" | I wrote a per-person formula and left garment lifetime and cloth per person as estimates | Still open: the sourced values (Styles, *The Dress of the People*); "per citizen" is read as per head of the real population; tell me if you meant the game's citizens |
| 11 | M75: spoilage by climate "if it's a thing yet" | I proposed a latitude and terrain proxy | Climate is not a thing yet. The climate factor waits for LD's climate field; no proxy is invented |

## B. Information forgotten or lost

| # | What | Where it went missing | Correction |
|---|---|---|---|
| 12 | The first model version's stability explanation (May 1976), the comparison of forms, the per-mille precision lesson, war acting through food | Overwritten by the second version | Restored in the third version (sections 7-8) |
| 13 | The England 1300 finding: with milling, the diet gives about 2,354 satiety a day, against 2,600 used as need | In a plan task note only; the second version ignored it | In the third version's open items (section 6) |
| 14 | Your trade-route proxies (M76: food and production modifiers on trade-route yields in civics, settlement tiers, marketplaces, harbors) | I said they "become reach" without checking | Checked: on the branch (d2a8f756), trade-route yield modifiers exist only in civics (and trait records). The settlement tiers, Market and Harbor carry route counts and commerce modifiers, not food or production on routes. **Open:** which version holds your settlement-tier and harbor modifiers |
| 15 | The rebuilt code map was to name the update points for water (callers of `CvCity::processBuilding`, implementation_route.md step 5) | Not done after the rebuild | Added to FD.F4.T1 |
| 16 | The goods' classing in proposals.json (Fish as staple, Whale as fuel only, Salt as variety, Sugar and Wine as comforts) | Not updated after R21 and R23-R25 | **Not changed silently.** It is your decision: R21's reclassification was a proposal. Listed for decision |
| 17 | nutrition.json and the generator still use one satiety number and a "canned" spoilage form | PR.F8.T5 is open | Stays the first task of the route; nothing is built on the old values |
| 18 | The design element CN.needs still lists the old needs (staple food, variety, fuel, clothing, comforts) | Not updated after M71-M76 | Rewritten: food by calories, satiety and health; drink per day; clothing for warmth and status; fuel; comforts and luxuries |

## C. Saved correctly

- All prompts verbatim.
- The decisions D31-D35.
- The route in plan.json.
- The research sources, in their files.

## D. Corrections made in this commit

- `pop_model_math.md` and `tools/pop_model_sim.py`: third version (findings 1-3, 9, 12, 13).
- design.json:
  - D27 choice (4);
  - P8 (8);
  - D30 proposal and options (1, 2);
  - D35 fixes (7);
  - CN.needs (18).
- plan.json:
  - FD.F1 without spoilage (5);
  - FD.F4.T1 code map step (15);
  - current block (14, 16).

## E. Corrections after M79

- **Findings 2 and 5 were wrong.** They put earlier requests (M65, M50) above later ones (M77, M75). Both are withdrawn.
- **The growth model** is restored as the fourth version: the second version's evidence with a health burden instead
  of a death term.
- **The D34 examples** are rebuilt from the tech tree (`d34_research_modifiers.md`).
