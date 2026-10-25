# CvRandom.cpp

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **14** `CvRandom::CvRandom()` (exported)
  - calls: CvRandom::reset
  - called by (6): CvCity::getVisibleEffects, CvGame::CvGame, CvGlobals::init, CvMapGenerator::getRiverValueAtPlot, CvPlayer::getReligionLayerColors, CvPlayer::getTradeLayerColors
- **20** `CvRandom::~CvRandom()` (exported; virtual)
  - calls: CvRandom::uninit
  - called by (7): CvCity::getVisibleEffects, CvGame::CvGame, CvGame::~CvGame, CvMapGenerator::getRiverValueAtPlot, CvPlayer::getReligionLayerColors, CvPlayer::getTradeLayerColors, CvRandom::`vector deleting dtor'
- **26** `CvRandom::init(unsigned long)` (exported; Python: init)
  - calls: CvRandom::reset
  - called by (6): CvCity::getVisibleEffects, CvGame::init, CvMapGenerator::getRiverValueAtPlot, CvPlayer::getReligionLayerColors, CvPlayer::getTradeLayerColors, CyRandomPythonInterface
- **37** `CvRandom::uninit()`
  - called by (3): CvGame::uninit, CvRandom::reset, CvRandom::~CvRandom
- **44** `CvRandom::reset(unsigned long)`
  - calls: CvRandom::uninit
  - called by (4): CvGame::reset, CvRandom::CvRandom, CvRandom::init, CvRandom::read
- **54** `CvRandom::get(unsigned short, char const*)` (exported; Python: get)
  - calls: CvGlobals::getLogging [CvGlobals.cpp], CvGlobals::getRandLogging [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvGame::getTurnSlice [CvGame.cpp], CvGlobals::getGameINLINE [CvGlobals.h], CvRandom::getSeed, CvDLLUtilityIFaceBase::messageControlLog [CvDLLUtilityIFaceBase.h], CvGlobals::getDLLIFace [CvGlobals.h]
  - called by (20): CvCity::getVisibleEffects, CvCityAI::AI_bestBuildingThreshold, CvCityAI::AI_bestUnit, CvCityAI::AI_bestUnitAI, CvFractal::fracInitInternal, CvGame::getMapRandNum, CvGame::getNextSoundtrack, CvGame::getSorenRandNum, CvGame::init, CvMapGenerator::getRiverValueAtPlot, CvPlayer::doEspionageMission, CvPlayer::verifyAlive …
- **77** `CvRandom::getFloat()` (exported)
  - calls: CvRandom::get
  - called by (2): CvPlayer::getReligionLayerColors, CvPlayer::getTradeLayerColors
- **83** `CvRandom::reseed(unsigned long)`
  - called by (1): CvGame::read
- **89** `CvRandom::getSeed()` (exported)
  - called by (2): CvGame::calculateSyncChecksum, CvRandom::get
- **95** `CvRandom::read(FDataStreamBase*)`
  - calls: CvRandom::reset, FDataStreamBase::Read [FDataStreamBase.h]
  - called by (1): CvGame::read
- **103** `CvRandom::write(FDataStreamBase*)`
  - calls: FDataStreamBase::Write [FDataStreamBase.h]
  - called by (1): CvGame::write
