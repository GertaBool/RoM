# Civ IV Art Studio

An offline image converter for **Civilization IV buttons and GameFont symbols**. No installation, Photoshop plugin, Python runtime or image upload is required to use the app.

[Download the ready-to-use ZIP](Civ4ArtStudio.zip?raw=true) · [Standalone HTML](dist/Civ4ArtStudio.html?raw=true)

![Button conversion preview](preview.png)

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

Visual row and column are navigation labels, **not `FontButtonIndex` or Unicode values**. The app replaces existing cells and does not create new glyph allocations, adjust resource/religion counts, or rewrite XML. Adding a new game object still requires the mod's own index and XML setup. Do not infer a game index from the displayed cell number.

### Font protection

- Detects cells from complete magenta/cyan divider rows and columns; rejects sheets without a detectable grid.
- Requires a true-color 32-bit TGA declaring 8 alpha bits. Uncompressed and RLE input are supported; output is uncompressed 32-bit TGA.
- Preserves dimensions, glyph positions and all original marker pixels, including markers inside a selected cell.
- Avoids introducing exact magenta or cyan marker colors into new artwork by changing the blue component by one level when necessary.
- Before export, checks every pixel outside edited rectangles and every original marker pixel against the original buffer.
- Decodes the exported file again and verifies that all RGBA bytes match the edited buffer.
- Retains the header, image ID and trailing metadata for standard uncompressed 32-bit input. RLE input is decoded and written as uncompressed TGA; optional trailing RLE metadata is not carried over because its byte offsets may no longer be valid.

If the grid cannot be detected reliably, use an intact original sheet. This version has no manual grid rebuilding mode. It is not a font-index editor or an atlas generator.

## Limits and validation

Artwork input is limited to 50 MB and 40 megapixels; a working copy is reduced to a maximum side of 2048 pixels. GameFont input is limited to 80 MB and 16 megapixels. Normal JPEG and PNG formats, including transparent PNG, are decoded by the browser. Broken or unsupported files produce an error.

The app was tested in Chromium with JPG/PNG loading, background keying, DDS and PNG downloads, custom dimensions, GameFont selection, undo and paired font export. An independent Pillow decoder checked DDS colors, alpha and orientation; it also checked both actual Rise of Mankind font files pixel by pixel. No original files were overwritten. No external requests occurred during the browser workflow.

In-game rendering has not been tested. File structure and preservation tests do not verify that you selected the correct semantic symbol or that your mod's XML points to the right artwork. Browser testing in this managed environment used a local HTTP server because its policy restricts `file:` URLs; the standalone file has all scripts embedded and needs no network resources. If your browser disallows local HTML or local workers, serve the folder with a local static server and open it on localhost.

## Source and tests

`app/` holds the readable HTML, UI script and binary-format implementation. `build.py` embeds both scripts into `dist/Civ4ArtStudio.html`. There are no third-party runtime dependencies.

Developer checks require Node.js, Python with Pillow, and optionally Playwright with Chromium:

```sh
python build.py
node tests/test_core.js /path/to/mod/Assets/res/Fonts
python tests/check_formats.py /path/to/mod/Assets/res/Fonts
python tests/browser_check.py /path/to/mod/Assets/res/Fonts
```

The core tests also run without the optional font-directory argument. Browser tests currently expect the Rise of Mankind font layout (1,301 / 1,325 detected cells). Synthetic fixtures and test outputs are generated under `tests/output/`; game files are read only and are not bundled.

The mod conventions were checked against Rise of Mankind source `2a8b9a83`: existing 64×64 DDS buttons use DXT3 among other formats; `CvGameTextMgr.cpp` assigns game font symbols using category counts and resource `FontButtonIndex`, confirming that a visual cell position alone is not a sufficient game index.
