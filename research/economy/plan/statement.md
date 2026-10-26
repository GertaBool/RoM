# Settlement Economy: production, consumption and trade of goods

## 1. Summary

Resources stop being map tokens that a civilization either has or lacks. They become **goods measured in physical quantities**: tonnes of wheat, dairy and coal, bales of cotton, crates of arms. Each settlement **produces** goods from the land it works, its improvements, its buildings, its specialists and its population. It **consumes** them in proportion to its size and way of life. Surpluses and shortages drive growth, contentment, industry, trade and war. Diplomacy moves from leasing a resource for gold per turn to **real commerce**: shipping goods, selling seeds and breeding stock, and negotiating multi-part contracts.

## 2. Design principles

1. **Physical quantities.** Every good is counted in units that mean something (tonnes, bales, barrels, crates) and is conserved: it is made, moved, stored, used up or spoiled. Nothing appears from nowhere.
2. **Production comes from the whole settlement.** Output combines worked tiles and their improvements, buildings, specialists and available labour. Land sets what is possible; people and capital set how much of it is realised.
3. **Consumption comes from population.** A settlement of a given size needs a plausible amount of food, fuel, clothing and comforts. Needs rise with size and with era.
4. **Industry transforms goods.** Factories turn inputs into outputs at defined rates, and the scarcest input limits the result.
5. **Military power has a material cost.** Units are built from production and goods, and armies in the field use supplies.
6. **Trade carries the goods themselves.** Civilizations exchange goods, the means to produce them (seeds, livestock, techniques), money and treaties, in deals of any shape.
7. **The simulation lives in the DLL.** The game's rules run in the DLL; XML holds the data and Python shows it to the player.

## 3. Core model

### 3.1 Goods
- **A catalogue of goods** defined in XML, each with:
  - its unit;
  - its category: staple food, other food, fuel, raw material, intermediate, finished good, luxury, military supply;
  - its storage limit and how fast it spoils;
  - its base value.
- **Today's resource types become entries in this catalogue.** No good sits on a map plot.

### 3.2 Production
A settlement's output of a good each turn combines:
- **Tiles:** the land's qualities for that good (climate, soil, ore grade, fishing grounds), times the improvement built on the tile.
- **Labour:** citizens working tiles produce raw goods. Specialists produce specific goods or multiply buildings' output, for example a miller, a smith or an engineer.
- **Buildings:**
  - processing (a mill makes flour; a dairy turns milk into cheese and butter);
  - storage (granary, warehouse);
  - industry (foundry, textile mill, arsenal).
- **Technology and policy:** multipliers on yields, and new production methods.

### 3.3 Consumption
- **Needs per citizen,** set by era and by the settlement's level of development:
  - staple food;
  - dietary variety: dairy, meat, fruit, oil;
  - fuel: wood, then coal, then oil;
  - clothing: wool, cotton, linen;
  - comforts and luxuries: coffee, wine, spices, fine goods.
- **Effects of being supplied:** a need that is met adds to growth, health and contentment, with diminishing returns. A shortfall causes hunger, illness, unrest and lost production. Larger settlements need proportionally more, so a single shipment of coffee no longer satisfies an empire.

### 3.4 Storage, spoilage and distribution
- **Stocks** sit in the settlement and are limited by its storage buildings. Perishable goods (fish, dairy, fruit) decay unless preserved.
- **Within a trade network,** surpluses flow to shortages automatically, limited by roads, rivers, ports and harbours. A blockade or a cut road changes what reaches a city.

### 3.5 Industry and unit production
- **Recipes:** buildings convert inputs into outputs at set rates and capacities. For example, 2 iron ore and 1 coal make 2 steel; 1 steel and 1 sulphur make 1 crate of arms.
- **Units** cost production plus goods, such as muskets, horses, steel and fuel. In later eras, armies in the field draw supplies, so industrial capacity and supply lines become part of warfare.

## 4. Trade and diplomacy

### 4.1 What can be traded
| Category | Examples | Nature |
|---|---|---|
| Goods | 50 tonnes of wheat; 10 crates of arms; coffee | Physical: shipped and used up |
| Means of production | Coffee seeds, breeding cattle, silkworms, mining or brewing techniques | Knowledge or stock: the buyer can then produce it |
| Money | Lump sum, instalments | Financial |
| Agreements | Open borders, alliances, rights to fishing grounds, exclusivity clauses | Political |

### 4.2 Deal structures
- **Spot deals:** one shipment, delivered now.
- **Supply contracts:** a quantity per turn for a set term at an agreed price, with penalties for failing to deliver.
- **Packages:** any combination. For example: 20 tonnes of grain per turn for 30 turns, plus coffee seeds, in exchange for iron ore, open borders and a lump sum.
- **Delivery is physical.** Goods travel by land or sea routes. Distance, ports and blockades affect what arrives, and war can break contracts.

### 4.3 How the AI values deals
The AI values a good by its **marginal value**: what one more unit changes in its own settlements' growth, contentment and output. Gold is valued at what it can buy. It also weighs the strategic cost of giving a rival the means to produce a good, for example selling seeds versus selling the harvest. This extends the principle behind the diplomacy change in !63, which values a resource by its effect in the AI's own cities.

### 4.4 Optional: market prices
Prices come from supply and demand among trading partners. That rewards monopolies, specialisation and stockpiling, and lets the player see why a good is valuable.

## 5. Compared with today

| | Today | Proposed |
|---|---|---|
| Resource | A token on one tile; you have it or you don't | A quantity, produced and used up |
| Source | The one tile holding the token | Tiles, improvements, buildings, specialists, labour |
| Demand | None; one copy serves every city | Each settlement uses goods in proportion to its size |
| Luxury | +1 happiness per city, whatever its size | Contentment that grows with supply per head |
| Industry | Buildings need inputs present and use nothing | Buildings convert inputs into outputs |
| Units | Need a resource present | Cost goods; armies use supplies |
| Diplomacy | Lease a resource for gold per turn | Shipments, seeds, contracts, packages |

## 6. Architecture

- **DLL:**
  - the per-settlement goods accounts;
  - production, consumption, spoilage, distribution, recipes;
  - unit costs;
  - new deal item types;
  - AI valuation.
- **XML:** the goods catalogue, needs per citizen, building recipes and capacities, specialist outputs, and unit costs.
- **Python:** the settlement goods screen, trade and contract views, and map overlays of land qualities.
- **The bridge to the existing engine:** a settlement that is supplied with a good also holds the matching resource count. That keeps existing building requirements, the AI and the trade screen working while the new systems are built. I checked in the code that a city's resource count reaches its trade network.

## 7. Decisions to discuss

1. **Scale of units.** Real quantities (tonnes per turn, which carry flavour but need large numbers) or abstract units close to today's yields (easier to balance and to show)?
2. **Food.** Does the current food yield become "tonnes of staple food", with growth driven by the food balance? Or does food stay as it is, with the goods system on top?
3. **Number of goods.** A broad, manageable set (about 25 to 40 goods), or a detailed one (100 or more, closer to Victoria or Anno)? This decides most of the interface and AI work.
4. **Need tiers.** Fixed by era, or by a settlement's development level, with richer settlements wanting more varied goods?
5. **Spoilage and storage.** Included from the start, or later?
6. **Distribution.** Automatic within a trade network (simple), or explicit shipments and routes the player manages (deep, but laborious)?
7. **Contracts and the trade screen.** The diplomacy screen belongs to the executable and knows a fixed set of item types. Do we fit contracts into it (the approach to check first), or build a separate Python trade screen?
8. **Order of work.** Start with goods and consumption inside settlements, then industry, then trade? Or start with trade, since that's where today's game feels most artificial?
