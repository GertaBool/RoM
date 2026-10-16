// Harness-only: lets the telemetry and diagnostics observe the AI without
// changing the game. Many AI getters fill a cache on first use each turn
// (attitudes, close-borders attitude, strategy and victory hashes, upgrade
// costs, empire averages, city closeness, floating defenders and yield ranks)
// and one rolls
// the synchronized random generator (AI_getStrategyRand). Called at the turn
// boundary by the harness, they would compute those values earlier than the
// game does and so change later decisions. build_dll.sh declares HarnessPeek a
// friend of CvPlayerAI, CvCityAI and CvCity in its copy of the source; a
// HarnessPeekGuard saves the caches and the random seeds and puts them back
// when it goes out of scope.
#pragma once
#ifndef HARNESS_PEEK_H
#define HARNESS_PEEK_H

#include "CvPlayerAI.h"
#include "CvCityAI.h"
#include "CvGameAI.h"
#include <vector>

struct HarnessPeek
{
	struct PlayerCaches
	{
		int iStrategyHash, iStrategyHashCacheTurn, iStrategyRand, iVictoryHash, iVictoryHashCacheTurn;
		int iUpgradeTurn, iUpgradeExpThreshold, iUpgradeGold, iAveragesTurn, iAverageGreatPeople;
		std::vector<int> aiAttitude, aiCloseBorders, aiAverages;
	};
	static void save(const CvPlayerAI& k, PlayerCaches& c)
	{
		c.iStrategyHash = k.m_iStrategyHash; c.iStrategyHashCacheTurn = k.m_iStrategyHashCacheTurn;
		c.iStrategyRand = k.m_iStrategyRand;
		c.iVictoryHash = k.m_iVictoryStrategyHash; c.iVictoryHashCacheTurn = k.m_iVictoryStrategyHashCacheTurn;
		c.aiAttitude.assign(k.m_aiAttitudeCache, k.m_aiAttitudeCache + MAX_PLAYERS);
		c.aiCloseBorders.assign(k.m_aiCloseBordersAttitudeCache, k.m_aiCloseBordersAttitudeCache + MAX_PLAYERS);
		c.iUpgradeTurn = k.m_iUpgradeUnitsCacheTurn; c.iUpgradeExpThreshold = k.m_iUpgradeUnitsCachedExpThreshold;
		c.iUpgradeGold = k.m_iUpgradeUnitsCachedGold;
		c.iAveragesTurn = k.m_iAveragesCacheTurn; c.iAverageGreatPeople = k.m_iAverageGreatPeopleMultiplier;
		c.aiAverages.assign(k.m_aiAverageYieldMultiplier, k.m_aiAverageYieldMultiplier + NUM_YIELD_TYPES);
		c.aiAverages.insert(c.aiAverages.end(), k.m_aiAverageCommerceMultiplier, k.m_aiAverageCommerceMultiplier + NUM_COMMERCE_TYPES);
		c.aiAverages.insert(c.aiAverages.end(), k.m_aiAverageCommerceExchange, k.m_aiAverageCommerceExchange + NUM_COMMERCE_TYPES);
	}
	static void restore(const CvPlayerAI& k, const PlayerCaches& c)
	{
		k.m_iStrategyHash = c.iStrategyHash; k.m_iStrategyHashCacheTurn = c.iStrategyHashCacheTurn;
		k.m_iStrategyRand = c.iStrategyRand;
		k.m_iVictoryStrategyHash = c.iVictoryHash; k.m_iVictoryStrategyHashCacheTurn = c.iVictoryHashCacheTurn;
		std::copy(c.aiAttitude.begin(), c.aiAttitude.end(), k.m_aiAttitudeCache);
		std::copy(c.aiCloseBorders.begin(), c.aiCloseBorders.end(), k.m_aiCloseBordersAttitudeCache);
		k.m_iUpgradeUnitsCacheTurn = c.iUpgradeTurn; k.m_iUpgradeUnitsCachedExpThreshold = c.iUpgradeExpThreshold;
		k.m_iUpgradeUnitsCachedGold = c.iUpgradeGold;
		k.m_iAveragesCacheTurn = c.iAveragesTurn; k.m_iAverageGreatPeopleMultiplier = c.iAverageGreatPeople;
		std::copy(c.aiAverages.begin(), c.aiAverages.begin() + NUM_YIELD_TYPES, k.m_aiAverageYieldMultiplier);
		std::copy(c.aiAverages.begin() + NUM_YIELD_TYPES, c.aiAverages.begin() + NUM_YIELD_TYPES + NUM_COMMERCE_TYPES, k.m_aiAverageCommerceMultiplier);
		std::copy(c.aiAverages.begin() + NUM_YIELD_TYPES + NUM_COMMERCE_TYPES, c.aiAverages.end(), k.m_aiAverageCommerceExchange);
	}
	// Per-turn city caches: player closeness, floating defenders, yield ranks.
	struct CityCaches
	{
		const CvCityAI* pCity;
		int iClosenessTurn, iClosenessDistance, iFloatingDefenders, iFloatingDefendersTurn, iPopulationRank;
		bool bPopulationRankValid;
		std::vector<int> aiCloseness, aiRanks;
		std::vector<bool> abRanksValid;
	};
	static void save(const CvCityAI& c, CityCaches& k)
	{
		k.pCity = &c;
		k.iClosenessTurn = c.m_iCachePlayerClosenessTurn; k.iClosenessDistance = c.m_iCachePlayerClosenessDistance;
		k.aiCloseness.assign(c.m_aiPlayerCloseness, c.m_aiPlayerCloseness + MAX_PLAYERS);
		k.iFloatingDefenders = c.m_iNeededFloatingDefenders; k.iFloatingDefendersTurn = c.m_iNeededFloatingDefendersCacheTurn;
		k.iPopulationRank = c.m_iPopulationRank; k.bPopulationRankValid = c.m_bPopulationRankValid;
		k.aiRanks.clear(); k.abRanksValid.clear();
		for (int i = 0; i < NUM_YIELD_TYPES; ++i)
		{
			k.aiRanks.push_back(c.m_aiBaseYieldRank[i]); k.abRanksValid.push_back(c.m_abBaseYieldRankValid[i]);
			k.aiRanks.push_back(c.m_aiYieldRank[i]); k.abRanksValid.push_back(c.m_abYieldRankValid[i]);
		}
		for (int i = 0; i < NUM_COMMERCE_TYPES; ++i) { k.aiRanks.push_back(c.m_aiCommerceRank[i]); k.abRanksValid.push_back(c.m_abCommerceRankValid[i]); }
	}
	static void restore(const CityCaches& k)
	{
		CvCityAI& c = const_cast<CvCityAI&>(*k.pCity);
		c.m_iCachePlayerClosenessTurn = k.iClosenessTurn; c.m_iCachePlayerClosenessDistance = k.iClosenessDistance;
		std::copy(k.aiCloseness.begin(), k.aiCloseness.end(), c.m_aiPlayerCloseness);
		c.m_iNeededFloatingDefenders = k.iFloatingDefenders; c.m_iNeededFloatingDefendersCacheTurn = k.iFloatingDefendersTurn;
		c.m_iPopulationRank = k.iPopulationRank; c.m_bPopulationRankValid = k.bPopulationRankValid;
		size_t j = 0;
		for (int i = 0; i < NUM_YIELD_TYPES; ++i)
		{
			c.m_aiBaseYieldRank[i] = k.aiRanks[j]; c.m_abBaseYieldRankValid[i] = k.abRanksValid[j]; ++j;
			c.m_aiYieldRank[i] = k.aiRanks[j]; c.m_abYieldRankValid[i] = k.abRanksValid[j]; ++j;
		}
		for (int i = 0; i < NUM_COMMERCE_TYPES; ++i) { c.m_aiCommerceRank[i] = k.aiRanks[j]; c.m_abCommerceRankValid[i] = k.abRanksValid[j]; ++j; }
	}
	// The cached hashes as the AI last computed them (no refresh).
	static int strategyHash(const CvPlayerAI& k) { return k.m_iStrategyHash; }
	static int victoryHash(const CvPlayerAI& k) { return k.m_iVictoryStrategyHash; }
};

class HarnessPeekGuard
{
public:
	HarnessPeekGuard() : m_aCaches(MAX_PLAYERS)
	{
		for (int i = 0; i < MAX_PLAYERS; ++i)
		{
			const CvPlayerAI& k = GET_PLAYER((PlayerTypes)i);
			HarnessPeek::save(k, m_aCaches[i]);
			int iLoop;
			for (CvCity* pCity = k.firstCity(&iLoop); pCity != NULL; pCity = k.nextCity(&iLoop))
			{
				m_aCities.push_back(HarnessPeek::CityCaches());
				HarnessPeek::save(*static_cast<const CvCityAI*>(pCity), m_aCities.back());
			}
		}
		m_ulSorenSeed = GC.getGameINLINE().getSorenRand().getSeed();
		m_ulMapSeed = GC.getGameINLINE().getMapRand().getSeed();
	}
	~HarnessPeekGuard()
	{
		for (int i = 0; i < MAX_PLAYERS; ++i) HarnessPeek::restore(GET_PLAYER((PlayerTypes)i), m_aCaches[i]);
		for (size_t i = 0; i < m_aCities.size(); ++i) HarnessPeek::restore(m_aCities[i]);
		GC.getGameINLINE().getSorenRand().reseed(m_ulSorenSeed);
		GC.getGameINLINE().getMapRand().reseed(m_ulMapSeed);
	}
private:
	std::vector<HarnessPeek::PlayerCaches> m_aCaches;
	std::vector<HarnessPeek::CityCaches> m_aCities;   // cities are not created or destroyed while observed
	unsigned long m_ulSorenSeed, m_ulMapSeed;
};

#endif
