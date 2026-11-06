# The record limit, clothing consumption, D34 examples, the Masons condition (R31, M77)

The population model's second version is in `pop_model_math.md` (R31.1).

## 1. Recorded as decided (M77)

- **D33 migration:** the flow model with civic values (`round_m76.md` section 2), accepted.
- **Food guilds** (`round_m76.md` section 4a) and **Clerks** (science and administration effects, cheaper writing,
  paper, printing and administration techs, lower distance maintenance), accepted.
- **Notre Dame and the J.S. Bach Cathedral** require the Masons guild's presence in the city.
- **D34:** the research field with the examples below.

## 2. The "32-bit limit": what it is, and the fix

**What the plan said.** Since M59: "no building per production step (the 32-bit executable's limits)". Nothing had
measured it.

**What the measurements say** (`research/graphics/README.md`, the mod's memory study):
- The executable, `Civ4BeyondSword.exe` of 2009-05-14, is already large-address-aware: 4 GB of address space on
  64-bit Windows. The DLL is linked with `/LARGEADDRESSAWARE` (every build's provenance).
- **R-A:** the DLL's own data, all game state and XML records included, was about 111 MB at turns 356-386, growing
  13.8 MB in 30 turns. XML records are not what fills memory.
- **R-C:** what grows is what the executable draws: unit models, city layouts and plot graphics (6,386 unit models,
  300 city layouts, 9,309 plots in that game). The memory allocation failure at 490 AD came from there.
- **The fix for that already exists:** graphics paging (`builds/graphics-paging/`) keeps those graphics only near the
  camera. It is tested headless and waits on your in-game check.

**The one real count limit for goods: the game font.**
- Each resource needs a glyph in both game fonts.
- `WOC_GAMEFONT_RESOURCE_FIX` is pinned at symbol code 8725, leaving room up to 98 resource records with an empty
  row (plan task LQ.F9; GitLab 93738c0c).
- There are 77 distinct resource records today (base and modules). Flax, Cloth, Fine Cloth, Coats and Dresses make
  82, and Meat (D28) 83. Under 98, so no change is needed.

**The fix beyond 98:** move the pin to the next multiple of 25 and add a row of glyphs to both font atlases, with the
existing tools (`font_patch.json`, `apply_font_patch.py`, the audit's `font_pinned`). That is one plan task when it
is needed.

**Consequence:** the M59 rule "no building per production step" rests on no measured limit. Buildings and goods can
be added as the design needs them. What costs memory is graphics, handled by paging. That decision (D28) stays
yours; the facts no longer force it.

## 3. Clothing consumption per citizen

**Facts:**
- **Spending:** Gregory King (1688) put clothing at about a quarter of England's national expenditure, the
  second-largest item.
- **Necessity:** clothing's income elasticity is below one in household studies (Turkey: food and clothing are both
  necessities).
- **Value and reuse:** clothes were valuable enough to appear in probate inventories, and were passed down and resold;
  the second-hand trade lasted until cheap ready-made clothing (Lemire 1988).
- **Open:** garment lifetimes and cloth per person. Styles, *The Dress of the People* (2007), has chapters on
  budgeting for clothes and clothes and the life cycle (to read).

**Proposal: consumption per person a year, for each garment good:**

```
garments per person per year = warmth need(climate) ÷ lifetime(material, quality)
                             + status demand × (wealth per head ÷ reference)^ε × dress norm
cloth per garment            = metres of cloth by garment type (coat, dress)
```

| Term | What sets it | Values (estimate unless sourced) |
|---|---|---|
| warmth need | climate: latitude and terrain (a climate field with LD) | coats needed per person: 0.5 in warm lands, 1.5 in cold |
| lifetime | material and quality grade | wool coat 5 years, linen shirt 2, fine and masterwork longer; to source from Styles |
| status demand | wealth per head (income from the goods economy) with elasticity ε below 1 | ε 0.8 (necessity; Engel-curve studies) |
| dress norm | religiosity, secularization, diversity, markets, media (`round_m76.md` section 3) | multiplies demand and how fast clothes go out of style |
| second-hand | a share of worn garments passes to the poorest | estimate |

**Spending as a check:** in a pre-industrial city the clothing need should take about a quarter of household spending
at King's prices. The coefficients are calibrated so the economy reproduces that share.

## 4. D34: the research field

The examples first given here were wrong: they named techs the buildings themselves require. They are withdrawn and
replaced by `d34_research_modifiers.md` (R33.1, M79), built from the tech tree with a checked rule.

## 5. The Masons condition for Notre Dame and the J.S. Bach Cathedral

**Facts:**
- Both wonders come with Architecture, as the Masons master guild does (`BUILDING_CORPORATION_33`, founding
  `CORPORATION_33`).
- The Masons guild hall is `BUILDING_GUILDHALL_33` (class `BUILDINGCLASS_GUILDHALL_33`, `PrereqCorporation`
  `CORPORATION_33`).

**Implementation:**
- Give both wonders `BuildingClassNeededs` = `BUILDINGCLASS_GUILDHALL_33` with `bNeededInCity` = 1. The city must
  have a Masons guild hall.
- This works both while the guild is a corporation, where the hall needs the guild in the city, and after D29 a makes
  the Masons national, where the hall comes with the national guild.
- **The AI** already reads `BuildingClassNeededs` when it values buildings (the engine's prerequisite check). So it
  sees the condition, and it values the Masons hall more where it wants these wonders. The hall's value for the
  wonder is to be checked in the AI's building valuation.

## 6. Plan changes

- **design.json:**
  - D33 decided;
  - D34 decided with the examples;
  - D35 (the record limit: no record-count limit below the font capacity; graphics paging for memory);
  - D29 updated (food guilds, Clerks, the Masons condition);
  - D28 clothing consumption.
- **plan.json:** FD.F1 gains `TechResearchModifiers`, `iBuildingProductionModifier` and the clothing fields.
