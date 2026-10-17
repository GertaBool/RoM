# Mission, plan and working method for RoM's war AI

## 1. Mission

Make Rise of Mankind's AI opponents competent enough to beat an expert human at a fair
difficulty (Noble: the AI gets no bonuses), while each leader keeps making plausible,
personality-driven decisions. The work also shows how much the AI needs: every weakness is
found, explained and fixed. War and the economy are both in scope. Ship this as reliable,
documented changes to the RoM DLL on GitLab `main`.

## 2. Goals and how each is judged

| # | Goal | Judged by |
|---|---|---|
| G1 | **No regressions**: no crash, no desync, saves stay compatible | Build with 0 errors and 0 warnings; regression suite; one deterministic game per change; replay identity where behaviour should not change |
| G2 | **Decision quality**: each war decision does what the game's rules make correct | A written rule chain per decision (data → mechanics → correct decision), and a unit test that the code follows it |
| G3 | **Character**: leader personality chooses between sound options | Personality inputs are kept, and named in each design note |
| G4 | **Turn time** no worse | Turn time of the deterministic game |
| G5 | **Traceability**: every change has its facts, rule, tests and provenance | Design note, patch, manifest, DLL provenance |

| G6 | **Closing the gap with the expert** | Measured in the user's logged games: hopeless attacks, cities defended against armies they can see, research compared with the human's |

**The benchmark is the user's games.** Each logged game is checked decision by decision
against the engine's own mathematics. Self-play hides weaknesses that both sides share, so
headless AI games check only safety, side effects and turn time. Self-play outcomes such as
"wins more wars" are not goals. Every civilization runs the same AI.

**Constraints.**
- GitLab through the connector: source only, few commits, ASCII.
- The DLL and documentation go to GitHub.
- MSVC 2003 under Wine.
- Each design is approved by the user before it is built.
- The token budget is limited.
- No model identifiers in any artifact.

## 3. Plan

| Phase | Output | Gate |
|---|---|---|
| P0 Knowledge | The rules of the game: [xml-knowledge.md](xml-knowledge.md), [xml-defines.md](xml-defines.md), [xml-war-tables.md](xml-war-tables.md), [strategy.md](strategy.md) | Done; maintained as facts change |
| P1 Diagnosis | For each decision area: what the AI does today (code path) against what the rules make correct, giving a ranked gap list | The user reviews the gap list |
| P2 Design | Per gap, one short note: facts → rule → decision → code location → personality inputs → tests → risk | The user approves the note |
| P3 Build | The smallest change that closes the gap: rule fixes unconditional, behaviour changes behind a switch until verified | Suite passes, 0 warnings |
| P4 Verify | Unit test of the decision; build; one deterministic game; a scenario only where the rule cannot be unit-tested | All pass |
| P5 Ship | GitLab MR; GitHub DLL, patch, manifest, docs | Diff on GitLab equals the tested tree |

**Decision areas,** in proposed order. The ranking is by effect on play against an expert ×
confidence in the rule ÷ cost.

1. **Siege:** sizing by the bombard arithmetic, no pauses, assault when the walls are down,
   the stop rule.
2. **Defence:** interior-line reserve, striking parked stacks, city ranged strikes.
3. **War timing and preparation:** tech windows, upgrades, XP buildings, civics before
   declaring.
4. **Campaign rhythm:** base on captured cities, heal, continue; target distance counted in
   enemy tiles.
5. **Formations:** combined-arms composition, escorts, homogeneous enemy-road stacks.
6. **Resource denial and raids.**
7. **IDW as a war aim.**

The order is re-ranked when diagnosis finds new facts. The reason for any change is
recorded.

## 4. Working method (each step)

1. **Question.** State the decision or fact needed and what answer would change the next
   action.
2. **Chain of requisites.** List the layers it depends on: XML field → DLL code that reads it
   → Python overrides → defines → AI code that uses it.
3. **Resolve each link with a narrow query,** against the single source for its layer:
   - XML: `tools/xmlread.py`'s resolved records;
   - defines: [xml-defines.md](xml-defines.md);
   - code: the DLL and Python source, by grep or a bounded read.
4. **Describe the facts** in a few lines before any inference.
5. **Infer.** Mark assumptions, and name what would falsify each one.
6. **Act** with the smallest change that answers the question.
7. **Verify** in proportion to the risk: one check that can change the decision, not a
   campaign.
8. **Record and checkpoint.** Facts go to the knowledge files, the decision to the design
   note, then a commit.

## 5. Fault tolerance

- **Single sources of truth.** The tools are in the repository and the database is
  regenerated from the XML, so no fact depends on memory of an earlier conversation.
- **Assumption log.** Every unverified assumption is written as one, and every output
  states which facts were checked.
- **Checkpoints.** Each finished unit of work is committed, so a context reset or a lost
  container costs at most one unit.
- **Gates.** A failed gate stops the phase. A change is rolled back by reverting its
  commit. Behaviour changes stay switchable until verified.
- **Re-planning trigger.** A step that takes twice its estimate, or a fact that contradicts
  the plan, stops work for a re-plan before going on.
- **Corrections from the user** are traced to the step of the method that failed, and the
  method is fixed, not only the output.

## 6. Efficiency

- Read only what a question needs. Full reads only where understanding the whole is the
  goal, as with the defines.
- Reuse the tools. Scripts live in files, not in one-off command lines.
- Run independent queries in parallel.
- No background agents unless the work is independent, parallel and agreed.
- Before any test, state what result would change the next step; otherwise skip it.
  Usually one headless game is enough.
- Use the simplest means that is enough, usually the mathematics the game already has.
- Read the user's intent, not only their words.
- Report facts, decision and next step, briefly.
