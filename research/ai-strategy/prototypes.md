# Prototypes: a more cunning war AI, measured

The [comparison with a cunning strategist](README.md) proposed four changes:
- declare war once the army is massed;
- count only the power that can reach the target;
- judge wars by their progress;
- attack from the stack.

This report prototypes them in the real DLL, measures each one in whole Marathon
games, and follows two leads the measurements turned up. Those leads are wars the AI
joins on request, and how a stack's composition and use decide an assault.

Each change sits behind one bit of a new define, `AI_CUNNING_FLAGS`. With the define
at 0 the game is unchanged: a Mediterranean game with every switch off replayed the
patch 0017 game identically over all 451 turns.

## Method

- **Games:** Mediterranean and Earth 12, map seeds 1 to 4, Marathon, Noble, turn 0 to
  450. The same 8 games per arm.
- **Arms:** the patch 0017 DLL (baseline), all switches on, and each switch alone.
- **Telemetry:** the harness now also records every city assault. That covers the
  attacking stacks' composition by unit class, bombardment and ranged strikes, the
  walls left at the first attack, whether a collateral unit opened, the defenders'
  health when hit, and whether the city fell that turn
  ([harness README](../../toolchain/harness/README.md)).
- **Tools:** [ab-compare.py](tools/ab-compare.py) (arms side by side),
  [assault-analysis.py](tools/assault-analysis.py) (what takes cities),
  [war-analysis.py](tools/war-analysis.py) (wars).

The games diverge once a change alters a decision, so arms are compared as
populations of wars and assaults, not game by game. With 8 games an arm has 100 to
150 wars. Differences of a few points in a percentage, or 0.2 in net cities per war,
are within chance.

## Two leads from the measurements

### A quarter of all wars are bought, and they achieve nothing

An AI at war pays other AIs, in technology or gold, to declare war on its enemy
(`CvPlayerAI::AI_doDiplo`). The joiner accepts if its power, plus the asker's,
exceeds half the target's for land targets, or the target's whole power otherwise
(`CvTeamAI::AI_declareWarTrade`). Neither side asks whether the joiner's army can
reach the target. "Land target" is true for every team on a large continent that is
still mostly unclaimed, as both test maps are for most of the game.

In the 8 baseline games:

| | Wars | Take a city | Net cities per war | Declared with nothing near | Declarer's battles per war |
|---|---|---|---|---|---|
| Bought wars | 39 | 8 % | -0.05 | 69 % | 10 |
| The AI's own wars | 103 | 50 % | +1.06 | 10 % | 34 |

The bought wars are most of the "declared with nothing near" wars of the [first
report](README.md#o2-concentration-and-surprise-war-starts-when-the-first-group-crosses-the-border).
The AI's own war plans almost always have troops near the target. The asker pays
technology to a rival for a war that never happens.

### What takes a city: size first, then how the defence is softened

519 city assaults in the baseline games (one team against one city in one turn):

| Stack | Assaults | City taken |
|---|---|---|
| 1 unit | 131 | 12 % |
| 2-5 units | 162 | 35 % |
| 6-15 units | 154 | 46 % |
| 16+ units | 72 | 74 % |

At the same stack size, composition and use matter less but still count:

| Stacks of 10+ units | With | Without |
|---|---|---|
| Collateral unit in the stack | 61 % | 52 % |
| A collateral unit attacks first | 62 % | 52 % |
| Siege unit in the stack | 60 % | 56 % |
| Archers in the stack | 50 % | 64 % |

Defenders already down to 60 % health or less when hit: the city fell in 60 % of
assaults, against 24 % when they were at 90 % or more. Part of that is circular, since
later attacks in a long assault meet damaged defenders.

How the baseline AI uses these units:
- **Bombarding.** It bombarded on the same turn as only 3 % of assaults; the walls
  were above half in 78 %.
- **The cause is a defect.** `CvUnitAI::AI_bombardCity` asks only whether the stack's
  head unit can bombard. A stack led by a swordsman does not bombard even when it
  carries catapults.
- **Archers.** RoM gives 11 archer and 13 siege units a ranged strike. The AI fires
  it only by chance, from `AI_anyAttack`. City defenders, the usual role for
  archers, never fire at all.
- **Dale's combat mod.** Its archer bombard is switched off. Its ranged bombard is
  switched on, but no unit has a range, and the AI's calls to it are blocked.

## The switches

| Bit | Change | Code |
|---|---|---|
| 1 | A prepared war (limited or total) starts only when 40 to 70 % of the offensive land units stand within three plots of the target's territory. Cautious leaders want more. Plans that never gather are dropped as before. | `CvTeamAI::AI_isStrikeForceReady`, `AI_doWar` |
| 2 | War targets are compared by the land power each side has in the target's land areas, without the old two-thirds discount on the target's defence. Dogpiles count each co-belligerent's power there, and join only if the AI can fight the target itself. | `AI_getReachablePower`, `AI_getReachableDefence`, `AI_doWar` |
| 4 | Each chosen war is reviewed once per period: 14 to 60 Marathon turns, longer for leaders slow to make peace. The review replaces the per-turn peace die. A war that gained a city's worth of war success, and more than the enemy, goes on. Otherwise peace is made if both sides value it at least half as much as the other. | `CvTeamAI::AI_reviewWars`; two saved arrays in `CvTeamAI` |
| 8 | The stack bombards if any of its units can, not only the head unit. A collateral unit opens the AI's assaults while two or more defenders are unhurt and the best attacker's odds are below 80. | `CvUnitAI::AI_bombardCity`, `CvSelectionGroup::groupAttack` |
| 16 | Collateral units join city-attack stacks in offensive areas, and are among the units trained for invasions. | `AI_collateralMove`, `CvCityAI` |
| 32 | An AI at war pays only allies that are near the enemy: a shared border, or cities within 8 plots of the enemy's on the same landmass. The ally accepts only on the same terms. | `CvPlayerAI::AI_doDiplo`, `AI_declareWarTrade`, `CvTeamAI::AI_isNearTarget` |
| 64 | Archers and siege in a city fire ranged strikes at enemy units next to it. A ranged strike does not move the unit, and it still defends. | `CvUnitAI::AI_update` |

## Results: each switch alone

8 games per arm. Cities captured counts every city that changed hands between
civilizations.

| | Base | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|---|
| Wars per game | 17.8 | 16.9 | 18.0 | 18.9 | 15.5 | 18.1 | 15.5 | 16.6 |
| Declared against a stronger team | 30 % | 30 % | **20 %** | 38 % | 35 % | 31 % | 24 % | 33 % |
| Declared with nothing near | 26 % | 27 % | 23 % | 26 % | 19 % | 19 % | **7 %** | 26 % |
| Wars that take a city | 39 % | 39 % | 44 % | 46 % | **48 %** | 38 % | **53 %** | 40 % |
| Net cities per war | 0.75 | 0.53 | **1.12** | 0.83 | 0.76 | 0.64 | 0.79 | 0.67 |
| Stalemates per game | 2.8 | 3.3 | 3.4 | 2.5 | 2.4 | 3.5 | **1.9** | 3.0 |
| Units lost per city taken | 7.4 | 7.9 | 5.7 | 6.0 | **5.1** | 7.1 | 6.6 | 6.8 |
| Cities captured per game | 27.5 | 24.6 | 30.6 | **33.4** | 30.9 | 28.1 | 26.8 | 27.5 |
| Late turn time (s) | 4.9 | 3.7 | 4.4 | 4.4 | 4.3 | 4.6 | 4.9 | 4.6 |

- **2, reachable power:** the AI's own wars against stronger teams fell from 21 % to
  9 %. Those wars gain 1.57 cities each instead of 1.06, at an exchange ratio of 1.24.
- **4, war review:** wars end sooner (median 27 turns against 35), and the cities
  captured rise by a fifth. Peace in stalled wars frees armies for the next war.
- **8, stack employment:** the largest gain per assault. 48 % of wars take a city,
  and each city costs 5.1 units instead of 7.4.
- **32, war requests:** bought wars fell from 39 to 11, and those that remain take a
  city 36 % of the time instead of 8 %.
- **64, city archers:** ranged strikes from cities tripled in a test from the turn-400
  position. Over whole games the war numbers barely move, since every AI's cities
  defend a little better.
- **1, massing gate:** more of the army is in place at declaration (median 21 %
  against 16 %), but wars gain less. The AI's own wars already have troops near
  90 % of the time; the empty-handed wars were the bought ones. Waiting gives the
  target time.
- **16, collateral units in stacks:** big stacks with collateral units take more
  cities (64 % against 31 % at 10+ units), but whole wars gain less (0.64 net cities
  against 0.75). Collateral units drawn into stacks are missing from other roles, and
  wars end without cities more often.

## All switches together

Measurement of the combinations is still running; this section follows with it.

## What did not work, and why

Two earlier versions of switch 8 made the AI worse. Both are kept out of the patch.

- **Bombard the walls down to a quarter before attacking.** Stacks waited at the
  walls. Big stacks attacked 4.3 times per assault turn instead of 9.5, and took the
  city 29 % of the time instead of 55 %. Cities captured fell from 27.5 to 23.4 per
  game. The AI's own skip-bombard rules are better than a fixed target.
- **Ranged strikes by the stack's archers and siege before the assault.** Captures
  fell from 18 to 8 in 25 turns from the turn-400 position. The cause is a rules
  interaction:
  - A ranged strike costs the unit its move.
  - When the stack moves on, into the captured city or towards the next one,
    `CvSelectionGroup::groupMove` splits off every unit without moves.
  - The archers and catapults left behind then act alone. Collateral units attack
    on their own at odds as low as 20 to 35 %.
  - Lone attacks rose from 44 % to 56 %.

  In defence there is no such cost: a city's archers do not move. That is switch 64.
- **Steady optimism:** the leader's attack-odds bonus as a fixed trait instead of a
  daily roll. No measurable effect, so it was dropped.
- **Switch 32, first version.** It tested whether the target was a "land target",
  and that holds for every team on a large, mostly unclaimed continent. Bought wars
  did not fall until the test became a real distance: a shared border, or cities
  within 8 plots.
