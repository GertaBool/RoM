# Diplomacy: trade values from effects, offers by value

**Status: built and tested headless, not yet in the game.** This DLL is GitLab `main` `3bec049` plus
[`fixes/diplomacy-values.patch`](../../fixes/diplomacy-values.patch) (build `c123133807f4`). It
contains everything in [`builds/graphics-paging-interface`](../graphics-paging-interface/README.md).

## What changes

The AI no longer picks the techs and resources it asks for at random, and it values them by what
they do for it:
- **Techs** at the research they would really cost it, after tech diffusion and known
  prerequisites.
- **Resources** by their effect in its own cities:
  - happiness and health where a city is short of them;
  - building yield bonuses on the city's real production and commerce (Town Essentials with
    Coffee, a Forge with Gold, a Market's or Library's bonus on top);
  - the units and buildings they unlock.
- **When you ask for a resource,** the deal must cover what its cities lose.
- **Offers:**
  - it asks for the tech it is researching or about to;
  - it gives the tech closest in value;
  - it swaps resources only when it gains more than it loses;
  - it sells no tech to a player ranked above it.
- **Gold:** a tech purchase it proposes keeps its gold reserve.

Each part is a bit of `AI_DIPLOMACY_FLAGS` in `BBAI_AI_Variables_GlobalDefines.xml` (default 15).
0 restores the old AI.

## Install

Copy into `Mods/Rise of Mankind/`:

| File here | Goes to |
|---|---|
| `CvGameCoreDLL.dll` | `Assets/CvGameCoreDLL.dll` |
| `BBAI_AI_Variables_GlobalDefines.xml` | `Assets/XML/BBAI_AI_Variables_GlobalDefines.xml` |

If you have not installed `builds/graphics-paging-interface`, also delete
`Assets/Python/EntryPoints/CvGameInterface.py` (see its README).

Saves move freely between this DLL and the earlier ones.

## What to look for in a game

- AIs pay for techs they need, not random ones, and keep some gold.
- An AI refuses to give you a resource its cities need, and offers gold per turn for a luxury when
  its cities are unhappy.
- Diplomacy lines in `WarLog.log` (`D`, `E`) record every deal, so a logged game can be compared
  with games 1 to 4.
