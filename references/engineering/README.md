# References, round 3: version control, code bases, refactoring, engineering practice, data

Reading notes on 39 sources, one file per source in `notes/` (Pro Git in two files). Each file has two
parts:
- **What it says.** The author's claims, in the order of the text, each with an exact quotation and its
  page (PDFs) or section heading (HTML and plain text).
- **Readings for our work.** Inferences, kept apart. Each names the points it rests on and what would
  make it not apply. They are proposals, not adopted rules.

The notes were written by eight reader sessions working in parallel from a shared brief. Each reader
read its texts in full. Every quotation was then checked by `tools/check_quotes.py` against the
source text, including the page where a page is given: 3435 quotations in 40 files, none missing.
The checker compares words and their order, ignoring case, punctuation, whitespace and hyphenation.
It checks that each quotation is in the source. It does not check that the note reads the quotation
correctly; the notes of Parnas 1972 and Cunningham 1992 were read against the papers by hand.

To rebuild the texts and re-run the check: `tools/build.sh <empty work dir>`. The URLs are in
`tools/sources.tsv`. The texts are not in the repository: the books, papers and pages belong to their
authors and publishers.

Not obtained, because their hosts do not resolve from the session (`tools/not-obtained.tsv`):
- Herzig & Zeller, *The Impact of Tangled Code Changes* (MSR 2013).
- Potvin & Levenberg, *Why Google Stores Billions of Lines of Code in a Single Repository* (CACM 2016).
- Opdyke, *Refactoring Object-Oriented Frameworks* (PhD thesis, 1992).

## Sources

**Git and version control**
- `progit-1`, `progit-2`: Chacon & Straub, *Pro Git*, 2nd ed., ch. 1–3, 5, 7 (parts), 8.3–8.4, 10.
- `gitworkflows`: the Git project, gitworkflows(7).
- `git-submitting`: the Git project, *SubmittingPatches*.
- `linux-submitting`: the Linux kernel, *Submitting patches*.
- `git-bisect-lk2009`: Couder, *Fighting regressions with git bisect* (2009).
- `swe-ch16-vcs`: Winters, *Version Control and Branch Management* (Software Engineering at Google, ch. 16).
- `zeller-dd`: Zeller & Hildebrandt, *Simplifying and Isolating Failure-Inducing Input* (IEEE TSE 2002).

**Code bases and how they age**
- `parnas-criteria`: Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules* (CACM 1972).
- `parnas-aging`: Parnas, *Software Aging* (ICSE 1994).
- `conway`: Conway, *How Do Committees Invent?* (Datamation 1968).
- `brooks-nsb`: Brooks, *No Silver Bullet* (1986).
- `lehman-laws`: Lehman, *Programs, Life Cycles, and Laws of Software Evolution* (Proc. IEEE 1980).
- `dijkstra-ewd340`: Dijkstra, *The Humble Programmer* (1972).
- `dijkstra-ewd215`: Dijkstra, *A Case against the GO TO Statement* (EWD215).
- `hoare-clothes`: Hoare, *The Emperor's Old Clothes* (Turing lecture 1980).
- `cunningham-debt`: Cunningham, *The WyCash Portfolio Management System* (OOPSLA 1992).

**Refactoring and large changes**
- `murphyhill-refactor`: Murphy-Hill, Parnin & Black, *How We Refactor, and How We Know It* (ICSE 2009).
- `kim-refactor`: Kim, Zimmermann & Nagappan, *A Field Study of Refactoring Challenges and Benefits* (FSE 2012).
- `swe-ch22-lsc`: Wright, *Large-Scale Changes* (SWE at Google, ch. 22).
- `swe-ch15-deprecation`: Wright, *Deprecation* (ch. 15).
- `swe-ch21-deps`: Winters, *Dependency Management* (ch. 21).
- `nagappan-churn`: Nagappan & Ball, *Use of Relative Code Churn Measures to Predict System Defect Density* (ICSE 2005).

**Engineering practice**
- `swe-ch01-what`: Winters, *What Is Software Engineering?* (ch. 1).
- `swe-ch09-review`: Manshreck & Sadowski, *Code Review* (ch. 9).
- `swe-ch11-testing`: Bender, *Testing Overview* (ch. 11).
- `bacchelli-review`: Bacchelli & Bird, *Expectations, Outcomes, and Challenges of Modern Code Review* (ICSE 2013).
- `fowler-ci`: Fowler, *Continuous Integration* (revised 2024).
- `basili-gqm`: Basili, Caldiera & Rombach, *The Goal Question Metric Approach*.

**Data**
- `codd-relational`: Codd, *A Relational Model of Data for Large Shared Data Banks* (CACM 1970).
- `stonebraker-wgaw`: Stonebraker & Hellerstein, *What Goes Around Comes Around* (2005).
- `wickham-tidy`: Wickham, *Tidy Data* (JSS 2014).
- `buneman-provenance`: Buneman, Khanna & Tan, *Why and Where: A Characterization of Data Provenance* (ICDT 2001).
- `bhattacherjee-versioning`: Bhattacherjee et al., *Principles of Dataset Versioning* (2015).
- `sculley-debt`: Sculley et al., *Hidden Technical Debt in Machine Learning Systems* (NIPS 2015).
- `breck-validation`: Breck et al., *Data Validation for Machine Learning* (SysML 2019).
- `gebru-datasheets`: Gebru et al., *Datasheets for Datasets* (2021 version).
- `wilson-best`: Wilson et al., *Best Practices for Scientific Computing* (PLOS Biology 2014).
- `wilson-goodenough`: Wilson et al., *Good Enough Practices in Scientific Computing* (PLOS CB 2017).
- `sandve-rules`: Sandve et al., *Ten Simple Rules for Reproducible Computational Research* (PLOS CB 2013).

## Where the sources agree

Readings, not facts. Each line names the notes it rests on; the quotations and pages are there.

1. **One concern per change, and each change works on its own.** Each commit is one logical change
   that builds and passes the checks by itself, so it can be reviewed, reverted and bisected.
   Mixing concerns is the normal case unless something enforces it: in Murphy-Hill's data, most
   refactoring happened inside commits that also changed behaviour.
   (progit-1, gitworkflows, git-submitting, linux-submitting, git-bisect-lk2009, swe-ch09-review,
   wilson-best, wilson-goodenough, murphyhill-refactor)
2. **Whitespace and line-ending changes are a concern of their own, and they can be detected.** A
   line-ending rewrite shows as every line removed and re-added. It also inflates churn to the size
   of the file. Formatting runs as a separate pass. Check with `git diff --check` and by comparing
   the diff with and without whitespace before a patch leaves.
   (progit-2, progit-1, git-submitting, linux-submitting, murphyhill-refactor, swe-ch22-lsc,
   nagappan-churn)
3. **A check binds only where the author cannot skip it.** Local hooks are skipped with
   `--no-verify` and are not cloned. Enforcement belongs on the server or in CI, run in a clean
   reference environment, over every commit pushed.
   (progit-2, progit-1, fowler-ci, swe-ch16-vcs, swe-ch09-review)
4. **Checks must be few, actionable, fast and tested.** Plant a fault and see the check fail. Record
   how often each check fires and how often a firing leads to a fix. Remove checks that fire
   falsely; people learn to bypass those. A checker guides judgement and does not replace it.
   (fowler-ci, swe-ch11-testing, breck-validation, swe-ch15-deprecation, swe-ch22-lsc,
   linux-submitting, basili-gqm)
5. **The checker should not be the author.** Review comes from someone other than the author. A
   check written and approved by the same hand is not a review; with one author, say so. Review
   finds few defects: mostly small improvements, and shallow ones from a reviewer who does not know
   the code. Correctness has to come from tests and the figure system, not from review.
   (swe-ch09-review, bacchelli-review, git-submitting, parnas-aging, conway, wilson-best, swe-ch16-vcs)
6. **Tools and checks are liabilities. Growth without consolidation is debt.** Code delivers function
   at a cost. Glue around the product dominates mature systems (Sculley: a mature system "might end up being (at most) 5% machine learning code and (at least) 95% glue code"). Each
   new construct must state what it buys over what exists. Additions must be matched by
   consolidation; delete what nothing needs.
   (cunningham-debt, sculley-debt, swe-ch15-deprecation, hoare-clothes, parnas-aging, lehman-laws,
   stonebraker-wgaw, brooks-nsb, swe-ch01-what, kim-refactor, swe-ch09-review)
7. **Questions before measurement.** Goal, then questions, then metrics; measurement from the bottom
   up does not work. Fix how the data will be read before the data come in. The essential work is
   deciding what to build; tooling attacks only the accidental part.
   (basili-gqm, brooks-nsb, gebru-datasheets)
8. **Determinism first, then search.** A seeded run that differs on re-run is a flaky test: fix the
   cause, don't re-run. Bisect and delta debugging need a test with a fixed outcome, and a time bound
   that counts as unresolved. Record the seed, build and tool versions with every result, and the
   toolchain as a dependency.
   (swe-ch11-testing, git-bisect-lk2009, zeller-dd, progit-2, sandve-rules, wilson-best, swe-ch21-deps)
9. **Raw data is read-only, every later stage is a script, and generated files are never edited.**
   Store raw logs and saves in full, and derived tables as recipes. Regenerate outputs and compare
   them with the committed copy; review the generator, not the output.
   (wilson-goodenough, wilson-best, sandve-rules, bhattacherjee-versioning, parnas-criteria,
   swe-ch09-review, fowler-ci)
10. **Tables have schemas, keys and provenance.** Name columns, never positions or row order. Declare
    a key and refuse duplicates on it. Keep one row per observation and one column per variable. The
    loader rejects records outside the schema. Check data validity separately from the outcome.
    Each figure points to the exact source record, down to the raw logs.
    (codd-relational, wickham-tidy, stonebraker-wgaw, breck-validation, buneman-provenance,
    gebru-datasheets, sculley-debt)
11. **The upstream DLL is a dependency, and patches to it are messages to another group.**
    - Pin the base commit of each patch.
    - Use one topic branch per merge request, cut from fresh upstream.
    - Deliver with `format-patch` or a branch, never as pasted text.
    - Name the base tree.
    - Put the numbers, and the downsides, in the description.
    - Deliver only what we will support.

    (swe-ch21-deps, gitworkflows, git-submitting, linux-submitting, progit-1, conway, swe-ch16-vcs)
12. **Changing legacy code needs a regression net and evidence, not a label.**
    - Before restructuring, have fixed-seed comparisons against the unpatched build.
    - Show that behaviour is unchanged; calling a change "refactoring" proves nothing.
    - Follow the design rules of the surrounding code.
    - Generate large changes by script, and split them into shards that can be merged on their own.

    (kim-refactor, murphyhill-refactor, swe-ch22-lsc, parnas-aging, wilson-best, swe-ch11-testing)
13. **Published history is final.** Rewrite only what has not been pushed. An append-only record can
    be verified from the git history itself.
    (progit-1, progit-2)

## Limits of this set

- Much of it is practitioner guidance whose evidence is experience at large organisations or in
  large open-source projects. That covers Google's chapters, the git and kernel rules, and Fowler,
  and some of them say so themselves. For a repository with one person and one AI, take the
  principles, not the scale arguments.
- The empirical studies are few: Murphy-Hill, Kim, Bacchelli, Nagappan, and the Lehman data. The one
  on tangled commits was not obtained.
- Several readings in the notes describe this repository from memory of the session that wrote the
  brief (for example the gate, the register and the folders). They must be checked against the
  repository before acting on them.
