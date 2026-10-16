# A cunning opponent: strategic principles against measured behaviour

What would an AI do if it played Rise of Mankind like a capable strategist, and how
far is the real AI from that? This report takes classical principles of strategy, turns
each into something an AI can do in RoM and something we can measure, and compares
both with what the AI did in six whole Marathon games.

"Cunning" here does not mean predictable or uniform. A strong human player is hard to
read, and a good AI should be too. Personality and chance should decide between good
options; they should not pick bad ones. Everything below is meant in that sense.

## Data

- **Games:** six Marathon games to turn 450.
  - Mediterranean seeds 1 and 2, Earth 12 seeds 1 and 2: patch 0017.
  - Earth 12 seeds 1 and 2 again on patch 0016, where Genghis Khan has no city, for
    more wars.
  - The harness used the game's own base XML.
- **Totals:** 104 wars, 4,594 battles and 178 cities taken between civilizations.
- **War telemetry, new in the harness:**
  - for every declaration: the war plan, both teams' power, how much of the declarer's
    land army stood within two plots of the target's territory, and the target's other
    wars;
  - for every battle: the predicted odds, the size of the attacking group, whether the
    target was a city, and whether the attacker had collateral damage;
  - for every captured city: its population.
- **Tools:** [tools/war-analysis.py](tools/war-analysis.py); unit activity and phase
  summaries come from [the behaviour study](../ai-behavior/README.md).

Correlations from 104 wars show what tends to work. They are not controlled
experiments; the proposals below are meant to be tested the same way.

## The model

| | Principle | What a cunning AI does in RoM | Measure |
|---|---|---|---|
| G1 | Strategic depth | Claims land fast while it is free | Cities over time; settler idle time |
| G2 | The economy is war potential | Keeps an army sized to the threat; turns surplus gold into strength | Units per city; idle units; unspent gold |
| G3 | Balance of power | Contains the leader; when leading, keeps rivals divided | Wars on the score leader; the leader's share |
| O1 | Choose the war | Fights only where it has a real edge, or a coalition that can reach the target | Power ratio at declaration and its outcome |
| O2 | Concentration and surprise | Masses the strike force on the border, then declares | Army near the target at declaration |
| O3 | Speed | Takes the first cities before the defender can react | Turns to the first capture |
| O4 | Decisive objectives | Takes valuable cities and keeps them | Population taken; share razed |
| O5 | Culminating point | Ends wars that stall; makes peace on gains | Stalemates; ended wars without gains |
| T1 | Tactics | Softens defences with siege and collateral, attacks in stacks at good odds | Lone attacks; odds; exchange ratio |
| T2 | Force multipliers | Uses transports, generals and every unit it pays for | Idle units by role |

## Comparison

### G1 Strategic depth: the land grab comes late

- **Measured:** the median AI has one city for the first 100 Marathon turns and 1.7
  by turn 200. Two thirds of settler time is spent in cities, and the first war comes
  between turns 155 and 248.
- **Cunning:** RoM ties settlers to Agriculture, so a cunning AI researches it early,
  trains a cheap escort before the settler is done, and does not let a finished
  settler wait.
- **Causes:**
  - A settler leaves only with a defender, and a city lends one only beyond its minimum
    garrison. So the city must train an extra unit first.
  - On Earth 12, one civilization never founded a city at all, in every earlier game.
    Patch 0017 fixes that.

### G2 The economy as war potential: idle armies, unspent gold

- **Measured:** units per city rise from 2.9 to 8.9 (Mediterranean seed 1). Late in the game:
  - 61 % of troop transports have not moved for 10+ turns;
  - Great Generals stay in cities;
  - explorers are never retired;
  - on Epic the median AI holds 25,000 gold.
- **Cunning:** a peacetime army sized to the threat; transports built for a planned
  landing; gold spent on upgrades, rush-buying and diplomacy.
- **Cause:** whether a city builds a unit is a personality roll against a cost cap, not
  a measure of threat ([personality map 2.4](../diplomacy/code-maps/personality-map.md#24-unit-build-probability-and-the-bup-derived-upkeep-ceiling)).

### G3 Balance of power: nobody contains the leader

- **Measured:** 6 % of wars are declared on the score leader. With about ten teams,
  random choice would give about 10 %. The leader's share of the total score rises
  from 12 % to 32 % (Mediterranean seed 1). The leader declares 21 % of all wars.
- **Cunning:** when one player pulls away, the others coordinate: joint wars, embargoes,
  refusing it trades.
- **Cause:** war targets are chosen by what each AI can beat alone. The runaway is the
  one opponent nobody can beat alone (proposal 2 of the [diplomacy study](../diplomacy/README.md)).

### O1 Choosing the war: the AI often attacks stronger enemies

| Power ratio, declarer to target | Wars | Took a city | Net cities per war | Units lost by target per unit lost by declarer |
|---|---|---|---|---|
| below 1.0 | 32 | 28 % | -0.28 | 0.67 |
| 1.0-1.5 | 18 | 44 % | 0.00 | 0.71 |
| 1.5-2.0 | 19 | 53 % | +0.89 | 0.89 |
| above 2.0 | 35 | 60 % | +1.83 | 1.30 |

- **Measured:**
  - **Stronger targets.** 31 % of wars are declared against a stronger team, and they
    lose on average.
  - **Dogpiles mostly fail.** The AI likes targets already at war (58 % of
    declarations), which is sound in principle. But a third of all wars are dogpiles,
    and only 24 % of those take a city: the joiner often has no army anywhere near.
- **Cunning:** declare when the power that can actually reach the front is at least
  1.5 to 2 times the target's. Join a dogpile only with forces in reach.
- **Causes:**
  - The total-war filter discounts the enemy's defence to two thirds and accepts
    targets up to 1.2 to 1.95 times our own power, depending on the leader.
  - The dogpile filter adds the power of every co-belligerent, wherever they are
    ([personality map 1.1](../diplomacy/code-maps/personality-map.md#11-war-peace-combat)).
  - Power counts every unit on the map, including garrisons on another continent.

### O2 Concentration and surprise: war starts when the first group crosses the border

- **Measured:**
  - At declaration, a median 23 % of the declarer's land army stands within two plots
    of the target.
  - In 21 % of wars none of it does, and those wars take a city 5 % of the time. Most
    of them are dogpiles.
  - Massing more than half the army did not show a further gain: such wars took a city
    in 47 % of cases (15 wars), against 60 % with a smaller share near (67 wars). The
    measure counts all land units near the border, garrisons included, not the strike
    force. A trial of proposal 1 settles how much massing pays.
- **Cunning:** assemble the strike force on the border, ideally facing several cities at
  once, then declare and strike in the same turn.
- **Cause:**
  - The plan advances from "preparing" to war after a timer of about 10 turns if the
    shared area is rated offensive and enemy power is below 140 %
    (`CvTeamAI::AI_doWar`). Nothing checks where the army is.
  - The declaration then comes from `CvSelectionGroup::groupDeclareWar`: the first
    group that tries to enter the target's territory declares, wherever the rest of
    the army is. One stack starts the war, and the defender gets the turns the others
    need to arrive.

### O3 Speed: good once the army is there

- **Measured:** in wars that take a city, the first one falls a median 7.5 turns after
  declaration. 46 % of wars take any city at all.
- **Cunning:** the same speed with the main force present from the first turn, so that
  the 54 % of wars that never take a city become the exception.

### O4 Objectives: cities are razed by dice

- **Measured:** 22 % of the cities that change hands between civilizations are razed.
  The median captured city had population 6.
- **Cunning:** keep cities worth keeping; raze only what cannot be held or would cost
  more than it gives.
- **Cause:** raze odds are personality plus distance, with no term for the city's
  value ([personality map 2.2](../diplomacy/code-maps/personality-map.md#22-raze-probability-p1733-1930)).

### O5 Culminating point: half the wars achieve nothing

- **Measured:**
  - Of the wars that ended, 22 gained the declarer cities, 25 ended even and 6 cost it
    cities.
  - 18 of 104 wars ran 50 turns or more without a city changing hands.
  - The median ended war lasted 33 turns.
- **Cunning:** judge each war every turn by its progress against its cost (war
  weariness, lost units, missed growth). End stalled wars; take peace with
  concessions after gains.
- **Cause:** peace among AIs is checked only when a per-turn die succeeds. For the
  most warlike leaders that is under 1 % of turns, so a stalemate runs about 125 turns
  before it is even examined
  ([personality map 2.5](../diplomacy/code-maps/personality-map.md#25-war-and-peace-hazards-are-per-turn-dice-opportunity-blind-and-speed-unscaled)).

### T1 Tactics: too many lone attacks; losses equal kills

| | Declarer attacking | Target counter-attacking |
|---|---|---|
| Attacks | 2,961 | 1,633 |
| Won | 59 % | 68 % |
| Mean predicted odds | 65 % | 71 % |
| By a lone unit | 44 % | 66 % |
| Mean attacking group | 8.1 | 3.3 |
| On cities (won) | 49 % (48 %) | 19 % (57 %) |
| By units with collateral damage | 25 % | 20 % |

- **Measured:**
  - **Exchange ratio.** Declarers lose 2,323 units and kill 2,271, an exchange ratio
    of 0.98. Attacking well-defended cities is expensive in Civ4, but a capable
    attacker should still trade better than one for one.
  - **Stacks vs lone units.** Wars fought mostly with stacks gain 2.1 cities on
    average; wars fought mostly by lone attackers gain 0.5.
- **Cunning:** bombard defences down, use collateral damage before the assault, attack
  with the strongest unit against the weakened defender, and keep the stack together.
  Counter-attack in groups.
- **Causes:**
  - **Lone attacks.** Attack and counter-attack units also look for targets on their
    own, so many attacks are single units.
  - **Optimism.** The AI adds an optimism bonus of 7 to 13 points (up to 27) to its
    odds, re-rolled every turn. A unit that wants 60 % then attacks at a true 33 to 53 %
    ([personality map 2.1](../diplomacy/code-maps/personality-map.md#21-attack-odds-optimism-p16193-16210-u934-u1012-u24929)).

### T2 Force multipliers: built, then left idle

From the behaviour study, turns 301-400 on Marathon, per game:
- 59 troop transports, 61 % unmoved for 10+ turns;
- 19 settler ships;
- 12 Great Generals, 78 % in cities;
- about 13 explorers kept through turn 300.

A cunning AI builds these for a plan and uses or retires them.

## What the AI already does well

- **It is opportunistic.** It prefers targets that are already at war.
- **It assaults cities in stacks of about eight**, with collateral units in a quarter of
  attacks.
- **Its predicted odds are close to the actual outcomes** (65 % predicted, 59 % won).
- **It takes the first city within about 7 turns** once it is in position.

The gaps are in when and where it commits, not in how it fights once its army is
there.

## Changes that would make it cunning, with variety kept

Ranked by expected gain for the effort.

1. **Declare when massed.**
   - **Change:** a war plan becomes war only when a share of the strike force (city
     attackers, siege and collateral units) can reach a target city within a few turns.
     The share is personality-biased, about 40 to 70 %, and that check replaces both
     the timer and "the first group crosses the border". A plan that never reaches the
     threshold is abandoned as today.
   - **Evidence:** the measured loss is the fifth of wars declared with nothing in
     reach (5 % take a city). Whether a larger share near the border pays beyond that
     is not shown by these games.
   - **Measure:** army near the target at declaration, turns to the first capture,
     wars that take a city.
2. **Count power that can reach the front.**
   - **Change:** for target selection and dogpiles, compare the power within N turns
     of the target with the target's defence, without the two-thirds discount. A
     leader's appetite can still shift the threshold.
   - **Measure:** declarations below ratio 1.0; net cities per war.
3. **Judge wars by progress, every turn.**
   - **Change:** replace the peace die with a war value that falls with stalled turns,
     losses and war weariness, and rises with recent gains. Personality sets patience,
     not whether the question is asked.
   - **Measure:** stalemates; ended wars without gains.
4. **Attack from the stack.**
   - **Change:**
     - city assaults go through the stack's siege and collateral units first;
     - attack and counter-attack units in a war area join a nearby stack or wait for
       it, unless the odds are high;
     - the optimism bonus becomes a fixed personality offset, with no per-turn
       re-roll.
   - **Measure:** lone attacks; exchange ratio.
5. **Raze by value.** Score a captured city by population, buildings, wonders and
   position, then let personality tilt the decision (proposal 3 of the diplomacy
   study).
6. **Coalitions against a runaway.** Add a balance-of-power term to target selection
   and alliance acceptance (diplomacy proposal 2).
7. **Use what was built.** Plan transports per operation, disband or reuse idle ones,
   retire explorers once the map is known, attach Great Generals. Also: escort
   settlers only when danger is in range.

Each item can be measured with the same telemetry and games, before and after. That
also shows whether behaviour still varies enough between leaders and games.
