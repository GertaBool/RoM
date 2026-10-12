# Rise of Mankind research and source fixes

Source-based assessment of [aretemaxxing-group/rise-of-mankind on GitLab](https://gitlab.com/aretemaxxing-group/rise-of-mankind), pinned to revision `1ab4f99a76adb530f86b278390ab8139ef41cc96`.

The latest fixes target GitLab revision `6222511c1a81649445fa69e8ca6dca79cf60c975`. Patch 0007 includes the preceding settlement/transport corrections and replaces premature destination pruning with joint destination and route search. The historical assessments retain their original source identity.

- [Implemented joint settlement search: complete candidates, route comparison and bound pruning](research/settlement-search/README.md)
- [Latest cumulative source patch: joint planning; 22 passing regression programs](fixes/README.md#joint-settlement-search)
- [Transport entry: loaded passengers, ship roles and autoplay update order](research/transport-entry/README.md)
- [Settlement placement: scoring defects, architectural criticism and a development-plan optimizer](research/settlement/README.md)
- [Previous settlement and transport-entry patch; 21 passing programs](fixes/README.md#settlement-placement)
- [Settler transport: root causes, voyage dispatcher, opening development and engine test scenarios](research/transport/README.md)
- [Previous opening/voyage patch for GitLab 19e4d59: 19 passing regression programs](fixes/README.md#opening-development-and-settler-voyages)
- [Carthage autoplay: worker/cargo defects, production accounting, civic tradeoffs and coordinated simulation](research/autoplay/README.md)
- [Historical autoplay patch: fixes plus cleanup, 17 passing regression programs](fixes/README.md#carthage-autoplay-coordination)
- [Current source cleanup: 291 fewer runtime lines, reserve correction, 16 passing regression programs](fixes/README.md#current-source-cleanup)
- [Original source fixes and operation-supply patch history](fixes/README.md#historical-source-correctness-patch)
- [Critical architecture assessment: hidden state, rule ownership and staged refactoring](research/architecture/README.md)
- [AI algorithm study: exact optimization, bounded search, evolutionary methods and C++03 costs](research/algorithms/README.md)
- [Detailed AI, turns, pathfinding, combat and diplomacy guide](docs/review/AI_AND_GAME_LOGIC.md)
- [Deeper findings with reproducible source probes](docs/review/DEEP_FINDINGS.md)
- [Simulation implementation plan, contracts and scenario backlog](simulation/README.md)
- [Architecture and code assessment](docs/review/REVIEW.md)
- [Game-flow model and headless simulator specification](docs/review/GAMEFLOW_MODEL.md)
- [Complete Python, XML and native file catalog](docs/review/FILE_CATALOG.md)
- [Architecture diagram](docs/review/architecture.svg)
- [Interactive source explorer](docs/review/explorer.html) — download the HTML and open it in a browser; GitHub's file view displays its source.
- [Regression output](docs/review/regression.log) and [reproduced findings](docs/review/audit-findings.json)

The reviewed revision contains 252 Python files, 956 XML files and 277 native source/header files. The review combines whole-tree structural analysis with focused behavioral inspection. The original regression baseline had 12 passing programs and 2 failing programs; the first correctness patch passed all 15 programs. The current upstream and cleanup revisions pass 16 programs; the autoplay fixes pass 17, and the opening/transport changes pass 19 and the settlement changes pass 20. The BTS executable and a complete headless simulator were not run.

**The bundled DLL is older than the source**, as confirmed by the repository owner. These reports assess the pinned source. In-game comparisons require a rebuilt DLL with recorded source/build provenance; the existing binary is not an oracle for the reviewed code. See [the provenance record](docs/review/source-binary-provenance.json).

The new Carthage autoplay report concerns a DLL the user compiled locally from current GitLab source, not that older bundled binary. Its save metadata and provenance limits are documented separately.

The reports include fixed-revision source links, a state-transition model, deterministic replay requirements, engine boundaries and proposed tests. The machine-readable inventories and review scripts are in `docs/review/`.

The deeper review reproduces five source-level issues and verifies two lifecycle/identity contracts. `simulation/` contains validated schema examples and a contract validator; it does not yet implement a game simulator. Run the commands in its README to validate the examples and reproduce the new source observations.
