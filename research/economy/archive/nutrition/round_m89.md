# Fruit and drinks: a different priority, the same satiety (R43, M89, M90)

*Withdrawn in M91: there is no priority tier. Fruit and drinks enter one allocation with their own values (`round_m91.md` section 4).*

## Recorded

- **M89:** "Fruit are not for satiety but well-being, the same goes for many drinks."
- **M90:** "Fruit does provide satiety as well, I am just saying there is a different set of priorities."

## The change in the food model (`plan/tools/food_model.py`)

**Well-being goods:** fruit (Apple, Banana, Lemon) and the drinks wine and beer (Wine, Alcohol); tea and coffee, which were already taken first for their caffeine.

**Their priority:** they are taken for well-being, up to their own ceilings, before the satiety order:
- fruit: one watermelon in all, 4,518 g;
- tea and coffee: up to 600 mg caffeine;
- wine and beer: as much as there is.

**What they give is unchanged:**
- their energy counts toward the energy ceiling and the food sufficiency `x`;
- their satiety, protein, nutrients (vitamin C, potassium) and drink count as for any good.

They no longer compete in the satiety ranking.

**The foods** (staples, meat, fish, dairy) then follow in order of quality, satiety × (1 + nutrient density), and fill the energy room that is left.

## The cities, rerun

| City | Eaten, in order | Energy eaten / need | Left over |
|---|---|---|---|
| A. Market town | apples 205 g, beer 411 g, milk 548 g, pork 82 g, bread grain 959 g | 3,464 / 3,193 | nothing |
| B. Coastal city | tea 8 g, bananas 205 g, fish 479 g, rice 1,027 g | 3,306 / 3,025 | nothing |
| C. Industrial city | coffee 8 g, potatoes 1,644 g, beef 110 g, milk 685 g, wheat 603 g, sugar 82 g | 3,600 / 2,916 | nothing |
| E. Rich city | apples 548 g, wine 411 g, potatoes 1,644 g, beef 548 g, milk 2.0 L (energy ceiling) | 3,685 / 2,711 | milk 77,031 t (spoils), wheat 40,000 t, sugar 8,000 t |

**What changed:**
- **The rich city:** it now drinks its wine (before, the energy ceiling left no room for it) and drinks less milk.
- **Vitamin C:** fruit is always eaten while there is any, so a rich city does not go short of vitamin C because its staples filled the energy room first.
- **Poorer cities (A, B, C):** nothing changes, because all their stock is eaten in any order.

## Open

- **Well-being as an output:** fruit, wine, beer, tea and coffee eaten per head could feed the happiness line (the engine's happy faces), as luxuries do today. The rule (for example one happy face per good above a daily amount) is still to be proposed.
