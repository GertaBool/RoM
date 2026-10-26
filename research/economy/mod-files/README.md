# Binary files for the mod branch

The GitLab connector that commits to `aretemaxxing-group/rise-of-mankind` branch `claude/settlement-economy` carries only text, so these binary files come through this repository (request R5). Each sits at the path it takes in the mod: upload it there in the GitLab web IDE, replacing the existing file where there is one.

| Path in the mod | Bytes | SHA-256 |
|---|---|---|
| `Assets/Art/Interface/Buttons/Goods/Biofuel.dds` | 4224 | `d7fcfb102029e0a94cb52a5ac39dae4f27677be27a4f092f3dba3e90f6cca0fb` |
| `Assets/Art/Interface/Buttons/Goods/Dairy.dds` | 4224 | `5bc9b62201e4cc6f6c00964dc4ac3f3869c43f143054c5e7afc4026a81526ba0` |
| `Assets/Art/Interface/Buttons/Goods/Leather.dds` | 4224 | `fc4602c4c98263f1c8ef28c5462686207fc3e4dbecfecba4c045f51c0ce7fe6c` |
| `Assets/Art/Interface/Buttons/Goods/SyntheticRubber.dds` | 4224 | `483670416be559af05164d42f793c72805daffc434360ac743c21f57725dee6b` |
| `Assets/Art/Interface/Buttons/Goods/Timber.dds` | 4224 | `c918afb24603a70713fa128a45de85fdd4688422995e84f708ecb0856e0308a2` |
| `Assets/res/Fonts/GameFont.tga` | 4423698 | `0db290ec792c16c7c75d0078e78672b9e6da5bf5b8c3fe994bc67d475456463f` |
| `Assets/res/Fonts/GameFont_75.tga` | 3768338 | `850cdfc00c0b6f99b6e362412e296ae232a77453d153726d989f5c1e3f0f19a5` |

They are the files `Tools/GameFontPatch/apply_font_patch.py` writes from `Tools/GameFontPatch/font_patch.json` on that branch (fonts: the glyphs of cells 106-111 added to the files at GitLab main 71de0abe; buttons: Timber, Dairy, Leather, Biofuel, Synthetic Rubber). After the upload, running

```
python Tools/GameFontPatch/apply_font_patch.py Tools/GameFontPatch/font_patch.json . --check
```

from the mod folder reports `already applied` for both fonts and `already in place` for each button when every file arrived intact. Sources and licences: `Assets/Art/Interface/Buttons/Goods/ASSETS.json` on the branch.
