# CyArtFileMgrInterface.cpp

Group: Python wrappers. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **10** `CyArtFileMgrPythonInterface()`
  - takes the address of: CyArtFileMgr::Reset [CyArtFileMgr.cpp], CyArtFileMgr::buildArtFileInfoMaps [CyArtFileMgr.cpp], CyArtFileMgr::getInterfaceArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getMovieArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getMiscArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getUnitArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getBuildingArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getCivilizationArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getLeaderheadArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getBonusArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getImprovementArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getTerrainArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::getFeatureArtInfo [CyArtFileMgr.cpp], CyArtFileMgr::isNone [CyArtFileMgr.h]
  - called by (1): DLLPublishToPython
