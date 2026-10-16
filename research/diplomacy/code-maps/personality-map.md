# Leader personality map: how CvLeaderHeadInfo shapes the AI (Rise of Mankind DLL)

Baseline: GitLab `main` 93ae873 (tree of commit 7f72bd4, "Upkeep traps ...", i.e. including patch 0013).
All file:line references were checked against `git show 7f72bd4:Assets/CvGameCoreDLL/<file>`
Patch 0013 shifted CvPlayerAI.cpp by +41 lines
after line ~13040 and by +71 after ~19870; CvCityAI.cpp and CvTeamAI.cpp are unchanged.
Leader statistics: [../data/leader-stats.txt](../data/leader-stats.txt) and [../data/leaders.json](../data/leaders.json) (82 non-barbarian leaders).

Abbreviations: P = CvPlayerAI.cpp, T = CvTeamAI.cpp, C = CvCityAI.cpp, U = CvUnitAI.cpp,
PL = CvPlayer.cpp, H = CvPlayerAI.h, AD = AI_Defines.h, MWR = iMaxWarRand,
BUP = iBuildUnitProb, WCR = iWonderConstructRand, R = AI_getStrategyRand().

Random-number conventions used in all formulas below:
- rand(N) = CvGame::getSorenRandNum(N) (CvGame.cpp:8002) -> CvRandom::get (CvRandom.cpp:53-73):
  uniform on 0..N-1, argument truncated to unsigned short, and rand(0) returns 0 (no assert).
  "rand(X) == 0" therefore fires with p = 1/X per call, and always when X <= 1.
- "per turn" means once per AI turn for each eligible pair; none of these rolls is scaled by game
  speed (see 2.5 and R5).
- R = AI_getStrategyRand() (P:21054-21062) is drawn ONCE per player (1..100000) and never re-rolled;
  every victory inclination and several strategy flags are fixed functions of it.

----------------------------------------------------------------------------------------------

## 0. Executive summary

1. Every AI getter of CvLeaderHeadInfo (CvInfos.h:4196-4440) has at least one live reader; no field
   is loaded-and-ignored. `getLoveOfPeace` does not exist in this DLL (closest: iBasePeaceWeight).
   Two reads are dead code (P:8732, P:8734, inside a /* */ block); six helper reads (four functions)
   are display-only. 44 fields are identical for all 82 leaders (study/extra.txt) and act as global
   constants.
2. Personality enters decisions mainly as (a) per-turn dice (war, peace, contact, memory decay,
   unit-vs-building, wonder windows), (b) fixed additive/multiplicative biases (raze, flavors,
   favourite civic/religion, unitAI weights) and (c) one-off dice fixed for the whole game (victory
   inclinations via R, DAGGER via R).
3. The clearest handicaps (section 2): attack-odds optimism of base+rand+rand (+agenda) percentage
   points added to perceived combat odds every turn (up to +20, +27 with the conquest agenda); flat
   raze probability up to 75% without any city-value term; WCR=0 leaders that effectively never
   start a wonder; a fixed BUP-derived unit-upkeep ceiling; war and peace hazards that are per-turn,
   opportunity-blind and not scaled by game speed; victory stage 1/2 decided by personality + R with
   no feasibility test, which then locks the agenda (CULTURE2 = 1100).
4. The agenda system (P:4533-4842) never reads CvLeaderHeadInfo. It is situational (war plan, enemy
   power, finance, sites, coast, tech gap, bad start, governor and general feedback), but
   personality leaks in through three flags it consumes: AI_STRATEGY_DAGGER (MWR + FLAVOR_MILITARY +
   R), AI_VICTORY_CULTURE1/2 (iCultureVictoryWeight + R) and hasWarPlan (war dice), plus BUP which
   is the base the military budget is added to.
5. Verified defects (section 5): strategy/victory bit confusion at P:7746; async RNG in a
   synchronous path at P:16904; NoGiveHelp/DemandTribute thresholds read from the TARGET's
   personality (P:17695, P:17859); mixed getLeaderType()/getPersonalityType() (P:5984, P:13869,
   P:16642, P:24652); vacuous surrender test for MWR < 100 (T:2855); never-produced DIPLOMACY2/4
   levels.

----------------------------------------------------------------------------------------------

## 1. Getter-by-getter map (who reads it, what it decides, how strongly)

### 1.1 War, peace, combat

getMaxWarRand (team average T:4107-4132)
- T:2870-2950 AI_getWarRands: TotalWarRand = avgMWR; x4 if any member CULTURE4, else x3 SPACE4, else
  x2 CULTURE3; then *(2+members)/(2+members+vassals); /4 under AI_STRATEGY_FINAL_WAR (T:2942).
- T:4965 total-war dice inside AI_doWar: fires if rand(TotalWarRand) <= TotalThr. TotalThr
  (T:2953-3018) = avg(max(0, unitCost%-7)/2) * (3 if aggressive/DAGGER/CONQ4/DOM4 else 2), x3 with
  DOMINATION3 or x2 with CONQUEST2, then /3, +1 if aggressive. In peacetime with unit cost <= 9% of
  expenses TotalThr = 0, so p = 1/MWR per turn: 2.0% (MWR 50: Alexander, Boudica, Genghis,
  Montezuma, Ragnar, Shaka, Afonso, Basil, Ivan) down to 0.25% (MWR 400: Gandhi, Mansa Musa,
  Menelik). The dice are only rolled when the team has no war plan or enemy power < 45% (T:4857) and
  after the handicap roll AIDeclareWarProb (T:4944).
- T:1435 AI_endWarVal: in financial trouble, DAGGER or MWR < 100 lowers peace value to 70% *
  5*their/(ours+4*their).
- T:1583 AI_minorKeepWarVal: rand(MWR/100) == 0, i.e. always true for MWR < 100.
- T:2855, T:2861 AI_acceptSurrender: keep conquering if valuable+threatened cities >= MWR/100;
  refuse if the surrendering team has fewer than ourCities/4 - MWR/100 cities (see D6).
- P:13021 AI_civicValue: iWarmongerPercent = 25000/max(100, 100+MWR) (166 at MWR 50, 125 at 100, 83
  at 200, 50 at 400); multiplies free-experience civic value (P:13062), military production modifier
  value (P:13070, /300 at war, /500 in peace) and UpgradeAnywhere (P:13156).
- P:21557 AI_getStrategyHash (DAGGER): +12000/max(100, 50+MWR), then *(R%11)/10.
- Display only: CvDLLWidgetData.cpp:3988-4046, CvGameTextMgr.cpp:4256.

getMaxWarNearbyPowerRatio (T:4137-4162)
- T:4994 total-war target filter, passes 0-1: theirDefPower*2/3 < OurPower' * ratio/100, with
  OurPower' = getPower(true) * (100 - enemyPower%)/100, *4/3 if aggressive and no war plan
  (T:4953-4962). Net: a target is admissible up to 1.5*ratio% of our power, i.e. 1.2x (ratio 80: De
  Gaulle, Elizabeth) to 1.95x (ratio 130: Isabella, Montezuma, Sitting Bull, Ivan, Marcus).
- T:4541 AI_doWar: war-preparation time shortened when enemyPower% < 0.8*ratio.
- T:1585 minor-civ war, T:1630-1636 barbarian-civ war value (x0.5 if their defence > 1.5*ratio% of
  ours, x2 if < ratio%), P:22692 floating defenders x2/3 in a MASSING area if enemyPower% <
  10+ratio.

getMaxWarDistantPowerRatio (T:4167-4192)
- T:4994 pass 2 (non-land targets): same test with this ratio. 0 for Sitting Bull and Marcus (never
  a distant total war), 100 for Isabella and Napoleon.

getMaxWarMinAdjacentLandPercent (T:4197-4222)
- T:5003 pass 0 only: adjacent land plots >= totalLand*pct/100 (0..4%).

getLimitedWarRand / getLimitedWarPowerRatio (T:4227-4282)
- T:5045 limited dice (evaluated only if the total dice failed): rand(LWR') <= LimitedThr,
  LimitedThr = +2 if aggressive and leader era < 3 (T:3018). p = 1/LWR in peace: 2.5% (40: Genghis,
  Montezuma, Napoleon, Ragnar, Afonso, Basil) .. 0.5% (200).
- T:5075 target filter theirDefPower < OurPower' * ratio/100 (80..130). T:1444 endWarVal as above.

getDogpileWarRand (T:4287-4312)
- T:5110 dogpile dice; target must already be at war and theirDef*1.5 < our + co-belligerents' power
  (T:5157). T:1453 endWarVal.

getMakePeaceRand (T:4317-4342)
- T:4748 gate for the whole AI-AI peace block: rand(MPR) == 0, then only chosen wars against
  non-human teams are examined (T:4756-4846: stalemate, long draw, lonely dogpile). 10 (Asoka,
  Catherine, De Gaulle, Elizabeth, Gandhi, Lincoln ...) = 10%/turn; 120 (Alexander, Sitting Bull,
  Marcus) = 0.8%/turn.

getNoWarAttitudeProb[attitude] (team average T:4347-4392, minus 30 if a member is CONQUEST4,
minus 20 if DOMINATION4)
- T:4990, T:5071, T:5133: a target is only considered if the no-war roll >= prob (total: rand(100)
  +10 aggressive +10 finance -20*GET_BETTER_UNITS share; limited: -10; dogpile: -20). FRIENDLY is
  100 for everybody; CAUTIOUS ranges 20..90, PLEASED 50..100.
- T:1593 minor war, T:5208 AI_performNoWarRolls (U:24272 poaching).
- P:8721 force-war vote: yes if prob < 30 or rand(100) > prob.
- P:21453 paranoia (ALERT1/2): +(100-prob)/2 per close rival with 4/3 of our defence.

getDeclareWarTradeRand: P:18504 AI_doDiplo; rand(DWTR scaled down when the current war is younger
  than 10 / 4 turns) == 0 -> look for an ally to hire. 40 for 80/82 leaders.

getDemandRebukedSneakProb: P:7284, called from PL:5190 (DIPLOEVENT_REJECTED_DEMAND): rand(100) <
  prob and our power > their defence -> WARPLAN_PREPARING_LIMITED. 0 (Asoka, Cyrus, Darius,
  Frederick, Gandhi, Hatshepsut ...) .. 100 (Alexander, Washington).
getDemandRebukedWarProb: P:7307 with GC.getASyncRand(); callers CyPlayer.cpp:2306 (Python diplomacy
  screen, async by design) and P:16904 (see D2).

getRefuseToTalkWarThreshold: P:7242 AI_isWillingToTalk: refuse for T turns (x2 if chosen war),
  shortened to T*(20+160*ours/theirs)% when losing badly. 5..12.

getBaseAttackOddsChange / getAttackOddsChangeRand: P:16207-16210 (AI_doMilitary, every turn): change
  = base + rand(AR) + rand(AR) + agenda term (AR = iAttackOddsChangeRand) (P:16193-16205: SURVIVE
  -10, POWER_SPIKE +4, CONQUEST +7). Added to perceived attack odds at U:934 (LFB path), U:1012
  (classic path) and U:24929 (LFBgetBetterAttacker). See 2.1.

getRazeCityProb: P:1770 (barbarian owner), P:1791 (small island, closeness 0), P:1810 (medium
  island, previous owner has >3 cities there), P:1876 (normal case). Decision P:1921: rand(100) <
  value. See 2.2.

getVassalPowerModifier: T:2159 AI_surrenderTrade: vassal power = power*(iPowerMultiplier +
  avgModifier)/100 (-20 Catherine/De Gaulle/Gandhi/Mansa/Kangxi .. +50 Alexander/Genghis/Sitting
  Bull).

getVassalRefuseAttitudeThreshold: T:2395 (deny vassal/capitulation if modified attitude <=
  threshold), P:9011 (tribute deal from master), P:8551 (force-peace vote "influence by secretary";
  a vassal threshold reused for an unrelated decision, S5).

### 1.2 Production, research, economy, religion

getBuildUnitProb
- C:10905 AI_buildUnitProb = BUP + 2*(production XP + free sea XP); /2 in financial trouble, else +
  min(15, militaryProductionModifier/4); x4/3 for rebels.
- C:894-944 adjustments in AI_chooseProduction: + (militaryBudget-200)/20 from the agenda
  (SURVIVE/CONQUEST +22, POWER_SPIKE +18, others -1..-4), +10 castellan governor, -5 agricultural/
  scholar governor, -15 in a safe small war, -25/-10 in a peaceful era-0 city lacking water trade/
  writing.
- Consumers: C:3288 main roll "rand(100) < BUP -> AI_chooseUnit()" when unit cost% < cap+5; C:2508
  cap iMaxUnitSpending = 3 (6 aggressive) + BUP/3 (+1 CONQ1, +3 CONQ3/DOM3, +7 CONQ4); C:1968 extra
  defenders when losing (odds = BUP, + |warSuccess|/3 when below -50, +10 in danger); C:2115/C:2143
  early attack stack (rand weight BUP/2, size 3+BUP/10); C:2207 missionary roll (100-BUP)/3;
  C:2719/C:2924 invader chance BUP+10; C:2996 pirates; C:1336 rebel offence.
- P:8211 nuke-ban vote threshold (+BUP, x WarmongerRespect); P:21248 OWABWNW nuclear strategy
  if (BUP + R%15) >= 43 (37 aggressive), so leaders with BUP <= 28 never adopt it in a normal
  game; P:23507 advanced start: military share (10 + BUP/3)% of points.
- Range 15 (Gandhi) .. 40 (Mehmed, Napoleon, Ragnar, Shaka, Ashur), 38 Augustus.

getWonderConstructRand
- C:2161 opportunistic wonder #1 (<= 3 cities): max build turns = rand(WCR)/5 + 7.
- C:2449 opportunistic wonder #2: max turns = rand(WCR)/5 + 8.
- C:3085-3125 wonder roll in top-production cities: WonderRand = (8 + rand(WCR)) * {35% early, 30%
  >=3 area cities, 25% otherwise} (*2/3 aggressive); WonderRoll = rand(100) (halved for rank 1); if
  roll < WonderRand: max turns = 20 + 2*(WonderRand-roll), halved at war.
- C:4074/C:4078 AI_bestBuildingThreshold: every world wonder gets +rand(WCR) (x2 if the area is
  alone) added to its value, for cities of production rank <= min(3,(cities+2)/3), before the
  *1000/(turns+3) normalisation (sync rand; ASync for the advisor path).
- 0 for Montezuma, Sitting Bull, Ivan; 50 for Alexander, Louis XIV, Ramesses; 40 for ten others.

getFlavorValue (via P:421 AI_getFlavorValue)
- P:6113-6120 tech value: affinity = 5*dot(leaderFlavor, techFlavor)/L1(leaderFlavor)
  (AIFlavorPolicy.h normalizedAffinity); value += affinity*20*35/100 (AI_TECH_FLAVOR_VALUE_PERCENT =
  35, GlobalDefinesAlt.xml:787). Over all leader x tech pairs: 0..700, mean 93 (stats).
- C:5814-5820 building value (non-human, pass > 0, value > 0): + affinity (0..100, mean 8.7).
- P:21111 FLAVOR_PRODUCTION >= 2 -> AI_STRATEGY_PRODUCTION (14 leaders) -> C:7319, C:8199 citizen
  weights +10 production / -10 commerce, permanently.
- P:21291-21293 missionary strategy score 2*GROWTH + 4*CULTURE + 6*RELIGION (threshold 100 with
  other terms). P:21560 DAGGER + 5*min(8, MILITARY).
- Flavors are no longer read by unit, civic or project valuation.

getUnitAIWeightModifier: C:3692 AI_bestUnit: aiUnitAIVal[ai] *= (100+mod)/100 (mod 0 or 100, a few
  15..60 for Augustus), applied to the deficit only (a positive need is doubled, no need cannot be
  created), followed by the agenda role price C:3700 and a rand(iMilitaryWeight) tiebreak.

getImprovementWeightModifier: C:7701 (AI_getImprovementValue) and C:11691 (AI_bestPlotBuild): value
  *= (200+mod)/200, i.e. +10% (20) or +15% (30). Mild and harmless.

getEspionageWeight: P:211 AI_setEspionageWeight(personality) -> P:2256 espionage commerce weight (x
  w/100), P:13567 civic value, P:21357 BIG_ESPIONAGE flag ((100-w)/10 term, S4). P:16642
  AI_doCommerce espionage slider target x w/100 uses getLeaderType() (D4).

getFavoriteCivic: P:13668 AI_civicValue x5/4 + 6*cities + 20 (state-religion civic only with a
  religion); P:5955 tech value +600 for every tech that enables it (even when inferior to the
  current civic); P:10558 AI_civicTrade DENIAL_FAVORITE_CIVIC; P:7976-7985 attitude; P:15188-15191
  counter; P:17544 civic pressure on humans; P:21295 missionary +20; PL:5232 accept-civic event.
getFavoriteReligion (all via getLeaderType()): P:5984 religion-founding tech: favourite gets
  1+rand(1200) extra, other religions' roll shrinks from 2400 to 1600; P:13869 AI_bestReligion x5/4;
  P:24652 AI_chooseReligion (PICK_RELIGION option): favourite if unfounded, else uniformly random.

### 1.3 Victory weights
getCultureVictoryWeight P:20298, getSpaceVictoryWeight P:20488, getConquestVictoryWeight P:20627,
getDominationVictoryWeight P:20714, getDiplomacyVictoryWeight P:20780. Only read in the stage
functions; formulas in section 4.

### 1.4 Attitude (AI_getAttitudeVal P:7379-7490, cached)
Sum of (personality-dependent terms marked *):
- * iBaseAttitude (P:7417), -1..+2.
- handicap attitude of the target.
- * AI-AI only: 4 - |PW_self - PW_other| (P:7431) where PW = iBasePeaceWeight + rand(3), drawn once
  at P:210; range -8..+4 (study: 15.7% of pairs <= -3, 26.3% >= +3), plus min(WarmongerRespect_self,
  WarmongerRespect_other) (P:7432, 0..2).
- team-size malus, +1 if both in bottom half of ranks.
- * rank: iWorseRank*diff/(N+1) or iBetterRank*(-diff)/(N+1) (P:7441/7445): up to -3 (Alexander,
  Montezuma, Stalin, Ivan, Nebuchadrezzar) for leaders ahead of us, up to +4 for leaders behind.
- * iLostWarAttitudeChange (P:7456, -1 for all).
- * close borders (P:7722-7758): change * (min(60, 3*stolen plots) + 40 if land target)/100, change
  -1..-5 (Augustus -5).
- * at war / at peace / same religion / different religion / bonus trade / open borders / defensive
  pact / share war / favourite civic (P:7773-7985): counter/divisor clipped to +-limit. Of these
  only SameReligionLimit (1..7), ShareWarLimit (2..6), FavoriteCivicLimit (1..6),
  DifferentReligionChange (-2..0), AtPeaceDivisor (50..70) vary between leaders.
- * memories (P:8010): count * MemoryAttitudePercent/100; decay P:15241-15243: each turn
  rand(MemoryDecayRand) == 0 removes one count (not speed-scaled).
- * colony (P:8019): FreedomAppreciation (10 for all).
- Display-only copies: AI_getFirstImpressionAttitude (P:7541/7552/7554),
  AI_getBetterRankDifferenceAttitude (P:7616), AI_getWorseRankDifferenceAttitude (P:7641),
  AI_getLostWarAttitude (P:7685): callers only in CvGameTextMgr.cpp:15346-15386.

### 1.5 Trade and diplomacy thresholds (attitude <= threshold -> DENIAL_ATTITUDE unless noted)
- TechRefuse T:1813; NoTechTradeThreshold T:4062 -> T:1826 (DENIAL_TECH_WHORE if the buyer received
  more techs than threshold recently); TechTradeKnownPercent T:4092 -> T:1859 (DENIAL_TECH_MONOPOLY
  if fewer than pct% of met teams know it, scaled by AI_getTechMonopolyValue).
- MapRefuse T:2014; OpenBordersRefuse T:3450; DefensivePactRefuse T:3500 (+ dead P:8732);
  PermanentAllianceRefuse T:3556; DeclareWarRefuse T:3353, P:8585, P:8701; DeclareWarThemRefuse
  T:3369 (deny if attitude to victim > threshold), P:8580.
- StrategicBonus P:10206, HappinessBonus P:10214, HealthBonus P:10222, StopTrading P:10468,
  StopTradingThem P:10484, AdoptCivic P:10572, ConvertReligion P:10646.
- DemandTribute P:17859 and NoGiveHelp P:17695: read from the TARGET player's personality (D3).
- MaxGoldTradePercent P:9633 (cap = pop*(metTurns+10)*pct/100), MaxGoldPerTurnTradePercent P:9665.
- ContactRand/ContactDelay: rand(ContactRand) == 0, then the timer is set to ContactDelay. Rands:
  peace P:972 (delays P:931, P:1175), alliance P:17394, religion pressure P:17514, civic pressure
  P:17556, join war P:17592, stop trading P:17653, give help P:17699, ask for help P:17768, demand
  tribute P:17863/17900/17933/17988, open borders P:18058, defensive pact P:18108, trade tech
  P:18163, trade bonus P:18341, trade map P:18451. Ask-for-help and trade-tech rands shrink when our
  tech score is < 90% of the best known (x max(1, pct-60)/30); trade tech is halved with SPACE1.
  Alexander has 1000 for PEACE_TREATY and 10000 for alliance/religion/civic pressure, and all delays
  = 10 (study).

### 1.6 Unread, dead and degenerate
- Unread getters: none. Non-AI getters (art, music script ids, hasTrait) are outside scope.
- Dead reads: P:8732 (getDefensivePactRefuseAttitudeThreshold) and P:8734 (getBasePeaceWeight) are
  inside the commented-out "defy force-war" block of AI_diploVote.
- Display-only reads: see 1.4; CvDLLWidgetData.cpp:3988-4046 and CvGameTextMgr.cpp:4256 (war ratio hover text).
- Constant for all 82 leaders (44 fields, study/extra.txt), e.g. iPeaceWeightRand 3,
  iFreedomAppreciation 10, iLostWarAttitudeChange -1, iAtWarAttitudeDivisor -5 / Limit 5,
  iAtPeaceAttitudeChangeLimit 1, Same/DifferentReligion divisors, BonusTrade/OpenBorders/DP limits,
  ShareWar change, FavoriteCivic change/divisor, NoWarProb FRIENDLY 100, ContactRand DEFENSIVE_PACT
  80, most memory decays. Near-constant: DemandTribute/NoGiveHelp threshold 2 (81/82),
  DeclareWarTradeRand 40 (80/82), MaxGoldPerTurnTradePercent 10 (79/82).
- Module leaders Basil, Ivan, Kangxi, Leonidas, Sejong lack NoWarProb ANNOYED (loads as 0, which 16
  core leaders also use, so harmless).

----------------------------------------------------------------------------------------------

## 2. Where personality makes the AI play worse (not merely differently)

### 2.1 Attack-odds optimism (P:16193-16210, U:934, U:1012, U:24929)
Perceived odds = true odds + base + rand(AR) + rand(AR) + agenda, re-rolled every turn
(AR = iAttackOddsChangeRand).
- All leaders are optimistic: base 0..6, AR 6..10, so E[bias] = base + (AR-1) = 7..13 points, max
  base + 2(AR-1) = 20 (Alexander, Napoleon, Ragnar, Mongkut, Jayavarman), +7 under the CONQUEST
  agenda = 27. A unit that requires 60% perceived odds attacks at a true 33-53%.
- The SURVIVE agenda subtracts 10, so the same leader swings by up to 37 points between agendas.
- The bias is not tied to anything that justifies risk (reinforcements, unit cost, war success,
  promotion value), and it is noise: the same stack may attack one turn and not the next.
Verdict: handicap for every leader, worst for the base-6 / rand-10 group.

### 2.2 Raze probability (P:1733-1930)
Normal branch (city on a continent where we already have cities):

```
value = (-closeness if close, else 40 + 5*(dist-9) [8 per tile for barbarian cities])
        + max(0, 70-15*pop) if in financial trouble, all scaled by trait upkeep modifiers
        + RazeCityProb - (50 with own-religion shrine | 10 with own religion)
raze if rand(100) < value
```

Holy/wonder cities, empires of <= 1 city (or < 5 cities and close) and DOMINATION3
primary-area cities are exempt.
- No term for population, buildings, resources, culture, or the -250 MEMORY_RAZED_CITY penalty with
  third parties. A 15-pop city adjacent to our core is razed with p = RazeProb - closeness.
- Extremes: Genghis 75; Brennus, Montezuma, Ragnar, Shaka, Abu Bakr, Ivan, Joan of Arc, Richelieu
  50; eight more at 25 (Isabella, Kublai, Mehmed, Stalin, Suryavarman, Tokugawa, Ashur,
  Nebuchadrezzar); 54 leaders at 0.
Verdict: for the 17 leaders >= 25 this destroys conquered value and is the textbook "flavour as handicap".

### 2.3 Wonder construction rand
- WCR = 0 (Montezuma, Sitting Bull, Ivan): window #1 is fixed at 7 turns, #2 at 8 turns (scaled by
  construct percent), the C:3085 roll succeeds with WonderRand = 8*{0.25..0.35} = 2 -> 2% (4% in the
  best city), and C:4074 adds nothing. In RoM, where many wonders are strategic (production,
  happiness, health, military), these leaders effectively skip all non-trivial wonders.
- WCR = 50 (Alexander, Louis XIV, Ramesses): window up to 16-17 turns, roll success about 10% on
  average and at most ~20% (about twice that in the rank-1 city), and +0..49 (0..98 if alone) of
  noise on every wonder's value in the top cities. The noise is independent of the wonder's
  usefulness, so a marginal wonder can outrank a needed building; because it is added before
  /(turns+3) it favours cheap marginal wonders.
Verdict: both extremes misallocate; the noise term should be a competition- and fit-driven bias.

### 2.4 Unit build probability and the BUP-derived upkeep ceiling
- C:3288: in peacetime each production decision builds "some unit" with p = BUP' while unit cost is
  below (3 + BUP'/3 + 5)% of expenses (C:2508, C:3284). BUP' = BUP +/- agenda/governor terms. Gandhi
  (15): cap 13%, roll 15%; Napoleon/Shaka/Ragnar (40): cap 21%, roll 40%.
- AI_bestUnit only fills positive deficits, but the ATTACK deficit grows with area population
  (C:3505: iMilitaryWeight/12 + ...), so a deficit almost always exists and the roll, not threat,
  decides how much army a peaceful empire keeps. Threat enters through separate danger/ALERT
  branches, not through this roll.
- P:21248: OWABWNW nuclear doctrine only for BUP + R%15 >= 43, so 36 of 82 leaders (BUP <= 28) never
  adopt it even when nukes are the decisive weapon.
Verdict: fixed army share instead of a threat-driven one; low-BUP leaders are under-armed, high-BUP
leaders over-pay upkeep in safe positions.

### 2.5 War and peace hazards are per-turn dice, opportunity-blind and speed-unscaled
- T:4965/5045/5110: p(start plan) = (thr+1)/rand per turn, thr mostly 0 in peace. Expected dice
  successes per game (study/extra.txt): most warlike 17.8 (Blitz) .. 248 (Snail); least 3.2 .. 44.8.
  Game length differs 14x between Blitz (215 turns) and Snail (3000), so the same leader starts up
  to 14x more war plans per era on slow speeds.
- The power filter is a personality ratio applied to a 2/3-discounted enemy defence (T:4992-4994):
  ratio 130 admits targets with 1.95x our power. The plan is then only converted to war if the
  shared area is OFFENSIVE and enemy power < 140% (T:4662), otherwise abandoned after ~20
  (speed-scaled) turns of build-up, i.e. production is wasted on preparations for wars that were
  never winnable.
- Peace: AI-AI peace checks are gated by rand(MPR) == 0 (T:4748) and only cover chosen wars;
  Alexander/Sitting Bull/Marcus check 0.8% of turns, so a stalemate persists ~125 turns on average
  before the "nothing happening" test is even evaluated.
- Target selection itself (AI_startWarVal) is situational; the problem is WHEN, not WHOM.

### 2.6 Victory inclinations are fixed dice without feasibility (details in section 4)
- Stage 1 is "weight + options + (R + k) % 100 >= 100", decided once (R never changes).
- CULTURE2 turns on purely by era (Medieval/Renaissance) and then forces the CULTURE agenda (score
  1100, P:4635) for as long as CULTURE2 holds (normally the rest of the game): culture commerce
  weight x2.75 (P:2310), no extra settler slots, BUP -4, DAGGER blocked (P:21552),
  NoNonStateReligionSpread civics valued /10 (P:13679), religious-victory push off (P:25283ff).
- Space: the Apollo tech is valued +2000 only with SPACE2 (P:5844), otherwise +100; SPACE3/4 need
  Apollo built. A runaway tech leader with low space weight under-values the space path.
- Cetshwayo has all five weights 0 (Cetshwayo_CIV4LeaderHeadInfos.xml:24-28): never inclined.

### 2.7 DAGGER is mostly personality plus R (P:21550-21686)
iDagger = (12000/max(100,50+MWR)) * (R%11)/10 + 5*min(8, MILITARY) + unit/situation terms;
threshold 100 (AD: AI_DAGGER_THRESHOLD). The personality part alone reaches 160 (Shaka, Ragnar,
Genghis), 145 (Montezuma, Ivan, Boudica) and at most 26 for Gandhi/Mansa/Menelik. The only
situational gates are era <= 2-3, no CULTURE2/MISSIONARY and "iCloseTargets > 0" (attitude-based).
There is no comparison of our early army with the neighbour's defence before committing.

### 2.8 Other personality-driven inefficiencies (milder)
- Peace-weight compatibility (P:7431): -8..+4 attitude fixed at turn 0 for every AI pair; together
  with WarmongerRespect it pre-decides alliances and dogpile targets independent of interests.
- TechTradeKnownPercent 0 (Mansa Musa, Menelik) sells monopoly techs to anyone; 100 (Tokugawa,
  Cetshwayo) refuses almost all trades (isolation). The monopoly guard should be about who the buyer
  is (score rival) rather than a constant.
- Favourite civic is triple-counted (P:13668 x1.25+6N+20, P:5955 +600 tech value even if worse,
  P:10558 refuse any civic in that slot by trade).
- Favourite religion beelining (P:5984) and AI_chooseReligion picking a random religion (P:24652)
  ignore religion-specific value.
- Memory decay (P:15241) and contact timers are per turn, so grudges last a fixed number of turns
  regardless of game speed.

----------------------------------------------------------------------------------------------

## 3. The agenda / budget system

### 3.1 What it is
- Enum H:17-30: SURVIVE, RECOVER, EXPAND_LAND, EXPAND_MARITIME, CONSOLIDATE, POWER_SPIKE, CONQUEST,
  SCIENCE, CULTURE. Budgets H:108-116: GROWTH, ECONOMY, MILITARY, EXPANSION, CULTURE (per mille).
- AI_updateAgenda (P:4533-4842), called from P:468 every turn, re-decides every
  AI_AGENDA_UPDATE_INTERVAL = 4 turns (GlobalDefinesAlt.xml:829) or immediately on emergency
  (strike, or at war with enemy power >= 140), bad-start change, or war-state change (P:4555-4565).
- Budget table P:4569-4580 (growth, economy, military, expansion, culture): survive
  100/150/650/50/50, recover 180/480/180/110/50, expand land 220/180/180/370/50, expand maritime
  180/260/180/330/50, consolidate 360/350/140/100/50, power spike 140/180/570/60/50, conquest
  100/170/650/40/40, science 180/520/160/90/50, culture 180/250/120/50/400.

### 3.2 How the agenda is chosen (all inputs from the one-turn snapshot P:4419-4490)
Scores P:4610-4637 (enemyPower is clamped to 25..400, P:4480):
- SURVIVE = 350*warPlan + 8*max(0, enemyPower-100) + 1200*strike
- RECOVER = 900*financialTrouble + 70*max(0, 10-goldRunway) + 600*strike
- EXPAND_LAND = 180*min(4,sites) + 180*(no settlers) + 220*(cities <= 3) - 700*fin - 300*warPlan
- EXPAND_MARITIME = 130*min(coastal,8) + 25*usefulForeignTradeCities + 400*capitalAreaAlone +
  180*(sites == 0) - 400*fin
- CONSOLIDATE = 200 + 30*min(cities,10) + 55*min(12, max(0, 5*cities-pop)) + 90*min(8, max(0,
  cities-workers)) + 120*fin
- POWER_SPIKE = (850 if GET_BETTER_UNITS else 100) + 250*warPlan
- CONQUEST = 850*warPlan + 500*DAGGER + 450*CRUSH + 3*max(0, 120-enemyPower) - 300*fin
- SCIENCE = 300 + 12*min(50, 100-techScore%) + (150, or -500 in financial trouble)
- CULTURE = 1100 if CULTURE2, 500 if CULTURE1, else 0
Then: bad-start bonuses (P:4641-4666), governor feedback via AIFeedbackPolicy::agendaDelta
(P:4671-4695, city-averaged, reputation-weighted), general doctrine from completed operations
(P:4703-4737, faded over 80 scaled turns), argmax with CONSOLIDATE as default (P:4739-4748),
hard overrides strike -> RECOVER, war with enemyPower >= 140 -> SURVIVE, bad start >= 40 -> land /
maritime / breakout (P:4753-4779), and hysteresis: keep the old agenda unless the new score beats it
by max(150, 12% of the old score) (P:4781-4791).

### 3.3 What the agenda changes
- Food yield weight 100 + (growth-180)/4, clamp 75..150% (P:2089-2093).
- Research (or gold when RECOVER/fin) weight 100 + (economy-250)/4, clamp 75..175%; culture weight
  100 + (culture-50)/2, clamp 75..275% (P:2298-2313).
- BUP + (military-200)/20 (C:898-902); settler slots + max(0,(expansion-100)/120) (C:990-996).
- Military role price per unitAI (P:3412-3459) applied in AI_bestUnit (C:3700), least-represented
  choice (C:9518) and AI_unitValue (P:11771-11774).
- Tech value AI_getTechAgendaValue (P:4970-5106, capped at AI_AGENDA_MAX_TECH_VALUE 1200).
- Attack odds -10/+4/+7 (P:16193-16210); gold target x1.5 RECOVER, x0.75 SCIENCE, x1.25 SURVIVE/
  CONQUEST (P:16252-16262).
- AIHierarchyPolicy::derive (AIHierarchyPolicy.h:51-77): naval priority, logistics, risk tolerance,
  expansion horizon, war posture; used by operations (P:15392-15819, P:16101-16104) and settling
  (U:10988, U:17059, U:18120).

### 3.4 Interaction with personality
- No CvLeaderHeadInfo getter is read in P:4419-4842 or P:4970-5106.
- Indirect channels: DAGGER (+500 to CONQUEST; MWR, FLAVOR_MILITARY, R), CRUSH (R%4 and DAGGER),
  hasWarPlan (+850 CONQUEST, +350 SURVIVE; produced by the personality war dice), CULTURE1/2 (+500/
  +1100; iCultureVictoryWeight and R), and BUP as the base of the military actuator.
- Space, conquest, domination and diplomacy inclinations have no agenda counterpart.

### 3.5 Does it respond to the situation?
Mostly yes (war, power, solvency, sites, coast, tech gap, bad start, feedback), with exceptions:
- CULTURE is a constant 1100 once CULTURE2 is on (era + personality dice), beating SCIENCE (max
  1050) and CONSOLIDATE in any peaceful state (only a war plan or a large coastal empire, S2,
  outscores it); the culture agenda then persists by hysteresis.
- CONQUEST carries a 285-point peacetime floor because enemyPower is clamped to 25 (S1).
- EXPAND_MARITIME grows linearly with coastal city count (S2).
- Expansion horizon shrinks as the expansion budget grows (S3).

----------------------------------------------------------------------------------------------

## 4. Victory strategies (AI_VICTORY_*, AD; P:20212-21050)

### 4.1 Mechanics
AI_getVictoryStrategyHash (P:20903-21050) is recomputed once per turn; AI_isDoVictoryStrategy
(P:20827) tests bits. Stages 3/4 are exclusive across types (bStartedOtherLevel3/4; diplomacy 3 is
skipped if another type is at 3).

Personality roll (stage >= 1) for each type: w + options + (R + k) % 100 >= 100, with
k = +10 culture (P:20323), +50 space (P:20497), +30 conquest (P:20631), +70 domination (P:20718),
+90 diplomacy (P:20789). ALWAYS_PEACE: +30 culture/space/diplomacy, conquest/domination off.
AGGRESSIVE_AI: -20 culture/space/diplomacy, +20 conquest/domination. Mean P(stage1): culture 28.6%,
space 23.4%, conquest 30.6%, domination 27.0%, diplomacy 27.2%; 9.8% of rolls give no inclination,
4% give three (stats). All five rolls use one number r = R%100, so they are perfectly correlated
offsets, not independent dice.

- Culture (P:20212-20367): personality roll skipped for humans; off for start era > 1 (P:20284), or
  a capital founded after turn 10 without 5 high-culture cities. Weight + 10*holy cities (if w > 20
  and >= 5 cities). Stage 2 at era >= 8/3 + R%2 = 2 or 3 (Medieval/Renaissance, P:20361); stage 3/4
  at era >= 8 - (2 + R%2) = 5 or 6 (Modern/Transhuman, P:20331) with enough high-culture cities or 3
  religions per city; stage 4 also directly when 5 cities are half-way to legendary (situational,
  any personality).
- Space (P:20369-20512): stage 3/4 from Apollo + tech position (situational); stage 1/2 from the
  roll, stage 2 at era >= 5 (Modern, P:20502).
- Conquest (P:20514-20649): stage 3/4 from power rank and others' war memories (situational); roll
  -> 1, -> 2 with GET_BETTER_UNITS, > 3 cities and 4*ours > 5*average.
- Domination (P:20651-20733): stage 3/4 from land/population progress (situational); roll -> 1, -> 2
  with > 3 cities and top-half rank.
- Diplomacy (P:20735-20825): roll -> 1; stage 3 if vote-eligible and inclined. Levels 2 and 4 are
  never returned (D5).

### 4.2 What the flags change (consumer counts outside display code)
CULTURE1 10 sites, CULTURE2 19, CULTURE3 22, CULTURE4 8; CONQUEST1 2, CONQUEST2 2, CONQUEST3 7,
CONQUEST4 6; DOMINATION1 0, DOMINATION2 1, DOMINATION3 8, DOMINATION4 6; SPACE1 2, SPACE2 1,
SPACE3 7, SPACE4 7; DIPLOMACY1 2, DIPLOMACY3 1, DIPLOMACY4 1 (dead).
Personality-level (1/2) effects:
- CULTURE1: religion-founding techs +500 (+1000 with no holy city) and no division by holy cities
  (P:6014-6024); CULTURE agenda 500. CULTURE2: CULTURE agenda 1100, culture building focus (C:3153),
  civic value /10 for NoNonStateReligionSpread (P:13679), dagger blocked (P:21552).
- SPACE1: tech-trade contact rand /2 (P:18171), building value (C:4279). SPACE2: Apollo tech +2000 (P:5844).
- CONQUEST1: unit spending cap +1 (C:2518), city-attack unit tech value (P:6911). CONQUEST2: total
  war threshold x2 (T:2984-3008) and start-war value (T:1296).
- DOMINATION2: settling-unit tech value +2000 vs +500 (P:7037). DOMINATION1: no consumer.
- DIPLOMACY1: vote-source building value x5 (C:5133), tech value (P:6490).

### 4.3 Assessment
Stage 1/2 are fixed at game start by personality plus one hidden number and are re-checked only
against era, city count and coarse power; they never react to "this victory is unreachable" or
"this victory is now easy". Stages 3/4 are situational and personality-free (good). The culture
chain is the only one that strongly drives the economy (through the agenda), and it is also the one
with the weakest feasibility check.

----------------------------------------------------------------------------------------------

## 5. Defects and suspicious logic

### 5.1 Verified defects
D1 P:7746 AI_getCloseBordersAttitude: `AI_isDoStrategy(AI_VICTORY_CONQUEST3)` tests bit 7 of the
   STRATEGY hash, which is AI_STRATEGY_FINAL_WAR (AD: both are 1 << 7). The intended 1.5x
   close-borders malus (cap 120%) fires under FINAL_WAR and never under conquest stage 3. Fix:
   AI_isDoVictoryStrategy(AI_VICTORY_CONQUEST3). Only occurrence of this bit mix-up.
D2 P:16904 AI_beginDiplomacy (do-not-bother path) calls AI_demandRebukedWar, which rolls
   GC.getASyncRand() (P:7307), and then executes handleDiploEvent(DIPLOEVENT_DEMAND_WAR) inside the
   synchronous AI turn (AI_doDiplo -> P:17086 etc.). The do-not-bother flag is synchronised game
   state (PL:5332, PL:12906), so in multiplayer each machine can roll differently -> war declared on
   some clients only (OOS). Single player: non-reproducible replays. Fix: use getSorenRandNum here.
D3 P:17695 (give help) and P:17859 (demand tribute) compare this AI's attitude against
   GC.getLeaderHeadInfo(GET_PLAYER(iI).getPersonalityType()), i.e. the human TARGET's leader. Should
   be getPersonalityType() of the AI. Low impact today (threshold 2 for 81/82 leaders).
D4 Personality source mixed: favourite religion P:5984, P:13869, P:24652 and espionage target rate
   P:16642 use getLeaderType(); all other reads (including AI_setEspionageWeight P:211) use
   getPersonalityType(). Under GAMEOPTION_RANDOM_PERSONALITIES one AI follows two leaders.
D5 AI_getDiplomacyVictoryStage (P:20735-20825) returns only 0, 1 or 3: AI_VICTORY_DIPLOMACY2 and
   DIPLOMACY4 are never set, so P:20859 (level-4 test) is dead; DOMINATION1 is set but never read.
D6 T:2855 AI_acceptSurrender: for MWR < 100 (Alexander, Boudica, Genghis, Montezuma, Ragnar, Shaka,
   Afonso, Basil, Ivan at 50, Masinissa 70, Augustus 90) MWR/100 = 0 and "valuable + threatened >=
   0" is always true: these leaders refuse every capitulation that is not forced by another team's
   success or war weariness, including ones that would end a costly war on good terms. The intent (a
   warmonger finishes conquests it can actually make) needs a real capacity test.
D7 Data: Cetshwayo has all five victory weights 0 (module file lines 24-28); Montezuma, Sitting Bull
   and Ivan have WCR 0 (2.3). Both turn personality into a strategic hole.
D8 rand-argument edge: P:17768 ask-for-help scales the rand by max(1, pct-60)/30 without a lower
   bound; for ContactRand 25..29 and pct <= 61 the result is 0 and rand(0) == 0 makes the contact
   certain whenever the 50-turn timer allows (trade tech has max(1, ...) at P:18176). Minor.

### 5.2 Suspicious (uncertain; intent unclear or needs measurement)
S1 Agenda CONQUEST has a peacetime floor of 3*(120-25) = 285 because enemyPower is clamped to >= 25
   (P:4480, P:4628-4631); with DAGGER this becomes 785 with no war plan at all.
S2 EXPAND_MARITIME = 130*min(coastal,8) (+180 when no land sites) reaches 1220 for a mature coastal
   empire with nothing left to settle, beating SCIENCE and CONSOLIDATE; may hold a peaceful naval
   empire in a 330-per-mille expansion posture.
S3 AIHierarchyPolicy.h:70 expansionHorizon = 24 - expansionBudget/40 - logistics/250: the expansion
   agendas get the SHORTEST settling horizon (about 15) and consolidate the longest (about 21); used
   as a hard cut at U:10988, U:17059, U:18120. Possibly inverted.
S4 P:21357: BIG_ESPIONAGE gains (100 - EspionageWeight)/10, so low-espionage leaders adopt it more
   often; the flag suppresses sabotage missions (P:14038-14178). Naming and effect look inverted.
S5 P:8551 force-peace vote uses VassalRefuseAttitudeThreshold for "secretary influence".
S6 Attack-odds change re-rolled every turn (P:16207): makes tactical choices non-stationary.
S7 One R for all victory rolls (P:20323-20789): inclinations are offsets of one number; e.g. with no
   options a leader can be culture- and diplomacy-inclined only if both windows overlap.
S8 Culture stage thresholds were written for 7 eras; with 8 eras (CIV4EraInfos.xml) stage 3 starts
   one era later (Modern/Transhuman) than in BTS.
S9 The total-war power filter uses 2/3 of the enemy's defensive power (T:4992) on top of ratios up
   to 130, then needs enemyPower < 140 to go live (T:4662); preparations against too-strong targets
   are probably common and wasted (needs log measurement).
S10 RELIGIOUS and SCIENTIFIC victories (CIV4VictoryInfo.xml) have no BBAI stage function; religious
   push (P:25283-25360) is situational and is disabled when culture stage > 1, so the culture dice
   also switch the religious plan off.

----------------------------------------------------------------------------------------------

## 6. Recommendations: personality should bias situational judgements, not replace them

Principle: keep each leader's identity as a bounded prior (+-10-20% on a utility, or a shifted
threshold), and compute the decision from observable state. Replace dice with hazards that scale with
opportunity and game speed.

R1 Attack odds (P:16193-16210; U:934, U:1012, U:24929). Remove rand+rand. Use a risk term from war
   success ratio, local reinforcement count, unit replacement turns and XP value, clamp to +-10;
   personality = base/2 (0..3). Keep the agenda term but symmetric (+-5).
R2 Raze (P:1733-1930). Compute keep value (pop, buildings, wonders, resources, culture, distance
   maintenance, reconquest risk) vs raze value (denial, unholdable, colony upkeep). Use RazeCityProb
   only as a +-15 tie-break and never above a value threshold (e.g. never raze pop >= 8 in our
   area).
R3 Wonders (C:2161, C:2449, C:3085, C:4074). Replace rand(WCR) by a deterministic per-leader bias
   (WCR/2) times wonder fit (flavor affinity, agenda, victory stage) and gate on competition (known
   rivals with the prerequisite tech, our production rank). Give WCR 0 leaders a floor (e.g. 15).
R4 Unit production (C:894-944, C:2508, C:3288, C:10905). Derive the peacetime unit roll and upkeep
   cap from threat (AI_getTotalAreaCityThreat, ALERT1/2, neighbour power ratio, war plan) and
   solvency; BUP becomes an offset of +-5 points. Make OWABWNW (P:21248) depend on nuke
   availability, enemy SDI and war state, with BUP as a small bias.
R5 War/peace timing (T:2870-3018, T:4857-5190, T:4748). Convert MWR/LWR/DWR into a threshold on
   AI_startWarVal and power ratio, evaluated every turn but with a hazard scaled by
   getTrainPercent()/100 (or VictoryDelayPercent) so wars per era are speed-invariant. Drive peace
   from war success, war weariness, enemy power and endWarVal every turn; MPR only as a bias on the
   required margin. Use the personality ratios to choose among targets, not to admit 1.95x stronger
   enemies.
R6 Surrender (T:2855). Replace MWR/100 with "we can take N more valuable cities within K turns given
   current power"; personality shifts K.
R7 Victory stages (P:20212-20825). Re-evaluate stage 1/2 periodically from feasibility (culture: top
   culture cities, wonders, holy cities, legendary ETA; space: tech rank and production; conquest/
   domination: power rank, land/pop share; diplomacy: vote share) with weight/100 as a prior, and
   allow dropping a stage. Value the Apollo tech (P:5844) by tech rank, not only SPACE2.
R8 Agenda (P:4533-4842). Make CULTURE score feasibility-based (e.g. legendary ETA vs rivals) instead
   of a constant 1100; add an explicit, documented personality prior (e.g. +-100 from flavors and
   victory weights) instead of the DAGGER/CULTURE2 side doors; review S1-S3; consider SPACE and
   DIPLOMACY agendas.
R9 Trade thresholds (T:1826-1870). Make the monopoly guard depend on the buyer's score rank and
   victory stage (never sell a monopoly tech to the closest rival); TechTradeKnownPercent shifts the
   threshold by +-20 only.
R10 Attitude: keep peace-weight compatibility but let it fade with shared enemies/religion; scale
   memory decay (P:15241) and contact timers by game speed.
R11 Consistency fixes: D1 (P:7746), D2 (P:7307/P:16904 sync rand), D3 (P:17695, P:17859), D4
   (getPersonalityType everywhere), D5 (produce diplomacy level 2/4 or remove the checks), D8 lower
   bound, and data fixes D7 (Cetshwayo weights, WCR floor).

Parameters that can stay random/static without hurting competence: improvement weight modifiers,
unitAI weight modifiers (deficit-only), flavor affinities (normalised and bounded), favourite civic
attitude, contact rands for flavour diplomacy, refusal thresholds (they are about relationships).

