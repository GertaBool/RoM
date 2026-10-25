# Reading notes: deterministic checks against degeneration (working file)

## Holzmann, The Power of Ten (IEEE Computer 2006; JPL)
- Long guidelines "tend to have little effect on what developers actually do"; "the most dooming aspect ... they rarely allow for comprehensive tool-based compliance checks".
- "To be effective ... the set of rules has to be small ... specific enough that they can be checked mechanically" (no more than ten).
- Rule 5: a check that can never fail violates the rule ("not possible to satisfy the rule by adding unhelpful assert(true)").
- Rule 10: zero warnings; if the checker is confused, rewrite the code so it becomes trivially valid; do not argue the warning away.

## Degani & Wiener, Human Factors of Flight-Deck Checklists (NASA CR-177549, 1990)
- Checklists are misused because they are routine and redundant, which makes them "appear 'safe' to misuse", and are "mandated ... however, no provisions for on-site enforcement are visible".
- Observed failures: done from memory; challenge answered "immediately ... not verifying that the item called was set accordingly"; several items "chunked"; no indication of completion.
- Under production pressure checklists are "relegated to second place status in order to save time".
- Guidelines: responses "should portray the desired status or the value of the item ... (not just 'checked' or 'set')"; most critical items first; no compromise on "killer" items; avoid tight coupling, keep buffers for recovery.
- Latent failures ("resident pathogens", Reason): the checklist itself can contain them.

## Barshi, Mauro, Degani, Loukopoulou, Designing Flightdeck Procedures (NASA TM-2016-219421)
- Response phrased as the actual system state: "position fifteen, indicated fifteen" confirms "the intended effect has also occurred"; generic "set", "checked" do not.
- Working memory holds reliably ~3 propositions; prospective memory (deferred intentions) is "particularly vulnerable"; checklists should catch deferred critical items.
- Length: "as long as it needs to be, and as short as possible"; long checklists get cut down to perceived killer items.
- Evaluation: "procedures must be given a chance to fail"; evaluation is not optional.

## Leveson & Thomas, STPA Handbook (MIT 2018)
- Control loop: controller acts on its process model (beliefs); unsafe control actions arise from inadequate process models: incorrect feedback, feedback ignored, feedback missing or delayed, or feedback that does not exist.
- "One common control algorithm flaw occurs when the control algorithm assumes that previous control actions have been executed properly ... especially relevant when there is no feedback."
- Bolt-on safety late in development is costly and less effective; constraints should follow from defined losses and hazards.
- Ch. 6: accidents come from "the migration of an organization to a state of increasing risk over time as safeguards and controls are relaxed due to conflicting goals and tradeoffs and reduced perceptions of risk". Assumption-based leading indicators: monitor the specific assumptions a design rests on, and have a process that acts when one breaks.

## Hauser, Ellsworth & Gonzalez, Are Manipulation Checks Necessary? (Front. Psychol. 2018)
- Check that the treatment produces the intended state in a pilot, "before actually running the experiment ... whose whole purpose is to find out whether the treatment successfully produces the intended" state, on people like the real sample, shortly before; "better to find out that your treatments are ineffective ... before running the whole experiment".

## Nosek, Ebersole, DeHaven & Mellor, The Preregistration Revolution (PNAS 2018)
- Prediction vs postdiction; hindsight bias makes the mistake hard to avoid; the remedy is defining questions and analysis before observing outcomes; deviations reported transparently.

## Shingo, poka-yoke (secondary sources only; the book was not obtained)
- Control devices stop the process; warning devices only signal. Source inspection: catch the error where it is made.
