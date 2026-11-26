# Build: code map errors

`CvGameCoreDLL.dll`, built from GitLab `main` `ede81881b7de` plus
[`fixes/0022-codemap-errors.patch`](../../fixes/0022-codemap-errors.patch). It serves P14. What the
patch changes and why is in [`fixes/codemap-errors/README.md`](../../fixes/codemap-errors/README.md);
hashes and checks are in [`provenance.json`](provenance.json).

## Install

Into a Rise of Mankind installation at GitLab `main` `ede81881b7de`:

| File | Goes to |
|---|---|
| `CvGameCoreDLL.dll` | `Assets/CvGameCoreDLL.dll` |
| `CIV4BuildingClassInfos.xml` | `Assets/XML/Buildings/CIV4BuildingClassInfos.xml` |
| `CIV4BonusInfos.xml` | `Assets/XML/Terrain/CIV4BonusInfos.xml` |
| `Guildhalls_CIV4BuildingClassInfos.xml` | `Assets/Modules/Projects/Vincentz/Guilds/Guildhalls_CIV4BuildingClassInfos.xml` |

Saves move freely between this DLL and `main`'s: nothing new is saved.

## How it was built

```sh
source ~/msvc/env.sh   # the environment setup script writes it
export BTS_SDK_DIR=~/src/bts-sdk/CvGameCoreDLL
toolchain/build_dll.sh <rise-of-mankind at the patched commit>/Assets/CvGameCoreDLL /tmp/build 8
```

0 errors, 0 warnings. Not tested in the game. The headless check is P14 (pending).
