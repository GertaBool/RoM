# Settler overproduction and Rome without Writing at 410 BC

Two follow-up questions on the Masinissa Marathon autorun save (`Masinissa BC-0410`,
game turn 269, not published here): what is going on with the settler
overproduction, and why has Rome no Writing by then?

Short answers:

- **Settlers.** Over the whole game the AIs built about as many settlers as they
  used. The 18 settlers standing around at 410 BC were idle ones, stuck for the
  reasons patch 0012 fixed. With the current code they are disbanded or put to
  use, and no new ones are trained for sites nobody can reach.
- **Rome.** Rome adopted the Mercenaries civic on turn 144 and could not get out
  of the trap it made. Unit charges took 45 of its 96 commerce. The AI sat in
  financial trouble with the slider at 95 percent gold (3 beakers a turn), and
  trained no settler although a good site was open. Writing was available the
  whole time (Rome had Priesthood and Trade) but never affordable. Four defects
  kept it there. Patch 0013 fixes them
  ([fixes/0013-upkeep-traps.patch](../../fixes/0013-upkeep-traps.patch), landed on
  GitLab `main` as [!38](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/38),
  merge `93ae873`, tree `5b4dd668` = the tested tree; DLL in
  [builds/0013](../../builds/0013/CvGameCoreDLL.dll)).

## Method

The save was loaded into the real DLL in the
[headless harness](../../toolchain/harness/README.md). Two new harness options
made this possible:

- `HARNESS_HISTORY_DIAG=1` dumps what the save remembers about the past. That
  covers each player's per-turn score, economy, industry, agriculture, power
  and culture series from turn 0, the replay messages (city foundings, civic
  adoptions, wars, first techs) and the game's count of every unit type ever
  created. It also dumps the present: research progress and queue, the cost
  terms, every unit with role and experience, and the AI's value of every
  civic it may adopt.
- `HARNESS_RESEED=n` restarts the synchronized random sequence after loading,
  so one save gives several independent continuations.

One diagnostic copy of the source also logged `AI_civicValue` term by term.
Timings and outcomes are harness runs; the game executable was not run.

## Rome

From [runs/history-410bc.txt](runs/history-410bc.txt):

| Turn | Event |
|---|---|
| 0 | Rome founded |
| 106, 124 | Antium, Cumae (2nd and 3rd city) |
| 144 | adopts Mercenaries (and Pastoral) |
| 170 to 260 | military power 39 to 201, no war |
| 260 | Neapolis (4th city) |
| 261 | declares war on Pericles |

Rome's total commerce stayed between 16 and 37 for 260 turns. Over the same
span the other civilizations went from about 20 to between 53 and 364. Every
civilization founded its second city late (turns 89 to 158; a settler costs
the production value of a new city, about 270 hammers on Marathon). After
turn 150 the others expanded and Rome did not.

At 410 BC:

- **Rome:** 4 cities and 45 units (39 military), among them 14 scouts. Unit
  charges were 45 of total costs of 58, against 96 commerce. The slider stood
  at 95 percent gold and research made 3 beakers a turn. Masonry, the
  prerequisite of Fortification, was at 115 of 498.
- **Other Mercenaries civs:** the civilizations still on Mercenaries pay the
  highest unit charges. Willem pays 42 for 51 units, Ivan and Joao 29 each.
  Fortification civilizations pay much less with as many or more units:
  Ramesses 25 for 73, Brennus 18 for 56.
- **Adoption history:** ten civilizations adopted Mercenaries between turns 144
  and 209.

The capital's production log at turn 270 reads `finance 1 ... settlers 0/0 site 3777/1725`:
a site of value 3777 is open, the minimum is 1725, and the settler allowance is
zero because of the financial trouble.

### Why Rome could not get out

1. **The civic value preferred Mercenaries.** Traced term by term
   ([runs/civic-trace-rome-0012.txt](runs/civic-trace-rome-0012.txt)), current
   code before patch 0013:

   | Term | Tribal Warfare (default) | Mercenaries |
   |---|---|---|
   | base, anarchy, upkeep | 20 | 17 |
   | free experience | 0 | +45 |
   | unit charges | -28 | -91 |
   | happiness per military unit | 0 | +24 |
   | **total** | **-7** | **-4** |

   - **Free experience** was priced as `experience x population x 30%` (12% in
     peace) times the production multiplier. That made Mercenaries' five points
     worth 45 a turn, half of Rome's commerce. The civic's extra unit charges
     cost Rome 31 gold.
   - **Unit charges** were counted raw. The game multiplies them by the
     handicap's unit cost percent (50 on Noble) and, for AIs, the AI and per-era
     percents. The penalty was therefore twice the real gold on Noble (1.7
     times on Deity). Correcting it alone would make Mercenaries look better,
     which is why the experience term had to be fixed with it.
   - **Military happiness** assumed three units in every city. Rome's cities held
     one or two.
2. **Nothing could be disbanded.** In financial trouble the AI calls
   `AI_disbandUnit(1, ...)`, which only considers units with at most one
   experience point. Mercenaries gives five at birth, so no unit trained under
   it qualifies.
3. **Explorers never retired.** A surplus explorer was scrapped only once its
   search for something to explore failed, which on a large map never happens.
   Rome kept 14 scouts against a need of three; 74 scouts were created in the game.
4. **Financial trouble stops expansion.** With four or more cities the settler
   allowance is zero in financial trouble (BBAI rule, unchanged). Together with 1
   to 3 this made a stable trap: gold slider, no research, no new cities, no way
   to shed upkeep.

### Patch 0013

| Function | Change |
|---|---|
| `AI_civicValue` | Free experience is worth the promotions it buys (BTS thresholds: five points are two promotions) at 15 percent of a unit each, on the hammers going into military units (two fifths of production with a war plan, one fifth otherwise). For Rome: 10 instead of 45. |
| `AI_civicValue` | Unit charges are projected in real gold: handicap, AI and per-era percents, inflation. |
| `AI_civicValue` | Happiness per military unit uses the cities' actual garrisons. |
| `AI_disbandUnit` | The experience threshold counts from the experience a unit of that type would be trained with today. A veteran stays protected. |
| `AI_exploreMove` | A surplus explorer retires before it searches. |

With patch 0013 the military civic values at 410 BC become:

| Leader | Before | After |
|---|---|---|
| Rome | Mercenaries -4 > Tribal Warfare -7 | Tribal Warfare 7 > Mercenaries 5 |
| Ivan | Mercenaries 149 > Raiders 136 | Raiders 69 > Mercenaries 38 |
| Willem | Fortification 118 > Mercenaries 108 | Fortification 132 > Mercenaries 46 |
| Joao | Fortification 133 > Mercenaries 78 | Fortification 127 > Mercenaries 44 |

### Measured on the save

Six 40-turn continuations per build, all seats on AI
([runs/seeds-40-turns.txt](runs/seeds-40-turns.txt)), mean ± standard deviation:

| | Patch 0012 | Patch 0013 |
|---|---|---|
| Research, all civilizations | 95 281 ± 6 251 | 95 818 ± 3 383 |
| Technologies gained | 119.5 ± 7.5 | 130.8 ± 11.1 |
| Cities at the end | 148.0 ± 4.0 | 151.7 ± 2.3 |
| Player-turns in financial trouble | 22.8 ± 3.7 | 16.2 ± 2.1 |
| Scouts at the end | 51.8 | 28.2 |
| Rome: turns in financial trouble | 6.3 | 3.0 |
| Rome: unit charges at the end | 22.3 | 12.5 |

Financial trouble falls by 29 percent and surplus scouts by half. Research and
cities do not change measurably over 40 turns. Rome gets Writing in every run of
both builds. That is partly patch 0012's work (the gold-target fix) and partly
because Rome loses its army attacking Tiryns around turn 272, which ends its
financial trouble by accident. The Mercenaries trap matters most earlier in a
game, before Masonry makes Fortification available. That is where the valuation
trace above shows the effect.

### Tried and not adopted

`AI_doCivics` weighs a switch over a horizon of twice `AI_CIVIC_CHANGE_DELAY`
(24) turns at every speed, while Marathon doubles anarchy. A change worth making
on Normal is therefore refused on Marathon; for example, Joao keeps a package
26 percent worse than his best. Scaling the horizon with the speed's anarchy
percent is the speed-invariant rule. In the same six runs it raised anarchy from
33.5 to 45.5 player-turns and showed no gain within 40 turns (late research
-3 percent, inside the noise). Switching pays later than that window shows, so
this needs a longer study and was left out.

## Settlers

From the whole-game counters: 141 settlers were created (18 of them at the
start) and 122 cities were founded. 18 settlers were alive at 410 BC, so about
one settler was lost. **The AIs did not build more settlers than they used.** About
one in eight stood idle at 410 BC:

- **Ivan:** 4 settlers for one site behind foreign borders.
- **Brennus:** settlers without escort.
- **Joao:** a galley waiting at sea for 64 turns.
- **Willem:** settlers in a threatened border city.

Patch 0012 addressed these
([research/autorun-masinissa](../autorun-masinissa/README.md)): sites count only if
a settler can be delivered there, settlers without a deliverable site retire,
lone settlers recruit an escort, and a transport without escort returns to port.

Same save, same seed, 30 turns ([runs/settlers-30-turns.txt](runs/settlers-30-turns.txt)):

| | Patch 0011 + hang guard | Patch 0012 |
|---|---|---|
| Settlers trained | 27 | 32 |
| Net new cities | 20 | 26 |
| Disbanded (no deliverable site) | 0 | 5 |
| Waiting at the end | 21 | 17, mostly younger than 17 turns |
| Ivan | 3 of 4 still stuck | all 4 disbanded, none trained |
| Willem | 3 more trained, 4 waiting | none trained, 2 waiting |

The settler cost is set in the DLL, not the XML (`iCost` 0): it is
`getNewCityProductionValue`, the free buildings plus the advanced-start city cost
and the growth thresholds of the first population, about 270 hammers on Marathon.
The remaining waste is Willem's two settlers in a border city that is under threat
every turn. They wait there by design, and the settler AI has no rule yet to move
them to a safer city.

## Validation

- **Regression suite:** 28 of 28 programs pass
  ([fixes/upkeep-traps-regression.log](../../fixes/upkeep-traps-regression.log)).
  The new `Tools/test_upkeep_traps.py` checks the civic terms with Rome's
  numbers, `AI_disbandUnit` compiled with stand-ins, and the order of the
  explorer check. All four cases fail against the previous source
  ([fixes/upkeep-traps-before.log](../../fixes/upkeep-traps-before.log)).
- **Patch application:** applying the patch to a clean `3553b8c` (GitLab
  `main` `abf8471`) reproduces the tested tree
  ([fixes/upkeep-traps-patch-validation.log](../../fixes/upkeep-traps-patch-validation.log)).
- **Clang gate:** no new diagnostics
  ([fixes/upkeep-traps-clang-gate.log](../../fixes/upkeep-traps-clang-gate.log)).
- **MSVC 2003 release build:** 0 errors, 0 warnings, the same 2451 exports
  ([builds/0013/provenance.json](../../builds/0013/provenance.json)).
- **Save format:** unchanged.

Scripts: [tools/](tools/) (`settlebal.py` settler balance from a logging run,
`seedcmp.py` multi-seed comparison, `seedrun.sh` one reseeded continuation).
