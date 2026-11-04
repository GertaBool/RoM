# Cataclysms, seasons and long cycles: research for D30 (R18, M64)

Your point (M64): the mod models history as a contest between players under resource limits. It leaves out the
cataclysms, the seasons and the long cycles that shaped real populations. This file shows what the mod has
(section 1), what the historical record shows (section 2), readings (section 3), and what it means for the
population model (section 4). It extends `population_model.md`. Nothing here is decided.

## 1. What the mod has (GitLab main: XML, DLL, Python)

**How a random event fires** (`CvPlayer::doEvents`, `CvPlayer.cpp` line 21538):
- **The roll.** After turn 20 (`FIRST_EVENT_DELAY_TURNS`), each player rolls once a turn against the era's
  `iEventChancePerTurn` out of 100 (`EVENT_PROBABILITY_ROLL_SIDES`). The chance is 2 in the Ancient era, 4 in the
  Classical, 8 in the Medieval and Renaissance, 12 in the Industrial, 16 in the Modern, then 20 and 24
  (`CIV4EraInfos.xml`).
- **The pick.** If the roll succeeds, one trigger is drawn by weight from all those eligible (310 trigger records,
  most of them not disasters).
- **Two switches.** `iPercentGamesActive` decides at game start whether a trigger exists in that game at all
  (`CvGame.cpp` line 10300). The game option No Events switches everything off.
- **Repeats.** A trigger marked `bGlobal` counts as fired for every player once one player has had it. A trigger
  without `bRecurring` fires once per player.

**The disasters and shocks among them** (`CIV4EventTriggerInfos.xml`, `CIV4EventInfos.xml`,
`CvRandomEventInterface.py`):

| Trigger | When it can happen | What it does |
|---|---|---|
| Black Death | after the Classical era, before Medicine; a city of size 10 or more; recurring; 85 % of games; weight 200 | One choice: -3 citizens and -300 gold. The other: -4 citizens, and -2 citizens in each of the 2-4 nearest own cities of size 3 or more |
| Smallpox | the same conditions | One choice: -100 gold. The other: -2 citizens, and -1 in each of the 1-3 nearest own cities of size 3 or more |
| Influenza | after the Industrial era, before Medicine; size 10 or more; 45 % of games | One choice: -3 citizens and -100 gold. The other: -4 citizens, and -2 in each of several nearest own cities (Python, `applyInfluenza2`) |
| Famine | 70 % of games; recurring; weighted by city food | Choices: nothing; -50 % food in a neighbour's city (attitude +1); -100 % food there and -10 gold (attitude +3). In effect, an offer to send food to a neighbour |
| Spoiled grain | a city with a Granary; 80 % of games | -100 % of the stored food, or -20 gold |
| Pestilence (three triggers) | a pasture, plantation or farm | Effects set in Python (not read here) |
| Volcano, Earthquake | after Writing, Monotheism, Horseback Riding or Iron Working; recurring | Volcano: up to 3 improvements next to the plot hit; cottages, hamlets, villages and towns turn to city ruins (Python, `applyVolcano1`); Earthquake similar (Python, not read in full) |
| Hurricane, Monsoon, Tsunami | coastal cities; the same techs (Tsunami: Theology, Literature, Code of Laws or Machinery) | Effects set in Python (not read here); one Tsunami choice also takes -5 citizens (XML) |
| Dust Bowl | 4 plains farms; Civil Service | -40 gold; may continue (25 % to clear each time) |
| Blizzard, Sandstorm | tundra or desert plots with improvements or roads | Small gold losses |
| Overfishing | fishing boats; city size 80 or more; Calendar to Ecology | The plot loses food |
| Great Depression, Large Recession | corporations, or the Tribute civic and Corporation | Gold and inflation |
| The Huns (and Vandals, Goths, ...) | until Nationalism, Printing Press, Education, Astronomy or Matchlock; 20 % of games | A barbarian uprising (Python) |
| Baby Boom | at peace, the turn after a peace treaty | +10 food |

- **Global warming** exists (`CvGame::doGlobalWarming`, with the `GLOBAL_WARMING_*` defines). It is driven by
  unhealthiness and nuclear use and turns terrain over.
- **What the mod has no state for:** climate or weather, harvest variation from year to year, seasons, an epidemic
  that spreads, and population cycles.
- **What one plague costs in people,** on the curve of `population_model.md`. Size 10 to 7 is 630,000 to 232,000
  (-63 %). Size 12 to 8 is -68 %. Size 20 to 16 is -46 %.

## 2. The historical record (sources named; web search, 2026-11-04)

**Epidemics:**
- **The Black Death, 1347-1351,** killed a third to 60 % of Europe's population. Benedictow estimates about 60 %; the
  common figure is about half. Plague then returned about once a generation into the 1700s, in more than 100
  epidemics. In England it came back in 1361-63 (about 20 % of Londoners died) and in 1369 (10-15 %).
- **The Americas after 1492 (Koch et al. 2019):** about 56 million deaths by about 1600. That is 90 % of a
  pre-contact population of about 60.5 million (interquartile range 44.8-78.2 million). The main cause was disease,
  with violence and famine. The abandoned farmland regrew as forest and took up carbon dioxide (5 ppm).

**Famine and harvests:**
- **The Great Famine, 1315-1317 (recovery by 1322):** 10-15 % of the population died in southern England and about
  10 % in northern France. Wheat prices doubled from 1315 to mid-1316. A cattle plague killed 62 % of the cattle in
  England and Wales. It came in a run of wet, cold years from 1310 to 1330.
- **Harvest failures cluster and persist:**
  - Campbell and Ó Gráda (2011) measured English grain yields for 1268-1480 and 1750-1850. Major harvest shortfalls
    were part of most subsistence crises, and back-to-back shortfalls caused the worst famines. By about 1800,
    yields varied less and prices reacted less to harvests.
  - Bekar (2019): a failed harvest raised the chance that the next one failed by 20-30 %. Harvests were not
    independent from year to year.
- **Famine was not most crisis mortality.**
  - On Wrigley and Schofield's English data for 1541-1871, Fogel found that less than 10 % of "crisis mortality"
    years (deaths 50-100 % above normal) came from famine. Disease caused the rest.
  - High prices showed up more in fewer marriages than in more deaths.
  - All of England's severe mortality crises (30 % above trend) came before 1750.

**Climate shocks:**
- **About 2200 BC: the 4.2-kiloyear event,** a drought through the 22nd century BC. It may be linked to the end of
  Egypt's Old Kingdom and of the Akkadian Empire, but this is contested.
- **About 1200 BC:** a drought of about 300 years framed the Late Bronze Age collapse, together with famine,
  invasions and political struggles (Kaniewski et al. 2010, 2013). The authors call climate one cause among several.
- **536 to about 660 AD: the Late Antique Little Ice Age** (Büntgen et al. 2016). Eruptions in 536, 540 and 547
  started it. The authors call it the strongest Northern-Hemisphere cooling of the last 2,000 years, and warn
  against simple cause and effect.
- **The 17th-century general crisis** (Parker 2013). The Little Ice Age met wars and revolts. Contemporaries guessed
  that a third of the world's people died; Parker calls the estimates partly guesswork, with some regions losing
  half or more. Reviewers dispute how much was climate.
- **1815 Tambora and the "year without a summer" of 1816** (Post). Death rates rose in 1816-17 by about 4 % in
  France, 6 % in Prussia and more than 20 % in Switzerland and Tuscany. Grain prices doubled or more, and food riots
  followed. Post called it the last great subsistence crisis in the Western world.

**Seasons:**
- In England the months before the harvest were the lean season, and infant mortality followed the seasons.
- Across nine pre-industrial European countries, deaths rose with high grain prices, cold winters and hot summers.
- In Germany in 1650-1790, mortality rose with rye prices. Market integration made prices less volatile and lowered
  the risk of dying of hunger.
- **Open:** a monthly grain-price series that measures the peak before the harvest.

**Long cycles:**
- **Turchin and Nefedov, *Secular Cycles* (2009),** building on Goldstone's demographic-structural theory:
  - Agrarian states went through long phases of expansion, stagflation, crisis and depression. For example, the
    Tudor-Stuart cycle ran from 1485 to 1730.
  - Prices mirror population. State strength, elite numbers and instability move with these phases.
  - Their cases are England, France, Russia and Rome.
  - I did not confirm a fixed cycle length from these sources.
- **After the Black Death,** Clark finds English real wages doubled: farm wages of 1450 were not matched again until
  the First World War. Broadberry et al. and others say wages followed population less tightly than a simple
  Malthusian model predicts.

## 3. Readings (each with what would contradict it)

**S1. The mod's shocks are rare, local and unconnected.**
- One player rolls 2-16 % a turn for any event at all, then one trigger is drawn among about 300.
- A plague hits one player's city and a few neighbours, never a region across borders.
- Nothing links shocks across players, years or places (except the Dust Bowl's continuation), and nothing ties them
  to density, trade or climate.
- History shows the opposite: shocks were correlated in space (one climate, one trade network), persistent in time
  (Bekar), and tied to density and connection.
- Contradicted if: the Revolution mod's mechanics, not catalogued here, carry such links.

**S2. They hit cities, not populations.**
- A plague takes 3-4 citizens from one city, which on the curve is 46-68 % of its people. Distant cities lose
  nothing.
- The Black Death took a third to 60 % of a continent, and then returned about every generation.

**S3. Your point holds in this form.**
- Besides the players' own choices and their enemies, the only forces on population are food and health, and they
  are steady.
- No outside process makes growth and collapse alternate. Yet that alternation (Turchin and Nefedov, Parker,
  Kaniewski) and the higher wages after a collapse (Clark) are central to the real record.

**S4. Disease mattered more than famine for crisis deaths, at least in early modern England** (Fogel on Wrigley and
Schofield). A model built only on harvests would get crisis mortality wrong. Disease needs its own process:
- it spreads along trade and armies;
- it hits harder where people are dense and towns are large;
- it returns as immunity fades.

**S5. Seasons fit the turn length only late.**
- At Normal speed a turn lasts 50 years down to 1 year for the first 550 turns, then half a year and a quarter
  (`proposals.json`, game facts).
- While a turn lasts a year or more, a season shows up only as the yearly cycle of harvest, store and spoilage.
  The goods pass (GW.F5) already stores and spoils.
- Seasons as such become possible only in the half-year and quarter-year turns.

## 4. What this means for the population model (D30): building blocks, not a decision

These need a population counted in people (D30 options 3 or 4). On the current curve they can only be events of
the kind in section 1.

**A. Climate as a slow regional state.**
- A seeded series per climate zone (warm optima, cool phases, droughts) scales yields through land quality.
- Volcanic winters are world-wide shocks lasting several years.
- Earth scenarios could anchor the series to their dates through the map's BeginEconomy block (D24).

**B. Harvests that vary.**
- Each year's yield per region varies around its mean. A bad year raises the chance of the next one being bad
  (20-30 % in Bekar), and neighbouring regions move together.
- The variation shrinks with the techs that reduced it historically, and with market integration (trade routes).
- Famine is what happens when the stores run out. It raises deaths and lowers marriages and births in the
  demographic model.

**C. The yearly cycle.**
- With turns of a year or more: one harvest a year, eaten from stores through the year, with spoilage as now.
- With half-year and quarter-year turns: seasons, so the harvest falls in its season and the lean months come
  before it.

**D. Epidemics as a process.**
- A disease starts somewhere, spreads by trade routes, armies and contact, and kills by density and urban share.
- The survivors are immune for a time; recurrence comes as immunity fades.
- Techs (sanitation, quarantine, Medicine, vaccination) and buildings reduce it.
- First contact between continents can bring the American kind of collapse.
- This replaces the fixed -3 citizens of the events.

**E. The demographic-structural loop.**
- Population pressure lowers food and wages per head. That raises instability (the Revolution indices exist) and
  leads to crisis and loss.
- Afterwards labour is scarce, so output per head and wages rise, and growth resumes.
- This loop is what makes cycles appear without scripting them.

**F. As game options,** like the Revolution options (R12.5): climate, harvest variation and epidemics each switched
on or off per game.

**Open:**
- The Revolution mod's indices and what they already link.
- The Pestilence, hurricane and tsunami effects in Python (not read).
- Sourced harvest variation (the Campbell series itself).
- A seasonal price series.
- The Justinianic plague and other pre-1300 epidemics.
- Whether the AI can plan for shocks it cannot foresee.
