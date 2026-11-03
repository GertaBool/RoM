# Production chains: assessment (R14, M58)

What the mod has today (read from GitLab `d2a8f756`), then the chains proposed from it, the gaps, the new goods and the
files each needs, and the textures. Facts first; proposals are marked as such. Techs are the buildings' own
`PrereqTech`. Nothing here is built yet: the recipes need the recipe mechanism (IN.F1, PR.F3), the quantities need PR.F1.

## 1. What exists

### Buildings that turn goods into goods today
A building that needs inputs present (`PrereqBonuses`) and gives an output as a free resource (`FreeBonus`).
Today this is presence, not quantity: the inputs are not used up.

| Building | Tech | Needs (any of) | Gives |
|---|---|---|---|
| Brewery | Fermentation | Apple, Corn, Rice, Sugar, Wheat | Alcohol |
| Glassblower | Glass Blowing | Salt | Glass |
| Steel Mill | Steel | Iron | Steel |
| Iron Works (national) | Steel | (yield mods Coal, Iron) | Steel |
| Weapon Factory | Explosives | Copper, Iron, Steel | Ammunition |
| Chemical Plant | Refining | Diesel, Oil | Chemicals |
| Fertilizer Plant | Organic Chemistry | Chemicals | Fertilizers |
| Rubber Factory | Refining | Lead, Sulphur | Vulcanized Rubber |
| Biofuel Refinery | Biofuels | Corn, Potato, Sugar | Biofuel |
| Oil Refinery | Refining | none | Diesel |
| Japanese Shale Plant | Thermodynamics | none | Diesel |
| Aluminum Factory | Industrialism | none | Aluminum |
| Cement Mill | Thermodynamics | none | Cement |
| Rubber Plant | Organic Chemistry | none | Synthetic Rubber |
| Silicon Valley, Nano Research, Nanite Lab, Replicator Plant, Research Hospital | modern techs | none | Semiconductors, Nanotubes, Nanobots, Personal Replicators, Smart Medicine |
| Stable | Chariotry | Horse, Ivory | Horse |
| Guildhall (Glass) | Guilds module | none | Glass |
| C/S/V Guildhalls | Guilds, Civil Service, Agricultural Tools | none | Guild paper |

### Buildings that need goods but make none
Bread Manufactory (*Brotmanufaktur*, Manufakturen: Corn, Rice, Wheat; +25 % food), Weapons Manufactory
(*Waffenmanufaktur*, Manufakturen: Copper, Iron), Armourer (Smithing: Copper, Iron), Forge and Iron Forge (Metal
Casting: Copper, Gold, Iron, Lead, Silver), Jewellery (Metal Casting: Amber, Gems, Gold, Pearls, Silver), Cannery
(Nationalism: Aluminum, Iron, Steel; % modifiers on 16 foods), Knight Stable, Tournament, Mongol Ger (Horse, Ivory).

### Guilds (Vincentz Guilds module): the artisan trades, consuming without producing
Carpenters (Timber), Drapers (Sheep, Dye, Cotton, Silk, Fur, Wool, Leather), Fishmongers (Fish, Shrimp, Crab, Clam,
Whale), Masons (Stone, Marble, Obsidian), Blacksmiths (Iron, Lead, Copper), Bakers (Wheat, Corn, Rice, Sugar),
Glassblowers (Salt, Stone, Glass), Mercers (Tea, Coffee, Sugar, Tobacco, Spices), Goldsmiths (Gold, Silver, Gems,
Pearls), Butchers (Cow, Pig, Deer, Sheep), Equestrians (Horse, Leather), Grocers (Apple, Banana, Lemon, Potato, Olives,
Dairy); each also needs Guild paper. Only the Artists Guild produces a good (Drama). Corporations 1-13 (Cereal Mills,
Sushi, Ethanol, Construction, Mining, Aluminum, Jewelers and the mod's 8-13) likewise consume; 3 gives Diesel, 6
Aluminum, 9 Cannabis.

### Improvements that give goods
Farm, Pasture (and Latifundium stages), Camp, Lumber Camp, Lumbermill, Mine, Shaft and Modern Mine, Quarry, Plantation,
Winery, Olive Farm, Apple Farm, Silk Farm, Fishing Boats, Whaling Boats, Well, Offshore Platform, Tree Farm, Windmill,
Watermill, Workshop. Windmill, Watermill and Workshop give no good today.

### What is absent
No granary, mill, bakery, smokehouse, tannery, weaver, sawmill or kiln building exists. No processed food (flour,
bread, cheese, cured meat or fish, dried fruit), no cloth, tools, charcoal, lumber or bricks exist as goods.

## 2. Chains (proposal)

Each step: inputs, the place it happens (an existing building, guild or improvement first; NEW only where none fits),
the output. Buildings marked modifier-only today become real converters.

### Agricultural and food
1. Grain to flour to bread: Wheat, Rice, Corn at a **Watermill or Windmill** (improvements that exist and give nothing)
   or the Cereal Mills corporation later: **Flour** (NEW). Flour at the **Bread Manufactory** (exists, needs grain,
   makes nothing) or the **Bakers Guild**: **Bread** (NEW). Grain kept as seed: the seed share in PR.F1, no separate good.
2. Livestock to meat, hides and milk: Cow, Pig, Sheep, Deer at the **Butchers Guild**: **Meat** (NEW) and Leather
   (exists); milk is Dairy (exists, from pastures).
3. Preserving (D27: keeps longest, adds most to the store): Dairy to **Cheese** (NEW) at the **Grocers Guild**; Meat
   with Salt to **Cured Meat** (NEW) at the Butchers Guild; Fish with Salt to **Cured Fish** (NEW) at the **Fishmongers
   Guild**; Apple, Banana, Lemon, Olives to **Dried Fruit** (NEW) at the Grocers Guild. Later the **Cannery** (exists,
   modifiers only) and Food Processing Plant can all foods into **Canned Food** (NEW).
4. Drink: grain and fruit to Alcohol at the **Brewery** (exists); grapes to Wine at the **Winery** improvement (exists).

### Artisanal
5. Fibre to cloth: Wool, Cotton, Silk at the **Drapers Guild**: **Cloth** (NEW); with Dye, **Fine Cloth** (NEW, luxury).
6. Leather goods: Leather at the **Equestrians Guild**: harness for mounted units (no new good: a unit material, D17).
7. Wood: Timber at the **Carpenters Guild**: building material (exists as Timber); Timber burnt to **Charcoal** (NEW),
   the smiths' fuel before coal (D12).
8. Metal: Iron or Copper with Charcoal (later Coal) at the **Forge** and **Blacksmiths Guild**: **Tools** (NEW); at the
   **Armourer** and **Weapons Manufactory** (both exist, make nothing): **Arms** (NEW, military supply).
9. Stone: Stone, Marble at the **Masons Guild**: building material (no new good).
10. Glass: sand is not a good; the Glassblower and Glass guildhall use Salt today. Proposal: Glass from Stone (as
    silica) with fuel, so salt stays food.
11. Jewellery: Gold, Silver, Gems, Pearls, Amber at the **Jewellery** building and **Goldsmiths Guild**: **Jewellery**
    (NEW, luxury).

### Industrial
12. Steel: Iron with Coal at the **Steel Mill** (needs Iron only today) and Iron Works.
13. Aluminum: Bauxite with energy at the **Aluminum Factory** (needs nothing today).
14. Fuel: Oil at the **Oil Refinery** (needs nothing today): Diesel; Chemicals and Fertilizers follow as today.
15. Cement: Stone with Coal at the **Cement Mill** (needs nothing today).
16. Rubber: Rubber with Sulphur at the **Rubber Factory** (needs Lead and Sulphur, not Rubber, today).
17. Machinery: Steel at the **Factory** (modifier only today): **Machinery** (NEW), the input of mechanised farms (the
    Machine Tools stage of D23) and of vehicles.
18. Textiles and food at scale: Cloth and Canned Food from the Factory and Cannery when the industrial era comes.

## 3. Gaps and inconsistencies found
- Oil Refinery, Aluminum Factory, Cement Mill and Rubber Plant make their goods from nothing.
- Rubber Factory makes Vulcanized Rubber without Rubber.
- Bread Manufactory and Weapons Manufactory need inputs and make no good.
- Glass is made from Salt.
- Glass's button points to `Art/Interface/Buttons/WorldBuilder/Wine.dds`, which is neither loose in the mod nor in
  RoMPak0/1 or RevDCM.FPK: unless the base game has it, Glass shows a missing button.
- Cow, Pig and Sheep are counted in tonnes as food ('other food'), while D15 says the livestock resources stand for the
  breeding stock: a herd is counted in head (Horse already is). With Meat as its own good, Cow, Pig, Sheep would count
  head (category livestock) and Meat would carry the tonnes.

## 4. New goods and the files each needs

Proposed new goods (14): Flour, Bread, Meat, Cheese, Cured Meat, Cured Fish, Dried Fruit, Canned Food, Cloth, Fine
Cloth, Charcoal, Tools, Arms, Jewellery, Machinery (15 with Machinery). Each needs:

| File | Entry |
|---|---|
| `Assets/XML/Terrain/CIV4BonusInfos.xml` | the record: type, description and pedia keys, class (MANUFACTURED or a new class), art define, tech reveal and trade, GoodUnit, GoodCategory, no map placement |
| `Assets/XML/Art/CIV4ArtDefines_Bonus.xml` | the art define: button, FontButtonIndex (free cells from 112), a NIF only if it is placed on the map (none of these are) |
| `Assets/XML/Text/RoM_GameText_*.xml` | name and Civilopedia text |
| `Assets/res/Fonts/GameFont.tga`, `GameFont_75.tga` | a glyph in each, through the font patch (Tools/GameFontPatch), then the icon audits (GW.F2) |
| button DDS | through the art patch, as Timber, Dairy and Leather were |
| `research/economy/plan/proposals.json` | unit, category, sector, roles; `catalogue.json` refreshed |
| the recipe data (IN.F1, PR.F3) | the building or guild that makes it, inputs, output, capacity |

Buildings that become converters change in `Assets/XML/Buildings/CIV4BuildingInfos.xml` (and the Guilds module's
corporation records), through the recipe tags IN.F1 adds; no new building is needed for the chains above, since mills
are improvements and the trades are guilds.

## 5. Textures

Every one of the 77 goods has its own button and its own glyph (audit I2; contact sheet in
`research/economy/plan/goods_art.png`). Findings:
- **Glass** needs a button (its file is missing, see above).
- **Timber, Dairy, Leather, Biofuel, Synthetic Rubber, Smart Medicine**: their glyphs and new buttons are in the font and
  art patch (`Tools/GameFontPatch`), not yet in the branch's font files; they appear once the patch is installed
  (the in-game check LQ.F9.T5 and LQ.F9.T6).
- 38 goods use the base game's atlas icons, which are not in this checkout and could not be looked at here; the rest
  were looked at and show their own good.
- Every new good in section 4 needs a button and two glyphs.

**Seeds and livestock (the assumption tested):**
- Seed grain is grain kept back (the seed share of PR.F1), so wheat, rice and corn seed need no good and no texture.
- Seedlings and cuttings of tree and bush crops (coffee, tea, olives, vines, spices, silkworms) are traded as means of
  production (TR.F3): the trade item can show the crop's own icon with one shared "seed" mark, so no texture per crop.
- Livestock resources are the breeding stock (D15) and already have their own icons: no new texture.
- The exception is **Meat**: once the herd is counted in head, the meat it yields is a separate good and needs its own
  button and glyph.
- Result: the assumption holds for seeds and livestock themselves; it does not hold for the products split off them
  (Meat; Cheese, Cured Meat and the other preserved foods if they become goods).
