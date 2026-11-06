# Art sources for the blocked buttons (R28.1, M74)

**Why other sources.** Wikimedia Commons and Flickr's image servers refuse this container: `live.staticflickr.com`
answers HTTP 429 "Rate limited - CIDR range blocked", and Commons answered 429 earlier (LQ.F10.T2 note). Pexels
(403) and Unsplash (a bot check) refuse it as well.

**What was reachable:**

| Source | Licence | What it gave |
|---|---|---|
| Openverse API | per image (CC0, public domain, CC BY) | search across sources |
| WordPress Photo Directory | CC0 | a few log piles, but in town settings, not forest scenes |
| Library of Congress (`loc.gov`, `tile.loc.gov`) | the Carol M. Highsmith Archive is public domain (her gift to the public) | high-quality colour photographs of American scenes |
| Cleveland Museum of Art Open Access API | CC0 | museum photographs of historic glass |

## Chosen files (copies in `research/economy/art_sources/`)

| Use | File | Source | Licence | SHA-256 |
|---|---|---|---|---|
| Lumber camp build button (LQ.F10.T2): a log stack with forested hills, a scene as the build buttons are | `loc_highsmith_50533_logs_mapleton.jpg` (1024 × 683) | Carol M. Highsmith, "Logs piled high at a lumberyard near Mapleton, Oregon", Library of Congress, https://www.loc.gov/item/2018698735/ | public domain | 344b1f10a3d7f639811b551c1e8f1b01b565fa3e74bd19f9ac4379782c29db8b |
| Glass resource button, first choice: a clear Venetian glass beaker, about 1490-1500. Murano is the glassmakers' guild of D29; the object is isolated on a neutral ground, as the resource buttons are | `cma_1950.573.a_venetian_beaker.jpg` (716 × 900) | Cleveland Museum of Art 1950.573.a, Beaker, Italy, Venice, c. 1490-1500, https://www.clevelandart.org/art/1950.573.a | CC0 | b29ed123d4121ef2f8f33484b686e262f6643817797eae223e4c7503d3044163 |
| Glass, alternative: Roman blue-green ribbed bowl, 50 BCE-100 CE | `cma_1959.250_roman_ribbed_bowl.jpg` (1263 × 646) | Cleveland Museum of Art 1959.250 | CC0 | 5a2d7b83d280c3cd498f6a72b542736bbad9401dc24eb731e064860b85f6a2a7 |
| Glass, alternative: green bottle, Iran, 800s-900s | `cma_1951.290_iranian_bottle.jpg` (804 × 893) | Cleveland Museum of Art 1951.290 | CC0 | b20e0492d35c3fb2cfcd3987a1bc7a50fc9e99dddfa9eedb8b51cdd542890b01 |

**Rejected:**
- the Chihuly and Museum of Glass photographs (Highsmith): the photographs are public domain, but the glass artworks
  in them are modern works under copyright;
- the urban log piles from the WordPress directory: not a forest scene.

## Next (LQ.F10.T2 and the Glass button)

- **The lumber camp button** needs the build-button frame: a scene filling the tile under a thin light rim, with the
  rim from the median outer band of the mod's build buttons. It needs a small helper beside `goods_batch.py`, as
  the task note plans.
- **The Glass button** uses the existing resource-button path (`goods_batch.py`, the object cut out inside the shared
  frame).
- Both are added to the art patch, not written over it.
