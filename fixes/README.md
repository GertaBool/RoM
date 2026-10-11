# Tested source fixes

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

## Operation supply

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
