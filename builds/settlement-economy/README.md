# Settlement economy test build

This DLL goes with the GitLab branch `claude/settlement-economy` (at `9a5795e9`), a separate testing branch of
Rise of Mankind for the settlement economy. The branch's own `Assets/CvGameCoreDLL.dll` is still GitLab `main`'s:
the connector that writes the branch cannot carry a binary, so the DLL is kept here. Without it the branch's XML
loads, but lumber camps, lumbermills, pastures and latifundia give no goods.

## What it adds to the branch

- **Improvements can give goods.** An improvement record may list goods it gives to the trade network
  (`ProducedBonuses`), each optionally only on a plot with a given resource. The goods count like a resource under
  the improvement: the plot must be connected (road, river, coast), the good's trade tech known.
- **Lumber camp** (Metal Casting, on forest, keeps the forest): gives Timber; no base yield, +1 production at each of
  Bronze Working, Iron Working and Mathematics. The **lumbermill** (Machinery) gives Timber too and now 5 production.
  Timber trades from Metal Casting.
- **Pastures and every Latifundium stage** give every product of their animal: sheep Wool, Dairy and Leather; cows
  Dairy and Leather; horses Leather; pigs nothing more. Wool trades from Animal Husbandry.
- **Hunting camps** on sheep, cows and horses give Leather (no Wool or Dairy).
- The AI's workers value a good a city lacks when they choose an improvement; the improvement's help lists its goods.
- Resource records may carry a goods unit and category (`GoodUnit`, `GoodCategory`); none does yet and nothing in
  the game uses them.

## Setup

1. Check out the GitLab branch `claude/settlement-economy` as the mod.
2. Copy `CvGameCoreDLL.dll` from this folder over `Assets/CvGameCoreDLL.dll` of that checkout (back up the old one).
3. Start a new game. Saves from other builds may not load correctly.

`provenance.json` names the source commit, the build id (`e7da41335d50`) and the DLL's hash.

## What to look at

- A lumber camp's help shows "Provides Timber to the trade network"; a connected camp gives its cities Timber
  (the resource bar and the city screen show it).
- A pasture on sheep gives Sheep, Wool, Dairy and Leather.
- Report anything odd: goods that stay after a camp or pasture is pillaged or replaced, missing art, or a crash.
