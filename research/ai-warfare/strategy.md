# War in Rise of Mankind: the strategy the rules imply

This document rethinks how war should be fought in RoM, starting from the rules: the
XML, `GlobalDefines.xml`, `GlobalDefinesAlt.xml`, the DLL code that applies them, and RoM's
Python rules. All of them are documented in [xml-knowledge.md](xml-knowledge.md). Where a
classic principle of military science applies, it is named, but every claim rests on a
rule of this game. The last section reviews the war AI built so far against this strategy.

Research distances are the base research cost to own a tech through its cheapest
prerequisites ([xml-war-tables.md](xml-war-tables.md)).

## 1. Ground and movement favour the defender, unless the attacker is built to use roads

### The rules
- **No enemy roads by default.** A unit uses a road in enemy land only with `bEnemyRoute`,
  and a group moves at its slowest unit's pace.
- **The defender moves two to four times faster.** His road network gives 2 tiles per move
  on roads, 3 on paved roads, 4 on Roman roads, about 10 on railroads. The invader pays
  terrain cost on every enemy tile:
  - desert costs 3 moves and gives −25 % defence;
  - marsh costs 3; forest 2 at +50 %; hills +1 at +25 %;
  - a river crossing costs −25 % in attack.
- **Healing.** 5 a turn in enemy land, 10 neutral, 15 friendly, 20 in a city, with up to 30
  more from city buildings. March heals while moving.
- **IDW.** Every battle won within 2 tiles moves plot culture to the winner, and a plot that
  flips gives its roads and resources to its new owner.

### What follows
- **Interior lines are the defender's to use.** Jomini's interior lines are literal here.
  The defender can concentrate against one invading column at a time and strike it while it
  crawls.
  - A defending AI should keep a mobile reserve, preferably collateral siege and flanking
    cavalry, in central cities on the road net.
  - It should attack an invading stack on the turn it ends next to its land or city. That
    is before its bombard has done anything, and before it can fortify.
- **For the attacker, distance means enemy tiles crossed.** Every enemy tile costs a turn of
  exposure and a turn of healing at 5.
  - Targets one or two tiles inside the border cost little.
  - Targets deep behind the defender's road net are costly: each turn of approach gives the
    defender a turn of concentration.
  - The approach should run through own and neutral land as long as possible. The
    declaration should come when the army is already adjacent to the target (the
    strike-force rule).
- **Roads change sides with ground won.** Field victories in enemy land flip the plots
  around them, so a winning army gains roads and resources as it fights forward. Fighting
  where the enemy's culture is thin (border plots, fresh cities) flips plots fastest; city
  plots take ×0.2.
- **Some forces are built for depth.** A stack made only of enemy-road units moves at the
  defender's own speed:
  - Rome's Legionary, Comitatenses and Centurio, with Commando and March free from the
    classical era;
  - the knightly orders and Crusaders (Fundamentalism, research distance 9,705);
  - Commando units from Military Science (139,414);
  - robots.

  These are the only forces that can raid deep or exploit a breakthrough. Mixing a single
  catapult or settler into such a stack throws the advantage away. A homogeneous
  enemy-road stack is a separate kind of formation: a raiding or exploitation force, not a
  siege army.
- **The culminating point is set by healing.** An invader heals 5 a turn, a defender 15 to
  50. Clausewitz's culminating point of the offensive comes early unless captured cities
  become bases: a captured city heals at 20.
  - The rhythm of a campaign is: take a city, heal in it, go on.
  - An army far from any own or captured city wears down until it must retreat. That is the
    "armies walk home" pattern the earlier studies found, and here it is a rule of the
    ground, not only an AI flaw.

## 2. Cities fall to arithmetic: the siege clock

### The rules
- **Total defence** is the larger of building defence and culture defence. Building
  defences add up, under RoM's upgrade lines:
  - High Walls (+50, bombard defence 40) replace Walls (+30/20);
  - the Castle (+50/20) stands beside them;
  - Essentials add +10 to +30;
  - temples +10, Krak des Chevaliers +75, Edinburgh Castle +100.
- **Each bombard strike** removes rate × (100 − summed bombard defence)/100 points. Units
  that ignore building defence skip the bombard defence.
- **A city heals 5** a turn, but not on a turn it was bombarded.
- **Defenders in a city** add the zeroed-or-not defence, fortification (+25), hills (+25),
  their city-defence bonus (archers +50, longbows +25), City Garrison promotions (+20 to +30)
  and first strikes.

### What follows
- **A siege is planned in strikes, not in units.** Against a city with High Walls, Castle
  and Essentials (120 % defence, 60 % bombard defence):

  | Unit | Points per strike | Strikes to zero |
  |---|---|---|
  | Trebuchet | 6 | 20 |
  | Catapult | 3 | 40 |
  | Bombard | 10 (ignores walls) | 12 |
  | Cannon | 12 | 10 |

  So the siege train must be sized to zero the defence in one to three turns of arrival.
  Five trebuchets take four turns, and every turn in place is a turn exposed to the
  defender's reserve.
  - The decision rule is: strikes available per turn × turns we can hold the tile ≥ strikes
    needed.
  - If that fails, the siege is not yet affordable. Bring more siege, or wait for gunpowder.
- **A siege must not pause.** A turn without bombardment gives back 5 points of damage,
  and a siege that pauses for two turns to heal has lost ten.
- **The assault comes the turn the walls are down,** in this order (Vauban's systematic
  siege: invest, breach, assault):
  1. ranged strikes;
  2. collateral, by effective strength (siege, then mounted units with real collateral);
  3. killers with the best odds;
  4. stop when the next attacker would be a sacrifice.

  Attacking before the walls are down is a slaughter. A fortified Longbowman fights at
  about 23 at full defence and about 14 at zero.
- **Windows of opportunity are tech events.** Each one is set by research distance:

  | Window | Research distance | What happens |
  |---|---|---|
  | Classical | 1,773 (Siege Warfare) | Catapult and High Walls arrive together. Sieges are slow: about 4 points per catapult strike against High Walls alone. |
  | Medieval | 8,887 (Engineering) | Trebuchet, Castle and Crossbowman arrive together. Sieges stay slow. |
  | **Gunpowder** | 43,080 (Gunpowder) → 83,658 (Flintlock) | Bombards ignore walls and bombard defence. Defenders are still Longbows, Crossbows, Pikemen and, with sulphur, Arquebusiers (Matchlock, 45,710). This is the classic offensive window. Denying sulphur keeps it open longer, since Musketmen and Arquebusiers need it. |
  | Late Renaissance | 68,701 (Economics); 107,865 (Rifling) | Castles and then all walls become obsolete. A city's defence is then its culture (+20 to +50) plus Essentials. |

  Tech diffusion makes known techs 30 % cheaper, so every window closes fast. A war planned
  for a window must start when the window opens. On Marathon (research 600 %, train 300 %)
  a window holds twice as many unit builds as on Normal.

## 3. The field battle: combined arms against a combined-arms enemy

### The rules
- **Collateral** strikes the stack before the battle and ignores terrain. Effective strength
  is an integer:
  - archers 0;
  - Catapult 6, Trebuchet 8, Bombard 11, Cannon 16;
  - Knight 7 at a 100 % cap, so it can kill.
- **Immunities.** Pikemen, Heavy Pikemen and the Sarissa take no collateral from mounted
  units. Siege takes none from siege.
- **Flanking strikes.** A winning mounted attacker damages the defender's siege: Horsemen at
  50, Horse Archers and Knights at 100, Cuirassiers and Cavalry against every early siege
  unit. Light and Heavy Cavalry flank archers.
- **Counters.** Spear and pike +50 % against mounted; axe and mace +50 % against melee;
  Chariot +100 % against Axemen; Crossbow +50 % against melee.
- **Forest and jungle.** Most mounted units attack at −25 % in forest and −50 % in jungle.
- **Ranged strikes** take the unit's attack but not its moves, and take archers' targets
  down to 10–25 %.

### What follows
- **The stack is a system** (combined arms, economy of force):

  | Element | Job |
  |---|---|
  | Siege | Collateral and bombard |
  | Killers | Melee or mounted, by era |
  | Escort | Anti-mounted, which is also immune to mounted collateral, so it shields the siege from cavalry |
  | Archers | Ranged strikes, for an archer-era army |
  | Medic and general | Healing, the decisive resource |

  A siege stack without anti-mounted escort loses its siege to flanking cavalry. A stack
  without collateral cannot break a defended stack.
- **Ground decides where to stand.** A stack ends its turn on forest or hills (+50 %, +25 %),
  never on open desert (−25 %). It never ends next to the enemy's collateral and flanking
  units on open ground unless the stack's own defender wins there. Fortification adds 5 % a
  turn up to 25 %, so a stack that stands still gets stronger.
- **Kill the enemy army in the open, then take the cities.** Field battles won in enemy land:
  - flip the land (IDW);
  - cost the enemy war weariness (2 per defender killed, 3 per attacker lost);
  - remove the city's future defenders.

  The expert's way: let the AI's stack come, collateral it on open ground, kill the rest.
  Each step is a rule of this game.
- **Concentration.** Collateral hits up to 6–10 units per attack, so it rewards the
  attacker against big stacks. The defender of a big stack must keep anti-siege counters
  (cavalry with flanking) and its own collateral ready. A big stack is strong only if it
  can strike the enemy's collateral first. Concentration means concentration of collateral
  and first strikes, not of headcount.

## 4. Supply and denial: the enemy's centre of gravity is often a resource

### The rules
- Horse is needed by every mounted unit.
- Iron is needed by the Swordsman, the heavy infantry, the Bombard and the Cannon, and is
  one option for most early melee.
- Copper, iron or obsidian: one of them is needed by most ancient and classical melee.
- Sulphur is needed by every gunpowder infantry unit, and is one option for Bombard, Cannon
  and Cuirassier.
- Ammo, made by a building, is needed by modern infantry and artillery. Diesel is needed by
  every vehicle.
- Pikemen and Spearmen need none.
- Resource tiles sit on improvements, several of them allowed outside borders. A pillaged or
  flipped tile denies the resource.

### What follows
- **Denial is a war aim of its own.** Taking or pillaging the enemy's only sulphur removes
  the Renaissance defensive line. Taking his only horses removes his counter to our siege
  (flanking cavalry). This is Clausewitz's centre of gravity, made concrete: a limited war
  for one tile can be worth more than a war for a city.
- **Raiding needs the right formation.** A small, fast stack of enemy-road units, mounted,
  or Commando, pillages the source and leaves. Pillaging also moves influence (IDW 2.0), and
  pillaging towns costs the enemy years of growth.
- **The defender protects his own resources first:** a fort on the resource (+50 %), a
  garrison, or a city that covers it.

## 5. Time, money and people

### The rules
- **Speed.** Marathon research 600 % against train 300 %; Epic 300 against 100.
- **Diffusion.** Known techs are 30 % cheaper.
- **The AI's discounts.** It upgrades at half cost and pays half supply. Upgrades cost 20 + 1
  gold per hammer.
- **Experience.**
  - Barracks +3, Legion Barracks +10 melee, Stable +2, Knight Stable +3, Siege Workshop +2.
  - West Point +4, Pentagon +2 globally.
  - Professional Army +10, Standing Army and Mercenaries +5.
- **Production.** Heroic Epic +100 % military; Hereditary Rule and Imperium +25 %.
- **War weariness.**
  - Losing an attacker costs 3, a city lost 6, with decay 1 a turn.
  - Map size runs from +50 % (Duel) to −85 % (Gigantic); civics from −50 % to +100 %.
  - Forced wars −50 %.

### What follows
- **Prepare before declaring:** XP buildings in the producing cities, the military civic
  (Professional Army, Hereditary Rule), the national epic. Then upgrade the whole army in
  the turns before the declaration. For the AI, upgrades are half price.
- **Failed attacks cost double:** the hammers, plus war weariness at 3 per attacker lost
  against 1 per defender killed. Odds thresholds should rise with the war-weariness cost on
  small maps and in high-weariness civics.
- **Peace has a price and a clock.** A treaty lasts 10 turns. Weariness decays at 1 a turn
  but 99 % at peace. The time to make peace is after the window closes, not while it is
  open.

## 6. Leaders: where character belongs

Each of the 82 leaders already carries a war personality in the XML:
- the odds he demands before attacking, and their random part;
- how often he plans total, limited and dogpile wars;
- the power ratios he wants for near and distant targets;
- his raze chance;
- one favoured unit role (collateral, pillage, city attack, counter, defence).

These should decide **between** sound options: which window to use, which target, raid or
siege, how much risk to take. They should not decide whether to follow the rules of
sections 1–5. Bismarck favours collateral and Boudica pillage; both should still bring
enough siege to break the walls in time.

## 7. The war AI built so far, judged against this

**Right, and more important than its measured gain:**
- **Declaring when the army stands at the target** (switch 1). With interior lines and
  enemy-road rules, a declaration before the army is in place hands the defender its
  concentration time.
- **Choosing targets by the power each side can bring to the target's land** (switch 2).
  Distance should be counted in enemy tiles to cross.
- **Bombarding with every unit that can, with a collateral unit opening the assault**
  (switches 8 and 16).
- **Ranged strikes from cities** (switch 64).
- **The three bug fixes now on main** (0019): units disbanded when enemies were near;
  collateral counted where it does no damage.

**In the right direction, still experimental:**
- City sallies against parked stacks (8192). Interior lines say the defender should do this
  far more, with a reserve and not only the garrison.
- Siege conduct with killer odds and a stop rule (16384).
- Exposure-aware approach (32768).
- Sacrifices only at real odds (65536).

**Missing, and central by the rules above:**
1. **Siege sizing by the bombard arithmetic** (section 2): strikes needed against strikes
   per turn, and no assault into standing walls.
2. **Tech windows** as a war-timing input: gunpowder against walls, obsolete walls after
   Rifling.
3. **Interior-line defence:** a central mobile reserve that strikes invaders while they
   crawl.
4. **Enemy-road formations:** homogeneous stacks for raids and exploitation (Rome, the
   orders, Commando), and never a slow unit in them.
5. **IDW as a war aim:** fight where plots flip, then use the roads gained.
6. **Campaign rhythm by healing:** take, heal in the captured city, continue. No deep
   advance without a base.
7. **Resource denial:** limited wars and raids for sulphur, iron, horse and copper, and
   forts on one's own.
8. **Preparation:** XP buildings, military civic and upgrades before the declaration.

**On method.** The expert oracle checks one-turn battle arithmetic and nothing more. The
large self-play campaigns measured an AI against itself. The way forward is the rules above,
turned into decisions in the DLL, each checked by:
- a unit test of the decision against the rule;
- a build;
- one game that must not crash or desync.

A campaign is warranted only where an effect is uncertain and large.
