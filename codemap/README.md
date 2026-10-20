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

## How it is made

`tool/build.sh <rise-of-mankind checkout> <base game Python dir> <Python 2.4 dir>` rebuilds everything, in a
few minutes. The source commit is written at the top of `skeleton.md`.

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
