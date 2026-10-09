# Rise of Mankind architecture research

Source-based assessment of [aretemaxxing-group/rise-of-mankind on GitLab](https://gitlab.com/aretemaxxing-group/rise-of-mankind), pinned to revision `1ab4f99a76adb530f86b278390ab8139ef41cc96`.

- [Detailed AI, turns, pathfinding, combat and diplomacy guide](docs/review/AI_AND_GAME_LOGIC.md)
- [Architecture and code assessment](docs/review/REVIEW.md)
- [Game-flow model and headless simulator specification](docs/review/GAMEFLOW_MODEL.md)
- [Complete Python, XML and native file catalog](docs/review/FILE_CATALOG.md)
- [Architecture diagram](docs/review/architecture.svg)
- [Interactive source explorer](docs/review/explorer.html) — download the HTML and open it in a browser; GitHub's file view displays its source.
- [Regression output](docs/review/regression.log) and [reproduced findings](docs/review/audit-findings.json)

The reviewed revision contains 252 Python files, 956 XML files and 277 native source/header files. The review combines whole-tree structural analysis with focused behavioral inspection. The existing regression suite has 12 passing programs and 2 failing programs. The BTS executable and a complete headless simulator were not run.

**The bundled DLL is older than the source**, as confirmed by the repository owner. These reports assess the pinned source. In-game comparisons require a rebuilt DLL with recorded source/build provenance; the existing binary is not an oracle for the reviewed code. See [the provenance record](docs/review/source-binary-provenance.json).

The reports include fixed-revision source links, a state-transition model, deterministic replay requirements, engine boundaries and proposed tests. The machine-readable inventories and review scripts are in `docs/review/`.
