#include "city_economy.h"
#include <iostream>
#include <sstream>
#include <string>
using namespace CityEconomy;

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream in(line); char kind; std::string extra;
        if (!(in >> kind)) { std::cerr << "empty record\n"; return 2; }
        if (kind == 'G') {
            GrowthSnapshot s;
            if (!(in >> s.population >> s.food >> s.foodKept >> s.threshold >> s.keptPercent
                     >> s.foodYield >> s.consumption >> s.foodProduction >> s.disorder
                     >> s.avoidGrowth >> s.callback) || (in >> extra)) {
                std::cerr << "invalid growth record\n"; return 2;
            }
            GrowthResult r = grow(s);
            std::cout << "{\"status\":\"" << statusName(r.status) << "\",\"population\":" << r.population
                      << ",\"food\":" << r.food << ",\"food_kept\":" << r.foodKept
                      << ",\"difference\":" << r.difference << ",\"grew\":" << r.grew << "}\n";
        } else if (kind == 'P') {
            ProductionSnapshot s;
            if (!(in >> s.progress >> s.needed >> s.baseProduction >> s.totalModifier
                     >> s.foodYield >> s.consumptionNoAngry >> s.overflow >> s.feature
                     >> s.foodProduction >> s.disorder >> s.callback >> s.choiceRequired
                     >> s.process >> s.hasOrder >> s.allowNoProduction) || (in >> extra)) {
                std::cerr << "invalid production record\n"; return 2;
            }
            ProductionResult r = produce(s);
            std::cout << "{\"status\":\"" << statusName(r.status) << "\",\"progress\":" << r.progress
                      << ",\"overflow\":" << r.overflow << ",\"feature\":" << r.feature
                      << ",\"difference\":" << r.difference << "}\n";
        } else if (kind == 'U') {
            UnitCompletionSnapshot s;
            if (!(in >> s.progress >> s.needed >> s.currentProductionNoOverflow >> s.totalModifier
                     >> s.baseModifier >> s.goldPercent >> s.overflow) || (in >> extra)) {
                std::cerr << "invalid unit completion record\n"; return 2;
            }
            UnitCompletionResult r = completeUnit(s);
            std::cout << "{\"status\":\"" << statusName(r.status) << "\",\"progress\":" << r.progress
                      << ",\"overflow\":" << r.overflow << ",\"gold\":" << r.gold << "}\n";
        } else { std::cerr << "unknown phase\n"; return 2; }
    }
}
