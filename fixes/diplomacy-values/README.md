# Diplomacy: trade values from effects, offers by value

[`../diplomacy-values.patch`](../diplomacy-values.patch) applies to GitLab `main` `3bec049` (tree
`d92c68e1` after it) and serves P18 and P19, under hypothesis H10 (`method/mission/register.json`).
P16 and P17 were the same change without the loss check in `AI_considerOffer`. They were withdrawn
before any evidence, when building the change showed that gap.

## The faults

Facts from the code (`main` `3bec049`):
- **Offers were random.** `CvPlayerAI::AI_doDiplo` chose by `getSorenRandNum(10000)` among the
  partner's tradeable items:
  - the tech it asked to buy, to swap or as help;
  - the tech it gave in a swap and the tech it sold;
  - both resources in a swap.
- **Techs were priced from the raw cost.** `CvTeamAI::AI_techTradeVal` priced a tech at 1.5 × its
  remaining `getResearchCost`, plus up to 0.5 × for teams lacking it. The receiver's research
  modifier was left out: `TECH_DIFFUSION_ENABLE` is 1 and gives up to +30% from known teams, and
  the known-prerequisite modifiers are 15.
- **Resources were valued by fixed weights.** `CvPlayerAI::AI_bonusTradeVal` took
  `AI_baseBonusVal`: +100 per happiness or health, half a point per percent of a building's
  `BonusYieldModifiers`. It scaled that by the smaller of the two players' city counts. The
  cities' unhappiness, unhealthiness, production and commerce never entered.
- **Examples from the records** (`BuildingInfo`):
  - `BUILDING_TOWN_ESSENTIALS` (Masonry, cost 70): Coffee [0, 20, 10];
  - `BUILDING_FORGE` (Metal Casting): Gold [0, 0, 25], Silver [0, 0, 15];
  - `BUILDING_MARKET`: `CommerceModifiers` [20].
- **The AI's own loss was not weighed.** `AI_considerOffer` valued what the AI gives only as the
  partner values it.
- **The whole treasury could go.** `AI_maxGoldTrade` let an AI with non-negative income trade all
  its gold, without regard to `AI_goldTarget`.

Facts from the user's game 4 (deal and diplomacy lines of `WarLog.log`, the AI opening each deal):
- Turn 264: AI 2 paid 520 gold for Archery, from 874.
- Turn 267: AI 13 paid 380, from 388.
- Turn 268: AI 11 paid 660 for Fermentation, from 697.
- Turns 254–285: AIs paid the human 2,545 gold, against the human's own income of 4,238 gold.

## The change

`AI_DIPLOMACY_FLAGS` (`BBAI_AI_Variables_GlobalDefines.xml`, default 15; 0 is the old AI):

| Bit | Change |
|---|---|
| 1 | `AI_techTradeVal` divides the remaining research by the receiver's `calculateResearchModifier` |
| 2 | `AI_bonusTradeVal` from `AI_bonusCityValue` (effect in its own cities, as gold per turn) and `AI_bonusUnlockVal` (units, buildings, routes; scaled by its own city count); `AI_considerOffer` makes a new deal cover the AI's loss |
| 4 | offers in `AI_doDiplo` by value (`AI_techOfferValue`), no tech sales to a higher-ranked team, resource swaps only for a gain greater than the loss |
| 8 | AI-proposed tech purchases pay at most `getGold() - AI_goldTarget()` |

`AI_baseBonusVal` is unchanged, so settlement, workers and research decide as before. Nothing new
is saved. `Docs/DIPLOMACY_VALUES.md` on GitLab describes the rules for players.

## Validation

- **Build:** MSVC 2003 release `c123133807f4`, 0 errors and 0 warnings.
- **Clang gate:** 0 new diagnostics on `CvPlayerAI.cpp`, `CvTeamAI.cpp` and `CvGameCoreUtils.cpp`
  ([clang-gate.log](clang-gate.log)).
- **Patch:** `apply.py` on a clean `3bec049` gives tree `d92c68e1` ([manifest.json](manifest.json)).
- **Switch off:** with `AI_DIPLOMACY_FLAGS` 0, the harness game is identical to build
  `504830a0dee0`'s in all 151 turn lines, timings aside.
  - Setup: Mediterranean Standard, Normal speed, seed 777, 150 turns.
  - `HARNESS_DEFINES` does not reach scenario runs (it is applied in the graphics setup), so the
    switch was set in the mod's XML.
- **P18 and P19 evidence:** pending.
- **In game:** not yet tested.
