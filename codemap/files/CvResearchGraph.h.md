# CvResearchGraph.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **15** `CvResearchGraph::CvResearchGraph(const CvPlayer &)`
  - calls: CvPlayer::getTeam [CvPlayer.cpp], CvTeamAI::getTeam [CvTeamAI.h]
  - called by (4): CvGameTextMgr::setTechTradeHelp, CvPlayer::findPathLength, CvPlayer::pushResearch, CvPlayerAI::AI_bestTech
- **20** `CvResearchGraph::numTechs()`
  - calls: CvGlobals::getNumTechInfos [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
- **21** `CvResearchGraph::numAndPrereqs()`
  - calls: CvGlobals::getNUM_AND_TECH_PREREQS [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
- **22** `CvResearchGraph::numOrPrereqs()`
  - calls: CvGlobals::getNUM_OR_TECH_PREREQS [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
- **23** `CvResearchGraph::andPrereq(int, int)`
  - calls: CvGlobals::getTechInfo(TechTypes) [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvTechInfo::getPrereqAndTechs [CvInfos.cpp]
- **24** `CvResearchGraph::orPrereq(int, int)`
  - calls: CvGlobals::getTechInfo(TechTypes) [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvTechInfo::getPrereqOrTechs [CvInfos.cpp]
- **26** `CvResearchGraph::satisfied(int)`
  - calls: CvPlayer::isResearchingTech [CvPlayer.cpp], CvTeam::isHasTech [CvTeam.cpp]
- **31** `CvResearchGraph::researchable(int)`
  - calls: CvPlayer::canEverResearch [CvPlayer.cpp]
- **33** `CvResearchGraph::cost(int)`
  - calls: CvTeam::getResearchCost [CvTeam.cpp]
