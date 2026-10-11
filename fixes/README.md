# Tested source fixes

## Opening development and settler voyages

[0005-opening-settler-voyages.patch](0005-opening-settler-voyages.patch) targets
**clean GitLab `19e4d59e0a8fc5dc138de5108d8e921e95d28ba1`**. GitLab advanced during
this investigation: that revision already includes the previous runtime fixes.
Use this patch on the new base; do not stack the historical patches below.
It also restores their regression tests, which the new upstream commit omitted.

The [investigation and algorithm](../research/transport/README.md) cover why
settler ships can stall: incompatible role gates, optional loading reservations,
per-hull/group confusion and destination selection that ignores sailing time.
The replacement assembles a party, compares delivery routes, commits a site,
sails without waiting for optional cargo, and keeps the landing party together.
Opening work boats/workers are considered before the first-garrison branch.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/voyages-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/voyages-manifest.json
```

Then run `python3 Tools/run_regression_suite.py` in the source checkout and
rebuild the Windows DLL. The helper verifies the clean base and hashes, then
applies **and stages** the source changes. Save format 6 is unchanged.

Validation: **19 regression programs pass**, including six new opening/transport
tests. The native probes execute production fragments using C++03, warnings as
errors and fatal UBSan. See the [manifest](voyages-manifest.json),
[suite output](voyages-regression.log), and [application verification](voyages-patch-validation.log).
A clean application must reproduce source commit `a9003cae719e69456e698905d44a28a4f508199a`.

**No full DLL build or BTS replay was performed.** Distant pickup, idle-fleet
demand, persistent retry limits and engine scheduling remain explicit validation
or implementation work. Runtime commits have not been pushed to GitLab.


## Carthage autoplay coordination

[0004-autoplay-coordination.patch](0004-autoplay-coordination.patch) is the historical
**cumulative** patch for clean GitLab source at
`5e6d03591731f64d589661f4f329aa28e8c71a7d`. It includes all of patch 0003 below;
apply 0004 directly to that base, not on top of 0003.

The new changes correct resource replacement under safe automation, reversed
resource build-time selection, four-slot settler transport escort gates, duplicate
queued-unit accounting, and a settler danger branch that failed to return after
skipping. Runtime edits remove another 22 net lines after the earlier cleanup.
The [investigation](../research/autoplay/README.md) distinguishes these defects
from unresolved settlement, fleet demand, civic and opening-production questions,
and supplies the next simulation scenarios.

From this GitHub checkout:

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/autoplay-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/autoplay-manifest.json
```

This verifies the exact revision, clean state, patch checksum and file digests,
then applies **and stages** the source changes. Run the suite in the source
checkout, then rebuild the Windows DLL to use the fixes in-game:

```sh
python3 Tools/run_regression_suite.py
```

Validation: **8 new tests pass; 7 reject the upstream source**, while the XML
control already passed. All **17 regression programs pass**. See the
[before-fix failures](autoplay-before.log), [fixed suite](autoplay-regression.log),
[manifest](autoplay-manifest.json) and [application checks](autoplay-patch-validation.log).
Native probes execute production methods/fragments in C++03 with fatal UBSan
and narrow adapters. A clean application reproduces tested source commit
`4b730c2cda091e25237d4ed418fddeefe562cbff` exactly.

No full DLL build, game replay, XML balance change or save-layout change is
claimed. The user compiled the reported autoplay DLL from current GitLab source;
it is distinct from the older bundled binary. These source commits have not
been pushed to GitLab. The raw uploaded save remains local.

## Current source cleanup

Patch 0003 remains available separately; its changes are included in 0004 above.

GitLab `main` was reviewed at
[`5e6d035`](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/commit/5e6d03591731f64d589661f4f329aa28e8c71a7d).
It already contains the original correctness fixes and newer supply, career and
reserve corrections. The older patches below are historical; do not apply them
over this revision. In particular, GitLab has superseded patch 0002's unsafe
distance shortcut and added further career/reserve handling.

[0003-current-source-cleanup.patch](0003-current-source-cleanup.patch) builds on
that current source. It removes **291 net runtime-source lines**:

* Delete the disabled centralized-production stub, caller and declarations.
* Remove abandoned commented building valuations and obsolete event code.
* Share load/start initialization while preserving profiler and lookup order.
* Collapse Crusade spawning to one call with the existing cadence and city order.
* Correct two reserve-arithmetic edge cases: overflow in the fractional remainder
  and premature clamping before speed scaling. Supply-demand, military operation,
  general-loss and save read/write bodies remain unchanged.

The earlier reserve code left 926,258,177 gold available in a case whose exact
result is 500,000,000; an extreme percentage also triggered UBSan. See
[the reproduced failures](current-reserve-before.log).

From this GitHub checkout, against a clean GitLab checkout at exactly `5e6d035`:

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/current-source-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/current-source-manifest.json
```

The helper verifies base revision, clean state, patch checksum and file digests;
it applies and stages the patch. Run `python3 Tools/run_regression_suite.py` from
the source checkout. Omitting `--manifest` still selects the original patch below.

Both the [upstream baseline](current-upstream-regression.log) and
[updated source](current-cleanup-regression.log) pass all **16 regression programs**.
Updated checks include 4,352 reserve cases against an independent exact-integer
oracle, 70 Crusade boundary scenarios, and load/start ordering. Native arithmetic
tests use C++03 and fatal UBSan checks. [Structural checks](current-cleanup-structure.log)
verify the removal's scope and preservation of the new upstream operation logic.
The [manifest](current-source-manifest.json) records all changed file digests;
[application validation](current-patch-validation.log) checks the staged tree
against the tested source commit.

This patch is source commit `a95a654dab1613f611592dd91b873358c1830d9e`, represented
here as an apply-ready diff. It has not been pushed to GitLab. There is no DLL
build or BTS engine run, and no additional save-format change beyond version 6.

## Historical source-correctness patch

These patches fix six groups of source defects against GitLab revision
`1ab4f99a76adb530f86b278390ab8139ef41cc96`. They have been applied and tested in
the source checkout. This GitHub repository holds the apply-ready patch, its
checksummed manifest, an application helper, and validation logs; it does not
contain a replacement game DLL or the full mod assets.

| Fix | Previous behavior | Updated behavior |
|---|---|---|
| Canal utility | Value was never positive, excluding canal-only worker candidates | Water areas larger than two tiles can contribute positive utility; existing legality guards remain |
| Fort selection | Last candidate overwrote location utility; slower equivalent builds won | Choose the shortest legal base build time, retain location utility, preserve native tie order and safely scale large scores |
| Agenda persistence | Load discarded history used by hysteresis and strategic consumers | Save format 6 records the incumbent, score, cadence, bad-start state, intent and budgets |
| Load/start mappings | Reusing a Python manager appended another 83 upgrade pairs | Rebuild fresh paired arrays and publish them only after successful lookups |
| Sparse cities | World Bank and Crusade effects missed cities beyond empty ID slots | Iterate actual cities; check the no-obsolete-tech sentinel before querying a technology |
| Team rollover | A dead team zero prevented later teams from being activated | Skip dead slots and activate the first living team |

The patch also removes the unused `AI_CIVIC_ECONOMIC_HORIZON_TURNS` XML define,
replaces a regression's dependency on a deleted comparison document with a live
city/agenda integration check, and updates the existing save-version assertion.
The economic regression assertion and old operation-record tests remain active.

## Apply and validate

Use a clean source checkout at the exact base revision. From this GitHub checkout:

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --check
python3 fixes/apply.py /path/to/rise-of-mankind
```

The helper verifies the patch checksum, source commit, clean working tree and
every original file digest. It then applies **and stages** the changes and verifies
every resulting file against the tested digest. It does not commit, push, rebuild
the DLL, overwrite local work, or accept a second application over staged changes.
Review and test from the source root:

```sh
git diff --cached
python3 Tools/test_review_correctness.py
python3 Tools/run_regression_suite.py
```

Python 3 and `g++` with C++03/UBSan support are required. The source patch is also
available directly as [0001-source-correctness.patch](0001-source-correctness.patch).
Its application installs `Docs/SOURCE_CORRECTNESS_FIXES.md` with source-side notes.
The [manifest](manifest.json) records the tested source commit and before/after
digests. The local source commit is represented by the patch; it has not been
pushed to GitLab.

## Evidence

* **Original source:** nine of ten new targeted tests reject it; the obsolete-bank
  control already passes. See [baseline-targeted.log](baseline-targeted.log).
  Three expected native assertion aborts appear as unittest errors, not failures
  from a running game.
* **Fixed source:** ten targeted tests pass; the full suite passes **15 of 15
  isolated regression programs**. See [fixed-regression.log](fixed-regression.log).
* **Published patch:** the application helper's dry run, application, refusal to
  overwrite staged work, file digests and full suite are checked again on a clean
  local clone of the original revision. See [patch-validation.log](patch-validation.log).
  The validation checkout omits unrelated assets through sparse checkout; no game
  runtime is inferred from this check.

The native tests compile actual methods/fragments with undefined-behavior
sanitization. Python tests execute actual handler bodies and the production city
iteration wrapper under narrow adapters. The save test covers extension stream
alignment, every new field, old-version defaults and preserved agenda hysteresis.
These tests do not constitute a full Windows DLL build, embedded Python 2 run or
real BTS save-file round trip.

## Compatibility and remaining work

**Version-6 saves require a rebuilt DLL with this source change. Older DLLs cannot
safely read them.** The new reader retains the old defaults for versions 0–5;
it cannot reconstruct agenda history that an old save never contained. Keep the
original saves when testing a new build. The bundled older DLL remains unchanged.

Fort selection now obtains required canal/airbase access using the shortest base
build time. It does not optimize defensive upgrades or total worker travel and
construction time. Restored positive canal scores need engine scenarios to assess
strategic quality beyond eligibility.

D04's research heuristic overcounting remains open: correcting shared AND/OR
prerequisites requires a defined package-search objective and bounded-cost
implementation. Unresolved XML callbacks, profiler schema issues and suspected
cache/pathfinding behavior also remain in the assessment backlog. The historical
review and its reproduction scripts still describe the original pinned source.

## Historical operation-supply patch

**Superseded by current GitLab source.** Retained with its original bytes for
provenance; use the current-source cleanup instructions above for `5e6d035`.

[0002-operation-supply.patch](0002-operation-supply.patch) is independent of the patch above. The hunks do not overlap, so either order works on revision `1ab4f99a76adb530f86b278390ab8139ef41cc96`. It does not change the save format, and `fixes/apply.py` does not install it.

```sh
git apply fixes/0002-operation-supply.patch
python3 Tools/test_operation_supply.py
```

sha256 `fb4deb2b3563eaa7a1169ff66b4ab812f246b2127ac2fe0e5da1015be23a2a52`. Context lines keep the CRLF bytes of `AIDecisionPolicy.h` and `CvPlayerAI.cpp` (`fixes/*.patch` is marked `-text`). If a checkout has rewritten those files to LF, use `git apply --ignore-whitespace`. The same bytes are also in [0002-operation-supply.patch.b64](0002-operation-supply.patch.b64) so a mangled line ending can be detected and restored with `base64 -d`.

| Fix | Previous behavior | Updated behavior |
|---|---|---|
| Field supply | An operation stack not standing on this player's land published zero replacement demand | `supplyReachable` rejects only stacks outside the logistics horizon; neutral and enemy ground still create demand; the existing safe-path check remains |
| Dead commander | `AI_rememberGeneral` returned when the unit was already gone, so an erase path dropped the career | The career is stored anyway. A later live unit copies it only with the doctrine badge |
| Gold hurry reserve | `-calculateGoldRate()` times the speed runway can negate `INT_MIN` or overflow signed 32-bit | `deficitReserve` returns 0 for a non-negative rate and saturates otherwise |

Four tests passed: three source contracts and one C++03 program compiled with `-Wall -Wextra -Werror`. This is not a Windows DLL build. Free `initUnit` generals and the immediate return in `AI_doCentralizedProduction` are unchanged on purpose. A successful 60–90% "AI General Survival" respawn still overwrites the dead unit id without calling `AI_rememberGeneral` first, so that death does not enter the career table. `AI_maxGoldTrade` still computes `-calculateGoldRate() * 12` and can overflow the same way; that call site is not in this patch.
