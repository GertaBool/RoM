# How the human decides: macro and micro rules across games 1–4

Sources: the generated tables of `games/game1`–`game4` and the figures in
[figures.md](figures.md) (`tools/decisions.py`; sections A–N are cited by letter). XML stats
are the records of the source tree the games ran on.

**What the data can and cannot show.** The logs record what the human did (commands, builds,
wars, deals, battles), never what was weighed. Every rule below is a model of the outcomes:
the simplest rule that reproduces the choices, with a rival rule and the cases that go
against it. The sample is one player and four games. Games 1–2 have no economy, city-state or
deal lines; games 3–4 have them. Game 2's attack odds are suspect: on turn 109 three
Javelineer attacks at 3.7–9.9 % were all logged as won, about a 1-in-10⁴ outcome.

## 1. Description

| Area | Figure | Game 1 | Game 2 | Game 3 | Game 4 |
|---|---|---|---|---|---|
| A | Human attacks: 10th percentile / median odds | 68 / 82 | (suspect) | 71 / 81 | 72 / 98 |
| A | Human attacks under 50 % | 0 % | (suspect) | 0 % | 4 % (1 of 80) |
| A | AI-on-AI attacks under 50 % (non-siege) | n/a | 62 % | 31 % | 22 % |
| C | Target power ÷ human power the turn before a declaration | – | – | 0.50, 0.32 | 0.13–0.81, median 0.37 |
| C | AI-on-AI declarations, same ratio, median | – | – | 0.66 | 0.92 |
| C | Turns from the last capture to peace (ended wars) | – | – | 0, 1 | 1, 2, 4, 2, 0 |
| D | Target is the nearest AI neighbour | – | – | 2 of 2 | 5 of 8 |
| D | Target is the weakest neighbour by power | – | – | 0 of 2 | 0 of 8 |
| E | Human's most-built recent unit ÷ target's best defender, strength | – | – | 6/3, 6/3 | 7/4, 7/7, 7/4, 8/5, 8/4, 8/5, 10/7, 10/7 |
| F | Upgrades within 5 turns of a declaration / share of turns in those windows | 11 of 16 / 13 % | 6 of 11 / 10 % | 6 of 8 / 6 % | 67 of 74 / 18 % |
| F | Gold the turn before a declaration against the 30-turn median | – | – | 63 vs 48, 61 vs 44 | above the median in 6 of 8 (1,457 vs 216 at turn 268) |
| G | Civics adopted within 1 turn of their tech | 8 of 9 | 12 of 14 | 13 of 15 | 9 of 13 |
| G | The same for AIs (game 4 replay messages) | | | | 119 of 214; median lag 1 for both |
| H | Research choices no AI knew yet | 9 of 18 | 24 of 33 | 15 of 25 | 18 of 33 |
| I/M | Median steps from a new city to the nearest earlier own city, human / AI | – | – | 4 / 4 | 3 / 3 |
| J | First order in a new city | Walls 8 of 15 | Obelisk 13 of 15 | Obelisk 7 of 12 | Obelisk 14 of 25 |
| K | Promotions | (indices only) | (indices only) | Guerilla 39, Combat 32 | Combat 129, Amphibious 45, Medic 23, Navigation 22 |
| N | AIs that knew a tech the human received in a trade (median) | – | – | 5 | 11 |
| N | Techs sold for gold | – | – | Archery ×3 (380–490), The Wheel (220) | Archery ×2 (520, 380), Fermentation (660), Seafaring (80) |

Further facts used below (game 4 unless marked):
- The first war in each game comes late: turn 186 (game 1), 92 then 229 (game 2), 203 (game
  3), 238 (game 4).
- Before it, game 3 (turns 165–221) and game 4 (206–250) each have a long pause without a
  new city: 56 and 44 turns.
- Amphibious promotions start on turn 236 and come mostly on turns 265–285. Carthage was
  taken from boats on turn 284.
- Fiscus (gold rushes) was adopted 24 turns after its tech, on the turn of the war against
  Masinissa and of 19 upgrades. Fortification followed 101 turns after its tech in game 3
  and 108 in game 4.
- Techs given on request (each buys a 10-turn forced peace with that AI) were mostly known
  by many AIs already: The Wheel by 10–14, Masonry by 9, Monarchy by 15.
  - Exceptions: Bronze Working given in game 3 when 0 and 6 AIs knew it; Currency traded in
    game 4 when no AI knew it; Code of Laws given in game 4 when 2 AIs knew it.

## 2. Readings: the rules that reproduce the choices

Each rule is given as cue → stop → decision, with its facts, its rival and what goes
against it.

### R1. When to go to war: a strength margin, then strike

- **Rule:** wait until the army's core unit beats the target's best defender clearly
  (strength ratio about 1.4 or more), with gold saved. Then declare and upgrade at once.
- **Facts:**
  - E: the ratio is 1.4–2.0 in 9 of 10 declarations.
  - F: upgrades cluster at declarations in all four games: 6 of 8 to 67 of 74, against
    6–18 % of turns.
  - Gold peaks before declarations in game 4. The first war comes after the economy phase in
    games 3 and 4.
- **Rival:** declare whenever an AI city appears inside one's own land (L). That predicts the
  timing of the probing wars equally well in game 4: 4 of the 6 cities taken on turns
  238–268 were nearer the human's cities than their owner's.
- **Against R1:** turn 252, Pericles. The ratio was 1.0 (Hastati 7 against Phalanx 7), and
  the war was a two-turn grab of a pop-1 city with one Spearman. The margin rule seems to
  apply to a city's defenders, not the target's whole army.

### R2. Whom to fight: the nearest, not the weakest

- **Rule:** one cue, distance. Attack the AI whose cities are nearest one's own, then finish
  a beaten neighbour.
- **Facts (D):**
  - Distance rank 1 in 7 of 10 declarations; power rank 1 (weakest) in none.
  - The weakest neighbour in game 4, Brennus (power 49–143), was never attacked.
  - Leonidas, attacked again on turn 271 at distance rank 7, was already down to 2 cities.
- **Rival:** the target with the most to take. Cities rank 1 in 1 of 10, so not supported.
- **Against R2:** turn 252 (distance rank 4), which matches the encroachment rival of R1.
- **Ecological reason (reading):** at Marathon speed with slow units, distance decides the
  cost of a campaign more than the target's total power does. Only the units near the front
  fight.

### R3. How long to fight: take what is in reach, then stop

- **Rule:** an aspiration level, not a war aim. Take the cities in reach in one push; when
  none is in reach, accept peace (the AI pays).
- **Facts:**
  - C: every ended war ends 0–4 turns after the last capture.
  - The probing wars in game 4 last 2–4 turns, and three end with the AI paying 220–430
    gold.
  - 9–14 turns of peace follow before the next declaration.
- **Rival:** the AI proposes peace and the human accepts every offer. This cannot be told
  apart: who proposed is not logged.
- **Against R3:** the wars of games 1–2 and the later wars of game 4 are open at the log's
  end, so their end is unseen.

### R4. Which fights to take: high odds only

- **Rule:** an odds floor of about 65–70 % per attack, except to finish a damaged defender.
- **Facts (A):**
  - 10th percentile of the human's attacks: 68–72 in games 1, 3 and 4.
  - Under 50 %: 0–4 %, against 22–62 % for AI-on-AI attacks.
  - B: in an assault the last attacks run at a median 85–100 %.
- **Rival:** no explicit floor. High odds follow from R1's strength margin.
- **Undecided:** the data hold only the attacks made, not the attacks declined, so a floor
  and a margin-chosen war look the same.

### R5. Money: save, then convert at the moment of use

- **Rule:** keep gold idle until a war starts, then spend it on upgrades and rush buying.
  Raise it by selling techs that do not threaten one's own army, and from peace payments.
- **Facts:**
  - F: in all four games.
  - N: game 4 sold Archery twice for 520 and 380, plus Fermentation (660) and Seafaring (80),
    on turns 264–275, during its war phase. Game 3 sold Archery three times for 380–490 on
    turns 261–265, at the end of its log, with no later declaration to compare.
  - Fiscus was held back until the war (24-turn lag) and adopted with the upgrade turn.
  - Peace payments in game 4: 905 gold.
- **Rival:** upgrades come at war start because the new units' techs arrive just before.
  - Game 4: Iron Working (254) came 8 turns before the first large burst (262), and Siege
    Warfare (264) 4 turns before the largest (268). The timing fits both rules.
  - The rival does not explain the gold held above its median before 6 of 8 declarations.

### R6. Techs: research the frontier, trade for the commons, give the cheap

- **Rule:** research what nobody has. Obtain by trade what many AIs already know. When asked,
  give what many already know (it buys a 10-turn peace); sell for gold what the AI values
  but that does not hurt one's own army.
- **Facts:**
  - H: 50–73 % of research choices were techs no AI knew (games 2–4; 9 of 18 in game 1).
  - N: techs received were known by a median of 5 (game 3) and 11 (game 4) AIs. Gifts were
    mostly The Wheel and Masonry, known by 9–14 AIs.
  - Archery sold to the AI it attacked 13 turns later (Pericles, game 4).
- **Against R6:**
  - Bronze Working given in game 3 when no AI knew it (for Writing, turn 197) and twice more
    later.
  - Currency traded in game 4 when no AI knew it (to Cyrus, far east).
  - So "never give a frontier tech" is false. A distance cue ("only to far-away AIs") fits
    Cyrus but not Bronze Working to Pericles (game 3, turn 221). *Open.*

### R7. Micro, prepared in advance for the planned operation

- **Rule:** promote for the next operation, not the current fight.
- **Facts:**
  - K: Amphibious (no penalty attacking from ships; requires Combat II) taken 45 times from
    turn 265, ahead of the landing at Carthage on turn 284.
  - Navigation and Medic on the fleet and army that carried it out.
  - Guerilla and Woodsman on the early Javelineer garrisons (game 3: 39 and 6).
  - Experience stacked before the conquest (Legion Barracks, Oligarchy, Mars Temples;
    game 4 analysis R5).
- **Rival:** Amphibious taken for river crossings (it also removes the river penalty). Not
  excluded. Its timing with the Quinquereme builds (11 on turns 260–284) favours the
  landing reading.

### R8. Expansion and first builds: ordinary, not distinctive

- **Facts:**
  - I/M: the human's city spacing equals the AI's (median 3–4 steps).
  - J: Obelisk is the first build in 13 of 15, 7 of 12 and 14 of 25 cities (games 2–4), Walls
    in 8 of 15 in game 1.
  - G: civics follow their tech within one turn as often as the AI's do.
- **Reading:** these decisions follow simple defaults. Obelisk is the cheapest culture
  building (30 hammers, +1 culture), and "cheapest culture first" or "cheapest first"
  predict the same. The data do not show an edge over the AI here.
- **Exceptions:** the situational civics (Fiscus, Fortification, Metals), held until their
  situation.

### R9. The interlinking: one plan orders the simple rules

The rules feed each other in a fixed order, the same in games 3 and 4:
1. Expand to a compact ring, with ordinary defaults (R8).
2. Stop expanding and build multipliers (game 4 analysis, R3). Commerce gives the research
   frontier (R6).
3. The frontier gives both a unit margin (R1) and techs to sell (R5).
4. Sales and saved gold pay for upgrades at the declaration (R5).
5. The margin gives high-odds attacks (R4) against the nearest cities (R2), in short wars
   that end with peace money (R3).
6. That money pays for the next round, with operations prepared in promotions and boats
   (R7).

Each rule uses one or two cues and ignores the rest (distance, a strength ratio, gold on
hand, how many AIs know a tech). None needs a weighted sum.
- **Reading:** this is where the human differs from the AI. Not in any single decision (R8
  shows defaults like the AI's), but in sequencing decisions so that each sets up the next.
- **What would contradict it:** a game in which the human wars early, without a tech or unit
  margin, and wins as easily. Game 2's war on turn 92 is the closest case: one city taken,
  after 18 turns.

## 3. Against the AI, decision by decision

| Decision | The human (rule) | The AI (data; code) | Status |
|---|---|---|---|
| War timing | Strength margin and saved gold (R1, R5) | AI-on-AI targets have a median 0.66–0.92 of the declarer's power (C); war is chosen by war plans and attitude in `CvTeamAI::AI_doWar` | data: measured; code: *open* |
| Target | Nearest (R2) | — | *open* |
| Attack choice | High odds only (R4) | 22–62 % of AI-on-AI attacks under 50 %; the floor in the user's settings is 5 % (`AI_ATTACK_ODDS_FLOOR`) | measured |
| Defence | — | No danger counted from units at sea (`AI_getPlotDanger`, `AI_getEnemyPlotStrength`: same land area only) | **traced** (game 4, 5A) |
| Money | Save, spend at the declaration (R5) | Upgrade timing not logged for the AI; it paid 380–660 gold for techs from the player who then attacked it | data: measured; code: *open* |
| Techs | Frontier research, trade the commons (R6) | Bought Archery and Fermentation from the human; sold common techs | *open* (`AI_techTradeVal`) |
| Civics, city spacing, first builds | Defaults (R8) | The same lag and spacing (G, M) | measured: no gap |
| Plan | One sequence (R9) | Each decision scored on its own (`AI_chooseProduction` priorities, additive valuations) | reading |

The measured gaps are in the war decisions, not the economic defaults. These are the
targets for AI work, in order of evidence:
1. Danger from the sea (traced).
2. Declaring against near-equals (measured).
3. Low-odds attacks (measured).
4. Selling techs and paying for peace to the attacker (measured; code open).
