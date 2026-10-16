# Game 1: England against 17 AIs

Source: `WarLog.log` from the user's game (the save is not published). Map 84×46,
Marathon, Noble, 18 players. The log covers turns 0–217 (6000 BC to 1145 BC). The human
is player 0, England.

## What the log shows

**The campaign.**
- The human declared war on three neighbours and took 10 cities in 31 turns:
  - the Netherlands (player 7) on turn 186: cities taken on turns 187, 187, 189, 190
    and 213;
  - the Celts (player 1) on turn 193: cities taken on turns 194, 194 and 195;
  - Portugal (player 14) on turn 206: cities taken on turns 207 and 217.
- Every attack was made with Celtic Warbands. A Warband has strength 6, 2 moves, costs
  40 hammers, needs Bronze Working and the Celtic religion tech, and needs no resource.
  - The human got Bronze Working on turn 170. The first Warbands were finished on
    turn 176, and 8 of them were ready before the first declaration.
  - The Warbands entered battle with 6–14 experience and were promoted 56 times.
  - From turn 207 they were upgraded to Celtic Swordsmen (strength 7).
- The armies were in place before each declaration, so the first battle came the turn
  of the declaration or the next one. The human had open borders with the Netherlands
  from turn 123 and with the Celts from turn 140.
- Each army was a few Warbands, moved one tile per order. The largest group near an
  enemy city had 4 Warbands.

**The battles.** There were 32 battles in the human's wars.
- The human attacked at win chances of 64–100 %. They won 23 battles and lost 9.
- The defenders were Javelineers (strength 3) and some Spearmen (strength 4).
- City defence was 0–40 %, with 1–2 units per city. The one exception was the city at
  29,33, which had 11 units and fell in two waves, on turns 209 and 213.
- The AI attacked once in all three wars: on turn 209 it killed a Warband that had 20 %
  health left.

**The AI's technology.**
- By turn 217 no AI had Bronze Working or Archery. Archery costs 60 beakers and needs
  only Hunting, which every AI had from turn 0.
- The AIs had 12–18 techs; the human had 21.
- The three targets researched their way to Mining, Sailing, Pottery and Trade. Two of
  them got Masonry: the Celts on turn 139 and Portugal on turn 175. The Netherlands got
  Metal Casting on turn 189, after its war had begun.

**What the AI built.**
- Over 217 turns, all 17 AIs together built:
  - 129 Javelineers, 37 Spearmen, 12 Rams and 6 Velites;
  - 85 Settlers, 74 Workboats, 67 Workers and 42 Galleys.
- After war was declared on them:
  - the Netherlands built 3 Spearmen in 31 turns;
  - the Celts built no units in 24 turns;
  - Portugal built 1 Javelineer in 11 turns.

**Diplomacy.**
- The human signed open borders with 12 AIs.
- The human refused AI requests:
  - to stop trading with someone, 5 times;
  - to change civics, once;
  - to join a war, once;
  - for help, twice.
- No AI declared war on the human.

**Other AI war.** AI 16 fought AI 2 from turn 152 to 172, with three battles in all. One
of them was an attack on a city at a 1 % chance of winning.

## What this suggests (inferences, to be tested against the code)

1. **The AI leaves a long window of weakness.** The human's units were twice as strong as
   the defenders for 16+ turns, because the AI does not research military techs, even
   cheap ones. Test: read how the AI values techs when it has no war plan, and with a
   stronger neighbour.
2. **The AI does not see a threat coming.** Foreign armies stood next to its cities under
   open borders, and nothing changed. Test: read how the AI counts danger from units of
   a civ it is at peace with, and when it cancels open borders.
3. **The AI does not mobilise when attacked.** Its cities kept building non-military
   things, or nothing military, for 11–31 turns. Test: read the city build choice when
   the city is under attack. The log has no city build list, so I can't yet tell
   "chose not to" from "could not".
4. **The AI does not counter-attack** damaged units next to its cities. There was one
   counter-attack in 32 battles. Test: read the defensive attack code, and the odds
   limits it uses.
5. **Attacks at hopeless odds** (1 %) still happen between AIs.

## Limits of this evidence

- One game, one player, at Noble. At Noble the AI gets no bonuses, so part of the tech
  gap may disappear at higher difficulties.
- The log records units built, not buildings, so city production choices are partly
  unseen.
- Garrison sizes are known only for plots where a battle took place.
- Worker builds are logged as numbers. I turned them into names by their order in the
  XML. Read that way, the most common were road 35, mine 24 and farm 10.
