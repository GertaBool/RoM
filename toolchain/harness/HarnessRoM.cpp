// Harness-only: Rise of Mankind's Python rules for buildings, mirrored in C++
// because the harness runs the DLL without Python. Compiled only into harness
// builds of CvGameCoreDLL.
//
//   RoMGameUtils.py   cannotConstruct      upgrade lines, observatory and
//                                          Copernicus terrain, Djenne desert,
//                                          zCivics building prerequisites
//                     getBuildingCostMod   Djenne cathedrals, civic discounts
//                     getUnitCostMod       missionaries under State Religion
//   RoMEventManager.py onBuildingBuilt     upgrade lines remove the buildings
//                                          they replace; Djenne, World Bank and
//                                          Crusade effects
//                     onBeginPlayerTurn    World Bank interest, Crusader spawns
//
// Without the upgrade lines a harness city keeps every tier of a line (scribes,
// library and university; market, fair and commodity market; every harbour and
// port) and grows and earns far more than in the game. The upgrade-line and
// zCivics tables are generated from the Python by build_dll.sh
// (HarnessRoMTables.h), so they follow the mod. Not mirrored: getUpgradePriceOverride
// (Personal Replicators), the Nanite Defuser and Eden project effects, and
// Enhanced Tech Conquest's research points for a conquered city.
#include "CvGameCoreDLL.h"
#include "CvGameAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvPlayerAI.h"
#include "CvTeamAI.h"
#include "CvCity.h"
#include "CvInfos.h"
#include "CvGameCoreUtils.h"
#include <algorithm>
#include <map>
#include <set>
#include <vector>
#include "HarnessRoMTables.h"

namespace
{
	struct RoMRules
	{
		bool bInit;
		std::vector<std::pair<int, int> > aUpgradePairs;   // (upgrade, replaced), Python order
		std::map<int, std::vector<int> > mSupersededBy;     // replaced -> upgrades
		std::map<int, int> mBuildingCivic;                  // building -> required civic
		int eObservatory, eCopernicus, eNewton, eLeonardo, eDjenne, eDesert;
		int eWorldBank, eCrusade, eCrusader, eTechAppliedEconomics, eTechFundamentalism;
		std::set<int> setCathedrals, setMissionaries;
		int eReligionOption, eLeadershipOption, eTaxOption, eEconomyOption, eMilitaryOption;
		int eStateReligion, eMonarchy, eTribute, eFortification, eFolklore, eImperium, eCorporate, eBarter;
		std::set<int> setImperiumClasses, setCorporateClasses, setTributeClasses;
		int eObeliskClass, eCastleClass, eMarketClass;
		RoMRules() : bInit(false) {}
	};
	RoMRules g_rom;

	int infoType(const char* sz) { return GC.getInfoTypeForString(sz, true); }

	RoMRules& rules()
	{
		RoMRules& r = g_rom;
		if (r.bInit) return r;
		r.bInit = true;
		for (int i = 0; g_aszRoMUpgradePairs[i][0] != NULL; ++i)
		{
			const int eUpgrade = infoType(g_aszRoMUpgradePairs[i][0]);
			const int eReplaced = infoType(g_aszRoMUpgradePairs[i][1]);
			if (eUpgrade < 0 || eReplaced < 0) continue;
			r.aUpgradePairs.push_back(std::make_pair(eUpgrade, eReplaced));
			std::vector<int>& v = r.mSupersededBy[eReplaced];
			if (std::find(v.begin(), v.end(), eUpgrade) == v.end()) v.push_back(eUpgrade);
		}
		for (int i = 0; g_aszRoMBuildingCivic[i][0] != NULL; ++i)
		{
			const int eBuilding = infoType(g_aszRoMBuildingCivic[i][0]);
			if (eBuilding >= 0) r.mBuildingCivic[eBuilding] = infoType(g_aszRoMBuildingCivic[i][1]);
		}
		r.eObservatory = infoType("BUILDING_OBSERVATORY");
		r.eCopernicus = infoType("BUILDING_COPERNICUS_OBSERVATORY");
		r.eNewton = infoType("BUILDING_NEWTONS_UNIVERSITY");
		r.eLeonardo = infoType("BUILDING_LEONARDO");
		r.eDjenne = infoType("BUILDING_DJENNE");
		r.eDesert = infoType("TERRAIN_DESERT");
		r.eWorldBank = infoType("BUILDING_WORLD_BANK");
		r.eCrusade = infoType("BUILDING_CRUSADE");
		r.eCrusader = infoType("UNIT_CRUSADER");
		r.eTechAppliedEconomics = infoType("TECH_APPLIED_ECONOMICS");
		r.eTechFundamentalism = infoType("TECH_FUNDAMENTALISM");
		static const char* aszCathedrals[] = { "JEWISH", "CHRISTIAN", "ISLAMIC", "HINDU", "BUDDHIST", "CONFUCIAN", "TAOIST",
			"HELLENIC", "ZOROASTRIAN", "EGYPT_MYTH", "MESOAMERICAN" };
		for (int i = 0; i < 11; ++i) r.setCathedrals.insert(infoType(CvString::format("BUILDING_%s_CATHEDRAL", aszCathedrals[i]).c_str()));
		static const char* aszMissionaries[] = { "JEWISH", "CHRISTIAN", "HINDU", "BUDDHIST", "CONFUCIAN", "TAOIST", "ISLAMIC",
			"HELLENIC", "ZOROASTRIAN", "EGYPT_MYTH", "NAGUALISM" };
		for (int i = 0; i < 11; ++i) r.setMissionaries.insert(infoType(CvString::format("UNIT_%s_MISSIONARY", aszMissionaries[i]).c_str()));
		r.setCathedrals.erase(-1);
		r.setMissionaries.erase(-1);
		r.eReligionOption = infoType("CIVICOPTION_RELIGION");
		r.eLeadershipOption = infoType("CIVICOPTION_LEADERSHIP");
		r.eTaxOption = infoType("CIVICOPTION_TAXATION");
		r.eEconomyOption = infoType("CIVICOPTION_ECONOMY");
		r.eMilitaryOption = infoType("CIVICOPTION_MILITARY");
		r.eStateReligion = infoType("CIVIC_STATE_RELIGION");
		r.eMonarchy = infoType("CIVIC_HEREDITARY_RULE");
		r.eTribute = infoType("CIVIC_TRIBUTE");
		r.eFortification = infoType("CIVIC_FORTIFICATION");
		r.eFolklore = infoType("CIVIC_FOLKLORE");
		r.eImperium = infoType("CIVIC_IMPERIUM");
		r.eCorporate = infoType("CIVIC_CORPORATE");
		r.eBarter = infoType("CIVIC_BARTER");
		r.setImperiumClasses.insert(infoType("BUILDINGCLASS_PUBLIC_TRANSPORTATION"));
		r.setImperiumClasses.insert(infoType("BUILDINGCLASS_PERSONAL_RAPID_TRAIN"));
		static const char* aszCorporate[] = { "SID_SUSHI_RESTAURANT", "CEREAL_MILLS_FACTORY", "STANDARD_ETHANOL_DISTILLERY",
			"CREATIVE_CONSTRUCTIONS_OFFICE", "MINING_INC_SURVEY_OFFICE", "ALUMINUM_CO_R_AND_D", "CIVILIZED_JEWELERS_STORE" };
		for (int i = 0; i < 7; ++i) r.setCorporateClasses.insert(infoType(CvString::format("BUILDINGCLASS_%s", aszCorporate[i]).c_str()));
		r.setTributeClasses.insert(infoType("BUILDINGCLASS_BARRACKS"));
		r.setTributeClasses.insert(infoType("BUILDINGCLASS_GARRISON"));
		r.setImperiumClasses.erase(-1);
		r.setCorporateClasses.erase(-1);
		r.setTributeClasses.erase(-1);
		r.eObeliskClass = infoType("BUILDINGCLASS_OBELISK");
		r.eCastleClass = infoType("BUILDINGCLASS_CASTLE");
		r.eMarketClass = infoType("BUILDINGCLASS_MARKET");
		return r;
	}

	int civicIn(const CvPlayer& kPlayer, int eOption)
	{
		return eOption >= 0 ? (int)kPlayer.getCivics((CivicOptionTypes)eOption) : -1;
	}

	// RoMGameUtils._city_owned_radius_plots: the city's own radius, plots of its team.
	template <class Pred> bool anyOwnedRadiusPlot(const CvCity& kCity, Pred pred)
	{
		for (int i = 0; i < NUM_CITY_PLOTS; ++i)
		{
			CvPlot* pPlot = kCity.getCityIndexPlot(i);
			if (pPlot != NULL && pPlot->getTeam() == kCity.getTeam() && pred(*pPlot)) return true;
		}
		return false;
	}
	struct PeakOrHill { bool operator()(const CvPlot& p) const { return p.isPeak() || p.isHills(); } };
	struct IsTerrain { int eTerrain; explicit IsTerrain(int eType) : eTerrain(eType) {} bool operator()(const CvPlot& p) const { return eTerrain >= 0 && p.getTerrainType() == eTerrain; } };

	bool notObsolete(const CvPlayer& kPlayer, int eBuilding)
	{
		const int eTech = GC.getBuildingInfo((BuildingTypes)eBuilding).getObsoleteTech();
		return eTech == NO_TECH || !GET_TEAM(kPlayer.getTeam()).isHasTech((TechTypes)eTech);
	}
}

extern "C" __declspec(dllexport) int HH_pyCannotConstruct(void* pCityV, int eBuilding)
{
	const CvCity* pCity = (const CvCity*)pCityV;
	if (pCity == NULL || eBuilding < 0) return 0;
	RoMRules& r = rules();
	std::map<int, std::vector<int> >::const_iterator it = r.mSupersededBy.find(eBuilding);
	if (it != r.mSupersededBy.end())
	{
		for (size_t i = 0; i < it->second.size(); ++i)
		{
			if (pCity->getNumRealBuilding((BuildingTypes)it->second[i]) > 0) return 1;
		}
	}
	if (eBuilding == r.eObservatory) return anyOwnedRadiusPlot(*pCity, PeakOrHill()) ? 0 : 1;
	if (eBuilding == r.eCopernicus)
	{
		if ((r.eNewton >= 0 && pCity->getNumRealBuilding((BuildingTypes)r.eNewton) > 0)
			|| (r.eLeonardo >= 0 && pCity->getNumRealBuilding((BuildingTypes)r.eLeonardo) > 0)) return 1;
		return anyOwnedRadiusPlot(*pCity, PeakOrHill()) ? 0 : 1;
	}
	if (eBuilding == r.eDjenne) return anyOwnedRadiusPlot(*pCity, IsTerrain(r.eDesert)) ? 0 : 1;
	std::map<int, int>::const_iterator itCivic = r.mBuildingCivic.find(eBuilding);
	if (itCivic != r.mBuildingCivic.end() && !GET_PLAYER(pCity->getOwnerINLINE()).isCivic((CivicTypes)itCivic->second)) return 1;
	return 0;
}

extern "C" __declspec(dllexport) int HH_pyBuildingCostMod(int ePlayer, int eBuilding)
{
	if (ePlayer < 0 || eBuilding < 0) return -1;
	RoMRules& r = rules();
	const CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)ePlayer);
	if (r.setCathedrals.count(eBuilding) && r.eDjenne >= 0)
	{
		const BuildingClassTypes eDjenneClass = (BuildingClassTypes)GC.getBuildingInfo((BuildingTypes)r.eDjenne).getBuildingClassType();
		if (kPlayer.getBuildingClassCount(eDjenneClass) > 0 && notObsolete(kPlayer, r.eDjenne)) return 50;
	}
	const int eClass = GC.getBuildingInfo((BuildingTypes)eBuilding).getBuildingClassType();
	const int eLeadership = civicIn(kPlayer, r.eLeadershipOption);
	const int eEconomy = civicIn(kPlayer, r.eEconomyOption);
	if (civicIn(kPlayer, r.eReligionOption) == r.eFolklore && eClass == r.eObeliskClass) return 50;
	if (eLeadership == r.eImperium && r.setImperiumClasses.count(eClass)) return 75;
	if (eEconomy == r.eCorporate && r.setCorporateClasses.count(eClass)) return 75;
	if (civicIn(kPlayer, r.eTaxOption) == r.eTribute && r.setTributeClasses.count(eClass)) return 75;
	if (eClass == r.eCastleClass)
	{
		const bool bMonarchy = eLeadership == r.eMonarchy;
		const bool bFortification = civicIn(kPlayer, r.eMilitaryOption) == r.eFortification;
		if (bMonarchy && bFortification) return 50;
		if (bMonarchy || bFortification) return 75;
	}
	if (eEconomy == r.eBarter && eClass == r.eMarketClass) return 75;
	return -1;
}

extern "C" __declspec(dllexport) int HH_pyUnitCostMod(int ePlayer, int eUnit)
{
	if (ePlayer < 0 || eUnit < 0) return -1;
	RoMRules& r = rules();
	if (r.setMissionaries.count(eUnit) && civicIn(GET_PLAYER((PlayerTypes)ePlayer), r.eReligionOption) == r.eStateReligion) return 75;
	return -1;
}

// Called from CvEventReporter::buildingBuilt in harness builds (build_dll.sh).
void HH_buildingBuilt(CvCity* pCity, BuildingTypes eBuilding)
{
	if (pCity == NULL || eBuilding == NO_BUILDING) return;
	RoMRules& r = rules();
	CvPlayer& kOwner = GET_PLAYER(pCity->getOwnerINLINE());
	if (eBuilding == r.eDjenne)
	{
		// +2 commerce on the owner's desert plots in the 5x5 square that are in one of its city radii.
		for (int iDX = -2; iDX <= 2; ++iDX)
		{
			for (int iDY = -2; iDY <= 2; ++iDY)
			{
				CvPlot* pPlot = plotXY(pCity->getX_INLINE(), pCity->getY_INLINE(), iDX, iDY);
				if (pPlot != NULL && pPlot->isPlayerCityRadius(kOwner.getID()) && pPlot->getTeam() == kOwner.getTeam()
					&& r.eDesert >= 0 && pPlot->getTerrainType() == r.eDesert)
				{
					GC.getGameINLINE().setPlotExtraYield(pPlot->getX_INLINE(), pPlot->getY_INLINE(), YIELD_COMMERCE, 2);
				}
			}
		}
	}
	if (eBuilding == r.eWorldBank) kOwner.changeGold(kOwner.getGold() / 2);
	for (size_t i = 0; i < r.aUpgradePairs.size(); ++i)
	{
		if (r.aUpgradePairs[i].first == eBuilding) pCity->setNumRealBuilding((BuildingTypes)r.aUpgradePairs[i].second, 0);
	}
	if (eBuilding == r.eCrusade && r.eCrusader >= 0)
	{
		kOwner.initUnit((UnitTypes)r.eCrusader, pCity->getX_INLINE(), pCity->getY_INLINE(), UNITAI_ATTACK_CITY, NO_DIRECTION);
	}
}

// Called from CvEventReporter::beginPlayerTurn in harness builds (build_dll.sh).
void HH_beginPlayerTurn(int iGameTurn, PlayerTypes ePlayer)
{
	if (ePlayer == NO_PLAYER) return;
	RoMRules& r = rules();
	CvPlayer& kPlayer = GET_PLAYER(ePlayer);
	const CvTeam& kTeam = GET_TEAM(kPlayer.getTeam());
	int iLoop;
	if (r.eWorldBank >= 0 && r.eTechAppliedEconomics >= 0 && kTeam.isHasTech((TechTypes)r.eTechAppliedEconomics) && notObsolete(kPlayer, r.eWorldBank))
	{
		for (CvCity* pCity = kPlayer.firstCity(&iLoop); pCity != NULL; pCity = kPlayer.nextCity(&iLoop))
		{
			if (pCity->getNumActiveBuilding((BuildingTypes)r.eWorldBank) > 0) kPlayer.changeGold(kPlayer.getGold() / 100);
		}
	}
	if (r.eCrusade >= 0 && r.eCrusader >= 0 && r.eTechFundamentalism >= 0 && kTeam.isHasTech((TechTypes)r.eTechFundamentalism) && notObsolete(kPlayer, r.eCrusade))
	{
		const int iEnd = GC.getGameINLINE().getEstimateEndTurn();
		const int iInterval = iEnd >= 1800 ? 16 : iEnd >= 1400 ? 14 : iEnd >= 1000 ? 12 : iEnd >= 700 ? 8 : iEnd >= 500 ? 6 : 4;
		if (iGameTurn % iInterval == 0)
		{
			for (CvCity* pCity = kPlayer.firstCity(&iLoop); pCity != NULL; pCity = kPlayer.nextCity(&iLoop))
			{
				if (pCity->getNumActiveBuilding((BuildingTypes)r.eCrusade) > 0)
				{
					kPlayer.initUnit((UnitTypes)r.eCrusader, pCity->getX_INLINE(), pCity->getY_INLINE(), UNITAI_ATTACK_CITY, NO_DIRECTION);
				}
			}
		}
	}
}
