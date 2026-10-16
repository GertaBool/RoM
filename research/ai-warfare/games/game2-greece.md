# Game 2: Greece against 17 AIs

Source: `WarLog.log` from the user's game (the save is not published).
- **Setup:** map 84×46, Marathon, Noble, 18 players. The human is player 2, Greece
  (Pericles). The log covers turns 0–235 (6000 BC to 875 BC).
- **Log version:** the game was played with the first log DLL (!46). It therefore has no
  city-state (`Y`) or building (`N`) lines, and worker builds and promotions appear as
  numbers.

Win chances below are the engine's own odds for each fight. They include promotions,
terrain, city defence, fortification and first strikes. Base strengths are XML values and
are given only to name the units.

## What the log shows

**Techs.**
- At turn 235 the human had 36 techs; the 17 AIs had 9–19.
- The human got Bronze Working on turn 194, then Military Training, Iron Working and
  Siege Warfare before the main war.

**The campaign.**
- **First war:** on turn 92 the human declared on Leonidas (player 16), a Greek civ. The
  city at 39,19 fell on turn 110 after 5 battles. The human attacked it with Javelineers
  at win chances of 4–10 % before the last two attacks (74 % and 46 %).
- **Main war:** on turn 229 the human declared on Hannibal (player 11), and on turn 230 on
  Joao (player 9). They took 9 cities in 8 turns.
  - Seven cities fell after a single battle, one after 2 and one after 3.
  - The attackers were Greek Phalanxes, a Warlord, Sarissas and Hypaspists with 9–19
    experience, plus Triremes at sea.
  - Every land attack had a win chance of 96–100 %.
- **The defenders** were one Javelineer or Spearman per city, at city defence 0–20 %. The
  largest city (44,17, population 9) had 3 defenders.
- **The AI's response.** Hannibal built no units in the 7 turns after the declaration. Joao
  built 3 Spearmen in 6 turns.

**What the human built** in 235 turns: 12 Greek Phalanxes, 9 Javelineers, 8 Triremes,
7 Workboats, 5 Settlers, 5 Peltists, 4 Galleys, 2 Spearmen, 2 Sarissas, 2 Hypaspists,
1 Worker, 1 Warlord and 1 War Galley.

## A new AI flaw: stack attacks at hopeless odds

**On turn 213** Rome (player 3) attacked the city at 39,29 (Alexander, player 17).
- **The city:** a hill city with 30 % defence and 2 defenders, one a Spearman with 11–12
  experience.
- **The attack:** a stack of 8 Javelineers attacked 8 times, at win chances of 0.1 %,
  0.7 %, 0.7 %, 2.8 %, 5.6 %, 9.5 %, 38.7 % and 38.7 %.
- **The result:** Rome lost 5 units, 3 withdrew, and the city held.
- **Earlier:** Charles V (player 12) had made similar attacks on turns 192 and 199, at
  0.1–21 %.

**In 4 headless AI games of 450 turns:**
- 293 of 2,659 AI attacks had win chances under 5 %.
- Siege units such as Catapults and Rams attack at low odds on purpose, for splash damage
  to the whole stack. Leaving them out, about 200 attacks remain, made with Spearmen,
  Velites, Javelineers, Axemen, chariots and others.

**Cause** (`CvUnitAI::AI_stackAttackCity` → `CvSelectionGroupAI::AI_compareStacks`).
- **The test:** the stack attacks when the sum of its units' strength, divided by the sum
  of the defenders' strength, reaches the attack ratio (at least 100).
- **What it counts:** the sums include the modifiers. Attackers get their attack bonuses
  (city attack, hills attack, river crossing); defenders get their defence bonuses (city
  defence, fortification, hills, promotions).
- **The flaw:** the sum is linear, but combat is not. A unit at under half the defender's
  effective strength almost always loses and does little damage, so adding more such
  units does not add up to a win. Here 8 units at a 0.4 strength ratio gave a sum ratio of
  about 160 %, while each fight had a 1–10 % chance.
- **Correct input:** the per-fight win chance the engine already computes, played out
  through the sequence of attacks. It should give the expected number of defenders killed
  and attackers left to move in.

## Consistent with game 1

- Cities held 1–2 defenders, and the first battle came the turn of the declaration or the
  next.
- The AI barely built units after war was declared on it.
- The human's tech count was about twice the AIs': 21 against 12–18 at turn 217 in game 1,
  and 36 against 9–19 at turn 235 here.
