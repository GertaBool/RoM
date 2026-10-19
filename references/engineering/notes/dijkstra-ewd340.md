# Edsger W. Dijkstra, The Humble Programmer (EWD340, ACM Turing Lecture 1972)
Source: lit3/dijkstra-ewd340/doc.txt. Read: lines 1-447 (all). The text has no section headings; bullets give the single heading The Humble Programmer and the topic of the passage.

## What it says
- The Humble Programmer, early years: "Where was the sound body of knowledge that could support it as an intellectually respectable discipline?" -- the author's question in the 1950s before choosing programming.
- The Humble Programmer, early years: "we must be very careful when we give advice to younger people; sometimes they follow it!"
- The Humble Programmer, early machines: "The overwhelming problem was to get and keep the machine in working order."
- The Humble Programmer, early machines: "his work derived all its significance from the existence of that wonderful machine." -- programs had only local significance and little lasting value.
- The Humble Programmer, early machines: "many a clever programmer derived an immense intellectual satisfaction from the cunning tricks by means of which he contrived to squeeze the impossible into the constraints of his equipment."
- The Humble Programmer, two opinions: "a really competent programmer should be puzzle-minded and very fond of clever tricks" -- the other opinion was that programming was nothing more than optimizing efficiency.
- The Humble Programmer, the software crisis: "But instead of finding ourselves in the state of eternal bliss of all programming problems solved, we found ourselves up to our necks in the software crisis!" -- after machines became several orders of magnitude more powerful.
- The Humble Programmer, minor cause: "we have got the I/O interrupts, occurring at unpredictable and irreproducible moments" -- and multi-level stores.
- The Humble Programmer, major cause: "the major cause is... that the machines have become several orders of magnitude more powerful!" -- society's ambition grew in proportion.
- The Humble Programmer, major cause: "it has only created them, it has created the problem of using its products."
- The Humble Programmer, third generation: "little will prevent you from ending up with a design in which the major part of your performance goal is reached by internal housekeeping activities of doubtful necessity." -- when performance is defined as the duty cycle of components.
- The Humble Programmer, third generation: "They silence their doubts by observing how many of these machines have been sold" -- compared to arguing that smoking must be healthy because so many people do it.
- The Humble Programmer, reviews of machines: "This suppression was an act of cowardice on my side for which I blame myself more and more." -- he did not submit a written review of a computer for fear of the difficulties.
- The Humble Programmer, reviews of machines: "The difficulties I foresaw were a consequence of the absence of generally accepted criteria" -- he wishes such reviews appeared as a sign of maturity.
- The Humble Programmer, influence of tools: "one of the most important aspects of any computing tool is its influence on the thinking habits of those that try to use it"
- The Humble Programmer, EDSAC: "We should recognise the closed subroutines as one of the greatest software inventions" -- it caters for one of the basic patterns of abstraction.
- The Humble Programmer, FORTRAN: "as a vehicle of thought it is no longer adequate: it wastes our brainpower, is too risky and therefore too expensive to use."
- The Humble Programmer, FORTRAN: "I pray daily that more of my fellow-programmers may find the means of freeing themselves from the curse of compatibility."
- The Humble Programmer, LISP: "it has assisted a number of our most gifted fellow humans in thinking previously impossible thoughts."
- The Humble Programmer, ALGOL 60: "the fruit of a genuine effort to carry abstraction a vital step further and to define a programming language in an implementation-independent way."
- The Humble Programmer, ALGOL 60: "it allows the programmer so much combinatorial freedom, that its confident use requires a strong discipline from the programmer." -- about the parameter mechanism.
- The Humble Programmer, PL/1: "keep our growing programs firmly within our intellectual grip when by its sheer baroqueness the programming language" -- escapes intellectual control.
- The Humble Programmer, PL/1: "little supposing that the main source of his problems could very well be that it contained already far too many" -- a user asking for about fifty new features in a one-hour lecture.
- The Humble Programmer, the vision: "these systems will be virtually free of bugs. These two improvements go hand in hand." -- with a cost of only a few percent of present man-years.
- The Humble Programmer, the vision: "they should not waste their time debugging, they should not introduce the bugs to start with."
- The Humble Programmer, three conditions: "The world at large must recognize the need for the change; secondly the economic need for it must be sufficiently strong; and, thirdly, the change must be technically feasible."
- The Humble Programmer, economic need: "as long as machines were the largest item on the budget, the programming profession could get away with its clumsy techniques" -- hardware prices were expected to drop by a factor of ten.
- The Humble Programmer, rules of program structure: "can differ tremendously in their intellectual manageability." -- even programs for the same task with the same mathematical content.
- The Humble Programmer, two kinds of rules: "Those of the first kind are easily imposed mechanically, viz. by a suitably chosen programming language." -- examples: no goto, no procedures with more than one output parameter.
- The Humble Programmer, two kinds of rules: "the rules of the second kind present themselves as elements of discipline required from the programmer." -- no mechanical way seen; example: no loop without a termination proof and an invariant.
- The Humble Programmer, the restriction: "it is not our business to make programs, it is our business to design classes of computations that will display a desired behaviour."
- The Humble Programmer, arguments one and two: "we have achieved, once and for all, a drastic reduction of the solution space to be considered." -- by restricting to intellectually manageable programs.
- The Humble Programmer, argument three: "program testing can be a very effective way to show the presence of bugs, but is hopelessly inadequate for showing their absence."
- The Humble Programmer, argument three: "the programmer should let correctness proof and program grow hand in hand." -- not first program then proof.
- The Humble Programmer, argument four: "the purpose of abstracting is not to be vague, but to create a new semantic level in which one can be absolutely precise."
- The Humble Programmer, argument four: "the intellectual effort needed to conceive or to understand a program need not grow more than proportional to program length." -- stated as an assumption not yet disproved by experience.
- The Humble Programmer, argument five: "the tools we are trying to use and the language or notation we are using to express or record our thoughts, are the major factors determining what we can think or express at all!"
- The Humble Programmer, argument five: "The competent programmer is fully aware of the strictly limited size of his own skull" -- so he avoids clever tricks like the plague.
- The Humble Programmer, argument five: "this language as a tool is an open invitation for clever tricks" -- from the one-liners phenomenon; called one of the most damning things to say of a language.
- The Humble Programmer, argument five: "I see a great future for very systematic and very modest programming languages."
- The Humble Programmer, experiment: "their notion of repetition was so tightly connected to the idea of an associated controlled variable to be stepped up, that they were mentally blocked from seeing the obvious." -- none of the experienced volunteers found the elegant solution.
- The Humble Programmer, aside: "Programming will remain very difficult, because once we have freed ourselves from the circumstantial cumbersomeness, we will find ourselves free to tackle the problems that are now well beyond our programming capacity."
- The Humble Programmer, argument six: "the only problems we can really solve in a satisfactory manner are those that finally admit a nicely factored solution." -- stated as an article of faith, hard to support experimentally.
- The Humble Programmer, argument six: "we shall do our utmost best to avoid all those interfaces impairing our ability to factor the system in a helpful way."
- The Humble Programmer, opposition: "those conservative groups of computer users that think their old programs so important that they don’t think it worth-while to rewrite and improve them." -- and the educational institutions.
- The Humble Programmer, political impediments: "is that of enhancing the capacities of the already capable, thus magnifying the difference in intelligence." -- the first effect of teaching a methodology.
- The Humble Programmer, conclusion: "the number of levels that can be distinguished meaningfully in a hierarchical system is kind of proportional to the logarithm of the ratio between the largest and the smallest grain"
- The Humble Programmer, conclusion: "provided that we respect the intrinsic limitations of the human mind and approach the task as Very Humble Programmers." -- also with full appreciation of the difficulty and modest, elegant languages.

## Readings for our work
- Separate our rules into the two kinds: rules that can be imposed mechanically (units on figures, quotes present in the source, typed numbers rejected) belong in the checks; rules that cannot (whether a reading follows from the facts, whether a question is the right one) remain discipline and must not be dressed up as checks. Check: for each check in method/, state which rule it enforces and whether a passing result actually establishes that rule. Rests on: two kinds of rules. Would not apply if: a rule of the second kind is later made mechanical with a sound procedure.
- Testing shows presence, not absence, of errors; our checks passing shows only that the faults they look for are absent. Build the argument (prediction, reasoning) together with the experiment, not after. Rests on: argument three. Would not apply if: the property checked is exhaustively enumerable (e.g. every quote against a fixed source).
- Avoid clever tricks in tools and DLL patches (one-line shell pipelines, regex rewrites of source files); they invite errors such as an unintended line-ending rewrite. Prefer plain, systematic edits. Rests on: argument five, open invitation for clever tricks, size of the skull. Would not apply if: the trick is wrapped, named and tested as a tool.
- The notations we use (the template syntax, the registry API) shape what we can express; when an analysis is hard to state in them, consider changing the notation rather than working around it. Rests on: influence of tools on thinking habits. Would not apply if: the difficulty is in the question itself.
- Asking for more features to fix a tool overloaded with features is the PL/1 symptom; before adding an option to the method, check whether the problem is that it already has too many. Rests on: PL/1. Would not apply if: the feature removes others.
- Old code is not untouchable: the legacy DLL parts we depend on can be rewritten and improved when the reason is recorded, but compatibility constraints of the mod must be stated. Rests on: curse of compatibility, opposition by users of old programs. Would not apply if: compatibility with saves and other mods is a hard constraint for the change.
