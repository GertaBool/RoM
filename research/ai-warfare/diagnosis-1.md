# Diagnosis 1: why the AI lost game 1

Evidence:
- [games/game1-england.md](games/game1-england.md);
- one 450-turn and one 200-turn headless game of 10 AIs (Mediterranean, Marathon,
  Noble), the second with the AI's tech scores logged;
- a test copy of the DLL that logs each part of every tech score.

The code read is GitLab `main` after !47.

## Gap 1: tech choice ignores how much stronger new units would be (rank 1)

**Facts.**
- In the 450-turn AI game, the AIs got Bronze Working on turns 250–365 and Masonry on
  turns 237–334; the first Archery came on turn 248. The human in game 1 had Bronze
  Working on turn 170.
- In the AI's own scores, Mining, Mysticism and Naturopathy beat Bronze Working by 8 to
  10 times. For one AI's first choice (raw value before dividing by research time):

  | Tech | Final score | Raw value | Of which: resources revealed | Units |
  |---|---|---|---|---|
  | Mysticism (chosen) | 250,767 | 15,347 | about 10,300 | none |
  | Mining (chosen 3 picks later) | 327,224 | 16,623 | about 15,200 | none |
  | Bronze Working | 24,431 | 3,782 | none | about 2,900 |
  | Archery | 20,110 | 1,459 | none | about 840 |

  The "units" figure in the log includes the resource reveals. Mysticism, Naturopathy
  and Mining unlock no units, so their figure is all reveal value.
- **Code** (`CvPlayerAI::AI_techValue`): each resource a tech reveals adds 150 + 50 × the
  resource's value, often over 5,000 each.
- **Code** (`AI_techUnitValue`): a unit unlock adds a flat amount per role, for example
  300 for a counter unit and 400 + 400 for a city defender when not planning war. The
  amount does not depend on:
  - the unit's strength compared with the best unit the AI can build now;
  - how strong its neighbours are.
- The Celtic Warband (strength 6, no resource needed) needs Bronze Working and the Celtic
  religion tech, for any civilization. The Celts in game 1 had the religion tech from
  turn 108 and never took Bronze Working.

**Rule.** A tech that doubles the strength of your best unit, while a neighbour is
stronger than you, is worth more than a resource you cannot yet use.

**Correct decision.** Add a term to the unit value: the gain in strength over the AI's
best current land unit, scaled by threat (neighbours' power against its own, and
attitude) and by the leader's military flavour.

## Gap 2: no danger from armies of civs at peace (rank 2)

**Facts.**
- **Code** (`CvPlayerAI::AI_getPlotDanger`): only units of a civ at war count, so an army
  standing next to a city under open borders counts as zero.
- **Code** (`CvTeamAI::AI_openBordersTrade`): open borders are judged on attitude alone.
  Deals are cancelled only when attitude drops.
- In game 1 the human's armies stood next to the AI cities before each declaration, and
  the first battle came the same turn or the next.

**Correct decision.**
- Count foreign land units that can attack within reach of a city as potential danger
  when their owner is stronger than the AI and not friendly.
- Cancel or refuse open borders with such a civ while its army is inside the AI's land.

## Gap 3: no mobilisation after war is declared on the AI (rank 3, cause unknown)

**Facts.**
- After war was declared on them, the targets built 3, 0 and 1 units in 31, 24 and
  11 turns.
- The minimum garrison (`AI_minDefenders`) is 1 for the whole Ancient era, plus 1 for the
  capital. Garrisons in game 1 were 1–2 units.

**Missing.** What the cities were building and how many hammers they had. The new `Y`
log lines (in !47) record this. The next human game decides whether the cause is
production choice or lack of production.

## Gap 4: few counter-attacks (rank 4)

There was one AI attack in 32 battles. With strength-3 units against strength-6 Warbands,
not attacking is mostly correct. This gap mostly follows from gap 1, so it is not worked
on now.

## Order of work

1. Gap 1, behind a switch (off by default), measured in headless games: when the AIs get
   Bronze Working and Masonry, and what it costs their economy (techs, cities, score).
2. Gap 3 diagnosis from the next human game's `Y` lines.
3. Gap 2 design.
