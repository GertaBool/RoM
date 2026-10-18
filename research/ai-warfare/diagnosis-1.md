# Diagnosis 1: why the AI lost game 1

Evidence:
- [games/game1/analysis.md](games/game1/analysis.md);
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

**Tested and dropped.** I built the term behind a switch (`AI_TECH_STRENGTH_GAIN_VALUE`)
and played 450-turn headless Marathon games of 10–12 AIs: Mediterranean seeds 1–3, and
Earth seed 1. The table gives the median turn the AIs got each tech, and the average number
of techs at turn 450.

| Weight | Metal Casting | Bronze Working | Masonry | Techs (Mediterranean / Earth) |
|---|---|---|---|---|
| 0 (off) | 226–255 | 303–329 | 211–282 | 38.8–42.4 / 31.8 |
| 10,000 | 207–235 | 298–312 | 257–294 | 40.0–43.0 / 29.8 |
| 30,000 | 183–226 | 278–306 | 239–344 | 37.4–44.3 / 27.3 |

- The gain is 10–25 turns, far from the human's turn 170.
- The stronger weight pushes Masonry (walls) 40–90 turns later on the Mediterranean map.
- The AIs are slow at all research, not only at ordering it: 12–18 techs by turn 217 in
  game 1, against the human's 21.
- Reordering techs cannot close a 130-turn gap, so this lever is dropped. The prototype
  is kept on a local branch only (`tech-gain`) and is not shipped.
- What follows: the AI has to survive the window with the units it has. That means
  enough defenders where a threat stands (gaps 2 and 3).

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

There was one AI attack in 32 battles. Javelineers attacking promoted, healthy Warbands
would have had low win chances, so not attacking is mostly correct. Its one attack was
on a Warband with 20 % health left, at a 77 % win chance. This gap mostly follows from gap 1, so it is not worked
on now.

## Gap 5: stack attacks at hopeless odds (rank 2, from game 2)

See [games/game2/analysis.md](games/game2/analysis.md).
- **Facts:** in 4 headless games, about 200 of 2,659 AI attacks were made by non-siege
  units at win chances under 5 %. In game 2 Rome lost 5 of 8 Javelineers on one city in
  one turn, at 0.1–39 % per fight, and took nothing.
- **Cause:** `AI_compareStacks` adds up the modified strengths of the whole stack and of
  all defenders. Modifiers are counted, but the sum is linear and combat is not.
- **Correct decision:** decide from the engine's per-fight win chances, played out through
  the attack sequence. Attack when the expected result kills every defender and leaves an
  attacker to take the city. Siege units keep attacking for splash damage as now.

## Underlying: the AI's research is half the expert's

**Facts from the user's games.**
- The human had about twice the AIs' techs: 21 against 12–18 at turn 217 in game 1, and 36
  against 9–19 at turn 235 in game 2.
- In game 2 the gap opened late. At turn 100 the human had 10 techs to the AIs' 7.9 on
  average, and at turn 169 it was 17 to 10.6. Between turns 169 and 235 the human gained
  19 techs, the AIs about 5. That stretch held two golden ages (one started by a Great
  Engineer on turn 201) and a civics switch on turn 205.
- **Not from tech trading:** 2 tech deals in each game, both gifts from the human.
- **Not from expansion:** the AIs' first Settler came around turn 100 (median), before the
  human's in game 2 (turn 119).

**Facts from one 450-turn headless game of 10 AIs** (Mediterranean, seed 1):
- **Golden ages:** one AI had one, from turn 399.
- **Great people:** 81, none before turn 219. They were 34 Generals, 28 Prophets,
  9 Merchants, 5 Warlords, 3 Artists, 2 Scientists, and no Engineers. 48 joined cities and
  1 started a golden age.
- **Wonders:** 10 in all, the first on turn 254, the Colossus on turn 399. The first
  buildings giving great-person points came on turn 230.
- **Research slider:** 100 % to turn 150, then an average of 66–75 % from turn 200 on.

**Code.**
- A great person starts a golden age when its value beats 60 % of a free tech.
- That value counts only the yield bonus (yield × population × length). It gives no credit
  for the free civics switch: anarchy is 0 during a golden age (`getCivicAnarchyLength`).

**What this suggests (to be measured against the human).**
- The AI gets great people late and spends them on joining cities, so it never builds the
  bursts the human used.
- Wonders and great-person buildings come late because the techs they need come late.
  This compounds the slow start.

**Missing:** the human's own economy, by turn. The `M` and `V` lines (GitLab !48, !49)
record it, so the next human game gives both sides on the same map.

## Order of work

1. ~~Gap 1~~: tested, dropped (above).
2. Gap 5 (hopeless stack attacks): design note, then build behind a switch.
3. Gap 3 diagnosis from the next human game's `Y` lines: what threatened cities build,
   and with how many hammers.
4. Gap 2 design, together with gap 3: defenders sized to the threat that stands next to a
   city, including armies of civs at peace.
