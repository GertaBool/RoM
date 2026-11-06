# Decisions waiting on you, with options (R28, M74)

Each section states the question, the facts it rests on, the options with what each means in play and in the code,
and a recommendation. Pick one option per question, or combine sub-options where marked. Facts and sources are in
the files named in each section. Decided so far in this round: D31, the full water model (M73), and people counted
in `__int64` inside the DLL with Python given thousands (M74).

---

## D30. How population works

**The question.** Should the game's people keep coming from the city size (`size^2.8 × 1000`), or should the city
count real people who grow and shrink with food, health and water, with the size following from them?

**Facts.**
- **The game today.** Size 7 shows 232,000 people, size 36 shows 22.8 million. A citizen eats 3 food whatever it
  stands for, and growth costs 30 + 10 × size food (`population_model.md`).
- **The harness games.** At 1300 BC the median city is size 6.8, shown as about 230,000 people. The largest real city
  of 2000 BC had 40,000-65,000; Babylon around 500 BC had 150,000-200,000.
- **History.** Population settles where food per head meets subsistence (Clark). Technology raised density, not
  income, before 1500 (Ashraf and Galor). England grew 0.4-0.5 % a year in 1086-1300 and 0.95 % in 1681-1821.
- **Sourced parameters.** `s` about 2,600 satiety units a day, `s_min` 1,500 kcal, `r` 1 % a year rising to 1.75 %
  in the transition (`open_questions.md` section 7).

**Options.**

| | Option | In play | In the code | For | Against |
|---|---|---|---|---|---|
| A | Keep the curve; workers per citizen as in D23 | as today; a citizen stands for more people the larger the city | none beyond D23 | no risk to balance or AI | early cities 4-6 times too large; food per person falls as cities grow; craftsman places cannot be counted in people |
| B | A curve fitted to real sizes, per era | sizes plausible on screen; growth unchanged | `getRealPopulation` only | one function | people still do not follow food; population jumps when the era changes |
| C | **The compact Malthusian model** (recommended) | cities grow toward what their food supports, faster when food is plenty, shrink in famine or bad health; size follows people | `m_llPeople` in CvCity; `doGrowth` replaced by the logistic year loop; `growthThreshold()` and `foodDifference()` kept as a translation layer so the AI and screens work | true to the sources; needs and craftsmen count real people; two parameters | the largest change; the AI's growth needs a 30-seed check |
| D | Food-box citizens kept, real people counted beside them | growth as today; people for display, needs and craftsmen | `m_llPeople` beside the food box | small engine change | two population numbers that can drift apart |

**Sub-choices if C:**
- **C1. What the city size is:**
  - **(i)** The inverse of today's curve, `(N/1000)^(1/2.8)`, so a city of 50,000 is size 4 and 1 million is size
    12. Recommended: the same scale players know.
  - **(ii)** Labour units: workers ÷ the people one citizen stands for in that era.
- **C2. Growth speed `r`:**
  - **(i)** 1 % a year before Medicine, 1.75 % to Sanitation, 0.5 % after (recommended, sourced).
  - **(ii)** One rate for all eras.
- **C3. Migration toward better-fed cities:** (i) on, 2 % of the gap a year (recommended); (ii) off.
- **C4. What health does:**
  - **(i)** A death term in the growth step (recommended; fits D31's water and health).
  - **(ii)** Health lowers the food per head instead.

---

## D24. What a map declares (the BeginEconomy block)

**The question.** How much economic data a map or scenario carries in its BeginEconomy block, and how map, XML and
game options layer.

**Facts.**
- **Today.** The block exists and holds the plot area (PR.F6). CvWBInterface.py reads it after the base game's
  reader, and the harness converter and WorldBuilder save carry it.
- **Map scripts** have no file, so their values come from functions such as `getPlotAreaKm2()`.
- **Your ideas (M56):** finite ore deposits, fertility ranges, starting seed stocks, trade-route settings, and economy
  screens switched like the Revolution options.

**Options.**

| | Option | What a map can say | For | Against |
|---|---|---|---|---|
| A | Plot area only (today) | the area per plot | nothing more to build | maps cannot set deposits, fertility or starting stocks |
| B | **Three layers** (recommended): XML defaults, then the map's map-wide values, then per-plot values, then the saved game state | map-wide: area, start era food per head, options; per plot (x,y): deposit (good, reserve t, grade), fertility per good; per player: starting stocks (seeds, breeding stock) | scenario authors can make an Earth map with real deposits and fields; random maps use the XML defaults | the block, its reader and the WorldBuilder writer grow; the converter must carry each key |
| C | Map-wide values only | area, food per head, options; no per-plot data | small | no finite deposits or local fertility on scenarios |

**Sub-choices if B:**
- **B1. Economy options:**
  - **(i)** A `Config/Economy.xml` with game options, as Revolution does: switch water, harvest variation, loans and
    so on per game (recommended).
  - **(ii)** Game options only.
- **B2. When to build it:** (i) with LD (land qualities and deposits) and TR.F3 (seeds), as planned (recommended);
  (ii) now, ahead of them.

---

## D21. Entertainment media (Drama, Music, Movies)

**The question.** Whether the media resources become goods with quantities, services, or stay as today until the
needs component (CN).

**Facts.** Today the media are free resources given by buildings (Broadway, Rock'n'Roll, Hollywood). A performance or
a film serves many people at little extra cost (M35: "still valuable goods, but maybe reworked").

**Options.**

| | Option | In play | For | Against |
|---|---|---|---|---|
| A | Goods made in quantities, stored and shipped | a city makes so many units of Movies, consumed as comforts | the same rules as every good | media do not run out with use, so stocks and shipping misrepresent them |
| B | **Services over the trade network** (recommended) | the building serves every city connected to it; the comfort need is met while the network holds; no stock | true to how media work; no storage or spoilage records | a new kind of supply (network coverage) |
| C | Keep today's free resource until CN, then decide | unchanged | no work now | the decision returns later |

---

## D27 (open item). How food keeps

**The question.** How preserved forms (cheese, cured meat, dried and salted fish, dried fruit) enter the economy.

**Facts.**
- Stockfish keeps several years; barrel-salted herring and salt cod keep through long voyages.
- Traditional grain storage loses about 5 % a year, and 20-40 % in poor storage (FAO).
- The 32-bit game limits how many new records can be added (M59).

**Options.**

| | Option | In play | For | Against |
|---|---|---|---|---|
| A | **A fresh and a kept part per food good**, with a yearly spoilage rate per form; Salt (and later the Cannery) moves food from fresh to kept (recommended) | grain 5 % with a granary, 25 % without; cheese, cured meat, salted fish 15 %; stockfish and dried fruit 10 %; canned 2 %; fresh food eaten within the year | no new records; preservation is a choice the city makes with Salt | two quantities per food good |
| B | Separate preserved goods (Cheese, Cured Meat, Dried Fish, Dried Fruit) | each made by recipe and traded | explicit, each with its own icon | 4-6 new records against the 32-bit limit; more recipes |
| C | One spoilage rate per good by technology (FG.F2's present wording) | spoilage falls with Pottery, Fermentation, Refrigeration | simplest | Salt and preserving have no role |

---

## D28 (open items). Flour and fine cloth

**Facts.**
- Stone mills extract about 80 %, roller mills over 90 %. A tonne of wheat makes about 1.1 t of bread.
- You decided no mills for flour (M59): the city makes goods from base goods.

**Flour**

| | Option | For | Against |
|---|---|---|---|
| A | **No Flour good**; bread from grain by the city's recipe at the extraction rate (0.8, then 0.9 after Industrialism) (recommended) | no new record; matches M59 | no flour trade |
| B | Flour as an intermediate good | flour can be traded and stored | one more record and recipe; flour spoils faster than grain |

**Fine cloth**

| | Option | For | Against |
|---|---|---|---|
| A | **A Drapers' guild luxury** (recommended) | gives the Drapers their luxury (D29) | |
| B | A general stage of cloth unlocked by tech | every city can make it | duplicates the guild role |
| C | Not a good | nothing to build | the Drapers lose their luxury |

---

## D29 (open items). The guilds

**Facts.**
- **Venice:** the glassmakers' guild forbade telling trade secrets outside Venice (about 1271); the furnaces moved to
  Murano (1291); emigrating masters faced death for a time.
- **England:** the Goldsmiths' wardens assayed and marked sterling under the 1300 statute. The Statute of Artificers
  (1563) set seven-year apprenticeships and one journeyman per three apprentices in certain trades.
- **Florence:** the 1293 Ordinances of Justice gave government to the major guilds.
- **In the engine:** a corporation can be founded once per game (`CvCity::canConstruct`).

**a. Which guilds stay once per game**

| | Option | For | Against |
|---|---|---|---|
| A | **Once per game where the luxury rests on a secret technique** (Glassblowers, Drapers); the other twelve become national (recommended) | follows the Murano evidence; most players get most guilds | two systems side by side |
| B | All 14 once per game, as now | no change | most players never have most guilds |
| C | All national | simple | no race for a technique; Master units and espionage lose their point |

**b. The luxury good of each guild** (from `open_questions.md` section 8)
- A. **Accept the table** (Glassblowers crystal glass and mirrors, Drapers fine cloth, Goldsmiths hallmarked jewellery
  and plate, Blacksmiths fine blades and locks, Carpenters fine furniture, Masons carved stone, Equestrians bred
  horses, Clerks books, Artists art, Bakers fine pastry, Butchers hams and sausages, Fishmongers delicacies,
  Grocers preserves and confectionery, Mercers trade only).
- B. Fewer luxuries: only the once-per-game guilds and Goldsmiths have one.
- C. Your own list.

**c. Quality grades**

| | Option | For | Against |
|---|---|---|---|
| A | **Three grades**: common; fine (made in a guild-hall city, × 1.5 toward needs and trade); masterwork (master-guild city or great person, × 2 toward needs, × 2.5 trade) (recommended) | simple, readable | multipliers are estimates |
| B | Two grades (common, guild) | simpler | no reward for the master guild |
| C | A continuous quality score per batch | finest model | more state per good |

**d. Political and social role**

| | Option | For | Against |
|---|---|---|---|
| A | **Guild councils** (Florence: under the Guilds civic, cities with three or more halls are governed by guilds; opposing their civics raises the Revolution index), **price control** (no price spikes in their goods, rationing instead) and **entry control** (limited craftsman places; abolition at Machine Tools frees them) (recommended) | downstream effects, no flat bonus; uses the Revolution indices that exist | three mechanisms to build |
| B | Revolution index effects only | small | price and entry roles missing |
| C | Economic role only | none to build | the political role you asked for is missing |

**e. Master craftsmen and the population**

| | Option | For | Against |
|---|---|---|---|
| A | **Workshops of 5 real people** (master, journeyman, 3 apprentices), drawn from the urban people; a guild hall opens about 4 per 100,000 people, at most 40 (recommended; needs D30 C or D) | true to the Statute of Artificers ratio; independent of city size | needs the people model |
| B | Specialist slots as today | no new state | a citizen of 600,000 cannot be a master |
| C | A share of the urban people | simple | no visible places |

---

## Summary of recommendations

| Decision | Recommendation |
|---|---|
| D30 | C with C1(i), C2(i), C3(i), C4(i) |
| D24 | B with B1(i), B2(i) |
| D21 | B |
| D27 | A |
| D28 | Flour A, fine cloth A |
| D29 | a A, b A, c A, d A, e A |
