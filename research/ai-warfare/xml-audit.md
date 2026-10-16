# RoM combat XML audit

The complete, schema-driven reading of all XML is [xml-knowledge.md](xml-knowledge.md); its tables are [xml-war-tables.md](xml-war-tables.md). This audit covers land units, promotions and city defences only.

## What the XML says, for the war-AI design

Read from the XML itself (all modules are loaded), with the DLL code checked where a value's effect depends on it.

**Settings (`GlobalDefinesAlt.xml`, `GlobalDefines.xml`, `LeadFromBehind_GlobalDefines.xml`).**
- DCM is mostly off:
  - Off: `DCM_RANGE_BOMBARD` (also unused in play; it was dysfunctional), stack attack, opportunity fire,
    active defence, archer bombard, air bombing, fighter engage.
  - On: battle effects, and **naval bombard** (ships bombard city defences).
- **Influence Driven War is on.** A won battle shifts plot culture within 2 plots (base 4.0). Influence is
  multiplied by 2.5 when a city's last defender dies and by 2.0 for a fort captured in combat. The emergency
  militia draft is off.
- Combat:
  - `COMBAT_DAMAGE` 20, `COMBAT_DIE_SIDES` 1000, `RANGE_COMBAT_DAMAGE` 30, `COLLATERAL_COMBAT_DAMAGE` 10.
  - Rivers -25 % and amphibious attacks -50 %. Hills +25 % defence. Fortification 5 % per turn up to 5 turns.
  - `RANGED_ATTACKS_USE_MOVES` 0: a ranged strike uses up the unit's attack, not its moves.
- Healing per turn: 5 HP in enemy land, 10 neutral, 15 friendly, 20 in a city, with the city building heal
  capped at 30. City defence recovers 5 per turn.
- Lead From Behind is on and uses combat odds. It holds back units with a general (5), units of limited
  classes (5), healers (2) and experienced units (1).

**Ranged strikes are the main no-risk damage source (33 land units).**
- Archers (11 units) default to `UNITAI_CITY_DEFENSE` and strike up to **75 %** damage:
  - **Longbowmen, Crossbowmen and Cho-ko-nu strike to 90 %**, so a city's archers can strip an adjacent
    stack's best defender to 10 % health.
- Siege units strike to 50 %, with their full collateral. Some mounted units (horse archers) and late units
  strike as well.
- **Each strike is small:** `rangeCombatDamage` uses `iAirCombat`, which is 1-2 on these units, so a strike
  deals about 12-16 HP to the defender the game picks, almost whatever the striker's own strength. Strikes add
  up: five longbowmen in a city take about 70 HP off the best defenders of a stack parked next to it, and
  siege strikes also spread their collateral.

**Effective collateral strength** (integer base strength × % / 100, which is what `collateralCombat` uses):
- Archers deal 0-2. Only Archer, Peltist and Babylon Bowman deal 0.
- Mounted units: Horseman 1, Horse Archer 2, Chariot 5, Knight 7, Cuirassier 5, Cavalry 6, War Elephant 5
  (10 targets).
- Siege: Catapult 6, Trebuchet 8, Bombard 11, Cannon 16, Artillery 24.
- **Mounted units have a collateral limit of 100 %, and that can kill.** `collateralCombat` caps damage at
  `min(limit, limit × (C+F)/(T+F))`, and `CvUnit::setDamage` kills a unit at full damage. Whenever the
  attacker's collateral strength C is at least the target's base strength T, a stack's weaker units can die
  from collateral alone. A Knight (C 7) does this to archers, spearmen and axemen. Siege collateral stops at
  50-70 % and cannot kill.

**Killers and non-killers.** 15 land units have a combat limit below 100 and cannot kill: 13 siege units and
2 wheeled units. Any count of "units that can take the city" must leave them out.

**City defence.**
- Walls +30 (bombard defence 20), High Walls +50/40, Castle +50/20, Montfort +50/25, Krak des Chevaliers +75,
  Edinburgh Castle +100.
- Several religious temples add +10 each, and building defences add up.
- 75 units, gunpowder onward, ignore building defence. Walls matter until the Renaissance and then stop.

**Roles that shape stacks.**
- Spearmen and Pikemen are `COUNTER` units and are never allowed `CITY_DEFENSE`. Archers are the default city
  defenders, so archers end up as the defenders of field stacks.
- Catapults, Trebuchets, Bombards and Cannons may be `CITY_COUNTER` units, so siege sits in cities as
  counter-attackers, the role defensive collateral needs.

**Prerequisite buildings.** Siege needs a Siege Workshop (Cannon Forge for cannon), mounted units a Stable or
Knight Stable, archers an Archery Range, many melee units Barracks or an Armourer. Without the building the AI
cannot build the unit at all, whatever it values.

**iPower**, which feeds the AI's power comparisons and war decisions:
- Per hammer it is similar across early combat types: siege 0.21, melee 0.22, mounted 0.23, archer 0.21.
  Catapult 10 against Swordsman 20 is per unit; per hammer it is 0.20 against 0.24.
- Power is per strength, so it misses what siege adds through collateral and strikes.
- Outlier: the **Ram** has iPower 8 for 15 hammers (0.53 per hammer), which inflates the power of stacks
  with rams.

**Promotions.**
- City Raider +15/+15/+20/+25 city attack; City Garrison +20/+25/+30.
- Barrage +15/+20/+25 collateral; Accuracy +8/+16 bombard.
- Cover / Shock / Formation in tiers of +20/+25/+30 against archer / melee / mounted. In RoM **Charge** is
  +20/+25/+30 against **siege**.
- Drill gives first strikes (Drill II +1, Drill IV +2); Flanking gives withdrawal +10/+15/+15; Tactics
  (with a leader) +20 withdrawal.
- **Medic needs the Naturopathy tech**: +10 same plot and +5 adjacent at levels I-II, +15/+15 at level III.

## Method

Read from `Assets/XML` and every module directory that `MLF_CIV4ModularLoadingControls.xml` loads (all are loaded). Land units with strength > 0: 250. Values are the XML values; derived columns are computed as the DLL does.

## Findings

- Units with a ranged strike (iAirRange > 0 and iAirCombat > 0): 33. By combat type: {'ARCHER': 11, 'MOUNTED': 4, 'SIEGE': 13, 'ASSAULT_MECH': 3, 'ROBOT': 2}.
- Units with iCollateralDamage > 0: 71, of which 3 have **effective collateral 0** (integer strength x % / 100), e.g. ARCHER, BABYLON_BOWMAN, PELTIST.
- Combat-limited units (iCombatLimit < 100, cannot kill): 15, by type: {'SIEGE': 13, 'WHEELED': 2}.
- Units that bombard city defences: 29; that ignore building defence: 75.
- Units with a DCM ranged-bombard range (DCM_RANGE_BOMBARD is 0, so unused): WARLORDII, WARLORDIII, WARLORDIV, WARLORDV.
- **iPower per hammer and per strength point**, median by combat type (iPower feeds the AI's power comparisons and war decisions):

| Combat type | Units | iPower / cost | iPower / strength | Example |
|---|---|---|---|---|
| MELEE | 48 | 0.22 | 1.71 | HYPASPISTS: cost 60, str 7, power 12 |
| MOUNTED | 45 | 0.23 | 1.88 | ARABIA_CAMELARCHER: cost 90, str 12, power 30 |
| TRACKED | 32 | 0.38 | 3.22 | TANK_PZKPFWIVAUSFF: cost 420, str 50, power 161 |
| GUN | 29 | 0.33 | 2.76 | WARLORDIII: cost 300, str 25, power 20 |
| SIEGE | 17 | 0.21 | 2.31 | BOMBARD: cost 140, str 11, power 23 |
| ARCHER | 14 | 0.21 | 1.73 | SAGITTARII: cost 40, str 5, power 9 |
| WHEELED | 9 | 0.34 | 2.92 | UN_MI: cost 400, str 48, power 23 |
| HITECH | 7 | 0.48 | 4.00 | ACVSAM: cost 840, str 100, power 400 |
| HELICOPTER | 6 | 0.43 | 3.58 | AH64_GUNSHIP: cost 710, str 85, power 322 |
| ROBOT | 6 | 0.53 | 4.51 | SIEGE_DROID: cost 1600, str 175, power 825 |
| DREADNOUGHT | 5 | 0.54 | 4.50 | THERMOBARIC_TANK: cost 1300, str 140, power 620 |
| ASSAULT_MECH | 4 | 0.59 | 4.59 | SCOUT_MECH: cost 1400, str 170, power 795 |
| ANIMAL | 3 | 0.13 | 1.50 | WARDOG: cost 30, str 4, power 6 |
| CLONES | 3 | 1.03 | 4.40 | BLEEDER: cost 600, str 140, power 616 |
| RECON | 2 | 0.24 | 4.35 | MOTORCYCLE: cost 220, str 26, power 70 |
| NANITE | 2 | 0.62 | 5.21 | NANITE_CLOUD: cost 3000, str 360, power 2100 |

- Unit AI roles allowed, by combat type (how often):

| Combat type | Roles |
|---|---|
| ANIMAL | ATTACK 3, RESERVE 3, COUNTER 3, CITY_SPECIAL 1 |
| ARCHER | ATTACK 13, CITY_DEFENSE 11, RESERVE 3, COUNTER 3, CITY_COUNTER 3, COLLATERAL 1, ATTACK_CITY 1 |
| ASSAULT_MECH | ATTACK 4, ATTACK_CITY 4, CITY_SPECIAL 3, CITY_COUNTER 3, COUNTER 1 |
| CLONES | ATTACK 3, CITY_DEFENSE 3, CITY_COUNTER 3, ATTACK_CITY 2, RESERVE 1 |
| DREADNOUGHT | ATTACK 5, ATTACK_CITY 5, PILLAGE 4 |
| GUN | RESERVE 21, ATTACK 20, CITY_DEFENSE 17, ATTACK_CITY 7, CITY_COUNTER 6, COUNTER 4, GENERAL 3, CITY_SPECIAL 3, PILLAGE 2, PARADROP 2 |
| HELICOPTER | ATTACK 5, PILLAGE 5, PARADROP 1 |
| HITECH | COUNTER 7, RESERVE 6, CITY_DEFENSE 6, CITY_SPECIAL 5, ATTACK 4, CITY_COUNTER 3, ATTACK_CITY 2, EXPLORE 1, PILLAGE 1, COLLATERAL 1 |
| MELEE | RESERVE 44, ATTACK_CITY 32, COUNTER 29, ATTACK 27, CITY_COUNTER 23, CITY_DEFENSE 23, PILLAGE 16, WORKER 4, GENERAL 2, EXPLORE 1 |
| MOUNTED | ATTACK 45, PILLAGE 41, COUNTER 20, CITY_COUNTER 8, RESERVE 6, CITY_DEFENSE 6, CITY_SPECIAL 6, WORKER 4, COLLATERAL 1 |
| NANITE | ATTACK_CITY 2, ATTACK 2, CITY_SPECIAL 2 |
| NONE | ANIMAL 12 |
| RECON | EXPLORE 7, MERCHANT 2, ENGINEER 2, CITY_SPECIAL 1, PILLAGE 1 |
| ROBOT | ATTACK 6, ATTACK_CITY 6, CITY_COUNTER 6, COUNTER 4, COLLATERAL 2, PILLAGE 1 |
| SIEGE | ATTACK_CITY 16, COLLATERAL 15, CITY_COUNTER 14, COUNTER 3, CITY_DEFENSE 2, EXPLORE 2, ATTACK 2, CITY_SPECIAL 2 |
| TRACKED | ATTACK 31, ATTACK_CITY 30, PILLAGE 30, RESERVE 2, COUNTER 2, CITY_DEFENSE 2, CITY_SPECIAL 1 |
| WHEELED | COUNTER 6, CITY_COUNTER 6, ATTACK 4, CITY_SPECIAL 3, EXPLORE 3, ATTACK_CITY 3, PILLAGE 3, RESERVE 3, CITY_DEFENSE 3 |

- Building prerequisites of land units: MOUNTED needs STABLE (23); MELEE needs BARRACKS (11); MOUNTED needs KNIGHT_STABLE (11); ARCHER needs ARCHERY_RANGE (10); MELEE needs ARMOURER (9); SIEGE needs SIEGE_WORKSHOP (5); MOUNTED needs BARRACKS (4); ASSAULT_MECH needs MECH_ASSEMBLY_PLANT (4); MELEE needs LEGION_BARRACKS (3); MELEE needs SENATE (2); SIEGE needs FORGE (2); ARCHER needs SIEGE_WORKSHOP (2); SIEGE needs CANNON_FORGE (2); WHEELED needs UN_MISSION (2); MOUNTED needs TEUTONIC_CHAPTER (2); ARCHER needs LEGION_BARRACKS (1); MELEE needs CHICHEN_ITZA (1); MELEE needs CRUSADE (1); GUN needs POLICE_STATION (1); GUN needs UN_MISSION (1).

## Land units

Columns: era, combat type, strength, moves, cost, iPower, first strikes (+chance), withdrawal %, combat limit, collateral % / limit / max units / **effective strength**, ranged strike (range, air combat, limit), bombard rate, ignores building defence, no defensive bonus, city attack / defence %, combat-type modifiers, roles (default first), building prerequisite, source file.

| Unit | Era | Type | Str | Mv | Cost | Pow | FS | Wd | Lim | Coll | Strike | Bomb | IgnB | NoDef | City a/d | Mods | Roles | Needs | Src |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TRAINEDDOG | ANCI | ANIMAL | 3 | 1 | 20 | 1 |  |  |  |  |  |  |  | Y | -50/0 | MOUNTED+25 ARCHER+25 | COUNTER; ATTACK,RESERVE |  | base |
| WARDOG | ANCI | ANIMAL | 4 | 2 | 30 | 6 |  |  |  |  |  |  |  | Y | -50/0 | MOUNTED+25 ARCHER+25 | COUNTER; ATTACK,RESERVE |  | base |
| ARCHER | ANCI | ARCHER | 3 | 1 | 30 | 4 | 1+0 |  |  | 25/50/2/**0** | 1/1/75 |  |  |  | 0/50 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| PELTIST | ANCI | ARCHER | 3 | 1 | 30 | 4 | 1+0 |  |  | 25/50/2/**0** | 1/1/75 |  |  |  | 0/50 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| BABYLON_BOWMAN | ANCI | ARCHER | 3 | 1 | 30 | 5 | 1+0 |  |  | 25/50/2/**0** | 1/1/75 |  |  |  | 0/50 | MELEE+50 | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| MONGOL_JAVELIN_THROWER | ANCI | ARCHER | 4 | 2 | 30 | 5 | 1+0 | 25 |  | 25/50/2/**1** |  |  |  |  | 0/50 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| MALI_SKIRMISHER | ANCI | ARCHER | 4 | 2 | 30 | 5 | 1+1 |  |  | 25/50/2/**1** |  |  |  |  | 0/50 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| ABYSSINIANS_EthiopianArcher | ANCI | ARCHER | 4 | 2 | 30 | 5 | 1+0 |  |  | 25/50/2/**1** | 1/1/75 |  |  |  | 25/50 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| VELITES | ANCI | ARCHER | 4 | 2 | 30 | 6 | 2+0 | 25 |  | 25/50/2/**1** |  |  |  |  |  |  | ATTACK; COLLATERAL,RESERVE,COUNTER,CITY_COUNTER,ATTACK_CITY |  | base |
| SAGITTARII | ANCI | ARCHER | 5 | 1 | 40 | 9 | 1+0 |  |  | 25/80/2/**1** | 1/1/75 |  |  |  | 0/50 |  | CITY_DEFENSE; ATTACK | LEGION_BARRACKS | base |
| JAVELINEER | ANCI | MELEE | 3 | 2 | 25 | 4 | 1+0 | 25 |  |  |  |  |  |  |  |  | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY |  | base |
| NATIVE_AMERICA_DOG_SOLDIER | ANCI | MELEE | 4 | 1 | 40 | 9 |  |  |  |  |  |  |  |  |  | MELEE+100 | COUNTER; ATTACK,ATTACK_CITY,RESERVE,CITY_DEFENSE,PILLAGE |  | base |
| SPEARMAN | ANCI | MELEE | 4 | 1 | 35 | 6 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY |  | base |
| ZULU_IMPI | ANCI | MELEE | 4 | 2 | 35 | 7 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; PILLAGE,RESERVE,CITY_COUNTER,ATTACK_CITY |  | base |
| MAYA_HOLKAN | ANCI | MELEE | 4 | 1 | 35 | 7 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY |  | base |
| AXEMAN | ANCI | MELEE | 5 | 1 | 40 | 8 |  |  |  |  |  |  |  |  |  | MELEE+50 | COUNTER; ATTACK,ATTACK_CITY,RESERVE,CITY_DEFENSE,PILLAGE |  | base |
| INCAN_QUECHUA2 | ANCI | MELEE | 5 | 1 | 40 | 8 |  |  |  |  |  |  |  |  |  | MELEE+50 | COUNTER; ATTACK,ATTACK_CITY,RESERVE,CITY_DEFENSE,PILLAGE |  | base |
| SUMERIAN_VULTURE | ANCI | MELEE | 6 | 1 | 40 | 9 |  |  |  |  |  |  |  |  |  | MELEE+25 | COUNTER; ATTACK,ATTACK_CITY,RESERVE,CITY_DEFENSE,PILLAGE |  | base |
| WARBAND | ANCI | MELEE | 6 | 1 | 45 | 10 |  |  |  |  |  |  |  |  |  | MOUNTED+25 | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY,PILLAGE |  | base |
| CELTIC_WARBAND | ANCI | MELEE | 6 | 2 | 40 | 10 |  |  |  |  |  |  |  |  |  |  | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY,PILLAGE |  | base |
| HASTATI | ANCI | MELEE | 7 | 2 | 50 | 10 | 1+0 | 25 |  |  |  |  |  |  |  | MELEE+25 MOUNTED+25 | COUNTER; ATTACK,ATTACK_CITY,RESERVE,CITY_DEFENSE,WORKER |  | base |
| GREEK_PHALANX | ANCI | MELEE | 7 | 1 | 60 | 8 |  |  |  |  |  |  |  |  | 0/25 | MELEE+50 MOUNTED+50 | COUNTER; ATTACK,ATTACK_CITY,RESERVE,CITY_DEFENSE,PILLAGE |  | base |
| CELTIC_SWORDSMAN | ANCI | MELEE | 7 | 2 | 60 | 14 |  |  |  |  |  |  |  |  |  |  | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY,PILLAGE |  | base |
| SEARAIDER | ANCI | MELEE | 8 | 1 | 60 | 13 |  |  |  |  |  |  |  |  | 15/0 | ARCHER+25 | PILLAGE; ATTACK_CITY,ATTACK,RESERVE,COUNTER,CITY_COUNTER |  | base |
| WARLORDI | ANCI | MELEE | 10 | 1 | 100 | 5 |  |  |  | 10/10/1/**1** |  |  |  |  |  | MOUNTED+25 MELEE+25 | GENERAL;  |  | Modules/Custom Units/Warlord/Warlord_CIV4UnitInfos.xml |
| CHARIOT | ANCI | MOUNTED | 5 | 2 | 30 | 6 |  | 25 |  | 100/50/2/**5** |  |  |  | Y |  |  | ATTACK; COUNTER,PILLAGE | STABLE | base |
| CELTIC_CHARIOT | ANCI | MOUNTED | 5 | 2 | 35 | 8 |  | 50 |  | 100/50/4/**5** |  |  |  | Y |  |  | ATTACK; COLLATERAL,COUNTER,PILLAGE |  | base |
| EGYPT_WARCHARIOT | ANCI | MOUNTED | 6 | 2 | 30 | 7 |  | 25 |  | 100/50/2/**6** |  |  |  | Y |  |  | ATTACK; COUNTER,PILLAGE | STABLE | base |
| HITTITES_HITTITE_CHARIOT | ANCI | MOUNTED | 6 | 2 | 25 | 7 |  | 25 |  | 100/50/2/**6** |  |  |  | Y |  |  | ATTACK; COUNTER,PILLAGE | STABLE | base |
| HORSEMAN | ANCI | MOUNTED | 6 | 2 | 60 | 10 | 0+1 | 25 |  | 25/100/4/**1** |  |  |  | Y |  | ARCHER+25 | ATTACK; PILLAGE | STABLE | base |
| MALI_CAVALRY | ANCI | MOUNTED | 6 | 2 | 60 | 9 | 0+1 | 25 |  | 25/100/4/**1** |  |  |  | Y |  | ARCHER+25 | ATTACK; PILLAGE | STABLE | base |
| PRODROMOI | ANCI | MOUNTED | 6 | 2 | 60 | 12 | 0+1 | 25 |  | 25/100/4/**1** |  |  |  | Y |  | ARCHER+25 | ATTACK; PILLAGE | STABLE | base |
| HORSEMAN_SCYTHIA | ANCI | MOUNTED | 7 | 2 | 50 | 12 | 0+1 | 25 |  | 25/100/4/**1** |  |  |  | Y |  | ARCHER+25 | ATTACK; PILLAGE | STABLE | base |
| ROME_CAVALRY_AUXILIA | ANCI | MOUNTED | 7 | 2 | 60 | 12 | 0+1 | 25 |  | 25/100/4/**1** |  |  |  | Y |  | ARCHER+25 | ATTACK; PILLAGE | STABLE | base |
| PERSIA_IMMORTAL | ANCI | MOUNTED | 8 | 3 | 60 | 7 |  | 25 |  | 50/100/4/**4** |  |  |  |  |  | ARCHER+50 | ATTACK; COUNTER,PILLAGE,CITY_COUNTER | STABLE | base |
| ELEPHANT_RIDER | ANCI | MOUNTED | 8 | 1 | 80 | 8 |  |  |  |  |  |  |  | Y | 25/0 | MOUNTED+50 | ATTACK; COUNTER,WORKER | BARRACKS | base |
| SCOUT | ANCI | RECON | 1 | 2 | 15 | 0 |  |  |  |  |  |  |  |  |  |  | EXPLORE;  |  | base |
| TRADE_CARAVAN | ANCI | RECON | 2 | 2 | 60 | 0 |  |  | 0 |  |  |  |  |  |  |  | MERCHANT; ENGINEER,EXPLORE |  | base |
| EXPLORER | ANCI | RECON | 3 | 2 | 45 | 0 |  |  |  |  |  |  |  |  |  |  | EXPLORE;  |  | base |
| RAM | ANCI | SIEGE | 3 | 1 | 15 | 8 |  |  | 75 |  |  | 5 |  |  |  |  | ATTACK_CITY;  |  | base |
| PIKEMAN | CLAS | MELEE | 6 | 1 | 50 | 10 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER | BARRACKS | base |
| HOLY_ROMAN_LANDSKNECHT | CLAS | MELEE | 6 | 1 | 50 | 11 |  |  |  |  |  |  |  |  |  | MOUNTED+75 MELEE+100 | COUNTER; RESERVE,CITY_COUNTER | BARRACKS | base |
| PIKEMAN_JAPAN_ASHIGARU | CLAS | MELEE | 6 | 1 | 50 | 10 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER | BARRACKS | base |
| TRIARII | CLAS | MELEE | 6 | 1 | 50 | 10 |  |  |  |  |  |  |  |  | 0/25 | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY,CITY_DEFENSE | BARRACKS | base |
| LIGHT_SWORDSMAN | CLAS | MELEE | 7 | 1 | 60 | 12 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | BARRACKS | base |
| HYPASPISTS | CLAS | MELEE | 7 | 1 | 60 | 12 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | BARRACKS | base |
| AZTEC_JAGUAR | CLAS | MELEE | 7 | 1 | 55 | 12 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | BARRACKS | base |
| CELTIC_GALLIC_WARRIOR | CLAS | MELEE | 7 | 1 | 60 | 12 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | BARRACKS | base |
| SARISSA | CLAS | MELEE | 7 | 1 | 40 | 12 |  |  |  |  |  |  |  |  | 0/25 | MOUNTED+100 MELEE+25 | COUNTER; RESERVE,CITY_COUNTER | BARRACKS | base |
| AUXILIAR | CLAS | MELEE | 8 | 1 | 60 | 13 |  |  |  |  |  |  |  |  | 0/25 | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER,ATTACK_CITY,CITY_DEFENSE | LEGION_BARRACKS | base |
| PRINCIPES | CLAS | MELEE | 8 | 2 | 50 | 16 | 1+0 | 25 |  |  |  |  |  |  |  | MELEE+25 MOUNTED+25 | ATTACK; ATTACK_CITY,RESERVE,WORKER | BARRACKS | base |
| AZTEC_EAGLE | CLAS | MELEE | 9 | 1 | 75 | 17 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER | BARRACKS | base |
| HYPASPIST2 | CLAS | MELEE | 9 | 2 | 75 | 20 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK; ATTACK_CITY,RESERVE |  | base |
| ROME_LEGIONARY | CLAS | MELEE | 10 | 2 | 60 | 24 | 1+0 |  |  |  |  |  |  |  |  |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE,WORKER | LEGION_BARRACKS | base |
| COMITATENSES | CLAS | MELEE | 10 | 2 | 75 | 23 | 1+0 |  |  |  |  |  |  |  |  |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE,WORKER | LEGION_BARRACKS | base |
| SWORDSMAN | CLAS | MELEE | 10 | 1 | 85 | 20 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | ARMOURER | base |
| AZTEC_ELITE_JAGUAR | CLAS | MELEE | 10 | 1 | 85 | 20 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | CHICHEN_ITZA | base |
| CENTURIO | CLAS | MELEE | 15 | 2 | 150 | 30 | 1+0 |  |  |  |  |  |  |  |  |  | ATTACK; ATTACK_CITY | SENATE | base |
| ROME_PRAETORIAN | CLAS | MELEE | 16 | 2 | 200 | 14 | 1+0 |  |  |  |  |  |  |  | 0/25 |  | CITY_DEFENSE; RESERVE | SENATE | base |
| MOUNTED_INFANTRY | CLAS | MOUNTED | 8 | 2 | 75 | 15 |  | 20 |  |  |  |  |  |  |  | ARCHER+50 | ATTACK; PILLAGE,RESERVE,COUNTER,CITY_COUNTER,CITY_DEFENSE,CITY_SPECIAL | STABLE | base |
| MONGOL_MOUNTED_SWORDSMAN | CLAS | MOUNTED | 8 | 2 | 75 | 18 |  | 20 |  |  |  |  |  |  |  | ARCHER+50 | ATTACK; PILLAGE,RESERVE,COUNTER,CITY_COUNTER,CITY_DEFENSE,CITY_SPECIAL | STABLE | base |
| ROME_CAVALRY | CLAS | MOUNTED | 8 | 2 | 80 | 15 |  | 20 |  |  |  |  |  |  |  | ARCHER+50 | ATTACK; PILLAGE,RESERVE,COUNTER,CITY_COUNTER,CITY_DEFENSE,CITY_SPECIAL | STABLE | base |
| DUTCH_BATAVIAN_CAVALRY | CLAS | MOUNTED | 8 | 2 | 80 | 15 |  | 20 |  |  |  |  |  |  |  | ARCHER+50 | ATTACK; PILLAGE,RESERVE,COUNTER,CITY_COUNTER,CITY_DEFENSE,CITY_SPECIAL | STABLE | base |
| MOUNTED_INFANTRY_SCYTHIA | CLAS | MOUNTED | 9 | 2 | 75 | 18 |  | 20 |  |  |  |  |  |  |  | ARCHER+50 | ATTACK; PILLAGE,RESERVE,COUNTER,CITY_COUNTER,CITY_DEFENSE,CITY_SPECIAL | STABLE | base |
| NORSE_WARHORSE | CLAS | MOUNTED | 9 | 2 | 80 | 18 |  | 25 |  | 25/100/2/**2** |  |  |  |  |  |  | ATTACK; PILLAGE,RESERVE,COUNTER,CITY_COUNTER,CITY_DEFENSE,CITY_SPECIAL | STABLE | base |
| HORSE_ARCHER | CLAS | MOUNTED | 10 | 2 | 90 | 25 | 1+1 | 20 |  | 25/100/6/**2** | 1/1/75 |  |  | Y |  |  | ATTACK; PILLAGE | STABLE | base |
| CARTHAGE_NUMIDIAN_CAVALRY | CLAS | MOUNTED | 10 | 2 | 80 | 25 | 1+1 | 50 |  | 50/100/6/**5** |  |  |  | Y |  | MELEE+50 | ATTACK; PILLAGE,COUNTER | STABLE | base |
| MONGOL_KESHIK | CLAS | MOUNTED | 10 | 3 | 80 | 25 | 1+1 | 20 |  | 25/100/6/**2** | 1/1/80 |  |  | Y |  |  | ATTACK; PILLAGE | STABLE | base |
| LIGHT_CAVALRY | CLAS | MOUNTED | 10 | 2 | 70 | 20 | 1+0 | 40 |  | 25/100/3/**2** |  |  |  | Y | -20/0 | ARCHER+25 MELEE+25 | ATTACK; PILLAGE,COUNTER | STABLE | base |
| ARABIAN_ANSAR | CLAS | MOUNTED | 10 | 2 | 70 | 15 |  | 40 |  | 25/100/3/**2** |  |  |  | Y | -20/0 | ARCHER+25 MELEE+25 | ATTACK; PILLAGE,COUNTER | STABLE | base |
| COMPANION_CAVALRY | CLAS | MOUNTED | 12 | 2 | 100 | 25 | 1+1 | 25 |  | 25/100/6/**3** |  |  |  | Y |  |  | ATTACK; PILLAGE | STABLE | base |
| HEAVY_CAVALRY | CLAS | MOUNTED | 12 | 2 | 150 | 25 |  | 25 |  | 25/100/5/**3** |  |  |  | Y | -10/0 | MELEE+25 | ATTACK; PILLAGE,COUNTER | STABLE | base |
| BYZANTINE_CATAPHRACT | CLAS | MOUNTED | 14 | 2 | 150 | 30 |  |  |  | 50/100/6/**7** |  |  |  | Y |  |  | ATTACK; PILLAGE | STABLE | base |
| KHMER_BALLISTA_ELEPHANT | CLAS | MOUNTED | 18 | 2 | 200 | 20 |  |  |  | 25/100/8/**4** | 1/1/50 |  |  | Y |  | MOUNTED+50 | ATTACK; COUNTER,WORKER | BARRACKS | base |
| WAR_ELEPHANT | CLAS | MOUNTED | 20 | 2 | 400 | 20 |  |  |  | 25/100/10/**5** |  |  |  | Y |  | MOUNTED+50 | ATTACK; COUNTER,WORKER | BARRACKS | base |
| SIAM_ELEPHANT | CLAS | MOUNTED | 20 | 2 | 200 | 17 |  |  |  | 25/100/8/**5** |  |  |  | Y |  | MOUNTED+50 | ATTACK; COUNTER,WORKER | BARRACKS | base |
| BALLISTA | CLAS | SIEGE | 5 | 1 | 60 | 10 |  | 50 |  | 100/50/1/**5** | 1/1/50 | 4 |  |  | 50/50 | MOUNTED+100 | CITY_DEFENSE; COLLATERAL,COUNTER,ATTACK_CITY,EXPLORE | FORGE | base |
| BALLISTA_ROME | CLAS | SIEGE | 5 | 1 | 60 | 10 |  | 50 |  | 100/50/1/**5** | 1/1/50 | 4 |  |  | 50/50 | MOUNTED+100 | CITY_DEFENSE; COLLATERAL,COUNTER,ATTACK_CITY,EXPLORE | FORGE | base |
| CATAPULT | CLAS | SIEGE | 6 | 1 | 50 | 10 |  |  | 75 | 100/50/6/**6** | 1/1/50 | 8 |  | Y | 50/0 |  | ATTACK_CITY; COLLATERAL,CITY_COUNTER | SIEGE_WORKSHOP | base |
| ANCIENT_CANNON | CLAS | SIEGE | 6 | 1 | 50 | 10 |  |  | 75 | 100/50/6/**6** | 1/1/50 | 8 |  | Y | 50/0 |  | ATTACK_CITY; COLLATERAL,CITY_COUNTER | SIEGE_WORKSHOP | base |
| KOREAN_HWACHA | CLAS | SIEGE | 6 | 1 | 50 | 12 |  |  | 75 | 100/50/6/**6** | 1/1/50 | 8 |  | Y | 50/0 | MELEE+50 | ATTACK_CITY; COLLATERAL,COUNTER,CITY_COUNTER | SIEGE_WORKSHOP | base |
| ASSYRIA_RAM | CLAS | SIEGE | 6 | 1 | 40 | 12 |  |  | 75 | 100/50/6/**6** |  | 8 |  | Y | 75/0 |  | ATTACK_CITY; COLLATERAL,CITY_COUNTER | SIEGE_WORKSHOP | base |
| LONGBOWMAN | MEDI | ARCHER | 8 | 1 | 65 | 15 | 1+0 |  |  | 25/80/3/**2** | 1/1/90 |  |  |  | 0/25 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| ENGLISH_LONGBOWMAN | MEDI | ARCHER | 8 | 1 | 65 | 16 | 2+0 |  |  | 30/80/4/**2** | 1/1/90 |  |  |  | 0/25 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| IROQUOIS_MOHAWKARCHER | MEDI | ARCHER | 8 | 2 | 65 | 16 | 1+0 |  |  | 25/75/3/**2** | 1/1/80 |  |  |  | 0/25 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| YUMISAMURAI | MEDI | ARCHER | 8 | 1 | 65 | 15 | 1+0 |  |  | 30/80/3/**2** | 1/1/90 |  |  |  | 0/25 |  | CITY_DEFENSE; ATTACK | ARCHERY_RANGE | base |
| CROSSBOWMAN | MEDI | ARCHER | 9 | 1 | 75 | 17 | 1+0 |  |  |  | 1/1/90 |  |  |  |  | MELEE+50 | COUNTER; ATTACK,RESERVE,CITY_COUNTER | SIEGE_WORKSHOP | base |
| CHINA_CHOKONU | MEDI | ARCHER | 9 | 1 | 75 | 19 | 2+0 |  |  | 50/60/5/**4** | 1/1/90 |  |  |  |  | MELEE+50 | COUNTER; ATTACK,RESERVE,CITY_COUNTER | SIEGE_WORKSHOP | base |
| HEAVY_PIKEMAN | MEDI | MELEE | 9 | 1 | 75 | 17 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER | ARMOURER | base |
| JAPAN_HEAVY_ASHIGARU | MEDI | MELEE | 9 | 1 | 75 | 17 |  |  |  |  |  |  |  |  |  | MOUNTED+50 | COUNTER; RESERVE,CITY_COUNTER | ARMOURER | base |
| MACEMAN | MEDI | MELEE | 10 | 1 | 85 | 20 |  |  |  |  |  |  |  |  |  | MELEE+50 | COUNTER; ATTACK,RESERVE,CITY_COUNTER,PILLAGE | ARMOURER | base |
| JAPAN_SAMURAI | MEDI | MELEE | 11 | 1 | 85 | 22 | 2+0 |  |  |  |  |  |  |  |  | MELEE+50 | COUNTER; ATTACK,RESERVE,CITY_COUNTER,PILLAGE | ARMOURER | base |
| VIKING_BESERKER | MEDI | MELEE | 11 | 1 | 85 | 22 |  |  |  |  |  |  |  |  | 10/0 | MELEE+50 | COUNTER; ATTACK_CITY,ATTACK,RESERVE,CITY_COUNTER,PILLAGE | ARMOURER | base |
| HEAVY_SWORDSMAN | MEDI | MELEE | 13 | 1 | 110 | 28 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | ARMOURER | base |
| GERMAN_TEUTONIC | MEDI | MELEE | 13 | 1 | 110 | 28 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | ARMOURER | base |
| CARTHAGE_SACRED_BAND | MEDI | MELEE | 13 | 1 | 110 | 28 |  |  |  |  |  |  |  |  | 10/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_DEFENSE | ARMOURER | base |
| WARLORDII | MEDI | MELEE | 15 | 1 | 200 | 12 |  | 10 |  | 20/20/2/**3** |  | 8 |  |  | 25/0 | MOUNTED+25 | GENERAL;  |  | Modules/Custom Units/Warlord/Warlord_CIV4UnitInfos.xml |
| CRUSADER | MEDI | MELEE | 15 | 2 | -1 | 34 |  |  |  |  |  |  |  |  |  |  | ATTACK_CITY; ATTACK,EXPLORE,PILLAGE,RESERVE,CITY_DEFENSE | CRUSADE | base |
| ARABIA_CAMELARCHER | MEDI | MOUNTED | 12 | 2 | 90 | 30 |  | 25 |  | 25/100/6/**3** | 1/1/80 |  |  | Y |  |  | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| KNIGHT | MEDI | MOUNTED | 14 | 2 | 120 | 30 |  |  |  | 50/100/6/**7** |  |  |  | Y |  |  | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| PERSIA_SIPAHI | MEDI | MOUNTED | 14 | 2 | 120 | 30 |  |  |  | 50/100/6/**7** |  |  |  | Y |  |  | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| CHIVALRY | MEDI | MOUNTED | 16 | 2 | 130 | 35 |  |  |  | 50/100/6/**8** |  |  |  | Y | -30/0 |  | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| FRENCH_CHIVALRY | MEDI | MOUNTED | 16 | 2 | 130 | 35 |  |  |  | 50/100/6/**8** |  |  |  | Y | -30/0 |  | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| GERMAN_CHIVALRY | MEDI | MOUNTED | 16 | 2 | 130 | 35 |  |  |  | 50/100/6/**8** |  |  |  | Y | -30/0 |  | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| ADVENTURER | MEDI | RECON | 7 | 2 | 140 | 0 |  |  |  |  |  |  |  |  |  |  | EXPLORE;  |  | base |
| TREBUCHET | MEDI | SIEGE | 8 | 1 | 75 | 15 |  |  | 75 | 100/50/6/**8** | 1/1/50 | 16 |  | Y | 75/0 |  | ATTACK_CITY; COLLATERAL,ATTACK,CITY_COUNTER | SIEGE_WORKSHOP | base |
| GUARDDOG | RENA | ANIMAL | 7 | 2 | 90 | 12 |  |  |  |  |  |  |  | Y | -50/25 | MOUNTED+25 ARCHER+25 | COUNTER; ATTACK,RESERVE,CITY_SPECIAL |  | base |
| ARQUEBUSIER | RENA | GUN | 15 | 1 | 100 | 34 | 1+0 |  |  |  |  |  |  |  |  |  | ATTACK; RESERVE,CITY_DEFENSE |  | base |
| GRENADIER | RENA | GUN | 18 | 1 | 150 | 43 |  |  |  |  |  |  | Y |  | 25/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_COUNTER |  | base |
| MUSKETMAN | RENA | GUN | 20 | 1 | 180 | 49 |  |  |  |  |  |  |  |  |  |  | ATTACK; RESERVE,CITY_DEFENSE |  | base |
| MINUTEMAN | RENA | GUN | 20 | 1 | 180 | 49 |  |  |  |  |  |  |  |  |  |  | ATTACK; RESERVE,CITY_DEFENSE |  | base |
| FRENCH_MUSKETEER | RENA | GUN | 20 | 2 | 180 | 52 |  |  |  |  |  |  |  |  |  |  | ATTACK; PILLAGE,RESERVE,CITY_DEFENSE |  | base |
| OTTOMAN_JANISSARY | RENA | GUN | 20 | 1 | 180 | 52 |  |  |  |  |  |  |  |  |  | MELEE+25 ARCHER+25 MOUNTED+25 | ATTACK; RESERVE,CITY_DEFENSE |  | base |
| ETHIOPIAN_OROMO_WARRIOR | RENA | GUN | 20 | 1 | 180 | 52 | 1+0 |  |  |  |  |  |  |  |  |  | ATTACK; RESERVE,CITY_DEFENSE |  | base |
| WARLORDIII | RENA | GUN | 25 | 1 | 300 | 20 |  | 15 |  | 30/30/3/**7** |  | 12 |  |  | 25/0 | ANIMAL+50 MELEE+50 ARCHER+25 MOUNTED+25 | GENERAL;  |  | Modules/Custom Units/Warlord/Warlord_CIV4UnitInfos.xml |
| RIFLEMAN | RENA | GUN | 26 | 1 | 230 | 69 |  |  |  |  |  |  |  |  |  | MOUNTED+25 | CITY_DEFENSE; ATTACK,RESERVE |  | base |
| ENGLISH_REDCOAT | RENA | GUN | 26 | 1 | 230 | 69 |  |  |  |  |  |  |  |  |  | MOUNTED+25 GUN+25 | CITY_DEFENSE; ATTACK,RESERVE |  | base |
| CUIRASSIER | RENA | MOUNTED | 21 | 2 | 180 | 52 |  | 15 |  | 25/100/6/**5** |  |  |  | Y |  | ANIMAL+50 | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| SPANISH_CONQUISTADOR | RENA | MOUNTED | 21 | 2 | 180 | 54 |  | 15 |  | 25/100/6/**5** |  |  |  |  |  | MELEE+50 ANIMAL+50 | ATTACK; PILLAGE,COUNTER,CITY_COUNTER | KNIGHT_STABLE | base |
| MEDIC | RENA | RECON | 5 | 1 | 180 | 30 |  | 50 |  |  |  |  |  | Y |  |  | CITY_SPECIAL; EXPLORE |  | base |
| BOMBARD | RENA | SIEGE | 11 | 1 | 140 | 23 |  |  | 80 | 100/60/6/**11** | 1/1/50 | 10 | Y | Y | 50/0 |  | ATTACK_CITY; COLLATERAL,CITY_COUNTER | CANNON_FORGE | base |
| CANNON | RENA | SIEGE | 16 | 1 | 190 | 37 |  |  | 80 | 100/60/7/**16** | 1/1/50 | 12 | Y | Y | 50/0 |  | ATTACK_CITY; COLLATERAL,CITY_COUNTER | CANNON_FORGE | base |
| GUERRILLA | INDU | GUN | 29 | 1 | 240 | 80 |  |  |  |  |  |  |  |  |  |  | CITY_DEFENSE; ATTACK,ATTACK_CITY,PILLAGE,COUNTER |  | base |
| INFANTRY | INDU | GUN | 34 | 1 | 280 | 97 |  |  |  |  |  |  |  |  | 0/25 | GUN+25 | CITY_DEFENSE; ATTACK,RESERVE |  | base |
| MODERN_GRENADIER | INDU | GUN | 34 | 1 | 280 | 98 |  |  |  |  |  |  | Y |  | 25/0 |  | ATTACK_CITY; ATTACK,RESERVE,CITY_COUNTER |  | base |
| MARINE | INDU | GUN | 39 | 1 | 320 | 117 |  |  |  |  |  |  |  |  |  |  | ATTACK; ATTACK_CITY,RESERVE,CITY_DEFENSE |  | base |
| AMERICAN_NAVY_SEAL | INDU | GUN | 39 | 1 | 320 | 125 | 1+1 |  |  |  |  |  |  |  |  |  | ATTACK; ATTACK_CITY,RESERVE,CITY_DEFENSE |  | base |
| FRENCH_MARINE | INDU | GUN | 39 | 1 | 320 | 117 |  |  |  |  |  |  |  |  |  |  | ATTACK; ATTACK_CITY,RESERVE,CITY_DEFENSE |  | base |
| WARLORDIV | INDU | GUN | 40 | 1 | 400 | 15 |  | 20 |  | 40/40/4/**16** |  | 16 |  |  | 25/0 | ANIMAL+100 MELEE+100 ARCHER+50 MOUNTED+25 | GENERAL;  |  | Modules/Custom Units/Warlord/Warlord_CIV4UnitInfos.xml |
| WARLORDV | INDU | GUN | 60 | 2 | 500 | 20 |  | 25 |  | 50/50/5/**30** |  | 20 |  |  | 25/0 |  | GENERAL;  |  | Modules/Custom Units/Warlord/Warlord_CIV4UnitInfos.xml |
| CAVALRY | INDU | MOUNTED | 27 | 2 | 270 | 72 |  | 30 |  | 25/100/6/**6** |  |  |  | Y |  | ANIMAL+50 | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| RUSSIA_COSSACK | INDU | MOUNTED | 27 | 2 | 270 | 75 |  | 30 |  | 25/100/6/**6** |  |  |  | Y |  | ANIMAL+50 MOUNTED+50 | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| FRENCH_DRAGOON | INDU | MOUNTED | 27 | 2 | 270 | 72 |  | 30 |  | 25/100/6/**6** |  |  |  | Y |  | ANIMAL+50 | ATTACK; PILLAGE | KNIGHT_STABLE | base |
| FREIGHT | INDU | RECON | 5 | 2 | 400 | 0 |  |  | 0 |  |  |  |  |  |  |  | MERCHANT; ENGINEER,EXPLORE |  | base |
| MOTORCYCLE | INDU | RECON | 26 | 2 | 220 | 70 |  | 10 |  |  |  |  |  |  |  |  | EXPLORE; PILLAGE |  | base |
| LIGHT_ARTILLERY | INDU | SIEGE | 20 | 2 | 240 | 50 |  | 20 | 85 | 75/50/4/**15** | 1/1/50 | 14 | Y | Y | 50/0 | SIEGE+50 MELEE+100 ARCHER+100 | ATTACK_CITY; COLLATERAL,CITY_COUNTER |  | base |
| ARTILLERY | INDU | SIEGE | 24 | 1 | 300 | 62 |  |  | 85 | 100/70/8/**24** | 1/2/50 | 16 | Y | Y | 50/0 | SIEGE+50 MELEE+100 ARCHER+100 | ATTACK_CITY; COLLATERAL,CITY_COUNTER |  | base |
| MACHINE_GUN | INDU | SIEGE | 30 | 1 | 250 | 83 | 1+0 |  |  |  |  |  |  |  |  | GUN+50 MOUNTED+50 ARCHER+75 MELEE+100 ANIMAL+100 | CITY_SPECIAL; CITY_COUNTER |  | base |
| FLAMETHROWER | INDU | SIEGE | 36 | 1 | 300 | 105 |  |  |  |  |  |  |  | Y | 20/20 | MELEE+100 ANIMAL+100 | CITY_SPECIAL; ATTACK,ATTACK_CITY,COLLATERAL,CITY_COUNTER |  | base |
| EARLY_TANK | INDU | TRACKED | 36 | 2 | 300 | 105 |  |  |  |  |  |  | Y | Y |  |  | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| FT17 | INDU | TRACKED | 36 | 2 | 300 | 105 |  |  |  |  |  |  | Y | Y |  |  | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| FT17US | INDU | TRACKED | 36 | 2 | 300 | 105 |  |  |  |  |  |  | Y | Y |  |  | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| FT17S | INDU | TRACKED | 36 | 2 | 300 | 105 |  |  |  |  |  |  | Y | Y |  |  | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| A7V | INDU | TRACKED | 36 | 2 | 300 | 105 |  |  |  |  |  |  | Y | Y |  |  | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| WHIPPET | INDU | TRACKED | 36 | 2 | 300 | 105 |  |  |  |  |  |  | Y | Y |  |  | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| LIGHT_TANK | INDU | TRACKED | 41 | 2 | 335 | 125 |  |  |  |  |  |  | Y | Y |  | MOUNTED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| L640 | INDU | TRACKED | 41 | 2 | 335 | 125 |  |  |  |  |  |  | Y | Y |  | MOUNTED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| M3A1 | INDU | TRACKED | 41 | 2 | 335 | 125 |  |  |  |  |  |  | Y | Y |  | MOUNTED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| BT2 | INDU | TRACKED | 41 | 2 | 335 | 125 |  |  |  |  |  |  | Y | Y |  | MOUNTED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| PZKPFWII | INDU | TRACKED | 41 | 2 | 335 | 125 |  |  |  |  |  |  | Y | Y |  | MOUNTED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| R35 | INDU | TRACKED | 41 | 2 | 335 | 125 |  |  |  |  |  |  | Y | Y |  | MOUNTED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| TANK | INDU | TRACKED | 50 | 2 | 420 | 161 |  |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| TANK_CHARBIS | INDU | TRACKED | 50 | 2 | 420 | 161 |  |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| TANK_CHURCHILL | INDU | TRACKED | 50 | 2 | 420 | 161 |  |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| TANK_M4A3 | INDU | TRACKED | 50 | 2 | 420 | 161 |  |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| TANK_PZKPFWIVAUSFF | INDU | TRACKED | 50 | 2 | 420 | 161 |  |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| TANK_T34 | INDU | TRACKED | 50 | 2 | 420 | 161 |  |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| GERMAN_PANZER | INDU | TRACKED | 50 | 2 | 420 | 165 |  |  |  |  |  |  | Y | Y |  | TRACKED+50 WHEELED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| HEAVY_TANK_M26 | INDU | TRACKED | 60 | 1 | 500 | 205 |  |  |  |  |  |  | Y | Y |  | TRACKED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| HEAVY_TANK_IS2 | INDU | TRACKED | 60 | 1 | 500 | 205 |  |  |  |  |  |  | Y | Y |  | TRACKED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| HEAVY_TANK_PZKPFWVI | INDU | TRACKED | 60 | 1 | 500 | 205 |  |  |  |  |  |  | Y | Y |  | TRACKED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| LIGHT_AA | INDU | WHEELED | 29 | 1 | 240 | 80 |  |  | 85 |  |  |  |  |  |  | TRACKED-25 | CITY_COUNTER; COUNTER,CITY_SPECIAL |  | base |
| ARMORED_CAR | INDU | WHEELED | 36 | 2 | 300 | 105 |  | 10 |  |  |  |  |  |  |  | TRACKED-25 | EXPLORE; ATTACK,ATTACK_CITY,PILLAGE,CITY_COUNTER |  | base |
| JEEP | INDU | WHEELED | 38 | 2 | 320 | 113 |  | 10 |  |  |  |  |  | Y |  | MOUNTED+25 TRACKED-25 | EXPLORE; ATTACK,ATTACK_CITY,PILLAGE,CITY_COUNTER |  | base |
| HALFTRACK | INDU | WHEELED | 40 | 2 | 350 | 120 |  |  | 90 |  |  |  |  |  |  | TRACKED-25 | CITY_COUNTER; COUNTER,CITY_SPECIAL |  | base |
| RIOTPOLICE | MODE | GUN | 25 | 1 | 210 | 66 |  |  |  |  |  |  |  |  | 0/20 | MELEE+75 | CITY_SPECIAL; RESERVE,CITY_DEFENSE,CITY_COUNTER | POLICE_STATION | base |
| PARATROOPER | MODE | GUN | 40 | 1 | 340 | 120 |  |  |  |  |  |  | Y |  | 25/0 |  | PARADROP;  |  | base |
| MERCENARY1 | MODE | GUN | 40 | 2 | 200 | 120 |  | 50 |  |  |  |  |  |  | 0/-50 | GUN+50 MOUNTED+50 | ATTACK; RESERVE |  | base |
| PEACE_KEEPER | MODE | GUN | 42 | 1 | 360 | 12 |  |  |  |  |  |  | Y |  |  |  | ATTACK; RESERVE,CITY_DEFENSE | UN_MISSION | Modules/Custom Units/UNPeaceKeeper/Peace_CIV4UnitInfos.xml |
| BAZOOKA | MODE | GUN | 45 | 1 | 375 | 140 |  |  |  |  |  |  | Y |  |  | GUN-50 TRACKED+50 WHEELED+50 | COUNTER; ATTACK,RESERVE,CITY_COUNTER |  | base |
| AT_INFANTRY | MODE | GUN | 50 | 1 | 540 | 162 |  |  |  |  |  |  | Y |  |  | GUN-50 TRACKED+50 WHEELED+50 | COUNTER; CITY_COUNTER,RESERVE,CITY_SPECIAL |  | base |
| MODERN_INFANTRY | MODE | GUN | 50 | 1 | 420 | 162 |  |  |  |  |  |  |  |  | 0/25 | GUN+25 | CITY_DEFENSE; ATTACK,RESERVE |  | base |
| SAM_INFANTRY | MODE | GUN | 54 | 1 | 450 | 178 |  |  |  |  |  |  | Y |  |  | HELICOPTER+75 | COUNTER; CITY_COUNTER,CITY_SPECIAL |  | base |
| MODERN_MARINE | MODE | GUN | 55 | 1 | 460 | 183 | 0+1 |  |  |  |  |  |  |  |  |  | ATTACK; ATTACK_CITY,RESERVE,CITY_DEFENSE |  | base |
| MODERN_PARATROOPER | MODE | GUN | 58 | 1 | 490 | 196 |  |  |  |  |  |  | Y |  | 25/0 |  | PARADROP;  |  | base |
| SPECIAL_FORCES | MODE | GUN | 60 | 2 | 500 | 205 | 1+1 | 20 |  |  |  | 10 | Y |  | 50/0 | GUN+25 | ATTACK;  |  | base |
| UN_26 | MODE | HELICOPTER | 27 | 4 | 400 | 12 |  |  |  |  |  |  |  | Y |  | TRACKED+25 WHEELED+25 | ATTACK;  | UN_MISSION | Modules/Custom Units/UN Transport Helicopter/UN_26_CIV4UnitInfos.xml |
| MI26 | MODE | HELICOPTER | 29 | 4 | 480 | 80 |  | 20 |  |  |  |  | Y | Y |  |  | ATTACK; PILLAGE |  | base |
| GUNSHIP | MODE | HELICOPTER | 58 | 4 | 480 | 196 |  | 25 |  |  |  |  | Y | Y |  | TRACKED+100 WHEELED+100 | ATTACK; PILLAGE |  | base |
| AH64_GUNSHIP | MODE | HELICOPTER | 85 | 5 | 710 | 322 |  | 30 |  |  |  |  | Y | Y |  | TRACKED+100 WHEELED+100 | ATTACK; PILLAGE |  | base |
| DRONE | MODE | ROBOT | 56 | 3 | 400 | 187 |  | 30 |  | 50/100/8/**28** |  |  | Y | Y | 50/0 | TRACKED+100 WHEELED+100 | ATTACK; ATTACK_CITY,PILLAGE,COUNTER,CITY_COUNTER |  | base |
| MOBILE_ARTILLERY | MODE | SIEGE | 48 | 2 | 400 | 153 |  |  | 85 | 100/70/8/**48** | 1/2/50 | 16 | Y | Y |  | SIEGE+50 MOUNTED+50 | ATTACK_CITY; COLLATERAL,CITY_COUNTER |  | base |
| ROCKET_ARTILLERY | MODE | SIEGE | 65 | 2 | 550 | 230 |  |  | 90 | 100/80/10/**65** | 1/1/50 | 20 | Y | Y |  | SIEGE+50 MOUNTED+50 | ATTACK_CITY; COLLATERAL,CITY_COUNTER |  | base |
| UN_IFV | MODE | TRACKED | 70 | 2 | 500 | 25 |  |  |  |  |  |  |  |  |  |  | CITY_DEFENSE; RESERVE,COUNTER | UN_MISSION | Modules/Custom Units/UN Peacekeeper IFV/UN_IFV_CIV4UnitInfos.xml |
| MECHANIZED_INFANTRY | MODE | TRACKED | 70 | 2 | 590 | 250 |  |  |  |  |  |  |  |  | 0/25 | WHEELED+50 | CITY_DEFENSE; ATTACK,RESERVE,COUNTER,CITY_SPECIAL |  | base |
| ARMOR_M60 | MODE | TRACKED | 72 | 2 | 600 | 260 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| ARMOR_CENTURION | MODE | TRACKED | 72 | 2 | 600 | 260 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| ARMOR_T72TAN | MODE | TRACKED | 72 | 2 | 600 | 260 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+25 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| MODERN_ARMOR | MODE | TRACKED | 105 | 2 | 875 | 425 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| MODERN_ARMOR_2A5 | MODE | TRACKED | 105 | 2 | 875 | 425 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| MODERN_ARMOR_T84 | MODE | TRACKED | 105 | 2 | 875 | 425 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| MODERN_ARMOR_TYPE99 | MODE | TRACKED | 105 | 2 | 875 | 425 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| T95 | MODE | TRACKED | 120 | 2 | 1000 | 505 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| UN_APC | MODE | WHEELED | 45 | 3 | 420 | 22 |  |  |  |  |  |  |  |  |  | WHEELED+50 | CITY_DEFENSE; RESERVE,COUNTER | UN_MISSION | Modules/Custom Units/UN APC/UN_APC_CIV4UnitInfos.xml |
| UN_MI | MODE | WHEELED | 48 | 3 | 400 | 23 |  |  |  |  |  |  |  |  |  | GUN+50 | CITY_DEFENSE; RESERVE,COUNTER | UN_MISSION | Modules/Custom Units/UN Motorized Infantry/UN_MI_CIV4UnitInfos.xml |
| BTR80 | MODE | WHEELED | 50 | 2 | 420 | 25 |  |  |  |  |  |  |  | Y |  | TRACKED-25 | CITY_DEFENSE; ATTACK,RESERVE,COUNTER |  | base + base |
| HUMVEE | MODE | WHEELED | 55 | 3 | 460 | 183 | 1+0 | 20 |  |  |  |  |  | Y |  | TRACKED-25 | EXPLORE; ATTACK,ATTACK_CITY,PILLAGE,CITY_COUNTER |  | base |
| MOBILE_SAM | MODE | WHEELED | 70 | 2 | 580 | 250 |  |  |  |  |  |  | Y | Y |  | HELICOPTER+200 TRACKED-25 | COUNTER; CITY_COUNTER,CITY_SPECIAL |  | base |
| POWER_ARMORED_INFANTRY | TRAN | ASSAULT_MECH | 120 | 2 | 900 | 500 | 1+0 | 15 |  |  | 1/35/50 | 10 | Y |  | 10/0 |  | ATTACK; ATTACK_CITY,CITY_SPECIAL,CITY_COUNTER | MECH_ASSEMBLY_PLANT | base |
| ANTI_PERSONNEL_MECH | TRAN | ASSAULT_MECH | 150 | 3 | 1000 | 675 |  | 25 |  |  |  | 8 | Y |  |  |  | ATTACK; ATTACK_CITY,COUNTER,CITY_COUNTER | MECH_ASSEMBLY_PLANT | base |
| SCOUT_MECH | TRAN | ASSAULT_MECH | 170 | 3 | 1400 | 795 | 1+0 | 25 |  |  | 1/50/50 | 15 | Y |  | 10/0 |  | ATTACK; ATTACK_CITY,CITY_SPECIAL,CITY_COUNTER | MECH_ASSEMBLY_PLANT | base |
| ASSAULT_MECH | TRAN | ASSAULT_MECH | 220 | 2 | 1800 | 1100 | 1+0 | 15 |  |  | 2/70/50 | 25 | Y |  | 10/0 |  | ATTACK; ATTACK_CITY,CITY_SPECIAL | MECH_ASSEMBLY_PLANT | base |
| AUTOMATONS | TRAN | CLONES | 70 | 1 | 350 | 250 |  |  |  |  |  |  |  |  |  |  | CITY_DEFENSE; ATTACK,RESERVE,CITY_COUNTER | CLONING_LABORATORY | base |
| BLEEDER | TRAN | CLONES | 140 | 4 | 600 | 616 |  |  |  |  |  |  | Y |  |  |  | ATTACK_CITY; ATTACK,CITY_COUNTER,CITY_DEFENSE |  | base |
| FERAL | TRAN | CLONES | 190 | 4 | 800 | 920 |  |  |  |  |  |  | Y |  |  |  | ATTACK_CITY; ATTACK,CITY_COUNTER,CITY_DEFENSE |  | base |
| STEALTH_ARMOR | TRAN | DREADNOUGHT | 140 | 3 | 1200 | 620 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+50 TRACKED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| THERMOBARIC_TANK | TRAN | DREADNOUGHT | 140 | 2 | 1300 | 620 | 1+0 |  |  |  |  | 20 | Y | Y | 25/0 |  | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| FUTURE_ARMOR | TRAN | DREADNOUGHT | 150 | 3 | 1250 | 675 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+50 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| PLASMA_ARMOR | TRAN | DREADNOUGHT | 170 | 3 | 1400 | 800 | 1+0 |  |  |  |  |  | Y | Y |  | WHEELED+100 TRACKED+100 | ATTACK; ATTACK_CITY,PILLAGE |  | base |
| DREADNOUGHT | TRAN | DREADNOUGHT | 240 | 3 | 2000 | 1240 | 2+0 |  |  |  |  | 40 | Y | Y |  |  | ATTACK; ATTACK_CITY |  | base |
| HYBRID_GUNSHIP | TRAN | HELICOPTER | 115 | 6 | 1000 | 480 |  | 30 |  |  |  | 10 | Y | Y |  | TRACKED+100 WHEELED+100 DREADNOUGHT+25 | ATTACK; PILLAGE |  | base |
| DROPSHIP | TRAN | HELICOPTER | 150 | 7 | 1350 | 675 | 1+0 | 30 |  |  |  |  | Y | Y |  | TRACKED+100 WHEELED+100 DREADNOUGHT+25 | PARADROP; ATTACK,PILLAGE |  | base |
| ACV | TRAN | HITECH | 80 | 3 | 670 | 298 | 1+0 | 20 |  |  |  |  |  | Y |  | CLONES+50 | EXPLORE; ATTACK,RESERVE,COUNTER,CITY_DEFENSE,ATTACK_CITY,PILLAGE |  | base |
| CYBORG | TRAN | HITECH | 95 | 2 | 540 | 372 |  | 10 |  |  |  |  |  |  |  |  | COUNTER; CITY_COUNTER,CITY_SPECIAL | CLONING_FACTORY | base |
| FUTURE_APC | TRAN | HITECH | 100 | 3 | 840 | 400 |  |  |  |  |  |  |  |  |  |  | CITY_DEFENSE; ATTACK,RESERVE,COUNTER,CITY_SPECIAL |  | base |
| ACVSAM | TRAN | HITECH | 100 | 3 | 840 | 400 |  | 30 |  |  |  |  | Y |  |  | GUN-25 HITECH-25 CLONES-25 ASSAULT_MECH-25 DREADNOUGHT-25 HELICOPTER+75 | COUNTER; CITY_COUNTER,CITY_SPECIAL,CITY_DEFENSE,RESERVE |  | base |
| TESLA_INFANTRY | TRAN | HITECH | 100 | 2 | 920 | 400 |  |  |  | 110/100/10/**110** |  |  | Y |  | 25/25 | HELICOPTER-100 WHEELED-50 TRACKED-50 | ATTACK_CITY; ATTACK,RESERVE,COUNTER,CITY_DEFENSE,COLLATERAL |  | base |
| SPECIAL_INFANTRY | TRAN | HITECH | 110 | 2 | 920 | 450 |  |  |  |  |  |  | Y |  |  | GUN+50 WHEELED+50 TRACKED+50 | CITY_DEFENSE; ATTACK,RESERVE,COUNTER,CITY_SPECIAL |  | base |
| SPACE_SAM_INFANTRY | TRAN | HITECH | 145 | 2 | 1200 | 645 |  | 30 |  |  |  |  | Y |  |  | HELICOPTER+75 ROBOT+50 SIEGE+50 TRACKED+50 WHEELED+50 GUN-50 HITECH-50 CLONES-50 ASSAULT_MECH-25 DREADNOUGHT-25 | COUNTER; CITY_COUNTER,CITY_SPECIAL,CITY_DEFENSE,RESERVE |  | base |
| NANITE_SWARM | TRAN | NANITE | 160 | 5 | 1350 | 735 |  | 30 |  | 100/100/10/**160** |  |  | Y |  |  |  | ATTACK_CITY; ATTACK,CITY_SPECIAL |  | base |
| NANITE_CLOUD | TRAN | NANITE | 360 | 5 | 3000 | 2100 |  | 30 |  | 100/100/10/**360** |  |  | Y |  |  |  | ATTACK_CITY; ATTACK,CITY_SPECIAL |  | base |
| WALKER | TRAN | ROBOT | 96 | 3 | 600 | 380 |  | 25 |  |  |  |  | Y |  | 0/25 |  | ATTACK; ATTACK_CITY,COUNTER,CITY_COUNTER |  | base |
| ASSAULT_DROID | TRAN | ROBOT | 130 | 2 | 1100 | 560 |  |  |  | 120/70/8/**156** |  | 30 | Y |  | 25/25 |  | ATTACK; ATTACK_CITY,COUNTER,COLLATERAL,CITY_COUNTER |  | base |
| SIEGE_DROID | TRAN | ROBOT | 175 | 2 | 1600 | 825 |  |  |  | 150/85/8/**262** |  | 40 | Y | Y | 25/0 |  | ATTACK_CITY; ATTACK,COUNTER,COLLATERAL,CITY_COUNTER |  | base |
| SENTINEL | TRAN | ROBOT | 220 | 4 | 2000 | 1100 |  |  |  |  | 3/60/75 |  | Y |  |  |  | ATTACK_CITY; ATTACK,CITY_COUNTER |  | base |
| HITECH_ROBOT | TRAN | ROBOT | 290 | 4 | 2400 | 1600 |  |  |  |  | 3/75/75 |  | Y |  |  |  | ATTACK_CITY; ATTACK,CITY_COUNTER |  | base |
| NLOS_CANNON | TRAN | SIEGE | 90 | 3 | 820 | 350 |  |  | 90 | 140/90/10/**126** | 1/2/50 | 26 | Y | Y |  | SIEGE+50 | ATTACK_CITY; COLLATERAL,CITY_COUNTER |  | base |
| WARRIOR | ? | MELEE | 2 | 1 | 10 | 2 |  |  |  |  |  |  |  |  |  |  | ATTACK; PILLAGE,CITY_DEFENSE |  | base |
| INCAN_QUECHUA | ? | MELEE | 2 | 1 | 15 | 3 |  |  |  |  |  |  |  |  | 0/25 | ARCHER+100 | ATTACK; PILLAGE,CITY_DEFENSE |  | base |
| SERGEANT_HOSPITALLER | ? | MELEE | 10 | 1 | 80 | 6 |  |  |  |  |  |  |  |  |  | MOUNTED+100 | ATTACK; RESERVE,COUNTER,CITY_COUNTER | HOSPITALLER_CHAPTER | Modules/Holy Wars/Christianity/Knight Hospitaller/Hospitaller_CIV4UnitInfos.xml |
| SERGEANT_TEMPLAR | ? | MELEE | 10 | 1 | 80 | 6 |  |  |  |  |  |  |  |  |  | MOUNTED+100 | ATTACK; RESERVE,COUNTER,CITY_COUNTER | TEMPLAR_CHAPTER | Modules/Holy Wars/Christianity/Knight Templar/Templar_CIV4UnitInfos.xml |
| SERGEANT_TEUTONIC | ? | MELEE | 10 | 1 | 80 | 6 |  |  |  |  |  |  |  |  |  | MOUNTED+100 | ATTACK; RESERVE,COUNTER,CITY_COUNTER | TEUTONIC_CHAPTER | Modules/Holy Wars/Christianity/Teutonic Knight/Teutonic_CIV4UnitInfos.xml |
| KNIGHT_HOSPITALLER | ? | MOUNTED | 13 | 2 | 120 | 10 |  |  |  |  |  |  |  | Y |  |  | ATTACK; PILLAGE | HOSPITALLER_CHAPTER | Modules/Holy Wars/Christianity/Knight Hospitaller/Hospitaller_CIV4UnitInfos.xml |
| KNIGHT_TEMPLAR | ? | MOUNTED | 13 | 3 | 120 | 10 |  |  |  |  |  |  |  |  |  |  | ATTACK; PILLAGE | TEMPLAR_CHAPTER | Modules/Holy Wars/Christianity/Knight Templar/Templar_CIV4UnitInfos.xml |
| KNIGHT_TEUTONIC | ? | MOUNTED | 13 | 2 | 120 | 10 |  |  |  |  |  |  |  | Y |  |  | ATTACK; PILLAGE | TEUTONIC_CHAPTER | Modules/Holy Wars/Christianity/Teutonic Knight/Teutonic_CIV4UnitInfos.xml |
| MARSHALL_HOSPITALLER | ? | MOUNTED | 17 | 2 | 150 | 11 |  |  |  |  |  |  |  | Y |  |  | ATTACK; PILLAGE | KRAK_DES_CHEVALIERS | Modules/Holy Wars/Christianity/Knight Hospitaller/Hospitaller_CIV4UnitInfos.xml |
| MARSHALL_TEMPLAR | ? | MOUNTED | 17 | 3 | 150 | 11 |  | -100 |  |  |  |  |  | Y |  |  | ATTACK; PILLAGE | AL_AQSA_MOSQUE | Modules/Holy Wars/Christianity/Knight Templar/Templar_CIV4UnitInfos.xml |
| MARSHALL_TEUTONIC | ? | MOUNTED | 17 | 2 | 150 | 11 |  |  |  |  |  |  |  | Y |  | MELEE+25 | ATTACK; PILLAGE | TEUTONIC_CHAPTER | Modules/Holy Wars/Christianity/Teutonic Knight/Teutonic_CIV4UnitInfos.xml |
| LION | ? | NONE | 1 | 1 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| WOLF | ? | NONE | 1 | 2 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| CHEETAH | ? | NONE | 1 | 2 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| LION_PACK | ? | NONE | 2 | 1 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| PANTHER | ? | NONE | 2 | 2 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| BENGALTIGER | ? | NONE | 2 | 2 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| DIREWOLF | ? | NONE | 2 | 2 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| CAVE_LION | ? | NONE | 3 | 1 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| BEAR | ? | NONE | 3 | 1 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| SIBERIANTIGER | ? | NONE | 3 | 2 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| CAVEBEAR | ? | NONE | 3 | 1 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |
| POLARBEAR | ? | NONE | 4 | 1 | -1 | 0 |  |  |  |  |  |  |  | Y |  |  | ANIMAL;  |  | base |

## Promotions with combat effects

| Promotion | Str % | City atk | City def | Hills a/d | Collat % | Bomb % | Wd % | FS | Heal (same/adj) | Combat-type mods | Prereq |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CRUCIBLE_STEEL | 15 |  |  | / |  |  |  |  | / |  | NONE |
| POISON_ARROWS |  |  |  | / |  |  |  |  | / | ANIMAL+25 ARCHER+25 MELEE+25 MOUNTED+25 RECON+25 | NONE |
| SEGMENTED_ARMOR |  |  |  | / |  |  |  |  | / | ARCHER+20 | NONE |
| CHAIN_SHOT |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+15 | NONE |
| GRAPE_SHOT |  |  |  | / |  |  |  |  | / | MELEE+15 ARCHER+15 MOUNTED+15 RECON+15 SIEGE+15 | NONE |
| COPPER_PLATING |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+10 | NONE |
| FUEL_TANK | -15 |  |  | / |  |  |  |  | / |  | NONE |
| LEADER |  |  |  | / |  |  |  | 1 | / |  | NONE |
| HEROIC | 20 | 20 | 20 | / |  |  |  |  | / |  | LEADER |
| TACTICS |  |  |  | / |  |  | 20 |  | / |  | LEADER |
| WALL_BREAKER |  | 15 |  | / | 30 | 3 |  |  | / |  | NONE |
| BERZERKER1 | 20 |  |  | / |  |  |  |  | / |  | NONE |
| BERZERKER2 | 20 |  |  | / |  |  |  |  | / |  | NONE |
| BERZERKER3 | 30 |  |  | / |  |  |  |  | / |  | NONE |
| CRUSADER |  | 25 |  | / |  |  |  |  | / |  | NONE |
| KANAI |  |  |  | / |  |  |  | 2 | / |  | NONE |
| MUJAHID | 15 |  |  | / |  |  |  |  | / | MELEE+15 MOUNTED+15 | NONE |
| ORDER_OF_ORMAZD |  | 15 | 15 | / |  |  |  |  | / |  | NONE |
| GENTLEMEN |  | -25 | 50 | / |  |  |  |  | / | ARCHER+25 GUN+25 | NONE |
| WAIDAN | 20 |  |  | / |  |  |  |  | / |  | NONE |
| MARTIAL_ARTS |  |  |  | / |  |  |  |  | / | MELEE+20 | NONE |
| PANKRATION | 5 |  |  | / |  |  |  |  | / | RECON+20 ARCHER+10 MELEE+20 GUN+10 | NONE |
| TRANSPORT1 | -20 |  |  | / |  |  |  |  | / |  | NONE |
| TRANSPORT2 | -20 |  |  | / |  |  |  |  | / |  | NONE |
| TRANSPORT3 | -20 |  |  | / |  |  |  |  | / |  | NONE |
| TORPEDOES |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+100 STEAM_SHIPS+75 DIESEL_SHIPS+75 NUCLEAR_SHIPS+50 SUBMARINE+25 | NONE |
| DRILL2 |  |  |  | / |  |  |  | 1 | / |  | NONE |
| DRILL4 |  |  |  | / |  |  |  | 2 | / | MOUNTED+10 | NONE |
| FLANKING1 |  |  |  | / |  |  | 10 |  | / |  | NONE |
| FLANKING2 |  |  |  | / |  |  | 15 |  | / |  | NONE |
| FLANKING3 |  |  |  | / |  |  | 15 |  | / |  | NONE |
| COMBAT1 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| ANTITANK_DEFENSE1 |  |  |  | / |  |  |  |  | / | WHEELED+10 TRACKED+10 DREADNOUGHT+10 | NONE |
| ANTITANK_DEFENSE2 |  |  |  | / |  |  |  |  | / | WHEELED+15 TRACKED+15 DREADNOUGHT+15 | ANTITANK_DEFENSE1 |
| ANTITANK_DEFENSE3 |  |  |  | / |  |  |  |  | / | WHEELED+20 TRACKED+20 DREADNOUGHT+20 | NONE |
| COVER |  |  |  | / |  |  |  |  | / | ARCHER+20 | NONE |
| COVER2 |  |  |  | / |  |  |  |  | / | ARCHER+25 | NONE |
| COVER3 |  |  |  | / |  |  |  |  | / | ARCHER+30 | NONE |
| SHOCK |  |  |  | / |  |  |  |  | / | MELEE+20 | NONE |
| SHOCK2 |  |  |  | / |  |  |  |  | / | MELEE+25 | NONE |
| SHOCK3 |  |  |  | / |  |  |  |  | / | MELEE+30 | NONE |
| PINCH |  |  |  | / |  |  |  |  | / | GUN+20 | NONE |
| PINCH2 |  |  |  | / |  |  |  |  | / | GUN+25 | NONE |
| PINCH3 |  |  |  | / |  |  |  |  | / | GUN+30 | NONE |
| COMBAT2 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| CHEMICAL1 |  |  |  | / | 10 |  |  |  | / | ANIMAL+20 MELEE+20 MOUNTED+20 ARCHER+20 GUN+20 CLONES+20 WHEELED+20 RECON+20 | NONE |
| CHEMICAL2 |  |  |  | / | 10 |  |  |  | / | ANIMAL+25 MELEE+25 MOUNTED+25 ARCHER+25 GUN+25 CLONES+25 WHEELED+25 RECON+25 | NONE |
| CHEMICAL3 |  |  |  | / | 10 |  |  |  | / | ANIMAL+30 MELEE+30 MOUNTED+30 ARCHER+30 GUN+30 CLONES+30 WHEELED+30 RECON+30 | NONE |
| FIELD1 |  |  |  | /-15 |  |  |  |  | / |  | NONE |
| FIELD2 |  |  |  | -15/ |  |  |  |  | / |  | NONE |
| FIELD3 |  |  |  | -20/-20 |  |  |  |  | / |  | NONE |
| COMBAT3 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| COMBAT4 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| COMBAT5 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| ANTIBIOLOGICAL | -15 |  |  | / |  |  |  |  | / | BIOLOGICAL+75 WHEELED+35 TRACKED+20 | COMBAT2 |
| SONAR |  |  |  | / |  |  |  |  | / | SUBMARINE+20 | NONE |
| VETERAN | 10 |  |  | / |  |  |  |  | / |  | NONE |
| LOW_ALTITUDE | -15 |  |  | / |  |  |  |  | / | ARCHER+50 MELEE+50 MOUNTED+25 GUN+25 SIEGE+25 | NONE |
| AIR_REFUEL | -15 |  |  | / |  |  |  |  | / |  | NONE |
| ACE | 10 |  |  | / |  |  |  |  | / |  | NONE |
| TOPGUN | 10 |  |  | / |  |  |  |  | / |  | NONE |
| FORMATION |  |  |  | / |  |  |  |  | / | MOUNTED+20 | NONE |
| FORMATION2 |  |  |  | / |  |  |  |  | / | MOUNTED+25 | NONE |
| FORMATION3 |  |  |  | / |  |  |  |  | / | MOUNTED+30 | NONE |
| CHARGE |  |  |  | / |  |  |  |  | / | SIEGE+20 | NONE |
| CHARGE2 |  |  |  | / |  |  |  |  | / | SIEGE+25 | NONE |
| CHARGE3 |  |  |  | / |  |  |  |  | / | SIEGE+30 | NONE |
| AMBUSH |  |  |  | / |  |  |  |  | / | TRACKED+20 WHEELED+20 | NONE |
| AMBUSH2 |  |  |  | / |  |  |  |  | / | TRACKED+25 WHEELED+25 | NONE |
| AMBUSH3 |  |  |  | / |  |  |  |  | / | TRACKED+30 WHEELED+30 | NONE |
| AMPHIBIOUS | 10 |  |  | / |  |  |  |  | / |  | NONE |
| MEDIC1 |  |  |  | / |  |  |  |  | 10/5 |  | NONE |
| MEDIC2 |  |  |  | / |  |  |  |  | 10/5 |  | NONE |
| MEDIC3 |  |  |  | / |  |  |  |  | 15/15 |  | NONE |
| GUERILLA1 |  |  |  | /20 |  |  |  |  | / |  | NONE |
| GUERILLA2 |  |  |  | /30 |  |  |  |  | / |  | NONE |
| GUERILLA3 |  |  |  | 25/ |  |  |  |  | / |  | NONE |
| WOODSMAN1 |  |  |  | / |  |  |  |  | / | ANIMAL+10 | NONE |
| WOODSMAN2 |  |  |  | / |  |  |  |  | / | ANIMAL+15 | NONE |
| WOODSMAN3 |  |  |  | / |  |  |  | 2 | 15/ | ANIMAL+20 | NONE |
| CITY_RAIDER1 |  | 15 |  | / |  |  |  |  | / |  | NONE |
| CITY_RAIDER2 |  | 15 |  | / |  |  |  |  | / |  | NONE |
| CITY_RAIDER3 |  | 20 |  | / |  |  |  |  | / | GUN+10 | NONE |
| CITY_RAIDER4 |  | 25 |  | / |  |  |  |  | / |  | NONE |
| CITY_GARRISON1 |  |  | 20 | / |  |  |  |  | / |  | NONE |
| CITY_GARRISON2 |  |  | 25 | / |  |  |  |  | / |  | NONE |
| CITY_GARRISON3 |  |  | 30 | / |  |  |  |  | / | MELEE+10 | NONE |
| URBAN_TACTICS1 |  | 20 | 10 | / |  |  |  |  | / | GUN+10 CLONES+10 WHEELED+10 TRACKED+10 | COMBAT1 |
| URBAN_TACTICS2 |  | 25 | 15 | / |  |  |  |  | / | SIEGE+15 HELICOPTER+15 | NONE |
| URBAN_TACTICS3 |  | 30 | 20 | / |  |  |  |  | / | HITECH+20 ROBOT+20 DREADNOUGHT+20 ASSAULT_MECH+20 | NONE |
| BARRAGE1 |  |  |  | / | 15 |  |  |  | / |  | NONE |
| NAPALM_BOMBS | -10 |  |  | / | 20 |  |  |  | / | ARCHER+200 MELEE+200 MOUNTED+100 GUN+50 SIEGE+50 WHEELED+35 TRACKED+20 | NONE |
| BARRAGE2 |  |  |  | / | 20 |  |  |  | / | MELEE+10 | NONE |
| BARRAGE3 |  |  |  | / | 25 |  |  |  | / | GUN+10 | NONE |
| ACCURACY |  |  |  | / |  | 8 |  |  | / |  | NONE |
| PRECISION_BOMBING |  |  |  | / | 10 | 10 |  |  | / | ARCHER+100 MELEE+100 MOUNTED+75 GUN+25 SIEGE+50 WHEELED+25 TRACKED+50 | NONE |
| ACCURACY2 |  |  |  | / |  | 16 |  |  | / |  | NONE |
| ACCURACY3 |  |  |  | / |  | 24 |  |  | / |  | NONE |
| PATROL3 |  |  | 15 | / |  |  |  |  | / |  | NONE |
| MANUEVERING1 |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+15 | NONE |
| MANUEVERING2 |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+15 | NONE |
| MANUEVERING3 |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+20 | NONE |
| BOMBARDING1 |  |  |  | / |  | 3 |  |  | / |  | NONE |
| BOMBARDING2 |  |  |  | / |  | 5 |  |  | / |  | NONE |
| BOMBARDING3 |  |  |  | / |  | 8 |  |  | / |  | NONE |
| FIREARMS1 |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+10 | NONE |
| FIREARMS2 |  |  |  | / |  |  |  |  | / | WOODEN_SHIPS+10 | NONE |
| FIREARMS3 |  |  |  | / |  |  |  | 1 | / | WOODEN_SHIPS+20 | NONE |
| AIR_DEFENSE1 |  |  |  | / |  |  |  |  | / | HELICOPTER+10 | NONE |
| AIR_DEFENSE2 |  |  |  | / |  |  |  |  | / | HELICOPTER+15 | NONE |
| AIR_DEFENSE3 |  |  |  | / |  |  |  |  | / | HELICOPTER+20 | NONE |
| COMBAT6 | 25 |  |  | / |  |  |  |  | / |  | NONE |
| FANATIC | 20 | 10 |  | / |  |  |  |  | / |  | NONE |
| KAMIKAZE |  | 10 |  | 20/ |  |  |  |  | / |  | NONE |
| ESCAPE1 |  |  |  | / |  |  | 40 |  | / |  | NONE |
| ESCAPE2 |  |  |  | / |  |  | 40 |  | / |  | SECURITY2 |
| COMBAT_AI1 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| COMBAT_AI2 | 12 |  |  | / |  |  |  |  | / |  | NONE |
| COMBAT_AI3 | 14 |  |  | / |  |  |  |  | / |  | NONE |
| COMBAT_AI4 | 16 |  |  | / |  |  |  |  | / |  | NONE |
| REINFORCED_STRUCTURE |  | 15 | 15 | / |  |  |  |  | / |  | NONE |
| AUTOMATIC_REPAIRS3 |  | 30 |  | / |  |  |  |  | 10/ |  | NONE |
| WEAPON_UPGRADE1 |  | 20 |  | / |  |  |  |  | / |  | NONE |
| WEAPON_UPGRADE2 |  | 25 |  | / |  |  |  |  | / |  | NONE |
| WEAPON_UPGRADE3 |  | 30 |  | / |  |  |  |  | / |  | NONE |
| FUSION_POWER_SOURCE |  |  |  | / |  |  |  |  | / | ROBOT+15 ASSAULT_MECH+15 | NONE |
| POWER_SOURCE_UPGRADE1 |  |  |  | / |  |  |  |  | / | ROBOT+10 ASSAULT_MECH+10 | NONE |
| POWER_SOURCE_UPGRADE2 |  |  |  | / |  |  |  |  | / | ROBOT+15 ASSAULT_MECH+15 | NONE |
| POWER_SOURCE_UPGRADE3 |  |  |  | / |  |  |  |  | / | ROBOT+20 ASSAULT_MECH+20 | NONE |
| SENSORS | 10 |  |  | / |  |  |  |  | / |  | NONE |
| SENSORS2 | 10 |  |  | / |  |  |  | 1 | / |  | SENSORS |
| SENSORS3 | 10 |  |  | / |  |  | 10 |  | / |  | SENSORS2 |
| LAND_WARRIOR1 |  |  |  | / |  |  |  | 1 | / |  | NONE |
| LAND_WARRIOR3 |  |  |  | / |  |  |  | 1 | / |  | NONE |
| STEALTH1 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| STEALTH2 | 10 |  |  | / |  |  |  |  | / |  | NONE |
| STEALTH3 | 15 |  |  | / |  |  |  | 1 | / |  | NONE |
| SUPER_CAVITATION |  |  |  | / |  |  |  | 1 | / |  | NONE |
| ELECTROMAGNETIC_ARMOR1 |  |  |  | / |  |  |  |  | / | MISSILE+10 | NONE |
| ELECTROMAGNETIC_ARMOR2 |  |  |  | / |  |  |  |  | / | MISSILE+15 | NONE |
| ELECTROMAGNETIC_ARMOR3 |  |  |  | / |  |  |  |  | / | MISSILE+20 | NONE |
| SHIELDING1 |  |  |  | / |  |  |  |  | / | MISSILE+10 | NONE |
| SHIELDING2 |  |  |  | / |  |  |  |  | / | MISSILE+15 | POWER_SOURCE_UPGRADE1 |
| SHIELDING3 |  |  |  | / |  |  |  |  | / | MISSILE+20 | POWER_SOURCE_UPGRADE2 |
| DEFENSIVE_PROTOCOLS1 |  |  |  | / |  |  | 15 |  | / |  | NONE |
| DEFENSIVE_PROTOCOLS2 |  |  |  | / |  |  | 20 |  | / |  | NONE |
| DEFENSIVE_PROTOCOLS3 |  |  |  | / |  |  | 25 |  | / |  | NONE |
| JUMP_SETS | 10 |  |  | / |  |  |  |  | / |  | NONE |
| ARMOR_UPGRADE1 |  |  | 20 | / |  |  |  |  | / |  | NONE |
| ARMOR_UPGRADE2 |  |  | 25 | / |  |  |  |  | / |  | NONE |
| ARMOR_UPGRADE3 |  |  | 30 | / |  |  |  |  | / |  | NONE |
| FUZZY_LOGIC |  |  |  | / |  |  |  | 1 | / |  | NONE |
| QUANTUM_ALGORITHMS |  |  |  | / |  |  |  | 2 | / |  | FUZZY_LOGIC |
| GLOBAL_AWERENESS |  |  |  | / |  |  |  | 3 | / | HELICOPTER+10 HITECH+10 DREADNOUGHT+10 | QUANTUM_ALGORITHMS |
| HEAT_SEEKING |  |  |  | / |  |  |  |  | / | HELICOPTER+15 TRACKED+15 WHEELED+15 ASSAULT_MECH+15 ROBOT+15 SIEGE+15 | NONE |
| LASER_GUIDANCE |  | 15 |  | / |  |  |  |  | / |  | NONE |
| GPS |  |  |  | / |  | 5 |  |  | / |  | NONE |
| SMALL_DIAMETER_BOMB | 50 |  |  | / |  | -10 |  |  | / |  | NONE |
| OFFENSIVE_PROTOCOLS1 |  |  |  | / |  |  |  |  | / | GUN+20 CLONES+20 SIEGE+20 HITECH+20 | NONE |
| OFFENSIVE_PROTOCOLS2 |  |  |  | / |  |  |  |  | / | GUN+20 CLONES+20 SIEGE+20 HITECH+20 | NONE |
| OFFENSIVE_PROTOCOLS3 |  |  |  | / |  |  |  |  | / | GUN+20 CLONES+20 SIEGE+20 HITECH+20 | NONE |
| TERRAIN_ANALYSIS1 |  |  |  | 15/ |  |  |  |  | / |  | NONE |
| TERRAIN_ANALYSIS2 |  |  |  | 20/ |  |  |  |  | / |  | NONE |
| TERRAIN_ANALYSIS3 |  |  |  | 30/ |  |  |  |  | / |  | NONE |
| OPERATION_GENERAL_CONQUEROR |  |  |  | / |  |  |  |  | /2 |  | NONE |
| OPERATION_GENERAL_LOGISTICIAN |  |  |  | / |  |  |  |  | 5/5 |  | NONE |
| OPERATION_GENERAL_COLONIZER |  |  |  | / |  |  |  |  | 3/3 |  | NONE |

## Buildings with defence

| Building | iDefense | iBombardDefense | iAllCityDefense | Other |
|---|---|---|---|---|
| GUILDHALL_33 | 20 | 20 |  | needs NONE |
| MONTFORT | 50 | 25 |  | needs CHIVALRY |
| KRAK_DES_CHEVALIERS | 75 | 25 |  | needs CHIVALRY |
| WALLS | 30 | 20 |  | needs MASONRY |
| CELTIC_DUN | 30 | 20 |  | needs MASONRY |
| HIGH_WALLS | 50 | 40 |  | needs SIEGE_WARFARE |
| CASTLE | 50 | 20 |  | needs ENGINEERING |
| SPANISH_CITADEL | 50 | 20 |  | needs ENGINEERING |
| BARBWIRE_FENCE | 50 |  |  | needs FASCISM |
| ANTI_MISSILE_BATTERIES | 25 | 25 |  | needs MILITARY_ROBOTS |
| NANITE_POPULATION | 25 |  |  | needs NANOBOTICS |
| SECURITY_CENTER | 20 | 20 |  | needs QUANTUM_COMPUTING |
| JEWISH_MASADA | 50 |  |  | needs MONOTHEISM |
| CHICHEN_ITZA |  |  | 25 | needs BLOOD_CULT |
| ADVANCED_SHIELDING | 30 | 30 |  | needs ADVANCED_SHIELDING |
| ALHAMBRA |  |  | 30 | needs DIVINE_RIGHT |
| EDINBURGH_CASTLE | 100 |  |  | needs ENGINEERING |
| COURIER_SYSTEM |  |  | 10 | needs WRITING |
| NANITE_DEFUSER |  |  | 50 | needs SMART_DUST |
| CELTIC_TEMPLE | 10 |  |  | needs  |
| NORDIC_TEMPLE | 10 |  |  | needs  |
| PHOEN_TEMPLE | 10 |  |  | needs  |
| MARS_TEMPLE | 10 |  |  | needs ROMAN |
| SHINTO_TEMPLE | 10 |  |  | needs  |
| ROMAN_DEPOT | 10 |  |  | needs CITY_PLANNING |
| SUMER_TEMPLE | 10 |  |  | needs  |
| TOWN_ESSENTIALS | 10 |  |  | needs MASONRY |
| CITY_ESSENTIALS | 20 |  |  | needs CITY_PLANNING |
| METROPOLITAN_ESSENTIALS | 30 |  |  | needs SANITATION |
