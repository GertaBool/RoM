# The human's micro-decisions: games 4 and 3

Figures: [micro-game4.md](micro-game4.md) and [micro-game3.md](micro-game3.md)
(`tools/micro.py`, sections 1–13), from each game's tables, the scenario file and the save
dump. The macro rules are in [human-decisions.md](human-decisions.md) (R1–R9).

Caveats:
- The `A` lines are the commands the human gave, not the options considered. A rule below
  is the simplest one that reproduces those commands, with its rival and its exceptions.
- Game 4 has 2,771 commands, game 3 1,301. Game 3 is the check on game 4.

## 1. Attention: little in peace, everything at war

| Turns (game 4) | Commands per turn | Turns at war |
|---|---|---|
| 0–99 | 0.3–2.3 | 0 |
| 100–224 | 3.2–5.1 | 0 |
| 225–249 | 11.4 | 3 |
| 250–274 | 30.5 | 15 |
| 275–285 | 53.0 | 11 |

- The eight busiest turns are all war turns (62–92 commands each). Game 3 is the same: its
  five busiest turns are its war turns 203–214.
- **Delegated:** Workboats (8), Galleys (7), the Scout and the Explorer are automated.
  Workers are never automated (189 hand-given moves, 276 builds).
- **Reading:** attention is spent where a decision changes the outcome (battles, worker
  placement) and withheld where the AI's routine is good enough (exploring, fishing boats).
  Simon's point that attention is the scarce resource, and a satisficing division of labour
  with the automation.

## 2. City production

| Figure | Game 4 | Game 3 |
|---|---|---|
| Orders queued (Shift) | 6 of 383 | 0 of 199 |
| The capital's orders that are units | 69 % | 71 % |
| Median military share of a city's hammers, human | 8 % | 0 % |
| The same for the AI | 42 % | 37 % |
| Human cities spending ≤ 15 % on military | 67 % | 92 % |
| AI cities spending ≤ 15 % on military | 3 % | 10 % |
| First order in a captured city | Obelisk 12 of 13 | Obelisk 6 of 6 |

- **One order at a time.** The human re-decides at each completion and does not plan the
  queue.
- **One factory.** The capital trains the army; Tribute gives it +25 % on all yields. The
  other cities build economy. In game 4 the next three cities made 42–47 % of their orders
  units.
- **A default for new and captured cities:** Obelisk (30 hammers, +1 culture). It is also
  the cheapest building; the data cannot separate the two cues.
- **Against the AI:** every AI city spends a large share on military (median 37–42 %). So
  its army is spread over every city, and its economy loses that share everywhere.

## 3. Workers

- **Order of builds (game 4):** camps and tracks first (16 of the first 20 builds), then
  mines. Then roads and paved roads replace tracks: tracks 69, roads 48, paved 14.
- **What goes where** (starting terrain, before chopping):
  - mines on hills (42 of 42);
  - farms on grassland and marsh;
  - camps, wineries, quarries and pastures on their resources;
  - cottages mostly on chopped forest hills (16 of 35).
- **Worked land tiles at the save (game 4):**

  | Group | Improved | Mines | Yield per tile |
  |---|---|---|---|
  | Human-founded cities | 84 % | 31 % | 9.32 |
  | Captured cities | 43 % | 17 % | 6.93 |
  | AI cities | 75 % | 25 % | 7.89 |

  Game 3: human-founded 88 % improved and 7.92 per tile, against the AI's 74 % and 7.65.
- **Roads toward the next target.** Route builds within 4 steps of the target's cities, in
  the 30 turns before the declaration against the 30 turns before that:

  | Declared | Before the war | Earlier |
  |---|---|---|
  | 238 | 11 of 28 | 2 of 5 |
  | 252 | 8 of 36 | 1 of 18 |
  | 268 | 19 of 36 | 1 of 28 |

  Not before turns 257, 271, 272, 277 or 283. Those wars started from roads already built
  or by sea.
- **Reading:** the worker plan follows the terrain, and the hills-and-forest start is
  turned into hammers (mines) before commerce. Logistics are prepared for the first push
  into each new region.

## 4. The research slider: one cue

Every slider move follows the sign of gold per turn the turn before:
- a cut when gold per turn ≤ 0;
- a raise when it is > 0.

| Game | Moves predicted | The exception |
|---|---|---|
| 4 | 24 of 25 | turn 182, at 0 |
| 3 | 13 of 14 | turn 165, a cut at +2 |

- Until about turn 228 the treasury is held near zero (0–40 gold), at the highest research
  rate that does not lose gold. After turn 247 the slider is not touched again, at 85 %, and
  gold accumulates from deals and conquest (R5).
- **Reading:** a one-reason rule for the peace economy. Its cue is the only one that
  matters while gold has no other use, and it is dropped when gold acquires a use
  (upgrades).

## 5. Combat

- **Concentration.** Cities are taken in one turn with 3–11 attacks on one plot; Pericles'
  capital took 11 attacks on turn 279.
- **The best unit leads.** The first attacker is the most experienced in 7 of 10 assaults.
  A random order would give that about 2 times in 10.
- **Wounded units finish.** 61 of 80 attacks are at full health. Of the 19 wounded attacks,
  15 come after another attack on the same plot that turn, and 17 are at 90 % or better
  (median 98 %). The four that open an assault are only lightly wounded (91–99 health).
  AI-on-AI attacks are at full health in 145 of 153.
- **Experience:** the attacker's median 14 against the defender's 2; the attacker has more
  in 71 of 80 attacks. Game 3: 6 against 5, so there the margin was strength, not
  experience.
- **Preparation by sea.** Five captures had Quinquereme bombardments or ranged attacks on
  the city in the 10 turns before: 38,23, 43,25, 37,26 (5 plus a Catapult), 46,25 and 47,23.
  Carthage was taken from the boats.
- **The odds floor gives way at a capital.** On turn 279 the first four attacks on Pericles'
  capital were at 36–72 %. All 11 attacks won, and the city fell on turn 280. Elsewhere the
  lowest opening odds are 57 %.
- **Movement:**
  - At war, 73 % of moves are single units and 7 % groups of four or more (largest 9).
  - In peace, 97 % are single units.
  - Units are placed one by one, then attack together. 49 sea patrols screen the fleet's
    lanes.
- **Reading:** Clausewitz's concentration at the decisive point, and economy of force
  elsewhere. Moves are cheap and singly controlled; the force is massed only for the blow.

## 6. Promotions: by role, and for the coming operation

| Unit | Promotions (game 4) |
|---|---|
| Legionary (assault) | Combat II 42, Amphibious 39 (needs Combat II), Combat I 26, Medic I 14, Combat III 8 |
| Hastati, Principes | Combat and Shock |
| Javelineer (early garrison) | Guerilla II 16, Woodsman I 4 (hills and forest, the home terrain) |
| Velites (garrison) | City Garrison |
| Quinquereme | Navigation I and II, 22 |
| Centurio (leader) | Heroic, Morale, Tactics |

Game 3: Guerilla 39, Combat 32.

- **Reading:** a short decision tree, role then promotion. Amphibious is chosen from turn
  265 on, before the landings, which shows the plan reaching down to single promotions.

## 7. Garrisons at the save

| Game | Human cities | AI cities |
|---|---|---|
| 4 | 2.1–2.2 land units each | 3.3–3.5 |
| 3 | 2.4–2.7 | 1.7–2.4 |

- No common rule: game 4's human garrisons are thinner than the AI's, game 3's thicker.
- In game 4 the human's units at the save are mostly field roles: counter 27, attack city
  23, attack 13, sea 17. Only 3 have the city-defence role.

## 8. Great people

- **Game 4:**
  - Engineer → golden age (229, the turn two civics changed without anarchy).
  - Prophet → a shrine construction (251).
  - Great Spy → a construction (270).
  - Great Generals joined units (257, 271); Warlords led stacks.
- **Game 3:** caravans used for trade missions (171–195), a General's construction (206), a
  Prophet's construction (260).
- **Reading:** great people are spent on the current phase: the economic boom (golden age),
  then the army (generals into units).

## 9. Requests from the AIs: what they asked, and whether they made sense

What the AI asks for, from `CvPlayerAI::AI_doDiplo` (`CvPlayerAI.cpp`, about lines
17610–17830):

| Request | What the AI picks | What it does not weigh |
|---|---|---|
| Join war | A random one of its war enemies that the human has met and can declare on (`getSorenRandNum(10000)` per candidate) | Distance, power, the human's trade with the target, any payment |
| Stop trading | Its worst enemy (`AI_getWorstEnemy`) | The value of that trade to the human |
| Ask for help | A random tech the human can give (uniform draw) | The tech's value to either side; fires when the human's assets exceed half the AI's |

None of the three models the human's interests. The requests in the logs show it:
- **Both sides of one war asked the human to join:**
  - game 4: Pericles on turn 178 and Leonidas on 179;
  - game 3: Brennus on 163 and Willem on 190.
- **The target was the human's trade partner:** 6 of 9 join-war requests in game 4
  (deal items with the target in the 40 turns before) and 3 of 6 in game 3.
- **The target was out of reach:** 9–14 steps in game 4 (turns 192 and 248); 10 steps in
  game 3 (turns 163, 204, 223).
- **The requester asked the player who then attacked it:**
  - game 4: Pericles asked on 178 and 222 and was attacked on 252; Masinissa asked on 248
    and was attacked on 268;
  - game 3: Willem asked on 190 and was attacked on 209.
- **No request offered anything in return.**

The human's answers:

| Request | Game 4 | Game 3 |
|---|---|---|
| Join war | refused 9 of 9 | refused 6 of 6 |
| Stop trading | refused 9 of 9 | refused 11 of 11 |
| Ask for help | given 10 of 22 | given 5 of 16 |

- **Join war and stop trading** are categorical refusals. They follow from R1: the human
  goes to war on its own timing, when its margin and gold are ready.
  - The same refusal stands even when the target was the human's own next victim (Leonidas,
    Masinissa, Willem).
  - A reflex "always say no" is excluded by the help requests, which got 15 yeses.
- **Ask for help** is accepted when the draw was likely cheap. The asked tech is a random
  draw, so the share of widely known techs (known by 5+ AIs) in the AI's pool is the chance
  the request was cheap:

  | Game | Pool share when given | Pool share when refused |
  |---|---|---|
  | 3 | about 0.5 | about 0.35 |
  | 4 | about 0.55 | about 0.3 |

  The techs given were mostly The Wheel and Masonry.
  - **Second cue: during the human's own wars, give.** In game 4 after turn 238, all 5 gifts
    were made during the human's wars, against 4 of 8 refusals. The three gifts on turn 279
    went to Alexander, Willem and Afonso while the human fought four AIs. Each gift buys a
    10-turn forced peace (`DIPLOEVENT_GIVE_HELP` → `forcePeace`), so they buy quiet flanks
    for the campaign.
- **Were the requests objectively bad?**
  - For the human: joining was costly in every case. It meant a war without a prize in
    reach, or against a trade partner, or on someone else's timing, and nothing was
    offered.
  - For the AI: asking is cheap, but the requests reveal no model of the human. The AI
    courts its future attacker and asks a strong neighbour to fight a third party at random.
  - The help draw is blind to value, so a request can ask for the human's most valuable
    tech. The human then refuses, and the refusal costs the AI goodwill (`MEMORY_REFUSED_HELP`
    on the AI's side).

## 10. Against the AI, micro decision by micro decision

| Decision | Human | AI | Status |
|---|---|---|---|
| Where hammers go | One military city; the rest economy (median 0–8 % military) | Every city 37–42 % military | measured |
| Production queue | One order at a time | Chosen per completion by `AI_chooseProduction` | — |
| Assault | Massed in one turn, best unit first, wounded units finish | Full-health attacks (145 of 153); low-odds attacks common (22–62 % under 50 %) | measured |
| Experience | 13–19 on attackers (stacked buildings, civic, religion) | Median 3–4 | measured |
| Sea threat | Bombards, then lands | Does not count units at sea | **traced** |
| Gold and slider | Gold per turn ≥ 0 at peace; hoard for war | Not logged | *open* |
| Promotions | By role and coming operation | Not logged | *open* |
| Diplomacy requests | Refuses joining and embargoes; gives cheap help, more at war | Random targets and random techs, blind to the human's interests | **traced** (`AI_doDiplo`) |

## 11. How the micro serves the macro

- The slider rule keeps the research lead (R6) without losing gold, until gold is needed
  (R5).
- The single factory city and economy-first production (section 2) give the hammers and
  research for the margin (R1).
- Roads toward the target and promotions for the landing prepare a war chosen in advance
  (R2).
- Assaults that mass the best units in one turn (section 5) keep the wars short (R3).
- Refusing requests (section 9) keeps the war calendar the human's own. Cheap gifts during
  wars stop third parties from joining against the human.

Each micro rule uses one cue, and the macro plan decides which cue matters at the time:
- the sign of gold per turn in peace, gold on hand before war;
- distance for targets;
- the role for promotions;
- for help requests, whether the ask is likely cheap and whether a war is on.

That switching of cues by phase is the expert's situational discrimination in Dreyfus's
sense. The AI's code uses the same cues and weights in every phase.
