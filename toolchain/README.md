# Building CvGameCoreDLL.dll on Linux

These scripts build the DLL with the compiler Civilization IV: Beyond the Sword
requires: **Visual C++ Toolkit 2003** (`cl` 13.10.3077) and the **Platform SDK for
Windows Server 2003 SP1**, run under Wine. No Windows installer is executed; both
are unpacked.

## Inputs

| Input | Used for |
|---|---|
| `Install_Civ4_Microsoft_Windows_SDK_Visual_C_Toolkit.exe` (community bundle of the 2003 toolkit) | `cl.exe`, `link.exe`, CRT headers and `msvcrt.lib`/`msvcprt.lib` |
| `5.2.3790.1830.15.PlatformSDK_Svr2003SP1_rtm.img` | Windows headers and import libraries |
| BTS SDK `CvGameCoreDLL` folder (`Boost-1.32.0/`, `Python24/`) | Boost.Python and Python 2.4 headers and libraries |

[`builds/0009/provenance.json`](../builds/0009/provenance.json) lists the hashes of
the files used for the published builds.

Host packages: `wine32` (Wine 9.0 was used), `innoextract`, `p7zip-full`, `msitools`, `make`.

## Build

```sh
toolchain/setup_toolchain.sh Install_Civ4_..._Toolkit.exe PlatformSDK_Svr2003SP1_rtm.img ~/msvc
# prints: export VCTOOLKIT_DIR=... PSDK_DIR=... WINEPREFIX=...
export VCTOOLKIT_DIR=~/msvc/vctk PSDK_DIR=~/msvc/psdk WINEPREFIX=~/msvc/wine32
export BTS_SDK_DIR=/path/to/beyond-the-sword-sdk/CvGameCoreDLL
toolchain/build_dll.sh /path/to/rise-of-mankind/Assets/CvGameCoreDLL /tmp/rom-build 8
# result: /tmp/rom-build/release/CvGameCoreDLL.dll
```

`setup_toolchain.sh` unpacks both packages and adds lower-case aliases for headers
and libraries, because MSVC looks them up case-insensitively. It also creates a 32-bit
Wine prefix. `build_dll.sh` copies the sources to the build folder and runs the
repository's own `GNUmakefile` with `TARGET=release` (`/O2 /Oy /Oi /G7 /MD /GR /Gy
/EHsc`, `/LARGEADDRESSAWARE /OPT:REF /OPT:ICF`) and no `_MOD_*` switches, matching
the shipped DLL. A full build takes about 1.5 minutes with 8 jobs.

Builds are not byte-reproducible: the PE header and the export directory carry
timestamps. To compare two builds, compare exports and section contents. Here, two
builds of equivalent source differed in exactly those 4 bytes.

Under Wine, `cl` can hang after a compile error instead of exiting. Use a timeout
when experimenting with single files.

## clang differential gate

`clang-gate/` type-checks every translation unit with clang in MSVC compatibility
mode, then reports only diagnostics that differ between two source trees:

```sh
export BTS_SDK_DIR=/path/to/beyond-the-sword-sdk/CvGameCoreDLL GATE_WORK=/tmp/rom-gate
toolchain/clang-gate/diffcheck.sh <baseline>/Assets/CvGameCoreDLL <patched>/Assets/CvGameCoreDLL [files.cpp ...]
```

- `mirror.sh` copies the sources and applies semantics-preserving portability edits:
  case-insensitive include aliases, and a token paste that only MSVC accepts.
- `forscope-pass.sh` emulates MSVC 7.1's legacy `for`-scope rule, where a loop
  variable outlives its loop, so old code type-checks as MSVC sees it.
- `check.sh` compiles one file with `-fms-extensions -fms-compatibility` against
  shim headers (`windows.h`, `tchar.h`, …) and the SDK's Boost/Python headers.
- `diffcheck.sh` enables bug-finding warnings (uninitialized values, self-assignment,
  parentheses, non-POD varargs, …). It exits non-zero if the patched tree adds an error.

The gate is a diagnostic aid. MSVC 2003 remains the compiler of record.
