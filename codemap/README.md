# Code map of the DLL

A map of every function in the DLL source (`Assets/CvGameCoreDLL` of the GitLab repository
`rise-of-mankind`) and how they connect: who calls whom, who overrides whom, what the game exe calls, what
Python calls, and what the DLL calls in Python. It describes linkage only, not what the functions do.

## Where to start

- `skeleton.md`: the overview.
  - Size and completeness.
  - The groups of files, and how many calls run between them.
  - Every file with what it calls most and what calls it most.
  - The class hierarchy.
  - The turn and update backbone, two levels deep.
- `entry_points.md`: how control enters the DLL.
  - Functions the exe calls (`DllExport`).
  - Interface methods the exe provides.
  - What is exposed to Python.
  - Where the DLL calls Python.
  - The events posted to Python, with every handler registered for them.
- `python.md`: the Python modules and how many of their calls reach DLL functions.
- `files/<file>.md`: one page per source file. Every function in line order, with what it calls, what it
  takes the address of, and who calls it.
- `map/`: the data, as tab-separated tables (below).
- `tool/query.py`: questions the pages don't answer directly.

```sh
python3 codemap/tool/query.py find 'AI_chooseProduction'          # find a function
python3 codemap/tool/query.py callees CvCityAI::AI_chooseProduction 2
python3 codemap/tool/query.py callers CvUnitAI::AI_attackCityMove 3
python3 codemap/tool/query.py path CvGame::update CvCityAI::AI_chooseProduction
```

## The tables in `map/`

C++, from clang:

| file | one row per |
|---|---|
| `functions.tsv` | function declared or defined in the source: `id`, scope, name, signature, kind, file, first and last line, and flags (`definition`, `exported`, `virtual`, `pure`, `static`), plus clang's USR as a stable key |
| `calls.tsv` | call site (`call`) or place where a function's address is taken (`ref`, e.g. a callback handed to the pathfinder): caller id, callee id, file, line |
| `overrides.tsv` | method and the base method it overrides directly |
| `classes.tsv`, `bases.tsv` | class or struct defined in the source; class and its base |
| `includes.tsv` | file and a file it includes |
| `python_defs.tsv` | function exposed to Python with `def("name", &f)`: Python name, function id |
| `python_calls.tsv` | DLL call into Python, `callFunction(module, "function")` |
| `events.tsv` | `CvDllPythonEvents` report function and the event name it posts |
| `diagnostics.tsv` | statement clang could not fully check; calls inside may be missing |
| `unresolved.tsv` | call clang could not resolve to a function |
| `completeness.tsv` | function definition seen by ctags only or by clang only |

Python, scanned by name:

| file | one row per |
|---|---|
| `py_functions.tsv` | `def` and `class` |
| `py_calls.tsv` | call site, with the target when the name is defined once in the same module |
| `py_to_cpp.tsv` | Python call of a name the DLL exposes, with the candidate C++ functions |
| `cpp_to_py.tsv` | DLL call into Python, with the Python function it lands in |
| `event_handlers.tsv` | event and each handler registered for it |

## How it is made

`tool/build.sh <rise-of-mankind checkout> <base game Python dir>` rebuilds everything. Two builds of the same
source give identical files. The source commit is written at the top of `skeleton.md`.

1. **Copy the source.** It is copied with the portability edits of `toolchain/clang-gate`:
   - case aliases for `#include` names;
   - MSVC 7.1's old `for` scope;
   - a token paste only MSVC accepts.

   `DllExport` is redefined as a clang annotation, because clang drops `__declspec(dllexport)` outside Windows
   targets. Line numbers stay those of the source.
2. **Parse each `.cpp` with libclang** (`tool/extract_cpp.py`), in MSVC compatibility mode with the release
   build's defines (`FINAL_RELEASE`, no `_MOD_*` switches) and the BTS SDK's Boost and Python headers.
   - Every call is resolved by clang to the exact function, so overloads and same-named methods are told
     apart.
   - Macros are expanded. `GC.` becomes `CvGlobals::getInstance()`, `GET_PLAYER` becomes
     `CvPlayerAI::getPlayer`.
   - Nothing is compiled or run.
3. **Count definitions with universal-ctags** on the same files, as an independent check of what clang found.
4. **Scan the mod's Python and the base game's Python** (`tool/extract_py.py`).
   - The game imports a module by name, mod first, so a base module the mod replaces is left out.
   - The BUG configuration XML is read for its event registrations.
5. **Render the pages** from the tables (`tool/render.py`). Every count on them is computed there.

## What it gets right, and what it does not show

Checked when it was built:
- The calls of `CvCity::doTurn` were compared with the source line by line.
- The function definitions were compared with ctags.
  - Definitions only ctags sees are inside `#ifdef` blocks the release build leaves out (`_MOD_FRACTRADE`,
    `_BUFFY`, the assert dialog), or are spelled differently.
  - Definitions only clang sees are written by macros or several to a line.
- The Python bindings were compared with a text search for `.def("`.
  - Every binding only the text search found is commented out or excluded by `#ifdef`.
  - Every one only clang found is written in a form the text pattern missed.
- The build was run twice and gave identical files.

Limits:
- **Virtual calls** are recorded to the method named at the call. Which override runs is decided at run time;
  `overrides.tsv` lists the candidates, and `query.py` and the pages follow them.
- **Function pointers** are recorded where the address is taken (`ref`), not where the pointer is later
  called.
- **The exe** is outside the map. Calls into its interfaces (`gDLL->...`, the `CvDLL*IFaceBase` classes) are
  recorded; what the exe calls back is known only through the exported functions.
- **Code the release build leaves out** by `#ifdef` is not in the map. **Statements clang could not fully
  check** are listed in `diagnostics.tsv`.
- **Python links are name matches,** not resolved targets. A method name exposed by several C++ classes gives
  several candidates. Calls through `getattr` or strings are not seen.
- **The base game's Python** comes from the game files in the session's downloads. A second downloaded folder
  of BUG/BUFFY add-on files is not part of the mod's import path and is not included.
- **Line numbers** refer to the source at the commit named in `skeleton.md`.

This folder is not one of the commit gate's gated paths (`method/config.json`). Its tools change no product
code, but they are tools, and the gate as configured does not cover them.
