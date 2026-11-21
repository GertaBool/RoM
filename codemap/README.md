# Code map of the DLL

A map of every function of the DLL (`Assets/CvGameCoreDLL` of the GitLab repository `rise-of-mankind`) and
how they connect. It shows:
- who calls whom, and who overrides whom;
- what the DLL offers the game exe and what it calls in the exe;
- what Python calls in the DLL, and what the DLL calls in Python.

It describes linkage only, not what the functions do. It is read from the output of the real compiler, the
one the DLL is built with, so every call is the call the compiler made.

## Where to start

- `skeleton.md` is the overview:
  - size and completeness;
  - the groups of files and the calls between them;
  - every file with what it calls most and what calls it most;
  - the class hierarchy;
  - the turn and update backbone, two levels deep.
- `entry_points.md`: how control enters the DLL.
  - Functions the DLL offers the exe (`DllExport`).
  - Interface methods the exe provides.
  - What is exposed to Python, and where the DLL calls Python.
  - The events posted to Python, with every handler registered for them.
- `python.md`: the Python modules and how many of their calls reach DLL functions.
- `guides/`: written by hand, from the same source commit.
  - `key-functions.md`: the functions that rank above the rest, what each does, and what a rewrite keeps.
  - `loans-and-bonds.md`: where loans and a bond market would go, in the DLL and the UI.
- `files/<file>.md`: one page per source file. Every function in line order, with what it calls, what it
  takes the address of, and who calls it.
- `map/`: the data, as tab-separated tables (below).
- `tool/query.py`: questions the pages don't answer directly.
- `graph.html`, `tool/impact.py`, `tool/graph.py`: the whole graph (C++, Python, members, XML, defines) and what a
  change reaches. See "The whole graph, and what a change reaches" below.

```sh
python3 codemap/tool/query.py find 'AI_chooseProduction'          # find a function
python3 codemap/tool/query.py callees CvCityAI::AI_chooseProduction 2
python3 codemap/tool/query.py callers CvUnitAI::AI_attackCityMove 3
python3 codemap/tool/query.py path CvGame::update CvCityAI::AI_chooseProduction
python3 codemap/tool/query.py rank 12                              # the functions that rank above the rest
```

`rank`: function A ranks above function B when every call path from outside the DLL into B passes through A
(A dominates B). Calls from outside enter at every function the exe or Python can call: exported functions,
functions bound for Python, and functions with no caller in the DLL. A function's rank is the number of
functions it dominates.

## Variables, XML, defines and what a change reaches

The compiler map has calls only. A second layer, read straight from the source with
[tree-sitter](https://tree-sitter.github.io/) (a C++ parser: no compiler, no headers, about 7 seconds for the
whole DLL), adds the data side. It can be rerun on any checkout, so it can be newer than the compiler map.
`map/syntax_meta.tsv` names its commit.

- `fields.tsv`: every data member of every class and struct, with its declared type.
- `field_access.tsv`: every use of a member inside a function: `read`, `write`, `ref` (`&m_x` passed on, as
  in `pStream->Read(&m_x)`), `call` (a method of the member, as in `m_aUnits.push_back`).
- `field_strings.tsv`: a member and a string passed to the same call. For the XML loaders this is the tag
  that fills the member (`GetChildXmlValByName(&m_iCost, "iCost")`).
- `defines_used.tsv`: `getDefineINT("NAME")` and the like.
- `xml_tags.tsv`, `xml_defines.tsv`: every XML element name and every `<DefineName>`, with the files that hold
  them in each layer the game reads (`mod`, `bts`, `civ4`), and whether the game loads that file: a file of the
  mod shadows the base game's file of the same path.
- `xml_classes.tsv`: which XML file fills which info class (`LoadGlobalClassInfo(GC.getTechInfo(),
  "CIV4TechInfos", "Technologies", ...)`, with the class from `std::vector<CvTechInfo*>& getTechInfo()`).
- `syntax_functions.tsv`, `syntax_calls.tsv`: function extents, and calls of names the compiler map does not
  define (callers of code added after the map's commit).

```sh
pip install tree-sitter tree-sitter-cpp
python3 codemap/tool/syntax.py <checkout>/Assets/CvGameCoreDLL <checkout>/Assets/XML <BTS XML> <Civ4 XML>
```

## The whole graph, and what a change reaches

`tool/graph.py` joins every table into one dependency graph. Its nodes are C++ functions, Python functions,
member variables, XML tags and defines. An edge from A to B means a change of A reaches B:

| link | from | to | source |
|---|---|---|---|
| `call` | C++ function | its C++ callers (virtual calls into overrides) | `calls.tsv` |
| `py>cpp` | C++ function bound for Python | the Python functions calling it (name match) | `py_to_cpp.tsv` |
| `py>py` | Python function | its Python callers: same module, or a name defined in one module only | `py_calls.tsv` |
| `cpp>py` | Python function | the C++ functions calling it | `cpp_to_py.tsv` |
| `event` | Python event handler | the C++ function posting its event | `event_handlers.tsv` |
| `read` | member variable | the functions reading it | `field_access.tsv` |
| `fill` | XML tag | the members it fills | `field_strings.tsv` |
| `define` | define | the functions reading it | `defines_used.tsv` |
| `writes` | changed C++ function | the members it writes (only from the changed functions themselves) | `field_access.tsv` |

Each member also carries the XML files it is filled from (its class's files, from `xml_classes.tsv`, that hold
the tag, with the base-game copies they shadow), and whether `read`/`write(FDataStreamBase*)` serializes it.

```sh
python3 codemap/tool/impact.py diff <checkout> origin/main origin/<branch>   # C++, Python and XML changes of a branch
python3 codemap/tool/impact.py func CvPlot::setRevealed
python3 codemap/tool/impact.py py CvEventManager.py:CvEventManager.onCityBuilt
python3 codemap/tool/impact.py field CvTechInfo::m_iResearchCost              # writers, readers, XML files, serialization
python3 codemap/tool/impact.py tag iCost                                       # XML tag -> members -> readers -> C++ and Python
python3 codemap/tool/impact.py define GRAPHICS_PAGING_MAX_IN
python3 codemap/tool/impact.py file Units/CIV4UnitInfos.xml                    # every tag the DLL reads from it
python3 codemap/tool/graph_html.py                                             # rebuild graph.html
```

A report lists, level by level, every node reached, with the node it was reached from and the link. It also
gives the members reached (serialization, XML files), the tags and defines, the exits (C++ functions the exe
calls, functions bound for Python, Python event handlers) and the C++ files and Python modules touched.

`diff` reads both commits itself:
- **C++:** changed, added and removed functions, member declarations, members written on changed lines, and
  defines read on changed lines.
- **Python:** changed functions, found by indentation.
- **XML:** tags on changed lines, and the `<DefineName>` of a changed define value.

When the source has moved past the compiler map's commit, a C++ function newer than the map is followed by name
("call (name match)").

`graph.html` is one self-contained page (open it in a browser, no server needed):
- **Files**: every C++ file, Python module and loaded XML file, linked by the function-level links above,
  summed per pair of files. Click a file for what it depends on and what depends on it, its functions, members
  or tags, and what a change of it reaches.
- **Impact**: search any C++ or Python function, member, `<tag>`, `#DEFINE` or file. The page shows every level
  of the reach in columns across C++, Python, members, tags and defines, each node with the link that reached
  it. For a member it shows its writers, readers, XML files and serialization.

Limits:
- Python links are name matches: Python resolves names when it runs.
- A `py>py` link across modules is made only when the name is defined in one module.

Limits of the member layer: it is a parser, not a compiler.
- Members are matched by name. Inside a method, an unqualified name is that class's member (or a base's)
  unless a local or parameter hides it. `obj->m_x` is counted for every class that declares `m_x`.
- Every `#ifdef` branch is read.
- MSVC words tree-sitter does not know (`DllExport` and similar) are blanked before parsing. The parse
  errors left are counted per file in `syntax_parse.tsv`.
- Checked by hand: the uses of `CvCity::m_iPopulation` and `CvPlot::m_bRevealedRouteDirty` match a grep of
  the source line for line.

`impact/` holds reports written with `impact.py diff`.

## Python: what lands in the DLL and what in the exe

The game's Python reaches C++ only through the classes of `CvPythonExtensions`. The DLL registers some
(`python::class_<C>("Name")`); the exe registers the rest (`CyInterface`, `CyEngine`, `CyCamera`, `CyPopup`,
`CyUserProfile` ...). The code map sees only the DLL, so `tool/pyapi.py` adds the class reference of the BUG
project ([civ4bug PythonAPI](https://civ4bug.sourceforge.net/PythonAPI/), BTS 3.17, generated from the game's
docstrings):

```sh
curl -sS -o /tmp/AllClasses.html https://civ4bug.sourceforge.net/PythonAPI/AllClasses.html
python3 codemap/tool/pyapi.py /tmp/AllClasses.html <checkout>/Assets/CvGameCoreDLL
```

- `python_classes.tsv`, `python_bindings.tsv`: every class the DLL registers, with its C++ class and bases, and
  every `.def("name", &f)` with the class it is chained to. Both are read from the source.
  `python_defs.tsv` (from the compiler) misses 37 of the 3,842 bindings at 9627e508:
  - 5 are virtual methods, all `getButton`: the listing pushes a vcall thunk, not the function;
  - 24 point at functions no unit compiles;
  - 8 are not yet explained (open).
- `py_api.tsv`: every method of the reference, and whether its class is registered by the DLL or by the exe.
- `py_targets.tsv`: every attribute call in the Python (`x.f()`), and where the name lands: `dll`, `exe`,
  `both` (both bind the name), or `python`. The match is by name, as Python resolves names when it runs.
- `py_api_check.tsv`: for each class the DLL registers, methods of the reference it does not bind (`missing`)
  and methods it binds that the reference lacks (`added`, mostly the mod's own, e.g. the Revolution getters of
  `CvCivicInfo`).

## The build at 9627e508 (GitLab Graphics-Paging-Fix-Test)

The whole map was rebuilt at `9627e508fedc` on a cloud machine, with `build.sh`'s steps run one by one.

| input | source | check |
|---|---|---|
| Visual C++ Toolkit 2003, Platform SDK | the user's Drive folder `platformsdk` | SHA-256 as in `builds/0009/provenance.json` |
| Boost 1.32, Python 2.4 headers | `beyond-the-sword-sdk-develop-functional.tar.gz`, GitLab repository root | SHA-256 as in the provenance |
| Python 2.4 (`python.exe` for `py24_scan.py`) | python.org `python-2.4.4.msi` | good PGP signature, key 0EDDC5F26A45C816 (Anthony Baxter) |
| mod's Python, XML, Config | GitLab `9627e508` | |
| Beyond the Sword's Python | the user's Drive folder `prereq_original_files_civ4_bts/Python (2)` | has `Screens/CvCorporationScreen.py` and the corporation events; the scan gives the same tables as github `max-zanko/civ4-beyond-the-sword-sdk` (code identical, whitespace aside) |
| Civilization IV's Python | the user's Drive folder `prereq_original_files_civ4_bts/Python (1)` | scanned with the mod at `2a8b9a83`, it reproduces the previous map's Python tables row for row |

Results:
- **DLL:** all 105 units compiled, with 0 warnings and 0 errors.
- **Python:** the game imports by module name, from the mod's folder, then Beyond the Sword's, then Civilization
  IV's. The previous map had no Beyond the Sword layer: its base modules, `CvEventManager.py` among them, were
  Civilization IV's. That layer is now in place. `map/py_modules.tsv` gives each module's layer: 189 mod,
  33 BTS, 55 Civilization IV. The event manager's handler map now has the 77 events of the BTS file, which
  include the corporation events and `ModNetMessage`; the previous map had 57.

Two snags of the machine, for whoever builds next:
- Wine 9.0 aborted at start-up (`free(): invalid pointer`) when run with that session's environment. It ran when
  started with `env -i HOME=/root PATH=/usr/bin:/bin` and the toolchain variables.
- `toolchain/setup_toolchain.sh` stops after unpacking. Under `set -e`, its case-alias loop ends with a false
  `[ ... ] && ln`, which ends the script. The remaining steps (aliases, `vctk` link, `wineboot`) were run by hand.

## How it is made

`tool/build.sh <rise-of-mankind checkout> <Python 2.4 dir> <base game Python dir>...` rebuilds everything, in a
few minutes. The base game Python dirs are the folders the game falls back to after the mod's, in its order:
Beyond the Sword's, then Civilization IV's. The DLL is compiled from the checkout's `Assets/CvGameCoreDLL`; the SDK
tarball supplies only the Boost 1.32 and Python 2.4 headers. The source commit is written at the top of
`skeleton.md`.

1. **`tool/compile.sh` compiles every `.cpp` with Visual C++ Toolkit 2003 under Wine.** It uses the source's
   own release flags and defines (`NDEBUG`, `FINAL_RELEASE`), with two changes:
   - `/Od /Ob0` instead of `/O2`, so no call is inlined or optimised away;
   - `/FAs`, an assembly listing per unit with the source lines in it.

   Nothing is linked or run. One extra unit includes every header and is built as a precompiled header with
   `/Z7`. MSVC then writes the type records of every class those headers define.
2. **`tool/extract_asm.py` reads the listings and objects.**
   - A function is a `PROC` of a listing whose source file belongs to the DLL. Its line is that of its
     opening brace.
   - A **direct call** (`call ?name`) names its exact target, as the compiler resolved it: overloads,
     `#ifdef`s, macros and templates included.
   - A **virtual call** (`call [table + N]`) is matched to a method by its slot. Several pieces of evidence
     are combined:
     - the method names written in the statement;
     - the slot layouts from the type records;
     - where the code shows it, the object's class. That is `this`, the result type of the call that
       produced the object, or a local's declared type.

     It points to the function in that class's table when the DLL has one, otherwise to the class that
     introduces the slot. The object's class, when known, is kept with the call. What may run instead is
     an override in that class or below it (`overrides.tsv`); the pages and `query.py` follow only those.
     A direct call to a virtual method (`Base::f()`, or an object whose class the compiler knew) runs that
     method only.
   - **Overrides** come from comparing each class's table of virtual functions in the listings with its
     base's.
   - **Exports** are the `/EXPORT` directives each object passes to the linker.
   - **Python bindings, calls into Python and event names** are the string arguments pushed for those calls.
3. **`tool/extract_py.py` lists the Python modules the game loads,** and `tool/py24_scan.py` parses them.
   - The game imports by name, the mod's folder first, then the base game's. A base module the mod replaces
     is left out, and so is a file whose name is not a module name.
   - The parser is the game's own Python 2.4 under Wine, its `compiler` package.
   - Links into the DLL and the event handlers are then matched by name. The handlers include the BUG
     configuration XML.
4. **`tool/render.py` writes the pages.** Every count on them is computed there from the tables.

## The tables in `map/`

| file | one row per |
|---|---|
| `functions.tsv` | function: `id`, scope, name, signature, kind (`method`, `function`, `generated` for those the compiler writes itself), file, first and last line, flags, and its mangled name as `key`. Rows with `definition` 0 are virtual methods that are called but have no function in the DLL: pure virtual, or provided by the exe. |
| `calls.tsv` | `call` (direct), `virtual`, or `ref` (a function's address taken, e.g. a callback for the pathfinder): caller, callee, file, line (empty in functions the compiler wrote), and for a virtual call the object's class when the code shows it. An ambiguous virtual call has one row per candidate. |
| `overrides.tsv` | method and the base method it overrides |
| `classes.tsv`, `bases.tsv` | class of the source, with its virtual slots and whether its table is in the DLL; class and base |
| `unresolved.tsv` | call not tied to one function, with the reason: a virtual `delete` (the class is not visible in the code), a call through a function pointer, an ambiguous virtual call, a virtual call matching no name |
| `imports.tsv` | function imported from another DLL (the C runtime, the C++ library) and how often it is called |
| `units.tsv` | compiled unit, its warnings and errors |
| `python_defs.tsv` | function exposed to Python with `def("name", &f)` |
| `python_calls.tsv` | DLL call into Python, `callFunction(module, "function")` |
| `events.tsv` | `CvDllPythonEvents` report function and the event it posts |
| `completeness.tsv` | definition seen by ctags only (in the source, compiled by no unit) or compiled only |
| `py_functions.tsv`, `py_calls.tsv`, `py_handlers.tsv`, `py_errors.tsv` | Python `def` and `class`; call site; `addEventHandler` call; module Python 2.4 could not parse |
| `py_to_cpp.tsv` | Python call of a name the DLL exposes, with the candidate C++ functions |
| `cpp_to_py.tsv` | DLL call into Python, with the Python function it lands in |
| `event_handlers.tsv` | event and each handler registered for it |
| `py_event_registrations.tsv` | every registration of a Python event handler, for any event name |
| `py_modules.tsv` | Python module the game loads, with its layer (mod, Beyond the Sword, Civilization IV) and file |
| `python_classes.tsv`, `python_bindings.tsv`, `py_api.tsv`, `py_targets.tsv`, `py_api_check.tsv` | see "Python: what lands in the DLL and what in the exe" |
| `fields.tsv`, `field_access.tsv`, `field_strings.tsv`, `defines_used.tsv`, `xml_tags.tsv`, `xml_defines.tsv`, `xml_classes.tsv`, `syntax_*.tsv` | see "Variables, XML, defines and what a change reaches" |

## Checks, and limits

Checked when it was built:
- **Against the source:** the calls of `CvCity::doTurn` in the listing are those of the source, line by line.
- **Against an earlier map made with clang** from the same source, pair by pair.
  - Where the two disagree, the compiler is right: a `sizeof(...)` that clang counted as a call, trivial
    copies, implicit destructors clang left out, `new T[n]` passing a constructor's address.
  - Or the two only spell a name differently.
- **Against ctags,** for the definitions. ctags sees inline functions nothing uses, templates never
  instantiated and `#ifdef`-ed code, which no unit compiles; the compiler sees functions written by macros.
- **The Python parse** covers every module the game loads.

Limits:
- **Only compiled code is in the map.** An inline function nothing calls, or a template never instantiated,
  is not, and `completeness.tsv` lists them.
- **A virtual call's target can stay open.** It is a candidate list when several classes share the method
  name at that slot and the code doesn't show the object's class.
  - A virtual `delete` has no class at all.
  - Calls through function pointers are listed with their statement; the function's address is in `calls.tsv`
    as `ref` where it is taken.
- **Overloaded virtual methods of the exe's interfaces** (e.g. `FDataStreamBase::Read`) are matched by name.
  The type records' slot offsets for overload sets cannot be read, so which overload is called is not shown.
- **The exe is outside the map.** Calls into its interfaces are recorded. Which exported functions the exe
  actually calls would need the exe's import table.
- **Python links into the DLL are name matches,** since Python resolves names when it runs. Calls through
  `getattr` or strings are not seen.
- **Line numbers** refer to the source at the commit named in `skeleton.md`.
- **Rebuilds give the same tables.** The compiler names each anonymous namespace with a hash that changes
  with every compile, so the hash is replaced by a number fixed by the unit's name.

This folder is not one of the commit gate's gated paths (`method/config.json`). Its tools change no product
code, but they are tools, and the gate as configured does not cover them.
