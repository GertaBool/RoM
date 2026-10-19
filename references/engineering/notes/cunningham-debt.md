# Ward Cunningham, The WyCash Portfolio Management System (OOPSLA '92, Experience Report, 1992)
Source: lit3/cunningham-debt/doc.txt. Read: lines 1-76 (all).

## What it says
- Experience report, opening paragraph: "WyCASH+ is a portfolio management system which provides basic accounting, record-keeping and reporting, as well as analytical computations" -- the system reported on manages cash-securities portfolios; the domain has "new security types are frequently introduced into the market".
- Experience report, choice of objects: "Wyatt Software chose to employ object technology in order to quickly and effectively address the diversity present in the market." -- the stated reason for the technology is diversity and change in the domain.
- Experience report, first benefit: "many security types fit nicely into an inheritance hierarchy which is directly supported by our language (Smalltalk) saving us considerable effort in coding."
- Experience report, second benefit: "changing market demands often require massive revisions which we have been able to accomodate because of the modularity intrinsic in a totally object-oriented implementation."
- Experience report, what customers value: "Our customers value our responsiveness as much as, if not more than, our product's fit to their current needs."
- Experience report, process: "We developed the product by incremental growth from a working prototype."
- Experience report, team knowledge: "Each member of our small engineering team maintains at least general knowledge of all aspects of the roughly four megabytes of source code." -- the code base includes vendor libraries and code written by third-party contractors to the team's specification.
- Experience report, consolidation: "Mature sections of the program have been revised or rewritten many times providing the consolidation that is key to understanding and continued incremental development" -- repeated revision is presented as the source of understanding.
- Experience report, claim for the process: "We believe this process leads to the most appropriate product in the shortest possible time." -- stated as belief, followed by the pitfalls.
- Experience report, first pitfall: "Not everyone is comfortable with sudden changes in direction, especially programmers." -- remedy given: "the best antidote is more complete familiarity with the product and its implementation."
- Experience report, acceptance of change: "Changes will be accepted when they are recognized as do-able."
- Experience report, second pitfall: "Another, more serious pitfall is the failure to consolidate."
- Experience report, effect of immature code: "excess quantities will make a program unmasterable, leading to extreme specialization of programmers and finally an inflexible product." -- immature code may still work and satisfy the customer.
- Experience report, the debt metaphor: "Shipping first time code is like going into debt."
- Experience report, condition for debt to help: "A little debt speeds development so long as it is paid back promptly with a rewrite." -- repayment is a rewrite, done promptly.
- Experience report, role of objects: "Objects make the cost of this transaction tolerable."
- Experience report, the danger: "The danger occurs when the debt is not repaid."
- Experience report, interest: "Every minute spent on not-quite-right code counts as interest on that debt."
- Experience report, scale of the danger: "Entire engineering organizations can be brought to a stand-still under the debt load of an unconsolidated implementation, object- oriented or otherwise." -- the danger is stated as independent of object orientation.
- Experience report, waterfall: "The traditional waterfall development cycle has endeavored to avoid programming catastrophy by working out a program in detail before programming begins."
- Experience report, waterfall in the debt analogy: "we recognize this amounts to preserving the concept of payment up-front and in-full."
- Experience report, conclusion: "The modularity offered by objects and the practice of consolidation make the alternative, incremental growth, both feasible and desirable (but not always comfortable)" -- the claim is scoped to the competitive financial software market.
- Addendum: "Comments include a history of the metaphor, its position as a defense of refactoring" -- a later 2009 video by the author is mentioned; it is not part of this text and was not read.

## Readings for our work
- Treat every quick tool, check or patch written to get a result as debt with a named repayment: a follow-up consolidation (rewrite or deletion) recorded before the next feature of the same kind. Check: for each tool added in a period, there is a later commit that consolidates or removes it; count tools never revisited. Rests on: debt metaphor, condition for debt to help, the danger. Would not apply if: the tool is used once and deleted, so no minutes are spent on it later.
- The repository's growth of tools and checks without consolidation matches the stated mechanism (unmasterable code, specialization, inflexibility). Before adding a check or script, ask whether an existing one can be revised to cover it; prefer revising. Check: the number of files in method/ and their line count should not grow faster than the analysis documents they serve. Rests on: second pitfall, effect of immature code, scale of the danger. Would not apply if: the added tools are each small, independent and fully understood by the one maintainer.
- Incremental growth is justified here only together with consolidation; the paper does not recommend incremental growth alone. When a document or tool is revised, it should be rewritten into a consolidated form, not patched with additions (this agrees with the repository's fresh-start rule). Rests on: consolidation, conclusion. Would not apply if: the change is a genuine correction of a single fact.
- Keeping general knowledge of the whole code base is the author's stated condition for accepting sudden changes. For the large legacy C++ DLL, where whole-code familiarity is not possible, changes should be kept small and local so that they remain recognisably do-able. Rests on: team knowledge, acceptance of change, first pitfall. Would not apply if: the parts of the DLL we change are already fully understood and documented.
- Interest is measured as time spent working around not-quite-right code. A concrete check: log time or commits spent fixing or working around our own earlier tools (for example check failures caused by the checks themselves); a rising share signals unpaid debt. Rests on: interest. Would not apply if: such work is negligible compared with work on the product.
