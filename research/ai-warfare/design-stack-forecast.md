# Design: stack assault forecast (gap 5)

**Status:** proposed, awaiting the user's approval. It will be built behind a switch,
`AI_STACK_FORECAST`, off by default.

## Problem

`AI_stackAttackCity` attacks when the sum of the stack's strength, divided by the sum of
the defenders' strength, reaches the attack ratio.
- Modifiers are counted, but the sum is linear and combat is not. In game 2, 8 Javelineers
  attacked at 0.1–39 % per fight, lost 5 units and took nothing.
- About 200 of 2,659 AI attacks in 4 headless games were non-siege attacks under 5 %.
- Odds of one fight alone are also wrong for this decision. A stack can take a city even
  when most single fights are poor. Defenders keep their damage, so later attackers face
  weaker defenders, and one or two lucky wins can break through.

## Rule

Attack when the chance that this turn's attacks take the city is high enough for the
leader's appetite for risk. That chance comes from playing the attacks forward with the
engine's own combat rules.

## Method: Monte Carlo over the engine's rules

**Input.**
- The group's units that can still attack the plot this turn.
- The visible defenders on the plot, with their current damage.

**Per pair (attacker, defender), computed once with the engine's functions:**
- the defender's modified strength against that attacker
  (`kDefender.maxCombatStr(pPlot, pAttacker)`), which holds every modifier that applies:
  city defence, fortification, terrain, promotions, and the attacker's own attack bonuses;
- the attacker's strength (`maxCombatStr(NULL, NULL)`, as `resolveCombat` uses);
- firepower, first strikes (fixed and chance), withdrawal chance and combat limit;
- each siege unit's collateral damage: amount, number of units and limit.

**Per sample (64 samples, about 13,000 combat rounds at most for 10 attackers):**
1. Copy the hit points.
2. Pick the next attacker: the unused one with the best strength ratio against the current
   best defender (close to the engine's Lead From Behind choice). Pick the defender with
   the highest current strength against it.
3. **Siege units:** their collateral damage is applied first. They stop at their combat
   limit, as in the engine.
4. **Play the fight round by round, as `resolveCombat` does:**
   - Strength scales with hit points at the start of the fight.
   - Each round the defender wins with probability D/(A+D).
   - Damage per round follows the firepower formula with `COMBAT_DAMAGE`.
   - First strikes are rounds in which only the striker can deal damage.
   - The attacker may withdraw from a lethal hit, with its withdrawal chance.
5. The sample counts as a capture if every defender dies and an attacker remains that can
   still move in: one that has not attacked, or the winner if it has moves left.

**Randomness.**
- The forecast uses its own small generator, seeded from the turn, the group and the plot.
- It never draws from the game's random numbers. The game stays in sync in multiplayer
  and a replay of the game is unchanged.

**Output:**
- the chance of capture;
- the expected attackers lost;
- the expected defenders killed.

## Decision

- **Rule:** attack if the chance of capture is at least the threshold T.
  - T starts at 50 %.
  - It is shifted by the leader's personality: the existing `BaseAttackOddsChange`
    (a more aggressive leader accepts lower odds), and the same random spread the AI
    already uses for single attacks.
- **Siege units** keep attacking for collateral damage when the stack is next to the city,
  as now. Their effect is included in the forecast.
- **Where it applies:** first only in `AI_stackAttackCity`, which is the city assault. The
  linear ratio stays as a cheap pre-filter for distant cities. The forecast decides only
  next to the city.

## Cost

- At most a few hundred forecasts per turn: once per assault decision, next to a city.
- Each forecast is microseconds to a millisecond.
- The change in turn time will be measured.

## Tests

1. **Accuracy.** For every fight in a headless game, log the forecast's single-fight win
   chance next to the engine's `getCombatOdds`. They must agree within sampling error
   (about ±6 points at 64 samples).
2. **Effect.** Play 4 headless games with the switch off and 4 with it on, and compare:
   - non-siege attacks under 5 %;
   - units lost per city captured;
   - cities captured;
   - turn time.
3. **Replay.** With the switch off, the game must be identical to the current DLL.

## Risks

- **Too cautious:** stacks wait while the defender heals or reinforces. To watch: cities
  captured must not fall.
- **The attacker choice differs from the engine's actual choice.** The real attacks are
  still made by the engine. Only the decision to start uses the forecast.
