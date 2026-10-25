# Civilopedia prose and localization fixes

[Patch 0020](../0020-pedia-localization.patch) applies to GitLab main
[`2a8b9a83`](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/commit/2a8b9a83eb5b4d339cb92d23d04155e47e868efa),
rechecked before publication. This is a proposed patch; it has not been submitted to or merged on GitLab.

The patch updates **40 text values in five XML files**: Civilopedia and strategy entries
for Trade, Peasantry, School of Scribes and River Port, in English, French, German,
Italian and Spanish. River Port's background was a single period. The new background
paragraphs describe trade networks, village agriculture, scribal training and river
transport. Strategy advice follows the current mechanics, including the additional
River Port route and replacement of older buildings by Library and Harbor.

It also restores positional language order in two Siam entries:
`AI_DIPLO_FIRST_CONTACT_LEADER_MONGKUT_1` and `TXT_KEY_CIV_SIAM_PEDIA`.
Their language contents are preserved. The loader selects language siblings by index.

## Apply to the game source

From a checkout of the pinned GitLab revision, with the patch downloaded locally:

```sh
git apply --check /path/to/0020-pedia-localization.patch
git apply /path/to/0020-pedia-localization.patch
```

Download the raw patch without re-encoding it: it preserves the original XML encodings
and CRLF line endings. No DLL rebuild is required. Restart the game with a fresh text
cache and inspect the affected pages, tooltips and languages before release.

## Evidence and validation

- [Exact old/new translations](changes.json).
- [Validation results and patch checksum](validation.json).
- Patch applied successfully in a fresh index of the latest fetched GitLab main; all
  five resulting files exactly match the reviewed XML files.
- All 40 updated values round-trip through XML parsing. Language-order audit findings
  fall from two to zero; placeholder-review findings stay at 107, with no new flags.
- Text keys, unrelated entries, untouched languages, encodings and line endings are
  preserved. One existing trailing space on an edited line was removed.

Rules were checked in `CIV4CivicInfos.xml` (Peasantry), `CIV4TechInfos.xml` (Trade),
`CIV4BuildingInfos.xml` (School of Scribes and River Port), and the replacement lists
in `RoMEventManager.py`. Historical prose does not imply additional simulated mechanics.

In-game rendering has not been tested. Native-speaker terminology review remains
useful. The other six language slots retain their existing values. Duplicate-key
precedence and Peasantry's improvement-growth integer truncation are separate issues;
this patch changes no gameplay arithmetic and promises no maturation acceleration.
