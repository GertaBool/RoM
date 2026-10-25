# The Living Economy: the complete design

[living-economy.pdf](living-economy.pdf) describes the economy of Rise of Mankind as one finished system rather than a set
of separate changes: land with climate, soil, ore and sea; citizens with occupations; one ledger of goods per city that
every flow passes through; living standards in four tiers; recipes, tools and power; markets with prices from scarcity;
trade by networks, convoys and contracts; civics as levers on the ledger; armies built and supplied from goods; and the
AI valuing goods by their marginal effect. Food, production and commerce remain, as views of the ledger, so the
interface, growth rule, build queue and sliders keep working.

It also lists what is cut, replaced and kept, the engine classes and functions that change, a build order in six
milestones on one branch, and the risks.

Every number in it is read from the two earlier studies: [Land, not tokens](../land-and-industry.pdf) (`../data/`) and
[Settlement Economy](../settlement/README.md) (`../settlement/data/`), including the need levels that
`settlement/tools/calibrate_needs.py` solves from design targets. It is a design, not a change: nothing in the mod is
altered, and no prediction is registered for it.

| File | What it is |
|---|---|
| `tools/vision.py` | The figures (`figures/`) and the PDF |

## Rebuilding

From `research/economy`, after the two studies:

```sh
python3 vision/tools/vision.py .
```

Needs numpy, matplotlib, reportlab and Pillow.
