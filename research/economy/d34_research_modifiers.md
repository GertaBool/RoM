# D34: which buildings make which technologies cheaper (R33.1, M79)

This replaces the examples of `round_m77.md` section 4, which made no sense.

**What was wrong with them.** They named each building's own prerequisite techs, or techs before them:
- the Lighthouse (needs Sailing) made Sailing cheaper;
- the Library (needs Literature) made Writing cheaper;
- the Observatory (needs Astronomy) made Astronomy cheaper;
- the Pyramid (needs Masonry) made Masonry cheaper.

The owner of such a building already has those techs. They also ignored that the Colossus goes obsolete at Astronomy
and the Great Lighthouse at Corporation.

## The rule (from the records)

A building may make cheaper only a tech that:
1. **is not among its own required techs or their ancestors** (`PrereqTech`, `TechTypes`, and everything those
   require, from `CIV4TechInfos.xml` OrPreReqs and AndPreReqs). The owner has those already;
2. **is not the building's obsolete tech or after it** (`ObsoleteTech` and its descendants). An obsolete building
   gives nothing;
3. **follows on from the building's knowledge:** preferably a tech below its own in the tree (the steps are shown).
   Where its line ends (Seafaring and Ship Building lead almost nowhere in this tree), a parallel tech the owner may
   still lack and the building's trade plainly prepares (for example Compass and Navigation for a Harbor).

Each pick below was checked by a script against rules 1 and 2. None failed. The steps count the shortest path down
the tree from the building's own techs.

**The guild halls:**
- The per-trade halls have no tech or obsolete tech of their own in the records. They are anchored to their master
  guild's tech and Guilds.
- Only the three grand halls go obsolete at Machine Tools.

## The table (techs and buildings from GitLab claude/settlement-economy d2a8f756; percents are estimates)

| Building or wonder | Its own techs (already known) | Obsolete at | Techs made cheaper (steps below its techs, or parallel) | % | Why |
|---|---|---|---|---:|---|
| Lighthouse | Sailing | - | Seafaring (1), Naval Warfare (1), Ship Building (2), Compass (1), Navigation (2) | 10 | coastal sailing knowledge |
| Great Lighthouse | Seafaring, Masonry, Greek | Corporation | Ship Building (1), Compass (4), Navigation (5), Astronomy (3) | 20 | pilots and navigation |
| Colossus | Bronze Working, Greek, Seafaring, Mathematics | Astronomy | Iron Working (1), Ship Building (1), Compass (2) | 15 | bronze casting at scale, harbour |
| Harbor | Seafaring | - | Ship Building (1), Compass (parallel), Navigation (parallel) | 10 | shipwrights and pilots |
| Shipyard | Ship Building | - | Compass (parallel), Navigation (parallel), Naval Cannon (parallel) | 10 | shipbuilding |
| Drydock | Steel | - | Screw Propeller (1) | 10 | steel ships |
| Magellan's Voyage | Navigation | Screw Propeller | Naval Tactics (1), Mercantilism (1) | 20 | ocean voyages, trade |
| Library | Literature | - | Philosophy (1), Theology (1), Paper (2), Printing Press (1), Education (2) | 10 | written learning |
| Great Library | Literature, Greek | Scientific Method | Philosophy (1), Paper (2), Printing Press (1), Education (2), Humanism (2) | 20 | collected learning |
| Archive | Writing, Religion Sumer | Education | Alphabet (1), Code Of Laws (1), Mathematics (1), Civil Service (2), Literature (2) | 10 | records and administration |
| University | Education | - | Printing Press (1), Anatomy (1), Algebra (1), Physics (1), Scientific Method (2) | 10 | scholarship |
| Observatory | Astronomy | - | Physics (1), Scientific Method (1) | 10 | observation |
| Copernicus' Observatory | Astronomy | Radar | Physics (1), Scientific Method (1), Thermodynamics (2) | 20 | astronomy |
| Newton's University | Physics | Quantum Physics | Scientific Method (1), Thermodynamics (1), Steam Power (1), Electricity (2) | 20 | physics |
| Leonardo's Workshop | Oil Painting | Thermodynamics | Free Artistry (1), Realism (2), Replaceable Parts (parallel) | 20 | art and engineering |
| Forge | Metal Casting | - | Bronze Working (1), Iron Working (2), Currency (1), Smithing (4), Metallurgy (5) | 10 | metalworking, coinage |
| Pyramid | Ceremonial Burial, Masonry | - | Construction (1), Engineering (2), Sculpture (1), Architecture (3) | 15 | monumental building |
| Stable | Chariotry | Vertical Flight | Horseback Riding (1), Horse Breeding (2), Stirrup (3) | 10 | horses |
| Market | Trade | - | Writing (1), Mathematics (1), Currency (2), Banking (3) | 10 | trade and accounts |
| Bank | Banking | - | Mercantilism (1), Economics (2), Corporation (3) | 10 | finance |
| Aqueduct | Waterworks | - | Sanitation (1), Modern Sanitation (2) | 10 | water works |
| Hospital | Medicine | - | Modern Sanitation (1), Organic Chemistry (1), Genetics (1), Modern Health Care (2) | 10 | medicine |
| Brewery | Fermentation | - | Agricultural Tools (parallel), Alchemy (parallel), Biology (parallel), Refrigeration (parallel) | 10 | brewing, distilling, yeast, cooling |
| Theatre | Drama | Wearable Electronics | Music (1), Humanism (1), Free Artistry (2), Realism (2) | 10 | performing arts |
| Siege Workshop | Siege Warfare | Artillery | Machinery (1), Engineering (2), Smithing (1) | 10 | machines |
| Masons guild hall (Masons: Architecture) | Architecture, Guilds | - | Perspective (1), Algebra (2), Physics (2), Civil Engineering (6) | 15 | building, geometry, statics |
| Clerks guild hall (Clerks: Paper) | Paper, Guilds | - | Printing Press (1), Education (1), Map Making (1), Political Philosophy (2), Economics (3) | 15 | printing, schooling, administration |
| Blacksmiths guild hall (Smithing) | Smithing, Guilds | - | Armor Crafting (1), Metallurgy (2), Replaceable Parts (3) | 15 | smithing |
| Carpenters guild hall (Engineering) | Engineering, Guilds | - | Architecture (1), Clockworks (2), Printing Press (2) | 15 | joinery, mechanisms, presses |
| Glassblowers guild hall (Optics) | Optics, Guilds | - | Astronomy (1), Scientific Method (2), Photography (1), Chemistry (3) | 15 | lenses, instruments, glassware |
| Goldsmiths guild hall (Clockworks) | Clockworks, Guilds | - | Compass (1), Navigation (1), Mercantilism (2) | 15 | precision work, coin and credit |
| Bakers guild hall (Agricultural Tools) | Agricultural Tools, Guilds | - | Alchemy (1), Biology (4), Pesticides (1) | 15 | yeast, grain care |
| Butchers guild hall (Crop Rotation) | Crop Rotation, Guilds | - | Biology (4), Refrigeration (5) | 15 | breeding, cooling |
| Fishmongers guild hall (Guilds) | Guilds | - | Map Making (2), Navigation (3), Refrigeration (5) | 15 | fishing grounds, keeping fish |
| Grocers guild hall (Usury) | Usury, Guilds | - | Banking (1), Mercantilism (2) | 15 | trade in provisions |
| Mercers guild hall (Banking) | Banking, Guilds | - | Mercantilism (1), Economics (2), Corporation (3) | 15 | trade, finance |
| Drapers guild hall (Heraldry) | Heraldry, Guilds | - | Mercantilism (2), Chemistry (3), Industrialism (6) | 15 | cloth trade, dyes, mills |
| Equestrians guild hall (Stirrup) | Stirrup, Guilds | - | Chivalry (1), Armored Cavalry (1), Cavalry Tactics (1) | 15 | horsemanship |
| Artists guild hall (Music) | Music, Guilds | - | Humanism (1), Free Artistry (2), Realism (1), Oil Painting (3) | 15 | arts |

**Notes:**
- **Stacking:** reductions for one tech add across a player's buildings, with a cap of *estimate* 50 %.
- **The Clerks** (accepted in M77 as "cheaper writing, paper, printing and administration techs"). Writing and Paper
  come before the Clerks master guild (it needs Paper), so by rule 1 the Clerks make the later steps cheaper: Printing
  Press, Education, Map Making, Political Philosophy, Economics.
- **The Marco Polo embassy** is left out. Its tech, Optics, leads only to Astronomy and Photography within two steps,
  neither related to embassies and trade.
- **The Academy** has no prerequisite tech in the records, so it gets no entry until one is chosen.
