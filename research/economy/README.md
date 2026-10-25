# Land, not tokens: a design for land qualities and industry

[land-and-industry.pdf](land-and-industry.pdf) proposes replacing the point resources of the map with qualities of the
land: climate per plot (temperature, water, growing season, hemisphere), soil, geological provinces with ore grade and
depth, and the carrying capacity of the sea. Goods become quantities that are made, used up, stored and traded. Resource
types survive only as the names of goods, so the engine's existing resource paths keep working.

[settlement/](settlement/README.md) holds the quantitative follow-up: a deterministic model of settlement goods economies run on 30 real harness games.

It is a design, not a change: nothing in the mod is altered, and no prediction is registered for it.

## Files

| File | What it is |
|---|---|
| `tools/extract.py` | Reads the mod's terrain, feature, bonus, improvement, build, building and unit records and one WorldBuilder map into `data/facts.json` |
| `tools/figures.py` | The models (climate, suitability, seed spreading, mine depth, sea, goods network, stockpiles, prices, the whole loop) and every figure; writes `figures/` and `data/numbers.json` |
| `tools/build_pdf.py` | Builds the PDF from those; every number in the text is read from `data/` |

## Rebuilding

```sh
python3 tools/extract.py <mod checkout at GitLab main 3bec049> "<mod>/PrivateMaps/Earth 18 preset civs, Huge.CivBeyondSwordWBSave" data
python3 tools/figures.py .
python3 tools/build_pdf.py .
```

Needs numpy, matplotlib, reportlab and Pillow.
