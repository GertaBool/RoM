#ifndef ROM_SIMULATION_CITY_ECONOMY_H
#define ROM_SIMULATION_CITY_ECONOMY_H

// Phase-local arithmetic. No game pointers, allocation, RNG or native mutation.
#include <algorithm>
#include <climits>

namespace CityEconomy {
#if defined(_MSC_VER)
typedef __int64 Wide;
#else
typedef long long Wide;
#endif
typedef char IntMustBe32Bits[(INT_MAX == 2147483647) ? 1 : -1];

enum Status {
    Applied, PopulationEffectsRequired, CompletionEffectsRequired, UnitCreationRequired,
    CallbackUnsupported, ProductionChoiceRequired, ProcessUnsupported,
    InvalidSnapshot, NativeArithmeticRange
};
inline const char* statusName(Status s) {
    switch (s) {
    case Applied: return "applied";
    case PopulationEffectsRequired: return "population_effects_required";
    case CompletionEffectsRequired: return "completion_effects_required";
    case UnitCreationRequired: return "unit_creation_required";
    case CallbackUnsupported: return "callback_unsupported";
    case ProductionChoiceRequired: return "production_choice_required";
    case ProcessUnsupported: return "process_unsupported";
    case InvalidSnapshot: return "invalid_snapshot";
    case NativeArithmeticRange: return "native_arithmetic_range";
    }
    return "invalid_status";
}
inline bool nativeInt(Wide value) { return value >= INT_MIN && value <= INT_MAX; }
inline bool flag(int value) { return value == 0 || value == 1; }

struct GrowthSnapshot {
    int population, food, foodKept, threshold, keptPercent;
    int foodYield, consumption, foodProduction, disorder, avoidGrowth, callback;
};
struct GrowthResult {
    Status status;
    int population, food, foodKept, difference, grew;
    explicit GrowthResult(const GrowthSnapshot& s): status(Applied),
        population(s.population), food(s.food), foodKept(s.foodKept),
        difference(0), grew(0) {}
};
inline GrowthResult grow(const GrowthSnapshot& s) {
    GrowthResult r(s);
    if (s.population < 1 || s.food < 0 || s.foodKept < 0 || s.threshold < 1 ||
        s.keptPercent < 0 || s.foodYield < 0 || s.consumption < 0 ||
        !flag(s.foodProduction) || !flag(s.disorder) || !flag(s.avoidGrowth) ||
        !flag(s.callback)) { r.status = InvalidSnapshot; return r; }
    if (s.callback) { r.status = CallbackUnsupported; return r; }
    int difference = s.disorder ? 0 : s.foodYield - s.consumption;
    if (s.foodProduction) difference = std::min(0, difference);
    if (s.population == 1 && s.food == 0) difference = std::max(0, difference);
    Wide food = Wide(s.food) + difference;
    Wide kept = Wide(s.foodKept) + difference;
    const Wide capProduct = Wide(s.threshold) * s.keptPercent;
    // Reject undefined native int arithmetic, even if a later clamp would hide it.
    if (!nativeInt(food) || !nativeInt(kept) || !nativeInt(capProduct)) {
        r.status = NativeArithmeticRange; return r;
    }
    kept = std::max(Wide(0), std::min(kept, capProduct / 100));
    int population = s.population;
    if (food >= s.threshold) {
        if (s.avoidGrowth) food = s.threshold;
        else {
            if (population == INT_MAX) { r.status = NativeArithmeticRange; return r; }
            food -= std::max(Wide(0), Wide(s.threshold) - kept);
            ++population;
            r.grew = 1;
        }
    } else if (food < 0) {
        food = 0;
        if (population > 1) --population;
    }
    r.food = int(food); r.foodKept = int(kept); r.population = population;
    r.difference = difference;
    if (population != s.population) r.status = PopulationEffectsRequired;
    return r;
}

struct ProductionSnapshot {
    int progress, needed, baseProduction, totalModifier;
    int foodYield, consumptionNoAngry, overflow, feature;
    int foodProduction, disorder, callback, choiceRequired;
    int process, hasOrder, allowNoProduction;
};
struct ProductionResult {
    Status status;
    int progress, overflow, feature, difference;
    explicit ProductionResult(const ProductionSnapshot& s): status(Applied),
        progress(s.progress), overflow(s.overflow), feature(s.feature), difference(0) {}
};
inline ProductionResult produce(const ProductionSnapshot& s) {
    ProductionResult r(s);
    if (s.progress < 0 || s.needed < 0 || s.baseProduction < 0 || s.totalModifier < 0 ||
        s.foodYield < 0 || s.consumptionNoAngry < 0 || s.overflow < 0 || s.feature < 0 ||
        !flag(s.foodProduction) || !flag(s.disorder) || !flag(s.callback) ||
        !flag(s.choiceRequired) || !flag(s.process) || !flag(s.hasOrder) ||
        !flag(s.allowNoProduction)) { r.status = InvalidSnapshot; return r; }
    if (s.callback) { r.status = CallbackUnsupported; return r; }
    if (s.choiceRequired) { r.status = ProductionChoiceRequired; return r; }
    if (!s.allowNoProduction && !s.hasOrder) return r;
    if (s.process) { r.status = ProcessUnsupported; return r; }
    if (s.disorder) return r;
    const Wide overflow = s.hasOrder ? Wide(s.overflow) + s.feature : 0;
    const Wide base = s.baseProduction + overflow;
    if (!nativeInt(overflow) || !nativeInt(base)) {
        r.status = NativeArithmeticRange; return r;
    }
    const Wide multiplied = base * s.totalModifier;
    const int food = s.foodProduction ? std::max(0, s.foodYield - s.consumptionNoAngry) : 0;
    const Wide difference = multiplied / 100 + food;
    if (!nativeInt(overflow) || !nativeInt(base) || !nativeInt(multiplied) || !nativeInt(difference)) {
        r.status = NativeArithmeticRange; return r;
    }
    if (s.hasOrder) {
        const Wide progress = s.progress + difference;
        if (!nativeInt(progress)) { r.status = NativeArithmeticRange; return r; }
        r.progress = int(progress); r.overflow = 0; r.feature = 0;
        // Boundary immediately BEFORE popOrder; no completion effects are invented.
        if (progress >= s.needed) r.status = CompletionEffectsRequired;
    } else {
        const Wide numerator = 100 * difference;
        const Wide stored = s.overflow + numerator / std::max(1, s.totalModifier);
        if (!nativeInt(numerator) || !nativeInt(stored)) {
            r.status = NativeArithmeticRange; return r;
        }
        r.overflow = int(stored);
    }
    r.difference = int(difference);
    return r;
}
// Unit orders only. Buildings can change modifiers BEFORE their overflow code.
struct UnitCompletionSnapshot {
    int progress, needed, currentProductionNoOverflow, totalModifier;
    int baseModifier, goldPercent, overflow;
};
struct UnitCompletionResult {
    Status status;
    int progress, overflow, gold;
    explicit UnitCompletionResult(const UnitCompletionSnapshot& s): status(UnitCreationRequired),
        progress(s.progress), overflow(s.overflow), gold(0) {}
};
inline UnitCompletionResult completeUnit(const UnitCompletionSnapshot& s) {
    UnitCompletionResult r(s);
    if (s.needed < 0 || s.progress < s.needed || s.currentProductionNoOverflow < 0 ||
        s.totalModifier < 0 || s.baseModifier < 0 || s.goldPercent < 0 || s.overflow < 0) {
        r.status = InvalidSnapshot; return r;
    }
    const int excess = s.progress - s.needed;
    const int cap = std::max(s.needed, s.currentProductionNoOverflow);
    const int carried = std::min(cap, excess);
    const Wide normalization = Wide(100) * carried;
    const Wide lostScaling = Wide(std::max(0, excess - cap)) * s.baseModifier;
    if (!nativeInt(normalization) || !nativeInt(lostScaling)) {
        r.status = NativeArithmeticRange; return r;
    }
    const Wide overflow = s.overflow + normalization / std::max(1, s.totalModifier);
    const Wide goldProduct = (lostScaling / std::max(1, s.totalModifier)) * s.goldPercent;
    if (!nativeInt(overflow) || !nativeInt(goldProduct)) {
        r.status = NativeArithmeticRange; return r;
    }
    r.progress = 0; r.overflow = int(overflow); r.gold = int(goldProduct / 100);
    return r;
}
} // namespace CityEconomy
#endif
