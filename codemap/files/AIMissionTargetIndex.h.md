# AIMissionTargetIndex.h

Group: AI. Functions in line order: what each calls (in order of first call), what it takes the address of, and who calls it. Callees in another file carry the file. A virtual callee lists its overrides after ⇢.

- **35** `AIMissionTargetIndex::Index::Index()`
  - called by (1): 
- **38** `AIMissionTargetIndex::Index::isCurrent(int, unsigned int, int) const`
  - called by (1): CvPlayerAI::AI_plotTargetMissionAIs(CvPlot*, MissionAITypes*, int, int&, CvSelectionGroup*, int) const
- **43** `AIMissionTargetIndex::Index::begin(int, unsigned int, int)`
  - called by (1): CvPlayerAI::AI_plotTargetMissionAIs(CvPlot*, MissionAITypes*, int, int&, CvSelectionGroup*, int) const
- **63** `AIMissionTargetIndex::Index::add(int, int, int, int, int, void const*)`
  - calls: AIMissionTargetIndex::Index::head
  - called by (1): CvPlayerAI::AI_plotTargetMissionAIs(CvPlot*, MissionAITypes*, int, int&, CvSelectionGroup*, int) const
- **90** `AIMissionTargetIndex::Index::count<struct `anonymous namespace'::MissionTargetMap, enum MissionAITypes>(`anonymous namespace'::MissionTargetMap const&, int, int, MissionAITypes const*, int, MissionAITypes, void const*, int, int&) const`
  - calls: `anonymous namespace'::MissionTargetMap::width [CvPlayerAI.cpp], `anonymous namespace'::MissionTargetMap::height [CvPlayerAI.cpp], AIMissionTargetIndex::Index::accumulate<struct `anonymous namespace'::MissionTargetMap, enum MissionAITypes>, `anonymous namespace'::MissionTargetMap::plotIndex [CvPlayerAI.cpp], AIMissionTargetIndex::Index::head
  - called by (1): CvPlayerAI::AI_plotTargetMissionAIs(CvPlot*, MissionAITypes*, int, int&, CvSelectionGroup*, int) const
- **133** `AIMissionTargetIndex::Index::head(int) const`
  - called by (2): AIMissionTargetIndex::Index::add, AIMissionTargetIndex::Index::count<struct `anonymous namespace'::MissionTargetMap, enum MissionAITypes>
- **143** `AIMissionTargetIndex::Index::accumulate<struct `anonymous namespace'::MissionTargetMap, enum MissionAITypes>(`anonymous namespace'::MissionTargetMap const&, AIMissionTargetIndex::Entry const&, int, int, MissionAITypes const*, int, MissionAITypes, void const*, int, int&, int&)` (static)
  - calls: `anonymous namespace'::MissionTargetMap::stepDistance [CvPlayerAI.cpp]
  - called by (1): AIMissionTargetIndex::Index::count<struct `anonymous namespace'::MissionTargetMap, enum MissionAITypes>
- **199** `AIMissionTargetIndex::UnitIndex::UnitIndex()`
  - called by (1): _$E11
- **203** `AIMissionTargetIndex::UnitIndex::noteQuery(int, unsigned int)`
  - called by (1): CvPlayerAI::AI_unitTargetMissionAIs(CvUnit*, MissionAITypes*, int, CvSelectionGroup*, int) const
- **216** `AIMissionTargetIndex::UnitIndex::isBuilt() const`
  - called by (1): CvPlayerAI::AI_unitTargetMissionAIs(CvUnit*, MissionAITypes*, int, CvSelectionGroup*, int) const
- **221** `AIMissionTargetIndex::UnitIndex::begin()`
  - called by (1): CvPlayerAI::AI_unitTargetMissionAIs(CvUnit*, MissionAITypes*, int, CvSelectionGroup*, int) const
- **239** `AIMissionTargetIndex::UnitIndex::add(int, int, int, int, void*)`
  - calls: AIMissionTargetIndex::UnitIndex::bucket, AIMissionTargetIndex::UnitIndex::head
  - called by (1): CvPlayerAI::AI_unitTargetMissionAIs(CvUnit*, MissionAITypes*, int, CvSelectionGroup*, int) const
- **261** `AIMissionTargetIndex::UnitIndex::visit<struct `anonymous namespace'::UnitTargetCounter>(int, int, `anonymous namespace'::UnitTargetCounter&) const`
  - calls: AIMissionTargetIndex::UnitIndex::bucket, AIMissionTargetIndex::UnitIndex::head, `anonymous namespace'::UnitTargetCounter::operator [CvPlayerAI.cpp]
  - called by (1): CvPlayerAI::AI_unitTargetMissionAIs(CvUnit*, MissionAITypes*, int, CvSelectionGroup*, int) const
- **274** `AIMissionTargetIndex::UnitIndex::bucket(int, int)` (static)
  - called by (2): AIMissionTargetIndex::UnitIndex::add, AIMissionTargetIndex::UnitIndex::visit<struct `anonymous namespace'::UnitTargetCounter>
- **280** `AIMissionTargetIndex::UnitIndex::head(int) const`
  - called by (2): AIMissionTargetIndex::UnitIndex::add, AIMissionTargetIndex::UnitIndex::visit<struct `anonymous namespace'::UnitTargetCounter>
