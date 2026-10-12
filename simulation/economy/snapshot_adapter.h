#ifndef ROM_SIMULATION_SNAPSHOT_ADAPTER_H
#define ROM_SIMULATION_SNAPSHOT_ADAPTER_H
#include "city_economy.h"

namespace CityEconomy {
// Instantiate against CvCity only at the named native phase boundary.
// Yield enum values are explicit to keep this header independent of DLL headers.
// Callbacks are effective runtime settings, never guessed from base XML.
template<class City, class Yield>
GrowthSnapshot captureGrowth(City& city, Yield foodYieldType, bool callbackEnabled) {
    GrowthSnapshot s;
    s.population = city.getPopulation(); s.food = city.getFood();
    s.foodKept = city.getFoodKept(); s.threshold = city.growthThreshold();
    s.keptPercent = city.getMaxFoodKeptPercent();
    s.foodYield = city.getYieldRate(foodYieldType);
    s.consumption = city.foodConsumption();
    s.foodProduction = city.isFoodProduction(); s.disorder = city.isDisorder();
    s.avoidGrowth = city.AI_isEmphasizeAvoidGrowth(); s.callback = callbackEnabled;
    return s;
}

template<class City, class Yield>
ProductionSnapshot captureProduction(City& city, Yield foodYieldType, Yield productionYieldType,
                                     bool callbackEnabled, bool allowNoProduction) {
    ProductionSnapshot s;
    s.hasOrder = city.isProduction(); s.process = city.isProductionProcess();
    s.callback = callbackEnabled; s.allowNoProduction = allowNoProduction;
    s.choiceRequired = (!city.isHuman() || city.isProductionAutomated()) &&
        (!s.hasOrder || s.process || city.AI_isChooseProductionDirty());
    s.disorder = city.isDisorder();
    s.progress = (s.hasOrder && !s.process) ? city.getProduction() : 0;
    s.needed = (s.hasOrder && !s.process) ? city.getProductionNeeded() : 0;
    s.baseProduction = city.getBaseYieldRate(productionYieldType);
    s.totalModifier = city.getBaseYieldRateModifier(productionYieldType, city.getProductionModifier());
    s.foodYield = city.getYieldRate(foodYieldType);
    s.consumptionNoAngry = city.foodConsumption(true);
    s.overflow = city.getOverflowProduction(); s.feature = city.getFeatureProduction();
    s.foodProduction = city.isFoodProduction();
    return s;
}
} // namespace CityEconomy
#endif
