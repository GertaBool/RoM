# Migration, clothing, guilds, research by buildings, Masons and Clerks (R30, M76)

The population model with its mathematics and edge cases is in `pop_model_math.md` (R30.1). This file covers the
rest of M76.

## 1. Recorded as decided (M76)

**Migration:**
- Migration gets a parameter in the civics, examined civic by civic.
- Cities grow beyond their own births only through migration.
- Skills, culture and burdens move with the people who migrate.

**Clothing:**
- It is both warmth (by climate) and status.
- The goods are the base fibres and skins (Wool, Leather, Cotton, Fur, Silk, hemp, Dye, and Flax, which is added),
  then Cloth and Fine Cloth, then coats and full dresses. Modern clothing is a kind of coat or dress.
- Dress depends on technology, resources, tools, machines, skilled labour, and on religiosity and culture: diversity,
  secularization, open or closed markets, free or censored media.

**Guilds:**
- The food guilds raise the quality of their goods, give employment and protect local industry.
- Their masterwork goods trade higher, perish slower and add to health and strength.
- Their real gain is education: adjacent technologies become cheaper.
- That becomes a new XML field for all buildings and wonders; the Lighthouse and the Colossus, for example, would
  make maritime technologies cheaper.

## 2. Migration

### 2a. Facts

- **Ravenstein (1885):** most migrants move short distances, often in steps, and every stream has a counter-stream.
- **The gravity model** (Zipf 1946, Stewart 1948): flows grow with the populations of origin and destination and fall
  with distance.
- **Lee (1966):** push factors at the origin, pull factors at the destination, obstacles between them, and the
  migrant's own traits.
- **Harris and Todaro (1970):** migrants respond to expected income, the wage times the chance of finding work.
  Migration continues until expected incomes are equal, even with urban unemployment.
- **Cities were demographic sinks.** They needed migrants to grow; London needed about 8,000 a year around 1700
  (Wrigley). See `pop_model_math.md` cases 5-6.
- **Skills move with people.** About 16,000-20,000 Huguenots came to Brandenburg-Prussia after 1685, on average more
  skilled than the natives. They raised textile productivity in the towns they settled for more than a century,
  through direct transfer of knowledge (Hornung 2014, *AER*). From 1686, unskilled Huguenots were refused.
- **The engine already has relevant pieces:**
  - tech diffusion through contact and open borders (`CvPlayer::calculateResearchModifier`, BBAI);
  - the Revolution mod's nationality index (`fRevIdxNationalityMod` on civics);
  - city culture per player.

### 2b. Proposal: the flow between two connected cities

Yearly flow from city `i` to city `j`:

```
m(i→j) = μ × N(i) × max(0, A(j) − A(i)) × exp(−d(i,j) ÷ d0) × permeability
```

- **`A`, a city's attractiveness:** food per head (`x`), expected income (wage × chance of work, Harris-Todaro),
  health, safety, and religious and cultural affinity, minus crowding.
- **`d`:** distance along the trade network (roads, rivers, sea), as the gravity model.
- **Permeability:**
  - within one player: the owner's **internal mobility** (civics, 2c);
  - between players: the origin's **emigration** × the destination's **immigration** × open borders;
  - refugees from war or famine move on push alone: the origin's emigration rule does not stop them, the
    destination's immigration rule does.
- **`μ`:** the base share. An *estimate* of 1 % of people a year per unit of attractiveness gap, with a cap on
  departures per year.

**What migrants carry:**
- **Skills:** the share of craftsmen, workshop people and the educated in the origin's people (the Huguenot case).
- **Culture:** the origin owner's culture added to the destination's plots, through the city culture per player.
- **Religion:** spread with them.
- **Burden:** a grievance when the destination's owner has made war on the origin, for example nuclear attacks. It
  enters the Revolution indices (nationality) and unhappiness in proportion to the migrants, fading over
  generations.
- **The two edges you named both follow from these rules:** skilled people leaving an overcrowded homeland for rural
  lands abroad, and embittered refugees settling in the capital of the power that destroyed their home.

**Your trade-route proxies.** Today the civics, settlement tiers, marketplaces and harbors carry food and production
modifiers on trade routes (2c lists them per civic). Those buildings' trade-route modifiers become reach for
migration and supply: a harbor and a market widen `d0` and raise the share of supply that travels.

### 2c. Each civic: internal mobility, emigration and immigration

100 is neutral. The trade-route columns are the values in the civic records today. The new values are proposals for
you to adjust.

| Category | Civic | Trade food % | Trade production % | Trade routes | Internal mobility | Emigration | Immigration | Reason |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Leadership | Patriarch |  |  |  | 80 | 80 | 80 | kin and clan bind people |
| Leadership | Oligarchy |  |  |  | 100 | 90 | 90 |  |
| Leadership | Priesthood |  |  |  | 100 | 90 | 80 | religious gatekeeping |
| Leadership | Hereditary Rule |  |  |  | 90 | 80 | 90 | subjects bound to lords |
| Leadership | Assembly |  |  |  | 110 | 110 | 110 | citizens free to move |
| Leadership | Patrician |  |  |  | 100 | 100 | 110 |  |
| Leadership | Imperium |  |  |  | 110 | 100 | 120 | empire integrates provinces |
| Leadership | Fraternity |  |  |  | 120 | 120 | 120 | free association |
| Leadership | Technocracy |  |  |  | 120 | 110 | 120 | recruits talent |
| Administration | Oral Law |  |  |  | 80 | 100 | 100 | no records to organise movement |
| Administration | Tablets |  |  |  | 90 | 100 | 100 |  |
| Administration | Standardized Tablets |  |  |  | 100 | 100 | 100 |  |
| Administration | Accounting |  |  |  | 100 | 100 | 100 |  |
| Administration | Bookkeeping |  |  |  | 110 | 100 | 100 |  |
| Administration | Double Entry |  |  |  | 110 | 100 | 100 |  |
| Administration | Digital |  |  |  | 120 | 100 | 100 | administration organises movement |
| Taxation | No Taxes |  |  |  | 100 | 110 | 110 |  |
| Taxation | Tribute |  |  |  | 90 | 90 | 70 | subject peoples, little welcome |
| Taxation | Census |  |  |  | 80 | 70 | 100 | registration binds people to place |
| Taxation | Fiscus |  |  |  | 100 | 90 | 100 |  |
| Taxation | National Debt |  |  |  | 100 | 100 | 100 |  |
| Taxation | National Banking |  |  |  | 110 | 100 | 110 |  |
| Taxation | Planned Allocation |  |  |  | 70 | 50 | 70 | state allocates people |
| Economy | Hunter Gatherer |  |  |  | 150 | 150 | 150 | mobile bands |
| Economy | Agricultural |  |  |  | 70 | 80 | 80 | tied to land |
| Economy | Pastoral |  |  |  | 130 | 120 | 110 | herders move with herds |
| Economy | Coastal |  |  |  | 110 | 110 | 120 | sea routes |
| Economy | Barter | 20 |  |  | 90 | 100 | 100 |  |
| Economy | Metals | 20 |  |  | 100 | 100 | 100 |  |
| Economy | Coinage | 25 |  | 1 | 110 | 100 | 110 |  |
| Economy | Usury | 25 |  | 1 | 110 | 100 | 110 |  |
| Economy | Colonial | 40 |  | 1 | 120 | 150 | 130 | settler emigration to colonies |
| Economy | Protectionism | 40 |  | 1 | 100 | 80 | 70 | closed to foreign labour |
| Economy | Corporate | 30 |  | 2 | 130 | 120 | 130 | labour follows capital |
| Economy | Planned | 50 | 50 | 1 | 80 | 50 | 50 | state directs labour |
| Economy | National Socialism | 50 | 50 | 1 | 60 | 30 | 20 | closed borders, no foreign trade |
| Economy | Keynesian | 50 |  | 2 | 120 | 110 | 120 |  |
| Employment | Aboriginal |  |  |  | 100 | 100 | 100 |  |
| Employment | Peasantry |  |  |  | 60 | 60 | 100 | serfdom binds peasants to land |
| Employment | Slavery |  |  |  | 50 | 50 | 120 | the enslaved cannot move; forced arrivals |
| Employment | Caste System |  |  |  | 50 | 70 | 60 | birth fixes place and trade |
| Employment | Proletariat |  | 50 |  | 140 | 120 | 120 | labour moves to factories |
| Employment | Qualified Labor |  | 50 |  | 130 | 120 | 130 | skilled labour recruited |
| Employment | Labor Allocation |  |  |  | 80 | 60 | 80 | state assigns work |
| Education | Homeschooling |  |  |  | 100 | 100 | 100 |  |
| Education | Elders |  |  |  | 90 | 100 | 100 |  |
| Education | Tutors |  |  |  | 100 | 100 | 100 |  |
| Education | Academies |  |  |  | 110 | 100 | 120 | attracts scholars |
| Education | Trade School |  |  |  | 110 | 100 | 110 |  |
| Education | Humanistic |  |  |  | 110 | 110 | 120 |  |
| Education | Public Schools |  |  |  | 110 | 100 | 110 |  |
| Religion | Folklore |  |  |  | 100 | 100 | 100 |  |
| Religion | Spiritism |  |  |  | 100 | 100 | 100 |  |
| Religion | Divine Rule |  |  |  | 90 | 80 | 80 |  |
| Religion | Sacrifice Cult |  |  |  | 80 | 70 | 60 | fear of outsiders |
| Religion | Fanaticism |  |  |  | 80 | 90 | 30 | minorities leave, few admitted |
| Religion | Pantheon |  |  |  | 100 | 100 | 130 | tolerance draws believers of many faiths |
| Religion | State Religion |  |  |  | 90 | 90 | 70 |  |
| Religion | Occult |  |  |  | 100 | 100 | 120 |  |
| Religion | Scientism |  |  |  | 110 | 100 | 120 |  |
| Military | Tribal Warfare |  |  |  | 100 | 100 | 100 |  |
| Military | Raiders |  |  |  | 100 | 100 | 80 |  |
| Military | Fortification |  |  |  | 90 | 100 | 100 |  |
| Military | Mercenaries |  |  |  | 100 | 100 | 120 | foreign soldiers settle |
| Military | Standing Army |  |  |  | 100 | 100 | 100 |  |
| Military | Militia |  |  |  | 90 | 100 | 100 |  |
| Military | Professional Army |  |  |  | 100 | 100 | 100 |  |
| Military | Conscription |  |  |  | 90 | 120 | 80 | draft-age emigration |
| Economy | Guilds | 30 |  | 1 | 80 | 80 | 60 | guild entry control (D29 d) |

## 3. Clothing

### 3a. Facts

- **Status.** The English Statute concerning Diet and Apparel (1363) set what each class could wear after the Black
  Death raised wages and the lower classes copied elite fashion; fur was the earliest restriction. A 1337 law banned
  importing foreign cloth and exporting wool (protection).
- **Value and reuse.** Clothes were handmade and valuable: probate inventories list them, and servants received and
  resold their masters' clothes. A large second-hand trade lasted until cheap ready-made clothing replaced it (Lemire
  1988).
- **Fibres:**
  - linen made the underclothing and shirts of medieval Europe;
  - hemp went mainly to rope and sailcloth;
  - Russian flax and hemp were major exports, the canvas and rope of navies.
- **Machines:**
  - the spinning mule (Crompton, 1779), and Roberts's self-acting mule (patented 1825, 1830);
  - by the mid-1820s a power-assisted mule of 600 spindles could process 100 lb of cotton in about 135 hours
    (Cottontown; the hand-spinning comparison is still to be sourced).
- **Open:** how long clothes lasted, and how much cloth a person used a year.

### 3b. Proposal

**Two needs per person:**
- **Warmth:** scaled by climate (latitude and terrain now, a climate field with LD). Met mainly by coats (wool, fur,
  leather).
- **Status:** scaled by wealth and culture. Met by dresses and fine cloth with quality grades (D29 c).

**Goods** (5 new records against the 32-bit limit):
- **base:** Wool, Leather, Cotton, Fur, Silk, Dye exist; hemp is the Cannabis resource; Flax is new (linen);
- **intermediate:** Cloth (from wool, cotton, flax or hemp) and Fine Cloth (the Drapers' luxury; D29);
- **garments:** Coats (outer wear, warmth first) and Dresses (full dress, status first). Each carries a quality grade.

**The chain:**
- Spinning and weaving happen inside the city from fibres, as bread does from grain.
- The rates rise with the textile technologies and machines: spinning wheel, flying shuttle, spinning jenny, water
  frame, mule, power loom.
- Skilled labour (workshops) raises quality.

**Dress norms:** a city's demand mix and the speed of fashion depend on:
- religiosity (state religion civics: modest, slower fashion);
- secularization (Scientism, Humanistic: freer dress);
- diversity (many religions and cultures in the city: more variety);
- open or closed markets (Protectionism, National Socialism: fewer imported styles);
- free or censored media (D21's media reach).

These shift how many dresses per coat people want and how fast clothes go out of style (replacement rate), not the
warmth need.

**Wear:** clothes are a flow. Each person replaces a share each year (rate open), and old clothes go to a second-hand
share that the poor use.

## 4. Guilds

### 4a. The food guilds (Bakers, Butchers, Fishmongers, Grocers)

- **Quality:** goods made in a city with the guild hall can be fine; in the master guild's city, masterwork (D29 c).
- **Employment:** the guild's workshops (D29 e) employ a share of the urban people.
- **Protection:** fixed prices (no price spikes in their goods) and a shield against cheaper imports of their goods
  under the Guilds civic.
- **What masterwork food does:**
  - trades higher (× 2-2.5);
  - spoils slower (its spoilage × 0.5, *estimate*);
  - adds to health and strength through the health profile (round_m75.md section 2), for example the protein
    coverage of cured hams and sausages (with their processed-meat harm counted).

### 4b. Education: cheaper adjacent technologies (a new field for all buildings and wonders)

- **Fact:** the research cost of a tech is set in `CvTeam::getResearchCost` and `CvPlayer::calculateResearchModifier`.
  The latter already holds tech diffusion (BBAI). The building records have no tech-cost field today: only
  `PrereqTech`, `ObsoleteTech` and `iFreeTechs`.
- **Proposal:** a list field on BuildingInfo, `TechResearchModifiers`.
  - Each entry is a tech (or a tech category) and a percent reduction of its research cost, for the owner of the
    building.
  - It is applied in `CvPlayer::calculateResearchModifier`, beside diffusion, with the AI reading it through the same
    function.
- **Examples (to fill per record):**
  - the Lighthouse, Great Lighthouse and Colossus: maritime technologies (the sailing and navigation line);
  - the guild halls: their trade's technologies (Bakers and Butchers: agricultural and food-processing techs;
    Masons: Masonry, Construction, Architecture and later; Clerks: writing, paper, printing and administration).

## 5. Masons and Clerks, as the XML has them

**Masons:**
- **Master guild:** comes with Architecture, needs the Crafts Guild Hall and two High Walls, built by a great engineer.
- **The guild:** +2 production per Stone, Marble and Obsidian.
- **The hall:** +20 % defence, +20 bombard defence; +10 % production per Stone and Marble, +5 % per Obsidian.

**Clerks:**
- **Master guild:** comes with Paper, needs two Libraries, built by a great scientist.
- **The guild:** +2 gold, +2 research and +2 culture.
- **The hall:** a free Scientist, +25 % espionage defence, Scientists +1 yield.

**The Architecture wonders:** Notre Dame and the J.S. Bach Cathedral (both Christian). There are also a cathedral wonder
per religion (Jewish, Christian, Islamic, Hindu, Buddhist, Confucian, Taoist, Hellenic, Zoroastrian, Egyptian,
Mesoamerican), Hagia Sophia (Theology) and the Sistine Chapel (Perspective).

**Building production fields:** the records only have `iMilitaryProductionModifier`, `iSpaceProductionModifier`, domain
and resource production modifiers. None speeds building construction.

**Proposal:**
- **Masons:**
  - a new field `iBuildingProductionModifier` (city), set on the Masons hall: +25 % *estimate* to building
    construction, replacing the +10 % per Stone and Marble;
  - the master guild (or a national Masons guild, D29 a) becomes a requirement for Notre Dame and the J.S. Bach
    Cathedral (and, if you want, the religions' cathedral wonders);
  - research reductions for masonry and architecture techs (4b).
- **Clerks:** science and administration effects, not a luxury:
  - research reductions for writing, paper, printing and administration techs (4b);
  - lower distance maintenance in their cities (record-keeping);
  - the free Scientist kept;
  - books as a good only if you want one.

## 6. Plan changes

- **design.json:** D33 records migration (decided parts and the open model); D28 and D29 get the decided parts; D34
  records the new research field; the Masons and Clerks proposals sit under D29.
- **plan.json:** none until D30 and the migration model are decided. The fields named here join FD.F1 when they are.
