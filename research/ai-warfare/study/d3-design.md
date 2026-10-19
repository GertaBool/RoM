<!-- Rendered by method/docs.py from d3-design.md.in. Do not edit; edit the template. -->
# D3, the balance against the leader: design (not built)

Principle D3 and gap R2 of `study/doctrine.md`. The AI teams declare wars among themselves in every
logged game, never on the human, even while it leads, and no stronger AI joined any of its wars.
This note asks for approval of two steps: a measurement, then a change whose final shape the
measurement decides. Code facts are from the DLL source as of the S2 commit (GitLab `e4679cd`).

## 1. Hypothesis (H3, to be registered with principle D3 and gap R2)

The AIs never move against the human because:
- every war path of `CvTeamAI::AI_doWar` wants a target weaker than the AI alone;
- every path passes a no-war roll against the leader's `NoWarAttitudeProbs` for its attitude to the
  target, and the human keeps that attitude high with gifts and open borders (R3);
- the one coalition path (dogpile) counts only the power of teams already at war with the target;
- a team with any war plan does not consider a new war at all.

It would be refuted if, at the saves, the AIs that could have joined were blocked by something
else, such as the land-target test or the war-rand gates. The change would then take another shape
(section 3).

## 2. Step 1: where the decision against the human fails (a measurement, not a change)

The decision follows from formulas, so it is computed, not simulated (CLAUDE.md, rule 9).

- **Tool.** `HARNESS_WAR_DIAG` in `toolchain/harness/HarnessState.cpp`, like `HARNESS_DEFENCE_DIAG`.
  At a loaded save it writes one telemetry line per AI team towards the human's team, with only
  reads and no change of state:
  - whether the team considers a new war this turn at all: no war plan, or its enemies' power
    percent below the threshold (`CvTeamAI.cpp:5126`);
  - for each path (total, limited, dogpile), the chance this turn of trying it, from
    `AI_getWarRands` and `AI_getWarThresholds`;
  - the attitude to the human, its no-war probability (`AI_noWarAttitudeProb`), and the chance the
    path's roll passes it;
  - the power test of each path, with both sides of the inequality (`CvTeamAI.cpp:5259`,
    `CvTeamAI.cpp:5347`, `CvTeamAI.cpp:5412`), and `AI_isLandTarget`;
  - `AI_startWarVal` towards the human, and its rank among the team's candidate targets.
- **Saves.** The last saves of game 3, game 4 and game 5, and the game 6 save.
- **Result.** A study table through `sqlfig.py` (the per-team gate that blocks), added to
  `study/doctrine.md` as facts for R2.

## 2a. Step 1 result

Built and run (`HARNESS_WAR_DIAG`; the tables are in `study/doctrine.md`, section 3.7):
- At the saves of game 3 to game 6, no power test of any AI team towards the human passes. Towards
  AI teams the tests pass for many pairs.
- The attitude roll is often not the block: many teams would pass it towards the human.
- Each AI alone is too weak, partly because its own wars take their share of its power. The dogpile
  path counts only teams already at war with the human.
- The teams whose roll can pass, together, reach the dogpile bar at two of the four saves.

So H3 stands, with weight on the power gate and the dogpile count, not on attitude. Of the
candidates below, (b) is the one the measurement supports. (a) would change little, since the roll
already passes for many teams. (c) matters only for teams with war plans, which the tables of step 1
show for many AIs.

## 3. Step 2: the balance term (shape decided by step 1)

The term is a define `AI_BALANCE_SHARE`: a share of known power, per mille. At zero it is off.
- **The hegemon.** A team is the hegemon for an AI when it has the most power of all living teams
  that AI has met, and its share of their summed power exceeds `AI_BALANCE_SHARE`. The human is
  never named: the term applies to any team, AI or human.
- **Character is kept through the leader's own fields.**
  - The no-war roll against a hegemon is lowered in proportion to the leader's
    `iWorseRankDifferenceAttitudeChange` (its envy of better-ranked players, from the
    `LeaderHeadInfo` records). Leaders whose field is zero or positive behave as now.
  - A leader at `ATTITUDE_FRIENDLY` keeps its no-war probability.
- **Candidates, chosen by what step 1 finds blocking:**
  - (a) the no-war roll, as above;
  - (b) the dogpile power test against a hegemon counts the power, in reach of the hegemon, of every
    team whose own roll passes against it this turn, not only those already at war (a coalition
    forms instead of each AI waiting for the others);
  - (c) a team whose only war plans are against teams weaker than a hegemon also considers the
    hegemon, with the dogpile path only.

  Step 1 decides which of these is needed. The others are not built.
- **Where.** `CvTeamAI.cpp` (`AI_doWar`, `AI_noWarAttitudeProb`), `CvTeamAI.h`,
  `GlobalDefinesAlt.xml`, the harness diagnostic and its README, a new `builds/balance/`, and its
  patch in `fixes/`.

## 4. How it will be judged (registered before any build)

- **On the mission.** A games prediction on `taken` (cities the human takes by the claim turn, at
  Noble, against the reference games), like P2 and P4. A second one on `lost` (cities the human
  loses), since a coalition that never takes a city does not beat the human.
- **In the harness.** `seat_captures` of the human-model seat over at least thirty seeded runs per
  arm, with S2 on in both arms and the balance term on in one, judged with the rank-based Welch
  test (CLAUDE.md, rule 9). It serves the `taken` prediction. Guards: `turn_seconds` no worse,
  `completed` no regression.
- **Character.** Reported per leader from the runs, not as a gate: how often each leader declares
  war, with the term on and off. Leaders whose envy field is zero must not change.
- **Risk to watch.** Coalitions against an AI hegemon may make AI-AI wars more frequent, so the runs
  report AI-AI declarations in both arms.

## 5. What is asked

Step 1 is approved and done. Proposed shape of step 2, for approval:
- Candidate (b), the coalition of the willing, against a hegemon only. In the dogpile test, the AI
  counts, beside the teams already at war with the hegemon, every team that has met it, can declare
  war on it, and whose own dogpile roll passes this turn. Each counts with its power in reach of the
  hegemon, after its own enemies' share, as the tests already count it.
- Candidate (c) for teams whose war plans are only against teams weaker than the hegemon: they
  consider the hegemon by the dogpile path alone.
- Candidate (a) only as the leader's envy term on the no-war roll, so character is kept: leaders
  with no envy are unchanged.
- The rolls stay random per team and per turn, so a coalition forms only when enough of its members
  are willing on the same turn. Each AI still decides alone; no AI is told to join.

## 6. Step 2 judged in the harness (P6)

Built as change B (`builds/balance`, `fixes/balance.patch`) and run under P6: the start-of-game scenario of
game 3 at Noble, the human model in the human's seat, thirty seeds per arm from `ledger.py seeds P6`, one
harness DLL with only `AI_BALANCE_SHARE` differing (arm a on, arm b off). The ledger's test (the
rank-based Welch test of `seat_captures`) does not corroborate the claim: the seat took no fewer
cities in arm a (`study/doctrine.md`, section 7).

Per arm:

| arm | runs | reached_300 | median_taken | total_taken | median_lost | total_lost | runs_with_war_on_seat | total_wars_on_seat | median_ai_ai_wars | median_seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| a | 30 | 30 | 2.0 | 68 | 0.0 | 18 | 13 | 17 | 11.0 | 545.833 |
| b | 30 | 30 | 1.0 | 50 | 0.0 | 19 | 14 | 23 | 11.0 | 544.932 |

*category; who: the human-model seat (seat 12) and the AI players, per arm of P6; turn: turns 1 to 300 of each run; rows counted: 2; source: P6 harness runs (the turn-0 scenario of game 3, Marathon, Noble; seat 12 played by the human model; arm a: AI_BALANCE_SHARE 110, arm b: 0; S2 on in both), loaded by study/p6_load.sql from each run's telemetry (run.jsonl): capture events by and from the seat, war events on and by the seat and between AI teams, the turns played and the telemetry's milliseconds [p6]. Every value counted (2).*

How often the seat, or an AI, was the hegemon, and the seat's share of power over the run:

| arm | run_turns | seat_hegemon_turns | ai_hegemon_turns | seat_share_100 | seat_share_150 | seat_share_200 | seat_share_250 | seat_share_300 |
|---|---|---|---|---|---|---|---|---|
| a | 7530 | 1088 | 362 | 71.429 | 71.978 | 68.523 | 96.417 | 109.436 |
| b | 7530 | 1030 | 259 | 71.545 | 71.049 | 73.794 | 89.243 | 106.853 |

*category; who: the human-model seat (seat 12) and the AI players, per arm of P6; turn: turns 50 to 300 of each run; the seat's share at turns 100, 150, 200, 250 and 300; rows counted: 2; source: as p6_arms: the power of each living player each turn (telemetry p records); a turn counts as a hegemon turn when the strongest player holds more than 110 per mille of the living players' power (AI_BALANCE_SHARE, here over all living players rather than those one team has met); the seat's share of that power, per mille, median over the runs [p6]. Every value counted (2).*

The declarations of war, by kind and target:

| arm | declarations | on_stronger_target | dogpile | on_seat | dogpile_on_seat | median_turn_on_seat |
|---|---|---|---|---|---|---|
| a | 427 | 138 | 84 | 17 | 1 | 214.0 |
| b | 453 | 127 | 98 | 23 | 1 | 155.0 |

*category; who: every declaration of war in the P6 runs, per arm; turn: turns 1 to 300 of each run; rows counted: 2; source: as p6_arms: the telemetry's war events (declaring team, target, both teams' power, the declarer's war plan: 4 limited, 5 total, 6 dogpile); declarations on a stronger target; on the seat; the median turn of the declarations on the seat [p6]. Every value counted (2).*

Every run:

| arm | seed | taken | lost | wars_on_seat | wars_by_seat | ai_ai_wars | last_turn |
|---|---|---|---|---|---|---|---|
| a | 72243828 | 0 | 1 | 1 | 2 | 12 | 300 |
| a | 124151260 | 3 | 1 | 1 | 1 | 14 | 300 |
| a | 200525027 | 4 | 0 | 0 | 4 | 10 | 300 |
| a | 207380157 | 2 | 0 | 0 | 2 | 11 | 300 |
| a | 355449549 | 2 | 0 | 0 | 2 | 11 | 300 |
| a | 414044836 | 0 | 2 | 1 | 0 | 14 | 300 |
| a | 429971064 | 1 | 1 | 1 | 3 | 13 | 300 |
| a | 643539951 | 5 | 3 | 1 | 6 | 11 | 300 |
| a | 705506003 | 2 | 1 | 0 | 1 | 13 | 300 |
| a | 767444573 | 2 | 0 | 0 | 1 | 14 | 300 |
| a | 773500259 | 1 | 0 | 0 | 2 | 10 | 300 |
| a | 817532997 | 1 | 0 | 0 | 3 | 13 | 300 |
| a | 842283125 | 3 | 1 | 1 | 3 | 8 | 300 |
| a | 905336430 | 3 | 0 | 0 | 3 | 12 | 300 |
| a | 996504313 | 1 | 0 | 0 | 1 | 12 | 300 |
| a | 1048957077 | 5 | 0 | 1 | 3 | 13 | 300 |
| a | 1126729056 | 4 | 0 | 1 | 3 | 10 | 300 |
| a | 1152569364 | 5 | 1 | 1 | 3 | 12 | 300 |
| a | 1281888470 | 2 | 0 | 0 | 2 | 10 | 300 |
| a | 1478284367 | 1 | 1 | 0 | 3 | 16 | 300 |
| a | 1517846120 | 0 | 0 | 0 | 0 | 8 | 300 |
| a | 1544723685 | 3 | 1 | 1 | 5 | 11 | 300 |
| a | 1576708976 | 2 | 3 | 3 | 0 | 7 | 300 |
| a | 1680322555 | 3 | 1 | 2 | 1 | 9 | 300 |
| a | 1716899563 | 1 | 0 | 0 | 2 | 11 | 300 |
| a | 1751420932 | 0 | 0 | 0 | 3 | 17 | 300 |
| a | 1857181504 | 6 | 0 | 0 | 5 | 9 | 300 |
| a | 1893151984 | 2 | 0 | 2 | 0 | 7 | 300 |
| a | 1955249151 | 3 | 0 | 0 | 4 | 12 | 300 |
| a | 2079583610 | 1 | 1 | 0 | 1 | 11 | 300 |
| b | 72243828 | 0 | 1 | 3 | 0 | 13 | 300 |
| b | 124151260 | 1 | 0 | 0 | 3 | 11 | 300 |
| b | 200525027 | 3 | 1 | 0 | 4 | 18 | 300 |
| b | 207380157 | 1 | 0 | 0 | 1 | 10 | 300 |
| b | 355449549 | 1 | 0 | 0 | 4 | 14 | 300 |
| b | 414044836 | 4 | 1 | 0 | 6 | 10 | 300 |
| b | 429971064 | 1 | 2 | 3 | 2 | 15 | 300 |
| b | 643539951 | 2 | 0 | 1 | 1 | 15 | 300 |
| b | 705506003 | 2 | 2 | 1 | 3 | 9 | 300 |
| b | 767444573 | 1 | 2 | 1 | 1 | 13 | 300 |
| b | 773500259 | 0 | 0 | 0 | 0 | 11 | 300 |
| b | 817532997 | 4 | 0 | 1 | 5 | 16 | 300 |
| b | 842283125 | 3 | 0 | 0 | 3 | 8 | 300 |
| b | 905336430 | 1 | 0 | 0 | 3 | 5 | 300 |
| b | 996504313 | 2 | 0 | 0 | 5 | 15 | 300 |
| b | 1048957077 | 1 | 0 | 0 | 2 | 8 | 300 |
| b | 1126729056 | 2 | 0 | 2 | 2 | 9 | 300 |
| b | 1152569364 | 1 | 1 | 1 | 0 | 10 | 300 |
| b | 1281888470 | 0 | 0 | 0 | 2 | 10 | 300 |
| b | 1478284367 | 1 | 1 | 3 | 1 | 11 | 300 |
| b | 1517846120 | 4 | 2 | 2 | 4 | 11 | 300 |
| b | 1544723685 | 2 | 4 | 1 | 2 | 11 | 300 |
| b | 1576708976 | 3 | 0 | 1 | 3 | 16 | 300 |
| b | 1680322555 | 1 | 0 | 0 | 3 | 11 | 300 |
| b | 1716899563 | 0 | 1 | 2 | 2 | 14 | 300 |
| b | 1751420932 | 1 | 0 | 0 | 3 | 12 | 300 |
| b | 1857181504 | 3 | 1 | 1 | 3 | 12 | 300 |
| b | 1893151984 | 1 | 0 | 0 | 3 | 13 | 300 |
| b | 1955249151 | 0 | 0 | 0 | 1 | 14 | 300 |
| b | 2079583610 | 4 | 0 | 0 | 4 | 9 | 300 |

*category; who: the human-model seat (seat 12), per run of P6; turn: turns 1 to 300 of each run; rows counted: 60; source: as p6_arms, one row per run: the seed (from ledger.py seeds P6), the cities the seat took and lost, the wars declared on it and by it, the wars between AI teams, the last turn played [p6]. Every value counted (60).*

Readings:
- The seat was rarely the hegemon. Its median share stays below the threshold until the last rows,
  where it reaches it. So the term mostly acted, if at all, against AI hegemons, and the test did
  not exercise D3 against the seat. Contradicted if runs with the seat as hegemon for most of the game
  show the same result.
- No coalition formed in either arm. Dogpile declarations are not more frequent with the term on.
  Why the term did not raise them is *open*: the war diagnostic at the turns where a hegemon existed
  in these runs would show which gate still blocked.
- What next is a decision for the line (`study/doctrine.md`, section 7). Either an opponent that
  compounds as the human does, so that the seat becomes the hegemon, or the human's own games under
  P5. The term stays in `builds/balance` behind its define; at zero it leaves the S2 build unchanged.

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `p.p6_arms` | table, 2 values | category | the human-model seat (seat 12) and the AI players, per arm of P6 | turns 1 to 300 of each run | 2 | P6 harness runs (the turn-0 scenario of game 3, Marathon, Noble; seat 12 played by the human model; arm a: AI_BALANCE_SHARE 110, arm b: 0; S2 on in both), loaded by study/p6_load.sql from each run's telemetry (run.jsonl): capture events by and from the seat, war events on and by the seat and between AI teams, the turns played and the telemetry's milliseconds [p6] |
| `p.p6_hegemon` | table, 2 values | category | the human-model seat (seat 12) and the AI players, per arm of P6 | turns 50 to 300 of each run; the seat's share at turns 100, 150, 200, 250 and 300 | 2 | as p6_arms: the power of each living player each turn (telemetry p records); a turn counts as a hegemon turn when the strongest player holds more than 110 per mille of the living players' power (AI_BALANCE_SHARE, here over all living players rather than those one team has met); the seat's share of that power, per mille, median over the runs [p6] |
| `p.p6_wars` | table, 2 values | category | every declaration of war in the P6 runs, per arm | turns 1 to 300 of each run | 2 | as p6_arms: the telemetry's war events (declaring team, target, both teams' power, the declarer's war plan: 4 limited, 5 total, 6 dogpile); declarations on a stronger target; on the seat; the median turn of the declarations on the seat [p6] |
| `p.p6_runs` | table, 60 values | category | the human-model seat (seat 12), per run of P6 | turns 1 to 300 of each run | 60 | as p6_arms, one row per run: the seed (from ledger.py seeds P6), the cities the seat took and lost, the wars declared on it and by it, the wars between AI teams, the last turn played [p6] |
