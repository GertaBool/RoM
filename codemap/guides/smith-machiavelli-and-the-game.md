# Smith, Machiavelli and the game

How the economy, diplomacy and war that Rise of Mankind implements compare with what Adam Smith, Niccolò Machiavelli,
Sun Tzu, Carl von Clausewitz and Thucydides wrote. Each section first describes the game, then gives the author's
claims, then the comparison. Interpretations are marked as such and kept apart from facts.

## Sources

**Texts.** Project Gutenberg, through its mirror `gutenberg.pglaf.org` (the main site was down for maintenance). Each
file is complete, ending with Gutenberg's end marker.

| text | Gutenberg | words |
|---|---|---|
| Smith, *An Inquiry into the Nature and Causes of the Wealth of Nations* (1776) | 3300 | 381,032 |
| Machiavelli, *The Prince* (Marriott translation) | 1232 | 49,958 |
| Machiavelli, *Discourses on the First Decade of Titus Livius* | 10827 | 140,779 |
| Sun Tzu, *The Art of War* (Giles translation) | 132 | 55,049 |
| Clausewitz, *On War* (Graham translation) | 1946 | 296,848 |
| Thucydides, *History of the Peloponnesian War* (Crawley translation) | 7142 | 204,671 |

**How *Wealth of Nations* was read.** The whole file was indexed: all five books and every chapter, part and article,
with their sizes.
- Read line by line in full, because each maps onto a system of the game: I.1, I.2 and I.3 (division of labour,
  exchange, extent of the market); III.1 (natural progress of opulence); V.1 part I (expense of defence).
- Every other passage quoted here was located in the full text and read in its context. These are I.5, IV.2, IV.3
  part II, IV.6, IV.7, IV.9 and V.3.
- The rest of the book was not read line by line. No claim below rests on it.

**The game.** GitLab `Graphics-Paging-Fix-Test` at `cdda5b6`, the commit the code map was built from. Code is cited
as file:function. XML values are the records the game loads, read when this was written. Defines come from the last
file that sets them (`CvXMLLoadUtilitySet.cpp:SetGlobalDefines` reads the files in order, and `SetValue`
overwrites).

## 1. Smith: exchange and the extent of the market

**The game.** Trade routes carry exchange between cities. A route's profit is computed in
`CvCity::getBaseTradeProfit` and `totalTradeModifier`.
- **Base:** the lesser of the partner city's population × `THEIR_POPULATION_TRADE_PERCENT` (50) and the distance ×
  the map size's `iTradeProfitPercent`, then × `TRADE_PROFIT_PERCENT` (20%), with a floor.
- **Raised by:**
  - the city's own population: (population − 10) × 5%;
  - connection to the capital: +25%;
  - overseas, meaning another landmass: `OVERSEAS_TRADE_MODIFIER` +50%;
  - foreign routes: `FOREIGN_TRADE_MODIFIER` +100%, granted in proportion to turns of peace up to
    `FOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS` (50), and nothing while at war (`getPeaceTradeModifier`).
- **Yield:** a route pays its profit as commerce (`CIV4YieldInfos.xml`: `YIELD_COMMERCE iTradeModifier` 100). Food
  or production come only from civics with a `TradeYieldModifiers` entry, below.

**Smith.**
- I.2: exchange arises from self-interest, "not from the benevolence of the butcher, the brewer, or the baker".
- I.3: "the extent of this division must always be limited by … the extent of the market". Water carriage opens the
  market, so industry begins "upon the sea-coast, and along the banks of navigable rivers".
- III.1: between town and country "the gains of both are mutual and reciprocal".

**Comparison.**
- *Agrees:* a route is worth more when the partner is larger, the partner's population standing for "the extent of
  the market". Overseas routes are favoured.
- *Differs:* distance *raises* a route's value, up to the population cap. To Smith, distance is a cost of carriage
  that shrinks trade.
- *Agrees, and goes further:* foreign trade grows with time at peace and stops in war. That makes commerce "a bond
  of union and friendship" (IV.3 part II) as a mechanism, not as a hope.

## 2. Smith: the AI as a trader

**The game.**
- **Acceptance** (`CvPlayerAI::AI_considerOffer`): the AI accepts an offer when what it receives is worth at least
  what it gives. When an existing deal is re-examined, it needs 110%.
- **The mod's valuation** (`AI_DIPLOMACY_FLAGS` = 15, `BBAI_AI_Variables_GlobalDefines.xml`):
  - switch 1: a tech's value is its remaining research at the receiver's own rate;
  - switch 2: a resource's value is its effect in the valuer's own cities;
  - switch 4: offers ask for what is worth most to the AI and give what is worth least to it, and **no tech is sold
    to a team ranked above it**.
- **Attitude** (`AI_getAttitudeVal`): a term penalises commerce with the AI's rivals (`AI_getRivalTradeAttitude`).
  The AI also remarks on it when greeting (`AI_getGreeting`: `AI_DIPLOCOMMENT_WORST_ENEMY_TRADING`).

**Smith.**
- IV.2: the merchant, intending only his own gain, is "led by an invisible hand to promote an end which was no part
  of his intention".
- IV.3 part II: "The wealth of neighbouring nations, however, though dangerous in war and politics, is certainly
  advantageous in trade … As a rich man is likely to be a better customer to the industrious people in his
  neighbourhood, than a poor, so is likewise a rich nation."
- He condemns the maxims by which "nations have been taught that their interest consisted in beggaring all their
  neighbours".

**Comparison.**
- *Agrees:* valuing each side of a deal by its effect on the party receiving it (switches 1 and 2) is Smith's
  exchange: a trade happens when both sides gain by their own measure.
- *Differs:* refusing to sell techs to a higher-ranked team, and resenting partners who trade with one's rivals, is
  the "mercantile jealousy" Smith attacks. *Interpretation:* Smith's own text gives the game a reason for it: wealth
  is "dangerous in war and politics". In a game whose victory conditions are relative, the AI follows the political
  half of his sentence and drops the commercial half.

## 3. Smith: protection, colonies and the economic civics

**The game.** These are XML records from `CIV4CivicInfos.xml`. Yield arrays are food, production, commerce;
commerce arrays are gold, research, culture, espionage.

| civic | effects (fields of the record) |
|---|---|
| `CIVIC_PROTECTIONISM` (Mercantilism) | `iTradeRoutes` +1; `TradeYieldModifiers` food +40%, commerce +10%; `CommerceModifiers` gold +25%; Merchant specialists valid; `iImprovementUpgradeRateModifier` +20; Upkeep medium |
| `CIVIC_COLONIAL` (Navigation) | `iTradeRoutes` +1; `TradeYieldModifiers` food +40%; `iDistanceMaintenanceModifier` −25; `iNumCitiesMaintenanceModifier` −25; `iGreatGeneralRateModifier` +30 |
| `CIVIC_CORPORATE` (Corporation) | `iTradeRoutes` +2; `TradeYieldModifiers` food +30%, commerce +25%; `YieldModifiers` production +25%; `CommerceModifiers` gold +25%; `iExtraHealth` −6; `iLargestCityHappiness` −6 |
| `CIVIC_BARTER` (Trade) | `TradeYieldModifiers` food +20%, commerce −25%; `bNoCorporations` |

**Smith.**
- IV.2: a restraint on imports may raise one domestic manufacture, but it turns "towards a particular employment a
  greater share of the stock and labour of the country" than would go there freely. His exceptions are defence
  ("As defence, however, is of much more importance than opulence, the act of navigation is, perhaps, the wisest of
  all the commercial regulations of England") and matching a domestic tax.
- IV.7 part III: the monopoly of the colony trade "necessarily reduced the whole quantity of capital employed in that
  trade below what it naturally would have been in the case of a free trade".

**Comparison.**
- *Differs:* the game rewards Protectionism with more trade (an extra route, +40% trade food, +10% trade commerce)
  and more gold. Smith's argument is that protection lowers a nation's total trade and income. Colonial likewise
  pays out where Smith counts the colonial monopoly as a loss to the mother country.
- *Agrees:* Corporate, the free-enterprise civic, gives the most trade routes (+2), which fits Smith. Its health and
  happiness penalties have no counterpart in him.

## 4. Smith: defence

**The game.**
- **Upkeep** (`CvPlayer::calculateUnitCost`): some units are free, from the difficulty, base values and a share of
  total population (`iFreeUnitsPopulationPercent`, `iFreeMilitaryUnitsPopulationPercent`). Every further unit costs
  gold (`getGoldPerUnit`, `getGoldPerMilitaryUnit`).
- **Military civics** (`CIV4CivicInfos.xml`):

| civic | effects |
|---|---|
| `CIVIC_STANDING_ARMY` (Military Training) | `iFreeExperience` 5; `iGoldPerMilitaryUnit` 1; `iHappyPerMilitaryUnit` 1; revolt index local −3, national −1 |
| `CIVIC_MILITIA` (Democracy) | `iFreeUnitsPopulationPercent` 30; `bMilitaryFoodProduction`; `iHappyPerMilitaryUnit` 1 |
| `CIVIC_PROFESSIONAL_ARMY` (Athletics) | `iFreeExperience` 10; `iGreatGeneralRateModifier` 50; `iHappyPerMilitaryUnit` 3; `iGoldPerMilitaryUnit` 1; Upkeep high |
| `CIVIC_CONSCRIPTION` (Vassalage) | `iMaxConscript` 6; `iWarWearinessModifier` +50; barracks −3 happiness |

**Smith, V.1 part I (read in full).**
- **Defence costs grow with civilization.** Hunters and shepherds go to war at no cost to the sovereign. Once there
  are manufactures, and war is fought through long campaigns, "the public should maintain those who serve the public
  in war".
- **A ceiling on soldiers:** "not more than the one hundredth part of the inhabitants of any country can be employed
  as soldiers, without ruin to the country which pays the expense of their service".
- **Wealth attracts attack:** "An industrious, and, upon that account, a wealthy nation, is of all nations the most
  likely to be attacked".
- **Discipline beats skill:** "A militia … must always be much inferior to a well disciplined and well exercised
  standing army", which he shows through Macedon, Carthage and Rome. A militia that serves several campaigns
  "becomes in every respect a standing army".
- **Firearms favour wealth:** "In modern war, the great expense of firearms gives an evident advantage to the nation
  which can best afford that expense".

**Comparison.**
- *Agrees:*
  - Upkeep paid by the non-soldiers, with free units in proportion to population, is Smith's ceiling in mechanical
    form.
  - Militia as a cheap, population-scaled force against professional armies that cost gold and gain experience
    (+5, +10) matches his militia and standing army.
  - Units gain experience in combat, so veterans improve, as his campaigning militia does.
- *Differs:* the game's Militia arrives with Democracy, late in the tree. Smith's militia is the early,
  pre-professional form of every society.
- *Open:* whether the AI attacks wealthy neighbours by preference, as Smith predicts of human rulers. It needs the
  target choice in `CvTeamAI::AI_doWar` read against his claim.

## 5. Smith: paying for war

**The game.**
- **No borrowing.** There is no loan, bond or debt anywhere in the DLL: no such symbol in its sources, and
  `codemap/guides/loans-and-bonds.md` says "Nothing like debt exists in the mod today".
- **"National Debt" is only a name.** `CIVIC_NATIONAL_DEBT` (Mercantilism) is a set of modifiers:
  - `YieldModifiers` production +25%, commerce +10%;
  - `CommerceModifiers` gold −10%, espionage +25%;
  - in the capital, commerce +25% and gold −25%;
  - `iNumCitiesMaintenanceModifier` +30;
  - buying production with gold enabled (`HURRY_GOLD`);
  - `iWarWearinessModifier` +50.
- **War weariness:** anger from war grows with each team's war weariness against the player
  (`CvPlayer::updateWarWearinessPercentAnger`), scaled by civics, buildings and map size.

**Smith, V.3.** Paying for war by borrowing ("funding") makes it painless now. "Were the expense of war to be defrayed
always by a revenue raised within the year … Wars would, in general, be more speedily concluded, and less wantonly
undertaken. The people feeling, during continuance of war, the complete burden of it, would soon grow weary of it."
And: "The practice of funding has gradually enfeebled every state which has adopted it."

**Comparison.**
- *Agrees:* the game is Smith's pay-as-you-go state. Every war is paid from the current turn's gold and production.
  War weariness is "the people feeling … the complete burden of it" as unhappiness.
- *Differs:* weariness grows with fighting, from losses and captured cities, not with the cost. A war of heavy
  spending and little fighting weighs little on the people.
- *Interpretation:* debt, which Smith thought ruins states, has no place in the game. The civic named after it
  raises production and makes war more wearying (+50%), which is closer to Smith's point than its name suggests.

## 6. Smith: money and prices

**The game.**
- **Inflation:** costs inflate with the turn count, not with money (`CvPlayer::calculateInflationRate`). Inflation
  starts after a game-speed offset and rises by a set percentage per turn, scaled by difficulty and the AI's
  handicap.
- **No markets:** goods have no prices. Resources are worth what they do in one's own cities (switch 2).

**Smith, I.5.** "The real price of every thing, what every thing really costs to the man who wants to acquire it, is
the toil and trouble of acquiring it". Money prices move with the supply of the metals.

**Comparison.**
- *Agrees, in part:* production as the cost of everything (hammers for units and buildings) is Smith's labour
  measure of real price.
- *Differs:* the game's inflation is a clock with no relation to money, metals or supply.

## 7. Machiavelli

**The game.**
- **Fear in decisions:**
  - Gifts: the AI refuses to give anything when its attitude is below Pleased and its power exceeds 4/3 of the
    asker's (`AI_considerOffer`).
  - Tribute: it demands tribute from weaker players (`CONTACT_DEMAND_TRIBUTE` in `AI_doDiplo`).
  - Talks during war: it refuses to talk while losing, for a refusal time scaled by the two sides' war success
    (`AI_isWillingToTalk`).
- **Keeping faith:** after 2 × `PEACE_TREATY_LENGTH` (10) turns the AI re-examines every deal (`AI_doDiplo`). With a
  human it cancels if the deal no longer clears `AI_considerOffer`'s 110% for an existing deal. With an AI it cancels
  if anything it gives has become refused.
- **Memory:** the AI remembers declarations of war, refused help, refused joint wars, stopped trading, cancelled open
  borders and more (`MemoryTypes`, `CvEnums.h`). Each memory moves its attitude.
- **Mercenaries:** `CIVIC_MERCENARIES` (Trade): `iFreeExperience` 5, `iGoldPerUnit` 1, `iGoldPerMilitaryUnit` 1,
  `iHappyPerMilitaryUnit` 1, revolt index local +1, `fRevViolentMod` 0.3. Units under it behave exactly as under any
  other civic.
- **Revolt and garrisons:** the Revolution mod computes a city's revolt index in Python
  (`Revolution.py:updateLocalRevIndices`). Garrison units lower it with diminishing returns (∝ defenders^0.6), more
  behind strong walls (building defence above 75) and less under Liberalism. The lowering is capped at −8, or −5
  where a foreign nationality is unhappy. Happiness, nationality, religion, distance, health and disorder are
  separate terms.

**Machiavelli.**
- *Prince* XVII: "it is much safer to be feared than loved, when, of the two, either must be dispensed with".
- *Prince* XVIII: "a wise lord cannot, nor ought he to, keep faith when such observance may be turned against him,
  and when the reasons that caused him to pledge it exist no longer".
- *Prince* XII: "Mercenaries and auxiliaries are useless and dangerous … in peace one is robbed by them, and in war by
  the enemy."
- *Prince* XX: "the best possible fortress is—not to be hated by the people, because, although you may hold the
  fortresses, yet they will not save you if the people hate you".
- *Prince* XXI: declaring oneself "will always be more advantageous than standing neutral".
- *Prince* III: send colonies to a conquered land rather than garrisons, "for with little or no expense he can send
  them out"; the garrison "consume[s] … all the income from the state".
- *Discourses* II.10: "nothing can be falser than the vulgar opinion which affirms [money] to be the sinews of war".

**Comparison.**
- *Agrees:*
  - Dropping a deal once "the reasons that caused him to pledge it exist no longer" is exactly the AI's
    re-examination after 20 turns.
  - Revolt that garrisons and walls only slow, with happiness as its own term, is the "best fortress".
  - Memories of refused joint wars punish neutrality, which fits XXI.
  - Colonial lowering distance and city-count maintenance by 25% points the same way as III.
- *Differs:*
  - Machiavelli's mercenaries are disloyal. The game's are as loyal as any other unit and cost a little gold, so XII
    has no counterpart.
  - The attitude system is built from "love": base attitude, shared religion, open borders, trade. Fear enters only
    the decisions above (gifts, tribute, talks), never attitude itself. *Interpretation:* a Machiavellian AI would let
    the other side's power and proximity weigh on attitude, so that a strong neighbour is courted rather than
    resented.

## 8. Sun Tzu

**The game.**
- **Long wars:** war weariness accumulates over a war (section 5). The AI's will to end a war is computed in
  `CvTeamAI::AI_endWarVal`.
- **Spies:** espionage missions exist, and the AI remembers spies caught (`MEMORY_SPY_CAUGHT`).
- **Sieges:** siege warfare is the war AI's first decision area in this repository (`method/docs/mission.md`).

**Sun Tzu.**
- Chapter II, "Waging War": "There is no instance of a country having benefited from prolonged warfare."
- Chapter III, "Attack by Stratagem": "supreme excellence consists in breaking the enemy's resistance without fighting", and "the worst policy of
  all is to besiege walled cities".
- Chapter XIII, "The Use of Spies": what lets the general win is "foreknowledge … knowledge of the enemy's dispositions".

**Comparison.**
- *Agrees:* war weariness makes long wars cost happiness.
- *Differs:* cities are conquered only by siege, and the AI's war aims centre on cities, so the game's war is the
  one Sun Tzu ranks worst.
- *Interpretation:* "without fighting" has a counterpart in vassalage and capitulation (`TRADE_VASSAL`,
  `TRADE_SURRENDER` in `AI_considerOffer`), the game's closest thing to breaking resistance without battle.

## 9. Clausewitz

**The game.**
- **Policy in war:** the AI holds war plans per team and counts war success, which decides when it will talk
  (`AI_isWillingToTalk`).
- **Defence:** a defender gains from the city's defence (`CvCity::getDefenseModifier`, which bombardment lowers),
  from fortifying (`CvUnit::fortifyModifier`: turns fortified × `FORTIFY_MODIFIER_PER_TURN`) and from terrain.

**Clausewitz.**
- "War is only a continuation of State policy by other means".
- "the defensive form, with a negative object, is the stronger form, the attack, with the positive object, the
  weaker".
- On the culminating point: once "the culminating point of this progressive advantage has arrived … it is time for
  the defender to proceed to action".

**Comparison.**
- *Agrees:* the game's defensive advantages give the defensive form its strength.
- *Interpretation:* the culminating point, where an attack has spent its strength, has a natural place in
  `AI_endWarVal` and the war-success counters. The code map records which inputs they read, not whether they weigh
  the attacker's exhaustion. Open.

## 10. Thucydides

**The game.**
- **Attitude:** an AI's attitude toward another changes with the rank difference between them, through each
  leader's `WorseRankDifferenceAttitudeChange` and `BetterRankDifferenceAttitudeChange` (`AI_getAttitudeVal`).
- **Power and refusal:** a weaker player's requests are refused when the AI is much stronger (section 7).

**Thucydides.**
- Book I, chapter I: "The growth of the power of Athens, and the alarm which this inspired in Lacedaemon, made war inevitable."
- Book I, chapter III (the Athenian envoys at Lacedaemon): "three of the strongest motives, fear, honour, and
  interest".
- Book I, chapter III (Archidamus, at the same congress): "war is a matter not so much of arms as of money, which
  makes arms of use".
- Book V, chapter XVII (the Melian dialogue): "the strong do what they can and the weak suffer what they must".

**Comparison.**
- *Agrees:* the rank terms are Thucydides' "alarm" at a rising power, written into attitude. The 4/3 power rule for
  refusing gifts is the Melian dialogue in one line.
- *Differs:* Archidamus' money and Machiavelli's denial of it divide the authors. The game sides with Archidamus
  only as far as gold buys units and upkeep.

## Summary

| idea | author | in the game |
|---|---|---|
| exchange from self-interest, both sides gain | Smith I.2, III.1 | yes: each side valued by its own gain (switches 1, 2) |
| market size limits the division of labour | Smith I.3 | partly: partner population caps route profit |
| distance as a cost of trade | Smith I.3 | no: distance raises route profit up to the cap |
| water carriage widens the market | Smith I.3 | yes: overseas routes +50% |
| commerce binds nations; peace and trade together | Smith IV.3 | yes: foreign trade credit grows with peace, none in war |
| beggar-thy-neighbour is folly | Smith IV.3 | no: no techs sold to a higher-ranked team; trade with rivals resented |
| protection and colonial monopoly lower total trade | Smith IV.2, IV.7 | no: Protectionism and Colonial add trade routes and yields |
| soldiers paid by the rest; a ceiling on their number | Smith V.1 | yes: population-scaled free units, then gold per unit |
| standing army beats militia | Smith V.1 | yes in kind: professional armies gain experience, militia is cheap |
| borrowing makes war easy and states weak | Smith V.3 | not modelled: no debt; war paid from current income |
| people tire of a war's burden | Smith V.3 | yes, but by losses, not cost |
| keep faith only while the reasons last | Machiavelli *Prince* XVIII | yes: deals re-examined after 20 turns and dropped below 110% |
| mercenaries are dangerous | Machiavelli *Prince* XII | no: mercenary units are as loyal as any |
| the best fortress is not to be hated | Machiavelli *Prince* XX | yes: garrisons cut revolt with diminishing returns; happiness is a separate term |
| better feared than loved | Machiavelli *Prince* XVII | partly: fear in gifts, tribute and talks; attitude is all "love" |
| neutrality is a mistake | Machiavelli *Prince* XXI | partly: refusing to join wars is remembered |
| prolonged war profits no one | Sun Tzu II | yes: war weariness grows with war |
| besieging cities is the worst policy | Sun Tzu III | no: conquest is by siege only |
| a rising power provokes war | Thucydides I.1 | yes in attitude: rank-difference terms |
| the strong do what they can | Thucydides V | yes: power rules for refusing gifts and demanding tribute |

**Changes the comparison suggests.** These are interpretations, to be judged by experiment as `method/docs/framework.md`
section 7 requires.
1. Debt that buys present strength at a future cost (Smith V.3), the design in `loans-and-bonds.md`. It would give
   Smith's mechanism, "wars … less wantonly undertaken" when paid for now, a counterpart to test.
2. War weariness that grows with what a war costs, not only with losses (Smith V.3).
3. A disloyalty risk for units under the Mercenaries civic, for example desertion when unpaid (Machiavelli XII).
4. An attitude term for the other side's power and proximity, so that a strong neighbour is courted (Machiavelli
   XVII, Thucydides I.1).
5. Selling techs to a richer partner when the trade itself is worth more than the rank it costs (Smith IV.3).

Open: whether the AI prefers wealthy targets (Smith V.1); whether `AI_endWarVal` weighs the attacker's exhaustion
(Clausewitz); and *Wealth of Nations* beyond the chapters listed under Sources.
