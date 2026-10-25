# Coffee processing chain — Rise of Mankind prototype

Coffee plantation → **Coffee Beans** → **Coffee Roastery** → **Roasted Coffee** → domestic consumption and exports.

The plantation resource represents beans already separated from the fruit, dried, hulled and sorted, but not roasted. Commercial roasting, grinding and packaging become a separate manufacturing stage.

## Rules

| Stage | Behavior |
| --- | --- |
| Coffee Beans | Existing `BONUS_COFFEE` ID, map placement, reveal/trade technologies, plantation connections and tile yield preserved. Renamed; direct happiness removed. |
| Coffee Roastery | New normal building. Requires Trade and access to Coffee Beans to construct. Base cost 120, scaled by normal game-speed rules. Supplies 5 tradable copies of Roasted Coffee to its connected trade network. |
| Roasted Coffee | New manufactured resource, `BONUS_ROASTED_COFFEE`. Never placed naturally on the map. Gives +1 happiness for access; duplicate copies do not stack happiness. Spare copies can be exported. |
| Consumer buildings | Existing coffee-based happiness in ports and commercial/urban buildings now uses roasted coffee. Magnitudes unchanged. |
| Commodity trade | Existing coffee yield modifiers, Fair construction eligibility, plantations and raw-material trader/guild inputs still use beans. |
| Optional MoonBean corporation | Its coffee input becomes Roasted Coffee. Other inputs and outputs remain unchanged. The installer skips this module if its file is absent. |

This uses RoM's existing `FreeBonus` manufacturing mechanism, as used by its Brewery and Steel Mill. Five copies are resource availability, NOT five units added to a warehouse every turn. Beans are a construction requirement: **they are not consumed, and losing bean access after construction does not stop output**. Implementing continuous input consumption would require additional game logic and testing; this package does not claim to do that.

The standard AI already evaluates building resource output. This makes the roastery visible to existing AI valuation, but does not demonstrate balanced AI behavior. Costs and output are an initial design, not a measured Marathon optimum.

## Install without editing XML

Requires Python 3. Close Civ IV and choose a **copy** of your Rise of Mankind mod. Use a **new game**, since this adds resource and building indices.

1. Extract the whole ZIP.
2. Double-click `InstallCoffeeChain.pyw` (or run `python install.py`). Select the copied mod's folder, the one containing `Assets`.
3. The installer checks compatibility and shows the destination before you install. It creates a `CoffeeChain-backup-...` folder in that mod.
4. Start the copied mod and open the Civilopedia entries for Coffee Beans, Roasted Coffee and Coffee Roastery.

Command line: `python install.py "path/to/Mods/Rise of Mankind"` checks only. Add `--apply` to install.

To undo: close Civ IV and run `python restore.py "path/to/mod/CoffeeChain-backup-TIMESTAMP"`. It restores original bytes and removes added assets, but refuses to overwrite edits made after installation. Keep the backup folder.

The patch merges selected XML entries and preserves unrelated entries, including the Empire State Building addition. Conflicting edits to affected entries or duplicate identifiers stop installation before any writes. Existing Latin-1 text files keep their declared encoding. This is not an automatic merge of conflicting text revisions.

## Art and text

Includes three distinct original buttons and English, French, German, Italian and Spanish descriptions. The roastery reuses the mod's existing Brewery model and construction sound. Both resource types share the existing coffee GameFont glyph; their names and full buttons distinguish them. No GameFont cell indices or existing resource IDs are shifted, and no fonts are replaced. A unique small glyph and dedicated roastery model can be added separately.

## Verification

See `validation.json`: real-source preflight; manufactured-resource placement and producer links; consumer/commodity separation; source XML child order and encoding; independent DDS decoding; duplicate/conflict refusal; absent optional-module handling; exact rollback; preservation of unrelated edits.

Still to verify in Civ IV: initial construction, five resource copies in the trade network, exports, local disconnection, capture/destruction, Civilopedia/button rendering and AI construction decisions. Check the expected construction-only input behavior explicitly by disconnecting beans after building. No game session or AI balance simulation has been run.

To change the initial tuning without squinting at XML, install into a copy, then open that mod in Civ IV Art Studio's Building Workshop or Resource Workshop and select Coffee Roastery / Roasted Coffee.

The new prose and generated icon artwork may be reused under CC0. XML template portions retain their existing game/mod rights. No extracted game models are included in this download.
