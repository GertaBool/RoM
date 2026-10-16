# Design: exact stack assault forecast (gap 5)

**Status:** built behind a switch, `AI_STACK_FORECAST`, off by default (0). The value is
the capture chance needed, per mille. The first version used sampling; on the user's
direction it was replaced by the exact computation below.

## Problem

`AI_stackAttackCity` attacks when the stack's summed strength over the defenders' summed
strength reaches the attack ratio.
- Modifiers are counted, but the sum is linear and combat is not. In game 2, 8 Javelineers
  attacked at 0.1–39 % per fight, lost 5 and took nothing.
- About 200 of 2,659 AI attacks in 4 headless games were non-siege attacks under 5 %.
- Single-fight odds alone are also wrong for this decision. Defenders keep their damage,
  so a few lucky wins can break through.

## Mathematics

**One fight.** The inputs are what `resolveCombat` uses:
- A is the attacker's strength; D is the defender's strength against that attacker, with
  every modifier, scaled by its current hit points.
- The defender wins a round with probability q = ⌊1000·D/(A+D)⌋/1000, as the engine's die
  roll gives; the attacker wins one with p = 1 − q.
- Damage per round follows the firepower formula with `COMBAT_DAMAGE`. So the attacker
  needs n_A hits (to kill, or to reach its combat limit), and the defender needs n_D.

With no first strikes:
- The attacker wins with probability Σ_{k<n_D} C(n_A−1+k, k) · p^{n_A} · q^k.
- The attacker loses after dealing exactly m hits (m < n_A) with probability
  C(n_D−1+m, m) · q^{n_D} · p^m. This is the exact distribution of the defender's
  remaining hit points.
- A losing attacker dies with probability 1 − withdrawal; otherwise it withdraws.

**First strikes.** Each side's first-strike count is uniform over [fixed, fixed + chance],
as the engine rolls it. The difference f is the number of free rounds. The hits made in
those rounds are binomial (f, p) for the attacker, or (f, q) for the defender, and the
normal rounds follow with the hits still needed. This is the decomposition
`getCombatOdds` uses.

**The stack's turn: dynamic programming over the defenders' hit points.**
- The state is the vector of defender hit points, and its probability.
- Attackers go in a fixed order: siege units first, then by single-fight win chance
  against the strongest defender.
- In each state the attacker meets the defender with the highest current strength
  against it, as the engine picks. A siege unit first applies collateral damage, by the
  engine's formula, to the defenders with the most hit points.
- Each fight splits the state by the exact distribution above.
- A state in which every defender is dead counts as a capture if a unit can still move
  in: one that has not attacked, or the last winner if it has more than one move.
- States below 10⁻⁹ are dropped, and at most 2,048 states are kept per step.

**Result:**
- the exact capture chance (per mille);
- the expected attackers lost.

**Simplifications, to be checked by test:**
- The attack order is fixed at the start. The engine re-picks after each fight.
- Collateral damage targets the healthiest defenders. The engine picks at random,
  weighted by hit points.

## Decision

Next to the city, the stack starts its attack if the capture chance is at least
`AI_STACK_FORECAST` − 10 × the leader's attack-odds change. The attack-odds change is
the existing personality value: base 0–6 plus a random 0–16, with 8 the most common. An
aggressive leader therefore accepts lower odds. Further from the city, the summed ratio
still decides whether to move towards it.

## Tests

1. **Accuracy.** For every fight in headless games, the forecast's single-fight win chance
   is logged next to the engine's `getCombatOdds` (test build only). They should match
   exactly, apart from rounding.
2. **Effect.** 4 headless games with the switch off (0) and 4 with it on (500). Compare
   non-siege attacks under 5 %, units lost per city captured, cities captured, and turn
   time.
3. **Off means unchanged.** With the switch at 0, the forecast code is never reached.
