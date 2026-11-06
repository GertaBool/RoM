# The conversation restated, topic by topic (R34, M80)

You asked (M80) to go through everything again, to see whether I remember the conversation correctly, before any
misunderstanding enters the plan or the task list.

**Sources.** Every point cites the prompt it comes from (M01-M80, saved verbatim in `plan/requests.json`) and the
design record it became (D1-D35 in `plan/design.json`).

**How to read it.** Later prompts take precedence over earlier ones. Points marked **Confirm** are where I am
unsure that I understood you, or where I settled something you have not explicitly approved. Nothing here enters
the plan until you answer.

---

## 0. The two corrections you asked for in M80

### 0a. Trade yield modifiers (checked again, in the DLL)

I had written that the settlement tiers, Market and Harbor carry only route counts and commerce modifiers. That
described the fields but missed how they act.

**How a trade route's yield is computed** (`CvCity::calculateTradeYield`, `CvCity::totalTradeModifier`):
- A route's food, production or commerce = route profit × the owner's **trade yield modifier** for that yield ÷ 100.
- The owner's trade yield modifier comes from:
  - the yield records: food 0, production 0, commerce 100, so by default routes give only commerce;
  - traits: Financial +1 commerce;
  - **civics:** Barter food +20; Metals food +20; Coinage food +25; Usury food +25; Colonial food +40; Protectionism
    food +40; Corporate food +30; Guilds food +30; Planned food +50 and production +50; National Socialism food +50
    and production +50; Keynesian food +50; Proletariat production +50; Qualified Labor production +50.
- Route profit is raised by the city's **trade route modifier**:
  - the Market +25 % (and +25 % foreign);
  - the Harbor +50 %, the Port, Commercial Port and International Port +50 % (and +25 % to +50 % foreign);
  - the Fair, Commodity Market and Commercial Center +30 % to +40 % (and +40 % to +50 % foreign);
  - city size and the capital.
- The **number of routes** comes from the buildings:
  - the settlement tiers: Town and City Essentials +1, Metropolitan Essentials +2;
  - Harbor +2, Port +3, Commercial Port +4, International Port +5, River Port +1.

**What follows.** The settlement tiers, markets and harbors multiply the food and production that the civics put on
trade routes. That is the supply and migration route you built (M76). The migration model's reach (D33) is
therefore built on these values: more routes and higher route profit carry more supply and more migrants. GitLab
main (71de0abe) is the same commit the economy branch started from, so nothing newer exists elsewhere.

### 0b. The goods classing

You discussed it at length (M57, M58, M67-M71, M75), and I wrongly called it your open call. Settled from what you
said:
- **Sectors (D26, M57, confirmed M58):** basic resources (seeds, timber, ore, leather...), essential needs,
  artisanal products, industrial goods, luxury goods. Wine and whale go under luxury, livestock under basic
  resources (M58: "Yes").
- **Food values are not categories any more.** Each food carries calories, satiety and health as three separate
  measures (M75). Meat, dairy and fish are among the most satiating per calorie and the complete protein (M57, M69).
  Liquid milk is a drink valued for hydration, protein and fats per day (M71). "Staple" and "variety" as categories
  are replaced by these measures.
- **Shelf life:** cereal products, dried fruit, fermented dairy, cured meat and fish keep longest and add most to the
  store (M57).
- **Confirm:** the further roles from my food survey (R21):
  - Whale as food (meat) besides oil;
  - Horse meat and mare's milk;
  - Olives as oil;
  - Sugar, Wine and Alcohol counted for their calories;
  - Salt as a preserver;
  - Lemon against scurvy.

  You did not object, but you did not approve them by name either.

---

## 1. The vision (M01-M07, M16)

**What you said:**
- Replace map bonuses (berries, ores, "cartoon animals on the sea") with land of varying qualities by climate and
  hemisphere, as attributes of regions rather than tokens (M01, M03).
- Towns produce goods from tiles, improvements, buildings, specialists and their population, and consume plausible
  amounts. Real quantities (tonnes of wheat, dairy, coal), then industry, trade and unit production. Diplomacy ships
  products, sells seeds and makes packages instead of "348 gold per turn" (M04).
- A fully sculpted vision, not patchwork; cut the Gordian knot; branches can be reverted (M07).

**The design statement (M16).** Physical quantities; production from the whole settlement; consumption from
population; industry transforms goods; military power has a material cost; trade carries the goods; the simulation
in the DLL.

**Recorded:** `plan/statement.md`, design elements P1-P7, and now P8 (AI awareness and UI for every mechanic, M75).

## 2. Ground rules of working (M10-M15, M18, M22, M23, M29-M34, M37-M38, M42, M46-M49, M73)

**What you said:**
- Work from first principles; tests and reports are tools, not the product. What matters is what the player sees,
  whether the game crashes, and an intuitive interface (M11).
- Do not hyperfixate on food (M12).
- No erratic patchwork; a step-by-step plan tied to the code (M14), kept as checkable JSON because my context is
  wiped (M15, M18, M22, M37).
- A separate test branch (M23).
- Check priors in the actual XML and Python (M29, M31, M33); use the code map and fix it if needed (M32).
- Ask in plain terms when specifics matter (M34).
- Store important files and tools on GitHub (M38).
- Look at the codebase rather than test blindly (M42).
- Meaning before means (M47-M49).
- Know the tools, like the code map (M73).
- **Later decisions over earlier ones; be consistent and conscientious** (M79).

**Recorded:** CLAUDE.md working rules A-F; requests.json; the plan's current block.

**Confirm:** this session has been heavily about food and population. That followed your prompts M53-M79, but M12
warned against fixating on food. Should the next stretch turn to the other components (production chains, industry,
trade)?

## 3. Goods: which exist, their units and icons (M09, M15, M17, M21, M24-M28, M31, M35-M36, M39, M41, M58-M60, M76-M77)

**What you said:**
- Goods in tonnes or similar whole units that cannot overflow; integers make diplomacy intuitive (M09).
- Keep the game's number of goods for now (M17). Later you asked for:
  - Timber, Wool, Dairy and Leather (M21);
  - Meat, counted with the livestock (M59);
  - charcoal (M59);
  - steel and machinery (M59);
  - tools and arms (M59);
  - Flax/linen, Cloth, Fine Cloth, Coats and Dresses (M76).
- No missing icons; realistic textures with the art studio (M15, M21, M24).
- Keep sheep; seeds and cattle are needed (M27).
- Wool and leather are clothing and toolmaking materials, dairy must be consequential, timber essential (M31).
- Timber's reveal and trade techs moved (M36).
- Hunting camps do not give wool or dairy (M41).
- "Just fix the limit" on records (M77).

**Recorded:**
- D1 (whole units);
- LQ.F8-F13 (Timber, Dairy, Leather, Wool restored; lumber camps and pastures; icons);
- D35 (no record-count limit below the font's 98 resource slots; graphics paging for memory).

**Status:**
- Timber, Dairy, Leather and Wool exist on the branch.
- The icons wait on your in-game check (LQ.F9.T5, T6).
- The lumber camp button and the Glass button have sources (CC0 and public domain, `art_sources.md`), but are not
  made yet.

**Confirm:** that the full list of goods to add is Flax, Cloth, Fine Cloth, Coats, Dresses, Meat, charcoal, steel,
machinery, tools and arms. Some of these are perhaps recipes inside the city rather than goods, as bread is. Which
ones?

## 4. Tiles, land and production (M01, M03, M17, M35, M39, M41, M53-M55, M57, M66)

**What you said:**
- Change geography and tiles first (M17).
- Lumber:
  - lumber camps at Metal Casting;
  - lumbermills at Machinery;
  - Bronze Working, Iron Working and Mathematics boost lumber;
  - Machinery does not boost lumber camps;
  - lumbermills 5 (M35, M39, M41).
- Pastures yield every product of their animal, Latifundia too (M35).
- Output depends on the real population employed, the efficiency given technologies and resources, land quality and
  the kind of good, "somewhat true to a real agricultural economy" (M53).
- Fermentation raises food value through bioavailability, not the harvest (M54).
- Flows per year until sub-year turns (M54); each map declares its area per tile (M55).
- Scale by land; the sea has its own mechanics: fish until overfishing; pearls; oil like an ore but not quite (M57).
- Output depends on tech, the people working the tile, their qualification, tools and machinery, fertility and the
  good (meat, dairy, fish, sugar, bananas too) (M66).

**Recorded:**
- D19, D20 (lumber, pastures);
- D23 (the production model);
- D25 (land scale; sea mechanics);
- PR.F6 done (map scale in all scenarios and map scripts);
- the tile formula (`tile_output.md`): output = yield(good, tech) × fertility × cropped share × min(usable area,
  workers × skill × ha per worker);
- the sourced yield tables (USDA NASS; `open_questions.md` sections 1-3).

**Open:** usable land per terrain; pastoral and fish yields still estimated.

## 5. Food, satiety, health and drink (M09, M54, M57, M69-M71, M75)

**What you said:**
- Cities grow with a food surplus and are not starving by default (M09).
- Meat, dairy and fish give the most nutrition and satiety. High-protein foods give unit strength bonuses, except to
  siege, vehicles, robots and machines (M57), and also not to hi-tech, biological, clone, worker, settler and animal
  units (M58).
- Animal foods carry calories (M69).
- Liquid milk: hydration, bioavailable protein and fats, lactose a stable carbohydrate; drinks are measured per day,
  like water or juice (M71).
- Calories, satiety and health are three separate measures, and should be mapped per good (M75):
  - apples and olives are healthy but barely satiating;
  - cured meat, canned food and fast food are satiating but harm health;
  - grains barely satiate and bring kidney stones, dental problems and scurvy, and build no muscle alone.
- Good food raises fertility, productivity, commercial, scientific and cultural output; not just a strength margin
  (M75).

**Recorded:**
- D27, its choice rewritten (M78);
- D31 (water and hydration, decided M73);
- `round_m75.md` section 2 (the three measures);
- `open_questions.md` section 4b (drinks).

**Status:** nutrition.json still uses one combined satiety number; PR.F8.T5 splits it before step 1.

**Confirm:**
- "fast food" is a modern good the game does not have. Should one be added, or is it an example only?
- I found sources for childhood bladder stones on grain diets, not kidney stones. Is that the ailment you meant?

## 6. Spoilage and storage (M09, M50-M51, M57, M59, M75)

**What you said:**
- Spoilage only by the technology a player lacks: pottery, fermentation, refrigeration (M09).
- Deal with spoilage later, when the system works (M50, M51).
- Preserved foods keep longest (M57).
- The Cannery prolongs shelf life; no canned-food good (M59).
- One spoilage rate per good by technology, also by infrastructure and climate "if it's a thing yet" (M75).

**Recorded:** D27 (M75 option C).

**Status:** the goods pass with storage and spoilage exists (GW.F5); spoilage is in the route again (M79).

## 7. Population (M54, M62, M63-M65, M75-M79)

**What you said:**
- A working citizen stands for the real population at first (M54, option a).
- The first citizen at size 1 should produce much less than the one at 36; the exponential count does not map to
  real dynamics (M62).
- Research the population model (M63).
- Not disasters for now; better modelling in general, without 10,000 variables (M64, M65).
- Growth by nutrient quality and quantity; good food raises fertility and outputs; players decide, not a curve;
  urban density, the economy, war and pillage matter; no era growth rates; health lowers growth or turns it negative;
  no death term needed; check the food box rendering (M75).
- More research, mathematical modelling, edge cases (M76).
- Health and fertility missing (M77).
- No deaths in the formula (M78).
- The evidence-based model was nearly right and should not have been shrunk (M79).

**Recorded:**
- D30, open: the fourth version (`pop_model_math.md`): growth = fertility − health burden, each built from its
  evidence;
- D32 (64-bit people);
- the food box check (`round_m75.md` section 4).

**Confirm:**
- Is the fourth version right?
- How should the city size follow people: the inverse of today's curve, or labour units?

## 8. Migration (M75, M76, M77)

**What you said:**
- Migration needs a civic parameter, civic by civic.
- Cities grow beyond their births only through migration.
- Your trade-route modifiers in civics, settlement tiers, marketplaces and harbors already stand for supply and
  migration routes.
- Skills, culture and burdens move with people, both ways.

**Recorded:** D33 (decided M77); civic values in `round_m76.md` section 2c.

**Correction (0a):** the reach of migration now follows your trade-route system as the DLL computes it.

## 9. Water (M71-M73)

**What you said:** drinks per day; implement hydration and water supply; you agreed to the proposal (M73).

**Recorded:** D31: two needs (drink 1.8 L by hydration index; household water at the WHO levels), city supply in m³ a
day, quality, effects through health, drinks as goods, water for herds.

## 10. Clothing (M75-M77)

**What you said:**
- Clothing is both warmth and status.
- The goods are the fibres and skins (Flax added), Cloth, Fine Cloth, coats and dresses.
- Dress depends on technology, resources, tools, machines, skilled labour, religiosity and culture (prudish or
  permissive eras), diversity, secularization, markets and media.
- A consumption rate per citizen from garment lifetime, cloth per person and the city's wealth.

**Recorded:** D28 (clothing parts); `round_m76.md` section 3; `round_m77.md` section 3.

**Open:** sourced lifetimes and cloth per person.

**Confirm:** does "per citizen" mean per real person?

## 11. Production chains and industry (M58, M59)

**What you said:**
- The input-less buildings get inputs: aluminum from bauxite, diesel from oil, cement from stone and coal, rubber from
  rubber and oil and chemicals (M59, M60).
- Bread and Weapons Manufactories boost bread and arms.
- No building per step because of the 32-bit executable (M59); see D35.
- The essentials stages carry functions.
- No flour at mills.
- The city makes artisanal goods from base goods and techs from communal economies on.
- Charcoal yes. Tools from ores, bauxite and lead too, not a Minecraft-style tier copy.
- The Forge and Factory make arms; the Armourer and Jewellery use them.
- Steel from iron and coal; machinery at the Factory.
- Cow, Pig and Sheep counted in head with Meat; Deer gives meat; Fur for clothing.

**Recorded:** D28 (decided M59, M60).

**Confirm:** with no measured limit found (D35), do you keep M59's "no building per step"?

## 12. Guilds (M59-M62, M75-M77)

**What you said:**
- Reworked, not the sole source of goods, perhaps national wonders (M59).
- All XML fields matter (M60).
- No more modifiers stacked on modifiers (M61).
- No low-quality default.
- Luxury goods and master craftsmen.
- Glassmakers once per game.
- Techniques carried by Master units, traded, stolen.
- Quality grades to specify.
- No innovation brake; no public-order bonus but a socioeconomic role.
- National guilds plus the world master guild (M62, option 3).
- Once per game only for secret techniques; three grades; councils, fixed prices and limited places with civics, UI
  and AI; workshops with the guild or hall, sized by population, not specialists (M75).
- Food guilds raise quality, employment and protection; masterwork goods; education makes adjacent techs cheaper
  through a new field (M76).
- Masons speed building and are required for the Architecture cathedrals; Clerks for science and administration
  (M76, M77).

**Recorded:** D29; D34 (rebuilt in M79, `d34_research_modifiers.md`).

**Open:** the luxuries of the other guilds (D29 b).

## 13. Map data and economy screens (M56, M75)

**What you said:**
- The BeginEconomy block can carry finite ore deposits, fertility ranges, starter seeds, trade-route settings, and
  switchable economy screens: import/export, loans, bonds, a national budget, national debt, central planning, a
  Roman senate (M56).
- "B as discussed. A really big change, but necessary" (M75).

**Recorded:** D24 (decided M75).

## 14. Interface (M11, M52, M57, M75)

**What you said:**
- What the player sees matters most (M11).
- A mock-up (M52).
- Anno-like sectors, an overview per city and in the economic advisor, consistent with the game (M57).
- Check whether the UI can be changed as wanted (M75).

**Recorded:** D26; the mock-up artifact (R9.1, waiting on your judgement); the food box check.

## 15. Trade and diplomacy (M04, M15, M17, M20, M56)

**What you said:**
- Real commerce, seeds, packages (M04).
- Trade will involve far more than cattle trades (M15).
- Modify the trade screen if possible, not a separate one; distribution close to how the game works (M17).
- Blockades are a thing; transport limits only for units (M20).

**Recorded:** the TR component (not started).

## 16. Media (M35, M75)

**What you said:**
- Media are valuable goods, perhaps reworked (M35).
- Services by reach that scales with technology, buildings and infrastructure; importable and exportable; applying
  across the country, as the Forge unlocks Gold (M75).

**Recorded:** D21 (decided M75).

## 17. Other resources (M35)

**What you said:** Ancient Temples serve archaeology; thermal vents give electricity (M35).

**Recorded:** in the M35 notes. **Confirm:** that these stay out of the goods economy as non-goods.

---

## Questions to answer before the plan moves on

1. 0b: the further food roles of R21 (Whale, Horse, Olives, Sugar, Wine, Alcohol, Salt, Lemon).
2. Section 2: turn away from food and population toward the other components next?
3. Section 3: which new goods are goods, and which are recipes inside the city?
4. Section 5: fast food as a good; kidney or bladder stones.
5. Section 7: the fourth population model, and city size from people.
6. Section 10: "per citizen" for clothing.
7. Section 11: keep or drop "no building per step".
8. Section 12: the other guilds' luxuries.
9. Section 17: Ancient Temples and thermal vents outside the goods economy.
