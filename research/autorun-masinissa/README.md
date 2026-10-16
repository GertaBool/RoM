# Autorun as Masinissa: the endless turn, turn time, settlers and the AI economy

The report, for a Marathon game on autorun as Masinissa with the save
`Masinissa BC-0410.CivBeyondSwordSave` (410 BC, game turn 269; sha256
`4a04d07b…4440dd`, not published here):

1. Landing fix works.
2. Settler mechanics still unripe.
3. AI still not valuing key buildings and technologies properly.
4. "Waiting for other players" at the end of the turn never ends, even after reloading or restarting.
5. Worse time complexity.

Patch 0012 ([fixes/0012-autorun-fixes.patch](../../fixes/0012-autorun-fixes.patch)) addresses
items 2 to 5. It landed on GitLab `main` as
[!37](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/37)
(merge `abf8471`, tree `c56ade12` = the tested tree). Its DLL is
[builds/0012](../../builds/0012/CvGameCoreDLL.dll).

## Method

The save was split with [`sav2dat.py`](../../toolchain/harness/sav2dat.py) and loaded
through the DLL's own `read()` functions in the
[headless harness](../../toolchain/harness/README.md): the real `CvGameCoreDLL.dll`,
built from the source under test, runs under Wine with the mod's XML and plays on with
every seat (Masinissa included) on AI. State files record each player's economy, cities
and settlers; optional diagnostics evaluate every test the settler search applies and the
city AI's own building values. Timings are harness timings on one machine; the game
executable was not run.

## 4. The turn that never ends

With GitLab `main` at `dcbae97` (patch 0011) turn 269 never ends:
[runs/main-dcbae97-turn269-stuck.log](runs/main-dcbae97-turn269-stuck.log) reports the
same group after 20 000, 40 000 and 80 000 `CvGame::update` calls.

The group is one Javelineer whose AI gave it a worker-style job (improve a tile). The
target tile holds an enemy unit. The path finder accepts that step, since a combat unit
could take it by attacking, but `CvSelectionGroup::groupMove` without
`MOVE_THROUGH_ENEMY` puts every unit that cannot enter the tile into a new group. The
lone unit therefore leaves its group, the group dies, `CvPlayerAI::AI_unitUpdate` stops
its loop at it, and the next slice finds a new group with full moves and the same job.
Reloading restores exactly this state.

The fix has three layers: `groupPathTo` ends a mission when no unit can take the next
step as the move it was given (the test `groupMove` applies); the worker searches
(`AI_improveLocalPlot`, `AI_improveBonus`) skip tiles with visible enemy units; and a
watchdog ends the moves of a unit that loses its group more than 20 times in one turn.
The save then plays on; 30 turns were checked.

## 5. Turn time

Turns 270 to 279 of the save, the same 10 turns on each build. Older builds need the
`groupPathTo` guard alone to get past turn 269:

| Build | ms per turn | Log |
|---|---|---|
| d8cedd5 + guard | 9 666 | [timing-d8cedd5-with-guard.log](runs/timing-d8cedd5-with-guard.log) |
| patch 0009 + guard | 9 560 | [timing-0009-a9b1fce-with-guard.log](runs/timing-0009-a9b1fce-with-guard.log) |
| patch 0010 + guard | 9 718 | [timing-0010-86af2ab-with-guard.log](runs/timing-0010-86af2ab-with-guard.log) |
| patch 0011 + guard | 9 979 | [timing-0011-with-guard.log](runs/timing-0011-with-guard.log) |
| patch 0012 | 2 575 | [patch0012-30-turns.log](runs/patch0012-30-turns.log) |

So "worse" was not a regression between patches: the previous four builds are equally
slow. A profile (harness profiler, inclusive time) put most of a turn in path searches,
then in exploration. The changes, each measured on the save:

- **`pathValid` memo.** All of `pathValid` except one sea-corner test looks only at the
  parent plot, while FAStar calls it once per neighbour of the plot it expands. The
  parent part is now remembered for the plot being expanded and dropped at the start of
  every search. The game state after 10 turns is byte-identical with and without it;
  turns went from 3.1 s to 2.7 s at that stage.
- **Exploration.** `AI_explore` ran one path search per candidate plot on the whole map.
  Candidates are now scored first and searched best upper bound first; the bound adds the
  largest possible random draw and divides by the fewest turns the path could take, so
  the search stops once no remaining candidate can win. `AI_exploreRange` skips plots
  whose lower bound already exceeds the range (exact: identical game state).
- **Upgrades.** `upgradeAvailable` walked the upgrade graph recursively per query; the
  reachable classes are cached per civilization and unit, and `AI_upgrade` returns
  early when the unit cannot upgrade this turn.
- **Trade denial.** `canTradeItem(..., bTestDenial)` evaluated the expensive denial
  before checking whether the item is tradeable at all.

The path lower bound: a unit may step while any move is left, and the cheapest step is
the lowest cost any route on the map can give the team (or half a move), so a group
with `m` moves takes at most `ceil(m / cheapest)` steps per turn and a target `d` plots
away needs at least `ceil(d / that)` turns. Both bounds are admissible, so the pruning
never changes which plot wins.

## 2. Settlers

At 410 BC 18 settlers existed and 15 had no destination. The harness evaluated, for each
of them and its eight best candidates, every test `AI_found` applies
([runs/settler-diagnosis-410bc.txt](runs/settler-diagnosis-410bc.txt)):

- **Ivan** (4 settlers, 11 to 34 turns old): one candidate, at (82,10), with no
  `MOVE_SAFE_TERRITORY` path and no path at all: it lies behind other civilizations'
  borders. No boat could take it either. The cities had kept training settlers for it.
- **Willem** (2): his sites were reachable only from his *other* cities; the city the
  settlers stood in was walled in by foreign borders.
- **Brennus, Hammurabi** (lone settlers): no escort, so every path failed the danger
  test. Defenders join settlers only when no danger is near, so a city near a war never
  released one.
- **Joao**: a galley had carried a settler for 64 turns. Its escort was gone, and at sea
  the transport routine skipped every turn waiting for one (`MISSING_ESCORT_OR_CAPACITY`).
- **Pericles, Leonidas**: sites on another landmass and no transport built for them.

Two structural defects underlie this: the site count for production did not ask whether
a settler trained there could reach the site, and since the settlement rework a settler
with no site was never disbanded (BTS scrapped it after 20 turns).

**Delivery regions** (`CvPlayerAI::AI_updateSettleReach`, rebuilt with the found values).
Land regions grow from each of the player's cities through revealed land that is the
player's or unclaimed, exactly the plots a `MOVE_SAFE_TERRITORY` path may cross. Sea
regions grow from the player's ports over water that a transport the player has or can
train may enter, using that unit's terrain and feature restrictions and the team's
techs. A party at `p` can be delivered to site `s` if both lie in the same land region,
or if `s` is next to a sea region reached from a port in `p`'s region. A party outside
every region (at sea, landed abroad) is not limited. A first version pooled all cities
into one region and wrongly counted Willem's sites as reachable; the
[test](../../fixes/0012-autorun-fixes.patch) for that case is the first in
`Tools/test_settle_reach.py`.

On these regions: production counts only deliverable sites, `AI_found` and the
transport search skip the rest (saving their failing path searches), a settler older
than max(20, 10 scaled by the train percent) turns with nothing deliverable is
disbanded (checked before the danger rule), a lone settler takes a spare defender from
its city (one above the minimum garrison), a transport at sea without escort returns to
port, and a city with a waiting settler whose sites all need a boat builds one.

Chronic cases (in a city or aboard, no destination, older than 20 turns),
from [runs/settlers-before-after.txt](runs/settlers-before-after.txt):

| State | Count | Who (age) |
|---|---|---|
| Save, turn 269 | 5 | Joao 64, Ivan 34, Ivan 28, Willem 25, Brennus 22 |
| Without the changes, turn 279 | 8 | Joao 74, Ivan 44, 38, 25, 21, Pericles 27, Brennus 26, Hammurabi 22 |
| Patch 0012, turn 299 | 3 | Willem 55, 38, Hannibal 29 |

Ivan's settlers were disbanded, Joao's galley returned to port, took an escort aboard and
sailed for (51,35), and Brennus' settlers left with recruited escorts. Cities grew from
118 to 144 in 30 turns.

**Known limit.** Willem's two settlers stand alone in a border city that is under threat
on every turn of the run. The settler rule there is deliberate: split off and wait in a
city while enemies are within three tiles. Their sites remain deliverable, so they are
neither retired nor sent out. Moving settlers away from a threatened city to a safer one
is not part of this patch. (Hannibal's settler has no deliverable site and is disbanded
on its next update.)

## 3. Buildings and technologies

[runs/economy-and-building-values-410bc.txt](runs/economy-and-building-values-410bc.txt)
lists every player's slider, gold target and commerce, and the city AI's building values.

**The Spearman pump.** Production in the first five turns was about 85 percent units: 54
of about 150 choices were Spearmen, 34 of them "choose min defender". The minimal
garrison counts only `UNITAI_CITY_DEFENSE` units, and a unit can take that role only
through its XML list or a city defence bonus (`CvPlayerAI::AI_unitValue`). Spearmen have
neither; Archers and Axemen do, but 9 of the 18 civilizations had neither Archery nor
Bronze Working, and 12 had no city-defence unit at all. Such a city failed the garrison
test at every production decision, fell back to an attack-role unit (`AI_chooseUnit
(UNITAI_ATTACK)` accepts any combat unit), which never counted, and built the next one.
Those Spearmen then left as attackers: Charlemagne's attack units went from 6 to 27 in
ten turns while his city-defence count stayed at zero. BBAI already counted all
defenders for the first era (Warriors); the fix does so in every era for a city that
cannot train a city-defence unit.

**Gold hoarding on slow speeds.** `AI_doCommerce` lowers research until
`gold + T * rate` exceeds `AI_goldTarget`. On Marathon the targets were 640 to 1270 gold
against total commerce of 50 to 420 per turn; Charles V banked 473 gold at 15 percent
research, Augustus ran 95 percent gold, Brennus 75. `AI_goldTarget` adds
`elapsedTurns / 2` and multiplies by the speed's price factor
`(research + train + construct) / 3` percent. A Marathon game has 1470 turns where
Normal has 700, so the elapsed term already grows 2.1 times faster for the same history,
and the price factor (366 percent) multiplied it again, about 7.7 times in all. The
liquidity cap was "one turn of commerce (two at war) times the research percent", that is
6 or 12 turns on Marathon. Now elapsed turns are converted to the standard speed's
calendar and the cap uses the calendar ratio (2.1 turns of commerce in peace, 4.2 at
war). Normal speed is unchanged (`Tools/test_gold_target_speed.py`).

Over 30 turns from the save, the same source with and without these two changes
([runs/economy-fixes-30-turn-comparison.txt](runs/economy-fixes-30-turn-comparison.txt)):

| | Without | With |
|---|---|---|
| Cumulative research (beakers) | 51 278 | 62 176 (+21 %) |
| Technologies gained | 79 | 100 |
| Buildings completed | 238 | 347 |
| Military units at the end | 915 | 857 |
| Research rate at the end | 2 471 | 3 144 |

Over the first 10 turns alone the faster build gained fewer technologies (22 against 36)
although it researched 10 percent more: in the slower build eight AIs had just picked
the cheap Archery; the faster ones chose Bronze Working or Monarchy, which take longer
than ten Marathon turns. Beakers, not counts, measure throughput over such short spans.

**What looked fine.** Technology values are sensible; for example Rome ranks Writing,
Seafaring, Bronze Working, Fermentation and Archery highest. The Brewery has the top
building value in every city that can build it (about 1700, against 50 to 360 for the
next), because BBAI multiplies the free Alcohol resource's empire-wide value by the
number of cities and by two when none is tradeable. It is a generous count, but hardly
any Brewery is built, so it does not drive production and was left alone.

## Validation

- `Tools/run_regression_suite.py`: 27 of 27 programs pass on the patched tree
  ([fixes/autorun-regression.log](../../fixes/autorun-regression.log)). New:
  `test_turn_end_guard.py` (the blocked step and the watchdog, compiled from source),
  `test_settle_reach.py` (regions on a grid map) and `test_gold_target_speed.py`.
  Against `dcbae97` the blocked-step test fails by its assertion; the other new tests
  cannot compile there because the code they test does not exist
  ([fixes/autorun-before.log](../../fixes/autorun-before.log)).
- Patch application on a clean `dcbae97` checkout reproduces the tested tree
  ([fixes/autorun-patch-validation.log](../../fixes/autorun-patch-validation.log)).
- Clang gate on the eight changed translation units: no new diagnostics
  ([fixes/autorun-clang-gate.log](../../fixes/autorun-clang-gate.log)).
- MSVC 2003 release build: 0 errors, 0 warnings, the same 2451 exports
  ([builds/0012/provenance.json](../../builds/0012/provenance.json)).
- Save format unchanged; all new state is transient and rebuilt after loading.

Analysis scripts used for the tables: [tools/](tools/).
