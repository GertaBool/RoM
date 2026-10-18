<!-- Rendered by method/docs.py from doctrine.md.in. Do not edit; edit the template. -->
# Doctrine: what the literature asks of the AI, and where it falls short in the logged games

Method: `method/docs/framework.md`. The queries are declared in `study/queries_doctrine.json` and
turned into figures by `tools/sqlfig.py` over the five logged games. Code facts name their file and
line in the DLL source as of the S2 commit (GitLab `e4679cd`, local `38bfd86`). The facts come first
(section 3 and section 4). The readings in section 5 each give the facts they rest on and what would
contradict them. Section 6 ranks the gaps and judges S2 from the higher stations.

This document is the "eagle's view" the work lacked. Each AI change so far was derived from the
game before it, one level down: from a case, to the code, to more code. Here the principles come
first, from the literature, each with its source. Each is then held against measured facts from the
games and located in the AI code. A change should come from a principle and its measured gap, and
after the change it goes back up to the principle to be judged again (Clausewitz, II.5: "the same
means which appeared advisable at one station, when looked at from the next above it may have to be
rejected").

## 1. Sources read

Primary texts, read in full where marked, otherwise in the chapters cited:

- Clausewitz, *On War* (Graham translation): I.1, I.2, II.5, III.8 to III.18, VI.1 to VI.5, VII.4,
  VII.5, VII.22, VIII.4.
- Sun Tzu, *The Art of War* (Giles translation): all thirteen chapters.
- Jomini, *The Art of War* (Mendell and Craighill translation): Art. IV, Art. X, the fundamental
  principle of chapter III, Art. XII, Art. XL.
- Lanchester, *Aircraft in Warfare*: chapters V and VI (concentration, the N-square law).
- Corbett, *Some Principles of Maritime Strategy*: Part I, chapter 4 to chapter 6 (limited war); Part II,
  chapter 1 (command of the sea); Part III, chapter 3 (fleet in being, minor counter-attacks).
- Mahan, *The Influence of Sea Power upon History*: the introductory chapters on concentration and
  coast defence, commerce-destroying.
- Adam Smith, *The Wealth of Nations*: Book II, chapter 3 (accumulation of capital); Book V,
  chapter 1, part I (the expense of defence).
- Sinha, Fang, An, Kiekintveld, Tambe: the IJCAI survey of Stackelberg security games.
- Branavan, Silver, Barzilay: *Learning to Win by Reading Manuals in a Monte-Carlo Framework* (JAIR).
- Lakatos, the methodology of scientific research programmes (the SEP entry).

John Boyd (*Patterns of Conflict*, *Destruction and Creation*) is *open*: every host that serves the
texts failed from this machine, and the doctrine does not quote him from memory.

## 2. Principles and questions

Each principle is stated with its sources, then the question it puts to the games and the source
that answers it.

- **D1. The weak must always be armed: readiness, not the enemy's not coming.**
  - Sun Tzu VIII.11: "rely not on the likelihood of the enemy's not coming, but on our own readiness
    to receive him".
  - Clausewitz VI.5: "it is just the weak, or that side which must defend itself, which should be
    always armed in order not to be taken by surprise".
  - Corbett III.3, on the surprise attack made before declaration: relations "had been highly
    strained ... the Russians had taken no precautions", and "the great power of even the flimsiest
    defence against such attacks".
  - Question: do the human's targets fall before they can react? Answered in `staging.md` from the
    `W`, `K` and `Y` lines; S2 (prediction P4) is the change built from it.
- **D2. Time favours the side whose economy compounds, so the other side must act before.**
  - Clausewitz I.1 §13: if waiting favours one side, "the other has a manifest interest to act
    without delay".
  - Clausewitz III.16: the tame mode of war works "only under the tacit condition that the adversary
    does no better".
  - Smith II.3: "Parsimony, and not industry, is the immediate cause of the increase of capital".
  - Smith V.1.1: "an industrious, and, upon that account, a wealthy nation, is of all nations the
    most likely to be attacked". And in modern war the expense of arms favours "the nation which can
    best afford that expense".
  - Question: when does the human's economy pull away from the AIs'? Source: `M` lines.
- **D3. The balance of power: the leader's victims find friends.**
  - Clausewitz VII.22: the danger that threatens the state "rouses other powers to its protection".
  - Clausewitz VIII.4: "envy, jealousy, anxiety for self ... raise up for him on the one hand
    friends".
  - Jomini Art. X: a state at war with two "will be extremely unfortunate if it does not find an ally
    to come to its aid, with a view to its own safety and the maintenance of the political
    equilibrium".
  - Sun Tzu XI.54 and XI.55, from the leader's side: prevent the joining of allies; do not "foster
    the power of other states".
  - Questions: do the AIs ever declare on the human, or on the leader? Did a third party with the
    power to intervene stand by when the human struck? Sources: `W` and `M` lines.
- **D4. Defence includes the counterstroke; a limited war is answered at the heart.**
  - Clausewitz VI.5: the counterstroke, "the flashing sword of vengeance", is "the most brilliant
    point in the defensive".
  - Corbett I.4: against a limited war between neighbours, the enemy can "pass to unlimited war ...
    and, ignoring the territorial objective, to strike at the heart" (Austerlitz).
  - Corbett I.6: limited war succeeds by controlling the force the enemy brings, which depends on
    "the nature and extent of his preoccupations elsewhere".
  - Mahan: coast defence that goes "to meet the enemy's fleet".
  - The security-games survey: defence is "a combination of defensive actions, offensive actions,
    and information seeking actions".
  - Question: do the AIs fight back, or take back what they lost? Sources: `C` and `K` lines.
- **D5. Concentration, in place and in time; force spent piecemeal is wasted.**
  - Lanchester §28: forces met separately count as the square root of the sum of their squares, so
    junction is the whole matter.
  - Lanchester §34 and §35: forces brought in successively are worth only the hypotenuse; a small
    force facing an overwhelming one is impotent "in the open", but not when "dug in".
  - Clausewitz III.11 and III.12: keep the forces concentrated, and apply them simultaneously.
  - Jomini, the fundamental principle: throw the mass upon the decisive point.
  - Question: how do the two sides attack: many blows on one plot in one turn, or single ones?
    Source: `C` lines. The game's combat is a series of duels, but damage persists until the unit
    heals at the start of its owner's turn (`CvUnit::doTurn`, `CvUnit.cpp:730`, which calls
    `doHeal` at `CvUnit.cpp:776`), and each attack meets the plot's best defender afresh
    (`CvUnit.cpp:1382`). So blows concentrated in one turn wear a garrison down, as fire does in
    Lanchester's model.
- **D6. Read the adversary from what he does and what he prepares.**
  - Clausewitz I.1 §7: each side forms an opinion of the other "from what he is and what he does".
  - Clausewitz III.18: tension begins with preparations alone.
  - Sun Tzu IX.24: "humble words and increased preparations are signs that the enemy is about to
    advance".
  - The security-games survey: the attacker "is able to observe and learn the defender's strategy",
    and a bounded-rational attacker's choices can be fitted from its observed attacks.
  - Question: how does the human manage the AIs' attitudes while it prepares? Sources: `D` lines
    (deals), `E` lines (diplomacy events), the save's memory table.
- **D7. Economy of force: no part idle.**
  - Clausewitz III.14: whoever has forces where the enemy does not employ them "is a bad manager of
    his forces".
  - Smith V.1.1: the late empire dispersed its legions "in small bodies through the different
    provincial towns", and they decayed into a militia.
  - Jomini Art. XL: do not try to cover every point; arrange signals, and rapidly concentrate all
    the disposable force at the point of landing.
  - Question: where were the AIs' armies when their cities fell? *Open* beyond Frisia in game 5
    (`staging.md`, section 2.4): unit positions come only from the `L` lines, which only game 5 has.

## 3. The facts

Setup, from the `H` lines and each game's analysis (`games/game1` to `games/game5`): every game is
played at Marathon speed and at Noble, except game 4 at Monarch. Game 5's header was written during
setup and lacks the map size (`games/game5/analysis.md`). In every game a single human plays against
AI players on their own teams.

### 3.1 The economies over time (D2)

The human against the living AI players at fixed turns. Game 1 and game 2 have no `M` lines.

| turn | human_commerce | ai_median_commerce | ai_max_commerce | human_hammers | ai_median_hammers | human_cities | ai_median_cities | human_power | ai_max_power | human_score_rank | players |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 21 | 21.0 | 28 | 4 | 3.0 | 1 | 1.0 | 11 | 11 | 7 | 18 |
| 100 | 28 | 24.0 | 35 | 20 | 8.0 | 1 | 1.0 | 34 | 24 | 2 | 18 |
| 150 | 55 | 38.0 | 60 | 36 | 21.0 | 4 | 3.0 | 59 | 49 | 2 | 18 |
| 200 | 89 | 48.0 | 133 | 109 | 47.0 | 5 | 4.0 | 128 | 118 | 3 | 18 |
| 250 | 828 | 111.0 | 359 | 522 | 106.0 | 13 | 5.0 | 483 | 351 | 1 | 18 |

*category; who: the human and the living AI players (players below 50, with at least one city); turn: turns 50, 100, 150, 200 and 250, where logged; rows counted: 5; source: M lines (end of each player turn): commerce, hammers, cities, power and score; the human's rank by score among the living players (1 = highest). Game 1 and game 2 have no M lines [game3]. Every value counted (5).*

| turn | human_commerce | ai_median_commerce | ai_max_commerce | human_hammers | ai_median_hammers | human_cities | ai_median_cities | human_power | ai_max_power | human_score_rank | players |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 21 | 22.5 | 27 | 6 | 3.0 | 1 | 1.0 | 13 | 15 | 5 | 19 |
| 100 | 22 | 30.0 | 41 | 21 | 7.0 | 3 | 1.5 | 25 | 32 | 3 | 19 |
| 150 | 43 | 44.5 | 65 | 49 | 21.0 | 5 | 3.0 | 59 | 59 | 1 | 19 |
| 200 | 146 | 75.5 | 208 | 109 | 46.0 | 8 | 5.0 | 149 | 146 | 1 | 19 |
| 250 | 777 | 173.5 | 397 | 532 | 149.5 | 11 | 7.0 | 441 | 543 | 2 | 19 |

*category; who: the human and the living AI players (players below 50, with at least one city); turn: turns 50, 100, 150, 200 and 250, where logged; rows counted: 5; source: M lines (end of each player turn): commerce, hammers, cities, power and score; the human's rank by score among the living players (1 = highest). Game 1 and game 2 have no M lines [game4]. Every value counted (5).*

| turn | human_commerce | ai_median_commerce | ai_max_commerce | human_hammers | ai_median_hammers | human_cities | ai_median_cities | human_power | ai_max_power | human_score_rank | players |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 26 | 22.0 | 30 | 5 | 3.0 | 1 | 1.0 | 15 | 15 | 7 | 19 |
| 100 | 24 | 25.0 | 36 | 16 | 6.5 | 1 | 1.0 | 28 | 26 | 3 | 19 |
| 150 | 37 | 38.5 | 56 | 38 | 16.5 | 4 | 3.0 | 41 | 47 | 2 | 19 |
| 200 | 133 | 60.5 | 140 | 135 | 43.0 | 7 | 4.0 | 117 | 143 | 1 | 19 |
| 250 | 1041 | 154.5 | 430 | 634 | 120.5 | 17 | 7.0 | 485 | 443 | 1 | 17 |

*category; who: the human and the living AI players (players below 50, with at least one city); turn: turns 50, 100, 150, 200 and 250, where logged; rows counted: 5; source: M lines (end of each player turn): commerce, hammers, cities, power and score; the human's rank by score among the living players (1 = highest). Game 1 and game 2 have no M lines [game5]. Every value counted (5).*

### 3.2 The AIs' declarations of war (D3)

Every declaration by an AI team, with the score leader of that turn, where known:

| turn | team | target | on_human | leader_team | human_leads |
|---|---|---|---|---|---|
| 152 | 16 | 2 | 0 | -1 | 0 |

*category; who: every AI team's declaration of war; turn: each AI declaration; rows counted: 1; source: W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game1]. Every value counted (1).*

| turn | team | target | on_human | leader_team | human_leads |
|---|---|---|---|---|---|
| 150 | 3 | 1 | 0 | -1 | 0 |
| 159 | 17 | 5 | 0 | -1 | 0 |
| 172 | 12 | 5 | 0 | -1 | 0 |
| 184 | 3 | 17 | 0 | -1 | 0 |

*category; who: every AI team's declaration of war; turn: each AI declaration; rows counted: 4; source: W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game2]. Every value counted (4).*

| turn | team | target | on_human | leader_team | human_leads |
|---|---|---|---|---|---|
| 124 | 16 | 2 | 0 | 16 | 0 |
| 159 | 1 | 7 | 0 | 13 | 0 |
| 240 | 14 | 5 | 0 | 12 | 1 |
| 245 | 2 | 4 | 0 | 12 | 1 |
| 258 | 17 | 2 | 0 | 12 | 1 |
| 264 | 15 | 8 | 0 | 12 | 1 |

*category; who: every AI team's declaration of war; turn: each AI declaration; rows counted: 6; source: W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game3]. Every value counted (6).*

| turn | team | target | on_human | leader_team | human_leads |
|---|---|---|---|---|---|
| 174 | 14 | 2 | 0 | 3 | 1 |
| 187 | 4 | 2 | 0 | 3 | 1 |
| 188 | 5 | 10 | 0 | 3 | 1 |
| 195 | 6 | 4 | 0 | 3 | 1 |
| 198 | 14 | 6 | 0 | 3 | 1 |
| 222 | 2 | 14 | 0 | 3 | 1 |
| 244 | 15 | 14 | 0 | 3 | 1 |
| 246 | 7 | 15 | 0 | 11 | 0 |
| 253 | 4 | 6 | 0 | 3 | 1 |
| 253 | 8 | 1 | 0 | 3 | 1 |
| 253 | 12 | 13 | 0 | 3 | 1 |

*category; who: every AI team's declaration of war; turn: each AI declaration; rows counted: 11; source: W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game4]. Every value counted (11).*

| turn | team | target | on_human | leader_team | human_leads |
|---|---|---|---|---|---|
| 133 | 14 | 2 | 0 | 0 | 1 |
| 207 | 8 | 1 | 0 | 0 | 1 |
| 250 | 4 | 2 | 0 | 0 | 1 |
| 258 | 6 | 14 | 0 | 0 | 1 |

*category; who: every AI team's declaration of war; turn: each AI declaration; rows counted: 4; source: W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game5]. Every value counted (4).*

### 3.3 The third parties when the human struck (D3)

At each declaration of the human: its power, the target's, and that of the strongest AI outside the
war.

| turn | target | human_power | target_power | largest_other_ai_power | others_stronger_than_human |
|---|---|---|---|---|---|
| 203 | 5 | 157 | 71 | 120 | 0 |
| 209 | 7 | 219 | 67 | 133 | 0 |

*category; who: the human, the target of each of its declarations, and the other AI players; turn: the turn of each declaration of the human; rows counted: 2; source: W lines declared by the human's team; M lines of that turn: power of the human, summed power of the target team's players, the largest power of an AI player outside the target team, and how many such players had more power than the human. Team of a player as in ai_declarations [game3]. Every value counted (2).*

| turn | target | human_power | target_power | largest_other_ai_power | others_stronger_than_human |
|---|---|---|---|---|---|
| 238 | 14 | 362 | 130 | 378 | 1 |
| 252 | 2 | 487 | 383 | 594 | 2 |
| 257 | 6 | 538 | 235 | 678 | 1 |
| 268 | 7 | 999 | 426 | 779 | 0 |
| 271 | 14 | 1199 | 117 | 811 | 0 |
| 272 | 10 | 1283 | 417 | 819 | 0 |
| 277 | 2 | 1597 | 434 | 876 | 0 |
| 283 | 7 | 1884 | 468 | 955 | 0 |

*category; who: the human, the target of each of its declarations, and the other AI players; turn: the turn of each declaration of the human; rows counted: 8; source: W lines declared by the human's team; M lines of that turn: power of the human, summed power of the target team's players, the largest power of an AI player outside the target team, and how many such players had more power than the human. Team of a player as in ai_declarations [game4]. Every value counted (8).*

| turn | target | human_power | target_power | largest_other_ai_power | others_stronger_than_human |
|---|---|---|---|---|---|
| 210 | 8 | 192 | 126 | 150 | 0 |

*category; who: the human, the target of each of its declarations, and the other AI players; turn: the turn of each declaration of the human; rows counted: 1; source: W lines declared by the human's team; M lines of that turn: power of the human, summed power of the target team's players, the largest power of an AI player outside the target team, and how many such players had more power than the human. Team of a player as in ai_declarations [game5]. Every value counted (1).*

### 3.4 Who fought whom (D4)

Per AI team that fought the human: the attacks of each side and the cities each side took.

| ai_team | human_attacks | ai_attacks | ai_attack_turns | cities_human_took | cities_ai_took | first_combat | last_combat |
|---|---|---|---|---|---|---|---|
| 1 | 7 | 0 | 0 | 3 | 0 | 194 | 195 |
| 7 | 18 | 1 | 1 | 5 | 0 | 186 | 213 |
| 14 | 6 | 0 | 0 | 2 | 0 | 206 | 217 |

*category; who: each AI team that fought the human (barbarians excluded); turn: the whole log; rows counted: 3; source: C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game1]. Every value counted (3).*

| ai_team | human_attacks | ai_attacks | ai_attack_turns | cities_human_took | cities_ai_took | first_combat | last_combat |
|---|---|---|---|---|---|---|---|
| 9 | 8 | 0 | 0 | 4 | 0 | 230 | 236 |
| 11 | 12 | 0 | 0 | 5 | 0 | 229 | 232 |
| 16 | 8 | 0 | 0 | 1 | 0 | 92 | 110 |

*category; who: each AI team that fought the human (barbarians excluded); turn: the whole log; rows counted: 3; source: C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game2]. Every value counted (3).*

| ai_team | human_attacks | ai_attacks | ai_attack_turns | cities_human_took | cities_ai_took | first_combat | last_combat |
|---|---|---|---|---|---|---|---|
| 5 | 5 | 0 | 0 | 5 | 0 | 203 | 206 |
| 7 | 9 | 0 | 0 | 1 | 0 | 211 | 213 |

*category; who: each AI team that fought the human (barbarians excluded); turn: the whole log; rows counted: 2; source: C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game3]. Every value counted (2).*

| ai_team | human_attacks | ai_attacks | ai_attack_turns | cities_human_took | cities_ai_took | first_combat | last_combat |
|---|---|---|---|---|---|---|---|
| 2 | 38 | 1 | 1 | 6 | 0 | 252 | 285 |
| 6 | 3 | 0 | 0 | 1 | 0 | 257 | 257 |
| 7 | 15 | 0 | 0 | 4 | 0 | 268 | 285 |
| 10 | 2 | 0 | 0 | 1 | 0 | 272 | 272 |
| 14 | 22 | 0 | 0 | 4 | 0 | 238 | 273 |

*category; who: each AI team that fought the human (barbarians excluded); turn: the whole log; rows counted: 5; source: C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game4]. Every value counted (5).*

| ai_team | human_attacks | ai_attacks | ai_attack_turns | cities_human_took | cities_ai_took | first_combat | last_combat |
|---|---|---|---|---|---|---|---|
| 8 | 26 | 1 | 1 | 8 | 0 | 210 | 224 |

*category; who: each AI team that fought the human (barbarians excluded); turn: the whole log; rows counted: 1; source: C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game5]. Every value counted (1).*

### 3.5 How each side attacked (D5)

Attacks grouped by the plot attacked and the turn:

| side | attacks | plot_turns | plot_turns_attacked_once | attacks_in_groups_of_3_plus | attacks_into_cities | median_odds |
|---|---|---|---|---|---|---|
| AI attacks on the human | 1 | 1 | 1 | 0 | 0 | 765.0 |
| human attacks | 31 | 20 | 14 | 9 | 27 | 818.0 |

*category; who: the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded); turn: the whole log; rows counted: 2; source: C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game1]. Every value counted (2).*

| side | attacks | plot_turns | plot_turns_attacked_once | attacks_in_groups_of_3_plus | attacks_into_cities | median_odds |
|---|---|---|---|---|---|---|
| human attacks | 28 | 20 | 16 | 10 | 18 | 996.0 |

*category; who: the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded); turn: the whole log; rows counted: 1; source: C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game2]. Every value counted (1).*

| side | attacks | plot_turns | plot_turns_attacked_once | attacks_in_groups_of_3_plus | attacks_into_cities | median_odds |
|---|---|---|---|---|---|---|
| human attacks | 14 | 7 | 3 | 7 | 14 | 810.5 |

*category; who: the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded); turn: the whole log; rows counted: 1; source: C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game3]. Every value counted (1).*

| side | attacks | plot_turns | plot_turns_attacked_once | attacks_in_groups_of_3_plus | attacks_into_cities | median_odds |
|---|---|---|---|---|---|---|
| AI attacks on the human | 1 | 1 | 1 | 0 | 1 | 471.0 |
| human attacks | 80 | 25 | 9 | 63 | 69 | 978.0 |

*category; who: the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded); turn: the whole log; rows counted: 2; source: C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game4]. Every value counted (2).*

| side | attacks | plot_turns | plot_turns_attacked_once | attacks_in_groups_of_3_plus | attacks_into_cities | median_odds |
|---|---|---|---|---|---|---|
| AI attacks on the human | 1 | 1 | 1 | 0 | 0 | 329.0 |
| human attacks | 26 | 17 | 9 | 3 | 22 | 980.0 |

*category; who: the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded); turn: the whole log; rows counted: 2; source: C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game5]. Every value counted (2).*

### 3.6 Deals and diplomacy with the human (D6)

The items exchanged in deals:

| item | direction | items | partners |
|---|---|---|---|
| TRADE_OPEN_BORDERS | AI gives | 42 | 14 |
| TRADE_OPEN_BORDERS | human gives | 42 | 14 |
| TRADE_PEACE_TREATY | AI gives | 1 | 1 |
| TRADE_PEACE_TREATY | human gives | 1 | 1 |
| TRADE_RESOURCES | AI gives | 2 | 2 |
| TRADE_RESOURCES | human gives | 4 | 2 |
| TRADE_TECHNOLOGIES | AI gives | 1 | 1 |
| TRADE_TECHNOLOGIES | human gives | 2 | 2 |

*category; who: deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714); turn: the whole log; rows counted: 8; source: D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game1]. Every value counted (8).*

| item | direction | items | partners |
|---|---|---|---|
| TRADE_GOLD_PER_TURN | AI gives | 1 | 1 |
| TRADE_OPEN_BORDERS | AI gives | 42 | 14 |
| TRADE_OPEN_BORDERS | human gives | 42 | 14 |
| TRADE_PEACE_TREATY | AI gives | 2 | 2 |
| TRADE_PEACE_TREATY | human gives | 2 | 2 |
| TRADE_RESOURCES | AI gives | 8 | 5 |
| TRADE_RESOURCES | human gives | 13 | 5 |
| TRADE_TECHNOLOGIES | human gives | 2 | 2 |

*category; who: deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714); turn: the whole log; rows counted: 8; source: D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game2]. Every value counted (8).*

| item | direction | items | partners |
|---|---|---|---|
| TRADE_GOLD | AI gives | 4 | 4 |
| TRADE_GOLD_PER_TURN | AI gives | 1 | 1 |
| TRADE_OPEN_BORDERS | AI gives | 51 | 16 |
| TRADE_OPEN_BORDERS | human gives | 51 | 16 |
| TRADE_PEACE_TREATY | AI gives | 6 | 6 |
| TRADE_PEACE_TREATY | human gives | 6 | 6 |
| TRADE_RESOURCES | AI gives | 19 | 7 |
| TRADE_RESOURCES | human gives | 22 | 7 |
| TRADE_TECHNOLOGIES | AI gives | 4 | 4 |
| TRADE_TECHNOLOGIES | human gives | 13 | 10 |

*category; who: deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714); turn: the whole log; rows counted: 10; source: D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game3]. Every value counted (10).*

| item | direction | items | partners |
|---|---|---|---|
| TRADE_GOLD | AI gives | 8 | 7 |
| TRADE_GOLD_PER_TURN | AI gives | 3 | 3 |
| TRADE_OPEN_BORDERS | AI gives | 57 | 17 |
| TRADE_OPEN_BORDERS | human gives | 57 | 17 |
| TRADE_PEACE_TREATY | AI gives | 15 | 11 |
| TRADE_PEACE_TREATY | human gives | 15 | 11 |
| TRADE_RESOURCES | AI gives | 10 | 4 |
| TRADE_RESOURCES | human gives | 13 | 4 |
| TRADE_TECHNOLOGIES | AI gives | 7 | 6 |
| TRADE_TECHNOLOGIES | human gives | 21 | 13 |

*category; who: deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714); turn: the whole log; rows counted: 10; source: D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game4]. Every value counted (10).*

| item | direction | items | partners |
|---|---|---|---|
| TRADE_GOLD_PER_TURN | AI gives | 2 | 2 |
| TRADE_OPEN_BORDERS | AI gives | 42 | 14 |
| TRADE_OPEN_BORDERS | human gives | 42 | 14 |
| TRADE_PEACE_TREATY | AI gives | 5 | 4 |
| TRADE_PEACE_TREATY | human gives | 5 | 4 |
| TRADE_RESOURCES | AI gives | 11 | 5 |
| TRADE_RESOURCES | human gives | 17 | 6 |
| TRADE_TECHNOLOGIES | AI gives | 3 | 3 |
| TRADE_TECHNOLOGIES | human gives | 10 | 7 |

*category; who: deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714); turn: the whole log; rows counted: 9; source: D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game5]. Every value counted (9).*

The deals in which one side gave nothing:

| kind | deals | human_gives_tech | ai_gives_tech | partners |
|---|---|---|---|---|
| exchange | 46 | 1 | 1 | 14 |
| human gives, nothing back | 1 | 1 | 0 | 1 |

*category; who: deals between the human and AI players; turn: the whole log; rows counted: 2; source: D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game1]. Every value counted (2).*

| kind | deals | human_gives_tech | ai_gives_tech | partners |
|---|---|---|---|---|
| exchange | 51 | 0 | 0 | 14 |
| human gives, nothing back | 2 | 2 | 0 | 2 |

*category; who: deals between the human and AI players; turn: the whole log; rows counted: 2; source: D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game2]. Every value counted (2).*

| kind | deals | human_gives_tech | ai_gives_tech | partners |
|---|---|---|---|---|
| exchange | 82 | 8 | 4 | 16 |
| human gives, nothing back | 5 | 5 | 0 | 5 |

*category; who: deals between the human and AI players; turn: the whole log; rows counted: 2; source: D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game3]. Every value counted (2).*

| kind | deals | human_gives_tech | ai_gives_tech | partners |
|---|---|---|---|---|
| exchange | 91 | 10 | 7 | 17 |
| human gives, nothing back | 10 | 10 | 0 | 8 |

*category; who: deals between the human and AI players; turn: the whole log; rows counted: 2; source: D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game4]. Every value counted (2).*

| kind | deals | human_gives_tech | ai_gives_tech | partners |
|---|---|---|---|---|
| exchange | 61 | 3 | 3 | 14 |
| human gives, nothing back | 5 | 5 | 0 | 4 |

*category; who: deals between the human and AI players; turn: the whole log; rows counted: 2; source: D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game5]. Every value counted (2).*

The diplomacy events between the human and the AIs:

| diplo_event | events | senders |
|---|---|---|
| DIPLOEVENT_AI_CONTACT | 26 | 15 |
| DIPLOEVENT_CONTACT | 17 | 10 |
| DIPLOEVENT_GIVE_HELP | 1 | 1 |
| DIPLOEVENT_NO_JOIN_WAR | 1 | 1 |
| DIPLOEVENT_NO_REVOLUTION | 1 | 1 |
| DIPLOEVENT_NO_STOP_TRADING | 5 | 4 |
| DIPLOEVENT_REFUSED_HELP | 2 | 2 |

*category; who: diplomacy between the human and AI players; turn: the whole log; rows counted: 7; source: E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game1]. Every value counted (7).*

| diplo_event | events | senders |
|---|---|---|
| DIPLOEVENT_AI_CONTACT | 65 | 17 |
| DIPLOEVENT_CONTACT | 25 | 12 |
| DIPLOEVENT_GIVE_HELP | 2 | 2 |
| DIPLOEVENT_NO_JOIN_WAR | 5 | 4 |
| DIPLOEVENT_NO_STOP_TRADING | 5 | 4 |
| DIPLOEVENT_REFUSED_HELP | 16 | 14 |

*category; who: diplomacy between the human and AI players; turn: the whole log; rows counted: 6; source: E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game2]. Every value counted (6).*

| diplo_event | events | senders |
|---|---|---|
| DIPLOEVENT_AI_CONTACT | 88 | 17 |
| DIPLOEVENT_CONTACT | 42 | 15 |
| DIPLOEVENT_CONVERT | 1 | 1 |
| DIPLOEVENT_GIVE_HELP | 5 | 5 |
| DIPLOEVENT_NO_JOIN_WAR | 6 | 5 |
| DIPLOEVENT_NO_STOP_TRADING | 11 | 7 |
| DIPLOEVENT_REFUSED_HELP | 11 | 10 |

*category; who: diplomacy between the human and AI players; turn: the whole log; rows counted: 7; source: E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game3]. Every value counted (7).*

| diplo_event | events | senders |
|---|---|---|
| DIPLOEVENT_AI_CONTACT | 102 | 18 |
| DIPLOEVENT_CONTACT | 66 | 14 |
| DIPLOEVENT_GIVE_HELP | 10 | 8 |
| DIPLOEVENT_NO_CONVERT | 2 | 2 |
| DIPLOEVENT_NO_JOIN_WAR | 9 | 8 |
| DIPLOEVENT_NO_STOP_TRADING | 9 | 6 |
| DIPLOEVENT_REFUSED_HELP | 12 | 11 |

*category; who: diplomacy between the human and AI players; turn: the whole log; rows counted: 7; source: E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game4]. Every value counted (7).*

| diplo_event | events | senders |
|---|---|---|
| DIPLOEVENT_AI_CONTACT | 54 | 15 |
| DIPLOEVENT_CONTACT | 13 | 6 |
| DIPLOEVENT_DO_NOT_BOTHER | 2 | 2 |
| DIPLOEVENT_GIVE_HELP | 5 | 4 |
| DIPLOEVENT_NO_JOIN_WAR | 2 | 2 |
| DIPLOEVENT_NO_STOP_TRADING | 2 | 2 |
| DIPLOEVENT_REFUSED_HELP | 7 | 6 |
| DIPLOEVENT_RESUME_BOTHER | 2 | 2 |

*category; who: diplomacy between the human and AI players; turn: the whole log; rows counted: 8; source: E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game5]. Every value counted (8).*

What the AIs remembered of the human when the log ended:

| memory | ai_players | total |
|---|---|---|
| ACCEPTED_RELIGION | 1 | 1 |
| DECLARED_WAR | 2 | 2 |
| DECLARED_WAR_ON_FRIEND | 12 | 17 |
| DENIED_JOIN_WAR | 4 | 4 |
| DENIED_STOP_TRADING | 6 | 9 |
| GIVE_HELP | 4 | 4 |
| RECEIVED_TECH_FROM_ANY | 7 | 13 |
| REFUSED_HELP | 8 | 8 |
| TRADED_TECH_TO_US | 6 | 8 |

*category; who: the AI players' memories of the human; turn: at the save the log ends with; rows counted: 9; source: save dump, memory table (AI_getMemoryCount of each AI towards the human): memory type, AI players holding it, summed count [game3]. Every value counted (9).*

| memory | ai_players | total |
|---|---|---|
| CANCELLED_OPEN_BORDERS | 1 | 1 |
| DECLARED_WAR | 4 | 6 |
| DECLARED_WAR_ON_FRIEND | 15 | 83 |
| DENIED_JOIN_WAR | 6 | 7 |
| DENIED_STOP_TRADING | 3 | 3 |
| GIVE_HELP | 7 | 7 |
| RECEIVED_TECH_FROM_ANY | 17 | 41 |
| REFUSED_HELP | 8 | 9 |
| TRADED_TECH_TO_US | 10 | 14 |

*category; who: the AI players' memories of the human; turn: at the save the log ends with; rows counted: 9; source: save dump, memory table (AI_getMemoryCount of each AI towards the human): memory type, AI players holding it, summed count [game4]. Every value counted (9).*

| memory | ai_players | total |
|---|---|---|
| DECLARED_WAR_ON_FRIEND | 6 | 6 |
| DENIED_JOIN_WAR | 2 | 2 |
| DENIED_STOP_TRADING | 1 | 1 |
| GIVE_HELP | 4 | 5 |
| RECEIVED_TECH_FROM_ANY | 6 | 11 |
| REFUSED_HELP | 4 | 5 |
| TRADED_TECH_TO_US | 6 | 9 |

*category; who: the AI players' memories of the human; turn: at the save the log ends with; rows counted: 7; source: save dump, memory table (AI_getMemoryCount of each AI towards the human): memory type, AI players holding it, summed count [game5]. Every value counted (7).*

### 3.7 Where each AI's decision to go to war on the human fails (D3)

The gates of `CvTeamAI::AI_doWar` at the saves, computed exactly by `HARNESS_WAR_DIAG` (step 1 of
`study/d3-design.md`; for game 6 the save the human sent). Per AI team towards the human:

| player | consider | att | roll_dogpile | can_declare | power_test_passes | ai_power | human_defence |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 3 | 0 | 1 | 0 | 18 | 486 |
| 1 | 0 | 2 | 200 | 1 | 0 | 94 | 486 |
| 2 | 0 | 2 | 200 | 1 | 0 | -111 | 486 |
| 3 | 1 | 3 | 400 | 1 | 0 | 334 | 486 |
| 4 | 0 | 1 | 1000 | 1 | 0 | -217 | 486 |
| 5 | 0 | 3 | 0 | 1 | 0 | -43 | 486 |
| 6 | 1 | 3 | 0 | 1 | 0 | 223 | 486 |
| 7 | 0 | 1 | 800 | 1 | 0 | -146 | 486 |
| 8 | 0 | 2 | 100 | 1 | 0 | -66 | 486 |
| 9 | 1 | 3 | 0 | 1 | 0 | 156 | 486 |
| 10 | 0 | 3 | 0 | 1 | 0 | 133 | 486 |
| 11 | 1 | 3 | 0 | 1 | 0 | 101 | 486 |
| 13 | 1 | 3 | 0 | 1 | 0 | 283 | 486 |
| 14 | 0 | 1 | 800 | 1 | 0 | 26 | 486 |
| 15 | 0 | 1 | 800 | 1 | 0 | 37 | 486 |
| 16 | 0 | 2 | 600 | 1 | 0 | 2 | 486 |
| 17 | 0 | 3 | 100 | 1 | 0 | -84 | 486 |

*category; who: each AI team towards the human's team; turn: at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent); rows counted: 17; source: HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game3]. Every value counted (17).*

| player | consider | att | roll_dogpile | can_declare | power_test_passes | ai_power | human_defence |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 600 | 1 | 0 | 28 | 1529 |
| 1 | 0 | 1 | 600 | 1 | 0 | -358 | 1529 |
| 2 | 1 | 0 | 1000 | 0 | 0 | 163 | 1529 |
| 4 | 0 | 1 | 1000 | 1 | 0 | 37 | 1529 |
| 5 | 1 | 1 | 700 | 1 | 0 | 809 | 1529 |
| 6 | 0 | 2 | 700 | 0 | 0 | -129 | 1529 |
| 7 | 0 | 0 | 1000 | 0 | 0 | -1377 | 1529 |
| 8 | 0 | 3 | 100 | 0 | 0 | 25 | 1529 |
| 9 | 1 | 1 | 600 | 1 | 0 | 412 | 1529 |
| 10 | 0 | 0 | 1000 | 0 | 0 | -1136 | 1529 |
| 11 | 1 | 1 | 600 | 1 | 0 | 900 | 1529 |
| 12 | 0 | 3 | 0 | 0 | 0 | -230 | 1529 |
| 13 | 0 | 2 | 400 | 1 | 0 | 372 | 1529 |
| 15 | 0 | 3 | 50 | 0 | 0 | -123 | 1529 |
| 16 | 0 | 1 | 700 | 1 | 0 | -110 | 1529 |
| 17 | 1 | 2 | 200 | 1 | 0 | 680 | 1529 |
| 18 | 0 | 2 | 200 | 1 | 0 | -240 | 1529 |

*category; who: each AI team towards the human's team; turn: at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent); rows counted: 17; source: HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game4]. Every value counted (17).*

| player | consider | att | roll_dogpile | can_declare | power_test_passes | ai_power | human_defence |
|---|---|---|---|---|---|---|---|
| 2 | 0 | 3 | 0 | 1 | 0 | -114 | 683 |
| 3 | 0 | 3 | 0 | 1 | 0 | 83 | 683 |
| 4 | 0 | 1 | 1000 | 1 | 0 | 87 | 683 |
| 5 | 1 | 3 | 0 | 1 | 0 | 428 | 683 |
| 6 | 0 | 3 | 100 | 0 | 0 | 72 | 683 |
| 7 | 0 | 3 | 0 | 1 | 0 | 115 | 683 |
| 12 | 1 | 3 | 0 | 1 | 0 | 67 | 683 |
| 13 | 0 | 2 | 300 | 1 | 0 | 60 | 683 |
| 14 | 0 | 2 | 600 | 1 | 0 | -74 | 683 |
| 15 | 1 | 2 | 300 | 1 | 0 | 104 | 683 |
| 16 | 1 | 2 | 200 | 1 | 0 | 64 | 683 |
| 17 | 1 | 4 | 0 | 1 | 0 | 390 | 683 |
| 18 | 0 | 2 | 300 | 1 | 0 | 235 | 683 |

*category; who: each AI team towards the human's team; turn: at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent); rows counted: 13; source: HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game5]. Every value counted (13).*

| player | consider | att | roll_dogpile | can_declare | power_test_passes | ai_power | human_defence |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 200 | 1 | 0 | 0 | 360 |
| 2 | 1 | 2 | 100 | 1 | 0 | 126 | 360 |
| 3 | 1 | 1 | 800 | 1 | 0 | 226 | 360 |
| 4 | 0 | 2 | 500 | 1 | 0 | 2 | 360 |
| 5 | 1 | 2 | 100 | 1 | 0 | 167 | 360 |
| 6 | 1 | 3 | 100 | 1 | 0 | 163 | 360 |
| 8 | 0 | 2 | 400 | 1 | 0 | -25 | 360 |
| 9 | 1 | 2 | 100 | 1 | 0 | 122 | 360 |
| 10 | 0 | 2 | 100 | 1 | 0 | -25 | 360 |
| 11 | 1 | 2 | 100 | 0 | 0 | 234 | 360 |
| 14 | 0 | 2 | 600 | 1 | 0 | -49 | 360 |
| 15 | 0 | 2 | 400 | 1 | 0 | -46 | 360 |
| 16 | 1 | 3 | 0 | 1 | 0 | 16 | 360 |
| 18 | 1 | 2 | 200 | 1 | 0 | 130 | 360 |

*category; who: each AI team towards the human's team; turn: at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent); rows counted: 14; source: HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game6]. Every value counted (14).*

The same gates towards the human and towards every AI team, summed:

| side | pairs | power_test_passes | dogpile_roll_can_pass | willing_power | dogpile_bar |
|---|---|---|---|---|---|
| towards AI teams | 287 | 110 | 203 | 26232 | 478.5 |
| towards the human | 17 | 0 | 10 | 493 | 729.0 |

*category; who: every AI team towards the human, and towards every AI team it has met (vassals excluded); turn: at the save, as gates_to_human; rows counted: 2; source: HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game3]. Every value counted (2).*

| side | pairs | power_test_passes | dogpile_roll_can_pass | willing_power | dogpile_bar |
|---|---|---|---|---|---|
| towards AI teams | 281 | 89 | 177 | 32162 | 1350.0 |
| towards the human | 17 | 0 | 16 | 3238 | 2293.5 |

*category; who: every AI team towards the human, and towards every AI team it has met (vassals excluded); turn: at the save, as gates_to_human; rows counted: 2; source: HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game4]. Every value counted (2).*

| side | pairs | power_test_passes | dogpile_roll_can_pass | willing_power | dogpile_bar |
|---|---|---|---|---|---|
| towards AI teams | 241 | 98 | 128 | 19497 | 865.5 |
| towards the human | 13 | 0 | 7 | 550 | 1024.5 |

*category; who: every AI team towards the human, and towards every AI team it has met (vassals excluded); turn: at the save, as gates_to_human; rows counted: 2; source: HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game5]. Every value counted (2).*

| side | pairs | power_test_passes | dogpile_roll_can_pass | willing_power | dogpile_bar |
|---|---|---|---|---|---|
| towards AI teams | 244 | 126 | 133 | 11727 | 448.5 |
| towards the human | 14 | 0 | 13 | 936 | 540.0 |

*category; who: every AI team towards the human, and towards every AI team it has met (vassals excluded); turn: at the save, as gates_to_human; rows counted: 2; source: HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game6]. Every value counted (2).*

## 4. The code at each principle

- **Where an AI chooses a war** (D2, D3): `CvTeamAI::AI_doWar` (`CvTeamAI.cpp:4746`). Each of its
  three paths needs the target to be weaker than the AI:
  - a total war needs the target's defensive power (two thirds of it, or its reachable defence in
    cunning mode) below a ratio of the AI's own (`CvTeamAI.cpp:5259` to `CvTeamAI.cpp:5270`);
  - a limited war has the same test with the limited-war ratio (`CvTeamAI.cpp:5347` to
    `CvTeamAI.cpp:5354`);
  - a dogpile war is the only coalition path: it adds the power of every team already at war with
    the target, and needs that sum to exceed one and a half times the target's defence
    (`CvTeamAI.cpp:5412` to `CvTeamAI.cpp:5440`).

  Every path first needs a random roll at or above the leader's `NoWarAttitudeProbs` for its
  attitude to the target (`AI_noWarAttitudeProb`, `CvTeamAI.cpp:4598`, from the `LeaderHeadInfo`
  records). The pleasanter the attitude, the less likely the war.
- **What makes a target attractive** (D3): `CvTeamAI::AI_startWarVal` (`CvTeamAI.cpp:1232`). It
  counts plot value, capital proximity, closeness and resources. A target is weighted for being
  ahead only when it pursues a victory strategy at level three or four. When the AI is already at
  war, or follows the early conquest strategy, the value is scaled by the AI's power over the
  target's defensive power, so weak targets are preferred.
- **Envy of the leader** (D3): the attitude term on rank (`CvPlayerAI::AI_getAttitudeVal`,
  `CvPlayerAI.cpp:7444`). It is the leader's `iWorseRankDifferenceAttitudeChange` times the rank
  difference, divided by the number of civilisations ever alive plus one, so its size is bounded by
  that one field.
- **Open borders** (D6): `CvTeamAI::AI_openBordersTrade` (`CvTeamAI.cpp:3446`) refuses only after a
  recent cancellation, to the worst enemy, or below the leader's attitude threshold. Neither the
  other side's power, nor its units near the border, nor its rank count.
- **Posture in an area at war** (D4): `CvTeamAI::AI_calculateAreaAIType` (`CvTeamAI.cpp:409`).
  - The area turns defensive when the AI's power there is below the enemy's and the AI has been
    losing (`CvTeamAI.cpp:518`), or below half the enemy's (`CvTeamAI.cpp:529`).
  - After a recent attack it masses only if its power there exceeds the enemy's, and otherwise turns
    defensive (`CvTeamAI.cpp:619`).
- **City danger and defenders** (D1): `staging.md`, section 2.3, and the S2 change
  (`AI_stagedForecast`, `builds/staging/README.md`).

## 5. Readings

- **R1. Time is on the human's side: its lead in hammers comes early, its lead in commerce between
  the last two rows of each economy table** (D2).
  - Facts: section 3.1. In the first rows the human's commerce is near the AI median. Its hammers
    are ahead of the median from the second row. In the last row its commerce is several times the
    median and above the best AI's, its hammers several times the median, and its cities have
    multiplied.
  - In game 4 and game 5 the human is first or second in score from the middle rows on. Those last rows come
    after its wars (`staging.md`, section 2.1), so the cities it took feed the lead (Sun Tzu II:
    "using the conquered foe to augment one's own strength").
  - Contradicted if a game shows the human's commerce pulling away before its first war, or the AI
    median keeping pace after it.
- **R2. No balance of power ever forms against the human** (D3).
  - Facts: section 3.2. The AI teams declared war among themselves in every game, never on the
    human, even on turns when the human was the score leader (`human_leads`).
  - Section 3.3 (game 3 to game 5): when the human struck, the target was always weaker than the human, and in the
    early wars of game 4 at least one AI outside the war was stronger than the human. None of them
    joined.
  - Code: section 4. Every war path wants a weaker target. The only coalition path (dogpile) adds
    the target's enemies' power, but it is gated by attitude like the others. A target counts for
    being ahead only near a victory.
  - Section 3.7, at the saves: no power test of any AI team towards the human passes, while towards
    AI teams they pass for many pairs. Many teams would pass the attitude roll towards the human, so
    at the end of these games the block is power, not attitude. Each AI alone is too weak, and the
    dogpile test counts only teams already at war with the human. The teams whose roll can pass,
    taken together, reach the dogpile bar at the saves of game 4 and game 6 but not of game 3 and
    game 5. These are late saves; the gates at the time of the human's first wars are *open*.
  - Contradicted if a game shows an AI declaring on the human, or joining one of the human's wars.
- **R3. The human keeps the AIs pleased while it prepares** (D6).
  - Facts: section 3.6. It holds open borders with almost every AI. Its one-sided deals are
    technologies it gives (`GIVE_HELP`): the AI asks and the human grants some requests and refuses
    others (`REFUSED_HELP`).
  - Overall it gives more technologies than it receives. That is Sun Tzu's "humble words and
    increased preparations" (IX.24), not fostering the human's power through trade (XI.55): the AIs
    do not feed the human; the human buys their attitude.
  - In the code, attitude decides the war roll and open borders (section 4). The open borders also
    give the human passage and sight for staging (`staging.md`).
  - What the AIs remember of the human at the end includes `DECLARED_WAR_ON_FRIEND`, held by several
    AIs in each game: they keep the grievance and do nothing about it.
  - Contradicted if the human's gifts do not come before its wars or do not go to the AIs that could
    have joined against it. That timing is not yet measured and is *open*.
- **R4. The AI never strikes back** (D4).
  - Facts: section 3.4. In every war the AI side attacked the human's units almost never, and took
    no city back. The human's attacks are many times the AI's.
  - The human's wars are limited wars in Corbett's sense. It chooses targets preoccupied elsewhere
    (`staging.md`, section 2.1), takes a few cities, and is never answered at its own cities.
  - Code: the area posture turns defensive whenever the enemy's power in the area exceeds the AI's
    (section 4).
  - Why the AI's units did not attack is *open*. The war log does not record the area AI type or the
    units' missions, except game 5's `L` lines.
  - Contradicted if the BBAI log of a replayed war shows the AI's area offensive or massing while its
    units still did not attack.
- **R5. The human concentrates in time; the AI attacks alone** (D5).
  - Facts: section 3.5. Most of the human's attacks go into cities. In game 4 most of them, and in
    game 3 half, are made in groups of three or more on one plot in one turn. Its median odds are high:
    "the victorious strategist only seeks battle after the victory has been won" (Sun Tzu IV.15).
  - The AI's few attacks were each the only attack on their plot that turn, and in game 4 and game 5
    at odds below even. That is Lanchester's piecemeal force.
  - Contradicted if more games show AI attacks on the human in groups.

## 6. Ranking the gaps, and S2 seen from above

The ranking criterion is the mission: beat an expert human at Noble while each leader keeps its
character. A gap ranks higher the more of the human's method it would defeat, and the earlier in the
game it acts.

1. **D3, the balance against the leader (R2, with R3).** It is the only gap that acts before the
   human's lead compounds (R1). It also turns the human's preferred target, an AI preoccupied
   elsewhere, from an opportunity into a risk. Today the attitude the human can buy decides it.
   Each leader's character survives a fix: attitude and war probabilities stay per leader, and the
   question is whether being the leader, or striking a neighbour, enters the calculation at all.
2. **D4, the counterstroke (R4).** A limited war is cheap only while no one answers it at the heart
   (Corbett I.4). An AI that strikes the human's own cities, or recaptures, makes every war cost
   the human what it gains.
3. **D1, readiness (S2).** It denies the capture on the declaration turn, the human's cheapest win.
   Without it, D3 and D4 come too late, because a city taken at once cannot be defended afterwards.
4. **D5, concentration (R5).** It matters once the AI does attack (D4), so it comes after it.
5. **D2, the economy (R1).** It is not a separate lever. The human's economic lead follows from its
   conquests, so closing D1, D3 and D4 closes much of it. Building better on its own does not:
   Smith's wealthy nation without "some new measure for the public defence" is the most attacked.
6. **D6 and D7** are means for the others: reading the human's preparations serves D1 and D3, and
   economy of force serves D4.

**S2, judged from each station.**

- At the station of the city it is right. In the harness replay of the game 6 save, the Sumerian
  city facing a Persian force at peace raises its defenders and its forecast falls; with S2 off it
  stays at one defender (`builds/staging/provenance.json`, `tested_headless`).
- At the station of the war it is necessary but not sufficient. A garrison in every threatened city
  is the late empire's militia (Smith V.1.1), and it makes the AI "everywhere weak" (Sun Tzu VI.18).
  It needs the mobile counterstroke behind it (D4) and the warning that tells that force where to go
  (Jomini XL; D6).
- At the station of the game it does not touch the cause. The human chooses when to fight because no
  one makes it fight earlier (D3).

So S2 was the right first move, because it is the lowest station and the others build on it. It was
not chosen from this view, and the next changes should be D3 and then D4, not more refinement of the
garrison. Lakatos's test applies to this sequence of changes: it is progressive only if each change
predicts something new that then holds. P2 and P4 (S2) predict fewer captures by the human; neither is
judged yet, because only one game so far has the snapshot lines a judgment needs.

## 7. Judged predictions

The gate (`method/ledger.py`, config `doctrine`) holds every new hypothesis to a principle of
section 2 and a reading of section 5. Each prediction decided by enough evidence to move its
line is stated here as `P..: <status>`, with what it changes in section 5 and section 6. None is decided
yet: P2 and P4 are open.

## 8. Open

- Boyd's texts (section 1).
- D7: where the AIs' armies stood when their cities fell, beyond game 5 (needs `L` lines).
- R3: the timing of the human's gifts relative to its wars, and to whom they went.
- R4: why the AI's units did not attack (needs the area AI and missions per turn, from a replay with
  the BBAI log).
- The meaning of the `TRADE_PEACE_TREATY` items in deals with players the human never fought
  (game 5).
- Game 6 (Ragnar) is a save without a war log, so it enters only through the S2 test of its save.
- Game 1 and game 2 have no `M` lines, so D2 and the leader column of D3 rest on game 3 to game 5.

## Figures used

| Figure | Value | Unit | Who | Turn | n | Source |
|---|---|---|---|---|---|---|
| `d.game3_economy` | table, 5 values | category | the human and the living AI players (players below 50, with at least one city) | turns 50, 100, 150, 200 and 250, where logged | 5 | M lines (end of each player turn): commerce, hammers, cities, power and score; the human's rank by score among the living players (1 = highest). Game 1 and game 2 have no M lines [game3] |
| `d.game4_economy` | table, 5 values | category | the human and the living AI players (players below 50, with at least one city) | turns 50, 100, 150, 200 and 250, where logged | 5 | M lines (end of each player turn): commerce, hammers, cities, power and score; the human's rank by score among the living players (1 = highest). Game 1 and game 2 have no M lines [game4] |
| `d.game5_economy` | table, 5 values | category | the human and the living AI players (players below 50, with at least one city) | turns 50, 100, 150, 200 and 250, where logged | 5 | M lines (end of each player turn): commerce, hammers, cities, power and score; the human's rank by score among the living players (1 = highest). Game 1 and game 2 have no M lines [game5] |
| `d.game1_ai_declarations` | table, 1 values | category | every AI team's declaration of war | each AI declaration | 1 | W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game1] |
| `d.game2_ai_declarations` | table, 4 values | category | every AI team's declaration of war | each AI declaration | 4 | W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game2] |
| `d.game3_ai_declarations` | table, 6 values | category | every AI team's declaration of war | each AI declaration | 6 | W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game3] |
| `d.game4_ai_declarations` | table, 11 values | category | every AI team's declaration of war | each AI declaration | 11 | W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game4] |
| `d.game5_ai_declarations` | table, 4 values | category | every AI team's declaration of war | each AI declaration | 4 | W lines whose declaring team is not the human's; the score leader of that turn from M lines (highest score, ties to the lower player id; -1 where the log has no M lines: game 1 and game 2). A player's team is its P line's team, or its id where the log has no P line for it (game 5) [game5] |
| `d.game3_third_parties` | table, 2 values | category | the human, the target of each of its declarations, and the other AI players | the turn of each declaration of the human | 2 | W lines declared by the human's team; M lines of that turn: power of the human, summed power of the target team's players, the largest power of an AI player outside the target team, and how many such players had more power than the human. Team of a player as in ai_declarations [game3] |
| `d.game4_third_parties` | table, 8 values | category | the human, the target of each of its declarations, and the other AI players | the turn of each declaration of the human | 8 | W lines declared by the human's team; M lines of that turn: power of the human, summed power of the target team's players, the largest power of an AI player outside the target team, and how many such players had more power than the human. Team of a player as in ai_declarations [game4] |
| `d.game5_third_parties` | table, 1 values | category | the human, the target of each of its declarations, and the other AI players | the turn of each declaration of the human | 1 | W lines declared by the human's team; M lines of that turn: power of the human, summed power of the target team's players, the largest power of an AI player outside the target team, and how many such players had more power than the human. Team of a player as in ai_declarations [game5] |
| `d.game1_fighting` | table, 3 values | category | each AI team that fought the human (barbarians excluded) | the whole log | 3 | C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game1] |
| `d.game2_fighting` | table, 3 values | category | each AI team that fought the human (barbarians excluded) | the whole log | 3 | C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game2] |
| `d.game3_fighting` | table, 2 values | category | each AI team that fought the human (barbarians excluded) | the whole log | 2 | C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game3] |
| `d.game4_fighting` | table, 5 values | category | each AI team that fought the human (barbarians excluded) | the whole log | 5 | C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game4] |
| `d.game5_fighting` | table, 1 values | category | each AI team that fought the human (barbarians excluded) | the whole log | 1 | C lines between the human's units and an AI team's (attacks by each side, the turns on which the AI attacked), K lines between them (cities taken by each side), first and last combat turn. Team of a player as in ai_declarations [game5] |
| `d.game1_concentration` | table, 2 values | category | the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded) | the whole log | 2 | C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game1] |
| `d.game2_concentration` | table, 1 values | category | the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded) | the whole log | 1 | C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game2] |
| `d.game3_concentration` | table, 1 values | category | the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded) | the whole log | 1 | C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game3] |
| `d.game4_concentration` | table, 2 values | category | the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded) | the whole log | 2 | C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game4] |
| `d.game5_concentration` | table, 2 values | category | the human's attacks on AI units, and AI attacks on the human's units (barbarians excluded) | the whole log | 2 | C lines: attacks grouped by side and by (turn, plot attacked); plot-turns attacked once, attacks made in groups of three or more on one plot in one turn, attacks into a city (city defence modifier logged), and the median attacker's odds (getCombatOdds, per thousand) [game5] |
| `d.game1_deals` | table, 8 values | category | deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714) | the whole log | 8 | D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game1] |
| `d.game2_deals` | table, 8 values | category | deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714) | the whole log | 8 | D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game2] |
| `d.game3_deals` | table, 10 values | category | deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714) | the whole log | 10 | D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game3] |
| `d.game4_deals` | table, 10 values | category | deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714) | the whole log | 10 | D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game4] |
| `d.game5_deals` | table, 9 values | category | deals between the human and AI players (the war log writes no deal between two AIs: warLogDeal, CvGameCoreUtils.cpp:3714) | the whole log | 9 | D lines exploded into deal_items (side 1 = first player gives, 2 = second gives); item names from CvEnums.h (TradeableItems). Direction: who gives; partners: distinct AI players on the other side [game5] |
| `d.game1_one_sided` | table, 2 values | category | deals between the human and AI players | the whole log | 2 | D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game1] |
| `d.game2_one_sided` | table, 2 values | category | deals between the human and AI players | the whole log | 2 | D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game2] |
| `d.game3_one_sided` | table, 2 values | category | deals between the human and AI players | the whole log | 2 | D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game3] |
| `d.game4_one_sided` | table, 2 values | category | deals between the human and AI players | the whole log | 2 | D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game4] |
| `d.game5_one_sided` | table, 2 values | category | deals between the human and AI players | the whole log | 2 | D lines: deals in which one side gives nothing (gift, tribute or demand) and the others, by direction; deals whose given side holds a technology (item 9 of TradeableItems); partners: distinct AI players [game5] |
| `d.game1_diplo_events` | table, 7 values | category | diplomacy between the human and AI players | the whole log | 7 | E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game1] |
| `d.game2_diplo_events` | table, 6 values | category | diplomacy between the human and AI players | the whole log | 6 | E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game2] |
| `d.game3_diplo_events` | table, 7 values | category | diplomacy between the human and AI players | the whole log | 7 | E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game3] |
| `d.game4_diplo_events` | table, 7 values | category | diplomacy between the human and AI players | the whole log | 7 | E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game4] |
| `d.game5_diplo_events` | table, 8 values | category | diplomacy between the human and AI players | the whole log | 8 | E lines (CvPlayer::handleDiploEvent) with the human as sender or receiver, by event (DiploEventTypes from CvEnums.h); senders: distinct players sending it [game5] |
| `d.game3_memories` | table, 9 values | category | the AI players' memories of the human | at the save the log ends with | 9 | save dump, memory table (AI_getMemoryCount of each AI towards the human): memory type, AI players holding it, summed count [game3] |
| `d.game4_memories` | table, 9 values | category | the AI players' memories of the human | at the save the log ends with | 9 | save dump, memory table (AI_getMemoryCount of each AI towards the human): memory type, AI players holding it, summed count [game4] |
| `d.game5_memories` | table, 7 values | category | the AI players' memories of the human | at the save the log ends with | 7 | save dump, memory table (AI_getMemoryCount of each AI towards the human): memory type, AI players holding it, summed count [game5] |
| `b.game3_gates_to_human` | table, 17 values | category | each AI team towards the human's team | at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent) | 17 | HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game3] |
| `b.game4_gates_to_human` | table, 17 values | category | each AI team towards the human's team | at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent) | 17 | HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game4] |
| `b.game5_gates_to_human` | table, 13 values | category | each AI team towards the human's team | at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent) | 13 | HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game5] |
| `b.game6_gates_to_human` | table, 14 values | category | each AI team towards the human's team | at the save (game 3, game 4 and game 5: the last save; game 6: the save the human sent) | 14 | HARNESS_WAR_DIAG (toolchain/harness, the gates of CvTeamAI::AI_doWar) in the state dump of the save, harness DLL of the S2 source with the diagnostic, S2 on, no turn played; loaded by study/balance_load.sql with STATE set to the dump: considers a new war (no war plan, or enemy power percent below 45); attitude (0 furious to 4 friendly); per-mille chance that the dogpile path's no-war roll passes; can declare war; whether any power test (total near or far, limited, dogpile) passes; the AI's power as the tests count it towards the human (after its enemies' share; negative when its enemies outweigh it); the human's defence as the limited and dogpile tests count it [game6] |
| `b.game3_gates_summary` | table, 2 values | category | every AI team towards the human, and towards every AI team it has met (vassals excluded) | at the save, as gates_to_human | 2 | HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game3] |
| `b.game4_gates_summary` | table, 2 values | category | every AI team towards the human, and towards every AI team it has met (vassals excluded) | at the save, as gates_to_human | 2 | HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game4] |
| `b.game5_gates_summary` | table, 2 values | category | every AI team towards the human, and towards every AI team it has met (vassals excluded) | at the save, as gates_to_human | 2 | HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game5] |
| `b.game6_gates_summary` | table, 2 values | category | every AI team towards the human, and towards every AI team it has met (vassals excluded) | at the save, as gates_to_human | 2 | HARNESS_WAR_DIAG as gates_to_human: pairs (AI team, target), pairs where any power test passes, pairs where the dogpile no-war roll can pass; willing power: the summed power towards the target of the teams whose dogpile roll can pass, that can declare war and whose power is positive (summed over all targets for the AI side); the dogpile test's bar: one and a half times the target's defence (the largest target's, for the AI side) [game6] |
