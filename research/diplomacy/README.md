# Diplomacy and leader personalities

What the Rise of Mankind AI does in diplomacy, where it gets it wrong, and what it
would take to make opponents that are dangerous and still play plausibly. Method:
read the code, then measure with the real DLL in the
[headless harness](../../toolchain/harness/README.md) on the mod's WorldBuilder
scenarios. Every seat is played by the AI.

Short answers:

- **Defects.** The deal, attitude and personality code had 14 defects, from 32-bit
  overflow in the peace and surrender valuations to tribute thresholds read from the
  wrong leader. They are fixed in patch 0014 (GitLab
  [!39](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/39)).
  Measured against patch 0013, the AIs fight fewer wars, at better odds, and win more
  of them. AI-to-AI resource swaps are halved now that they are value-checked.
- **Harness.** The harness itself first had to become trustworthy, because the
  earlier campaign numbers were wrong:
  - It did not apply RoM's Python building rules, so late-game cities stacked every
    tier of a building line.
  - It leaked memory on every Python callback. That, not slow DLL code, was the
    Marathon crash at turn 491.
  - Its telemetry changed the games it observed.

  All three are fixed, and the earlier campaign was re-run.
- **Save and reload.** A game reloaded from a save played differently from the game
  that saved it. The two causes were stale attitude caches and wrong border-danger
  flags, fixed in patches 0014 and 0015
  ([!40](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/40)).
  Reloaded games now play identically to the running game.
- **Turn time.** Late-game turns are mostly path finding and unit-training queries.
  Patch 0015 removes redundant `canTrain` work: 17 % less time on a turn-400 Marathon
  position, with an identical game.
- **What still limits the AI:**
  - Every AI-to-AI deal is proposed by one side and never evaluated by the other.
  - No AI ever signed a defensive pact.
  - Almost no war targets the score leader, so a runaway conquers unopposed: in one
    Marathon game Augustus won by conquest at turn 501.
  - Personalities act as dice rather than as biases on a judgement.

  The proposals at the end are ranked by how much they would add to the opponents'
  competence and what they cost.

## Method

**Code maps.** Three read-only maps of the source at GitLab `main` 93ae873 (with
patch 0013) were checked line by line against the tree:

- [trade-map.md](code-maps/trade-map.md): every tradeable item, every deal the AI
  proposes or accepts, every valuation.
- [personality-map.md](code-maps/personality-map.md): every leaderhead field, who reads
  it and what it decides. Statistics over all 82 leaders are in
  [data/leader-stats.txt](data/leader-stats.txt) and [data/leaders.json](data/leaders.json).
- [open-borders-map.md](code-maps/open-borders-map.md): everything Open Borders
  touches, as groundwork for splitting it.

**Campaign.** Two WorldBuilder scenarios were converted with `wbs2scn.py`:

- Mediterranean, standard size, 10 civilizations.
- Earth with 12 preset civilizations, standard size.

They were played at Noble: Epic (300 turns) with seeds 1 to 5, and Marathon (590 turns)
with seeds 1 and 2.
Every seed was played with patch 0013 and with patch 0014: same scenario, same seed,
different DLL. The telemetry records each turn: every player's economy, building and
unit counts, attitudes, the team relations matrix (war, open borders, pacts, vassals,
war plans), and every trade as it is agreed. [tools/dipl-compare.py](tools/dipl-compare.py)
pairs the runs and reports the mean paired difference and in how many pairs the
difference has each sign.

**Harness corrections made first.** These invalidated the earlier campaign (see the
section at the end).

## What the AI does in diplomacy

The full maps are linked above. The points that matter most for competence:

1. **AI-to-AI deals are one-sided.**
   - The proposer checks only the partner's denials, then calls `implementDeal`. The
     partner's `AI_considerOffer` runs only when a human makes the offer.
   - Before patch 0014, resource swaps between AIs had no value check at all.
2. **The AI uses a narrow set of deal shapes.** It proposes only:
   - tech for tech or gold;
   - resource for resource;
   - map for map;
   - open borders, defensive pacts and permanent alliances, each for the same item;
   - peace with tech, gold or a city;
   - tech and gold to hire a war;
   - liberation gifts and vassal offers.

   Patch 0014 adds tech for gold and gold per turn for a resource.

   One rule in `CvPlayer::updateTradeList` forbids mixing annual items (resources, gold
   per turn, agreements) with one-shot items (gold, tech, maps, cities) in any trade
   involving an AI. That rule alone blocks "lump-sum gold for a resource" and "pay me
   to liberate this city", both for proposals and for the AI's counter-proposals.
3. **Personality is mostly dice.**
   - War and peace are per-turn rolls against MaxWarRand and similar fields. They do
     not depend on opportunity and do not scale with game speed.
   - Victory inclinations and the DAGGER strategy are rolled once per game, with no
     feasibility check.
   - Attack odds get an optimism bonus of up to 20 points (27 with the conquest agenda).
   - Raze chances go up to 75 % with no value term.
   - Leaders with a wonder-construction rand of 0 effectively never start a wonder.
   - 44 of the leaderhead fields are identical for all 82 leaders.
4. **Rate limits are few.** Between AIs, contact timers are never advanced. The only
   limit is a per-turn roll on the leader's `ContactRand`:

   | Proposal | ContactRand |
   |---|---|
   | Tech and resource | 5 |
   | Open borders | 20 |
   | Defensive pact | 80 |

   On top of that, a defensive pact needs Pleased attitude on both sides.

## Defects fixed (patch 0014)

| Defect | Effect |
|---|---|
| 32-bit power products in `AI_endWarVal` (5 sites), `AI_surrenderTrade` (3), `AI_considerOffer` (2), paranoia | Team power passes 10^5 in later eras (RoM unit power reaches 2100). Peace values became garbage, and capitulation was refused once both powers passed about 33,000. |
| Received resource valued with `iChange -1` | Valued as a spare copy, a fifth of its worth. |
| No value check on AI-to-AI resource swaps | An AI gave away resources for much less in return. |
| Peace gold counted 1:1 | `AI_dealVal` prices gold at 2 to 3 value per gold, so peace cost several times too much gold. |
| Second war-hire tech compared with the first one's best | Wrong tech offered. |
| Embargo priced from all the target's deals | Embargo requests were refused or accepted on the wrong value. |
| Help and tribute thresholds read from the other leader | A warmonger asked for tribute with a pacifist's patience, and the reverse. |
| Favourite religion and espionage weight read from the leader, not the personality | Wrong with random personalities. |
| `AI_isDoStrategy(AI_VICTORY_CONQUEST3)` | Tested the strategy bit 7 (FINAL_WAR) instead of the victory flag. |
| `AI_acceptSurrender` bound `MaxWarRand/100` | 0 for eleven leaders, who then refused every capitulation. |
| Memories and gifts did not refresh the attitude cache | A gift and a request in the same turn met the old mood. |
| Team counters advanced before the attitudes that use them | Attitudes lagged a turn, and reloaded games diverged. |
| `AI_demandRebukedWar` on the asynchronous generator in the synchronous turn | The war could start on some multiplayer machines only. |
| AI vassals never asked about tribute | Tribute was simply taken. |

Each fix has a test in `Tools/test_diplomacy_fixes.py` on GitLab (14 tests, all failing
on the previous source); see [fixes/README.md](../../fixes/README.md).

## Measured: patch 0013 against patch 0014

**Epic, six pairs** (Mediterranean and Earth 12, seeds 1 to 3, 300 turns). The last
column counts the pairs where 0014 is higher or lower.

| Per 100 turns unless noted | 0013 | 0014 | 0014 higher / lower |
|---|---|---|---|
| All trades | 134.0 | 98.4 | 1/5 |
| Resource swaps | 44.7 | 23.4 | 0/6 |
| Tech for tech | 6.5 | 6.0 | 3/3 |
| Tech for gold | 20.8 | 22.1 | 4/2 |
| Resource for gold per turn (new) | 0 | 0.3 | 2/0 |
| One-sided (gifts, tribute, help) | 13.8 | 6.6 | 1/5 |
| Open borders signed | 33.8 | 30.5 | 1/5 |
| Wars declared | 7.8 | 6.5 | 1/4 |
| Median war length (turns) | 27.3 | 24.4 | 1/5 |
| Median power ratio, declarer to target | 1.20 | 1.39 | 4/2 |
| Cities taken by the declarer per war | 1.01 | 1.17 | 5/1 |
| Wars in which the declarer took a city | 36 % | 43 % | 4/2 |
| Vassal pairs at the end | 2.2 | 1.2 | 1/4 |
| Mean techs at the end | 49.3 | 47.8 | 3/3 |
| Cities at the end | 137.8 | 138.0 | 3/3 |
| Player-turns in financial trouble | 3.2 % | 4.4 % | 4/2 |

What the table shows:

- **Value-checked trades.** Fewer swaps go through, and fewer one-sided deals.
- **More deliberate wars.** Fewer and shorter wars, declared at better odds, and more
  often successful.
- **Fewer vassals.** Fewer vassal relationships form. The corrected surrender and
  capitulation valuations are the likely cause, but this was not traced case by case.
- **Economy unchanged within noise.** Techs and cities do not move. Financial trouble
  rises a little, but in different runs and for different leaders, and its sign is
  mixed (4/2).

Six pairs separate only the large effects. Seeds 4 and 5 and the Marathon pairs
follow below.

<!-- MARATHON -->

## What else the campaign shows

These appear in both builds:

- **No defensive pact in any run.** Pacts need Political Philosophy, a Pleased attitude
  on both sides, and a 1-in-80 roll per pair and turn. Attitudes are spread around 0
  (median 0 to 1; 30 % at +5 or more), so the rolls rarely meet two Pleased partners.
- **Nobody gangs up on the leader.** Only 4 to 5 % of wars are declared on the
  player with the highest score; with 10 to 12 players, random targets would give about
  10 %. The AI picks targets it can beat, which is individually rational. Collectively
  it lets a runaway grow. In a Marathon test game Augustus held 99 cities and won by
  conquest at turn 501, with the rest reduced to 2 to 5 cities each.
- **Gold piles up.** At turn 300 on Epic the median AI holds 1,100 to 1,200 gold, and
  the largest hoards reach 18,000 to 31,000. Research is already at its maximum share
  and the surplus comes from gold earned outside the slider. The AI's gold-hurry planner
  needs a civic that allows buying production, so without one the surplus does nothing.
- **Armies are large.** About 14 units per city at turn 300 on Epic, 12.6 of them
  military, and the unit count drives the late-game turn time (below).

## Turn time and the crash at turn 491 (patch 0015)

The Marathon runs of the first campaign crashed between turns 450 and 520. Memory
sampling on an identical game settled the cause:

| Turn | Old harness | Fixed harness |
|---|---|---|
| 287 | 520 MB | 67 MB |
| 415 | 1.9 GB | 75 MB |
| 491 | 4.09 GB, then a crash | 90 MB |

The fixed harness ran on to the conquest victory at turn 518. The harness's stand-in
Python objects allocated memory for every callback the DLL prepared and never freed
it. The DLL itself stays under 100 MB even in this late-game state.

Turn time is the real cost of the late game. From a turn-400 Marathon snapshot (342
cities, about 1,800 units), the profile of three turns:

- Path finding: 52 % of the time inclusive. Most of it comes from unit AI that searches
  a path to each candidate city and rejects the result afterwards: `AI_guardCity` alone
  takes 16 %, and its searches run to completion even when only paths under one to three
  turns are wanted.
- `CvCity::canTrain`: 20 % of the time, 3.8 million calls in three turns.

Patch 0015 removes the redundant `canTrain` work. `AI_buildingValueThreshold` now
checks a building's combat-type experience before asking whether the city can train
that combat type, and `AI_bestUnitAI` reuses its first pass. Calls fall to 1.3 million,
the turns take 17 % less time, and the game is identical.

Bounding path searches by the turn limit the caller wants is the next large saving.
It would change which path the finder returns in some cases, so it is a pathfinder
project, not part of this patch.

## Reloaded games now play like the running game

A harness snapshot (`HARNESS_SNAPSHOT`) writes the game exactly as a save does, and the
harness can load it again. Writing a loaded snapshot back gives the same bytes, apart
from one replay message the load adds. Yet a game continued from a snapshot diverged
from the game that wrote it within two turns. The divergence came from state that a
save does not carry:

1. **Attitudes lagged the team counters by a turn.**
   - `CvTeamAI::AI_doCounter` advances the at-war, at-peace and shared-war counters at
     turn rollover.
   - The members' attitude caches were cleared only at the end of each player's next
     turn.
   - A reloaded game starts with empty caches, so the first difference was player 2's
     attitude toward player 0: −6 after reload against a cached −5.
   - Fixed in patch 0014.
2. **Border-danger flags were wrong and never cleared.**
   - `AI_getAnyPlotDanger` flags plots next to enemy territory as dangerous (`CvPlot`'s
     team border cache, not saved). It also flagged them for the enemy team and on the
     enemy's plot, where nothing was known.
   - The flags were cleared only by war, peace or a nearby change of owner, so the
     running game kept marking safe plots as dangerous for a worker.
   - The random-number log (`HARNESS_RAND_LOG`) showed the first differing draw: a
     worker rolling "build Fort with Priority" in one game only.
   - A [static audit](code-maps/unsaved-state-audit.md) of every unsaved member found the cache.
   - Fixed in patch 0015: only the queried plot and team are flagged, and the flags are
     cleared each turn.

With both fixes, continuations from a snapshot are identical to the running game for 12
turns on Mediterranean (turns 150 to 162) and 25 turns on Earth 12 (turns 200 to 225).
In multiplayer, the old behaviour could put a rejoining player out of sync. In single
player it made a reloaded game play differently.

## Proposals

Ranked by what they add to the opponents' competence, with cost and risk. None is
implemented yet.

1. **Let the partner judge AI-to-AI deals.** Run the receiving AI's `AI_considerOffer`
   on every AI proposal, as a human's offer gets. The value checks now differ by deal
   type; this replaces them with one rule and removes give-aways at the source. Small,
   around 30 lines in `AI_doDiplo` and `AI_doPeace`. Risk: trade volume falls further,
   which needs measuring.
2. **Balance of power.**
   - In war-target selection (`AI_startWarVal`, dogpile plans), add a term for the
     target's share of score or land when it leads by a margin.
   - In defensive pact acceptance, count a shared threat in place of the Pleased
     requirement.

   Lets AIs form coalitions against a runaway, the missing behaviour behind the
   Augustus conquest. Medium cost, 100 to 200 lines. Needs campaign tuning so that it
   does not turn into a permanent dogpile of the human.
3. **Personality as bias, not dice.** Recommendations R1 to R11 in
   [personality-map.md](code-maps/personality-map.md#6-recommendations-personality-should-bias-situational-judgements-not-replace-them):
   - attack odds without the optimism dice;
   - raze by value;
   - war and peace as thresholds on the war value, with a hazard scaled by game speed;
   - victory stages re-evaluated for feasibility.

   Medium to large. Each item can land and be measured on its own.
4. **Lump-sum and liberation deals.** Allow one-shot plus annual mixes in AI
   proposals: gold or tech for a resource, gold for liberating a city. This needs the
   `updateTradeList` rule relaxed for AI-to-AI deals only, so that the trade screen is
   unaffected. Medium, and only the AI side can be tested headless.
5. **Split Open Borders** into trade rights, civilian access and military access
   ([open-borders-map.md](code-maps/open-borders-map.md)): about 700 to 1,000 DLL lines
   in about 20 files, plus 150 to 250 Python lines. Risk is medium to high: the trade
   screen lives in the game executable and can only be tested in game, and existing
   saves need converting. Best done after 1 and 2.
6. **Surplus gold.** When gold exceeds the target by several turns of income and no
   gold-hurry civic is active, value civics that allow buying production more highly,
   or spend on upgrades and tech purchases. Small to medium.
7. **Bounded path searches** for unit-AI candidate loops (`AI_guardCity` and similar):
   pass the caller's turn limit into the path finder. Large turn-time saving; medium
   risk, because results change at the margin.

## Harness corrections made during this study

| Problem | Effect on earlier numbers | Fix |
|---|---|---|
| RoM's Python building rules not applied: upgrade lines, observatory, Djenne, zCivics prerequisites, cost modifiers, Djenne, World Bank and Crusade effects | Late-game cities stacked every tier: 54 pop per city and 924,000 gold in total at turn 480 on Marathon, against 12.5 and 28,000 with the rules | `HarnessRoM.cpp`, with tables generated from the mod's Python |
| A Python stand-in allocated memory per callback | The process reached 4 GB and crashed around turn 450 to 520 on Marathon | Nothing is allocated per call |
| Telemetry refreshed AI caches (attitude, strategy, victory, city closeness) and could roll the synchronized generator | The same seed gave a different game from turn 38 on | `HarnessPeek.h` restores caches and seeds; full and minimal telemetry now give the same game |

The harness also gained snapshots, a random-number log and building counts in the
telemetry ([toolchain/harness/README.md](../../toolchain/harness/README.md)).

## Files

- [code-maps/](code-maps/): the three code maps.
- [data/](data/): leader statistics.
- [tools/](tools/):
  - `runscn.sh`: one scenario run.
  - `roundtrip.sh`: the reload check.
  - `memsample.sh`: process memory per turn.
  - `dipl-analyze.py`: trades, wars and relations per run.
  - `dipl-compare.py`: paired comparison of two builds.
  - `fidelity.py`: economy totals per turn.
  - `snapdiff.py`: snapshot comparison by part.
  - `leader-stats.py` and `leader-extra.py`: leaderhead statistics.
- [runs/](runs/): the campaign comparisons.

Timings and outcomes are harness runs with every seat on AI; the game executable was
not run.
