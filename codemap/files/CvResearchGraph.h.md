# CvResearchGraph.h

Group: other. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **17** `CvResearchGraph::CvResearchGraph(CvPlayer const&)`
  - calls: CvPlayer::getTeam [CvPlayer.cpp], CvTeamAI::getTeam [CvTeamAI.h]
  - called by (4): CvGameTextMgr::setTechTradeHelp, CvPlayer::findPathLength, CvPlayer::pushResearch, CvPlayerAI::AI_bestTech
- **20** `CvResearchGraph::numTechs() const`
  - calls: CvGlobals::getNumTechInfos [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
  - called by (1): ResearchPathPlan::Planner<CvResearchGraph>::Planner<class CvResearchGraph>
- **21** `CvResearchGraph::numAndPrereqs() const`
  - calls: CvGlobals::getNUM_AND_TECH_PREREQS [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
  - called by (5): ResearchPathPlan::Planner<CvResearchGraph>::computeForced, ResearchPathPlan::Planner<CvResearchGraph>::emit, ResearchPathPlan::Planner<CvResearchGraph>::resolve, ResearchPathPlan::Planner<CvResearchGraph>::treeSteps, ResearchPathPlan::Planner<CvResearchGraph>::visit
- **22** `CvResearchGraph::numOrPrereqs() const`
  - calls: CvGlobals::getNUM_OR_TECH_PREREQS [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h]
  - called by (4): ResearchPathPlan::Planner<CvResearchGraph>::alternatives, ResearchPathPlan::Planner<CvResearchGraph>::resolve, ResearchPathPlan::Planner<CvResearchGraph>::treeSteps, ResearchPathPlan::Planner<CvResearchGraph>::visit
- **23** `CvResearchGraph::andPrereq(int, int) const`
  - calls: CvGlobals::getTechInfo(TechTypes) [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvTechInfo::getPrereqAndTechs [CvInfos.cpp]
  - called by (5): ResearchPathPlan::Planner<CvResearchGraph>::computeForced, ResearchPathPlan::Planner<CvResearchGraph>::emit, ResearchPathPlan::Planner<CvResearchGraph>::resolve, ResearchPathPlan::Planner<CvResearchGraph>::treeSteps, ResearchPathPlan::Planner<CvResearchGraph>::visit
- **24** `CvResearchGraph::orPrereq(int, int) const`
  - calls: CvGlobals::getTechInfo(TechTypes) [CvGlobals.cpp], CvGlobals::getInstance [CvGlobals.h], CvTechInfo::getPrereqOrTechs [CvInfos.cpp]
  - called by (4): ResearchPathPlan::Planner<CvResearchGraph>::alternatives, ResearchPathPlan::Planner<CvResearchGraph>::resolve, ResearchPathPlan::Planner<CvResearchGraph>::treeSteps, ResearchPathPlan::Planner<CvResearchGraph>::visit
- **27** `CvResearchGraph::satisfied(int) const`
  - calls: CvPlayer::isResearchingTech [CvPlayer.cpp], CvTeam::isHasTech [CvTeam.cpp]
  - called by (2): ResearchPathPlan::Planner<CvResearchGraph>::resolve, ResearchPathPlan::Planner<CvResearchGraph>::treeSteps
- **31** `CvResearchGraph::researchable(int) const`
  - calls: CvPlayer::canEverResearch [CvPlayer.cpp]
  - called by (1): ResearchPathPlan::Planner<CvResearchGraph>::resolve
- **34** `CvResearchGraph::cost(int) const`
  - calls: CvTeam::getResearchCost [CvTeam.cpp]
  - called by (2): ResearchPathPlan::Planner<CvResearchGraph>::costOf, ResearchPathPlan::Planner<CvResearchGraph>::marginal
- **·** `ResearchPathPlan::Planner<CvResearchGraph>::~Planner<class CvResearchGraph>()` (written by the compiler)
  - called by (4): CvGameTextMgr::setTechTradeHelp, CvPlayer::findPathLength, CvPlayer::pushResearch, CvPlayerAI::AI_bestTech
