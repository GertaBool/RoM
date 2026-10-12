# Making RoM's AI competent: plans, opportunity costs and execution

Subsequent implementation: [economic arithmetic kernel](../../simulation/economy/README.md) and [settler landing handoff fix](../landing/README.md). The dated research below retains its original source identity.

**Recommendation: build a shared economic/project planner and reliable job execution, then use specialized search and learning where they earn their cost.** The next major improvement should compare complete, feasible ways to obtain a capability—not add another personality weight or recruit more units because a local branch runs first.

Research pass: 12 October 2026. GitLab remains at `6222511`; GitHub contains cumulative patch 0007. This study inspects local patched source `8edb23b96c7b9f6369a54d18d0a84a62c799b841`. [Pinned source map](source-map.json), [retrieved literature and implementation ledger](sources.json), [implementation specification](IMPLEMENTATION.md), [evaluation scenarios](evaluation.json).

This builds on the [earlier algorithm study](../algorithms/README.md), rather than replacing it with a new list of fashionable methods. Eight primary texts were retrieved and selected sections inspected, along with pinned Freeciv, Unciv, OpenRA and Cicero source. The earlier PDF-access limitation no longer applies to those texts. No human was contacted and no external bot was run. Downloaded papers remain outside this repository; citations and hashes are published.

## 1. What is actually holding the AI back

The game already has a hierarchy: team war plans; player agendas, budgets and strategic context; city governors and production; military operations; selection groups; individual roles. It also has substantial rule knowledge in C++, Python callbacks and effective XML. Replacing that with a single optimizer would throw away useful legality and tactical behavior.

The missing coordination is more specific:

| Current mechanism | Why it is insufficient | Required replacement or boundary |
|---|---|---|
| `AI_chooseProduction` commits through early-return branches | A useful later choice can never compete; worker/workboat output changes future production, growth and research | Pure proposals plus short economic rollout; commit one selected first action |
| `AIProductionChainPolicy::readinessPercent` multiplies availability discounts | A percentage is not a dated plan to acquire technology, mine, connection and prerequisite building | Explicit prerequisite tasks with feasible completion dates and reserved resources |
| `AI_doCivics` adds separately scored category winners | Payoff may require future worked pastures; package interactions and the option to switch later are missed | Joint package evaluation against the same development plan, including anarchy and deferral |
| Governor reputation follows a change in aggregate prosperity | Geography, national investment and war disruption confound attribution; feedback can reinforce a label without proving that its policy helped | Holdout ablations and outcome deltas against controlled alternative decisions |
| Unit roles and mission queues share decision authority | A valid local action can steal a unit from a useful expedition or erase its destination | One owner for each accepted job, explicit reservations, progress and recovery |
| Transport and city production use role counts and broad maritime priorities | A boat has no demonstrated value merely because it exists; a missing escort or pickup can dominate the schedule | Concrete delivery requests, compatible parties and marginal fleet capacity |
| Settlement patch 0007 optimizes the existing delivery-discounted found value | Better search over a flawed economic estimate can confidently pick the wrong city | Population-constrained development rollout and marginal empire value |
| Scalar technology path estimates sum shared prerequisites | They can charge for the same unlock twice and choose incompatible cheap OR branches | Distinct prerequisite packages, then execute the evaluated package |

These are inspected source properties, not claims that every reported harbor turn has been reproduced. The [transport entry](../transport-entry/README.md) and [joint settlement search](../settlement-search/README.md) already repair important execution/selection gaps, but do not supply the missing economic model.

Two further cautions from this pass:

* `AI_getStrategicContext` still counts queued settlers twice (`AI_totalUnitAIs` already includes training). Its inspected agenda consumer only checks whether the count is zero, so this does **not** currently establish a changed agenda decision. Correct the representation before using it as a quantity in a new planner; do not market this as the cause of bad play.
* Patch 0007's branch-and-bound is exact for its declared static utility and supported routes, but has no constant path-query cap. Its worst case is large. A new economic evaluator also invalidates its `foundValue` upper bound unless the new objective is bounded by that value. Both issues need explicit integration work, not optimistic claims about the existing patch.

## 2. The objective: better outcomes, not more activity

At strategic scale, optimize expected victory prospects against a varied opponent population. A small online planner cannot directly solve the full stochastic, partially observed, multiplayer campaign. Give it a calibrated approximation of **marginal empire value**, relative to continuing the incumbent plan:

```
plan value = expected discounted economic/strategic outcome difference
             - opportunity cost of scarce units, gold and production
             - expected losses and switching cost
             + terminal value of capabilities beyond the planning horizon
```

Do not count the same economic benefit twice as tile yield, extra production and a separately valued completed unit. A flow-based rollout accounts for intermediate production through resulting state; terminal value accounts for what remains beyond its horizon. Strategic resource access has additional option value only when it unlocks plausible useful actions.

The baseline matters. Moving an existing worker to a new city sacrifices its previous improvement job. Shipping an escort away can delay a real defense commitment. Building a boat consumes city production and maintenance. Staying with the current build is a candidate, not a zero-value absence of action.

Safety should be temporal and evidence-based. Compare estimated enemy arrival/combat outcomes with the plan's reinforcement dates. An economic investment can be the fastest route to adequate fighting power. A visible attack that arrives before the investment pays back can reverse that choice. A missing visible enemy is not proof of zero risk, but an imagined worst-case rush on every turn is not a calibrated threat model either.

Use a small set of consistent opponent scenarios initially: observed force continues, retreats or reinforces; a plausible unseen force constrained by known access and recent sightings. Measure prediction calibration. Apply an explicit city-loss risk limit or tail-loss penalty where appropriate; do not hide universal conservatism in a huge generic danger multiplier. Never let an optimizer exploit opponent information outside its declared observation contract.

## 3. First priority: economic project planning

The closest useful research analogy is build-order optimization, coupled with receding-horizon control [P1, P2]. Churchill and Buro model prerequisites, borrowed resources, consumed resources and produced resources, and search concurrent build orders. Their paper also explicitly limits optimality to its abstraction and assumes that build goals are supplied. That distinction matters here: RoM must choose worthwhile goals as well as schedule them.

Represent small packages such as:

- Workboat → reachable water improvement → actually worked yields → growth/research/production benefit.
- Worker travel → legal mine → resource connection → trainable unit → delivery to operation.
- Settler + escort + optional ship → rendezvous → founding → workable food tile → viable second city.
- Technology package → prerequisite building → trained force before an opponent's vulnerable window closes.
- Civic package → anarchy → changed tile/upkeep output, with an option to wait until a pasture or technology is ready.

Use an HTN-like set of methods to generate these useful task structures [P3]. HTN is a way to represent domain knowledge and legal decompositions; it does not prove that the chosen strategy is best. Always retain a useful incumbent, a legal fallback, and a method for waiting when waiting has value.

Within a package, solve tiny scheduling problems exactly. Across interacting packages, use bounded beam search or best-first branch-and-bound over **completion events**. Borrowed resources include city production slots, worker time, ships and escort commitments; consumed resources include gold and units expended on improvements. Resource output can change future task durations. That is why sorting current `value / buildTurns` is insufficient.

Replan on completion, new information or a material change; execute only the accepted next action and maintain the rest as a revisable commitment. Carry progress forward. Receding horizon is useful because the forecast will be wrong [P2]; the stability and feasibility theorems of control theory do not automatically apply to a discrete adversarial game.

### What the new C++03 experiment shows

The original [planning lab](planning_lab.cpp) models a city production slot, independently occupied activity slots, prerequisites, changing production/income rates, optional anarchy and an explicit defense deadline. It includes full state-space search for small models and a width-limited beam with a validated goal-first fallback. It is a research model, not a replacement for `CvCity::doTurn`.

| Controlled scenario | Exact model result | Why it matters |
|---|---|---|
| Base production 2; defender costs 12; workboat costs 4; one-turn improvement adds 4 production | Workboat completes at 2, improvement at 3, defender at 5; direct defender would take 6 | Economic development can improve the defense deadline itself |
| Defender costs 6; attack deadline is 3 | Defender starts immediately and completes at 3; workboat follows | Planning does not imply blindly preferring development |
| Same peaceful economy, no defense requirement | Improve the water resource; omit the optional guard | Empty guard count alone does not create a goal |
| Civic switch with anarchy and no realized payoff | Keep the current civic | No reward for switching merely because a category score increased |
| One worker must mine then connect a resource before recruitment | Mine finishes at 2, connection at 3, recruitment at 5 | Capability readiness is a schedule, not a fractional discount |

[Results](results.json): all **165 models** match an independent exhaustive enumerator of absolute start-time calendars. Every returned feasible schedule is independently replayed, including resource exclusivity and deadlines. A width-one beam is suboptimal in **13 cases**, with a maximum utility gap of 4. Widths 8 and 32 match these small oracles, which is not a general optimality guarantee. Budget-limited results remain labelled approximate even when they happen to match the optimum.

The optimized 165-case batch took roughly 10 ms on this Linux instance, including process launch, serialization and Python witness checks. That figure excludes native pathfinding, city updates, Python callbacks, population and the full game economy; it is not a DLL performance estimate. See [MODEL.md](MODEL.md) for precise semantics, missing mechanics and complexity.

The earlier prerequisite/assignment lab was also rerun against the current source XML: **300 research-package and 160 assignment oracle cases passed**. Its [separate results](prerequisite-assignment-results.json) preserve current fixture identity without overwriting the historical experiment. These checks establish the represented subproblems, not full economic or naval behavior.

## 4. Transport: schedule a delivery service, not several cooperating guesses

Freeciv is a useful implementation reference [I1]. Its ferry AI records passenger/boat associations in both directions, distinguishes requested, available and abandoned assignments, updates availability statistics and clears associations when units disappear. It also treats bodyguard capacity explicitly. This demonstrates concrete ownership/recovery machinery; it does not prove that Freeciv's route choices should be copied unchanged.

For RoM, use an expedition job with a destination, party manifest, embarkation point, landing point, predicted arrival, owner and lease/progress state. A walking route is one method of that job. A sea route is another. Manual boarding or autoplay changes trigger reconciliation of actual memberships with the job, rather than independent role decisions by each passenger.

Generate complete feasible candidate bundles:

```
(settler, escort or justified escort-free method, ship if needed,
 pickup, landing, inland leg if needed, destination, time/resource reservations)
```

Then select compatible bundles. **This is not generally ordinary bipartite matching.** A bundle simultaneously consumes a settler, a particular escort, a ship/time interval and a settlement site; three-way compatibility and conflicting city radii make it a set-packing/scheduling problem. Use exact subset/branch-and-bound for small local fleets, and a bounded master selection with local swaps for larger ones. A flow relaxation can give bounds or solve a genuinely separable subproblem, but must not split an indivisible party into mathematically convenient cargo.

Min-cost flow *does* fit assigning already formed, mutually compatible parties to ship departure slots when those edge values and capacities are separable. Its cost should include arrival delay, exposure, maintenance and the ship's next-best job. Multi-stop pickup/delivery with time windows is harder; begin with one-party direct voyages and nearby rendezvous before tackling a global vehicle-routing problem.

Fleet production follows accepted demand: compare the best delivery schedule with and without one additional hull. A marginal improvement can justify a ship; a maritime flavor or unused cargo capacity alone cannot. The first correctness gates are completed viable voyages, bounded unexplained harbor stalls, and no duplicate use of an escort—not boat utilization or the number of galleys built.

## 5. Settlement and workers must share a development forecast

For each destination/arrival scenario, initialize the actual city's population, center yield, available plots, ownership/culture timing, happiness/health, trade access and maintenance. At each forecast step, only citizens actually available may work tiles. A fish resource is valuable when a legal workboat can improve it and a citizen can use it; a resource connection may unlock production even when the tile is not worked. Keep those effects separate.

Use a small cardinality/food dynamic program or exhaustive oracle for citizens inside the rollout. Under an additive per-turn model, `O(J P F)` for J slots, P citizens and F represented food totals is practical; nonlinear specialist, threshold and growth effects require additional state or explicit evaluation. It does not make the entire multi-turn city plan polynomial or exact.

Worker allocation starts with independent one-worker jobs and min-cost matching/flow, using values derived from completion-time differences in that forecast. Include continuing a partly completed improvement. Multiple workers on the same job, roads that connect several cities, chopping and tech-dependent improvements need project scheduling rather than independent slot scores. Include the worker opportunity cost in settlement decisions; otherwise every potential city implicitly borrows the same worker for free.

For choosing several future cities, compare compatible portfolios with shared maintenance, workers, transport and overlapping worked tiles. A small beam with add/drop/swap moves is a sensible first approximation. Preserve route/geographic diversity when using a budget, and measure missed opportunities against exhaustive tiny maps. Patch 0007 already removes the old movement shortlist restriction; it should not acquire a new unsafe top-K cutoff under a different name.

## 6. Cunning: opportunities, timing and information

Cunning should emerge from comparing plans that exploit an opponent's constraints:

* Recruit a force that arrives before the opponent's reinforcement or technology date, rather than accumulating a large idle army.
* Pillage a strategic connection if it prevents a dangerous unit upgrade or new production; compare that with attacking the city directly.
* Feint, scout or stage when the information or repositioning changes a later decision. Exploration has value because it can change the selected plan, not merely because it reveals tiles.
* Negotiate access or trade for a missing resource when it beats researching, conquering or detouring for it.
* Abandon a siege whose reinforcement race has become unfavorable, preserving useful units instead of satisfying a stale operation label.

At the operation level, use a small portfolio of these macro-actions and short rollouts. Start with exact combat calculations where the source exposes them, then bounded expectimax or MCTS for attack ordering, collateral, retreat and keeping a capturer alive [P4]. MCTS needs a faithful transition/evaluation model; it cannot supply one. A simple operation portfolio is a stronger first baseline than millions of searches over invalid or purposeless unit moves.

For hidden information, maintain a small opponent belief model before considering POMCP/information-set search [P5]. POMCP requires a generative simulator and suitable beliefs; its convergence statements are conditional, not a finite-budget guarantee for a multiplayer diplomacy campaign. Sampling a hidden world and acting as if the AI knows which world it sampled creates strategy fusion. Actions must depend on observations actually available to the player.

For diplomacy, preserve game legality and hard denials, then search offer bundles against predicted acceptance and strategic effects. Repeated deals and coalition risks matter. Cicero's inspected code separates strategic search, opponent-type beliefs and learned policy/value models [I4]. That is a useful architectural lesson; importing its language-model stack or equilibrium assumptions is not a suitable drop-in upgrade for RoM's structured trade menus.

## 7. Which algorithms to deploy, and which to postpone

| Priority | Algorithm | Specific implementation target | Guarantee/cost boundary |
|---|---|---|---|
| First | Receding-horizon project search + HTN-style methods | Workboat/worker/recruitment/settlement/civic packages | Beam is budget-limited; exact small scheduling is exponential in general |
| First | Finite-state job executor + resource reservations | Settler/escort/ship and operation ownership | Progress/cancellation invariants; not itself a strategy optimizer |
| First | Exact assignment / min-cost flow for separable tasks | Regional workers, already formed parties, some reinforcement slots | Matching `O(n^3)`; edge generation and paths often dominate |
| Next | Small DP / exact package search | Citizen allocation, gold allocation, shared tech prerequisites, civic combinations | Exact within the represented state/objective; dimensionality and package interactions matter |
| Next | Portfolio search, expectimax, then MCTS | Tactical/operation alternatives with verified transitions | Simulations × transition/evaluation cost; no finite-budget global guarantee |
| Conditional | D* Lite / reusable distance fields | Repeated related paths with stable movement profiles | Reuse only with valid state/cache keys; changing goals/groups can defeat it [P6] |
| Offline first | CMA-ES, constrained evolution, compact learned ranking | Economic value weights, terminal values, method ordering | Training cost dominated by campaign evaluations; inference stays cheap [P7] |
| Experimental online | Rolling-horizon evolutionary search | Compact macro-action sequences with a trustworthy forward model | `O(generations × population × horizon × transition cost)` plus repair; compare equal budgets [P8] |

RHEA is a real online planning alternative, not something to reject merely because it is evolutionary. The inspected survey emphasizes how strongly population, horizon, evaluation and reuse settings interact [P8]. Test it against a well-implemented beam and useful scripted portfolios on the **same** model and forward-model budget. Genetic crossover does not automatically preserve prerequisite order, resource reservations or city legality; encode or repair these constraints explicitly. CMA-ES is more natural for continuous weights than for assigning indivisible passengers to ships.

Do not use an online LLM to choose individual DLL actions. Do not replace the closed host pathfinder merely because a newer graph algorithm exists. Do not train a settlement model to imitate old `AI_foundValue` decisions. The existing pairwise trainer correctly calls for controlled outcome labels; retain that requirement.

## 8. What to trim, retain and test by ablation

Retain native legality, economic accounting, combat rules, effective XML, useful operation phases and tested movement/mission handling. Make these callable through pure snapshots/adapters where possible.

Replace ordinary early-return production competition with proposal/evaluate/commit. Remove duplicated scores only after the package evaluator covers their effects. Keep immediate tactical interrupts as explicit reasons, not buried priority exceptions.

Test governor/career feedback and flavor multipliers with controlled on/off variants. The current prosperity calculation sums potential yields across assigned city plots, not only the population's worked output, and attributes subsequent changes to the governor. That is a questionable signal of decision quality. Personality can produce coherent strategic variation; it should not outweigh evidence that a concrete plan is infeasible or inferior.

Do not mistake free commander replacement, occupation reductions or other rule effects for smarter planning. Keep those rules fixed in algorithm comparisons and report their contribution separately if changed. Any feature that adds state, runtime and interactions without improving held-out decisions is a candidate for removal. The present inspection alone does not establish which entire subsystem should be deleted.

## 9. Implementation sequence and proof required

1. **Create the first faithful economic slice and pure proposals.** Capture worked plots, growth/production stocks, overflow, food-production units, modifiers, research, maintenance and timed improvements. Differential-check one-city transitions against a matching rebuilt DLL. The lab supplies scheduling tests, not that accounting engine.
2. **Connect the short economic planner to ordinary city production and settlement valuation.** Begin in shadow mode using already captured values, then commit selected first actions. Test workboat-first/guard-first reversals, barren coasts, lost workers, delayed borders, happiness limits and anarchy.
3. **Introduce expedition jobs and a small compatible-bundle selector.** Cover manual boarding, passenger-first/ship-first updates, group replacement, distant pickup cancellation, partial landing and invalid destinations. Drive new ships from marginal delivery demand.
4. **Allocate workers and research packages against those accepted plans.** Ensure the evaluated tech order is the one queued; ensure one scarce worker or escort is not promised twice.
5. **Add operation opportunity search and opponent scenarios.** Make force delivery, scouting and withdrawal decisions legible before increasing tactical search depth.
6. **Train compact evaluators and compare alternative searches.** Use paired held-out maps/eras/opponents and full campaigns; retain individual failure scenarios as regressions.

This order differs from the earlier general study's research-package-first recommendation because the user's observations and subsequent code work identify economic sequencing and job completion as the more immediate competence bottlenecks. The prerequisite solver remains useful, but should serve the shared plan rather than become another independent subsystem.

Success means better opening payoff and expansion, useful resource connections, completed deliveries, stronger operations and improved held-out game outcomes at an acceptable turn-time cost. The [evaluation specification](evaluation.json) distinguishes source tests, model experiments and rebuilt-engine evidence. Passing the lab does not certify an improved opponent; it supplies a tested planning mechanism and falsifiable integration targets.

## Sources actually inspected

**P1.** Churchill & Buro (2011), [Build Order Optimization in StarCraft](https://ojs.aaai.org/index.php/AIIDE/article/download/12435/12294).

**P2.** Rawlings, Mayne & Diehl (2024 printing), [Model Predictive Control: Theory, Computation, and Design](https://sites.engineering.ucsb.edu/~jbraw/mpc/MPC-book-2nd-edition-5th-printing.pdf), selected introductory and economic-control passages.

**P3.** Nau et al. (2003), [SHOP2: An HTN Planning System](https://jair.org/index.php/jair/article/download/10362/24790).

**P4.** Browne et al. (2012), [A Survey of Monte Carlo Tree Search Methods](https://repository.essex.ac.uk/4117/1/MCTS-Survey.pdf).

**P5.** Silver & Veness (2010), [Monte-Carlo Planning in Large POMDPs](https://proceedings.neurips.cc/paper_files/paper/2010/file/edfbe1afcf9246bb0d40eb4d8027d90f-Paper.pdf).

**P6.** Koenig & Likhachev (2002), [Improved Fast Replanning for Robot Navigation in Unknown Terrain](https://www.cs.cmu.edu/~maxim/files/dlite_icra02.pdf).

**P7.** Hansen, [The CMA Evolution Strategy: A Tutorial](https://arxiv.org/abs/1604.00772), inspected v2 (2023).

**P8.** Gaina et al., [Rolling Horizon Evolutionary Algorithms for General Video Game Playing](https://arxiv.org/abs/2003.12331), journal DOI [10.1109/TG.2021.3060282](https://doi.org/10.1109/TG.2021.3060282).

**I1.** Freeciv [ferry ownership/recovery](https://github.com/freeciv/freeciv/blob/0695957ae339ec1db15a98e65f8d981ecf16fa0f/ai/default/aiferry.c), with city production inspected at the same commit.

**I2.** Unciv [construction proposals](https://github.com/yairm210/Unciv/blob/8e03dc2667234d2388abefd69ccaa1710893600e/core/src/com/unciv/logic/automation/city/ConstructionAutomation.kt) and worker automation at the same commit. It provides a useful proposal/commit comparison, but still contains heuristic scoring and explicit TODOs; it is not treated as an optimal opponent.

**I3.** OpenRA [squad ownership and scheduled updates](https://github.com/OpenRA/OpenRA/blob/e180e3225f3930272dd451917467631618f8976f/OpenRA.Mods.Common/Traits/BotModules/SquadManagerBotModule.cs). Borrow the separation and budget discipline, not its tick semantics or gameplay rules.

**I4.** Cicero/Diplodocus [belief-conditioned strategic search](https://github.com/facebookresearch/diplomacy_cicero/blob/e85afeddb34f5b7c1ea0827203b425a0f7e68ead/fairdiplomacy/agents/bqre1p_agent.py) and repository documentation. This pass inspected code/documentation, not a trained model or reproduction of its reported playing strength.
