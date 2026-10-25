# Empire State Building — Rise of Mankind wonder prototype

An original, stylized low-poly building: limestone window bays, vertical Art Deco piers, stepped podium, crown and spire. Includes an actual static NIF model, mipmapped DDS texture, 64px DDS button, linked building/class/art definitions, and Civilopedia text in English, French, German, Italian and Spanish. No GameFont changes or DLL required. There is no wonder movie.

## Proposed gameplay

World wonder, one globally. Base production cost: 1400; the game's speed modifiers apply automatically, including Marathon. Requires Civil Engineering, Physics and Steel technologies, and access to Cement AND Steel resources. Effects in its city: +25% gold, +2 trade routes, +6 culture, +2 Great Merchant points. No free buildings or inherited Skyscraper food/production yields. AI uses existing building evaluation and FLAVOR_GOLD; balance and AI performance have not been measured.

## Installation

Use a COPY of the Rise of Mankind mod and start a NEW GAME. Do not use an existing save to assess a new building/class index. Close Civ IV before changing files.

1. Extract this entire ZIP.
2. Run `python install.py "C:/path/to/Mods/Rise of Mankind"` to check compatibility without writing.
3. Run the same command with `--apply` to install. The installer validates every target before writing, refuses changed source XML or asset collisions, and creates a timestamped backup inside the copied mod.
4. Launch the copied mod. Check the Civilopedia entry, then place the wonder through WorldBuilder and inspect city appearance at different zoom levels. Verify effects in the city screen and test normal construction prerequisites. Check another civilization cannot build a second instance.
5. To undo, close the game and run `python restore.py "C:/path/to/mod/EmpireState-backup-TIMESTAMP"`. Restore refuses files edited after installation.

The installer intentionally requires the exact source XML hashes in manifest.json. If your files differ, do not force an overwrite: merge the three small definitions into your current version using the Building Workshop or a proper XML merge. Generated asset paths are listed in the manifest.

## Validation and limitations

The model is 456 triangles with UV coordinates and an external texture link, NIF 20.0.0.4. This package is a MODEL TEST prototype. Independent NIF parsing, DDS decoding, XML linkage/schema-order checks and installation/rollback are checked during packaging. It has NOT been rendered or played inside Civilization IV. Scale and lighting may need adjustment in CIV4ArtDefines_Building.xml (`fScale` / `fInterfaceScale`). The preview is a Blender render, not an in-game screenshot. This simplified silhouette is not a surveyed architectural reconstruction. No animation, collision mesh, night lighting or wonder movie.

Source assets and the original model-generation script are included. The generated geometry, textures and new prose may be reused under CC0; the XML template portions retain the source game's/mod's rights. No third-party photographs or extracted game models are included.

The NIF coordinates are 20 times the supplied OBJ coordinates (40-unit footprint, approximately 120-unit height), before XML art scaling. To rebuild the Blender preview, run source/model.py using Blender with Pillow available. The OBJ and diffuse PNG can also be imported into the Art Studio Building Workshop.
