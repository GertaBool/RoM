# Transformation plan: from resource tokens to land and goods

The goal: resources stop being icons connected to a network and become qualities of the land. Towns make goods from
land, workers, buildings and population, consume them, and trade, ship and build with them, in tons.

Every function named below exists in the RoM DLL source (GitLab `main`); the line of work is in that repository.

## Rules the plan keeps

- **One architecture, laid down first.** Step 1 adds every data structure the later steps fill (the goods stock,
  the deal quantity, the goods fields of the records, the turn hook). Later steps add rules, never new plumbing.
- **The bridge keeps the game whole.** The engine counts resources per trade network (`CvPlotGroup`), and every
  building, unit, civic and AI check asks that count (`CvCity::hasBonus`). From step 2 on, the count is fed from the
  goods stock instead of from map icons, so nothing that reads resources breaks while the rest changes.
- **Resource types are the goods.** Each `BonusType` is a good; made goods (cloth, tools, bronze) are new
  `BonusInfo` records that are never placed on the map. Icons, Civilopedia, trade screen and requirements are reused.
- **Food stays the engine's yield** in this plan (growth pacing is untouched). Grain enters the goods stock only as
  tradeable surplus (step 5).
- **Each step ends playable**, with old saves loading, 5 headless games without a crash or slower turns, and your
  own game. A step is not started before the previous one is done.

## Step 1. Foundations (nothing changes in play)

| What | Code |
|---|---|
| Goods fields on resource records: class (raw, made, food), tons per unit of output, storage per citizen, base price | `CvBonusInfo::read(CvXMLLoadUtility*)`, `CvBonusInfo::copyNonDefaults`, `CvInfos.h`; `CIV4TerrainSchema.xml`; `CIV4BonusInfos.xml` |
| Goods stock per city: stock, made, used, received, sent (int tons per good) | `CvCity.h`; `CvCity::init`, `reset`, `read`, `write` (behind the save version flag) |
| Goods-provided resource count per city, added to the network like a building's free resource | new `m_paiGoodsBonus` in `CvCity`; one term in `CvPlot::updatePlotGroupBonus` next to `getFreeBonus` |
| Quantity per deal item (tons per turn), stored with the deal | `CvDeal.h`; `CvDeal::read`, `write`; set in `CvDeal::addTrades` |
| The goods pass: one call per player per turn, before its cities | `CvPlayer::doTurn` calls `CvPlayer::doGoods()` (new, empty) |
| Trade screen check: a resource item whose text carries tons ("Copper, 20 t per turn") | `CvGameTextMgr::getTradeString` (`TRADE_RESOURCES`); `CvPlayer::buildTradeTable` |

Done when old saves load, 5 games run clean, and the diplomacy screen shows and accepts an item with tons in its text
(the one point where the closed executable could object; the item keeps a valid resource index, so it cannot crash on it).

## Step 2. Goods from worked land (today's map)

The player sees: each city's goods panel (tons made, used, stored per good) where the resource list is today; a
worked wheat plot makes tons of wheat each turn. An unworked resource plot makes nothing.

| What | Code |
|---|---|
| A worked plot with a resource and its improvement adds tons to the city's stock | `CvPlayer::doGoods` (loop over cities and worked plots); amounts from `CvBonusInfo` and `CvImprovementInfo` |
| Placed resources stop feeding the network directly; the goods-provided count does instead (a network with stock of a good "has" it) | `CvPlot::updatePlotGroupBonus` (the placed-resource branch); `CvCity::changeGoodsBonus` (new, same pattern as `changeFreeBonus`) |
| The governor values the goods a plot gives | `CvCityAI::AI_yieldValue`, `CvCityAI::AI_juggleCitizens` |
| City screen goods panel | `Python/Screens/CvMainInterface.py` (the `BonusList` panel) |
| Plot help: what the plot makes in tons | `CvGameTextMgr::setPlotHelp` |

Done when every building and unit that needed a resource still builds where the good is in stock, and AI cities work
their resource plots.

## Step 3. Distribution and consumption

The player sees: goods shared automatically across a connected network; citizens consuming goods by tier; health and
happiness from what is supplied, shown in the usual breakdowns ("+2 from goods").

| What | Code |
|---|---|
| Network stock: cities in one network pool goods; exact integer rationing | `CvPlayer::doGoods`; network membership from `CvPlotGroup` |
| Consumption per citizen by tier (everyday, comfort, luxury), tons per citizen in XML | `CvPlayer::doGoods`; tier and amounts in `CvBonusInfo` |
| Health and happiness from citizens supplied replace the flat per-resource bonus | `CvCity::processBonus` (per-resource health and happiness off for goods); `CvCity::changeBonusGoodHealth`, `changeExtraHappiness` set by the goods pass |
| Breakdown text | `CvGameTextMgr::setHappyHelp`, `setAngerHelp`, `setGoodHealthHelp`, `setBadHealthHelp` |
| The governor and build AI see shortages | `CvCityAI::AI_yieldValue`, `CvCityAI::AI_buildingValue` |

## Step 4. Workshops and recipes

The player sees: buildings with workshop slots (smithy, weaver, mill); an artisan turns inputs into outputs each turn;
tools raise the city's production.

| What | Code |
|---|---|
| Recipes on buildings: inputs, outputs, runs per artisan | `CvBuildingInfo::read`, `copyNonDefaults`; `CIV4BuildingsSchema.xml`; `CIV4BuildingInfos.xml` |
| Artisan occupations: specialists that run a recipe | `CvSpecialistInfo::read`; `CIV4SpecialistInfos.xml` |
| Recipes run in dependency order inside the goods pass | `CvPlayer::doGoods` |
| Tools and power as production modifiers | `CvCity::changeBaseYieldRate` (production), set by the goods pass |
| Production help text | `CvGameTextMgr::setProductionHelp` |
| AI: build recipe buildings whose outputs are worth more than inputs and labour | `CvCityAI::AI_buildingValue`, `CvCityAI::AI_chooseProduction` |

## Step 5. Trade in quantities

The player sees: deals in tons per turn for a term ("40 t of wool a turn for 20 t of copper, 20 turns"); surplus
grain offered like any good; the AI asking for what it lacks and selling what it has spare.

| What | Code |
|---|---|
| A resource item moves its tons every turn instead of switching the resource on | `CvDeal::doTurn`, `CvDeal::startTrade`, `CvDeal::endTrade` (no more `changeBonusExport`/`changeBonusImport` for goods) |
| An item can be offered only from surplus | `CvPlayer::canTradeItem`, `CvPlayer::getTradeDenial` |
| Grain surplus as a good (food beyond growth, taken from the food box) | `CvPlayer::doGoods`; `CvCity::doGrowth` reads the exports |
| AI value of a good from its shortage or surplus (one function feeds trades, sites and builds) | `CvPlayerAI::AI_baseBonusVal`, `AI_bonusTradeVal`, `AI_bonusTrade` |
| AI offers and requests | `CvPlayerAI::AI_doDiplo` |

## Step 6. Land qualities replace placed resources

The player sees: no resource icons; the land itself has qualities shown in the plot help ("wheat: good; copper ore:
rich, shallow") and in a map overlay. What a farm, pasture or mine makes follows the land.

| What | Code |
|---|---|
| Plot qualities: crop and herd suitability, ore grade and depth, fishing capacity (small ints, saved) | `CvPlot.h`; `CvPlot::read`, `write` |
| Qualities computed once the map exists, from terrain, latitude, rivers and coasts; ore regions seeded from the resources the map script or scenario placed, which are then removed. One routine for generated maps, scenarios and old saves alike: it runs when a flag saved with the game is unset | new `CvGame::buildLandQualities()`, called from `CvGame::doTurn`; the flag in `CvGame::read`, `write`; `CvPlot::setBonusType` |
| Goods from land quality and improvement replace resource yields | `CvPlot::calculateYield`; `CvPlayer::doGoods` |
| Plot help and overlay | `CvGameTextMgr::setPlotHelp`; a goods overlay in Python on the pattern of `Python/Contrib/CvStrategyOverlay.py` (`CyEngine().addColoredPlot`) |
| AI: city sites, worker builds and plot values from qualities | `CvPlayerAI::AI_foundValue`, `CvUnitAI` worker build choice, `CvCityAI::AI_yieldValue` |

## Step 7. Units and war from goods

The player sees: units that cost goods as well as production (a legion needs iron arms); a city without them cannot
train the unit.

| What | Code |
|---|---|
| Goods costs on units | `CvUnitInfo::read`; `CIV4UnitInfos.xml` |
| Training checks and consumes the goods | `CvCity::canTrain`; unit completion in `CvCity::popOrder` |
| AI weighs goods costs in what it trains | `CvCityAI::AI_chooseProduction` |

## Step 8. Seeds, techniques and package deals

The player sees: seed and breeding stock offered in deals; buying rice seed lets your suitable land grow rice.

| What | Code |
|---|---|
| Seeds are goods ("rice seed"), traded with the step-5 item; importing one unlocks that crop on suitable land for the buyer | new `BonusInfo` records; `CvPlayer::doGoods`; `CvPlot::calculateYield` |
| AI values seeds by the land it could use them on | `CvPlayerAI::AI_baseBonusVal` |

## What is never changed

The executable; the three yields and four commerce outputs; the growth rule; the tech tree; civics' structure.
