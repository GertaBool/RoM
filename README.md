# Rise of Mankind research and source fixes

Source-based assessment of [aretemaxxing-group/rise-of-mankind on GitLab](https://gitlab.com/aretemaxxing-group/rise-of-mankind), pinned to revision `1ab4f99a76adb530f86b278390ab8139ef41cc96`.

New research: [AI behaviour over four whole Marathon games](research/ai-behavior/README.md) (one civilization never founds a city on Earth 12, settlers wait for escorts, transports and generals sit idle) and [how the game runs](research/engine/README.md) (rendering and HUD requests, turn time, memory). Patch 0016, landed as [!41](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/41), fixes a random crash: an AI that razed a captured city read the city's name after deleting it. A Marathon game in the harness crashed on it at turn 415 and plays on with the fix. Before that, the work studied the AI in diplomacy and the late game: patches 0014 and 0015, both landed ([!39](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/39), [!40](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/40)). Mapping the deal, attitude and personality code found 14 defects. Examples: 32-bit overflow in the peace and surrender valuations, a received resource valued at a fifth of its worth, AI-to-AI resource swaps with no value check, tribute thresholds read from the wrong leader, and attitudes that lagged a turn. Fixed, the AIs fight fewer wars, at better odds, and win more of them. The headless harness first had to be corrected in three ways. It now applies RoM's Python building rules. It no longer leaks memory per callback: that leak, not slow DLL code, caused the Marathon crashes around turn 491. And its telemetry no longer changes the games it observes. A game reloaded from a save used to play differently from the running game; with 0014 and 0015 it plays identically. Patch 0015 also cuts late-game turn time by 17 % with an identical game. Before that, patch 0013 followed up on the same save: why Rome had no Writing at 410 BC, and what the settler overproduction was. Rome kept the Mercenaries civic for 125 turns because the AI valued its free experience at half of Rome's commerce, counted its unit charges at twice the real gold and could not disband any unit trained under it; unit charges took 45 of 96 commerce and research ran at 3 beakers a turn. The settlers were idle rather than overbuilt (141 created over the game, 122 cities founded), for causes patch 0012 had fixed. Patch 0013 has landed as [!38](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/38). Patch 0012 answers an autorun report as Masinissa (Marathon, 410 BC): the turn that never ended, slow turns, idle settlers and AIs that hoarded gold and trained Spearmen instead of buildings. The reported save was loaded into the real DLL in the headless harness and played on with every seat on AI. The endless turn came from a unit that lost its group on every update slice; turns now take 2.6 s instead of 9.6 s; settlers count only sites they can be delivered to and are disbanded when none remain; over 30 turns the AIs research 21 % more and complete 347 buildings instead of 238. Patch 0012 targets GitLab `main` after patch 0011 and has landed as [!37](https://gitlab.com/aretemaxxing-group/rise-of-mankind/-/merge_requests/37). Patch 0011 fixes settlers that never landed: at sea, no land unit aboard counted as an escort. Patch 0010 keeps AI path searches reusable, indexes escort grouping, and fixes siege positioning, synchronized landings, worker targeting and settlers abandoning a reached site. Patch 0009 fixes defects found by compiling the whole DLL, removes two turn-time hot spots and plans research as a minimum-cost prerequisite closure. Each ships an MSVC 2003-built DLL with provenance. Historical patches and assessments retain their original source identity.

- [Diplomacy and leader personalities: code maps, defects, a corrected 0013 vs 0014 campaign, reloaded games and late-game turn time](research/diplomacy/README.md)
- [Patch 0016 and its DLL: crash fixes, 31 passing regression programs; landed on GitLab main](fixes/README.md#crash-fixes-objects-used-after-they-were-deleted)
- [Patch 0015 and its DLL: 30 passing regression programs; landed on GitLab main](fixes/README.md#late-game-turn-time-and-save-consistency)
- [Patch 0014: 29 passing regression programs; landed on GitLab main](fixes/README.md#diplomacy-power-overflow-deal-valuation-attitude-lag-new-deal-shapes)
- [Rome without Writing and the settlers at 410 BC: upkeep traps, measured on the reported save](research/rome-and-settlers/README.md)
- [Patch 0013 and its DLL: 28 passing regression programs; landed on GitLab main](fixes/README.md#upkeep-traps-rome-without-writing-settlers)
- [Autorun as Masinissa: the endless turn, turn time, settlers and the AI economy, measured on the reported save](research/autorun-masinissa/README.md)
- [Patch 0012 and its DLL: 27 passing regression programs; landed on GitLab main](fixes/README.md#autorun-fixes-endless-turn-turn-time-settlers-and-ai-economy)
- [Settler landing checked against the real DLL: why the ship waited offshore, and the fix](research/landing-engine/README.md)
- [Patch 0011 and its DLL: 24 passing regression programs; landed on GitLab main](fixes/README.md#settler-landing-escorts-at-sea)
- [Headless harness: run the real CvGameCoreDLL.dll under Wine without the game](toolchain/harness/README.md)
- [Pathfinding, naval transport, settlers and siege: reusable searches, grouping index and four decision fixes](research/pathing/README.md)
- [Patch 0010 and its DLL: 24 passing regression programs; landed on GitLab main](fixes/README.md#pathfinding-transport-and-siege)
- [Turn time, research planning and compiler-found defects: math, measurements and interaction audit](research/turn-time/README.md)
- [Patch 0009: 21 passing regression programs; landed on GitLab main](fixes/README.md#turn-time-and-research-planning)
- [Built DLLs: patch 0009 and the unmodified baseline, with provenance](builds/0009/provenance.json)
- [Building the DLL on Linux: Visual C++ Toolkit 2003 under Wine, plus a clang differential gate](toolchain/README.md)
- [Earlier settler landing fix (patch 0008; did not fix the reported failure on its own)](research/landing/README.md)
- [Implemented C++03 city-economy arithmetic: 15,000 native-fragment comparisons](simulation/economy/README.md)
- [New AI competence study: economic project planning, transport ownership, 165-case C++03 lab and integration plan](research/competence/README.md)
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

**The bundled DLL is older than the source**, as confirmed by the repository owner. These reports assess the pinned source. In-game comparisons require a rebuilt DLL with recorded source/build provenance; the existing binary is not an oracle for the reviewed code. See [the provenance record](docs/review/source-binary-provenance.json). `builds/` now holds such rebuilt DLLs for `d8cedd5` and patch 0009.

The new Carthage autoplay report concerns a DLL the user compiled locally from current GitLab source, not that older bundled binary. Its save metadata and provenance limits are documented separately.

The reports include fixed-revision source links, a state-transition model, deterministic replay requirements, engine boundaries and proposed tests. The machine-readable inventories and review scripts are in `docs/review/`.

The deeper review reproduces five source-level issues and verifies two lifecycle/identity contracts. `simulation/` contains validated schema examples and a contract validator; it does not yet implement a game simulator. Run the commands in its README to validate the examples and reproduce the new source observations.
