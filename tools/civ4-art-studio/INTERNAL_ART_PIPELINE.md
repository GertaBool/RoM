# Internal art tooling for Civilization IV

The aim is a small, controllable art pipeline with a game-specific export contract. High quality means a readable silhouette at normal zoom, intentional materials, stable joints and contacts, and correct combat/death event timing. File validity alone is insufficient.

## Implemented in 1.5

| Tool | Produces | Current boundary |
| --- | --- | --- |
| Shape Lab, a Blender sidebar | Original modular foot-soldier meshes, armor, helmets, equipment, palettes and neutral GLB | Procedural base meshes; no sculpted anatomy, UV painting UI, rig or character animation |
| Unit Model Studio | Baked DDS and donor-skinned NIF from GLB | Experimental nearest-vertex skin-weight transfer; donor body/rest pose must be similar |
| Motion Lab, a desktop form | Native KF rotation variations, patch, backup and checksums | Supported LINEAR quaternion channels only; no complete movement synthesis or animated preview |
| Unit Workshop | Linked unit definitions and art paths with backups | Uses donor animation routing; it does not create a new KFM state machine |

The shape generator is independent of external image reconstruction. It uses parameterized silhouettes and separate parts, so an artist can replace or refine a helmet, boot, breastplate or limb in Blender. A single image can be a reference, but it does not determine unseen geometry or a correct joint layout.

The motion prototype reads actual Civ IV NiControllerSequence files and resolves bone names through their string palettes. It clones the selected transform interpolator, preserves translation/scale channels, samples an additive local-axis rotation, and keeps the original sequence timeline and text-key events. Unsupported channels survive untouched. It neither guesses bone equivalence from similar names nor silently discards compressed motion.

## Design for higher quality — not yet implemented

1. **Donor rig profiles.** Extract joint names, hierarchy, bind matrices, bone lengths, rest pose, attached equipment and known NIF/KFM pairings. Store a profile per validated donor family: upright humanoid, rider, quadruped, wheeled vehicle and ship. Fit mesh parts to those exact joint landmarks before assigning weights. A same-name skeleton is not sufficient evidence of compatibility.
2. **Artist-controlled parts library.** Refine several original heads, hands, torsos, boots and armor styles instead of treating primitive assembly as finished art. Use proportion presets, joint-safe seams, UV atlases, hand-painted color variation and strong light/dark separation. Reference images guide choices and painting. They should not become flat textures stretched over unrelated shapes.
3. **Direct skinning bridge.** Preserve vertex groups authored against the donor profile, export exact weights and bind transforms, then regenerate partitions. Keep nearest-vertex transfer only as an initial fallback. Add heat maps for unweighted vertices, excessive influence distances and likely joint collapse.
4. **Donor-aware animation workspace.** Import/evaluate the full KF set, including compressed interpolators, in a Blender rig with verified axis and transform conventions. Support pose keys, mirrored poses and restrained additive layers. Preserve root-motion conventions and attachment bones. The present curve-only Motion Lab is a first export/preservation test, not that workspace.
5. **Contact and event tools.** Mark stance intervals, lock planted feet with IK, constrain weapon hands, avoid armor penetration, and explicitly place attack, projectile, sound and effect events. Foot sliding, floating weapons and missed hit timing matter more than adding keyframes. Idle, movement, fortify, attack, hurt, death and transition clips need separate checks.
6. **Native export and routing.** Export supported KF channels with measured coordinate fidelity; retain or deliberately rebuild KFM sequence identifiers and transitions. Package an isolated animation set for a new unit instead of modifying a shared KF. Require explicit review when a shared asset affects several unit types.
7. **Visual validation.** Compare neutral poses and selected animation frames against a known source model, render at map and Civilopedia scales, measure silhouette loss after simplification, inspect joint deformation and contact, and run the complete state sequence in Civ IV. Blender renders do not establish engine correctness.

## Acceptance gates

- New shape: original or user-authorized geometry; visible joints; intentional equipment grip; usable silhouette at map zoom; manageable triangle/material/texture budgets.
- Rig: all vertices weighted; normalized weights; compatible partitions; unchanged donor bind transforms unless deliberately retargeted; no detached accessories or collapsed joints during the full motion set.
- Animation: finite normalized quaternions; correct target bones; valid times; required event markers and state transitions; controlled root motion; no visible sliding or contact breakage.
- Packaging: no edits to source assets; exact backups; path and checksum validation; explicit shared-asset scope; rollback instructions.
- Release: structural tests plus visual review plus an in-game animation/state check. Current prototypes pass structural tests only; the model render is an initial shape review.

## Practical next milestone

Choose one upright humanoid donor with its complete loose animation set. Build one refined soldier around that exact rest pose, import its complete KF set for playback, and verify an unchanged NIF/KF round trip before adding full animation authoring. That gives a reproducible quality target for the internal pipeline instead of expanding to many unsupported body types at once.


## Refinement delivered in 1.8

The browser now provides source/prepared clay comparison under a shared scale and camera, optional converted diffuse display, topology overlays, 64px readability thumbnails and per-part reduction findings. This covers the baking/simplification stage only. Native animated NIF comparison, donor-bound skinning review and an in-game quality gate remain open. See the README for the source snapshot limits and seam-aware simplification checks.

## Correction delivered in 1.9

The user requested a proper unit model with animation previews. A procedural blockout and static geometry comparison did not satisfy that requirement. The primary companion action now opens a native textured NIF/KF preview; Shape Lab is a secondary blockout utility. The new preview uses the actual unit mesh, skin weights and animation tracks, supports clip selection and playback/scrubbing, and can inspect converted model.nif files with donor clips.

The implementation samples transforms and skin deformation in Python, embeds diffuse PNG textures and sampled positions/normals in a local HTML viewer, and uses WebGL for playback. No original game files are modified or distributed. Bounds are shared across clips. Unsupported transform tracks reject a clip; omitted visibility/material controllers and approximate TBC/quadratic quaternion easing are disclosed per clip. Alpha uses cutout approximation. No KFM transition, team-color, particle, event-effect or game-renderer parity is claimed.

A proper newly authored character still requires suitable anatomy, costume/equipment geometry, UVs, texture painting and rig weights. The native preview supplies the missing inspection stage; it does not turn the blockout into a finished realistic unit.
