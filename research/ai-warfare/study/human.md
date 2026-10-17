<!-- Rendered by tools/docs.py from human.md.in. Do not edit; edit the template. -->
# The human's decisions: a study across the four logged games

Method: `framework.md`. Every number comes from the registries named in the source of this
page; the table at the end gives each figure's unit, actor, turn and source.

## 1. Questions

- **Q1.** What does the log record of the human's decisions, and when? Answered from the DLL
  source, not from the war-log README.
- **Q2.** For each class of decision with enough cases: which cue, known before the decision,
  predicts it in a game the model was not fitted on?
- **Q3.** Where the human's rule differs from the AI's behaviour, how? Answered from outcomes,
  because the AI's choices are not logged as commands.

## 2. The sources, checked in the code

- **Commands.** An A line is written when a command executes, in the `Execute` function of its
  network message (`CvMessageData.cpp`). Message types with no log call: extended game,
  advanced start, mod messages, empire split, founding a religion, launching a spaceship, ping
  and reminders. City governors and automated units act without a message, so their actions are
  not commands either. Only the order to automate is logged.
- **Economy.** An M line is written at the end of each player's turn
  (`CvEventReporter::endPlayerTurn`), so it already contains that turn's effects.
  - Commands logged after the human's own M line of the same turn (made while the AIs move):
    game 4 18, game 3 0.
  - A decision's information set is therefore defined by log position, not by turn number.
- **The slider check.** The slider change between consecutive M lines was compared with the
  slider clicks of the turn:
  - game 4: 275 of 284 turns match, and
    5 turns moved with no click;
  - game 3: 264 of 265 turns match, and
    1 moved with no click.

  The moves without a click come from the game: `CvPlayer::verifyGoldCommercePercent` raises the
  gold share whenever gold plus income would go below zero. The M-line slider is therefore not
  the human's choice; only the clicks are. The remaining mismatches are clicks made after the
  M line, which show in the next one.
- **War plans.** The W lines carry no war plan (`toolkit.md`, section 7).
- **Log versions.** Game 1 and game 2 used the first log version, which has no M lines. Only
  decisions without economy cues can be studied there.

## 3. Cases and cues

A case is one decision. Its cues are binary and computed from the lines before it in the log,
limited to what the human sees:
- its own M lines and techs;
- declarations and peace treaties of anyone (they are announced);
- the cities it captured;
- its own commands.

Cues and thresholds were fixed before any model was fitted. The cases are in
`games/gameN/cases_<class>.csv`, written by `tools/cases.py`.

| Class | A case is | `y = 1` when | Games |
|---|---|---|---|
| city order | every city order | the order is a unit | all four |
| slider direction | every turn with a net slider change | the change is toward gold | game 3 and game 4 |
| slider timing | every turn the human ended | it clicked the slider | game 3 and game 4 |
| upgrade timing | every turn the human ended | it upgraded a unit | game 3 and game 4 |

Cues by class:
- city order: at_war, declared_3, capital, captured_city, young_city;
- slider direction: gold_rate_neg, at_war, declared_3, slider_high;
- slider timing: gold_rate_neg, at_war, declared_3, peace_3, captured_3;
- upgrade timing: declared_1, at_war, gold_rate_pos, gold_doubled_10, tech_3.

What the cues mean:
- `gold_rate_neg` / `gold_rate_pos`: the sign of gold per turn in the last M line.
- `at_war`: at war with anyone.
- `declared_k`: the human declared a war in the last `k` turns, this turn included.
- `peace_k`, `captured_k`, `tech_k`: the same window, for a peace treaty, a captured city and a
  new tech.
- `slider_high`: the research slider at `70` % or more.
- `gold_doubled_10`: gold at least twice what it was `10` turns earlier.
- `capital`: the human's first city.
- `captured_city`: a city the human captured.
- `young_city`: founded or captured within `20` turns.

Cases per game:

| Class | game 1 | game 2 | game 3 | game 4 |
|---|---|---|---|---|
| city orders (units) | 153 (68) | 170 (61) | 199 (52) | 383 (139) |
| slider-direction turns (toward gold) | – | – | 14 (8) | 25 (11) |
| turns ended (with a slider click) | – | – | 265 (15) | 284 (30) |
| turns ended (with an upgrade) | – | – | 265 (4) | 284 (17) |

`tools/cases.py` refuses to run if the city-order cases differ from the city-order lines.

## 4. Method

`tools/models.py` uses leave one game out: each model is fitted on the other games and scored on
the held-out one, and the hits are summed over the held-out games. The models:
- `base`: the training majority.
- `single`: the best single cue.
- `fft`: fast-and-frugal trees, every cue order and exit direction tried.
- `tally`: at least `k` cues.
- `logit` and `cart`: weighted rivals (logistic regression, a tree of depth three).

Every cue is oriented on the training games only. The p value is an exact McNemar test against
`base` on the same held-out cases.

## 5. Results

### 5.1 City orders

| model | hits | n | hit rate | balanced | p vs base |
|---|---|---|---|---|---|
| base | 585 | 905 | 0.646 | 0.500 | - |
| single | 702 | 905 | 0.776 | 0.739 | 1.48e-12 |
| fft | 702 | 905 | 0.776 | 0.739 | 1.48e-12 |
| tally | 673 | 905 | 0.744 | 0.679 | 7.49e-10 |
| logit | 702 | 905 | 0.776 | 0.739 | 1.48e-12 |
| cart | 702 | 905 | 0.776 | 0.739 | 1.48e-12 |

*share; who: human; turn: all turns of game1, game2, game3, game4; rows counted: 905; source: models.py, leave one game out over game1, game2, game3, game4. Every value counted (6).*

| held-out game | n | base hits | single hits | fft hits | logit hits |
|---|---|---|---|---|---|
| game1 | 153 | 85 | 122 | 122 | 122 |
| game2 | 170 | 109 | 129 | 129 | 129 |
| game3 | 199 | 147 | 174 | 174 | 174 |
| game4 | 383 | 244 | 277 | 277 | 277 |

*orders; who: human; turn: all turns of game1, game2, game3, game4; rows counted: 905; source: models.py, each game held out in turn. Every value counted (4).*

- Single cue fitted on all games: y = 1 exactly when capital = 1.
- Tree fitted on all games: if capital = 0 then y = 0; if captured_city = 0 then y = 1; if at_war = 0 then y = 1; if declared_3 = 0 then y = 1; else y = 1 exactly when young_city = 0.

Completions (U lines are units, N lines buildings), with the capital taken as the city holding
the palace at the save:

| Share of units among completions | game 3 | game 4 |
|---|---|---|
| human, capital | 0.73 | 0.679 |
| human, other cities | 0.026 | 0.261 |
| AI, capitals | 0.835 | 0.816 |
| AI, other cities | 0.681 | 0.693 |

### 5.2 Slider direction

| model | hits | n | hit rate | balanced | p vs base |
|---|---|---|---|---|---|
| base | 17 | 39 | 0.436 | 0.439 | - |
| single | 35 | 39 | 0.897 | 0.895 | 0.000121 |
| fft | 32 | 39 | 0.821 | 0.816 | 0.00408 |
| tally | 32 | 39 | 0.821 | 0.816 | 0.00408 |
| logit | 35 | 39 | 0.897 | 0.895 | 0.000121 |
| cart | 35 | 39 | 0.897 | 0.895 | 0.000121 |

*share; who: human; turn: all turns of game3, game4; rows counted: 39; source: models.py, leave one game out over game3, game4. Every value counted (6).*

| held-out game | n | base hits | single hits | fft hits | logit hits |
|---|---|---|---|---|---|
| game3 | 14 | 6 | 12 | 12 | 12 |
| game4 | 25 | 11 | 23 | 20 | 23 |

*turns; who: human; turn: all turns of game3, game4; rows counted: 39; source: models.py, each game held out in turn. Every value counted (2).*

- Single cue fitted on both games: y = 1 exactly when gold_rate_neg = 1.
- Tree: if gold_rate_neg = 1 then y = 1; if at_war = 0 then y = 0; if declared_3 = 1 then y = 1; else y = 1 exactly when slider_high = 1.

### 5.3 Slider timing

| model | hits | n | hit rate | balanced | p vs base |
|---|---|---|---|---|---|
| base | 504 | 549 | 0.918 | 0.500 | - |
| single | 417 | 549 | 0.760 | 0.474 | 3.77e-21 |
| fft | 430 | 549 | 0.783 | 0.487 | 1.31e-17 |
| tally | 504 | 549 | 0.918 | 0.500 | 1 |
| logit | 504 | 549 | 0.918 | 0.500 | 1 |
| cart | 504 | 549 | 0.918 | 0.500 | 1 |

*share; who: human; turn: all turns of game3, game4; rows counted: 549; source: models.py, leave one game out over game3, game4. Every value counted (6).*

| held-out game | n | base hits | single hits | fft hits | logit hits |
|---|---|---|---|---|---|
| game3 | 265 | 250 | 189 | 190 | 250 |
| game4 | 284 | 254 | 228 | 240 | 254 |

*turns; who: human; turn: all turns of game3, game4; rows counted: 549; source: models.py, each game held out in turn. Every value counted (2).*

### 5.4 Upgrade timing

| model | hits | n | hit rate | balanced | p vs base |
|---|---|---|---|---|---|
| base | 528 | 549 | 0.962 | 0.500 | - |
| single | 521 | 549 | 0.949 | 0.608 | 0.143 |
| fft | 521 | 549 | 0.949 | 0.562 | 0.0923 |
| tally | 525 | 549 | 0.956 | 0.520 | 0.375 |
| logit | 528 | 549 | 0.962 | 0.500 | 1 |
| cart | 528 | 549 | 0.962 | 0.546 | 1 |

*share; who: human; turn: all turns of game3, game4; rows counted: 549; source: models.py, leave one game out over game3, game4. Every value counted (6).*

| held-out game | n | base hits | single hits | fft hits | logit hits |
|---|---|---|---|---|---|
| game3 | 265 | 261 | 261 | 261 | 261 |
| game4 | 284 | 267 | 260 | 260 | 267 |

*turns; who: human; turn: all turns of game3, game4; rows counted: 549; source: models.py, each game held out in turn. Every value counted (2).*

## 6. Readings

Each reading names its facts and what would refute it.

1. **The human runs two kinds of city.** The capital trains units; every other city builds.
   - Facts:
     - in all four held-out games, the capital cue alone beats the majority rule (section 5.1);
     - no model with more cues does better than that single cue;
     - in completions, the human's other cities produce far fewer units than the AI's, while
       both capitals produce mostly units.
   - Refuted if: a further game where the capital cue does not beat the majority rule, or where
     the human's other cities train units at the AI's rate.
2. **The slider follows one cue: gold per turn.** The slider moves toward gold when the last
   gold per turn was negative, and toward research otherwise.
   - Facts: section 5.2, out of sample in both games. War, a recent declaration and a high slider add
     nothing over that one cue.
   - Refuted if: a further game where the sign of gold per turn does not predict the direction.
3. **When the human touches the slider, and when it upgrades, is not predicted by these cues.**
   - Facts: sections 5.3 and 5.4. No model beats the majority rule; the upgrade cue "declared in the last
     turn" does not reach significance.
   - The earlier rule "upgrades at declarations" (`decisions/human-decisions.md`, R1) was fitted
     and judged on the same data, and does not hold up as a turn-level prediction here.
   - Refuted if: a cue fixed in advance that beats the majority rule out of sample.

## 7. Limits

- **The p values are optimistic.** Cases within one game are not independent: decisions come in
  streaks (`framework.md`, section 5).
- **Few games.** The economy classes rest on two games, so every reading is a hypothesis tested
  on one held-out game in each direction. The city-order reading rests on four.
- **The capital cue is the first city founded,** not the palace's position at the time.
- **No AI command comparison.** The AI's choices appear only as completions, which mix choice
  with production speed.

## 8. The tools, reviewed for this study

- **Changed:**
  - `extract.py` gained the log position of every line, without which "known before the
    decision" cannot be computed.
  - It also gained typed columns for empty tables; without them, the queries failed on the two
    games without M lines.
- **New:**
  - `figlib.result_table` checks that a table lists every model it says it evaluated.
  - `docs.py` names registries (`as g4`) and refuses one id defined by two registries; this was
    found when four registries with the same ids would have overwritten each other in silence.
  - `cases.py`, `models.py` and `production.py`.
- **Gate:** `check_all.py` reproduces every registry with the analysis toolkit's Python, so
  these producers are checked at every commit.
- **Not fit, and why:** the old `micro.py` and `decisions.py` describe and fit on the same data,
  and their documents stay in `UNCHECKED`.

## 9. Open

- **More classes:** promotions (which promotion, given the unit and the coming operation) and
  research choices (a tech known to others or not). Both need XML cues: unit class and tech
  cost.
- **Attacks:** studying when the human attacks needs the options it had on its turn, which the
  log does not hold. A harness replay of the human's turns from a save would give them.
- **Credibility pooling across games** (`framework.md`, section 6), once a fifth game exists.

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `g4.cmds_after_own_M` | 18 | orders | human (player 3) | all turns |  | wl_A rows after the human's own wl_M row of the same turn |
| `g3.cmds_after_own_M` | 0 | orders | human (player 12) | all turns |  | wl_A rows after the human's own wl_M row of the same turn |
| `g4.slider_consistent` | 275 | turns | human (player 3) | all turns |  | turns where the slider change equals the clicks |
| `g4.slider_turns_compared` | 284 | turns | human (player 3) | all turns |  | wl_M slider change against wl_A PERCENT clicks, research |
| `g4.slider_moved_no_click` | 5 | turns | human (player 3) | all turns |  | slider changed with no click: CvPlayer::verifyGoldCommercePercent |
| `g3.slider_consistent` | 264 | turns | human (player 12) | all turns |  | turns where the slider change equals the clicks |
| `g3.slider_turns_compared` | 265 | turns | human (player 12) | all turns |  | wl_M slider change against wl_A PERCENT clicks, research |
| `g3.slider_moved_no_click` | 1 | turns | human (player 12) | all turns |  | slider changed with no click: CvPlayer::verifyGoldCommercePercent |
| `ou.order_unit_cues` | at_war, declared_3, capital, captured_city, young_city | category | human | - |  | cases_order_unit.csv header |
| `sd.slider_dir_cues` | gold_rate_neg, at_war, declared_3, slider_high | category | human | - |  | cases_slider_dir.csv header |
| `st.slider_turn_cues` | gold_rate_neg, at_war, declared_3, peace_3, captured_3 | category | human | - |  | cases_slider_turn.csv header |
| `ut.upgrade_turn_cues` | declared_1, at_war, gold_rate_pos, gold_doubled_10, tech_3 | category | human | - |  | cases_upgrade_turn.csv header |
| `g1.order_unit_n` | 153 | orders | human (player 0) | 0-217 |  | cases_order_unit.csv |
| `g1.order_unit_pos` | 68 | orders | human (player 0) | 0-217 |  | cases_order_unit.csv, y = 1 |
| `g2.order_unit_n` | 170 | orders | human (player 2) | 0-236 |  | cases_order_unit.csv |
| `g2.order_unit_pos` | 61 | orders | human (player 2) | 0-236 |  | cases_order_unit.csv, y = 1 |
| `g3.order_unit_n` | 199 | orders | human (player 12) | 0-266 |  | cases_order_unit.csv |
| `g3.order_unit_pos` | 52 | orders | human (player 12) | 0-266 |  | cases_order_unit.csv, y = 1 |
| `g4.order_unit_n` | 383 | orders | human (player 3) | 0-285 |  | cases_order_unit.csv |
| `g4.order_unit_pos` | 139 | orders | human (player 3) | 0-285 |  | cases_order_unit.csv, y = 1 |
| `g3.slider_dir_n` | 14 | turns | human (player 12) | 108-250 |  | cases_slider_dir.csv |
| `g3.slider_dir_pos` | 8 | turns | human (player 12) | 108-250 |  | cases_slider_dir.csv, y = 1 |
| `g4.slider_dir_n` | 25 | turns | human (player 3) | 102-246 |  | cases_slider_dir.csv |
| `g4.slider_dir_pos` | 11 | turns | human (player 3) | 102-246 |  | cases_slider_dir.csv, y = 1 |
| `g3.slider_turn_n` | 265 | turns | human (player 12) | 1-265 |  | cases_slider_turn.csv |
| `g3.slider_turn_pos` | 15 | turns | human (player 12) | 1-265 |  | cases_slider_turn.csv, y = 1 |
| `g4.slider_turn_n` | 284 | turns | human (player 3) | 1-284 |  | cases_slider_turn.csv |
| `g4.slider_turn_pos` | 30 | turns | human (player 3) | 1-284 |  | cases_slider_turn.csv, y = 1 |
| `g3.upgrade_turn_n` | 265 | turns | human (player 12) | 1-265 |  | cases_upgrade_turn.csv |
| `g3.upgrade_turn_pos` | 4 | turns | human (player 12) | 1-265 |  | cases_upgrade_turn.csv, y = 1 |
| `g4.upgrade_turn_n` | 284 | turns | human (player 3) | 1-284 |  | cases_upgrade_turn.csv |
| `g4.upgrade_turn_pos` | 17 | turns | human (player 3) | 1-284 |  | cases_upgrade_turn.csv, y = 1 |
| `ou.order_unit_models` | table, 6 values | share | human | all turns of game1, game2, game3, game4 | 905 | models.py, leave one game out over game1, game2, game3, game4 |
| `ou.order_unit_by_game` | table, 4 values | orders | human | all turns of game1, game2, game3, game4 | 905 | models.py, each game held out in turn |
| `ou.order_unit_single_rule` | y = 1 exactly when capital = 1 | category | human | all turns of game1, game2, game3, game4 |  | models.py, single cue on all games |
| `ou.order_unit_fft_rule` | if capital = 0 then y = 0; if captured_city = 0 then y = 1; if at_war = 0 then y = 1; if declared_3 = 0 then y = 1; else y = 1 exactly when young_city = 0 | category | human | all turns of game1, game2, game3, game4 |  | models.py, fft fitted on all games |
| `prod.game3_human_capital_unit_share` | 0.73 | share | human | 7-266 | 63 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `prod.game4_human_capital_unit_share` | 0.679 | share | human | 6-285 | 84 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `prod.game3_human_other_unit_share` | 0.026 | share | human | 7-266 | 116 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `prod.game4_human_other_unit_share` | 0.261 | share | human | 6-285 | 261 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `prod.game3_ai_capital_unit_share` | 0.835 | share | ai | 7-266 | 641 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `prod.game4_ai_capital_unit_share` | 0.816 | share | ai | 6-285 | 900 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `prod.game3_ai_other_unit_share` | 0.681 | share | ai | 7-266 | 680 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `prod.game4_ai_other_unit_share` | 0.693 | share | ai | 6-285 | 1875 | wl_U and wl_N completions; capital = BUILDING_PALACE at the save |
| `sd.slider_dir_models` | table, 6 values | share | human | all turns of game3, game4 | 39 | models.py, leave one game out over game3, game4 |
| `sd.slider_dir_by_game` | table, 2 values | turns | human | all turns of game3, game4 | 39 | models.py, each game held out in turn |
| `sd.slider_dir_single_rule` | y = 1 exactly when gold_rate_neg = 1 | category | human | all turns of game3, game4 |  | models.py, single cue on all games |
| `sd.slider_dir_fft_rule` | if gold_rate_neg = 1 then y = 1; if at_war = 0 then y = 0; if declared_3 = 1 then y = 1; else y = 1 exactly when slider_high = 1 | category | human | all turns of game3, game4 |  | models.py, fft fitted on all games |
| `st.slider_turn_models` | table, 6 values | share | human | all turns of game3, game4 | 549 | models.py, leave one game out over game3, game4 |
| `st.slider_turn_by_game` | table, 2 values | turns | human | all turns of game3, game4 | 549 | models.py, each game held out in turn |
| `ut.upgrade_turn_models` | table, 6 values | share | human | all turns of game3, game4 | 549 | models.py, leave one game out over game3, game4 |
| `ut.upgrade_turn_by_game` | table, 2 values | turns | human | all turns of game3, game4 | 549 | models.py, each game held out in turn |
