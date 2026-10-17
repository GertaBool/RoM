# Working rules for this repository

The mission is in `research/ai-warfare/mission.md`. The method for analysing a game, and for
every AI change built from one, is in `research/ai-warfare/data-protocol.md`. Read both before
starting.

Hard rules (details in the protocol):
1. **Questions first,** each with its source. Build a tool only when no source answers a
   question. Do not rebuild the DLL for an analysis.
2. **Setup first:** scenario, options, players, starts. Then the whole game. Then the human.
3. **Describe before inferring.** No reasons in descriptions. Readings come separately, with
   the facts they rest on and what would contradict them.
4. **Effects from the XML records only,** looked up at the time of writing. Never from
   memory, notes or a context summary.
5. **Turns:** every figure carries its turn. Never use the save's state for an earlier turn.
6. **Fresh starts:** when told to start over, replace the old text; do not patch it.
7. **Work through to the end without mid-way questions.** Mark unknowns *open*. Deliver once.
