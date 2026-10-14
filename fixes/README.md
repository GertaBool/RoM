# Tested source fixes

## Autorun fixes: endless turn, turn time, settlers and AI economy

[0012-autorun-fixes.patch](0012-autorun-fixes.patch) is the current incremental patch for
GitLab **`main` at `dcbae97`** (patch 0011 and its documentation follow-up). It has
**landed on GitLab `main`** ([!37](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/37),
merge commit `abf8471`, tree `c56ade12` = the tested tree). A clone of current `main`
needs nothing applied; only the DLL below has to be installed.

It answers the autorun report as Masinissa (Marathon save at 410 BC, game turn 269).
Everything was checked by loading that save into the real DLL in the
[headless harness](../toolchain/harness/README.md) and playing on with every seat on AI.

- **"Waiting for other players" forever.** A lone Javelineer with a worker job pathed onto
  a tile holding an enemy unit. `groupMove` put it into a new group on every update slice
  and the player's unit loop stopped at it, so the turn never ended, also after reloading.
  `groupPathTo` now ends a mission no unit can step on, the worker searches skip tiles
  with visible enemies, and a watchdog ends the moves of a unit that keeps losing its
  group. Before: turn 269 never ends. After: turns 269 to 299 played.
- **Turn time** (turns 270 to 279): 9.6 s per turn on every build since `d8cedd5`, 2.6 s
  now. `pathValid` remembers its parent-plot tests per expansion, exploration searches
  candidates best bound first and skips plots out of range (both exact: identical game
  state), upgrade reachability is cached, and trade denial is tested last.
- **Settlers.** Settlement sites count only if a settler can be delivered there from its
  region (own or unclaimed land; sea reached by a transport the player can build).
  Settlers with nothing deliverable are disbanded after max(20, scaled 10) turns, lone
  settlers recruit a spare defender, a transport at sea without escort returns to port,
  and a city with a waiting settler builds a boat when only overseas sites remain.
  Chronic idle settlers: 8 without the changes, 3 with.
- **Buildings and technologies.** Cities that cannot train a city-defence unit (no
  Archery or Bronze Working) trained Spearmen at every decision, because Spearmen never
  count as garrison; they now do in that case. `AI_goldTarget` scaled slow speeds twice
  and hoarded gold at low research. Over 30 turns: research +21 %, 100 techs against 79,
  347 buildings against 238.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/autorun-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/autorun-manifest.json
```

**27 regression programs pass.** The DLL is built with MSVC 2003: 0 errors, 0 warnings,
the same 2451 exports. Use [`builds/0012/CvGameCoreDLL.dll`](../builds/0012/CvGameCoreDLL.dll);
the save format is unchanged. The game executable was not run.

[Investigation](../research/autorun-masinissa/README.md) · [Manifest](autorun-manifest.json) ·
[Before](autorun-before.log) · [Suite](autorun-regression.log) ·
[Patch verification](autorun-patch-validation.log) · [Clang gate](autorun-clang-gate.log) ·
[Build provenance](../builds/0012/provenance.json).

## Settler landing: escorts at sea

[0011-settler-landing-escort.patch](0011-settler-landing-escort.patch) is the previous
incremental patch for GitLab **`main` at `86af2ab`** (patch 0010 merged). It has **landed on
GitLab `main`** ([!36](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/36),
merge commit `9b6c47c`, tree `2f144cfd` = the tested tree), followed by a documentation-only
correction (`dcbae97`). Its DLL is superseded by [`builds/0012`](../builds/0012/CvGameCoreDLL.dll).

It fixes the reported failure: the galley sailed to the tile in front of the site and
stayed there with the settler and escort aboard. Patch 0008 did not fix this.

- **Escort at sea.** `AI_settlerSeaTransport` recognised the escort with `canDefend()`,
  which tests the unit's own plot. A land unit aboard a ship at sea cannot defend water,
  so the ship never had an escort and skipped every turn (`MISSING_ESCORT_OR_CAPACITY`).
  It now uses `canFight()`.
- **Landed party.** `CvUnit::setXY` puts each unit leaving a ship into a new group. The
  escort now rejoins the settler, and the group gets its founding destination back.
- **Tests.** The landing tests' stand-ins now behave like the engine on both points.
  Against the previous source 9 of 14 cases fail.

The fix was checked by running the real DLL headlessly
([toolchain/harness](../toolchain/harness/README.md)). Before: the galley waits next to
the site for 28 to 29 turns and no city is founded. After: the party lands on turn 2 or 3
and founds the next turn.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/landing-escort-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/landing-escort-manifest.json
```

**24 regression programs pass.** The DLL is built with MSVC 2003: 0 errors, 0 warnings,
the same 2451 exports ([`builds/0011/CvGameCoreDLL.dll`](../builds/0011/CvGameCoreDLL.dll), superseded);
the save format is unchanged. The game executable was not run.

[Investigation](../research/landing-engine/README.md) · [Manifest](landing-escort-manifest.json) ·
[Before](landing-escort-before.log) · [Suite](landing-escort-regression.log) ·
[Patch verification](landing-escort-patch-validation.log) · [Build provenance](../builds/0011/provenance.json).

## Pathfinding, transport and siege

[0010-pathing-transport-and-siege.patch](0010-pathing-transport-and-siege.patch) is the
previous incremental patch for GitLab **`main` at `a9b1fce`** (patch 0009 merged). It has
**landed on GitLab `main`** ([!35](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/35),
merge commit `86af2ab`, tree `147f6d1f` = the tested tree). Its DLL is superseded by
[`builds/0011`](../builds/0011/CvGameCoreDLL.dll).

- **Path searches stay reusable.** Queries about other groups (`AI_cityTargetUnitsByPath`,
  `AI_unitTargetMissionAIs`, `AI_isPlotThreatened`, synchronized landings, ship searches
  for coastal attacks) ran on the planner's A* and discarded its incremental search. They
  now use a second finder. Reuse is admitted only for the same group, membership, turn
  and moves, because the engine checks only the start plot and flags. The threat check
  searches each enemy group once, not once per unit.
- **Escort and stack grouping.** `AI_group` was Θ(candidates × groups) per call; a
  unit-target index answers repeated queries. A `MAX_INT + 1` overflow counted
  unreachable groups as "joining soon" for waiting transports.
- **Decisions.** `AI_choke` used the last reachable plot instead of the best. Synchronized
  landings ignored their own "can the cargo fight there" check. Workers compared raw value
  against value per turn. A settler whose escort fell on arrival walked home instead of
  founding.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/pathing-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/pathing-manifest.json
```

**24 regression programs pass**. The 13 new test cases all fail on unmodified `main`.
The DLL is built with MSVC 2003: 0 errors, 0 warnings, exports identical to the shipped
DLL. Use [`builds/0010/CvGameCoreDLL.dll`](../builds/0010/CvGameCoreDLL.dll); the save
format is unchanged. The game executable was not run.

[Investigation](../research/pathing/README.md) · [Manifest](pathing-manifest.json) ·
[Before](pathing-before.log) · [Suite](pathing-regression.log) ·
[Patch verification](pathing-patch-validation.log) · [Build provenance](../builds/0010/provenance.json).

## Turn time and research planning

[0009-turn-time-and-research-planning.patch](0009-turn-time-and-research-planning.patch)
is the previous incremental patch for clean GitLab **`d8cedd551212c9a769230d66c219860c901798dd`**,
which already contains 0008's runtime change. It has **landed on GitLab `main`**
([!34](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/34), merge commit
`a9b1fce`, tree `e3cbb9a8` = the tested tree). A clone of current `main` needs nothing applied.

- **Defects from compiling the whole DLL**: the executive-value assignment and self-count,
  25 constant `Write(&field)` calls, No Tech Brokering reading uninitialized research,
  team/player ID mix-up in event messages, stale pickup path turns, the danger-guard
  precedence, always-taken bad-feature odds, objects passed to variadic logging, the
  self-initialized `CyGameTextMgr` member and double-counted settlers.
- **Turn time**: `AI_plotTargetMissionAIs` uses an epoch-invalidated plot index. A whole-map
  scan drops from Θ(plots·groups) to Θ(plots+groups), with identical results.
  `findPathLength` no longer expands the prerequisite tree (up to 1.09·10⁹ calls).
  Python cost callbacks no longer scan cities or search tables per query.
- **Research planning**: one minimum-cost AND/OR plan is shared by `pushResearch`,
  `findPathLength` and `AI_bestTech`. All 44,396 tested plans are proved optimal, and
  none costs more than the old queue rule.
- **Feature**: technology help shows the plan's size, beakers and turns.
- **Python rules**: corrected Corporate, Fortification-castle and Replicators prices,
  and the Observatory/Djenne radius.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/turn-time-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/turn-time-manifest.json
```

**21 regression programs pass**. Upstream had 16 programs with 4 stale failures,
whose 0008 assertions this patch restores. Four new programs cover the static
findings, the mission index, the Python callbacks and the research plan. The DLL is
built with MSVC 2003: 0 errors, 0 warnings, exports identical to the shipped DLL.
Use [`builds/0009/CvGameCoreDLL.dll`](../builds/0009/CvGameCoreDLL.dll); a
[baseline build](../builds/d8cedd5-baseline/) of unmodified `d8cedd5` is there for A/B
comparison. The save format is unchanged. The game executable was not run.

[Investigation, math and interaction audit](../research/turn-time/README.md) ·
[Manifest](turn-time-manifest.json) · [Before](turn-time-before.log) ·
[Suite](turn-time-regression.log) · [Patch verification](turn-time-patch-validation.log) ·
[Build provenance](../builds/0009/provenance.json) · [Toolchain](../toolchain/README.md).

## Settler landing

[0008-settler-landing.patch](0008-settler-landing.patch) is the earlier incremental
fix for clean GitLab **`b8c379c1ffad9cd5408ca0e43dca88daf8ba85ee`**. That revision
already includes patch 0007's runtime changes; do not reapply older patches.

The civilian dispatcher now hands the last shore step directly to its selected
settler/escort group, preserves `MISSIONAI_FOUND`, and prevents unrelated or
immobile cargo from blocking a ready party. Busy parties wait, failed landing
paths request recovery, and passenger IDs are rechecked after movement callbacks.
Shared military amphibious logic, save layout and XML are unchanged.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/landing-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/landing-manifest.json
```

The helper verifies and **stages** the patch. Run `python3 Tools/run_regression_suite.py`
in the patched source and rebuild the DLL. **17 regression programs pass**, including
**14 landing cases**; eight of those fail assertions against unmodified upstream.
Four stale upstream test programs are also aligned with previously imported fixes.
The runtime change is confined to one function in `CvUnitAI.cpp`.

[Investigation and audit](../research/landing/README.md) ·
[Manifest](landing-manifest.json) · [Before](landing-before.log) ·
[Current suite](landing-regression.log) ·
[Upstream's stale tests](landing-upstream-regression.log) ·
[Patch verification](landing-patch-validation.log).

The landing cases execute native dispatch, amphibious forwarding and group movement
with explicit host adapters. No full DLL build or autoplay-save replay is claimed.

## Joint settlement search

[0007-joint-settlement-planning.patch](0007-joint-settlement-planning.patch) is the
earlier cumulative patch for clean GitLab **`6222511c1a81649445fa69e8ca6dca79cf60c975`**.
It includes 0006 below; apply 0007 directly to the clean base, not on top of 0006.

Actual settlers now search the complete independent candidate snapshot and compare
destination–route pairs. Hypothetical production sites no longer suppress their
alternatives. Branch-and-bound stops only when the remaining site values cannot
beat a feasible delivery plan. Shore parties can choose a worthwhile island before
committing to a land destination; loaded transports use the same candidate pool.
Accepted land jobs persist, and obsolete naval-preference/shortlist shortcuts are
removed. This follow-up removes **92 net runtime lines** relative to 0006.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/joint-settlement-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/joint-settlement-manifest.json
```

Then run `python3 Tools/run_regression_suite.py` in the patched source and rebuild
the DLL. Application verifies checksums and **stages** the patch. No save-layout
or XML change is introduced.

**22 regression programs pass**, including 1,000 joint-search cases checked against
an exhaustive route oracle. The old function demonstrably chooses a 270-utility
land plan over an available 584-utility island plan; the replacement chooses the
island, with separate tests ensuring better walking plans win.

[Algorithm and complexity](../research/settlement-search/README.md) ·
[Before/after evidence](joint-settlement-before.log) ·
[Full suite](joint-settlement-regression.log) ·
[Manifest](joint-settlement-manifest.json) ·
[Patch application verification](joint-settlement-patch-validation.log).

The applied tree matches tested source `8edb23b96c7b9f6369a54d18d0a84a62c799b841`.
Tests compile production fragments with explicit path/mission adapters in C++03;
no full DLL build or BTS replay is claimed. The utility still uses the corrected
native found-value heuristic, not a complete city-economy rollout. Runtime changes
have not been pushed directly to GitLab.

## Settlement placement

Superseded by cumulative patch 0007 above; retained for provenance.

[0006-settlement-placement.patch](0006-settlement-placement.patch) targets clean
GitLab **`6222511c1a81649445fa69e8ca6dca79cf60c975`**. That base already contains
patch 0005's runtime changes. Apply 0006 directly to this clean base; the patch
also restores regression tests and documentation omitted from the upstream import.

The [transport entry investigation](../research/transport-entry/README.md) addresses
loaded parties bypassing the voyage controller after manual boarding or autoplay
changes. Passengers defer to their carrier; loaded ships enter civilian transport
control regardless of their previous role; destinations survive role changes.
Walking remains an eligible choice. The objective is competent settlement delivery,
not more boat use. Land decisions now log their destination and route scores.

The [settlement assessment](../research/settlement/README.md) traces the placement
pipeline and criticizes static scoring, premature pruning and missing development
plans. Corrections cover omitted sea-resource/base-improvement value, whole-city
resource-count penalties, duplicate close-spacing penalties, capital distance,
settler-demand counting and an opportunistic founding shortcut.

```sh
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/settlement-manifest.json --check
python3 fixes/apply.py /path/to/rise-of-mankind --manifest fixes/settlement-manifest.json
```

The helper verifies the base/hashes and applies **and stages** the changes.
Run `python3 Tools/run_regression_suite.py` from that source checkout and rebuild
the DLL. Save layout and XML rules are unchanged.

**21 regression programs pass.** Seven settlement checks and two transport-entry
checks were added. Against base `6222511`, five settlement checks fail native
assertions and one fails the founding-path contract; the XML control already
passes. See [before](settlement-before.log), [after](settlement-regression.log),
[manifest](settlement-manifest.json) and [patch verification](settlement-patch-validation.log).
Clean application reproduces tested source commit `9b140263c46e9545a6226595ce2fde561c845e38`.

These are executed C++03 fragments and source/XML contracts, not a DLL build or
BTS replay. The transport fixtures cover manual boarding, update order and role
changes using explicit host adapters. Full engine scheduling, distant pickup,
retry limits and transport demand remain unresolved. The settlement report's
population-constrained rollout optimizer is proposed, not implemented.
These runtime commits have not been pushed to GitLab.


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
