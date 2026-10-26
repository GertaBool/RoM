# Civ IV Art Studio

An offline workshop for **Civilization IV units, buildings, resources, DDS buttons and GameFont symbols**. The browser editor requires no installation or image upload. Native model conversion and animated NIF previews use the included Python desktop helpers (optional).

[Download the ready-to-use ZIP](Civ4ArtStudio.zip?raw=true) · [Standalone HTML](dist/Civ4ArtStudio.html?raw=true)

**Status:** nothing this tool writes has been tried in Civ IV yet. The checks under *Source and tests* test file structure, references within the mod and the browser app, not the game. Install every patch into a copy of the mod and test it there first.

## Start

1. Download and extract `Civ4ArtStudio.zip`.
2. Open `Civ4ArtStudio.html` in a current desktop Chrome, Edge or Firefox browser.
3. Choose a JPG or PNG. Select **Buttons & DDS textures** or **GameFont symbols**.

Everything runs on your device. Images are never sent to a server. Downloads are new files; the program does not write directly into your mod installation. The app and its source are MIT-licensed. It contains no game artwork.

## Make a button

- Choose **64 × 64 — button** for a standard icon.
- Use **Fit entire image**, **Fill & crop**, or **Stretch to fit**. Crop focus controls choose which part stays visible; inset adds breathing room.
- Transparent PNG is best for cutout artwork. For a plain JPG background, enable **Remove a background color** and choose its color and tolerance. This is color keying, not automatic subject detection: matching colors inside the subject are also removed.
- Rounded corners, a solid background and a subtle gold border are optional.
- Export **DXT3 DDS** for compact files or **RGBA DDS** for lossless 8-bit alpha and color. DXT3 uses 4-bit alpha and lossy color compression. The preview shows your prepared artwork before DDS compression.
- Leave mipmaps off for a typical UI button. Turn them on when the specific texture needs them. General textures support square presets or custom power-of-two dimensions from 4 through 2048.

Place the result under your mod, for example:

```text
Assets/Art/Interface/Buttons/Custom/my_button.dds
```

The app provides a direct Button XML value:

```xml
<Button>Art/Interface/Buttons/Custom/my_button.dds</Button>
```

Use the appropriate object or ArtDefine entry. This is a standalone button, not an atlas reference. For model textures, existing NIF material/UV assignments still determine where the image appears; the converter does not make or alter those assignments.

Detail-preserving photo downsampling is enabled by default, with linear-light Lanczos filtering and premultiplied alpha. Use Fill crop, focus controls and Portrait zoom to frame the identifying features; judge the actual-size preview. RGBA is now the default to avoid block-compression losses. DXT3 remains available when compact files matter. Unit and building workshop button exports also use the resampler and RGBA. This preserves available image information; it does not invent detail beyond a 64px button's capacity.

## Make a GameFont symbol

A GameFont sheet is **not** a regular resized image. It contains glyph cells, transparent RGB data and marker pixels that Civ IV uses to find symbols. Work from your mod's existing files:

```text
Assets/res/Fonts/GameFont.tga
Assets/res/Fonts/GameFont_75.tga
```

1. Back up both originals outside the mod folder.
2. Open **GameFont symbols** and load the original full-size TGA.
3. Click the cell already assigned to the symbol you are replacing. You can also use its visual row and column. **Reveal grid & markers** shows the RGB colors stored beneath transparency; uncheck it to view the normal artwork.
4. Adjust the artwork, then click **Apply artwork to selected cell**. Undo is available for each sheet.
5. Load the small font and select its matching symbol **independently**. Its cell size and location can differ. Apply the artwork there too.
6. Download an edited TGA individually, or download both edited sheets and their JSON edit log as a ZIP.
7. Put the edited files in the mod's `Assets/res/Fonts` directory and inspect the relevant symbol in game at both font sizes.

Visual row and column are navigation labels, **not `FontButtonIndex` or Unicode values**. The standalone GameFont tab replaces existing cells and does not create new glyph allocations or rewrite XML. The separate Resource workshop creates matching resource XML and supports explicitly mapped empty slots. Adding a new game object still requires the mod's own index and XML setup. Do not infer a game index from the displayed cell number.

### Font protection

- Detects cells from complete magenta/cyan divider rows and columns; rejects sheets without a detectable grid.
- Requires a true-color 32-bit TGA declaring 8 alpha bits. Uncompressed and RLE input are supported; output is uncompressed 32-bit TGA.
- Preserves dimensions, glyph positions and all original marker pixels, including markers inside a selected cell.
- Avoids introducing exact magenta or cyan marker colors into new artwork by changing the blue component by one level when necessary.
- Before export, checks every pixel outside edited rectangles and every original marker pixel against the original buffer.
- Decodes the exported file again and verifies that all RGBA bytes match the edited buffer.
- Retains the header, image ID and trailing metadata for standard uncompressed 32-bit input. RLE input is decoded and written as uncompressed TGA; optional trailing RLE metadata is not carried over because its byte offsets may no longer be valid.

If the grid cannot be detected reliably, use an intact original sheet. This version has no manual grid rebuilding mode. It does not rebuild the font grid or generate button atlases.

## Resource workshop

Open **Resources & mod patch**, then choose your mod folder (the folder containing `Assets`, or `Assets` itself). The browser may call folder selection an “upload”; this app reads it locally and makes no network requests.

1. Choose **Create a new resource** or **Edit an existing resource**, and select a template. Bauxite is a useful mined-deposit template in Rise of Mankind.
2. Enter a name. New internal identifiers are generated automatically. Existing identifiers stay fixed.
3. Set discovery/trade/obsolete technologies, health, happiness, tile yields, terrain and placement weight. Unexposed rules remain inherited from the template: the form explains latitude, feature and random-placement inheritance.
4. Select connecting improvements, producer buildings, and mandatory unit/building consumers. Existing alternative requirements remain unchanged. Multiple selections use Ctrl/Cmd-click. Existing connections retain their yields; new connections copy the template's improvement entry when available.
5. Choose an existing resource's map model. Optionally load a PNG/JPG for a new 64×64 DXT3 button. Model textures and animations remain in your mod; this tool does not create NIFs.
6. Write the Civilopedia description and optional translations. Missing French/German/Italian/Spanish strings fall back to English, explicitly reported in the patch notes.
7. **Review patch**, then **Download reviewed patch**. Any form change invalidates the review.

The ZIP contains `patch/Assets/...`, exact original-file backups, a SHA256 manifest, a reusable draft and installation/rollback instructions. Copy the **contents of patch/** into a test copy of the mod. Nothing writes into the selected installation. Create one resource per patch, install/test it, then reload the updated folder before producing another patch. Drafts save settings but not artwork; reselect the image after reopening a draft.

Natural resources keep the template's map-generation behavior except for the controls you change. Manufactured resources disable natural placement and require a producer building. The producer uses `FreeBonus` and `iNumFreeBonuses`; this is not an automatic input/output conversion chain. Buildings already producing another resource cannot be reassigned here. Corporation inputs, special Python rules, advanced building modifiers, arbitrary schema editing and save-game migration are outside the form.

### Resource GameFont choices

**Reuse existing symbol** is the default and works without editing either font. A new resource can use its own button/model while sharing an existing text symbol.

**Custom GameFont slot** presents enlarged cells from both sheets. Enter the intended resource index and select matching empty cells independently. The editor checks every resource art definition it finds, including modules, and blocks occupied indices and cells with visible artwork. It protects markers and checks both exported TGAs pixel by pixel. An unreferenced number does **not** prove an unused or valid glyph allocation.

Without an in-game-verified mapping, the ZIP is labelled **TEST ONLY**. Test that resource at both font sizes, plus existing health/happiness/trade and other symbols. Mark the mapping verified only after that check. Draft import deliberately clears verification because the loaded font/DLL may have changed. The editor never infers an index by counting visual cells, expands the font grid, or rewrites DLL offsets. Module load order is not inferred: ambiguous duplicate definitions are blocked, and inactive modules still participate in collision checks.

This is a template editor with structural and reference checks, not a full Civ IV schema validator or a game simulator. Restart the game and use a new map to test additions. Mod-specific map scripts may control placement separately. No in-game test has been performed in this environment.

## Building workshop

Open **Buildings & 3D art** and select your complete mod folder. It shares the folder already loaded in the Resource workshop. The default template in Rise of Mankind is Library; use an ordinary building for ordinary construction, and inspect the **Inherited rules** panel before cloning a special building.

1. Choose **Create building** or **Edit building**, a template, and a display name. A new building gets its own building class and default-building link, rather than replacing an existing civilization's unique building.
2. Set ordinary/national/world/team limits, base production cost, technology, mandatory resource, and buildings required in the same city. Production cost is the unscaled XML value: Marathon applies its game-speed modifiers in game.
3. Set health, happiness, maintenance and defense, flat yields/commerce, and percentage modifiers. Schema-aware insertion puts optional arrays in the appropriate position. Unexposed requirements, empire-wide prerequisite counts, effects and flags stay inherited and are listed for review. Class-limit changes are blocked when they would also change civilization variants.
4. Choose an artwork route below. Art definitions with the same type in different modules are shown as explicit source choices. New art is cloned into its own unique definition; the editor does not guess module load order.
5. Choose a city footprint from your actual `Civ4CityLSystem.xml`, and tune city/Pedia scale. Generic footprints already in that file do not need new L-system entries.
6. Add an optional button image, Civilopedia and strategy text, and translations. Empty translations fall back to English and are reported.
7. Review and download a patch. It includes building XML, class XML when needed, art, text, generated assets, exact backups, checksums, draft and rollback instructions. Install only in a test copy of the same mod snapshot. Reload after installing before preparing another patch.

Buildings do not ordinarily need a GameFont slot. A new building's original template movie is cleared; special Python behavior tied to the old building identifier does not transfer automatically. The editor is not an arbitrary schema editor, full dependency solver or save migration tool.

### Building artwork routes

| What you have | Route | What it produces |
| --- | --- | --- |
| Existing Civ IV building art | Reuse existing model | New art definition referencing the working model, textures and animation |
| PNG/JPEG façade or surface image | Simple box building | Actual static NIF geometry, a diffuse DDS with mipmaps, UV mapping and optional preview-derived button |
| Triangulated OBJ and one texture atlas | Architectural OBJ | Static NIF with positions, normals, UVs, bounds, material and linked diffuse DDS |
| BLEND, FBX, GLB/GLTF or multi-material OBJ | Prepare in Blender first | Triangulated OBJ and a single baked PNG atlas for the browser route |
| CAD, plans or an ordinary photograph | Model/tessellate first, or use the box route | No automatic reconstruction of a detailed building from a photograph or floor plan |

**An image does not describe geometry.** The box is a simple six-sided structure, with the image repeated on four walls and a solid-color roof. It is useful for placeholders and simple buildings, not architectural reconstruction. Existing NIF reuse keeps the original texture assignments; this release does not retarget arbitrary NIF materials.

The OBJ route accepts a single material and requires UV coordinates and triangle faces. It supports negative indices and supplied normals; otherwise it computes face normals. Z-up and Y-up imports and V flipping are explicit controls. Meshes are centered, grounded and normalized to a two-unit horizontal span. Limits: 20 MB OBJ, 20,000 triangles, and fewer than 65,536 exported vertices. OBJ polygons, missing UVs, out-of-range indices, degenerate triangles and multiple materials are rejected rather than silently flattened.

Generated models use standard **Gamebryo NIF 20.0.0.4** with a static mesh and one opaque diffuse material. OBJ texture images are stretched to a square 256/512/1024 atlas without cropping; the box route reserves one quarter of its atlas for the solid roof, encoded as DXT3 with a full mip chain, and linked by an explicit game-relative path. Transparent input pixels are composited over the chosen background. This route does not export animation, skinning, collision, PBR, normal maps, specular/glow maps or alpha-cutout materials. Preserve source images and project files for future edits.

The WebGL preview lets you rotate the mesh and inspect a UV overlay. With no separate button image, its current view is rendered into a 64×64 DDS button. Model generation needs WebGL; model reuse and ordinary image conversion do not. Browser preview lighting is not Civ IV lighting. New-model ZIPs are labelled **MODEL-TEST**: test in-game city and Pedia rendering, scale, UV orientation, different eras/art styles, requirements and effects before deployment.

### Box façade finishes

![Generated brick façade and roof](building-texture-preview.png)

Choose the box artwork route, then select a **Box façade finish**: brick, limestone or timber/plaster. Set floors and weathering; no uploaded façade is required for those presets. Window recesses, mullions, lintels, floor bands, mortar, doors and base staining are painted into the atlas. Choose slate/tile or metal roof courses and a roof color. The live preview and exported mipmapped DDS use the same texture. **Download diffuse texture PNG** also saves the atlas independently. These presets paint the existing box geometry; they do not add physical windows or roof geometry. For an architectural OBJ, supply its own UV-aligned diffuse atlas as before.

Generated details are deterministic. Weathering and contrast are intentionally bounded; inspect both map-scale and Civilopedia views in game, since this release still has no Civ IV renderer. No existing mod texture files are edited in place.

### Prepare architecture in Blender

The downloadable ZIP includes `helpers/prepare_building.py`. Install **Blender 4.x** only if you need this optional preparation step. Run from a terminal, quoting your paths:

```sh
blender --background --python-exit-code 1 --python helpers/prepare_building.py -- "my-building.glb" "prepared-building" --size 512 --triangles 8000
```

Use an empty output directory. The helper reads BLEND, FBX, GLB, GLTF or OBJ, evaluates visible mesh geometry, joins it, simplifies when necessary, triangulates, creates a new UV atlas, and bakes unlit base color to PNG. It exports `building.obj`, `diffuse.png` and `preparation.json`. Source project files are never saved; embedded Blender scripts are disabled when loading a BLEND file. Load the OBJ with **Z up** and the PNG as the diffuse texture in the app.

The helper supports Principled, Diffuse and Emission surface shaders. Mix/group/custom surface graphs require manual baking; geometry, instances and procedural mapping should always be inspected after conversion. It does not interpret CAD or invent geometry from a photograph. Remove interiors and unseen details before processing; decimation is a polygon reduction, not architectural understanding. Open the source in Blender and bake manually when its material setup falls outside these limits.

## Unit workshop

Open **Units & armies** and select the complete mod folder (or reuse the folder loaded by another workshop). Search by name or identifier. The default template is Warrior; choose a template of the same kind as the intended unit, especially for aircraft, ships, workers, transports and special units.

- **Add:** create a separate unlimited unit class available to all civilizations, or a unique replacement within the template's class for selected civilizations. The review names any existing unique unit being replaced. Class-based upgrades resolve to each civilization's corresponding unit.
- **Edit:** change cost, land/air strength, movement, work rate, cargo capacity, withdrawal, city combat modifiers, bombard/collateral effects, draft priority and extra maintenance. Set AI roles, common flags, main/additional technologies, mandatory/alternative resources, city building/religion/corporation requirements, upgrades, free promotions and worker actions.
- **Disable normal recruitment:** sets production cost to -1. It preserves existing units and references. It does not remove existing units or prevent scripted creation; upgrade and event behavior still follows the game rules.
- **Remove:** deletes the unit definition and its exclusive class if unused. References to either ID elsewhere block removal. The Connections panel lists affected files. Shared art and text are retained. Resolve references externally and reload, or disable recruitment instead. No blind cascading deletion is performed.

Use the **Connections and inherited rules** panel before exporting. Civilian actions, cargo restrictions, combat/terrain modifiers, class limits on edits, other special prerequisites, sounds and unexposed settings remain inherited. New standalone classes reset template instance limits; unique replacements retain the existing class limits. Editing a unit does not change its class or civilization assignments. Python and compiled behavior tied to an original identifier is not transferred to a newly named clone.

**Art:** keep the template's mesh groups and early/middle/late era art, or select an existing art definition and change its scale/button. An art definition reuses its NIF, KFM, shader model, sounds and shadow together. Selecting an art source includes its module path to avoid guessing which definition was intended. A JPG/PNG can become a 64px DDS button. For new 3D geometry, use the external reconstruction and desktop companion workflow below. Art replacement assigns the selected definition to all existing mesh groups and era slots, retaining group sizes and formation. For existing units, civilization style overrides are updated by default; unchecking this explicitly preserves them. New unit identifiers do not inherit style overrides keyed to the old identifier. Test movement, attacks and death animations in game: use the native animation preview below to inspect deformation first. There is no manual weight editor. The companion offers experimental automatic weight transfer.

Write names, Civilopedia and strategy in five language tabs. Missing translations fall back to English and appear in the review. Save/resume drafts; image files must be reselected. Changing a field invalidates the prior review.

**Export and install:** download a reviewed ZIP containing `patch/`, exact `backup/` originals, a checksummed manifest, draft and install/rollback instructions. No files in your mod are overwritten by the app. Apply to a copy of the exact loaded mod; compare checksums first and use a new game for structural changes. Test trainability, resource AND/OR logic, civilization availability, upgrades, promotions, artwork and AI behavior. Exported patches are not claimed to have been run in Civ IV.

Removal scans supplied XML, Python, C++/headers, INI/JSON and WorldBuilder files. It cannot inspect compiled DLL references, files outside the selected Assets tree or saves. Module activation/load order is not simulated; ambiguous unit/class definitions are blocked. Prerequisite array limits are checked against supplied GlobalDefines variants conservatively (the smallest declared limit), with conservative defaults if absent. Upgrade cycles returning to the edited class and contradictory AI-role selections are rejected.

### How units connect

`CIV4UnitInfos.xml` links the unit to its class, technologies, resources, buildings, promotions, AI roles, build actions and art mesh groups. `CIV4UnitClassInfos.xml` supplies a default unit and instance limits. `CIV4CivilizationInfos.xml` can replace that default per civilization. `CIV4UnitArtStyleTypeInfos.xml` can override models by unit ID and civilization art style. `CIV4ArtDefines_Unit.xml` connects each art type to NIF/KFM/shader assets, button and sound/shadow settings. GameText supplies localized names and descriptions.

Draft priority is the selection weight used by `CvCity::getConscriptUnit`, not a population cost. `CvCity::getConscriptPopulation` calculates that separately from production cost and `CONSCRIPT_POPULATION_PER_COST`.

Source tracing in this RoM checkout: `CvPlayer::canTrain` checks civilization mapping, cost and player-level prerequisites; `CvCity::isPlotTrainable` checks city building restrictions; `CvPlot::canTrain` handles plot/resource constraints; `CvUnitInfo::read` loads the prerequisite arrays using GlobalDefines capacities. Actual training and scripted spawning can have additional Python/option-dependent rules, so the editor preserves unexposed template fields and exposes the reference scan.

## Model review

Open the new **Model review** tab and select a companion output folder, or its `prepared` subfolder. No mod XML is required. New preparations include `review.json`; older folders must be regenerated.

- Source and prepared meshes share one scale, framing and camera. Rotate, change elevation, zoom, or use the front/side/back presets. Presets assume Blender −Y is forward.
- Clay shading isolates changes to the silhouette and surface. Toggle topology to inspect reduction, or show the converted diffuse atlas on the right. The source materials are not rendered in this view.
- Native 64px thumbnails help judge readability. They do not reproduce Civ IV's camera, lighting or formation scale.
- Findings identify the largest relative triangle reductions and accepted material losses. Expand **All part changes** for the full list and closed-surface diagnostics. A reduction percentage is not a quality score.

The review compares **mesh preparation before rig transfer**. Final NIF skinning, retained donor attachments, animations, team colors and game lighting still require separate validation. Source snapshots are limited to 100,000 triangles / 300,000 vertices; larger sources are explicitly omitted rather than silently downsampled for the comparison. Converted meshes can still be inspected.

This review exposed a real simplification defect: glTF/GLB may contain duplicate vertices along UV/normal seams, and treating those as disconnected faces can produce holes during reduction. Explicit budget mode now reconnects coincident vertices at a small scale/precision-aware tolerance, preserves corner UV data, rejects ambiguous non-manifold joins, and stops if a previously closed part becomes open. Preservation mode does not weld or simplify source geometry. This does not guarantee that aggressive reduction preserves anatomy or visual quality; inspect the result.

## Desktop helpers

These run on your computer with Python (and Blender for some). Install their dependencies once with `python -m pip install -r helpers/unit-model-requirements.txt`.

### Preview a real unit in motion

1. Install Python and the helper dependencies once: `python -m pip install -r helpers/unit-model-requirements.txt`.
2. Open **helpers/UnitAnimationPreview.pyw**, or click **Preview textured NIF + animations** in Unit Model Studio. On Linux/macOS run `python helpers/unit_animation_preview.py`.
3. Select the unit's **NIF**, then select its **KF animation clips** from the list. Clips beside the NIF are found automatically; **Add KF clips** lets you choose clips elsewhere. Set the game's **Assets** folder if textures live elsewhere. Packed FPK assets must first be extracted locally with a compatible tool.
4. Click **Build and open animated unit preview**, choose a new HTML filename, and use **Play/Pause**, the timeline, clip selector, playback speed, orbit, elevation, zoom and part visibility controls. The generated viewer is offline and needs no Python after it has been built.

This displays the actual textured unit mesh, native skin weights, equipment and sampled bone animation. It does not substitute a procedural soldier. To review a newly converted unit, choose its exported **model.nif** and its donor's KF clips. This preview step does not create a new high-quality character: original geometry must come from a finished model or a reconstructed model refined for the intended unit. Shape Lab is retained only as an optional blockout utility.

**Fidelity:** linear quaternion tracks use slerp; ordinary/compressed B-spline transform tracks use cubic sampling; linear/quadratic position and scale curves are supported. Quaternion TBC/quadratic tracks currently use key-to-key slerp, so their easing is approximate; a per-clip message identifies this. Other unsupported transform curves reject the clip. Matching node names are checked, but matching names cannot prove compatible bind poses. The viewer keeps root motion and uses shared bounds across clips.

**Rendering limits:** diffuse textures and normals are previewed. Alpha-bearing materials use a cutout approximation, not full blended/game shader rendering. Team colors, gloss, game lighting, controller-driven visibility/material changes, particles, animation event effects and KFM transitions are not simulated. Events are listed with their times. Model parts can be toggled manually, including alternative meshes present in a NIF. Missing textures and rejected clips remain visible in the report. Test the final result in Civ IV.

Select up to twelve clips, each up to twenty seconds; a combined frame/vertex budget prevents excessive browser memory use. Large models need fewer clips or a lower **Sampling FPS** setting. The tool reads original game files without rewriting them and refuses to overwrite an existing viewer. A generated preview embeds the selected meshes, textures and sampled animation; keep previews private unless you have permission to share that artwork. The download contains the viewer program, **not game artwork**.

Validation includes independently known skinned translations and quaternion rotation, plus a native humanoid's Run/Idle previews, browser playback, scrubbing, clip switching, visibility and source-file integrity. These checks do not establish exact Civ IV rendering or animation parity.

### Image to a new animated unit model (experimental)

The ZIP now includes `helpers/UnitModelStudio.pyw`, a desktop companion. This produces new geometry from a reconstructed model, then transfers a Civ IV donor skeleton's weights. It does not reconstruct a 3D shape inside the browser or convert arbitrary animations to KF.

1. Install Python 3.10+ with Tkinter and Blender 4.x. In the extracted ZIP run `python -m pip install -r helpers/unit-model-requirements.txt`, then `python helpers/unit_model_studio.py` (or double-click UnitModelStudio.pyw).
2. Select your PNG/JPEG. Open Meshy or Tripo using the companion buttons, upload it yourself, and download a textured GLB. Their accounts, charges and upload terms apply. No image is uploaded automatically. Use a separated-limb neutral pose matching your intended donor; one image leaves unseen surfaces to the provider's inference.
3. Select the mod folder and scan donors. Choose an anatomically similar model, its body mesh, and an existing animation pairing. Only loose NIF files are listed; packed game art must first be extracted. A KFM may still depend on the installed base game.
4. Select the downloaded GLB, Blender executable, an empty output folder and the exact new unit ID. Choose orientation, triangle target and texture size, then Prepare. Blender bakes supported base-color materials, preserving geometry unless simplification is explicitly enabled; the converter fits the mesh to donor height, transfers up to four bone influences per vertex and writes partitioned NIF plus mipmapped DDS.
5. Open Art Studio HTML → Units, load the same mod and configure the unit. Under Model, animations and button select **Import a prepared reconstructed model**, then its output folder. Use the matching unit ID. Pick a known animation pairing, review and download the patch.
6. Install into a mod copy and test idle, movement, attacks and death. Automatic weights are experimental: differing poses, silhouettes, hands, equipment and joint placement often need manual weight painting in a compatible NIF toolchain. The native animation preview can inspect exported model.nif with donor KF clips. There is no manual weight editor. Source-mod animation/equipment dependencies remain required.

The converter replaces one selected body mesh. Other meshes are optionally retained; inspect the list for duplicate bodies and attachments. Transparent hair/cards are not preserved by the opaque diffuse bake. This is an initial conversion route, not a guarantee of campaign-ready artwork. Structurally tested with synthetic geometry and a real mod donor; no external reconstruction result or Civ IV rendering has been tested.

Read [the unit art study](UNIT_VISUAL_STUDY.md) before choosing an image-to-model workflow. Shape Lab is a **prototype/blockout tool**, not a finished realistic-character generator. Its simple geometry was the main cause of the toy-like look; texture noise cannot repair proportions, hands, faces, equipment construction or animation contact.

The companion now preserves source geometry unless you check **Reduce geometry to triangle target**. The generic Blender helper requires `--simplify` to apply its target. Simplification retains small mesh objects where possible and writes per-part before/after triangle counts to `prepared/preparation.json`. A unit above the 10,000-triangle exporter limit stops for review rather than silently shrinking to a generic budget. Do not interpret the limit as a recommended game budget.

The opaque bake also stops when it detects transparency or linked normal/bump detail. If you deliberately accept the loss, use the companion checkboxes or the helper's `--allow-alpha-flatten` / `--allow-normal-loss` flags. The report lists accepted losses. Correct alpha-cutout/team-color conversion and full source-shader preservation are still unfinished; a flag cannot recover them. Review the resulting geometry and materials before importing the prepared folder.

### Shape Lab and Motion Lab (prototypes)

Open `helpers/UnitModelStudio.pyw` to find both tools. They work locally; neither requires an image-generation account. See [the internal art pipeline design](INTERNAL_ART_PIPELINE.md) for the implemented scope, limitations and next steps.

**Shape Lab:** choose your Blender executable, then click **Optional blockout utility (not finished unit art)**. In Blender's 3D View, press **N** and select the **Civ IV** sidebar. Change proportions, rest-pose arm angle, armor, helmet, colors, weapon and shield, then **Build / rebuild soldier**. Rebuild replaces the generated parts, so save any manual refinements separately first. Each part is editable Blender geometry. Export a neutral GLB to a new filename and feed it to Unit Model Studio with a matching donor. Start without generated weapons/shields if retaining the donor's equipment, to avoid duplicates. The model is an original stylized base mesh, not an anatomically finished character. Skeleton fitting remains experimental.

**Motion Lab:** click **Edit native KF tracks**. Select the mod, an existing loose KF and an empty export folder outside the mod. Find editable bone tracks; choose a local rotation axis, small amplitude and cycle count. The curve shows the added rotation, not an animated character. Export produces `patch/`, an exact `backup/`, checksums and install instructions. It preserves the original KF filename, so the existing KFM uses it without XML edits. Every unit sharing that KF receives the variation. It does not create an isolated new KFM set.

Motion Lab currently supports LINEAR quaternion rotation tracks. Compressed B-spline, Euler and TBC tracks remain untouched and cannot be selected. It adds a sampled motion layer, with zero added rotation at the sequence boundaries, to the original movement. Other tracks and animation events are preserved. It does not generate a complete walk/attack/death set, solve foot contact, or guarantee compatible transitions. Test in a copy of the mod before using either prototype in a campaign.

Direct launch alternatives:

```sh
blender --python helpers/shape_lab.py
python helpers/motion_lab.py
```

The Blender panel is registered for the current session; rerun the script when reopening Blender. The saved mesh itself does not require the panel. Automated tests exercise Blender generation/render/export, geometry conversion, native KF preservation and the existing browser editor. Desktop window layout has not been manually tested on Windows.

Shape Lab now generates packed diffuse image textures for cloth, steel, etched breastplates, leather, brass, wood and skin. Cloth has weave, folds and contrasting hems; metal has painted highlights, tarnish and an etched motif; leather has pores, seams and edge wear. The new default uses blue cloth, cooler steel and warm brass for separation at map scale. Adjust **Painted material detail**, **Weathering** and the material colors, then rebuild. Existing saved models need rebuilding or manual material reassignment to receive the new surfaces. Export GLB and use Unit Model Studio as before: image textures and UVs survive the Blender bake into the single Civ IV DDS atlas. These are original procedural diffuse details, not downloaded textures or PBR-only effects.

### Resource icons in batch

Three helpers make resource buttons and GameFont glyphs for several goods at once, in the style of the mod's own resource art. They need Python with Pillow, numpy and OpenCV, and Node.js, which runs the studio's own resampler, DDS writer and font replacement (`helpers/core_bridge.js` calls `app/core.js`).

1. **Find the cells.** `python helpers/font_index_map.py /path/to/mod --sheet out/map` detects the glyph grid of both GameFont sheets, takes the resource block (by default the first row of the last group of full rows), and compares every resource button it can read (loose DDS and the mod's FPK archives) with every block cell. It reports how many land on cell = FontButtonIndex against the number expected by chance, the empty cells a new resource can take, and every glyph that more than one resource record shows (records inside XML comments do not count). In Rise of Mankind 13 of 31 buttons match at cell = index, against 0.08 by chance, in both sheets; cells 106 onward were empty. A match count is evidence, not proof: check the result in game.
2. **Make the icons.** Write a spec (JSON) with the mod folder, an output folder and per good its art define, font index, button path, source photograph (title, page, author, licence) and how to take the object: `cutout` (GrabCut inside a crop, or a colour key; `hull` keeps the convex hull, for jars whose white label resembles the background), `fill` (shapes filled with texture from the photo, each with its own crop and shade: log ends cut from a stack, a hide outline filled with leather, a bale from a rubber sheet) or `button` (the object of an existing button, so glyph and button match). Then run `python helpers/goods_batch.py spec.json`. Buttons are 64 x 64 DXT3 with the frame read from the mod's own resource buttons (their median over the outer band). Glyphs fill their cell with a one-pixel margin over a soft dark edge. Only empty cells are written; markers are never touched and every other pixel is checked. The output holds the buttons, both edited sheets, `font_patch.json`, `ASSETS.json` (sources, licences, SHA-256) and `preview.png`, which shows each glyph between its font neighbours at both sizes.
3. **Install the glyphs elsewhere.** `python helpers/apply_font_patch.py font_patch.json Assets/res/Fonts [--check]` writes the same cells into another copy of the fonts using only the standard library. It refuses cells that already hold artwork, backs up each font, verifies the result byte for byte when the fonts are the ones the patch was made from, and reports a second run as already applied. Use it when the edited sheets are too large to carry, for example in a commit made through a web connector.

A new resource glyph appears only if the DLL assigns the symbols as the font expects. In Rise of Mankind, `CvGameTextMgr::assignFontIds` moves the happy, health and other extra symbols by 25 codes once there are more than 73 resource records, unless `WOC_GAMEFONT_RESOURCE_FIX` pins them. Check the number of records before adding one.

### Audit unit art

Audit your own mod's referenced loose unit assets with:

```sh
python helpers/audit_unit_art.py /path/to/mod /path/to/unit-art-audit.json
```

The audit includes optional module definitions and excludes FPK-only/base-game assets. Stored triangles are not necessarily the simultaneously rendered count. No gameplay rendering test was performed for this release.

## Limits and validation

Artwork input is limited to 50 MB and 40 megapixels; a working copy is reduced to a maximum side of 2048 pixels. GameFont input is limited to 80 MB and 16 megapixels. Normal JPEG and PNG formats, including transparent PNG, are decoded by the browser. Broken or unsupported files produce an error.

The app was tested in Chromium with JPG/PNG loading, background keying, DDS and PNG downloads, custom dimensions, GameFont selection, undo and paired font export. An independent Pillow decoder checked DDS colors, alpha and orientation; it also checked both actual Rise of Mankind font files pixel by pixel. No original files were overwritten. No external requests occurred during the browser workflow.

In-game rendering has not been tested. File structure and preservation tests do not verify that you selected the correct semantic symbol or that your mod's XML points to the right artwork. Browser testing in this managed environment used a local HTTP server because its policy restricts `file:` URLs; the standalone file has all scripts embedded and needs no network resources. If your browser disallows local HTML or local workers, serve the folder with a local static server and open it on localhost.

## Source and tests

`app/` holds the readable HTML, UI script and binary-format implementation. `build.py` embeds the scripts into `dist/Civ4ArtStudio.html`. There are no third-party runtime dependencies.

One command runs every check in the order their outputs depend on, and reports each as passed, failed or skipped:

```sh
python tests/run_all.py /path/to/rise-of-mankind
```

It needs Node.js and Python with Pillow, numpy and Playwright (`python -m pip install playwright`, then `python -m playwright install chromium`). The model checks also need PyFFI 2.2.3 and Blender 4.x; without them they are skipped, with the reason. The mod folder can also be given in `CIV4_MOD`; set `CHROMIUM` or `BLENDER` to use a particular browser or Blender (otherwise Playwright's Chromium and `blender` on PATH). `tests/paths.py` holds these lookups. Each check can also run alone with the same mod argument; `run_all.py` shows the order.

`python build.py` rebuilds `dist/Civ4ArtStudio.html`, the download ZIP and `SHA256SUMS.json`; `python build.py --check`, the first check, fails when any of them is out of date with `app/`, `helpers/` or the documents.

The core tests also run without the optional font-directory argument. The resource integration test expects the Rise of Mankind definitions (including Bauxite and Guilds). It copies inputs to ignored test fixtures, generates and inspects patches, and never modifies the supplied mod. Browser tests currently expect the Rise of Mankind font layout (1,301 / 1,325 detected cells). Synthetic fixtures and test outputs are generated under `tests/output/`; game files are read only and are not bundled.

The mod conventions were checked against Rise of Mankind source `2a8b9a83`: existing 64×64 DDS buttons use DXT3 among other formats; `CvGameTextMgr.cpp` assigns game font symbols using category counts and resource `FontButtonIndex`, and `CvBonusInfo::setChar` adds 125 in this mod, confirming that a visual cell position alone is not a sufficient game index.

Building validation includes real mod XML/class/art linking, schema order, wonder limits, backup integrity, OBJ error cases, generated DDS decoding, and repeated edits. NIF output is also checked independently with PyFFI 2.2.3 (a development-only dependency), and the Blender helper was exercised with a synthetic two-material scene in Blender 4.3.2. These checks are not an in-game rendering test.
