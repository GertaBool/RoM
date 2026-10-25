# Civic prose and translation polish

Patch 0021 reviews all **68 core civics**, updating **942 localized text values** in two text XML files. It follows [patch 0020](../0020-pedia-localization.patch) on GitLab revision [`2a8b9a83`](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/commit/2a8b9a83eb5b4d339cb92d23d04155e47e868efa). GitLab main was checked again and remains at that revision.

## What changed

- **67 Civilopedia entries rewritten.** Short historical paragraphs replace name-only entries, slogans and misleading generalizations. Peasantry retains its already revised background from patch 0020.
- **59 strategy entries rewritten.** Advice follows the current rules and highlights useful conditions or trade-offs. Peasantry retains the previous correction. Eight civics have no Strategy key in the game rules; their new background text is supplied without changing rule XML to introduce new fields.
- **68 civic labels reviewed** in English, French, German, Italian and Spanish. Established English names remain, with capitalization normalized in four labels; other languages receive fitting localized labels.
- **Every existing copy of affected duplicate keys updated** in those five languages. No duplicate declarations were deleted or language blocks reordered.

The prose distinguishes oral tradition, written records, accounting and bookkeeping; treats barter as one of several forms of exchange; separates standing armies from professional military careers; and describes institutions without presenting their names as sufficient explanations. Historical passages on slavery, colonialism and National Socialism describe coercion and harm directly. Background imagery is not a claim that additional mechanics are simulated.

## Gameplay corrections

Several old passages contradicted current XML:

| Civic | Old advice | New advice |
| --- | --- | --- |
| Oligarchy | Claimed commerce and trade-gold bonuses | Explains recruit experience, palace happiness and distance maintenance |
| Priesthood | Claimed three free specialists | Explains priest assignments and capital research/culture, with city-count maintenance |
| Corporate | Claimed better health and research | Explains production, gold and corporation benefits alongside health and large-city happiness penalties |
| Caste | Claimed Great People/culture penalties and fishing-boat benefits | Explains current health, military production, selected improvements and slower workers |
| Public Schools | Claimed a research bonus | Explains production and free specialists alongside health and upkeep costs |
| Planned | Claimed trade cannot exist in a planned economy | Uses historical context in the pedia and distinguishes the actual corporation restriction in strategy |

No gameplay values, prerequisites, Python callbacks, C++ code or text keys change. Numeric effects remain in generated help. Strategy paragraphs are selective advice, not exhaustive effect inventories or claims of optimal play. Civic names and their effects need not correspond to a historical causal model.

## Read and apply

- [English preview of all civics](PREVIEW.md)
- [Exact localized before/after text](changes.json)
- [Per-civic coverage](coverage.json)
- [Rule evidence from the pinned source](rule-evidence.json)
- [Validation results and checksum](validation.json)
- [Download patch 0021](../0021-civic-prose.patch)

Apply the raw patch to a game-source checkout **after patch 0020**:

```sh
git apply --check /path/to/0021-civic-prose.patch
git apply /path/to/0021-civic-prose.patch
```

The GitHub repository hosts the patches and research; apply them to the separate GitLab game repository. Preserve the raw patch bytes because the original text files use legacy encodings and CRLF line endings. No DLL rebuild is needed.

## Validation

All target keys were found, all five-language values round-trip through XML parsing, and duplicated target definitions agree. Original encoding, line endings, element order, other languages and unrelated entries were preserved. A temporary Git index verifies that 0020 followed by 0021 produces exactly the reviewed files. The whole-text audit found no new placeholder, color or language-order flags; placeholder review candidates decrease from 107 to 105.

The source civic rules match the version used for the economic research. `rule-evidence.json` records the corresponding rule values and locations; Barter's Market discount additionally comes from `Assets/Python/RoMGameUtils.py`.

In-game rendering, label clipping and native-speaker terminology review remain untested. Restart with a fresh text cache and check the civics advisor and Civilopedia in all five languages before release. The six other language slots retain their previous content. The separate improvement-maturation arithmetic issue remains unchanged.
