# What RoM's XML says about war

This is what the game's own data says about war in Rise of Mankind. It is read
deterministically from the XML and checked against the DLL and RoM's Python rules
wherever a value only means something through the code that uses it. The generated tables
are in [xml-war-tables.md](xml-war-tables.md).

## How the XML was read

[tools/xmlread.py](tools/xmlread.py) reads the XML as the game loads it:

- **Parsing.** Every XML file is parsed with a real XML parser, against the XDR schema its
  root names (`xmlns="x-schema:…"`). The schema declares each element's content, its data
  type (int, boolean, float or string) and whether it repeats. Every record is written with
  every field its schema declares.
- **Which files.**
  - `Assets/XML` comes first.
  - Then come the module directories that the `MLF_CIV4ModularLoadingControls.xml` files
    load, in MLF order. Paths are matched case-insensitively, as on Windows.
  - `Assets/Unloaded Modules` is never read.
- **Merging.** A module record whose Type already exists is merged as the DLL's
  `copyNonDefaults` merges it: the module's non-default values replace the old ones.
- **Defines.** These follow `CvXMLLoadUtility::SetGlobalDefines`:
  - files are read in this order: `GlobalDefines`, `GlobalDefinesAlt`, `BBAI_AI_Variables`,
    `BBAI_Game_Options`, `TechDiffusion`, `LeadFromBehind`, `PythonCallbackDefines`, then the
    module defines;
  - a later value always replaces an earlier one (`SetValue`).

Result:
- 757 XML files: 548 have a schema and 521 are loaded.
- 7,613 records of 64 types.
- The files without a schema are game text, config and README files.
- Seven loaded schema files hold only art, audio, hint and world-picker scripts, keyed by
  other fields.

Further tools:
- [tools/xmlprofile.py](tools/xmlprofile.py) lists every field of a record type, with how
  many records set it and its range or values. All 30 gameplay record types were read in
  full this way.
- [tools/wartables.py](tools/wartables.py) builds the tables.

Earlier hand-written readers had two errors, both corrected here:
- They read `Assets/Unloaded Modules` (217 leader files the game never loads).
- They took `WAR_SUCCESS_CITY_CAPTURING` as 25. The game's value is 22, because the BBAI
  file is read after `GlobalDefines.xml`.

## Time: how long a military advantage lasts

**Game speed sets research against production.** Research is several times dearer
relative to units on slow speeds:

| Speed | Research | Train | Research ÷ train |
|---|---|---|---|
| Normal | 100 | 100 | 1 |
| Epic | 300 | 100 | 3 |
| Marathon | 600 | 300 | 2 |
| Snail | 700 | 300 | 2.3 |

On Marathon an era lasts twice as many unit builds as on Normal; on Epic, three times.
- An army of one era is larger relative to the pace of technology.
- A unit advantage is held for more turns.

**Techs get cheaper as others learn them.** Tech diffusion is on:
- A tech known by teams one has met is 30 % cheaper.
- `TECH_COST_KNOWN_PREREQ_MODIFIER` is 15.

So a technological lead closes quickly, and a window of opportunity has to be used while
it is open.

**Eras change unit costs.**
- Units get cheaper per era: training costs 90 % in the Renaissance and falls to 50 % in
  the Future era.
- Research falls faster: 90 % down to 40 %.

**Difficulty helps the AI more as the game goes on.**
- The AI trains and builds at 60 % (Deity) to 95 % (Prince).
- It pays 50 % for unit supply and for upgrades at every level.
- `iAIPerEraModifier` adds −2 to −5 % per era from Monarch up.
- AI war weariness is 50–100 %.

## Space: movement, ground, interior lines

**Movement.** The denominator is 120.
- Flat land costs 1 move.
- Desert costs 3 moves and gives −25 % defence. Marsh costs 3; tundra and snow cost 2.
- Hills cost +1 move and give +25 % defence. Peaks are impassable.
- Forest gives **+50 %** defence (twice the BTS value) and costs 2 moves.
- Jungle gives +50 % and costs 3. Swamp gives +25 % and costs 3.
- Crossing a river costs −25 % in attack; an amphibious attack costs −50 %.

**Roads.** A road counts only when both tiles have it.

| Route | Tiles per move | Needs |
|---|---|---|
| Road | 2 | The Wheel |
| Paved road | 3 | Stone, Construction |
| Roman road | 4 | |
| Modern road | 4 | Diesel |
| Railroad | about 10 | Steel and coal, oil or diesel |

**Enemy roads cannot be used** (`CvPlot::isValidRoute`), unless a promotion grants
`bEnemyRoute` (five do). Inside his own land the defender moves reserves two to four times
faster than the invader advances, and the invader pays full terrain cost on every enemy tile.
- A one-move siege train advances one tile a turn in enemy land, roads or not.
- Influence Driven War shifts plot culture after won battles, and pillaging shifts it too.
  Tiles that become the invader's give him their roads.

**Ground.** Collateral damage ignores terrain, so collateral is what dislodges stacks.
Other defensive ground:
- Forts give +50 % (Mathematics), bunkers +75 %, future bunkers +100 %; all may be built
  outside borders.
- Hamlets, villages and towns give +10/+15/+20 %.
- Latifundia give up to +35 %.

## Cities: what a siege must break

These rules are all from `CvCity` and `CvUnit::bombard`.

- **Total city defence** is the larger of the building defence and the culture defence, plus
  a player modifier. The two are not added.
- **Culture defence** runs +10 (Fledgling) to +50 (Legendary). On Marathon, Developing takes
  550 culture and gives +20.
- **Building defences add up.** RoM's Python upgrade rules (`RoMGameUtils.cannotConstruct`,
  `onBuildingBuilt`) decide which buildings stand together:
  - High Walls replace Walls.
  - Town, City and Metropolitan Essentials replace each other.
  - The Castle stands alone.

| Building | Defence | Bombard defence | Tech | Obsolete | Survives capture |
|---|---|---|---|---|---|
| Walls | +30 | 20 | Masonry | Rifling | 20 % |
| High Walls | +50 | 40 | Siege Warfare | Rifling | 30 % |
| Castle | +50 | 20 | Engineering | Economics | 40 % |
| Essentials (Town / City / Metropolitan) | +10 / +20 / +30 | — | | | |

  Temples of several religions add +10. The Krak des Chevaliers gives +75 and Edinburgh
  Castle +100.

- **Bombarding.** Each strike removes rate × (100 − summed bombard defence) / 100 defence
  points, converted to damage as 100 × points / total defence.
  - Units that ignore building defence, gunpowder siege onwards, skip the bombard defence.
  - A city heals 5 points of damage a turn, but only on a turn it was not bombarded.

**Worked example: a well-built medieval city.** High Walls, Castle and City Essentials give
120 % building defence and 60 % bombard defence. Bringing it to zero takes:

| Bombarding unit | Rate | Points per strike | Strikes |
|---|---|---|---|
| Trebuchet | 16 | 16 × 40 / 100 = 6 | about 20 |
| Catapult | 8 | 3 | about 40 |
| Bombard (ignores the walls) | 10 | 10 | 12 |

  So five trebuchets need four turns of unbroken bombardment. A siege that pauses for a turn
  gives back 5 % of the damage.

- **The defender's side.** Its Longbowman is strength 8, +25 % city defence, with one first
  strike. In the city at full defence, fortified (+25 %) and on hills (+25 %), it fights at
  about 8 × 2.9 ≈ 23 (+120 building, +25 city, +25 fortify, +25 hills). At zero defence it
  fights at about 8 × 1.75 = 14. A Knight is 14, a Heavy Swordsman 13 with +10 % city attack,
  a Trebuchet 8 with +75 % city attack.

  Assaulting before the walls are down is a slaughter. After they are down it is an even
  fight, and collateral decides it.
- **Archers in cities.**
  - Archers get +50 % city defence and Longbowmen +25 %; both have a first strike.
  - Every archer and siege unit has a ranged strike: 75–90 % for archers, 50 % for siege.
  - The Protective trait adds City Garrison I (+20 % city defence) and Drill I to archers
    and gunpowder units.
- **Capturing a city.**
  - Each building survives capture with its `iConquestProb` (290 buildings set it).
  - Occupation lasts 3 turns + 50 % of population.
  - Capture gold is 20 + 10 per population, with a random part.
  - Razing is allowed while the city's culture is under 25 %.
  - War success: 22 for the city, 4 per attack won, 3 per defence won.

## The army: units, counters, collateral

The [unit table](xml-war-tables.md#land-combat-units-class-defaults-by-research-distance)
covers all 138 land unit classes in order of research distance. For each it gives
strength, cost, moves, city attack and defence, first strikes, withdrawal, combat limit,
collateral (effective strength, %, targets, cap), bombard, ranged strike, whether it
ignores walls, counters, flanking strikes, collateral immunities, forest/jungle
modifiers, resources and buildings.

**Counters and collateral immunity.**
- Spearmen, Pikemen and Heavy Pikemen get +50 % against mounted units and need no resource.
- Pikemen, Heavy Pikemen and the Sarissa are **immune to collateral from mounted units**
  (`UnitCombatCollateralImmunes`, checked against the victim in `CvUnit.cpp:13112`). A
  Knight's collateral, which can kill, does not touch them.
- Siege units are immune to collateral from enemy siege.
- Axemen and Macemen get +50 % against melee; Chariots +100 % against Axemen; Crossbowmen
  +50 % against melee.
- Horsemen get +25 % against catapults, trebuchets and archers.

**Flanking strikes.** When a mounted unit wins, it damages siege units in the stack it
attacked:
- Horsemen: catapults and trebuchets at 50.
- Horse Archers and Knights: at 100.
- Cuirassiers and Cavalry: every early siege unit.
- Light and Heavy Cavalry: archers, longbowmen and crossbowmen at 100.

A siege stack without anti-mounted escorts loses its siege to cavalry.

**Forest and jungle.** Most mounted and wheeled units attack at −25 % in forest and −50 to
−75 % in jungle. Elephants gain +15 to +25 %.

**Collateral as the battle applies it.** Effective strength is base strength × % / 100, as
an integer:
- Archers: 0.
- Catapult 6, Trebuchet 8, Bombard 11, Cannon 16, Artillery 24.
- Knight 7 at a 100 % cap, so it can kill.

**Buildings that gate units.**
- Siege needs a Siege Workshop; Bombards and Cannons a Cannon Forge.
- Knights need a Knight Stable and most mounted units a Stable.
- Archers need an Archery Range.
- Swordsmen and the heavy infantry need an Armourer.

The unit cannot be trained at all without the building.

## Supply: what to deny

[The resource table](xml-war-tables.md#strategic-resources-land-unit-lines-that-need-them)
lists, for each strategic resource, the unit lines that need it.

| Resource | Units that need it |
|---|---|
| Horse | Every mounted unit, Chariot to Cavalry |
| Iron | Swordsman, Heavy Swordsman, Heavy Pikeman, Bombard, Cannon; one option for most ancient and classical melee |
| Copper, iron or obsidian | Most ancient and classical melee (any one of them) |
| Sulphur | Arquebusier, Musketman, Grenadier; one option for Bombard, Cannon and Cuirassier |
| Ammo | Every modern infantry and artillery unit (Ammo is produced by a building) |
| Diesel | Every vehicle |

- **Pikemen and Spearmen need none.** A defender without horses still has its anti-cavalry.
- **Sulphur gates the whole gunpowder line.** An empire cut off from sulphur cannot field the
  Renaissance defence.

Taking or pillaging the source denies it. Strategic resources sit on mines, quarries,
pastures, wells and camps, several of them allowed outside borders.

## Production, experience, healing, morale

Full tables: [civics](xml-war-tables.md#civics-with-military-effects) and
[buildings](xml-war-tables.md#buildings-with-military-effects).

**Experience.**
- Barracks give +3 to melee and recon, +2 to mounted and animal, +1 to siege.
- Legion Barracks give melee +10 and military production +25 %.
- The Stable gives mounted +2, the Knight Stable +3, the Siege Workshop siege +2 and archers
  +3, the Spanish Citadel siege +5.
- West Point gives all units +4 and the Pentagon +2 globally.
- Civics: Professional Army gives free experience +10, Standing Army and Mercenaries +5,
  Public Schools +5, Academies, Oligarchy and Raiders +3.

**Military production.**
- Heroic Epic and Secret Army Base +100 %.
- Military Academy, Waffenmanufaktur and Shinto Shrine +50 %.
- Hereditary Rule, Imperium, Caste System and Planned Allocation +25 %.
- Legion Barracks, Early Barracks, Shinto Temple and Temple of Set +25 %.

**Healing.** Base rates are 5 in enemy land, 10 neutral, 15 friendly and 20 in a city, with
city buildings adding at most 30. The Roman Depot and the Incubation Center add +30, the
Garrison +20.

**War weariness.** Own attackers killed weigh 3, own defenders killed 2, a city lost 6. It
decays 1 per turn.
- Map size changes it from +50 % (Duel) to −85 % (Gigantic), so long wars cost little on
  big maps.
- Civics range from −50 % (Divine Rule, State Religion, Sacrifice Cult) to +100 % (Patrician).
- The Statue of Zeus gives the enemy +100 %.

**Great Generals.**
- The threshold starts at 30 and rises by 50 for each one.
- The Imperialist trait doubles the rate; the Art of War gives +50 % and halves upgrade costs.
- Humanistic gives +100 %; Fortification and Assembly +100 % at home.

## Leaders

The [leader table](xml-war-tables.md#leaders-war-personality) covers all 82 loaded
leaders.

| Setting | Range | Median | Meaning |
|---|---|---|---|
| Base attack odds | +0 to +6 | | Added to the odds the AI demands before attacking |
| Attack odds random | +6 to +10 | | Random part of the same |
| `iBuildUnitProb` | 15–40 % | 30 % | |
| `iMaxWarRand` | 50–400 | 100 | A war is planned with probability 1/rand: smaller is more aggressive |
| `iLimitedWarRand` | 40–200 | | Same rule, limited war |
| `iDogpileWarRand` | 20–150 | | Same rule, dogpile war |
| `iMakePeaceRand` | 10–120 | | |
| Power ratio wanted (nearby target) | 80–130 % | | |
| Power ratio wanted (distant target) | 0–100 % | | |
| `iRazeCityProb` | 0–75 % | 0 | |

Two other personality settings are exact:
- **Unit AI weights.** Each leader has one favoured unit role at +100. Examples: Bismarck,
  Ashur, Lenin and Leonidas favour collateral units; Boudica, Genghis Khan and Shaka
  favour pillage; Charlemagne, Deganawida and Louis XIV favour city attack.
- **Military flavour.** It runs from 2 to 10. The highest are Bismarck, Genghis Khan,
  Lenin, Ragnar and Shaka.

These settings are where an opponent's character already lives. A better war AI should
keep them deciding between good options rather than replace them.
