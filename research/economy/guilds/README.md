# The guilds as the XML defines them (R15, M60)

Read from every field of the Vincentz Guilds module's records (GitLab `d2a8f756`,
`Assets/Modules/Projects/Vincentz/Guilds/`). The full field dumps sit beside this file:
`buildings.md`, `building_classes.md`, `corporations.md`, `civics.md`, `units.md`, `unit_classes.md`
(made by `research/economy/plan/tools/xml_fields.py`; list positions: yields 0 food, 1 production, 2 commerce;
commerces 0 gold, 1 research, 2 culture). Sections 1-6 are facts; section 7 is a reading.

## 1. Three grand guild halls (national: `iMaxPlayerInstances` 1)

| Building | Tech | Gives | Yield | Other fields |
|---|---|---|---|---|
| Grand Mastercraftsmens Guild (Crafts Guild Hall) | Guilds | Guild paper (free bonus) | +25 % production | Industrious trait builds it at double speed |
| Grand Mastervictuallers Guild (Victuallers) | Agricultural Tools and Guilds | Guild paper | +25 % food | Expansive trait |
| Grand Masterservants Guild (Servants) | Civil Service and Guilds | Guild paper | +25 % commerce | Organized trait |

All three: `bGovernmentCenter` (a second centre of government, as a palace is for distance maintenance), `bNeverCapture`,
cost 100, `iMaintenanceModifier` 100, culture doubling after 1000 years, obsolete at Machine Tools.

## 2. Fourteen master guilds (world-unique corporation headquarters: `iMaxGlobalInstances` 1)

Each founds its corporation, needs the matching grand hall in the same city, a tech beside Guilds, often two of a
related building in the empire, and is built by a great person (the great people's `Buildings` lists). Each gives
+2 culture that survives obsolescence, +1 gold per city with its guild (`GlobalCorporationCommerce`, headquarter
commerce 1), +1 great-people point of its kind, cost 300.

| Master guild | Grand hall | Tech | Needs 2 of | Built by | Further fields |
|---|---|---|---|---|---|
| Carpenters | Crafts | Engineering | Siege Workshop | Engineer | |
| Masons | Crafts | Architecture | High Walls | Engineer | |
| Blacksmiths | Crafts | Smithing | Forge | Engineer | |
| Glassblowers | Crafts | Optics | none | Engineer | |
| Goldsmiths | Crafts | Clockworks | Jewellery | Artist | |
| Fishmongers | Victuallers | Guilds | Lighthouse | Merchant | free Lighthouse |
| Bakers | Victuallers | Agricultural Tools | none | Merchant | +5 % food per Wheat, Corn, Rice, Potato |
| Mercers | Victuallers | Banking | Market | Merchant | +2 % food per Olives, Wine, Fur, Coffee, Dye, Tea, Tobacco; +5 % per Silk |
| Butchers | Victuallers | Crop Rotation | none | Merchant | +5 % food per Cow, Pig, Sheep; +3 % per Deer |
| Grocers | Victuallers | Usury | none | Engineer | +3 % food per Apple, Olives, Banana, Cotton, Lemon, Spices, Alcohol |
| Drapers | Servants | Heraldry | none | Artist | |
| Artists | Servants | Music | Theatre | Artist | |
| Equestrians | Servants | Stirrup | none | Merchant | |
| Clerks | Servants | Paper | Library | Scientist | |

## 3. The guilds as corporations: inputs and what they give

Each consumes Guild paper and its trade's goods. In the base game's corporation rule a corporation gives its yields
per input resource the city has (value / 100 per resource). Every guild: maintenance 20, spread factor 200, spread cost 20.

| Guild | Inputs beside paper | Gives per input resource |
|---|---|---|
| Carpenters | Timber | +4 production |
| Masons | Stone, Marble, Obsidian | +2 production |
| Blacksmiths | Iron, Lead, Copper | +1 production |
| Glassblowers | Salt, Stone, Glass | +1 production |
| Equestrians | Horse, Leather | +1 production |
| Bakers | Wheat, Corn, Rice, Sugar | +0.5 food |
| Fishmongers | Fish, Shrimp, Crab, Clam, Whale | +0.5 food |
| Butchers | Cow, Pig, Deer, Sheep | +1 food |
| Grocers | Apple, Banana, Lemon, Potato, Olives, Dairy | +1 food |
| Mercers | Tea, Coffee, Sugar, Tobacco, Spices | +2 commerce |
| Drapers | Sheep, Dye, Cotton, Silk, Fur, Wool, Leather | +1 gold, +1 culture |
| Goldsmiths | Gold, Silver, Gems, Pearls | +1 gold, +0.5 culture |
| Clerks | none | +2 gold, +2 research, +2 culture |
| Artists | none | +4 culture; produces Drama |

## 4. Guild halls in member cities (built by the Master units; `PrereqCorporation`)

| Hall | Fields |
|---|---|
| Carpenters | one free specialist per Lumbermill |
| Drapers | +1 happiness; +1 happiness for each of Sheep, Dye, Cotton, Silk, Fur, Wool, Leather; +5 % enemy war weariness |
| Masons | +20 % defence, +20 bombard defence; +10 % production per Stone and Marble, +5 % per Obsidian |
| Blacksmiths | +20 % production of land units |
| Artists | free Artist; +2 happiness; -20 % war weariness |
| Glassblowers | free Glass; +10 % production per Wine and Alcohol, +5 % per Glass |
| Goldsmiths | +5 % golden age length; +20 % trade route yield |
| Equestrians | free Horse; units built get the Mobility promotion |
| Clerks | free Scientist; +25 % espionage defence; Scientists +1 yield |

The building classes of the Fishmongers, Bakers, Mercers, Butchers and Grocers halls exist, but no building records
for them do (`Guildhalls_CIV4BuildingInfos.xml` holds 9 records for 14 classes).

## 5. Master units

Fourteen Master units (Master Carpenter ... Master Clerk): `SPECIALUNIT_PEOPLE`, missionary AI, cost 100, 2 moves,
at most 3 per player, spread their guild (40) and build its hall in the target city, need the master guild and the
corporation; they upgrade to Freight.

## 6. The Guilds civic (economy)

Guilds tech; medium upkeep; anarchy 1; no foreign corporations; -20 % corporation maintenance; +15 % distance
maintenance; +3 health; +25 % worker speed; +50 % improvement upgrade rate; +1 trade route; +30 % trade route food
(yield position 0); +20 % culture; Engineer specialists allowed; Revolution: nationality and distance indices +0.05,
environmental protection 1.

## 7. Reading: the role the guilds already have

- **They are an institutional layer, not workshops.** The grand halls are national institutions (one per player,
  government centres, +25 % to one yield). The master guilds are world-unique headquarters founded by great people,
  and the guilds spread to member cities through Master units.
- **They turn the trade goods a player owns into yields:** production for the building trades (carpenters, masons,
  smiths, glassblowers, equestrians), food for the victualling trades (bakers, fishmongers, butchers, grocers), and
  commerce and culture for the servant trades (mercers, drapers, goldsmiths, clerks, artists). Their halls add
  specialists, defence, unit production and promotions, happiness and trade.
- **The Guilds civic** closes the economy to foreign corporations and favours workers, improvements and trade.
- **In the goods economy (proposal, for the decision):** keep this role and turn it from presence to quantity. A
  guild in a city raises the output and quality of that city's own production in its trade, for example more bread
  per tonne of grain, cloth from fewer bales, tools from less ore. It consumes its trade's goods as it does now, and
  it keeps its specialists, halls and civic. The city makes the goods; the guild makes the trade better. This fits
  M59: an important role, not the source of goods.
- **"National rather than world wonders" (M59) against these facts:** the three grand halls are already national;
  the 14 master guilds are the world-unique headquarters. Making the master guilds national would let every player
  found every guild, so each guild becomes a domestic institution rather than a race between players.
