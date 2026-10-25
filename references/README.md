# References

The outside sources read so far, where each came from, and the notes taken from it. The notes
are the reading notes as written while reading, with quotations and section numbers.

- `notes-strategy.md`: round 1, strategy and method of research (for the AI work).
- `notes-checks.md`: round 2, how checks and procedures fail and how to design ones that work
  (for the workflow).
- `engineering/`: round 3, version control, code bases, refactoring, engineering practice and data
  engineering: 39 sources, notes with checked quotations, and where the sources agree
  (`engineering/README.md`).

The files themselves are not in the repository. In the session they were kept under
`lit/` and `lit2/` of the scratchpad.

## Round 1: strategy and research method

| Source | Edition or address | What the notes cover |
|---|---|---|
| Clausewitz, *On War* | Graham tr., Project Gutenberg eBook #1946 | I.1, I.2, II.5, III.8–18, VI.1–5, VII.4–5, VII.22, VIII.4 |
| Sun Tzu, *The Art of War* | Giles tr., Project Gutenberg eBook #132 | I–IV, VI, VIII, IX, XI–XIII |
| Jomini, *The Art of War* | Mendell & Craighill tr., Project Gutenberg eBook #13549 | Art. IV, X, XII, XL, ch. III |
| Lanchester, *Aircraft in Warfare* (1916) | Internet Archive scan | ch. V–VI, §19–41 |
| Corbett, *Some Principles of Maritime Strategy* (1911) | Project Gutenberg eBook #15076 | I.4, I.6, II.1, III.3 |
| Mahan, *The Influence of Sea Power upon History* (1890) | Project Gutenberg eBook #13529 | introductory chapter |
| Smith, *The Wealth of Nations* (1776) | Project Gutenberg eBook #3300 | II.3, V.1.1 |
| Sinha, Fang, An, Kiekintveld, Tambe, *Stackelberg Security Games: Looking Beyond a Decade of Success*, IJCAI-18 | andrew.cmu.edu/user/feif/Publications/2018_IJCAI_SSGsurvey.pdf | see notes |
| Branavan, Silver, Barzilay, *Learning to Win by Reading Manuals in a Monte-Carlo Framework*, JAIR 2012 | arXiv:1401.5390 | see notes |
| Lakatos, methodology of research programmes | Stanford Encyclopedia of Philosophy, entry "Imre Lakatos" | the entry only, not the book |

Downloaded but not read, no notes: Ashby, *An Introduction to Cybernetics* (archive.org);
Ross, Gordon, Bagnell, *DAgger* (arXiv:1011.0686). Downloads that failed (an error page was
saved instead of the file): Boyd, *Patterns of Conflict*; Campbell, *Assessing the Impact of
Planned Social Change*; Hitch.

## Round 2: checks and procedures

| Source | Edition or address | What the notes cover |
|---|---|---|
| Holzmann, *The Power of Ten: Rules for Developing Safety-Critical Code*, IEEE Computer 2006 | cs.otago.ac.nz/cosc345/resources/nasa-10-rules.pdf | see notes |
| Degani & Wiener, *Human Factors of Flight-Deck Checklists: The Normal Checklist*, NASA CR-177549, 1990 | ntrs.nasa.gov, citation 19910017830 | see notes |
| Barshi, Mauro, Degani, Loukopoulou, *Designing Flightdeck Procedures*, NASA TM-2016-219421 | hsi.arc.nasa.gov (also ntrs.nasa.gov, citation 20160013263) | see notes |
| Leveson & Thomas, *STPA Handbook*, MIT 2018 | psas.scripts.mit.edu, STPA_handbook.pdf | the control loop, losses and hazards, ch. 6 on drift |
| Hauser, Ellsworth & Gonzalez, *Are Manipulation Checks Necessary?*, Frontiers in Psychology 2018 | doi 10.3389/fpsyg.2018.00998 | see notes |
| Nosek, Ebersole, DeHaven & Mellor, *The Preregistration Revolution*, PNAS 2018 | copy at errorstatistics.com | see notes |
| Shingo, poka-yoke | secondary sources only; the book was not obtained | control vs warning devices |

## What round 2 says about the checks in this repository

These are readings, not facts; each names the source it rests on.

- The rules for the work were written before round 2 was read. They were not derived from it.
  (My own admission, recorded here so it is not lost.)
- A check that cannot fail is worthless (Holzmann, rule 5). The `Method: <reason>` trailer is
  free text I write myself, so it never fails.
- A check that only warns does not stop the error (Shingo: warning vs control devices). The
  Claude Code hook on method changes only asks, and the ask did not stop me.
- Checks get skipped under pressure to finish, and answered without looking (Degani & Wiener).
  A check should report the actual state ("indicated fifteen"), not "done" (Barshi et al.).
- Safety rules should follow from the losses to avoid, not be bolted on (STPA). Drift happens as
  safeguards are relaxed one at a time for good-seeming reasons (STPA ch. 6).
- Test that the treatment works in a small pilot before the full experiment (Hauser et al.).
  Change B was run for thirty seeds before checking that the human-model seat ever became the
  hegemon; it rarely did.
- Fix the question and the analysis before seeing the outcome (Nosek et al.).

Candidate constraints drawn from these, not adopted:
1. A pilot before every campaign, checking that the change acts on what it is meant to.
2. The assumption the proxy rests on is checked in that pilot.
3. The two arms of an experiment differ in one setting only.
4. The checks cannot be changed from the session that is being checked: a refusal, not a warning.
5. An indicator of drift into work on the tools instead of the product.
6. Remove rules that can never fail.
