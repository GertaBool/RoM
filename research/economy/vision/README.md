# The Living Economy: the complete design

[living-economy.pdf](living-economy.pdf) describes the economy of Rise of Mankind as one finished system rather than a set
of separate changes: land with climate, soil, ore and sea; citizens with occupations; one ledger of goods per city that
every flow passes through; living standards in four tiers; recipes, tools and power; markets with prices from scarcity;
trade by networks, convoys and contracts; civics as levers on the ledger; armies built and supplied from goods; and the
AI valuing goods by their marginal effect. Food, production and commerce remain, as views of the ledger, so the
interface, growth rule, build queue and sliders keep working.

Food keeps the engine's rule: a city eats first, grows from its surplus and loses a citizen only when its food box is
empty. What is new is that the box can rot, at rates set only by the preservation technologies the owner lacks (Pottery,
Fermentation, Refrigeration). Every good is counted in whole tons (one unit of food yield is 100 t), in integers sized
from bounds in the records so they cannot overflow; living standards are counted in whole citizens supplied.

It also lists what is cut, replaced and kept, the engine classes and functions that change, a build order in six
milestones on one branch, and the risks.

Every number in it is read from the growth runs of this folder (`data/`) and from the two earlier studies: [Land, not tokens](../land-and-industry.pdf) (`../data/`) and
[Settlement Economy](../settlement/README.md) (`../settlement/data/`), including the need levels that
`settlement/tools/calibrate_needs.py` solves from design targets. It is a design, not a change: nothing in the mod is
altered, and no prediction is registered for it.

| File | What it is |
|---|---|
| `tools/food_facts.py` | The records food rests on: the three preservation techs, what names them, food kept, growth defines, the calendar; `data/food_facts.json` |
| `tools/tech_turns.py` | The earliest turn each player of the 30 games could have known each preservation tech (a bound from tech counts); `data/tech_turns.json` |
| `tools/bounds.py` | An upper bound on one city's food harvest from the records, to size the integers; `data/bounds.json` |
| `tools/growth.py` | The food rule in tons on the 30 games' cities, with size following the food box, by preservation level; `data/growth.json` |
| `tools/vision.py` | The figures (`figures/`) and the PDF |

## Rebuilding

From `research/economy`, after the two studies (`<mod>`: the mod checkout; `<runs>`: the P18 baseline run folders):

```sh
python3 vision/tools/food_facts.py <mod> vision/data
python3 vision/tools/tech_turns.py <mod> vision/data <runs>/s*
python3 vision/tools/bounds.py <mod> .
python3 vision/tools/growth.py .
python3 vision/tools/vision.py .
```

Needs numpy, matplotlib, reportlab and Pillow.
