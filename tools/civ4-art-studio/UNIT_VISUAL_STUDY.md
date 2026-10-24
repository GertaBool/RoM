# Realistic unit art: findings and conversion changes

## What was inspected

This study reads Rise of Mankind's actual UnitArtInfo records, referenced loose NIF geometry and diffuse DDS images. It includes optional modules and excludes assets available only in base-game/FPK archives. It is an asset study, **not an in-game rendering test**. No running Civ IV renderer or gameplay screenshots were available here, so camera scale, lighting, active LODs and animation appearance remain unverified.

The reproducible scanner is `helpers/audit_unit_art.py`. Run it with the mod folder and an output JSON path after installing the companion dependencies. Source revision and scope are recorded in the release validation metadata.

The scan found 185 qualifying art definitions referencing 168 distinct loose NIFs; all parsed. It resolved 441 unique referenced diffuse images. Of those, 293 are 128×128, 74 are 64×64, and 46 are 256×256. The remainder use other sizes. The median **stored** triangle count is 876; this can include alternate meshes and must not be treated as a live draw-call budget. Alpha properties occur in 166 models, and 232 resolved diffuse images have some non-opaque alpha. Alpha properties can be disabled, and texture alpha may encode team color or other information: these figures do not mean every such mesh is transparent.

| Referenced unit art | Stored triangles | Relevant observation |
| --- | ---: | --- |
| Indian Archer | 732 | Distinct arrows, quiver and body meshes; thin equipment carries identity |
| Indian Rifleman | 771 | Head/hat/equipment pieces and a separate body; body texture references include 128² and 256² images |
| Indian Infantry | 766 | Several small pieces accompany a 586-triangle body mesh |
| Celtic Heavy Footman | 833 | Body and shield/cape textures are separately authored |
| Frankish Swordsman | 1,026 | Distinct body and shield textures |
| Indian Pikeman | 1,032 | Polearm pieces contribute to a specific silhouette |
| Indian Knight | 1,338 | Rider/equipment and mount-related pieces have different roles |
| Indian Chariot | 1,484 | Horse, harness, vehicle/rider pieces; a humanoid-only rig/shape is inadequate |
| Asian Machine Gun | 1,554 | Stored geometry includes two substantial body meshes plus gun/equipment parts; do not assume all are shown together |

Examples resolve through `Assets/XML/Art/CIV4ArtDefines_Unit.xml` and the corresponding modular art definitions. Concrete assets include `Assets/art/units/Specials/Celtic Heavy Footman/celtichvyfootman.nif`, `Assets/art/units/Swordsman/Swordsman_German/frankishswordsman.nif`, and the Indian art folders under `Assets/Modules/Custom ArtStyles/India/`.

## Why the prototype looked like a toy

The procedural soldier was assembled from rounded joints, simple limb sections, a broad rigid breastplate, mitten-like hands and a minimally described face. Adding a fabric pattern does not change those shapes or provide historically specific construction. It also uses more geometry than several complete game assets listed above. More polygons and larger textures are therefore not, by themselves, a solution.

Direct inspection of the Frankish, Celtic heavy-footman and infantry diffuse maps shows deliberately placed faces, eyes/hair or helmets, clothing boundaries, belts, boots and patterned equipment. A horse atlas likewise puts recognizable facial and equipment detail in specific UV regions. These are semantic details painted for a particular mesh, not uniform noise added over a generic body. Such decisions explain more of the visual difference than texture resolution alone; the final comparison still needs in-game validation.

The appropriate target is historically grounded art consistent with the mod's visual treatment. A raw photograph, an oversharpened texture or an arbitrary gold ornament does not automatically fit that target.

## Conversion changes implemented

- **Preserve geometry by default.** The Blender helper no longer silently decimates a model to the triangle target. Explicit budget mode reduces separate mesh objects before joining them, retains small pieces where the budget permits, and reports before/after counts for each part. It cannot identify a face or fingers inside a single combined mesh. The unit exporter still has its 10,000-triangle structural limit; exceeding it produces an actionable stop rather than silent simplification.
- **Make material losses explicit.** The current bake is an opaque base-color export. It now stops on linked normal/bump inputs or transparency unless the user explicitly accepts those losses. Accepted losses are listed in the preparation report. This is not native alpha-cutout, team-color or normal-map support, and it cannot prove that a source material is visually equivalent in Civ IV.
- **Preserve button information.** Linear-light Lanczos resampling uses premultiplied alpha to avoid transparent-color fringes. Portrait zoom complements the existing crop focus controls. Standalone buttons default to uncompressed RGBA; workshop-generated unit/building buttons also use RGBA. DXT3 remains an explicit compact option. GameFont handling remains separate.
- **Keep the procedural soldier in its proper role.** Shape Lab is labeled a prototype/blockout route. It is not the recommended source of finished realistic troops. Better textures do not remove the need for a well-designed source mesh and a donor-compatible rest pose.

## Working standard for realistic assets

1. Choose a specific unit and era, with useful front, side and equipment references. Prefer a neutral full-body reference for reconstruction and a separate composition for the UI button. A single picture cannot establish hidden surfaces, depth or exact anatomy.
2. Match the donor's body plan, joint positions, grip and rest pose. Preserve a coherent torso, shoulder/hip transitions, hands and feet; avoid a chain of rounded primitives. Mounted units require rider, mount, reins and contact points to be designed together.
3. Preserve the unit's identifying silhouette: headgear, weapon length and grip, shield outline, clothing cut and carriage. Keep historically meaningful asymmetry. Review detached or fused straps, fingers and weapon parts in AI-generated meshes.
4. Use UV space deliberately. Faces, hands and identifying equipment deserve readable detail. Place folds and seams where the mesh and costume justify them. Keep fine weave, scratches and weathering subordinate to shape and material separation.
5. Compare source and export in neutral lighting, from the front, side and back, at both Civilopedia and map sizes. Check actual native-size buttons. Do not use a flattering high-resolution render as the only quality gate.
6. Run idle, movement, attacks, fortify, hurt and death in Civ IV. Look for sliding feet, broken grips, armor clipping, distorted faces, team-color errors and mismatched event timing. Match the surrounding unit set, not just the isolated model.

## Still needed for a production-quality pipeline

Exact donor-profile fitting, direct export of authored skin weights, full native animation playback, alpha/team-color-aware material conversion, high-to-low baking of relevant surface detail, and source/export visual comparison remain unfinished. The new guards prevent some silent losses; they do not generate anatomically correct models or guarantee flawless immersion. The next useful benchmark is one convincingly finished, donor-matched unit evaluated beside existing units in the actual game.
